# Feature Specification: RAG Website URL Ingestion, Embedding Generation, and Vector Storage

**Feature Branch**: `001-rag-ingestion-pipeline`
**Created**: 2025-12-19
**Status**: Draft
**Input**: User description: "Create a repeatable pipeline that extracts text from deployed Docusaurus website URLs, chunks content for semantic retrieval, generates vector embeddings using Cohere models, and stores them in Qdrant Cloud"

## Overview

This feature creates a foundational RAG (Retrieval-Augmented Generation) ingestion pipeline for the Physical AI & Humanoid Robotics Book project. The pipeline prepares deployed book content for intelligent querying by extracting text from the Docusaurus website, generating vector embeddings, and storing them in a vector database.

**Target Audience**:
- AI developers building RAG systems
- Backend engineers implementing vector search
- Students learning RAG implementation patterns
- Evaluators assessing end-to-end RAG readiness

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Initial Content Ingestion (Priority: P1)

A developer wants to ingest all book content from the deployed Docusaurus website into the vector database so that the content is ready for semantic search queries.

**Why this priority**: This is the core functionality. Without successful ingestion of content into the vector database, no other RAG capabilities can function. This delivers the foundational value of making book content searchable.

**Independent Test**: Can be fully tested by running the ingestion pipeline against the deployed website and verifying chunks appear in Qdrant with correct metadata.

**Acceptance Scenarios**:

1. **Given** a list of deployed Docusaurus book URLs, **When** the ingestion pipeline runs, **Then** all pages are crawled and text content is extracted successfully
2. **Given** extracted page content, **When** the chunking process runs, **Then** content is split into appropriately-sized chunks with overlap for context preservation
3. **Given** text chunks, **When** embeddings are generated, **Then** each chunk has a corresponding vector embedding with consistent dimensionality
4. **Given** embeddings and metadata, **When** stored in Qdrant, **Then** each record contains source URL, page title, chunk index, and text content

---

### User Story 2 - Pipeline Verification (Priority: P2)

A developer wants to verify that the ingestion was successful and that the stored content is queryable so that they can confirm the system is ready for RAG queries.

**Why this priority**: Verification is essential to confirm the pipeline worked correctly before building query-time features. Without verification, developers cannot trust the ingested data.

**Independent Test**: Can be fully tested by running the verification script after ingestion and checking all validation checks pass.

**Acceptance Scenarios**:

1. **Given** a completed ingestion run, **When** the verification script runs, **Then** it reports the total number of chunks stored in Qdrant
2. **Given** stored embeddings, **When** a test similarity search is performed, **Then** relevant chunks are returned based on semantic similarity
3. **Given** the verification results, **When** reviewed by the developer, **Then** insertion success rates and any errors are clearly reported

---

### User Story 3 - Content Update Re-ingestion (Priority: P3)

A developer wants to re-run the pipeline after book content updates so that the vector database stays synchronized with the latest published content.

**Why this priority**: Content will evolve over time, and the pipeline must support safe re-runs. This ensures long-term maintainability of the RAG system.

**Independent Test**: Can be fully tested by modifying a test page, re-running the pipeline, and verifying the updated content appears in Qdrant.

**Acceptance Scenarios**:

1. **Given** existing content in Qdrant, **When** the pipeline runs again with updated source URLs, **Then** the database is updated without creating duplicate entries
2. **Given** a re-run of the pipeline, **When** completed, **Then** a summary shows what was added, updated, or unchanged

---

### Edge Cases

- What happens when a URL returns a 404 or is unreachable?
  - Pipeline logs the error, skips the URL, and continues processing remaining URLs
- What happens when Qdrant Cloud is temporarily unavailable?
  - Pipeline implements retry logic with exponential backoff; after max retries, fails gracefully with clear error message
- What happens when Cohere API rate limits are hit?
  - Pipeline implements rate limiting and batch processing to stay within API limits
- What happens when a page has no meaningful text content (e.g., only images)?
  - Pipeline logs a warning and skips pages with insufficient text content (below minimum threshold)
- What happens when the same URL is provided multiple times in the input list?
  - Pipeline deduplicates URLs before processing

## Requirements *(mandatory)*

### Functional Requirements

**URL Extraction & Crawling**

