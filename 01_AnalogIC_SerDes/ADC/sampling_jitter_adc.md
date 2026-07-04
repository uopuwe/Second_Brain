---
title: "Sampling Jitter in ADCs"
domain: "AnalogIC_SerDes"
tags:
  - ADC
  - SamplingJitter
  - Clocking
  - SNDR
  - SerDes
  - PAM4
  - PLL
  - Synopsys
created: 2026-07-01
updated: 2026-07-01
source: "ChatGPT technical notes and Synopsys role preparation"
status: "active"
---

# Sampling Jitter in ADCs

## 中文补充翻译

这篇笔记解释 ADC sampling jitter 为什么会限制高速输入下的 SNDR。采样瞬间如果有时间误差，输入波形会因为局部斜率被采在错误电压上，因此 timing error 会转化为 voltage error。

核心关系是：输入频率越高、波形斜率越大、采样 jitter 越大，jitter-induced noise 越严重。常用近似公式是 `SNR_jitter = -20log10(2*pi*f_in*sigma_t)`，它说明在 GHz 到 tens of GHz 的 SerDes / PAM4 receiver 中，即使几十到几百 fs 的 jitter 也可能成为硬限制。

这类 jitter 不一定能靠数字校准消除。随机 aperture jitter 是采样瞬间的不确定性，DSP 只能处理已经采错的样本。TI-ADC 的静态 skew 可以校准，动态 skew、supply-induced skew 和 clock distribution mismatch 则需要通过 clocking、layout、supply isolation 和 calibration 一起控制。

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
* `../ADC_TI_SAR/ti_sar_mismatch_calibration.md`
* `../PLL_CDR_Clocking/pll_phase_noise_jitter.md`
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

## 14. Batch 1 Extracted Knowledge - 2026-07-02

### 14.1 Aperture Jitter Formula

For a sine input, sampling-time error converts to voltage error:

```text
x(t) = A*sin(2*pi*f_in*t)
e(t) ~= Delta t * dx/dt
SNR_jitter ~= -20*log10(2*pi*f_in*sigma_t)
```

Design implications:

- Jitter sensitivity increases directly with input frequency.
- ADC ENOB can be jitter-limited even when quantization noise is acceptable.
- Random aperture jitter raises the noise floor and is not removed by deterministic skew calibration.

### 14.2 Deterministic Skew vs Random Jitter

For repeated edge measurements:

```text
t_i = t_ideal_i + Delta t_i + j_i
mean(t_i - t_ideal_i) -> deterministic skew estimate
std(t_i - t_ideal_i) -> random jitter estimate
sigma_mean = sigma_j / sqrt(N)
```

Use many samples to estimate deterministic skew below the single-shot random jitter floor.

### 14.3 TI-ADC Skew Example

For `f_s = 8 GS/s` and `M = 8`:

```text
T_s = 125 ps
sub-ADC spacing = 125 ps / 8 = 15.625 ps
```

A deterministic skew of hundreds of femtoseconds is small relative to the sub-ADC spacing, but large enough to create high-frequency mismatch spurs and degrade SFDR.

### 14.4 Source Conversations

- `../../00_Inbox/raw_chat_exports/chatgpt_export_2026-07-01/md_by_conversation/2026-05-13__SerDes_PLL_CDR_带宽.md`
- `../../00_Inbox/raw_chat_exports/chatgpt_export_2026-07-01/md_by_conversation/2026-05-24__高速TI-ADC时钟偏移.md`

---

## 15. Deep Ingest 2026-07-04: Quantization-Referenced Jitter Bound

Source: El-Chammas & Murmann, *Background Calibration of Time-Interleaved Data Converters*, Springer 2012 (see [[core_serdes_papers]]; archived under `../../90_Archive/processed/2026/books/`). This complements the existing `-20log10(2π f_in σ_t)` relation with a bound referenced to quantization noise, and unifies jitter with timing skew.

### 15.1 Jitter as the Infinite-Interleaving Limit of Timing Skew

中文：本书给出一个漂亮的统一视角：随机采样 jitter 可以看作"通道数趋于无穷"的 TI-ADC timing skew——每个样本都用一个独立随机相位采一次，等价于每个"子 ADC"只采一次、且有随机 skew。于是 skew 的方差界在 `N → ∞` 取极限，就得到 jitter 的容许界。它与输入信号统计通过自相关曲率 `R''(0)` 相关，而不仅仅是单一频率。

