---

title: "Bandgap and Reference Notes"
domain: "AnalogIC_SerDes"
tags:

* Bandgap
* Reference
* LDO
* Bias
* PSRR
* Noise
* SerDes
* PLL
* ADC
* PCIe7
* Synopsys
  created: 2026-07-01
  updated: 2026-07-01
  source: "ChatGPT technical notes and Synopsys role preparation"
  status: "active"

---

# Bandgap and Reference Notes

## Purpose

This note summarizes bandgap and reference design from the perspective of analog IC design and SerDes power integrity.

The goal is to understand how reference voltage accuracy, noise, PSRR, startup, temperature drift, and layout affect LDOs, PLLs, CDRs, ADCs, RX front-end circuits, bias circuits, and high-speed SerDes performance.

This note supports Synopsys preparation, especially for PCIe 7.0 clocking, LDO, and analog / mixed-signal IP work.

---

## 1. Big Picture

A bandgap reference provides a relatively stable reference voltage across process, supply, and temperature.

In many analog / mixed-signal IP blocks, references are used by:

* LDOs
* bias generators
* ADCs
* comparators
* CTLE / RX front-end
* PLL / CDR support circuits
* calibration circuits
* POR / BOR circuits
* common-mode generation
* threshold generation

Key idea:

```text
Reference quality affects everything downstream.
```

If the reference is noisy, supply-sensitive, or temperature-dependent, the error can propagate into many blocks.

Important chain:

```text
Bandgap / reference error
↓
LDO output error or noise
↓
PLL / RX / ADC / bias disturbance
↓
jitter, amplitude error, threshold error, or calibration error
↓
SerDes margin degradation
```

A bad reference is not a local problem. It is a polite disaster distributor.

---

## 2. Why Reference Design Matters in SerDes

High-speed SerDes depends on accurate and quiet analog support circuits.

Reference issues can affect:

* PLL bias current
* VCO control environment
* LDO output voltage
* RX front-end bias
* CTLE operating point
* comparator threshold
* ADC reference level
* ADC capacitor DAC reference
* PAM4 decision thresholds
* calibration DACs
* common-mode levels

For PCIe 7.0 / PAM4, this matters because:

* vertical eye margin is small
* timing margin is small
* jitter budget is tight
* RX decisions are sensitive to threshold and gain errors
* ADC-based receivers are sensitive to reference noise and drift

Key idea:

```text
In PAM4 SerDes, reference error can become vertical eye closure.
In clocking circuits, reference and bias error can become jitter.
```

---

## 3. Bandgap Basic Principle

A bandgap reference combines two temperature-dependent voltages:

```text
CTAT voltage + scaled PTAT voltage ≈ temperature-independent voltage
```

Where:

* CTAT = complementary to absolute temperature
* PTAT = proportional to absolute temperature

Typical CTAT source:

```text
VBE of a bipolar transistor
```

Typical PTAT source:

```text
ΔVBE between two bipolar devices operating at different current densities
```

The simplified reference equation is:

```text
VREF = VBE + K × ΔVBE
```

`VBE` decreases with temperature.

`ΔVBE` increases with temperature.

With proper scaling, first-order temperature dependence can be cancelled.

---

## 4. CTAT Component

The base-emitter voltage `VBE` of a bipolar device decreases with temperature.

Approximate behavior:

```text
VBE decreases by about 1.5 to 2 mV/°C
```

This is the CTAT component.

In CMOS processes, parasitic BJTs are often used for bandgap references.

Important concerns:

* device matching
* current density ratio
* temperature behavior
* layout symmetry
* substrate noise
* process variation

---

## 5. PTAT Component

The PTAT voltage is usually generated from the difference between two VBE voltages.

Simplified expression:

```text
ΔVBE = VT × ln(N)
```

where:

* `VT = kT/q`
* `N` is current density ratio or emitter area ratio

Since `VT` is proportional to absolute temperature, `ΔVBE` is PTAT.

The PTAT voltage is scaled and added to `VBE`.

Important concerns:

* resistor ratio accuracy
* current density matching
* amplifier offset
* device mismatch
* temperature curvature

---

## 6. First-Order Bandgap Reference

The classic first-order bandgap generates a voltage near the silicon bandgap voltage.

Typical output:

```text
VREF ≈ 1.2 V
```

But in modern low-voltage processes, lower-voltage references may be required.

First-order cancellation removes the main linear temperature slope, but residual curvature remains.

Result:

```text
VREF is relatively stable,
but not perfectly flat across temperature.
```

Apparently silicon refuses to become ideal just because the schematic looks tidy.

---

## 7. Curvature Error

Even after first-order compensation, bandgap reference voltage still has curvature over temperature.

Sources of curvature:

* nonlinear VBE temperature behavior
* resistor temperature coefficient
* mobility variation
* current source temperature dependence
* amplifier offset drift
* package stress
* device mismatch

Curvature correction techniques:

* higher-order compensation
* nonlinear resistor combinations
* PTAT2 terms
* temperature-dependent current shaping
* digital trimming
* piecewise correction

Important question:

```text
What temperature accuracy is actually required by the downstream block?
```

Do not overdesign the bandgap if the load does not need it. Also do not underdesign it and then blame “system variation” like a cowardly spreadsheet.

---

## 8. Reference Accuracy

Reference accuracy depends on:

* initial process variation
* resistor mismatch
* BJT mismatch
* amplifier offset
* current mirror mismatch
* temperature drift
* supply sensitivity
* layout gradient
* package stress
* aging

Important specs:

* absolute voltage accuracy
* temperature coefficient
* line regulation
* load regulation
* output noise
* PSRR
* startup reliability
* trim range
* trim resolution

For LDO use, reference error directly affects output voltage:

```text
VOUT = VREF × feedback gain
```

So reference error is amplified by the LDO feedback ratio.

---

## 9. Temperature Coefficient

Temperature coefficient describes how much reference voltage changes with temperature.

Common unit:

```text
ppm/°C
```

Example:

```text
20 ppm/°C
```

This means the reference changes by 20 parts per million per degree Celsius.

Important notes:

* TC depends on temperature range.
* TC may look good near room temperature but worse at extremes.
* Curvature matters.
* Trim point matters.
* Packaging can shift behavior.

Bad statement:

```text
The bandgap is temperature-stable.
```

Better statement:

```text
The bandgap has 25 ppm/°C temperature coefficient from -40°C to 125°C after trimming.
```

Engineering: where every useful sentence becomes longer and more annoying.

---

## 10. Line Regulation / Supply Sensitivity

Bandgap output should not change much with supply voltage.

Supply sensitivity matters because upstream supply noise or droop can modulate the reference.

Chain:

```text
Supply ripple
↓
bandgap output ripple
↓
LDO reference ripple
↓
LDO output ripple
↓
PLL / RX / ADC disturbance
```

Important questions:

* What is bandgap PSRR?
* What supply frequency range matters?
* Is the reference buffered?
* Does supply noise couple through current mirrors?
* Does startup circuit inject supply-sensitive error?
* Is there isolation from noisy digital supply?

---

## 11. Reference Noise

Reference noise is critical for sensitive analog blocks.

Noise sources include:

* BJT noise
* resistor thermal noise
* amplifier input noise
* current mirror noise
* flicker noise
* reference buffer noise
* supply-coupled noise
* substrate-coupled noise

Reference noise can affect:

* LDO output noise
* ADC reference noise
* comparator thresholds
* bias currents
* PLL / VCO bias stability
* PAM4 decision thresholds

Important chain:

```text
Reference noise
↓
threshold / bias / supply noise
↓
amplitude or timing error
↓
SerDes margin loss
```

For ADC-based PAM4 RX, reference noise can directly degrade digitized amplitude accuracy.

For PLL-related circuits, bias noise can become phase noise or jitter.

---

## 12. Bandgap PSRR

Bandgap PSRR describes how well the reference rejects supply noise.

Important frequency regions:

## Low Frequency

Dominated by:

* current source supply rejection
* opamp gain
* feedback loop behavior
* cascode effectiveness

## Mid Frequency

Dominated by:

* amplifier bandwidth
* current mirror poles
* internal nodes
* reference buffer behavior

## High Frequency

Dominated by:

* parasitic coupling
* substrate noise
* supply routing
* local decap
* package coupling

Important idea:

```text
A bandgap with poor PSRR can poison every LDO that uses it.
```

That is not drama. That is literally signal propagation.

---

