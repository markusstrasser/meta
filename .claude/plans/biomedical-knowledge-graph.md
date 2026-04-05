# Biomedical Knowledge Graph — Implementation Plan

> **Goal:** Unified queryable graph joining personal genomics (variants, phenotypes, PGx) with public biomedical databases (interactions, pathways, diseases, adverse events) + agent-maintained living edges from literature surveillance.
>
> **Key insight:** Dev cost ≈ 0. Filter on join quality and epistemic value, not effort.

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

## Architecture Decision: Neo4j + DuckDB (hybrid)

**Neo4j Community Edition (local, `brew install neo4j`)** for the multi-source biomedical graph. Graph traversal queries (multi-hop paths, convergence detection, shortest-path-to-phenotype) are native Cypher, painful in SQL.

**DuckDB stays** for variant lakehouse (columnar VCF queries) and structured analytics. No migration — different tools for different query shapes.

**PGx graph migrates** from DuckDB→Neo4j as a subgraph. The signed-edge sign-propagation logic moves to Cypher (relationship properties). NetworkX stays available as a Python escape hatch via `neo4j` driver → NetworkX conversion for algorithms Neo4j doesn't support natively.

**Join keys across all sources:**
- **Gene:** HGNC symbol (universal). SIGNOR uses UniProt → map via HGNC. CTD uses gene symbols directly.
- **Compound:** ChEBI ID preferred (CTD, SIGNOR both use it). UNII as fallback (DSLD uses it). Supplement common names as aliases.
- **Phenotype:** HPO code (already structured in selve). MeSH as bridge to CTD/DisGeNET disease terms.
- **Variant:** rsID (variant_registry already has 168).

---

## Phase 1: Neo4j Setup + Personal Subgraph (day 1)

### 1a. Install Neo4j Community Edition

```bash
brew install neo4j           # Community Edition, free, local
neo4j start                  # runs on localhost:7474 (browser) + bolt://localhost:7687
```

Config: `~/.neo4j/neo4j.conf` — set `server.memory.heap.max_size=2G`, `dbms.security.auth_enabled=false` (local only).

### 1b. Load existing PGx graph into Neo4j

Script: `selve/scripts/connectors/load_pgx_to_neo4j.py`

Read `pgx.duckdb` nodes + edges → Cypher `CREATE` statements. Preserve all existing properties (sign, weight, evidence, pmid, personal_genotype, activity_modifier).

Node labels: `:Compound`, `:Gene`, `:Enzyme`, `:Metabolite`, `:Receptor`, `:Phenotype`, `:Variant`
Edge types: `INTERACTS_WITH`, `METABOLIZES`, `PRODUCES`, `ACTIVATES`, `INHIBITS` (map from sign ±1)

### 1c. Load personal variants + phenotypes

- Import variant_registry.json (168 rsIDs) as `:Variant` nodes linked to `:Gene` nodes via `HAS_VARIANT`
- Import HPO phenotype contracts as `:Phenotype` nodes with HPO codes
- Import active-protocol supplements as `:Supplement` nodes (subset of `:Compound`)
- Create `:Person {name: "self"}` node with edges to variants, phenotypes, supplements

### 1d. Load SIGNOR (already cached)

Read `signor_human.tsv` → create edges with sign, mechanism, PMID. 42K edges.
Filter: keep chemical→protein, protein→protein, protein→phenotype. Skip complex/family-level.

**Validation:** After Phase 1, the personal PGx graph should be queryable in Neo4j with same results as current DuckDB+NetworkX. Run the sign-propagation queries from `pgx.py` as Cypher and compare.

---

## Phase 2: CTD Integration (day 1-2)

The highest-value new data source. 94M curated chemical→gene interactions.

### 2a. Bulk download

CTD downloads are CAPTCHA-protected. Two options:
- **Manual download** (one-time): download `CTD_chem_gene_ixns.tsv.gz` from ctdbase.org/downloads
- **Monthly refresh:** launchd plist that alerts user to re-download (CAPTCHA prevents full automation)

### 2b. Filter & load

Full CTD is 94M rows — too large. Filter to:
1. Chemicals matching our 30 supplement compound names + their ChEBI IDs
2. Genes in our variant_registry (168 genes) + PGx gene panel (20 genes)
3. Expand 1-hop: genes connected to our compounds, compounds connected to our genes

Expected filtered size: ~5K-50K edges (manageable).

Script: `selve/scripts/connectors/load_ctd.py`

### 2c. The killer join

```cypher
// Supplements that interact with YOUR variant-affected genes
MATCH (s:Supplement)-[:CTD_INTERACTS]->(g:Gene)<-[:HAS_VARIANT]-(v:Variant)
WHERE v.personal_genotype IS NOT NULL
RETURN s.name, g.symbol, v.rsid, v.phenotype, g.activity_modifier
ORDER BY s.name
```

