Below are **silent failure modes** that make the engine *look* like it’s learning/working while it’s actually leaking edge, fabricating edge, or accumulating hidden risk. I’m assuming: quarterly universe reconstitution, 50–100 datasets, ~50 signals, and a concentrated book with human execution.

**Scales**
- **Severity (S 1–5):** 1 = nuisance, 3 = meaningfully negative EV, 5 = can blow up / permanently damage strategy.
- **Detectability (D 1–5):** 1 = obvious quickly, 3 = shows up after a few quarters, 5 = can persist for years.
- Where I quantify, I’ll use order-of-magnitude numbers (you should plug in your actual turnover, AUM, ADV constraints, and holding periods).

---

## 1) Statistical Traps

### 1.1 **Universe Reconstitution Survivorship**
- **Mechanism:** You define the target universe as `$500M–$5B market cap` but use *today’s* membership (or any post-period membership) when training/evaluating. Companies that fell below $500M due to bad outcomes get dropped, so the model “learns” from survivors. This inflates hit-rate and suppresses drawdowns in backtests. It also biases signal weights toward “things that happen in winners.”
- **S:** 5 (turns negative-EV ideas into “validated” edge; can destroy most of your Sharpe)
- **D:** 5 (can look great for years; only obvious after live PnL disappoints)
- **Defense (architectural):**  
  - Maintain a **point-in-time universe table**: `universe_membership(date, perm_id, in_universe_bool, reason)` computed using only data available as-of that date.  
  - Enforce in code: every feature row must join to `universe_membership` **as-of feature timestamp**, never “current”.
  - Add a unit test: “No training example includes a name that entered the universe after the example date.”

### 1.2 **Delisting / Corporate Action Return Omission**
- **Mechanism:** Small/mid caps frequently delist, get acquired, reverse merge, go to OTC. If your label is based on CRSP-like total return but you’re using “available Yahoo prices” (or missing last prints), you systematically omit the worst outcomes (or mis-handle acquisition premia). The model learns wrong base rates and mis-sizes tail risk.
- **S:** 5 (silent blow-ups; systematically understated left tail)
- **D:** 4 (manifests as “why are live losers worse than backtest losers?”)
- **Defense:**  
  - Use a **survivor-bias-free price/return source** (CRSP/Refinitiv) or explicitly model delisting outcomes via corporate actions feed.  
  - Implement `total_return(price, dividends, delisting_cash, exchange)` and hard-fail if delisting status unknown for labels.
  - Add a “missing label audit”: fraction of examples with missing forward returns must be ~0; if not, block training.

### 1.3 **Reporting Lag Look-Ahead (Government/Healthcare)**
- **Mechanism:** Many datasets have **publication lag + event-date backfill** (e.g., FAERS case received vs event date; FPDS action date vs posted date; enforcement actions updated retroactively). If you join on event date rather than *first-public date*, you leak information that wasn’t known at trade time.
- **S:** 5 (creates phantom alpha)
- **D:** 5 (very hard to notice without rigorous “as-of” discipline)
- **Defense:**  
  - Every record needs two timestamps: `event_date` and **`first_seen_date`** (when your pipeline first observed it). Trading features must use `first_seen_date <= decision_time`.  
  - Store immutable raw snapshots by fetch time (content-addressed). Recompute “as-of” features from snapshots.

### 1.4 **Restatement / Amendment Leakage (SEC Filings)**
- **Mechanism:** 10-K/A, 8-K amendments, XBRL taxonomy changes, late corrections. If you pull “latest filing” or “latest XBRL fact” you accidentally use corrected values that weren’t known when the market priced the original filing.
- **S:** 4
- **D:** 4
- **Defense:**  
  - A **filing version graph** keyed by accession number; features must reference a specific accession and its acceptance timestamp.  
  - For any XBRL fact, persist `(fact, filing_accession, extracted_at)`; never “latest”.

