---
title: "Fractional-N and Digital PLL"
domain: "AnalogIC_SerDes"
tags:
  - PLL
  - FractionalN
  - DeltaSigma
  - DSM
  - DPLL
  - ADPLL
  - BBPLL
  - TDC
  - DCO
  - SerDes
  - Clocking
aliases:
  - pll_fractional_n_digital
  - Fractional-N PLL
  - Digital PLL
  - ADPLL
created: 2026-07-05
updated: 2026-07-05
source: "Deep Ingest of Rhee and Yu, Phase-Locked Loops, Wiley/IEEE Press, 2024"
status: "active"
---

# Fractional-N and Digital PLL

## 1. Purpose and Scope

中文：这篇笔记是 fractional-N PLL、delta-sigma modulation、digital PLL、bang-bang DPLL 和 hybrid PLL 的 canonical note。它承接需要细频率分辨率、digital-intensive clocking、DCO/TDC modeling、fractional spur control 和 DSM quantization-noise shaping 的资料。它不替代 [[pll_fundamentals]]，而是把 integer-N CPPLL 之外的 architecture-specific 知识集中管理。

English: This is the canonical note for fractional-N PLLs, delta-sigma modulation, digital PLLs, bang-bang DPLLs, and hybrid PLLs. It captures sources that involve fine frequency resolution, digital-intensive clocking, DCO/TDC modeling, fractional-spur control, and DSM quantization-noise shaping. It does not replace [[pll_fundamentals]]; it centralizes architecture-specific knowledge beyond integer-N CPPLL behavior.

中文：本笔记适用于 SerDes/PCIe clock synthesis、spread-spectrum clocking、multi-rate PHY frequency planning、wireless-style synthesizer intuition、digital calibration-heavy PLL 和 interview preparation。PFD/CP 的具体非理想性归入 [[pfd_charge_pump_notes]]，phase-noise and jitter conversion 归入 [[pll_phase_noise_jitter]]，CDR-specific BBPD loop behavior 归入 [[cdr_fundamentals]]。

English: This note applies to SerDes/PCIe clock synthesis, spread-spectrum clocking, multi-rate PHY frequency planning, wireless-synthesizer intuition, calibration-heavy digital PLLs, and interview preparation. Detailed PFD/CP nonidealities belong in [[pfd_charge_pump_notes]], phase-noise and jitter conversion belongs in [[pll_phase_noise_jitter]], and CDR-specific BBPD loop behavior belongs in [[cdr_fundamentals]].

## 2. Canonical Role and Merge Policy

中文：当新资料讨论 fractional divider、DSM order、MASH、integer-boundary spur、DTC compensation、multi-phase fractional division、TDC quantization、DCO quantization、BBPLL limit cycle、ADPLL loop filter 或 hybrid PLL 时，默认 merge 到这篇 note。不要新建 `fractional_pll_notes.md`、`adpll_notes.md` 或 `dpll_basics.md`，除非资料是具体 paper summary 或 project note，并且该文件明确链接回这里。

English: When a new source discusses fractional dividers, DSM order, MASH, integer-boundary spur, DTC compensation, multi-phase fractional division, TDC quantization, DCO quantization, BBPLL limit cycle, ADPLL loop filters, or hybrid PLLs, the default destination is this note. Do not create `fractional_pll_notes.md`, `adpll_notes.md`, or `dpll_basics.md` unless the source is a concrete paper summary or project note that links back here.

## 3. Fractional-N PLL Problem Statement

中文：integer-N PLL 的输出频率通常为 $f_{out}=Nf_{ref}$，频率分辨率被 reference frequency 限制。fractional-N PLL 通过在相邻 divider modulus 之间切换，使平均 divider ratio 等于 $N+\alpha$，从而得到更细频率分辨率：

English: In an integer-N PLL, the output frequency is usually $f_{out}=Nf_{ref}$, so frequency resolution is limited by the reference frequency. A fractional-N PLL switches between adjacent divider moduli so that the average divider ratio is $N+\alpha$, producing finer frequency resolution:

$$
f_{out}=(N+\alpha)f_{ref}
$$

中文：核心问题是 divider ratio 不能在每个 reference cycle 都取连续小数值。它必须用 integer sequence 近似平均值，因此会产生 quantization error。若这个 error pattern 是 deterministic periodic pattern，就会形成 fractional spur；若它被 randomized，就会形成 noise；若它被 delta-sigma shaped，就会把大部分 quantization noise 推到高频，再由 PLL loop filter 抑制。

English: The core problem is that the divider ratio cannot take a continuous fractional value on each reference cycle. It must approximate the average with an integer sequence, creating quantization error. If this error pattern is deterministic and periodic, it creates fractional spurs; if it is randomized, it creates noise; if it is delta-sigma shaped, most quantization noise is pushed to high frequency and then suppressed by the PLL loop filter.

中文：因此 fractional-N 设计的主要任务不是“让 divider 平均值正确”这么简单，而是控制 quantization error 的 spectral placement、PFD/CP nonlinearity、integer-boundary spur、coupling path、DSM idle tone、DTC/DAC compensation 和 loop bandwidth。

English: Therefore the main fractional-N design task is not simply “make the divider average correct.” It is to control the spectral placement of quantization error, PFD/CP nonlinearity, integer-boundary spurs, coupling paths, DSM idle tones, DTC/DAC compensation, and loop bandwidth.

## 4. Classical Fractional-N Spur Mechanism

中文：传统 fractional-N PLL 使用 accumulator 或 deterministic modulus-control sequence。若 $\alpha$ 是 rational fraction，divider pattern 会周期性重复，PFD phase error 也会周期性重复，从而在 output spectrum 中形成 fractional spur。更细频率分辨率并不天然更好；如果 fractional pattern 更长、更复杂，但没有有效 spur suppression，spur/noise 可能更难处理。

English: A traditional fractional-N PLL uses an accumulator or deterministic modulus-control sequence. If $\alpha$ is a rational fraction, the divider pattern repeats periodically, and the PFD phase error repeats periodically, creating fractional spurs in the output spectrum. Finer frequency resolution is not automatically better; if the fractional pattern becomes longer or more complex without effective spur suppression, spur/noise can become harder to manage.

