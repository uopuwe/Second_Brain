---

title: "Synopsys Relevant Q&A"
domain: "AnalogIC_SerDes"
tags:

* Synopsys
* Interview
* Q&A
* PCIe7
* SerDes
* PLL
* CDR
* LDO
* ADC
  created: 2026-07-01
  updated: 2026-07-01
  source: "ChatGPT technical notes and Synopsys role preparation"
  status: "active"

---

# Synopsys Relevant Q&A

## Purpose

This note collects technical Q&A most relevant to Synopsys Analog Design / SerDes / PCIe 7.0 preparation.

The goal is to practice concise explanations that connect analog circuit knowledge to PHY-level impact.

---

## 1. Big Picture

The expected preparation themes are:

* PCIe 7.0 PHY basics
* SerDes architecture
* PLL / CDR / clocking
* LDO / power integrity
* bandgap / reference
* ADC-based PAM4 receiver basics
* technical ownership stories

The strongest answers should follow this pattern:

```text
define concept
down
explain circuit mechanism
down
connect to SerDes metric
down
mention practical verification
```

---

## 2. Key Concepts

High-value concepts:

* PAM4 margin
* jitter and phase noise
* PLL loop bandwidth
* CDR jitter tolerance
* supply-induced jitter
* LDO PSRR
* LDO stability
* reference noise
* CTLE / FFE / DFE
* ADC sampling jitter
* TI-ADC calibration
* PVT / Monte Carlo / post-layout verification

---

## 3. SerDes / PCIe 7.0 Questions

## Q1: What matters most in PCIe 7.0 PHY design?

PCIe 7.0 uses 128 GT/s PAM4 signaling, so the PHY must manage tight timing and voltage margins. The key topics are channel loss, equalization, PLL / CDR jitter, PAM4 receiver accuracy, power integrity, calibration, and link training.

## Q2: Why is PAM4 used?

PAM4 carries 2 bits per symbol, improving bandwidth efficiency without requiring the same proportional increase in symbol rate. The penalty is smaller vertical eye opening and higher sensitivity to noise, nonlinearity, offset, and jitter.

## Q3: What blocks are inside a SerDes PHY?

Serializer, TX FFE and driver, channel interface, RX CTLE, slicer or ADC, FFE / DFE / DSP, CDR, PLL, clock distribution, references, LDOs, calibration, and deserializer.

---

## 4. PLL / CDR Questions

## Q4: How does PLL phase noise affect SerDes?

PLL phase noise becomes timing jitter. That jitter moves TX launch or RX sampling edges and closes the eye horizontally, reducing BER margin.

## Q5: How does PLL bandwidth affect jitter?

Inside the loop bandwidth, reference and in-loop noise are transferred more strongly. Outside the loop bandwidth, VCO noise often dominates. Bandwidth trades off VCO noise suppression, reference noise transfer, spur, stability, and lock time.

## Q6: What is CDR?

CDR recovers the sampling clock phase from incoming data transitions. It adjusts the sampling phase so the receiver samples near the eye center.

## Q7: What are jitter transfer, tolerance, and generation?

Jitter transfer describes how input jitter passes through the CDR. Jitter tolerance describes how much input jitter the receiver can survive. Jitter generation is jitter created internally by the CDR / clocking path.

---

## 5. LDO / Power Questions

## Q8: Why does LDO matter in SerDes?

LDO output noise, finite PSRR, and transient response can disturb PLL, CDR, clock buffers, RX front-end, ADC, references, and bias circuits. These disturbances become jitter, vertical eye closure, or calibration error.

## Q9: How does supply noise become jitter?

Supply noise can modulate VCO frequency or clock buffer delay. VCO modulation creates phase modulation, and buffer delay modulation moves clock edges. Both create timing jitter.

## Q10: How do you explain PSRR across frequency?

Low-frequency PSRR is mainly loop-gain dominated. Mid-frequency PSRR depends on loop bandwidth, poles, zeros, pass device behavior, and output capacitor. High-frequency PSRR is often limited by parasitic feedthrough, decap, package, and layout.

## Q11: Why is LDO stability important for PCIe clocking?

Weak LDO stability can create output ringing or noise peaking. If the LDO powers PLL or clock buffers, that ripple can become jitter and reduce eye margin.

---

## 6. ADC / PAM4 Questions

## Q12: Why use ADC-based receivers?

ADC-based receivers digitize the received waveform and allow flexible DSP equalization, calibration, and PAM4 decisions. They are attractive for high-speed PAM4 but require careful control of ADC power, jitter, resolution, and mismatch.

## Q13: What matters in a time-interleaved ADC?

Offset mismatch, gain mismatch, timing skew, and bandwidth mismatch. Timing skew is especially harmful because sample voltage error is proportional to input slope.

## Q14: How does sampling jitter affect ADC SNDR?

Sampling jitter creates voltage error when the input has slope. A common approximation is `SNR_jitter = -20 log10(2 pi fin sigma_t)`, so higher input frequency and larger RMS jitter reduce SNDR.

---

## 7. SerDes / PCIe 7.0 Relevance

All answers should connect back to link margin:

```text
circuit imperfection
down
timing or amplitude error
down
eye closure
down
BER / link margin degradation
```

That is the practical engineering bridge between analog block design and SerDes system performance.

---

## 8. Synopsys Preparation Relevance

Use this note for:

* pre-onboarding review
* quick interview-style practice
* preparing questions for the team
* connecting prior experience to expected PCIe 7.0 clocking and LDO work

Do not state internal Synopsys architecture unless it has been confirmed from approved internal sources.

---

## 9. Interview Explanation

One useful framing:

```text
My preparation focus is to connect analog block design to PCIe 7.0 SerDes performance. PLL phase noise and CDR behavior determine sampling timing. LDO PSRR, noise, and stability affect jitter and receiver margin. PAM4 receiver design is sensitive to both amplitude and timing errors. So I want to reason from device and block-level mechanisms all the way to eye margin and BER.
```

---

## 10. Common Interview Questions

Common themes to practice:

* Explain PCIe 7.0 at PHY level.
* Explain why PAM4 is harder than NRZ.
* Explain PLL phase noise vs jitter.
* Explain CDR jitter tolerance.
* Explain LDO PSRR.
* Explain LDO stability.
* Explain supply noise to jitter.
* Explain ADC sampling jitter.
* Explain TI-ADC mismatch.
* Tell a technical story about debugging an analog block.

---

## 11. Open Questions

* Which technical questions are most likely for the actual Synopsys team?
* Which internal documents should define the correct architecture vocabulary?
* What are the team's preferred jitter metrics?
* How much detail should be known before onboarding versus learned after joining?
* Which answers need diagrams?
* Which answers should be expanded into standalone notes?

---

## 12. Related Notes

* `technical_story_bank.md`
* `../Study_Plans/synopsys_4_week_prep_plan.md`
* `../SerDes/pcie7_overview.md`
* `../SerDes/serdes_architecture_overview.md`
* `../PLL_CDR_Clocking/pcie7_clocking_notes.md`
* `../PLL_CDR_Clocking/pll_fundamentals.md`
* `../PLL_CDR_Clocking/cdr_fundamentals.md`
* `../LDO_Bandgap/serdes_power_integrity.md`
* `../ADC/adc_based_receiver.md`
* `../../02_Synopsys_Work/onboarding_plan.md`

---

## 13. Next Actions

1. Convert the strongest Q&A into flashcards.
2. Add diagrams for PLL, CDR, LDO, and ADC-based RX.
3. Add short and long versions of each answer.
4. Update after Synopsys onboarding clarifies actual team focus.

---

## Last Updated

2026-07-01

