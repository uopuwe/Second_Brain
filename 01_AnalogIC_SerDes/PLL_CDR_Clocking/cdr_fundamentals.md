---
title: "CDR Fundamentals"
domain: "AnalogIC_SerDes"
tags:
  - CDR
  - Clocking
  - SerDes
  - PLL
  - PhaseNoise
  - Jitter
  - PAM4
  - PCIe7
  - Synopsys
created: 2026-07-01
updated: 2026-07-01
source: "ChatGPT technical notes and Synopsys role preparation"
status: "active"
---

# CDR Fundamentals

## 中文补充翻译

这篇笔记解释 CDR 的基本作用：receiver 不能假设本地 clock 天然对准数据眼图中心，必须从接收到的数据或 equalized waveform 中恢复 sampling phase。CDR 通过 phase detector、loop filter、VCO 或 PI、sampler 形成闭环，让采样点跟随数据相位。

PLL 生成本地频率参考，CDR 则解决接收数据的相位对准问题。CDR 的核心指标包括 jitter transfer、jitter tolerance 和 jitter generation。bandwidth 越宽，越能跟踪低频 wander / SSC / frequency offset，但也可能传递更多 input jitter 和 phase detector noise；bandwidth 越窄，滤波更强，但可能跟不上慢变化。

在 PAM4 和 ADC-based receiver 中，CDR 更复杂，因为 phase detector 看到的是多电平、带 ISI、noise 和 equalizer residue 的波形。equalization 会影响 CDR 判断，CDR phase 又会影响 equalizer adaptation，因此两者必须联合仿真和验证。

## Purpose

This note summarizes CDR fundamentals from the perspective of high-speed SerDes / PCIe 7.0 clocking preparation.

The goal is to understand why CDR is needed, how it recovers timing from incoming data, how it interacts with equalization, and how jitter transfer / jitter tolerance / jitter generation affect SerDes link margin.

This note supports Synopsys preparation, especially for PCIe 7.0 clocking and SerDes receiver understanding.

---

## 1. Big Picture

CDR means clock and data recovery.

In a SerDes receiver, incoming data does not arrive with a separate ideal sampling clock. The receiver must recover the correct sampling phase from the incoming data stream.

The CDR adjusts the sampling clock so that the receiver samples near the best decision point.

Core chain:

```text
Incoming high-speed data
↓
Channel loss / ISI / jitter / noise
↓
Equalizer
↓
Sampler / slicer / ADC
↓
Phase detector
↓
Loop filter / digital loop
↓
VCO / phase interpolator / sampling phase control
↓
Recovered sampling clock
```

Key idea:

```text
CDR turns data transitions into timing information.
```

In high-speed SerDes, CDR quality directly affects sampling margin, eye opening, BER, and link robustness.

---

## 2. Why CDR Is Needed

A high-speed serial receiver needs to know when to sample data.

If the sampling clock is too early or too late, the receiver may sample near transitions instead of the eye center.

Bad sampling phase causes:

* higher bit error rate
* smaller horizontal eye margin
* more sensitivity to jitter
* more sensitivity to ISI
* worse PAM4 symbol decisions
* reduced link margin

Simplified view:

```text
Good CDR:
sampling near eye center
↓
larger margin

Bad CDR:
sampling near transition
↓
more errors
```

At PCIe 7.0 / PAM4 speeds, the UI is very small, so even small timing errors matter.

---

## 3. PLL vs CDR

PLL and CDR are related but not identical.

## PLL

A PLL locks a generated clock to a reference clock.

```text
Reference clock
↓
PLL
↓
Generated clock
```

The phase detector compares clock edge to clock edge.

## CDR

A CDR recovers timing from data transitions.

```text
Incoming data
↓
CDR
↓
Recovered sampling clock
```

The phase detector often compares data transitions with sampling clock phase.

Key difference:

```text
PLL locks to a clock.
CDR locks to data.
```

