# Tasks: Docusaurus RAG Chatbot Widget

**Input**: Design documents from `/specs/004-docusaurus-chatbot/`
**Prerequisites**: plan.md, spec.md, data-model.md, research.md, quickstart.md

**Tests**: Manual browser testing (no automated tests specified)

**Organization**: Tasks organized by user story for independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- All file paths relative to repository root

---

## Phase 1: Setup (Backend CORS + Directory Structure)

**Purpose**: Enable frontend-backend communication and create component folder structure

- [ ] T001 Add CORS middleware to FastAPI backend in backend/app/main.py
- [ ] T002 Create src/components/ChatWidget/ folder structure
- [ ] T003 Create src/theme/ folder for Root component override

**Checkpoint**: Backend accepts requests from localhost:3000

---

## Phase 2: Foundational (Configuration + Base Component)

**Purpose**: Create config, Root injection, and basic ChatWidget skeleton

**CRITICAL**: Must complete before any user story implementation

- [ ] T004 Create config.js with API_URL and widget settings in src/components/ChatWidget/config.js
- [ ] T005 [P] Create ChatWidget.css with base styles and CSS variables in src/components/ChatWidget/ChatWidget.css
- [ ] T006 [P] Create index.js exporting ChatWidget in src/components/ChatWidget/index.js
- [ ] T007 Create ChatWidget.js with state initialization and empty render in src/components/ChatWidget/ChatWidget.js
- [ ] T008 Create Root.js theme override injecting ChatWidget in src/theme/Root.js

**Checkpoint**: `npm run start` shows empty chat widget container on all pages

---

## Phase 3: User Story 1 - Ask Questions About Book Content (Priority: P1) MVP

**Goal**: Floating chat button + chat panel + Q&A with sources

**Independent Test**: Click chat button → type question → receive answer with clickable source links

### Implementation for User Story 1

- [ ] T009 [US1] Implement renderChatButton() creating floating button element in src/components/ChatWidget/ChatWidget.js
- [ ] T010 [US1] Add CSS for chat button (fixed position, bottom-right, z-index) in src/components/ChatWidget/ChatWidget.css
- [ ] T011 [US1] Implement togglePanel() to show/hide chat panel in src/components/ChatWidget/ChatWidget.js
- [ ] T012 [US1] Implement renderChatPanel() with header, message list, input area in src/components/ChatWidget/ChatWidget.js
- [ ] T013 [US1] Add CSS for chat panel layout and animations in src/components/ChatWidget/ChatWidget.css
- [ ] T014 [US1] Implement renderMessage(message) for user and assistant messages in src/components/ChatWidget/ChatWidget.js
- [ ] T015 [US1] Implement renderSources(sources) with clickable links in src/components/ChatWidget/ChatWidget.js
- [ ] T016 [US1] Add CSS for message bubbles (user right-aligned, assistant left-aligned) in src/components/ChatWidget/ChatWidget.css
- [ ] T017 [US1] Implement handleInputChange() updating inputValue state in src/components/ChatWidget/ChatWidget.js
- [ ] T018 [US1] Implement handleSubmit() sending question to backend in src/components/ChatWidget/ChatWidget.js
- [ ] T019 [US1] Implement sendMessage(question) using fetch to POST /chat in src/components/ChatWidget/ChatWidget.js
- [ ] T020 [US1] Implement addMessage(role, content, sources) updating messages array in src/components/ChatWidget/ChatWidget.js
- [ ] T021 [US1] Implement renderLoadingIndicator() showing during API call in src/components/ChatWidget/ChatWidget.js
- [ ] T022 [US1] Add CSS for loading indicator animation in src/components/ChatWidget/ChatWidget.css
- [ ] T023 [US1] Implement handleError(error) displaying user-friendly message in src/components/ChatWidget/ChatWidget.js
- [ ] T024 [US1] Add try/catch for fetch errors with timeout handling in src/components/ChatWidget/ChatWidget.js
- [ ] T025 [US1] Implement handleClosePanel() triggered by close button and outside click in src/components/ChatWidget/ChatWidget.js
- [ ] T026 [US1] Add sessionStorage persistence for messages array in src/components/ChatWidget/ChatWidget.js
- [ ] T027 [US1] Add Docusaurus theme integration (light/dark mode CSS) in src/components/ChatWidget/ChatWidget.css

**Checkpoint**: Full Q&A workflow works - type question, get answer with sources, click source to navigate

---

## Phase 4: User Story 2 - Ask About Selected Text (Priority: P2)

**Goal**: Text selection detection + "Ask about this" tooltip + context in question

**Independent Test**: Select text → tooltip appears → click → chat opens with context pre-filled

### Implementation for User Story 2

- [ ] T028 [US2] Implement handleTextSelection() detecting selected text in src/components/ChatWidget/ChatWidget.js
- [ ] T029 [US2] Add mouseup and touchend event listeners for selection detection in src/components/ChatWidget/ChatWidget.js
- [ ] T030 [US2] Implement renderSelectionTooltip(position) showing "Ask about this" button in src/components/ChatWidget/ChatWidget.js
- [ ] T031 [US2] Add CSS for selection tooltip positioning and styling in src/components/ChatWidget/ChatWidget.css
- [ ] T032 [US2] Implement handleAskAboutSelection() opening chat with context in src/components/ChatWidget/ChatWidget.js
- [ ] T033 [US2] Implement renderContextBadge(text) showing selected text preview in input area in src/components/ChatWidget/ChatWidget.js
- [ ] T034 [US2] Add CSS for context badge styling (truncated text, dismiss button) in src/components/ChatWidget/ChatWidget.css
- [ ] T035 [US2] Modify sendMessage() to include context prefix when selection exists in src/components/ChatWidget/ChatWidget.js
- [ ] T036 [US2] Implement handleContextMenu(event) for right-click menu option in src/components/ChatWidget/ChatWidget.js
- [ ] T037 [US2] Implement renderCustomContextMenu(position) with "Ask about this" option in src/components/ChatWidget/ChatWidget.js
- [ ] T038 [US2] Add CSS for custom context menu styling in src/components/ChatWidget/ChatWidget.css
- [ ] T039 [US2] Implement clearSelection() to dismiss tooltip and context in src/components/ChatWidget/ChatWidget.js

