

# Architecture Design: Alpha Engine

## 0. Design Philosophy

Before the subsystems: the core insight is that this system is a **conjecture-refutation machine**. Every entity relationship is a conjecture. Every signal is a conjecture. Every trade thesis is a conjecture. Market feedback refutes or fails to refute. The architecture exists to make that loop as tight and honest as possible.

The second insight: the AI agent isn't a user of the system — it **is** the system's reasoning layer. The architecture should feel like the agent's native memory and toolset, not an application with an API.

---

## 1. Subsystems and Boundaries

```
┌─────────────────────────────────────────────────────────────────────┐
│                        ALPHA ENGINE                                 │
│                                                                     │
│  ┌──────────┐  ┌──────────┐  ┌───────────┐  ┌──────────────────┐  │
│  │  INGEST  │→ │  ENTITY  │→ │  SIGNAL   │→ │    THESIS        │  │
│  │  LAYER   │  │  GRAPH   │  │  ENGINE   │  │    MANAGER       │  │
│  └──────────┘  └──────────┘  └───────────┘  └──────────────────┘  │
│       ↑                                            │               │
│       │              ┌──────────────┐              ↓               │
│       │              │   ERROR      │←───── ┌──────────┐          │
│       └──────────────│   LEDGER     │       │ PORTFOLIO│          │
│                      └──────────────┘       │ SCORECARD│          │
│                             ↑               └──────────┘          │
│                             │                     │               │
│                      ┌──────────────┐             │               │
│                      │   MARKET     │←────────────┘               │
│                      │   FEEDBACK   │                             │
│                      └──────────────┘                             │
└─────────────────────────────────────────────────────────────────────┘

Persistent State:
  - DuckDB:       analytics/signals/market data (columnar, fast)
  - Entity Files: git-versioned markdown+YAML (agent-readable, diffable)
  - Error Ledger: git-versioned log of every prediction + outcome
```

### Six subsystems, each with a single owner:

**1. Ingest Layer** — Owns: downloading, parsing, and loading raw data into DuckDB staging tables. Guarantees: every row has `source_id`, `source_name`, `ingested_at`, `raw_hash`. Knows nothing about entities or signals.

**2. Entity Graph** — Owns: the canonical identity of every company, person, and relationship. The single hardest subsystem. Guarantees: every resolved entity has a stable `entity_id`, a confidence score on each alias mapping, and provenance for every link.

**3. Signal Engine** — Owns: computing quantitative signals from joined data. Each signal is a pure function: `(entity_id, time_window) → (value, z_score, percentile, source_grade)`. Guarantees: signals are reproducible, timestamped, and never forward-looking.

**4. Thesis Manager** — Owns: combining signals into trade hypotheses. Each thesis is a structured document with: claim, evidence for, evidence against, predicted outcome, timeframe, confidence, position sizing. Guarantees: every thesis has a falsification condition and a deadline.

**5. Portfolio Scorecard** — Owns: current positions, proposed trades (outbox), P&L tracking, risk limits. Guarantees: Kelly sizing, concentration limits, drawdown breakers are enforced in code, not in instructions.

**6. Error Ledger + Market Feedback** — Owns: the loop. Every prediction gets a resolution. Every surprise gets a post-mortem. Every post-mortem can generate a new signal rule or update signal weights. This is the compounding asset.

### Interface contracts between subsystems:

```
Ingest → Entity Graph:    Staging tables with raw identifiers
Entity Graph → Signal:    entity_id joins across all datasets
Signal → Thesis:          Signal vectors per entity
Thesis → Portfolio:       Proposed trades with sizing
Portfolio → Feedback:     Positions + entry prices + timestamps
Feedback → Error Ledger:  Prediction outcomes (hit/miss/partial)
Error Ledger → Signal:    Updated signal weights + new rules
Error Ledger → Ingest:    New data source requests (when blind spots found)
```

---

## 2. The Data Pipeline — Full Trace

### Layer 0: Raw Download

```
data/
  raw/
    fda_faers/
      2024_Q3/
        DRUG24Q3.txt
        REAC24Q3.txt
        ...
      manifest.json          ← {url, downloaded_at, sha256, row_count}
    sec_edgar/
      ...
    cfpb_complaints/
      ...
```

Each data source gets a Python ingest script. The script:
1. Downloads (or checks for updates via ETag/Last-Modified)
2. Validates checksums
3. Loads into DuckDB staging schema with zero transformation
4. Writes manifest

```python
# ingest/fda_faers.py — representative pattern
def ingest(db: duckdb.DuckDBPyConnection, quarter: str):
    """Load raw FAERS data into staging.fda_faers_*"""
    # Download if not cached
    # Parse fixed-width/CSV into staging tables
    # Every row gets: _source='fda_faers', _source_period=quarter, _ingested_at=now()
    # No entity resolution here. Raw drug names, raw manufacturer names.
```