## 13. Startup Circuit

A bandgap can have more than one operating point.

One possible operating point is the desired reference state.

Another possible operating point is zero-current state.

Startup circuit ensures the bandgap leaves the zero-current state and reaches the correct operating point.

Startup must work across:

* process
* voltage
* temperature
* ramp rate
* power sequencing
* low supply
* leakage
* aging

Startup problems can cause:

* no reference
* wrong reference voltage
* long startup delay
* intermittent boot failure
* POR / BOR failure
* LDO not regulating
* analog IP stuck in bad state

Important question:

```text
Does startup work for slow ramp, fast ramp, cold corner, hot leakage, and minimum supply?
```

Startup circuits are boring until they fail, then suddenly everyone becomes religious.

---

## 14. Reference Buffer

Bandgap output often cannot directly drive all loads.

A reference buffer may be needed.

The buffer provides:

* drive capability
* isolation from load variation
* lower output impedance
* filtering
* distribution support

But the buffer can add:

* noise
* offset
* stability issues
* PSRR degradation
* startup delay
* load transient response problems

Important questions:

* What loads does the reference drive?
* Is the buffer stable with capacitive load?
* Does buffer noise dominate?
* Is the buffer supply clean?
* Is reference distributed globally or locally regenerated?

---

## 15. Reference Distribution

In a large IP block, reference distribution matters.

Problems:

* IR drop
* coupling from digital signals
* substrate noise
* clock coupling
* long routing resistance
* capacitive coupling
* reference sharing between noisy and sensitive blocks
* mismatch between local references

Good practices:

* local buffering
* quiet routing
* shielding
* differential or Kelvin sensing if needed
* local filtering
* star distribution when appropriate
* avoid routing reference near switching clocks
* isolate ADC / PLL references when needed

Key question:

```text
Is the reference quiet at the block that actually uses it?
```

Not where the schematic says it is. Where the electrons suffer.

---

## 16. Bandgap and LDO Connection

LDO output depends on reference voltage.

Simplified:

```text
VOUT = VREF × (1 + R1 / R2)
```

So reference error becomes output error.

Reference noise becomes LDO output noise through the closed-loop transfer.

Reference supply sensitivity can appear as LDO output ripple.

Important chain:

```text
Bandgap noise / drift
↓
LDO reference input
↓
LDO output noise / drift
↓
sensitive SerDes block disturbance
```

Therefore, for an LDO powering PLL / RX / ADC:

* reference noise must be low
* reference PSRR must be good
* reference routing must be quiet
* reference buffer must be stable
* reference startup must be reliable

---

## 17. Bandgap and PLL / Clocking

Bandgap may not directly generate the PLL clock, but it can affect PLL through:

* bias current reference
* LDO reference
* VCO bias
* charge pump current reference
* loop filter bias circuits
* regulator for PLL supply
* calibration DAC reference

Possible chain:

```text
Reference noise
↓
charge pump current noise or VCO bias noise
↓
PLL phase noise
↓
clock jitter
↓
SerDes eye closure
```

Another chain:

```text
Reference drift
↓
VCO bias / control range shift
↓
PLL operating point shift
↓
jitter or lock margin issue
```

Important questions:

* Does PLL use reference-derived bias?
* Is charge pump current reference noisy?
* Does VCO supply LDO use this bandgap?
* Is reference noise filtered before reaching clocking circuits?

---

## 18. Bandgap and ADC / PAM4 RX

ADC-based PAM4 RX can be sensitive to reference quality.

Reference may affect:

* ADC full-scale range
* capacitor DAC levels
* comparator thresholds
* calibration DACs
* PAM4 slicer levels
* common-mode reference
* gain calibration
* offset calibration

Reference noise can appear as input-referred ADC noise.

Reference drift can cause gain error.

Reference mismatch between interleaved channels can create channel mismatch.

Possible chain:

```text
ADC reference noise
↓
digitized amplitude error
↓
DSP / slicer decision error
↓
vertical eye closure
```

For PAM4, this is dangerous because adjacent levels are closer together.

---

## 19. Bandgap and Bias Circuits

Bandgap often supports bias generation.

Bias circuits may create:

* PTAT current
* constant-gm bias
* temperature-compensated bias
* current references
* voltage references
* threshold references

Bias errors can affect:

* amplifier bandwidth
* CTLE pole / zero
* comparator speed
* VCO frequency
* charge pump current
* ADC sampling switch behavior
* RX front-end gain

Important idea:

```text
Reference error becomes bias error.
Bias error becomes circuit performance error.
```

In SerDes, these circuit performance errors can become link margin issues.

---

## 20. Trim and Calibration

Bandgap references often need trimming.

Trim can correct:

* absolute voltage error
* resistor mismatch
* curvature
* process variation
* output target

Trim methods:

* fuse trim
* metal option
* digital register trim
* resistor ladder trim
* current DAC trim
* production test trim

Important questions:

* What is trim range?
* What is trim resolution?
* Is trim one-time or programmable?
* Is temperature drift corrected or only room-temperature error?
* Does trim affect noise or PSRR?
* Is trim stored reliably?

Bad trim strategy:

```text
Trim it at room temperature and pray.
```

A bold method, though not usually recommended outside mythology.

---

## 21. Layout Considerations

Bandgap layout is critical.

Important layout rules:

* match BJT devices carefully
* use common-centroid if needed
* match resistor ratios
* shield sensitive nodes
* isolate from digital noise
* avoid thermal gradients
* use guard rings
* keep reference routing quiet
* match current mirror devices
* avoid stress gradients
* place decap carefully
* separate noisy supply routing
* use Kelvin sensing where needed

Common layout problems:

* unequal BJT stress
* resistor gradient
* coupling into high-impedance nodes
* digital clock near reference line
* poor ground return
* noisy substrate
* bad startup routing
* reference buffer too far from load
* shared supply impedance with switching circuits

---

## 22. Simulation Checklist

Bandgap simulations should include:

## DC / Accuracy

* nominal VREF
* line regulation
* load regulation
* temperature sweep
* process corners
* supply corners
* resistor variation
* device mismatch
* Monte Carlo

## Noise

* output noise spectral density
* integrated output noise
* low-frequency flicker noise
* buffer noise
* reference noise contribution to LDO / ADC

## PSRR

* supply ripple rejection vs frequency
* low / mid / high frequency behavior
* post-layout PSRR
* effect of decap and buffer

## Startup

* cold startup
* hot startup
* slow supply ramp
* fast supply ramp
* minimum supply startup
* leakage corner
* power sequencing

## Transient

* reference settling time
* load step if buffered
* supply ramp response
* enable / disable behavior
* mode transition

## Post-Layout

* extracted accuracy
* extracted PSRR
* extracted noise
* extracted startup
* extracted reference distribution

---

## 23. Debug Checklist

If silicon shows reference-related issues, check:

* Does VREF start correctly?
* Does VREF depend too much on supply?
* Does VREF drift with temperature?
* Is startup failing at cold or hot?
* Is output noisy?
* Does LDO output noise follow reference noise?
* Does PLL jitter improve with cleaner reference?
* Does ADC performance improve with external reference?
* Does digital activity couple into reference?
* Does reference shift when other blocks turn on?
* Does reference settling affect calibration?
* Does trim code behave as expected?

Possible debug flow:

```text
Observe SerDes / LDO / PLL issue
↓
Check local supply
↓
Check reference voltage
↓
Check reference noise
↓
Check reference PSRR
↓
Check startup and settling
↓
Check coupling from digital / clock activity
↓
Check downstream block sensitivity
```

---

## 24. Interview Explanation

Short explanation:

```text
A bandgap reference generates a relatively temperature-stable voltage by combining a CTAT VBE term with a scaled PTAT ΔVBE term. The simplified form is VREF = VBE + K × ΔVBE. The reference must be accurate, low-noise, supply-insensitive, and reliable at startup. In SerDes, bandgap and reference quality matters because it affects LDO outputs, bias currents, ADC references, comparator thresholds, PLL support circuits, and calibration blocks.
```

Synopsys-focused explanation:

```text
For PCIe 7.0 SerDes work, I would treat bandgap and reference circuits as part of the analog performance foundation. A noisy or supply-sensitive reference can propagate through LDOs, PLL bias, RX front-end bias, ADC reference, or PAM4 thresholds. That can become jitter, vertical eye closure, or calibration error. So the reference should be reviewed together with noise, PSRR, startup, layout isolation, and downstream load sensitivity.
```

