---
title: "PFD and Charge Pump Notes"
domain: "AnalogIC_SerDes"
tags:
  - PLL
  - CPPLL
  - PFD
  - ChargePump
  - Clocking
  - PhaseNoise
  - Spur
  - SerDes
  - PCIe7
aliases:
  - pfd_charge_pump_notes
  - PFD Charge Pump
  - Charge Pump PLL Front End
created: 2026-07-05
updated: 2026-07-05
source: "Deep Ingest of Rhee and Yu, Phase-Locked Loops, Wiley/IEEE Press, 2024"
status: "active"
---

# PFD and Charge Pump Notes

## 1. Purpose and Scope

中文：这篇笔记是 PFD、phase detector 和 charge pump 的 canonical note，用来承接 PLL 书籍、论文和项目经验中关于 phase comparison、current steering、dead zone、reference spur、charge-pump noise、leakage、UP/DOWN mismatch 和 loop-filter ripple 的可复用知识。它不是 `pll_fundamentals` 的重复版本，而是把 PLL front-end 的电路级细节单独沉淀出来，方便在 SerDes clocking、PCIe PLL、CDR 和 fractional-N PLL review 中快速引用。

English: This note is the canonical note for PFDs, phase detectors, and charge pumps. It captures reusable knowledge about phase comparison, current steering, dead zone, reference spur, charge-pump noise, leakage, UP/DOWN mismatch, and loop-filter ripple from PLL books, papers, and project experience. It is not a duplicate of `pll_fundamentals`; it isolates PLL front-end circuit detail so SerDes clocking, PCIe PLL, CDR, and fractional-N PLL reviews can reference it directly.

中文：本笔记覆盖 classical phase detector、XOR detector、flip-flop detector、sample-and-hold detector、sub-sampling detector、PFD、single-ended charge pump、differential charge pump、CP loop-gain modeling、dead-zone avoidance、reference-spur formation 和 implementation checklist。loop-level stability、VCO design、fractional-N DSM 和 full CDR behavior 分别归入 [[pll_fundamentals]]、[[pll_phase_noise_jitter]]、[[pll_fractional_n_digital]] 和 [[cdr_fundamentals]]。

English: This note covers classical phase detectors, XOR detectors, flip-flop detectors, sample-and-hold detectors, sub-sampling detectors, PFDs, single-ended charge pumps, differential charge pumps, CP loop-gain modeling, dead-zone avoidance, reference-spur formation, and implementation checklists. Loop-level stability, VCO design, fractional-N DSM, and full CDR behavior belong in [[pll_fundamentals]], [[pll_phase_noise_jitter]], [[pll_fractional_n_digital]], and [[cdr_fundamentals]] respectively.

## 2. Canonical Role in the Knowledge Base

中文：当新资料讨论 PFD reset delay、charge-pump current mismatch、dead zone、leakage spur、CP output compliance、current-source switching、fractional-N nonlinearity 或 loop-filter ripple 时，默认应该 merge 到这篇 note，而不是新建 `charge_pump_design.md`、`pfd_notes.md`、`pll_spur_notes.md` 之类的重复文件。只有当资料进入具体 silicon implementation，例如一个完整 low-spur CPPLL design note，才可以建立项目级 note 并反向链接这里。

English: When a new source discusses PFD reset delay, charge-pump current mismatch, dead zone, leakage spur, CP output compliance, current-source switching, fractional-N nonlinearity, or loop-filter ripple, the default destination should be this note rather than a duplicate file such as `charge_pump_design.md`, `pfd_notes.md`, or `pll_spur_notes.md`. A project-level note is appropriate only when the source describes a concrete silicon implementation, such as a complete low-spur CPPLL design note, and that note should link back here.

Related canonical notes:

- [[pll_fundamentals]] for loop architecture, loop type, stability, and acquisition.
- [[pll_phase_noise_jitter]] for phase-noise, jitter, spur-to-time-jitter conversion, and oscillator noise.
- [[pll_loop_bandwidth]] for bandwidth routing and design tradeoffs.
- [[pll_fractional_n_digital]] for DSM quantization, fractional spurs, DPLL, BBPLL, and hybrid PLLs.
- [[cdr_fundamentals]] for phase detectors inside data-recovery loops.
- [[pcie7_clocking_notes]] for PCIe-oriented clocking interpretation.

## 3. Phase Detector Taxonomy

中文：phase detector 的核心工作是把两个 periodic signals 的 phase error 转换成电压、电流、电荷或数字码。不同 detector 的 gain、linear range、acquisition behavior、noise、spur 和 data-dependence 完全不同，因此不能只写“PD compares phase”。在 senior-level review 中，必须问清楚 detector 类型、gain definition、linear range、output waveform、lock-point behavior 和后级 loop filter 如何解释这个输出。

