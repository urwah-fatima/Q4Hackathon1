---
id: 002
title: Retrieval CLI Implementation Plan
stage: plan
date: 2025-12-20
surface: agent
model: claude-opus-4-5-20251101
feature: 002-retrieval-testing
branch: 002-retrieval-testing
user: developer
command: /sp.plan
labels: ["typer", "cli", "retrieval", "testing", "qdrant", "cohere"]
links:
  spec: specs/002-retrieval-testing/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-retrieval-testing/plan.md
  - specs/002-retrieval-testing/research.md
  - specs/002-retrieval-testing/data-model.md
  - specs/002-retrieval-testing/quickstart.md
tests:
  - Constitution check passed (6/6 principles)
---

## Prompt

Retrieval testing script using existing Qdrant collection and Cohere embeddings
- Continue in the existing uv-managed backend project; add dependencies if needed: uv add typer (for nice CLI)
- Create test_retrieval.py: CLI script with command to query (e.g., uv run test_retrieval.py "What is speculative execution?")
- Query flow: Embed input query with Cohere (input_type="search_query") → search Qdrant collection (top_k=5) → print results with score, text preview, source URL, metadata
- Include 5+ predefined test queries from different parts of the book; also support interactive mode
- Success: All test queries return relevant chunks from correct pages; verified manually against book content

## Response snapshot

Created implementation plan for retrieval testing CLI with:

**Architecture**:
- Single new file: `test_retrieval.py` in existing backend/
- Typer CLI with 3 commands: query, test, interactive
- Embeds queries with Cohere (input_type="search_query")
- Searches existing Qdrant collection (book_chatbot_embedding)
- Pretty-printed output with scores and metadata

**CLI Commands**:
- `uv run test_retrieval.py query "..."` - Single query
- `uv run test_retrieval.py test` - Run predefined suite
- `uv run test_retrieval.py interactive` - REPL mode

**Options**: --top-k (default 5), --threshold (default 0.5)

**Predefined Queries**: 6 queries covering physical AI, robotics, sensors, RL, locomotion

Constitution check: 6/6 principles passed.

## Outcome

- ✅ Impact: Complete plan for retrieval testing CLI to verify indexing quality
- 🧪 Tests: Constitution check (6/6)
- 📁 Files: plan.md, research.md, data-model.md, quickstart.md
- 🔁 Next prompts: /sp.tasks to generate implementation tasks
- 🧠 Reflection: Simple extension of existing backend - just one new file and one new dependency (typer).

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Constitution PASS (6/6)
- Prompt variant (if applicable): User-specified typer CLI with detailed query flow
- Next experiment (smallest change to try): N/A - plan complete
