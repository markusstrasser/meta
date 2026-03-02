# CONTEXT: Cross-Model Review — Meta Knowledge MCP Server Proposal

You are reviewing a proposal to build a FastMCP v3 server that exposes meta-project knowledge (hook designs, failure modes, prompting patterns, architectural decisions) as MCP tools consumable by other Claude Code projects.


# PROJECT CONSTITUTION
Review against these principles, not your own priors.

# Meta — Agent Infrastructure

## Purpose
This repo plans and tracks improvements to agent infrastructure across projects (intel, selve, genomics, skills, papers-mcp). It's the "thinking about thinking" repo.

<communication>
Never start responses with positive adjectives. Skip flattery, respond directly. Find what's wrong first.
</communication>

## Key Files
- `GOALS.md` — what the system optimizes for (human-owned)
- `maintenance-checklist.md` — pending improvements, monitoring list, sweep schedule
- `agent-failure-modes.md` — documented failure modes from real sessions
- `improvement-log.md` — structured findings from session analysis (session-analyst appends here)
- `frontier-agentic-models.md` — research report on agentic model behavior (4 papers read in full)
- `search-retrieval-architecture.md` — CAG vs embedding retrieval, Groq/Gemini assessment, routing decision framework
- `cockpit.md` — human-agent interface: status line, notifications, receipts, dashboard, ideas backlog

<constitution>
> **Human-protected.** Agent may propose changes but must not modify without explicit approval.

### Generative Principle

> Maximize the rate at which agents become more autonomous, measured by declining supervision.

Autonomy is the primary objective. In code, you can always run things — if they don't run successfully, they produce errors, and errors get corrected. With good verification, common sense, and cross-checking, autonomy leads to more than caution does. Grow > de-grow. Build the guardrails because they're cheap, not because they're the goal.

Error correction per session is the secondary constraint: autonomy only increases if errors are actually being caught. If supervision drops but errors go undetected, the system is drifting, not improving.

**The arms race:** The better the agent gets, the faster the human must rethink what they want next. Agent capability outpaces goal-setting. The human iteratively discovers what they want based on what they have — goals emerge from capability, not the other way around. The endgame: wake up to 30 great ideas, say yes/no, go back to sleep. Until then, the agent proposes and the human steers.

### Principles

**1. Architecture over instructions.** Instructions alone = 0% reliable (EoG). If it matters, enforce with hooks/tests/scaffolding. Text is a prototype; architecture is the product. Exception: simple format rules and semantic predicates that can't be expressed as deterministic checks.

**2. Enforce by category.**

| Category | Examples | Enforcement |
|----------|----------|-------------|
| Cascading waste | Spin loops, bash parse errors, search flooding | Hooks (block) |
| Irreversible state | Protected data writes, destructive git ops | Hooks (block) |
| Epistemic discipline | Source tagging, hypothesis generation, pushback | Stop hook (advisory) |
| Style/format | Commit messages, naming | Instructions |

**3. Measure before enforcing.** Log every hook trigger to measure false positives. Without data, you can't promote or demote hooks rationally.

**4. Self-modification by reversibility + blast radius.** "Obvious improvement" is unmeasurable. Use concrete proxies:
- **Autonomous:** affects only meta's files, easily reversible, one clear approach, no other project changes
- **Propose and wait:** touches shared infrastructure, multiple viable approaches, affects other projects, deletes/restructures architecture
- **Always human-approved:** this Constitution section, GOALS.md

**5. Research is first-class.** Divergent (explore) → convergent (build) → eat your own dogfood → analyze → research again when stuck. Not every session. Action produces information. Opportunistic, not calendar-driven.

**6. Skills governance.** Meta owns skill quality: authoring, testing, propagation. Skills stay in `~/Projects/skills/` (separate). Meta governs through session-analyst (sees usage across projects) and improvement-log.

**7. Fail open, carve out exceptions.** Hooks fail open by default. Explicit fail-closed list: protected data writes, multiline bash, repeated failure loops (>5). List grows only with measured ROI data.

**8. Recurring patterns become architecture.** If used/encountered 10+ times → hook, skill, or scaffolding. Not a snippet, not a manual habit. (The Raycast heuristic.)

**9. Cross-model review for non-trivial decisions.** Same-model review is a martingale. Cross-model provides real adversarial pressure. Required for multi-project or shared infrastructure changes. **Dispatch on proposals, not open questions** — critique is sharper than brainstorming. When model review disagrees with user's expressed preference, surface the disagreement and let the user decide.

**10. The git log is the learning.** Every correction is a commit. The error-correction ledger is the moat. Commits touching governance files (CLAUDE.md, MEMORY.md, improvement-log, hooks) require evidence trailers.

### Autonomy Boundaries

**Hard limits (never without human):** modify Constitution or GOALS.md; deploy shared hooks/skills affecting 3+ projects; delete architectural components.

**Autonomous:** update meta's CLAUDE.md/MEMORY.md/improvement-log/checklist; add meta-only hooks; run session-analyst; conduct research sweeps; create new skills (propagation = propose).

### Self-Improvement Governance

A finding becomes a rule or fix only if: (1) recurs 2+ sessions, (2) not covered by existing rule, (3) is a checkable predicate OR architectural change. Reject everything else.

Primary feedback: session-analyst comparing actual runs vs optimal baseline. If a change doesn't improve things in 30 days, revert or reclassify as experimental.

### Session Architecture
- Fresh context per orchestrated task (no --resume)
- 15 turns max per orchestrated task
- Subagent delegation for fan-out (>10 discrete operations)

### Known Limitations
- **Sycophancy:** instruction-mitigated only. Session-analyst detects post-hoc.
- **Semantic failures:** unhookable. Cross-model review is the only mitigation.
- **Instructions work >0% for simple predicates.** Don't over-hook.

### Pre-Registered Tests

How to verify this constitution is working (check via session-analyst after 2 weeks):

1. **No build-then-undo on shared infrastructure changes.** The reversibility + blast radius boundary should prevent autonomous changes that get reverted. Test: zero reverts of meta-initiated shared changes in 14 days.
2. **Hooks fire on high-frequency failures.** Deployed hooks (bash-loop-guard, spinning-detector, failure-loop) should reduce repeated tool failures. Test: ≥50% reduction in ≥5-bash-failure-streaks vs pre-deployment baseline.
3. **Research produces architecture, not documents.** Research sessions should result in hooks, skills, or code — not just memos. Test: ≥50% of research findings in improvement-log have "implemented" status within 30 days.
4. **Model review surfaces disagreements.** When cross-model review disagrees with a stated preference, the synthesis explicitly flags it. Test: zero instances of silently overriding user preference in review artifacts.
</constitution>

## Backlog

- [ ] **Cron/auto-update skill** — Cross-project daily job monitoring new papers/tools/databases. (Source: genomics goals elicitation 2026-02-28)
- [ ] **Hook ROI telemetry** — Log every hook trigger/decision to JSONL for false-positive measurement. Prerequisite for progressive enforcement. (Source: constitution model-review 2026-02-28)
- [ ] **Regret/corrections metric** — Instrument corrections per session as a first-class metric from session-analyst. (Source: constitution model-review 2026-02-28)

## What This Repo Is NOT
- Not a place to write more rules about rules.
- Not a place to document things that should be implemented. Plan here → implement in target repo in same session.
- Architectural changes > documentation changes.

<reference_data>
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
| Genomics pipeline | `~/Projects/genomics/` | Extracted from selve 2026-02-28 |

## Intel-Local Skills

| Shared skill | Intel-local variant | Difference |
|-------------|---------------------|------------|
| `competing-hypotheses` | `intel/.claude/skills/competing-hypotheses/` | Adds Bayesian LLR scoring via `ach_scorer.py` |
| (none) | `intel/.claude/skills/thesis-check/` | Full adversarial trade-thesis stress-test (432 lines) |
| `model-review` | `intel/.claude/skills/multi-model-review/` | Intel-specific review routing |

## Shared Hooks Inventory

Scripts in `~/Projects/skills/hooks/`. Referenced by absolute path from settings.json.

