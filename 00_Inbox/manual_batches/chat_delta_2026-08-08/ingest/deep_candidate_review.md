# Stage 3 Deep Candidate Compare-Before-Merge Review

Generated: 2026-08-08

No item below was merged. Comparison was intentionally lightweight: relevant headings and sections plus a few distinctive concepts or formulas. `DEEP_APPROVE` means that a later explicitly approved deep ingest appears valuable; it is not current authorization.

## 1. SerDes 终端偏置网络

- Conversation ID: `6a4aa78a-beb0-83ea-874f-6d53a24afa40`
- Likely canonical note: `01_AnalogIC_SerDes/SerDes/serdes_architecture_overview.md`, near RX termination/common-mode bias
- Actual novelty found: topology-specific V1/V2 bias analysis, alternate resistor/inverter networks, and reasoning about how termination, common-mode generation, and receiver input behavior interact.
- Overlap with existing note: the note now contains only the basic differential/Thevenin termination checkpoint; it does not contain the topology reconstruction or node-voltage analysis.
- Recommended action: **DEEP_APPROVE**
- Reason: the material can improve receiver-front-end understanding, but the conversation contains uncertain diagram reconstruction and edition-specific claims that require schematic/source verification.
- Estimated merge scope: medium; one focused topology section with verified diagrams/equations and explicit assumptions.

## 2. 深度解析3.1节内容

- Conversation ID: `6a52a064-2a64-83ea-b37b-2bc58be2b460`
- Likely canonical note: `01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_phase_noise_jitter.md`, oscillator-noise/ISF area
- Actual novelty found: explicit separation of driven open-loop delay-line phase error from closed-loop oscillator phase accumulation, including the $T_{DL}=T_0/2$ time-domain derivation.
- Overlap with existing note: extensive oscillator phase-noise, ISF, $1/f^2$, and $1/f^3$ material already exists; the delay-line-versus-closed-loop bridge is less explicit.
- Recommended action: **BALANCED_LATER**
- Reason: novelty is narrow and useful but does not justify another deep chapter-sized merge.
- Estimated merge scope: small; one verified explanatory subsection and one compact derivation.

## 3. 3.2节设计方法详解

- Conversation ID: `6a52c126-9540-83ea-8b0c-99d34b1c4b43`
- Likely canonical note: `01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_phase_noise_jitter.md`, with possible linkage to `pll_fundamentals.md`
- Actual novelty found: a unified comparison of ring-oscillator frequency reduction by stage count, sizing, capacitance, and supply/current changes, emphasizing that equal frequency or lower phase-noise number does not imply equal design quality.
- Overlap with existing note: broad power/phase-noise tradeoffs and oscillator noise physics already exist, but the comparative preliminary-design workflow is not organized around these four levers.
- Recommended action: **DEEP_APPROVE**
- Reason: a verified, source-aligned comparison could add reusable oscillator-design methodology beyond a formula dump.
- Estimated merge scope: medium to large; comparative table, normalized metrics, and selected derivations only.

## 4. ADC设计从Spec到Tapeout

- Conversation ID: `6a5695fc-6e04-83ea-9984-152017761ba2`
- Likely canonical notes: `01_AnalogIC_SerDes/ADC/adc_based_receiver.md` and `01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_fundamentals.md`
- Actual novelty found: an end-to-end specification-to-signoff workflow spanning requirement clarification, compliance matrices, architecture, testbenches, layout/PEX, signoff, and silicon feedback; the extract also mixes PLL content and document-rendering repairs.
- Overlap with existing note: existing notes are architecture- and block-focused; they do not present a complete ADC project-gate workflow. A substantial portion of this delta is artifact formatting/status rather than knowledge.
- Recommended action: **DEEP_APPROVE**
- Reason: the reusable methodology has high potential, but it must be separated from PLL material, formatting chatter, and artifact completion messages before any merge.
- Estimated merge scope: large; likely a dedicated design-methodology note plus only small links into ADC/PLL notes.

## 5. 224G SerDes PLL分析

