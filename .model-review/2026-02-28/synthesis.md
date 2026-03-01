## Cross-Model Review: Agent Skill Architecture
**Mode:** Review
**Date:** 2026-02-28
**Models:** Gemini 3.1 Pro, GPT-5.2
**Constitutional anchoring:** Yes (CONSTITUTION.md, GOALS.md)

---

### Verified Findings (adopt)

| Finding | Source | Verified How |
|---------|--------|-------------|
| ACH must be available to trade workflow, not locked in investigate | Gemini + GPT | CONSTITUTION.md P11: "Before any trade recommendation" — broader than fraud |
| Source-grading scope is project-wide (P3), not investigate-only | Gemini | P3: "every claim that enters entity files or analysis docs" |
| Change #7 (trade-thesis) is highest priority, not lowest | Gemini + GPT | GPT quantified: P9=10%, P11=35%, P12=5% coverage. Core mission gap. |
| Change #6 (trim Exa section) must be conditional on #5 (hook) | GPT | Logically valid: removing guidance before enforcement exists worsens behavior |
| Entity-management: add investment categories, don't delete bio | GPT | P8: "physiological signals where research-validated" |
| 51% violation rate doesn't prove instruction is useless — no counterfactual | GPT | Valid: instruction may reduce from 90%→51%, not 0%→51% |
| Prediction ledger is a missing constitutional artifact | GPT | P5 (Fast Feedback), P9 (Portfolio as Scorecard), GOALS.md (≥20 predictions/quarter) |
| Trade tickets need a linter/hook, not just a skill | GPT | "instructions alone = 0% reliable" applies to trade-thesis too |

### Where I (Claude) Was Wrong

| My Original Claim | Reality | Who Caught It |
|-------------------|---------|--------------|
| "Inline source-grading into investigate" | P3 mandates grading for ALL entity files and analysis, not just investigation. Inlining isolates epistemics to secondary mission. | Gemini |
| "Inline competing-hypotheses into investigate Phase 4" | ACH is constitutionally required for trade recommendations (P11), not just fraud leads. Burying it in investigate breaks the primary mission workflow. | Gemini + GPT |
| "Change #7 defer?" | This is the highest-impact change. P9/P11/P12 are the least-covered principles and most central to the generative principle. | Gemini + GPT |
| "Update entity-management: remove genes/drugs" | P8 explicitly values multi-domain signals including physiological. Add investment categories, keep bio as secondary. | GPT |
| "Trim researcher Exa section" as independent action | Must be conditional on Exa hook deployment. Standalone removal worsens behavior. | GPT |

### Gemini Errors (distrust)

| Claim | Why Wrong |
|-------|-----------|
| "Claude Code cannot natively spawn independent Gemini/GPT agents via Task tools" | Partially wrong. Task tool agents are Claude, but they can call llmx internally. The competing-hypotheses skill itself says "If multi-model dispatch isn't available, same-model agents still have value." Architecture works indirectly. |
| "Create a dedicated Python script for sequential Exa, removing direct API access" | Over-engineered. Would require an MCP server wrapper or tool replacement. A stateful PreToolUse hook (tracking calls via $PPID temp file) is simpler and doesn't break existing MCP architecture. |
| "Rename source-grading to epistemics-finance and expand" | Scope creep. The Admiralty system IS domain-agnostic — that's its strength. Adding SEC-specific source types is fine but doesn't justify a full skill rename and expansion. |
| "Rewrite epistemics for the Financial Domain" | P8 says "physiological signals where research-validated." Purging bio epistemics would violate this. The investment research domain's epistemics are already in the Constitution (P2-4, P7, P11). A financial-epistemics skill would largely duplicate constitutional text. |
| "Build a dataset-joiner orchestration skill" | Interesting idea but over-scoped. Entity resolution is ad-hoc and domain-specific. A skill template for DuckDB joins would be low-reuse. |
| Temperature override (0.3 → 1.0) | Gemini 3.1 Pro locks temperature server-side — expected. Noted in model-review skill already. |

### GPT Errors (distrust)

| Claim | Why Wrong |
|-------|-----------|
| "Coverage score P7 (Honest About Provenance) = 80%" | Likely overestimate. Dual provenance schema (Admiralty vs researcher tags) creates real ambiguity. Without enforcement hooks, actual compliance in outputs is probably lower. |
| "Effort: 12-30 hours for trade-thesis skill" | Likely underestimate for the full ticket system with linter + Kelly script. But reasonable for a minimal skill without architectural enforcement. |
| "Archived = possibly still accessible internally" | Incorrect for Claude Code skills. Archived skills in archive/ subdirectory are not symlinked and not loaded. The broken reference is real. |
| "Unify provenance into a single canonical claim object schema with renderers" | Over-engineered. Two schemas serve different contexts (investigation vs general research). Clarifying when each applies is simpler than building a unified data model. |

### Revised Priority List

Based on both reviews, constitutional alignment, and fact-checking:

1. **Build trade-thesis skill + ticket linter (was #7, now #1)**
   - Why: P9=10%, P11=35%, P12=5%. Largest constitutional gap. Primary mission enabler.
   - Scope: trade ticket template + required fields + pre-commit linter + Kelly sizing script
   - Testable: ≥95% of trade proposals include thesis/falsification/sizing/exits

2. **Unarchive competing-hypotheses as standalone (was #2, approach changed)**
   - Why: ACH is needed for BOTH trade theses (P11) and fraud investigation. Inlining into investigate would restrict it.
   - Change: Unarchive, keep standalone, make available to both investigate and trade-thesis workflows.

3. **Keep source-grading standalone (was #1, approach reversed)**
   - Why: P3 mandates grading for ALL entity files and analysis docs. Standalone keeps it universally available.
   - Change: Keep as-is. Add 3-line quick-reference in entity-management. Clarify researcher's "don't mix" language.

4. **Build prediction ledger (NEW — GPT recommendation)**
   - Why: P5 (Fast Feedback), P9 (Portfolio as Scorecard), GOALS.md (≥20 predictions/quarter, calibration curve).
   - Scope: predictions.csv schema + resolver job
   - Testable: ≥20 predictions/quarter with deadlines and resolution tracking

5. **Build Exa throttle hook (was #5, keep)**
   - Why: 51% violation rate. Sequential evidence incorporation is structurally important.
   - Change: Stateful PreToolUse hook tracking Exa calls per turn via $PPID. Do NOT trim researcher Exa section until hook proves effective.

6. **Entity-management: add investment categories, keep bio (was #4, approach changed)**
   - Change: Add companies/, people/, contracts/, filings/ as primary. Keep genes/, drugs/ as secondary (P8).

7. **Trim goals to drift-detection focus (was #3, keep as lowest priority)**
   - Lowest priority because disable-model-invocation means no context cost. Still worth doing for usability.

### Dropped Changes

- **#6 (Trim researcher Exa section):** Conditional on #5. Do not trim until hook proves effective (measure burst rate before/after).
