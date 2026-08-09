---
title: "SerDes Architecture Overview"
domain: "AnalogIC_SerDes"
tags:
  - SerDes
  - Architecture
  - PAM4
  - PCIe7
  - Equalization
  - CDR
  - PLL
  - ADC
  - Synopsys
created: 2026-07-01
updated: 2026-08-08
source: "ChatGPT technical notes and Synopsys role preparation"
status: "active"
---

# SerDes Architecture Overview

## 中文补充翻译

这篇笔记概览 SerDes PHY 的系统架构。SerDes 的核心任务是把并行低速数据转换成高速串行信号发送出去，再在接收端从有损 channel 中恢复数据、时钟和符号判决。

典型链路包括 TX serializer、driver、FFE/pre-emphasis、package/PCB/channel、RX termination、CTLE、sampler/ADC、DFE/DSP、CDR 和 clocking。每个模块都不是孤立的：channel loss 会决定 equalization 需求，equalizer 会改变 CDR 看到的边沿和误差信号，PLL/CDR jitter 会影响 sampling margin，LDO/power noise 会同时造成 amplitude error 和 timing error。

对 PCIe 7.0 / PAM4 来说，SerDes 架构重点在于带宽、线性度、jitter、vertical margin、equalization、power integrity 和 verification 的联合 tradeoff。面试或 design review 中要能从完整 signal chain 解释问题，而不是只讲单个 block。

## Purpose

This note gives a system-level map of a modern high-speed SerDes PHY.

The goal is to understand where TX, RX, equalization, PLL, CDR, ADC, LDO, and calibration blocks fit before going deeper into individual circuits.

---

## 1. Big Picture

SerDes means serializer / deserializer.

It converts parallel data into high-speed serial data for transmission over a channel, then recovers the data at the receiver.

Simplified chain:

```text
Parallel data
down
Serializer
down
TX equalization / driver
down
Package / channel / connector
down
RX front-end / CTLE
down
Sampler or ADC
down
FFE / DFE / DSP
down
CDR / timing recovery
down
Deserializer
down
Parallel data
```

The architecture is a system of loops: timing recovery, equalization adaptation, calibration, and power regulation all interact.

---

## 2. Key Concepts

Important SerDes concepts:

* unit interval
* channel insertion loss
* return loss
* ISI
* crosstalk
* PAM4 levels
* TX FFE
* RX CTLE
* RX FFE
* DFE
* CDR
* jitter budget
* eye diagram
* bathtub curve
* BER / SER
* link training
* ADC-based receiver
* calibration
* power integrity

The core problem:

```text
Transmit enough information through a lossy channel,
then recover amplitude and timing with acceptable BER.
```

---

## 3. Transmitter Path

The TX path may include:

* data muxing / serialization
* high-speed clocking
* TX FFE taps
* output driver
* impedance control
* common-mode control
* pre-driver stages
* calibration for swing and impedance

TX FFE intentionally shapes the transmitted waveform to compensate for channel loss.

Simple idea:

```text
Pre-distort signal at TX
down
channel loss partially cancels distortion
down
RX sees a more open eye
```

---

## 4. Channel

The channel includes:

* package
* PCB traces
* connectors
* vias
* cables if present
* retimers or redrivers if present

Channel issues:

* high-frequency loss
* reflections
* impedance discontinuities
* crosstalk
* skew
* dispersion

High-frequency loss creates ISI, which is the reason equalization is mandatory.

---

## 5. Receiver Path

The RX path may include:

* termination
* ESD and input protection
* CTLE
* variable gain
* sampler or ADC
* slicers for PAM4 thresholds
* FFE / DFE / DSP
* CDR
* adaptation loops
* offset / gain / threshold calibration

The RX must recover both:

```text
Amplitude information
and
Timing information
```

PAM4 makes amplitude recovery harder. High speed makes timing recovery harder.

### 5.1 RX Termination And Bias Checkpoint

中文：RX termination 的第一层任务是让负载阻抗接近 channel 特性阻抗，以降低反射。对给定频率处的等效负载 $Z_L$ 和特性阻抗 $Z_0$，反射系数为

English: The first job of RX termination is to make the effective load impedance approach the channel characteristic impedance and thereby reduce reflections. For effective load $Z_L$ and characteristic impedance $Z_0$ at the frequency of interest, the reflection coefficient is

