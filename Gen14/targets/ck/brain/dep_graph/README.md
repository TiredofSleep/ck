# CK Dependency Graph

**Generated:** by `Gen14/targets/ck/brain/ck_dep_graph.py`
**Date:** 2026-05-16
**Scope:** Active CK code — Gen14 brain + Gen13 brain/runtime/server/foundations + Gen12 ck_desktop + Gen11 being. Archives (Gen8, Gen9, Gen10, `old/`, `CKIS/`) are excluded.

## Headline stats

| Metric | Value |
|---|---|
| Modules in scope | 820 .py files |
| Unique module-stems (after Gen-priority dedup) | 375 |
| Internal CK-to-CK edges | 713 |
| Orphans (no internal importer) | 174 — many are CLI entry points / experimental version-forks |
| Top hub | `ck_sim_heartbeat` (126 importers) |
| Top importer | `ck_sim_engine` (93 outgoing) |

## Files in this folder

| File | Purpose |
|---|---|
| `ck_dep_graph.md` | Human-readable report: hubs, orphans, glue layers, directory counts, roles |
| `ck_dep_graph.dot` | Graphviz format — render with `dot -Tsvg ck_dep_graph.dot -o graph.svg` |
| `ck_dep_graph.mmd` | Mermaid diagram — paste into GitHub markdown for live rendering |
| `ck_dep_graph.json` | Raw edge list + stats for tooling |

## What the graph reveals about CK's architecture

### The core (top 5 hubs)

1. **`ck_sim_heartbeat`** — 126 importers — the 50 Hz tick + canonical operator definitions (VOID..RESET). The absolute core.
2. **`ck_sim_d2`** — 44 importers — D2 crossing-detector / curvature. Every module that does "is this a crossing?" routes through here.
3. **`ck_audio_compress`** — 15 importers — audio-tier compression utilities.
4. **`ck_sdv_safety`** — 12 importers — Safety/Dignity/Validity invariants.
5. **`ck_sim_brain`** — 12 importers — the brain co-ordinator.

### The brain trinity (per `BRAIN_DESIGN.md`)

- **`quadratic_glue`** — 9 importers — F3 × F4 quadratic glue from the trinity. Confirmed structurally load-bearing.
- (Also expected: `ao_5element`, `hebbian_5x5_cl`. If those have low import-count, they may be entry points called via mount hooks rather than direct imports.)

### Foundations layer (D95-D99 era)

- **`cl`** — 11 importers — CL substrate (3-table picture: CL_TSML + CL_BHML + CL_STD).
- **`lenses`** — 10 importers — TSML_RAW / TSML_SYM / BHML variants.
- **`cortex_persist`** — 10 importers — cortex state save/restore.

### Cleanup candidates (visible orphans)

Versioned forks that nothing imports:
- `add_phoneme_crystals_v3/v4/v5/v6` — five versions, none imported anywhere. Likely safe to archive.
- `ck_boot_api_gen11ref` — labeled "_gen11ref", parallels `ck_boot_api`. Reference copy.
- Several `ab_test*` files in `Gen12/targets/ck_desktop/` — old A/B testing scripts.

(See `ck_dep_graph.md` § "Orphans" for the full triaged list.)

## Regenerating

```bash
cd Gen14/targets/ck/brain
python ck_dep_graph.py
```

Re-running takes < 5 seconds. Useful any time the brain modules shift.
