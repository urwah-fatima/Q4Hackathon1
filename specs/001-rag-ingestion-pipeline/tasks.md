# Tasks: RAG Ingestion Pipeline

**Input**: Design documents from `/specs/001-rag-ingestion-pipeline/`
**Prerequisites**: plan.md, spec.md, data-model.md, research.md, quickstart.md

**Tests**: Manual verification via Qdrant dashboard (no automated tests specified)

**Organization**: Tasks organized by user story for independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- All file paths relative to `backend/` folder

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Create uv-managed Python project with all dependencies

- [ ] T001 Create backend folder at repository root
- [ ] T002 Initialize uv project: `uv init rag-ingestion --python 3.11` in backend/
- [ ] T003 Create virtual environment: `uv venv` in backend/
- [ ] T004 Add dependencies: `uv add cohere qdrant-client langchain langchain-community langchain-text-splitters beautifulsoup4 requests python-dotenv tqdm`
- [ ] T005 Create .env.example with required environment variables in backend/.env.example
- [ ] T006 Create .gitignore with .env and .venv exclusions in backend/.gitignore

**Checkpoint**: Project structure ready, dependencies installed

---

## Phase 2: Foundational (Core Setup in main.py)

**Purpose**: Create main.py skeleton with imports and configuration loading

**CRITICAL**: Must complete before any user story implementation

- [ ] T007 Create main.py with imports and load_dotenv() in backend/main.py
- [ ] T008 Add configuration constants (COLLECTION_NAME, CHUNK_SIZE, CHUNK_OVERLAP) in backend/main.py
- [ ] T009 Initialize Cohere client with API key from environment in backend/main.py
- [ ] T010 Initialize Qdrant client with URL and API key from environment in backend/main.py

**Checkpoint**: Foundation ready - main.py has all imports and client initialization

---

## Phase 3: User Story 1 - Initial Content Ingestion (Priority: P1) MVP

**Goal**: Ingest all book content from deployed Docusaurus website into Qdrant

**Independent Test**: Run `uv run main.py`, verify chunks appear in Qdrant dashboard with correct metadata

### Implementation for User Story 1

- [ ] T011 [US1] Implement get_all_urls() function returning list of book URLs in backend/main.py
- [ ] T012 [US1] Implement extract_text_from_url(url) using requests and BeautifulSoup in backend/main.py
- [ ] T013 [US1] Implement chunk_text(text, url, title) using RecursiveCharacterTextSplitter in backend/main.py
- [ ] T014 [US1] Implement embed(texts) using Cohere embed-english-v3.0 with batching in backend/main.py
- [ ] T015 [US1] Implement create_collection() for book_chatbot_embedding (1024-dim, cosine) in backend/main.py
- [ ] T016 [US1] Implement save_chunk_to_qdrant(chunks, embeddings) with upsert in backend/main.py
- [ ] T017 [US1] Implement main() orchestrating full pipeline with tqdm progress in backend/main.py
- [ ] T018 [US1] Add error handling for HTTP failures (skip and continue) in backend/main.py
- [ ] T019 [US1] Add error handling for Cohere API rate limits (retry logic) in backend/main.py

**Checkpoint**: `uv run main.py` successfully ingests all book pages into Qdrant

---

## Phase 4: User Story 2 - Pipeline Verification (Priority: P2)

**Goal**: Verify ingestion success and test similarity search

**Independent Test**: Run verification function, confirm chunk count and search results

### Implementation for User Story 2

- [ ] T020 [US2] Implement verify_collection() to count vectors in Qdrant in backend/main.py
- [ ] T021 [US2] Implement test_search(query) to perform similarity search in backend/main.py
- [ ] T022 [US2] Add --verify CLI flag to run verification instead of ingestion in backend/main.py
- [ ] T023 [US2] Print verification report: vector count, sample search results in backend/main.py

**Checkpoint**: `uv run main.py --verify` shows collection stats and search results

---

## Phase 5: User Story 3 - Content Update Re-ingestion (Priority: P3)

**Goal**: Support safe re-runs without duplicate entries

**Independent Test**: Run ingestion twice, verify no duplicate chunks in Qdrant

### Implementation for User Story 3

- [ ] T024 [US3] Generate deterministic point IDs from URL hash + chunk index in backend/main.py
- [ ] T025 [US3] Use upsert (not insert) for idempotent storage in backend/main.py
- [ ] T026 [US3] Add summary output showing chunks processed vs already existing in backend/main.py

**Checkpoint**: Re-running `uv run main.py` completes without creating duplicates

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements and documentation

- [ ] T027 Add docstrings to all functions in backend/main.py
- [ ] T028 Add logging statements for pipeline progress in backend/main.py
- [ ] T029 [P] Update .env.example with all required variables in backend/.env.example
- [ ] T030 Validate against quickstart.md instructions

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - start immediately
- **Foundational (Phase 2)**: Depends on Setup completion
- **User Story 1 (Phase 3)**: Depends on Foundational - BLOCKS US2 and US3
- **User Story 2 (Phase 4)**: Depends on US1 (needs data in Qdrant to verify)
- **User Story 3 (Phase 5)**: Depends on US1 (extends save logic)
- **Polish (Phase 6)**: Depends on all user stories

### User Story Dependencies

- **User Story 1 (P1)**: Independent - core ingestion
- **User Story 2 (P2)**: Requires US1 data to verify
- **User Story 3 (P3)**: Extends US1's save_chunk_to_qdrant()

### Within Each Phase

- Tasks execute sequentially within main.py (single file)
- No [P] markers since all tasks modify same file

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T006)
2. Complete Phase 2: Foundational (T007-T010)
3. Complete Phase 3: User Story 1 (T011-T019)
4. **STOP and VALIDATE**: Run `uv run main.py` and check Qdrant dashboard
5. MVP is complete when chunks appear in Qdrant!

### Incremental Delivery

1. Setup + Foundational → Project ready
2. User Story 1 → Core ingestion working (MVP!)
3. User Story 2 → Verification capability
4. User Story 3 → Safe re-runs
5. Polish → Production-ready

---

## Summary

| Phase | Tasks | Description |
|-------|-------|-------------|
| 1. Setup | T001-T006 | Project initialization |
| 2. Foundational | T007-T010 | main.py skeleton |
| 3. US1 (P1) | T011-T019 | Core ingestion (MVP) |
| 4. US2 (P2) | T020-T023 | Verification |
| 5. US3 (P3) | T024-T026 | Idempotent re-runs |
| 6. Polish | T027-T030 | Documentation |

**Total Tasks**: 30
**MVP Scope**: T001-T019 (19 tasks)
**Parallel Opportunities**: Limited (single file architecture)

---

## Notes

- All implementation in single `backend/main.py` file
- Run with `uv run main.py` after setup
- Verify with Qdrant Cloud dashboard
- Collection name: `book_chatbot_embedding`
- Commit after each phase completion
