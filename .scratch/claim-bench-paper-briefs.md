# Claim-Bench Paper Briefs — 2026 Literature Audit

**Generated:** 2026-04-11
**Papers read:** 10/10 (all fetched full text)
**Status:** COMPLETE — all 10 papers fetched as PDF and queried via Gemini 1M-context `ask_papers`. No FETCH FAILED entries.

Initial fetches of arXiv 2604.03141, 2603.16544, 2602.10380, 2602.23193 failed on `/abs/` URLs but succeeded on `/pdf/` URLs after one retry each. All Tier 1 papers (4) and all Tier 2 papers (6) are full-text-backed.

---

## Paper 1 — arXiv:2602.13855 — From Fluent to Verifiable: Claim-Level Auditability for Deep Research Agents

**Status:** FETCHED FULL TEXT (16.9K tokens extracted)

**Authors/venue/date:** Razeen A Rasheed (IISc), Somnath Banerjee (IIT KGP, Cisco), Animesh Mukherjee (IIT KGP), Rima Hazra (TCG CREST). 2026. Perspective paper, no venue listed in preview.

**TL;DR** Position paper proposing a **Semantic Provenance Graph** with typed nodes (source/reasoning/claim) and typed edges (supports/contradicts/refines/prerequisite) as the auditability substrate for deep research agents; defines the **Auditable Autonomous Research (AAR) standard** with four computable metrics.

### Structured answers

**Q1 — Schema proposed:** A **Semantic Provenance Graph** `G_q = (V, E)` where `V = S_q ∪ R_q ∪ C_q` (source nodes, reasoning nodes, claim nodes), with typed edges.

- **Source node tuple:** `(id, DOI/URL, excerpt, timestamp)` — §4.3
- **Reasoning node tuple:** `(id, inference, type, model)` where `type ∈ {deduction, induction, synthesis}` and `model` identifies the generating LLM — §4.3
- **Claim node tuple:** `(id, statement, location)` where `location` specifies position in output — §4.3
- **Edge tuple:** `(u, v, rel, w)` where `rel ∈ {supports, contradicts, refines, prerequisite}`, and for `supports` edges `w ∈ [0, 1]` quantifies entailment strength (`w = null` otherwise) — §4.3

**Q2 — Claim identification level:** Claim nodes are defined as "the factual assertion answering (part of) q" (§4.3, Definition 7). **Not explicitly atomic**; they allow claims to cover partial answers. No sentence-level or sub-claim decomposition is mandated.

**Q3 — Metadata on claim→passage links:**
- **(a) Authority/source credibility:** YES — §5 states provenance must record "source reliability."
- **(b) Confidence score:** YES — edge weight `w ∈ [0, 1]` for `supports` edges quantifies entailment strength (Definition 8). §5 also mentions "extraction confidence."
- **(c) Evidence class (support/refute/neutral):** YES — the `rel` field is a typed enum `{supports, contradicts, refines, prerequisite}`. Note: **4 classes**, not the typical 3 (support/refute/neutral). `refines` and `prerequisite` are extras.

**Q4 — Position paper vs. implementation:** **Position/perspective paper, no code.** Abstract: "This perspective proposes claim-level auditability as a first-class design and evaluation target for deep research agents... and introduces the Auditable Autonomous Research (AAR) standard..." §1: "We (i) formalise operational requirements... (ii) propose a concrete provenance encoding... and (iii) demonstrate practical instrumentation..." No repo/dataset mentioned in extracted text.

**Q5 — Citable verbatim quotes:**
1. "As research generation becomes cheap, auditability becomes the bottleneck, and the dominant risk shifts from isolated factual errors to scientifically styled outputs whose claim–evidence links are weak, missing, or misleading." — Abstract
2. "A research agent is auditable if independent reviewers can verify claim correctness with effort E_verify ≪ E_generate, where verification accesses only: (1) agent outputs, (2) structured provenance graphs, and (3) cited sources." — §4.1
3. "deep research requires semantic provenance that preserves evidential structure, not merely action traces." — §1
4. "the failure mode is shifting from wrong answers to wrong citations: analyses have surfaced hallucinated references in technical writing pipelines... showing how attribution—central to reproducibility and credit assignment—can silently break under AI-mediated drafting." — §1
5. "Each edge (u, v, rel, w) ∈ E connects nodes with relation rel ∈ {supports, contradicts, refines, prerequisite}." — §4.3

**Q6 — Auditability measurement methodology:** Argumentation-based formal framework (AAR standard) with four computable metrics:
- **Provenance Coverage (P_Cov):** fraction of claims with complete traceable paths
- **Provenance Soundness (P_Snd):** whether cited sources actually entail attributed claims (semantic validity scores)
- **Contradiction Transparency (C_Tran):** proportion of evidence conflicts detected/reported
- **Audit Effort (A_Eff):** empirical time for expert to verify, or automated proxy counting steps/sources in provenance path
— §4.2, §4.3

**Q7 — Claim vs sub-claim distinction:** Paper does NOT formally distinguish claims from "atomic claims" or "sub-claims." It only says claims answer "(part of) q" — implying claims may span multiple atoms but the paper is silent on granularity. Critical gap: §4.3, Definition 7.

**VerificationEvent compatibility (plan Q):** The plan's `VerificationEvent {claim_id, passage_id, verdict, confidence, timestamp}` is **a strict SUBSET** of the Rasheed Semantic Provenance Graph. Concretely: `claim_id` maps to Claim node id; `passage_id` maps to Source node id; `verdict` ≈ `rel` (but our 3-class vs their 4-class); `confidence` ≈ edge weight `w`; `timestamp` maps to Source node timestamp. The superset Rasheed graph adds: (a) Reasoning nodes with inference type tagging, (b) `refines`/`prerequisite` relation types, (c) typed node distinction between source/reasoning/claim. VerificationEvent is flat, theirs is typed-node-graph. A one-way adapter is straightforward (emit VerificationEvent, then materialize a subgraph).

**Confidence:** high — read full body, methodology and schema section extracted verbatim.

---

## Paper 2 — arXiv:2603.05912 — DeepFact: Co-Evolving Benchmarks and Agents for Deep Research Factuality

**Status:** FETCHED FULL TEXT (14.5K tokens extracted)

**Authors/venue/date:** Yukun Huang (Duke), Leonardo F.R. Ribeiro (Amazon AGI), Momchil Hardalov (Amazon AGI), Bhuwan Dhingra (Duke), Markus Dreyer (Amazon AGI), Venkatesh Saligrama (Amazon AGI/BU). 2026.

