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
  - SerDes
  - PLL
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
- Use bullets for peer lists.
- Use numbered lists for ordered procedures.
- Use fenced code blocks for commands, code, and text diagrams.
- Use relative Markdown links for durable file references.
- Keep plugin-specific syntax minimal.

## Good Example

```markdown
# CDR Jitter Tolerance

## Purpose

This note explains how CDR loop behavior affects receiver tolerance to input jitter.

## Related Notes

- [CDR fundamentals](cdr_fundamentals.md)
- [PLL phase noise and jitter](pll_phase_noise_jitter.md)
```

## Bad Example

```markdown
# notes
PLL CDR stuff #important #readlater [[thing]] [here](missing.md)
```

## Link Standard

Prefer:

```markdown
[PLL phase noise and jitter](../PLL_CDR_Clocking/pll_phase_noise_jitter.md)
```

Avoid vague links:

```markdown
[here](note.md)
```

## Markdown Quality Gate

Before finishing a durable note:

- Frontmatter is valid when present.
- H1 is specific.
- Headings are coherent.
- Links are useful and resolve.
- No empty section stubs remain.
- The file is readable in plain text.

