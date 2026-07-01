---

title: "PLL Fundamentals"
domain: "AnalogIC_SerDes"
tags:

* PLL
* Clocking
* PhaseNoise
* Jitter
* CDR
* SerDes
* PCIe7
* Synopsys
  created: 2026-07-01
  updated: 2026-07-01
  source: "ChatGPT technical notes and Synopsys role preparation"
  status: "active"

---

# PLL Fundamentals

## 中文补充翻译

这篇笔记解释 PLL 的基本结构和 SerDes 中的作用。PLL 的目标是从 reference clock 生成频率更高、相位受控的本地 clock，典型 charge-pump PLL 包含 PFD、charge pump、loop filter、VCO 和 divider。PLL 不是单个 block，而是一个反馈系统。

核心 tradeoff 包括 loop bandwidth、stability、lock time、phase noise、reference spur、VCO tuning range、KVCO、divider noise、charge pump mismatch、supply sensitivity 和 clock distribution。更宽 bandwidth 可以压低部分 VCO close-in noise 并加快 lock，但会传递更多 reference / PFD / CP noise，也可能增加 spur 和 stability 风险；更窄 bandwidth 可以滤掉 reference noise，但会留下更多 VCO noise。

在 SerDes 中，PLL 输出最终会影响 TX launch clock、RX local clock、CDR phase interpolator、sampler 或 ADC。设计 review 中不能只问“PLL jitter 是多少”，还要问 carrier frequency、integration bandwidth、measurement point、clock tree、PI、supply noise 和 CDR interaction。

## Purpose

This note summarizes PLL fundamentals from the perspective of high-speed SerDes / PCIe 7.0 clocking preparation.

The goal is to understand PLL architecture, loop dynamics, phase noise, jitter, loop bandwidth tradeoffs, and how PLL behavior affects SerDes timing margin.

This note supports Synopsys preparation, especially for PCIe 7.0 clocking and analog / mixed-signal IP work.

---

## 1. Big Picture

PLL means phase-locked loop.

A PLL generates an output clock whose phase and frequency are locked to a reference clock.

In SerDes, PLLs are used for:

* high-speed clock generation
* TX serialization clock
* RX sampling clock support
* multi-phase clock generation
* CDR support
* frequency multiplication
* clock distribution
* jitter filtering, depending on architecture

Key idea:

```text
Reference clock
↓
PLL
↓
Low-jitter high-frequency clock
↓
SerDes TX / RX / CDR / sampler
```

For PCIe 7.0 / high-speed PAM4 SerDes, PLL quality directly affects sampling timing, eye margin, and BER.

---

## 2. Basic PLL Architecture

A classical charge-pump PLL contains:

```text
Reference clock
↓
PFD
↓
Charge pump
↓
Loop filter
↓
VCO
↓
Divider
↓
Back to PFD
```

Main blocks:

* PFD: phase-frequency detector
* CP: charge pump
* LF: loop filter
* VCO: voltage-controlled oscillator
* Divider: divides VCO output back to reference comparison frequency

The PLL adjusts the VCO control voltage until the divided output clock aligns with the reference clock.

---

## 3. PFD: Phase-Frequency Detector

The PFD compares the reference clock phase with the divided feedback clock phase.

It generates UP and DOWN pulses.

If reference leads feedback:

```text
Reference arrives first
↓
UP pulse
↓
charge pump increases control voltage
↓
VCO frequency increases
```

If feedback leads reference:

```text
Feedback arrives first
↓
DOWN pulse
↓
charge pump decreases control voltage
↓
VCO frequency decreases
```

Important PFD topics:

* dead zone
* reset delay
* phase detection range
* mismatch between UP and DOWN paths
* reference spur generation
* metastability
* minimum pulse width

In high-performance PLLs, PFD non-idealities can create spurs and jitter.

---

## 4. Charge Pump

The charge pump converts PFD UP / DOWN pulses into current pulses.

These pulses charge or discharge the loop filter.