中文：工程上最危险的误解是把 fractional spur 看成纯数字问题。divider sequence 是数字产生的，但 spur 最终来自 PFD/CP、loop filter、VCO control line、supply/substrate coupling 和 loop nonlinearity 的混合。一个理想 linear model 可能显示 DSM quantization noise 被 high-pass shaped，但真实 CP nonlinearity 会把它折回 in-band。

English: The most dangerous engineering misunderstanding is treating fractional spur as a purely digital problem. The divider sequence is generated digitally, but the spur ultimately comes from the mixture of PFD/CP behavior, loop filter, VCO control line, supply/substrate coupling, and loop nonlinearity. An ideal linear model may show DSM quantization noise high-pass shaped, while real CP nonlinearity folds it back in-band.

## 5. Delta-Sigma Fractional-N PLL

中文：delta-sigma modulation 的作用是把 fractional division 的 quantization error 重新塑形。低频误差被压低，高频误差增加。只要 PLL bandwidth 不太宽，高频 quantization noise 会被 loop 低通/高通组合抑制在输出端。

English: Delta-sigma modulation reshapes the quantization error of fractional division. Low-frequency error is reduced while high-frequency error increases. If the PLL bandwidth is not too wide, high-frequency quantization noise is suppressed at the output by the loop response.

### 5.1 First-Order DSM

中文：一阶 DSM 的输出可以用 input 与 error difference 表示：

English: A first-order DSM output can be expressed as the input plus an error difference:

$$
y_i=x_{i-1}+(e_i-e_{i-1})
$$

中文：因此 quantization noise 被一阶 difference shaped。对 white quantization error 的理想近似，in-band rms noise 随 oversampling ratio 快速下降：

English: Thus the quantization noise is first-order difference shaped. Under the ideal approximation of white quantization error, the in-band rms noise decreases rapidly with oversampling ratio:

$$
n_o\approx e_{rms}\frac{\pi}{\sqrt{3}}OSR^{-3/2}
$$

中文：这个公式的前提是量化误差近似 white 且没有强 idle tone。对 simple rational fractions、短 pattern 或 poor dithering，实际 spur 可能远高于 white-noise estimate。

English: This formula assumes that the quantization error is approximately white and that strong idle tones are absent. For simple rational fractions, short patterns, or poor dithering, actual spurs can be far above the white-noise estimate.

### 5.2 Second-Order DSM

中文：二阶 DSM 的 error shaping 可写为二阶 difference：

English: A second-order DSM shapes error as a second difference:

$$
y_i=x_{i-1}+(e_i-2e_{i-1}+e_{i-2})
$$

$$
|N(f)|=E(f)\left(1-e^{-j\omega T}\right)^2
$$

中文：理想 in-band rms noise 近似为：

English: The ideal in-band rms noise can be approximated as:

$$
n_o\approx e_{rms}\frac{\pi^2}{\sqrt{5}}OSR^{-5/2}
$$

中文：二阶以上 DSM 可以显著降低 close-in quantization noise，但会增加 high-frequency shaped noise。这个 high-frequency noise 需要由 PLL loop filter、高阶 pole、post-divider 或 architecture compensation 处理，否则会带来 out-of-band phase noise 或 spur folding。

English: A second-order or higher DSM can greatly reduce close-in quantization noise, but it increases high-frequency shaped noise. This high-frequency noise must be handled by the PLL loop filter, higher-order poles, post-divider, or architecture compensation; otherwise it can create out-of-band phase noise or spur folding.

### 5.3 Lth-Order DSM

中文：$L$ 阶 DSM 的理想噪声传递具有 $L$ 阶 high-pass 特性：

English: An $L$th-order DSM has an ideal $L$th-order high-pass noise transfer:

$$
|N_L(f)|=
\frac{e_{rms}}{\sqrt{2T}}
\left[2\sin\left(\frac{\omega T}{2}\right)\right]^L
$$

中文：对应 in-band rms noise 近似为：

English: The corresponding in-band rms noise is approximately:

$$
n_o\approx
e_{rms}
\frac{\pi^L}{\sqrt{2L+1}}
OSR^{-(L+1/2)}
$$

中文：这个表达式解释了为什么 fractional-N PLL 常用三阶或更高 DSM：更高阶数可以把 close-in quantization noise 推得更远。但阶数越高，stability、idle tones、word-length effects、out-of-band peaking 和 CP nonlinearity sensitivity 越需要认真验证。

English: This expression explains why fractional-N PLLs often use third-order or higher DSMs: higher order pushes close-in quantization noise farther away. But higher order also demands more careful verification of modulator stability, idle tones, word-length effects, out-of-band peaking, and sensitivity to CP nonlinearity.

## 6. MASH, Idle Tones, and Dithering

中文：MASH DSM 在 commercial fractional-N PLL 中常见，因为它可以用数字 cascade structure 实现高阶 shaping，并且在许多情况下比 single-loop DSM 更容易得到可预测的输出统计。但 MASH 不是 magic；finite word length、digital overflow handling、rational input、truncation 和 implementation bug 都可能形成 idle tone。

English: MASH DSMs are common in commercial fractional-N PLLs because a digital cascade structure can implement high-order shaping with relatively predictable output statistics. But MASH is not magic; finite word length, overflow handling, rational input values, truncation, and implementation bugs can all create idle tones.

中文：dithering 可以打散 idle tone，把 deterministic spur 转换为更 noise-like 的 spectrum。代价是 noise floor 增加。对某些 simple rational fractions，例如 1/2 或 1/4，若 spur 本来位于 loop bandwidth 之外并可被充分滤除，dither 反而可能不划算。

English: Dithering can break idle tones and convert deterministic spurs into a more noise-like spectrum. The cost is increased noise floor. For some simple rational fractions such as 1/2 or 1/4, if the spur is already outside loop bandwidth and sufficiently filtered, dithering may not be worth the added noise.

## 7. Compensation Methods

### 7.1 DAC Charge Compensation

中文：charge compensation 的思想是用 DAC 注入与 fractional timing error 相反的 charge，抵消 PFD/CP 看到的 deterministic phase error。若 divider timing error sequence 为 $e[m]$，所需补偿电荷可按累积误差估算：

