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
updated: 2026-07-05
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

## 33. Deep Ingest 2026-07-05 - Rhee and Yu CDR PLL Metrics and Architectures

Source update:

- Woogeun Rhee and Zhiping Yu, *Phase-Locked Loops: System Perspectives and Circuit Design Aspects*, Wiley/IEEE Press, 2024.
- Archived source packet: [Rhee and Yu PLL book 2026-07-05](<../../90_Archive/processed/2026/books/phase_locked_loops_rhee_yu_2024/>)
- Related promoted notes: [[pll_fundamentals]], [[pll_phase_noise_jitter]], [[pfd_charge_pump_notes]], [[pll_fractional_n_digital]].

### 33.1 CDR Is a PLL with Data-Dependent Phase Information

中文：Rhee 和 Yu 把 CDR PLL 的核心 tradeoff 归纳为三类指标：jitter generation、jitter transfer 和 jitter tolerance。对 SerDes 来说，这比只讨论“CDR bandwidth 几 MHz”更准确，因为同一个 bandwidth 可以改善 VCO noise、恶化 input jitter tracking、改变 pattern-dependent jitter、影响 acquisition，并且改变 receiver 对 SSC、frequency offset 和 channel-induced jitter 的容忍度。

English: Rhee and Yu frame a CDR PLL around three metrics: jitter generation, jitter transfer, and jitter tolerance. For SerDes, this is more precise than asking only “what is the CDR bandwidth,” because the same bandwidth can improve VCO noise, worsen input-jitter tracking, change pattern-dependent jitter, affect acquisition, and change receiver tolerance to SSC, frequency offset, and channel-induced jitter.

中文：CDR 与 clock-generation PLL 的关键差异是 phase information 来自数据 transition，而不是干净 periodic reference。NRZ/PAM4 transition density、ISI、equalizer residual、sampler noise、decision error 和 long CID 都会改变 phase-detector output。因此 CDR loop 必须和 data pattern、equalization、slicer/ADC front-end 一起建模。

English: The key difference between a CDR and a clock-generation PLL is that phase information comes from data transitions rather than a clean periodic reference. NRZ/PAM4 transition density, ISI, equalizer residue, sampler noise, decision error, and long CIDs all change the phase-detector output. Therefore a CDR loop must be modeled together with data pattern, equalization, and the slicer/ADC front end.

### 33.2 Jitter Generation

中文：jitter generation 是 CDR 自己产生的 output jitter，包括 VCO/DCO noise、phase detector noise、bang-bang limit cycle、PI quantization、digital loop truncation、supply noise、clock buffer noise 和 pattern-dependent jitter。与 clock multiplier PLL 不同，CDR 通常没有 feedback divider，因此 divider noise 不是主要项；但 data-dependent detector behavior 会成为独特噪声源。

English: Jitter generation is output jitter produced by the CDR itself, including VCO/DCO noise, phase-detector noise, bang-bang limit cycle, PI quantization, digital-loop truncation, supply noise, clock-buffer noise, and pattern-dependent jitter. Unlike a clock-multiplying PLL, a CDR often has no feedback divider, so divider noise is not a main term; however, data-dependent detector behavior becomes a unique noise source.

中文：宽 CDR bandwidth 可以压低 VCO/DCO close-in noise，但也会让 phase-detector noise、data-dependent jitter 和 quantization error 更容易进入 recovered clock。窄 bandwidth 可以滤掉高频 input/data-dependent components，但可能留下更多 local oscillator noise 并降低 tracking ability。

English: Wider CDR bandwidth can suppress VCO/DCO close-in noise, but it also passes phase-detector noise, data-dependent jitter, and quantization error more easily into the recovered clock. Narrower bandwidth can filter high-frequency input/data-dependent components, but it can leave more local oscillator noise and reduce tracking ability.

### 33.3 Jitter Transfer

中文：Type-II CP CDR 的 jitter transfer 可以写成类似 second-order PLL 的形式：

English: The jitter transfer of a Type-II CP CDR can be written in a form similar to a second-order PLL:

$$
H_{JTRAN}(s)=
\frac{\omega_n^2(1+s/\omega_z)}
{s^2+2\zeta\omega_ns+\omega_n^2}
$$

