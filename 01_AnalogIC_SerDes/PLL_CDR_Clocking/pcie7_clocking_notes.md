---

title: "PCIe 7.0 Clocking Notes"
domain: "AnalogIC_SerDes"
tags:

* PCIe7
* Clocking
* PLL
* CDR
* Jitter
* SerDes
* PAM4
* Synopsys
  created: 2026-07-01
  updated: 2026-07-01
  source: "ChatGPT technical notes and Synopsys role preparation"
  status: "active"

---

# PCIe 7.0 Clocking Notes

## Purpose

This note summarizes PCIe 7.0 clocking from the perspective of analog / mixed-signal SerDes preparation.

The goal is to connect PLL, CDR, clock distribution, jitter, supply noise, and PAM4 receiver margin into one practical clocking view.

---

## 1. Big Picture

PCIe 7.0 pushes the PHY to 128 GT/s using PAM4 signaling. At this speed, the clock path is not only a timing utility. It is one of the main link-margin limiters.

Simplified chain:

```text
Reference clock
down
PLL / clock generator
down
Clock distribution / phase generation
down
TX launch clock and RX sampling clock
down
CDR timing recovery
down
Eye margin / BER
```

The practical question is:

```text
How much timing uncertainty can the link tolerate before the eye closes?
```

---

---

## Formula Derivations

### 1. Unit Interval for PCIe 7.0

For a high-speed serial link, the unit interval is the time duration of one symbol or transfer interval.

```text
UI = 1 / data_rate
```

For PCIe 7.0, using 128 GT/s as the transfer rate:

```text
UI = 1 / 128e9
   = 7.8125 ps
```

This means one UI is only about 7.8 ps.

Design meaning:

```text
Small UI
↓
small timing margin
↓
PLL jitter, CDR error, clock buffer delay modulation, and supply-induced jitter become critical
```

Important note:

```text
待确认：For detailed PCIe 7.0 compliance analysis, confirm how the official specification defines transfer rate, PAM4 symbol mapping, FLIT / FEC overhead, and the exact timing budget.
```

---

### 2. Jitter as Fraction of UI

Jitter is often normalized to UI.

```text
jitter_UI = jitter_seconds / UI
```

Example:

```text
RMS jitter = 100 fs
UI = 7.8125 ps

jitter_UI = 100 fs / 7.8125 ps
          ≈ 0.0128 UI
```

So 100 fs RMS jitter is about 1.28% of UI.

Design meaning:

```text
At PCIe 7.0 speed, even femtosecond-level jitter can consume meaningful timing margin.
```

This is why clocking cannot be treated as a casual support block. At these speeds, clocking is basically holding the whole circus tent up while everyone else pretends the PHY is simple.

---

### 3. Phase Error to Timing Error

Clock phase error and timing error are related by:

```text
Δφ = 2πf0Δt
```

Therefore:

```text
Δt = Δφ / (2πf0)
```

where:

* `Δφ` is phase error in radians
* `f0` is clock frequency
* `Δt` is timing error in seconds

Design meaning:

```text
PLL phase noise
↓
phase error
↓
timing jitter
↓
sampling uncertainty
↓
horizontal eye closure
```

For SerDes, the time-domain effect matters because the receiver samples data at a specific clock edge.

---

### 4. Phase Noise to Integrated RMS Jitter

A common relationship between single-sideband phase noise and RMS jitter is:

```text
σt = 1 / (2πf0) × sqrt(2 × ∫ 10^(L(f)/10) df)
```

where:

* `σt` is RMS jitter in seconds
* `f0` is carrier frequency
* `L(f)` is phase noise in dBc/Hz
* the integral is over a defined offset-frequency range

Important rule:

```text
Integrated jitter must always specify the integration bandwidth.
```

Bad statement:

```text
PLL jitter is 80 fs.
```

Better statement:

```text
PLL output integrated RMS jitter is 80 fs from 10 kHz to 100 MHz at a specific output frequency and operating corner.
```

Design meaning:

```text
Different integration ranges can produce different jitter numbers.
```

So a jitter number without bandwidth is not a specification. It is a decorative number wearing an engineering costume.

---

### 5. Supply Noise to VCO Frequency Modulation

If the VCO frequency changes with supply voltage, define supply sensitivity as:

```text
KVDD = Δf / ΔVDD
```

where:

* `KVDD` is VCO supply pushing
* `Δf` is frequency change
* `ΔVDD` is supply voltage change

Supply ripple can modulate VCO frequency:

```text
Supply ripple
↓
VCO frequency modulation
↓
phase modulation
↓
PLL output jitter
↓
sampling clock uncertainty
```

Design meaning:

```text
LDO PSRR and output noise directly affect PLL / clocking jitter if the VCO or clock buffers are supply-sensitive.
```

This connects PCIe 7.0 clocking directly to LDO design.

Related notes:

* `../LDO_Bandgap/serdes_power_integrity.md`
* `../LDO_Bandgap/ldo_psrr_notes.md`

---

### 6. Clock Buffer Supply Noise to Delay Modulation

Clock buffers can convert supply noise into timing error.

Simplified relationship:

```text
Δt ≈ sensitivity_delay_to_supply × ΔVDD
```

where:

* `Δt` is clock edge timing shift
* `ΔVDD` is supply disturbance
* delay sensitivity depends on buffer design, load, process, and operating point

Design chain:

```text
Supply noise
↓
clock buffer delay variation
↓
clock edge movement
↓
sampling jitter
↓
horizontal eye closure
```

Design meaning:

```text
Even if the PLL itself is clean, noisy clock distribution can still degrade SerDes timing margin.
```

This is why clock distribution, local decap, LDO placement, and supply isolation matter.

---

### 7. Sampling Jitter and ADC-Based Receiver Error

For an ADC-based PAM4 receiver, sampling jitter creates voltage error proportional to signal slope.

```text
ΔV ≈ dV/dt × Δt
```

For a sinusoidal input, jitter-limited SNR is approximately:

```text
SNR_jitter ≈ -20 log10(2πfinσt)
```

where:

* `fin` is input frequency
* `σt` is RMS sampling jitter

Design meaning:

```text
Higher input frequency
↓
larger signal slope
↓
same sampling jitter creates larger voltage error
↓
worse SNDR / EVM / PAM4 symbol margin
```

This connects PLL / CDR clock quality to ADC-based receiver performance.

Related notes:

* `../ADC/sampling_jitter_adc.md`
* `../ADC/adc_based_receiver.md`

---

## Worked Examples

### Example 1: PCIe 7.0 UI Calculation

Given:

```text
Data rate = 128 GT/s
```

Calculation:

```text
UI = 1 / 128e9
   = 7.8125 ps
```

Conclusion:

```text
PCIe 7.0 has an extremely small UI, so clock jitter and CDR timing error must be tightly controlled.
```

---

### Example 2: 100 fs Jitter as UI Fraction

Given:

```text
RMS jitter = 100 fs
UI = 7.8125 ps
```

Calculation:

```text
jitter_UI = 100 fs / 7.8125 ps
          = 0.0128 UI
```

Conclusion:

```text
100 fs RMS jitter is about 1.28% UI.
```

Design interpretation:

```text
This may look small, but total timing margin must also include CDR error, channel-induced jitter, ISI, supply-induced jitter, clock distribution jitter, and receiver noise.
```

---

### Example 3: Supply Ripple Reaching VCO Through Finite LDO PSRR

Given:

```text
Input supply ripple = 10 mV
LDO PSRR = 40 dB at the ripple frequency
```

Since:

```text
40 dB = 100x attenuation
```

Residual output ripple:

```text
Vout_ripple = 10 mV / 100
            = 100 µV
```

Design interpretation:

```text
If the VCO is sensitive to supply noise, this residual 100 µV ripple can still create frequency modulation and jitter.
```

Open question:

```text
待确认：Need actual VCO supply sensitivity, LDO PSRR curve, and relevant supply noise spectrum to calculate jitter impact.
```

---

### Example 4: Sampling Jitter Impact on ADC-Based RX

Given:

```text
Input frequency = fin
RMS sampling jitter = σt
```

The jitter-limited SNR is:

```text
SNR_jitter ≈ -20 log10(2πfinσt)
```

Interpretation:

```text
As input frequency increases, the same sampling jitter causes worse SNR.
```

Design meaning for SerDes:

```text
ADC-based PAM4 receivers need low-jitter sampling clocks because high-frequency input content makes aperture jitter more damaging.
```

---

## Design Implications

### 1. PCIe 7.0 Clocking Is a System-Level Problem

