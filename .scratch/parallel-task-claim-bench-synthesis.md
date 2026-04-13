# parallel_task synthesis — claim_bench 2026 literature audit

**Source:** `mcp-parallel-parallel_task-1775948892585.txt` (172 KB, 1,681 lines, 84 Confidence/Reasoning blocks)

## Structural caveat up front

The report is **NOT structured by the 12 components**. It is a flat stream of 84 blocks of the form `Confidence: [high|medium] / Reasoning: ... / papers: ...`, each scoring a "fine-grained field value" rather than producing a per-component verdict. There is **no explicit per-component summary table, no overall recommendation section, and no pause/revise verdict** anywhere in the file. The report reads as a dump of evidence gathered per query shard, not a synthesis. The explicit verdict labels "NOTHING NEW / MINOR UPDATE / MATERIAL" appear only 3 times in the entire file:

1. Line 113: "advocates a **MINOR UPDATE** to the AutoVerifier-style six-layer verification pipeline" (Component 8 / AutoVerifier)
2. Line 824: "The field value **MINOR UPDATE** signals a modest evolution rather than a wholesale redesign of the evaluation-card concept" (Component 10 / evaluation cards)
3. Line 1067: "The field value **MATERIAL** is most strongly supported by the excerpt that describes an evidence ledger with a unique assertion identifier, a cryptographic watermark, partitioned storage, credential methods, and a 90-day expiry, collectively forming an immutable audit trail" (Component 1 / event ledger, citing AI Trust OS / arXiv:2604.04749)

Every other verdict below is my **inferred** mapping based on which fine-grained field values cluster onto which of the 12 components. This inference is NOT a verdict from the report — it is my best reconstruction. Where a component has no clear evidence block, I flag it as a **coverage gap** below.

## Per-Component Verdicts (inferred from clustered blocks)

### 1. Append-only JSONL event ledger (content-hash event_id)
**Inferred verdict:** MATERIAL (explicitly labeled as such at line 1067). Multiple blocks (lines 3-69, 195-232, 513-533, 1032-1051, 1067-1085, 1199-1220, 1243-1261, 1403-1423, 1514-1535, 1551-1572, 1639-1659) repeatedly surface the same 4 pieces of evidence. **Quote (line 1067):** *"The field value MATERIAL is most strongly supported by the excerpt that describes an evidence ledger with a unique assertion identifier, a cryptographic watermark, partitioned storage, credential methods, and a 90-day expiry, collectively forming an immutable audit trail suitable for external review. This directly aligns with evaluating the ledger component for material improvements in immutability, verifiability, and external-auditor readiness."*

Candidate papers:
- **arXiv:2604.04749** "AI Trust OS — A Continuous Governance Framework for Autonomous AI Observability and Zero-Trust Compliance in Enterprise Environments" (claimed "5 days ago" as of report date). *"Each assertion was persisted to the evidence ledger with a unique assertion identifier, SHA-256 watermark, workspace partition key, credential method, and a 90-day expiry timestamp, forming an immutab[le]..."* TL;DR: Telemetry-first governance framework with expiring, signed assertions. Why it matters: reframes event ledger from passive log to governance-active control plane with expiry semantics.
- **arXiv:2603.28988** "Attesting LLM Pipelines: Enforcing Verifiable Training and Release Claims" — *"Claims are issued as in-toto attestation predicates, signed via Sigstore and bound to the artifact..."* TL;DR: in-toto/Sigstore for LLM-pipeline claim attestation. Why it matters: suggests replacing raw JSONL with signed attestations.
- **draft-cowles-volt-00 (IETF)** "Verifiable Operations Ledger and Trace (VOLT) Protocol" — *"the sequence of events linked by prev_hash references, forming an append-only integrity chain. Each event's hash covers the event content, and each event's prev_hash points to the hash..."* TL;DR: IETF draft for content-addressed append-only ledger. Why it matters: formalizes prev-hash chaining over bare content-hash event_id.
- **arXiv:2601.22963** "Epoch-Resolved Arbitration for Duelling Admins in Group..." — separates finalised vs. unfinalised events. Why it matters: finality boundary for concurrent ledgers.
- **arXiv:2603.27202** "Sal: Multi-modal Verification of Replicated Data Types" (Lean/Dijkstra Monads). Why it matters: verified ledger data types.

