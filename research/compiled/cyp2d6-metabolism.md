---
type: compiled
concept: CYP2D6 Metabolism and Pharmacogenomics
compiled: 2026-04-03
sources: 7
projects: [selve, genomics]
---

## Summary

CYP2D6 *1/*4 Intermediate Metabolizer (Activity Score 1.0) — one functional allele, ~50-75% of normal metabolic capacity. Metabolizes ~25% of clinically used drugs. Most drugs need no dose adjustment for IM alone, but the compound metabolizer phenotype (CYP2D6 IM + CYP3A4/5 PM) and phenoconversion risk (strong CYP2D6 inhibitors convert IM to effective PM with 94% probability) create the real clinical significance. No multi-gene CPIC guidelines exist; DPWG 2023 published the first multi-gene PGx guideline for antipsychotics.

## Key Claims

| # | Claim | Source | Project | Date | Grade |
|---|-------|--------|---------|------|-------|
| 1 | Personal diplotype *1/*4, IM, AS 1.0. Source: PharmCAT + Cyrius | cyp2d6.md entity | selve | 2026-03 | [A1: PharmCAT/Cyrius] |
| 2 | *4 allele frequency ~20-25% in Europeans (most common non-functional allele) | pgx_deep_dive_2026.md | selve | 2026-02 | [A1: CPIC, PMID 31453527] |
| 3 | IM = ~50-75% of normal metabolic capacity; IM is NOT PM | pgx_deep_dive_2026.md | selve | 2026-02 | [A1: CPIC] |
| 4 | Most drugs need no dose adjustment for IM — standard dosing adequate for most encounters | cyp2d6.md entity | selve | 2026-03 | [CALC: from CPIC guidelines] |
| 5 | Tamoxifen is most impactful IM drug — prefer aromatase inhibitor per CPIC | cyp2d6.md entity | selve | 2026-03 | [A1: CPIC 2018, PMID 29385237] |
| 6 | Metoprolol: ~2x AUC in IM, enhanced beta-blockade; bisoprolol is alternative | cyp2d6.md entity | selve | 2026-03 | [A1: CPIC 2024, DOI 10.1002/cpt.3351] |
| 7 | CYP2D6 IM + CYP3A4 *1/*22 + CYP3A5 *3/*3 = compound metabolizer phenotype | combinatorial_pgx_memo.md | genomics | 2026-03 | [A1: Kitzmiller 2014, PMID 25051018] |
| 8 | Paroxetine phenoconverts 94% of gAS1 subjects to PM (RCT, n=34) | combinatorial_pgx_memo.md | genomics | 2026-03 | [A1: Storelli 2018, PMID 28940476] |
| 9 | DPWG 2023 = first multi-gene PGx guideline (CYP2D6+CYP3A4+CYP1A2, antipsychotics) | combinatorial_pgx_memo.md | genomics | 2026-03 | [A1: Beunk 2023, PMID 37002327] |
| 10 | No CPIC guideline addresses >2 gene interactions simultaneously | combinatorial_pgx_memo.md | genomics | 2026-03 | [A2: guideline review] |
| 11 | NAT2 + CYP2D6: no drugs with documented dual-pathway interaction | combinatorial_pgx_memo.md | genomics | 2026-03 | [A2: negative lit search] |
| 12 | Clomiphene/enclomiphene partially CYP2D6-metabolized; start 25mg EOD for IM | enclomiphene_testosterone.md | selve | 2026-03 | [B2: clinical note] |
| 13 | PBPK kcat_rel for AS 1.0 estimated ~0.50 (extrapolated from AS 1.5 model) | cyp2d6.md entity | selve | 2026-03 | [CALC: GPT-5.4 Pro T6, extrapolation] |
| 14 | "CYP2D6 IMs have 40% less codeine analgesia than NMs" — INCONCLUSIVE | gpt54pro_validated_claims.md | selve | 2026-03 | [INCONCLUSIVE: 3 exposures, 4 IMs] |
| 15 | Phenoconversion to PM + CYP3A PM = critical risk for oxycodone, methadone (respiratory depression, QTc) | combinatorial_pgx_memo.md | genomics | 2026-03 | [CALC: from CPIC + Storelli] |
| 16 | DPWG TCA recommendations more conservative than CPIC (amitriptyline: 75% vs 75% standard; nortriptyline: 60% vs 75%) | pgx_deep_dive_2026.md | selve | 2026-02 | [A1: DPWG 2026, DOI 10.1038/s41431-025-02008-3] |

## Contradictions and Open Questions

**1. Metoprolol dose adjustment: entity vs deep dive**
- Entity page (selve, 2026-03): "Start low, titrate carefully; consider bisoprolol"
- PGx deep dive (selve, 2026-02): "No specific dose adjustment for IM (CPIC 2024: recommendations focus on PM; IM: 'plasma concentrations increased... titrate carefully')"
- **Resolution:** These don't actually contradict — CPIC 2024 doesn't give a specific % reduction for IM but does note increased plasma concentrations. The entity page's "start low, titrate" is a reasonable clinical interpretation. The deep dive is more literal about CPIC's wording.

**2. Codeine analgesia reduction: claim vs evidence**
- Validated claims memo (selve, 2026-03): 40% reduction claim classified INCONCLUSIVE — only 3 codeine exposures across 4 IMs, sample too small for reliable quantitation.
- CPIC guideline: "Use label-recommended dose; if inadequate response, use alternative"
- **Open question:** The magnitude of analgesia reduction in IM (not PM) is poorly quantified. Personal experience data would resolve this.

**3. PBPK parameters: AS 1.5 vs AS 1.0**
- Entity page PBPK section models kcat_rel for AS 1.5 (*1/*41) = 0.68, then extrapolates AS 1.0 (*1/*4) "would shift kcat_rel lower (~0.50)"
- **Open question:** This is an extrapolation from a different genotype's model, not a direct measurement or simulation. No direct PBPK modeling for *1/*4 has been done in the pipeline.

**4. Compound metabolizer phenotype: quantification gap**
- Combinatorial memo (genomics) identifies CYP2D6 IM + CYP3A PM as highest-risk combination
- Entity page (selve) notes this creates a compound phenotype
- **Open question:** No quantitative model exists for combined pathway impairment. The combinatorial memo estimates effective CYP3A capacity at ~40-50% but marks this as [INFERENCE]. The interaction between two reduced pathways is likely super-additive, not additive, for dual-pathway drugs.

## Timeline

| Date | Source | Development |
|------|--------|-------------|
| 2026-02-19 | pgx_deep_dive (selve) | 51-reference literature review establishing drug tables |
| 2026-03-01 | combinatorial_pgx_memo (genomics) | Combinatorial effects analysis; phenoconversion risk quantified |
| 2026-03-16 | cyp2d6.md entity (selve) | Entity page created, derived from deep dive + PharmCAT |
| 2026-03-29 | cyp2d6.md entity (selve) | PBPK parameter priors added (GPT-5.4 Pro T6 session) |
| 2026-03-31 | validated_claims (selve) | Codeine analgesia claim tested — classified INCONCLUSIVE |

## Cross-References

**selve:**
- `docs/entities/genes/cyp2d6.md` — entity page (primary reference)
- `docs/research/pgx_deep_dive_2026.md` — comprehensive literature review
- `docs/research/enclomiphene_testosterone.md` — enclomiphene CYP2D6 interaction
- `docs/research/gpt54pro_validated_claims_genotype_kernel_2026-03-31.md` — codeine analgesia claim validation
- `docs/reports/PHARMCAT_DRUG_INTERACTIONS.md` — PharmCAT output
- `docs/research/psychedelic_systemic_mechanisms_2026_03.md` — CYP2D6 IM and psychedelic metabolism

**genomics:**
- `docs/research/combinatorial_pgx_memo.md` — combinatorial effects, phenoconversion
- `docs/research/brainstorm_anesthesia_card.md` — opioid sensitivity (stubs only)
- `docs/audit/biomedical-fact-check-2026-03-24/pgx-card-verification.md` — CYP2D6 drug claim verification

## Gaps

1. **No direct PBPK simulation for *1/*4.** The kcat_rel is extrapolated from *1/*41 (AS 1.5). A PK-Sim run with the actual *1/*4 diplotype would ground the pharmacokinetic predictions.

2. **Phenoconversion monitoring protocol absent.** Storelli 2018 shows 94% phenoconversion with paroxetine. No structured check exists in the pipeline to flag when a CYP2D6 inhibitor is prescribed alongside the IM genotype.

3. **Anesthesia card incomplete.** `brainstorm_anesthesia_card.md` has CYP2D6/opioid section as stubs ([SEARCHING...]). Opioid sensitivity pre-surgical recommendations not written.

4. **Cyrius/Aldy read-backed calling status unclear.** Multiple memos mention this is needed/was done, but the pipeline status (whether PharmCAT is running with outside calls) isn't confirmed in any current source.

5. **No personal codeine/tramadol exposure data.** The codeine analgesia claim is INCONCLUSIVE due to sample size. Personal exposure would resolve this for the individual's specific phenotype.

6. **Combinatorial model is qualitative only.** The dual-pathway risk (CYP2D6 IM + CYP3A PM) is described narratively but not quantified via PBPK or population PK models. The interaction may be super-additive.

<!-- knowledge-index
generated: 2026-04-03T19:11:25Z
hash: 1230ee4aa24c

cross_refs: docs/audit/biomedical-fact-check-2026-03-24/pgx-card-verification.md, docs/entities/genes/cyp2d6.md, docs/reports/PHARMCAT_DRUG_INTERACTIONS.md, docs/research/brainstorm_anesthesia_card.md, docs/research/combinatorial_pgx_memo.md, docs/research/enclomiphene_testosterone.md, docs/research/gpt54pro_validated_claims_genotype_kernel_2026-03-31.md, docs/research/pgx_deep_dive_2026.md, docs/research/psychedelic_systemic_mechanisms_2026_03.md
sources: 15
  A1: PharmCAT/Cyrius
  A1: CPIC, PMID 31453527
  A1: CPIC
  CALC: from CPIC guidelines
  A1: CPIC 2018, PMID 29385237
  A1: CPIC 2024, DOI 10.1002/cpt.3351
  A1: Kitzmiller 2014, PMID 25051018
  A1: Storelli 2018, PMID 28940476
  A1: Beunk 2023, PMID 37002327
  A2: guideline review
table_claims: 16

end-knowledge-index -->
