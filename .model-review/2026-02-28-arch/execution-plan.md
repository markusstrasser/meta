# Execution Plan: 5-Agent Parallel Build Sprint

**Date:** 2026-02-28
**Source:** synthesis.md (6 model outputs, 2 rounds) + MASTER_PLAN.md + REFACTORING_PLAN.md
**Target repo:** ~/Projects/intel
**Method:** Orchestrator session dispatches 5 subagents in worktrees. Zero file overlap between agents. Merge sequentially after completion.

---

## Guiding Principle

**Iterate, don't rebuild.** The codebase has 295 working DuckDB views, 26 working (but untested) scan functions, working pipelines, working Brier scoring, working paper trading. The synthesis identifies what's MISSING, the refactoring plan identifies what's FRAGILE. We fix fragile + add missing. We don't touch what works.

**MVFL framing** (Gemini R1): The shortest path to closing the feedback loop is: prediction table → resolution → post-mortem. Everything else supports that loop. If an agent's work doesn't connect to predictions, it's infrastructure for later.

---

## Orchestrator Protocol

The orchestrator is a human or a top-level Claude Code session. It:

1. **Pre-flight**: Verifies intel repo state (clean git, DuckDB accessible, tests pass)
2. **Dispatches**: Spawns agents A-E in worktrees (parallel where possible)
3. **Collects**: Waits for completion, reviews outputs
4. **Merges**: Sequential merge in dependency order
5. **Integration test**: Runs full pipeline after merge to verify nothing broke

### Pre-flight Checklist

```bash
cd ~/Projects/intel
git status                              # Clean working tree
uv run python3 tools/healthcheck.py     # All checks pass
uv run pytest tools/tests/ -v           # Existing tests pass (test_scoring.py)
```

### Dispatch Order

```
Batch 1 (parallel, no dependencies):
  Agent A: Scanner Tests          — touches: tools/tests/ (new)
  Agent C: Entity Resolution      — touches: tools/build_issuer_xwalk.py (new)
  Agent D: Data Health            — touches: tools/dataset_registry.py (new), healthcheck.py (modify)

Batch 2 (after Batch 1 merged, needs test infrastructure from A):
  Agent B: Prediction Ledger      — touches: prediction_tracker.py (modify), new files

Batch 3 (after B merged, needs prediction table):
  Agent E: Surprise Detector      — touches: tools/surprise_detector.py (new)
```

Agents A, C, D can run simultaneously — they touch completely different files. Agent B needs A's conftest.py fixtures to write its own tests. Agent E needs B's prediction table to query.

### Merge Order

```
1. Agent A (tools/tests/ — all new files, no conflicts possible)
2. Agent D (tools/dataset_registry.py new + healthcheck.py modify)
3. Agent C (tools/build_issuer_xwalk.py — all new files)
4. Agent B (prediction_tracker.py modify + new files)
5. Agent E (tools/surprise_detector.py — all new files)
```

After each merge: `uv run pytest tools/tests/ -v` to verify no regression.

---

## Agent A: Scanner Test Suite

**Mission:** Write tests for every `scan_*` function in signal_scanner.py. This is 3,693 lines of trade-influencing code with zero test coverage.

### Context to Load (read, don't modify)

```
tools/signal_scanner.py              — 26 scan functions, understand signatures and SQL
tools/lib/scoring.py                 — fuse_evidence, llr_boolean, llr_from_percentile, etc.
tools/lib/watchlist.py               — WATCHLIST, SECTOR_MAP
tools/lib/db.py                      — DB_PATH, DATASETS
tools/tests/test_scoring.py          — existing test patterns (use as template)
tools/setup_duckdb.py                — view schemas (what columns exist in each view)
```

### Deliverables

