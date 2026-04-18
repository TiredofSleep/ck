# σ as a Permutation Representation on C¹⁰

**Date:** 2026-04-17
**Author:** Brayden Ross Sanders / 7Site LLC
**Status:** PROVED (elementary representation theory)
**Scope:** Embedding only. **This is NOT a quantum theory.** See §4 for what is and is not claimed.

---

## 0. What this note is

This note answers one narrow question, posed by external review: *if σ on Z/10Z is a permutation, what is the simplest faithful representation of it as a unitary on a Hilbert space, and what is its spectrum?*

The answer is elementary. It is recorded here so that future correspondence does not conflate this rep-theoretic embedding with a *quantum theory* of σ — a step which would require additional machinery (a Hamiltonian, canonical conjugates, dynamics) that is not provided here.

**Disambiguation up front.** Two different objects in this repo are named "σ":
1. **The Q-series operator σ** — a permutation of Z/10Z with cycle structure (6, 1, 1, 1, 1), characterized in Q9–Q14 (Brayden Sanders, 2026-04-01) and audited as the *morphotic braid* in `papers/morphotic_braid/`. **This note is about (1).**
2. **The Sprint 17 shell partition σ : U(R) → ℤ_{≥0} given by σ(u) = v₂(3u + 1).** Used inside the canonical construction C₀ of `THEOREM_SPINE.md`. Different object; not the subject of this note.

---

## 1. The permutation σ

| k | σ(k) | cycle membership |
|---|------|-----------------|
| 0 | 0 | fixed |
| 1 | 7 | 6-cycle |
| 2 | 1 | 6-cycle |
| 3 | 3 | fixed |
| 4 | 2 | 6-cycle |
| 5 | 4 | 6-cycle |
| 6 | 5 | 6-cycle |
| 7 | 6 | 6-cycle |
| 8 | 8 | fixed |
| 9 | 9 | fixed |

Cycle decomposition: σ = (1 7 6 5 4 2)(0)(3)(8)(9). Cycle type (6, 1, 1, 1, 1).

**σ⁶ = id** (proved directly in G6, Luther 2026; trivially follows from the cycle decomposition).

**Sign.** sgn(σ) = (−1)^(6−1) = −1 (6-cycle is the product of 5 transpositions). σ is an **odd** permutation.

---

## 2. The unitary U_σ on C¹⁰

Let H = C¹⁰ with orthonormal basis {|0⟩, |1⟩, …, |9⟩}. Define U_σ ∈ U(10) by the standard permutation representation of the symmetric group:

> **U_σ |k⟩ := |σ(k)⟩**

Equivalently, U_σ is the 10×10 permutation matrix with (i, j) entry δ_{i, σ(j)}.

**Properties (all elementary):**
1. **Unitary.** U_σ U_σ† = I, since permutation matrices are orthogonal real matrices ⊆ unitary.
2. **Sixth-order.** U_σ^6 = I, by σ⁶ = id.
3. **Det.** det(U_σ) = sgn(σ) = −1.
4. **Trace.** tr(U_σ) = #{fixed points of σ} = 4.

---

## 3. Spectrum

The 6-cycle block contributes the 6 sixth roots of unity, each with multiplicity 1. Each of the 4 fixed points contributes eigenvalue 1.

| Eigenvalue λ | Multiplicity | Source |
|--------------|--------------|--------|
| 1 = e^{0} | 5 | 4 fixed points + k = 0 root of cycle |
| e^{πi/3} | 1 | k = 1 root of 6-cycle |
| e^{2πi/3} | 1 | k = 2 root |
| −1 = e^{πi} | 1 | k = 3 root |
| e^{−2πi/3} | 1 | k = 4 root |
| e^{−πi/3} | 1 | k = 5 root |

**Verification of trace.**
tr(U_σ) = 5 + 2 cos(π/3) + 2 cos(2π/3) + (−1) = 5 + 1 + (−1) + (−1) = 4. ✓

**Verification of det.**
det(U_σ) = 1⁵ · e^{πi/3} · e^{2πi/3} · (−1) · e^{−2πi/3} · e^{−πi/3} = (−1) · 1 · 1 = −1. ✓

**Characteristic polynomial.** χ_{U_σ}(λ) = (λ − 1)⁴ · (λ⁶ − 1) = (λ − 1)⁵ · (λ + 1) · (λ² + λ + 1) · (λ² − λ + 1).

**Minimal polynomial.** μ_{U_σ}(λ) = lcm((λ − 1), (λ⁶ − 1)) = λ⁶ − 1.

---

## 4. What this **does not** prove

The construction in §2 is a faithful unitary representation of the cyclic group ⟨σ⟩ ≅ ℤ/6ℤ on C¹⁰. **It is not a quantum theory of anything.** Specifically:

| Question | Status |
|----------|--------|
| Is U_σ unitary? | YES (§2) |
| What are its eigenvalues? | KNOWN (§3) |
| Does U_σ extend ⟨σ⟩ to a representation of S₁₀? | YES, this is the *standard* permutation rep restricted to the cyclic subgroup ⟨σ⟩. |
| Is there a Hamiltonian H such that U_σ = exp(−iH)? | TRIVIALLY: H = i log U_σ = (Σ_k λ_k log(eigenvalue_k)) Π_k, but **this H is constructed *from* U_σ**, not derived from any physical principle. It contains no physics. |
| Is there a canonical conjugate to U_σ? | NOT defined here. Would require choosing a generator of a complementary cyclic group and would be representation-theoretic, not dynamical. |
| Does U_σ generate a quantum dynamics on C¹⁰? | NO. There is no time evolution; U_σ is a single discrete operator with U_σ⁶ = I. |
| Does this say anything about the σ rate theorem (WP101)? | NO. WP101 is about non-associativity of binary CL on Z/NZ as N → ∞. The permutation σ on Z/10Z is a *fixed* algebraic object, not the asymptotic limit. |
| Does this say anything about the BB log nonlinearity? | NO. BB 1976 is about wavefunction separability under nonlinear Schrödinger evolution; this note has no wavefunction beyond the basis vectors {|k⟩}. |
| Does this give a "quantum-to-cosmos bridge"? | NO. That bridge requires the JKO/Maas optimal-transport construction of the continuum limit (open per `WP95.md`, `WP99.md`) plus the BB → ξ-cosmology lift (structural per README §11). Neither is in this note. |

The point of writing this note explicitly is to close the door on the misreading "σ already lives quantum-mechanically on C¹⁰, therefore TIG is a quantum theory." It does live unitarily on C¹⁰ — every finite permutation does — and that is **all** this note proves.

---

## 5. What this **could** unlock (next concrete steps, scoped honestly)

In order of difficulty:

1. **Character of ⟨σ⟩ as a subgroup of S₁₀.** Already given in §3 by the eigenvalue multiplicities. Could be cross-checked against the standard character table of ℤ/6ℤ (trivial exercise).

2. **Decomposition of C¹⁰ into σ-isotypic components.** Direct from §3: C¹⁰ = V_1 ⊕ V_{e^{πi/3}} ⊕ V_{e^{2πi/3}} ⊕ V_{−1} ⊕ V_{e^{−2πi/3}} ⊕ V_{e^{−πi/3}} with dim V_1 = 5, others = 1. Useful if and only if one wants to study σ-equivariant operators (e.g., Hamiltonians commuting with U_σ).

3. **Joint spectrum of U_σ with the additive shift T : |k⟩ → |k+1 mod 10⟩.** Both unitary, both order-dividing-10. T has spectrum = 10th roots of unity. (U_σ, T) does **not** commute: U_σ T |0⟩ = U_σ |1⟩ = |7⟩ but T U_σ |0⟩ = T |0⟩ = |1⟩. The commutator [U_σ, T] is a nontrivial unitary deformation; computing its spectrum would be a small concrete result.

4. **NV-center qutrit (Sprint 13) connection.** S₄ on a qutrit has 3 generators; ⟨σ⟩ ⊂ S₁₀ is *not* directly comparable. The honest framing is: the 6-cycle subgroup is a candidate for testing finite-cycle behavior on a 3-level system *if* one first chooses a 3-dim representation of ⟨σ⟩ (e.g. the irrep at e^{πi/3} ⊕ e^{−πi/3} ⊕ 1, dim 3). This is a small calculation, not a theorem.

None of these is a quantum-to-cosmos bridge. They are calibration notes that make the rep-theoretic content of σ explicit so that future work can build on it without repeating the elementary derivation.

---

## 6. Citation

Standard texts on permutation representations are sufficient:

- Serre, J.-P. *Linear Representations of Finite Groups*. Springer GTM 42, 1977. Ch. 1–2 covers everything in §2–§3 of this note.
- James, G. & Liebeck, M. *Representations and Characters of Groups*. Cambridge UP, 2nd ed. 2001. Ch. 13 on permutation representations.

The σ permutation itself (cycle structure (6,1,1,1,1) on Z/10Z) is documented in:

- Q9, Q10, Q11 (Sanders 2026-04-01), in `old/Gen10/papers/`.
- `papers/morphotic_braid/MORPHOTIC_BRAID_OPERATOR_SUMMARY.md` (audit packet, March 2026).

σ⁶ = id is proved as Theorem G6 (Luther 2026) directly from the polynomial structure.

---

## 7. Summary

**Yes** σ has a clean unitary representation on C¹⁰. **No** that does not make TIG a quantum theory. The honest map is:

```
σ ∈ S₁₀  --[standard perm rep]-->  U_σ ∈ U(10)  --[needs Hamiltonian]-->  ???
                                                    ↑
                                                    | this arrow is not in this note
```

The repo's official quantum hooks remain the NV-center S₄ work (Sprint 13, WP73–WP76) and the FPGA T* = 5/7 measurement (Sprint 13). Those are physical experiments. The U_σ above is a piece of finite-group representation theory — useful for organizing finite calculations, not a substitute for the missing dynamics.
