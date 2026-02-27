# Claude Code Architecture: Research Notes

**Date:** 2026-02-27
**Sources:** Anthropic engineering blog, claude-code-docs bundle, Trail of Bits config, incident.io blog, decodeclaude.com, community posts, 50+ GitHub repos (99%+ slop filtered out)

---

## The Mental Model

Claude Code is a **context-limited agent**. Every design decision flows from one constraint: the context window is finite and recall degrades as it fills. The entire architecture — rules, skills, hooks, subagents, MCP — exists to manage what's in the window at any given moment.

**Progressive disclosure** is the organizing principle:
- CLAUDE.md: always loaded (~200 lines max, every line costs every turn)
- `.claude/rules/`: path-scoped, loaded only when relevant files are active
- `.claude/skills/`: on-demand, loaded only when invoked
- Hooks: deterministic, zero context cost (run outside the model)
- Subagents: isolated context windows, return 1-2K token summaries
- MCP servers: external tools, schema consumes context on first use

## What Anthropic Actually Does Internally

### Context Engineering (Sep 2025 blog)
- **Context rot is continuous, not a cliff.** Recall accuracy degrades as token count increases. n-squared pairwise relationships stretch thin.
- **Microcompaction**: Tool outputs (Read, Bash, Grep, etc.) go from "hot tail" (recent, inline) to "cold storage" (disk-referenced). Only the 5 most recently accessed files get re-read after compaction.
- **"If a human engineer can't definitively say which tool should be used, an AI agent can't either."** Bloated tool sets are worse than no tools. Limit MCP servers to 2-3 active.

### Long-Running Agents (Nov 2025 blog)
- **Two-agent architecture**: Initializer creates `init.sh` + `claude-progress.txt` + baseline git commit. Coding agent reads these on every new session. No fancy memory — just files and git.
- **Feature list as JSON with `passes` boolean**: Agents can only flip the flag, never delete features. Prevents premature "done" declarations.
- **One-shotting is the core failure mode**: Agents exhaust context mid-feature, leave undocumented half-work. Fix: force incremental, documented progress.
- **Browser automation (Puppeteer MCP) caught bugs unit tests missed.** Without e2e, Claude marks features "complete" prematurely.

### Internal Usage Data (Dec 2025 study)
- **67% increase in merged PRs/engineer/day**. But 27% of Claude-assisted work is entirely new tasks that wouldn't have been done otherwise.
- **Skill atrophy is real.** Senior Anthropic engineers flagged it explicitly: "When producing output is so easy, it gets harder to actually learn."
- **Supervision paradox**: Using Claude well requires skills that atrophy from using Claude.
- **Claude replaced colleague questions.** Junior engineers stopped asking seniors. Mentorship decreased measurably.
- **Variable time savings**: Some engineers spend MORE time debugging Claude's output than writing it themselves.

## Compaction System Internals

Source: decodeclaude.com reverse engineering + docs bundle.

### Three layers:
1. **Microcompaction**: Tool output → disk. Hot tail (recent) stays inline, older outputs become file references.
2. **Auto-compaction**: Triggers at ~64-75% context usage (not 90% as previously assumed). Reserves buffer for both output AND the compaction workflow itself.
3. **Manual**: `/compact` command.

### Compaction contract (what the summary MUST include):
- User intent (what are we trying to accomplish)
- Technical decisions made
- Files touched (read and modified)
- Errors encountered
- Pending tasks
- Next steps

### Rehydration sequence after compaction:
1. Boundary marker
2. Compressed summary
3. Re-read 5 most recently accessed files
4. Todo list state
5. Plan state
6. Hook outputs

### Key insight (hyperdev.matsuoka.com):
Recent Claude Code performance improvements may come from **reserving more free context for reasoning** rather than better models. When Claude Code reported 10% remaining, independent measurement showed 36% free. The "completion buffer" prevents disruptive mid-operation compaction.

## Hook System

### Three execution types:
1. **Command** (`type: "command"`): Shell script. Fast, deterministic. Exit 0 = proceed, exit 2 = block + feed error back.
2. **Prompt** (`type: "prompt"`): Single Haiku LLM call. Good for fuzzy classification (is this command destructive?).
3. **Agent** (`type: "agent"`): Subagent with tool access, 60s timeout. Full reasoning but expensive.

### Hook events:
- `PreToolUse` / `PostToolUse`: Before/after any tool call. Matcher regex on tool_name.
- `Notification`: On events like context window warnings.
- `Stop`: When Claude thinks it's done. Exit 2 = "no you're not, keep going."
- `SubagentStop`: When subagent completes.

### Non-obvious patterns (Marco Patzelt, Feb 2026):

**PreCompact backup hook**: Save full transcript to timestamped files before auto-compaction. Context is otherwise irreversibly lost.
```json
{
  "event": "PreCompact",
  "type": "command",
  "command": "cp $CLAUDE_TRANSCRIPT ~/.claude/transcripts/$(date +%s).json"
}
```

**Tool input modification**: PreToolUse hooks can silently rewrite command arguments. Force `--dry-run` on destructive operations, redirect paths to sandboxes, redact secrets. Claude sees the original; the modified version runs.

**Anti-rationalization Stop hooks**: Use a fast model (Haiku) to evaluate whether Claude is rationalizing premature completion. Relevant for any adversarial/investigation workflow.

**Async hooks** (`"async": true`, Jan 2026): Run backgrounded without blocking. No deduplication. Good for test suites and CI triggers, cannot block behavior.

