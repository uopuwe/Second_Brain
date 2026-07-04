---

title: "PAM4 Receiver Basics"
domain: "AnalogIC_SerDes"
tags:

* PAM4
* SerDes
* Receiver
* ADC
* CDR
* Equalization
* PCIe7
* Synopsys
  created: 2026-07-01
  updated: 2026-07-01
  source: "ChatGPT technical notes and Synopsys role preparation"
  status: "active"

---

# PAM4 Receiver Basics

## 中文补充翻译

这篇笔记解释 PAM4 receiver 的基本概念。PAM4 使用四个电平，每个 symbol 传 2 bits，因此在相同 bit rate 下可以把 symbol rate 降为 NRZ 的一半，但代价是 vertical eye margin 大幅缩小，需要更高线性度、更准确 threshold、更好的 equalization 和更谨慎的 jitter 控制。

PAM4 RX 通常包含 AFE、CTLE、sampler 或 ADC、threshold / slicer、FFE/DFE/DSP、CDR 和 adaptation loop。由于有三个 eye 和多个 decision threshold，offset、gain error、ISI、noise、jitter 和 level-dependent behavior 都比 NRZ 更敏感。

对 PCIe 7.0 这类高速链路，PAM4 的核心 tradeoff 是用 vertical margin 换 bandwidth。不能只说 symbol UI 变长而认为 clocking 更容易；timing error 会通过 `dV/dt` 变成 voltage error，并消耗已经很小的 PAM4 eye margin。

## Purpose

This note summarizes the basics of a PAM4 receiver for high-speed SerDes preparation.

The goal is to understand why PAM4 is used, why it is harder than NRZ, and what receiver blocks are needed to recover PAM4 data.

---

## 1. Big Picture

PAM4 uses four amplitude levels to carry two bits per symbol.

Compared with NRZ:

```text
NRZ: 2 levels, 1 bit per symbol
PAM4: 4 levels, 2 bits per symbol
```

PAM4 improves spectral efficiency but reduces vertical noise margin.

The receiver must determine which of four levels was sent while also recovering timing through a lossy and noisy channel.

---

## 2. Key Concepts

Important PAM4 RX concepts:

* four amplitude levels
* three eye openings
* Gray coding
* vertical eye closure
* horizontal eye closure
* slicer thresholds
* level separation
* linearity
* SNR
* CTLE
* FFE / DFE
* ADC-based receiver
* CDR
* timing error detector
* offset / gain calibration
* decision feedback
* BER / SER

PAM4 receiver design is a joint amplitude and timing problem.

---

## 3. Why PAM4 Is Used

PAM4 is used because it doubles bits per symbol without doubling symbol rate.

This helps when channel bandwidth is limited.

But the cost is smaller vertical spacing:

```text
Same full-scale swing
down
4 levels instead of 2
down
smaller distance between adjacent levels
down
less noise margin
```

So PAM4 requires better equalization, linearity, threshold control, and noise management.

---

## 4. PAM4 RX Building Blocks

A simplified PAM4 RX may include:

* termination
* CTLE
* VGA or gain control
* slicers or ADC
* threshold generation
* offset calibration
* FFE / DFE / DSP equalization
* CDR / timing recovery
* adaptation engine
* deserializer

Slicer-based RX:

```text
Analog front-end
down
multiple thresholds
down
PAM4 decisions
```

ADC-based RX:

```text
Analog front-end
down
ADC samples
down
DSP equalization and decisions
```

---

## 5. Thresholds and Linearity

PAM4 needs decision thresholds between adjacent levels.

Issues:

* threshold offset
* level compression
* gain error
* nonlinearity
* common-mode shift
* reference noise
* temperature drift
* supply noise

If thresholds move, symbol decisions become wrong.

Important chain:

```text
reference or offset error
down
threshold movement
down
vertical eye margin loss
down
symbol errors
```

---

## 6. Equalization

PAM4 still suffers from channel loss and ISI.

Equalization blocks:

* TX FFE
* RX CTLE
* RX FFE
* DFE
* DSP equalization

Equalization must preserve level information while reducing ISI.

Bad equalization can:

* close one or more PAM4 eyes
* bias CDR phase detection
* cause wrong DFE decisions
* distort level spacing
* increase error propagation

---

## 7. CDR and Timing Recovery

PAM4 timing recovery is harder than NRZ because transitions have different amplitudes and vertical margin is smaller.

