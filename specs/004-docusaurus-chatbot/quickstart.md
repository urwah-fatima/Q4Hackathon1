# Quickstart: Docusaurus RAG Chatbot Widget

**Feature**: 004-docusaurus-chatbot
**Date**: 2025-12-21

## Prerequisites

- Completed 003-rag-api-backend (FastAPI server with /chat endpoint)
- Existing Docusaurus book project with `npm install` completed
- Node.js 18+ and npm installed

## Setup

### 1. Start the Backend Server

In a separate terminal:

```bash
cd backend
uv run uvicorn app.main:app --reload
```

Verify it's running: `curl http://localhost:8000/health`

### 2. Enable CORS on Backend

Add CORS middleware to `backend/app/main.py` (if not already present):

```python
from fastapi.middleware.cors import CORSMiddleware

# Add after app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3. Create Chatbot Component

Create the component directory:

```bash
mkdir -p src/components/ChatWidget
```

Create the main files:
- `src/components/ChatWidget/index.js`
- `src/components/ChatWidget/ChatWidget.js`
- `src/components/ChatWidget/ChatWidget.css`

### 4. Create Root Theme Override

Create the Root component to inject the chatbot:

```bash
mkdir -p src/theme
touch src/theme/Root.js
```

### 5. Start Docusaurus

```bash
npm run start
```

Opens at http://localhost:3000

## Usage

### Basic Question

1. Click the chat button (bottom-right corner)
2. Type a question: "What is physical AI?"
3. Press Enter or click Send
4. View the answer and click sources to navigate

### Ask About Selected Text

1. Highlight any text on a book page
2. Click "Ask about this" tooltip (or right-click → "Ask about this")
3. The chat opens with the text pre-filled
4. Add a follow-up question or just press Enter
5. Receive contextual answer about the highlighted text

### Mobile Usage

1. Tap the chat button
2. Chat opens in full-screen mode
3. Type question using on-screen keyboard
4. Tap outside or swipe down to close

## Expected Behavior

### Chat Panel

```
┌─────────────────────────────────┐
│ 📚 Book Assistant            ✕ │
├─────────────────────────────────┤
│                                 │
│  [User bubble]                  │
│  What is physical AI?           │
│                                 │
│  [Assistant bubble]             │
│  Physical AI refers to AI       │
│  systems that interact with     │
│  the physical world...          │
│                                 │
│  📖 Sources:                    │
│  • Introduction to Physical AI  │
│  • Embodied Intelligence        │
│                                 │
├─────────────────────────────────┤
│ [Type your question...     ] 📤 │
└─────────────────────────────────┘
```

### Selection Tooltip

```
"reinforcement learning"
        │
        ▼
   ┌─────────────────┐
   │ Ask about this  │
   └─────────────────┘
```

## Testing Checklist

### User Story 1: Basic Chat

- [ ] Chat button visible on all pages
- [ ] Click opens chat panel
- [ ] Type question and receive answer
- [ ] Answer shows within 5 seconds
- [ ] Sources displayed with links
- [ ] Click source navigates to section
- [ ] Close button works
- [ ] Click outside closes panel

### User Story 2: Text Selection

- [ ] Select text on any page
- [ ] "Ask about this" tooltip appears
- [ ] Click tooltip opens chat with context
- [ ] Right-click shows "Ask about this" option
- [ ] Context displayed in chat input area
- [ ] Submit sends question with context
- [ ] Answer addresses the selected text

### User Story 3: Mobile

- [ ] Button visible on mobile viewport
- [ ] Tap opens full-screen chat
- [ ] Keyboard doesn't obscure input
- [ ] Tap outside/swipe closes chat
- [ ] Text selection works on mobile

### Error Handling

- [ ] Backend unavailable shows error message
- [ ] Empty question disabled
- [ ] Timeout after 30 seconds with message
- [ ] Network error shows retry option

### Theme

- [ ] Light mode styling correct
- [ ] Dark mode styling correct
- [ ] Theme switch updates chat appearance

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Chat button not visible | Check Root.js is loading ChatWidget |
| CORS error in console | Add CORS middleware to backend |
| "Connection refused" | Start backend server on port 8000 |
| Style not matching theme | Check CSS uses Docusaurus variables |
| Selection tooltip not appearing | Check mouseup event listener registered |
| Mobile layout broken | Check responsive CSS media queries |

## Configuration

Edit `src/components/ChatWidget/config.js`:

```javascript
export const config = {
  // Change for production deployment
  apiUrl: 'http://localhost:8000',

  // Max messages to keep in session
  maxMessages: 50,

  // API timeout in milliseconds
  timeout: 30000,

  // Position of chat button
  position: 'bottom-right'
};
```

## File Structure After Setup

```
src/
├── theme/
│   └── Root.js               # Injects chatbot globally
├── components/
│   └── ChatWidget/
│       ├── index.js          # Component export
│       ├── ChatWidget.js     # Main chatbot logic
│       ├── ChatWidget.css    # Styles
│       └── config.js         # Configuration
└── css/
    └── custom.css            # Existing Docusaurus styles

backend/
└── app/
    └── main.py               # Add CORS middleware here
```

## Next Steps

1. Complete implementation of all component files
2. Test all user stories
3. Verify theme integration (light/dark mode)
4. Test on mobile devices
5. Configure production API URL when deploying
