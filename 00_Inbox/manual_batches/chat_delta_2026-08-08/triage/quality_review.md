# Stage 2.5 Targeted Triage Quality Review

Scope: 22 high-risk records only?technical SKIPs, filename-based duplicate SKIPs, and all DEEP_CANDIDATE records. No ingest or canonical-note edits were performed.

## Findings

- Records reviewed: 22
- Classifications changed: 9
- SKIP ? FAST: 0
- SKIP ? BALANCED: 1
- SKIP ? DEEP_CANDIDATE: 1
- DEEP_CANDIDATE downgraded: 7
- Revised retained-message count: 2000
- Revised retention ratio: 2000 / 3016 = 66.31%

Matching filenames were treated only as weak initial evidence. SKIP was retained only where headings and distinctive formulas/concepts showed close content overlap. `DEEP_CANDIDATE` remains a review flag and does not authorize Deep Ingest.

## Reviewed Records

| Title | Messages | Original | Proposed | Duplicate status | Compare before merge | Likely canonical note |
|---|---:|---|---|---|---|---|
| PCIe7 Clocking LDO学习计划 | 2 | SKIP | SKIP | appears_represented_by_filename | false | `01_AnalogIC_SerDes/PLL_CDR_Clocking/pcie7_clocking_notes.md` |
| PCIe 7.0 Symbol Rate | 20 | SKIP | SKIP | appears_represented_by_filename | false | `01_AnalogIC_SerDes/PLL_CDR_Clocking/pcie7_clocking_notes.md` |
| PLL设计文档修改 | 133 | DEEP_CANDIDATE | BALANCED | uncertain | true | `01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_fundamentals.md` |
| SerDes 端接电阻讲解 | 12 | DEEP_CANDIDATE | BALANCED | uncertain | true | `01_AnalogIC_SerDes/SerDes/serdes_architecture_overview.md` |
| SerDes 终端偏置网络 | 20 | DEEP_CANDIDATE | DEEP_CANDIDATE | uncertain | true | `01_AnalogIC_SerDes/SerDes/serdes_architecture_overview.md` |
| 深度解析3.1节内容 | 11 | DEEP_CANDIDATE | DEEP_CANDIDATE | uncertain | true | `01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_phase_noise_jitter.md` |
| 3.2节设计方法详解 | 20 | DEEP_CANDIDATE | DEEP_CANDIDATE | uncertain | true | `01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_phase_noise_jitter.md` |
| ADC设计从Spec到Tapeout | 31 | DEEP_CANDIDATE | DEEP_CANDIDATE | uncertain | true | `01_AnalogIC_SerDes/ADC/adc_based_receiver.md; 01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_fundamentals.md` |
| 224G SerDes PLL分析 | 88 | DEEP_CANDIDATE | DEEP_CANDIDATE | uncertain | true | `01_AnalogIC_SerDes/Design_Methodology/224G_SerDes_PLL_Spec_Matrix_and_Example.md; 01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_phase_noise_jitter.md` |
| SerDes设计指南扩展 | 26 | DEEP_CANDIDATE | BALANCED | uncertain | true | `01_AnalogIC_SerDes/SerDes/serdes_architecture_overview.md` |
| Jitter Budget 数值分析 | 8 | DEEP_CANDIDATE | DEEP_CANDIDATE | uncertain | true | `01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_phase_noise_jitter.md` |
| BER到晶体管参数推导 | 106 | SKIP | SKIP | appears_represented_by_filename | false | `01_AnalogIC_SerDes/Design_Methodology/BER_to_Transistor_Translation.md` |
| Ring vs LC Oscillator相噪分析 | 5 | SKIP | SKIP | appears_represented_by_filename | false | `01_AnalogIC_SerDes/Design_Methodology/Ring_vs_LC_??????.md` |
| 生成Word文档技巧 | 39 | DEEP_CANDIDATE | BALANCED | uncertain | true | `01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_phase_noise_jitter.md` |
| LC Tank 能量交换详解 | 20 | DEEP_CANDIDATE | DEEP_CANDIDATE | uncertain | true | `01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_phase_noise_jitter.md` |
| LDO PSRR 高频对比 | 59 | SKIP | DEEP_CANDIDATE | uncertain | true | `01_AnalogIC_SerDes/LDO_Bandgap/ldo_psrr_notes.md` |
| C1和Rp在VCO中的作用 | 4 | SKIP | BALANCED | uncertain | true | `01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_fundamentals.md` |
| PLL相位检测反馈控制精讲 | 111 | DEEP_CANDIDATE | BALANCED | uncertain | true | `01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_fundamentals.md` |
| 第七章习题解答 | 7 | DEEP_CANDIDATE | FAST | uncertain | true | `01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_fundamentals.md` |
| PLL设计第9章精讲 | 27 | DEEP_CANDIDATE | BALANCED | uncertain | true | `01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_fundamentals.md` |
| 开环传输函数相角 | 22 | DEEP_CANDIDATE | DEEP_CANDIDATE | uncertain | true | `01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_fundamentals.md` |
| Ip/C2与spur关系 | 37 | SKIP | SKIP | appears_represented_by_filename | false | `01_AnalogIC_SerDes/PLL_CDR_Clocking/Razavi_PLL_?8.9-8.10?_Spur?????????_????.md` |

