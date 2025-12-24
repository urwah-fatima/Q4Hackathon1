# Feature Specification: Docusaurus RAG Chatbot Widget

**Feature Branch**: `004-docusaurus-chatbot`
**Created**: 2025-12-21
**Status**: Draft
**Input**: User description: "Embed RAG chatbot into the published Docusaurus book with selected-text support"

## Overview

Embed an interactive chatbot widget into the Physical AI & Humanoid Robotics Docusaurus book that allows readers to ask questions about book content. The chatbot integrates with the existing FastAPI RAG backend (Spec-3) and includes a special feature allowing users to highlight text on any page and ask questions about that specific selection.

## Target Audience

- Readers of the deployed book on GitHub Pages
- Researchers and students exploring Physical AI topics
- Developers integrating with the book content

## Dependencies

- **Spec-3** (003-rag-api-backend): FastAPI backend providing /chat endpoint

## User Scenarios & Testing

### User Story 1 - Ask Questions About Book Content (Priority: P1)

A reader browsing the Physical AI book wants to ask a question about a concept they're reading. They click the floating chatbot button, type their question, and receive an accurate answer with references to relevant book sections.

**Why this priority**: Core value proposition - readers can get instant answers without leaving the book. This is the fundamental feature that delivers the most value.

**Independent Test**: Can be fully tested by opening any book page, clicking the chat button, typing a question, and verifying the answer references book content.

**Acceptance Scenarios**:

1. **Given** a reader is on any page of the book, **When** they click the chatbot button, **Then** a chat panel opens ready for input
2. **Given** the chat panel is open, **When** the reader types a question and submits, **Then** they receive an answer within 5 seconds with source references
3. **Given** the reader receives an answer, **When** they click a source link, **Then** they are navigated to the relevant book section
4. **Given** the chat panel is open, **When** the reader asks an out-of-scope question, **Then** the system responds that the information is not in the book

---

### User Story 2 - Ask About Selected Text (Priority: P2)

A reader highlights a specific paragraph or sentence they don't understand. A contextual button appears (or right-click menu option) allowing them to ask questions about that highlighted text. The chatbot opens with the selected text pre-filled as context.

**Why this priority**: Enhances learning experience by allowing contextual questions. Differentiating feature that adds significant value beyond basic Q&A.

**Independent Test**: Can be tested by selecting text on any page, triggering the "Ask about this" action, and verifying the chatbot opens with the selection pre-filled.

**Acceptance Scenarios**:

1. **Given** a reader selects/highlights text on a page, **When** the selection is complete, **Then** an "Ask about this" button appears near the selection
2. **Given** the "Ask about this" button is visible, **When** the reader clicks it, **Then** the chat panel opens with the selected text displayed as context
3. **Given** the chat panel has selected text context, **When** the reader types a follow-up question, **Then** the answer specifically addresses the highlighted content
4. **Given** text is selected, **When** the reader right-clicks, **Then** a context menu option "Ask about this" is available

---

### User Story 3 - Responsive Mobile Experience (Priority: P3)

A reader accesses the book on a mobile device and wants to use the chatbot. The interface adapts to the smaller screen, providing a full-screen chat experience that is easy to use with touch input.

**Why this priority**: Extends accessibility to mobile readers. Important for broad adoption but secondary to core functionality.

**Independent Test**: Can be tested by accessing the book on a mobile device or using browser dev tools mobile emulation, verifying the chatbot is usable.

**Acceptance Scenarios**:

1. **Given** a reader is on a mobile device, **When** they tap the chatbot button, **Then** the chat opens in a mobile-optimized full-screen view
2. **Given** the chat is open on mobile, **When** the reader types a question, **Then** the keyboard doesn't obscure the input field
3. **Given** the chat is open on mobile, **When** the reader taps outside or swipes down, **Then** the chat panel closes smoothly

---

### Edge Cases

