# Implementation Plan: RAG API Backend

**Branch**: `003-rag-api-backend` | **Date**: 2025-12-21 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-rag-api-backend/spec.md`

## Summary

Create a FastAPI backend (`app/`) with OpenAI-powered RAG agent for book Q&A. The API embeds questions with Cohere, retrieves relevant chunks from Qdrant, builds a grounded prompt, and generates answers using gpt-4o-mini. Includes streaming support and health monitoring.

## Technical Context

**Language/Version**: Python 3.11
**Package Manager**: uv (existing project)
**Primary Dependencies**: fastapi, uvicorn, openai, cohere, qdrant-client, python-dotenv, pydantic
**Storage**: Qdrant Cloud - collection `book_chatbot_embedding` (existing)
**Testing**: Manual verification via curl and Swagger UI
**Target Platform**: Local development (cross-platform), deployed API
**Project Type**: Modular API application (app/ folder)
**Performance Goals**: < 5 seconds p95 response latency
**Constraints**: < 512MB memory, handle 10 concurrent requests
**Scale/Scope**: Development tool, single deployment

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-checked after Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. Accuracy First | PASS | Uses gpt-4o-mini with grounding prompt to ensure factual responses from indexed content |
| II. Context Primacy | PASS | RAG retrieves from indexed book content; answers grounded in source documents |
| III. Technical Rigor | PASS | Uses official SDKs (OpenAI, Cohere, Qdrant); follows FastAPI best practices |
| IV. Clarity | PASS | API contracts defined with Pydantic schemas; OpenAPI docs auto-generated |
| V. Reproducibility | PASS | Environment variables for configuration; same embedding model as ingestion |
| VI. Modularity | PASS | Separate modules (retriever, agent, models); clear separation of concerns |

## Project Structure

### Documentation (this feature)

```text
specs/003-rag-api-backend/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Technology decisions
├── data-model.md        # Entity definitions
├── quickstart.md        # Usage guide
└── tasks.md             # Implementation tasks (/sp.tasks)
```

### Source Code (extends existing backend/)

```text
backend/
├── app/
│   ├── __init__.py      # Package marker
│   ├── main.py          # FastAPI app, routes, health
│   ├── retriever.py     # Cohere embedding + Qdrant search
│   ├── agent.py         # Prompt building + OpenAI generation
│   ├── models.py        # Pydantic request/response schemas
│   └── config.py        # Settings from environment
├── main.py              # Ingestion script (Spec-1)
├── test_retrieval.py    # Testing CLI (Spec-2)
├── .env                 # API keys (add OPENAI_API_KEY)
├── pyproject.toml       # Add new dependencies
└── uv.lock              # Updated lockfile
```

**Structure Decision**: Modular `app/` folder with separate files for retriever, agent, and models. This enables clean testing, maintenance, and follows FastAPI's recommended structure for larger applications.

## Architecture

### RAG Flow

```
1. User sends: POST /chat {"question": "What is physical AI?"}
                │
                ▼
2. retriever.py: embed_query(question)
   └─→ Cohere API (embed-english-v3.0, input_type="search_query")
   └─→ Returns: 1024-dim query vector
                │
                ▼
3. retriever.py: search_qdrant(query_vector, top_k=5)
   └─→ Qdrant search on book_chatbot_embedding
   └─→ Returns: List of chunks with scores and payloads
                │
                ▼
4. agent.py: build_context(chunks)
   └─→ Formats chunks into context string
   └─→ Adds system prompt for grounding
                │
                ▼
5. agent.py: generate_answer(context, question)
   └─→ OpenAI gpt-4o-mini chat completion
   └─→ Returns: Generated answer
                │
                ▼
6. main.py: format_response(answer, chunks)
   └─→ Returns: {"answer": "...", "sources": [...]}
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/chat` | POST | Single question → answer + sources |
| `/chat/stream` | POST | Streaming answer (SSE) |
| `/health` | GET | Dependency health check |
| `/docs` | GET | Swagger UI (auto-generated) |

### Module Responsibilities

| Module | Responsibility |
|--------|---------------|
| `main.py` | FastAPI app, route definitions, error handling |
| `retriever.py` | Cohere client, embed_query(), Qdrant client, search() |
| `agent.py` | System prompt, build_context(), generate_answer(), stream_answer() |
| `models.py` | Pydantic schemas (ChatRequest, ChatResponse, Source, etc.) |
| `config.py` | Settings class, environment loading |

## Key Implementation Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| LLM Model | gpt-4o-mini | Cost-effective ($0.15/1M input), fast, sufficient quality |
| Project Structure | app/ folder | Clean module separation, follows FastAPI conventions |
| Streaming | SSE via StreamingResponse | Native FastAPI support, works with EventSource API |
| Error Handling | HTTPException with 503 | Semantically correct for dependency failures |
| Grounding | System prompt | Instructs LLM to only use provided context |

## Grounding Strategy

The system prompt ensures answers are grounded in retrieved content:

```python
SYSTEM_PROMPT = """You are a helpful assistant that answers questions about Physical AI and Humanoid Robotics based on the provided book content.

IMPORTANT RULES:
1. ONLY use information from the provided context to answer
2. If the context doesn't contain relevant information, say "I don't have information about that in the book."
3. Be accurate and cite the source when possible
4. Keep answers concise but complete
5. Do not make up or infer information not in the context"""
```

## Setup Commands

```bash
# Add new dependencies
cd backend
uv add fastapi uvicorn openai

# Add OPENAI_API_KEY to .env
echo "OPENAI_API_KEY=your-key" >> .env

# Create app structure
mkdir -p app
touch app/__init__.py app/main.py app/retriever.py app/agent.py app/models.py app/config.py

# Run the server
uv run uvicorn app.main:app --reload
```

## Success Criteria

- [ ] `uv run uvicorn app.main:app --reload` starts server at localhost:8000
- [ ] POST /chat returns relevant answers with sources
- [ ] POST /chat/stream streams tokens progressively
- [ ] GET /health returns dependency status
- [ ] Answers are grounded in retrieved book content
- [ ] Out-of-scope questions return "I don't have information" message
- [ ] Error responses use appropriate HTTP status codes

## Generated Artifacts

| Artifact | Path | Status |
|----------|------|--------|
| Research Document | specs/003-rag-api-backend/research.md | Complete |
| Data Model | specs/003-rag-api-backend/data-model.md | Complete |
| Quickstart Guide | specs/003-rag-api-backend/quickstart.md | Complete |

## Next Steps

1. Run `/sp.tasks` to generate implementation tasks
2. Add dependencies: `uv add fastapi uvicorn openai`
3. Create app/ folder structure
4. Implement modules in order: config → models → retriever → agent → main
5. Test with curl and Swagger UI
6. Verify answers match expected book content
