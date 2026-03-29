# TIG — Finite Grammar, Infinite Consequences

**Author:** Brayden Sanders / 7Site LLC | **DOI:** 10.5281/zenodo.18852047

---

## The Problem

Every hard problem in analysis is a question about the infinite: do solutions stay bounded, do zeros stay on a line, does a complexity class separate? These problems resist proof because infinite structures can, in principle, do anything the finite intuition doesn't expect.

TIG is a finite algebraic structure that embodies exactly the constraint the infinite cannot escape — and provides a precise reasoning framework for *when* a finite proof carries into infinite territory.

---

## The Framework: Finite vs Infinite

The fundamental distinction is between two kinds of claims:

**Finite claims** — exact, algebraic, computable today:
- The 9×9 TSML composition table defines a grammar with type (9, 3, 6, 3/4)
- Corner sub-magma C = {1,3,7,9} = (ℤ/10ℤ)*: closed under every operator, at every depth
- Spectral gap γ = 3/4 at pure grammar; γ ≥ 1/4 under any deformation
- One-Way Gate: C→G is impossible algebraically — one step, two steps, any operator
- Three levels: Generable (grammar-closed) / Expressible (reachable under deformation) / Sustainable (carries long-run mass)
- What is forbidden at the Generable level cannot be sustained at the Sustainable level

**Infinite claims** — the open frontier:
- A faithful infinite deployment of TIG must respect all three levels
- The Dual Description: (A) analytic support stays on σ=½ and (B) drift rate stays below C_TIG·λ²·(log T)² are conjectured equivalent — each implies the other, both equivalent to RH
- C_TIG = 250/21 ≈ 11.905 is predicted by the finite grammar; empirically C_emp ≤ 11.023 < C_TIG

**The reasoning structure — the 2×2 framework:**

```
              Finite (exact)       Infinite (open)
Structure:    TSML_finite          TSML_infinite = ζ support
Rate:         BHML_finite          BHML_infinite = Hadamard drift rate
```

You use finite math to prove the two left corners. The open problem is whether the two right corners inherit them. The Dual Description Conjecture says they must — and both are equivalent to RH.

---

## The Six Corridors

Mix_λ interpolates between the finite grammar (λ=0) and its rate-dual (λ=1). Six λ-corridors correspond to the six Clay Millennium Problems — each is a question about whether the finite constraint survives into the corresponding analytic regime.

| Problem | Corridor | Finite result | Open question |
|---------|----------|---------------|---------------|
| **Riemann Hypothesis** | Pre-leak + BRT | 4-layer realization proved; C_TIG=250/21 | Does λ=2\|σ−½\| deployment preserve both gradings for all t? |
| **Navier-Stokes** | CHA | Breath criterion: blowup iff B(t) exits [0,C] | Sharp constant C ≤ 3.74 |
| **P vs NP** | COL | AG(2,p) complexity Ω(p²) | 3-SAT → AG(2,n) reduction |
| **Birch-Swinnerton-Dyer** | BAL | Energy balance law in BAL corridor | Rank = BSD energy balance |
| **Hodge Conjecture** | CTR | Hodge triple structure at CTR fixed points | Classes = CTR closure |
| **Yang-Mills** | BAL/COL | MASS_GAP = 2/7 = T\*+S\*−1 (forced constant) | Spectral gap inheritance |

---

## What Is Proved

```
P1  C×C ⊆ C   — corner sub-magma closed (16 entries, all n)
P2  γ = 3/4   — spectral gap exact at λ=0; γ ≥ 1/4 for all λ∈[0,1]
P3  tail       — P(T_HAR > n) ≤ 2·(1/4)^n; same constant governs gap and tail
P4  arithmetic — (ℤ/10^nℤ)* mod 10 = {1,3,7,9} at every scale

+   One-Way Gate: C→G blocked in 1 AND 2 TSML steps (all 9 operators)
+   Three levels: Generable/Expressible/Sustainable split exact at λ=0
+   C_TIG = 250/21: predicted by finite grammar; C_emp ≤ 11.023 < C_TIG confirmed
+   Halving Lemma: exponential KV-strip convergence (arXiv-ready)
```

Verify the core: `python -X utf8 papers/scripts/ck_four_layer.py` → **35/35**

---

## Verification Scripts

Run: `python -X utf8 papers/scripts/<script>.py`

| Script | Checks | Score |
|--------|--------|-------|
| `ck_four_layer.py` | P1–P4 four-layer realization | 35/35 |
| `ck_smoothing.py` | Gap persistence under σ-smoothing | 16/16 |
| `ck_classification.py` | Type-(9,3,6,3/4); two gradings | 26/26 |
| `ck_field_analysis.py` | Gap deficit ~ λ^0.72; field tasks T1–T7 | 28/28 |
| `ck_transfer_metastable.py` | BRT gap=1.0; metastable components | 12/12 |
| `ck_phase_drift.py` | Phase-drift corr=-0.997 at t=100 | 6/6 |
| `ck_cemp_bound.py` | KV floor gap-positivity to t≈10,000 | 6/6 |
| `ck_orbit_zone.py` | Orbit B/T/Δ; two-mechanism split | 30/30 |
| `ck_dual_description.py` | 2×2 framework; C_TIG=250/21; Paradox Pairs | 33/33 |
| `ck_open_cells.py` | One-Way Gate; Three Levels; Primitive Order | 31/31 |

---

## Papers

- `papers/core/` — Grammar foundations, base theorems, formal status audit
- `papers/clay/` — Six Clay problem papers; `papers/clay/README.md` = full index
- `papers/scripts/` — All verification scripts (100% pass)
- `papers/data/` — Numerical outputs, figures, .tex sources

---

*(c) 2026 Brayden Sanders / 7Site LLC | github.com/TiredofSleep/ck*