中文：在 overdamped approximation 下，jitter-transfer 3 dB bandwidth 通常接近 unity-gain frequency：

English: Under an overdamped approximation, the jitter-transfer 3 dB bandwidth is often close to unity-gain frequency:

$$
\omega_{3dB}\approx\omega_u
$$

中文：jitter peaking 可以用 damping factor 估计：

English: Jitter peaking can be estimated from damping factor:

$$
JP\approx
20\log_{10}
\left(
1+\frac{1}{4\zeta^2}
\right)
$$

中文：当 damping 较大时，可以近似为：

English: For larger damping, this can be approximated as:

$$
JP\approx\frac{8.686}{4\zeta^2}
$$

中文：这给 review 一个明确问题：CDR bandwidth 不只是 tracking speed，也决定 input jitter 在某些频段是否被 peaking 放大。对 PCIe/PAM4，必须确认 jitter-transfer peaking 和 compliance mask / receiver timing margin 的关系，而不能沿用 SONET 或其它 legacy system 的固定数值。

English: This gives review a concrete question: CDR bandwidth is not only tracking speed; it also determines whether input jitter is amplified by peaking in some frequency band. For PCIe/PAM4, jitter-transfer peaking must be checked against the applicable compliance mask and receiver timing margin, not inherited from SONET or another legacy system.

### 33.4 Jitter Tracking and Jitter Tolerance

中文：CDR residual phase error 与 jitter transfer 互补：

English: CDR residual phase error is complementary to jitter transfer:

$$
H_{JTRACK}(s)=1-H_{JTRAN}(s)
$$

中文：如果 NRZ decision 需要 residual phase error 小于 $0.5\,\mathrm{UI}$，则 jitter tolerance 可以用 residual-error transfer 的倒数近似：

English: If an NRZ decision requires residual phase error below $0.5\,\mathrm{UI}$, jitter tolerance can be approximated from the inverse of the residual-error transfer:

$$
H_{JTOL}(s)=\frac{0.5}{H_{JTRACK}(s)}
$$

中文：对 second-order CDR，可写成：

English: For a second-order CDR, this can be written as:

$$
H_{JTOL}(s)=
\frac{s^2+2\zeta\omega_ns+\omega_n^2}{2s^2}
$$

中文：这个公式给出 intuition：低频 jitter 更容易被 CDR tracking，因此 tolerance 高；高频 jitter 无法被 loop 追踪，因此 residual error 直接打到 sampling point。对 PAM4，实际 tolerance 还会受 vertical noise margin、equalizer residual、decision threshold、ADC aperture 和 FEC/BER target 影响。

English: This equation gives intuition: low-frequency jitter is easier for the CDR to track, so tolerance is high; high-frequency jitter cannot be tracked by the loop and appears directly at the sampling point. For PAM4, actual tolerance also depends on vertical noise margin, equalizer residue, decision thresholds, ADC aperture, and FEC/BER target.

### 33.5 Hogge and Alexander Detector Tradeoffs

中文：linear NRZ phase detectors 通过 data transition 生成 timing information，但 long CID 和 transition-density variation 会降低有效 gain 并产生 pattern-dependent jitter。Hogge detector 是经典 linear CDR PD，它同时做 retiming 和 phase detection，在没有 transition 时保持 neutral；但它的 gain 依赖 transition density，并且 DFF delay mismatch 会引入 offset 与 pattern dependency。

English: Linear NRZ phase detectors generate timing information from data transitions, but long CIDs and transition-density variation reduce effective gain and create pattern-dependent jitter. The Hogge detector is a classic linear CDR PD that performs retiming and phase detection and stays neutral when no transition is present; however, its gain depends on transition density, and DFF delay mismatch introduces offset and pattern dependency.

中文：Alexander detector 是 2x oversampling bang-bang detector。它只输出 early/late decision，不输出线性 phase error magnitude。优点是结构简单、适合数字实现，并且 no-transition 时可以 neutral；缺点是 loop gain 依赖 input jitter statistics，容易出现 limit cycle，并且 loop latency 会放大 jitter peaking 与 limit-cycle jitter。

