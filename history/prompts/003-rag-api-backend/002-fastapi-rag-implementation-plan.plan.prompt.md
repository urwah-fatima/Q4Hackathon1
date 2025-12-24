---
id: 002
title: FastAPI RAG Implementation Plan
stage: plan
date: 2025-12-21
surface: agent
model: claude-opus-4-5-20251101
feature: 003-rag-api-backend
branch: 003-rag-api-backend
user: developer
command: /sp.plan
labels: ["fastapi", "rag", "openai", "cohere", "qdrant", "streaming"]
links:
  spec: specs/003-rag-api-backend/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-rag-api-backend/plan.md
  - specs/003-rag-api-backend/research.md
  - specs/003-rag-api-backend/data-model.md
  - specs/003-rag-api-backend/quickstart.md
tests:
  - Constitution check passed (6/6 principles)
---

## Prompt

/sp.plan

FastAPI RAG backend with OpenAI generation in existing uv project
- Continue in existing uv-managed backend folder; add dependencies: uv add fastapi uvicorn openai python-dotenv typer
- Create app/ folder: main.py (FastAPI app), retriever.py (Qdrant + Cohere query embedding), agent.py (prompt building + OpenAI chat completion)
- API endpoint: POST /chat with JSON {question: str} → returns {answer: str, sources: list of {url, title, snippet}}
- RAG flow: embed question → search Qdrant (top_k=5) → build system/user prompt with context → call OpenAI gpt-4o-mini → extract and return answer + sources
- Add streaming endpoint /chat/stream (optional bonus); run with uv run uvicorn app.main:app --reload
- Success: Local API answers book-specific questions accurately; refuses out-of-scope queries; sources link back to correct pages

## Response snapshot

Created implementation plan for FastAPI RAG backend with:

**Architecture**:
- Modular app/ folder: main.py, retriever.py, agent.py, models.py, config.py
- RAG flow: embed → search → context → generate → respond
- Endpoints: POST /chat, POST /chat/stream, GET /health

**Key Decisions**:
- LLM: gpt-4o-mini (cost-effective, fast)
- Streaming: SSE via FastAPI StreamingResponse
- Grounding: System prompt instructs LLM to only use context

**Research Topics**:
- FastAPI project structure best practices
- OpenAI chat completion for RAG
- SSE streaming implementation
- Cohere query vs document embedding

**Data Models**:
- ChatRequest (question)
- ChatResponse (answer, sources)
- Source (title, url, chunk_index, score, snippet)
- StreamEvent (token, done, sources)
- HealthResponse (status, version, dependencies)

Constitution check: 6/6 principles passed.

## Outcome

- ✅ Impact: Complete plan for RAG API backend with modular architecture
- 🧪 Tests: Constitution check (6/6)
- 📁 Files: plan.md, research.md, data-model.md, quickstart.md
- 🔁 Next prompts: /sp.tasks to generate implementation tasks
- 🧠 Reflection: Clean modular structure with app/ folder enables testing and maintenance. Grounding strategy via system prompt should keep answers accurate.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Constitution PASS (6/6)
- Prompt variant (if applicable): User-specified app/ folder structure with modular files
- Next experiment (smallest change to try): N/A - plan complete
