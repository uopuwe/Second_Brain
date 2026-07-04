# Book Note Template

> Compatibility notice: the canonical template contract is now [../core/template_contracts.md](../core/template_contracts.md). This file is retained for existing path compatibility. Future agents must follow the core contract and ignore any duplicated legacy guidance below when it conflicts with the core operating system.

## Purpose

Use this template for textbooks, reference books, lecture-note collections, and long-form technical material.

The goal is not to reproduce the book.
The goal is to capture durable concepts, reading progress, useful equations, and connections to the vault.

## Recommended Frontmatter

```yaml
---
title: "Book Title Reading Notes"
domain: "AnalogIC_SerDes"
tags:
  - Book
  - AnalogIC
  - PLL
status: "active"
created: "2026-07-03"
updated: "2026-07-03"
source: "Book"
confidence: "medium"
author: "Author Name"
year: "YYYY"
---
```

## File Naming

Use:

```text
razavi_pll_reading_notes.md
serdes_reference_book_notes.md
adc_textbook_reading_notes.md
```

## Bibliographic Details

```markdown
## Bibliographic Details

- Title:
- Author:
- Edition:
- Year:
- Publisher:
- ISBN or URL:
- Access status: owned, library, online, excerpt, notes only.
```

If a field is unknown, state it clearly in prose rather than leaving it blank.

## Why This Book Matters

Example:

```markdown
## Why This Book Matters

This book provides the foundation for PLL loop dynamics and phase-noise intuition used in SerDes clocking and CDR design. It should support deeper notes on jitter transfer, oscillator noise, and supply-induced phase modulation.
```

## Reading Scope

Clarify the intended use.

```markdown
## Reading Scope

Current purpose:

- Review PLL fundamentals.
- Extract phase-noise and jitter conversion methods.
- Build interview-ready explanations.
- Link useful concepts to existing vault notes.

Not the current purpose:

- Reproduce every derivation.
- Summarize unrelated chapters in detail.
```

## Reading Status

```markdown
## Reading Status

- Current status: chapter-level reading in progress.
- Priority chapters: PLL basics, oscillator phase noise, clock recovery.
- Deep-read chapters: loop dynamics and noise.
- Skim chapters: unrelated RF system material.
```

## Chapter Map

Use a concise map.

```markdown
## Chapter Map

| Chapter | Topic | Vault Relevance | Status |
| --- | --- | --- | --- |
| 1 | Feedback basics | PLL/LDO loop intuition | skimmed |
| 2 | Oscillators | VCO phase noise | active |
| 3 | PLLs | Clocking and CDR | active |
```

Keep the table readable.

## Concept Extraction

For each important concept:

```markdown
## Concept: Loop Bandwidth

Source location:
Chapter and section if known.

Summary:
Loop bandwidth controls how the PLL responds to phase error over frequency. In a conventional PLL model, different noise sources are shaped differently by the loop.

Vault connections:

- [PLL fundamentals](../../01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_fundamentals.md)
- [PLL phase noise and jitter](../../01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_phase_noise_jitter.md)

Design implication:
Choosing loop bandwidth requires balancing tracking, noise filtering, stability, and spur behavior.
```

## Important Equations

Use `.codex/formula_style.md`.

Example:

```markdown
## Important Equations

The book's PLL noise model should be translated into the vault's notation before being added to topic notes.

When extracting equations:

- Define symbols.
- Preserve assumptions.
- State whether the model is linearized.
- Connect to design implications.
```

## Design Lessons

Capture reusable lessons.

Example:

```markdown
## Design Lessons

- A loop bandwidth number alone is not enough to characterize a PLL. Noise transfer, stability margin, reference quality, VCO noise, and spurs all matter.
- Oscillator supply sensitivity connects power integrity directly to clock jitter.
- Linear models are useful for intuition but must be checked against nonlinear behavior such as bang-bang phase detection or saturation.
```

## Interview Use

Example:

```markdown
## Interview Use

Useful for answers about:

- How a PLL works.
- How phase noise becomes jitter.
- Why loop bandwidth matters.
- How supply noise affects clocking.
- How to explain design tradeoffs beyond formulas.
```

## Links to Topic Notes

```markdown
## Links to Topic Notes

- [PLL fundamentals](../../01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_fundamentals.md)
- [CDR fundamentals](../../01_AnalogIC_SerDes/PLL_CDR_Clocking/cdr_fundamentals.md)
- [PLL phase noise and jitter](../../01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_phase_noise_jitter.md)
- [SerDes power integrity](../../01_AnalogIC_SerDes/LDO_Bandgap/serdes_power_integrity.md)
```

## Questions for Later Review

Use technical questions:

```markdown
## Questions for Later Review

- Which PLL noise transfer derivation is most useful for the vault's SerDes clocking notes?
- Which assumptions break when moving from a linear PLL to a bang-bang CDR?
- Which equations should be converted into a Python calculation script?
```

## Extraction Log

Use this when reading over time.

```markdown
## Extraction Log

- 2026-07-03: Extracted loop bandwidth intuition and linked it to PLL fundamentals.
- 2026-07-04: Added phase-noise integration notes to the jitter topic note.
```

Use real dates when creating actual notes.

## Copyright-Safe Practice

Do:

- Paraphrase.
- Quote only short phrases when necessary.
- Record page or section references.
- Link concepts to your own notes.

Do not:

- Copy chapter text.
- Recreate long derivations verbatim.
- Paste large tables from the book.
- Store copyrighted figures unless allowed.

## Book Note Completion Checklist

Before finishing:

- Bibliographic data is captured.
- Reading scope is clear.
- Chapter map is useful.
- Extracted concepts link to topic notes.
- Equations are rewritten with symbols and assumptions.
- Design lessons are separated from book summary.
- No large copyrighted text is copied.
- Open technical questions are explicit.

## Expert Rationale for This Template

Book notes serve a different role from paper notes.
Papers often provide narrow evidence.
Books provide conceptual frameworks, derivations, terminology, and durable mental models.

The risk with book notes is over-summarization:
copying chapter structure without extracting usable engineering knowledge.
This template forces reading notes to connect book concepts to vault topics, design intuition, formulas, and future study.

For a senior engineer, a useful book note should answer:

- Which chapters matter for current goals?
- Which concepts should be promoted to topic notes?
- Which derivations are worth revisiting?
- Which assumptions does the book use?
- How does this source improve design reasoning?

For a future AI agent, the book note identifies source authority and extraction status.

## Why Each Section Exists

### Bibliographic Details

Reason:
Books have editions.
Equations, chapters, and terminology may differ by edition.

### Reading Scope

Reason:
A technical book may cover far more than the vault needs.
Scope prevents wasted extraction.

### Chapter Map

Reason:
Chapter maps support long-term reading across many sessions.

### Concept Extraction

Reason:
The durable value is usually a concept, derivation, or model that should link to topic notes.

### Extraction Log

Reason:
Book reading often happens over weeks or months.
The log prevents repeated work.

## Best Practices

- Read with a technical goal.
- Track edition and chapter.
- Extract concepts, not whole chapters.
- Paraphrase in your own words.
- Record page or section references when useful.
- Link concepts to domain notes.
- Promote equations only with assumptions.
- Separate book explanation from Codex interpretation.
- Keep reading status honest.

## Bad Book Note Example

```markdown
Chapter 1 talks about analog design. Chapter 2 talks about PLLs. Chapter 3 talks about noise. This is useful.
```

Why this is bad:

- No extraction.
- No technical details.
- No links.
- No reading status.
- No design implication.

## Good Book Note Example

```markdown
## Concept: PLL Noise Transfer

Source location:
Chapter 8, PLL noise section.

Summary:
The book models PLL output phase noise as shaped contributions from reference, divider, loop components, and oscillator noise. The useful vault-level lesson is that loop bandwidth cannot be optimized without knowing the dominant noise source.

Vault links:
- [PLL fundamentals](../../01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_fundamentals.md)
- [PLL phase noise and jitter](../../01_AnalogIC_SerDes/PLL_CDR_Clocking/pll_phase_noise_jitter.md)
```

## Engineering Example: PLL Textbook

Extract:

- Linear PLL model.
- Noise transfer functions.
- Loop bandwidth intuition.
- Stability criteria.
- Oscillator phase noise mechanisms.
- Phase-noise-to-jitter conversion.

Promote to:

- `pll_fundamentals.md`
- `pll_phase_noise_jitter.md`
- `cdr_fundamentals.md` only with caveats about data-driven detectors.

Avoid:

- Treating linear PLL results as directly applicable to every CDR.
- Copying derivations verbatim.
- Ignoring notation differences.

## Workflow for Book Reading

1. Capture bibliographic metadata.
2. Define reading scope.
3. Identify priority chapters.
4. Create a chapter map.
5. Extract concepts one at a time.
6. Link each concept to topic notes.
7. Promote durable concepts into domain notes when ready.
8. Record extraction log.
9. Add questions for later review.
10. Avoid copying long passages.

## Edge Cases

### The Book Is Broad

Scope the reading to current goals.
Do not summarize unrelated chapters in detail.

### Edition Is Unknown

State that edition is unknown.
Avoid page-specific references unless they can be verified.

### The Book Uses Different Notation

Translate notation when promoting equations.
Record original notation only when needed.

### The Book Conflicts with a Paper

Check assumptions.
Books may present foundational models while papers address architecture-specific implementations.

### The Book Is Used for Interview Prep

Extract concise explanations, but link them to deep technical notes.
Do not let interview phrasing replace technical understanding.

## Quality Checklist

- Bibliographic details are recorded.
- Reading scope is clear.
- Chapter map is useful.
- Extracted concepts are specific.
- Equations include assumptions and notation.
- Topic notes are linked.
- Reading status is honest.
- Copyright-safe paraphrase is used.
- Open questions are technical and actionable.

## Automation Opportunities

Future tools could:

- Generate citation frontmatter.
- Track reading status.
- Build chapter progress tables.
- Suggest vault links from concept headings.
- Detect copied long excerpts.
- Convert extracted equations into formula-style entries.
- Generate reading plans from career goals.

Automation should not replace careful reading or source-aware synthesis.

## Future Extension Ideas

- Add a book reading dashboard.
- Add priority chapter queues for PLL/CDR, ADC, LDO, and SerDes.
- Add concept-to-note promotion tracking.
- Add a bibliography index.
- Add comparison notes across books.
- Add interview answer extraction maps.

## Self-Contained Summary

This template creates book notes that support long-term technical learning.
It captures bibliographic context, reading scope, chapter maps, extracted concepts, equations, design lessons, links, and reading history.
The goal is durable engineering understanding, not chapter-by-chapter copying.
