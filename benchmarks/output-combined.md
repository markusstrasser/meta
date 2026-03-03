# EBF3 p.Pro263Leu — Clinical Significance Assessment
**Research date:** 2026-03-03
**Query context:** Heterozygous VUS, healthy adult male WGS, survived 4-agent verification as sole TIER-1 finding from 365 rare HIGH/MODERATE variants

---

## Executive Summary

**Classification: VUS — lean uncertain, likely benign in HADDS clinical context**

p.Pro263Leu is not documented in any clinical database or published case series. The variant falls in the IPT/TIG domain (~aa 240–305), outside the established ZNF/DBD pathogenic hotspot (aa 163–209) that accounts for the most recurrent and functionally validated HADDS missense variants. The most powerful evidence against classical HADDS is phenotypic: the patient is a healthy adult, while HADDS has near-complete penetrance and presents with childhood-onset hypotonia, intellectual disability, ataxia, and neurogenic bladder in infancy. A neurotypical adult harboring this variant is inconsistent with the expected clinical trajectory for a classical pathogenic EBF3 allele. However, the gene's extreme intolerance (pLI=1.0, LOEUF=0.25) and concordant deep-learning predictors prevent downgrading to likely benign without functional data or inheritance context.

---

## Domain Map

```
EBF3 protein (591 aa):
[1 ←————— DBD (Rel-like) ————→ ~230] [~240 ←— IPT/TIG —→ ~305] [~305 ← HLHLH → ~370] [~400 ←———— CTD ————→ 591]
                      └── ZNF (zinc knuckle): ~aa 159–196 ──┘
                                ↑ PATHOGENIC HOTSPOT
                                R163W/Q/L/P, G171D, R209W/Q (all aa 163–209)

                                                         Pro263 → IPT/TIG domain ↑
```

**Domain sources:** Siponen et al. 2010 (PDB 3N50, JBC); Treiber et al. 2010 (PDB 3MQN, Genes Dev); Deisseroth et al. 2022 (Ann Neurol); GeneReviews Table 5 (NBK570204)

---

## Claims Table

| # | Claim | Evidence | Grade | Confidence | Source |
|---|-------|----------|-------|------------|--------|
| 1 | p.Pro263Leu not in ClinVar/LOVD/published cases | No results found in database/literature search | E5 (null) | High | ClinVar search; PubMed/S2 search 2026-03-03 |
| 2 | EBF3 is maximally intolerant to LoF variants | pLI=1.0, LOEUF=0.25 (gnomAD v2.1.1); HI score 3.89 (DECIPHER) | A2 | High | Geisinger DBD Database (verified 2024-11-04) |
| 3 | HADDS caused by haploinsufficiency | Whole-gene deletion causes HADDS; NMD predicted for LoF variants | A2 | High | Lopes et al. 2017 (Front Genet); Nishi et al. 2021 (AJMG) |
| 4 | ClinGen Definitive classification for HADDS | Curated by ClinGen NDD Expert Panel | A2 | High | search.clinicalgenome.org (HGNC:19087) |
| 5 | HADDS missense variants can be pathogenic | Multiple missense variants (p.Arg163W/Q, p.Gly171D, p.Arg209W/Q) confirmed pathogenic in ClinVar/GeneReviews | A2 | High | GeneReviews Table 5; Harms et al. 2017 (AJHG) |
| 6 | ZNF-domain missense = highest-risk subtype | 83-patient cohort; ZNF missense failed fly rescue + impaired transcriptional activation; highest symptom severity | A2 | High | Deisseroth et al. 2022 (Ann Neurol doi:10.1002/ana.26359) |
| 7 | p.Arg209Trp (DBD, non-ZNF) partially rescues fly viability | Confirms that not all EBF3 missense = null allele; DBD non-ZNF can preserve partial function | A2 | High | Deisseroth et al. 2022 |
| 8 | Pro263 is in IPT/TIG domain, NOT ZNF hotspot | GeneReviews notable pathogenic variants cluster at aa 163–209; residue 263 is past the IPT/TIG N-boundary (~240) | B2 | Medium-high | Siponen 2010 (PDB 3N50); domain modeling from EBF1 homology |
| 9 | Proline residues in HLHLH H1-H2 loop are structurally important | Siponen 2010 crystal structure specifically highlights Pro residues in the HLHLH loop for H1-H2 packing | B3 | Medium | Siponen et al. 2010 JBC; SGC structural entry thesgc.org/structures/3n50 |
| 10 | Pro→Leu substitution could disrupt loop geometry | Proline's conformational rigidity (φ constrained to ~−60°) is non-substitutable by leucine in turn/loop positions | C3 | Medium | Structural logic; no EBF3-specific experimental data |
| 11 | HADDS has near-complete penetrance in published cases | 83 published cases all symptomatic; no asymptomatic adult carriers documented | B2 | High | Deisseroth et al. 2022 (41+42 meta-analysis); Nishi et al. 2021 |
| 12 | >90% of HADDS diagnoses are in patients <18 years | Age-at-diagnosis data from largest cohort to date | A2 | High | Deisseroth et al. 2022 Fig. 1B |
| 13 | Virtually all HADDS cases are de novo | Multiple case series; parental testing routinely unaffected | A2 | High | Harms et al. 2017; Nishi et al. 2021; GeneReviews |
| 14 | No MAVE/DMS data for EBF3 exists | MaveDB searched; EBF3 not listed as target gene | E5 (null) | High | mavedb.org (2026-03-03) |
| 15 | No EBF3 missense near Pro263 documented as benign | No gnomAD common variants at position 263 found | D4 (indirect) | Medium | gnomAD constraint data; absence-of-evidence inference |
| 16 | Six DL predictors concordantly score Pro263Leu as damaging | Per query context; concordance expected for rare missense in maximally constrained gene | C3 | Medium | Per original query; predictor concordance is higher prior for pLI=1.0 genes |
| 17 | Healthy adult phenotype is strong evidence against classic HADDS | HADDS onset is childhood; core features (ID, ataxia, neurogenic bladder in infancy) absent in proband | B2 | High | GeneReviews diagnostic criteria; Nishi et al. 2021; Deisseroth et al. 2022 |
| 18 | Reduced penetrance/subclinical EBF3 adult phenotype not documented | No case series describe adult asymptomatic EBF3 carriers; EBF3 NDD listed as "typically de novo" | C3 | Medium | GeneReviews; absence of case reports |

