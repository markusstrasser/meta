# Cross-Model Review: Intel System Step-Change Ideas
**Mode:** Brainstorming
**Date:** 2026-02-28
**Models:** Gemini 3.1 Pro, GPT-5.2
**Constitutional anchoring:** Yes (CONSTITUTION.md, GOALS.md)
**Extraction:** 40 items extracted, 24 included, 5 deferred, 3 rejected, 8 merged

## Was Wave 2-7 Smart?

**Both models agree: premature.** But both also hallucinated the severity.

The real diagnosis: You built 4 new scanners and event cascades (976 LOC, well-tested) when the prediction tracker, backtest framework, and paper ledger **already existed** but weren't wired into the daily workflow. The prediction_tracker.py has 24 predictions with 3 resolved. The backtest.py has 28 scenarios. prediction_tables.py has the DuckDB schema but it was never run.

**The wave wasn't wrong — the sequencing was wrong.** Expanding signal breadth before activating the existing feedback loop violates the generative principle: "maximize error-correction rate." The error-correction machinery EXISTS. It's just dormant.

## Verified Findings (adopt)

| Priority | Finding | Source | Verified How |
|----------|---------|--------|-------------|
| **Tier 1** | System is calibration-limited, not signal-limited. Freeze signal expansion. | G1, G10, P1, P2 | Both models converge. 24 predictions, 3 resolved. No daily resolver. No cron. |
| **Tier 1** | Wire existing prediction infra into daily workflow: (1) run prediction_tables.py, (2) auto-create predictions from signal scanner, (3) daily resolver on cron, (4) calibration feedback to LLR priors | P2, P3, P13, P20 | prediction_tracker.py exists. prediction_tables.py exists. resolver logic exists. None automated. |
| **Tier 2** | Build shadow portfolio (paper trading) from predictions. Track NAV vs IWM. | P4, P14, P21 | paper_ledger.py exists but doesn't do full portfolio sim. Constitution requires this (Principle 9: portfolio is scorecard). |
| **Tier 2** | Automate backtest at scale — run 28 scanners against 2022-2024 data, score, kill underperformers | G2, G13 | backtest.py exists with 28 scenarios. Has PIT contamination tracking. Never run systematically against all scanners. |
| **Tier 3** | Empirical LLR calibration — learn per-scanner hit rates from resolved predictions, auto-update priors | P5, P15, P20 | estimate_beta_alpha() in scoring.py. Not wired to ledger data. Online update is ~200 LOC. |
| **Tier 3** | CLV (Closing Line Value) tracking — measure pre-catalyst price drift, not just final outcome | G7 | Novel metric. Additive to prediction_outcomes table. Would distinguish "knew before the market" from "lucky on earnings." |
| **Tier 3** | Signal dropout ablation — randomly disable 70% of scanners, measure if Brier score degrades | G8 | Cheap experiment. No code change needed — just run scanner with subset. Would identify dead-weight scanners. |
| **Tier 3** | Canary tickers / null tests — run scanners on shuffled dates or random tickers | P19 | If "edge" persists on randomized data, you're leaking. <100 LOC to implement. |
| **Tier 3** | Entity resolution hardening — FAERS NDC→drug→ticker mapping has no audit trail or error bars | P11, P17 | build_ndc_drug_map.py creates the mapping. No confidence scores. Mapping errors → confidently wrong signals. |
| **Tier 4** | FDR / e-values for multiple testing control | P6, P16 | 28 scanners × 70 tickers = 1960 implicit tests. No multiple testing correction. Risk of false discoveries. |

## The Step-Change Architecture (P20)

Both models independently converge on the same architecture. This is the unifying change:

```
Signal Scanner → Prediction Ledger → Daily Resolver → Calibration
     ↑                                                    ↓
     └────── Updated LLR priors ←── Per-scanner hit rates ┘
```

This closes the error-correction loop. Currently the loop is open: signals fire → CSV → human reads → maybe acts. The closed loop:

1. Scanner fires signal (existing)
2. If posterior > threshold → auto-create prediction with entry price, horizon, confidence (NEW: wire emit_predictions)
3. Daily cron resolves expired predictions against actual prices (NEW: wire resolve_predictions)
4. Resolution data feeds per-scanner calibration → updates p_hit_h1/p_hit_h0 (NEW: ~200 LOC)
5. Scanners that degrade automatically lose weight (self-throttling)

**Effort:** ~500 LOC new code + wiring of ~800 LOC existing code.
**Impact:** Transforms the system from a "theory generator" to an "error-correction engine" (the stated goal).

## Novel Ideas Worth Pursuing

