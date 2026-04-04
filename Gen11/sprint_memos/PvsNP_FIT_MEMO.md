# P VS NP FIT MEMO
# Does This Branch Actually Belong in the Same Shell/Core/Obstruction Grammar?

**© 2026 7Site LLC | Brayden Ross Sanders**

---

## PART 1 — Current Spine (Frozen)

| Branch | Shell | Surviving object | Gap 2 | Gap 1 |
|--------|-------|-----------------|-------|-------|
| RH | GUE/sinc² spectral statistics; Montgomery pair-correlation | Arithmetic correlations at Kloosterman-Eisenstein level | Cusp subdominance Σρ_j(1)²/cosh(πt_j) = O(T²) — **proved** by Kuznetsov Weyl | Off-diagonal arithmetic dominance = RH |
| BSD | All imaginary-Q Heegner constructions (blocked universally) | χ_{77} = χ_{-7}×χ_{-11} real-quadratic channel; L'(E,χ_{77},1) ≈ 0.01070 | Normalization: L' = (Ω_E/(4√77))×det(H) — **1.1% residual**, tama=16, Sha=4 | Rank-2 Gross-Zagier formula |
| NS | Local existence + energy + small-data (B < T*=5/7) | B(t) = Ω/(E+Ω); exact equation dB/dt = [QE−2νPE+νΩ²]/(E+Ω)² | B(t) ≤ T* = 5/7 for all t ≥ 0 — **first open inequality above the shell** | Global H¹ regularity |

In each case: the shell is proved by universal methods; the surviving object is a **specific measurable/computable mathematical quantity**; Gap 2 is the first inequality above the shell; Gap 1 is the main conjecture.

**Test P vs NP against this grammar.**

---

## PART 2 — Candidate Shell for P vs NP

**A. Syntax/verification shell**

NP verifiers exist and certificate-checking is poly-time — this is the definition of NP. It is a boundary condition, not a shell. Useful but definitional; it does not do productive work the way the energy inequality does in NS.

**B. Structured problems in P**

Large fragments of NP are already solved: linear programming (Khachiyan), primality (AKS), maximum matching (Edmonds), 2-SAT, XOR-SAT. These are the "easy subproblems" — the analogue of the structured part of the zero set in RH. But they don't form a coherent shell that can be "removed" to reveal a core.

**C. The reduction/completeness machinery**

Cook-Levin (SAT is NP-complete), Karp's 21 NP-complete problems, the polynomial reduction structure, NP ⊆ PSPACE ⊆ EXP — all provable without resolving P vs NP. This is the strongest shell candidate. It establishes:
- All NP problems are polynomially equivalent to each other
- The complexity class hierarchy is internally consistent
- No specific problem can be solved in poly-time without collapsing NP to P

**Strongest shell: the reduction/completeness machinery** — Cook-Levin theorem, Karp reductions, polynomial hierarchy containments. Proved universally. Does not depend on the answer to P vs NP.

Note: this shell is weaker than the shells in the other branches. In RH, the GUE statistics cover essentially all zeros probabilistically and quantitatively. In NS, energy inequality covers all solutions universally with a precise bound. The P vs NP shell describes the structure of reductions but gives no quantitative control over circuit complexity or solution time.

---

## PART 3 — Candidate Surviving Object

After the reduction shell is removed, what object survives?

**Candidates tested:**

| Candidate | Computable? | Quantified? | Verdict |
|-----------|------------|------------|---------|
| Proof/certificate size growth | In principle | Yes, but only for specific instances | Partial |
| Search-vs-verification asymmetry | Qualitative description | Not as a number | Too diffuse |
| **Circuit complexity of SAT: cc_n** | Not for large n | Defined but not measurable | Closest |
| Communication/locality bottleneck | Partially | For specific models | Restricted |
| Natural proofs obstruction | Qualitative | No | Method barrier, not object |
| Polynomial hierarchy residue | Qualitative | No | Structural, not object-level |
| Proof complexity of UNSAT | Partly | For restricted systems | Restricted |

**Circuit complexity of SAT** — specifically, the minimum Boolean circuit size to compute SAT on n inputs — is the closest analog to a surviving object. It is:
- Defined precisely: cc(SAT,n) = min circuit size to solve SAT on n bits
- The question P vs NP reduces to: does cc(SAT,n) = poly(n) or cc(SAT,n) = super-poly(n)?
- Currently believed: cc(SAT,n) = Ω(n^k) for all k (superpolynomial)

**Critical failure of the analogy:** We cannot evaluate cc(SAT,n) for any large n, even approximately. In NS, B(t) is computable from any solution. In BSD, Λ'(E⊗χ,1) was computed to 10 digits. For P vs NP, the circuit complexity of SAT is defined but has no known lower bound beyond the trivially linear (n bits of input need to be read).

