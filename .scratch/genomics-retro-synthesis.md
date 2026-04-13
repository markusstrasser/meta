# Genomics Retro Synthesis — 2026-04-02

Cross-artifact pattern extraction from decisions, audits, upgrade runs, model-reviews,
and meta improvement-log. Source artifacts span 2026-02-28 to 2026-04-02.

## Artifact Inventory

| Type | Count | Span |
|------|------:|------|
| Decision records | 57 | Feb 24 -- Apr 02 |
| Research memos | 119 | Mar -- Apr |
| Audit directories | 37 | Mar 18 -- Apr 02 |
| Model-review dirs | 99 | Mar 20 -- Apr 02 |
| GPT-5.4 review rounds | 5 (37 responses) | Mar 20 -- present |
| Project-upgrade runs | 13 dirs | Feb 28 -- Apr 01 |
| Total upgrade findings | ~858 | across all runs |
| Meta improvement-log genomics entries | 25+ | Mar 07 -- Mar 26 |
| Worktrees | 12 (11 agent + 1 symlink), 5.3 GB | Mar 31 |

---

## 1. Recurring Issues Across Multiple Artifacts

### 1a. Split Authority / Registry Drift (found in 6+ artifacts)

The single most repeated finding. The stage registry (`pipeline_stages.py`) does not
match runtime reality in multiple dimensions:

- **Name drift:** 9 registry-vs-decorator name mismatches (architecture-unelegance, Mar 31).
  `pgx_regenotype` vs `pgx_regenotype_missing`, `triage` vs `rare_variant_triage`, etc.