```
tools/tests/conftest.py              — Shared fixtures:
                                       - in_memory DuckDB with mock views
                                       - mock data generators per domain
                                       - WATCHLIST/SECTOR_MAP fixture

tools/tests/test_insider.py          — Tests for: scan_insider_activity,
                                       scan_insider_cadence, scan_form144_presale

tools/tests/test_price.py            — Tests for: scan_price_extremes,
                                       scan_short_volume, scan_short_pressure

tools/tests/test_filings.py          — Tests for: scan_8k_events,
                                       scan_sec_metadata, scan_legal

tools/tests/test_macro.py            — Tests for: scan_macro_regime,
                                       scan_sentiment

tools/tests/test_alt_data.py         — Tests for: scan_google_trends,
                                       scan_app_rankings, scan_prediction_markets

tools/tests/test_regulatory.py       — Tests for: scan_federal_register,
                                       scan_warn_act, scan_supply_chain,
                                       scan_clinical_trials

tools/tests/test_congressional.py    — Tests for: scan_congressional

tools/tests/test_fraud.py            — Tests for: scan_mechanism_checklist,
                                       scan_leiden_clusters, scan_splink_resurrection,
                                       scan_mco_dead_npi, scan_address_anomalies

tools/tests/test_options.py          — Tests for: scan_options_surface

tools/tests/test_cross_signal.py     — Tests for: scan_cross_signals,
                                       scan_discovery, _detect_cascades,
                                       _fuse_correlated_groups
```

### Technical Spec

Each test must:
1. Create an **in-memory DuckDB** with minimal mock data matching the real view schema
2. Call the scan function with `(con, baselines)` arguments
3. Assert on: **signal count** (>0 for known anomalies, 0 for normal data), **LLR sign** (correct direction), **severity level** (maps correctly)
4. Test **graceful failure** when expected views are missing (should return empty list, not crash)

**Mock data pattern:**
```python
# conftest.py pattern
@pytest.fixture
def mock_db():
    """In-memory DuckDB with mock investment views."""
    con = duckdb.connect(":memory:")
    # Create view schemas matching setup_duckdb.py
    con.execute("""
        CREATE TABLE prices AS SELECT
            'ACME' as ticker, CURRENT_DATE as date,
            25.0 as close, 100000 as volume, ...
    """)
    # ... minimal realistic data per view
    return con
```

**Key gotcha:** signal_scanner.py imports `from tools.lib.scoring import ...` — tests need `sys.path` setup or the conftest must handle imports. Follow the pattern from existing `test_scoring.py`.

**What NOT to do:**
- Do NOT modify signal_scanner.py
- Do NOT modify scoring.py
- Do NOT create mock data that requires the full 525 GB dataset
- Do NOT test download scripts or pipeline scripts

### Acceptance Criteria

```bash
uv run pytest tools/tests/ -v         # All tests pass
uv run pytest tools/tests/ -v --co    # ≥26 test functions collected (one per scan_*)
```

---

## Agent B: Prediction Ledger + Experiment Registry

**Mission:** Upgrade prediction tracking from CSV to DuckDB, create the experiment registry, and define dual resolution criteria (Goodhart defense).

### Context to Load (read before starting)

```
tools/prediction_tracker.py          — Current implementation (1,835 lines, CSV-based)
                                       Understand: add, extract, resolve, score commands
tools/paper_ledger.py                — Integration point (calls prediction_tracker)
tools/signal_scanner.py              — What signal types exist (for experiment registry)
tools/lib/scoring.py                 — Current Brier scoring
tools/lib/db.py                      — DB_PATH, connection patterns
docs/CONSTITUTION.md                 — Principles 1 (predictions as commitments),
                                       11 (falsify before recommending)
```

### Deliverables