$$
\Gamma=\frac{Z_L-Z_0}{Z_L+Z_0}.
$$

中文：$\Gamma=0$ 只表示该模型和该频率点的匹配，不代表 package、ESD、T-coil、输入寄生和 frequency-dependent channel 在宽带内完全匹配。因此 termination 应与 return loss、eye、ringing、CTLE/ADC 输入范围和 PVT calibration 一起验证。

English: $\Gamma=0$ proves matching only for that model and frequency point; it does not prove broadband matching once package, ESD, T-coil, input parasitics, and the frequency-dependent channel are included. Termination should therefore be verified together with return loss, eye opening, ringing, CTLE/ADC input range, and PVT calibration.

中文：差分 RX 可使用跨 RXP/RXN 的约 $100\ \Omega$ 端接，也可使用两个约 $50\ \Omega$ 电阻接到 $V_{CM}$ 的 Thevenin 形式。后者同时提供 differential termination 和 RX common-mode bias，对 AC-coupled link 尤其重要；但 $V_{CM}$ 的噪声、阻抗和 decoupling 会直接影响输入。

English: A differential RX can use an approximately $100\ \Omega$ resistor across RXP/RXN or a Thevenin form with two approximately $50\ \Omega$ resistors tied to $V_{CM}$. The latter provides both differential termination and RX common-mode bias, which is especially important for an AC-coupled link; however, the noise, impedance, and decoupling of $V_{CM}$ then directly affect the input.

### 5.2 Termination-Bias Network Analysis Workflow

中文：多电阻 termination/bias network 不应只凭电阻数量或模糊电路记忆猜测 $V_1$、$V_2$。第一步是在 TX 静态、AC coupling 已隔离 DC、RX input leakage 可忽略或已建模的条件下做 DC nodal analysis；第二步把同一网络分解成 differential-mode termination 与 common-mode bias；第三步再加入 ESD、pad、T-coil、receiver input conductance 和 calibration switch 的寄生，检查 broadband impedance 与 bias settling。

English: A multi-resistor termination and bias network should not be solved by guessing $V_1$ and $V_2$ from the resistor count or from an uncertain memory of the schematic. First perform DC nodal analysis with explicit assumptions about the static transmitter, AC coupling, and receiver input leakage. Next decompose the same network into differential-mode termination and common-mode bias. Finally add ESD, pad, T-coil, receiver-input conductance, calibration-switch parasitics, and verify broadband impedance and bias settling.

对连接到多个 Thevenin source 的线性节点 $V_x$，KCL 可写成：

For a linear node $V_x$ connected to several Thevenin sources, KCL can be written as:

$$
V_x=\frac{\sum_k G_kV_k+I_{ext}}{\sum_kG_k+G_{in}},
$$

其中 $G_k=1/R_k$ 是第 $k$ 条支路的 conductance，$V_k$ 是该支路的 DC source voltage，$I_{ext}$ 是按流入节点为正定义的外部 DC current，$G_{in}$ 是 receiver input 的线性化 DC conductance。该式只适用于线性 DC network；若 ESD diode、inverter input、termination calibration MOS 或 protection clamp 导通，必须使用分段 operating-point analysis。

where $G_k=1/R_k$ is the conductance of branch $k$, $V_k$ is its DC source voltage, $I_{ext}$ is external DC current defined positive into the node, and $G_{in}$ is the linearized DC conductance of the receiver input. This expression applies only to a linear DC network. Conducting ESD diodes, inverter inputs, termination-calibration MOS devices, or protection clamps require piecewise operating-point analysis.

中文：求出两个输入节点后，应同时计算 $V_{CM,in}=(V_1+V_2)/2$ 与 $V_{DM}=V_1-V_2$。正常静态 bias 可能要求 $V_{DM}\approx0$，但这不证明 differential impedance 正确；相反，满足 $100\ \Omega$ differential termination 也不证明 common-mode 落在 CTLE、slicer 或 ADC input range 内。两种 mode 必须分别验证。

English: After solving the two input nodes, compute both $V_{CM,in}=(V_1+V_2)/2$ and $V_{DM}=V_1-V_2$. A normal static bias may require $V_{DM}\approx0$, but that does not prove that the differential impedance is correct. Conversely, satisfying a $100\ \Omega$ differential termination does not prove that common mode lies within the CTLE, slicer, or ADC input range. The two modes must be verified separately.

