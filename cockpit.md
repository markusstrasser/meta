# Cockpit — Human-Agent Interface

The "cockpit" is the set of tools that keep the human operator informed, oriented, and in control during Claude Code sessions. Design principle: the human should never have to ask "what's happening?" — the answer should already be visible.

## Deployed Components

### Status Line (`~/.claude/statusline.sh`)
Persistent bar inside Claude Code TUI. Updates after every assistant turn.

**Shows:** model · branch · $cost · ▓▓▓░░░ ctx% · duration · lines+/-
**Thresholds:**
- Context bar: green <50%, yellow 50-80%, red >80%
- Cost: turns red at threshold (default $2.00, set in cockpit.conf)
- Context >80%: shows `→ /compact` inline guidance
- Duration: shows `Xm` suffix after 5 min
- Lines: shows `+N/-N` when non-zero

**Also:** updates Ghostty tab title via OSC 2 (`Model · branch · $cost · ctx%`).

### Idle Notification (`~/.claude/hooks/stop-notify.sh`)
Stop hook. Sends macOS notification via `osascript` when Claude finishes responding. Shows first line of response as notification body.

**Toggle:** `~/.claude/cockpit.conf` → `notifications=on|off`

### Spinning Detector (`~/.claude/hooks/spinning-detector.sh`)
PostToolUse hook. Tracks consecutive same-tool calls via `/tmp/claude-spinning-$PPID`.

- **4 repeats:** advisory note ("agent may be repeating itself")
- **8 repeats:** stronger warning ("likely stuck in a loop")

### Session Receipt (`sessionend-log.sh`)
SessionEnd hook (enhanced). Writes two logs:
1. `~/.claude/session-log.jsonl` — backwards-compatible event log
2. `~/.claude/session-receipts.jsonl` — enriched flight receipt with cost, model, branch, context%, lines

Cost data flows: status line persists to `/tmp/claude-cockpit-{session_id}` → SessionEnd reads it.

### Dashboard (`meta/scripts/dashboard.py`)
Reads session-receipts.jsonl. Shows weekly/all-time stats.

```
uv run python3 scripts/dashboard.py          # last 7 days
uv run python3 scripts/dashboard.py --days 30
```

### Config (`~/.claude/cockpit.conf`)
```
notifications=on       # macOS notifications on idle
cost_warning=2.00      # cost threshold for red visual
```

## Architecture

```
                    ┌─────────────────────────────────┐
                    │         Claude Code TUI          │
                    ├─────────────────────────────────┤
 status line ──────│ Opus main · $0.42 · ▓▓▓▓░░ 67%  │
                    └──────────┬──────────────────────┘
                               │
           ┌───────────────────┼───────────────────────┐
           │                   │                        │
    ┌──────▼──────┐   ┌───────▼───────┐   ┌───────────▼──────────┐
    │  OSC 2 tab  │   │  /tmp state   │   │  cockpit.conf        │
    │  title      │   │  file         │   │  (toggles/thresholds)│
    └─────────────┘   └───────┬───────┘   └──────────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │  SessionEnd hook  │
                    │  → receipt JSONL  │
                    └─────────┬─────────┘
                              │
                    ┌─────────▼─────────┐
                    │  dashboard.py     │
                    │  (weekly stats)   │
                    └───────────────────┘
```

## Ideas Backlog

### Feasible, Not Yet Prioritized

- **Project-specific SessionStart hooks** — per-project reminders on session start. Intel: "check market hours". Genomics: "check Modal credits". Could use a `~/.claude/project-reminders/` directory with `project-name.txt` files.

- **Compaction countdown** — status line estimates turns remaining before auto-compaction based on context growth rate. Would need to track delta between updates.

- **Session templates** — pre-configured `.claude/session-start.md` files per project that set context for common task types (debugging, research, feature work).

- **Agent-type stop hook verifier** — use a `type: "agent"` Stop hook (has Read/Grep/Glob access) to verify output quality before session ends. E.g., check that all new files have tests, or that MEMORY.md wasn't corrupted.

- **Cost rate display** — show $/min in status line. Useful for spotting expensive loops. Need a rolling window, not just total/duration.

- **Sound alerts** — terminal bell (`\a`) on task completion or error threshold. Complements visual notification for when terminal isn't focused.

- **Multi-session sidebar** — cmux (Ghostty-based terminal wrapper) provides vertical tabs with per-pane context. Worth evaluating if running parallel sessions regularly.

- **Model comparison logging** — structured logging of task type + model used + cost + outcome. Over time, builds evidence for "use sonnet for X, opus for Y" routing decisions.

### Speculative / Low Priority

- **UserPromptSubmit preprocessing** — hook that analyzes user input before Claude sees it. Could detect pasted AI output and add a warning tag. Complex, unclear value.

- **PermissionRequest class-based hooks** — intercept permission dialogs by category (destructive, network, file write) instead of tool-by-tool. Cleaner than current Bash text matching but requires understanding the permission model deeply.

- **OpenTelemetry export** — full metrics pipeline to Prometheus/Grafana. Overkill for single-user, but the infrastructure exists in Claude Code.

- **Ghostty status bar widget** — blocked on Ghostty feature request #2421. When available, would allow persistent info display in terminal chrome separate from Claude Code's TUI.
