# Quickstart: Retrieval Testing Pipeline

**Feature**: 002-retrieval-testing
**Date**: 2025-12-20

## Prerequisites

- Completed 001-rag-ingestion-pipeline (collection populated)
- Existing backend/ folder with uv setup
- Same .env file with API credentials

## Setup

### 1. Add Typer Dependency

```bash
cd backend
uv add typer
```

### 2. Verify .env

Ensure .env has the required variables:

```env
COHERE_API_KEY=your-cohere-api-key
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your-qdrant-api-key
```

### 3. Create test_retrieval.py

Create `test_retrieval.py` in the backend folder with CLI commands.

## Usage

### Single Query

```bash
uv run test_retrieval.py query "What is physical AI?"
```

### Run Test Suite

```bash
uv run test_retrieval.py test
```

### Interactive Mode

```bash
uv run test_retrieval.py interactive
```

### Options

```bash
# More results
uv run test_retrieval.py query "robots" --top-k 10

# Show help
uv run test_retrieval.py --help
```

## Expected Output

```
Query: "What is physical AI?"
═══════════════════════════════════════════════════════════════

[1] Score: 0.89
    Title: Introduction to Physical AI
    URL: https://example.com/docs/intro
    Chunk: 0
    ───────────────────────────────────────────────────────────
    Physical AI refers to artificial intelligence systems...

[2] Score: 0.76
    Title: Embodied Intelligence
    ...
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Collection not found" | Run ingestion first (main.py) |
| "COHERE_API_KEY not set" | Check .env file |
| No results | Try broader query terms |
| Low scores on all results | Content may not match query topic |

## Test Queries

The test suite includes queries like:
1. "What is physical AI?"
2. "How do humanoid robots balance?"
3. "What sensors are used in robotics?"
4. "Explain reinforcement learning for robots"
5. "What are the challenges of bipedal locomotion?"

Customize these based on actual book content.