English: The core job of a phase detector is to convert phase error between two periodic signals into a voltage, current, charge, or digital code. Different detectors have very different gain, linear range, acquisition behavior, noise, spur, and data-dependence, so “the PD compares phase” is not enough. In a senior-level review, the detector type, gain definition, linear range, output waveform, lock-point behavior, and interpretation by the loop filter must all be explicit.

| Detector | Useful model | Strength | Risk |
|---|---|---|---|
| Multiplier / mixer PD | Sinusoidal phase detector | Simple analog model, useful for intuition | Limited linear range, double-frequency ripple |
| XOR PD | Duty-cycle-to-voltage detector | Simple digital implementation | Linear range typically around half cycle, duty-cycle sensitivity |
| Flip-flop PD | Edge-order detector | Wider phase range than XOR | Sawtooth characteristic, ripple, ambiguity outside range |
| Sample-and-hold PD | Samples VCO/reference waveform | Low output ripple, good for some low-spur PLLs | Needs acquisition aid, gain depends waveform slope |
| Sub-sampling PD | Samples high-frequency VCO with reference | Very high effective gain, can avoid divider noise in lock | Narrow lock range, kickback, reference spur, fractional-N difficulty |
| PFD | Phase-and-frequency detector | Wide acquisition, no false lock for large frequency error in normal use | Dead zone, reset delay, CP mismatch, spur |

### 3.1 Multiplier Phase Detector

中文：multiplier detector 对正弦输入的输出包含一个 phase-error DC term 和一个 twice-frequency ripple term。若两个输入为 $A\sin(\omega t+\theta)$ 与 $B\cos(\omega t)$，相乘后得到：

English: A multiplier detector with sinusoidal inputs produces a phase-error DC term and a twice-frequency ripple term. If the two inputs are $A\sin(\omega t+\theta)$ and $B\cos(\omega t)$, the product is:

$$
v_p(t)=\frac{AB}{2}\sin\theta+\frac{AB}{2}\sin(2\omega t+\theta)
$$

中文：小信号下 $\sin\theta\approx\theta$，因此 phase-detector gain 为：

English: Under small-signal conditions, $\sin\theta\approx\theta$, so the phase-detector gain is:

$$
K_d=\frac{AB}{2}
$$

中文：这个模型适合建立 intuition，但在 integrated CPPLL 中不应直接替代 PFD/CP 的 switched-current behavior。真实 CPPLL 的 phase error 先被转换为 pulse width，再转换为 charge packet，最后经 loop filter 转为 VCO control voltage。

English: This model is useful for intuition, but it should not replace the switched-current behavior of a PFD/CP in an integrated CPPLL. In a real CPPLL, phase error first becomes pulse width, then charge packet, and finally VCO control voltage through the loop filter.

### 3.2 XOR and Flip-Flop Phase Detectors

中文：XOR detector 把 phase difference 变成 duty-cycle difference。对 rail-to-rail digital signal，常用小信号 gain 近似为：

English: An XOR detector converts phase difference into duty-cycle difference. For rail-to-rail digital signals, a common small-signal gain approximation is:

$$
K_d=\frac{V_{DD}}{\pi}
$$

中文：XOR PD 的线性范围通常围绕 $\pm\pi/2$，并且对输入 duty cycle 和波形对称性敏感。它适合教学和某些 DLL/CDR 场景，但不适合需要大 acquisition range 和 low spur 的 general-purpose frequency synthesizer。

English: The XOR PD is usually linear around $\pm\pi/2$ and is sensitive to input duty cycle and waveform symmetry. It is useful for teaching and some DLL/CDR settings, but it is not ideal for a general-purpose frequency synthesizer requiring large acquisition range and low spur.

中文：flip-flop detector 可以提供更宽的 phase range。常用 gain 近似为：

English: A flip-flop detector can provide wider phase range. A common gain approximation is:

$$
K_d=\frac{V_{DD}}{2\pi}
$$

中文：flip-flop detector 的输出 characteristic 更接近 sawtooth，因此它的 ripple、wrap-around 和 large-signal behavior 必须在 loop analysis 中处理。不要把它和 PFD 混为一谈；PFD 有 frequency-detection behavior，而简单 flip-flop PD 不一定有可靠的 frequency acquisition。

English: The flip-flop detector has a more sawtooth-like characteristic, so ripple, wrap-around, and large-signal behavior must be handled in loop analysis. It should not be confused with a PFD; a PFD has frequency-detection behavior, while a simple flip-flop PD may not provide reliable frequency acquisition.

### 3.3 Sample-and-Hold and Sub-Sampling Detectors