Important parameters:

* charge pump current
* UP / DOWN current matching
* output impedance
* leakage current
* switching charge injection
* current noise
* compliance range

Charge pump mismatch can create static phase offset and reference spurs.

Chain:

```text
UP / DOWN mismatch
↓
periodic ripple on control voltage
↓
VCO frequency modulation
↓
reference spur / jitter
```

Important interview point:

```text
Charge pump mismatch and leakage are not just small circuit errors.
They can become clock spurs and deterministic jitter.
```

Tiny error, giant review meeting. Analog design, naturally.

---

## 5. Loop Filter

The loop filter converts charge pump current pulses into a smoother VCO control voltage.

It determines much of the PLL loop dynamics.

Common passive loop filter elements:

* resistor
* capacitor
* second capacitor for high-frequency pole
* sometimes higher-order filtering

The loop filter affects:

* loop bandwidth
* damping factor
* phase margin
* lock time
* reference spur
* noise shaping
* control voltage ripple

Simplified role:

```text
Charge pump pulses
↓
Loop filter
↓
Smooth VCO control voltage
```

Bad loop filter design can cause:

* instability
* excessive peaking
* slow lock
* poor jitter
* large spur
* poor filtering of charge pump ripple

---

## 6. VCO

The VCO generates an oscillation frequency controlled by voltage.

Simplified relation:

```text
fout = ffree + KVCO × Vctrl
```

where:

* `ffree` is free-running frequency
* `KVCO` is VCO gain
* `Vctrl` is control voltage

Important VCO parameters:

* tuning range
* phase noise
* KVCO
* supply sensitivity
* temperature sensitivity
* amplitude
* power
* startup robustness
* pushing and pulling
* layout symmetry
* tank Q, if LC VCO
* delay cell noise, if ring VCO

VCO is often the dominant high-frequency phase noise contributor outside PLL bandwidth.

---

## 7. Divider

The divider divides the VCO output frequency before feeding it back to the PFD.

For an integer-N PLL:

```text
fout = N × fref
```

where:

* `fout` is PLL output frequency
* `fref` is reference frequency
* `N` is divider ratio

Divider issues:

* divider noise
* duty-cycle distortion
* high-speed operation
* power consumption
* modulus switching, in fractional-N PLL
* spur generation
* layout coupling

Divider noise appears inside the PLL loop and can contribute to output jitter.

---

## 8. Integer-N vs Fractional-N PLL

## Integer-N PLL

Output frequency is an integer multiple of reference frequency.

```text
fout = N × fref
```

Advantages:

* simpler
* lower fractional spur concern
* easier analysis

Disadvantages:

* frequency resolution limited by reference frequency
* may require high divider ratio

## Fractional-N PLL

Output frequency can be a fractional multiple of reference frequency.

```text
fout = (N + fraction) × fref
```

Advantages:

* fine frequency resolution
* flexible frequency planning

Disadvantages:

* quantization noise
* fractional spurs
* sigma-delta modulator noise
* more complex spur and noise behavior

In SerDes, the architecture depends on required frequencies, protocol standards, jitter targets, and implementation constraints.

---

## 9. PLL Lock

PLL lock means output phase and frequency are aligned with reference after division.

Lock has two aspects:

## Frequency Lock

The output frequency reaches the desired multiple of reference frequency.

## Phase Lock

The phase error between reference and feedback becomes stable and small.

Lock behavior depends on:

* loop bandwidth
* damping factor
* VCO tuning range
* initial frequency error
* charge pump current
* loop filter
* PFD range
* supply and temperature conditions

Important questions:

* What is lock time?
* Is there false lock risk?
* Does lock work across PVT?
* Does startup sequence guarantee correct operating point?
* Does VCO tuning range cover all corners?

---

## 10. Loop Bandwidth

PLL loop bandwidth is one of the most important design parameters.

It roughly determines how fast the PLL tracks reference phase variation and how strongly it suppresses VCO noise.

Simplified idea:

