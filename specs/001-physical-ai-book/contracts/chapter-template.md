# Chapter Template

**Purpose**: Standardized structure for all book chapters
**Version**: 1.0.0
**Applies to**: All 24 chapters across 4 modules

---

## Frontmatter (Required)

```yaml
---
sidebar_position: {1-6}
title: "{Chapter Title}"
description: "{One-sentence description for SEO, max 160 characters}"
keywords: [{keyword1}, {keyword2}, {keyword3}]
---
```

---

## Chapter Structure

Copy and fill this template for each chapter:

```markdown
# {Chapter Title}

**Prerequisites**: {List prior chapters or "None"}
**Learning Objectives**: By the end of this chapter, you will be able to:
- {Objective 1}
- {Objective 2}
- {Objective 3}

## Concept Overview

{Define the topic and its role in the Physical AI pipeline. State what problem this solves and why it matters for humanoid robotics.}

{~100 words}

## System Architecture

{Describe the component relationships. Explain how this topic fits within the broader system. Include architecture diagram reference if applicable.}

{~150 words}

## Data Flow and Components

{Explain inputs, outputs, and transformations. Identify key interfaces and data structures. Describe the flow from input to output.}

{~150 words}

## Example Workflow

{Provide a concrete, reproducible example. Include code snippets with version specifications. Walk through the example step by step.}

```{language}
# {Framework} {Version} | {Language} {Version} | {Package} {Version}
{code}
```

{~200 words including code}

## Common Failure Modes

{Document known issues and their mitigations. Reference troubleshooting resources where applicable.}

| Failure Mode | Symptoms | Mitigation |
|--------------|----------|------------|
| {Issue 1} | {How it manifests} | {How to fix/prevent} |
| {Issue 2} | {How it manifests} | {How to fix/prevent} |

{~100 words}

## Summary

{Recap the key points covered in this chapter. Link to the next chapter and note any advanced topics for further reading.}

**Next**: [{Next Chapter Title}](./{next-chapter-slug})

{~50 words}

---

## References

{List all citations used in this chapter in APA format}

1. {Citation 1}
2. {Citation 2}
```

---

## Word Count Guidelines

| Section | Target | Tolerance |
|---------|--------|-----------|
| Concept Overview | 100 | ±20 |
| System Architecture | 150 | ±30 |
| Data Flow | 150 | ±30 |
| Example Workflow | 200 | ±40 |
| Failure Modes | 100 | ±20 |
| Summary | 50 | ±10 |
| **Total** | **750** | **500-800** |

---

## Code Block Requirements

Every code example MUST include:

1. **Version header** as first line comment:
   ```python
   # ROS 2 Humble | Python 3.10 | rclpy 3.3.x
   ```

2. **Language specifier** for syntax highlighting:
   ```python
   ```python
   ```

3. **Complete imports** - no assumed context:
   ```python
   import rclpy
   from rclpy.node import Node  # Explicit imports
   ```

4. **Runnable or traceable** - either executable as-is or clearly marked as pseudocode

---

## Citation Requirements

Every chapter MUST have at least one citation. Format per APA 7th edition:

**Documentation**:
```
Open Robotics. (2023). ROS 2 Humble documentation. https://docs.ros.org/en/humble/ (accessed 2025-12-18)
```

**Academic**:
```
Quigley, M., Conley, K., Gerkey, B., et al. (2009). ROS: an open-source Robot Operating System. *ICRA Workshop on Open Source Software*.
```

**Inline**:
```markdown
The Data Distribution Service (DDS) provides the middleware layer (Open Robotics, 2023).
```

---

## Checklist Before Submission

- [ ] Frontmatter complete with sidebar_position, title, description, keywords
- [ ] All 6 sections present in order
- [ ] Word count within 500-800 range
- [ ] At least one citation in References section
- [ ] All code examples have version headers
- [ ] All technical terms defined on first use
- [ ] All acronyms expanded on first use
- [ ] Links to previous/next chapters work
- [ ] Docusaurus build passes
