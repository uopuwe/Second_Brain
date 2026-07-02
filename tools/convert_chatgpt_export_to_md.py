#!/usr/bin/env python3
"""Convert ChatGPT export conversations into one Markdown file per conversation."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_INPUT_DIR = Path("00_Inbox/raw_chat_exports/chatgpt_export_2026-07-01")
DEFAULT_OUTPUT_DIR = DEFAULT_INPUT_DIR / "md_by_conversation"
DEFAULT_INVENTORY = Path("00_Inbox/conversation_inventory/raw_conversation_list.md")
DEFAULT_REPORT = Path("00_Inbox/conversation_inventory/conversion_report_2026-07-01.md")

WINDOWS_INVALID_FILENAME_CHARS = r'<>:"/\|?*'
MAX_SAFE_TITLE_LENGTH = 120
MAX_FILENAME_LENGTH = 180
VISIBLE_ROLES = {"user": "User", "assistant": "Assistant"}
NON_TEXT_PLACEHOLDER = "[Non-text content omitted]"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert ChatGPT conversations.json or conversations-*.json exports to Markdown."
    )
    parser.add_argument("--input-dir", type=Path, default=DEFAULT_INPUT_DIR)
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--inventory", type=Path, default=DEFAULT_INVENTORY)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def detect_input_files(input_dir: Path) -> list[Path]:
    single_file = input_dir / "conversations.json"
    split_files = sorted(input_dir.glob("conversations-*.json"), key=lambda path: path.name)

    if split_files:
        return split_files
    if single_file.exists():
        return [single_file]
    raise FileNotFoundError(
        f"No ChatGPT conversation export files found in {input_dir}: "
        "expected conversations.json or conversations-*.json"
    )


def load_conversations(paths: list[Path]) -> tuple[list[dict[str, Any]], list[str]]:
    conversations: list[dict[str, Any]] = []
    problems: list[str] = []

    for path in paths:
        try:
            with path.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
        except Exception as exc:  # noqa: BLE001 - report and continue with other split files.
            problems.append(f"{path.name}: failed to read JSON ({exc})")
            continue

        if isinstance(data, list):
            records = data
        elif isinstance(data, dict) and isinstance(data.get("conversations"), list):
            records = data["conversations"]
        else:
            problems.append(f"{path.name}: JSON did not contain a conversation list")
            continue

        for index, record in enumerate(records, start=1):
            if isinstance(record, dict) and isinstance(record.get("mapping"), dict):
                conversations.append(record)
            else:
                problems.append(f"{path.name} record {index}: skipped non-conversation record")

    return conversations, problems


def timestamp_to_datetime(value: Any) -> str:
    if value in (None, ""):
        return ""
    if isinstance(value, (int, float)):
        try:
            return datetime.fromtimestamp(value, tz=timezone.utc).isoformat()
        except (OverflowError, OSError, ValueError):
            return str(value)
    if isinstance(value, str):
        return value
    return str(value)


def date_prefix(conversation: dict[str, Any]) -> str:
    value = conversation.get("create_time") or conversation.get("update_time")
    if isinstance(value, (int, float)):
        try:
            return datetime.fromtimestamp(value, tz=timezone.utc).strftime("%Y-%m-%d")
        except (OverflowError, OSError, ValueError):
            return "unknown-date"
    if isinstance(value, str):
        match = re.search(r"\d{4}-\d{2}-\d{2}", value)
        if match:
            return match.group(0)
    return "unknown-date"


def conversation_id(conversation: dict[str, Any]) -> str:
    for key in ("conversation_id", "id"):
        value = conversation.get(key)
        if value not in (None, ""):
            return str(value)
    return ""


def conversation_title(conversation: dict[str, Any]) -> str:
    title = conversation.get("title")
    if isinstance(title, str) and title.strip():
        return title.strip()
    return "untitled_conversation"


def sanitize_filename_part(value: str, max_length: int = MAX_SAFE_TITLE_LENGTH) -> str:
    translation = {ord(char): "" for char in WINDOWS_INVALID_FILENAME_CHARS}
    value = value.translate(translation)
    value = re.sub(r"[\x00-\x1f]", "", value)
    value = re.sub(r"\s+", "_", value.strip())
    value = re.sub(r"_+", "_", value)
    value = value.strip(" ._")
    if not value:
        value = "untitled_conversation"
    return value[:max_length].rstrip(" ._") or "untitled_conversation"


def unique_markdown_filename(
    prefix: str, safe_title: str, used_names: set[str], max_length: int = MAX_FILENAME_LENGTH
) -> str:
    base = f"{prefix}__{safe_title}"
    max_base_length = max_length - len(".md")
    base = base[:max_base_length].rstrip(" ._")
    name = f"{base}.md"
    counter = 2

    while name.lower() in used_names:
        suffix = f"_{counter}"
        trimmed_base = base[: max_base_length - len(suffix)].rstrip(" ._")
        name = f"{trimmed_base}{suffix}.md"
        counter += 1

    used_names.add(name.lower())
    return name


def yaml_quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"').replace("\r", " ").replace("\n", " ") + '"'


def markdown_escape_table(value: str) -> str:
    return value.replace("\\", "\\\\").replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def clean_text(value: str) -> str:
    value = value.replace("\r\n", "\n").replace("\r", "\n")
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def text_from_part(part: Any) -> tuple[str, bool]:
    if isinstance(part, str):
        return part, False
    if not isinstance(part, dict):
        return "", True

    for key in ("text", "content", "name"):
        value = part.get(key)
        if isinstance(value, str) and value.strip():
            return value, False

    return "", True


def extract_text_from_content(content: Any) -> tuple[str, bool]:
    if not isinstance(content, dict):
        return "", True

    content_type = content.get("content_type")
    parts = content.get("parts")
    texts: list[str] = []
    saw_non_text = False

    if isinstance(parts, list):
        for part in parts:
            text, non_text = text_from_part(part)
            if text.strip():
                texts.append(text)
            saw_non_text = saw_non_text or non_text

    if not texts:
        for key in ("text", "result", "summary"):
            value = content.get(key)
            if isinstance(value, str) and value.strip():
                texts.append(value)

    if texts:
        return clean_text("\n\n".join(texts)), False

    if content_type and content_type != "text":
        return "", True
    return "", saw_non_text


def visible_message_from_node(node: dict[str, Any]) -> dict[str, Any] | None:
    message = node.get("message")
    if not isinstance(message, dict):
        return None

    author = message.get("author")
    role = author.get("role") if isinstance(author, dict) else None
    if role not in VISIBLE_ROLES:
        return None

    text, non_text = extract_text_from_content(message.get("content"))
    if not text and not non_text:
        return None
    if not text and non_text:
        text = NON_TEXT_PLACEHOLDER

    return {
        "role": VISIBLE_ROLES[role],
        "text": text,
        "create_time": message.get("create_time"),
    }


def node_path_from_current(conversation: dict[str, Any]) -> list[dict[str, Any]]:
    mapping = conversation.get("mapping")
    if not isinstance(mapping, dict):
        return []

    current_node = conversation.get("current_node")
    if not current_node or current_node not in mapping:
        return []

    path: list[dict[str, Any]] = []
    seen: set[str] = set()
    node_id = current_node

    while node_id and node_id in mapping and node_id not in seen:
        seen.add(node_id)
        node = mapping[node_id]
        if isinstance(node, dict):
            path.append(node)
            node_id = node.get("parent")
        else:
            break

    return list(reversed(path))


def fallback_traversal_nodes(conversation: dict[str, Any]) -> list[dict[str, Any]]:
    mapping = conversation.get("mapping")
    if not isinstance(mapping, dict):
        return []

    roots: list[str] = []
    children_by_parent: dict[str, list[str]] = {}
    node_ids = set(mapping.keys())

    for node_id, node in mapping.items():
        if not isinstance(node, dict):
            continue
        parent = node.get("parent")
        if parent in node_ids:
            children_by_parent.setdefault(parent, []).append(node_id)
        else:
            roots.append(node_id)

    ordered_nodes: list[dict[str, Any]] = []
    seen: set[str] = set()

    def visit(node_id: str) -> None:
        if node_id in seen:
            return
        seen.add(node_id)
        node = mapping.get(node_id)
        if isinstance(node, dict):
            ordered_nodes.append(node)
        for child_id in children_by_parent.get(node_id, []):
            visit(child_id)

    for root_id in roots:
        visit(root_id)
    for node_id in mapping:
        visit(node_id)

    return ordered_nodes


def conversation_messages(conversation: dict[str, Any]) -> list[dict[str, Any]]:
    nodes = node_path_from_current(conversation) or fallback_traversal_nodes(conversation)
    messages: list[dict[str, Any]] = []

    for ordinal, node in enumerate(nodes):
        message = visible_message_from_node(node)
        if message is None:
            continue
        message["ordinal"] = ordinal
        messages.append(message)

    if messages and all(isinstance(message.get("create_time"), (int, float)) for message in messages):
        messages.sort(key=lambda message: (message["create_time"], message["ordinal"]))

    return messages


def render_conversation_markdown(conversation: dict[str, Any], messages: list[dict[str, Any]]) -> str:
    title = conversation_title(conversation)
    front_matter = [
        "---",
        f"title: {yaml_quote(title)}",
        f"created: {yaml_quote(timestamp_to_datetime(conversation.get('create_time')))}",
        f"updated: {yaml_quote(timestamp_to_datetime(conversation.get('update_time')))}",
        'source: "ChatGPT export"',
        f"conversation_id: {yaml_quote(conversation_id(conversation))}",
        "---",
        "",
    ]

    body: list[str] = []
    for message in messages:
        body.extend([f"## {message['role']}", "", message["text"], ""])

    if not body:
        body.extend(["[No user-visible messages found]", ""])

    return "\n".join(front_matter + body).rstrip() + "\n"


def write_inventory(path: Path, rows: list[dict[str, str]]) -> None:
    rows = sorted(rows, key=lambda row: (row["date"], row["title"].lower(), row["markdown_file"]))
    lines = [
        "# Raw Conversation List",
        "",
        "| Date | Title | Markdown File | Conversation ID |",
        "|---|---|---|---|",
    ]

    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_escape_table(row["date"]),
                    markdown_escape_table(row["title"]),
                    markdown_escape_table(row["markdown_file"]),
                    markdown_escape_table(row["conversation_id"]),
                ]
            )
            + " |"
        )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_report(
    path: Path,
    input_files: list[Path],
    conversations_loaded: int,
    markdown_generated: int,
    output_dir: Path,
    problems: list[str],
) -> None:
    lines = [
        "# Conversion Report - 2026-07-01",
        "",
        "## Input Files Detected",
        "",
    ]
    lines.extend(f"- {input_file.as_posix()}" for input_file in input_files)
    lines.extend(
        [
            "",
            "## Summary",
            "",
            f"- Conversations loaded: {conversations_loaded}",
            f"- Markdown files generated: {markdown_generated}",
            f"- Output folder: {output_dir.as_posix()}",
            "",
            "## Skipped or Problematic Conversations",
            "",
        ]
    )
    if problems:
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("- None")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def convert(input_dir: Path, output_dir: Path, inventory_path: Path, report_path: Path) -> None:
    input_files = detect_input_files(input_dir)
    conversations, problems = load_conversations(input_files)

    output_dir.mkdir(parents=True, exist_ok=True)
    used_names: set[str] = set()
    inventory_rows: list[dict[str, str]] = []
    markdown_generated = 0

    for index, conversation in enumerate(conversations, start=1):
        title = conversation_title(conversation)
        prefix = date_prefix(conversation)
        safe_title = sanitize_filename_part(title)
        filename = unique_markdown_filename(prefix, safe_title, used_names)
        output_path = output_dir / filename
        messages = conversation_messages(conversation)

        if not messages:
            problems.append(
                f"conversation {conversation_id(conversation) or index}: no user-visible messages found"
            )

        output_path.write_text(render_conversation_markdown(conversation, messages), encoding="utf-8")
        markdown_generated += 1
        inventory_rows.append(
            {
                "date": prefix,
                "title": title,
                "markdown_file": output_path.as_posix(),
                "conversation_id": conversation_id(conversation),
            }
        )

    write_inventory(inventory_path, inventory_rows)
    write_report(report_path, input_files, len(conversations), markdown_generated, output_dir, problems)

    print(f"Input files detected: {len(input_files)}")
    print(f"Conversations loaded: {len(conversations)}")
    print(f"Markdown files generated: {markdown_generated}")
    print(f"Output folder: {output_dir}")
    print(f"Inventory: {inventory_path}")
    print(f"Report: {report_path}")
    if problems:
        print(f"Skipped/problematic conversations: {len(problems)}")


def main() -> None:
    args = parse_args()
    input_dir = args.input_dir
    output_dir = args.output_dir or input_dir / "md_by_conversation"
    convert(input_dir, output_dir, args.inventory, args.report)


if __name__ == "__main__":
    main()
