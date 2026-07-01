---

title: "LDO PSRR Notes"
domain: "AnalogIC_SerDes"
tags:

* LDO
* PSRR
* PowerIntegrity
* SerDes
* PLL
* CDR
* Jitter
* SupplyNoise
* Synopsys
  created: 2026-07-01
  updated: 2026-07-01
  source: "ChatGPT technical notes and Synopsys role preparation"
  status: "active"

---

# LDO PSRR Notes

## 中文补充翻译

这篇笔记从 analog IC 和 SerDes power integrity 角度解释 LDO PSRR。PSRR 描述输入 supply ripple 被 LDO 抑制后，有多少会出现在 regulated output。PSRR 越高，传到负载的 ripple 越小，但 PSRR 是频率相关的 transfer function，不是一个固定 DC 数字。

在 SerDes 中，LDO 输出 ripple 可能扰动 PLL/VCO、clock buffer、CDR、RX front-end、ADC、reference 和 bias。低频 PSRR 主要依赖 loop gain 和 reference；中频受 loop bandwidth、error amplifier、pass device 和 compensation 影响；高频时 loop gain 下降，寄生 feedthrough、package、decap 和 layout path 往往决定真实抑制能力。

设计 review 中要问：PSRR 在哪个频率测量、负载电流是多少、是否接近 dropout、输出电容和 decap 如何、reference noise 是否被包含、是否有 PSRR peaking、以及 supply ripple 如何转换为 jitter 或 amplitude error。

## Purpose

This note summarizes LDO PSRR from the perspective of analog IC design and SerDes power integrity.

The goal is to understand how LDO power-supply rejection affects sensitive blocks such as PLL, VCO, CDR, clock buffers, RX front-end, ADC, reference, and bias circuits.

This note supports Synopsys preparation, especially for PCIe 7.0 clocking and LDO-related work.

---

## 1. Big Picture

PSRR means power supply rejection ratio.

For an LDO, PSRR describes how much input supply ripple is rejected before it appears at the regulated output.

Basic definition:

```text
PSRR(dB) = 20 log10(ΔVin / ΔVout)
```

Higher PSRR means less input ripple reaches the load.

Key chain in SerDes:

```text
External supply ripple
↓
Finite LDO PSRR
↓
Residual LDO output ripple
↓
PLL / clock buffer / RX front-end disturbance
↓
Jitter or amplitude error
↓
Eye closure
↓
Worse BER / link margin
```

Important idea:

```text
In high-speed SerDes, PSRR is not just an LDO spec.
It is part of the jitter and noise budget.
```

---

## 2. Why PSRR Matters in SerDes

SerDes circuits are sensitive to supply noise because they contain:

* PLL
* VCO / DCO
* CDR
* clock buffers
* high-speed samplers
* CTLE
* RX front-end
* TX driver
* ADC
* comparator
* bias circuits
* bandgap / references

Supply ripple can become:

* clock jitter
* VCO phase noise
* clock buffer delay modulation
* comparator threshold shift
* RX gain variation
* ADC reference movement
* bias current variation
* vertical eye closure
* horizontal eye closure

For PAM4, this is worse because the vertical eye opening is smaller than NRZ.

---

## 3. PSRR Definition

A small ripple on the LDO input creates a smaller ripple on the LDO output.

```text
Vin = Vin_DC + vin_ripple
Vout = Vout_DC + vout_ripple
```

PSRR is:

```text
PSRR = vin_ripple / vout_ripple
```

In dB:

```text
PSRR(dB) = 20 log10(vin_ripple / vout_ripple)
```

Example:

```text
If input ripple = 100 mV
and output ripple = 1 mV

PSRR = 100
PSRR(dB) = 40 dB
```

This means the LDO attenuates supply ripple by 40 dB at that frequency.

Important warning:

```text
PSRR is frequency-dependent.
```

A single PSRR number without frequency is incomplete.

Bad statement:

```text
The LDO PSRR is 60 dB.
```

Better statement:

```text
The LDO PSRR is 60 dB at 100 kHz and 35 dB at 10 MHz under 100 mA load.
```

Because apparently numbers need conditions. A shocking concept, except to anyone who has survived a real design review.

---

## 4. Frequency Dependence of PSRR

LDO PSRR changes strongly with frequency.

A useful mental model:

```text
Low frequency:
mainly controlled by loop gain

Mid frequency:
controlled by loop bandwidth, poles, zeros, pass device behavior

High frequency:
controlled by parasitic coupling, output capacitor, decap, layout, package
```