**TL;DR** Proposes **Audit-then-Score (AtS)**: a 4-stage co-evolutionary protocol where a Challenger agent disagrees with the current benchmark state, an Auditor adjudicates, and accepted updates version-bump the benchmark. Ships a 944-claim benchmark from 20 reports across 6 domains. Headline: DeepFact-Eval reaches 83.4% vs 58.5% for traditional fact-checkers; expert auditor accuracy climbs from 60.8% (one-shot) to 90.9% (over 4 AtS rounds).

### Structured answers

**Q1 — AtS mechanics (4 stages, Figure 1 verbatim):**
1. **Evaluate:** "Run a Challenger agent (M_t) on the current benchmark state (B_t), producing a verdict ŷ_i."
2. **Challenge:** "When ŷ_i ≠ y_i^(t), the Challenger submits a proposal with evidence."
3. **Audit:** "An Auditor (human expert or trusted agent) adjudicates the dispute; if the Challenger's argument is stronger than the incumbent rationale, the update is accepted."
4. **Evolve & Score:** "Accepted updates yield the next benchmark state (B_{t+1}); the Challenger is then scored against this refined ground truth."

Formal state transition: `B_{t+1} = F(B_t, U_{M,t}, A_t)` — §5.1.

**Q2 — Benchmark format:**
- **(a) Case count:** 944 claims from 20 reports. Split: 323 claims (5 reports) validation, 621 claims (15 reports) test. Test set includes 143 micro-golds, 120 adversarially constructed — §6.5.
- **(b) Schema per instance:** "a verbatim claim sentence, its source report as context, a final expert verdict, and a supporting rationale" — §6.5. Verdict space: SUPPORTED, INCONCLUSIVE, CONTRADICTORY.
- **(c) Domains (6):** computer science, control theory, environmental engineering, education, public health, engineering management — §4.2, §6.5.

**Q3 — Verifier/benchmark co-evolution mechanism:** "each evaluated model becomes both a subject of evaluation and a potential contributor to future benchmark revisions" (§5.1). New Challenger provides rationale+evidence; if Auditor deems Challenger's argument stronger than incumbent rationale, benchmark version advances. The benchmark "co-evolves with agent capabilities" — §1, §5.1.

**Q4 — `inspect_ai.Sample` compatibility:** Paper does not mention inspect_ai. Schema maps cleanly to `(id, input, target, metadata)`:
- **input:** verbatim claim sentence + source report as context
- **target:** expert verdict (SUPPORTED / INCONCLUSIVE / CONTRADICTORY)
- **metadata:** supporting rationale + versioning info (B_t state id)

The explicit versioning (`B_t` state id) is an extra field beyond inspect_ai's native schema; would need to live in metadata.

**Q5 — Revisability:** YES, explicit. "benchmark labels and rationales are explicitly revisable" (Abstract). "ongoing dialogue" rather than "frozen snapshot" (§1). Mechanism: if Challenger rationale demonstrates "superior evidential quality or coherence" vs incumbent, Auditor accepts and benchmark version advances — §5.1.

**Q6 — Citable verbatim quotes:**
1. "Rather than a one-shot 'human-gold → model evaluation' pipeline, AtS treats benchmarking as a co-evolutionary process: model disagreements trigger auditing, and accepted revisions update the shared consensus over time." — §5.1
2. "AtS treats the benchmark as a versioned state B_t. The state at time t+1 is a function of the previous state, the Challenger's proposals, and the Auditor's decisions: B_{t+1} = F(B_t, U_{M,t}, A_t)." — §5.1
3. "The benchmark contains 944 claims from 20 reports spanning six domains." — §6.5
4. "Across four AtS rounds, expert micro-gold accuracy rises to 90.9%, indicating experts are substantially more reliable as auditors than as one-shot labelers." — Abstract
5. "DeepFact-Eval (GPT-4.1) achieved 83.4% accuracy, significantly outperforming traditional pipelines (max 58.5%) and deep-research agents (max 69.1%)." — §7.2

**Q7 — Evaluated models:**
- Traditional fact-checkers: FactCheck-GPT, SAFE, VeriScore, FIRE
- Deep research agents (repurposed): GPT-Researcher (Deep/Deep+), SmolAgents
- Their agents: DeepFact-Eval (Expert and Lite/Grouped)
- Backbones tested: GPT-4.1, GPT-5, Gemini-2.5-Pro, Qwen-3-32B — §7.1, §7.2

**Headline:** DeepFact-Eval 83.4% vs traditional max 58.5% vs deep-research max 69.1%. Unassisted expert 60.8% → expert-as-auditor 90.9% (4 rounds).

**Confidence:** high — full body extracted, mechanism and numbers verified.

---

## Paper 3 — arXiv:2603.28005 — A Matched Holistic Rubric Rivals Self-Decomposing Atomic Judges for Benchmark-Style Reference-Support Classification

**Status:** FETCHED FULL TEXT (12.9K tokens extracted)

**Authors/venue/date:** Xinran Zhang (UC Berkeley). 2026 preprint under review. **Note:** title as fetched differs from the task spec "Rethinking Atomic Decomposition for LLM Judges" — this is the same paper, Zhang apparently renamed between arXiv versions or the task cites an earlier working title.

**TL;DR** Controlled empirical counterexample to the "atomic decomposition is automatically better" heuristic. A matched holistic rubric matches or beats self-decomposing atomic judges on 2 of 3 benchmarks (ASQA, QAMPARI) when prompt richness and JSON schema are controlled. Token cost of atomic is 1.4–2.3× higher but delivers no accuracy gain on completeness-heavy tasks.

### Structured answers

**Q1 — Headline conclusion:** **(c) NEUTRAL or INFERIOR on 2 of 3 benchmarks after control.** Abstract: "we find the holistic judge matches or exceeds the atomic judge on two of three benchmarks: ASQA and QAMPARI favor holistic across all four families... while TruthfulQA shows a small atomic edge." Conclusion (§7): "a prompt-controlled holistic rubric matches or outperforms the atomic judge on completeness-heavy settings (ASQA, QAMPARI), while TruthfulQA shows a small atomic edge."

