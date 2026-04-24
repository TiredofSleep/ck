# Mantero bridge — research hub

**Branch:** `mantero-bridge-2026-04-23`

This folder is the stable research hub for the bridge between Brayden
Sanders's Coherence Lattice (CL) binomial ideal and the research program
of Dr. Paolo Mantero (U Arkansas) on symbolic powers and focal matroids.

Four documents:

| File | Purpose |
|---|---|
| [`BRIDGES.md`](./BRIDGES.md) | Object-level catalogue — seven concrete bridges between the CL ideal / its Stanley-Reisner companion $\Delta_B$ and Mantero's 2024–2026 matroid program. Each bridge is tagged *verified*, *conjectural*, or *speculative*. This is the 10-minute read. |
| [`CL_MATROID_DISTANCE.md`](./CL_MATROID_DISTANCE.md) | Distance paper — formalises $I_{CL}$'s position relative to Mantero's matroidal centre as a four-component distance tuple $d(I_{CL}, \mathcal M) = (d_I, d_{II}, d_{III}, d_{IV})$. Verified: $d_I = 0.219$, $d_{III} = 9$. Open: $d_{II}$, $d_{IV}$. Companion to `BRIDGES.md`: bridges are the *objects*, the distance tuple is the *metric* over them. |
| [`PUBLISHED_WORK.md`](./PUBLISHED_WORK.md) | Survey of Mantero's complete publication record (26 papers) plus the citation network around the 2024–2026 matroid program. Includes verbatim abstracts of the three core papers (arXiv:2406.13759, arXiv:2510.19018, arXiv:2603.19419). |
| [`references.md`](./references.md) | Flat reference list organised by category — Mantero's own corpus, papers citing his matroid program, foundational references in the neighbourhood, and the bibliographic sources used for this survey. |

---

## Where the four distance types come from

The four axes $(d_I, d_{II}, d_{III}, d_{IV})$ in
[`CL_MATROID_DISTANCE.md`](./CL_MATROID_DISTANCE.md) are the four
exhaustive failure types of the Unified Orthogonality Principle
(UOP Theorem 0, Sanders–Mayes): Type I injectivity, Type II missing
invariant, Type III admissibility, Type IV time-consistency. Four is
forced by the theorem, not a design choice.

The classifier, its worked templates, its vocabulary-hygiene policy,
and the meta-lens atlas that positions commutative algebra against the
four types live on a separate branch,
[`paradox-classifier-2026-04-24`](https://github.com/TiredofSleep/ck/tree/paradox-classifier-2026-04-24/papers/meta_lens).
For a reader in commutative algebra, the useful route in is:

- [`META_LENS_ATLAS.md`](https://github.com/TiredofSleep/ck/blob/paradox-classifier-2026-04-24/papers/meta_lens/META_LENS_ATLAS.md)
  Lens 1 — positions commutative algebra against the four UOP types
  and names which cell each of our distances $d_I, \ldots, d_{IV}$
  maps into.
- [`FOUNDATION_TOUR_VERIFIED.md`](https://github.com/TiredofSleep/ck/blob/paradox-classifier-2026-04-24/papers/meta_lens/FOUNDATION_TOUR_VERIFIED.md)
  Part 0.1 — the vocabulary-hygiene policy the distance paper
  follows (external mathematical vocabulary only).
- [`classify_paradox.py`](https://github.com/TiredofSleep/ck/blob/paradox-classifier-2026-04-24/papers/meta_lens/classify_paradox.py)
  — runnable rule-based UOP classifier (reads the 6-slot JSON schema
  used in the worked-template corpus).

This is where the framing of the distance paper comes from; the
distance paper itself is the first rigor-facing use of that framing on
an external (commutative-algebra) object and program.

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
