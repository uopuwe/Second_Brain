---
title: "PLL Fundamentals"
domain: "AnalogIC_SerDes"
tags:
  - PLL
  - Clocking
  - PhaseNoise
  - Jitter
  - CDR
  - SerDes
  - PCIe7
  - Synopsys
created: 2026-07-01
updated: 2026-08-08
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

### 6.1 LC-Tank $C_1$ And $R_p$ Interpretation

中文：教材简化 LC tank 中的 $C_1$ 应解释为参与谐振的总等效电容，而不是默认等于电感自身寄生电容。实际值包括 varactor、switched-capacitor bank、电感和有源器件寄生、布线以及 buffer/divider loading。

English: In a simplified LC-tank model, $C_1$ should be interpreted as the total effective capacitance participating in resonance, not automatically as the inductor's parasitic capacitance. The implemented value includes the varactor, switched-capacitor bank, inductor and active-device parasitics, routing, and buffer/divider loading.

$$
C_{tank}=C_{var}+C_{bank}+C_{L,par}+C_{MOS}+C_{wire}+C_{load}.
$$

中文：$R_p$ 通常是把整个 tank 损耗折算到谐振点的并联等效电阻，不是设计者主动并联的真实电阻。高 $Q$ 且以电感串联损耗 $R_s$ 起步时，谐振点附近可用

English: $R_p$ normally represents the total tank loss transformed into an equivalent parallel resistance at resonance; it is not a physical resistor intentionally placed across the tank. Starting from inductor series loss $R_s$ and assuming high $Q$, the near-resonance approximation is

$$
R_p\approx\frac{\omega_0^2L^2}{R_s}=Q\omega_0L.
$$

中文：工程分析要区分仅电感的 $R_{p,L}$ 与包含 varactor、switch、active-device $r_o$ 和 loading 的 $R_{p,tank}$。$C_{tank}$ 主要决定振荡频率、调谐范围和 $K_{VCO}$；$R_{p,tank}$ 主要决定 $Q$、启动余量、摆幅、维持功耗和相噪。系数形式的启动条件依赖 single-ended/differential 定义，不应脱离 topology 死记 $g_mR_p$ 的常数。

English: Engineering analysis should distinguish the inductor-only $R_{p,L}$ from $R_{p,tank}$ including varactor, switch, active-device $r_o$, and load loss. $C_{tank}$ mainly sets oscillation frequency, tuning range, and $K_{VCO}$; $R_{p,tank}$ mainly sets $Q$, startup margin, amplitude, sustaining power, and phase noise. The coefficient in a $g_mR_p$ startup rule depends on single-ended/differential and topology definitions and should not be memorized without that context.

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
pll_phase_noise_jitter.md
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

### 19.1 Five-Question Design Review Lens

中文：一个简洁的 PLL design review 可以用五个问题防止讨论停留在单一 block 或单一数字：测量定义是什么；误差源从哪个注入点经哪个 transfer function 到输出；当前问题属于锁定后小信号、离散采样还是非线性捕获；优化代价转移到 jitter、spur、lock time、power、area 还是 yield；以及 silicon 上如何观测和证伪。

English: A compact PLL design review can use five questions to avoid reducing the discussion to one block or one number: What is the measurement definition? Which error source enters at which injection point and reaches the output through which transfer function? Is the problem a locked small-signal, discrete-time sampling, or nonlinear acquisition problem? Where does the optimization cost move among jitter, spur, lock time, power, area, and yield? How will silicon make the hypothesis observable and falsifiable?

Review shorthand:

1. Define the metric, node, mode, PVT, load, filtering, and integration range.
2. Map each error source to its injection point and transfer function.
3. Select the correct linear, sampled-data, or nonlinear model.
4. Close system budgets instead of optimizing one block in isolation.
5. Plan calibration, DFT, observability, and lab/ATE evidence before tapeout.

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
* `../../00_Inbox/manual_batches/chat_delta_2026-08-08/new_conversations/6a622892-1564-83ea-b248-fd61c8ac2c09.md` - "C1和Rp在VCO中的作用"; conversation-derived LC-tank interpretation, requiring textbook/PDK verification before signoff use.
* `../../00_Inbox/manual_batches/chat_delta_2026-08-08/new_conversations/6a67f666-2a2c-83ea-a9f1-ae66ef8c79d0.md` - "PLL核心思维模式"; conversation-derived design-review checklist, not a primary technical source.