中文：sample-and-hold PD 通过采样某个周期波形的斜率把 phase error 转换为电压误差。若最大控制幅度近似为 $V_{Cmax}$，常用 gain 可写为：

English: A sample-and-hold PD converts phase error into voltage error by sampling the slope of a periodic waveform. If the maximum control amplitude is approximated as $V_{Cmax}$, a common gain model is:

$$
K_d=\frac{V_{Cmax}}{2\pi}
$$

中文：S/H PD 的一个优势是 held output 在 lock 附近比较安静，因此 reference spur 可以较低。但它通常需要额外 acquisition circuit，因为 detector 只在有限 phase range 内提供可靠信息。

English: One advantage of a S/H PD is that the held output can be quiet near lock, which can reduce reference spur. However, it usually needs an additional acquisition circuit because the detector gives reliable information only over a limited phase range.

中文：sub-sampling PD 直接用 reference edge 采样高频 VCO waveform，等效 PD gain 来自 VCO waveform 的 slope，因此 gain 可以很高。高 PD gain 可以降低 charge-pump noise 的 input-referred effect，也可以在 locked state 避免 divider noise，但它把系统风险转移到 reference path、sampler kickback、false lock、frequency acquisition、DTC/DSM compensation 和 spur isolation。

English: A sub-sampling PD samples the high-frequency VCO waveform directly with the reference edge. The effective PD gain comes from the VCO waveform slope and can be high. High PD gain can reduce the input-referred effect of charge-pump noise and avoid divider noise in lock, but it shifts system risk to the reference path, sampler kickback, false lock, frequency acquisition, DTC/DSM compensation, and spur isolation.

## 4. PFD Operation

中文：PFD 的基本输出状态是 UP、DOWN 和 neutral。reference edge 先到时，UP pulse 拉高；feedback edge 先到时，DOWN pulse 拉高；两边 edge 都到达后 reset 回 neutral。这个结构让 PFD 不仅检测 phase error，也能在 feedback frequency 明显错误时持续给出方向正确的 correction，因此更准确的名字是 phase-and-frequency detector。

English: A PFD has three basic output states: UP, DOWN, and neutral. If the reference edge arrives first, the UP pulse goes high; if the feedback edge arrives first, the DOWN pulse goes high; after both edges have arrived, reset returns the detector to neutral. This structure lets the PFD detect not only phase error but also a clear frequency error, so “phase-and-frequency detector” is the more accurate name.

中文：PFD 的 nominal detection range 可以接近 $\pm 2\pi$，比 XOR 或 simple flip-flop detector 更适合 PLL acquisition。这个能力对 SerDes clocking 很关键，因为上电、频率切换、spread-spectrum tracking 或 divider reconfiguration 期间，loop 需要避免 false lock 并能回到目标频率。

English: The nominal detection range of a PFD can approach $\pm 2\pi$, which makes it more suitable for PLL acquisition than XOR or simple flip-flop detectors. This is important in SerDes clocking because during power-up, frequency switching, spread-spectrum tracking, or divider reconfiguration, the loop must avoid false lock and return to the target frequency.

中文：PFD gain 本身通常不直接以 volts/rad 使用，而是和 charge-pump current 合并为 current-domain detector gain。若 charge pump current 为 $I_{CP}$，PFD/CP 的等效 gain 为：

English: PFD gain is often not used directly as volts/radian; it is combined with charge-pump current into a current-domain detector gain. If the charge-pump current is $I_{CP}$, the equivalent PFD/CP gain is:

$$
K'_d=\frac{I_{CP}}{2\pi}
$$

中文：如果 loop filter 中的 resistor $R_1$ 把 current pulse 转成控制电压的 proportional path，则等效 voltage-domain gain 可近似为：

English: If the loop-filter resistor $R_1$ converts the current pulse into a proportional control-voltage path, the equivalent voltage-domain gain can be approximated as:

$$
K_d=\frac{I_{CP}R_1}{2\pi}
$$

## 5. Dead Zone and Minimum Turn-On Time

中文：dead zone 指小 phase error 下 PFD/CP 没有产生有效 output charge 的区域。常见原因是 PFD reset pulse 太短、UP/DOWN driver drive strength 不足、charge pump switch 没有完全打开、current source settling 太慢，或者 CP output node 电压让 current source 进入 poor-compliance region。

English: Dead zone is the region where a small phase error produces no effective output charge from the PFD/CP. Common causes include too-short PFD reset pulses, weak UP/DOWN drivers, charge-pump switches that do not fully turn on, slow current-source settling, or a CP output voltage that pushes current sources into poor compliance.