```
tools/prediction_tables.py           — DDL script that creates DuckDB tables:

    CREATE TABLE prediction (
        pred_id VARCHAR PRIMARY KEY,
        entity_id VARCHAR,
        ticker VARCHAR NOT NULL,
        created_at TIMESTAMP NOT NULL,
        resolve_at DATE NOT NULL,           -- mandatory deadline
        target VARCHAR NOT NULL,            -- 'price_return', 'relative_return', 'event'
        direction VARCHAR NOT NULL,         -- 'up', 'down', 'event_occurs', 'event_absent'
        threshold DOUBLE,                   -- magnitude threshold
        probability DOUBLE NOT NULL,        -- confidence [0,1]
        rationale_ref VARCHAR,              -- path to thesis file or signal CSV
        strategy VARCHAR,                   -- which signal type generated this
        linked_signal_ids VARCHAR,          -- JSON array of signal_ids
        resolution_type VARCHAR NOT NULL    -- 'market_return' or 'dual'
            CHECK(resolution_type IN ('market_return', 'dual')),
        fundamental_criterion VARCHAR,      -- for dual: what fundamental confirmation needed
        status VARCHAR DEFAULT 'open'
            CHECK(status IN ('open', 'resolved_hit', 'resolved_miss',
                             'resolved_partial', 'expired', 'cancelled'))
    );

    CREATE TABLE prediction_resolution (
        pred_id VARCHAR PRIMARY KEY REFERENCES prediction(pred_id),
        resolved_at TIMESTAMP NOT NULL,
        market_outcome VARCHAR,             -- 'hit', 'miss', 'partial'
        fundamental_outcome VARCHAR,        -- 'confirmed', 'refuted', 'pending', 'n/a'
        final_outcome VARCHAR NOT NULL,     -- 'hit', 'miss', 'partial'
        realized_return DOUBLE,
        brier DOUBLE,
        cause VARCHAR                       -- 'thesis_correct', 'timing', 'factor_shock',
            CHECK(cause IN ('thesis_correct', 'timing', 'factor_shock',
                           'data_error', 'thesis_invalid', 'unknown')),
        notes_ref VARCHAR                   -- path to post-mortem file
    );

    CREATE TABLE experiment_registry (
        experiment_id VARCHAR PRIMARY KEY,  -- signal_type + definition_hash
        signal_type VARCHAR NOT NULL,
        definition_hash VARCHAR NOT NULL,   -- SHA256 of signal logic
        created_at TIMESTAMP NOT NULL,
        hypothesis VARCHAR NOT NULL,        -- what we expected
        test_start DATE,
        test_end DATE,
        result VARCHAR                      -- 'active', 'validated', 'failed', 'retired'
            CHECK(result IN ('active', 'validated', 'failed', 'retired')),
        hit_rate DOUBLE,
        sample_n INTEGER,
        notes VARCHAR
    );


tools/prediction_tracker.py          — MODIFIED to:
                                       1. Write to DuckDB tables (prediction, prediction_resolution)
                                       2. Keep CSV as fallback/backup (don't delete it)
                                       3. `resolve` uses dual resolution when resolution_type='dual':
                                          - Check market return against threshold
                                          - Check fundamental_criterion if specified
                                          - final_outcome = hit only if BOTH pass (for dual)
                                       4. `score` computes Brier from DuckDB table

tools/experiment_logger.py           — NEW: logs signal experiments
                                       - log_experiment(signal_type, hypothesis, definition_code)
                                       - retire_experiment(experiment_id, reason)
                                       - report() — research hit-rate KPI

tools/tests/test_prediction.py       — NEW: tests for:
                                       - Brier scoring correctness (known inputs → known outputs)
                                       - Auto-resolution (price crosses threshold → resolved_hit)
                                       - Dual resolution (market hit + fundamental pending → stays open)
                                       - Direction parsing (up/down/event)
                                       - Experiment registry CRUD
```

### Technical Spec: Goodhart Defense (Dual Resolution)

This is the key design decision from GPT R2 §5.1. The generative principle says "maximize error correction measured by market feedback." But market feedback conflates:
- (a) being right about fundamentals
- (b) market timing
- (c) factor moves
- (d) sentiment

**Resolution types:**
- `market_return`: Simple — did the stock move as predicted? Used for short-term signals (5d, 20d).
- `dual`: Requires BOTH market return AND fundamental confirmation. Used for thesis-based predictions (60d, 90d). Examples of fundamental confirmation: earnings revision matches thesis, enforcement action occurs, FDA outcome matches prediction, insider behavior confirms.

**The agent must decide resolution_type at prediction creation time, not after the fact.** This prevents narrative post-mortem bias (GPT R2 §5.4).

### Migration Plan

1. Create DuckDB tables via `prediction_tables.py`
2. Migrate existing `datasets/predictions/predictions.csv` rows into DuckDB
3. Modify `prediction_tracker.py` to write to both CSV and DuckDB during transition
4. After verification: make DuckDB the primary, CSV the backup

### What NOT to Do

