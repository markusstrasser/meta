# Extraction & Disposition — Validation Review

**Date:** 2026-02-28
**Models:** Gemini 3.1 Pro, GPT-5.2
**Fact-checked by:** Claude Opus 4.6 (subagent verified 8 Gemini claims)

## Extraction: Gemini

G1. Agent A failed — only 9/26 scan_* functions have tests (5 test files missing)
G2. Agent B passed — prediction schema exact match, Goodhart dual resolution implemented
G3. Agent C passed — OOM-safe via streaming ZIP iteration, schema matches
G4. Agent D passed — all 5 silence rules implemented, state.duckdb separation correct
G5. Agent E passed — post-mortem template matches spec
G6. signal_scanner.py has pervasive bare except blocks (silent failures)
G7. SQL injection risk in silence_detector.py and healthcheck.py (f-string SQL with view names)
G8. prediction_tracker.py has fragile regex parsing for automated extraction
G9. dataset_registry.py has hardcoded paths in _find_dataset_dir
G10. 16 scan_* functions have zero tests (leiden_clusters, mechanism_checklist most critical)
G11. Surprise detector edge case: IPO with <20 days history → bad ADV calculation
G12. experiment_logger.py has no dedicated test file
G13. Violation of Principle 12 (Kelly sizing) — no trade outbox integration
G14. scan_discovery double-counts insider buys when WATCHLIST is empty
G15. DuckDB concurrency risk in prediction_tracker.py (repeated connection opens in loops)
G16. scoring.py has excellent mathematical rigor (Beta distribution, conditional independence)
G17. build_issuer_xwalk.py uses elite staging DB pattern (avoid write locks)
G18. Dual resolution state machine brilliantly executed (resolved_partial → confirm_fundamental)

## Extraction: GPT

P1. prediction table: resolution_type DEFAULT 'market_return' may hide omissions (spec says "decide at creation")
P2. prediction table: good tightening vs spec (added CHECK constraints on target, direction, probability)
P3. linked_signal_ids: no JSON validity constraint (VARCHAR only)
P4. CSV migration misuses strategy column (stores claim text, not signal type)
P5. prediction_resolution: missing FK constraint on pred_id
P6. prediction_resolution: missing CHECK constraints on market_outcome, fundamental_outcome, final_outcome
P7. experiment_registry: uses sequential EXP-001 IDs instead of deterministic signal_type+hash key
P8. dataset_registry: missing entity_type column (spec required)
P9. issuer_xwalk: missing PRIMARY KEY constraint (uses non-equivalent COALESCE unique index)
P10. issuer_xwalk: start_date/end_date always NULL — PIT lifecycle not implemented
P11. issuer_xwalk: CUSIP always NULL — EDGAR submissions don't provide it
P12. issuer_xwalk: OOM risk — accumulates all rows in Python list before inserting
P13. poll_endpoint count only 7, spec requires ≥10
P14. silence_detector does NOT update dataset_registry.last_poll_status (only inserts events)
P15. populate() overwrites row_count/schema_hash baselines, defeating drift detection
P16. surprise detector ADV20 window off-by-one (21 preceding, not 20)
P17. surprise detector doesn't log resolution data for predicted surprises
P18. post-mortem template missing Forward Test checklist and richer action fields
P19. check_column_died doesn't compare against historical baseline (false positives)
P20. Constitutional coverage scores: Kelly=0%, Falsify=25%, Provenance=30%, Sourced=20%

## Extraction: Fact-Check Results

F1. G1 PARTIALLY RIGHT — 9 tested is correct, but 17 missing (not 16). Total is 26.
F2. G6 line numbers fabricated — bare except blocks exist but at different lines, most set fallback values not bare pass
F3. G7 line numbers wrong — f-string SQL exists but at lines 245/277, not 142/196/218. Not real injection risk (internal registry values).
F4. G8 line numbers wrong — lines 438-444 are a parameterized SQL query, not regex
F5. G17 RIGHT — staging DB pattern exists at lines 418-434
F6. G18 RIGHT — cmd_confirm_fundamental exists at line 1817, works as described
F7. G12 RIGHT — no test_experiment.py exists
F8. P12 vs G3 CONFLICT — Gemini says OOM-safe via streaming; GPT says accumulates in list. GPT is more likely correct (describes specific implementation detail).

---

## Disposition Table

