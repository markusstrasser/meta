# Vendor Sweep — 2026-04-07

**Window:** 2026-04-01 to 2026-04-07
**Sources:** GitHub API (releases), Brave, Perplexity, vendor changelogs
**Baseline:** `scripts/vendor-versions.py` run 2026-04-07 20:34 UTC

---

## Codex CLI (OpenAI)

| Field | Value |
|-------|-------|
| Installed | 0.118.0 |
| Latest stable (npm) | 0.118.0 |
| Latest alpha | 0.119.0-alpha.16 (2026-04-07, very active — 16 alphas in ~1 week) |
| Released | 2026-03-31 |

### Notable changes in 0.118.0 (released March 31, since last scout)

- **Dynamic bearer token auth** for custom model providers — short-lived tokens, not just static creds (#16286-16288). Relevant if llmx ever routes through codex as transport.
- **`codex exec` stdin piping** — can now pipe input + separate prompt (#15917).
- **ChatGPT device-code login** for app-server clients (#15525).
- **Windows sandbox proxy networking** with OS-level egress rules (#12220).
- TUI fixes: hook notification replay, `/copy`, `/resume <name>`, agent picker, skills picker pagination.
- MCP robustness: longer startup window, failed handshakes now surface warnings.
- **Process hardening removed** (upstream #8951) — simplifies bash execution.
- Legacy TUI split removed (#15922).

### 0.119.0-alpha signals (Rust rewrite continues)

- 16 alpha releases in 6 days — heavy development.
- `codex-tools` extraction ongoing: MCP schema adapters, dynamic tool adapters, named tool definitions, Responses API tool models, discovery tool specs. This is a major refactoring of tool infrastructure into standalone crates.
- Named tool definitions and discoverable tool models suggest convergence toward a plugin/skill-like architecture.

### Breaking changes affecting llmx

**None.** 0.118.0 is backward-compatible. The Rust rewrite (0.119) is alpha-only. No API-level changes that break our `codex` transport.

---

## OpenAI API

| Field | Value |
|-------|-------|
| Python SDK | 2.30.0 (installed) |
| OpenAI Agents SDK | 0.13.5 (installed) |

### Changes since April 1

- **GPT-4.1 deprecation approaching** — Azure: deprecation 2026-04-14, retirement 2026-10-14. Replacement: `gpt-5`. Direct API (non-Azure) has not announced specific date but GPT-4o API access ended Feb 16.
- **ChatGPT in Apple CarPlay** (April 2) — consumer, not API.
- **GPT-5.4 mini** rolled out as rate-limit fallback for GPT-5.4 Thinking (March 18). Not a new API model, but may appear in responses if hitting limits.

### No new API models since April 1

The official changelog at platform.openai.com shows no new API features or models in April 2026. Last API update was January 2026 (Open Responses spec, gpt-5.2-codex).

### Breaking changes affecting llmx

**None immediate.** GPT-4.1 deprecation on April 14 is relevant if any fallback paths use it (they don't — we use gpt-5.4 and gpt-5.3-codex). No action needed.

---

## Gemini CLI (Google)

| Field | Value |
|-------|-------|
| Installed | 0.36.0 |
| Latest stable (npm) | 0.36.0 |
| Latest preview | 0.37.0-preview.2 (2026-04-07) |
| Nightly | 0.36.0-nightly.20260407 |

### v0.37.0-preview.0 highlights (massive release, ~100 PRs)

**New features:**
- **Subagent isolation and cleanup hardening** (#23903) — better subagent lifecycle
- **Dynamic Linux sandbox expansion + worktree support** (#23692) — git worktree-aware sandboxing
- **Windows sandbox dynamic expansion** Phase 1+2 (#23691, #24027)
- **forbiddenPaths** for OS-specific sandbox managers (#23282, #23936)
- **Secret visibility lockdown** for env files (#23712)
- **Persistent browser session management** (#21306)
- **Tool-based topic grouping (Chapters)** (#23150) — conversation organization
- **Compact tool output** (#20974) — reduced token usage from tool responses
- **Tab to queue messages while generating** (#24052)
- **Gemini Flash 3.1 Lite** support (experiment-gated) (#23794)
- **Project-level memory scope** for save_memory tool (#24161)
- **Plan mode in untrusted folders** (#17586)
- **Mid-stream retries for all models** (#24302)
- **Unified Context Management and Tool Distillation** (#24157)
- **CI skill** for automated failure replication (#23720)
- **Configurable memoryBoundaryMarkers** setting (#24020)
- **A2A/ACP improvements** — remote agent inline card support, attachment permissions
- **TTY hang fix** in headless environments (#23673) — relevant for our non-interactive dispatch

**Bug fixes relevant to us:**
- Dynamic model routing for Gemini 3.1 Pro to customtools model (#23641)
- Shell tool heredoc fix via subshells (#24024)
- SessionEnd no longer fires twice in non-interactive mode (#22139)

### Breaking changes affecting llmx

**Watch:** 0.37.0 is preview only. When it goes stable, the "compact tool output" and "unified context management" features may change how tool responses are formatted/compressed. The mid-stream retry behavior change could affect error handling in our fallback logic. No immediate action — we're on 0.36.0 stable.

---

## Google GenAI SDK (Python)

| Field | Value |
|-------|-------|
| Installed | 1.70.0 |
| Latest (PyPI) | 1.70.0 |
| Released | 2026-04-01 |

### v1.70.0 (April 1)

- **TextAnnotationDelta for streaming** tool responses — new dedicated type for streaming annotations.
- **Fix service_tier enums** — relevant: this is the Flex/Priority tier enum fix.

### Gemini API platform changes (April 1-2)

- **Flex and Priority inference tiers launched** (April 1):
  - **Flex**: lower priority, ~50% discount, synchronous (same API call), requests may be preempted during traffic spikes. Replaces the old Batch API discount model for non-interactive work.
  - **Priority**: guaranteed low-latency, available to Tier 2/3 paid projects, graceful degradation to Standard on overload.
  - **Standard**: unchanged default.
  - These are set via the existing `service_tier` field in API requests.
- **Gemma 4 models** released (April 2): `gemma-4-26b-a4b-it` and `gemma-4-31b-it` on AI Studio + API.
- **Vertex AI SDK deprecation reminder**: `google-cloud-aiplatform` generative modules sunset June 24, 2026. Migrate to `google-genai`.

### Breaking changes affecting llmx

**ACTION NEEDED:** The `service_tier` enum fix in v1.70.0 confirms the Flex/Priority tiers are now properly supported in the SDK. Our CLAUDE.md already documents Flex tier for non-interactive dispatch. Verify that llmx passes `service_tier: "flex"` correctly with the updated enum values. The old workaround (if any) should be validated against the new enum.

---

## Summary: Action Items

| Priority | Item | Scope |
|----------|------|-------|
| **Verify** | Flex tier `service_tier` enum in llmx — v1.70.0 fixed enums | llmx |
| **Watch** | Gemini CLI 0.37.0 preview — compact tool output, unified context mgmt | llmx gemini transport |
| **Watch** | Codex CLI 0.119.0 alpha — tool infrastructure refactoring | codex transport |
| **Note** | GPT-4.1 API deprecation April 14 (Azure) — no impact on our models | none |
| **Note** | Gemma 4 models available — not used in our infrastructure | none |
| **Upgrade** | Gemini CLI to 0.37.0 when it reaches stable | gemini-cli |

## No Breaking Changes Detected

Nothing in the April 1-7 window breaks our current llmx transport layer. All tools remain at their installed versions as latest stable. The Flex/Priority tier launch is the most operationally significant change — we already reference Flex in our routing rules and should confirm the SDK enum is correct.
