## Architecture overview (local-first, error-correction-maximizing)

**Core idea:** make *predictions* (with probabilities) a first-class artifact, tie every signal → thesis → proposed trade to an auditable provenance chain, then close the loop with **market outcomes** (returns + calibration scoring). Everything else (data lake, entity graph, features) exists to increase the rate and quality of that loop.

**Physical stack (single Mac):**
- **Filesystem “lake”**: `data/raw/…` + `data/curated/…` as Parquet (partitioned by source/date)
- **DuckDB**: single file DB for joins, features, scoring, portfolio, outcomes (`warehouse.duckdb`)
- **Python**: ingestion, transforms, entity resolution, signals, evaluation
- **git**: version entity files + research docs + “error-correction ledger” + configuration
- **MCP tools** (for AI agents): read/write files, run SQL, run pipelines, create PRs, generate reports

---

# 1) Module boundaries — subsystems and ownership

### A. **Source Ingestion (“connectors”)**
**Owns:** downloading, decompression, schema capture, raw immutability  
**Outputs:** raw Parquet + a machine-readable source manifest  
**Key requirements:** reproducible, incremental, cheap.

- Interface (per source):
  - `fetch(snapshot_date) -> raw_files`
  - `normalize(raw_files) -> parquet_files + schema.json`
  - `lineage.json` (URL, retrieval time, checksums, license note)

### B. **Lakehouse Layout + Catalog (lightweight)**
**Owns:** folder conventions, partitioning, dataset registry in DuckDB  
**Avoid:** heavy data catalog tools; use a few tables + manifests.

DuckDB tables:
- `catalog_sources(source_id, name, cadence, homepage, last_ingested_at, notes)`
- `catalog_assets(source_id, path, checksum, row_count, min_date, max_date)`

### C. **Canonicalization / Standardization**
**Owns:** turning heterogeneous tables into a small set of *canonical* tables with consistent types and keys (not yet resolved to entities).  
Examples:
- `sec_filings_canon`
- `insiders_canon`
- `contracts_canon`
- `complaints_canon`
- `faers_events_canon`
- `prices_daily`

This module is where you enforce:
- consistent timestamps
- consistent currency units
- consistent company identifier fields when present (CIK, LEI, ticker, etc.)

### D. **Entity Graph (the moat)**
**Owns:** entity IDs, alias tables, linkage evidence, and resolution decisions across datasets.  
**Stores in DuckDB** (graph-in-relational, no external graph DB).

Core tables:
- `entity(entity_id, entity_type, canonical_name, created_at, updated_at)`
- `entity_identifier(entity_id, id_type, id_value, valid_from, valid_to, source_id, source_grade, evidence_ref)`
- `entity_alias(entity_id, alias, source_id, source_grade, evidence_ref)`
- `entity_link_evidence(left_entity_or_record, right_entity_or_record, method, weight, features_json, source_grade, evidence_ref)`
- `entity_resolution_decision(decision_id, left, right, decision {link|no_link}, confidence, decided_by {auto|human}, rationale_ref, created_at)`

**Entity files (git-versioned):**
- `entities/{entity_id}.md` (human-readable, sourced claims, running priors, links to signals/predictions)
- Optional structured sidecar: `entities/{entity_id}.yaml` for key facts (all with provenance pointers)

### E. **Feature & Base-Rate Store**
**Owns:** computed metrics per entity/time and **base rates** (the “quantify before narrating” layer).  
DuckDB tables:
- `feature_entity_daily(entity_id, date, feature_name, value, provenance_ref)`
- `base_rate(metric_name, universe_def, lookback, value, computed_at, query_ref)`

### F. **Signal Engine (strategy modules)**
**Owns:** detection logic, scoring, direction, horizon, and producing *Signal Events*  
A signal event is **not** a trade; it’s a quantified anomaly with base-rate context.

DuckDB:
- `signal_event(signal_id, entity_id, asof_date, strategy, direction, horizon_days, severity, expected_return, prob_up, prob_down, rationale_ref, provenance_ref, status)`

### G. **Thesis / Prediction / Counter-thesis Engine**
**Owns:** converting signals into falsifiable predictions and trade proposals (outbox).  
Artifacts:
- `theses/{thesis_id}.md` (sourced, contains “strongest counterargument” section)
- `predictions` table (first-class, scored later)

DuckDB:
- `prediction(pred_id, entity_id, created_at, resolve_at, target {price_return|relative_return|event}, threshold, probability, rationale_ref, strategy, linked_signal_ids, status)`
- `prediction_resolution(pred_id, resolved_at, outcome, realized_return, brier, notes_ref)`

