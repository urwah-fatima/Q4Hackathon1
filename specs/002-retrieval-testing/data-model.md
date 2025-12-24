# Data Model: Retrieval Testing Pipeline

**Feature**: 002-retrieval-testing
**Date**: 2025-12-20
**Version**: 1.0

## Entity Overview

```
Query Text → embed_query() → search_qdrant() → format_results() → Display
                ↓                  ↓                  ↓
           QueryVector       SearchResults      FormattedOutput
```

## Entities

### SearchResult

A single result from Qdrant similarity search.

| Field | Type | Description |
|-------|------|-------------|
| score | float | Similarity score (0.0 - 1.0) |
| text | str | Chunk text content |
| url | str | Source page URL |
| title | str | Page title |
| chunk_index | int | Position in document |

**From Qdrant Payload**:
```python
{
    "url": "https://...",
    "title": "Page Title",
    "chunk_index": 0,
    "text": "Chunk content..."
}
```

---

### TestQuery

A predefined query for the test suite.

| Field | Type | Description |
|-------|------|-------------|
| text | str | Natural language query |
| topic | str | Expected topic area (for reference) |

**Example**:
```python
TEST_QUERIES = [
    {"text": "What is physical AI?", "topic": "Introduction"},
    {"text": "How do robots balance?", "topic": "Locomotion"},
    ...
]
```

---

## Function Signatures

```python
def embed_query(query: str) -> list[float]:
    """Embed query text using Cohere (input_type=search_query)."""

def search_qdrant(query_vector: list[float], top_k: int = 5) -> list[SearchResult]:
    """Search Qdrant collection and return results."""

def format_result(result: SearchResult, rank: int) -> str:
    """Format a single result for terminal display."""

def run_test_suite() -> None:
    """Run all predefined test queries."""

def interactive_mode() -> None:
    """Enter interactive query loop."""
```

---

## CLI Commands

```bash
# Single query
uv run test_retrieval.py query "What is physical AI?"

# Run test suite
uv run test_retrieval.py test

# Interactive mode
uv run test_retrieval.py interactive

# With options
uv run test_retrieval.py query "robots" --top-k 10
```

---

## Output Format

```
Query: "What is physical AI?"
═══════════════════════════════════════════════════════════════

[1] Score: 0.89
    Title: Introduction to Physical AI
    URL: https://example.com/docs/intro
    Chunk: 0
    ───────────────────────────────────────────────────────────
    Physical AI refers to artificial intelligence systems that
    interact with the physical world through sensors and actuators...

[2] Score: 0.76
    Title: Embodied Intelligence
    URL: https://example.com/docs/embodied
    Chunk: 2
    ───────────────────────────────────────────────────────────
    The concept of embodied AI builds on physical AI principles...

[3] Score: 0.45 ⚠️ Low relevance
    ...
```
