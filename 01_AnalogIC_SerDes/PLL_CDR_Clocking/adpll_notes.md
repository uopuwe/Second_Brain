---
title: "ADPLL Notes"
domain: "AnalogIC_SerDes"
tags:
  - PLL
  - ADPLL
  - DPLL
  - TDC
  - DCO
  - Clocking
  - SerDes
  - PCIe7
aliases:
  - adpll_notes
  - ADPLL
  - All-Digital PLL
created: 2026-07-05
updated: 2026-07-05
status: "active"
---

# ADPLL Notes

## 1. Purpose

中文：这篇笔记是 all-digital PLL 的专门 canonical note，用来组织 TDC、DCO、digital loop filter、DTC-assisted fractional-N、background calibration、digital coefficient scaling、limit cycle、quantization noise 和 supply/digital coupling 等主题。它不是 [[pll_fractional_n_digital]] 的重复；那篇 note 继续负责 fractional-N、DSM、BBPLL 和 hybrid PLL 的横向主题，这篇 note 专注 ADPLL architecture 和 implementation review。

English: This is the dedicated canonical note for all-digital PLLs. It organizes TDCs, DCOs, digital loop filters, DTC-assisted fractional-N operation, background calibration, digital coefficient scaling, limit cycles, quantization noise, and supply/digital coupling. It is not a duplicate of [[pll_fractional_n_digital]]; that note remains the broader home for fractional-N, DSM, BBPLL, and hybrid-PLL topics, while this note focuses on ADPLL architecture and implementation review.

## 2. System Context

中文：ADPLL 的主要吸引力来自 CMOS scaling：loop filter 可以数字化，系数可以 programmable，calibration 可以后台运行，large passive capacitor 和 charge-pump leakage 的压力降低，频率切换和测试观测也更灵活。它特别适合 low-power radios、multi-standard clocking、digital calibration-heavy systems，以及需要强可编程性的 SerDes/SoC clocking 环境。

English: The main attraction of an ADPLL comes from CMOS scaling: the loop filter can be digital, coefficients are programmable, calibration can run in the background, pressure from large passive capacitors and charge-pump leakage is reduced, and frequency switching plus observability become more flexible. It is especially attractive for low-power radios, multi-standard clocking, digital-calibration-heavy systems, and programmable SerDes/SoC clocking environments.

中文：ADPLL 并不自动比 CPPLL 更低 jitter。它只是把关键模拟瓶颈从 charge pump 和 analog loop filter 转移到 time-to-digital conversion、digitally controlled oscillation、DTC/DCO/TDC linearity、quantization noise、clock-domain crossing、digital supply coupling 和 calibration loop stability。换句话说，ADPLL 是 mixed-signal architecture，不是纯数字模块。

English: An ADPLL is not automatically lower jitter than a CPPLL. It moves the key analog bottlenecks from charge pump and analog loop filter into time-to-digital conversion, digitally controlled oscillation, DTC/DCO/TDC linearity, quantization noise, clock-domain crossing, digital supply coupling, and calibration-loop stability. In other words, an ADPLL is a mixed-signal architecture, not a purely digital block.

## 3. Canonical Architecture

```text
Reference clock
  -> phase prediction / counter / divider
  -> TDC or BBPD
  -> digital loop filter
  -> DCO tuning code
  -> DCO output clock
  -> feedback path
```

中文：典型 ADPLL 可以分为 integer phase path、fractional phase path、TDC/BBPD phase detection、digital loop filter、DCO tuning bank、calibration logic 和 clock distribution。若是 DTC-assisted fractional-N ADPLL，还会在 reference 或 feedback edge 上加入 DTC，以便在 TDC/BBPD 前抵消 fractional timing error。

English: A typical ADPLL can be partitioned into integer phase path, fractional phase path, TDC/BBPD phase detection, digital loop filter, DCO tuning bank, calibration logic, and clock distribution. In a DTC-assisted fractional-N ADPLL, a DTC is added on the reference or feedback edge to cancel fractional timing error before it reaches the TDC/BBPD.

## 4. Key Blocks

| Block | Function | Main risk |
|---|---|---|
| TDC | Converts timing error to digital code | Resolution, range, gain drift, INL/DNL, metastability |
| BBPD | Converts phase sign to early/late decision | Limit cycles, jitter-dependent gain, latency sensitivity |
| Digital loop filter | Implements proportional/integral control | Coefficient scaling, word length, truncation, overflow |
| DCO | Converts tuning code to frequency | LSB size, phase noise, supply pushing, bank mismatch |
| DTC | Applies fractional timing correction | INL, mismatch, dynamic range, calibration, spur |
| Calibration loops | Track PVT and gain drift | Interaction with main loop, update noise, convergence |

