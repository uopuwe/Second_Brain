---
title: "224G SerDes PLL：Spec Matrix、完整规格与电路参数推导"
subtitle: "从系统语言到 PLL 架构、模块参数、晶体管目标与 PDK sizing"
author: ""
date: "2026-07-19"
lang: zh-CN
---

# 文档说明

本文合并并整理以下三部分内容：

1.  **Spec Compliance Matrix 的真正作用**：如何把 BER、UI、eye margin、protocol mask、CDR tracking 等系统语言，翻译成 PLL/clocking 工程师可以直接设计和验证的电路语言。
2.  **一个 224G SerDes PLL/CMU 的完整 Spec 实例**：以 224 Gb/s PAM4、112 GBd、14 GHz 1/8-rate shared CMU 为例，给出从系统目标、jitter budget、phase-noise mask，到 PFD、charge pump、loop filter、VCO、divider、spur、供电、校准、PVT、Monte Carlo 和 signoff 的完整规格。
3.  **从 Spec 到架构与具体电路参数**：给出频率规划、环路滤波器、VCO tank、粗细调谐、启动跨导、PFD/CP、divider、输出 buffer、供电隔离及 PDK sizing 的计算流程。

> **重要说明**：本文中的 `[A]` 表示架构假设，`[D]` 表示由上游条件推导出的内部设计指标，`[P]` 表示公开论文或标准讨论中的参考信息。除明确标记为公开来源的内容外，数值均为工程设计实例，不能冒充 OIF、IEEE 或某篇论文的强制规范。毕竟把示例数字抄进正式 spec，是项目中最省时间、也最贵的一种错误。

# 第一部分：Spec Matrix 的真正作用

## 1.1 Spec Matrix 不是需求清单，而是翻译系统

Spec Compliance Matrix 的核心价值，不是把要求、负责人和截止日期排列得像一份行政表格，而是建立一条**可计算、可分配、可验证、可追溯**的规格翻译链：

$$\boxed{\text{系统性能要求} \rightarrow \text{观测节点与测量条件} \rightarrow \text{噪声/抖动预算} \rightarrow \text{模块级指标} \rightarrow \text{电路参数} \rightarrow \text{晶体管与版图约束}}$$

系统团队通常讨论：

- BER；
- UI；
- eye height 和 eye width；
- protocol mask；
- COM；
- sRJ、dJ 和 TJ；
- JTOL、JTRAN；
- CDR tracking；
- pre-FEC 和 post-FEC BER；
- interoperability。

而 PLL、CMU 和 clocking 设计工程师真正能直接控制的是：

$$f_{PFD},\quad N,\quad BW_{PLL},\quad I_{CP},\quad K_{VCO}/K_{DCO}$$

以及：

$$\text{VCO range},\quad\text{divider topology},\quad\text{DTC/TDC resolution},\quad\text{phase-rotator LSB}$$

再加上：

$$\text{supply isolation},\quad\text{clock-buffer slew},\quad\text{calibration policy},\quad\text{servo update rate}$$

Matrix 的作用，就是把“链路是否能工作”转换成“这些电路旋钮应该满足什么范围，以及如何证明满足”。

## 1.2 为什么普通需求表不能指导 PLL 设计

一张普通项目表可能只有：

| Spec      | Target       | Owner | Status |
|-----------|--------------|-------|--------|
| TX jitter | < 55 fs RMS | PLL   | Open   |

这张表对电路设计几乎没有可执行价值，因为它没有回答：

- 55 fs 是在哪个节点测量？
- 是 PLL core 输出、shared CMU 输出，还是 TX serializer 的最终数据 crossing？
- 是 raw jitter，还是经过 4 MHz reference CRU/CDR 后的 residual jitter？
- 积分频带的下限和上限是什么？
- 是否包含 reference spur、fractional spur、supply spur 和 calibration spur？
- 是否包含 global clock distribution、lane CCU、ILO、phase shifter 和 phase rotator？
- 55 fs 是否包含 measurement floor？
- 是 typical 结果，还是 PVT、mismatch、PEX 和 all-lane activity 下的 signoff 指标？
- calibration 是 active、converged，还是 frozen？

如果这些语义没有定义，“55 fs”只是一个带单位的愿望。它可以用于会议，但无法用于 sizing、noise budget、testbench 或 signoff。

一个合格的 Spec Matrix 至少承担四项任务：

1.  **语义翻译**：指标究竟在什么条件下代表什么。
2.  **预算分解**：哪些模块各自允许贡献多少。
3.  **设计反推**：这些预算对应哪些架构和电路参数。
4.  **验证闭环**：用什么模型、滤波、testbench 和 pass/fail 判据证明满足。

## 1.3 “TX endpoint RMS jitter < 55 fs”包含哪些隐藏条件

假设系统给出：

> 在 224 Gb/s PAM4 mode 下，TX endpoint clock RMS jitter 小于 55 fs，测量采用 4 MHz reference CDR/CRU filter。

这句话至少要展开成以下层级。

### 1.3.1 Mode

224 Gb/s PAM4 的 symbol rate 为：

$$R_{s} = \frac{224\ Gb/s}{2} = 112\ GBd$$

Symbol UI 为：

$$UI = \frac{1}{112\ GHz} = 8.929\ ps$$

因此：

$$55\ fs = \frac{55\ fs}{8.929\ ps} = 0.00616\ UI = 6.16\ mUI$$

同一个 fs 数字若用于 NRZ、PAM4、112G、224G、1/8-rate 或 full-rate 节点，其系统意义完全不同。Matrix 必须记录：

- protocol mode；
- symbol rate；
- internal clock rate；
- reference frequency；
- divider ratio；
- clock-generation topology；
- backward-compatible mode 是否适用。

### 1.3.2 Node

下列节点的 jitter 不能混写：

1.  VCO core 输出；
2.  PLL divider 前的高速输出；
3.  shared CMU 输出；
4.  global clock distribution 末端；
5.  lane-local CCU 输出；
6.  1/8-rate serializer clock；
7.  ILO 输出；
8.  phase shifter 输出；
9.  phase rotator 输出；
10. serializer 最后一层 mux clock；
11. TX pad 处数据 crossing；
12. 经过 reference CRU 后观测到的 TX residual jitter。

若 PLL 输出 jitter 为 $40\ fs$，不代表 TX endpoint 也是 $40\ fs$。Endpoint 还会增加：

$$\sigma_{dist},\quad\sigma_{CCU},\quad\sigma_{ILO},\quad\sigma_{PS},\quad\sigma_{PR},\quad\sigma_{mux},\quad\sigma_{supply}$$

若各噪声源不相关：

$$\boxed{\sigma_{endpoint}^{2} = \sum_{i}^{}\sigma_{i}^{2}}$$

若存在相关性：

$$\boxed{\sigma_{endpoint}^{2} = \sum_{i}^{}{\sum_{j}^{}\rho_{ij}}\sigma_{i}\sigma_{j}}$$

其中 $\rho_{ij}$ 为相关系数。Shared supply noise、common reference modulation 或同源数字耦合都可能引入相关项，因此不能机械地对所有数字做 RSS。

## 1.4 Raw jitter 与 CDR-filtered jitter

### 1.4.1 Raw integrated jitter

Raw RMS jitter 通常由 phase-noise PSD 积分得到：

$$\sigma_{t,raw}^{2} = \frac{1}{\left( 2\pi f_{clk} \right)^{2}}\int_{f_{L}}^{f_{H}}S_{\phi}(f)\, df$$

其中：

- $S_{\phi}(f)$：phase-noise PSD，单位通常为 $rad^{2}/Hz$；
- $f_{L}$：积分下限；
- $f_{H}$：积分上限；
- $f_{clk}$：被测时钟频率。

不写积分频带，就不存在唯一的“RMS jitter”。例如，10 kHz 到 100 MHz 与 1 MHz 到 1 GHz 得到的结果不能直接比较。

### 1.4.2 Reference CDR/CRU filtered residual jitter

设输入 TX phase 为 $\phi_{TX}(s)$，CDR tracking transfer function 为 $H_{CDR}(s)$：

$$\phi_{rec}(s) = H_{CDR}(s)\phi_{TX}(s)$$

残余相位误差为：

$$\phi_{err}(s) = \left\lbrack 1 - H_{CDR}(s) \right\rbrack\phi_{TX}(s)$$

定义 residual transfer function：

$$H_{res}(s) = 1 - H_{CDR}(s)$$

对一阶 CDR：

$$H_{CDR}(s) = \frac{\omega_{c}}{s + \omega_{c}}$$

则：

$$\boxed{H_{res}(s) = \frac{s}{s + \omega_{c}}}$$

它是高通型残余传递函数，因此 filtered jitter 为：

$$\boxed{\sigma_{t,filtered}^{2} = \frac{1}{\left( 2\pi f_{clk} \right)^{2}}\int_{f_{L}}^{f_{H}}\left| H_{res}(j2\pi f) \right|^{2}S_{\phi}(f)\, df}$$

### 1.4.3 4 MHz corner 的实际含义

若：

$$f_{c} = 4\ MHz$$

一阶 residual filter 幅度为：

$$\left| H_{res}(f) \right| = \frac{f}{\sqrt{f^{2} + f_{c}^{2}}}$$

在 $100\ kHz$：

$$\left| H_{res} \right| \approx \frac{0.1}{\sqrt{{0.1}^{2} + 4^{2}}} \approx 0.025$$

低频 jitter 仅残留约 2.5%。

在 $40\ MHz$：

$$\left| H_{res} \right| \approx \frac{40}{\sqrt{40^{2} + 4^{2}}} \approx 0.995$$

高频 jitter 几乎全部保留。

因此 PLL 真正应该优化的不是一个脱离系统的 raw integral，而是：

$$\boxed{\int\left| H_{res}(f) \right|^{2}S_{\phi}(f)\, df}$$

低 offset phase noise 很差但被 reference CRU 跟踪的 PLL，filtered jitter 未必差；反过来，raw jitter 看起来不错，但在 10 MHz 到数百 MHz 有 VCO、divider、buffer、supply noise 或 spur 的设计，endpoint 仍可能失败。

## 1.5 为什么 55 fs 不能全部分配给 PLL core

Endpoint phase-noise PSD 可表示为：

$$\begin{matrix}
S_{\phi,EP}(f) = & \left| H_{CMU \rightarrow EP}(f) \right|^{2}S_{\phi,CMU}(f) \\
 & + \left| H_{dist \rightarrow EP}(f) \right|^{2}S_{\phi,dist}(f) \\
 & + \left| H_{CCU \rightarrow EP}(f) \right|^{2}S_{\phi,CCU}(f) \\
 & + \left| H_{ILO \rightarrow EP}(f) \right|^{2}S_{\phi,ILO}(f) \\
 & + S_{\phi,PS}(f) + S_{\phi,PR}(f) \\
 & + S_{\phi,servo}(f) + S_{\phi,supply}(f)
