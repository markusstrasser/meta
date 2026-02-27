# Agent Infrastructure Maintenance Checklist

## When a New Model Ships (Claude, GPT, Gemini)

### 1. Update Model Guide
- [ ] Pull release notes / system card / technical report
- [ ] Fetch and read the actual paper (don't summarize from training data)
- [ ] Update `~/.claude/skills/model-guide/SKILL.md` with new model capabilities, pricing, known issues
- [ ] Update `memory/MEMORY.md` frontier model section if it changes our routing decisions
- [ ] Search for independent evals (not just provider self-assessments)

### 2. Update Claude Code Docs (Claude releases only)
- [ ] Check Claude Code changelog: `claude --version`, release notes
- [ ] Claude Code source is not public — read the docs instead
- [ ] Check for new hook types, skill features, MCP changes, settings options
- [ ] Update `~/.claude/skills/` with any new capabilities
- [ ] Update project `.claude/rules/` if new features change best practices
- [ ] Check if CLAUDE.md spec changed (new fields, frontmatter, etc.)

### 3. Cross-Agent Parity
Each project should have:
```
CLAUDE.md          ← canonical agent instructions
AGENTS.md -> CLAUDE.md   ← symlink for OpenAI Codex CLI
GEMINI.md -> CLAUDE.md   ← symlink for Google Gemini CLI
```

**Agent-specific config files:**
| Agent | Config | Instructions | Settings | Skills/Rules |
|-------|--------|-------------|----------|-------------|
| Claude Code | `.claude/` | `CLAUDE.md` | `.claude/settings.json` | `.claude/skills/`, `.claude/rules/` |
| Codex CLI | — | `AGENTS.md` | — | — |
| Gemini CLI | — | `GEMINI.md` | — | — |

The other two read the same instructions via symlink. They don't have hooks, skills, or rules — that's OK. The shared content (hard constraints, DuckDB, data, principles) works universally.

**Parity gaps (known):**
- Codex/Gemini have no equivalent of hooks (PreToolUse, Stop, PreCompact)
- Codex/Gemini have no equivalent of path-scoped rules
- Codex/Gemini have no equivalent of skills/slash commands
- MCP server config is Claude-specific (`.mcp.json`)
- These are real capability gaps, not just config differences

### 4. Research Sweep (Weekly)
- [ ] Search arxiv for last 7 days: "LLM agents", "coding agents", "tool use", "agentic AI"
- [ ] Search for Anthropic employee blog posts / personal setups
- [ ] Search for new papers on: agent evaluation, prompt engineering, CLAUDE.md patterns
- [ ] Check Trail of Bits, Simon Willison, Hamel Husain for agent security/best practices posts
- [ ] Check Kapoor/Narayanan (normaltech.ai) for reliability research updates
- [ ] Save interesting papers to corpus: `mcp__research__save_paper`
- [ ] Fetch + read key papers: `mcp__research__fetch_paper` + `read_paper`
- [ ] Export to selve: `mcp__research__export_for_selve` → `./selve update`
- [ ] Update `frontier-agentic-models.md` with significant findings
- [ ] **Use Exa for recency searches, not S2** (S2 has no date filtering)

### 4a. Papers Pending Save (2026-02-27 sweep)
- [ ] arXiv:2602.16666 — Princeton reliability (Kapoor/Narayanan/Rabanser). 14 models, 12 dimensions.
- [ ] arXiv:2601.17915 — EoG graph-guided investigation (IBM). 7x Majority@k gain. Table 3 = instructions alone fail.
- [ ] arXiv:2602.11224 — Agent-Diff state-diff evaluation. Documentation Hub vs Non-Hub experiment.
- [ ] arXiv:2601.06112 — ReliabilityBench. pass^k metric, chaos engineering for agents.

### 5. Skills Propagation
When updating a skill in `~/.claude/skills/` (user-level):
- [ ] Check if any project has a project-level override in `.claude/skills/`
- [ ] If so, decide: update the project version or delete it to inherit user-level
- [ ] Currently overridden in intel: `researcher`, `deep-research` (redirected), `competing-hypotheses`, `multi-model-review`, `thesis-check`, `new-dataset`, `commands`

## Project Setup for New Repos
```bash
# Create agent instruction symlinks
ln -sf CLAUDE.md AGENTS.md
ln -sf CLAUDE.md GEMINI.md

# Add to .gitignore
echo ".claude/" >> .gitignore

# Initialize Claude Code
mkdir -p .claude/rules .claude/skills
```

## Key URLs to Monitor
- Claude Code releases: `anthropic.com/claude-code` (no public changelog URL — check `claude --version`)
- Codex CLI: `github.com/openai/codex` (or wherever they publish)
- Gemini CLI: `github.com/google/gemini-cli` (or wherever they publish)
- Agent benchmarks: SWE-bench, BFCL, Terminal-Bench
- Security: Trail of Bits blog, OWASP LLM Top 10