### 2. ClaimRecord with stable_id + content_version_hash
**Inferred verdict:** MINOR (several medium-confidence blocks 283-305, 306-323, 1156-1173). The evidence is mostly "CIDs exist; PROV-K exists" not "newer work replaces your design." **Quote (line 307):** *"The notion of upgrading content_version_hash to a Content Identifier (CID) is directly supported by materials formalizing content-addressed identifiers. These sources describe CID concepts, the inclusion of content hashes with codec and format metadata, and the idea that CIDs enable cryptographic verifiability and global uniqueness. This is precisely the kind of self-describing, hash-based identifier that decouples identity from storage location and encodes the hash algorithm and data format..."*

Candidate:
- **IPFS CID docs** (not an arXiv paper). Use CIDs instead of raw SHA hashes for self-describing hash+codec encoding.
- **arXiv:2602.03417** "FactNet: A Billion-Scale Knowledge Graph for Multilingual..." — claimed to support stable-id separation via span-level evidence grounding.
- **arXiv:2408.03866** "A semantic approach to mapping the Provenance Ontology to Basic Formal Ontology" (pre-2026, FAIR/PROV-O alignment).

### 3. Verifier + DecisionGate typing.Protocol
**Inferred verdict:** MINOR (blocks around lines 346-368, 761-775, 889-905, 941-970). Evidence supports **enriching** the Protocol signature but nothing replaces the pluggable pattern. **Quote (line 347):** *"The field value asserts that by early 2026 there were concrete frameworks that materially extend the capabilities of a simple, protocol-based pluggable verifier. The most directly relevant lines describe a six-layer verifier framework where claims are decomposed into structured triples..."*

Candidates:
- **arXiv:2604.02617** "AutoVerifier: An Agentic Automated Verification Framework Using LLMs" (dated Apr 3, 2026). Six-layer pipeline, SPO triple decomposition. Why it matters: extends simple Verifier contract to layered multi-pass verification.
- **arXiv:2502.20379** "Multi-Agent Verification: Scaling Test-Time Compute with Multiple Verifiers" — Aspect Verifiers (AVs) off-the-shelf LLMs verifying specific aspects. Why it matters: richer routing/aggregation pattern.
- **arXiv:2604.07725** "Squeeze Evolve: Unified Multi-Model Orchestration for Verifier-Free Evolution"
- **arXiv:2604.01652** "ThinknCheck: Grounded Claim Verification with Compact, Reasoning-Driven, and Interpretable Models" — *"On LLMAggreFact, ThinknCheck attains 78.1 balanced accuracy (BAcc), surpassing MiniCheck-7B (77.4) with 7x fewer parameters"*

### 4. TTL per-modality integer-days with DECAYED events
**Inferred verdict:** MINOR/MATERIAL-leaning (many blocks 99-111, 398-410, 677-702, 1355-1368, 1425-1428, 1595-1605, 1660-1664). Oblivion is the recurring candidate. The report strongly suggests replacing integer-day TTLs with continuous decay. **Quote (line 691):** *"The most directly relevant excerpt describes a memory-control framework that replaces discrete TTL semantics with a continuous, exponential retention score, modulated by usage and uncertainty gating. This directly provides a complete alternative to a discrete DECAYED event system by offering a formal retention function and retrieval gating, which could be applied to per-claim retention in the event ledger and mitigate stale entry retention through principled forgetting."*

Candidates:
- **arXiv:2604.00131** "Oblivion: Self-Adaptive Agentic Memory Control through Decay-Driven Activation" (v1, 31 Mar 2026). *"Oblivion, a memory control framework that casts forgetting as decay-driven reductions in accessibility, not explicit deletion. The read path decides when to consult memory, based on agent uncertainty and memory buffer sufficiency..."* Why it matters: directly proposes replacing binary DECAYED with continuous retention score + uncertainty-gated retrieval. Introduces "Recognizer/Activator" pair.
- **arXiv:2601.18642** "FadeMem: Biologically-Inspired Forgetting for Efficient Agent Memory" — *"adaptive exponential decay functions modulated by semantic relevance, access frequency"*
- **arXiv:2603.14517** "Learning to Forget: Sleep-Inspired Memory Consolidation for Resolving Proactive Interference in LLMs" (15 Mar 2026)

