# CONTEXT: Cross-Model Review — Git Workflow for AI Agent Self-Optimization

## Review Target
An AI agent (Claude Code) operates across multiple repos (intel, selve, meta, skills) for a solo developer. The question: what git workflow maximizes value for an agent doing recursive self-optimization?

**Current approach:** Simple semantic commits (1-2 sentences) directly on main. No branches, no trailers, no structured metadata in commits.

**Proposed alternative (rejected by Claude in conversation):** Feature branches with `--no-ff` merges, structured commit trailers (Evidence:, Verifiable:, Reverts-to:), descriptive branch names.

**Claude's argument for rejection:** The agent never reads `git log` — it reads MEMORY.md, improvement-log.md, and CLAUDE.md instead. These are organized by topic, not chronologically, and contain richer context. Git history is redundant with these sources.

**User's counter-arguments for structured git:**
1. Git archaeology — understanding how the codebase evolved
2. Hook targets — branch creation and merge are concrete events that could trigger automated reviews
3. The agent isn't lazy like humans — zero friction to write detailed metadata
4. **MEMORY.md, improvement-log, CLAUDE.md are all mutable** — they get edited, overwritten, compacted. Git preserves every version. The "richer sources" Claude cited can be deleted or changed; their history only exists in git.

## The Core Tension
Claude argued git is redundant because topic-organized files carry richer context. But those files are mutable — their evolution IS the git history. The question is whether the commit messages describing changes to those files need to be structured, or whether `git diff` on the files themselves is sufficient for archaeology.

## Existing Context Infrastructure

### MEMORY.md (auto-memory, persists across sessions)
- Constitutional decisions, autonomy boundaries, epistemic standards
- Exa MCP configuration, research patterns
- Hooks architecture (deployed, gotchas, not-yet-implemented)
- Hook authoring lessons, session-analyst pipeline
- Search & retrieval decisions, agent self-modification research
- ~104 lines, topic-organized, updated incrementally
- **Mutable** — entries are added, edited, and removed across sessions

### improvement-log.md (session-analyst findings)
- Each finding: session ID, evidence, failure mode, proposed fix, severity, status
- Tracks: observed → proposed → implemented → measured
- Currently 93 lines, 10 findings
- **Mutable** — status fields get updated, findings could be removed

### CLAUDE.md (project instructions)
- Architecture tables, hard rules, evidence base, cross-project architecture
- Hook events reference, session forensics
- ~130 lines per project
- **Mutable** — rules added, removed, refined every session

### Session transcripts
- JSONL files at ~/.claude/projects/*/UUID.jsonl
- Full conversation history, 150-1200+ lines each
- ~20 sessions for meta project alone
- **Append-only but ephemeral** — may be cleaned up

### Session logs
- compact-log.jsonl (compaction events)
- session-log.jsonl (session end events with reason, cwd, transcript lines)
- **Append-only**

## Actual Git History (meta repo, all 30 commits)

```
e0f3ac2 Add agent self-modification research memo, gitignore .mcp.json
e190dcb Add rule promotion criteria — require recurrence, non-redundancy, and checkability before encoding findings as rules
11b4a16 Reject heuristic gate findings — domain-specific one-off, covered by existing pushback rule
cd58f22 Update improvement-log with selve session findings and triage decisions
f1582f9 docs: add complete hooks inventory and verified event reference
b305877 Add session-analyst findings: sycophancy on heuristic rules, build-then-undo waste, redundant file reads, auto-commit rule tension
0ce9601 Add cross-model review artifacts for search MCP plan (Gemini 3.1 Pro + GPT-5.2 outputs, context bundles, synthesis)
8493153 Add search MCP design plan — emb wrapper with RRF cross-index fusion, heuristic routing, 3 tools
d55dcf9 docs: update hooks table with bash-loop-guard and failure-loop hooks, fix deployment list
835e465 docs: add session analysis section and shared hooks table
d91f941 docs: add failure modes 21-22 (sycophancy, usage-limit spin loop)
b46e6e3 docs: add session forensics section to AGENTS.md
27cd3d6 feat: add improvement-log.md for session analysis findings
cf53c89 Update key files list and maintenance checklist to reference search-retrieval-architecture.md
715e783 Add search & retrieval architecture research — CAG vs embedding decision framework
0278f3c Add skill-authoring skill for creating and validating agent skills
d01e45b Add global CLAUDE.md row to cross-project architecture table
1068fba Add community-validated patterns and Plan & Clear documentation
620ee56 Update research artifacts with 30+ paper sweep findings
b1d41c5 Remove obsolete planning docs — action plans were executed in intel repo
650a84c Add skills review synthesis and model review artifacts (2026-02-28)
007f5da Add Claude Code infrastructure: CLAUDE.md, hooks, researcher skill
9786558 Add pending paper saves and Exa recency note to research sweep
b6973d9 Add agent maintenance checklist and selve failure modes evaluation
83b82d7 docs: deep research on frontier agentic model behavior
0814a3f docs: add Claude Code architecture research and epistemic agent philosophy
92c8684 docs(analysis): update action plan with multi-model review corrections
1036c6b docs(analysis): add multi-model review synthesis for action plan
9b8633e docs: add action plan — 12-item implementation for intel deep layer
ece2a45 docs: add constitutional delta — philosophical foundation for autonomous agent
```

All on main. No branches. All from 2026-02-28 (one day). 5 commits within 2 minutes (11:57-11:59).

## Git History From Other Repos

### Selve (genomics pipeline)
```
20e3b21 merge: curation tooling v3 — normalization, regions, echtvar, IGV, calibration, phasing
```
One merge commit exists. All else flat on main. This is the only example of branch-based work.

### Intel (investment research)
All flat on main. No branches, no merges.

## Evidence Base (from meta CLAUDE.md)
- Instructions alone = 0% Majority@3 (EoG, IBM). Architecture produces reliability.
- Documentation helps +19 pts for novel knowledge, +3.4 for known APIs (Agent-Diff).
- Simpler beats complex under stress (ReliabilityBench). ReAct > Reflexion under perturbations.

## Available Hook Events
Claude Code supports: WorktreeCreate, WorktreeRemove, PreToolUse:Bash (could match git commands), Stop, PreCompact, SessionEnd. There is no native "pre-merge" or "post-merge" hook event — any merge hooking would require matching `git merge` in PreToolUse:Bash.

## Key Constraints
- Solo developer, no team, no PR reviews, no CI gates
- Agent writes most code and all commits
- Self-improvement pipeline: session-analyst → improvement-log → triage → implement → commit
- Agent has zero friction writing detailed metadata
- Repos span very different domains (investment research, genomics, agent infrastructure)
