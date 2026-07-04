# Indexing Workflow

## Purpose

Use this workflow to maintain curated indexes.
Quality standards are in [core/quality_standards.md](core/quality_standards.md).
The vault tree is in [knowledge_tree.md](knowledge_tree.md).

## Active Roles

- Librarian: retrieval paths and source inventories.
- Knowledge architect: canonical notes and folder boundaries.
- Editor: concise index descriptions.

## Primary Index

The main technical index is:

```text
01_AnalogIC_SerDes/analog_ic_serdes_master_index.md
```

## Workflow

1. Identify changed or new notes.
2. Decide whether they are index-worthy.
3. Determine domain and canonical status.
4. Add concise entries with descriptions.
5. Add read-first order when useful.
6. Mark canonical notes when duplicates exist.
7. Track source batches separately from durable topic notes.
8. Check relative links.
9. Keep the index concise enough to scan.

## Good Entry

```markdown
- [PLL phase noise and jitter](PLL_CDR_Clocking/pll_phase_noise_jitter.md): Phase-noise sources, integration to RMS jitter, and SerDes clocking implications.
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

## Output Contract

Indexes should answer what to read first, which note is canonical, where the topic lives, and what is source material versus durable knowledge.

