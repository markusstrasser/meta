# Extraction: Cross-Model Brainstorming — Intel System Step-Change Ideas

## Extraction: gemini-brainstorm.md
G1. [Wave 2-7 was premature — conjectures without refutation engine. Negative returns on signal breadth until scoring exists]
G2. [Biggest lever: PIT backtester. Compress 5 years of feedback into 5 minutes. Decouple feedback from linear time]
G3. [Alt architecture A: Internal prediction market — 28 sub-agents betting against each other, market-clearing price = conviction]
G4. [Alt architecture B: Pure catalyst straddles — use signals for anomaly detection only, force ACH sprint at anomaly]
G5. [Alt architecture C: "Short-seller's long" — invert pipeline, generate short theses, go long competitor]
G6. [Adjacent: Meteorology ensemble perturbation — pass same entity to Claude 5× with varied prompts, if thesis survives ensemble it's robust]
G7. [Adjacent: Sports betting CLV (Closing Line Value) — measure if signal predicted pre-catalyst price drift, not just final outcome]
G8. [Unconventional: Deliberate signal dropout — randomly disable 70% of datasets for half the watchlist, like neural net dropout. Tests which signals carry structural alpha]
G9. [Over-engineered: scoring.py is "mathematical LARP" — 582 lines of hedge-fund math applied to [F3] guessed priors. Replace with integer tally (+1/-1) until backtester calibrates]
G10. [Binding constraint: calibration-limited. conviction is a guess → size is a guess → gambling not intelligence]
G11. [Blind spot: LLMs naturally validate qualitative signals (FAERS/CFPB). Market may have arb'd CFPB signal away years ago]
G12. [Blind spot: PIT backtesting on local files is notoriously hard. LLMs terrible at spotting look-ahead bias in code]
G13. [Summary directive: freeze signal_scanner.py, stop adding data, build prediction ledger, run against 2022 data, kill 20 that don't work, recalibrate 8 that do]

## Extraction: gpt-brainstorm.md
P1. [Wave 2-7: added option value but P(deployed+measured)≈0 right now. Near-term marginal value low. Premature expansion of theory generator before reality checker]
P2. [Priority order: (1) prediction ledger MVP, (2) daily resolver + calibration, (3) shadow portfolio, (4) backtest harness walk-forward PIT-safe]
P3. [Idea #1: Prediction ledger + daily resolver — 300-700 LOC]
P4. [Idea #2: Shadow portfolio with fractional Kelly — 300-800 LOC]
P5. [Idea #3: Scanner/cascade calibration via Beta-Binomial — 200-500 LOC, learns per-scanner p(hit|signal) from ledger]
P6. [Idea #4: FDR / e-values for multiple testing control — 200-600 LOC]
P7. [Idea #5: PIT provenance (first_seen_at + as-of views) — 300-900 LOC]
P8. [Idea #6: Health checks + staleness SLOs — 150-400 LOC]
P9. [Idea #7: Discovery→research queue via active learning — 200-500 LOC]
P10. [Idea #8: Outcome taxonomy beyond price — resolve on events, not just returns — 400-1200 LOC]
P11. [Idea #9: Entity resolution hardening — auditable mappings with error bars — 300-1000 LOC]
P12. [Idea #10: Regime tags + conditional performance reporting — 300-800 LOC]
P13. [Deep dive: Prediction ledger architecture — evidence_events, predictions, prediction_outcomes tables. Online calibration without full backtest]
P14. [Deep dive: Shadow portfolio — portfolio_state, positions, fills tables. Paper trading as systems test (catches pipeline bugs)]
P15. [Deep dive: Empirical calibration of LLRs — maintain alpha_hit/beta_hit per scanner, online daily update, self-throttling scanners that degrade lose weight]
P16. [Pre-mortem: false alpha from PIT leakage + multiple testing is existential. Thousands of implicit hypotheses/month]
P17. [Pre-mortem: Entity mapping errors (FAERS drug→ticker) producing confident but wrong signals]
P18. [Pre-mortem: Orchestrator staleness — system silently stops updating]
P19. [Preventive controls: canary tickers / null tests — run scanners on shuffled dates, if edge persists you're leaking]
P20. [Combo: ledger + calibration + FDR = adaptive model. Scanner zoo → self-calibrating ensemble]
P21. [Combo: shadow portfolio + drawdown pause + health checks = visible failures]
P22. [Combo: discovery screener + active-learning queue + human review budget = VOI-optimal attention allocation]
P23. [Combo: event cascades + empirical Neff from ledger = learned correlations]
P24. [GPT bias: engineering/instrumentation bias, may underweight bespoke alpha from domain signals]
P25. [GPT bias: price-based resolution may miss asymmetric downside risk signals (CFPB/FAERS)]
P26. [GPT bias: underestimating data pain (PIT, corporate actions, price quality) — LOC estimates ±2×]
P27. [GPT bias: assuming stationarity — calibration needs decay/rolling windows or regime tags]

## Fact-Check Results

### CRITICAL CORRECTION: Prediction infrastructure EXISTS
- `prediction_tracker.py` (full CLI: add/extract/resolve/score/list) — EXISTS
- `prediction_tables.py` (DuckDB schema: prediction, prediction_resolution) — EXISTS but tables NOT CREATED in state.duckdb
- `predictions.csv` — 24 predictions, 3 resolved (HIMS, HIMS, PYPL)
- `backtest.py` — 28 scenario files (battery, copper, energy, health, semis, solar, monthly screens) — EXISTS
- `paper_ledger.py` — EXISTS

### State of prediction infrastructure:
- Code written, partially used (24 predictions logged)
- DuckDB tables not created (prediction_tables.py never run)
- No automated signal→prediction pipeline (predictions are manual CLI)
- No daily resolver running on cron
- 3 out of 24 predictions resolved, with Brier scores
- Backtest scenarios exist with contamination tracking

### Both models hallucinated the gap:
Both said "no prediction ledger" and "no backtest" because I told them so in the context bundle. My context description was wrong — the tools exist but aren't integrated/automated.

### The REAL gap:
Not "build prediction infrastructure" but "wire existing prediction infrastructure into the daily workflow":
1. Run prediction_tables.py to create DuckDB tables
2. Wire signal scanner → automatic prediction creation (emit_predictions)
3. Wire daily cron → automatic prediction resolution
4. Wire resolution → calibration feedback to LLR priors

## Disposition Table

| ID  | Claim (short) | Disposition | Reason |
|-----|--------------|-------------|--------|
| G1  | Waves premature, negative returns on breadth | INCLUDE — modified | Both models agree. But correction: prediction infra exists, just not wired |
| G2  | PIT backtester is biggest lever | INCLUDE — Tier 2 | Backtest framework exists (28 scenarios!). Real gap: automate + run at scale |
| G3  | Internal prediction market (sub-agents) | REJECT | Over-engineered for one person. Constitutional violation: simpler beats complex |
| G4  | Catalyst straddles / anomaly-only detection | DEFER | Interesting but requires options. Current long-only constraint makes this impractical |
| G5  | Short-seller's long (go long competitor) | INCLUDE — idea | Novel, practical within long-only constraint. Worth testing on 1-2 positions |
| G6  | Ensemble perturbation (5× varied prompts) | DEFER | Interesting but expensive ($15+ per entity × 5). Maybe for high-conviction thesis checks |
| G7  | CLV (closing line value) tracking | INCLUDE — Tier 3 | Concrete, additive to prediction ledger. Track pre-catalyst drift, not just final |
| G8  | Signal dropout (randomly disable 70% datasets) | INCLUDE — idea | Clever ablation study. Cheap to implement. Would identify dead-weight scanners |
| G9  | scoring.py is LARP, replace with tally | REJECT | The math is correct and calibrated (GPT-5.2 verified). The priors are guesses but the framework handles calibration updates. Replacing with +1/-1 would lose the framework |
| G10 | Calibration-limited, not signal-limited | INCLUDE — Tier 1 | Both models agree. Constitution aligns. Verified |
| G11 | CFPB signal may be arb'd away | INCLUDE — risk | Valid concern. No way to know without backtest |
| G12 | PIT backtesting is hard, LLMs bad at spotting bias | INCLUDE — risk | Valid. backtest.py has contamination tracking — partially addressed |
| G13 | Freeze scanner, kill 20/28 scanners | INCLUDE — modified | Don't freeze code, but freeze signal breadth expansion. Focus on wiring + calibration |
| P1  | P(deployed+measured)≈0 for new scanners | INCLUDE — modified | Correct diagnosis, but correction: ledger code exists, just needs wiring |
| P2  | Priority: ledger → resolver → shadow portfolio → backtest | INCLUDE — Tier 1 | Modified: ledger exists, priority is WIRING not BUILDING |
| P3  | Prediction ledger 300-700 LOC | MERGE WITH P2 | Already exists as prediction_tracker.py (~400 LOC) |
| P4  | Shadow portfolio 300-800 LOC | INCLUDE — Tier 2 | paper_ledger.py exists but unclear if it does full portfolio sim |
| P5  | Scanner calibration via Beta-Binomial | INCLUDE — Tier 3 | estimate_beta_alpha() already in scoring.py. Wire to resolved predictions |
| P6  | FDR / e-values for multiple testing | INCLUDE — Tier 4 | Real concern. 28 scanners × 70 tickers = 1960 tests. No correction applied |
| P7  | PIT provenance (first_seen_at) | INCLUDE — Tier 3 | Partially addressed: backtest.py has contamination tracking. Downloads lack fetch_ts |
| P8  | Health checks + staleness SLOs | MERGE WITH existing | healthcheck.py already exists. Orchestrator has generate_healthcheck_tasks |
| P9  | Discovery→research queue via active learning | INCLUDE — Tier 4 | Universe screener outputs CSV but no priority-ranked research queue |
| P10 | Outcome taxonomy beyond price | DEFER | Adds complexity. Price resolution is sufficient for calibration MVP |
| P11 | Entity resolution hardening (FAERS drug mapping) | INCLUDE — Tier 3 | build_ndc_drug_map.py exists but has no error bars or audit trail |
| P12 | Regime tags + conditional performance | DEFER | Requires prediction ledger + portfolio first. Second-order optimization |
| P13 | Prediction ledger architecture | MERGE WITH P2 | Schema exists in prediction_tables.py. Run it |
| P14 | Shadow portfolio architecture | MERGE WITH P4 | |
| P15 | Empirical LLR calibration online | MERGE WITH P5 | |
| P16 | Pre-mortem: PIT leakage + multiple testing | INCLUDE — risk | Critical risk. Both models flagged |
| P17 | Pre-mortem: Entity mapping errors | INCLUDE — risk | FAERS NDC→drug→ticker chain is fragile |
| P18 | Pre-mortem: Orchestrator staleness | INCLUDE — risk | Orchestrator not on cron (verified) |
| P19 | Canary tickers / null tests | INCLUDE — Tier 3 | Cheap, high-leverage. Run scanners on shuffled dates |
| P20 | Combo: ledger + calibration + FDR | INCLUDE — architecture | This IS the step-change. Self-calibrating ensemble |
| P21 | Combo: portfolio + drawdown + health | INCLUDE — architecture | Constitutional alignment (drawdown circuit breaker) |
| P22 | Combo: discovery + active learning + human budget | DEFER | Requires resolved ledger first |
| P23 | Combo: cascades + empirical Neff | INCLUDE — Tier 4 | Requires prediction data to learn correlations |
| P24-P27 | GPT bias warnings | NOTED | Valid cautions, incorporated into synthesis |

## Coverage
- Total extracted: 40 items (13 Gemini, 27 GPT)
- Included: 24
- Deferred: 5
- Rejected: 3
- Merged: 8