Senior-level explanation:

```text
The key is to translate reference specs into system impact. A bandgap does not only need a good nominal voltage. It must provide low noise, low temperature drift, good supply rejection, robust startup, and clean distribution to sensitive blocks. For a SerDes IP, reference noise can become LDO output noise, PLL bias noise, ADC reference noise, or PAM4 threshold error. Therefore the reference architecture, buffer, trim, layout, and distribution should be designed based on the sensitivity of downstream blocks.
```

---

## 25. Common Interview Questions

## Q1: What is the basic principle of a bandgap reference?

A bandgap reference combines a CTAT voltage, usually VBE, with a scaled PTAT voltage, usually ΔVBE, to create a relatively temperature-stable reference voltage.

## Q2: Why is ΔVBE PTAT?

ΔVBE is proportional to thermal voltage `VT = kT/q`, so it increases with absolute temperature.

## Q3: Why is VBE CTAT?

The base-emitter voltage of a bipolar transistor decreases as temperature increases.

## Q4: What limits bandgap accuracy?

Process variation, resistor mismatch, BJT mismatch, amplifier offset, current mirror mismatch, temperature curvature, supply sensitivity, layout stress, and package effects.

## Q5: Why is startup needed?

A bandgap can have a zero-current stable state. Startup circuitry ensures the bandgap reaches the intended operating point after power-on.

## Q6: How does bandgap noise affect an LDO?

Bandgap noise appears at the LDO reference input and can be transferred to the LDO output, disturbing sensitive loads.

## Q7: How can reference noise affect PLL jitter?

Reference-derived bias or LDO output noise can modulate VCO frequency, charge pump current, or clocking support circuits, creating phase noise and jitter.

## Q8: How can reference error affect ADC-based PAM4 RX?

ADC reference error or noise changes digitized amplitude levels and can reduce vertical eye margin or create gain error.

## Q9: What is bandgap PSRR?

Bandgap PSRR describes how much supply ripple is rejected before appearing at the reference output.

## Q10: What are key bandgap layout concerns?

Matching, thermal gradients, resistor ratio accuracy, substrate noise, digital coupling, quiet routing, guard rings, reference distribution, and isolation from noisy supplies.

---

## 26. Personal Connection to My Experience

This note connects to my previous analog IP and LDO work.

Relevant background:

* bandgap reference
* LDO reference path
* PSRR
* output noise
* startup
* POR / BOR
* analog biasing
* PVT simulation
* Monte Carlo
* layout-sensitive analog design

How to present this experience:

```text
My bandgap and reference experience is relevant to SerDes because reference quality affects LDO output, PLL bias, RX front-end bias, ADC reference, and calibration circuits. In high-speed PAM4 links, reference noise or drift can become jitter, vertical eye closure, threshold error, or calibration error. So I would analyze the reference not only as a standalone voltage source, but as part of the SerDes power, bias, and noise chain.
```

---

## 27. Open Questions

* What bandgap / reference architecture is used in Synopsys PCIe 7.0 IP?
* Which LDOs share the same reference?
* Are PLL and ADC references separated from general references?
* What reference noise budget is used?
* What reference PSRR is required?
* Is reference distribution global, local, or buffered per block?
* How is startup verified across PVT?
* Is trimming required?
* How is reference noise linked to PLL jitter or ADC SNDR?
* What are common reference-related silicon issues in SerDes IP?

---

## 28. Related Notes

* `../analog_ic_serdes_master_index.md`
* `serdes_power_integrity.md`
* `ldo_psrr_notes.md`
* `ldo_stability_notes.md`
* `../PLL_CDR_Clocking/phase_noise_jitter.md`
* `../SerDes/pcie7_overview.md`
* `../Study_Plans/synopsys_4_week_prep_plan.md`
* `../../02_Synopsys_Work/synopsys_master_note.md`
* `../../02_Synopsys_Work/onboarding_plan.md`

---

## 29. Next Actions

1. Create an LDO interview Q&A note.
2. Create PLL fundamentals note.
3. Add bandgap diagrams later.
4. Add actual circuit examples from past work if available.
5. Add Synopsys-specific reference requirements after joining.
6. Link this note to future ADC and PLL notes.

---

## Last Updated

2026-07-01
