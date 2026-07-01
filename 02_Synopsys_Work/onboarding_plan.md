---
title: "Synopsys Onboarding Plan"
domain: "Synopsys_Work"
tags:
  - Synopsys
  - onboarding
  - first90days
  - PCIe7
  - LDO
created: 2026-07-01
updated: 2026-07-01
source: "ChatGPT conversations and role preparation"
status: "active"
---

# Synopsys Onboarding Plan

## 中文补充翻译

这份 onboarding 计划的目标，是在加入 Synopsys 前后围绕 PCIe 7.0 clocking 和 LDO 建立清晰的准备路径。重点不是被动适应入职流程，而是尽快理解团队、项目、文档、工具和当前设计压力，并在早期就能对团队产生实际帮助。

入职前应重点复习 PCIe 7.0、SerDes 架构、PLL/CDR/clocking、jitter / phase noise、PAM4、LDO stability、LDO PSRR、bandgap reference 和 ADC-based receiver。第一周主要确认团队结构、工具账号、项目现状和直接职责；前 30/60/90 天逐步从读文档、跑仿真、理解 block ownership，过渡到能独立承担小范围设计或验证任务。

这篇笔记里的英文问题清单可以保留原样，因为它们适合直接用于和 manager、mentor、HR 或 benefits provider 沟通。

## Goal

Prepare for joining Synopsys as Analog Design, Senior Staff Engineer, with a first-year focus on PCIe 7.0 clocking and LDO.

The goal is not just to survive onboarding, but to quickly become useful in the team and build a strong path toward SerDes / ADC-based receiver work.

## Before Start Date

Start date: August 17, 2026.

### Technical Preparation

Focus on:

- PCIe 7.0 overview
- SerDes architecture
- PLL / CDR / clocking
- Jitter and phase noise
- PAM4 signaling
- LDO stability
- LDO PSRR
- Bandgap reference
- ADC-based receiver basics

### Practical Preparation

- Confirm start date and onboarding logistics
- Confirm benefits start date
- Confirm dental coverage details
- Prepare questions for manager
- Organize prior project experience into Synopsys-relevant stories
- Prepare short self-introduction for team meetings

## First Week

### Main Goals

- Understand team structure
- Understand current project status
- Set up tools and accounts
- Learn internal documentation system
- Clarify immediate responsibilities

### Questions to Ask

- What block am I expected to work on first?
- What is the current schedule pressure?
- Who owns clocking?
- Who owns LDO?
- Who owns verification?
- What documents should I read first?
- What prior project or test chip should I study?

## First 30 Days

### Main Goals

- Understand the PCIe 7.0 IP architecture at a high level
- Understand the clocking architecture
- Understand LDO requirements and constraints
- Read existing design documents
- Reproduce key simulations if possible
- Build trust by asking precise technical questions

### Deliverables

- Internal notes on architecture
- Block-level understanding of assigned design
- Simulation setup familiarity
- List of design risks and open questions

## First 60 Days

### Main Goals

- Become productive in assigned block
- Understand design tradeoffs
- Start contributing to simulation / debugging / review
- Learn team coding, documentation, and review style

### Technical Focus

- Clocking path
- Jitter budget
- Power supply noise
- LDO stability and PSRR
- Corner simulation
- Monte Carlo
- Layout-sensitive issues

## First 90 Days

### Main Goals

- Own a meaningful part of the work
- Be seen as reliable and technically strong
- Identify path toward deeper SerDes work
- Build relationship with manager and key technical people

### Possible Contributions

- Improve simulation coverage
- Debug circuit issues
- Create comparison tables
- Summarize design tradeoffs
- Help close review items
- Prepare clean technical documentation

## Manager 1:1 Topics

Use these questions gradually, not all at once like a confused interrogation robot.

### Role Clarification

- What are the top priorities for my first 3 months?
- Which block should I focus on first?
- What does success look like by the end of 90 days?

### Technical Direction

- How is the PCIe 7.0 clocking architecture organized?
- What are the biggest technical risks in the current design?
- How does the LDO interact with the SerDes clocking / analog blocks?

### Career Direction

- What skills should I build to move deeper into SerDes architecture?
- Is there a path toward ADC / receiver-related work later?
- Which internal experts should I learn from?

## Personal Strategy

Do:

- Ask precise questions.
- Keep private notes.
- Learn internal flow quickly.
- Document what I understand.
- Connect LDO / PLL / CDR knowledge to SerDes context.
- Build reputation quietly through useful work.

Avoid:

- Over-talking.
- Acting like I already know the internal architecture.
- Revealing too much external job strategy.
- Asking career-jump questions too early.
- Getting trapped only in low-level support work without learning the architecture.

## Related Notes

- `synopsys_master_note.md`
- `benefits_dental.md`
- `../01_AnalogIC_SerDes/analog_ic_serdes_master_index.md`

## Last Updated

2026-07-01
