# Knowledge Ingestion Pipeline

## Purpose

This document is the permanent standard workflow for moving knowledge through this repository.
For normal external knowledge ingestion, the pipeline starts in `00_Inbox/incoming/` and ends in `90_Archive/`.

It applies to books, ISSCC papers, JSSC papers, patents, conference slides, blog posts, YouTube transcripts, PDFs, images, screenshots, whitepapers, Reddit discussions, emails, Word documents, and Markdown notes.

Global mandatory rules remain authoritative:

- [core/mandatory_rules.md](core/mandatory_rules.md)
- [core/quality_standards.md](core/quality_standards.md)
- [ingest.md](ingest.md)
- [knowledge_tree.md](knowledge_tree.md)

## Pipeline Philosophy

The pipeline treats source material like engineering data.
Raw source is preserved, extracted text is traceable, claims are screened, durable knowledge is promoted into canonical notes, and processed source packets are archived.

The goal is not to ingest everything.
The goal is to convert useful information into trustworthy, retrievable, source-aware knowledge.

## Canonical Flow

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

The detailed ingestion stages below implement the capture and ingest portions of the normal workflow, then hand off to [knowledge_evolution.md](knowledge_evolution.md), [quality_score.md](quality_score.md), [knowledge_gap.md](knowledge_gap.md), [research_roadmap.md](research_roadmap.md), [continuous_knowledge_improvement.md](continuous_knowledge_improvement.md), archive handling, and reporting.
The repository may store intermediate reports for normal external ingestion under `00_Inbox/incoming/` until automation creates dedicated subfolders.
Legacy ChatGPT export and conversation-processing folders under `00_Inbox/` are explicit-only lanes and are not scanned by this pipeline unless the user names them.

## Archive Structure

Use this archive structure when moving completed source packets:

```text
90_Archive/
  processed/
    YYYY/
      source_type/
  rejected/
    YYYY/
      source_type/
  superseded/
    YYYY/
      source_type/
  sensitive/
    YYYY/
      source_type/
```

Archive categories:

- `processed`: source was evaluated and useful content was promoted or intentionally left unpromoted.
- `rejected`: source had no durable value, was too low quality, or was irrelevant.
- `superseded`: source was replaced by a better source or newer version.
- `sensitive`: source should be retained but not promoted because of privacy, confidentiality, or licensing concerns.

Do not archive by deleting provenance.
Archive packets must retain enough metadata to trace durable notes back to source.

## Stage 00: Intake Landing

### Purpose

Capture incoming external material exactly as received under `00_Inbox/incoming/` before interpretation, cleanup, summarization, or promotion.

### Inputs

- Raw PDFs.
- EPUB or book exports.
- Paper PDFs.
- Patent PDFs or web exports.
- Conference slide decks.
- Blog URLs or saved pages.
- YouTube transcript text.
- Images and screenshots.
- Whitepapers.
- Reddit discussions.
- Emails.
- Word documents.
- Markdown notes.
- Manual source packets.

### Outputs

- Source file or packet stored under `00_Inbox/incoming/`.
- Initial filename that preserves origin and date when possible.
- No durable technical note yet.

### Decision Criteria

Accept into intake if:

- The user explicitly provides it.
- It is relevant to analog IC, SerDes, PLL/CDR, ADC/DAC, LDO/bandgap, DSP, SI, Python, or career knowledge.
- It may become useful after screening.

Do not promote at this stage.

### Automation Rules

- Preserve original filenames when meaningful.
- Add date prefixes only when needed for disambiguation.
- Do not OCR, summarize, or rewrite during intake.
- Do not overwrite same-named files; add a suffix or create a packet folder.

### Quality Checks

- File exists.
- File is readable or at least preserved.
- Source location is recorded.
- User-provided context is not lost.

### Failure Recovery

- If a file cannot be read, keep it and mark extraction status as failed.
- If encoding is broken, preserve original and create a separate normalized copy later.
- If source type is unknown, classify it as `unknown_source` until Stage 50.

### Examples

Good:

```text
00_Inbox/incoming/papers/2026-07-04_isscc_adc_pam4_receiver.pdf
```