\end{matrix}$$

测量端再经过 reference CRU：

$$S_{\phi,meas}(f) = \left| H_{res}(f) \right|^{2}S_{\phi,EP}(f)$$

最终：

$$\boxed{\sigma_{t,meas}^{2} = \frac{1}{\left( 2\pi f_{clk} \right)^{2}}\int S_{\phi,meas}(f)\, df}$$

若把全部 55 fs 交给 PLL core：

1.  PLL 团队会过度优化 core noise，增加 VCO、CP、divider 和 buffer 功耗；
2.  distribution、CCU、ILO 和 phase-control path 没有预算，endpoint 仍可能失败；
3.  项目得到一个局部极优的 PLL 和一个整体不合格的 TX。芯片不会因为某个模块在内部评比里第一名就自动通过协议测试。

## 1.6 一个 55 fs endpoint budget 示例

以下为预算方法示例，不是公开论文的正式分配。

外部或系统目标：

$$\sigma_{endpoint,max} = 55\ fs$$

内部设计目标保守设为：

$$\sigma_{endpoint,target} = 45\ fs$$

| Contributor                       | RMS allocation |
|-----------------------------------|----------------|
| CMU 经 4 MHz CRU 后的残余         | 25 fs          |
| 1/8-rate clock distribution       | 14 fs          |
| TX CCU residual                   | 16 fs          |
| 8-stage ILO added jitter          | 20 fs          |
| Phase shifter 动态量化/噪声       | 4 fs           |
| Phase rotator residual            | 12 fs          |
| TDC/background servo update noise | 10 fs          |
| Supply/crosstalk induced jitter   | 12 fs          |

若这些项可视为不相关：

$$\sigma_{EP} = \sqrt{25^{2} + 14^{2} + 16^{2} + 20^{2} + 4^{2} + 12^{2} + 10^{2} + 12^{2}} = 43.37\ fs$$

因此：

$$43.37\ fs < 45\ fs < 55\ fs$$

Margin 不应伪装成另一个随机源加入 RSS。合理做法是把内部设计目标压低，为 PVT、PEX、模型误差、未建模相关性、测量重复性和 aging 保留空间。

## 1.7 如何从 CMU allocation 反推 PLL core

假设 shared CMU 的 filtered allocation 为：

$$\sigma_{t,CMU,res} \leq 25\ fs$$

对应约束为：

$$\boxed{\frac{1}{\left( 2\pi f_{clk} \right)^{2}}\int_{f_{L}}^{f_{H}}\left| H_{res}(f) \right|^{2}S_{\phi,CMU}(f)\, df \leq (25\ fs)^{2}}$$

CMU phase-noise PSD 由各来源组成：

$$\begin{matrix}
S_{\phi,CMU}(f) = & \left| H_{ref}(f) \right|^{2}S_{\phi,ref}(f) \\
 & + \left| H_{PFD/CP}(f) \right|^{2}S_{\phi,PFD/CP}(f) \\
 & + \left| H_{divider}(f) \right|^{2}S_{\phi,divider}(f) \\
 & + \left| H_{VCO}(f) \right|^{2}S_{\phi,VCO}(f) \\
 & + S_{\phi,supply}(f) + S_{\phi,spur}(f)
\end{matrix}$$

这时 Matrix 才真正开始决定 PLL 参数。

### 1.7.1 $f_{PFD}$ 和 divider ratio

$$N = \frac{f_{out}}{f_{PFD}}$$

提高 $f_{PFD}$ 通常可降低 $N$，有利于减少参考路径噪声放大，但同时增加：

- PFD/CP 速度要求；
- reference distribution 功耗；
- reference spur 压力；
- 高速数字活动和耦合。

Matrix 应写清楚 reference/PFD/divider 在相应频段允许贡献多少，而不是写“$f_{PFD}$ 越高越好”。

### 1.7.2 Loop bandwidth

PLL bandwidth 决定噪声分工：

- 环内更容易通过 reference、PFD、CP 和 divider noise；
- 环外主要由 VCO noise 主导。

系统应最小化：

$$\int\left| H_{res}(f) \right|^{2}\left\lbrack \left| H_{ref} \right|^{2}S_{ref} + \left| H_{VCO} \right|^{2}S_{VCO} + \cdots \right\rbrack df$$

而不是只追求 PLL raw integrated jitter 最小。

### 1.7.3 $I_{CP}$

Charge-pump current 影响：

$$K_{loop} \propto I_{CP}K_{VCO}$$

并进一步影响：

- loop bandwidth；
- damping；
- CP thermal/shot noise；
- UP/DN mismatch；
- reference spur；
- control-voltage ripple；
- dead-zone sensitivity。

因此 Matrix 不能只写“PLL BW = 3 MHz”，还应写该 BW 与 $I_{CP}$、loop-filter impedance、$K_{VCO}$ 和 PVT 范围的关系。

### 1.7.4 $K_{VCO}$ 或 $K_{DCO}$

控制节点噪声到输出相位的转换为：

$$S_{\phi,ctrl}(f) \propto \left| \frac{K_{VCO}}{j2\pi f} \right|^{2}S_{v,ctrl}(f)$$

较大的 $K_{VCO}$ 有利于 tuning range，但会增加：

- loop-filter noise sensitivity；
- CP ripple sensitivity；
- supply/control coupling；
- spur；
- calibration-code noise。

因此 tuning range、coarse-bank coverage、fine gain、control-node noise 和 endpoint jitter 必须在同一条 traceability chain 中。

## 1.8 1/8-rate clock 与 full-rate clock 为什么不能只比较 fs

假设：

$$f_{1/8} = 14\ GHz,\quad\quad f_{full} = 112\ GHz$$

14 GHz 时钟的 90 fs 对应相位 RMS：

$$\sigma_{\phi} = 2\pi(14\ GHz)(90\ fs) = 0.00792\ rad = {0.454}^{\circ}$$

112 GHz 时钟的 55 fs 对应：

$$\sigma_{\phi} = 2\pi(112\ GHz)(55\ fs) = 0.0387\ rad = {2.22}^{\circ}$$

因此：

- 从 time jitter 看，55 fs 小于 90 fs；
- 从 phase jitter 看，112 GHz 上的 55 fs 反而对应更大的相位误差；
- 不同频率、不同节点的两个 fs 数字不能直接判断哪个时钟“更干净”。

理想频率倍增 $M$ 倍时：

$$\sigma_{\phi,out} = M\sigma_{\phi,in}$$

且：

$$f_{out} = Mf_{in}$$

于是：

$$\sigma_{t,out} = \frac{M\sigma_{\phi,in}}{2\pi Mf_{in}} = \sigma_{t,in}$$

理想倍频不改变 time jitter，但实际 ILO、multiplier、mux 和 clock buffer 会加入额外 jitter。

## 1.9 Phase shifter LSB 不等于 RMS jitter

若 phase shifter step 为：

$$\Delta t_{PS} = 14\ fs$$

若 code 固定，量化误差是 bounded static phase offset：

$$- \frac{\Delta t}{2} \leq e_{t} \leq + \frac{\Delta t}{2}$$

因此：

$$\left| e_{t} \right|_{\max} = 7\ fs$$

它不一定属于 random jitter。

只有在量化误差被随机化、且近似均匀分布时，才可写：

$$\sigma_{t,quant} = \frac{\Delta t}{\sqrt{12}} = \frac{14}{\sqrt{12}} = 4.04\ fs$$

若 background servo 在两个 code 间周期性跳动，产生的可能是：

- discrete spur；
- limit cycle；
- periodic jitter；
- data-correlated modulation。

所以 Matrix 中应分别记录 LSB、static residual、dynamic quantization、update rate、dither policy 和 spur，而不能把“14 fs step”直接填进 RSS 表。

## 1.10 Phase rotator 1/128 UI 不等于随机 jitter

在 112 GBd 下：

$$UI = 8.929\ ps$$

1/128 UI 的 step 为：

$$\Delta t_{PR} = \frac{8.929\ ps}{128} = 69.76\ fs$$

它看起来比 55 fs 还大，但不一定矛盾，因为它可能是静态 phase-position LSB，而非 RMS jitter。

若粗略假设量化误差均匀随机化：

$$\sigma_{PR,quant} = \frac{69.76}{\sqrt{12}} = 20.14\ fs$$

若 code 静止，则应描述为 bounded static phase error；若 code 周期切换，则应分析 update noise、limit-cycle spur 和 INL/DNL，而不是偷懒地称为“20 fs jitter”。

## 1.11 TDC/background servo 为什么可能成为真正失败点

TDC 和 background servo 的误差包括：

$$\sigma_{TDC,quant},\quad\sigma_{TDC,offset},\quad\sigma_{servo,dither},\quad\sigma_{update}$$

若更新频率为 $f_{u}$，控制环在若干 code 间周期运动，endpoint spectrum 可能在：

$$f_{u},\quad 2f_{u},\quad 3f_{u}$$

附近产生离散 spur。

若 spur 位于 4 MHz 以上，reference CRU 基本不会滤除。因此可能出现：

- PLL core PNOISE 很好；
- endpoint phase spectrum 有明显 calibration spur；
- filtered RMS jitter 或 protocol mask 仍失败。

Matrix 必须把 calibration active、converged 和 frozen 分成不同 operating condition。

## 1.12 Measurement floor 必须写进 Matrix

若测得：

$$\sigma_{meas} = 55\ fs$$

仪器和 fixture 的独立噪声底为：

$$\sigma_{floor} = 15\ fs$$

则：

$$\sigma_{DUT} = \sqrt{\sigma_{meas}^{2} - \sigma_{floor}^{2}} = \sqrt{55^{2} - 15^{2}} = 52.9\ fs$$

若 55 fs 指标不包含 measurement floor，则允许仪器读数为：

$$\sqrt{55^{2} + 15^{2}} = 57.0\ fs$$

不定义 floor 是否 de-embed，实验室和设计团队很容易围绕几飞秒争论数周。人类尤其擅长为没有定义清楚的数字开非常正式的会议。

## 1.13 Spur 是否计入 RMS jitter

若存在正弦相位调制：

$$\phi(t) = A_{\phi}\sin\left( 2\pi f_{m}t \right)$$

对应时间抖动：

$$t_{j}(t) = \frac{A_{\phi}}{2\pi f_{clk}}\sin\left( 2\pi f_{m}t \right)$$

其峰值、RMS 和峰峰值分别为：

$$t_{pk} = \frac{A_{\phi}}{2\pi f_{clk}}$$

$$\boxed{t_{rms} = \frac{A_{\phi}}{\sqrt{2}\, 2\pi f_{clk}}}$$

$$t_{pp} = \frac{2A_{\phi}}{2\pi f_{clk}}$$

Matrix 必须明确：

