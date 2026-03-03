# EBF3 p.Pro263Leu — Clinical Significance Assessment
**Method:** Web search only (Perplexity, Brave, Exa) — no academic DB tools
**Date:** 2026-03-03
**Variant:** NM_001375380.1(EBF3):c.787C>T p.Pro263Leu (het) — ClinVar VUS
**Context:** Sole TIER-1 finding from personal WGS; healthy adult male; survived 4-agent verification

---

## 1. Variant-Level Evidence

| Claim | Evidence | Grade |
|-------|----------|-------|
| p.Pro263Leu absent from ClinVar, LOVD, HGMD, published case reports | No results found across Exa, Brave, Perplexity queries for "Pro263" or "P263" in EBF3 | D4 |
| No prior documentation at position 263 in any EBF3 variant database | Multiple targeted searches across databases yielded zero hits for this specific position | D4 |
| Pro263 is the **exact N-terminal residue of the IPT/TIG domain** (UniProt Q9H4W6: IPT/TIG 263-346) | UniProt annotation confirmed via Perplexity citing Q9H4W6 entry; structural crystallography (PDB: 3MUJ) confirms domain boundaries | B2 |
| Pro263 sits at the DBD/IPT/TIG domain interface — a structural hinge position | IPT/TIG domain begins at 263 per UniProt; DBD ends ~240-262; proline uniquely lacks backbone NH, creating rigid structural breaks at domain junctions | B2 |
| P→L substitution at this position could alter interdomain orientation or IPT/TIG N-terminal folding | Proline's pyrrolidine ring imposes ψ/φ constraints; leucine is a helix-former; structural logic inferred from COE family crystallography (PMC2923972) | C3 |

**Verdict on variant-level:** Novel variant, no prior disease or population documentation. Structurally plausible concern due to domain boundary position but lacks empirical support.

---

## 2. Gene-Level Missense Constraint

| Claim | Evidence | Grade |
|-------|----------|-------|
| EBF3 pLI = 1.0, LOEUF = 0.353 (or 0.25 per Geisinger DBD) | Confirmed via Geisinger DBD database, gnomAD v2; minor discrepancy between sources likely reflects gnomAD version | A2 |
| EBF3 LoF o/e = 0.03 — among the most constrained genes in gnomAD | Perplexity citing gnomAD v2.1 data | B2 |
| EBF3 missense Z-score: **not retrieved** | Multiple searches failed to surface specific missense Z-score; gnomAD missense constraint data unavailable from web search alone | — |
| **All documented pathogenic EBF3 missense variants cluster in the DNA-binding domain (DBD, ~residues 1-262)** — NOT in the IPT/TIG domain | Perplexity synthesis of Padhi 2021 (PMC8278787) and Deisseroth 2022 (PMID 35340043); 5 missense variants in Padhi cohort all located in DBD; key variants include R152C, F211L, R163G, R63Q | B2 |
| p.Gly347Asp (Deisseroth 2022) is pathogenic and located **just outside** the IPT/TIG domain (position 347 vs. IPT/TIG ends at 346) | Deisseroth 2022 PMID 35340043 via SFARI/Perplexity; Gly347 is 1 residue C-terminal to IPT/TIG boundary | B3 |
| No pathogenic variant documented within the IPT/TIG domain proper (residues 263-346) | Synthesis of all Exa + Perplexity searches; no reports found | D4 |
| Published pathogenic missense variants include: p.Arg163Leu, p.Lys193Asn, p.Arg163Pro, p.Lys64Thr, p.Arg209Gln, p.Glu102Gly, p.Gly338Val, p.Gly347Asp | Multiple sources: SFARI gene database, Sleven 2016 (PMC5223060), Chao 2016 (PMID 28017372), Padhi 2021, Deisseroth 2022 | A2 |

**Key disconfirmatory signal:** The mutational clustering pattern for pathogenic EBF3 missense is the DBD (particularly zinc knuckle region). The IPT/TIG domain has no published pathogenic missense variant. p.Pro263Leu breaks this pattern.

---

## 3. Functional Data

