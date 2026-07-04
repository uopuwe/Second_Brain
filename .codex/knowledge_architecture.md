# Knowledge Architecture

## Purpose

This document defines the permanent knowledge architecture for this repository.
It is designed to scale beyond 100,000 notes without becoming difficult to maintain.

It defines:

- Folder hierarchy.
- Topic hierarchy.
- Knowledge tree.
- Tagging system.
- Index pages.
- Maps of Content.
- Cross-link strategy.
- Permanent note strategy.
- Reference note strategy.
- Atomic note strategy.
- Long-form handbook strategy.
- Versioning strategy.
- Duplicate detection strategy.
- Knowledge growth strategy.

Related operating documents:

- [AGENTS.md](AGENTS.md)
- [knowledge_tree.md](knowledge_tree.md)
- [knowledge_ingestion_pipeline.md](knowledge_ingestion_pipeline.md)
- [indexing.md](indexing.md)
- [build_links.md](build_links.md)
- [core/quality_standards.md](core/quality_standards.md)

## Architecture Principles

### Principle 1: Stable Top-Level Folders

The top-level folder structure must change rarely.
At 100,000 notes, folder churn is expensive because it breaks links, indexes, habits, and automation.

Top-level folders represent lifecycle and domain, not temporary projects.

### Principle 2: Lifecycle Before Topic

The vault separates source lifecycle from durable knowledge.

Source material moves:

```text
00_Inbox -> processing -> durable notes -> 90_Archive
```

Durable notes live in canonical domain folders.
Archived source packets remain traceable.

### Principle 3: Indexes and MOCs Are Navigation Infrastructure

Indexes answer "what exists?"
Maps of Content answer "how should I think through this area?"

Both are required at scale.

### Principle 4: Tags Are Metadata, Not Structure

Folders define ownership.
Links define relationships.
MOCs define learning paths.
Tags define filters and automation.

Tags must never become the only way to find knowledge.

### Principle 5: Atomic Notes and Handbooks Coexist

Atomic notes preserve precise reusable ideas.
Long-form handbooks synthesize many atomic notes into coherent explanations.

One does not replace the other.

### Principle 6: Source Notes Are Not Permanent Notes

Reference notes summarize or annotate a source.
Permanent notes express durable understanding in the vault's own structure.

Do not confuse paper summaries with canonical technical explanations.

## Top-Level Folder Hierarchy

Canonical top-level hierarchy:

```text
Second_Brain/
  00_Inbox/
  01_AnalogIC_SerDes/
  02_Synopsys_Work/
  03_Investing/
  04_Canada_Life/
  05_Health_Medical/
  06_Other_Affairs/
  70_Indexes/
  80_MOCs/
  90_Archive/
  99_Templates/
  .codex/
  export_data/
  tools/
```

Existing top-level folders remain valid.
`70_Indexes/` and `80_MOCs/` are the scalable navigation layer.
Create them when maintaining vault-wide navigation.

## Lifecycle Folders

### `00_Inbox/`

Purpose:
Unprocessed or semi-processed source material.

Contains:

- Raw chat exports.
- Manual batches.
- Extracted source packets.
- Conversation inventories.
- Temporary triage notes.

Rules:

- Do not store final technical knowledge here.
- Do not delete source packets after promotion.
- Use [knowledge_ingestion_pipeline.md](knowledge_ingestion_pipeline.md) for processing.

### `70_Indexes/`

Purpose:
Curated inventory pages that answer "what exists?"

Examples:

```text
70_Indexes/
  master_index.md
  analog_ic_serdes_index.md
  source_index.md
  paper_index.md
  patent_index.md
  interview_index.md
  python_tools_index.md
```

Rules:

- Index pages should be concise.
- Prefer canonical notes.
- Include status and short descriptions.
- Do not list every atomic note if a MOC or folder index is better.

### `80_MOCs/`

Purpose:
Maps of Content that answer "how do these ideas connect?"

Examples:

```text
80_MOCs/
  serdes_moc.md
  pcie6_pcie7_moc.md
  pll_cdr_clocking_moc.md
  adc_based_receiver_moc.md
  ldo_bandgap_power_moc.md
  signal_integrity_moc.md
  interview_prep_moc.md
```

Rules:

- MOCs are curated conceptual maps, not file dumps.
- MOCs should include learning paths, concept clusters, and canonical references.
- MOCs should link to handbooks, atomic notes, and source indexes.

### `90_Archive/`

Purpose:
Processed, rejected, superseded, or sensitive source packets.

Rules:

- Archive source packets only after status is recorded.
- Preserve provenance.
- Do not archive durable notes merely because they are old.

## Domain Folder Hierarchy

Canonical technical domain:

