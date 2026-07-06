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
updated: 2026-07-05
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

## 13. Ingested Books / Cornerstone References

This section records source-backed material that has been ingested into the vault, so any durable note citing it has a single citation anchor.

### B1. El-Chammas & Murmann — Background Calibration of Time-Interleaved Data Converters

- **Citation:** M. El-Chammas and B. Murmann, *Background Calibration of Time-Interleaved Data Converters*, Analog Circuits and Signal Processing series, Springer, 2012. ISBN 978-1-4614-1510-7 (e-ISBN 978-1-4614-1511-4), DOI 10.1007/978-1-4614-1511-4. 138 pp.
- **One-sentence value:** The definitive monograph on modeling and background-calibrating time-interleaved ADCs, with closed-form offset/gain/timing-skew bounds and a statistics-based cross-correlation timing-skew calibration demonstrated on a 5-bit, 12-GS/s flash ADC in 65 nm CMOS.
- **Reading status:** Deep Ingest completed 2026-07-04 (Ch. 2 error analysis, Ch. 3 calibration algorithm, Appendices D–E). Ch. 4–6 (comparator power optimization, circuit design, measurements) reviewed at summary level.
- **Chapter map:** Ch. 2 TI-ADC model + mismatch bounds; Ch. 3 background timing-skew calibration; Ch. 4 architecture/comparator-power optimization; Ch. 5 circuit design (bootstrapped T&H, dynamic comparator, delay line); Ch. 6 measurements; App. A WSCS signals; App. B comparator power; App. D comparator skew; App. E residual-skew/jitter extraction.
- **Promoted into:** [[ti_sar_mismatch_calibration]] (bounds + calibration algorithm; canonical TI-SAR note), [[sampling_jitter_adc]] (quantization-referenced jitter bound, comparator skew), [[ti_adc_calibration_moc]] (MOC).
- **Archived source:** `../../90_Archive/processed/2026/books/background_calibration_of_ti_data_converters/`.
- **Verification note:** formulas re-derived here; the book's printed gain-mismatch numeric example is marked `待确认` pending primary-source recheck.

---

### B2. Rhee & Yu - Phase-Locked Loops

- **Citation:** W. Rhee and Z. Yu, *Phase-Locked Loops: System Perspectives and Circuit Design Aspects*, Wiley/IEEE Press, 2024. 383 pp.
- **One-sentence value:** A system-to-circuit PLL textbook that connects linear loop dynamics, transient response, spectral purity, PFD/CP/VCO/divider circuit design, fractional-N PLLs, digital-intensive PLLs, and CDR PLLs.
- **Reading status:** Deep Ingest completed 2026-07-05. The ingest prioritized Ch. 2 loop dynamics, Ch. 4 spectral purity, Ch. 6 PFD/charge pump, Ch. 9 fractional-N PLL, Ch. 10 digital-intensive PLL, and Ch. 11 CDR PLL; remaining chapters were reviewed at source-routing level.
- **Chapter map:** Ch. 2 linear model and loop dynamics; Ch. 3 transient response; Ch. 4 frequency and spectral purity; Ch. 5 application aspects; Ch. 6 phase detector and charge pump; Ch. 7 VCO; Ch. 8 divider; Ch. 9 fractional-N PLL; Ch. 10 digital-intensive PLL; Ch. 11 CDR PLL.
- **Promoted into:** [[pll_fundamentals]] (loop dynamics and CPPLL sizing), [[pll_phase_noise_jitter]] (spur, jitter, spectral purity), [[pfd_charge_pump_notes]] (PFD/CP canonical note), [[pll_fractional_n_digital]] (fractional-N, DSM, DPLL, BBPLL, HPLL canonical note), [[cdr_fundamentals]] (JGEN/JTRAN/JTOL and CDR detectors).
- **Archived source:** `../../90_Archive/processed/2026/books/phase_locked_loops_rhee_yu_2024/`.
- **Verification note:** formulas were promoted as engineering models, not PCIe compliance requirements. Project signoff still requires PVT-aware circuit simulation, behavioral PLL/CDR modeling, and applicable internal/spec-level jitter masks.

---

### B3. Staszewski & Balsara - All-Digital Frequency Synthesizer

- **Citation:** R. B. Staszewski and P. T. Balsara, *All-Digital Frequency Synthesizer in Deep-Submicron CMOS*, Wiley, 2006.
- **One-sentence value:** A cornerstone ADPLL book that explains phase-domain ADPLL architecture, DCO/TDC normalization, digitally controlled oscillators, fractional DCO dithering, direct frequency modulation, frequency synthesis, and built-in self-test in deep-submicron CMOS.
- **Reading status:** Balanced Ingest completed 2026-07-05. The ingest promoted architecture-level ADPLL/DCO/TDC knowledge only; a future Deep Ingest is appropriate if ADPLL becomes a primary design or interview focus.
- **Chapter map:** Ch. 2 DCO; Ch. 3 normalized DCO; Ch. 4 ADPLL; Ch. 5 phase-domain modeling; Ch. 6 digital direct frequency modulation; Ch. 7 frequency synthesis; Ch. 8 system integration; Ch. 9 built-in self-test.
- **Promoted into:** [[adpll_notes]].
- **Archived source:** `../../90_Archive/processed/2026/books/all_digital_frequency_synthesizer_staszewski_balsara_2006/`.
- **Verification note:** Bluetooth/RF implementation details are reusable for ADPLL architecture intuition, not direct PCIe/SerDes jitter targets.

