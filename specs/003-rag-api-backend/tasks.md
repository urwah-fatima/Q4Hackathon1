# Tasks: RAG API Backend

**Input**: Design documents from `/specs/003-rag-api-backend/`
**Prerequisites**: plan.md, spec.md, data-model.md, research.md, quickstart.md

**Tests**: Manual verification (no automated tests specified)

**Organization**: Tasks organized by user story for independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- All file paths relative to `backend/` folder

---

## Phase 1: Setup (Add Dependencies)

**Purpose**: Add FastAPI dependencies to existing backend project

- [ ] T001 Add fastapi dependency: run `uv add fastapi` in backend/
- [ ] T002 Add uvicorn dependency: run `uv add uvicorn` in backend/
- [ ] T003 Add openai dependency: run `uv add openai` in backend/
- [ ] T004 Verify .env has OPENAI_API_KEY, COHERE_API_KEY, QDRANT_URL, QDRANT_API_KEY in backend/.env

**Checkpoint**: All dependencies installed, environment ready

---

## Phase 2: Foundational (App Structure)

**Purpose**: Create app/ folder with config and models

**CRITICAL**: Must complete before any user story implementation

- [ ] T005 Create app/ folder structure with __init__.py in backend/app/__init__.py
- [ ] T006 [P] Create config.py with Settings class loading environment variables in backend/app/config.py
- [ ] T007 [P] Create models.py with ChatRequest, Source, ChatResponse Pydantic models in backend/app/models.py
- [ ] T008 [P] Add StreamEvent and HealthResponse models to backend/app/models.py
- [ ] T009 Create main.py with FastAPI app instance and basic imports in backend/app/main.py

**Checkpoint**: `uv run uvicorn app.main:app --reload` starts (empty app)

---

## Phase 3: User Story 1 - Answer Book Questions via API (Priority: P1) MVP

**Goal**: POST /chat endpoint accepts question, returns answer with sources from book content

**Independent Test**: `curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"question": "What is physical AI?"}'` returns answer with sources

### Implementation for User Story 1

- [ ] T010 [US1] Create retriever.py with Cohere client initialization in backend/app/retriever.py
- [ ] T011 [US1] Implement embed_query(text) using Cohere with input_type="search_query" in backend/app/retriever.py
- [ ] T012 [US1] Add Qdrant client initialization to retriever.py in backend/app/retriever.py
- [ ] T013 [US1] Implement search_qdrant(query_vector, top_k) returning results with payloads in backend/app/retriever.py
- [ ] T014 [US1] Implement retrieve(question, top_k) combining embed + search in backend/app/retriever.py
- [ ] T015 [US1] Create agent.py with SYSTEM_PROMPT constant for grounding in backend/app/agent.py
- [ ] T016 [US1] Add OpenAI client initialization to agent.py in backend/app/agent.py
- [ ] T017 [US1] Implement build_context(chunks) formatting retrieved chunks for prompt in backend/app/agent.py
- [ ] T018 [US1] Implement generate_answer(context, question) using gpt-4o-mini in backend/app/agent.py
- [ ] T019 [US1] Add POST /chat endpoint to main.py calling retriever and agent in backend/app/main.py
- [ ] T020 [US1] Implement format_sources(chunks) converting retrieval results to Source models in backend/app/main.py
- [ ] T021 [US1] Add try/except for Qdrant errors with HTTPException 503 in backend/app/main.py
- [ ] T022 [US1] Add try/except for Cohere API errors with HTTPException 503 in backend/app/main.py
- [ ] T023 [US1] Add try/except for OpenAI API errors with HTTPException 503 in backend/app/main.py
- [ ] T024 [US1] Add validation for empty question with HTTPException 400 in backend/app/main.py

**Checkpoint**: `POST /chat` returns relevant answers with sources from book content

---

## Phase 4: User Story 2 - Stream Responses for Better UX (Priority: P2)

**Goal**: POST /chat/stream streams answer tokens progressively via SSE

**Independent Test**: `curl -X POST http://localhost:8000/chat/stream -H "Content-Type: application/json" -d '{"question": "How do robots balance?"}'` streams tokens

### Implementation for User Story 2

- [ ] T025 [US2] Implement stream_answer(context, question) using OpenAI streaming in backend/app/agent.py
- [ ] T026 [US2] Create async generator for SSE events yielding tokens in backend/app/agent.py
- [ ] T027 [US2] Add POST /chat/stream endpoint with StreamingResponse in backend/app/main.py
- [ ] T028 [US2] Implement stream generator combining retrieval + streaming generation in backend/app/main.py
- [ ] T029 [US2] Add final SSE event with sources array when stream completes in backend/app/main.py
- [ ] T030 [US2] Add error handling for streaming endpoint in backend/app/main.py