## 5. Loop-Gain Bookkeeping

中文：ADPLL review 最容易出错的地方是 gain convention。TDC gain、DCO gain、divider ratio、reference period、$2\pi$ conversion 和 digital coefficient scaling 必须写在同一张表里。否则 behavioral model、RTL、MATLAB、Verilog-A 和 transistor simulation 很容易相差一个 $N$、$T_{ref}$ 或 $2\pi$。

English: The easiest ADPLL review mistake is gain convention. TDC gain, DCO gain, divider ratio, reference period, $2\pi$ conversion, and digital coefficient scaling must be documented in one table. Otherwise behavioral model, RTL, MATLAB, Verilog-A, and transistor simulation can easily differ by a factor of $N$, $T_{ref}$, or $2\pi$.

Common phase-domain definitions:

$$
K_{tdc}=\frac{T_{ref}}{2\pi t_{res}}
$$

$$
K_{dco}=2\pi f_{res}
$$

For a proportional coefficient $\alpha$:

$$
\omega_u\approx\frac{\alpha K_{tdc}K_{dco}}{N}
$$

For a digital integral coefficient $\beta$:

$$
\omega_z\approx\frac{\beta/\alpha}{T_{ref}}
$$

中文：这些公式适合 first-pass loop review。signoff 需要包括 sample/update delay、digital pipeline latency、DCO gain nonlinearity、TDC gain drift、DTC calibration residue 和 quantization noise folding。

English: These formulas are appropriate for first-pass loop review. Signoff must include sample/update delay, digital pipeline latency, DCO-gain nonlinearity, TDC-gain drift, DTC calibration residue, and quantization-noise folding.

## 6. TDC Review

中文：TDC 的三个核心指标是 resolution、range 和 linearity。高 resolution 降低 quantization noise，但可能增加 power、metastability risk 和 delay-chain sensitivity。宽 range 有助 acquisition，但在 locked state 可能浪费功耗。narrow-range TDC 对低功耗很有吸引力，但 acquisition 初期 out-of-range 行为必须小心处理，否则会把瞬时 loop gain 拉高并损害 phase margin。

English: The three core TDC metrics are resolution, range, and linearity. Fine resolution reduces quantization noise but can increase power, metastability risk, and delay-chain sensitivity. Wide range helps acquisition but can waste power in lock. Narrow-range TDCs are attractive for low power, but out-of-range behavior during acquisition must be handled carefully; otherwise instantaneous loop gain can increase and degrade phase margin.

TDC quantization variance:

$$
\sigma_{tdc}^2=\frac{t_{res}^2}{12}
$$

中文：如果 in-band noise floor 由 TDC quantization 主导，TDC gain calibration 就不只是 calibration feature，而是 loop bandwidth 和 jitter stability 的一部分。PVT 漂移会改变 $t_{res}$，进而改变 effective loop gain 和 output noise。

English: If the in-band noise floor is dominated by TDC quantization, TDC gain calibration is not just a calibration feature; it is part of loop-bandwidth and jitter stability. PVT drift changes $t_{res}$, which changes effective loop gain and output noise.

## 7. DCO Review

中文：DCO 不是 VCO 的数字名字。DCO tuning bank 的 LSB、segmentation、bank mismatch、dynamic element switching、supply pushing、substrate coupling、flicker upconversion、fine-bank noise 和 calibration update 都会进入 phase-noise and spur budget。DCO gain curve 必须作为 code-dependent quantity review，而不是单个常数。

English: A DCO is not just a VCO with a digital name. DCO tuning-bank LSB, segmentation, bank mismatch, dynamic element switching, supply pushing, substrate coupling, flicker upconversion, fine-bank noise, and calibration updates all enter the phase-noise and spur budget. The DCO gain curve must be reviewed as a code-dependent quantity, not as a single constant.

DCO frequency-step quantization:

$$
\sigma_{n,f}^2=\frac{f_{res}^2}{12}
$$

中文：DCO quantization is frequency-domain error, and phase is the integral of frequency. 因此粗 DCO LSB 会在 loop 外表现为 $1/f_m^2$ 类似的 phase-noise contribution，并可能通过 fractional modulation 或 calibration activity 形成 spurs。

