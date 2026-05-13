#!/usr/bin/env python3
"""
Session metrics extractor for agent-framework.

Parses a Claude Code session JSONL file and computes metrics for the
Close Report. Run this at project close before filling in the Metrics
section of the Close Report.

Usage:
    python scripts/metrics.py /path/to/session.jsonl

To find the current session JSONL:
    ls -t ~/.claude/projects/<project-slug>/*.jsonl | head -1

The project slug is the CWD path with slashes replaced by dashes, e.g.:
    /Users/alice/work/my-project -> -Users-alice-work-my-project
"""

import json
import sys
import argparse
from collections import defaultdict
from pathlib import Path


def parse_session(path: Path) -> dict:
    entries = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                entries.append(json.loads(line))
    return entries


def extract_metrics(entries: list) -> dict:
    # --- Token counts ---
    input_tokens = 0
    output_tokens = 0
    cache_read_tokens = 0
    cache_creation_tokens = 0

    # --- Turn counts ---
    user_turns = 0
    assistant_turns = 0

    # --- Tool tracking ---
    tool_calls = []        # list of {name, input}
    tool_results = []      # list of {tool_use_id, is_error, content_preview}

    # Build a map from tool_use_id -> tool info (name, input)
    tool_use_map = {}

    for entry in entries:
        t = entry.get("type")

        if t == "assistant":
            assistant_turns += 1
            msg = entry.get("message", {})

            # Tokens
            usage = msg.get("usage", {})
            input_tokens += usage.get("input_tokens", 0)
            output_tokens += usage.get("output_tokens", 0)
            cache_read_tokens += usage.get("cache_read_input_tokens", 0)
            cache_creation_tokens += usage.get("cache_creation_input_tokens", 0)

            # Tool use blocks
            for block in msg.get("content", []):
                if isinstance(block, dict) and block.get("type") == "tool_use":
                    tool_use_map[block["id"]] = {
                        "name": block.get("name", ""),
                        "input": block.get("input", {}),
                    }
                    tool_calls.append({
                        "id": block["id"],
                        "name": block.get("name", ""),
                        "input": block.get("input", {}),
                    })

        elif t == "user":
            content = entry.get("message", {}).get("content", [])
            if isinstance(content, list) and content:
                user_turns += 1
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "tool_result":
                        is_error = block.get("is_error", False)
                        raw_content = block.get("content", "")
                        if isinstance(raw_content, list):
                            preview = str(raw_content)[:120]
                        else:
                            preview = str(raw_content)[:120]
                        tool_results.append({
                            "tool_use_id": block.get("tool_use_id", ""),
                            "is_error": is_error,
                            "preview": preview,
                        })

    # --- Tool error rate ---
    total_tool_calls = len(tool_results)
    error_results = [r for r in tool_results if r["is_error"]]
    tool_error_count = len(error_results)
    tool_error_rate = (tool_error_count / total_tool_calls * 100) if total_tool_calls else 0

    # --- Error detail: which tools errored ---
    errored_tools = defaultdict(int)
    for r in error_results:
        tid = r["tool_use_id"]
        tool_info = tool_use_map.get(tid, {})
        name = tool_info.get("name", "unknown")
        errored_tools[name] += 1

    # --- Files edited >3x ---
    file_edit_counts = defaultdict(int)
    for call in tool_calls:
        if call["name"] in ("Edit", "Write"):
            fp = call["input"].get("file_path", "")
            if fp:
                file_edit_counts[fp] += 1
    files_over_3 = {fp: n for fp, n in file_edit_counts.items() if n > 3}

    # --- Git errors ---
    git_error_count = 0
    git_errors = []
    for r in error_results:
        tid = r["tool_use_id"]
        tool_info = tool_use_map.get(tid, {})
        if tool_info.get("name") == "Bash":
            cmd = tool_info.get("input", {}).get("command", "")
            if "git" in cmd:
                git_error_count += 1
                git_errors.append(cmd[:80])

    # Also catch git errors that don't use is_error but have "fatal:" in content
    for r in tool_results:
        if r["is_error"]:
            continue  # already counted
        tid = r["tool_use_id"]
        tool_info = tool_use_map.get(tid, {})
        if tool_info.get("name") == "Bash":
            cmd = tool_info.get("input", {}).get("command", "")
            preview = r["preview"]
            if "git" in cmd and ("fatal:" in preview or "error:" in preview.lower()):
                git_error_count += 1
                git_errors.append(cmd[:80])

    return {
        "turns": {
            "user": user_turns,
            "assistant": assistant_turns,
            "total": user_turns + assistant_turns,
        },
        "tokens": {
            "input": input_tokens,
            "output": output_tokens,
            "cache_read": cache_read_tokens,
            "cache_creation": cache_creation_tokens,
            "total": input_tokens + output_tokens,
        },
        "tool_calls": {
            "total": total_tool_calls,
            "errors": tool_error_count,
            "error_rate_pct": round(tool_error_rate, 1),
            "errors_by_tool": dict(errored_tools),
        },
        "rework": {
            "files_edited_over_3x": files_over_3,
            "count": len(files_over_3),
        },
        "git_errors": {
            "count": git_error_count,
            "commands": git_errors,
        },
    }


def print_report(metrics: dict, jsonl_path: Path):
    t = metrics["tokens"]
    turns = metrics["turns"]
    tc = metrics["tool_calls"]
    rw = metrics["rework"]
    git = metrics["git_errors"]

    print(f"Session: {jsonl_path.name}")
    print()
    print("Turns")
    print(f"  User:      {turns['user']}")
    print(f"  Assistant: {turns['assistant']}")
    print(f"  Total:     {turns['total']}")
    print()
    print("Tokens")
    print(f"  Input:          {t['input']:,}")
    print(f"  Output:         {t['output']:,}")
    print(f"  Cache read:     {t['cache_read']:,}")
    print(f"  Cache creation: {t['cache_creation']:,}")
    print(f"  Total (I+O):    {t['total']:,}")
    print()
    print("Tool calls")
    print(f"  Total:      {tc['total']}")
    print(f"  Errors:     {tc['errors']}")
    print(f"  Error rate: {tc['error_rate_pct']}%")
    if tc["errors_by_tool"]:
        print("  Errors by tool:")
        for tool, count in sorted(tc["errors_by_tool"].items(), key=lambda x: -x[1]):
            print(f"    {tool}: {count}")
    print()
    print("Rework (files edited >3x)")
    if rw["files_edited_over_3x"]:
        for fp, n in sorted(rw["files_edited_over_3x"].items(), key=lambda x: -x[1]):
            print(f"  {n}x  {fp}")
    else:
        print("  none")
    print()
    print("Git errors")
    print(f"  Count: {git['count']}")
    if git["commands"]:
        for cmd in git["commands"]:
            print(f"  - {cmd}")


def main():
    parser = argparse.ArgumentParser(description="Extract session metrics from Claude Code JSONL")
    parser.add_argument("jsonl", type=Path, help="Path to session JSONL file")
    parser.add_argument("--json", action="store_true", help="Output raw JSON instead of formatted report")
    args = parser.parse_args()

    if not args.jsonl.exists():
        print(f"ERROR: file not found: {args.jsonl}")
        sys.exit(1)

    entries = parse_session(args.jsonl)
    metrics = extract_metrics(entries)

    if args.json:
        print(json.dumps(metrics, indent=2))
    else:
        print_report(metrics, args.jsonl)


if __name__ == "__main__":
    main()