**Q2 — Experimental setup:** Four axes of control (§3.2, §3.3 verbatim): "(1) same underlying model, (2) same input fields, (3) similarly detailed JSON output instructions, and (4) realized token usage measured directly." 3 independently worded prompt variants per method family. 200 source examples per dataset, 400 pointwise rows per dataset. 3 datasets: **TruthfulQA, ASQA, QAMPARI**. 4 models: **Opus-4.6, gpt-4.1, gemini-3.1-flash-lite, deepseek-v3.2**.

**Q3 — Recommended prompt design:** Detailed holistic rubric with fields for correctness, completeness, unsupported detail, and resistance to style bias. §7: "Within this scope, should practitioners default to the self-decomposing single-prompt atomic pattern? Our evidence suggests not—a matched holistic rubric is competitive on two of three benchmarks and cheaper on all three."

**Q4 — Invalidation vs complication:** COMPLICATION, not invalidation. Paper is explicit that the finding is **specific to self-decomposing single-prompt atomic**, NOT multi-stage or externally-decomposed atomic pipelines. §1: "We do not claim that atomic structure is inherently inferior. Our finding is specific to the self-decomposing single-prompt pattern on three QA-style benchmarks... multi-stage atomic pipelines and non-QA tasks remain untested." §7: "Stronger atomic variants (externally supplied decompositions, multi-stage pipelines) remain untested... We do not recommend against atomic evaluation in general."

**Q5 — Citable verbatim quotes:**
1. "Our contribution is a controlled empirical counterexample to the heuristic that decomposition is automatically advantageous." — §1
2. "The main comparison is controlled in four ways: (1) same underlying model, (2) same input fields, (3) similarly detailed JSON output instructions, and (4) realized token usage measured directly." — §3.2
3. "The holistic advantage is concentrated in incompleteness detection (`partially_supported` cases), not generic accuracy." — §1
4. "Within this scope, should practitioners default to the self-decomposing single-prompt atomic pattern? Our evidence suggests not—a matched holistic rubric is competitive on two of three benchmarks and cheaper on all three." — §7
5. "Among the perturbations we tested, reference-quality degradation produced larger accuracy drops than schema or output-structure changes." — §1

**Q6 — Token-cost confound evidence:** YES explicit. Table 5 shows atomic judges produce **1.4–2.3× more tokens** on ASQA and QAMPARI. §4.4 paraphrased: atomic "does not buy accuracy commensurate with its token overhead on completeness-heavy tasks." Key quote: "If atomic judges outperform holistic ones, the gain may come from prompt richness or extra generation rather than from decomposition itself."

**Q7 — Prompt variants compared:**
1. **Atomic Judge v1-v3:** single-prompt decompose-and-verify
2. **Prompt-Controlled Holistic Judge v1-v3:** detailed rubric (correctness, completeness, unsupported detail, style-bias resistance)
3. **Schema-Matched Judge (ablation):** atomic-style JSON fields but no decomposition instruction — isolates output format effect
4. **Budget control:** max output tokens 128, 256, 512
5. **Grounding sensitivity:** reduced (paraphrased) and removed (no reference) inputs

**Confidence:** high — controlled experimental design cleanly described, headline finding unambiguous. **Critical caveat for plan:** applies to single-prompt atomic only; externally-decomposed atomic pipelines (what FIRE-Bench and similar use) are explicitly UNTESTED.

---

## Paper 4 — arXiv:2604.00131 — OBLIVION: Self-Adaptive Agentic Memory Control through Decay-Driven Activation

**Status:** FETCHED FULL TEXT (10.7K tokens extracted)

**Authors/venue/date:** Ashish Rana, Chia-Chien Hung, Qumeng Sun, Julian Martin Kunkel, Carolin Lawrence. NEC Labs Europe (Heidelberg) + GWDG Göttingen. 2026.

**TL;DR** Memory framework using an Ebbinghaus-inspired retention score R_t(c) = exp(-n/S) with learned utility + access-frequency stability S; Recognizer/Activator/Decayer modules handle write/read/gate; triggers activation only when uncertainty signals cross threshold. LONGMEMEVAL 89.0% → 90.6%; 73% token reduction at 120K span.

### Structured answers

**Q1 — Decay-driven activation mechanism:** "memory control framework that casts forgetting as decay-driven reductions in accessibility—not explicit deletion" (Abstract). Math (§2.2):

```
R_t(c) = exp(-n_t(c) / S_t(c))
S_t(c) = (1 / (U_t(c) + F_t(c) + ε)) · T
```

where `n_t(c)` = turns since cluster c last accessed, `U_t(c) ∈ [0,1]` = learned utility proxy, `F_t(c) ∈ [0,1]` = access-frequency proxy, `ε` prevents zero division, `T` = decay temperature (stability scale).

**Q2 — Recognizer / Activator definitions (§2.3, §2.2):**
- **Recognizer (§2.3):** "(i) extracts new L_2 factual memories and accumulates episodic entries toward L_3 episodes; (ii) constructs or updates L_1 cluster topics—including procedural memory—based on observed interaction patterns; and (iii) performs credit assignment by identifying which specific memory entries in B_t were used to generate the response."
- **Activator (§2.2):** "When triggered, the Activator reduces uncertainty by retrieving L_2/L_3 entries from D and updating B_t under fixed cache budgets."
- **Decayer (§2.2):** computes R_t(c) via Ebbinghaus curve; gates activation through uncertainty+retention checks.

**Q3 — Re-verification trigger / gating logic (§2.2 verbatim):** "Activation is always triggered when B_t contains no L_2/L_3 items. Otherwise, the gating threshold adapts across rounds: in the first round, either signal alone suffices (OR), favoring recall over precision; in subsequent rounds, both must agree (AND), preventing redundant retrieval once the buffer is already populated."

Two gating signals: (i) uncertainty estimation ("Whether to retrieve?"), (ii) retention scoring ("Which memories remain accessible?").

**Q4 — Comparison vs discrete TTL:** **NO explicit comparison to discrete TTL baselines in extracted text.** Compared against LME-RFT, FULLCTX (direct baselines) and EVERMEMOS, BEYONDPROMPTS (memory baselines) — §3.2. Discrete TTL is not on their baseline list.

**Q5 — Is integer TTL a degenerate case of the continuous retention function?** The paper does not discuss this explicitly. However, based on the formula R_t(c) = exp(-n_t(c) / S_t(c)), a per-modality integer TTL maps to a step function that is **not a natural specialization** of this exponential form. An integer TTL corresponds to `R = 1 if age < TTL else 0`, while Oblivion produces continuous decay with no hard cutoff. They are structurally different regimes: TTL is piecewise-constant, Oblivion is continuous-smooth. The plan's TTL approach could be approximated by choosing a large T (slow decay) and clipping R at a threshold, but this would not replicate Oblivion's interaction-driven adaptive decay.

