---
id: 003
title: Generate Chatbot Widget Tasks
stage: tasks
date: 2025-12-21
surface: agent
model: claude-opus-4-5-20251101
feature: 004-docusaurus-chatbot
branch: 004-docusaurus-chatbot
user: developer
command: /sp.tasks
labels: ["tasks", "implementation", "docusaurus", "chatbot", "vanilla-js"]
links:
  spec: specs/004-docusaurus-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/004-docusaurus-chatbot/tasks.md
tests:
  - Task format validation passed
---

## Prompt

/sp.tasks

Generate implementation tasks based on plan.md and spec.md for Docusaurus chatbot widget.

## Response snapshot

Generated tasks.md with 52 tasks across 6 phases:

**Phase 1: Setup** (T001-T003)
- Add CORS middleware to backend
- Create component folder structure

**Phase 2: Foundational** (T004-T008)
- Create config.js with API settings
- Create ChatWidget.css with base styles
- Create Root.js theme override

**Phase 3: User Story 1 - Chat Q&A** (T009-T027) MVP
- Floating chat button (fixed position)
- Chat panel (header, messages, input)
- Message rendering (user/assistant)
- Source links (clickable navigation)
- API integration (fetch /chat)
- Loading states and error handling
- Theme integration (light/dark)

**Phase 4: User Story 2 - Text Selection** (T028-T039)
- Selection detection (mouseup/touchend)
- "Ask about this" tooltip
- Context badge in input area
- Right-click context menu
- Context prefix in question

**Phase 5: User Story 3 - Mobile** (T040-T045)
- Full-screen layout on mobile
- Touch-friendly sizing
- Swipe-to-close gesture

**Phase 6: Polish** (T046-T052)
- Input validation
- Text truncation
- Accessibility
- Cross-browser testing

**Summary**:
- Total: 52 tasks
- MVP: 27 tasks (T001-T027)
- Single component architecture (ChatWidget/)

## Outcome

- ✅ Impact: Complete task list for implementing Docusaurus chatbot widget
- 🧪 Tests: Format validation passed
- 📁 Files: specs/004-docusaurus-chatbot/tasks.md
- 🔁 Next prompts: /sp.implement or manually execute tasks
- 🧠 Reflection: Tasks cleanly separate core chat (US1), text selection (US2), and mobile (US3). MVP delivers value with just US1.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Format validation PASS
- Prompt variant (if applicable): Standard /sp.tasks flow
- Next experiment (smallest change to try): N/A - tasks complete
