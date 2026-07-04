# 00_Inbox Guide

## Purpose

`00_Inbox/` is the landing area for material that has not yet become durable vault knowledge.
It contains two separate operating lanes:

- New external knowledge ingestion.
- Legacy ChatGPT export and conversation-processing workflows.

These lanes must remain separate.
Normal knowledge ingestion scans only `00_Inbox/incoming/`.
Legacy ChatGPT and conversation-processing folders require explicit user instruction.

## Default Incoming Lane

Use `00_Inbox/incoming/` for new external knowledge materials.

```text
00_Inbox/incoming/
  papers/
  books/
  articles/
  screenshots/
  videos/
  datasheets/
  patents/
  slides/
  misc/
```

If the user says "ingest inbox" without further clarification, Codex may scan only:

```text
00_Inbox/incoming/
```

Codex must not scan legacy ChatGPT or conversation-processing folders during normal incoming ingestion.

## Where To Put New Material

### Papers

Put papers here:

```text
00_Inbox/incoming/papers/
```

Use for:

- ISSCC papers.
- JSSC papers.
- VLSI Symposium papers.
- arXiv papers.
- Conference papers.
- Technical PDF papers.

Example:

```text
00_Inbox/incoming/papers/2026-07-04_jssc_fractional_n_pll.pdf
```

### Books

Put books or book-derived material here:

```text
00_Inbox/incoming/books/
```

Use for:

- Book PDFs or EPUBs.
- Chapter notes.
- Reading notes from textbooks.
- Book summary packets.

Example:

```text
00_Inbox/incoming/books/razavi_pll_chapter_notes.md
```

### Articles

Put articles and web references here:

```text
00_Inbox/incoming/articles/
```

Use for:

- Blog posts.
- Technical articles.
- Whitepapers.
- Webpage exports.
- Saved online references.

Example:

```text
00_Inbox/incoming/articles/ctle_noise_tradeoff_article.md
```

### Screenshots

Put screenshots and images here:

```text
00_Inbox/incoming/screenshots/
```

Use for:

- Screenshots of figures.
- Plot captures.
- Measurement screenshots.
- Slide screenshots.
- Formula images.

Example:

```text
00_Inbox/incoming/screenshots/pam4_eye_margin_plot_2026-07-04.png
```

### Videos

Put video-related material here:

```text
00_Inbox/incoming/videos/
```

Use for:

- YouTube transcripts.
- Lecture transcripts.
- Webinar notes.
- Video links saved as Markdown.
- Timestamped technical notes from talks.

Example:

```text
00_Inbox/incoming/videos/cdr_jitter_tolerance_transcript.md
```

### Datasheets

Put datasheets and component references here:

```text
00_Inbox/incoming/datasheets/
```

Use for:

- IC datasheets.
- Evaluation board manuals.
- Application notes tied to specific parts.
- Component specification PDFs.

Example:

```text
00_Inbox/incoming/datasheets/ldo_psrr_datasheet_example.pdf
```

### Patents

Put patent material here:

```text
00_Inbox/incoming/patents/
```

Use for:

- Patent PDFs.
- Patent webpage exports.
- Patent claim notes.
- Prior-art search packets.

Example:

```text
00_Inbox/incoming/patents/adc_based_serdes_receiver_patent.pdf
```

### Slides

Put slide decks here:

```text
00_Inbox/incoming/slides/
```

Use for:

- Conference slide decks.
- Tutorial slides.
- Webinar decks.
- Presentation PDFs.

Example:

```text
00_Inbox/incoming/slides/pcie7_clocking_tutorial_slides.pdf
```

### Miscellaneous

Put uncategorized external material here:

```text
00_Inbox/incoming/misc/
```

Use for:

- Material that does not yet fit another incoming category.
- Mixed source packets.
- Temporary external references awaiting classification.

Example:

```text
00_Inbox/incoming/misc/serdes_research_packet_2026-07-04.md
```

## Legacy ChatGPT And Conversation-Processing Folders

The following folders already existed before the `incoming/` lane.
They are preserved for ChatGPT export cleanup and historical conversation processing.
Do not rename, move, delete, merge, or repurpose them.

### `conversation_inventory/`

Purpose:

- Inventory files for prior ChatGPT conversations.
- Conversion reports.
- Conversation lists and processing status.

Default scan permission:

- Codex must not scan this folder during normal incoming ingestion.
- Codex may process it only when the user explicitly asks for conversation inventory or ChatGPT export work.

### `manual_batches/`

Purpose:

- Historical manual batches.
- Curated conversation/source packets from earlier workflows.
- Batch-oriented cleanup material.

Default scan permission:

- Codex must not scan this folder during normal incoming ingestion.
- Codex may process it only when the user explicitly names manual batch processing.

### `processed_by_chatgpt/`

Purpose:

- Processed ChatGPT summaries.
- AI-assisted conversation outputs.
- Intermediate material from ChatGPT export cleanup.

Default scan permission:

- Codex must not scan this folder during normal incoming ingestion.
- Codex may process it only when the user explicitly asks to ingest or review processed ChatGPT output.

### `raw_chat_exports/`

Purpose:

- Raw ChatGPT exports.
- Unfiltered conversation exports.
- Source material for conversation cleanup.

Default scan permission:

- Codex must not scan this folder during normal incoming ingestion.
- Codex may process it only when the user explicitly asks for raw ChatGPT export processing.

### `unprocessed_notes/`

Purpose:

- Legacy unprocessed conversation notes.
- Notes awaiting explicit cleanup or routing.

Default scan permission:

- Codex must not scan this folder during normal incoming ingestion.
- Codex may process it only when the user explicitly asks for legacy note processing.

## Default Scan Rules

Codex may scan by default:

```text
00_Inbox/incoming/
```

Codex requires explicit instruction before scanning:

```text
00_Inbox/conversation_inventory/
00_Inbox/manual_batches/
00_Inbox/processed_by_chatgpt/
00_Inbox/raw_chat_exports/
00_Inbox/unprocessed_notes/
```

## Safety Rules

- Normal incoming ingestion must never touch legacy ChatGPT or conversation-processing folders.
- Codex must never archive, move, delete, merge, or repurpose files from legacy folders during normal incoming ingestion.
- If files are found only in legacy folders, Codex must ask for confirmation before processing them.
- If the user says "ingest inbox", Codex must treat that as `00_Inbox/incoming/` only.
- ChatGPT export ingestion is a separate explicit workflow.
- Manual batch processing is a separate explicit workflow.

## Summary

Use `00_Inbox/incoming/` for new external knowledge.
Use the legacy folders only for explicit ChatGPT export, conversation inventory, or manual batch work.
This keeps new research ingestion clean while preserving the historical conversation-processing workflow.
