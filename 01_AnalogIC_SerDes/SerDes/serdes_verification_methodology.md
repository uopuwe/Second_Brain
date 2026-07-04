---
title: "SerDes Verification Methodology"
domain: "AnalogIC_SerDes"
tags:
  - SerDes
  - Verification
  - PCIe7
  - CDR
  - Jitter
aliases:
  - serdes_verification_methodology
  - SerDes verification methodology
canonical: "[[pcie7_clocking_notes]]"
created: 2026-07-04
updated: 2026-07-04
status: "routing"
---

# SerDes Verification Methodology

This is a routing note, not a duplicate verification handbook.

Use [[pcie7_clocking_notes]], [[cdr_jitter_tolerance]], and [[pll_phase_noise_jitter]] as the canonical technical references for clocking, CDR, and jitter verification.

## Core Reminder

SerDes verification must connect block-level simulations to link-level margin. A useful methodology states the measurement point, PVT, supply condition, integration bandwidth, jitter taxonomy, channel/equalizer state, CDR state, adaptation sequence, BER or margin criterion, and compliance caveats.

For PCIe 7.0 work, do not claim official compliance unless the setup follows the official specification or approved internal requirement.

## Canonical Sections

- [[pcie7_clocking_notes]]
- [[pcie7_clocking_notes#15. Design Checklist]]
- [[cdr_jitter_tolerance]]
- [[cdr_jitter_tolerance#19. Principal-Level Checklist]]
- [[pll_phase_noise_jitter]]
- [[pll_phase_noise_jitter#22. Principal-Level Design Checklist]]

## Related Notes

- [[serdes_architecture_overview]]
- [[ctle_ffe_dfe_notes]]
- [[pam4_adc_based_rx]]
