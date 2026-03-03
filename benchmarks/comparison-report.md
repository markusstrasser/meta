# EBF3 p.Pro263Leu Research API Benchmark — Comparison Report

**Date:** 2026-03-03
**Variants assessed:** 3 strategies (academic, websearch, combined)
**Scoring rubric:** Factual accuracy 30%, Coverage 25%, Source quality 20%, Null results 15%, Actionability 10%
**PMID verification method:** Semantic Scholar search (independent of strategy outputs)

---

## 1. Per-Strategy Scores

| Strategy | Factual accuracy (30%) | Coverage (25%) | Source quality (20%) | Null results (15%) | Actionability (10%) | **Total** |
|----------|----------------------|---------------|---------------------|-------------------|-------------------|-----------|
| Academic | 84 → **25.2** | 72 → **18.0** | 80 → **16.0** | 86 → **12.9** | 80 → **8.0** | **80/100** |
| Websearch | 62 → **18.6** | 84 → **21.0** | 73 → **14.6** | 83 → **12.5** | 87 → **8.7** | **75/100** |
| Combined | 70 → **21.0** | 92 → **23.0** | 83 → **16.6** | 90 → **13.5** | 90 → **9.0** | **83/100** |

### Detailed component rationale

**Factual accuracy:**
- Academic (84): All major PMIDs verified. Domain boundaries inferred from EBF1 homology (Treiber 2010, EBF1 crystal) rather than EBF3-specific UniProt — less precise but not wrong. Claims graded transparently. No hallucinated citations.
- Websearch (62): Two year errors (Chao/Sleven published 2017, cited as 2016). PDB 3MUJ is not the Treiber 2010 structure (which is 3MQN); 3MUJ is a different crystal form or protein — likely hallucinated. Interface area cited as 1,960 Å² (Siponen 2010 PMC2923972) vs academic's 490 Å² (Treiber 2010) — these may measure different interfaces (combined HLH+TIG vs TIG-alone), but the websearch presents the number without this context, making direct comparison misleading. Self-contradiction: claims "no pathogenic variant in IPT/TIG domain" then notes Gly338Val may be within IPT/TIG (residues 263–346).
- Combined (70): Deisseroth 2022 (PMID 35340043 ✓), Nishi 2021 (✓), Padhi 2021 (✓), Lopes 2017 (✓) all real. **Critical error:** cites "Harms et al. 2017 (Am J Hum Genet 100:117)" — the Harms FL et al. 2017 paper is real but published in *Human Mutation* (PMID 28736989), not AJHG. AJHG 100:117 is Chao et al. 2017. Journal and page are both wrong. LOEUF = 0.25 (gnomAD v4) vs ground truth 0.353 (gnomAD v2) — version difference, not a hallucination.

**Coverage:**
- Academic (72): Addressed all 4 axes. **Missed the domain clustering argument** — failed to note that documented pathogenic EBF3 missense clusters in the ZNF/DBD, not IPT/TIG, which is the strongest single analytical finding against pathogenicity. Structural analysis focused on EBF1 homology rather than EBF3-specific data.
- Websearch (84): Strong on domain clustering (key disconfirmation). UniProt domain boundaries directly queried. Cited unique finding: mosaic carrier mother (22–33% mosaicism, clinically unaffected) from openaccess.sgul.ac.uk — not found in other strategies. Addressed all 4 axes. Weaker on phenotype axis detail (missed Deisseroth 2022 age-at-diagnosis distribution).
- Combined (92): Most comprehensive. Uniquely described Deisseroth 2022 fly rescue assay (partial rescue for Arg209Trp, no rescue for ZNF variants). Cited age-at-diagnosis data (>90% diagnosed <18y, Deisseroth 2022 Fig. 1B). DECIPHER HI score 3.89 and SFARI Score 1 added. Zhu et al. 2023 (12 Chinese patients, PMC10020332) not in other strategies. Explicitly flagged PP3 inflation in pLI=1.0 genes — methodologically important.

**Source quality:**
- Academic (80): Treiber 2010 EBF1 crystal for structural inference — peer-reviewed but EBF1, not EBF3; correctly flagged as B3 inference. Consistent evidence grading throughout.
- Websearch (73): UniProt and MaveDB are strong authoritative sources. PDB error weakens structural claims. Year errors on Sleven/Chao reduce confidence. Functional data section leans on Padhi 2021 — correct paper, real source.
- Combined (83): Siponen 2010 (PDB 3N50, EBF3-specific structure) is the right crystal structure — better choice than academic's EBF1 inference. Deisseroth 2022 as primary evidence backbone is appropriate. Harms citation error is an isolated problem in an otherwise well-sourced output.

