# Implementation Plan: Retrieval Testing Pipeline

**Branch**: `002-retrieval-testing` | **Date**: 2025-12-20 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-retrieval-testing/spec.md`

## Summary

Create a CLI script (`test_retrieval.py`) using Typer that allows developers to test semantic search against the indexed book content in Qdrant. The script embeds queries with Cohere (input_type="search_query"), searches the existing collection, and displays results with scores, text, URLs, and metadata. Includes predefined test queries and interactive mode.

## Technical Context

**Language/Version**: Python 3.11
**Package Manager**: uv (existing project)
**Primary Dependencies**: typer (new), cohere, qdrant-client, python-dotenv (existing)
**Storage**: Qdrant Cloud - collection `book_chatbot_embedding` (existing)
**Testing**: Manual verification of retrieved results
**Target Platform**: Local development (cross-platform)
**Project Type**: Single CLI script (extends existing backend/)
**Performance Goals**: Execute 5+ queries in under 30 seconds
**Constraints**: Use same Cohere model and Qdrant collection as ingestion
**Scale/Scope**: Developer testing tool, not production service

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-checked after Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. Accuracy First | PASS | Uses same embedding model as ingestion for consistency |
| II. Context Primacy | PASS | Queries indexed book content as source of truth |
| III. Technical Rigor | PASS | Uses official Cohere and Qdrant SDKs |
| IV. Clarity | PASS | CLI with clear commands and formatted output |
| V. Reproducibility | PASS | Same environment as ingestion script |
| VI. Modularity | PASS | Separate script, reuses existing configuration |

## Project Structure

### Documentation (this feature)

```text
specs/002-retrieval-testing/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Technology decisions
├── data-model.md        # Entity definitions
├── quickstart.md        # Usage guide
└── tasks.md             # Implementation tasks (/sp.tasks)
```

### Source Code (extends existing backend/)

```text
backend/
├── .venv/               # Existing uv environment
├── .env                 # Existing API credentials
├── main.py              # Existing ingestion script
├── test_retrieval.py    # NEW: Retrieval testing CLI
├── pyproject.toml       # Add typer dependency
└── uv.lock              # Updated lockfile
```

**Structure Decision**: Single new file `test_retrieval.py` added to existing backend project. No new folders or restructuring needed.

## Architecture

### Query Flow

```
1. User runs: uv run test_retrieval.py query "What is physical AI?"
              │
              ▼
2. embed_query(text)
   └─→ Cohere API (embed-english-v3.0, input_type="search_query")
   └─→ Returns: 1024-dim query vector
              │
              ▼
3. search_qdrant(query_vector, top_k=5)
   └─→ Qdrant search on book_chatbot_embedding
   └─→ Returns: List of (score, payload) tuples
              │
              ▼
4. format_results(results)
   └─→ Pretty-printed terminal output with:
       - Rank and similarity score
       - Page title and URL
       - Chunk index
       - Text preview
       - Low relevance warning if score < 0.5
```

### CLI Commands

| Command | Description | Example |
|---------|-------------|---------|
| `query` | Single query search | `uv run test_retrieval.py query "What is AI?"` |
| `test` | Run predefined test suite | `uv run test_retrieval.py test` |
| `interactive` | Enter REPL mode | `uv run test_retrieval.py interactive` |

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `--top-k` | 5 | Number of results to return |
| `--threshold` | 0.5 | Low relevance warning threshold |

## Key Implementation Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| CLI Framework | Typer | User requirement; modern, type-hinted |
| Query Embedding | input_type="search_query" | Cohere recommends for queries (vs search_document) |
| Result Count | top_k=5 | User requirement; more than spec's top-3 default |
| Output Format | Rich tables via Typer | Built-in, readable terminal output |
| Error Handling | Try/except with messages | Graceful failures with helpful hints |

## Setup Commands

```bash
# Add typer dependency
cd backend
uv add typer

# Verify existing .env has credentials
cat .env

# Run test retrieval
uv run test_retrieval.py query "What is physical AI?"
uv run test_retrieval.py test
uv run test_retrieval.py interactive
```

## Predefined Test Queries

Based on Physical AI & Humanoid Robotics book topics:

1. "What is physical AI?"
2. "How do humanoid robots maintain balance?"
3. "What sensors are commonly used in robotics?"
4. "Explain reinforcement learning for robot control"
5. "What are the challenges of bipedal locomotion?"
6. "How does computer vision help robots navigate?"

*Note: Customize queries after reviewing actual book content.*

## Success Criteria

- [ ] `uv run test_retrieval.py query "..."` returns relevant results
- [ ] `uv run test_retrieval.py test` executes all predefined queries
- [ ] `uv run test_retrieval.py interactive` allows continuous querying
- [ ] Results display score, text, URL, title, chunk_index
- [ ] Low scores trigger warning message
- [ ] Errors handled gracefully with helpful messages

## Generated Artifacts

| Artifact | Path | Status |
|----------|------|--------|
| Research Document | specs/002-retrieval-testing/research.md | Complete |
| Data Model | specs/002-retrieval-testing/data-model.md | Complete |
| Quickstart Guide | specs/002-retrieval-testing/quickstart.md | Complete |

## Next Steps

1. Run `/sp.tasks` to generate implementation tasks
2. Add typer dependency: `uv add typer`
3. Implement test_retrieval.py with CLI commands
4. Test with actual book content queries
5. Verify results match expected book sections