- continuous phase-noise floor 是否包含；
- reference spur 是否包含；
- fractional spur 是否包含；
- calibration/servo spur 是否包含；
- supply spur 是否包含；
- 是否还有独立的 single-tone mask。

总 RMS 合格不代表最大 spur 合格，因此两种限制都需要。

## 1.14 一个合格的 Spec Matrix 行

### Requirement ID

`CLK-TX-224G-001`

### System requirement

在 224 Gb/s PAM4 mode 下，TX endpoint residual RMS jitter 不大于 55 fs。

### System purpose

限制 TX data crossing 的随机时间误差，保护 eye width、BER 和 transmit-jitter compliance margin。

### Measurement node

TX endpoint，即最终 serializer/driver 对应的数据 crossing。不是 VCO pin，不是 shared CMU pin，也不是 1/8-rate internal clock。

### Measurement filter

Reference CRU residual high-pass transfer function：corner 4 MHz，20 dB/dec。必须保存完整 transfer function、order、peaking 和实现容差。

### Integration range

明确 $f_{L}$、$f_{H}$、scope bandwidth 和数据处理算法。不得只写“integrated jitter”。

### Included components

- 连续随机 phase noise；
- reference/PFD/CP/VCO/divider noise；
- clock distribution；
- lane CCU；
- ILO；
- phase shifter；
- phase rotator；
- background servo；
- supply/crosstalk；
- 规定范围内的 spur。

### Excluded or separately limited components

- 静态 phase offset；
- lane-to-lane static skew；
- 已 de-embed 的 instrument floor；
- 低于 CRU tracking bandwidth 的 wander；
- 由 protocol mask 单独约束的 deterministic spur。

### Internal design target

$$\sigma_{EP,int} \leq 45\ fs$$

45 fs 是内部预算值，不是标准原文。

### Circuit parameters affecting the row

$$f_{PFD},\quad N,\quad BW,\quad I_{CP},\quad K_{VCO}/K_{DCO}$$

以及：

- VCO phase noise；
- divider topology；
- clock-buffer slew；
- CCU bandwidth；
- ILO locking range 和 bandwidth；
- phase-shifter LSB、INL、DNL；
- phase-rotator LSB；
- TDC resolution；
- servo update rate；
- supply PSRR；
- calibration policy。

### Verification

- behavioral phase-domain model；
- PLL phase-noise integration；
- PSS/PNOISE；
- transient jitter；
- AMS clock-chain simulation；
- post-layout extracted simulation；
- supply-injection simulation；
- all-lane switching simulation；
- 使用规定 4 MHz CRU 的 bench measurement；
- measurement-floor characterization。

### Corners

- 全部支持 mode；
- PVT；
- calibration extremes；
- supply droop；
- all-lane activity；
- local mismatch；
- PEX；
- aging；
- calibration on/off/frozen；
- startup 和 steady state。

## 1.15 Spec Matrix 如何指导每个模块

### Shared CMU

必须给出：

- 输出频率；
- raw phase-noise mask；
- 经过 CRU 后的 jitter allocation；
- reference spur；
- supply sensitivity；
- lane loading；
- output interface。

然后才能反推：

$$f_{PFD},\quad N,\quad BW,\quad I_{CP},\quad K_{VCO}$$

### Clock distribution

必须定义：

- path length；
- fanout；
- load capacitance；
- insertion delay；
- added jitter；
- static skew；
- DCD；
- supply-induced jitter；
- coupling environment。

再决定 CML/CMOS、buffer stage 数、taper、current、swing、shielding 和 local regulation。

### TX CCU

需要定义输入 jitter spectrum、输出 allocation、tracking bandwidth、ratio、acquisition range、steady-state residual 和 calibration behavior，而不是写一句“CCU cleans the clock”。

### ILO

需要定义：

- injection frequency 和 ratio；
- locking range；
- injection strength；
- residual phase noise；
- supply sensitivity；
- startup/acquisition；
- unlock detection；
- PVT margin。

ILO 既可能滤除输入 phase noise，也会加入自身 oscillator noise，必须用传递函数建模，不能把它当成固定 fs 黑盒。

### Phase shifter/rotator

需要定义 LSB、range、INL、DNL、monotonicity、code-dependent jitter、update glitch、settling、static residual、dynamic contribution 和 spur。

### TDC/background servo

需要定义 resolution、input-referred noise、dead zone、update frequency、loop gain、averaging length、dither、limit-cycle amplitude、convergence、freeze policy 和 pattern dependence。

## 1.16 Matrix 还是变更影响分析工具

若 reference CRU corner 从 4 MHz 改为 8 MHz，不能只改一个表格单元格。它会同时影响：

$$\text{CRU BW} \rightarrow \text{TX jitter filtering} \rightarrow \text{CMU budget} \rightarrow \text{PLL BW}$$

以及：

$$\text{CRU BW} \rightarrow \text{RX CDR latency} \rightarrow \text{DSP architecture} \rightarrow \text{power}$$

因此 Matrix 也是架构 trade-off 和 change-impact 工具。

## 1.17 常见错误

### 错误一：只有一个总 jitter 数字

没有 node、filter 和 integration range，无法转换成 phase-noise mask。

### 错误二：把所有 jitter 都交给 PLL

这会忽略 distribution、CCU、ILO、phase rotator、serializer 和 supply coupling。

### 错误三：把 LSB 直接当 RMS jitter

$$\Delta t = 14\ fs \Rightarrow \not{}\sigma_{t} = 14\ fs$$

必须区分 static quantization、randomized quantization、limit cycle 和 periodic spur。

### 错误四：把所有误差都 RSS

Static offset、bounded DNL、correlated supply noise、deterministic spur、worst-case skew 和 common-mode phase modulation不能随便 RSS。应根据物理性质使用 covariance、linear sum、spectral simulation、Monte Carlo 或 worst-case bound。

### 错误五：只给 loop bandwidth，不给 transfer function

同样是 4 MHz，loop order、damping、peaking、zero/pole、group delay 和 digital latency 都会改变结果。

### 错误六：混用 phase jitter 和 time jitter

$$\sigma_{t} = \frac{\sigma_{\phi}}{2\pi f_{clk}}$$

换了频率后，同样的 phase jitter 对应不同 fs；同样的 fs 也对应不同 radian。

### 错误七：不记录 calibration 状态

Background calibration 开启时可能增加 dither、update spur 和 switching noise；关闭时可能增加 drift、mismatch 和 static error。因此至少区分：

- Calibration active；
- Calibration converged；
- Calibration frozen。

## 1.18 推荐的 Matrix 字段

| 类别     | 字段                                       |
|----------|--------------------------------------------|
| 标识     | Requirement ID、版本、来源                 |
| 系统语义 | mode、用途、BER/eye 关联                   |
| 节点     | source node、observation node              |
| 指标定义 | RMS/pp、random/deterministic               |
| 滤波     | transfer function、corner、order           |
| 频带     | integration lower/upper limit              |
| 内容     | spur、floor、wander 是否包含               |
| 预算     | external limit、internal target、margin    |
| 分解     | 各 block allocation                        |
| 公式     | 从系统量到 block spec 的关系               |
| 电路旋钮 | $f_{PFD}$、$N$、BW、$I_{CP}$、$K_{VCO}$ 等 |
| 条件     | mode、PVT、activity、calibration           |
| 验证     | model、testbench、pass/fail script         |
| 证据     | simulation report、measurement report      |
| 管理     | owner、open issue、closure state           |

Owner、日期和状态有用，但它们只是管理字段，不能替代工程字段。

## 1.19 第一部分结论

每一条系统指标都必须回答五个问题：

1.  **为什么需要它**；
2.  **它究竟测量什么**；
3.  **哪些模块贡献它**；
4.  **哪些电路参数可以改善它**；
5.  **如何证明已经满足**。

完整翻译链为：

$$\boxed{\begin{matrix}
 & 55\ fs\ endpoint\ requirement \\
 & \Downarrow \\
 & \text{node/filter/bandwidth definition} \\
 & \Downarrow \\
 & \text{clock-chain contribution allocation} \\
 & \Downarrow \\
 & \text{CMU/CCU/ILO/phase-control specifications} \\
 & \Downarrow \\
 & \text{PLL noise mask and circuit parameters} \\
 & \Downarrow \\
 & \text{testbench and compliance evidence}
\end{matrix}}$$

没有这条链，Matrix 是汇报材料；有了这条链，它才是 PLL 架构、噪声预算、模块接口、验证计划和 tapeout signoff 的共同合同。

# 第二部分：224G SerDes PLL/CMU Spec 实例

## 2.1 设计定位与架构假设

本文给出一个可用于项目启动的 224G SerDes PLL/CMU 规格实例，采用：

- 224 Gb/s PAM4；
- 112 GBd symbol rate；
- 14 GHz 1/8-rate shared LC-PLL/CMU；
- 250 MHz reference；
- integer-N CPPLL；
- lane-local CCU/multi-phase generation；
- 4 MHz reference CRU 条件下的 endpoint jitter compliance。

OIF CEI-224G 面向不同 reach 和 channel class，不存在脱离产品架构的唯一“224G PLL spec”。因此，下面是工程设计实例，而不是标准原文。

### 2.1.1 数据率与频率关系

$$R_{b} = 224\ Gb/s$$

PAM4 每 symbol 携带 2 bit：

$$R_{s} = \frac{R_{b}}{2} = 112\ GBd$$

Symbol UI：

$$UI = \frac{1}{112\ GHz} = 8.929\ ps$$

1/8-rate CMU frequency：

$$f_{CMU} = \frac{112\ GHz}{8} = 14\ GHz$$

假设 reference：

$$f_{REF} = 250\ MHz$$

则 divider ratio：

$$N = \frac{14\ GHz}{250\ MHz} = 56$$

### 2.1.2 Clock chain

$$\boxed{250\ MHz\ Ref \rightarrow 14\ GHz\ LC\ PLL/CMU \rightarrow \text{global clock distribution} \rightarrow \text{lane CCU} \rightarrow \text{multi-phase/phase alignment} \rightarrow \text{1/8-rate TX serializer}}$$

PLL 只负责 shared CMU 的贡献，不直接承担全部 endpoint jitter。

## 2.2 顶层系统 Spec Matrix

| ID      | 项目                          | 设计目标                  | 类型    | 说明                         |
|---------|-------------------------------|---------------------------|---------|------------------------------|
| SYS-001 | 数据率                        | 224 Gb/s PAM4             | `[A]`   | 112 GBd                      |
| SYS-002 | Symbol UI                     | 8.929 ps                  | `[D]`   | $1/112\ GHz$                 |
| SYS-003 | TX 架构                       | 1/8-rate                  | `[A]`   | 14 GHz internal clock        |
| SYS-004 | Endpoint sRJ compliance limit | $\leq 10\ mUI = 89.3\ fs$ | `[P]`   | 4 MHz reference CRU          |
| SYS-005 | Endpoint internal target      | $\leq 55\ fs_{rms}$       | `[D]`   | 为 PVT、PEX 和建模留 margin  |
| SYS-006 | Reference CRU                 | 4 MHz，20 dB/dec          | `[P]`   | residual high-pass filter    |
| SYS-007 | Endpoint deterministic jitter | $\leq 170\ fs_{pp}$       | `[A/P]` | 需独立 mask                  |
| SYS-008 | Pre-FEC BER validation        | $\leq 10^{- 6}$           | `[A/P]` | link-level validation target |

