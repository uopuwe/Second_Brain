---
title: "SerDes Power Integrity"
domain: "AnalogIC_SerDes"
tags:
  - SerDes
  - PowerIntegrity
  - LDO
  - PSRR
  - PLL
  - CDR
  - Jitter
  - SupplyNoise
  - PCIe7
  - Synopsys
created: 2026-07-01
updated: 2026-07-01
source: "ChatGPT technical notes and Synopsys role preparation"
status: "active"
---

# SerDes Power Integrity

## 中文补充翻译

这篇笔记说明 SerDes power integrity 为什么会直接影响 link margin。高速 SerDes 中，供电噪声不只是“电源质量”问题，它会通过两条主要路径伤害系统：一是变成 amplitude error，影响 RX front-end、ADC、reference、threshold 和 driver swing；二是变成 timing error，影响 PLL、VCO、clock buffer、PI、sampler 和 CDR。

在 PCIe 7.0 / PAM4 下，vertical eye margin 更小，timing UI 也很紧，因此同样的 supply ripple 比低速 NRZ 系统更危险。LDO 的作用是隔离外部 supply noise、提供局部低噪声供电、降低 block 间耦合，但 LDO 本身的 output noise、PSRR peaking、load transient、stability、dropout 和 layout parasitic 都可能成为问题。

这篇笔记的核心思路是把 supply noise 映射到实际 SerDes 错误：PLL jitter、clock buffer delay modulation、RX threshold error、ADC reference / aperture error、bandgap noise 和 correlated lane jitter。设计和验证时必须从 LDO-level、block-level 和 system-level 三层一起检查。

## Purpose

This note explains how power integrity affects high-speed SerDes performance.

The goal is to connect LDO, PSRR, supply noise, bandgap, bias, PLL, CDR, jitter, and eye margin into one system-level view.

This note is especially important for Synopsys preparation because the expected first-year work may involve PCIe 7.0 clocking and LDO.

---

## 1. Big Picture

In high-speed SerDes, power integrity is not just a support topic.

Supply noise can directly become:

* PLL phase noise
* clock jitter
* sampling uncertainty
* RX front-end noise
* ADC reference disturbance
* comparator threshold error
* eye closure
* BER degradation

Key chain:

```text
Power supply noise
↓
LDO finite PSRR / regulator noise
↓
Sensitive analog block disturbance
↓
PLL / clock / sampler / RX front-end modulation
↓
Timing or amplitude error
↓
Eye closure
↓
Higher BER / lower link margin
```

The core idea:

```text
In SerDes, bad power integrity becomes bad timing margin and bad voltage margin.
```

---

## 2. Why Power Integrity Matters More in PCIe 7.0 / PAM4

PCIe 7.0 uses very high data rate and PAM4 signaling.

PAM4 has four voltage levels, so the vertical distance between adjacent decision levels is much smaller than NRZ.

This means the receiver is more sensitive to:

* thermal noise
* supply noise
* reference noise
* offset
* gain error
* nonlinearity
* ISI
* jitter

Simplified view:

```text
NRZ:
2 levels
larger vertical eye
more noise margin

PAM4:
4 levels
smaller vertical eye
less noise margin
more sensitive to power and clock noise
```

Therefore, supply noise can hurt PAM4 links through both:

1. amplitude-domain error
2. timing-domain error

---

## 3. Two Main Error Paths

Power noise affects SerDes through two major paths.

## Path 1: Amplitude Error

Supply noise affects analog signal amplitude, reference, threshold, or front-end gain.

Examples:

```text
Supply noise
↓
RX front-end gain variation
↓
Decision threshold movement
↓
Vertical eye closure
```

or:

```text
Supply noise
↓
ADC reference disturbance
↓
Wrong digitized amplitude
↓
DSP / slicer error
```

Affected blocks:

* CTLE
* RX front-end
* sampler
* slicer
* ADC
* comparator
* reference ladder
* bias circuits
* TX driver

