# Ingest Workflow

## Purpose

Use this workflow when bringing new external knowledge material into the vault.
Global policy is in [core/mandatory_rules.md](core/mandatory_rules.md).
Quality gates are in [core/quality_standards.md](core/quality_standards.md).
The end-to-end source pipeline is defined in [knowledge_ingestion_pipeline.md](knowledge_ingestion_pipeline.md).

For normal knowledge ingestion, the default inbox root is `00_Inbox/incoming/`.
The phrase "ingest everything in `00_Inbox`" means ingest only `00_Inbox/incoming/` unless the user explicitly names a legacy ChatGPT or conversation-processing folder.

## Active Roles

- Researcher: source quality and verification status.
- Librarian: source preservation and traceability.
- Knowledge architect: destination selection.
- Analog IC expert: technical screening.

Role responsibilities are defined in [core/roles.md](core/roles.md).

## Inputs

This workflow applies by default to external knowledge material placed under `00_Inbox/incoming/`, including papers, books, articles, screenshots, videos, datasheets, patents, slides, technical references, interview notes, work or design notes, and Python analysis snippets.

ChatGPT exports, conversation inventories, processed ChatGPT summaries, historical manual batches, and unprocessed conversation notes use the separate conversation-processing workflow and require explicit user instruction before processing.

## Workflow

The ingest workflow is no longer complete when content is merely promoted.
Every source-processing task follows this chain:

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

1. Capture new external source material in `00_Inbox/incoming/` according to [knowledge_ingestion_pipeline.md](knowledge_ingestion_pipeline.md).
2. Inventory source path, source type, date if known, domains, and sensitivity.
3. Search for existing canonical notes before creating new files.
4. Classify fragments as concept, equation, tradeoff, debug, interview, source, career, raw, or not promoted.
5. Screen technical claims for assumptions, units, source quality, and confidentiality.
6. Choose destination using [knowledge_tree.md](knowledge_tree.md) and [knowledge_architecture.md](knowledge_architecture.md).
7. Promote only durable content into domain notes.
8. Record provenance in every destination note touched.
9. Apply [knowledge_evolution.md](knowledge_evolution.md) to decide whether each output is a reference note, seed note, active permanent note, MOC candidate, handbook candidate, superseded item, or archive-only source.
10. Apply [quality_score.md](quality_score.md) to durable notes that were created, substantially changed, or proposed for maturity.
11. Apply [knowledge_gap.md](knowledge_gap.md) to record unresolved source, equation, standards, link, tradeoff, debug, or synthesis gaps.
12. Apply [research_roadmap.md](research_roadmap.md) when a gap is high-priority, multi-note, source-dependent, or relevant to SerDes/PCIe7/PLL/CDR/ADC/LDO/DSP study direction.
13. Apply [continuous_knowledge_improvement.md](continuous_knowledge_improvement.md) to run the automatic post-ingest improvement pass: refactor changed notes, triage duplicates, optimize links, improve formulas, expand engineering insight, generate interview questions, detect research gaps, recommend reading, and check knowledge density.
14. Add links using [build_links.md](build_links.md) when promoted material affects related notes or CKI identifies missing graph edges.
15. Update indexes using [indexing.md](indexing.md) when notes become canonical, mature, MOC-worthy, source-index-worthy, roadmap-relevant, or CKI identifies retrieval gaps.
16. Archive completed source packets according to [knowledge_ingestion_pipeline.md](knowledge_ingestion_pipeline.md) only after CKI status is recorded.
17. Write an ingest report for substantial batches using [core/template_contracts.md](core/template_contracts.md). The legacy path [reports/ingest_report_template.md](reports/ingest_report_template.md) remains available for compatibility.
18. Verify against [core/quality_standards.md](core/quality_standards.md).

## Destination Rules

- New papers: `00_Inbox/incoming/papers/`
- New books: `00_Inbox/incoming/books/`
- New articles and blog posts: `00_Inbox/incoming/articles/`
- New screenshots and images: `00_Inbox/incoming/screenshots/`
- New videos and transcripts: `00_Inbox/incoming/videos/`
- New datasheets: `00_Inbox/incoming/datasheets/`
- New patents: `00_Inbox/incoming/patents/`
- New slide decks: `00_Inbox/incoming/slides/`
- New uncategorized external material: `00_Inbox/incoming/misc/`
- Legacy raw chat exports, explicit workflow only: `00_Inbox/raw_chat_exports/`
- Legacy manual source packets, explicit workflow only: `00_Inbox/manual_batches/`
- Legacy processed ChatGPT summaries, explicit workflow only: `00_Inbox/processed_by_chatgpt/`
- Legacy conversation inventories, explicit workflow only: `00_Inbox/conversation_inventory/`
- Legacy unprocessed conversation notes, explicit workflow only: `00_Inbox/unprocessed_notes/`
- Durable technical notes: `01_AnalogIC_SerDes/`
- Work context: `02_Synopsys_Work/`
- Agent operating documents: `.codex/`
- Completed source packets: `90_Archive/`

## Inbox Lane Rules

- `00_Inbox/incoming/` is the only default scan target for new external knowledge ingestion.
- `00_Inbox/conversation_inventory/`, `00_Inbox/manual_batches/`, `00_Inbox/processed_by_chatgpt/`, `00_Inbox/raw_chat_exports/`, and `00_Inbox/unprocessed_notes/` are legacy ChatGPT export and conversation-processing lanes.
- Normal paper, book, article, screenshot, video, datasheet, patent, slide, or technical-reference ingestion must never scan legacy chat-processing folders.
- ChatGPT export ingestion must be requested explicitly and handled as conversation processing, not as default external knowledge ingestion.
- If the user says "ingest inbox" without clarification, process `00_Inbox/incoming/` only.
- If relevant files are found only in legacy folders, ask for confirmation before processing them.
- During normal incoming ingestion, do not archive, move, delete, merge, or repurpose files from legacy chat-processing folders.

## Good Example

```markdown
Source packet about PCIe 7.0 clocking is preserved under `00_Inbox/incoming/papers/` or `00_Inbox/incoming/slides/`.
Durable clocking concepts are promoted to `01_AnalogIC_SerDes/PLL_CDR_Clocking/pcie7_clocking_notes.md`.
Exact compliance numbers remain marked as requiring current primary-source verification.
```

## Bad Example

```markdown
A full AI conversation is pasted into a PLL note and treated as source-backed technical truth.
```

```markdown
The user says "ingest inbox", and the assistant scans `00_Inbox/raw_chat_exports/` without explicit confirmation.
```

## Edge Cases

- If a source contains confidential work details, generalize the learning and do not promote sensitive identifiers.
- If a source conflicts with an existing note, record the conflict instead of silently overwriting.
- If a source has no durable value, preserve or report it without promoting content.
- If exact standards numbers appear, promote only when source and conditions are clear.

## Output Contract

An ingest task should produce one or more of updated durable notes, source-specific notes, a source inventory, an ingest report, links, index entries, CKI actions, or CKI metrics.
Final response must include changed files, lifecycle decisions, quality evaluation, gap decisions, roadmap decisions, continuous improvement actions, archive actions, and verification limits.