- Do NOT delete predictions.csv
- Do NOT modify paper_ledger.py (it calls prediction_tracker — the interface must stay the same)
- Do NOT implement weight learning (that's Phase 3, needs resolution data)
- Do NOT build the surprise detector (that's Agent E)

### Acceptance Criteria

```bash
uv run python3 tools/prediction_tables.py               # Tables created without error
uv run python3 tools/prediction_tracker.py list          # Shows existing predictions
uv run python3 tools/prediction_tracker.py score         # Brier scores match CSV version
uv run pytest tools/tests/test_prediction.py -v          # All tests pass
# Verify: SELECT COUNT(*) FROM prediction; matches CSV row count
```

---

## Agent C: Entity Resolution (issuer_xwalk)

**Mission:** Build the CIK → ticker → EIN → CUSIP bridge table from EDGAR Submissions Bulk ZIP. This unblocks every signal scanner that needs to map government data to tradeable securities.

### Context to Load

```
tools/build_entity_tables.py         — Existing entity table builder (understand patterns)
tools/setup_duckdb.py                — Existing xwalk-related views (search for 'xwalk', 'cik')
tools/lib/db.py                      — DB_PATH, connection patterns
tools/lib/normalize.py               — Name normalization functions
docs/MASTER_PLAN.md lines 431-448    — issuer_xwalk schema
docs/MASTER_PLAN.md lines 289-308    — 12 identifier namespaces + cast gotchas
```

### Data Source

EDGAR Submissions Bulk ZIP: `data.sec.gov/submissions/`
- ~4 GB nested JSON (company facts, filings, tickers, exchanges)
- Already downloaded to `datasets/sec/` (verify path)
- **OOM warning:** `read_json_auto` on 4GB nested JSON WILL crash on 18GB RAM. Must use strict column projection and streaming.

### Deliverables

```
tools/build_issuer_xwalk.py          — NEW: parses EDGAR bulk submissions
                                       Creates issuer_xwalk table in DuckDB:

    CREATE TABLE IF NOT EXISTS issuer_xwalk (
        cik VARCHAR NOT NULL,            -- VARCHAR not BIGINT: leading zeros matter
        ticker VARCHAR,
        cusip VARCHAR,
        ein VARCHAR,                     -- bridge to DOL/SAM/USASpending
        company_name VARCHAR,
        sic_code VARCHAR,
        exchange VARCHAR,                -- NYSE, NASDAQ, OTC, etc.
        start_date DATE,                 -- ticker validity window (PIT)
        end_date DATE,                   -- NULL = current
        PRIMARY KEY (cik, ticker, start_date)
    );

                                       Parsing strategy:
                                       1. Iterate JSON files individually (not bulk load)
                                       2. Extract: cik, name, ein, sic, tickers[], exchanges[]
                                       3. For ticker lifecycle: parse filings for ticker changes
                                       4. Insert with strict column projection

tools/lib/xwalk.py                   — NEW: lookup helpers
                                       - ticker_to_cik(ticker, as_of_date=None) → cik
                                       - cik_to_ticker(cik, as_of_date=None) → ticker
                                       - name_to_cik(company_name) → list of (cik, confidence)
                                       - get_entity_ids(ticker) → dict with cik, ein, cusip, sic
                                       All queries respect PIT: use as_of_date to handle
                                       ticker changes, delistings, acquisitions.

tools/tests/test_xwalk.py            — NEW: tests for:
                                       - Known mappings: AAPL → CIK 320193, TSLA → CIK 1318605
                                       - PIT correctness: ticker that changed returns correct
                                         CIK for each time period
                                       - Leading-zero preservation: CIK '0000320193' not '320193'
                                       - EIN format: strip dashes, consistent
                                       - Fuzzy name matching returns ranked candidates
```

### Technical Spec: 12 Identifier Namespaces

The xwalk is the FIRST bridge. Other namespaces will be added later but need consistent patterns:

| Key Type | Cast Gotchas | Agent C handles? |
|----------|-------------|-----------------|
| CIK | Leading zeros, int vs string | YES — always VARCHAR |
| ticker | Exchange suffix variations | YES — normalize |
| EIN | Strip dashes | YES |
| CUSIP | 6 vs 8 vs 9 digit | YES (from EDGAR) |
| NPI, FIPS, UEI, etc. | Various | NO — future agents |

### What NOT to Do

- Do NOT attempt fuzzy entity resolution across all 50 datasets (that's a future phase)
- Do NOT use `read_json_auto` on the full bulk ZIP (OOM)
- Do NOT modify setup_duckdb.py (the xwalk table is standalone)
- Do NOT build the full entity graph (24M edges already exists in build_entity_tables.py)

### Acceptance Criteria

```bash
uv run python3 tools/build_issuer_xwalk.py               # Completes without OOM
# In DuckDB:
# SELECT COUNT(DISTINCT cik) FROM issuer_xwalk;            > 10,000
# SELECT ticker FROM issuer_xwalk WHERE cik = '0000320193'; → 'AAPL'
# SELECT ticker FROM issuer_xwalk WHERE cik = '0001318605'; → 'TSLA'
# SELECT COUNT(*) FROM issuer_xwalk WHERE end_date IS NOT NULL; > 0
# SELECT COUNT(*) FROM issuer_xwalk WHERE ein IS NOT NULL;  > 5,000
uv run pytest tools/tests/test_xwalk.py -v                # All tests pass
```

---

## Agent D: Data Health (Dataset Registry + Silence Detection)

**Mission:** Create the dataset_registry and dataset_health_events tables, populate from existing sources, and implement silence detection rules that block signal scanners from running on corrupted data.

### Context to Load

```
tools/healthcheck.py                 — Current health checks (will add registry checks)
tools/setup_duckdb.py                — View definitions, system_watermarks
tools/daily_refresh.py               — SOURCE_REGISTRY dict (12 polling sources)
tools/staleness.py                   — Entity freshness checks
tools/lib/db.py                      — DB_PATH, DATASETS
docs/MASTER_PLAN.md lines 79-167     — dataset_registry + health_events schemas
docs/MASTER_PLAN.md lines 393-402    — Silence detection rules
```

### Deliverables

```
tools/dataset_registry.py            — NEW: DDL + population script

    DDL (in state.duckdb, NOT intel.duckdb — registry is operational, not analytical):

    CREATE TABLE IF NOT EXISTS dataset_registry (
        dataset_id VARCHAR PRIMARY KEY,
        name VARCHAR NOT NULL,
        domain VARCHAR,                      -- healthcare, finance_sec, energy, etc.
        entity_type VARCHAR,                 -- event, time_series, feed, etc.
        source_url VARCHAR,
        source_publisher VARCHAR,
        download_script VARCHAR,
        coverage_start DATE,
        coverage_end DATE,
        refresh_cadence VARCHAR NOT NULL,
        publication_lag_days INTEGER,
        pit_safe BOOLEAN DEFAULT FALSE,
        join_keys VARCHAR,
        file_path VARCHAR,
        file_format VARCHAR,
        view_names VARCHAR,
        poll_endpoint VARCHAR,
        poll_interval_minutes INTEGER,
        last_poll_at TIMESTAMP,
        last_poll_status VARCHAR,
        downloaded_at TIMESTAMP,
        next_refresh_at TIMESTAMP,
        row_count BIGINT,
        size_bytes BIGINT,
        schema_hash VARCHAR,
        notes VARCHAR
    );

    CREATE TABLE IF NOT EXISTS dataset_health_events (
        dataset_id VARCHAR NOT NULL,
        event_at TIMESTAMP DEFAULT now(),
        event_type VARCHAR NOT NULL,
        row_count BIGINT,
        schema_hash VARCHAR,
        details VARCHAR
    );

    Population sources (in order):
    1. system_watermarks table (existing) → coverage_end, row_count
    2. daily_refresh.py SOURCE_REGISTRY → poll sources, endpoints, intervals
    3. daily_update.sh steps → download_script mappings
    4. setup_duckdb.py view names → view_names column
    Manually fill: domain, entity_type, pit_safe, publication_lag_days
    for top-20 datasets. Leave rest NULL (progressive enrichment).


tools/silence_detector.py            — NEW: 5 detection rules
    Called by healthcheck.py after data refresh.

    Rules (from MASTER_PLAN, battle-tested — scrapers already broke for
    OIG LEIE, DOL WHD, CMS downloads):

    1. STALE: No new rows in 3× expected refresh interval
       → UPDATE dataset_registry SET last_poll_status = 'stale'

    2. SCHEMA_DRIFT: schema_hash changed from last known good
       → INSERT INTO dataset_health_events (event_type='schema_drift')
       → UPDATE dataset_registry SET last_poll_status = 'schema_drift'

    3. HTML_NOT_CSV: File contains '<html' or '<!DOCTYPE' tags
       → INSERT INTO dataset_health_events (event_type='html_not_csv')
       (This actually happened — scrapers returned error pages as 200)

    4. TRUNCATED: Row count dropped >50% from previous
       → INSERT INTO dataset_health_events (event_type='truncated')

    5. COLUMN_DIED: Previously-populated column is now all NULL
       → INSERT INTO dataset_health_events (event_type='column_died')

    Returns: list of unhealthy datasets.
    Integration: healthcheck.py calls silence_detector before
    allowing signal_scanner to run.


tools/healthcheck.py                 — MODIFIED: add two checks:
    1. After existing checks: call silence_detector.check_all()
    2. If any critical dataset (prices, sec_form4, insider trades)
       is unhealthy → EXIT 1 (block pipeline)
    3. If non-critical dataset is unhealthy → WARN but continue


tools/tests/test_data_health.py      — NEW: tests for:
    - Registry population: ≥20 datasets populated
    - Silence detection: mock stale data → correctly flagged
    - Silence detection: mock HTML-in-CSV → correctly flagged
    - Silence detection: mock row count drop → correctly flagged
    - Schema hash: compute hash, change column, verify hash changed
    - healthcheck integration: unhealthy critical dataset → exit 1
```

### Technical Spec: state.duckdb vs intel.duckdb

The dataset_registry is **operational state** (what's stale, what's broken). It goes in `state.duckdb`, not `intel.duckdb`. This separation already exists — `intel.duckdb` is analytical (295 views), `state.duckdb` is operational (predictions, ledger, etc.).

If `state.duckdb` doesn't exist yet, create it. Check what's already there.

### Schema Hash Computation

```python
def compute_schema_hash(con, view_name: str) -> str:
    """SHA256 of sorted column names + types."""
    cols = con.execute(f"DESCRIBE {view_name}").fetchall()
    schema_str = "|".join(f"{c[0]}:{c[1]}" for c in sorted(cols))
    return hashlib.sha256(schema_str.encode()).hexdigest()[:16]
```

### What NOT to Do

- Do NOT modify setup_duckdb.py (views stay as-is)
- Do NOT modify daily_refresh.py (it works)
- Do NOT try to populate ALL ~400 datasets into the registry (start with top 20-30 that have active views)
- Do NOT build the JSON descriptor system from MASTER_PLAN Layer 2 (that's Phase B, after proving the LLM consumer needs it)

### Acceptance Criteria

```bash
uv run python3 tools/dataset_registry.py populate        # Populates registry
# In state.duckdb:
# SELECT COUNT(*) FROM dataset_registry;                   ≥ 20
# SELECT COUNT(*) FROM dataset_registry WHERE refresh_cadence = 'daily'; ≥ 5
# SELECT COUNT(*) FROM dataset_registry WHERE poll_endpoint IS NOT NULL; ≥ 10
uv run python3 tools/silence_detector.py check            # Runs without error
uv run python3 tools/healthcheck.py                       # Still passes
uv run pytest tools/tests/test_data_health.py -v          # All tests pass
```

---

## Agent E: Surprise Detector + Post-Mortem Loop

**Mission:** Build the "missed surprise becomes a rule" mechanism. Nightly: check top movers in universe, cross-reference against active predictions, spawn structured post-mortem for misses.

### Context to Load

```
tools/prediction_tracker.py          — How predictions are stored (DuckDB after Agent B)
tools/signal_scanner.py              — What signals exist, what alert files look like
tools/lib/watchlist.py               — WATCHLIST (current universe)
tools/lib/db.py                      — DB_PATH, how to query prices
tools/lib/scoring.py                 — fuse_evidence (for understanding signal scores)
docs/CONSTITUTION.md                 — Principle: "every missed surprise becomes a rule"
```

### Deliverables

```
tools/surprise_detector.py           — NEW: the feedback loop closer

    def detect_surprises(con, date, threshold_pct=15.0, volume_multiple=2.0):
        """
        Find stocks in universe that moved >threshold% on >volume_multiple× avg volume.
        Returns list of {ticker, date, return_pct, volume_ratio, direction}.
        """
        # Query prices view for date
        # Filter to WATCHLIST + universe (if universe_membership exists)
        # Compute: |daily_return| > threshold AND volume > volume_multiple * ADV20

    def check_predictions(con, surprises: list):
        """
        For each surprise: did we have an active prediction?
        Returns: {predicted: [...], missed: [...]}
        """
        # Query prediction table for open predictions matching ticker
        # Predicted: we had a prediction, check if direction matches
        # Missed: no prediction existed for this ticker

    def generate_postmortem(con, surprise: dict, output_dir: str):
        """
        Create structured post-mortem file for a missed surprise.
        NOT a narrative — a structured checklist.
        """
        # Query all data sources for this ticker in last 90 days:
        #   - signal_scanner alerts (any signals fired?)
        #   - insider trades (Form 4 activity?)
        #   - 8-K filings (material events?)
        #   - Entity file (was it on our radar?)
        #
        # Write to analysis/postmortems/{ticker}_{date}.md
        # with structured template (see below)

    def main():
        """
        Nightly run:
        1. detect_surprises() for today
        2. check_predictions() — partition into predicted/missed
        3. For each missed: generate_postmortem()
        4. For each predicted: log resolution data
        5. Print summary to stdout
        """


POST-MORTEM TEMPLATE (structured, not narrative — from GPT R2 §5.4):

    # Post-Mortem: {TICKER} {DATE} ({RETURN}%)

    ## Event
    - Ticker: {TICKER}
    - Date: {DATE}
    - Return: {RETURN}%
    - Volume: {VOLUME_RATIO}× average

    ## Did we predict this?
    - [ ] Active prediction existed
    - [ ] Signal fired in last 30 days
    - [ ] Entity file existed and was current

    ## Pre-committed cause checklist
    Pick ONE primary cause (no narratives):
    - [ ] DATA_GAP: Relevant dataset not ingested
    - [ ] ENTITY_MISS: Entity resolution failed (data existed but didn't map)
    - [ ] SIGNAL_MISS: Signal logic didn't fire (data + entity OK, threshold wrong)
    - [ ] TIMING: Signal fired but too late (after price moved)
    - [ ] FACTOR_SHOCK: Macro/sector move, not company-specific
    - [ ] UNKNOWN: Genuinely unpredictable from available data

    ## Data audit (auto-populated)
    | Dataset | Had data? | Last update | Signal fired? |
    |---------|-----------|-------------|---------------|
    | prices  | {y/n}     | {date}      | —             |
    | insider | {y/n}     | {date}      | {y/n, z-score}|
    | 8-K     | {y/n}     | {date}      | {y/n}         |
    | CFPB    | {y/n}     | {date}      | {y/n, z-score}|
    ...

    ## Action item
    If cause is DATA_GAP or ENTITY_MISS or SIGNAL_MISS:
    - Proposed fix: {one sentence}
    - Estimated effort: {hours}
    - Requires: {new data / entity mapping / threshold change / new signal}

    ## Forward test
    Any new rule proposed here must survive:
    - [ ] Forward holdout (not tested on this event's data)
    - [ ] Expected lift with uncertainty bounds


tools/tests/test_surprise.py         — NEW: tests for:
    - Mock price data with 20% move → detected as surprise
    - Mock price data with 5% move → NOT detected
    - Mock prediction exists → classified as "predicted"
    - No prediction → classified as "missed"
    - Post-mortem template renders correctly
    - Data audit section populates from available views
```

### Technical Spec: Integration with Daily Pipeline

After Agent E is merged, add to `daily_update.sh` as a SOFT step after prediction resolution:

```bash
# Step N: Surprise detection
run_soft "Surprise detector" "uv run python3 tools/surprise_detector.py --date $(date +%Y-%m-%d)"
```

This is a one-line addition. The agent should note this in a comment but NOT modify daily_update.sh (the human does that).

### What NOT to Do

- Do NOT modify daily_update.sh (note the integration point, human adds it)
- Do NOT modify signal_scanner.py
- Do NOT implement weight learning or automatic rule creation (the post-mortem generates ACTION ITEMS for a human/agent to review, not automatic signal changes)
- Do NOT use LLM to generate narrative post-mortems (structured checklist only — GPT R2 §5.4 warns against narrative bias)

### Acceptance Criteria

```bash
# With mock data:
uv run python3 tools/surprise_detector.py --date 2026-02-28  # Runs without error
# Check output: any surprises detected are listed
# Check: postmortem files created in analysis/postmortems/
uv run pytest tools/tests/test_surprise.py -v                 # All tests pass
```

---

## Integration Test (After All Merges)

The orchestrator runs this after merging all 5 agents:

```bash
cd ~/Projects/intel

# 1. Full test suite
uv run pytest tools/tests/ -v

# 2. Existing pipeline still works
uv run python3 tools/healthcheck.py

# 3. New tables exist and are populated
uv run python3 -c "
import duckdb
con = duckdb.connect('intel.duckdb')
print('issuer_xwalk:', con.execute('SELECT COUNT(*) FROM issuer_xwalk').fetchone()[0])
con.close()

con = duckdb.connect('state.duckdb')
print('dataset_registry:', con.execute('SELECT COUNT(*) FROM dataset_registry').fetchone()[0])
print('prediction:', con.execute('SELECT COUNT(*) FROM prediction').fetchone()[0])
print('experiment_registry:', con.execute('SELECT COUNT(*) FROM experiment_registry').fetchone()[0])
con.close()
"

# 4. Prediction tracker still works with DuckDB backend
uv run python3 tools/prediction_tracker.py list
uv run python3 tools/prediction_tracker.py score

# 5. Signal scanner still works (no regressions from test changes)
uv run python3 tools/signal_scanner.py --dry-run  # if available, else manual check

# 6. Surprise detector runs
uv run python3 tools/surprise_detector.py --date $(date +%Y-%m-%d)
```

---

## What This Sprint Does NOT Build

Deferred to future phases (requires weeks of resolution data or different dependency chain):

| Item | Why deferred | Blocked by | Synthesis ref |
|------|-------------|------------|---------------|
| **first_seen_date on downloads** | Touches 28 scripts — add incrementally as each gets touched | Nothing (do opportunistically) | Tier 1.3 |
| **universe_membership table (PIT)** | 3-5 days, needs daily market cap data. Critical for any backtesting or weight learning. | Price data + market cap computation | Tier 2.2 |
| **Trade outbox table** | paper_ledger.py partially serves this role. Formal outbox is for graduated autonomy. | Graduated autonomy design | Phase 0 |
| **Liquidity gate** | "Can I exit 20% ADV in 3 days?" pre-trade check. ~1 day effort. | Nothing (do early in Phase 1) | Phase 1 |
| **Coverage eligibility maps** | "Which entities should appear in which datasets." Metadata enrichment. | dataset_registry (Agent D) | Phase 1 |
| **Quantitative sanity frame** | Three hard-coded numbers (FDR budget, resolution rate cap, liquidity cap). Design constraints, not code. Encode as constants when building weight learning. | Nothing (design decision) | Tier 1.6 |
| Signal weight learning | Needs months of resolved predictions | Resolution data | Tier 2.1 |
| Signal eval harness + random noise control | Run random signals through harness, must show ~0% edge | Prediction ledger + resolution data | Tier 6.4 |
| Alpha decay detector | Factor correlation monitoring per signal | Signal-level return attribution | Tier 3.7 |
| Base-rate store | Useful but not blocking | Nothing (low priority) | Tier 2.3 |
| Agent OS (task queue, BOOT.md) | Human still in the loop daily | Feedback loop validation | Tier 5 |
| Novel signals (Kitchen Sink, Deferred Maintenance, etc.) | Test existing scanners first | Scanner tests | Tier 3.x |
| Directory restructuring (views/, scanners/) | Cosmetic, not blocking | Nothing (low priority) | Refactoring Plan |
| Pipeline Python conversion | Bash works | Nothing (low priority) | Refactoring Plan |
| FDR control (Benjamini-Hochberg) | Needs experiment registry populated | Experiment data | Tier 1.6 |
| Graduated autonomy levels | Needs paper trading validation | Track record | Tier 6.3 |
| **Remaining Tier 4 red team defenses** | See synthesis.md Tier 4 table (14 items). Sprint covers 3 (schema drift, narrative bias, selective memory). Remaining 11 require infrastructure from later phases. | Various (universe table, weight learning, signal covariance) | Tier 4 |

---

## Estimated Timeline

| Agent | Effort | Can parallel with |
|-------|--------|-------------------|
| A: Scanner Tests | 3-4 days | C, D |
| B: Prediction Ledger | 2-3 days | (after A merged for test fixtures) |
| C: Entity Resolution | 2-3 days | A, D |
| D: Data Health | 2-3 days | A, C |
| E: Surprise Detector | 1-2 days | (after B merged for prediction table) |
| Integration + merge | 1 day | — |

**Critical path:** A/C/D parallel (3-4 days) → B (2-3 days) → E (1-2 days) → merge (1 day) = **~8-10 days total.**

With full parallelism on Batch 1, this compresses to ~7-8 days elapsed.