English: The Alexander detector is a 2x oversampling bang-bang detector. It outputs only an early/late decision, not a linear phase-error magnitude. Its strengths are simple structure, digital compatibility, and neutral behavior on no-transition events; its risks are loop gain dependence on input-jitter statistics, limit cycles, and latency-induced jitter peaking or limit-cycle jitter.

中文：bang-bang detector 的统计线性 gain 常随 input jitter 的 RMS 值变化：

English: The statistically linearized gain of a bang-bang detector often varies with input RMS jitter:

$$
K_{BBPD}\approx\frac{V_{DD}}{\sigma_t\sqrt{2\pi}}
$$

中文：因此 BB-CDR 的 “loop bandwidth” 不是固定常数；它会随 channel condition、equalizer state、noise、transition density 和 slicer error statistics 改变。这一点在 ADC-based or DSP-assisted PAM4 RX 中尤其重要。

English: Therefore the “loop bandwidth” of a BB-CDR is not a fixed constant; it changes with channel condition, equalizer state, noise, transition density, and slicer-error statistics. This is especially important in ADC-based or DSP-assisted PAM4 receivers.

### 33.6 Frequency Acquisition and Dynamic Bandwidth

中文：CDR 常需要 frequency detector、reference-aided acquisition loop 或 wide-band acquisition mode。关键规则是：辅助 acquisition path 必须在正常 data-tracking mode 中退出 critical jitter path，否则它会成为额外 noise/spur source。

English: A CDR often needs a frequency detector, reference-aided acquisition loop, or wide-band acquisition mode. The key rule is that the auxiliary acquisition path must leave the critical jitter path during normal data-tracking mode; otherwise it becomes an extra noise/spur source.

中文：dynamic bandwidth 可以加快 acquisition，但 wide-to-normal bandwidth transition 不能太突兀，否则会引入 overshoot、cycle slip 或 extra settling。SerDes bring-up 中常见的问题不是最终 lock 不住，而是 mode transition、coefficient handoff 或 PI/DCO code handoff 造成隐藏 timing hit。

English: Dynamic bandwidth can speed acquisition, but the transition from wide to normal bandwidth cannot be too abrupt; otherwise it can introduce overshoot, cycle slip, or extra settling. In SerDes bring-up, the common issue is often not final lock failure but hidden timing hits from mode transition, coefficient handoff, or PI/DCO-code handoff.

### 33.7 DLL-Assisted CDR

中文：DLL-assisted CDR 或 D/PLL 结构可以把 jitter transfer 和 jitter tracking 的 corner 分开。一个重要 intuition 是：通过 DLL/VCDL path 处理 tracking，可以在不引入传统 second-order peaking 的情况下获得较宽 tracking bandwidth。

English: A DLL-assisted CDR or D/PLL architecture can separate the jitter-transfer and jitter-tracking corners. One important intuition is that using a DLL/VCDL path for tracking can provide wide tracking bandwidth without the conventional second-order peaking.

中文：D/PLL 的 jitter transfer 可近似写成：

English: The D/PLL jitter transfer can be approximated as:

$$
H_{JTRAN}(s)=
\frac{1}
{s^2C/(K_dK_v)+sK_{vd}/K_v+1}
$$

中文：在 overdamped condition 下，两个 pole 可近似为：

English: Under an overdamped condition, the two poles can be approximated as:

$$
\omega_{PL}\approx\frac{K_v}{K_{vd}}
$$

$$
\omega_{PH}\approx\frac{K_{vd}K_d}{C}
$$

中文：工程意义是可以把 narrow JTRAN 与 wide JTOL 分开调节。代价是 VCDL power/range、ISI if data path is delayed、PVT sensitivity、delay-line nonlinearity 和 calibration complexity。

English: The engineering meaning is that narrow JTRAN and wide JTOL can be tuned separately. The cost is VCDL power/range, ISI if the data path is delayed, PVT sensitivity, delay-line nonlinearity, and calibration complexity.

### 33.8 Burst-Mode and Frequency-Offset Tracking

中文：burst-mode CDR 中，frequency offset 会在 burst 间快速累积 phase error。若 phase margin 为 $\phi_m$ UI，bit rate 为 $R_b$，frequency offset 为 $\Delta f$，可容忍 consecutive identical digits 或 burst gap 的量级可估算为：

