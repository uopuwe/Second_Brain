# Ingest Workflow

## Purpose

Use this workflow when bringing new external knowledge material into the vault.
Global policy is in [core/mandatory_rules.md](core/mandatory_rules.md).
Quality gates are in [core/quality_standards.md](core/quality_standards.md).
The end-to-end source pipeline is defined in [knowledge_ingestion_pipeline.md](knowledge_ingestion_pipeline.md).

For normal knowledge ingestion, the default inbox root is `00_Inbox/incoming/`.
The phrase "ingest everything in `00_Inbox`" means ingest only `00_Inbox/incoming/` unless the user explicitly names a legacy ChatGPT or conversation-processing folder.

## Active Roles

- Researcher: source quality and verification status.
- Librarian: source preservation and traceability.
- Knowledge architect: destination selection.
- Analog IC expert: technical screening.

Role responsibilities are defined in [core/roles.md](core/roles.md).

## Inputs

This workflow applies by default to external knowledge material placed under `00_Inbox/incoming/`, including papers, books, articles, screenshots, videos, datasheets, patents, slides, technical references, interview notes, work or design notes, and Python analysis snippets.

ChatGPT exports, conversation inventories, processed ChatGPT summaries, historical manual batches, and unprocessed conversation notes use the separate conversation-processing workflow and require explicit user instruction before processing.

## Ingest Level

Every normal external knowledge ingest must run in one of three levels.
If the user does not specify a level, use Balanced Ingest.

Ingest level controls extraction depth, merge depth, report length, and token budget.
It does not change the canonical-note rule, inbox-lane safety rule, provenance requirement, bilingual writing requirement, or archive requirement.

### Fast Ingest

Use Fast Ingest for blogs, short articles, Reddit/forum discussions, screenshots, simple slides, quick web captures, and lightweight references.

Purpose:

- Minimize token use.
- Preserve source provenance.
- Extract only the material that is clearly useful.
- Avoid turning low-density sources into large note expansions.

Required actions:

- Extract title, source, date if available, topic, short summary, key claims, useful links, and relevance.
- Search for an existing canonical note before creating anything.
- Update an existing canonical note only when the source contains clearly reusable knowledge.
- Preserve source provenance in any note touched.
- Archive the source after processing.
- Generate a short ingest report.

Limits:

- Do not expand derivations.
- Do not generate long interview sections.
- Do not deeply rewrite existing notes.
- Do not update indexes or MOCs unless a small link repair or obvious index entry is needed.
- Do not create duplicate notes when a canonical note already exists.

Good Fast Ingest examples:

- A Reddit discussion with one useful lab-debug heuristic for reference-clock termination.
- A screenshot of a conference slide showing an ADC timing-skew taxonomy.
- A short blog post explaining a useful Python plotting trick for jitter histograms.

Bad Fast Ingest behavior:

- Expanding a full PLL handbook from a two-page blog post.
- Creating a new `ring_vco_phase_noise.md` note when `pll_phase_noise_jitter.md` already covers the canonical topic.
- Spending deep-study effort on a source whose only durable value is one link and one caution.

### Balanced Ingest

Balanced Ingest is the default mode.
Use it for ordinary papers, whitepapers, datasheets, technical articles, useful slide decks, and moderate-size sources.

Purpose:

- Extract reusable engineering knowledge.
- Merge high-value material into existing canonical notes.
- Keep note growth disciplined.
- Capture formulas and insights without turning every source into a full study project.

Required actions:

- Classify the topic and source type.
- Identify existing canonical notes before creating any new note.
- Merge only high-value material into existing canonical notes.
- Extract important formulas into Markdown LaTeX.
- Expand only important omitted derivations.
- Add concise engineering insights, assumptions, limitations, and design implications.
- Add Obsidian links where they improve retrieval.
- Update indexes and MOCs only when useful.
- Preserve source provenance.
- Archive the source after successful ingestion.
- Generate a normal ingest report.

Limits:

- Do not deeply rewrite large sections unless the source materially improves them.
- Do not create long interview sections unless the source directly supports interview-quality knowledge.
- Do not update every related note just because a link could exist.
- Do not use Deep Ingest behavior unless the user requested it or approved it.

Good Balanced Ingest examples:

- A JSSC paper with two formulas, one design tradeoff, and one measurement caution that belong in an existing PLL note.
- A datasheet that improves an LDO noise or ADC reference-drive note with practical limits.
- A technical article that adds a compact DSP equalization insight and a source link.

Bad Balanced Ingest behavior:

- Copying a paper section-by-section into Markdown.
- Expanding every equation in a source when only one is central to the vault.
- Creating parallel source notes that duplicate canonical notes.

### Deep Ingest

