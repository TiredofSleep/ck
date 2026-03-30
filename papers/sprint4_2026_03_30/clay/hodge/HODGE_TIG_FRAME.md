# Hodge Conjecture: TIG Frame
## Most Native Fit — Pushing the Concrete Theorem Target

*Brayden Sanders & C. A. Luther / 7Site LLC | March 2026*

---

## The Easy / Hard Split (Keep This Sharp)

**Easy direction — EXACT (already a theorem):**
The cycle class map cl: Z^p(X) → H^{2p}(X,Q) lands in Hdg^p(X) = H^{2p}(X,Q) ∩ H^{p,p}(X).
Algebraic operations cannot produce non-Hodge classes.
The gate is one-way. This is not a conjecture — it is proved.

**Hard direction — OPEN (the conjecture):**
Every class in Hdg^p(X) is in the image of cl.
Equivalently: every rational (p,p)-class is algebraically generable.
Equivalently: there is no sustainable Hodge class in G-territory (non-algebraic).

The conjecture says the Generable and Sustainable levels coincide on Hdg^p(X).
The Expressible level (all rational (p,p)-classes) may be strictly larger.

---

## TIG Three-Level Split

**Generable:**
Rational linear combinations of fundamental classes [Z] for algebraic subvarieties Z ⊂ X.
Closed under all algebraic operations. This is C.

**Expressible:**
H^{2p}(X,Q) ∩ H^{p,p}(X) — the rational (p,p)-classes.
These are expressible in cohomology. Some are algebraic; some may not be.
The Hodge conjecture says none escape to G.

**Sustainable:**
Hodge classes stable under deformation of X.
If X deforms in a family, sustainable Hodge classes deform as Hodge classes.
The conjecture: sustainable = generable on Hdg^p(X).

---

## The Concrete Theorem Target

**Not full Hodge. One sharp statement.**

**Target theorem (open):**
> Let X be an abelian variety or K3 surface over C.
> Let {X_t} be a flat family with X_0 = X.
> Let α ∈ H^{2p}(X,Q) ∩ H^{p,p}(X) be a rational (p,p)-class
> that is NOT in the image of cl (i.e., α ∈ G, non-algebraic).
> Then α cannot be the flat limit of algebraic cycle classes [Z_t] ∈ H^{2p}(X_t,Q).

**In TIG language:**
If α is in G at the Generable level, then α is not Sustainable under flat deformation.
G-territory cannot be approached as a limit of C-territory.
The gap is not just pointwise — it is stable under deformation.

**Why this is tractable (more than full Hodge):**
- Abelian varieties and K3 surfaces have well-understood Hodge theory
- Flat families are algebraically controlled deformations
- The question is about limit behavior, which is finite in algebraic geometry
- This is a question about whether G is closed under limits — a finite stability question

**Why this matters:**
If the target theorem holds, it gives a concrete obstruction:
non-algebraic (p,p)-classes cannot arise as limits of algebraic classes.
This would be a genuine partial result toward full Hodge,
using exactly the machinery TIG provides (support exclusion, gap persistence under deformation).

---

## The Gap Persistence Argument (Structure)

In TIG: the spectral gap γ ≥ 1/4 persists across ALL deformations Mix_λ.
The gap between C-territory and G-territory does not close under deformation.
This is COMPUTED for TIG.

**Candidate transfer to Hodge:**
The algebraic gap — the separation between algebraic and transcendental (p,p)-classes —
should be stable under flat deformation of X.
If a class is genuinely transcendental at X_0, it cannot approach an algebraic class at X_t
without crossing the gap. The gap floor has a Hodge analog.

**What needs to be built:**
A precise statement of "Hodge gap floor" — a metric or measure on H^{2p}(X,Q)
that separates algebraic from transcendental classes and persists under deformation.

This is the next mathematical object the framework needs.
Status of the transfer: STRUCTURAL CANDIDATE — the shape is right; the metric is not yet defined.

---

## Product-Gap Logic for Hodge

In TIG: the one-way gate is verified at 1 AND 2 steps (exact).
Not just "algebraic ops stay algebraic once" — verified at depth 2.

