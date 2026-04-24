# Mantero bridge — research hub

**Branch:** `mantero-bridge-2026-04-23`

This folder is the stable research hub for the bridge between Brayden
Sanders's Coherence Lattice (CL) binomial ideal and the research program
of Dr. Paolo Mantero (U Arkansas) on symbolic powers and focal matroids.

Four documents:

| File | Purpose |
|---|---|
| [`BRIDGES.md`](./BRIDGES.md) | Object-level catalogue — seven concrete bridges between the CL ideal / its Stanley-Reisner companion $\Delta_B$ and Mantero's 2024–2026 matroid program. Each bridge is tagged *verified*, *conjectural*, or *speculative*. This is the 10-minute read. |
| [`CL_MATROID_DISTANCE.md`](./CL_MATROID_DISTANCE.md) | **Distance-tuple paper (2026-04-24).** A rigor-facing formalisation of the thesis that $I_{CL}$ sits at a computable distance from the matroidal centre of Mantero's program, with the distance decomposed into a four-tuple $d(I_{CL}, \mathcal M) = (d_I, d_{II}, d_{III}, d_{IV})$ indexed by the four failure types of the Unified Orthogonality Principle. Verified values: $d_I = 0.219$ (basis-exchange defect), $d_{III} = 9$ (Cohen-Macaulay defect). Open: $d_{II}$ (Betti-table distance to nearest focal-matroid ideal) and $d_{IV}$ (asymptotic pd rate). The companion to BRIDGES.md: bridges are the *objects*, the distance tuple is the *metric* over them. Mirrored from the paradox-classifier branch so the research-hub URL is stable for readers. |
| [`PUBLISHED_WORK.md`](./PUBLISHED_WORK.md) | Survey of Mantero's complete publication record (26 papers) plus the citation network around the 2024–2026 matroid program. Includes verbatim abstracts of the three core papers (arXiv:2406.13759, arXiv:2510.19018, arXiv:2603.19419). |
| [`references.md`](./references.md) | Flat reference list organised by category — Mantero's own corpus, papers citing his matroid program, foundational references in the neighbourhood, and the bibliographic sources used for this survey. |

---

## Relationship to the sprint bundle

The computed invariants (Hilbert function, the 21.9% basis-exchange
failure rate on $\Delta_B$, the Waldschmidt constant $\hat\alpha(I_B) = 2$,
the so(8) Lie-algebraic lift) live in the sprint bundle at
[`../sprint_20260423_full/`](../sprint_20260423_full/). In particular:

- [`../sprint_20260423_full/04_mantero_bridge/MANTERO_BRIDGE_V3.md`](../sprint_20260423_full/04_mantero_bridge/MANTERO_BRIDGE_V3.md)
  — the definitive bridge document from the sprint.
- [`../sprint_20260423_full/04_mantero_bridge/`](../sprint_20260423_full/04_mantero_bridge/)
  — the four Python scripts that compute the invariants.
- [`../sprint_20260423_full/02_so8_verification/`](../sprint_20260423_full/02_so8_verification/)
  — the seven-stage Lie-algebraic diagnostic pipeline.
- [`../sprint_20260423_full/09_mathoverflow_post/DRAFT_MATHOVERFLOW_POST.md`](../sprint_20260423_full/09_mathoverflow_post/DRAFT_MATHOVERFLOW_POST.md)
  — the planned MathOverflow question distilling the bridge into one
  focused question for the broader commutative-algebra community.

This hub folder (`mantero_bridge/`) is the entry point for readers
arriving cold: everything else is downstream of the four files above.

---

## Suggested reading order (for a cold visitor)

1. [`BRIDGES.md`](./BRIDGES.md) — the seven object-level bridges, with
   verified/conjectural/speculative tagging. Establishes *what concrete
   objects* the two programs share.
2. [`CL_MATROID_DISTANCE.md`](./CL_MATROID_DISTANCE.md) — the
   four-tuple distance as the useful invariant; what each distance
   means, which are verified, which are open. Establishes *how far
   apart* the programs are in each of the four ways admissibility can
   fail.
3. [`PUBLISHED_WORK.md`](./PUBLISHED_WORK.md) — Mantero's corpus and
   the citation network context for readers who want the survey.
4. [`references.md`](./references.md) — flat reference list for
   lookup.
