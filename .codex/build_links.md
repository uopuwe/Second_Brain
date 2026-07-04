# Build Links Workflow

## Purpose

Use this workflow to improve navigation through the vault.
Global link quality standards are in [core/quality_standards.md](core/quality_standards.md).
Vault structure is defined in [knowledge_tree.md](knowledge_tree.md) and the scalable architecture in [knowledge_architecture.md](knowledge_architecture.md).
Continuous improvement may route link gaps and cross-link optimization work here from [continuous_knowledge_improvement.md](continuous_knowledge_improvement.md).

## Active Roles

- Librarian: links, backlinks, source trails.
- Knowledge architect: canonical targets.
- Editor: link text clarity.

## Link Types

- Parent links: detailed note to index or overview.
- Child links: overview to detailed notes.
- Sibling links: related notes at the same level.
- Source links: durable notes to source material.
- Application links: technical notes to interview, career, or design notes.

## Workflow

1. Read the target note.
2. Identify primary domain and abstraction level.
3. Search for existing canonical related notes.
4. Add a curated related-notes section if useful.
5. Use relative Markdown links for durable links.
6. Add source links when claims depend on source material.
7. Add index links for major notes using [indexing.md](indexing.md).
8. Return link decisions to [continuous_knowledge_improvement.md](continuous_knowledge_improvement.md) when link work is part of a post-ingest improvement pass.
8. Check that targets exist.
9. Avoid duplicate-folder targets unless intentional.

## Good Example

```markdown
## Related Notes

- SerDes architecture overview: `../SerDes/serdes_architecture_overview.md`
- PLL phase noise and jitter: `../PLL_CDR_Clocking/pll_phase_noise_jitter.md`
- Sampling jitter in ADCs: `../ADC/sampling_jitter_adc.md`
```

## Bad Example

```markdown
See vague links such as `here`, ambiguous wikilinks such as `stuff`, and missing targets such as `missing.md`.
```

## Edge Cases

- If a useful target does not exist, list it as a future note in inline code instead of a broken link.
- If two targets exist, prefer the canonical one from the index.
- If a note already uses wikilinks consistently, do not rewrite unrelated links.
- If link density becomes high, group links by purpose.

## Output Contract

Link work should leave important notes easier to navigate without creating broken links or noisy link walls.