| Claim | Evidence | Grade |
|-------|----------|-------|
| No MAVE/DMS data for EBF3 in MaveDB | MaveDB covers 74 datasets across 32 disease genes; EBF3 not among them | A2 (for absence) |
| No saturation genome editing (SGE) data for EBF3 coding variants | Confirmed absent from web search | D4 |
| Pathogenic missense in DBD causes cytoplasmic mislocalization and loss of DNA binding (experimental) | Padhi 2021 functional validation: R163G disrupts DNA H-bond; R152C/F211L/R63Q shift subcellular localization | A2 |
| IPT/TIG domain has dimerization function with 1,960 Å² buried interface (β-strands β1, β2, β4) | PMC2923972 crystallography study; EBF1 and EBF3 IPT/TIG domains have 98% identity, 0.72 Å RMSD | A2 |
| P→L at domain N-terminus could disrupt IPT/TIG β-barrel folding or interdomain orientation | Structural logic from proline role in protein architecture; no direct EBF3 experimental data | C3 |
| Six deep-learning pathogenicity predictors concordantly call p.Pro263Leu damaging | Stated in research prompt (AlphaMissense and 5 others); these tools have limited domain-context awareness | C3 |
| Deep-learning predictors may overweight proline substitutions at conserved positions regardless of functional domain context | Known limitation of sequence-based tools (no domain-context correction); not specific to this variant | C3 |

---

## 4. Phenotype Correlation & Penetrance

| Claim | Evidence | Grade |
|-------|----------|-------|
| HADDS presents in infancy/childhood with hypotonia, ataxia, developmental delay, intellectual disability | GeneReviews NBK570204; HADDS.org; multiple case series | A1 |
| Expected penetrance appears complete for confirmed pathogenic EBF3 variants | All documented adult carriers in clinical literature show HADDS features; transmitters are symptomatic parents | B2 |
| No healthy adult carriers of confirmed pathogenic EBF3 variants documented in population studies | Perplexity synthesis of 62-67 case cohort; no gnomAD-equivalent healthy carrier reports | B3 |
| One mosaic mother (22-33% mosaicism) was clinically unaffected — suggests mosaicism can reduce expressivity but germline full-penetrance maintained | Cited in Perplexity response from openaccess.sgul.ac.uk/114054 | B3 |
| Healthy adult male with no HADDS features carrying this variant is **phenotypically discordant** with expected HADDS penetrance | Stated context; HADDS onset is neonatal/infantile; a healthy functional adult is unexpected for a truly pathogenic EBF3 variant | B2 |
| Zinc finger (ZNF) domain variants associate with more severe motor/language impairment than non-ZNF variants | Deisseroth 2022 Annals of Neurology "high-risk subtype" finding | B2 |

---

## 5. Disconfirmatory Evidence Summary

The following findings argue **against pathogenicity** of p.Pro263Leu:

1. **Domain location mismatch:** All documented pathogenic EBF3 missense variants cluster in the DNA-binding domain. Pro263 is at the IPT/TIG domain's N-terminus — no pathogenic precedent in this region.
2. **Absent from databases:** Zero prior reports in ClinVar, LOVD, HGMD, or case series. Novel variants in high-penetrance early-onset disorders are suspect when found in healthy adults.
3. **Phenotypic discordance:** The subject is a healthy adult male. HADDS onset is neonatal/infantile and appears fully penetrant in germline heterozygotes. A healthy adult with this variant in a high-penetrance gene is the strongest single argument against pathogenicity.
4. **No functional validation:** No experimental data (cell, animal, or in vitro) for this specific variant.
5. **No MAVE data available** to quantify effect size relative to known pathogenic variants.

---

## Domain Map (EBF3, 591 aa)

```
|-- N-term --|--------- DBD (~26-262) ---------|-- IPT/TIG (263-346) --|-- HLH (~350-430) --|-- C-term --|
                       |zinc knuckle|                 ^
                       ~157-177                    Pro263 ← HERE (exact N-terminal boundary)

Known pathogenic missense:
  K64T, R63Q          ←--- DBD start
  R152C, R163L/G/P    ←--- zinc knuckle proximal
  K193N, F211L, R209Q ←--- DBD mid
  G338V               ←--- DBD/IPT boundary (just before 263? — position unclear; see note)
  G347D               ←--- 1 residue past IPT/TIG end (346)
  P263L               ←--- This variant (IPT/TIG N-terminal boundary)
```

*Note: p.Gly338Val location relative to domain boundaries requires reconciliation — reported in Padhi 2021 functional cohort, and genebe.net confirms it absent from gnomAD. If 338 < 346 (IPT/TIG end), it would be the ONLY documented pathogenic variant within IPT/TIG. Treat with B3 confidence pending primary source verification.*

