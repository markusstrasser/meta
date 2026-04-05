# Biomedical Knowledge Graph — Implementation Plan (v2)

> **Goal:** Unified queryable graph joining personal genomics (variants, phenotypes, PGx) with public biomedical databases (interactions, pathways, diseases, adverse events) + agent-maintained living edges from literature surveillance.
>
> **Key insight:** Dev cost ≈ 0. Filter on join quality and epistemic value, not effort.
>
> **v2 (2026-04-05):** Revised after cross-model review (Gemini 3.1 Pro + GPT-5.4). Key changes: no new graph engine (extend existing DuckDB + NetworkX), entity registry as Phase 0, staging layer for agent edges, dropped Reactome dump, fixed identifier assumptions and pair-count math. Review: `.model-review/2026-04-05-biomedical-knowledge-graph-plan-2ee406/`

## Architecture Decision: Extend DuckDB + NetworkX (no new engine)

**Why not Neo4j:** Over-engineered. JVM daemon, memory config, backup/restore, service lifecycle — all for <100K edges. Both review models flagged this as the #1 maintenance trap.

**Why not Kùzu:** Gemini proposed this as Neo4j alternative (embedded, Cypher, pip install). But we already have DuckDB + NetworkX and it works. Adding Kùzu is solving a problem that doesn't exist. The PGx graph queries are 5-10 line NetworkX operations, not complex Cypher. The `pgx.py` PgxGraph class already handles upsert, mutation, traversal. Kùzu's maturity and DuckDB integration are also unverified.

**What we do:** Extend `selve/indexed/pgx.duckdb` with new tables for each data source. Build the NetworkX DiGraph from all tables at query time (same pattern as today). DuckDB for storage + filtering, NetworkX for graph algorithms (sign propagation, shortest path, convergence detection, centrality).

**Rejected:** `duckdb-pgq` extension (Property Graph Queries) — potentially interesting but immature, and NetworkX is already working.

## What Already Exists (don't rebuild)

| Component | Location | Tech | Data |
|-----------|----------|------|------|
| PGx causal graph | `selve/indexed/pgx.duckdb` + NetworkX | DuckDB 6MB | Compound→enzyme→metabolite→receptor→phenotype, signed edges, personal genotypes |
| SIGNOR interactions | `selve/data/signor_human.tsv` | TSV 20MB (42K rows) | Chemical→protein, protein→protein, protein→phenotype, signed, PMIDs |
| KEGG drug metabolism | `selve/data/kegg/hsa0098{2,3}.xml` | KGML XML | CYP450 + other enzyme pathways |
| INDRA causal statements | `selve/scripts/connectors/fetch_indra.py` | REST API | Causal statements for 20 PGx genes |
| PharmGKB annotations | `selve/indexed/pharmgkb_parsed.json` | JSON 237KB | 395 gene-drug clinical annotations |
| GWAS Catalog | `genomics/scripts/modal_gwas_catalog.py` | DuckDB on Parquet | Personal VCF ∩ GWAS, pleiotropy network |
| Open Targets | `genomics/data/` (SSD mirror) | Parquet ~50GB | L2G, credible sets, studies, targets |
| Pathway mappings | `genomics/config/gene_pathway_mappings.json` | JSON 21MB | Gene→pathway membership |
| Variant registry | `genomics/config/variant_registry.json` | JSON 62KB | 168 rsIDs with positions |
| HPO phenotypes | `selve/config/phenotype/` + exports | JSON contracts | 6 HP terms, strict/broad, Phenopacket |
| Phenotype store | `selve/data/phenotype_contract/store.json` | JSON 118KB | Normalized observations, events, artifacts |
| Variant lakehouse | `genomics/scripts/variant_lakehouse.py` | DuckDB on Parquet | Cross-stage VCF queries (9 stages) |
| Supplement labels | `selve/scripts/dsld.py` | REST (DSLD API) | NIH label data for 16 supplements |
| Adverse events | `selve/scripts/openfda_caers.py` | REST (OpenFDA) | CAERS reports for stack |
| Nutrient composition | `selve/scripts/usda_fdc.py` | REST (USDA FDC) | Dietary nutrient lookup |
| Connectors pattern | `selve/scripts/connectors/` | Python scripts | fetch_kegg, fetch_signor, fetch_indra, seed_pgx_graph |

---

## Phase 0: Entity Resolution Registry (prerequisite for all phases)