中文：dead zone 会降低 effective loop gain，并把 small phase error 转换成随机或数据相关的 timing uncertainty。在 phase-noise view 中，它常表现为 in-band noise 变差；在 time-domain view 中，它表现为 residual phase dithering、limit-cycle-like behavior 或 lock point jitter。

English: Dead zone reduces effective loop gain and converts small phase error into random or data-dependent timing uncertainty. In the phase-noise view, it often worsens in-band noise; in the time-domain view, it appears as residual phase dithering, limit-cycle-like behavior, or lock-point jitter.

中文：常用修复方法是在 PFD reset path 中加入 minimum turn-on delay，使 zero phase error 时 UP 和 DOWN 都短暂打开。这个技巧消除 dead zone，但不是 free lunch：过大的 minimum pulse width 会增加 charge-pump noise duty ratio、reference ripple、current mismatch sensitivity，并且可能在高 reference frequency 下损害 acquisition。

English: A common fix is to add a minimum turn-on delay in the PFD reset path so both UP and DOWN briefly turn on at zero phase error. This removes dead zone, but it is not free: excessive minimum pulse width increases charge-pump noise duty ratio, reference ripple, current-mismatch sensitivity, and can hurt acquisition at high reference frequency.

## 6. Charge Pump Loop Modeling

中文：二阶 Type-II CPPLL 的一阶设计模型来自 charge pump、loop-filter capacitor、loop-filter resistor 和 VCO integrator 的组合。对最简单的 $R_1$-$C_1$ filter，open-loop transfer function 可写为：

English: The first design model for a second-order Type-II CPPLL comes from the combination of charge pump, loop-filter capacitor, loop-filter resistor, and VCO integrator. For the simplest $R_1$-$C_1$ filter, the open-loop transfer function can be written as:

$$
G(s)=\frac{I_{CP}K_v(1+sR_1C_1)}{2\pi C_1s^2}
$$

中文：这个表达式中的两个 integrator 分别来自 loop-filter capacitor 的 charge integration 和 VCO 的 phase integration。$R_1$ 引入 zero，用来提供 damping。如果没有这个 zero，Type-II loop 会更容易出现 peaking、ringing 或 instability。

English: The two integrators in this expression come from charge integration by the loop-filter capacitor and phase integration by the VCO. The resistor $R_1$ introduces a zero that provides damping. Without this zero, the Type-II loop is more prone to peaking, ringing, or instability.

中文：常用近似参数为：

English: Common approximate parameters are:

$$
\omega_u \approx \frac{I_{CP}R_1K_v}{2\pi}
$$

$$
\omega_z=\frac{1}{R_1C_1}
$$

$$
\omega_n=\sqrt{\frac{I_{CP}K_v}{2\pi C_1}}
$$

$$
\zeta=\frac{R_1}{2}\sqrt{\frac{I_{CP}C_1K_v}{2\pi}}
$$

中文：这些公式适合 first-pass sizing，但不应该替代 transistor-level verification。真实设计还需要包含 divider ratio、VCO gain curve、loop-filter parasitics、reference-rate sampling、CP current mismatch、switching glitches、PFD delay、package/supply coupling 和 PVT variation。

English: These formulas are good for first-pass sizing, but they should not replace transistor-level verification. A real design must also include divider ratio, VCO gain curve, loop-filter parasitics, reference-rate sampling, CP current mismatch, switching glitches, PFD delay, package/supply coupling, and PVT variation.

## 7. Third-Order CPPLL and Ripple Capacitor

中文：实际 CPPLL 很少只用理想二阶 $R_1$-$C_1$ loop filter，因为 charge-pump pulse 会在 VCO control node 产生 reference-rate ripple，可能导致 reference spur、VCO pulling、调谐节点饱和或 supply/coupling sensitivity。常见做法是加入 shunt capacitor $C_2$ 和其他高频 pole 来降低 ripple。

English: A practical CPPLL rarely uses only an ideal second-order $R_1$-$C_1$ loop filter because charge-pump pulses create reference-rate ripple on the VCO control node. This can produce reference spur, VCO pulling, tuning-node saturation, or supply/coupling sensitivity. A common approach is to add a shunt capacitor $C_2$ and other high-frequency poles to reduce ripple.

中文：高阶 loop filter 的常用近似为：

English: A common approximation for a higher-order loop filter is:

$$
\omega_u \approx \frac{I_{CP}R_1K_v}{2\pi}
$$

$$
\omega_z \approx \frac{1}{R_1C_1}
$$

$$
\omega_{p1}\approx \frac{1}{R_1C_2}
$$

$$
\omega_{p2}\approx \frac{1}{R_pC_p}
$$