### 5. Meta-claim L0/L1/L2 level rule
**Inferred verdict:** MATERIAL-leaning (blocks 411-497, 1262-1272, 1287-1306, 1380-1401, 1665-1681). Multiple blocks push for replacing flat L0/L1/L2 with graph/DAG representation. **Quote (line 412):** *"The target field value calls out a need to replace or augment a simple hierarchical (L0/L1/L2) claim structure with a richer, graph-based model of evidence. Excerpts describing evidence graphs and structured evidence nodes provide concrete grounding for this shift: claims decomposed into verifiable units tied to explicit evidence lines and provenance metadata..."* And (line 1381): *"The field value argues for abandoning a simple hierarchical L0/L1/L2 structure in favor of a directed-graph representation of claims and evidence, where edges encode explicit relationships such as SUPPORTS, CONTRADICTS, and other relations."*

Candidates:
- **arXiv:2603.28325** "Building evidence-based knowledge graphs from full-text literature for disease-specific biomedical reasoning" (v2). "EvidenceNet"-style structured evidence node with experimental context, entities, quantitative results, source text, confidence.
- **PROV-K Ontology** (Zenodo 15187372) — captures reliability and trust relationships between agents and assertions.
- **SEPIO** (Monarch Initiative) — Scientific Evidence and Provenance Information Ontology.
- **arXiv:2601.01609** "Structured Decomposition for LLM Reasoning" (Sadowski 2026).
- **arXiv:2604.04344** "Domain-Contextualized Inference" — CDC framework 4-tuple <concept, relation@domain, concept'>.

### 6. inspect_ai harness integration
**Inferred verdict:** NOTHING NEW / baseline-holds. **Quote (line 71, high confidence):** *"The field value asserts that, as of early 2026, Inspect AI remains the primary neutral substrate for high-assurance, sandboxed evaluation, with other harnesses offering complementary strengths rather than replacing it."* And (line 649): *"no single harness has displaced inspect_ai as the primary neutral substrate for high-assurance, sandboxed evaluation, and noting complementary strengths of other harnesses (e.g., DeepEval, lm-evaluation-harness, and promptfoo)."*

Notable context:
- **OpenAI acquired Promptfoo (March 9, 2026)** — cited via OpenAI blog + TechCrunch. Not an academic paper but a market move worth noting.
- **arXiv:2405.14782** "lm-evaluation-harness" (Biderman 2024, cited 118x) — pre-frontier baseline.
- **DeepEval** (confident-ai GitHub) — complementary, Pytest-like.

### 7. FIRE-Bench atomic-claim P/R/F1
**Inferred verdict:** MATERIAL-leaning (blocks 233-265, 730-759, 791-811, 812-822, 1189-1198, 1273-1285, 1308-1328, 1344-1354, 1369-1379, 1429-1454, 1481-1485, 1501-1512). The strongest and most repeatedly cited finding. **Quote (line 731):** *"The field value claims that the traditional FIRE-Bench atomic-claim scoring (precision, recall, F1) is superseded by more advanced 2026 frameworks. The most direct support comes from AtomEval, which introduces a validity-aware scoring approach (VASR) and decomposes claims into structured SROM atoms to detect subtle factual corruption that surface metrics miss. This demonstrates a move away from simple aggregate metrics toward atom-level validity checks."* And (line 1308): *"The field value describes a framework named AtomEval that (a) decomposes complex claims into structured Subject-Relation-Object-Modifier (SROM) atoms, and (b) uses a novel Atomic Validity Scoring (VASR) metric combining a hard structural gate with a soft semantic degradation score to measure factual corruption."*