**Null results:**
- Academic (86): Explicitly documented: no MAVE/DMS for EBF3, no case report for p.Pro263Leu, no gnomAD portal access (acknowledged limitation), no published benign variant at position 263, no EBF3 missense Z-score found. Well-executed.
- Websearch (83): MaveDB absence confirmed with quantification ("74 datasets across 32 disease genes; EBF3 not among them") — most specific formulation. No SGE data noted. Missense Z-score not retrieved — acknowledged.
- Combined (90): Best null result documentation. 5 research gaps explicitly enumerated. Cross-species conservation specifically flagged as absent. IPT/TIG missense functional data gap named as "understudied." MaveDB confirmed with forward-looking note ("likely to be assayed in next 2–3 years").

**Actionability:**
- Academic (80): Recommends clinical referral for HADDS feature evaluation. Lists 6 data gaps. Clear but doesn't prioritize — leaves clinician to determine which gap to close first.
- Websearch (87): Priority steps explicitly numbered. Working hypothesis stated: "more likely a tolerated variant of uncertain effect." Not hedged to uselessness.
- Combined (90): Parental testing named as "single most informative next step" — correct prioritization (de novo vs. inherited is the cheapest highest-yield test). Bottom line explicit. "File as VUS, monitor" is actionable disposition.

---

## 2. Unique Findings Per Strategy

### Academic only
- **Batie et al. 2023 (PMID 37718233)** — urologic manifestations in HADDS, including cystostomy rates. Strengthens penetrance argument via urological specifics.
- **Blackburn et al. 2017 (PMID 28487885)** — additional single-case EBF3 variant report. Not clinically decisive but part of systematic coverage.
- **EBF1 dimerization interface quantified at 490 Å²** (Treiber 2010) — number not in other outputs. Context: this is TIG-domain-specific interface.
- Correctly identified that ACMG criterion PM1 likely **not met** at IPT/TIG (domain is functional but not the established hotspot) — implicit, but cleaner acknowledgment than other outputs.

