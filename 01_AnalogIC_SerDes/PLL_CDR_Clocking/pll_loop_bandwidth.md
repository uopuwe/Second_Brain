---
title: "PLL Loop Bandwidth"
domain: "AnalogIC_SerDes"
tags:
  - PLL
  - LoopBandwidth
  - PhaseNoise
  - Jitter
  - SerDes
aliases:
  - pll_loop_bandwidth
  - PLL loop bandwidth
canonical: "[[pll_fundamentals]]"
created: 2026-07-04
updated: 2026-07-04
status: "routing"
---

# PLL Loop Bandwidth

This is a routing note, not a duplicate PLL handbook.

Use [[pll_fundamentals]] for PLL loop architecture and [[pll_phase_noise_jitter]] for phase-noise and jitter implications.

## Core Reminder

PLL loop bandwidth trades reference/in-loop noise transfer, VCO-noise suppression, spur behavior, stability margin, and lock time.

Inside the loop bandwidth, reference and in-loop noise tend to transfer more strongly to the output. Outside the loop bandwidth, VCO noise usually dominates. Real behavior depends on loop order, damping, peaking, divider ratio, PFD/CP gain, loop filter, VCO gain, PVT, and extracted parasitics.

## Canonical Sections

- [[pll_fundamentals]]
- [[pll_fundamentals#10. Loop Bandwidth]]
- [[pll_phase_noise_jitter]]
- [[pll_phase_noise_jitter#7. PLL Bandwidth and Jitter Peaking]]

## Related Notes

- [[cdr_jitter_tolerance]]
- [[pcie7_clocking_notes]]
- [[serdes_power_integrity]]