## Record-by-Record Evidence

### PCIe7 Clocking LDO学习计划

- Original classification: `SKIP`
- Proposed classification: `SKIP`
- Reason: The focused rate-to-baud/UI/Nyquist explanation is already covered at equation and worked-example level.
- Duplicate evidence: Lightweight check found explicit 128 GT/s -> 64 Gbaud -> 15.625 ps symbol UI -> 32 GHz Nyquist derivations and the 7.8125 ps warning in pcie7_clocking_notes.md.
- Likely canonical note: `01_AnalogIC_SerDes/PLL_CDR_Clocking/pcie7_clocking_notes.md`
- Compare before merge: `false`

### PCIe 7.0 Symbol Rate

- Original classification: `SKIP`
- Proposed classification: `SKIP`
- Reason: The reusable technical content and the requested expansion structure are already present in the detailed clocking note.
- Duplicate evidence: The note contains dedicated GT/s/Gbaud/UI derivations, worked examples, clocking/CDR implications, common mistakes, interview questions, and design checklists matching the delta.
- Likely canonical note: `01_AnalogIC_SerDes/PLL_CDR_Clocking/pcie7_clocking_notes.md`
- Compare before merge: `false`

### PLL设计文档修改

- Original classification: `DEEP_CANDIDATE`
- Proposed classification: `BALANCED`
- Reason: The conversation mixes useful PLL design-document requirements with extensive formatting/tool execution and an unrelated housing query, so it is not a coherent cornerstone derivation.
- Duplicate evidence: Delta preview shows repeated Word-format changes, file-copy requests, generated-artifact status, and mixed topics; no duplicate claim was made.
- Likely canonical note: `01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_fundamentals.md`
- Compare before merge: `true`

### SerDes 端接电阻讲解

- Original classification: `DEEP_CANDIDATE`
- Proposed classification: `BALANCED`
- Reason: This is a focused reusable termination tutorial with equations and references, but its scope is narrower than a cornerstone deep merge.
- Duplicate evidence: The architecture note mentions termination only briefly, while the delta contains reflection coefficient, impedance matching, bias context, and source recommendations.
- Likely canonical note: `01_AnalogIC_SerDes/SerDes/serdes_architecture_overview.md`
- Compare before merge: `true`

### SerDes 终端偏置网络

- Original classification: `DEEP_CANDIDATE`
- Proposed classification: `DEEP_CANDIDATE`
- Reason: The multi-step termination-bias interview analysis and extended lecture remain substantial enough for explicit deep-candidate review.
- Duplicate evidence: The architecture note has only brief termination coverage; the delta develops V1/V2 dividers, six-resistor variants, common-mode behavior, and interview reasoning.
- Likely canonical note: `01_AnalogIC_SerDes/SerDes/serdes_architecture_overview.md`
- Compare before merge: `true`

### 深度解析3.1节内容

- Original classification: `DEEP_CANDIDATE`
- Proposed classification: `DEEP_CANDIDATE`
- Reason: The delta contains focused ring-oscillator phase-noise derivations and a detailed TDL=T0/2 derivation request.
- Duplicate evidence: PLL fundamentals has broad VCO coverage but no lightweight evidence of the specific chapter 3.1 derivation chain.
- Likely canonical note: `01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_phase_noise_jitter.md`
- Compare before merge: `true`

### 3.2节设计方法详解

