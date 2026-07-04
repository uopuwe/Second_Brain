# Ingest Workflow

## Purpose

Use this workflow when bringing raw or semi-processed material into the vault.
Global policy is in [core/mandatory_rules.md](core/mandatory_rules.md).
Quality gates are in [core/quality_standards.md](core/quality_standards.md).
The end-to-end source pipeline is defined in [knowledge_ingestion_pipeline.md](knowledge_ingestion_pipeline.md).

## Active Roles

- Researcher: source quality and verification status.
- Librarian: source preservation and traceability.
- Knowledge architect: destination selection.
- Analog IC expert: technical screening.

Role responsibilities are defined in [core/roles.md](core/roles.md).

## Inputs

This workflow applies to chat exports, manual source packets, processed AI summaries, paper excerpts, book notes, interview notes, work or design notes, and Python analysis snippets.

## Workflow

1. Preserve raw input in the appropriate source location.
2. Inventory source path, source type, date if known, domains, and sensitivity.
3. Search for existing canonical notes before creating new files.
4. Classify fragments as concept, equation, tradeoff, debug, interview, source, career, raw, or not promoted.
5. Screen technical claims for assumptions, units, source quality, and confidentiality.
6. Choose destination using [knowledge_tree.md](knowledge_tree.md).
7. Promote only durable content into domain notes.
8. Record provenance in every destination note touched.
9. Add links using [build_links.md](build_links.md) when promoted material affects related notes.
10. Update indexes using [indexing.md](indexing.md) only for major durable changes.
11. Write an ingest report for substantial batches using [reports/ingest_report_template.md](reports/ingest_report_template.md).
12. Archive completed source packets according to [knowledge_ingestion_pipeline.md](knowledge_ingestion_pipeline.md).
13. Verify against [core/quality_standards.md](core/quality_standards.md).

## Destination Rules

- Raw chat exports: `00_Inbox/raw_chat_exports/`
- Manual source packets: `00_Inbox/manual_batches/`
- Processed summaries: `00_Inbox/processed_by_chatgpt/`
- Conversation inventories: `00_Inbox/conversation_inventory/`
- Durable technical notes: `01_AnalogIC_SerDes/`
- Work context: `02_Synopsys_Work/`
- Agent operating documents: `.codex/`
- Completed source packets: `90_Archive/`

## Good Example

```markdown
Source packet about PCIe 7.0 clocking is preserved under `00_Inbox/manual_batches/`.
Durable clocking concepts are promoted to `01_AnalogIC_SerDes/PLL_CDR_Clocking/pcie7_clocking_notes.md`.
Exact compliance numbers remain marked as requiring current primary-source verification.
```

## Bad Example

```markdown
A full AI conversation is pasted into a PLL note and treated as source-backed technical truth.
```

## Edge Cases

- If a source contains confidential work details, generalize the learning and do not promote sensitive identifiers.
- If a source conflicts with an existing note, record the conflict instead of silently overwriting.
- If a source has no durable value, preserve or report it without promoting content.
- If exact standards numbers appear, promote only when source and conditions are clear.

## Output Contract

An ingest task should produce one or more of updated durable notes, source-specific notes, a source inventory, an ingest report, links, or index entries.
Final response must include changed files and verification limits.
