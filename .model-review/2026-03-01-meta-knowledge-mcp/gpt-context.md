# CONTEXT: Cross-Model Review — Meta Knowledge MCP Server

## PROJECT CONSTITUTION (in CLAUDE.md)
Generative principle: "Maximize the rate agents become more autonomous, measured by declining supervision."
Key principles:
1. Architecture over instructions (instructions alone = 0% reliable at EoG)
2. Enforce by category: cascading waste → hooks, epistemic → advisory, style → instructions
3. Measure before enforcing (log hook triggers for ROI)
4. Self-modification by reversibility + blast radius
5. Research is first-class (divergent → convergent → dogfood → analyze)
6. Skills governance: meta owns quality, skills in ~/Projects/skills/
7. Fail open, carve exceptions (explicit fail-closed list)
8. Recurring patterns → architecture (10+ occurrences → hook/skill/scaffolding)
9. Cross-model review for non-trivial decisions
10. Git log is the learning (every correction is a commit)

Autonomy boundaries:
- Hard limits: no Constitution/GOALS.md edits, no shared hooks/skills affecting 3+ projects, no delete architectural components
- Autonomous: update meta's CLAUDE.md/MEMORY.md/improvement-log, add meta-only hooks, run session-analyst, create new skills (propagation = propose)

## PROJECT GOALS
Primary metric: fraction of session time Claude operates without human correction
Target: 90% uninterrupted rate within 6 months
Projects served: intel, selve, genomics, anki, skills, papers-mcp

## THE PROBLEM

Meta accumulates knowledge about Claude Code optimizations across 6 projects. Current distribution:
1. Global ~/.claude/CLAUDE.md (~200 lines, always loaded in every session, every project)
2. Shared skills (symlinked from ~/Projects/skills/)
3. Project CLAUDE.md files (per-project, meta's is ~300 lines)
4. MEMORY.md (per-project persistent memory)

Problems:
- Global CLAUDE.md is machine-local. Anyone cloning repo gets different behavior. Not portable.
- Everything in global CLAUDE.md costs tokens whether relevant or not ("lost in the middle" at scale)
- Knowledge propagation is manual: meta discovers something → writes to MEMORY.md → manually propagates to global/project CLAUDE.md. Slow, error-prone, creates version skew.
- To leverage meta's knowledge in another project, user must cd into meta, analyze, cd back. No programmatic access.

Evidence of cross-repo reach (last week):
- Session-analyst diagnosed intel sycophancy (105 tasks, 145 spin events) → wrote rules + deployed hook
- Planned/validated selve→genomics split (116 scripts)
- Designed 11+ hooks in meta, deployed globally
- Directed intel skill restructuring via cross-model review
- Supervision audit: 68 sessions analyzed, deployed fixes globally
- Auto-overview trigger: meta-designed, multi-project impact

## THE PROPOSAL

Build a FastMCP v3 server in meta that exposes accumulated knowledge as MCP tools.

Architecture:
- FastMCP v3 (already running in papers-mcp with 11 tools, pattern proven)
- stdio transport via `uv run --directory /path/to/meta meta-mcp`
- Tools: search_knowledge, get_hook_design, get_failure_modes, get_prompt_guidance, get_architecture_decision
- Backed by actual meta files (parsed at startup via lifespan)
- Added to each project's .mcp.json

What moves behind MCP (on-demand):
- Hook design patterns and inventory (11+ hooks, events table, design principles)
- Agent failure modes (22 documented)
- Improvement-log findings
- Cross-project architecture decisions
- Prompt format research
- Search/retrieval architecture decisions
- Session forensics patterns

What stays in global CLAUDE.md (always-loaded):
- Behavioral rules (communication, pushback)
- Git workflow (commits, trailers, no branches)
- Environment (uv, python3, DuckDB)
- Context management (compaction, plans)

Portability argument: .mcp.json travels with the repo (checked in), making the dependency explicit. Global CLAUDE.md doesn't travel at all.

## QUESTIONS FOR REVIEW

1. Is MCP the right abstraction? vs .claude/rules/ files, emb search, thicker per-project CLAUDE.md
2. What's the right partition between always-loaded and on-demand?
3. Tool granularity: few broad tools or many specific ones?
4. Does the portability argument hold? Or is it worse (now need running server)?
5. Alternative architectures not considered?
6. Failure modes: when does this make things worse?
7. Cost-benefit: is this worth building given the current project scale (1 human, 6 repos)?

## EXISTING PATTERNS

papers-mcp: 11 tools, lifespan pattern, FastMCP 3.0.2, returns dicts
intel intelligence_mcp: bare mcp package, single-file, no lifespan, graceful degradation
Both use stdio transport configured in .mcp.json