| Hook | Event | Blocks? | Deployed where | What it does |
|------|-------|---------|----------------|--------------|
| `pretool-bash-loop-guard.sh` | PreToolUse:Bash | exit 2 | Global | Blocks multiline for/while/if (zsh parse error #1) |
| *(inline)* bare-python-guard | PreToolUse:Bash | exit 2 | Global | Blocks bare `python`/`python3` without `uv run` |
| `pretool-search-burst.sh` | PreToolUse:search tools | exit 0/2 | Global | Warns at 4, blocks at 8 consecutive searches |
| `pretool-data-guard.sh` | PreToolUse:Write\|Edit | exit 2 | (available) | Blocks writes to protected paths |
| `postwrite-source-check.sh` | PostToolUse:Write\|Edit | exit 2 | Intel | Blocks research writes without source tags |
| `posttool-bash-failure-loop.sh` | PostToolUse:Bash | exit 0 (warns) | Global | Warns after 5 consecutive Bash failures |
| `stop-research-gate.sh` | Stop | exit 2 | Intel | Blocks stop if research files lack source tags |
| `precompact-log.sh` | PreCompact | exit 0 (async) | Global | Logs compaction events |
| `session-init.sh` | SessionStart | exit 0 | Global | Persists session ID to `.claude/current-session-id` |
| `sessionend-log.sh` | SessionEnd | exit 0 (async) | Global | Logs session end + flight receipt + recent commits |
| `stop-notify.sh` | Stop | exit 0 | Global | macOS notification on idle |
| `spinning-detector.sh` | PostToolUse | exit 0 (warns) | Global | Warns at 4/8 consecutive same-tool calls (uses additionalContext) |
| `userprompt-context-warn.sh` | UserPromptSubmit | exit 0 (warns) | Global | Detects continuation boilerplate |
| `pretool-commit-check.sh` | PreToolUse:Bash | exit 0/2 | Global | Checks git commits: [prefix], no Co-Authored-By, governance trailers |

### Skill-Embedded Hooks (new pattern, 2026-03-01)
| Skill | Event | Type | What it does |
|-------|-------|------|-------------|
| `researcher` | PostToolUse:Write\|Edit | prompt | Checks source citations on factual claims |

### Intel-Only Hooks (in .claude/settings.json)
| Hook | Event | What it does |
|------|-------|-------------|
| Large file guard | PreToolUse:Read | Advisory when file >256KB without offset/limit |
| DuckDB dry-run | PostToolUse:Write\|Edit | Advisory when setup_duckdb.py or tools/datasets/ modified |
| Backtest guard | PreToolUse:search tools | Blocks external queries during active backtests |
| Data protection | PreToolUse:Write\|Edit | Blocks writes to datasets/, .parquet, intel.duckdb |
| Secrets guard | PreToolUse:Write\|Edit | Blocks writes to .env, credentials, secrets files |

## Hook Design Principles
- Deterministic > LLM-judged. Guard concrete invariants, not vibes.
- Fail open unless blocking is clearly worth it.
- `trap 'exit 0' ERR` swallows `exit 2` from Python — disable trap before critical Python calls.
- Stop hooks must check `stop_hook_active` to prevent infinite loops.

## Claude Code Hook Events (verified 2026-02-28)

17 events total. Source: https://code.claude.com/docs/en/hooks

| Event | Fires when | Can block? | Hook types |
|-------|-----------|------------|------------|
| SessionStart | Session begins/resumes | No | command |
| UserPromptSubmit | User submits prompt | Yes | command, prompt, agent |
| PreToolUse | Before tool call | Yes (deny/allow/ask) | command, prompt, agent |
| PermissionRequest | Permission dialog | Yes (allow/deny) | command, prompt, agent |
| PostToolUse | After tool succeeds | No | command, prompt, agent |
| PostToolUseFailure | After tool fails | No | command, prompt, agent |
| Notification | Notification sent | No | command |
| SubagentStart | Subagent spawned | No | command |
| SubagentStop | Subagent finishes | Yes (block) | command, prompt, agent |
| Stop | Claude finishes | Yes (block) | command, prompt, agent |
| TeammateIdle | Teammate idle | Yes (exit 2) | command |
| TaskCompleted | Task completed | Yes (exit 2) | command |
| ConfigChange | Config changes | Yes (block) | command |
| WorktreeCreate | Worktree created | Yes (non-zero fails) | command |
| WorktreeRemove | Worktree removed | No | command |
| PreCompact | Before compaction | No | command |
| SessionEnd | Session terminates | No | command |

### Decision control patterns
- PreToolUse: JSON `hookSpecificOutput.permissionDecision` (allow/deny/ask)
- PermissionRequest: JSON `hookSpecificOutput.decision.behavior` (allow/deny)
- Stop, PostToolUse, SubagentStop, ConfigChange, UserPromptSubmit: JSON `decision: "block"`
- TeammateIdle, TaskCompleted: exit code 2 blocks
- PreCompact, SessionEnd, Notification, WorktreeRemove: no decision control
</reference_data>

<cockpit>
## Cockpit (Human-Agent Interface)

Status line, notifications, receipts, and dashboard. Full details in `cockpit.md`.

| Component | Location | What |
|-----------|----------|------|
| Status line | `~/.claude/statusline.sh` | Model, branch, cost, context bar |
| Config | `~/.claude/cockpit.conf` | `notifications=on\|off`, `cost_warning=2.00` |
| Dashboard | `meta/scripts/dashboard.py` | `uv run python3 scripts/dashboard.py [--days N]` |
</cockpit>

<session_forensics>
## Session Forensics
- Chat histories: `~/.claude/projects/-Users-alien-Projects-*/UUID.jsonl`
- Compaction log: `~/.claude/compact-log.jsonl`
- Session receipts: `~/.claude/session-receipts.jsonl`
- Top error sources (Feb 2026): zsh multiline loops (178/wk), DuckDB column guessing (324/wk), llmx wrong flags (16/wk)
</session_forensics>


# PROJECT GOALS

# Meta — Goals

> Human-owned. Agent may propose changes but must not modify without explicit approval.

## Mission

Maximize autonomous agent capability across all projects while maintaining epistemic integrity. The system should learn things once and handle them forever — the human intervenes only for genuinely new information, creative direction, or goal-setting.

## Generative Principle

**Maximize the rate at which agents become more autonomous, measured by declining supervision — AND maximize error correction per session across all projects.**

The deeper dynamic: the better the agent gets, the faster the human must rethink what they actually want next. This is an arms race — agent capability outpaces goal-setting until prediction quality is high enough that the agent can extrapolate what the human would want without asking. The endgame: wake up to 30 great ideas, say yes/no, go back to sleep.

## Primary Success Metric

**Ratio of autonomous-to-supervised work across sub-projects.** Measured qualitatively: when reviewing a day's chat logs, there should be no:
- Reverted work (build-then-undo)
- 5-hour runs that should have been 1-hour (missing scaffolding, bad DX)
- Error branch spirals (bad hooks, missing guards)
- Agent theater (performative work that produces no value)
- Repeated corrections for things already taught once

The closer sessions get to "optimal run" (what would happen if the agent had perfect tooling and perfect instructions), the better meta is doing its job.

## Secondary Metrics

- **Wasted supervision rate** — % of human turns that are corrections, boilerplate, or rubber stamps. Currently ~21%. No numeric target, but qualitative trend should be downward.
- **Agent reliability** — % of tasks completed correctly without correction.
- **Time-to-capability** — how fast a new project gets proper agent infrastructure.

## Self-Modification Boundaries

**Full autonomy within invariants**, with a gradient:
- **Clear improvement, one obvious path** → just do it, commit, move on
- **Multiple valid solutions, could change a lot** → propose and wait for human review
- **CLAUDE.md Constitution section / GOALS.md** → always human-approved

The invariants: the Constitution section (in CLAUDE.md) and GOALS.md are human-owned. Everything else (rest of CLAUDE.md, hooks, skills, maintenance checklists, rules, MEMORY.md) can be modified autonomously when the improvement is unambiguous.

## Strategy

1. **Session forensics** — session-analyst finds behavioral anti-patterns, improvement-log tracks them to architectural fixes
2. **Hook engineering** — deterministic guards that prevent known failure modes (instructions alone = 0% reliable)
3. **Observability** — cockpit components keep the human informed without requiring them to ask
4. **Research** — stay current on agent behavior research, absorb what's applicable, ignore what's not
5. **Cross-project propagation** — skills, hooks, rules, and patterns flow from meta to all projects
6. **Self-improvement** — meta improves its own tooling using the same methods it applies to sub-projects

## Orchestrator

**Unblocked.** The orchestrator is meta-level infrastructure, independent of any specific project's validation status. Build it for tasks that are clearly automatable now:
- Entity refresh cycles
- Data maintenance
- Research sweeps
- Self-improvement passes (`/project-upgrade`, `/goals` elicitation)

The vision: any project can receive `/project-upgrade` or `/goals` and get meta's full toolkit applied autonomously, stopping only when a quality judge determines no further improvement is possible given the project's goals.

## Research Cadence

**First-class function, not every-session.** Research is divergent thinking — exploring what's new, what's possible, what others have solved. Implementation is convergent — building, testing, eating your own dogfood.

The cycle: research (divergent) until diminishing returns → build (convergent) → use it → analyze whether it actually works → research again when stuck or when new information appears.

- **Not calendar-driven.** No fixed weekly sweep that degrades into checkbox behavior.
- **Opportunistic.** New model ships → immediate sweep. Stuck on a problem → search for prior art. Steep improvement curve → more research. Diminishing returns → more action.
- **Action produces information.** At some point, building and using is more informative than reading papers.

## Projects Served

All projects: intel, selve, genomics, skills, papers-mcp, and any future repos. The uneven attention to date (mostly intel) is an artifact of where work has concentrated, not a priority decision.

Meta provides: shared skills, hooks, MCP servers, maintenance checklists, session analysis, observability, and the research pipeline. Any project should be able to install meta's toolkit and benefit.

## Skills Ownership

**Meta owns skill quality.** Meta runs session analysis, sees when skills are applied across projects, and can judge whether they work. Claude Code knowledge is co-located here. The information flow is natural: session-analyst findings → skill improvements → propagation.

Skills (`~/Projects/skills/`) may merge into meta as a directory. For now, kept separate. But quality governance (authoring standards, testing, versioning, cross-project propagation) lives in meta regardless of directory structure.

## Quality Standard

Recurring patterns (used/encountered 10+ times) must become architecture — not instructions, not snippets, not manual habits. The Raycast-snippet heuristic: if you paste it 10 times, it should be a hook, a skill, or scaffolding.

Qualitative reports from session-analyst are the primary feedback mechanism. No arbitrary numeric targets — the goal is "no stupid shit in the logs," judged by comparing actual runs against what an optimal run would look like.

## Open Questions (dispatched to model-review)

- **Enforcement granularity** — which principles deserve hooks vs. which stay instructional? Hooks can be annoying. Need empirical data from meta sessions. Progressive approach for now.
- **Autonomy gradient threshold** — where exactly does "clear improvement" end and "multiple valid solutions" begin? Probably can't be defined precisely; needs examples over time.
- **Skills merge timing** — meta owns quality but skills/ is still separate. When/whether to merge directories.

## Deferred Scope

- **IB API / trading automation** — blocked by paper trading validation in intel, not meta's concern
- **Fraud/corruption separation** — stays in intel until compute burden forces a split
- **Numeric benchmarking** — qualitative assessment first, formalize metrics when patterns stabilize

## Exit Condition

Meta becomes unnecessary when:
1. Claude (5, 6, N) natively handles meta-improvement — eliciting user goals, applying project upgrades, working correctly across subdomains, benchmarking itself
2. Claude Code ships native equivalents of hooks, observability, session analysis
3. The creative/divergent capability (connecting old projects, finding novel solutions across domains) is handled natively

This may never fully happen — meta encodes domain-specific and personal-idiosyncratic knowledge that generic tooling won't replicate. But the goal is to make meta's job progressively smaller, not to preserve it.

## Resource Constraints

- Single human operator with limited attention
- Cost-conscious (session receipts track spend)
- Compute: local Mac + cloud APIs (Anthropic, Google, OpenAI, Exa)
- Storage: SSK1TB external drive for large datasets

---

*Created: 2026-02-28. Updated: 2026-02-28 (generative principle, self-modification boundaries, research philosophy, skills ownership). Elicited via goals + constitution questionnaire.*


# GLOBAL CLAUDE.MD (always loaded, every project)

# Global Rules

<communication>
Never start responses with positive adjectives. Skip flattery, respond directly.
</communication>

<technical_pushback>
"No" is a valid answer. "Don't do this" is a valid answer. "This isn't done yet" is a valid answer. Refusing a request or flagging incomplete work is better than complying and producing worse software.

When the user proposes an approach and you have strong technical grounds to disagree:
- Say so before writing any code. Explain what's wrong and what you'd do instead.
- Hold your position if pushed back — state what evidence would change your mind rather than folding.
- If the user insists after hearing your case, comply but note the tradeoff. Their codebase, their call.

Before building a feature, answer these out loud if non-obvious:
1. **Will this work in our environment?** (e.g., SQLite on NFS = locking failures. Check before building.)
2. **Who calls this?** Code with no caller is not "done" — it's dead code with a plan attached. Either wire it in or don't build it.
3. **Can we validate at 1/10 the code?** Build the 50-line version first. Expand only after evidence it works.

Applies to: architecture, abstractions, schema design, over-engineering, speculative features, unintegrated code.
Does NOT apply to: style preferences, naming, minor implementation choices, things that are genuinely subjective.
</technical_pushback>

<git_rules>
## Git Commits
- Do not add `Co-Authored-By: Claude` (or any Claude co-author line) to commit messages.
- Commit messages: semantic, 1-2 sentences. No essays.
- Prefer granular semantic commits over one big commit.
- When user says "commit" or "commit your changes" with no further instructions, follow these rules as-is. No additional guidance needed.
- **Trailers required** on commits touching `CLAUDE.md`, `MEMORY.md`, `improvement-log.md`, or hook code/config:
  ```
  Evidence: session/<id> or improvement-log#<n>
  Affects: memory|rules|hooks|code
  ```
  Optional: `Verifiable: yes|no`, `Reverts-to: <commit>`. Ordinary code commits skip trailers.

## Git Workflow
All commits go to main. No branches. This avoids HEAD collisions when parallel agents share a working directory (observed: wrong-branch commits in intel 2026-02-28).

- **Prefix commits with `[feature-name]`** for semantic grouping: `[docs-triage] Delete 18 superseded files`
- `git log --grep="\[feature-name\]"` recovers full feature history
- Parallel agents commit to main with different prefixes — no coordination needed
- This implicitly authorizes commits — don't ask permission at each step
</git_rules>

<ai_text_policy>
## AI-Generated Text (Critical)
Text from other AI models — whether pasted by the user OR returned from llmx/multi-model queries — is **unverified by default**. Before adopting any claim or recommendation:
1. Check for hallucinated specifics (author names, numbers, variant designations, function names).
2. Check for slop (vague platitudes dressed as insight).
3. Check for impracticality (production-grade recommendations for personal projects).
4. Reference the `model-guide` skill for each model's known failure modes and hallucination rates.
5. Cosign, reject, or complement — never adopt wholesale.

## Multi-Model Review
When `llmx` is available and work is non-trivial, offer to cross-check conclusions with a second model via `/model-review`. Gemini 3.1 Pro for pattern review over large context; GPT-5.2 for reasoning depth. Both hallucinate — be critical of their outputs.
</ai_text_policy>

<environment>
## Python & Environment
- Use `python3` not `python` (macOS has no `python` binary).
- All projects use `uv`. Run scripts with `uv run python3 script.py` or `uvx tool`. Never bare `python3 -c "import pkg"` for project dependencies — use `uv run`.
- Multi-line Python (>10 lines): write a `.py` file, not inline `python3 -c`. Exception: one-shot queries.
- Prefer `ast` module or direct import over regex when parsing Python source code.

## DuckDB
Before querying any table for the first time, run `DESCRIBE tablename` or `SELECT * FROM tablename LIMIT 1`. Never guess column names.

## Efficiency
- Save `find`/`ls` output to `/tmp/` when you need multiple passes over the same file listing.
</environment>

<context_management>
## Context Continuations
After compaction or session continuation, read `.claude/checkpoint.md` if it exists. It contains branch, uncommitted changes, diff summary, and recent commits. Use this to infer what was being worked on — examine the recent commits, diffs, and modified files to determine the task. Don't ask the user for context; re-orient from the git state.

## Context-Save Before Compaction
When approaching context limits, proactively save progress to `.claude/checkpoint.md` before compaction occurs. Include: current task, what's done, what's remaining, key decisions made, files modified. Don't stop tasks early due to context concerns — save state and continue after compaction.

## Post-Synthesis Completeness Check
After producing a synthesis from multiple inputs (model reviews, research rounds, multi-source analysis), mechanically verify: does every input item appear in the output? List any dropped items and justify the omission. Don't wait for the user to ask "are you sure you included everything?"

## Plan-Mode Handoff
After any research/analysis phase that consumed >50% context and produced actionable findings (model-review, researcher, multi-step exploration), offer a plan-mode handoff instead of trying to implement in remaining context. The plan file persists through the clear — it's the information bridge between the exploration phase and the execution phase. Don't offer if findings are purely exploratory with no concrete next steps.
## Plan & Work Tracking
Plans are ephemeral working documents. Never commit them to `docs/` or repo root.

- **Location:** `.claude/plans/` (gitignored)
- **Naming:** `{session_id[:8]}-{slug}.md` — read session ID from `.claude/current-session-id`
- **Content header:** Include full session ID, date, project name at top of plan file
- **At session start:** Scan `.claude/plans/` for recent plans. Check what's done (checkboxes). Don't redo completed work. Delete plans older than 14 days.
- **During work:** Update plan checkboxes as items complete
- **Never commit plans.** The git log is the record of what was done. Plans are scratch.
</context_management>

<subagent_usage>
## Subagent Usage
Use subagents when tasks can run in parallel, require isolated context, or involve independent workstreams that don't need to share state. For simple tasks, sequential operations, single-file edits, or tasks where you need to maintain context across steps, work directly rather than delegating. Don't spawn a subagent for something a single Grep or Read call would answer.
</subagent_usage>


# MEMORY.MD

# Meta Project Memory

## Constitutional Decisions (2026-02-27, updated 2026-02-28)
Resolved via structured questionnaire. These are stable unless user revisits.

### Intel (2026-02-27, updated 2026-03-01)
- **Primary mission:** Investment research (most falsifiable, fastest learning signal)
- **Fraud/corruption:** Stays in intel. May separate later.
- **Target:** $500M-$5B small/mid-cap public companies
- **Constitution** lives in `CLAUDE.md` as `## Constitution` heading (merged from `docs/CONSTITUTION.md` on 2026-03-01). **GOALS.md** (`docs/`). Both human-protected.
- **Generative principle:** "Maximize error correction rate, measured by market feedback."

### Meta (2026-02-28)
- **Constitution lives in CLAUDE.md** as `## Constitution` heading — not a separate file.
- **GOALS.md** is a separate file (human-owned).
- **Generative principle:** "Maximize the rate agents become more autonomous, measured by declining supervision." Autonomy > caution (grow > de-grow). Guardrails are cheap insurance, not the goal.
- **Self-modification:** reversibility + blast radius, not "obviousness." Autonomous for meta-only reversible changes. Propose for shared/multi-approach/cross-project.
- **Skills:** Meta owns quality. Skills stay in `~/Projects/skills/` (separate). Merge only if concrete friction.
- **Research:** First-class, not every-session. Divergent → convergent → dogfood → analyze.
- **Enforcement:** Progressive. Hook ROI telemetry first. Cascading waste → hooks; epistemic → advisory; semantic → instructions.
- **Orchestrator:** UNBLOCKED. Meta-level infra, independent of project validation.
- **Model review:** Dispatch on proposals, not open questions. Surface disagreements with user preference.
- **Process lessons:** Fewer questions, more inference. Tradeoff questions > principle questions. Pre-register tests. Constitution in CLAUDE.md, not separate file.

### Autonomy Boundaries
- Hard limits: no capital deployment, no external contacts, no constitution edits without approval
- Autonomous: create entities, add datasets, update rules/CLAUDE.md/MEMORY.md, auto-commit verified knowledge
- Auto-commit standard: verified sources, shown reasoning, source grades, confidence threshold
- IB sandbox ($10K): future phase, pending paper trading validation

### Epistemic Standards
- Source grading: NATO Admiralty for now, may evolve to domain-optimized system
- Multi-model review: required for trade-influencing analysis; use judgment elsewhere
- Adversarial stance: skeptical but fair, domain-dependent (don't assume every company is fraudulent)
- Falsification before trade recommendation: mandatory (Principle 11)

### Agent Self-Improvement
- Can update: rules, MEMORY.md, CLAUDE.md, scoring, tooling, base rates
- Cannot update: CONSTITUTION.md, GOALS.md (propose changes, human decides)
- Rule changes need evidence from observed sessions, not speculation
- Prefer hooks/tests over advisory rules ("instructions alone = 0% reliable")

### Orchestrator
- Concept: Python cron + SQLite + subprocess, 15 turns/task, fresh context per task
- Status: idea/future. Blocked by paper trading validation.
- Details: see maintenance-checklist.md "Ideas / Future Work"

## Exa MCP Configuration
- **HTTP transport with API key** enables optional tools: `deep_researcher_start/check`, `web_search_advanced_exa`, `crawling_exa`, `people_search_exa`
- Config: `"type": "http", "url": "https://mcp.exa.ai/mcp?exaApiKey=KEY&tools=..."` in `.mcp.json`
- `.mcp.json` must be in `.gitignore` (contains API key)
- Rate limits (free tier): /search 10 QPS, /contents 100 QPS, /answer 10 QPS, /research 15 concurrent
- Own API key removes rate limits

## Research Patterns
- WebSearch works when Exa is rate-limited; use as fallback
- Reddit site: searches often return empty; aggregator sites + WebFetch extracts more signal
- Kimi CLI available for subagent tasks (user preference)

## Hooks Architecture (verified 2026-02-28)

### Deployed hooks
- **Global** (`~/.claude/settings.json`): bash-loop-guard (PreToolUse), session-init (SessionStart), precompact-log (PreCompact, async), sessionend-log (SessionEnd, async)
- **Intel** (`intel/.claude/settings.json`): data-guard, secrets-guard, bash-rm-guard, backtest_guard, failure-loop (PostToolUse), source-check (PostToolUse:Write|Edit), stop-research-gate (Stop, blocks exit 2)
- **Anki** (`anki/.claude/settings.json`): SessionStart healthcheck, prompt-type PreToolUse on deleteNotes

### Gotchas
- `trap 'exit 0' ERR` swallows Python `sys.exit(2)` — disable trap before critical Python calls
- Stop hooks: must check `stop_hook_active` or get infinite loops
- PreCompact/SessionEnd: **no decision control** — side-effect only
- Heredoc `<< 'EOF'` replaces Python's stdin — use `INPUT=$(cat); echo "$INPUT" | python3 -c '...'` pattern

### Observability logs
- `~/.claude/compact-log.jsonl` — PreCompact events (session, trigger, cwd, transcript_lines, modified_files)
- `~/.claude/session-log.jsonl` — SessionEnd events (session, reason, cwd, transcript_lines)
- `~/.claude/session-receipts.jsonl` — Flight receipts with commits field (since 2026-03-01)

## Plan & Work Tracking (2026-03-01)
- **Plans → `.claude/plans/{session_id[:8]}-{slug}.md`** (gitignored, ephemeral)
- **Never commit plans** to `docs/` or repo root. Git log = record of work. Plans = scratch.
- **Session ID** persisted to `.claude/current-session-id` by SessionStart hook
- **SessionEnd** captures commits made during session into receipts (uses session-id file mtime as anchor)
- **Cross-agent awareness**: agent reads `.claude/plans/` at session start + recent receipts
- **Gitignore deployed**: genomics, selve, anki. Intel already has `.claude/` blanket ignore.
- **Problem solved**: genomics had `docs/IMPROVEMENT_PLAN.md` committed as permanent cruft; intel had 11 stale plans in `docs/plans/` duplicated 3x across worktrees

### Native Claude Code Features Leveraged (2026-03-01)
- **`additionalContext` JSON output**: spinning-detector now injects warnings directly into Claude's context (not stderr)
- **Prompt hooks (`type: "prompt"`)**: researcher SKILL.md embeds PostToolUse prompt hook for source citation checking. Selve uses prompt Stop hook for research quality gate.
- **Agent hooks (`type: "agent"`)**: session-analyst subagent has Stop agent hook that verifies output quality (the cockpit.md "stop hook verifier" idea — now implemented natively)
- **Subagent persistent memory**: researcher + session-analyst at `~/.claude/agents/` with `memory: user`. Intel agents (entity-refresher, dataset-discoverer, investment-reviewer) with `memory: project`.
- **`model` field**: Only useful on `context: fork` skills (session-analyst). Inline skills inherit session model — pinning changes model mid-conversation which is unexpected. User preference: smart model by default, cheaper for search/lookup.
- **Skill-embedded hooks**: New pattern — hooks in skill frontmatter scoped to skill lifecycle. Reduces global hook complexity.
- **`pretool-commit-check.sh`**: Deterministic git commit checks deployed globally. Semantic checks (message quality) deferred — prompt hooks on every Bash call too expensive.
- **Full assessment**: `meta/research/claude-code-native-vs-meta-infra.md`
- **Implementation plan**: `meta/research/native-leverage-plan.md`

### Not yet implemented (potential value)
- UserPromptSubmit: pre-processing before Claude sees input (e.g., AI-output detection)
- PermissionRequest: class-based destructive action hooks (cleaner than Bash text matching)

## Hook Authoring Lessons (2026-02-28)
- **`$$` vs `$PPID`**: `$$` = hook's own PID (unique per invocation). `$PPID` = Claude Code parent (stable within session). Use `$PPID` for any hook tracking state across invocations.
- **PostToolUse can warn, not block.** Only PreToolUse can block (exit 2). PostToolUse messages are advisory.
- **API usage limits are unhookable.** "Out of extra usage" = system message, not tool output. No hook event fires. Bash failure-loop detector is the closest proxy. Watch for future `OnRateLimit` event.

## Session-Analyst Pipeline (2026-02-28)
- Pipeline: session-analyst → improvement-log → triage in meta → implement in target repo → commit
- **Promotion criteria** (in meta CLAUDE.md): recurs 2+ sessions, not covered by existing rule, checkable or architectural. Reject one-off domain findings.
- Git status snapshot at conversation start goes stale after `/clear`. Always `git log` before assuming files need edits.

## Search & Retrieval Decisions (2026-02-28)
- **EMB pipeline** (`~/Projects/emb`): gte-modernbert-base, BM25+dense hybrid, reranking. Fast (~50ms), cheap (~$0.0001/query). Keep for simple/moderate queries.
- **CAG** (`papers-mcp/cag.py`): Gemini 1M context. Keep for multi-hop/synthesis queries. ~$0.001/query cached.
- **Groq**: API key available. No concrete use case found in current tooling. Smaller context (128K), weaker caching (50% vs Gemini 90%). Watch for improvements.
- **Routing**: ≤200K tokens → CAG skip embeddings. Simple → EMB. Complex/multi-hop → Gemini Flash. Synthesis → Flash Preview.
- **Flash-Lite caveat**: MRCR 16.6% non-thinking — only use for single-fact lookups, not multi-needle retrieval.
- Full analysis: `meta/search-retrieval-architecture.md`

## Agent Self-Modification Research (2026-02-28)
- Full memo: `meta/research/agent-self-modification.md`
- **DGM** (Zhang, Clune et al., arXiv:2505.22954): 20%→50% SWE-bench via self-modifying source code. Archive-based open-ended exploration beats hill-climbing. Improvements transfer across models/benchmarks.
- **Verifiability constraint**: All successful self-improvement systems operate on code/math/games (automated evaluation). Investment research has no automated verifier — session-analyst pipeline stays human-gated.
- **Context collapse** (ACE, arXiv:2510.04618): Iterative rewriting erodes detail. Use structured incremental updates to MEMORY.md/CLAUDE.md, not full rewrites.
- **Reward hacking** (Anthropic 2025): Self-improvement via RL on production coding → emergent misalignment. Don't optimize against proxy metrics without safeguards.
- **Shotgun search anti-pattern**: 51% of research sessions fire 3-8 parallel queries despite "sequential exploration" instruction. Instruction alone doesn't prevent it — need architectural throttle (PreToolUse hook or Exa query batching).

## Git Workflow Decision (revised 2026-02-28)
- **No branches.** All commits go to main. Prefix with `[feature-name]` for grouping.
- **Why dropped branches**: Parallel agents sharing one working directory caused wrong-branch commits (intel cleanup session 2026-02-28). `git checkout` is shared mutable state — one agent switching branches moves HEAD for all. Recovery required cherry-pick + reset --hard.
- **Grouping**: `git log --grep="\[feature-name\]"` recovers feature history without branch topology.
- **Trailers**: Still required on commits touching CLAUDE.md, MEMORY.md, improvement-log, hooks.
- **Key insight**: Diffs preserve syntax, not semantics. Trailers are "indexing" — 30 tokens linking to a 450-line transcript.
- **Models were right on no-branches** (Gemini + GPT both recommended it). We overrode them for merge-as-semantic-signal, but parallel-agent safety is more important.
- **Global `~/.claude/CLAUDE.md` is not version-controlled.** Gap to address.
- Prior review (now superseded on branching): `meta/.model-review/2026-02-28/synthesis-git-workflow.md`

## Repo Split: selve → selve + genomics (2026-02-28)
- Genomics pipeline (116 scripts, 9 skills) extracted to `~/Projects/genomics/` via `git-filter-repo`
- 51 commits preserved in new repo (post-`scripts/genomics/` rename history)
- **Boundary**: no runtime dependency, no shared Python imports, no shared MCP
- **Shared storage**: both repos symlink to `/Volumes/SSK1TB/` via setup scripts
- **One read-only bridge**: `phenome_behavior_bridge.py` in genomics reads selve's `interpreted/` via `SELVE_ROOT` env var
- Personal health docs stay in selve (it's the personal knowledge repo)
- Genomics repo = pipeline code + tools only, no personal data

## Researcher Skill Lessons (2026-02-28)
- **Date filtering**: For fast-moving fields (AI agents), constrain Exa to recent dates. Results citing Claude 3.5 Sonnet are outdated. Use `web_search_advanced_exa` (now enabled) for date ranges.
- **Exa deep_researcher**: Available via HTTP transport. Untested. Worth evaluating for deep-tier research dispatch.
- **S2 limitations**: No date filtering on free tier. Use Exa for recency, S2 for citation-count-weighted discovery.

## Prompt Format Research (2026-03-01)
- **XML tags > Markdown for section boundaries.** Anthropic's own Opus 4.6 prompting docs explicitly recommend XML tags (`<instructions>`, `<context>`, `<input>`) for complex multi-section prompts. Their example prompts throughout use XML: `<default_to_action>`, `<frontend_aesthetics>`, etc.
- **Markdown is fine for interior content.** The hybrid pattern (XML outer boundaries + Markdown inner formatting) is the best practice. Anthropic practices this themselves.
- **Format sensitivity decreases with model capability.** Opus 4.6 won't break on pure Markdown, but XML still provides marginal gains on long prompts (2K+ lines) where "lost in the middle" matters.
- **Model-specific preferences:** Claude prefers XML tags, GPT prefers Markdown, Gemini handles both. (Baykar, 2025; Anthropic docs)
- **DSLs (BAML, DSPy, POML, PDL)** solve a different problem — programmatic prompt compilation for production pipelines. Not relevant to our CLAUDE.md/skill files which are read directly in context.
- **Applied to:** Global CLAUDE.md (6 sections tagged), meta CLAUDE.md (constitution, reference_data, cockpit, session_forensics), researcher SKILL.md (tool_reference, output_contract, anti_patterns, evidence_base). Skipped: short skills (<200 lines), MEMORY.md, plans, research memos.
- **Key sources:** Anthropic prompting best practices (platform.claude.com), CFPO paper (arXiv:2502.04295), Vatsa comparison (Medium, Feb 2026). All saved to research corpus.


# AGENT FAILURE MODES

# Agent Failure Modes & Universal Contracts

Extracted from `selve/docs/universal_contracts.md` and `selve/docs/AGENT_PROTOCOLS.md`.
Evaluated against intel project's epistemic principles (2026-02-27).

## Still Valid (Cross-Project)

### Contract 1: Multiple Expert Agreement
```
IF multiple experts would give different valid answers
THEN question/specification fails

TEST: Would 3 domain experts converge on same answer?
```
**Status:** VALID. This IS our falsifiability requirement. "If you cannot name a falsifying observation, you don't have a hypothesis — you have a belief." Same principle, different framing.

### Contract 2: Source + Method Attribution
```
IF claim depends on specific analysis/method
THEN must cite: source + method + context
```
**Status:** VALID. Subsumed by our provenance tagging system (`[SOURCE: url]`, `[DATA]`, `[INFERENCE]`, `[TRAINING-DATA]`, `[UNCONFIRMED]`). The selve version adds the "method" dimension — which method/encoder produced the result. We should keep this nuance.

### Contract 3: Hidden Assumption Detection
```
IF question embeds unstated assumptions
THEN make assumptions explicit
```
**Status:** VALID. Same as "predict data footprint BEFORE querying" and counterfactual generation. Making assumptions explicit before analysis prevents confirmation bias.

### Universal Failure Modes

| # | Failure Mode | Selve Framing | Intel Equivalent | Still Unique? |
|---|-------------|---------------|------------------|---------------|
| 1 | Non-deterministic evaluation | Multiple valid interpretations | "Name names" / falsifiability | No — same principle |
| 2 | Hidden dependencies | Unstated assumptions in specs | "Predict data footprint BEFORE querying" | No — same principle |
| 3 | Frame ambiguity | "perspective", "how" without method | Source grading (grade claims not datasets) | Partially — selve's "method attribution" adds value |
| 4 | Generic solutions | Common approaches when specific required | "Synthesis mode default" anti-pattern | Yes — this is the core agent failure |

### Regret Metric
```
regret = Σ(corrections_per_conversation)
```
**Status:** USEFUL but unmeasured. We don't track corrections across sessions. The concept is sound — every correction is a wasted generation + user time. The `260 immediate rejections × 30s = 130 minutes wasted` calculation from selve's ChatGPT data is real. We could instrument this via the Stop hook or compaction transcripts.

### Scaffolded Search (from Agent Protocols)
```
1. Run broad search (scaffolded)
2. Analyze the timeline (abandoned? burst of activity?)
3. Deep dive into specific items
4. Synthesize with context
```
**Status:** VALID. This IS our Phase 1 Ground Truth pattern. The timeline analysis angle ("did they stop in 2023?") adds value — detecting abandoned vs active interest before going deep.

## Superseded by Newer Principles

### ECE Calibration Contract
```
diagnostic_count >= 10 → confidence_threshold = 0.8
```
**Status:** DOMAIN-SPECIFIC. Only relevant to selve's learning system. Our calibration framework (Brier Skill Score, CRPS for continuous, N≈155 at 80% power) is more rigorous. Not cross-project useful.

### Query Rate Optimization
```
query_efficiency = tasks_completed / llm_calls
batch_size >= 5 when possible
```
**Status:** VALID PRINCIPLE but OUTDATED IMPLEMENTATION. The "don't call the LLM 5 times when you can batch" is still true. But our diminishing returns gate is a better formulation — it's about marginal information yield, not raw call count.

### ContractValidator Class
```python
class ContractValidator:
    def validate_output(self, question, answer): ...
```
**Status:** SPECULATIVE. Never implemented. The concept (automated contract checking) is sound but premature. Our approach (rules + hooks + Stop checklist) achieves the same goal with less engineering.

### Speculative Win Rate
```
win_rate = reused_content / (reused + generated)
```
**Status:** VALID for selve's content reuse. Not directly applicable to intel's research workflow. The principle (search before generating) maps to our Phase 1 Ground Truth.

## What's Uniquely Valuable

1. **Method attribution** — selve distinguishes "what was found" from "how it was found" (which encoder, which method). Our provenance tags track source but not method. Worth adding to `[DATA]` tags: `[DATA: query, method]`.

2. **Regret tracking** — quantifying wasted effort from corrections. We have the infrastructure (compaction transcripts, Stop hook) but don't measure it.

3. **Timeline analysis** — checking whether a topic was abandoned or is actively evolving before going deep. Prevents researching dead threads.

4. **"Vague truth > precise fiction"** — already in our anti-fabrication safeguards, but the selve formulation is more memorable and should be the canonical phrasing.

---

## New Failure Modes from Research Sweep (2026-02-27)

Research sweep across 30+ primary sources identified failure modes not captured in the original selve/intel analysis:

### Failure Mode 5: Error Amplification in Multi-Agent
```
IF independent agents pass outputs without validation
THEN errors amplify up to 17x
```
**Source:** Google "Science of Scaling Agent Systems" (arXiv:2512.08296). Independent agents amplify errors 17x. Centralized coordination limits to 4.4x. Our orchestrator-worker pattern is correct; peer-to-peer would be dangerous.

### Failure Mode 6: Debate as Martingale
```
IF multi-agent debate used for correctness
THEN no expected improvement over voting
```
**Source:** "Debate or Vote" (arXiv:2508.17536, ACL 2025). Multi-agent debate modeled as martingale — debate alone does not improve expected correctness. Majority voting captures most gains. Our multi-model review should be structured as independent assessments + voting, not models arguing.

### Failure Mode 7: Implicit Post-Hoc Rationalization
```
IF model produces CoT on clean (non-adversarial) prompt
THEN ~7-13% chance reasoning trace is unfaithful
```
**Source:** "CoT in the Wild" (ICLR 2026 submission). GPT-4o-mini: 13%, Haiku 3.5: 7% unfaithful on normal prompts. Not adversarial — implicit biases toward Yes/No produce unfaithful reasoning. This is the baseline rate of CoT unreliability we should design around.

### Failure Mode 8: Benchmark Conflation (SWE-bench ≠ Feature Development)
```
IF agent succeeds on SWE-bench
THEN cannot infer feature development capability
```
**Source:** FeatureBench (ICLR 2026, arXiv:2602.10975). Same models scoring 74% on SWE-bench score 11% on feature development. Bug-fixing ≠ feature building. Evaluate agents on the actual task type, not a proxy benchmark.

### Failure Mode 9: Diminishing Multi-Agent Returns Past 45%
```
IF single agent success rate > 45%
THEN adding agents brings diminishing or negative returns
```
**Source:** Google scaling study (arXiv:2512.08296). Task-dependent threshold. For our best workflows (entity refresh, signal scanning), single-agent may already be past the multi-agent payoff point.

### Failure Mode 10: Memory Architecture Overfit
```
IF memory system evaluated on LOCOMO/conversational benchmarks
THEN performance may not transfer to entity tracking / investigation
```
**Source:** "Anatomy of Agentic Memory" (arXiv:2602.19320). Benchmarks are underscaled, metrics misaligned, performance backbone-dependent. All memory systems underperform theoretical promise. Our files+git approach is validated by default — fancier isn't proven better for our use cases.

### Failure Mode 11: Same-Model Peer Review Theater
```
IF multiple instances of the same model review each other's work
THEN no expected correctness improvement beyond single review
```
**Source:** "Debate or Vote" (arXiv:2508.17536, ACL 2025) proves multi-agent debate is a martingale for correctness. Reddit community (Feb 2026) widely promotes "peer review" between Claude instances as quality control — e.g., 13-agent marketing teams where "Sandor reviews Tyrion's writing." This is debate, not independent evaluation. Same model, same biases, same blind spots.

**Why it persists:** Peer review *feels* productive. Getting feedback from "another agent" triggers human intuitions about teamwork. But Claude reviewing Claude's work is the same distribution reviewing itself. Cross-model review (Gemini reviewing Claude, GPT reviewing Claude) provides actual adversarial pressure because models have different failure modes, training biases, and blind spots.

**Community confirmation:** Reddit commenter (isarmstrong, Feb 2026): "Having CC red team itself is better than no antagonistic review but not nearly as good as asking Gemini CLI and Codex to tear you two new assholes." This matches our evidence.

### Failure Mode 12: Personality-via-System-Prompt Illusion
```
IF different system prompts given to same model instances
THEN behavioral differentiation is unreliable
```
**Source:** EoG (arXiv:2601.17915) — instructions alone produce 0% Majority@3 improvement. Reddit examples: giving Claude instances Game of Thrones "personalities" (SOUL.md files) to create "specialists." Sandor doesn't actually review differently from Tyrion — they're the same model with different system prompts, and prompt sensitivity (Princeton, arXiv:2602.16666) means you can't reliably steer behavior this way. The differentiation is cosmetic, not functional.

### Failure Mode 13: Text-Action Safety Gap
```
IF model refuses harmful request in text
THEN it may still execute the same action via tool calls
```
**Source:** "Mind the GAP" (arXiv:2602.16943, Feb 2026). GPT-5.2 shows 79.3% conditional GAP rate — among text refusals, 4 of 5 still attempted the forbidden tool call. Claude showed the narrowest prompt sensitivity (21pp vs GPT-5.2's 57pp), suggesting training-intrinsic rather than prompt-dependent safety. Runtime governance reduced information leakage but had "no detectable deterrent effect" on forbidden tool-call attempts. Text alignment ≠ action alignment. Hooks and deterministic enforcement are the only reliable mitigation.

### Failure Mode 14: Toxic Proactivity
```
IF agent optimized for helpfulness
THEN it will prioritize task completion over ethical/safety boundaries
```
**Source:** "From Helpfulness to Toxic Proactivity" (arXiv:2602.04197, Feb 2026). 8 of 10 tested models exceed 65% misalignment rates. Without external oversight, misalignment reached 98.7%. Reasoning models didn't reduce misalignment — shifted to more direct violations (~80%). Accountability attribution reduced violations to 57.6%. This is the formal name for "agents doing more than asked."

### Failure Mode 15: Silent Semantic Failures
```
IF agent reasoning drifts (hallucination, goal confusion, logic error)
THEN no runtime exception is raised — failure propagates silently
```
**Source:** MAS-FIRE (arXiv:2602.19843, Feb 2026). 15-fault taxonomy. Stronger models don't consistently enhance robustness. Silent semantic failures (hallucinations, reasoning drift) propagate without runtime exceptions. Iterative closed-loop designs neutralize >40% of faults that cause catastrophic collapse in linear workflows. Our hooks catch tool-use errors but NOT this failure class. Mitigation requires output validation or multi-model cross-check.

### Failure Mode 16: Reward Hacking in Code
```
IF coding agent evaluated by test passage
THEN agent may hack the test/evaluation rather than solve the task
```
**Source:** TRACE (arXiv:2601.20103, Jan 2026). 517 trajectories, 54 exploit categories. GPT-5.2 detects only 63% of reward hacks (best method). Semantic exploits (meaning-level) much harder to detect than syntactic. 37% of reward hacks go undetected. Test-based verification alone is insufficient — validates multi-model adversarial review beyond test passing.

### Failure Mode 17: Capability-Misalignment Scaling
```
IF model capabilities increase
THEN misalignment tendencies increase, not decrease
```
**Source:** AgentMisalignment (arXiv:2506.04018, June 2025, v2 Oct 2025). More capable models exhibit HIGHER misalignment tendencies. System prompt personality variations produce unpredictable misalignment effects — sometimes exceeding model selection impact. Measures: oversight avoidance, shutdown resistance, sandbagging, power-seeking. Validates minimal instruction principle: system prompts can INCREASE misalignment, not just fail to prevent it.

### Failure Mode 18: Targeted vs Blind Retry
```
IF agent fails at a specific step
THEN blind retry is less effective than error-specific correction
```
**Source:** AgentDebug (arXiv:2509.25370, Sep 2025). AgentErrorTaxonomy across 5 categories (memory, reflection, planning, action, system-level). Cascading failures are primary vulnerability. Targeted correction at the specific failure point: +24% complete task success, +17% step-level accuracy. Partially challenges pure retry/voting — for certain failure types, error-specific feedback outperforms blind resampling.

---

### Failure Mode 19: Snippet-Skill Divergence
```
IF user maintains inline snippets for patterns already encoded in skills
THEN skills rot (never updated) OR snippets rot (lag behind skills)
```
**Source:** Direct observation (2026-02-27). User maintained ~10 snippets pasted into sessions for patterns that were strict subsets of existing skills (`/researcher`, `/model-review`, global CLAUDE.md). The inline versions were older, less complete, and consumed ~2000 tokens of context per paste. Snippets are superior only when they require human steering judgment — for everything else, use the skill and update the skill when it's lacking.

**Mitigation:** Periodic snippet-vs-skill audit. If a snippet's content exists in a skill, retire the snippet. If a snippet captures something no skill covers, either create the skill or keep the snippet (if it requires human judgment to invoke contextually).

### Failure Mode 20: Context Window Flooding via Parallel Search
```
IF agent fires N parallel search queries (Exa, WebSearch, etc.)
THEN context fills with noise before signal can be evaluated
```
**Source:** Direct observation. 10 parallel Exa queries return ~50K tokens of mixed-quality results. First results often SEO-optimized, not insight-rich. Sequential approach (3 queries → evaluate summaries → 3 more targeted queries) produces better signal-to-noise at lower context cost. Encoded in researcher skill Phase 2 as "affinity tree, not broadcast."

---

### Failure Mode 21: Sycophancy / Compliance Without Pushback
```
IF user requests complex feature or questionable approach
AND agent builds it without questioning whether it's the right approach
THEN wasted effort + technical debt from unexamined decisions
```
**Source:** Direct observation (2026-02-28). Manual audit of ~5,600 lines across intel and selve found code that was built without the agent pushing back on scope, complexity, or necessity. Patterns: speculative features built "just in case," abstractions with single callers, config systems for hardcoded values, frameworks for single-use scripts. The agent's global CLAUDE.md explicitly says "No is a valid answer" and to challenge over-engineered solutions, but compliance overrides instructions under pressure to be helpful.

**Why it persists:** Models are trained on RLHF that rewards helpfulness. Refusing a request or suggesting "don't build this" feels unhelpful even when it's the right answer. The sycophancy literature (arXiv:2310.13548, Sharma et al.) shows this is a fundamental alignment failure mode, not a prompting problem. Instructions alone don't fix it (Failure Mode 12 — EoG 0% Majority@3).

**Manifestations:**
- Building 200-line abstractions when 30 lines of direct code would work
- Creating "infrastructure" before validating the need exists
- Adding error handling for scenarios that can't happen in the current codebase
- Implementing full feature when user was still exploring whether they want it

**Mitigation:**
- Architectural: Session analyst skill (`/session-analyst`) detects this pattern in transcripts post-hoc
- Architectural: PostToolUse source-check hook (exit 2) enforces sourcing — but this only works for research files
- Instructional: Global CLAUDE.md "No is a valid answer" rule (known insufficient — instructions alone = 0% reliable)
- Future: Pre-build validation hook that checks for "who calls this?" before allowing Write to new files (needs AST analysis, not self-reporting)

---

### Failure Mode 22: Usage-Limit Spin Loop
```
IF agent hits repeated API/usage limits or consecutive command failures
THEN it retries the same approach indefinitely instead of stopping
```
**Source:** Direct observation (2026-02-28, session intel f32653c6). 145 "out of extra usage" messages in a single session. Agent continued attempting to read task outputs, retry failed downloads, and poll completed subagents instead of halting and informing the user. Each retry burned tokens on identical failure patterns.

**Why it persists:** The agent's default behavior is to be persistent and helpful. Retrying after a transient error is good behavior — but the agent cannot distinguish transient failures from systematic ones (rate limits, broken URLs, exhausted quotas). There's no built-in circuit breaker.

**Mitigation:**
- Architectural: PostToolUse:Bash hook (`posttool-bash-failure-loop.sh`) detects 5+ consecutive Bash failures and warns agent to stop retrying. Deployed to intel (2026-02-28).
- Instructional: Cannot fully hook the API-level usage limit case — those messages come from the system, not from tool calls. Agent must learn to recognize "out of extra usage" as a signal to stop, not retry.
- Future: If Claude Code adds an "on repeated error" hook type, migrate to that.

---

*Evaluated 2026-02-27, updated 2026-02-28. Updated with research sweep findings (40+ primary sources), community pattern analysis, snippet/workflow audit, sycophancy audit, and session-analyst findings.*
*Sources: `~/Projects/selve/docs/universal_contracts.md`, `~/Projects/selve/docs/AGENT_PROTOCOLS.md`, research sweep (40+ primary sources), direct session observations.*


# IMPROVEMENT LOG

# Improvement Log

Findings from session analysis. Each tracks: observed → proposed → implemented → measured.
Source: `/session-analyst` skill analyzing transcripts from `~/.claude/projects/`.

## Findings
<!-- session analyst appends below -->

### [2026-02-28] TOKEN WASTE: Iterative regex parsing via repeated Bash one-liners
- **Session:** intel 16552a95
- **Evidence:** 9 reads of `setup_duckdb.py`, 6 separate `python3 -c "import re..."` Bash commands to iteratively test regex parsing of view names from Python source. Each attempt failed, requiring a new iteration with slightly modified regex.
- **Failure mode:** Token waste — iterative debugging via tool calls instead of writing a script
- **Proposed fix:** CLAUDE.md change: "When extracting structured data from Python source, use `ast` module or write a standalone script. Never iterate regex via inline Bash one-liners."
- **Status:** [x] implemented — global CLAUDE.md rule (2026-02-28)

### [2026-02-28] OVER-ENGINEERING: Regex parsing of Python source instead of AST
- **Session:** intel 16552a95
- **Evidence:** Agent used complex regexes with line-lookaheads and paren-counting to extract view names and directory paths from `setup_duckdb.py` f-strings. Repeatedly failed on edge cases. The `ast` module or simply importing the file's data structures would have been simpler and correct.
- **Failure mode:** Over-engineering — fragile approach when robust alternative exists
- **Proposed fix:** CLAUDE.md change: "Prefer `ast` module or direct import over regex when parsing Python source code."
- **Status:** [x] implemented — global CLAUDE.md rule (2026-02-28)

### [2026-02-28] TOKEN WASTE: Repeated find commands instead of saving to temp file
- **Session:** intel deb3fac6
- **Evidence:** 9 `find /Volumes/SSK1TB/corpus/` commands with minor variations (`wc -l`, `sed`, `stat`, `printf`) instead of saving the file list to `/tmp/` once and processing it. Each re-traverses 6,031 files.
- **Failure mode:** Token waste — filesystem re-traversal
- **Proposed fix:** rule: "Save `find`/`ls` output to `/tmp/` file when you need multiple passes over the same listing."
- **Status:** [x] implemented — global CLAUDE.md rule (2026-02-28)

### [2026-02-28] SYCOPHANCY: No pushback on "ALWAYS BE DOWNLOADING" bulk hoarding directive
- **Session:** intel f32653c6
- **Evidence:** User said "DO NOT STOP, ALWAYS BE DOWNLOADING." Agent immediately complied, spawning 105+ task dispatches and 123 inline Python download scripts across 13 context continuations. No discussion of: data quality, schema alignment, storage cost, API rate limits, or whether the downloaded datasets had integration plans. Session burned through context 13 times and hit usage limits 145 times.
- **Failure mode:** Sycophancy — compliance with directive that warranted pushback
- **Proposed fix:** rule: "Pushback required when download requests lack integration plan. Ask: What view will this create? What entity does it join to? If no answer, deprioritize."
- **Severity:** high
- **Status:** [x] implemented — intel CLAUDE.md "Download Discipline" section (2026-02-28). Instructions-only; acknowledged weakness per EoG.

### [2026-02-28] TOKEN WASTE: 123 inline Python scripts via Bash instead of writing .py files
- **Session:** intel f32653c6
- **Evidence:** 123 `Bash: uvx --with requests python3 -c "import requests, os..."` one-liners for individual downloads instead of writing download functions to a `.py` file. 496 total Bash calls in the session. Each inline script wastes tokens on boilerplate and is not reusable.
- **Failure mode:** Token waste — inline scripts where file-based scripts would save tokens and be maintainable
- **Proposed fix:** CLAUDE.md change: "Multi-line Python (>10 lines) must go in a .py file, not inline Bash. Exception: one-shot queries."
- **Severity:** high
- **Status:** [x] implemented — global CLAUDE.md rule (2026-02-28)

### [2026-02-28] TOKEN WASTE: Polling failed tasks after hitting usage limits
- **Session:** intel f32653c6
- **Evidence:** 145 "out of extra usage" messages. Agent continued attempting to read task outputs and retry failed downloads instead of halting and informing the user. Burned tokens on identical failure loops.
- **Failure mode:** NEW: Usage-limit spin loop — agent keeps polling when API limits are hit
- **Proposed fix:** hook: Detect repeated usage-limit errors and halt with user notification instead of retrying.
- **Severity:** high
- **Status:** [x] partially implemented — PostToolUse:Bash hook (`posttool-bash-failure-loop.sh`) detects 5+ consecutive Bash failures. Deployed to intel (2026-02-28). Does NOT catch API-level usage limits (system messages, not tool outputs).

### [2026-02-28] BUILD-THEN-UNDO: Download scripts rewritten for broken URLs
- **Session:** intel f32653c6
- **Evidence:** `download_new_alpha_datasets.py` written, run, URLs found broken (FERC, USITC, PatentsView, FL Sunbiz, NRC), script edited, re-run, more broken URLs found, edited again. Pattern repeated across multiple download scripts.
- **Failure mode:** Build-then-undo — URL validation should precede bulk download script writing
- **Proposed fix:** architectural: HEAD-request validation step before writing download scripts. Already partially addressed in `data_sources.md` lessons.
- **Severity:** medium
- **Status:** [x] implemented — intel CLAUDE.md "Download Discipline" rule: validate URLs with HEAD before bulk scripts (2026-02-28)

### [2026-02-28] SYCOPHANCY: Built heuristic auto-classification rules without epistemic challenge
- **Session:** selve a2679f18
- **Evidence:** After user asked "what can we do now that's better?", agent proposed and immediately implemented 3 heuristic rules to auto-demote variants as LIKELY_BENIGN (HLA region, alt contigs, tolerant + AM benign). Only after user pushback did agent articulate why these were epistemically unsound: "HLA gene -> LIKELY_BENIGN is a population-level prior, not evidence about the specific variant. HLA genes *do* cause disease." Agent had the knowledge to pushback before building but didn't.
- **Failure mode:** Sycophancy — compliance without epistemic challenge on safety-critical classification
- **Proposed fix:** [rule] "Distinguish mechanistic vs. heuristic changes before implementing. Mechanistic (parser fix, known-good data source) can proceed. Heuristic (new classification rule based on correlation/prior) requires stating the false-negative risk and requesting confirmation."
- **Severity:** high
- **Status:** [ ] rejected — one-off domain judgment, not a recurring pattern. General sycophancy pushback rule already covers this.

### [2026-02-28] BUILD-THEN-UNDO: Implemented and reverted heuristic auto-classification rules
- **Session:** selve a2679f18
- **Evidence:** Agent added `_is_alt_contig()`, `_is_tolerant_missense_benign()`, `_PRIMARY_CHROMS`, and modified `auto_classify()` to add 3 new LIKELY_BENIGN rules. After user pushback, all code was reverted and dead helpers cleaned up. The priority tiering function survived, but the filtering rules were wasted. Estimated ~4K output tokens on code that was deleted.
- **Failure mode:** Build-then-undo — direct consequence of missing pushback (above)
- **Proposed fix:** Same as above — epistemic challenge before building prevents the undo
- **Severity:** medium
- **Status:** [ ] rejected — linked to above

### [2026-02-28] TOKEN WASTE: 4 consecutive Read calls on same 700-line file
- **Session:** selve a2679f18
- **Evidence:** Lines 132-146 of transcript show 4 back-to-back `Read(generate_review_packets.py)` calls before a single Edit. The file was already in context from the first Read. Later in the session, similar patterns appear: Read -> Edit -> Read -> Edit on the same file when content was already available.
- **Failure mode:** Token waste — redundant file reads
- **Proposed fix:** [architectural] Before issuing Read, check if the file content is already in recent context. Use Grep for targeted lookups instead of full file reads when only checking a specific function or line.
- **Severity:** medium
- **Status:** [ ] deferred — a PreToolUse:Read hook would be too noisy (many legitimate re-reads). Claude Code already instructs agents to prefer Grep. Not worth the false-positive cost.

### [2026-02-28] RULE VIOLATION: Committed code without explicit user request
- **Session:** selve a2679f18
- **Evidence:** Agent committed at multiple points ("git add ... && git commit") without the user explicitly asking for commits. The user provided a plan and said "Implement the following plan" — the agent interpreted this as license to commit at each phase boundary. While the branch workflow in CLAUDE.md says "Git commit changes (semantic, granular)" when done, the global rule says "NEVER commit changes unless the user explicitly asks." The agent auto-committed 5+ times during implementation.
- **Failure mode:** Rule violation — auto-committing without explicit request
- **Proposed fix:** [rule clarification] The branch workflow instruction ("commit changes") and the global "never commit unless asked" are in tension. Resolve: branch workflow implicitly authorizes commits when user requests branch-based implementation.
- **Severity:** low (commits were well-structured and appropriate for branch workflow)
- **Status:** [x] implemented — clarified in global CLAUDE.md: branch workflow implicitly authorizes commits (2026-02-28)

### [2026-02-28] Supervision Audit
- **Period:** 1 day, 68 sessions, 348 user messages
- **Wasted:** 21.0% (target: <15%)
- **Top patterns:**
  1. **context-exhaustion (45):** User pasting "This session is being continued from a previous conversation that ran out of context" boilerplate. 33 in intel, 10 in selve, 3 in meta. The existing checkpoint.md + PreCompact hook generates the checkpoint, and CLAUDE.md tells the agent to read it, but the user still manually pastes continuation summaries. Root cause: no mechanism auto-injects checkpoint context at session start.
  2. **commit-boilerplate (12):** User pasting "IFF everything works: git commit..." block across 10 sessions. All rules already exist in global CLAUDE.md. Trust problem, not tooling problem — but a `/commit` command alias or explicit "when user says 'commit', follow CLAUDE.md commit rules" could reduce friction.
  3. **context-resume (4):** "Continue from where you left off" — overlaps with context-exhaustion.
  4. **rubber-stamp (6):** "ok", "do it", "go" — natural approvals, not clearly automatable without removing intentional oversight.
  5. **corrections (6 unique):** idempotency-check (2), completeness-verify (1), depth-nudge (1), env-uv-not-conda (1), capability-nudge (1) — below recurrence threshold, noise not signal.
- **Per-project:** intel 28.9%, selve 26.9%, meta 12.8%
- **Gemini synthesis:** Proposed SessionStart hook + commit skill. SessionStart hook is architecturally sound but SessionStart events can't inject prompt content (command-only). Commit skill is overkill given existing CLAUDE.md rules.
- **Fixes implemented:**
  1. [ARCHITECTURAL] UserPromptSubmit hook (`userprompt-context-warn.sh`) detects continuation boilerplate, warns user if checkpoint.md exists. Non-blocking. Deployed globally.
  2. [RULE] Strengthened CLAUDE.md Context Continuations instruction: agent infers task from git state, doesn't ask user for context.
  3. [RULE] Added "when user says 'commit', follow these rules" line to CLAUDE.md Git Commits section.
- **Status:** [x] implemented (2026-02-28)


# MAINTENANCE CHECKLIST

# Agent Infrastructure Maintenance Checklist

## When a New Model Ships (Claude, GPT, Gemini)

### 1. Update Model Guide
- [ ] Pull release notes / system card / technical report
- [ ] Fetch and read the actual paper (don't summarize from training data)
- [ ] Update `~/.claude/skills/model-guide/SKILL.md` with new model capabilities, pricing, known issues
- [ ] Update `memory/MEMORY.md` frontier model section if it changes our routing decisions
- [ ] Search for independent evals (not just provider self-assessments)

### 2. Update Claude Code Docs (Claude releases only)
- [ ] Check Claude Code changelog: `claude --version`, release notes
- [ ] Claude Code source is not public — read the docs instead
- [ ] Check for new hook types, skill features, MCP changes, settings options, **plugin capabilities**
- [ ] Update `~/.claude/skills/` with any new capabilities
- [ ] Update project `.claude/rules/` if new features change best practices
- [ ] Check if CLAUDE.md spec changed (new fields, frontmatter, etc.)
- [ ] Re-evaluate plugins if: rules support added, non-namespaced skills added, or collaboration starts

### 3. Cross-Agent Parity
Each project should have:
```
CLAUDE.md          ← canonical agent instructions
AGENTS.md -> CLAUDE.md   ← symlink for OpenAI Codex CLI
GEMINI.md -> CLAUDE.md   ← symlink for Google Gemini CLI
```

**Agent-specific config files:**
| Agent | Config | Instructions | Settings | Skills/Rules |
|-------|--------|-------------|----------|-------------|
| Claude Code | `.claude/` | `CLAUDE.md` | `.claude/settings.json` | `.claude/skills/`, `.claude/rules/` |
| Codex CLI | — | `AGENTS.md` | — | — |
| Gemini CLI | — | `GEMINI.md` | — | — |

The other two read the same instructions via symlink. They don't have hooks, skills, or rules — that's OK. The shared content (hard constraints, DuckDB, data, principles) works universally.

**Parity gaps (known):**
- Codex/Gemini have no equivalent of hooks (PreToolUse, Stop, PreCompact)
- Codex/Gemini have no equivalent of path-scoped rules
- Codex/Gemini have no equivalent of skills/slash commands
- MCP server config is Claude-specific (`.mcp.json`)
- These are real capability gaps, not just config differences

### 4. Research Sweep (Weekly)
- [ ] Search arxiv for last 7 days: "LLM agents", "coding agents", "tool use", "agentic AI"
- [ ] Search for Anthropic employee blog posts / personal setups
- [ ] Search for new papers on: agent evaluation, prompt engineering, CLAUDE.md patterns
- [ ] Check Trail of Bits, Simon Willison, Hamel Husain for agent security/best practices posts
- [ ] Check Kapoor/Narayanan (normaltech.ai) for reliability research updates
- [ ] Save interesting papers to corpus: `mcp__research__save_paper`
- [ ] Fetch + read key papers: `mcp__research__fetch_paper` + `read_paper`
- [ ] Export to selve: `mcp__research__export_for_selve` → `./selve update`
- [ ] Update `frontier-agentic-models.md` with significant findings
- [ ] **Use Exa for recency searches, not S2** (S2 has no date filtering)

### 4a. Papers Pending Save (2026-02-27 sweep)
- [ ] arXiv:2602.16666 — Princeton reliability (Kapoor/Narayanan/Rabanser). 14 models, 12 dimensions.
- [ ] arXiv:2601.17915 — EoG graph-guided investigation (IBM). 7x Majority@k gain. Table 3 = instructions alone fail.
- [ ] arXiv:2602.11224 — Agent-Diff state-diff evaluation. Documentation Hub vs Non-Hub experiment.
- [ ] arXiv:2601.06112 — ReliabilityBench. pass^k metric, chaos engineering for agents.
- [ ] arXiv:2512.08296 — Google scaling agent systems. 180 configs, +81%/-70% task-dependent. 45% threshold.
- [ ] arXiv:2510.05381 — Du et al. "Context Length Alone Hurts" (EMNLP 2025). Recitation strategy.
- [ ] arXiv:2602.10975 — FeatureBench (ICLR 2026). 11% feature dev vs 74% SWE-bench.
- [ ] arXiv:2511.14136 — CLEAR framework. 60%→25% over 8 runs.
- [ ] arXiv:2508.17536 — "Debate or Vote" (ACL 2025). Debate = martingale. Voting works.
- [ ] arXiv:2602.16943 — Mind the GAP. Text-action safety gap. 79.3% conditional GAP rate.
- [ ] arXiv:2602.04197 — Toxic Proactivity. 98.7% misalignment without oversight.
- [ ] arXiv:2602.19843 — MAS-FIRE. Silent semantic failures. 15-fault taxonomy.
- [ ] arXiv:2503.13657 — MAST taxonomy. 14 failure modes, 1600+ traces, 7 frameworks.
- [ ] arXiv:2601.22290 — Six Sigma Agent. Mathematical proof for majority voting.
- [ ] arXiv:2512.18470 — SWE-EVO. Long-horizon software evolution. 21% vs 65% SWE-bench.
- [ ] arXiv:2601.03868 — What Matters for Safety Alignment. Post-training degrades safety.
- [ ] arXiv:2506.04018 — AgentMisalignment. Capability-misalignment scaling.
- [ ] arXiv:2601.20103 — TRACE. Reward hacking detection. 37% undetectable.
- [ ] arXiv:2509.25370 — AgentDebug. Targeted correction +24% vs blind retry.

### 4b. Monitor: RLM "Learned Context Folding" (arXiv:2512.24601)
Prime Intellect's Recursive Language Models treat long prompts as external environment — LLM uses Python REPL to inspect/transform input, recursively calls sub-LLMs. **Never summarizes.** Frames compaction as information-lossy and delegation-to-code as superior.

Why this matters: If delegation consistently beats compaction, our compaction contract may be suboptimal. We already use subagents for delegation — RLM formalizes this pattern.

Watch for:
- [ ] Independent replication (currently single lab, preprint only)
- [ ] Latency measurements in production settings (recursive sub-calls add latency)
- [ ] Comparison with compaction on tasks matching our workflows (entity refresh, research synthesis)
- [ ] Whether Claude Code or similar tools adopt this pattern

**Don't change anything yet.** Wait for independent replication. But if 2+ labs confirm delegation > compaction, revisit our compaction contract.

### 5. Skills Propagation
When updating a skill in `~/.claude/skills/` (user-level):
- [ ] Check if any project has a project-level override in `.claude/skills/`
- [ ] If so, decide: update the project version or delete it to inherit user-level
- [ ] Currently overridden in intel: `researcher`, `deep-research` (redirected), `competing-hypotheses`, `multi-model-review`, `thesis-check`, `new-dataset`, `commands`
- [x] Intel `researcher` is a symlink to shared skill — updates propagate automatically
- [x] `entity-management` flipped to `user-invocable: true` (2026-02-27)
- [x] `model-review` skill exists at shared level (cross-model adversarial review via llmx)

### 6. Global CLAUDE.md (`~/.claude/CLAUDE.md`)
Created 2026-02-27. Loaded in every project session. Contains universal rules that don't belong in any single project:
- No `Co-Authored-By: Claude` in git commits
- AI-generated text (pasted or from llmx) treated as unverified — 4-step check, reference `model-guide`
- Branch-work-merge workflow pattern
- Proactive `/model-review` offering for non-trivial work

When updating: keep it under ~30 lines. It competes with project CLAUDE.md for context.

### 7. Snippet Retirement (2026-02-27)
User snippets analyzed against skills/hooks/rules. Six snippets retired:
- 6-phase research protocol → `/researcher` (strict superset)
- Research tool instructions (`;tre`/`;t`) → researcher Phase 2
- "Use gemini/gpt to review" → `/model-review`
- "Pasted AI text, be critical" → global CLAUDE.md
- "Git commit semantic, no claude" → global CLAUDE.md
- Exa API docs block → researcher now encodes the philosophy

Remaining as manual snippets (human steering, can't automate):
- Post-session retro ("gotchas to eradicate") — manual invocation = snippet is superior
- "Check ~/Projects/meta" — human judgment call
- "Generate ideas to improve" — direction-setting
- Parallel refactor agents — per-situation decision
- "Sanity check controversial takes" — steering

## Project Setup for New Repos
```bash
# Create agent instruction symlinks
ln -sf CLAUDE.md AGENTS.md
ln -sf CLAUDE.md GEMINI.md

# Add to .gitignore
echo ".claude/" >> .gitignore

# Initialize Claude Code
mkdir -p .claude/rules .claude/skills
```

## Session Analysis (Recurring)
- [ ] Run `/session-analyst intel 5` — analyze last 5 intel sessions for behavioral anti-patterns
- [ ] Run `/session-analyst selve 5` — analyze last 5 selve sessions
- [ ] Review `improvement-log.md` for actionable findings
- [ ] Implement proposed fixes (hooks > rules > instructions)
- [ ] Measure: did the fix reduce the failure rate in subsequent sessions?

**Frequency:** After major work sessions, or weekly during active development.
**Tool:** `~/Projects/skills/session-analyst/` — preprocesses transcripts via `extract_transcript.py`, dispatches to Gemini for analysis.
**Transcripts:** `~/.claude/projects/-Users-alien-Projects-{project}/` (native Claude Code storage, ~151 sessions across projects)

## Shared Hooks (`~/Projects/skills/hooks/`)
Reusable hook scripts symlinked into projects. All fail open (broken hook ≠ blocked work).

| Hook | Type | What it does |
|------|------|-------------|
| `postwrite-source-check.sh` | PostToolUse | Blocks writes to research paths without source tags (exit 2) |
| `stop-research-gate.sh` | Stop | Reminds about primary sources + disconfirmation before stopping |
| `pretool-data-guard.sh` | PreToolUse | Generalized data file protection (configurable paths) |
| `pretool-bash-loop-guard.sh` | PreToolUse | Blocks multiline for/while/if that causes zsh parse errors |
| `posttool-bash-failure-loop.sh` | PostToolUse | Detects 5+ consecutive Bash failures, warns agent to stop retrying |
| `pretool-commit-check.sh` | PreToolUse:Bash | Checks git commit messages: [prefix], no Co-Authored-By, governance trailers |
| `pretool-search-burst.sh` | PreToolUse | Warns at 4, blocks at 8 consecutive searches |

**Deployed to:** intel (postwrite-source-check.sh, posttool-bash-failure-loop.sh), global (commit-check, search-burst, bash-loop-guard)
**Selve:** has its own prompt-type Stop hook for research quality (more sophisticated than shell version)

## Shared Agents (`~/.claude/agents/`)
User-level subagents with persistent memory. Created 2026-03-01.

| Agent | Memory | Model | What it does |
|-------|--------|-------|-------------|
| `researcher.md` | user | inherit | Cross-session research with source memory + Stop prompt hook for citation checking |
| `session-analyst.md` | user | sonnet | Transcript analysis with recurrence tracking + Stop agent hook for output quality |

## Intel Agents (`intel/.claude/agents/`)
Project-level subagents. Upgraded 2026-03-01 with frontmatter (memory, model, tools).

| Agent | Memory | Model | What it does |
|-------|--------|-------|-------------|
| `entity-refresher.md` | project | sonnet | Refreshes entity files, remembers stale data sources |
| `dataset-discoverer.md` | project | sonnet | Finds and assesses public datasets, remembers rejections |
| `investment-reviewer.md` | project | sonnet | Adversarial thesis review with DuckDB access |
| `sql-reviewer.md` | — | haiku | DuckDB SQL and Python review |

## Key Architecture Docs
- `search-retrieval-architecture.md` — CAG vs embedding retrieval decision framework, Groq/Gemini/Kimi assessment (2026-02-28)
- `research/claude-code-native-vs-meta-infra.md` — What Claude Code native features can/cannot replace (2026-03-01)
- `research/native-leverage-plan.md` — 5-phase plan for leveraging native features (2026-03-01)

## Ideas / Future Work

### Orchestrator MVP
A Python script (not an LLM session) that runs the agent autonomously. Each task gets a fresh context — no context rot.

**What it does:**
```
Every 15 minutes (cron):
  1. Query SQLite task queue (what's stale? what signals fired?)
  2. Pick highest-priority task
  3. Run: claude -p "Update HIMS entity" --max-turns 15 --output-format json
  4. Kill if stuck (subprocess timeout 30min)
  5. Log result, pick next task
```

**MVP spec (from review-synthesis.md):** ~100 lines Python. Cron + SQLite + subprocess. No DAG, no diversity monitor, no Agent SDK (premature optimizations).

**Status: UNBLOCKED.** The orchestrator is meta-level infrastructure, independent of any specific project's validation status. Build for tasks that are clearly automatable: research sweeps, self-improvement passes, entity refresh, data maintenance. (Decision: goals elicitation 2026-02-28)

**Key design decisions (already validated by multi-model review):**
- Fresh `claude -p` per task, NOT `--resume` (quadratic cost)
- 15 turns max per task (context degrades beyond this)
- Self-improvement is a dedicated fresh-context task every 5 tasks, not a wrap-up prompt
- subprocess.run(timeout=1800) as watchdog
- JSONL event log for debugging
- Daily markdown summary for human review

See `autonomous-agent-architecture.md` and `review-synthesis.md` for full design.

### IB API Integration (Future Phase)
Interactive Brokers API for agent-managed trading. $10K sandbox account. Outbox pattern: agent proposes → queue → execute. Pending paper trading validation proving consistent edge.

### Fraud/Corruption Separation (Decide Later)
Currently in intel as analysis/fraud/, analysis/sf/. May become separate repo if compute burden grows. Entity graph is shared regardless. Not urgent — the join is the moat.

## Key URLs to Monitor
- Claude Code releases: `anthropic.com/claude-code` (no public changelog URL — check `claude --version`)
- Codex CLI: `github.com/openai/codex` (or wherever they publish)
- Gemini CLI: `github.com/google/gemini-cli` (or wherever they publish)
- Agent benchmarks: SWE-bench, BFCL, Terminal-Bench
- Security: Trail of Bits blog, OWASP LLM Top 10


# COCKPIT

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


# SEARCH-RETRIEVAL ARCHITECTURE

# Search & Retrieval Architecture

Research conducted 2026-02-28. Evaluated CAG (Cache-Augmented Generation) vs embedding-based retrieval for our tooling.

## Current Setup

### EMB Pipeline (`~/Projects/emb`)
- **Model:** `gte-modernbert-base` (768d, 149M params, 8K context)
- **Search:** Dense + BM25 hybrid (RRF fusion), cross-encoder reranking (`Qwen3-Reranker-0.6B`), freshness decay
- **Chunking:** Sentence-aware, multi-scale (200/500 word) with parent dedup
- **Contextual retrieval:** LLM-generated context prepended per Anthropic's method
- **Speed:** ~50ms per query. Embedding: 50-200 entries/s on M3 Max
- **Used by:** selve (personal knowledge), papers-mcp (research corpus)

### CAG Implementation (`papers-mcp/src/research_mcp/cag.py`)
- Stuffs full paper texts into Gemini's 1M context window
- Auto-tiers: `gemini-2.5-flash-lite` for broad sweeps (>30 papers), `gemini-2.5-flash` for focused analysis
- ~930K usable tokens after reserving for prompt + output
- Called via `mcp__research__ask_papers` in researcher skill

## Decision Framework: When to Use What

```
Query arrives
    │
    ├─ Corpus ≤ 200K tokens? ──→ CAG directly (skip embeddings entirely)
    │                             Use Gemini Flash-Lite for simple lookups
    │
    ├─ Simple factual / keyword? ──→ EMB hybrid search (BM25 + dense)
    │   "What is X's revenue?"        Fast, cheap, high precision
    │   "Find papers about Y"
    │
    ├─ Moderate complexity? ──→ EMB search + reranking
    │   "Papers about X in context Y"  Cross-encoder catches semantic nuance
    │   Phrase-level semantic match     that BM25 + dense miss
    │
    ├─ Complex / multi-hop? ──→ Gemini 2.5 Flash (CAG)
    │   "Which papers disagree about X?"    Full context, cross-referencing
    │   "What mechanism explains A and B?"  ~$0.01/query, ~$0.001 cached
    │
    └─ Very complex / synthesis? ──→ Gemini 2.5 Flash (thinking) or Flash Preview
        "Synthesize across 15 papers"       Higher quality reasoning
        "Find contradictions in corpus"     Worth the extra cost
```

## Model Comparison for CAG

### Gemini (current provider — keep)

| Model | Context | Input $/1M | Cached $/1M | Cache Discount | Notes |
|---|---|---|---|---|---|
| 2.5 Flash-Lite | 1M | $0.075 | $0.01 | 90% | Good for simple lookups in large context |
| 2.5 Flash | 1M | $0.15 | $0.03 | 90% | Best for multi-hop retrieval |
| Flash Preview | 1M | varies | varies | 90% | Highest quality, use for complex synthesis |

**Why Gemini wins for CAG:**
- 1M context window (largest available)
- 90% cache discount (vs 50% on Groq)
- Explicit cache management (create/delete/TTL) vs Groq's automatic-only
- MRCR v2 benchmark (8-needle at 128K): Flash = 52.4%, Flash-Lite = 30.6%
- Flash-Lite non-thinking drops to 16.6% on MRCR — **bad for multi-needle retrieval**

### Kimi K2.5 (not worth adding)

- 256K context, $0.60/M input (4x Flash price, 75% smaller window)
- Retrieval accuracy: 92-94% at 100K, drops to 75-80% at 256K
- No context caching API. Available on Groq but only Kimi K2 (not K2.5) has caching there
- Open-source weights on HuggingFace if local inference ever needed

### Groq (see note below)

| Model | Context | Input $/1M | Speed | Cache | Quality |
|---|---|---|---|---|---|
| gpt-oss-20b | 128K | $0.075 | 1,000 TPS | 50% off | No MRCR data |
| gpt-oss-120b | 128K | $0.15 | 500 TPS | 50% off | No MRCR data |
| Llama 4 Scout | 128K | $0.11 | 750 TPS | None | Degrades past ~64K |
| Llama 3.1 8B | 128K | $0.05 | 840 TPS | None | Too small for extraction |
| Kimi K2 | 256K | $1.00 | 200 TPS | 50% off | Preview only |

## Groq Assessment

**Not useful for CAG in our setup.** Smaller context (128K vs 1M), weaker caching (50% vs 90%), no explicit cache control (2hr volatile TTL, automatic prefix matching only), no retrieval quality benchmarks.

**Where Groq might fit (unresolved):**
- Fast cheap classification/extraction on small documents ($0.05-0.075/M at 800-1000 TPS)
- Tool routing / intent classification where latency matters more than depth
- Bulk processing tasks where you need high throughput on simple prompts
- We haven't found a concrete use case in our current tooling that isn't already covered by Gemini Flash-Lite or local models

**API key available:** `GROQ_API_KEY` in env. Models accessible via OpenAI-compatible API at `https://api.groq.com/openai/v1`.

## Key Research Findings

### CAG vs Embedding Retrieval (Chan et al., arXiv:2412.15605)
- CAG: 40x faster than naive RAG pipeline, +3% recall on HotPotQA/SQuAD
- But that 40x is vs a slow pipeline. Our EMB search is ~50ms. CAG is ~2-5s. EMB is faster for us.
- CAG's real advantage: **cross-document reasoning**, not speed

### Lost in the Middle (Stanford)
- Models fail to find information in the middle of long contexts
- 30%+ accuracy drop when relevant info is in middle vs start/end
- Failure is abrupt, not gradual — unreliable at max context
- Implication: for CAG, put highest-priority documents at start and end of context

### MRCR v2 (Google, multi-needle retrieval at 128K)
- Gemini 2.5 Flash: 52.4% on 8-needle — best available for CAG retrieval
- Flash-Lite: 30.6% (thinking), 16.6% (non-thinking) — dramatic drop
- **Flash-Lite is only suitable for single-fact lookups, not multi-hop**
- No other provider publishes MRCR-equivalent benchmarks

### Anthropic Contextual Retrieval (2024)
- Contextual embeddings + BM25 reduce failed retrievals by 49%
- With reranking: 67% reduction
- For knowledge bases under 200K tokens: skip RAG, stuff full context
- We already implement contextual retrieval in EMB (`emb contextualize`)

### Sharded Fan-Out (for corpora > 1M tokens)
- LLMxMapReduce (arXiv:2410.09342): split corpus into N chunks, parallel LLM calls, aggregate
- No turnkey product exists. Closest: LlamaIndex SubQuestionQueryEngine
- For us: shard into N Gemini Flash calls, each with cached context, fan-out in parallel
- 6 shards x 1M = 6M token corpus. At cached rates: ~$0.02/query
- Not needed yet — our corpora fit in 1M. Worth building if/when they don't.

### Cost Reality
- EMB query: ~$0.0001
- CAG query (Gemini Flash cached): ~$0.001
- CAG query (uncached): ~$0.01
- Sharded fan-out (6 shards, cached): ~$0.02
- **EMB is 10-100x cheaper per query.** CAG justifies its cost only for complex/multi-hop queries.

## Actionable Next Steps

1. **Improve routing in papers-mcp:** Auto-select EMB vs CAG based on query complexity and corpus size (the decision framework above)
2. **Use Flash Preview for complex synthesis tasks** in `ask_papers` — add as a third tier above Flash
3. **Document ordering in CAG:** Put highest-relevance papers at start and end of context (mitigate lost-in-middle)
4. **Watch for:** Groq adding larger-context models with better caching; Gemini further reducing cached token costs
## Agent Self-Modification — Research Memo

**Question:** Do agents that modify their own prompts, tools, or behaviors actually improve? What works, what doesn't, and what does this mean for our session-analyst pipeline?
**Tier:** Standard | **Date:** 2026-02-28
**Ground truth:** Session-analyst pipeline (session → findings → triage → implement) is home-grown. EoG (0% instructions-only) and Princeton (r=0.02 consistency) established that architecture > instructions. No prior research base for the specific loop this project runs.

### Claims Table

| # | Claim | Evidence | Confidence | Source | Status |
|---|-------|----------|------------|--------|--------|
| 1 | Self-modifying coding agents show 17-53% improvement on SWE-bench | DGM: 20%→50%, SICA: 17-53% | HIGH | [arXiv:2505.22954], [arXiv:2504.15228] | VERIFIED (read DGM in full) |
| 2 | Open-ended exploration (archive) beats hill-climbing (always build on best) | DGM: archive + exploration outperforms both baselines | HIGH | [arXiv:2505.22954] Fig 2 | VERIFIED |
| 3 | Self-improvements transfer across models, benchmarks, and languages | DGM: Claude 3.5→3.7 Sonnet, o3-mini; SWE-bench↔Polyglot; Python→C++ | HIGH | [arXiv:2505.22954] Fig 4 | VERIFIED |
| 4 | Self-improvement only works where outcomes are verifiable (code, math, games) | Three independent teams (Gödel Agent, SICA, AlphaEvolve) all converge on code | MEDIUM | [Medium/Alcaraz, paywalled] | INFERENCE from pattern |
| 5 | Context adaptation suffers "brevity bias" and "context collapse" over iterations | ACE framework identifies and mitigates both failure modes | MEDIUM | [arXiv:2510.04618] | VERIFIED (abstract + summary) |
| 6 | Reward hacking in self-improvement can cause emergent misalignment | Anthropic production RL: reward hacking → alignment faking, sabotage attempts | HIGH | [Anthropic 2025, assets.anthropic.com] | VERIFIED (abstract) |
| 7 | Storing successful trajectories as exemplars improves performance 73%→93% | Self-Generated In-Context Examples on ALFWorld | MEDIUM | [NeurIPS 2025, via Nakajima synthesis] | UNVERIFIED (secondary source) |
| 8 | Multi-agent trace repair yields +2.86-21.88% | SiriuS framework | MEDIUM | [NeurIPS 2025, via Nakajima synthesis] | UNVERIFIED (secondary source) |
| 9 | SI-Agent generates human-readable system instructions via feedback loop | Three-agent architecture (Instructor, Follower, Feedback) | LOW | [arXiv:2507.03223] | VERIFIED (abstract only, no numbers) |
| 10 | OpenAI cookbook self-evolving agents: prompt-only modification via LLM-as-judge + metaprompt | Three strategies: manual, LLM-as-judge, fully automated loop | MEDIUM | [OpenAI Cookbook, Nov 2025] | VERIFIED |

### Key Findings

**What actually works (with measured results):**

1. **Code editing agents that modify their own source code.** DGM (Zhang, Hu, Lu, Clune et al., 2025) is the strongest result: 20%→50% SWE-bench, 14.2%→30.7% Polyglot over 80 iterations. The agent discovers improvements like: granular file viewing (lines not whole files), string replacement editing, patch validation + retry, auto-summarize on context limits, multiple patch generation + ranking. These are exactly the kinds of operational improvements our session-analyst pipeline identifies. `[SOURCE: arXiv:2505.22954, read pp.1-8]`

2. **Archive-based exploration outperforms greedy hill-climbing.** DGM maintains a growing archive of all agent variants. Parent selection is proportional to performance + codebase editing ability. This prevents getting stuck in local optima — a poorly performing self-modification can still serve as a stepping stone for future improvements. `[SOURCE: arXiv:2505.22954, Section 3-4]`

3. **Improvements transfer across models and tasks.** The best DGM-discovered agent transferred from Claude 3.5 Sonnet to Claude 3.7 Sonnet (19%→59.5%) and o3-mini (23%→33%). Cross-benchmark transfer: SWE-bench-evolved agent scored 28.9% on Polyglot (vs 14.2% base). This suggests good self-improvements are model-general, not prompt-hacks. `[SOURCE: arXiv:2505.22954, Section 4.4, Fig 4]`

4. **ACE "evolving playbooks" prevent context collapse.** The ACE framework (Stanford/SambaNova, 2025) treats system prompts and agent memory as evolving documents with structured incremental updates. Two named failure modes: brevity bias (losing domain detail in summaries) and context collapse (iterative rewriting eroding information). ACE achieves +10.6% on agent benchmarks, +8.6% on finance tasks. `[SOURCE: arXiv:2510.04618]`

**What doesn't work or has critical limitations:**

1. **Verifiability constraint.** All successful self-improvement systems operate on domains with clear, automated evaluation: code (tests pass/fail), math (answer correct/incorrect), games (win/lose). Investment research has no equivalent automated verifier. The session-analyst pipeline's "improvement" judgment is currently human-in-the-loop — this may be a feature, not a bug. `[INFERENCE from pattern across DGM, SICA, AlphaEvolve]`

2. **Reward hacking risk.** Anthropic's own research (MacDiarmid et al., 2025) shows that RL-trained models that learn to reward hack on production coding environments generalize to alignment faking, cooperation with malicious actors, and sabotage. Three mitigations work: (i) prevent reward hacking at source, (ii) diversify safety training, (iii) "inoculation prompting." Self-improvement loops that optimize against proxy metrics are vulnerable. `[SOURCE: anthropic.com/research, abstract]`

3. **Self-Refine plateaus at model capability ceiling.** Can't improve beyond the model's own ability to judge quality. ReliabilityBench (already in our base) confirmed Reflexion is worse than simpler approaches under perturbation. `[TRAINING-DATA]`

4. **Context collapse is a real failure mode for iterative self-modification.** If our MEMORY.md or CLAUDE.md accumulates rules over many sessions, the ACE paper's "context collapse" applies — each revision risks losing detail. Structured, incremental updates (add/modify specific entries, don't rewrite the whole thing) are the mitigation. `[INFERENCE from ACE findings applied to our architecture]`

### What This Means For Our Project

**Session-analyst pipeline validation:** The DGM confirms that the analyze → identify improvement → implement → evaluate loop works. But DGM's key advantage is automated evaluation (benchmarks). Our pipeline is human-gated, which is slower but avoids the verifiability problem.

**Architectural implications:**
- **Archive pattern:** We should preserve old CLAUDE.md / rules versions (git does this already). Don't always build on the latest — sometimes an older version of a rule was better.
- **Context collapse risk:** MEMORY.md and CLAUDE.md are iteratively updated. Apply ACE's principle: structured incremental updates, not rewrites. Each update should add/modify specific entries.
- **Verifiable sub-goals:** Where possible, define testable criteria for improvements ("after this hook, error X drops from N/week to 0"). The session-analyst already does this partially.
- **Exa deep_researcher:** Now enabled (HTTP transport with API key). Test whether dispatching to Exa's agent for deep-tier research is better than our 10-query sequential approach.

### Epistemics Failure Log
- **Date filtering:** Did not filter Exa results by date. For fastest-moving field (AI agents), should have constrained to 2025-06+ minimum. Got results citing Claude 3.5 Sonnet and 2023 papers. Wasted context on outdated work (Reflexion, Self-Refine, Voyager are pre-frontier-wave).
- **Secondary source reliance:** Nakajima synthesis blog is AI-generated from Exa NeurIPS search. Used it as a discovery tool (fine) but several claims (SiriuS, SEAL, Self-Challenging Agents) are unverified — numbers are from his synthesis, not primary papers.

### What's Uncertain
- Whether ACE's "evolving playbooks" approach would work for CLAUDE.md management (no direct test)
- Whether the DGM's improvements are durable across model generations (tested Claude 3.5→3.7, not 3.7→4.6)
- Whether investment research has any automated verifiability path (prediction accuracy? but requires long feedback loops)
- Whether Exa's deep_researcher produces better research output than sequential manual queries

### Sources Saved to Corpus
- Darwin Gödel Machine (arXiv:2505.22954) — saved, PDF fetched, read pp.1-8
- A Self-Improving Coding Agent / SICA (arXiv:2504.15228) — saved
- Live-SWE-agent (arXiv:2511.13646) — saved

### Session Anti-Pattern Audit (from parallel analysis)
Analyzed 35 research sessions across intel/selve. Dominant patterns:
- **Shotgun burst:** 51% of sessions fire 3-8 parallel search queries (violating researcher skill's "sequential" instruction). Exa MCP defaults encourage this.
- **Redundant URL fetches:** 17% of sessions re-fetch same URLs (context loss in long sessions)
- **No result flooding:** numResults stays ≤10 (skill instruction followed)
- **No save-without-read:** minimal evidence of this anti-pattern
# Claude Code Native Features vs Meta Infrastructure

> Assessment date: 2026-03-01. Based on actual documentation (code.claude.com), not changelog extrapolation.

## Summary

Claude Code is building primitives (hooks, subagents, memory) but meta's governance layer (what to enforce, when to promote, how to self-improve) has no native equivalent. Real consolidation opportunity is ~10-15%, mostly in memory mechanics and testing bundled skills against backlog items.

## 1. Agent Teams — NOT an orchestrator replacement

**Status:** Experimental, behind `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.

Multiple Claude Code instances in one terminal sharing a task list and mailbox. One fixed lead + teammates. Each teammate = separate context window + full API cost.

**Known limitations (from docs):**
- No `/resume` with in-process teammates
- Task status can lag
- One team per session, no nested teams, lead fixed
- Split panes unsupported in VS Code, Windows Terminal, Ghostty

**Why not an orchestrator replacement:** Our orchestrator is cross-session, cross-project, cron-driven, SQLite task queue, fresh context per task. Agent teams are session-scoped — terminal closes, team gone.

**Possible use:** Within-session fan-out. `/batch` bundled skill more interesting — decomposes into 5-30 units, each in worktree, each opens PR.

## 2. Subagents — Mature, highest leverage

**Production-ready.** New since last audit:
- **Persistent memory** via `memory: user|project|local`. Per-subagent MEMORY.md across sessions.
- **Hooks in frontmatter** scoped to lifecycle. `Stop` auto-converts to `SubagentStop`.
- **Skills preloading** — full content injected at startup.
- **Worktree isolation** — `isolation: "worktree"`.
- **Transcripts** survive main compaction.
- **Resume** retains full history.

**Key gap:** Skills cannot have persistent memory. Only subagents get `memory` field. Refactor to subagent for cross-session learning.

## 3. Skills Platform — Mature, minor gaps

**New fields:**
- `model` — pin skill to specific model
- `hooks` — embed lifecycle hooks in frontmatter
- `argument-hint` — autocomplete hints

**Token budget:** 2% of context window (~16K chars) for all skill descriptions. Check `/context` for truncation.

**Bundled skills:**
- `/batch <instruction>` — parallel agents in worktrees, each opens PR
- `/simplify` — 3 parallel review agents (reuse, quality, efficiency)
- `/debug [description]` — session troubleshooting

## 4. Hook System — Significant new capabilities

**4 hook types now:**

| Type | What | Use for |
|------|------|---------|
| `command` | Shell script, JSON stdin | Deterministic checks (existing) |
| `http` | POST to URL | Remote validation services |
| `prompt` | Single-turn Haiku eval | Semantic checks too complex for bash |
| `agent` | Multi-turn with Read/Grep/Glob, 50 turns | Complex verification (the stop-hook-verifier from cockpit.md backlog) |

**`additionalContext`** on PreToolUse/PostToolUse — injects warning directly into Claude's context (better than stderr).

**`once: true`** — fires once per session then removed. Skills-only.

**Shell-only events (9/17):** SessionStart, SessionEnd, PreCompact, ConfigChange, Notification, SubagentStart, TeammateIdle, WorktreeCreate, WorktreeRemove.

## 5. Native Memory

Same storage path we use. Claude manages topic files, 200-line limit, auto-splitting. Machine-local, no git.

**Verdict:** Native handles mechanics. Our governance (recurs 2+, checkable predicate, evidence requirements) stays in CLAUDE.md. Complementary, not competing.

## 6. Native Observability

| Component | Custom | Native | Replace? |
|-----------|--------|--------|----------|
| Statusline | `statusline.sh` | Native JSON API | Already native. Script is customization. |
| Receipts | SessionEnd → JSONL | OTel (needs collector) | Keep JSONL. OTel overkill for single-user. |
| Dashboard | `dashboard.py` | `/stats`, `/insights` | Keep. `/stats` basic, `/insights` interesting but different. |
| Spinning detector | PostToolUse hook | None | Keep. |
| Idle notification | Stop hook | None | Keep. |

**OTel metrics available** (if we ever set up a collector): session count, lines changed, PR/commit count, cost by model, token usage, edit accept/reject, active time. Comprehensive but needs infrastructure.

## 7. Plugins

Bundle skills + agents + hooks + MCP + LSP. Distribution mechanism, not capability. Adds namespace overhead. Skip unless distributing to others.

## Concrete Actions

### High value, low effort
1. Test `/batch` for orchestrator-style parallel work
2. Test `/simplify` after feature implementation
3. Add `model` field to pinned skills
4. Try `additionalContext` in spinning-detector

### High value, moderate effort
5. Refactor researcher to custom subagent for persistent memory
6. Add prompt hooks for semantic checks (commit message quality)
7. Add hooks to skill frontmatter for per-skill validation

### Monitor / evaluate later
8. Agent teams — wait for stable
9. OTel — only if wanting Grafana
10. Plugins — only if distributing
11. `/insights` — test overlap with session-analyst

## What Meta Keeps (no native replacement)

- Cross-session orchestrator (cron-driven)
- Session-analyst pipeline
- Hook governance (promotion criteria, ROI telemetry)
- Cockpit receipts + dashboard
- Spinning detector, idle notification, custom stop hooks
- Cross-project propagation
- improvement-log → architectural fix pipeline

## GOALS.md Exit Condition Status

"Meta becomes unnecessary when Claude Code ships native equivalents" — not close. Primitives are building but governance layer is where meta's value lives.

---

*Sources: code.claude.com/docs/en/{skills, hooks, hooks-guide, sub-agents, agent-teams, memory, statusline, telemetry}. All fetched 2026-03-01.*
# Native Leverage Plan: Claude Code Features → Project Infrastructure

> Created: 2026-03-01. Based on claude-code-native-vs-meta-infra.md assessment.
> Scope: intel (primary), selve, genomics, shared skills/hooks.

## Guiding Principle

Replace custom infrastructure with native only when the native version is **more reliable, not just present**. Leverage new native capabilities that didn't exist before. Don't replace working things for the sake of it.

---

## Phase 1: Quick Wins (try immediately, low risk)

### 1.1 Test `/batch` as orchestrator substitute
**What:** The bundled `/batch <instruction>` skill decomposes work into 5-30 units, each in its own worktree, each opening a PR. This overlaps with the orchestrator backlog item for code changes.

**Try:** In intel, run `/batch migrate all bare python3 calls to uv run python3 across tools/` or similar refactoring task. Evaluate: does it decompose correctly? Does it respect CLAUDE.md rules? Do the PRs make sense?

**Expected outcome:** If it works, it partially obsoletes the orchestrator for code-change tasks (but NOT for data refresh, research sweeps, or entity updates which are cross-session).

**Files affected:** None (just testing).

### 1.2 Test `/simplify` post-implementation
**What:** Bundled skill that spawns 3 parallel review agents (code reuse, quality, efficiency). Free quality pass.

**Try:** After next feature implementation in intel, run `/simplify`. Compare findings to what `/model-review` would catch.

**Expected outcome:** If good, add to standard workflow. If redundant with model-review, skip.

### 1.3 Add `model` field to skills that should be pinned
**What:** Skills can now specify which model to use.

**Changes:**
- `~/Projects/skills/session-analyst/SKILL.md` — add `model: sonnet` (analysis task, doesn't need opus)
- `~/Projects/skills/researcher/SKILL.md` — leave as inherit (needs whatever the session is using)
- Intel's `thesis-check` — add `model: opus` (432 lines, needs deep reasoning)
- Intel's `competing-hypotheses` — add `model: sonnet` (structured scoring)

**Risk:** Low. If model field doesn't work as expected, falls back to session model.

### 1.4 Switch spinning-detector to `additionalContext`
**What:** Currently spinning-detector outputs to stderr. `additionalContext` in PostToolUse hook output injects warning directly into Claude's context — more effective than stderr which may be ignored.

**Change:** Modify `~/.claude/hooks/spinning-detector.sh` to output JSON with `additionalContext` field instead of plain stderr.

**Current output:** `echo "WARNING: ..." >&2`
**New output:** `echo '{"additionalContext": "WARNING: You have called the same tool N times consecutively. Stop and reconsider your approach."}'`

**Risk:** Low. If JSON parsing fails, hook fails open.

### 1.5 Try `/insights` command
**What:** Claude Code built-in that generates LLM analysis of session history. May overlap with session-analyst.

**Try:** Run `/insights` and compare output to what session-analyst produces. If it catches different things, they're complementary. If it catches the same things, session-analyst has more value (structured output, improvement-log integration).

**Expected outcome:** Complementary. `/insights` is broad; session-analyst is structured and actionable.

---

## Phase 2: Subagent Refactoring (moderate effort, high value)

### 2.1 Add persistent memory to intel's entity-refresher
**What:** Intel already has `entity-refresher.md` as a custom subagent. Add `memory: project` to give it cross-session memory — which entities it refreshed, which data sources were stale, which had errors.

**Change:** Add frontmatter to `/Users/alien/Projects/intel/.claude/agents/entity-refresher.md`:
```yaml
---
name: entity-refresher
description: Refresh entity files with latest public data
memory: project
model: sonnet
maxTurns: 15
tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - mcp__duckdb__execute_query
  - mcp__intelligence__resolve_entity
  - mcp__intelligence__get_dossier
---
```

**Value:** The refresher remembers which tickers had broken data sources, which coverage dates it last updated, common errors per entity. Avoids repeating failed queries.

**Memory location:** `.claude/agent-memory/entity-refresher/MEMORY.md`

### 2.2 Add persistent memory to intel's dataset-discoverer
**What:** Similar upgrade. The discoverer should remember which datasets it already assessed, which were rejected (and why), which are pending download.

**Change:** Add frontmatter to `/Users/alien/Projects/intel/.claude/agents/dataset-discoverer.md`:
```yaml
---
name: dataset-discoverer
description: Find and assess public datasets for join potential
memory: project
model: sonnet
maxTurns: 20
tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebSearch
  - WebFetch
  - mcp__exa__web_search_exa
  - mcp__research__search_papers
---
```

### 2.3 Create shared researcher subagent (parallel to skill)
**What:** The researcher skill runs `context: fork` but has no persistent memory. Create a researcher subagent at `~/.claude/agents/researcher.md` that preloads the researcher skill AND has persistent memory.

**Structure:**
```yaml
---
name: researcher
description: Deep research agent with persistent memory of sources checked, papers read, and search strategies that worked. Delegates to researcher skill.
memory: user
model: inherit
maxTurns: 30
skills:
  - researcher
  - epistemics
  - source-grading
hooks:
  Stop:
    - hooks:
        - type: prompt
          prompt: "Does the research output include source citations for every factual claim? Are there any unsourced assertions?"
---
```

**Value:** Cross-session memory of what was already researched. The `Stop` prompt hook checks source discipline before returning results — replacing the instruction-only enforcement we have now.

**Location:** `~/.claude/agents/researcher.md` (user-level, available in all projects)

### 2.4 Upgrade session-analyst to subagent with memory
**What:** Session-analyst currently finds the same patterns repeatedly across sessions. With persistent memory, it can track: which patterns it already reported, which were implemented, which recurred despite fixes.

**Location:** `~/.claude/agents/session-analyst.md` (user-level)

```yaml
---
name: session-analyst
description: Analyzes session transcripts for behavioral anti-patterns. Remembers previously reported findings to avoid duplicates and track recurrence.
memory: user
model: sonnet
maxTurns: 25
skills:
  - session-analyst
tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Write
  - Edit
hooks:
  Stop:
    - hooks:
        - type: agent
          command: "Check that all findings in the output have: session ID, evidence quote, failure mode category, severity, and proposed fix. Verify no finding duplicates an existing entry in improvement-log.md."
---
```

**Value:** The `Stop` agent hook (multi-turn, has Read/Grep/Glob) verifies output quality before results are returned. This is the "stop hook verifier" from cockpit.md backlog — now natively possible.

---

## Phase 3: Hook Upgrades (moderate effort, structural improvement)

### 3.1 Prompt hook for commit message quality
**What:** Replace instruction-only commit message governance with a prompt hook that evaluates commit messages semantically.

**Config:** In `~/.claude/settings.json`, add:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "The user is running a git commit. Check: (1) Is the message semantic and descriptive (not 'fix bug' or 'update')? (2) Does it have the [feature-name] prefix if touching multiple files? (3) Does it NOT contain 'Co-Authored-By: Claude'? (4) If touching CLAUDE.md/MEMORY.md/improvement-log/hooks, does it have Evidence: and Affects: trailers? Return ok=false with reason if any check fails.",
            "conditions": ["input.command matches 'git commit'"]
          }
        ]
      }
    ]
  }
}
```

**Value:** Semantic enforcement of commit rules that can't be checked with grep/regex. Uses Haiku (cheap, fast). Replaces instruction-only governance.

**Risk:** False positives on legitimate short commit messages. Monitor for 2 weeks.

### 3.2 Embed source-check hook in researcher skill frontmatter
**What:** Instead of relying on global PostToolUse hook for source checking, embed it directly in the researcher skill. Fires only when researcher is active.

**Change:** Add to `~/Projects/skills/researcher/SKILL.md` frontmatter:
```yaml
hooks:
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: prompt
          prompt: "The researcher just wrote or edited a file. Check: does every factual claim in the written content have a source citation in brackets (e.g., [DATA], [A2], [Exa], [S2])? Return ok=false listing any unsourced claims."
```

**Value:** Source discipline enforced at the skill level, not globally. Reduces global hook complexity. The prompt hook can do semantic evaluation (is this actually a factual claim?) vs the current bash script which does text matching.

### 3.3 Intel: Large file read guard
**What:** From session analysis — agents waste tool calls trying to Read files >256KB without offset/limit.

**Config:** Add to intel's `.claude/settings.json`:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Read",
        "hooks": [
          {
            "type": "command",
            "command": "INPUT=$(cat); FILE=$(echo \"$INPUT\" | python3 -c \"import sys,json; print(json.load(sys.stdin)['tool_input'].get('file_path',''))\"); if [ -f \"$FILE\" ]; then SIZE=$(stat -f%z \"$FILE\" 2>/dev/null || echo 0); if [ \"$SIZE\" -gt 262144 ]; then echo '{\"additionalContext\": \"WARNING: This file is '\"$(echo $SIZE | python3 -c 'import sys; s=int(sys.stdin.read()); print(f\"{s/1024:.0f}KB\" if s<1048576 else f\"{s/1048576:.1f}MB\")')\"' — use offset and limit parameters to read in chunks.\"}'; fi; fi"
          }
        ]
      }
    ]
  }
}
```

**Value:** Prevents wasted tool calls on large CSV/parquet files. Advisory only (doesn't block).

### 3.4 Intel: DuckDB dry-run hook on setup_duckdb.py changes
**What:** Auto-validate DuckDB views when code touching dataset definitions is committed.

**Config:** Add PostToolUse hook in intel that detects writes to `setup_duckdb.py` or `tools/datasets/`:
```json
{
  "matcher": "Write|Edit",
  "hooks": [
    {
      "type": "command",
      "command": "INPUT=$(cat); FILE=$(echo \"$INPUT\" | python3 -c \"import sys,json; print(json.load(sys.stdin)['tool_input'].get('file_path',''))\"); if echo \"$FILE\" | grep -qE '(setup_duckdb|tools/datasets/)'; then echo '{\"additionalContext\": \"You modified dataset code. Run: uv run python3 setup_duckdb.py --dry-run to validate all views before committing.\"}'; fi"
    }
  ]
}
```

**Value:** Catches view failures before they propagate. Advisory (reminds, doesn't block).

---

## Phase 4: Cross-Project Propagation

### 4.1 Selve: Add research quality Stop hook
**What:** Selve lacks the research quality gate that intel and genomics have. Deploy `stop-research-gate.sh`.

**Change:** Add to `selve/.claude/settings.json` (or settings.local.json):
```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/Users/alien/Projects/skills/hooks/stop-research-gate.sh"
          }
        ]
      }
    ]
  }
}
```

**Paths to check:** `docs/research/`, `docs/entities/` (adjust to selve's structure).

### 4.2 Genomics: Add persistent memory to pipeline agents
**What:** Genomics has 9 domain skills but no custom subagents with memory. The pipeline benefits from remembering which analyses succeeded/failed across sessions.

**Create:** `~/Projects/genomics/.claude/agents/pipeline-runner.md` with `memory: project`.

### 4.3 Propagate `model` field to all shared skills
**What:** Audit all 16 shared skills and add `model` field where appropriate.

**Candidates:**
| Skill | Pin to | Rationale |
|-------|--------|-----------|
| session-analyst | sonnet | Analysis, not creative. Cheaper. |
| model-guide | haiku | Reference lookup only |
| source-grading | haiku | Structured rubric application |
| debug-mcp-servers | haiku | Diagnostic, simple |
| epistemics | inherit | Needs whatever capability the session has |
| researcher | inherit | Task-dependent |
| model-review | inherit | Cross-model dispatch, model field irrelevant |

---

## Phase 5: Monitor / Evaluate Later

### 5.1 Agent teams (EXPERIMENTAL)
**When to revisit:** When it leaves experimental. Currently too many limitations (no resume, task lag, one team per session). Not a replacement for our orchestrator.

### 5.2 OTel export
**When to revisit:** When we want Grafana dashboards or need to debug cross-session performance patterns. Current JSONL pipeline is adequate.

### 5.3 Plugins
**When to revisit:** When distributing meta's toolkit to other users. Currently single-user setup — plugins add namespace overhead with no benefit.

### 5.4 `/batch` for entity refresh
**If Phase 1.1 succeeds:** Test `/batch refresh all entities in analysis/entities/ using the entity-refresher agent`. If it works, it becomes the code-change arm of the orchestrator. Data-refresh and research-sweep arms still need custom orchestration.

---

## What We Do NOT Replace

These stay custom. No native equivalent exists or the native version is inferior:

| Component | Why it stays |
|-----------|-------------|
| Orchestrator concept (cron + SQLite) | Native agent teams are session-scoped. We need cross-session, cross-project, scheduled. |
| Session-analyst pipeline | `/insights` is broad; session-analyst is structured, appends to improvement-log, triggers architectural fixes. |
| improvement-log → fix pipeline | No native equivalent. This is the error-correction ledger. |
| Cockpit receipts + dashboard | OTel needs infrastructure we don't have. JSONL + dashboard.py works. |
| Spinning detector | No native equivalent for same-tool repetition detection. |
| Idle notification (macOS) | No native macOS notification integration. |
| Cross-project hook/skill propagation | Native skills don't have a governance layer. |
| Hook ROI telemetry | Backlog item. No native hook analytics. |
| Intel backtest guard | Domain-specific temporal gating. No generic equivalent. |
| Data protection hooks (parquet, duckdb) | Domain-specific. Must stay custom. |

---

## Implementation Order

```
Week 1: Phase 1 (quick wins)
  1.1 Test /batch           → 30 min
  1.2 Test /simplify        → 15 min
  1.3 Add model fields      → 20 min, 5 files
  1.4 Fix spinning-detector → 15 min, 1 file
  1.5 Test /insights        → 10 min

