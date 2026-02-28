# Improvement Log

Findings from session analysis. Each tracks: observed → proposed → implemented → measured.
Source: `/session-analyst` skill analyzing transcripts from `~/.claude/projects/`.

## Findings
<!-- session analyst appends below -->

### [2026-02-28] TOKEN WASTE: Iterative regex parsing via repeated Bash one-liners
- **Session:** intel 16552a95
- **Evidence:** 9 reads of `setup_duckdb.py`, 6 separate `python3 -c "import re..."` Bash commands to iteratively test regex parsing of view names from Python source. Each attempt failed, requiring a new iteration with slightly modified regex.
- **Failure mode:** Token waste — iterative debugging via tool calls instead of writing a script
- **Proposed fix:** CLAUDE.md change: "When extracting structured data from Python source, use `ast` module or write a standalone script. Never iterate regex via inline Bash one-liners."
- **Status:** [x] implemented — global CLAUDE.md rule (2026-02-28)

### [2026-02-28] OVER-ENGINEERING: Regex parsing of Python source instead of AST
- **Session:** intel 16552a95
- **Evidence:** Agent used complex regexes with line-lookaheads and paren-counting to extract view names and directory paths from `setup_duckdb.py` f-strings. Repeatedly failed on edge cases. The `ast` module or simply importing the file's data structures would have been simpler and correct.
- **Failure mode:** Over-engineering — fragile approach when robust alternative exists
- **Proposed fix:** CLAUDE.md change: "Prefer `ast` module or direct import over regex when parsing Python source code."
- **Status:** [x] implemented — global CLAUDE.md rule (2026-02-28)

### [2026-02-28] TOKEN WASTE: Repeated find commands instead of saving to temp file
- **Session:** intel deb3fac6
- **Evidence:** 9 `find /Volumes/SSK1TB/corpus/` commands with minor variations (`wc -l`, `sed`, `stat`, `printf`) instead of saving the file list to `/tmp/` once and processing it. Each re-traverses 6,031 files.
- **Failure mode:** Token waste — filesystem re-traversal
- **Proposed fix:** rule: "Save `find`/`ls` output to `/tmp/` file when you need multiple passes over the same listing."
- **Status:** [x] implemented — global CLAUDE.md rule (2026-02-28)

### [2026-02-28] SYCOPHANCY: No pushback on "ALWAYS BE DOWNLOADING" bulk hoarding directive
- **Session:** intel f32653c6
- **Evidence:** User said "DO NOT STOP, ALWAYS BE DOWNLOADING." Agent immediately complied, spawning 105+ task dispatches and 123 inline Python download scripts across 13 context continuations. No discussion of: data quality, schema alignment, storage cost, API rate limits, or whether the downloaded datasets had integration plans. Session burned through context 13 times and hit usage limits 145 times.
- **Failure mode:** Sycophancy — compliance with directive that warranted pushback
- **Proposed fix:** rule: "Pushback required when download requests lack integration plan. Ask: What view will this create? What entity does it join to? If no answer, deprioritize."
- **Severity:** high
- **Status:** [x] implemented — intel CLAUDE.md "Download Discipline" section (2026-02-28). Instructions-only; acknowledged weakness per EoG.

### [2026-02-28] TOKEN WASTE: 123 inline Python scripts via Bash instead of writing .py files
- **Session:** intel f32653c6
- **Evidence:** 123 `Bash: uvx --with requests python3 -c "import requests, os..."` one-liners for individual downloads instead of writing download functions to a `.py` file. 496 total Bash calls in the session. Each inline script wastes tokens on boilerplate and is not reusable.
- **Failure mode:** Token waste — inline scripts where file-based scripts would save tokens and be maintainable
- **Proposed fix:** CLAUDE.md change: "Multi-line Python (>10 lines) must go in a .py file, not inline Bash. Exception: one-shot queries."
- **Severity:** high
- **Status:** [x] implemented — global CLAUDE.md rule (2026-02-28)

### [2026-02-28] TOKEN WASTE: Polling failed tasks after hitting usage limits
- **Session:** intel f32653c6
- **Evidence:** 145 "out of extra usage" messages. Agent continued attempting to read task outputs and retry failed downloads instead of halting and informing the user. Burned tokens on identical failure loops.
- **Failure mode:** NEW: Usage-limit spin loop — agent keeps polling when API limits are hit
- **Proposed fix:** hook: Detect repeated usage-limit errors and halt with user notification instead of retrying.
- **Severity:** high
- **Status:** [x] partially implemented — PostToolUse:Bash hook (`posttool-bash-failure-loop.sh`) detects 5+ consecutive Bash failures. Deployed to intel (2026-02-28). Does NOT catch API-level usage limits (system messages, not tool outputs).