---

## 24. Related Notes

* `pll_phase_noise_jitter.md`
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

## 26. Batch 1 Extracted Knowledge - 2026-07-02

### 26.1 Type-II CPPLL Loop Bandwidth Derivation

For a charge-pump PLL with divider ratio `N`, charge-pump gain `Kpd`, VCO gain `Kvco`, and loop-filter impedance `Z(s)`:

```text
G(s) = (Kpd * Kvco / N) * Z(s) / s
```

For a simple PI filter:

```text
Z(s) = R + 1/(sC)
K = Kpd * Kvco / N
characteristic equation: s^2 + K*R*s + K/C = 0
omega_n = sqrt(K/C)
zeta = (R/2) * sqrt(K*C)
f_BW ~= omega_n / (2*pi)
```

Worked example from the conversation:

```text
Icp = 200 uA
Kvco = 200 MHz/V
N = 112
C = 20 pF

omega_n ~= sqrt((Icp*Kvco/N)/C)
f_BW is on the order of a few MHz, about 3.3 MHz with the simplified assumptions.
```

Design implication: use this only as a sizing estimate. Real loop bandwidth and peaking must be verified with the actual PFD/CP gain, loop filter, divider ratio, VCO gain curve, PVT, parasitics, and nonlinear simulations.

### 26.2 SerDes PLL vs RF PLL Emphasis

- SerDes PLL design is usually judged by time-domain sampling or launch jitter after the clock tree and CDR interaction.
- RF PLL design is often judged more directly by phase-noise spectrum, close-in phase noise, EVM, ACLR, and spur purity.
- SerDes PLL loop bandwidths are often wider than narrowband RF PLLs because the link can tolerate or track some low-frequency wander while needing low high-frequency sampling jitter.
- PLL output phase noise shaping:

```text
S_out ~= |H_ref|^2*S_ref + |H_vco|^2*S_vco + in-loop noise terms
```

Inside the loop bandwidth, reference and in-loop noise dominate more strongly. Outside the loop bandwidth, VCO noise dominates more strongly.

### 26.3 GF22FDX CPPLL Lessons to Reuse

The extracted design checklist from the GF22FDX CPPLL conversation:

- Start with architecture: PFD, charge pump, passive second/third-order loop filter, LC-VCO or ring VCO, divider, output buffer, bias, and supply isolation.
- PFD: check reset delay, dead zone, phase-detector linearity, and reference-spur contribution.
- Charge pump: trim UP/DN mismatch, check output current versus control voltage, feedthrough, leakage, and compliance range.
- Loop filter: place the zero near the target loop bandwidth region and place high-frequency poles to control ripple and peaking.
- VCO: keep `Kvco` low enough for jitter sensitivity while preserving tuning range; use switched capacitor banks for coarse tuning and varactors for fine tuning.
- Divider: include divider and clock-buffer noise in the PLL output budget; they are often underestimated.
- Verification: run lock transient, loop stability, PSS/PNoise, transient noise, reference spur, supply pushing, PVT, Monte Carlo, and extracted simulations.

待确认: Exact GF22FDX internal CPPLL schematic choices, device options, and signoff targets are not public and should not be asserted as facts.

### 26.4 LC-VCO Extraction Reminders

- Use EM extraction for inductors, shields, and high-Q routing; use active-device PEX for the oscillator core.
- From extracted impedance:

```text
L_eff = Im(Z) / (2*pi*f)
Q = Im(Z) / Re(Z)
```

- Keep self-resonant frequency well above the operating band where possible.
- Startup rule of thumb: `gm*Rp > 1`; practical margin target is often greater than 2 to 3.
- Re-check phase noise, tuning range, supply pushing, and startup after replacing ideal inductors with EM-extracted nports.

### 26.5 Source Conversations

