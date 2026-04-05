# Biomedical Database Freshness Probe

**Date:** 2026-04-05

## Summary Table

| # | Database | Last Update | Frequency | Format | Approx Size | Status |
|---|----------|-------------|-----------|--------|-------------|--------|
| 1 | **CTD** (ctdbase.org) | Monthly (NAR 2025 paper: Jan 2025) | Monthly bulk refresh | CSV/TSV bulk downloads (gzipped) | ~94M relationships; multi-GB compressed | **Active** |
| 2 | **TWOSIDES** (Tatonetti Lab) | Original release ~2012; promised 2022 update never shipped | **Frozen** — abandoned | MySQL dump / flat files via nsides.io | 4.6M drug-drug-effect pairs | **Frozen academic release** |
| 3 | **DisGeNET** (disgenet.com) | v25.4 — January 8, 2026 | Quarterly (~4 releases/yr: v25.1-v25.4 in 2025-2026) | REST API + bulk TSV/CSV downloads | ~1.3M gene-disease associations, ~680K variant-disease | **Active; commercialized** |
| 4 | **SemMedDB** (NLM/NIH) | v43_R — final update, data through May 8, 2024 | **Discontinued** Dec 31, 2024 | MySQL SQL + CSV (gzipped) | 37.2M citations, 130.5M predications, ~25 GB uncompressed | **Dead — final version** |
| 5 | **PheWAS Catalog** (Vanderbilt) | Original catalog ~2013; PhecodeX v1.0 is the successor | **Frozen** — original catalog not updated | CSV download + web browse | 3,144 SNPs x 1,358 phenotypes | **Legacy; use PhecodeX/PheWAS tools** |
| 6 | **HPO** (hpo.jax.org) | v2026-02-16 (Feb 16, 2026) | ~Bimonthly (8 releases in 2025, 2 in 2026 so far) | OWL, OBO, JSON via GitHub + PURL | ~18K terms; ontology files <100 MB | **Active, well-maintained** |
| 7 | **Reactome** (reactome.org) | V95 — December 3, 2025 | Quarterly (V91-V95 over 2024-2025) | Neo4j dump, MySQL dump, BioPAX3, SBML, GMT, PSI-MITAB, SVG/PNG | 16,200 reactions, 2,848 pathways, 32,318 proteins; multi-GB | **Active, quarterly** |
| 8 | **SIDER** (sideeffects.embl.de) | SIDER 4.1 — October 21, 2015 | **Frozen** — no updates since 2015 | TSV flat files via FTP | 1,430 drugs, 5,868 side effects, 139,756 pairs | **Frozen since 2015** |
| 9 | **Hetionet** (het.io) | v1.0 — 2017 (Himmelstein thesis) | **Frozen** — academic release | Neo4j dump, JSON, TSV | 47K nodes, 2.25M edges, 29 source databases | **Frozen since 2017** |

## Detailed Notes