中文：设计 tradeoff 是明确的：$C_2$ 降低 ripple 和 reference spur，但引入额外 pole 并降低 phase margin。一个好的 design review 不会只问 spur 是否变低，而会同时检查 phase margin、settling、jitter peaking、sampled-data stability 和 worst-case PVT 下的 VCO control range。

English: The design tradeoff is explicit: $C_2$ reduces ripple and reference spur, but it adds an extra pole and reduces phase margin. A good design review does not ask only whether the spur is lower; it also checks phase margin, settling, jitter peaking, sampled-data stability, and VCO control range across worst-case PVT.

## 8. Spur Mechanisms from PFD and Charge Pump

中文：reference spur 的根源通常是 reference-rate periodic disturbance 被 VCO gain 转换成 phase modulation。PFD/CP 相关来源包括 UP/DOWN mismatch、CP leakage、reset pulse feedthrough、switch charge injection、loop-filter ripple、divider waveform coupling、reference buffer coupling 和 substrate/supply coupling。

English: Reference spur usually comes from a reference-rate periodic disturbance that is converted by VCO gain into phase modulation. PFD/CP-related sources include UP/DOWN mismatch, CP leakage, reset-pulse feedthrough, switch charge injection, loop-filter ripple, divider waveform coupling, reference-buffer coupling, and substrate/supply coupling.

中文：若 leakage current 为 $I_{leak}$，static phase error 可近似为：

English: If the leakage current is $I_{leak}$, the static phase error can be approximated as:

$$
\theta_e=\frac{2\pi I_{leak}}{I_{CP}}
$$

中文：leakage 通过 loop-filter resistor 形成 periodic control-voltage component 时，reference spur 的 rough estimate 可以写为：

English: When leakage creates a periodic control-voltage component through the loop-filter resistor, a rough reference-spur estimate is:

$$
P_{spur}=20\log_{10}\left(\frac{I_{leak}R_1K_v}{f_{ref}}\right)
$$

中文：这个公式的价值不是提供 signoff 数字，而是揭示 scaling：更大 leakage、更大 $R_1$、更大 $K_v$、更低 $f_{ref}$ 都会恶化 spur。signoff 必须用 actual switching waveform、loop-filter impedance、VCO gain curve、layout coupling 和 transient/PSS/PNoise/PXF 仿真确认。

English: The value of this formula is not to provide a signoff number, but to expose scaling: larger leakage, larger $R_1$, larger $K_v$, and lower $f_{ref}$ all worsen spur. Signoff must use the actual switching waveform, loop-filter impedance, VCO gain curve, layout coupling, and transient/PSS/PNoise/PXF simulation.

## 9. Spur-to-Jitter Interpretation

中文：narrowband spur 可以看成窄带 FM。若 modulation index 为 $m=\Delta f_{pk}/f_m=\Delta\theta_{pk}$，单边 spur level 近似为：

English: A narrowband spur can be interpreted as narrowband FM. If the modulation index is $m=\Delta f_{pk}/f_m=\Delta\theta_{pk}$, the single-sideband spur level is approximately:

$$
P_{spur}=20\log_{10}\left(\frac{m}{2}\right)
$$

中文：对应的 deterministic jitter 近似为：

English: The corresponding deterministic jitter can be approximated as:

$$
DJ=\frac{m}{\pi}\;\mathrm{UI}
$$

中文：Rhee 和 Yu 给出的实用例子是：若希望 deterministic jitter 小于 $0.01\,\mathrm{UI}$，则 $m<\pi/100$，对应 spur 大约低于 $-36\,\mathrm{dBc}$；留 3 dB margin 时，$-40\,\mathrm{dBc}$ 可作为一个工程警戒线。这个数字不是 PCIe 规范，也不是所有系统的 pass/fail threshold，而是把 spur 与 UI-level timing error 联系起来的 sanity check。

English: Rhee and Yu give a useful example: if deterministic jitter should be below $0.01\,\mathrm{UI}$, then $m<\pi/100$, corresponding to a spur below about $-36\,\mathrm{dBc}$; with 3 dB margin, $-40\,\mathrm{dBc}$ can be used as an engineering warning line. This is not a PCIe specification and not a universal pass/fail threshold; it is a sanity check connecting spur to UI-level timing error.

## 10. Single-Ended Charge Pump Tradeoffs

中文：single-ended tri-state charge pump 的优势是 power 和 noise 通常较低，因为 locked state 下只有 minimum turn-on window 导通。它也适合 external loop filter 或 large on-chip capacitor，因为 output node 可以直接驱动 loop filter。

English: A single-ended tri-state charge pump often has lower power and noise because in lock it conducts only during the minimum turn-on window. It is also convenient for external loop filters or large on-chip capacitors because the output node directly drives the loop filter.

