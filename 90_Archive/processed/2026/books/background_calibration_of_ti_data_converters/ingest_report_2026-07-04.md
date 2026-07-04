---
title: "Ingest Report: Background Calibration of Time-Interleaved Data Converters"
domain: "Vault_Maintenance"
tags:
  - Ingest
  - Report
  - ADC
  - TimeInterleaving
  - Calibration
status: "active"
created: 2026-07-04
updated: 2026-07-04
source: "Deep Ingest workflow (.codex/ingest.md)"
confidence: "high"
---

# Ingest Report: Background Calibration of Time-Interleaved Data Converters

## Summary

- **Ingest level:** Deep Ingest (explicitly requested by the user; source is a 138-page book, so per rule 21 confirmation was already given by the explicit request).
- **Workflow:** `.codex/ingest.md` → Capture → Ingest → Knowledge Evolution → Quality Evaluation → Gap Analysis → Research Roadmap → CKI → Archive → Report.
- **Scan scope:** `00_Inbox/incoming/` only (inbox-lane rule respected; no legacy chat folders touched).
- **Result:** One cornerstone source fully processed; 6 canonical/index notes updated; 1 MOC created; 0 duplicate knowledge notes created; source archived.

## Processed Files

| Source | Type | Pages | Disposition |
|---|---|---|---|
| `00_Inbox/incoming/books/Background Calibration of Time-Interleaved Data Converters.pdf` | Book (Springer 2012) | 138 | Deep-ingested, archived |

- **Citation:** M. El-Chammas and B. Murmann, *Background Calibration of Time-Interleaved Data Converters*, Analog Circuits and Signal Processing series, Springer, 2012. ISBN 978-1-4614-1510-7; DOI 10.1007/978-1-4614-1511-4.
- **Extraction depth:** Ch. 2 (TI-ADC model, frequency-domain analysis, quantitative mismatch bounds) and Ch. 3 (background timing-skew calibration) read in full; Appendices D (comparator skew) and E (residual-skew/jitter extraction) read in full; Ch. 4–6 and Appendices A–C reviewed at summary level (comparator power optimization, circuit design, measured results).

## Updated Canonical Notes

| Note | Change |
|---|---|
| `01_AnalogIC_SerDes/ADC_TI_SAR/ti_sar_mismatch_calibration.md` | **Primary destination.** Added "Deep Ingest 2026-07-04" section: best-fit error model, closed-form offset/gain/skew variance bounds referenced to `SNR_Q`, signal-statistics (`R''(0)`) dependence and sine over-constraint, the cross-correlation background timing-skew calibration algorithm (reference ADC, 1-bit + subsampled simplifications, Van Vleck, convergence self-normalization), skew-mitigation routes, residual-skew extraction, prototype data point, 4 new common mistakes, provenance. |
| `01_AnalogIC_SerDes/ADC/sampling_jitter_adc.md` | Added quantization-referenced jitter bound (jitter as `N→∞` limit of skew), `R''(0)` signal dependence, comparator-skew SNR, deterministic-vs-random separation. |
| `01_AnalogIC_SerDes/ADC/ti_sar_adc_calibration.md` | Light-touch cross-reference to the canonical bounds/algorithm (no formula duplication, to respect the one-topic-one-canonical-note rule given the existing overlap between the two TI notes). |
| `01_AnalogIC_SerDes/Papers_Books/core_serdes_papers.md` | Added §13 "Ingested Books / Cornerstone References" with full citation, reading status, chapter map, and promotion targets (citation anchor). |
| `01_AnalogIC_SerDes/analog_ic_serdes_master_index.md` | Added canonical TI note + MOC + source pointer to the ADC section. |

## New Notes (created only where structurally necessary)

| Note | Justification |
|---|---|
| `80_MOCs/ti_adc_calibration_moc.md` | The `80_MOCs/` folder was empty; the newly source-backed TI-ADC / ADC-based-RX cluster now warrants a Map of Content (reading order + concept map + key results). This is graph structure, not duplicated knowledge. |

No new **knowledge** notes were created. The two pre-existing overlapping TI notes (`ti_sar_adc_calibration.md`, `ti_sar_mismatch_calibration.md`) were reused rather than adding a third.

## Formulas and Derivations Promoted

Written in Markdown LaTeX with symbols, units, and validity limits per `.codex/formula_style.md`:

- Quantization-noise reference SNR: `SNR_Q = (3/2)·2^(2B)`.
- Best-fit error decomposition `y[n] = x_o[n] + e[n]`, orthogonality of `x_o` and `e`.
- Closed-form variance bounds: offset `σ_o² ≤ (N/(N-1))·(2/3)·P/2^(2B)`; gain `σ_G² ≤ (N/(N-1))·(2/3)·1/2^(2B)`; timing skew `σ_τ² ≤ (N/(N-1))·(2/3)·1/(2^(2B)|R''(0)|)`.
- Sine-input skew bound and the `|R''(0)| = (2π f_in)²` substitution.
- Jitter bound `σ² ≤ 2/(3·2^(2B)|R''(0)|)` as the `N→∞` limit; sine form `σ² ≤ 2/(3·2^(2B)(2π f_in)²)`.
- Cross-correlation estimator `R̂(τ) = (1/M)Σ y[n]y_c[n] = R(τ) + E(M)`, var(E) ∝ 1/M.
- Van Vleck 1-bit correlation `R_1(τ) = (2/π)sin⁻¹(R(τ))` and the offset flat-region bound.
- Calibration-clock cycling condition `f_cal = f_s/M`, `gcd(M,N)=1`.
- Convergence: samples ∝ `c⁴` of frequency ratio, self-normalized by the `1/f_in` skew bound.
- Comparator-skew SNR `1/(2π f_in σ_α)²`; residual-skew pseudo-inverse extraction `C = B⁻¹A`, `τ_i = ln(C_i)/(-j2π f_in)`.

Derivations expanded because they teach reusable reasoning: (a) why only inter-channel *differences* distort; (b) why skew tolerance is signal-statistics dependent; (c) why cross-correlation with a reference ADC substitutes for the unavailable input autocorrelation; (d) why the sample-count requirement self-normalizes with frequency.

## Index and MOC Updates

- Created `80_MOCs/ti_adc_calibration_moc.md`.
- Updated `analog_ic_serdes_master_index.md` ADC section (added canonical note, MOC link, source note).
- Added citation anchor section in `core_serdes_papers.md`.
- Obsidian `[[wikilinks]]` added across the five touched notes to connect the cluster (clocking, supply, equalization neighbors).

## Archive Actions

- Moved source PDF to `90_Archive/processed/2026/books/background_calibration_of_ti_data_converters/` (source was untracked in git; moved on disk; `00_Inbox/incoming/books/` returned to `.gitkeep`-only).
- This report co-located with the archived source, matching the existing `90_Archive/processed/2026/papers/*/ingest_report_*.md` pattern.
- Temporary text-extraction files under `tools/` were removed after use.

## Bilingual / Confidentiality / Quality Screen

- **Bilingual:** all newly added explanatory prose is in paragraph-level Chinese-then-English pairs (formulas, tables, path lists, and short link lists excluded per rule 18).
- **Confidentiality:** none — the source is a published book; no employer-confidential content involved. Existing `待确认` Synopsys markers preserved.
- **Quality (per `quality_score.md`):** `ti_sar_mismatch_calibration.md` was already a mature, math-complete note; this ingest raises its provenance and rigor to reference-grade. `sampling_jitter_adc.md` upgraded from active to reference-grade on the jitter-bound topic. MOC is a new active navigation note.

## Manual Review Items / Gaps (per knowledge_gap.md)

1. **`待确认` — gain-mismatch numeric example.** The book's printed gain example (~1.1% for N=2, B=10) did not reconcile with the value implied by `SNR_Q=(3/2)2^(2B)` (self-derivation gives ~0.08–0.11%). Formulas retained as authoritative; printed figure flagged for primary-source recheck.
2. **Bandwidth mismatch** is explicitly out of this book's calibration scope; the vault's frequency-dependent `H_m(f)` / FIR treatment remains the canonical coverage — no source upgrade from this book.
3. **Roadmap link:** the correlation-based reference-ADC calibration and the `1/f_in`-self-normalizing convergence are strong candidates to connect to the future 112G/224G ADC-based RX study thread and to PCIe 7.0 clocking (sampling-phase generation). Recorded for research roadmap.
4. Ch. 4–5 circuit-level details (dynamic-comparator power model, bootstrapped T&H, delay cell) were summary-read only; a future Balanced pass could promote the comparator power/area optimization framework if a circuit-design note is created.

## Verification Limits

- PDF text was auto-extracted; math glyphs were partially garbled in extraction, so every promoted equation was reconstructed from context and **re-derived / dimensionally checked** rather than copied. The offset worked example (0.8 mV) and the sub-ps skew conclusion were reproduced independently and match the book; the gain numeric is flagged above.
- Chapters not read in full (4–6, App. A–C) are represented only at summary level and were not used to assert quantitative durable claims.