PCIe 7.0 clocking is not only about building a PLL.

It includes:

* reference clock quality
* PLL phase noise
* PLL integrated jitter
* CDR tracking behavior
* jitter transfer
* jitter tolerance
* jitter generation
* clock distribution
* phase interpolator
* supply-induced jitter
* LDO PSRR
* local decap
* clock buffer delay modulation
* equalization interaction

Key design chain:

```text
Clocking noise
↓
sampling timing uncertainty
↓
horizontal eye closure
↓
reduced link margin
```

---

### 2. PAM4 Makes Clocking More Painful

PAM4 already has smaller vertical eye openings than NRZ.

Clock jitter closes the eye horizontally.

Together:

```text
PAM4 smaller vertical margin
+
clock jitter horizontal margin loss
+
ISI
+
supply noise
=
reduced receiver margin
```

So PCIe 7.0 clocking must be understood together with PAM4 receiver behavior.

---

### 3. PLL Jitter Must Be Connected to CDR Behavior

A PLL can generate a clock, but the receiver still depends on CDR behavior.

Important questions:

* Which jitter does the CDR track?
* Which jitter does the CDR reject?
* Which jitter becomes sampling error?
* How does CDR bandwidth interact with PLL noise?
* How does CDR interact with equalization?

Design meaning:

```text
PLL output jitter alone does not fully define RX timing margin.
CDR behavior determines how timing error appears at the sampler.
```

---

### 4. LDO and Power Integrity Are Part of Clocking

For PCIe 7.0 clocking, LDO design is not just power support.

LDO affects:

* VCO supply noise
* PLL phase noise
* clock buffer delay
* phase interpolator delay
* sampler aperture timing
* RX front-end bias
* ADC reference and sampling quality

Design meaning:

```text
Power integrity must be included in clocking analysis.
```

---

### 5. Clock Distribution Can Ruin a Clean PLL

Even if the PLL has good phase noise, clock distribution can add jitter.

Possible contributors:

* clock buffer supply noise
* duty-cycle distortion
* routing mismatch
* crosstalk
* substrate noise
* clock divider noise
* phase interpolator nonlinearity
* layout parasitics

Design meaning:

```text
The relevant clock quality is the clock at the sampler or transmitter, not only the clock at the PLL output.
```

Tiny distinction. Huge consequences. Naturally, the circuit charges extra for forgetting it.

---

## Synopsys Onboarding Questions

### Architecture Questions

* What is the top-level PCIe 7.0 clocking architecture?
* Which blocks are included in the local team’s responsibility?
* Is the clocking architecture based on PLL, DLL, ILO, PI, or a combination?
* Which clock domains are most important for the PHY?
* How are TX and RX clocks generated and distributed?
* How is the recovered clock handled in the RX path?

### PLL Questions

* What PLL architecture is used?
* What are the main PLL output frequencies?
* What is the target integrated RMS jitter?
* What phase noise integration range is used?
* What are the dominant PLL noise contributors?
* How are reference spur and deterministic jitter verified?
* How is supply-induced phase noise simulated?

### CDR Questions

* What CDR architecture is used?
* Is the CDR baud-rate or oversampling?
* Does it use a phase interpolator?
* What is the CDR loop bandwidth?
* How are jitter transfer, jitter tolerance, and jitter generation verified?
* How does the CDR interact with CTLE / FFE / DFE adaptation?

### Power / LDO Questions

* Which clocking blocks are powered by local LDOs?
* Are PLL, VCO, clock buffers, and PI powered by separate regulators?
* What are the LDO PSRR and noise requirements for clocking supplies?
* How is supply noise translated into jitter budget?
* Are supply ripple injection simulations part of signoff?
* How much decap is available near clocking blocks?

### Simulation / Signoff Questions

* Which simulations are most important for clocking signoff?
* Are phase noise, transient jitter, and supply-induced jitter all simulated?
* How is jitter budget allocated across PLL, CDR, PI, clock buffers, and channel?
* Are post-layout extracted simulations required for clocking paths?
* What are the most common clocking-related silicon issues?

---

## 待确认

The following items must be confirmed after joining Synopsys or from official public specifications.

### PCIe 7.0 Specification Details

