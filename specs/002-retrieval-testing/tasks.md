# Tasks: Retrieval Testing Pipeline

**Input**: Design documents from `/specs/002-retrieval-testing/`
**Prerequisites**: plan.md, spec.md, data-model.md, research.md, quickstart.md

**Tests**: Manual verification (no automated tests specified)

**Organization**: Tasks organized by user story for independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- All file paths relative to `backend/` folder

---

## Phase 1: Setup (Add Dependency)

**Purpose**: Add typer dependency to existing backend project

- [ ] T001 Add typer dependency: run `uv add typer` in backend/
- [ ] T002 Verify .env has COHERE_API_KEY, QDRANT_URL, QDRANT_API_KEY in backend/.env

**Checkpoint**: Typer installed, environment ready

---

## Phase 2: Foundational (Script Skeleton)

**Purpose**: Create test_retrieval.py with imports and client initialization

**CRITICAL**: Must complete before any user story implementation

- [ ] T003 Create test_retrieval.py with imports (typer, cohere, qdrant_client, dotenv) in backend/test_retrieval.py
- [ ] T004 Add load_dotenv() and initialize Cohere client in backend/test_retrieval.py
- [ ] T005 Add Qdrant client initialization with environment variables in backend/test_retrieval.py
- [ ] T006 Create Typer app instance with help text in backend/test_retrieval.py
- [ ] T007 Add configuration constants (COLLECTION_NAME, DEFAULT_TOP_K, THRESHOLD) in backend/test_retrieval.py

**Checkpoint**: Script runs with `uv run test_retrieval.py --help`

---

## Phase 3: User Story 1 - Run Retrieval Test Suite (Priority: P1) MVP

**Goal**: Developer can run predefined test queries and see results with scores

**Independent Test**: `uv run test_retrieval.py test` executes all queries with formatted results

### Implementation for User Story 1

- [ ] T008 [US1] Implement embed_query(text) using Cohere with input_type="search_query" in backend/test_retrieval.py
- [ ] T009 [US1] Implement search_qdrant(query_vector, top_k) returning results with payloads in backend/test_retrieval.py
- [ ] T010 [US1] Implement format_result(result, rank) for pretty terminal output in backend/test_retrieval.py
- [ ] T011 [US1] Add TEST_QUERIES list with 5+ predefined queries covering book topics in backend/test_retrieval.py
- [ ] T012 [US1] Implement run_single_query(query_text, top_k) combining embed + search + format in backend/test_retrieval.py
- [ ] T013 [US1] Add @app.command() for `test` command running all predefined queries in backend/test_retrieval.py
- [ ] T014 [US1] Add @app.command() for `query` command with text argument and --top-k option in backend/test_retrieval.py

**Checkpoint**: `uv run test_retrieval.py test` runs 5+ queries with formatted output

---

## Phase 4: User Story 2 - Interactive Query Testing (Priority: P2)

**Goal**: Developer can enter custom queries in a REPL loop

**Independent Test**: `uv run test_retrieval.py interactive` allows multiple queries

### Implementation for User Story 2

- [ ] T015 [US2] Add @app.command() for `interactive` command in backend/test_retrieval.py
- [ ] T016 [US2] Implement input loop with prompt "Enter query (or 'quit' to exit): " in backend/test_retrieval.py
- [ ] T017 [US2] Call run_single_query() for each user input in interactive mode in backend/test_retrieval.py

**Checkpoint**: `uv run test_retrieval.py interactive` works as REPL

---

## Phase 5: User Story 3 - Handle Edge Cases Gracefully (Priority: P3)

**Goal**: Script handles errors without crashing, provides helpful messages

**Independent Test**: Trigger edge cases (no results, connection error) and observe graceful handling

### Implementation for User Story 3

- [ ] T018 [US3] Add try/except for Qdrant connection errors with helpful message in backend/test_retrieval.py
- [ ] T019 [US3] Add try/except for Cohere API errors with helpful message in backend/test_retrieval.py
- [ ] T020 [US3] Add check for empty results with "No results found" message in backend/test_retrieval.py
- [ ] T021 [US3] Add low relevance warning when score < threshold in format_result() in backend/test_retrieval.py
- [ ] T022 [US3] Add collection existence check before querying in backend/test_retrieval.py

**Checkpoint**: Edge cases handled gracefully with informative messages

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements and documentation

- [ ] T023 Add docstrings to all functions in backend/test_retrieval.py
- [ ] T024 Add --threshold option to query and test commands in backend/test_retrieval.py
- [ ] T025 Validate script against quickstart.md instructions

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - start immediately
- **Foundational (Phase 2)**: Depends on Setup completion
- **User Story 1 (Phase 3)**: Depends on Foundational - core functionality
- **User Story 2 (Phase 4)**: Depends on US1 (reuses run_single_query)
- **User Story 3 (Phase 5)**: Can run after US1 (extends existing functions)
- **Polish (Phase 6)**: Depends on all user stories

### User Story Dependencies

- **User Story 1 (P1)**: Independent - core search functionality
- **User Story 2 (P2)**: Depends on US1's run_single_query()
- **User Story 3 (P3)**: Extends US1's functions with error handling

### Within Each Phase

- Tasks execute sequentially within test_retrieval.py (single file)
- No [P] markers since all tasks modify same file

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T002)
2. Complete Phase 2: Foundational (T003-T007)
3. Complete Phase 3: User Story 1 (T008-T014)
4. **STOP and VALIDATE**: Run `uv run test_retrieval.py test`
5. MVP is complete when queries return relevant results!

### Incremental Delivery

1. Setup + Foundational → Script skeleton ready
2. User Story 1 → Test suite and single query working (MVP!)
3. User Story 2 → Interactive mode added
4. User Story 3 → Robust error handling
5. Polish → Production-ready

---

## Summary

| Phase | Tasks | Description |
|-------|-------|-------------|
| 1. Setup | T001-T002 | Add typer dependency |
| 2. Foundational | T003-T007 | Script skeleton |
| 3. US1 (P1) | T008-T014 | Test suite & query (MVP) |
| 4. US2 (P2) | T015-T017 | Interactive mode |
| 5. US3 (P3) | T018-T022 | Error handling |
| 6. Polish | T023-T025 | Documentation |

**Total Tasks**: 25
**MVP Scope**: T001-T014 (14 tasks)
**Parallel Opportunities**: Limited (single file architecture)

---

## Notes

- All implementation in single `backend/test_retrieval.py` file
- Reuses existing .env and uv configuration from Spec-1
- Run with `uv run test_retrieval.py [command]`
- Collection: `book_chatbot_embedding` (same as ingestion)
- Commit after each phase completion
