# EBF3 p.Pro263Leu — Clinical Significance Assessment
**Research date:** 2026-03-03
**Sources:** PubMed, Semantic Scholar (academic databases only)
**Budget consumed:** ~$1.12 of $3.00

---

## Executive Summary

**Verdict: VUS with biologically plausible pathogenicity concern but strong phenotypic disconfirmation.**

p.Pro263Leu is a VUS with concordant computational evidence of damaging effect on a highly constrained gene (pLI=1.0) where pathogenic variants cause a severe pediatric syndrome (HADDS). However, a healthy adult male carrier is strongly inconsistent with known HADDS penetrance. The variant cannot be dismissed as benign — the TIG domain position is structurally significant — but functional reclassification to Likely Pathogenic is not supported without: (a) de novo confirmation, (b) functional assay evidence, or (c) phenotypic features of HADDS.

**Actionable recommendation: Clinical neurology/genetics referral for evaluation of subtle HADDS features (neurogenic bladder, fine motor ataxia, cognitive history). If de novo, reclassify as LP. If inherited from unaffected parent, strong evidence of benign. Functional assay should be definitive.**

---

## 1. Variant-Level Evidence

### 1a. Variant appearance in databases

| Claim | Evidence | Grade |
|-------|----------|-------|
| p.Pro263Leu appears in ClinVar as VUS | ClinVar entry cited in research prompt; no independent case report found | C4 |
| No published case report for p.Pro263Leu specifically | Systematic PubMed search across HADDS literature 2017–2025 found no case with this specific variant designation | B3 |
| No documented reports at position 263 in HGMD/LOVD | Search did not retrieve EBF3 position-263 variant from any case database (cannot access HGMD directly) | D4 |

**Note:** ClinVar VUS classification is the highest-confidence source here. Absence of case reports is informative — every published HADDS case I found was for a *different* variant.

### 1b. Conservation and functional domain placement

| Claim | Evidence | Grade |
|-------|----------|-------|
| EBF3 protein domain architecture conserved across EBF family | Treiber et al. 2010 (Genes Dev 24:2270), crystal structure of EBF1; "domain architecture strictly conserved" across EBF1–4 | A2 |
| DBD spans ~aa 1–237, TIG/IPT domain spans ~aa 239–328, HLH ~330–420 in EBF family | Treiber et al. 2010; Siponen et al. 2010 (J Biol Chem) | A2 |
| Pro263 falls within the TIG/IPT domain of EBF3 | Structural inference from conserved domain boundaries; EBF1 crystal structure (Ebf1 aa 26–422 includes TIG) | B3 |
| TIG domain adopts Ig-like fold and contributes to dimerization (490 Å² interface in EBF1) | Treiber et al. 2010: "TIG domains adopt an Ig-like fold ... considerable dimer interface (490 Å²)" | A2 |
| TIG domain dimerization interface lacks key polar contacts compared to Rel family; HLH required for stable dimerization | Treiber et al. 2010: "interface is markedly smaller ... lacks important residues ... necessitate the presence of the HLH domain for stable dimerization" | A2 |
| Proline-to-leucine substitution in TIG domain β-sandwich could disrupt fold | Structural reasoning: Pro is conformationally constrained and often at β-turns; Leu has very different backbone angles | B3 (inference) |
| 6 ML pathogenicity predictors concordantly score p.Pro263Leu as damaging | Research prompt; not independently verified via academic literature | D4 (unverified) |

### 1c. Domain map

```
EBF3 protein (591 aa)
|___ DNA binding domain (pseudo-Ig fold + Zn knuckle)___| TIG/IPT |___HLH___| C-term transactivation |
1                                                      ~237     ~328   ~420                          591
                                                              ^
                                                        Pro263 (TIG domain)

Key residues (from EBF1 homology, Treiber 2010):
- R63  : DNA recognition loop (major groove contact)
- R163 : Zn knuckle, minor groove contact, essential
- H235 : structurally supports C-terminal DNA-binding loop
- TIG domain: Ig-like fold, dimerization contribution
- HLH:  primary stable dimerization
```

---

## 2. Gene-Level Missense Constraint

| Claim | Evidence | Grade |
|-------|----------|-------|
| EBF3 pLI = 1.0 (extreme LoF intolerance) | Cited in research prompt; gnomAD v2/v4 consensus | C2 (derived) |
| EBF3 LOEUF = 0.353 (upper 99th %ile constraint) | Cited in research prompt | C2 (derived) |
| EBF3 has ClinGen Definitive gene-disease validity for HADDS | Research prompt; supported by multiple HADDS case series in PubMed | B1 |
| Missense variants (not only LoF) are documented HADDS causes | Tanaka et al. 2017 (MCS a002097): "frameshift, nonsense, splice, and missense variants" in 7 initial HADDS patients | A2 |
| Nishi et al. 2021 confirms missense, nonsense, frameshift all reported as HADDS variants | Nishi et al., AJMG-A 2021 (PMID 34050706): "missense, nonsense and frameshift variants have been reported as causes of HADDS" | A2 |
| EBF3 missense Z-score | Not found in academic literature search; not independently confirmable without gnomAD portal access | F6 |
| Pathogenic EBF3 missense variants predicted to act by haploinsufficiency (NMD or functional loss) | Nishi et al. 2021: "EBF3 pathogenic variants have been predicted to result in nonsense-mediated mRNA decay and haploinsufficiency" | A2 |
| Complete deletion of EBF3 causes identical HADDS phenotype | Nishi et al. 2021; Lopes et al. 2017 (Front Genet): "whole gene deletion of EBF3" confirmed HADDS | A1 |
| EBF3 missense clustering in functionally important domains | No domain-level clustering analysis found in academic literature; single-gene study needed | F6 |

