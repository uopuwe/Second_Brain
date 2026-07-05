---
title: "Balanced Ingest Report - Digital Bang-Bang and Fractional-N ADPLL Sources"
date: 2026-07-05
mode: "Balanced Ingest"
status: "completed"
---

# Balanced Ingest Report - Digital Bang-Bang and Fractional-N ADPLL Sources

## 1. Processed Files

| Source | Type | Classification | Archive path |
|---|---|---|---|
| `00_Inbox/incoming/articles/eetop.cn_Theory and Implementation of Digital Bang-Bang Frequency Synthesizers for High S.pdf` | Dissertation PDF | Digital bang-bang PLL, BBPD, BBPLL nonlinear dynamics, CDR-related clock synthesis | `90_Archive/processed/2026/articles/digital_bang_bang_frequency_synthesizers_da_dalt_2007/` |
| `00_Inbox/incoming/papers/A 529-uW Fractional-N All-Digital PLL.pdf` | IEEE paper PDF | Fractional-N ADPLL, DTC-assisted ADPLL, hybrid TDC, TDC gain calibration, inverse-class-F DCO | `90_Archive/processed/2026/papers/chen_529uw_fractional_n_adpll_2022/` |

## 2. Updated Canonical Notes

| Note | Update |
|---|---|
| `01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_fractional_n_digital.md` | Added Balanced Ingest section for Da Dalt BBPLL nonlinear dynamics and Chen et al. low-power fractional-N ADPLL. Promoted BBPLL nonlinear map, latency jitter relationships, BPD gain dependence, hybrid TDC calibration equations, snapshot offset timing, and DTC mismatch/power/spur scaling. |
| `01_AnalogIC_SerDes/PLL_CDR_Clocking/cdr_fundamentals.md` | Added CDR-facing BBPLL lessons from Da Dalt: low-noise limit-cycle regime versus high-noise linearized regime, loop-latency warning, and BBPD gain review questions. |
| `01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_phase_noise_jitter.md` | Added inverse-class-F DCO case-study insight from Chen et al., including harmonic-alignment condition and effective-ISF flicker-upconversion interpretation. |
| `01_AnalogIC_SerDes/Papers_Books/core_serdes_papers.md` | Added P7/P8 source-index entries for Da Dalt and Chen et al. |

## 3. New Notes

No new notes were created.

Both sources had existing canonical destinations:

- [[pll_fractional_n_digital]]
- [[cdr_fundamentals]]
- [[pll_phase_noise_jitter]]

## 4. Formulas Promoted

| Formula / relationship | Destination | Use |
|---|---|---|
| $\tau_{k+1}=\tau_k+x_0-R\psi_{k-D}-\operatorname{sgn}(\tau_{k-D})$ | `pll_fractional_n_digital.md` | Normalized nonlinear Type-II BBPLL map. |
| $\psi_{k+1}=\psi_k+\operatorname{sgn}(\tau_{k+1})$ | `pll_fractional_n_digital.md` | BBPLL integral-state update. |
| $\tau_{k+1}=\tau_k+x_0-\operatorname{sgn}(\tau_{k-D})$ | `pll_fractional_n_digital.md` | First-order BBPLL map. |
| $\tau_{pp}=1+2D$ | `pll_fractional_n_digital.md`, `cdr_fundamentals.md` | Low-noise latency-driven BBPLL jitter warning. |
| $\sigma_\tau^2=(1+2D)^2/12$ for $D\ne0$ | `pll_fractional_n_digital.md` | First-order BBPLL jitter variance estimate. |
| $\tau_{pp}=2(1+D)$ | `pll_fractional_n_digital.md`, `cdr_fundamentals.md` | Nonzero-offset worst-case BBPLL jitter estimate. |
| $12\tau_s=T_v$, $8\tau_s=10\tau_f$, $\tau_{res}=T_v/60$ | `pll_fractional_n_digital.md` | Hybrid TDC gain calibration target. |
| $t_{dx}=T_v/2+t_{c2q}+t_{d2f}-t_{d2s}$ | `pll_fractional_n_digital.md` | Snapshot/TDC offset delay alignment. |
| $16\xi^2+(100k^2-68)\xi+16=0$ | `pll_phase_noise_jitter.md` | Inverse-class-F DCO harmonic-alignment condition. |