- `../../00_Inbox/raw_chat_exports/chatgpt_export_2026-07-01/md_by_conversation/2026-05-13__SerDes_PLL_CDR_带宽.md`
- `../../00_Inbox/raw_chat_exports/chatgpt_export_2026-07-01/md_by_conversation/2026-02-15__SerDes_vs_RF_PLL_Jitter.md`
- `../../00_Inbox/raw_chat_exports/chatgpt_export_2026-07-01/md_by_conversation/2026-04-21__GF_22FDX_CPPLL设计.md`

---

## 27. Balanced Ingest 2026-07-05 - CPPLL and PLL Architecture Sources

Source update:

- Hanumolu, Brownlee, Mayaram, and Moon, "Analysis of Charge-Pump Phase-Locked Loops," IEEE TCAS-I, Vol. 51, No. 9, September 2004.
- Nguyen and Pham, "An Overview of Phase-Locked Loop: From Fundamentals to the Frontier," Sensors, 2025.
- Dutta et al., "Exploring the Landscape of Phase-Locked Loop Architectures: A Comprehensive Review," review PDF.
- Archived source packet: [PLL oscillator sources 2026-07-05](<../../90_Archive/processed/2026/papers/pll_oscillator_sources_2026-07-05/>)
- Source confidence: high for Hanumolu et al. CPPLL discrete-time/state-space analysis; moderate for the two broad overview papers because they are useful for taxonomy and vocabulary but should not be treated as primary formula authority.

### 27.1 Why This Batch Belongs Here

中文：这批资料的共同价值是把 PLL 从“方框图”推进到 design-review 层级：CPPLL 不是连续时间二阶环路的简单延伸，architecture taxonomy 也不能替代具体的 loop dynamics、noise transfer、reference update rate、charge-pump nonideality 和 clocking application constraint。对 SerDes 来说，最重要的不是记住更多 PLL 类型，而是知道每种架构改变了哪些 noise path、locking behavior、spur mechanism 和 verification burden。

English: The shared value of this batch is to move PLL knowledge from block diagrams to design-review depth: a CPPLL is not just a continuous-time second-order loop with one more component, and architecture taxonomy cannot replace specific loop dynamics, noise transfer, reference update rate, charge-pump nonideality, and clocking application constraints. For SerDes, the important skill is not memorizing more PLL types, but knowing which noise paths, locking behaviors, spur mechanisms, and verification burdens each architecture changes.

### 27.2 Third-Order CPPLL Is A Sampled-Data Loop

中文：Hanumolu 等人的 CPPLL analysis 强调：third-order charge-pump PLL 同时有 large-signal lock acquisition 和 small-signal tracking 行为，且 PFD/CP action 是 reference-rate sampled event。连续时间近似对 intuition 很有用，但当 loop bandwidth 接近 reference update rate 时，sampled-data delay 会引入额外 phase shift，可能让 continuous-time Bode phase-margin 看起来可接受的 loop 在 z-domain pole location 上失稳。

English: Hanumolu et al.'s CPPLL analysis emphasizes that a third-order charge-pump PLL has both large-signal lock acquisition and small-signal tracking behavior, and the PFD/CP action is a reference-rate sampled event. Continuous-time approximations are useful for intuition, but when loop bandwidth approaches the reference update rate, sampled-data delay adds phase shift and can make a loop that looks acceptable in continuous-time Bode phase margin unstable in z-domain pole location.

中文：一个实用 review rule 是：不要只问 loop bandwidth 和 phase margin，也要问 reference frequency / PFD update rate 与 loop bandwidth 的比例。paper 的 example 显示某个 CPPLL 在 update-rate-to-loop-bandwidth ratio 约为 3 左右会遇到 sampled-data stability limit；这个数字不是通用规格，但它很好地提醒 designer：reference-rate sampling 本身是 stability constraint。

English: A practical review rule is: do not ask only for loop bandwidth and phase margin; also ask for the ratio between reference frequency or PFD update rate and loop bandwidth. The paper's example shows a sampled-data stability limit around an update-rate-to-loop-bandwidth ratio near 3 for that CPPLL; this number is not a universal specification, but it is an excellent reminder that reference-rate sampling itself is a stability constraint.

### 27.3 CPPLL Loop Filter Ripple And Third Pole

