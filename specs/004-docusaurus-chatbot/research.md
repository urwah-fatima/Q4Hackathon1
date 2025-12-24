# Research: Docusaurus RAG Chatbot Widget

**Feature**: 004-docusaurus-chatbot
**Date**: 2025-12-21

## Research Questions

### RQ1: Docusaurus Custom Component Integration

**Question**: How to inject custom JavaScript and UI components into Docusaurus?

**Decision**: Use client modules and custom theme components

**Rationale**:
- Docusaurus supports `clientModules` in config for injecting JS on every page
- Custom theme components in `src/theme/` can override or extend default theme
- Static files in `static/` are served as-is and can be referenced

**Implementation Approach**:
```
src/
├── theme/
│   └── Root.js           # Wrap entire app, inject chatbot
├── components/
│   └── ChatWidget/       # Chatbot component files
│       ├── index.js
│       ├── styles.css
│       └── chatbot.js
static/
└── js/
    └── chatbot.js        # Alternative: vanilla JS loaded via script
```

**Alternatives Considered**:
- Plugin approach: Overkill for single widget, requires npm package structure
- MDX component: Only appears where explicitly added, not global
- Swizzling NavbarItem: Limited to navbar, not ideal for floating button

### RQ2: Floating Button + Modal Pattern

**Question**: How to implement a floating chat button that opens a modal/panel?

**Decision**: Fixed-position button with slide-in panel overlay

**Rationale**:
- Fixed positioning ensures visibility on all pages
- Slide-in panel provides better UX than modal (doesn't block entire screen)
- CSS transitions provide smooth animations
- Z-index management keeps button above content

**Implementation Pattern**:
```css
.chat-button {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
}

.chat-panel {
  position: fixed;
  bottom: 80px;
  right: 20px;
  width: 380px;
  height: 500px;
  z-index: 999;
  transform: translateY(20px);
  opacity: 0;
  transition: all 0.3s ease;
}

.chat-panel.open {
  transform: translateY(0);
  opacity: 1;
}
```

### RQ3: Text Selection Detection

**Question**: How to detect text selection and show contextual button?

**Decision**: Use `mouseup`/`touchend` events with `window.getSelection()`

**Rationale**:
- `window.getSelection()` is cross-browser compatible
- Event delegation reduces number of event listeners
- Positioning tooltip near selection using `getBoundingClientRect()`

**Implementation Pattern**:
```javascript
document.addEventListener('mouseup', (e) => {
  const selection = window.getSelection();
  const selectedText = selection.toString().trim();

  if (selectedText.length > 0) {
    const range = selection.getRangeAt(0);
    const rect = range.getBoundingClientRect();
    showAskButton(rect.left + rect.width / 2, rect.top - 10);
  } else {
    hideAskButton();
  }
});
```

**Alternatives Considered**:
- Selection change event: Fires too frequently, poor performance
- MutationObserver: Not designed for selection, overkill
- Context menu only: Less discoverable than tooltip button

### RQ4: Right-Click Context Menu Integration

**Question**: How to add "Ask about this" to the browser context menu?

**Decision**: Custom context menu overlay (not native browser menu)

**Rationale**:
- Native context menu modification requires browser extension
- Custom overlay is fully controllable and cross-browser
- Can match Docusaurus theme styling

**Implementation Pattern**:
```javascript
document.addEventListener('contextmenu', (e) => {
  const selection = window.getSelection().toString().trim();
  if (selection.length > 0) {
    e.preventDefault();
    showCustomContextMenu(e.clientX, e.clientY, selection);
  }
});
```

### RQ5: Docusaurus Theme Integration (Light/Dark Mode)

**Question**: How to make chatbot match Docusaurus light/dark theme?

**Decision**: Use CSS custom properties from Docusaurus theme

**Rationale**:
- Docusaurus uses CSS variables like `--ifm-color-primary`
- `data-theme="dark"` attribute on html element indicates dark mode
- CSS can respond to theme changes without JavaScript

**Implementation Pattern**:
```css
.chat-panel {
  background: var(--ifm-background-color);
  color: var(--ifm-font-color-base);
  border: 1px solid var(--ifm-color-emphasis-300);
}

[data-theme='dark'] .chat-panel {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
}
```

### RQ6: CORS Configuration for FastAPI

**Question**: How to enable CORS for frontend-backend communication?

**Decision**: Add CORSMiddleware with permissive settings for development

**Rationale**:
- Docusaurus runs on port 3000, FastAPI on 8000
- CORS middleware needed for cross-origin requests
- Allow all origins for development (restrict in production)

**Implementation Pattern** (backend update):
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["http://localhost:3000"] for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### RQ7: API Communication Pattern

**Question**: Best pattern for chat API calls from frontend?

**Decision**: Async fetch with loading states and error handling

**Rationale**:
- Fetch API is native and sufficient for simple POST requests
- Async/await provides clean error handling
- AbortController enables request cancellation

**Implementation Pattern**:
```javascript
async function sendQuestion(question, selectedText = null) {
  const body = { question: selectedText
    ? `Context: "${selectedText}"\n\nQuestion: ${question}`
    : question
  };

  const response = await fetch(API_URL + '/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });

  if (!response.ok) throw new Error('API request failed');
  return response.json();
}
```

## Technology Stack Summary

| Component | Choice | Notes |
|-----------|--------|-------|
| UI Injection | Docusaurus Root component | Wraps entire app |
| Styling | CSS with Docusaurus variables | Theme-aware |
| JavaScript | Vanilla ES6+ | No frameworks |
| API Calls | Fetch API | Native browser |
| Backend CORS | FastAPI CORSMiddleware | Allow localhost |

## File Structure

```
src/
├── theme/
│   └── Root.js               # Injects chatbot component
├── components/
│   └── ChatWidget/
│       ├── index.js          # Main component export
│       ├── ChatWidget.js     # Core chatbot logic
│       └── ChatWidget.css    # Styles with CSS variables
└── css/
    └── custom.css            # Existing, add chat variables if needed

static/
└── (no changes needed)
```

## Backend Update Required

Add CORS middleware to `backend/app/main.py`:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## References

- [Docusaurus Swizzling](https://docusaurus.io/docs/swizzling)
- [Docusaurus Client Modules](https://docusaurus.io/docs/api/docusaurus-config#clientModules)
- [MDN Selection API](https://developer.mozilla.org/en-US/docs/Web/API/Selection)
- [FastAPI CORS](https://fastapi.tiangolo.com/tutorial/cors/)
