---
title: "PLL Phase Noise to Jitter"
domain: "AnalogIC_SerDes"
tags:
  - PLL
  - PhaseNoise
  - Jitter
  - Clocking
  - SerDes
aliases:
  - pll_phase_noise_to_jitter
  - phase noise to jitter
canonical: "[[pll_phase_noise_jitter]]"
created: 2026-07-04
updated: 2026-07-04
status: "routing"
---

# PLL Phase Noise to Jitter

This is a routing note, not a duplicate phase-noise handbook.

Use [[pll_phase_noise_jitter]] as the canonical reference for phase-noise density, integration bandwidth, RMS phase error, RMS time jitter, spur policy, and SerDes clocking interpretation.

## Core Reminder

Phase noise is a frequency-domain description of phase fluctuation around a carrier. Jitter is a time-domain description of edge timing uncertainty. Any conversion must state carrier frequency, offset-frequency integration limits, single-sideband convention, spur inclusion policy, and measurement node.

## Canonical Sections

- [[pll_phase_noise_jitter]]
- [[pll_phase_noise_jitter#4. Relationship Between L(f), S_phi(f), Phase Error, and Jitter]]
- [[pll_phase_noise_jitter#5. Numerical Integration of Phase Noise]]
- [[pll_fundamentals#13. Phase Noise to Jitter]]

## Related Notes

- [[sampling_jitter_adc]]
- [[cdr_jitter_tolerance]]
- [[pcie7_clocking_notes]]