其中：

$$10\ mUI = 0.01 \times 8.929\ ps = 89.29\ fs$$

55 fs 是内部设计目标，不应冒充协议唯一限制。

## 2.3 Endpoint jitter budget

内部目标：

$$\sigma_{EP,target} = 55\ fs$$

建议模块 RSS 目标压到约 46 fs：

| Contributor                             | RMS allocation |
|-----------------------------------------|----------------|
| Shared CMU/PLL，4 MHz filtered          | 25 fs          |
| Global 14 GHz distribution              | 15 fs          |
| Lane CCU                                | 15 fs          |
| Multi-phase generator / phase alignment | 18 fs          |
| Serializer clock path                   | 12 fs          |
| Supply/crosstalk residual               | 10 fs          |
| Calibration/servo update noise          | 8 fs           |

$$\sigma_{EP} = \sqrt{25^{2} + 15^{2} + 15^{2} + 18^{2} + 12^{2} + 10^{2} + 8^{2}} = 45.99\ fs$$

因此：

$$45.99\ fs < 55\ fs < 89.29\ fs$$

剩余空间用于 PEX、模型误差、correlation uncertainty、bench repeatability、aging 和 all-lane switching。

## 2.4 PLL/CMU 顶层频率规格

| Spec                            | Target                                         |
|---------------------------------|------------------------------------------------|
| PLL type                        | Type-II、3rd-order integer-N CPPLL             |
| Nominal reference frequency     | 250 MHz                                        |
| Reference input range           | 200–400 MHz                                    |
| Nominal output frequency        | 14.000 GHz                                     |
| Guaranteed functional range     | 13.5–14.5 GHz                                  |
| Total calibration capture range | 12.5–15.5 GHz                                  |
| Nominal divider ratio           | 56                                             |
| Output format                   | Differential CML                               |
| Output phases                   | PLL 提供 differential clock；lane CCU 生成多相 |
| Frequency accuracy in lock      | 跟随 reference，静态误差 <1 ppm equivalent    |
| Reference tolerance             | 至少 $\pm 100$ ppm                             |

Total tuning range 必须大于 guaranteed operating range，以覆盖 process、temperature、supply、aging 和模型误差。把产品频率范围与 VCO tuning range 写成完全相同，是没有余量，不是精确。

## 2.5 Jitter 规格

| Spec                                       | Target               | 条件                        |
|--------------------------------------------|----------------------|-----------------------------|
| CMU 4 MHz-filtered RMS jitter              | $\leq 25\ fs$        | continuous PN，10 kHz–1 GHz |
| CMU raw RMS jitter                         | $\leq 55\ fs$        | continuous PN，10 kHz–1 GHz |
| Raw total jitter including specified spurs | $\leq 65\ fs$        | 统一 spur-to-jitter 方法    |
| Cycle-to-cycle jitter                      | $\leq 150\ fs_{rms}$ | PVT，clean nominal supply   |
| Period jitter                              | $\leq 200\ fs_{rms}$ | 同上                        |
| Added jitter from output buffer            | $\leq 8\ fs_{rms}$   | VCO tap 到 CMU output       |
| PEX jitter degradation                     | $\leq 10\%$          | 相对 schematic              |

Phase-noise integrated jitter、period jitter、cycle-to-cycle jitter 和 CDR-filtered residual jitter 是不同统计量，不能统称为一个“PLL jitter”。

## 2.6 Phase-noise mask 实例

以下 mask 是满足 55 fs raw 和 25 fs filtered 预算的初始设计目标，不是标准值。

| Offset frequency | Maximum SSB phase noise |
|------------------|-------------------------|
| 10 kHz           | $- 90\ dBc/Hz$          |
| 100 kHz          | $- 110\ dBc/Hz$         |
| 1 MHz            | $- 125\ dBc/Hz$         |
| 10 MHz           | $- 140\ dBc/Hz$         |
| 100 MHz          | $- 150\ dBc/Hz$         |
| 1 GHz            | $- 155\ dBc/Hz$         |

SSB phase noise 转为 phase PSD：

$$S_{\phi}(f) \approx 2 \times 10^{L(f)/10}$$

Raw RMS jitter：

$$\boxed{\sigma_{t,raw} = \frac{1}{2\pi f_{CMU}}\sqrt{\int_{f_{L}}^{f_{H}}S_{\phi}(f)\, df}}$$

设计目标：

$$\sigma_{t,raw} \leq 55\ fs$$

### 2.6.1 4 MHz CRU-filtered jitter

$$H_{CRU}(s) = \frac{\omega_{c}}{s + \omega_{c}}$$

$$H_{res}(s) = 1 - H_{CRU}(s) = \frac{s}{s + \omega_{c}}$$

其中：

$$f_{c} = 4\ MHz$$

Filtered jitter：

$$\boxed{\sigma_{t,filtered} = \frac{1}{2\pi f_{CMU}}\sqrt{\int_{f_{L}}^{f_{H}}\left| H_{res}(j2\pi f) \right|^{2}S_{\phi}(f)\, df}}$$

目标：

$$\sigma_{t,filtered} \leq 25\ fs$$

PLL 优化必须同时观察 raw jitter、filtered jitter、离散 spur 和 endpoint total jitter。

## 2.7 PLL noise-contribution budget

| PLL noise source               | 4 MHz-filtered allocation |
|--------------------------------|---------------------------|
| Reference input                | 6 fs                      |
| Reference buffer               | 4 fs                      |
| PFD/charge pump                | 8 fs                      |
| Divider                        | 5 fs                      |
| VCO intrinsic noise            | 18 fs                     |
| Loop-filter/control-node noise | 5 fs                      |
| Supply/substrate noise         | 7 fs                      |
| Output clock buffer            | 8 fs                      |

$$\sigma_{CMU} = \sqrt{6^{2} + 4^{2} + 8^{2} + 5^{2} + 18^{2} + 5^{2} + 7^{2} + 8^{2}} = 24.56\ fs$$

满足：

$$24.56\ fs < 25\ fs$$

各项最终应保存完整 PSD，而不仅是一个 fs 数值，因为相同 RMS 若位于不同 offset，其 CRU residual 和 protocol 影响不同。

## 2.8 Loop dynamics 规格

| Spec                                | Target                    |
|-------------------------------------|---------------------------|
| Nominal closed-loop bandwidth       | 3.0 MHz                   |
| PVT bandwidth range                 | 2.5–3.5 MHz               |
| Phase margin                        | $55^{\circ}$–$75^{\circ}$ |
| Preferred nominal phase margin      | $65^{\circ}$              |
| Closed-loop peaking                 | <1 dB                    |
| Damping factor                      | 0.7–1.1                   |
| Reference/PFD noise crossover       | 与 VCO noise 最优点附近   |
| Settling to $\pm 100$ ppm           | <3 $\mu$s                |
| Settling to $\pm 10$ ppm            | <5 $\mu$s                |
| Total cold-start lock               | <10 $\mu$s               |
| Cycle slip after coarse calibration | 不允许                    |
| Loss-of-lock detection              | <2 $\mu$s                |
| Automatic relock                    | <10 $\mu$s               |

Bandwidth 不应由“同类项目通常几 MHz”决定，而应通过 sweep 最小化：

$$\boxed{J(BW) = \int\left| H_{res}(f) \right|^{2}S_{\phi,out}(f,BW)\, df}$$

其中：

$$\begin{matrix}
S_{\phi,out}(f) = & \left| H_{ref}(f) \right|^{2}S_{\phi,ref}(f) \\
 & + \left| H_{PFD/CP}(f) \right|^{2}S_{\phi,PFD/CP}(f) \\
 & + \left| H_{div}(f) \right|^{2}S_{\phi,div}(f) \\
 & + \left| H_{VCO}(f) \right|^{2}S_{\phi,VCO}(f)
\end{matrix}$$

## 2.9 PFD 规格

| Spec                        | Target                                        |
|-----------------------------|-----------------------------------------------|
| PFD frequency               | 250 MHz                                       |
| Dead zone                   | <1 ps equivalent phase difference            |
| Reset-path mismatch         | <2 ps                                        |
| UP/DN pulse symmetry        | error <2%                                    |
| Maximum operating frequency | >500 MHz                                     |
| Input duty-cycle tolerance  | 40%–60%                                       |
| PFD input-referred jitter   | <3 fs referred to CMU output after filtering |

PFD signoff 必须覆盖 reset race、minimum pulse width、dead zone、input slew、PVT、mismatch、PEX 和 supply coupling。

## 2.10 Charge-pump 规格

| Spec                                | Target                             |
|-------------------------------------|------------------------------------|
| Nominal $I_{CP}$                    | 0.8 mA                             |
| Programmable range                  | 0.4–1.6 mA                         |
| Programming steps                   | 至少 16                            |
| UP/DN mismatch                      | <1% nominal                       |
| UP/DN mismatch across control range | <3%                               |
| Output compliance                   | 0.15–0.65 V，假设 0.8 V supply     |
| Output resistance                   | >200 k$\Omega$ equivalent         |
| CP current noise                    | 满足 filtered contribution <8 fs  |
| Charge injection                    | 必须进入 reference-spur simulation |
| Leakage at lock                     | <1 nA equivalent target           |

$I_{CP}$ 必须与 $K_{VCO}$、divider ratio、loop-filter impedance、BW 和 spur 联合综合，不能先拍一个“常见值”，再让 loop filter 替早期随意决定擦屁股。

## 2.11 Loop-filter 规格

采用 type-II、3rd-order passive filter，候选元件为：

$$C_{1},\quad R_{z},\quad C_{2},\quad R_{p},\quad C_{3}$$

| Parameter                            | Initial target           |
|--------------------------------------|--------------------------|
| Main integrating capacitance $C_{1}$ | 5–15 pF                  |
| Zero placement                       | 0.5–1.5 MHz              |
| High-frequency pole                  | 10–30 MHz                |
| Control-node RMS noise               | 满足 <5 fs contribution |
| Leakage-induced frequency error      | <1 ppm equivalent       |
| Capacitor PVT variation              | 纳入 BW/PM corners       |
| Extracted routing resistance         | 纳入 loop stability      |
| Reference ripple                     | 满足 spur target         |

最终值必须由：

$$I_{CP},\quad K_{VCO},\quad N,\quad BW,\quad\zeta$$

联合求解。

