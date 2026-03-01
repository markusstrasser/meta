# Extraction: project-upgrade Skill Review

## Extraction: gemini-upgrade-output.md

G1. [Phase 5 execution loop is purely instructional — violates "instructions alone = 0% reliable"]
G2. [100-line truncation is fatal — function called on line 150 flagged as DEAD_CODE]
G3. [Greedy JSON regex `\[.*\]` will capture beyond intended JSON array]
G4. [Rollback via `git checkout -- .` doesn't remove untracked files created during failed fix]
G5. [Phase 0 AST check uses system default encoding — non-UTF-8 crash risk]
G6. [Gemini output token limit (~8K default) will truncate large JSON arrays silently]
G7. [LLMs produce trailing commas in JSON — `json.loads` will reject]
G8. [Test suite per finding: 20 findings × 3min tests = 1 hour of testing]
G9. [File deletion/renaming: git add may only add new file, leave old unstaged]
G10. [Recommendation: Replace markdown Phase 5 with Python driver script for execution]
G11. [Recommendation: Use AST skeletonization instead of 100-line truncation]
G12. [Recommendation: Non-greedy regex + trailing comma sanitizer for JSON parsing]
G13. [Recommendation: Chunk Gemini request by directory to bypass output token limits]
G14. [Recommendation: Force UTF-8 encoding in file reading]

## Extraction: gpt-upgrade-output.md

P1. [Scaffolding phase is a second change-set needing separate human approval]
P2. [Rollback doesn't handle untracked files — same as G4]
P3. [Baseline test evidence uses `tail -20` which loses exit code — can't distinguish pass/fail]
P4. [DEAD_CODE verification (import check) doesn't prove function was unused — invalid inference]
P5. [Dump fidelity (truncation) contradicts "CERTAIN" constraint in Gemini prompt — same as G2]
P6. [Shell snippets: `while read f` without `-r`, `find` without parentheses for `-o` flags]
P7. [Token-budget 400K limit inconsistent with stated 1M capability claim]
P8. [Recommendation: Pre-triage validity gate — auto-check file exists, symbol greppable, auto-mark INVALID]
P9. [Recommendation: Split approval gates — (A) APPLY findings, (B) scaffolding proposals]
P10. [Recommendation: Fan-in-based dump priority — full text for high-import files, truncate leaf modules]
P11. [Prediction framework: ≥60% finding correctness, 0 unreviewed changes, ≥80% apply success rate]
P12. [Failure mode: hallucinated findings probability ~0.6 per run]
P13. [Recommendation: Use git worktree for isolation instead of checkout-based rollback]
P14. [Recommendation: Replace `tail -20` with `set -euo pipefail` and exit code capture]
P15. [Prediction: median time-to-value ≤45 minutes for repos under 150K LOC]

## Disposition Table

| ID | Claim (short) | Disposition | Reason |
|----|--------------|-------------|--------|
| G1 | Phase 5 is instructional only | INCLUDE | Valid concern. But ALL skills are instructions — the mitigation is per-step verification, not a driver script. Note for v2. |
| G2 | 100-line truncation causes false positives | INCLUDE | Verified: dump_codebase.py:128 truncates to 100 lines. Real risk for DEAD_CODE findings. |
| G3 | Greedy JSON regex | INCLUDE | Verified: dump_codebase.py doesn't have this (it's in SKILL.md Phase 2 inline code). Easy fix. |
| G4 | Rollback doesn't clean untracked files | INCLUDE | Verified: SKILL.md says `git checkout -- .` which only reverts tracked. Fix: `git checkout -- . && git clean -fd`. |
| G5 | Encoding crash risk | INCLUDE — low | macOS defaults to UTF-8. Fragile but unlikely. Fix: add `encoding='utf-8'` param. |
| G6 | Gemini 8K output limit truncates JSON | INCLUDE | Model-guide confirms default 8,192 max output. Must explicitly raise. Critical bug. |
| G7 | Trailing commas in JSON | INCLUDE | Real issue. Fix: regex sanitizer or `json5` library. |
| G8 | Test suite scaling | DEFER | Valid but premature. `-x` flag already in detection. Address if observed. |
| G9 | File rename tracking | DEFER | Edge case. Most findings don't rename files. |
| G10 | Python driver for Phase 5 | DEFER | Over-engineering for v1. Note for orchestrator evolution. |
| G11 | AST skeletonization | INCLUDE | Excellent idea. Preserves API surface without wasting tokens on function bodies. |
| G12 | Robust JSON parsing | INCLUDE | Fix for G3+G7. Easy implementation. |
| G13 | Chunk by directory | DEFER | Try raising max output tokens first. Chunking adds complexity. |
| G14 | Force UTF-8 | INCLUDE | Easy fix for G5. One-line change. |
| P1 | Scaffolding needs second approval | INCLUDE | Both models caught this. Constitutional alignment issue. |
| P2 | Rollback untracked files | MERGE WITH G4 | Same finding. |
| P3 | Exit code lost by tail -20 | INCLUDE | Verified: SKILL.md uses `eval "$TEST_CMD" > file`. Fix: capture `$?`. |
| P4 | Dead-code verification invalid | INCLUDE — nuance | Import check proves nothing breaks, not that function was unused. Add grep for callers. |
| P5 | Truncation contradicts certainty | MERGE WITH G2 | Same finding. |
| P6 | Shell snippet bugs | INCLUDE | Real bugs: no `-r` on read, missing find parentheses. Fix. |
| P7 | Token budget inconsistency | REJECT | Design choice (400K leaves room for prompt). Not a real inconsistency. |
| P8 | Pre-triage validity gate | INCLUDE | High ROI: auto-reject hallucinated paths/symbols before human reviews. |
| P9 | Split approval gates | MERGE WITH P1 | Same finding about scaffolding needing separate approval. |
| P10 | Fan-in-based dump priority | INCLUDE | Better than modification time. Files imported most = most important to include fully. |
| P11 | Testable prediction framework | INCLUDE | Adopt as evaluation scorecard for first run. |
| P12 | Hallucination probability ~0.6 | INCLUDE | Supports P8 (pre-triage gate). Accept as working estimate. |
| P13 | Git worktree isolation | DEFER | Good idea but adds complexity. `git reset --hard + git clean -fd` sufficient for v1. |
| P14 | Replace tail -20 with pipefail | INCLUDE | Fix for P3. Straightforward. |
| P15 | Time-to-value ≤45min | INCLUDE | Adopt as target metric. |

## Coverage Check
- Total extracted: 29 items (14 Gemini, 15 GPT)
- INCLUDE: 18
- DEFER: 5 (G8, G9, G10, G13, P13)
- REJECT: 1 (P7)
- MERGE: 5 (P2→G4, P5→G2, P9→P1)
- All items dispositioned: YES
