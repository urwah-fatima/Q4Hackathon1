# Section Schema

**Purpose**: Define the 6-section structure required for every chapter
**Version**: 1.0.0
**Enforcement**: Mandatory - all chapters must conform

---

## Section Overview

Every chapter MUST contain exactly 6 sections in this order:

| Order | Section ID | Heading | Word Target | Purpose |
|-------|------------|---------|-------------|---------|
| 1 | concept_overview | Concept Overview | ~100 | Define topic and context |
| 2 | system_architecture | System Architecture | ~150 | Describe components |
| 3 | data_flow | Data Flow and Components | ~150 | Explain interfaces |
| 4 | example_workflow | Example Workflow | ~200 | Provide reproducible example |
| 5 | failure_modes | Common Failure Modes | ~100 | Document issues |
| 6 | summary | Summary | ~50 | Recap and link forward |

**Total**: ~750 words (within 500-800 range)

---

## Section 1: Concept Overview

**Heading**: `## Concept Overview`
**Word Target**: ~100 words (80-120)
**Purpose**: Orient the reader to the topic

**Required Content**:
- Definition of the concept being covered
- Role in the Physical AI pipeline
- Problem this topic solves
- Why it matters for humanoid robotics

**Template**:
```markdown
## Concept Overview

{Topic} is {definition}. In the context of Physical AI for humanoid robotics, it serves as {role in pipeline}.

The primary challenge that {topic} addresses is {problem statement}. Without {topic}, {consequence of absence}.

**Learning Objectives**:
- {Objective 1}
- {Objective 2}
- {Objective 3}
```

**Quality Criteria**:
- [ ] Concept clearly defined
- [ ] Connection to Physical AI pipeline stated
- [ ] Learning objectives measurable

---

## Section 2: System Architecture

**Heading**: `## System Architecture`
**Word Target**: ~150 words (120-180)
**Purpose**: Describe component relationships

**Required Content**:
- Key components involved
- How components relate to each other
- Where this topic fits in the broader system
- Architecture diagram reference (if applicable)

**Template**:
```markdown
## System Architecture

The {topic} architecture consists of {N} primary components:

1. **{Component 1}**: {role and responsibility}
2. **{Component 2}**: {role and responsibility}
3. **{Component 3}**: {role and responsibility}

These components interact through {interaction pattern}. The {topic} layer sits between {upstream component} and {downstream component} in the overall Physical AI stack.

{Optional: See Figure X for the architecture diagram.}
```

**Quality Criteria**:
- [ ] All key components identified
- [ ] Relationships clearly described
- [ ] Position in overall system stated
- [ ] Diagram referenced if complex

---

## Section 3: Data Flow and Components

**Heading**: `## Data Flow and Components`
**Word Target**: ~150 words (120-180)
**Purpose**: Explain inputs, outputs, and transformations

**Required Content**:
- Input data types and sources
- Processing/transformation steps
- Output data types and destinations
- Key interfaces and protocols

**Template**:
```markdown
## Data Flow and Components

**Inputs**:
- {Input 1}: {type, source, format}
- {Input 2}: {type, source, format}

**Processing**:
1. {Step 1}: {transformation description}
2. {Step 2}: {transformation description}
3. {Step 3}: {transformation description}

**Outputs**:
- {Output 1}: {type, destination, format}
- {Output 2}: {type, destination, format}

**Key Interfaces**:
- {Interface 1}: {protocol, data format}
- {Interface 2}: {protocol, data format}
```

**Quality Criteria**:
- [ ] All inputs documented
- [ ] All outputs documented
- [ ] Transformations explained
- [ ] Interfaces identified

---

## Section 4: Example Workflow

**Heading**: `## Example Workflow`
**Word Target**: ~200 words (160-240)
**Purpose**: Provide concrete, reproducible example

**Required Content**:
- Step-by-step walkthrough
- Code snippet(s) with version headers
- Expected output or behavior
- Prerequisites for running the example