## 2.12 VCO 规格

假设采用 differential LC VCO 加 coarse capacitor bank。

| Spec                          | Target                         |
|-------------------------------|--------------------------------|
| Nominal frequency             | 14.0 GHz                       |
| Total tuning range            | 12.5–15.5 GHz                  |
| Guaranteed operating range    | 13.5–14.5 GHz                  |
| Fine tuning gain $K_{VCO}$    | 100–250 MHz/V                  |
| Preferred nominal $K_{VCO}$   | 150 MHz/V                      |
| Coarse-bank overlap           | 相邻 bank >15%                |
| Frequency monotonicity        | 全 code 保证                   |
| Coarse calibration resolution | <50 MHz/LSB                   |
| Calibration residual          | fine range 中心附近 $\pm 20\%$ |
| VCO startup                   | <100 ns                       |
| Startup margin                | $g_{m}R_{p} > 2$ across PVT    |
| VCO phase-noise contribution  | <18 fs filtered               |
| Amplitude variation           | <$\pm 10\%$ across PVT        |
| Frequency pushing             | <30 MHz/V                     |
| Temperature drift after lock  | PLL 可跟踪且不失锁             |
| Supply isolation              | 见 supply-injection spec       |

控制节点到 phase 的关系：

$$\Phi_{out}(s) = \frac{K_{VCO}}{s}V_{ctrl}(s)$$

因此：

$$S_{\phi,ctrl}(f) = \left| \frac{K_{VCO}}{j2\pi f} \right|^{2}S_{v,ctrl}(f)$$

$K_{VCO}$ 越大，fine tuning 越容易，但 CP ripple、control-node noise、substrate coupling 和 calibration-code noise 更容易转成 jitter。

## 2.13 Divider 规格

| Spec                            | Target                                            |
|---------------------------------|---------------------------------------------------|
| Total divide ratio              | 56                                                |
| Prescaler topology              | CML / injection-assisted / static divider，待权衡 |
| Input frequency                 | 12.5–15.5 GHz                                     |
| Input sensitivity               | VCO 最小摆幅下仍有 >6 dB margin                  |
| Added filtered jitter           | <5 fs                                            |
| Maximum divider PN contribution | 按 PSD mask 管理                                  |
| Duty-cycle sensitivity          | 不得 false count                                  |
| Supply-noise tolerance          | 规定注入条件下不丢计数                            |
| Startup                         | 无 stuck state                                    |
| Power                           | <8 mW，项目预算                                  |
| PVT operation margin            | 全 corner + PEX                                   |

Divider 的首要 signoff 不是“TT schematic 能除频”，而是 slow device、低 supply、高温、最高频率、最低 VCO swing、extracted interconnect 和 supply noise 同时存在时仍能可靠除频。

## 2.14 Spur 规格

| Spur type                        | Target                        |
|----------------------------------|-------------------------------|
| Reference spur at 250 MHz offset | <$- 60$ dBc                  |
| Harmonics related to PFD         | <$- 60$ dBc                  |
| Supply-induced discrete spur     | <$- 55$ dBc                  |
| Calibration update spur          | <$- 65$ dBc 或独立 mask      |
| Digital clock coupling spur      | <$- 60$ dBc                  |
| Fractional spur                  | nominal integer-N mode 不适用 |
| Largest unspecified spur         | <$- 65$ dBc                  |

Spur 必须同时以 dBc mask 和 equivalent time jitter 验证。

若：

$$\phi(t) = A_{\phi}\sin\left( 2\pi f_{m}t \right)$$

则：

$$\boxed{\sigma_{t,spur} = \frac{A_{\phi}}{\sqrt{2}\, 2\pi f_{clk}}}$$

只积分 continuous PNOISE，然后把频谱尖刺当背景装饰，不算 signoff。

## 2.15 Supply 和 substrate 规格

### 2.15.1 Supply domains

本例假设：

- VCO/PLL analog：0.8 V；
- digital calibration：0.75–0.8 V；
- VCO 使用独立 local LDO 或强 RC/LC isolation；
- VCO/loop-filter 与高活动 DSP 分 supply island。

### 2.15.2 Supply sensitivity

| Test                                   | Target                                 |
|----------------------------------------|----------------------------------------|
| Static frequency pushing               | <30 MHz/V                             |
| 10 mVpp sine at 1 MHz                  | sideband <$- 50$ dBc                  |
| 10 mVpp sine at 10 MHz                 | sideband <$- 55$ dBc                  |
| 10 mVpp sine at 100 MHz                | sideband <$- 55$ dBc                  |
| Defined broadband supply-noise profile | added jitter <7 fs                    |
| All-lane simultaneous switching        | CMU filtered jitter degradation <5 fs |
| Ground bounce                          | 无 false lock、cycle slip              |
| LDO PSRR                               | 由 VCO pushing 和 jitter budget 反推   |

建立 supply-to-phase model：

$$S_{\phi,supply}(f) = \left| K_{\phi,VDD}(f) \right|^{2}S_{VDD}(f)$$

然后：

$$\sigma_{t,VDD}^{2} = \frac{1}{\left( 2\pi f_{CMU} \right)^{2}}\int\left| H_{res}(f) \right|^{2}S_{\phi,supply}(f)\, df$$

“PSRR 要高”不叫 spec，和“芯片要好用”属于同一个技术层级。

## 2.16 Clock-output 规格

| Spec                                      | Target                                |
|-------------------------------------------|---------------------------------------|
| Output frequency                          | 14 GHz                                |
| Output topology                           | Differential CML                      |
| Differential swing                        | 250–400 mVppd                         |
| Common mode                               | 由 lane CCU input range 定义          |
| Load                                      | 20 fF nominal，30 fF max              |
| Rise/fall time                            | <10 ps，20%–80%                      |
| Duty cycle                                | 50% $\pm 2\%$                         |
| Output-buffer added jitter                | <8 fs                                |
| Clock amplitude variation                 | <$\pm 10\%$ PVT                      |
| Lane distribution skew before calibration | <5 ps                                |
| Lane distribution skew after calibration  | <200 fs                              |
| Crosstalk sensitivity                     | 指定 aggressor 下 added jitter <5 fs |

Static lane skew 与 random RMS jitter 必须分开管理。

## 2.17 Calibration 规格

| Function                         | Target                                               |
|----------------------------------|------------------------------------------------------|
| VCO coarse frequency calibration | <3 $\mu$s                                           |
| Calibration success rate         | 定义 signoff MC 集合内 100%                          |
| Final VCO band                   | control voltage 位于 usable range 的 30%–70%         |
| Calibration resolution           | <50 MHz/step                                        |
| Wrong-band detection             | 必须具备                                             |
| Background calibration           | 可配置 enable/freeze                                 |
| Calibration update spur          | <$- 65$ dBc                                         |
| Temperature recalibration        | 无数据中断，或由 protocol state 管理                 |
| Loss-of-lock recovery            | 自动 coarse tune + relock                            |
| Register observability           | band code、control voltage、lock status、error flags |

应记录 calibration active、converged 和 frozen 三种状态下的 jitter、spur、power 和 drift。

## 2.18 Power、area 与可靠性预算

这些值高度依赖工艺，以下只是项目预算。

| Spec                        | Target                          |
|-----------------------------|---------------------------------|
| VCO core power              | $\leq 18\ mW$                   |
| PFD/CP/filter/bias          | $\leq 5\ mW$                    |
| Divider                     | $\leq 8\ mW$                    |
| CMU output buffer           | $\leq 10\ mW$                   |
| Calibration digital average | $\leq 2\ mW$                    |
| Total PLL/CMU               | $\leq 43\ mW$                   |
| Active area excluding decap | $\leq 0.12\ mm^{2}$             |
| EM current density          | 满足 foundry 10-year life limit |
| Aging frequency-margin loss | <5% tuning margin              |
| Hot-carrier/BTI             | 纳入 end-of-life corner         |
| Startup under supply ramp   | 全规定 ramp rate 成功           |

功耗必须分块管理。只给 total power，项目后期才发现 divider 或 output buffer 独自超支，是一种十分传统的惊喜。

## 2.19 PVT 与 Monte Carlo signoff

### 2.19.1 Global corners

至少覆盖：

$$FF,\ FS,\ SF,\ SS,\ TT$$

并叠加：

- $VDD_{\min}$、$VDD_{\max}$；
- $T = - 40^{\circ}C$ 到 $125^{\circ}C$；
- VCO inductor/metal model corners；
- resistor/capacitor corners；
- reference amplitude 和 slew corners；
- aging/EOL corners。

### 2.19.2 Monte Carlo

| Verification item          | Minimum requirement          |
|----------------------------|------------------------------|
| VCO frequency distribution | 500 runs                     |
| VCO startup                | 500 runs                     |
| CP mismatch                | 500 runs                     |
| Lock acquisition           | 200 runs/major PVT           |
| Reference spur             | mismatch-aware               |
| Divider functional margin  | mismatch + PVT               |
| Complete PLL jitter        | selected statistical corners |
| Calibration success        | defined run set 中零失败     |

“500 次没失败”不等于真正 failure probability 为零。应结合 sigma model、yield target、importance sampling 或 tail analysis。

## 2.20 完整验证矩阵

| Level        | Required verification                                            |
|--------------|------------------------------------------------------------------|
| Behavioral   | Matlab/Python phase-domain model、noise budget、BW sweep         |
| Verilog-A    | acquisition、cycle slip、calibration、loss-of-lock               |
| Schematic    | PSS/PNOISE、transient noise、spur、supply injection              |
| Block PEX    | VCO、divider、CP、output buffer                                  |
| Full PLL PEX | lock、jitter、spur、stability                                    |
| EM           | VCO inductor、clock routes、supply grid                          |
| AMS          | calibration FSM、register、mode switching                        |
| Clock-chain  | CMU + distribution + CCU + multiphase + serializer               |
| Link-level   | TX waveform、4 MHz CRU、BER/eye                                  |
| Bench        | phase noise、raw jitter、filtered jitter、spur、supply injection |

## 2.21 可直接写入 Spec Matrix 的核心行

| Field                      | 内容                                                |
|----------------------------|-----------------------------------------------------|
| Requirement ID             | PLL-CMU-224G-001                                    |
| System mode                | 224 Gb/s PAM4，112 GBd                              |
| System purpose             | 保证 TX endpoint sRJ 和 eye-width margin            |
| PLL node                   | Shared 14 GHz CMU output                            |
| Endpoint requirement       | sRJ $\leq 10$ mUI with 4 MHz reference CRU          |
| Internal endpoint target   | $\leq 55\ fs_{rms}$                                 |
| PLL allocation             | $\leq 25\ fs_{rms}$，4 MHz filtered                 |
| Raw PLL jitter             | $\leq 55\ fs_{rms}$，10 kHz–1 GHz                   |
| Reference                  | 250 MHz differential                                |
| Divider ratio              | 56                                                  |
| Loop bandwidth             | 3 MHz nominal                                       |
| Phase margin               | $65^{\circ}$ nominal                                |
| VCO frequency              | 14 GHz nominal                                      |
| VCO total range            | 12.5–15.5 GHz                                       |
| $K_{VCO}$                  | 100–250 MHz/V                                       |
| Reference spur             | <$- 60$ dBc                                        |
| Added output-buffer jitter | <8 fs                                              |
| Supply-added jitter        | <7 fs                                              |
| Lock time                  | <10 $\mu$s cold start                              |
| Power                      | <43 mW                                             |
| Signoff                    | PVT + MC + PEX + supply injection + clock-chain BER |