### 1.5 **Multiple Comparisons / False Discovery Flood**
- **Mechanism:** 50 signals × 100 entities × (time windows, thresholds, transformations) easily becomes **5,000–50,000 implicit hypotheses**. Even at 5% significance, you expect **250–2,500 false “edges”** per evaluation cycle. The system then “learns” weights on noise and produces confident theses.
- **S:** 5 (systematically negative EV with high conviction)
- **D:** 3–5 (can look good briefly; degrades out-of-sample)
- **Defense:**  
  - Apply **FDR control** (Benjamini–Hochberg) or hierarchical Bayesian shrinkage on signal efficacy.  
  - Enforce a **research registry**: new signal definitions must be “frozen” and evaluated on a *forward* holdout window before entering production.  
  - Use **purged/embargoed walk-forward CV** (Lopez de Prado style) to reduce leakage via overlapping labels.

### 1.6 **Outcome-Conditioned Feature Engineering (Subtle P-Hacking)**
- **Mechanism:** The AI coding agent iterates: “this signal didn’t work → tweak thresholds/windows → re-test,” implicitly conditioning on outcomes. Even if you don’t *intend* to overfit, the loop is a hyperparameter search driven by the same historical sample.
- **S:** 5
- **D:** 4 (shows up as live decay; looks like “regime change”)
- **Defense:**  
  - Split data into **(train, validation, “quarantine” test)** where the quarantine set is never touched until a monthly/quarterly “release”.  
  - Track **experiment lineage**: every code change must log which data partitions were viewed and which metrics were used for acceptance (prevents silent iterative overfit).

### 1.7 **Base-Rate Neglect (Anomaly ≠ Predictive)**
- **Mechanism:** “Anomaly detected” gets treated as “expected to move.” In reality most anomalies are: data noise, coverage artifacts, sector-wide shocks, or mean-reverting attention blips. If the true base rate is, say, **52% directional accuracy with weak magnitude**, your concentrated sizing turns tiny edge into big drawdowns once costs/slippage hit.
- **S:** 4–5 (especially in small caps)
- **D:** 3
- **Defense:**  
  - Maintain explicit **base-rate dashboards**: for each anomaly type, track `P(move)`, `P(direction correct)`, and expected `E[return | signal]` net of costs.  
  - Force all theses to include a **prior** and a posterior update (Bayesian framing), not just “signal fired”.

---

## 2) Correlation and Concentration Risk

### 2.1 **Liquidity-Adjusted Kelly Fallacy**
- **Mechanism:** Fractional Kelly assumes you can rebalance at modeled prices. In $500M–$5B names, the relevant constraint is **ADV and market impact**, especially during stress when liquidity evaporates. A “10% weight” might be **multiple days of volume**; exiting converts a paper loss into a realized air pocket.
- **S:** 5 (can create catastrophic drawdowns in a single unwind)
- **D:** 2–3 (you notice when you try to trade; but damage already done)
- **Defense:**  
  - Position sizing must be **liquidity-first**: cap by `%ADV` (e.g., 10–20% ADV over N days) and stress ADV haircuts (e.g., 50–80% reduction).  
  - Embed an **impact model** into sizing: expected slippage + adverse selection; Kelly uses *net* returns with impact.  
  - Pre-trade “can I exit in 3 days at 95% confidence?” gate.

### 2.2 **Latent-Factor Double Counting (Pseudo-Independent Signals)**
- **Mechanism:** “Insider selling”, “CFPB complaints”, “charge-offs”, “late payments”, “short interest” may all spike together due to a single macro factor (rates/credit). The engine counts them as independent evidence, inflating conviction and sizing right when correlations are highest.
- **S:** 5
- **D:** 4 (only obvious when many “uncorrelated” bets lose together)
- **Defense:**  
  - Build a **signal covariance model**: estimate correlation of signals *conditional on regimes* (risk-on/off, vol quartiles).  
  - Use **evidence aggregation** that penalizes redundancy (e.g., Bayesian model with latent factors; or shrink weights when signals cluster).  
  - Enforce portfolio constraints on **effective number of bets** (ENB) rather than count of positions.

### 2.3 **Sector/Policy Shock Correlation**
- **Mechanism:** A reporting rule change (FDA, CMS coding update, CFPB portal changes) causes a sector-wide shift that looks like many company-specific anomalies. You end up concentrated in one sector with a “strong multi-signal” story that is actually a measurement artifact.
- **S:** 4–5
- **D:** 3–4
- **Defense:**  
  - Dataset-level **structural break detectors**: monitor aggregate counts/ratios over time; alert on step changes.  
  - Require anomalies be evaluated **relative to sector peers** and **relative to dataset-wide baselines** (difference-in-differences style).  
  - Hard sector caps + “same-data-source exposure” caps.

