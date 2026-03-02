# Cross-Model Review: Meta Knowledge MCP Server

**Mode:** Review (convergent/critical)
**Date:** 2026-03-01
**Models:** Gemini 3.1 Pro (~82K token context), GPT-5.2 (reasoning-effort high)
**Constitutional anchoring:** Yes (CLAUDE.md Constitution + GOALS.md)
**Extraction:** 41 items extracted, 27 included, 5 deferred, 2 rejected, 1 merged

## Key Takeaway

Gemini killed the proposal as stated. GPT conditionally approved it with heavy measurement gates. After fact-checking, the truth is between them but closer to Gemini.

**The fundamental insight (G4):** All 6 cross-repo evidence examples are PUSH (meta analyzing and modifying target repos), not PULL (a target repo querying meta for advice). Building a pull-based MCP server addresses a workflow that doesn't actually happen. The real workflow is: human cd's into meta → meta pushes changes outward. An MCP server optimizes the wrong direction.

**However:** The user identified a real problem that Gemini didn't fully address — knowledge that is NOT about enforcement but about reference/guidance. "What's the hook pattern for blocking writes?" is a legitimate pull query that currently requires context-switching to meta. The question is whether this happens often enough to justify infrastructure.

## Where I (Claude) Was Wrong

| My Original Claim | Reality | Who Caught It |
|-------------------|---------|--------------|
| "Push vs pull doesn't matter — it's about access" | ALL 6 cited examples are push. MCP is pull. Fundamental architectural mismatch. | Gemini (G4) |
| "Global CLAUDE.md token cost is the driver" | Global CLAUDE.md is only ~1,712 tokens. Not bloated. Token pressure is not the primary problem. | Measured directly |
| "Portability improves with .mcp.json" | .mcp.json with absolute paths (/Users/alien/...) is no more portable than global CLAUDE.md | Both models (G2, P1) |
| "MCP replaces always-loaded with on-demand" | For behavioral rules, on-demand = invisible. Agent can't query what it doesn't know it needs. | Gemini (G1) |

## Verified Findings (adopt)

| ID | Finding | Source | Verified How |
|----|---------|--------|-------------|
| G1 | Behavioral rules MUST stay always-loaded; agents can't self-diagnose failure modes | Gemini | Constitutional P1 + failure mode #15 (silent semantic failures) |
| G2, P1 | Portability argument fails with absolute paths | Both | .mcp.json in meta uses `/Users/alien/Projects/...` — verified |
| G4 | All cross-repo evidence is push, not pull | Gemini | Verified all 6 examples — every one is meta→target |
| G5 | Native progressive disclosure via skills exists | Gemini | Verified in opus-46-prompt-structure.md |
| G6 | EMB pipeline + hooks are zero-token alternatives | Gemini | EMB exists, hooks cost 0 context tokens |
| G9 | Top failure modes → prompt hooks (active enforcement) | Gemini | Better than passive reference. Scales to top 5-10, not all 22. |
| G20 | MCP as safe WRITE tool (update_rule with validation) | Gemini (blind spot) | Novel idea. Programmatic meta-rule updates > raw Edit on CLAUDE.md. |
| P2 | Token savings not guaranteed; could ADD tokens | GPT | Valid: tool call overhead + response excerpts. Must measure. |
| P4 | Deployment skew replaces manual propagation skew | GPT | Meta repo state varies; sessions may use stale checkout |
| P5 | MCP across 3+ projects = shared infrastructure (governance exception) | GPT | Verified against autonomy boundaries |
| P6, P9 | Start with ONE search tool, not 5 specialized tools | GPT | Simpler, lower maintenance, prove need first |
| P8 | Measurement gates before any migration | GPT | Can't know if this works without baseline data |
| P11 | Response size budgets (≤350 tokens p90) | GPT | Prevents token blow-up that erases savings |
| P13-P18 | 6 testable predictions as verification framework | GPT | Well-formed falsifiable criteria |

## Deferred (with reason)

| ID | Finding | Why Deferred |
|----|---------|-------------|
| G8 | Orchestrator MVP | Separate backlog item; solves different problem (automation vs knowledge access) |
| G11-G14 | Gemini priority list (telemetry, subagent, context-save) | All valid backlog items but not alternatives to the knowledge distribution question |
| G21 | Remote/distributed future | Not relevant until multi-machine |

## Rejected (with reason)

| ID | Finding | Why Rejected |
|----|---------|-------------|
| G10 | Kill the proposal entirely | Too absolute. The underlying problem (reference knowledge access across projects) is real even if the original MCP framing was wrong. |
| G18 | "Agent theater" — zero autonomy value | Unfair characterization. Reducing context-switching IS real work. But the DIRECTION (pull vs push) matters. |

## Gemini Errors (distrust)

| Claim | Why Wrong |
|-------|-----------|
| G3: "agents can just Read meta files" | Technically true (Claude Code CAN read arbitrary paths) but the agent doesn't know meta files exist from an intel session. Discovery is the problem, not access. |
| G15-G17: "MCP violates P1, P2, P8" | Over-applied. These principles are about ENFORCEMENT, not advisory knowledge. P1 says instructions alone are unreliable for enforcement — correct. But reference docs ("here's how to design a hook") are legitimately text, not enforcement. Gemini conflated serving reference content with serving behavioral rules. |
| G19: "fix is ruthless editing" | Global CLAUDE.md is only 1,712 tokens. It's already lean. There's nothing to ruthlessly edit. |