## 2.22 从系统到晶体管的最终链条

$$\boxed{\begin{matrix}
 & 224\ Gb/s\ PAM4 \\
 & \Downarrow \\
 & 112\ GBd,\ UI = 8.929\ ps \\
 & \Downarrow \\
 & 10\ mUI = 89.3\ fs \\
 & \Downarrow \\
 & 55\ fs\ endpoint\ internal\ target \\
 & \Downarrow \\
 & 25\ fs\ CMU\ allocation \\
 & \Downarrow \\
 & \text{phase-noise mask + spur mask} \\
 & \Downarrow \\
 & f_{PFD} = 250\ MHz,\ N = 56,\ BW = 3\ MHz \\
 & \Downarrow \\
 & I_{CP},\ K_{VCO},\ C_{LF},\ R_{LF} \\
 & \Downarrow \\
 & g_{m},\ I_{D},\ C_{tank},\ R_{p},\ \text{divider speed} \\
 & \Downarrow \\
 & \text{schematic / PEX / clock-chain / link signoff}
\end{matrix}}$$

这才是一份可执行的 224G SerDes PLL spec。只写“14 GHz、jitter <55 fs、power 越低越好”，不是 spec，而是三个愿望加一个频率。

# 第三部分：根据 Spec 制定 PLL 架构并计算电路具体参数

根据前述 Spec，不能立刻打开 Virtuoso 开始画 VCO。正确流程是先完成三次“降维翻译”：

$$\boxed{\text{System Spec} \rightarrow \text{PLL Architecture} \rightarrow \text{Block Electrical Spec} \rightarrow \text{Transistor Targets} \rightarrow \text{PDK Sizing}}$$

也就是先计算频率规划、环路、噪声和调谐范围，再得到 $g_{m}$、电流、电容、输出电阻等电气目标，最后才用 PDK LUT 得到 Fin 数或 $W/L$。直接从 25 fs 跳到晶体管宽度，和从“我要去温哥华”直接推导发动机活塞尺寸差不多。

下面使用前述设计实例：

| 参数                  | 数值              |
|-----------------------|-------------------|
| Data rate             | 224 Gb/s PAM4     |
| Baud rate             | 112 GBd           |
| Internal architecture | 1/8-rate          |
| PLL output            | 14 GHz            |
| Reference             | 250 MHz           |
| Divider ratio         | 56                |
| PLL type              | Integer-N CPPLL   |
| Loop bandwidth        | 3 MHz             |
| Phase margin          | $65^{\circ}$      |
| Charge-pump current   | 0.8 mA nominal    |
| $K_{VCO}$             | 150 MHz/V nominal |
| VCO total range       | 12.5–15.5 GHz     |
| PLL filtered jitter   | $\leq 25$ fs RMS  |
| PLL raw jitter        | $\leq 55$ fs RMS  |
| Supply                | 0.8 V             |

## 3.1 先决定 PLL 架构

### 3.1.1 推荐架构

对于这个固定频率、低 jitter 的 224G SerDes CMU，第一版建议采用：

$$\boxed{\begin{matrix}
 & 250\ MHz\ differential\ reference \\
 & \rightarrow \text{PFD} \\
 & \rightarrow \text{低噪声差分 Charge Pump} \\
 & \rightarrow \text{Type-II 3rd-order passive loop filter} \\
 & \rightarrow \text{14 GHz differential LC VCO} \\
 & \rightarrow \div 8\ \text{CML divider} \\
 & \rightarrow \div 7\ \text{CMOS divider} \\
 & \rightarrow \text{PFD feedback}
\end{matrix}}$$

VCO 另外通过隔离 buffer 驱动：

$$14\ GHz\ CMU \rightarrow \text{global distribution} \rightarrow \text{lane CCU / multiphase generator}$$

具体组成：

- Integer-N CPPLL；
- 差分 LC VCO；
- switched-MIM coarse capacitor bank；
- 小范围模拟 varactor；
- Type-II、三阶无源 loop filter；
- 三级高速 CML $\div 2$；
- 低速 CMOS $\div 7$；
- 独立 quiet supply 或 local LDO；
- 差分 CML CMU output buffer；
- 数字 coarse-frequency calibration。

### 3.1.2 为什么不用 Ring PLL

Ring VCO 的优点是 tuning range 大、面积小、多相输出自然、校准容易。但这里 PLL filtered jitter 只有：

$$25\ fs_{rms}$$

对应 14 GHz 的积分相位 RMS：

$$\sigma_{\phi} = 2\pi f_{0}\sigma_{t} = 2\pi(14\ GHz)(25\ fs)$$

$$\boxed{\sigma_{\phi} = 2.20 \times 10^{- 3}\ rad = {0.126}^{\circ}}$$

这对 ring VCO 极其苛刻，尤其是 4 MHz 以上的 VCO 噪声。因此优先选择 LC VCO。

### 3.1.3 为什么采用 Integer-N

频率规划为：

$$N = \frac{14\ GHz}{250\ MHz} = 56$$

而且：

$$56 = 8 \times 7$$

因此没有必要为了显示架构“先进”而引入 fractional-N、DSM 和 DTC。那些模块会额外带来 quantization noise、fractional spur、DTC INL、background calibration、供电噪声和验证负担。功能不需要时增加复杂度，在 PPT 上叫创新，在 silicon 上通常叫 bug source。

## 3.2 将 jitter Spec 变成 PLL 噪声目标

### 3.2.1 PLL filtered jitter

PLL allocation 是：

$$\sigma_{t,PLL} = 25\ fs$$

在 14 GHz 下：

$$\sigma_{\phi,PLL} = 2\pi f_{PLL}\sigma_{t} = 2.199 \times 10^{- 3}\ rad$$

相位方差：

$$\boxed{\sigma_{\phi,PLL}^{2} = 4.84 \times 10^{- 6}\ rad^{2}}$$

这意味着经过 4 MHz CRU residual filter 后，所有 PLL 输出相位噪声积分必须满足：

$$\boxed{\int_{f_{L}}^{f_{H}}\left| H_{res}(f) \right|^{2}S_{\phi,PLL}(f)\, df \leq 4.84 \times 10^{- 6}}$$

其中：

$$H_{res}(s) = \frac{s}{s + 2\pi \cdot 4\ MHz}$$

不能只给 VCO 一个“18 fs”数字。必须给 VCO、CP、divider、reference buffer 各自的 PSD mask，再通过 NTF 积分。

### 3.2.2 PLL 内部噪声分配

| 来源                     | Filtered jitter |
|--------------------------|-----------------|
| Reference input          | 6 fs            |
| Reference buffer         | 4 fs            |
| PFD/CP                   | 8 fs            |
| Divider                  | 5 fs            |
| VCO                      | 18 fs           |
| Loop filter/control node | 5 fs            |
| Supply/substrate         | 7 fs            |
| Output buffer            | 8 fs            |

RSS 为：

$$\sqrt{6^{2} + 4^{2} + 8^{2} + 5^{2} + 18^{2} + 5^{2} + 7^{2} + 8^{2}} = 24.56\ fs$$

因此架构重点依次是 VCO 与输出 buffer、PFD/CP、供电隔离以及高速 divider。不能只拼命优化 VCO，然后让 clock buffer 用数字标准单元随缘驱动。那种做法很适合在项目最后一个月制造团队凝聚力。

## 3.3 计算环路滤波器参数

### 3.3.1 采用的三阶无源滤波器

在 charge-pump 输出节点使用：

- $C_{p}$：直接从控制节点接地；
- $R_{z} - C_{z}$：串联后从控制节点接地。

其阻抗为：

$$Z(s) = \frac{1 + sR_{z}C_{z}}{s\left( C_{p} + C_{z} \right) + s^{2}R_{z}C_{p}C_{z}}$$

可写为：

$$Z(s) = \frac{1 + s/\omega_{z}}{s\left( C_{p} + C_{z} \right)\left( 1 + s/\omega_{p} \right)}$$

其中：

$$\omega_{z} = \frac{1}{R_{z}C_{z}}$$

$$\omega_{p} = \frac{C_{p} + C_{z}}{R_{z}C_{p}C_{z}}$$

### 3.3.2 环路开环增益

PFD/CP 增益：

$$K_{\phi} = \frac{I_{CP}}{2\pi}$$

VCO 增益：

$$K_{V} = 2\pi K_{VCO,Hz}$$

开环增益：

$$L(s) = \frac{K_{\phi}K_{V}}{N}\frac{Z(s)}{s}$$

代入：

$$I_{CP} = 0.8\ mA$$

$$K_{VCO} = 150\ MHz/V$$

$$N = 56$$

得到环路增益常数：

$$K_{0} = \frac{K_{\phi}K_{V}}{N} = \frac{I_{CP}K_{VCO,Hz}}{N}$$

$$K_{0} = \frac{0.8 \times 10^{- 3} \times 150 \times 10^{6}}{56}$$

$$\boxed{K_{0} = 2142.9}$$

### 3.3.3 设置环路极点和零点

目标：

$$f_{c} = 3\ MHz$$

$$PM = 65^{\circ}$$

选择高频极点：

$$f_{p} = 20\ MHz$$

三阶环路的相位裕量近似为：

$$PM = \tan^{- 1}\left( \frac{f_{c}}{f_{z}} \right) - \tan^{- 1}\left( \frac{f_{c}}{f_{p}} \right)$$

因此：

$$f_{z} = \frac{f_{c}}{\tan\left\lbrack PM + \tan^{- 1}\left( f_{c}/f_{p} \right) \right\rbrack}$$

代入得到：

$$\boxed{f_{z} = 0.887\ MHz}$$

验证：

$$\tan^{- 1}(3/0.887) - \tan^{- 1}(3/20) = {73.53}^{\circ} - {8.53}^{\circ} = 65^{\circ}$$

### 3.3.4 计算总电容

在 crossover 处令：

$$\left| L\left( j\omega_{c} \right) \right| = 1$$

得到：

$$C_{tot} = C_{p} + C_{z}$$

$$C_{tot} = \frac{K_{0}\sqrt{1 + \left( f_{c}/f_{z} \right)^{2}}}{\omega_{c}^{2}\sqrt{1 + \left( f_{c}/f_{p} \right)^{2}}}$$