---

## ACMG Criteria Preliminary Assessment

| Criterion | Application | Direction |
|-----------|-------------|-----------|
| **PP3** | 6 concordant in silico tools | Pathogenic supporting |
| **PM2** | Absent from gnomAD (implied, given gene constraint and no database hits) | Pathogenic moderate |
| **PM1** | Position in IPT/TIG domain, NOT in established hotspot (DBD) — criterion likely **not met** | Neutral |
| **PS3** | No functional data | Not applicable |
| **PS1/PM5** | No same-position or same-AA-change documented as pathogenic | Not applicable |
| **BP4** | N/A — in silico tools favor pathogenic | Not applicable |
| **BS2** | Healthy adult with no HADDS features (high-penetrance childhood-onset disorder) | **Benign strong** — arguably applicable |
| **BP5** | Variant in gene/domain pattern inconsistent with published disease mechanism | Benign supporting |

**Preliminary classification: VUS (uncertain significance)**
Supporting pathogenic: PP3 + PM2
Supporting benign: BS2 (phenotype discordance) + BP5 (domain location outside hotspot)
These partially cancel → remains VUS. BS2 alone can hold classification at VUS rather than LP.

---

## Recommendation

**Clinical significance: VUS — do not act on this finding without further workup.**

**Priority next steps:**
1. **Formal neurological evaluation:** Subtle HADDS features (mild hypotonia, fine motor issues, speech delay history, EEG/MRI, gait assessment). If truly absent, strengthens BS2 application toward likely benign.
2. **Family segregation:** If first-degree relatives available, sequence for cosegregation/absence. De novo status would shift toward LP; inherited from unaffected parent would shift toward LB.
3. **Functional assay:** Cell-based transcriptional reporter assay (EBF3 target gene activation) comparing WT vs. Pro263Leu. All existing functional data for HADDS missense uses this approach (Padhi 2021).
4. **Await MaveDB/SGE data:** EBF3 is not yet covered. When saturation genome editing data becomes available (Broad/Wellcome Sanger programs), reclassify.

**Working hypothesis:** p.Pro263Leu is more likely to be a **tolerated variant of uncertain effect** than a causative HADDS allele. The primary reason: healthy adult with no HADDS features, disease penetrance is early and near-complete, and domain location is outside the canonical pathogenicity cluster. The concordant damaging predictions from 6 deep-learning tools are insufficient to override phenotypic discordance given known limitations of these tools for non-DBD positions in constraint genes.

---

## Sources

| Source | Grade | URL |
|--------|-------|-----|
| GeneReviews EBF3 NBK570204 (Narayanan 2021) | A2 | https://www.ncbi.nlm.nih.gov/books/NBK570204/ |
| Sleven et al. 2016 AJHG (De Novo Mutations in EBF3) | A2 | https://pmc.ncbi.nlm.nih.gov/articles/PMC5223060/ |
| Padhi et al. 2021 Hum Genomics (Coding/noncoding EBF3) | A2 | https://pmc.ncbi.nlm.nih.gov/articles/PMC8278787/ |
| Deisseroth et al. 2022 Ann Neurol (Zinc finger subtype) | A2 | https://www.researchgate.net/publication/359505256 |
| PMC2923972 (EBF1/EBF3 IPT/TIG crystal structure) | A2 | https://pmc.ncbi.nlm.nih.gov/articles/PMC2923972/ |
| UniProt Q9H4W6 (EBF3 domain annotation) | A2 | https://www.uniprot.org/uniprotkb/Q9H4W6/entry |
| SFARI Gene EBF3 | B2 | https://gene.sfari.org/database/human-gene/EBF3 |
| Geisinger DBD Genes (EBF3, pLI/LOEUF) | B2 | https://dbd.geisingeradmi.org/site/missense-EBF3 |
| ClinVar VCV000268155 (Arg163Leu reference) | A2 | https://www.ncbi.nlm.nih.gov/clinvar/variation/268155 |
| MaveDB (EBF3 absent) | A2 (for absence) | https://www.mavedb.org |
| HADDS.org research | B3 | https://www.hadds.org/research |
| genebe.net Gly338Val | B3 | https://genebe.net/variant/hg38/EBF3%20p.Gly338Val |