```text
Inside loop bandwidth:
PLL output follows reference-related noise.

Outside loop bandwidth:
PLL output is dominated more by VCO noise.
```

But real PLL noise also includes PFD, charge pump, divider, loop filter, and buffer contributions.

## Wider Bandwidth

Pros:

* suppresses VCO noise over wider frequency range
* faster lock
* faster tracking

Cons:

* passes more reference noise
* passes more PFD / charge pump / divider noise
* may increase reference spur sensitivity
* stability becomes harder

## Narrower Bandwidth

Pros:

* filters reference noise better
* can reduce in-band noise contribution

Cons:

* less VCO noise suppression
* slower lock
* slower tracking
* more sensitivity to VCO close-in noise

Key SerDes question:

```text
Which noise should the PLL track, and which noise should it filter?
```

This is the adult version of PLL design. The childish version is “make bandwidth bigger because fast is good,” which is how circuits learn to scream.

---

## 11. PLL Stability

A PLL is a feedback loop, so stability matters.

Important loop metrics:

* loop bandwidth
* phase margin
* damping factor
* peaking
* settling behavior
* lock time

Too little phase margin can cause:

* jitter peaking
* ringing in phase response
* poor settling
* lock instability

In SerDes, PLL peaking is dangerous because it can amplify jitter in certain frequency ranges.

Important idea:

```text
A PLL can be locked but still have poor jitter behavior.
```

Lock does not mean good. It only means the circuit has chosen one way to disappoint you.

---

## 12. PLL Noise Sources

PLL output phase noise includes contributions from:

* reference clock
* PFD
* charge pump
* loop filter resistor noise
* VCO
* divider
* clock buffers
* supply noise
* substrate noise
* coupling from digital circuits
* fractional-N quantization noise, if applicable

Noise shaping depends on where the noise enters the loop.

Simplified view:

```text
Reference / PFD / CP / divider noise:
mostly important inside loop bandwidth

VCO noise:
mostly important outside loop bandwidth
```

But always check the actual transfer functions and simulation results.

---

## 13. Phase Noise to Jitter

PLL phase noise becomes time-domain jitter.

Key relation:

```text
Δt = Δφ / (2πf0)
```

Integrated RMS jitter can be estimated by integrating phase noise over a relevant offset-frequency range.

Important reminder:

```text
Jitter number without integration bandwidth is incomplete.
```

Bad statement:

```text
PLL jitter is 80 fs.
```

Better statement:

```text
PLL output integrated RMS jitter is 80 fs from 10 kHz to 100 MHz at 16 GHz output frequency under TT, 25°C.
```

The second sentence is uglier, which is how you know it might be useful.

Related note:

```text
phase_noise_jitter.md
```

---

## 14. Reference Spur

Reference spur is a periodic tone at offset frequencies related to reference frequency.

Possible causes:

* charge pump mismatch
* charge pump leakage
* PFD reset mismatch
* loop filter ripple
* supply coupling
* substrate coupling
* divider switching
* reference feedthrough

Chain:

```text
Periodic disturbance at reference rate
↓
VCO control ripple
↓
frequency modulation
↓
spur near carrier
```

Spurs can create deterministic jitter and degrade SerDes margin.

Important questions:

* What is spur level?
* Which offset frequency?
* Does it fall into a sensitive jitter band?
* Does it affect compliance?
* Does layout coupling worsen it?

---

## 15. Supply Noise Sensitivity

PLL is sensitive to supply noise through:

* VCO supply pushing
* charge pump current variation
* divider delay variation
* clock buffer delay modulation
* bias current variation
* reference or LDO noise

Important chain:

```text
Supply noise
↓
VCO frequency modulation
↓
phase modulation
↓
PLL output jitter
↓
SerDes eye closure
```

This connects PLL design to LDO and power integrity.

Related notes:

```text
../LDO_Bandgap/serdes_power_integrity.md
../LDO_Bandgap/ldo_psrr_notes.md
```

