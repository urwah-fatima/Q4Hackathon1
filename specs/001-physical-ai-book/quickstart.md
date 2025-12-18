# Quickstart Guide: Physical AI & Humanoid Robotics Book Authoring

**Feature Branch**: `001-physical-ai-book`
**Date**: 2025-12-18
**Purpose**: Author workflow for creating book chapters

---

## Overview

This guide walks you through the process of authoring a chapter for the Physical AI & Humanoid Robotics technical book. Each chapter follows a standardized structure to ensure consistency, accuracy, and reproducibility.

---

## Prerequisites

Before starting chapter authoring:

1. **Review Documents**:
   - [ ] Read `constitution.md` (quality standards)
   - [ ] Read `spec.md` (feature requirements)
   - [ ] Read `plan.md` (chapter matrix and structure)
   - [ ] Review `contracts/chapter-template.md`
   - [ ] Review `contracts/citation-guide.md`
   - [ ] Review `contracts/section-schema.md`

2. **Environment Setup**:
   - [ ] Node.js 18+ installed
   - [ ] Docusaurus development server running
   - [ ] Word count tool available (`wc -w` or editor plugin)

3. **Context Access**:
   - [ ] MCP documentation server available (if applicable)
   - [ ] Vendor documentation bookmarked (ROS 2, NVIDIA, Gazebo, Unity)

---

## Authoring Workflow

### Step 1: Select Chapter

Choose a chapter from the `plan.md` Module-Chapter Matrix:

```bash
# Check plan for available chapters
cat specs/001-physical-ai-book/plan.md | grep "| Module"
```

Chapters should be authored in order within each module to maintain narrative flow.

### Step 2: Create Chapter File

Create the chapter file in the appropriate module directory:

```bash
# Example: Module 1, Chapter 1
touch docs/module-1-ros2/01-ros2-architecture.md
```

### Step 3: Add Frontmatter

Start with required Docusaurus frontmatter:

```yaml
---
sidebar_position: 1
title: "ROS 2 Architecture and DDS Communication"
description: "Understanding ROS 2's middleware architecture and Data Distribution Service for humanoid robotics"
keywords: [ROS 2, DDS, middleware, robotics, communication]
---
```

### Step 4: Research Phase

**Follow source hierarchy** (per Constitution):

1. **Query MCP documentation** (if available)
   - Check for topic-specific guidance
   - Note any MCP-provided examples

2. **Consult vendor documentation**
   - ROS 2: https://docs.ros.org/en/humble/
   - NVIDIA Isaac: https://docs.omniverse.nvidia.com/isaacsim/
   - Gazebo: https://gazebosim.org/docs/fortress/
   - Unity ROS: https://github.com/Unity-Technologies/ROS-TCP-Connector

3. **Reference academic sources**
   - Search IEEE Xplore, ACM Digital Library
   - Check arXiv for relevant papers

4. **Document sources** in a local notes file:
   ```markdown
   ## Sources for Chapter 1.1
   - [ ] MCP: (pending query)
   - [x] ROS 2 Docs: About-Nodes.html
   - [x] Macenski et al., 2022 - Science Robotics
   ```

### Step 5: Draft Sections

Write each section following the schema (`contracts/section-schema.md`):

| Order | Section | Action |
|-------|---------|--------|
| 1 | Concept Overview | Define topic, state objectives (~100 words) |
| 2 | System Architecture | Describe components (~150 words) |
| 3 | Data Flow | Document I/O and interfaces (~150 words) |
| 4 | Example Workflow | Provide code example (~200 words) |
| 5 | Failure Modes | List issues and mitigations (~100 words) |
| 6 | Summary | Recap and link forward (~50 words) |

**Code Example Requirements**:
```python
# ROS 2 Humble | Python 3.10 | rclpy 3.3.x
import rclpy
from rclpy.node import Node

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        # ... implementation
```

### Step 6: Add Citations

Insert inline citations and build References section:

**Inline**:
```markdown
ROS 2 uses the Data Distribution Service (DDS) as its communication middleware (Open Robotics, 2023).
```

**References Section**:
```markdown
## References

1. Macenski, S., et al. (2022). Robot Operating System 2: Design, architecture, and uses in the wild. *Science Robotics*, 7(66).

2. Open Robotics. (2023). ROS 2 Humble documentation. https://docs.ros.org/en/humble/ (accessed 2025-12-18)
```

### Step 7: Validate

Run validation checks:

```bash
# Word count (should be 500-800)
wc -w docs/module-1-ros2/01-ros2-architecture.md

# Docusaurus build (should pass)
npm run build

# Check for broken links (built into Docusaurus)
# Review build output for warnings
```

### Step 8: Self-Review Checklist

Before marking chapter complete:

- [ ] Word count: 500-800 words
- [ ] All 6 sections present in order
- [ ] At least 1 citation in References
- [ ] All code has version headers
- [ ] All technical terms defined on first use
- [ ] All acronyms expanded on first use
- [ ] Link to next chapter works
- [ ] Docusaurus build passes
- [ ] No [REQUIRES VERIFICATION] markers remain

---

## Quick Reference

### File Naming Convention

```
docs/module-{N}-{slug}/{NN}-{chapter-slug}.md
```

Examples:
- `docs/module-1-ros2/01-ros2-architecture.md`
- `docs/module-2-simulation/03-urdf-sdf-usage.md`

### Word Count Targets

| Section | Words |
|---------|-------|
| Concept Overview | 100 |
| System Architecture | 150 |
| Data Flow | 150 |
| Example Workflow | 200 |
| Failure Modes | 100 |
| Summary | 50 |
| **Total** | **750** |

### Version Targets

| Technology | Version |
|------------|---------|
| ROS 2 | Humble |
| Python | 3.10+ |
| Gazebo | Fortress |
| Isaac Sim | 2023.1.x |
| Docusaurus | 3.x |

---

## Common Issues

| Issue | Solution |
|-------|----------|
| Word count too high | Split into two chapters or trim Example Workflow |
| Word count too low | Expand Failure Modes or add second code example |
| Build fails on link | Check relative path: `./next-chapter-slug` |
| Missing citations | Every technical claim needs at least one source |
| Code block errors | Verify language specifier and syntax |

---

## Support

- **Constitution questions**: See `.specify/memory/constitution.md`
- **Template questions**: See `contracts/chapter-template.md`
- **Citation questions**: See `contracts/citation-guide.md`
- **Section questions**: See `contracts/section-schema.md`

---

## Next Steps

After completing a chapter:

1. Run final validation
2. Commit with descriptive message
3. Move to next chapter in sequence
4. Update progress in project tracking
