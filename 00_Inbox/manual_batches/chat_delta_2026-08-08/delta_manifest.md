# ChatGPT Export Delta Manifest - 2026-08-08

Stage: delta extraction only. No ingest, canonical-note promotion, or master-inventory update was performed.

## Sources

- New export: `00_Inbox/raw_chat_exports/chatgpt-export-2026-08-08.zip`
- Authoritative baseline: `00_Inbox/raw_chat_exports/chatgpt_export_2026-07-01/`
- Inventory reference: `00_Inbox/conversation_inventory/raw_conversation_list.md`

## Counts

| Delta class | Count |
|---|---:|
| Entirely new conversations | 133 |
| Updated existing conversations | 8 |
| Genuinely new messages | 3016 |
| Materially edited existing messages | 0 |
| Messages requiring later ingest review | 3016 |
| Unchanged conversations skipped | 512 |
| Old-only conversations | 5 |
| Old-only messages | 78 |
| Ambiguous items | 2 |

All old-only records are marked `historical_missing_from_latest`; no deletion is inferred or performed.