* 待确认：Exact PCIe 7.0 jitter specifications.
* 待确认：Official compliance requirements for clocking and jitter.
* 待确认：How PCIe 7.0 defines timing budget under PAM4 and FLIT / FEC structure.
* 待确认：Which clocking assumptions apply to Synopsys PCIe 7.0 IP.

### Synopsys Internal Architecture

* 待确认：Actual Synopsys PCIe 7.0 PLL architecture.
* 待确认：Actual CDR architecture.
* 待确认：Whether the RX is slicer-based, ADC-based, or uses another internal architecture.
* 待确认：Clock distribution architecture.
* 待确认：Phase interpolator usage.
* 待确认：Local LDO partitioning for clocking blocks.

### Signoff and Simulation

* 待确认：Internal phase noise and jitter simulation methodology.
* 待确认：Jitter integration bandwidth used by the team.
* 待确认：Supply-induced jitter simulation flow.
* 待确认：Post-layout extraction requirements.
* 待确认：Jitter tolerance and jitter transfer verification flow.

### Learning Priorities

* 待确认：Which internal documents should be read first.
* 待确认：Which block I will own first.
* 待确认：Which clocking topics are most urgent for the first 90 days.
* 待确认：Who are the key internal experts for PCIe 7.0 clocking, PLL, CDR, and LDO.


---

## 2. Key Concepts

Important clocking concepts:

* reference clock quality
* PLL phase noise and integrated jitter
* VCO / DCO supply sensitivity
* clock divider and buffer noise
* clock distribution skew
* multi-phase clock generation
* phase interpolator linearity
* CDR jitter transfer
* CDR jitter tolerance
* jitter generation
* spread-spectrum clocking support
* supply-induced jitter
* clock-domain isolation between noisy and sensitive blocks

Useful mental model:

```text
PLL creates the clock.
Clock distribution delivers the clock.
CDR positions the clock.
Power integrity protects the clock.
```

---

## 3. Clocking Blocks in a SerDes PHY

A PCIe-class SerDes may include:

* reference clock input path
* clock multiplier PLL
* LC VCO, ring VCO, or DCO depending on architecture
* dividers
* duty-cycle correction
* quadrature or multi-phase generation
* phase interpolators
* TX serializer clock tree
* RX sampling clock tree
* CDR phase detector and loop
* lane-to-lane clock distribution
* test / calibration clocking

待确认: The exact Synopsys implementation is unknown and should be learned from internal documents after onboarding.

---

## 4. Jitter Budget Thinking

Clocking should be viewed through a jitter budget.

Possible contributors:

* reference clock jitter
* PLL in-band noise
* VCO out-of-band noise
* divider jitter
* clock buffer delay noise
* phase interpolator quantization and nonlinearity
* supply-induced jitter
* crosstalk-induced jitter
* CDR jitter generation

Important note:

```text
The relevant number is not just total PLL jitter.
The relevant number is timing error at the sampler or TX launch point after all transfer functions.
```

---

## 5. SerDes / PCIe 7.0 Relevance

PCIe 7.0 uses PAM4, so the receiver has smaller vertical margin than NRZ. Clock jitter adds horizontal eye closure on top of that.

This creates a double sensitivity:

```text
PAM4 smaller vertical eye
+
clock jitter horizontal movement
+
channel ISI
=
reduced link margin
```

Clocking matters for:

* TX launch timing
* RX sampling phase
* CDR lock and tracking
* equalizer adaptation quality
* jitter tolerance compliance
* link training robustness
* retimer / multi-lane timing if relevant

---

## 6. Supply Noise to Clocking

Supply noise can become clock jitter through:

* VCO supply pushing
* DCO delay sensitivity
* clock buffer delay modulation
* phase interpolator delay modulation
* sampler aperture variation
* divider supply sensitivity
* bias current disturbance

Important chain:

```text
LDO residual ripple
down
VCO / clock buffer modulation
down
clock edge movement
down
sampling uncertainty
down
eye closure
```

This is the main bridge between LDO work and PCIe 7.0 clocking work.

---

## 7. CDR Connection

The PLL may create clean clock phases, but the CDR decides where the RX samples incoming data.

Important CDR clocking questions:

* What is the CDR loop bandwidth?
* What jitter is tracked?
* What jitter is rejected?
* How does the phase detector behave under PAM4 ISI?
* Does the CDR use a phase interpolator?
* How is spread-spectrum clocking handled?
* How does equalization affect timing recovery?

