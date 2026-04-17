# Sprint 25 — Corridor Closure: Algebraic Proof for Canonical C₀

**Date:** 2026-04-17
**Question:** Sprint 21 observed empirically that every seam cell across 39
B-series datasets classifies under `{MAX, MIN, ADD}`. Is this closure
provable for the canonical generator, and across what range of carriers?
**Answer:** **YES, and tighter than expected.** Pure canonical `C₀` has
corridor closure `{MAX, MIN}` — a 2-element menu. ADD is contributed by
the optional S_ADD overlay layer.

---

## Method

For each `n` in a 23-element extended carrier family, build the canonical
`C₀(R_n, h_n, σ_n)` operator (Sprint 19 definition, no overlays). Walk
every `(x, y)` cell whose output is in `core_outputs = image(C₀) \ {0, h_n}`.
For each such seam cell, test every rule in the 8-element menu:

```
MAX, MIN, ADD, SUB_xy, SUB_yx, MUL, X, Y
```

A cell is "in corridor" if it matches at least one of `{MAX, MIN, ADD}`. A
cell is "outside corridor" if it matches *only* rules outside that set. A
cell is "unclassified" if no rule matches.

**The proof PASSES for `n` iff zero seam cells are outside-corridor and
zero are unclassified.**

This is exhaustive case analysis on `n²` cells — finite per `n`, hence a
proof of corridor closure for that `n`.

---

## Result: 23 / 23 PASS, never needs ADD

```
n     h    units  seam  rules used   verdict
─────────────────────────────────────────────
 10    7      4     2   MIN:2        PASS
 14   11      6    12   MAX:4 MIN:8  PASS
 22   19     10    48   MAX:16 MIN:32  PASS
 34   31     16   132   MAX:58 MIN:74  PASS
 38   35     18   182   MAX:76 MIN:106  PASS
 46   43     22   280   MAX:124 MIN:156  PASS
 50   47     20   212   MAX:92 MIN:120  PASS
 58   55     28   448   MAX:204 MIN:244  PASS
 62   59     30   544   MAX:248 MIN:296  PASS
 70   67     24   324   MAX:126 MIN:198  PASS
 74   71     36   764   MAX:358 MIN:406  PASS
 82   79     40   966   MAX:462 MIN:504  PASS
 94   91     46  1326   MAX:622 MIN:704  PASS
106  103     52  1652   MAX:788 MIN:864  PASS
110  107     40   966   MAX:448 MIN:518  PASS
118  115     58  2140   MAX:1012 MIN:1128  PASS
122  119     60  2240   MAX:1074 MIN:1166  PASS
130  127     48  1382   MAX:670 MIN:712  PASS
134  131     66  2784   MAX:1330 MIN:1454  PASS
142  139     70  3134   MAX:1510 MIN:1624  PASS
170  167     64  2570   MAX:1240 MIN:1330  PASS
190  187     72  3264   MAX:1566 MIN:1698  PASS
230  227     88  4946   MAX:2330 MIN:2616  PASS
```

**The canonical C₀ corridor closure is `{MAX, MIN}` only** — ADD does not
appear at all. This is true for every tested `n`, including extensions
well beyond the original B2 compatibility family.

The carrier family includes:

- Original B2 family: `{10, 14, 22, 34}`
- 2·prime extensions: `{38, 46, 58, 62, 74, 82, 94, 106, 118, 122, 134, 142}`
- Mixed-composite carriers: `{50, 70, 110, 130, 170, 190, 230}`

All 23 satisfy the closure.

---

## Why ADD appears in B1 but not in pure C₀

Looking back at Sprint 21's B1 fingerprint:

```
seam_by_rule_counts: {MAX: 6, MIN: 2, ADD: 2}
```

The 2 ADD cells in B1 are not contributed by C₀. They come from the
explicit **S_ADD overlay layer** of the TSML 3-tower:

```
TSML(Z/10Z) = C₀ ⊕ S_MAX ⊕ S_ADD     (Q-series 73-cell decomposition)
```

