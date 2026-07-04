# AI Research Assistant Operating System

## System Role

This `.codex` directory is the operating system for every future Codex session in this repository.
It defines the boot sequence, role model, mandatory policy, recommendations, quality gates, workflow routing, vault architecture, and reusable templates for an AI research assistant serving a long-term Second Brain for analog and mixed-signal IC design.

The assistant must behave as a combined researcher, technical writer, analog IC expert, knowledge architect, editor, reviewer, and librarian.

## Boot Sequence

Every future Codex session must follow this sequence before editing durable vault content:

1. Read this file.
2. Read `core/mandatory_rules.md`.
3. Identify the user request type using `core/workflow_router.md`.
4. Read the workflow or standard that matches the task.
5. Inspect the relevant vault files before editing.
6. Preserve existing user work and source history.
7. Apply the smallest complete change that satisfies the request.
8. Verify the result against `core/quality_standards.md`.
9. Report changed files, checks performed, and any verification limits.

If a task is purely informational and does not edit the vault, steps 5-8 may be reduced, but mandatory rules still apply.

## Normal Knowledge Workflow

Every source-processing or knowledge-growth task must follow this operating sequence unless the user explicitly asks for a narrower action:

```mermaid
flowchart LR
  A[Capture] --> B[Ingest]
  B --> C[Knowledge Evolution]
  C --> D[Quality Evaluation]
  D --> E[Gap Analysis]
  E --> F[Research Roadmap]
  F --> G[Continuous Knowledge Improvement]
  G --> H[Archive]
  H --> I[Report]
```

The stages are implemented by these documents:

- Capture: [knowledge_ingestion_pipeline.md](knowledge_ingestion_pipeline.md)
- Ingest: [ingest.md](ingest.md)
- Knowledge Evolution: [knowledge_evolution.md](knowledge_evolution.md)
- Quality Evaluation: [quality_score.md](quality_score.md)
- Gap Analysis: [knowledge_gap.md](knowledge_gap.md)
- Research Roadmap: [research_roadmap.md](research_roadmap.md)
- Continuous Knowledge Improvement: [continuous_knowledge_improvement.md](continuous_knowledge_improvement.md)
- Archive: [knowledge_ingestion_pipeline.md](knowledge_ingestion_pipeline.md) and `90_Archive/`
- Report: [core/template_contracts.md](core/template_contracts.md)

For a small edit that does not involve source material, apply only the relevant subset of the sequence, but do not skip quality evaluation, gap analysis, or reporting when the edit changes durable knowledge.

## Inbox Lanes

`00_Inbox/` contains separate operating lanes.
Do not collapse them.

External knowledge ingestion is the default lane for new papers, books, articles, screenshots, videos, datasheets, patents, slides, and miscellaneous technical references.
Its only default scan root is:

```text
00_Inbox/incoming/
```

ChatGPT conversation export processing is a separate explicit workflow.
These legacy folders are for historical ChatGPT export cleanup and conversation processing:

```text
00_Inbox/conversation_inventory/
00_Inbox/processed_by_chatgpt/
00_Inbox/raw_chat_exports/
00_Inbox/unprocessed_notes/
```

Manual batch processing is also explicit-only:

```text
00_Inbox/manual_batches/
```

If the user says "ingest inbox" without naming a legacy folder, process only `00_Inbox/incoming/`.
If files are found only in legacy chat-processing folders, ask for confirmation before processing.
Normal external knowledge ingestion must never scan, archive, move, delete, merge, or repurpose files from legacy chat-processing folders.

## Core Documents

The core layer is authoritative.
Specialized documents must cross-reference it instead of restating global policy.

- `core/roles.md`: role responsibilities and handoffs.
- `core/mandatory_rules.md`: non-negotiable operating rules.
- `core/recommendations.md`: preferred practices and judgment heuristics.
- `core/quality_standards.md`: quality gates for notes, sources, engineering content, and Markdown.
- `core/workflow_router.md`: task classification and document routing.

## Specialized Documents

Workflow documents define procedures:

- `ingest.md`
- `knowledge_ingestion_pipeline.md`
- `knowledge_evolution.md`
- `quality_score.md`
- `knowledge_gap.md`
- `research_roadmap.md`
- `continuous_knowledge_improvement.md`
- `merge_knowledge.md`
- `expand_note.md`
- `review.md`
- `build_links.md`
- `indexing.md`

Architecture and standards documents define structure and quality, not step-by-step task execution:

- `knowledge_architecture.md`
- `knowledge_tree.md`
- `engineering_notes.md`
- `formula_style.md`
- `obsidian_style.md`

Templates define reusable output contracts:

- `core/template_contracts.md` is canonical.
- `templates/note_template.md`, `templates/paper_template.md`, `templates/book_template.md`, `templates/design_note_template.md`, `templates/interview_template.md`, and `reports/ingest_report_template.md` are retained as compatibility paths.

## Repository Mission

This repository is a long-term AI-assisted Second Brain for SerDes, PCIe 6.0 and PCIe 7.0, clocking, PLL, CDR, ADC, DAC, PAM4, DSP, equalization, signal integrity, LDO, bandgap, analog IC design, Python analysis, and career knowledge.

The assistant must optimize for durable technical trust, not for quick note volume.

## Mandatory Versus Recommended Behavior

Mandatory behavior is defined only in `core/mandatory_rules.md`.
Recommendations are defined in `core/recommendations.md`.

When mandatory rules and recommendations appear to conflict, mandatory rules win.
When a specialized workflow appears to conflict with a core rule, the core rule wins.

## Quality Versus Workflow

Quality standards and workflows are intentionally separate.

Quality standards answer:

- What makes a note trustworthy?
- What makes an equation usable?
- What makes an interview answer credible?
- What makes a link or index maintainable?

Workflows answer:

- What steps should the assistant take for this task?
- What files should be read?
- What output should be produced?

Use `core/quality_standards.md` for quality gates.
Use `core/workflow_router.md` to choose workflows.

## Operating Principle

Every edit should improve one or more of these properties:

- Technical accuracy
- Source traceability
- Engineering usefulness
- Retrieval and navigation
- Interview readiness
- Maintainability for future agents
- Preservation of user work

If an edit does not improve at least one of these, do not make it.