English: The book gives an elegant unification: random sampling jitter is the `N → ∞` limit of TI-ADC timing skew — each sample is taken once at an independent random phase, as if every "sub-ADC" samples exactly once with a random skew. Taking the skew-variance bound to `N → ∞` therefore yields the tolerable-jitter bound, tied to the input statistics through the autocorrelation curvature `R''(0)`, not merely a single frequency.

For an ADC of resolution `B` bits, the tolerable RMS sampling jitter to stay at or above the quantization floor is:

$$
\sigma^2 \;\le\; \frac{2}{3\cdot 2^{2B}\,\lvert R''(0)\rvert}
$$

where `R''(0)` is the curvature of the input autocorrelation at zero lag (V²/s²). For a sine input, `R''(0) = -(2π f_in)²`, so this reduces to the familiar sine result:

$$
\sigma^2 \;\le\; \frac{2}{3\cdot 2^{2B}\,(2\pi f_{in})^2}
$$

中文：注意这与前面 `-20log10(2π f_in σ_t)` 是一致的——后者说的是 jitter 限制下的 SNR，前者说的是"要让 jitter 噪声不超过量化噪声"所允许的 σ。两者都表明高频、高 σ 更糟。用宽带信号的真实 `R''(0)`（而非最坏正弦 `f_in`）来定 jitter 预算，通常会得到更宽松、更真实的要求。

English: This is consistent with the earlier `-20log10(2π f_in σ_t)` relation — that one gives the jitter-limited SNR, while this one gives the σ allowed for jitter noise to stay under quantization noise. Both say higher frequency and higher σ are worse. Budgeting jitter against a broadband signal's true `R''(0)` (rather than the worst-case sine `f_in`) generally yields a looser, more realistic requirement; the sine assumption over-constrains by up to 3× for a brick-wall-band-limited input.

### 15.2 Comparator / Latch Skew Without a Track-and-Hold

中文：附录 D 分析了 flash ADC 中比较器 latch 时刻的 skew（来自时钟分布和比较器晶体管失配）。它与随机 jitter 一样，误差正比于信号斜率。对无限分辨率、方差为 `σ_α²` 的比较器 skew，正弦输入下的 SNR 为 `SNR = 1/(2π f_in σ_α)²`。书中例子：10 GHz 输入、仅 2 ps 比较器 skew，ENOB 已跌到 3 bit 以下——这正是高速下必须用前端 track-and-hold 的原因：T/H 把输入保持住，使后面比较器的采样时刻 skew 几乎无害。

English: Appendix D analyzes comparator latch-time skew in a flash ADC (from clock distribution and comparator transistor mismatch). Like random jitter, its error is proportional to signal slope. For an infinite-resolution ADC with comparator-skew variance `σ_α²` and a sine input, the SNR is:

$$
\mathrm{SNR} = \frac{1}{(2\pi f_{in}\,\sigma_\alpha)^2}
$$

The book's example: a 10 GHz input with only 2 ps of comparator skew drops ENOB below 3 bits. This is precisely why a front-end track-and-hold is important at high speed — the T/H holds the input constant so that skew in the following comparators' sampling instants becomes nearly harmless.

### 15.3 Separating Deterministic Skew From Random Jitter in Measurements

中文：残余确定性 skew 可以从 skew spur 的复幅度用伪逆法反解（见 [[ti_sar_mismatch_calibration]] 的 Appendix E 部分）。去掉 skew 谱线后，SNR 随输入频率的额外下降就只归因于随机 jitter，从而把二者分开估计。低频段用来标定量化+热噪声底，因为那里 jitter 和 skew 影响可忽略。

English: Residual deterministic skew can be back-solved from the complex magnitudes of the skew spurs via a pseudo-inverse (see the Appendix E discussion in [[ti_sar_mismatch_calibration]]). After removing the skew spurs, any SNR degradation that grows with input frequency is attributed to random jitter, separating the two. Low-frequency inputs calibrate the quantization-plus-thermal noise floor, where jitter and skew are negligible.

### 15.4 Source

- El-Chammas & Murmann, Springer 2012, Ch. 2 (Eq. for jitter bound) and Appendices D–E. Formulas dimensionally checked; jitter/skew unification reproduced. See [[ti_sar_mismatch_calibration]] for the companion timing-skew bounds and background-calibration algorithm.

---

## Last Updated

2026-07-04