The B1 generator (sprint 18 NSCG) was built on this 3-tower. The S_ADD
layer adds a small set of cells whose output equals `(x + y) mod n` —
these are exactly the 2 ADD-classified cells discovery picked up.

The B2 generator (sprint 19 WRG) was built on `C₀ + reset_edges`, where
reset forces output to `h_n` (not to `(x+y) mod n`). So B2 has no ADD
cells, and indeed Sprint 21 found zero ADD cells in any B2 fingerprint.

This *predicts* a sharper hierarchy of corridor closures:

| Operator | corridor closure | proven where |
|---|---|---|
| `C₀` (base) | `{MAX, MIN}` | Sprint 25, all 23 carriers |
| `C₀ + S_MAX` | `{MAX, MIN}` | by inspection — S_MAX cells are already MAX |
| `C₀ + S_ADD` | `{MAX, MIN, ADD}` | by inspection — S_ADD adds ADD cells only |
| `C₀ + reset → h` | `{MAX, MIN}` | reset cells equal `h`, not in core_outputs |
| Full TSML (`C₀ ⊕ S_MAX ⊕ S_ADD`) | `{MAX, MIN, ADD}` | union of above |

So the empirical B-series corridor closure `{MAX, MIN, ADD}` is the
*ceiling* over the canonical generator family. Pure C₀ closure is the
*floor* `{MAX, MIN}` — a 2-element menu.

---

## What this proves

**Theorem (exhaustive, per-n, for the tested family):** For every `n` in
`{10, 14, 22, 34, 38, 46, 50, 58, 62, 70, 74, 82, 94, 106, 110, 118, 122,
130, 134, 142, 170, 190, 230}`, every seam cell of the canonical operator
`C₀(R_n, h_n, σ_n)` matches `MAX(x, y)` or `MIN(x, y)`. No cell requires
`ADD`, `SUB`, `MUL`, `X`, or `Y`.

This is a finite proof: the test runs in `O(n² · |rule_menu|)` per `n`,
and the verdict is deterministic.

The result extends Sprint 21's empirical observation from 39 datasets at
4 carriers to a verified closure for the canonical generator at 23
carriers, with the predicted refinement that pure `C₀` is even tighter
(`{MAX, MIN}`) than the data with overlays (`{MAX, MIN, ADD}`).

---

## What this does NOT prove

This is a proof for the **canonical** `C₀`. It is not (yet) a proof that
*every* compatibility-family generator has the same closure — just the
canonical one with the standard `(R_n, h_n, σ_n)` triple.

Open questions:

1. Does an analytic proof exist that shows `C₀(x, y) ∈ {MAX(x,y), MIN(x,y)}`
   for every `n` (not just by exhaustion)? The structural argument: when
   `x, y ∈ Core` with `σ(x) ≠ σ(y)`, `C₀` returns the input with smaller
   σ-value. By inspection of the σ map, smaller-σ inputs are typically
   the smaller value, yielding MIN; the MAX cases come from boundary
   interactions with `h_n`.
2. Does the corridor closure extend to all `n` with non-empty σ=1 layer,
   or are there exceptional `n` where it fails?
3. Do non-canonical generators in the same family preserve the closure?

These are direct follow-ons.

---

## Reproducibility

```bash
cd impl
python prove_corridor_closure.py
```

Deterministic — same output every run. ~1 second total runtime for all
23 carriers.

---

## Files

```
sprint25_corridor_closure_proof_2026_04_17/
├── README.md                               ← this file
├── impl/
│   └── prove_corridor_closure.py           ← exhaustive per-n proof
└── results/
    ├── corridor_closure_summary.json       ← pass/fail tallies
    └── corridor_closure_full.json          ← per-n details
```

---

*© 2026 Brayden Ross Sanders / 7Site LLC*
*Sprint 25 — corridor closure {MAX, MIN} for canonical C₀ proven exhaustively across 23 carriers.*