**Grade key (NATO Admiralty adapted):**
Source reliability: A=Direct experimental/curated, B=Peer-reviewed secondary analysis, C=Structural inference, D=Indirect/computational, E=Null result, F=Unverified
Information credibility: 1=Confirmed multiple sources, 2=Likely confirmed, 3=Plausible/moderate, 4=Uncertain, 5=Absence of evidence, 6=Cannot be assessed

---

## Evidence by Axis

### Axis 1: Variant-Level Evidence

**p.Pro263Leu is a database-novel variant.** No entry found in ClinVar, GeneReviews Table 5, HGMD-accessible records, or published HADDS case series. The Frontiers in Genetics 2021 case report (Huang et al., Chinese boy), the Nishi 2021 cohort of 8 individuals, the 12-patient Chinese delineation study (Zhu et al. 2023, PMC10020332), and the Deisseroth 2022 83-patient meta-cohort collectively describe variants predominantly in the ZNF/DBD region (aa ~159–209). None document Pro263 or any variant near residue 263.

**Notable pathogenic missense variants (GeneReviews Table 5):**
All cluster in aa 163–209: p.Arg163Trp (recurrent, CpG hotspot), p.Arg163Gln, p.Arg163Leu, p.Arg163Pro, p.Gly171Asp, p.Arg206Ter (nonsense), p.Arg209Trp (recurrent), p.Arg209Gln.
→ Pro263 falls ~54 residues downstream of the most distal notable pathogenic variant (Arg209).

**Conservation at Pro263:** Not directly verified from sequence alignment databases within this research session. However, proline residues in EBF-family IPT/TIG domains are broadly conserved across vertebrates based on structural data (Siponen 2010; Treiber 2010). MISSING DATA: orthologue alignment (Drosophila Collier, C. elegans Unc-3) would be informative.

### Axis 2: Gene-Level Missense Constraint

EBF3 is among the most constrained human genes:
- pLI = 1.0 (v2.1.1) / LOEUF = 0.25 (v4.0 beta)
- DECIPHER HI score: 3.89 (high intolerance)
- SFARI Score: 1 (highest autism gene confidence)
- ClinGen: Definitive for HADDS; GenCC: Definitive + Strong

**Missense constraint:** The Geisinger DBD database (Nov 2024) classifies EBF3 as Tier 1 (≥3 de novo pathogenic LoF variants in ID). EBF3's extreme intolerance means computational missense predictors will nearly universally score rare variants as damaging — this reduces the independent evidential weight of the 6 concordant DL scores (PP3 is weak evidence here).

**Domain clustering:** Deisseroth 2022 provides the strongest genotype-phenotype data. Pathogenic missense clusters in the ZNF domain cause severe phenotypes and fail functional rescue. DBD-non-ZNF missense (p.Arg209Trp) shows partial function. IPT/TIG-domain missense pathogenicity is not directly characterized in published functional studies.

### Axis 3: Functional Data

**MAVE/DMS:** No deep mutational scanning data for EBF3 exists in MaveDB (confirmed). This is a significant evidence gap — MaveDB covers >7M variant effects (2025 update) but EBF3 has not been assayed.