Candidates:
- **arXiv:2604.07967** "AtomEval: Atomic Evaluation of Adversarial Claims in Fact Verification" (claimed "2 days ago" as of report date ≈ Apr 9, 2026). SROM atoms + VASR / AVS scoring.
- **arXiv:2603.05912** "DeepFact: Co-Evolving Benchmarks and Agents for Deep Research Factuality" — *"We propose Evolving Benchmarking via Audit-then-Score (AtS), where benchmark labels and rationales are explicitly revisable: when a verifier disagrees with the current benchmark, it must submit eviden[ce]... across four AtS rounds, expert micro-gold accuracy rises to 90.9%"*. Why it matters: replaces static FIRE-Bench labels with audit-then-score.
- **arXiv:2602.07621** "SciClaimEval: Cross-modal Claim Verification in Scientific Papers" — 1,664 annotated samples from 180 papers across ML/NLP/medicine.
- **FIRE-Bench** (maitrix-org GitHub) — existing baseline, "research-problem decomposition".
- **arXiv:2604.01306** "M2-Verify: A Large-Scale Multidomain Benchmark for Checking Multimodal Claim Consistency" — 16 scientific domains, 469K+ instances.

### 8. AutoVerifier 6-layer pattern
**Inferred verdict:** MINOR UPDATE (explicitly labeled at line 113). **Quote (line 113):** *"The core fine-grained field value advocates a MINOR UPDATE to the AutoVerifier-style six-layer verification pipeline, specifically recommending the integration of formal, verifiable substructures rather than changing the six-layer blueprint."* And (line 603): *"refine or augment it without wholesale replacement."*

Candidates:
- **arXiv:2604.02617** "AutoVerifier: An Agentic Automated Verification Framework" (03 Apr 2026). Six-layer pipeline; SPO triple extraction into knowledge graphs. Claims to have "dismantled a contested runtime advantage claim".
- **arXiv:2602.07559** "VERIFY-RL: Verifiable Recursive Decomposition for RL in Mathematical Reasoning" (Feb 7, 2026) — chain/product/sum rule decomposition operators with preservation proofs.
- **arXiv:2604.07907** "Capture-Quiet Decomposition for Chess Endgame Verification" — structural criterion anchored to externally verified sub-models, avoiding the fixpoint trap. (Chess-specific but cited as structurally analogous.)
- **arXiv:2603.25450** "Cross-Model Disagreement as a Label-Free Correctness Signal"

### 9. FINCH-ZK cross-family routing
**Inferred verdict:** MINOR (blocks 971-987, 1174-1187). Medium confidence; the report basically says Finch-Zk still exists and is relevant. **Quote (line 972):** *"The most relevant passages directly address Finch-Zk and related cross-model consistency tooling, which are central to the question of whether 2026 work fundamentally reshapes or merely augments authority-class-weighted routing. Finch-Zk is presented as a framework for fine-grained cross-model consistency in hallucination management..."*

Candidates:
- **arXiv:2508.14314** "Zero-knowledge LLM hallucination detection and mitigation through fine-grained cross-model consistency" (Finch-Zk, v2). Pre-existing paper, not new work.
- **arXiv:2603.25450** "Cross-Model Disagreement as a Label-Free Correctness Signal" (Mar 26, 2026) — *"Cross-Model Perplexity (CMP), which measures the verifying model's surprise at the generating model's answer tokens, and Cross-Model Entropy (CME)..."* Why it matters: label-free signal for routing escalation without retraining.
- **arXiv:2602.04448** "RASA: Routing-Aware Safety Alignment for Mixture-of-Experts Models" (v2)
- **arXiv:2602.09001** "DirMoE: Dirichlet-routed Mixture of Experts" — sparse interpretable routing on simplex.

### 10. Phase 4 independence + adequacy cards
**Inferred verdict:** MINOR UPDATE (explicitly labeled at line 824). **Quote (line 824):** *"The field value MINOR UPDATE signals a modest evolution rather than a wholesale redesign of the evaluation-card concept. Excerpts describing provenance and evidence models (for example, SEPIO and PROV-K) illuminate how evidence provenance and trust relationships can be described and linked to claims, which is directly relevant to how evaluation cards should represent evidence lines and their credibility."*

Candidates:
- **SEPIO** (Monarch Initiative) — evidence/provenance ontology.
- **PROV-K Ontology** (Zenodo 15187372) — extends PROV-O for multi-sourced assertions.
- **GRADE approach** (gradeworkinggroup.org) — Evidence-to-Decision framework, non-academic but established.
- **Provenance-driven nanopublications** (Springer IJDL 2025).

