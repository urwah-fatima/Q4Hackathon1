# Data Model: Physical AI & Humanoid Robotics Technical Book

**Feature Branch**: `001-physical-ai-book`
**Date**: 2025-12-18
**Status**: Complete

## Overview

This document defines the content schema for the technical book. Since this is a documentation/authoring project (not a database application), the "data model" describes content entities, their attributes, and relationships.

---

## Entity Definitions

### 1. Book

The top-level container for all content.

| Attribute | Type | Constraints | Description |
|-----------|------|-------------|-------------|
| title | string | Required | "Physical AI & Humanoid Robotics" |
| modules | Module[] | Exactly 4 | Ordered list of modules |
| introduction | Chapter | Required | Book introduction page |
| references | Bibliography | Required | Consolidated reference list |
| version | semver | Required | Content version (e.g., 1.0.0) |

**Relationships**:
- Book → contains → Module (1:4)
- Book → contains → Bibliography (1:1)

---

### 2. Module

A major thematic section containing related chapters.

| Attribute | Type | Constraints | Description |
|-----------|------|-------------|-------------|
| id | integer | 1-4 | Module number |
| title | string | Required | Human-readable title |
| slug | string | kebab-case | URL-safe identifier |
| description | string | Required | Module overview (1-2 sentences) |
| prerequisites | string[] | Optional | Required prior knowledge |
| learning_objectives | string[] | 3-5 items | What readers will learn |
| chapters | Chapter[] | 5-6 | Ordered list of chapters |

**Relationships**:
- Module → contains → Chapter (1:5-6)
- Module → depends_on → Module (optional, DAG)

**Module Instances**:

| ID | Title | Slug | Prerequisites |
|----|-------|------|---------------|
| 1 | The Robotic Nervous System (ROS 2) | module-1-ros2 | Python, Linux basics |
| 2 | The Digital Twin (Gazebo & Unity) | module-2-simulation | Module 1 |
| 3 | The AI-Robot Brain (NVIDIA Isaac) | module-3-isaac | Module 1, Module 2 |
| 4 | Vision-Language-Action (VLA) | module-4-vla | Module 1, Module 2, Module 3 |

---

### 3. Chapter

A standalone unit of content covering a specific topic.

| Attribute | Type | Constraints | Description |
|-----------|------|-------------|-------------|
| id | string | MM-CC format | Module-Chapter identifier (e.g., "01-01") |
| title | string | Required | Chapter title |
| slug | string | kebab-case | Filename without extension |
| word_count | integer | 500-800 | Total word count |
| sections | Section[] | Exactly 6 | Ordered section list |
| code_examples | CodeExample[] | 0+ | Code snippets |
| citations | Citation[] | 1+ | At least one citation |
| prerequisites | string[] | Optional | Required prior chapters |
| sidebar_position | integer | Required | Docusaurus ordering |

**Relationships**:
- Chapter → contains → Section (1:6)
- Chapter → contains → CodeExample (1:*)
- Chapter → references → Citation (1:*)
- Chapter → depends_on → Chapter (optional, DAG)

**Validation Rules**:
- `word_count` MUST be between 500 and 800 inclusive
- `citations` MUST have at least one entry
- `sections` MUST have exactly 6 entries in prescribed order

---

### 4. Section

A structural division within a chapter.

| Attribute | Type | Constraints | Description |
|-----------|------|-------------|-------------|
| order | integer | 1-6 | Section position |
| type | SectionType | enum | Prescribed section type |
| heading | string | Required | Section heading (H2) |
| content | markdown | Required | Section body text |
| word_target | integer | Varies | Target word count |

**SectionType Enum**:

| Order | Type | Heading | Word Target |
|-------|------|---------|-------------|
| 1 | concept_overview | Concept Overview | ~100 |
| 2 | system_architecture | System Architecture | ~150 |
| 3 | data_flow | Data Flow and Components | ~150 |
| 4 | example_workflow | Example Workflow | ~200 |
| 5 | failure_modes | Common Failure Modes | ~100 |
| 6 | summary | Summary | ~50 |

**Validation Rules**:
- Sections MUST appear in order 1-6
- Each section type MUST appear exactly once per chapter
- Total word targets sum to 750 (within 500-800 range)

---

### 5. CodeExample

An executable or illustrative code snippet.

| Attribute | Type | Constraints | Description |
|-----------|------|-------------|-------------|
| id | string | Unique per chapter | Code block identifier |
| language | string | Required | Syntax highlighting hint |
| version_header | string | Required | Dependency versions |
| source | string | Required | Code content |
| caption | string | Optional | Explanatory text |
| source_url | string | Optional | Origin URL if adapted |

