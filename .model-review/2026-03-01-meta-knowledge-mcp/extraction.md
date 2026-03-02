# Extraction: Meta Knowledge MCP Proposal

## Gemini 3.1 Pro Output

G1. On-demand knowledge fallacy: agents can't proactively query "what am I about to do wrong?" — failure modes (sycophancy, spin loops) are silent. Moving rules behind MCP degrades from "0% reliable at EoG" to invisible.
G2. Portability is illusory: .mcp.json still requires absolute paths (/Users/alien/Projects/meta/...), completely defeating portability argument.
G3. Redundant abstraction: agents already have Read/Glob/Grep and can read meta files directly. MCP wrapping adds latency and failure risk without adding capability.
G4. Push vs pull asymmetry: ALL cross-repo evidence cited is PUSH (meta analyzing and modifying target repos), not PULL (target querying meta). MCP is a pull mechanism. Evidence supports building an orchestrator, not a pull server.
G5. Native progressive disclosure exists: Skills platform already does metadata always-loaded → body on trigger → resources on demand. Embed failure modes into relevant skills instead.
G6. Context economics: if context pressure is the problem, solution is EMB pipeline (already built) or deterministic hooks that consume zero tokens until triggered — not an MCP that stuffs markdown back into context via tool calls.
G7. Alternative: abandon MCP. Universal rules stay in ~/.claude/CLAUDE.md. Domain rules in .claude/rules/. Shared executable knowledge in ~/Projects/skills/. Enforcement in hooks.
G8. Upgrade: build Orchestrator MVP (cron + SQLite + subprocess) from backlog instead. Reads session-receipts.jsonl, detects activity, spawns session-analyst targeting that repo.
G9. Upgrade: encode failure modes as PreToolUse prompt hooks instead of reference text — enforce actively at runtime.
G10. Priority 1: Kill the MCP proposal (negative work — zero hours on static markdown wrapping).
G11. Priority 2: Build Orchestrator MVP from backlog.
G12. Priority 3: Deploy Hook ROI Telemetry from backlog.
G13. Priority 4: Upgrade session-analyst to persistent subagent (Phase 2.4 of native-leverage-plan).
G14. Priority 5: Implement context-save before compaction (solves underlying anxiety driving the MCP idea).
G15. Constitutional violation P1: MCP takes architectural constraints and downgrades them back to text instructions that must be fetched.
G16. Constitutional violation P2: MCP provides neither block hooks nor Stop hooks — it's passive.
G17. Constitutional violation P8: Serving text via API is not architecture. Hooks actually stopping processes are architecture.
G18. Constitutional violation of generative principle: "agent theater" producing no autonomy value.
G19. Blind spot: may underestimate how bloated global CLAUDE.md is becoming. But fix is ruthless editing + hook offloading, not MCP.
G20. Blind spot: MCP might have value as a WRITE tool with validation gates (update_rule(category, new_rule)) — safer than raw Edit calls on CLAUDE.md.
G21. Blind spot: if meta eventually hosts on remote server for distributed agents, MCP API boundary becomes necessary. Assuming single-machine based on context.

## GPT-5.2 Output

