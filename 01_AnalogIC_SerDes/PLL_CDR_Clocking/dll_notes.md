---
title: "DLL Notes"
domain: "AnalogIC_SerDes"
tags:
  - DLL
  - Clocking
  - CDR
  - SerDes
  - Jitter
  - PhaseInterpolator
  - DelayLine
  - PCIe7
aliases:
  - dll_notes
  - DLL
  - Delay-Locked Loop
created: 2026-07-05
updated: 2026-07-05
status: "active"
---

# DLL Notes

## 1. Purpose

中文：这篇笔记是 delay-locked loop 的 canonical note，用来组织 DLL、MDLL、VCDL/DCDL、DLL-assisted CDR、phase generation、deskew、clock distribution、jitter filtering 和 delay-line calibration。它和 [[pll_fundamentals]] 的区别是：PLL 通过 oscillator integration 生成或恢复 frequency/phase；DLL 通过可控 delay line 对已有 clock/data edge 进行 phase alignment。

English: This is the canonical note for delay-locked loops. It organizes DLLs, MDLLs, VCDLs/DCDLs, DLL-assisted CDRs, phase generation, deskew, clock distribution, jitter filtering, and delay-line calibration. Its distinction from [[pll_fundamentals]] is that a PLL generates or recovers frequency/phase through oscillator integration, while a DLL aligns the phase of an existing clock/data edge through a controllable delay line.

## 2. Basic Architecture

```text
Input clock
  -> controllable delay line
  -> delayed clock
  -> phase detector
  -> charge pump / digital loop filter
  -> delay control
```

中文：DLL 的 loop 通常把 delay-line output edge 对齐到 input/reference edge。因为 delay line 不是自由振荡器，DLL 没有 VCO phase integration，因此不会像 Type-II PLL 那样自然累积 frequency error correction。它更适合 deskew、multi-phase generation、clock distribution alignment 和 bounded phase tracking。

English: A DLL loop usually aligns the delay-line output edge to the input/reference edge. Because the delay line is not a free-running oscillator, a DLL does not have VCO phase integration and does not naturally accumulate frequency-error correction like a Type-II PLL. It is better suited to deskew, multiphase generation, clock-distribution alignment, and bounded phase tracking.

## 3. DLL Versus PLL

| Topic | DLL | PLL |
|---|---|---|
| Controlled element | Delay line | Oscillator |
| Frequency generation | No new average frequency | Can multiply or synthesize frequency |
| Accumulated phase noise | Usually bounded by delay path | Oscillator phase noise accumulates |
| Frequency offset tracking | Limited by delay range | Natural through oscillator control |
| Typical use | Deskew, phase generation, CDR assist | Clock synthesis, CDR, jitter filtering |
| Main risk | Delay range, PVT, jitter transfer, false lock | VCO noise, stability, spur, lock time |

中文：DLL 的优势是没有 free-running oscillator phase-noise accumulation，因此在 clock deskew 和 phase generation 中可以很干净。缺点是 delay range 有限；如果输入和目标 clock 存在持续 frequency offset，DLL control 会跑到边界，无法像 PLL 那样长期吸收 offset。

English: The DLL advantage is that it avoids free-running oscillator phase-noise accumulation, so it can be clean for clock deskew and phase generation. The drawback is limited delay range; if input and target clock have persistent frequency offset, DLL control can run to the boundary and cannot absorb offset indefinitely like a PLL.

## 4. Delay Line Choices

中文：VCDL 使用 analog voltage 控制 delay，通常有平滑调节和较低 quantization artifact，但更容易受 supply noise、control noise、PVT drift 和 analog loop stability 影响。DCDL 使用 digital code 控制 delay，便于 calibration、scan、repeatability 和 digital control，但会引入 delay LSB quantization、code-dependent INL 和 switching spur。

English: A VCDL uses analog voltage to control delay and often provides smooth tuning with low quantization artifact, but it is more sensitive to supply noise, control noise, PVT drift, and analog-loop stability. A DCDL uses digital code to control delay, which helps calibration, scan, repeatability, and digital control, but introduces delay-LSB quantization, code-dependent INL, and switching spurs.

中文：delay line 的每一级都可能把 supply noise 转换成 timing noise。对 SerDes clocking，VCDL/DCDL 不应只看 total delay range；还要看 delay sensitivity、duty-cycle distortion、edge slew degradation、phase spacing mismatch 和 clock-tree loading。

English: Each delay-line stage can convert supply noise into timing noise. For SerDes clocking, VCDL/DCDL review should not look only at total delay range; it must also check delay sensitivity, duty-cycle distortion, edge-slew degradation, phase-spacing mismatch, and clock-tree loading.

## 5. Phase Generation and Deskew

中文：DLL 常用于生成多相 clock。若一个 reference period 被分成 $M$ 个 phase tap，ideal phase spacing 为：

English: DLLs are often used to generate multiphase clocks. If one reference period is divided into $M$ phase taps, the ideal phase spacing is:

$$
\Delta t=\frac{T_{ref}}{M}
$$

or:

$$
\Delta\phi=\frac{2\pi}{M}
$$

中文：真正的误差来自 delay-cell mismatch、edge loading、routing skew、tap buffer mismatch、supply gradient 和 duty-cycle distortion。多相 clock 用于 phase interpolator、serializer、deserializer 或 ADC sampling 时，tap mismatch 会变成 deterministic jitter 或 sampling skew。

