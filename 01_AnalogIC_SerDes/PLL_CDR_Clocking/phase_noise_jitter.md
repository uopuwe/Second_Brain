---
title: "Phase Noise and Jitter"
domain: "AnalogIC_SerDes"
tags:
  - PhaseNoise
  - Jitter
  - PLL
  - Clocking
  - SerDes
aliases:
  - phase_noise_jitter
  - Phase Noise and Jitter
canonical: "[[pll_phase_noise_jitter]]"
created: 2026-07-01
updated: 2026-07-01
status: "merged"
---

# Phase Noise and Jitter

This note has been merged into [[pll_phase_noise_jitter]].

Use [[pll_phase_noise_jitter]] as the canonical reference for:

- phase noise to RMS jitter conversion
- PLL noise transfer functions
- PLL bandwidth and jitter peaking
- spurs and deterministic jitter
- supply noise, LDO PSRR, and power integrity to jitter
- PCIe 7.0 PAM4 timing scale
- CDR jitter transfer, tolerance, and generation
- ADC aperture jitter
- Cadence / SpectreRF simulation flow
- lab debug and design-review checklists

## Merge Decision

The previous `phase_noise_jitter.md` was an early general study note. Its useful material is now covered at higher rigor in [[pll_phase_noise_jitter]], including the original phase-noise-to-jitter equations, SerDes eye-closure framing, CDR interaction, LDO/supply conversion, and interview Q&A.

This file is kept only as a stable Obsidian alias so old links do not break.

## Related Notes

- [[pll_phase_noise_jitter]]
- [[pll_fundamentals]]
- [[pll_loop_bandwidth]]
- [[cdr_jitter_tolerance]]
- [[cdr_fundamentals]]
- [[sampling_jitter_adc]]
- [[ldo_psrr_notes]]
- [[serdes_power_integrity]]