Bad:

```text
01_AnalogIC_SerDes/ADC/random_pdf_text_dump.md
```

### Performance Considerations

- Large files should stay as source files rather than pasted into Markdown.
- Batch many small screenshots into one source packet when they belong to the same topic.
- Avoid repeatedly parsing large PDFs if extracted text already exists and is traceable.

## Stage 10: Source Registration

### Purpose

Create a source record so the material can be tracked through the pipeline.

### Inputs

- Intake file or folder from Stage 00.
- User-provided description.
- URL, citation, sender, or source metadata if available.

### Outputs

- Source inventory entry.
- Source ID.
- Processing status.
- Initial source type.

### Decision Criteria

Register every source that may be processed.
For trivial one-line notes, registration may be embedded in the destination note's source section.

### Automation Rules

Source ID format:

```text
YYYY-MM-DD_source-type_short-topic
```

Examples:

```text
2026-07-04_isscc-paper_adc-pam4-rx
2026-07-04_youtube-transcript_cdr-jitter
2026-07-04_email_career-followup
```

### Quality Checks

- Source ID is unique.
- Source path is exact.
- Source type is recorded.
- Initial status is one of `new`, `extracting`, `triaged`, `promoted`, `rejected`, `archived`, or `blocked`.

### Failure Recovery

- If metadata is missing, mark fields as unknown in prose.
- If duplicate source appears, link to the older source ID instead of creating a parallel record.

### Examples

Good:

```markdown
- Source ID: `2026-07-04_jssc-paper_fractional-n-pll`
- Path: `00_Inbox/incoming/papers/jssc_fractional_n_pll.pdf`
- Status: `new`
- Initial type: JSSC paper
```

Bad:

```markdown
- Source: paper
```

### Performance Considerations

- Use inventories for batches instead of one report per tiny item.
- Keep source records concise enough to scan.

## Stage 20: Quarantine and Safety Screen

### Purpose

Identify sources that require special handling before extraction or promotion.

### Inputs

- Registered source.
- Source metadata.
- Any user-provided sensitivity notes.

### Outputs

- Safety classification.
- Processing permission status.
- Redaction or exclusion decision.

### Decision Criteria

Classify as sensitive if it contains:

- Employer-confidential information.
- Proprietary design values.
- Internal roadmaps.
- Customer names or customer data.
- Personal health, finance, immigration, or legal information.
- Copyrighted material that should not be reproduced.
- Private email content not meant for general technical notes.

### Automation Rules

- Do not promote sensitive content into general technical notes.
- Do not copy long copyrighted passages into Markdown.
- For Reddit, preserve attribution and links when quoting; otherwise summarize.
- For emails, separate action items from private content.

### Quality Checks

- Sensitive status is recorded.
- Redaction decision is explicit.
- Generalized learning is separated from private details.

### Failure Recovery

- If sensitivity is uncertain, keep the source in `00_Inbox/incoming/` and mark processing as blocked.
- If sensitive content was accidentally promoted, flag high severity and remove or generalize with user approval.

### Examples

Good:

```markdown
This work note contains project-specific values. Promote only the general LDO stability mechanism; do not promote circuit values or internal project names.
```

Bad:

```markdown
Copy internal design details into a reusable PLL note.
```

### Performance Considerations

- Run safety screening before expensive extraction.
- Batch-screen email threads and screenshots to avoid repeated privacy review.

## Stage 30: Normalize and Extract

### Purpose

Convert source material into machine-readable text and structured assets without losing the original.

### Inputs

- Registered and screened source.
- Raw file or source packet.

### Outputs

- Extracted text.
- Extracted images or figures when appropriate.
- OCR output for image-based sources.
- Conversion notes.
- Extraction quality status.

### Decision Criteria

Choose extraction method by source type:

- Text PDF: extract text directly.
- Scanned PDF, image, screenshot: OCR.
- Word document: convert to Markdown or plain text.
- Slides: extract slide text and preserve slide numbers.
- YouTube transcript: normalize timestamps and speaker markers.
- Reddit: preserve thread hierarchy when relevant.
- Email: preserve sender/date/subject metadata and extract content.
- Patent: preserve claims, abstract, figures, assignee, inventors, and dates.

