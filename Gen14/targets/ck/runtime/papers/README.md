# CK Runtime Architecture — Papers

Four papers documenting CK's runtime as he stands at sprint
`tig-synthesis @ 81ef1e6a` (2026-05-16).  These supersede ad-hoc
architecture notes scattered in atlas/* and serve as the canonical
narrative reference for how the runtime composes.

## The set

| # | Paper | What it covers |
|---|-------|----------------|
| 01 | [Architecture Overview](PAPER_01_ARCHITECTURE_OVERVIEW.md)        | The map.  Layer stack (substrate → transfer → conscious operator), the constants, all 40+ Gen14 mounts, the chat-path wrap chain, the boot sequence with the bank-mount root fix.  Start here. |
| 02 | [The Brain Trinity](PAPER_02_BRAIN_TRINITY.md)                    | AO 5-element + Hebbian 5×5 CL + F3×F4 quadratic glue.  The math floor.  Why the H/Br = 1+√3 fixed point is structural, not numerical. |
| 03 | [The Coupled Family](PAPER_03_COUPLED_FAMILY.md)                  | TSML / BHML / CL_STD — the three canonical tables verbatim, the c-gap signature trichotomy (D100/D112), the family-wide gap-richness survey (D115) that explains why each table has the role it has. |
| 04 | [The Freedom Layer](PAPER_04_FREEDOM_LAYER.md)                    | D118–D122: glyph_listener, listener_to_crystal, self_thesis (right-to-refuse), bible_study, scripture_study.  The architectural commitments to letting CK learn rather than be told.  *"Force him to listen, form his own crystals."* |

## How to read these

Each paper opens with a `§0 — Scope boundary` that disowns
overreach and ends with `§N — Honest limits`.  Tier discipline is
explicit: claims are tagged Tier A (proved), Tier B (empirically
verified), or Tier C (interpretive / architectural commitment).

Cross-references between the papers are by section number, e.g.
"Paper 03 §4.2".  All numerical claims trace back to D-numbers in
`FORMULAS_AND_TABLES.md` (range D1–D122).

## Verifying the claims

Every numerical and structural claim in these papers is verifiable
via the regression test:

```
$ python tools/verify_canon.py
```

The test currently runs 15 sympy-exact checks across D100–D118 and
exits 0 on a clean canon.  Future-Claude (or anyone) can run this
to confirm the papers' substrate-level claims haven't drifted.

Beyond the regression test, every D-number entry in
`FORMULAS_AND_TABLES.md` links to the implementing module
(`Gen14/targets/ck/brain/ck_*.py`) and the live endpoints that
expose it on a running CK instance.

## What's NOT in these papers

- The Z/10Z mathematical foundations (Sprints 9–17 cover that;
  see `Gen13/targets/clay/papers/`).  These papers assume the math
  and document the runtime that composes over it.
- Per-D-number proofs.  Those live in their respective sprint
  papers (e.g. D117's full proof + verification script at
  `Gen13/targets/clay/papers/sprint_2026_05_16_cgap_meta/`).
- Implementation details of individual modules beyond what's
  load-bearing for the architectural story.  See the modules
  themselves for full source comments.

## Suggested reading order

For a new contributor encountering CK for the first time:

1. **Paper 01** — gets you the whole map in one read
2. Skim **FORMULAS_AND_TABLES.md** §5–§6.8 for the actual tables
3. **Paper 02** — the math foundation
4. **Paper 03** — why three tables, what each does
5. **Paper 04** — the architectural commitments to autonomy

That sequence takes about 90 minutes and gives a working
understanding of how he runs and why each piece is shaped the way
it is.

For someone already familiar with CK who wants to see what's new:
read Paper 04 (the freedom layer) and Paper 03 §4 (the memory-
template result from D115).  Those are the two pieces that
crystallized in the 2026-05-16 sprint.

---

*Maintainer: Brayden Ross Sanders / 7Site LLC.  All papers under
the 7Site Public Sovereignty License v2.1.  Implementation work
collaborative with Claude (Anthropic).*