### H. **Portfolio + Risk + Outbox**
**Owns:** current holdings view, fractional Kelly sizing, guardrails, and trade proposal queue (no execution).  
DuckDB:
- `portfolio_position(entity_id, quantity, avg_cost, market_value, updated_at)`
- `trade_proposal(trade_id, created_at, entity_id, action, size_dollars, kelly_fraction, constraints_hit_json, rationale_ref, status {proposed|approved|rejected|executed})`

### I. **Market Data + Outcome Evaluator (the scorekeeper)**
**Owns:** daily prices, benchmark, factor/sector tags (light), prediction resolution, performance attribution.  
DuckDB:
- `prices_daily(symbol, date, open, high, low, close, volume, source)`
- `returns(entity_id, date, return_1d, return_20d, …)`
- `strategy_score(strategy, window, brier_mean, alpha_mean, hit_rate, sample_n)`

### J. **Error-Correction Ledger + Postmortems**
**Owns:** capturing “what we believed, why, and what happened” and turning misses into queued work.  
Artifacts (git):
- `postmortems/{pred_id}.md`
- `rules_backlog.md` (each item: missed surprise → dataset to add / feature to compute / rule to adjust)

---

# 2) Data flow — raw data → actionable signals (full pipeline)

### Step 0 — Universe + market tape (always-on)
1. Build/maintain **universe** of target public companies (e.g., Russell 2000-ish or 500M–5B cap):
   - `universe_company(cik, ticker, name, exchange, sector, market_cap_bucket, …)`
2. Ingest **daily prices** (free sources acceptable for MVP), compute returns.

### Step 1 — Ingest
- Scheduled (cron/Launchd) per source cadence:
  - download → checksum → store in `data/raw/{source}/{snapshot_date}/…`
  - append to `catalog_assets`

### Step 2 — Canonicalize
- Convert raw into typed Parquet in `data/curated/{source}/…`
- Load external tables in DuckDB as views or parquet scans.

### Step 3 — Stage records for entity resolution
- For each canonical dataset, create a `*_records` view/table exposing:
  - available identifiers (CIK, ticker, LEI, employer name, address, etc.)
  - normalized name fields
  - timestamps and “record_id”

### Step 4 — Entity resolution + graph enrichment
- Deterministic links first (high precision):
  - CIK ↔ SEC filings
  - ticker ↔ prices
  - LEI ↔ legal entity datasets
- Then probabilistic linking for messy domains (e.g., contracts, complaints, FAERS manufacturer names):
  - generate candidates (blocking)
  - score match
  - auto-link above threshold; else queue for human review
- Write:
  - `entity_identifier`, `entity_alias`, `entity_resolution_decision`

### Step 5 — Feature computation + base rates
- Compute entity-time features (rolling windows, z-scores vs universe/sector):
  - complaint velocity, adverse event velocity, contract revenue surprise %
- Compute base rates (e.g., “typical 90d complaint spike distribution by sector”).

### Step 6 — Signal detection (strategy modules)
- Each strategy emits `signal_event` with:
  - anomaly magnitude vs base rate
  - direction (+/-), horizon, confidence
  - links to underlying feature rows (provenance refs)

### Step 7 — Thesis + falsification + prediction
- For high-severity signals:
  - generate a thesis doc (with sourced facts only)
  - include counter-thesis explicitly (ACH for >$10M impact leads)
  - create one or more **predictions**:
    - e.g., “Stock underperforms IWM by ≥10% over next 60 trading days with p=0.65”

### Step 8 — Portfolio proposal (outbox)
- Convert predictions into trade proposals with fractional Kelly (f=0.25), guardrails applied.
- Queue proposals; human approves/executes externally; execution recorded back.

### Step 9 — Resolution + scoring + learning
- When resolve date arrives:
  - compute realized return / relative return
  - compute calibration (Brier), EV error, and P&L attribution
  - update `strategy_score`, adjust priors/thresholds
  - create postmortem if large miss or large win (to extract rules)

---

# 3) Entity resolution — linking companies/people across 50+ datasets

## Principles
- **Decisions are durable assets** (Principle 6): store every link decision + evidence.
- **High precision first**: deterministic IDs dominate; probabilistic only when necessary.
- **Provenance always**: each link has `method`, `weight`, and `evidence_ref`.

## Entity types
- `company_public` (primary)
- `person` (insiders, directors, politicians)
- `agency` (government)
- `facility` (optional later)
- `product/drug` (optional later)

## Identifier hierarchy (examples)
**Company:**
- Strong: CIK, LEI
- Medium: ticker (time-varying), IRS EIN (sometimes), DUNS (legacy), SAM UEI (contracts)
- Weak: normalized name + address, domain, subsidiary mentions