English: DCO quantization is a frequency-domain error, and phase is the integral of frequency. Therefore coarse DCO LSB can appear outside the loop as a $1/f_m^2$-like phase-noise contribution and can create spurs through fractional modulation or calibration activity.

## 8. DTC-Assisted Fractional-N ADPLL

中文：DTC-assisted ADPLL 的目标是在 phase detector 之前抵消 fractional divider timing error，使 TDC/BBPD 不必承受完整 DSM-induced deterministic phase error。这个方法对 low-power fractional-N ADPLL 很有吸引力，但 DTC INL、DTC gain drift、edge slew、supply noise 和 calibration residue 可能直接变成 fractional spur。

English: A DTC-assisted ADPLL aims to cancel fractional-divider timing error before the phase detector, so the TDC/BBPD does not see the full DSM-induced deterministic phase error. This is attractive for low-power fractional-N ADPLLs, but DTC INL, gain drift, edge slew, supply noise, and calibration residue can directly become fractional spurs.

中文：Chen et al. 的 529-uW ADPLL case study 提醒一个 practical point：buffer-cascaded DTC 简单、低设计风险，但 mismatch spur 的 sizing tradeoff 很贵。约 4x power 只换来约 2x mismatch reduction，也就是 spur 大约改善 6 dB。不要把 DTC linearity 问题简单归结为“加大尺寸”。

English: The 529-uW ADPLL case study by Chen et al. gives a practical reminder: a buffer-cascaded DTC is simple and low-risk to design, but mismatch-spur sizing is expensive. About 4x power buys about 2x mismatch reduction, or roughly 6 dB spur improvement. Do not reduce DTC-linearity problems to “make devices larger.”

## 9. Common Mistakes

中文：常见错误一是把 digital coefficient 当作 physical bandwidth。没有 TDC/DCO gain、divider ratio 和 update period，digital coefficient 本身没有稳定的物理意义。

English: A common mistake is treating a digital coefficient as physical bandwidth. Without TDC/DCO gain, divider ratio, and update period, a digital coefficient has no stable physical meaning.

中文：常见错误二是只优化 locked-state jitter，而忽略 acquisition out-of-range behavior。narrow-range TDC 在 lock 后很省电，但 acquisition 时的 coarse correction 必须避免过度推 phase error。

English: A second common mistake is optimizing locked-state jitter while ignoring acquisition out-of-range behavior. A narrow-range TDC can save power after lock, but coarse correction during acquisition must avoid over-pushing phase error.

中文：常见错误三是把 ADPLL spur 全部归咎于 DSM。DTC INL、DCO bank mismatch、clock gating、snapshot timing、digital supply noise、calibration update 和 substrate coupling 都可能产生 deterministic tones。

English: A third common mistake is blaming every ADPLL spur on the DSM. DTC INL, DCO-bank mismatch, clock gating, snapshot timing, digital supply noise, calibration updates, and substrate coupling can all create deterministic tones.

## 10. Design Review Checklist

- Are TDC gain, DCO gain, divider ratio, update rate, and digital coefficients documented with units?
- Is TDC range sufficient for acquisition without destabilizing wide-band operation?
- Is TDC gain calibrated or bounded across PVT?
- Is DCO LSB small enough for jitter and spur targets?
- Is DCO phase noise separated from quantization and calibration noise?
- Are DTC INL/DNL, gain drift, mismatch, and supply sensitivity included?
- Are clock gating and snapshot circuits checked for metastability and phase offset?
- Is digital supply coupling included in phase-noise and spur simulations?
- Are behavioral, RTL, mixed-signal, and transistor-level models using the same gain conventions?

## 11. Related Notes

- [[pll_fractional_n_digital]]
- [[pll_fundamentals]]
- [[pll_phase_noise_jitter]]
- [[pfd_charge_pump_notes]]
- [[cdr_fundamentals]]
- [[dll_notes]]

## 12. Balanced Ingest 2026-07-05 - Staszewski/Balsara Phase-Domain ADPLL Sources

Source update:

- Robert Bogdan Staszewski and Poras T. Balsara, *All-Digital Frequency Synthesizer in Deep-Submicron CMOS*, Wiley, 2006.
- Robert Bogdan Staszewski et al., "All-Digital TX Frequency Synthesizer and Discrete-Time Receiver for Bluetooth Radio in 130-nm CMOS," IEEE JSSC, 2004.
- Ingest level: Balanced Ingest. The book was treated as a high-value architecture source, not as a full Deep Ingest.

