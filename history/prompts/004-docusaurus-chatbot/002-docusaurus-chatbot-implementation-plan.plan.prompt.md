---
id: 002
title: Docusaurus Chatbot Implementation Plan
stage: plan
date: 2025-12-21
surface: agent
model: claude-opus-4-5-20251101
feature: 004-docusaurus-chatbot
branch: 004-docusaurus-chatbot
user: developer
command: /sp.plan
labels: ["docusaurus", "chatbot", "vanilla-js", "text-selection", "frontend"]
links:
  spec: specs/004-docusaurus-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/004-docusaurus-chatbot/plan.md
  - specs/004-docusaurus-chatbot/research.md
  - specs/004-docusaurus-chatbot/data-model.md
  - specs/004-docusaurus-chatbot/quickstart.md
tests:
  - Constitution check passed (6/6 principles)
---

## Prompt

/sp.plan

Embed chatbot UI in Docusaurus and connect to FastAPI backend with selected-text feature
- Work in the existing Docusaurus book project; add custom components/scripts in src/theme or static folder
- Add floating chatbot button (bottom-right) using custom NavbarItem or MDX component; opens modal/panel with chat interface
- Chat UI: Simple HTML + CSS + vanilla JS; input box, message history, send button; POST to http://localhost:8000/chat
- Selected-text feature: Inject JS to listen for text selection → show "Ask about this" context menu or tooltip → populate chat input with selected text + "Explain this:" prompt
- Enable CORS on FastAPI backend (add uv add "fastapi[all]" if needed, then app.add_middleware(CORSMiddleware, allow_origins=["*"] for dev))
- Success: Run Docusaurus locally → open book → type or highlight+ask → chatbot answers correctly using only book content; sources shown/linked

## Response snapshot

Created implementation plan for Docusaurus chatbot widget with:

**Architecture**:
- Root.js theme override to inject chatbot globally
- ChatWidget component in src/components/ChatWidget/
- Vanilla JS for all interactions (no React/Vue for widget)
- CSS variables for Docusaurus theme integration

**Key Decisions**:
- Use Docusaurus Root component swizzling
- sessionStorage for session-only chat history
- MutationObserver for theme change detection
- Fetch API for backend communication

**Research Topics**:
- Docusaurus component injection patterns
- Text selection detection with getSelection()
- Custom context menu implementation
- CORS middleware for FastAPI

**Data Model**:
- ChatMessage (id, role, content, timestamp, sources)
- Source (title, url, chunk_index, score)
- TextSelection (text, pageUrl, position)
- ChatState (isOpen, messages, currentSelection, isLoading)

**Backend Update**: Add CORSMiddleware to allow localhost:3000

Constitution check: 6/6 principles passed.

## Outcome

- ✅ Impact: Complete plan for embedding RAG chatbot in Docusaurus
- 🧪 Tests: Constitution check (6/6)
- 📁 Files: plan.md, research.md, data-model.md, quickstart.md
- 🔁 Next prompts: /sp.tasks to generate implementation tasks
- 🧠 Reflection: Vanilla JS approach keeps bundle size minimal. Text selection feature differentiates from standard chatbots.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Constitution PASS (6/6)
- Prompt variant (if applicable): User-specified vanilla JS + CORS requirements
- Next experiment (smallest change to try): N/A - plan complete
