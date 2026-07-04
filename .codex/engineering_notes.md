# Engineering Note Standards

## Purpose

This document defines technical depth standards for analog and mixed-signal notes.
It is a quality standard, not a workflow.
Use [expand_note.md](expand_note.md) for expansion steps and [core/quality_standards.md](core/quality_standards.md) for global gates.
Continuous engineering-insight expansion is coordinated by [continuous_knowledge_improvement.md](continuous_knowledge_improvement.md), which routes post-ingest depth improvements here instead of duplicating these standards.

## Core Standard

A strong engineering note connects:

1. System problem.
2. Architecture or circuit mechanism.
3. Quantitative relationship.
4. Design tradeoff.
5. Failure mode or debug implication.

## Domain Standards

### SerDes and PCIe

Must distinguish:

- NRZ versus PAM4.
- GT/s, Gb/s, Gbaud, UI, and Nyquist frequency.
- Channel loss, ISI, crosstalk, jitter, and noise.
- TX FFE, CTLE, RX FFE, DFE, ADC/DSP, and CDR roles.

Exact PCIe compliance claims require source verification under [core/mandatory_rules.md](core/mandatory_rules.md).

### PLL / CDR / Clocking

Must distinguish:

- Phase noise versus time jitter.
- Jitter transfer versus jitter tolerance.
- Reference noise, VCO noise, divider noise, and supply-induced noise.
- Linear PLL assumptions versus bang-bang or data-driven CDR behavior.

### ADC / DAC

Must distinguish:

- SNR, SNDR, ENOB, SFDR, aperture jitter, and quantization noise.
- Standalone ADC metrics versus link-level receiver performance.
- Correctable calibration errors versus irreversible information loss.

### LDO / Bandgap

Must distinguish:

- Stability, PSRR, output noise, output impedance, transient response, and load regulation.
- Block-level regulator metrics versus system-level supply-noise impact.
- Bandgap PTAT/CTAT behavior, startup, trimming, curvature, and reference noise.

### DSP and Equalization

Must connect algorithms to channel behavior:

- Cursor model.
- Pre-cursor and post-cursor ISI.
- Noise enhancement.
- Adaptation limits.
- ADC and CDR interaction.

## Good Example

```markdown
An ADC-based PAM4 receiver can use DSP equalization to reduce ISI after sampling, but the analog front-end must still preserve enough bandwidth, linearity, timing accuracy, and SNR. DSP cannot recover information lost before or during sampling.
```

## Bad Example

```markdown
DSP fixes the channel after the ADC.
```

## Engineering Quality Gate

Before calling a note technically strong:

- System impact is clear.
- Assumptions are explicit.
- Metrics and units are defined.
- Tradeoffs are balanced.
- Failure modes are included when relevant.
- Source status is visible.
- Related notes are linked.