### 12.1 Phase-Domain ADPLL Framing

中文：Staszewski/Balsara 的核心贡献之一是把 ADPLL 明确写成 phase-domain sampled-data system。reference phase、variable phase、fractional phase error 和 loop-filter output 都可以在数字域中用 accumulator 和 arithmetic subtractor 表示；TDC 只负责把 reference edge 与 DCO edge 之间剩余的 sub-clock timing residue 转换为数字量。这个视角很重要，因为 ADPLL 的“数字化”不是把 PLL 变成无模拟误差的系统，而是把模拟误差集中到 DCO、TDC、retiming、clock distribution 和 supply coupling 等少数边界上。

English: One central contribution of the Staszewski/Balsara ADPLL work is framing the loop as a phase-domain sampled-data system. Reference phase, variable phase, fractional phase error, and loop-filter output can be represented by digital accumulators and arithmetic subtraction; the TDC converts only the remaining sub-clock timing residue between the reference edge and the DCO edge. This matters because ADPLL "digitization" does not remove analog error; it concentrates analog error at the DCO, TDC, retiming, clock distribution, and supply-coupling boundaries.

中文：phase detector 可以变成数字减法器，而不是传统 PFD/charge-pump pulse-width-to-charge converter。这样做的工程收益是 phase comparison 本身具有精确、可重复、可扩展 word length 的特点，不再受到 charge-pump current mismatch、dead zone 和 loop-filter leakage 的同类限制。工程代价是必须严肃管理 word length、modulo arithmetic、TDC gain normalization、DCO gain normalization 和 digital pipeline latency。

English: The phase detector can become a digital subtractor instead of a traditional PFD/charge-pump pulse-width-to-charge converter. The engineering benefit is that phase comparison becomes precise, repeatable, and scalable by word length rather than being limited by charge-pump current mismatch, dead zone, and loop-filter leakage. The cost is that word length, modulo arithmetic, TDC gain normalization, DCO gain normalization, and digital pipeline latency must be managed explicitly.

### 12.2 DCO as the Central Mixed-Signal Boundary

中文：DCO 不应被看成“有数字输入的 VCO”。在 Staszewski 的 Bluetooth ADPLL 中，DCO tuning bank 使用 integer thermometer path、DEM 和 fractional sigma-delta dithering，把有限电容 LSB 转换为更细的 effective frequency resolution。若 DCO 物理 LSB 为 $\Delta f_{\mathrm{DCO}}$，fractional path 有 $B$ 个有效 fractional bits，则一阶估算为：

English: A DCO should not be treated as merely a VCO with digital inputs. In the Staszewski Bluetooth ADPLL, the DCO tuning bank uses an integer thermometer path, DEM, and fractional sigma-delta dithering to convert a finite capacitor LSB into a finer effective frequency resolution. If the physical DCO LSB is $\Delta f_{\mathrm{DCO}}$ and the fractional path has $B$ effective fractional bits, a first-order estimate is:

$$
\Delta f_{\mathrm{eff}}\approx \frac{\Delta f_{\mathrm{DCO}}}{2^B}
$$

中文：该论文中的示例约为 $23\,\mathrm{kHz}/32\approx719\,\mathrm{Hz}$ effective open-loop DCO resolution。这个数字不应转用为 SerDes 目标，但它给出一个强工程直觉：coarse physical tuning bank 可以通过高频 dithering 得到细分辨率，不过量化能量会被推到频谱中，必须由 loop filtering、DEM、spur analysis 和 DCO phase-noise budget 共同吸收。

English: The paper's example is about $23\,\mathrm{kHz}/32\approx719\,\mathrm{Hz}$ effective open-loop DCO resolution. This number is not a SerDes target, but it gives a useful engineering intuition: a coarse physical tuning bank can obtain fine effective resolution through high-rate dithering, but the quantization energy is pushed into the spectrum and must be handled by loop filtering, DEM, spur analysis, and the DCO phase-noise budget.

中文：Staszewski 的实现还强调了 time-variant DCO switching：在 LC tank 能量主要位于电感中的时刻更新 tuning word，可以减少 capacitance switching 对 amplitude 的扰动，降低 AM-to-PM 转换风险。对高性能 ADPLL/DCO review，这意味着 DCO code update timing 本身是 jitter/spur variable，而不是纯 RTL 事件。