### 2.4 **Short Borrow / Recall / Squeeze Risk**
- **Mechanism:** In small/mid caps, borrow availability and cost are unstable. A correct thesis can still lose money if borrow cost spikes, shares get recalled, or a squeeze forces buy-in. This is not in your signal model but dominates realized PnL tails.
- **S:** 5
- **D:** 2 (shows quickly once you scale; but not in backtest)
- **Defense:**  
  - Integrate **borrow data** (utilization, cost, locate availability) into idea eligibility and sizing.  
  - “Short feasibility” checks: max borrow cost, min availability, and squeeze risk proxy (SI%float, lend concentration).

### 2.5 **Hidden Beta / Factor Crowding**
- **Mechanism:** Many anomaly strategies unintentionally load on small/value/quality/momentum. In certain regimes (e.g., sharp risk-off), factor moves swamp idiosyncratic edge. Your engine thinks it’s selecting idiosyncratic opportunities but is actually running a factor book.
- **S:** 4–5
- **D:** 4
- **Defense:**  
  - Daily/weekly **factor attribution** (e.g., Barra-style or simpler: size, value, momentum, profitability, beta, sector).  
  - Constrain exposures and size trades by **marginal factor contribution**.

### 2.6 **Event Clustering (Earnings/Guidance Overlap)**
- **Mechanism:** Signals fire around the same calendar times (earnings season, FDA meetings, budget cycles). Positions cluster temporally, increasing gap risk and correlation exactly when volatility is highest.
- **S:** 4
- **D:** 3
- **Defense:**  
  - Calendar-aware risk: cap gross exposure within ±X days of earnings/known catalysts unless explicitly modeled.  
  - Run **jump risk stress tests** (e.g., -30% overnight moves) for small caps.

---

## 3) Data Quality Failures

### 3.1 **Schema Drift Masquerading as “Real Signal”**
- **Mechanism:** Column rename, new category, changed encoding, revised definitions. Your parser silently maps unknowns to NULL/0, producing discontinuities that look like anomalies (or suppress anomalies).
- **S:** 4
- **D:** 3 (might be noticed only after performance drifts)
- **Defense:**  
  - Strong **schema contracts**: expected columns/types/ranges; pipeline fails closed on deviations.  
  - “Data diff” CI: for each ingest, compute distribution summaries and compare to rolling history; alert on KL-divergence/PSI.

### 3.2 **Staleness Interpreted as Absence**
- **Mechanism:** FAERS, CMS, enforcement actions often have multi-month lags. If you treat missing recent records as “no incidents,” you create a false safety signal.
- **S:** 4
- **D:** 4
- **Defense:**  
  - Track **dataset freshness** (last update date; expected cadence).  
  - Features must be computed with **availability-aware missingness** (e.g., if lag window not complete, label feature as “unknown” and block decisions depending on it).

### 3.3 **Retroactive Backfill / Silent Revisions**
- **Mechanism:** Government datasets frequently revise prior periods. If your DuckDB table is “latest state,” your backtests unknowingly use revised history unavailable at the time. This is a subtle look-ahead.
- **S:** 5
- **D:** 5
- **Defense:**  
  - Immutable **snapshot storage** keyed by download timestamp; feature computation uses snapshots strictly up to as-of.  
  - Maintain “record first seen” and “record last changed” fields.

### 3.4 **Entity Resolution Collisions (Phantom Signal Fusion)**
- **Mechanism:** Ticker changes, CIK changes, subsidiaries, acquisitions. Two companies get merged in your entity graph, so complaints/FAERS/contracts for one bleed into another. This creates convincing but false multi-source confirmation.
- **S:** 5 (can generate high-conviction wrong-way trades)
- **D:** 4 (hard to detect because evidence looks consistent)
- **Defense:**  
  - Use **stable entity IDs** (PERMNO/LEI when possible).  
  - Entity resolution should be probabilistic with **confidence scores**; downstream features must respect uncertainty (don’t hard-join at low confidence).  
  - Build an “entity audit UI” showing all linked identifiers and top contributing records.