**Q6 — Retention function form:** **Exponential decay** (Ebbinghaus form). §2.2: "the Decayer computes R_t(c) via an interaction-based forgetting curve (Ebbinghaus, 1885; Woźniak et al., 1995): R_t(c) = exp(-n_t(c) / S_t(c))". Stability S is data-adaptive (U+F-driven).

**Q7 — Citable verbatim quotes:**
1. "OBLIVION, a memory control framework that casts forgetting as decay-driven reductions in accessibility—not explicit deletion." — Abstract
2. "R_t(c) = exp(-n_t(c) / S_t(c)), S_t(c) = (1 / (U_t(c) + F_t(c) + ε)) · T" — §2.2
3. "Activation is always triggered when B_t contains no L_2/L_3 items. Otherwise, the gating threshold adapts across rounds: in the first round, either signal alone suffices (OR), favoring recall over precision; in subsequent rounds, both must agree (AND), preventing redundant retrieval once the buffer is already populated." — §2.2
4. "The Recognizer: (i) extracts new L_2 factual memories... (ii) constructs or updates L_1 cluster topics... (iii) performs credit assignment..." — §2.3
5. "OBLIVION demonstrates superior stability across all spans; for GPT-4.1-mini, solved scenarios rise from 6.29 to 8.41 (2K) and 6.05 to 6.79 (32K) compared to FULLCTX." — §4.2

**Q8 — Benchmark & deltas:**
- **LONGMEMEVAL** (static retrieval-heavy QA) & **GOODAILTM** (dynamic long-horizon) — §3.1
- Headline: LONGMEMEVAL (S) GPT-4.1-mini **89.0% → 90.6%** — §4.1
- GOODAILTM (2K) GPT-4.1-mini **6.29 → 8.41 solved scenarios** vs FULLCTX — §4.2
- **73% token reduction** at 120K span — §5.3

**Confidence:** high — formula, architecture, and benchmarks all extracted verbatim.

---

## Paper 5 — arXiv:2604.03141 — Beyond Precision: Importance-Aware Recall for Factuality Evaluation in Long-Form LLM Generation

**Status:** FETCHED FULL TEXT (9.6K tokens extracted)

**Authors/venue/date:** Nazanin Jafari (UMass Amherst), James Allan (UMass Amherst), Mohit Iyyer (U. Maryland). 2026 preprint under review.

**TL;DR** Extends factuality eval from precision-only to importance-weighted recall. Each reference fact gets two LLM-judged scalars (Relevance, Salience) on 1-5 scales, normalized to [0,1], combined as composite importance. Weighted recall weights each covered fact by its importance.

### Structured answers (abbreviated — Tier 2)

**Q1 — Importance-weighting mechanism:** §3.2.3: "We therefore assign each fact f_k ∈ F an importance score that captures both its query-specific relevance and its broader salience with respect to the answer topic."

**Q2 — Source of salience scores:** **(a) LLM-scored.** §3.2.3 verbatim: "Concretely, for each fact f_k and query q, an LLM judge assigns two discrete ratings on a 1–5 scale based on Relevance to capture how relevant f_k is to answering the query q and Salience to capture how central f_k is to the main topic/entity/entities implicated by q, independent of any particular document's phrasing."

**Q3 — Importance weight type:** **Composite scalar in [0,1]**. §3.2.3: normalized `r̃_k = (r_k - 1)/4`, `s̃_k = (s_k - 1)/4`. Composite: `imp(f_k; q) = α·r̃_k + β·s̃_k` where α, β ≥ 0 tune relevance-vs-salience trade-off.

**Q4 — Recall formula (§3.4):**
- Unweighted: `Rec_F = (1/|F*(q)|) · Σ_{f_k ∈ F*} 1[y_k^cov = COVERED]`
- Importance-weighted: `Rec_F^w = Σ imp(f_k; q) · 1[y_k^cov = COVERED] / Σ imp(f_k; q)`

**Q5 — Eval & headline:** Evaluated on **FactScore (Bio), LongFact, LongForm**. Headline: "current LLMs perform substantially better on precision than on recall, suggesting that factual incompleteness remains a major limitation of long-form generation and that models are generally better at covering highly important facts than the full set of relevant facts" (Abstract).

**Q6 — Citable verbatim quotes:**
1. "We therefore assign each fact f_k ∈ F an importance score that captures both its query-specific relevance and its broader salience with respect to the answer topic." — §3.2.3
2. "Rec_F^w = Σ_{f_k∈F*} imp(f_k; q)·1[y_k^cov = COVERED] / Σ imp(f_k; q)" — §3.4
3. "current LLMs perform substantially better on precision than on recall..." — Abstract
4. "Prec_F = (1/|C|) Σ_{ℓ=1}^L 1[y_ℓ^prec = SUPPORTED]" — §3.4
5. "Overall, longer generations are neither necessary nor sufficient for better factuality. Although greater verbosity can improve recall, it often reduces precision and yields limited gains when the main challenge is selecting and aligning the right facts." — §4.2.1

**Confidence:** high — formula and methodology cleanly described.

---

## Paper 6 — arXiv:2603.16544 — How often do Answers Change? Estimating Recency Requirements in Question Answering

**Status:** FETCHED FULL TEXT (9.3K tokens extracted)

**Authors/venue/date:** Bhawna Piryani (U. Innsbruck), Zehra Mert (MEF University Istanbul), Adam Jatowt (U. Innsbruck). 2026.

**TL;DR** Does NOT publish per-topical-category decay rates. Instead defines a **12-class recency taxonomy** from "An-Hour" to "Never" and a **stationarity** distinction (stable vs context-dependent). Ships RECENCYQA with 4,031 questions.

### Structured answers (abbreviated — Tier 2)

**Q1 — Per-category decay rates:** **NO.** The paper does NOT publish topical-category decay rates (e.g., "sports = 1 day, politics = 30 days"). Instead, it maps questions to 12 temporal classes based on expected change interval.

**Q2 — What they measure:**
- **Recency** (§3): "the expected temporal stability of a question's answer—that is, how soon the answer is likely to change under typical real-world conditions"
- **Stationarity** (§3): "the stability of a question's recency behavior over time... a question is stationary if its recency label remains consistent... non-stationary... exhibits different recency patterns depending on the temporal context"
- **Transition Accuracy** (Table 7): adaptation success across contexts for non-stationary questions

