# Cross-Model Review: Git Workflow for AI Agent Self-Optimization
**Mode:** Review
**Date:** 2026-02-28
**Models:** Gemini 3.1 Pro, GPT-5.2

## Where I (Claude) Was Wrong

Both models independently identified the same flaw in my reasoning:

| My Claim | Reality | Who Caught It |
|----------|---------|---------------|
| "Git is redundant with MEMORY.md/improvement-log" | Confuses current-state richness with historical observability. Mutable files overwrite their own rationale — git is the only append-only record. | Both models |
| "Agent never reads git log, so it doesn't matter" | Non sequitur. Workflow should be optimized for failure modes, not nominal behavior. Future archaeology consumers don't exist yet. | GPT |
| "Topic-organized files > chronological git" | True for execution, false for self-optimization. When a rule is deleted, the reason for its existence disappears from the file. | Gemini |

## Converged Recommendation (both models agree)

**No branches. No `--no-ff`. Yes to trailers — scoped to self-optimization artifacts.**

| Enhancement | Gemini verdict | GPT verdict | Adopt? |
|-------------|---------------|-------------|--------|
| Feature branches by default | No — too heavy for rapid-fire commits | No — low ROI, adds operational surface area | **No** |
| `--no-ff` merges | No — agent doesn't need visual grouping | No — moot without branches | **No** |
| Git trailers (lightweight) | Yes — "natively parseable, zero-friction, high ROI" | Yes — "highest signal-per-cost lever" | **Yes** |
| Long structured messages | Not recommended | Medium ROI at best — template fatigue risk | **No** |
| Branch/merge as hook targets | "Speculative, fragile, architecturally misaligned" | Low ROI — existing hooks can trigger on file patterns | **No** |

## Verified Findings

| Finding | Source | Verified How |
|---------|--------|-------------|
| Diffs preserve syntax, not semantics — same diff can mean bugfix, revert, experiment, or refactor | GPT (information theory framing) | Logical: `git diff` of "remove rule X" is identical whether the reason is benchmark failure, redundancy, or tool conflict |
| 4 commits in 112 seconds (11:57:15–11:59:07) makes branching impractical | Gemini | Verified from `git log --format='%h %ai'` |
| SessionEnd/PreCompact hooks are better merge-event substitutes | Gemini | True per hook events reference — both exist, SessionEnd fires on every session |
| Trailers are machine-parseable via `git log --format='%(trailers)'` | Both | Standard git feature |
| Session transcripts are ephemeral — Evidence: links may rot | GPT blind spot #2 | True: transcripts at `~/.claude/projects/*/UUID.jsonl` have no retention guarantee |

## Gemini Errors

| Claim | Assessment |
|-------|-----------|
| "Claude 3.7/Code" reference | Anachronism — current model is Claude Opus 4.6. Minor, doesn't affect reasoning. |
| Temperature override caveat noted in output | Accurate — Gemini thinking models lock temperature. The `-t 0.3` was correctly ignored. |

## GPT Errors

| Claim | Assessment |
|-------|-----------|
| Math notation (LaTeX) used throughout | Not wrong, but over-formal for the domain. The mutual information framing is valid but unnecessary to reach the conclusion. |
| "≥30-60% time-to-answer improvement" | Fabricated precision — no empirical basis for these specific numbers. The directional claim is plausible. |

## The Trailer Schema (GPT's recommendation, Gemini-compatible)

Both models converged on similar trailer sets. GPT's is more specific:

```
Evidence: session/<id> or improvement-log#<n>
Verifiable: yes|no
Affects: memory|rules|hooks|code
Reverts-to: <commit> (when applicable)
```

**Scope:** Only required for commits modifying CLAUDE.md, MEMORY.md, improvement-log.md, and hook code/config. Ordinary code commits keep simple messages.

## Key Insight (GPT, verified)

> "Identifiers are high-leverage bits: they let you retrieve large external context with a few bytes. This is classic indexing: small message, large recall."

A trailer like `Evidence: session/a2679f18` costs ~30 tokens but links the commit to a 450-line transcript. That's the information-theoretic argument for trailers over verbose messages.

## Open Risk (both models flagged)

Agent may hallucinate trailer values (fake Finding-IDs, claim `Verifiable: yes` without running checks). Gemini flagged this as a blind spot. GPT suggested conservative semantics: default to `Verifiable: no` unless proven. A PreToolUse:Bash hook could validate `Evidence:` references exist before allowing the commit.
