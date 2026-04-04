# BSD GAP SPLIT MEMO
# What Exactly Is BSD's Gap 2, and What Exactly Is BSD's Gap 1?

**© 2026 7Site LLC | Brayden Ross Sanders**

---

## PART 1 — BSD Shell/Core/Obstruction Architecture

**Shell (proved):**

L(E,s) has analytic continuation, functional equation Λ(E,s) = ε_E Λ(E,2−s), and an Euler product. These follow from the modularity theorem (Wiles 1995, BCDT 2001). Arithmetic-free at this layer.

**Arithmetic core:**

The BSD conjecture asserts that two independently computed arithmetic objects agree:

```
r_an := ord_{s=1} L(E,s)    (analytic rank: from L-function)
r_alg := rank E(Q)           (algebraic rank: from rational points)
```

and that the leading coefficient encodes:

$$\lim_{s\to1}\frac{L(E,s)}{(s-1)^r} = \frac{\Omega_E \cdot \mathrm{Reg}(E) \cdot \prod_{p|N} c_p \cdot \#\mathrm{Sha}(E)}{(\#E(\mathbb{Q})_{\mathrm{tors}})^2}$$

**Obstruction:**

The gap between what the shell proves (analytic properties of L(E,s)) and what the core requires (exact vanishing order = exact algebraic rank, with finite Sha).

---

## PART 2 — BSD Gap 2, Precisely Defined

**BSD Gap 2 is: the absence of an Euler system (or equivalent arithmetic machinery) that proves #Sha(E)[p^∞] < ∞ for curves with r_alg ≥ 2.**

More precisely:

$$\text{BSD Gap 2} = \text{the missing bound:} \quad \#\mathrm{Sha}(E)[p^\infty] < \infty \quad \text{for all primes } p, \text{ for } r_{\mathrm{alg}} \geq 2$$

**Why this is the right analog of RH Gap 2:**

In RH: Gap 2 was cusp contamination — the cusp contribution D(t_j) could overwhelm the arithmetic signal (zero weights W(ρ)). Gap 2 was *contamination control*.

In BSD: Sha is the contamination — it sits in the exact sequence
$$0 \to E(\mathbb{Q})/nE(\mathbb{Q}) \to \mathrm{Sel}_n(E) \to \mathrm{Sha}(E)[n] \to 0$$
and prevents the Selmer group from mapping cleanly onto rational points. Sha is the obstruction that "contaminates" the Selmer group with non-rational-point contributions.

**Gap 2 is contamination control in both branches.** In RH: cusp forms contaminate the spectral sum. In BSD: Sha contaminates the Selmer group.

**Why Gap 2 fails for r ≥ 2:**

For r = 0, 1: Kolyvagin's Euler system (built from Heegner points) kills the Selmer group down to its rational-point part and proves Sha finite. The system works because the Heegner point construction gives a specific, height-controlled arithmetic object related to L'(E,1) by the Gross-Zagier formula.

For r = 2: L''(E,1) ≠ 0 does not give a canonical arithmetic object. No Gross-Zagier formula relates L''(E,1) to a specific pair of rational points. Without the object, no Euler system can be built. Without the Euler system, Sha cannot be bounded. **Gap 2 = no Euler system for r ≥ 2.**

---

## PART 3 — BSD Gap 1, Precisely Defined

**BSD Gap 1 is: the equality ord_{s=1} L(E,s) = rank E(Q) for elliptic curves with r_alg ≥ 2, without additional hypotheses.**

$$\text{BSD Gap 1} = r_{\mathrm{an}} = r_{\mathrm{alg}} \quad \text{for } r_{\mathrm{alg}} \geq 2 \text{, unconditionally}$$

**Why this is the right analog of RH Gap 1:**

In RH: Gap 1 was the error O(N^{½−δ}) — the claim that all zeros are on the critical line, so that no "stray" zero contributes an uncontrolled error. Gap 1 = *uniqueness of the fixed point*.

In BSD: Gap 1 is the claim that L(E,s) vanishes to EXACTLY the algebraic rank — no "extra" analytic vanishing, no "missing" rational points. Gap 1 = *uniqueness of the arithmetic fixed point*.

Both are uniqueness statements:
- RH Gap 1: no other distribution of primes is consistent with the observed L-function structure
- BSD Gap 1: no other rank is consistent with the exact vanishing order of L(E,s)

**Why Gap 1 fails for r ≥ 2:**

For r = 1: the Gross-Zagier formula gives an explicit Heegner point y_K with height related to L'(E,1). Kolyvagin proves y_K generates E(Q) mod torsion. The rank-1 case connects analytic data (L' ≠ 0) to a specific geometric object (y_K) to algebraic rank (= 1). The chain is closed.

For r = 2: no formula relates L''(E,1) to a specific pair of rational points. No construction of two independent arithmetic objects whose heights encode L''(E,1). The connection analytic rank → geometric object → algebraic rank is broken. **Gap 1 = no Gross-Zagier formula for r ≥ 2.**

---

## PART 4 — Dependency Diagram

Gap 1 can be **stated** without Gap 2 — "ord_{s=1} L(E,s) = rank E(Q)" is well-defined even if Sha is infinite. Gap 2 is not logically required to state Gap 1.