### Automation Rules

- Preserve page, slide, timestamp, paragraph, or claim references.
- Keep original source unchanged.
- Store extracted text separately from durable notes.
- Do not infer missing figure content from low-quality OCR.

### Quality Checks

- Extraction completeness is recorded.
- Page or timestamp references are retained when useful.
- OCR confidence is noted when low.
- Tables and equations are checked manually before promotion.

### Failure Recovery

- If OCR fails, keep image assets and mark extraction as partial.
- If math extraction is corrupted, retype only necessary formulas with source reference.
- If tables are mangled, summarize manually and avoid false precision.

### Examples

Good:

```markdown
Page 4 figure summary: architecture diagram shows CTLE -> ADC -> DSP equalizer. OCR quality high for captions, low for axis labels.
```

Bad:

```markdown
OCR text from a plot is treated as exact measurement data.
```

### Performance Considerations

- Cache extracted text for large PDFs.
- Process long books chapter by chapter.
- Split long transcript files by timestamp or topic.
- Avoid full OCR of image-heavy documents when only a few figures matter.

## Stage 40: Metadata and Provenance Enrichment

### Purpose

Attach enough metadata to make the source retrievable, citable, and auditable.

### Inputs

- Source record.
- Extracted text.
- Raw metadata from file, URL, citation, or user.

### Outputs

- Enriched metadata record.
- Citation information when applicable.
- Source quality rating.
- Provenance block for later notes.

### Decision Criteria

Capture metadata appropriate to source type:

- Books: title, author, edition, publisher, year, chapter.
- Papers: title, authors, venue, year, DOI or URL.
- Patents: patent number, inventors, assignee, filing date, publication date.
- Slides: event, speaker, organization, date.
- Blog posts: author, site, URL, publication date.
- YouTube: title, channel, URL, upload date, transcript date.
- Images/screenshots: source, date, context, visible content.
- Emails: subject, sender, date, thread context.
- Markdown notes: path, author if known, date, relationship to existing notes.

### Automation Rules

- Prefer exact metadata over inferred metadata.
- Mark unknown fields instead of inventing.
- Normalize dates as `YYYY-MM-DD` when known.
- Store URL access date for web sources.

### Quality Checks

- Source can be found again.
- Metadata confidence is clear.
- Source quality category is assigned.

### Failure Recovery

- If citation metadata is incomplete, continue with available fields and mark missing fields.
- If multiple versions exist, record version or access date.

### Examples

Good:

```markdown
Source quality: primary paper, full PDF available, citation metadata complete.
```

Bad:

```markdown
Source quality: high because the summary sounds technical.
```

### Performance Considerations

- Metadata extraction can be automated, but source quality classification requires review.
- Avoid spending time perfecting metadata for rejected sources beyond traceability needs.

## Stage 50: Triage and Classification

### Purpose

Decide whether the source should be promoted, summarized, deferred, rejected, or archived.

### Inputs

- Source record.
- Extracted text.
- Metadata.
- Safety screen result.

### Outputs

- Processing decision.
- Destination candidates.
- Source priority.
- Required workflow documents.

### Decision Criteria

Promote if:

- It supports core technical domains.
- It contains reusable mechanisms, equations, design tradeoffs, or references.
- It improves existing canonical notes.
- It supports interview or career knowledge with technical grounding.

Defer if:

- It is relevant but too large for current processing.
- It needs external verification.
- It requires user context.

Reject if:

- It is irrelevant.
- It is low-quality and adds no useful source trail.
- It duplicates a better source.
- It is unsafe to process.

### Automation Rules

- Assign domain tags.
- Suggest destination folder using [knowledge_tree.md](knowledge_tree.md).
- Suggest template contract using [core/template_contracts.md](core/template_contracts.md).
- Never auto-promote exact technical claims without review.

### Quality Checks

- Decision is recorded.
- Destination candidate is canonical.
- Rejection reason is explicit.
- Sensitive status remains visible.

