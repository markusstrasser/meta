ℹ Starting chat {"provider": "google", "model": "gemini-3.1-pro-preview", "stream": false, "reasoning_effort": null}
⚠ Temperature override ignored: gemini/gemini-3.1-pro-preview only supports temperature=1.0 {"requested": 0.3, "using": 1.0}
## 1. Where the Analysis Is Wrong

*   **The Router Architecture:** The plan relies on a heuristic `classify_query` (e.g., `len(query.split()) <= 3 -> hybrid`) to hide the search strategy behind `strategy="auto"`. This is brittle. "FDA FAERS trajectory" is 3 words but requires semantic dense search, not hybrid/BM25. "NPI 1234567890" is 2 words and requires strict BM25. Masking this from the agent prevents the agent from correcting its own retrieval errors.
*   **Dynamic Index Merging:** The plan suggests `search_all` across indexes. However, the existing `emb` API notes show `add_index()` "invalidates FTS cache" and merges into the current engine. If the `EnginePool` dynamically merges indexes per request based on the `indexes` parameter, it will constantly trigger FTS rebuilds and destroy the ~50ms latency. 
*   **Memory Footprint Assumption:** The existing `emb` library loads the entire index (entries + numpy embedding arrays) into memory, plus a 149M parameter ModernBERT model and a 0.6B parameter reranker. An `EnginePool` that lazy-loads but doesn't unload multiple distinct indexes will quickly blow up the RAM on a local machine, causing swap thrashing.
*   **Thread Safety:** The `emb` API notes explicitly state: *"Not thread-safe by default for embedding model"*. FastMCP handles requests asynchronously. If the agent fires off parallel searches (e.g., searching 3 different indexes simultaneously), the underlying embedding model will likely crash or block unpredictably.

## 2. What Was Missed

*   **Provenance Truncation:** The `emb` search returns text truncated to 300 characters. The Constitution mandates: *"Every Claim Sourced and Graded"*. A raw 300-character middle-slice of a document might strip the source grade (e.g., `[A1]`, `[DATA]`) located at the top or bottom of the file. The MCP must guarantee that index name, original file source, and any metadata/grades are explicitly appended to the snippet payload.
*   **Query Expansion / Contextualization:** The architecture research notes that `emb` already implements Anthropic's contextual retrieval (`emb contextualize`). But the MCP plan doesn't expose whether it searches the raw chunks or the contextualized chunks.
*   **Error Handling for Missing Indexes:** The plan relies on `mtime` for cache invalidation. It misses the scenario where an index is deleted or corrupted by an external `emb` CLI process while the MCP is running.

## 3. MCP vs Skill vs Subagent