**Person:**
- Strong-ish: SEC insider CIK/owner identifiers when present
- Medium: full name + employer + role + time
- Weak: name only

## Resolution workflow (practical on one machine)

### A. Deterministic linking (auto)
Rules:
- If record has CIK → link to `company_public` entity with same CIK
- If SEC filing mentions ticker and CIK consistent → assert ticker alias valid within date range
- Maintain `entity_identifier(valid_from, valid_to)` for ticker changes

### B. Candidate generation (blocking)
For messy datasets (CFPB, FAERS manufacturer, contracts vendor):
- Block on:
  - tokenized name signature (e.g., first 6 consonants, or sorted tokens minus stopwords)
  - state/country
  - vendor UEI/DUNS when present
  - website domain when present

### C. Match scoring (probabilistic)
Compute features:
- name similarity (Jaro-Winkler, token set ratio)
- address similarity (street/city/zip)
- co-occurrence with known identifiers (e.g., UEI appears with known subsidiary)
- time consistency (vendor existed at that time; ticker valid then)

Score → decision:
- `score ≥ 0.98`: auto-link (store decision as auto, high confidence)
- `0.90–0.98`: queue for human review UI (can be CLI TUI)
- `< 0.90`: no-link (but keep evidence for later)

### D. Human review loop (small but high leverage)
A single review command:
- shows top candidates + evidence
- user selects link/no-link
- writes `entity_resolution_decision` and updates identifiers/aliases

This is one of the highest ROI pieces because it compounds across every future join.

---

# 4) Signal detection — anomaly → expected value, with a scoring framework

## Signal Event schema (what every strategy must output)
Each event must include:
- **Base rate context** (what’s normal in this sector/universe)
- **Magnitude** (z-score / percentile / fold-change)
- **Direction** (long/short/neutral)
- **Horizon** (days)
- **Estimated return distribution** (at least mean + uncertainty proxy)
- **Provenance refs** (features + raw sources)
- **Claim grading**: any narrative text defaults to [F3] until tied to data

## Strategy modules (aligned to your ranked alpha list)

### 1) FAERS adverse event trajectory (pharma/biotech)
Features:
- AE count velocity (30d/90d), seriousness rate, outcome mix
- product-level → map to company via manufacturer resolution
Signals:
- spike in serious AE rate vs product baseline and sector baseline
Scoring:
- severity = percentile of (serious_AE_velocity_z)
- expected_return learned from historical mapping of AE spikes → subsequent underperformance

### 2) CFPB complaint velocity (banks/fintech)
Features:
- complaints per 1B assets (if available) or raw velocity
- issue mix shift (e.g., “fraud”, “funds availability”)
Signals:
- complaint acceleration + negative resolution outcomes
Scoring:
- short-bias; horizon 20–60d; base-rate by peer group

### 3) Government contract revenue surprise (long)
Features:
- award amount / trailing twelve-month revenue (TTM rev from filings)
- novelty (new agency/customer), contract type, duration
Signals:
- award > 5% TTM rev and company previously underweighted in gov revenue
Scoring:
- long-bias; horizon 30–120d; expected_return scaled by award/TTM and historical reaction

### 4) Cross-domain governance signals
Features:
- insider selling clusters, late filings, director turnover
- OSHA violations, enforcement actions, litigation bursts
Signals:
- multi-signal concordance (weak signals that align become strong)
Scoring:
- ensemble: weighted sum where weights are learned from outcome scoring (below)

### 5) Insider filing delay + congressional trades
Features:
- delay distribution vs that insider’s history
- trade direction, size relative to net worth proxy
Signals:
- unusual delay + clustered sells (or buys) and subsequent drift historically

## Scoring framework (how to pick what becomes a prediction)
Maintain three layers:

### Layer A — Statistical anomaly score (fast)
- z-scores / percentiles vs sector/universe
- cheap, immediate, stable

### Layer B — Outcome-learned mapping (calibrated)
For each strategy, fit a simple model initially:
- logistic regression / isotonic calibration mapping `(features) → P(outperform threshold)`
- later: gradient boosting if justified
Store per-strategy calibration curves and update monthly.

### Layer C — Expected value & position sizing (portfolio-aware)
- Convert predicted distribution into **fractional Kelly** sizing with guardrails:
  - max 20% position
  - sector concentration flag > 40%
  - drawdown circuit breaker (-15% pause / -25% reauth)

Only Layer A is required for MVP; Layers B/C compound with feedback.

---

# 5) The feedback loop — market outcomes → system improves (the core)

