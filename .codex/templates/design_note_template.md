# Design Note Template

> Compatibility notice: the canonical template contract is now [../core/template_contracts.md](../core/template_contracts.md). This file is retained for existing path compatibility. Future agents must follow the core contract and ignore any duplicated legacy guidance below when it conflicts with the core operating system.

## Purpose

Use this template for design-focused notes, architecture decisions, circuit investigations, debug writeups, simulation plans, and engineering tradeoff records.

This template is for practical engineering thinking.
It should capture assumptions, options, constraints, decisions, evidence, and next checks.

## Recommended Frontmatter

```yaml
---
title: "LDO PSRR Impact on PLL Supply Noise"
domain: "AnalogIC_SerDes"
tags:
  - LDO
  - PLL
  - PowerIntegrity
status: "active"
created: "2026-07-03"
updated: "2026-07-03"
source: "Design synthesis"
confidence: "medium"
design_context: "general learning"
---
```

If the note is work-related, avoid proprietary details unless the user explicitly provides them and asks to retain them.

## Title

Use a title that identifies the design question.

Good:

- `LDO PSRR Impact on PLL Supply Noise`
- `ADC-Based PAM4 Receiver Timing Budget`
- `CDR Loop Bandwidth Tradeoff`
- `TI-SAR Skew Calibration Strategy`

Weak:

- `Design`
- `Debug`
- `Thoughts`

## Design Question

State the central question.

Example:

```markdown
## Design Question

How does LDO output noise and finite PSRR affect PLL phase noise and RMS jitter in a SerDes clocking path?
```

The design question should be answerable by analysis, simulation, measurement, or literature review.

## Context

Describe the system context.

Example:

```markdown
## Context

The PLL provides a sampling or serialization clock for a high-speed SerDes link. Supply noise at sensitive frequencies can modulate the oscillator and appear as phase noise or spurs. The LDO is intended to isolate the PLL from upstream supply noise, but its PSRR, output impedance, and own noise vary with frequency and load.
```

## Assumptions

List assumptions explicitly.

```markdown
## Assumptions

- The note is architecture-level and does not use proprietary circuit values.
- PLL supply sensitivity is nonzero and frequency-dependent.
- LDO PSRR is frequency-dependent.
- Local decoupling is present but not ideal.
- Exact compliance limits are not assumed without a source.
```

Assumptions make the note reusable and prevent false generalization.

## Requirements or Success Criteria

Use this section when requirements are known.

```markdown
## Requirements or Success Criteria

- Reduce supply-induced phase modulation at the PLL output.
- Maintain LDO loop stability across load and PVT.
- Avoid excessive output noise from the regulator itself.
- Preserve transient response for activity-dependent load current.
```

If exact numeric requirements are unknown, say that they are not established in the note.

## Candidate Options

Compare options.

```markdown
## Candidate Options

| Option | Benefit | Risk | When It Makes Sense |
| --- | --- | --- | --- |
| Increase local decoupling | Reduces local supply ripple at some frequencies | Area, resonance, limited low-frequency effect | High-frequency current demand |
| Improve LDO PSRR | Better upstream noise rejection | Loop stability and power tradeoffs | Supply noise is dominant through regulator path |
| Isolate PLL supply | Reduces coupling from digital blocks | Routing and area cost | Noisy shared supply environment |
```

## Analysis

Write the reasoning.

Example:

```markdown
## Analysis

The PLL does not care about supply noise only as a voltage ripple. It cares about how that ripple converts to phase modulation. The relevant path is:

```text
upstream noise -> LDO attenuation/output noise -> PLL supply ripple -> VCO frequency modulation -> phase noise or spurs -> time jitter
```

Therefore the design must evaluate both the regulator behavior and the PLL supply sensitivity. A high PSRR number at low frequency is not sufficient if the sensitive noise lies near a frequency where PSRR has degraded or where package/decap resonance creates a peak.
```

## Equations

Use formulas only with assumptions.

Example:

