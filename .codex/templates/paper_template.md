# Paper Note Template

> Compatibility notice: the canonical template contract is now [../core/template_contracts.md](../core/template_contracts.md). This file is retained for existing path compatibility. Future agents must follow the core contract and ignore any duplicated legacy guidance below when it conflicts with the core operating system.

## Purpose

Use this template for technical papers, conference publications, journal articles, public standards summaries, and application notes.

The goal is to capture what the paper actually says, why it matters, and how it connects to the vault.
Do not copy large sections of copyrighted text.
Summarize in your own words.

## Recommended Frontmatter

```yaml
---
title: "Paper Title"
domain: "AnalogIC_SerDes"
tags:
  - Paper
  - SerDes
  - ADC
status: "active"
created: "2026-07-03"
updated: "2026-07-03"
source: "Paper"
confidence: "medium"
paper_type: "conference"
venue: "ISSCC"
year: "2026"
---
```

Adjust tags and metadata to match the paper.

## File Naming

Use a readable filename:

```text
isscc_2026_adc_based_pam4_receiver.md
jssc_2024_fractional_n_pll_jitter.md
pcie7_public_summary_notes.md
```

If the exact venue or year is unknown, use a descriptive topic name and record uncertainty in the note.

## Citation

Capture enough bibliographic information to find the paper again.

```markdown
## Citation

- Title:
- Authors:
- Venue:
- Year:
- DOI or URL:
- Source type: conference paper, journal paper, standard summary, vendor app note, thesis, book chapter.
- Access status: abstract only, full paper, public summary, personal notes.
```

When exact metadata is unavailable, write that clearly rather than inventing it.

## One-Sentence Value

Write one sentence explaining why the paper belongs in the vault.

Example:

```markdown
## One-Sentence Value

This paper is useful because it shows how an ADC-based PAM4 receiver combines analog front-end bandwidth, time-interleaved conversion, DSP equalization, and clocking calibration at a high SerDes data rate.
```

## Reading Status

Use a clear status:

```markdown
## Reading Status

- Status: first pass complete
- Depth: architecture-level summary
- Figures reviewed: architecture diagram, measurement table, jitter or BER plot
- Needs deeper review: calibration loop and power breakdown
```

## Paper Context

Explain the technical context.

Example:

```markdown
## Paper Context

The paper sits in the ADC-based PAM4 receiver branch of the vault. It is relevant to SerDes RX architecture, TI-SAR ADC calibration, sampling jitter, DSP equalization, and clocking.
```

## Problem Statement

Summarize the problem the paper addresses.

Example:

```markdown
## Problem Statement

At high PAM4 data rates, the receiver must recover symbols through a lossy channel with limited vertical eye margin. The design challenge is to preserve enough analog signal quality for DSP equalization while controlling ADC power, timing skew, and front-end bandwidth.
```

## Architecture Summary

Describe the architecture in your own words.

```markdown
## Architecture Summary

The receiver uses:

- Analog front-end for termination, gain, and bandwidth shaping.
- Time-interleaved ADC for waveform sampling.
- Digital equalization for ISI reduction.
- CDR or sampling-clock recovery.
- Calibration loops for offset, gain, and timing mismatch.
```

Add a simple text diagram if useful:

```text
Channel -> AFE -> TI-ADC -> DSP equalizer -> slicer/decoder
                    ^
                    |
              sampling clock / CDR
```

## Key Technical Claims

List claims the paper makes.
Separate measured results from interpretation.

Example:

```markdown
## Key Technical Claims

- The architecture uses ADC sampling followed by DSP equalization.
- Calibration is required to reduce interleaving mismatch.
- The measured performance depends on channel loss, clock quality, and equalization settings.
```

If exact numbers are included, preserve units and context.

## Important Figures or Tables

Summarize figures without copying them.

```markdown
## Important Figures or Tables

- Architecture figure: Shows the RX chain from analog front-end through ADC and DSP.
- Calibration figure: Shows offset, gain, or timing-skew correction loop.
- Measurement table: Reports data rate, power, process, area, and performance metrics.
- Eye or BER plot: Shows link margin after equalization.
```