**Q3 — Recency taxonomy (Table 2, 12 classes):**
1. An-Hour
2. A-Few-Hours
3. A-Day
4. A-Few-Days
5. A-Week
6. A-Few-Weeks
7. A-Month
8. A-Few-Months
9. A-Year
10. A-Few-Years
11. Many-Years
12. Never

**Q4 — Per-domain numeric TTLs for adoption:** **NO.** Paper explicitly does not propose per-domain TTLs. It labels individual questions, not domains. The 12-class taxonomy is a labeling system for the instances in RECENCYQA, not a set of defaults for adoption. §1: existing benchmarks "lack a principled way to estimate a question's recency demand."

**Q5 — Citable verbatim quotes:**
1. "Large language models (LLMs) often rely on outdated knowledge when answering time-sensitive questions, leading to confident yet incorrect responses." — Abstract
2. "Recency captures the expected temporal stability of a question's answer—that is, how soon the answer is likely to change under typical real-world conditions." — §3
3. "A question is stationary if its recency label remains consistent... In contrast, a non-stationary question... exhibits different recency patterns depending on the temporal context." — §3
4. "Existing benchmarks typically frame recency as a binary distinction between current and outdated information, without modeling the expected rate at which answers change." — §2
5. "Non-stationary questions, i.e. those where context changes the recency requirement, are significantly more challenging for LLMs, with difficulty increasing as update frequency rises." — Abstract

**Q6 — Dataset & categories:**
- **RECENCYQA:** 4,031 open-domain questions
- Sources: FreshQA, PATQA, SituatedQA + LLaMA 3.3 (70B)-generated event questions
- Categories: 12 recency classes × 2 stationarity labels; also Singlehop (3,161) / Multihop (870)
— §4.1, Table 3

**Confidence:** high — clear description of taxonomy structure. **Key takeaway for plan: this paper establishes a 12-class labeling vocabulary and the stationarity distinction, but provides no per-modality defaults. The plan cannot cite this paper for numeric TTL values.**

---

## Paper 7 — arXiv:2602.10380 — The Alignment Bottleneck in Decomposition-Based Claim Verification

**Status:** FETCHED FULL TEXT (14.2K tokens extracted)

**Authors/venue/date:** Mahmud Elahi Akhter (QMUL), Federico Ruggeri (U. Bologna), Iman Munire Bilal (Warwick), Rob Procter (Warwick), Maria Liakata (QMUL, Alan Turing). 2026.

**TL;DR** Diagnostic study: decomposition helps **only** when sub-claims are paired with sub-claim-specific evidence (SAE); with repeated claim-level evidence (SRE), models collapse to ~0.44 F1. Error amplification quantified at ~0.19 F1 drop under noisy label conditions.

### Structured answers (abbreviated — Tier 2)

**Q1 — Alignment definition:** **Sub-claim Aligned Evidence (SAE)** — structural pairing where each sub-claim is co-located with its own evidence block. §4.1: "SAE inserts the sub-claim-specific evidence block E_j next to its sub-claim s_j." Abstract: "decomposition brings significant performance improvement only when evidence is granular and strictly aligned."

Not semantic or embedding-based — structural/positional pairing of text blocks.

**Q2 — Error amplification quantified:** YES.
- Methodology: compare Oracle_SAE (best case) vs Noisy_SRE (noisy labels + repeated claim-level evidence)
- §5.4: "Under SRE, the models collapse (dropping to ≈ 0.44 F1), confirming that redundant claim-level evidence exacerbates error propagation from noisy sub-claim labels."
- Table 3: Qwen Oracle_SAE → Noisy_SRE: **ΔF1 = -0.1933, Δ balanced accuracy = -0.2147**

**Q3 — Headline:** Abstract: "decomposition brings significant performance improvement only when evidence is granular and strictly aligned. By contrast, standard setups that rely on repeated claim-level evidence (SRE) fail to improve and often degrade performance."

**Q4 — Citable verbatim quotes:**
1. "We argue that these inconsistencies stem from two overlooked bottlenecks: evidence alignment and sub-claim error profiles." — Abstract
2. "By contrast, standard setups that rely on repeated claim-level evidence (SRE) fail to improve and often degrade performance..." — Abstract
3. "This indicates that granular, sub-claim-level, evidence is insufficient on its own. Without the signal from correct sub-claim veracity labels, the model struggles to synthesize the fine-grained information, leading to inference errors that coarser evidence setups seem to avoid." — §5.2
4. "Under SRE, the models collapse (dropping to ≈ 0.44 F1), confirming that redundant claim-level evidence exacerbates error propagation from noisy sub-claim labels." — §5.4
5. "Ultimately, we conclude that the primary bottleneck for deployment in real-world settings is not decomposition itself, but the capability for precise evidence synthesis and alignment." — §7

**Q5 — Fix proposed?** **No** — purely diagnostic. §3.2: "fixed decomposition procedure to isolate the effects... rather than optimizing the decomposition model itself." Future work: "precise evidence synthesis" and "calibrating the label bias" (§7).

**Q6 — Datasets:** **PHEMEPlus** (event-centric rumors), **MMM-Fact** (multi-domain), **COVID-Fact** (health) — §3.2.

**Confidence:** high — key numbers and mechanism clean.

---

## Paper 8 — arXiv:2602.23193 — ESAA: Event Sourcing for Autonomous Agents in LLM-Based Software Engineering

**Status:** FETCHED FULL TEXT (8.9K tokens extracted)

**Authors/venue/date:** Elzo Brito dos Santos Filho. February 2026. Independent author (elzo.santos@cps.sp.gov.br).

**TL;DR** Architectural pattern: agents emit structured **intentions** (JSON), deterministic orchestrator validates, appends to `activity.jsonl`, and projects `roadmap.json`. Immutable event log + deterministic projection enables replay debugging. Ships public repo at "initial/clean state."

### Structured answers (abbreviated — Tier 2)

**Q1 — Event model field names:**

**Agent Output Contract (Appendix A, JSON Schema):**
```
required: ["schema_version", "correlation_id", "task_id", "attempt_id",
           "actor", "action", "idempotency_key", "payload"]
```