That one sentence is simple enough that someone will still manage to overcomplicate it in a meeting.

---

## 4. Basic CDR Loop

A CDR loop usually contains:

* phase detector
* loop filter
* clock generation or phase adjustment block
* sampler / slicer / ADC
* feedback path

Simplified loop:

```text
Data input
↓
Sampler / slicer
↓
Phase detector
↓
Loop filter
↓
VCO / PI / sampling phase controller
↓
Sampling clock
↓
Sampler / slicer
```

The CDR observes whether the sampling clock is early or late and adjusts the sampling phase.

---

## 5. Phase Detector

The phase detector extracts timing error information from the received data.

In a CDR, the phase detector may use:

* data samples
* edge samples
* slicer decisions
* transition information
* ADC samples
* equalized data
* error signals from DSP

The phase detector tells the loop whether the sampling clock should move earlier or later.

Important challenge:

```text
Data transitions are not guaranteed every UI.
```

If there are long runs without transitions, the CDR receives less timing information.

This is why transition density and data pattern matter.

---

## 6. Bang-Bang CDR

Bang-bang CDR is also called binary phase detector CDR.

It usually produces only early / late decisions.

Output:

```text
Clock is early
or
Clock is late
```

It does not measure exact phase error magnitude.

Advantages:

* simple
* robust
* common in high-speed links
* works well with slicer-based receivers

Disadvantages:

* nonlinear behavior
* limit cycle jitter
* harder linear analysis
* performance depends on transition density
* can interact with ISI and equalization

Bang-bang CDR is widely used because real circuits enjoy turning elegant linear theory into a street fight.

---

## 7. Linear CDR

A linear CDR produces phase error proportional to timing error over some range.

Advantages:

* easier loop analysis
* predictable small-signal behavior
* useful in some architectures

Disadvantages:

* may need more analog complexity
* may be more sensitive to amplitude noise
* may depend on linear front-end behavior
* can be harder at very high speed

Linear CDR models are useful for understanding jitter transfer and loop bandwidth, even when the actual implementation is nonlinear.

---

## 8. Baud-Rate vs Oversampling CDR

## Baud-Rate CDR

Samples once per UI, or effectively at the baud rate.

Advantages:

* lower power
* simpler high-speed front-end
* common in high-speed SerDes

Disadvantages:

* less timing information
* more dependent on equalization and data decisions
* phase detection can be harder under heavy ISI

## Oversampling CDR

Samples multiple times per UI.

Advantages:

* more timing information
* can directly observe edges
* easier phase detection in some architectures

Disadvantages:

* higher power
* higher sampling speed requirement
* more hardware complexity

At very high speed, power and bandwidth constraints often push designs toward baud-rate approaches.

---

## 9. Phase Interpolator-Based CDR

Many high-speed SerDes receivers use a phase interpolator, or PI, to adjust sampling phase.

Basic idea:

```text
PLL generates multiple clock phases
↓
Phase interpolator blends phases
↓
CDR selects / adjusts sampling phase
```

Advantages:

* avoids needing a full VCO in each lane
* supports fine phase control
* useful for multi-lane SerDes
* can work with a shared PLL

Important PI concerns:

* phase step size
* integral nonlinearity
* differential nonlinearity
* phase noise
* supply sensitivity
* mismatch between phases
* clock distribution skew
* calibration

CDR performance depends not only on the loop algorithm but also on the quality of clock phases and PI linearity.

---

## 10. VCO-Based CDR

Some CDRs use a local oscillator or VCO controlled by the CDR loop.

Advantages:

* can directly generate recovered clock
* classical PLL-like analysis may apply
* useful in some architectures

Disadvantages:

* VCO phase noise matters
* supply sensitivity matters
* per-lane VCO may consume area and power
* tuning range and calibration may be needed

In modern multi-lane SerDes, shared PLL plus per-lane PI-based CDR is common, but the actual Synopsys architecture is 待确认.

