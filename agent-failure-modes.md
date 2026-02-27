# Agent Failure Modes & Universal Contracts

Extracted from `selve/docs/universal_contracts.md` and `selve/docs/AGENT_PROTOCOLS.md`.
Evaluated against intel project's epistemic principles (2026-02-27).

## Still Valid (Cross-Project)

### Contract 1: Multiple Expert Agreement
```
IF multiple experts would give different valid answers
THEN question/specification fails

TEST: Would 3 domain experts converge on same answer?
```
**Status:** VALID. This IS our falsifiability requirement. "If you cannot name a falsifying observation, you don't have a hypothesis — you have a belief." Same principle, different framing.

### Contract 2: Source + Method Attribution
```
IF claim depends on specific analysis/method
THEN must cite: source + method + context
```
**Status:** VALID. Subsumed by our provenance tagging system (`[SOURCE: url]`, `[DATA]`, `[INFERENCE]`, `[TRAINING-DATA]`, `[UNCONFIRMED]`). The selve version adds the "method" dimension — which method/encoder produced the result. We should keep this nuance.

### Contract 3: Hidden Assumption Detection
```
IF question embeds unstated assumptions
THEN make assumptions explicit
```
**Status:** VALID. Same as "predict data footprint BEFORE querying" and counterfactual generation. Making assumptions explicit before analysis prevents confirmation bias.

### Universal Failure Modes

| # | Failure Mode | Selve Framing | Intel Equivalent | Still Unique? |
|---|-------------|---------------|------------------|---------------|
| 1 | Non-deterministic evaluation | Multiple valid interpretations | "Name names" / falsifiability | No — same principle |
| 2 | Hidden dependencies | Unstated assumptions in specs | "Predict data footprint BEFORE querying" | No — same principle |
| 3 | Frame ambiguity | "perspective", "how" without method | Source grading (grade claims not datasets) | Partially — selve's "method attribution" adds value |
| 4 | Generic solutions | Common approaches when specific required | "Synthesis mode default" anti-pattern | Yes — this is the core agent failure |

### Regret Metric
```
regret = Σ(corrections_per_conversation)
```
**Status:** USEFUL but unmeasured. We don't track corrections across sessions. The concept is sound — every correction is a wasted generation + user time. The `260 immediate rejections × 30s = 130 minutes wasted` calculation from selve's ChatGPT data is real. We could instrument this via the Stop hook or compaction transcripts.

### Scaffolded Search (from Agent Protocols)
```
1. Run broad search (scaffolded)
2. Analyze the timeline (abandoned? burst of activity?)
3. Deep dive into specific items
4. Synthesize with context
```
**Status:** VALID. This IS our Phase 1 Ground Truth pattern. The timeline analysis angle ("did they stop in 2023?") adds value — detecting abandoned vs active interest before going deep.

## Superseded by Newer Principles

### ECE Calibration Contract
```
diagnostic_count >= 10 → confidence_threshold = 0.8
```
**Status:** DOMAIN-SPECIFIC. Only relevant to selve's learning system. Our calibration framework (Brier Skill Score, CRPS for continuous, N≈155 at 80% power) is more rigorous. Not cross-project useful.

### Query Rate Optimization
```
query_efficiency = tasks_completed / llm_calls
batch_size >= 5 when possible
```
**Status:** VALID PRINCIPLE but OUTDATED IMPLEMENTATION. The "don't call the LLM 5 times when you can batch" is still true. But our diminishing returns gate is a better formulation — it's about marginal information yield, not raw call count.

### ContractValidator Class
```python
class ContractValidator:
    def validate_output(self, question, answer): ...
```
**Status:** SPECULATIVE. Never implemented. The concept (automated contract checking) is sound but premature. Our approach (rules + hooks + Stop checklist) achieves the same goal with less engineering.

### Speculative Win Rate
```
win_rate = reused_content / (reused + generated)
```
**Status:** VALID for selve's content reuse. Not directly applicable to intel's research workflow. The principle (search before generating) maps to our Phase 1 Ground Truth.

## What's Uniquely Valuable

1. **Method attribution** — selve distinguishes "what was found" from "how it was found" (which encoder, which method). Our provenance tags track source but not method. Worth adding to `[DATA]` tags: `[DATA: query, method]`.

2. **Regret tracking** — quantifying wasted effort from corrections. We have the infrastructure (compaction transcripts, Stop hook) but don't measure it.

3. **Timeline analysis** — checking whether a topic was abandoned or is actively evolving before going deep. Prevents researching dead threads.

4. **"Vague truth > precise fiction"** — already in our anti-fabrication safeguards, but the selve formulation is more memorable and should be the canonical phrasing.

---

*Evaluated 2026-02-27. Source: `~/Projects/selve/docs/universal_contracts.md`, `~/Projects/selve/docs/AGENT_PROTOCOLS.md`.*