---

## 5. Low-Frequency PSRR

At low frequency, the LDO feedback loop has high gain.

The error amplifier senses output variation and corrects the pass device.

Dominant factors:

* error amplifier DC gain
* feedback factor
* pass device transconductance
* reference rejection
* loop gain

Higher loop gain generally improves low-frequency PSRR.

Simplified idea:

```text
High loop gain
↓
strong correction
↓
better low-frequency PSRR
```

Low-frequency PSRR can be degraded by:

* low amplifier gain
* poor reference PSRR
* feedback resistor coupling
* limited pass device gain
* dropout operation
* insufficient headroom
* large load current reducing loop gain

---

## 6. Mid-Frequency PSRR

At mid frequency, the LDO loop gain starts rolling off.

This region is often determined by:

* dominant pole
* output pole
* error amplifier bandwidth
* pass device pole
* compensation network
* output capacitor
* ESR zero
* load current

PSRR usually gets worse as frequency increases because the loop can no longer correct supply disturbance quickly enough.

Important tradeoff:

```text
Higher bandwidth can improve PSRR over a wider range,
but may create stability problems.
```

This is classic analog design: improve one thing, awaken three demons.

---

## 7. High-Frequency PSRR

At high frequency, feedback loop gain is low.

The LDO cannot actively reject fast supply ripple well.

High-frequency PSRR is often dominated by:

* pass device parasitic capacitance
* drain-to-source coupling
* gate-to-drain coupling
* substrate coupling
* package inductance
* layout coupling
* output decoupling capacitor
* local supply grid impedance
* bondwire / bump / package parasitics

Important idea:

```text
High-frequency PSRR is often a layout and parasitic problem,
not just an amplifier gain problem.
```

At high frequency, output decap and layout become critical.

---

## 8. LDO PSRR and Pass Device Type

LDO PSRR depends strongly on pass device architecture.

## PMOS Pass LDO

Common features:

* simple gate drive
* low dropout possible
* input ripple can couple through parasitic capacitances
* high-frequency PSRR may be limited by pass device feedthrough

## NMOS Pass LDO

Common features:

* may need charge pump or higher gate voltage
* can have good current capability
* dropout depends on gate drive
* different PSRR behavior due to source follower nature

## Source Follower Regulator

Common features:

* fast
* potentially good high-frequency behavior
* limited DC accuracy depending on loop
* headroom-sensitive

Design implication:

```text
There is no universal PSRR behavior.
The pass device, loop architecture, load, capacitor, and layout all matter.
```

---

## 9. Dropout Effect on PSRR

PSRR usually becomes worse when the LDO approaches dropout.

Why?

In dropout, the pass device has less voltage headroom and less ability to regulate.

The pass device may move toward triode operation or reduced gain condition.

Result:

```text
Less headroom
↓
weaker regulation
↓
lower PSRR
↓
more input ripple appears at output
```

Important for low-voltage advanced nodes:

```text
Small voltage headroom makes high PSRR harder.
```

This matters in SerDes because analog supplies may be low, but jitter and noise requirements remain brutal. Naturally, physics shows no sympathy.

---

## 10. Load Current Effect on PSRR

PSRR depends on load current.

Changing load current changes:

* output pole
* pass device operating point
* transconductance
* output resistance
* loop gain
* phase margin
* dropout margin
* thermal behavior

At heavy load:

* pass device headroom may reduce
* loop gain may change
* output pole shifts
* transient response becomes more demanding

At light load:

* output pole may move
* stability can degrade
* some architectures enter low-power mode
* PSRR can change significantly

Important note:

```text
PSRR must be checked across load current range,
not only at a typical current.
```

---

## 11. Output Capacitor and Decap Effect

Output capacitor affects PSRR in multiple ways.

It can:

* reduce output ripple
* create output pole
* introduce ESR zero
* improve high-frequency filtering
* affect loop stability
* interact with package / routing inductance

At high frequency, local decap can be more important than loop action.

But decap is not magic dust.

Bad approach:

```text
PSRR is poor, add huge cap.
```

Better approach:

```text
Analyze supply impedance, resonance, loop stability, decap placement, and parasitics.
```

Because blindly adding capacitance is how engineers turn silicon into expensive superstition.

---

## 12. Reference PSRR

The LDO output depends on its reference.

If the reference is noisy or supply-sensitive, the LDO output can still be noisy even if the loop rejects input ripple well.

Reference path:

```text
Supply noise
↓
Bandgap / reference disturbance
↓
Error amplifier input disturbance
↓
Pass device correction in wrong direction
↓
Output noise / ripple
```

Important questions:

* What is bandgap PSRR?
* What is reference noise?
* Is reference filtered?
* Is reference shared by many blocks?
* Does digital noise couple into reference routing?
* Is reference buffer stable and low noise?

Key idea:

```text
The LDO cannot produce a clean output from a dirty reference.
```

A regulator with a contaminated reference is just a well-dressed noise distributor.

---

## 13. Error Amplifier Contribution

The error amplifier affects PSRR through:

* DC gain
* bandwidth
* input-referred noise
* output swing
* slew rate
* PSRR of the amplifier itself
* offset
* stability compensation

The amplifier must reject supply noise on its own rails.

If the error amplifier supply is noisy, the gate control of the pass device can be disturbed.

This can create output ripple even if input-to-output pass device coupling is not dominant.

---

## 14. Feedthrough Path

A major high-frequency PSRR limitation is direct feedthrough from input to output through the pass device.

For a PMOS pass device, input ripple can couple through parasitic capacitances.

Simplified feedthrough path:

```text
Input supply ripple
↓
Pass device parasitic capacitance
↓
Output node
↓
Load supply ripple
```

At high frequency, this path can bypass the feedback loop.

This explains why PSRR may degrade sharply at high frequency.

---

## 15. PSRR and PLL / VCO

PLL and VCO are among the most PSRR-sensitive loads.

Supply ripple at the VCO can modulate oscillation frequency.

If VCO frequency changes with supply:

```text
KVDD = Δf / ΔVDD
```

Then residual LDO output ripple creates frequency modulation.

Chain:

```text
LDO output ripple
↓
VCO supply modulation
↓
frequency modulation
↓
phase modulation
↓
clock jitter
↓
horizontal eye closure
```

Important questions:

* What is VCO supply sensitivity?
* Which supply frequencies create the most phase noise?
* What is the PLL loop bandwidth?
* Does the PLL suppress this noise or pass it?
* What is the integrated jitter contribution?
* Is the LDO PSRR sufficient at the relevant offset frequencies?

---

## 16. PSRR and Clock Buffers

Clock buffers also convert supply noise into jitter.

Mechanism:

```text
Supply noise
↓
buffer delay variation
↓
clock edge timing movement
↓
jitter
```

Clock buffer sensitivity is often described as delay sensitivity to supply.

Important questions:

* How much delay changes per mV of supply noise?
* Are buffers powered by a quiet local LDO?
* Are clock buffers isolated from digital switching supply?
* Is local decap close enough?
* Does supply noise correlate with clock jitter?

Even if the PLL is clean, dirty clock distribution can still ruin the sampling clock. Very democratic of the circuit: everyone gets a chance to destroy the margin.

---

## 17. PSRR and RX Front-End

RX front-end supply noise can affect:

* CTLE gain
* CTLE pole / zero location
* sampler offset
* comparator threshold
* input common-mode
* bias currents
* ADC reference
* decision levels

For PAM4:

```text
Supply-induced amplitude error
↓
vertical eye closure
↓
symbol decision error
```

Since PAM4 has smaller vertical spacing between levels, front-end supply noise is more dangerous than in NRZ.

---

## 18. PSRR Measurement / Simulation Setup

Typical PSRR simulation:

```text
Apply small AC ripple at LDO input
Measure AC ripple at LDO output
Sweep frequency
Compute 20log10(Vin_ripple / Vout_ripple)
```

Simulation setup:

```text
Vin = DC supply + AC 1 V small-signal source
Vout = regulated output
Load = representative current / impedance
Sweep frequency
Plot PSRR vs frequency
```

Important conditions to record:

* input voltage
* output voltage
* load current
* output capacitor
* ESR
* process corner
* temperature
* dropout margin
* operating mode
* decap configuration
* whether reference supply is ideal or realistic
* whether layout parasitics are included

Bad PSRR result note:

```text
PSRR is 50 dB.
```

Good PSRR result note:

```text
PSRR is 50 dB at 1 MHz and 28 dB at 100 MHz under TT, 25°C, Vin = 1.2 V, Vout = 0.9 V, Iload = 100 mA, Cout = 100 pF, post-layout extracted.
```

---

## 19. PSRR in Transient Simulation

AC PSRR is useful but not sufficient.

Transient simulations are also needed.

Useful transient tests:

* sinusoidal ripple injection at input
* square-wave supply disturbance
* load current step
* digital switching noise profile
* multi-tone supply noise
* package / board supply ripple
* supply droop during activity burst

Observe:

* output ripple
* settling time
* ringing
* PLL phase disturbance
* clock jitter
* RX eye degradation
* ADC SNDR degradation
* comparator threshold movement

Key idea:

```text
AC PSRR shows small-signal rejection.
Transient simulation shows real operating disturbance.
```

Both matter. Picking one and pretending the other does not exist is how lab surprises are born.

---

## 20. Layout Impact on PSRR

Layout can make or break PSRR.

Important layout factors:

* input-output coupling
* pass device placement
* reference routing
* ground routing
* substrate noise
* guard rings
* well isolation
* decap placement
* current return path
* supply grid impedance
* noisy digital proximity
* clock routing proximity
* matching of feedback resistors
* Kelvin sensing if needed

Common layout problems:

* input supply routed too close to output sense node
* noisy digital supply sharing return path with analog LDO
* reference line routed near switching clocks
* output decap too far from load
* feedback node exposed to coupling
* insufficient isolation around VCO supply
* long high-current path creating IR drop and bounce

---

## 21. PSRR Design Improvement Methods

Possible methods:

## Improve Loop Gain

* increase error amplifier gain
* optimize pass device gm
* improve feedback loop design

Useful mostly at low / mid frequencies.

## Increase Loop Bandwidth

* extend correction range
* improve mid-frequency rejection

But watch stability.

## Improve Reference Filtering

* low-noise bandgap
* RC filter
* reference buffer
* isolated reference routing

## Improve High-Frequency Filtering

* local decap
* better decap placement
* reduce parasitic inductance
* optimize supply grid
* reduce pass-device feedthrough

## Improve Isolation

* separate analog and digital supplies
* dedicated LDO for PLL / VCO
* guard rings
* deep n-well
* careful floorplan

## Reduce Load Sensitivity

* local decap near load
* faster transient response
* better load regulation
* reduce shared impedance

---

## 22. PSRR Tradeoffs

Improving PSRR can trade off with:

* stability
* output noise
* quiescent current
* dropout voltage
* area
* output capacitance
* transient response
* startup time
* design complexity

Examples:

```text
Higher loop bandwidth
↓
better mid-frequency PSRR
↓
possible stability risk
```

```text
More filtering
↓
lower noise
↓
slower startup or larger area
```

```text
More decap
↓
better high-frequency supply impedance
↓
more area and possible resonance issues
```

There is no free lunch. Analog design is mostly paying for lunch with different organs.

---

## 23. PSRR Checklist for SerDes LDO

When reviewing an LDO for SerDes, ask:

* Which block does this LDO power?
* Is the load PLL, VCO, CDR, RX, ADC, TX, or bias?
* What is the load's noise sensitivity?
* What PSRR is required at each frequency?
* What is the supply noise spectrum?
* What is the LDO output noise?
* What is the dropout margin?
* What is the load current range?
* What are the transient current profiles?
* What output capacitor is available?
* Is the LDO stable across PVT and load?
* Is reference noise included?
* Is post-layout extraction included?
* Is package / board parasitic included?
* Does supply-induced jitter meet the system budget?
* Are noisy and sensitive blocks isolated?

---

## 24. Interview Explanation

Short explanation:

```text
LDO PSRR is the ability of the regulator to reject input supply ripple before it reaches the output. It is frequency-dependent. At low frequency, PSRR is mainly determined by loop gain. At mid frequency, loop bandwidth, poles, zeros, pass device behavior, and output capacitor matter. At high frequency, loop gain is low, so parasitic feedthrough, layout, package, and decap dominate. In SerDes, LDO PSRR matters because residual supply ripple can modulate PLL / VCO frequency, clock buffer delay, RX front-end gain, or ADC reference, creating jitter and eye closure.
```

Synopsys-focused explanation:

```text
For PCIe 7.0 clocking and LDO work, I would not evaluate PSRR as an isolated regulator curve. I would connect the PSRR curve to the sensitive load. For example, if the LDO powers a VCO, the important question is how much residual supply ripple remains at offset frequencies that convert into VCO phase noise and integrated jitter. If it powers RX front-end or ADC reference, the key question is how supply ripple affects vertical eye margin or SNDR.
```

Senior-level explanation:

```text
The most important point is to translate LDO PSRR into system impact. PSRR tells us how much input supply ripple reaches the load, but whether that matters depends on the load sensitivity. For a PLL, residual ripple can become phase modulation through VCO supply pushing. For clock buffers, it can become delay modulation. For a PAM4 receiver, it can disturb thresholds, gain, or ADC reference. So PSRR has to be analyzed together with supply noise spectrum, load sensitivity, LDO output noise, decap, layout parasitics, and the SerDes jitter / noise budget.
```

---

## 25. Common Interview Questions

## Q1: What is PSRR?

PSRR is power supply rejection ratio. For an LDO, it describes how much input supply ripple is rejected before appearing at the output.

## Q2: Why is PSRR frequency-dependent?

Because the feedback loop, pass device, output capacitor, parasitics, and layout all have frequency-dependent behavior. Low-frequency PSRR is mainly loop-gain dominated, while high-frequency PSRR is often parasitic and decap dominated.

## Q3: What determines low-frequency PSRR?

Mainly error amplifier gain, feedback loop gain, reference rejection, pass device gain, and operating headroom.

## Q4: Why does high-frequency PSRR degrade?

At high frequency, loop gain is low, and direct feedthrough through pass device parasitics, layout coupling, package parasitics, and finite decap effectiveness dominate.

## Q5: How does dropout affect PSRR?

Near dropout, the pass device loses regulation headroom. Its gain and ability to reject input ripple are reduced, so PSRR degrades.

## Q6: How does load current affect PSRR?

Load current changes the pass device operating point, loop gain, output pole, dropout margin, and stability. Therefore PSRR must be checked across load range.

## Q7: How can LDO PSRR affect PLL jitter?

Residual LDO output ripple can modulate VCO frequency through supply pushing. This creates phase modulation and timing jitter.

## Q8: What is the difference between LDO output noise and PSRR?

Output noise is noise generated internally by the LDO and its reference / amplifier / pass device. PSRR describes rejection of input supply noise. Both affect the final supply noise seen by the load.

## Q9: How do you simulate PSRR?

Apply a small AC ripple at the LDO input, measure output ripple, sweep frequency, and compute `20log10(Vin_ripple / Vout_ripple)`. Repeat across PVT, load, dropout, output capacitor, and layout conditions.

## Q10: How do you improve PSRR?

Improve loop gain, optimize loop bandwidth, reduce pass-device feedthrough, improve reference filtering, add well-placed decap, isolate sensitive blocks, and optimize layout / supply routing.

---

## 26. Personal Connection to My Experience

This note connects directly to my previous LDO experience.

Relevant background:

* LDO design
* PSRR simulation
* load transient
* line transient
* stability
* PVT corners
* Monte Carlo
* bandgap / reference
* POR / BOR
* analog IP integration
* layout-sensitive design

How to present this experience:

```text
My LDO experience is relevant to SerDes because LDO PSRR and output noise directly affect sensitive high-speed blocks. For example, if the LDO powers PLL or clocking circuits, residual supply ripple can become phase noise or jitter. If it powers RX front-end or ADC reference, it can reduce vertical eye margin. So I would analyze PSRR not only as a regulator metric, but as part of the SerDes power integrity and jitter budget.
```

---

## 27. Open Questions

* What PSRR targets are used for Synopsys PCIe 7.0 LDOs?
* Which frequency bands matter most for PLL supplies?
* Is PSRR specified at block level or system level?
* How is supply-induced jitter simulated internally?
* Are LDO PSRR simulations linked to PLL phase noise simulations?
* What output decap is available in the target process?
* How is post-layout PSRR verified?
* How much package / board supply noise is modeled?
* Are PLL and RX supplies separated by dedicated LDOs?
* What are the most common PSRR-related silicon issues in SerDes IP?

---

## 28. Related Notes

* `../analog_ic_serdes_master_index.md`
* `serdes_power_integrity.md`
* `ldo_stability_notes.md`
* `bandgap_reference_notes.md`
* `../PLL_CDR_Clocking/phase_noise_jitter.md`
* `../SerDes/pcie7_overview.md`
* `../Study_Plans/synopsys_4_week_prep_plan.md`
* `../../02_Synopsys_Work/synopsys_master_note.md`
* `../../02_Synopsys_Work/onboarding_plan.md`

---

## 29. Next Actions

1. Create `ldo_stability_notes.md`.
2. Create `bandgap_reference_notes.md`.
3. Add PSRR diagrams later.
4. Add real simulation examples from past LDO work if available.
5. Add Synopsys-specific PSRR targets after joining.
6. Link this note to interview Q&A.

---

## Last Updated

2026-07-01