其中：

$$\omega_{c} = 2\pi(3\ MHz)$$

代入得到：

$$\boxed{C_{tot} \approx 21.04\ pF}$$

又因为：

$$\frac{f_{p}}{f_{z}} = \frac{C_{p} + C_{z}}{C_{p}}$$

定义：

$$\alpha = \frac{f_{p}}{f_{z}} = 22.55$$

因此：

$$C_{p} = \frac{C_{tot}}{\alpha}$$

$$\boxed{C_{p} \approx 0.93\ pF}$$

$$C_{z} = C_{tot} - C_{p}$$

$$\boxed{C_{z} \approx 20.1\ pF}$$

最后：

$$R_{z} = \frac{1}{2\pi f_{z}C_{z}}$$

$$\boxed{R_{z} \approx 8.93\ k\Omega}$$

所以第一版 loop filter 是：

| 元件         | 初始值       |
|--------------|--------------|
| $R_{z}$      | 8.9 kΩ       |
| $C_{z}$      | 20.1 pF      |
| $C_{p}$      | 0.93 pF      |
| Zero         | 0.887 MHz    |
| Pole         | 20 MHz       |
| Crossover    | 3 MHz        |
| Phase margin | $65^{\circ}$ |

这些不是 tapeout 值，而是 schematic 起点。加入 CP output resistance、VCO control-node capacitance、varactor parasitic、R/C PVT、routing RC、CP leakage、PFD delay 和 VCO gain variation 后，必须重新优化。

## 3.4 解决 $K_{VCO}$ 变化导致的带宽漂移

环路增益近似正比于：

$$I_{CP}K_{VCO}$$

而 Spec 中：

$$K_{VCO} = 100\text{–}250\ MHz/V$$

如果 $I_{CP}$ 固定，环路 gain 会变化 2.5 倍，带宽不可能一直保持在 2.5–3.5 MHz。

因此 charge-pump current 必须随 VCO band 调整：

$$I_{CP}\left( K_{V} \right) = I_{CP,nom}\frac{K_{V,nom}}{K_{V}}$$

代入 nominal：

$$I_{CP}\left( K_{V} \right) = 0.8\ mA\frac{150\ MHz/V}{K_{V}}$$

| $K_{VCO}$ | 所需 $I_{CP}$ |
|-----------|---------------|
| 100 MHz/V | 1.20 mA       |
| 150 MHz/V | 0.80 mA       |
| 200 MHz/V | 0.60 mA       |
| 250 MHz/V | 0.48 mA       |

这些值落在 0.4–1.6 mA 的 Spec 范围内。因此 calibration FSM 应根据 VCO band code 设置 CP current code。否则“programmable $I_{CP}$”只是寄存器表里一个漂亮但没被使用的字段。

## 3.5 计算 VCO Tank 参数

### 3.5.1 选择电感

第一版假设有效差分电感：

$$L_{tank} = 250\ pH$$

谐振关系：

$$f_{0} = \frac{1}{2\pi\sqrt{LC}}$$

所以：

$$C_{tank} = \frac{1}{\left( 2\pi f_{0} \right)^{2}L}$$

在 14 GHz：

$$\boxed{C_{tank,14G} \approx 517\ fF}$$

### 3.5.2 总调谐范围对应的电容范围

在 12.5 GHz：

$$\boxed{C_{\max} \approx 648\ fF}$$

在 15.5 GHz：

$$\boxed{C_{\min} \approx 422\ fF}$$

所以需要的有效可变电容跨度约为：

$$\Delta C = 648 - 422$$

$$\boxed{\Delta C \approx 227\ fF}$$

这是有效 tank capacitance，包含 inductor parasitic、cross-coupled device capacitance、output-buffer loading、switched-cap bank、varactor 和 routing。不能画一个 227 fF 的 capacitor bank，然后庆祝调谐范围完成。寄生电容会很有礼貌地替你重新设计频率。

### 3.5.3 Coarse capacitor bank 分辨率

小变化条件下：

$$\frac{\Delta f}{f} \approx - \frac{1}{2}\frac{\Delta C}{C}$$

因此：

$$\Delta C \approx 2C\frac{|\Delta f|}{f}$$

若 coarse step 为 50 MHz：

$$\Delta C_{50MHz} \approx 2(517\ fF)\frac{50\ MHz}{14\ GHz}$$

$$\boxed{\Delta C_{50MHz} \approx 3.69\ fF}$$

但 Spec 又要求 calibration 后控制电压位于可用范围的 30%–70%。可用控制范围为 0.15–0.65 V，30%–70% 对应大约 0.30–0.50 V，其频率覆盖仅为：

$$150\ MHz/V \times 0.2\ V = 30\ MHz$$

因此 coarse step 最好不超过 30 MHz，对应：

$$\Delta C_{unit} \approx 2(517\ fF)\frac{30\ MHz}{14\ GHz}$$

$$\boxed{\Delta C_{unit} \approx 2.22\ fF}$$

227 fF 总跨度需要约 102 个有效单位，因此至少需要：

$$\boxed{7\text{-bit equivalent coarse bank}}$$

实际建议使用 segmented bank：binary coarse MSB、thermometer fine LSB、dummy switch、common-centroid unit placement 和差分对称控制布线。

### 3.5.4 Fine varactor 范围

Fine control range 为：

$$0.15\text{–}0.65\ V$$

若：

$$K_{VCO} = 150\ MHz/V$$

则 fine frequency span：

$$\Delta f_{fine} = 150\ MHz/V \times 0.5\ V$$

$$\boxed{\Delta f_{fine} = 75\ MHz}$$

对应有效电容变化：

$$\Delta C_{fine} \approx 2(517\ fF)\frac{75\ MHz}{14\ GHz}$$

$$\boxed{\Delta C_{fine} \approx 5.5\ fF}$$

所以结构应为：约 227 fF coarse switched-cap range，加约 5–10 fF fine varactor range。Coarse bank 负责 PVT，varactor 只负责闭环调节，以保持较低的 $K_{VCO}$。

## 3.6 计算 VCO 启振 $g_{m}$

假设 tank Q：

$$Q = 15$$

电感的等效并联电阻近似：

$$R_{p} \approx Q\omega_{0}L$$

代入：

$$R_{p} = 15 \cdot 2\pi(14\ GHz)(250\ pH)$$

$$\boxed{R_{p} \approx 330\ \Omega}$$

对于 NMOS cross-coupled pair，差分负电阻近似：

$$R_{neg} \approx - \frac{2}{g_{m}}$$

启振条件：

$$\left| R_{neg} \right| < R_{p}$$

所以：

$$g_{m} > \frac{2}{R_{p}}$$

$$g_{m} > 6.1\ mS$$

加入 2 倍 startup margin：

$$\boxed{g_{m,startup,target} \geq 12.1\ mS/device}$$

如果 worst-case EM 后 Q 下降到 10：

$$R_{p} \approx 220\ \Omega$$

则：

$$\boxed{g_{m,startup,target} \geq 18.2\ mS/device}$$

若采用：

$$g_{m}/I_{D} = 12\ V^{- 1}$$

则每个器件最低电流：

$$I_{D} = \frac{18.2\ mS}{12\ V^{- 1}}$$

$$\boxed{I_{D} \approx 1.52\ mA/device}$$

这只是启振下限。最终 VCO 电流由 phase noise 决定，第一轮可 sweep：

$$\boxed{I_{VCO} = 8,\ 10,\ 12,\ 16\ mA}$$

并对每个点检查 phase-noise FOM、amplitude、$K_{VCO}$、tank loading、supply pushing、startup、PVT 和 PEX。

18 mW 的 VCO power Spec 对应：

$$I_{\max} = \frac{18\ mW}{0.8\ V} = 22.5\ mA$$

这是上限，不是要求一上来就把 22.5 mA 全烧掉。

## 3.7 PFD 和 Charge Pump 参数

### 3.7.1 Charge-pump 电压步进

总有效 loop-filter capacitance：

$$C_{tot} \approx 21\ pF$$

假设最小有效 UP/DN pulse：

$$t_{p} = 20\ ps$$

单次注入电荷：

$$Q_{p} = I_{CP}t_{p}$$

$$Q_{p} = 0.8\ mA \times 20\ ps = 16\ fC$$

控制电压变化：

$$\Delta V_{ctrl} = \frac{Q_{p}}{C_{tot}}$$

$$\boxed{\Delta V_{ctrl} \approx 0.76\ mV}$$

对应 VCO 瞬时频率变化：

$$\Delta f = K_{VCO}\Delta V_{ctrl}$$

$$\boxed{\Delta f \approx 114\ kHz}$$

这可用于检查 minimum phase correction、dead zone、limit cycle、reference spur 和 lock settling。

### 3.7.2 Charge-pump mismatch

要求 nominal mismatch 小于 1%。若最小脉冲为 20 ps，则 1% mismatch 对应残余电荷：

$$\Delta Q = 0.01I_{CP}t_{p} = 0.16\ fC$$

残余控制电压：

$$\Delta V = \frac{0.16\ fC}{21\ pF}$$

$$\boxed{\Delta V \approx 7.6\ \mu V}$$

对应频率调制：

$$\Delta f \approx 1.14\ kHz$$

实际 reference spur 更可能被 clock feedthrough、drain-voltage modulation、UP/DN switching skew、CP output resistance、leakage、PFD reset glitch 和 VCO control-line coupling 支配。所以只把 current mirror 做到“DC 1% matching”远远不够。

### 3.7.3 Charge-pump 拓扑

0.8 V supply 下要求：

$$V_{ctrl} = 0.15\text{–}0.65\ V$$

同时希望有效输出电阻高于 200 kΩ。简单 current mirror 很难同时满足 headroom 和输出阻抗。建议考虑 source-switched current steering、regulated low-voltage cascode、replica-biased CP、drain-voltage matching、差分 CP 加 common-mode control，以及 local amplifier 或 gain boosting。

电流源器件面积由 mismatch 决定：

$$\left( \frac{\sigma_{I}}{I} \right)^{2} \approx \frac{A_{\beta}^{2} + \left( g_{m}/I_{D} \right)^{2}A_{V_{T}}^{2}}{WL}$$

若要求三倍标准差小于 1%：

$$3\sigma_{I}/I < 1\%$$

则：

$$\boxed{WL \geq \left\lbrack \frac{\sqrt{A_{\beta}^{2} + \left( g_{m}/I_{D} \right)^{2}A_{V_{T}}^{2}}}{0.00333} \right\rbrack^{2}}$$

具体面积或 Fin 数只能由 PDK mismatch model 得到，不能凭一腔热情现场编造。

## 3.8 Divider 架构与参数

### 3.8.1 Divider 分解

选择：

$$56 = 2 \times 2 \times 2 \times 7$$

即：