In an interview, avoid describing CDR as a standalone block. It must be connected to equalization, jitter tolerance, and sampling margin.

---

## 8. Synopsys Preparation Relevance

For Synopsys preparation, the useful focus is:

* understand clocking as a SerDes system problem
* review PLL phase noise and jitter conversion
* understand CDR jitter transfer / tolerance / generation
* connect LDO PSRR and supply noise to jitter
* prepare questions about actual PCIe 7.0 clocking architecture
* avoid guessing confidential implementation details

Unknown internal details should be marked as `待确认` until verified after joining.

Batch 2 emphasis:

* Treat PCIe 7.0 clocking as a SerDes PHY margin problem, not only a PLL block problem.
* Connect PLL phase noise, CDR transfer / tolerance / generation, equalizer interaction, and LDO supply noise in one timing budget.
* Record the measurement point for any jitter number: PLL output, distributed clock, recovered clock, TX launch clock, or RX sampling clock.
* For onboarding, prepare questions about clock domains, frequency plan, clock distribution, jitter budget allocation, and signoff simulations.

---

## 9. Interview Explanation

Short explanation:

```text
PCIe 7.0 clocking is critical because the link runs at 128 GT/s with PAM4 signaling. PLL phase noise, clock distribution noise, CDR jitter behavior, and supply-induced delay modulation all become sampling uncertainty. That uncertainty closes the eye horizontally, while PAM4 already has reduced vertical margin. So clocking must be analyzed from reference clock through PLL, clock distribution, CDR, and final sampling point.
```

Synopsys-focused explanation:

```text
For PCIe 7.0 clocking work, I would connect PLL jitter, CDR bandwidth, phase interpolator behavior, and LDO supply noise to the SerDes jitter budget. The key is not only producing a high-frequency clock, but ensuring the final sampling and launch clocks meet the link margin requirement across PVT, supply noise, and channel conditions.
```

---

## 10. Common Interview Questions

## Q1: Why is clocking difficult in PCIe 7.0?

Because the UI is very small and PAM4 has reduced vertical margin. Small timing errors can significantly reduce eye margin.

## Q2: What is the difference between PLL jitter and CDR jitter tolerance?

PLL jitter describes clock noise generated by the PLL path. CDR jitter tolerance describes how much input data jitter the receiver can survive while maintaining target BER.

## Q3: How does supply noise create clock jitter?

Supply noise can modulate oscillator frequency, clock buffer delay, phase interpolator delay, or sampler timing.

## Q4: Why does CDR bandwidth matter?

It determines which input phase variations are tracked and which become sampling error.

## Q5: What should be recorded with a jitter number?

Clock frequency, integration bandwidth, RMS or peak-to-peak definition, PVT condition, load condition, and measurement point.

---

## 11. Open Questions

* 待确认: What PCIe 7.0 clocking architecture is used in the relevant Synopsys IP?
* 待确认: What PLL architecture is used?
* 待确认: What are the target clock frequencies and divider ratios?
* 待确认: What integrated jitter budget is allocated to PLL, CDR, and clock distribution?
* 待确认: What CDR architecture is used?
* 待确认: How is spread-spectrum clocking handled?
* Which supplies are most clock-jitter sensitive?
* 待确认: How is supply-induced jitter verified internally?
* 待确认: Which clocking simulations are signoff-critical?

---

## Source Conversations / Source Packets

* `../../00_Inbox/manual_batches/batch2_serdes_pcie_pll_cdr_adc_2026-07-01/source_packet.md`

---

## 12. Related Notes

* `pll_fundamentals.md`
* `cdr_fundamentals.md`
* `phase_noise_jitter.md`
* `../SerDes/pcie7_overview.md`
* `../SerDes/serdes_architecture_overview.md`
* `../LDO_Bandgap/serdes_power_integrity.md`
* `../LDO_Bandgap/ldo_psrr_notes.md`
* `../Study_Plans/synopsys_4_week_prep_plan.md`
* `../../02_Synopsys_Work/synopsys_master_note.md`

---

## 13. Next Actions

1. Add a clocking block diagram after learning the actual architecture.
2. Add jitter budget examples with clear integration bandwidth.
3. Link this note to future clocking interview Q&A.
4. Add Synopsys-specific details only after they are available internally.

---

## Last Updated

2026-07-01
