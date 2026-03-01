

# The Agent Operating System: Complete Runtime Specification

## Architecture Overview

The system is a **file-driven state machine**. Every piece of state lives in the filesystem or DuckDB. There is no external orchestrator—the agent IS the orchestrator, bootstrapping its own context from disk at every session start.

```
HEDGE_SYSTEM/
├── .agent/                     # Agent operating system state
│   ├── clock.json              # Heartbeat + session tracking
│   ├── queue.db                # Task queue (SQLite, not DuckDB—no locking issues)
│   ├── BOOT.md                 # Session bootstrap prompt (always loaded first)
│   ├── locks/                  # File-based locks
│   └── checkpoints/            # Mid-task crash recovery
├── entities/                   # One file per entity
│   ├── TICKER.md               # Structured entity file
│   └── .meta/TICKER.json       # Freshness, confidence, source hashes
├── signals/                    # Signal outputs
│   ├── latest_scan.json        # Most recent signal scan results
│   ├── fired/                  # Signals that crossed thresholds
│   └── archive/                # Historical signals for backtesting
├── theses/                     # Active investment theses
│   ├── active/TICKER_thesis.md
│   └── graveyard/              # Dead theses with post-mortems
├── portfolio/                  # Portfolio state
│   ├── positions.json          # Current positions
│   ├── proposals/              # Pending trade proposals for human
│   └── ledger.json             # All historical trades + outcomes
├── predictions/                # Falsifiable predictions
│   ├── open/                   # Unresolved predictions
│   └── resolved/               # Resolved with outcome
├── errors/                     # Error ledger
│   └── ledger.jsonl            # Append-only error log
├── briefings/                  # Human-facing outputs
│   └── YYYY-MM-DD_morning.md
├── data/                       # Raw and processed data
│   ├── warehouse.duckdb        # Main analytical database
│   ├── raw/                    # Raw downloaded files
│   └── staging/                # Pre-load staging area
├── metrics/                    # Operational metrics
│   └── ops.jsonl               # Append-only operational metrics
└── scripts/                    # Reusable Python scripts
    ├── signals/                # Signal computation scripts
    ├── ingest/                 # Data ingestion scripts
    └── validate/               # Validation scripts
```

---

## 1. The Task Scheduler

### The Boot Sequence

Every session begins by reading `.agent/BOOT.md`. This file is the **constitutional bootstrap**—it never exceeds 3,000 tokens and tells the agent exactly how to orient itself.

```markdown
<!-- .agent/BOOT.md -->
# BOOT SEQUENCE

You are the autonomous intelligence engine. Read this, then act.

## Step 1: Read clock
`cat .agent/clock.json`

## Step 2: Check for crash recovery
`ls .agent/checkpoints/`
If non-empty: resume the interrupted task BEFORE scheduling new work.

## Step 3: Load working memory
`python scripts/ops/load_context.py`
This prints a <4000 token summary of: portfolio state, active theses (count + top 3 by urgency), stale entities, fired signals, pending predictions near resolution, last session summary.

## Step 4: Read the task queue
`python scripts/ops/next_task.py`
This returns the highest-priority task. Execute it.

## Step 5: After each task
`python scripts/ops/complete_task.py --task-id <ID>`
Then go to Step 4 for the next task. If context usage > 70%, commit all work and EXIT cleanly so a fresh session starts.

## Invariant
NEVER modify this file. NEVER modify the constitution. NEVER execute trades.
If you are uncertain whether an action is permitted, STOP and write to `.agent/escalations/`.
```

### The Task Schema

Tasks live in `.agent/queue.db` (SQLite—chosen over DuckDB specifically because SQLite handles concurrent reads gracefully and the agent only needs single-writer access for the queue).

