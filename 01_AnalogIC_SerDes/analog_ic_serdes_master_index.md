---

title: "Analog IC / SerDes Master Index"
domain: "AnalogIC_SerDes"
tags:

* AnalogIC
* SerDes
* PCIe7
* PLL
* CDR
* ADC
* LDO
* Bandgap
* Interview
  created: 2026-07-01
  updated: 2026-07-01
  source: "ChatGPT conversations, interview preparation, work notes"
  status: "active"

---

# Analog IC / SerDes Master Index

## Purpose

This is the central technical index for my Analog IC, SerDes, PCIe 7.0, PLL / CDR, ADC, LDO, and interview preparation notes.

The goal is to organize long-term technical knowledge for:

* Synopsys onboarding
* PCIe 7.0 clocking work
* LDO / power block work
* SerDes architecture learning
* ADC-based receiver preparation
* Future career transition toward high-speed SerDes / Marvell-level roles

This file is the map. Detailed notes should live in subfolders.

---

## Current Career Direction

My current technical transition path is:

```text
General analog IC / LDO background
↓
PCIe 7.0 clocking and LDO at Synopsys
↓
SerDes clocking / PLL / CDR
↓
ADC-based PAM4 receiver understanding
↓
112G / 224G SerDes architecture
↓
Senior / principal-level SerDes roles
```

The main goal is to convert existing analog IC experience into credible high-speed SerDes IP experience.

---

## Main Technical Domains

## 1. SerDes Architecture

Folder:

```text
01_AnalogIC_SerDes/SerDes/
```

Use this area for:

* 112G / 224G SerDes
* PAM4 architecture
* TX / RX signal chain
* Channel loss and equalization
* CTLE / FFE / DFE
* ADC-based receiver
* Jitter budget
* Link training
* Eye diagram and bathtub curve
* BER / SER analysis

Important future files:

* `serdes_architecture_overview.md`
* `pam4_receiver_basics.md`
* `ctle_ffe_dfe_notes.md`
* `112g_224g_serdes_notes.md`
* `serdes_jitter_budget.md`

---

## 2. PCIe 7.0

Folder:

```text
01_AnalogIC_SerDes/SerDes/
```

Use this area for:

* PCIe 7.0 basics
* 128 GT/s signaling
* PAM4 in PCIe 7.0
* Clocking requirements
* Link architecture
* Equalization
* Jitter tolerance
* Synopsys PCIe 7.0 IP preparation

Important future files:

* `pcie7_overview.md`
* `pcie7_clocking_requirements.md`
* `pcie7_serdes_architecture.md`

Key concepts to track:

* GT/s vs Gb/s
* PAM4 symbol rate
* Nyquist frequency
* x16 bandwidth
* Jitter requirements
* Clock generation and distribution

---

## 3. PLL / CDR / Clocking

Folder:

```text
01_AnalogIC_SerDes/PLL_CDR_Clocking/
```

Use this area for:

* PLL fundamentals
* CPPLL
* ADPLL
* CDR
* Clock generation
* Clock distribution
* Phase noise
* Jitter transfer
* Jitter tolerance
* PFD / charge pump
* Loop bandwidth
* VCO / DCO
* Injection-locked oscillator
* DLL / ILO if relevant

Important future files:

* `pll_fundamentals.md`
* `cdr_fundamentals.md`
* `phase_noise_jitter.md`
* `pcie7_clocking_notes.md`
* `pfd_charge_pump_notes.md`
* `clocking_interview_qa.md`

Key questions:

* How does PLL phase noise translate to jitter?
* How does CDR track incoming data phase?
* What is the relationship between loop bandwidth and jitter filtering?
* How should clocking be designed for high-speed SerDes?
* What matters most for PCIe 7.0 clocking?

---

## 4. ADC / ADC-Based Receiver

Folder:

```text
01_AnalogIC_SerDes/ADC/
```

Use this area for:

* SAR ADC
* TI-SAR ADC
* ADC-based PAM4 receiver
* Offset / gain / skew calibration
* Sampling clock jitter
* ENOB / SNDR / EVM
* Background calibration
* Comparator design
* ADC front-end limitations

Important future files:

* `adc_based_receiver.md`
* `ti_sar_adc_calibration.md`
* `sampling_jitter_adc.md`
* `sar_adc_interview_qa.md`
* `adc_serdes_receiver_tradeoffs.md`

Key questions:

* Why do modern high-speed PAM4 receivers use ADC-based architectures?
* How does TI-SAR calibration work?
* How do offset, gain, and skew mismatch affect the receiver?
* How does sampling jitter limit SNDR?
* What ADC specs matter most for SerDes?

---

## 5. LDO / Bandgap / Power

Folder:

```text
01_AnalogIC_SerDes/LDO_Bandgap/
```

Use this area for:

* LDO stability
* LDO PSRR
* Load transient response
* Line transient response
* Bandgap reference
* POR / BOR
* Power supply noise
* SerDes power integrity
* Regulator interaction with PLL / clocking blocks