English: In a burst-mode CDR, frequency offset rapidly accumulates phase error between bursts. If phase margin is $\phi_m$ UI, bit rate is $R_b$, and frequency offset is $\Delta f$, the tolerable consecutive-identical-digit length or burst gap scale can be estimated as:

$$
N_{CID}=\frac{\phi_mR_b}{\Delta f}
$$

中文：这个公式在 PCIe continuous link 中不一定直接作为 specification 使用，但它提醒我们：transition density、frequency offset 和 phase margin 是绑定的。任何 CDR 架构都必须说明 long-CID、SSC、frequency offset 和 retimer/repeater scenarios 下的 tracking strategy。

English: This equation is not necessarily a direct PCIe continuous-link specification, but it reminds us that transition density, frequency offset, and phase margin are tied together. Any CDR architecture must explain its tracking strategy under long-CID, SSC, frequency offset, and retimer/repeater scenarios.

### 33.9 Review Questions Added

| Review item | Deep-ingest question |
|---|---|
| JGEN | Which blocks dominate generated jitter: VCO/DCO, detector, PI, digital loop, supply, or pattern dependency? |
| JTRAN | Is jitter peaking quantified, and is it checked against the relevant system mask? |
| JTOL | Is residual phase error evaluated over frequency, not only as a single bandwidth number? |
| Detector | Is the PD linear, bang-bang, Hogge, Alexander, ADC/DSP-based, or hybrid? |
| BB loop | Is loop gain tied to input jitter statistics and transition density? |
| Acquisition | Does the acquisition path exit the normal jitter path after lock? |
| DLL-assisted CDR | Are VCDL range, power, ISI, and PVT calibration included? |

### 33.10 Source Provenance Added

| Source | Type | Status | Reusable knowledge promoted |
|---|---|---|---|
| Woogeun Rhee and Zhiping Yu, *Phase-Locked Loops: System Perspectives and Circuit Design Aspects*, Wiley/IEEE Press, 2024 | Book PDF | Deep Ingest 2026-07-05; archived in `90_Archive/processed/2026/books/phase_locked_loops_rhee_yu_2024/` | CDR JGEN/JTRAN/JTOL metric framing, Type-II CDR jitter-transfer equations, jitter peaking estimate, jitter tolerance transfer, Hogge and Alexander detector tradeoffs, BBPD gain dependence, acquisition-path caution, DLL-assisted CDR intuition |

---

## 34. Balanced Ingest 2026-07-05 - Da Dalt BBPLL Lessons for CDR

Source update:

- Nicola Da Dalt, *Theory and Implementation of Digital Bang-Bang Frequency Synthesizers for High Speed Serial Data Communications*, Ph.D. dissertation, RWTH Aachen, 2007.
- Archived source packet: `90_Archive/processed/2026/articles/digital_bang_bang_frequency_synthesizers_da_dalt_2007/`.
- Canonical detailed destination: [[pll_fractional_n_digital]].

### 34.1 Why This Source Affects CDR

中文：Da Dalt 的 dissertation 不是传统 data CDR paper，而是面向高速串行通信 clock generation 的 digital bang-bang frequency synthesizer。它仍然应该影响 CDR note，因为 BBPD CDR 和 BBPLL frequency synthesizer 共享同一个核心问题：binary phase detector 不提供误差幅度，loop 在低噪声下容易形成 limit cycle，而 loop latency 会直接增加 deterministic timing jitter。

English: Da Dalt's dissertation is not a conventional data-CDR paper; it is a digital bang-bang frequency-synthesizer study for high-speed serial communication clock generation. It should still affect the CDR note because BBPD CDRs and BBPLL frequency synthesizers share the same core issue: a binary phase detector does not provide error magnitude, the loop can form limit cycles under low-noise conditions, and loop latency directly increases deterministic timing jitter.

中文：对 CDR review 来说，最可复用的结论是：不能只给一个“linearized CDR bandwidth”。如果 receiver input jitter、loop-generated jitter、transition density 和 slicer noise 使 BBPD 进入 high-noise statistical regime，线性模型比较有用；如果系统处于 low-noise deterministic regime，limit-cycle/orbit model 更能解释 jitter tones、peaking 和 residual timing error。

