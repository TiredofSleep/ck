# BSD NECESSARY VS SUFFICIENT MEMO
# Is Sha the Analog of the RH Uniqueness Gap?

**© 2026 7Site LLC | Brayden Ross Sanders**

---

## 1. Is Sha Merely Present, or Genuinely Necessary?

**Sha is genuinely necessary** in the BSD leading coefficient formula.

The exact BSD formula requires #Sha(E) as a factor:

$$\lim_{s\to1}\frac{L(E,s)}{(s-1)^r} = \frac{\Omega_E \cdot \mathrm{Reg}(E) \cdot \prod_p c_p \cdot \#\mathrm{Sha}(E)}{(\#E_{\mathrm{tors}})^2}$$

If Sha is infinite, the leading coefficient is infinite — contradicting the known finiteness of the L-function's Taylor coefficients. Therefore finiteness of Sha is **necessary** for BSD to make sense.

Sha is also **prime-specific** in a structural sense: it measures the failure of the Hasse principle for 1-cocycles over Q. For composite moduli (in the Kloosterman analogy), the relevant Galois cohomology is different. Sha is irreducibly arithmetic.

---

## 2. Does Rank Agreement Follow in Low-Rank Cases?

**For rank 0**: If L(E,1) ≠ 0 (analytically computable), then by Kolyvagin:
- rank E(Q) = 0 (proved)
- Sha is finite (proved)
- BSD formula verified (up to 2-part of Sha in many cases)

**For rank 1**: If L'(E,1) ≠ 0, then by Gross-Zagier + Kolyvagin:
- rank E(Q) ≥ 1 (Heegner point is nontrivial)
- rank E(Q) = 1 (under mild conditions)
- Sha is finite (proved in many cases)

For r = 0 and r = 1: **BSD is essentially proved in most cases** (conditionally on analytic rank computations matching the conjectural rank).

**For rank ≥ 2**: No general theorem. The analytic rank r_an = ord_{s=1} L(E,s) can be computed numerically but its equality with r_alg = rank E(Q) has no general proof.

---

## 3. The Real Wall: Three Options

| Wall | Meaning | Analog |
|------|---------|--------|
| Existence of Sha | Sha is nontrivial — the obstruction exists | Not the main wall for low rank |
| Finiteness of Sha | #Sha(E) < ∞ | **BSD Gap 2 analog** — open for r≥2 |
| Rank equality | r_an = r_alg | **BSD Gap 1 analog** — open for r≥2, the main wall |

**The real wall for BSD is rank equality for r ≥ 2.**

Sha finiteness is the secondary wall — necessary for the full formula, but dependent on the rank equality being established first. If r_an = r_alg = 2 is proved, Sha finiteness is expected to follow from the same machinery (Euler systems for higher rank).

---

## 4. BSD's Exact Analog of RH's Gap 1

**RH Gap 1**: the error O(N^{½−δ}) requires the zero-free region of ζ(s). Equivalent to RH.

**BSD Gap 1 analog**: the equality ord_{s=1} L(E,s) = rank E(Q) for r ≥ 2 requires a theorem connecting the analytic L-function data to the algebraic rank. No such theorem exists in general.

The mechanism that would close BSD Gap 1:
- An Euler system for rank ≥ 2 (no such system is known)
- A p-adic L-function argument reaching rank ≥ 2 (open)
- A geometric construction generalizing Heegner points to higher rank (open)

**BSD's Gap 1 is harder than RH's Gap 1**, in the sense that RH at least has a clear conjecture with numerical evidence and an explicit formula structure. BSD for r ≥ 2 lacks even a clear mechanism for proving the rank equality.

---

## 5. Necessary vs Sufficient for BSD

**Necessary** (established for r = 0, 1):
- L(E,s) has analytic continuation and functional equation (shell — proved)
- L-value ≠ 0 at s=1 → rank 0 (Kolyvagin, conditional)
- Heegner point construction → rank ≥ 1 for r_an = 1 (Gross-Zagier)

**Sufficient** (not established for r ≥ 2):
- The analytic rank r_an uniquely determines the algebraic rank r_alg
- Sha is finite for all elliptic curves

**The gap**: BSD says the analytic data (L-function vanishing) DETERMINES the arithmetic data (rank, Sha). For r ≥ 2, this determination is not proved. The L-function might vanish to order 2 without the rational points generating a rank-2 group (though this is not expected).

**Sha is the BSD analog of the cusp-form contamination (Gap 2)** — a secondary obstruction that complicates the leading coefficient but is not the primary wall. The rank equality (Gap 1 analog) is the true remaining barrier.