## Path 2: Timing Error

Supply noise modulates clock path delay or oscillator frequency.

Examples:

```text
Supply noise
↓
VCO frequency modulation
↓
PLL phase noise / jitter
↓
Sampling phase uncertainty
↓
Horizontal eye closure
```

or:

```text
Supply noise
↓
Clock buffer delay modulation
↓
Clock edge movement
↓
Sampling jitter
```

Affected blocks:

* PLL
* VCO / DCO
* clock divider
* clock buffer
* CDR
* sampler clock path
* TX clock path

---

## 4. LDO Role in SerDes

An LDO provides local regulated supply for sensitive analog and mixed-signal blocks.

In SerDes, LDOs may supply:

* PLL
* VCO / DCO
* CDR
* clock buffers
* RX front-end
* TX driver
* ADC
* bias circuits
* bandgap / reference
* calibration circuits

The LDO must provide:

* correct DC voltage
* low output noise
* high PSRR over relevant frequency range
* stability across PVT and load
* good transient response
* low coupling between blocks
* layout-friendly supply isolation

Key point:

```text
For SerDes, LDO performance should be judged by its impact on link margin, not only by standalone regulator metrics.
```

---

## 5. Important LDO Metrics for SerDes

## Output Noise

LDO output noise can directly disturb sensitive blocks.

Important questions:

* What is the integrated output noise?
* What frequency band matters for the powered block?
* Does noise hit the PLL / VCO sensitive band?
* Does noise affect RX front-end or ADC reference?

## PSRR

PSRR describes how much input supply noise is rejected by the LDO.

General definition:

```text
PSRR(dB) = 20 log10(ΔVin / ΔVout)
```

Higher PSRR means less input ripple appears at the output.

Important questions:

* What is PSRR at low frequency?
* What is PSRR at mid frequency?
* What is PSRR at high frequency?
* Where does PSRR start degrading?
* Is high-frequency supply noise bypassing the regulator through parasitics?

## Load Transient

SerDes blocks can have dynamic current changes.

Important questions:

* How much output droop occurs under load step?
* How fast does the LDO recover?
* Does transient response create clock jitter or reference error?
* Does load transient couple into nearby blocks?

## Stability

LDO stability must hold across:

* PVT
* load current
* output capacitor
* ESR
* package / routing parasitics
* different operating modes

Unstable or weakly stable LDOs can create peaking and ringing, which may be worse than simple DC error.

## Dropout

Dropout affects headroom and regulation.

In advanced nodes and low-voltage SerDes IP, limited voltage headroom can make LDO design much harder.

---

## 6. PSRR Frequency Regions

LDO PSRR usually behaves differently across frequency.

## Low Frequency

Dominated by:

* error amplifier gain
* feedback loop gain
* reference rejection

Usually PSRR can be strong if loop gain is high.

## Mid Frequency

Dominated by:

* loop bandwidth
* pass device behavior
* output pole
* internal compensation

PSRR may begin to degrade as loop gain rolls off.

## High Frequency

Dominated by:

* pass device parasitics
* gate-drain / drain-source coupling
* package parasitics
* layout coupling
* output decoupling capacitor
* local routing impedance

At high frequency, the LDO loop may no longer help much.

Key reminder:

```text
High-frequency PSRR often depends more on parasitics and decap strategy than on ideal loop gain.
```

---

## 7. Supply Noise to PLL Jitter

PLL / VCO is one of the most power-sensitive blocks in SerDes.

If VCO frequency depends on supply voltage:

```text
KVDD = Δf / ΔVDD
```

Then supply ripple creates frequency modulation.

Chain:

```text
Supply ripple
↓
VCO frequency variation
↓
Phase modulation
↓
PLL output jitter
↓
Sampling clock uncertainty
↓
Eye closure
```

Important questions:

* What is the VCO supply sensitivity?
* What is the supply noise spectrum?
* Which offset frequencies matter?
* How much of the supply noise passes through the LDO?
* Does the PLL loop suppress or pass the resulting phase noise?
* Does the CDR track or reject the jitter?

---

## 8. Supply Noise to Clock Buffer Jitter

Even if the VCO is clean, clock buffers can convert supply noise into edge timing error.

Mechanism:

```text
Supply voltage changes
↓
Buffer delay changes
↓
Clock edge shifts
↓
Jitter appears at sampler or TX
```

This is especially dangerous because clock distribution can contain many buffers.

Important questions:

* What is delay sensitivity to supply?
* Are clock buffers powered by quiet supplies?
* Are clock buffers isolated from noisy digital blocks?
* Is local decoupling placed close enough?
* Does the clock distribution share supply with switching logic?

---

## 9. Supply Noise to RX Front-End Error

RX analog front-end is sensitive to supply and bias noise.

Supply noise can change:

* CTLE gain
* CTLE pole / zero location
* comparator threshold
* sampler offset
* bias current
* input common-mode
* ADC reference
* ADC comparator delay

Chain:

```text
Supply noise
↓
RX analog parameter variation
↓
Amplitude error / threshold error
↓
Vertical eye closure
↓
Symbol error
```

For PAM4, this matters strongly because the vertical eye is small.

---

## 10. Supply Noise to ADC-Based RX

ADC-based PAM4 receivers are especially sensitive to power integrity.

Affected ADC aspects:

* sampling aperture
* comparator noise
* comparator delay
* reference ladder
* capacitor DAC reference
* clock path
* time-interleaving skew
* offset / gain calibration stability

Possible error chain:

```text
Supply noise
↓
ADC reference movement
↓
Digitized PAM4 level error
↓
DSP equalization error
↓
Symbol decision error
```

Another chain:

```text
Supply noise
↓
Sampling clock buffer delay modulation
↓
Sampling jitter
↓
SNDR degradation
↓
Worse RX margin
```

Important questions:

* Is the ADC reference generated locally?
* Is the ADC supply separated from digital DSP supply?
* Does calibration track supply-induced drift?
* How much supply noise is tolerable before ENOB / EVM degrades?

---

## 11. Bandgap / Reference Relevance

Bandgap and reference circuits are foundational for SerDes analog IP.

They may provide:

* LDO reference
* bias reference
* ADC reference
* comparator threshold reference
* common-mode reference
* calibration reference

Reference noise or drift can affect many blocks at once.

Important concerns:

* reference noise
* supply sensitivity
* temperature drift
* startup reliability
* mismatch
* layout gradient
* coupling from digital noise
* reference distribution

Key point:

```text
A noisy reference can quietly contaminate many blocks at once.
```

This is why bandgap / reference design should be treated as part of system noise planning, not as a boring utility block exiled to the corner of the chip.

---

## 12. Decoupling Strategy

Decoupling capacitors reduce local supply impedance.

They help provide fast transient current and shunt high-frequency noise.

Important concepts:

* local decap close to sensitive blocks
* distributed decap network
* package inductance
* routing resistance
* resonance
* anti-resonance
* supply impedance target
* frequency-dependent effectiveness

Simple view:

```text
LDO handles low / mid frequency noise.
Decap handles high-frequency local transient noise.
Package and layout determine what actually happens.
```

Important warning:

```text
Adding decap blindly is not a strategy.
```

Decap placement, parasitic inductance, resonance, and supply grid impedance matter. Otherwise it becomes decorative silicon furniture.

---

## 13. Isolation Between Blocks

SerDes contains both noisy and sensitive blocks.

Noisy blocks:

* digital logic
* DSP
* serializers / deserializers
* large clock dividers
* TX drivers
* calibration engines

Sensitive blocks:

* PLL / VCO
* CDR
* RX front-end
* ADC
* references
* bias circuits
* samplers

Isolation techniques:

* separate LDOs
* separate supply domains
* guard rings
* deep n-well isolation
* local decap
* careful floorplanning
* differential routing
* shielding
* quiet reference routing
* avoiding shared high-current return paths

Key question:

```text
Which noisy blocks share impedance with which sensitive blocks?
```

Shared impedance is often where the villain hides.

---

## 14. Simulation Checklist

For SerDes power integrity, useful simulations include:

## LDO-Level

* DC regulation
* line regulation
* load regulation
* load transient
* line transient
* PSRR vs frequency
* output noise
* stability / phase margin
* PVT corners
* Monte Carlo
* dropout behavior

## Block-Level

* PLL phase noise with supply noise
* VCO supply pushing
* clock buffer supply sensitivity
* sampler jitter from supply disturbance
* ADC SNDR / ENOB under supply ripple
* RX front-end gain / offset under supply variation

## System-Level

* eye diagram under supply noise
* bathtub curve
* jitter budget
* link margin
* BER / SER degradation
* power supply noise injection
* aggressor-victim coupling

---

## 15. Measurement / Debug Checklist

If silicon or lab data shows SerDes margin issue, power integrity should be checked.

Questions:

* Is there supply ripple at relevant frequency?
* Does jitter correlate with supply ripple?
* Does eye margin improve with cleaner lab supply?
* Does changing decap change the issue?
* Does changing LDO load affect PLL jitter?
* Does enabling digital blocks degrade RX margin?
* Does the problem depend on data pattern?
* Does the problem depend on temperature or voltage?
* Is the issue worse at certain frequencies?
* Is the same supply shared by noisy and sensitive blocks?

Possible debug flow:

```text
Observe eye / BER issue
↓
Check clock jitter
↓
Check PLL phase noise
↓
Check supply ripple
↓
Inject controlled supply noise
↓
Measure sensitivity
↓
Identify coupling path
↓
Improve LDO / decap / layout / isolation
```

---

## 16. Interview Explanation

Short explanation:

```text
In high-speed SerDes, power integrity directly affects timing and amplitude margin. Supply noise can pass through finite LDO PSRR, modulate VCO frequency or clock buffer delay, and become sampling jitter. It can also disturb RX front-end gain, comparator thresholds, ADC references, and bias currents, causing vertical eye closure. For PAM4 links like PCIe 7.0, the margin is smaller, so LDO noise, PSRR, decap strategy, and supply isolation are tightly connected to BER and link reliability.
```

Synopsys-focused explanation:

```text
For PCIe 7.0 clocking and LDO work, I should treat LDO design as part of the SerDes performance path. The LDO is not just generating a regulated voltage. It controls how much external supply noise reaches PLL, clock buffers, RX front-end, and ADC-related blocks. Its PSRR, output noise, transient response, and stability can affect jitter, eye opening, and link margin.
```

Senior-level explanation:

```text
The key is to translate LDO metrics into SerDes-level impact. For example, finite PSRR allows supply ripple to reach the VCO or clock buffer, where it can convert into phase modulation or delay modulation. That creates timing jitter, which reduces horizontal eye margin. Similarly, reference and bias noise can disturb RX amplitude decisions, causing vertical eye closure. So the right design question is not only whether the LDO is stable or low-noise, but whether the remaining supply disturbance is acceptable for the SerDes jitter and noise budget.
```

---

## 17. Common Interview Questions

## Q1: Why does LDO matter in SerDes?

Because LDO output noise, finite PSRR, and transient response affect sensitive blocks such as PLL, CDR, clock buffers, RX front-end, ADC, bias, and reference circuits. These errors can degrade jitter, eye margin, and BER.

## Q2: How does supply noise become jitter?

Supply noise can modulate VCO frequency or clock buffer delay. VCO supply modulation creates phase modulation. Clock buffer delay modulation moves clock edges. Both appear as timing jitter.

## Q3: What PSRR frequency range matters most?