**Event store entry example (Appendix E):**
```json
{"ts":"2026-02-19T21:55:44","action":"claim","task_id":"T-2301",
 "agent_id":"claude-opus-4-6","acceptance_results":null}
```
Fields observed in stored entries: `ts`, `action`, `task_id`, `agent_id`, `acceptance_results`.

**Q2 — Reference implementation:**
- **Pseudocode in Appendix D:** `canonical_json(obj)`, `hash_input(projected_state)`, `compute_projection_hash(projected_state)` — Python-like
- **Public repo:** §4.3 — "For open reproducibility purposes, the project's public repository provides the architecture in its initial state (clean state)..."
- **Future work:** §8 — "Future work includes: (i) an official CLI (`esaa init/run/verify`)..."
- Verdict: **Pattern description + reference skeleton, not a production library.**

**Q3 — Event types:**

**Canonical vocabulary (Table 3, 15 types):**
`run.init`, `attempt.create`, `attempt.timeout`, `orchestrator.dispatch`, `agent.result`, `issue.report`, `output.rejected`, `orchestrator.file.write`, `orchestrator.view.mutate`, `task.create`, `task.update`, `verify.start`, `verify.ok`, `verify.fail`, `run.end`

**Simplified vocabulary (Table 4):** `roadmap.version`, `promote`, `claim`, `complete`, `phase.complete`

**Q4 — Base Event struct:** NO Python dataclass — defined as JSON Schema. Agent `action` is constrained: `enum: ["agent.result", "issue.report"]` for agent output.

**Q5 — VerificationEvent compatibility:** **Partially compatible**. claim_bench `VerificationEvent {claim_id, passage_id, verdict, confidence, timestamp}` would need to be wrapped inside ESAA's `payload` field of an `agent.result` action. Mapping:
- `claim_id` → `payload.claim_id`
- `passage_id` → `payload.passage_id`
- `verdict, confidence` → `payload.summary` or `payload.verification`
- `timestamp` → top-level `ts`

ESAA adds mandatory correlation fields (`schema_version, correlation_id, task_id, attempt_id, actor, idempotency_key`) that VerificationEvent doesn't have. Adapter required, not drop-in.

**Q6 — Citable verbatim quotes:**
1. "Event store (`activity.jsonl`): an append-only log of ordered events (`event_seq`), containing intentions, dispatches, effects, and run closures." — §3.1
2. "ESAA applies the Event Sourcing pattern to the agent's lifecycle: the source of truth is not the current snapshot of the repository, but an immutable log of intentions, decisions, and effects, from which the current state is deterministically projected." — §1
3. "Concurrent execution is naturally serialized at the event level: multiple agents can work in parallel, but their results are validated and appended sequentially, preserving total ordering in the log." — §3.4
4. "The immutability of done rule defines that completed tasks cannot regress. In case of a defect, an `issue.report` event creates a new correction path (hotfix) without reopening the history, preserving the decision trail." — §3.2
5. "To ensure reproducibility via replay, ESAA specifies deterministic canonicalization of the projected state and hash calculation... The SHA-256 hash of the canonicalized read-model (`projection_hash_sha256`) allows for the detection of divergence between projection and materialization." — §3.3

**Q7 — Snapshots / compaction / replay:**
- **Replay:** emphasized — "time-travel debugging via replay: reprocessing the event store from event zero to reconstruct the read-model exactly" (§6.2)
- **Snapshots:** NOT used; the paper explicitly criticizes AutoGen/MetaGPT/LangGraph for relying on "in-memory data structures or database snapshots, lacking the immutable audit trail" (§1)
- **Compaction:** NOT discussed in extracted text

**Confidence:** high — schema, event types, and semantics all extracted.

---

## Paper 9 — arXiv:2603.25097 — ElephantBroker: A Knowledge-Grounded Cognitive Runtime for Trustworthy AI Agents

**Status:** FETCHED FULL TEXT (28.6K tokens extracted — longest paper in set)

**Authors/venue/date:** Cristian Lupascu (PhD), Alexandru Lupascu. Elephant Broker, Bucharest Romania. 2026.

**TL;DR** System/architectural paper proposing a cognitive runtime with: **fact assertions** as core entity (12 categories), a **four-state verification model** (UNVERIFIED, SELF-SUPPORTED, TOOL-SUPPORTED, SUPERVISOR-VERIFIED) mapped to scalar confidence multipliers, typed graph edges for provenance, exponential decay recency with bi-temporal metadata, property graph formalization. 2,200+ tests, architectural validation only — no task-benchmark evaluation.

### Structured answers (abbreviated — Tier 2)

**Q1 — Provenance tracking mechanism:**

**Fact assertion fields (§3.2):** "content text, a category drawn from twelve built-in types (identity, preference, event, decision, system, relationship, trait, project, general, constraint, procedure reference, and verification)... a scope, a memory class, a confidence score, source and target actors, goal associations, and goal relevance tags."

**Graph provenance (§3.2.3):** "The actor model uses typed graph edges (authorship, actor-about, goal-serving, goal-ownership) to maintain provenance chains that can be traversed during retrieval."

**Bi-temporal metadata (§3.2.5):** "Every fact and graph edge carries explicit temporal metadata... three timestamps: an event timestamp... an ingestion timestamp... and an update timestamp."

**Q2 — Trustworthiness tracking:** **Typed enum (state machine) mapped to scalar multipliers.** §3.6:

| State | Multiplier |
|-------|-----------|
| SUPERVISOR-VERIFIED | 1.0 |
| TOOL-SUPPORTED | 0.9 |
| no associated claims | 0.8 (default) |
| SELF-SUPPORTED | 0.7 |
| UNVERIFIED | 0.5 |

"The verification state connects to the scoring engine through graded confidence multipliers... creating a feedback loop where verified facts gain a sustained competitive advantage in working set selection."

**Q3 — AuthorityClass analog:** YES but different axis. ElephantBroker has TWO discrete classifications:

**Actor types (§3.2.3, 12 types):** human roles (coordinator, operator, external), agent roles (manager, worker, reviewer, supervisor, peer, service, external), orgs (teams, organizations).

**Authority tiers (§3.9.1, 4 levels — access control, not source credibility):**
- Regular actors: level 0-49
- Team leads: 50-69
- Organization administrators: 70-89
- System administrators: 90+

**Mapping to claim_bench AuthorityClass:** ElephantBroker's **four-state verification model** is the closer analog to an AuthorityClass enum (UNVERIFIED/SELF/TOOL/SUPERVISOR-VERIFIED). But their levels are about *who verified*, not *what type of source* (e.g., PEER_REVIEWED vs BLOG). Their actor-type enum (12 roles) does not cleanly map to source credibility tiers.

