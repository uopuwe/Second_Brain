# Obsidian and Markdown Standards

## Purpose

This document defines Markdown and Obsidian standards for durable vault content.
It is a quality standard, not a workflow.

## Frontmatter Standard

Durable notes should use valid YAML frontmatter:

```yaml
---
title: "Readable Note Title"
domain: "AnalogIC_SerDes"
tags:
  - domain/analog_ic_serdes
  - topic/serdes
  - topic/pll
  - type/permanent
  - status/active
status: "active"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
source: "short source description"
confidence: "medium"
---
```

## Markdown Standard

- Use one H1 per note.
- Use headings for navigation.
- Use short paragraphs.
- For durable explanatory content added during ingest, use paragraph-level Chinese-English bilingual pairs.
- Use bullets for peer lists.
- Use numbered lists for ordered procedures.
- Use fenced code blocks for commands, code, and text diagrams.
- Use relative Markdown links for durable file references.
- Keep plugin-specific syntax minimal.

## Bilingual Paragraph Standard

When ingesting new external knowledge into durable notes, write newly added or substantially rewritten explanatory content as bilingual paragraph pairs.

Use this order:

```markdown
中文：先用自然工程中文解释概念、假设、限制和设计意义。

English: Then provide the matching English explanation with the same technical meaning.
```

Rules:

- Keep the Chinese and English paragraphs adjacent.
- Match technical meaning across both languages.
- Do not use English as a vague summary if the Chinese paragraph contains specific assumptions, equations, or caveats.
- Do not use Chinese as a literal word-by-word translation if a clearer engineering expression exists.
- Equations, YAML frontmatter, code blocks, file paths, and short link lists do not need duplicate bilingual copies.
- Formula explanations, symbol definitions, approximation limits, and engineering implications should be bilingual.
- Tables may remain compact, but surrounding context should be bilingual.
- Existing legacy text does not need full conversion unless it is substantially edited.

## Good Example

```markdown
# CDR Jitter Tolerance

## Purpose

中文：这篇笔记解释 CDR loop behavior 如何影响接收端对输入 jitter 的容忍度。

English: This note explains how CDR loop behavior affects receiver tolerance to input jitter.

## Related Notes

- CDR fundamentals: `cdr_fundamentals.md`
- PLL phase noise and jitter: `pll_phase_noise_jitter.md`
```

## Bad Example

```markdown
# notes
PLL CDR stuff #important #readlater thing here missing.md
```

## Link Standard

Prefer:

```markdown
PLL phase noise and jitter: `../PLL_CDR_Clocking/pll_phase_noise_jitter.md`
```

Avoid vague links:

```markdown
here: `note.md`
```

## Markdown Quality Gate

Before finishing a durable note:

- Frontmatter is valid when present.
- H1 is specific.
- Headings are coherent.
- Links are useful and resolve.
- No empty section stubs remain.
- The file is readable in plain text.
