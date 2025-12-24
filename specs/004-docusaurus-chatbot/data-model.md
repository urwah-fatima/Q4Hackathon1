# Data Model: Docusaurus RAG Chatbot Widget

**Feature**: 004-docusaurus-chatbot
**Date**: 2025-12-21

## Frontend Entities

### ChatMessage

**Purpose**: Represents a single message in the chat conversation

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | string | Yes | Unique message identifier (timestamp-based) |
| role | string | Yes | "user" or "assistant" |
| content | string | Yes | Message text content |
| timestamp | Date | Yes | When the message was created |
| sources | Source[] | No | Array of sources (assistant messages only) |
| isLoading | boolean | No | True while waiting for response |
| error | string | No | Error message if request failed |

**JavaScript Representation**:
```javascript
const message = {
  id: 'msg-1703123456789',
  role: 'user',  // or 'assistant'
  content: 'What is physical AI?',
  timestamp: new Date(),
  sources: [],
  isLoading: false,
  error: null
};
```

### Source

**Purpose**: A reference to a book section returned by the backend

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | Yes | Page/section title |
| url | string | Yes | Link to the book section |
| chunk_index | number | Yes | Position of chunk in page |
| score | number | Yes | Relevance score (0.0-1.0) |
| snippet | string | No | Text preview (first 100 chars) |

**JavaScript Representation**:
```javascript
const source = {
  title: 'Introduction to Physical AI',
  url: '/intro',
  chunk_index: 0,
  score: 0.89,
  snippet: 'Physical AI refers to...'
};
```

### TextSelection

**Purpose**: User-highlighted text with page context

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| text | string | Yes | The selected text content |
| pageUrl | string | Yes | Current page URL |
| position | object | No | Screen coordinates for tooltip |

**JavaScript Representation**:
```javascript
const selection = {
  text: 'reinforcement learning for robot control',
  pageUrl: '/module-4-vla/speech-to-command',
  position: { x: 450, y: 200 }
};
```

### ChatState

**Purpose**: Overall state of the chatbot widget

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| isOpen | boolean | Yes | Whether chat panel is visible |
| messages | ChatMessage[] | Yes | Array of chat messages |
| currentSelection | TextSelection | No | Currently selected text |
| isLoading | boolean | Yes | Waiting for API response |
| error | string | No | Current error message |
| inputValue | string | Yes | Current input field value |

**JavaScript Representation**:
```javascript
const chatState = {
  isOpen: false,
  messages: [],
  currentSelection: null,
  isLoading: false,
  error: null,
  inputValue: ''
};
```

## API Request/Response (from Backend)

### ChatRequest

**Purpose**: Request body for /chat endpoint

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| question | string | Yes | User's question (may include context) |

**Format**:
```json
{
  "question": "What is physical AI?"
}
```

**With Selection Context**:
```json
{
  "question": "Context: \"reinforcement learning for robot control\"\n\nExplain this concept in more detail."
}
```

### ChatResponse

**Purpose**: Response from /chat endpoint

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| answer | string | Yes | Generated answer text |
| sources | Source[] | Yes | Array of source references |

**Format**:
```json
{
  "answer": "Physical AI refers to...",
  "sources": [
    {
      "title": "Introduction to Physical AI",
      "url": "/intro",
      "chunk_index": 0,
      "score": 0.89,
      "snippet": "Physical AI refers to..."
    }
  ]
}
```

## UI Component Structure

```
ChatWidget (Root Component)
├── ChatButton
│   └── Icon + Badge (unread indicator)
├── ChatPanel
│   ├── ChatHeader
│   │   └── Title + Close Button
│   ├── MessageList
│   │   ├── UserMessage (for each user message)
│   │   └── AssistantMessage (for each assistant message)
│   │       └── SourceList
│   │           └── SourceLink (for each source)
│   ├── LoadingIndicator (when waiting)
│   └── InputArea
│       ├── ContextBadge (selected text preview)
│       ├── TextInput
│       └── SendButton
└── SelectionTooltip
    └── "Ask about this" button
```

## State Transitions

```
Initial State
    │
    ▼
┌───────────────┐
│  isOpen: false │
│  messages: []  │
│  selection: null│
└───────────────┘
    │
    ├─── User clicks chat button ───┐
    │                               ▼
    │                     ┌───────────────┐
    │                     │  isOpen: true  │
    │                     │  Panel visible │
    │                     └───────────────┘
    │                               │
    │                               ├─── User types + sends ───┐
    │                               │                          ▼
    │                               │               ┌───────────────┐
    │                               │               │ isLoading: true│
    │                               │               │ User message   │
    │                               │               │ added          │
    │                               │               └───────────────┘
    │                               │                          │
    │                               │                          ▼
    │                               │               ┌───────────────┐
    │                               │               │ isLoading: false│
    │                               │               │ Assistant msg  │
    │                               │               │ added          │
    │                               │               └───────────────┘
    │                               │
    └─── User selects text ─────────┼───┐
                                    │   ▼
                                    │ ┌───────────────┐
                                    │ │ selection: {...}│
                                    │ │ Tooltip shown  │
                                    │ └───────────────┘
                                    │         │
                                    │         ├─── Clicks "Ask about this" ───┐
                                    │         │                               ▼
                                    │         │                    ┌───────────────┐
                                    │         │                    │ isOpen: true   │
                                    │         │                    │ Context badge  │
                                    │         │                    │ visible        │
                                    │         │                    └───────────────┘
                                    │         │
                                    │         └─── Clicks elsewhere ───┐
                                    │                                  ▼
                                    │                       ┌───────────────┐
                                    │                       │ selection: null│
                                    │                       │ Tooltip hidden │
                                    │                       └───────────────┘
```

## Configuration

### ChatConfig

**Purpose**: Widget configuration options

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| apiUrl | string | http://localhost:8000 | Backend API base URL |
| position | string | bottom-right | Button position |
| theme | string | auto | light, dark, or auto (follows Docusaurus) |
| maxMessages | number | 50 | Max messages to keep in memory |
| timeout | number | 30000 | API request timeout in ms |

**JavaScript Representation**:
```javascript
const config = {
  apiUrl: process.env.CHATBOT_API_URL || 'http://localhost:8000',
  position: 'bottom-right',
  theme: 'auto',
  maxMessages: 50,
  timeout: 30000
};
```

## Local Storage (Session)

The chatbot stores conversation in sessionStorage for page refresh persistence:

```javascript
// Key: 'chatbot-messages'
// Value: JSON array of ChatMessage objects
sessionStorage.setItem('chatbot-messages', JSON.stringify(messages));
```

Note: Chat history is NOT persisted across browser sessions (per spec).