Important future files:

* `ldo_fundamentals.md`
* `ldo_psrr_notes.md`
* `ldo_stability_notes.md`
* `bandgap_reference_notes.md`
* `serdes_power_integrity.md`

Key questions:

* How does LDO noise affect PLL / CDR performance?
* What determines LDO PSRR at low, mid, and high frequency?
* How should LDO stability be analyzed across load and corner?
* What are the layout-sensitive issues in LDO and bandgap design?

---

## 6. Interview Q&A

Folder:

```text
01_AnalogIC_SerDes/Interview_QA/
```

Use this area for:

* Synopsys interview questions
* Marvell interview preparation
* PLL Q&A
* ADC Q&A
* LDO Q&A
* SerDes Q&A
* Behavioral technical stories
* Whiteboard problem summaries

Important future files:

* `serdes_interview_qa.md`
* `pll_cdr_interview_qa.md`
* `adc_interview_qa.md`
* `ldo_bandgap_interview_qa.md`
* `synopsys_interview_summary.md`
* `marvell_interview_prep.md`

Key interview themes:

* Explain design tradeoffs clearly.
* Connect circuit-level details to system-level impact.
* Show ownership and debugging ability.
* Avoid sounding like a textbook with a pulse.

---

## 7. Papers / Books / References

Folder:

```text
01_AnalogIC_SerDes/Papers_Books/
```

Use this area for:

* ISSCC / JSSC / CICC papers
* SerDes textbooks
* PLL / CDR references
* ADC references
* PCIe specifications and summaries
* Synopsys / Cadence / Marvell technical materials

Important future files:

* `core_serdes_papers.md`
* `pll_cdr_books.md`
* `adc_books_papers.md`
* `pcie7_references.md`
* `reading_log.md`

Important references to track later:

* 224 Gb/s SerDes papers
* ADC-based PAM4 receiver papers
* PCIe 7.0 technical summaries
* PLL / CDR classic materials
* Razavi analog / RF / optical communication IC books
* High-speed link design references

---

## 8. Study Plans

Folder:

```text
01_AnalogIC_SerDes/Study_Plans/
```

Use this area for:

* 4-week Synopsys preparation plan
* 2-month PCIe 7.0 / SerDes plan
* PLL / CDR focused plan
* ADC-based receiver plan
* LDO / power refresh plan

Important future files:

* `synopsys_4_week_prep_plan.md`
* `pcie7_serdes_2_month_plan.md`
* `pll_cdr_study_plan.md`
* `adc_receiver_study_plan.md`

---

## Current Priority List

## Priority 1: Synopsys First-Year Preparation

Focus:

* PCIe 7.0 clocking
* LDO
* SerDes system overview
* PLL / CDR fundamentals
* Power noise impact on clocking

Related note:

```text
../02_Synopsys_Work/synopsys_master_note.md
```

---

## Priority 2: PLL / CDR / Clocking

Focus:

* PLL loop basics
* Phase noise to jitter
* Jitter transfer and jitter tolerance
* CDR architecture
* Clock distribution
* PCIe clocking requirements

---

## Priority 3: ADC-Based PAM4 Receiver

Focus:

* Why ADC-based RX is used
* TI-SAR architecture
* Calibration
* Sampling jitter
* Equalization after ADC
* ENOB / SNDR / EVM

---

## Priority 4: LDO / Bandgap Refresh

Focus:

* LDO stability
* PSRR
* Load transient
* Noise
* Bandgap accuracy
* Interaction with PLL / SerDes blocks

---

## Knowledge Rules

1. Keep raw chat records in `00_Inbox`.
2. Move reusable technical summaries into this folder.
3. Do not mix career logistics with technical notes.
4. Do not create too many tiny files too early.
5. Every major topic should eventually have:

   * overview note
   * key equations
   * design tradeoffs
   * interview Q&A
   * open questions
   * references
6. Mark uncertain claims as `待确认`.
7. Prefer clear technical explanations over copied chat transcripts.

---

## Open Technical Questions

* What exact PCIe 7.0 clocking blocks will I work on at Synopsys?
* How much CDR architecture exposure will I get?
* Will my first-year work connect directly to SerDes receiver architecture?
* Which PLL / CDR topics should be mastered before start date?
* Which ADC-based receiver papers are most relevant to 112G / 224G PAM4?
* How should I connect my LDO experience to SerDes IP value?
* What technical stories should I prepare for future Marvell-level interviews?

---

## Related Notes

* `../02_Synopsys_Work/synopsys_master_note.md`
* `../02_Synopsys_Work/onboarding_plan.md`
* `../02_Synopsys_Work/benefits_dental.md`
* `SerDes/`
* `PLL_CDR_Clocking/`
* `ADC/`
* `LDO_Bandgap/`
* `Interview_QA/`
* `Papers_Books/`
* `Study_Plans/`

---

## Last Updated

2026-07-01