English: Charge compensation uses a DAC to inject charge opposite to the fractional timing error, cancelling deterministic phase error seen by the PFD/CP. If the divider timing-error sequence is $e[m]$, the required compensation charge can be estimated from accumulated error:

$$
Q_n[k]=I_{CP}T_{ref}\sum_{m=0}^{k-1}e[m]
$$

中文：DAC compensation 的难点是 matching、gain calibration、timing alignment、DAC glitch 和 PFD/CP nonlinearity。它对 sample-and-hold PD 可能更自然，而对 PFD pulse-width ripple 不一定能完全取消。

English: The difficult parts of DAC compensation are matching, gain calibration, timing alignment, DAC glitch, and PFD/CP nonlinearity. It can be more natural with sample-and-hold PDs; for PFD pulse-width ripple, complete cancellation is harder.

### 7.2 DTC Timing Compensation

中文：DTC compensation 在 PFD 之前直接校正 fractional timing error，因此通常比 charge-domain DAC 更接近问题本身。它把 divider edge 或 reference edge 延迟到更接近理想 fractional phase 的位置。

English: DTC compensation corrects the fractional timing error before the PFD, so it often attacks the problem more directly than charge-domain DAC compensation. It delays the divider edge or reference edge toward the ideal fractional phase.

中文：DTC 的工程风险是 dynamic range、resolution、INL/DNL、PVT drift、supply sensitivity、calibration loop interaction 和 glitch. 高性能 fractional-N BBPLL 或 DPLL 可能需要 12-bit 级别或更高的 effective timing resolution，这会把问题从 loop filter 转移到 time-domain converter design。

English: The engineering risks of a DTC are dynamic range, resolution, INL/DNL, PVT drift, supply sensitivity, calibration-loop interaction, and glitch. A high-performance fractional-N BBPLL or DPLL may need effective timing resolution at the 12-bit level or higher, moving the problem from loop-filter design into time-domain converter design.

### 7.3 Multi-Phase Fractional Division

中文：multi-phase fractional divider 使用多个 VCO phases 或 phase interpolator 生成 finer timing steps。若可用 phase 数为 $k$，quantization step 可降低约 $k$ 倍，quantization noise 可理想降低约 $20\log_{10}k$。

English: A multi-phase fractional divider uses multiple VCO phases or a phase interpolator to generate finer timing steps. If $k$ phases are available, the quantization step can ideally be reduced by about $k$, and quantization noise by about $20\log_{10}k$.

中文：这个方法的风险是 phase mismatch、PI INL、glitchless high-speed phase selection、VCO loading、phase routing skew 和 calibration burden。对 SerDes 多相 clocking，它很有吸引力，但必须和 clock distribution、PI calibration、CDR operation 一起 review。

English: The risks are phase mismatch, PI INL, glitchless high-speed phase selection, VCO loading, phase-routing skew, and calibration burden. For SerDes multiphase clocking it is attractive, but it must be reviewed together with clock distribution, PI calibration, and CDR operation.

## 8. Fractional-N Nonidealities

中文：fractional-N 的重要 nonideality 包括 CP nonlinearity、PFD reset mismatch、DTC INL、DSM idle tone、divider delay modulation、VCO/reference harmonic coupling、supply/substrate coupling、reference/feedback intermodulation 和 integer-boundary spur。integer-boundary spur 特别棘手，因为它发生在输出频率接近 integer-N channel 时，frequency plan 与 coupling path 可能同时放大问题。

English: Important fractional-N nonidealities include CP nonlinearity, PFD reset mismatch, DTC INL, DSM idle tones, divider-delay modulation, VCO/reference harmonic coupling, supply/substrate coupling, reference/feedback intermodulation, and integer-boundary spurs. Integer-boundary spur is especially difficult because it occurs when the output frequency is near an integer-N channel, where the frequency plan and coupling paths may reinforce the issue.

中文：fractional-N review 必须同时包含 digital simulation、behavioral PLL simulation、transistor-level PFD/CP/DTC simulation 和 spur-aware layout/supply review。只看 DSM spectrum 或 Simulink noise shaping 不够。

English: Fractional-N review must include digital simulation, behavioral PLL simulation, transistor-level PFD/CP/DTC simulation, and spur-aware layout/supply review. Looking only at DSM spectrum or Simulink noise shaping is not enough.

## 9. Digital PLL Motivation

中文：digital PLL 的吸引力来自 process scaling、programmability、area reduction、leakage avoidance、digital calibration、fast mode switching 和 testability。digital loop filter 不需要大 passive capacitor，不会像 analog loop filter 那样受 leakage 与 capacitor density 限制。

English: Digital PLLs are attractive because of process scaling, programmability, area reduction, leakage avoidance, digital calibration, fast mode switching, and testability. A digital loop filter does not need a large passive capacitor and is less constrained by leakage and capacitor density than an analog loop filter.

中文：但是 digital PLL 不是天然更低 jitter。TDC resolution/linearity、DCO frequency step、DCO phase noise、quantization noise、limit cycle、supply sensitivity、clock-domain crossing 和 calibration noise 都可能支配 performance。digital-friendly 不等于 analog-easy。

English: A digital PLL is not automatically lower jitter. TDC resolution/linearity, DCO frequency step, DCO phase noise, quantization noise, limit cycle, supply sensitivity, clock-domain crossing, and calibration noise can dominate performance. Digital-friendly does not mean analog-easy.

## 10. Linear TDC/DCO DPLL Model

中文：linear TDC-based DPLL 可以把 time error 量化成 digital code，再经 digital loop filter 控制 DCO。TDC time-domain gain 为：

English: A linear TDC-based DPLL quantizes time error into a digital code and controls a DCO through a digital loop filter. The TDC time-domain gain is:

$$
K_{td}=\frac{1}{t_{res}}
$$

中文：DCO 的 time-domain gain 可近似为：

English: The DCO time-domain gain can be approximated as:

$$
K_{vt}=\frac{f_{res}}{f_v^2}
$$

中文：若 digital loop filter 为：

English: If the digital loop filter is:

$$
F(z)=\alpha+\frac{\beta}{1-z^{-1}}
$$

