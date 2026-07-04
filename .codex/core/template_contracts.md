# Template Contracts

## Purpose

This document is the canonical contract for all reusable note and report templates.
Legacy files under `../templates/` and `../reports/` are retained for path compatibility, but future agents should treat this file as the authoritative template layer.

Global policy:

- [mandatory_rules.md](mandatory_rules.md)
- [quality_standards.md](quality_standards.md)
- [workflow_router.md](workflow_router.md)

## General Note Contract

Use for durable concept notes.

Required intent:

- Purpose.
- System context.
- Mechanism.
- Assumptions.
- Related links.
- Source and verification status.

Recommended sections:

```markdown
# Title

## Purpose
## Summary
## System Context
## Key Concepts
## Mechanism
## Equations
## Design Tradeoffs
## Failure Modes or Debug Hooks
## Related Notes
## Sources and Verification Status
## Open Questions
```

## Paper Note Contract

Use for source-specific paper notes.

Required intent:

- Citation.
- Reading status.
- Architecture or method summary.
- Claims versus interpretation.
- Metrics with units and conditions.
- Related durable notes.

Recommended sections:

```markdown
# Paper Title

## Citation
## One-Sentence Value
## Reading Status
## Problem Statement
## Architecture Summary
## Key Technical Claims
## Metrics and Conditions
## Design Lessons
## Relevance to This Vault
## Related Notes
## Claims Not Yet Verified
```

## Book Note Contract

Use for textbooks and long-form references.

Required intent:

- Bibliographic details.
- Reading scope.
- Chapter or concept map.
- Extracted concepts.
- Links to durable notes.

## Design Note Contract

Use for engineering decisions, tradeoff studies, debug plans, and design investigations.

Required intent:

- Design question.
- Context.
- Assumptions.
- Candidate options.
- Analysis.
- Evidence plan.
- Decision or current conclusion.

## Interview Note Contract

Use for technical Q&A, story banks, and role preparation.

Required intent:

- Role context.
- 30-second answer.
- Deeper answer.
- Tradeoff.
- Practical check.
- Deep references.
- Truthful experience mapping.

## Ingest Report Contract

Use after substantial source ingestion.

Required intent:

- Source paths.
- Destination notes changed.
- Content promoted.
- Content left raw.
- Content not promoted.
- Technical uncertainty.
- Confidentiality screen.
- Verification performed.
- Continuous knowledge improvement actions and metrics from [../continuous_knowledge_improvement.md](../continuous_knowledge_improvement.md).

## Template Quality Gate

Before using any template:

- Remove unused sections.
- Keep source status visible.
- Do not duplicate global policy inside the note.
- Link to durable notes when relevant.
- Apply [quality_standards.md](quality_standards.md).