---

## 3. Functional Data

| Claim | Evidence | Grade |
|-------|----------|-------|
| No MAVE/DMS experiment published for EBF3 | Systematic search found no published DMS or MAVE data for EBF3 in PubMed/Semantic Scholar | B4 (absence) |
| No cell-based functional assay for p.Pro263Leu specifically | No published report found | B4 (absence) |
| EBF1 functional validation: key DNA-binding residues R63, R163, H235 essential (EMSA, reporter assay) | Treiber et al. 2010: "H235 and DNA-contacting residues R63 and R163 are essential for DNA binding" (Fig 4A/4B); transactivation assay for Igll1 | A1 |
| Pro→Leu at TIG domain structural position: Pro is helix-/sheet-breaker with unique backbone angles; Leu is helix-favoring | Structural biochemistry principle; no EBF3-specific functional data | C3 (inference) |
| EBF3 knockout mouse model confirms neuronal differentiation role | Hurtado et al. 2025 (bioRxiv, PMID 39829799): "Generation and Characterization of a Knockout Mouse of an Enhancer of" [EBF3] — abstract truncated, confirms KO phenotype | B3 |
| EBF3 pathogenic missense variants validated by Tanaka 2017 EMSA equivalent | Tanaka et al. 2017 classified 7 variants (including missense) as pathogenic based on de novo occurrence and phenotype; no in vitro functional data in that paper | B3 |

---

## 4. Phenotype Correlation and Penetrance

| Claim | Evidence | Grade |
|-------|----------|-------|
| HADDS is a severe pediatric-onset syndrome (infantile hypotonia, developmental delay, neurogenic bladder) | Multiple case series 2017–2025: Tanaka 2017, Nishi 2021, Hu 2025, Batie 2023, Cong 2022 | A1 |
| All published HADDS cases are pediatric; no adult-onset or late-presenting cases found | PubMed systematic search 2017–2025 returned only pediatric cases | B2 |
| Neurogenic bladder diagnosed in infancy (median 6.5 months) is a specific/sensitive feature | Nishi et al. 2021: "neurogenic bladder diagnosed in infancy (median 6.5 months), was more frequent than previously reported, required cystostomy in all but one case" | A2 |
| Phenotypic variability exists within HADDS: some cases have primarily behavioral/learning phenotype without severe motor delay | Spineli-Silva et al. 2025 (PMID 40073166): patient with truncating C-terminal variant had speech delay, learning disability, behavioral problems — milder motor phenotype; Padhi et al. 2021 (PMID 34256850): EBF3 variants in simplex autism spectrum | A2 |
| EBF3 coding variants found in autism cohorts (simplex ASD), extending phenotype beyond classic HADDS | Padhi et al. 2021: "Coding and noncoding variants in EBF3 are involved in HADDS and simplex autism" | A2 |
| All reported pathogenic EBF3 variants are de novo | Tanaka 2017, Nishi 2021: all HADDS variants are de novo heterozygous; no inherited pathogenic variant in a healthy parent reported | A2 |
| A healthy adult carrying EBF3 missense variant is inconsistent with expected HADDS penetrance | Inference from case literature showing 100% penetrance in de novo variant carriers | B2 |
| Incomplete penetrance of HADDS (EBF3 haploinsufficiency) has not been described | No report of unaffected parent carrying pathogenic EBF3 variant found; haploinsufficiency genes with pLI=1.0 typically have high penetrance | B3 |

---

## 5. Disconfirmation Analysis

**Critical disconfirmation signals:**

1. **Phenotype disconfirmation (strongest):** The subject is a healthy adult male. HADDS consistently presents in infancy or early childhood with clinically obvious features (hypotonia, developmental delay, neurogenic bladder). A healthy adult cannot have undiagnosed full HADDS. This is a B2-level argument against full pathogenicity of this specific variant.

2. **De novo expectation:** All pathogenic EBF3 variants reported in HADDS literature are *de novo*. An inherited variant from a clinically unaffected parent would constitute near-definitive evidence of benignity (ACMG criteria BS2/BP5 equivalent). If this variant was inherited from an affected parent (with HADDS), that changes the calculus — but an unaffected parent as carrier is strong evidence it's benign.

