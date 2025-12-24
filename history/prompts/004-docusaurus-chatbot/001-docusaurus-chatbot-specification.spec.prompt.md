---
id: 001
title: Docusaurus Chatbot Specification
stage: spec
date: 2025-12-21
surface: agent
model: claude-opus-4-5-20251101
feature: 004-docusaurus-chatbot
branch: 004-docusaurus-chatbot
user: developer
command: /sp.specify
labels: ["docusaurus", "chatbot", "widget", "text-selection", "rag", "frontend"]
links:
  spec: specs/004-docusaurus-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/004-docusaurus-chatbot/spec.md
  - specs/004-docusaurus-chatbot/checklists/requirements.md
tests:
  - Specification quality checklist validated
---

## Prompt

/sp.specify

Embed RAG chatbot into the published Docusaurus book with selected-text support
Target audience: Readers of the deployed book on GitHub Pages
Focus: Seamless in-page chatbot that answers questions using only book content, with special support for questions about user-highlighted text
Success criteria:
- Chatbot UI visibly embedded in the Docusaurus site (e.g., floating button or sidebar)
- Users can type questions and get accurate, sourced answers from the book
- Users can select/highlight any text on a page → click "Ask about this" (or right-click) → chatbot opens pre-filled with that text as context
- All answers generated via the existing FastAPI backend (/chat endpoint)
- Works locally and on the deployed GitHub Pages site
- Responsive, clean design matching Docusaurus theme
Constraints:
- Modify only the existing Docusaurus book project (no new repo)
- Backend remains the uv-managed FastAPI server from spec-3 (run locally for now)
- Use vanilla JS or lightweight library (no heavy framework)

## Response snapshot

Created feature specification for Docusaurus RAG Chatbot Widget with:

**User Stories**:
- US1 (P1): Ask questions about book content - core Q&A functionality
- US2 (P2): Ask about selected/highlighted text - contextual questions
- US3 (P3): Responsive mobile experience - touch-friendly UI

**Functional Requirements**: 24 requirements covering:
- Chat widget core (floating button, chat panel, input/output)
- Text selection integration (detect selection, "Ask about this" button, context menu)
- Visual design (theme matching, animations, loading states)
- Error handling (backend unavailable, empty input, timeouts)
- Responsiveness (desktop/mobile, touch support)
- Configuration (API URL for dev/prod)

**Key Entities**:
- ChatMessage (role, content, timestamp)
- Source (title, url, score)
- TextSelection (text, pageUrl, position)

**Success Criteria**: 7 measurable outcomes (response time, error rate, load time, coverage, mobile width, navigation, visual review)

All checklist items passed - no clarifications needed.

## Outcome

- ✅ Impact: Complete specification for embedding RAG chatbot in Docusaurus book
- 🧪 Tests: Specification quality checklist validated (all items pass)
- 📁 Files: spec.md, checklists/requirements.md
- 🔁 Next prompts: /sp.plan to create implementation plan
- 🧠 Reflection: Clean spec with text-selection as differentiating feature. Vanilla JS constraint keeps it lightweight.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Checklist PASS
- Prompt variant (if applicable): Standard /sp.specify flow
- Next experiment (smallest change to try): N/A - spec complete