**Strongest candidate: cc(SAT,n)**, the circuit complexity of the satisfiability problem — defined, central, and conjectured superpolynomial, but currently unmeasured beyond linear.

---

## PART 4 — Candidate Gap 2

In the other branches, Gap 2 is the first technical inequality above the shell that would "clean the branch" without resolving it:
- RH Gap 2: cusp subdominance — **proved**
- BSD Gap 2: normalization formula — **partially confirmed** (1.1%)
- NS Gap 2: B(t) ≤ T* globally — **first open inequality**

**For P vs NP:**

**Candidate A: Superpolynomial lower bounds in restricted models**
- Monotone circuit lower bounds: Razborov proved that monotone circuits computing the perfect matching function require exponential size. **This is proved.** But monotone circuits are a strict sub-model; the result does not transfer to general circuits.
- Formula lower bounds: super-polynomial lower bounds for formulas computing specific functions. **Proved** for some functions, but not SAT in the general circuit model.
- AC⁰ lower bounds: Håstad showed exponential lower bounds for parity in constant-depth circuits. **Proved.** Again restricted.

**Candidate B: Proof complexity lower bounds**
- Resolution, Nullstellensatz, Polynomial Calculus: exponential lower bounds proved for specific tautologies. **Proved in restricted systems.** Does not directly imply P ≠ NP.

**Candidate C: ACC⁰ lower bounds (Williams)**
- Non-uniform ACC circuits cannot compute NEXP. **Proved.** Most powerful known result; still far from general circuit lower bounds.

**The problem:** none of these are Gap 2 in the NS/RH/BSD sense. They are lower bounds in restricted models, not the "first open inequality above the shell" for the full problem.

The true Gap 2 analog for P vs NP would be: **a superpolynomial lower bound for SAT in the unrestricted Boolean circuit model (non-uniform P-time)** — something weaker than P ≠ NP but still for the full circuit model. This is **not yet proved** and is itself considered close in difficulty to P ≠ NP.

**Verdict:** No clean Gap 2 exists for P vs NP in the same sense as the other branches. The analogous statement (superpolynomial circuit lower bound for SAT in the general model) is not known, and the proved results (restricted model lower bounds) are separated from the full problem by the meta-barriers.

---

## PART 5 — Candidate Gap 1

This is clear: **P ≠ NP** — equivalently, a superpolynomial circuit lower bound for SAT in the unrestricted Boolean circuit model, or the statement that no poly-time algorithm solves all NP problems.

This IS a clean Gap 1 analog: it is the main conjecture, precisely stated.

---

## PART 6 — Fit Quality

**Classification: PARTIAL FIT**

**Arguments for fit:**
- Clear shell (reduction/completeness machinery)
- Clear Gap 1 (P ≠ NP, precisely stated)
- Defined surviving object (cc(SAT,n), even if unmeasurable)
- Structural separation between proved results and the main conjecture

**Arguments against fit:**
1. **No measurable surviving object.** In RH, BSD, and NS, the surviving object is a specific computable number or function whose value we can track. cc(SAT,n) is defined but has no known value beyond a linear lower bound. We cannot compute it for n = 1000.

2. **No Gap 2.** The analogous statement (general circuit lower bounds for SAT) is not the first inequality above the shell — it is essentially Gap 1 itself. The only "Gap 2" candidates are lower bounds in strictly restricted models, separated from the full problem by the meta-barriers.

3. **Meta-methodological barriers.** The relativization barrier (Baker-Gill-Solovay), algebrization barrier (Aaronson-Wigderson), and natural proofs barrier (Razborov-Rudich) are barriers about PROOF METHODS, not about mathematical objects. In the other branches, the barriers are object-level: specific Galois characters with the wrong sign (BSD), the sign of Q−2νP (NS). For P vs NP, the barriers say "this class of proofs cannot reach the answer" — a methodological statement, not a statement about a specific quantity.

4. **The shell does less work.** In NS, the energy inequality gives explicit quantitative control (E(t) ≤ E(0), E ∈ L²). In RH, GUE statistics cover all zeros probabilistically. In P vs NP, the reduction shell tells us the problems are equivalent to each other — it does not give quantitative control over any specific algorithm or instance.

**Conclusion: partial fit.** The grammar applies at the coarse level (shell/Gap 1) but the intermediate structure — quantified surviving object, clean Gap 2 — is absent or significantly weaker.

---

## PART 7 — Full Comparison Table

