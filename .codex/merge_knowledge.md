# Merge Knowledge Workflow

## Purpose

Use this workflow when overlapping notes should be consolidated or canonicalized.
Mandatory policy is in [core/mandatory_rules.md](core/mandatory_rules.md).
Quality gates are in [core/quality_standards.md](core/quality_standards.md).

## Active Roles

- Knowledge architect: canonical destination and boundaries.
- Editor: structure and clarity.
- Librarian: source history and link updates.
- Reviewer: conflict and quality checks.

## When to Merge

Merge when notes duplicate the same concept at the same level.
Do not merge when notes serve distinct purposes such as paper summary, interview answer, design record, and general concept note.

## Workflow

1. Identify all candidate notes.
2. Read each candidate fully.
3. Classify each note's purpose.
4. Choose a canonical note or decide not to merge.
5. Build a merge map listing canonical file, source files, promoted content, retained separate content, and conflicts.
6. Move unique high-value content into the canonical note.
7. Preserve source history in the canonical note.
8. Resolve conflicting claims or add a visible uncertainty section.
9. Update links using [build_links.md](build_links.md).
10. Update indexes using [indexing.md](indexing.md).
11. Do not delete source notes unless explicitly requested.
12. Verify against [core/quality_standards.md](core/quality_standards.md).

## Good Example

```markdown
Canonical: `PLL_CDR_Clocking/pll_phase_noise_jitter.md`
Source notes: chat summary and older phase-noise note.
Promoted: integration-bandwidth caveat and phase-error conversion.
Kept separate: paper-specific reading notes.
```

## Bad Example

```markdown
All CDR, PLL, paper, and interview notes are merged into `clocking_notes.md`.
```

This destroys purpose boundaries.

## Edge Cases

- If two notes conflict, prefer sourced and assumption-aware claims.
- If an older note is useful only as history, leave it intact or add redirect text with permission.
- If a duplicate folder contains unique content, inventory before promotion.
- If merge scope becomes too large, split into staged merges.

## Output Contract

A merge task should report canonical note, source notes considered, content promoted, conflicts or uncertainty, links and indexes updated, and source notes left untouched or redirected.

