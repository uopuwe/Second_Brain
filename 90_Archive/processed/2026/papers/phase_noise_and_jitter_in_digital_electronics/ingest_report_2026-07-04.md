# Ingest Report: Phase Noise and Jitter in Digital Electronics

## Summary

Processed one external paper from `00_Inbox/incoming/papers/` and merged reusable knowledge into the existing canonical PLL/clocking note.
No duplicate technical note was created.

## Source Material

- Original inbox path: `00_Inbox/incoming/papers/Phase Noise and Jitter in Digital Electronics.pdf`
- Archived path: `90_Archive/processed/2026/papers/phase_noise_and_jitter_in_digital_electronics/Phase Noise and Jitter in Digital Electronics.pdf`
- Source type: paper PDF.
- Source title: "Phase Noise and Jitter in Digital Electronics"
- Authors: Claudio E. Calosso and Enrico Rubiola.
- Date: 2017-01-03.
- Public identifier: arXiv:1701.00094v1.
- Domains: phase noise, jitter, digital clock distribution, PLL, divider, FPGA clocking, thermal delay, Allan deviation.

## Topic Classification

- Primary topic: PLL / CDR / Clocking.
- Secondary topics: digital clock distribution, measurement methodology, clock buffer noise, phase-noise scaling, jitter interpretation.
- Not promoted as: PCIe compliance source, SerDes standards source, or direct silicon signoff data.

## Canonical Note Decision

Canonical destination:

- `01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_phase_noise_jitter.md`

Reason:

- The repository already has an active canonical note for phase noise, jitter, PLL noise shaping, CDR interaction, and SerDes clocking implications.
- `01_AnalogIC_SerDes/PLL_CDR_Clocking/phase_noise_jitter.md` is already a merged alias pointing to `pll_phase_noise_jitter.md`.
- Creating another phase-noise or jitter note would duplicate existing canonical knowledge.

## Content Promoted

Reusable knowledge merged into the canonical note:

- Phase-time conversion using $x(t)=\phi(t)/(2\pi\nu_0)$.
- PSD conversion using $S_x(f)=S_\phi(f)/(4\pi^2\nu_0^2)$.
- RMS time fluctuation from $\int S_x(f)\,df$.
- Distinction between phase-type and time-type noise.
- Threshold-noise-to-edge-time conversion using $x(t)=n(t)/\mathrm{SR}$.
- Sinusoidal zero-crossing slew relation $\mathrm{SR}=2\pi\nu_0V_0$.
- Digital clocking aliasing equations for phase-type and time-type white noise.
- Input chatter condition and slew-rate interpretation.
- FPGA/internal PLL measurement lessons as design-review intuition.
- Thermal delay transient model and low-frequency wander implications.
- Engineering review questions for SerDes/PLL/CDR clock distribution.

## Formulas Extracted

The following formulas were added in Markdown LaTeX:

- $x(t)=\phi(t)/(2\pi\nu_0)$
- $S_x(f)=S_\phi(f)/(4\pi^2\nu_0^2)$
- $J^2=\int_{f_L}^{f_H}S_x(f)\,df$
- $x(t)=n(t)/\mathrm{SR}$
- $\mathrm{SR}=2\pi\nu_0V_0$
- $\phi(t)=n(t)/V_0$
- $b_0=h_0B/(\nu_0V_0^2)$
- $k_0=h_0B/(4\pi^2\nu_0^3V_0^2)$
- $k_0=J^2/\nu_0$
- $b_0=4\pi^2J^2\nu_0$
- $\langle \mathrm{SR}_n^2\rangle = 4\pi^2\int_0^\infty f^2S_n(f)\,df$
- $\langle \mathrm{SR}_n^2\rangle = (4\pi^2/3)h_0B^3$
- $\nu_0V_0=\sqrt{h_0B^3/3}$
- $x(t)=k'\Delta T(1-e^{-t/\tilde{\tau}})+k''t$

## Destination Notes Changed

- `01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_phase_noise_jitter.md`
  - Updated frontmatter date.
  - Added `Digital Clock Distribution Noise` section.
  - Added source provenance table.
  - Added archived PDF link.
  - Added engineering insights and design-review questions.

## New Notes Created

No new technical note was created.
The existing canonical note was updated.

This ingest did create this archive report:

- `90_Archive/processed/2026/papers/phase_noise_and_jitter_in_digital_electronics/ingest_report_2026-07-04.md`

## Links And Indexes

- Added a Markdown provenance link from the canonical note to the archived PDF.
- No master-index update was required because `pll_phase_noise_jitter.md` was already listed as an active PLL/CDR/clocking note.
- No MOC update was required because no new canonical concept note was created.

## Continuous Knowledge Improvement

### Actions Completed

- Knowledge evolution: canonical note remains active; no maturity upgrade claimed.
- Quality evaluation: source-backed formula and engineering insight coverage improved.
- Gap analysis: no new blocking gap created; existing standards caveats remain.
- Research roadmap: no new roadmap item required from this single source.
- Duplicate elimination: avoided duplicate note creation; used existing canonical note.
- Cross-link optimization: source provenance link added.
- Formula improvement: equations added with symbol definitions and engineering implications.
- Engineering insight expansion: added digital clock distribution, chatter, internal PLL, and thermal wander implications.
- Knowledge density optimization: promoted reusable synthesis only; did not paste raw paper text.

### Metrics

| Metric | Result | Notes |
| --- | --- | --- |
| Source coverage ratio | 1/1 changed durable note | Canonical note includes archived source link. |
| Quality evaluation coverage | Complete for this scoped ingest | Focused quality check only; no numeric score recorded. |
| Gap decision coverage | Complete | No new blocking gap opened. |
| Duplicate candidates | 1 existing alias note checked | `phase_noise_jitter.md` already points to canonical note. |
| Broken links introduced | 0 expected | Archived PDF link target exists after archive action. |
| Formula completeness findings | Improved | Added symbol definitions and design implications. |
| Interview questions generated | 0 | Existing canonical note already has interview Q&A; this ingest added review questions instead. |
| Reading recommendations created | 0 | Source itself was the planned reading item. |
| Density issues resolved or deferred | Complete | Raw paper text was not copied into the note. |

## Archive Actions

- Created archive folder: `90_Archive/processed/2026/papers/phase_noise_and_jitter_in_digital_electronics/`
- Moved original PDF from `00_Inbox/incoming/papers/` to the archive folder.
- Created this ingest report in the archive folder.

## Manual Review Items

- Device-specific FPGA measurements should not be generalized to SerDes silicon without topology, technology, and measurement-context review.
- Existing PCIe 7.0 compliance caveats in the canonical note remain unresolved and require primary specification or internal requirement verification.
- Existing Obsidian wikilinks in `pll_phase_noise_jitter.md` include several future-note-style targets; a separate link-health pass can decide whether to create, redirect, or leave them as roadmap targets.
- The canonical note contains older mixed-language and encoding artifacts outside the new section; cleanup is outside this ingest scope.

## Final Status

The source was processed successfully.
Reusable knowledge was merged into the existing canonical note.
The original PDF was archived.
No duplicate phase-noise or jitter note was created.