中文：third-order CPPLL 中，loop-filter resistor 引入稳定零点，但 charge-pump pulse 会在 control voltage 上产生 ripple；额外 capacitor 可以降低 ripple，却也引入第三个 pole，降低 phase margin。这个 tradeoff 在 SerDes PLL 中很实际：减小 ripple / spur 的动作可能同时改变 loop stability、settling、jitter peaking 和 VCO control-line noise transfer。

English: In a third-order CPPLL, the loop-filter resistor introduces a stabilizing zero, but the charge-pump pulse creates ripple on the control voltage; an added capacitor can reduce ripple, but it also introduces a third pole and reduces phase margin. This tradeoff is very practical in SerDes PLLs: an action that reduces ripple or spur can also change loop stability, settling, jitter peaking, and VCO control-line noise transfer.

中文：因此 CPPLL design review 应把 `R`, `C1`, `C2`, charge-pump current, divider ratio, VCO gain, reference frequency, reset delay, CP pulse width, and parasitic pole 放在同一张表里。只给一个 `f_BW` 或一个 damping factor 不够，因为 spur、ripple、noise transfer 和 sampled-data stability 都可能由被隐藏的实现细节决定。

English: Therefore a CPPLL design review should put `R`, `C1`, `C2`, charge-pump current, divider ratio, VCO gain, reference frequency, reset delay, CP pulse width, and parasitic poles in the same table. A single `f_BW` or damping factor is not enough, because spur, ripple, noise transfer, and sampled-data stability can be set by hidden implementation details.

### 27.4 Architecture Taxonomy Is A Starting Point

中文：两篇 overview / taxonomy paper 对长期 Second Brain 的价值主要是分类：APLL、DPLL、ADPLL、integer-N、fractional-N、sub-sampling PLL、injection-locked PLL、DLL、low-power PLL 和 specialized clock-recovery loops。分类有助于检索和面试表达，但不能直接给出 signoff conclusion；同一类 PLL 的 phase noise、spur、lock time 和 power 可能被 topology、process、frequency plan、reference source、divider、layout 和 supply isolation 完全改变。

English: The main value of the two overview/taxonomy papers for this long-term Second Brain is classification: APLL, DPLL, ADPLL, integer-N, fractional-N, sub-sampling PLL, injection-locked PLL, DLL, low-power PLL, and specialized clock-recovery loops. Classification helps retrieval and interview language, but it does not directly produce signoff conclusions; phase noise, spur, lock time, and power within the same PLL class can be completely changed by topology, process, frequency plan, reference source, divider, layout, and supply isolation.

中文：工程使用这些 review papers 时，应把它们当作 routing map，而不是 formula source。真正进入 design note 的结论必须来自 primary paper、textbook derivation、simulation result、measurement data 或明确的 project requirement。

English: In engineering use, these review papers should be treated as routing maps, not formula sources. Conclusions promoted into design notes should come from primary papers, textbook derivations, simulation results, measurement data, or explicit project requirements.

### 27.5 Added CPPLL Review Questions

中文：这批 source 给 `pll_fundamentals` 增加的最有用 review question 是：continuous-time loop analysis 和 sampled-data loop analysis 是否都通过？如果没有这个问题，designer 很容易只看 analog loop-gain Bode plot，而漏掉 PFD update rate、z-domain pole migration、CP pulse timing 和 reference-rate sampling 对 stability 的影响。

English: The most useful review question added by this source batch is: have both continuous-time loop analysis and sampled-data loop analysis passed? Without this question, a designer can look only at an analog loop-gain Bode plot and miss the effects of PFD update rate, z-domain pole migration, CP pulse timing, and reference-rate sampling on stability.

| Review item | Why it matters |
|---|---|
| Reference update rate versus loop bandwidth | Bounds sampled-data stability and loop delay sensitivity. |
| Third pole from ripple-suppression capacitor | Can reduce spur/ripple while degrading phase margin. |
| CP pulse width and reset delay | Affects dead zone, CP noise duty cycle, ripple, and spur. |
| VCO gain and divider ratio | Sets loop gain and converts control noise into phase noise. |
| Continuous-time and z-domain checks | Prevents a false sense of stability from continuous-time approximations alone. |
| Architecture label versus implementation detail | Prevents overgeneralizing from taxonomy papers. |

### 27.6 Source Provenance Added