- **Registry not executable truth:** orchestrator shells into scripts ignoring registry's
  `app_name` / `function_name` (architecture-unelegance finding #1-2).
- **Local scripts registered as Modal stages:** plain scripts (cognitive_trait_panel,
  sensory_receptor_panel) registered in the Modal-oriented stage registry, producing
  plans the executor cannot run (harness audit B1, Mar 26).
- **`app_name` and `audit_commit` have zero code accesses** -- decorative governance
  fields (architecture-unelegance finding #9).
- **Dangling dependency in DAG:** `rasp_ddg` depends on `"rare_variant_triage"` but
  actual stage is `"triage"` (pipeline-audit, Mar 18).
- **`spliceai` references nonexistent `finalize` function** (pipeline-audit, Mar 18).

This was flagged in Feb 28, Mar 06, Mar 18, Mar 26, and Mar 31 artifacts.

### 1b. Path Drift / Wrong Artifact Resolution (found in 5+ artifacts)

Consumers point at stale or wrong paths and silently degrade:

- **`trait_panels` path:** `reverse_phenotype.py`, `contradiction_resilience.py`,
  `genome_dockets.py` all look for `analysis/trait_panels/` but producer writes
  `analysis/trait_variants/trait_panel.json` (synthesis audit B3-B4, Mar 26).
- **PharmCAT path:** 3 competing resolvers across `finding_adapters`, `analysis_loaders`,
  and `generate_dashboard` (architecture-unelegance #9-10).
- **HLA/KIR paths:** `virome_expansion.py` points at wrong HLA path and dead KIR path
  (synthesis audit B3, Mar 26).
- **PRS JSON contract broken:** 3 consumers treat dict-format PRS output as a bare list,
  silently dropping all PRS evidence (harness audit B2, Mar 26).
- **`review_packets` fallback ladders:** `triage/review_packets.json` vs
  `review_packets/review_packets.json` -- migration never finished
  (architecture-unelegance #11).

### 1c. Silent Degradation / Swallowed Errors (found in 4+ artifacts)

- Consumers that fail to load data return empty results instead of failing. The
  `generate_dashboard.py` file alone has 5 separate fallback stubs that mask broken
  imports (architecture-unelegance #12).
- Raw subprocess calls without `check=True` in critical-path scripts like
  `modal_slivar.py` (pipeline-audit audit 5).
- NCBoost2 swallowed extraction errors (upgrade Feb 28 -- Mar 03).
- Stale PRS data file served as canonical despite containing LOW_PRECISION flags
  (improvement-log, Mar 26).

### 1d. Report Generator Monoliths (found in 3+ artifacts)

Five files exceed 2,500 lines and keep accumulating local loaders instead of consuming
a shared assembly:

| File | Lines | Local loaders |
|------|------:|:-------------:|
| `generate_clinical_report.py` | 4,760 | 42 `load_*` fns |
| `generate_dashboard.py` | 3,772 | 46 top-level fns |
| `pipeline_stages.py` | 2,822 | registry + graph + paths + display |
| `generate_review_packets.py` | 2,736 | threshold + lookup loading at import |
| `generate_condition_reports.py` | 2,497 | 16 `load_*` fns |

The finding-IR stack (adapters/IR/policy) exists but has only 2 importers of
`finding_policy` vs 52 consumers of `review_packets.json`.

### 1e. False Multi-Sample Generality (found in 3+ artifacts)

151 hardcoded `markus` references. The repo pays abstraction cost for N>1 samples
without actually supporting it -- `sample_id` fields in freshness markers, duplicate
path layers, hardcoded defaults. Called out in architecture-unelegance (Mar 31),
GPT-5.4 findings (Mar 28), and upgrade runs.

### 1f. Agent-Specific Failures in Genomics Sessions

From meta improvement-log (13 genomics sessions analyzed):
- **File-poll loops:** 11x consecutive Read on same file (a62b3f8f), 3x sleep-poll (955df826).
- **Stale data read:** reported retracted SCZ PRS finding as headline (fddae46b).
- **Parallel agent commit contamination:** uncommitted edits swept into wrong commit (dfc98f6c).
- **Callsite renames missed by dedup agents:** 3/4 agents deleted functions but left
  old-name call sites, requiring ruff cleanup.
- **28% hallucination rate on model-review code claims:** 11/40 claims of "missing feature"
  were wrong -- features existed in code (model-review retro, Mar 25).
- **Duplicate brainstorm sessions:** same topic ran 3x across parallel sessions (a62b3f8f, 5584f9f9, 955df826).

---

## 2. Recommended But Never Implemented

| Recommendation | Source | Date | Status |
|---------------|--------|------|--------|
| Make stage identity canonical (registry = decorator name) | architecture-unelegance #1 | Mar 31 | Partially addressed by StrEnum in worktree harness commits, but name drift still present |
| Split `StageSpec` into execution + presentation | architecture-unelegance #4 | Mar 31 | Not done |
| Pick one findings architecture (adapter/IR/policy vs raw JSON) | architecture-unelegance #3 | Mar 31 | Convergence progress (Apr 02) shows adapter extraction, but dual paths remain |
| Package repo properly, kill 47 `sys.path.insert` | architecture-unelegance #10 | Mar 31 | Not done |
| Make imports pure (no file scanning at import time) | architecture-unelegance #9 | Mar 31 | Not done; `generate_review_packets.py` and `variant_evidence_core.py` still load at import |
| AnalysisBundle / ReportResources passed to renderers | architecture-unelegance #8 | Mar 31 | Not done; individual loaders still grow |
| Hard call on sample scope (single vs N>1) | architecture-unelegance #12 | Mar 31 | Not done |
| Delete dead `config/default.yaml` + `wgs_config.py` YAML path | integration-audit | Mar 18 | Unknown |
| Register sidecar artifacts consumed by reports | integration-audit | Mar 18 | Partially via adapter extraction |
| Add `validate()` to critical-path scripts (slivar, PRS, GLIMPSE2, mito) | pipeline-audit | Mar 18 | Unknown |

---

## 3. Patterns of Failure / Inefficiency

**Stranded migrations.** New abstractions get created (finding IR, typed config,
shared loaders, local_stage wrapper, summary schemas) but old code never fully migrates.
The repo accumulates parallel systems: 6 importers of `finding_ir` vs 52 consumers
of `review_packets.json`; 2 importers of `pipeline_config` vs 170+ importers of
`modal_utils`; 18 `Paths()` callsites vs 174 `wgs_config` importers using raw globals.

**QA compensates for weak contracts.** 12+ validation/lint scripts police invariants
that could be intrinsic to types and assembly APIs. Each new analysis adds another
canary/lint/check instead of enforcing at the contract level.

**Audit volume exceeds fix throughput.** 858 total findings across upgrade runs,
99 model-review directories, 37 audit directories. The convergence-progress file
(Apr 02) shows substantial burn-down (72 tests, 74/74 canaries, 11 product surfaces
cleaned), but the finding generation rate appears to exceed the fix rate.

**Agent hallucination on code claims.** Cross-model reviews hallucinate missing features
at 28% rate. This is structural -- the review process now includes mandatory grep
verification (Step 4), but the finding itself recurs.

---

## 4. What's Working Well

- **DAG and orchestration layer** is a real abstraction, not decorative
  (architecture-unelegance strength #1).
- **Decision journal** (57 records) provides genuine path-dependent reasoning history.
- **Threshold centralization ~95% complete** (pipeline-audit Mar 18).
- **GPT-5.4 review cycle** producing real bugs: PRS dosage logic bug, conditional
  FDR statistical bug, JSON shape bugs, coordinate normalization bug (Mar 28 findings).
- **Convergence progress** (Apr 02): 72 focused tests passing, 74/74 canaries, product
  import lint clean, silent fallback lint clean, adapter canonicalization across 6 domains.
- **Review packet typed models** centralized meaningfully (variant_evidence_core,
  review_packet_models).
- **Canary gate** operational at 74/74 + 6/6 analysis canaries.

---

## 5. Worktree Status

12 entries in `.claude/worktrees/`: 11 agent worktrees + 1 biomedical-mcp symlink.
Total disk: **5.3 GB**. All 11 agent worktrees date from Mar 31 and contain harness
refactoring commits (StrEnums, atomic JSON, threshold registry migration, etc.).
All appear to be on topic-specific branches (`worktree-agent-*`). These are stale
(2 days old, work appears merged or superseded) and are safe to prune.

---

## 6. Concrete Fix Recommendations (Priority Order)

1. **Prune worktrees.** `git worktree prune` + `rm -rf .claude/worktrees/agent-*` to
   reclaim 5.3 GB. Verify commits are on main first.

2. **Fix the 4 broken data contracts.** PRS JSON dict-vs-list (B2), trait_panels path
   (B3-B4), PharmCAT path in genome_dockets (B4), HLA/KIR paths in virome_expansion
   (B3). These are active bugs producing silent wrong output.

3. **Enforce stage name canonicality.** Add a lint test: for each `_reg(StageSpec(...))`,
   grep the target script for `@stage("...")` and assert names match. Prevents future
   drift and catches the 9 existing mismatches.

4. **Delete decorative StageSpec fields.** `app_name` (0 accesses) and `audit_commit`
   (0 accesses) advertise governance that does not exist. Remove or wire them.

5. **Decide sample scope.** Either commit to single-sample (delete `sample_id` from
   freshness, collapse path layers) or properly parameterize. The false generality costs
   complexity without delivering flexibility.

6. **Slow the audit cadence, increase the fix cadence.** 858 findings across 13 upgrade
   runs means ~66 findings per run, but the convergence burn-down shows ~20-30 fixes
   per focused session. Either reduce audit frequency or dedicate sessions to pure
   fix execution against the existing backlog.