## Skills Architecture

### What makes a good skill:
- **Progressive disclosure**: Metadata (~50 tokens) always loaded. Instructions (~200-500 tokens) on activation. Resources (examples/templates) on reference.
- **$ARGUMENTS injection**: Skill receives user arguments as template variable.
- **`allowed-tools`**: Restrict skills to read-only tools for safety.
- **SkillsBench finding**: Self-generated skills = 0% improvement. Curated human-authored = +16.2%.

### Skills vs Subagents vs MCP (decision framework, Ryan Smith):
| | Context Cost | Portability | Best For |
|---|---|---|---|
| **Skills** | 70-90% savings via progressive loading | Works across all Claude products | Workflows, methodologies, templates |
| **Subagents** | ~70% savings via context filtering | Claude Code only | Parallel research, isolated exploration |
| **MCP** | Highest (schema loaded upfront) | Claude Code only | External data, APIs, stateful services |

**Critical insight**: "Claude becomes dumber after compacting when extensive exploration stays in main conversation." Deploy subagents early, even for moderately complex tasks. The exploration stays in the subagent's window; only the summary enters yours.

## Agent Teams

Beyond subagents. Full peer-to-peer collaboration.

### 7 primitives:
TeamCreate, TaskCreate, TaskUpdate, TaskList, Task (spawn teammate), SendMessage, TeamDelete. All map to filesystem operations. File locking prevents double-claiming.

### Cost reality (Alexander Opalic, Feb 2026):
- Solo session: ~200K tokens
- 3 subagents: ~440K tokens
- 3-person team: ~800K tokens

Teammates are full context windows. Linear cost scaling. **Teammates do NOT inherit lead's conversation history** — only project context via CLAUDE.md.

### Effective pattern:
- Run `/plan` at ~10K tokens to produce breakdown
- Hand approved plan to team lead
- Planning checkpoint prevents expensive mid-swarm course corrections
- Mixed model strategy: Sonnet for teammates, Opus for lead

## Security (Trail of Bits, Feb 2026)

**Stars:** 1,202. Most security-conscious public config.

- **Project MCP servers disabled by default** (`enableAllProjectMcpServers: false`). Cloning a repo with malicious `.mcp.json` could execute arbitrary code.
- **Credential blocklists**: SSH, AWS, Docker, npm, kubeconfig, crypto wallet paths.
- **Hook-based `rm -rf` prevention**: Suggests `trash` instead.
- **Mutation logging**: Hooks classify every shell command as read/write and log to `~/.claude/bash-commands.log`.
- **Local model fallback**: Qwen3-Coder-Next (80B MoE, 3B active) via LM Studio with Anthropic-compatible endpoint.

## Best GitHub Repos (filtered from 99%+ slop)

| Repo | Stars | Why it matters |
|---|---|---|
| **trailofbits/claude-code-config** | 1,202 | Security-first config with anti-rationalization hooks |
| **wshobson/agents** | 29,531 | 112 agents across 72 plugins. Three-tier model strategy (Opus/Sonnet/Haiku by task type) |
| **affaan-m/everything-claude-code** | 51,900 | Kitchen-sink reference. Anthropic hackathon winner. Catalog, not template. |

## Parallel Development (incident.io, Jun 2025)

Real production team running 4-7 parallel Claude agents simultaneously:
- Custom `w` bash function for worktree management with auto-completion
- Voice-driven development via SuperWhisper for complex specs
- Plan Mode as psychological safety — teams leave Claude running without worrying about unauthorized changes
- **Claude overestimates its own work duration**: Estimated 2 hours for a task completed in 10 minutes

## Brad Feld's Configuration

Most sophisticated solo-developer setup found:
- **Session state as process memory**: `.claude-session/*.json` files survive context compaction. Include `blockedActions` array enforcing workflow mid-session. Circuit breaker blocks `git commit` if status = `awaiting_user_test`.
- **Deterministic port allocation**: `PORT = 3000 + (worktree * 10) + app_slot` for 8 concurrent worktrees.
- **MCP Tool Search as lazy loading**: Instead of all MCP schemas upfront, `ToolSearch({ query: 'linear issues' })` loads tools on-demand.

## Design Principles Summary

1. **Context is your scarcest resource.** Every token in the window competes with reasoning capacity. Minimize always-loaded content.
2. **Progressive disclosure > monolithic instructions.** CLAUDE.md → rules → skills → subagents. Load what's needed when it's needed.
3. **Hooks are free.** They run outside the model. Use them for deterministic enforcement (formatting, security, workflow gates).
4. **Subagents protect the main window.** Exploration-heavy tasks should be delegated early. The summary is cheaper than the exploration.
5. **Git is the memory system.** Not databases, not vector stores. Files + commits + diffs. Anthropic's own long-running agents use this pattern.
6. **Compaction is lossy.** Design around it: backup transcripts, use session state files, keep critical context in files the model will re-read.
7. **SkillsBench: human-authored skills work, self-generated don't.** Invest in writing good skills. Don't let Claude write its own.
8. **Two-agent architecture for multi-session work.** Initializer writes plan + progress file. Worker reads and continues. No state beyond files.
9. **Anti-rationalization is a real failure mode.** Stop hooks that evaluate completion claims catch premature "done" declarations.
10. **Security by default.** Disable project MCP servers, blocklist credentials, log mutations, prefer `trash` over `rm`.
