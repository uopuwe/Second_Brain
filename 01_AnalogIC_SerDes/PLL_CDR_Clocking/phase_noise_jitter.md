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

## Batch 1 Alias Update - 2026-07-02

The reusable phase-noise / jitter material extracted from the top-10 batch should be maintained in [[pll_phase_noise_jitter]]. The important additions from this batch are:

- SerDes focuses on edge timing margin and BER impact; RF focuses more directly on spectral purity, close-in phase noise, EVM, and ACLR.
- PLL noise shaping can be summarized as `S_out ~= |H_ref|^2*S_ref + |H_vco|^2*S_vco + in-loop noise terms`.
- PCIe / SerDes jitter interpretation must include PLL, divider, clock tree, CDR tracking, supply noise, and ADC aperture jitter, not only oscillator phase noise.
- CDR low-frequency tracking means low-frequency phase noise may be attenuated at the sampler, while high-frequency jitter more directly closes the horizontal eye.

Source conversations:

- `../../00_Inbox/raw_chat_exports/chatgpt_export_2026-07-01/md_by_conversation/2026-02-15__SerDes_vs_RF_PLL_Jitter.md`
- `../../00_Inbox/raw_chat_exports/chatgpt_export_2026-07-01/md_by_conversation/2026-05-13__SerDes_PLL_CDR_带宽.md`
