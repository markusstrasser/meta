# Storage-Cost-Reduction Dossier: personal + publishing

Read-only investigation. No files deleted, moved, or rewritten. Generated 2026-07-14.

> **CORRECTION 2026-07-14 (post-verification): the publishing rewrite is NOT worth doing — do not run §1's command.**
> The 227 MiB "dead" figure was computed against `main`'s HEAD only. publishing has **39 refs incl. ~30
> design-experiment branches** (`design/v1-editorial`, `v2-quiet`, `v3-warm`, `design-refresh-bold`…). Recomputing
> "dead" against ALL ref tips: **42 of the 123 media blobs the main-only calc flagged are LIVE in a design branch**
> — the §1 command would have deleted images from your design experiments. Genuinely-dead-at-all-tips media is only
> **81 blobs / 41 MiB**. Rewriting all 39 refs (every design-branch SHA changes) to reclaim ~41 MiB is a bad trade
> with real taste-data risk. VERDICT: skip. (Also: stripping ALL 2680 "dead" blobs as §1 literally says would destroy
> the revision history of every edited .svelte/.svx/.md/.ts/.css — the dossier's "museum-JPEG only" framing was wrong.)

## Per-repo totals

| Repo | Working tree | .git | Notes |
|---|---|---|---|
| `personal` | 2.0G (5.5M actually git-tracked) | 24M | bloat is 100% gitignored working-tree cruft, not history |
| `publishing` | 1.3G (`src/` 246M, mostly `node_modules`) | 481M (409 MiB pack, `git count-objects -v`: size-pack 419466 KiB) | real git-history blob bloat |

---

## 1. `publishing` — GIT HISTORY BLOAT

**Remote:** `origin git@github.com:markusstrasser/publishing.git` (GitHub, fetch+push same URL). **Single author** across all 1267 commits: `Markus Strasser` (`git log --format='%an' | sort -u`) — solo repo, so force-push coordination risk is low, but old commit SHAs referenced anywhere (other clones, CI, PR links) will still break.

### Top blobs ever committed (from `git rev-list --objects --all` + `cat-file --batch-check`, top 40 by size)

```
13982370  src/lib/images/genesis/rembrandt-jacob-wrestling-commons.jpg   DEAD (not in HEAD)
 9370128  src/lib/images/king-lear/romney-lear-awakened.jpg              DEAD
 8937166  src/lib/images/genesis/martin-sodom.jpg                        DEAD
 7822138  src/lib/images/matthew/perugino-delivery-keys.jpg              DEAD
 7323616  src/lib/images/essays/smut/lyra.mp3                            LIVE
 6368435  src/lib/images/mark/burial/caravaggio-entombment.jpg           DEAD
 5856708  static/media/essays/smut/lyra.mp3                              DEAD
 5429979  src/lib/images/luke/parables/rembrandt-return-prodigal-son.jpg DEAD
 4816718  src/lib/images/john/velazquez-crucified-christ-prado.jpg       LIVE
 4646361  src/lib/images/genesis/rembrandt-jacob-blessing-joseph-commons.jpg DEAD
 4536303  src/lib/images/john/guercino-samaritan-woman-kimbell.jpg       DEAD
 4427236  static/media/projects/lupa.webp                                DEAD
 2471134  static/media/projects/lupa.webp                                LIVE  ← same path, 3 different historical sizes (4.43M/2.47M/2.34M dead)
```
(full 40-row table in scratch; DEAD = blob hash absent from current `git ls-tree -r HEAD`, i.e. genuinely dead weight in history, not just "large but current.")

### Root cause — confirmed via commit log, not guessed

```
85d2edd [media] Cap image sources at 2560px — 20 museum scans 93MB → 28MB, lint-enforced
2dc55c8 [media] Cap image variants at 640/1280/2560 — kills 3-5MB museum-scan payloads
```
36 commits touch `src/lib/images`. The repo repeatedly committed full-resolution museum-scan JPEGs, then re-encoded/downscaled them **in place at the same path** in later commits. Every pre-optimization full-res version is still sitting in pack history. `node_modules` was **never** committed (`grep -c node_modules` on all blob paths = 0) — ruled out as a bloat source.

### Reclaimable estimate (measured, not guessed)

| | Bytes | MiB |
|---|---|---|
| All unique blob content, all history | 517,859,976 | 482 |
| **Dead** (2680 blobs, unreachable from current HEAD) | 238,318,069 | **227** |
| Live (1527 blobs, still referenced by HEAD) | 279,541,907 | 266 |

Dead content is 47% of all historical blob bytes. Current working tree (`src/lib/images` 238M + `static/media` 5.5M ≈ 243M) roughly matches the 266 MiB "live" figure — sanity check passes. Post-rewrite + `gc --aggressive`, expect the 409 MiB pack to shrink proportionally to roughly **200–230 MiB**, i.e. `.git` drops from 481M to an estimated **~220–260M** (≈45–50% reclaim, ~220–260 MiB freed).

### Exact command sequence

```bash
cd /Users/alien/Projects/publishing

# 1. backup mirror before any rewrite
git clone --mirror . /Users/alien/Documents/publishing-git-backup-2026-07-14.git

# 2. build the dead-blob-id list precisely (hash present in history, absent from current HEAD tree)
git rev-list --objects --all > /tmp/pub-all-objects.txt
git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' \
  < /tmp/pub-all-objects.txt | awk '/^blob/ {print $2}' | sort -u > /tmp/pub-all-blob-ids.txt
git ls-tree -r HEAD | awk '{print $3}' | sort -u > /tmp/pub-head-blob-ids.txt
comm -23 /tmp/pub-all-blob-ids.txt /tmp/pub-head-blob-ids.txt > /tmp/pub-dead-blob-ids.txt
wc -l /tmp/pub-dead-blob-ids.txt   # sanity check: should be ~2680

# 3. strip exactly those blobs — never touches any blob HEAD still references
git filter-repo --strip-blobs-with-ids /tmp/pub-dead-blob-ids.txt --force

# filter-repo removes the 'origin' remote as a safety default — re-add it:
git remote add origin git@github.com:markusstrasser/publishing.git

git reflog expire --expire=now --all
git gc --prune=now --aggressive

# 4. force-push (REWRITES ALL COMMIT SHAs from the first touched commit forward —
#    effectively the whole history, since image commits are interleaved throughout)
git push origin --force --all
git push origin --force --tags
```

`--strip-blobs-with-ids` (not `--strip-blobs-bigger-than`) is the correct flag here — it takes an explicit list of object IDs, so it is guaranteed not to touch any blob the current HEAD tree still needs (unlike a size threshold, which would also nuke several *currently live* >2MB images sitting in the same size band as the dead ones, e.g. the live 4.8M `velazquez-crucified-christ-prado.jpg`).

### Risk

- **All downstream commit SHAs change.** Solo-author repo, GitHub-only remote — no visible collaborators/PRs to coordinate, so risk is low but not zero (anything with the old SHAs pinned, e.g. deploy configs referencing a commit, breaks).
- GitHub itself may retain the old objects in its own storage for a retention window after a force-push (dangling-commit GC on GitHub's side, out of local control) — local `.git` shrinks immediately; remote-side accounting lags.
- Take the mirror backup (step 1) before running step 3 — non-negotiable, rewrite is destructive to history.

---

## 2. `personal` — WORKING-TREE (not git; everything below is gitignored)

`git status --short --ignored` confirms `exports`, `indexed/*`, `.venv/`, `data/`, `web/node_modules/` are all `!!` (ignored). `.gitignore` lines: `26:/exports`, `19:web/node_modules/`, `11:.venv/`, `21:data/`. Git-tracked content in the whole repo is only 5.5M (`git ls-files -z | xargs -0 du -ch`) — the 2.0G is pure working-tree accumulation, none of it is git history bloat.

**Key discovery: `exports/` is a symlink, not a directory in the repo.**
```
lrwxr-xr-x  1 alien  wheel  30 Jun 23 08:08 exports -> /Users/alien/Documents/exports
```
Its 2.1G physically lives on the **boot volume** under `~/Documents/exports`, not inside the repo tree. Boot volume (`/`): 460Gi total, **174Gi free** (7% used) — not under space pressure today, but `/Volumes/2TBPNY` has 277Gi free and is the documented intended home for this class of data (`indexed/README.md`: *"mount 2TBPNY before embedding or serving"*).

### `exports/` breakdown (`du -sh /Users/alien/Documents/exports/*/`)

| Chunk | Size | Class | Evidence | Action | GB saved |
|---|---|---|---|---|---|
| `snapshots/` (logseq + notes point-in-time dumps) | 916M | **a** — likely irreplaceable personal archive; no evidence found in this probe of a live sync elsewhere | dir names are dated snapshots (`logseq-snapshot-2025-11-16` … `notes-snapshot-2026-06-07`); no generator script found | relocate to 2TBPNY, do not delete | 0.90G (relocated, not freed) |
| `chatgpt/` (`conversations.json` 509MB raw) | 487M | **b** — re-exportable free from OpenAI account settings self-service export; `grep -rl "exports/chatgpt" scripts/ src/ tools/` = 0 hits, nothing in-repo reads it | no consumer; pure cold archive | relocate to 2TBPNY | 0.48G |
| `claude/` (`conversations.json` 254MB raw) | 244M | **b** — same pattern, Anthropic account-settings export, 0 in-repo consumers | pure cold archive | relocate to 2TBPNY | 0.24G |
| `ibkr/` | 198M | **b** — Interactive Brokers Flex/statement data; `README.md` present, but portfolio truth is read from `finances-master-*.xlsx` + `portfolio.duckdb`, not raw `ibkr/` files directly (`tools/portfolio_snapshot.py` docstring: *"intel/indexed/portfolio.duckdb is the IBKR-Flex slice ONLY"*) | re-fetchable from IBKR account/API | relocate to 2TBPNY | 0.19G |
| `phenome-data/backups/twitter_unified.2026-06-11.sqlite` | 167M | **d** — redundant stale snapshot of a *derived* DB. The live version of this exact file is already relocated: `data/twitter_unified.sqlite -> /Volumes/2TBPNY/ext-media/twitter/store/twitter_unified.sqlite` (symlink, confirmed). A dated June-11 backup copy sitting on the boot disk adds no unique value over the live derived index. | dated backup of a rebuildable derived index, superseded by the live symlinked copy | safe to delete or relocate | 0.16G |
| `instagram/` + `bumble/` + `hinge/` | 45M+40M+38M = 123M | **b** — dating/social-app self-export data (photos, matches, `report.pdf`); each platform offers self-service re-export but with friction (multi-day wait, account-dependent) | personal social data, no in-repo consumer found | relocate to 2TBPNY | 0.12G |
| `sozialversicherung/`, `nexo/`, `upstream-cache/`, `etoro/`, `n26/`, `wise/`, `finanzamt/`, `revolut/`, `twitter/`, `papers/`, `binance/`, `assets/`, `bear-notes/` | ~13M combined | **b** — small account/tax export dumps, all re-exportable from source services | negligible size, not worth prioritizing | leave as-is | — |

**`exports/` total: 2.1G. Realistic action = relocate ~1.9G to 2TBPNY (symlink target swap), delete ~0.16G stale backup outright.** None of it is "irreplaceable and unbacked" except `snapshots/`, which should be relocated (kept), not deleted.

### `indexed/` breakdown (1.1G, physically inside the repo, gitignored)

`indexed/README.md` (dated 2026-06-21) confirms this is a **derived Gemini-embedding media index** — explicitly documented as rebuildable, with the generator script named and a real dollar cost quoted:

| File | Size | Class | Evidence |
|---|---|---|---|
| `_gemini_embedding_cache.json` | 438M | **b** | content-hash resume cache for `scripts/media/generate_gemini_embeddings.py` |
| `image_embeddings.json` | 376M | **b** | main vector index, 39,664 entries (google_photos 23,359 / twitter 11,200 / pinterest 2,863 / instagram 2,242), rebuildable via the same script |
| `_gemini_visual_cache.json` | 233M | **b** | vision-caption cache |
| `media_extractions.json` | 64M | **b** | Gemini vision captions, partial coverage |
| `mercury.sqlite` | 128K | **c** | rebuilt by `scripts/finance/mercury_sync.py` (read-only Mercury bank API sync) — trivial size |
| `dedup_manifest.json`, `twitter_exact_duplicates.json` | ~3M | **b** | dedup run outputs |

Rebuild is possible but **not free**: README states remaining incremental video-embedding cost was ~$27 (standard) / ~$14 (batch, 50% off) for ~1,085 videos as of 2026-06-19 — full rebuild from zero across all 39,664 entries would cost meaningfully more. README itself states the intended location is 2TBPNY (*"mount 2TBPNY before embedding or serving"*), so this 1.1G is already documented as belonging off the boot disk — it's just not been moved yet.

**Verdict: relocate `indexed/` (1.1G) to 2TBPNY, do not delete/regenerate** — cost of relocation is ~zero, cost of regeneration is real API dollars plus the reprocessing runtime.

`finance/portfolio.duckdb` (6.3M) — class **c**, rebuildable IBKR-Flex-slice derivation per `portfolio_snapshot.py` docstring; too small to matter for space, noted for completeness.

`web/node_modules` (84M), `.venv` (815M), `data/` (240K) — explicitly out of scope per task framing; these are the machine-wide `reclaim` CLI's territory (rebuildable via `npm install` / `uv sync`, zero unique data).

---

## Top 3 ranked recommendations

1. **`publishing` git-history rewrite** — reclaims an estimated **~220–260 MiB** of dead pack weight (47% of all historical blob bytes, confirmed dead via HEAD-tree membership check, root-caused to two specific image-optimization commits `85d2edd`/`2dc55c8`). Single largest, most "real" reclaim of genuinely useless data. Moderate effort (one `filter-repo` pass), low-but-nonzero risk (solo author + GitHub-only remote, but full SHA rewrite) — mirror-backup first, force-push after.
2. **`personal`: relocate `exports/` + `indexed/` to `/Volumes/2TBPNY`** — ~3.2G off the boot disk (2.1G exports minus 0.16G deleted stale backup, plus 1.1G indexed), near-zero risk since everything is already gitignored and `indexed/README.md` already documents 2TBPNY as the intended home; this is a `mv` + symlink swap, not a judgment call.
3. **Delete `exports/phenome-data/backups/twitter_unified.2026-06-11.sqlite`** (167M) — a dated backup of a derived DB whose live copy is already symlinked from 2TBPNY (`data/twitter_unified.sqlite`); adds no unique value, cheapest single win in the dossier.

Boot volume is not under space pressure today (174Gi free / 460Gi), so none of this is urgent — but #1 is the only item that reduces *actual bloat* (dead git history); #2 and #3 are relocations of legitimate data to its documented correct home.