It depends on the powered block and noise sensitivity. Low-frequency PSRR is controlled by loop gain, while high-frequency rejection often depends on parasitics, decap, and layout. For PLL / VCO, supply noise at offset frequencies that convert into phase noise is especially important.

## Q4: Why is PAM4 more sensitive to power noise?

PAM4 has smaller vertical eye openings than NRZ. Supply-induced amplitude error, threshold movement, or reference noise consumes a larger portion of the available margin.

## Q5: How do you debug supply-induced SerDes jitter?

Check whether jitter or BER correlates with supply ripple. Inject controlled supply noise, measure PLL phase noise or recovered clock jitter, change decap or supply filtering, and isolate noisy blocks from sensitive supplies.

## Q6: What is the difference between LDO output noise and PSRR?

Output noise is noise generated by the LDO itself and its reference / amplifier / pass device. PSRR is rejection of input supply noise. Both contribute to the final supply noise seen by the load.

## Q7: Why can high-frequency PSRR be poor?

At high frequency, loop gain is low and parasitic coupling through the pass device, layout, package, and substrate can dominate. Decap and layout become critical.

## Q8: How can bandgap noise affect SerDes?

Bandgap noise can propagate through LDO references, bias currents, ADC references, and thresholds. Since many blocks depend on shared references, one noisy reference can affect multiple sensitive paths.

## Q9: Why can decap create problems?

Decap has parasitic resistance and inductance. Poorly planned decap networks can create resonance or anti-resonance, causing supply impedance peaks at problematic frequencies.

## Q10: What makes this a system-level issue?

Because power noise may start at the supply, pass through LDO and layout, modulate PLL or RX circuits, and finally show up as eye closure or BER degradation. The root cause is electrical, but the failure is system-level.

---

## 18. Design Checklist

When reviewing an LDO for SerDes use, check:

* Which block does it power?
* What is the block's noise sensitivity?
* What is the required output noise?
* What is the PSRR target and frequency range?
* What is the load current profile?
* What is the load transient condition?
* What output decap is available?
* Is the LDO stable across all corners?
* Is dropout acceptable?
* Is the reference clean enough?
* Is the supply routing isolated?
* Are noisy digital blocks sharing the same supply?
* Is local decap close to the load?
* Is substrate / package coupling considered?
* Is there a way to verify supply-induced jitter?

---

## 19. Personal Connection to My Experience

This topic connects strongly to my previous LDO and analog IP experience.

Relevant experience areas:

* LDO design
* PSRR analysis
* stability analysis
* load transient
* line transient
* bandgap / reference
* POR / BOR
* analog IP integration
* PVT and Monte Carlo simulation
* layout-sensitive analog design

How to present it for Synopsys:

```text
My LDO experience is directly relevant to SerDes because local regulators are not just power delivery blocks. Their noise, PSRR, stability, and transient response can affect PLL jitter, clock quality, RX front-end performance, and ultimately PCIe link margin. I want to connect my prior LDO experience with PCIe 7.0 clocking and SerDes power integrity requirements.
```

---

## 20. Open Questions

* 待确认: Which Synopsys PCIe 7.0 blocks use local LDOs?
* 待确认: Are PLL and clock buffers powered by dedicated regulators?
* 待确认: What PSRR requirement is used for the PLL supply?
* 待确认: What output noise budget is allocated to each LDO?
* 待确认: How is supply-induced jitter simulated?
* 待确认: Are supply ripple injection simulations part of signoff?
* 待确认: How is decap planned between analog and digital regions?
* 待确认: How much supply isolation exists between PLL, RX, TX, and DSP?
* 待确认: What are the most common silicon issues related to SerDes power integrity?
* 待确认: How does Synopsys model package / board supply noise?

---

## Source Conversations / Source Packets

* `../../00_Inbox/manual_batches/batch2_serdes_pcie_pll_cdr_adc_2026-07-01/source_packet.md`

---

## 21. Related Notes

