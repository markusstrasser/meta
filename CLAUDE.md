# Meta — Agent Infrastructure

## Purpose
This repo plans and tracks improvements to agent infrastructure across projects (intel, selve, skills, papers-mcp). It's the "thinking about thinking" repo.

## Communication
Never start responses with positive adjectives. Skip flattery, respond directly. Find what's wrong first.

## Key Files
- `maintenance-checklist.md` — pending improvements, monitoring list, sweep schedule
- `agent-failure-modes.md` — documented failure modes from real sessions
- `improvement-log.md` — structured findings from session analysis (session-analyst appends here)
- `frontier-agentic-models.md` — research report on agentic model behavior (4 papers read in full)
- `search-retrieval-architecture.md` — CAG vs embedding retrieval, Groq/Gemini assessment, routing decision framework
- `search-mcp-plan.md` — design plan for search MCP (emb wrapper + RRF fusion + routing), cross-model reviewed

## Hard Rule
**Changes must be testable.** If you can't describe how to verify an improvement, it's not an improvement. "Add a rule that says X" is not testable. "After this change, the agent will do Y instead of Z in scenario W" is testable.

## When to Add a Rule
A session-analyst finding becomes a rule only if:
1. **Recurs across 2+ sessions** — one-off domain findings are noise, not signal.
2. **Not already covered** by an existing general rule (e.g., sycophancy pushback already covers domain-specific compliance failures).
3. **Is a simple, checkable format rule** (">10 lines → use a .py file") OR is architectural (hook, test, scaffold).
Reject everything else. Over-prescription rots faster than under-prescription.

## What This Repo Is NOT
- Not a place to write more rules about rules. Instructions alone produce 0% reliable improvement (EoG, arXiv:2601.17915).
- Not a place to document things that should be implemented. If you plan a change here, implement it in the target repo in the same session.
- Architectural changes (hooks, healthchecks, deterministic scaffolding) > documentation changes.

## Evidence Base
- Instructions alone = 0% Majority@3 (EoG, IBM). Architecture produces reliability.
- Documentation helps +19 pts for novel knowledge, +3.4 for known APIs (Agent-Diff). Only encode what the model doesn't already know.
- Consistency flat over 18 months (Princeton, r=0.02). Retry and majority-vote are architectural necessities.
- Simpler beats complex under stress (ReliabilityBench). ReAct > Reflexion under perturbations.

## Cross-Project Architecture
| Layer | Location | Syncs how |
|-------|----------|-----------|
| Global CLAUDE.md | `~/.claude/CLAUDE.md` | Loaded in every project (universal rules) |
| Shared skills | `~/Projects/skills/` | Symlinked into each project's `.claude/skills/` |
| Shared hooks | `~/Projects/skills/hooks/` | Referenced by path in each project's `settings.json` |
| Project rules | `.claude/rules/` per project | Diverges intentionally (domain-specific) |
| Project hooks | `.claude/settings.json` per project | Per-project, similar patterns |
| Global hooks | `~/.claude/settings.json` | Loaded in every project |
| Research MCP | `~/Projects/papers-mcp/` | Configured in `.mcp.json` per project |

## Intel-Local Skills

Intel has local skill variants that diverge from shared skills. Cross-model reviews may flag "gaps" that are actually covered here:

| Shared skill | Intel-local variant | Difference |
|-------------|---------------------|------------|
| `competing-hypotheses` | `intel/.claude/skills/competing-hypotheses/` | Adds Bayesian LLR scoring via `ach_scorer.py` |
| (none) | `intel/.claude/skills/thesis-check/` | Full adversarial trade-thesis stress-test (432 lines) |
| `model-review` | `intel/.claude/skills/multi-model-review/` | Intel-specific review routing |

## Shared Hooks Inventory

Scripts in `~/Projects/skills/hooks/`. Referenced by absolute path from settings.json files.