```sql
-- .agent/queue.db schema
CREATE TABLE tasks (
    id TEXT PRIMARY KEY,           -- UUID
    created_at TEXT NOT NULL,      -- ISO 8601
    updated_at TEXT NOT NULL,
    state TEXT NOT NULL CHECK(state IN (
        'pending', 'ready', 'in_progress', 'completed',
        'failed', 'blocked', 'cancelled'
    )),
    priority REAL NOT NULL,        -- Higher = more urgent. Computed dynamically.
    category TEXT NOT NULL CHECK(category IN (
        'crash_recovery',          -- Resume interrupted work
        'interrupt',               -- Time-sensitive external event
        'signal_scan',             -- Run signal scanners
        'entity_refresh',          -- Update entity files
        'data_ingest',             -- Download/load new data
        'thesis_work',             -- Develop/stress-test theses
        'prediction_resolve',      -- Check if predictions resolved
        'error_review',            -- Review error ledger for patterns
        'maintenance',             -- Cleanup, optimization
        'exploration'              -- Open-ended research
    )),
    title TEXT NOT NULL,
    description TEXT,              -- Detailed task description
    inputs TEXT,                   -- JSON: files/queries needed
    success_criteria TEXT,         -- JSON: what "done" looks like
    outputs TEXT,                  -- JSON: files produced (filled on completion)
    depends_on TEXT,               -- JSON array of task IDs that must complete first
    entity TEXT,                   -- Ticker if entity-specific
    estimated_tokens INTEGER,      -- Estimated context consumption
    actual_tokens INTEGER,         -- Filled on completion
    attempt_count INTEGER DEFAULT 0,
    max_attempts INTEGER DEFAULT 3,
    error_log TEXT,                -- JSON array of error messages from failed attempts
    session_id TEXT,               -- Which session picked this up
    started_at TEXT,
    completed_at TEXT
);

CREATE TABLE task_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    event TEXT NOT NULL,           -- 'created', 'started', 'completed', 'failed', 'retried'
    details TEXT,
    FOREIGN KEY (task_id) REFERENCES tasks(id)
);

CREATE INDEX idx_tasks_state_priority ON tasks(state, priority DESC);
CREATE INDEX idx_tasks_category ON tasks(category);
```

### The Priority Function

Priority is **dynamically computed**, not a static ordering. The function runs every time `next_task.py` is called.

```python
# scripts/ops/priority.py

import json
import sqlite3
import os
from datetime import datetime, timedelta

def compute_priority(task: dict, context: dict) -> float:
    """
    Priority is a weighted sum of urgency signals.
    Higher = do first.

    Context includes: portfolio state, entity freshness map,
    fired signals, market hours status.
    """
    base_priorities = {
        'crash_recovery': 10000,    # Always first
        'interrupt': 5000,          # Time-sensitive events
        'signal_scan': 100,         # Base: routine
        'prediction_resolve': 90,
        'entity_refresh': 80,
        'data_ingest': 70,
        'thesis_work': 60,
        'error_review': 40,
        'maintenance': 20,
        'exploration': 10,
    }

    score = base_priorities.get(task['category'], 0)

    # --- Urgency Modifiers ---

    # Portfolio exposure: tasks about current holdings get +500
    if task.get('entity') and task['entity'] in context.get('held_tickers', []):
        score += 500

    # Staleness: entity refresh tasks get boosted by days since last update
    if task['category'] == 'entity_refresh' and task.get('entity'):
        freshness = context.get('entity_freshness', {})
        last_updated = freshness.get(task['entity'])
        if last_updated:
            days_stale = (datetime.utcnow() - datetime.fromisoformat(last_updated)).days
            score += days_stale * 25  # 10 days stale = +250
        else:
            score += 300  # Never updated = high priority

    # Signal fire: if a signal fired for this entity, boost thesis work
    if task['category'] == 'thesis_work' and task.get('entity'):
        if task['entity'] in context.get('fired_signal_tickers', []):
            score += 400

    # Prediction near expiry: predictions resolving within 48h get boosted
    if task['category'] == 'prediction_resolve':
        score += 200  # Always somewhat urgent

    # Market hours: signal scans more valuable when market is open or about to open
    if task['category'] == 'signal_scan' and context.get('market_hours_proximity', 999) < 2:
        score += 300

    # Retry penalty: tasks that have failed before get slightly deprioritized
    # (but not too much—they might be important)
    score -= task.get('attempt_count', 0) * 15

    # Age bonus: tasks sitting in queue for a long time get a small boost
    # to prevent starvation
    created = datetime.fromisoformat(task['created_at'])
    hours_waiting = (datetime.utcnow() - created).total_seconds() / 3600
    score += min(hours_waiting * 5, 200)  # Cap at +200

    # Dependency check: if depends_on has incomplete tasks, set to -1 (blocked)
    if task.get('depends_on'):
        deps = json.loads(task['depends_on']) if isinstance(task['depends_on'], str) else task['depends_on']
        if deps and not all(d in context.get('completed_task_ids', set()) for d in deps):
            return -1  # Blocked

    return score
```

### The Task Selector