---

## 16. PLL in SerDes

In SerDes, PLL may support:

* TX clock generation
* RX sampling clock
* multi-lane clock distribution
* CDR reference
* local high-speed clocks
* clock multiplication
* retimer clocking

SerDes PLL requirements often include:

* low integrated jitter
* low phase noise
* low spur
* robust lock
* wide PVT coverage
* supply noise tolerance
* compatibility with protocol frequency plan
* low power
* small area
* good testability

For PCIe 7.0 / PAM4, PLL jitter matters because timing margin is small.

---

## 17. PLL and CDR Relationship

PLL and CDR are related but not identical.

## PLL

Locks output clock to a reference clock.

```text
Reference clock → clean generated clock
```

## CDR

Recovers timing from incoming data.

```text
Incoming data transitions → recovered sampling clock
```

A CDR may contain PLL-like loop structures, but its phase detector often works on data transitions.

Key differences:

* PLL compares clock to clock.
* CDR extracts phase information from data.
* CDR performance depends on data pattern and transition density.
* CDR interacts strongly with equalization and channel ISI.

Related future note:

```text
cdr_fundamentals.md
```

---

## 18. Important PLL Simulations

Useful simulations:

* operating point
* VCO tuning curve
* lock acquisition
* phase noise
* integrated jitter
* transient jitter
* reference spur
* supply pushing
* PSRR impact
* loop stability
* PVT corners
* Monte Carlo
* startup
* post-layout extraction
* supply noise injection
* clock buffer jitter
* divider operation

Record conditions:

* reference frequency
* output frequency
* divider ratio
* loop bandwidth
* phase margin
* integration bandwidth
* process corner
* temperature
* supply voltage
* load condition
* pre-layout or post-layout

---

## 19. Common PLL Design Tradeoffs

## Bandwidth vs Noise

Wider bandwidth suppresses more VCO noise but passes more reference and in-loop noise.

## Bandwidth vs Lock Time

Wider bandwidth usually locks faster.

## Bandwidth vs Stability

Wider bandwidth can reduce phase margin if compensation is poor.

## KVCO vs Tuning Range

Higher KVCO gives wider tuning but increases sensitivity to control noise.

## Power vs Phase Noise

Lower power usually worsens phase noise.

## Spur vs Lock Speed

Stronger charge pump current can improve lock speed but may increase ripple / spur if not managed.

## Area vs Noise

Better passive components and decoupling may require more area.

No free lunch. PLL design is mostly deciding which monster gets fed first.

---

## 20. Interview Explanation

Short explanation:

```text
A PLL locks an output clock to a reference clock by comparing the reference with a divided version of the output, generating an error through the PFD and charge pump, filtering it, and controlling the VCO. The loop bandwidth determines how reference noise and VCO noise are shaped. Inside the bandwidth, the output tends to follow reference and in-loop noise; outside the bandwidth, VCO noise usually dominates. For SerDes, PLL phase noise and jitter directly affect sampling margin and eye closure.
```

Synopsys-focused explanation:

```text
For PCIe 7.0 SerDes clocking, I would focus on PLL jitter, phase noise, spur, loop bandwidth, and supply sensitivity. The PLL is not only a frequency multiplier. Its noise and jitter become timing uncertainty for TX or RX clocks. The right analysis should connect PLL phase noise, integrated jitter, LDO supply noise, clock buffer delay modulation, and the SerDes jitter budget.
```

Senior-level explanation:

```text
The key is to analyze the PLL at both circuit and system levels. At circuit level, PFD, charge pump, loop filter, VCO, divider, and buffers each contribute noise, spur, and non-idealities. At system level, the important question is how those errors affect SerDes timing margin. Loop bandwidth should be chosen based on reference noise, VCO noise, in-loop noise, lock time, spur, stability, and the CDR / receiver jitter tolerance requirements.
```

---

## 21. Common Interview Questions

## Q1: What is a PLL?

