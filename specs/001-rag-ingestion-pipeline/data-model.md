# Data Model: RAG Ingestion Pipeline

**Feature**: 001-rag-ingestion-pipeline
**Date**: 2025-12-20
**Version**: 1.0

## Entity Overview

```
URLs List → extract_text_from_url() → chunk_text() → embed() → save_chunk_to_qdrant()
                     ↓                      ↓            ↓              ↓
               PageContent            TextChunk    Embedding      VectorRecord
```

## Entities

### PageContent

Extracted content from a single URL.

| Field | Type | Description |
|-------|------|-------------|
| url | str | Source URL |
| title | str | Page title |
| content | str | Clean extracted text |

---

### TextChunk

A segment of page content for embedding.

| Field | Type | Description |
|-------|------|-------------|
| text | str | Chunk text content |
| metadata | dict | Contains url, title, chunk_index |

**Metadata Structure**:
```python
{
    "url": "https://...",
    "title": "Page Title",
    "chunk_index": 0
}
```

---

### VectorRecord (Qdrant Point)

Stored in Qdrant collection `book_chatbot_embedding`.

| Field | Type | Description |
|-------|------|-------------|
| id | str/int | Unique point ID |
| vector | list[float] | 1024-dim embedding |
| payload | dict | Metadata (url, title, chunk_index, text) |

**Qdrant Payload Structure**:
```python
{
    "url": "https://...",
    "title": "Page Title",
    "chunk_index": 0,
    "text": "Chunk content..."
}
```

---

## Qdrant Collection Configuration

**Collection Name**: `book_chatbot_embedding`

```python
from qdrant_client.models import Distance, VectorParams

client.create_collection(
    collection_name="book_chatbot_embedding",
    vectors_config=VectorParams(
        size=1024,
        distance=Distance.COSINE
    )
)
```

## Function Signatures

```python
def get_all_urls() -> list[str]:
    """Return list of Docusaurus URLs to crawl."""

def extract_text_from_url(url: str) -> tuple[str, str]:
    """Fetch URL and return (title, clean_text)."""

def chunk_text(text: str, url: str, title: str) -> list[dict]:
    """Split text into chunks with metadata."""

def embed(texts: list[str]) -> list[list[float]]:
    """Generate Cohere embeddings for text list."""

def create_collection() -> None:
    """Create Qdrant collection if not exists."""

def save_chunk_to_qdrant(chunks: list[dict], embeddings: list[list[float]]) -> None:
    """Upsert chunks with embeddings to Qdrant."""

def main() -> None:
    """Orchestrate full ingestion pipeline."""
```
