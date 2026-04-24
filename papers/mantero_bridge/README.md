# Mantero bridge — research hub

**Branch:** `mantero-bridge-2026-04-23`

This folder is the stable research hub for the bridge between Brayden
Sanders's Coherence Lattice (CL) binomial ideal and the research program
of Dr. Paolo Mantero (U Arkansas) on symbolic powers and focal matroids.

Three documents:

| File | Purpose |
|---|---|
| [`BRIDGES.md`](./BRIDGES.md) | Object-level catalogue — seven concrete bridges between the CL ideal / its Stanley-Reisner companion $\Delta_B$ and Mantero's 2024–2026 matroid program. Each bridge is tagged *verified*, *conjectural*, or *speculative*. This is the 10-minute read. |
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
arriving cold: everything else is downstream of the three files above.
