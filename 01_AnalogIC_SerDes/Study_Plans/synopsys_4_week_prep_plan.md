---

title: "Synopsys 4-Week Preparation Plan"
domain: "AnalogIC_SerDes"
tags:

* Synopsys
* PCIe7
* SerDes
* PLL
* CDR
* LDO
* ADC
* Clocking
* StudyPlan
  created: 2026-07-01
  updated: 2026-07-01
  source: "ChatGPT conversations and Synopsys role preparation"
  status: "active"

---

# Synopsys 4-Week Preparation Plan

## Purpose

This is a focused 4-week technical preparation plan before joining Synopsys as Analog Design, Senior Staff Engineer.

The first-year role direction is expected to involve:

* PCIe 7.0 clocking
* LDO
* Analog / mixed-signal IP work
* Possible later exposure to ADC / SerDes receiver-related topics

The goal is not to master every SerDes topic in 4 weeks. The goal is to build a strong technical map, refresh the most relevant circuit knowledge, and prepare for productive discussions after joining.

---

## Batch 2 Focus Update

The manual Batch 2 packet reinforces these priorities:

* Put PCIe 7.0 clocking first: PLL phase noise, integrated jitter, clock distribution, CDR behavior, and supply-induced jitter.
* Treat LDO preparation as SerDes power integrity: PSRR, output noise, stability, load transient, and supply-to-jitter conversion.
* Keep ADC-based PAM4 RX as the long-term bridge: TI-SAR mismatch, timing skew, sampling jitter, and DSP equalization.
* Prepare technical stories around LDO, ADC, PLL / DCO, and automation.
* Mark Synopsys internal architecture, jitter targets, CDR architecture, clocking implementation, and signoff flow as `待确认` until internal sources are available.

---

## Main Preparation Goals

By the end of this 4-week plan, I should be able to:

1. Explain the PCIe 7.0 / SerDes signal chain at a system level.
2. Understand how PLL / CDR / clocking blocks affect high-speed link performance.
3. Connect LDO noise, PSRR, stability, and transient response to SerDes clocking and analog IP.
4. Understand why ADC-based PAM4 receivers are used in 112G / 224G SerDes.
5. Prepare clear technical stories from prior analog IC experience.
6. Ask precise questions during Synopsys onboarding.

---

# Week 1: PCIe 7.0 and SerDes Architecture Overview

## Goal

Build the system-level map first.

Do not start with random PLL equations before understanding where the clock is used. That is how people become very confident and very lost.

## Topics

### PCIe 7.0 Basics

Study:

* PCIe 7.0 target data rate
* 128 GT/s meaning
* PAM4 signaling
* GT/s vs Gb/s
* x16 bandwidth
* Nyquist frequency
* Link training
* Equalization overview

Key questions:

* Why does PCIe 7.0 use PAM4?
* What is the relationship between 128 GT/s and actual data throughput?
* What does clocking need to support in PCIe 7.0?
* What are the main analog blocks inside a PCIe SerDes PHY?

## SerDes Signal Chain

Study the basic chain:

```text
TX data
↓
Serializer
↓
TX FFE / driver
↓
Package / channel
↓
CTLE
↓
ADC or slicer
↓
FFE / DFE / DSP
↓
CDR
↓
Deserializer
```

Key questions:

* What does each block do?
* Which blocks are analog?
* Which blocks are mixed-signal?
* Which blocks are mostly digital / DSP?
* Where do clocking and jitter matter most?

## Deliverables

Create or update these notes:

* `../SerDes/serdes_architecture_overview.md`
* `../SerDes/pcie7_overview.md`
* `../SerDes/pam4_receiver_basics.md`
* `../SerDes/ctle_ffe_dfe_notes.md`

Minimum content to write:

* One-page PCIe 7.0 summary
* One block diagram of SerDes RX / TX in text form
* List of unknowns to clarify later

## End-of-Week Check

I should be able to explain:

* What PCIe 7.0 is trying to achieve
* Why PAM4 is used
* What a SerDes PHY contains
* Where PLL / CDR / LDO / ADC fit into the system

---

# Week 2: PLL / CDR / Clocking

## Goal

Refresh and organize clocking knowledge for high-speed SerDes.

For Synopsys, this is probably the highest-value technical preparation area.

## Topics

### PLL Fundamentals

Study:

* Phase detector / PFD
* Charge pump
* Loop filter
* VCO / DCO
* Divider
* Loop bandwidth
* Lock behavior
* Reference spur
* Phase noise
* Jitter

Key questions:

* How does PLL phase noise translate to time-domain jitter?
* How does loop bandwidth affect reference noise and VCO noise?
* Why does charge pump mismatch create spur?
* What is the tradeoff between jitter filtering and tracking?

### CDR Fundamentals

Study:

* Why CDR is needed
* Phase tracking
* Data transition density
* Bang-bang CDR
* Linear CDR
* Jitter transfer
* Jitter tolerance
* Jitter generation

Key questions:

* How does a CDR recover clock from data?
* What is the difference between PLL and CDR?
* How does CDR interact with equalization?
* What happens when the channel has heavy ISI?

### Clocking in SerDes

Study:

* TX clock generation
* RX sampling clock
* Multi-phase clocks
* Clock distribution
* Jitter budget
* Supply noise sensitivity
* Interaction with LDO / power supply

Key questions:

* Which clock paths are most jitter-sensitive?
* How does supply noise modulate oscillator phase?
* Why does LDO design matter for SerDes clocking?

## Deliverables

Create or update:

* `../PLL_CDR_Clocking/pll_fundamentals.md`
* `../PLL_CDR_Clocking/cdr_fundamentals.md`
* `../PLL_CDR_Clocking/phase_noise_jitter.md`
* `../PLL_CDR_Clocking/pcie7_clocking_notes.md`
* `../ADC/sampling_jitter_adc.md`

Minimum content to write:

* PLL block diagram
* CDR block diagram
* Phase noise to jitter explanation
* List of common interview questions

## End-of-Week Check

I should be able to explain:

* PLL architecture and main tradeoffs
* CDR purpose and basic operation
* Difference between phase noise and jitter
* Why clocking is critical in PCIe 7.0 / SerDes

---

# Week 3: LDO / Bandgap / Power for SerDes

## Goal

Connect existing LDO / analog power experience to SerDes value.

This is important because my first-year work may include LDO, and the strongest career strategy is to present LDO knowledge not as isolated regulator work, but as part of SerDes clocking / analog IP performance.

## Topics

### LDO Fundamentals

Study:

* Error amplifier
* Pass device
* Feedback loop
* Load regulation
* Line regulation
* Dropout voltage
* Output capacitor
* ESR / zero
* Stability
* Load transient
* Line transient

Key questions:

* What determines LDO stability?
* How do load current and output capacitor affect phase margin?
* What are the dominant poles and zeros?
* How should worst-case corners be simulated?

### LDO PSRR

Study:

* Low-frequency PSRR
* Mid-frequency PSRR
* High-frequency PSRR
* Error amplifier gain
* Pass device output resistance
* Parasitic coupling
* Layout effects

Key questions:

* Why does PSRR degrade at high frequency?
* How does LDO PSRR affect PLL / clocking blocks?
* What is more important for SerDes: DC accuracy, noise, PSRR, transient response, or stability?

### Bandgap / Reference

Study:

* CTAT / PTAT
* Curvature correction basics
* Opamp offset
* Startup circuit
* Noise
* Supply sensitivity
* Temperature drift

Key questions:

* How does reference noise affect LDO output?
* How does bandgap accuracy affect analog IP?
* What are the common layout issues?

## SerDes Power Integrity Connection

Think in terms of system impact:

```text
Supply noise
↓
LDO output ripple / noise
↓
VCO / clock buffer phase modulation
↓
Sampling jitter
↓
Eye closure / BER degradation
```

This connection is critical. It turns ordinary LDO experience into SerDes-relevant experience.

## Deliverables

Create or update:

* `../LDO_Bandgap/ldo_fundamentals.md`
* `../LDO_Bandgap/ldo_psrr_notes.md`
* `../LDO_Bandgap/ldo_stability_notes.md`
* `../LDO_Bandgap/bandgap_reference_notes.md`
* `../LDO_Bandgap/serdes_power_integrity.md`

Minimum content to write:

* LDO loop diagram
* PSRR frequency-region explanation
* LDO-to-PLL noise impact chain
* 5 interview-ready LDO stories from previous work

## End-of-Week Check

I should be able to explain:

* LDO stability in a structured way
* PSRR across frequency
* Why LDO matters for SerDes
* How my previous LDO work is relevant to Synopsys PCIe / SerDes IP

---

# Week 4: ADC-Based PAM4 RX and Technical Story Preparation

## Goal

Build the bridge toward future ADC-based receiver work and prepare clean technical narratives.

This week is not about becoming an ADC-based SerDes architect overnight. Unfortunately, physics and hiring managers both object to that fantasy.

## Topics

### ADC-Based Receiver Basics

Study:

* Why PAM4 needs accurate amplitude information
* Slicer-based vs ADC-based RX
* CTLE before ADC
* ADC sampling clock
* DSP equalization after ADC
* FFE / DFE
* Timing recovery
* ENOB / SNDR / EVM
* Power vs performance tradeoff

Key questions:

* Why are ADC-based receivers used in high-speed PAM4 links?
* What ADC specifications matter most?
* How does sampling jitter affect ADC performance?
* How do offset, gain, and skew errors affect time-interleaved ADCs?

### TI-SAR ADC Calibration

Study:

* Time-interleaving
* Offset mismatch
* Gain mismatch
* Timing skew
* Background calibration
* Correlation-based skew detection
* Calibration convergence

Key questions:

* Why is timing skew especially harmful?
* How does skew create frequency-dependent error?
* What can be calibrated digitally?
* What must be improved in circuit design?

### Technical Story Preparation

Prepare technical stories using this structure:

```text
Project context
↓
Design challenge
↓
My responsibility
↓
Tradeoffs considered
↓
Simulation / silicon result
↓
Debugging / improvement
↓
What I learned
↓
How it connects to SerDes / Synopsys
```

Candidate story areas:

* LDO design
* Bandgap / reference
* SAR ADC
* Sigma-delta ADC
* PLL / DCO / ADPLL
* Automation / verification
* Debugging difficult corners
* Layout-sensitive analog blocks

## Deliverables

Create or update:

* `../ADC/adc_based_receiver.md`
* `../ADC/ti_sar_adc_calibration.md`
* `../ADC/sampling_jitter_adc.md`
* `../Interview_QA/technical_story_bank.md`
* `../Interview_QA/synopsys_relevant_qa.md`
* `../Papers_Books/core_serdes_papers.md`

Minimum content to write:

* ADC-based RX overview
* TI-SAR mismatch summary
* 3 polished technical stories
* 10 questions to ask Synopsys team after joining

## End-of-Week Check

I should be able to explain:

* Why ADC-based RX is important in modern PAM4 SerDes
* Basic TI-ADC calibration problems
* How my prior ADC / LDO / PLL experience supports the Synopsys role
* My first 90-day technical learning direction

---

# Weekly Time Allocation

Recommended time budget:

```text
Weekdays:
- 45 to 60 minutes per day

Weekends:
- 2 to 3 hours total
```

If time is limited:

```text
Minimum viable plan:
- Week 1: PCIe 7.0 / SerDes overview
- Week 2: PLL / CDR / jitter
- Week 3: LDO / PSRR / stability
- Week 4: ADC-based RX + technical stories
```

Do not try to read everything. Focus on notes that can be reused during onboarding.

---

# Daily Study Routine

Each study session should produce one small output.

Use this pattern:

```text
Read / review
↓
Write 5 to 10 bullet points
↓
Write 2 open questions
↓
Link the note to this plan
```

A session without written output is usually just intellectual window-shopping.

---

# Priority Questions for Synopsys Onboarding

Use these gradually after joining.

## Architecture Questions

* 待确认: What is the top-level PCIe 7.0 PHY architecture?
* 待确认: Which blocks are owned by the local team?
* 待确认: How are clocking, LDO, and analog IP responsibilities divided?
* 待确认: What is the most timing-sensitive or noise-sensitive block?

## Clocking Questions

* 待确认: What clocking architecture is used?
* 待确认: What are the dominant jitter contributors?
* 待确认: How is jitter budget allocated?
* 待确认: Which simulations are considered signoff-critical?

## LDO / Power Questions

* 待确认: Which blocks are powered by local LDOs?
* 待确认: What are the PSRR and noise requirements?
* 待确认: How is supply noise modeled?
* 待确认: What are the key stability corners?

## Career / Learning Questions

* 待确认: Which internal documents should I read first?
* 待确认: Which previous design should I study?
* 待确认: Who are the key technical experts for clocking / SerDes?
* 待确认: What should I be able to own after 90 days?

---

# Source Conversations / Source Packets

* `../../00_Inbox/manual_batches/batch2_serdes_pcie_pll_cdr_adc_2026-07-01/source_packet.md`

---

# Related Notes

* `../../02_Synopsys_Work/synopsys_master_note.md`
* `../../02_Synopsys_Work/onboarding_plan.md`
* `../analog_ic_serdes_master_index.md`
* `../SerDes/`
* `../PLL_CDR_Clocking/`
* `../ADC/`
* `../LDO_Bandgap/`
* `../Interview_QA/`
- `../SerDes/serdes_architecture_overview.md`
- `../SerDes/pam4_receiver_basics.md`
- `../SerDes/ctle_ffe_dfe_notes.md`
- `../PLL_CDR_Clocking/phase_noise_jitter.md`
- `../PLL_CDR_Clocking/pll_fundamentals.md`
- `../PLL_CDR_Clocking/cdr_fundamentals.md`
- `../PLL_CDR_Clocking/pcie7_clocking_notes.md`
- `../ADC/adc_based_receiver.md`
- `../ADC/ti_sar_adc_calibration.md`
- `../ADC/sampling_jitter_adc.md`
- `../LDO_Bandgap/serdes_power_integrity.md`
- `../LDO_Bandgap/ldo_psrr_notes.md`
- `../LDO_Bandgap/ldo_stability_notes.md`
- `../LDO_Bandgap/bandgap_reference_notes.md`
- `../Interview_QA/technical_story_bank.md`
- `../Interview_QA/synopsys_relevant_qa.md`
- `../Papers_Books/core_serdes_papers.md`
---

# Next Actions

1. Create the missing topic notes listed in this plan.
2. Start with `../SerDes/pcie7_overview.md`.
3. Then create `../PLL_CDR_Clocking/phase_noise_jitter.md`.
4. Then create `../LDO_Bandgap/ldo_psrr_notes.md`.
5. Update this file weekly as preparation progresses.

---

# Last Updated

2026-07-01