This is the nutrigenomics interaction matrix — "your supplements hit your broken genes."

---

## Phase 3: Reactome Pathways (day 2)

### 3a. Load Reactome Neo4j dump

Reactome ships quarterly as a Neo4j dump. Download from reactome.org/download-data → "Graph Database" → `reactome.graphdb.dump`.

Load directly: `neo4j-admin database load --from-path=reactome.graphdb.dump reactome`

But: Reactome's Neo4j schema is complex (100+ node labels). Don't load the whole thing. Extract:
- Pathway nodes (2,848)
- Gene/protein→pathway membership edges
- Pathway hierarchy (parent→child)

Script: `selve/scripts/connectors/load_reactome.py` — reads the dump or uses Reactome Content Service REST API (https://reactome.org/ContentService/) to fetch pathway membership for our gene list.

### 3b. Pathway convergence queries

```cypher
// Which supplements converge on the same pathway?
MATCH (s1:Supplement)-[:CTD_INTERACTS]->(g1:Gene)-[:IN_PATHWAY]->(p:Pathway)
      <-[:IN_PATHWAY]-(g2:Gene)<-[:CTD_INTERACTS]-(s2:Supplement)
WHERE s1 <> s2 AND s1.name < s2.name  // avoid duplicates
RETURN s1.name, s2.name, p.name, collect(DISTINCT g1.symbol) + collect(DISTINCT g2.symbol) AS genes
ORDER BY size(genes) DESC
```

**Note:** `gene_pathway_mappings.json` (21MB, already in genomics) may be sufficient instead of loading full Reactome. Check if it has pathway IDs that can be resolved to names. If yes, skip the Reactome dump and just load this JSON.

---

## Phase 4: OnSIDES + CAERS Adverse Events (day 2-3)

### 4a. OnSIDES (replaces TWOSIDES + SIDER)

Download v3.1.0 from GitHub (tatonetti-lab/onsides). CSV of drug→adverse_event from FDA labels.
Filter to: our 2 drugs (tirzepatide, naltrexone) + any supplement compounds that appear.

Load as `:AdverseEvent` nodes with `:CAUSES` edges from `:Compound`.

### 4b. CAERS integration

Already wired as live API (`openfda_caers.py`). Periodically pull and load report counts as edge properties on existing `:Supplement`→`:AdverseEvent` edges.

### 4c. Combination risk surface

```cypher
// Compounds in your stack that share adverse event signals
MATCH (c1:Compound)-[:CAUSES]->(ae:AdverseEvent)<-[:CAUSES]-(c2:Compound)
WHERE c1.in_stack AND c2.in_stack AND c1 <> c2
RETURN c1.name, c2.name, ae.name, ae.severity
ORDER BY ae.severity DESC
```

---

## Phase 5: DisGeNET Gene-Disease (day 3)

### 5a. Free academic API

DisGeNET v25.4 free tier: curated associations only (text-mined excluded). Good enough — curated is higher quality.

API: `https://www.disgenet.org/api/gda/gene/{gene_id}` (requires free academic API key registration).

Filter to our gene list (168 + PGx 20). Load as `:Disease` nodes with `:ASSOCIATED_WITH` edges from `:Gene`.

### 5b. Three-way diagnostic join

```cypher
// Diseases associated with your variant-affected genes + matching your phenotype
MATCH (v:Variant)-[:IN_GENE]->(g:Gene)-[:ASSOCIATED_WITH]->(d:Disease)
MATCH (self:Person)-[:HAS_PHENOTYPE]->(ph:Phenotype)
WHERE v.personal_genotype IS NOT NULL
  AND d.hpo_codes IS NOT NULL
  AND ANY(code IN d.hpo_codes WHERE code IN [ph.hpo_id])
RETURN g.symbol, v.rsid, d.name, d.score, collect(ph.label) AS matching_phenotypes
ORDER BY d.score DESC
```

---

## Phase 6: Agent Surveillance Jobs (day 3-4)

These fill gaps no static database covers. Three jobs, each a launchd-scheduled script.

### 6a. Supplement-supplement interaction scanner (daily)

No database covers this. Agent scans biorxiv/pubmed for interaction evidence between specific pairs from our stack.

```
Schedule: daily, 6am
Script: selve/scripts/agents/scan_supplement_interactions.py
Method: search_preprints + Exa for each pair in our 153-pair matrix (batched, ~20 pairs/day rotating)
Output: append to Neo4j as :LITERATURE_EVIDENCE edges with PMID, date, confidence
Cost: ~$0.50/day
```

### 6b. Mechanism predication extractor (weekly)

Focused SemMedDB replacement. For our 30 supplement compounds, extract "compound VERB target" from new PubMed abstracts.

```
Schedule: weekly, Saturday
Script: selve/scripts/agents/extract_mechanism_triples.py
Method: search_papers for each compound (last 7 days), LLM extraction of subject-predicate-object
Output: append to Neo4j as edges with PMID provenance
Cost: ~$1/week
```

### 6c. GWAS association updater (monthly)

GWAS Catalog updates quarterly. Check for new associations for our 168 rsIDs.

```
Schedule: monthly, 1st
Script: genomics/scripts/update_gwas_associations.py (extends modal_gwas_catalog.py)
Method: re-download GWAS Catalog, diff against previous, flag new associations
Output: new :GWASAssociation edges in Neo4j + alert file
Cost: ~$0 (free API)
```

---

## Phase 7: Query Layer + MCP (day 4-5)

### 7a. Python query module

`selve/src/selve/biograph.py` — typed query functions wrapping Cypher:

```python
def supplement_gene_interactions(supplements: list[str]) -> list[Interaction]
def pathway_convergence(supplements: list[str]) -> list[PathwayOverlap]
def variant_drug_risks(variants: list[str]) -> list[RiskSignal]
def diagnostic_differential(phenotypes: list[str], genes: list[str]) -> list[Diagnosis]
def combination_adverse_events(compounds: list[str]) -> list[CombinationAE]
```

### 7b. MCP tool (optional, Phase 2+)

Expose key queries as MCP tools for agent access. Low priority — scripts + Cypher shell are fine initially.

### 7c. Notebook / dashboard

Jupyter notebook for interactive exploration: `selve/notebooks/biograph-explorer.ipynb`
Shows: personal interaction matrix, pathway convergence heatmap, risk surface.

---

## Data Refresh Schedule

| Source | Frequency | Method | Automated? |
|--------|-----------|--------|------------|
| SIGNOR | Quarterly | `fetch_signor.py` (existing) | Semi — run manually |
| CTD | Monthly | Manual download (CAPTCHA) + `load_ctd.py` | No — CAPTCHA blocks |
| Reactome | Quarterly | Download dump or REST API | Semi |
| OnSIDES | Quarterly | GitHub release download | Semi |
| DisGeNET | Quarterly | API pull | Yes (script) |
| HPO | Bimonthly | GitHub release download | Yes (script) |
| GWAS Catalog | Quarterly | `modal_gwas_catalog.py` (existing) | Yes |
| CAERS | Continuous | `openfda_caers.py` (existing) | Yes (live API) |
| Supplement interactions | Daily | Agent scan | Yes (launchd) |
| Mechanism triples | Weekly | Agent extraction | Yes (launchd) |
| New GWAS hits | Monthly | Agent check | Yes (launchd) |

---

## Phase Sequence & Dependencies

```
Phase 1 (Neo4j + personal) ─── no dependencies, start here
  │
  ├── Phase 2 (CTD) ─── needs Neo4j running + manual CTD download
  │
  ├── Phase 3 (Reactome) ─── needs Neo4j; check if gene_pathway_mappings.json suffices first
  │
  ├── Phase 4 (OnSIDES) ─── needs Neo4j
  │
  └── Phase 5 (DisGeNET) ─── needs Neo4j + free API key registration
        │
        └── Phase 6 (Agents) ─── needs graph populated for edge insertion
              │
              └── Phase 7 (Query layer) ─── needs all data loaded
```

Phases 2-5 are independent of each other (parallelize). Phase 6 needs the graph populated. Phase 7 wraps up.

---

## What NOT to Do

- **Don't load full CTD** (94M rows). Filter to our compounds + genes first.
- **Don't load full Reactome dump**. Check if `gene_pathway_mappings.json` is sufficient first.
- **Don't build a web UI**. Cypher shell + Python queries + notebook is enough.
- **Don't migrate variant lakehouse to Neo4j**. DuckDB on Parquet is the right tool for columnar VCF queries.
- **Don't automate CTD download** — CAPTCHA blocks it. Manual monthly download is fine.
- **Don't build an "interaction checker" tool** — the graph IS the tool. Write queries, not wrappers.

## Success Criteria

After all phases:
1. `supplement_gene_interactions(["ashwagandha", "NAC", "saffron"])` returns which of your variant-affected genes each compound touches
2. `pathway_convergence(my_stack)` identifies supplements converging on the same pathway
3. `combination_adverse_events(["LDN", "melatonin"])` returns combination AE signals
4. `diagnostic_differential(my_hpo_codes, my_genes)` suggests conditions not yet ruled out
5. Agent jobs surface new interaction evidence within 24h of publication