```text
01_AnalogIC_SerDes/
  SerDes/
  SerDes_RX/
  PLL_CDR_Clocking/
  ADC/
  ADC_TI_SAR/
  DAC/
  DSP_Equalization/
  Signal_Integrity/
  LDO_Bandgap/
  Papers_Books/
  Patents/
  Standards/
  Interview_QA/
  Study_Plans/
  Handbooks/
```

Existing folders remain valid.
New folders should be created only when the volume or retrieval pattern justifies them.

## Topic Hierarchy

### Level 0: Repository Domains

- Analog IC / SerDes.
- Work and career.
- Investing.
- Canada life.
- Health and medical.
- Other affairs.

### Level 1: Technical Pillars

For `01_AnalogIC_SerDes/`:

- SerDes architecture.
- PCIe 6.0 / PCIe 7.0.
- PLL / CDR / clocking.
- ADC / TI-SAR / ADC-based RX.
- DAC.
- DSP and equalization.
- Signal integrity.
- LDO / bandgap / power integrity.
- Papers, books, patents, standards.
- Interview and career technical preparation.

### Level 2: Subdomains

Examples:

```text
PLL / CDR / Clocking
  PLL fundamentals
  Phase noise and jitter
  Clock distribution
  CDR loop behavior
  Jitter transfer
  Jitter tolerance
  Supply-induced jitter

ADC / ADC-Based RX
  Sampling theory
  Aperture jitter
  ENOB / SNDR / SFDR
  TI-SAR mismatch
  Background calibration
  ADC-based PAM4 receiver

SerDes
  TX architecture
  RX architecture
  PAM4 signaling
  Link training
  Equalization
  BER / bathtub / eye diagrams
```

### Level 3: Atomic Concepts

Examples:

- `phase_noise_integration_bandwidth.md`
- `pam4_vertical_eye_margin.md`
- `cdr_transition_density.md`
- `ldo_psrr_frequency_dependence.md`
- `ti_adc_skew_mismatch.md`

Atomic notes should be small enough to represent one reusable concept, but large enough to be useful.

## Knowledge Tree

The knowledge tree uses four note types:

```text
Source notes
  -> Reference notes
    -> Atomic permanent notes
      -> MOCs
        -> Long-form handbooks
```

### Source Notes

Raw or extracted source material.
Usually lives in `00_Inbox/`, `Papers_Books/`, `Patents/`, or `90_Archive/`.

### Reference Notes

A structured summary of one source.

Examples:

- One ISSCC paper note.
- One JSSC paper note.
- One patent note.
- One book chapter note.
- One YouTube transcript note.

### Atomic Permanent Notes

Durable notes in the user's own words.
They are not tied to one source.

### MOCs

Curated maps that organize many notes.

### Handbooks

Long-form synthesized documents for major areas.

Examples:

- `Handbooks/serdes_receiver_handbook.md`
- `Handbooks/pll_cdr_clocking_handbook.md`
- `Handbooks/adc_based_pam4_receiver_handbook.md`

## Tagging System

Tags are controlled metadata.
Use stable tags with consistent capitalization.

### Required Tag Classes

Use only when applicable:

```yaml
tags:
  - domain/analog_ic_serdes
  - topic/pll
  - type/permanent
  - status/active
  - source/jssc
  - confidence/medium
```

### Tag Namespaces

#### `domain/`

- `domain/analog_ic_serdes`
- `domain/work`
- `domain/career`
- `domain/investing`
- `domain/life_admin`
- `domain/health`

#### `topic/`

- `topic/serdes`
- `topic/pcie6`
- `topic/pcie7`
- `topic/pam4`
- `topic/pll`
- `topic/cdr`
- `topic/clocking`
- `topic/phase_noise`
- `topic/jitter`
- `topic/adc`
- `topic/dac`
- `topic/dsp`
- `topic/equalization`
- `topic/signal_integrity`
- `topic/ldo`
- `topic/bandgap`
- `topic/python`

#### `type/`

- `type/source`
- `type/reference`
- `type/permanent`
- `type/atomic`
- `type/moc`
- `type/index`
- `type/handbook`
- `type/interview`
- `type/design_note`
- `type/report`

#### `status/`

- `status/seed`
- `status/active`
- `status/mature`
- `status/needs_review`
- `status/archived`
- `status/superseded`

#### `source/`

- `source/book`
- `source/isscc`
- `source/jssc`
- `source/patent`
- `source/slides`
- `source/blog`
- `source/youtube`
- `source/whitepaper`
- `source/reddit`
- `source/email`
- `source/ai_summary`
- `source/user_note`

#### `confidence/`

- `confidence/low`
- `confidence/medium`
- `confidence/high`

### Tagging Rules

Mandatory:

- Use `type/` for note class.
- Use `status/` for lifecycle.
- Use at least one `topic/` for technical notes.

Recommended:

- Use one primary `domain/`.
- Use `source/` for source-derived notes.
- Use `confidence/` when claims depend on source quality.

Avoid:

- Synonyms such as `topic/phase-noise`, `topic/phase_noise`, and `topic/phasenoise`.
- Personal temporary tags such as `important`, `readlater`, or `misc`.
- More than 8 tags on a normal note.

## Index Pages

Index pages are inventory documents.
They should scale by hierarchy.

### Required Indexes at Scale

```text
70_Indexes/master_index.md
70_Indexes/analog_ic_serdes_index.md
70_Indexes/source_index.md
70_Indexes/paper_index.md
70_Indexes/patent_index.md
70_Indexes/standards_index.md
70_Indexes/interview_index.md
70_Indexes/handbook_index.md
```

### Index Entry Format

```markdown
- [PLL phase noise and jitter](../01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_phase_noise_jitter.md)
  - Type: permanent
  - Status: active
  - Topics: PLL, phase noise, jitter
  - Summary: Phase-noise integration, RMS jitter conversion, and SerDes clocking implications.
```

### Index Rules

- Index canonical notes.
- Do not index every source fragment.
- Keep index entries short.
- Prefer folder-level or topic-level indexes when a list grows too long.
- Use MOCs for conceptual navigation.

## Maps of Content

MOCs are guided maps through concepts.
They should be human-readable and AI-friendly.

### MOC Structure

```markdown
# PLL / CDR / Clocking MOC

## Purpose

## Read First

## Concept Map

## Core Permanent Notes

## Reference Notes

## Design Questions

## Interview Path

## Open Questions

## Related MOCs
```

### MOC Rules

- A MOC should explain why links matter.
- A MOC should include read-first paths.
- A MOC should point to handbooks when available.
- A MOC should not become a full handbook.

## Cross-Link Strategy

### Link Types

- Parent: atomic note to MOC or index.
- Child: MOC to atomic note.
- Sibling: closely related concepts.
- Source: permanent note to reference note.
- Application: technical note to design note or interview note.
- Handbook: permanent note to long-form synthesis.

### Link Rules

- Link canonical notes.
- Use descriptive link text.
- Do not link every repeated keyword.
- Add source links when a claim depends on source material.
- Add MOC links for important permanent notes.
- Avoid broken future links; use inline code for planned notes.

### Minimum Links by Note Type

| Note Type | Minimum Links |
| --- | --- |
| Atomic permanent note | One MOC or parent topic link, one related note if applicable |
| Reference note | Source citation, related topic note |
| MOC | Core notes, related MOCs, handbook if available |
| Handbook | MOC, major atomic notes, source indexes |
| Interview note | Deep technical references |

## Permanent Note Strategy

Permanent notes are durable, source-aware explanations in the vault's own words.

### Permanent Note Requirements

- One clear concept or tightly scoped topic.
- User's own synthesis.
- Source/provenance section.
- Links to related concepts.
- Status and confidence metadata.
- No long copied text.

### Good Permanent Note

```markdown
# PAM4 Vertical Eye Margin

Explains why PAM4 has smaller adjacent level spacing than binary signaling for the same full-scale swing and how that affects noise, linearity, equalization, and sampling timing.
```

### Bad Permanent Note

```markdown
# PAM4

Mixed paper quotes, transcript fragments, interview answers, and copied diagrams.
```

## Reference Note Strategy

Reference notes summarize one source.

### Reference Note Requirements

- Citation or source metadata.
- Source type.
- Summary.
- Key claims.
- Metrics with conditions.
- Relevance to vault.
- Links to permanent notes.
- Claims not yet verified.

### Source-Specific Rules

- ISSCC/JSSC papers: capture architecture, measurements, process, and conditions.
- Patents: capture claims and figures, but do not treat as measured proof.
- Blog posts: label author and bias.
- Reddit: treat as anecdotal unless externally supported.
- YouTube: preserve timestamps.

## Atomic Note Strategy

Atomic notes are small permanent notes for one concept.

### Atomic Note Requirements

- One idea.
- Clear title.
- Minimal but sufficient context.
- Links to parent MOC and related notes.
- Source/provenance if derived.

### Atomic Note Size

Good range:

- 300 to 1,500 words for most concepts.
- Longer only if equations, examples, and caveats require it.

Split when:

- The note has multiple independent concepts.
- It mixes source summary and synthesis.
- It mixes interview answer and technical reference.

## Long-Form Handbook Strategy

Handbooks synthesize mature knowledge into coherent chapters.

### Handbook Purpose

Use handbooks for:

- SerDes architecture overview.
- PLL/CDR/clocking mastery.
- ADC-based PAM4 receiver study.
- LDO/bandgap/power integrity.
- Interview preparation path.

### Handbook Rules