---

## 11. CDR Loop Bandwidth

CDR loop bandwidth determines how quickly the recovered clock tracks input data phase variation.

Simplified:

```text
Low-frequency input jitter:
CDR may track it

High-frequency input jitter:
CDR may not track it and it appears as sampling error
```

## Wider CDR Bandwidth

Pros:

* tracks faster phase variation
* can tolerate more low / mid frequency wander
* faster phase acquisition

Cons:

* may pass more input jitter to recovered clock
* may increase jitter generation
* may interact with noise and equalization
* stability can become harder

## Narrower CDR Bandwidth

Pros:

* filters more input jitter
* potentially lower recovered clock jitter

Cons:

* worse tracking of low-frequency phase movement
* slower acquisition
* may fail under large frequency offset or wander

Key question:

```text
What jitter should the CDR track, and what jitter should it reject?
```

That is the whole game. Everything else is the circuit making you pay for the answer.

---

## 12. Jitter Transfer

Jitter transfer describes how input jitter appears at the recovered clock or output data.

Question:

```text
If the incoming data has phase modulation, how much does the CDR follow it?
```

Typical behavior:

```text
Low-frequency jitter:
CDR tracks

High-frequency jitter:
CDR does not fully track
```

Jitter transfer depends on:

* loop bandwidth
* loop order
* phase detector gain
* loop filter
* PI / VCO gain
* data pattern
* transition density
* equalization
* nonlinear effects

Important point:

```text
Jitter transfer is a loop response, not just a clock quality number.
```

---

## 13. Jitter Tolerance

Jitter tolerance describes how much input jitter the receiver can tolerate while maintaining a target BER.

Question:

```text
How much input jitter can the link survive?
```

Jitter tolerance is usually frequency-dependent.

At low jitter frequency:

```text
CDR can track more jitter
↓
higher tolerance
```

At high jitter frequency:

```text
CDR cannot track quickly
↓
jitter appears as sampling phase error
↓
lower tolerance
```

Jitter tolerance is critical for SerDes compliance and robustness.

---

## 14. Jitter Generation

Jitter generation is jitter created by the receiver / CDR itself.

Sources:

* PI noise
* local oscillator noise
* clock buffer noise
* supply noise
* phase detector noise
* quantization noise
* loop filter noise
* digital control limit cycles
* power coupling
* substrate coupling

Even with clean input data, the recovered clock can have jitter created internally.

Important chain:

```text
CDR internal noise
↓
sampling clock jitter
↓
horizontal eye closure
↓
BER degradation
```

---

## 15. ISI and CDR

ISI means inter-symbol interference.

Channel loss spreads one symbol into neighboring symbols. This distorts transitions and shifts apparent edge timing.

ISI can cause:

* data-dependent jitter
* wrong early / late decisions
* phase detector bias
* reduced eye opening
* worse CDR lock point

Important interaction:

```text
Equalization affects the waveform.
The waveform affects phase detector decisions.
Phase detector decisions affect CDR phase.
CDR phase affects sampling.
Sampling affects equalization adaptation.
```

Congratulations, it is a loop inside a loop inside a headache.

---

## 16. CDR and Equalization Interaction

CDR and equalization are tightly coupled.

Equalizers include:

* CTLE
* FFE
* DFE
* DSP equalization

If equalization is poor:

* eye is closed
* transitions are distorted
* CDR phase detector gets bad timing information
* CDR may lock to a poor phase

If CDR phase is poor:

* samples are bad
* DFE decisions are wrong
* adaptation may converge incorrectly
* eye margin worsens

Important question:

```text
Which adapts first: equalization or timing?
```

In real systems, acquisition sequence matters.

Possible startup flow:

```text
coarse clock / frequency lock
↓
basic equalization
↓
CDR phase lock
↓
DFE / FFE adaptation
↓
fine timing adjustment
↓
margin optimization
```