- Original classification: `DEEP_CANDIDATE`
- Proposed classification: `DEEP_CANDIDATE`
- Reason: The linked chapter 3.2-3.4 explanations request substantial derivations and cross-example synthesis.
- Duplicate evidence: No exact chapter-level coverage was established by the lightweight heading and concept checks.
- Likely canonical note: `01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_phase_noise_jitter.md`
- Compare before merge: `true`

### ADC设计从Spec到Tapeout

- Original classification: `DEEP_CANDIDATE`
- Proposed classification: `DEEP_CANDIDATE`
- Reason: The delta spans end-to-end ADC and PLL spec-to-tapeout methodology and remains a major design-workflow candidate despite the title being ADC-only.
- Duplicate evidence: ADC canonical headings are mostly receiver architecture and metrics; the delta adds project planning, testbenches, layout, PEX, signoff, and silicon bring-up across ADC and PLL.
- Likely canonical note: `01_AnalogIC_SerDes/ADC/adc_based_receiver.md; 01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_fundamentals.md`
- Compare before merge: `true`

### 224G SerDes PLL分析

- Original classification: `DEEP_CANDIDATE`
- Proposed classification: `DEEP_CANDIDATE`
- Reason: The 224G clock-generator specification, tapeout flow, and phase-noise derivations remain cornerstone technical material.
- Duplicate evidence: PLL fundamentals is broad, while the delta includes a concrete 224G/PAM4 specification, design workflow, and detailed phase-noise questions.
- Likely canonical note: `01_AnalogIC_SerDes/Design_Methodology/224G_SerDes_PLL_Spec_Matrix_and_Example.md; 01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_phase_noise_jitter.md`
- Compare before merge: `true`

### SerDes设计指南扩展

- Original classification: `DEEP_CANDIDATE`
- Proposed classification: `BALANCED`
- Reason: The conversation contains a valuable SerDes design-guide scope and review framework, but most delta content is artifact-generation instruction/status rather than the resulting 1000-page technical content.
- Duplicate evidence: Preview shows three large specification prompts and brief completion summaries; the generated guide itself is not embedded in the delta.
- Likely canonical note: `01_AnalogIC_SerDes/SerDes/serdes_architecture_overview.md`
- Compare before merge: `true`

### Jitter Budget 数值分析

- Original classification: `DEEP_CANDIDATE`
- Proposed classification: `DEEP_CANDIDATE`
- Reason: The delta catches unit, sidedness, PSD, integration, and spur-budget errors in a numerical jitter workflow.
- Duplicate evidence: The phase-noise note has integration and transfer-function sections, but the delta supplies a distinctive six-step numerical correction and error analysis.
- Likely canonical note: `01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_phase_noise_jitter.md`
- Compare before merge: `true`

### BER到晶体管参数推导

- Original classification: `SKIP`
- Proposed classification: `SKIP`
- Reason: A lightweight content check shows the canonical note already implements the same full BER-to-device translation chain and numerical structure.
- Duplicate evidence: Headings explicitly cover BER to Q/SNR, vertical and horizontal eye margins, ISI, gm, current, W/L, CTLE, comparator, ADC, CDR/PLL, driver, full numerical example, and signoff.
- Likely canonical note: `01_AnalogIC_SerDes/Design_Methodology/BER_to_Transistor_Translation.md`
- Compare before merge: `false`

### Ring vs LC Oscillator相噪分析

- Original classification: `SKIP`
- Proposed classification: `SKIP`
- Reason: The focused comparison is already represented with the same noise-source, Q, flicker, power, supply, FOM, and selection framework.
- Duplicate evidence: Lightweight search found ring/LC source paths, 1/f2 and 1/f3 regions, Rp/Q, supply sensitivity, FOM scaling, ISF/Leeson links, and topology-selection conclusions.
- Likely canonical note: `01_AnalogIC_SerDes/Design_Methodology/Ring_vs_LC_??????.md`
- Compare before merge: `false`

### 生成Word文档技巧

- Original classification: `DEEP_CANDIDATE`
- Proposed classification: `BALANCED`
- Reason: The title masks mixed content: useful PLL oscillator-noise chapter prompts plus a reusable Word-generation recipe, but most responses are document completion/status rather than embedded derivations.
- Duplicate evidence: Delta contains repeated chapter 6 document prompts, OMML/format constraints, and short artifact summaries; the generated documents are external to the delta.
- Likely canonical note: `01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_phase_noise_jitter.md`
- Compare before merge: `true`

### LC Tank 能量交换详解

