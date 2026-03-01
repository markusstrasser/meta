The year is 2026. The easy alpha from basic alt-data (like credit card receipts and satellite parking lot imagery) has been arbitraged away by mega-funds with massive compute. But in the $500M-$5B market cap space, there is a structural blind spot: **mega-funds don't care enough to model the idiosyncratic complexities of small caps, and retail/small funds don't have the data infrastructure to join 50+ regulatory datasets.** 

Your edge on a single Mac with DuckDB is **relational creativity**—finding the hidden graph edges that connect human behavior, regulatory friction, and corporate distress before it hits the 10-K.

Here are the non-obvious, cross-disciplinary signals to program into your engine:

### 1. Cross-Dataset Joins Nobody Makes

**Signal 1: The "Deferred Maintenance" Cascade**
*   **Mechanism:** When a company faces a cash crunch, they don't immediately announce it. They cut corners. They delay equipment maintenance (triggering EPA emission violations), push workers harder (triggering OSHA safety violations), and delay paying suppliers (triggering mechanic's liens in local court data).
*   **Key Join:** EPA ECHO database + OSHA enforcement + Local/Federal Court dockets (liens) + SEC 10-Q (capex spend).
*   **Data Lag:** 30–60 days (OSHA/EPA reporting lags).
*   **Alpha Half-Life:** 3–6 months. It predicts the *next* catastrophic earnings miss.
*   **Novelty:** High. Quants look at OSHA for ESG scores, not as a real-time proxy for liquidity crises.

**Signal 2: The "Brain Drain to Quality Collapse" Pipeline**
*   **Mechanism:** Great scientists and engineers leave before a product fails. If H-1B visa transfers (foreign workers moving to competitors) spike, followed by a drop in patent filings, it means the R&D pipeline is dead. If this happens at a biotech, the next FDA inspection (Form 483) will likely result in a Warning Letter. 
*   **Key Join:** DOL PERM/H-1B data + USPTO Patent Assignments + FDA Form 483 issuance.
*   **Data Lag:** DOL data is quarterly; FDA 483s are often posted within 45 days.
*   **Alpha Half-Life:** 6–12 months (long-tail short thesis).
*   **Novelty:** Very High. HR data is usually siloed from regulatory quality data.

### 2. Temporal Pattern Signals

**Signal 3: The "Broken Windows" Lead-Lag**
*   **Mechanism:** Operational sloppiness precedes financial sloppiness. An acceleration (second derivative) in minor, unrelated regulatory fines (e.g., fleet vehicles getting DOT violations, minor zoning disputes) is the leading indicator for SEC accounting restatements or CFPB actions. 
*   **Data Lag:** Varies, but DOT/local fines are near real-time.
*   **Alpha Half-Life:** 3 months.
*   **Novelty:** High. It applies criminological theory (Broken Windows) to corporate governance.

**Signal 4: Omission Alpha (Silence as Signal)**
*   **Mechanism:** Companies love to brag. If a $2B SaaS company has mentioned "Net Retention Rate" in 14 consecutive earnings calls, and suddenly omits it in the 15th, the metric has crashed. Similarly, if a company that usually files Form 4s (insider trades) within 2 days suddenly takes the maximum allowable time, legal is scrutinizing the trades.
*   **Key Join:** NLP on SEC EDGAR transcripts (measuring metric-specific token frequency) joined with historical baseline reporting behavior.
*   **Novelty:** Medium-High. NLP sentiment is common; NLP *omission tracking* is rare.

### 3. Network/Graph Signals

**Signal 5: Director Contagion & The "Lax Auditor" Cluster**
*   **Mechanism:** The world is one graph. If Director X is on the board of Company A (which just got investigated by the SEC for fraud) and Company B (a $1B market cap company), Company B is now high-risk. This is amplified if both companies share the same regional auditing firm. You short Company B before the contagion spreads.
*   **Key Join:** SEC DEF 14A (Proxy statements for board members) + PCAOB Auditor data + SEC Enforcement Actions.
*   **Data Lag:** 1–5 days (SEC enforcement to graph update).
*   **Alpha Half-Life:** Weeks. 
*   **Novelty:** High. Citadel maps the graph of mega-cap suppliers, but small-cap director/auditor contagion networks are mostly ignored.