| Source | Type | Status | Reusable knowledge promoted |
|---|---|---|---|
| Hanumolu, Brownlee, Mayaram, and Moon, "Analysis of Charge-Pump Phase-Locked Loops," IEEE TCAS-I, 2004 | IEEE paper PDF | Balanced Ingest 2026-07-05; archived in `90_Archive/processed/2026/papers/pll_oscillator_sources_2026-07-05/` | Third-order CPPLL sampled-data/state-space framing, continuous-time versus z-domain stability caution, reference-update-rate versus loop-bandwidth review item, loop-filter ripple/third-pole tradeoff |
| Nguyen and Pham, "An Overview of Phase-Locked Loop: From Fundamentals to the Frontier," Sensors, 2025 | Review paper PDF | Balanced Ingest 2026-07-05; archived in `90_Archive/processed/2026/papers/pll_oscillator_sources_2026-07-05/` | PLL architecture taxonomy and broad trend vocabulary; not used as primary formula authority |
| Dutta et al., "Exploring the Landscape of Phase-Locked Loop Architectures: A Comprehensive Review" | Review paper PDF | Balanced Ingest 2026-07-05; archived in `90_Archive/processed/2026/papers/pll_oscillator_sources_2026-07-05/` | PLL taxonomy and comparison vocabulary; source confidence treated as moderate because the PDF appears review-oriented and formula/detail claims require primary-source confirmation |

---

## 28. Deep Ingest 2026-07-05 - Rhee and Yu PLL System and Circuit Design

Source update:

- Woogeun Rhee and Zhiping Yu, *Phase-Locked Loops: System Perspectives and Circuit Design Aspects*, Wiley/IEEE Press, 2024.
- Archived source packet: [Rhee and Yu PLL book 2026-07-05](<../../90_Archive/processed/2026/books/phase_locked_loops_rhee_yu_2024/>)
- Source confidence: high for textbook-level PLL loop equations, CPPLL architecture, PFD/CP tradeoffs, fractional-N/DPLL taxonomy, and CDR metric framing; final silicon signoff still requires project-specific models and simulation.

### 28.1 Why This Book Belongs in the PLL Canon

中文：Rhee 和 Yu 这本书的长期价值在于它把 PLL 作为完整 feedback system，而不是一组孤立 building blocks。它从 continuous-time loop model、transient response、spectral purity、PFD/CP/VCO/divider circuit design，一直延伸到 fractional-N PLL、digital-intensive PLL 和 CDR PLL。对 SerDes/PCIe clocking 来说，这种 system-to-circuit-to-system 的视角比单独背诵 loop bandwidth 或 phase-noise formula 更重要。

English: The long-term value of Rhee and Yu's book is that it treats a PLL as a complete feedback system, not as isolated building blocks. It moves from continuous-time loop models, transient response, spectral purity, and PFD/CP/VCO/divider circuit design into fractional-N PLLs, digital-intensive PLLs, and CDR PLLs. For SerDes/PCIe clocking, this system-to-circuit-to-system view is more valuable than memorizing isolated loop-bandwidth or phase-noise formulas.

中文：本次 Deep Ingest 没有把整本书复制进一个新 handbook，而是把知识拆到 canonical notes：本文件保留 loop dynamics 与 CPPLL system model；[[pfd_charge_pump_notes]] 承接 PFD/CP 电路细节；[[pll_phase_noise_jitter]] 承接 spectral purity、spur 与 jitter conversion；[[pll_fractional_n_digital]] 承接 fractional-N、DSM、DPLL、BBPLL 和 HPLL；[[cdr_fundamentals]] 承接 CDR JGEN/JTRAN/JTOL。

English: This Deep Ingest did not copy the whole book into a new handbook. The knowledge was split into canonical notes: this file keeps loop dynamics and CPPLL system modeling; [[pfd_charge_pump_notes]] owns PFD/CP circuit detail; [[pll_phase_noise_jitter]] owns spectral purity, spurs, and jitter conversion; [[pll_fractional_n_digital]] owns fractional-N, DSM, DPLL, BBPLL, and HPLL; [[cdr_fundamentals]] owns CDR JGEN/JTRAN/JTOL.

### 28.2 Linear Model and Transfer Functions