English: Real error comes from delay-cell mismatch, edge loading, routing skew, tap-buffer mismatch, supply gradient, and duty-cycle distortion. When multiphase clocks feed a phase interpolator, serializer, deserializer, or ADC sampler, tap mismatch becomes deterministic jitter or sampling skew.

## 6. DLL-Assisted CDR

中文：DLL-assisted CDR 的价值是把 tracking path 和 oscillator path 分开。PLL 可以提供 average frequency 和 low-jitter base clock，DLL/VCDL 可以提供 bounded phase tracking 或 data-aligned delay correction。这样有机会把 jitter transfer bandwidth 和 jitter tolerance bandwidth 部分分离。

English: The value of a DLL-assisted CDR is separating the tracking path from the oscillator path. A PLL can provide average frequency and a low-jitter base clock, while a DLL/VCDL provides bounded phase tracking or data-aligned delay correction. This can partially separate jitter-transfer bandwidth from jitter-tolerance bandwidth.

From the CDR note:

$$
H_{JTRAN}(s)=
\frac{1}
{s^2C/(K_dK_v)+sK_{vd}/K_v+1}
$$

For an overdamped D/PLL approximation:

$$
\omega_{PL}\approx\frac{K_v}{K_{vd}}
$$

$$
\omega_{PH}\approx\frac{K_{vd}K_d}{C}
$$

中文：这些公式的直觉是：一个 pole 可设定较窄 jitter transfer，另一个 pole 可帮助较宽 tracking/tolerance。实际设计必须同时检查 VCDL range、linearity、power、ISI if data is delayed、PVT calibration 和 phase-detector noise。

English: The intuition is that one pole can set narrow jitter transfer while the other helps wider tracking/tolerance. A real design must also check VCDL range, linearity, power, ISI if data is delayed, PVT calibration, and phase-detector noise.

## 7. MDLL and Multiplying DLL

中文：MDLL 或 multiplying DLL 用 reference edge 周期性刷新 oscillator/delay-domain phase，以降低 accumulated oscillator jitter。它可以把 PLL 和 DLL 的优点混合：利用 clean reference edge reset phase error，同时用 oscillator/delay path 产生高频 clock。代价是 reference spur、edge injection disturbance、multiplying ratio constraints、duty-cycle sensitivity 和 injection timing calibration。

English: An MDLL or multiplying DLL periodically refreshes oscillator/delay-domain phase with a reference edge to reduce accumulated oscillator jitter. It can mix PLL and DLL advantages: use a clean reference edge to reset phase error while using an oscillator/delay path to generate a high-frequency clock. The costs are reference spur, edge-injection disturbance, multiplication-ratio constraints, duty-cycle sensitivity, and injection-timing calibration.

## 8. Common Mistakes

中文：常见错误一是把 DLL 当成可以无限 tracking frequency offset 的 PLL。DLL 只有有限 delay range，持续 frequency offset 会把 control code 推到边界。

English: A common mistake is treating a DLL as a PLL that can track frequency offset indefinitely. A DLL has finite delay range, so persistent frequency offset pushes the control code to the boundary.

中文：常见错误二是只检查 lock，而不检查 wrong-lock 或 harmonic-lock condition。DLL 对一个 period 的 integer ambiguity、edge polarity、duty cycle 和 reset/startup sequence 敏感。

English: A second common mistake is checking lock but not wrong-lock or harmonic-lock conditions. A DLL is sensitive to integer-period ambiguity, edge polarity, duty cycle, and reset/startup sequence.

中文：常见错误三是忽略 delay-line supply sensitivity。delay cell 本质上是 time-domain analog element；即使 loop control 是 digital，supply noise 仍会直接调制 edge timing。

English: A third common mistake is ignoring delay-line supply sensitivity. A delay cell is a time-domain analog element; even if loop control is digital, supply noise still directly modulates edge timing.

## 9. Design Review Checklist

- What is the required delay range across PVT?
- Is the lock point unique, or can the DLL false-lock to another edge?
- What is delay LSB or analog delay sensitivity?
- How much supply noise converts to time jitter through the delay line?
- Are duty-cycle distortion and edge slew preserved through the delay path?
- Are phase taps matched after routing and buffering?
- Does the DLL need startup, reset, or coarse-lock assistance?
- If used in CDR, what are JTRAN, JTOL, and JGEN implications?
- If used as MDLL, how are reference spur and injection disturbance controlled?

## 10. Related Notes

- [[cdr_fundamentals]]
- [[pll_fundamentals]]
- [[pll_phase_noise_jitter]]
- [[clock_distribution_jitter]]
- [[phase_interpolator]]
- [[adpll_notes]]
- [[pcie7_clocking_notes]]

## 11. Source Provenance

| Source | Type | Reusable knowledge |
|---|---|---|
| Woogeun Rhee and Zhiping Yu, *Phase-Locked Loops: System Perspectives and Circuit Design Aspects*, Wiley/IEEE Press, 2024 | Book | DLL-assisted CDR, D/PLL jitter-transfer intuition, PLL architecture taxonomy |
| Existing CDR canonical note | Vault synthesis | JGEN/JTRAN/JTOL framing and DLL-assisted CDR tradeoffs |