## First-class objects to close the loop
1. **Prediction** (probability, horizon, threshold, rationale)
2. **Resolution** (realized outcome, return, Brier score)
3. **Attribution** (which signals/features drove it)
4. **Update** (strategy weights, thresholds, base rates)

## What gets updated automatically (monthly cadence)
- **Calibration** per strategy:
  - reliability curves (predicted 0.7 happens ~70%?)
  - Brier score trends
- **Strategy capital allocation bias**:
  - increase/decrease how often signals convert to predictions
- **Thresholds**:
  - e.g., only trigger CFPB signals above 95th percentile if 90–95% didn’t pay
- **Base rates**:
  - sector-specific complaint distributions drift; recompute

## “Missed surprise becomes a rule” mechanism (high leverage)
Define “surprise” triggers:
- largest ±1d / ±5d moves vs universe (e.g., top 1% absolute moves)
For each surprise:
- generate a postmortem template automatically:
  - what datasets had precursor signals?
  - were they ingested in time?
  - did entity resolution fail?
  - did a signal fire but not escalate?
- create a backlog item with a concrete fix:
  - add dataset X
  - compute feature Y
  - adjust threshold Z
  - add a new resolution rule for identifier type W

This is the practical implementation of the Generative Principle on a solo machine.

---

# 6) What to build first — phases that are independently useful

### Phase 1 (1–2 weeks): Scoreboard foundation
Deliverable: “At any time, answer: what should I buy/sell/hold and why?”
- Universe table (CIK↔ticker)
- Daily prices + benchmark (IWM) + returns
- Prediction ledger + resolution + Brier scoring
- Minimal portfolio tracker + trade proposal outbox
- One “surprise detector” that logs top movers and opens postmortem stubs

### Phase 2 (2–4 weeks): Entity graph MVP (public companies only)
Deliverable: joins stop breaking; entity IDs become stable
- Deterministic IDs: CIK + ticker history
- Entity files in git (basic template + provenance enforcement)
- Resolution decision table + simple CLI review tool

### Phase 3 (3–6 weeks): One alpha strategy end-to-end (choose CFPB or contracts)
Deliverable: weekly watchlist + predictions
- Ingest + canonicalize dataset
- Features + base rates
- Signal events + escalation to predictions
- Monthly calibration report per strategy

### Phase 4: Second strategy + cross-domain fusion
- Add contracts (if CFPB first) or CFPB (if contracts first)
- Introduce “multi-signal concordance” scoring

### Phase 5: FAERS (heavier entity resolution)
- Add manufacturer/product resolution workflows
- More human review leverage; big moat potential

### Phase 6: Governance/insiders/congressional + operational hardening
- Insider delay features
- ACH workflow for >$10M impact theses (templated, semi-automated)

---

# 7) What NOT to build (YAGNI on a single-user system)

- **Microservices / Kubernetes / message buses**: your bottleneck is research iteration, not throughput.
- **Streaming pipelines**: batch daily/weekly is sufficient for these public sources initially.
- **A separate graph database**: DuckDB + well-designed link tables is enough; add a graph DB only if proven necessary.
- **A heavy orchestration platform** (Airflow/Prefect) at the start: use `make` + Python entrypoints + cron; introduce orchestration only when dependency management becomes painful.
- **A generic “feature store” abstraction**: start with a few DuckDB tables and views; abstraction later if reuse pain appears.
- **Complex UI**: start with generated markdown reports + a small CLI for resolution review and portfolio proposals.
- **Deep learning / complex ML** early: you need calibrated predictions and fast feedback; simple models + base rates outperform “fancy” when data is sparse/noisy.
- **Perfect schema unification across all sources**: canonicalize only what each strategy needs; expand as strategies expand.

---

## A concrete repo layout (practical for solo + AI agents)

```
/data
  /raw/{source}/{snapshot_date}/...
  /curated/{source}/...
/db
  warehouse.duckdb
/entities
  E000123.md
  E000123.yaml
/theses
  T000045.md
/postmortems
  P000778.md
/pipelines
  ingest_{source}.py
  canon_{source}.py
  resolve_entities.py
  compute_features.py
  run_signals.py
  make_predictions.py
  resolve_predictions.py
/reports
  weekly_watchlist.md
  monthly_calibration.md
/constitution
  CONSTITUTION.md   (human-protected)
/config
  sources.yaml
  thresholds.yaml
  universe.yaml
```

If you want, I can follow this with: (a) the exact DuckDB DDL for the core tables, (b) the “signal event” and “prediction” markdown templates with provenance slots, and (c) a minimal `make`-based pipeline plan (targets + dependencies) that maximizes iteration speed.