### 11. Authority class + evidence modality taxonomies
**Inferred verdict:** MATERIAL-leaning (blocks 160-193, 370-396, 1018-1031, 1104-1131, 1230-1240). Strong push to replace ad-hoc taxonomy strings with formal ontologies (SEPIO, PROV-K). **Quote (line 371):** *"The finegrained field concerns adopting interoperable, machine-actionable authority/evidence taxonomies to replace simple taxonomy strings. The excerpts point to SEPIO as a core information model for modeling claims, evidence lines, methods, and agents in a domain-agnostic way, enabling profile customization via LinkML. This directly supports a redesign of how evidence and provenance are represented in claim_bench beyond ad-hoc taxonomies."*

Candidates:
- **SEPIO-ontology** (Monarch Initiative GitHub) — *"an OWL ontology developed to support rich, computable representations of the evidence and provenance behind scientific claims"*
- **PROV-K Ontology**
- **FactNet** arXiv:2602.03417 — billion-scale KG with span-level evidence grounding.
- **arXiv:2603.00267** "Multi-Sourced, Multi-Agent Evidence Retrieval for Fact-Checking" — POMDP model with expand-and-prune KG retrieval.
- **arXiv:2603.10742** "A Grammar of Machine Learning Workflows Rejecting Data Leakage at Call Time" — typed primitives + DAG with hard constraints to make leakage structurally unrepresentable. Cited as a design analogue.

### 12. Cross-project adapter pattern (core + thin adapters)
**Inferred verdict:** MINOR (blocks 499-512, 1004-1017, 1052-1065). **Quote (line 500):** *"The Domain-Contextualized Inference (CDC) excerpts describe a five-layer inference framework with explicit domain consideration and a minimal, stable API surface (Query, Extend, Bridge). This directly supports the fine-grained field value by showing how to elevate domain as a first-class input to the inference process, enabling domain-specific adapters to be plugged into the core stack. The references to a compact API surface indicate an opportunity to design a core that remains lightweight wh[ile enabling richer adapters]..."*

Candidates:
- **arXiv:2604.04344** "Domain-Contextualized Inference: A Computable Graph Architecture for Explicit-Domain Reasoning" — CDC framework (Li & Wang, 2026), five-layer architecture (Domain Lattice, Fiber Concept Graphs, Reindexing Functors, Cross-Fiber Bridges, Meta-Layer). Why it matters: formal analogue for core + domain adapters with domain as a "modal world constraint".
- **arXiv:2603.00267** "Multi-Sourced, Multi-Agent Evidence Retrieval" — modular retrieval policy refinement without modifying core.
- **arXiv:2508.05097** "MultiCheck: Strengthening Web Trust with Unified Multimodal Fact Verification" — modular (text/image/fusion/classification) architecture.

## MATERIAL findings (verbatim quotes)

The report only explicitly labels ONE component as MATERIAL — Component 1 (event ledger), at line 1067. Full verbatim:

> *"Reasoning: The field value MATERIAL is most strongly supported by the excerpt that describes an evidence ledger with a unique assertion identifier, a cryptographic watermark, partitioned storage, credential methods, and a 90-day expiry, collectively forming an immutable audit trail suitable for external review. This directly aligns with evaluating the ledger component for material improvements in immutability, verifiability, and external-auditor readiness. An additional excerpt discusses binding claims to [artifacts via in-toto/Sigstore]..."*

Supporting argument (line 1033): *"a simple hash-chained JSONL log is insufficient for a modern, tamper-evident, governance-driven evidence ledger and highlights three directions: (a) improving cryptographic security and structure of the event payload, evolving from generic JSON to non-repudiable attestations; (b) implementing automated governance features, such as expiring assertions to maintain evidence freshness and treating the ledger as an active control-plane component; and (c) considering [CRDT-based causally-ordered event stores]..."*

Further argument (line 1243): *"(a) a structured, expiry-enabled evidence ledger and immutable audit trail for governance and automation; (b) cryptographically signed attestations binding claims to exact artifacts for zero-trust verification; and (c) distributed, causally-ordered event stores (CRDT-based) enabling concurrent event generation with finality mechanisms."*

