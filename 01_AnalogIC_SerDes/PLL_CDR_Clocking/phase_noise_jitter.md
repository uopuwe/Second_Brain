---

title: "Phase Noise and Jitter"
domain: "AnalogIC_SerDes"
tags:

* PhaseNoise
* Jitter
* PLL
* CDR
* Clocking
* SerDes
* PCIe7
* Synopsys
  created: 2026-07-01
  updated: 2026-07-01
  source: "ChatGPT technical notes and SerDes preparation"
  status: "active"

---

# Phase Noise and Jitter

## Purpose

This note summarizes phase noise and jitter from the perspective of PLL / CDR / SerDes clocking preparation.

The goal is to connect oscillator / PLL phase noise to time-domain sampling uncertainty, eye closure, BER degradation, and PCIe 7.0 SerDes performance.

This note supports Synopsys preparation, especially for PCIe 7.0 clocking and LDO-related work.

---

## 1. Big Picture

In a high-speed SerDes link, the sampling clock must arrive at the correct time.

Any uncertainty in the clock edge creates sampling error.

At low data rates, small timing error may be tolerable. At 112G / 224G / PCIe 7.0-class links, timing margin becomes extremely small.

Key idea:

```text
Phase noise in frequency domain
↓
Timing jitter in time domain
↓
Sampling uncertainty
↓
Eye closure
↓
Higher BER / lower link margin
```

In SerDes, clock quality is not an isolated PLL metric. It directly affects receiver margin.

---

## 2. What Is Phase Noise?

An ideal oscillator output can be written as:

```text
v(t) = A cos(2πf0t)
```

A real oscillator has amplitude noise and phase noise:

```text
v(t) = A(t) cos(2πf0t + φ(t))
```

Usually, phase noise matters more for clocking because zero-crossing time depends strongly on phase variation.

Phase noise describes short-term random phase fluctuation around the carrier.

It is usually reported as:

```text
L(f) in dBc/Hz
```

where `f` is offset frequency from the carrier.

Example:

```text
Phase noise = -100 dBc/Hz at 1 MHz offset
```

This means the noise power in a 1 Hz bandwidth at 1 MHz away from the carrier is 100 dB below the carrier power.

---

## 3. What Is Jitter?

Jitter is timing uncertainty of clock edges in the time domain.

An ideal clock edge happens exactly at:

```text
t = nT
```

A real clock edge happens at:

```text
t = nT + Δt
```

where `Δt` is timing error.

Common jitter units:

* seconds
* ps
* fs
* UI

UI means unit interval.

For a data rate:

```text
UI = 1 / data rate
```

For very high-speed links, the UI is extremely small, so even small jitter becomes important.

---

## 4. Phase Error to Time Error

Phase and time are connected.

For a clock frequency `f0`:

```text
Δφ = 2πf0Δt
```

Therefore:

```text
Δt = Δφ / (2πf0)
```

This is the most important bridge between phase noise and jitter.

Key idea:

```text
The same phase error creates smaller or larger time error depending on clock frequency.
```

For clocking discussion:

* Phase noise is often analyzed in frequency domain.
* Jitter is often interpreted in time domain.
* SerDes sampling margin cares about time-domain uncertainty.

---

## 5. Integrated RMS Jitter from Phase Noise

Phase noise is often integrated over an offset-frequency range to estimate RMS jitter.

A commonly used relationship is:

```text
σt = 1 / (2πf0) × sqrt(2 × ∫ 10^(L(f)/10) df)
```

where:

* `σt` is RMS jitter in seconds
* `f0` is carrier frequency
* `L(f)` is single-sideband phase noise in dBc/Hz
* integration range is usually selected based on system relevance

The factor of 2 appears because single-sideband phase noise is converted into total phase variance.

Important warning:

```text
Integrated jitter depends strongly on integration bandwidth.
```

So a jitter number without integration range is incomplete.

Bad statement:

```text
The jitter is 100 fs.
```

Better statement:

```text
The integrated RMS jitter is 100 fs from 10 kHz to 100 MHz offset.
```