**Checkpoint**: `/chat/stream` streams tokens progressively and ends with sources

---

## Phase 5: User Story 3 - Health and Status Monitoring (Priority: P3)

**Goal**: GET /health returns dependency status for monitoring

**Independent Test**: `curl http://localhost:8000/health` returns status with dependency checks

### Implementation for User Story 3

- [ ] T031 [US3] Implement check_qdrant_health() testing collection access in backend/app/retriever.py
- [ ] T032 [US3] Implement check_cohere_health() testing embed API in backend/app/retriever.py
- [ ] T033 [US3] Implement check_openai_health() testing chat API in backend/app/agent.py
- [ ] T034 [US3] Add GET /health endpoint calling all health checks in backend/app/main.py
- [ ] T035 [US3] Return HealthResponse with status and dependency details in backend/app/main.py
- [ ] T036 [US3] Add API_VERSION constant to config.py in backend/app/config.py

**Checkpoint**: `/health` returns dependency status for Qdrant, Cohere, and OpenAI

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements and documentation

- [ ] T037 Add docstrings to all functions in backend/app/retriever.py
- [ ] T038 Add docstrings to all functions in backend/app/agent.py
- [ ] T039 Add docstrings to all functions in backend/app/main.py
- [ ] T040 Add --top-k query parameter to /chat endpoint in backend/app/main.py
- [ ] T041 Add low relevance warning when score < threshold in response in backend/app/main.py
- [ ] T042 Validate server against quickstart.md instructions

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - start immediately
- **Foundational (Phase 2)**: Depends on Setup completion
- **User Story 1 (Phase 3)**: Depends on Foundational - core RAG functionality
- **User Story 2 (Phase 4)**: Depends on US1 (reuses retriever + agent modules)
- **User Story 3 (Phase 5)**: Can run after Foundational (independent health checks)
- **Polish (Phase 6)**: Depends on all user stories

### User Story Dependencies

- **User Story 1 (P1)**: Independent - core chat functionality (MVP)
- **User Story 2 (P2)**: Depends on US1's retriever.py and agent.py modules
- **User Story 3 (P3)**: Independent - only uses client initialization, no US1/US2 logic

### Within Each Phase

- Tasks within same file execute sequentially
- Tasks marked [P] in different files can run in parallel

---

## Parallel Opportunities

### Phase 2 (Foundational)
```
# These can run in parallel (different files):
T006: config.py
T007: models.py (first batch)
T008: models.py (second batch - after T007)
```

### Phase 3 (User Story 1)
```
# retriever.py and agent.py can be developed in parallel:
Team A: T010-T014 (retriever.py)
Team B: T015-T018 (agent.py)
Then: T019-T024 (main.py integration)
```

### Phase 5 (User Story 3)
```
# Health checks can be developed in parallel:
T031-T032: retriever.py health checks
T033: agent.py health check
Then: T034-T036 (main.py integration)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T004)
2. Complete Phase 2: Foundational (T005-T009)
3. Complete Phase 3: User Story 1 (T010-T024)
4. **STOP and VALIDATE**: Run `curl -X POST http://localhost:8000/chat ...`
5. MVP is complete when questions return relevant answers!

### Incremental Delivery

1. Setup + Foundational → App skeleton ready
2. User Story 1 → Chat endpoint working (MVP!)
3. User Story 2 → Streaming added
4. User Story 3 → Health monitoring
5. Polish → Production-ready

---

## Summary

| Phase | Tasks | Description |
|-------|-------|-------------|
| 1. Setup | T001-T004 | Add dependencies |
| 2. Foundational | T005-T009 | App structure |
| 3. US1 (P1) | T010-T024 | POST /chat (MVP) |
| 4. US2 (P2) | T025-T030 | POST /chat/stream |
| 5. US3 (P3) | T031-T036 | GET /health |
| 6. Polish | T037-T042 | Documentation |

**Total Tasks**: 42
**MVP Scope**: T001-T024 (24 tasks)
**Parallel Opportunities**: Within phases 2, 3, and 5

---

## Notes

- All implementation in `backend/app/` folder
- Reuses existing .env and uv configuration from Spec-1
- Run with `uv run uvicorn app.main:app --reload`
- Collection: `book_chatbot_embedding` (same as ingestion)
- Commit after each phase completion