中文：主要风险是 UP/DOWN current mismatch、output compliance、switch charge injection、leakage、current-source channel-length modulation、loop-filter node coupling 和 PVT current variation。对于 fractional-N PLL，CP nonlinearity 尤其危险，因为 deterministic divider timing error 和 DSM quantization residue 会被 nonlinear CP 转换成 in-band noise 与 fractional spur。

English: The main risks are UP/DOWN current mismatch, output compliance, switch charge injection, leakage, current-source channel-length modulation, loop-filter-node coupling, and PVT current variation. In a fractional-N PLL, CP nonlinearity is especially dangerous because deterministic divider timing error and DSM quantization residue can be converted by nonlinear CP behavior into in-band noise and fractional spur.

## 11. Differential Charge Pump Tradeoffs

中文：differential charge pump 可以改善 common-mode coupling immunity、UP/DOWN matching、output compliance 和 substrate/supply rejection。它对 fully differential loop filter、high-swing VCO control 和 aggressive noise environment 更有吸引力。

English: A differential charge pump can improve common-mode coupling immunity, UP/DOWN matching, output compliance, and substrate/supply rejection. It is attractive for fully differential loop filters, high-swing VCO control, and aggressive noise environments.

中文：代价是 power 和 intrinsic noise 往往更高，因为 differential architecture 可能需要持续 bias current 或更复杂 common-mode feedback。建模时不要随意把 single-ended 与 differential gain 混合；若把 differential loop filter 折算成 single-ended model，最好把 factor of two 明确放入 $I_{CP}$ 或等效 detector gain，并保持 $K_v$ 与 $R_1$ 的定义一致。

English: The cost is often higher power and intrinsic noise because a differential architecture may require continuous bias current or more complex common-mode feedback. In modeling, do not casually mix single-ended and differential gains; if a differential loop filter is reduced to a single-ended model, place the factor of two explicitly into $I_{CP}$ or equivalent detector gain and keep the definitions of $K_v$ and $R_1$ consistent.

## 12. Switch Placement and Current Steering

中文：charge pump switch 可以放在 source、gate 或 drain path，不同选择改变 switching speed、glitch、noise 和 compliance。source-switching 可以兼顾较快 switching、较低 power 和较低 noise；gate-switching 可能受大 gate capacitance 限制而较慢；drain-switching 快，但更容易把 glitch 和 charge injection 直接耦合到 output node。

English: Charge-pump switches can be placed in the source, gate, or drain path, and the choice changes switching speed, glitch, noise, and compliance. Source switching can offer fast switching with low power and low noise; gate switching can be slower because of large gate capacitance; drain switching is fast but more likely to couple glitches and charge injection directly to the output node.

中文：不要仅凭 schematic topology 判断 CP 好坏。必须用 transistor-level transient 检查 UP/DOWN edge overlap、current settling、output-voltage dependence、temperature corners、low-supply corners、mismatch corners、minimum pulse width 和 loop-filter ripple。

English: Do not judge a charge pump only from its schematic topology. Transistor-level transient simulation must check UP/DOWN edge overlap, current settling, output-voltage dependence, temperature corners, low-supply corners, mismatch corners, minimum pulse width, and loop-filter ripple.

## 13. Engineering Workflow

中文：PFD/CP review 的推荐流程是先固定 loop-level target，再回到电路实现，而不是先画 charge pump 再猜 loop bandwidth。第一步确认 output frequency、reference frequency、divider ratio、target loop bandwidth、phase margin、settling time、spur budget、integrated jitter budget 和 VCO gain range。第二步用 CPPLL equations 估算 $I_{CP}$、$R_1$、$C_1$、$C_2$。第三步用 transistor-level CP waveform 提取 effective charge per radian。第四步把实际 waveform 放回 loop simulation 和 spur/noise estimation。

English: The recommended PFD/CP review flow is to fix loop-level targets first and then return to the circuit implementation, rather than drawing a charge pump first and guessing loop bandwidth. First confirm output frequency, reference frequency, divider ratio, target loop bandwidth, phase margin, settling time, spur budget, integrated jitter budget, and VCO gain range. Second use CPPLL equations to estimate $I_{CP}$, $R_1$, $C_1$, and $C_2$. Third extract effective charge per radian from transistor-level CP waveforms. Fourth feed the actual waveform back into loop simulation and spur/noise estimation.

中文：对 SerDes/PCIe clocking，额外 workflow 是把 CP spur 和 PLL output jitter 映射到 final clock distribution、PI/CDR、sampler aperture 和 PAM4 UI。一个 CP spur 在 PLL output 处看似可接受，也可能在 clock tree resonance、supply coupling 或 CDR tracking band 中变成系统性 timing margin loss。

