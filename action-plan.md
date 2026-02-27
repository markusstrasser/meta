# Action Plan: Deep Layer Implementation for Intel

**Date:** 2026-02-27
**Goal:** Implement the foundational CLAUDE.md + rules + skills + hooks configuration such that epistemic discipline, adversarial orientation, and temporal coherence become structural rather than aspirational.
**Principle:** Maximize error-correction rate per dollar. Every item below either closes a feedback loop, prevents a known error class, or reduces the latency between error and correction.

---

## What This Replaces

Currently, epistemic discipline depends on the human remembering to invoke it. Multi-model review is ad hoc. Competing hypotheses is referenced but has no skill file. Predictions don't auto-resolve. Kill conditions are prose. The agent drifts without human course correction.

After implementation: every Claude session in intel automatically operates with source grading, base rates, competing hypotheses, and adversarial default — not because the agent is told to, but because the infrastructure enforces it.

---

## Phase 1: The Deepest Layer (CLAUDE.md + Rules)

### 1.1 Trim CLAUDE.md to ~120 lines

Current: ~244 lines. Community consensus and Anthropic's own data: past ~150 lines, the model stops absorbing instructions equally. Important rules get lost in noise.

**Move out:**
- Common Commands section (80+ lines) → already in `/commands` skill
- Detailed DuckDB gotchas → already in `.claude/rules/duckdb.md`
- Detailed tool execution notes → already in `.claude/rules/tools.md`
- Dataset-specific gotchas → already in `.claude/rules/datasets.md`

**Add (5 lines):**
```markdown
## Generative Principle
Maximize the rate of epistemic error correction, measured by market feedback.
When in doubt about what to do or how to prioritize, ask: "Does this increase
the rate at which we correct errors about the world?" If yes, do it.
```

**Add (anti-sycophancy, tested effective):**
```markdown
## Communication
Never start responses with positive adjectives about the user's input.
Skip flattery and respond directly. Find what's wrong first.
```

### 1.2 Add Amendment Rules to CONSTITUTION.md

Hart's secondary rules — currently missing. Required for autonomous operation.

```markdown
## Amendment Rules
- CONSTITUTION.md: Human approval required. Never auto-modified.
- priors.md base rates: Require N>=3 new cases or multi-model review. Log prior→evidence→posterior.
- scoring.py formulas: Changes require backtest on held-out data before merge.
- MEMORY.md: AI may add entries during sessions. Entries require evidence from 2+ sessions.
  Quarterly human review to prune stale entries.
- .claude/rules/: AI may propose. Human approves before commit.
- Entity files: AI may append to ## Signal Inbox. Human writes narrative sections.
```

### 1.3 Add Epistemic Discipline Rule

New file: `.claude/rules/epistemics.md`

```yaml
---
paths:
  - "analysis/**"
  - "memory/**"
---
```

Content:
- Every factual claim in entity files requires [SOURCE_GRADE]
- Every quantitative claim requires base rate from priors.md
- Leads >$10M require /competing-hypotheses before commitment
- Predict data footprint BEFORE querying (Phase 2 discipline)
- LLM outputs are [F3] until verified against data
- Detrend before claiming correlation (cite Brooklyn lesson)

This is Frankfurt's second-order move: not "always source-grade" (first-order rule) but a rule file that makes the system WANT to source-grade by loading it into context whenever analysis files are active.

---

## Phase 2: Skills (Structural Enforcement)

### 2.1 Create /competing-hypotheses Skill

The most-cited workflow in CLAUDE.md with NO implementation. This is the #1 gap.

File: `.claude/skills/competing-hypotheses/SKILL.md`

Structure:
1. State the lead/hypothesis explicitly
2. Generate minimum 3 competing explanations (including "benign coincidence" and "data artifact")
3. For each hypothesis, predict what data footprint it would leave
4. Query data to test predictions
5. Score each hypothesis against the evidence matrix
6. Output: surviving hypothesis with confidence, killed hypotheses with reason