P1. Portability contradiction: .mcp.json specifies invocation but doesn't ensure server exists on target machine. Absolute paths + uv + deps needed. Portable config ≠ portable behavior.
P2. Token savings not monotonic: if agent calls search_knowledge early in most sessions, could ADD tokens (scaffolding + JSON overhead + retrieval excerpts + follow-up calls).
P3. Lost-in-the-middle not solved: MCP retrieval doesn't guarantee right-time/right-place usage. Need retrieval+summarization constraints (top-k caps, byte/token budgets).
P4. Version skew replaced not solved: "parsed at startup" means meta repo state matters. Some sessions may use older meta checkout. Manual propagation skew → deployment skew.
P5. Governance exception: deploying MCP across ≥3 projects is functionally shared infrastructure. Not prohibited but needs explicit governance (autonomy boundary says "no shared hooks/skills affecting 3+").
P6. Tool overlap: if search_knowledge exists, specialized tools are either redundant convenience wrappers (conflicts with simplicity) or require curated schemas (more work than implied).
P7. Lifespan failure semantics: fail closed violates "fail open" principle; fail degraded reintroduces correctness risk. Not specified.
P8. Recommendation 1: Add measurement gates before moving any text. Log tokens/session attributable to meta text, tool call rate, correction metrics. Gate: move only if projected net savings ≥300 tokens/session.
P9. Recommendation 2: Start with ONE constrained tool: search + cite + budget params {query, scopes[], max_results, max_tokens_per_result, total_budget_tokens}. Track ≥70% single-call resolution.
P10. Recommendation 3: Make portability real with repo-local wrapper script (./tools/meta-knowledge) using relative paths or env var fallback.
P11. Recommendation 4: Enforce response size budgets (≤350 tokens p90) with ask-to-expand mechanism.
P12. Recommendation 5: Add freshness/commit-pin mechanism — tool responses include meta_commit_sha, warn when dirty.
P13. Testable prediction 1: After removing X lines from global CLAUDE, median input tokens per session decreases ≥400 tokens across ≥50 sessions.
P14. Testable prediction 2: Uninterrupted rate improves +5-10pp within 4 weeks in MCP-using repos.
P15. Testable prediction 3: Median time-to-first-correct-guidance drops ≥2 minutes for meta-knowledge tasks.
P16. Testable prediction 4: search_meta_knowledge called in ≤40% of sessions, median response ≤250 tokens.
P17. Testable prediction 5: Fresh machine time-to-working ≤15 minutes without manual path edits. NOTE: not yet testable if single machine.
P18. Testable prediction 6: "stale instruction" incidents drop ≥50% over 6 weeks.
P19. Constitutional scoring: P1 architecture=85%, P2 enforce by category=60%, P3 measure first=30%, P7 fail open=50%, P8 recurring patterns=75%.
P20. Where wrong: token savings magnitude uncertain (could be 100-300 not 600-1200). Tool call frequency uncertain. Maintenance overhead uncertain. Effect on autonomy might be weak if interruptions are mostly model behavior (sycophancy, planning) better solved by hooks.

## Fact-Check Required