$$14\ GHz \rightarrow 7\ GHz \rightarrow 3.5\ GHz \rightarrow 1.75\ GHz \rightarrow 250\ MHz$$

建议前三极使用 CML $\div 2$，最后一级使用 CMOS $\div 7$，避免在 14 GHz 直接做复杂 $\div 56$ programmable counter。

### 3.8.2 第一级 Divider 的再生要求

14 GHz 周期：

$$T = \frac{1}{14\ GHz} = 71.4\ ps$$

每半周期：

$$T/2 = 35.7\ ps$$

假设允许 latch 用约 7 ps 完成主要再生，节点总电容：

$$C_{L} = 12\ fF$$

再生时间常数：

$$\tau \approx \frac{C_{L}}{g_{m}}$$

因此：

$$g_{m} \geq \frac{12\ fF}{7\ ps}$$

$$g_{m} \geq 1.71\ mS$$

加入速度、PEX 和 PVT margin，第一版目标：

$$\boxed{g_{m,divider} = 4\text{–}5\ mS/device}$$

若：

$$g_{m}/I_{D} = 12\ V^{- 1}$$

则：

$$I_{D} \approx 0.33\text{–}0.42\ mA/device$$

完整 master-slave divider 的 tail current 可从 1.5–2 mA/latch 开始 sweep。第一阶段功耗约 2.5–3.5 mW，后续级逐级减小电流，使 divider 总功耗控制在约 6–8 mW。

## 3.9 CMU 输出 Buffer 参数

目标包括：14 GHz、300 mVppd nominal、30 fF maximum load、rise/fall time 小于 10 ps、added jitter 小于 8 fs。

### 3.9.1 电阻和电流

采用 CML buffer，初始选择：

$$R_{L} = 150\ \Omega$$

$$I_{tail} = 2\ mA$$

得到约：

$$V_{ppd} \approx I_{tail}R_{L}$$

$$\boxed{V_{ppd} \approx 300\ mV}$$

具体 swing 定义需按 differential topology 仿真确认。

输出极点：

$$f_{p} = \frac{1}{2\pi R_{L}C_{L}}$$

$$f_{p} = \frac{1}{2\pi(150\ \Omega)(30\ fF)}$$

$$\boxed{f_{p} \approx 35.4\ GHz}$$

对应一阶 rise time：

$$t_{r} \approx \frac{0.35}{f_{p}}$$

$$\boxed{t_{r} \approx 9.9\ ps}$$

满足 10 ps 初始目标。

### 3.9.2 Buffer 噪声要求

300 mVppd 的正弦时钟，差分峰值：

$$V_{pk} = 150\ mV$$

crossing slope：

$$\left| \frac{dV}{dt} \right| = 2\pi fV_{pk}$$

$$\boxed{\left| \frac{dV}{dt} \right| \approx 13.2\ mV/ps}$$

若 added jitter 小于 8 fs：

$$\sigma_{v} \leq \sigma_{t}\left| \frac{dV}{dt} \right|$$

$$\sigma_{v} \leq 0.008\ ps \times 13.2\ mV/ps$$

$$\boxed{\sigma_{v,buffer} \leq 106\ \mu V_{rms}}$$

这就是 output buffer 的 integrated voltage-noise target。

## 3.10 从 Supply Spec 反推 LDO 和隔离要求

VCO pushing：

$$K_{push} \leq 30\ MHz/V$$

注入：

$$10\ mV_{pp}$$

即：

$$V_{pk} = 5\ mV$$

频率偏移峰值：

$$\Delta f_{pk} = K_{push}V_{pk}$$

$$\boxed{\Delta f_{pk} = 150\ kHz}$$

正弦 FM 的 modulation index：

$$\beta = \frac{\Delta f_{pk}}{f_{m}}$$

小调制下单边 spur：

$$Spur \approx 20\log_{10}\left( \frac{\beta}{2} \right)$$

### 3.10.1 在 1 MHz 注入

$$\beta = 0.15$$

$$Spur \approx - 22.5\ dBc$$

目标小于 $- 50$ dBc，所以至少需要 27.5 dB 电源隔离。加入 6 dB margin：

$$\boxed{PSRR_{effective}(1\ MHz) \geq 34\ dB}$$

### 3.10.2 在 10 MHz 注入

$$\beta = 0.015$$

原始 spur：

$$- 42.5\ dBc$$

目标小于 $- 55$ dBc，需要 12.5 dB 隔离。加入 margin：

$$\boxed{PSRR_{effective}(10\ MHz) \geq 19\ dB}$$

这直接决定是否需要 local LDO、LDO bandwidth、RC/LC filtering、decap、analog supply island、VCO 与 digital divider 的供电分离，以及 substrate guard ring 和 deep-Nwell。

## 3.11 第一版可画原理图的参数表

| Block                        | 第一版参数                                    |
|------------------------------|-----------------------------------------------|
| PLL topology                 | Integer-N Type-II 3rd-order CPPLL             |
| Reference                    | 250 MHz differential                          |
| Output                       | 14 GHz                                        |
| Divide ratio                 | 56                                            |
| Divider chain                | CML $\div 2 \div 2 \div 2$ + CMOS $\div 7$    |
| Nominal bandwidth            | 3 MHz                                         |
| Phase margin                 | $65^{\circ}$                                  |
| $I_{CP}$                     | 0.8 mA nominal                                |
| $I_{CP}$ range               | 0.48–1.20 mA，补偿 $K_{V}$                    |
| $K_{VCO}$                    | 150 MHz/V nominal                             |
| $R_{z}$                      | 8.9 kΩ                                        |
| $C_{z}$                      | 20.1 pF                                       |
| $C_{p}$                      | 0.93 pF                                       |
| Loop zero                    | 0.887 MHz                                     |
| Loop HF pole                 | 20 MHz                                        |
| VCO inductance               | 250 pH effective starting point               |
| Tank capacitance at 14 GHz   | 517 fF                                        |
| Tank capacitance range       | 422–648 fF                                    |
| Effective coarse span        | about 227 fF                                  |
| Effective coarse LSB         | 2.2–3.0 fF                                    |
| Coarse bank                  | 7-bit equivalent, segmented                   |
| Fine varactor range          | about 5.5 fF effective                        |
| VCO startup $g_{m}$          | $\geq 18$ mS/device at pessimistic $Q = 10$   |
| Initial VCO current sweep    | 8–16 mA                                       |
| First divider device $g_{m}$ | 4–5 mS                                        |
| First divider latch current  | 1.5–2 mA                                      |
| Output-buffer load resistor  | 150 Ω                                         |
| Output-buffer tail current   | 2 mA                                          |
| Output swing                 | about 300 mVppd                               |
| Output pole at 30 fF         | about 35 GHz                                  |
| Required supply isolation    | $\geq 34$ dB at 1 MHz，$\geq 19$ dB at 10 MHz |

## 3.12 如何把电气参数变成晶体管尺寸

不能使用平方律直接算最终 $W/L$。正确流程是建立 PDK LUT：

$$g_{m}/I_{D},\quad g_{ds}/I_{D},\quad C_{gg}/W,\quad C_{gd}/W,\quad f_{T},\quad J_{D} = I_{D}/W$$

### 3.12.1 根据速度和增益选择沟道长度

- VCO cross-coupled pair：接近 minimum $L$，但要检查 $r_{o}$、flicker upconversion 和 reliability；
- charge-pump current source：适当增加 $L$，提高 $r_{o}$ 和 matching；
- divider latch：minimum 或 near-minimum $L$；
- output CML buffer：由速度、swing 和 output loading 决定；
- reference buffer：由噪声和 slew 决定。

### 3.12.2 选择 $g_{m}/I_{D}$

| Circuit                 | 初始 $g_{m}/I_{D}$ |
|-------------------------|--------------------|
| VCO cross-coupled pair  | 10–14 V$^{- 1}$    |
| Divider latch           | 8–12 V$^{- 1}$     |
| CP current source       | 10–16 V$^{- 1}$    |
| CML output buffer       | 8–12 V$^{- 1}$     |
| Bias/reference circuits | 15–20 V$^{- 1}$    |

### 3.12.3 计算电流

$$I_{D} = \frac{g_{m}}{g_{m}/I_{D}}$$

### 3.12.4 从 PDK 查电流密度

$$W = \frac{I_{D}}{J_{D}}$$

FinFET 工艺中转换成 Fin 数、finger 数、stack 数、multiplier 和 total effective width。

### 3.12.5 回读寄生并重新闭环

得到尺寸以后必须重新提取：

$$C_{gs},\ C_{gd},\ C_{db},\ g_{m},\ g_{ds},\ f_{T}$$

然后重新计算 VCO frequency、$K_{VCO}$、tank Q、divider regeneration、output pole、PLL bandwidth、phase margin 和 phase noise。

这不是一次计算，而是闭环：

$$\boxed{\text{Spec} \rightarrow \text{Electrical target} \rightarrow \text{Device sizing} \rightarrow \text{Parasitic} \rightarrow \text{Spec recheck}}$$

## 3.13 实际执行顺序

真正进入设计时，建议按以下顺序推进：

1.  用 Python/Matlab 建 phase-domain PLL model，确认 3 MHz 是否为 filtered jitter 最优点。
2.  建立 VCO $L/C$、coarse bank、varactor 和 $K_{V}$ 模型。
3.  完成 VCO EM inductor candidate sweep。
4.  设计并验证高速 $\div 2$ divider。
5.  设计 PFD/CP 和无源 filter。
6.  通过 $I_{CP}$ code 补偿 $K_{V}$。
7.  做完整 phase-noise contribution integration。
8.  加入 output buffer 和 supply injection。
9.  做 PVT 和 Monte Carlo。
10. 做 block PEX，再做 full-loop PEX。
11. 将 CMU 输出接入 distribution、CCU 和 serializer，验证 endpoint 55 fs，而不是只验证 VCO pin。

这套参数已经足以开始第一版 behavioral model、loop-filter synthesis、VCO tank sweep 和 divider schematic。真正不能确定的只剩 PDK 相关量，例如 Fin 数、实际 Q、器件噪声、mismatch 和 MIM 密度。这些必须由 PDK 回答。任何在没有 PDK 时给出“NMOS 宽度 7.2 μm”的人，通常不是算得准，只是小数点写得很有自信。

# 参考资料

1.  OIF, **Common Electrical I/O (CEI)-224G**：<https://www.oiforum.com/technical-work/hot-topics/common-electrical-i-o-cei-224g/>
2.  IEEE 802.3dj public contribution, **4 MHz reference CRU / transmit jitter discussion**：<https://www.ieee802.org/3/dj/public/24_03/ghiasi_3dj_01a_2403.pdf>
3.  Synopsys 224 Gb/s 3 nm FinFET transceiver paper，ISSCC 2024 Session 7.3，公开检索入口：<https://ieeexplore.ieee.org/document/10454537/>
