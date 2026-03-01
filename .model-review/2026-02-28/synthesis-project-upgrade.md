# Cross-Model Review: project-upgrade Skill

**Mode:** Review (convergent/critical)
**Date:** 2026-02-28
**Models:** Gemini 3.1 Pro, GPT-5.2
**Constitutional anchoring:** Yes (CONSTITUTION.md, GOALS.md)
**Extraction:** 29 items extracted, 18 included, 5 deferred, 1 rejected, 5 merged

## Verified Findings (applied)

| ID | Finding | Source | Fix Applied |
|----|---------|--------|------------|
| G2, P5 | Truncation causes false positives (DEAD_CODE, BROKEN_REFERENCE) | Both | Replaced 100-line truncation with AST skeletonization for Python files. Preserves function/class signatures. |
| G3, G7, G12 | JSON parser: greedy regex + no trailing comma handling | Gemini | Bracket-counting parser with trailing comma sanitizer, error recovery to raw file |
| G4, P2 | Rollback doesn't clean untracked files | Both | Changed `git checkout -- .` to `git reset --hard HEAD && git clean -fd` + invariant check |
| G5, G14 | Encoding crash risk in file reading | Gemini | Added `encoding='utf-8'` to all file reads |
| G6 | Gemini 8K default output limit truncates JSON | Gemini | Added warning + guidance to raise max output tokens or split by directory |
| P1, P9 | Scaffolding is second change-set needing separate approval | Both | Added explicit "REQUIRES SEPARATE APPROVAL" gate with quantified benefit requirement |
| P3, P14 | Test baseline loses exit code via `tail -20` | GPT | Added explicit `$?` capture with `set +e` |
| P4 | DEAD_CODE verification doesn't prove non-use | GPT | Added `grep -r` for callers before removal, with dynamic dispatch caveat |
| P6 | Shell bugs: `read` without `-r`, `find` without parentheses | GPT | Fixed both in baseline snapshot section |
| P8 | Missing pre-triage validity gate | GPT | Added automated file-existence + symbol-grep check before human review |
| P10 | Fan-in-based dump priority | GPT | Implemented in dump_codebase.py — files show fan-in counts in inventory |
| P11 | Missing evaluation scorecard | GPT | Added 6-metric scorecard with targets and failure thresholds |

## Deferred (with reason)

| ID | Finding | Why Deferred |
|----|---------|-------------|
| G8 | Test suite per-finding is slow | Premature — `-x` flag already detected. Address after observed issue |
| G9 | File rename tracking in git | Edge case — most findings don't rename files |
| G10 | Python driver script for Phase 5 | Over-engineering for v1. All skills are instructional by nature |
| G13 | Chunk Gemini request by directory | Try raising max output tokens first. Chunking adds significant complexity |
| P13 | Git worktree isolation | `git reset --hard + git clean -fd` sufficient for v1 |

## Rejected (with reason)

| ID | Finding | Why Rejected |
|----|---------|-------------|
| P7 | Token budget 400K inconsistent with 1M claim | Design choice — 400K leaves room for prompt + safety margin. Not an inconsistency. |

## Gemini Errors (distrust)

| Claim | Assessment |
|-------|-----------|
| "Phase 0 AST encoding crash" (G5) | Overstated — macOS defaults to UTF-8. But fix is cheap, so applied anyway. |
| Temperature override warning | Gemini correctly self-reported that temperature was locked at 1.0. Not an error, but means our `-t 0.3` request is ignored. |

## GPT Errors (distrust)

| Claim | Assessment |
|-------|-----------|
| "Probability estimates" (P12) | GPT assigned 0.6 probability to hallucinated findings. These are priors, not measured. Useful as estimates, not facts. |
| "Bash snippets are executed literally" (P6 caveat) | GPT hedged that these might be illustrative. They're illustrative — Claude reads the SKILL.md as instructions, not as a shell script. But the bugs are real if Claude copies them. |

## Key Insight: Skeletonization

The single highest-value change from this review. Before: files truncated to 100 lines, losing function definitions that Gemini then hallucinates as dead code. After: AST extracts all signatures (imports, class defs, function sigs with docstrings), preserving the API surface while saving ~70% of tokens per large file.

Tested: genomics repo now has 4 skeletonized files (previously 24 truncated). `modal_utils.py` shows fan-in:87 — correctly identified as the most important file in the project.

## Files Modified

- `~/Projects/skills/project-upgrade/SKILL.md` — 12 fixes applied
- `~/Projects/skills/project-upgrade/scripts/dump_codebase.py` — Rewritten with skeletonization + fan-in + UTF-8
- `~/Projects/meta/.model-review/2026-02-28/extraction-upgrade.md` — Disposition table