## 5. Engineering Insights Added

中文：Da Dalt source 的核心 insight 是 BBPLL 不能默认按 linear PLL 处理。低噪声时它是 nonlinear orbit / limit-cycle problem；高噪声时才更适合统计线性化。loop latency 对 deterministic jitter 的影响非常直接，因此 BB-CDR/BBPLL 设计必须把 decision latency、digital filtering latency 和 phase-actuator latency 当作一等设计参数。

English: The core insight from the Da Dalt source is that a BBPLL should not be treated by default as a linear PLL. Under low-noise conditions it is a nonlinear orbit / limit-cycle problem; under high-noise conditions statistical linearization becomes more appropriate. Loop latency has a direct impact on deterministic jitter, so BB-CDR/BBPLL design must treat decision latency, digital filtering latency, and phase-actuator latency as first-class design parameters.

中文：Chen et al. source 的核心 insight 是 low-power ADPLL 的难点不只是降低电流。TDC range、out-of-range behavior、TDC gain calibration、DTC mismatch spur、snapshot timing 和 DCO waveform shaping 都会互相牵制。TDC gain 漂移会改变实际 loop bandwidth；DTC mismatch 通过 fractional spur 暴露出来；inverse-class-F DCO 的 FoM 还取决于 harmonic alignment 对 PVT/mismatch 的鲁棒性。

English: The core insight from the Chen et al. source is that low-power ADPLL design is not just reducing current. TDC range, out-of-range behavior, TDC gain calibration, DTC mismatch spur, snapshot timing, and DCO waveform shaping constrain one another. TDC gain drift changes real loop bandwidth; DTC mismatch appears as fractional spur; inverse-class-F DCO FoM also depends on harmonic-alignment robustness against PVT and mismatch.

## 6. Archive Actions

| Action                            | Result                                                                                      |
| --------------------------------- | ------------------------------------------------------------------------------------------- |
| Created article archive directory | `90_Archive/processed/2026/articles/digital_bang_bang_frequency_synthesizers_da_dalt_2007/` |
| Created paper archive directory   | `90_Archive/processed/2026/papers/chen_529uw_fractional_n_adpll_2022/`                      |
| Moved Da Dalt PDF                 | Completed                                                                                   |
| Moved Chen et al. PDF             | Completed                                                                                   |
| Legacy folders touched            | None                                                                                        |

## 7. Quality Evaluation

| Area                      | Result                                                                                   |
| ------------------------- | ---------------------------------------------------------------------------------------- |
| Canonical-note rule       | Passed. No duplicate notes were created.                                                 |
| Bilingual durable writing | Passed for newly added explanatory paragraphs.                                           |
| Formula style             | Passed with symbol explanations and validity cautions.                                   |
| Provenance                | Passed. Source provenance added to destination notes and source index.                   |
| Indexing                  | Passed. `core_serdes_papers.md` updated; master index did not require structural change. |
| Knowledge evolution       | Existing canonical notes remained active; source PDFs moved to archive.                  |
| Continuous improvement    | Added source-index entries and cross-links where useful; avoided broad rewrites.         |

## 8. Manual Review Items

- Da Dalt is a dissertation-length source. This Balanced Ingest promoted selected high-value BBPLL ideas and formulas, not a full dissertation extraction.
- Chen et al. is a BLE/IoT-oriented ADPLL paper. Its measured jitter, spur, power, and FoM are not SerDes or PCIe targets.
- The BBPLL stochastic BPD gain derivation is deep enough to justify a future Deep Ingest if bang-bang CDR becomes a near-term design focus.
- The inverse-class-F DCO harmonic-alignment equations should be rechecked against the paper figures before using them for transistor-level design.
- Existing PCIe 7.0 TODO/spec-verification markers in `pll_phase_noise_jitter.md` remain intentionally unresolved.

## 9. Research Roadmap Impact

No new standalone roadmap item was created. The sources strengthen the existing PLL/CDR study direction:

- BBPLL / BB-CDR nonlinear dynamics.
- DTC-assisted fractional-N ADPLL design.
- TDC gain calibration and digital loop coefficient robustness.
- Waveform-shaped DCO phase-noise robustness.

