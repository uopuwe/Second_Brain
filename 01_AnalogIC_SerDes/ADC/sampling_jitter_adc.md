---

title: "Sampling Jitter in ADCs"
domain: "AnalogIC_SerDes"
tags:

* ADC
* SamplingJitter
* Clocking
* SNDR
* SerDes
* PAM4
* PLL
* Synopsys
  created: 2026-07-01
  updated: 2026-07-01
  source: "ChatGPT technical notes and Synopsys role preparation"
  status: "active"

---

# Sampling Jitter in ADCs

## Purpose

This note summarizes how sampling jitter affects ADC performance, especially in ADC-based SerDes receivers.

The goal is to connect clock phase noise, sampling aperture uncertainty, SNDR degradation, PAM4 receiver margin, and LDO supply noise.

---

## 1. Big Picture

An ADC should sample the input at a precise time.

If the sampling instant moves, the sampled voltage is wrong.

Core chain:

```text
clock jitter
down
sampling time error
down
voltage sample error
down
SNDR degradation
down
receiver margin loss
```

Sampling jitter is more damaging when the input signal changes quickly.

---

## 2. Key Concepts

Important concepts:

* aperture jitter
* sampling clock jitter
* input slope
* phase noise
* integrated RMS jitter
* SNDR
* ENOB
* jitter-limited SNR
* ADC front-end bandwidth
* time-interleaving skew
* PLL phase noise
* clock buffer delay noise
* supply-induced jitter

Useful relation:

```text
voltage error = input slope x time error
```

---

## 3. Jitter-Limited SNR

For a sinusoidal input, a common approximation is:

```text
SNR_jitter = -20 log10(2 pi fin sigma_t)
```

where:

* `fin` is input frequency
* `sigma_t` is RMS sampling jitter

This shows why high-frequency inputs are more sensitive to jitter.

If `fin` doubles, jitter-limited SNR gets worse.

---

## 4. Phase Noise Connection

Sampling clock jitter comes from phase noise and other timing disturbances.

Clock path contributors:

* PLL phase noise
* VCO / DCO noise
* divider noise
* phase interpolator noise
* clock buffer noise
* supply-induced delay modulation
* crosstalk

Phase noise must be integrated over the relevant frequency range to estimate RMS jitter.

Important warning:

```text
A jitter number without integration bandwidth is incomplete.
```

---

## 5. Supply Noise Connection

Supply noise can create sampling jitter through:

* PLL supply pushing
* clock buffer delay modulation
* sampler switch timing variation
* comparator delay variation
* phase interpolator delay modulation

Chain:

```text
finite LDO PSRR
down
clock supply ripple
down
delay or frequency modulation
down
sampling jitter
down
ADC error
```

This connects ADC performance directly to LDO and power integrity.

---

## 6. Time-Interleaving vs Jitter

In time-interleaved ADCs, deterministic sampling phase errors appear as timing skew.

Random sampling uncertainty appears as jitter.

Both create voltage error:

```text
timing error
down
wrong sample voltage
```

But calibration handles them differently:

* static skew may be calibrated
* random jitter cannot be fully calibrated after the fact
* supply-induced deterministic jitter may require clock / supply fixes

---

## 7. SerDes / PCIe 7.0 Relevance

ADC-based PAM4 receivers are sensitive to sampling jitter because the input bandwidth is high and PAM4 levels have small spacing.

Jitter affects:

* ADC SNDR
* digital equalizer input quality
* CDR timing error detection
* PAM4 level decisions
* BER margin

For PCIe 7.0 preparation, sampling jitter is the bridge between PLL clocking and ADC-based receiver performance.

---

## 8. Synopsys Preparation Relevance

Useful preparation focus:

* explain jitter-limited SNR
* connect phase noise integration to ADC sampling jitter
* connect LDO PSRR to supply-induced clock jitter
* understand why high input frequency makes jitter worse
* avoid claiming actual Synopsys ADC jitter budgets before seeing internal data

Batch 2 emphasis:

* Sampling jitter is the direct bridge between PCIe 7.0 clocking / PLL phase noise and ADC-based PAM4 receiver performance.
* Static TI-ADC skew may be calibrated, but random aperture jitter becomes noise-like sample error and cannot be fully removed after conversion.
* Always connect a sampling-jitter number to input frequency, clock path, integration bandwidth, and receiver margin target.

---

## 9. Interview Explanation

Short explanation:

```text
Sampling jitter is uncertainty in the ADC sampling instant. If the input signal has a slope, a timing error becomes a voltage error. For a sinusoidal input, jitter-limited SNR is approximately -20log10(2*pi*fin*sigma_t), so higher input frequency and larger RMS jitter reduce SNDR. In ADC-based SerDes receivers, sampling jitter reduces the quality of the digitized PAM4 waveform and can hurt equalization, CDR, and BER.
```

Synopsys-focused explanation:

```text
For PCIe 7.0 SerDes preparation, sampling jitter connects PLL, CDR, LDO, and ADC topics. PLL phase noise and supply-induced clock delay modulation create sampling jitter, while PAM4 receiver margin depends on accurate sampled amplitude. So clocking and power integrity directly affect ADC-based RX performance.
```

---

## 10. Common Interview Questions

## Q1: What is sampling jitter?

Uncertainty in the exact time at which the ADC samples the input.

## Q2: Why does jitter create voltage error?

Because if the input is changing with time, sampling early or late gives a different voltage.

## Q3: What is the jitter-limited SNR equation?

`SNR_jitter = -20 log10(2 pi fin sigma_t)` for a sinusoidal input.

## Q4: Why is jitter worse at high input frequency?

Higher-frequency signals have larger slopes, so the same timing error creates larger voltage error.

## Q5: Can random sampling jitter be calibrated out?

Not fully. Static timing skew may be calibrated, but random jitter is a noise process.

---

## 11. Open Questions

* 待确认: What sampling jitter budget is used for Synopsys PCIe 7.0 RX?
* 待确认: What clock phase noise integration range is relevant for ADC-based RX?
* 待确认: Which clock path dominates sampling jitter?
* 待确认: How much jitter comes from PLL vs clock distribution vs supply noise?
* 待确认: How is supply-induced ADC jitter simulated?
* 待确认: What SNDR or EVM target is required for PAM4 receiver margin?
* 待确认: How does CDR loop behavior affect sampling jitter interpretation?

---

## Source Conversations / Source Packets

* `../../00_Inbox/manual_batches/batch2_serdes_pcie_pll_cdr_adc_2026-07-01/source_packet.md`

---

## 12. Related Notes

* `adc_based_receiver.md`
* `ti_sar_adc_calibration.md`
* `../PLL_CDR_Clocking/phase_noise_jitter.md`
* `../PLL_CDR_Clocking/pll_fundamentals.md`
* `../PLL_CDR_Clocking/pcie7_clocking_notes.md`
* `../SerDes/pam4_receiver_basics.md`
* `../LDO_Bandgap/serdes_power_integrity.md`
* `../Study_Plans/synopsys_4_week_prep_plan.md`

---

## 13. Next Actions

1. Add numeric examples for jitter-limited SNR.
2. Link this note to future ADC interview Q&A.
3. Add phase noise integration examples later.
4. Add Synopsys-specific budgets only after onboarding.

---

## Last Updated

2026-07-01
