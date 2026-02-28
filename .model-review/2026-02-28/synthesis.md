# Cross-Model Review: Search MCP Design Plan
**Mode:** Review (critical)
**Date:** 2026-02-28
**Models:** Gemini 3.1 Pro, GPT-5.2
**Constitutional anchoring:** Yes (CONSTITUTION.md, GOALS.md)

## Verified Findings (adopt)

| Finding | Source | Verified How |
|---------|--------|-------------|
| Router can't check corpus size but CAG routing needs it | GPT + Gemini | Confirmed: `classify_query(query: str)` has no index metadata; architecture doc uses corpus size for routing |
| `add_index()` invalidates FTS cache — don't use for dynamic merging | Gemini | Confirmed: search.py:280 sets `self._fts_db = None` |
| Cross-index scores not comparable if different embedding models used | GPT | Confirmed: no model enforcement in SearchEngine; merge warns but search doesn't |
| No thread safety in SearchEngine | Gemini | Confirmed: no locks anywhere; shared `_embedding_model` instance |
| Provenance fields insufficient for "Every Claim Sourced and Graded" | Both | Plan only mentions `source`; missing `index`, `doc_id`, `chunk_id`, `source_uri` |
| CAG in v1 is negative EV unless ≥2 weekly synthesis workflows exist | Both | GPT: 8-20hr build, <20 calls/week → 3-6 week payback IF quality holds |
| Merged ranking needs RRF, not global score sort | GPT | Correct: cosine similarities from different indexes are not on same scale even with same model |

## Where I (Claude) Was Wrong

| My Original Claim | Reality | Who Caught It |
|-------------------|---------|--------------|
| `search_all` merges results across indexes | Can't use `add_index()` for this — it invalidates FTS | Gemini |
| Router heuristic selects CAG based on query intent | CAG decision actually needs corpus size, not just query text | GPT + Gemini |
| 4 tools (search, get_content, indexes, ask) | `ask` should be deferred — adds complexity for unproven use case | Both |
| `strategy="auto"` with heuristic router | Heuristic has systematic edge case failures (quoted+synthesis, IDs in questions) | GPT enumerated 5 failure patterns |

## Gemini Errors (distrust)

| Claim | Why Wrong/Overstated |
|-------|---------------------|
| "Make `strategy` a required Enum, no `auto`" | Overly rigid. Auto with override + logging is pragmatically correct for a personal project. Gemini's own blind spot section acknowledges "LLMs might just default to hybrid for everything" — the router helps. |
| "CAG violates Principle 7 (provenance)" | Technically true but overstated — papers-mcp already runs CAG and user accepts it. The real issue is whether non-paper CAG is needed NOW, not whether it's epistemically pure. |
| Temperature override warning (0.3 → 1.0) | Gemini 3.1 Pro locks temperature — expected; doesn't affect review quality. |

## GPT Errors (distrust)

| Claim | Why Wrong/Overstated |
|-------|---------------------|
| "Add `search(mode='pros_and_cons')`" and "`search(intent='disconfirm')`" | Scope creep. This is retrieval, not reasoning. The agent handles disconfirmation logic. |
| "Add `indexes_manifest.json` with build timestamps, source snapshots, embedding model version" | Over-engineering for personal project. Index metadata already contains this info. |
| "`search(diversity=True)` to reduce cherry-picking" | Nice idea but not a v1 concern. MMR or diversity reranking is a separate feature. |
| Usage estimates (30-100 searches/day) | Fabricated — no data on actual usage patterns yet. |

## Revised Plan

### Scope: v1 = 3 tools, no CAG

| Tool | Keep/Cut | Rationale |
|------|----------|-----------|
| `search` | **Keep** | Core value. Primary reason to build this. |
| `get_content` | **Keep** | Agent decision point between search and full read. |
| `indexes` | **Keep** | Discovery before search. |
| `ask` (CAG) | **Cut from v1** | Both models agree: unproven use case, high complexity. Re-add when ≥2 weekly synthesis workflows exist for non-paper content. |

### Architecture Changes

1. **Per-index search, RRF fusion (not `add_index()` merging):**
   - Each index gets its own SearchEngine instance
   - Multi-index search: query each separately, fuse with RRF
   - Avoids FTS cache invalidation entirely

2. **Router gets index metadata:**
   ```python
   def classify_query(query: str, corpus_tokens: int | None = None) -> str:
   ```
   - Still heuristic, but corpus-aware
   - Agent can override with `strategy=` parameter

3. **Thread safety:**
   - `asyncio.Lock()` per SearchEngine instance for `_encode_query()`
   - Or: share one embedding model across all engines with a global lock

4. **Structured provenance in results:**
   ```python
   {
       "id": str,
       "index": str,          # which index this came from
       "source": str,
       "title": str,
       "date": str,
       "text": str,           # truncated
       "score": float,        # RRF-fused rank score
       "metadata": dict,
   }
   ```

5. **Multiple index directories:**
   - `SEARCH_INDEX_DIR` as colon-separated paths
   - No forced convention; discover from wherever indexes already live

6. **Query + response logging:**
   - Log `(timestamp, query, strategy_chosen, indexes_searched, latency_ms, result_count)`
   - Enable offline eval later without building a full harness now

### Implementation Order (revised)

1. `engine.py` — EnginePool with per-index SearchEngine, mtime invalidation, asyncio.Lock
2. `server.py` — FastMCP with `search` (RRF cross-index) + `indexes`
3. `get_content` tool
4. `router.py` — corpus-aware heuristic with `strategy=auto|dense|bm25|hybrid`
5. Query logging
6. Tests (router classification, search integration, thread safety)
7. Wire into `.mcp.json` for intel and selve

### Dependencies (simplified)

```toml
[project]
dependencies = [
    "fastmcp>=2.0",
    "emb",
]
# No litellm — CAG deferred
```

### Open Questions Resolved

| Question | Decision | Reasoning |
|----------|----------|-----------|
| Merge across indexes by default? | Yes, but RRF fusion not score sort | GPT: RRF is robust; include `index` field so agent can filter |
| Router configurable per-index? | Yes, minimal hints in metadata | `{preferred_strategy, supports_rerank}` |
| CAG in v1? | No | Both models agree; defer until concrete weekly use case |
| Index directory convention? | Colon-separated `SEARCH_INDEX_DIR` | GPT: don't force migration; support multiple dirs |
