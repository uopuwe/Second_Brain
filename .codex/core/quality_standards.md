# Quality Standards

## Purpose

This document defines quality gates.
It does not define task workflow.
For workflow selection, see [workflow_router.md](workflow_router.md).

## Global Quality Gates

Every durable output must be:

- Accurate within stated assumptions.
- Source-aware.
- Maintained in the correct vault location.
- Readable in Markdown.
- Linked when it affects other knowledge.
- Free of hidden uncertainty.
- Safe with respect to confidentiality.

## Technical Note Quality

A strong technical note includes:

- Purpose.
- System context.
- Mechanism.
- Assumptions.
- Quantitative relationships when useful.
- Design tradeoffs.
- Failure modes or debug hooks when relevant.
- Related links.
- Source and verification status.

Bad note:

```markdown
The CDR recovers the clock and reduces jitter.
```

Good note:

```markdown
A CDR estimates phase error from data transitions and adjusts sampling phase or recovered clock timing. Its jitter behavior depends on detector type, transition density, loop bandwidth, equalizer output, and the input jitter spectrum.
```

## Source Quality

Use this hierarchy:

1. Primary standards, papers, books, datasheets, or official documentation.
2. Vendor application notes with vendor-specific framing.
3. User-provided design experience or notes.
4. Existing vault synthesis.
5. AI-generated summaries.

AI-generated summaries are never primary sources.

## Engineering Rigor

Technical claims must state conditions when conditions matter.

Examples:

- Phase noise to jitter requires carrier frequency and integration bandwidth.
- LDO PSRR depends on frequency, load, topology, and operating point.
- ADC jitter SNR formulas for sine waves need caveats for PAM4 receiver waveforms.
- PAM4 bit-rate benefit must be distinguished from symbol rate and vertical margin cost.

## Formula Quality

See [../formula_style.md](../formula_style.md).

Gate:

- No important formula should appear without symbol definitions, units, assumptions, and validity limits.

## Markdown Quality

See [../obsidian_style.md](../obsidian_style.md).

Gate:

- Markdown must be readable in Obsidian, Git, and plain text.

## Link and Index Quality

See:

- [../build_links.md](../build_links.md)
- [../indexing.md](../indexing.md)

Gate:

- Important notes should not be orphaned.
- Indexes should curate canonical notes rather than list every file.

## Review Quality

See [../review.md](../review.md).

Gate:

- Reviews must identify actionable issues by severity.
- If no issues are found, residual risk must still be stated.

## Interview Quality

A strong interview answer:

- Starts from system impact.
- Explains mechanism.
- Includes a tradeoff.
- Includes a practical check.
- Links to deep technical notes.
- Does not exaggerate user experience.

## Quality Checklist

Before finishing an edit:

- Correct folder?
- Source recorded?
- Uncertainty visible?
- Assumptions stated?
- Units included?
- Links checked?
- No confidential material promoted?
- Index updated if needed?
- Verification limits reported?