CDR must handle:

* data-dependent transitions
* ISI-distorted edges
* amplitude noise affecting timing decisions
* threshold errors
* equalizer adaptation interaction

Key idea:

```text
PAM4 reduces vertical margin.
Jitter reduces horizontal margin.
The receiver must manage both at the same time.
```

---

## 8. SerDes / PCIe 7.0 Relevance

PCIe 7.0 uses PAM4 at 128 GT/s.

This makes PAM4 RX topics directly relevant:

* smaller eye openings
* stronger equalization need
* tighter jitter tolerance
* careful clock recovery
* more calibration
* stronger power integrity requirements
* possible ADC-based RX tradeoffs

待确认: The exact PCIe 7.0 implementation details used by Synopsys are unknown until internal documentation is available.

---

## 9. Synopsys Preparation Relevance

For Synopsys preparation, this note helps connect likely clocking / LDO work to receiver margin.

Useful focus:

* understand why PAM4 is sensitive to noise and jitter
* explain how threshold error causes symbol errors
* connect PLL / CDR jitter to eye closure
* connect LDO / reference noise to vertical margin
* understand why ADC-based RX is attractive for high-speed PAM4

Batch 2 emphasis:

* PAM4 should be studied through both amplitude margin and timing margin.
* ADC-based RX is useful long-term because it exposes amplitude information for DSP equalization and adaptation, but it increases clock jitter, reference noise, power, and calibration pressure.
* CTLE / FFE / DFE settings affect the waveform used by CDR, so receiver margin cannot be separated cleanly into independent equalization and timing problems.

---

## 10. Interview Explanation

Short explanation:

```text
PAM4 uses four voltage levels to carry two bits per symbol, which improves bandwidth efficiency but reduces vertical eye margin compared with NRZ. A PAM4 receiver must recover both amplitude and timing through a lossy channel. It needs equalization, threshold or ADC accuracy, CDR, calibration, and good power integrity. Noise, nonlinearity, offset, jitter, and ISI all consume margin.
```

Synopsys-focused explanation:

```text
For PCIe 7.0, PAM4 means clocking and LDO work directly affect RX margin. PLL and CDR jitter close the eye horizontally, while supply noise, reference noise, and threshold errors close the eye vertically. That is why clocking, power integrity, and receiver architecture should be discussed together.
```

---

## 11. Common Interview Questions

## Q1: Why use PAM4?

It carries 2 bits per symbol, improving bandwidth efficiency without requiring the same proportional increase in symbol rate.

## Q2: What is the main penalty of PAM4?

Smaller vertical eye opening and higher sensitivity to noise, nonlinearity, offset, and jitter.

## Q3: How many eyes does PAM4 have?

Three vertical eyes between four amplitude levels.

## Q4: Why is CDR harder in PAM4?

Different transition amplitudes, smaller vertical margin, ISI, and threshold errors can corrupt timing information.

## Q5: Why might ADC-based RX be used?

It captures amplitude information digitally and enables flexible DSP equalization and calibration.

---

## 12. Open Questions

* 待确认: Is the relevant Synopsys PCIe 7.0 receiver slicer-based or ADC-based?
* 待确认: What PAM4 decision / threshold architecture is used?
* 待确认: What equalization blocks are in the analog front-end?
* 待确认: How is timing recovery performed?
* 待确认: How are thresholds calibrated?
* 待确认: How is vertical margin measured internally?
* 待确认: How is PAM4 receiver margin connected to LDO and reference specs?

---

## Source Conversations / Source Packets

* `../../00_Inbox/manual_batches/batch2_serdes_pcie_pll_cdr_adc_2026-07-01/source_packet.md`

---

## 13. Related Notes

* `serdes_architecture_overview.md`
* `pcie7_overview.md`
* `ctle_ffe_dfe_notes.md`
* `../ADC/adc_based_receiver.md`
* `../PLL_CDR_Clocking/cdr_fundamentals.md`
* `../PLL_CDR_Clocking/pll_phase_noise_jitter.md`
* `../LDO_Bandgap/serdes_power_integrity.md`
* `../Study_Plans/synopsys_4_week_prep_plan.md`

---

## 14. Next Actions

1. Add diagrams of PAM4 levels and three eyes later.
2. Add notes on Gray coding and error impact.
3. Link to ADC-based receiver details.
4. Add measured / simulated margin examples when available.

---

## Last Updated

2026-07-01
