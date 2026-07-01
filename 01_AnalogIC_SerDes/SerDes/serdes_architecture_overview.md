---

title: "SerDes Architecture Overview"
domain: "AnalogIC_SerDes"
tags:

* SerDes
* Architecture
* PAM4
* PCIe7
* Equalization
* CDR
* PLL
* ADC
* Synopsys
  created: 2026-07-01
  updated: 2026-07-01
  source: "ChatGPT technical notes and Synopsys role preparation"
  status: "active"

---

# SerDes Architecture Overview

## Purpose

This note gives a system-level map of a modern high-speed SerDes PHY.

The goal is to understand where TX, RX, equalization, PLL, CDR, ADC, LDO, and calibration blocks fit before going deeper into individual circuits.

---

## 1. Big Picture

SerDes means serializer / deserializer.

It converts parallel data into high-speed serial data for transmission over a channel, then recovers the data at the receiver.

Simplified chain:

```text
Parallel data
down
Serializer
down
TX equalization / driver
down
Package / channel / connector
down
RX front-end / CTLE
down
Sampler or ADC
down
FFE / DFE / DSP
down
CDR / timing recovery
down
Deserializer
down
Parallel data
```

The architecture is a system of loops: timing recovery, equalization adaptation, calibration, and power regulation all interact.

---

## 2. Key Concepts

Important SerDes concepts:

* unit interval
* channel insertion loss
* return loss
* ISI
* crosstalk
* PAM4 levels
* TX FFE
* RX CTLE
* RX FFE
* DFE
* CDR
* jitter budget
* eye diagram
* bathtub curve
* BER / SER
* link training
* ADC-based receiver
* calibration
* power integrity

The core problem:

```text
Transmit enough information through a lossy channel,
then recover amplitude and timing with acceptable BER.
```

---

## 3. Transmitter Path

The TX path may include:

* data muxing / serialization
* high-speed clocking
* TX FFE taps
* output driver
* impedance control
* common-mode control
* pre-driver stages
* calibration for swing and impedance

TX FFE intentionally shapes the transmitted waveform to compensate for channel loss.

Simple idea:

```text
Pre-distort signal at TX
down
channel loss partially cancels distortion
down
RX sees a more open eye
```

---

## 4. Channel

The channel includes:

* package
* PCB traces
* connectors
* vias
* cables if present
* retimers or redrivers if present

Channel issues:

* high-frequency loss
* reflections
* impedance discontinuities
* crosstalk
* skew
* dispersion

High-frequency loss creates ISI, which is the reason equalization is mandatory.

---

## 5. Receiver Path

The RX path may include:

* termination
* ESD and input protection
* CTLE
* variable gain
* sampler or ADC
* slicers for PAM4 thresholds
* FFE / DFE / DSP
* CDR
* adaptation loops
* offset / gain / threshold calibration

The RX must recover both:

```text
Amplitude information
and
Timing information
```

PAM4 makes amplitude recovery harder. High speed makes timing recovery harder.

---

## 6. Equalization

Equalization fights ISI.

Common blocks:

* TX FFE for pre-emphasis / de-emphasis
* RX CTLE for analog high-frequency boost
* RX FFE for linear post-processing
* DFE for cancelling post-cursor ISI
* DSP adaptation in ADC-based receivers

Important point:

```text
Equalization is not independent from CDR.
The waveform created by equalization is the waveform used for timing recovery.
```

---

## 7. Clocking and CDR

SerDes requires clean clocking for:

* TX serialization
* TX launch timing
* RX sampling
* phase interpolation
* deserialization
* calibration and DSP timing

CDR uses received data transitions to place the sampling clock.

Key clocking risks:

* PLL phase noise
* clock buffer jitter
* supply-induced jitter
* phase interpolator nonlinearity
* CDR lock to poor phase under ISI
* jitter peaking

---

## 8. SerDes / PCIe 7.0 Relevance

PCIe 7.0 is a SerDes PHY challenge because it uses 128 GT/s PAM4 signaling.

The architecture must manage:

* small PAM4 vertical eye
* tight jitter budget
* heavy channel equalization
* robust CDR
* power and area limits
* link training and adaptation
* compliance and margin testing

PCIe 7.0 should be studied as a system-level PHY problem, not only as a protocol standard.

---

## 9. Synopsys Preparation Relevance

For Synopsys preparation, this note is the map that connects detailed notes:

* PLL and jitter notes explain clock quality.
* CDR notes explain timing recovery.
* LDO notes explain supply sensitivity.
* ADC notes explain possible PAM4 RX architecture.
* Equalization notes explain channel compensation.

Unknown internal implementation details should remain open questions until onboarding.

---

## 10. Interview Explanation

Short explanation:

```text
A SerDes PHY serializes parallel data, drives it through a lossy high-speed channel, then recovers the data with an RX front-end, equalization, CDR, and deserializer. The main impairments are channel loss, ISI, noise, jitter, crosstalk, and power supply disturbance. In PCIe 7.0 PAM4, both amplitude and timing margins are tight, so equalization, clocking, CDR, ADC or slicer design, and power integrity all interact.
```

Synopsys-focused explanation:

```text
For Synopsys preparation, I should understand the SerDes architecture well enough to place my likely clocking and LDO work in the full PHY. PLL jitter and LDO supply noise are not isolated block metrics; they affect RX sampling, TX launch timing, eye margin, and BER.
```

---

## 11. Common Interview Questions

## Q1: What are the main blocks of a SerDes PHY?

Serializer, TX equalization and driver, channel, RX front-end, CTLE, sampler or ADC, FFE / DFE / DSP, CDR, deserializer, PLL, references, regulators, and calibration.

## Q2: Why is equalization needed?

The channel attenuates high-frequency content and creates ISI. Equalization compensates for that distortion.

## Q3: Why is CDR needed?

The receiver needs to recover the correct sampling phase from incoming data transitions.

## Q4: Why is PAM4 harder than NRZ?

PAM4 carries 2 bits per symbol but has smaller vertical eye openings, making it more sensitive to noise, nonlinearity, threshold error, and jitter.

## Q5: How does LDO design connect to SerDes?

LDO noise and finite PSRR can disturb PLL, CDR, RX front-end, ADC, and references, reducing eye margin.

---

## 12. Open Questions

* Which SerDes blocks will I directly work on at Synopsys?
* How is the PCIe 7.0 PHY partitioned between analog, mixed-signal, and digital teams?
* Is the receiver slicer-based or ADC-based?
* What equalization architecture is used?
* What CDR architecture is used?
* Which blocks have dedicated LDOs?
* What documents should I read first after joining?

---

## 13. Related Notes

* `pcie7_overview.md`
* `pam4_receiver_basics.md`
* `ctle_ffe_dfe_notes.md`
* `../PLL_CDR_Clocking/pcie7_clocking_notes.md`
* `../PLL_CDR_Clocking/pll_fundamentals.md`
* `../PLL_CDR_Clocking/cdr_fundamentals.md`
* `../ADC/adc_based_receiver.md`
* `../LDO_Bandgap/serdes_power_integrity.md`
* `../Study_Plans/synopsys_4_week_prep_plan.md`

---

## 14. Next Actions

1. Add a cleaner TX / RX block diagram later.
2. Expand the equalization section after studying CTLE / FFE / DFE.
3. Add architecture-specific notes after reading internal Synopsys material.
4. Use this note as the starting point for interview explanations.

---

## Last Updated

2026-07-01

