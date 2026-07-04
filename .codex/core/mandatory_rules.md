# Mandatory Rules

## Purpose

These are non-negotiable rules for every future Codex session in this repository.
Recommendations live in [recommendations.md](recommendations.md).
Quality gates live in [quality_standards.md](quality_standards.md).

## Rules

1. Preserve user work. Do not delete, overwrite, revert, or reorganize user-created content unless explicitly requested.
2. Read before editing. Inspect the target file, relevant nearby files, the matching workflow, and applicable quality standard.
3. Keep raw sources separate. New external knowledge material belongs in `00_Inbox/incoming/`; legacy ChatGPT exports and conversation-processing material must remain in their existing `00_Inbox/` legacy folders unless explicitly processed.
4. Preserve provenance. Durable notes must identify source history, source quality, and verification status.
5. Mark uncertainty. Do not make unverified claims sound certain.
6. Do not invent sources, citations, standards requirements, paper results, employer details, measurement conditions, or user experience.
7. Protect confidentiality. Do not promote employer-confidential, customer, proprietary, unreleased, or sensitive personal information into general technical notes.
8. Use canonical paths. Route knowledge according to [../knowledge_tree.md](../knowledge_tree.md) and the scalable architecture in [../knowledge_architecture.md](../knowledge_architecture.md).
9. Apply the normal knowledge workflow for source-processing or durable-knowledge changes: capture, ingest, knowledge evolution, quality evaluation, gap analysis, research roadmap, continuous knowledge improvement, archive, report.
10. Separate workflow from quality. Do not duplicate global quality policy in workflow files.
11. Use engineering rigor. State assumptions, units, approximations, topology limits, and system impact.
12. Make formulas usable. Follow [../formula_style.md](../formula_style.md).
13. Reviews must lead with findings. Follow [../review.md](../review.md).
14. Do not create broken knowledge graphs. Follow [../build_links.md](../build_links.md).
15. Keep Markdown durable. Follow [../obsidian_style.md](../obsidian_style.md).
16. Report verification limits in final responses after vault edits.
17. During normal incoming ingestion, never archive, move, delete, merge, or repurpose files from legacy chat-processing folders: `00_Inbox/conversation_inventory/`, `00_Inbox/manual_batches/`, `00_Inbox/processed_by_chatgpt/`, `00_Inbox/raw_chat_exports/`, or `00_Inbox/unprocessed_notes/`.
18. During ingest, newly added or substantially rewritten durable explanatory content must use paragraph-level Chinese-English bilingual pairs unless the content is YAML frontmatter, a formula, code, path list, source table, or short navigation list.
19. Every normal external knowledge ingest must run in exactly one ingest level: Fast Ingest, Balanced Ingest, or Deep Ingest.
20. If the user does not specify an ingest level, use Balanced Ingest.
21. Never use Deep Ingest by default. For very large sources such as full books, long specifications, or multi-hundred-page standards, ask before using Deep Ingest unless the user explicitly requested it.
22. Ingest level changes the depth of extraction and reporting, not the repository architecture, canonical-note merge rule, provenance rule, bilingual writing rule, archive rule, or inbox lane safety rule.
23. Normal ingest must scan only `00_Inbox/incoming/`; ChatGPT export and conversation-processing workflows remain separate explicit workflows.

## Conflict Resolution

If rules conflict:

1. The user's latest explicit instruction wins unless it would destroy user work or violate confidentiality.
2. Mandatory rules win over recommendations.
3. Core rules win over specialized workflow text.
4. Source-backed facts win over AI-generated summaries.

## Mandatory Completion Gate

Before finishing edits, confirm:

- User work was preserved.
- Source trail was preserved or explicitly not applicable.
- Lifecycle status was evaluated for durable knowledge changes.
- Quality score or quality evaluation was performed when notes were created, substantially changed, or matured.
- Knowledge gaps were opened, closed, or explicitly not found.
- Roadmap impact was evaluated.
- Continuous knowledge improvement was applied or explicitly not needed.
- Archive action was completed or explicitly not needed.
- Bilingual paragraph format was applied to durable explanatory content added or substantially rewritten during ingest.
- Ingest level was selected, recorded, and applied; Balanced Ingest was used when unspecified.
- Technical uncertainty is visible.
- Links and indexes were updated when required.
- Verification limits are stated.
