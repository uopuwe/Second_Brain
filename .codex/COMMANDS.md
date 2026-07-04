# Second Brain Commands

This file is a quick cheat sheet for using the Second_Brain repository with Codex.
It does not replace the operating manuals.
For detailed rules, follow [AGENTS.md](AGENTS.md), [core/mandatory_rules.md](core/mandatory_rules.md), and the referenced workflow documents.

## Daily Ingest

### Purpose

Process all new files under:

```text
00_Inbox/incoming/
```

Use this for new external knowledge materials such as papers, books, articles, screenshots, videos, datasheets, patents, slides, and miscellaneous technical references.
If no mode is specified, use Balanced Ingest.

### Workflow Reference

- [ingest.md](ingest.md)
- [knowledge_ingestion_pipeline.md](knowledge_ingestion_pipeline.md)
- [continuous_knowledge_improvement.md](continuous_knowledge_improvement.md)

### Fast Ingest Command

```text
Execute the workflow defined in .codex/ingest.md for every file under:

00_Inbox/incoming/

Mode: Fast Ingest.

Follow .codex/AGENTS.md and all mandatory rules.

For every source:

- classify the topic

- identify the existing canonical note

- merge only clearly reusable knowledge into the canonical note

- never create a duplicate note if a canonical note already exists

- extract title, source, date if available, topic, short summary, key claims, and useful links

- minimize token use

- do not expand derivations

- do not generate long interview sections

- do not deeply rewrite existing notes

- preserve source provenance

- archive the original source after processing

Finally generate a short Ingest Report summarizing:

- processed files

- updated canonical notes

- new notes, only if absolutely necessary

- archive actions

- manual review items
```

### Balanced Ingest Command

```text
Execute the workflow defined in .codex/ingest.md for every file under:

00_Inbox/incoming/

Mode: Balanced Ingest.

Follow .codex/AGENTS.md and all mandatory rules.

For every source:

- classify the topic

- identify the existing canonical note

- merge high-value reusable knowledge into the canonical note

- never create a duplicate note if a canonical note already exists

- extract important formulas into Markdown LaTeX

- expand omitted derivations when valuable

- add concise engineering insights

- write durable note updates as paragraph-level Chinese-English bilingual pairs

- update Obsidian links

- update indexes and MOCs when needed

- preserve source provenance

- archive the original source after successful ingestion

Finally generate a normal Ingest Report summarizing:

- processed files

- updated canonical notes

- new notes (if absolutely necessary)

- archive actions

- manual review items
```

### Deep Ingest Command

```text
Execute the workflow defined in .codex/ingest.md for every file under:

00_Inbox/incoming/

Mode: Deep Ingest.

Follow .codex/AGENTS.md and all mandatory rules.

Use Deep Ingest only because this request explicitly asks for it.

For every source:

- classify the topic

- identify every affected existing canonical note

- merge reusable knowledge into the correct canonical notes

- never create a duplicate note if a canonical note already exists

- perform full technical extraction

- extract and explain formulas carefully in Markdown LaTeX

- expand important derivations

- add engineering tradeoffs, common mistakes, examples, interview questions, and implementation notes

- write durable note updates as paragraph-level Chinese-English bilingual pairs

- update Obsidian links

- update indexes and MOCs when useful knowledge graph structure changes

- preserve source provenance

- archive the original source after successful ingestion

Finally generate a detailed Ingest Report summarizing:

- processed files

- updated canonical notes

- new notes, only if absolutely necessary

- formulas and derivations promoted

- index and MOC updates

- archive actions

- manual review items
```

### Expected Outputs

- Updated canonical notes.
- Updated indexes.
- Updated links.
- Archive completed.
- Ingest report.

## Weekly Review

### Purpose

Review the entire vault.
Detect duplicate notes.
Repair links.
Update indexes.
Generate a review report.

### Workflow Reference

- [review.md](review.md)
- [build_links.md](build_links.md)
- [indexing.md](indexing.md)
- [merge_knowledge.md](merge_knowledge.md)

### Command To Copy Into Codex

```text
Execute the workflow defined in .codex/review.md for the Second_Brain vault.

Detect duplicate notes, broken links, weak canonical structure, stale indexes, and unclear source trails.

Apply safe fixes directly.

Generate a concise review report with findings, fixes applied, and remaining risks.
```