**Key decision**: staging tables are append-only, partitioned by source period. Never mutate raw data. DuckDB handles this efficiently with partitioned parquet under the hood.

### Layer 1: Clean + Normalize (still pre-entity-resolution)

```sql
-- clean/fda_faers.sql
CREATE OR REPLACE TABLE clean.fda_adverse_events AS
SELECT
    primaryid,
    caseid,
    UPPER(TRIM(drugname)) as drug_name_raw,
    UPPER(TRIM(prod_ai)) as active_ingredient_raw,
    UPPER(TRIM(mfr_sndr)) as manufacturer_raw,
    pt as preferred_term,           -- MedDRA preferred term
    event_dt,
    init_fda_dt,
    -- Standardize dates, handle nulls, deduplicate
FROM staging.fda_faers_drug d
JOIN staging.fda_faers_reaction r ON d.primaryid = r.primaryid
WHERE event_dt IS NOT NULL;
```

Each source gets a clean script that:
- Standardizes column names and types
- Handles known data quality issues (documented in comments)
- Deduplicates within-source
- Produces a `clean.*` table

### Layer 2: Entity Resolution (see Section 3)

Maps raw identifiers to canonical `entity_id`. Produces:

```sql
-- resolved.entity_map
-- entity_id | source | source_id | raw_name | confidence | method
-- ENT_001   | sec    | 0000789019| MICROSOFT CORP | 0.99 | cik_match
-- ENT_001   | cfpb   | NULL      | MICROSOFT      | 0.85 | fuzzy_name
-- ENT_001   | faers  | NULL      | MICROSOFT CORPORATION | 0.92 | fuzzy_name+sector
```

### Layer 3: Joined Analytical Views

```sql
-- analytics.company_signals is the master view
-- Joins across all resolved sources for a given entity_id + time_window
CREATE OR REPLACE VIEW analytics.entity_signal_base AS
SELECT
    e.entity_id,
    e.canonical_name,
    e.sector,
    e.market_cap_bucket,
    -- FDA signals
    faers.adverse_event_count_90d,
    faers.adverse_event_velocity,  -- rate of change
    faers.serious_event_ratio,
    -- CFPB signals
    cfpb.complaint_count_90d,
    cfpb.complaint_velocity,
    cfpb.company_response_rate,
    -- Insider signals
    insider.net_insider_shares_90d,
    insider.form4_filing_delay_avg,
    -- Contract signals
    contracts.new_contract_value_90d,
    contracts.contract_pipeline_change,
    -- ... 30-50 more columns
FROM resolved.entities e
LEFT JOIN analytics.fda_entity_signals faers USING (entity_id)
LEFT JOIN analytics.cfpb_entity_signals cfpb USING (entity_id)
-- ...
```

### Layer 4: Signal Computation

Each signal is a registered function that computes a score:

```python
# signals/fda_adverse_trajectory.py
class FDAAdverseTrajectory(Signal):
    id = "fda_adverse_trajectory"
    domain = "regulatory"
    
    def compute(self, entity_id: str, as_of: date) -> SignalResult:
        """
        Computes 90-day adverse event velocity vs. 12-month baseline.
        Returns z-score relative to same-sector peers.
        """
        # Query DuckDB for this entity's adverse event time series
        # Compute velocity (events/month, trailing 3mo vs trailing 12mo)
        # Z-score against sector peers
        # Return SignalResult(value, z_score, percentile, confidence, grade)
```

### Layer 5: Thesis Construction

The agent reads signal vectors and entity files, constructs theses:

```yaml
# theses/active/ACME_fda_adverse_spike.yaml
thesis_id: "ACME_fda_adverse_spike_2024Q4"
entity_id: "ENT_0472"
canonical_name: "Acme Pharma Inc"
direction: short_watchlist  # no shorting yet, but flag
created: 2024-11-15
deadline: 2025-02-15

claim: "ACME's lead drug will face regulatory action within 90 days based on adverse event acceleration"

evidence_for:
  - signal: fda_adverse_trajectory
    value: 3.2  # z-score
    grade: "[DATA]"
    detail: "Serious adverse events up 340% QoQ, 8x sector median velocity"
  - signal: insider_net_selling
    value: 2.1
    grade: "[DATA]"
    detail: "CFO and CMO sold $2.4M combined in 30 days, unusual vs. 3yr pattern"

evidence_against:
  - "Drug class historically has high FAERS noise (antidepressants). Base rate for regulatory action given this signal level: ~12%"
  - "Company recently expanded label — volume increase could explain some AE increase"

falsification: "If 90-day AE velocity drops below 1.5 z-score OR company receives FDA approval for new indication"
predicted_outcome: "Stock declines >15% within 90 days"
confidence: 0.35
position: NONE  # watchlist only at this confidence
```