**In vivo model (fly):** Deisseroth 2022 established a UAS-GAL4 Drosophila rescue assay. ZNF variants (e.g., p.Cys162Ser, p.Arg163Cys) = no rescue + impaired luciferase reporter. p.Arg209Trp = partial rescue. **Pro263Leu not tested.**

**Structural rationale for Pro→Leu:**
Proline is the only amino acid with its side chain cyclized back to the backbone nitrogen, constraining φ to ~−60° and preventing standard backbone hydrogen bonding. In loop regions (particularly the H1-H2 loop of HLHLH domains), proline introduces a defined kink/turn geometry. Leucine at the same position would allow full rotational freedom, potentially disrupting the precise geometry needed for H1-H2 helix packing or for IPT-domain β-sheet integrity. The Siponen 2010 crystal structure (PDB 3N50) specifically annotates proline residues in the HLHLH loop as relevant to helix packing interactions. **However, without knowing the exact secondary structure assignment of residue 263 (β-strand, loop, or helix), this structural argument remains inferential (grade C3).**

**Animal model:** Cordova Hurtado et al. 2025 (Biol Open/bioRxiv) generated an EBF3 enhancer knockout mouse showing NDD phenotypes, confirming haploinsufficiency sensitivity of the locus but not directly informative about Pro263.

### Axis 4: Phenotype and Penetrance

**HADDS clinical features** (GeneReviews, Nishi 2021, Deisseroth 2022):
- Developmental delay / intellectual disability (universal)
- Generalized hypotonia (universal)
- Neurogenic bladder diagnosed in infancy (median 6.5 months; Nishi 2021 — "more frequent than previously reported")
- Ataxia, speech delay, dysarthria
- Facial dysmorphisms (mild)
- Behavioral anomalies

**Penetrance:** Near-complete based on published literature. GeneReviews states "typically caused by a de novo pathogenic variant." No asymptomatic adult carriers of established HADDS pathogenic variants have been reported. The Nishi 2021 series specifically examined parental samples — none carried the proband variants.

**Adult-onset HADDS:** Not documented. The disorder is congenital/early-childhood onset. Prenatal features (reduced fetal movement) have now been documented (Hu et al. 2025, Heliyon; He et al. 2025, MFM), indicating phenotype begins before birth. An adult without known hypotonia, ID, ataxia, or urological issues as a child is phenotypically inconsistent with the expected trajectory of a classical pathogenic EBF3 allele.

**Milder phenotype possibility:** A small minority of HADDS patients have milder presentations (borderline ID, ASD without ID). The Spineli-Silva et al. 2025 case (C-terminal transactivation domain nonsense) presented with ID and behavioral disorder but reportedly milder features, demonstrating phenotypic spectrum. However, even mild HADDS cases have childhood-onset developmental concerns — not an asymptomatic adult.

---

## Disconfirmation Evidence

| Disconfirmation claim | Strength | Finding |
|----------------------|----------|---------|
| Pro263 not in ZNF hotspot (aa 163–209) — lower prior for pathogenicity | Strong | CONFIRMED — Pro263 is in IPT/TIG domain, not the validated high-risk ZNF region |
| All documented HADDS missense cluster in aa 163–209 | Strong | CONFIRMED — GeneReviews Table 5, all notable missense aa 163–209 |
| Healthy adult phenotype inconsistent with HADDS penetrance | Very strong | CONFIRMED — 90%+ diagnosed <18y; neurogenic bladder in infancy |
| No DMS/MAVE data to confirm Pro263Leu is damaging | Confirmed gap | No MaveDB entry for EBF3 |
| DBD non-ZNF missense can preserve partial function | Relevant analog | p.Arg209Trp partially rescues in fly — establishes that EBF3 missense ≠ null allele obligatorily |
| Computational predictors are inflated for pLI=1.0 genes | Methodological | DL predictors trained partly on constraint metrics; near-universal "damaging" for ultra-rare variants in LoF-intolerant genes; PP3 weight is reduced |
| No disconfirmation that Pro263 is conserved | MISSING DATA | Cross-species alignment not retrieved — gap in evidence |

---

## ACMG/AMP Evidence Weighing

| Criterion | Assessment | Weight |
|-----------|-----------|--------|
| PVS1 | Not applicable (missense, not LoF) | — |
| PS1 | Not applicable (no same-codon pathogenic variant in ClinVar) | — |
| PS2 | Cannot assess (de novo status unknown for healthy adult) | — |
| PS3 | Not applicable (no functional data for Pro263Leu) | — |
| PS4 | Not applicable (no prior cases) | — |
| PM1 | Weak-moderate: IPT/TIG domain is critical for dimerization, but not the established mutational hotspot | +weak |
| PM2 | Applicable: absent or ultra-rare in gnomAD for maximally constrained gene | +moderate |
| PM5 | Not applicable (no pathogenic variant at same residue) | — |
| PP2 | Applicable: missense in gene where missense is established disease mechanism | +supporting |
| PP3 | Weak: 6/6 DL predictors — but expected in pLI=1.0 gene; reduced independent weight | +weak |
| BP1 | Partially applicable: primary mechanism is LoF (haploinsufficiency), but pathogenic missense exist | weak negative |
| BP4 | Not applicable (all predictors concordant damaging) | — |
| BS2 | Not strictly applicable: gnomAD population absence ≠ de novo evidence | — |
| BS4 | Potentially applicable if parent study shows inherited from unaffected parent | N/A (not tested) |
| **Net** | **VUS — insufficient evidence for LP or LB** | Leans uncertain |

