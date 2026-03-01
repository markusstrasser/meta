# Cross-Model Review Synthesis: Selve → Selve + Genomics Split

**Mode:** Review (critical)
**Date:** 2026-02-28
**Models:** Gemini 3.1 Pro, GPT-5.2
**Constitutional anchoring:** Yes (CONSTITUTION.md, GOALS.md)

---

## Fact-Check Results

### What both models got wrong about data coupling

Both models assumed `data/` is git-tracked shared mutable state. **It's not.** `data/` is in `.gitignore` (0 files tracked). Raw genomics data lives on external volumes via symlinks. The coupling is **filesystem-level** (paths in configs/scripts), not **git-level**.

### PHI scope is docs, not blobs

The actual PHI in git history is **20+ markdown docs** in `docs/` (health summaries, WGS reports, medical contacts, omics outreach emails). Binary data (CRAM, VCF) was never committed. This means:
- PII scrubbing is scoped to text files in `docs/`, not multi-GB binary blobs
- `git-filter-repo` runs much faster on text paths than Gemini/GPT implied
- Repo size isn't inflated by binary PHI (their "technical necessity" concern is moot)

### Gemini's dismissal of cross-project genomics queries — partially wrong

Gemini said "N=1 PGx data has zero statistical base-rate value for biotech DD." But Gemini then self-corrected: if genomics MCP queries **reference databases** (PharmGKB, ClinVar, gnomAD constraint scores) rather than personal variants, the cross-project value is real. This is the likely use case — drug target validation via curated biomedical DBs, not personal VCF lookups.

### GPT's coupling tightness scores — somewhat pessimistic

GPT scored `data/` at tightness 5. Since `data/` isn't in git, the coupling is "where does genomics write results and how does selve find them" — a **path configuration** issue (tightness 2-3 with absolute paths or env vars), not shared mutable state.

---

## Verified Findings (adopt)

| Finding | Source | Verified How |
|---------|--------|-------------|
| PHI docs (20+) in git history need scrubbing | Both | `git ls-files docs/` confirmed personal health files tracked |
| `data/` not in git, coupling is filesystem paths only | Fact-check | `git ls-files data/` = 0 files, `.gitignore` confirmed |
| Hooks need per-repo split (data guard conflicts with genomics writes) | Gemini | `settings.json` PreToolUse blocks `data/` writes; genomics scripts write to `data/wgs/` |
| PII scrub should happen BEFORE split (splitting copies the problem) | GPT | Logically sound — filter-repo on one repo easier than two |
| Export contract needed for clean seam (manifest + versioned artifacts) | GPT | Without it, selve relies on implicit path knowledge of genomics output structure |
| agent_coord.py needs interface refactor | Both | SessionStart hook hardcodes selve-local agent_coord.py |
| 116 genomics scripts have git history worth preserving | Fact-check | `git ls-files scripts/genomics/ \| wc -l` = 116 |

## Where I Was Wrong

| My Original Claim | Reality | Who Caught It |
|-------------------|---------|--------------|
| "Integration seam is clean" | Seam is at filesystem path level (medium coupling), not git/code level. Cleaner than models claimed, but needs explicit export contract | Both (overstated), fact-check (calibrated) |
| Cross-project PGx query for biotech DD | As personal N=1 variants: low value. As reference DB queries: real value | Gemini (then self-corrected) |

## Gemini Errors

| Claim | Why Wrong |
|-------|-----------|
| "data/ is shared mutable state [tightness 5]" | data/ is gitignored, not tracked. Coupling is path-level, not state-level |
| "Git filter-repo will rewrite entire repository SHAs" | True, but scope is limited to docs/ text files, not massive binary blobs. The concern about repo size degradation doesn't apply |
| "neurokit2 and oura-ring might need cross-pollination with variant curation" | Plausible but speculative — no evidence of current cross-usage |

## GPT Errors

| Claim | Why Wrong |
|-------|-----------|
| "PII scrubbing: 16-40 hrs" | Likely 4-8 hrs given scope is ~20 markdown files, not binary blobs. git-filter-repo with path list is fast |
| "Shared data/ is tightness 5" | Tightness 2-3 (path config), not 5 (shared mutable state) |
| "Commit-based triggers: tightness 4" | No evidence selve indexes based on git commits from genomics |

---

## Revised Recommendations (priority order)

### 1. PII scrub first (before split)
- Scope: 20+ docs in `docs/personal_*`, `docs/HEALTH_*`, `docs/brain_*`, `docs/hifi_*`, `docs/handoffs/personal_*`
- Tool: `git-filter-repo --path docs/personal_wgs_report.md --path docs/HEALTH_AND_GENOMICS_SUMMARY.md ...`
- Either delete from all history OR move to a never-committed location
- Estimated effort: 4-8 hrs (including verification)
- **Do this in the current monorepo before splitting**

### 2. Define export interface
- Genomics writes results to a known location (already `/data/wgs/analysis/` or external volume)
- Create a simple manifest: `genomics_export.json` listing available result sets + paths
- Selve indexes from the manifest, not from implicit path knowledge
- This is what makes the "clean seam" actually clean

### 3. Split repos via git-filter-repo
- Extract `scripts/genomics/` with history into new `genomics` repo
- Move genomics-specific docs (20+ files) to genomics repo
- Leave selve with search engine + personal knowledge sources
- Skills: genomics-pipeline, genomics-status, annotsv, clinpgx-database, gget, vcfexpress → genomics repo
- Skills: modal → probably genomics (primary consumer), but could be shared
- Rules: epistemics.md → shared (used by both domains)

### 4. Create genomics MCP
- Typed query interface: `get_variant()`, `get_prs()`, `pipeline_status()`, `query_pharmgkb()`, `query_clinvar()`
- Exposes reference DB queries (high cross-project value)
- Exposes pipeline status and results (high within-project value)
- Personal variant data: available but clearly labeled as N=1

### 5. Refactor hooks per repo
- Genomics: remove data/ write guard, keep ruff-format, add Modal-specific guards
- Selve: keep data/ write guard, keep research gate, remove genomics-specific stop hook logic
- Both: keep bare python guard (shared pattern)

### 6. Update orchestrator references
- `autonomous-agent-architecture.md`: "self" → "genomics" for Loops 1,2,6,7
- `agent_coord.py`: dispatch to `~/Projects/genomics/` for pipeline tasks
- Loops 3,4,5 (phenotype investigation, multi-model review, N=1 experiments) may span both repos — orchestrator needs multi-repo dispatch

---

## Constitutional Alignment Assessment

| Principle | Impact of split |
|-----------|----------------|
| #1 Autonomous Decision Test | **Positive** — leaner context per session, faster decisions |
| #5 Fast Feedback | **Positive** — search and pipeline operate at their natural speeds |
| #6 The Join Is The Moat | **Neutral if export contract exists** — one graph via manifest-based integration. **Negative if ad-hoc** — knowledge silos |
| #10 Compound, Don't Start Over | **Positive if history preserved** — git-filter-repo keeps commit history. **Negative if fresh repo** — loses institutional memory |

---

## Sequencing

1. PII scrub (selve monorepo)
2. Define export contract (manifest spec)
3. git-filter-repo to extract genomics with history
4. Set up genomics repo (CLAUDE.md, skills, hooks, MCP)
5. Update selve (remove genomics paths, update CLAUDE.md, update hooks)
6. Build genomics MCP server
7. Update orchestrator/meta docs
8. Verify: selve indexes genomics results via manifest, cross-project queries work