### 3.5 **Coverage Bias = “Clean” Bias**
- **Mechanism:** Some datasets are inherently about certain business models (CFPB → consumer finance; FAERS → drug exposure; CMS → Medicare-heavy providers). Absence of records isn’t evidence of absence; it’s often “not in domain.”
- **S:** 4
- **D:** 4
- **Defense:**  
  - For each dataset, define an explicit **eligibility map**: which industries/business models are expected to appear.  
  - Only interpret “no records” as informative when eligibility is high; otherwise treat as missing/irrelevant.

### 3.6 **Unit/Scale Errors That Don’t Crash**
- **Mechanism:** Dollars vs thousands, counts vs rates, per-quarter vs annual, share count splits. These errors often create stable but wrong signals (e.g., “contract spend spiked 1000×”).
- **S:** 4
- **D:** 3
- **Defense:**  
  - Range checks + invariants (e.g., revenue/market cap sanity; complaint rates per customer bounds).  
  - Cross-validate key metrics against independent sources (two-source reconciliation for high-impact features).

---

## 4) Adversarial Manipulation

### 4.1 **Complaint/Portal Gaming**
- **Mechanism:** Companies can improve apparent CFPB “response rate” metrics without improving underlying customer harm (template responses, pushing arbitration, channel shifting to non-reportable routes). Or competitors/activists can coordinate complaint floods.
- **S:** 3–4 (can create wrong-way trades in consumer names)
- **D:** 4 (looks like genuine sentiment shift)
- **Defense:**  
  - Use robust complaint features: weight by **resolution type**, text embeddings novelty, and abnormal complainant patterns (burstiness, geographic clustering).  
  - Detect manipulation: outlier detection on complaint composition, not just count.

### 4.2 **FAERS Reporting Strategy / Channel Shifting**
- **Mechanism:** Manufacturers and providers can change reporting practices (stimulate or suppress reports), or publicity events cause reporting bursts unrelated to incidence (“notoriety bias”). The dataset is not a clean incidence measure.
- **S:** 4
- **D:** 4
- **Defense:**  
  - Model FAERS with **notoriety controls**: include media volume, label changes, and class-wide reporting trends.  
  - Prefer features like **disproportionality metrics** (PRR/ROR) computed point-in-time with appropriate lag handling rather than raw counts.

### 4.3 **Insider Trading Evasion (10b5-1 / Trusts / Related Parties)**
- **Mechanism:** Visible insider selling can be moved to plans, family entities, or indirect vehicles that aren’t captured in your “insider sells” dataset; or the opposite—cosmetic insider buys to pump.
- **S:** 3–4
- **D:** 4
- **Defense:**  
  - Enrich insiders with relationship graphs (officer/director/10% owner + linked entities) and detect **plan adoption timing** (new 10b5-1 plans right before bad news).  
  - Downweight insider signals absent corroboration from harder-to-game fundamentals.

### 4.4 **Government Contract “Priced Before Posting”**
- **Mechanism:** Award decisions are known to participants well before FPDS updates. By the time it hits your pipeline, price already moved. Backtests that use action date (or revised FPDS) will overstate edge.
- **S:** 4
- **D:** 3–5
- **Defense:**  
  - Use **first_seen_date** strictly; estimate average lead/lag and require a minimum “freshness alpha window.”  
  - Compare to intraday/short-horizon price reaction around *your observed release time*; if no reaction, treat as mostly priced.

### 4.5 **Political Signal Alpha Decay (Crowding)**
- **Mechanism:** Congressional trades and politician portfolios become widely followed; any exploitable drift compresses. Signals persist in your model because of historical performance but are dead now.
- **S:** 3–4
- **D:** 4
- **Defense:**  
  - Continuous **alpha decay tests**: rolling out-of-sample efficacy with changepoint detection.  
  - Automatic “sunsetting”: if a signal underperforms for N windows, it gets gated off until re-validated.

### 4.6 **Small-Cap Spoofing of Public Signals**
- **Mechanism:** In thin names, actors can create optical anomalies (press releases timed to reporting windows, micro-contract announcements, minor enforcement settlements) to attract quant flows. Your system might be a predictable buyer/seller after “anomaly thresholds.”
- **S:** 4
- **D:** 5 (very hard to prove; looks like normal noise)
- **Defense:**  
  - Avoid deterministic thresholds; use **randomized execution timing** and robust anomaly scoring less sensitive to single prints.  
  - Monitor “post-signal adverse selection”: do returns reverse immediately after your typical entry window?

