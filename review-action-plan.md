# Multi-Model Review: Action Plan
**Date:** 2026-02-27
**Reviewers:** Gemini 3.1 Pro (2 queries: broad review + architecture/failure modes), GPT-5.2 (1 query: math verification)
**Cost:** ~$3-4 total
**Source grades:** Gemini architectural claims `[C3]`, GPT-5.2 math derivations `[A2]`

---

## Consensus Findings (Both Models Agree)

### 1. Autonomous Loop Will OOM Without Concurrency Lock [CRITICAL]
**Gemini Q1:** "If Task A takes 16 minutes, Cron dispatches Task B. Two parallel DuckDB connections. Machine OOMs."
**Gemini Q2:** "Task 2 spawns a second claude -p instance. DuckDB throws locking error. WAL spills to disk. OOM-killer terminates MCP server."

**Fix:** File lock (`fcntl.flock`) or SQLite `status='RUNNING'` mutex. If lock held, cron exits immediately.

**Verdict:** TAKE. This is a day-one crash. Must add to Phase 6.

### 2. No Budget Circuit Breaker in MVP [CRITICAL]
**Gemini Q1:** "Running claude -p 96 times/day at ~$1-2/task = $100-200/day."

**Fix:** Hard daily dollar limit in orchestrator. Track cumulative spend in SQLite. Stop dispatching when limit hit.

**Verdict:** TAKE. $30/day cap, enforced in code.

### 3. Corrections Register Should Be CSV, Not Markdown [BOTH AGREE]
**Gemini Q1:** "You cannot run SQL aggregations on a markdown table."
**GPT-5.2:** "The register alone doesn't define the metric. You need an explicit denominator."

**Fix:** `datasets/corrections.csv` + `tools/log_correction.py` for the agent to call. Define metric as impact-weighted corrections per dollar + median time-to-detect.

**Verdict:** TAKE. CSV > markdown for anything we want to measure.

### 4. Build Skills BEFORE Trimming CLAUDE.md [SEQUENCING FIX]
**Gemini Q1:** "You are tearing down the fence before building the wall. Build skills first, then trim."

**Fix:** Reorder: (1) cron resolves, (2) create skills, (3) epistemics rule, (4) THEN trim CLAUDE.md.

**Verdict:** TAKE. Obvious in hindsight.

---

## GPT-5.2 Math Findings [A2]

### 5. 150-Line Threshold Has No Evidence
"The specific threshold (~150 lines) is not evidenced by the provided materials. Instruction-following generally degrades as instruction sets grow and conflict."

**Fix:** Replace claim with: "Keep always-loaded instructions short; push detail into selectively-loaded rules/skills."

**Verdict:** TAKE. The direction is right, the number is made up.

### 6. N>=3 Prior Update Rule Is Not Statistically Justified
"Beta updates are valid for any n>=0. 'Meaningful' depends on prior ESS."
Derives: n >= 0.1(α+β) as "new data is at least 10% of pseudo-count mass."

**Fix:** Replace "N>=3" with ESS-based criterion: `n >= 0.1 * ESS` or posterior shift threshold.

**Verdict:** TAKE. Better rule.

### 7. Sigmoid Sampling Is Mathematically Sound [CONFIRMS]
"12.19x ratio is consistent with logistic over ±2.5. Valid probability distribution. UCB1 only better if you define/measure reward."

**Verdict:** CONFIRMS prior design. Start with sigmoid, add UCB when reward data exists.

### 8. Scoring.py Test Invariants [EXTREMELY USEFUL]
Provides specific invariants:
- `llr_from_percentile`: monotonicity, E[H0] = -0.1931, known point checks (u=0.95→0.8047)
- `fuse_evidence`: identity with no evidence, additivity, odds ratio scaling
- `composite_infrastructure_llr`: correct mapping (0→-0.5, 1→0.7, 2→1.8, 3→3.0), monotonicity

**Verdict:** TAKE verbatim for test_scoring.py. Pure math, no DuckDB needed.

### 9. Error-Correction Metric Needs Explicit Denominator
"Given the plan's principle ('maximize error-correction rate per dollar'), use impact-weighted corrections per dollar + latency metrics (time-to-detect, time-to-fix)."

**Verdict:** TAKE. Three metrics: (1) corrections/dollar, (2) median time-to-detect, (3) median time-to-fix.

### 10. Quadratic Cost for Resumed Sessions Confirmed [CONFIRMS]
"Under resume-includes-full-history, quadratic growth is correct. Compaction restores near-linear at cost of information loss."

**Verdict:** CONFIRMS. Fresh sessions only.

---

## Gemini Architecture Findings [C3]

### 11. Epistemics Rule Will Degrade After Turn 6
**Gemini Q2:** "Once context exceeds ~40k tokens with tabular data, Claude's attention mechanism will prioritize recency of massive data dump."

**Assessment:** PARTIALLY VALID but OVERCORRECTED. Rules are in system prompt (primacy position), not middle of context. They'll degrade under context pressure but won't vanish. More importantly, the rule serves as a reminder at session START before context fills up. The real fix is short sessions (15 turns max), which we already have.

