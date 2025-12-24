# Research: RAG Ingestion Pipeline

**Feature**: 001-rag-ingestion-pipeline
**Date**: 2025-12-20
**Status**: Complete

## Technology Decisions

### 1. Project Management: uv

**Decision**: Use `uv` for Python project and dependency management

**Rationale**:
- Modern, fast Python package manager (10-100x faster than pip)
- Built-in virtual environment management
- Lockfile support for reproducible builds
- Single tool for init, venv, add, and run commands

**Commands**:
```bash
uv init rag-ingestion --python 3.11
cd backend
uv venv
uv add cohere qdrant-client langchain langchain-community langchain-text-splitters beautifulsoup4 requests python-dotenv tqdm
uv run main.py
```

---

### 2. Cohere Embedding Model

**Decision**: Use `embed-english-v3.0` with 1024 dimensions

**Rationale**:
- Specified in user requirements
- 1024 dimensions - good balance of quality and storage
- Optimized for English text (book content is English)
- Well-documented API with Python SDK

**API Usage**:
```python
import cohere
co = cohere.Client(api_key=os.getenv("COHERE_API_KEY"))
response = co.embed(
    texts=["text chunk"],
    model="embed-english-v3.0",
    input_type="search_document"
)
```

---

### 3. Vector Database: Qdrant Cloud

**Decision**: Use Qdrant Cloud with collection `book_chatbot_embedding`

**Rationale**:
- Free tier available for development
- Native Python client with upsert support
- Cosine distance for semantic similarity
- 1024-dimensional vectors matching Cohere output

**Collection Config**:
- Name: `book_chatbot_embedding`
- Vector size: 1024
- Distance: Cosine

---

### 4. HTML Extraction

**Decision**: Use `BeautifulSoup4` with `requests`

**Rationale**:
- Specified in user requirements
- Simple, well-established libraries
- Sufficient for static Docusaurus content
- Easy to extract specific content selectors

---

### 5. Text Chunking

**Decision**: Use `langchain-text-splitters` with RecursiveCharacterTextSplitter

**Rationale**:
- Specified in user requirements (langchain ecosystem)
- Preserves document structure
- Configurable chunk size and overlap
- Handles various text formats

**Configuration**:
- Chunk size: ~1000 characters
- Overlap: ~200 characters

---

### 6. Single File Architecture

**Decision**: All logic in `main.py` with these functions:
- `get_all_urls()` - Discover/list URLs to crawl
- `extract_text_from_url(url)` - Fetch and extract clean text
- `chunk_text(text, metadata)` - Split text into chunks
- `embed(chunks)` - Generate Cohere embeddings
- `create_collection()` - Initialize Qdrant collection
- `save_chunk_to_qdrant(chunks, embeddings)` - Upsert vectors
- `main()` - Orchestrate pipeline

**Rationale**:
- User explicitly requested single file design
- Simpler for initial implementation
- Easy to run with `uv run main.py`

---

## Dependency Summary

| Package | Purpose |
|---------|---------|
| cohere | Embedding generation API |
| qdrant-client | Vector database client |
| langchain | LangChain core |
| langchain-community | Community integrations |
| langchain-text-splitters | Text chunking |
| beautifulsoup4 | HTML parsing |
| requests | HTTP requests |
| python-dotenv | Environment variables |
| tqdm | Progress bars |

## Environment Variables

| Variable | Description |
|----------|-------------|
| COHERE_API_KEY | Cohere API key |
| QDRANT_URL | Qdrant Cloud cluster URL |
| QDRANT_API_KEY | Qdrant Cloud API key |