Actual implementation depends on architecture. The universe, tragically, did not standardize this for your convenience.

---

## 17. CDR in PAM4 Systems

PAM4 makes CDR harder than NRZ in several ways.

PAM4 has:

* four amplitude levels
* three eyes
* smaller vertical spacing
* more sensitivity to noise
* more complex transitions
* more threshold decisions
* more equalization dependency

CDR challenges in PAM4:

* transition detection can be more complex
* amplitude noise can affect timing decisions
* slicer threshold errors can corrupt phase detector decisions
* ISI can distort level crossings
* equalization and timing recovery are more coupled

Important idea:

```text
PAM4 reduces vertical margin.
Jitter reduces horizontal margin.
Together they squeeze the eye from both directions.
```

Very considerate of them.

---

## 18. CDR in ADC-Based Receivers

ADC-based receivers digitize the incoming signal and perform more processing digitally.

In ADC-based RX, CDR may use:

* ADC samples
* digital timing error detector
* DSP equalized samples
* interpolated samples
* decision-directed phase error
* Mueller-Muller-type timing detection
* data-aided or blind adaptation methods

Advantages:

* flexible digital timing recovery
* can use DSP to improve phase detection
* can combine with FFE / DFE adaptation
* supports advanced calibration

Challenges:

* ADC sampling jitter matters
* ADC power matters
* time-interleaving mismatch matters
* DSP latency matters
* timing recovery and equalization strongly interact
* digital loop design becomes complex

Important question:

```text
Does timing recovery happen before or after main equalization?
```

Architecture matters a lot.

---

## 19. CDR Acquisition vs Tracking

CDR has two important modes:

## Acquisition

The CDR finds the correct phase from an initially unknown state.

Challenges:

* large phase error
* frequency offset
* poor equalization at startup
* low transition density
* noisy input
* pattern dependency

## Tracking

The CDR follows phase changes after lock.

Challenges:

* input jitter
* supply noise
* temperature drift
* channel variation
* crosstalk
* data-dependent jitter

A CDR that tracks well may still acquire poorly. Another delightful circuit ambush.

---

## 20. Frequency Offset

The incoming data rate may not perfectly match the local clock frequency.

CDR must handle frequency offset between transmitter and receiver.

If frequency offset exists:

```text
phase error accumulates over time
↓
CDR must continuously adjust sampling phase
```

If CDR bandwidth or phase adjustment range is insufficient, the recovered clock may slip or lose lock.

Important questions:

* What ppm offset must be tolerated?
* Is there SSC, spread-spectrum clocking?
* How does CDR handle frequency drift?
* Is the loop phase range sufficient?
* How are slips avoided?

---

## 21. CDR and Spread-Spectrum Clocking

PCIe systems may involve spread-spectrum clocking.

Spread-spectrum clocking modulates clock frequency to reduce EMI.

For CDR, this means the incoming data phase may have low-frequency modulation.

The CDR must track this modulation without creating errors.

Important question:

```text
Is the CDR bandwidth sufficient to track allowed low-frequency clock modulation?
```

But if bandwidth is too wide, it may also pass unwanted jitter.

Again, a tradeoff. Analog and mixed-signal design: the art of being trapped between two bad choices and making it look intentional.

---

## 22. Supply Noise and CDR

CDR is sensitive to supply noise through:

* PI delay modulation
* clock buffer delay modulation
* VCO / PLL phase noise
* slicer offset
* sampler aperture variation
* digital loop noise
* reference / bias noise

Supply noise can create:

* sampling jitter
* phase detector error
* wrong slicer decisions
* jitter generation
* spurs
* lock instability

Important chain:

```text
Supply noise
↓
clock phase / sampler / slicer disturbance
↓
CDR phase error
↓
sampling jitter or wrong tracking
↓
eye closure
```

Related notes:

```text
../LDO_Bandgap/serdes_power_integrity.md
../LDO_Bandgap/ldo_psrr_notes.md
```

---

## 23. CDR Metrics

Important CDR-related metrics:

* jitter transfer
* jitter tolerance
* jitter generation
* lock time
* acquisition range
* tracking range
* phase margin
* loop bandwidth
* phase step size
* recovered clock jitter
* BER under jitter injection
* eye margin
* bathtub curve
* pattern sensitivity
* supply sensitivity
* PVT robustness

A CDR is not “good” because it locks once in a pretty simulation. That is the engineering equivalent of passing one multiple-choice question and declaring intellectual victory.

---

## 24. Important Simulations

Useful CDR simulations include:

## Basic Function

* phase acquisition
* lock behavior
* frequency offset tracking
* phase step response
* pattern dependency
* transition density stress

## Jitter

* jitter transfer
* jitter tolerance
* jitter generation
* sinusoidal jitter injection
* random jitter injection
* periodic jitter injection
* data-dependent jitter

## Equalization Interaction

* CDR with CTLE only
* CDR with FFE / DFE
* CDR during adaptation
* CDR under channel loss
* CDR under crosstalk

## Supply / Noise

* PI supply noise sensitivity
* PLL supply-induced jitter
* clock buffer supply sensitivity
* slicer threshold disturbance
* reference / bias noise sensitivity

## Corners

* PVT
* channel corners
* package corners
* voltage corners
* temperature corners
* process mismatch
* post-layout extraction if relevant

---

## 25. Debug Checklist

If a SerDes RX has margin or lock problems, ask:

* Does CDR lock?
* How long does it take to lock?
* Does it lock to the correct phase?
* Does lock depend on data pattern?
* Does lock depend on equalization setting?
* Does jitter tolerance fail at specific frequencies?
* Does BER improve if sampling phase is manually shifted?
* Does supply noise correlate with recovered clock jitter?
* Does enabling DFE improve or worsen CDR stability?
* Does channel loss create data-dependent jitter?
* Does CDR fail under SSC or frequency offset?
* Is phase detector biased by ISI?
* Are PI steps monotonic?
* Does PVT affect loop bandwidth?

Possible debug flow:

```text
Observe BER / eye issue
↓
Sweep sampling phase manually
↓
Check eye center and margin
↓
Check CDR lock point
↓
Inject jitter and measure tolerance
↓
Check equalization settings
↓
Check supply noise and recovered clock jitter
↓
Check phase detector decisions
↓
Adjust loop bandwidth / adaptation sequence / equalization
```

---

## 26. Interview Explanation

Short explanation:

```text
A CDR recovers the sampling clock phase from incoming serial data. It uses data transitions to determine whether the sampling clock is early or late, filters that phase error, and adjusts the sampling phase through a VCO, phase interpolator, or clock control block. The key CDR metrics are jitter transfer, jitter tolerance, jitter generation, acquisition range, tracking range, and BER impact.
```

SerDes-focused explanation:

```text
In high-speed SerDes, the CDR is critical because the receiver must sample data near the eye center despite channel loss, ISI, jitter, noise, and frequency offset. The CDR interacts strongly with CTLE, FFE, DFE, and ADC / slicer decisions. If equalization is poor, phase detection can be biased. If timing is poor, equalization and decisions become worse. So CDR should be understood as part of the full RX adaptation loop, not as an isolated block.
```

Synopsys-focused explanation:

```text
For PCIe 7.0 preparation, I would focus on how CDR bandwidth, jitter tolerance, jitter transfer, and supply-induced jitter affect link margin. Since PAM4 has smaller vertical eye openings, timing recovery must work with less margin and stronger equalization dependency. I would also pay attention to how PLL noise, phase interpolator nonlinearity, LDO supply noise, and RX equalization interact with CDR performance.
```

Senior-level explanation:

```text
The key is to connect CDR loop behavior to system-level link robustness. The CDR does not just lock a clock. It determines where the receiver samples the data under jitter, ISI, noise, channel loss, supply disturbance, and adaptation transients. A robust CDR must have appropriate loop bandwidth, jitter tolerance, acquisition behavior, low jitter generation, stable interaction with equalization, and good PVT / supply-noise resilience.
```

---

## 27. Common Interview Questions

## Q1: What is CDR?

CDR means clock and data recovery. It recovers the sampling clock phase from incoming serial data so the receiver can sample data correctly.

## Q2: Why is CDR needed in SerDes?

Because high-speed serial data arrives without a separate ideal sampling clock. The receiver must recover timing from data transitions.

## Q3: What is the difference between PLL and CDR?

A PLL locks to a reference clock. A CDR locks sampling phase to incoming data transitions.

## Q4: What is bang-bang CDR?

A bang-bang CDR uses binary early / late phase decisions rather than proportional phase error.

## Q5: What is jitter transfer?

Jitter transfer describes how much input data jitter is transferred to the recovered clock or output.

## Q6: What is jitter tolerance?

Jitter tolerance describes how much input jitter the receiver can tolerate while maintaining target BER.

## Q7: What is jitter generation?

Jitter generation is jitter created internally by the CDR / receiver clocking system.

## Q8: How does CDR bandwidth affect performance?

Wider bandwidth tracks faster input phase variation but may pass more jitter and noise. Narrower bandwidth filters more jitter but tracks slower and may reduce tolerance to low-frequency wander.

## Q9: How does ISI affect CDR?

ISI distorts transitions and can bias phase detector decisions, causing the CDR to lock to a poor sampling phase.

## Q10: How does equalization interact with CDR?

Equalization shapes the waveform used for phase detection. Poor equalization can hurt timing recovery, while poor CDR timing can hurt equalization and data decisions.

## Q11: Why is PAM4 harder for CDR than NRZ?

PAM4 has smaller vertical eye openings and more complex transitions, so noise and threshold errors can more easily corrupt phase detection and sampling.

## Q12: How does supply noise affect CDR?

Supply noise can modulate PI delay, clock buffer delay, sampler aperture, slicer threshold, or PLL phase, creating jitter and phase detection errors.

---

## 28. Personal Connection to My Experience

This note connects to my PLL, ADC, LDO, and SerDes preparation.

Relevant background:

* PLL / ADPLL / DCO work
* phase noise and jitter analysis
* ADC sampling and timing sensitivity
* LDO supply noise and PSRR
* analog IP integration
* high-speed mixed-signal design
* clocking-related interview preparation

How to present this experience:

```text
My previous PLL, ADC, and LDO experience connects naturally to CDR and SerDes clocking. PLL knowledge helps me understand recovered clock generation and jitter shaping. ADC experience helps me understand sampling phase and timing error. LDO experience helps me understand supply-induced jitter and clock path disturbance. For PCIe 7.0 SerDes, these pieces come together in CDR performance, jitter tolerance, and receiver margin.
```

---

## 29. Open Questions

* 待确认: What CDR architecture is used in Synopsys PCIe 7.0 IP?
* 待确认: Is the CDR baud-rate or oversampling?
* 待确认: Is it bang-bang, linear, or DSP-based?
* 待确认: Does it use a phase interpolator or local VCO?
* 待确认: What is the target CDR loop bandwidth?
* 待确认: How is jitter tolerance verified?
* 待确认: How is jitter transfer specified?
* 待确认: How does CDR interact with CTLE / DFE / FFE?
* 待确认: How does the architecture handle PAM4 timing recovery?
* 待确认: How does supply-induced jitter enter the CDR path?
* 待确认: What acquisition sequence is used during link training?
* 待确认: What are the most common CDR-related debug issues?

---

## Source Conversations / Source Packets

* `../../00_Inbox/manual_batches/batch2_serdes_pcie_pll_cdr_adc_2026-07-01/source_packet.md`

