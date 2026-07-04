# General Technical Note Template

> Compatibility notice: the canonical template contract is now [../core/template_contracts.md](../core/template_contracts.md). This file is retained for existing path compatibility. Future agents must follow the core contract and ignore any duplicated legacy guidance below when it conflicts with the core operating system.

> Canonical template status: this file is retained for compatibility. Future agents should treat global policy as centralized in `../core/mandatory_rules.md`, recommendations in `../core/recommendations.md`, quality standards in `../core/quality_standards.md`, and workflow routing in `../core/workflow_router.md`. Do not duplicate those rules here.

## Purpose

Use this template for durable technical notes that do not fit a more specific template.
This includes concept notes, architecture notes, math notes, debug notes, Python analysis notes, and synthesis notes created from multiple sources.

This template is intentionally instructive.
When creating a real note, keep the sections that add value and remove guidance text that is no longer needed.
Do not leave empty headings.

## Recommended Frontmatter

Use this frontmatter for a durable note:

```yaml
---
title: "PLL Phase Noise and Jitter"
domain: "AnalogIC_SerDes"
tags:
  - PLL
  - PhaseNoise
  - Jitter
status: "active"
created: "2026-07-03"
updated: "2026-07-03"
source: "Synthesized from existing vault notes"
confidence: "medium"
---
```

Field guidance:

- `title`: Human-readable title.
- `domain`: Usually `AnalogIC_SerDes` for technical notes in this vault.
- `tags`: Stable retrieval tags.
- `status`: Use `seed`, `active`, `mature`, `needs_review`, or `archived`.
- `created`: Date the note was created.
- `updated`: Date the note was last materially changed.
- `source`: Short source description.
- `confidence`: Use `low`, `medium`, or `high`.

## Title

Use one H1:

```markdown
# PLL Phase Noise and Jitter
```

The title should be specific enough to retrieve later.

Good:

- `PLL Phase Noise and Jitter`
- `ADC Sampling Jitter`
- `SerDes Power Integrity`
- `PAM4 Receiver Basics`

Weak:

- `Notes`
- `Clocking`
- `ADC Stuff`
- `Important`

## Purpose

Explain why the note exists.

Example:

```markdown
## Purpose

This note explains how PLL phase noise relates to RMS jitter and why the integration bandwidth, carrier frequency, and noise source assumptions matter for high-speed SerDes clocking.
```

Purpose should be practical.
It should help a future reader decide whether this is the right note.

## Short Summary

Write a compact summary.

Example:

```markdown
## Short Summary

Phase noise describes frequency-domain phase fluctuations around a carrier. RMS jitter is a time-domain measure derived from integrated phase noise over a specified offset-frequency range. The conversion is not meaningful unless the carrier frequency and integration limits are stated.
```

Keep the summary accurate rather than catchy.

## Why This Matters

Connect the concept to design or career value.

Examples:

```markdown
## Why This Matters

In PCIe and SerDes clocking, jitter directly affects sampling margin and link reliability. A PLL that looks acceptable at one integration bandwidth may not meet a different system or compliance requirement, so the measurement assumptions must be explicit.
```

```markdown
## Why This Matters

For interview preparation, this topic tests whether the explanation can connect circuit noise, loop behavior, and system timing margin rather than only reciting formulas.
```

## Context

State where the concept lives in the system.

Example:

```markdown
## Context

This topic sits between PLL design, CDR behavior, and SerDes receiver timing margin. It is closely related to:

- Clock generation.
- Clock distribution.
- Supply noise.
- Sampling jitter.
- Jitter tolerance.
```

## Key Concepts

List the important ideas.

Example:

```markdown
## Key Concepts

- Phase noise is a frequency-domain description of phase fluctuation around a carrier.
- RMS jitter is a time-domain measure of timing uncertainty.
- Integrated jitter depends on offset-frequency limits.
- PLL loop dynamics shape different noise sources differently.
- Supply noise can modulate oscillator phase and appear as jitter.
```

Avoid listing terms without explaining them later.

## Architecture or Circuit View

Use this section to describe the relevant block.

Example for PLL:

```markdown
## Architecture View

A conventional charge-pump PLL contains:

- Reference input.
- Phase-frequency detector.
- Charge pump.
- Loop filter.
- VCO.
- Feedback divider.

The loop compares divided output phase against reference phase and adjusts the VCO control voltage to reduce phase error.
```

Example for SerDes RX:

```markdown
## Architecture View

A simplified ADC-based PAM4 receiver chain is:

```text
Channel -> termination -> CTLE/VGA -> ADC -> DSP FFE/DFE -> slicer -> decoder
                         ^
                         |
                       CDR / sampling clock