| Idea | Source | Why it's interesting |
|------|--------|---------------------|
| **Short-seller's long** — generate short theses, go long the competitor | G5 | Works within long-only constraint. Pharma especially: if FAERS kills drug X, competitor Y benefits. |
| **Signal dropout** — neural-net-style ablation to test which scanners carry alpha | G8 | Cheap, revealing, no code change. Could eliminate 10+ scanners. |
| **CLV tracking** — did the signal predict price BEFORE the catalyst, not just after? | G7 | Separates signal quality from luck. Key metric for alpha-vs-beta attribution. |
| **Canary tickers** — run scanners on shuffled data as null hypothesis test | P19 | If edge persists on random data → you're measuring noise. Essential sanity check. |

## Deferred (with reason)

| ID | Finding | Why Deferred |
|----|---------|-------------|
| G4 | Catalyst straddles | Requires options, currently deferred per GOALS.md |
| G6 | Ensemble perturbation (5× thesis) | Expensive. Maybe for high-conviction positions only |
| P10 | Outcome taxonomy beyond price | Adds complexity. Price resolution sufficient for MVP |
| P12 | Regime tags + conditional performance | Second-order. Requires ledger + portfolio first |
| P22 | Active learning for discovery queue | Requires resolved ledger to compute uncertainty |

## Rejected (with reason)

| ID | Finding | Why Rejected |
|----|---------|-------------|
| G3 | Internal prediction market (28 sub-agents) | Over-engineered for one person. Violates "simpler beats complex" evidence base |
| G9 | Replace scoring.py with +1/-1 tally | The math IS correct. Replacing calibrated LLR framework with a tally would lose the ability to do automatic calibration updates. The priors are guesses now but the framework handles learning |
| P8 | Health checks + staleness SLOs | Already exists (healthcheck.py, orchestrator healthcheck tasks) |

## Where Both Models Were Wrong

| Claim | Reality | Who Caught It |
|-------|---------|--------------|
| "No prediction ledger exists" | prediction_tracker.py exists with 24 predictions, 3 resolved | Fact-check against codebase |
| "No backtest exists" | backtest.py exists with 28 scenarios and PIT contamination tracking | Fact-check against codebase |
| "No paper trading" | paper_ledger.py exists | Fact-check against codebase |
| "Build X from scratch" (both models) | The code exists but isn't wired. The gap is integration, not creation | Fact-check |

**Root cause of hallucination:** My context bundle said "What's NOT Built Yet: No prediction ledger, No backtest, No paper trading." Both models trusted my description. **Lesson: never trust the prompt author's claims about absence — verify.**

## Gemini Errors (distrust)

| Claim | Why Wrong |
|-------|-----------|
| "scoring.py is a mathematical LARP" | The math was verified by GPT-5.2 (analysis/llm_checks/math_*.md). The framework is sound even if current priors are estimates. Discarding it would throw away calibration infrastructure |
| "Replace with integer tally" | Would lose: PIT normalization, Neff discount, crowding adjustment, Empirical Bayes — all of which are correct and tested |
| "Marginal alpha of uncalibrated signal is zero" | Wrong: a properly specified but uncalibrated signal still has informational value if the direction is correct. It's overconfident, not uninformative |

## GPT Errors (distrust)

| Claim | Why Wrong |
|-------|-----------|
| LOC estimates (300-700 for ledger) | The code already exists (~400 LOC). Actual new code needed is ~200 LOC for wiring + cron |
| "Build from scratch" framing throughout | Should have qualified "verify existing code first" — engineering bias toward greenfield |

## Revised Priority List

1. **Run prediction_tables.py** — create DuckDB tables in state.duckdb (5 min)
2. **Wire signal scanner → emit_predictions** — auto-create predictions when posterior > threshold (~200 LOC)
3. **Set up daily resolver on cron** — resolve expired predictions against prices (~100 LOC + crontab)
4. **Per-scanner calibration report** — Brier score and hit-rate by scanner type (~200 LOC)
5. **Calibration feedback loop** — update p_hit_h1/p_hit_h0 from resolved data (~200 LOC)
6. **Shadow portfolio** — extend paper_ledger.py to track NAV, drawdown, IWM comparison (~400 LOC)
7. **Canary tickers / null test** — sanity check: run scanners on shuffled dates (~100 LOC)
8. **Signal dropout ablation** — test which scanners carry alpha (experiment, no code)
9. **CLV metric** — add pre-catalyst price drift tracking to prediction_outcomes (~100 LOC)
10. **FDR control** — Benjamini-Hochberg on signal alerts per week (~200 LOC)
