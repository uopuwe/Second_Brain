# ChatGPT Export Comparison Report - 2026-08-08

## Scope and Results

This is Stage 1 delta extraction only. Exactly six July shards (525 conversations) and seven August ZIP shards (653 conversations) were compared. Results: 133 entirely new conversations, 8 updated conversations, 512 unchanged common conversations, 5 old-only conversations, 3016 genuinely new messages, 0 materially edited messages, 78 old-only messages, and 2 ambiguous items.

## Exact Comparison Algorithm

Conversations were indexed by stable ID, requiring `id` and `conversation_id` to agree when both occur. Common conversations were compared by `update_time`, stable message IDs, message creation timestamps, and normalized-payload SHA-256. New IDs are genuinely new; common IDs with different material hashes are edited; creation-time-only changes are ambiguous. Existing conversations are updated only if they contain a new or materially edited message. Every message-bearing mapping node is included, not merely the `current_node` path. Old-only records remain non-destructive `historical_missing_from_latest` items.

## Normalization and Hashing

Hashes are SHA-256 of canonical UTF-8 JSON with sorted dictionary keys, compact separators, preserved Unicode, and preserved list order. The payload preserves role, author name, the full structured content object, textual content, ordered parts, code/structured content, and meaningful attachments, file references, citations, image results, search-result groups, targeted-reply fields, and automation title.

IDs and creation timestamps are excluded from the hash because they are compared independently. Volatile export/rendering fields are excluded: model slug, parent ID, serialization metadata, tool icons, view state, locale/voice display flags, nested timestamp-like fields, and `content_references.result_source`. The July-to-August `result_source` removals are search/export provenance drift and do not change semantic message content. Excluding them corrected 153 false edit candidates to zero material edits; the genuinely new-message count remained 3,016.

## Project Membership

Conversation keys and message metadata were searched case-insensitively for project-like fields. None were present in either observed export schema. Project association is therefore recorded as `null`; it was not inferred from titles or content.

## Branches and Context

All message-bearing nodes in each `mapping` were compared, including alternate or detached paths. No observed August node exposed multiple child links. Updated-conversation extracts include only delta messages plus at most one immediate non-delta parent identified through `metadata.parent_id`; context entries are not counted as delta records.

## Hidden, System, and Tool Messages

All message-bearing nodes are retained. Observed author roles were `user` and `assistant`; no separate system/tool author roles occurred. `thoughts`, `reasoning_recap`, and `user_editable_context` are labeled `hidden_or_internal`; `text` and `multimodal_text` are labeled `display_content`. Structural mapping nodes without a message are not treated as malformed.

## Schema Differences and Ambiguities

Top-level conversation keys are unchanged between exports. July keys: `conversation_id, conversation_template_id, create_time, current_node, default_model_slug, id, is_archived, is_do_not_remember, is_read_only, is_starred, is_study_mode, mapping, memory_scope, pinned_time, plugin_ids, title, update_time, voice`. August keys: `conversation_id, conversation_template_id, create_time, current_node, default_model_slug, id, is_archived, is_do_not_remember, is_read_only, is_starred, is_study_mode, mapping, memory_scope, pinned_time, plugin_ids, title, update_time, voice`. August adds a seventh shard and additional heterogeneous payload records. Search citation metadata shows non-semantic normalization drift, specifically removal of `result_source` fields.

Ambiguous records are stored individually under `ambiguous_items/`. Update-time-only or creation-time-only differences are not promoted to material edits. Old-only absence remains unresolved historical state and is never interpreted as deletion. No content-worthiness judgment was made.

## Preservation and Validation

Input hashes were captured before generation and rechecked afterward. The generator wrote only under `00_Inbox/manual_batches/chat_delta_2026-08-08/`; it did not scan `00_Inbox/incoming/` or modify exports, inventories, canonical notes, MOCs, indexes, architecture, or `processed_by_chatgpt`.
