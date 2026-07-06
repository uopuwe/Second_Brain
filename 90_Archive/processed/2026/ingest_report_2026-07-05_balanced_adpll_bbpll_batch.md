---
title: "Balanced Ingest Report - ADPLL and Bang-Bang PLL/CDR Batch"
date: 2026-07-05
mode: "Balanced Ingest"
source_root: "00_Inbox/incoming/"
status: "complete"
---

# Balanced Ingest Report - ADPLL and Bang-Bang PLL/CDR Batch

## Summary

Processed six incoming sources under `00_Inbox/incoming/` using Balanced Ingest. The batch focused on ADPLL/DCO/TDC architecture, digital bang-bang PLL nonlinear dynamics, bang-bang CDR design equations, CPPLL review checklists, and duplicate PLL architecture review handling.

Durable note updates were written as paragraph-level Chinese-English bilingual pairs where new technical content was added.

## Processed Files

| Source file | Classification | Outcome |
|---|---|---|
| `00_Inbox/incoming/books/All-Digital Frequency Synthesizer in Deep-Submicron CMOS-Wiley2006.pdf` | Book; ADPLL, DCO, TDC, phase-domain frequency synthesis | Balanced extraction promoted into [[adpll_notes]] and source index |
| `00_Inbox/incoming/papers/2278stas All-Digital TX Frequency Synthesizer and.pdf` | IEEE JSSC paper; ADPLL Bluetooth synthesizer and discrete-time receiver | Balanced extraction promoted into [[adpll_notes]] and source index |
| `00_Inbox/incoming/papers/A design-oriented study of the nonlinear dynamics of digital bang-bang PLLs.pdf` | IEEE TCAS-I paper; nonlinear digital BBPLL dynamics | Promoted into [[pll_fractional_n_digital]], [[cdr_fundamentals]], and source index |
| `00_Inbox/incoming/papers/Designing Bang-Bang PLLs for Clock and Data Recovery in Serial Data Transmission.pdf` | CDR paper; bang-bang PLL/CDR design equations | Promoted into [[cdr_fundamentals]] and source index |
| `00_Inbox/incoming/papers/eetop.cn_CMOS analog and mixed-signal phase-locked loops_ An overview.pdf` | Review paper; AMS/CPPLL overview | Review-level checklist promoted into [[pfd_charge_pump_notes]] and source index |
| `00_Inbox/incoming/papers/Exploring_the_Landscape_of_Phase-Locked_Loop_Architectures A Comprehensive Review.pdf` | IEEE Access review; PLL architecture taxonomy | Detected as duplicate of already represented source; archived with no new durable note update |

## Updated Canonical Notes

| Note | Update |
|---|---|
| [[adpll_notes]] | Added Staszewski/Balsara phase-domain ADPLL source section covering accumulator-based phase comparison, DCO fractional dithering, DCO update timing, TDC retiming, and TDC gain normalization |
| [[cdr_fundamentals]] | Added bang-bang CDR design equations for phase-step update, lock range, hunting jitter, duty-cycle/frequency-offset relation, slope overload, and second-order bang-bang review |
| [[pll_fractional_n_digital]] | Added Da Dalt 2005 paper as peer-reviewed condensed source anchor for nonlinear BBPLL dynamics |
| [[pfd_charge_pump_notes]] | Added AMS CPPLL review checklist covering CP mismatch, loop-filter ripple, bandwidth/settling tradeoff, fractional-N PFD/CP nonlinearity, and divider-noise caution |
| [[core_serdes_papers]] | Added B3 and P9-P13 source anchors for the processed batch |
| [[analog_ic_serdes_master_index]] | Updated PLL/CDR source-backed update summary to include phase-domain ADPLL and bang-bang PLL/CDR nonlinear dynamics |

## New Notes

No new technical notes were created. Existing canonical notes were used.

## Formulas and Derivations Promoted

