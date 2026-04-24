# VOCABULARY_RECONCILIATION.md

## Sprint 11 four-type axis vs. WP61 five-category axis

A reader encountering both the Sprint 11 `PARADOX_CLASSIFICATION_MEMO.md`
and `WP61_PRODUCTIVE_INCOMPLETENESS.md` will notice two related-looking
classifications that do not line up 1-to-1. This brief documents the
exact relationship.

### The two axes

**Sprint 11 four-type axis** — classifies *what goes wrong* with a joint
measurement map. It is the axis used throughout
`META_LENS_ATLAS.md` for headline verdicts.

| Type | Name | Failure mode |
|---|---|---|
| I | Injectivity Failure (Insufficient Coverage) | Need another measurement to separate remaining points |
| II | Missing Invariant (Coverage-Invariant Mismatch) | No measurement exists in the allowed family |
| III | Admissibility Failure (Invalid Domain) | The domain `𝒳` is itself ill-defined |
| IV | Time-Consistency Failure (Observer-State Dependence) | `𝒳` shifts as observation proceeds |

**WP61 five-category axis** — classifies *how completely* a specific
measurement family `F` resolves a given non-injectivity.

| Cat. | Name | Resolution-score condition |
|---|---|---|
| I | Complete Complement | `U(F) = ∅`, `score = 1` globally |
| II | Partial Complement | `U(F) ≠ ∅` but `U(F) ⊊ U(∅)` |
| III | Refinement Only | `U(F) = U(F₀)` for some `F₀ ⊊ F` (F is redundant) |
| IV | Invariant-Isolating | `U(F) ≠ ∅` but `score = 1` for some specific task `T` |
| V | Invalid / Inadmissible | Map or domain is ill-posed |

### How they relate

**Axes are orthogonal except for one overlap:**

- **Sprint 11 Type III = WP61 Category V.** Both flag that the proposed
  hidden-object space is not a well-defined domain; `U(f)` is not a
  meaningful object; UOP does not apply. WP61 explicitly cross-references
  this: its Category V is written as "Category V — Invalid / Inadmissible
  (Type III)".
- **Everywhere else the axes are independent.** A given non-injectivity
  has one Type (I, II, or IV) and separately one Category (I, II, III, or
  IV), depending on which measurement family `F` you are scoring against.

**Examples.**

| Paradox / result | Sprint 11 Type | WP61 Category (vs. canonical `F`) | Reason they combine this way |
|---|---|---|---|
| Zeno | I | I (after adding `f_duration`) | After orthogonal measurement is added, `U(F) = ∅`, so score = 1 globally. |
| Banach-Tarski | II | II or III | No `f₂` in the allowed family fully separates orbit-equivalent pairs; a chosen `F` may give partial resolution or pure refinement. |
| Russell | III | V | Same phenomenon: domain invalid; UOP does not apply. |
| Unexpected Hanging | IV | II (under static `F`); not applicable under dynamic template | Static `F` gives partial resolution; the true description requires leaving static UOP. |
| WP62 7-cycle conjecture | (was IV before rejection) | I (now, post-simulation): score = 1 in the refuted sense — classifier resolves to "conjecture rejected" | Classifier gave a clean verdict against TIG's own conjecture. |

### Which axis the atlas uses

**`META_LENS_ATLAS.md` uses the four-type axis exclusively for headline
verdicts**, because it answers the question *"what resolution path do
we need?"* — which is the atlas's central question. The WP61 score is
used as the quantitative output `score_n(f | F) ∈ [0, 1]` reported
per analysis. Both axes together give

```
  verdict ∈ {I, II, III, IV}   (Sprint 11 axis — what went wrong)
  score   ∈ [0, 1]             (WP61 axis — how completely F resolves it)
```

Both are needed; the atlas cites each at its canonical home and does
not attempt to collapse them into one.

### Where this matters in the atlas

- Part I's "The diagnostic template" reports both the Sprint 11 verdict
  and the WP61 score as distinct outputs.
- Part I's "Canonical worked examples" gives the Sprint 11 verdict for
  each paradox; the `score 1.0` / `score 0.0` values are the WP61
  `score_n` values under the canonical measurement family.
- Part II's six-lens × four-type matrix is organized on the Sprint 11
  axis because the atlas's question is "which resolution path for this
  failure mode?" — naturally indexed by type.
- Part III's coherence score `C ∈ [0, 1]` is a different number again:
  it is CK's runtime headline output, related to but distinct from the
  WP61 `score_n`. The atlas keeps them separate (§III.2).

### Canonical citations

- `Gen12/targets/clay/papers/sprint11_tig_bundle_2026_04_08/sprints/PARADOX_CLASSIFICATION_MEMO.md` — four-type axis.
- `Gen12/targets/clay/papers/sprint12_uop_gut_arc_2026_04_08/WP58_UNIFIED_ORTHOGONALITY_PRINCIPLE.md` — UOP Theorem 0.
- `Gen12/targets/clay/papers/sprint12_uop_gut_arc_2026_04_08/WP61_PRODUCTIVE_INCOMPLETENESS.md` — five-category axis.
- `Gen12/targets/clay/papers/sprint12_uop_gut_arc_2026_04_08/WP62_7CYCLE_BOUNDED_AGENT.md` — classifier used against a TIG conjecture.
- `papers/WP_PARADOX_CLASSIFIER.md` — unified spec paper on `tig-synthesis`.