Based on Richards Heuer's CIA ACH methodology, already referenced in `docs/workflows/investigate.md`.

### 2.2 Create /multi-model-review Skill

Currently ad hoc ("use gemini 3.1 and gpt5.2 to review"). Should be one command.

File: `.claude/skills/multi-model-review/SKILL.md`

Structure:
1. Accept: file path(s) to review + review type (pattern/math/review/compare)
2. Route per model-guide: pattern→Gemini, math→GPT-5.2, review→Gemini, compare→both
3. Use llm_check.py with structured numbered questions (validated effective)
4. Feed first model's review as context to second model (adversarial pressure)
5. Output: synthesis with [VERIFIED]/[PLAUSIBLE]/[HALLUCINATED] tags per claim
6. Auto-commit results to analysis/llm_checks/

This replaces the recurring pattern of "use gemini and gpt to review" that appears in every session.

### 2.3 Upgrade /thesis-check with Proactive Triggering

The skill exists and is excellent. What's missing: proactive staging.

Add to signal_scanner.py output: when a CRITICAL or WARNING signal matches a watchlist ticker with an open position, append:
```
THESIS-CHECK RECOMMENDED: {TICKER} — signal: {signal_type}
```

This appears in the daily triage output. For autonomous operation, it queues a thesis-check task.

---

## Phase 3: Feedback Loop Closure

### 3.1 Add prediction_tracker resolve to daily_update.sh

Two lines. The single highest-leverage fix. Currently predictions can sit unresolved for weeks — the Brier score feedback loop has a human-dependent step in the middle.

```bash
# After signal scanner, before paper ledger
echo "=== Resolving predictions ===" >> "$LOG"
uvx --with duckdb --with yfinance python3 tools/prediction_tracker.py resolve --auto 2>&1 | tee -a "$LOG"
```

### 3.2 Add source_eval resolve to weekly_update.sh

Source credibility scores can be stale for months. Not in any cron job.

```bash
echo "=== Resolving source claims ===" >> "$LOG"
uvx --with duckdb --with yfinance python3 tools/source_eval.py resolve 2>&1 | tee -a "$LOG"
```

### 3.3 Create corrections register

New file: `analysis/corrections.md`

Template:
```markdown
# Corrections Register

Track errors, when caught, cost/impact, and fix applied. This IS the error-correction rate metric.

## Format
| Date | Error | How Caught | Impact | Fix | Lesson |
|------|-------|-----------|--------|-----|--------|
| 2026-02-27 | prior_odds passes probability not odds | GPT-5.2 math review | Small (9.09% vs 10%) | Fix in fuse_evidence() | Always verify probability↔odds at API boundaries |
| 2026-02-27 | TOUCH resolution inflates accuracy | Multi-model review | Medium (win rate overstated) | Default to TERMINAL | Precommit resolution mode at prediction time |
| 2026-02-27 | scoring.py E[LLR] comment wrong | GPT-5.2 independent verification | Low (comment only) | Fix comment | Mathematical comments need verification |
```

Every fix commit should add a row. This makes the error-correction rate measurable (Popper).

---

## Phase 4: Precommitment Infrastructure (Elster)

### 4.1 Kill Conditions in Entity YAML Frontmatter

Add structured kill conditions that triage.py can parse:

```yaml
kill_conditions:
  - trigger: "FDA rejects compounded semaglutide"
    action: "EXIT full position"
    deadline: 2026-06-30
  - trigger: "Insider cluster sell > 3 executives in 30 days"
    action: "REDUCE to half"
```

Wire into staleness.py or a new tool that checks these against daily signals.

### 4.2 Open Questions File

New file: `analysis/open_questions.md`

Active hypotheses with falsification criteria stated BEFORE investigation (Bratman planning):

