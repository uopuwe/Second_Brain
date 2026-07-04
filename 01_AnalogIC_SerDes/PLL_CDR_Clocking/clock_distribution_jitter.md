---
title: "Clock Distribution Jitter"
domain: "AnalogIC_SerDes"
tags:
  - Clocking
  - Jitter
  - SerDes
  - PLL
  - PowerIntegrity
aliases:
  - clock_distribution_jitter
  - clock tree jitter
canonical: "[[pll_phase_noise_jitter]]"
created: 2026-07-04
updated: 2026-07-04
status: "routing"
---

# Clock Distribution Jitter

This is a routing note, not a duplicate clocking handbook.

Use [[pll_phase_noise_jitter]] for digital clock-distribution noise and [[pcie7_clocking_notes]] for PCIe 7.0 clock-chain interpretation.

## Core Reminder

PLL output jitter is not necessarily sampler-clock jitter. Dividers, clock buffers, local routing, multi-phase generation, phase interpolators, serializer clocks, sampler buffers, ADC clock trees, supply noise, and thermal delay drift can all add timing uncertainty after the PLL.

Clock-distribution jitter should be reviewed by measurement point, carrier frequency, integration band, supply domain, extracted loading, switching activity, correlation across lanes, and whether the noise is phase-type or time-type.

## Canonical Sections

- [[pll_phase_noise_jitter]]
- [[pll_phase_noise_jitter#23. Digital Clock Distribution Noise]]
- [[pcie7_clocking_notes#8. Clocking Architecture]]
- [[pcie7_clocking_notes#9. Jitter and Phase Noise Implications]]

## Related Notes

- [[serdes_power_integrity]]
- [[ldo_psrr_notes]]
- [[cdr_jitter_tolerance]]
