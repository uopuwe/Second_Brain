---
title: "Phase Interpolator"
domain: "AnalogIC_SerDes"
tags:
  - CDR
  - PhaseInterpolator
  - Clocking
  - Jitter
  - SerDes
aliases:
  - phase_interpolator
  - PI
canonical: "[[cdr_fundamentals]]"
created: 2026-07-04
updated: 2026-07-04
status: "routing"
---

# Phase Interpolator

This is a routing note, not a duplicate CDR handbook.

Use [[cdr_fundamentals]] as the canonical reference for CDR actuators and [[pcie7_clocking_notes]] for PCIe 7.0 PI step-size interpretation.

## Core Reminder

A phase interpolator adjusts sampling phase by blending or selecting clock phases. In SerDes receivers it is often the actuator used by the CDR loop. Its range, step size, INL/DNL, monotonicity, supply sensitivity, mismatch, and calibration directly affect residual jitter and sampling margin.

For PCIe 7.0 PAM4, PI step size must be interpreted against the PAM4 symbol UI, not the bit-equivalent interval, unless the architecture explicitly defines otherwise.

## Canonical Sections

- [[cdr_fundamentals]]
- [[cdr_fundamentals#9. Phase Interpolator-Based CDR]]
- [[pcie7_clocking_notes#10. CDR Implications]]
- [[pcie7_clocking_notes#9. Jitter and Phase Noise Implications]]

## Related Notes

- [[cdr_jitter_tolerance]]
- [[pll_phase_noise_jitter]]
- [[sampling_jitter_adc]]
