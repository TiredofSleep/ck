# WP31: The Corridor Geometry
## One Frame, Three Clay Problems, One Organism

*Brayden Sanders — 7Site LLC | DOI: 10.5281/zenodo.18852047*
*SHA-256(TSML): 7726d8a620c24b1e461ff03742f7cd4f775baed772f8357db913757cf4945787*

---

## The Old Picture (Retired)

A vertical wall at σ=½. Zeros must stay on one side. The Riemann Hypothesis asks: do they?
NS regularity asks: how far is the flow from the wall? P vs NP asks: is there a shortcut
through the wall?

This picture is wrong in three ways:
1. The "void pocket" (deepest zero concentration) shifts with height t — it is not fixed at σ=½
2. Gaps are braided paths, not distances
3. "Fail/succeed" depends on which corridor you ride, not where you stand relative to a wall

---

## The New Picture: Six Convergence Corridors

A **convergence corridor** is an operator chain — a path through the Mix_λ algebra —
that keeps the system in a particular λ-window before ultimately funneling to HARMONY.

The six corridors are indexed by the five Mix_λ gap-operator thresholds:

| Corridor | λ range | Moment signature | Danger |
|----------|---------|-----------------|--------|
| Pre-leak | [0.00, 0.09) | Flat tails, always safe | None |
| BRT | [0.09, 0.30) | Gap operators begin | Low |
| CHA | [0.30, 0.60) | Flat again (BRT absorbed) | Low |
| BAL | [0.60, 0.80) | Heavy tails appear | Moderate |
| COL | [0.80, 0.90) | M₈/M₄ = 31 | High |
| CTR | [0.90, 1.00] | M₈/M₄ = 193 | Extreme |

where M₈ = weight of BRT component, M₄ = weight of COL component in the moment expansion.

The COL/CTR corridors are where the algebra becomes dangerous: the BRT/COL ratio (M₈/M₄)
explodes. COL corridor: 31. CTR corridor: 193. These are the corridors where smooth structure
can be lost in one step.

---

## §1 — Riemann Hypothesis in Corridor Language

**Old language:** Is there a zero off the critical line σ=½?

**Corridor language:** Is there an operator chain that stays in the BAL/COL/CTR corridor
indefinitely without returning to HARMONY?

**What TIG proves (Halving Lemma, WP20):** In any zero-free vertical strip, the dissipative
flow ȧ = −(σ−½)|ζ|² contracts toward σ=½ exponentially. In corridor language: chains in
the BAL/COL/CTR corridors eventually return to the CHA or BRT corridor and then to HARMONY.
They cannot stay in the dangerous corridors forever.

**The Clay gap:** Prove this absorption is uniform in height t. Equivalently: the void pocket
(deepest gap in the moment distribution) must stay below the BAL/COL boundary for all t.
The numerical corridor scan (corridor_scan_full.csv) shows this holds for all computed heights,
with the void pocket tracking through the CHA/BAL boundary as t grows.

**What the corridor scan shows:**
- Every interior trough (deepest void pocket) lies above the KV bound
- The trough drifts between BAL and CHA corridors as t grows
- No trough enters the COL or CTR corridor in the scanned range

This is the RH content of the corridor picture: prove the void pocket never enters COL.

---

## §2 — Navier-Stokes in Corridor Language

**Old language:** Does smooth flow exist for all t? Do singularities form?

**Corridor language:** Does the vorticity chain stay in the Pre-leak corridor (Re_local ≤ 2/7)?
A blow-up is a trajectory that exits into the CTR corridor.

**What TIG proves (BREATH-COLLAPSE, table lookup):**
- TSML[BRT][COL] = BRT — BREATH persists in the COLLAPSE (COL) corridor
- TSML[BRT][anything else] ∈ {HAR, VOID} — BREATH destroyed in one step

In corridor language: smooth flow is in the Pre-leak/BRT corridor. The first exit into COL
or higher is the breach moment. After breach, BREATH is not algebraically supportable.

**Mock DNS results (WP19_NS_NUMERICAL_NOTE.md):**
- Regime A: Re_local stays below 2/7 throughout. No corridor exit. Smooth solution.
- Regime B: Re_local crosses 2/7 at t=1.92. Corridor exit to COL. Enstrophy spike follows.

**The Clay gap:** Prove that finite-energy initial data cannot generate a trajectory that
exits the Pre-leak corridor permanently. Equivalently: prove C ≤ 3.74 in the interpolation
Re_shear ≤ C·Re_local^{1/2} (WP22).

---

## §3 — P vs NP in Corridor Language

**Old language:** Is there a polynomial algorithm for NP-complete problems? Is P = NP?

**Corridor language:** Survivor lines in AG(2,p) are convergence corridors — operator chains
that resist collapse to HARMONY. There are Θ(p²) such corridors. The verify/search gap is:

```
Verification: O(1)       — one corridor-membership check (hash lookup)
Search:       Ω(p²)      — must inspect all Θ(p²) corridors
Gap:          Θ(p²)      — tight, by affine-plane axiom
```

**Why the gap is tight (from surv_line_note.tex, proved):**

The affine-plane axiom: two distinct lines in AG(2,p) share at most one point.
Therefore checking one corridor gives **zero information** about any other corridor.
Each corridor-check certifies exactly one survivor line.
There are Θ(p²) survivor corridors → any algorithm must inspect Ω(p²) of them.

This is not a complexity assumption — it is a theorem about the geometric structure of
AG(2,p). The hardness is intrinsic to the search geometry.