**Checkpoint**: Select text → "Ask about this" appears → click → chat opens with context → question includes context

---

## Phase 5: User Story 3 - Responsive Mobile Experience (Priority: P3)

**Goal**: Full-screen chat on mobile with touch support

**Independent Test**: Open on mobile viewport → chat opens full-screen → touch interactions work

### Implementation for User Story 3

- [ ] T040 [US3] Add CSS media queries for mobile layout (full-screen panel) in src/components/ChatWidget/ChatWidget.css
- [ ] T041 [US3] Adjust chat button position for mobile (smaller margins) in src/components/ChatWidget/ChatWidget.css
- [ ] T042 [US3] Add viewport meta handling for keyboard visibility in src/components/ChatWidget/ChatWidget.js
- [ ] T043 [US3] Implement touch-friendly button sizes and spacing in src/components/ChatWidget/ChatWidget.css
- [ ] T044 [US3] Add swipe-to-close gesture handling for mobile in src/components/ChatWidget/ChatWidget.js
- [ ] T045 [US3] Ensure input field scrolls into view when keyboard opens in src/components/ChatWidget/ChatWidget.js

**Checkpoint**: Mobile-responsive chat works on 320px viewport with touch interactions

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements, edge cases, and validation

- [ ] T046 Add empty question validation (disable submit button) in src/components/ChatWidget/ChatWidget.js
- [ ] T047 Add long text truncation (>1000 chars) for selected text in src/components/ChatWidget/ChatWidget.js
- [ ] T048 Add request queuing for rapid submissions in src/components/ChatWidget/ChatWidget.js
- [ ] T049 Add accessibility attributes (aria-labels, focus management) in src/components/ChatWidget/ChatWidget.js
- [ ] T050 Add keyboard shortcuts (Escape to close, Enter to submit) in src/components/ChatWidget/ChatWidget.js
- [ ] T051 Validate against quickstart.md testing checklist
- [ ] T052 Test cross-browser compatibility (Chrome, Firefox, Safari, Edge)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - start immediately
- **Foundational (Phase 2)**: Depends on Setup completion
- **User Story 1 (Phase 3)**: Depends on Foundational - core chat functionality (MVP)
- **User Story 2 (Phase 4)**: Depends on US1 (reuses chat panel and sendMessage)
- **User Story 3 (Phase 5)**: Depends on US1 (adds mobile CSS to existing components)
- **Polish (Phase 6)**: Depends on all user stories

### User Story Dependencies

- **User Story 1 (P1)**: Independent - core chat widget (MVP)
- **User Story 2 (P2)**: Depends on US1's chat panel and sendMessage function
- **User Story 3 (P3)**: Depends on US1's layout (extends with mobile CSS)

### Within Each Phase

- CSS tasks ([P]) can run in parallel with JS tasks for different features
- JS tasks within same function must be sequential

---

## Parallel Opportunities

### Phase 2 (Foundational)
```
# These can run in parallel (different files):
T005: ChatWidget.css (base styles)
T006: index.js (exports)
```

### Phase 3 (User Story 1)
```
# CSS and JS can be parallelized:
Team A (CSS): T010, T013, T016, T022, T027
Team B (JS): T009, T011, T012, T014, T017, T018...
```

### Phase 4 (User Story 2)
```
# CSS and JS can be parallelized:
Team A (CSS): T031, T034, T038
Team B (JS): T028, T029, T030, T032...
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Foundational (T004-T008)
3. Complete Phase 3: User Story 1 (T009-T027)
4. **STOP and VALIDATE**: Open Docusaurus, click chat, type question, verify answer with sources
5. MVP is complete when Q&A works end-to-end!

### Incremental Delivery

1. Setup + Foundational → Widget skeleton visible
2. User Story 1 → Chat Q&A working (MVP!)
3. User Story 2 → Text selection feature added
4. User Story 3 → Mobile responsive
5. Polish → Production-ready

---

## Summary

| Phase | Tasks | Description |
|-------|-------|-------------|
| 1. Setup | T001-T003 | CORS + folder structure |
| 2. Foundational | T004-T008 | Config + Root injection |
| 3. US1 (P1) | T009-T027 | Chat Q&A (MVP) |
| 4. US2 (P2) | T028-T039 | Text selection |
| 5. US3 (P3) | T040-T045 | Mobile responsive |
| 6. Polish | T046-T052 | Edge cases + validation |

**Total Tasks**: 52
**MVP Scope**: T001-T027 (27 tasks)
**Parallel Opportunities**: CSS/JS can be parallelized within phases

---

## Notes

- All widget files in `src/components/ChatWidget/`
- Root.js in `src/theme/` for Docusaurus integration
- Backend CORS update in `backend/app/main.py`
- Run Docusaurus with `npm run start`
- Backend must be running on port 8000
- Commit after each phase completion
