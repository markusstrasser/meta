# Extraction: Constitutional Questions Review

## Extraction: gemini-output.md

G1. "Obviousness" for autonomy threshold is subjective and unmeasurable — violates generative principle
G2. Sycophancy fix via instruction is known-failed mitigation (EoG 0%)
G3. Hook exit code binary (0 vs 2) misses Claude Code's native `ask` permission decision
G4. Skills in separate repo fractures git-based error-correction ledger
G5. Need hook regret tracking — log false positive blocks to measure if hooks save or waste tokens
G6. Autonomy gradient should be about state reversibility, not cognitive difficulty
G7. Fan-out tasks (>10 repeated ops) need MapReduce via subagents, not linear Bash execution
G8. Q1: Use "Cascading vs Epistemic" divide — hard hooks for cascading waste, Stop hooks for epistemic discipline
G9. Q2: Replace "obviousness" with testable reversibility — autonomous if stateless + has verification test
G10. Q3: Merge skills/ into meta/skills/ — Bratman's planning agency demands unified git log
G11. Priority 1: Migrate skills/ into meta/
G12. Priority 2: API-level usage limit circuit breaker (PostToolUse grep for rate limit strings)
G13. Priority 3: Replace sycophancy instructions with PreToolUse:Write hook requiring plan.md before >50 line scripts
G14. Priority 4: Hook intervention logging to ~/.claude/hook-interventions.jsonl + dashboard integration
G15. Priority 5: Subagent MapReduce rule for >10 discrete operations
G16. Constitutional violation: instruction-only sycophancy fix contradicts "error correction must be structural"
G17. Constitutional violation: separate repos for rationale and execution violates "git log is the learning"
G18. Constitutional concern: bash-loop-guard exit 2 may violate "fail open" principle
G19. Self-doubt: Gemini may underestimate symlink/path complexity in skills merge
G20. Self-doubt: hookSpecificOutput.permissionDecision:ask JSON schema may be unstable
G21. Self-doubt: friction cost of false-positive blocks at 2 AM for single operator

## Extraction: gpt-output.md

P1. Logical inconsistency: "instructions = 0% reliable" contradicts "keep things instructional for now"
P2. Autonomous self-modification without rollback contract → systematically produces reverted work
P3. Dual-objective telos (autonomy + error correction) can conflict — no reliability floor constraint
P4. Hook "fail open" principle contradicts need for deterministic enforcement of text-action gap
P5. "Meta owns skill quality" is social ownership without technical enforcement when code is separate
P6. "Not calendar-driven" research contradicts "daily cron auto-update" backlog item
P7. Q1 ROI model: Benefit ≈ f × L × p_prevent; Cost ≈ E_dev + E_friction (f × p_false+ × t_interrupt)
P8. Q1: ROI ranking: C (tiny fail-closed set) > B (warn-only hooks) > A (instruction-only)
P9. Q2 ROI ranking: B (rubric) + C (blast radius gates) together > either alone > pure judgment
P10. Q3 ROI ranking: Option 1 (separate + versioning) or Option 3 (submodule) > Option 2 (merge) > Option 4 (package)
P11. Q1-P1: Blocking deterministic invariants → ≥50% drop in ≥5 bash failure streaks within 7 days
P12. Q1-P2: Warn-only hooks → supervision waste 21%→≤18% in 14 days (requires hook decision instrumentation)
P13. Q1-P3: "Changes must be testable" won't reach ≥80% compliance via hooks (semantic predicate)
P14. Q2-P1: Self-mod rubric → ≥30% reduction in build-then-undo within 30 days
P15. Q2-P2: Human approval for global hooks/shared skills → ≥25% reduction in post-hoc vetoes in 30 days
P16. Q3-P1: Version tags + pin → median propagation time ≤1 hour
P17. Q3-P2: Merge without release mechanics → still ≥1/month stale skill incidents
P18. Goals alignment table: Mission 70%, Generative principle 55%, Primary metric 60%, Skills ownership 50%
P19. Top 5 #1: Hook ROI telemetry — log every trigger/decision/interruption to JSONL
P20. Top 5 #2: Autonomy Change Risk Score rubric + Blast Radius Gates
P21. Top 5 #3: Tiny fail-closed set chosen by expected loss (loss × frequency)
P22. Top 5 #4: Keep skills separate + formalize with version tags + per-project pin + one-command sync
P23. Top 5 #5: Instrument regret/corrections per session as first-class metric
P24. Self-doubt: EoG "0% reliable" is task-dependent, some instructions work >0%
P25. Self-doubt: Semantic failures (silent reasoning errors) can't be caught by hooks
P26. Self-doubt: Metrics can be gamed — need paired metrics (throughput + quality)
P27. Self-doubt: Submodule advice may be too production-grade for single operator
P28. Self-doubt: Quantitative estimates are priors, not posteriors — need A/B-style rollouts

