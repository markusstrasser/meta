To design a system that maximizes the rate of error correction via market feedback, we must discard standard enterprise data architectures. Standard architectures are designed to preserve state and serve queries. This system is designed to **falsify conjectures**. 

Because you are a single user on a single machine relying on Claude Code, the architecture must be strictly local, declarative, and entirely version-controlled. We replace distributed infrastructure with raw compute (DuckDB) and agentic loops (MCP + LLM).

Here is the blueprint for the Intelligence Engine.

---

### 1. The Core Architecture: "Everything as a Git Commit"

The entire system state—data schemas, extraction scripts, entity mappings, signal rules, and trading hypotheses—lives in a Git repository. 

*   **Why?** The constitution mandates that "the error-correction ledger IS the moat." Git provides out-of-the-box, immutable provenance. When the market refutes a hypothesis, you can checkout the exact commit of the database and rules that generated it to understand *why*.
*   **The Stack:** DuckDB (data), Python (orchestration), MCP Servers (exposing DuckDB, web scraping, and Git to Claude Code), and Markdown/JSON (for entity files and theses).

### 2. The Data Transformation Pipeline (Provenance Preserved)

Standard pipelines destroy information via aggregation. We maintain a strict separation of layers, preserving provenance through foreign keys that trace all the way back to the source URL.

*   **Layer 0: The Vault (Raw Files):** Compressed Parquet/CSV files on your SSD. Immutable.
*   **Layer 1: The Epistemic Lake (DuckDB Raw):** Exact 1:1 copies of the Vault files in DuckDB. Added columns: `ingest_timestamp`, `source_url`, `admiralty_grade` (e.g., [A1] for SEC EDGAR).
*   **Layer 2: The Translation Layer (Entity Mapping):** We do *not* join raw tables directly. Instead, we maintain a `Master_Entity` table and a `Cross_Reference` table. 
*   **Layer 3: The Signal Layer (Conjectures):** A directory of `.sql` files. Each query reads from Layer 1, joins through Layer 2, and outputs anomalous events. 
*   **Layer 4: The Graph (Entity Files):** A directory of Markdown files (e.g., `entities/US/BPMC.md`). Claude Code compiles Layer 3 signals into text, updating base rates and asserting probabilities.

### 3. The Highest-Leverage Subsystem: The Identity Resolution Engine

**This is the subsystem that makes everything else easier.** Raw data is a commodity; the *resolved graph* is the moat. If you solve cross-domain entity matching, alpha naturally falls out.

**How it works without a heavy Graph DB:**
1.  **Central UUID:** Every real-world company gets a `Sys_ID`.
2.  **The Rosetta Stone Table:** A DuckDB table mapping `(Native_ID_Type, Native_ID, Sys_ID)`. (e.g., `('CIK', '0001018724', 'UUID-123')`, `('UEI', 'ABC123XYZ', 'UUID-123')`).
3.  **Agentic Resolution via MCP:** 
    *   When a new dataset is added (e.g., OSHA violations), an MCP tool attempts deterministic matching (exact name, address, ticker).
    *   For the unmapped remainder, the system triggers Claude Code. Claude uses a `web_search` MCP and an `edgar_search` MCP to figure out that "Acme Manufacturing LLC" is a subsidiary of "Acme Corp" (Ticker: ACME).
    *   Claude **commits** the new mapping to the Rosetta Stone table. *The agent does the grunt work of entity resolution asynchronously.*

### 4. Scoring and Signal Fusion: Bayesian Log-Odds

Multiple weak signals (a delayed SEC filing + a spike in CFPB complaints + a director resigning) must fuse into a tradable probability. 

*   **The Base Rate:** Every entity file starts with the baseline probability of an IWM stock beating the index over 90 days.
*   **The Weighting:** Each `.sql` signal generates a Bayes Factor (multiplier). 
*   **How it learns:** Initially, weights are naive. As trades resolve, a script calculates the actual predictive power of each `.sql` file. If a rule fires 10 times and the stock drops 8 times, the weight of that `.sql` file automatically adjusts upward. *The math handles the fusion; the market tunes the weights.*

### 5. Self-Improvement Mechanics: The "Autopsy" Loop

The constitution states: "Every missed surprise becomes a rule." This is how the system compounds.

1.  **The Target:** A nightly cron job checks the Russell 2000. It finds any stock that moved >15% on high volume (a "Surprise").
2.  **The Falsification Check:** Did we have an active hypothesis predicting this?
3.  **The Autopsy (If Missed):** 
    *   The system spawns Claude Code with the prompt: *"Ticker XYZ moved 18% today. We missed it. Here is read-only access to our DuckDB containing all data on XYZ from the last 90 days. Find the leading indicator we ignored."*
    *   Claude queries government contracts, FDA adverse events, insider trades.
    *   If Claude finds that a $50M DOD contract was awarded 14 days ago, it writes a new `.sql` signal file to catch this next time, grades it, and submits a Git PR.
    *   You approve the PR. The intelligence engine has successfully corrected an error.

### 6. The Minimum Viable Feedback Loop (MVFL)

Before ingesting 50 datasets, build the shortest path to a market refutation.

1.  **Data:** Ingest *only* CFPB complaints (CSV) and a master ticker list.
2.  **Resolution:** Map CFPB company names to Tickers (using Claude to resolve the hard ones).
3.  **Signal:** Write one `CFPB_Velocity.sql` rule: *Flag companies with a >3-sigma spike in complaints over a 14-day trailing window compared to their 1-year baseline.*
4.  **Hypothesis:** Agent drafts a standard markdown outbox file: *"Short thesis on Ticker [X]. 3.2x base rate complaint spike. [F3] confidence."*
5.  **Action:** Paper trade based on Fractional Kelly sizing rules. 
6.  **Review:** 30 days later, run the PnL script. Update the Bayes weight of the CFPB rule. 

### 7. What You Should NOT Build (Anti-Patterns for this Context)

*   **Do not build a UI/Dashboard.** Market visualization is commodity. Read Markdown files and Git diffs. If you need a chart, let Python output a static PNG to a folder. 
*   **Do not build Airflow/Prefect.** Standard cron or simple Python loops (`while True: sleep(86400)`) are fine. Failure states should simply exit and let you (the human) restart.
*   **Do not build an LLM RAG pipeline (Vector DB).** Vector embeddings abstract away provenance and blur exact details. Use DuckDB Full-Text Search and exact SQL queries.
*   **Do not stream data.** Alpha in small-caps doesn't disappear in milliseconds; it takes days for the market to price in a messy government contract or a CFPB spike. Daily batch pulls at midnight are 100% sufficient.

### Summary of Daily Operation

1.  **Midnight:** Python script downloads delta files from FDA, SEC, etc., loads into DuckDB.
2.  **1:00 AM:** Unmapped entities are passed to Claude Code (via MCP) for identity resolution.
3.  **2:00 AM:** All `.sql` signal rules are run. Anomalies are written to a `Signals` table.
4.  **3:00 AM:** Claude Code reviews the highest-probability entities. It explicitly tries to falsify the thesis. If the thesis survives, it generates an Outbox file (e.g., `proposals/2026-02-14-BUY-BPMC.md`).
5.  **Morning:** You review the Markdown files. You execute the trades in IBKR.
6.  **Weekend:** The Autopsy script runs on the week's missed market moves, drafting new `.sql` rules to plug the gaps in your edge.