---

## 14. Ingested PLL / Oscillator Sources

This section records source-backed PLL and oscillator material promoted into canonical clocking notes.

### P1. Hanumolu et al. - Analysis of Charge-Pump Phase-Locked Loops

- **Citation:** P. K. Hanumolu, M. Brownlee, K. Mayaram, and U.-K. Moon, "Analysis of Charge-Pump Phase-Locked Loops," IEEE Transactions on Circuits and Systems I: Regular Papers, Vol. 51, No. 9, pp. 1665-1674, September 2004.
- **One-sentence value:** A state-space and sampled-data treatment of third-order CPPLLs that clarifies lock acquisition, small-signal tracking, noise transfer, and update-rate stability limits.
- **Promoted into:** [[pll_fundamentals]].
- **Archived source:** `../../90_Archive/processed/2026/papers/pll_oscillator_sources_2026-07-05/`.

### P2. Razavi - Jitter-Power Trade-Offs in PLLs

- **Citation:** B. Razavi, "Jitter-Power Trade-Offs in PLLs," IEEE Transactions on Circuits and Systems I: Regular Papers, Vol. 68, No. 4, pp. 1381-1387, April 2021.
- **One-sentence value:** A first-order lower-bound analysis showing why low-femtosecond PLL jitter becomes power-expensive, especially when reference and charge-pump noise are included.
- **Promoted into:** [[pll_phase_noise_jitter]].
- **Archived source:** `../../90_Archive/processed/2026/papers/pll_oscillator_sources_2026-07-05/`.

### P3. Razavi - The Ring Oscillator

- **Citation:** B. Razavi, "The Ring Oscillator," IEEE Solid-State Circuits Magazine, Fall 2019.
- **One-sentence value:** A practical tutorial on inverter and differential ring oscillators, including delay, power, supply sensitivity, multiphase generation, FOM, and LDO-noise implications.
- **Promoted into:** [[pll_phase_noise_jitter]].
- **Archived source:** `../../90_Archive/processed/2026/papers/pll_oscillator_sources_2026-07-05/`.

### P4. PLL Architecture Review Sources

- **Sources:** Nguyen and Pham, "An Overview of Phase-Locked Loop: From Fundamentals to the Frontier," Sensors, 2025; Dutta et al., "Exploring the Landscape of Phase-Locked Loop Architectures: A Comprehensive Review."
- **One-sentence value:** Broad taxonomy and vocabulary support for PLL architecture routing; not used as primary formula authority.
- **Promoted into:** [[pll_fundamentals]].
- **Archived source:** `../../90_Archive/processed/2026/papers/pll_oscillator_sources_2026-07-05/`.

### P5. Hajimiri and Lee - A General Theory of Phase Noise in Electrical Oscillators

- **Citation:** A. Hajimiri and T. H. Lee, "A General Theory of Phase Noise in Electrical Oscillators," IEEE Journal of Solid-State Circuits, Vol. 33, No. 2, pp. 179-194, February 1998.
- **One-sentence value:** The classic impulse-sensitivity-function treatment of oscillator phase noise, including periodically time-varying noise conversion, flicker upconversion, cyclostationary noise, and waveform-symmetry design rules.
- **Promoted into:** [[pll_phase_noise_jitter]].
- **Archived source:** `../../90_Archive/processed/2026/papers/hajimiri_gao_pll_sources_2026-07-05/`.

### P6. Gao et al. - Low-Noise Sub-Sampling PLL

- **Citation:** X. Gao, E. A. M. Klumperink, M. Bohsali, and B. Nauta, "A Low Noise Sub-Sampling PLL in Which Divider Noise is Eliminated and PD/CP Noise is Not Multiplied by $N^2$," IEEE Journal of Solid-State Circuits, Vol. 44, No. 12, pp. 3253-3263, December 2009.
- **One-sentence value:** A source-backed explanation of why sub-sampling PLLs can remove divider noise in lock and avoid the conventional $N^2$ PD/CP noise penalty, while shifting attention to reference-buffer noise, acquisition, and spur control.
- **Promoted into:** [[pll_phase_noise_jitter]].
- **Archived source:** `../../90_Archive/processed/2026/papers/hajimiri_gao_pll_sources_2026-07-05/`.

### P7. Da Dalt - Digital Bang-Bang Frequency Synthesizers

- **Citation:** N. Da Dalt, *Theory and Implementation of Digital Bang-Bang Frequency Synthesizers for High Speed Serial Data Communications*, Ph.D. dissertation, RWTH Aachen University, 2007.
- **One-sentence value:** A design-oriented nonlinear treatment of digital bang-bang PLLs, including phase-plane orbits, loop-latency-driven limit-cycle jitter, BPD gain dependence on untracked jitter, and a 130 nm CMOS high-bandwidth synthesizer case study.
- **Promoted into:** [[pll_fractional_n_digital]] and [[cdr_fundamentals]].
- **Archived source:** `../../90_Archive/processed/2026/articles/digital_bang_bang_frequency_synthesizers_da_dalt_2007/`.