- Original classification: `DEEP_CANDIDATE`
- Proposed classification: `DEEP_CANDIDATE`
- Reason: The delta gives a substantial LC-tank energy and phase-sensitivity derivation with direct physical intuition.
- Duplicate evidence: PLL fundamentals only has broad VCO headings; no lightweight evidence matched the energy-at-zero-crossing and phase-impulse derivation.
- Likely canonical note: `01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_phase_noise_jitter.md`
- Compare before merge: `true`

### LDO PSRR 高频对比

- Original classification: `SKIP`
- Proposed classification: `DEEP_CANDIDATE`
- Reason: The delta materially extends the existing PSRR note with capacitor-vs-capless segmentation, load-dependent curves, and an output-impedance interpretation.
- Duplicate evidence: The note has generic frequency/load/output-capacitor sections, but searches did not find capless comparison, ESL/self-resonance detail, 1uA-vs-100mA curve treatment, or the PSRR/output-impedance curve-shift explanation.
- Likely canonical note: `01_AnalogIC_SerDes/LDO_Bandgap/ldo_psrr_notes.md`
- Compare before merge: `true`

### C1和Rp在VCO中的作用

- Original classification: `SKIP`
- Proposed classification: `BALANCED`
- Reason: The focused C1/Rp interpretation is reusable circuit intuition and is not covered sufficiently by the broad PLL note.
- Duplicate evidence: Repository search found only a brief Rp loss reference elsewhere; it did not find the Fig. 1.15/1.17 distinction between total tank capacitance, parasitics, and fictitious parallel loss resistance.
- Likely canonical note: `01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_fundamentals.md`
- Compare before merge: `true`

### PLL相位检测反馈控制精讲

- Original classification: `DEEP_CANDIDATE`
- Proposed classification: `BALANCED`
- Reason: The requested chapter coverage is broad, but the delta mainly contains document-generation prompts and completion summaries rather than the derivations themselves.
- Duplicate evidence: Preview shows repeated chapter requests and short artifact summaries; the generated Word material is not embedded for direct knowledge merge.
- Likely canonical note: `01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_fundamentals.md`
- Compare before merge: `true`

### 第七章习题解答

- Original classification: `DEEP_CANDIDATE`
- Proposed classification: `FAST`
- Reason: Only a concise completion summary and highlights of the 21 solved problems are present; the actual derivations live in an external Word artifact.
- Duplicate evidence: The delta has one prompt and one status answer listing selected conclusions, not the 21 full solutions.
- Likely canonical note: `01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_fundamentals.md`
- Compare before merge: `true`

### PLL设计第9章精讲

- Original classification: `DEEP_CANDIDATE`
- Proposed classification: `BALANCED`
- Reason: The chapter 9/10 design-study outline and noted consistency check are reusable, but the detailed technical artifact is external and the remaining delta is figure-fix workflow.
- Duplicate evidence: Preview shows a short 21-page artifact summary, several figure repair requests, and another generation prompt rather than embedded chapter derivations.
- Likely canonical note: `01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_fundamentals.md`
- Compare before merge: `true`

### 开环传输函数相角

- Original classification: `DEEP_CANDIDATE`
- Proposed classification: `DEEP_CANDIDATE`
- Reason: The delta contains actual open-loop phase, phase-margin, Nyquist-path, and trajectory derivations rather than artifact-only status.
- Duplicate evidence: PLL fundamentals has stability and open-loop sections, but the delta provides a focused multi-method derivation and Nyquist construction example requiring compare-before-merge.
- Likely canonical note: `01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_fundamentals.md`
- Compare before merge: `true`

### Ip/C2与spur关系

- Original classification: `SKIP`
- Proposed classification: `SKIP`
- Reason: The existing dedicated note reproduces the same four-question framework and distinctive equations at detailed section level.
- Duplicate evidence: The note explicitly covers Ip/C2 spur scaling, beta/2 sideband amplitude, exact and approximate D(s), all major PLL noise transfer functions, PSD summation, and common errors.
- Likely canonical note: `01_AnalogIC_SerDes/PLL_CDR_Clocking/Razavi_PLL_?8.9-8.10?_Spur?????????_????.md`
- Compare before merge: `false`

## Corrected Classification Totals

- SKIP: 67
- FAST: 28
- BALANCED: 37
- DEEP_CANDIDATE: 9

The original `triage_inventory.jsonl` remains authoritative as the unmodified Stage 2 artifact; `triage_inventory_corrected.jsonl` is the Stage 2.5 corrected view.
