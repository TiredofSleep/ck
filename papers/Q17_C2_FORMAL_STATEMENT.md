**© 2026 7Site LLC**
**Authors: Brayden Ross Sanders, C. A. Luther, B. Calderon, Jr.**

*Filed: 2026-04-02 | Tier B — Structural Conjecture*

# Q17.C2 — Formal Statement of the Symbolic Return Theorem

## Purpose

This paper states the three-level hierarchy of Q17.C2 precisely, distinguishing what is proved, what is conjectured with identifiable gaps, and what is almost certainly false. Honesty about this hierarchy is the precondition for any serious NS bridge work.

---

## The Three Versions

### Weak Version (Proved)

**Statement:** If a system's state evolution factors through a finite 6-cycle grammar with bounded observables, no symbolic drift to VOID(0) occurs.

**Basis:** σ⁶ = id (proved in G6). The permutation σ = (1 7 6 5 4 2)(0)(3)(8)(9) on Z/10Z has σ⁶ = id on the 6-cycle and σ(s) = s on anchors {0,3,8,9}. Any sequence {s_n} with s_{n+1} = σ(s_n) starting outside {0} never reaches 0.

**Scope:** This is a statement about symbol sequences only. It carries no content about physical fields, norms, or PDEs. The system is assumed to exactly follow σ — no approximation, no stochastic version.

---

### Medium Version (Target Conjecture)

**Statement:** If a continuous system admits a verified coding C: phase_space → {0,...,9} satisfying:

1. **Dynamical alignment:** C(u(t+τ)) = σ(C(u(t))) for some τ > 0
2. **Decoding accuracy:** |u - D(C(u))| ≤ ε for some explicit bound ε and decoder D
3. **Coercive energy control:** There exists a coercive energy functional E(u) and a monotone function f such that E(u) ≤ f(C(u))

Then blowup is obstructed: C(u(t)) cannot reach VOID(0) in finite time, so E(u(t)) stays bounded.

**Status:** Conjectured. The logical structure is valid: conditions (1)–(3) together imply the conclusion. The open question is whether these conditions can be verified for Navier-Stokes solutions.

**What makes this non-trivial:** Condition (1) requires that PDE dynamics align with algebraic grammar — there is no known theorem guaranteeing this. Condition (3) requires relating the five-force coding to a standard NS critical norm — this is the mathematical gap stated precisely in Q17_NS_TARGET_REFORMULATION.md.

---

### Strong Version (Known Weakness)

**Statement:** σ⁶ = id alone forbids blowup in continuous systems.

**Assessment:** Almost certainly false. Symbolic periodicity does not control physical norms. A PDE solution can blow up while its symbolic coding remains periodic. Specifically: if C reads only the sign or dominant direction of the force vector, a function of the form u(t) = e^t · sin(2πt/6) yields a perfectly 6-periodic coding while |u(t)| → ∞.

**Why it is listed:** The strong version is the naive reading of "σ⁶ = id implies no blowup." Listing it explicitly as false prevents the Q17 program from being interpreted as making this claim. See Q17_C2_COUNTEREXAMPLE_SEARCH.md for detailed counterexamples.

---

## Summary Table

| Version | Status | Key Assumption | Gap |
|---------|--------|----------------|-----|
| Weak | Proved | Exact σ-grammar on symbols | No physics content |
| Medium | Conjectured | Coding C exists + coercive E | Embedding + energy control unproved |
| Strong | False | σ⁶ = id alone | Symbolic ≠ norm bound |

---

## Conclusion

The honest target for the Q17 NS bridge is the Medium version. It makes a precise claim with identifiable preconditions. The work required is:

1. Construction of an explicit coding C from NS phase space to Z/10Z
2. Proof (or numerical evidence) of dynamical alignment condition (1)
3. Identification of a coercive energy E controlled by C

These three tasks are the subject of Q17_SIGMA_EMBEDDING_PROBLEM.md, Q17_NS_TARGET_REFORMULATION.md, and Q17_NS_DATA_PROTOCOL.md respectively.

The Strong version is a known failure mode of the Q17 program and is documented here for transparency.