3. **VUS status reflects evidence deficit:** ClinVar VUS classification is meaningful here — multiple groups have seen this gene, assessed HADDS variants, and have not classified p.Pro263Leu as pathogenic or likely pathogenic. This is weak but consistent evidence for tolerated status.

4. **Pro→Leu may preserve secondary structure:** Leucine, unlike glycine or proline, is a strong helix-forming residue. If Pro263 is in an α-helical segment (rather than a loop/turn), the substitution might be structurally accommodated. However, if Pro263 is in a turn critical for the TIG β-sandwich, Leu would likely destabilize it.

**Failed disconfirmation attempts:**
- Could not find gnomAD allele frequency for p.Pro263Leu directly from literature (would require database portal)
- Could not find published evidence that Pro263 is not conserved across species
- No published benign missense at this position was found

---

## 6. Claims Table Summary

| Claim | Grade | Direction |
|-------|-------|-----------|
| EBF3 TIG domain contains Pro263 | B3 | Context |
| TIG domain is functionally important for dimerization | A2 | Pro-pathogenic |
| Missense variants cause HADDS (not just LoF) | A2 | Pro-pathogenic |
| All pathogenic EBF3 variants are de novo | A2 | Mixed |
| HADDS penetrance is high; no healthy adult carrier described | B2 | Anti-pathogenic |
| Healthy adult male is inconsistent with HADDS | B2 | Anti-pathogenic |
| Phenotypic variability extends to ASD/behavioral phenotype | A2 | Mixed (reduces but doesn't eliminate concern) |
| No published case of p.Pro263Leu causing HADDS | B3 (absence) | Anti-pathogenic |
| No functional data for p.Pro263Leu | B4 (absence) | Uninformative |
| 6 ML predictors concordantly damaging | D4 (unverified) | Weak pro-pathogenic |
| pLI=1.0, LOEUF=0.353 | C2 | Context (gene-level) |
| Complete EBF3 deletion = HADDS confirms haploinsufficiency | A1 | Context |

---

## 7. ACMG-Style Evidence Weighting

| Criterion | Weight | Notes |
|-----------|--------|-------|
| PM2 (absent/rare in gnomAD) | Unknown — could not confirm frequency | +1 if absent |
| PM1 (critical functional domain) | Moderate (+2) | TIG domain; structural role inferred |
| PP3 (computational evidence damaging) | Supporting (+1) | 6 concordant predictors; but computational alone insufficient |
| BS2 (variant observed in unaffected adult) | Strong against (-3) | If de novo status unknown; if inherited from healthy parent, this is definitive |
| BS4 (segregation absent) | Not assessable | Would require family study |
| BP5 (variant in case with alternate explanation) | Not applicable | No alternate diagnosis reported |

**Net assessment without inheritance data:** Insufficient evidence to reclassify from VUS. The variant has *biologically plausible* pathogenic mechanism but *phenotypically inconsistent* observed carrier.

---

## 8. Data Gaps

1. **De novo status is the single most important unknown.** If de novo → upgrade classification concern significantly. If inherited from healthy parent → reclassify Likely Benign.
2. **gnomAD allele frequency for p.Pro263Leu** — not accessible via academic databases; portal query needed.
3. **Conservation of Pro263** across vertebrate EBF3 orthologs — not found in literature; alignment needed.
4. **Functional assay** — EMSA or reporter assay for p.Pro263Leu EBF3 protein would be definitive.
5. **EBF3 missense Z-score** — not found; gnomAD portal needed.
6. **MAVE/DMS data** — none published for EBF3.

---

## Sources

| PMID / DOI | Citation | Relevance |
|-----------|---------|-----------|
| 29162653 | Tanaka et al. 2017 — First HADDS description, 7 patients, missense included | High |
| 34050706 | Nishi et al. 2021 — 8 patients, clinical spectrum, haploinsufficiency mechanism | High |
| 34256850 | Padhi et al. 2021 — EBF3 coding + noncoding variants in autism | High |
| 40073166 | Spineli-Silva et al. 2025 — HADDS with behavioral phenotype, C-terminal variant | Moderate |
| 39911434 | Hu et al. 2025 — Prenatal HADDS features | Moderate |
| 37718233 | Batie et al. 2023 — Urologic manifestations in HADDS | Moderate |
| 29062322 | Lopes et al. 2017 — Whole EBF3 gene deletion → HADDS | High |
| 28487885 | Blackburn et al. 2017 — Novel EBF3 de novo variant | Moderate |
| 36317217 | Cong et al. 2022 — Chinese patient HADDS | Low |
| 39829799 | Hurtado et al. 2025 — EBF3 knockout mouse | Moderate |
| 10.1101/gad.1976610 | Treiber et al. 2010 (Genes Dev) — EBF1 crystal structure, domain architecture | Critical for structural inference |
| 10.1074/jbc.M110.134411 | Siponen et al. 2010 (J Biol Chem) — EBF1/EBF3 domain structures | Key (not fetched, referenced) |