- **FR-001**: System MUST accept a list of Docusaurus website URLs as input
- **FR-002**: System MUST fetch and parse HTML content from each provided URL
- **FR-003**: System MUST extract clean text content, removing navigation, headers, footers, and other non-content elements
- **FR-004**: System MUST extract the page title from each URL for metadata
- **FR-005**: System MUST handle HTTP errors gracefully, logging failures and continuing with remaining URLs

**Content Chunking**

- **FR-006**: System MUST split extracted text into chunks suitable for semantic retrieval
- **FR-007**: System MUST apply overlap between consecutive chunks to preserve context at chunk boundaries
- **FR-008**: System MUST track chunk index/position within each source document
- **FR-009**: System MUST maintain a configurable chunk size (default: 500 tokens) and overlap (default: 50 tokens)

**Embedding Generation**

- **FR-010**: System MUST generate vector embeddings using Cohere embedding models
- **FR-011**: System MUST produce embeddings with consistent dimensionality across all chunks
- **FR-012**: System MUST batch embedding requests to optimize API usage and respect rate limits
- **FR-013**: System MUST handle Cohere API errors with appropriate retry logic

**Vector Storage**

- **FR-014**: System MUST store embeddings in Qdrant Cloud (Free Tier)
- **FR-015**: System MUST store metadata with each vector: source URL, page title, chunk index, and text content
- **FR-016**: System MUST create or use an existing Qdrant collection with appropriate vector configuration
- **FR-017**: System MUST support idempotent upsert operations for safe re-runs

**Verification**

- **FR-018**: System MUST provide a verification script that reports the number of chunks stored
- **FR-019**: System MUST verify successful insertion by counting records in Qdrant
- **FR-020**: System MUST demonstrate similarity search capability with a test query

**Configuration**

- **FR-021**: System MUST read API credentials from environment variables (COHERE_API_KEY, QDRANT_URL, QDRANT_API_KEY)
- **FR-022**: System MUST provide configurable options for chunk size, overlap, and collection name

### Key Entities

- **SourceURL**: A deployed Docusaurus page URL to be ingested; contains the location of book content
- **PageContent**: Extracted text and metadata from a single URL; includes title, clean text, and source reference
- **TextChunk**: A segment of page content sized for embedding; includes text, chunk index, and parent page reference
- **VectorRecord**: An embedding stored in Qdrant; contains vector, source URL, page title, chunk index, and text content
- **IngestionRun**: A single execution of the pipeline; tracks URLs processed, chunks created, and any errors

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Pipeline successfully processes 100% of reachable URLs from the provided list without crashing
- **SC-002**: All ingested pages result in at least one chunk stored in the vector database
- **SC-003**: Verification script confirms all chunks are retrievable via similarity search within 5 seconds
- **SC-004**: Re-running the pipeline on unchanged content completes without creating duplicate records
- **SC-005**: Pipeline execution time scales linearly with the number of URLs (no exponential slowdown)
- **SC-006**: All stored records contain complete metadata (source URL, page title, chunk index, text content)
- **SC-007**: Similarity search returns semantically relevant results for test queries related to book topics

## Assumptions

- The Docusaurus website is publicly accessible without authentication
- Cohere embedding model produces vectors of 1024 dimensions (embed-english-v3.0 or equivalent)
- Qdrant Cloud Free Tier provides sufficient storage for the book content (typically thousands of chunks)
- Book content is primarily in English
- Default chunk size of 500 tokens with 50-token overlap is suitable for RAG retrieval (configurable if needed)
- The deployed website structure follows standard Docusaurus patterns for content extraction

## Out of Scope

- Query-time retrieval or ranking logic
- AI agent or LLM interaction for answering questions
- Frontend UI or user experience
- Authentication or access control
- Fine-tuning of embedding models
- Real-time content synchronization (manual re-run required for updates)
- Multi-language support beyond English

## Dependencies

- **External Services**:
  - Cohere API for embedding generation
  - Qdrant Cloud for vector storage
  - Deployed Docusaurus website (GitHub Pages)

- **Python Libraries** (to be determined during planning):
  - HTTP client for web requests
  - HTML parsing library
  - Cohere SDK
  - Qdrant client library