中文：z-domain open-loop transfer 可以写成：

English: The z-domain open-loop transfer can be written as:

$$
G(z)=
\frac{K_{td}F(z)NK_{vt}}{1-z^{-1}}
$$

中文：phase-domain 表达常用：

English: A common phase-domain representation is:

$$
K_{tdc}=\frac{T_{ref}}{2\pi t_{res}}
$$

$$
K_{dco}=2\pi f_{res}
$$

$$
\omega_u\approx\frac{\alpha K_{tdc}K_{dco}}{N}
$$

$$
\omega_z=\frac{\beta/\alpha}{T_{ref}}
$$

中文：这些公式有助于把 digital coefficients 映射回 loop bandwidth 和 zero location。设计时必须记录 $\alpha$、$\beta$ 的 scaling convention，否则不同团队的 code gain 和 physical gain 很容易差一个 $2\pi$、$N$ 或 $T_{ref}$。

English: These equations help map digital coefficients back to loop bandwidth and zero location. The scaling convention of $\alpha$ and $\beta$ must be recorded; otherwise different teams can easily differ by a factor of $2\pi$, $N$, or $T_{ref}$ in code gain versus physical gain.

## 11. TDC and DCO Quantization Noise

中文：TDC quantization error 若近似 uniform distribution，则 variance 为：

English: If TDC quantization error is approximated as uniformly distributed, its variance is:

$$
\sigma_{tdc}^2=\frac{t_{res}^2}{12}
$$

中文：output-referred TDC phase noise floor 可按 sampling reference rate 和 output period 进行量纲转换。常用 scaling 是：

English: The output-referred TDC phase-noise floor can be dimensionally converted using the reference sampling rate and output period. A common scaling is:

$$
L_{TDC}\propto
\frac{(2\pi)^2}{12}
\left(\frac{t_{res}}{T_{out}}\right)^2
\frac{1}{f_{ref}}
$$

中文：DCO quantization 的 frequency-step variance 为：

English: The frequency-step variance of DCO quantization is:

$$
\sigma_{n,f}^2=\frac{f_{res}^2}{12}
$$

中文：frequency noise 经过 phase integration 后形成近似 $1/f_m^2$ 的 phase-noise slope。直觉上，DCO LSB 越粗、reference update 越慢、loop outside-band filtering 越弱，DCO quantization 对 jitter 的影响越大。

English: Frequency noise becomes phase noise through integration, giving an approximate $1/f_m^2$ phase-noise slope. Intuitively, a coarser DCO LSB, slower reference update, and weaker outside-band filtering make DCO quantization more damaging to jitter.

## 12. Bang-Bang DPLL

中文：bang-bang DPLL 用 binary phase detector，只告诉 loop “early” 或 “late”，不提供线性 phase error magnitude。在没有足够 random jitter 的情况下，BBPLL 容易进入 deterministic limit cycle，产生 periodic timing jitter。

English: A bang-bang DPLL uses a binary phase detector that says only “early” or “late,” without providing a linear phase-error magnitude. Without enough random jitter, a BBPLL can enter deterministic limit cycles and produce periodic timing jitter.

中文：Rhee 和 Yu 给出的 limit-cycle peak-to-peak jitter model 可写为：

English: A limit-cycle peak-to-peak jitter model from Rhee and Yu can be written as:

$$
\Delta t_{pp}=2(1+D)\alpha NK_{vt}
$$

中文：对应 RMS estimate 为：

English: The corresponding RMS estimate is:

$$
\sigma_{t,lc}=\frac{(1+D)\alpha NK_{vt}}{\sqrt{3}}
$$

中文：其中 $D$ 表示 loop delay 相关项。这个公式的 design message 是明确的：BBPLL 的 proportional step、DCO time gain、divider ratio 和 loop latency 都会直接放大 limit-cycle jitter。

English: Here $D$ represents a loop-delay-related term. The design message is clear: proportional step size, DCO time gain, divider ratio, and loop latency directly enlarge BBPLL limit-cycle jitter.

## 13. Random-Jitter Linearization of BBPD

中文：当输入 random jitter 足够大时，BBPD 可以被统计 linearization。常用有效 gain 为：

English: When input random jitter is large enough, a BBPD can be statistically linearized. A common effective gain is:

$$
K_{td}=\frac{\eta}{\sigma_t}
$$

$$
\eta=\sqrt{\frac{2}{\pi}}
$$

中文：对应 unity-gain frequency 近似为：

English: The corresponding unity-gain frequency is approximately:

$$
\omega_u\approx
\sqrt{\frac{2}{\pi}}
\frac{\alpha NK_{vt}}{T_{ref}\sigma_t}
$$

中文：进入 random-noise-dominated regime 的一个实用条件是 limit-cycle jitter 不应大于 random jitter：

English: A practical condition for entering the random-noise-dominated regime is that limit-cycle jitter should not exceed random jitter:

$$
\sigma_{t,lc}\le\sigma_t
$$

中文：这解释了为什么 BBPLL/CDR 中 loop latency、PI/DCO step size 和 input jitter statistics 必须一起看。少量随机噪声有时反而让 bang-bang loop 更可线性建模，但过多随机噪声会直接恶化 sampling margin。

English: This explains why loop latency, PI/DCO step size, and input-jitter statistics must be reviewed together in BBPLL/CDR systems. A small amount of random noise can make a bang-bang loop more linearizable, but too much random noise directly hurts sampling margin.

## 14. Fractional-N BB-DPLL

中文：fractional-N BB-DPLL 特别困难，因为 DSM divider pattern 会产生 deterministic jitter，而这个 jitter 可能远大于 receiver input random jitter。BBPD 因此被推入 limit-cycle-dominated behavior，loop bandwidth 变窄，in-band phase noise 变差。

English: A fractional-N BB-DPLL is especially difficult because the DSM divider pattern creates deterministic jitter that can be much larger than the receiver input random jitter. The BBPD is then pushed into limit-cycle-dominated behavior, loop bandwidth narrows, and in-band phase noise worsens.