English: For CDR review, the reusable conclusion is that a single “linearized CDR bandwidth” is not enough. If receiver input jitter, loop-generated jitter, transition density, and slicer noise put the BBPD into a high-noise statistical regime, a linear model is useful; if the system is in a low-noise deterministic regime, a limit-cycle/orbit model better explains jitter tones, peaking, and residual timing error.

### 34.2 Latency Rule for BB-CDR

中文：Da Dalt 的 first-order BBPLL analysis shows that normalized peak-to-peak timing jitter grows with loop delay. In one simplified low-noise case:

English: Da Dalt's first-order BBPLL analysis shows that normalized peak-to-peak timing jitter grows with loop delay. In one simplified low-noise case:

$$
\tau_{pp}=1+2D
$$

中文：在 nonzero frequency-offset approximation 中：

English: In a nonzero frequency-offset approximation:

$$
\tau_{pp}=2(1+D)
$$

中文：这里的 $D$ 是 normalized loop latency。对 CDR，这个式子不应直接当作 PCIe/PAM4 jitter budget，但它是非常强的 design warning：sampler decision latency、retiming latency、digital loop-filter delay、PI update latency、DCO code latency 和 clock feedback path 都会增加 bang-bang loop 的 deterministic jitter risk。

English: Here $D$ is normalized loop latency. For a CDR, this equation should not be used directly as a PCIe/PAM4 jitter budget, but it is a strong design warning: sampler decision latency, retiming latency, digital loop-filter delay, PI update latency, DCO-code latency, and clock-feedback path all increase deterministic jitter risk in a bang-bang loop.

### 34.3 CDR Review Additions

| Review item | Added question |
|---|---|
| BBPD regime | Is the loop operating in low-noise limit-cycle regime or high-noise linearized regime? |
| Loop latency | How many UI/reference cycles exist from phase decision to phase actuator update? |
| Jitter tones | Are observed spurs/tones consistent with BBPD limit-cycle period? |
| Gain estimate | Is BBPD gain estimated from untracked jitter including loop-generated jitter? |
| SSC tracking | Does the loop meet modulation tracking without excessive peaking or limit-cycle growth? |

### 34.4 Source Provenance Added

| Source | Type | Status | Reusable knowledge promoted |
|---|---|---|---|
| Nicola Da Dalt, *Theory and Implementation of Digital Bang-Bang Frequency Synthesizers for High Speed Serial Data Communications*, Ph.D. dissertation, RWTH Aachen, 2007 | Dissertation PDF | Balanced Ingest 2026-07-05; archived in `90_Archive/processed/2026/articles/digital_bang_bang_frequency_synthesizers_da_dalt_2007/` | BBPLL/BB-CDR nonlinear limit-cycle framing, loop-latency jitter warning, low-noise nonlinear versus high-noise linearized model selection, BBPD gain dependence on untracked jitter |

---

## 35. Balanced Ingest 2026-07-05 - Bang-Bang CDR Design Equations

Source update:

- "Designing Bang-Bang PLLs for Clock and Data Recovery in Serial Data Transmission."
- Nicola Da Dalt, "A Design-Oriented Study of the Nonlinear Dynamics of Digital Bang-Bang PLLs," IEEE TCAS-I, 2005.
- Ingest level: Balanced Ingest. Equations below are promoted as design-intuition models, not as PCIe compliance formulas.

### 35.1 Why Flip-Flop Bang-Bang Detectors Matter

中文：bang-bang CDR 常用 flip-flop/sampler 结构同时完成 retiming 和 phase detection。它的优势不是“线性精确”，而是 sampling phase 可以天然与数据 decision point 对齐，PVT tracking 较好，并且 detector 的最窄脉冲通常由 flip-flop 输出决定，适合非常高速的 serial data path。对多相采样 CDR，这种结构也容易扩展为 edge/data sample 比较。

English: A bang-bang CDR often uses flip-flop/sampler structures for both retiming and phase detection. Its strength is not linear precision; it is that the sampling phase can naturally align with the data decision point, PVT tracking is good, and the detector's narrowest pulse is usually set by flip-flop output behavior, making it suitable for very high-speed serial data paths. For multiphase CDRs, the structure also extends naturally to edge/data sample comparison.

