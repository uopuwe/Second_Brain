---
title: "Deep Ingest Report - Rhee and Yu Phase-Locked Loops"
date: 2026-07-05
mode: "Deep Ingest"
source_type: "Book PDF"
status: "completed"
---

# Deep Ingest Report - Rhee and Yu Phase-Locked Loops

## 1. Source Processed

| Field | Value |
|---|---|
| Source file | `00_Inbox/incoming/books/Phase-Locked Loops - Woogeun Rhee.pdf` |
| Archived file | `90_Archive/processed/2026/books/phase_locked_loops_rhee_yu_2024/Phase-Locked Loops - Woogeun Rhee.pdf` |
| Title | *Phase-Locked Loops: System Perspectives and Circuit Design Aspects* |
| Authors | Woogeun Rhee and Zhiping Yu |
| Publisher | Wiley / IEEE Press |
| Year | 2024 |
| Page count | 383 pages |
| Ingest mode | Deep Ingest, explicitly requested by the user |
| Classification | PLL, CPPLL, PFD, charge pump, phase noise, spur, fractional-N PLL, DSM, ADPLL/DPLL, BBPLL, HPLL, CDR |

## 2. Processing Summary

中文：本次 Deep Ingest 将 Rhee 和 Yu 的 PLL textbook 作为 long-term canonical reference 处理。没有创建重复 handbook，而是按照已有知识架构把 reusable knowledge 合并到 PLL/CDR canonical notes，并补齐两个缺失但独立的 canonical notes：PFD/charge pump 与 fractional-N/digital PLL。

English: This Deep Ingest treated Rhee and Yu's PLL textbook as a long-term canonical reference. It did not create a duplicate handbook; reusable knowledge was merged into existing PLL/CDR canonical notes, and two missing but independent canonical notes were added: PFD/charge pump and fractional-N/digital PLL.

## 3. Updated Canonical Notes

| Note | Action | Knowledge promoted |
|---|---|---|
| `01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_fundamentals.md` | Updated | Linear PLL model, closed-loop and error transfer functions, Type-I/Type-II loop parameters, CPPLL sizing equations, continuous-time approximation boundary, loop-delay caution, Deep Ingest review checklist |
| `01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_phase_noise_jitter.md` | Updated | Narrowband FM spur model, spur-to-deterministic-jitter conversion, phase-noise integration convention, divider/multiplier spur scaling, reference-spur suppression versus phase-margin tradeoff, optimum bandwidth as source-crossover problem |
| `01_AnalogIC_SerDes/PLL_CDR_Clocking/cdr_fundamentals.md` | Updated | CDR JGEN/JTRAN/JTOL metric framing, Type-II CDR jitter-transfer equations, jitter peaking estimate, jitter tolerance transfer, Hogge and Alexander detector tradeoffs, BBPD gain dependence, acquisition-path caution, DLL-assisted CDR intuition |
| `01_AnalogIC_SerDes/Papers_Books/core_serdes_papers.md` | Updated | Added Rhee and Yu as cornerstone ingested book source and citation anchor |
| `01_AnalogIC_SerDes/analog_ic_serdes_master_index.md` | Updated | Added new active PLL/CDR canonical notes and expanded source-backed PLL ingest summary |

## 4. New Notes Created

| New note | Reason |
|---|---|
| `01_AnalogIC_SerDes/PLL_CDR_Clocking/pfd_charge_pump_notes.md` | Existing PLL fundamentals mentioned PFD/CP, but there was no dedicated canonical note for detector taxonomy, CP gain, dead zone, reset delay, spur/leakage scaling, CP topology, and implementation checklist. Creating this note prevents future duplicate PFD/CP notes. |
| `01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_fractional_n_digital.md` | The repository lacked a canonical destination for fractional-N PLL, DSM, DTC/DAC compensation, DPLL, BBPLL, and HPLL material. Creating this note prevents future duplicate ADPLL/fractional-N notes. |

## 5. Formulas and Derivations Promoted