A PLL is a feedback system that locks an output clock phase and frequency to a reference clock.

## Q2: What are the main blocks of a charge-pump PLL?

PFD, charge pump, loop filter, VCO, divider, and output buffers.

## Q3: What does the PFD do?

It compares the phase and frequency of the reference clock and divided feedback clock, then generates UP or DOWN pulses.

## Q4: What does the charge pump do?

It converts UP / DOWN pulses into current pulses that charge or discharge the loop filter.

## Q5: What determines PLL loop bandwidth?

Charge pump current, loop filter values, VCO gain, divider ratio, and loop architecture.

## Q6: How does loop bandwidth affect phase noise?

Inside loop bandwidth, reference and in-loop noise are more strongly transferred to output. Outside loop bandwidth, VCO noise usually dominates.

## Q7: Why does high KVCO increase sensitivity?

A higher KVCO means a small control voltage noise creates larger frequency variation, which can increase phase noise or jitter.

## Q8: What causes reference spur?

Charge pump mismatch, leakage, PFD reset effects, control voltage ripple, divider switching, and coupling from reference-related activity.

## Q9: How does supply noise affect PLL?

Supply noise can modulate VCO frequency, charge pump current, divider delay, or buffer delay, creating phase noise and jitter.

## Q10: Why is PLL important in SerDes?

Because PLL clock jitter directly affects TX timing, RX sampling timing, CDR behavior, eye margin, and BER.

---

## 22. Personal Connection to My Experience

This note connects to my previous analog and mixed-signal experience.

Relevant background:

* PLL / fractional-N PLL
* ADPLL / DCO
* phase noise
* jitter
* VCO / DCO tuning
* PFD / charge pump behavior
* loop bandwidth
* LDO supply noise
* analog IP integration
* PVT simulation
* post-layout sensitivity

How to present this experience:

```text
My PLL and clocking experience is relevant to SerDes because high-speed links depend on low-jitter clock generation and clean sampling timing. PLL phase noise, loop bandwidth, supply sensitivity, and clock buffer jitter all affect eye margin. In PCIe 7.0 / PAM4 systems, these effects become more critical because both timing and voltage margins are tight.
```

---

## 23. Open Questions

* 待确认: What PLL architecture is used in Synopsys PCIe 7.0 IP?
* 待确认: What output clock frequencies are generated?
* 待确认: What loop bandwidth is targeted?
* 待确认: What integrated jitter budget is required?
* 待确认: What phase noise integration range is used?
* 待确认: What is the dominant noise contributor?
* 待确认: How is supply-induced jitter simulated?
* 待确认: How are reference spurs verified?
* 待确认: How is clock distributed across lanes?
* 待确认: How does the PLL interact with CDR in the actual architecture?

---

## Source Conversations / Source Packets

* `../../00_Inbox/manual_batches/batch2_serdes_pcie_pll_cdr_adc_2026-07-01/source_packet.md`

---

## 24. Related Notes

* `phase_noise_jitter.md`
* `cdr_fundamentals.md`
* `pcie7_clocking_notes.md`
* `../SerDes/pcie7_overview.md`
* `../SerDes/serdes_architecture_overview.md`
* `../LDO_Bandgap/serdes_power_integrity.md`
* `../LDO_Bandgap/ldo_psrr_notes.md`
* `../ADC/sampling_jitter_adc.md`
* `../Interview_QA/synopsys_relevant_qa.md`
* `../Study_Plans/synopsys_4_week_prep_plan.md`
* `../../02_Synopsys_Work/synopsys_master_note.md`
* `../../02_Synopsys_Work/onboarding_plan.md`

---

## 25. Next Actions

1. Create `cdr_fundamentals.md`.
2. Create `pcie7_clocking_notes.md`.
3. Add PLL block diagrams later.
4. Add PLL loop transfer equations later.
5. Add real phase noise / jitter examples from past work if available.
6. Add Synopsys-specific PLL architecture notes after joining.

---

## Last Updated

2026-07-01