中文：DTC cancellation 可以把 DSM-induced timing error 从 BBPD 输入处移除，使 loop 回到 random-noise-dominated regime。但这要求 DTC 有足够 dynamic range、resolution、linearity 和 calibration robustness，且 DTC 自身 supply noise 与 INL 不应变成新的 spur source。

English: DTC cancellation can remove DSM-induced timing error at the BBPD input and return the loop to a random-noise-dominated regime. But this requires enough DTC dynamic range, resolution, linearity, and calibration robustness, and the DTC's own supply noise and INL must not become a new spur source.

## 15. Hybrid PLL

中文：hybrid PLL 把 analog proportional path 和 digital integral path 结合。小信号 loop dynamics 主要由 analog proportional path 决定，large-signal frequency acquisition 和 slow integral correction 由 digital path 提供。它试图保留 analog loop 的低噪声与线性优势，同时避免巨大 analog integral capacitor 和 leakage 问题。

English: A hybrid PLL combines an analog proportional path with a digital integral path. Small-signal loop dynamics are mainly set by the analog proportional path, while large-signal frequency acquisition and slow integral correction come from the digital path. It tries to keep the low-noise and linear advantages of an analog loop while avoiding a large analog integral capacitor and leakage problems.

中文：一个混合 loop 的近似 open-loop expression 可以写成 analog path 与 digital path 的和：

English: An approximate open-loop expression for a hybrid loop can be written as the sum of an analog path and a digital path:

$$
G(s)\approx
\frac{1}{Ns}
\left(
\frac{I_{CP}R_1K_v}{2\pi}
+
\frac{\eta\beta K_{dco}}{\sigma_t s}
\right)
$$

中文：这个表达式的重点不是某个系数，而是结构：analog proportional path 负责 fast low-noise phase correction，digital integral path 负责 long-term frequency accuracy。review 时必须确认两条路径的 gain、latency、noise、calibration update 和 mode transition 不互相打架。

English: The point of this expression is structure, not a single coefficient: the analog proportional path provides fast low-noise phase correction, while the digital integral path provides long-term frequency accuracy. A review must confirm that the gain, latency, noise, calibration updates, and mode transitions of the two paths do not fight each other.

## 16. Engineering Tradeoffs

中文：fractional-N PLL 的主要 tradeoff 是 frequency resolution versus spur/noise. 更高 DSM order 降低 close-in quantization noise，但提高 out-of-band noise 并增加 implementation risk。更宽 loop bandwidth 可以压低 VCO noise，却可能让 shaped quantization noise 或 reference/PFD noise 进入输出。更细 DTC/DCO resolution 降低 quantization error，却增加 area、power、calibration 和 nonlinearity burden。

English: The main fractional-N tradeoff is frequency resolution versus spur/noise. Higher DSM order reduces close-in quantization noise but increases out-of-band noise and implementation risk. Wider loop bandwidth can suppress VCO noise but may pass shaped quantization noise or reference/PFD noise to the output. Finer DTC/DCO resolution reduces quantization error but increases area, power, calibration, and nonlinearity burden.

中文：digital PLL 的主要 tradeoff 是 programmability versus converter quality. Loop filter 可以数字化，但 time-to-digital 和 digital-to-frequency conversion 仍然是 analog/mixed-signal bottlenecks。优秀 ADPLL 不是把 analog 问题消灭，而是把问题搬到可校准、可观测、可量产的边界上。

English: The main digital PLL tradeoff is programmability versus converter quality. The loop filter can be digital, but time-to-digital and digital-to-frequency conversion remain analog/mixed-signal bottlenecks. A good ADPLL does not eliminate analog problems; it moves them to boundaries that are calibratable, observable, and manufacturable.

## 17. Common Mistakes

中文：常见错误一是只检查 DSM ideal spectrum，而不检查 PFD/CP nonlinearity。理想 DSM 只能说明 quantization noise 的目标分布，不能证明真实 PLL output spur 合格。

English: A common mistake is checking only the ideal DSM spectrum and not PFD/CP nonlinearity. An ideal DSM shows the target distribution of quantization noise; it does not prove that real PLL output spur is acceptable.

中文：常见错误二是把 TDC resolution 当作唯一 DPLL jitter metric。TDC resolution 重要，但 DCO LSB、DCO intrinsic phase noise、DTC INL、supply pushing、digital truncation、limit cycles 和 calibration noise 同样可能主导 jitter。

English: A second common mistake is treating TDC resolution as the only DPLL jitter metric. TDC resolution matters, but DCO LSB, DCO intrinsic phase noise, DTC INL, supply pushing, digital truncation, limit cycles, and calibration noise can also dominate jitter.

中文：常见错误三是在 BBPLL 中忽略 loop latency。latency 会放大 limit-cycle jitter 并增加 jitter peaking；在 high-speed SerDes CDR 中，几个 UI 的 decision/filter/PI delay 就可能改变 loop behavior。

English: A third common mistake is ignoring loop latency in a BBPLL. Latency increases limit-cycle jitter and jitter peaking; in a high-speed SerDes CDR, a few UI of decision/filter/PI delay can change loop behavior.

## 18. Deep-Ingest Interview Questions

中文：Q1：fractional-N PLL 为什么会有 fractional spur？好答案应说明 divider ratio 用 integer sequence 近似 fractional average，periodic quantization error 通过 PFD/CP 和 VCO control path 形成 phase modulation，并且 CP nonlinearity/coupling 会恶化 spur。

English: Q1: Why does a fractional-N PLL have fractional spurs? A good answer explains that divider ratio uses an integer sequence to approximate a fractional average, periodic quantization error becomes phase modulation through the PFD/CP and VCO control path, and CP nonlinearity/coupling worsens the spur.

中文：Q2：为什么 DSM 可以帮助 fractional-N PLL？好答案应说明 DSM 把低频 quantization noise 推到高频，让 PLL loop filter 更容易抑制；同时也要指出 high-order DSM 会增加 out-of-band noise、idle tone 和 nonlinearity sensitivity。

English: Q2: Why does a DSM help a fractional-N PLL? A good answer says the DSM pushes low-frequency quantization noise to high frequency where the PLL loop filter can suppress it, while noting that high-order DSMs increase out-of-band noise, idle tones, and nonlinearity sensitivity.