### 1. CTD (Comparative Toxicogenomics Database)
- **NAR 2025 update paper** (PMID 39385618) describes 20th anniversary release with 94M toxicogenomic relationships
- Downloads are behind CAPTCHA (anti-bot), so no direct programmatic scraping
- Bulk CSV files include: chemical-gene interactions, chemical-disease associations, gene-disease associations, chemical-phenotype interactions, exposure-disease associations
- Monthly update cadence confirmed in their documentation
- [SOURCE: https://academic.oup.com/nar/article/53/D1/D1328/7816860]

### 2. TWOSIDES / OffSIDES / OnSIDES
- **TWOSIDES** (drug-drug interaction side effects) is effectively frozen. The nsides.io page says "these resources are quite a bit out of date" with a promised 2022 update that never materialized
- **OnSIDES** (successor, single-drug FDA label extraction) IS actively maintained — v3.1.0 released May 8, 2025, with ongoing quarterly updates
- TWOSIDES data: mined from FDA AERS reports, ~4.6M drug-drug-effect pairs
- OnSIDES is the actively maintained replacement for single-drug adverse events
- [SOURCE: https://nsides.io/, https://github.com/tatonetti-lab/onsides/releases]

### 3. DisGeNET
- **Commercialized** — now disgenet.com (was .org), operated by MedBioinformatics Solutions SL
- Current version: v25.4 (Jan 8, 2026). Previous: v25.2 (Aug 2025)
- **Free Academic License exists** but excludes text-mined data from literature. Curated data only
- Full access requires paid Standard or Advanced subscription
- Biopreprint (Jan 5, 2026): "Accelerating Data-Driven Discovery in Disease Genomics" describes v25 architecture
- API available for programmatic access (also tiered)
- [SOURCE: https://disgenet.com/, https://support.disgenet.com/, https://blog.disgenet.com/disgenet-v25-2-whats-new/]

### 4. SemMedDB
- **Officially discontinued** as of December 31, 2024
- Final version: semmedVER43_R, data processed through May 8, 2024
- Contains 37,233,341 citations and 130,480,195 semantic predications (subject-predicate-object triples) from MEDLINE
- Available as MySQL SQL and CSV (gzipped) — still downloadable from archived page
- NLM states: "Indexing Initiative Github repository under development" as possible successor
- [SOURCE: https://lhncbc.nlm.nih.gov/temp/SemRep_SemMedDB_SKR/SemMedDB_download.html]

### 5. PheWAS Catalog
- **Original catalog is frozen** (~2013 vintage): 3,144 SNPs from NHGRI GWAS Catalog tested against 1,358 EMR phenotypes in 13,835 European-ancestry BioVU individuals
- **PhecodeX v1.0** is the active successor — updated phecode mappings used in current PheWAS analyses
- The phewascatalog.org site hosts both legacy catalog and current PhecodeX tools
- R packages (PheWAS) and Python library (PheTK) available
- The catalog itself is not continuously updated; it's a fixed dataset. The tools/phecodes around it are
- [SOURCE: https://phewascatalog.org/]

### 6. HPO (Human Phenotype Ontology)
- Latest: **v2026-02-16** (Feb 16, 2026) — 10 new terms, 29 obsoleted with replacements, 75 renamed
- Very active release cadence: 8 releases in 2025, 2 in 2026 Q1
- Available via GitHub releases (obophenotype/human-phenotype-ontology), OBO Foundry PURLs
- Formats: OWL, OBO, JSON
- ~18,000 phenotype terms; files are small (<100 MB)
- Also mirrored at EMBL-EBI OLS (version 2026-01-08 indexed there)
- [SOURCE: https://github.com/obophenotype/human-phenotype-ontology/releases]

### 7. Reactome
- Latest: **V95** (December 3, 2025). NAR 2026 paper published Dec 8, 2025
- Quarterly release cadence (V91 through V95 over 2024-2025)
- 16,200 reactions, 2,848 pathways, 32,318 proteins, 11,429 genes, 5,750 protein variants
- Formats: Neo4j graph DB (dump), MySQL dump, BioPAX Level 3, SBML (Level 3 v1), SBGN, GMT, PSI-MITAB, SVG/PNG diagrams
- Legacy Protege 2.0 and BioPAX Level 2 dropped as of V94
- CC-licensed, also on Zenodo (quarterly since V89)
- [SOURCE: https://reactome.org/about/news/284-v95-released, https://reactome.org/download-data]

### 8. SIDER
- **Frozen since October 21, 2015** (SIDER 4.1)
- Website (sideeffects.embl.de) is still live and downloadable
- 1,430 drugs, 5,868 side effects, 139,756 drug-SE pairs (39.9% with frequency info)
- TSV flat files on FTP
- NAR 2016 paper (Kuhn et al.) is the reference publication
- Zenodo mirror also exists (zenodo_7877719)
- No successor announced. For current drug side effect data, use OnSIDES (FDA labels) or DrugBank
- [SOURCE: http://sideeffects.embl.de/, http://sideeffects.embl.de/download/]

### 9. Hetionet
- **Frozen since 2017** (v1.0, Daniel Himmelstein's PhD thesis project)
- 47,031 nodes (11 types), 2,250,197 edges (24 types) from 29 source databases
- Available at het.io as Neo4j dump, JSON, TSV
- Listed in KG-Registry (kghub.org) as a knowledge graph resource
- Himmelstein's "Hetnet connectivity search" paper (GigaScience 2023) describes the search interface but the underlying data is still v1.0
- For a current alternative: PrimeKG (2025, Harvard) or BiomedGraphica (Nature MI, Mar 2025) are actively maintained biomedical KGs
- [SOURCE: https://het.io/, https://kghub.org/kg-registry/resource/hetionet/hetionet.html]

## Recommendations

**Use without reservation:** CTD, HPO, Reactome — actively maintained, well-funded, regular releases.

**Use with version awareness:** DisGeNET (free tier is limited; commercialized but current), OnSIDES (replacing TWOSIDES for single-drug AEs).

**Use as frozen snapshots only:** SIDER (2015), Hetionet (2017), PheWAS Catalog (2013), TWOSIDES (~2012). These are citeable historical datasets but should not be treated as current.

**Do not build on:** SemMedDB — officially discontinued Dec 2024. The 130M predications are still downloadable but will not be updated. NLM has not announced a direct successor, though UMLS continues to be updated (2025AA released May 2025).