FC1. G3 claim "agents can Read/Glob/Grep meta files directly" — TRUE only if agent has filesystem access to /Users/alien/Projects/meta from another project's working directory. Claude Code CAN read arbitrary paths, so this is technically true.
FC2. G4 claim "ALL evidence is PUSH not PULL" — VERIFIED against the 6 examples. All are meta→target, none are target→meta.
FC3. G5 claim "native progressive disclosure" — VERIFIED in opus-46-prompt-structure.md, skills platform does metadata→body→resources.
FC4. G15-G18 constitutional violations — need careful evaluation. G15 is partially right but MCP IS architecture (code, not text). G16 is correct for enforcement but MCP serves advisory knowledge. G17 conflates text-serving with enforcement (they're different use cases). G18 is harsh but has a point.
FC5. P2 token savings — valid concern. Needs measurement (agrees with P8).
FC6. P5 governance exception — VERIFIED against autonomy boundaries. MCP across 3+ projects is shared infrastructure.

## Disposition Table

| ID | Claim (short) | Disposition | Reason |
|----|--------------|-------------|--------|
| G1 | On-demand knowledge fallacy | INCLUDE — critical design constraint | Valid: behavioral rules must be always-loaded. But reference knowledge (hook designs, research findings) IS suitable for on-demand. Partition matters. |
| G2 | Portability illusory (abs paths) | INCLUDE — design requirement | Both models agree. Fix: env var or relative paths. |
| G3 | Redundant abstraction (Read/Glob) | INCLUDE — counterargument | Technically true but misses the point: MCP adds structure, search, and doesn't require knowing which file to read. |
| G4 | Push vs pull asymmetry | INCLUDE — fundamental insight | The strongest point. All evidence is push. MCP is pull. Changes what to build. |
| G5 | Native progressive disclosure | INCLUDE — alternative approach | Valid: skills already do tiered loading. Embed domain knowledge there. |
| G6 | Context economics (EMB/hooks) | INCLUDE — alternative approach | Valid: hooks are zero-token enforcement. EMB already exists for search. |
| G7 | Alternative: no MCP, use existing | INCLUDE — baseline comparison | The "do nothing different" option. |
| G8 | Build orchestrator instead | DEFER | Orchestrator is separate backlog item. Not mutually exclusive with MCP. Different problem (automation vs knowledge access). |
| G9 | Failure modes as prompt hooks | INCLUDE — hybrid approach | Encode high-frequency patterns as hooks. Good for top-5 failure modes. Doesn't scale to 22. |
| G10 | Kill the proposal | REJECT | Too absolute. The underlying problem (knowledge distribution) is real even if MCP isn't the only solution. |
| G11-G14 | Gemini priority list | DEFER | These are backlog items, not alternatives to the knowledge distribution problem. |
| G15 | P1 violation (downgrade to text) | INCLUDE — partial | Only valid for enforcement rules. Advisory knowledge is fine as text. Over-applies the principle. |
| G16 | P2 violation (passive) | INCLUDE — partial | Correct: MCP shouldn't replace enforcement. It should serve reference knowledge. |
| G17 | P8 violation (text ≠ architecture) | INCLUDE — partial | Valid for enforcement. But a searchable knowledge API IS architecture for advisory content. |
| G18 | Generative principle violation | REJECT | "Agent theater" is unfair. Reducing context-switching IS autonomy work. |
| G19 | Fix: ruthless editing of CLAUDE.md | INCLUDE — complementary | Should happen regardless. |
| G20 | MCP as write tool (update_rule) | INCLUDE — novel | Interesting: safe programmatic updates to meta rules with validation. |
| G21 | Remote/distributed future | DEFER | Not relevant to current single-machine setup. |
| P1 | Portable config ≠ portable behavior | MERGE WITH G2 | Same finding. |
| P2 | Token savings not monotonic | INCLUDE — measurement gate | Valid concern. Must instrument. |
| P3 | Lost-in-middle not solved by MCP | INCLUDE — design constraint | Need retrieval budgets. Agrees with P11. |
| P4 | Deployment skew replaces manual skew | INCLUDE — design requirement | Need commit-pin or freshness mechanism. |
| P5 | Governance exception for 3+ projects | INCLUDE — governance | Must explicitly govern. Add to autonomy boundaries. |
| P6 | Tool overlap (search vs specialized) | INCLUDE — design decision | Start with ONE search tool (P9). |
| P7 | Lifespan failure semantics | INCLUDE — design requirement | Must specify: fail open with empty results + warning. |
| P8 | Measurement gates first | INCLUDE — prerequisite | Both models implicitly agree: measure before migrating. |
| P9 | Single constrained search tool | INCLUDE — design decision | Best starting point. Expand only with evidence. |
| P10 | Repo-local wrapper for portability | INCLUDE — design decision | Practical solution to G2/P1. |
| P11 | Response size budgets ≤350 tokens | INCLUDE — design constraint | Prevents token blow-up. |
| P12 | Commit-pin freshness | INCLUDE — design feature | Addresses P4 (deployment skew). |
| P13-P18 | Testable predictions | INCLUDE — success criteria | All 6 are well-formed. Adopt as verification framework. |
| P19 | Constitutional scoring | INCLUDE — reference | Useful quantified alignment check. |
| P20 | GPT uncertainty items | INCLUDE — calibration | Honest about unknowns. |

## Coverage
- Total extracted: 41 (G1-G21, P1-P20)
- Included: 27
- Deferred: 5 (G8, G11-G14, G21)
- Rejected: 2 (G10, G18)
- Merged: 1 (P1 → G2)
- No item left undispositioned.