中文：Q3：ADPLL 相比 CPPLL 的真正优势和风险是什么？好答案应提到 programmability、scaling、digital calibration 和 leakage/area 优势，同时指出 TDC/DCO quantization、DCO phase noise、supply sensitivity 和 limit-cycle behavior 是主要风险。

English: Q3: What are the real advantages and risks of an ADPLL compared with a CPPLL? A good answer mentions programmability, scaling, digital calibration, and leakage/area advantages, while pointing out that TDC/DCO quantization, DCO phase noise, supply sensitivity, and limit-cycle behavior are major risks.

## 19. Quality Checklist

- Fractional ratio, DSM order, word length, and dither policy are documented.
- DSM noise shaping is checked with rational fractions and worst-case channels, not only random inputs.
- PFD/CP nonlinearity or DTC INL is included in spur simulation.
- Integer-boundary channels are explicitly tested.
- Loop bandwidth is checked against VCO noise, reference noise, and shaped quantization noise.
- TDC resolution, DCO LSB, and DTC resolution use consistent time/phase/frequency units.
- BBPLL latency and limit-cycle jitter are estimated before signoff.
- Digital coefficient scaling is documented with $2\pi$, $N$, and $T_{ref}$ conventions.
- Spur results are converted to UI or time jitter when used for SerDes margin.

## 20. Balanced Ingest 2026-07-05 - Bang-Bang Synthesizer and Low-Power Fractional-N ADPLL

Source update:

- Nicola Da Dalt, *Theory and Implementation of Digital Bang-Bang Frequency Synthesizers for High Speed Serial Data Communications*, Ph.D. dissertation, RWTH Aachen, 2007.
- Peng Chen, Xi Meng, Jun Yin, Pui-In Mak, Rui P. Martins, and Robert Bogdan Staszewski, "A 529-uW Fractional-N All-Digital PLL Using TDC Gain Auto-Calibration and an Inverse-Class-F DCO in 65-nm CMOS," IEEE TCAS-I, Vol. 69, No. 1, January 2022.
- Ingest level: Balanced Ingest.

### 20.1 Da Dalt BBPLL Thesis - Why It Matters

中文：Da Dalt 的博士论文把 bang-bang PLL 从“可以线性化的 PLL”重新放回 nonlinear sampled system。BPD 是 hard nonlinearity，因此 BBPLL 在低噪声条件下不会像线性 PLL 那样收敛到固定 phase-error operating point，而是在 phase plane 中形成 orbit 或 limit cycle。对 SerDes CDR 和 digital frequency synthesizer 来说，这个观点很重要：稳定性不只是 pole location，也包括 nonlinear orbit 是否存在、loop latency 是否扩大 limit cycle，以及噪声是否足够大到让统计线性化模型成立。

English: Da Dalt's dissertation reframes a bang-bang PLL as a nonlinear sampled system rather than merely a PLL that can be linearized. The BPD is a hard nonlinearity, so under low-noise conditions a BBPLL does not converge to a fixed phase-error operating point like a linear PLL; it forms an orbit or limit cycle in phase plane. For SerDes CDRs and digital frequency synthesizers, this matters because stability is not only pole location; it also depends on whether a nonlinear orbit exists, whether loop latency expands the limit cycle, and whether noise is large enough for a statistical linearized model to be valid.

中文：论文的 target application 是高速串行通信中的数字 bang-bang frequency synthesizer，用于 Fully Buffered DIMM AMB 的 CDR clock generation，频率最高约 4.8 GHz，目标包括全片上集成、低 jitter、小于 3 dB peaking、11 MHz 到 33 MHz bandwidth、SSC tracking、supply/substrate robustness、小面积和低功耗。130 nm CMOS prototype 报告了约 600 fs 到 650 fs measured jitter。这个结果对现代 PCIe/SerDes 不是直接指标，但它证明 high-bandwidth all-digital bang-bang synthesis 可以达到 analog-PLL-like jitter，同时带来 nonlinear analysis burden。

English: The dissertation targets a digital bang-bang frequency synthesizer for high-speed serial communication, specifically CDR clock generation in a Fully Buffered DIMM AMB, with output frequency up to about 4.8 GHz. Its requirements include full integration, low jitter, peaking below 3 dB, 11 MHz to 33 MHz bandwidth, SSC tracking, supply/substrate robustness, small area, and low power. A 130 nm CMOS prototype reported about 600 fs to 650 fs measured jitter. This is not a modern PCIe/SerDes target number, but it shows that high-bandwidth all-digital bang-bang synthesis can reach analog-PLL-like jitter while introducing nonlinear analysis burden.

### 20.2 Nonlinear BBPLL Map and Latency Jitter

中文：Da Dalt 的 Type-II BBPLL normalized map 可以写成：

English: Da Dalt's normalized Type-II BBPLL map can be written as:

$$
\tau_{k+1}
=
\tau_k+x_0-R\psi_{k-D}-\operatorname{sgn}(\tau_{k-D})
$$

$$
\psi_{k+1}=\psi_k+\operatorname{sgn}(\tau_{k+1})
$$

中文：其中 $\tau$ 是归一化 timing error，$x_0$ 是 reference period 与 free-running divided DCO period 的归一化偏差，$R=\alpha/\beta$ 表示 integral/proportional loop-filter coefficient ratio，$D$ 是 loop latency。这个 map 的工程价值是把 proportional step、integral action、frequency offset 和 latency 放在同一个 nonlinear recursion 中，而不是把 BBPLL 强行塞进普通 Laplace-domain PLL 模型。

English: Here $\tau$ is normalized timing error, $x_0$ is the normalized difference between reference period and free-running divided DCO period, $R=\alpha/\beta$ is the integral-to-proportional loop-filter coefficient ratio, and $D$ is loop latency. The engineering value of this map is that proportional step, integral action, frequency offset, and latency are placed in the same nonlinear recursion instead of forcing the BBPLL into an ordinary Laplace-domain PLL model.

中文：对 first-order BBPLL，简化 map 为：

English: For a first-order BBPLL, the simplified map is:

$$
\tau_{k+1}=\tau_k+x_0-\operatorname{sgn}(\tau_{k-D})
$$