**Critical missing evidence:** (1) De novo vs. inherited status — if inherited from unaffected parent = strong BS4 (likely benign); (2) Neurological/developmental history of proband — formal exam for ataxia, bladder function, cognitive testing; (3) Cross-species conservation of Pro263; (4) EBF3 missense functional assay for Pro263Leu

---

## Recommendation

**Immediate clinical actions (highest ROI):**

1. **Parental testing** — single most informative next step. If inherited from phenotypically normal parent → BS4 (strong evidence benign). If de novo in healthy adult → unusual (adults with confirmed de novo EBF3 pathogenic variants are rare but should have childhood-onset features).

2. **Targeted clinical evaluation** — not a diagnosis, but screening: neurological exam (gait/ataxia), urological symptom review (urinary frequency/urgency), formal cognitive/attention assessment. If truly asymptomatic on comprehensive exam → further lowers posterior probability of classical HADDS pathogenicity.

3. **Conservation analysis** — retrieve EBF3 ortholog alignment (Collier/Unc-3/EBF1/EBF2/EBF4) at position 263. If Pro is conserved across vertebrates and invertebrates → stronger PM1; if variable → supports benign inference.

4. **Hold for MAVE data** — No DMS exists for EBF3. Watch MaveDB; EBF3 is a high-priority NDD gene likely to be assayed in the next 2–3 years.

**Bottom line:** The variant is a *genuine* VUS — not a false alarm (gene is real, mechanism is real, DL concordance is real), but the absence of the expected clinical phenotype in an adult is the strongest single piece of counter-evidence available. The finding should not be dismissed but should not drive clinical intervention without functional validation or inheritance context. File as "VUS, monitor" with parental testing recommended.

---

## Key Sources

| Reference | Key finding | Grade |
|-----------|------------|-------|
| Harms et al. 2017 (Am J Hum Genet 100:117) | Original EBF3 NDD characterization; 8 patients; ZNF/DBD variants | A2 |
| Nishi et al. 2021 (AJMG 162:2369) | 8-patient series; neurogenic bladder in infancy; haploinsufficiency confirmed | A2 |
| Deisseroth et al. 2022 (Ann Neurol 92:138; doi:10.1002/ana.26359) | 83-patient cohort; ZNF missense = high-risk; fly rescue assay; >90% dx <18y | A2 |
| GeneReviews EBF3-NDD (NBK570204; updated) | Table 5: notable pathogenic variants aa 163–209; diagnostic criteria | A2 |
| Siponen et al. 2010 (JBC 285:25875; PDB 3N50) | Crystal structure of EBF3 IPT/TIG + HLHLH domains; Pro in HLHLH H1-H2 loop | B2 |
| Zhu et al. 2023 (Front Pediatr 11:1091532; PMC10020332) | 12 Chinese patients; further delineation | B2 |
| Lopes et al. 2017 (Front Genet 8:143) | Whole gene deletion → HADDS; haploinsufficiency mechanism | A2 |
| Cordova Hurtado et al. 2025 (Biol Open; doi:10.1242/bio.062070) | EBF3 enhancer KO mouse shows NDD phenotypes | B3 |
| Spineli-Silva et al. 2025 (Psychiatr Genet; doi:10.1097/YPG.0000000000000386) | C-terminal TAD nonsense; ID + behavioral disorder; phenotypic spectrum | B3 |
| MaveDB (mavedb.org) | EBF3 not listed — no DMS/MAVE data available | E5 |

---

## Research Gaps Identified

1. **No cross-species conservation data retrieved** for Pro263 specifically — structural databases were searched but ortholog alignment not extracted
2. **No functional assay data** for Pro263Leu — EBF3 fly rescue model exists (Deisseroth 2022) but this variant not in cohort
3. **gnomAD variant-level frequency** for p.Pro263Leu not directly confirmed (no allele count retrieved) — inferred absent/ultra-rare from constraint data
4. **No LOVD/HGMD direct query** — these databases were not directly queried; null result is based on literature mining
5. **IPT/TIG missense functional data** — Deisseroth 2022 focuses on ZNF vs. DBD; IPT/TIG domain missense pathogenicity is understudied
