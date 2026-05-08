# Falsifier List
## What Would Break the 3-Layer Tower Claim

---

## How to Read This List

Each falsifier is a specific, concrete observation that, if true, would invalidate some part of the theorem. The falsifiers are grouped by which layer of the claim they attack.

Testing a falsifier requires a specific computation or comparison. No metaphysical refutation is relevant.

---

## Category A: Cell-Level Falsifiers

**A1. A single cell mismatch.**

If for any $(x,y) \in \mathbb{Z}/10\mathbb{Z} \times \mathbb{Z}/10\mathbb{Z}$, the tower's output $\mathsf{T}(x,y)$ differs from the published TSML $T(x,y)$, the theorem is false as stated.

Currently: 100/100 cells match. No mismatch known.

**A2. The published TSML is different from what was read.**

The theorem relies on the TSML table as published. If the CK framework's TSML differs from what I read in the image (e.g., a typo or misreading), some cells might mismatch. Test: recomputing from CK source code.

**A3. Published TSML has different conventions.**

If the table is transposed, indexed differently (1-indexed vs 0-indexed), or represents a non-commutative operation, the direct comparison fails. Test: verify commutativity holds in the published table ($T(x,y) = T(y,x)$ everywhere).

---

## Category B: Domain-Level Falsifiers

**B1. Overlapping domains.**

If $S_{\text{MAX}} \cap S_{\text{ADD}} \ne \emptyset$, priority ordering matters and the disjoint-domain guarantee fails.

Currently: Lemma 1 gives $S_{\text{MAX}} \cap S_{\text{ADD}} = \emptyset$ by construction ($S_{\text{ADD}}$ contains 1 by definition; $S_{\text{MAX}}$ does not).

**B2. Incomplete coverage.**

If $S_{\text{MAX}} \cup S_{\text{ADD}} \ne S$, some seam cells fall through to $C_0$, which would give 7 (mismatch). Test: verify $|S_{\text{MAX}}| + |S_{\text{ADD}}| = |S| = 8$.

Currently: $|S_{\text{MAX}}| = 6, |S_{\text{ADD}}| = 2$, sum = 8. ✓

**B3. Hidden cell outside named domains.**

If the tower fails to cover some $(x,y) \in R^2 \setminus (S_{\text{MAX}} \cup S_{\text{ADD}})$, the tower is incomplete. Test: verify every cell is covered by exactly one of $D_0 = R^2 \setminus S$, $D_1 = S_{\text{MAX}}$, $D_2 = S_{\text{ADD}}$.

Currently: $|D_0| + |D_1| + |D_2| = 92 + 6 + 2 = 100 = |R^2|$. Lemma 2 establishes disjoint partition.

---

## Category C: Rule-Level Falsifiers

**C1. $C_0$ is ambiguous.**

If two rules in the canonical construction contradict each other for some cell, $C_0$ is ill-defined. Test: verify the three sub-rules (DEFAULT, V0, shell-stability) never conflict on any cell.

Currently: DEFAULT is the base; V0 overrides only on cells with a 0 coordinate; shell-stability overrides only on core × core with different shells. The shell-stability domain excludes V0's domain (neither 0 nor 1 is in the core). Rules compose cleanly.

**C2. The HARMONY exception at (0, h) is ad hoc.**

The exception "$(0, h) = (h, 0) = h$" is necessary to match the published TSML but does not follow from ring axioms. If this were actually an ECHO-style exception rather than a canonical one, the count would shift from 92/100 to 90/100. Test: justify or drop the HARMONY exception.

Currently: the exception is kept and labeled as such. It is ring-specific (depends on the choice of $h$), and it is an honest piece of ring-specific data. Whether to consider it "canonical" is a labeling choice.

**C3. Shell partition is ambiguous for some element.**

If any unit $u$ has more than one possible shell value (e.g., from different definitions of $\sigma$), the shell-stability rule is ill-defined. Test: verify $\sigma(u) = v_2(3u+1)$ is well-defined for each $u \in U(R)$.

Currently: $v_2$ is uniquely defined for positive integers, and $3u+1 > 0$ for $u > 0$. No ambiguity.

**C4. MAX or ADD violates commutativity.**

$\max(x,y) = \max(y,x)$ and $(x+y) \bmod n = (y+x) \bmod n$ are both commutative. The published TSML is commutative. If MAX were replaced with a non-commutative rule, the tower would mismatch on ordered pairs. Currently: no issue.

