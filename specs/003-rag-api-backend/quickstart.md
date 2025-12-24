# Quickstart: RAG API Backend

**Feature**: 003-rag-api-backend
**Date**: 2025-12-21

## Prerequisites

- Completed 001-rag-ingestion-pipeline (Qdrant collection populated)
- Completed 002-retrieval-testing (retrieval quality verified)
- Existing backend/ folder with uv setup
- API keys: OPENAI_API_KEY, COHERE_API_KEY, QDRANT_URL, QDRANT_API_KEY

## Setup

### 1. Add Dependencies

```bash
cd backend
uv add fastapi uvicorn openai python-dotenv
# cohere and qdrant-client already exist from Spec-1
```

### 2. Update .env

Add OpenAI API key to existing .env:

```env
# Existing from Spec-1
COHERE_API_KEY=your-cohere-api-key
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your-qdrant-api-key

# New for Spec-3
OPENAI_API_KEY=your-openai-api-key
```

### 3. Create App Structure

```bash
cd backend
mkdir -p app
touch app/__init__.py
touch app/main.py
touch app/retriever.py
touch app/agent.py
touch app/models.py
touch app/config.py
```

### 4. Run the Server

```bash
uv run uvicorn app.main:app --reload
```

Server starts at http://localhost:8000

## Usage

### Single Question (POST /chat)

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is physical AI?"}'
```

**Response:**
```json
{
  "answer": "Physical AI refers to artificial intelligence systems that interact with the physical world...",
  "sources": [
    {
      "title": "Introduction to Physical AI",
      "url": "https://example.com/docs/intro",
      "chunk_index": 0,
      "score": 0.89,
      "snippet": "Physical AI refers to..."
    }
  ]
}
```

### Streaming Response (POST /chat/stream)

```bash
curl -X POST http://localhost:8000/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"question": "How do humanoid robots balance?"}'
```

**Response (SSE):**
```
data: {"token": "Humanoid"}

data: {"token": " robots"}

data: {"token": " maintain"}

...

data: {"done": true, "sources": [...]}
```

### Health Check (GET /health)

```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "ok",
  "version": "0.1.0",
  "dependencies": {
    "qdrant": "ok",
    "cohere": "ok",
    "openai": "ok"
  }
}
```

### Interactive API Docs

Visit http://localhost:8000/docs for Swagger UI

## Example Queries

Try these questions based on the book content:

1. "What is physical AI?"
2. "How do humanoid robots maintain balance?"
3. "What sensors are commonly used in robotics?"
4. "Explain reinforcement learning for robot control"
5. "What are the challenges of bipedal locomotion?"

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "OPENAI_API_KEY not set" | Add to .env file |
| "Collection not found" | Run ingestion first (Spec-1) |
| "Vector database unavailable" | Check QDRANT_URL and QDRANT_API_KEY |
| "Embedding service unavailable" | Check COHERE_API_KEY |
| Slow responses | Normal for LLM calls (~2-5 seconds) |
| "I don't have information" | Question is out of scope |

## Project Structure

```
backend/
├── app/
│   ├── __init__.py      # Package marker
│   ├── main.py          # FastAPI app, routes
│   ├── retriever.py     # Cohere + Qdrant
│   ├── agent.py         # OpenAI + prompts
│   ├── models.py        # Pydantic schemas
│   └── config.py        # Settings
├── main.py              # Ingestion script (Spec-1)
├── test_retrieval.py    # Testing CLI (Spec-2)
├── .env                 # API keys
├── pyproject.toml       # Dependencies
└── uv.lock              # Lock file
```

## Testing the RAG Flow

1. **Verify retrieval** (Spec-2 first):
   ```bash
   uv run test_retrieval.py query "What is physical AI?"
   ```

2. **Start API server**:
   ```bash
   uv run uvicorn app.main:app --reload
   ```

3. **Test chat endpoint**:
   ```bash
   curl -X POST http://localhost:8000/chat \
     -H "Content-Type: application/json" \
     -d '{"question": "What is physical AI?"}'
   ```

4. **Verify sources match retrieval results**

## Next Steps

After implementation:
1. Test all endpoints work correctly
2. Verify answers are grounded in book content
3. Test out-of-scope question handling
4. Ready for Spec-4 (Docusaurus chatbot integration)