| Topic | Formula / model promoted | Destination |
|---|---|---|
| Linear PLL open-loop model | $G(s)=K_dK_vF(s)/s$ | `pll_fundamentals.md` |
| Closed-loop transfer | $H(s)=G(s)/(1+G(s))$ | `pll_fundamentals.md` |
| Error transfer | $H_e(s)=1/(1+G(s))$ | `pll_fundamentals.md` |
| Type-I loop | $H(s)=K/(s+K)$ | `pll_fundamentals.md` |
| Type-II second-order loop | $\omega_n=\sqrt{K\omega_z}$, $\zeta=(1/2)(\omega_n/\omega_z)$ | `pll_fundamentals.md` |
| CP gain | $K'_d=I_{CP}/(2\pi)$ | `pfd_charge_pump_notes.md` |
| CPPLL open-loop model | $G(s)=I_{CP}K_v(1+sR_1C_1)/(2\pi C_1s^2)$ | `pll_fundamentals.md`, `pfd_charge_pump_notes.md` |
| CPPLL first-pass sizing | $\omega_u$, $\omega_z$, $\omega_n$, $\zeta$ relationships | `pll_fundamentals.md`, `pfd_charge_pump_notes.md` |
| Leakage spur scaling | $\theta_e=2\pi I_{leak}/I_{CP}$ and leakage-spur estimate | `pfd_charge_pump_notes.md` |
| Narrowband FM spur | $P_{spur}=20\log_{10}(m/2)$ | `pll_phase_noise_jitter.md` |
| Spur to deterministic jitter | $DJ=m/\pi\;\mathrm{UI}$ | `pll_phase_noise_jitter.md`, `pfd_charge_pump_notes.md` |
| Phase-noise integration | $\Delta\theta_n=\sqrt{\int_a^b2\mathcal{L}(f_m)\,df_m}$ | `pll_phase_noise_jitter.md` |
| DSM first/second/Lth-order shaping | Difference-noise and OSR scaling formulas | `pll_fractional_n_digital.md` |
| DTC charge compensation | $Q_n[k]=I_{CP}T_{ref}\sum e[m]$ | `pll_fractional_n_digital.md` |
| TDC/DCO DPLL model | $K_{td}=1/t_{res}$, $K_{vt}=f_{res}/f_v^2$, z-domain loop model | `pll_fractional_n_digital.md` |
| BBPLL limit-cycle jitter | $\Delta t_{pp}=2(1+D)\alpha NK_{vt}$ | `pll_fractional_n_digital.md` |
| BBPD statistical gain | $K_{td}=\eta/\sigma_t$, $\eta=\sqrt{2/\pi}$ | `pll_fractional_n_digital.md` |
| CDR jitter transfer | $H_{JTRAN}(s)$ second-order model | `cdr_fundamentals.md` |
| CDR jitter tolerance | $H_{JTOL}(s)=0.5/H_{JTRACK}(s)$ | `cdr_fundamentals.md` |
| DLL-assisted CDR | D/PLL jitter-transfer and pole intuition | `cdr_fundamentals.md` |

## 6. Index and MOC Updates

| File | Update |
|---|---|
| `01_AnalogIC_SerDes/analog_ic_serdes_master_index.md` | Added `pfd_charge_pump_notes.md` and `pll_fractional_n_digital.md` to active PLL/CDR knowledge routing; updated 2026-07-05 source-backed PLL summary. |
| `01_AnalogIC_SerDes/Papers_Books/core_serdes_papers.md` | Added B2 cornerstone book entry for Rhee and Yu with promoted notes and archive path. |

No separate MOC file was created because the existing repository architecture routes PLL/CDR material through the master index and `core_serdes_papers.md`.

## 7. Archive Actions

| Action | Result |
|---|---|
| Created archive directory | `90_Archive/processed/2026/books/phase_locked_loops_rhee_yu_2024/` |
| Moved source PDF | From `00_Inbox/incoming/books/` to archive directory |
| Created report | `ingest_report_2026-07-05.md` in the archive directory |
| Legacy inbox folders touched | None |

## 8. Manual Review Items

- The source is a copyrighted book; durable notes were written as summarized engineering knowledge and formulas, not copied textbook prose.
- Formulas were promoted as engineering models. They should not be treated as PCIe 7.0 compliance limits or project signoff masks.
- The `-40 dBc` spur warning line is a useful isolated-spur-to-DJ sanity check, not a universal pass/fail requirement.
- DSM quantization-noise formulas assume idealized quantization statistics. Real fractional-N designs require idle-tone, word-length, DTC/CP nonlinearity, and integer-boundary spur simulation.
- DPLL and BBPLL formulas depend on coefficient scaling conventions. Future project notes should record units for $\alpha$, $\beta$, $K_{tdc}$, $K_{dco}$, $N$, and $T_{ref}$ explicitly.
- CDR formulas are useful for architecture intuition, but PAM4/ADC-based receiver signoff must include equalizer residue, transition density, slicer/ADC noise, adaptation loops, FEC/BER targets, and applicable PCIe compliance procedures.

## 9. Quality Checks Performed

- Confirmed normal ingest target was `00_Inbox/incoming/`.
- Confirmed only one real source file was present under incoming.
- Confirmed no legacy ChatGPT export or conversation-processing folders were scanned or modified.
- Confirmed no duplicate handbook was created.
- Confirmed new notes are canonical topic notes rather than duplicate summaries.
- Confirmed Obsidian links added in modified files resolve to existing Markdown note basenames.
- Confirmed source provenance was added to updated notes and source index.
- Confirmed source PDF was archived after successful ingestion.

## 10. Future Knowledge Growth

中文：未来如果继续 ingest PLL/CDR 资料，应优先补充 modern SerDes-specific clocking papers、PCIe public clocking references、PAM4 baud-rate CDR papers、ADPLL/DPLL measured silicon papers、fractional-N spur case studies、PSS/PNoise/PXF simulation recipes 和 lab debug notes。Rhee 和 Yu 应作为 system-level textbook anchor，而不是替代 modern silicon papers 或 official standards。

English: Future PLL/CDR ingests should prioritize modern SerDes-specific clocking papers, public PCIe clocking references, PAM4 baud-rate CDR papers, measured ADPLL/DPLL silicon papers, fractional-N spur case studies, PSS/PNoise/PXF simulation recipes, and lab-debug notes. Rhee and Yu should serve as a system-level textbook anchor, not as a replacement for modern silicon papers or official standards.