```markdown
## Active Hypotheses

### HIMS: FDA will approve compounded semaglutide regulation by Q3 2026
- **Falsification:** FDA issues enforcement guidance banning compounding
- **Data to watch:** Federal Register, FDA warning letters, Congressional hearings
- **Status:** Awaiting data
- **Registered:** 2026-02-25

### Brooklyn Cluster: Shared infrastructure indicates coordinated billing
- **Falsification:** Infrastructure sharing is explained by common registered agent services
- **Data to watch:** UCC filings, corporate records, ProPublica 990s
- **Status:** Partially confirmed (composite LLR +3.0 for 3/3 sharing)
- **Registered:** 2026-01-15
```

---

## Phase 5: Hooks (Hard Enforcement)

### 5.1 Pre-commit Mathematical Verification

The prior_odds error sat in scoring.py until multi-model review caught it. A pre-commit hook that runs basic sanity checks on scoring.py changes would catch this class of error.

Add to `.githooks/pre-commit`:
```bash
# If scoring.py changed, run unit tests
if git diff --cached --name-only | grep -q "scoring.py"; then
    uvx --with duckdb python3 -m pytest tools/tests/test_scoring.py -q || exit 1
fi
```

(Requires creating `tools/tests/test_scoring.py` with basic invariant checks.)

### 5.2 Source Grade Enforcement for Entity Files

Currently advisory. Could be a PostToolUse hook that checks entity file edits for source grades.

Lower priority — the `.claude/rules/epistemics.md` should handle most cases. Only escalate to hook if the rule is repeatedly ignored.

---

## Phase 6: Autonomous Loop (MVP)

This is the headless entity refresher from review-synthesis.md, now informed by all the research:

```
staleness.py → SQLite queue → cron every 15 min →
claude -p --max-turns 15 → subprocess timeout 30 min →
git commit on success → Telegram alert for human review
```