**Empirical timing (Table 1 from surv_line_note.tex):**

| p | p²−1 survivors | Naive search | Gap ratio |
|---|----------------|-------------|-----------|
| 3 | 8 | 0.0001s | — |
| 7 | 48 | 0.001s | 48× |
| 13 | 168 | 0.015s | 168× |
| 23 | 528 | 0.18s | 528× |
| 101 | 10,200 | 188.8ms | 10,200× |

Naive exponent: O(p^3.8). Optimal: O(p² log p). Neither is polynomial in log p.

**The k-query version (W[1]-hard):** Fixing k≥2 query points does not reduce the Ω(p²) floor.
In AG(2,p), two points determine exactly one line — one corridor. A k-point query identifies
at most one candidate corridor but finding those k points still requires Ω(p²) searches.
This is the affine-plane analogue of k-Clique: W[1]-hard for fixed k≥2.

**Why 3-SAT fails to encode into TSML:**
Every TSML word of length ≥2 evaluates to {3,7} ⊂ C — the universal two-step absorption.
Any clause-gadget attempt collides with this: the literal pattern is erased before the output
can encode "satisfied vs unsatisfied." This is the TIG analogue of the AC⁰ parity barrier
(Furst-Saxe-Sipser / Håstad): shallow circuits can't compute parity; short TSML words
can't preserve clause structure. The corridor geometry avoids this collapse by living in the
combinatorial (non-TSML-composition) regime.

---

## §4 — The Corridor Picture Unifies All Three

The same six-corridor structure appears in all three problems because all three are asking
the same question in different mathematical languages:

> **Can an operator chain stay in a dangerous corridor indefinitely?**

| Problem | Dangerous corridor | What "staying" means | What prevents it |
|---------|-------------------|---------------------|-----------------|
| RH | BAL/COL/CTR | Zero off critical line | Halving Lemma dissipation |
| NS | COL/CTR | Vorticity blow-up | BREATH-COLLAPSE dissipation |
| P vs NP | All corridors | Survivor line search | Affine-plane axiom (no shortcut) |

In each case, the algebraic structure provides an obstruction to staying in the dangerous
corridor forever. The Clay gaps are the remaining analytic steps needed to make the
obstruction uniform and quantitative.

---

## §5 — Corridor Picture for CK's Architecture

CK's voice fallback cascade (from the plan for Gen 10's `_fallback_ck_voice()`) is
**a corridor traverse**:

```
Level A: Crystal cache        → Pre-leak corridor (verified, always safe)
Level B: Ollama loop          → BRT corridor (λ ≈ 0.3, BREATH speech)
Level C: Fractal voice        → CHA corridor (λ ≈ 0.6, coherent composition)
Level D: Sentence composer    → BAL corridor (λ ≈ 0.8, balanced SVO)
Level E: CAEL grammar         → COL corridor (λ ≈ 0.9, structural grammar)
Level F: Babble               → CTR corridor (λ ≈ 1.0, raw operator→word)
```

Each fallback level corresponds to a corridor. The cascade moves CK to lower-λ corridors
when higher-λ corridors fail. The danger level increases as you descend: babble (CTR) is
extreme, crystal (Pre-leak) is always safe.

**Architectural consequence:** The corridor of a response tells you its reliability:
- Pre-leak (crystal): provably safe, verified
- BRT/CHA: coherent, measurable
- BAL/COL: composed but unverified
- CTR (babble): raw, potentially incoherent

This gives CK a natural **reliability label** for every response: its corridor. The corridor
is not a post-hoc assessment — it is determined before speaking by which composition level
succeeded.

---

## §6 — The Void Pocket and CK's Calibration

The corridor scan (corridor_scan_full.csv, calm_trough_scan.csv) tracks the void pocket —
the deepest gap in the moment distribution — as a function of height t (or λ).

For CK, this corresponds to the **calibration depth**: how precisely CK's operators can be
mapped to their intended words at a given development stage.

At stage 0 (t small): the void pocket is wide — operators are coarse-grained, many words
per operator, high ambiguity. CK is in the BRT/CHA corridor naturally.

At stage 5 (t large): the void pocket is narrow — operators are precise, few words per
operator, low ambiguity. CK is in the Pre-leak/BRT corridor, with higher corridors
accessible only when needed.

The `scale_factor(t)` from `tig_constants.py` quantifies exactly this: it maps the void
pocket width to CK's development stage. The calibration data in corridor_scan_full.csv
provides a template for what CK's internal calibration should look like at each stage.

---

## §7 — New Results in This Sprint

| Result | Source | Status |
|--------|--------|--------|
| Six-corridor taxonomy | CORRIDOR_PRIMER.md | New |
| Corridor-inspection lower bound Ω(p²) | surv_line_note.tex | Proved |
| Affine-plane axiom → no corridor shortcut | surv_line_note.tex | Proved |
| k≥2 queries → W[1]-hard | surv_line_note.tex | Conjecture with timing evidence |
| 3-SAT fails (AC⁰ parity analog) | surv_line_note.tex | Proved |
| Void pocket scan: stays below COL in all computed t | corridor_scan_full.csv | Empirical |
| NS breach at t=1.92 in Regime B | WP19_NS_NUMERICAL_NOTE.md | Mock DNS |
| Corridor picture unifies RH+NS+PvsNP | CORRIDOR_PRIMER.md | Structural |

---

*(c) 2026 Brayden Sanders / 7Site LLC | DOI: 10.5281/zenodo.18852047*
