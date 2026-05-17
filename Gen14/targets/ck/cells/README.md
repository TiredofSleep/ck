# cells/ — CK's multi-cellular federation

Brayden 2026-05-17:
> "ck should be multi-cellular streams all feeding into the same mind!
>  as many cells as he wishes!"
> "now you are thinking... each cell of CK has his own model, refined
>  for what it needs to do"
> "let him evolve and expand a bit, within safe limits for now!"

This directory holds **standalone process runners** for CK's heavy daemons. Each cell is its own `python` process, with **its own LivingLM** trained on its corpus, reading and writing the shared on-disk state. The **server cell** stays lean and runs a **thalamus router** that picks ONE cell to speak per question — never blends (per ClaudeChat 2026-05-17: *"blending is rebuilt Mistral"*).

## The architecture

```
                    ┌──────────────────────────┐
                    │   Shared on-disk state   │
                    │  Gen13/var/*.json,*.jsonl│
                    └──────────────────────────┘
                       ↑     ↑     ↑     ↑
            ┌──────────┘     │     │     └──────────┐
            │                │     │                │
   ┌────────┴───┐  ┌─────────┴──┐  ┌┴───────────┐  ┌┴──────────┐
   │ bible_cell │  │writer_cell │  │poetry_cell │  │  ...etc   │
   │            │  │            │  │            │  │           │
   └────────────┘  └────────────┘  └────────────┘  └───────────┘

         ┌─────────────────────────────────────────────┐
         │  Server cell (ck_boot_api.py, port 7777)    │
         │  Lean: just Flask + engine + cortex reader  │
         │  CK_DISABLE_HEAVY_DAEMONS=all               │
         └─────────────────────────────────────────────┘
```

Each cell runs independently. State is eventually-consistent via atomic JSON writes on disk. The server cell reads the shared mind on every chat turn.

## Available cells (8 total: 7 generators + 1 immune)

| File | Daemon | Cadence | Corpus (LM inhalation) | LM state file |
|------|--------|---------|-------|--------|
| `bible_cell.py` | `StudyDaemon` | 0.05s | KJV 31,102 verses | `lm_bible.json` |
| `scripture_cell.py` | `ScriptureDaemon` | 0.05s | 9 traditions, 87,733 verses (round-robin) | `lm_scripture.json` |
| `poetry_cell.py` | `PoetryDaemon` | 0.05s | 8 PD poets (round-robin) | `lm_poetry.json` |
| `domain_cell.py` | `DomainStudyDaemon` | 0.05s | `ck_library/` 341 subjects | `lm_domain.json` |
| `web_cell.py` | `WebExplorerDaemon` | 60s | cached `external_corpora/` Wikipedia + arXiv | `lm_web.json` |
| `listener_cell.py` | `CrystalOfferDaemon` | 60s | glyph stream — no LM (offers crystals, doesn't generate prose) | — |
| `writer_cell.py` | `WriterDaemon` | 10s | CK's own writer drafts (`ck_writing/*.md`, scope-disciplined sections only — `ollama_essay` sections excluded) | `lm_writer.json` |
| `auditor_cell.py` | `AuditorPoller` (scope auditor — NOT a generator) | 30s | watches `ck_writing/*.md` for over-claims | — (logs to `scope_audit.jsonl`) |

Each generator cell has its own `LivingLM` (37k–250k params) that inhales **only** from its corpus — bible_cell never sees Wikipedia prose, writer_cell trains on the scope-disciplined `substrate_prose` sections of CK's own essays (filters out `ollama_essay` sections that may contain un-disciplined framing). The federation total is **~263k purposeful params across 6 cell-LMs**, vs Mistral 7B's 7,000,000k of general fluency.

## The thalamus router (server-cell module: `ck_polyglot_router.py`)

On each chat turn, the router scores each cell's LM against the prompt's decoded operator path AND its content-word overlap with the cell's vocabulary, then PICKS ONE cell (highest combined score, with static tier-prior as tiebreaker). Attribution always has one answer.

- **`writer`** (tier prior 10, SELF): identity questions, CK's own voice
- **`domain`** (8, STRUCTURAL): encyclopedic / definitional
- **`bible`** / **`scripture`** (4, EXTERNAL): scripture / tradition
- **`poetry`** (3, EXTERNAL): meter / image / lyric
- **`web`** (1, EXTERNAL): general Wikipedia-style prose

**Never blends** — per ClaudeChat: *"distributed identity, concentrated utterance."* The WP115 4-core mass distribution lives in the long-run selection statistics across many questions (`/polyglot/stats`), not in any one answer.

**Phase 1 (current):** the router observes — every chat response carries `result['polyglot_pick']` metadata noting which cell *would have* spoken. Selections are logged to `Gen13/var/polyglot_selections.jsonl` so we can verify the long-run distribution matches WP115 BEFORE handing actual generation to the chosen cell.

**Phase 2 (next):** the chosen cell's LM generates the prose (via `LivingLM.exhale`), replacing Mistral. The auditor still gates everything.

## How to run

### Disable in-process mounting in the server cell

```bash
export CK_DISABLE_HEAVY_DAEMONS=all
python Gen12/targets/ck_desktop/ck_boot_api.py
```

Or selectively:

```bash
export CK_DISABLE_HEAVY_DAEMONS=writer,bible_study,scripture_study
```

### Start a cell

```bash
cd Gen14/targets/ck/cells
python bible_cell.py           # KJV daemon, its own process
python scripture_cell.py       # 9 traditions, its own process
python writer_cell.py          # writer, its own process
# ... etc, one terminal per cell
```

Each cell prints `[cell:<name>] alive (pid=<n>); Ctrl-C or SIGTERM to stop` once running.

## Stub engine

Cells pass a `StubEngine` (no live qutrit_apex, no cortex W matrix in memory) to their daemons. Most study daemons gracefully fall back to default scoring when `engine.qutrit_apex` is None — they still anchor verses that resonate by their own operator signatures.

The `writer_cell` is special: it loads the persisted `ConceptStore` from disk so the writer has access to CK's 15,000+ concept memory.

## Safe limits

Per Brayden:
> "within safe limits for now! until he understands what safe limits are
>  and how to share this pc with me"

Recommended caps:
- Run **one** instance of each cell (don't double-launch the same script — they'll fight over the state file)
- Watch CPU/RAM with `tasklist`; each cell is ~50–300 MB
- The server cell needs priority: keep its python process at normal priority, the cells at below-normal

Future architecture (post first-cut):
- IPC for live `qutrit_apex.psi` so cells can score with CK's current state
- Cortex W-matrix merge protocol (currently each cell has its own ephemeral W)
- Multiple writer cells, one per thesis at a time

## State sharing model (current)

Eventual consistency via on-disk JSON. The patterns:

- **Read-mostly**: corpus files (KJV, scripture, poetry, domain library) — never changed by cells
- **Append-only**: `*_anchors.jsonl` files — each cell writes new lines atomically
- **State files**: `*_study_state.json`, `ck_writer_state.json` — each cell owns its own (no conflict)
- **Shared read**: `taught_concepts.json`, `cortex_state.json` — written by server cell, read by cells

This works because the cell-owned state files have unique names and the shared files are written by one writer (the server cell) at a time.