```
```

## Equations

Use `.codex/formula_style.md`.

Example:

```markdown
## Equations

For small phase error, RMS time jitter can be estimated from RMS phase error:

$$
\sigma_t = \frac{\sigma_\phi}{2\pi f_0}
$$

where:

- $\sigma_t$ is RMS time jitter in seconds.
- $\sigma_\phi$ is RMS phase error in radians.
- $f_0$ is carrier frequency in hertz.

This equation is only meaningful after defining how $\sigma_\phi$ was obtained, including integration bandwidth.
```

## Design Tradeoffs

Use the tradeoff pattern from `.codex/engineering_notes.md`.

Example:

```markdown
## Design Tradeoffs

### Loop Bandwidth

Increasing loop bandwidth can improve tracking of low-frequency reference-related behavior and reduce some oscillator noise contribution inside the loop bandwidth.

It can also increase sensitivity to reference noise, spurs, or stability issues depending on loop design.

The correct bandwidth depends on noise sources, reference quality, output frequency, architecture, and system jitter requirements.
```

## Failure Modes

Describe practical ways the concept fails.

Example:

```markdown
## Failure Modes

- Symptom: Measured RMS jitter changes depending on the instrument setup.
- Likely mechanism: Integration bandwidth, filtering, or clock frequency assumptions differ between measurements.
- How to test: Record offset-frequency limits, instrument settings, and phase-noise curve before comparing numbers.
- Possible fixes: Standardize measurement assumptions and compare phase-noise plots, not just scalar jitter values.
```

## Debug Checklist

Add a checklist when the note supports practical debugging.

Example:

```markdown
## Debug Checklist

- Confirm units and measurement bandwidth.
- Confirm the exact node being measured.
- Separate random and deterministic effects.
- Sweep supply, temperature, and load when relevant.
- Compare simulation assumptions against measurement setup.
- Check related blocks that can create the same symptom.
```

## Interview Framing

Use when the topic is interview-relevant.

Example:

```markdown
## Interview Framing

If asked to explain this topic:

1. Start from system impact.
2. Explain the circuit or algorithm mechanism.
3. Mention the key equation or metric.
4. Discuss one real tradeoff.
5. End with a practical verification or debug point.
```

Example answer:

```markdown
For PLL jitter, I would first clarify the carrier frequency and integration bandwidth. Phase noise is the spectral description, while RMS jitter is obtained after integrating phase noise over a defined offset-frequency range and converting phase error to time error. In a SerDes clocking path, that timing uncertainty reduces sampling margin, and supply noise can further modulate the oscillator depending on supply sensitivity.
```

## Related Notes

Add links to nearby notes.

Example:

```markdown
## Related Notes

- [SerDes architecture overview](../../01_AnalogIC_SerDes/SerDes/serdes_architecture_overview.md)
- [CDR fundamentals](../../01_AnalogIC_SerDes/PLL_CDR_Clocking/cdr_fundamentals.md)
- [SerDes power integrity](../../01_AnalogIC_SerDes/LDO_Bandgap/serdes_power_integrity.md)
```

## Sources and Provenance

State source history.

Example:

```markdown
## Sources and Provenance

- Synthesized from existing vault notes.
- Source packet: `../../00_Inbox/manual_batches/batch2_serdes_pcie_pll_cdr_adc_2026-07-01/source_packet.md`
- Verification status: exact PCIe compliance numbers were not checked against primary sources in this session.
```

## Open Questions

Use open questions for real uncertainty.

Example:

```markdown
## Open Questions

- Which integration bandwidth is most relevant for the target PCIe clocking compliance setup?
- Which supply-noise frequency range most strongly modulates the PLL in this architecture?
```

Do not use open questions as a dumping ground for unfinished editing work.

## Completion Checklist

Before using a note created from this template:

- Frontmatter is valid.
- Purpose is clear.
- Summary is technically accurate.
- Equations define symbols and units.
- Assumptions are stated.
- Related notes are linked.
- Sources or provenance are recorded.
- No empty headings remain.
- Unverified claims are marked.

## Expert Rationale for This Template

This template exists because general notes are the most common source of vault drift.
Without a strong template, a general note can become a vague container for definitions, pasted chat fragments, and unsupported claims.

The template forces a general note to answer:

- Why does this note exist?
- What system or design problem does it support?
- What mechanism matters?
- What assumptions apply?
- What equations or tradeoffs are relevant?
- What can go wrong?
- Where did the knowledge come from?
- What should the reader inspect next?

For a senior analog IC designer, this template should produce notes that are useful in design review, debug planning, paper reading, and interview preparation.
For a future AI agent, it provides enough structure to classify, expand, link, and review the note later.