中文：当 $x_0=0$ 时，最大 orbit 的 peak-to-peak jitter 为：

English: When $x_0=0$, the peak-to-peak jitter of the maximum orbit is:

$$
\tau_{pp}=1+2D
$$

中文：对应 timing-error variance 为：

English: The corresponding timing-error variance is:

$$
\sigma_{\tau}^2=
\begin{cases}
\dfrac{(1+2D)^2}{12}, & D\ne0 \\
\dfrac{1}{4}, & D=0
\end{cases}
$$

中文：当 $x_0\ne0$ 且用 worst-case uniform approximation 时：

English: When $x_0\ne0$ and a worst-case uniform approximation is used:

$$
\tau_{pp}=2(1+D)
$$

$$
\sigma_{\tau}^2\approx\frac{(1+D)^2}{3}
$$

中文：这些公式的核心 design message 很朴素：loop latency 会近似线性放大 BBPLL limit-cycle jitter，并把 limit-cycle tones 移到更低 offset frequency。对 SerDes CDR，这意味着 digital decision latency、retiming latency、loop-filter update delay、PI/DCO code latency 和 clock-distribution feedback delay 都不能被当成小实现细节。

English: The core design message of these equations is simple: loop latency roughly linearly increases BBPLL limit-cycle jitter and moves limit-cycle tones to lower offset frequency. For a SerDes CDR, digital decision latency, retiming latency, loop-filter update delay, PI/DCO-code latency, and clock-distribution feedback delay cannot be treated as minor implementation details.

### 20.3 Linearized BPD Gain Depends on the Whole Loop

中文：Da Dalt 的另一个重要结论是：BPD gain 不应只由 reference jitter 单独决定。BPD 看到的是 reference clock 与 feedback clock 之间的 untracked jitter，而这个 untracked jitter 由 input jitter、PLL-generated jitter、loop coefficients、DCO gain 和 limit-cycle dynamics 共同决定。当 reference jitter 和 PLL-generated jitter 同量级时，把 BPD 当成 standalone component 来估 gain 会偏离真实 loop behavior。

English: Another important conclusion from Da Dalt is that BPD gain should not be determined from reference jitter alone. The BPD sees the untracked jitter between reference clock and feedback clock, and that untracked jitter is jointly determined by input jitter, PLL-generated jitter, loop coefficients, DCO gain, and limit-cycle dynamics. When reference jitter and PLL-generated jitter are comparable, estimating BPD gain as a standalone component can miss the real loop behavior.

中文：论文使用 Markov-chain-based reasoning 推导更 general 的 BPD linearized gain，并指出噪声大小决定应使用 nonlinear limit-cycle model 还是 high-noise statistical linearized model。换句话说，BBPLL 的 small-signal bandwidth 和 peaking 不是固定电路常数，而是 operating condition dependent quantities。

English: The dissertation uses Markov-chain-based reasoning to derive a more general linearized BPD gain and notes that the amount of noise determines whether the nonlinear limit-cycle model or a high-noise statistical linearized model should be used. In other words, BBPLL small-signal bandwidth and peaking are not fixed circuit constants; they are operating-condition-dependent quantities.

### 20.4 Chen et al. 529-uW Fractional-N ADPLL - Why It Matters

中文：Chen 等人的 2022 TCAS-I 论文展示了一个 DTC-assisted fractional-N ADPLL：65 nm CMOS，BLE-oriented，fractional-N channel integrated jitter 868 fs rms，总功耗 529 uW，reported FoM 为 -244 dB。对本知识库来说，它的价值不在于把 BLE 指标套到 SerDes，而在于提供一个现代 low-power ADPLL case study：TDC range、TDC gain calibration、DTC mismatch spur、DCO waveform shaping 和 PVT robustness 如何互相牵制。

English: Chen et al.'s 2022 TCAS-I paper demonstrates a DTC-assisted fractional-N ADPLL in 65 nm CMOS for BLE-oriented operation, with 868 fs rms integrated jitter in a fractional-N channel, 529 uW total power, and reported FoM of -244 dB. For this knowledge base, its value is not applying BLE numbers to SerDes; it is a modern low-power ADPLL case study showing how TDC range, TDC gain calibration, DTC mismatch spur, DCO waveform shaping, and PVT robustness constrain one another.

中文：论文提出的 hybrid TDC 用 flash-like coarse quantization 扩展 vernier TDC input range，同时复用 delay chain 做 background gain calibration。关键问题是 narrow-range TDC 在 acquisition 初期可能 out-of-range；若简单把 out-of-range code 放大，会瞬间放大 loop gain，在较宽 bandwidth 下损害 phase margin，甚至导致 loop 失锁。因此 acquisition 辅助不应粗暴提高 out-of-range gain，而应尽量让 digital loop filter 看到接近真实 phase error 的 coarse quantized value。

English: The paper's hybrid TDC uses flash-like coarse quantization to extend the input range of a vernier TDC while reusing delay chains for background gain calibration. The key issue is that a narrow-range TDC can go out of range during acquisition; simply enlarging the out-of-range code instantaneously increases loop gain, reducing phase margin under wide bandwidth and potentially causing loss of lock. Therefore acquisition assistance should not blindly increase out-of-range gain; it should let the digital loop filter see a coarse quantized value close to the actual phase error.

### 20.5 TDC Gain Calibration and DTC Implementation

中文：Chen 等人的 hybrid TDC calibration 目标可以概括为：

English: Chen et al.'s hybrid TDC calibration target can be summarized as:

$$
12\tau_s=T_v
$$

$$
8\tau_s=10\tau_f
$$

$$
\tau_{res}=\tau_s-\tau_f=\frac{T_v}{60}
$$

中文：其中 $\tau_s$ 和 $\tau_f$ 分别是 slow/fast delay-cell delay，$T_v$ 是 DCO period，$\tau_{res}$ 是 vernier resolution。这个例子说明 TDC gain calibration 本质上是 delay-locking problem：如果 TDC gain 随 PVT 漂移，digital loop coefficient 虽然没变，physical loop bandwidth 和 in-band quantization-noise floor 仍会漂移。

