# Quickstart: RAG Ingestion Pipeline

**Feature**: 001-rag-ingestion-pipeline
**Date**: 2025-12-20

## Prerequisites

- Python 3.11+
- uv (install: `curl -LsSf https://astral.sh/uv/install.sh | sh`)
- Cohere API key (https://dashboard.cohere.com/)
- Qdrant Cloud account (https://cloud.qdrant.io/)

## Setup

### 1. Initialize Project

```bash
mkdir backend
cd backend
uv init rag-ingestion --python 3.11
uv venv
# Windows: .venv\Scripts\activate
# Unix: source .venv/bin/activate
```

### 2. Install Dependencies

```bash
uv add cohere qdrant-client langchain langchain-community langchain-text-splitters beautifulsoup4 requests python-dotenv tqdm
```

### 3. Configure Environment

Create `.env` file in backend folder:

```env
COHERE_API_KEY=your-cohere-api-key
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your-qdrant-api-key
```

### 4. Create main.py

Create `main.py` with the pipeline functions:
- `get_all_urls()`
- `extract_text_from_url(url)`
- `chunk_text(text, url, title)`
- `embed(texts)`
- `create_collection()`
- `save_chunk_to_qdrant(chunks, embeddings)`
- `main()`

## Usage

### Run Ingestion

```bash
uv run main.py
```

### Expected Output

```
Fetching URLs...
Found 25 pages to process
Processing: Introduction to Physical AI
  Extracted 4523 characters
  Created 5 chunks
  Generated embeddings
  Saved to Qdrant
...
Ingestion complete: 125 chunks stored
```

## Verification

Check Qdrant Dashboard:
1. Navigate to your Qdrant Cloud cluster
2. Open collection `book_chatbot_embedding`
3. Verify vector count matches expected chunks
4. Run sample search to test similarity

## Project Structure

```
backend/
├── .venv/              # Virtual environment
├── .env                # API keys (not committed)
├── main.py             # Single file with all pipeline logic
├── pyproject.toml      # uv project config
└── uv.lock            # Dependency lockfile
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "COHERE_API_KEY not set" | Check .env file exists and is loaded |
| "Connection refused" | Verify QDRANT_URL is correct |
| "Rate limit exceeded" | Add delays between API calls |
| Empty content | Check URL is accessible |
