# Review Workflow

## Purpose

Use this workflow when the user asks for review, critique, audit, or risk assessment.
Mandatory review behavior is defined in [core/mandatory_rules.md](core/mandatory_rules.md).
Global quality gates are in [core/quality_standards.md](core/quality_standards.md).

## Active Roles

- Reviewer: findings and severity.
- Analog IC expert: technical correctness.
- Editor: clarity and structure.
- Librarian: links, sources, and canonical placement.

## Review Output Order

1. Findings ordered by severity.
2. Open questions or assumptions.
3. Suggested fixes.
4. Brief summary only after findings.

If no issues are found, say that clearly and state residual risk.

## Severity

- High: likely technical error, confidentiality issue, unsupported standards claim, or broken core reference.
- Medium: missing caveat, weak provenance, unclear equation, duplicate content, or misleading structure.
- Low: local clarity, naming, formatting, or link improvement.

## Workflow

1. Identify review mode: technical, structure, interview, source, Markdown, or tooling.
2. Read the target file.
3. Read related files if needed.
4. Evaluate against [core/quality_standards.md](core/quality_standards.md).
5. Check formulas with [formula_style.md](formula_style.md).
6. Check Markdown with [obsidian_style.md](obsidian_style.md).
7. Check links and indexes with [build_links.md](build_links.md) and [indexing.md](indexing.md).
8. Write findings with file, section, severity, why it matters, and suggested fix.
9. State verification limits.

## Good Finding

```markdown
High: The note reports RMS jitter without carrier frequency or phase-noise integration range.

Why it matters:
RMS jitter derived from phase noise is not comparable without those conditions.

Suggested fix:
Add carrier frequency, offset-frequency integration limits, and whether spurs are included.
```

## Bad Finding

```markdown
This note could be better and needs more detail.
```

## Edge Cases

- If the user asks only for review, do not edit unless requested.
- If current external facts matter, verify them or state that they were not verified.
- If confidential material appears, treat it as high severity.
- If a note is stylistically messy but technically sound, do not overstate style issues.

## Output Contract

A review response must be actionable and must not hide residual risk.