English: Here $\tau_s$ and $\tau_f$ are slow/fast delay-cell delays, $T_v$ is DCO period, and $\tau_{res}$ is vernier resolution. This example shows that TDC gain calibration is essentially a delay-locking problem: if TDC gain drifts with PVT, the digital loop coefficients may be unchanged while physical loop bandwidth and in-band quantization-noise floor still drift.

中文：论文的 snapshot/offset timing 关系为：

English: The paper's snapshot/offset timing relationship is:

$$
t_{dx}=\frac{T_v}{2}+t_{c2q}+t_{d2f}-t_{d2s}
$$

中文：这个式子提醒 ADPLL designer：clock gating、snapshot sampling、TDC input alignment 和 metastability margin 都是 loop design 的一部分。为了省电而 gating DCO clock 可以减少冗余 transition，但必须保留正确 phase information，且 offset delay 不能把 TDC transfer function 推到 detection window 边缘。

English: This equation reminds ADPLL designers that clock gating, snapshot sampling, TDC input alignment, and metastability margin are part of loop design. Gating the DCO clock can save power by avoiding redundant transitions, but it must preserve correct phase information, and offset delay must not push the TDC transfer function to the edge of its detection window.

中文：DTC 方面，buffer-cascaded DTC 简化实现，但 nonlinearity 主要来自 device mismatch。论文给出的 practical scaling 是：约 4x power 只能换来约 2x mismatch reduction，也就是 spur 大约改善 6 dB。这个 tradeoff 很有价值，因为它把 fractional spur control 从“多加尺寸”拉回到 power budget、calibration 和 architecture compensation 的共同优化。

English: On the DTC side, a buffer-cascaded DTC simplifies implementation, but its nonlinearity mainly comes from device mismatch. The paper gives a practical scaling: about 4x power buys only about 2x mismatch reduction, corresponding to roughly 6 dB spur improvement. This tradeoff is valuable because it turns fractional-spur control from “just size up devices” into a joint optimization of power budget, calibration, and architectural compensation.

### 20.6 Balanced Design Lessons

| Lesson | Engineering use |
|---|---|
| BBPLL low-noise behavior is nonlinear | Use phase-plane/limit-cycle thinking before trusting linear bandwidth numbers. |
| BPD gain is loop-dependent | Estimate gain from untracked jitter, not only standalone reference jitter. |
| Loop latency directly increases limit-cycle jitter | Minimize decision, filter, PI/DCO, and feedback latency in BBPLL/CDR loops. |
| TDC range and acquisition are coupled | Out-of-range code handling can destabilize wide-band ADPLLs. |
| TDC gain drift changes real loop bandwidth | Background TDC gain calibration can stabilize in-band PN and loop dynamics. |
| DTC mismatch spur has expensive sizing tradeoff | Use sizing, calibration, dithering, and architecture together. |
| BLE/IoT metrics are not SerDes metrics | Reuse architecture lessons, not application-specific pass/fail numbers. |

### 20.7 Manual Review Items

- Da Dalt's thesis is a long source; this Balanced Ingest promoted core BBPLL concepts and selected formulas, not a full dissertation-level extraction.
- Chen et al.'s ADPLL is optimized for BLE/IoT, so measured jitter, spur, power, and FoM should not be treated as SerDes or PCIe targets.
- TDC/DTC formulas depend on the paper's architecture and symbol definitions; future project notes should restate local conventions before reuse.
- BBPLL stochastic gain modeling is deeper than this Balanced update; mark it for future Deep Ingest if BB-CDR design becomes a near-term focus.

## 21. Source Provenance

| Source | Type | Status | Reusable knowledge promoted |
|---|---|---|---|
| Woogeun Rhee and Zhiping Yu, *Phase-Locked Loops: System Perspectives and Circuit Design Aspects*, Wiley/IEEE Press, 2024 | Book PDF | Deep Ingest 2026-07-05; archived under `90_Archive/processed/2026/books/phase_locked_loops_rhee_yu_2024/` | Fractional-N divider problem, DSM quantization-noise shaping, spur-control options, DTC/DAC compensation, fractional-N nonidealities, TDC/DCO DPLL modeling, BBPLL limit-cycle and random-linearized behavior, hybrid PLL architecture |
| Nicola Da Dalt, *Theory and Implementation of Digital Bang-Bang Frequency Synthesizers for High Speed Serial Data Communications*, Ph.D. dissertation, RWTH Aachen, 2007 | Dissertation PDF | Balanced Ingest 2026-07-05; archived under `90_Archive/processed/2026/articles/digital_bang_bang_frequency_synthesizers_da_dalt_2007/` | BBPLL nonlinear orbit/limit-cycle framing, latency-driven jitter formulas, BPD gain dependence on loop-generated untracked jitter, nonlinear versus linearized model selection, digital loop-gain monitoring concept |
| Peng Chen et al., "A 529-uW Fractional-N All-Digital PLL Using TDC Gain Auto-Calibration and an Inverse-Class-F DCO in 65-nm CMOS," IEEE TCAS-I, Vol. 69, No. 1, January 2022 | IEEE paper PDF | Balanced Ingest 2026-07-05; archived under `90_Archive/processed/2026/papers/chen_529uw_fractional_n_adpll_2022/` | DTC-assisted fractional-N ADPLL case study, hybrid TDC range extension, background TDC gain calibration, out-of-range TDC stability caution, DTC mismatch/power/spur scaling, snapshot offset timing |

## 22. Future Evolution

中文：未来扩展这篇 note 时，应加入具体 MASH examples、integer-boundary spur case studies、DTC calibration loops、modern ADPLL silicon papers、PCIe spread-spectrum clocking application、BBPLL CDR comparison、DCO layout/noise case studies，以及 behavioral model templates。不要把 general PLL bandwidth、VCO ISF 或 CP dead-zone 内容复制到这里；应链接对应 canonical notes。

English: Future extensions should add concrete MASH examples, integer-boundary spur case studies, DTC calibration loops, modern ADPLL silicon papers, PCIe spread-spectrum clocking applications, BBPLL CDR comparisons, DCO layout/noise case studies, and behavioral model templates. Do not copy general PLL bandwidth, VCO ISF, or CP dead-zone content here; link to the corresponding canonical notes instead.
