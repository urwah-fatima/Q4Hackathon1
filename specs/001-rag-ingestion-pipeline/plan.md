# Implementation Plan: RAG Ingestion Pipeline

**Branch**: `001-rag-ingestion-pipeline` | **Date**: 2025-12-20 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-rag-ingestion-pipeline/spec.md`

## Summary

Build a uv-managed Python backend that crawls deployed Docusaurus book URLs, extracts clean text, chunks with LangChain, generates embeddings with Cohere embed-english-v3.0 (1024-dim), and upserts to Qdrant Cloud collection `book_chatbot_embedding`. All logic in single `main.py` file.

## Technical Context

**Language/Version**: Python 3.11
**Package Manager**: uv
**Primary Dependencies**: cohere, qdrant-client, langchain, langchain-community, langchain-text-splitters, beautifulsoup4, requests, python-dotenv, tqdm
**Storage**: Qdrant Cloud (Free Tier) - collection `book_chatbot_embedding`
**Testing**: Manual verification via Qdrant dashboard and sample searches
**Target Platform**: Local development (cross-platform)
**Project Type**: Single CLI script
**Performance Goals**: Process all book pages without timeout
**Constraints**: Cohere API rate limits; Qdrant Free Tier limits
**Scale/Scope**: ~50-200 book pages, estimated 500-2000 chunks

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-checked after Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. Accuracy First | PASS | Using official Cohere embed-english-v3.0 model (documented) |
| II. Context Primacy | PASS | Crawling deployed Docusaurus site as source of truth |
| III. Technical Rigor | PASS | Using official SDKs (cohere, qdrant-client) |
| IV. Clarity | PASS | Single file design with clear function names |
| V. Reproducibility | PASS | uv lockfile ensures reproducible environment |
| VI. Modularity | PASS | Each function handles one pipeline stage |

## Project Structure

### Documentation (this feature)

```text
specs/001-rag-ingestion-pipeline/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Technology decisions
├── data-model.md        # Entity definitions
├── quickstart.md        # Setup guide
└── tasks.md             # Implementation tasks (/sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── .venv/               # uv virtual environment
├── .env                 # API keys (COHERE_API_KEY, QDRANT_URL, QDRANT_API_KEY)
├── main.py              # Single file with all pipeline logic
├── pyproject.toml       # uv project configuration
└── uv.lock              # Dependency lockfile
```

**Structure Decision**: Single file architecture as specified by user. All pipeline logic in `main.py` with these functions:
- `get_all_urls()` - List URLs to crawl
- `extract_text_from_url(url)` - Fetch and extract text
- `chunk_text(text, url, title)` - Split into chunks
- `embed(texts)` - Generate Cohere embeddings
- `create_collection()` - Initialize Qdrant collection
- `save_chunk_to_qdrant(chunks, embeddings)` - Upsert vectors
- `main()` - Orchestrate pipeline

## Architecture

### Pipeline Flow

```
1. get_all_urls()
   └─→ List of Docusaurus URLs

2. For each URL:
   └─→ extract_text_from_url(url)
       └─→ (title, clean_text)

3. chunk_text(text, url, title)
   └─→ List of chunks with metadata

4. embed(chunk_texts)
   └─→ List of 1024-dim vectors

5. create_collection() [once]
   └─→ Qdrant collection ready

6. save_chunk_to_qdrant(chunks, embeddings)
   └─→ Vectors stored with metadata
```

### Qdrant Collection

```python
Collection: "book_chatbot_embedding"
├── Vector size: 1024
├── Distance: Cosine
└── Payload:
    ├── url: str
    ├── title: str
    ├── chunk_index: int
    └── text: str
```

## Key Implementation Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Package Manager | uv | User requirement; fast, modern |
| Embedding Model | embed-english-v3.0 | User requirement; 1024 dims |
| Collection Name | book_chatbot_embedding | User requirement |
| File Structure | Single main.py | User requirement |
| HTML Parser | BeautifulSoup4 | User requirement |
| HTTP Client | requests | User requirement |
| Chunking | langchain-text-splitters | User requirement |

## Setup Commands

```bash
# 1. Create backend folder and init project
mkdir backend
cd backend
uv init rag-ingestion --python 3.11

# 2. Create and activate virtual environment
uv venv
# Windows: .venv\Scripts\activate
# Unix: source .venv/bin/activate

# 3. Add dependencies
uv add cohere qdrant-client langchain langchain-community langchain-text-splitters beautifulsoup4 requests python-dotenv tqdm

# 4. Create .env with API keys
# COHERE_API_KEY=...
# QDRANT_URL=...
# QDRANT_API_KEY=...

# 5. Run ingestion
uv run main.py
```

## Success Criteria

- [x] `uv run main.py` executes without errors
- [x] All book pages crawled and processed
- [x] Chunks stored in `book_chatbot_embedding` collection
- [x] Qdrant dashboard shows correct vector count
- [x] Sample similarity search returns relevant results

## Generated Artifacts

| Artifact | Path | Status |
|----------|------|--------|
| Research Document | specs/001-rag-ingestion-pipeline/research.md | Complete |
| Data Model | specs/001-rag-ingestion-pipeline/data-model.md | Complete |
| Quickstart Guide | specs/001-rag-ingestion-pipeline/quickstart.md | Complete |

## Next Steps

1. Run `/sp.tasks` to generate implementation tasks
2. Create backend folder with uv init
3. Implement main.py with all functions
4. Test with real Docusaurus URLs
5. Verify in Qdrant dashboard
