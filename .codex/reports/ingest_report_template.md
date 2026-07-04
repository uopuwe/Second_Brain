# Ingest Report Template

> Compatibility notice: the canonical report contract is now [../core/template_contracts.md](../core/template_contracts.md). This file is retained for existing path compatibility. Future agents must follow the core contract and ignore any duplicated legacy guidance below when it conflicts with the core operating system.

## Purpose

Use this report after processing a substantial source batch.
The report records what was ingested, what was promoted, what remained raw, what was rejected from durable notes, and what still needs verification.

Reports are part of vault memory.
They help future Codex sessions understand why notes changed.

## Recommended Filename

Use:

```text
ingest_report_YYYY-MM-DD.md
```

For a named batch:

```text
ingest_report_batch2_serdes_pcie_pll_cdr_adc_2026-07-01.md
```

## Recommended Location

Place reports near the relevant source:

```text
00_Inbox/conversation_inventory/
```

or inside the batch folder:

```text
00_Inbox/manual_batches/<batch_name>/ingest_report_YYYY-MM-DD.md
```

Use one location consistently for a batch.

## Report Frontmatter

```yaml
---
title: "Ingest Report: Batch Name"
domain: "Vault_Maintenance"
tags:
  - Ingest
  - Report
status: "active"
created: "2026-07-03"
updated: "2026-07-03"
source: "Ingest workflow"
confidence: "high"
---
```

## Summary

Example:

```markdown
## Summary

This ingest processed a source packet covering PCIe 7.0 clocking, PLL/CDR fundamentals, ADC-based PAM4 receivers, sampling jitter, and LDO power integrity. Durable material was promoted into existing technical notes where possible. Exact standards-related numbers were not promoted unless source-backed.
```

## Source Material

List all inputs.

```markdown
## Source Material

- `00_Inbox/manual_batches/batch2_serdes_pcie_pll_cdr_adc_2026-07-01/source_packet.md`
- `00_Inbox/processed_by_chatgpt/batch2_serdes_pcie_pll_cdr_adc_2026-07-01.md`
```

For each source, record:

- Type.
- Date if known.
- Processing status.
- Main domains.

Example:

```markdown
### Source: `source_packet.md`

- Type: AI conversation packet.
- Date: 2026-07-01.
- Status: processed for durable concepts.
- Domains: PCIe 7.0, SerDes, PLL, CDR, ADC, LDO.
```

## Destination Notes Changed

List changed durable notes.

```markdown
## Destination Notes Changed

- `01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_phase_noise_jitter.md`
  - Added integration-bandwidth caution.
  - Added system impact on SerDes clocking.

- `01_AnalogIC_SerDes/ADC/adc_based_receiver.md`
  - Added ADC-based PAM4 receiver tradeoff section.
  - Linked sampling jitter and DSP equalization notes.
```

## New Notes Created

```markdown
## New Notes Created

- `01_AnalogIC_SerDes/PLL_CDR_Clocking/cdr_jitter_tolerance.md`
  - Purpose: consolidate CDR jitter transfer and tolerance concepts.
  - Confidence: medium.
  - Source: AI-assisted source packet plus existing vault notes.
```

If no new notes were created:

```markdown
## New Notes Created

No new durable notes were created. Existing notes were updated instead.
```

## Content Promoted

Use categories.

```markdown
## Content Promoted

### Concepts

- PAM4 reduces vertical margin compared with binary signaling for the same full-scale swing.
- ADC-based RX enables flexible DSP equalization but increases sensitivity to sampling jitter and ADC calibration.

### Equations

- Phase error to RMS time jitter relationship.
- Sampling jitter SNR approximation for sinusoidal inputs.

### Tradeoffs

- CDR loop bandwidth tracking versus filtering.
- LDO PSRR versus output noise and transient behavior.

### Interview Material

- Short answer for why LDO noise matters to PLL jitter.
- Short answer for why ADC-based receivers are used in modern PAM4 links.
```