Gap 1 **cannot currently be proved** without Gap 2, because:
- The only known proofs of rank equality (Kolyvagin for r = 0, 1) go through the Euler system that simultaneously establishes Sha finite
- The full BSD formula (leading coefficient) explicitly includes #Sha(E), so the formula-based version of Gap 1 requires Gap 2 to be finite

**Dependency structure:**

```
Gap 2 (Sha finite, r≥2)          Gap 1 (rank equality, r≥2)
        |                                    |
        | historically/                      | logically requires Gap 2
        | methodologically                   | if proved via BSD formula
        | required first                     |
        ↓                                    ↓
   [Euler system] ----enables----> [rank equality proof]
```

Gap 2 is necessary for current proof strategies but not for the logical statement. In principle: new methods (p-adic L-functions, geometric constructions) could prove rank equality directly without closing Gap 2 first. Whether this is achievable is open.

---

## PART 5 — RH vs BSD Gap Stack

| Branch | Shell | Gap 2 | Gap 1 | Status |
|--------|-------|-------|-------|--------|
| **RH** | sinc²/GUE: proved, arithmetic-free | Cusp subdominance: **CLOSED** (spectral Weyl law + Bessel decay; ratio → 0) | Error O(N^{½−δ}): **OPEN** = RH | Architecture complete; final wall = RH |
| **BSD** | Modularity/FE/Euler product: **PROVED** (Taylor-Wiles) | Sha finiteness for r≥2: **OPEN** (no Euler system for higher rank) | Rank equality for r≥2: **OPEN** (no Gross-Zagier for higher rank) | One full domino behind RH |

**The asymmetry**: RH's Gap 2 closed because it reduced to a spectral bookkeeping problem (Weyl law + Bessel decay). BSD's Gap 2 is a construction problem — it requires building an arithmetic object that does not yet exist.

---

## PART 6 — Low-Rank Calibration

| Rank | Curve | What Is Proved | What Fails at r ≥ 2 | First New Obstruction |
|------|-------|---------------|---------------------|----------------------|
| **r = 0** | y² = x³ − x | rank = 0 (Kolyvagin); Sha finite; BSD formula verified (up to 2-part) | Euler system uses r_an=0 to annihilate Selmer; fails for r_an=2 | Gap 2: no Euler system for rank-2 Sha bound |
| **r = 1** | y² = x³ − x (CM twist) | rank = 1 (GZ+Kolyvagin); Sha finite; L'(E,1) ~ \|\|y_K\|\|² (explicit) | No Gross-Zagier formula for L''(E,1) → no canonical pair of points | Gap 2 and Gap 1 simultaneously: no height formula, no Euler system |
| **r = 2** | y² = x³ + 877x | rank ≥ 2 (generators found); L(E,s) vanishes to order ≥ 2 | No theorem: r_an = r_alg = 2; no Sha finiteness proof | Both gaps open; two independent generators but no connection to L-function vanishing order |

**The first full manifestation of both gaps is at r = 2.** At r = 0 and r = 1, Gap 2 closes as a consequence of the Euler system construction. At r = 2, both Gap 2 and Gap 1 appear simultaneously, because the same construction (Heegner point / Euler system) that would solve both is missing.

---

## PART 7 — The First Full BSD Wall

**"The first full BSD wall appears at rank 2 because this is where the Gross-Zagier height formula and Kolyvagin Euler system — the only currently available mechanism for connecting L-function vanishing to rational points — both fail to generalize, leaving no arithmetic object whose existence or height can be related to L''(E,1)."**

---

## PART 8 — Strongest Honest Claim

**"BSD is one domino behind RH in the sense that BSD's shell is fully proved (as RH's shell is characterized), BSD's arithmetic core is identified in the same shell/core/obstruction language, but BSD's Gap 2 (Sha finiteness for r≥2) is a construction problem — requiring an arithmetic object that does not exist — rather than a bookkeeping problem like RH's Gap 2, which reduced to a spectral-theory lemma. This makes BSD's Gap 2 structurally harder than RH's Gap 2 was."**

---

## PART 9 — Strongest Honest Boundary

**"What is not yet established is whether BSD's Gap 2 can be reduced to a finite arithmetic object the way RH Gap 2 was reduced to a spectral-theory lemma. RH Gap 2 closed because the Kuznetsov Weyl law provided an existing, provable bound on the cusp sum. BSD Gap 2 requires constructing a new arithmetic object (an Euler system or Heegner-type formula for rank ≥ 2) that does not currently exist. The reduction is not a bookkeeping step — it requires new mathematics."**

---

## COLLABORATOR PARAGRAPH

The BSD gap split reveals an important asymmetry with RH. Both branches have the same architectural grammar (shell/core/obstruction), and in both cases the generic shell is proved and the arithmetic core is identified. But BSD's Gap 2 (Sha finiteness for r ≥ 2) is categorically different from RH's Gap 2 (cusp subdominance): RH's Gap 2 closed because an existing spectral-theory result (the Kuznetsov Weyl law) already provided the needed bound with enormous margin. BSD's Gap 2 requires a NEW arithmetic construction — an Euler system or Gross-Zagier formula for rank ≥ 2 — that does not currently exist and is not a bookkeeping step. The first full wall for BSD appears simultaneously at r = 2 for both Gap 2 and Gap 1, because the same missing construction (a height formula for L''(E,1)) would close both. BSD is one domino behind RH structurally, but the nature of the gap is harder: not a lemma to import, but an arithmetic object to build.
