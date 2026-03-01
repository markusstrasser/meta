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