---

## 30. Related Notes

* `pll_fundamentals.md`
* `pll_phase_noise_jitter.md`
* `pcie7_clocking_notes.md`
* `../SerDes/pcie7_overview.md`
* `../SerDes/serdes_architecture_overview.md`
* `../SerDes/pam4_receiver_basics.md`
* `../SerDes/ctle_ffe_dfe_notes.md`
* `../LDO_Bandgap/serdes_power_integrity.md`
* `../LDO_Bandgap/ldo_psrr_notes.md`
* `../ADC/adc_based_receiver.md`
* `../ADC/sampling_jitter_adc.md`
* `../Interview_QA/synopsys_relevant_qa.md`
* `../Study_Plans/synopsys_4_week_prep_plan.md`
* `../../02_Synopsys_Work/synopsys_master_note.md`
* `../../02_Synopsys_Work/onboarding_plan.md`

---

## 31. Next Actions

1. Create `pcie7_clocking_notes.md`.
2. Create `../ADC/adc_based_receiver.md`.
3. Add CDR block diagrams later.
4. Add jitter transfer / tolerance curve examples later.
5. Add architecture-specific Synopsys notes after joining.
6. Link this note to future SerDes interview Q&A.

---

## 32. Batch 1 Extracted Knowledge - 2026-07-02

### 32.1 CDR Bandwidth Rule

CDR bandwidth should be high enough to track low-frequency phase wander, frequency offset, and SSC-related movement, but low enough to reject high-frequency jitter, ISI-driven data-dependent jitter, phase-detector noise, and quantization noise.

Useful first-order loop relationship:

```text
H_CDR(s) ~= L(s) / (1 + L(s))
```

Below the CDR bandwidth, input phase tends to be tracked. Above the bandwidth, the CDR increasingly rejects input phase movement and the sampler sees residual high-frequency jitter.

Practical ranges from the conversation, not standards:

- 10/25G links: often a few MHz.
- 56G PAM4: often a few MHz to about 10 MHz.
- 112G PAM4: often about 5 to 20 MHz.
- 224G PAM4: several MHz to tens of MHz, strongly architecture-dependent.

待确认: Actual Synopsys CDR loop bandwidth targets, jitter-transfer masks, and measurement methods must be checked against internal design documents.

### 32.2 112G PAM4 Timing Example

For 112 Gb/s PAM4:

```text
symbol rate = 56 Gbaud
UI = 1 / 56e9 = 17.86 ps
CDR bandwidth = 10 MHz
normalized bandwidth = 10e6 / 56e9 = 1.8e-4
```

Design implication: even a 10 MHz CDR is extremely slow relative to symbol rate. It tracks low-frequency phase movement over many symbols, not individual symbol-to-symbol data transitions.

### 32.3 Interaction With ADC-Based RX

In an ADC-based receiver, CDR behavior moves into a mixed analog/digital boundary:

- ADC aperture jitter and sampling-clock phase noise create voltage noise before DSP can help.
- Digital timing recovery can track low-frequency timing movement but cannot undo random aperture jitter.
- FFE/DFE adaptation, timing recovery, gain/offset adaptation, and TI-ADC skew calibration should run on separated time scales.
- Rule of thumb:

```text
adaptation bandwidth << CDR bandwidth << symbol rate
```

### 32.4 Jitter Generation Sources

CDR jitter generation can come from:

- phase-detector noise and quantization
- bang-bang phase detector limit cycles
- DCO/VCO phase noise
- PI quantization and INL
- supply noise on clock buffers and samplers
- digital loop truncation or coefficient quantization
- ADC noise causing timing-detector error

### 32.5 Source Conversation

- `../../00_Inbox/raw_chat_exports/chatgpt_export_2026-07-01/md_by_conversation/2026-05-13__SerDes_PLL_CDR_带宽.md`

---

## Last Updated

2026-07-02