中文：PLL 的 basic linear model 可以从 open-loop gain 开始。若 phase detector gain 为 $K_d$，VCO gain 为 $K_v$，loop filter 为 $F(s)$，则不含 divider 的 open-loop transfer function 为：

English: The basic PLL linear model starts from open-loop gain. If the phase-detector gain is $K_d$, VCO gain is $K_v$, and loop filter is $F(s)$, the open-loop transfer function without a divider is:

$$
G(s)=\frac{K_dK_vF(s)}{s}
$$

中文：对应 closed-loop phase transfer 和 phase-error transfer 为：

English: The corresponding closed-loop phase transfer and phase-error transfer are:

$$
H(s)=\frac{G(s)}{1+G(s)}
=
\frac{K_dK_vF(s)}{s+K_dK_vF(s)}
$$

$$
H_e(s)=\frac{1}{1+G(s)}
=
\frac{s}{s+K_dK_vF(s)}
$$

中文：这个 pair 是 PLL intuition 的核心：reference/in-loop source 通常被 low-pass shaped，VCO free-running phase noise 通常被 high-pass shaped。loop bandwidth 不是孤立指标，而是 noise partition、settling、spur rejection、jitter peaking 和 acquisition robustness 的共同结果。

English: This pair is the core PLL intuition: reference and in-loop sources are usually low-pass shaped, while free-running VCO phase noise is usually high-pass shaped. Loop bandwidth is not an isolated metric; it is the joint result of noise partition, settling, spur rejection, jitter peaking, and acquisition robustness.

### 28.3 Type-I and Type-II Loop Parameters

中文：一阶 Type-I PLL 的 loop filter 可视为 constant gain，open-loop gain 为：

English: A first-order Type-I PLL can treat the loop filter as a constant gain, giving:

$$
G(s)=\frac{K_dK_fK_v}{s}
$$

$$
K=K_dK_fK_v
$$

$$
H(s)=\frac{K}{s+K}
$$

中文：因此 unity-gain frequency 近似就是 $K$。这个模型简单，但因为没有额外 integrator，对 static frequency error、reference spur、noise shaping 和 acquisition 的能力有限。

English: Thus the unity-gain frequency is approximately $K$. This model is simple, but without an additional integrator it has limited ability for static frequency error, reference spur, noise shaping, and acquisition.

中文：二阶 Type-II active-loop model 可以写成 proportional-plus-integral control：

English: A second-order Type-II active-loop model can be written as proportional-plus-integral control:

$$
F(s)=\frac{1+s/\omega_z}{s/\omega_p}
$$

$$
F(s)=\alpha+\frac{\beta}{s}
$$

中文：对应 closed-loop denominator 可映射到标准二阶形式：

English: The closed-loop denominator maps to the standard second-order form:

$$
H(s)=
\frac{\omega_n^2(1+s/\omega_z)}
{s^2+2\zeta\omega_ns+\omega_n^2}
$$

$$
\omega_n=\sqrt{K\omega_z}
$$

$$
\zeta=\frac{1}{2}\frac{\omega_n}{\omega_z}
$$

$$
K=2\zeta\omega_n
$$

中文：Rhee 和 Yu 的 practical reminder 是：电路设计者很少只为“critical damping”而设计。真实 loop 会为了 spur、settling、noise、VCO gain variation、reference frequency、divider ratio 和 loop-filter realizability 有意选择 underdamped 或 overdamped behavior。实际 review 中，loop gain $K$ 往往比单独引用 $\omega_n$ 更接近 designer 调参的手柄。

English: Rhee and Yu's practical reminder is that circuit designers rarely design only for “critical damping.” Real loops intentionally choose underdamped or overdamped behavior to balance spur, settling, noise, VCO gain variation, reference frequency, divider ratio, and loop-filter realizability. In review, loop gain $K$ is often closer to the designer's control knob than $\omega_n$ alone.

### 28.4 CPPLL First-Pass Sizing

中文：charge-pump PLL 的有效 detector gain 通常写成 current-domain form：

English: The effective detector gain of a charge-pump PLL is usually written in current-domain form:

$$
K'_d=\frac{I_{CP}}{2\pi}
$$

中文：对基本 $R_1$-$C_1$ loop filter，open-loop transfer function 为：

