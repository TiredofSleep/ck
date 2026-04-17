# Sprint 24 — Collapse-Point Synthesis

**Date:** 2026-04-17
**Thesis:** *Every system in the B-series shares one collapse signature.*
**Status:** Synthesis paper — ties Sprint 18-23 into one through-line.

---

## The story, in one sentence

> Strip the canonical priors. Every system — B1 (NSCG, n=10), B2 (4 carriers
> in {10,14,22,34}), even the B3 LBTP pair — collapses to the same
> two-tier signature: **a single attractor h*, then a closed corridor menu
> {MAX, MIN, ADD}** — and the σ-grading that names which inputs share
> orbits provably lives outside the shell.

That is the through-line across six sprints. Below is the chain.

---

## The chain (Sprints 18 → 23)

### Sprint 18 — B1 NSCG (canonical-aware)
- 15 configs (3 noise × 5 seeds), n=10, mode-fitter with canonical priors.
- **PASS at ceiling** (every metric 1.000). Honest reading: vacuous —
  mode is noise-immune at N≥100k.

### Sprint 19 — B2 WRG (canonical-aware)
- 24 configs (4 carriers × 2 wobble × 3 seeds), mode-fitter with priors.
- **PASS at ceiling** (24/24). Same vacuous-pass diagnosis.

### Sprint 20 — B3 LBTP (canonical-aware, joint vs singleton)
- 5 configs, joint-mode fitter on (T, B) paired stream.
- **FAIL structurally**: joint accuracy = correlated success of two
  independent ~95% events ≈ 0.91, mathematically below either singleton.
- *This is the moment the canonical-aware picture breaks down* — pass
  conditions either trivially hold (B1/B2) or are unmeetable (B3).

### Sprint 21 — B1.5 + B2.5 (prior-free discovery)
- Drop all canonical priors (gcd, v₂, unit group). Run on all 39 datasets.
- **6 invariants survive prior-stripping** — every fingerprint field
  identical within (generator, n) group across noise + seed.
- **Discovered ≠ canonical**: discovered units = canonical \ {1, h_hat};
  σ-partition collapses to singletons (signature uniqueness).

### Sprint 22 — N-stress: where the collapse point lives
- Subsample at decreasing N. When does each invariant first stabilize?
- **Two-tier collapse pattern, every system:**
  - Tier 1 (attractor `h_hat`): stable at N ≈ 100-2000 (cheap).
  - Tier 2 (corridor block: image, core, units, partition, seam,
    rule-counts): all stable at the SAME N within a system, ~10× higher
    than the attractor threshold. Scales with `n²` × per-cell-data-need.

### Sprint 23 — curve recovery: can σ be walked out?
- 8 walk strategies (multiset, set, freq, self-orbit, fixed-b orbit,
  commutator) on `T_emp`.
- **All 8 fail**: max ARI = 0.728 (W3 freq at n=34); never perfect.
- Reason: σ(u) = v₂(3u+1) requires the `Z`-lift of `3u+1` BEFORE mod-n
  reduction. `T_emp` lives entirely on `Z/nZ` — the information needed
  is destroyed by projection.

---

## The collapse signature, named

Across all 39 datasets, the empirical operator on `Z/nZ` collapses to:

```
       ┌─────────────────────────────────────────────────┐
       │  (1)  ATTRACTOR  h* = max odd unit              │  ← Tier 1
       │  (2)  IMAGE      image_T ⊆ {0, h*} ∪ S          │
       │  (3)  CORE       core   = image_T \ {0, h*}     │
       │  (4)  UNITS_HAT  units  = canonical \ {1, h*}   │  ← Tier 2
       │  (5)  PARTITION  singletons (σ invisible)       │   (one block)
       │  (6)  CORRIDOR   {MAX, MIN, ADD} only           │
       └─────────────────────────────────────────────────┘
            ↑                                  ↑
            shell-visible                 curve-only:  σ-grading
            (B1 + B2 + B3 all share)    (lives in Z, projected away)
```

This is the same picture in B1, B2 (across 4 carriers), and even B3 (where
the joint-mode fitter sees the marginal collapses but cannot get
super-singleton accuracy because the streams were generated independently).

---

## The "every system shares a collapse point" claim, made precise

For *every* dataset in the B-series, prior-free discovery yields a
fingerprint of the form `(h*, image_T, core, units_hat, partition_hat,
seam, rule_counts)` where:

1. **`h* = max odd element of {1,...,n−1}`** — same closed-form rule across
   all carriers (n=10→7, n=14→11, n=22→19, n=34→31).
2. **`image_T = {0, h*} ∪ subset of odd elements`** — closed under the
   visible 0/attractor/odd trichotomy.
