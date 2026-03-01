# CONTEXT: Cross-Model Brainstorming — Intel Investment Research System

## PROJECT CONSTITUTION
Generative principle: "Maximize the rate at which the system corrects its own errors about the world, measured by market feedback."
Key principles: every claim sourced/graded (NATO Admiralty), quantify before narrating, fast feedback over slow, the join is the moat, portfolio is the scorecard, falsify before recommending, size by fractional Kelly (f=0.25, max 20% per position, -15% drawdown pause, -25% human re-auth).

## PROJECT GOALS
$500M-$5B market cap small/mid-cap companies. Benchmark: Russell 2000 (IWM). Success: alpha vs IWM, Sortino >1.5, calibration curve (70% predictions resolve at ~70%). FDA FAERS, CFPB velocity, gov contract surprise, cross-domain governance signals, insider filing delay — ranked by expected value.

## Current System
- 28 signal scanners producing LLR-scored signals across insider, price, SEC, options, alt-data, macro, congressional, fraud domains
- Bayesian fusion: LLR sum + prior log-odds → posterior. Crowding discount (0.6×) for mechanical signals. Neff discount for correlated signals. Event cascades (9 defined).
- Discovery mode: scans ALL tickers, not just watchlist (~70 tickers)
- Orchestrator: autonomous task loop, claude -p per task, $30/day budget
- 141+ datasets, 212GB, DuckDB 295 views
- Entity files per ticker with YAML frontmatter, staleness detection
- Scoring: pit_normalize → llr_from_percentile (Beta(0.5,1)), llr_boolean, fuse_evidence, neff_discount, eb_shrink_rate, source_llr

## Just Built (Wave 2-7): 976 insertions, 8 files
1. CFPB velocity scanner (z-score on 3-month complaint velocity vs 12-month trailing)
2. FAERS velocity scanner (same pattern, adverse events per ticker via NDC drug→ticker mapping)
3. Universe screener ($500M-$5B, scored by signal source coverage)
4. Gov contract surprise (USAspending awards as % of revenue, tiers at 5/10/20%)
5. Insider filing delay (Form 4 gap > 3 calendar days, tiers at 5/10/10+ days)
6. 4 new event cascades: FAERS+insider, CFPB+insider, filing_delay+8K, FAERS+trial_halt
7. 2 consensus groups: regulatory_risk_{ticker} (CFPB+courts), drug_safety_{ticker} (FAERS+trial halts)

## Critical Gaps
1. **No prediction ledger** — signals fire but predictions aren't tracked against outcomes. Constitution says "portfolio is the scorecard" but there's no scorecard.
2. **No backtest** — LLR priors are estimates [F3], not calibrated. No confusion matrix. No historical accuracy data.
3. **No paper trading** — no live market validation. The entire system is untested against market reality.
4. **Orchestrator not running** — built but not deployed to cron. Entity files get stale.
5. **LLR calibration** — all p_hit_h1/p_hit_h0 values are guesses. estimate_beta_alpha() exists but isn't wired to historical data.
6. **No portfolio optimization** — Kelly sizing formula exists in CONSTITUTION but no implementation. No position tracking. No P&L.
7. **Discovery→thesis pipeline** — universe screener outputs CSV but doesn't feed back into research prioritization.
8. **No point-in-time safety** — downloads lack first_seen_date. PIT violations possible.
9. **No FDR control** — running 28 scanners × ~70 tickers = thousands of implicit hypothesis tests per month. No multiple testing correction.

## Evidence Base
- Instructions alone = 0% reliable (EoG). Architecture > rules.
- Consistency flat over 18 months (Princeton). Need retry/majority-vote.
- Simpler beats complex under stress (ReliabilityBench).

## Constraints
- One person, no team, no cloud, no budget for data vendors
- MacBook 18GB RAM, 1TB SSD. DuckDB (single-writer, no concurrent).
- Free public data only (SEC EDGAR, CMS, FAERS, USAspending, FRED, etc.)
- No options/shorts/leverage until paper trading demonstrates edge
- All code runs via `uvx --with duckdb` (no persistent Python env)
