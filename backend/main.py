"""
RAG Ingestion Pipeline for Physical AI & Humanoid Robotics Book

This script crawls deployed Docusaurus book URLs, extracts text content,
generates embeddings using Cohere, and stores them in Qdrant Cloud.

Usage:
    uv run main.py           # Run full ingestion
    uv run main.py --verify  # Verify collection and test search
"""

import hashlib
import os
import time
from typing import Optional
import argparse

import cohere
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams
from tqdm import tqdm

# Load environment variables
load_dotenv()

# Configuration constants
COLLECTION_NAME = "book_chatbot_embedding"
CHUNK_SIZE = 500  # characters
CHUNK_OVERLAP = 50  # characters
EMBEDDING_DIM = 1024  # Cohere embed-english-v3.0 dimension
BATCH_SIZE = 96  # Cohere batch limit

# Base URL for the deployed Docusaurus site
# Change this to your deployed URL (e.g., Vercel, GitHub Pages)
BASE_URL = os.getenv("DOCUSAURUS_URL", "http://localhost:3000")

# Initialize clients
cohere_client = cohere.Client(os.getenv("COHERE_API_KEY"))
qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
)


def get_all_urls() -> list[str]:
    """
    Return list of all Docusaurus book URLs to crawl.

    The URL structure follows Docusaurus routing:
    - /intro for intro.md
    - /references for references.md
    - /module-X-name/chapter-slug for chapters

    Returns:
        List of fully qualified URLs to crawl
    """
    # URL paths based on Docusaurus routing (routeBasePath: '/')
    paths = [
        # Introduction
        "/intro",

        # Module 1: ROS 2 Foundations
        "/module-1-ros2/ros2-architecture",
        "/module-1-ros2/nodes-topics-services",
        "/module-1-ros2/actions-communication",
        "/module-1-ros2/rclpy-python-agents",
        "/module-1-ros2/urdf-humanoid-modeling",
        "/module-1-ros2/launch-files-parameters",

        # Module 2: Simulation
        "/module-2-simulation/gazebo-environment-setup",
        "/module-2-simulation/physics-simulation",
        "/module-2-simulation/urdf-sdf-usage",
        "/module-2-simulation/unity-visualization",
        "/module-2-simulation/sensor-simulation",
        "/module-2-simulation/validation-strategies",

        # Module 3: Isaac
        "/module-3-isaac/isaac-sim-synthetic-data",
        "/module-3-isaac/isaac-ros-vslam",
        "/module-3-isaac/nav2-humanoid-navigation",
        "/module-3-isaac/reinforcement-learning",
        "/module-3-isaac/sim-to-real-transfer",
        "/module-3-isaac/ros2-isaac-integration",

        # Module 4: VLA
        "/module-4-vla/speech-to-command",
        "/module-4-vla/llm-task-decomposition",
        "/module-4-vla/multimodal-perception",
        "/module-4-vla/capstone-autonomous-humanoid",
        "/module-4-vla/edge-deployment",
        "/module-4-vla/evaluation-testing",

        # References
        "/references",
    ]

    # Remove duplicates while preserving order
    seen = set()
    unique_paths = []
    for path in paths:
        if path not in seen:
            seen.add(path)
            unique_paths.append(path)

    return [f"{BASE_URL}{path}" for path in unique_paths]


def extract_text_from_url(url: str) -> tuple[Optional[str], Optional[str]]:
    """
    Fetch and extract clean text content from a Docusaurus page.

    Args:
        url: Full URL to fetch

    Returns:
        Tuple of (title, clean_text) or (None, None) on error
    """
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"  [WARN] Failed to fetch {url}: {e}")
        return None, None

    soup = BeautifulSoup(response.text, "html.parser")

    # Extract title
    title_tag = soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else url.split("/")[-1]

    # Extract main content (Docusaurus uses article or main tag)
    content_container = soup.find("article") or soup.find("main")

    if not content_container:
        print(f"  [WARN] No content found for {url}")
        return None, None

    # Remove navigation, buttons, and other non-content elements
    for element in content_container.find_all(["nav", "button", "script", "style", "footer", "aside"]):
        element.decompose()

    # Remove table of contents
    for toc in content_container.find_all(class_=lambda x: x and "toc" in x.lower()):
        toc.decompose()

    # Remove pagination
    for pagination in content_container.find_all(class_=lambda x: x and "pagination" in x.lower()):
        pagination.decompose()

    # Get clean text
    text = content_container.get_text(separator="\n", strip=True)

    # Skip if too little content
    if len(text) < 100:
        print(f"  [WARN] Insufficient content for {url} ({len(text)} chars)")
        return None, None

    return title, text