**Why this is Phase 0:** The cross-model review identified identifier alignment as the #1 risk. CTD uses MeSH chemical IDs. DisGeNET uses UMLS disease IDs. Open Targets uses EFO/Ensembl. DSLD uses UNII. Naive string matching ("ashwagandha") will drop >50% of valid edges.

### 0a. Build entity registry

Create `selve/config/entity_registry.json` mapping each supplement and gene to all relevant IDs:

```json
{
  "compounds": {
    "ashwagandha": {
      "aliases": ["Withania somnifera", "KSM-66", "Sensoril"],
      "chebi": "CHEBI:xxxxx",
      "mesh": "D000000",
      "unii": "xxxxxxxxxx",
      "cas": "xxx-xx-x",
      "ctd_chemical_id": "D000000"
    }
  },
  "genes": {
    "CYP2D6": {
      "hgnc_symbol": "CYP2D6",
      "ncbi_gene_id": 1565,
      "uniprot": "P10635",
      "ensembl": "ENSG00000100197"
    }
  },
  "diseases": {
    "insomnia": {
      "hpo": "HP:0100785",
      "mesh": "D007319",
      "umls": "C0917801",
      "mondo": "MONDO:0005271",
      "efo": "EFO:0004698"
    }
  }
}
```

### 0b. Populate via automated lookup

Script: `selve/scripts/connectors/build_entity_registry.py`
- For compounds: query PubChem by name → get CID → cross-refs to ChEBI, MeSH, UNII, CAS
- For genes: HGNC REST API → NCBI, UniProt, Ensembl mappings
- For diseases: query MONDO API or OLS (Ontology Lookup Service) → HPO, UMLS, MeSH, EFO mappings

### 0c. Validation gate

All downstream loaders **reject entities not in the registry**. If CTD returns a compound not in `entity_registry.json`, it's skipped with a warning, not silently loaded. This prevents garbage edges.

---

## Phase 1: CTD Integration (highest-value new data source)

94M curated chemical→gene interactions. Filtered to personal subgraph.

### 1a. Bulk download

CTD downloads are CAPTCHA-protected. Options:
- **Manual download** (simplest): download `CTD_chem_gene_ixns.tsv.gz` from ctdbase.org/downloads
- **Investigate alternatives:** Check if PubChem or BioGRID mirrors CTD interaction data without CAPTCHA
- **Playwright automation:** If no mirror, script the CAPTCHA flow with headless browser

Do NOT build a launchd alert for manual re-download — that violates the autonomy principle.

### 1b. Filter & load into DuckDB

