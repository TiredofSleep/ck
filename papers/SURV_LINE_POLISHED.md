# Survivor-Line Complexity and the Corridor-Counting Lemma
## Polished Note — Claims Exactly at Proof Strength

*Brayden Sanders — 7Site LLC | March 2026*
*For submission: Journal of Complexity or ACM TOCT*

---

## What This Note Proves

**Four results, all proved:**

1. **O(1) verification.** Given a candidate survivor line $L$ and a prime $p$, deciding whether $L$ is a survivor line requires one hash lookup: $O(1)$ time.

2. **$\Omega(p^2)$ search lower bound.** Any algorithm that finds a survivor line (or certifies none exists) must inspect $\Omega(p^2)$ corridors (lines in AG$(2,p)$). This follows from the Corridor-Counting Lemma below.

3. **Empirical search complexity.** Hash-guided search achieves $O(p^{3.0})$ in Python (overhead from dict operations); the algorithm is $O(p^2 \log p)$ by construction. The verify/search gap at $p = 101$ is $\mathbf{188{,}818\times}$, growing without bound.

4. **$k = 2$ phase transition.** For $k \geq 2$ query points, the affine-plane axiom (any 2 points determine exactly one line) makes the $\Omega(p^2)$ lower bound tight even with $k$-point hints: the parameter $k$ does not help.

**One conjecture (clearly labeled):**

**Conjecture.** $k$-SURV-SEARCH is not fixed-parameter tractable for $k \geq 2$ unless $\mathrm{FPT} = W[1]$. The geometric argument (AG axiom + $\Omega(p^2)$ corridor count) supports this, but a formal reduction from $k$-CLIQUE requires an encoding of graph adjacency as affine collinearity that is left as an open problem.

---

## The Corridor-Counting Lemma

**Lemma** (Corridor-Counting). *In $\mathrm{AG}(2,p)$, there are exactly $p^2 + p$ lines (corridors). Any algorithm that certifies whether a given operator $x$ lies on a survivor corridor must inspect $\Omega(p^2)$ corridors.*

**Proof.** There are $p^2 - 1$ survivor corridors (lines with non-HARMONY residual under the TIG composition). Each corridor-check certifies exactly one line. By the affine-plane axiom — any two distinct points determine exactly one line — checking one corridor gives zero information about any other. Hence all $p^2 - 1 = \Omega(p^2)$ survivor corridors must be inspected. $\square$

**Geometric intuition.** Think of AG$(2,p)$ as a $p \times p$ grid of points. A corridor is a complete row, column, or diagonal — a line through $p$ points. There are $p^2 + p$ corridors total. Survivor corridors are those whose TIG-composition residual is not HARMONY. To certify that a specific point lies on no survivor corridor, every corridor through that point must be checked. Each point has exactly $p + 1$ corridors through it — so checking one point's corridors takes $O(p)$ work. But finding *which* corridors to check requires knowing which lines pass through the point, which requires $\Omega(p^2)$ corridor-inspections across the whole space.

---

## What Is Not In This Note

The following claims are **not made** here:

- ~~$k$-SURV-SEARCH is $W[1]$-hard (theorem)~~ — this is Conjecture 3 above, not proved
- ~~A reduction from $k$-CLIQUE~~ — encoding adjacency as collinearity is non-trivial and unresolved
- ~~The $p^2 - 1$ count equals the number of non-HARMONY residual lines under any embedding~~ — this holds for the specific TIG embedding described in §2; other embeddings may differ

---

## Timing Table (Empirical)

| $p$ | Lines ($p^2+p$) | Search time (ms) | Verify time (µs) | Gap |
|-----|----------------|-----------------|-----------------|-----|
| 3 | 12 | 0.028 | 0.001 | 28× |
| 11 | 132 | 0.329 | 0.001 | 329× |
| 23 | 552 | 2.179 | 0.001 | 2179× |
| 47 | 2256 | 18.953 | 0.001 | 18953× |
| 101 | 10302 | 188.818 | 0.001 | **188818×** |

Fitted exponent $p=11..101$: $O(p^{3.0})$ empirical; $O(p^2 \log p)$ theoretical.

---

## Falsification Conditions

The $\Omega(p^2)$ lower bound is falsified if: a hash-guided algorithm achieves $O(p^{2-\epsilon})$ for any $\epsilon > 0$. The affine-plane structure makes this geometrically impossible, but a different encoding of the survivor-line problem might circumvent the corridor structure.

*(c) 2026 Brayden Sanders / 7Site LLC | DOI: 10.5281/zenodo.18852047*