### Expected Outputs

- Duplicate candidates identified or merged.
- Broken links repaired.
- Index updates applied.
- Review findings documented.
- Follow-up risks listed.

## Expand Existing Note

### Purpose

Expand one existing canonical note.
Never create another handbook when a canonical note already exists.

### Workflow Reference

- [expand_note.md](expand_note.md)
- [engineering_notes.md](engineering_notes.md)
- [formula_style.md](formula_style.md)

### Command To Copy Into Codex

```text
Execute the workflow defined in .codex/expand_note.md for this existing canonical note:

<paste note path here>

Improve the existing note instead of creating a duplicate note or another handbook.

Add engineering depth, source-aware explanations, formulas, examples, links, and gaps where needed.
```

### Expected Outputs

- Existing canonical note improved.
- Related links updated.
- Formula quality improved when applicable.
- Gaps recorded if knowledge is missing.
- No duplicate handbook or parallel note created.

## Merge Knowledge

### Purpose

Merge new knowledge into existing canonical notes.
Use this when two notes overlap or when new material belongs in an existing note.

### Workflow Reference

- [merge_knowledge.md](merge_knowledge.md)
- [build_links.md](build_links.md)
- [indexing.md](indexing.md)

### Command To Copy Into Codex

```text
Execute the workflow defined in .codex/merge_knowledge.md.

Merge the source material or duplicate note into the existing canonical note.

Preserve provenance.

Do not delete source notes unless explicitly requested.

Update links and indexes.
```

### Expected Outputs

- Canonical note selected.
- Unique useful content merged.
- Source history preserved.
- Links and indexes updated.
- Duplicate or source note left intact unless explicitly directed otherwise.

## Continuous Improvement

### Purpose

Improve note quality after every ingest.
Use this to strengthen the vault after new knowledge has been added.

### Workflow Reference

- [continuous_knowledge_improvement.md](continuous_knowledge_improvement.md)
- [quality_score.md](quality_score.md)
- [knowledge_evolution.md](knowledge_evolution.md)

### Command To Copy Into Codex

```text
Execute the workflow defined in .codex/continuous_knowledge_improvement.md for the notes changed by the latest ingest.

Improve quality, remove duplication, optimize links, improve formulas, expand engineering insight, detect gaps, recommend reading, and update indexes.

Report measurable quality changes and remaining risks.
```

### Expected Outputs

- Improved note quality.
- Duplicate candidates handled or recorded.
- Links and formulas improved.
- Engineering insights expanded.
- Gaps and reading recommendations updated.

## Knowledge Gap

### Purpose

Find missing knowledge.
Recommend future study.

### Workflow Reference

- [knowledge_gap.md](knowledge_gap.md)
- [research_roadmap.md](research_roadmap.md)

### Command To Copy Into Codex

```text
Execute the workflow defined in .codex/knowledge_gap.md for this topic or note:

<paste topic or note path here>

Find missing source evidence, equations, tradeoffs, debug knowledge, links, standards verification, and synthesis gaps.

Recommend future study only where it materially improves the vault.
```

### Expected Outputs

- Gaps identified and classified.
- Immediate fixes applied when safe.
- Roadmap candidates created when needed.
- Missing sources or study needs documented.

## Research Roadmap

### Purpose

Plan future learning.
Use this when gaps need structured study, source acquisition, or long-term learning direction.

### Workflow Reference

- [research_roadmap.md](research_roadmap.md)
- [knowledge_gap.md](knowledge_gap.md)
- [knowledge_architecture.md](knowledge_architecture.md)

### Command To Copy Into Codex

```text
Execute the workflow defined in .codex/research_roadmap.md for this domain or gap cluster:

<paste domain, note path, or gap list here>

Create a prioritized research roadmap with source targets, expected outputs, done criteria, and links to affected notes.
```

### Expected Outputs

- Prioritized research items.
- Source acquisition plan.
- Target notes or MOCs identified.
- Done criteria defined.
- Study outputs tied to vault improvement.

## Repository Principles

One topic

↓

One canonical note.

Never create duplicate handbook files.

Always improve existing notes.

Use `00_Inbox/incoming/` as the default location for new external knowledge ingestion.

Treat ChatGPT exports and conversation batches as explicit separate workflows.

Preserve source provenance.

Prefer better links, clearer formulas, and stronger engineering insight over more files.