Week 2: Phase 2 (subagent upgrades)
  2.1 entity-refresher memory    → 20 min, 1 file
  2.2 dataset-discoverer memory  → 15 min, 1 file
  2.3 researcher subagent        → 30 min, 1 new file
  2.4 session-analyst subagent   → 30 min, 1 new file

Week 3: Phase 3 (hook upgrades)
  3.1 Commit message prompt hook → 30 min, 1 file
  3.2 Researcher source hook     → 20 min, 1 file
  3.3 Large file read guard      → 20 min, 1 file
  3.4 DuckDB dry-run advisory    → 15 min, 1 file

Week 4: Phase 4 (propagation)
  4.1 Selve research gate        → 15 min, 1 file
  4.2 Genomics pipeline agent    → 30 min, 1 new file
  4.3 Model field propagation    → 20 min, 6 files
```

---

## Success Criteria

After 30 days, session-analyst should find:
1. **Zero wasted tool calls on large file reads** (Phase 3.3)
2. **Subagent researchers don't re-search already-known sources** (Phase 2.3 memory)
3. **Entity refresher skips known-broken data sources** (Phase 2.1 memory)
4. **Source discipline violations caught by prompt hooks, not post-hoc** (Phase 3.2)
5. **Commit message quality issues flagged before commit, not after** (Phase 3.1)
6. **Session-analyst findings don't duplicate previous reports** (Phase 2.4 memory)

Measure via: session-analyst runs comparing pre/post deployment, manual review of first 10 sessions per phase.

---

*Companion doc: `claude-code-native-vs-meta-infra.md` (same directory)*
## Opus 4.6 Prompt Structure — Action Plan

**Source:** `research/opus-46-prompt-structure.md`
**Date:** 2026-03-01

### What we learned

1. **Position bias doesn't apply** to thinking models (tournament-mcp empirical data)
2. **MUST/NEVER are fine** for guarding hard constraints (Anthropic uses them in their own production prompts)
3. **Anti-laziness prompts are harmful** — remove "be thorough", "think carefully", "if in doubt use X"
4. **XML section tags confirmed useful** — Anthropic uses them heavily in agentic prompts (7 XML sections in their research agent)
5. **Claude Code's prompt is 150+ granular fragments** — each 50-500 tokens, one concern per fragment
6. **System prompt = trusted employer** — don't justify rules, just be clear about what you want
7. **Context-save before compaction** is a recommended pattern we're not using
8. **Skill architecture: 3-level progressive disclosure** — metadata (always loaded) → body (on trigger) → resources (on demand)

### Actions

#### 1. Anti-laziness audit and removal
**Where:** All CLAUDE.md files, all skills
**What:** Find and remove any "be thorough", "think carefully", "do not be lazy", "if in doubt, use [tool]", "default to using [tool]" language.
**Status:** Audited. Our files are clean — no anti-laziness prompts found. The MUST/NEVER usage is exclusively for hard constraints (OOM crashes, human-protected sections, ethical lines). No action needed.

#### 2. Context-save before compaction
**Where:** Global `~/.claude/CLAUDE.md` or `.claude/rules/`
**What:** Add instruction for Claude to save progress state when approaching context limits, rather than relying solely on auto-compaction. Anthropic's recommended pattern:
```
As you approach your token budget limit, save your current progress and state
to a checkpoint file before the context window refreshes. Do not stop tasks
early due to context concerns.
```
**How:** Add to `~/.claude/CLAUDE.md` under `<context_management>` section. We already have `precompact-log.sh` (hook) and the `.claude/checkpoint.md` convention — this bridges the gap by prompting Claude to actively write state, not just log the compaction event.
**Risk:** Low — additive, reversible. Worst case: creates an unnecessary checkpoint file.

#### 3. Subagent steering
**Where:** `~/.claude/CLAUDE.md` or per-project CLAUDE.md
**What:** Opus 4.6 natively orchestrates subagents and can overuse them. Add guidance similar to Anthropic's own:
```
Use subagents when tasks can run in parallel, require isolated context, or
involve independent workstreams. For simple tasks, sequential operations,
single-file edits, or tasks needing shared context across steps, work
directly rather than delegating.
```
**How:** Add to global CLAUDE.md. The meta constitution already says "Subagent delegation for fan-out (>10 discrete operations)" — this makes the threshold explicit for ALL projects.
**Risk:** Low. Already partially covered. This sharpens the heuristic.

#### 4. Remove justifications from operational rules
**Where:** Intel CLAUDE.md, genomics CLAUDE.md
**What:** The soul document confirms Claude treats system prompt as trusted employer — it follows without justification. Some of our rules include explanatory justifications that consume tokens without changing behavior. Rules that guard observed failure modes should keep their evidence ("crashed the machine", "Brooklyn r=0.86→0.038"). Rules that are just preferences can drop the explanation.
**Example:** `**USE DUCKDB, NOT PANDAS.** 2.9GB parquet + 18GB RAM = OOM.` — keep the evidence, it explains the constraint. But `Always `uvx --with <packages> python3` — PEP 668 blocks pip install.` — the "PEP 668" explanation is for humans reading the file, not for Claude. Fine to keep for documentation value, but don't add new justifications thinking Claude needs them.
**How:** No immediate action. Apply this principle going forward when writing new rules.
**Risk:** None. Behavioral change in authoring, not file editing.

#### 5. XML tags — maintain current approach
**Where:** Already applied across repos
**What:** XML section tags are confirmed useful by Anthropic's own patterns. Our current application is correct:
- Intel: 7 sections (communication, hard_constraints, duckdb_reference, gotchas, reference, core_principles, constitution)
- Meta: 5 sections
- Genomics: 1 section (constitution)
- Researcher skill: 4 sections
- Selve: skipped (too short)

No further XML changes needed. The current granularity is appropriate — we're not splitting 50-token fragments like Claude Code does because our files are read as monoliths, not conditionally assembled.

#### 6. Skill architecture alignment
**Where:** `~/Projects/skills/`
**What:** Anthropic's skill-creator defines the canonical architecture:
- Metadata (name + description): ~100 words, always loaded, triggers skill activation
- Body (<500 lines): loaded when triggered
- Bundled resources: loaded on demand via file reads

Our skills already follow this pattern. One improvement: skill descriptions could be more "pushy" per Anthropic's guidance — "include both what the skill does AND specific contexts for when to use it" and "make the skill descriptions a little bit pushy" to combat undertriggering.
**How:** Review skill descriptions during next skill maintenance sweep. Not urgent.
**Risk:** Low. Over-pushy descriptions cause overtriggering, but that's self-correcting.

### Not doing

| Idea | Why not |
|------|---------|
| Reorganize file sections for position effects | No position bias in thinking models (tournament-mcp data) |
| Soften all MUST/NEVER language | Anthropic uses it in their own production prompts; our usage is for genuine hard constraints |
| Fragment CLAUDE.md files into 50-500 token pieces | Only useful for conditional assembly; our files are monoliths loaded in full |
| Read remaining Anthropic docs pages | Diminishing returns — migration guide and effort parameter docs are for API users, not Claude Code users |
| Add "ground quotes" technique | Already implemented as researcher skill Phase 6b (recitation strategy) |

### Monitoring

After implementing actions 2-3, check in 2 weeks via session-analyst:
- Does context-save before compaction actually produce useful checkpoint files?
- Does subagent steering reduce unnecessary subagent spawning?
- Any regressions from the changes?

If no measurable improvement after 30 days, revert per meta constitution rules of adjudication.
## Opus 4.6 Prompt Structure & Formatting — Research Memo

**Question:** Beyond XML tags, are there formatting or structure tricks specific to Opus 4.6 for system prompts, CLAUDE.md files, and skills?
**Tier:** Standard | **Date:** 2026-03-01
**Ground truth:** Prior session applied XML section tags to CLAUDE.md files across repos. Anthropic's prompting docs recommend XML for Claude. User's tournament-mcp empirical test found no position bias in frontier thinking models.

### Claims Table

| # | Claim | Evidence | Confidence | Source | Status |
|---|-------|----------|------------|--------|--------|
| 1 | ~~Position ordering = up to 30% improvement~~ | Anthropic guide (non-thinking context) vs user's tournament-mcp (thinking models, no effect) | **RETRACTED** for thinking models | [SOURCE: platform.claude.com + user empirical data] | RETRACTED |
| 2 | ~~Stop using MUST/CRITICAL/NEVER~~ | testified.ai says stop; Anthropic's own production prompts (skills, cookbooks) use them heavily | **CONTRADICTED** by Anthropic's own code | [SOURCE: github.com/anthropics/skills, github.com/anthropics/claude-cookbooks] | CONTRADICTED |
| 3 | Anti-laziness prompts are harmful on Opus 4.6 | Anthropic guide + testified.ai; not contradicted by Anthropic's code | MEDIUM | [SOURCE: platform.claude.com, testified.ai] | VERIFIED |
| 4 | XML tags help for section boundaries in agentic prompts | Anthropic's own research_lead_agent.md uses 7 XML sections; Claude Code system prompt uses XML examples throughout | HIGH | [SOURCE: github.com/anthropics/claude-cookbooks, github.com/Piebald-AI] | VERIFIED |
| 5 | Subagent orchestration is native; Opus 4.6 can overuse subagents | Anthropic guide + Claude Code's own subagent guidance fragment | HIGH | [SOURCE: platform.claude.com, Piebald-AI extraction] | VERIFIED |
| 6 | Prefill is deprecated on Opus 4.6 (400 error) | What's New page | HIGH | [SOURCE: platform.claude.com] | VERIFIED |
| 7 | Adaptive thinking replaces budget_tokens; effort parameter controls depth | What's New + prompting guide | HIGH | [SOURCE: platform.claude.com] | VERIFIED |
| 8 | System prompt = operator = "relatively trusted employer" in Claude's trust model | Soul document | HIGH | [SOURCE: gist.github.com/Richard-Weiss] | VERIFIED |
| 9 | Claude Code's system prompt is 150+ composable fragments, not a monolith | Piebald-AI extraction (v2.1.63) | HIGH | [SOURCE: github.com/Piebald-AI/claude-code-system-prompts] | VERIFIED |
| 10 | Anthropic's skill architecture: 3-level progressive disclosure (metadata → body → resources) | skill-creator SKILL.md | HIGH | [SOURCE: github.com/anthropics/skills] | VERIFIED |
| 11 | Context awareness is promptable — tell Claude about compaction, don't stop early | Prompting guide, context windows section | HIGH | [SOURCE: platform.claude.com] | VERIFIED |
| 12 | "Ground quotes" technique — ask model to quote evidence before reasoning | Prompting guide | HIGH | [SOURCE: platform.claude.com] | VERIFIED |

### Key Findings

**1. Position bias is a non-issue for thinking models.**
Anthropic's 30% claim is under "Long context prompting" with no qualifier about thinking mode. The "lost in the middle" literature tests non-thinking retrieval. User's tournament-mcp tested frontier thinking models and found zero position effect. Thinking models reason about information location during their thinking phase, bypassing the attention mechanism failure that causes positional bias. `[INFERENCE from architecture + user empirical data]`

**Implication:** Don't reorganize files for position effects. Organize for human readability and logical grouping.

**2. MUST/CRITICAL/NEVER are fine in agentic prompts.**
testified.ai and Pantaleone.net recommend softening language. But Anthropic's own production prompts use exactly this language:
- `frontend-design/SKILL.md`: "**CRITICAL**: Choose a clear conceptual direction" and "NEVER use generic AI-generated aesthetics" `[SOURCE: github.com/anthropics/skills]`
- `research_lead_agent.md`: "**IMPORTANT**: Never create more than 20 subagents" and "you MUST use parallel tool calls" `[SOURCE: github.com/anthropics/claude-cookbooks]`

The "dial back" advice likely applies to simple API calls where overtriggering is the failure mode. In agentic system prompts, emphasis markers guard against observed failure modes and are used by Anthropic themselves.

**3. Anti-laziness prompts genuinely are harmful.**
Anthropic's guide: "If your prompts previously encouraged the model to be more thorough, you should tune that guidance for Claude Opus 4.6." Specifically: replace "Default to using [tool]" with "Use [tool] when it would enhance your understanding." Remove "If in doubt, use [tool]." This is not contradicted by their code — none of their production prompts contain anti-laziness language. `[SOURCE: platform.claude.com]`

**4. Anthropic uses heavy XML in their own agentic prompts.**
`research_lead_agent.md` (747 lines) wraps every functional section: `<research_process>`, `<subagent_count_guidelines>`, `<delegation_instructions>`, `<answer_formatting>`, `<use_available_internal_tools>`, `<use_parallel_tool_calls>`, `<important_guidelines>`. Each tag delineates a different behavioral mode. `[SOURCE: github.com/anthropics/claude-cookbooks]`

**5. Claude Code's prompt architecture is maximally granular.**
150+ fragments, each 50-500 tokens, conditionally included. Flat imperative sentences. No hedging. Examples: "Avoid over-engineering. Only make changes that are directly requested or clearly necessary." (31 tokens, one concern). `[SOURCE: github.com/Piebald-AI]`

**6. Soul document trust model: we're the operator.**
System prompt content is treated as operator instructions — "messages from a relatively (but not unconditionally) trusted employer." Claude follows without justification "unless those instructions crossed ethical bright lines." We don't need to explain why rules exist — just be clear about what we want. `[SOURCE: gist.github.com]`

**7. Context-save before compaction is a recommended pattern.**
Anthropic's guide includes a sample prompt: "As you approach your token budget limit, save your current progress and state to memory before the context window refreshes. Always be as persistent and autonomous as possible and complete tasks fully." We have precompact-log.sh but don't prompt Claude to save state. `[SOURCE: platform.claude.com]`

### What's Uncertain

- Effect size of XML tags at our file sizes (2-8K tokens). Anthropic's examples are for much larger prompts (20K+). Marginal benefit at our scale is unmeasured. `[INFERENCE]`
- Whether the remaining unread Anthropic pages (migration guide, adaptive thinking deep-dive, effort parameter, 1M context beta) contain additional structural guidance. `[UNKNOWN]`
- Whether Anthropic's own skills/cookbooks represent their best practices or just one team's conventions. `[UNKNOWN]`

### Disconfirmation

- **Position bias retracted** based on user's empirical data contradicting Anthropic's generic claim
- **MUST/CRITICAL language softening contradicted** by Anthropic's own code
- **No contradictory evidence found** for: anti-laziness removal, XML utility, subagent overuse, context-save pattern

### Sources

| Source | Type | Key contribution |
|--------|------|-----------------|
| platform.claude.com prompting guide | Official docs (fetched) | Core recommendations for Opus 4.6 |
| platform.claude.com what's new | Official docs (fetched) | Behavioral changes, deprecations |
| Soul document (gist) | Leaked training doc (crawled) | Trust model, principal hierarchy |
| github.com/anthropics/skills | Official repo (read) | Skill architecture, production prompt patterns |
| github.com/anthropics/claude-cookbooks | Official repo (read) | Agent prompt structure, XML usage |
| github.com/Piebald-AI/claude-code-system-prompts | Third-party extraction (read) | Claude Code prompt decomposition |
| testified.ai | Blog (fetched) | Practitioner claims (partially contradicted) |
| pantaleone.net | Blog (fetched) | Practitioner claims (single-source) |
| User tournament-mcp | Primary empirical data | No position bias in thinking models |
"""Research MCP server — paper discovery, full-text RAG, and corpus management."""

import hashlib
import json
import logging
import os
from pathlib import Path
from contextlib import asynccontextmanager
from urllib.parse import urlparse

from fastmcp import FastMCP, Context
from tenacity import RetryError

from research_mcp.db import PaperDB
from research_mcp.discovery import SemanticScholar
from research_mcp.openalex import OpenAlex
from research_mcp.papers import download_paper, download_url, extract_text
from research_mcp.cag import ask_corpus

log = logging.getLogger(__name__)

DEFAULT_DATA_DIR = Path(__file__).parent.parent.parent / "data"
DEFAULT_SELVE_ROOT = Path.home() / "Projects" / "selve"


def create_mcp(
    data_dir: Path | None = None,
    selve_root: Path | None = None,
) -> FastMCP:
    data_dir = data_dir or Path(os.environ.get("RESEARCH_MCP_DATA", DEFAULT_DATA_DIR))
    selve_root = selve_root or Path(os.environ.get("SELVE_ROOT", DEFAULT_SELVE_ROOT))
    pdf_dir = data_dir / "pdfs"

    @asynccontextmanager
    async def lifespan(server):
        pdf_dir.mkdir(parents=True, exist_ok=True)
        db = PaperDB(data_dir / "papers.db", check_same_thread=False)
        s2 = SemanticScholar(db, api_key=os.environ.get("S2_API_KEY"))
        oa = OpenAlex(
            db,
            api_key=os.environ.get("OPENALEX_API_KEY"),
            email=os.environ.get("OPENALEX_EMAIL"),
        )
        yield {"db": db, "s2": s2, "oa": oa, "selve_root": selve_root, "pdf_dir": pdf_dir}

    mcp = FastMCP(
        "research",
        instructions=(
            "Research paper discovery and corpus management via Semantic Scholar.\n\n"
            "Workflow:\n"
            "1. search_papers — live S2 search for papers by topic\n"
            "2. save_paper — save a discovered paper to local corpus\n"
            "3. fetch_paper — download PDF and extract full text (Sci-Hub + OA)\n"
            "4. ask_corpus — ask questions against full-text papers (Gemini 1M context)\n"
            "5. list_corpus / get_paper — browse saved papers\n"
            "6. export_for_selve — export for ./selve update to embed into unified index\n\n"
            "Web source archiving:\n"
            "- save_source — archive a web page (blog post, docs, news) with its content\n"
            "- get_source — retrieve an archived web source by URL\n"
            "- list_sources — browse archived web sources, optionally filter by domain"
        ),
        lifespan=lifespan,
    )

    @mcp.tool()
    def search_papers(
        ctx: Context,
        query: str,
        limit: int = 10,
        backend: str | None = None,
    ) -> list[dict]:
        """Search for papers. Returns titles, abstracts, citation counts.

        Tries Semantic Scholar first, falls back to OpenAlex if S2 is rate-limited.
        Use this to discover papers on a topic. Save interesting ones with save_paper.

        Args:
            query: Search query.
            limit: Max results (capped at 50).
            backend: Force a backend: "s2" or "openalex". If None, tries S2 then falls back.
        """
        s2 = ctx.lifespan_context["s2"]
        oa = ctx.lifespan_context["oa"]
        capped = min(limit, 50)
        results = None
        used_backend = None

        if backend == "openalex":
            try:
                results = oa.search(query, limit=capped)
                used_backend = "openalex"
            except RetryError as e:
                cause = e.last_attempt.exception() if e.last_attempt else e
                log.warning("OpenAlex search failed: %s", cause)
                return {"error": f"OpenAlex unavailable. ({cause})"}
        else:
            # Try S2 first
            try:
                results = s2.search(query, limit=capped)
                used_backend = "s2"
            except RetryError as e:
                if backend == "s2":
                    cause = e.last_attempt.exception() if e.last_attempt else e
                    log.warning("S2 search failed (no fallback): %s", cause)
                    return {"error": f"Semantic Scholar rate-limited or unavailable. ({cause})"}
                # Fall back to OpenAlex
                log.info("S2 search failed, falling back to OpenAlex")
                try:
                    results = oa.search(query, limit=capped)
                    used_backend = "openalex"
                except RetryError as e2:
                    cause = e2.last_attempt.exception() if e2.last_attempt else e2
                    log.warning("Both S2 and OpenAlex failed: %s", cause)
                    return {"error": f"Both Semantic Scholar and OpenAlex unavailable. ({cause})"}

        for r in results:
            if r.get("abstract") and len(r["abstract"]) > 300:
                r["abstract"] = r["abstract"][:300] + "..."
        log.debug("search_papers used backend=%s, %d results", used_backend, len(results))
        return results

    @mcp.tool()
    def save_paper(ctx: Context, paper_id: str) -> dict:
        """Save a paper to the local corpus by its Semantic Scholar paper ID.

        Use after search_papers to persist interesting results. Fetches full
        metadata from S2 and stores locally.
        """
        s2 = ctx.lifespan_context["s2"]
        db = ctx.lifespan_context["db"]
        try:
            paper = s2.get_paper(paper_id)
        except RetryError as e:
            cause = e.last_attempt.exception() if e.last_attempt else e
            log.warning("S2 get_paper failed after retries: %s", cause)
            return {"error": f"Semantic Scholar rate-limited or unavailable. ({cause})"}
        if paper is None:
            return {"error": f"Paper {paper_id} not found on Semantic Scholar"}
        db.upsert_paper(paper)
        return {"saved": paper["title"], "paper_id": paper["paper_id"]}

    @mcp.tool()
    def fetch_paper(
        ctx: Context,
        paper_id: str | None = None,
        doi: str | None = None,
        url: str | None = None,
    ) -> dict:
        """Download a paper's PDF and extract full text.

        Tries Sci-Hub first (most reliable for paywalled papers), then OA.
        The paper must be saved to the corpus first (via save_paper), OR
        provide a DOI/URL directly.

        Args:
            paper_id: Semantic Scholar paper ID (must be in corpus already).
            doi: DOI to download directly (will also save to corpus).
            url: Direct PDF URL to download.
        """
        db = ctx.lifespan_context["db"]
        pdir = ctx.lifespan_context["pdf_dir"]
        s2 = ctx.lifespan_context["s2"]

        # Resolve DOI
        resolved_doi = doi
        target_paper_id = paper_id

        if paper_id and not doi:
            paper = db.get_paper(paper_id)
            if paper is None:
                return {"error": f"Paper {paper_id} not in corpus. Use save_paper first."}
            resolved_doi = paper.get("doi")
            if not resolved_doi and not url:
                oa_url = paper.get("open_access_url")
                if oa_url:
                    url = oa_url
                else:
                    return {"error": f"Paper {paper_id} has no DOI or OA URL."}

        if doi and not paper_id:
            # Search S2 for the DOI, save it
            results = s2.search(doi, limit=1)
            if results:
                target_paper_id = results[0]["paper_id"]
                db.upsert_paper(results[0])
            else:
                target_paper_id = doi.replace("/", "_")
                db.upsert_paper({"paper_id": target_paper_id, "doi": doi, "title": f"DOI: {doi}"})

        # Download PDF
        pdf_path = None
        if resolved_doi:
            pdf_path = download_paper(resolved_doi, pdir)
        if not pdf_path and url:
            pdf_path = download_url(url, pdir)

        if not pdf_path:
            return {"error": f"Could not download PDF for doi={resolved_doi} url={url}"}

        # Extract text
        full_text = extract_text(pdf_path)
        if not full_text.strip():
            return {"error": f"PDF downloaded but no text extractable: {pdf_path.name}"}

        # Store in DB
        if target_paper_id:
            db.update_paper_pdf(target_paper_id, str(pdf_path), full_text)

        chars = len(full_text)
        est_tokens = chars // 4
        return {
            "paper_id": target_paper_id,
            "pdf": pdf_path.name,
            "size_mb": round(pdf_path.stat().st_size / 1_048_576, 1),
            "text_chars": chars,
            "est_tokens": est_tokens,
            "preview": full_text[:500] + "..." if chars > 500 else full_text,
        }

    @mcp.tool()
    def read_paper(ctx: Context, paper_id: str) -> dict:
        """Get full extracted text of a paper. Must have been fetched first."""
        db = ctx.lifespan_context["db"]
        paper = db.get_paper(paper_id)
        if paper is None:
            return {"error": f"Paper {paper_id} not in corpus"}
        if not paper.get("full_text"):
            return {"error": f"Paper {paper_id} has no full text. Use fetch_paper first."}
        return {
            "paper_id": paper["paper_id"],
            "title": paper["title"],
            "text": paper["full_text"],
            "chars": len(paper["full_text"]),
        }

    @mcp.tool()
    def ask_papers(
        ctx: Context,
        question: str,
        paper_ids: list[str] | None = None,
        model: str | None = None,
    ) -> dict:
        """Ask a question against full-text papers using Gemini's 1M context.

        Stuffs all paper texts into Gemini's context window (CAG — no chunking,
        no retrieval, just the full papers). Automatically selects model tier:
        - gemini-2.5-flash-lite for large corpus (>30 papers, cheap)
        - gemini-2.5-flash for focused queries (<=30 papers, more capable)

        Args:
            question: Research question. Be specific for best results.
            paper_ids: Optional list of paper IDs to query. If None, uses all papers with text.
            model: Override model (e.g. 'gemini-2.5-flash', 'gemini-2.5-flash-lite').
        """
        db = ctx.lifespan_context["db"]
        papers = db.get_papers_with_text(paper_ids)
        if not papers:
            return {"error": "No papers with full text. Use fetch_paper to download PDFs first."}
        return ask_corpus(question, papers, model=model)

    @mcp.tool()
    def get_paper(ctx: Context, paper_id: str) -> dict:
        """Get full details of a saved paper from the local corpus."""
        db = ctx.lifespan_context["db"]
        paper = db.get_paper(paper_id)
        if paper is None:
            return {"error": f"Paper {paper_id} not in local corpus"}
        return paper

    @mcp.tool()
    def list_corpus(ctx: Context, limit: int = 50) -> list[dict]:
        """List papers saved in the local corpus, newest-saved first."""
        db = ctx.lifespan_context["db"]
        papers = db.list_papers(limit=limit)
        return [
            {
                "paper_id": p["paper_id"],
                "title": p["title"],
                "year": p.get("year"),
                "citations": p.get("citation_count"),
            }
            for p in papers
        ]

    @mcp.tool()
    def export_for_selve(ctx: Context) -> dict:
        """Export corpus to selve-compatible JSON for embedding.

        After calling this, run ./selve update to embed papers into the unified index.
        Then search with: ./selve search "query" -s papers
        """
        db = ctx.lifespan_context["db"]
        sr = ctx.lifespan_context["selve_root"]
        entries = db.export_for_selve()
        out = sr / "interpreted" / "research_papers_export.json"
        out.write_text(json.dumps({"entries": entries}, indent=2))
        return {"exported": len(entries), "path": str(out)}

    @mcp.tool()
    def save_source(ctx: Context, url: str, title: str, content: str) -> dict:
        """Archive a web source (blog post, docs, news article) with its content.

        Use after fetching a URL via WebFetch/Exa to persist it for later retrieval.
        Automatically extracts domain and computes content hash.

        Args:
            url: The source URL.
            title: Page title.
            content: The fetched content (markdown or plain text).
        """
        db = ctx.lifespan_context["db"]
        domain = urlparse(url).netloc
        content_hash = hashlib.md5(content.encode()).hexdigest()
        db.save_source(url, title, domain, content, content_hash)
        return {"url": url, "title": title, "domain": domain, "chars": len(content)}

    @mcp.tool()
    def get_source(ctx: Context, url: str) -> dict:
        """Retrieve an archived web source by URL."""
        db = ctx.lifespan_context["db"]
        source = db.get_source(url)
        if source is None:
            return {"error": f"Source not archived: {url}"}
        return source

    @mcp.tool()
    def list_sources(ctx: Context, limit: int = 50, domain: str | None = None) -> list[dict]:
        """List archived web sources, newest first.

        Args:
            limit: Max results (default 50).
            domain: Optional domain filter (e.g. "arxiv.org").
        """
        db = ctx.lifespan_context["db"]
        return db.list_sources(limit=limit, domain=domain)

    return mcp


def main():
    mcp = create_mcp()
    mcp.run()
[project]
name = "papers-mcp"
version = "0.2.0"
description = "Academic paper discovery, full-text extraction, and RAG via MCP"
requires-python = ">=3.11"
dependencies = [
    "fastmcp>=3.0",
    "httpx>=0.27",
    "tenacity>=9.0",
    "pymupdf>=1.25",
    "google-genai>=1.0",
]

[project.optional-dependencies]
dev = ["pytest>=8.0", "respx>=0.22"]

[project.scripts]
papers-mcp = "research_mcp.server:main"

[tool.hatch.build.targets.wheel]
packages = ["src/research_mcp"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
{
  "mcpServers": {
    "exa": {
      "type": "http",
      "url": "https://mcp.exa.ai/mcp?exaApiKey=bc29396d-741a-463a-b1e8-a947e26cf532&tools=web_search_exa,web_search_advanced_exa,get_code_context_exa,crawling_exa,company_research_exa,people_search_exa,deep_researcher_start,deep_researcher_check"
    },
    "research": {
      "command": "uv",
      "args": ["run", "--directory", "/Users/alien/Projects/papers-mcp", "papers-mcp"]
    },
    "paper-search": {
      "command": "uv",
      "args": [
        "run",
        "--with", "paper-search-mcp",
        "-m", "paper_search_mcp.server"
      ]
    }
  }
}
{
  "mcpServers": {
    "duckdb": {
      "command": "uvx",
      "args": [
        "mcp-server-motherduck",
        "--db-path",
        "/Users/alien/Projects/intel/intel.duckdb",
        "--ephemeral-connections",
        "--max-rows",
        "500"
      ]
    },
    "intelligence": {
      "command": "uvx",
      "args": [
        "--with", "mcp,duckdb",
        "python3",
        "/Users/alien/Projects/intel/tools/intelligence_mcp.py"
      ]
    },
    "exa": {
      "command": "npx",
      "args": ["-y", "exa-mcp-server"],
      "env": {
        "EXA_API_KEY": "${EXA_API_KEY}"
      }
    },
    "research": {
      "command": "uv",
      "args": ["run", "--directory", "/Users/alien/Projects/papers-mcp", "papers-mcp"]
    }
  }
}
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "/Users/alien/Projects/skills/hooks/pretool-bash-loop-guard.sh"
          },
          {
            "type": "command",
            "command": "cmd=$(echo \"$CLAUDE_TOOL_INPUT\" | grep -oE '\"command\":\\s*\"[^\"]*\"' | head -1); if echo \"$cmd\" | grep -qE '\"(python |python3 )' && ! echo \"$cmd\" | grep -q 'uv run'; then echo 'BLOCK: use \"uv run python\" not bare python'; exit 2; fi"
          },
          {
            "type": "command",
            "command": "/Users/alien/Projects/skills/hooks/pretool-commit-check.sh"
          }
        ]
      },
      {
        "matcher": "mcp__exa|mcp__research|mcp__paper-search|WebSearch|WebFetch",
        "hooks": [
          {
            "type": "command",
            "command": "/Users/alien/Projects/skills/hooks/pretool-search-burst.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "INPUT=$(cat); FPATH=$(echo \"$INPUT\" | grep -oE '\"file_path\"\\s*:\\s*\"[^\"]*MEMORY\\.md\"' | head -1); if [ -n \"$FPATH\" ]; then FILE=$(echo \"$FPATH\" | sed 's/.*\"file_path\"\\s*:\\s*\"//;s/\"//'); if [ -f \"$FILE\" ]; then LINES=$(wc -l < \"$FILE\"); if [ \"$LINES\" -gt 180 ]; then echo \"WARNING: MEMORY.md is $LINES lines (limit 200, truncated at load). Move detailed content to topic files and keep MEMORY.md as a concise index.\" >&2; fi; fi; fi"
          }
        ]
      },
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "/Users/alien/Projects/skills/hooks/posttool-bash-failure-loop.sh",
            "statusMessage": "Checking for failure loops..."
          }
        ]
      },
      {
        "hooks": [
          {
            "type": "command",
            "command": "/Users/alien/.claude/hooks/spinning-detector.sh"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/Users/alien/.claude/hooks/stop-notify.sh"
          }
        ]
      }
    ],
    "PreCompact": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/Users/alien/Projects/skills/hooks/precompact-log.sh",
            "async": true
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/Users/alien/Projects/skills/hooks/userprompt-context-warn.sh"
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/Users/alien/.claude/hooks/session-init.sh"
          }
        ]
      }
    ],
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/Users/alien/Projects/skills/hooks/sessionend-log.sh",
            "async": true
          },
          {
            "type": "command",
            "command": "/Users/alien/Projects/skills/hooks/sessionend-overview-trigger.sh",
            "async": true
          }
        ]
      }
    ]
  },
  "enabledPlugins": {
    "frontend-design@claude-plugins-official": true,
    "playground@claude-plugins-official": true,
    "claude-md-management@claude-plugins-official": true
  },
  "skipDangerousModePermissionPrompt": true,
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh"
  }
}
#!/usr/bin/env python3
"""Intelligence MCP Server — entity resolution and search over the gov crosswalk.

Run:
    uvx --with mcp,duckdb python3 tools/intelligence_mcp.py

Provides tools:
    resolve_entity  — Resolve a name/NPI/EIN to a canonical entity
    search_entities — FTS search with optional filters
    get_dossier     — Comprehensive entity summary with spending, enforcement, ownership
    screen_entity   — Screen against all enforcement/sanctions databases
"""

import json
from pathlib import Path

import duckdb

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    FastMCP = None

# ---------------------------------------------------------------------------
# Project imports
# ---------------------------------------------------------------------------
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from tools.lib.db import DB_PATH as GOV_DB

REQUIRED_ENTITY_TABLES = (
    "entities",
    "xwalk",
    "entity_aliases",
    "entity_identifiers",
    "entity_edges",
)

# ---------------------------------------------------------------------------
# FastMCP server (lazy — only instantiated when mcp package is available)
# ---------------------------------------------------------------------------
if FastMCP is not None:
    mcp = FastMCP("intelligence")
else:
    # Stub so @mcp.tool() decorators don't crash at import time.
    # Functions remain importable as plain functions.
    class _MCPStub:
        @staticmethod
        def tool():
            return lambda fn: fn

        def run(self, **kwargs):
            raise RuntimeError(
                "mcp package not installed. "
                "Run: uvx --with mcp,duckdb python3 tools/intelligence_mcp.py"
            )

    mcp = _MCPStub()


def get_gov_con() -> duckdb.DuckDBPyConnection:
    """Return a read-only DuckDB connection with the FTS extension loaded."""
    con = duckdb.connect(str(GOV_DB), read_only=True)
    con.execute("LOAD fts;")
    missing = [
        t
        for t in REQUIRED_ENTITY_TABLES
        if con.execute(
            "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = ?", [t]
        ).fetchone()[0]
        == 0
    ]
    if missing:
        con.close()
        missing_txt = ", ".join(missing)
        raise RuntimeError(
            "Intelligence entity tables are missing: "
            f"{missing_txt}. Run: uvx --with duckdb python3 tools/build_entity_tables.py --all"
        )
    return con


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _build_entity_result(con, entity_id: str, confidence: float, method: str) -> dict:
    """Build a full entity result dict with aliases, identifiers, and datasets."""
    entity = con.execute(
        "SELECT entity_id, schema_type, name, jurisdiction FROM entities WHERE entity_id = ?",
        [entity_id],
    ).fetchone()

    if not entity:
        return {"entity_id": entity_id, "error": "not found"}

    aliases = [
        r[0]
        for r in con.execute(
            "SELECT DISTINCT alias FROM entity_aliases WHERE entity_id = ? LIMIT 10",
            [entity_id],
        ).fetchall()
    ]

    identifiers = [
        {"type": r[0], "value": r[1]}
        for r in con.execute(
            "SELECT id_type, id_value FROM entity_identifiers WHERE entity_id = ?",
            [entity_id],
        ).fetchall()
    ]

    datasets = [
        r[0]
        for r in con.execute(
            "SELECT DISTINCT dataset FROM xwalk WHERE entity_id = ?",
            [entity_id],
        ).fetchall()
    ]

    return {
        "entity_id": entity[0],
        "schema_type": entity[1],
        "name": entity[2],
        "jurisdiction": entity[3],
        "aliases": aliases,
        "identifiers": identifiers,
        "datasets_linked": datasets,
        "confidence": confidence,
        "method": method,
    }


def _resolve_to_id(con, query: str, id_type: str = "auto") -> str | None:
    """Resolve a query to a single entity_id. Returns None if not found."""
    # If it looks like an entity_id already
    if ":" in query:
        row = con.execute(
            "SELECT entity_id FROM entities WHERE entity_id = ?", [query]
        ).fetchone()
        if row:
            return row[0]

    if id_type == "auto":
        if query.isdigit() and len(query) == 10:
            id_type = "npi"
        elif query.isdigit() and len(query) == 9:
            id_type = "ein"
        elif query.isdigit():
            id_type = "npi"
        else:
            id_type = "name"

    if id_type == "entity_id":
        row = con.execute(
            "SELECT entity_id FROM entities WHERE entity_id = ?", [query]
        ).fetchone()
        return row[0] if row else None

    if id_type != "name":
        row = con.execute(
            "SELECT entity_id FROM entity_identifiers WHERE id_type = ? AND id_value = ? LIMIT 1",
            [id_type, query],
        ).fetchone()
        if row:
            return row[0]

    # Name-based: try FTS
    try:
        row = con.execute(
            """
            SELECT entity_id FROM entity_aliases
            WHERE fts_main_entity_aliases.match_bm25(entity_id, ?) IS NOT NULL
            ORDER BY fts_main_entity_aliases.match_bm25(entity_id, ?) DESC
            LIMIT 1
        """,
            [query, query],
        ).fetchone()
        if row:
            return row[0]
    except Exception:
        pass

    # Jaro-Winkler fallback
    norm = query.upper().strip()
    row = con.execute(
        """
        SELECT entity_id FROM entity_aliases
        WHERE left(normalized_alias, 3) = left(?, 3)
          AND jaro_winkler_similarity(normalized_alias, ?) > 0.85
        ORDER BY jaro_winkler_similarity(normalized_alias, ?) DESC
        LIMIT 1
    """,
        [norm, norm, norm],
    ).fetchone()
    return row[0] if row else None


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------


@mcp.tool()
def resolve_entity(query: str, id_type: str = "auto") -> str:
    """Resolve a name, NPI, EIN, or other identifier to a canonical entity.

    Args:
        query: Name, NPI, EIN, or other identifier to resolve
        id_type: Type of identifier -- auto, npi, ein, cik, dos_id, name (default: auto)

    Returns:
        JSON with canonical entity, aliases, identifiers, and confidence.
    """
    con = get_gov_con()
    try:
        results = []

        # Auto-detect identifier type
        if id_type == "auto":
            stripped = query.strip()
            if ":" in stripped:
                # Looks like an entity_id (e.g. nppes:1234567890)
                id_type = "entity_id"
            elif stripped.isdigit() and len(stripped) == 10:
                id_type = "npi"
            elif stripped.isdigit() and len(stripped) == 9:
                id_type = "ein"
            elif stripped.isdigit():
                id_type = "npi"
            else:
                id_type = "name"

        # Direct entity_id lookup
        if id_type == "entity_id":
            entity = con.execute(
                "SELECT entity_id FROM entities WHERE entity_id = ?", [query.strip()]
            ).fetchone()
            if entity:
                results.append(
                    _build_entity_result(
                        con, entity[0], confidence=1.0, method="exact_entity_id"
                    )
                )

        # ID-based lookup (NPI, EIN, CIK, etc.)
        elif id_type != "name":
            rows = con.execute(
                """
                SELECT ei.entity_id, ei.id_type, ei.id_value,
                       e.name, e.schema_type, e.jurisdiction
                FROM entity_identifiers ei
                JOIN entities e ON e.entity_id = ei.entity_id
                WHERE ei.id_type = ? AND ei.id_value = ?
                """,
                [id_type, query.strip()],
            ).fetchall()

            for row in rows:
                entity_id = row[0]
                results.append(
                    _build_entity_result(
                        con, entity_id, confidence=1.0, method=f"exact_{id_type}"
                    )
                )

        # Name-based lookup: FTS first, then jaro_winkler fallback
        if id_type == "name" or not results:
            # FTS search
            try:
                fts_rows = con.execute(
                    """
                    SELECT entity_id, alias,
                           fts_main_entity_aliases.match_bm25(entity_id, ?) AS score
                    FROM entity_aliases
                    WHERE score IS NOT NULL
                    ORDER BY score DESC
                    LIMIT 10
                    """,
                    [query],
                ).fetchall()
            except Exception:
                fts_rows = []

            seen = {
                r["entity_id"] for r in results if "entity_id" in r and "error" not in r
            }
            for row in fts_rows:
                eid = row[0]
                if eid not in seen:
                    seen.add(eid)
                    results.append(
                        _build_entity_result(con, eid, confidence=0.9, method="fts")
                    )

            # Jaro-Winkler fallback if FTS returns nothing useful
            if not results:
                norm_query = query.upper().strip()
                jw_rows = con.execute(
                    """
                    SELECT DISTINCT a.entity_id,
                           jaro_winkler_similarity(a.normalized_alias, ?) AS sim
                    FROM entity_aliases a
                    WHERE left(a.normalized_alias, 3) = left(?, 3)
                      AND jaro_winkler_similarity(a.normalized_alias, ?) > 0.85
                    ORDER BY sim DESC
                    LIMIT 10
                    """,
                    [norm_query, norm_query, norm_query],
                ).fetchall()

                for row in jw_rows:
                    eid = row[0]
                    if eid not in seen:
                        seen.add(eid)
                        results.append(
                            _build_entity_result(
                                con,
                                eid,
                                confidence=round(row[1], 3),
                                method="jaro_winkler",
                            )
                        )

        if not results:
            return json.dumps(
                {"error": "No entity found", "query": query, "id_type": id_type}
            )

        return json.dumps(
            {"results": results[:5], "total_matches": len(results)}, indent=2
        )

    finally:
        con.close()


@mcp.tool()
def search_entities(
    query: str,
    schema_type: str = "",
    jurisdiction: str = "",
    limit: int = 20,
) -> str:
    """Search for entities by name pattern with optional filters.

    Args:
        query: Name pattern to search for
        schema_type: Filter by type -- LegalEntity, Person, PublicBody (default: all)
        jurisdiction: Filter by state code or 'federal' (default: all)
        limit: Max results (default: 20, max: 50)
    """
    con = get_gov_con()
    limit = min(limit, 50)
    try:
        # FTS search
        try:
            fts_rows = con.execute(
                """
                SELECT a.entity_id, a.alias,
                       fts_main_entity_aliases.match_bm25(a.entity_id, ?) AS score
                FROM entity_aliases a
                WHERE score IS NOT NULL
                ORDER BY score DESC
                LIMIT ?
                """,
                [query, limit * 3],
            ).fetchall()
        except Exception:
            fts_rows = []

        results = []
        seen = set()
        for row in fts_rows:
            eid = row[0]
            if eid in seen:
                continue
            seen.add(eid)

            entity = con.execute(
                "SELECT entity_id, schema_type, name, jurisdiction FROM entities WHERE entity_id = ?",
                [eid],
            ).fetchone()

            if not entity:
                continue
            if schema_type and entity[1] != schema_type:
                continue
            if jurisdiction and entity[3] != jurisdiction:
                continue

            results.append(
                {
                    "entity_id": entity[0],
                    "schema_type": entity[1],
                    "name": entity[2],
                    "jurisdiction": entity[3],
                    "match_alias": row[1],
                    "score": round(row[2], 4),
                }
            )

            if len(results) >= limit:
                break

        return json.dumps({"results": results, "total": len(results)}, indent=2)

    finally:
        con.close()


@mcp.tool()
def get_dossier(query: str, id_type: str = "auto") -> str:
    """Get a comprehensive summary dossier for an entity.

    Returns scalar aggregates (total spend, sanctions, donations, connections)
    plus flags and top connected entities. NOT raw data -- use find_connections
    or raw SQL for drill-down.

    Args:
        query: Entity name, NPI, EIN, or entity_id (e.g. 'nppes:1417262056')
        id_type: auto, npi, ein, name, entity_id (default: auto)
    """
    con = get_gov_con()
    try:
        entity_id = _resolve_to_id(con, query, id_type)
        if not entity_id:
            return json.dumps({"error": "Entity not found", "query": query})

        # --- Core entity info ---
        entity = con.execute(
            "SELECT entity_id, schema_type, name, jurisdiction FROM entities WHERE entity_id = ?",
            [entity_id],
        ).fetchone()

        dossier = {
            "entity_id": entity[0],
            "schema_type": entity[1],
            "name": entity[2],
            "jurisdiction": entity[3],
        }

        # --- Identifiers ---
        identifiers = con.execute(
            "SELECT id_type, id_value FROM entity_identifiers WHERE entity_id = ?",
            [entity_id],
        ).fetchall()
        dossier["identifiers"] = [{"type": r[0], "value": r[1]} for r in identifiers]

        # --- Aliases ---
        aliases = con.execute(
            "SELECT DISTINCT alias FROM entity_aliases WHERE entity_id = ? LIMIT 10",
            [entity_id],
        ).fetchall()
        dossier["aliases"] = [r[0] for r in aliases]

        # --- Datasets linked ---
        datasets = con.execute(
            "SELECT DISTINCT dataset FROM xwalk WHERE entity_id = ?",
            [entity_id],
        ).fetchall()
        dossier["datasets_linked"] = [r[0] for r in datasets]

        # --- Spending aggregates (look up NPI from identifiers) ---
        npi_ids = [r[1] for r in identifiers if r[0] == "npi"]
        spending = None
        if npi_ids:
            try:
                npi = npi_ids[0]
                row = con.execute(
                    """
                    SELECT
                        total_paid, total_claims, n_years,
                        first_claim_month, last_claim_month
                    FROM npi_spending_summary
                    WHERE npi = ?
                """,
                    [npi],
                ).fetchone()
                if row and row[0] is not None:
                    spending = {
                        "total_paid": float(row[0]),
                        "total_claims": int(row[1]),
                        "months_active": int(row[2]),
                        "first_month": str(row[3]),
                        "last_month": str(row[4]),
                    }
            except Exception:
                pass
        dossier["spending"] = spending

        # --- Enforcement: sanctions from entity_edges ---
        sanctions = con.execute(
            """
            SELECT e.target_id, t.name AS target_name, e.start_date, e.end_date,
                   e.dataset, e.source_grade, e.details
            FROM entity_edges e
            LEFT JOIN entities t ON t.entity_id = e.target_id
            WHERE e.source_id = ? AND e.rel_type = 'sanctioned'
        """,
            [entity_id],
        ).fetchall()

        # Also check if this entity IS a sanction target
        sanctions_as_target = con.execute(
            """
            SELECT e.source_id, s.name AS source_name, e.start_date, e.end_date,
                   e.dataset, e.source_grade, e.details
            FROM entity_edges e
            LEFT JOIN entities s ON s.entity_id = e.source_id
            WHERE e.target_id = ? AND e.rel_type = 'sanctioned'
        """,
            [entity_id],
        ).fetchall()

        sanction_records = []
        for r in sanctions:
            sanction_records.append(
                {
                    "direction": "subject_sanctioned",
                    "related_entity": r[1],
                    "start_date": str(r[2]) if r[2] else None,
                    "end_date": str(r[3]) if r[3] else None,
                    "dataset": r[4],
                    "source_grade": r[5],
                }
            )
        for r in sanctions_as_target:
            sanction_records.append(
                {
                    "direction": "sanctioned_by",
                    "related_entity": r[1],
                    "start_date": str(r[2]) if r[2] else None,
                    "end_date": str(r[3]) if r[3] else None,
                    "dataset": r[4],
                    "source_grade": r[5],
                }
            )
        dossier["sanctions"] = sanction_records

        # --- Ownership (owns / owned by) ---
        owns = con.execute(
            """
            SELECT e.target_id, t.name, e.percentage, e.dataset
            FROM entity_edges e
            LEFT JOIN entities t ON t.entity_id = e.target_id
            WHERE e.source_id = ? AND e.rel_type = 'owns'
            LIMIT 20
        """,
            [entity_id],
        ).fetchall()

        owned_by = con.execute(
            """
            SELECT e.source_id, s.name, e.percentage, e.dataset
            FROM entity_edges e
            LEFT JOIN entities s ON s.entity_id = e.source_id
            WHERE e.target_id = ? AND e.rel_type = 'owns'
            LIMIT 20
        """,
            [entity_id],
        ).fetchall()

        dossier["ownership"] = {
            "owns": [
                {
                    "entity_id": r[0],
                    "name": r[1],
                    "percentage": float(r[2]) if r[2] is not None else None,
                    "dataset": r[3],
                }
                for r in owns
            ],
            "owned_by": [
                {
                    "entity_id": r[0],
                    "name": r[1],
                    "percentage": float(r[2]) if r[2] is not None else None,
                    "dataset": r[3],
                }
                for r in owned_by
            ],
        }

        # --- Connected entities count ---
        conn_count = con.execute(
            """
            SELECT COUNT(DISTINCT other_id) FROM (
                SELECT target_id AS other_id FROM entity_edges WHERE source_id = ?
                UNION ALL
                SELECT source_id AS other_id FROM entity_edges WHERE target_id = ?
            )
        """,
            [entity_id, entity_id],
        ).fetchone()
        dossier["connected_entity_count"] = conn_count[0] if conn_count else 0

        # --- Deactivated NPI check ---
        deactivated_npi = False
        if npi_ids:
            try:
                for npi in npi_ids:
                    row = con.execute(
                        """
                        SELECT deactivation_date FROM nppes
                        WHERE NPI = TRY_CAST(? AS BIGINT)
                          AND deactivation_date IS NOT NULL
                    """,
                        [npi],
                    ).fetchone()
                    if row:
                        deactivated_npi = True
                        break
            except Exception:
                pass

        # --- Flags ---
        flags = []
        if spending and spending["total_paid"] >= 1_000_000_000:
            flags.append("billion_dollar_biller")
        if sanction_records:
            flags.append("sanctioned")
        if deactivated_npi:
            flags.append("deactivated_npi")
        dossier["flags"] = flags

        return json.dumps(dossier, indent=2, default=str)

    finally:
        con.close()


@mcp.tool()
def screen_entity(query: str, id_type: str = "auto") -> str:
    """Screen an entity against all enforcement/sanctions databases.

    Checks: LEIE, SAM, OSHA, OpenSanctions matches, entity_edges sanctions.

    Args:
        query: Entity name, NPI, EIN, or entity_id
        id_type: auto, npi, ein, name, entity_id (default: auto)
    """
    con = get_gov_con()
    try:
        entity_id = _resolve_to_id(con, query, id_type)
        if not entity_id:
            return json.dumps({"error": "Entity not found", "query": query})

        # Get entity info
        entity = con.execute(
            "SELECT entity_id, schema_type, name, jurisdiction FROM entities WHERE entity_id = ?",
            [entity_id],
        ).fetchone()
        entity_name = entity[2] if entity else query

        # Get NPI(s) for cross-referencing
        identifiers = con.execute(
            "SELECT id_type, id_value FROM entity_identifiers WHERE entity_id = ?",
            [entity_id],
        ).fetchall()
        npi_ids = [r[1] for r in identifiers if r[0] == "npi"]

        hits = []

        # --- 1. Entity edges: sanctions ---
        sanction_edges = con.execute(
            """
            SELECT e.target_id, t.name, e.start_date, e.end_date, e.dataset, e.source_grade
            FROM entity_edges e
            LEFT JOIN entities t ON t.entity_id = e.target_id
            WHERE e.source_id = ? AND e.rel_type = 'sanctioned'
        """,
            [entity_id],
        ).fetchall()

        sanction_edges_rev = con.execute(
            """
            SELECT e.source_id, s.name, e.start_date, e.end_date, e.dataset, e.source_grade
            FROM entity_edges e
            LEFT JOIN entities s ON s.entity_id = e.source_id
            WHERE e.target_id = ? AND e.rel_type = 'sanctioned'
        """,
            [entity_id],
        ).fetchall()

        for r in sanction_edges:
            hits.append(
                {
                    "source": r[4],  # dataset (leie, sam, etc.)
                    "grade": r[5],
                    "type": "sanction",
                    "details": f"Sanctioned -> {r[1]}; start={r[2]}, end={r[3]}",
                }
            )
        for r in sanction_edges_rev:
            hits.append(
                {
                    "source": r[4],
                    "grade": r[5],
                    "type": "sanction",
                    "details": f"Sanctioned by {r[1]}; start={r[2]}, end={r[3]}",
                }
            )

        # --- 2. OSHA violations (match on entity name) ---
        try:
            search_name = entity_name[:30] if entity_name else ""
            if search_name:
                osha_rows = con.execute(
                    """
                    SELECT i.activity_nr, i.estab_name, i.open_date, i.site_city, i.site_state,
                           v.issuance_date, v.viol_type, v.current_penalty
                    FROM osha_inspections i
                    JOIN osha_violations v ON i.activity_nr = v.activity_nr
                    WHERE i.estab_name ILIKE '%' || ? || '%'
                    LIMIT 20
                """,
                    [search_name],
                ).fetchall()

                for r in osha_rows:
                    hits.append(
                        {
                            "source": "osha",
                            "grade": "[A2]",
                            "type": "osha_violation",
                            "details": (
                                f"Estab: {r[1]}; city={r[3]}, state={r[4]}; "
                                f"viol_type={r[6]}; penalty=${r[7]}"
                            ),
                        }
                    )
        except Exception:
            pass  # OSHA views may not exist

        # --- 3. OpenSanctions screening results ---
        try:
            if npi_ids:
                for npi in npi_ids:
                    os_rows = con.execute(
                        """
                        SELECT * FROM opensanctions_screening
                        WHERE CAST(npi AS VARCHAR) = ?
                        LIMIT 10
                    """,
                        [npi],
                    ).fetchall()

                    cols = [d[0] for d in con.description] if con.description else []
                    for r in os_rows:
                        row_dict = dict(zip(cols, r))
                        hits.append(
                            {
                                "source": "opensanctions",
                                "grade": "[B3]",
                                "type": "sanctions_screening",
                                "details": json.dumps(row_dict, default=str),
                            }
                        )
        except Exception:
            pass  # opensanctions_screening view may not exist

        # --- 4. OpenSanctions batch results ---
        try:
            if npi_ids:
                for npi in npi_ids:
                    batch_rows = con.execute(
                        """
                        SELECT * FROM opensanctions_batch
                        WHERE CAST(npi AS VARCHAR) = ?
                        LIMIT 10
                    """,
                        [npi],
                    ).fetchall()

                    cols = [d[0] for d in con.description] if con.description else []
                    for r in batch_rows:
                        row_dict = dict(zip(cols, r))
                        hits.append(
                            {
                                "source": "opensanctions_batch",
                                "grade": "[B3]",
                                "type": "sanctions_screening",
                                "details": json.dumps(row_dict, default=str),
                            }
                        )
        except Exception:
            pass  # opensanctions_batch view may not exist

        result = {
            "entity_id": entity_id,
            "entity_name": entity_name,
            "clean": len(hits) == 0,
            "hit_count": len(hits),
            "hits": hits,
        }

        return json.dumps(result, indent=2, default=str)

    finally:
        con.close()


@mcp.tool()
def find_connections(
    query: str,
    id_type: str = "auto",
    hops: int = 1,
    rel_types: str = "",
    limit: int = 50,
) -> str:
    """Find entities connected to a given entity via the edge graph.

    Args:
        query: Entity name, NPI, EIN, or entity_id
        id_type: auto, npi, ein, name, entity_id (default: auto)
        hops: Number of hops (1-3, default: 1)
        rel_types: Comma-separated filter -- owns,sanctioned,donates_to,contracts_with,lobbies (default: all)
        limit: Max results (default: 50)
    """
    con = get_gov_con()
    try:
        entity_id = _resolve_to_id(con, query, id_type)
        if not entity_id:
            return json.dumps({"error": "Entity not found", "query": query})

        # Get source entity info
        entity = con.execute(
            "SELECT entity_id, schema_type, name FROM entities WHERE entity_id = ?",
            [entity_id],
        ).fetchone()
        source_info = (
            {
                "entity_id": entity[0],
                "schema_type": entity[1],
                "name": entity[2],
            }
            if entity
            else {"entity_id": entity_id, "name": "unknown"}
        )

        # Cap hops and limit
        hops = max(1, min(hops, 3))
        limit = max(1, min(limit, 50))

        # Build rel_type filter
        rel_filter = ""
        rel_params = []
        if rel_types.strip():
            types = [t.strip() for t in rel_types.split(",") if t.strip()]
            if types:
                placeholders = ", ".join(["?"] * len(types))
                rel_filter = f"AND ee.rel_type IN ({placeholders})"
                rel_params = types

        if hops == 1:
            # Simple 1-hop query
            sql = """
                SELECT
                    CASE WHEN ee.source_id = ? THEN ee.target_id ELSE ee.source_id END AS connected_id,
                    ee.rel_type,
                    ee.amount,
                    ee.percentage,
                    ee.dataset,
                    ee.source_grade,
                    CASE WHEN ee.source_id = ? THEN 'outgoing' ELSE 'incoming' END AS direction
                FROM entity_edges ee
                WHERE (ee.source_id = ? OR ee.target_id = ?)
            """
            params = [entity_id, entity_id, entity_id, entity_id]

            if rel_params:
                sql += f" AND ee.rel_type IN ({', '.join(['?'] * len(rel_params))})"
                params.extend(rel_params)

            sql += " ORDER BY COALESCE(ee.amount, 0) DESC LIMIT ?"
            params.append(limit)

            rows = con.execute(sql, params).fetchall()

            connections = []
            for r in rows:
                connected_id = r[0]
                # Look up name and schema_type
                ent = con.execute(
                    "SELECT schema_type, name FROM entities WHERE entity_id = ?",
                    [connected_id],
                ).fetchone()
                connections.append(
                    {
                        "entity_id": connected_id,
                        "name": ent[1] if ent else None,
                        "schema_type": ent[0] if ent else None,
                        "rel_type": r[1],
                        "amount": float(r[2]) if r[2] is not None else None,
                        "percentage": float(r[3]) if r[3] is not None else None,
                        "dataset": r[4],
                        "source_grade": r[5],
                        "direction": r[6],
                        "depth": 1,
                    }
                )

        else:
            # Multi-hop recursive CTE
            # Build the rel_filter for use inside the CTE
            cte_rel_filter_1 = ""
            cte_rel_filter_2 = ""
            if rel_params:
                placeholders = ", ".join(["?"] * len(rel_params))
                cte_rel_filter_1 = f"AND ee.rel_type IN ({placeholders})"
                cte_rel_filter_2 = f"AND ee.rel_type IN ({placeholders})"

            sql = f"""
                WITH RECURSIVE paths AS (
                    SELECT
                        CASE WHEN ee.source_id = ? THEN ee.target_id ELSE ee.source_id END AS node,
                        ee.rel_type,
                        ee.amount,
                        ee.percentage,
                        ee.dataset,
                        ee.source_grade,
                        1 AS depth,
                        ARRAY[?::VARCHAR] AS visited
                    FROM entity_edges ee
                    WHERE (ee.source_id = ? OR ee.target_id = ?)
                      {cte_rel_filter_1}

                    UNION ALL

                    SELECT
                        CASE WHEN ee.source_id = p.node THEN ee.target_id ELSE ee.source_id END,
                        ee.rel_type,
                        ee.amount,
                        ee.percentage,
                        ee.dataset,
                        ee.source_grade,
                        p.depth + 1,
                        array_append(p.visited, p.node)
                    FROM entity_edges ee
                    JOIN paths p ON (ee.source_id = p.node OR ee.target_id = p.node)
                    WHERE p.depth < ?
                      AND NOT array_contains(p.visited,
                          CASE WHEN ee.source_id = p.node THEN ee.target_id ELSE ee.source_id END)
                      {cte_rel_filter_2}
                )
                SELECT DISTINCT node, rel_type, amount, percentage, dataset, source_grade, depth
                FROM paths
                ORDER BY depth, COALESCE(amount, 0) DESC
                LIMIT ?
            """
            params = [entity_id, entity_id, entity_id, entity_id]
            params.extend(rel_params)  # for cte_rel_filter_1
            params.append(hops)
            params.extend(rel_params)  # for cte_rel_filter_2
            params.append(limit)

            rows = con.execute(sql, params).fetchall()

            connections = []
            for r in rows:
                connected_id = r[0]
                ent = con.execute(
                    "SELECT schema_type, name FROM entities WHERE entity_id = ?",
                    [connected_id],
                ).fetchone()
                connections.append(
                    {
                        "entity_id": connected_id,
                        "name": ent[1] if ent else None,
                        "schema_type": ent[0] if ent else None,
                        "rel_type": r[1],
                        "amount": float(r[2]) if r[2] is not None else None,
                        "percentage": float(r[3]) if r[3] is not None else None,
                        "dataset": r[4],
                        "source_grade": r[5],
                        "depth": r[6],
                    }
                )

        result = {
            "source_entity": source_info,
            "hops": hops,
            "rel_types_filter": rel_types if rel_types else "all",
            "connections": connections,
            "total": len(connections),
        }
        return json.dumps(result, indent=2, default=str)

    finally:
        con.close()


@mcp.tool()
def flag_anomalies(query: str = "", jurisdiction: str = "", limit: int = 50) -> str:
    """Flag statistical anomalies: explosive growth, deactivated-but-billing, concentration.

    Args:
        query: Entity name/NPI to check (default: scan all)
        jurisdiction: Filter by state (default: all)
        limit: Max results (default: 50)
    """
    con = get_gov_con()
    try:
        limit = max(1, min(limit, 50))
        flags = []

        if query.strip():
            # --- Entity-specific mode: check for explosive growth ---
            entity_id = _resolve_to_id(con, query)
            if not entity_id:
                return json.dumps({"error": "Entity not found", "query": query})

            entity = con.execute(
                "SELECT entity_id, schema_type, name FROM entities WHERE entity_id = ?",
                [entity_id],
            ).fetchone()
            entity_name = entity[2] if entity else query

            # Get NPI(s) for this entity
            npi_ids = [
                r[0]
                for r in con.execute(
                    "SELECT id_value FROM entity_identifiers WHERE entity_id = ? AND id_type = 'npi'",
                    [entity_id],
                ).fetchall()
            ]

            if not npi_ids:
                return json.dumps(
                    {
                        "entity_id": entity_id,
                        "entity_name": entity_name,
                        "flags": [],
                        "note": "No NPI linked — cannot check spending anomalies",
                    }
                )

            for npi in npi_ids:
                # Growth check: 2019 vs 2024
                row = con.execute(
                    """
                    SELECT
                        COALESCE((SELECT yearly_paid FROM npi_yearly_spending
                                  WHERE npi = s.npi AND year = '2019'), 0) AS spend_2019,
                        COALESCE((SELECT yearly_paid FROM npi_yearly_spending
                                  WHERE npi = s.npi AND year = '2024'), 0) AS spend_2024,
                        s.total_paid AS total_all
                    FROM npi_spending_summary s
                    WHERE s.npi = ?
                """,
                    [npi],
                ).fetchone()

                if row and row[0] is not None:
                    spend_2019 = float(row[0])
                    spend_2024 = float(row[1])
                    total_all = float(row[2])

                    if spend_2019 > 0:
                        growth_pct = ((spend_2024 - spend_2019) / spend_2019) * 100
                    elif spend_2024 > 0:
                        growth_pct = float("inf")
                    else:
                        growth_pct = 0.0

                    flag_entry = {
                        "npi": npi,
                        "entity_id": entity_id,
                        "entity_name": entity_name,
                        "spend_2019": spend_2019,
                        "spend_2024": spend_2024,
                        "total_all_years": total_all,
                        "growth_pct": growth_pct
                        if growth_pct != float("inf")
                        else "inf",
                    }

                    if growth_pct > 500:
                        flag_entry["flag"] = "explosive_growth"
                        flag_entry["severity"] = "high"
                    elif growth_pct > 200:
                        flag_entry["flag"] = "rapid_growth"
                        flag_entry["severity"] = "medium"
                    elif spend_2019 == 0 and spend_2024 > 1_000_000:
                        flag_entry["flag"] = "new_high_volume"
                        flag_entry["severity"] = "medium"
                    else:
                        flag_entry["flag"] = "normal_growth"
                        flag_entry["severity"] = "low"

                    # Check deactivation
                    deact = con.execute(
                        """
                        SELECT deactivation_date FROM nppes
                        WHERE NPI = TRY_CAST(? AS BIGINT)
                          AND deactivation_date IS NOT NULL
                    """,
                        [npi],
                    ).fetchone()
                    if deact:
                        flag_entry["deactivated"] = str(deact[0])
                        flag_entry["flag"] = "deactivated_but_billing"
                        flag_entry["severity"] = "critical"

                    flags.append(flag_entry)

            result = {
                "entity_id": entity_id,
                "entity_name": entity_name,
                "flags": flags,
                "total": len(flags),
            }

        else:
            # --- Scan mode: deactivated NPIs still billing ---
            jurisdiction_filter = ""
            jurisdiction_params = []
            if jurisdiction.strip():
                jurisdiction_filter = "AND n.state = ?"
                jurisdiction_params = [jurisdiction.strip().upper()]

            rows = con.execute(
                f"""
                SELECT
                    s.npi,
                    n.org_name,
                    n.last_name,
                    n.first_name,
                    n.state,
                    n.deactivation_date,
                    s.total_paid,
                    s.total_claims,
                    s.last_claim_month AS last_billing_month
                FROM npi_spending_summary s
                JOIN nppes n ON TRY_CAST(s.npi AS BIGINT) = n.NPI
                WHERE n.deactivation_date IS NOT NULL
                  {jurisdiction_filter}
                ORDER BY s.total_paid DESC
                LIMIT ?
            """,
                [*jurisdiction_params, limit],
            ).fetchall()

            for r in rows:
                name = r[1] if r[1] else f"{r[3] or ''} {r[2] or ''}".strip()
                flags.append(
                    {
                        "npi": r[0],
                        "name": name,
                        "state": r[4],
                        "deactivation_date": str(r[5]) if r[5] else None,
                        "total_paid": float(r[6]),
                        "total_claims": int(r[7]),
                        "last_billing_month": r[8],
                        "flag": "deactivated_but_billing",
                        "severity": "critical",
                    }
                )

            result = {
                "scan_type": "deactivated_but_billing",
                "jurisdiction": jurisdiction if jurisdiction else "all",
                "flags": flags,
                "total": len(flags),
            }

        return json.dumps(result, indent=2, default=str)

    finally:
        con.close()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if FastMCP is None:
        print(
            "Error: mcp package required. "
            "Run: uvx --with mcp,duckdb python3 tools/intelligence_mcp.py",
            file=sys.stderr,
        )
        sys.exit(1)
    mcp.run(transport="stdio")
## Cross-Model Review: Agent Skill Architecture
**Mode:** Review
**Date:** 2026-02-28
**Models:** Gemini 3.1 Pro, GPT-5.2
**Constitutional anchoring:** Yes (CONSTITUTION.md, GOALS.md)

---

### Verified Findings (adopt)

| Finding | Source | Verified How |
|---------|--------|-------------|
| ACH must be available to trade workflow, not locked in investigate | Gemini + GPT | CONSTITUTION.md P11: "Before any trade recommendation" — broader than fraud |
| Source-grading scope is project-wide (P3), not investigate-only | Gemini | P3: "every claim that enters entity files or analysis docs" |
| Change #7 (trade-thesis) is highest priority, not lowest | Gemini + GPT | GPT quantified: P9=10%, P11=35%, P12=5% coverage. Core mission gap. |
| Change #6 (trim Exa section) must be conditional on #5 (hook) | GPT | Logically valid: removing guidance before enforcement exists worsens behavior |
| Entity-management: add investment categories, don't delete bio | GPT | P8: "physiological signals where research-validated" |
| 51% violation rate doesn't prove instruction is useless — no counterfactual | GPT | Valid: instruction may reduce from 90%→51%, not 0%→51% |
| Prediction ledger is a missing constitutional artifact | GPT | P5 (Fast Feedback), P9 (Portfolio as Scorecard), GOALS.md (≥20 predictions/quarter) |
| Trade tickets need a linter/hook, not just a skill | GPT | "instructions alone = 0% reliable" applies to trade-thesis too |

### Where I (Claude) Was Wrong

| My Original Claim | Reality | Who Caught It |
|-------------------|---------|--------------|
| "Inline source-grading into investigate" | P3 mandates grading for ALL entity files and analysis, not just investigation. Inlining isolates epistemics to secondary mission. | Gemini |
| "Inline competing-hypotheses into investigate Phase 4" | ACH is constitutionally required for trade recommendations (P11), not just fraud leads. Burying it in investigate breaks the primary mission workflow. | Gemini + GPT |
| "Change #7 defer?" | This is the highest-impact change. P9/P11/P12 are the least-covered principles and most central to the generative principle. | Gemini + GPT |
| "Update entity-management: remove genes/drugs" | P8 explicitly values multi-domain signals including physiological. Add investment categories, keep bio as secondary. | GPT |
| "Trim researcher Exa section" as independent action | Must be conditional on Exa hook deployment. Standalone removal worsens behavior. | GPT |

### Gemini Errors (distrust)

| Claim | Why Wrong |
|-------|-----------|
| "Claude Code cannot natively spawn independent Gemini/GPT agents via Task tools" | Partially wrong. Task tool agents are Claude, but they can call llmx internally. The competing-hypotheses skill itself says "If multi-model dispatch isn't available, same-model agents still have value." Architecture works indirectly. |
| "Create a dedicated Python script for sequential Exa, removing direct API access" | Over-engineered. Would require an MCP server wrapper or tool replacement. A stateful PreToolUse hook (tracking calls via $PPID temp file) is simpler and doesn't break existing MCP architecture. |
| "Rename source-grading to epistemics-finance and expand" | Scope creep. The Admiralty system IS domain-agnostic — that's its strength. Adding SEC-specific source types is fine but doesn't justify a full skill rename and expansion. |
| "Rewrite epistemics for the Financial Domain" | P8 says "physiological signals where research-validated." Purging bio epistemics would violate this. The investment research domain's epistemics are already in the Constitution (P2-4, P7, P11). A financial-epistemics skill would largely duplicate constitutional text. |
| "Build a dataset-joiner orchestration skill" | Interesting idea but over-scoped. Entity resolution is ad-hoc and domain-specific. A skill template for DuckDB joins would be low-reuse. |
| Temperature override (0.3 → 1.0) | Gemini 3.1 Pro locks temperature server-side — expected. Noted in model-review skill already. |

### GPT Errors (distrust)

| Claim | Why Wrong |
|-------|-----------|
| "Coverage score P7 (Honest About Provenance) = 80%" | Likely overestimate. Dual provenance schema (Admiralty vs researcher tags) creates real ambiguity. Without enforcement hooks, actual compliance in outputs is probably lower. |
| "Effort: 12-30 hours for trade-thesis skill" | Likely underestimate for the full ticket system with linter + Kelly script. But reasonable for a minimal skill without architectural enforcement. |
| "Archived = possibly still accessible internally" | Incorrect for Claude Code skills. Archived skills in archive/ subdirectory are not symlinked and not loaded. The broken reference is real. |
| "Unify provenance into a single canonical claim object schema with renderers" | Over-engineered. Two schemas serve different contexts (investigation vs general research). Clarifying when each applies is simpler than building a unified data model. |

### Revised Priority List

Based on both reviews, constitutional alignment, and fact-checking:

1. **Build trade-thesis skill + ticket linter (was #7, now #1)**
   - Why: P9=10%, P11=35%, P12=5%. Largest constitutional gap. Primary mission enabler.
   - Scope: trade ticket template + required fields + pre-commit linter + Kelly sizing script
   - Testable: ≥95% of trade proposals include thesis/falsification/sizing/exits

2. **Unarchive competing-hypotheses as standalone (was #2, approach changed)**
   - Why: ACH is needed for BOTH trade theses (P11) and fraud investigation. Inlining into investigate would restrict it.
   - Change: Unarchive, keep standalone, make available to both investigate and trade-thesis workflows.

3. **Keep source-grading standalone (was #1, approach reversed)**
   - Why: P3 mandates grading for ALL entity files and analysis docs. Standalone keeps it universally available.
   - Change: Keep as-is. Add 3-line quick-reference in entity-management. Clarify researcher's "don't mix" language.

4. **Build prediction ledger (NEW — GPT recommendation)**
   - Why: P5 (Fast Feedback), P9 (Portfolio as Scorecard), GOALS.md (≥20 predictions/quarter, calibration curve).
   - Scope: predictions.csv schema + resolver job
   - Testable: ≥20 predictions/quarter with deadlines and resolution tracking

5. **Build Exa throttle hook (was #5, keep)**
   - Why: 51% violation rate. Sequential evidence incorporation is structurally important.
   - Change: Stateful PreToolUse hook tracking Exa calls per turn via $PPID. Do NOT trim researcher Exa section until hook proves effective.

6. **Entity-management: add investment categories, keep bio (was #4, approach changed)**
   - Change: Add companies/, people/, contracts/, filings/ as primary. Keep genes/, drugs/ as secondary (P8).

7. **Trim goals to drift-detection focus (was #3, keep as lowest priority)**
   - Lowest priority because disable-model-invocation means no context cost. Still worth doing for usability.

### Dropped Changes

- **#6 (Trim researcher Exa section):** Conditional on #5. Do not trim until hook proves effective (measure burst rate before/after).
# Cross-Model Review: Meta Constitutional Questions
**Mode:** Review (critical)
**Date:** 2026-02-28
**Models:** Gemini 3.1 Pro, GPT-5.2
**Constitutional anchoring:** GOALS.md (yes), CONSTITUTION.md (not yet created — this review informs it)
**Extraction:** 56 items extracted, 45 included, 7 merged, 3 deferred, 1 already handled

## Question 1: Enforcement Granularity

### Surviving Framework: "Cascading vs. Epistemic" + ROI Model

Both models converge on the same answer from different angles:

**Gemini** proposes a qualitative divide: hard hooks for cascading token waste and irreversible state corruption; Stop/advisory hooks for epistemic discipline (source tagging, hypothesis generation). Hard-blocking mid-investigation for a missing source tag derails the train of thought.

**GPT** proposes a quantitative ROI model: `Benefit ≈ f × L × p_prevent` vs `Cost ≈ E_dev + (f × p_false+ × t_interrupt)`. The ranking: tiny fail-closed set (high f × L, deterministic predicate) > warn-only hooks > instruction-only.

**Synthesis — what to enforce first (by expected loss):**

| Priority | Principle | Enforcement | Why first |
|----------|-----------|------------|-----------|
| 1 | Spin loops / repeated failures | PostToolUse counter + block | Already deployed (bash-failure-loop). 145 errors in one session = highest observed L. |
| 2 | Multiline bash parse errors | PreToolUse block | Already deployed (bash-loop-guard). 178/wk frequency. |
| 3 | Protected data writes | PreToolUse block | Available but not deployed to meta. Low false-positive risk. |
| 4 | Search burst flooding | PreToolUse warn → block at 8 | Already deployed globally. |
| 5 | Fan-out >10 ops without subagent | Advisory (instruction) → promote if measured | New. Gemini insight. Need regret data first. |

**What stays instructional (for now):** Sycophancy pushback, "changes must be testable," epistemic discipline. These are semantic predicates — hooks can't evaluate them deterministically. The Stop hook checklist is the right enforcement level.

**Prerequisite (both models agree):** Hook ROI telemetry. Log every hook trigger/decision to `~/.claude/hook-interventions.jsonl`. Without false-positive data, you can't promote or demote hooks rationally. Build this BEFORE adding more hooks.

### Key Disagreement: Sycophancy

Gemini says replace sycophancy instructions with a PreToolUse:Write hook requiring plan.md before >50-line scripts. This is creative but brittle — it would block legitimate rapid prototyping. The architectural fix for sycophancy is session-analyst (post-hoc detection) + the "No is a valid answer" instruction (imperfect but cheap). Accept this as a known weakness rather than over-engineering a hook.

## Question 2: Autonomy Gradient Threshold

### Surviving Framework: Reversibility + Blast Radius (not "obviousness")

Both models agree: "clear improvement" is unmeasurable. Replace with concrete proxies.

**Gemini** proposes: autonomous if (A) target is stateless AND (B) agent can write+execute a verification test. Propose if change alters shared state or no test is possible.

**GPT** proposes: rubric scoring blast radius, reversibility, ambiguity (# viable solutions), evidence count, measurability. Gate rule: score ≥ threshold OR touches shared hooks/global rules → propose + wait.

**Synthesis — the operationalized boundary:**

**Autonomous (just do it):**
- Change affects only meta's own files (not shared/global)
- Change is easily reversible (git revert suffices)
- There's one obvious approach (not multiple competing designs)
- No other project's behavior changes as a result

**Propose and wait:**
- Change touches shared infrastructure (global CLAUDE.md, shared hooks, shared skills)
- Multiple viable approaches exist with different tradeoffs
- Change affects how OTHER projects behave
- Change involves deleting or restructuring existing architecture

**Always human-approved:**
- CONSTITUTION.md, GOALS.md

**GPT's rollback contract point is valid but premature.** Adding a formal rollback plan to every self-modification is over-engineering at current scale. The git log IS the rollback mechanism. If autonomous changes start producing reverts (measurable), add the rollback contract then.

**GPT's reliability floor constraint is important.** The dual telos (autonomy + error correction) needs an implicit constraint: autonomy only increases if reliability holds. If supervision drops but errors go undetected, the system is broken. Track both.

## Question 3: Skills Directory Merge

### The Models Disagree — And GPT Is Right

**Gemini** says merge skills/ into meta/skills/ for unified git history. Bratman's planning agency demands it.

**GPT** says keep separate + formalize with version tags and per-project pins. Merge doesn't automatically solve versioning/propagation. ROI ranking: keep separate + version > merge.

**Why GPT is right for this case:**

1. `~/.claude/skills/` is a symlink to `~/Projects/skills/`. Claude Code loads skills from `~/.claude/skills/`. If skills move into meta, the symlink changes to `~/Projects/meta/skills/`. Technically simple.

2. But skills/ has its own git history, its own `.git`. Merging means either losing that history or doing a git-filter-repo merge (complex, fragile).

3. Gemini's "unified git log" argument assumes you need atomic commits spanning improvement-log + skill code. In practice, the improvement-log entry and the skill fix can cross-reference each other by commit hash. They don't need to be in the same repo.

4. The real problem isn't directory location — it's propagation tracking. Whether skills are in meta or separate, you need to know: is this project running the latest version of this skill?

**Recommendation: Keep separate. Add lightweight governance.**
- Add version tags to skills repo (just `git tag v0.X` after significant changes)
- Add a `skills-manifest.json` or similar that meta maintains — lists each skill, current version, which projects use it
- meta's session-analyst already sees skill usage across projects — this is the quality feedback loop
- Merge only if the separate directory causes concrete friction (not theoretical)

### Gemini Error

G19 (self-doubt) was correct: "I might be underestimating symlink/path complexity." The symlink chain is simple but the git history merge would be messy. Gemini's philosophical argument (Bratman) is sound but the practical recommendation is wrong.

### GPT Error

P10 suggests submodules as a viable option. For a single operator, submodules add friction with no benefit over simple symlinks + tags. GPT flagged this in P27 (self-doubt). Discard submodule recommendation.

## Cross-Cutting Insights

### Both Models Agree On (verified)

1. **Hook ROI telemetry is the prerequisite** — can't optimize enforcement without measuring false positives and interventions (G5, G14, P19)
2. **"Obviousness" must be replaced with measurable proxies** — reversibility and blast radius (G1, G6, G9, P9)
3. **Instructions work for some things** — EoG "0% reliable" is task-dependent. Simple format rules work >0%. Semantic predicates don't. (G2, P1, P24)
4. **Dual telos needs a constraint** — autonomy and error correction can conflict without a reliability floor (P3)
5. **Regret/corrections per session should be a first-class metric** (G5, P23)

### Where Both Models Are Wrong

1. **Production-grade recommendations.** Both suggest formal ROI models, rubric scoring systems, version-pinning mechanisms. For a single operator with ~5 projects, the right answer is simpler: a checklist in the agent's head (CLAUDE.md), not a scoring framework. Start with the checklist, formalize only if the checklist fails.

2. **Over-indexing on measurement.** "Measure everything" is correct in principle but expensive in practice. Start with the one metric that matters most (supervision waste rate from session-analyst) and add others only when the first is stable.

### Gemini-Only Insights (verified, valuable)

- **`hookSpecificOutput.permissionDecision: ask`** — real feature, but Gemini's own self-doubt about schema stability is valid. Defer. (G3, G20)
- **Fan-out >10 ops → subagent** — good architectural rule, not yet needed in meta itself (G7)

### GPT-Only Insights (verified, valuable)

- **ROI formula for hook prioritization** — useful mental model even if not formally computed (P7)
- **Paired metrics to prevent gaming** — throughput + quality, not either alone (P26)
- **Goals alignment scores** — useful baseline showing generative principle at 55% coverage (P18)

## Summary: What Goes Into CONSTITUTION.md

From this review, the constitution should encode:

1. **Generative principle** — from GOALS.md (already written)
2. **Enforcement philosophy** — cascading/irreversible → hooks; epistemic → advisory/Stop; semantic → instruction-only
3. **Self-modification boundary** — reversibility + blast radius, not "obviousness"
4. **Invariants** — CONSTITUTION.md and GOALS.md are human-owned; everything else is autonomous within the boundary
5. **Research as first-class function** — divergent/convergent cycle, not every-session
6. **Skills governance** — meta owns quality, skills stay separate with lightweight versioning
7. **Hook ROI telemetry** — measure before adding more enforcement
8. **Reliability floor** — autonomy only increases if error correction holds
# Cross-Model Review: Git Workflow for AI Agent Self-Optimization
**Mode:** Review
**Date:** 2026-02-28
**Models:** Gemini 3.1 Pro, GPT-5.2

## Where I (Claude) Was Wrong

Both models independently identified the same flaw in my reasoning:

| My Claim | Reality | Who Caught It |
|----------|---------|---------------|
| "Git is redundant with MEMORY.md/improvement-log" | Confuses current-state richness with historical observability. Mutable files overwrite their own rationale — git is the only append-only record. | Both models |
| "Agent never reads git log, so it doesn't matter" | Non sequitur. Workflow should be optimized for failure modes, not nominal behavior. Future archaeology consumers don't exist yet. | GPT |
| "Topic-organized files > chronological git" | True for execution, false for self-optimization. When a rule is deleted, the reason for its existence disappears from the file. | Gemini |

## Converged Recommendation (both models agree)

**No branches. No `--no-ff`. Yes to trailers — scoped to self-optimization artifacts.**

| Enhancement | Gemini verdict | GPT verdict | Adopt? |
|-------------|---------------|-------------|--------|
| Feature branches by default | No — too heavy for rapid-fire commits | No — low ROI, adds operational surface area | **No** |
| `--no-ff` merges | No — agent doesn't need visual grouping | No — moot without branches | **No** |
| Git trailers (lightweight) | Yes — "natively parseable, zero-friction, high ROI" | Yes — "highest signal-per-cost lever" | **Yes** |
| Long structured messages | Not recommended | Medium ROI at best — template fatigue risk | **No** |
| Branch/merge as hook targets | "Speculative, fragile, architecturally misaligned" | Low ROI — existing hooks can trigger on file patterns | **No** |

## Verified Findings

| Finding | Source | Verified How |
|---------|--------|-------------|
| Diffs preserve syntax, not semantics — same diff can mean bugfix, revert, experiment, or refactor | GPT (information theory framing) | Logical: `git diff` of "remove rule X" is identical whether the reason is benchmark failure, redundancy, or tool conflict |
| 4 commits in 112 seconds (11:57:15–11:59:07) makes branching impractical | Gemini | Verified from `git log --format='%h %ai'` |
| SessionEnd/PreCompact hooks are better merge-event substitutes | Gemini | True per hook events reference — both exist, SessionEnd fires on every session |
| Trailers are machine-parseable via `git log --format='%(trailers)'` | Both | Standard git feature |
| Session transcripts are ephemeral — Evidence: links may rot | GPT blind spot #2 | True: transcripts at `~/.claude/projects/*/UUID.jsonl` have no retention guarantee |

## Gemini Errors

| Claim | Assessment |
|-------|-----------|
| "Claude 3.7/Code" reference | Anachronism — current model is Claude Opus 4.6. Minor, doesn't affect reasoning. |
| Temperature override caveat noted in output | Accurate — Gemini thinking models lock temperature. The `-t 0.3` was correctly ignored. |

## GPT Errors

| Claim | Assessment |
|-------|-----------|
| Math notation (LaTeX) used throughout | Not wrong, but over-formal for the domain. The mutual information framing is valid but unnecessary to reach the conclusion. |
| "≥30-60% time-to-answer improvement" | Fabricated precision — no empirical basis for these specific numbers. The directional claim is plausible. |

## The Trailer Schema (GPT's recommendation, Gemini-compatible)

Both models converged on similar trailer sets. GPT's is more specific:

```
Evidence: session/<id> or improvement-log#<n>
Verifiable: yes|no
Affects: memory|rules|hooks|code
Reverts-to: <commit> (when applicable)
```

**Scope:** Only required for commits modifying CLAUDE.md, MEMORY.md, improvement-log.md, and hook code/config. Ordinary code commits keep simple messages.

## Key Insight (GPT, verified)

> "Identifiers are high-leverage bits: they let you retrieve large external context with a few bytes. This is classic indexing: small message, large recall."

A trailer like `Evidence: session/a2679f18` costs ~30 tokens but links the commit to a 450-line transcript. That's the information-theoretic argument for trailers over verbose messages.

## Open Risk (both models flagged)

Agent may hallucinate trailer values (fake Finding-IDs, claim `Verifiable: yes` without running checks). Gemini flagged this as a blind spot. GPT suggested conservative semantics: default to `Verifiable: no` unless proven. A PreToolUse:Bash hook could validate `Evidence:` references exist before allowing the commit.
# Architecture Review Synthesis — Best of 6 Model Outputs

Two rounds × 3 models. Round 1: architecture design (clean room). Round 2: red team, signal discovery, agent OS.

Models: GPT-5.2 (high reasoning), Gemini 3.1 Pro (high thinking), Claude Opus 4.6.

**Evaluation criteria**: Does this increase error-correction rate measured by market feedback? Is it better than what intel already has?

---

## TIER 1: Critical Gaps — Things intel MUST build

These came up across multiple models and address the biggest structural gap: **the feedback loop is open**.

### 1.1 Prediction Ledger (all 3 models, both rounds)

**What**: A DuckDB table + structured files making predictions first-class objects with mandatory fields: entity, claim, predicted outcome, timeframe, confidence, falsification condition, linked signals.

**Why this matters**: The constitution says "maximize error-correction rate." You can't correct errors if you don't track predictions. Currently, predictions live as prose in entity files — no deadline, no structured resolution, no Brier scoring. The loop is open.

**GPT's schema** (most concrete):
```sql
prediction(pred_id, entity_id, created_at, resolve_at, target, threshold,
           probability, rationale_ref, strategy, linked_signal_ids, status)
prediction_resolution(pred_id, resolved_at, outcome, realized_return, brier, notes_ref)
```

**Assessment**: This is ~2 days of work. Highest ROI item in the entire review. Blocks everything else (calibration, weight learning, post-mortems). Build first.

### 1.2 Surprise Detector + Autopsy Loop (Gemini R1, GPT R1, GPT R2)

**What**: Nightly script checks top movers in the universe. For each surprise (>15% move on high volume): did we predict it? If not, spawn a post-mortem: what datasets had precursor signals? Was entity resolution missing? Did a signal fire but not escalate?

**Why**: Constitution Principle says "every missed surprise becomes a rule." Currently NO architectural enforcement of this.

**Gemini's version** (most vivid): Agent gets spawned with: "Ticker XYZ moved 18% today. We missed it. Here's read-only DuckDB access. Find the leading indicator we ignored." If found, write a new signal rule and submit a PR.

**GPT's version** (most rigorous): Surprise triggers structured post-mortem template with pre-committed falsifiable causes (data error, timing, factor shock, thesis invalid). Any new rule must survive forward holdout.

**Assessment**: ~1 week including price data integration + template + PR workflow. Second-highest ROI.

### 1.3 Point-in-Time Discipline (GPT R2 — most critical red team finding)

**What**: Every record gets TWO timestamps: `event_date` and `first_seen_date`. Features for trading decisions MUST use `first_seen_date <= decision_time`. Raw data stored as immutable snapshots keyed by fetch time.

**Why**: FAERS has 6-month reporting lag. FPDS backfills. SEC XBRL gets restated. Without point-in-time discipline, backtests have phantom alpha from look-ahead bias. GPT rated this S:5 / D:5 (maximum severity, maximum stealth).

**Current intel state**: `download_*.py` scripts fetch current data. No `first_seen_date` tracking. Signal scanner uses whatever's in DuckDB. **This is a real vulnerability.**

**Assessment**: Retrofitting is expensive (~1-2 weeks for the infrastructure, ongoing for each dataset). But without it, any backtesting or weight learning is contaminated. Implement incrementally: start with new downloads, add `first_seen_date` column, log fetch timestamps.

### 1.4 Goodharted Learning Objective (GPT R2 §5.1 — challenges the generative principle itself)

**What**: "Correcting errors about the world measured by market feedback" conflates four things: (a) being right about fundamentals, (b) market timing, (c) factor moves, (d) sentiment. The system can learn to optimize for predictable short-term reactions rather than truth — becoming a noisy momentum/reversal trader without realizing it. S:5, D:4.

**Why this is Tier 1**: This isn't a bug in the system — it's a bug in the OBJECTIVE FUNCTION. If you close the feedback loop (Tier 1.1-1.3) naively, you risk learning market reflexes instead of fundamental truth.

**Defense (architectural)**:
- Define explicit **prediction targets AND horizons** per signal (5d reaction vs. 90d fundamental drift)
- Use **dual resolution criteria**: market return + subsequent fundamental confirmation (earnings revision, enforcement outcome, guidance change)
- Separate "truth learning" (did our thesis about the company prove correct?) from "trade timing" (did we capture the return?)

**Assessment**: This is a design decision, not a coding task. Must be resolved BEFORE implementing weight learning (Tier 2.1). Without it, the feedback loop optimizes the wrong thing.

### 1.5 Experiment Registry / Research Survivorship (GPT R2 §5.5)

**What**: Failed signals get quietly removed or redefined. The research record only shows survivors. System "improves" on paper while true discovery rate is low. S:5, D:5.

**Why this is Tier 1**: Same stealth profile as universe survivorship — invisible from within the system. If the AI agent tests 50 signal variants and only keeps the 3 that worked, that's classic p-hacking, regardless of intent.

**Defense**:
- Immutable **experiment registry**: every attempted signal gets logged with definition hash, dates tested, and results (including failures)
- Track a "research hit-rate" KPI: fraction of ideas that survive forward validation
- Git already provides immutability — enforce that signal definitions are never deleted, only deprecated with a reason

**Assessment**: Low effort (~1-2 days). The registry is just a JSONL file or DuckDB table. The discipline of logging failures is the hard part — needs a hook or template.

### 1.6 Quantitative Sanity Frame (GPT R2)

Three numbers that prevent self-deception. Should be hard-coded into the system:

1. **False discovery budget**: 50 signals × 100 entities × parameter space ≈ 5,000-50,000 implicit hypotheses/month. At 5% significance, expect 250-2,500 false positives. FDR control (Benjamini-Hochberg) is mandatory, not optional.

2. **Resolution rate constraint**: Concentrated portfolio generates ~10-30 resolved predictions/quarter. That is NOWHERE NEAR ENOUGH to update dozens of signal weights without overfitting. Cap weight updates per quarter. Use strong Bayesian priors.

3. **Liquidity constraint**: If position >20% of 20-day ADV, you cannot exit in stress without multi-% impact. Kelly must be capped by liquidity, not just by conviction.

**Assessment**: These aren't features to build — they're constraints to enforce. Print them on the wall. Hard-code the limits.

---

## TIER 2: High-Value Improvements — Should build in next phase

### 2.1 Signal Weight Learning from Outcomes (Gemini R1, GPT R1)

**What**: After predictions resolve, compute actual predictive power of each signal. Update Bayes weights from market outcomes, not developer intuition.

**Gemini**: "The math handles the fusion; the market tunes the weights."
**GPT**: Per-strategy calibration curves + isotonic calibration, updated monthly.

**Current intel**: `scoring.py` has LLR fusion with developer-set weights. Signal decay via exponential half-life. Weights are hypotheses but not empirically validated.

**Assessment**: Requires prediction ledger first (Tier 1.1). Also requires sufficient resolution data (GPT flags: concentrated portfolio = ~10-30 resolutions/quarter, "nowhere near enough" for aggressive weight updates). Use Bayesian shrinkage with strong priors, cap per-quarter weight changes.

**GPT R2 red team warning**: This is where overfitting enters. "The AI agent iterates: signal didn't work → tweak → re-test. Even without intent, the loop is hyperparameter search on historical sample." Defense: quarantine test set, experiment registry, forward holdout before production.

**Credit assignment problem** (GPT R2 §5.2, S:5): With a concentrated book, PnL is dominated by idiosyncratic jumps and factor shocks. Updating signal weights on raw trade outcomes = updating on noise. Defense: weight updates on **risk-adjusted residual returns** (strip factor/sector/beta), evaluate signal on idiosyncratic component only.

### 2.2 Universe Reconstitution Table (GPT R2)

**What**: `universe_membership(date, entity_id, in_universe, reason)` computed using only data available as-of that date. Every feature/backtest join must use this table.

**Why**: S:5 / D:5. Companies that fall below $500M (due to bad outcomes) get silently dropped from current-universe queries. Backtests learn from survivors. This inflates hit-rate for years.

**Current intel**: Watchlist is a static CSV (`thesis_universe.csv`, ~100 tickers). No point-in-time universe tracking.

**Assessment**: Medium effort (~3-5 days). Critical for any backtesting or weight learning. Without it, all historical evaluation is biased.

### 2.3 Base-Rate Store (GPT R1)

**What**: Explicit, queryable tables for base rates — sector norms, historical distributions, expected frequencies.

```sql
base_rate(metric_name, universe_def, lookback, value, computed_at, query_ref)
```

**Why**: Constitution Principle 4: "Quantify before narrating." Currently, base rates are computed ad-hoc in signal_scanner. Making them queryable means every signal output includes "how unusual is this vs. sector/universe?"

**Current intel**: Signal scanner computes PIT normalization (percentiles) and z-scores. This is similar but not stored persistently.

**Assessment**: Low effort (~2-3 days). Good foundation for signal learning.

### 2.4 Agent Task Queue (Opus R2)

**What**: SQLite-based task queue with dynamic priority function. Categories: crash_recovery > interrupt > signal_scan > prediction_resolve > entity_refresh > data_ingest > thesis_work > error_review > maintenance > exploration.

Priority modifiers: portfolio exposure (+500), entity staleness (+25/day), fired signal (+400), market hours proximity (+300), age bonus (prevents starvation).

**Why**: The constitution envisions autonomous multi-hour operation. Currently the agent has no task scheduler — it does whatever the human asks, or follows `.claude/agents/entity-refresher.md` protocol.

**Key design choice**: SQLite for queue (not DuckDB) — avoids file-locking conflicts with the analytical DB.

**Assessment**: ~3-5 days. Unlocks autonomous operation milestone from GOALS.md. The BOOT.md pattern (3000-token bootstrap → load context → read queue → execute) is sound and works within Claude Code's session model.

---

## TIER 3: Signal Discovery — Evaluate feasibility

These are Gemini R2's proposed non-obvious signals. Graded by my assessment of feasibility and novelty.

### 3.1 "Deferred Maintenance Cascade" — A-
EPA violations + OSHA inspections + court liens + SEC capex decline → predicts earnings miss.
**Feasibility**: Intel already has EPA ECHO, OSHA, SEC filings. Court docket data would be new. Entity resolution across these is the hard part.
**Novelty**: High. Most quants use OSHA/EPA for ESG scores, not as liquidity proxies.
**Action**: Wire existing EPA + OSHA data into signal_scanner as operational-quality composite.

### 3.2 "Brain Drain to Quality Collapse" — B+
H-1B transfers out + patent filing drop → predicts FDA Form 483 → drug pipeline risk.
**Feasibility**: Intel has DOL H-1B data. Would need USPTO patent assignments (public, downloadable). The join is novel.
**Novelty**: Very high. HR data → regulatory quality is a path nobody takes.
**Action**: Add USPTO patent data to download scripts. Test the H-1B → patent → 483 chain.

### 3.3 "Omission Alpha" (Silence as Signal) — A
Company drops a metric it always reported. Filing delay breaks historical pattern.
**Feasibility**: Intel already tracks insider filing delays. Extending to earnings call NLP would require transcript data (expensive or scraping).
**Novelty**: Medium-high. NLP sentiment is common; NLP *omission tracking* is rare.
**Action**: The filing-delay signal already exists in signal_scanner. Extend to track metric omissions in 10-K/10-Q structure (free via EDGAR XBRL tags — which facts were reported last year but not this year).

### 3.4 "Director Contagion" — B
Board member shared with sanctioned company → risk contagion.
**Feasibility**: Intel has SEC proxy/DEF-14A data and enforcement actions. Board member resolution is messy (person entity matching).
**Novelty**: High for small-caps. Citadel does this for mega-cap supply chains, not small-cap director networks.
**Action**: Build director graph from proxy statements. Cross-reference with enforcement actions.

### 3.5 "Kitchen Sink Turnaround" — A-
New CEO + spike in bad news + insider buying = BUY, not sell.
**Feasibility**: All data exists in intel (8-K CEO changes, CFPB/regulatory fines, Form 4 insider buys). This is a signal LOGIC change, not a data change.
**Novelty**: Very high. Reverses the naive interpretation of distress signals.
**Action**: Add CEO-change context to signal_scanner. When distress signals fire AND new CEO <6 months AND insider buying, flip signal direction.

### 3.6 "Unhedged Tariff Shock" — C+
UN Comtrade import data + tariff schedule changes → margin compression for specific mid-caps.
**Feasibility**: Intel has UN Comtrade. Tariff schedule data is public. The mapping to specific companies via 10-K segment reporting is the hard join.
**Novelty**: High but data-intensive. The company-specific mapping is where this lives or dies.
**Action**: Defer. High effort for uncertain payoff. Revisit when supply-chain signals are needed.

### 3.7 Alpha Decay Detector — A
Regress signal returns against factor ETFs. When proprietary signal correlates >0.8 with generic factor, alpha has decayed into beta.
**Feasibility**: Straightforward. Need daily factor returns (Fama-French freely available) + per-signal return attribution.
**Novelty**: Medium (standard quant practice) but currently absent from intel.
**Action**: Implement after prediction ledger. Requires signal-level return attribution.

---

## TIER 4: Red Team Defenses — Priority architectural safeguards

From GPT R2 (S = severity, D = detectability, both 1-5 scale, higher = worse):

| Failure Mode | S | D | Defense | Effort |
|---|---|---|---|---|
| Universe survivorship bias | 5 | 5 | Point-in-time universe table | 3-5 days |
| Look-ahead bias (reporting lags) | 5 | 5 | `first_seen_date` on all records | 1-2 weeks |
| Multiple comparison false discovery | 5 | 3-5 | FDR control (BH), research registry, forward holdout | 1 week |
| Liquidity-adjusted Kelly fallacy | 5 | 2-3 | ADV-based sizing cap, impact model, "can I exit in 3 days?" gate | 3-5 days |
| Latent-factor double counting | 5 | 4 | Signal covariance model, effective-bets constraint | 1-2 weeks |
| Delisting return omission | 5 | 4 | Survivor-bias-free price source or explicit delisting modeling | 1 week |
| Schema drift as false signal | 4 | 3 | Schema contracts, distribution drift monitoring (KL/PSI) | 3-5 days |
| Narrative post-mortem bias | 4 | 5 | Structured pre-committed cause checklist, forward holdout for new rules | 2-3 days |
| Credit assignment error | 5 | 4 | Risk-adjusted residual returns, Bayesian shrinkage | 1 week |
| Selective memory (research survivorship) | 5 | 5 | Immutable experiment registry, research hit-rate KPI | 1-2 days |
| Implicit sampling / partial refreshes | 4 | 5 | Deterministic replayable pipeline, lineage hashes | 1 week |
| Coverage bias ("clean" = "not in dataset") | 4 | 4 | Explicit eligibility maps per dataset per entity type | 2-3 days |
| Small-cap signal spoofing | 4 | 5 | Randomized execution timing, post-signal adverse selection monitoring | 2-3 days |
| Right-censoring (premature resolution) | 4 | 4 | Minimum resolution time per thesis type, survival-analysis framing | 2-3 days |

### Most dangerous (S5 × D5):
1. **Universe survivorship** — You can't detect this from within the system. Point-in-time universe table is mandatory.
2. **Reporting lag look-ahead** — Creates phantom alpha that looks real for years. `first_seen_date` is mandatory.
3. **Selective memory** — Failed signal hypotheses silently pruned. Immutable experiment registry is mandatory.

### Most actionable (high severity, low effort):
1. **Liquidity gate** — "Can I exit 20% of ADV in 3 days?" as a pre-trade check. ~1 day.
2. **Schema contracts** — Expected columns/types per dataset, pipeline fails on deviations. ~2-3 days.
3. **Structured post-mortem template** — Pre-committed cause checklist instead of open-ended narrative. ~1 day.

---

## TIER 5: Agent OS Design — Operational architecture

From Opus R2 (truncated but key patterns captured):

### BOOT.md Pattern — Adopt
3,000-token bootstrap file loaded at every session start. Steps: read clock → check crash recovery → load 4K-token context summary → read task queue → execute.

**Why it's good**: Solves the "fresh context per task" problem from the constitution. The agent doesn't need the full conversation history — it needs a compact state snapshot plus the next task.

### SQLite for Task Queue — Adopt
Not DuckDB. DuckDB has file-locking issues with concurrent access. SQLite handles single-writer gracefully. Task queue is OLTP, not OLAP.

### Context Budget Tracking
Opus proposed `estimated_tokens` per task + "if context usage > 70%, commit all work and EXIT cleanly." This prevents context degradation during long sessions.

### File-Based Locks
`.agent/locks/` directory with lock files for shared resources (DuckDB, entity files). Simple, visible, debuggable.

### Interrupt Pattern
`.agent/interrupts/` drop directory. When an 8-K fires for a portfolio company, a monitoring script drops a JSON file. The agent's next task selection picks it up with +5000 priority.

---

## TIER 6: From Existing Plans — Tactical items the clean-room missed

The clean-room models didn't know about the ~400 datasets, 295 DuckDB views, or current codebase. These items from MASTER_PLAN.md and REFACTORING_PLAN.md fill gaps the synthesis can't cover from first principles.

### 6.1 Dataset Registry + Health Events (MASTER_PLAN)

The synthesis has no dataset management layer. The MASTER_PLAN has a complete, cross-model-reviewed `dataset_registry` schema (46 columns: source, temporal, join routing, feed health, operational stats) plus an append-only `dataset_health_events` table. This is foundational infrastructure — the agent can't decide what to refresh, what's stale, or what's broken without it.

**Key additions over synthesis**: `schema_hash` for drift detection, `publication_lag_days` for PIT safety, `poll_endpoint`/`last_poll_status` for feed health, `join_keys` for entity resolution routing.

**Silence detection rules** (already battle-tested — scrapers already broke for OIG LEIE, DOL WHD, CMS): no new rows in 3× interval, schema hash changed, HTML tags in CSV, row count dropped >50%, all-null in previously-populated column. These block signal scanners from running on corrupted data.

**Assessment**: Build sequence Phase 0 should include this. The prediction ledger needs data flowing correctly first.

### 6.2 Issuer Crosswalk + 12 Identifier Namespaces (MASTER_PLAN)

The synthesis assumes entity resolution works. It doesn't yet. `issuer_xwalk(cik, ticker, cusip, ein, company_name, sic_code, start_date, end_date)` is the bridge from any government dataset to a tradeable security. Without it, every signal scanner needs its own ad-hoc ticker lookup.

The MASTER_PLAN documents 12 identifier namespaces (NPI, CIK, ticker, EIN, FIPS, CUSIP, UEI, NCT, plant_id, NAICS, CCN, ISO zone) with cast gotchas (VARCHAR vs BIGINT, leading zeros, strip dashes). This is hard-won operational knowledge.

**Assessment**: Build sequence Phase 0, alongside prediction ledger. Most scanners are blocked by this.

### 6.3 Graduated Autonomy Model (MASTER_PLAN)

The synthesis mentions Brier scoring for calibration but has no framework for WHEN the agent gets more autonomy. The MASTER_PLAN defines 4 levels:
- L0: Agent proposes, human executes everything (current)
- L1: Agent executes stop-losses/rebalancing (after 3 months paper trading)
- L2: Agent executes trades <$2K (after 6 months + positive returns + Brier <0.25)
- L3: Agent manages portfolio (after 12 months + consistent alpha + Brier <0.20)

"Autonomy never increases without demonstrated calibration. Bad predictions → autonomy ratchets back."

**Assessment**: This is the operational answer to the synthesis's Agent OS design (Tier 5). The task queue needs to know what the agent CAN do. Add to Phase 2 (Agent Autonomy) as a configuration.

### 6.4 Signal Evaluation Harness with Random Noise Control (MASTER_PLAN)

The synthesis mentions "forward holdout" but the MASTER_PLAN has a specific anti-look-ahead test: "Random signals through the harness must show ~0% edge, ~50% hit rate. If random noise shows alpha, the harness leaks future data." Also: incremental alpha over OAP's 209 academic factors (already downloaded, 2.4 GB). Signal kill-switch: flag for retirement if no edge after 6 months with <30 samples.

**Assessment**: Add to Phase 3 (Learning). The random noise test is the cheapest, most powerful sanity check for backtesting integrity.

### 6.5 Codebase Remediation Priorities (REFACTORING_PLAN)

The synthesis designs what to BUILD. The refactoring plan identifies what to FIX first:
1. **signal_scanner.py** (3,693 lines, zero tests) — generates trade signals. Silent `except` on every scan function. Highest risk.
2. **setup_duckdb.py** (4,146 lines) — the entire queryable surface. No subset rebuild. Schema contracts duplicated in healthcheck.py.
3. **test_lib.py** (552 lines) — homebrew test runner duplicating pytest. Migrate and delete.

The "MUST test" list: scoring.py (has tests), each scan_* function (zero tests), backtest inject_cutoff (4 tests on 3K lines), prediction_tracker Brier scoring (zero tests), paper_ledger P&L (zero tests).

**Assessment**: This is prerequisite work. Building new features on untested trade-influencing code compounds risk. Phase 0.5: scanner tests + test infrastructure before new feature development. Estimated 4-5 days. Not sexy, highest ROI for system reliability.

---

## WHAT TO SKIP (Convergent across all models)

All models agree — these are YAGNI:
- UI/dashboard (agent reads markdown)
- Streaming/real-time (daily batch is sufficient for small-cap alpha)
- Airflow/Prefect (cron + Python + make)
- Vector DB / RAG — Not just YAGNI but **principled** (Gemini R1): "Vector embeddings abstract away provenance and blur exact details." DuckDB FTS preserves exact facts with source pointers. RAG would violate Constitution Principle 7 (Honest About Provenance).
- Microservices / Kubernetes
- Graph database (DuckDB relational is sufficient)
- Deep learning / complex ML (simple models + base rates first)
- Generic feature store abstraction (DuckDB tables + views)

---

## CONCRETE TEMPLATES (Copy-pasteable from Opus R1)

The most immediately useful output from Opus was the exact YAML formats for the new first-class objects:

### Thesis Template
```yaml
thesis_id: "TICKER_signal_type_YYYYQN"
entity_id: "ENT_XXXX"
direction: long|short_watchlist
created: YYYY-MM-DD
deadline: YYYY-MM-DD
claim: "Falsifiable prediction statement"
evidence_for:
  - signal: signal_id
    value: 3.2  # z-score
    grade: "[DATA]"
    detail: "Human-readable explanation"
evidence_against:
  - "Counter-argument with base rate"
falsification: "Specific condition that kills this thesis"
predicted_outcome: "Stock does X within Y days"
confidence: 0.35
position: NONE|size
```

### Error Ledger Resolution Template
```yaml
thesis_id: "TICKER_signal_type_YYYYQN"
prediction: "What we predicted"
outcome: HIT|MISS|PARTIAL
actual_return: 0.188
timeframe_days: 45
confidence_at_entry: 0.45
post_mortem: |
  Structured analysis (not open narrative).
  Cause: [data_error|timing|factor_shock|thesis_invalid|signal_correct]
signal_updates:
  - signal_id: signal_name
    old_weight: 1.0
    new_weight: 1.3
    reason: "Evidence-based with n= and confidence"
```

### Portfolio State Template
```yaml
as_of: YYYY-MM-DD
cash_pct: 45
positions:
  - entity_id: ENT_XXXX
    ticker: XYZ
    thesis_id: "linked_thesis"
    kelly_fraction: 0.12
outbox:
  - action: BUY|SELL
    ticker: ABC
    thesis_id: "linked_thesis"
    rationale: "One-line with signal z-score"
    max_entry_price: 14.50
risk_check:
  max_single_position: 0.20    # HARD LIMIT
  current_max_position: 0.12
  drawdown_from_peak: -0.03    # breakers at -0.15, -0.25
```

---

## RECOMMENDED BUILD SEQUENCE

Based on dependency analysis across all outputs:

### Phase 0: Foundation (5-7 days)
- [ ] Scanner test coverage — test each `scan_*` function, add pre-commit gate (Tier 6.5)
- [ ] `dataset_registry` + `dataset_health_events` tables (Tier 6.1)
- [ ] Silence detection rules on top-10 feeds (Tier 6.1)
- [ ] `issuer_xwalk` from EDGAR Submissions Bulk ZIP (Tier 6.2)
- [ ] `prediction` table in DuckDB + YAML template (Tier 1.1)
- [ ] `prediction_resolution` table + Brier scoring script
- [ ] Trade outbox table (structured proposals)
- [ ] `first_seen_date` column on new downloads going forward (Tier 1.3)
- [ ] Experiment registry — JSONL log of every signal hypothesis tested (Tier 1.5)
- [ ] Resolve Goodhart defense: define dual resolution criteria (market return + fundamental confirmation) BEFORE building the learning loop (Tier 1.4)

### Phase 1: Close the Loop (1-2 weeks)
- [ ] Surprise detector (daily top movers vs. active predictions) (Tier 1.2)
- [ ] Post-mortem template (structured, pre-committed cause checklist — NOT open narrative)
- [ ] Point-in-time universe table (historical membership) (Tier 2.2)
- [ ] Liquidity gate: "can I exit 20% ADV in 3 days?" hard pre-trade check
- [ ] Schema contracts for top-10 datasets (expected columns/types, fail on deviation)
- [ ] Coverage eligibility maps: which entities should appear in which datasets

### Phase 2: Agent Autonomy (1-2 weeks)
- [ ] SQLite task queue + priority function (Tier 2.4)
- [ ] BOOT.md bootstrap sequence (Tier 5)
- [ ] Graduated autonomy levels as task queue config — L0→L3 with Brier-gated thresholds (Tier 6.3)
- [ ] Context summary generator (4K token snapshot)
- [ ] Recurring task generation (signal scan, prediction resolve, data refresh)
- [ ] `.agent/interrupts/` pattern for 8-K/urgent events
- [ ] Context budget tracking: estimated_tokens per task, exit at 70% usage

### Phase 3: Learning (2-4 weeks, needs Phase 0 resolution data)
- [ ] Signal evaluation harness with random noise control — random signals must show ~0% edge (Tier 6.4)
- [ ] Incremental alpha test: does signal add value over OAP's 209 academic factors? (Tier 6.4)
- [ ] Signal kill-switch: retire if no edge after 6 months/<30 samples (Tier 6.4)
- [ ] Signal weight learning — ON RISK-ADJUSTED RESIDUAL RETURNS, not raw PnL (credit assignment fix)
- [ ] Bayesian shrinkage with strong priors, capped per-quarter weight changes (sanity frame: ~10-30 resolutions/quarter is not enough for aggressive updates)
- [ ] Base-rate store (persistent, queryable) (Tier 2.3)
- [ ] Calibration curve tracking (Brier per strategy)
- [ ] Alpha decay detector (factor correlation monitoring) (Tier 3.7)
- [ ] FDR control (Benjamini-Hochberg) for multiple comparison correction
- [ ] Research hit-rate KPI: fraction of signal hypotheses that survive forward validation

### Phase 4: Signal Expansion
- [ ] "Omission Alpha" — XBRL fact presence/absence tracking (Tier 3.3)
- [ ] "Kitchen Sink Turnaround" — CEO-change + distress + insider buy flip (Tier 3.5)
- [ ] "Deferred Maintenance Cascade" — EPA + OSHA composite (Tier 3.1)
- [ ] Director contagion graph from proxy statements (Tier 3.4)
- [ ] H-1B + patent pipeline signal (Tier 3.2)

---

## MODEL PERFORMANCE NOTES

**GPT-5.2**: Strongest output overall. The red team analysis is the single most valuable piece across all 6 outputs — specific, quantitative, actionable. Architecture design (R1) was thorough but conventional. Best at: adversarial analysis, structured enumeration, defense proposals.

**Gemini 3.1 Pro**: Most creative. "Kitchen Sink Turnaround" and "Deferred Maintenance Cascade" are genuinely novel signal ideas. Architecture design (R1) was the most concise and opinionated ("MVFL" concept). Weakest at: operational detail, code-level specificity. Best at: abstract pattern recognition, cross-domain connections.

**Claude Opus 4.6**: Best at framing ("conjecture-refutation machine", "agent IS the reasoning layer"). The agent OS design (R2) was the most operationally concrete — actual schemas, actual code, actual priority functions. Truncated both times (~10K token outputs). Best at: operational architecture, agent-native design, pragmatic code.

**Hallucination check**: No factual claims to verify (clean-room design, not fact-retrieval). GPT's red team used standard quant concepts (Lopez de Prado, Benjamini-Hochberg, fractional Kelly) correctly. Gemini's signal ideas are mechanistically plausible but untested — treat as hypotheses, not validated signals.
# Cross-Model Review Synthesis: Selve → Selve + Genomics Split

**Mode:** Review (critical)
**Date:** 2026-02-28
**Models:** Gemini 3.1 Pro, GPT-5.2
**Constitutional anchoring:** Yes (CONSTITUTION.md, GOALS.md)

---

## Fact-Check Results

### What both models got wrong about data coupling

Both models assumed `data/` is git-tracked shared mutable state. **It's not.** `data/` is in `.gitignore` (0 files tracked). Raw genomics data lives on external volumes via symlinks. The coupling is **filesystem-level** (paths in configs/scripts), not **git-level**.

### PHI scope is docs, not blobs

The actual PHI in git history is **20+ markdown docs** in `docs/` (health summaries, WGS reports, medical contacts, omics outreach emails). Binary data (CRAM, VCF) was never committed. This means:
- PII scrubbing is scoped to text files in `docs/`, not multi-GB binary blobs
- `git-filter-repo` runs much faster on text paths than Gemini/GPT implied
- Repo size isn't inflated by binary PHI (their "technical necessity" concern is moot)

### Gemini's dismissal of cross-project genomics queries — partially wrong

Gemini said "N=1 PGx data has zero statistical base-rate value for biotech DD." But Gemini then self-corrected: if genomics MCP queries **reference databases** (PharmGKB, ClinVar, gnomAD constraint scores) rather than personal variants, the cross-project value is real. This is the likely use case — drug target validation via curated biomedical DBs, not personal VCF lookups.

### GPT's coupling tightness scores — somewhat pessimistic

GPT scored `data/` at tightness 5. Since `data/` isn't in git, the coupling is "where does genomics write results and how does selve find them" — a **path configuration** issue (tightness 2-3 with absolute paths or env vars), not shared mutable state.

---

## Verified Findings (adopt)

| Finding | Source | Verified How |
|---------|--------|-------------|
| PHI docs (20+) in git history need scrubbing | Both | `git ls-files docs/` confirmed personal health files tracked |
| `data/` not in git, coupling is filesystem paths only | Fact-check | `git ls-files data/` = 0 files, `.gitignore` confirmed |
| Hooks need per-repo split (data guard conflicts with genomics writes) | Gemini | `settings.json` PreToolUse blocks `data/` writes; genomics scripts write to `data/wgs/` |
| PII scrub should happen BEFORE split (splitting copies the problem) | GPT | Logically sound — filter-repo on one repo easier than two |
| Export contract needed for clean seam (manifest + versioned artifacts) | GPT | Without it, selve relies on implicit path knowledge of genomics output structure |
| agent_coord.py needs interface refactor | Both | SessionStart hook hardcodes selve-local agent_coord.py |
| 116 genomics scripts have git history worth preserving | Fact-check | `git ls-files scripts/genomics/ \| wc -l` = 116 |

## Where I Was Wrong

| My Original Claim | Reality | Who Caught It |
|-------------------|---------|--------------|
| "Integration seam is clean" | Seam is at filesystem path level (medium coupling), not git/code level. Cleaner than models claimed, but needs explicit export contract | Both (overstated), fact-check (calibrated) |
| Cross-project PGx query for biotech DD | As personal N=1 variants: low value. As reference DB queries: real value | Gemini (then self-corrected) |

## Gemini Errors

| Claim | Why Wrong |
|-------|-----------|
| "data/ is shared mutable state [tightness 5]" | data/ is gitignored, not tracked. Coupling is path-level, not state-level |
| "Git filter-repo will rewrite entire repository SHAs" | True, but scope is limited to docs/ text files, not massive binary blobs. The concern about repo size degradation doesn't apply |
| "neurokit2 and oura-ring might need cross-pollination with variant curation" | Plausible but speculative — no evidence of current cross-usage |

## GPT Errors

| Claim | Why Wrong |
|-------|-----------|
| "PII scrubbing: 16-40 hrs" | Likely 4-8 hrs given scope is ~20 markdown files, not binary blobs. git-filter-repo with path list is fast |
| "Shared data/ is tightness 5" | Tightness 2-3 (path config), not 5 (shared mutable state) |
| "Commit-based triggers: tightness 4" | No evidence selve indexes based on git commits from genomics |

---

## Revised Recommendations (priority order)

### 1. PII scrub first (before split)
- Scope: 20+ docs in `docs/personal_*`, `docs/HEALTH_*`, `docs/brain_*`, `docs/hifi_*`, `docs/handoffs/personal_*`
- Tool: `git-filter-repo --path docs/personal_wgs_report.md --path docs/HEALTH_AND_GENOMICS_SUMMARY.md ...`
- Either delete from all history OR move to a never-committed location
- Estimated effort: 4-8 hrs (including verification)
- **Do this in the current monorepo before splitting**

### 2. Define export interface
- Genomics writes results to a known location (already `/data/wgs/analysis/` or external volume)
- Create a simple manifest: `genomics_export.json` listing available result sets + paths
- Selve indexes from the manifest, not from implicit path knowledge
- This is what makes the "clean seam" actually clean

### 3. Split repos via git-filter-repo
- Extract `scripts/genomics/` with history into new `genomics` repo
- Move genomics-specific docs (20+ files) to genomics repo
- Leave selve with search engine + personal knowledge sources
- Skills: genomics-pipeline, genomics-status, annotsv, clinpgx-database, gget, vcfexpress → genomics repo
- Skills: modal → probably genomics (primary consumer), but could be shared
- Rules: epistemics.md → shared (used by both domains)

### 4. Create genomics MCP
- Typed query interface: `get_variant()`, `get_prs()`, `pipeline_status()`, `query_pharmgkb()`, `query_clinvar()`
- Exposes reference DB queries (high cross-project value)
- Exposes pipeline status and results (high within-project value)
- Personal variant data: available but clearly labeled as N=1

### 5. Refactor hooks per repo
- Genomics: remove data/ write guard, keep ruff-format, add Modal-specific guards
- Selve: keep data/ write guard, keep research gate, remove genomics-specific stop hook logic
- Both: keep bare python guard (shared pattern)

### 6. Update orchestrator references
- `autonomous-agent-architecture.md`: "self" → "genomics" for Loops 1,2,6,7
- `agent_coord.py`: dispatch to `~/Projects/genomics/` for pipeline tasks
- Loops 3,4,5 (phenotype investigation, multi-model review, N=1 experiments) may span both repos — orchestrator needs multi-repo dispatch

---

## Constitutional Alignment Assessment

| Principle | Impact of split |
|-----------|----------------|
| #1 Autonomous Decision Test | **Positive** — leaner context per session, faster decisions |
| #5 Fast Feedback | **Positive** — search and pipeline operate at their natural speeds |
| #6 The Join Is The Moat | **Neutral if export contract exists** — one graph via manifest-based integration. **Negative if ad-hoc** — knowledge silos |
| #10 Compound, Don't Start Over | **Positive if history preserved** — git-filter-repo keeps commit history. **Negative if fresh repo** — loses institutional memory |

---

## Sequencing

1. PII scrub (selve monorepo)
2. Define export contract (manifest spec)
3. git-filter-repo to extract genomics with history
4. Set up genomics repo (CLAUDE.md, skills, hooks, MCP)
5. Update selve (remove genomics paths, update CLAUDE.md, update hooks)
6. Build genomics MCP server
7. Update orchestrator/meta docs
8. Verify: selve indexes genomics results via manifest, cross-project queries work
# Cross-Model Review: Evo → Intel Infrastructure Transfer

**Mode:** Review
**Date:** 2026-03-01
**Models:** Gemini 3.1 Pro, GPT-5.2
**Constitutional anchoring:** Yes (Meta CLAUDE.md constitution, Intel constitution, Meta GOALS.md)
**Extraction:** 56 items extracted, 39 included, 3 deferred, 1 rejected, 4 merged

---

## Where I (Claude) Was Wrong

| My Original Claim | Reality | Who Caught It |
|-------------------|---------|--------------|
| "Intel has zero introspection tooling" | Intel has `tools/evals/smoke_queries.py` with `--quick` and `--domain` flags | Fact-check |
| "Lessons scattered in narrative memory only" for Admiralty | `tools/lib/admiralty.py` already exists as structured Python — per-dataset, per-column, per-inference grades | Fact-check (G5 rejected) |
| "backtest.py at 109K" (implied LOC) | 109K bytes = 3,037 lines. Both models accepted uncritically. | Fact-check (FC1) |
| Architecture analysis should map Python scripts | Complexity lives in SQL layer (295 views, 610 datasets), not Python call graphs (G1, both models) | Gemini + GPT |
| Event sourcing ledger as medium-leverage transfer | Anti-pattern for 525GB bulk ingestion; data contract verification is the right analog (G2, G13, P1) | Both models |
| Analysis was "too generic software engineering" | Neglected intel-specific value: entity resolution quality, join integrity, backtest reproducibility (G21, P18-P21) | Both models |

## Gemini Errors (distrust)

| Claim | Why Wrong |
|-------|-----------|
| G5: "Admiralty grading is in narrative memory" | Already structured code in `tools/lib/admiralty.py` |
| G9: `duckdb_dependencies()` as easy DAG source | Function exists but may not track through complex CTEs/macros — Gemini flagged this itself (G24) |
| Temperature override note: Gemini's `-t 0.3` was ignored (locked at 1.0 for thinking model) | Output quality unaffected |

## GPT Errors (distrust)

| Claim | Why Wrong |
|-------|-----------|
| Accepted "109K" backtest.py without questioning | File is 3,037 lines (109K bytes). Should have asked for clarification. |
| P27: Effort estimates (40-90h for task runner, 120-300h for specs) | Likely inflated for a solo-dev + agent workflow. Task runner is ~4-8h, not 40-90h. Specs depends on scope. |
| P18-P21: Constitutional coverage percentages | Precise numbers with no measurement methodology — confident fabrication pattern. Directional assessment is useful, absolute scores are not. |

---

## Revised Priority List (Post-Review)

### Tier 1: High leverage, directly serves intel's error-correction mission

**1. DuckDB View Lineage DAG** (G1, G9, G15)
- Build `tools/arch/view_lineage.py` using DuckDB's `duckdb_dependencies()` or SQL parsing
- Output: `views_dag.json` + visualization
- Gate: pre-commit hook rejects view changes that break downstream
- Risk: dynamic SQL may defeat static analysis (G24, P2). Start with what `duckdb_dependencies()` gives, supplement with grep-based parsing.
- Verification: identifies ≥15% orphaned views; top 5 hotspots cover ≥50% of incident touchpoints (P12)

**2. Join-Quality SLOs** (P22, G4, P3)
- Cardinality monitors on canonical joins: null-rate, duplication, pre/post row counts, many-to-many detection
- Time leakage checks for backtests (feature timestamp must precede label timestamp)
- This is the "spec-as-database" pattern applied to where intel's actual risk lives: *semantic join correctness*, not schema types
- Verification: ≥30% reduction in silent data errors caught late (P22)

**3. Backtest Reproducibility Harness** (P23)
- Golden runs: frozen datasets + parameter sets, checksum outputs
- Regression detection on every material change to backtest infrastructure
- Verification: "backtest changed unexpectedly" incidents down ≥40% over 2 months

### Tier 2: High leverage, infrastructure improvement

**4. Task Registry** (G3, G8, P6, P11)
- Start with a simple `tasks.toml` or `Makefile` mapping the top 30 scripts by usage
- Include: script, required deps, expected inputs/outputs, DuckDB tables touched
- Later: expose via MCP for agent autonomy (G7) — but validate simple version first (G25)
- Add env pinning (P6): Python deps via `uv`, DuckDB version
- Verification: ≥70% recurring ops via runner within 4 weeks (P11)

**5. Structured Failure Modes → Thesis-Check Integration** (G11, G16, P7, P14)
- Consolidate `memory/analytical_reasoning.md`, `docs/download_agent_lessons.md`, CLAUDE.md `<gotchas>` into `resources/failure_modes.json`
- Wire into `thesis-check` skill: agent queries failure DB before generating hypothesis
- CRITICAL: must have ingestion mechanism (P7) — each incident produces an entry, or it becomes stale docs
- Verification: top 10 failure modes have linked tests; recurrence ≤1/month (P14)

**6. Multi-Tier Testing with Gates** (G12, G19, P8, P15)
- Acknowledge: `tools/evals/smoke_queries.py` and 24 test files already exist
- Formalize: `bb test:smoke` (<30s, view compilation + basic smoke queries), `bb test:integrity` (<2min, entity graph checks, join cardinality), `bb test:backtest` (minutes, golden run regression)
- Enforce: smoke tier runs on every commit; integrity on every data rebuild
- Verification: regressions down ≥25%, MTTR down ≥20% (P15)

### Tier 3: Medium leverage, worth doing when Tier 1-2 are stable

**7. ER Evaluation Bench** (P24)
- Labeled benchmark set for entity resolution precision/recall/F1
- Canary entities with known ground truth
- Weekly tracking
- Verification: ER F1 tracked; "wrong entity" incidents down ≥30%

**8. Provenance Enforcement at Output** (P25)
- Strict schema for signals/claims: value, entity_id, asof_ts, provenance label, source_uri, NATO grade, pipeline_run_id
- Reject outputs missing fields
- Verification: ≥95% outputs pass provenance gate; supervision waste from 21% → ≤15%

**9. Falsification Scaffolding** (G6)
- Standard API to inject null models/randomized data into backtests
- Pre-trade falsification checklist
- Serves Principle 11 directly

**10. Operational Telemetry** (P26, G20)
- Structured logs: job_id, inputs, outputs, runtime, row counts, failure class
- DORA-style dashboards: MTTD, MTTR, change-failure rate
- Serves Meta "measure before enforcing" — need baseline data before adding more gates
- Verification: MTTR down ≥25%, ≥80% failures auto-classified

### Deferred / Rejected

| Item | Status | Reason |
|------|--------|--------|
| Event sourcing ledger (broad) | DEFER | Anti-pattern for bulk data (G2, G13, P1). If scoped to entity mutations only, reconsider as part of #7 ER Bench |
| Three-primitive kernel | REJECT | Category error from UI to research (P5). Intel's operations are too heterogeneous. |
| Documentation landing page | DEFER | Low leverage (P10). CLAUDE.md `<reference>` section partially serves this role |
| Dry-run extension beyond setup_duckdb.py | DEFER | setup_duckdb.py already has --dry-run. Extend to build_entity_tables.py when warranted |
| Code-level arch analysis (Python call graphs) | DEFER | Low leverage vs. view DAG. Reconsider if agent code navigation proves to be the bottleneck (G26) |

---

## Constitutional Gaps Identified

The strongest critique from both models: my original analysis was **generic software engineering** that neglected intel's domain-specific constitutional principles. The revised priority list addresses:

- **"The Join Is the Moat"** → #2 Join-Quality SLOs, #7 ER Bench (was barely touched in original)
- **"Falsify Before Recommending"** → #9 Falsification Scaffolding, #3 Backtest Reproducibility (absent from original)
- **"Portfolio Is the Scorecard"** → Still underserved. None of the proposals directly integrate portfolio performance as an integration test. (P20: 20% coverage)
- **"Size by Fractional Kelly"** → Still underserved. No sizing engine integration. (P21: 15% coverage)
- **"Fast Feedback"** → Well-served by task runner + testing tiers + dry-run

The two lowest-scored principles (Portfolio as Scorecard, Fractional Kelly) require *application-level* work, not infrastructure patterns. They're out of scope for an infra transfer analysis.

---

## Key Takeaway

The original evo→intel analysis was useful as a starting point but treated intel as a generic codebase. The cross-model review correctly identified that intel's highest-leverage improvements are **domain-specific**: join integrity, backtest reproducibility, entity resolution quality. The evo patterns (specs-as-data, testing tiers, task runner) are valid *mechanisms* but must be applied to intel's actual error surfaces — which are semantic and data-level, not code-level.
# Cross-Model Review: Overview Trigger Mechanism

**Mode:** Review (critical)
**Date:** 2026-03-01
**Models:** Gemini 3.1 Pro, GPT-5.2
**Constitutional anchoring:** Yes (CLAUDE.md Constitution + GOALS.md)
**Extraction:** 22 items extracted, 17 included, 2 deferred, 1 rejected, 2 merged

## Verified Findings (adopt)

| ID | Finding | Source | Verified How |
|----|---------|--------|-------------|
| G1, P1, P2 | LOC is a bad proxy for arch significance | Both | Obviously true — 1-line schema change vs 500-line formatting |
| G3, P5, P10 | Per-overview-type triggering needed | Both | 1 trigger = 3 overviews is a 3x cost multiplier for no reason |
| G4, P8, P15 | Measure before deploying thresholds | Both | Constitutional: "Log every hook trigger to measure false positives" |
| G6 | Path-based scoping via git diff --name-only | Gemini | Deterministic, zero-cost, enables per-overview routing |
| G8 | Shadow mode first (log decisions, don't generate) | Gemini | Best path to constitutional compliance |
| P9 | Composite trigger: structural signals + LOC | GPT | Fixes core gap — renames, file adds are low-LOC high-impact |
| P11 | Preview gate: skip test/docs/formatting | GPT | Low-cost FP reduction |
| P12 | Time decay via cron, not SessionEnd | GPT | Solves genomics bursty-quiet pattern |
| P14 | Testable metrics spec for logging | GPT | Implementation spec for measurement phase |

## Deferred (with reason)

| ID | Finding | Why Deferred |
|----|---------|-------------|
| G5 | LLM router (Flash as semantic judge) | Flash sycophancy risk (G11). Adds LLM dependency to trigger. Only evaluate if deterministic signals prove insufficient after logging phase |
| G7 | AST/structural diffing (difftastic) | Tool dependency. Evaluate if LOC + structural signals insufficient |

## Rejected (with reason)

| ID | Finding | Why Rejected |
|----|---------|-------------|
| G10 | Drop time decay entirely | GPT's cron point (P12) is stronger — bursty projects (genomics: weeks quiet, then burst) need a staleness cap. Without it, overview stays stale forever during quiet periods after a burst |

## Where I Was Wrong

| My Original Claim | Reality | Who Caught It |
|-------------------|---------|--------------|
| "Lines-changed threshold is the sweet spot" | LOC is a broken proxy — misses renames, config, and feature flags; over-triggers on formatting | Both models |
| "Time decay via SessionEnd" | SessionEnd doesn't fire during quiet periods — need cron for actual guarantee | GPT |
| "One trigger fires all 3 overviews" | Per-overview scoping cuts cost 2-3x with zero staleness penalty | Both models |
| "50 lines is a reasonable threshold" | Magic number without data violates "measure before enforcing" | Both models |

## Gemini Errors (distrust)

| Claim | Assessment |
|-------|-----------|
| "Drop time decay entirely" | Wrong — ignores the quiet-after-burst case. Gemini's reasoning ("if untouched, architecture unchanged") is circular: the burst may have changed architecture, and no sessions fire to trigger detection |
| Flash LLM router recommendation | Interesting but premature — adds complexity and LLM dependency. The sycophancy risk Gemini self-flagged is real |

## GPT Errors (distrust)

| Claim | Assessment |
|-------|-----------|
| Quantitative cost-benefit numbers | All synthetic — acknowledged. Framework is sound but specific numbers ($0.197/wk etc.) are fabricated. Don't use for threshold selection |
| "Material change rate" estimates per project | Guessed from qualitative descriptions. Need actual logs |

---

## Revised Recommendation

### Architecture: Two-Stage Deterministic Trigger

**Stage 1: Route (free, instant)**
```
git diff --name-only <marker>..HEAD
  → classify each file into overview scope:
    - src/**          → SOURCE_ARCH
    - scripts/*, hooks/*, *rc, bb.edn, *.config.* → DEV_TOOLING
    - file adds/deletes/renames (any scope)        → PROJECT_STRUCTURE
    - test/*, *_test.*, docs/*, *.md               → SKIP (no overview impact)
```

**Stage 2: Per-scope composite trigger**
For each scope that has changes:
```
REGENERATE if ANY of:
  - files_added + files_deleted + renames >= 1  (structural change)
  - dependency/config file touched               (tooling change)
  - LOC_changed > T                              (volume threshold, TBD from data)
```

**Stage 3: Execute**
- Generate ONLY the overview types whose scope was triggered
- Background, async, non-blocking (nohup from SessionEnd)
- Use Flash model (cheap/fast), not Pro

**Staleness safety net:**
- Daily cron (or orchestrator tick): check each repo for changes since last overview > 7 days
- If stale + any changes exist → regenerate in background

### Implementation Order

1. **Shadow mode (week 1-2):** Log trigger decisions to JSONL without generating. Metrics per P14: repo, timestamp, diff_lines, diff_files, diff_renames, paths_hit, which_overviews_would_fire. This satisfies constitutional "measure before enforcing."

2. **Tune thresholds (end of week 2):** Plot FPR/FNR vs LOC threshold. Pick Pareto point. Validate structural signals (renames, adds) catch the surgical-change cases.

3. **Enable generation (week 3+):** Switch from logging to actual generation. Per-overview-type. Flash model.

4. **Evaluate LLM router (future):** Only if deterministic signals show persistent FP/FN gaps that LOC + structural signals can't fix.

### Key Design Decisions

- **No LLM in the trigger path** (for now). Deterministic signals are cheaper, faster, more predictable. LLM router deferred until data shows it's needed.
- **Per-overview scoping is the single biggest win.** Both models independently identified this. Cuts generation cost 2-3x with zero staleness penalty.
- **Measurement first is constitutionally required.** The 50-line threshold was a guess. 2 weeks of logging will produce the actual number.
- **Cron for staleness, not SessionEnd.** SessionEnd only fires when sessions happen. Quiet projects (genomics) need an independent check.
---
name: researcher
description: Autonomous research agent that orchestrates all available MCP tools with epistemic rigor. Use when the user needs deep research, literature review, evidence synthesis, or any investigation requiring multiple sources. Effort-adaptive (quick/standard/deep), anti-fabrication safeguards built in.
argument-hint: [research question or topic]
hooks:
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: prompt
          prompt: "The researcher just wrote or edited a file. Check: does every factual claim in the written content have a source citation in brackets (e.g., [DATA], [A2], [Exa], [S2], [PubMed], [arXiv])? Return ok=false listing any unsourced factual assertions. Ignore formatting, headers, and instructions — only check empirical claims."
---

# Researcher

## Current Environment
`!echo "Date: $(date +%Y-%m-%d) | Project: $(basename $PWD) | MCP servers: $(claude mcp list 2>/dev/null | wc -l | tr -d ' ')"`

Research with the rigor of an investigative journalist, not a search engine. Every claim needs provenance. Inference is fine — but say it's inference, not fact.

**Invoke companion skills if relevant:**
- **`epistemics`** — if the question touches bio/medical/scientific claims
- **`source-grading`** — if this is an investigation/OSINT context (use Admiralty grades)

**Project-specific tool routing and gotchas are in `.claude/rules/research-depth.md`** (if it exists). Check it before starting.

<tool_reference>
## Available Research Tools

Use whichever of these are available in the current project's `.mcp.json`:

| Tool | What it does | When to use |
|------|-------------|-------------|
| `mcp__selve__search` | Personal knowledge search | Prior work, conversations, notes — **always check first** if available |
| `mcp__duckdb__execute_query` | Query project DuckDB views | Local data — check before going external |
| `mcp__intelligence__*` | Entity resolution, dossiers, screening | Investigation targets (if configured) |
| `mcp__research__search_papers` | Semantic Scholar search | Finding papers. **No date filtering** — use Exa for recency |
| `mcp__research__save_paper` | Save paper to local corpus | After finding useful paper |
| `mcp__research__fetch_paper` | Download PDF + extract text | **Before citing any paper** |
| `mcp__research__read_paper` | Get full extracted text | Reading a fetched paper |
| `mcp__research__ask_papers` | Query across papers (Gemini 1M) | Synthesizing multiple papers |
| `mcp__research__list_corpus` | List saved papers | Check before searching externally |
| `mcp__research__export_for_selve` | Export for knowledge embedding | End of session, persist findings (if configured) |
| `mcp__paper-search__search_arxiv` | arXiv search | Preprints — flag as `[PREPRINT]` |
| `mcp__paper-search__search_pubmed` | PubMed search | Clinical/medical literature |
| `mcp__paper-search__search_biorxiv` | bioRxiv/medRxiv search | Biology/medical preprints |
| `mcp__exa__web_search_exa` | Semantic web search | Non-obvious connections, expert blogs, recent work |
| `mcp__exa__company_research_exa` | Company intelligence | Business/financial research |
| `mcp__exa__get_code_context_exa` | Code/docs search | Technical implementation |
| `mcp__context7__*` | Library documentation | API/framework questions |
| WebFetch | Fetch specific URLs | Known databases, filings, regulatory |
| WebSearch | General web search | News, grey literature |

Not all tools exist in every project. Use what's available. The agent will error on tools not in `.mcp.json` — just skip them.

**Critical rule:** `fetch_paper` then `read_paper` BEFORE citing. Abstracts are not primary sources.

**S2 gotcha:** No date filtering on free tier. ~100 req/5min rate limit. Use Exa for "recent papers on X."
</tool_reference>

## Effort Classification

Before doing anything, classify the question:

| Tier | Signals | Axes | Output |
|------|---------|------|--------|
| **Quick** | Factual lookup, single claim | 1 | Inline answer with source |
| **Standard** | Topic review, comparison, "what do we know?" | 2 | Research memo with claims table |
| **Deep** | Literature review, novel question, "investigate X" | 3+ | Full report with disconfirmation + search log |

User can override with `--quick` or `--deep`. Announce the tier before starting.

## Domain Profiles

Classify the question's domain before starting. Domain-specific gotchas (non-obvious mistakes per field) are in **`DOMAINS.md`** alongside this skill. Read it when the domain applies.

If a question spans domains, name the primary and secondary. Use the stricter evidence standard. Project-specific routing (which DuckDB views, which databases) lives in `.claude/rules/research-depth.md`.

## Phase 1 — Ground Truth (always first)

Before any external search, check what exists locally:

1. **Personal knowledge** — `selve` MCP search if available, or local docs
2. **Project data** — DuckDB queries, local analysis files, entity docs
3. **Research corpus** — `list_corpus` for previously saved papers
4. **Training data** — what you know (label `[TRAINING-DATA]`)

Output: "What I already know" inventory. Flag contradictions with later findings.
**Quick tier:** If ground truth answers the question, stop here.

## Phase 2 — Exploratory Divergence

**Mandatory:** Name 2+ independent search axes before searching. Different axes reach different literatures.

Example axes:
- **Academic-anchored:** concept → literature → state of the art
- **Mechanism-anchored:** pathway → modulators → evidence
- **Investigation-anchored:** entity → enforcement → patterns
- **Population-anchored:** comparable cases → what happened
- **Application-anchored:** use case → implementations → lessons
- **Genotype-anchored:** variant → mechanism → intervention (genomics)
- **Guideline-anchored:** clinical guidelines → standard of care (medical)

If your axes all start from the same place, you have one axis with multiple queries.

**Search strategy per axis:**
- Minimum 3 query formulations (vary semantic vs keyword)
- Use different tools per axis when possible
- Scan titles/abstracts from 15+ sources before forming hypotheses
- **Save papers** with `save_paper`, **fetch full text** before citing

**Exa search philosophy (semantic search, not keyword):**
- **Match recency filter to field velocity.** Before searching, judge how fast the field moves and filter accordingly. Stable fields (physics, law) need no date gate. Fast fields (AI, crypto, geopolitics) go stale in months — if results reference superseded models, outdated benchmarks, or pre-current-generation tools, discard and re-query with tighter dates. Use `web_search_advanced_exa` date ranges when available, or add year terms to queries.
- Exa matches by meaning, not keywords. Query by phrase — describe the *concept* you want results from, not the terms you'd grep for. "Gene-diet interaction abolishing cardiovascular genetic risk" finds different (better) results than "9p21 diet interaction."
- **Seek insight from adjacent domains.** The most useful context often isn't phrased the same way or even from the same field. Ask: "What knowledge space would contain a brilliant critique of this idea?" Then phrase the query *from that domain's perspective*.
- **Know when to use your own knowledge vs. search.** Your training data is a massive library with a hard expiration date. Use it deliberately:
  - **Trust pre-training for:** foundational concepts, mathematical relationships, well-established science, historical facts, stable APIs, canonical papers (the *existence* and *core claims* of Shannon 1948 won't change).
  - **Verify via search for:** numbers that update (market caps, benchmarks, model rankings, statistics), claims about what's "state of the art," anything where the landscape shifted since your cutoff, named entities' current status.
  - **Assume stale for:** model comparisons, leaderboard positions, library versions, company valuations, anything where "latest" or "best" matters. Your training snapshot is months old — in fast fields that's a different era.
  - **Always tag it:** use `[TRAINING-DATA]` when relying on pre-training knowledge so the reader knows the provenance. This isn't a formality — it's how you distinguish "I retrieved this" from "I remember this."
  - **The dangerous zone:** you *feel* confident about a specific number, author name, or benchmark result from training. That feeling is the fabrication trigger. The more specific and numeric a memory feels, the more likely it's reconstructed, not recalled. Verify or hedge.
- **Sequential exploration, not shotgun.** Don't fire 10 Exa queries in parallel and flood the context window with noise. Instead: 3 targeted queries → scan summaries → identify which direction has signal → 3 more queries doubling down on the most promising vein. This is an affinity tree, not a broadcast. **Measured: 51% of research sessions violate this** by firing 3-8 simultaneous queries (session audit, 2026-02-28). Query at position 3 in a burst cannot incorporate what query 1 returned. The instruction exists because it's a real failure mode, not a style preference.
- **Use Exa's `summary` and `highlights` fields** to scan results before pulling full text. Set `maxCharacters` on `text` to limit per-result context. The best sources are usually papers, blog posts, essays, and threads — not marketing pages.
- **First results may be SEO noise.** Don't stop at the top 3 — scan 8-10 results at summary level, then read the 2-3 that actually have signal.

**Quick:** 1 axis, 1-2 queries. **Standard:** 2 axes, 5+ queries. **Deep:** 3+ axes, 10+ queries.

## Phase 3 — Hypothesis Formation (Standard + Deep)

From Phase 2 findings, form 2-3 testable hypotheses as falsifiable claims:
- "If X is true, we should see Y in the data/literature."
- "If X is false, we should see Z."

## Phase 4 — Disconfirmation (Standard + Deep)

For EACH hypothesis, actively search for contradictory evidence:
- "X does not work", "X failed", "X criticism", "X negative results"
- "no association between X and Y", "X limitations"
- Check single lab/group vs independent replication

If no contradictory evidence after genuine effort: "no contradictory evidence found" (≠ "none exists").
**This phase is structurally required.** Output without disconfirmation is incomplete.

## Phase 5 — Claim-Level Verification

For every specific claim in your output:

- **Numbers:** From a source, or generated? If generated → `[ESTIMATED]`
- **Names:** From a source you accessed, or memory? If memory → verify or label `[UNVERIFIED]`
- **Existence:** Does this paper actually exist? If you cannot confirm, DO NOT cite it
- **Attribution:** Does the paper actually say what you think? Use `read_paper` to verify

**YOU WILL FABRICATE under pressure to be precise.** The pattern: real concept + invented specifics (author name, fold-change, sample size). Catch yourself. Vague truth > precise fiction.

## Phase 6 — Diminishing Returns Gate

After each research action, assess marginal yield:

```
IF last action added new info that changes conclusions → CONTINUE
IF two independent sources agree, no contradictions   → CONVERGED: synthesize
IF last 2+ actions added nothing new                  → DIMINISHING: start writing
IF expanding laterally instead of resolving question   → SCOPE CREEP: refocus
IF question is more complex than initially classified  → UPGRADE TIER
```

The goal is sufficient evidence for the stakes level, not exhaustive coverage.
3 well-read papers beat 20 saved-but-unread papers.

## Phase 6b — Recitation Before Conclusion

Before writing any conclusion or synthesis that draws on multiple sources:

**Restate the specific evidence you're drawing from.** List the concrete data points, not summaries. Then derive the conclusion.

This is the "recitation strategy" (Du et al., EMNLP 2025, arXiv:2510.05381): prompting models to repeat relevant evidence before answering improves accuracy by +4% on long-context tasks. Training-free, model-agnostic. Works because it forces the model to retrieve and hold evidence in recent context before reasoning over it.

```
WRONG: "The evidence suggests X is effective."
RIGHT: "Study A found 26% improvement (n=500). Study B found no effect (n=200).
        Study C found 15% improvement but only in subgroup Y (n=1200).
        Weighing by sample size and methodology: modest evidence for X, limited to subgroup Y."
```

This is structural, not stylistic. Recitation surfaces contradictions that narrative synthesis buries.

## Phase 7 — Source Assessment

For each source that grounds a claim:

1. **Quality:** Peer-reviewed vs preprint vs blog? Sample size, methodology, COI?
2. **Situating:** Confirms prior work? Contradicts it? Novel/`[FRONTIER]`? Isolated/`[SINGLE-SOURCE]`?
3. **Confidence:** Strong methodology > volume of weaker studies. "We don't know yet" is valid.

## Phase 8 — Corpus Building

During and after research:
- **Papers:** `save_paper` for key finds, `fetch_paper` for papers you cited
- **Cross-paper synthesis:** `ask_papers` to query across fetched papers
- **Session end:** `export_for_selve` → run `./selve update` to embed into unified index
- **Research memos:** Write to project-appropriate location (`docs/research/`, `analysis/`)

<output_contract>
## Output Contract

### Quick Tier
Answer inline with source citation. No formal report.

### Standard Tier
```markdown
## [Topic] — Research Memo

**Question:** [what was asked]
**Tier:** Standard | **Date:** YYYY-MM-DD
**Ground truth:** [what was already known]

### Claims Table
| # | Claim | Evidence | Confidence | Source | Status |
|---|-------|----------|------------|--------|--------|
| 1 | ... | RCT / dataset | HIGH | [DOI/URL] | VERIFIED |
| 2 | ... | Inference | LOW | [URL] | INFERENCE |

### Key Findings
[With source quality assessment]

### What's Uncertain
[Unresolved questions]

### Sources Saved
[Papers/sources added to corpus]
```

### Deep Tier
Standard tier plus:
- **Disconfirmation results** — contradictory evidence found
- **Verification log** — claims verified via tool vs training data, caught fabricating
- **Search log** — queries run, tools used, hits/misses
- **Provenance tags** — every claim tagged

## Provenance Tags

Tag every claim:
- **`[SOURCE: url]`** — Directly sourced from a retrieved document
- **`[DATABASE: name]`** — Queried a reference database (ClinVar, gnomAD, DuckDB)
- **`[DATA]`** — Our own analysis, query reproducible
- **`[INFERENCE]`** — Logically derived from sourced facts (state the chain)
- **`[TRAINING-DATA]`** — From model training, not retrieved this session
- **`[PREPRINT]`** — From unreplicated preprint
- **`[FRONTIER]`** — From unreplicated recent work
- **`[UNVERIFIED]`** — Plausible but not verified

Never present inference as sourced fact. Never present training data as retrieved evidence.

**Precedence:** Admiralty grades (`[A1]`–`[F6]` per `source-grading` skill) are the standard for investigation/OSINT contexts — they grade both source reliability and information credibility. Provenance tags above (`[SOURCE]`, `[DATA]`, etc.) are the standard for general research — they track where a claim came from. When both apply (e.g., `/investigate` triggering `/researcher` for external validation), use Admiralty grades — they're strictly more granular. Don't duplicate by tagging the same claim with both systems.
</output_contract>

## Parallel Agent Dispatch (Deep tier)

- Split by **axis and subtopic**, not by tool
- Include ground truth context in each agent
- Dispatch verification agent after research agents return
- Synthesis is a separate step (agents can't see each other's output)
- 2 agents on 2 axes > 10 agents on 1 axis

<anti_patterns>
## Anti-Patterns

- **Synthesis mode default:** Summarized training data instead of fetching primary sources. THE failure mode this skill exists to prevent.
- **Confirmation bias:** Queries like "X validation" instead of "X criticism" or "X failed".
- **Authority anchoring:** Found one source and stopped
- **Precision fabrication:** Invented specific numbers under pressure to be precise
- **Author confabulation:** Remembered finding but not author, generated plausible name
- **Telephone game:** Cited primary study via review without reading the primary
- **Directionality error:** Cited real paper but inverted the sign of the finding
- **Single-axis search:** All queries from same starting point
- **Ground truth neglect:** Went external without checking local data first
- **Infinite research:** Kept searching past convergence instead of writing conclusions
- **Source hoarding:** Saved papers but never fetched/read them
- **Tier inflation/deflation:** Mismatched effort to stakes
- **MCP bypass:** Used WebSearch when a specialized MCP tool exists
- **Scope creep without pushback:** User asks 15 things, attempt all, run out of context. Say "this session can handle N of these well; which are priority?"
- **Training data as research:** Reciting textbook citations from training without `[TRAINING-DATA]` tags
- **S2 for recency:** Using Semantic Scholar when Exa is better for recent work
- **Redundant documentation:** For tools the model already knows, adding instructions is noise
</anti_patterns>

<evidence_base>
## What Research Shows About Agent Reliability

Evidence from 4 papers (Feb 2026), all read in full. Not aspirational — measured.

- **Instructions alone don't produce reliability.** EoG (IBM, arXiv:2601.17915): giving LLM perfect investigation algorithm as prompt = 0% Majority@3 for 2/3 models. Architecture (external state, deterministic control) produces reliability, not instructions. This skill is necessary but NOT sufficient — hooks, healthchecks, and deterministic scaffolding are what make agents reliable.
- **Consistency is flat.** Princeton (arXiv:2602.16666): 14 models, 18 months, r=0.02 with time. Same task + same model + different run = different outcome. Retry logic and majority-vote are architectural necessities.
- **Documentation helps for novel knowledge, not for known APIs.** Agent-Diff (arXiv:2602.11224): +19 pts for genuinely novel APIs, +3.4 for APIs in pre-training. Domain-specific constraints (DuckDB types, ClinVar star ratings) are "novel" = worth encoding. Generic tool routing is "known" = low value.
- **Simpler beats complex under stress.** ReliabilityBench (arXiv:2601.06112): ReAct > Reflexion under perturbations. More complex reasoning architectures compound failure.
</evidence_base>

$ARGUMENTS
---
name: model-review
description: Cross-model adversarial review via llmx. Dispatches architecture, code, or design decisions to Gemini 3.1 Pro and GPT-5.2 for independent critique, then fact-checks and synthesizes surviving insights. Supports review mode (convergent/critical) and brainstorming mode (divergent/creative).
argument-hint: [topic or decision to review — e.g., "selve search architecture", "authentication redesign"]
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - Task
---

# Cross-Model Adversarial Review

You are orchestrating a cross-model review. Same-model peer review is a martingale — no expected correctness improvement (ACL 2025, arXiv:2508.17536). Cross-model review provides real adversarial pressure because models have different failure modes, training biases, and blind spots.

## Prerequisites

- `llmx` CLI installed (`which llmx`)
- API keys configured for Google (Gemini) and OpenAI (GPT)
- Gemini Flash for fact-checking (`llmx -m gemini-3-flash-preview`)

## Pre-Flight: Constitutional Check

Before building context, check if the project has constitutional documents:

```bash
# Check for project principles — constitution may be standalone or a section in CLAUDE.md
CONSTITUTION=$(find . -maxdepth 3 -name "CONSTITUTION.md" 2>/dev/null | head -1)
if [ -z "$CONSTITUTION" ]; then
  # Check for ## Constitution section in CLAUDE.md (preferred location since 2026-03)
  CLAUDE_MD=$(find . -maxdepth 1 -name "CLAUDE.md" | head -1)
  if [ -n "$CLAUDE_MD" ] && grep -q "^## Constitution" "$CLAUDE_MD"; then
    CONSTITUTION="$CLAUDE_MD"  # Use CLAUDE.md — constitution is inline
  fi
fi
GOALS=$(find . -maxdepth 3 -name "GOALS.md" 2>/dev/null | head -1)
```

- **If constitution found (standalone or in CLAUDE.md):** Inject as preamble into ALL context bundles. Instruct models to review against project principles, not their own priors.
- **If GOALS.md exists:** Inject into GPT context (quantitative alignment check) and Gemini context (strategic coherence).
- **If neither exists:** Warn the user: *"No constitution (in CLAUDE.md or standalone) or GOALS.md found. Reviews will lack project-specific anchoring. Consider `/constitution` or `/goals` first."* Proceed anyway — cross-model review still has value without constitutional grounding.

## Mode Selection

Choose the mode BEFORE building context. These are cognitively different tasks.

### Review Mode (default)
**Convergent thinking.** Find what's wrong: errors, inconsistencies, missed edge cases, violations of stated principles.

- Lower temperature for Gemini (`-t 0.3`) — more deterministic, stern
- GPT reasoning-effort high — deep fault-finding
- Prompts ask "what's wrong" and "where does this break"
- Output: ranked list of problems with verification criteria

### Brainstorming Mode
**Divergent thinking.** Generate new ideas, alternative approaches, novel connections.

- Default/higher temperature for Gemini (`-t 0.8`) — more creative
- GPT reasoning-effort medium — broader exploration, less tunnel vision
- Prompts ask "what else could work" and "what's the unconventional approach"
- Output: ranked list of ideas with feasibility assessment

Select mode based on the review target:
- Code/architecture/decisions → **Review mode**
- Strategy/design space/exploration → **Brainstorming mode**
- User can override with `--brainstorm` or `--review`

## The Process

### Step 1: Define the Review Target

State clearly what's being reviewed: `$ARGUMENTS`

Identify:
- **The decision/recommendation/code** under review
- **Who made it** (you, a previous Claude session, a human)
- **What evidence exists** (code, configs, research, benchmarks)
- **Mode:** Review (default) or Brainstorming

### Step 2: Bundle Context

Build context files. Constitutional documents go first (if found).

**Output directory setup:**
```bash
# Persist outputs — NOT /tmp
# Slug from topic prevents collisions when multiple reviews run on the same day
REVIEW_SLUG=$(echo "$TOPIC" | tr '[:upper:]' '[:lower:]' | tr -cs '[:alnum:]' '-' | sed 's/^-//;s/-$//' | cut -c1-40)
REVIEW_DIR=".model-review/$(date +%Y-%m-%d)-${REVIEW_SLUG}"
mkdir -p "$REVIEW_DIR"
```

Where `$TOPIC` is a short label for the review target (e.g., "hook architecture", "search retrieval").
Use the first 2-3 words of the review subject. Examples:
- `.model-review/2026-03-01-hook-architecture/`
- `.model-review/2026-03-01-search-retrieval/`
- `.model-review/2026-02-28-genomics-split/`

**Gemini 3.1 Pro context** (~50K-200K tokens target):
```bash
cat > "$REVIEW_DIR/gemini-context.md" << 'HEADER'
# CONTEXT: Cross-Model Review of [topic]
HEADER

# Constitutional preamble (if found)
if [ -n "$CONSTITUTION" ]; then
  echo -e "\n# PROJECT CONSTITUTION\nReview against these principles, not your own priors.\n" >> "$REVIEW_DIR/gemini-context.md"
  cat "$CONSTITUTION" >> "$REVIEW_DIR/gemini-context.md"
fi
if [ -n "$GOALS" ]; then
  echo -e "\n# PROJECT GOALS\n" >> "$REVIEW_DIR/gemini-context.md"
  cat "$GOALS" >> "$REVIEW_DIR/gemini-context.md"
fi

# Append source code, configs, research, docs
# ... include everything. Gemini's strength is pattern-matching over large context.
```

**GPT-5.2 context** (~10K-30K tokens target):
```bash
cat > "$REVIEW_DIR/gpt-context.md" << 'HEADER'
# CONTEXT: Cross-Model Review of [topic]
HEADER

# Constitutional preamble (if found)
if [ -n "$CONSTITUTION" ]; then
  echo -e "\n# PROJECT CONSTITUTION\nQuantify alignment gaps. For each principle, assess: coverage (0-100%), consistency, testable violations.\n" >> "$REVIEW_DIR/gpt-context.md"
  cat "$CONSTITUTION" >> "$REVIEW_DIR/gpt-context.md"
fi
if [ -n "$GOALS" ]; then
  echo -e "\n# PROJECT GOALS\nAssess quantitative alignment. Which goals are measurably served? Which are neglected?\n" >> "$REVIEW_DIR/gpt-context.md"
  cat "$GOALS" >> "$REVIEW_DIR/gpt-context.md"
fi

# Focused summary — GPT's strength is reasoning depth, not context volume
```

**Token budget guidance:**
| Model | Sweet spot | Max useful | Strength |
|-------|-----------|------------|----------|
| Gemini 3.1 Pro | 80K-150K | ~500K | Pattern matching, cross-referencing across large context |
| GPT-5.2 | 15K-40K | ~100K | Deep reasoning with `--reasoning-effort high`, formal analysis |

### Step 3: Dispatch Reviews (Parallel)

Fire both reviews simultaneously. Each model gets a DIFFERENT cognitive task.

---

#### Review Mode Prompts

**Gemini 3.1 Pro — Architectural/Pattern Review:**
```bash
cat "$REVIEW_DIR/gemini-context.md" | llmx chat -m gemini-3.1-pro-preview \
  -t 0.3 --no-stream --timeout 300 "
[Describe what's being reviewed]

RESPOND WITH EXACTLY THESE SECTIONS:

## 1. Where the Analysis Is Wrong
Specific errors or oversimplifications. Reference actual code/config.

## 2. What Was Missed
Patterns, problems, or opportunities not identified. Cite files, line ranges, architectural gaps.

## 3. Better Approaches
For each recommendation, either: Agree (with refinements), Disagree (with alternative), or Upgrade (better version).

## 4. What I'd Prioritize Differently
Your ranked list of the 5 most impactful changes, with testable verification criteria.

## 5. Constitutional Alignment
$([ -n "$CONSTITUTION" ] && echo "Where does the reviewed work violate or neglect stated principles? Which principles are well-served?" || echo "No constitution provided — assess internal consistency only.")

## 6. Blind Spots In My Own Analysis
What am I (Gemini) likely getting wrong? Where should you distrust my assessment?

Be concrete. No platitudes. Reference specific code, configs, and findings.
" > "$REVIEW_DIR/gemini-output.md" 2>&1
```

**GPT-5.2 — Quantitative/Formal Analysis:**
```bash
cat "$REVIEW_DIR/gpt-context.md" | llmx chat -m gpt-5.2 \
  --reasoning-effort high --stream --timeout 600 "
[Describe what's being reviewed]

You are performing QUANTITATIVE and FORMAL analysis. Gemini is handling qualitative pattern review separately. Focus on what Gemini can't do well.

RESPOND WITH EXACTLY:

## 1. Logical Inconsistencies
Formal contradictions, unstated assumptions, invalid inferences. If math is involved, verify it.

## 2. Cost-Benefit Analysis
For each proposed change: estimated effort, expected impact, risk. Rank by ROI.

## 3. Testable Predictions
Convert vague claims into falsifiable predictions with success criteria. If a claim can't be made testable, flag it.

## 4. Constitutional Alignment (Quantified)
$([ -n "$CONSTITUTION" ] && echo "For each constitutional principle: coverage score (0-100%), specific gaps, suggested fixes." || echo "No constitution provided — assess internal logical consistency.")

## 5. My Top 5 Recommendations (different from the originals)
Ranked by measurable impact. Each must have: (a) what, (b) why with quantitative justification, (c) how to verify with specific metrics.

## 6. Where I'm Likely Wrong
What am I (GPT-5.2) probably getting wrong? Known biases to flag: overconfidence in fabricated specifics, overcautious scope-limiting, production-grade recommendations for personal projects.

Be precise. Show your reasoning. No hand-waving.
" > "$REVIEW_DIR/gpt-output.md" 2>&1
```

---

#### Brainstorming Mode Prompts

**Gemini 3.1 Pro — Creative Exploration:**
```bash
cat "$REVIEW_DIR/gemini-context.md" | llmx chat -m gemini-3.1-pro-preview \
  -t 0.8 --no-stream --timeout 300 "
[Describe the design space to explore]

Think divergently. Challenge assumptions. What would a completely different approach look like?

## 1. Alternative Architectures
3 fundamentally different approaches. Not variations — genuinely different paradigms.

## 2. What Adjacent Fields Do Differently
Patterns from other domains that could apply here. Cite specific systems or papers.

## 3. The Unconventional Idea
The approach that seems wrong but might work. Explain why it could succeed despite looking odd.

## 4. What's Being Over-Engineered
Where is complexity not earning its keep? What could be radically simplified?

## 5. Blind Spots
What am I (Gemini) missing because of my training distribution? Where should my creativity be distrusted?
" > "$REVIEW_DIR/gemini-brainstorm.md" 2>&1
```

**GPT-5.2 — Structured Ideation:**
```bash
cat "$REVIEW_DIR/gpt-context.md" | llmx chat -m gpt-5.2 \
  --reasoning-effort medium --stream --timeout 300 "
[Describe the design space to explore]

Generate novel approaches with feasibility assessment.

## 1. Idea Generation (10 ideas)
Quick-fire: 10 approaches ranked by novelty. For each: one sentence + feasibility (High/Medium/Low).

## 2. Deep Dive on Top 3
For each: architecture sketch, estimated effort, risk, what makes it non-obvious.

## 3. Combination Plays
Ideas that work poorly alone but well together. Cross-pollinate from the list above.

## 4. What Would Break Each Approach
Pre-mortem: for the top 3, what's the most likely failure mode?

## 5. Where I'm Likely Wrong
What am I (GPT-5.2) probably biased toward? Where should my suggestions be distrusted?
" > "$REVIEW_DIR/gpt-brainstorm.md" 2>&1
```

---

**Optional — Flash pattern extraction pass:**
For large codebases, a cheap Flash pass before the main reviews can surface mechanical issues:
```bash
cat /path/to/large-context.md | llmx chat -m gemini-3-flash-preview \
  -t 0.2 --no-stream --timeout 120 "
Mechanical audit only. Find:
- Duplicated content across files
- Inconsistent naming (model names, paths, conventions)
- Stale references (wrong versions, deprecated APIs)
- Missing cross-references between related documents
Output as a flat list. No analysis, no recommendations.
" > "$REVIEW_DIR/flash-audit.md" 2>&1
```

### Step 4: Fact-Check Outputs (MANDATORY)

**Both models hallucinate. Never adopt a recommendation without verification.**

For each claim in each review:

1. **Code claims** — Read the actual file and verify. Models frequently cite wrong line numbers, invent function names, or misread logic.
2. **Research claims** — Check if the cited paper/finding actually says what the model claims. Models often distort findings to support their argument.
3. **"Missing feature" claims** — Grep the codebase. The feature may already exist. Models frequently recommend adding things that are already implemented.

Use Flash for rapid fact-checking of specific claims:
```bash
echo "Claim: [model's claim]. Actual code: [paste relevant code]" | \
  llmx -m gemini-3-flash-preview "Is this claim about the code accurate? Be precise."
```

### Step 5: Extract & Enumerate (Anti-Loss Protocol)

**Why this step exists:** Single-pass synthesis is lossy. The agent biases toward recent, vivid, or structurally convenient ideas and silently drops others. In observed sessions, users had to ask "did you include everything?" 3+ times — each time recovering omissions. The EVE framework (Chen & Fleming, arXiv:2602.06103) shows that separating extraction from synthesis improves recall +24% and precision +29%.

**Do this BEFORE writing any synthesis prose.**

**5a. Extract claims per source.** For each model output, enumerate every discrete idea/recommendation/finding as a numbered item. One idea per line. Keep it mechanical — don't evaluate yet.

```markdown
## Extraction: gemini-output.md
G1. [Prediction ledger needed — no structured tracking exists]
G2. [Signal scanner has silent except blocks — masks failures]
G3. [DuckDB FTS preserves provenance better than vector DB]
...

## Extraction: gpt-output.md
P1. [Universe survivorship bias — S:5, D:5]
P2. [first_seen_date needed on all records for PIT safety]
P3. [FDR control mandatory — 5000-50000 implicit hypotheses/month]
...
```

**5b. Disposition table.** Every extracted item gets a verdict. No item left undispositioned.

```markdown
## Disposition Table
| ID  | Claim (short) | Disposition | Reason |
|-----|--------------|-------------|--------|
| G1  | Prediction ledger | INCLUDE — Tier 1 | Both models, verified gap |
| G2  | Silent except blocks | INCLUDE — Tier 6 | Verified in signal_scanner.py |
| G3  | DuckDB > vector DB | INCLUDE — YAGNI | Constitutional alignment |
| P1  | Universe survivorship | INCLUDE — Tier 4 | Verified, no PIT table exists |
| P2  | first_seen_date | INCLUDE — Tier 1 | Verified, downloads lack it |
| P3  | FDR control | DEFER | Needs experiment registry first |
| P7  | Kubernetes deployment | REJECT | Scale mismatch (personal project) |
| ... | ... | ... | ... |
```

Valid dispositions: `INCLUDE`, `DEFER (reason)`, `REJECT (reason)`, `MERGE WITH [ID]` (dedup).

**5c. Coverage check.** Before proceeding to synthesis:
- Count: total extracted, included, deferred, rejected, merged
- If any ID has no disposition → stop and fix
- Save extraction + disposition table to `$REVIEW_DIR/extraction.md`

This file is the checklist. If the user asks "did you include everything?" — point them here, not the prose.

### Step 6: Synthesize

Build the synthesis from the disposition table. Every INCLUDE item must appear. Reference IDs so coverage is auditable.

**Trust ranking for included items:**

| Trust Level | Criterion | Action |
|------------|-----------|--------|
| **Very high** | Both models agree + verified against code | Adopt |
| **High** | One model found + verified against code | Adopt |
| **Medium** | Both models agree but unverified | Verify before adopting |
| **Low** | Single model, unverified | Flag for investigation |
| **Reject** | Model recommends itself, or claim contradicts verified code | Discard |

**Output format:**

```markdown
## Cross-Model Review: [topic]
**Mode:** Review / Brainstorming
**Date:** YYYY-MM-DD
**Models:** Gemini 3.1 Pro, GPT-5.2
**Constitutional anchoring:** Yes/No (CLAUDE.md Constitution section or standalone, GOALS.md)
**Extraction:** N items extracted, M included, D deferred, R rejected

### Verified Findings (adopt)
| ID | Finding | Source | Verified How |
|----|---------|--------|-------------|
| G1, P4 | Prediction ledger needed | Gemini + GPT | No prediction table in DuckDB |

### Deferred (with reason)
| ID | Finding | Why Deferred |
|----|---------|-------------|

### Rejected (with reason)
| ID | Finding | Why Rejected |
|----|---------|-------------|

### Where I Was Wrong
| My Original Claim | Reality | Who Caught It |
|-------------------|---------|--------------|

### Gemini Errors (distrust)
| Claim | Why Wrong |

### GPT Errors (distrust)
| Claim | Why Wrong |

### Revised Priority List
1. ...
```

**Save both files:**
```bash
# Extraction + disposition (the checklist)
# Synthesis (the prose)
# Both persist in $REVIEW_DIR
```

### Step 7: Plan-Mode Handoff (Optional)

If the synthesis produced concrete INCLUDE items with actionable work, offer the user a plan-mode handoff:

> "Synthesis identified N actionable items. This review used ~X% context. Want me to write an implementation plan and hand off to a fresh context?"

If yes: call `EnterPlanMode`, write the implementation plan referencing INCLUDE items by ID (link to `$REVIEW_DIR/extraction.md`), then `ExitPlanMode`. The clear+execute dialog reclaims context — the plan file is the information bridge.

If no: end here. The synthesis and extraction persist in `$REVIEW_DIR/`.

Don't offer this if all findings are DEFER/REJECT or exploratory with no concrete next steps.

### Multi-Round Reviews

When running multiple dispatch rounds (e.g., Round 1 architecture + Round 2 red team):

1. **Extract per round, not per synthesis.** Each round's outputs get their own extraction pass (G1-Gn for round 1 Gemini, G2.1-G2.n for round 2 Gemini, etc.).
2. **Merge disposition tables across rounds** before writing the final synthesis. Dedup with `MERGE WITH [ID]`.
3. **Never synthesize a synthesis.** The final prose is written once from the merged disposition table. Don't compress round 1's synthesis — compress round 1's raw extraction alongside round 2's raw extraction.
4. **Total coverage count** in the final output: "R1: 47 items extracted, R2: 38 items extracted. Final: 85 total, 62 included, 14 deferred, 9 rejected."

This prevents the sawtooth pattern (compress → lose stuff → user catches → patch → compress again → lose different stuff).

## Known Model Biases

Flag these when they appear in outputs. Don't adopt recommendations that match a model's known bias without independent verification.

| Model | Bias | How It Manifests | Countermeasure |
|-------|------|-----------------|----------------|
| **Gemini 3.1 Pro** | Production-pattern bias | Recommends enterprise patterns (DuckDB migrations, service meshes) for personal projects | Check if recommendation matches project scale |
| **Gemini 3.1 Pro** | Self-recommendation | Suggests using Gemini for tasks, recommends Google services | Flag any self-serving suggestions |
| **Gemini 3.1 Pro** | Instruction dropping | Ignores structured output format in long contexts | Re-prompt if output sections are missing |
| **GPT-5.2** | Confident fabrication | Invents specific numbers, file paths, function names with high confidence | Verify every specific claim against actual code |
| **GPT-5.2** | Overcautious scope | Adds caveats that dilute actionable findings, hedges everything | Push for concrete recommendations |
| **GPT-5.2** | Production-grade creep | Recommends auth, monitoring, CI/CD for hobby projects | Match recommendations to actual project scale |
| **Flash** | Shallow analysis | Good for pattern matching, bad for architectural judgment | Use ONLY for mechanical audits and fact-checking |
| **Flash** | Recency bias | Defaults to latest patterns even when older ones are better | Don't use for "which approach" decisions |

## Model-Specific Prompting Notes

**Gemini 3.1 Pro:**
- Excels at cross-referencing across large context (finds contradictions between file A and file B)
- Review mode: `-t 0.3` for analytical work. Brainstorming mode: `-t 0.8` for creative exploration
- Note: Gemini thinking models may lock temperature server-side — the flag is a hint, not a guarantee
- Will recommend itself for tasks — always flag self-serving suggestions
- Tends to over-recommend architectural changes (DuckDB migrations, etc.)

**GPT-5.2:**
- `--reasoning-effort high` is essential for review mode (burns thinking time for deep fault-finding)
- `--reasoning-effort medium` for brainstorming mode (avoids tunnel vision)
- MUST use `--stream` with reasoning-effort high — non-streaming timeouts are common
- Temperature is locked at 1.0 for reasoning models (llmx overrides lower values)
- `--timeout 600` minimum for high reasoning effort
- Tends toward overcautious "production-grade" recommendations for personal projects
- **Differentiated role:** Quantitative/formal analysis — logical inconsistencies, math errors, cost-benefit, testable predictions. Gemini handles the qualitative pattern review.

**Gemini Flash (`gemini-3-flash-preview`):**
- Use for rapid verification of specific claims against code snippets
- Fast and cheap — good for 10-20 quick checks and mechanical audits
- Don't use for architectural judgment, only factual verification and pattern matching
- Note: `gemini-flash-3` and `gemini-3-flash` are both 404s — always use `gemini-3-flash-preview`

## Anti-Patterns

- **Synthesizing without extracting first.** The #1 information loss pattern. Never go from raw model outputs directly to prose synthesis. Always run the extraction + disposition step (Step 5) first. If you skip it, the user will ask "did you include everything?" and you will have lost items.
- **Synthesizing a synthesis.** Each compression pass drops ideas. If you have Round 1 synthesis + Round 2 outputs, don't compress the Round 1 synthesis — go back to Round 1's raw extraction and merge with Round 2's extraction. One synthesis pass from merged extractions, not cascaded compressions.
- **Adopting recommendations without code verification.** Both models hallucinated "missing" features that already existed in the codebase.
- **Treating model agreement as proof.** Two models can be wrong the same way (shared training data). Always verify against source code.
- **Letting models review their own previous output.** Send fresh prompts, not "here's what you said last time, improve it."
- **Using same-model instances as "different reviewers."** Claude reviewing Claude = same distribution. This skill exists because cross-model is the only form that provides real adversarial pressure.
- **Skipping the self-doubt section.** The "Where I'm Likely Wrong" section is the most valuable part of each review. Models that can't identify their own weaknesses are less trustworthy.
- **Same prompt to both models.** Gemini and GPT have different strengths. Sending the same qualitative prompt to both wastes GPT's formal reasoning capability. Gemini = patterns, GPT = quantitative/formal.
- **Writing to /tmp.** Review outputs are valuable artifacts. Always persist to `.model-review/YYYY-MM-DD-topic/`.
- **Using bare date directories.** `.model-review/2026-03-01/` will collide when two reviews run the same day. Always append a topic slug.
- **Skipping constitutional check.** Reviews without project-specific anchoring drift into generic advice. Always check for constitution (in CLAUDE.md or standalone) and GOALS.md first.
- **Mixing review and brainstorming.** Convergent (find errors) and divergent (generate ideas) thinking are cognitively different. Don't ask for both in one prompt — the outputs will be mediocre at both.

$ARGUMENTS
---
name: session-analyst
description: Analyzes Claude Code session transcripts for behavioral anti-patterns — sycophancy, over-engineering, build-then-undo, token waste. Dispatches compressed transcripts to Gemini for analysis, appends structured findings to meta/improvement-log.md. The "recursive self-improvement" component.
user-invocable: true
context: fork
argument-hint: <project> [session_count]
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Write
  - Edit
---

# Session Analyst

Analyze session transcripts for behavioral patterns that no linter or static analysis can detect. This is for agent behavioral failures — not code quality.

## Current Environment
`!echo "Date: $(date +%Y-%m-%d) | CWD: $(basename $PWD) | Transcripts: $(ls ~/.claude/projects/ | wc -l | tr -d ' ') project dirs"`

## What This Detects
1. **Sycophantic compliance** — Built what was asked without pushback when pushback was warranted
2. **Over-engineering** — Complex solution when simple would work (abstraction before evidence)
3. **Build-then-undo** — Code written then deleted/reverted in same session (wasted tokens)
4. **Token waste** — Excessive tool calls, redundant searches, reading files already in context
5. **Advisory rule violations** — Things CLAUDE.md/rules say to do but the agent didn't
6. **Missing disconfirmation** — Research without contradictory evidence search
7. **Source grading gaps** — Claims in research files without provenance tags

## What This Does NOT Detect
Dead code (use vulture/ast), style issues (use ruff/eslint), type errors (use mypy/tsc). Those are static analysis problems, not behavioral ones.

## Process

### Step 1: Extract Transcripts
Parse the project argument from $ARGUMENTS. Default: last 5 sessions.

```bash
python3 ~/Projects/skills/session-analyst/scripts/extract_transcript.py <project> --sessions <N> --output /tmp/session_analysis_input.md
```

Verify the output is reasonable (<100KB, readable markdown).

### Step 2: Dispatch to Gemini
Use llmx to send compressed transcript to Gemini 3.1 Pro (1M context, cheap) with the analysis prompt:

```bash
llmx -p google -m gemini-2.5-pro -f /tmp/session_analysis_input.md "$(cat <<'PROMPT'
You are analyzing Claude Code session transcripts for behavioral anti-patterns. For each session, identify:

1. SYCOPHANCY: Did the agent build something without questioning whether it was the right approach? Look for: user requests complex feature → agent immediately starts building (no "do we need this?" or "simpler alternative?"). Distinguish genuine helpfulness from compliance.

2. OVER-ENGINEERING: Did the agent build something more complex than needed? Look for: abstractions with one caller, config systems for hardcoded values, frameworks for single-use scripts.

3. BUILD-THEN-UNDO: Was code written then deleted or substantially rewritten in the same session? Calculate approximate wasted tokens.

4. TOKEN WASTE: Excessive tool calls — reading the same file twice, searching for something already in context, redundant web searches, reading entire files when a grep would suffice.

5. RULE VIOLATIONS: Based on the messages, did the agent skip source grading, skip disconfirmation search, commit without being asked, or violate other stated principles?

6. MISSING PUSHBACK: Did the user propose something questionable and the agent went along? Look for technically suboptimal decisions the agent should have flagged.

For each finding, output this exact format:

### [CATEGORY]: [one-line summary]
- **Session:** [session ID prefix]
- **Evidence:** [specific message excerpts or tool call sequences]
- **Failure mode:** [category name from agent-failure-modes.md, or "NEW: description"]
- **Proposed fix:** [hook | skill | rule | CLAUDE.md change | architectural]
- **Severity:** [low | medium | high] based on wasted effort or risk

If a session has no notable anti-patterns, say so explicitly — do not fabricate findings.
Output ONLY the findings, no preamble.
PROMPT
)"
```

### Step 3: Review and Append
1. Read the Gemini output critically — it may hallucinate session details
2. Cross-check any specific claims against the transcript
3. Append validated findings to `~/Projects/meta/improvement-log.md` with today's date
4. If a finding maps to a known failure mode, reference it. If new, flag as "NEW"

### Step 4: Summary
Report to user:
- Sessions analyzed: N
- Findings: N (by category)
- New failure modes discovered: N
- Proposed fixes: list

## Output Format (appended to improvement-log.md)

```markdown
### [YYYY-MM-DD] [CATEGORY]: [summary]
- **Session:** [project] [session-id-prefix]
- **Evidence:** [what happened, with message excerpts]
- **Failure mode:** [link to agent-failure-modes.md category, or "NEW"]
- **Proposed fix:** [hook | skill | rule | CLAUDE.md change | architectural]
- **Status:** [ ] proposed
```

## Notes
- Transcript source: `~/.claude/projects/-Users-alien-Projects-{project}/` (native Claude Code storage)
- Preprocessor strips thinking blocks (huge, low signal) and base64 content
- Gemini 3.1 Pro at ~$0.001/query cached — cheap enough to run frequently
- If llmx is unavailable, you can still extract transcripts and analyze them directly (less context capacity but still useful)

$ARGUMENTS


# CROSS-REPO EVIDENCE: Meta Reaching Into Other Repos

These are concrete examples of the current workflow this MCP would improve:

1. Intel session f32653c6: meta's session-analyst diagnosed sycophantic compliance (105 tasks, 145 usage-limit spins), then wrote "Download Discipline" rule into intel's CLAUDE.md and deployed bash-failure-loop hook.

2. Selve-Genomics split: Meta planned and validated the split (116 scripts, 9 skills), directing hook refactoring per-repo via cross-model review.

3. 11+ global/project hooks: Designed in meta from session analysis, deployed by editing settings.json files.

4. Intel skill restructuring: Cross-model reviews in meta directed priority changes in intel skills.

5. Supervision audit: Analyzed 68 sessions across all projects (28.9% waste in intel, 26.9% in selve), deployed fixes globally.

6. Auto-overview trigger: Designed in meta, affects regeneration across intel/selve/genomics.

Current workflow: meta accumulates knowledge -> human cd's into meta -> agent analyzes -> human cd's into target repo -> agent implements. MCP would let target repo's session query meta directly.


# THE PROPOSAL

Build a FastMCP v3 server in meta that exposes accumulated knowledge as tools. Key questions:
- Is MCP the right abstraction vs .claude/rules/, emb search, thicker CLAUDE.md files?
- What knowledge benefits from on-demand vs always-loaded? What's the partition?
- Tool design: search-based? category-based? how granular?
- Portability: MCP declared in .mcp.json (travels with repo) vs global CLAUDE.md (machine-local). Better?
- Alternative architectures we haven't considered?
- Failure modes: when would this make things worse?

FastMCP v3 capabilities available: FileSystemProvider, SkillsProvider, ResourcesAsTools transform, per-session visibility, component versioning, composable lifespans, instructions= parameter.