English: For a basic $R_1$-$C_1$ loop filter, the open-loop transfer function is:

$$
G(s)=\frac{I_{CP}K_v(1+sR_1C_1)}{2\pi C_1s^2}
$$

中文：常用 first-pass parameters 为：

English: Common first-pass parameters are:

$$
\omega_u \approx \frac{I_{CP}R_1K_v}{2\pi}
$$

$$
\omega_z=\frac{1}{R_1C_1}
$$

$$
\omega_n=\sqrt{\frac{I_{CP}K_v}{2\pi C_1}}
$$

$$
\zeta=\frac{R_1}{2}\sqrt{\frac{I_{CP}C_1K_v}{2\pi}}
$$

中文：这些公式的使用边界必须明确。它们适合第一轮 sizing 和 design conversation，但不能替代 sampled-data analysis、transistor-level PFD/CP waveform、实际 $K_v$ 曲线、loop-filter parasitic、divider latency、VCO control-line ripple 和 PVT corner 验证。

English: The boundary of these equations must be explicit. They are appropriate for first-pass sizing and design conversation, but they do not replace sampled-data analysis, transistor-level PFD/CP waveforms, actual $K_v$ curves, loop-filter parasitics, divider latency, VCO control-line ripple, and PVT-corner verification.

### 28.5 Continuous-Time Approximation Boundary

中文：本书给出的一个 useful rule 是：当 loop bandwidth 小于 reference frequency 大约十分之一时，continuous-time approximation 通常适合作为 intuition 和 first-order design；若 bandwidth 更接近 reference update rate，就必须使用 sampled/discrete-time analysis。这个规则和 Hanumolu CPPLL paper 的 sampled-data caution 一致。

English: A useful rule from the book is that when loop bandwidth is below about one-tenth of the reference frequency, a continuous-time approximation is usually suitable for intuition and first-order design; if bandwidth approaches the reference update rate, sampled/discrete-time analysis is required. This is consistent with the sampled-data caution from the Hanumolu CPPLL paper.

中文：另一个 practical rule 是：若 loop delay 小于 loop time constant 大约五十分之一，delay 影响通常可以先忽略；否则 delay 会明显消耗 phase margin。对 high-speed SerDes PLL，divider、PFD reset、digital calibration path、DTC/TDC path 和 clock-distribution feedback path 都可能引入不可忽略 delay。

English: Another practical rule is that loop delay is often negligible if it is below about one-fiftieth of the loop time constant; otherwise it consumes phase margin. In high-speed SerDes PLLs, divider delay, PFD reset, digital calibration paths, DTC/TDC paths, and clock-distribution feedback can all introduce non-negligible delay.

### 28.5.1 Open-Loop Phase And Nyquist Construction

中文：求 open-loop phase 时，应把 transfer function 分解为 constant gain、integrator、real poles/zeros、complex pairs 和 explicit delay，再用相角相加；不能只看分母阶数猜 phase margin。对

English: To compute open-loop phase, factor the transfer function into constant gain, integrators, real poles and zeros, complex pairs, and explicit delay, then add their phase contributions. Phase margin should not be guessed from denominator order alone. For

$$
L(s)=\frac{K}{s\left(1+s/\omega_p\right)},\qquad K>0,
$$

有

we obtain

$$
\angle L(j\omega)=-90^\circ-\tan^{-1}\!\left(\frac{\omega}{\omega_p}\right).
$$

中文：其中 $\omega$、$\omega_p$ 的单位均为 rad/s。若 $\omega_u$ 是 $|L(j\omega_u)|=1$ 的 unity-gain frequency，标准负反馈且无额外符号反转时 $PM=180^\circ+\angle L(j\omega_u)$。实际计算应使用 `atan2` 或保持 quadrant 信息；单独相除后使用 principal-value `atan` 很容易丢失 $180^\circ$。

English: Here $\omega$ and $\omega_p$ are in rad/s. If $\omega_u$ is the unity-gain frequency where $|L(j\omega_u)|=1$, then for the standard negative-feedback sign convention with no extra inversion, $PM=180^\circ+\angle L(j\omega_u)$. Practical calculations should use `atan2` or otherwise preserve quadrant information; applying a principal-value arctangent after algebraic division can lose $180^\circ$.

