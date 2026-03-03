# EBF3 p.Pro263Leu Variant Research Benchmark

Benchmark prompt for comparing research API strategies. Run via orchestrator
with different `allowed_tools` per strategy.

## Prompt

Research the clinical significance of a heterozygous EBF3 p.Pro263Leu missense variant (ClinVar VUS) found in whole-genome sequencing of a healthy adult male.

Context: This variant survived 4-agent verification as the sole TIER-1 finding from 365 rare HIGH/MODERATE variants in a personal WGS analysis. The gene has pLI=1.0, LOEUF=0.353, ClinGen Definitive for HADDS (Hypotonia, Ataxia, and Delayed Development Syndrome, OMIM #617330). Six deep-learning pathogenicity predictors concordantly score it as damaging. However, HADDS is caused by heterozygous loss-of-function — the question is whether this specific missense variant causes haploinsufficiency or is tolerated.

Research axes:

1. **Variant-level evidence:** Does p.Pro263Leu (or any missense at position 263) appear in ClinVar, LOVD, HGMD, or published case reports? What is the position's conservation across orthologs? Is position 263 within a known functional domain (DNA-binding, dimerization, transactivation)?

2. **Gene-level missense constraint:** What is EBF3's missense constraint (Z-score, regional constraint if available)? HADDS is primarily a LoF disorder — are there documented cases of HADDS or neurodevelopmental phenotypes caused by missense (not LoF) EBF3 variants? If so, are they clustered in specific domains?

3. **Functional data:** Has EBF3 been subjected to saturation mutagenesis (MAVE/DMS)? Check MaveDB. Are there cell-based or animal model functional assays for EBF3 missense variants? What is known about Pro->Leu substitution effects on helix-loop-helix transcription factor structure?

4. **Phenotype correlation:** HADDS presents in childhood with hypotonia, ataxia, delayed development. For an apparently healthy adult, what is the expected penetrance of pathogenic EBF3 variants? Are there reports of adults with EBF3 variants and subclinical or mild phenotypes (e.g., subtle coordination issues, learning differences)?

**Disconfirmation:** Search specifically for evidence that EBF3 missense variants are generally tolerated (benign), that Pro263 is not conserved, or that HADDS has no adult-onset presentation. Also search for healthy carriers of pathogenic EBF3 variants in population databases.

**Output format:** Claims table with evidence grades per the epistemics hierarchy below, domain map if findable, recommendation for clinical follow-up (or not).

Evidence grades: A1 (systematic review) > A2 (RCT) > B2 (functional assay/MAVE) > B3 (cohort/case-control) > C3 (ClinVar 3+ stars) > C4 (ClinVar 1 star) > D4 (case report) > E5 (in silico) > F6 (LLM-generated).

## Scoring Rubric

Grade each strategy's output on:

| Criterion | Weight | What to check |
|-----------|--------|---------------|
| Factual accuracy | 30% | Are PMIDs real? Are claims verified against primary sources? |
| Coverage | 25% | How many of the 4 axes + disconfirmation were addressed? |
| Source quality | 20% | Primary sources vs reviews vs training data? Evidence grades? |
| Null results | 15% | Did it correctly identify what data DOESN'T exist (e.g., no MAVE)? |
| Actionability | 10% | Clear recommendation, or hedged to uselessness? |

## Expected Ground Truth (for scoring)

- EBF3 pLI=1.0, LOEUF=0.353 (gnomAD)
- HADDS: OMIM #617330, ClinGen Definitive
- Most published HADDS cases are de novo LoF (frameshift, nonsense, splice)
- Some missense cases exist but are rarer
- No MAVE/DMS data for EBF3 (expected null — verify)
- Position 263 is in the IPT/TIG domain (immunoglobulin-like, if training data is correct — VERIFY)
- Healthy adults with pathogenic EBF3 variants: likely unreported (ascertainment bias)