```python
# scripts/ops/next_task.py
"""
Called by the agent after boot. Returns the next task to execute.
Also handles: generating recurring tasks if queue is empty,
detecting interrupts, and recomputing priorities.
"""

import sqlite3
import json
import os
import sys
from datetime import datetime, timedelta
from priority import compute_priority

QUEUE_DB = '.agent/queue.db'

def load_context():
    """Load minimal context needed for priority computation."""
    ctx = {}

    # Current portfolio
    if os.path.exists('portfolio/positions.json'):
        with open('portfolio/positions.json') as f:
            positions = json.load(f)
            ctx['held_tickers'] = [p['ticker'] for p in positions.get('positions', [])]
    else:
        ctx['held_tickers'] = []

    # Entity freshness
    freshness = {}
    meta_dir = 'entities/.meta'
    if os.path.exists(meta_dir):
        for fname in os.listdir(meta_dir):
            if fname.endswith('.json'):
                ticker = fname.replace('.json', '')
                with open(os.path.join(meta_dir, fname)) as f:
                    meta = json.load(f)
                    freshness[ticker] = meta.get('last_updated', '2000-01-01')
    ctx['entity_freshness'] = freshness

    # Fired signals
    fired_dir = 'signals/fired'
    ctx['fired_signal_tickers'] = set()
    if os.path.exists(fired_dir):
        for fname in os.listdir(fired_dir):
            if fname.endswith('.json'):
                with open(os.path.join(fired_dir, fname)) as f:
                    sig = json.load(f)
                    ctx['fired_signal_tickers'].add(sig.get('ticker', ''))

    # Completed task IDs (for dependency resolution)
    conn = sqlite3.connect(QUEUE_DB)
    conn.row_factory = sqlite3.Row
    completed = conn.execute(
        "SELECT id FROM tasks WHERE state = 'completed'"
    ).fetchall()
    ctx['completed_task_ids'] = {row['id'] for row in completed}
    conn.close()

    return ctx


def check_for_interrupts():
    """
    Check for time-sensitive events that should preempt the queue.
    Returns list of interrupt tasks to inject.
    """
    interrupts = []

    # Check for new 8-K filings for held companies
    # (This would query a local cache of SEC EDGAR RSS or a data provider)
    # For now, check a drop directory
    interrupt_dir = '.agent/interrupts'
    if os.path.exists(interrupt_dir):
        for fname in os.listdir(interrupt_dir):
            fpath = os.path.join(interrupt_dir, fname)
            with open(fpath) as f:
                interrupt = json.load(f)
            interrupts.append(interrupt)
            os.rename(fpath, fpath + '.processed')

    return interrupts


def ensure_recurring_tasks(conn, ctx):
    """
    If the queue has no pending signal_scan tasks and the last one
    was >6 hours ago, create one. Same for other recurring work.
    """
    now = datetime.utcnow()
    recurring = [
        {
            'category': 'signal_scan',
            'title': 'Routine signal scan',
            'description': 'Run all signal scanners against current universe',
            'interval_hours': 6,
            'estimated_tokens': 40000,
        },
        {
            'category': 'prediction_resolve',
            'title': 'Check prediction resolutions',
            'description': 'Check all open predictions for resolution',
            'interval_hours': 12,
            'estimated_tokens': 15000,
        },
        {
            'category': 'data_ingest',
            'title': 'Refresh market data',
            'description': 'Download latest price data, filings, news',
            'interval_hours': 8,
            'estimated_tokens': 30000,
        },
        {
            'category': 'error_review',
            'title': 'Review error ledger for patterns',
            'description': 'Analyze recent errors for systematic issues',
            'interval_hours': 48,
            'estimated_tokens': 20000,
        },
    ]

    for r in recurring:
        last = conn.execute("""
            SELECT completed_at FROM tasks
            WHERE category = ? AND state = 'completed'
            ORDER BY completed_at DESC LIMIT 1
        """, (r['category'],)).fetchone()

        should_create = False
        if not last or not last['completed_at']:
            should_create = True
        else:
            last_time = datetime.fromisoformat(last['completed_at'])
            if (now - last_time) > timedelta(hours=r['interval_hours']):
                should_create = True

        # Don't create if there's already a pending/in_progress one
        existing = conn.execute("""
            SELECT id FROM tasks
            WHERE category = ? AND state IN ('pending', 'ready', 'in_progress')
            LIMIT 1
        """, (r['category'],)).fetchone()

        if should_create and not existing:
            import uuid
            task_id = str(uuid.uuid4())[:8]
            conn.execute("""
                INSERT INTO tasks (id, created_at, updated_at, state, priority,
                    category, title, description, estimated_tokens)
                VALUES (?, ?, ?, 'pending', 0, ?, ?, ?, ?)
            """, (task_id, now.isoformat(), now.isoformat(),
                  r['category'], r['title'], r['description'],
                  r['estimated_tokens']))

    # Also: generate entity refresh tasks for stale entities
    for ticker, last_updated in ctx.get('entity_freshness', {}).items():
        days_stale = (now - datetime.fromisoformat(last_updated)).days
        if days_stale > 7:
            existing = conn.execute("""
                SELECT id FROM tasks
                WHERE category = 'entity_refresh' AND entity = ?
                AND state IN ('pending', 'ready', 'in_progress')
                LIMIT 1
            """, (ticker,)).fetchone()
            if not existing:
                import uuid
                task