### 4. Behavioral / Anthropological Signals

**Signal 6: The "Legal/Compliance Desperation" Hire**
*   **Mechanism:** When a company knows a massive regulatory hammer is about to drop (but hasn't disclosed it), they frantically hire to build a defense. A sudden spike in job postings for "Litigation Counsel," "FDA Remediation Specialist," or "Bankruptcy Restructuring Analyst."
*   **Key Join:** Scraped job postings (Internet Archive/Indeed) + Corporate Entity mapping.
*   **Data Lag:** Real-time (job postings are public immediately).
*   **Alpha Half-Life:** 1–2 months (the time between the hire and the regulatory public announcement).
*   **Novelty:** Medium. Funds scrape job boards for *growth* (e.g., hiring salespeople). Using job boards for *distress/litigation* proxying is much rarer.

### 5. Macro-Micro Bridges

**Signal 7: The Unhedged Tariff/Supply Chain Shock**
*   **Mechanism:** As of 2026, global trade policy is highly volatile. Mega-caps hedge currency and supply chain risks. $1B companies do not. If you know exactly which specific mid-cap companies import a raw material (via UN Comtrade and US Customs Bill of Lading data) that just had a tariff exclusion expire, you know exactly whose margins will compress next quarter.
*   **Key Join:** US Customs (Enigma/Panjiva equivalent data) + US Trade Representative (USTR) tariff schedules + SEC 10-K (Segment reporting).
*   **Data Lag:** Customs data lags by ~14 days.
*   **Alpha Half-Life:** 1 quarter (until earnings release).
*   **Novelty:** High. Bridging geopolitical macro directly to specific small-cap micro supply chains is computationally heavy, but DuckDB handles it beautifully.

### 6. Contrarian / Anti-Signals

**Signal 8: The "Kitchen Sink" Turnaround**
*   **Mechanism:** A high CFPB complaint velocity or SEC investigation usually tanks a stock. However, if a *new* CEO was appointed within the last 6 months, an explosion in bad news is actually a *buy signal*. It's the "Kitchen Sink" quarter—the new CEO is writing off all bad debt, settling all lawsuits, and taking the pain so that the baseline is reset for their tenure. Coupled with Insider Buying, this is a massive long signal.
*   **Key Join:** SEC Form 4 (Insider Buy) + SEC Form 8-K (CEO Change) + CFPB/Regulatory Fines (Spike).
*   **Data Lag:** 2–3 days.
*   **Alpha Half-Life:** 6–12 months (the time it takes the market to realize the turnaround is real).
*   **Novelty:** Very High. Standard quant models see "Fine + Complaints" and auto-short. Your engine sees the context (CEO change + insider conviction) and takes the other side.

### 7. Alpha Decay Detection

To measure the rate at which your system corrects its own errors, you need an automated **Decay Oracle**.

*   **How to detect crowding:** Monitor the correlation of your signal's returns against standard quantitative factor ETFs (Momentum, Value, Quality). If your proprietary "Deferred Maintenance" signal starts showing a 0.8 correlation with a generic Small-Cap Short-Interest ETF, the alpha has decayed into beta. You are no longer trading a unique insight; you are riding a crowded factor wave.
*   **The Meta-Signal:** The fastest decaying signals are raw data dumps (e.g., an FDA warning letter goes public). The slowest decaying signals are **multi-hop graph queries** (e.g., Director Contagion or Tariff Exclusions). 
*   **Execution in DuckDB:** Build a nightly job that regresses the simulated PnL of each of your 50+ signals against the broader small-cap index and standard factors. When the rolling 30-day alpha (residual return) hits zero, the system must automatically deprecate the signal and re-weight toward newly discovered cross-joins. 

By operating in the $500M-$5B space with multi-domain graph joins, you are effectively performing investigative journalism at computational scale—finding the truths companies are actively trying to hide, exactly where the big algorithms aren't looking.
