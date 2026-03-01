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
