# Indexing Workflow

## Purpose

Use this workflow to maintain curated indexes.
Quality standards are in [core/quality_standards.md](core/quality_standards.md).
The vault tree is in [knowledge_tree.md](knowledge_tree.md).
Repository-scale index architecture is in [knowledge_architecture.md](knowledge_architecture.md).
Continuous post-ingest improvement signals are defined in [continuous_knowledge_improvement.md](continuous_knowledge_improvement.md).

## Active Roles

- Librarian: retrieval paths and source inventories.
- Knowledge architect: canonical notes and folder boundaries.
- Editor: concise index descriptions.

## Primary Indexes

The current technical index is:

```text
01_AnalogIC_SerDes/analog_ic_serdes_master_index.md
```

The scalable index layer is:

```text
70_Indexes/
```

## Workflow

1. Identify changed or new notes.
2. Decide whether they are index-worthy.
3. Determine domain and canonical status.
4. Check lifecycle state from [knowledge_evolution.md](knowledge_evolution.md).
5. Check quality band from [quality_score.md](quality_score.md) when available.
6. Check open gaps from [knowledge_gap.md](knowledge_gap.md).
7. Check roadmap relevance from [research_roadmap.md](research_roadmap.md).
8. Check CKI outputs from [continuous_knowledge_improvement.md](continuous_knowledge_improvement.md), especially canonical-note decisions, duplicate candidates, link gaps, formula-improvement status, interview-question outputs, reading recommendations, and density concerns.
9. Add concise entries with descriptions.
10. Add read-first order when useful.
11. Mark canonical notes when duplicates exist.
12. Track source batches separately from durable topic notes.
13. Track archived source packets only through source indexes or reports, not as durable knowledge.
14. Check relative links.
15. Keep the index concise enough to scan.

## Good Entry

```markdown
- PLL phase noise and jitter: `PLL_CDR_Clocking/pll_phase_noise_jitter.md`
  - Scope: phase-noise sources, integration to RMS jitter, and SerDes clocking implications.
```

## Bad Entry

```markdown
- jitter.md
```

## Edge Cases

- If a domain grows too large, create a folder index and keep the master index curated.
- If a note is immature but important, label it as a seed or active note.
- If a duplicate remains, mark the canonical note clearly.
- If a source batch was reviewed but not promoted, index the report rather than treating the source as durable knowledge.
- If a roadmap item depends on an immature note, index the roadmap item separately from the note's canonical technical entry.
- If a gap remains open, do not present the related note as mature without caveat.
- If CKI identifies duplicate candidates, expose the canonical note and avoid indexing every duplicate as equally authoritative.
- If CKI generates reading recommendations or interview questions, index them only when they support a durable study path or career objective.

## Output Contract

Indexes should answer what to read first, which note is canonical, where the topic lives, and what is source material versus durable knowledge.
Indexes should also expose lifecycle status, quality maturity, major open gaps, roadmap relevance, CKI outcomes, reading recommendations, interview artifacts, and archive/report traceability when those fields affect future navigation.