Use Deep Ingest only for high-value sources such as textbooks, PCIe specifications, cornerstone papers, important JSSC/ISSCC papers, or explicit deep-study requests from the user.

Purpose:

- Perform full technical extraction.
- Build durable engineering understanding, not just a summary.
- Update every relevant canonical note that materially benefits from the source.
- Preserve detailed derivations, tradeoffs, examples, mistakes, and implementation guidance.

Required actions:

- Perform full source triage and technical extraction.
- Extract and explain formulas carefully in Markdown LaTeX.
- Expand derivations when they teach reusable engineering reasoning.
- Add engineering tradeoffs, common mistakes, examples, interview questions, implementation notes, and verification implications.
- Update all relevant canonical notes while preserving the one-topic-one-canonical-note rule.
- Update indexes, MOCs, and source trails when knowledge graph structure changes.
- Record gaps and roadmap implications.
- Generate a detailed ingest report.

Limits and safety rules:

- Never use Deep Ingest by default.
- If the source is very large, such as a full book, long specification, or multi-hundred-page standard, ask before using Deep Ingest unless the user explicitly requested it.
- Do not create duplicate handbook files when canonical notes already exist.
- Do not promote unverifiable or copyrighted long passages into durable notes.
- Higher token use is acceptable only when the source value justifies it.

Good Deep Ingest examples:

- A PCIe specification chapter that affects clocking, jitter tolerance, equalization, and compliance terminology.
- A cornerstone JSSC/ISSCC paper that should update PLL, CDR, ADC, and SerDes verification notes.
- A textbook chapter on sampled-data noise that needs formulas, derivations, examples, and interview questions.

Bad Deep Ingest behavior:

- Deep-processing every blog post by default.
- Asking no confirmation before deeply processing a full book.
- Rebuilding the repository architecture because one source is broad.

## Workflow

The ingest workflow is no longer complete when content is merely promoted.
Every source-processing task follows this chain:

```text
Capture
  -> Ingest
  -> Knowledge Evolution
  -> Quality Evaluation
  -> Gap Analysis
  -> Research Roadmap
  -> Continuous Knowledge Improvement
  -> Archive
  -> Report
```

1. Capture new external source material in `00_Inbox/incoming/` according to [knowledge_ingestion_pipeline.md](knowledge_ingestion_pipeline.md).
2. Select and record the ingest level: Fast Ingest, Balanced Ingest, or Deep Ingest. Use Balanced Ingest when unspecified.
3. Inventory source path, source type, date if known, domains, and sensitivity.
4. Search for existing canonical notes before creating new files.
5. Classify fragments as concept, equation, tradeoff, debug, interview, source, career, raw, or not promoted.
6. Screen technical claims for assumptions, units, source quality, and confidentiality.
7. Choose destination using [knowledge_tree.md](knowledge_tree.md) and [knowledge_architecture.md](knowledge_architecture.md).
8. Promote only durable content into domain notes at the depth allowed by the selected ingest level.
9. Write newly added or substantially rewritten explanatory content using the bilingual ingest writing standard: Chinese paragraph first, matching English paragraph immediately after.
10. Record provenance in every destination note touched.
11. Apply [knowledge_evolution.md](knowledge_evolution.md) to decide whether each output is a reference note, seed note, active permanent note, MOC candidate, handbook candidate, superseded item, or archive-only source.
12. Apply [quality_score.md](quality_score.md) to durable notes that were created, substantially changed, or proposed for maturity.
13. Apply [knowledge_gap.md](knowledge_gap.md) to record unresolved source, equation, standards, link, tradeoff, debug, or synthesis gaps.
14. Apply [research_roadmap.md](research_roadmap.md) when a gap is high-priority, multi-note, source-dependent, or relevant to SerDes/PCIe7/PLL/CDR/ADC/LDO/DSP study direction.
15. Apply [continuous_knowledge_improvement.md](continuous_knowledge_improvement.md) to run the automatic post-ingest improvement pass at a depth consistent with the selected ingest level: minimal for Fast, normal for Balanced, detailed for Deep.
16. Add links using [build_links.md](build_links.md) when promoted material affects related notes or CKI identifies missing graph edges.
17. Update indexes using [indexing.md](indexing.md) when notes become canonical, mature, MOC-worthy, source-index-worthy, roadmap-relevant, or CKI identifies retrieval gaps.
18. Archive completed source packets according to [knowledge_ingestion_pipeline.md](knowledge_ingestion_pipeline.md) only after CKI status is recorded.
19. Write an ingest report using [core/template_contracts.md](core/template_contracts.md): short for Fast, normal for Balanced, detailed for Deep. The legacy path [reports/ingest_report_template.md](reports/ingest_report_template.md) remains available for compatibility.
20. Verify against [core/quality_standards.md](core/quality_standards.md).