**Version Header Format**:
```
# {Framework} {Version} | {Language} {Version} | {Package} {Version}
```

**Example**:
```python
# ROS 2 Humble | Python 3.10 | rclpy 3.3.x
import rclpy
```

**Validation Rules**:
- `version_header` MUST specify at least framework and language versions
- `language` MUST be a valid Docusaurus code block language

---

### 6. Citation

A reference to an authoritative source.

| Attribute | Type | Constraints | Description |
|-----------|------|-------------|-------------|
| id | string | Unique | Citation key |
| type | SourceType | enum | Source category |
| authors | string[] | Optional | Author list |
| title | string | Required | Source title |
| year | integer | Required | Publication year |
| url | string | Optional | Web URL |
| accessed | date | Required if URL | Access date |
| publication | string | Optional | Journal/conference name |
| doi | string | Optional | Digital Object Identifier |

**SourceType Enum** (per Constitution hierarchy):

| Priority | Type | Description |
|----------|------|-------------|
| 1 | mcp_documentation | MCP-provided Docusaurus docs |
| 2 | vendor_documentation | Official vendor docs |
| 3 | peer_reviewed | IEEE, ACM, arXiv with review |
| 4 | industry_whitepaper | Technical reports |
| 5 | technical_standard | ISO, IEC, ROS REPs |

**APA Format Output**:
- Documentation: Organization. (Year). *Title*. URL (accessed Date)
- Academic: Author, A. A., & Author, B. B. (Year). Title. *Publication*, Volume(Issue), Pages. DOI

---

### 7. Bibliography

Consolidated reference list for the entire book.

| Attribute | Type | Constraints | Description |
|-----------|------|-------------|-------------|
| citations | Citation[] | Required | All unique citations |
| grouped_by | GroupingType | Optional | Organization method |

**GroupingType Enum**:
- `source_type`: Group by SourceType priority
- `module`: Group by originating module
- `alphabetical`: A-Z by first author/organization

---

## Entity Relationship Diagram

```text
┌─────────────────────────────────────────────────────────────────┐
│                           BOOK                                  │
│  title, version                                                 │
├───────────────┬─────────────────────────────────────────────────┤
│               │                                                 │
│    ┌──────────▼──────────┐                    ┌───────────────┐ │
│    │      MODULE         │                    │  BIBLIOGRAPHY │ │
│    │  id, title, slug    │                    │  citations[]  │ │
│    │  prerequisites[]    │                    └───────────────┘ │
│    │  learning_obj[]     │                                      │
│    └──────────┬──────────┘                                      │
│               │ 1:5-6                                           │
│    ┌──────────▼──────────┐                                      │
│    │      CHAPTER        │                                      │
│    │  id, title, slug    │                                      │
│    │  word_count         │                                      │
│    │  sidebar_position   │                                      │
│    └──┬───────┬───────┬──┘                                      │
│       │       │       │                                         │
│       │1:6    │1:*    │1:*                                      │
│   ┌───▼───┐ ┌─▼─────┐ ┌▼────────┐                               │
│   │SECTION│ │CODE   │ │CITATION │                               │
│   │order  │ │EXAMPLE│ │id, type │                               │
│   │type   │ │lang   │ │authors  │                               │
│   │content│ │version│ │title    │                               │
│   └───────┘ │source │ │year     │                               │
│             └───────┘ └─────────┘                               │
└─────────────────────────────────────────────────────────────────┘
```

---

## File System Mapping

| Entity | File Location | Format |
|--------|---------------|--------|
| Book | `docs/` directory | Directory structure |
| Module | `docs/module-N-slug/` | Directory with `_category_.json` |
| Chapter | `docs/module-N-slug/NN-slug.md` | Markdown file |
| Section | Within chapter file | H2 headings |
| CodeExample | Within chapter file | Fenced code blocks |
| Citation | Inline + `docs/references.md` | APA format text |
| Bibliography | `docs/references.md` | Markdown file |

---

## Docusaurus Frontmatter Schema

Each chapter Markdown file includes:

```yaml
---
sidebar_position: 1
title: "Chapter Title"
description: "Brief chapter description for SEO"
keywords: [keyword1, keyword2, keyword3]
---
```

---

## Validation Checklist

- [ ] Each module has 5-6 chapters
- [ ] Each chapter has 500-800 words
- [ ] Each chapter has exactly 6 sections in order
- [ ] Each chapter has at least 1 citation
- [ ] All code examples have version headers
- [ ] Module dependencies form a DAG (no cycles)
- [ ] All citations use APA 7th edition format
