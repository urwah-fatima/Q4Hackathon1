<!--
Sync Impact Report
==================
Version change: 0.0.0 → 1.0.0 (MAJOR - initial constitution ratification)

Modified principles: N/A (initial version)

Added sections:
- Core Principles (6 principles: Accuracy First, Context Primacy, Technical Rigor, Clarity, Reproducibility, Modularity)
- Authorship Standards (citation, attribution, quality)
- Content Development Workflow (research, verification, review)
- Governance (amendment procedures, versioning)

Removed sections: N/A (initial version)

Templates requiring updates:
- ✅ plan-template.md - Constitution Check section compatible
- ✅ spec-template.md - Requirements/Success criteria compatible
- ✅ tasks-template.md - Phase structure compatible

Follow-up TODOs: None
-->

# Physical AI & Humanoid Robotics Book Constitution

## Core Principles

### I. Accuracy First

All factual claims, technical specifications, and procedural descriptions MUST be verifiable against authoritative sources. This principle supersedes completeness—incomplete but accurate content is preferable to comprehensive but unverifiable content.

**Non-negotiables:**
- Every technical claim MUST cite at least one authoritative source
- Unverified information MUST be explicitly marked as "unverified" or "requires verification"
- Speculative content MUST be clearly distinguished from established fact
- When sources conflict, all perspectives MUST be presented with source attribution

### II. Context Primacy

MCP-provided Docusaurus documentation serves as the primary source of truth for all project-related technical content. External sources supplement but never override MCP context.

**Non-negotiables:**
- MCP-provided documentation takes precedence over general knowledge
- When MCP context is unavailable, explicitly state the alternative source used
- All technical workflows MUST be validated against MCP-provided specifications
- Deviations from MCP guidance MUST be justified and documented

### III. Technical Rigor

Content MUST reflect the standards of peer-reviewed academic and industry publications. All technical content undergoes verification against official vendor documentation and established research.

**Acceptable source hierarchy (in order of preference):**
1. MCP-provided Docusaurus documentation
2. Official vendor/manufacturer documentation
3. Peer-reviewed academic publications (IEEE, ACM, arXiv with peer review)
4. Industry whitepapers from established organizations
5. Technical standards documents (ISO, IEC, ROS REPs)

**Non-negotiables:**
- Citation style: APA format (inline references where appropriate)
- Plagiarism tolerance: 0% (all content must be original or properly attributed)
- Code examples MUST be tested and functional
- Mathematical formulations MUST be verified for correctness

### IV. Clarity

All content targets readers with computer science or robotics background (undergraduate level or higher). Writing MUST be precise, unambiguous, and free of unnecessary jargon.

**Non-negotiables:**
- Flesch-Kincaid grade level: appropriate for technical graduate audience
- Technical terms MUST be defined on first use
- Acronyms MUST be expanded on first occurrence per chapter
- Complex concepts MUST include illustrative examples
- Avoid marketing language; prefer precise technical description

### V. Reproducibility

All technical workflows, code examples, and procedures MUST be logically complete and internally consistent. A qualified reader should be able to reproduce any described process.

**Non-negotiables:**
- All code examples MUST include version specifications for dependencies
- Hardware configurations MUST specify exact models and firmware versions
- Simulation environments MUST document all parameters
- Step-by-step procedures MUST be tested before publication
- Known limitations and failure modes MUST be documented

### VI. Modularity

Each chapter MUST function as an independent unit while contributing to the complete system architecture. Cross-references are permitted but no chapter may require another to be comprehensible.

**Non-negotiables:**
- Each chapter MUST have clearly defined prerequisites
- Shared concepts MUST be briefly restated rather than assumed
- Code modules MUST be self-contained with explicit imports
- Chapter dependencies MUST form a directed acyclic graph (no circular dependencies)

## Authorship Standards

### Citation and Attribution

- **Primary format**: APA 7th edition
- **In-text citations**: Author-date format for academic sources
- **Code attribution**: Comment header with source URL and license
- **Figure attribution**: Caption with source and permission status
- **Data attribution**: Methodology section with dataset provenance

### Quality Gates

All content MUST pass these gates before inclusion:

1. **Source verification**: Every claim traced to acceptable source
2. **Technical review**: Code/math verified by execution or proof
3. **Clarity review**: Terminology consistent, definitions present
4. **Reproducibility check**: Procedures tested on clean environment

## Content Development Workflow

### Research Phase

1. Query MCP-provided documentation first
2. Supplement with official vendor documentation
3. Cross-reference against peer-reviewed literature
4. Document all sources in working bibliography

### Verification Phase

1. Test all code examples in specified environments
2. Verify mathematical derivations
3. Validate hardware specifications against datasheets
4. Confirm API contracts against current documentation

### Review Phase

1. Technical accuracy review (source verification)
2. Clarity review (terminology, structure)
3. Reproducibility review (procedure completeness)
4. Consistency review (cross-chapter alignment)

## Governance

This constitution establishes the authoritative standards for all content in the Physical AI & Humanoid Robotics book project. All contributors, human and AI, MUST adhere to these principles.

### Amendment Procedure

1. Proposed amendments MUST be documented with rationale
2. Amendments MUST specify affected sections and migration requirements
3. Version increment follows semantic versioning:
   - MAJOR: Principle removal or fundamental redefinition
   - MINOR: New principle or substantial guidance expansion
   - PATCH: Clarification, correction, or minor refinement
4. All amendments MUST update dependent templates (plan, spec, tasks)

### Compliance

- All pull requests MUST verify constitution compliance
- Complexity or deviation MUST be justified against principles
- Runtime development guidance in `CLAUDE.md` supplements but does not override this constitution

**Version**: 1.0.0 | **Ratified**: 2025-12-18 | **Last Amended**: 2025-12-18
