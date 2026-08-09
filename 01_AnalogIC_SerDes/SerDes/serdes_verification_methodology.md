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
updated: 2026-08-08
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

## Boundary With PERC Reliability Checking

中文：SerDes link verification 和 PERC 电气可靠性检查解决不同问题。前者连接 channel、equalization、CDR、jitter 和 BER/margin；后者基于 schematic 或 extracted netlist 检查 DRC/LVS 不会自动证明的电气可靠性约束，例如 ESD/EOS 保护路径、电压域 crossing、thin-oxide 器件过压、body/well 连接和 HV/LV 器件误用。

English: SerDes link verification and PERC electrical-reliability checking answer different questions. Link verification connects the channel, equalization, CDR, jitter, and BER or margin; PERC checks electrical reliability constraints that DRC/LVS do not prove automatically, such as ESD/EOS protection paths, voltage-domain crossings, thin-oxide overstress, body/well connectivity, and HV/LV device misuse.

中文：Schematic PERC 依赖准确的 power-domain、pad/ESD cell、device-class 和 voltage-propagation 标注，适合在 layout 前查 topology 和可能的 terminal-voltage 组合。Layout PERC 再加入 guard ring、spacing、path resistance、current path 等物理上下文。工程上不应把 PERC 当作 LVS/DRC 的替代品，也不能在没有 foundry/company rule deck 和 mode/sequence 假设时把聊天中的 checklist 当作 signoff 证据。

English: Schematic PERC depends on correct power-domain, pad/ESD-cell, device-class, and voltage-propagation annotations; it is useful for topology and possible terminal-voltage combinations before layout. Layout PERC adds physical context such as guard rings, spacing, path resistance, and current paths. PERC is neither a replacement for LVS/DRC nor signoff evidence without the applicable foundry/company rule deck and explicit mode and sequencing assumptions.

Compact review checklist:

- normal, startup, shutdown, disabled, and power-sequencing modes;
- maximum permitted `VGS`, `VGD`, `VDS`, and `VGB` for each device class;
- pad-to-core ESD path and cross-domain level shifting or isolation;
- body, well, substrate, and floating-terminal connectivity;
- rule-deck version, domain annotations, waivers, and violation ownership.

## Related Notes

- [[serdes_architecture_overview]]
- [[ctle_ffe_dfe_notes]]
- [[pam4_adc_based_rx]]

## Source Conversations

- `../../00_Inbox/manual_batches/chat_delta_2026-08-08/new_conversations/6a4680a7-2fdc-83ea-be6a-25d108ea926b.md` - "PERC 检查原理"; conversation-derived synthesis, verification required against the applicable rule deck and official tool/foundry documentation.
