# Workflow Router

## Purpose

Use this document to choose the correct workflow or standard before acting.
Mandatory policy is in [mandatory_rules.md](mandatory_rules.md).
Quality gates are in [quality_standards.md](quality_standards.md).

## Routing Table

| User request | Use this document |
| --- | --- |
| Bring new external source material into the vault | [../ingest.md](../ingest.md) |
| Ingest papers, books, articles, screenshots, videos, datasheets, patents, slides, or technical references from `00_Inbox/incoming/` | [../ingest.md](../ingest.md) |
| Process source material from `00_Inbox/incoming/` through final archive | [../knowledge_ingestion_pipeline.md](../knowledge_ingestion_pipeline.md) |
| Choose Fast Ingest, Balanced Ingest, or Deep Ingest | [../ingest.md](../ingest.md) |
| Process ChatGPT exports, conversation inventories, processed ChatGPT summaries, historical manual batches, or unprocessed conversation notes | Conversation-processing workflow; require explicit user instruction before scanning legacy folders |
| Combine overlapping notes | [../merge_knowledge.md](../merge_knowledge.md) |
| Turn a thin note into a durable note | [../expand_note.md](../expand_note.md) |
| Review content without necessarily editing | [../review.md](../review.md) |
| Add cross-links or backlinks | [../build_links.md](../build_links.md) |
| Maintain master indexes | [../indexing.md](../indexing.md) |
| Design or audit repository-scale knowledge architecture | [../knowledge_architecture.md](../knowledge_architecture.md) |
| Manage note maturity or lifecycle transitions | [../knowledge_evolution.md](../knowledge_evolution.md) |
| Score note quality or maturity | [../quality_score.md](../quality_score.md) |
| Identify or close knowledge gaps | [../knowledge_gap.md](../knowledge_gap.md) |
| Plan research priorities or study tracks | [../research_roadmap.md](../research_roadmap.md) |
| Run automatic post-ingest knowledge improvement | [../continuous_knowledge_improvement.md](../continuous_knowledge_improvement.md) |
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

## Normal Knowledge Workflow

When a request involves source material, durable note growth, or repository knowledge maintenance, route through the full workflow:

```text
Capture
  -> Ingest
  -> Knowledge Evolution
  -> Quality Evaluation
  -> Gap Analysis
  -> Research Roadmap
  -> Continuous Knowledge Improvement
  -> Archive
  -> Report
```

Stage routing:

| Stage | Required documents |
| --- | --- |
| Capture | [../knowledge_ingestion_pipeline.md](../knowledge_ingestion_pipeline.md) |
| Ingest | [../ingest.md](../ingest.md), [template_contracts.md](template_contracts.md) |
| Knowledge Evolution | [../knowledge_evolution.md](../knowledge_evolution.md) |
| Quality Evaluation | [../quality_score.md](../quality_score.md), [../review.md](../review.md) when needed |
| Gap Analysis | [../knowledge_gap.md](../knowledge_gap.md) |
| Research Roadmap | [../research_roadmap.md](../research_roadmap.md) |
| Continuous Knowledge Improvement | [../continuous_knowledge_improvement.md](../continuous_knowledge_improvement.md), [../merge_knowledge.md](../merge_knowledge.md), [../build_links.md](../build_links.md), [../formula_style.md](../formula_style.md), [../engineering_notes.md](../engineering_notes.md), [../indexing.md](../indexing.md) |
| Archive | [../knowledge_ingestion_pipeline.md](../knowledge_ingestion_pipeline.md), `90_Archive/` |
| Report | [template_contracts.md](template_contracts.md) |

Use a subset only when the request is explicitly scoped, such as "review this note only" or "fix this link only."
If a scoped request changes durable knowledge, still apply quality evaluation, gap analysis, and reporting.

## Ingest Level Routing

Every normal external knowledge ingest must select one ingest level before extraction.
If the user does not name a level, route to Balanced Ingest.

| Ingest level | Route when |
| --- | --- |
| Fast Ingest | The source is a blog post, short article, Reddit/forum discussion, screenshot, simple slide deck, or low-risk quick-reference item; the user asks for a quick or lightweight ingest; token use should be minimized. |
| Balanced Ingest | The user does not specify a mode; the source is an ordinary paper, whitepaper, datasheet, technical article, useful slide deck, or moderate-size source that deserves reusable engineering extraction without full deep study. |
| Deep Ingest | The user explicitly asks for deep study, or the source is a high-value textbook, PCIe specification, cornerstone paper, important JSSC/ISSCC paper, or source that should update multiple canonical notes with formulas, derivations, examples, mistakes, interview material, and implementation notes. |