Full CTD is 94M rows. Filter to:
1. Chemicals matching our 30 supplement compounds via `entity_registry.json` (using CTD's MeSH chemical IDs)
2. Genes matching our variant-associated genes (map rsIDs → genes first — note: rsID→gene is many-to-many, gene count is NOT 168)
3. 1-hop expansion: genes connected to our compounds, compounds connected to our genes

Load into `pgx.duckdb` as a `ctd_interactions` table with columns: `compound_mesh_id, gene_ncbi_id, interaction_type, pmid_count, source='CTD'`.

Expected filtered size: ~5K-50K edges.

### 1c. NetworkX integration

Extend `pgx.py` to load CTD edges into the graph alongside SIGNOR/KEGG/INDRA edges. CTD edges get `evidence_class='curated_interaction'` to distinguish from causal edges (SIGNOR) and association edges (GWAS).

### 1d. The join

```python
# Supplements that interact with your variant-affected genes
def supplement_gene_interactions(graph, supplements, variant_genes):
    """Return CTD interactions between stack compounds and personal variant genes."""
    hits = []
    for compound in supplements:
        compound_id = entity_registry.resolve(compound, 'ctd_chemical_id')
        for gene in variant_genes:
            if graph.has_edge(compound_id, gene):
                edge = graph[compound_id][gene]
                hits.append({
                    'supplement': compound,
                    'gene': gene,
                    'interaction': edge.get('interaction_type'),
                    'evidence_class': edge.get('evidence_class'),
                    'pmids': edge.get('pmid_count'),
                })
    return hits
```

---

## Phase 2: Pathway Convergence (using existing data)

### 2a. Load gene_pathway_mappings.json into DuckDB

The 21MB `gene_pathway_mappings.json` already exists in genomics. Load as `gene_pathways` table in `pgx.duckdb`.

Do NOT load the Reactome Neo4j dump — 100+ node labels, schema mapping nightmare, marginal gain over existing JSON.

### 2b. Pathway convergence query

```python
def pathway_convergence(graph, supplements, gene_pathways):
    """Find supplements that converge on the same biological pathway."""
    # For each supplement, get its target genes (via CTD + SIGNOR)
    supp_genes = {s: set(graph.neighbors(entity_registry.resolve(s))) for s in supplements}
    
    # For each gene, get its pathways
    # Find pathway overlaps between supplement pairs
    overlaps = []
    for s1, s2 in itertools.combinations(supplements, 2):
        shared_pathways = set()
        for g1 in supp_genes[s1]:
            for g2 in supp_genes[s2]:
                p1 = set(gene_pathways.get(g1, []))
                p2 = set(gene_pathways.get(g2, []))
                shared_pathways |= (p1 & p2)
        if shared_pathways:
            overlaps.append((s1, s2, shared_pathways))
    return overlaps
```

---

## Phase 3: OnSIDES Adverse Events (day 2)

### 3a. Download OnSIDES v3.1.0

From GitHub (tatonetti-lab/onsides). Replaces frozen TWOSIDES (2012) + SIDER (2015).

Filter to: our 2 drugs (tirzepatide, naltrexone) + any supplement compounds that appear (likely sparse for supplements — most OnSIDES entries are prescription drugs).

### 3b. Load into DuckDB

`onsides_adverse_events` table. Combine with existing CAERS data.

### 3c. Combination risk query

```python
def combination_adverse_events(compounds, onsides_db, caers_db):
    """Find adverse events shared across compounds in the stack."""
    # OnSIDES: drug-level AEs from FDA labels
    # CAERS: product-level AE reports (live API)
    # Cross-reference: compounds sharing the same AE term
```

**Evidence class:** OnSIDES edges are `evidence_class='label_derived'`, CAERS edges are `evidence_class='spontaneous_report'`. Keep these separate in the graph — don't mix confidence levels.

---

## Phase 4: DisGeNET Gene-Disease (day 2-3, conditional)

### 4a. Assess marginal value first

Open Targets is already mirrored (50GB). DisGeNET's unique value over Open Targets:
- Curated gene-disease associations from literature (vs Open Targets' GWAS/L2G statistical associations)
- Evidence scoring (GDA score)

**Gate:** Before building the loader, check how many of our ~20 key genes have DisGeNET associations that Open Targets doesn't already cover. If overlap is >80%, skip this phase.

### 4b. The HPO bridge problem

DisGeNET uses UMLS disease IDs. Our phenotype system uses HPO codes. The Phase 5b Cypher query from v1 was invalid — DisGeNET doesn't have HPO-coded phenotypes.

**Fix:** Use MONDO ontology as the bridge. MONDO maps UMLS → OMIM → HPO. Load MONDO mappings into `entity_registry.json` disease entries. The diagnostic differential query then joins through MONDO:

```
Gene → (DisGeNET, UMLS disease ID) → (MONDO bridge) → (HPO phenotype) → your phenotypes
```

### 4c. Free academic API

Register for free academic key at disgenet.com. Pull curated associations for our gene list. Load into DuckDB with `evidence_class='curated_association'`.

---

## Phase 5: Agent Surveillance Jobs (day 3-4)

### Key change from v1: staging layer

Agent-extracted edges go into `selve/indexed/pending_edges.duckdb`, NOT the main graph. Human reviews and promotes via a simple CLI tool. This satisfies the epistemic discipline requirement.

### 5a. Supplement-interaction scanner (weekly, not daily)

**Corrected math:** 18 items in stack (16 supplements + 2 drugs) → C(18,2) = 153 pairs. At 20 pairs per run, full sweep takes ~8 runs. Weekly cadence = full sweep every ~2 months. NOT 24h freshness — that was mathematically impossible.

```
Schedule: weekly, Saturday
Script: selve/scripts/agents/scan_supplement_interactions.py
Method: search_preprints + Exa for rotating batch of 20 pairs
Output: append to pending_edges.duckdb with PMID, date, confidence
Cost: ~$0.50/week
```

### 5b. Mechanism predication extractor (biweekly)

Focused SemMedDB replacement. For 30 supplement compounds, extract "compound VERB target" from recent PubMed abstracts.

```
Schedule: biweekly, 1st and 15th
Script: selve/scripts/agents/extract_mechanism_triples.py
Method: search_papers for each compound (last 14 days), LLM extraction of subject-predicate-object
Output: append to pending_edges.duckdb with PMID provenance
Cost: ~$1/run
```

### 5c. GWAS association updater (quarterly)

GWAS Catalog updates quarterly. Align check cadence with source cadence.

```
Schedule: quarterly (matches GWAS Catalog release cycle)
Script: genomics/scripts/update_gwas_associations.py (extends modal_gwas_catalog.py)
Method: re-download GWAS Catalog, diff against previous, flag new associations
Output: alert file + new associations in pending_edges.duckdb
Cost: ~$0 (free API)
```

### 5d. Edge review CLI

```bash
# Review pending edges
uv run python3 scripts/review_pending_edges.py list       # show pending
uv run python3 scripts/review_pending_edges.py approve 42  # promote to main graph
uv run python3 scripts/review_pending_edges.py reject 42   # discard with reason
```

---

## Phase 6: Query Layer (day 4)

### 6a. Extend pgx.py

Add typed query functions to the existing `selve/src/selve/pgx.py` PgxGraph class:

```python
def supplement_gene_interactions(self, supplements: list[str]) -> list[dict]
def pathway_convergence(self, supplements: list[str]) -> list[dict]
def combination_adverse_events(self, compounds: list[str]) -> list[dict]
def diagnostic_differential(self, phenotypes: list[str]) -> list[dict]
```

All queries use NetworkX graph operations. No new engine needed.

### 6b. Evidence class filtering

Every query function accepts an `evidence_classes` parameter defaulting to `['curated_interaction', 'curated_causal', 'curated_association']`. Agent-extracted edges (`evidence_class='literature_extraction'`) are excluded by default — opt-in only.

### 6c. Notebook (optional)

`selve/notebooks/biograph-explorer.ipynb` for interactive exploration. Low priority — CLI queries are fine initially.

---

## Data Refresh Schedule

| Source | Frequency | Method | Automated? |
|--------|-----------|--------|------------|
| SIGNOR | Quarterly | `fetch_signor.py` (existing) | Semi — run manually |
| CTD | Quarterly | Manual download or Playwright | Semi (investigate automation) |
| Reactome | N/A | Using `gene_pathway_mappings.json` instead | N/A |
| OnSIDES | Quarterly | GitHub release download | Semi |
| DisGeNET | Quarterly | API pull (if Phase 4 passes gate) | Yes (script) |
| HPO/MONDO | Bimonthly | GitHub release download | Yes (script) |
| GWAS Catalog | Quarterly | `modal_gwas_catalog.py` (existing) | Yes |
| CAERS | Continuous | `openfda_caers.py` (existing) | Yes (live API) |
| Supplement interactions | Weekly | Agent scan → pending_edges | Yes (launchd) |
| Mechanism triples | Biweekly | Agent extraction → pending_edges | Yes (launchd) |

---

## Phase Sequence & Dependencies

```
Phase 0 (Entity Registry) ─── prerequisite for everything
  │
  ├── Phase 1 (CTD) ─── needs entity registry for compound ID mapping
  │
  ├── Phase 2 (Pathways) ─── uses existing gene_pathway_mappings.json
  │
  ├── Phase 3 (OnSIDES) ─── independent
  │
  └── Phase 4 (DisGeNET) ─── conditional on value gate + MONDO bridge
        │
        └── Phase 5 (Agents) ─── needs graph populated, writes to staging
              │
              └── Phase 6 (Query layer) ─── extends existing pgx.py
```

Phases 1-4 are independent of each other (parallelize after Phase 0).

---

## What NOT to Do

- **Don't add a new graph engine** (Neo4j, Kùzu, or duckdb-pgq). DuckDB + NetworkX is sufficient and proven.
- **Don't load full CTD** (94M rows). Filter via entity registry.
- **Don't load Reactome dump**. Use existing `gene_pathway_mappings.json`.
- **Don't let agents write directly to the main graph**. Staging layer + human review.
- **Don't build a launchd CAPTCHA reminder**. Either automate CTD download or accept quarterly manual refresh.
- **Don't assume identifier alignment**. Entity registry first, load data second.
- **Don't mix evidence classes in graph queries**. Curated vs association vs spontaneous report vs LLM-extracted have different confidence levels.

## Success Criteria

1. Entity registry covers ≥90% of stack compounds with at least one cross-database ID
2. `supplement_gene_interactions(my_stack)` returns CTD interactions filtered to personal variant genes
3. `pathway_convergence(my_stack)` identifies supplements converging on shared pathways using existing JSON
4. `combination_adverse_events(["LDN", "melatonin"])` returns combination AE signals from OnSIDES + CAERS
5. Agent jobs populate `pending_edges.duckdb` on schedule; zero unreviewed edges in main graph
6. Total new dependencies: 0 (all in existing DuckDB + NetworkX + Python stdlib)
