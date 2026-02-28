# CONTEXT: Cross-Model Review — Git Workflow for AI Agent Self-Optimization

## Decision Under Review
An AI agent (Claude Code) assists a solo developer across multiple repos. The agent does recursive self-optimization (analyzes its own sessions, updates rules/memory, improves hooks).

**Question:** Should the git workflow use structured commits (feature branches, `--no-ff` merges, trailers like `Evidence:`, `Verifiable:`, `Reverts-to:`) — or keep simple semantic commits on main?

**Claude's recommendation:** Keep simple. The agent never reads git log. It reads MEMORY.md (topic-organized), improvement-log.md (findings with evidence/status), and CLAUDE.md (rules/architecture). These are richer than anything git messages could provide. Structured git is redundant.

**User's counter-arguments:**
1. Git archaeology — tracking how decisions evolved over time
2. Hook integration — branch/merge events as triggers for automated review
3. Zero friction — agent can write arbitrarily detailed metadata unlike lazy humans
4. **Mutability** — MEMORY.md, improvement-log, CLAUDE.md are all mutable. They get edited, overwritten, compacted. Git is the only immutable record of their evolution. Claude argued these files are "richer than git" but they can be deleted or changed — their history only exists in git diffs.

## The Core Tension
Is the valuable archaeological record in the **commit messages** or in the **diffs of the mutable files themselves**? If the diffs carry the information, then simple commit messages + `git log -p` may be sufficient. If commit messages need to carry context that isn't in the diffs (e.g., "why" this change, what evidence triggered it), then structured messages add value.

## Current State
- 30 commits on main in meta repo, all from one day (2026-02-28)
- 5 commits within 2 minutes (rapid-fire session work)
- No branches ever used in meta or intel repos
- Selve has ONE merge commit ("curation tooling v3"), all else flat
- Agent reads MEMORY.md + CLAUDE.md at session start, never git log

## Context Infrastructure (what carries information today)
| Source | Organized by | Mutable? | Size |
|--------|-------------|----------|------|
| MEMORY.md | Topic | Yes — edited/overwritten | ~104 lines |
| improvement-log.md | Chronological findings | Yes — statuses updated | ~93 lines |
| CLAUDE.md | Section | Yes — rules added/removed | ~130 lines |
| Session transcripts | Time (JSONL) | Append-only, ephemeral | 150-1200+ lines |
| Git history | Chronological diffs | Immutable | Growing |

## Evidence Base
- Instructions alone = 0% reliable improvement (EoG, IBM)
- Simpler beats complex under stress (ReliabilityBench)
- Documentation helps +19 pts for novel knowledge, +3.4 for known APIs (Agent-Diff)

## Available Hook Events for Git
No native pre-merge/post-merge hook in Claude Code. Would need PreToolUse:Bash matching `git merge`. WorktreeCreate event exists but is for worktrees, not branches.

## Constraints
- Solo developer, no team, no PR reviews, no CI
- Agent writes most code and all commits
- Self-improvement pipeline: session-analyst → improvement-log → triage → implement → commit
- Hook infrastructure exists (PreToolUse, PostToolUse, Stop hooks deployed)
- Zero friction for agent to write detailed commit metadata
