# Workflow Router

## Purpose

Use this document to choose the correct workflow or standard before acting.
Mandatory policy is in [mandatory_rules.md](mandatory_rules.md).
Quality gates are in [quality_standards.md](quality_standards.md).

## Routing Table

| User request | Use this document |
| --- | --- |
| Bring source material into the vault | [../ingest.md](../ingest.md) |
| Process source material from `00_Inbox/` through final archive | [../knowledge_ingestion_pipeline.md](../knowledge_ingestion_pipeline.md) |
| Combine overlapping notes | [../merge_knowledge.md](../merge_knowledge.md) |
| Turn a thin note into a durable note | [../expand_note.md](../expand_note.md) |
| Review content without necessarily editing | [../review.md](../review.md) |
| Add cross-links or backlinks | [../build_links.md](../build_links.md) |
| Maintain master indexes | [../indexing.md](../indexing.md) |
| Design or audit repository-scale knowledge architecture | [../knowledge_architecture.md](../knowledge_architecture.md) |
| Decide where knowledge belongs | [../knowledge_tree.md](../knowledge_tree.md) |
| Check engineering depth | [../engineering_notes.md](../engineering_notes.md) |
| Check formulas | [../formula_style.md](../formula_style.md) |
| Check Markdown and Obsidian style | [../obsidian_style.md](../obsidian_style.md) |
| Create a general note | [template_contracts.md](template_contracts.md) |
| Create a paper note | [template_contracts.md](template_contracts.md) |
| Create a book note | [template_contracts.md](template_contracts.md) |
| Create a design note | [template_contracts.md](template_contracts.md) |
| Create interview material | [template_contracts.md](template_contracts.md) |
| Report a source ingest | [template_contracts.md](template_contracts.md) |

## Multi-Workflow Tasks

Many tasks require multiple workflows.

Examples:

- Ingesting a paper may use `ingest.md`, `paper_template.md`, `build_links.md`, and `indexing.md`.
- Expanding a PLL note may use `expand_note.md`, `engineering_notes.md`, `formula_style.md`, and `build_links.md`.
- Merging duplicate ADC notes may use `merge_knowledge.md`, `knowledge_tree.md`, `build_links.md`, and `indexing.md`.

## Default Decision Logic

1. If source material is raw, start with ingest.
2. If two notes overlap, start with merge.
3. If one note is thin, start with expand.
4. If the user asks for critique, start with review.
5. If the task is navigation, start with links or indexing.
6. If the task is note creation, choose the template by note type.
7. If uncertain, inspect files and choose the least destructive workflow.

## Output Expectations

Every workflow should end with:

- Files changed or reviewed.
- Quality checks performed.
- Remaining uncertainty or verification limits.
- Any recommended follow-up that materially matters.