### Layer 6: Portfolio Decision

```yaml
# portfolio/current.yaml
as_of: 2024-11-15
cash_pct: 45
positions:
  - entity_id: ENT_0123
    ticker: XYZ
    shares: 500
    entry_price: 23.40
    entry_date: 2024-10-01
    thesis_id: "XYZ_contract_surprise_2024Q4"
    current_price: 27.80
    unrealized_pnl_pct: 18.8
    kelly_fraction: 0.12  # quarter-kelly
    
outbox:  # proposed trades for human execution
  - action: BUY
    ticker: ABC
    target_allocation_pct: 8
    thesis_id: "ABC_cfpb_divergence_2024Q4"
    rationale: "Complaint velocity declining while stock at 52w low. Signal z=-2.1"
    max_entry_price: 14.50
    
risk_check:
  max_single_position: 0.20  # HARD LIMIT
  current_max_position: 0.12  # OK
  drawdown_from_peak: -0.03  # OK (breakers at -0.15, -0.25)
  positions_count: 6
```

### Layer 7: Feedback Loop

```yaml
# error_ledger/resolutions/XYZ_contract_surprise_2024Q4.yaml
thesis_id: "XYZ_contract_surprise_2024Q4"
prediction: "Stock rises >20% within 60 days on contract revenue surprise"
outcome: HIT
actual_return: 0.188
timeframe_days: 45
confidence_at_entry: 0.45

post_mortem: |
  Signal worked. Contract announcement on day 32 drove 14% gap up.
  Remaining 4.8% was drift. 
  
  Key learning: government contract signals had 3-week lead time 
  before public announcement. The FPDS data showed obligation 
  increase 22 days before press release.
  
  Action: Weight FPDS obligation velocity higher for defense 
  contractors. Current signal weight 1.0 → propose 1.3.

signal_updates:
  - signal_id: govt_contract_velocity
    old_weight: 1.0
    new_weight: 1.3
    reason: "Empirical lead time confirmation, n=1 (low confidence update)"
```

---

## 3. Entity Resolution — The Hard Problem

This is genuinely the hardest part of the system. I'll be honest about what I know and don't know.

### The Problem

The same company appears as:
- CIK `0000789019` in SEC filings
- "MICROSOFT CORPORATION" in FAERS
- "Microsoft" in CFPB complaints
- "MICROSOFT CORP" in FPDS contracts
- Ticker `MSFT` in market data
- Various subsidiary names, former names, DBA names

For $500M-$5B companies, this is harder than for mega-caps. Names are less standardized, there are more ambiguous matches, and some companies have common-word names.

### My Approach: Tiered Resolution

**Tier 1: Deterministic matches (high confidence, do first)**

SEC EDGAR gives us CIK → ticker → company name. This is the canonical anchor. About 8,000 companies in our market cap range.

```sql
-- The anchor table
CREATE TABLE resolved.entities (
    entity_id VARCHAR PRIMARY KEY,  -- 'ENT_' || md5(cik)[:8]
    cik VARCHAR UNIQUE,
    ticker VARCHAR,
    canonical_name VARCHAR,
    sic_code VARCHAR,
    sector VARCHAR,
    market_cap_latest DECIMAL,
    -- metadata
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

Some sources have CIK or ticker directly (SEC filings, insider transactions). These join deterministically.

**Tier 2: Fuzzy name matching with sector constraints**

For sources with only company names (FAERS, CFPB, FPDS):

```python
def resolve_name(raw_name: str, source: str, sector_hint: str = None) -> list[EntityMatch]:
    """
    1. Normalize: uppercase, strip suffixes (INC, CORP, LLC, CO), 
       remove punctuation, collapse whitespace
    2. Exact match against canonical names → confidence 0.95
    3. Token-set similarity (handles word reordering) → threshold 0.85
    4. If sector_hint available, boost matches in same sector
    5. For ambiguous matches (0.70-0.85), flag for review
    """
```

I'd use `rapidfuzz` for string matching — it's fast enough for our scale (matching against ~8K canonical names is trivial).

**Tier 3: Subsidiary resolution**

This is the genuinely hard part. SEC filings list subsidiaries (Exhibit 21). A company might file FAERS reports under a subsidiary name that doesn't obviously connect to the parent.

```
# entities/ENT_a1b2c3d4/aliases.yaml
canonical_name: "Acme Pharmaceuticals Inc"
cik: "0001234567"
ticker: "ACME"
aliases:
  - name: "ACME PHARMA INC"
    source: faers
    
