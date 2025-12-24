# Research: RAG API Backend

**Feature**: 003-rag-api-backend
**Date**: 2025-12-21

## Research Questions

### RQ1: FastAPI Project Structure for RAG Backend

**Question**: What is the optimal FastAPI project structure for a RAG backend with multiple modules?

**Decision**: Modular app/ folder structure with separate files for concerns

**Rationale**:
- FastAPI best practices recommend separating routers, services, and models
- The app/ structure allows `uvicorn app.main:app` convention
- Separate files for retriever.py and agent.py enable clean testing and maintenance

**Alternatives Considered**:
- Single main.py file: Rejected - becomes unwieldy with RAG logic, streaming, and health checks
- src/ layout with setup.py: Rejected - overkill for API-only project

**Structure Chosen**:
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py         # FastAPI app, routers, health endpoint
│   ├── retriever.py    # Cohere embedding + Qdrant search
│   ├── agent.py        # Prompt building + OpenAI generation
│   ├── models.py       # Pydantic request/response schemas
│   └── config.py       # Environment variable loading
├── .env
├── pyproject.toml
└── uv.lock
```

### RQ2: OpenAI Chat Completion for RAG

**Question**: How to use OpenAI gpt-4o-mini for RAG answer generation with grounded responses?

**Decision**: Use ChatCompletion API with system prompt for grounding

**Rationale**:
- gpt-4o-mini is cost-effective ($0.15/1M input tokens) and fast
- System prompt can instruct the model to only use provided context
- Supports streaming for better UX

**Implementation Pattern**:
```python
from openai import OpenAI

client = OpenAI()

system_prompt = """You are a helpful assistant that answers questions about Physical AI and Humanoid Robotics.
You MUST only use the provided context to answer. If the context doesn't contain relevant information,
say "I don't have information about that in the book."
Always be accurate and cite the source when possible."""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
    ],
    stream=True  # For streaming endpoint
)
```

**Alternatives Considered**:
- gpt-4o: More capable but 10x cost - rejected for development/testing
- Claude via Anthropic API: Would work but adds another API key dependency

### RQ3: Streaming SSE Implementation in FastAPI

**Question**: How to implement Server-Sent Events (SSE) streaming in FastAPI?

**Decision**: Use `StreamingResponse` with async generator

**Rationale**:
- FastAPI's `StreamingResponse` handles SSE natively
- Async generator allows yielding tokens as they arrive from OpenAI
- Standard SSE format (`data: {...}\n\n`) works with EventSource API in browsers

**Implementation Pattern**:
```python
from fastapi.responses import StreamingResponse
import json

async def generate_stream():
    for chunk in response:  # OpenAI streaming response
        if chunk.choices[0].delta.content:
            token = chunk.choices[0].delta.content
            yield f"data: {json.dumps({'token': token})}\n\n"
    yield f"data: {json.dumps({'done': True, 'sources': sources})}\n\n"

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    return StreamingResponse(
        generate_stream(),
        media_type="text/event-stream"
    )
```

### RQ4: Error Handling Strategy

**Question**: How to handle external service failures gracefully?

**Decision**: Try/except blocks with HTTP 503 responses and detailed error messages

**Rationale**:
- 503 Service Unavailable is semantically correct for dependency failures
- Detailed error messages help debugging without exposing internals
- FastAPI's HTTPException provides clean error responses

**Implementation Pattern**:
```python
from fastapi import HTTPException

try:
    embeddings = cohere_client.embed(...)
except Exception as e:
    raise HTTPException(status_code=503, detail="Embedding service unavailable")

try:
    results = qdrant_client.search(...)
except Exception as e:
    raise HTTPException(status_code=503, detail="Vector database unavailable")
```

### RQ5: Cohere Query Embedding

**Question**: How to embed queries for search (vs documents)?

**Decision**: Use `input_type="search_query"` for query embeddings

**Rationale**:
- Cohere embed-english-v3.0 has asymmetric embeddings
- Documents use `input_type="search_document"` (done in ingestion)
- Queries use `input_type="search_query"` for optimal retrieval

**Implementation**:
```python
response = cohere_client.embed(
    texts=[question],
    model="embed-english-v3.0",
    input_type="search_query"
)
query_vector = response.embeddings[0]
```

## Technology Stack Summary

| Component | Choice | Version |
|-----------|--------|---------|
| Web Framework | FastAPI | 0.104+ |
| ASGI Server | uvicorn | 0.24+ |
| LLM | OpenAI gpt-4o-mini | Latest |
| Embeddings | Cohere embed-english-v3.0 | Latest |
| Vector DB | Qdrant Cloud | 1.7+ |
| Validation | Pydantic | 2.0+ |
| Package Manager | uv | Latest |

## Dependencies to Add

```bash
uv add fastapi uvicorn openai python-dotenv
# cohere and qdrant-client already exist from Spec-1
```

## References

- [FastAPI Project Structure Best Practices](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
- [OpenAI Chat Completions API](https://platform.openai.com/docs/api-reference/chat)
- [FastAPI StreamingResponse](https://fastapi.tiangolo.com/advanced/custom-response/#streamingresponse)
- [Cohere Embed Types](https://docs.cohere.com/reference/embed)
