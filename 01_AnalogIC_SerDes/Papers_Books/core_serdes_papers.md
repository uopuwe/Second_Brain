---
title: "Core SerDes Papers"
domain: "AnalogIC_SerDes"
tags:
  - Papers
  - Books
  - References
  - SerDes
  - PCIe7
  - PAM4
  - PLL
  - CDR
  - ADC
created: 2026-07-01
updated: 2026-07-01
source: "ChatGPT technical notes and reading plan"
status: "active"
---

# Core SerDes Papers

## 中文补充翻译

这篇笔记用于规划 SerDes 相关论文和资料阅读。重点不是盲目收集论文，而是跟踪对 PCIe 7.0 / PAM4 / PLL / CDR / ADC-based RX / power integrity 真正有帮助的主题、指标和设计思路。

阅读 SerDes 论文时，应重点关注数据率、调制方式、UI、Nyquist、channel loss、equalization 架构、PLL/CDR jitter、power、area、process node、BER / bathtub / eye margin、测试条件和 measurement setup。不同论文之间的指标不能直接横向比较，必须确认测试条件、channel、package、supply、temperature 和是否包含实际 silicon measurement。

这份笔记的作用是建立阅读模板：读论文时先抓 architecture 和关键 tradeoff，再看哪些指标与 Synopsys PCIe 7.0 clocking、LDO、ADC receiver 或验证流程相关。

## Purpose

This note tracks core SerDes papers, books, and reading themes for long-term preparation.

The goal is to build a practical reading list around PCIe 7.0, PAM4 receivers, PLL / CDR, ADC-based RX, equalization, and SerDes power integrity.

---

## 1. Big Picture

The reading goal is not to collect papers endlessly.

The goal is to extract reusable design knowledge:

* architecture choices
* block diagrams
* performance metrics
* tradeoffs
* calibration methods
* jitter and noise analysis
* measurement approaches
* terminology used by experts

Useful output from each paper:

```text
one-page summary
down
key architecture diagram
down
main tradeoffs
down
interview-ready explanation
down
open questions
```

---

## 2. Key Concepts to Track

When reading SerDes papers, track:

* data rate and modulation
* NRZ vs PAM4
* process node
* channel loss
* TX equalization
* RX equalization
* CDR architecture
* PLL architecture
* ADC architecture if used
* DSP / adaptation
* power efficiency
* jitter tolerance
* BER target
* measured eye / bathtub
* calibration methods
* supply / reference strategy

Do not just copy headline data rate. Headline numbers are not understanding.

---

## 3. Priority Reading Themes

## PCIe 7.0 and Standards Context

Read public PCI-SIG material and reputable technical summaries for:

* 128 GT/s target
* PAM4 use
* bandwidth claims
* reliability goals
* backward compatibility
* PHY-level implications

## PAM4 SerDes Architecture

Look for papers on:

* 112G / 224G PAM4 links
* TX FFE and RX equalization
* ADC-based receivers
* baud-rate CDR
* DSP-assisted receiver architectures

## PLL / CDR

Look for:

* low-jitter PLLs
* phase interpolator CDRs
* bang-bang CDRs
* jitter tolerance methods
* supply-induced jitter analysis

## ADC-Based RX

Look for:

* time-interleaved ADCs
* TI-SAR ADC calibration
* ADC-based PAM4 receivers
* sampling jitter sensitivity
* digital equalization after ADC

## Power Integrity

Look for:

* LDOs for SerDes / PLL supply
* supply noise to jitter
* on-chip regulation
* decap and supply isolation
* reference noise impact

---

## 4. Candidate Source Venues

High-value venues:

* ISSCC
* JSSC
* CICC
* VLSI Symposium
* IEEE Solid-State Circuits Magazine
* IEEE Transactions on Circuits and Systems
* PCI-SIG public materials
* reputable university lecture notes
* analog / mixed-signal textbooks

Use public sources only unless reading approved internal Synopsys documents after joining.

---

## 5. Reading Template

Use this template for each paper:

```text
Title:
Authors:
Venue / year:
Data rate:
Modulation:
Process:
Architecture:
Key circuit blocks:
Main innovation:
Measured metrics:
Jitter / BER / power:
What I learned:
SerDes relevance:
Synopsys relevance:
Open questions:
```

This keeps reading output reusable.

---

## 6. SerDes / PCIe 7.0 Relevance

Papers are useful when they help answer:

* How do real high-speed PAM4 receivers partition analog and DSP?
* What clocking architectures are common?
* What jitter numbers are realistic?
* How are CDR and equalization coupled?
* What ADC specs matter in practice?
* How do designers measure margin?
* How is power efficiency achieved?

The point is to build intuition for real architecture tradeoffs, not memorize isolated paper titles.

---

## 7. Synopsys Preparation Relevance

For Synopsys preparation, reading should support:

* PCIe 7.0 clocking vocabulary
* SerDes architecture awareness
* LDO / power integrity system impact
* ADC-based receiver background
* better onboarding questions
* better long-term career positioning in SerDes IP

Do not infer confidential Synopsys design choices from public papers.

---

## 8. Interview Explanation

Short explanation:

```text
My SerDes reading plan focuses on extracting architecture and tradeoff knowledge from public papers rather than memorizing paper titles. For each paper, I want to understand the data rate, modulation, channel, TX / RX equalization, CDR, PLL, ADC use, calibration, jitter, BER, and power. The goal is to connect circuit-level techniques to link-level margin and to build vocabulary for PCIe 7.0 / PAM4 SerDes discussions.
```

---

## 9. Common Interview Questions

## Q1: How do you read a SerDes paper effectively?

Start with the architecture diagram, identify the main impairments, understand the equalization and clocking approach, then connect measured metrics to design tradeoffs.

## Q2: What metrics matter in SerDes papers?

Data rate, modulation, BER, channel loss, power efficiency, jitter, equalization capability, area, process, and measured margin.

## Q3: Why compare multiple papers?

To see recurring architecture patterns and tradeoffs instead of overfitting to one design.

## Q4: What should be treated carefully?

Headline data rates, unverified marketing claims, missing test conditions, and confidential implementation assumptions.

---

## 10. Open Questions

* Which public PCIe 7.0 technical references are most useful?
* Which 112G / 224G PAM4 receiver papers should be read first?
* Which ADC-based RX papers best explain timing recovery?
* Which PLL / CDR references are most relevant to PCIe?
* Which textbooks should be prioritized?
* What internal Synopsys reading list is recommended after onboarding?
* How should paper summaries be linked into the Second Brain?

---

## 11. Related Notes

* `../analog_ic_serdes_master_index.md`
* `../SerDes/pcie7_overview.md`
* `../SerDes/serdes_architecture_overview.md`
* `../SerDes/pam4_receiver_basics.md`
* `../SerDes/ctle_ffe_dfe_notes.md`
* `../PLL_CDR_Clocking/pcie7_clocking_notes.md`
* `../ADC/adc_based_receiver.md`
* `../Study_Plans/synopsys_4_week_prep_plan.md`

---

## 12. Next Actions

1. Add 5 to 10 concrete public paper titles after manual source selection.
2. Create one-page summaries for the first three papers.
3. Add a section for books and lecture notes.
4. Link paper summaries to the technical notes they support.

---

## Last Updated

2026-07-01
