---
title: "PCIe 7.0 GT/s vs Gbaud vs UI"
domain: "AnalogIC_SerDes"
tags:
  - PCIe7
  - PAM4
  - SerDes
  - Clocking
  - UI
aliases:
  - pcie7_gtps_vs_gbaud_ui
  - PCIe7 GT/s vs Gbaud UI
canonical: "[[pcie7_clocking_notes]]"
created: 2026-07-04
updated: 2026-07-04
status: "routing"
---

# PCIe 7.0 GT/s vs Gbaud vs UI

This is a routing note, not a duplicate handbook.

Use [[pcie7_clocking_notes]] as the canonical technical reference for PCIe 7.0 rate, PAM4 symbol rate, symbol UI, bit-equivalent UI, and Nyquist-frequency interpretation.

## Core Reminder

PCIe 7.0 public headline rate is 128 GT/s per lane. With PAM4, each electrical symbol carries 2 bits, so the electrical symbol rate is 64 Gbaud and the PAM4 symbol UI is 15.625 ps.

Do not use 7.8125 ps as the PAM4 symbol UI. That value is the bit-equivalent interval for 128 Gb/s arithmetic, not the symbol spacing used for CDR sampling phase, PI step sizing, horizontal eye margin, or symbol-spaced equalization.

## Canonical Sections

- [[pcie7_clocking_notes]]
- [[pcie7_clocking_notes#4. GT/s vs Gb/s vs Gbaud vs UI]]
- [[pcie7_clocking_notes#5. PAM4 Symbol Rate and UI Derivation]]
- [[pcie7_clocking_notes#6. Worked Example 1: 128 GT/s PCIe 7.0 UI and Nyquist]]
- [[pcie7_overview]]

## Related Notes

- [[pll_phase_noise_jitter]]
- [[cdr_jitter_tolerance]]
- [[pam4_receiver_basics]]
- [[pam4_adc_based_rx]]