### Websearch only
- **UniProt Q9H4W6 domain boundary directly queried:** IPT/TIG = residues 263–346 (EBF3-specific annotation). Other strategies infer from EBF1 homology or use approximate boundaries. If accurate, Pro263 is the **exact N-terminal residue** of IPT/TIG — a structural hinge, not a buried core position. This changes the structural argument (hinge Pro→Leu may disrupt interdomain orientation rather than domain fold itself).
- **Domain clustering disconfirmation (strongest analytical finding):** All documented pathogenic EBF3 missense variants cluster in DBD (residues 1–262), not in IPT/TIG. Listed pathogenic variants: K64T, R63Q, R152C, R163L/G/P, K193N, F211L, R209Q — all DBD. No pathogenic missense precedent at any IPT/TIG residue (263–346). This makes Pro263Leu an outlier by domain location — significantly lowers PM1 and weakens pathogenicity prior. *(Caveat: Gly338Val may be within IPT/TIG per UniProt boundaries; websearch flags but doesn't resolve this.)*
- **Mosaic carrier mother** (22–33% mosaicism, unaffected) — cited from openaccess.sgul.ac.uk/114054. Demonstrates mosaicism can reduce expressivity. Not directly relevant to Pro263Leu (which appears germline), but adds nuance to penetrance discussion.
- **ACMG BP5 applied** — variant in gene/domain pattern inconsistent with published disease mechanism. Other strategies don't apply this criterion.

### Combined only
- **Deisseroth 2022 fly rescue assay** — UAS-GAL4 Drosophila rescue experiment; ZNF variants (Cys162Ser, Arg163Cys) = no rescue + impaired luciferase reporter; Arg209Trp = partial rescue. Establishes functional spectrum: EBF3 missense ≠ null allele obligatorily. Pro263Leu untested. This is the strongest functional evidence in any output and uniquely cited by combined.
- **Age-at-diagnosis quantified:** >90% HADDS diagnoses in patients <18 years (Deisseroth 2022 Fig. 1B). Other strategies state childhood onset without the specific percentage.
- **PP3 inflation explicitly flagged:** "DL predictors trained partly on constraint metrics; near-universal 'damaging' for ultra-rare variants in LoF-intolerant genes; PP3 weight is reduced." Important methodological caveat absent from other outputs.
- **Zhu et al. 2023 (Front Pediatr, PMC10020332)** — 12 Chinese patients, additional delineation.
- **SFARI Score 1, DECIPHER HI 3.89, GenCC Definitive+Strong** — richer constraint evidence than other outputs.

---

## 3. Hallucinations and Factual Errors

### Academic
- **Domain boundaries from EBF1 homology (Treiber 2010, EBF1 crystal)** applied to EBF3 without flagging species/paralog gap. DBD boundary ~237 and TIG ~239–328 may differ from EBF3-specific UniProt annotation (263–346). Not a hallucination — a methodological limitation that is implicit but not disclosed. The Siponen 2010 EBF3 crystal (PDB 3N50) existed and would have been the correct source.
- **"6 ML predictors concordantly score p.Pro263Leu as damaging" graded D4 (unverified).** Correctly flagged as unverified in the academic output — no error here, appropriate grade.
- No verified PMIDs were found to be incorrect.

### Websearch
- **"Chao 2016 (PMID 28017372)"** — Year error. Chao et al. is conventionally cited as 2017 (AJHG 100:117–127). Published online Nov 2016 but the volume is 2017.
- **"Sleven 2016 (PMC5223060)"** — Year error. Sleven et al. is 2017 (PMID 28017370, AJHG 100:128–135). Same online-2016/print-2017 issue.
- **"PDB: 3MUJ"** — cited as supporting domain boundaries from "structural crystallography." PDB 3MUJ is not the Treiber 2010 EBF1 structure (which is PDB 3MQN) or the Siponen 2010 EBF3 structure (PDB 3N50). 3MUJ is an unrelated entry. Hallucinated PDB ID.
- **"1,960 Å² buried interface"** attributed to PMC2923972 — this is the total dimer interface (HLH+TIG combined per Siponen 2010), not the TIG-alone interface. Academic's 490 Å² (Treiber 2010) is TIG-specific. Websearch presents 1,960 Å² as if it measures the same thing as academic's 490 Å², making the two numbers appear contradictory when they likely aren't. Selective context omission rather than pure hallucination.
- **Self-contradictory claim on IPT/TIG pathogenic variants:** States "No pathogenic variant documented within the IPT/TIG domain proper (residues 263–346)" but then lists Gly338Val (position 338 = within 263–346) as potentially pathogenic and gnomAD-absent. The claim and the evidence in the same output are inconsistent. Flagged with B3 uncertainty but not resolved.

### Combined
- **"Harms et al. 2017 (Am J Hum Genet 100:117)"** — **Confirmed hallucinated citation.** Harms FL et al. 2017 is a real paper ("De novo variants in EBF3 cause early infantile spasms, severe intellectual disability, and functional deficits in Drosophila") but published in *Human Mutation* (PMID 28736989), not AJHG. AJHG 100:117 is Chao et al. 2017. The combined output merged Harms (real author, wrong journal) with Chao's AJHG page coordinates. Claims attributed to "Harms et al." in the output (de novo, HADDS characterization) may be accurate in substance — the Harms paper is real — but the citation format points to the wrong journal and wrong pages.
- **Domain boundary: IPT/TIG ~240–305.** The N-terminal boundary (~240) is inconsistent with UniProt Q9H4W6 (263) and plausibly inconsistent with Siponen 2010 (PDB 3N50). The C-terminal boundary (~305) differs from UniProt's 346 by 41 residues. If the UniProt annotation is authoritative, the combined output places Pro263 inside IPT/TIG but at the wrong position relative to the domain boundary.
- **LOEUF = 0.25** vs. ground truth 0.353. Uses gnomAD v4 beta rather than v2.1.1. Not a hallucination — both values are defensible depending on version. Combined correctly notes v4.0 beta sourcing.

---

## 4. Cross-Strategy Disagreements — Ground Truth Assessment

| Disagreement | Academic | Websearch | Combined | Assessment |
|---|---|---|---|---|
| IPT/TIG N-boundary | ~aa 239 | aa 263 (UniProt Q9H4W6) | ~aa 240 | Websearch most likely correct; UniProt annotation is authoritative for EBF3 specifically |
| IPT/TIG C-boundary | ~aa 328 | aa 346 (UniProt) | ~aa 305 | Websearch most likely correct |
| Pro263 position in domain | Mid-TIG | Exact N-terminal boundary of IPT/TIG | Mid-IPT/TIG | Websearch most likely correct — Pro263 is first residue of IPT/TIG |
| Dimer interface area | 490 Å² (TIG-alone, Treiber) | 1,960 Å² (combined HLH+TIG, Siponen) | Not cited | Both figures may be correct for different measurements; websearch context is misleading |
| Pathogenic missense clustering | TIG domain is structurally important (doesn't address clustering) | All in DBD (1–262), none in IPT/TIG | ZNF hotspot (163–209) | Combined most accurate: ZNF is the specific hotspot, not just all-DBD; Deisseroth 2022 fly assay supports ZNF-specific high risk |
| LOEUF | 0.353 (gnomAD v2) | 0.353/0.25 (version-dependent) | 0.25 (gnomAD v4) | Ground truth specifies 0.353; academic/websearch match |

---

## 5. Optimal Research API Routing Recommendation

### Summary verdict
**Combined > Academic > Websearch** on total score. Combined produces the most clinically useful output due to Deisseroth 2022 fly rescue data, ZNF hotspot specificity, and explicit PP3 inflation caveat. However, combined introduces a hallucinated journal citation and imprecise domain boundaries.

### Routing architecture

**For variant pathogenicity assessment of this type (rare VUS in high-penetrance NDD gene), the optimal strategy is sequential, not simultaneous:**

**Phase 1 — Websearch (databases, domain annotation):**
- Query UniProt for variant's protein domain position (IPT/TIG boundaries are the key disconfirmation)
- Query MaveDB for DMS absence confirmation
- Query gnomAD for allele frequency (websearch can access these; academic cannot)
- Query ClinVar for prior submissions
- *Goal: Establish the factual frame (domain position, population frequency, database absence) before literature synthesis*

**Phase 2 — Academic (literature synthesis):**
- Search PubMed/Semantic Scholar for gene-disease case series (Nishi, Deisseroth, Padhi)
- PMID verification — do not trust websearch-returned PMIDs without cross-checking
- Identify functional assay data (Padhi 2021 mislocalization data, Deisseroth fly assay)
- *Goal: Get peer-reviewed evidence on penetrance, functional mechanism, and phenotype*

**Phase 3 — Combined (synthesis with prior context from Phases 1+2):**
- Feed Phase 1 domain findings and Phase 2 literature into the combined prompt
- Combined performs best synthesis when it has concrete domain boundary data from websearch rather than inferring from EBF1 homology
- *Goal: ACMG weighing, clinical recommendation*

### What not to do
- **Don't run combined in isolation.** The Harms citation hallucination is a product of reasoning from training data about a less-indexed paper. With Phase 1+2 evidence as context, combined would not need to invent citations.
- **Don't trust websearch PDB IDs.** Websearch found the right papers but hallucinated PDB 3MUJ. Any structural biology claim from websearch should be independently verified against RCSB PDB or the actual paper.
- **Don't treat domain boundaries as interchangeable.** The 23-residue difference in the N-terminal IPT/TIG boundary between academic (~239) and UniProt (263) changes the clinical interpretation: Pro263 at the exact domain boundary is mechanistically different from Pro263 buried mid-domain.

### Key finding that changes clinical interpretation
The **websearch's domain clustering finding** — that no documented pathogenic EBF3 missense variant sits within the IPT/TIG domain proper (if UniProt boundaries are correct) — is the strongest single disconfirmatory result and was **missed by the academic strategy entirely**. The academic output concluded "TIG domain position is structurally significant" without checking whether any precedent pathogenic variant exists in that domain. This is a protocol gap: domain importance ≠ domain clustering. The combined output partially captured this via ZNF hotspot analysis but didn't explicitly state "no pathogenic missense in IPT/TIG."

This finding should be the first thing resolved in a reclassification workup: is Gly338Val actually pathogenic and actually within IPT/TIG (263–346)? If yes, IPT/TIG has one precedent. If no, the domain is completely uncharacterized for missense pathogenicity, strengthening BP5 application.

---

## Appendix: PMID Verification Summary

| PMID | Claimed by | Verified identity | Status |
|------|-----------|-------------------|--------|
| 29162653 | Academic | Tanaka et al. 2017, *Mol Case Studies* a002097 | ✓ Verified |
| 34050706 | Academic | Nishi et al. 2021, *AJMG-A* doi:10.1002/ajmg.a.62369 | ✓ Verified |
| 34256850 | Academic, Websearch, Combined | Padhi et al. 2021, *Human Genomics* | ✓ Verified |
| 35340043 | Websearch, Combined | Deisseroth et al. 2022, *Ann Neurol* doi:10.1002/ana.26359 | ✓ Verified |
| 28017372 | Websearch ("Chao 2016") | Chao et al. **2017**, *AJHG* (published online Nov 2016) | Year error — should be 2017 |
| 28017370 | Websearch PMC5223060 ("Sleven 2016") | Sleven et al. **2017**, *AJHG* (published online Nov 2016) | Year error — should be 2017 |
| 28736989 | Not cited directly | Harms FL et al. 2017, *Human Mutation* | Combined cites as "AJHG 100:117" — **wrong journal/page** |
| PMC2923972 | Websearch | Siponen et al. 2010, *JBC* (EBF3 IPT/TIG + HLHLH crystal) | Plausible; not independently confirmed but consistent |
| 40073166 | Academic (Spineli-Silva 2025) | Not independently verified | High PMID consistent with 2025; plausible |
| 37718233 | Academic (Batie 2023) | Not independently verified | PMID range consistent with 2023 |
| PDB 3MUJ | Websearch | **Not the Treiber 2010 structure.** Treiber 2010 = PDB 3MQN (EBF1); Siponen 2010 = PDB 3N50 (EBF3) | Likely hallucinated |