## Content Left Raw

Explain what was not promoted but preserved.

```markdown
## Content Left Raw

- Conversational filler and repeated explanations were left in the source packet.
- Unsourced exact PCIe compliance values were not promoted.
- Broad career comments were left in the inbox until they can be routed into a study plan or interview note.
```

## Content Not Promoted

Be explicit.

```markdown
## Content Not Promoted

- Claims that sounded plausible but lacked source support.
- Duplicate explanations already covered in canonical notes.
- Overly generic interview phrasing without technical mechanism.
```

## Technical Uncertainties

List unresolved technical uncertainty.

```markdown
## Technical Uncertainties

- Exact public PCIe 7.0 clocking and jitter requirements need current source verification.
- The most relevant ADC-based RX paper list should be refreshed from primary sources.
- CDR jitter tolerance explanations should be checked against architecture-specific models.
```

## Confidentiality Screen

```markdown
## Confidentiality Screen

- No employer-confidential design details were promoted.
- No proprietary specification text was copied.
- Work-related learning was kept at a general technical level.
```

If sensitive content existed:

```markdown
Sensitive source content was not promoted into durable technical notes. The source remains in its original location for user-controlled handling.
```

## Links Added or Updated

```markdown
## Links Added or Updated

- Added links from `analog_ic_serdes_master_index.md` to updated PLL/CDR notes.
- Added related links between ADC sampling jitter and ADC-based receiver notes.
- Added interview-note links to deeper LDO and PLL references.
```

## Index Updates

```markdown
## Index Updates

- Updated `01_AnalogIC_SerDes/analog_ic_serdes_master_index.md`.
- Added read-first ordering for PLL/CDR notes.
```

If no index was updated, state why:

```markdown
No index update was needed because no major durable note was created or reclassified.
```

## Verification Performed

```markdown
## Verification Performed

- Checked that destination files exist.
- Checked relevant related notes for overlap.
- Checked that links use correct relative paths.
- Did not externally verify current PCIe standards details in this ingest.
```

## Suggested Next Actions

Use concrete actions.

```markdown
## Suggested Next Actions

- Review PCIe 7.0 public materials for current clocking terminology and source-backed wording.
- Expand `cdr_jitter_tolerance.md` with architecture-specific examples.
- Add a paper note for one ADC-based PAM4 receiver paper and link it to ADC/DSP notes.
```

These are recommendations, not unfinished report content.

## Final Status

```markdown
## Final Status

The source batch has been processed into durable vault notes with provenance preserved. Remaining uncertainty is explicitly listed above.
```

## Report Completion Checklist

Before finishing:

- Source paths are listed.
- Destination notes are listed.
- New notes are listed.
- Promoted content is summarized.
- Raw or rejected content is explained.
- Technical uncertainty is explicit.
- Confidentiality screen is included.
- Links and indexes are documented.
- Verification limits are clear.

## Expert Rationale for This Report

An ingest report is the audit trail for knowledge transformation.
It records how raw source material became durable notes.

Without ingest reports, future agents may see changed notes but not understand:

- Which source batch triggered the changes.
- Which claims were promoted.
- Which claims were rejected.
- Which uncertainties remain.
- Whether confidentiality was screened.
- Whether indexes and links were updated.

For a senior engineer, this is similar to a lab or design-review record.
For a future AI agent, it prevents repeating the same ingest work and preserves source-to-note traceability.

## Why Each Section Exists

### Source Material

Reason:
The report must identify exactly what was processed.

### Destination Notes Changed

Reason:
Future reviewers need to know which durable notes were affected.

### Content Promoted

Reason:
Promotion is the main knowledge transformation.
This section explains what became part of the vault.

### Content Left Raw or Not Promoted

Reason:
Not promoting content is an engineering decision.
The report should explain why.

### Technical Uncertainties

Reason:
Uncertainty should remain visible after ingestion.