中文：代价是 detector 只输出 early/late sign，不输出 phase-error magnitude。因此 loop gain、jitter generation、jitter tolerance 和 acquisition behavior 都依赖输入 jitter statistics、transition density、frequency offset、latency 和 actuator step size。面试或 design review 中说“这是一个 bang-bang CDR”还不够，必须继续问它处于 low-noise limit-cycle regime 还是 high-noise statistical linearized regime。

English: The cost is that the detector outputs only the early/late sign, not phase-error magnitude. Therefore loop gain, jitter generation, jitter tolerance, and acquisition behavior depend on input-jitter statistics, transition density, frequency offset, latency, and actuator step size. In an interview or design review, saying "this is a bang-bang CDR" is not enough; the next question is whether it operates in a low-noise limit-cycle regime or a high-noise statistically linearized regime.

### 35.2 First-Order Bang-Bang Loop Model

中文：一个简化 first-order bang-bang CDR/PLL 可以写成 data phase 与 oscillator phase 的离散更新关系：

English: A simplified first-order bang-bang CDR/PLL can be written as discrete updates of data phase and oscillator phase:

$$
\theta_d(t_n)=\theta_d(0)+2\pi\delta f\,t_n+\phi(t_n)
$$

$$
\theta_v(t_{n+1})=\theta_v(t_n)+\epsilon_n\theta_{bb}
$$

$$
\epsilon_n=\operatorname{sgn}\left[\theta_d(t_n)-\theta_v(t_n)\right]
$$

$$
\theta_{bb}=2\pi\frac{f_{bb}}{f_{nom}}
$$

中文：这里 $\delta f$ 是 input/oscillator 频率误差，$\phi(t)$ 是输入相位抖动，$\theta_{bb}$ 是每次 bang-bang correction 的 phase step。锁定需要 phase step 能 bracket frequency error，简化条件为：

English: Here $\delta f$ is the input/oscillator frequency error, $\phi(t)$ is input phase jitter, and $\theta_{bb}$ is the phase step per bang-bang correction. Lock requires the phase step to bracket the frequency error, giving the simplified condition:

$$
|\delta f|<f_{bb}
$$

中文：在低噪声 hunting limit-cycle 条件下，简化 peak-to-peak jitter 可以估为：

English: Under low-noise hunting-limit-cycle conditions, simplified peak-to-peak jitter can be estimated as:

$$
J_{pp}=4\pi\frac{f_{bb}}{f_{nom}}
$$

中文：这条公式把 tradeoff 说得很直接：增大 $f_{bb}$ 可以提高 frequency tracking 和 slope-overload tolerance，但也会增加 deterministic hunting jitter。减小 $f_{bb}$ 可以降低 generated jitter，但会降低可跟踪频偏和低频相位斜率的能力。

English: This equation makes the tradeoff explicit: increasing $f_{bb}$ improves frequency tracking and slope-overload tolerance, but increases deterministic hunting jitter. Decreasing $f_{bb}$ reduces generated jitter, but lowers the ability to track frequency offset and low-frequency phase slope.

### 35.3 Duty Cycle, Frequency Offset, and Slope Overload

中文：在有静态 frequency offset 时，early/late decision 的平均占空比会偏离 50%。一个常用一阶关系是：

English: With static frequency offset, the average duty cycle of early/late decisions moves away from 50%. A useful first-order relation is:

$$
C=\frac{1}{2}+\frac{\delta f}{2f_{bb}}
$$

中文：当 $\delta f$ 接近 $f_{bb}$ 时，detector 输出会接近单边饱和，loop 失去对额外频偏或 jitter slope 的余量。对 sinusoidal input phase jitter $\phi(t)=A\sin(2\pi f_{mod}t)$ 且 $\delta f\approx0$ 的情况，slope-overload 前的近似幅度尺度为：

English: As $\delta f$ approaches $f_{bb}$, the detector output becomes nearly one-sided and the loop loses margin for additional frequency offset or jitter slope. For sinusoidal input phase jitter $\phi(t)=A\sin(2\pi f_{mod}t)$ with $\delta f\approx0$, the approximate amplitude scale before slope overload is:

$$
A_{\max}\approx\frac{f_{bb}}{f_{mod}}
$$

中文：这不是完整 JTOL mask，但它解释了为什么 bang-bang CDR 的 jitter tolerance 与 actuator step、loop update rate 和 jitter frequency 紧密相连。高频 jitter 更容易超过 phase actuator 的最大追踪斜率；低频 jitter 更容易被 loop 跟踪，但可能带来 recovered clock wander 或 jitter-transfer peaking。

English: This is not a complete JTOL mask, but it explains why bang-bang CDR jitter tolerance is tightly tied to actuator step, loop update rate, and jitter frequency. High-frequency jitter more easily exceeds the maximum trackable phase-actuator slope; low-frequency jitter is easier to track but can create recovered-clock wander or jitter-transfer peaking.

### 35.4 Second-Order Bang-Bang Loop Review

中文：second-order bang-bang CDR 加入 integrator 后，可以扩大 frequency tracking range，而不必只靠增大 $f_{bb}$。一个实用 review 变量是 proportional correction 与 integral correction 的比值：

English: A second-order bang-bang CDR adds an integrator, increasing frequency tracking range without relying only on a larger $f_{bb}$. A useful review variable is the ratio of proportional correction to integral correction:

$$
\xi\equiv
\frac{\Delta\theta_{\mathrm{proportional}}}
{\Delta\theta_{\mathrm{integral}}}
$$

中文：$\xi$ 不应被随意等同于 linear PLL damping factor。它是 bang-bang loop 中 proportional step、integrator update、latency 和 nonlinear orbit 共同作用下的稳定性尺度。设计上，$f_{bb}$ 更直接影响 jitter generation/tolerance 的 phase-step tradeoff，而 integrator path 更直接影响 frequency offset acquisition 和 long-term tracking。

English: $\xi$ should not be casually equated with the damping factor of a linear PLL. It is a stability scale shaped by proportional step, integrator update, latency, and nonlinear orbits in a bang-bang loop. In design terms, $f_{bb}$ more directly controls the phase-step tradeoff for jitter generation/tolerance, while the integrator path more directly controls frequency-offset acquisition and long-term tracking.

### 35.5 Review Checklist Added

| Review item | Question |
|---|---|
| Phase step | What physical PI/DCO/DLL step corresponds to $\theta_{bb}$? |
| Tracking range | Is $|\delta f|<f_{bb}$ satisfied with margin across SSC, ppm offset, and clock tolerance? |
| Hunting jitter | Is $J_{pp}$ from bang-bang hunting included in the timing budget? |
| Slope overload | Is sinusoidal jitter tolerance limited by actuator slew before slicer margin is exhausted? |
| Second-order path | Is the integrator range separated from proportional jitter-generation tradeoff? |
| Latency | Does sampler, retimer, DSP, loop filter, PI/DCO update, and clock-tree delay change the nonlinear orbit? |

### 35.6 Source Provenance Added

| Source | Type | Status | Reusable knowledge promoted |
|---|---|---|---|
| "Designing Bang-Bang PLLs for Clock and Data Recovery in Serial Data Transmission" | Paper PDF | Balanced Ingest 2026-07-05; archived in `90_Archive/processed/2026/papers/bang_bang_plls_cdr_serial_data_transmission/` | Flip-flop bang-bang CDR motivation, first-order bang-bang phase-step equations, lock range, hunting jitter, duty-cycle/frequency-offset relation, slope-overload intuition, second-order stability-factor framing |
| Nicola Da Dalt, "A Design-Oriented Study of the Nonlinear Dynamics of Digital Bang-Bang PLLs," IEEE TCAS-I, 2005 | IEEE paper PDF | Balanced Ingest 2026-07-05; archived in `90_Archive/processed/2026/papers/da_dalt_nonlinear_dynamics_bbpll_2005/` | Condensed nonlinear BBPLL orbit/limit-cycle model, loop-delay effect on timing jitter, design-oriented validation of low-noise versus linearized analysis |

---

## Last Updated

2026-07-05