Key design decisions validated by research:
- **Fresh sessions, not --resume** (quadratic cost avoidance, validated by GPT-5.2 math)
- **15 turns max** (Gemini + our own failure data agree; Anthropic's own engineering uses similar bounds)
- **Explicit delegation with boundaries** (Anthropic's multi-agent lessons: each task needs objectives, output format, tool guidance, task boundaries)
- **Self-generated skills are worthless** (SkillsBench: 0% improvement; curated skills: +16.2%. Human-authored knowledge only.)
- **SQLite for durable state** (cron + SQLite over async Python — Gemini's "one weekend MVP")
- **Document & Clear pattern** (write progress to markdown, exit, queue continuation)

---

## Implementation Order

| Priority | Item | Effort | Error-Correction Impact |
|----------|------|--------|------------------------|
| 1 | Trim CLAUDE.md + add generative principle | 1 hour | Every session starts better-oriented |
| 2 | Add prediction_tracker resolve to daily cron | 5 min | Closes the Brier feedback loop |
| 3 | Create /competing-hypotheses skill | 2 hours | Structural adversarial forcing on every lead |
| 4 | Create corrections register | 30 min | Makes error-correction rate measurable |
| 5 | Add .claude/rules/epistemics.md | 30 min | Epistemic discipline loads automatically |
| 6 | Create /multi-model-review skill | 2 hours | Replaces ad hoc "use gemini to review" |
| 7 | Add amendment rules to CONSTITUTION.md | 15 min | Enables autonomous methodology updates |
| 8 | Kill conditions in entity YAML | 1 hour | Precommitment becomes checkable |
| 9 | Open questions file | 30 min | Planning agency across sessions |
| 10 | Add source_eval resolve to weekly cron | 5 min | Source credibility stays current |
| 11 | Pre-commit scoring.py tests | 2 hours | Catches math errors before commit |
| 12 | Autonomous loop MVP | 1 weekend | The whole point — headless entity refresh |

**Total estimated effort:** ~2 days for items 1-11, 1 weekend for item 12.

---

## What Falls Away

With this infrastructure in place, the following recurring session patterns disappear:

| Current Pattern | Why It Disappears |
|----------------|-------------------|
| "Use gemini and gpt to review" (every session) | /multi-model-review skill does it in one command |
| Re-explaining goals at session start | Generative principle in CLAUDE.md, zero-shot |
| Human remembering to resolve predictions | daily_update.sh does it automatically |
| Fix commits days after initial error | Pre-commit tests + automatic review catch errors earlier |
| Manual competing hypotheses | /competing-hypotheses skill structures it |
| Prose kill conditions nobody checks | YAML frontmatter, parsed by triage.py |
| "What should I work on?" drift | open_questions.md + staleness.py + signal scanner provide prioritized queue |
| Entity files going stale | Autonomous loop refreshes them headlessly |
| Methodology changes without evidence | Amendment rules require N>=3 cases or review |
| Error lessons scattered across files | Corrections register centralizes them |

The deepest layer is: **CLAUDE.md (120 lines, generative principle) + .claude/rules/epistemics.md (loaded when analyzing) + 2 new skills (competing-hypotheses, multi-model-review) + daily cron resolve + corrections register.**

Everything else is important but derivative. Get the deepest layer right and the rest self-organizes.

---

## Research Sources

### Practical LLM Prompting (What Actually Works)
- [Anthropic: How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) — orchestrator-worker pattern, explicit delegation, breadth-before-depth
- [Blake Crosley: Runtime Constitutions for Self-Governing Agents](https://blakecrosley.com/es/blog/agent-self-governance) — canonical source registration, active governance gates, immutable governance files. SkillsBench: self-generated skills = 0% improvement.
- [Simon Willison: Claude 4 System Prompt](https://simonwillison.net/2025/May/25/claude-4-system-prompt/) — "Never start with positive adjectives" as tested anti-sycophancy
- [Anthropic: Sycophancy to Subterfuge](https://github.com/anthropics/sycophancy-to-subterfuge-paper) — sycophancy is gateway to reward tampering; structural enforcement needed
- [DreamHost: 25 Claude Prompt Techniques Tested](https://www.dreamhost.com/blog/claude-prompt-engineering/) — Claude 4.x takes instructions literally; precise structural prompts matter
- [ACL 2025: Epistemic Markers](https://aclanthology.org/2025.naacl-long.452/) — LLM-judges penalize uncertainty; enforce calibration structurally

### Claude Code Architecture
- [Marc0.dev: Claude Code Hooks Production Patterns](https://www.marc0.dev/en/blog/claude-code-hooks-production-patterns-async-setup-guide-1770480024093)
- [Kyle Stratis: Better Practices Guide](https://www.kylestratis.com/posts/a-better-practices-guide-to-using-claude-code/)
- [Mario Ottmann: Rules vs Skills vs Subagents vs MCPs](https://marioottmann.com/articles/claude-code-customization-guide)
- [r/LocalLLaMA: Prompts Aren't Enough for Long-Running Agents](https://www.reddit.com/r/LocalLLaMA/comments/1rev8jl/prompts_arent_enough_for_longrunning_agents_they/)

### Constitutional / Philosophical
- [Zvi Mowshowitz: Three-part analysis of Claude's Constitution](https://thezvi.substack.com/p/claudes-constitutional-structure)
- [Anthropic: Constitutional AI paper](https://arxiv.org/abs/2212.08073)
- [Askell et al: Specific vs General Principles](https://arxiv.org/abs/2310.13798)
- [Agent Drift](https://arxiv.org/abs/2601.04170) — ~50% purpose drift by 600 interactions
- [Agent Behavioral Contracts](https://arxiv.org/abs/2602.22302) — Lyapunov drift bounds
- Ginsburg, Elkins, Melton: *The Endurance of National Constitutions* (2009) — flexibility + inclusion + specificity

### Multi-Model Review (Our Own Data)
- review-synthesis.md in this repo — --resume is wrong, 15 turns max, SQLite over DAG, fresh sessions
- constitutional-delta.md in this repo — generative principle, seven philosophical streams