English: For SerDes/PCIe clocking, an additional workflow is to map CP spur and PLL output jitter into final clock distribution, PI/CDR, sampler aperture, and PAM4 UI. A CP spur that looks acceptable at the PLL output can still become systematic timing-margin loss through clock-tree resonance, supply coupling, or the CDR tracking band.

## 14. Common Mistakes

中文：常见错误一是只用 ideal $K_d=I_{CP}/2\pi$ 而不验证 minimum pulse width 下的 effective charge。真实 CP current pulse 有 finite edge rate、settling tail、switch feedthrough 和 compliance dependence，small phase error 下的有效 gain 可能明显低于公式值。

English: A common mistake is to use the ideal $K_d=I_{CP}/2\pi$ without verifying the effective charge under minimum pulse width. A real CP current pulse has finite edge rate, settling tails, switch feedthrough, and compliance dependence, so the effective gain under small phase error can be much lower than the formula value.

中文：常见错误二是用 mismatch-only thinking 解释 reference spur。UP/DOWN mismatch 重要，但 leakage、reset pulse timing、divider coupling、reference buffer coupling、loop-filter parasitic pole 和 VCO supply pushing 都可能支配 spur。

English: A second common mistake is to explain reference spur only through UP/DOWN mismatch. Mismatch matters, but leakage, reset-pulse timing, divider coupling, reference-buffer coupling, loop-filter parasitic poles, and VCO supply pushing can dominate the spur.

中文：常见错误三是为了降低 ripple 盲目增大 $C_2$。如果额外 pole 太接近 unity-gain frequency，phase margin 和 jitter peaking 可能恶化，settling time 也可能超出系统要求。

English: A third common mistake is to blindly increase $C_2$ to reduce ripple. If the added pole is too close to unity-gain frequency, phase margin and jitter peaking can degrade, and settling time can exceed system requirements.

## 15. Deep-Ingest Interview Questions

中文：Q1：为什么 CPPLL 需要 minimum PFD reset delay？好答案应该同时提到 dead zone removal、UP/DOWN both-on window、in-band phase-noise improvement，以及过大 reset delay 对 CP noise、spur 和 acquisition 的副作用。

English: Q1: Why does a CPPLL need minimum PFD reset delay? A good answer mentions dead-zone removal, the UP/DOWN both-on window, in-band phase-noise improvement, and the side effects of excessive reset delay on CP noise, spur, and acquisition.

中文：Q2：如何从 charge-pump leakage 推出 reference spur 的 scaling？好答案应指出 leakage 造成 static phase error 与 periodic control disturbance，并解释 spur 随 $I_{leak}$、$R_1$、$K_v$ 增大而恶化，随 $f_{ref}$ 增大而改善。

English: Q2: How does charge-pump leakage scale reference spur? A good answer points out that leakage causes static phase error and periodic control disturbance, and explains why spur worsens with larger $I_{leak}$, $R_1$, and $K_v$, and improves with higher $f_{ref}$.

中文：Q3：为什么 fractional-N PLL 对 CP nonlinearity 特别敏感？好答案应说明 DSM residue 和 divider timing error 会持续扫过 PFD/CP characteristic，非线性把高频 shaped noise 或 deterministic pattern fold 回 in-band noise 与 fractional spur。

English: Q3: Why is a fractional-N PLL especially sensitive to CP nonlinearity? A good answer explains that DSM residue and divider timing error continuously sweep across the PFD/CP characteristic, and nonlinearity folds shaped noise or deterministic patterns back into in-band noise and fractional spur.

## 16. Quality Checklist

- The detector type is named explicitly.
- $K_d$, $I_{CP}$, $R_1$, $C_1$, $C_2$, $K_v$, divider ratio, and reference frequency use consistent units.
- Minimum pulse width and dead-zone behavior are verified at transistor level.
- UP/DOWN current mismatch is checked across output voltage and PVT.
- CP leakage and loop-filter leakage are included in spur analysis.
- Loop-filter ripple is checked together with phase margin and jitter peaking.
- Fractional-N operation is checked with CP nonlinearity, not only ideal DSM noise.
- Spur is translated to time jitter or UI when it matters for SerDes.
- The final conclusion separates first-pass formulas from signoff simulation.

## 17. Balanced Ingest 2026-07-05 - AMS CPPLL Review Checklist

Source update:

- Zhao Zhang, "CMOS analog and mixed-signal phase-locked loops: An overview," *Journal of Semiconductors*, 2020.
- Ingest level: Balanced Ingest. This review source reinforces existing CPPLL/PFD rules rather than replacing primary textbook or circuit-paper sources.