## GPT Errors (distrust)

| Claim | Why Wrong |
|-------|-----------|
| P19: Constitutional P1 score = 85% | Too generous. Gemini correctly identified that moving behavioral rules behind tools violates P1. Score should be ~40-50% for the proposal as originally stated. Higher only if partition is correct (behavioral rules stay loaded, reference knowledge goes behind MCP). |
| P13: "median input tokens decreases ≥400" | Global CLAUDE.md is only ~1,712 tokens total. Can't save 400 tokens from a 1,712 token file while keeping behavioral rules. The removable reference content is much smaller. |
| P14: "uninterrupted rate +5-10pp" | Likely overestimates. Knowledge access is weakly causal for autonomy. Hooks and behavioral rules matter more. GPT acknowledges this in P20. |

## Revised Recommendation

The original proposal (build a meta knowledge MCP server) is **wrong as stated** but contains a kernel of a real need. Here's what survives:

### What's Actually Needed

1. **Reference knowledge access from other projects** — "how do I design a hook?" "what did the prompt format research find?" This IS a pull use case, but it's LOW frequency. Doesn't justify dedicated infrastructure yet.

2. **Behavioral rule distribution** — NOT via MCP. These must stay always-loaded. The question is: where? Currently global CLAUDE.md. Could also be per-project `.claude/rules/` (more portable).

3. **Cross-project propagation** — Currently manual. The real pain point. But this is a PUSH problem (meta pushes rules outward), not a PULL problem (other projects pull knowledge).

### Revised Architecture Options

**Option A: Do nothing new (Gemini's recommendation)**
- Global CLAUDE.md stays as-is (~1,712 tokens, already lean)
- Reference knowledge stays in meta files, queryable via Read tool if agent knows the path
- Skills embed domain-specific failure modes (e.g., hook gotchas in researcher skill)
- Enforcement stays in hooks
- Cost: $0, 0 hours
- Risk: knowledge stays siloed in meta, accessible only when human navigates there

**Option B: Minimal knowledge MCP (GPT's recommendation, refined)**
- Single tool: `search_meta(query, max_tokens=350)` backed by lightweight search over meta .md files
- Added to each project's .mcp.json
- Global CLAUDE.md unchanged (behavioral rules stay)
- No migration of content — additive only
- instructions= tells agent what meta knows (hook designs, failure modes, research findings, architecture decisions)
- Cost: ~8-12 hours, near-zero maintenance
- Risk: tool rarely called, net-negative ROI. But cheap to test.
- Gate: measure baseline first (P8). Build only if reference knowledge queries happen ≥5/week across projects.

**Option C: Hybrid — skills embed knowledge + MCP for search**
- Top 5-10 failure modes encoded as prompt hooks on relevant events (G9)
- Reference content stays in meta .md files
- Skills link to meta knowledge where relevant (progressive disclosure, G5)
- Optional: lightweight MCP for cross-project search (Option B)
- Cost: ~15-20 hours
- Risk: over-engineering if usage is low

**Option D: Focus on push (G4's insight)**
- Instead of pull-based MCP, build the cross-project propagation pipeline
- session-analyst detects patterns → improvement-log → auto-generate rule updates → PR or direct commit to target repos
- This is the orchestrator MVP (G8) scoped to knowledge propagation only
- Cost: ~20-30 hours
- Risk: higher complexity, but addresses the ACTUAL workflow evidenced by cross-repo examples

### My Recommendation

**Option B with measurement gate.** It's the cheapest way to test whether pull-based knowledge access has real demand. If after 4 weeks `search_meta` is called <5 times/week, kill it. If it's called regularly, expand.

But **acknowledge Gemini was right about the big picture**: the real leverage is in push (propagation, orchestrator, hooks), not pull. The MCP is a small bet to test a hypothesis. Don't build the 5-tool version the original proposal described.

### What Stays in Global CLAUDE.md (no change)
Everything. It's 1,712 tokens. Already lean. No migration needed.

### What Gets Added (if Option B)
- A 50-100 line FastMCP server in meta with one search tool
- A line in each project's .mcp.json
- An `instructions=` string telling the agent what meta knows

### Success Criteria (from P13-P18, calibrated)
1. search_meta called in ≥5 sessions/week across all projects (proves demand)
2. p90 response size ≤350 tokens (proves token discipline)
3. No increase in correction rate (proves no harm)
4. If criteria 1 fails after 4 weeks: kill the MCP, move on to push-based propagation

### The Portability Question
The user's intuition was right: global CLAUDE.md is machine-local state that doesn't travel with repos. But the MCP doesn't solve this either (absolute paths). The real solution for portability is:
- `.claude/rules/` (per-repo, checked in, travels with clone)
- Skills (checked into shared skills repo, symlinkable)
- Hooks (referenced by path, needs setup script)

None of these are new. The portability gap is real but the MCP doesn't close it.
