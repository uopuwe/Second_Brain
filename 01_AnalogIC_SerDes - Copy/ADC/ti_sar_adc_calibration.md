---

title: "TI-SAR ADC Calibration"
domain: "AnalogIC_SerDes"
tags:

* ADC
* SAR
* TimeInterleaving
* Calibration
* PAM4
* SerDes
* Receiver
* Synopsys
  created: 2026-07-01
  updated: 2026-07-01
  source: "ChatGPT technical notes and Synopsys role preparation"
  status: "active"

---

# TI-SAR ADC Calibration

## 中文补充翻译

这篇笔记总结 time-interleaved SAR ADC 的 mismatch 和 calibration。TI-SAR ADC 用多个较低速 SAR 通道交错采样来实现更高总采样率，但每个子 ADC 的 offset、gain、timing skew 和 bandwidth mismatch 都会在输出中形成 spur、distortion 或 noise floor。

Offset mismatch 会造成通道间固定偏移；gain mismatch 会让不同 sub-ADC 对同一输入的幅度响应不同；timing skew 会在高频输入下把时间误差转成电压误差，通常最难处理；bandwidth mismatch 会导致频率相关误差。foreground calibration 适合启动或空闲时校准，background calibration 则在正常工作中持续追踪漂移，但设计更复杂。

对 PCIe 7.0 / PAM4 ADC-based RX 来说，TI-SAR calibration 不只是 ADC 内部问题。采样时钟、PLL jitter、CDR phase、LDO noise、reference stability 和 DSP equalization 都会影响最终 link margin。

## Purpose

This note summarizes time-interleaved SAR ADC calibration topics relevant to ADC-based SerDes receivers.

The goal is to understand offset, gain, timing skew, and bandwidth mismatch, and how calibration connects to PAM4 receiver margin.

---

## 1. Big Picture

High-speed ADCs often use time interleaving to reach a sample rate beyond what one ADC slice can handle.

Basic structure:

```text
Input signal
down
sample clock phases
down
SAR ADC slice 0
SAR ADC slice 1
SAR ADC slice 2
SAR ADC slice 3
down
digital recombination
```

The problem is that no two slices are perfectly identical.

Mismatch creates tones, noise, distortion, and receiver decision errors.

---

## 2. Key Concepts

Important concepts:

* SAR ADC
* time interleaving
* offset mismatch
* gain mismatch
* timing skew
* bandwidth mismatch
* capacitor DAC mismatch
* comparator offset
* reference mismatch
* sample clock phase error
* background calibration
* foreground calibration
* convergence
* adaptation stability
* digital correction

Calibration tries to make multiple imperfect ADC slices behave like one cleaner high-speed ADC.

---

## 3. Offset Mismatch

Offset mismatch means each ADC slice has a different output offset.

Effect:

```text
slice-dependent DC error
down
periodic output pattern
down
interleaving spur
```

In a PAM4 receiver, offset mismatch can shift digitized levels and decision thresholds.

Correction:

* estimate average error per slice
* subtract digital offset
* calibrate comparator or DAC offset if supported

---

## 4. Gain Mismatch

Gain mismatch means each slice has a different conversion gain.

Effect:

```text
same input amplitude
down
different digital output scale per slice
down
amplitude modulation / spur
```

In PAM4, gain mismatch changes level spacing depending on sample phase.

Correction:

* estimate slice gain
* apply digital scaling
* calibrate reference or capacitor DAC if possible

---

## 5. Timing Skew

Timing skew means slices sample at slightly wrong times.

This is often the most difficult mismatch at high input frequency.

Approximate error:

```text
voltage error = input slope x timing error
```

So the error increases when:

* input frequency is high
* signal slope is high
* timing skew is large

In SerDes, timing skew directly damages sampled waveform accuracy and can hurt equalization and CDR.

---

## 6. Bandwidth Mismatch

Bandwidth mismatch means slices have different frequency responses.

It can be caused by:

* sampling switch resistance mismatch
* input capacitance mismatch
* routing parasitics
* buffer mismatch
* clock path mismatch

This is harder than simple gain mismatch because the error depends on frequency.

---

## 7. Calibration Approaches

Calibration can be:

## Foreground Calibration

Runs during startup or test mode.

Pros:

* easier to control
* can use known input patterns
* simpler estimation

Cons:

* cannot track drift during normal operation
* may interrupt data path

## Background Calibration

Runs while normal data is active.

Pros:

* tracks temperature, voltage, and aging drift
* supports long-term operation

Cons:

* algorithm complexity
* convergence risk
* interaction with data and equalization
* possible adaptation noise

---

## 8. SerDes / PCIe 7.0 Relevance

ADC-based PAM4 receivers may require time-interleaved ADCs because the sampling rates are extremely high.

Calibration matters because:

* PAM4 vertical margin is small
* ADC errors reduce digital equalization accuracy
* timing skew appears as signal-dependent error
* slice mismatch can create spurs and deterministic distortion
* calibration errors can degrade BER

Even if the actual PCIe 7.0 RX architecture is unknown, TI-ADC calibration is a useful preparation topic for advanced SerDes.

---

## 9. Synopsys Preparation Relevance

For Synopsys preparation:

* know the four main TI-ADC mismatch categories
* explain why timing skew is especially harmful
* connect calibration to PAM4 receiver margin
* connect clock phase quality to ADC accuracy
* connect LDO / reference noise to calibration stability
* mark actual internal calibration architecture as unknown

Batch 2 emphasis:

* Prior discussion included 4-way, 8-way, and 16-way TI-SAR examples; treat exact project details and any Synopsys usage as `待确认`.
* Offset and gain mismatch mainly create slice-dependent amplitude errors; timing skew creates slope-dependent error and becomes more harmful as input frequency rises.
* Background calibration can track drift during operation, but it must not destabilize receiver equalization, CDR, or decision-directed adaptation.

---

## 10. Interview Explanation

Short explanation:

```text
A time-interleaved SAR ADC uses multiple ADC slices sampling at staggered phases to achieve a higher effective sample rate. The main issue is mismatch between slices: offset mismatch creates slice-dependent DC error, gain mismatch creates amplitude scaling error, timing skew creates slope-dependent sampling error, and bandwidth mismatch creates frequency-dependent error. Calibration estimates and corrects these errors, often digitally, but background calibration must be stable and must not corrupt the receiver adaptation loops.
```

Synopsys-focused explanation:

```text
For ADC-based PAM4 SerDes, TI-ADC calibration is important because slice mismatch directly reduces amplitude accuracy and link margin. Timing skew also connects strongly to clocking, because phase errors between ADC sampling clocks become voltage errors at high input slopes. This connects ADC, PLL, CDR, LDO, and calibration work.
```

---

## 11. Common Interview Questions

## Q1: Why use time interleaving?

To achieve a higher effective sample rate than a single ADC slice can support.

## Q2: What are the main TI-ADC mismatch types?

Offset, gain, timing skew, and bandwidth mismatch.

## Q3: Why is timing skew especially harmful?

It creates a voltage error proportional to input slope, so it becomes worse at high frequency.

## Q4: What is foreground calibration?

Calibration performed during startup or test mode, often with known signals.

## Q5: What is background calibration?

Calibration running during normal operation to track drift without stopping the data path.

---

## 12. Open Questions

* 待确认: Does the relevant Synopsys receiver use a time-interleaved ADC?
* 待确认: If yes, is it SAR, flash, pipeline, or another architecture?
* 待确认: How many interleaved slices are used?
* 待确认: Which mismatch sources dominate?
* 待确认: What calibration is foreground vs background?
* 待确认: How is timing skew detected?
* 待确认: How is calibration stability verified?
* 待确认: How does calibration interact with equalization and CDR?
* 待确认: What supply and reference noise limits are needed for calibration accuracy?

---

## Source Conversations / Source Packets

* `../../00_Inbox/manual_batches/batch2_serdes_pcie_pll_cdr_adc_2026-07-01/source_packet.md`

---

## 13. Related Notes

* `adc_based_receiver.md`
* `sampling_jitter_adc.md`
* `../SerDes/pam4_receiver_basics.md`
* `../SerDes/ctle_ffe_dfe_notes.md`
* `../PLL_CDR_Clocking/pll_phase_noise_jitter.md`
* `../PLL_CDR_Clocking/cdr_fundamentals.md`
* `../LDO_Bandgap/serdes_power_integrity.md`
* `../Study_Plans/synopsys_4_week_prep_plan.md`

---

## 14. Next Actions

1. Add equations for offset / gain / skew spur locations later.
2. Add one example of timing skew error vs input frequency.
3. Add references to ADC-based receiver papers.
4. Add personal ADC project connections in the technical story bank.

---

## Last Updated

2026-07-01
