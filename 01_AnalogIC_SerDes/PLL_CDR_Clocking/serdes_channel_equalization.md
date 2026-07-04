---
title: "SerDes Channel Equalization"
domain: "AnalogIC_SerDes"
tags:
  - SerDes
  - Equalization
  - CTLE
  - FFE
  - DFE
  - PAM4
aliases:
  - serdes_channel_equalization
  - channel equalization
canonical: "[[ctle_ffe_dfe_notes]]"
created: 2026-07-04
updated: 2026-07-04
status: "routing"
---

# SerDes Channel Equalization

This is a routing note, not a duplicate equalization handbook.

Use [[ctle_ffe_dfe_notes]] as the canonical note for CTLE, FFE, DFE, ISI, adaptation, PAM4 equalization, and CDR interaction.

## Core Reminder

Channel equalization is the SerDes method for recovering margin lost to frequency-dependent channel loss, reflections, package/board discontinuities, crosstalk, and symbol-spaced ISI.

CTLE, FFE, and DFE solve different parts of the problem. CTLE boosts high-frequency content but also boosts noise and crosstalk. FFE shapes transmitted or digital samples but consumes swing and can enhance noise. DFE cancels postcursor ISI without directly amplifying input noise, but it can propagate decision errors.

## Canonical Sections

- [[ctle_ffe_dfe_notes]]
- [[pam4_receiver_basics]]
- [[serdes_architecture_overview]]
- [[pcie7_clocking_notes#11. Channel and Nyquist Implications]]

## Related Notes

- [[cdr_fundamentals]]
- [[cdr_jitter_tolerance]]
- [[pam4_adc_based_rx]]
