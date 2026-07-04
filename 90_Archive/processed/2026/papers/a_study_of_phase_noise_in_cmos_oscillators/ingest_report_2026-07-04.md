# Ingest Report: A Study of Phase Noise in CMOS Oscillators

Date: 2026-07-04

Pipeline: `00_Inbox/incoming/` -> canonical note merge -> archive -> report

Operating manual references:

- [AGENTS.md](<../../../../../.codex/AGENTS.md>)
- [ingest.md](<../../../../../.codex/ingest.md>)
- [mandatory_rules.md](<../../../../../.codex/core/mandatory_rules.md>)
- [knowledge_architecture.md](<../../../../../.codex/knowledge_architecture.md>)

## Summary

本次 ingest 处理了一篇 CMOS oscillator phase-noise 经典论文，并将可复用知识合并到现有 canonical note。没有创建新的 handbook 或重复主题文件。

This ingest processed one classic CMOS oscillator phase-noise paper and merged reusable knowledge into the existing canonical note. No new handbook or duplicate topic file was created.

## Processed Files

| Source file | Source type | Classification | Status |
|---|---|---|---|
| `00_Inbox/incoming/papers/A Study of Phase Noise in CMOS Oscillators BRMar96.pdf` | IEEE JSSC paper PDF | PLL / VCO / CMOS oscillator phase noise / SerDes clocking | Processed and archived |

## Canonical Note Updates

| Canonical note | Update |
|---|---|
| [pll_phase_noise_jitter.md](<../../../../../01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_phase_noise_jitter.md>) | Added `## 24. CMOS Oscillator Phase Noise Mechanisms` with paragraph-level Chinese-English bilingual explanations, Markdown LaTeX formulas, source provenance, and design-review implications. |

新增内容重点覆盖 Razavi paper 中最适合长期复用的工程知识：open-loop Q 的 phase-slope interpretation、additive/high-frequency multiplicative/low-frequency multiplicative noise 分类、FM sensitivity、power/swing/stage-count tradeoff、simulation artifact warning、measurement normalization，以及 differential CMOS oscillator 的 supply/substrate coupling。

The added content focuses on the engineering knowledge from the Razavi paper that is most reusable over decades: open-loop Q as phase-slope interpretation, additive/high-frequency multiplicative/low-frequency multiplicative noise classification, FM sensitivity, power/swing/stage-count tradeoff, simulation artifact warnings, measurement normalization, and supply/substrate coupling in differential CMOS oscillators.

## New Notes

没有创建新笔记。主题已经由现有 canonical note `pll_phase_noise_jitter.md` 覆盖，创建新 note 会违反 one-topic-one-canonical-note 原则。

No new note was created. The topic is already covered by the existing canonical note `pll_phase_noise_jitter.md`, and creating another note would violate the one-topic-one-canonical-note principle.

## Formula Handling

| Formula or model | Handling |
|---|---|
| Open-loop Q as phase slope | Converted to Markdown LaTeX and explained bilingually. |
| Frequency modulation from control/bias/supply noise | Converted to Markdown LaTeX and tied to measurable sensitivities such as $K_{VCO}$, supply pushing, and bias-current sensitivity. |
| First-order phase-noise versus power intuition | Added as a bounded sanity-check relationship, not as a universal law. |

## Index And Link Updates

没有新增 canonical note，因此没有更新 MOC 或 index 页面。现有 `[[pll_phase_noise_jitter]]` entry remains the correct topic entry point.

No MOC or index page was updated because no new canonical note was created. The existing `[[pll_phase_noise_jitter]]` entry remains the correct topic entry point.

## Archive Actions

| Original source | Archive destination |
|---|---|
| `00_Inbox/incoming/papers/A Study of Phase Noise in CMOS Oscillators BRMar96.pdf` | [A Study of Phase Noise in CMOS Oscillators BRMar96.pdf](<A Study of Phase Noise in CMOS Oscillators BRMar96.pdf>) |

归档操作只作用于 `00_Inbox/incoming/` ingestion lane，未扫描、移动、归档或修改任何 legacy ChatGPT export / conversation-processing folder。

The archive action applied only to the `00_Inbox/incoming/` ingestion lane. No legacy ChatGPT export or conversation-processing folder was scanned, moved, archived, or modified.

## Manual Review Items

1. Razavi paper 的数值结果来自 0.5 um CMOS ring/relaxation oscillator，不能直接当作现代 PCIe 6.0/7.0 SerDes PLL/DCO signoff target。
2. The numerical results in the Razavi paper come from 0.5 um CMOS ring/relaxation oscillators and should not be used directly as modern PCIe 6.0/7.0 SerDes PLL/DCO signoff targets.

3. paper 中部分 equation extraction from PDF text was visually degraded, so the canonical note promotes robust mechanisms and clearly recoverable formulas rather than fragile copied equation numbering.
4. Some equation extraction from the PDF text was visually degraded, so the canonical note promotes robust mechanisms and clearly recoverable formulas rather than fragile copied equation numbering.

5. 如果未来加入 modern DCO、injection-locked oscillator、LC VCO 或 ring-VCO PNoise simulation case studies，应把 Razavi 分类框架扩展为 comparative design table。
6. If modern DCO, injection-locked oscillator, LC VCO, or ring-VCO PNoise simulation case studies are ingested later, the Razavi classification framework should be extended into a comparative design table.

## Quality Checklist

| Check | Result |
|---|---|
| Source classified | Pass |
| Existing canonical note identified | Pass |
| Duplicate note avoided | Pass |
| Durable note update written as paragraph-level Chinese-English pairs | Pass |
| Markdown LaTeX used for formulas | Pass |
| Engineering insights added | Pass |
| Source provenance preserved | Pass |
| Source archived after successful merge | Pass |
| Legacy inbox folders left untouched | Pass |