中文：Zhang 的 AMS PLL overview 对本 note 的主要价值是提供一个 compact CPPLL issue checklist。它再次强调 charge-pump current mismatch、loop-filter ripple、large passive capacitor pressure、fractional-N PFD/CP nonlinearity、divider noise 和 settling/bandwidth tradeoff 是 CPPLL 架构选择中的 recurring issues。因为这些内容已由 [[pll_fundamentals]]、[[pll_phase_noise_jitter]] 和本 note 详细承接，这里只把它作为 review-level confirmation source。

English: Zhang's AMS PLL overview is most useful here as a compact CPPLL issue checklist. It reinforces that charge-pump current mismatch, loop-filter ripple, large passive-capacitor pressure, fractional-N PFD/CP nonlinearity, divider noise, and settling/bandwidth tradeoff are recurring issues in CPPLL architecture selection. Because these topics are already captured in [[pll_fundamentals]], [[pll_phase_noise_jitter]], and this note, it is used here only as a review-level confirmation source.

中文：该综述中一个值得保留的 caution 是：narrow bandwidth 可以降低 reference spur 和 fractional DSM quantization residue，但会拉长 lock time，并降低对 VCO noise 的 suppression；large charge-pump current 可以降低某些 in-band noise contribution，但增加功耗、switching transient 和 layout/coupling 压力。换句话说，CPPLL 的 low-jitter 不是单旋钮优化，而是 bandwidth、settling、spur、power、area、noise source partition 和 implementation nonlinearity 的联合 tradeoff。

English: One useful caution from the review is that narrow bandwidth can reduce reference spur and fractional DSM quantization residue, but lengthens lock time and weakens VCO-noise suppression; large charge-pump current can reduce some in-band noise contributions, but increases power, switching transients, and layout/coupling pressure. In other words, low-jitter CPPLL design is not a one-knob optimization; it is a joint tradeoff among bandwidth, settling, spur, power, area, noise-source partitioning, and implementation nonlinearity.

中文：对 fractional-N CPPLL，最危险的路径仍然是 shaped DSM quantization residue 被 PFD/CP nonlinearity 折回 in-band，或转换为 fractional spur。review 时不要只看 ideal DSM noise transfer；必须检查 PFD reset、CP pulse settling、UP/DOWN mismatch、loop-filter ripple、DTC/DAC compensation residue 和 supply/substrate coupling。

English: For fractional-N CPPLLs, the most dangerous path remains shaped DSM quantization residue being folded in-band by PFD/CP nonlinearity or converted into fractional spur. In review, do not look only at the ideal DSM noise transfer; check PFD reset, CP pulse settling, UP/DOWN mismatch, loop-filter ripple, DTC/DAC compensation residue, and supply/substrate coupling.

## 18. Source Provenance

| Source | Type | Status | Reusable knowledge promoted |
|---|---|---|---|
| Woogeun Rhee and Zhiping Yu, *Phase-Locked Loops: System Perspectives and Circuit Design Aspects*, Wiley/IEEE Press, 2024 | Book PDF | Deep Ingest 2026-07-05; archived under `90_Archive/processed/2026/books/phase_locked_loops_rhee_yu_2024/` | Phase detector taxonomy, PFD behavior, dead-zone and reset-delay tradeoff, CP gain equations, loop-filter ripple and higher-order CPPLL pole intuition, single-ended/differential CP tradeoffs, reference-spur and leakage scaling |
| Zhao Zhang, "CMOS analog and mixed-signal phase-locked loops: An overview," *Journal of Semiconductors*, 2020 | Review paper PDF | Balanced Ingest 2026-07-05; archived under `90_Archive/processed/2026/papers/zhang_cmos_ams_pll_overview_2020/` | Review-level CPPLL issue checklist: CP mismatch, loop-filter ripple, bandwidth/settling tradeoff, fractional-N PFD/CP nonlinearity, divider noise, AMS versus ADPLL architecture caution |

## 19. Future Evolution

中文：未来扩展这篇 note 时，应优先加入 transistor-level CP design examples、layout coupling case studies、PSS/PNoise/PXF simulation recipes、fractional-N CP linearization methods、sub-sampling PD/DTC compensation detail，以及 PCIe/SerDes lab spur debug workflow。不要把 full PLL architecture 或 VCO phase-noise theory 重复复制到这里；那些内容应继续保留在相关 canonical notes 中。

English: Future growth of this note should prioritize transistor-level CP design examples, layout-coupling case studies, PSS/PNoise/PXF simulation recipes, fractional-N CP linearization methods, sub-sampling PD/DTC compensation detail, and PCIe/SerDes lab spur-debug workflows. Do not copy full PLL architecture or VCO phase-noise theory here; those topics should remain in their own canonical notes.