### Failure Recovery

- If classification is uncertain, create a short triage note and leave source in `00_Inbox/incoming/`.
- If a source was misclassified, re-register with corrected type and keep the history.

### Examples

Good:

```markdown
Decision: promote paper summary to `Papers_Books/`; extract ADC jitter concept to `ADC/sampling_jitter_adc.md`.
```

Bad:

```markdown
Decision: paste the whole paper summary into the ADC note.
```

### Performance Considerations

- Triage large batches before deep extraction.
- Reject low-value sources early.
- Prioritize high-authority sources such as ISSCC/JSSC papers over generic blog summaries when time is limited.

## Stage 60: Claim and Knowledge Extraction

### Purpose

Extract reusable knowledge units from the source while preserving source boundaries.

### Inputs

- Triaged source.
- Extracted text.
- Metadata.
- Destination candidates.

### Outputs

- Claim list.
- Equation list.
- Figure/table summaries.
- Design lessons.
- Open questions.
- Candidate note updates.

### Decision Criteria

Extract:

- Mechanisms.
- Architecture descriptions.
- Equations with assumptions.
- Metrics with units and conditions.
- Design tradeoffs.
- Failure modes.
- Debug methods.
- Interview-relevant explanations.
- Bibliographic references.

Do not extract:

- Long copyrighted text.
- Unsupported speculation.
- Low-value filler.
- Claims without enough context to be useful.

### Automation Rules

- Label each extracted item as fact, claim, equation, metric, interpretation, or open question.
- Preserve page, slide, claim, timestamp, or URL anchor when available.
- Mark AI-derived synthesis separately from source-derived claims.

### Quality Checks

- Extracted claims are traceable.
- Metrics include units and conditions.
- Equations follow [formula_style.md](formula_style.md).
- Interpretations are not mislabeled as source claims.

### Failure Recovery

- If a claim is plausible but unverified, keep it in open questions.
- If an extracted metric lacks conditions, do not promote it as a durable requirement.
- If source text is ambiguous, summarize the ambiguity.

### Examples

Good:

```markdown
Claim: The receiver uses ADC sampling before DSP equalization.
Source location: paper page 2 architecture figure.
Interpretation: This supports the vault's ADC-based PAM4 receiver topic.
```

Bad:

```markdown
Claim: All future SerDes receivers should use ADCs.
```

### Performance Considerations

- Extract by section or chapter for long sources.
- Use claim tables for papers and patents.
- Use timestamp chunks for transcripts.
- Use figure-first extraction for slide decks and screenshots.

## Stage 70: Synthesis and Promotion

### Purpose

Convert extracted knowledge into durable vault notes and hand off each output to lifecycle, quality, gap, roadmap, and continuous-improvement evaluation.

### Inputs

- Extracted claims and lessons.
- Candidate destination notes.
- Template contract.

### Outputs

- Updated canonical notes.
- New source-specific notes when needed.
- Source/provenance sections.
- Open questions.
- Lifecycle decisions under [knowledge_evolution.md](knowledge_evolution.md).
- Quality evaluation under [quality_score.md](quality_score.md).
- Gap records under [knowledge_gap.md](knowledge_gap.md) when needed.
- Roadmap decisions under [research_roadmap.md](research_roadmap.md) when needed.
- CKI candidates under [continuous_knowledge_improvement.md](continuous_knowledge_improvement.md), including duplicate, link, formula, engineering-insight, interview-question, reading-recommendation, and density opportunities.

### Decision Criteria

Update an existing note when:

- The topic already has a canonical note.
- The new source adds evidence, correction, or nuance.

Create a new note when:

- The topic is distinct and durable.
- The source itself deserves a paper, book, patent, or report note.
- The material is a design note or interview note with a separate retrieval purpose.

### Automation Rules

- Use [core/template_contracts.md](core/template_contracts.md) for note shape.
- Use [merge_knowledge.md](merge_knowledge.md) if overlap is found.
- Use [expand_note.md](expand_note.md) if a destination note is too thin.
- Keep source-specific notes separate from general topic notes.
- Do not skip lifecycle, quality, gap, roadmap, or CKI stages after promoting durable knowledge.