**Template**:
```markdown
## Example Workflow

The following example demonstrates {what the example shows}.

**Prerequisites**: {required setup, installed packages}

**Step 1**: {description}

```{language}
# {Framework} {Version} | {Language} {Version} | {Package} {Version}
{code for step 1}
```

**Step 2**: {description}

```{language}
# {Framework} {Version} | {Language} {Version} | {Package} {Version}
{code for step 2}
```

**Expected Output**:
```
{expected terminal output or behavior description}
```

This example illustrates {key concept demonstrated}.
```

**Quality Criteria**:
- [ ] Example is reproducible
- [ ] All code has version headers
- [ ] Prerequisites stated
- [ ] Expected output documented

---

## Section 5: Common Failure Modes

**Heading**: `## Common Failure Modes`
**Word Target**: ~100 words (80-120)
**Purpose**: Document known issues and mitigations

**Required Content**:
- Common errors or failures
- Symptoms of each failure
- Mitigation or resolution steps
- Reference to troubleshooting resources

**Template**:
```markdown
## Common Failure Modes

| Failure Mode | Symptoms | Mitigation |
|--------------|----------|------------|
| {Issue 1} | {observable symptoms} | {resolution steps} |
| {Issue 2} | {observable symptoms} | {resolution steps} |
| {Issue 3} | {observable symptoms} | {resolution steps} |

**Troubleshooting Resources**:
- {Resource 1}: {URL or reference}
- {Resource 2}: {URL or reference}
```

**Quality Criteria**:
- [ ] At least 2 failure modes documented
- [ ] Symptoms are observable/testable
- [ ] Mitigations are actionable
- [ ] Resources referenced

---

## Section 6: Summary

**Heading**: `## Summary`
**Word Target**: ~50 words (40-60)
**Purpose**: Recap and guide reader forward

**Required Content**:
- Key takeaways (2-3 points)
- Link to next chapter
- Optional: advanced topics for further reading

**Template**:
```markdown
## Summary

This chapter covered {topic}, focusing on:
- {Key takeaway 1}
- {Key takeaway 2}
- {Key takeaway 3}

**Next**: [{Next Chapter Title}](./{next-chapter-slug}) explores {brief preview of next topic}.

**Further Reading**: {Optional advanced resources}
```

**Quality Criteria**:
- [ ] 2-3 key takeaways listed
- [ ] Link to next chapter works
- [ ] Summary is concise (no new information)

---

## Validation Rules

### Structural Validation
1. All 6 sections MUST be present
2. Sections MUST appear in order 1-6
3. Section headings MUST match exactly (case-sensitive)
4. No additional H2 sections allowed (except References)

### Content Validation
1. Total word count: 500-800 words
2. Each section within word tolerance
3. At least one code example in Section 4
4. At least 2 failure modes in Section 5
5. Working link in Section 6

### Code Validation
1. All code blocks have language specifier
2. All code blocks have version header
3. Code is syntactically valid
4. Imports are explicit

---

## Section Dependency Map

```text
Concept Overview (1)
       │
       ▼
System Architecture (2) ──────► Diagram (if applicable)
       │
       ▼
Data Flow and Components (3)
       │
       ▼
Example Workflow (4) ◄──────── Code Examples
       │
       ▼
Common Failure Modes (5) ◄──── Troubleshooting
       │
       ▼
Summary (6) ─────────────────► Next Chapter Link
```

---

## Checklist for Authors

- [ ] Section 1 defines concept and learning objectives
- [ ] Section 2 describes architecture with components
- [ ] Section 3 documents complete data flow
- [ ] Section 4 provides reproducible example with code
- [ ] Section 5 lists failure modes with mitigations
- [ ] Section 6 summarizes and links to next chapter
- [ ] Total word count is 500-800
- [ ] All code has version headers
- [ ] At least one citation per chapter