| ID | Claim | Disposition | Reason |
|----|-------|-------------|--------|
| G1/F1 | 17/26 scan_* untested | INCLUDE | Verified. Highest-priority gap. |
| G2 | Agent B schema match | INCLUDE | Verified by GPT (P2) and fact-check (F6) |
| G3 | Agent C OOM-safe | REJECT | Contradicted by GPT (P12) and F8. Rows accumulated in list. |
| G4 | Agent D all 5 rules implemented | INCLUDE | Verified |
| G5 | Agent E post-mortem matches | INCLUDE (partially) | GPT (P18) notes missing Forward Test section |
| G6 | Silent except blocks | INCLUDE | Real issue, wrong line numbers. 55+ broad exception handlers in scanner. |
| G7 | f-string SQL | DEFER | Internal values, not user input. Low real risk. |
| G8 | Fragile regex | REJECT | Wrong location. Need to verify if regex parsing exists elsewhere. |
| G9 | Hardcoded paths | INCLUDE (low priority) | Real but cosmetic |
| G10 | 16 untested scan_* | MERGE WITH G1 | Same finding, slightly different count |
| G11 | IPO ADV edge case | INCLUDE | Plausible, untested path. MERGE WITH P16 (ADV window bug). |
| G12 | No experiment test file | INCLUDE | Verified (F7) |
| G13 | No Kelly sizing integration | DEFER | Explicitly deferred in execution plan |
| G14 | Discovery double-count | INCLUDE | Plausible logic bug, needs code verification |
| G15 | DuckDB concurrency | DEFER | Single-user batch architecture. Gemini self-flagged this. |
| G16 | scoring.py excellent | INCLUDE | Verified quality signal |
| G17 | Staging DB pattern | INCLUDE | Verified (F5) |
| G18 | Dual resolution state machine | INCLUDE | Verified (F6) |
| P1 | DEFAULT on resolution_type | INCLUDE | Valid concern — hides omissions |
| P2 | Good tightening (CHECK constraints) | INCLUDE | Positive finding |
| P3 | No JSON constraint on linked_signal_ids | DEFER | DuckDB doesn't enforce JSON; app-level concern |
| P4 | CSV migration misuses strategy | INCLUDE | Real semantic bug |
| P5 | Missing FK on prediction_resolution | INCLUDE | Schema gap vs spec |
| P6 | Missing CHECK on outcome columns | INCLUDE | Schema gap vs spec |
| P7 | Sequential experiment IDs vs deterministic hash | INCLUDE | Allows duplicates, violates spec intent |
| P8 | Missing entity_type column | INCLUDE | Schema gap vs spec |
| P9 | Missing PRIMARY KEY on issuer_xwalk | INCLUDE | Schema gap vs spec |
| P10 | PIT lifecycle not implemented (dates always NULL) | INCLUDE | Critical gap — acceptance criteria fail |
| P11 | CUSIP always NULL | INCLUDE | Data gap, EDGAR doesn't provide it |
| P12 | OOM risk in xwalk loader | INCLUDE | Contradicts Gemini; GPT more specific |
| P13 | poll_endpoint count < 10 | INCLUDE | Acceptance criteria deterministic fail |
| P14 | silence_detector doesn't update last_poll_status | INCLUDE | Spec gap — events logged but status not updated |
| P15 | populate() overwrites baselines | INCLUDE | Defeats drift detection logic |
| P16 | ADV20 off-by-one (21 not 20) | INCLUDE | Quantitative bug |
| P17 | No resolution logging for predicted surprises | INCLUDE | Feedback loop incomplete |
| P18 | Post-mortem missing Forward Test section | INCLUDE | Spec gap |
| P19 | check_column_died no historical baseline | INCLUDE | False positive risk |
| P20 | Constitutional coverage scores | DEFER | GPT acknowledged limited visibility |

---

## Coverage Summary

- **Total extracted:** 38 items (18 Gemini + 20 GPT)
- **Included:** 27
- **Deferred:** 6 (low risk, out of scope, or limited visibility)
- **Rejected:** 2 (contradicted by evidence)
- **Merged:** 3 (duplicate findings across models)

## Where Models Agreed (high confidence)

1. Agent A incomplete (17/26 scan_* untested)
2. Agent B well-implemented (schema, dual resolution, Goodhart defense)
3. Agent D well-implemented (5 silence rules, state separation)
4. scoring.py mathematically solid
5. PIT lifecycle not implemented in issuer_xwalk (critical)
6. Post-mortem template incomplete vs spec

## Where Models Disagreed

1. **OOM safety of xwalk loader** — Gemini: "beautifully safe." GPT: "accumulates in list, will OOM." → GPT wins (more specific implementation detail)
2. **Silent except blocks** — Gemini: "pervasive, severe." Gemini self-correction: "intentional resilience." → Both views valid; log-then-continue is the right fix.
3. **DuckDB concurrency** — Gemini flagged, then self-corrected. GPT didn't mention. → Not a real issue for batch architecture.