- What happens when the backend is unavailable? Display a friendly error message with suggestion to try later
- What happens when the user submits an empty question? Disable submit button until text is entered
- What happens when the response is very long? Display with scrollable area within the chat panel
- What happens when the user rapidly submits multiple questions? Queue requests and show loading state
- What happens on very slow connections? Show loading indicator and timeout message after 30 seconds
- What happens when selected text is extremely long (>1000 chars)? Truncate with indication and allow user to refine

## Requirements

### Functional Requirements

**Chat Widget Core**:
- **FR-001**: System MUST display a floating chat button visible on all book pages
- **FR-002**: System MUST open a chat panel when the user clicks the floating button
- **FR-003**: System MUST allow users to type questions in a text input field
- **FR-004**: System MUST send questions to the backend /chat endpoint
- **FR-005**: System MUST display the answer with clear formatting
- **FR-006**: System MUST display source references with clickable links to book sections
- **FR-007**: System MUST close the chat panel when user clicks outside or presses close button
- **FR-008**: System MUST persist chat history during the current page session

**Text Selection Integration**:
- **FR-009**: System MUST detect when user selects/highlights text on the page
- **FR-010**: System MUST display an "Ask about this" button near selected text
- **FR-011**: System MUST pre-fill the chat with selected text as context when triggered
- **FR-012**: System MUST include the selected text in the question sent to backend
- **FR-013**: System MUST provide right-click context menu option for selected text

**Visual Design**:
- **FR-014**: Chat widget MUST match the Docusaurus theme (light/dark mode support)
- **FR-015**: Chat widget MUST be positioned to not obscure main content
- **FR-016**: Chat widget MUST animate smoothly when opening/closing
- **FR-017**: System MUST show loading indicator while waiting for response

**Error Handling**:
- **FR-018**: System MUST display user-friendly error messages when backend is unavailable
- **FR-019**: System MUST prevent submission of empty questions
- **FR-020**: System MUST handle timeout gracefully with retry option

**Responsiveness**:
- **FR-021**: Chat widget MUST be usable on desktop browsers (Chrome, Firefox, Safari, Edge)
- **FR-022**: Chat widget MUST adapt to mobile screen sizes
- **FR-023**: Chat widget MUST support touch interactions on mobile devices

**Configuration**:
- **FR-024**: Backend API URL MUST be configurable for local development vs production

### Key Entities

- **ChatMessage**: Represents a single message in the conversation (role: user/assistant, content, timestamp)
- **Source**: A reference to a book section (title, url, relevance score)
- **TextSelection**: User-highlighted text with page context (text, pageUrl, position)

## Success Criteria

### Measurable Outcomes

- **SC-001**: Users can ask a question and receive an answer within 5 seconds
- **SC-002**: 95% of chatbot interactions complete without error
- **SC-003**: Chat widget loads within 1 second of page load
- **SC-004**: Text selection feature works on 100% of book content pages
- **SC-005**: Chat interface is fully usable on screens as small as 320px wide
- **SC-006**: Users can navigate from answer sources to correct book sections in one click
- **SC-007**: Chat widget integrates visually with Docusaurus theme (passes visual review)

## Assumptions

- Backend FastAPI server (Spec-3) will be running locally during development
- Production deployment strategy for backend is out of scope for this spec
- Docusaurus project uses standard theme with CSS custom properties for theming
- Modern browsers with ES6+ support are the target (no IE11 support needed)
- Chat history is session-only (not persisted across page reloads)

## Out of Scope

- Backend deployment or hosting configuration
- User authentication or personalization
- Conversation history across sessions
- Export or share chat functionality
- Voice input/output
- Multi-language support
- Analytics or tracking

## Technical Constraints

- Must use vanilla JavaScript or lightweight library (no React/Vue/Angular)
- Must integrate with existing Docusaurus project structure
- Must work with static site hosting (GitHub Pages)
- Backend API calls must handle CORS for local development