**Verdict:** LEAVE the architecture as-is. The 15-turn cap IS the mitigation.

### 12. Skills Must Be "Programmatic Harness, Not Text Prompt"
**Gemini Q2:** "The skill must force a hard stop after hypothesis generation, execute mandatory DuckDB query."

**Assessment:** OVERCORRECTION. Claude Code skills ARE markdown files loaded into prompt. That's the architecture — you can't make them "programmatic state machines" without building custom tooling outside Claude Code. The SkillsBench 16.2% improvement comes from well-structured procedural prompts, not from external harnesses.

**Verdict:** LEAVE. Structure the skills as detailed step-by-step procedures with explicit tool-use instructions. That's "curated" in the SkillsBench sense.

### 13. Entity YAML + LLM Prose = Broken Formatting
**Gemini Q2:** "LLMs are fundamentally incapable of reliably preserving strict whitespace when editing mixed-mode files. It will change a date from 2026-06-30 to June 30, 2026."

**Assessment:** VALID CONCERN. Our existing entity files already have YAML frontmatter (staleness.py parses it) and this hasn't broken yet, but adding MORE structured data (kill conditions) increases risk.

**Fix:** Keep kill conditions simple (single-line triggers, not nested YAML arrays). Or use a separate `kill_conditions.yaml` file.

**Verdict:** PARTIALLY TAKE. Simplify the kill condition format.

### 14. Amendment Rules Are Over-Engineering
**Gemini Q1:** "For a 1-person project, writing formal Amendment Rules for an AI to propose changes to its own Constitution is administrative bloat."

**Assessment:** VALID. Single line in CLAUDE.md: "Do not edit CONSTITUTION.md. You may update priors.md and mechanisms.md based on backtest results."

**Verdict:** TAKE. Kill the amendment rules section. One line instead.

### 15. yfinance Failure → Corrupted Brier Scores
**Gemini Q2:** Maps exact cascade: yfinance rate-limited → stale price → wrong resolution → corrupted Brier → poisoned LLR weights.

**Fix:** prediction_tracker.py resolve needs a freshness check: if latest price is >2 trading days old, skip resolution and log warning.

**Verdict:** TAKE. Add price freshness gate.

### 16. 6-Month Failure: Queue Bankruptcy / Alert Fatigue
**Gemini Q2:** "By month 3, 400 backlogged triage items. You stop reading git diffs. Agent drift sets in. Entity files fill with hallucinated slop."

**Assessment:** VALID but premature. This is a Phase 2+ problem. The MVP runs 1 task per cron cycle, not 96/day. But the warning is real.

**Fix:** Built-in decay: auto-dismiss triage items older than 14 days. Cap entity file commits to 1/entity/week. Require human review every N commits.

**Verdict:** NOTE for Phase 2. Not blocking for MVP.

---

## What's Missing (Both Models Identified)

### 17. Upstream Schema Drift Detection
**Gemini Q1:** "Government datasets change column names without warning. Autonomous loop will blindly fail and retry, burning budget."

**Fix:** healthcheck.py already validates views. Wire it as pre-flight check before each autonomous task.

### 18. Data Freshness Checks
**Gemini Q1:** "Nothing checks if DuckDB data is stale relative to the real world."

**Fix:** Already partially addressed by staleness.py's coverage dates. Could add a `data_freshness` check to healthcheck.

---

## Revised Implementation Order

Based on all three reviews:

| Priority | Item | Change from Original |
|----------|------|---------------------|
| 1 | Add prediction_tracker resolve to daily cron | UNCHANGED — both models agree this is highest ROI |
| 2 | Add source_eval resolve to weekly cron | MOVED UP from #10 — trivial effort, closes loop |
| 3 | Create /competing-hypotheses skill | UNCHANGED — #1 epistemic gap |
| 4 | Create /multi-model-review skill | MOVED UP — needed before CLAUDE.md trim |
| 5 | Add .claude/rules/epistemics.md | UNCHANGED |
| 6 | Trim CLAUDE.md + generative principle | MOVED DOWN from #1 — build replacements first |
| 7 | Create corrections register (CSV) | FORMAT CHANGED from markdown to CSV |
| 8 | Kill conditions (simplified format) | SIMPLIFIED — single-line triggers, not nested YAML |
| 9 | Open questions file | UNCHANGED |
| 10 | Pre-commit scoring.py tests (GPT-5.2 invariants) | HAS SPECIFIC INVARIANTS now |
| 11 | Autonomous loop MVP + concurrency lock + budget cap | ADDED: file lock, $30/day cap, price freshness gate |
| 12 | Drop amendment rules section | REPLACED with 1 line in CLAUDE.md |

---

## Bottom Line

The action plan's CONTENT is sound — both models validated the core ideas. The issues are:
1. **Missing safety mechanisms** in the autonomous loop (concurrency, budget, price freshness)
2. **Wrong sequencing** (build replacements before removing what they replace)
3. **Wrong format** for corrections register (CSV > markdown)
4. **Over-engineering** on amendment rules (1 line > 10 lines)
5. **Under-specified** error-correction metric (needs denominator)

None of these invalidate the plan. They're fixes, not redesigns.