Other strong-but-unlabeled revisions (my reading, not the report's explicit verdict):

**Component 4 (TTL/DECAY), line 691:** *"The most directly relevant excerpt describes a memory-control framework that replaces discrete TTL semantics with a continuous, exponential retention score, modulated by usage and uncertainty gating. This directly provides a complete alternative to a discrete DECAYED event system by offering a formal retention function and retrieval gating, which could be applied to per-claim retention in the event ledger and mitigate stale entry retention through principled forgetting."*

**Component 7 (FIRE-Bench scoring), line 731:** *"The field value claims that the traditional FIRE-Bench atomic-claim scoring (precision, recall, F1) is superseded by more advanced 2026 frameworks. The most direct support comes from AtomEval, which introduces a validity-aware scoring approach (VASR)... This demonstrates a move away from simple aggregate metrics toward atom-level validity checks."*

**Component 5 (L0/L1/L2 meta-claim), line 1381:** *"The field value argues for abandoning a simple hierarchical L0/L1/L2 structure in favor of a directed-graph representation of claims and evidence, where edges encode explicit relationships such as SUPPORTS, CONTRADICTS, and other relations."*

## Overall recommendation

**There is no overall recommendation in the file.** I searched for "overall", "recommend", "pause", "should.*paused", "revise". The only "recommend" hits are boilerplate GRADE text ("typically rely on multiple streams of evidence to formulate recommendations") and individual block reasoning phrases, none of which constitute a summary verdict on whether to pause/revise the claim_bench plan. The report is an evidence dump, not a synthesis. **The caller must produce their own pause/revise decision** based on the per-component signals above.

## Hallucination red flags

I did NOT verify any of these externally — just flagging plausibility based on the file content:

1. **Every 2604.xxxxx arXiv ID claims to be from April 2026** (the month of the research dispatch). The report says things like "2 days ago" (AtomEval), "Apr 3, 2026" (AutoVerifier), "5 days ago" (AI Trust OS), "Apr 2, 2026" (ThinknCheck). This is internally consistent with a report run on or around 2026-04-11 — but it means the entire MATERIAL-leaning signal rests on papers dated within ~2 weeks of the dispatch. **I have moderate confidence in these IDs but they should be the FIRST thing to verify externally** since brand-new papers are the highest-entropy hallucination target and confirmation via an independent search would be cheap.

2. **arXiv:2604.04749 "AI Trust OS"** — Described as a "telemetry-first AI governance framework" for SOC 2, ISO 27001, ISO 42001, EU AI Act, HIPAA. This is an unusual blend of enterprise compliance and LLM research for an arXiv paper; the framing reads more like a vendor whitepaper than a typical arXiv submission. **Flag for verification.**

3. **arXiv:2604.07967 "AtomEval"** — The naming convention varies between "VASR" (Validity-Aware Scoring) and "AVS" (Atomic Validity Scoring) in different excerpts (compare line 30 "Atomic Validity Scoring (VASR)" vs line 1198 "Scoring (AVS)"). This inconsistency could indicate paraphrasing drift OR could reflect that the paper uses both terms. **Flag for direct read.**

4. **arXiv:2604.02617 "AutoVerifier"** — The report quotes *"The system effectively dismantled a contested 'runtime advantage' claim"* as a case study. This is specific enough that it should be verifiable in the abstract. Recurs in ~15 blocks, suggesting it is central to the report's evidence — worth reading directly before citing.

5. **arXiv:2604.00131 "Oblivion"** — "v1 [cs.CL] 31 Mar 2026". Submission date and content are internally consistent. Introduces "Recognizer/Activator" terminology — distinctive enough to verify.

6. **arXiv:2601.18642 "FadeMem"** — January 2026. Sub-year-field "18642" is unusually high for January (arXiv monthly counts rarely exceed ~10K for cs.). **Possibly suspicious numbering — flag.**

7. **arXiv:2601.22963 "Epoch-Resolved Arbitration for Duelling Admins in Group..."** — Even higher sub-year number (22963). Title is also an unusual topic for cs.DC ("duelling admins"). **Plausibly fabricated — flag prominently.**

8. **arXiv:2604.04344 "Domain-Contextualized Inference"** — CDC framework by "Li & Wang, 2026". Specific framework name and author pair. Worth a quick Google Scholar check.

9. **IETF draft "draft-cowles-volt-00"** — VOLT Protocol. I could not verify author name "cowles" or the draft existence, but IETF drafts have loose namespacing so I would not reject on prima facie grounds.

10. **"AtomEval" vs "AtomEval:Bench" vs huggingface "CLAIM-BENCH"** — The huggingface link mentions a separately-named "CLAIM-BENCH" paper that is conflated with AtomEval in several blocks. **Possible conflation, not hallucination — flag for careful disambiguation.**

Importantly: a large fraction of the 2604.xxxxx IDs may be real — but the report never provides author names (except "Li & Wang" and "Vahidi" and "Sadowski"), dates are relative ("2 days ago", "5 days ago"), and the same 4-5 papers recur across 80+ blocks. This is a characteristic of a thin evidence base wrapped in heavy re-quoting. **Re-verify with an independent search for at least the top 3 MATERIAL-coded papers (2604.04749 AI Trust OS, 2604.07967 AtomEval, 2604.02617 AutoVerifier, 2604.00131 Oblivion) before updating the plan.**

## Coverage gaps

Components where the report is thin, evasive, or where I could not cleanly map a block:

- **Component 2 (ClaimRecord stable_id + content_version_hash):** The report repeatedly defaults to the IPFS CID concept page (not an academic paper) and PROV-K (also largely non-academic). No 2026 paper directly addresses content-version-hash semantics. **Re-search with keywords: "content addressable claim identifier", "CRDT claim merging", "Merkle claim versioning".**
- **Component 3 (Verifier + DecisionGate typing.Protocol):** The report conflates this with Component 8 (AutoVerifier 6-layer). It never addresses Python Protocol / duck typing / interface design specifically — the evidence is about verifier richness, not interface design. **Re-search with keywords: "pluggable verifier interface", "typing protocol LLM eval", "verifier composition API".**
- **Component 6 (inspect_ai integration):** The "NOTHING NEW" signal is credibly argued but the report cites only the GitHub README + OpenAI/Promptfoo acquisition news. No 2026 academic paper is cited. The caller may want to verify that inspect_ai is still the default substrate by checking recent UKAISI publications.
- **Component 9 (FINCH-ZK cross-family routing):** The cited Finch-Zk paper (arXiv:2508.14314) is from August 2025, pre-dating the research window. The newer candidates (Cross-Model Disagreement 2603.25450, RASA, DirMoE) are related but not replacements. **The report does not credibly establish a 2026 replacement for FINCH-ZK — this is a weak answer dressed in high confidence. Re-search with keywords: "zero-knowledge hallucination detection 2026", "cross-family model routing", "authority-weighted verifier routing".**
- **Component 10 (Phase 4 independence + adequacy cards):** Cited only SEPIO, PROV-K, GRADE (established ontologies, not new work) — no 2026 paper directly addresses "independence" or "adequacy cards" as concepts. Partial coverage.
- **Component 12 (cross-project adapter pattern):** Only one 2026 paper (Domain-Contextualized Inference 2604.04344) is even tangentially relevant, and its "domain as modal world" framing is not directly about Python-package adapters. **Re-search with keywords: "core-adapter pattern verification library", "shared claim verification core", "multi-domain LLM evaluation library".**

General coverage observations:

1. **Roughly 6 papers dominate the citations** (2604.04749, 2604.07967, 2604.02617, 2604.00131, 2603.05912, 2603.28325 + PROV-K + SEPIO). Everything else is supporting. A proper audit should read these 6 papers directly.
2. **No block discusses testing/CI integration** for the inspect_ai harness specifically.
3. **No block discusses Python type system evolution** (PEP 695, TypedDict extensions, Protocol refinements) relevant to DecisionGate.
4. **The report has NO discussion of existing claim-verification libraries** (MiniCheck is mentioned once as a baseline beaten by ThinknCheck, but Loki/OpenFactVerification is mentioned only once in passing at line 454-456). **Re-search keywords: "open-source claim verification Python package 2026", "fact-checking library LLMAggreFact".**
5. **The report conflates "what's new in 2026" with "what exists" repeatedly** — large portions argue for adopting ontologies (SEPIO, PROV-K) that predate 2026 entirely. If the audit's purpose is "is there new 2026 work that changes the plan", the repeated citation of 2025-era ontologies is an evasion dressed as evidence.

## File path
`/Users/alien/Projects/agent-infra/.scratch/parallel-task-claim-bench-synthesis.md`