| Hook | Event | Blocks? | Deployed where | What it does |
|------|-------|---------|----------------|--------------|
| `pretool-bash-loop-guard.sh` | PreToolUse:Bash | exit 2 | Global | Blocks multiline for/while/if (zsh parse error #1) |
| `pretool-search-burst.sh` | PreToolUse:search tools | exit 0/2 | Global | Warns at 4 consecutive searches, blocks at 8 without reading results |
| `pretool-data-guard.sh` | PreToolUse:Write\|Edit | exit 2 | (available) | Blocks writes to protected paths (datasets/, .parquet, .duckdb) |
| `postwrite-source-check.sh` | PostToolUse:Write\|Edit | exit 2 | Intel | Blocks research file writes without source tags |
| `posttool-bash-failure-loop.sh` | PostToolUse:Bash | exit 0 (warns) | Intel | Tracks consecutive Bash failures, warns after 5 |
| `stop-research-gate.sh` | Stop | exit 2 | Intel | Blocks stop if research files lack source tags; checks `stop_hook_active` |
| `precompact-log.sh` | PreCompact | exit 0 (async) | Global | Logs compaction events + modified files to `~/.claude/compact-log.jsonl` |
| `sessionend-log.sh` | SessionEnd | exit 0 (async) | Global | Logs session end events to `~/.claude/session-log.jsonl` |
| `add-mcp.sh` | (utility) | N/A | Manual | Adds MCP server presets to project `.mcp.json` |

### Hook design principles
- Deterministic > LLM-judged. Guard concrete invariants, not vibes.
- Fail open (`exit 0` or `trap 'exit 0' ERR`) unless blocking is clearly worth it.
- `trap 'exit 0' ERR` will swallow intentional `exit 2` from Python subprocesses — disable the trap before critical Python calls.
- Stop hooks must check `stop_hook_active` to prevent infinite loops.
- PreCompact and SessionEnd have **no decision control** — side-effect only (logging, backup, cleanup).

## Claude Code Hook Events (verified 2026-02-28)

17 events total. Source: https://code.claude.com/docs/en/hooks

| Event | Fires when | Can block? | Hook types |
|-------|-----------|------------|------------|
| SessionStart | Session begins/resumes | No | command |
| UserPromptSubmit | User submits prompt, before Claude sees it | Yes | command, prompt, agent |
| PreToolUse | Before a tool call executes | Yes (deny/allow/ask) | command, prompt, agent |
| PermissionRequest | Permission dialog appears | Yes (allow/deny) | command, prompt, agent |
| PostToolUse | After a tool call succeeds | No | command, prompt, agent |
| PostToolUseFailure | After a tool call fails | No | command, prompt, agent |
| Notification | Claude Code sends a notification | No | command |
| SubagentStart | Subagent spawned | No | command |
| SubagentStop | Subagent finishes | Yes (block) | command, prompt, agent |
| Stop | Claude finishes responding | Yes (block) | command, prompt, agent |
| TeammateIdle | Agent team teammate about to go idle | Yes (exit 2) | command |
| TaskCompleted | Task being marked completed | Yes (exit 2) | command |
| ConfigChange | Config file changes during session | Yes (block) | command |
| WorktreeCreate | Worktree being created | Yes (non-zero fails) | command |
| WorktreeRemove | Worktree being removed | No | command |
| PreCompact | Before context compaction | No | command |
| SessionEnd | Session terminates | No | command |

### Key fields
- `stop_hook_active`: Boolean in Stop/SubagentStop input. True when agent is continuing due to a stop hook. Must check to prevent loops.
- `last_assistant_message`: In Stop/SubagentStop. Claude's final response text.
- `trigger`: In PreCompact. `manual` or `auto`.
- `reason`: In SessionEnd. `clear`, `logout`, `prompt_input_exit`, `bypass_permissions_disabled`, `other`.

### Decision control patterns
- PreToolUse: JSON `hookSpecificOutput.permissionDecision` (allow/deny/ask)
- PermissionRequest: JSON `hookSpecificOutput.decision.behavior` (allow/deny)
- Stop, PostToolUse, SubagentStop, ConfigChange, UserPromptSubmit: JSON `decision: "block"`
- TeammateIdle, TaskCompleted: exit code 2 blocks
- WorktreeCreate: stdout = worktree path; non-zero exit fails creation
- PreCompact, SessionEnd, Notification, WorktreeRemove: no decision control

## Session Forensics
- Chat histories: `~/.claude/projects/-Users-alien-Projects-*/UUID.jsonl` (JSONL, one entry per message)
- Compaction log: `~/.claude/compact-log.jsonl` (PreCompact hook, auto-logged)
- Session log: `~/.claude/session-log.jsonl` (SessionEnd hook, auto-logged)
- Error mining: Python script with `json.loads` per line, check `is_error`, `Exit code`, tool result content
- Top error sources (Feb 2026): zsh multiline loops (178/wk), DuckDB column guessing (324/wk), llmx wrong flags (16/wk)