---

## 5) The Meta-Failure: Learning the Wrong Lessons

### 5.1 **Goodharted Learning Objective (Market Feedback ≠ Truth)**
- **Mechanism:** “Correcting errors about the world measured by market feedback” conflates: (a) being right about fundamentals, (b) market microstructure timing, (c) factor moves, (d) sentiment. The system can learn to optimize for *predictable short-term reactions* rather than truth—especially if evaluation horizon is short/variable.
- **S:** 5 (you become a noisy momentum/reversal trader unintentionally)
- **D:** 4
- **Defense:**  
  - Define explicit **prediction targets** and horizons per signal (e.g., 5d reaction vs 90d fundamental drift).  
  - Use **multiple resolution criteria**: market return + subsequent fundamental confirmation (earnings revision, enforcement outcome, guidance change).  
  - Separate “truth learning” models from “trade timing” models.

### 5.2 **Credit Assignment Error (PnL Attribution Wrong)**
- **Mechanism:** With a concentrated book, PnL is dominated by idiosyncratic jumps and factor shocks. Updating signal weights based on raw trade outcomes is essentially updating on noise. You reinforce luck and punish good signals that were unlucky in a bad tape.
- **S:** 5
- **D:** 4
- **Defense:**  
  - Do weight updates on **risk-adjusted residual returns**: remove factor/sector/beta; evaluate signal on idiosyncratic component.  
  - Use **Bayesian updating with strong priors** + shrinkage; cap per-quarter weight changes.

### 5.3 **Right-Censoring / Delayed Resolution**
- **Mechanism:** Many theses resolve over months/years (regulatory actions, product safety). If you mark outcomes too early, you label true positives as false (or vice versa), corrupting learning.
- **S:** 4
- **D:** 4
- **Defense:**  
  - For each thesis type, define a **minimum resolution time** and a survival-analysis approach (censoring-aware).  
  - Don’t update weights until resolution criteria met; keep “pending” bucket.

### 5.4 **Narrative Post-Mortem Bias**
- **Mechanism:** Humans (and LLMs) generate plausible stories after the fact, then encode them as rules. Random outcomes get rationalized into systematic changes, creating rule-bloat and overfit.
- **S:** 4
- **D:** 5 (accumulates slowly; system becomes brittle)
- **Defense:**  
  - Post-mortems must be **structured and pre-committed**: checklist of falsifiable causes (data error, timing, factor shock, thesis invalid).  
  - Require that any new rule be tested on a forward holdout and include an expected lift with uncertainty bounds.

### 5.5 **Selective Memory (Killing Losers in the Research Log)**
- **Mechanism:** Failed signals quietly removed or redefined, so the research record only contains survivors. The system “improves” on paper while true discovery rate is low.
- **S:** 5
- **D:** 5
- **Defense:**  
  - Immutable **experiment registry**: every attempted signal gets logged with definition hash, dates, and results.  
  - Track a “research hit-rate” KPI: fraction of ideas that survive forward validation.

### 5.6 **Non-Stationary Targets (Benchmark Drift)**
- **Mechanism:** If labels are “beat SPY” or “beat sector,” your objective moves with volatility and dispersion regimes. You may conclude a signal died when dispersion collapsed (or “works” when dispersion expanded).
- **S:** 3–4
- **D:** 4
- **Defense:**  
  - Normalize performance by **opportunity set**: expected cross-sectional dispersion, volatility, and liquidity.  
  - Evaluate signals in **regime buckets**; only compare like-with-like.

---

## 6) Regime Blindness

### 6.1 **Liquidity Regime Shift (Small Caps Get Abandoned)**
- **Mechanism:** In tightening cycles or crises, small-cap liquidity and breadth collapse; bid-ask widens, gaps increase, correlations spike. Strategies reliant on “exitability” fail even if signals remain directionally correct.
- **S:** 5
- **D:** 2–3 (you’ll see slippage and gapping quickly)
- **Defense:**  
  - Real-time **liquidity regime indicators**: spreads, ADV trend, market depth proxies, Russell 2000 liquidity metrics.  
  - Automatic de-risking: reduce gross and single-name caps when liquidity regime worsens.