| Formula | Destination | Use |
|---|---|---|
| $\Delta f_{\mathrm{eff}}\approx \Delta f_{\mathrm{DCO}}/2^B$ | [[adpll_notes]] | First-order DCO fractional dithering resolution estimate |
| $\theta_d(t_n)=\theta_d(0)+2\pi\delta f\,t_n+\phi(t_n)$ | [[cdr_fundamentals]] | First-order bang-bang CDR/PLL input phase model |
| $\theta_v(t_{n+1})=\theta_v(t_n)+\epsilon_n\theta_{bb}$ | [[cdr_fundamentals]] | Bang-bang phase actuator update model |
| $\epsilon_n=\operatorname{sgn}[\theta_d(t_n)-\theta_v(t_n)]$ | [[cdr_fundamentals]] | Binary early/late detector model |
| $\theta_{bb}=2\pi f_{bb}/f_{nom}$ | [[cdr_fundamentals]] | Phase step from bang-bang update frequency |
| $|\delta f|<f_{bb}$ | [[cdr_fundamentals]] | Simplified lock-range criterion |
| $J_{pp}=4\pi f_{bb}/f_{nom}$ | [[cdr_fundamentals]] | Hunting jitter estimate |
| $C=1/2+\delta f/(2f_{bb})$ | [[cdr_fundamentals]] | Early/late duty-cycle relation under frequency offset |
| $A_{\max}\approx f_{bb}/f_{mod}$ | [[cdr_fundamentals]] | Slope-overload intuition for sinusoidal jitter |
| $\xi=\Delta\theta_{\mathrm{proportional}}/\Delta\theta_{\mathrm{integral}}$ | [[cdr_fundamentals]] | Second-order bang-bang loop review variable |

## Index and MOC Updates

- Updated `01_AnalogIC_SerDes/Papers_Books/core_serdes_papers.md`.
- Updated `01_AnalogIC_SerDes/analog_ic_serdes_master_index.md`.
- No separate MOC update was required because the affected topics already resolve through the master index and PLL/CDR canonical notes.

## Archive Actions

| Source | Archive destination |
|---|---|
| All-Digital Frequency Synthesizer book PDF | `90_Archive/processed/2026/books/all_digital_frequency_synthesizer_staszewski_balsara_2006/` |
| Staszewski JSSC Bluetooth ADPLL PDF | `90_Archive/processed/2026/papers/staszewski_all_digital_tx_synthesizer_bluetooth_2004/` |
| Da Dalt 2005 BBPLL nonlinear dynamics PDF | `90_Archive/processed/2026/papers/da_dalt_nonlinear_dynamics_bbpll_2005/` |
| Bang-bang CDR design PDF | `90_Archive/processed/2026/papers/bang_bang_plls_cdr_serial_data_transmission/` |
| Zhang 2020 AMS PLL overview PDF | `90_Archive/processed/2026/papers/zhang_cmos_ams_pll_overview_2020/` |
| Dutta 2024 PLL architecture review duplicate PDF | `90_Archive/processed/2026/papers/duplicate_dutta_pll_architecture_review_2024/` |

## Manual Review Items

- The Staszewski/Balsara book was processed at Balanced level only. If ADPLL becomes a near-term design or interview focus, run a future Deep Ingest specifically on the DCO, phase-domain modeling, frequency synthesis, and BIST chapters.
- The "Designing Bang-Bang PLLs for Clock and Data Recovery in Serial Data Transmission" PDF did not yield confident author metadata during Balanced Ingest. Keep title-only citation until manually verified.
- Bluetooth ADPLL performance numbers were not promoted as SerDes/PCIe targets. They were used only for architecture and implementation intuition.
- Dutta 2024 was treated as a duplicate broad taxonomy source and archived without additional note edits.

## Verification

- Normal ingest target remained `00_Inbox/incoming/`.
- Legacy ChatGPT export and conversation-processing folders were not scanned, moved, archived, or modified.
- No duplicate canonical notes were created.
- Durable technical additions were merged into existing canonical notes.
