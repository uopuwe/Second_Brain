# Expand Note Workflow

## Purpose

Use this workflow to turn a thin, rough, or conversational note into durable engineering knowledge.
Quality standards live in [core/quality_standards.md](core/quality_standards.md).
Engineering depth standards live in [engineering_notes.md](engineering_notes.md).

## Active Roles

- Technical writer: durable explanation.
- Analog IC expert: technical rigor.
- Editor: structure and readability.
- Librarian: links and provenance.

## Workflow

1. Read the target note.
2. Search for overlapping or related notes.
3. Identify note type: concept, design, paper, book, interview, or source-derived synthesis.
4. Preserve strong existing content.
5. Add or clarify purpose, summary, and system context.
6. Add mechanism-level explanation.
7. Add equations only under [formula_style.md](formula_style.md).
8. Add tradeoffs, failure modes, or debug hooks when relevant.
9. Add source and confidence information.
10. Add related links using [build_links.md](build_links.md).
11. Update indexes if the note becomes a major canonical reference.
12. Verify against [core/quality_standards.md](core/quality_standards.md).

## Expansion Targets

Use expansion for seed notes, AI-generated summaries, thin technical notes, notes missing assumptions or sources, and interview answers that need deeper references.
Do not expand by adding generic filler.

## Good Example

```markdown
Thin claim: "DSP fixes channel loss."

Expanded claim: "DSP equalization can reduce ISI after sampling, but it cannot recover information lost to insufficient analog bandwidth, excessive noise, aperture jitter, severe nonlinearity, or inadequate ADC resolution."
```

## Bad Example

```markdown
The note becomes longer but still lacks assumptions, source history, design tradeoffs, and links.
```

## Edge Cases

- If the note is technically wrong, correct the false claim before expanding.
- If a note spans too many domains, split by purpose and link the pieces.
- If the source is AI-generated, keep confidence conservative.
- If standards details are involved, mark exact values as source-required unless verified.

## Output Contract

An expanded note should have clear purpose, system context, technical mechanism, assumptions and units where relevant, source history, related links, and visible uncertainty.