### 6.2 **Correlation Regime Shift (Everything Becomes One Trade)**
- **Mechanism:** In stress, cross-asset and cross-sector correlations rise; your “diversified” book becomes one macro bet. Signal independence assumptions break.
- **S:** 5
- **D:** 3
- **Defense:**  
  - Monitor realized correlation of portfolio constituents and of signals; constrain **portfolio effective correlation**.  
  - Stress test with historical crisis covariance; cap exposure when correlation > threshold.

### 6.3 **Rates/Inflation Regime (Valuation and Discounting Rewrite)**
- **Mechanism:** Many mid-cap theses implicitly depend on low discount rates (growth duration). A rates shock can dominate micro signals; what “should” happen from your anomaly doesn’t matter near-term.
- **S:** 4
- **D:** 3–4
- **Defense:**  
  - Add explicit macro conditioning: performance of each signal vs rates/credit spreads.  
  - If sensitivity is high, gate signals or hedge duration/credit exposure.

### 6.4 **Regulatory/Data Generation Change**
- **Mechanism:** The fundamental meaning of a dataset changes (new enforcement priorities, new CMS billing rules, new FAERS format, SEC disclosure changes). The model treats it as the same distribution.
- **S:** 4–5
- **D:** 4
- **Defense:**  
  - Dataset drift detectors + changepoint detection on key aggregates.  
  - Version your feature definitions by **dataset regime**; retrain only within consistent regimes.

### 6.5 **Alpha Decay from Crowding / Dissemination**
- **Mechanism:** Once a public-data signal becomes widely used, its edge compresses or reverses (signal becomes a contrarian indicator). Your learner keeps weight because historical backtests dominate.
- **S:** 4
- **D:** 4
- **Defense:**  
  - Rolling forward performance with **half-life tracking**; if decay detected, reduce weight automatically.  
  - Penalize signals whose efficacy is concentrated in early history.

### 6.6 **Microstructure Regime (Tick sizes, halts, retail flow)**
- **Mechanism:** Small caps are sensitive to venue behavior, halts, limit up/down, retail option flow. Your “fundamental anomaly” can be overwhelmed by flow-driven dynamics.
- **S:** 4
- **D:** 3
- **Defense:**  
  - Add microstructure-aware constraints: avoid names with frequent halts, extreme retail flow proxies, or persistent wide spreads.  
  - Separate “slow fundamental” from “fast flow” books; don’t mix sizing logic.

---

# Cross-Cutting Silent Failure: “Single-Mac Research Constraints” (Non-crash version)
### **Implicit Sampling / Truncation**
- **Mechanism:** Because it’s heavy to recompute everything locally, the operator starts running partial refreshes, sampling entities, caching intermediate tables, or only reprocessing “interesting” names. This creates untracked selection bias and breaks reproducibility (“it worked on my cached subset”).
- **S:** 4
- **D:** 5
- **Defense:**  
  - Make the pipeline **deterministic and fully replayable** from raw snapshots.  
  - Track data lineage hashes: every model run logs exact input snapshot IDs and row counts per dataset.  
  - Block training if any dataset is “partial” unless explicitly flagged and handled.

---

## A quantitative “sanity frame” you should bake in (to prevent self-deception)
1. **False discovery expectation:** if you effectively test 10,000 hypotheses/month, expect ~500 false positives at 5% unless you control FDR.  
2. **Resolution rate constraint:** concentrated portfolio might generate ~10–30 “resolved” theses/quarter. That is *nowhere near enough* to update dozens of weights aggressively without overfitting.  
3. **Liquidity constraint:** if your position is >20% of 20-day average daily dollar volume, assume you cannot exit in stress without multi-% impact; Kelly must be capped by liquidity.

---

## If you want, I can turn this into a concrete checklist + schema
If you share:
- your current universe construction,
- how you timestamp records (event date vs ingest date),
- how you label outcomes (horizon, benchmark),
- and your sizing + liquidity assumptions,

…I can propose a **specific data model** (tables/fields), **CI tests**, and a **“point-in-time feature store”** layout in DuckDB that directly prevents the highest-severity failures above.
