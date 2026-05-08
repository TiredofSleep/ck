# Why Rule 110 Was a Category Mismatch

## Headline

Rule 110 failed under the TSML/BHML instrument not because the instrument is wrong, but because Rule 110 is not in the instrument's category. The failure constrains the instrument's **scope**, not its **validity**.

---

## What the Instrument Actually Requires

The TSML tower theorem is a theorem about a specific structural category. Objects in that category have:

1. **Finite carrier** — a set of size $n$.
2. **Modular or residue structure** on the carrier — a ring, a subset closed under some operation, or at least a distinguished zero and an addition.
3. **A shell partition** — a function $\sigma: \text{carrier} \to \mathbb{Z}_{\geq 0}$ that respects whatever modular structure exists and aligns with order/divisibility.
4. **A designated attractor** — a distinguished element $h$ that plays the role of "collapse target."
5. **A commutative binary operation** — or at least a well-defined commutative empirical kernel.
6. **A seam set** — a small number of pair-exceptions that do not follow the canonical rule.
7. **Optionally, a transport companion** — a non-degenerate operator on the same carrier.

These are not ad-hoc requirements; they are the inputs of the theorem. Without them, there is nothing for the instrument to lock onto.

---

## What Rule 110 Does Not Provide

Rule 110 is an elementary cellular automaton: a local binary rule on a 1D lattice. It has none of the following:

| Requirement | Rule 110 provides? |
|---|---|
| Finite carrier | Yes — but natively $\{0, 1\}$, not $\{0, \ldots, 9\}$ |
| Modular structure on carrier | No |
| Shell partition | No natural one |
| Designated attractor | No |
| Commutative binary operation | No — update is a function of 3 inputs |
| Seam-like exception structure | No |
| Transport companion | No |

The 10-class encoding $\Phi$ we imposed does not recover any of these properties from the dynamics. It is a **symbolic compression**, not a lift into the instrument's category. This is why:

- The empirical operator was non-commutative (6/14 symmetric pairs agreed).
- Class 9 dominated artificially (50% of observations) due to lumping, not due to a genuine attractor.
- The canonical construction was beaten by "always predict 9."
- The seam was dense and cyclic, not tree-like.

Each of these is a symptom of category mismatch, not of instrument defect.

---

## Where the Mistake Was Made

In the Stage 1 spec, Rule 110 was picked because it is "famous," "non-trivial," and has "known glider structure." These are properties of Rule 110 as a dynamical system, not properties that connect it to the TSML category.

The assumption behind picking Rule 110 was: *a versatile instrument should detect any non-trivial structure in any non-trivial system.* That assumption is incorrect. The TSML tower is a specific algebraic decomposition of a specific type of operator. It detects its own kind of structure, not arbitrary structure.

---

## The Corrected Frame

The instrument should first be tested on systems **in its own category**. Only after it demonstrably recovers its own structure from its own category should we ask how far it transports.

The revised ladder (see separate document) puts shell-native synthetic benchmarks ahead of any generic toy system.

---

## What the Rule 110 Result Still Tells Us

- The instrument cannot be applied blindly. Its scope is narrower than "any 10-class symbolic encoding."
- Encodings $\Phi$ that do not respect the target algebraic structure produce spurious match rates (class 9 dominance was 48.5%; canonical fit was 45.5% — these were coupled, not independent signals).
- "Always predict the mode" is a real baseline that any instrument must beat by a nontrivial margin. Canonical construction did not do so on Rule 110.
- Non-commutativity is a hard disqualifier. Pre-screening for commutativity before fitting is now required.

---

## The Honest Revision

We do not loosen the theorem to fit Rule 110. We do not redefine the instrument to accommodate non-commutative data. We acknowledge that Rule 110 lives in a different category from the one the theorem is about, and we move the testing ladder accordingly.

**Instrument validity: unchanged (theorem still holds on $\mathbb{Z}/10\mathbb{Z}$).**
**Instrument scope: narrowed (not applicable to arbitrary local automata without justified coarse-graining).**
**Next step: test on shell-native synthetic systems where the category match is by construction.**