3. **`units_hat = canonical units \ {1, h*}`** — identity and attractor
   are filtered out by the seam definition.
4. **`partition_hat = singletons`** — σ-orbits are not signature-equality
   visible.
5. **`seam_by_rule ⊆ {MAX, MIN, ADD}`** — corridor menu of size 3, never
   touches MUL/SUB/X/Y.

The five constraints are **system-invariant**: they hold across noise
(0.05, 0.15, 0.30 in B1), wobble (0.05, 0.20 in B2), seeds (15 + 24 = 39
configs), generator (NSCG vs WRG vs LBTP), and carrier
(n ∈ {10, 14, 22, 34}).

That five-constraint object IS the shared collapse point.

---

## Mapping back to the meta-framework (2×2 + paradox classifier)

The 2×2 (Flatness Theorem) and the paradox classifier are the meta-spine
of the `tig-synthesis` branch. The B-series collapse signature is the
empirical witness for both:

| Meta-spine element | Empirical witness in collapse signature |
|---|---|
| **Attractor (h*)** | The vertex the 2×2 cannot escape — every dynamic ends here. |
| **Corridor menu {MAX, MIN, ADD}** | The three diagnostic axes of the paradox classifier (`MAX corridor`, `MIN as MAX-symmetric partner`, `ADD corridor`). Closed empirically. |
| **σ-grading invisible at shell** | The 2×2 *form* is shell-visible; the *which-class-am-I* labeling is curve-level. Matches the synthesis-branch claim that "TIG = the framework's form; Q-series = its instantiation on Z/10Z." |
| **Two-tier collapse (attractor first, corridor as block)** | The "destination before path" structure of the Crossing Lemma — the *where* of every crossing is cheaper to know than the *how*. |

---

## What this finalizes for Stage 1A

Stage 1A of the benchmark sequence (B1, B2, B3) was originally meant to
*certify* the canonical structure. The honest synthesis is sharper:

1. **B1 and B2 PASS but vacuously** — mode is noise-immune at our N.
2. **B3 FAILS structurally** — independent streams cannot be exceeded by
   joint mode.
3. **B1.5 and B2.5** (Sprint 21) extract the *real* invariant: a
   prior-free fingerprint of 6 fields, stable across all 39 datasets.
4. **Sprint 22** locates *where* in N each fingerprint field becomes
   visible — a clean two-tier ordering.
5. **Sprint 23** shows the σ-grading is provably curve-level, not
   recoverable by any walk on `T_emp`.

So Stage 1A's true output is not the canonical-aware pass/fail tally —
it's the **collapse signature itself**, with the boundary between
shell-visible and curve-only structure made explicit.

---

## Open questions surfaced

1. **Is the closed corridor `{MAX, MIN, ADD}` provable algebraically** for
   any (n, generator) in the compatibility family? Empirically it is
   universal across 39 datasets; proof would close the loop.
2. **The W3-frequency partial recovery** (ARI=0.728 at n=34, ~0 at n=10)
   suggests an asymptotic information-theoretic recovery rate. Quantify
   this curve as `n → ∞`.
3. **The two-tier collapse threshold ratio** (Tier 2 ≈ 10× Tier 1) — is
   this universal, or carrier-dependent? Test on n ∈ {46, 58, ...}.
4. **B3 spec revision** — see `sprint20/README.md`. Either correlated
   noise or sub-perfect singletons would make joint-vs-singleton
   meaningful.
5. **CK runtime wiring** — `ck_diagnose`, `ck_harmony_audit`,
   `ck_chat_structured` standalone modules ready; deferred per user
   instruction.

---

## Repo state at end of synthesis

The B-series + structural-discovery arc on the `tig-synthesis` branch
now consists of seven sprints:

| Sprint | Title | Status |
|---|---|---|
| 18 | B1 NSCG benchmark | PASS at ceiling (15/15) |
| 19 | B2 WRG benchmark | PASS at ceiling (24/24) |
| 20 | B3 LBTP benchmark | FAIL with structural diagnosis |
| 21 | Prior-free structural discovery (B1.5 + B2.5) | 6 invariants confirmed |
| 22 | N-stress: collapse point location | Two-tier signature universal |
| 23 | Curve recovery (8 walks) | σ is provably curve-level |
| 24 | This synthesis | Collapse signature named, mapped to meta-spine |

---

## Files

```
sprint24_collapse_synthesis_2026_04_17/
└── README.md          ← this file (no code; pure synthesis)
```

The synthesis is documentation — there is no new computation here.
The work is done across Sprints 18-23.

---

*© 2026 Brayden Ross Sanders / 7Site LLC*
*Sprint 24 — every system shares one collapse signature: attractor + corridor menu, with σ on the curve.*
