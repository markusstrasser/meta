#!/usr/bin/env python3
"""Extract condensed session summaries from both Codex and Claude Code sessions.

Produces a structured summary per session: user prompts, tool calls, errors, corrections.
Designed for design-review analysis — captures workflow patterns, not full content.
"""

import json
import sys
import os
from pathlib import Path
from collections import Counter
from datetime import datetime, timedelta

def extract_codex_session(path: Path) -> dict:
    """Extract key signals from a Codex CLI session."""
    meta = {}
    user_messages = []
    tool_calls = []
    agent_messages = []
    errors = []
    compactions = 0
    web_searches = []
    patches = []
    spawned_agents = []

    with open(path) as f:
        for line in f:
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue

            t = d.get("type", "")
            p = d.get("payload", {})
            ts = d.get("timestamp", "")

            if t == "session_meta":
                meta = {
                    "id": p.get("id", ""),
                    "cwd": p.get("cwd", ""),
                    "model_provider": p.get("model_provider", ""),
                    "cli_version": p.get("cli_version", ""),
                    "timestamp": p.get("timestamp", ts),
                }

            elif t == "response_item":
                ri_type = p.get("type", "")
                role = p.get("role", "")

                if ri_type == "message":
                    content = p.get("content", [])
                    text = ""
                    for c in content:
                        if c.get("type") == "input_text":
                            text = c.get("text", "")[:500]
                        elif c.get("type") == "output_text":
                            text = c.get("text", "")[:500]
                    if role in ("user", "developer"):
                        user_messages.append(text)
                    elif role == "assistant":
                        agent_messages.append(text[:300])

                elif ri_type == "function_call":
                    name = p.get("name", "?")
                    args = p.get("arguments", "")
                    if isinstance(args, str):
                        try:
                            args_d = json.loads(args)
                            # Extract command for shell calls
                            cmd = args_d.get("command", args_d.get("cmd", ""))[:200]
                        except (json.JSONDecodeError, AttributeError):
                            cmd = args[:200]
                    else:
                        cmd = str(args)[:200]
                    tool_calls.append({"name": name, "args_preview": cmd})

                elif ri_type == "function_call_output":
                    output = p.get("output", "")
                    if isinstance(output, str) and ("error" in output.lower() or "traceback" in output.lower()):
                        errors.append(output[:300])

                elif ri_type == "web_search_call":
                    q = p.get("query", "?")
                    web_searches.append(q)

            elif t == "event_msg":
                em_type = p.get("type", "")
                if em_type == "user_message":
                    text = ""
                    items = p.get("items", [])
                    for item in items:
                        if isinstance(item, dict):
                            text = item.get("text", "")[:500]
                    if text:
                        user_messages.append(text)
                elif em_type == "context_compacted":
                    compactions += 1
                elif em_type == "collab_agent_spawn_end":
                    spawned_agents.append(p.get("agent_name", "?"))
                elif em_type == "patch_apply_end":
                    patches.append(p.get("path", "?"))
                elif em_type == "exec_command_end":
                    exit_code = p.get("exit_code", 0)
                    if exit_code != 0:
                        cmd = p.get("command", "?")[:200]
                        errors.append(f"exit={exit_code}: {cmd}")

            elif t == "compacted":
                compactions += 1

    # Summarize tool usage
    tool_counts = Counter(tc["name"] for tc in tool_calls)

    return {
        "source": "codex",
        "file": str(path.name),
        "meta": meta,
        "user_messages": user_messages[:20],  # Cap
        "agent_messages": agent_messages[:10],
        "tool_summary": dict(tool_counts.most_common(15)),
        "tool_calls_sample": tool_calls[:30],  # First 30 for pattern analysis
        "errors": errors[:20],
        "web_searches": web_searches[:10],
        "patches": patches[:20],
        "spawned_agents": spawned_agents,
        "compactions": compactions,
        "total_tool_calls": len(tool_calls),
        "total_events": sum(1 for _ in open(path)),
    }


