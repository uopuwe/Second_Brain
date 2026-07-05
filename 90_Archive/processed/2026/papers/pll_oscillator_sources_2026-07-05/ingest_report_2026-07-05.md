# Ingest Report - PLL and Oscillator Source Batch

## Run Summary

| Item | Value |
|---|---|
| Date | 2026-07-05 |
| Mode | Balanced Ingest |
| Ingest target | `00_Inbox/incoming/` |
| Source lane | `00_Inbox/incoming/papers/` |
| Archive destination | `90_Archive/processed/2026/papers/pll_oscillator_sources_2026-07-05/` |
| Canonical-note policy | Merge into existing canonical notes; do not create duplicate notes |
| Bilingual-note policy | Durable note additions were written as paragraph-level Chinese-English bilingual pairs |

## Processed Files

| Source file | Source type | Classification | Canonical destination | Status |
|---|---|---|---|---|
| `1665-Analysis of charge-pump phase-locked loops.pdf` | IEEE TCAS-I paper | CPPLL, sampled-data loop analysis, third-order loop filter, stability | `01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_fundamentals.md` | Processed and archived |
| `An_Overview_of_Phase-Locked_Loop_From_Fundamentals.pdf` | Review paper | PLL architecture taxonomy and broad survey context | `01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_fundamentals.md` | Processed and archived |
| `Exploring_the_Landscape_of_Phase-Locked_Loop_Archi.pdf` | Review paper | PLL architecture survey vocabulary and comparison context | `01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_fundamentals.md` | Processed and archived |
| `Jitter-Power Trade-Offs in PLLs BR_TCAS_2021.pdf` | IEEE TCAS-I paper | PLL jitter-power scaling, VCO/reference/charge-pump noise, ADC jitter penalty | `01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_phase_noise_jitter.md` | Processed and archived |
| `The Ring Oscillator [A Circuit for All Seasons]-Razavi.pdf` | IEEE Solid-State Circuits Magazine tutorial | Ring oscillator delay, power, phase noise, supply sensitivity, multiphase generation | `01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_phase_noise_jitter.md` | Processed and archived |

## Updated Canonical Notes

| Note | Update |
|---|---|
| `01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_fundamentals.md` | Added a Balanced Ingest section covering third-order CPPLL sampled-data behavior, loop-filter ripple/third-pole tradeoff, architecture taxonomy handling, design-review questions, and source provenance. |
| `01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_phase_noise_jitter.md` | Added jitter-power lower-bound scaling, reference-limited jitter-power scaling, charge-pump noise treatment, ADC sampling jitter formulas, ring-oscillator delay/power relations, supply-noise-to-phase-noise modeling, and design-review additions. |
| `01_AnalogIC_SerDes/Papers_Books/core_serdes_papers.md` | Added Section 14 as the citation anchor for the ingested PLL and oscillator papers. |
| `01_AnalogIC_SerDes/analog_ic_serdes_master_index.md` | Added a source-backed PLL update pointer from the master index to the canonical PLL notes and citation anchor. |

## New Notes

No new technical notes were created. Existing canonical notes were sufficient:

- `pll_fundamentals.md`
- `pll_phase_noise_jitter.md`
- `core_serdes_papers.md`
- `analog_ic_serdes_master_index.md`

## Formulas Promoted

The following formulas were promoted into canonical notes in Markdown LaTeX form:

```latex
T_0 = 2 N T_D
```

```latex
P \approx N f_0 C_L V_{DD}^2
```

```latex
P_{VCO} =
\frac{kT(1+\gamma)}{\pi Q^2 f_2}
\frac{1}{\sigma_j^2}
```

```latex
P_{VCO} =
\frac{kT(1+\gamma) S_{REF}}{\pi^2 Q^2 f_{REF}^2}
\frac{1}{\sigma_j^4}
```

```latex
S_{CP}(f)=
8\pi^2\frac{T_{CP}}{T_{REF}}
\frac{\overline{i_n^2}}{I_P^2}
```

```latex
\sigma_j^2 =
\frac{10^{m/10}-1}{3\pi^2 f_{in}^2 2^{2M+1}}
```

```latex
\sigma_j^2 =
\frac{10^{m/10}-1}{3\pi^2 f_{CK}^2 2^{2M-1}}
```

```latex
\phi_{VDD}(t)=K_{VDD}\int v_n(t)\,dt
```

```latex
S_{\phi,VDD}(f)=
\frac{K_{VDD}^2}{(2\pi f)^2}S_{VDD}(f)
```

## Archive Actions

The following files were moved from `00_Inbox/incoming/papers/` to `90_Archive/processed/2026/papers/pll_oscillator_sources_2026-07-05/`:

- `1665-Analysis of charge-pump phase-locked loops.pdf`
- `An_Overview_of_Phase-Locked_Loop_From_Fundamentals.pdf`
- `Exploring_the_Landscape_of_Phase-Locked_Loop_Archi.pdf`
- `Jitter-Power Trade-Offs in PLLs BR_TCAS_2021.pdf`
- `The Ring Oscillator [A Circuit for All Seasons]-Razavi.pdf`

No legacy ChatGPT export, conversation inventory, manual batch, processed export, raw export, or unprocessed-note folder was scanned, moved, archived, or modified during this run.

## Manual Review Items

| Item | Reason |
|---|---|
| CPPLL update-rate ratio example | The Hanumolu paper's instability examples are design-specific. Treat the reference-update-rate to loop-bandwidth ratio as a review warning, not a universal numeric rule. |
| PLL architecture review papers | The Nguyen/Pham and Dutta et al. sources are useful for taxonomy and vocabulary, but formula-level and performance claims should be confirmed against primary sources before design use. |
| Razavi jitter-power lower bounds | The expressions are first-order lower-bound estimates. Use them for design intuition and sanity checks, then verify with circuit-level phase-noise simulation, supply-noise analysis, and lab data. |
| Charge-pump noise treatment | The promoted charge-pump noise expression is a compact reference-like model. Real designs still need current-source noise, switching edge behavior, mismatch, leakage, and spur analysis. |
| Ring oscillator supply sensitivity | The $K_{VDD}$ model is a design-review anchor. Actual noise coupling depends on VCO topology, LDO output impedance, layout, substrate coupling, and supply distribution. |

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

1. Use the CPPLL sampled-data section as a seed for a future dedicated `pfd_charge_pump_notes.md` only when enough source-backed PFD/charge-pump material exists to justify a separate canonical note.
2. During the next PLL review pass, connect the jitter-power scaling results to PCIe clock-generation power budgeting and LDO noise budgeting.
3. Add primary-source ISSCC/JSSC examples of low-jitter LC PLLs, ring PLLs, and ADC sampling-clock generators to calibrate the lower-bound equations against measured silicon.
4. Add a compact interview section later if the user requests interview-focused expansion; this Balanced Ingest intentionally avoided long interview-question generation.