### [2026-02-28] BUILD-THEN-UNDO: Download scripts rewritten for broken URLs
- **Session:** intel f32653c6
- **Evidence:** `download_new_alpha_datasets.py` written, run, URLs found broken (FERC, USITC, PatentsView, FL Sunbiz, NRC), script edited, re-run, more broken URLs found, edited again. Pattern repeated across multiple download scripts.
- **Failure mode:** Build-then-undo — URL validation should precede bulk download script writing
- **Proposed fix:** architectural: HEAD-request validation step before writing download scripts. Already partially addressed in `data_sources.md` lessons.
- **Severity:** medium
- **Status:** [x] implemented — intel CLAUDE.md "Download Discipline" rule: validate URLs with HEAD before bulk scripts (2026-02-28)

### [2026-02-28] SYCOPHANCY: Built heuristic auto-classification rules without epistemic challenge
- **Session:** selve a2679f18
- **Evidence:** After user asked "what can we do now that's better?", agent proposed and immediately implemented 3 heuristic rules to auto-demote variants as LIKELY_BENIGN (HLA region, alt contigs, tolerant + AM benign). Only after user pushback did agent articulate why these were epistemically unsound: "HLA gene -> LIKELY_BENIGN is a population-level prior, not evidence about the specific variant. HLA genes *do* cause disease." Agent had the knowledge to pushback before building but didn't.
- **Failure mode:** Sycophancy — compliance without epistemic challenge on safety-critical classification
- **Proposed fix:** [rule] "Distinguish mechanistic vs. heuristic changes before implementing. Mechanistic (parser fix, known-good data source) can proceed. Heuristic (new classification rule based on correlation/prior) requires stating the false-negative risk and requesting confirmation."
- **Severity:** high
- **Status:** [ ] proposed

### [2026-02-28] BUILD-THEN-UNDO: Implemented and reverted heuristic auto-classification rules
- **Session:** selve a2679f18
- **Evidence:** Agent added `_is_alt_contig()`, `_is_tolerant_missense_benign()`, `_PRIMARY_CHROMS`, and modified `auto_classify()` to add 3 new LIKELY_BENIGN rules. After user pushback, all code was reverted and dead helpers cleaned up. The priority tiering function survived, but the filtering rules were wasted. Estimated ~4K output tokens on code that was deleted.
- **Failure mode:** Build-then-undo — direct consequence of missing pushback (above)
- **Proposed fix:** Same as above — epistemic challenge before building prevents the undo
- **Severity:** medium
- **Status:** [ ] proposed (linked to finding above)

### [2026-02-28] TOKEN WASTE: 4 consecutive Read calls on same 700-line file
- **Session:** selve a2679f18
- **Evidence:** Lines 132-146 of transcript show 4 back-to-back `Read(generate_review_packets.py)` calls before a single Edit. The file was already in context from the first Read. Later in the session, similar patterns appear: Read -> Edit -> Read -> Edit on the same file when content was already available.
- **Failure mode:** Token waste — redundant file reads
- **Proposed fix:** [architectural] Before issuing Read, check if the file content is already in recent context. Use Grep for targeted lookups instead of full file reads when only checking a specific function or line.
- **Severity:** medium
- **Status:** [ ] proposed

### [2026-02-28] RULE VIOLATION: Committed code without explicit user request
- **Session:** selve a2679f18
- **Evidence:** Agent committed at multiple points ("git add ... && git commit") without the user explicitly asking for commits. The user provided a plan and said "Implement the following plan" — the agent interpreted this as license to commit at each phase boundary. While the branch workflow in CLAUDE.md says "Git commit changes (semantic, granular)" when done, the global rule says "NEVER commit changes unless the user explicitly asks." The agent auto-committed 5+ times during implementation.
- **Failure mode:** Rule violation — auto-committing without explicit request
- **Proposed fix:** [rule clarification] The branch workflow instruction ("commit changes") and the global "never commit unless asked" are in tension. Resolve: branch workflow implicitly authorizes commits when user requests branch-based implementation.
- **Severity:** low (commits were well-structured and appropriate for branch workflow)
- **Status:** [ ] proposed — may be a false positive given branch workflow context