```markdown
## Equations

If VCO frequency sensitivity to supply is approximated as $K_{VDD}$ in Hz/V, a sinusoidal supply ripple can create frequency modulation. The resulting spur or phase modulation depends on ripple amplitude, modulation frequency, and oscillator sensitivity.

This note does not assign a universal formula because the exact result depends on modulation model and measurement definition.
```

## Simulation or Measurement Plan

Describe how to test.

```markdown
## Simulation or Measurement Plan

1. Measure or simulate LDO output noise and PSRR versus frequency.
2. Inject supply ripple into the PLL supply in simulation.
3. Sweep ripple frequency and amplitude.
4. Measure output phase noise, spurs, or time-domain jitter.
5. Repeat across PVT and load conditions.
6. Compare against the relevant system budget.
```

## Failure Modes

```markdown
## Failure Modes

- LDO stable at nominal load but unstable at light load.
- PSRR good at low frequency but poor near PLL-sensitive offset frequencies.
- Decoupling creates resonance with package inductance.
- Regulator output noise dominates after upstream noise is attenuated.
- Digital activity couples through substrate or package rather than through the LDO path.
```

## Decision

Use when a decision is made.

```markdown
## Decision

The preferred next design direction is to evaluate the supply-noise-to-jitter path directly rather than optimizing LDO PSRR as an isolated metric.
```

If no decision has been made, use:

```markdown
## Current Conclusion

The current conclusion is that more evidence is needed before choosing a design knob. The next evidence should be frequency-dependent PSRR and PLL supply sensitivity.
```

## Design Review Questions

```markdown
## Design Review Questions

- What is the dominant noise source?
- What frequency range matters most?
- What is the coupling path?
- Which block has the most effective design knob?
- What assumption would invalidate this analysis?
- What measurement would prove the fix worked?
```

## Related Notes

```markdown
## Related Notes

- [SerDes power integrity](../LDO_Bandgap/serdes_power_integrity.md)
- [LDO PSRR notes](../LDO_Bandgap/ldo_psrr_notes.md)
- [PLL phase noise and jitter](../PLL_CDR_Clocking/pll_phase_noise_jitter.md)
```

## Sources and Provenance

```markdown
## Sources and Provenance

- Design synthesis based on existing vault notes.
- No proprietary implementation details are included.
- Exact numeric requirements should be checked against the relevant design or standard before signoff.
```

## Design Note Completion Checklist

Before finishing:

- Design question is clear.
- Context is stated.
- Assumptions are explicit.
- Options and tradeoffs are captured.
- Evidence or planned evidence is listed.
- Decision or current conclusion is clear.
- Failure modes are included.
- Related notes are linked.
- Confidential information is avoided or clearly controlled.

## Expert Rationale for This Template

Design notes capture engineering reasoning under assumptions.
They are not the same as concept notes.
A concept note explains how something works.
A design note explains how to decide, debug, compare, or act.

This template exists because design reasoning is easy to lose:
the final conclusion may remain, but the assumptions, rejected options, evidence, and failure modes disappear.
For analog and mixed-signal work, that lost context can be more valuable than the conclusion itself.

For a senior analog IC designer, this template should support design review and debug planning.
For a principal engineer, it should make tradeoffs and risk explicit.
For a future AI agent, it should preserve enough context to continue the reasoning without inventing missing assumptions.

## Why Each Section Exists

### Design Question

Reason:
A design note should be organized around a decision or investigation, not a topic label.

Bad example:

```markdown
LDO notes.
```

Good example:

```markdown
How does LDO output noise and finite PSRR affect PLL jitter in a SerDes clocking path?
```

### Assumptions

Reason:
Design conclusions are assumption-dependent.
Without assumptions, future reuse is unsafe.

### Candidate Options

Reason:
A design note should show alternatives, not only the chosen path.

### Analysis

Reason:
This is where mechanisms, equations, and evidence connect.

### Decision or Current Conclusion

Reason:
The reader needs to know whether the note reached a decision or is still gathering evidence.

## Best Practices

