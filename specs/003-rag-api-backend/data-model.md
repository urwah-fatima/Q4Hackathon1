# Data Model: RAG API Backend

**Feature**: 003-rag-api-backend
**Date**: 2025-12-21

## Entities

### ChatRequest

**Purpose**: Incoming request to the /chat endpoint

| Field | Type | Required | Validation | Description |
|-------|------|----------|------------|-------------|
| question | string | Yes | min_length=1, max_length=1000 | User's question |

**Pydantic Model**:
```python
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000)
```

### Source

**Purpose**: A retrieved document chunk used as context for the answer

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | Yes | Page title from Qdrant payload |
| url | string | Yes | Source page URL |
| chunk_index | integer | Yes | Position of chunk within page |
| score | float | Yes | Similarity score (0.0-1.0) |
| snippet | string | No | Text preview (first 200 chars) |

**Pydantic Model**:
```python
class Source(BaseModel):
    title: str
    url: str
    chunk_index: int
    score: float
    snippet: str | None = None
```

### ChatResponse

**Purpose**: Response from the /chat endpoint

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| answer | string | Yes | Generated answer from LLM |
| sources | list[Source] | Yes | Retrieved chunks used for answer |

**Pydantic Model**:
```python
class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]
```

### StreamEvent

**Purpose**: Single event in the SSE stream

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| token | string | No | Single token from LLM stream |
| done | boolean | No | True when stream is complete |
| sources | list[Source] | No | Sources (only in final event) |

**Pydantic Model**:
```python
class StreamEvent(BaseModel):
    token: str | None = None
    done: bool | None = None
    sources: list[Source] | None = None
```

### HealthResponse

**Purpose**: Response from the /health endpoint

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| status | string | Yes | "ok" or "error" |
| version | string | Yes | API version |
| dependencies | dict | Yes | Status of each dependency |

**Pydantic Model**:
```python
class DependencyStatus(BaseModel):
    qdrant: str  # "ok" or "error"
    cohere: str
    openai: str

class HealthResponse(BaseModel):
    status: str
    version: str
    dependencies: DependencyStatus
```

## Internal Entities

### RetrievalResult

**Purpose**: Internal representation of Qdrant search result

| Field | Type | Description |
|-------|------|-------------|
| id | string | Qdrant point ID |
| score | float | Similarity score |
| payload | dict | Contains title, url, chunk_index, text |

**Usage**:
```python
@dataclass
class RetrievalResult:
    id: str
    score: float
    payload: dict

    @property
    def text(self) -> str:
        return self.payload.get("text", "")

    @property
    def title(self) -> str:
        return self.payload.get("title", "")

    @property
    def url(self) -> str:
        return self.payload.get("url", "")

    @property
    def chunk_index(self) -> int:
        return self.payload.get("chunk_index", 0)
```

### RAGContext

**Purpose**: Assembled context for LLM prompt

| Field | Type | Description |
|-------|------|-------------|
| question | string | Original user question |
| chunks | list[RetrievalResult] | Retrieved chunks |
| context_text | string | Formatted context for prompt |

## Entity Relationships

```
ChatRequest
    │
    ▼
┌──────────────────────┐
│    RAG Pipeline      │
│                      │
│  1. Embed question   │
│  2. Search Qdrant    │
│  3. Build context    │
│  4. Generate answer  │
└──────────────────────┘
    │
    ▼
ChatResponse
    ├── answer: str
    └── sources: [Source, Source, ...]

For streaming:
    │
    ▼
StreamEvent (repeated)
    ├── {token: "..."}
    ├── {token: "..."}
    └── {done: true, sources: [...]}
```

## Qdrant Payload Schema (from Spec-1)

The RAG backend reads from the existing Qdrant collection `book_chatbot_embedding`:

```python
{
    "url": "https://physical-ai-book.com/docs/intro",
    "title": "Introduction to Physical AI",
    "text": "Physical AI refers to...",
    "chunk_index": 0
}
```

**Vector**: 1024-dimensional float array (Cohere embed-english-v3.0)

## Configuration Entity

### Settings

**Purpose**: Application configuration from environment

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| OPENAI_API_KEY | string | .env | OpenAI API key |
| COHERE_API_KEY | string | .env | Cohere API key |
| QDRANT_URL | string | .env | Qdrant Cloud URL |
| QDRANT_API_KEY | string | .env | Qdrant API key |
| COLLECTION_NAME | string | constant | "book_chatbot_embedding" |
| TOP_K | int | constant | 5 (default) |
| RELEVANCE_THRESHOLD | float | constant | 0.5 (default) |

**Implementation**:
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str
    cohere_api_key: str
    qdrant_url: str
    qdrant_api_key: str
    collection_name: str = "book_chatbot_embedding"
    top_k: int = 5
    relevance_threshold: float = 0.5

    class Config:
        env_file = ".env"
```