def chunk_text(text: str, url: str, title: str) -> list[dict]:
    """
    Split text into chunks suitable for embedding and retrieval.

    Args:
        text: Full page text content
        url: Source URL for metadata
        title: Page title for metadata

    Returns:
        List of chunk dictionaries with text and metadata
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    text_chunks = splitter.split_text(text)

    chunks = []
    for i, chunk_text in enumerate(text_chunks):
        chunks.append({
            "text": chunk_text,
            "url": url,
            "title": title,
            "chunk_index": i,
        })

    return chunks


def embed(texts: list[str]) -> list[list[float]]:
    """
    Generate embeddings using Cohere embed-english-v3.0.

    Args:
        texts: List of text strings to embed

    Returns:
        List of embedding vectors (1024-dim each)
    """
    all_embeddings = []

    # Process in batches to respect API limits
    for i in range(0, len(texts), BATCH_SIZE):
        batch = texts[i:i + BATCH_SIZE]

        try:
            response = cohere_client.embed(
                texts=batch,
                model="embed-english-v3.0",
                input_type="search_document",
            )
            all_embeddings.extend(response.embeddings)
        except cohere.errors.TooManyRequestsError:
            print("  [WARN] Rate limited, waiting 60 seconds...")
            time.sleep(60)
            # Retry the batch
            response = cohere_client.embed(
                texts=batch,
                model="embed-english-v3.0",
                input_type="search_document",
            )
            all_embeddings.extend(response.embeddings)
        except Exception as e:
            print(f"  [ERROR] Cohere API error: {e}")
            raise

    return all_embeddings


def generate_point_id(url: str, chunk_index: int) -> str:
    """
    Generate deterministic point ID from URL and chunk index.

    This ensures idempotent upserts - re-running the pipeline
    updates existing records instead of creating duplicates.

    Args:
        url: Source URL
        chunk_index: Chunk position within the page

    Returns:
        UUID-compatible string ID
    """
    unique_key = f"{url}::{chunk_index}"
    hash_bytes = hashlib.md5(unique_key.encode()).hexdigest()
    # Convert to UUID format for Qdrant compatibility
    return f"{hash_bytes[:8]}-{hash_bytes[8:12]}-{hash_bytes[12:16]}-{hash_bytes[16:20]}-{hash_bytes[20:32]}"


def create_collection() -> None:
    """
    Create Qdrant collection if it doesn't exist.

    Collection configuration:
    - Vector size: 1024 (Cohere embed-english-v3.0)
    - Distance: Cosine similarity
    """
    collections = qdrant_client.get_collections().collections
    collection_names = [c.name for c in collections]

    if COLLECTION_NAME not in collection_names:
        print(f"[INFO] Creating collection: {COLLECTION_NAME}")
        qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=EMBEDDING_DIM,
                distance=Distance.COSINE,
            ),
        )
    else:
        print(f"[INFO] Collection already exists: {COLLECTION_NAME}")


def save_chunks_to_qdrant(chunks: list[dict], embeddings: list[list[float]]) -> int:
    """
    Upsert chunks with embeddings to Qdrant.

    Uses deterministic IDs for idempotent updates.

    Args:
        chunks: List of chunk dictionaries with metadata
        embeddings: Corresponding embedding vectors

    Returns:
        Number of points upserted
    """
    points = []
    for chunk, embedding in zip(chunks, embeddings):
        point_id = generate_point_id(chunk["url"], chunk["chunk_index"])
        points.append(
            PointStruct(
                id=point_id,
                vector=embedding,
                payload={
                    "url": chunk["url"],
                    "title": chunk["title"],
                    "chunk_index": chunk["chunk_index"],
                    "text": chunk["text"],
                },
            )
        )

    # Upsert in batches
    batch_size = 100
    for i in range(0, len(points), batch_size):
        batch = points[i:i + batch_size]
        qdrant_client.upsert(
            collection_name=COLLECTION_NAME,
            points=batch,
        )

    return len(points)


def verify_collection() -> dict:
    """
    Verify collection exists and report statistics.

    Returns:
        Dictionary with collection stats
    """
    try:
        collection_info = qdrant_client.get_collection(COLLECTION_NAME)
        return {
            "status": "ok",
            "points_count": collection_info.points_count,
            "vectors_count": collection_info.vectors_count,
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
        }


def test_search(query: str, top_k: int = 3) -> list[dict]:
    """
    Perform a test similarity search.

    Args:
        query: Search query text
        top_k: Number of results to return

    Returns:
        List of search results with scores
    """
    # Embed query with search_query input type
    response = cohere_client.embed(
        texts=[query],
        model="embed-english-v3.0",
        input_type="search_query",
    )
    query_vector = response.embeddings[0]

    # Search Qdrant
    results = qdrant_client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k,
    )

    return [
        {
            "score": hit.score,
            "title": hit.payload.get("title", "Unknown"),
            "url": hit.payload.get("url", ""),
            "text": hit.payload.get("text", "")[:200] + "...",
        }
        for hit in results
    ]


def main():
    """
    Main pipeline orchestration.

    Crawls all book URLs, chunks content, generates embeddings,
    and stores in Qdrant with progress tracking.
    """
    parser = argparse.ArgumentParser(description="RAG Ingestion Pipeline")
    parser.add_argument("--verify", action="store_true", help="Verify collection and test search")
    args = parser.parse_args()

    if args.verify:
        print("\n[VERIFY] Verifying collection...")
        stats = verify_collection()
        print(f"  Collection: {COLLECTION_NAME}")
        print(f"  Status: {stats.get('status')}")
        if stats.get("status") == "ok":
            print(f"  Points: {stats.get('points_count')}")
            print(f"  Vectors: {stats.get('vectors_count')}")

            print("\n[TEST] Testing search with query: 'What is ROS 2?'")
            results = test_search("What is ROS 2?")
            for i, result in enumerate(results, 1):
                print(f"\n  Result {i} (score: {result['score']:.4f}):")
                print(f"    Title: {result['title']}")
                print(f"    URL: {result['url']}")
                print(f"    Text: {result['text']}")
        else:
            print(f"  Error: {stats.get('message')}")
        return

    print("\n=== RAG Ingestion Pipeline ===")
    print(f"  Collection: {COLLECTION_NAME}")
    print(f"  Chunk size: {CHUNK_SIZE} chars")
    print(f"  Overlap: {CHUNK_OVERLAP} chars")
    print(f"  Base URL: {BASE_URL}")

    # Step 1: Get all URLs
    urls = get_all_urls()
    print(f"\n[INFO] Found {len(urls)} URLs to process")

    # Step 2: Create collection
    create_collection()

    # Step 3: Process each URL
    all_chunks = []
    failed_urls = []

    print("\n[STEP] Extracting content from URLs...")
    for url in tqdm(urls, desc="Crawling"):
        title, text = extract_text_from_url(url)
        if title and text:
            chunks = chunk_text(text, url, title)
            all_chunks.extend(chunks)
        else:
            failed_urls.append(url)

    print(f"\n[INFO] Created {len(all_chunks)} chunks from {len(urls) - len(failed_urls)} pages")

    if not all_chunks:
        print("[ERROR] No chunks to process. Check if the Docusaurus site is running.")
        return

    # Step 4: Generate embeddings
    print("\n[STEP] Generating embeddings...")
    texts = [chunk["text"] for chunk in all_chunks]
    embeddings = embed(texts)
    print(f"  Generated {len(embeddings)} embeddings")

    # Step 5: Store in Qdrant
    print("\n[STEP] Storing in Qdrant...")
    count = save_chunks_to_qdrant(all_chunks, embeddings)
    print(f"  Upserted {count} vectors")

    # Summary
    print("\n[SUCCESS] Ingestion complete!")
    print(f"  Total chunks: {len(all_chunks)}")
    print(f"  Failed URLs: {len(failed_urls)}")
    if failed_urls:
        print("  Failed URLs:")
        for url in failed_urls:
            print(f"    - {url}")

    # Verify
    print("\n[VERIFY] Verification:")
    stats = verify_collection()
    print(f"  Points in collection: {stats.get('points_count', 'N/A')}")


if __name__ == "__main__":
    main()