- Handbooks cite and link permanent notes.
- Handbooks should not be the only location for atomic concepts.
- Handbooks should be periodically rebuilt from mature notes.
- Handbooks may include narrative, diagrams, examples, and study paths.

### Handbook Structure

```markdown
# Handbook Title

## Scope
## Prerequisites
## Chapter Map
## Core Concepts
## Design Tradeoffs
## Worked Examples
## Failure Modes
## Interview Applications
## Source Notes
## Open Questions
```

## Versioning Strategy

### Git-Level Versioning

Use Git for file history.
Commit related architecture changes together.
Avoid massive unrelated rewrites.

### Note-Level Versioning

Use frontmatter:

```yaml
status: "active"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
version: "1.0"
```

### Semantic Meaning

- `0.x`: seed or draft note.
- `1.x`: active usable note.
- `2.x`: mature reviewed note.

### Change Log

Use change logs only for high-value handbooks, MOCs, and canonical reference notes.

```markdown
## Change Log

- 2026-07-04: Promoted to mature after source review.
```

## Duplicate Detection Strategy

### Duplicate Types

- Exact duplicate file.
- Same title, different folder.
- Same concept, different wording.
- Source note mistaken for permanent note.
- Old copy folder duplicate.
- AI-generated duplicate summary.

### Detection Signals

- Similar filenames.
- Similar H1 titles.
- Similar aliases.
- Same source citation.
- Same key equations.
- Same related links.
- Same tags and overlapping content.

### Duplicate Handling

1. Identify canonical note.
2. Compare unique content.
3. Promote missing unique content.
4. Preserve source history.
5. Redirect or mark superseded if appropriate.
6. Update indexes and MOCs.

Use [merge_knowledge.md](merge_knowledge.md) for merges.

### Automation Opportunities

- Filename similarity scan.
- H1 title scan.
- Source citation scan.
- Embedding similarity scan.
- Broken canonical-link scan.
- Duplicate tag cluster report.

## Knowledge Growth Strategy

### Growth Stages

```text
Source captured
  -> Reference note
  -> Atomic permanent note
  -> MOC integration
  -> Handbook synthesis
  -> Review and maturity upgrade
```

### Growth Rules

- New knowledge enters through the ingestion pipeline.
- Mature knowledge earns links from indexes and MOCs.
- Handbooks are built from mature notes, not raw sources.
- Duplicate prevention is part of every growth cycle.
- Review status must be visible.

### Scaling Rules for 100,000 Notes

- Use stable top-level folders.
- Use MOCs for concept navigation.
- Use indexes for inventory.
- Keep note types explicit in tags and frontmatter.
- Avoid giant folders with no indexes.
- Avoid unbounded tag creation.
- Avoid one-off filenames.
- Use automation for validation, not judgment.

### Growth Metrics

Track periodically:

- Number of notes by type.
- Number of notes by status.
- Orphan permanent notes.
- Notes without source/provenance.
- Duplicate candidates.
- Broken links.
- MOCs missing updates.
- Handbooks needing refresh.

## Frontmatter Standard

Use this expanded schema for scalable notes:

```yaml
---
title: "Readable Title"
aliases: []
domain: "AnalogIC_SerDes"
note_type: "permanent"
status: "active"
confidence: "medium"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
version: "1.0"
tags:
  - domain/analog_ic_serdes
  - topic/pll
  - type/permanent
  - status/active
  - confidence/medium
source:
  type: "jssc"
  path: ""
  citation: ""
related_mocs:
  - ""
---
```

Do not require every field for tiny notes, but canonical notes should approach this schema.

## Naming Strategy

Use lowercase snake_case for filenames.

Patterns:

```text
atomic concept: phase_noise_integration_bandwidth.md
reference note: jssc_2024_fractional_n_pll.md
MOC: pll_cdr_clocking_moc.md
handbook: pll_cdr_clocking_handbook.md
index: paper_index.md
```

Avoid:

```text
notes.md
final.md
new.md
misc.md
Untitled.md
```

## Maintenance Cadence

### Every Ingestion Batch

- Source registration.
- Promotion decision.
- Link updates.
- Archive status.

### Weekly or Per Study Cycle

- Update current MOCs.
- Review orphan notes.
- Merge duplicates.

### Monthly

- Refresh indexes.
- Review source backlog.
- Promote mature notes into handbooks.

### Quarterly

- Audit tag drift.
- Audit duplicate candidates.
- Review standards-sensitive notes.
- Update architecture if folder growth justifies changes.

## Architecture Quality Gate

Before adding new knowledge at scale:

- Does it have a note type?
- Does it belong in a canonical folder?
- Does it need a reference note, permanent note, MOC entry, or handbook section?
- Does it duplicate existing knowledge?
- Are tags controlled?
- Are source and confidence visible?
- Is it linked to a parent MOC or index?

