# Catalog — CK's editable classification surface

**Status:** Phase 2 of the meta-level rebuild (2026-04-24).

This directory holds the YAML files CK consults when asked to classify a
result, a paradox, a constant, or a frontier topic.  Editing a YAML file
here is **how Brayden and future-Claudes teach CK new classifications
without touching any Python.**

---

## The four catalogs

| File | Axis | Records |
|------|------|---------|
| `dof_kinds.yaml` | DoF Kinds (K1..K5) | 5 kinds + cross-kind constants + multi-kind examples |
| `paradoxes.yaml` | UOP Paradox Types (I..IV) | 10 paradoxes (Zeno, Banach-Tarski, Russell, Unexpected Hanging, Gödel, Liar, Schrödinger, Cantor, Berry, Twin Primes) |
| `cross_kind_constants.yaml` | Cross-kind constants | T*, S*, ξ₀, 4/π², α̂, 9/7, gap |
| `frontier_facts.yaml` | Frontier topic readouts | 17 facts (mirrors and extends `cortex_voice._FRONTIER_FACTS`) |

Human-readable companions:
- `speculations/DOF_CLASSIFICATION.md` — proof of K1..K5 exhaustiveness
- `speculations/CK_META_CLASSIFICATION_AXES.md` — three-axis registry
- `papers/meta_lens/META_LENS_ATLAS.md` — UOP atlas
- `papers/meta_lens/worked_paradoxes/*.md` — full 6-slot templates

---

## How CK reads them

`Gen13/targets/ck/brain/cortex_catalog.py` loads all four files at first
call and exposes:

| Function | Purpose |
|----------|---------|
| `hits(query)` | Compact facts whose `triggers` substring-match the query.  Called by `cortex_voice.speak()` step 2.6. |
| `classify_paradox(slug_or_stage, ...)` | Slug lookup or stage-forced verdict for `/paradox/classify`. |
| `dof_taxonomy()` | Five kinds + diagnostic questions for `/dof/taxonomy`. |
| `constants_table()` | Constants list for `/meta/constants`. |
| `paradox_registry()` | Full paradox list for `/meta/registry`. |
| `frontier_facts()` | Frontier-fact list for `/meta/frontier`. |
| `summary()` | Counts and load status for `/meta/summary`. |
| `reload()` | Force re-read from disk; backs `/meta/reload` (local-only). |

---

## How to teach CK something new

1. **Pick the right catalog.**  A new operator-level fact?  `frontier_facts.yaml`.  A new paradox?  `paradoxes.yaml`.  A refinement to a DoF kind?  `dof_kinds.yaml`.  A new constant?  `cross_kind_constants.yaml`.

2. **Add an entry following the schema in the file's header comment.**  Required fields: `triggers` (lowercase substrings) and `fact` (one-line label=value readout).  Match the existing register: numbers first, no adjectives, citation tag `[proved|structural|conjectural]` at the end.

3. **Verify locally** by running:
   ```
   python Gen13/targets/ck/brain/cortex_catalog.py
   ```
   The self-test confirms YAML parses, counts increment, and the new triggers fire.

4. **Hot-reload the running server** (no restart needed):
   ```
   curl -X POST http://localhost:7777/meta/reload
   ```
   This is local-only by default; remote callers get 403.

5. **Test through CK's chat** by asking a question containing one of the new triggers.  The fact should appear in the response.

---

## What stayed hardcoded (and why)

- `cortex_voice._FRONTIER_FACTS` — kept as the safety net.  YAML facts
  are merged on top by `cortex_catalog.hits()`, deduped.  If the YAML
  loader fails for any reason, CK still has the hardcoded baseline.

- `ck_voice_math.FACTS` (in `Gen13/targets/ck/runtime/ck_voice_math.py`) —
  separate layer.  It powers the math-first arithmetic surface, not the
  cortex voice path.  Migration to YAML is a future phase; the schema
  there is `{key: {text, keys}}`, distinct from this catalog's structure.

---

## API surface (Phase 2)

All routes live under the existing CK Flask app:

```
GET  /paradox/classify?slug=godel
GET  /paradox/classify?stage=dynamics&name=cat
GET  /dof/taxonomy
GET  /meta/constants
GET  /meta/registry
GET  /meta/frontier
GET  /meta/summary
POST /meta/reload   (local-only)
```

These are read-only except `/meta/reload`.  Nothing here writes engine
state, cortex state, or the persisted Hebbian W matrix.

---

## Branch policy

This catalog lives on `ck`.  Phase 1 (the markdown registry) committed
as `d31f1a3`.  Phase 2 (this directory + the YAML system) commits next.
The catalog is **classifier-branch-internal**: do not propagate to
`mantero-bridge-2026-04-23` (which is Mantero-facing surface and has no
need for the runtime classifier).