## Equations and Metrics

Capture formulas or metrics that matter.

Examples:

```markdown
## Equations and Metrics

Relevant metrics:

- Data rate or symbol rate.
- Energy per bit.
- ADC resolution and sampling rate.
- SNDR or ENOB.
- BER.
- Channel loss.
- Jitter.
- Power breakdown.
```

Follow `.codex/formula_style.md` if writing equations.

## Design Lessons

Write durable lessons cautiously.

Example:

```markdown
## Design Lessons

- ADC-based receiver architecture shifts part of equalization into DSP, but it increases the importance of sampling clock quality and ADC calibration.
- Time interleaving improves effective sampling rate but creates offset, gain, bandwidth, and skew mismatch that must be calibrated.
- Receiver performance should be judged at the link level, not only by standalone ADC metrics.
```

Do not claim the paper proves a universal design rule unless it does.

## Relevance to This Vault

Connect to the user's focus.

```markdown
## Relevance to This Vault

This paper supports study of:

- PCIe and high-speed PAM4 receiver architecture.
- ADC-based receiver design.
- TI-SAR calibration.
- Sampling jitter.
- DSP equalization.
- Interview explanations for modern SerDes RX tradeoffs.
```

## Related Notes

Add links:

```markdown
## Related Notes

- [PAM4 receiver basics](../SerDes/pam4_receiver_basics.md)
- [ADC-based receiver](../ADC/adc_based_receiver.md)
- [Sampling jitter in ADCs](../ADC/sampling_jitter_adc.md)
- [CTLE, FFE, and DFE notes](../SerDes/ctle_ffe_dfe_notes.md)
```

## Questions for Deeper Reading

Use real technical questions.

Example:

```markdown
## Questions for Deeper Reading

- What exact mismatch sources dominate the TI-ADC performance?
- How does the CDR interact with ADC sampling timing?
- What channel-loss condition was used for the main result?
- How much of the power is analog front-end, ADC, DSP, and clocking?
```

## Claims Not Yet Verified

Use this section if the note is based on a quick read or secondary source.

Example:

```markdown
## Claims Not Yet Verified

- Exact reported energy per bit should be checked against the original measurement table.
- The calibration loop description is based on a first-pass reading and needs figure-level review.
```

## Interview Use

Capture interview value.

Example:

```markdown
## Interview Use

This paper can support an answer to:

"Why do modern PAM4 receivers often use ADC-based architectures?"

Answer angle:
ADC-based RX enables flexible DSP equalization and adaptation, but it makes converter speed, timing accuracy, interleaving calibration, and power central design constraints.
```

## Paper Note Completion Checklist

Before finishing:

- Citation is complete or uncertainty is explicit.
- Summary is in original words.
- Important architecture and metrics are captured.
- Design lessons are cautious.
- Related notes are linked.
- Paper claims are separated from Codex inference.
- No long copyrighted excerpts are copied.
- Unverified exact numbers are marked.

## Expert Rationale for This Template

Paper notes are source-backed memory.
They must preserve what the paper actually contributes without turning into copied text or overgeneralized design rules.

A paper is not automatically a universal truth.
It is evidence under specific assumptions:

- Technology node.
- Architecture.
- Data rate.
- Channel condition.
- Measurement setup.
- Figure of merit.
- Calibration method.
- Supply and clocking environment.

For a senior engineer, a paper note should answer:

- What did the authors build or analyze?
- What was measured or proven?
- What assumptions or conditions matter?
- What can be reused in my design intuition?
- What should not be generalized?

For a future AI agent, this template separates paper claims from Codex synthesis.

## Why Each Section Exists

### Citation

Reason:
The paper must be findable again.
Incomplete citations make future verification difficult.

### One-Sentence Value

Reason:
Not every paper deserves deep extraction.
This sentence records why the paper is in the vault.

### Architecture Summary

Reason:
Analog and mixed-signal papers are architecture-dependent.
Performance numbers are meaningless without architecture context.

### Key Technical Claims