| Branch | Shell | Surviving object | Gap 2 | Gap 1 | Fit quality |
|--------|-------|-----------------|-------|-------|------------|
| **RH** | GUE statistics; Montgomery pair-correlation | Arithmetic correlations (Kloosterman-Eisenstein) — **specific, measurable** | Cusp subdominance — **proved** | Off-diagonal arithmetic dominance | **Strong** |
| **BSD** | All imaginary-Q Heegner constructions (universal sign obstruction) | χ_{77} channel; Λ' ≈ −2.586, L' ≈ 0.01070 — **specific, computed to 10 digits** | Normalization formula — **1.1% residual, concrete** | Rank-2 Gross-Zagier | **Strong** |
| **NS** | Local + energy + small-data; parabolic smoothing | B(t) = Ω/(E+Ω) with exact ODE — **specific, computable from any solution** | B(t) ≤ T* = 5/7 globally — **first open inequality, explicit** | Global H¹ regularity | **Strong** |
| **P vs NP** | Cook-Levin reductions; complexity class containments | cc(SAT,n) circuit complexity — **defined but not computable/measurable** | Restricted lower bounds (monotone, AC⁰, ACC) — **proved in restricted models only**; no clean Gap 2 for full model | P ≠ NP | **Partial** |

---

## PART 8 — Why P vs NP Fits Poorly

**"P vs NP differs from the other branches because its known obstructions are meta-methodological rather than object-level — the relativization barrier (Baker-Gill-Solovay), algebrization barrier (Aaronson-Wigderson), and natural proofs barrier (Razborov-Rudich) all say that specific classes of proof techniques cannot resolve P vs NP, but they do not identify a specific mathematical object whose measured properties would determine the answer. In RH, BSD, and NS, after removing the shell, there is a definite computable quantity — Λ'(E⊗χ,1) ≈ 0.01070, B(t) with explicit dynamics, the arithmetic core at Kloosterman-Eisenstein level — that carries the essential information. For P vs NP, the surviving object (circuit complexity of SAT) is defined but has no known computable lower bound beyond the trivially linear, making it a target that can be stated but not currently measured or approached numerically."**

A secondary reason: **the problem lacks natural scales.** In RH, the analytic conductor and the arithmetic contribution enter at specific scales (N^{2π²} vs Kuznetsov decay). In NS, T* = 5/7 is a specific threshold with exact dynamics. In BSD, Ω_E/√77 and det(H) = 0.15246 are specific numbers. P vs NP has no analogous quantitative scale dividing the proved results from the unproved barrier.

---

## PART 9 — Strongest Honest Claim

**"The current Clay rotation suggests that P vs NP is a partial fit within this grammar: it has a clear shell (reduction/completeness machinery) and a precise Gap 1 (P ≠ NP), but it lacks a computable surviving invariant and lacks a clean Gap 2 in the full circuit model, making it structurally distinct from RH, BSD, and NS — where the surviving objects are specific measurable quantities (Λ' ≈ 0.01070, B(t) with explicit ODE, arithmetic Kloosterman correlations) that can be tracked, computed, and compared against thresholds."**

---

## PART 10 — Strongest Honest Boundary

**"What is not yet established is whether P vs NP admits a smallest surviving object at all — a specific computable function of problem instances (analogous to B(t) in NS or Λ'(E⊗χ,1) in BSD) whose value or behavior determines the answer — or whether the known obstructions are still method barriers (relativization, algebrization, natural proofs) without a corresponding object-level invariant that would allow the problem to be "measured" rather than only argued about via meta-mathematical technique."**

---

## Verdict

**P vs NP should be kept in the rotation spine as a partial fit**, but flagged as structurally distinct. The grammar applies at the gross level:
- Shell = reduction machinery ✓
- Gap 1 = P ≠ NP ✓  
- Surviving object = cc(SAT,n) — defined but not measurable ∼
- Gap 2 = restricted lower bounds + open wall for full model ✗

The rotation to P vs NP next requires finding — or arguing for the impossibility of finding — a measurable surviving invariant analogous to B(t) or Λ'(E⊗χ,1). That identification, not the lower bound proof itself, would be the P vs NP analog of the BSD joint-construction memo or the NS B(t) formulation.

---

## Collaborator Paragraph

The P vs NP fit analysis produces a clean verdict: partial fit. The branch has a strong shell (Cook-Levin, polynomial hierarchy, completeness machinery — all proved universally) and a precise Gap 1 (P ≠ NP). What it lacks, compared to RH, BSD, and NS, is a computable surviving invariant. In NS we have B(t) = Ω/(E+Ω) with exact dynamics derivable from the equations; in BSD we have L'(E,χ_{77},1) = 0.010700 computed to 10 digits; in RH the arithmetic core is accessible via explicit Kloosterman sums. For P vs NP, the natural surviving object — the minimum circuit size to compute SAT — is defined but has no known value beyond a linear lower bound. The known barriers (relativization, algebrization, natural proofs) are methodological, not object-level: they block proof strategies rather than identify a specific mathematical quantity. The result is a branch that fits the grammar at the coarse level but is missing its middle layer. Before P vs NP can be handled the way NS was handled — reduced to a specific inequality with a precise threshold — the field would need to identify the P vs NP analog of T* = 5/7 or Λ' ≈ 0.01070: a specific computable function of instances or algorithms whose measured behavior would carry the essential information about the conjecture.