## Why Each Section Exists

### Purpose

Reason:
Purpose prevents a note from becoming an undirected collection of facts.

Bad example:

```markdown
This note is about jitter.
```

Good example:

```markdown
This note explains how sampling-clock jitter creates voltage error in ADC-based PAM4 receivers and why that matters for SerDes timing margin.
```

### Short Summary

Reason:
The summary gives fast retrieval.
Future agents can decide whether to read the full note.

### Context

Reason:
Analog and mixed-signal concepts are system-dependent.
A formula or circuit block must be placed in the signal chain.

### Equations

Reason:
Equations capture quantitative relationships, but only if assumptions and units are included.

### Design Tradeoffs

Reason:
Tradeoffs are the core of engineering judgment.
They prevent notes from becoming one-sided recommendations.

### Failure Modes

Reason:
Failure modes connect theory to debug and silicon learning.

### Sources and Provenance

Reason:
Source history lets future agents assess trust.

## Best Practices

- Keep only sections that serve the real note.
- Preserve the order from system-level to detail-level.
- Use specific titles and stable tags.
- Add at least one design implication for major concepts.
- Add related links before finishing.
- Add source quality and confidence.
- Avoid using this template to hide weak source material behind polished prose.
- Remove instructional text from real notes.
- Do not leave empty sections.

## Bad Note Example

```markdown
# PAM4

PAM4 has four levels and is used in SerDes. It is faster than NRZ. Equalization is important. ADCs and DSP are used.
```

Why this is bad:

- No purpose.
- "Faster" is imprecise.
- No system context.
- No tradeoff.
- No source.
- No links.

## Good Note Example

```markdown
# PAM4 Receiver Basics

## Purpose

This note explains how PAM4 receiver architecture differs from binary signaling and why vertical margin, linearity, equalization, and timing recovery become more critical.

## Short Summary

PAM4 carries two bits per symbol using four amplitude levels. For the same full-scale swing, adjacent level spacing is smaller than binary signaling, so noise, distortion, equalization error, and sampling jitter consume margin more quickly.

## Design Tradeoff

PAM4 improves bit rate for a given symbol rate, but it increases receiver complexity and sensitivity to amplitude and timing impairments.
```

## Engineering Example

Use this template for `sampling_jitter_adc.md`:

- Purpose: connect clock jitter to ADC and receiver performance.
- Context: ADC-based PAM4 receiver.
- Equation: jitter-limited SNR for sinusoidal input with caveat.
- Tradeoff: lower jitter costs power, PLL complexity, and clock distribution care.
- Failure mode: good standalone ADC SNDR but poor link margin due to sampling clock noise.
- Links: PLL phase noise, ADC-based receiver, PAM4 receiver basics.

## Workflow for Creating a General Note

1. Choose the destination folder.
2. Search for existing notes.
3. Choose a specific title.
4. Add frontmatter.
5. Write purpose and summary.
6. Add context before details.
7. Add mechanisms and equations.
8. Add tradeoffs and failure modes.
9. Add links and sources.
10. Remove template guidance.
11. Check that no empty headings remain.

## Edge Cases

### The Note Is Only a Seed

Use `status: "seed"` and `confidence: "low"` or `medium`.
Keep it short but source-aware.

### The Note Is a Cross-Domain Concept

Choose the strongest primary domain and add links.
Do not duplicate the note in multiple folders.

### The Note Is Based on AI Output

State that clearly in source/provenance.
Screen claims before promoting them.

### The Note Needs External Verification

Mark the relevant claims.
Do not imply source-backed certainty.

## Quality Checklist

- The note has a specific purpose.
- Summary is accurate.
- System context is present.
- Assumptions are explicit where needed.
- Equations follow formula style.
- Tradeoffs are balanced.
- Failure modes or debug hooks are included when relevant.
- Links are useful.
- Provenance is explicit.
- Confidence matches source quality.

## Automation Opportunities

Future tools could:

- Generate frontmatter from file path.
- Suggest tags from headings.
- Detect empty sections.
- Suggest related notes.
- Check for missing source sections.
- Flag formulas without definitions.
- Generate note skeletons from this template.

## Future Extension Ideas

- Create domain-specific note templates for PLL, CDR, ADC, LDO, and SerDes.
- Add metadata for canonical status.
- Add maturity scoring.
- Add generated related-link suggestions.
- Add a note creation wizard for future agents.

## Self-Contained Summary

This template creates durable general technical notes.
It should produce notes with purpose, context, mechanisms, equations, tradeoffs, failure modes, links, and provenance.
The goal is a reusable engineering reference, not a decorated scratchpad.
