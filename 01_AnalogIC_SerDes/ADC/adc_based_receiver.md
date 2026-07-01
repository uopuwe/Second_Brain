---

title: "ADC-Based Receiver"
domain: "AnalogIC_SerDes"
tags:

* ADC
* Receiver
* SerDes
* PAM4
* DSP
* Equalization
* CDR
* PCIe7
* Synopsys
  created: 2026-07-01
  updated: 2026-07-01
  source: "ChatGPT technical notes and Synopsys role preparation"
  status: "active"

---

# ADC-Based Receiver

## Purpose

This note summarizes ADC-based receiver architecture for high-speed PAM4 SerDes.

The goal is to understand why ADC-based RX is useful, what problems it solves, and what new problems it creates.

---

## 1. Big Picture

An ADC-based receiver digitizes the received waveform, then performs equalization, timing recovery support, calibration, and symbol decisions in digital logic or DSP.

Simplified chain:

```text
Channel
down
RX front-end / CTLE
down
ADC
down
DSP equalization
down
timing recovery / adaptation
down
PAM4 decisions
```

The architecture trades analog simplicity in some blocks for ADC performance, DSP complexity, and calibration burden.

---

## 2. Key Concepts

Important ADC-based RX concepts:

* front-end bandwidth
* sampling rate
* ADC resolution
* ENOB
* SNDR
* aperture jitter
* time-interleaving
* offset mismatch
* gain mismatch
* timing skew
* digital FFE
* DFE / MLSE-like processing if used
* timing error detection
* background calibration
* ADC reference noise
* DSP power
* latency

The key tradeoff:

```text
More digital flexibility
versus
ADC power, jitter sensitivity, and calibration complexity
```

---

## 3. Why ADC-Based RX Is Used

ADC-based RX can be attractive because:

* PAM4 needs amplitude information
* DSP can implement flexible equalization
* adaptation can be more programmable
* calibration can correct analog imperfections
* multiple channel conditions can be handled with digital algorithms
* process scaling favors digital logic

Compared with pure slicer-based RX, ADC-based RX gives more information to the digital backend.

---

## 4. ADC Requirements

Important ADC requirements:

* enough bandwidth for the received signal
* enough sampling rate for timing / equalization architecture
* enough resolution for PAM4 level separation
* low sampling jitter
* low input-referred noise
* good linearity
* manageable power
* robust calibration
* low reference noise
* stable behavior across PVT

For SerDes, the ADC is not judged only by standalone SNDR. It is judged by link margin after equalization and timing recovery.

---

## 5. Time-Interleaving

Very high sampling rates often require multiple ADC slices operating in parallel.

Time-interleaved ADC concept:

```text
ADC0 samples at t0
ADC1 samples at t1
ADC2 samples at t2
...
combined output creates high effective sample rate
```

Main mismatch errors:

* offset mismatch
* gain mismatch
* timing skew
* bandwidth mismatch

Timing skew is especially dangerous at high input frequency because it creates an error proportional to signal slope.

---

## 6. ADC and CDR

ADC-based RX can support digital timing recovery.

Timing recovery may use:

* raw ADC samples
* equalized samples
* decision-directed error
* interpolation
* Mueller-Muller-type timing error detection
* baud-rate or fractional-rate loops

Key question:

```text
Does timing recovery happen before, during, or after main equalization?
```

Architecture matters. There is no single universal answer.

---

## 7. SerDes / PCIe 7.0 Relevance

Modern high-speed PAM4 SerDes often consider ADC-based architectures because PAM4 benefits from digitized amplitude information and DSP equalization.

For PCIe 7.0 preparation, ADC-based RX is relevant even if the specific Synopsys implementation is unknown because it explains:

* why sampling clock jitter matters
* why time-interleaving calibration matters
* why LDO / reference noise matters
* why receiver design is now mixed-signal plus DSP
* why equalization and CDR are tightly connected

---

## 8. Synopsys Preparation Relevance

Useful preparation focus:

* explain ADC-based RX at block level
* understand TI-ADC mismatch and calibration
* connect sampling jitter to SNDR and link margin
* connect LDO and reference noise to ADC performance
* avoid claiming the actual Synopsys RX architecture without confirmation

Unknown internal details should stay in open questions.

---

## 9. Interview Explanation

Short explanation:

```text
An ADC-based SerDes receiver samples the incoming waveform and moves much of the equalization and decision logic into DSP. This is attractive for PAM4 because the receiver benefits from amplitude information and flexible digital equalization. The tradeoff is that the ADC must have enough bandwidth, resolution, low jitter, and calibration accuracy. Time-interleaving errors, sampling jitter, reference noise, and ADC power become major design concerns.
```

Synopsys-focused explanation:

```text
For PCIe 7.0 preparation, ADC-based RX helps me connect ADC, PLL, CDR, LDO, and DSP topics. Sampling jitter from clocking degrades ADC performance, reference and supply noise affect digitized amplitude, and calibration is needed for interleaved ADC mismatches. Even if my first work is clocking or LDO, those blocks directly support receiver margin.
```

---

## 10. Common Interview Questions

## Q1: Why use an ADC-based receiver for PAM4?

It captures amplitude information and enables flexible digital equalization, calibration, and adaptation.

## Q2: What are the main ADC-based RX drawbacks?

ADC power, sampling jitter sensitivity, time-interleaving mismatch, reference noise, DSP complexity, and latency.

## Q3: What mismatches matter in time-interleaved ADCs?

Offset, gain, timing skew, and bandwidth mismatch.

## Q4: Why is timing skew harmful?

A sample time error creates voltage error proportional to input slope. At high frequency, the slope is large.

## Q5: How does sampling jitter affect ADC-based RX?

It creates sample amplitude error, reducing SNDR and receiver margin.

---

## 11. Open Questions

* Is the relevant Synopsys PCIe 7.0 RX ADC-based?
* What ADC architecture is used if ADC-based RX is present?
* Is the ADC time-interleaved?
* What resolution and sample rate are required?
* How are offset, gain, skew, and bandwidth mismatch calibrated?
* How is sampling jitter budget allocated?
* How is ADC SNDR linked to PAM4 link margin?
* How are LDO and reference noise requirements derived?

---

## 12. Related Notes

* `ti_sar_adc_calibration.md`
* `sampling_jitter_adc.md`
* `../SerDes/pam4_receiver_basics.md`
* `../SerDes/serdes_architecture_overview.md`
* `../SerDes/ctle_ffe_dfe_notes.md`
* `../PLL_CDR_Clocking/cdr_fundamentals.md`
* `../PLL_CDR_Clocking/phase_noise_jitter.md`
* `../LDO_Bandgap/serdes_power_integrity.md`
* `../Study_Plans/synopsys_4_week_prep_plan.md`

---

## 13. Next Actions

1. Add a block diagram of ADC-based RX.
2. Add a table comparing slicer-based and ADC-based RX.
3. Add deeper notes on TI-SAR calibration.
4. Add paper references in `../Papers_Books/core_serdes_papers.md`.

---

## Last Updated

2026-07-01