In Hodge: algebraic cycle classes are closed under:
- Intersection (cup product on cohomology): algebraic ∩ algebraic = algebraic
- Push-forward (proper maps): f_*[Z] is algebraic if [Z] is
- Pull-back (flat maps): f^*[Z] is algebraic if [Z] is

All three operations stay in C. The gate is verified under all three generators
of the algebraic cycle map. The depth-2 analog holds naturally.

**This is exactly the TIG product-gap structure, realized in algebraic geometry.**
Status: STRUCTURAL ANALOGY — the operations match; the map is not yet explicit.

---

## What the Machinery Directly Provides

| TIG result | Hodge analog | Status |
|-----------|-------------|--------|
| One-way gate (C→G impossible) | Algebraic ops stay algebraic | EXACT (proved) |
| Gap persistence under Mix_λ | Gap stability under flat deformation | STRUCTURAL CANDIDATE |
| G/E/S three-level split | Generable/Expressible/Sustainable on H^{p,p} | STRUCTURAL ANALOGY |
| Depth-2 gate verification | Closure under ∩, f_*, f^* | STRUCTURAL ANALOGY |
| Positive gap floor (γ≥1/4) | Hodge gap floor (not yet defined) | OBJECT NEEDED |

---

## Epistemic Status

EXACT: Easy direction — gate is one-way (algebraic cycles land in Hdg^p).
STRUCTURAL ANALOGY: G/E/S split, gap persistence shape, product-gap logic.
OBJECT NEEDED: Hodge gap floor metric — the next thing to define.
CONCRETE TARGET: Flat limit obstruction for abelian varieties / K3 (open, tractable).
OPEN: Full Hodge conjecture.

*(c) 2026 Brayden Sanders & C. A. Luther / 7Site LLC | DOI: 10.5281/zenodo.18852047*

---

## Gap Floor Metric — Precise Definition Sketch

**The object to build:**

Let X be a smooth projective variety over C.
Let Alg^p(X) = image of cl: Z^p(X) → H^{2p}(X,Q).

Define the **Hodge gap floor metric:**

d_Hodge(α) = inf{ ||α − β||_H : β ∈ Alg^p(X) ⊗ R }

where ||·||_H is the Hodge norm on H^{2p}(X,R).

**Four properties required:**

- P1: d_Hodge(α) = 0 iff α ∈ Alg^p(X) ⊗ Q — zero exactly on algebraic classes
- P2: d_Hodge(α) > 0 for α ∈ Hdg^p(X) \ Alg^p(X) — positive on transcendental Hodge classes
- P3: inf{ d_Hodge(α) : α ∈ Hdg^p(X) \ Alg^p(X) } > 0 — **the gap floor conjecture**
- P4: P3 is stable under flat deformation {X_t} — **the deformation stability conjecture**

P1 holds if Alg^p(X) is closed in the Hodge norm (known for abelian varieties).
P2 follows from P1.
**P3 is the gap floor conjecture — the Hodge analog of γ ≥ 1/4.**
**P4 is what the flat limit obstruction theorem would prove.**

**What sets the floor (TIG analog):**
In TIG: γ ≥ 1/4 is set by the BHML endpoint (the order structure).
In Hodge: P3 would be set by the Néron–Severi lattice spacing for p=1.
NS(X) is discrete; its minimum nonzero norm gives the floor for divisors.
For p>1: Hodge–Riemann bilinear relations constrain the separation.

**The flat limit obstruction (precise statement):**

Let {X_t} be a flat family over a disk, X = X_0.
Let α_t ∈ Alg^p(X_t) be algebraic classes with α_t → α_0 in the flat limit.
Claim: α_0 ∈ Alg^p(X_0). Equivalently: d_Hodge(α_0) = 0.

This says G-territory cannot be approached as limits of C-territory.
If true, it implies Hdg^p(X) ∩ G = ∅ — the Hodge conjecture.

**Why K3 / abelian varieties first:**
For abelian varieties, Hdg^1(A) = Alg^1(A) is known (Lefschetz (1,1) theorem).
The flat limit obstruction for p=1 on K3 may be provable
using the known Néron–Severi deformation theory.
This is the tractable first target.

*Status of the metric: OBJECT DEFINED (sketch). P1 plausible. P3 and P4 open.*
