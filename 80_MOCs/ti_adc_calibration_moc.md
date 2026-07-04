---
title: "MOC: Time-Interleaved ADC Calibration and ADC-Based RX"
domain: "AnalogIC_SerDes"
tags:
  - MOC
  - ADC
  - TimeInterleaving
  - Calibration
  - Jitter
  - PAM4
  - SerDes
created: 2026-07-04
updated: 2026-07-04
source: "Deep Ingest of El-Chammas & Murmann 2012; existing vault notes"
status: "active"
---

# MOC: Time-Interleaved ADC Calibration and ADC-Based RX

中文：这是一张关于"时间交织 ADC 失配、校准与 ADC-based PAM4 接收机"的内容地图（Map of Content）。它不重复各笔记的技术细节，而是说明这些笔记如何连成一条从"采样时序误差 → 失配/jitter → 校准 → 链路 margin"的知识链，并给出建议阅读顺序。核心一手来源是 El-Chammas & Murmann 的 TI-ADC 后台校准专著（见 [[core_serdes_papers]]）。

English: This is a Map of Content for time-interleaved ADC mismatch, calibration, and ADC-based PAM4 receivers. It does not repeat the technical detail in each note; it shows how the notes connect into one chain — sampling-time error → mismatch/jitter → calibration → link margin — and gives a suggested reading order. The cornerstone primary source is El-Chammas & Murmann's monograph on TI-ADC background calibration (see [[core_serdes_papers]]).

## Suggested Reading Order

1. [[adc_based_receiver]] — why ADC-based RX exists; the full chain and ADC requirements.
2. [[pam4_adc_based_rx]] — PAM4-specific margin, resolution vs level spacing, worked examples.
3. [[ti_sar_mismatch_calibration]] — **canonical** TI-SAR ADC note: the four mismatch types, closed-form offset/gain/skew bounds, the cross-correlation background timing-skew calibration algorithm, and the merged practical menu (spur signatures, calibration methods, debug order).
4. [[sampling_jitter_adc]] — sampling/aperture jitter, the quantization-referenced jitter bound, comparator skew.

## Concept Map

中文：这些概念如何相互作用——时序误差（确定性 skew 或随机 jitter）经波形斜率变成电压误差；失配产生 spur；校准（前台/后台）试图恢复精度；但校准会与 CDR、equalizer adaptation、supply/reference 噪声耦合，最终体现在 PAM4 眼图和 BER 上。

English: How the concepts interact — a timing error (deterministic skew or random jitter) becomes a voltage error through waveform slope; mismatch creates spurs; calibration (foreground/background) tries to restore accuracy; but calibration couples to CDR, equalizer adaptation, and supply/reference noise, and ultimately shows up in the PAM4 eye and BER.

```text
sampling-time error (skew, jitter)
      -> voltage error via dV/dt
mismatch (offset / gain / skew / bandwidth)
      -> interleaving spurs, deterministic distortion
calibration (foreground / background cross-correlation)
      -> restores accuracy, but couples to CDR / DSP / supply
outcome: PAM4 vertical+horizontal margin -> BER
```

## Key Source-Backed Results (from Deep Ingest 2026-07-04)

- **Mismatch bounds referenced to quantization SNR** `SNR_Q = (3/2)·2^(2B)` — see [[ti_sar_mismatch_calibration]].
- **Timing skew is signal-statistics dependent** via autocorrelation curvature `R''(0)`; sine analysis over-constrains the budget — see [[ti_sar_mismatch_calibration]] and [[sampling_jitter_adc]].
- **Sub-picosecond skew** is required above ~4 GHz input even for 5-bit resolution → motivates active calibration.
- **Background timing-skew calibration** replaces the unavailable input autocorrelation with cross-correlation against a reference ADC; can use a 1-bit, subsampled comparator that cycles through all slices.
- **Jitter = infinite-interleaving limit of skew** — a clean unification, see [[sampling_jitter_adc]].

## Related Domains

- Clocking that sets the sampling phases: [[pll_phase_noise_jitter]], [[cdr_fundamentals]], [[pcie7_clocking_notes]].
- Supply/reference noise that perturbs calibration: [[serdes_power_integrity]], [[ldo_psrr_notes]].
- Equalization the ADC feeds: [[ctle_ffe_dfe_notes]], [[pam4_receiver_basics]].

## Related Notes

- Master index: [[analog_ic_serdes_master_index]]
- Source anchor: [[core_serdes_papers]]