*   **For Retrieval (`search`, `get_content`, `indexes`):** MCP is the exact right abstraction. MCP is designed to expose data systems to an LLM without polluting the LLM's system prompt with integration code. It treats the local embedding store as a standard database.
*   **For Synthesis (`ask` / CAG):** MCP is the **wrong** abstraction. Calling an LLM (Gemini) from inside a tool used by another LLM (Claude) creates an opaque subagent. It violates Principle 7 ("The reasoning chain must show its sources"). The main agent gets a summarized narrative back and cannot verify the citations or source grades because the context was stuffed into Gemini, not Claude. 
*   **Alternative:** Retrieval should be an MCP. Synthesis (if Gemini's 1M context is required for cost/size) should be a dedicated Subagent or a Claude Code Skill where the system prompt explicitly enforces the "Skeptical but Fair" and "Quantify Before Narrating" rules.

## 4. Tool Granularity Assessment

Applying the existing ecosystem rule: *"Split a tool if there is a decision the agent should make between steps. Merge if the steps always execute together."*

*   **`indexes`**: Keep. The agent must decide what domain to target.
*   **`search` vs `get_content`**: Keep split. This is correct. The agent reads 10 snippets and makes a deliberate decision about which 2-3 are worth spending context window tokens on to read in full.
*   **`search` index targeting**: The plan asks if it should merge results across all indexes by default. **No.** Do not merge by default. Force the agent to select indexes. If you merge git commits, papers, and chat history by default, the reranker will struggle to compare semantic relevance across entirely different ontological domains.
*   **`ask`**: Remove entirely from this MCP (see Section 6).

## 5. Router Design

The heuristic router should be scrapped. 

The Constitution states: *"Instructions alone = 0% reliable. Prefer architectural enforcement."* If you want the agent to use the right search strategy, force it to declare its intent.

Make `strategy` a required `Enum` parameter (`dense`, `bm25`, `hybrid`). Do not offer `auto`. 
If the agent searches for a specific NPI number using `dense` and fails, it will receive an empty result, realize its error, and retry with `bm25`. This exercises the **Generative Principle** (maximizing error correction). An opaque heuristic router steals the agent's ability to learn how the database behaves and prevents it from executing precise, intentional queries.

## 6. CAG Placement

**CAG should NOT live in the Search MCP.**

1.  **Dependency Bloat:** Adding `litellm`, Gemini API keys, and LLM orchestration to a fast, local, offline vector search server pollutes the operational boundary. Search MCP should only depend on `emb` and `fastmcp`.
2.  **Epistemic Opacity:** If the agent uses `ask`, it delegates the synthesis to a cheaper, smaller model (Flash-Lite) without seeing the raw text. This violates "Falsify Before Recommending" and "Every Claim Sourced and Graded" because the primary reasoning engine (Claude) is taking a summary on blind faith.
3.  **Refactoring:** Leave `cag.py` in `papers-mcp` for now. If cross-domain synthesis becomes a verified bottleneck, create a dedicated `synthesis-skill` that takes a list of document IDs, fetches them via Search MCP, and runs the Gemini call with strict prompt engineering aligned to the Constitution.

## 7. Constitutional Alignment

*   **Passes - "The Join Is the Moat":** Exposing all `emb` indexes to the agent allows cross-domain signal fusion (e.g., matching a DOJ press release index with an SEC filings index).
*   **Passes - "Fast Feedback":** ~50ms local search provides immediate operational feedback to the agent's query formulations.
*   **Violates - "The Autonomous Decision Test":** The heuristic `strategy="auto"` router makes decisions *for* the agent, making the agent less informed about why a query returned specific results.
*   **Violates - "Honest About Provenance":** Returning truncated strings without hardcoding the injection of the source file, source grade, and index name into the `text` field will lead to unsourced assertions entering the entity files.

## 8. What I'd Prioritize Differently

1.  **Remove `ask` and all CAG code:** Drop `litellm` and Gemini dependencies. Keep the MCP strictly focused on sub-100ms byte retrieval. *(Verification: `pyproject.toml` contains only `fastmcp` and `emb`)*.
2.  **Make `strategy` explicitly required:** Delete `router.py`. Force the agent to choose `dense`, `bm25`, or `hybrid` in the tool schema. *(Verification: Tool call fails if `strategy` is omitted)*.
3.  **Require explicit index selection:** Remove "search all" defaults. Force the agent to call `indexes` first, then pass specific index names to `search`. *(Verification: `indexes` parameter in `search` has no default, and `EnginePool` does not attempt to merge incompatible FTS tables)*.
4.  **Enforce Provenance in Snippets:** Wrap the `emb` search return dict to prepend `[Index: {name} | Source: {source}]` to every 300-char text snippet. *(Verification: Every `search` result string explicitly contains its origin metadata)*.
5.  **Implement LRU Cache & Thread Locking in EnginePool:** Protect the non-thread-safe embedding model with an `asyncio.Lock()`, and only keep the 2-3 most recently used indexes in memory to prevent RAM exhaustion. *(Verification: Concurrent search requests do not crash the script, RAM usage remains stable during multi-index queries)*.

## 9. Blind Spots In My Own Analysis

*   **M-Series Mac Unified Memory:** I am assuming RAM constraints based on standard local environments. If this is running on an M3 Max with 128GB of unified memory, holding 20 numpy arrays and the reranker in RAM simultaneously might be completely fine, making my LRU cache warning overly pedantic.
*   **LLM Stubbornness:** I advocate forcing the agent to choose `strategy` manually. However, LLMs are notoriously lazy and might just default to `hybrid` for everything, wasting compute on reranking. The heuristic router *might* be a necessary evil to protect the system from the agent's own laziness.
*   **CAG Pragmatism:** I am applying strict epistemic purity (Principle 7) to remove CAG. But if the actual daily workflow involves summarizing 40 long documents, removing `ask` might force the human to manually copy-paste IDs into a different tool, violating the goal of a "fully autonomous research pipeline." I may be over-weighting architectural purity over workflow convenience.
