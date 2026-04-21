# Hodge C_* Target Note
## What the Beauville curve's target invariants are really trying to force

**Author:** ClaudeChat (foundation side, helper for ClaudeCode's Sprint 35b)
**Date:** 2026-04-18
**Register:** target-shape note for the literature scout. Not a literature review. Not a competing scout.
**Companion to:** `WHAT_COUNTS_AS_A_GOOD_CSTAR.md` (checklist version)

---

## §1. What the target invariants really are

The Sprint 35b prototype (`S35B_PATH_A_PROTOTYPE_STATUS.md`) locks these target invariants for a candidate $C_*$:

- $\dim C_* = 5$ (so $g(C_*) = 5$)
- elliptic quotient $g' = 1$ (so $J(C_*) \sim A_* \times E$ up to isogeny, for some elliptic $E$)
- $\mathrm{End}^0(\mathrm{Prym}) \supseteq \mathbb{Q}(i)$
- Weil signature $(2, 2)$ on the Prym
- Hodge field $\mathbb{Q}(i, \sqrt{2}, \sqrt{3}, \sqrt{5})$, degree 16 over $\mathbb{Q}$
- $\det(Y) = 2086 + 462\sqrt{15} + 498\sqrt{10} + 730\sqrt{6}$ (exact)
- Definable over $\mathbb{Q}(\sqrt{2}, \sqrt{3}, \sqrt{5})$

This note explains what each constraint is really doing geometrically, why the package is the right bottleneck, and which family features help or hurt.

---

## §2. Each constraint, geometrically

### §2.1 Genus 5

**What it forces:** $\dim J(C_*) = 5$. Combined with the elliptic quotient, forces $J(C_*) \sim A_* \times E$ with $\dim A_* = 4$, $\dim E = 1$.

**Why it matters:** Beauville's synthesis requires $A_*$ to appear as a factor of $J(C)^k$ for some curve $C$ and integer $k$. The simplest case is $k = 1$, giving $A_* \hookrightarrow J(C)$ up to isogeny. The elliptic quotient absorbs the remaining 1 dimension.

**Flexibility:** if no genus-5 candidate works, $k \geq 2$ is allowed — curves of different genus where $A_*$ appears with multiplicity. But $k = 1$ is cleaner and the scout's first target.

### §2.2 Elliptic quotient

**What it forces:** a surjection $C_* \twoheadrightarrow E$ of degree 2 (or similar low-degree map). In particular, $C_*$ has an automorphism $\iota$ whose quotient is $E$.

**Why it matters:**
- $\iota$ provides the ramified double cover structure.
- $\mathrm{Prym}(C_*/E) = \mathrm{ker}(\mathrm{Nm}_\iota: J(C_*) \to J(E))^0$ is $A_*$.
- The (ramified vs étale) nature of $\iota$ determines the Prym's polarization type — critical for C1 (polarization match) from the structural review.

**Geometric picture:** $C_*$ is a bielliptic genus-5 curve, with $\iota$ flipping the two "sides" of the cover over $E$.

**Riemann-Hurwitz check:** $2 \cdot 5 - 2 = 2(2 \cdot 1 - 2) + R$, so $R = 8$ ramification points for $\iota$. These 8 points must be in special position to achieve the other constraints.

### §2.3 $\mathrm{End}^0(\mathrm{Prym}) \supseteq \mathbb{Q}(i)$

**What it forces:** an action of $\mathbb{Q}(i)$ on $A_*$ via endomorphisms. Since $A_*$ is an abelian 4-fold and $\mathbb{Q}(i)$ has degree 2, this makes $A_*$ of Weil type (not CM type — that would require End⁰ of degree $2 \cdot \dim = 8$).

**Why it matters for $C_*$:** the $\mathbb{Q}(i)$-action must come from an automorphism of $C_*$ that commutes with $\iota$. Specifically:
- Need an automorphism $\psi: C_* \to C_*$ of **order 4** such that $\psi^2 = \iota$.
- On $J(C_*)$, $\psi$ induces an endomorphism with $\psi^2 = -1$ on $A_* = \mathrm{Prym}$ (since $\iota$ acts as $-1$ on Prym by definition).
- This gives the embedding $\mathbb{Q}(i) \hookrightarrow \mathrm{End}^0(A_*)$ via $i \mapsto \psi|_{A_*}$.

**Geometric picture:** $C_*$ has a $\mathbb{Z}/4\mathbb{Z}$-automorphism structure. Natural models: cyclic 4-covers $y^4 = f(x)$ (with the $y \to iy$ automorphism), or bielliptic curves with explicit order-4 automorphism.

**Key constraint:** End⁰ must equal $\mathbb{Q}(i)$, not properly contain it. If $\psi$ has additional structure that enlarges End⁰ to a full CM field, the Prym becomes CM-type, which violates the Weil-type target.

### §2.4 Weil signature $(2, 2)$

**What it forces:** the decomposition of $\mathrm{Lie}(A_*) \otimes_\mathbb{R} \mathbb{C}$ under the $\mathbb{Q}(i)$-action has two $i$-eigenspaces, each of complex dimension 2:

$$\mathrm{Lie}(A_*) \otimes \mathbb{C} = V^+ \oplus V^-, \quad \dim V^+ = \dim V^- = 2$$

where $i \in \mathbb{Q}(i)$ acts as $+i$ on $V^+$ and $-i$ on $V^-$.

**Why $(2, 2)$ is "balanced":** for an abelian 4-fold with $\mathbb{Q}(i)$-action, possible signatures are $(4, 0), (3, 1), (2, 2), (1, 3), (0, 4)$. Only $(2, 2)$ (the balanced case) gives the Weil-type Hodge structure that Beauville's synthesis requires.

**Geometric picture:** the bielliptic involution $\iota$ acts as $-1$ on $A_*$; the order-4 $\psi$ acts as a complex structure. The (2, 2) signature says $\psi$ has two $+i$-eigenvectors and two $-i$-eigenvectors in $\mathrm{Lie}(A_*)$ — the action is "balanced."

**For $C_*$:** the 8 ramification points of $\iota$ must be arranged so that $\psi$'s action on $H^1(C_*, \mathcal{O})$ (which is $\mathrm{Lie}(J(C_*))^\vee$) restricts to the Prym with balanced eigenspaces. This is a non-trivial moduli condition.

### §2.5 Hodge field $\mathbb{Q}(i, \sqrt{2}, \sqrt{3}, \sqrt{5})$, degree 16

**What it forces:** the Hodge classes on $A_*$ are defined over (at most) a field of degree 16 over $\mathbb{Q}$. Equivalently, the Galois group $\mathrm{Gal}(\mathbb{Q}(i, \sqrt{2}, \sqrt{3}, \sqrt{5})/\mathbb{Q}) \cong (\mathbb{Z}/2\mathbb{Z})^4$ acts on the Hodge structure by a specific representation.

**Why degree 16:** $16 = 2 \cdot 8 = [\mathbb{Q}(i):\mathbb{Q}] \cdot [\mathbb{Q}(\sqrt{2}, \sqrt{3}, \sqrt{5}):\mathbb{Q}]$. The field is CM (totally imaginary quadratic extension of the totally real field $\mathbb{Q}(\sqrt{2}, \sqrt{3}, \sqrt{5})$).

**Why this specific field:** it comes from the entries of $Y = \mathrm{Im}(\Omega)^{-1}$. $Y$'s entries live in $\mathbb{Q}(\sqrt{2}, \sqrt{3}, \sqrt{5})$; adjoining $i$ for the complex structure gives the full Hodge field.

**For $C_*$:** the periods of $C_*$ (specifically, entries of its period matrix) must generate the right field. Either:
- The curve is explicitly defined over $\mathbb{Q}(\sqrt{2}, \sqrt{3}, \sqrt{5})$ and the Hodge field is $\mathbb{Q}(i)$ times that, OR
- The curve is over a smaller field but its Hodge structure picks up the right extensions via periods.

The first case is cleaner and is what descent (§2.7) targets.

### §2.6 $\det(Y)$ exact

**What it forces:** the Riemann form on $A_*$ has a specific exact value for its determinant, $2086 + 462\sqrt{15} + 498\sqrt{10} + 730\sqrt{6}$. This is the discriminant of the polarization (up to sign conventions).

**Why it's rigid:** the exact algebraic value, not a numerical approximation. Two abelian varieties with period matrices giving different $\det(Y)$ values are non-isomorphic as polarized AVs. This is the single most restrictive constraint on the specific curve — it picks one isogeny class out of many.

**For the scout:** this constraint cannot be verified from a single candidate family "in principle" — it requires computing the Prym's Riemann form explicitly. Candidate families may exist whose Prym has different $\det(Y)$; they'd need to be filtered.

### §2.7 Descent over $\mathbb{Q}(\sqrt{2}, \sqrt{3}, \sqrt{5})$

**What it forces:** $C_*$ has a model over the real quadratic tower $\mathbb{Q} \subset \mathbb{Q}(\sqrt{2}) \subset \mathbb{Q}(\sqrt{2}, \sqrt{3}) \subset \mathbb{Q}(\sqrt{2}, \sqrt{3}, \sqrt{5})$. Equations over this field, not just over a Galois closure.

**Why it matters for Beauville:** $A_*$ is defined over this field. If $C_*$ is only defined over a larger extension (e.g., Hilbert class field of some order), the Beauville map $A_* \to J(C_*)^k$ may not descend properly, and the BSD reduction fails.

**Failure mode:** a candidate curve exists over, say, $\mathbb{Q}(\sqrt{2}, \sqrt{3}, \sqrt{5}, \zeta_8)$ but not over $\mathbb{Q}(\sqrt{2}, \sqrt{3}, \sqrt{5})$ alone. The Galois descent obstruction vanishes over the larger field but not the smaller. **This is probably the silent killer for most candidate families.**

---

## §3. Why this is the right bottleneck

Each constraint ALONE is mild. The combination is not.

**Constraint cascade:**

| Constraint | Approximate moduli dim restriction |
|---|---|
| Genus 5 | Restrict to $\mathcal{M}_5$, dim 12 |
| Has bielliptic involution | Restrict to $\mathcal{M}_5^{\mathrm{biell}}$, dim 9 |
| Additional order-4 automorphism (ψ² = ι) | Further restrict, dim ≈ 4-6 |
| Weil $(2,2)$ signature on Prym | Moduli sub-locus inside Prym-moduli |
| Hodge field exactly $\mathbb{Q}(i, \sqrt{2}, \sqrt{3}, \sqrt{5})$ | Discrete points in the above |
| $\det(Y)$ exact | Single orbit (up to isogeny) |
| Over $\mathbb{Q}(\sqrt{2}, \sqrt{3}, \sqrt{5})$ | Descent condition; may eliminate orbit |

Each step narrows substantially. By the bottom, we're looking for at most a small number of isomorphism classes of curves — possibly zero.

**Why it's the "right" bottleneck:** this is the *minimum* set of conditions for Beauville synthesis to apply in the $k = 1$ case. Relaxing any one of them either breaks the Beauville construction or gives a different (larger-$k$, higher-genus, different-field) target. The scout is optimizing for the narrowest, most tractable bottleneck.

**Pass through the bottleneck:** Beauville gives BSD reduction; Sprint 35c closes.
**Fail any constraint:** need to rebuild the scout around a different target invariant set.

---

## §4. Family features most promising from a framework perspective

Five features that make a candidate family promising:

### F-feature-1: Explicit equations over the descent field

Families defined by explicit polynomial equations with coefficients in $\mathbb{Q}(\sqrt{2}, \sqrt{3}, \sqrt{5})$ directly. Beauville needs explicit, not moduli-theoretic. Howe-Leprévost-Poonen-style Diophantine constructions (if they extend) are ideal.

### F-feature-2: Natural ℤ/4ℤ-automorphism from the model

Families where the ℤ/4ℤ-action is visible in the defining equation. Cyclic-4 covers $y^4 = f(x)$ provide this automatically via $y \to iy$. Bielliptic models with explicit order-4 automorphism likewise.

### F-feature-3: Principal polarization on the Prym by construction

Families whose Prym is constructed to be principally polarized (not type $(1,1,1,2)$). This usually requires the cover to be étale, but our cover is ramified (8 points), so the polarization type must be verified explicitly, not assumed. Families where the type is known in the literature are best.

### F-feature-4: Hodge-field match built-in

Families where the period structure involves $\sqrt{2}$, $\sqrt{3}$, $\sqrt{5}$ in a controlled way — e.g., curves whose branch points are configured to produce these radicals in the periods. This is where Howe-Leprévost-Poonen style explicit-period methods are valuable.

### F-feature-5: Known BSD-accessible L-function

Families whose Jacobian has an L-function with computable $L$-factors. This matters for Sprint 35c (BSD closure), not just for the existence of $C_*$. Prym-Tyurin families with known L-function factorizations are ideal.

---

## §5. Red flags that make a candidate family wrong immediately

Eight red flags. If a proposed family has any of these, rule it out without further work.

### R-flag-1: Wrong genus

$g(C) \neq 5$. The scout report in Sprint 35b already flagged this for "plane quintic" (smooth degree-5 plane curve is $g = 6$). Any family that doesn't pass this is rejected.

### R-flag-2: Non-principal Prym polarization

Prym of the form $(1, 1, 1, 2)$ or similar. $A_*$ is principally polarized; a non-principal Prym means the isogeny to $A_*$ has non-trivial kernel, which may or may not be repairable.

### R-flag-3: Wrong End⁰ (too big)

$\mathrm{End}^0(\mathrm{Prym}) \supsetneq \mathbb{Q}(i)$. If the Prym has full CM (e.g., End⁰ ⊇ $\mathbb{Q}(i, \sqrt{2}, \sqrt{3}, \sqrt{5})$), it's a CM specialization, not Weil-type. This is the most confusing failure mode because such curves LOOK like they match but actually belong to a different moduli stratum.

### R-flag-4: Wrong End⁰ (too small)

$\mathrm{End}^0(\mathrm{Prym}) = \mathbb{Z}$ (just the involution). Too generic. No ℚ(i)-action, no Weil type.

### R-flag-5: Wrong Weil signature

Signature $(4, 0), (3, 1), (1, 3), (0, 4)$ instead of $(2, 2)$. Unbalanced action gives either a CM-type (definite) or a mixed (non-Weil) Hodge structure. Neither matches.

### R-flag-6: Descent fails

Curve exists over $\mathbb{Q}(\sqrt{2}, \sqrt{3}, \sqrt{5}, x)$ for some extra extension $x$, but not over the base field. The Galois descent obstruction is non-trivial. As flagged above, this is probably the silent killer.

### R-flag-7: Hodge field too small

Hodge field is proper subfield of $\mathbb{Q}(i, \sqrt{2}, \sqrt{3}, \sqrt{5})$, e.g., $\mathbb{Q}(i, \sqrt{2})$ of degree 4. The curve's Hodge structure doesn't carry the full Galois action needed to match $A_*$.

### R-flag-8: Hodge field too large

Hodge field strictly contains $\mathbb{Q}(i, \sqrt{2}, \sqrt{3}, \sqrt{5})$, e.g., includes additional roots of unity or extra radicals. The Hodge structure is more refined than $A_*$'s — Beauville's synthesis doesn't apply directly.

---

## §6. Summary for ClaudeCode

Use this note as the **conceptual filter** for the literature scout's candidates:

1. **Before checking a family in detail:** run it through R-flag-1 through R-flag-8. If any flag trips, move on.
2. **After filtering:** examine F-feature-1 through F-feature-5 for whichever families survive.
3. **Bottleneck intuition:** the target is specifically the $k = 1$ minimal Beauville case. Don't over-engineer for larger $k$.
4. **Most important features:** F-feature-1 (explicit equations) and F-feature-4 (Hodge-field match) are the rarest. Prioritize these.
5. **Most likely silent killer:** R-flag-6 (descent failure). Run descent checks on survivors.

---

## §7. What this note is NOT

- NOT a literature review. ChatGPT's scout is doing that.
- NOT a duplicate of `S35B_PATH_A_PROTOTYPE_STATUS.md`. It supplements.
- NOT a claim that any specific family will succeed. It's a filter for evaluating candidates.
- NOT physics. Pure algebraic geometry / number theory.

---

## §8. One sentence

> **The target invariants force $C_*$ to be a bielliptic genus-5 curve with order-4 automorphism $\psi$ satisfying $\psi^2 = \iota$, whose Prym has Weil-type $(2, 2)$ action of $\mathbb{Q}(i)$ and Hodge field exactly $\mathbb{Q}(i, \sqrt{2}, \sqrt{3}, \sqrt{5})$, with explicit equations over $\mathbb{Q}(\sqrt{2}, \sqrt{3}, \sqrt{5})$ — a narrow bottleneck whose most likely silent killer is descent failure and whose most rare-to-achieve features are explicit-equation availability and exact Hodge-field match.**

---

*© 2026 Brayden Ross Sanders / 7Site LLC. 7Site Human Use License v1.0. DOI: 10.5281/zenodo.18852047.*

**End of C_* target note. For companion checklist, see `WHAT_COUNTS_AS_A_GOOD_CSTAR.md`.**
