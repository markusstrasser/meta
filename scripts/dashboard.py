#!/usr/bin/env python3
"""Claude Code session dashboard.

Reads ~/.claude/session-receipts.jsonl and ~/.claude/compact-log.jsonl
to show weekly/all-time stats: cost, duration, compactions, top projects.

Usage: uv run python3 scripts/dashboard.py [--days N]
"""

import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

RECEIPTS = Path.home() / ".claude" / "session-receipts.jsonl"
COMPACTIONS = Path.home() / ".claude" / "compact-log.jsonl"


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    entries = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return entries


def parse_ts(ts: str) -> datetime:
    # Handle both ISO formats
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f"):
        try:
            return datetime.strptime(ts, fmt)
        except ValueError:
            continue
    return datetime.min


def main():
    days = 7
    if "--days" in sys.argv:
        idx = sys.argv.index("--days")
        if idx + 1 < len(sys.argv):
            days = int(sys.argv[idx + 1])

    cutoff = datetime.now() - timedelta(days=days)

    # --- Load data ---
    receipts = load_jsonl(RECEIPTS)
    compactions = load_jsonl(COMPACTIONS)

    recent = [r for r in receipts if parse_ts(r.get("ts", "")) > cutoff]
    recent_compactions = [c for c in compactions if parse_ts(c.get("ts", "")) > cutoff]

    if not recent:
        print(f"No sessions in the last {days} days.")
        if receipts:
            print(f"({len(receipts)} total receipts on file)")
        else:
            print("No receipts yet. Receipts are written when sessions end.")
        return

    # --- Aggregate ---
    total_cost = sum(float(r.get("cost_usd", 0)) for r in recent)
    total_mins = sum(float(r.get("duration_min", 0)) for r in recent)
    total_lines_add = sum(int(r.get("lines_added", 0)) for r in recent)
    total_lines_rm = sum(int(r.get("lines_removed", 0)) for r in recent)
    avg_context = sum(int(r.get("context_pct", 0)) for r in recent) / len(recent)

    # By project
    by_project: dict[str, dict] = defaultdict(lambda: {"sessions": 0, "cost": 0.0, "mins": 0.0})
    for r in recent:
        p = r.get("project", "?")
        by_project[p]["sessions"] += 1
        by_project[p]["cost"] += float(r.get("cost_usd", 0))
        by_project[p]["mins"] += float(r.get("duration_min", 0))

    # By model
    by_model: dict[str, int] = defaultdict(int)
    for r in recent:
        by_model[r.get("model", "?")] += 1

    # Exit reasons
    by_reason: dict[str, int] = defaultdict(int)
    for r in recent:
        by_reason[r.get("reason", "?")] += 1

    # --- Print ---
    print(f"{'=' * 50}")
    print(f"  Claude Code Dashboard — last {days} days")
    print(f"{'=' * 50}")
    print()
    print(f"  Sessions:     {len(recent)}")
    print(f"  Total cost:   ${total_cost:.2f}")
    print(f"  Total time:   {total_mins:.0f} min ({total_mins/60:.1f} hrs)")
    print(f"  Avg context:  {avg_context:.0f}% at exit")
    print(f"  Code churn:   +{total_lines_add} / -{total_lines_rm}")
    print(f"  Compactions:  {len(recent_compactions)}")
    print()

    # By project table
    print("  By project:")
    sorted_projects = sorted(by_project.items(), key=lambda x: x[1]["cost"], reverse=True)
    for proj, stats in sorted_projects:
        print(f"    {proj:<20} {stats['sessions']:>3} sessions  ${stats['cost']:>6.2f}  {stats['mins']:>5.0f}m")
    print()

    # By model
    print("  By model:")
    for model, count in sorted(by_model.items(), key=lambda x: x[1], reverse=True):
        print(f"    {model:<20} {count:>3} sessions")
    print()

    # Exit reasons
    print("  Exit reasons:")
    for reason, count in sorted(by_reason.items(), key=lambda x: x[1], reverse=True):
        print(f"    {reason:<20} {count:>3}")
    print()

    # All-time summary if we have more data
    if len(receipts) > len(recent):
        all_cost = sum(float(r.get("cost_usd", 0)) for r in receipts)
        print(f"  All-time: {len(receipts)} sessions, ${all_cost:.2f} total")


if __name__ == "__main__":
    main()