### Quality Checks

- Destination is canonical.
- Source history is recorded.
- Claims are not overgeneralized.
- Technical uncertainty remains visible.
- Links are added where useful.
- Lifecycle state is assigned.
- Quality score or reason for not scoring is recorded.
- Gaps are opened, closed, or explicitly absent.
- Roadmap impact is evaluated.
- CKI opportunities are applied, triaged, or explicitly absent.

### Failure Recovery

- If promotion would require a major rewrite, create a staged plan or source report first.
- If source confidence is low, create a seed note or open question rather than a mature note.
- If a conflict appears, use [merge_knowledge.md](merge_knowledge.md) or [review.md](review.md).

### Examples

Good:

```markdown
Paper-specific result stays in `Papers_Books/`.
Reusable sampling-jitter explanation updates `ADC/sampling_jitter_adc.md`.
```

Bad:

```markdown
The whole paper becomes a generic ADC note.
```

### Performance Considerations

- Promote high-value claims first.
- Avoid expanding every related note in one pass.
- Use staged promotion for books and long transcripts.

## Stage 80: Review, Continuous Improvement, Integration, and Indexing

### Purpose

Ensure promoted knowledge is accurate, linked, indexed, scored, gap-aware, roadmap-aware, continuously improved, and maintainable before archive and report.

### Inputs

- Updated notes.
- Source records.
- Extracted claims.

### Outputs

- Reviewed notes.
- Related links.
- Index updates.
- Quality score records.
- Gap records.
- Roadmap updates.
- CKI actions and metrics.
- Ingest report.
- Verification status.

### Decision Criteria

Review is required when:

- Exact technical claims were promoted.
- Standards-sensitive content was added.
- A note became canonical.
- Multiple sources were merged.
- Source quality is mixed.

### Automation Rules

- Run link checks when links are added.
- Scan for source sections in promoted notes.
- Update master indexes only for important durable notes.
- Run [continuous_knowledge_improvement.md](continuous_knowledge_improvement.md) for every substantial source batch before archive.
- Generate ingest reports for substantial batches.

### Quality Checks

- Apply [review.md](review.md).
- Apply [build_links.md](build_links.md).
- Apply [indexing.md](indexing.md).
- Apply [knowledge_evolution.md](knowledge_evolution.md).
- Apply [quality_score.md](quality_score.md).
- Apply [knowledge_gap.md](knowledge_gap.md).
- Apply [research_roadmap.md](research_roadmap.md).
- Apply [continuous_knowledge_improvement.md](continuous_knowledge_improvement.md).
- Apply [core/quality_standards.md](core/quality_standards.md).

### Failure Recovery

- If review finds high-severity issues, stop promotion and fix or revert only the agent's own changes.
- If links are broken, repair or remove them.
- If index updates become noisy, keep only canonical entries.

### Examples

Good:

```markdown
The new JSSC paper note links to ADC-based receiver, sampling jitter, and TI-SAR calibration notes. The master index includes only the canonical topic note, not every intermediate extraction file.
```

Bad:

```markdown
Every extracted fragment is added to the master index.
```

### Performance Considerations

- Review high-impact notes first.
- Link checking can be batch-run after multiple notes are updated.
- Avoid re-indexing the whole vault for a single small note.

## Stage 90: Archive and Retention

### Purpose

Move processed source packets out of active inbox state while preserving traceability.

### Inputs

- Source record.
- Extracted text.
- Ingest report.
- CKI status and unresolved improvement risks.
- Updated durable notes.
- Review status.

### Outputs

- Archived source packet under `90_Archive/`.
- Archive manifest.
- Remaining links from durable notes to source record or archive path.
- Cleaned active inbox state.

### Decision Criteria

Archive as `processed` when:

- Source was reviewed.
- Useful content was promoted or intentionally not promoted.
- Continuous improvement status was recorded.
- Ingest report records the decision.

Archive as `rejected` when:

- Source is irrelevant, low-value, duplicate, or unusable.