Reason:
This separates what the paper says from what the agent infers.

### Important Figures or Tables

Reason:
Many IC papers are best understood through block diagrams, measured plots, and comparison tables.
This section tells future readers which figures to revisit.

### Design Lessons

Reason:
Design lessons are the reusable output, but they must be cautious and source-aware.

## Best Practices

- Use original wording only in very short excerpts when necessary.
- Paraphrase aggressively.
- Record exact numbers only with units and conditions.
- Distinguish measured results from simulation results.
- Distinguish paper claims from your interpretation.
- Link the paper to durable topic notes.
- Extract only reusable concepts into topic notes.
- Keep copyright safety in mind.
- Record reading depth honestly.

## Bad Paper Note Example

```markdown
This paper proves ADC-based receivers are best for PAM4. It achieves great power and fixes channel loss with DSP.
```

Why this is bad:

- Overgeneralizes one paper.
- No architecture.
- No conditions.
- No measured metrics.
- No source detail.
- "Best" is unsupported.

## Good Paper Note Example

```markdown
The paper demonstrates an ADC-based PAM4 receiver under the reported channel and measurement conditions. The durable lesson is that ADC sampling enables flexible DSP equalization, but the architecture depends heavily on front-end bandwidth, sampling-clock quality, interleaving calibration, and digital adaptation.
```

## Engineering Example: ADC-Based PAM4 Receiver Paper

Extract:

- Data rate and symbol rate.
- PAM4 or NRZ signaling.
- ADC architecture and sampling strategy.
- Equalization architecture.
- CDR or sampling-clock approach.
- Calibration loops.
- Channel loss condition.
- Power breakdown.
- BER or eye measurement.

Do not extract as universal:

- The exact ADC resolution as a requirement for all receivers.
- The exact power number without process and measurement conditions.
- The architecture as automatically suitable for PCIe.

## Workflow for Paper Processing

1. Capture citation.
2. Identify paper type and venue.
3. Write one-sentence value.
4. Summarize problem statement.
5. Summarize architecture.
6. Extract key claims and metrics.
7. Identify important figures.
8. Write design lessons.
9. Link to topic notes.
10. Add claims not yet verified if reading is incomplete.
11. Promote reusable concepts to domain notes only after screening.

## Edge Cases

### Only Abstract Is Available

Set access status to abstract-only.
Do not infer details not present in the abstract.

### Paper Uses Proprietary or Unavailable Details

Summarize public information only.
Do not reconstruct missing data from speculation.

### Paper Results Conflict with Another Paper

Record conditions.
Different architecture, process, channel, or measurement setup may explain the conflict.

### Vendor Application Note

Label as vendor-specific.
Do not treat it as neutral academic evidence.

### Standard Summary

Use public material only.
Avoid copying protected standard text.

## Quality Checklist

- Citation is complete enough to find the source.
- Access status is clear.
- Architecture is described.
- Metrics include units and conditions.
- Claims are separated from interpretation.
- Design lessons are cautious.
- Related notes are linked.
- Copyrighted text is not copied at length.
- Reading depth is honest.
- Unverified details are marked.

## Automation Opportunities

Future tools could:

- Extract citation metadata from DOI or BibTeX.
- Generate frontmatter.
- Suggest related vault notes from abstract keywords.
- Build a paper-to-topic map.
- Track reading status.
- Detect exact metrics without units.
- Detect missing venue/year/author fields.

Automation must not summarize copyrighted text beyond safe paraphrase and must not invent inaccessible details.

## Future Extension Ideas

- Add a paper ranking rubric for relevance to SerDes, PLL/CDR, ADC, LDO, and career goals.
- Add a reading queue.
- Add citation graph support.
- Add paper comparison tables.
- Add a "design lessons promoted" field.
- Add links from topic notes back to supporting papers.

## Self-Contained Summary

This template creates paper notes that preserve source value without copying or overgeneralizing.
The output should capture citation, architecture, metrics, claims, design lessons, links, and uncertainty.
The paper note remains source-specific; reusable concepts can be promoted into domain notes.
