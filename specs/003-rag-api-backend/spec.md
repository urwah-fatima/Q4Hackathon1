# Feature Specification: RAG API Backend

**Feature**: 003-rag-api-backend
**Branch**: `003-rag-api-backend`
**Date**: 2025-12-21
**Status**: Draft

## Overview

FastAPI backend with OpenAI-powered RAG agent for book Q&A. Provides a reliable API endpoint that answers questions using only the book's indexed content via retrieval-augmented generation.

## Target Audience

- Embedded chatbot in the Docusaurus frontend (spec-4)
- Developers testing the API directly

## Dependencies

- **Spec-1** (001-rag-ingestion-pipeline): Qdrant collection with embedded book content
- **Spec-2** (002-retrieval-testing): Verified retrieval quality

## User Stories

### US1: Answer Book Questions via API (Priority: P1)

**As a** frontend chatbot widget
**I want to** send questions to a REST API and receive answers with sources
**So that** users can get accurate answers from the book content

**Acceptance Criteria:**
- POST /chat endpoint accepts `{"question": "string"}`
- Response includes `{"answer": "string", "sources": [...]}`
- Answer is generated using only retrieved book content
- Sources include page title, URL, and relevance score
- Response time < 5 seconds for typical queries

### US2: Stream Responses for Better UX (Priority: P2)

**As a** frontend developer
**I want to** receive streaming responses
**So that** users see answers appearing progressively

**Acceptance Criteria:**
- POST /chat/stream endpoint available
- Response uses text/event-stream content type
- Tokens stream as they're generated
- Final event includes sources array
- Client can cancel mid-stream

### US3: Health and Status Monitoring (Priority: P3)

**As a** DevOps engineer
**I want to** check API health and dependencies
**So that** I can monitor system availability

**Acceptance Criteria:**
- GET /health returns `{"status": "ok"}` when healthy
- GET /health checks Qdrant and Cohere connectivity
- Returns appropriate error status when dependencies fail
- Response includes version information

## Functional Requirements

### API Endpoints

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-01 | POST /chat accepts JSON body with `question` field | P1 |
| FR-02 | POST /chat returns JSON with `answer` and `sources` fields | P1 |
| FR-03 | Sources array includes title, url, chunk_index, score for each source | P1 |
| FR-04 | POST /chat/stream returns text/event-stream response | P2 |
| FR-05 | GET /health returns system health status | P3 |
| FR-06 | GET /health checks Qdrant collection accessibility | P3 |
| FR-07 | GET /health checks Cohere API connectivity | P3 |

### RAG Pipeline

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-08 | Embed user question using Cohere with input_type="search_query" | P1 |
| FR-09 | Search Qdrant collection for top-5 relevant chunks | P1 |
| FR-10 | Build prompt with retrieved context and user question | P1 |
| FR-11 | Send prompt to OpenAI gpt-4o-mini for answer generation | P1 |
| FR-12 | Include system prompt instructing to answer only from context | P1 |
| FR-13 | Return "I don't have information about that" for out-of-scope questions | P1 |

### Configuration

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-14 | Load API keys from environment variables | P1 |
| FR-15 | OPENAI_API_KEY for OpenAI access | P1 |
| FR-16 | COHERE_API_KEY for embedding queries | P1 |
| FR-17 | QDRANT_URL and QDRANT_API_KEY for vector search | P1 |
| FR-18 | Configurable top_k parameter (default: 5) | P2 |
| FR-19 | Configurable relevance threshold (default: 0.5) | P2 |

### Error Handling

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-20 | Return 400 for missing or empty question | P1 |
| FR-21 | Return 503 when Qdrant is unavailable | P1 |
| FR-22 | Return 503 when Cohere API fails | P1 |
| FR-23 | Return 503 when OpenAI API fails | P1 |
| FR-24 | Include error message in response body | P1 |

## Non-Functional Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-01 | Response latency | < 5 seconds p95 |
| NFR-02 | Concurrent requests | Handle 10 simultaneous |
| NFR-03 | Memory usage | < 512MB |
| NFR-04 | Startup time | < 10 seconds |

## Technical Constraints

- **Runtime**: Python 3.11 with uv package manager
- **Framework**: FastAPI with uvicorn
- **LLM**: OpenAI gpt-4o-mini (cost-effective, fast)
- **Embeddings**: Cohere embed-english-v3.0 (same as ingestion)
- **Vector DB**: Qdrant Cloud (existing collection)
- **Project**: Extends existing backend/ folder

## API Contracts

### POST /chat

**Request:**
```json
{
  "question": "What is physical AI?"
}
```

**Response (200 OK):**
```json
{
  "answer": "Physical AI refers to artificial intelligence systems that interact with the physical world through sensors and actuators...",
  "sources": [
    {
      "title": "Introduction to Physical AI",
      "url": "https://example.com/docs/intro",
      "chunk_index": 0,
      "score": 0.89
    },
    {
      "title": "Embodied Intelligence",
      "url": "https://example.com/docs/embodied",
      "chunk_index": 2,
      "score": 0.76
    }
  ]
}
```

**Error Response (400):**
```json
{
  "detail": "Question cannot be empty"
}
```

**Error Response (503):**
```json
{
  "detail": "Vector database unavailable"
}
```

### POST /chat/stream

**Request:** Same as /chat

**Response (200 OK, text/event-stream):**
```
data: {"token": "Physical"}

data: {"token": " AI"}

data: {"token": " refers"}

...

data: {"done": true, "sources": [...]}
```

### GET /health

**Response (200 OK):**
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

## Out of Scope

- User authentication/authorization
- Rate limiting
- Request logging/analytics
- Conversation history/memory
- Multiple model support
- Caching layer
- Database for chat history

## Success Criteria

- [ ] `uv run uvicorn app.main:app --reload` starts server
- [ ] POST /chat returns relevant answers with sources
- [ ] POST /chat/stream streams tokens progressively
- [ ] GET /health returns dependency status
- [ ] Answers are grounded in retrieved book content
- [ ] Out-of-scope questions are handled gracefully

## Open Questions

1. Should we add request ID for tracing? (Defer to future spec)
2. Should streaming include intermediate sources? (Defer - sources at end)
3. Maximum question length? (Suggest 1000 characters)

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Cohere Embed API](https://docs.cohere.com/reference/embed)
- [Qdrant Python Client](https://qdrant.tech/documentation/quick-start/)