Archive as `superseded` when:

- A better version or primary source replaces it.

Archive as `sensitive` when:

- It must be retained but should not be promoted.

### Automation Rules

- Create archive path by year and source type.
- Preserve source ID in archive folder or manifest.
- Do not break provenance links.
- Do not delete original source unless the archive copy is verified.

### Quality Checks

- Archive path exists.
- Manifest exists for substantial sources.
- Durable notes still trace back to source.
- Inbox no longer contains active processed clutter unless intentionally retained.

### Failure Recovery

- If archive move fails, leave source in `00_Inbox/incoming/` and mark status `archive_failed`.
- If links break after archiving, repair links or preserve a source registry in the ingest report or archive manifest.
- If archive category was wrong, move between archive categories with a note in the manifest.

### Examples

Good:

```text
90_Archive/processed/2026/isscc-paper/2026-07-04_isscc-paper_adc-pam4-rx/
```

Bad:

```text
Delete the source PDF after summarizing it.
```

### Performance Considerations

- Archive completed batches together.
- Compress very large source packets only when future tooling can still access them.
- Keep manifests lightweight for small sources.

## Source-Type Adapters

### Books

- Process chapter by chapter.
- Capture edition and chapter metadata.
- Extract concepts, not long chapter summaries.
- Promote durable concepts to domain notes.
- Archive reading packets when chapter extraction is complete.

### ISSCC and JSSC Papers

- Treat as high-authority primary technical sources.
- Capture citation, architecture, metrics, figures, and measurement conditions.
- Do not generalize one paper into a universal design rule.
- Link paper notes to topic notes.

### Patents

- Capture patent number, assignee, inventors, dates, claims, figures, and jurisdiction.
- Treat claims as legal/technical positioning, not proof of silicon performance.
- Extract architecture ideas carefully and label as patent-derived.

### Conference Slides

- Preserve slide numbers.
- Treat slides as compressed and often incomplete.
- Extract architecture diagrams, terminology, and pointers to deeper sources.
- Avoid overclaiming from a single slide.

### Blog Posts and Whitepapers

- Capture author, organization, URL, date, and vendor bias.
- Treat as secondary or vendor-specific unless independently supported.
- Promote explanations only after technical screening.

### YouTube Transcripts

- Preserve URL, channel, title, upload date, transcript date, and timestamps.
- Chunk by topic and timestamp.
- Treat as informal source unless speaker authority and content are strong.

### PDFs, Images, and Screenshots

- Preserve original files.
- OCR only as an extracted derivative.
- Record OCR quality.
- Do not infer exact values from unreadable plots.

### Reddit Discussions

- Preserve URL, subreddit, date, and thread context.
- Treat as anecdotal unless backed by external sources.
- Quote only when necessary and attribute clearly.
- Extract practical questions, terminology, and leads rather than treating comments as authority.

### Emails

- Preserve sender, date, subject, and thread context.
- Separate private content from reusable knowledge.
- Promote action items or generalized lessons only.

### Word Documents

- Convert to Markdown or text while preserving headings.
- Preserve original `.docx`.
- Record conversion quality and missing embedded assets.

### Markdown Notes

- Preserve original path.
- Check whether it is source, draft, durable note, or duplicate.
- Promote by merge or expansion rather than blind copy.

## Pipeline Quality Gate

Before a source leaves active processing:

- Source is registered.
- Safety screen is complete.
- Extraction quality is known.
- Metadata is sufficient for retrieval.
- Triage decision is recorded.
- Promoted claims are traceable.
- Durable notes are linked and source-aware.
- Review status is recorded.
- CKI status is recorded.
- Archive category is correct.

## Automation Roadmap

Recommended future tools:

- Source registry generator.
- File-type classifier.
- OCR and text extraction runner.
- Metadata extractor for DOI, patents, URLs, and PDFs.
- Claim extraction table generator.
- Link checker.
- Frontmatter validator.
- Archive manifest generator.
- Inbox dashboard showing source status by stage.

Automation must not silently promote claims, delete source material, or override confidentiality screening.