**Q4 — Temporal mechanism:** **YES, exponential decay with bi-temporal metadata.** §3.5.2: "Recency applies an exponential decay function: `r(t) = exp(-(ln 2 / t_{1/2}) · Δt)` where Δt is time since last access... half-life t_{1/2} is set per profile preset."

Two decay modes (§3.15):
- Recalled but unused: `c' = c · 0.9^t_r` (t_r = recall turns)
- Never recalled: `c' = c · 0.95^t_d` (t_d = days since creation)

TTL also present: "Bucket 1 holds session-scoped goals in the cache with a configurable TTL" (§3.10).

**Q5 — Citable verbatim quotes:**
1. "The core entity is the fact assertion, which represents a unit of agent memory and includes fields for content text, a category... a scope, a memory class, a confidence score, source and target actors, goal associations, and goal relevance tags." — §3.2
2. "The evidence system implements a four-state verification model that tracks claim trustworthiness over the lifetime of a fact... The highest level, SUPERVISOR-VERIFIED, is reached when a human supervisor provides an explicit sign-off." — §3.6
3. "The actor model uses typed graph edges (authorship, actor-about, goal-serving, goal-ownership) to maintain provenance chains that can be traversed during retrieval." — §3.2.3
4. "Every fact and graph edge carries explicit temporal metadata that supports bi-temporal reasoning over the knowledge base. Each fact assertion records three timestamps: an event timestamp... an ingestion timestamp... and an update timestamp." — §3.2.5
5. "The verification state connects to the scoring engine through graded confidence multipliers... creating a feedback loop where verified facts gain a sustained competitive advantage in working set selection." — §3.6

**Q6 — Paper type:** **System/architectural paper.** No empirical task evaluation. §5.6 verbatim: "The current evaluation is architectural rather than empirical: we validate correctness through systematic testing but do not yet report end-to-end task completion metrics or hallucination reduction rates on standardized benchmarks." Abstract: "2,200 tests spanning unit, integration, and end-to-end levels confirms subsystem correctness."

**Q7 — Claim-to-evidence link representation:** Property graph, §3.2:
```
G = (N, E, φ)
N = {facts, actors, goals, procedures, claims, evidence, artifacts}
E = typed directed edges (authorship, supersession, contradiction,
    goal-serving, ownership, parent-child)
```

Scoring traverses (§3.5.1): "(1) evidence counts via a graph chain traversal (Evidence→Claim→Fact)".

**Confidence:** high — very detailed paper extracted.

---

## Paper 10 — arXiv:2601.21116 — AI-Assisted Engineering Should Track the Epistemic Status and Temporal Validity of Architectural Decisions

**Status:** FETCHED FULL TEXT (15.8K tokens extracted)

**Authors/venue/date:** Sankalp Gilda (DeepThought Solutions), Shlok Gilda (U. Florida CS). 2026 preprint. Position paper with reference implementation (anonymized) and retrospective audit of 62 ADRs across 2 projects.

**TL;DR** CRITICAL PAPER FOR THE PLAN. Defines **F0–F3 formality levels** (rigor of claim expression), **L0–L2 epistemic layers** (verification stage), **CL0–CL3 scope congruence** (evidence transfer penalty), **Gamma Invariant Quintet** (conservative aggregation), and **evidence decay with uncertainty floor at 0.1** (distinguishes epistemic uncertainty from low confidence). Reference implementation is "an existence proof, not the contribution."

### Structured answers (DETAILED — this is the critical paper for the plan)

**Q1 — F0-F3 formality levels (Table 1, §2.1, verbatim):**

| Level | Name | Example | Reliability Ceiling |
|-------|------|---------|---------------------|
| F0 | Informal | "Felt faster in staging" | **70%** |
| F1 | Structured | ADR with trade-offs | **85%** |
| F2 | Empirical | "Load test: 12k RPS" | **95%** |
| F3 | Formal proof | TLA+, Z3 | **100%** |

Quote: "The ceiling matters most: no amount of evidence can push reliability above what the formality level permits... This prevents informal consensus from masquerading as empirical certainty" (§2.1).

**Q2 — F0-F3 vs L0/L1/L2 — ORTHOGONAL, multiplicatively bounded.**

Gilda L-layers (ADI — Abduction-Deduction-Induction cycle, §2.4):
- **L0 Conjecture:** unverified hypothesis. Cap: **35%**
- **L1 Substantiated:** logically verified claim. Cap: **75%**
- **L2 Corroborated:** empirically validated claim. Cap: **100%**

**Combination rule (§2.1):** "When both layer and formality ceilings apply, R_eff is bounded by the minimum of both: an F0 claim at L1 is capped at min(0.70, 0.75) = 0.70".

**Orthogonality:** F measures *rigor of expression*; L measures *stage in verification cycle*. They are independent axes combined by `min()`.

**Critical divergence from plan:** The plan's L0/L1/L2 naming is the SAME as Gilda's L-layers, but the plan's naming convention per the task statement ("L0 = external priors, L1 = object claim, L2 = meta") is **DIFFERENT from Gilda's**. Gilda's L-layers are NOT about external-vs-object-vs-meta levels; they are about ADI verification stage (conjecture/substantiated/corroborated). **These are NOT the same semantic axis.** The plan's "meta-claim level" and Gilda's "L-layer" share letter names but mean different things. The plan should either (a) rename its levels to avoid collision, or (b) adopt Gilda's L-layers explicitly and map its own meta-claim concept onto F-levels instead.

**Q3 — Scope-based evidence transfer penalty (§2.1, Table 2):**

**Formula:** `R_adj = max(0, R(e) - penalty)`

**Congruence Levels (CL):**
| Level | Name | Example | Penalty |
|-------|------|---------|---------|
| CL3 | Same context | internal test on target HW | **0%** (none) |
| CL2 | Similar context | same arch, different scale | **10%** |
| CL1 | Different context | external benchmark | **40%** |
| CL0 | No context match | unrelated domain | **90%** |

**Q4 — Conservative aggregation invariants — Gamma Invariant Quintet (§2.2):**