---

## 6. Equalization

Equalization fights ISI.

Common blocks:

* TX FFE for pre-emphasis / de-emphasis
* RX CTLE for analog high-frequency boost
* RX FFE for linear post-processing
* DFE for cancelling post-cursor ISI
* DSP adaptation in ADC-based receivers

Important point:

```text
Equalization is not independent from CDR.
The waveform created by equalization is the waveform used for timing recovery.
```

---

## 7. Clocking and CDR

SerDes requires clean clocking for:

* TX serialization
* TX launch timing
* RX sampling
* phase interpolation
* deserialization
* calibration and DSP timing

CDR uses received data transitions to place the sampling clock.

Key clocking risks:

* PLL phase noise
* clock buffer jitter
* supply-induced jitter
* phase interpolator nonlinearity
* CDR lock to poor phase under ISI
* jitter peaking

---

## 8. SerDes / PCIe 7.0 Relevance

PCIe 7.0 is a SerDes PHY challenge because it uses 128 GT/s PAM4 signaling.

The architecture must manage:

* small PAM4 vertical eye
* tight jitter budget
* heavy channel equalization
* robust CDR
* power and area limits
* link training and adaptation
* compliance and margin testing

PCIe 7.0 should be studied as a system-level PHY problem, not only as a protocol standard.

---

## 9. Synopsys Preparation Relevance

For Synopsys preparation, this note is the map that connects detailed notes:

* PLL and jitter notes explain clock quality.
* CDR notes explain timing recovery.
* LDO notes explain supply sensitivity.
* ADC notes explain possible PAM4 RX architecture.
* Equalization notes explain channel compensation.

Unknown internal implementation details should remain `待确认` until onboarding.

Batch 2 emphasis:

* Use this note as the top-level map linking PCIe 7.0 clocking, PLL jitter, CDR behavior, CTLE / FFE / DFE, ADC-based PAM4 RX, and LDO power integrity.
* Frame the career transition as moving from block-level analog ownership toward SerDes IP system thinking.
* Treat LDO, PLL, ADC, and automation experience as credible bridges into high-speed PHY work when each story is tied to eye margin, BER, jitter, or calibration robustness.

---

## 10. Interview Explanation

Short explanation:

```text
A SerDes PHY serializes parallel data, drives it through a lossy high-speed channel, then recovers the data with an RX front-end, equalization, CDR, and deserializer. The main impairments are channel loss, ISI, noise, jitter, crosstalk, and power supply disturbance. In PCIe 7.0 PAM4, both amplitude and timing margins are tight, so equalization, clocking, CDR, ADC or slicer design, and power integrity all interact.
```

Synopsys-focused explanation:

```text
For Synopsys preparation, I should understand the SerDes architecture well enough to place my likely clocking and LDO work in the full PHY. PLL jitter and LDO supply noise are not isolated block metrics; they affect RX sampling, TX launch timing, eye margin, and BER.
```

---

## 11. Common Interview Questions

## Q1: What are the main blocks of a SerDes PHY?

Serializer, TX equalization and driver, channel, RX front-end, CTLE, sampler or ADC, FFE / DFE / DSP, CDR, deserializer, PLL, references, regulators, and calibration.

## Q2: Why is equalization needed?

The channel attenuates high-frequency content and creates ISI. Equalization compensates for that distortion.

## Q3: Why is CDR needed?

The receiver needs to recover the correct sampling phase from incoming data transitions.

## Q4: Why is PAM4 harder than NRZ?

PAM4 carries 2 bits per symbol but has smaller vertical eye openings, making it more sensitive to noise, nonlinearity, threshold error, and jitter.

## Q5: How does LDO design connect to SerDes?

LDO noise and finite PSRR can disturb PLL, CDR, RX front-end, ADC, and references, reducing eye margin.

---

## 12. Open Questions

* 待确认: Which SerDes blocks will I directly work on at Synopsys?
* 待确认: How is the PCIe 7.0 PHY partitioned between analog, mixed-signal, and digital teams?
* 待确认: Is the receiver slicer-based or ADC-based?
* 待确认: What equalization architecture is used?
* 待确认: What CDR architecture is used?
* 待确认: Which blocks have dedicated LDOs?
* 待确认: What documents should I read first after joining?

---

## Source Conversations / Source Packets