* `../analog_ic_serdes_master_index.md`
* `../SerDes/pcie7_overview.md`
* `../SerDes/serdes_architecture_overview.md`
* `../SerDes/pam4_receiver_basics.md`
* `../PLL_CDR_Clocking/pll_phase_noise_jitter.md`
* `../PLL_CDR_Clocking/pcie7_clocking_notes.md`
* `../ADC/adc_based_receiver.md`
* `../ADC/sampling_jitter_adc.md`
* `ldo_fundamentals.md`
* `ldo_psrr_notes.md`
* `ldo_stability_notes.md`
* `bandgap_reference_notes.md`
* `../Interview_QA/synopsys_relevant_qa.md`
* `../Study_Plans/synopsys_4_week_prep_plan.md`
* `../../02_Synopsys_Work/synopsys_master_note.md`
* `../../02_Synopsys_Work/onboarding_plan.md`

---

## 22. Next Actions

1. Create `ldo_psrr_notes.md`.
2. Create `ldo_stability_notes.md`.
3. Create `bandgap_reference_notes.md`.
4. Add real diagrams and equations later.
5. Add specific Synopsys internal requirements after joining.
6. Link this note to onboarding questions.

---

## 23. Batch 1 Extracted Knowledge - 2026-07-02

### 23.1 LDO-to-Clock-Jitter Chain

For SerDes clocking, the LDO requirement should be traced through the clock path:

```text
LDO output noise / ripple
-> local PDN impedance and package resonance
-> VCO / divider / PI / clock-buffer supply modulation
-> phase noise, deterministic jitter, duty-cycle distortion, or skew
-> TX launch / RX sampler timing error
-> PAM4 eye margin and BER
```

Design implication: PSRR at one frequency is not enough. The relevant frequency band is set by supply-noise spectrum, PLL/CDR transfer behavior, VCO/clock-buffer supply sensitivity, and PDN resonances.

### 23.2 Supply Ripple Budget From Jitter Budget

For a sensitive clock block:

```text
Delta f = K_VDD * v_supply
Delta phi_pk = K_VDD * V_ripple_pk / f_ripple
Delta t_pk = Delta phi_pk / (2*pi*f_clk)
```

Use this to back-calculate the allowed ripple after assigning a jitter budget to the block. Then verify with supply-ripple injection in Spectre, not only with small-signal PSRR.

### 23.3 Domain Partitioning Questions

- Put VCO supplies, divider supplies, PI / phase-rotator supplies, clock-buffer supplies, sampler supplies, and digital supplies into separate analysis buckets.
- Local LDOs reduce low/mid-frequency supply coupling but can interact with package inductance and on-die decap.
- Clock-buffer simultaneous switching current can turn supply impedance into deterministic jitter or duty-cycle distortion.
- ADC sampler supplies connect power integrity directly to aperture jitter and kickback sensitivity.

### 23.4 EMIR Reminders

- EM uses long-term current density and heating risk.
- Static IR uses average current drop.
- Dynamic IR uses transient switching current and local droop.
- Supply-noise-to-jitter analysis needs both amplitude and spectrum, especially near PLL/CDR-sensitive bands.

### 23.5 Synopsys Onboarding Questions

- 待确认: Which clock domains have dedicated local LDOs versus shared analog supplies?
- 待确认: What supply-noise injection amplitude and frequency grid is used for jitter signoff?
- 待确认: Are VCO, divider, PI, clock buffer, and sampler `K_VDD` or PSIJ metrics maintained as internal specs?
- 待确认: How are package / board impedance and on-die decap included in SerDes jitter budgeting?

### 23.6 Source Conversations

- `../../00_Inbox/raw_chat_exports/chatgpt_export_2026-07-01/md_by_conversation/2026-06-06__PCIe7_Clocking_LDO学习计划.md`
- `../../00_Inbox/raw_chat_exports/chatgpt_export_2026-07-01/md_by_conversation/2026-04-21__GF_22FDX_CPPLL设计.md`

---

## Last Updated

2026-07-02