### Verification Performed

Reason:
The report must not imply checks that did not happen.

## Best Practices

- Write the report immediately after substantial ingest.
- Use exact source paths.
- List destination notes clearly.
- Separate promoted, left raw, and rejected content.
- Record standards-sensitive uncertainty.
- Record confidentiality screening.
- Mention link and index updates.
- State verification limits.
- Keep the report concise but complete.
- Avoid using the report as a dumping ground for raw source text.

## Bad Ingest Report Example

```markdown
Processed the SerDes batch. Updated notes. Some things need review.
```

Why this is bad:

- No source path.
- No destination files.
- No promoted content.
- No uncertainty.
- No verification details.

## Good Ingest Report Example

```markdown
## Source Material

- `00_Inbox/manual_batches/serdes_pcie_clocking/source_packet.md`

## Destination Notes Changed

- `01_AnalogIC_SerDes/PLL_CDR_Clocking/pcie7_clocking_notes.md`
- `01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_phase_noise_jitter.md`

## Content Promoted

- Public-level PCIe 7.0 PAM4 clocking implications.
- Phase-noise integration caveat.
- CDR bandwidth tradeoff language.

## Technical Uncertainties

- Exact PCIe compliance values were not externally verified.
```

## Engineering Examples

### ADC Paper Ingest Report

Promoted:

- ADC-based receiver architecture summary.
- TI-ADC mismatch categories.
- Sampling jitter limitations.

Left raw:

- Full paper text.
- Figure captions.
- Exact comparison table until verified.

Uncertainty:

- Whether reported BER condition maps to PCIe compliance use.

### LDO Debug Ingest Report

Promoted:

- General supply-noise-to-jitter mechanism.
- PSRR versus output-noise distinction.
- Failure mode checklist.

Not promoted:

- Proprietary implementation details.
- Internal project identifiers.
- Exact circuit values.

## Workflow for Writing an Ingest Report

1. List source files.
2. Identify source type and domains.
3. List destination notes changed.
4. List new notes created.
5. Summarize promoted content by category.
6. Summarize raw or rejected content.
7. Record technical uncertainties.
8. Record confidentiality screening.
9. Record links and index updates.
10. Record verification performed.
11. Add suggested next actions.
12. State final status.

## Edge Cases

### No Content Was Promoted

Say so clearly.
This is a valid report outcome.

### Source Was Sensitive

Record that sensitive details were not promoted.
Do not repeat the sensitive details in the report.

### Destination Notes Were Not Changed

Explain whether the source was only inventoried, rejected, or deferred.

### External Verification Was Not Available

State that exact external facts were not verified.

### Multiple Batches Were Processed

Either create one report per batch or a consolidated report with clear source grouping.

## Quality Checklist

- Source paths are exact.
- Destination paths are exact.
- Promoted content is categorized.
- Unpromoted content is explained.
- Technical uncertainty is visible.
- Confidentiality screen is present.
- Link/index updates are recorded.
- Verification limits are explicit.
- Suggested next actions are concrete.
- Report can stand alone months later.

## Automation Opportunities

Future tools could:

- Generate changed-file lists from Git.
- Populate source paths from ingest commands.
- Generate report skeletons.
- Detect destination notes modified during ingest.
- Extract link/index updates.
- Flag missing uncertainty sections.
- Build source-to-note traceability maps.

Automation should not decide which technical claims were valid.
The report still requires engineering judgment.

## Future Extension Ideas

- Add machine-readable report metadata.
- Add an ingest dashboard.
- Add batch status tracking.
- Add source confidence scoring.
- Add promotion statistics by domain.
- Add automatic follow-up issue generation.
- Add periodic review of unresolved uncertainties.

## Self-Contained Summary

An ingest report records how source material was processed into vault knowledge.
It should preserve traceability from raw source to destination notes, record what was promoted or rejected, identify uncertainty, document confidentiality screening, and make future maintenance easier.