* `../../00_Inbox/manual_batches/batch2_serdes_pcie_pll_cdr_adc_2026-07-01/source_packet.md`
* `../../00_Inbox/manual_batches/chat_delta_2026-08-08/new_conversations/6a49c746-0710-83ea-844a-c1c5cb24bcdf.md` - "SerDes 端接电阻讲解"; conversation-derived formulas and topology summary, not a standards or signoff source.
* `../../00_Inbox/manual_batches/chat_delta_2026-08-08/new_conversations/6a4aa78a-beb0-83ea-874f-6d53a24afa40.md` - "SerDes 终端偏置网络"; only the general nodal-analysis workflow was promoted because the reconstructed interview schematic remained uncertain.

---

## 13. Related Notes

* `pcie7_overview.md`
* `pam4_receiver_basics.md`
* `ctle_ffe_dfe_notes.md`
* `../PLL_CDR_Clocking/pcie7_clocking_notes.md`
* `../PLL_CDR_Clocking/pll_fundamentals.md`
* `../PLL_CDR_Clocking/cdr_fundamentals.md`
* `../ADC/adc_based_receiver.md`
* `../LDO_Bandgap/serdes_power_integrity.md`
* `../Study_Plans/synopsys_4_week_prep_plan.md`

---

## 14. Next Actions

1. Add a cleaner TX / RX block diagram later.
2. Expand the equalization section after studying CTLE / FFE / DFE.
3. Add architecture-specific notes after reading internal Synopsys material.
4. Use this note as the starting point for interview explanations.

---

## 15. Batch 1 Extracted Knowledge - 2026-07-02

### 15.1 224 Gb/s ADC/DSP-Based Transceiver Pattern

From the public Synopsys 224 Gb/s PAM4 transceiver discussion, the reusable architecture pattern is:

```text
TX DSP -> serializer -> DAC / driver -> channel
channel -> termination / T-coil -> CTLE -> VGA -> TI-SAR ADC -> DSP FFE / DFE / MLSD -> CDR / timing recovery
```

Important design points:

- PAM4 at 224 Gb/s corresponds to 112 Gbaud, so analog bandwidth and clocking are strongly constrained.
- A 1/8-rate clocking architecture reduces full-rate clock distribution burden, but requires accurate multi-phase clock generation and phase correction.
- ADC/DSP-based receivers move more equalization into digital logic, but sampler aperture jitter, AFE noise, ADC quantization, and TI-ADC mismatch remain analog limits.
- MLSD can recover margin beyond plain DFE when the post-equalized channel still has controlled memory.
- Inverter-based AFE stages can be attractive for speed and energy, but biasing, linearity, common-mode control, and PVT sensitivity become central design questions.

待确认: Whether the new role directly works on the same architecture, same 224G design family, or a different Synopsys Interface IP project must be confirmed during onboarding.

### 15.2 Clocking Hierarchy Lessons

The 224G discussion emphasized clock hierarchy rather than only a standalone PLL:

- Shared CMU / PLL generates a clean base clock.
- Multi-phase clocks feed TX and RX clock-control units.
- Injection-locked oscillators, phase rotators, or phase-shifting buffers can create fine phase placement.
- Background drift correction is needed across voltage and temperature.
- Clocking must be evaluated with the AFE, ADC, DSP timing recovery, and link margin, not as an isolated block.

### 15.3 Interview-Safe Framing

Safe framing for prior work:

- Strong direct experience: ADC, SAR/TI concepts, PLL/DCO, regulator/LDO, bandgap/reference, analog verification, modeling.
- SerDes-relevant bridge: system-level PAM4 receiver modeling, CTLE/FFE/DFE tradeoffs, jitter/noise budgeting, and analog-to-DSP boundary reasoning.
- Avoid overclaim: do not imply direct SerDes silicon ownership or 224G tapeout unless there is specific evidence.

### 15.4 Source Conversations

- `../../00_Inbox/raw_chat_exports/chatgpt_export_2026-07-01/md_by_conversation/2026-05-04__总结A_224Gbs_Transceiver.md`
- `../../00_Inbox/raw_chat_exports/chatgpt_export_2026-07-01/md_by_conversation/2026-06-02__Synopsys入职技术准备.md`
- `../../00_Inbox/raw_chat_exports/chatgpt_export_2026-07-01/md_by_conversation/2026-04-29__职位匹配与薪资分析.md`

---

## Last Updated

2026-08-08