Because apparently numbers need context, an idea humanity keeps rediscovering after every design review.

---

## 6. Random Jitter vs Deterministic Jitter

Total jitter is often separated into:

```text
Total Jitter = Random Jitter + Deterministic Jitter
```

## Random Jitter

Random jitter is usually caused by thermal noise, flicker noise, oscillator phase noise, and other random processes.

Characteristics:

* Unbounded in theory
* Often modeled as Gaussian
* Described by RMS value
* Important for BER extrapolation

Examples:

* VCO thermal noise
* PLL phase noise
* Clock buffer random noise
* Device noise affecting zero crossing

## Deterministic Jitter

Deterministic jitter is bounded and caused by systematic effects.

Examples:

* Duty-cycle distortion
* Data-dependent jitter
* ISI-induced jitter
* Periodic jitter
* Power-supply-induced jitter
* Crosstalk-induced jitter

Characteristics:

* Bounded
* Pattern-dependent or periodic
* Often measured peak-to-peak
* Can sometimes be reduced by design, layout, equalization, or calibration

---

## 7. Important Jitter Types in SerDes

## Period Jitter

Variation in one clock period from its ideal value.

Useful for clock quality but not always the best metric for SerDes sampling.

## Cycle-to-Cycle Jitter

Difference between adjacent clock periods.

Useful for digital timing and clock distribution.

## Long-Term Jitter

Accumulated timing variation over many cycles.

Relevant when low-frequency wander matters.

## RMS Jitter

Standard deviation of timing error.

Often used for random jitter.

## Peak-to-Peak Jitter

Maximum observed timing spread.

Can be misleading unless observation time and BER target are specified.

## UI Jitter

Jitter normalized to unit interval.

Example:

```text
jitter_UI = jitter_seconds / UI
```

This is useful for SerDes because margin is naturally measured relative to UI.

---

## 8. Phase Noise Regions

Oscillator phase noise often has different slope regions:

```text
1/f^3 region
1/f^2 region
flat noise floor
```

Typical interpretation:

* Close-in noise may be dominated by flicker noise upconversion.
* Far-out noise may be dominated by thermal noise.
* Noise floor may come from buffer, divider, or measurement limitations.

In PLL systems, the final output phase noise is shaped by the loop.

---

## 9. PLL Noise Contributors

A PLL output phase noise can include contributions from:

* Reference clock
* PFD / charge pump
* Loop filter
* VCO
* Divider
* Clock buffers
* Supply noise
* Substrate noise
* Spur coupling

Simplified view:

```text
Reference noise dominates inside PLL bandwidth.
VCO noise dominates outside PLL bandwidth.
```

More carefully:

* Low-frequency output phase follows reference path.
* High-frequency output phase is dominated by VCO noise.
* Loop bandwidth determines the crossover.
* Charge pump noise and divider noise are also shaped by the loop.

---

## 10. PLL Bandwidth Tradeoff

PLL loop bandwidth is a key design knob.

## Wider Bandwidth

Advantages:

* Tracks reference more strongly
* Suppresses VCO close-in noise over wider range
* Faster lock time

Disadvantages:

* Passes more reference noise
* Passes more PFD / charge pump noise
* May increase spur sensitivity
* Stability becomes more challenging

## Narrower Bandwidth

Advantages:

* Filters reference noise better
* Can reduce some in-band noise sources

Disadvantages:

* Allows more VCO noise
* Slower tracking
* Slower lock
* May not track required low-frequency variation

Key SerDes question:

```text
Which jitter components should the clocking loop track, and which should it filter?
```

---

## 11. CDR Jitter Transfer, Tolerance, and Generation

CDR behavior is often described using three concepts.

## Jitter Transfer

How much input jitter appears at the recovered clock or output data.

Question:

```text
If input data has jitter, how much does the CDR track it?
```

Low-frequency jitter may be tracked. High-frequency jitter may be rejected or may cause sampling error.

## Jitter Tolerance

How much input jitter the receiver can tolerate while maintaining target BER.

Question:

```text
How much sinusoidal jitter can the receiver survive at each jitter frequency?
```

