# Ingest Report - Hajimiri ISF and Gao Sub-Sampling PLL Sources

## Run Summary

| Item | Value |
|---|---|
| Date | 2026-07-05 |
| Mode | Balanced Ingest |
| Ingest target | `00_Inbox/incoming/` |
| Source lane | `00_Inbox/incoming/papers/` |
| Archive destination | `90_Archive/processed/2026/papers/hajimiri_gao_pll_sources_2026-07-05/` |
| Canonical-note policy | Merge into existing canonical notes; do not create duplicate notes |
| Bilingual-note policy | Durable explanatory additions were written as paragraph-level Chinese-English bilingual pairs |

## Processed Files

| Source file | Source type | Classification | Canonical destination | Status |
|---|---|---|---|---|
| `0179haji.pdf` | IEEE JSSC paper | Oscillator phase-noise theory, ISF, flicker upconversion, waveform symmetry | `01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_phase_noise_jitter.md` | Processed and archived |
| `A_Low_Noise_Sub-Sampling_PLL_in_Which_Divider_Noise_Is_Eliminated_and_PD-CP_Noise_Is_not_multiplied_by_N^2.pdf` | IEEE JSSC paper | Sub-sampling PLL, divider-noise elimination, PD/CP in-band noise scaling, reference-buffer limit | `01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_phase_noise_jitter.md` | Processed and archived |

## Updated Canonical Notes

| Note | Update |
|---|---|
| `01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_phase_noise_jitter.md` | Added Section 26 covering ISF theory, white-noise and flicker-upconversion formulas, phase-noise corner intuition, sub-sampling PLL CP-noise scaling, jitter integration, reference-buffer noise, and design-review additions. |
| `01_AnalogIC_SerDes/Papers_Books/core_serdes_papers.md` | Added source anchors P5 and P6 under the ingested PLL / oscillator source section. |
| `01_AnalogIC_SerDes/analog_ic_serdes_master_index.md` | Updated the PLL source-backed update line to include oscillator ISF theory and sub-sampling PLL in-band noise scaling. |

## New Notes

No new technical notes were created. Existing canonical notes were sufficient:

- `pll_phase_noise_jitter.md`
- `core_serdes_papers.md`
- `analog_ic_serdes_master_index.md`

## Formulas Promoted

The following formulas were promoted into canonical notes in Markdown LaTeX form:

```latex
h_{\phi}(t,\tau)=\frac{\Gamma(\omega_0\tau)}{q_{\max}}u(t-\tau)
```

```latex
\phi(t)=\frac{1}{q_{\max}}\int_{-\infty}^{t}\Gamma(\omega_0\tau)i(\tau)\,d\tau
```

```latex
\Gamma(\omega_0\tau)=\frac{c_0}{2}+\sum_{n=1}^{\infty}c_n\cos(n\omega_0\tau+\theta_n)
```

```latex
\mathcal{L}\{\Delta\omega\}=
10\log\left(
\frac{\Gamma_{\mathrm{rms}}^2}{q_{\max}^2}
\frac{\overline{i_n^2}/\Delta f}{4\Delta\omega^2}
\right)
```

```latex
\omega_{1/f^3}=
\omega_{1/f}\frac{c_0^2}{2\Gamma_{\mathrm{rms}}^2}
\approx
\omega_{1/f}\left(\frac{c_0}{c_1}\right)^2
```

```latex
\mathcal{L}_{\mathrm{in-band,CP}}
\approx
\frac{S_{iCP,n}}{2\beta_{CP}^{2}}
```

```latex
\beta_{CP,PFD}
=
\frac{I_{CP}}{2\pi}\frac{1}{N}
=
\frac{K_d}{N}
```

```latex
\beta_{CP,SS}
\approx
A_{VCO}g_m
```

```latex
\frac{\mathcal{L}_{\mathrm{in-band,CP,PFD}}}
{\mathcal{L}_{\mathrm{in-band,CP,SS}}}
=
\left(
4\pi N\frac{A_{VCO}}{V_{gs,\mathrm{eff}}}
\right)^2
\left(
\frac{\tau_{PFD}}{T_{ref}}
\right)
```

```latex
\sigma_t^2=
\frac{2\int_{f_l}^{f_h}\mathcal{L}(f)\,df}
{(2\pi f_{out})^2}
```

```latex
\mathcal{L}_{\mathrm{in-band,RefBuff}}
\approx
\frac{1}{2}N^2S_{\phi,\mathrm{RefBuff},n}
```

## Archive Actions

The following files were moved from `00_Inbox/incoming/papers/` to `90_Archive/processed/2026/papers/hajimiri_gao_pll_sources_2026-07-05/`:

- `0179haji.pdf`
- `A_Low_Noise_Sub-Sampling_PLL_in_Which_Divider_Noise_Is_Eliminated_and_PD-CP_Noise_Is_not_multiplied_by_N^2.pdf`

No legacy ChatGPT export, conversation inventory, manual batch, processed export, raw export, or unprocessed-note folder was scanned, moved, archived, or modified during this run.

## Manual Review Items

| Item | Reason |
|---|---|
| ISF formula use | The formulas are source-backed, but practical use requires extracting or simulating $\Gamma(x)$ for the actual oscillator topology and noise-injection node. |
| Flicker upconversion | The $c_0$ guidance is qualitative unless the waveform and ISF coefficients are computed. Treat symmetry as a strong design rule, not a guaranteed numeric result. |
| Sub-sampling PLL acquisition | The in-band noise advantage assumes locked operation. Frequency acquisition, false-lock avoidance, and FLL disengagement still require circuit-level verification. |
| Reference-buffer noise | The SSPLL paper shows that reference-buffer noise can become dominant after divider and PD/CP noise are reduced. SerDes clocking review must include the full reference path. |
| Measured 0.15 ps jitter example | The reported result is from a 2.21 GHz, 0.18 um CMOS demonstration. Do not treat it as a modern PCIe 7.0 target or guarantee. |

## Quality Checklist

| Check | Result |
|---|---|
| Used Balanced Ingest mode | Pass |
| Scanned only `00_Inbox/incoming/` | Pass |
| Avoided legacy chat-processing folders | Pass |
| Classified each source | Pass |
| Identified canonical notes before editing | Pass |
| Avoided duplicate technical notes | Pass |
| Promoted important formulas in Markdown LaTeX | Pass |
| Added concise engineering insights | Pass |
| Added durable note updates as bilingual paragraph pairs | Pass |
| Preserved source provenance | Pass |
| Updated index and paper citation anchor | Pass |
| Archived originals after successful processing | Pass |

## Follow-Up Recommendations

1. If future PLL papers add enough material, consider a dedicated canonical note on sub-sampling PLLs, but only after the topic exceeds the scope of `pll_phase_noise_jitter.md`.
2. Add simulation workflow notes later for extracting ISF from transient-noise/PSS-style analysis if supported by tool-specific sources.
3. In future SerDes clocking reviews, compare PLL architectures by in-band noise multiplication, reference-noise transfer, acquisition robustness, spur behavior, and integrated jitter together.
