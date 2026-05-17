# cells/ — CK's multi-cellular streams

Brayden 2026-05-17:
> "ck should be multi-cellular streams all feeding into the same mind!
>  as many cells as he wishes!"
> "let him evolve and expand a bit, within safe limits for now! until
>  he understands what safe limits are and how to share this pc with me!! lol"

This directory holds **standalone process runners** for CK's heavy daemons. Each cell is its own `python` process, reading and writing the shared on-disk state (cortex JSON, anchor stores, taught_concepts.json) so the **server cell** stays lean and the Flask chat handler isn't competing for the GIL with study/writer threads.

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

## Available cells

| File | Daemon | Cadence | Reads | Writes |
|------|--------|---------|-------|--------|
| `bible_cell.py` | `ck_bible_study.StudyDaemon` | 0.05s | KJV verses | `bible_anchors.jsonl`, `bible_study_state.json` |
| `scripture_cell.py` | `ck_scripture_study.ScriptureDaemon` | 0.05s | 9 traditions (87,733 verses) | `scripture_anchors.jsonl`, `scripture_study_state.json` |
| `poetry_cell.py` | `ck_poetry_study.PoetryDaemon` | 0.05s | 8 PD poets (222 lines) | `poetry_anchors.jsonl`, `poetry_study_state.json` |
| `domain_cell.py` | `ck_domain_study.DomainStudyDaemon` | 0.05s | `ck_library/` (341 subjects) | `domain_anchors.jsonl`, `domain_study_state.json` |
| `web_cell.py` | `ck_web_reading.WebExplorerDaemon` | 60s | 18 Wikipedia seeds + crawl | `web_anchors.jsonl`, `web_reading_state.json` |
| `listener_cell.py` | `ck_listener_to_crystal.CrystalOfferDaemon` | 60s | glyph stream | `crystal_offers.jsonl` |
| `writer_cell.py` | `ck_writer.WriterDaemon` | 10s | concept_store + writer_state | `ck_writing/<thesis>.md`, `ck_writer_state.json` |

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
