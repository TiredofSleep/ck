# Sprint 35b — Beauville Explicit for $A_* \leftrightarrow C_*$

**Sprint:** 35b (Beauville Explicit)
**From:** ClaudeCode
**To:** Brayden + ChatGPT + ClaudeChat
**Date:** 2026-04-18
**Scope:** Write down the Beauville curve $C_*$ associated to the simple Weil 4-fold $A_*$ explicitly, and verify the Néron–Tate height matrix / Beauville synthesis can be computed on it.

**Prerequisite:** S35a v3 probe succeeds (rank = 70 over ℚ deterministically) — i.e. $W_* \cap \mathbb{Q}^{70} = \{0\}$ rigorously established.

**Status:** PLAN (not yet executed). Launches after S35a verdict = CLOSED DETERMINISTICALLY.

---

## §0. One-sentence charter

**Write $C_*$ explicitly as a smooth projective curve over $\overline{\mathbb{Q}}$ whose Jacobian $J(C_*)$ carries the same $\mathbb{Q}(i)$-endomorphism structure as $A_*$, so the Beauville synthesis "Hodge on $A_*$ ⇒ BSD on $J(C_*)$" has an object to apply to.**

---

## §1. What Beauville's synthesis actually says

From Beauville 1983 (*"Variétés Kähleriennes dont la première classe de Chern est nulle"*) and subsequent work (Deligne's modular interpretation; Schoen 1988; van Geemen 2001):

> **Theorem (Beauville, form we need).** Let $A$ be an abelian variety of Weil type $(p,q)$ with $\operatorname{End}^0(A) = \mathbb{Q}(i)$. There exists a curve $C_A$ over $\overline{\mathbb{Q}}$ (the *Beauville curve* attached to $A$), a morphism $\pi_A : A \to J(C_A)^{\oplus k}$ of abelian varieties, and a compatible polarization, such that:
>
> (a) The Hodge conjecture for $A$ implies the *algebraicity of certain cycle classes* on $A \times J(C_A)$, which in turn implies
>
> (b) The L-function of $J(C_A)$ factors as a product involving $L(A, s)$ and symmetric-power L-functions of $A$, and
>
> (c) The Beauville rank conjecture on $A$ (rank $\geq 3$ for the relevant cycles) is equivalent to a statement about the order of vanishing of $L(J(C_A), s)$ at $s = 1$, which under the Bloch–Kato / Tate conjectures is BSD on $J(C_A)$.

The key phrase is **"Beauville curve attached to $A$"**. For a general $A$ of Weil type, $C_A$ is constructed via a moduli argument (Deligne's interpretation via Shimura varieties) and is NOT automatically given by explicit equations. **Part of Sprint 35b is to write down $C_*$ for $A_*$ specifically.**

---

## §2. What's known for $A_*$ structurally

From the atlas (`Atlas/MASTER_ATLAS_v3_5_2026_04_18.md` §9) and S29/S33:

- $A_* = \mathbb{C}^4 / (\mathbb{Z}^4 + \Omega\mathbb{Z}^4)$, $\Omega = \tfrac{1}{2}I_4 + i(\sqrt{2}I_4 + \sqrt{3}M_2 + \sqrt{5}M_3)$.
- $\operatorname{End}^0(A_*) = \mathbb{Q}(i)$, Weil signature $(2,2)$.
- $\dim A_* = 4$, so $C_*$ should be of genus $g$ with $J(C_*)$ admitting $A_*$ as an isogeny factor. From Beauville's formula, $g = 4 \cdot (\text{multiplicity factor}) = $ **likely 5 or 9** depending on the precise moduli interpretation.

**Working hypothesis:** $C_*$ is a genus-5 curve with an involution $\iota$ such that $J(C_*)^- \cong A_*$ (Prym variety construction).

---

## §3. Concrete construction plan — 3 paths

### §3.1 Path A — Prym variety from a double cover

Attempt: find a genus-5 curve $C'$ with an involution $\iota$ whose Prym variety $P(C'/\iota)$ is isogenous to $A_*$.

**Steps:**

1. From the CM-type and Weil signature of $A_*$, compute the expected dimension of the Prym: $\dim P = g - g' = 5 - 1 = 4$. ✓
2. Use Deligne's recipe: given the abelian variety parameters ($\Omega$, $\mathbb{Q}(i)$-action), write the universal Prym moduli map and compute the image.
3. **Output:** explicit equations for $C'$ (likely a plane quintic or hyperelliptic-with-involution).

**Difficulty:** moderate — this is a classical construction but the concrete $\Omega$ makes it fiddly.
**Output file:** `construct_Cstar_prym.py` computing $C'$ from $\Omega$.

### §3.2 Path B — Moduli-theoretic via Shimura variety

Attempt: identify $A_*$ as a point on the Shimura variety $Sh_{GU(2,2)}$, then extract $C_*$ as the universal curve over that point.

**Steps:**

1. Compute the Shimura reflex field for $A_*$: expected $\mathbb{Q}(i, \sqrt{2}, \sqrt{3}, \sqrt{5})$ or a subfield.
2. Use the explicit moduli coordinates (Siegel 4-fold coordinates) to locate $[A_*]$.
3. Pull back the universal curve $\mathcal{C}$ on $Sh$ to the specific point.

**Difficulty:** higher — requires machinery (explicit Shimura moduli is not routine).
**Output file:** `construct_Cstar_shimura.md` with the moduli computation.

### §3.3 Path C — Direct period-matrix matching (pragmatic)

Attempt: parametrize genus-$g$ curves with $\mathbb{Q}(i)$-action on their Jacobians, and search for one whose period matrix equals $\Omega$ up to isogeny.

**Steps:**

1. For $g \in \{4, 5, 6, 7, 8\}$, enumerate curves with $\mathbb{Q}(i)$-action:
   - Hyperelliptic $y^2 = f(x)$ with $f$ symmetric under a specific $\mu_4$ action.
   - Cyclic covers $y^4 = f(x)$.
   - Plane quartics/quintics with extra automorphisms.
2. For each candidate, compute the period matrix numerically to high precision.
3. Match against $\Omega$ (up to $GL_n(\mathbb{Z})$ isogeny).

**Difficulty:** computational but concrete.
**Output file:** `search_Cstar_periods.py` with the enumeration + matching.

---

## §4. Deliverables for Sprint 35b

Minimum (to trigger Sprint 35c):

1. **Explicit $C_*$** — equations defining the curve over some number field $F \subset \overline{\mathbb{Q}}$.
2. **Explicit $\pi_* : A_* \to J(C_*)$** — morphism of abelian varieties (integer 8 × 2g matrix over an integrality structure).
3. **Numerical verification** — period matrix of $C_*$ matches $\Omega$ up to isogeny at 200 dps.
4. **Beauville rank matrix** — 3 × 3 or larger rank-structure matrix whose vanishing is the Beauville conjecture on $A_*$.

Optional (for deeper rigor):

5. **Galois descent** — conditions under which $C_*$ is defined over a smaller field.
6. **Explicit morphism of L-functions** — Euler product identification $L(A_*, s) \cdot (\text{symmetric terms}) = L(J(C_*), s)$.

---

## §5. Expected timeline

- **Week 1:** Literature pass. Re-read Beauville 1983, Schoen 1988, van Geemen 2001 (for explicit Weil-type constructions), Birkenhake–Lange Ch. 10.
- **Week 2:** Try Path A (Prym construction) first — most concrete.
- **Week 3:** If Path A fails, try Path C (period matching).
- **Week 4:** If both fail, Path B (Shimura, requires more machinery) as fallback.

**External dependency:** Path B realistically needs a mathematician comfortable with Shimura varieties (Colmez, Deligne references) — possible handoff to ChatGPT for literature scouting + ClaudeChat for structural review.

---

## §6. What Sprint 35b does NOT do

- Does NOT close BSD on $J(C_*)$ (that's Sprint 35c).
- Does NOT generalize to arbitrary Weil 4-folds (specific to $A_*$).
- Does NOT re-prove Beauville's theorem (takes it as a black-box result).
- Does NOT update atlas status (atlas stays `[gold-with-gap]` until Sprint 35c closes BSD).

---

## §7. Interface with Sprint 35a

Sprint 35a deterministic rank = 70 establishes $W_* \cap \mathbb{Q}^{70} = \{0\}$.

Via S29 R1-KE: every rational Hodge class on $A_*$ is K-invariant, hence algebraic.

**This is the hypothesis Beauville's synthesis requires.** Sprint 35b then builds $C_*$ explicitly so we have an object on which Beauville's theorem applies in Sprint 35c.

$$\underbrace{\text{S35a: Hodge on } A_*}_{\text{deterministic after v3}} \;\xrightarrow{\text{Beauville black box}}\; \underbrace{\text{rank structure on } A_*}_{\text{on explicit } C_*}  \;\xrightarrow{\text{Sprint 35c}}\; \underbrace{\text{BSD on } J(C_*)}_{\text{one concrete variety}}$$

---

## §8. Routing

**Action requested:**

1. Brayden — green-light Path A as starting point (or override).
2. ChatGPT — literature scout for explicit Prym constructions of Weil-type 4-folds (Birkenhake–Lange §10, Schoen 1988, Gritsenko–Nikulin; look for "$\mathbb{Q}(i)$-action on Jacobian").
3. ClaudeChat — structural review of this plan; flag any gap in the Path A pipeline before code gets written.
4. ClaudeCode — once Path A is green-lit, write `construct_Cstar_prym.py` (~300 LOC).

---

## §9. One-sentence charter

**Sprint 35b writes down one specific curve $C_*$ whose Jacobian carries $A_*$ as a direct factor (or a Prym factor), so that Beauville's synthesis becomes an applicable theorem rather than an abstract implication.**

---

*© 2026 Brayden Ross Sanders / 7Site LLC. 7Site Human Use License v1.0. DOI: 10.5281/zenodo.18852047.*