English: Staszewski's implementation also emphasizes time-variant DCO switching: updating the tuning word when the LC tank energy is mostly in the inductor can reduce amplitude disturbance from capacitance switching and lower AM-to-PM conversion risk. For high-performance ADPLL/DCO review, this means DCO code-update timing is itself a jitter/spur variable, not just an RTL event.

### 12.3 TDC, Retiming, and Gain Normalization

中文：phase-domain ADPLL 的 TDC 应被视为唯一连续时间到数字时间误差转换点。Bluetooth JSSC paper 中 reference clock 先由 DCO clock retime，再用 TDC 提取 residual timing error；retimed reference edge strips away most reference timing information seen by later digital logic，使大规模数字逻辑可以在 TDC detection 之后的 quiet interval 运行。这个结构提醒我们：ADPLL 的 digital activity schedule 会影响 spur 和 supply-induced jitter。

English: In a phase-domain ADPLL, the TDC should be treated as the only continuous-time-to-digital timing-error conversion point. In the Bluetooth JSSC paper, the reference clock is retimed by the DCO clock and the TDC extracts the residual timing error; the retimed reference edge strips away most timing information seen by later digital logic, allowing large digital logic to run during a quiet interval after TDC detection. This structure reminds us that an ADPLL's digital-activity schedule affects spur and supply-induced jitter.

中文：TDC normalization 不能只假设一个固定 inverter delay。该 paper 通过平均多个 DCO periods 来估计 DCO period 与 inverter delay 的关系，并在 packet start 或 calibration interval 更新 normalization factor。对现代 SerDes/SoC ADPLL，这条规则仍然成立：TDC LSB、DCO period、temperature、supply 和 layout local variation 必须被绑定到 loop-gain tracking 中。

English: TDC normalization cannot simply assume a fixed inverter delay. The paper estimates the relationship between DCO period and inverter delay by averaging multiple DCO periods and updates the normalization factor at packet start or during a calibration interval. For modern SerDes/SoC ADPLLs, the rule still holds: TDC LSB, DCO period, temperature, supply, and local layout variation must be tied into loop-gain tracking.

### 12.4 Engineering Review Questions Added

| Review item | Added question |
|---|---|
| Phase-domain bookkeeping | Are reference phase, variable phase, fractional residue, and TDC residue represented with explicit units and modulo ranges? |
| DCO update timing | Is tuning-word switching aligned to a low-AM-disturbance point, or has AM-to-PM from code updates been simulated? |
| DCO fractional resolution | Is the effective fine resolution backed by DSM/DEM spectrum analysis rather than only by the average frequency step? |
| TDC normalization | Is TDC gain calibrated against actual DCO period and PVT drift? |
| Digital activity | Are retiming, accumulator update, TDC sampling, and digital switching scheduled to avoid deterministic supply tones? |

## 13. Source Provenance

| Source | Type | Reusable knowledge |
|---|---|---|
| Woogeun Rhee and Zhiping Yu, *Phase-Locked Loops: System Perspectives and Circuit Design Aspects*, Wiley/IEEE Press, 2024 | Book | DPLL/ADPLL loop model, TDC/DCO gain conventions, BBPLL and HPLL framing |
| Peng Chen et al., "A 529-uW Fractional-N All-Digital PLL Using TDC Gain Auto-Calibration and an Inverse-Class-F DCO in 65-nm CMOS," IEEE TCAS-I, 2022 | IEEE paper | Hybrid TDC, TDC gain calibration, DTC-assisted fractional-N ADPLL, DTC mismatch tradeoff, snapshot timing, inverse-class-F DCO case study |
| Nicola Da Dalt, *Theory and Implementation of Digital Bang-Bang Frequency Synthesizers for High Speed Serial Data Communications*, RWTH Aachen, 2007 | Dissertation | Bang-bang PLL nonlinear dynamics, limit cycles, BPD gain dependence, loop latency caution |
| Robert Bogdan Staszewski and Poras T. Balsara, *All-Digital Frequency Synthesizer in Deep-Submicron CMOS*, Wiley, 2006 | Book | Phase-domain ADPLL architecture, DCO/TDC normalization, DCO dithering/DEM, modulo arithmetic, gear-shifting and built-in-test framing |
| Robert Bogdan Staszewski et al., "All-Digital TX Frequency Synthesizer and Discrete-Time Receiver for Bluetooth Radio in 130-nm CMOS," IEEE JSSC, 2004 | IEEE paper | Silicon case study for DCO-based ADPLL, retimed reference/TDC operation, DCO fractional dithering, low-supply digital CMOS ADPLL implementation |