- Write the design question first.
- State all major assumptions.
- Separate requirements from preferences.
- Compare options fairly.
- Use equations only with valid assumptions.
- Include simulation or measurement plans.
- Capture rejected options and why.
- Include failure modes.
- Avoid confidential details unless explicitly intended.
- Link to durable concept notes.

## Bad Design Note Example

```markdown
# PLL Supply

Need clean supply. Use better LDO and more decap.
```

Why this is bad:

- No coupling mechanism.
- No frequency range.
- No assumptions.
- No comparison of options.
- No measurement plan.
- No clear decision basis.

## Good Design Note Example

```markdown
# PLL Supply Noise Mitigation

## Design Question

Which supply-noise mitigation knob is most effective for reducing PLL output jitter: LDO PSRR improvement, local decoupling, supply isolation, or reducing VCO supply sensitivity?

## Analysis

The relevant path is:

```text
upstream ripple -> regulator/output network -> PLL supply -> VCO frequency modulation -> phase noise/spurs -> RMS jitter
```

The best knob depends on ripple frequency, LDO PSRR, decap impedance, package resonance, and VCO supply pushing.
```

## Engineering Examples

### CDR Loop Bandwidth Design Note

Design question:
What CDR loop bandwidth best balances jitter tracking, jitter filtering, stability, and detector noise?

Evidence to capture:

- Jitter transfer curve.
- Jitter tolerance curve.
- Detector type.
- Transition density.
- Equalizer interaction.
- Compliance assumptions.

### ADC Interleaving Calibration Design Note

Design question:
Which calibration loops are required for offset, gain, bandwidth, and timing-skew mismatch in a TI-SAR ADC used for PAM4 RX?

Evidence to capture:

- Dominant mismatch source.
- Background versus foreground calibration.
- Impact on SNDR or link margin.
- DSP correction limits.
- Power and area overhead.

## Workflow for Creating a Design Note

1. Define the design question.
2. Define context and block boundaries.
3. List assumptions.
4. Capture known requirements.
5. Identify candidate options.
6. Analyze mechanisms and tradeoffs.
7. Add equations or models.
8. Define simulation or measurement plan.
9. List failure modes.
10. Record decision or current conclusion.
11. Link to concept notes.
12. Screen confidentiality.

## Edge Cases

### No Decision Yet

Use `Current Conclusion` instead of forcing a decision.
List the evidence needed next.

### Requirements Are Unknown

State that exact numeric requirements are not known.
Use qualitative goals and identify the source needed.

### Design Context Is Confidential

Generalize the mechanism.
Remove proprietary identifiers and exact values.

### Multiple Options Are All Plausible

Create a comparison table and define what evidence would distinguish them.

### Simulation and Measurement Disagree

Record setup differences, model assumptions, bandwidth, loading, PVT, and measurement configuration.

## Quality Checklist

- Design question is explicit.
- Context and block boundary are clear.
- Assumptions are listed.
- Requirements or success criteria are stated.
- Options are compared.
- Analysis connects mechanism to metric.
- Evidence plan is included.
- Failure modes are included.
- Decision status is clear.
- Confidentiality is screened.
- Related concept notes are linked.

## Automation Opportunities

Future tools could:

- Generate design-note frontmatter.
- Extract assumptions into a checklist.
- Build option comparison tables.
- Link design notes to concept notes.
- Track open evidence items.
- Generate simulation checklist skeletons.
- Detect missing decision status.
- Flag confidential-looking terms for review.

Automation should help structure design reasoning, not make design decisions.

## Future Extension Ideas

- Add domain-specific design note variants for PLL, CDR, ADC, LDO, and SerDes RX.
- Add simulation plan templates.
- Add measurement plan templates.
- Add decision log integration.
- Add risk register sections.
- Add design review readiness scoring.

## Self-Contained Summary

This template captures design reasoning.
It should preserve design question, context, assumptions, requirements, options, analysis, evidence, failure modes, decision status, links, and confidentiality screening.
The goal is a reusable engineering decision record.