Jitter tolerance is crucial for compliance and link robustness.

## Jitter Generation

How much jitter the CDR / transmitter / clocking system creates by itself.

Question:

```text
Even with a clean input, how much jitter does the circuit add?
```

---

## 12. Jitter and Eye Closure

Clock jitter causes horizontal eye closure.

Noise and distortion cause vertical eye closure.

For PAM4, this is especially painful because vertical eye openings are already smaller than NRZ.

Simplified view:

```text
Clock jitter
↓
Sampling point moves left/right
↓
Less horizontal margin
↓
Higher probability of sampling during transition
↓
More symbol errors
```

For PAM4:

```text
Smaller vertical eye
+
Timing uncertainty
+
ISI
+
Noise
=
Reduced link margin
```

This is why PLL / CDR clock quality matters so much in high-speed PAM4 SerDes.

---

## 13. Supply Noise to Jitter

Supply noise can become jitter through several mechanisms.

## VCO Supply Pushing

If VCO frequency changes with supply voltage:

```text
KVDD = Δf / ΔVDD
```

Then supply ripple modulates oscillator frequency.

This creates phase modulation and jitter.

Chain:

```text
Supply ripple
↓
VCO frequency modulation
↓
Phase modulation
↓
Clock jitter
```

## Clock Buffer Delay Modulation

Clock buffer delay depends on supply voltage.

Supply noise can modulate buffer delay:

```text
Supply noise
↓
Delay variation
↓
Edge timing variation
↓
Jitter
```

## RX Front-End / ADC Impact

Supply noise can also affect:

* comparator threshold
* sampler aperture
* ADC reference
* ADC comparator delay
* bias current
* front-end gain

For SerDes, power noise can hurt both timing and amplitude margin.

---

## 14. Why LDO Matters

An LDO can reduce supply noise, but only within its useful PSRR range.

Important LDO-related questions:

* What is the LDO output noise?
* What is PSRR at PLL-sensitive frequencies?
* What frequency range dominates jitter conversion?
* Does the LDO remain stable across PVT and load?
* Does load transient create supply disturbance?
* Is there coupling through layout or shared supply routing?

Important chain:

```text
External supply noise
↓
LDO finite PSRR
↓
Residual internal supply noise
↓
VCO / clock buffer / sampler modulation
↓
Jitter and eye closure
```

This is a key connection between LDO experience and SerDes clocking.

---

## 15. Phase Noise vs Jitter: How to Explain in Interview

A concise explanation:

```text
Phase noise is the frequency-domain representation of random phase fluctuation around a carrier, usually reported in dBc/Hz at offset frequencies. Jitter is the time-domain edge uncertainty caused by phase fluctuation. For a clock at frequency f0, phase error and timing error are related by Δt = Δφ / (2πf0). By integrating phase noise over a relevant offset-frequency band, we can estimate RMS jitter. In SerDes, this jitter directly affects sampling margin and causes horizontal eye closure.
```

A SerDes-focused explanation:

```text
In high-speed SerDes, phase noise matters because it becomes sampling clock jitter. Sampling jitter moves the sampling instant inside the eye, reducing horizontal margin. In PAM4 links, the vertical margin is already smaller than NRZ, so clock jitter, supply-induced jitter, and CDR tracking behavior become critical to BER and link margin.
```

A Synopsys-role-focused explanation:

```text
For PCIe 7.0 clocking, I need to understand not just the PLL phase noise number, but which noise sources dominate over which offset-frequency range, how much integrated jitter falls into the relevant bandwidth, how CDR tracks or filters that jitter, and how LDO supply noise can convert into clock jitter through VCO supply pushing or clock buffer delay modulation.
```

---

## 16. Common Interview Questions

## Q1: What is the difference between phase noise and jitter?

Phase noise is frequency-domain phase fluctuation around a carrier. Jitter is time-domain edge uncertainty. They describe related phenomena in different domains.

## Q2: How do you convert phase noise to RMS jitter?

Integrate phase noise over the relevant offset-frequency range to obtain phase variance, then divide RMS phase error by `2πf0` to convert to time jitter.