## Destination Rules

- New papers: `00_Inbox/incoming/papers/`
- New books: `00_Inbox/incoming/books/`
- New articles and blog posts: `00_Inbox/incoming/articles/`
- New screenshots and images: `00_Inbox/incoming/screenshots/`
- New videos and transcripts: `00_Inbox/incoming/videos/`
- New datasheets: `00_Inbox/incoming/datasheets/`
- New patents: `00_Inbox/incoming/patents/`
- New slide decks: `00_Inbox/incoming/slides/`
- New uncategorized external material: `00_Inbox/incoming/misc/`
- Legacy raw chat exports, explicit workflow only: `00_Inbox/raw_chat_exports/`
- Legacy manual source packets, explicit workflow only: `00_Inbox/manual_batches/`
- Legacy processed ChatGPT summaries, explicit workflow only: `00_Inbox/processed_by_chatgpt/`
- Legacy conversation inventories, explicit workflow only: `00_Inbox/conversation_inventory/`
- Legacy unprocessed conversation notes, explicit workflow only: `00_Inbox/unprocessed_notes/`
- Durable technical notes: `01_AnalogIC_SerDes/`
- Work context: `02_Synopsys_Work/`
- Agent operating documents: `.codex/`
- Completed source packets: `90_Archive/`

## Inbox Lane Rules

- `00_Inbox/incoming/` is the only default scan target for new external knowledge ingestion.
- `00_Inbox/conversation_inventory/`, `00_Inbox/manual_batches/`, `00_Inbox/processed_by_chatgpt/`, `00_Inbox/raw_chat_exports/`, and `00_Inbox/unprocessed_notes/` are legacy ChatGPT export and conversation-processing lanes.
- Normal paper, book, article, screenshot, video, datasheet, patent, slide, or technical-reference ingestion must never scan legacy chat-processing folders.
- ChatGPT export ingestion must be requested explicitly and handled as conversation processing, not as default external knowledge ingestion.
- If the user says "ingest inbox" without clarification, process `00_Inbox/incoming/` only.
- If relevant files are found only in legacy folders, ask for confirmation before processing them.
- During normal incoming ingestion, do not archive, move, delete, merge, or repurpose files from legacy chat-processing folders.

## Bilingual Writing Rules

- Durable note content added during ingest must be paragraph-level bilingual: Chinese first, English second.
- The English paragraph should be a precise technical counterpart, not a loose summary.
- The Chinese paragraph should be natural engineering Chinese, not a literal machine translation.
- Do not duplicate YAML frontmatter, file paths, source tables, code blocks, equations, or short link lists solely for bilingual format.
- For formulas, write the surrounding explanation, assumptions, symbol meanings, and engineering implication bilingually.
- For tables, either use bilingual column labels or add bilingual text before and after the table.
- Existing legacy text can remain as-is unless the ingest substantially rewrites it.
- If a paragraph is touched during ingest, leave it in bilingual-pair form before completing the task.

Good bilingual ingest update:

```markdown
中文：数字时钟分布中的 threshold noise 会通过输入边沿斜率转换成采样时间误差；因此低摆幅或低 slew-rate 的参考时钟更容易出现 jitter 或 chatter。

English: Threshold noise in digital clock distribution converts through input edge slew rate into sampling-time error, so low-amplitude or low-slew-rate reference clocks are more vulnerable to jitter or chatter.
```

Bad ingest update:

```markdown
Threshold noise causes jitter.
```

## Good Example

```markdown
Source packet about PCIe 7.0 clocking is preserved under `00_Inbox/incoming/papers/` or `00_Inbox/incoming/slides/`.
Durable clocking concepts are promoted to `01_AnalogIC_SerDes/PLL_CDR_Clocking/pcie7_clocking_notes.md`.
Exact compliance numbers remain marked as requiring current primary-source verification.
```

## Bad Example

```markdown
A full AI conversation is pasted into a PLL note and treated as source-backed technical truth.
```

```markdown
The user says "ingest inbox", and the assistant scans `00_Inbox/raw_chat_exports/` without explicit confirmation.
```

## Edge Cases

- If a source contains confidential work details, generalize the learning and do not promote sensitive identifiers.
- If a source conflicts with an existing note, record the conflict instead of silently overwriting.
- If a source has no durable value, preserve or report it without promoting content.
- If exact standards numbers appear, promote only when source and conditions are clear.

## Output Contract

An ingest task should produce one or more of updated durable notes, source-specific notes, a source inventory, an ingest report, links, index entries, CKI actions, or CKI metrics.
Final response must include changed files, lifecycle decisions, quality evaluation, gap decisions, roadmap decisions, continuous improvement actions, archive actions, and verification limits.
