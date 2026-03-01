# CONTEXT: Cross-Model Review — Splitting Selve into Selve + Genomics Repo

## PROJECT CONSTITUTION
Quantify alignment gaps. For each principle, assess coverage (0-100%), consistency, testable violations.

The generative principle: "Maximize the rate at which the system corrects its own errors about the world, measured by market feedback."
Key derived principles: every claim sourced/graded, quantify before narrating, the join is the moat (one entity graph), compound don't start over.

## THE DECISION
Split `selve` (personal knowledge manifold) into:
1. **selve** — personal knowledge search MCP (18+ sources, local embedding/search)
2. **genomics** — WGS pipeline repo + MCP (111 Modal scripts, 42 analysis stages, 20+ ref DBs)

## KEY CLAIMS TO STRESS-TEST
1. "Integration seam is clean" — genomics produces results → embedded → searched. But: 10 genomics-specific skills live in selve, hooks reference genomics paths, data/ directory is shared, agent_coord.py coordinates across both.
2. "Different execution model" — Modal serverless vs local search. But: genomics curation tools (manual_variant_review.py, generate_review_packets.py) run locally.
3. "Genomics MCP enables cross-project queries" — e.g., intel queries PGx for biotech DD. But: does this use case actually exist yet? Is it speculative?
4. "Both MCPs lighter and focused" — But: adds coordination overhead, two CLAUDE.md files, two hook configs, two MCP configs.

## MIGRATION RISKS
- Git history: 111 scripts + 42 analysis dirs + 18+ docs have commit history in selve. Options: git filter-branch/filter-repo to extract with history, or fresh repo losing history.
- Personal health info in git history: medical records, WGS variants, health summaries committed over time. Even if removed from HEAD, still in git objects. Requires BFG or git-filter-repo to truly scrub.
- Skills split: 10+ genomics skills (genomics-pipeline, genomics-status, annotsv, clinpgx-database, gget, modal, neurokit2, oura-ring, vcfexpress) move to genomics. But modal is also used by non-genomics. researcher and epistemics are shared.
- Hooks: data/ write guard, bare python guard, ruff-format, stop research gate — which repo gets which?
- Orchestrator: autonomous-agent-architecture.md references "self" project with 7 loops. Needs update to reference "genomics" project. Does the orchestrator dispatch to both selve AND genomics?
- Selve search integration: after split, how does selve index genomics results? Git source in selve won't see genomics commits. Need explicit export/sync mechanism.

## WHAT I WANT FROM YOU
1. Logical inconsistencies in the claims
2. Cost-benefit analysis of splitting now vs later
3. Testable predictions (what would prove the split was right/wrong)
4. Hidden coupling we're underestimating
5. The git history + PII scrubbing problem — what's the right approach

