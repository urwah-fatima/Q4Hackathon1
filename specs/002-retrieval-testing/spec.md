# Feature Specification: Retrieval Testing Pipeline

**Feature Branch**: `002-retrieval-testing`
**Created**: 2025-12-20
**Status**: Draft
**Input**: User description: "Retrieval testing pipeline for Qdrant-indexed book content to verify indexing quality before building the chatbot backend"

## Overview

This feature provides a testing utility for developers to verify that the RAG ingestion pipeline (Spec-1) has correctly indexed book content. Before building the chatbot backend, developers need confidence that semantic search over the embedded chunks returns accurate, relevant results. This is a developer-facing quality assurance tool, not a user-facing feature.

**Target Audience**:
- Developers verifying indexing quality
- QA engineers validating RAG system readiness
- Technical evaluators assessing retrieval accuracy

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Run Retrieval Test Suite (Priority: P1)

A developer wants to run a predefined set of test queries against the indexed book content to verify that semantic search returns relevant chunks for each query.

**Why this priority**: This is the core functionality. Without the ability to run test queries and see results, the developer cannot validate indexing quality.

**Independent Test**: Run the test script with predefined queries and observe that results are displayed with relevance scores.

**Acceptance Scenarios**:

1. **Given** the indexed book content in Qdrant, **When** the developer runs the test script, **Then** it executes 5+ predefined test queries covering different book topics
2. **Given** a test query, **When** the search completes, **Then** the top-3 retrieved chunks are displayed with text, source URL, metadata, and similarity scores
3. **Given** the test results, **When** the developer reviews them, **Then** they can assess whether retrieved chunks are relevant to each query

---

### User Story 2 - Interactive Query Testing (Priority: P2)

A developer wants to enter custom queries interactively to explore the indexed content and test edge cases not covered by the predefined test suite.

**Why this priority**: After validating with predefined queries, developers need flexibility to test custom scenarios and investigate specific content areas.

**Independent Test**: Run the script in interactive mode, enter a custom query, and observe results.

**Acceptance Scenarios**:

1. **Given** the test script running, **When** the developer provides a custom query, **Then** the system performs semantic search and displays results
2. **Given** an interactive session, **When** the developer enters multiple queries, **Then** each query returns results without restarting the script

---

### User Story 3 - Handle Edge Cases Gracefully (Priority: P3)

A developer wants the script to handle edge cases (no results, low scores, connection errors) gracefully so that testing doesn't crash unexpectedly.

**Why this priority**: Robust error handling ensures the testing tool is reliable and provides useful feedback even when issues occur.

**Independent Test**: Run queries that produce edge cases and observe graceful handling with informative messages.

**Acceptance Scenarios**:

1. **Given** a query with no matching content, **When** the search returns zero results, **Then** a clear message indicates "No results found" rather than crashing
2. **Given** results with low similarity scores (below threshold), **When** displayed, **Then** a warning indicates the results may not be highly relevant
3. **Given** a connection error to Qdrant, **When** the script attempts to query, **Then** a clear error message is displayed with troubleshooting hints

---

### Edge Cases

- What happens when no results are returned for a query?
  - Display "No results found for query: [query text]" and continue
- What happens when similarity scores are very low (e.g., below 0.5)?
  - Display results with a warning: "Low relevance - scores below threshold"
- What happens when Qdrant connection fails?
  - Display error message with connection details and suggest checking .env configuration
- What happens when the collection doesn't exist?
  - Display error: "Collection 'book_chatbot_embedding' not found. Run ingestion first."
- What happens when query embedding fails?
  - Display error with Cohere API details and suggest checking API key

## Requirements *(mandatory)*

### Functional Requirements

**Query Execution**

- **FR-001**: System MUST accept natural language queries as input
- **FR-002**: System MUST embed queries using the same embedding model as ingestion (Cohere embed-english-v3.0)
- **FR-003**: System MUST perform similarity search against the indexed collection
- **FR-004**: System MUST retrieve top-K results (default K=3, configurable)

**Result Display**

- **FR-005**: System MUST display the retrieved text content for each result
- **FR-006**: System MUST display the source URL for each result
- **FR-007**: System MUST display the chunk metadata (title, chunk_index) for each result
- **FR-008**: System MUST display the similarity score for each result
- **FR-009**: System MUST format output for easy reading in terminal

**Test Suite**

- **FR-010**: System MUST include at least 5 predefined test queries covering diverse book topics
- **FR-011**: System MUST run all predefined queries when invoked in batch mode
- **FR-012**: System MUST support interactive mode for custom queries

**Error Handling**

- **FR-013**: System MUST handle empty result sets gracefully with informative messages
- **FR-014**: System MUST warn when similarity scores fall below a relevance threshold
- **FR-015**: System MUST handle connection errors with clear error messages
- **FR-016**: System MUST validate that the target collection exists before querying

**Configuration**

- **FR-017**: System MUST read credentials from environment variables (same as ingestion script)
- **FR-018**: System MUST use the same collection name as the ingestion pipeline (book_chatbot_embedding)

### Key Entities

- **TestQuery**: A natural language question used to test retrieval; includes query text and expected topic area
- **SearchResult**: A retrieved chunk from Qdrant; includes text, URL, title, chunk_index, and similarity score
- **TestRun**: A complete execution of the test suite; tracks queries executed and results per query

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Test script executes all 5+ predefined queries in under 30 seconds total
- **SC-002**: For each predefined query, at least 2 of the top-3 results are relevant to the query topic (subjective developer assessment)
- **SC-003**: All results display complete metadata (text, URL, title, chunk_index, score)
- **SC-004**: Edge cases (no results, low scores, errors) are handled without script crashes
- **SC-005**: Developer can complete a full test run and assessment in under 5 minutes

## Assumptions

- The ingestion pipeline (Spec-1) has already been run and the collection is populated
- The same Qdrant Cloud instance and collection (book_chatbot_embedding) is used
- The same Cohere API key and embedding model (embed-english-v3.0) is used for query embedding
- The existing uv-managed backend project is used (no new project initialization)
- Relevance threshold for warnings is 0.5 similarity score (configurable)
- Top-K default is 3 results per query

## Out of Scope

- Automated relevance scoring or evaluation metrics
- FastAPI endpoints or REST API
- Frontend UI or web interface
- Agent logic or LLM-based answer generation
- Performance benchmarking or load testing
- Modifying the indexed content

## Dependencies

- **Prerequisite Feature**: 001-rag-ingestion-pipeline (must be complete and collection populated)
- **External Services**:
  - Qdrant Cloud (same instance as ingestion)
  - Cohere API (for query embedding)
- **Existing Project**: backend/ folder with uv configuration
