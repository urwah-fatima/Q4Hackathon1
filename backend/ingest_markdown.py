"""
Quick markdown ingestion script - reads docs/*.md files directly.
"""

import hashlib
import os
import re
from pathlib import Path

import cohere
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams
from tqdm import tqdm

load_dotenv()

# Config
COLLECTION_NAME = "book_chatbot_embedding"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
EMBEDDING_DIM = 1024
BATCH_SIZE = 96
DOCS_PATH = Path(__file__).parent.parent / "docs"
BASE_URL = "http://localhost:3000"

# Clients
cohere_client = cohere.Client(os.getenv("COHERE_API_KEY"))
qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
)


def get_url_from_path(file_path: Path) -> str:
    """Convert file path to Docusaurus URL."""
    rel_path = file_path.relative_to(DOCS_PATH)
    # Remove .md extension and number prefix
    parts = []
    for part in rel_path.parts:
        if part.endswith('.md'):
            # Remove .md and leading number like "01-"
            name = part[:-3]
            name = re.sub(r'^\d+-', '', name)
            parts.append(name)
        else:
            parts.append(part)

    url_path = '/'.join(parts)
    return f"{BASE_URL}/{url_path}"


def extract_title(content: str, file_path: Path) -> str:
    """Extract title from markdown frontmatter or first heading."""
    # Check frontmatter
    if content.startswith('---'):
        end = content.find('---', 3)
        if end != -1:
            frontmatter = content[3:end]
            for line in frontmatter.split('\n'):
                if line.startswith('title:'):
                    return line.split(':', 1)[1].strip().strip('"\'')

    # Check first h1
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()

    # Fallback to filename
    return file_path.stem.replace('-', ' ').title()


def clean_markdown(content: str) -> str:
    """Remove frontmatter and clean markdown for embedding."""
    # Remove frontmatter
    if content.startswith('---'):
        end = content.find('---', 3)
        if end != -1:
            content = content[end + 3:].strip()

    # Remove code blocks (keep the code but remove the markers)
    content = re.sub(r'```\w*\n', '', content)
    content = re.sub(r'```', '', content)

    # Remove images
    content = re.sub(r'!\[.*?\]\(.*?\)', '', content)

    # Convert links to just text
    content = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', content)

    # Remove HTML tags
    content = re.sub(r'<[^>]+>', '', content)

    return content.strip()


def chunk_text(text: str, url: str, title: str) -> list[dict]:
    """Split text into chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    text_chunks = splitter.split_text(text)

    return [
        {"text": chunk, "url": url, "title": title, "chunk_index": i}
        for i, chunk in enumerate(text_chunks)
    ]


def embed(texts: list[str]) -> list[list[float]]:
    """Generate embeddings using Cohere."""
    all_embeddings = []

    for i in range(0, len(texts), BATCH_SIZE):
        batch = texts[i:i + BATCH_SIZE]
        response = cohere_client.embed(
            texts=batch,
            model="embed-english-v3.0",
            input_type="search_document",
        )
        all_embeddings.extend(response.embeddings)

    return all_embeddings


def generate_point_id(url: str, chunk_index: int) -> str:
    """Generate deterministic point ID."""
    unique_key = f"{url}::{chunk_index}"
    hash_bytes = hashlib.md5(unique_key.encode()).hexdigest()
    return f"{hash_bytes[:8]}-{hash_bytes[8:12]}-{hash_bytes[12:16]}-{hash_bytes[16:20]}-{hash_bytes[20:32]}"


def create_collection():
    """Create Qdrant collection if needed."""
    collections = qdrant_client.get_collections().collections
    collection_names = [c.name for c in collections]

    if COLLECTION_NAME not in collection_names:
        print(f"Creating collection: {COLLECTION_NAME}")
        qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=EMBEDDING_DIM, distance=Distance.COSINE),
        )
    else:
        print(f"Collection exists: {COLLECTION_NAME}")


def save_chunks_to_qdrant(chunks: list[dict], embeddings: list[list[float]]) -> int:
    """Save chunks to Qdrant."""
    points = [
        PointStruct(
            id=generate_point_id(chunk["url"], chunk["chunk_index"]),
            vector=embedding,
            payload={
                "url": chunk["url"],
                "title": chunk["title"],
                "chunk_index": chunk["chunk_index"],
                "text": chunk["text"],
            },
        )
        for chunk, embedding in zip(chunks, embeddings)
    ]

    batch_size = 100
    for i in range(0, len(points), batch_size):
        qdrant_client.upsert(collection_name=COLLECTION_NAME, points=points[i:i + batch_size])

    return len(points)


def main():
    print("\n=== Markdown Ingestion Pipeline ===")
    print(f"Docs path: {DOCS_PATH}")

    # Find all markdown files
    md_files = list(DOCS_PATH.rglob("*.md"))
    print(f"Found {len(md_files)} markdown files")

    # Create collection
    create_collection()

    # Process files
    all_chunks = []
    print("\nProcessing files...")

    for file_path in tqdm(md_files, desc="Reading"):
        content = file_path.read_text(encoding='utf-8')
        title = extract_title(content, file_path)
        clean_content = clean_markdown(content)
        url = get_url_from_path(file_path)

        if len(clean_content) < 100:
            print(f"  Skipping {file_path.name} (too short)")
            continue

        chunks = chunk_text(clean_content, url, title)
        all_chunks.extend(chunks)

    print(f"\nCreated {len(all_chunks)} chunks from {len(md_files)} files")

    if not all_chunks:
        print("No chunks to process!")
        return

    # Generate embeddings
    print("\nGenerating embeddings...")
    texts = [chunk["text"] for chunk in all_chunks]
    embeddings = embed(texts)
    print(f"Generated {len(embeddings)} embeddings")

    # Save to Qdrant
    print("\nSaving to Qdrant...")
    count = save_chunks_to_qdrant(all_chunks, embeddings)
    print(f"Saved {count} vectors")

    # Verify
    info = qdrant_client.get_collection(COLLECTION_NAME)
    print(f"\nCollection now has {info.points_count} points")
    print("\nDone!")


if __name__ == "__main__":
    main()