Routing safeguards:

- Never select Deep Ingest by default.
- For full books, long standards, large specifications, or very large source packets, ask before using Deep Ingest unless the user explicitly requested Deep Ingest.
- Ingest level controls depth only; it does not permit duplicate notes, legacy-folder scanning, architecture changes, or unproven claims.
- Fast Ingest may archive a source with little or no durable-note update when no clearly reusable knowledge is found.
- Balanced and Deep Ingest must still avoid deep rewrites unless the source materially improves an existing canonical note.

## Inbox Routing Rules

Default external knowledge ingestion scans only `00_Inbox/incoming/`.
This lane is for new papers, books, articles, screenshots, videos, datasheets, patents, slides, and miscellaneous technical references.

Legacy ChatGPT and conversation-processing folders are not part of normal external knowledge ingestion:

- `00_Inbox/conversation_inventory/`
- `00_Inbox/manual_batches/`
- `00_Inbox/processed_by_chatgpt/`
- `00_Inbox/raw_chat_exports/`
- `00_Inbox/unprocessed_notes/`

Routing decisions:

- If the user says "ingest inbox" without clarification, process only `00_Inbox/incoming/`.
- If the user names a new paper, book, article, screenshot, video, datasheet, patent, slide deck, or technical reference, route to normal knowledge ingestion.
- If the user names ChatGPT export cleanup, conversation inventory, raw chat export, processed ChatGPT summary, manual conversation batch, or historical conversation processing, route to the conversation-processing workflow.
- If files are found only in legacy folders during a normal ingest request, ask for confirmation before processing them.
- During normal incoming ingestion, do not archive, move, delete, merge, or repurpose files from legacy chat-processing folders.

## Multi-Workflow Tasks

Many tasks require multiple workflows.

Examples:

- Ingesting a paper must use capture, ingest, knowledge evolution, quality evaluation, gap analysis, roadmap decision, continuous knowledge improvement, archive, and report stages.
- Processing a ChatGPT export must not use the default `00_Inbox/incoming/` assumption; it requires explicit conversation-processing scope.
- Expanding a PLL note may use `expand_note.md`, `engineering_notes.md`, `formula_style.md`, and `build_links.md`.
- Merging duplicate ADC notes may use `merge_knowledge.md`, `knowledge_tree.md`, `build_links.md`, and `indexing.md`.
- Upgrading a note to mature status may use `knowledge_evolution.md`, `quality_score.md`, `review.md`, and `indexing.md`.
- Planning SerDes or PCIe7 study may use `knowledge_gap.md`, `research_roadmap.md`, and `knowledge_architecture.md`.

## Default Decision Logic

1. If source material is raw external knowledge, start with capture and ingest from `00_Inbox/incoming/`.
2. If the user says "ingest inbox", default to `00_Inbox/incoming/`.
3. If the user does not specify Fast, Balanced, or Deep Ingest, use Balanced Ingest.
4. If the source is very large and Deep Ingest seems appropriate, ask before using Deep Ingest unless the user explicitly requested it.
5. If source material exists only in legacy ChatGPT or conversation-processing folders, ask for confirmation before processing.
6. If two notes overlap, start with merge.
7. If one note is thin, start with expand.
8. If the user asks for critique, start with review.
9. If the task is navigation, start with links or indexing.
10. If the task is note creation, choose the template by note type.
11. After durable knowledge changes, run knowledge evolution, quality evaluation, gap analysis, roadmap decision, continuous knowledge improvement, archive decision, and report.
12. If uncertain, inspect files and choose the least destructive workflow.

## Output Expectations

Every workflow should end with:

- Files changed or reviewed.
- Ingest level selected when source material was processed.
- Quality checks performed.
- Lifecycle status decision.
- Quality score or reason scoring was not needed.
- Gaps opened, closed, or explicitly absent.
- Roadmap item created, updated, deferred, or explicitly unnecessary.
- Continuous improvement actions performed or explicitly unnecessary.
- Archive action or reason no archive action was needed.
- Remaining uncertainty or verification limits.
- Any recommended follow-up that materially matters.