---

## Category D: Minimality / Uniqueness Falsifiers

**D1. An alternative equally minimal decomposition exists.**

If another 3-rule decomposition has the same description length but uses different rules (e.g., multiplicative + ADD), the uniqueness of the tower is questionable.

Currently: I tested MAX, ADD, MULT, MIN on the 8-entry residue. Only the combination MAX (non-1 edges) + ADD (1-edges) gives 8/8. No equally compact alternative decomposition has been found. But uniqueness has not been proved.

**D2. A smaller decomposition exists.**

If some 2-rule decomposition or a single-rule decomposition recovers TSML, the 3-layer tower is suboptimal.

Currently: no single rule covers all of TSML. Any 2-rule decomposition would need to handle 100 entries between 2 rules, which implies one rule covers ≥ 50 cells. The canonical construction at layer 0 covers 92, leaving 8 for layer 1. But then the 8 residue cells follow two distinct rules, not one. A 2-rule decomposition would require a unified rule on the 8 residue cells, which we showed does not exist among tested rules.

**D3. Different attractor choice gives a better match.**

$C_0$ depends on the choice of $h = 7$. If $h' \ne 7$ gives a better match against the published TSML, the choice $h = 7$ is not canonical.

Currently: $h = 7$ was chosen as the largest shell-1 element in $U(R)$ and matches the framework's HARMONY attractor. Alternative choices have not been tested but would produce different $C_0$ outputs that would not match published TSML.

---

## Category E: Semantic Dependency Falsifiers

**E1. The choice of $h$ depends on hidden semantic information.**

The theorem uses $h = 7$. If this choice is motivated by the CK framework's operator semantics (HARMONY = 7) rather than ring structure alone, the theorem is semantically dependent.

Currently: the rubric "largest shell-1 element in $U(R)$" produces $h = 7$ for Z/10Z algorithmically. However, for other rings, this rubric may produce different values that may or may not match framework semantics.

**E2. The shell partition $\sigma$ depends on hidden semantic information.**

If $\sigma$ were defined differently (e.g., by a different 2-adic valuation or a different flow), the theorem would predict different entries. Test: verify $\sigma$ is fully specified by the stated formula.

Currently: $\sigma(u) = v_2(3u+1)$ is fully specified.

**E3. The seam residue $S$ is defined post-hoc.**

$S$ is identified as "where $C_0$ disagrees with published TSML." If one did not have access to the published TSML, one could not know $S$ in advance. This means the theorem as stated is conditional on knowing $T$.

Currently: this is acknowledged in the Notation Sheet ("S is given data, not derived from ring axioms"). The theorem is a reconstruction theorem, not a prediction theorem.

---

## Category F: Generalization Falsifiers (Outside Theorem Scope)

These would not falsify the Z/10Z theorem but would falsify stronger claims made informally:

**F1. Another ring in the compatibility family has a published TSML that does not decompose as a 3-layer tower.**

Would falsify the conjecture that the tower structure generalizes. The theorem spine is unaffected since it is scoped to Z/10Z only.

**F2. The branch-rule mapping (identity→ADD, others→MAX) does not hold in another ring.**

Would falsify the conjecture that the mapping generalizes. Again, the theorem spine is not affected.

**F3. The 3-layer structure is specific to Z/10Z and requires semantic input.**

Would formally establish that the tower is Z/10-specific, not a general ring-theoretic phenomenon. The theorem spine (narrowly scoped to Z/10Z) remains valid.

---

## Summary: The Theorem Is Robust To

1. **Cell checks:** all 100 verified, any single mismatch would be decisive.
2. **Domain disjointness:** proven by construction.
3. **Rule compositionality:** proven.
4. **Minimality:** tested against flat and 2-component descriptions; tower is smaller.

## The Theorem Is Conditional On

1. **Published TSML values:** as read from the image.
2. **Choice of $h = 7$:** matches framework convention.
3. **Definition of $\sigma$:** $v_2(3u+1)$ as specified.
4. **Seam residue $S$ given as data:** identified post-hoc by comparison.

## The Theorem Does Not Claim

1. **Generalization to other rings:** outside scope.
2. **Uniqueness of decomposition in some absolute sense:** other decompositions may exist.
3. **Semantic content of TSML operators:** not addressed.
4. **BHML:** separate table, separate investigation.