中文：Nyquist trajectory 是把完整 Nyquist contour 上的每个 $s$ 映射为复数 $L(s)$，不是手绘一条“像 Bode 的曲线”。对正频率轴上的上述例子：

English: A Nyquist trajectory maps every $s$ on the complete Nyquist contour into the complex number $L(s)$; it is not a hand-drawn curve resembling a Bode plot. For the positive-frequency axis of the example above:

$$
\Re\{L(j\omega)\}=-\frac{K\omega_p}{\omega^2+\omega_p^2},\qquad
\Im\{L(j\omega)\}=-\frac{K\omega_p^2}{\omega(\omega^2+\omega_p^2)}.
$$

中文：以 $\omega>0$ 从低频扫到高频时，轨迹位于第三象限并趋向原点；real-coefficient system 的负频率分支是其共轭镜像。由于该例在原点有 open-loop pole，标准 Nyquist contour 必须绕开 $s=0$，不能把 positive-frequency branch 单独拿来数 $-1$ 绕行。最终应在明确 contour orientation 和 sign convention 后使用 argument principle，并把 open-loop 右半平面 poles、$-1$ encirclement 与 closed-loop 右半平面 poles 一起记录。

English: As $\omega>0$ sweeps from low to high frequency, the trajectory lies in the third quadrant and approaches the origin; the negative-frequency branch of a real-coefficient system is its complex-conjugate mirror. Because this example has an open-loop pole at the origin, the standard Nyquist contour must indent around $s=0$; the positive-frequency branch alone cannot be used to count encirclements of $-1$. The final argument-principle count must state contour orientation and sign convention and record open-loop right-half-plane poles, encirclements of $-1$, and closed-loop right-half-plane poles together.

### 28.6 Design Review Additions

中文：这本书把 PLL design review 的问题从“环路是否稳定”扩展成“哪些近似在这个设计中仍然成立”。review checklist 应明确列出 continuous-time approximation、sampled-data effects、loop delay、CP pulse shape、VCO gain range、divider ratio、loop-filter high-frequency poles 和 acquisition mode。

English: This book expands PLL design review from “is the loop stable” to “which approximations remain valid in this design.” A review checklist should explicitly include continuous-time approximation, sampled-data effects, loop delay, CP pulse shape, VCO gain range, divider ratio, loop-filter high-frequency poles, and acquisition mode.

| Review item | Deep-ingest question |
|---|---|
| Loop model | Are $K_d$, $K_v$, $F(s)$, divider ratio, and units defined consistently? |
| Loop approximation | Is loop bandwidth safely below reference update rate, or is sampled analysis required? |
| Delay | Is total loop delay small relative to loop time constant? |
| CPPLL sizing | Are $I_{CP}$, $R_1$, $C_1$, $C_2$, and $K_v$ checked across PVT? |
| Third-order pole | Does ripple suppression preserve phase margin and settling? |
| Acquisition | Is large-signal acquisition verified separately from small-signal tracking? |
| Architecture split | Are PFD/CP, fractional-N, DPLL, and CDR-specific effects routed to the right canonical notes? |

### 28.7 Source Provenance Added

| Source | Type | Status | Reusable knowledge promoted |
|---|---|---|---|
| Woogeun Rhee and Zhiping Yu, *Phase-Locked Loops: System Perspectives and Circuit Design Aspects*, Wiley/IEEE Press, 2024 | Book PDF | Deep Ingest 2026-07-05; archived in `90_Archive/processed/2026/books/phase_locked_loops_rhee_yu_2024/` | Linear PLL transfer functions, Type-I and Type-II loop dynamics, CPPLL first-pass sizing equations, continuous-time approximation boundary, loop-delay caution, system-to-circuit review workflow |
| ChatGPT delta `6a6e0313-043c-83ea-a96e-c98e23275cbc`, "开环传输函数相角" | Conversation-derived worked explanation | Deep Ingest 2026-08-08; source retained in the delta batch; verify sign/contour conventions against a control textbook before signoff use | Factor-by-factor open-loop phase, `atan2` caution, explicit Nyquist parameterization, pole-on-contour warning |

---

## Last Updated

2026-08-08
