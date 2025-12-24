# Implementation Plan: Docusaurus RAG Chatbot Widget

**Branch**: `004-docusaurus-chatbot` | **Date**: 2025-12-21 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-docusaurus-chatbot/spec.md`

## Summary

Embed an interactive chatbot widget into the Physical AI Docusaurus book that connects to the FastAPI RAG backend. Features include a floating chat button, chat panel with message history, text selection integration ("Ask about this"), and responsive mobile support. Uses vanilla JavaScript with Docusaurus theme integration.

## Technical Context

**Language/Version**: JavaScript ES6+, CSS3
**Package Manager**: npm (Docusaurus project)
**Primary Dependencies**: Docusaurus 3.x (existing), no new npm dependencies
**Storage**: sessionStorage for chat history
**Testing**: Manual browser testing
**Target Platform**: Modern browsers (Chrome, Firefox, Safari, Edge)
**Project Type**: Frontend widget integration
**Performance Goals**: < 1 second widget load, < 5 second response time
**Constraints**: Vanilla JS only (no React/Vue for widget), must match Docusaurus theme
**Scale/Scope**: Single widget, embedded in existing site

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-checked after Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. Accuracy First | PASS | Widget queries RAG backend which retrieves verified book content |
| II. Context Primacy | PASS | All answers grounded in indexed Docusaurus book content |
| III. Technical Rigor | PASS | Uses Docusaurus official extension patterns, standard web APIs |
| IV. Clarity | PASS | Chat UI provides clear, formatted answers with source links |
| V. Reproducibility | PASS | Step-by-step quickstart guide, all files documented |
| VI. Modularity | PASS | Self-contained widget component, doesn't modify Docusaurus core |

## Project Structure

### Documentation (this feature)

```text
specs/004-docusaurus-chatbot/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Technology decisions
├── data-model.md        # Entity definitions
├── quickstart.md        # Usage guide
└── tasks.md             # Implementation tasks (/sp.tasks)
```

### Source Code (extends Docusaurus project)

```text
src/
├── theme/
│   └── Root.js              # NEW: Wraps app, injects chatbot
├── components/
│   └── ChatWidget/          # NEW: Chatbot widget
│       ├── index.js         # Component export
│       ├── ChatWidget.js    # Main widget logic
│       ├── ChatWidget.css   # Styles (theme-aware)
│       └── config.js        # Configuration constants
└── css/
    └── custom.css           # Existing (add chat variables if needed)

backend/
└── app/
    └── main.py              # UPDATE: Add CORS middleware
```

**Structure Decision**: Use Docusaurus Root component swizzling to inject the chatbot globally. Widget is self-contained in `src/components/ChatWidget/` with vanilla JavaScript.

## Architecture

### Widget Component Structure

```
Root.js (Theme Override)
    │
    ├── Original Docusaurus App
    │
    └── ChatWidget
        ├── ChatButton (fixed position, bottom-right)
        │   └── Click → toggles isOpen
        │
        ├── ChatPanel (slide-in overlay)
        │   ├── Header (title + close button)
        │   ├── MessageList (scrollable)
        │   │   ├── UserMessage (right-aligned)
        │   │   └── AssistantMessage (left-aligned)
        │   │       └── SourceList (clickable links)
        │   ├── LoadingIndicator (when fetching)
        │   └── InputArea
        │       ├── ContextBadge (selected text preview)
        │       ├── TextInput (question input)
        │       └── SendButton
        │
        └── SelectionTooltip (appears near selected text)
            └── "Ask about this" button
```

### Data Flow

```
1. User selects text OR clicks chat button
                │
                ▼
2. ChatWidget updates state
   ├── isOpen: true
   └── currentSelection: {text, pageUrl}
                │
                ▼
3. User types question + submits
                │
                ▼
4. ChatWidget.sendMessage()
   ├── Add user message to state
   ├── Set isLoading: true
   └── Build request body with optional context
                │
                ▼
5. fetch(API_URL + '/chat', { body: {question} })
                │
                ▼
6. Receive response
   ├── Parse answer + sources
   ├── Add assistant message to state
   └── Set isLoading: false
                │
                ▼
7. MessageList re-renders with new message
   └── Sources rendered as clickable links
```

### Event Listeners

```javascript
// Text selection detection
document.addEventListener('mouseup', handleTextSelection);
document.addEventListener('touchend', handleTextSelection);

// Context menu (right-click)
document.addEventListener('contextmenu', handleContextMenu);

// Click outside to close
document.addEventListener('click', handleOutsideClick);

// Theme change detection
const observer = new MutationObserver(handleThemeChange);
observer.observe(document.documentElement, { attributes: true });
```

## Key Implementation Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| JS Framework | Vanilla ES6+ | User requirement; keeps bundle small |
| Styling | CSS with Docusaurus variables | Automatic theme sync |
| State Management | Plain object + DOM updates | Simple enough for widget scope |
| API Communication | Fetch API | Native, no library needed |
| Storage | sessionStorage | Session-only history per spec |
| Theme Detection | MutationObserver on data-theme | Reactive to theme toggle |

## CSS Variables Strategy

```css
/* Use Docusaurus CSS variables for theme integration */
.chat-widget {
  --chat-bg: var(--ifm-background-color);
  --chat-text: var(--ifm-font-color-base);
  --chat-border: var(--ifm-color-emphasis-300);
  --chat-primary: var(--ifm-color-primary);
  --chat-user-bg: var(--ifm-color-primary);
  --chat-assistant-bg: var(--ifm-background-surface-color);
}
```

## Backend CORS Update

Add to `backend/app/main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        # Add production domain when deploying
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Question Format with Context

When user selects text and asks a question:

```javascript
const questionWithContext = currentSelection
  ? `Context: "${currentSelection.text}"\n\nQuestion: ${userQuestion}`
  : userQuestion;

fetch(API_URL + '/chat', {
  method: 'POST',
  body: JSON.stringify({ question: questionWithContext })
});
```

## Mobile Responsiveness

```css
@media (max-width: 768px) {
  .chat-panel {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    width: 100%;
    height: 100%;
    border-radius: 0;
  }

  .chat-button {
    bottom: 16px;
    right: 16px;
  }
}
```

## Success Criteria

- [ ] Chat button visible on all book pages (bottom-right)
- [ ] Click button opens chat panel with animation
- [ ] Type question → receive answer within 5 seconds
- [ ] Sources displayed with clickable links
- [ ] Text selection shows "Ask about this" tooltip
- [ ] Selected text included as context in question
- [ ] Right-click menu includes "Ask about this"
- [ ] Mobile-responsive full-screen chat
- [ ] Light/dark theme automatically matched
- [ ] Error messages displayed when backend unavailable

## Generated Artifacts

| Artifact | Path | Status |
|----------|------|--------|
| Research Document | specs/004-docusaurus-chatbot/research.md | Complete |
| Data Model | specs/004-docusaurus-chatbot/data-model.md | Complete |
| Quickstart Guide | specs/004-docusaurus-chatbot/quickstart.md | Complete |

## Next Steps

1. Run `/sp.tasks` to generate implementation tasks
2. Add CORS middleware to backend (one-line update)
3. Create src/theme/Root.js to inject widget
4. Create src/components/ChatWidget/ files
5. Test with Docusaurus dev server
6. Verify all user stories work