def extract_claude_session(path: Path) -> dict:
    """Extract key signals from a Claude Code session."""
    user_messages = []
    tool_calls = []
    agent_messages = []
    errors = []
    subagents = []

    with open(path) as f:
        for line in f:
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue

            msg_type = d.get("type", "")
            role = d.get("role", "")

            if msg_type == "human" or role == "user":
                content = d.get("content", d.get("message", {}).get("content", ""))
                if isinstance(content, list):
                    for c in content:
                        if isinstance(c, dict) and c.get("type") == "text":
                            user_messages.append(c.get("text", "")[:500])
                elif isinstance(content, str):
                    user_messages.append(content[:500])

            elif msg_type == "assistant" or role == "assistant":
                content = d.get("content", d.get("message", {}).get("content", ""))
                if isinstance(content, list):
                    for c in content:
                        if isinstance(c, dict):
                            if c.get("type") == "tool_use":
                                tool_calls.append({
                                    "name": c.get("name", "?"),
                                    "args_preview": str(c.get("input", {}))[:200],
                                })
                            elif c.get("type") == "text":
                                text = c.get("text", "")
                                if text.strip():
                                    agent_messages.append(text[:300])

            elif msg_type == "tool_result":
                content = d.get("content", "")
                if isinstance(content, list):
                    for c in content:
                        if isinstance(c, dict) and c.get("type") == "text":
                            text = c.get("text", "")
                            if "error" in text.lower() or "traceback" in text.lower():
                                errors.append(text[:300])
                elif isinstance(content, str) and ("error" in content.lower() or "traceback" in content.lower()):
                    errors.append(content[:300])

    # Determine project from path
    project = "unknown"
    for part in path.parts:
        if part.startswith("-Users-alien-Projects-"):
            project = part.replace("-Users-alien-Projects-", "")
            break

    tool_counts = Counter(tc["name"] for tc in tool_calls)

    return {
        "source": "claude",
        "file": str(path.name),
        "project": project,
        "user_messages": user_messages[:20],
        "agent_messages": agent_messages[:10],
        "tool_summary": dict(tool_counts.most_common(15)),
        "tool_calls_sample": tool_calls[:30],
        "errors": errors[:20],
        "total_tool_calls": len(tool_calls),
    }


def main():
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    min_size = 10 * 1024  # 10KB minimum

    cutoff = datetime.now() - timedelta(days=days)
    results = {"codex": [], "claude": []}

    # Codex sessions
    codex_dir = Path.home() / ".codex" / "sessions"
    if codex_dir.exists():
        for f in sorted(codex_dir.rglob("*.jsonl")):
            if f.stat().st_size < min_size:
                continue
            mtime = datetime.fromtimestamp(f.stat().st_mtime)
            if mtime < cutoff:
                continue
            try:
                summary = extract_codex_session(f)
                results["codex"].append(summary)
            except Exception as e:
                print(f"WARN: {f}: {e}", file=sys.stderr)

    # Claude sessions
    claude_projects = Path.home() / ".claude" / "projects"
    if claude_projects.exists():
        for f in sorted(claude_projects.rglob("*.jsonl")):
            if "subagents" in str(f):
                continue
            if f.stat().st_size < min_size:
                continue
            mtime = datetime.fromtimestamp(f.stat().st_mtime)
            if mtime < cutoff:
                continue
            try:
                summary = extract_claude_session(f)
                results["claude"].append(summary)
            except Exception as e:
                print(f"WARN: {f}: {e}", file=sys.stderr)

    # Sort by total_tool_calls desc (most active first)
    for source in results:
        results[source].sort(key=lambda x: x.get("total_tool_calls", 0), reverse=True)

    # Output
    out_path = Path("/Users/alien/Projects/meta/.scratch/session-extracts.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, default=str)

    # Print summary stats
    print(f"Extracted {len(results['codex'])} Codex sessions, {len(results['claude'])} Claude sessions")
    for source in results:
        for s in results[source][:5]:
            project = s.get("meta", {}).get("cwd", s.get("project", "?"))
            if "/" in project:
                project = project.split("/")[-1]
            um = len(s.get("user_messages", []))
            tc = s.get("total_tool_calls", 0)
            errs = len(s.get("errors", []))
            print(f"  [{source}] {project}: {um} user msgs, {tc} tool calls, {errs} errors — {s.get('file','')[:40]}")


if __name__ == "__main__":
    main()
