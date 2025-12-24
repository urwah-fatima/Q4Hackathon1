# Research: Retrieval Testing Pipeline

**Feature**: 002-retrieval-testing
**Date**: 2025-12-20
**Status**: Complete

## Technology Decisions

### 1. CLI Framework: Typer

**Decision**: Use `typer` for CLI interface

**Rationale**:
- User requirement specified typer for nice CLI
- Modern Python CLI framework with type hints
- Automatic help generation
- Simple command definition with decorators
- Good terminal output formatting

**Usage**:
```python
import typer
app = typer.Typer()

@app.command()
def query(text: str, top_k: int = 5):
    """Search the book content."""
    ...

if __name__ == "__main__":
    app()
```

---

### 2. Query Embedding: Cohere

**Decision**: Use Cohere `embed-english-v3.0` with `input_type="search_query"`

**Rationale**:
- Must match ingestion model for consistent embeddings
- `search_query` input type optimized for query embedding (vs `search_document` for documents)
- Same 1024-dimensional vectors

**Usage**:
```python
response = co.embed(
    texts=[query_text],
    model="embed-english-v3.0",
    input_type="search_query"  # Important: different from ingestion
)
```

---

### 3. Vector Search: Qdrant

**Decision**: Use Qdrant client's `search()` method

**Rationale**:
- Same collection as ingestion (`book_chatbot_embedding`)
- Built-in similarity scoring
- Payload retrieval for metadata

**Usage**:
```python
results = client.search(
    collection_name="book_chatbot_embedding",
    query_vector=query_embedding,
    limit=top_k,
    with_payload=True
)
```

---

### 4. Output Formatting

**Decision**: Use `rich` library for terminal output (comes with typer)

**Rationale**:
- Typer includes rich integration
- Pretty tables, colors, formatting
- Better readability for test results

---

### 5. Predefined Test Queries

**Decision**: Include 5+ diverse queries covering book topics

**Rationale**:
- Cover different sections/chapters
- Mix of specific and general queries
- Easy to extend

**Example Queries** (to be customized based on book content):
1. "What is physical AI?"
2. "How do humanoid robots balance?"
3. "What sensors are used in robotics?"
4. "Explain reinforcement learning for robots"
5. "What are the challenges of bipedal locomotion?"

---

## Dependency Summary

| Package | Purpose | Status |
|---------|---------|--------|
| typer | CLI framework | Add with uv |
| cohere | Query embedding | Already installed |
| qdrant-client | Vector search | Already installed |
| python-dotenv | Environment vars | Already installed |
| rich | Terminal formatting | Comes with typer |

**New Dependency**: `uv add typer`

## Environment Variables

Same as ingestion script:

| Variable | Description |
|----------|-------------|
| COHERE_API_KEY | Cohere API key |
| QDRANT_URL | Qdrant Cloud cluster URL |
| QDRANT_API_KEY | Qdrant Cloud API key |

## Configuration Defaults

| Setting | Default | Description |
|---------|---------|-------------|
| top_k | 5 | Number of results to return |
| threshold | 0.5 | Low relevance warning threshold |
| collection | book_chatbot_embedding | Qdrant collection name |
