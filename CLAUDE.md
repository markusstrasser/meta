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

## Hard Rule
**Changes must be testable.** If you can't describe how to verify an improvement, it's not an improvement. "Add a rule that says X" is not testable. "After this change, the agent will do Y instead of Z in scenario W" is testable.

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
| Global hooks | `~/.claude/settings.json` | Loaded in every project (zsh loop guard) |
| Research MCP | `~/Projects/papers-mcp/` | Configured in `.mcp.json` per project |

## Session Forensics
- Chat histories: `~/.claude/projects/-Users-alien-Projects-*/UUID.jsonl` (JSONL, one entry per message)
- Error mining: Python script with `json.loads` per line, check `is_error`, `Exit code`, tool result content
- Top error sources (Feb 2026): zsh multiline loops (178/wk), DuckDB column guessing (324/wk), llmx wrong flags (16/wk)