## Q3: Why does integration bandwidth matter?

Because phase noise is frequency-dependent. Different systems care about different offset-frequency ranges. A jitter number without integration range is incomplete.

## Q4: How does PLL bandwidth affect output phase noise?

Inside loop bandwidth, output phase noise tends to follow reference and in-loop noise sources. Outside loop bandwidth, VCO noise tends to dominate. Increasing bandwidth suppresses more VCO noise but passes more reference / PFD / charge pump noise.

## Q5: How does supply noise create jitter?

Supply noise can modulate VCO frequency, clock buffer delay, sampler timing, comparator delay, or bias conditions. This converts voltage noise into timing uncertainty.

## Q6: Why is jitter especially important for PAM4?

PAM4 has smaller vertical eye openings than NRZ. Timing jitter causes horizontal eye closure, and when combined with smaller vertical margin, ISI, and noise, the BER margin becomes worse.

## Q7: What is CDR jitter tolerance?

It describes how much input jitter the receiver can tolerate while maintaining a target BER. It is usually frequency-dependent.

## Q8: What is the difference between jitter transfer and jitter tolerance?

Jitter transfer describes how input jitter is passed to recovered clock or output. Jitter tolerance describes how much input jitter the system can survive.

## Q9: What is random jitter?

Random jitter is unbounded timing variation often caused by thermal noise and phase noise. It is usually modeled statistically and described by RMS value.

## Q10: What is deterministic jitter?

Deterministic jitter is bounded timing variation caused by systematic effects such as ISI, duty-cycle distortion, periodic interference, or supply noise.

---

## 17. Practical Simulation / Measurement Notes

Important simulation outputs:

* Phase noise plot
* Integrated RMS jitter
* Transient jitter
* Period jitter
* Cycle-to-cycle jitter
* Eye diagram
* Bathtub curve
* Jitter transfer curve
* Jitter tolerance curve
* Supply noise sensitivity

Important details to always record:

* Carrier frequency
* Offset-frequency integration range
* RMS vs peak-to-peak
* Simulation corner
* Supply condition
* Temperature
* Load condition
* Whether noise is PLL output, VCO-only, recovered clock, or sampling clock

Bad note:

```text
PLL jitter is 80 fs.
```

Better note:

```text
PLL output integrated RMS jitter is 80 fs from 10 kHz to 100 MHz at 16 GHz output frequency under TT, 0.8 V, 25°C.
```

The second one sounds like an engineer wrote it. The first one sounds like a marketing slide escaped containment.

---

## 18. Open Questions

* What integration bandwidth does Synopsys use for PCIe 7.0 clocking jitter?
* What PLL architecture is used in the relevant IP?
* What is the target RMS jitter budget?
* Which jitter contributors dominate in the actual design?
* How much supply-induced jitter comes from LDO residual ripple?
* Which clock paths are most sensitive to buffer delay modulation?
* How is CDR jitter tolerance verified?
* What compliance tests are used for PCIe 7.0 jitter?
* How are phase noise and transient jitter correlated in the internal flow?
* Which simulation benches should I learn first after joining?

---

## 19. Related Notes

* `../analog_ic_serdes_master_index.md`
* `../SerDes/pcie7_overview.md`
* `../Study_Plans/synopsys_4_week_prep_plan.md`
* `pll_fundamentals.md`
* `cdr_fundamentals.md`
* `pcie7_clocking_notes.md`
* `../LDO_Bandgap/ldo_psrr_notes.md`
* `../LDO_Bandgap/serdes_power_integrity.md`
* `../../02_Synopsys_Work/synopsys_master_note.md`

---

## 20. Next Actions

1. Create `pll_fundamentals.md`.
2. Create `cdr_fundamentals.md`.
3. Create `pcie7_clocking_notes.md`.
4. Create `../LDO_Bandgap/serdes_power_integrity.md`.
5. Add real equations, diagrams, and paper references later.
6. Update this note after reading actual Synopsys internal documents.

---

## Last Updated

2026-07-01