- Conversation ID: `6a56baa8-8a8c-83ea-8a21-a6280c60c276`
- Likely canonical notes: `01_AnalogIC_SerDes/Design_Methodology/224G_SerDes_PLL_Spec_Matrix_and_Example.md` and `01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_phase_noise_jitter.md`
- Actual novelty found: possible project-priority sequencing and a few focused phase-noise scaling clarifications; many delta messages are Word generation, formatting, download, or completion status.
- Overlap with existing note: very high. The 224G canonical document already covers spec matrices, endpoint and filtered jitter, block allocation, phase-noise masks, module parameters, PVT, verification, and signoff in depth.
- Recommended action: **BALANCED_LATER**
- Reason: compare individual concepts against the existing long-form note; do not ingest the conversation or generated-artifact status wholesale.
- Estimated merge scope: small to medium; only verified missing priority gates or corrected formulas.

## 6. Jitter Budget 数值分析

- Conversation ID: `6a5ab9ec-e824-83ea-aee0-69f52f6a06ca`
- Likely canonical note: `01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_phase_noise_jitter.md`, numerical integration and jitter combination sections
- Actual novelty found: correction-oriented worked reasoning for dBc/Hz units, one-sided/two-sided PSD consistency, $\sqrt{2}$ errors, and an RSS arithmetic correction.
- Overlap with existing note: high; the canonical note already documents phase-noise integration convention, numerical integration, and mixed jitter budgets.
- Recommended action: **BALANCED_LATER**
- Reason: the value is primarily as a compact error-checking example, not a new deep framework.
- Estimated merge scope: small; one corrected example or red-flag box after independently verifying every number.

## 7. LC Tank 能量交换详解

- Conversation ID: `6a5fb697-1d1c-83ea-93c7-1211019bba6d`
- Likely canonical note: `01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_phase_noise_jitter.md`, oscillator/ISF section
- Actual novelty found: four-time-point LC energy exchange, state-plane interpretation, and a bridge from instantaneous energy/sensitivity to ISF and phase perturbation.
- Overlap with existing note: ISF and oscillator-noise sections are extensive, but the elementary energy trajectory is not used as the explanatory bridge.
- Recommended action: **DEEP_APPROVE**
- Reason: it could materially improve pedagogical continuity if checked against a primary oscillator source and kept separate from artifact-edit status.
- Estimated merge scope: medium; one illustrated conceptual section and selected equations.

## 8. LDO PSRR 高频对比

- Conversation ID: `6a617bbd-d714-83ea-8fbb-463691f07371`
- Likely canonical note: `01_AnalogIC_SerDes/LDO_Bandgap/ldo_psrr_notes.md`
- Actual novelty found: cap versus capless load dependence, distinction between feedthrough admittance and closed-loop output impedance, conditions for vertical curve shifts versus shape changes, dominant-pole/ESR-zero reasoning, and competing full-load effects.
- Overlap with existing note: the canonical note covers general PSRR mechanisms but does not fully organize these load-dependent high-frequency comparisons or curve-interpretation cautions.
- Recommended action: **DEEP_APPROVE**
- Reason: the delta is substantial and potentially useful, but several generated plots and simplified assumptions need model-level verification before becoming canonical.
- Estimated merge scope: large; a structured load/capacitance comparison with equations, assumptions, and verified plots.

## 9. 开环传输函数相角

- Conversation ID: `6a6e0313-043c-83ea-a96e-c98e23275cbc`
- Likely canonical note: `01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_fundamentals.md`, loop stability area
- Actual novelty found: stepwise construction of open-loop phase from each factor, explicit $s=j\omega$ mapping, Nyquist trajectory parameterization, sample points, and argument-principle interpretation.
- Overlap with existing note: the fundamentals note has stability, damping, and loop-transfer material but not a worked Nyquist construction.
- Recommended action: **DEEP_APPROVE**
- Reason: the material is reusable control-theory scaffolding, but a deep merge should verify contour orientation, pole-on-axis handling, sign conventions, and PLL-specific assumptions.
- Estimated merge scope: medium; one control-theory subsection with a worked example and caveats.

## Recommendation Totals

| Recommended action | Count |
|---|---:|
| SKIP | 0 |
| BALANCED_LATER | 3 |
| DEEP_APPROVE | 6 |

These recommendations preserve the deep queue without changing any canonical note during this review.