### P8. Chen et al. - 529-uW Fractional-N ADPLL

- **Citation:** P. Chen, X. Meng, J. Yin, P.-I. Mak, R. P. Martins, and R. B. Staszewski, "A 529-uW Fractional-N All-Digital PLL Using TDC Gain Auto-Calibration and an Inverse-Class-F DCO in 65-nm CMOS," IEEE Transactions on Circuits and Systems I: Regular Papers, Vol. 69, No. 1, pp. 51-62, January 2022, DOI 10.1109/TCSI.2021.3094094.
- **One-sentence value:** A low-power DTC-assisted fractional-N ADPLL case study showing hybrid TDC range extension, background TDC gain calibration, DTC mismatch/spur tradeoffs, snapshot timing, and PVT-robust inverse-class-F DCO design.
- **Promoted into:** [[pll_fractional_n_digital]] and [[pll_phase_noise_jitter]].
- **Archived source:** `../../90_Archive/processed/2026/papers/chen_529uw_fractional_n_adpll_2022/`.

### P9. Staszewski et al. - All-Digital TX Frequency Synthesizer and Discrete-Time Receiver

- **Citation:** R. B. Staszewski et al., "All-Digital TX Frequency Synthesizer and Discrete-Time Receiver for Bluetooth Radio in 130-nm CMOS," IEEE Journal of Solid-State Circuits, 2004, DOI 10.1109/JSSC.2004.836345.
- **One-sentence value:** A silicon case study replacing conventional VCO/PFD/CP synthesis with DCO/TDC-based phase-domain ADPLL operation, including DCO fractional dithering, retimed reference operation, TDC normalization, and digital frequency modulation.
- **Promoted into:** [[adpll_notes]].
- **Archived source:** `../../90_Archive/processed/2026/papers/staszewski_all_digital_tx_synthesizer_bluetooth_2004/`.

### P10. Da Dalt - Nonlinear Dynamics of Digital Bang-Bang PLLs

- **Citation:** N. Da Dalt, "A Design-Oriented Study of the Nonlinear Dynamics of Digital Bang-Bang PLLs," IEEE Transactions on Circuits and Systems I: Regular Papers, Vol. 52, No. 1, January 2005, DOI 10.1109/TCSI.2004.840089.
- **One-sentence value:** A concise peer-reviewed nonlinear BBPLL source explaining why locked bang-bang loops form phase-plane orbits/limit cycles and how loop delay changes jitter and stability.
- **Promoted into:** [[pll_fractional_n_digital]] and [[cdr_fundamentals]].
- **Archived source:** `../../90_Archive/processed/2026/papers/da_dalt_nonlinear_dynamics_bbpll_2005/`.

### P11. Designing Bang-Bang PLLs for Clock and Data Recovery

- **Citation:** "Designing Bang-Bang PLLs for Clock and Data Recovery in Serial Data Transmission."
- **One-sentence value:** A CDR-oriented bang-bang PLL source with first-order phase-step equations, lock range, hunting jitter, duty-cycle/frequency-offset relation, slope-overload intuition, and second-order stability-factor framing.
- **Promoted into:** [[cdr_fundamentals]].
- **Archived source:** `../../90_Archive/processed/2026/papers/bang_bang_plls_cdr_serial_data_transmission/`.
- **Verification note:** Author metadata was not confidently extracted during Balanced Ingest; cite by title until the PDF front matter is manually verified.

### P12. Zhang - CMOS Analog and Mixed-Signal PLL Overview

- **Citation:** Z. Zhang, "CMOS analog and mixed-signal phase-locked loops: An overview," *Journal of Semiconductors*, Vol. 41, No. 11, 111402, 2020, DOI 10.1088/1674-4926/41/11/111402.
- **One-sentence value:** A compact AMS/CPPLL review that reinforces recurring CPPLL architecture issues, including CP mismatch, loop-filter ripple, fractional-N PFD/CP nonlinearity, bandwidth/settling tradeoff, divider noise, and AMS versus ADPLL selection.
- **Promoted into:** [[pfd_charge_pump_notes]].
- **Archived source:** `../../90_Archive/processed/2026/papers/zhang_cmos_ams_pll_overview_2020/`.

### P13. Dutta et al. - PLL Architecture Review Duplicate Source

- **Citation:** Dutta et al., "Exploring the Landscape of Phase-Locked Loop Architectures: A Comprehensive Review," IEEE Access, 2024, DOI 10.1109/ACCESS.2024.3446393.
- **One-sentence value:** Duplicate incoming copy of a broad PLL architecture taxonomy source already represented in P4; no new durable note update was needed.
- **Promoted into:** No additional promotion in this batch.
- **Archived source:** `../../90_Archive/processed/2026/papers/duplicate_dutta_pll_architecture_review_2024/`.

---

## Last Updated

2026-07-05