## Disposition Table

| ID | Claim (short) | Disposition | Reason |
|----|--------------|-------------|--------|
| G1 | "Obviousness" unmeasurable | INCLUDE | Both models flag this (G1, P9). Core Q2 insight. |
| G2 | Sycophancy instruction-only is failed mitigation | INCLUDE | Verified — EoG evidence + improvement-log acknowledges weakness |
| G3 | Hook `ask` permission decision underused | DEFER | G20 flags JSON schema instability. Valid concept, risky implementation. |
| G4 | Separate repos fracture git ledger | INCLUDE | Valid principle (G4, G17). But weigh against P10, P17, P22. |
| G5 | Hook regret/false-positive tracking needed | INCLUDE | Both models (G5, P19). Prerequisite for progressive enforcement. |
| G6 | Reversibility > cognitive difficulty for autonomy gradient | INCLUDE | Key insight. Maps to P9 blast radius gates. |
| G7 | Fan-out >10 ops → subagent MapReduce | INCLUDE | Valid architectural pattern. Addresses failure mode 22. |
| G8 | Cascading vs Epistemic divide for hooks | INCLUDE | Good framework for Q1. |
| G9 | Testable reversibility for Q2 | INCLUDE | Strong. But "can write verification test" is itself semantic — partial solution. |
| G10 | Merge skills into meta/skills/ | MERGE WITH P10, P22 | Gemini says merge; GPT says keep separate + version. Tension. |
| G11-G15 | Gemini's priority list | MERGE WITH P19-P23 | Overlapping recommendations, synthesize below. |
| G16 | Sycophancy instruction = constitutional violation | MERGE WITH G2 | Same point. |
| G17 | Separate repos = constitutional violation | MERGE WITH G4 | Same point. |
| G18 | Bash-loop-guard may violate fail-open | INCLUDE | Worth noting. Current guard is tight. |
| G19 | Skills merge may break paths | INCLUDE | Real risk if merge pursued. |
| G20 | hookSpecificOutput JSON instability risk | INCLUDE | Validates deferring `ask` pattern. |
| G21 | False positive cost at 2 AM | INCLUDE | Core single-operator constraint. |
| P1 | Instructions=0% vs "keep instructional" tension | MERGE WITH G2 | Same insight. |
| P2 | Self-mod without rollback contract | INCLUDE | Neither model's Q2 answer fully addresses this. |
| P3 | Dual telos needs reliability floor | INCLUDE | Important. No weighting declared. |
| P4 | Fail-open vs text-action gap contradiction | INCLUDE | Need explicit carve-out for high-blast-radius tools. |
| P5 | "Owns quality" without technical enforcement = social | INCLUDE | Validated by both. |
| P6 | Research cadence vs daily cron contradiction | INCLUDE | Minor — cron backlog is future, not current. Note for consistency. |
| P7 | Hook ROI model formula | INCLUDE | Useful framework for Q1 prioritization. |
| P8 | Q1 ROI ranking | INCLUDE | Aligns with G8. |
| P9 | Q2 ROI ranking: rubric + blast radius gates | INCLUDE | Strongest Q2 recommendation from either model. |
| P10 | Q3: Keep separate + version > merge | INCLUDE | Contradicts Gemini. Both have valid points. |
| P11-P17 | Testable predictions | INCLUDE | All valuable. Some need instrumentation first. |
| P18 | Goals alignment scores | INCLUDE | Useful baseline. |
| P19-P23 | GPT top 5 recommendations | INCLUDE | Overlap with Gemini priorities; merge in synthesis. |
| P24 | EoG 0% is overstated | INCLUDE | Fair correction. Instructions work for simple predicates. |
| P25 | Semantic failures unhookable | INCLUDE | Important constraint on enforcement scope. |
| P26 | Metrics can be gamed | INCLUDE | Paired metrics needed. |
| P27 | Submodule may be overkill | INCLUDE | Validates keeping things simple. |
| P28 | Estimates are priors | INCLUDE | Good epistemic hygiene. |

**Coverage:** 28 Gemini items + 28 GPT items = 56 total. 45 INCLUDE, 7 MERGE, 3 DEFER, 1 already handled.