Five invariants any valid aggregation operator Γ must satisfy to prevent "trust inflation":
1. **IDEM (Identity):** `Γ([x]) = x` — single evidence speaks for itself
2. **COMM (Commutativity):** `Γ([a,b]) = Γ([b,a])` — order irrelevant
3. **LOC (Locality):** changing E does not affect holons with no dependency on E
4. **WLNK (Weakest Link Upper Bound):** `Γ(S) ≤ min(S)` — no aggregation can exceed weakest link
5. **MONO (Monotonicity):** `a ≤ a'` implies `Γ([a,b]) ≤ Γ([a',b])` — improvement never worsens assurance

Aggregation target: **serial dependency structures (argument chains).** The WLNK invariant is the strong anti-inflation constraint.

**Q5 — Data schema (Appendix B, verbatim table names):**

Proposed DRR (Design Rationale Record) schema tables:
- `holons` (knowledge units)
- `evidence` (with `valid_until` timestamps)
- `relations` (serial/parallel dependencies)
- `characteristics` (quantitative properties)
- `waivers` (documented risk acceptances)

§2.4: DRR is "architectural decision record augmented with evidence validity windows, dependency chains, and assurance scores."

**Q6 — Temporal decay mechanism (§2.5 verbatim formula):**

```
R_eff(e, t) = { R(e)  if t ≤ valid_until(e)
              { 0.1   otherwise
```

**Critical insight: uncertainty floor at 0.1.** §2.5: "Expired evidence moves to 0.1 regardless of its original score, representing epistemic uncertainty rather than low confidence... This distinguishes epistemic decay from simple TTL caching" and "An expired falsification (R = 0.05) becomes 'we no longer know' (R = 0.1), not 'the falsification is slightly more reliable.'"

The floor 0.1 is **higher than low-confidence evidence** to mark "unknown" state distinctly.

**Q7 — Ten verbatim citable quotes:**
1. "Formality (F) determines the rigor of expression... F caps the maximum achievable R." — §2.1
2. "Scope constrains evidence transfer... FPF formalizes this through Congruence Levels (CL)." — §2.1
3. "These invariants prevent trust inflation—the failure mode where an agent hallucinates higher confidence by aggregating massive amounts of low-quality evidence." — §2.2
4. "Assurance equals the weakest supporting evidence. When a decision depends on multiple pieces of evidence, the effective reliability equals the weakest link." — §2.3
5. "Evidence either has a validity window or it does not count toward assurance." — §2.5
6. "An expired falsification (R = 0.05) becomes 'we no longer know' (R = 0.1), not 'the falsification is slightly more reliable.'" — §2.5
7. "The entity that finalizes a decision must be external to the generation loop... This prevents a failure mode where an autonomous agent bootstraps confidence in its own recommendations." — §2.4 (the "Transformer Mandate")
8. "20–25% of architectural decisions had stale evidence within two months, validating the need for temporal accountability." — Abstract
9. "Abduction generates conjectures (L0), Deduction verifies logical consistency (L1), and Induction validates empirically (L2)." — Figure 3
10. "Integrate decay checks into CI/CD so benchmarks auto-refresh on dependency updates." — §6

**Q8 — Paper type + implementation status:** Primarily **position paper** BUT with:
- **Reference implementation** (anonymized for review). §1: "A reference implementation (anonymized for review) is an existence proof, not the contribution itself."
- **Retrospective audit** of 62 ADRs across 2 internal projects — §4
- **Property-based verification** of framework logic — §4
- Empirical claim: 20-25% of ADRs had stale evidence within 2 months (Abstract)

**Q9 — Epistemic audit trail concept:** The **Design Rationale Record (DRR)** is the proposed audit substrate. §2.4: "evidence validity windows, dependency chains, and assurance scores." §1, §3.2: "durable audit trails that survive beyond a single session" and "dependency-aware invalidation."

Maps to claim-level verification: DRR tracks decisions + evidence with validity windows + dependency chains. A VerificationEvent could be a primitive feeding DRR records.

**Q10 — Formality direction (explicit):** **F3 = HIGHEST** (Cap 100%, formal proof). **F0 = LOWEST** (Cap 70%, informal). Table 1 confirms. Direction is counter to intuition that "0 = best" — here 0 = least formal, 3 = most formal. Plan authors should double-check they're using the same direction.

**Recommendation (structural, not editorial):** The plan's Component 5 (meta-claim level rule) should reference Gilda's F0-F3 levels directly for naming collision avoidance. Concretely:
- Gilda's **L0-L2** are about ADI verification stage (Abduction/Deduction/Induction)
- Plan's current "L0/L1/L2 meta-claim levels" per task spec have DIFFERENT semantics (external priors / object claim / meta)
- Name collision is severe — reading either document out of context loses the distinction
- Suggested mapping: plan's L0/L1/L2 → rename to e.g., "scope levels" or "claim-layer" (SL0/SL1/SL2 or CL0/CL1/CL2 — though CL collides with Gilda's Congruence Levels too)
- Or: adopt Gilda's L-layers as a new (orthogonal) axis in the plan, keeping plan's meta-claim as a separate axis
- Also: Gilda's CL0-CL3 scope penalties (0%, 10%, 40%, 90%) could populate the plan's evidence-transfer mechanics directly — the numbers are ready-to-adopt

**Confidence:** high — critical paper read carefully, full body extracted.

---

## Papers that failed to fetch

**None.** All 10 papers fetched full PDF successfully after at most one retry.

Four papers (2604.03141, 2603.16544, 2602.10380, 2602.23193) failed on initial `/abs/` URLs and succeeded on `/pdf/` URLs after one retry. For future sweeps: **default to `/pdf/` URLs for arXiv fetches** — the abs-URL redirect chain is flaky via Sci-Hub backend.

No paper required S2 abstract-only fallback. No paper required OpenAlex resolution. Full-text coverage: 10/10.

---

## Summary for coordinator (mechanical, not editorial)

- **Tier 1 (must-read full text):** Papers 1-4 all extracted full text. Questions answered with verbatim quotes.
- **Tier 2 (skim):** Papers 5-9 all extracted full text (stronger coverage than required).
- **Critical paper (10 — Gilda & Gilda):** Full body extracted. F0-F3 definitions verbatim, CL0-CL3 penalties verbatim, Gamma Invariant Quintet enumerated, uncertainty floor formula extracted, L-layer direction confirmed.
- **Schema compatibility notes are embedded in each Tier 1 brief** (Paper 1, 2, 4, 8) — synthesis/decision is deferred to the plan author.
- **Naming-collision warning for Paper 10** flagged as structural, not a recommendation — plan author's call.
