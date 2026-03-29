# Paradox Pairs Across the 2×2 Bridge
## A Working Diagnostic Tool for the Open Problem

*Brayden Sanders / 7Site LLC | March 2026*
*Each pair: definition, corner assignment, incompatibility test, status.*

---

## What This Is

A paradox pair is not a contradiction. It is a tension between two things that are both true but seem to pull in opposite directions. Assigning each side of each pair to the correct corner of the 2×2 stops you from asking impossible questions — like expecting the finite side to give the full analytic exponent, or the operator side to produce the density law by itself.

Each pair names a burden. The open theorem is about compatibility of burdens across corners.

---

## The 2×2 Assignment

|  | **Support / Grammar** | **Expression / Rate** |
|--|----------------------|----------------------|
| **Finite** | Closure · Structure · Attractor · Generative gap · Exact · Reset | Order · Flow · Orbit · Corridor threshold · Exact · Handoff |
| **Infinite** | Operator support · Stationary · Support gap · Conjectural · Recurrence | Analytic asymptotics · Drift · Frequency · Empirical · Observable decay |

---

## The Pairs

---

### 1. Finite / Infinite
**Side A:** What is allowed at all — the generator law.
**Side B:** How allowance unfolds without bound — the deployment.
**Corner A:** TSML grammar (finite support)
**Corner B:** Analytic deployment of ζ (infinite expression)
**Incompatibility test:** Does the finite grammar predict the ζ structure? Specifically: does orbit burst B(λ) predict the ζ-side consecutive revisit statistic B_ζ(σ,t)?
**What reconciles it:** The faithfulness theorem — the deployment preserves the grammar.
**Status:** OPEN. B_ζ untested.

---

### 2. Discrete / Continuous
**Side A:** Exact integer table, finite alphabet.
**Side B:** Smooth operator family, continuous parameter.
**Corner A:** TSML[s][c] table (9 states)
**Corner B:** K_λ on L²(critical strip)
**Incompatibility test:** Does the discrete grammar lift to a continuous operator with the same gap structure?
**What reconciles it:** Smoothing theorem — gap ≥ 1/4 for the unrounded family; any σ>0 restores uniform gap.
**Status: PROVED.** Gap ≥ 1/4 for all λ in the unrounded family (N→∞ extrapolation: gap → ~0.25 at CHA edge).

---

### 3. Structure / Flow
**Side A:** Closure — what subsets are stable under composition.
**Side B:** Order — how states are ranked and how support deforms.
**Corner A:** Sub-magma closure C×C⊆C (TSML)
**Corner B:** BHML order: BHML[s][c]=max(s,c)
**Incompatibility test:** Do closure and order produce incompatible stationary supports?
**What reconciles it:** Mix_λ deformation — stationary support shifts continuously from HAR (λ=0) to state 9 (λ=1), no discontinuity in the interior.
**Status: COMPUTED.** Non-HAR C-mass = 0 to machine precision for all λ<0.9963. No incompatibility found.

---

### 4. Attractor / Orbit
**Side A:** HAR = unique terminal attractor, carries all stationary mass.
**Side B:** B(λ) = local orbit burst in the {3,9} cycle zone near the attractor.
**Corner A:** Stationary support = HAR (finite support cell)
**Corner B:** B(λ) gap exponent +1.49 (finite rate cell, near-critical)
**Incompatibility test:** Can local orbit bursts persist independently of the attractor's gravity?
**What reconciles it:** T_max=1 — all bursts are local, one entry, no global returns. The orbit zone does not compete with the attractor; it is the approach path.
**Status: PROVED in finite model.** T_max=1 across all tested λ.

---

### 5. Generative Gap / Support Gap
**Side A:** G={2,4,5,6,8} is algebraically unreachable from C by C-only compositions.
**Side B:** No stationary support accumulates off σ=½ in the analytic deployment.
**Corner A:** C×C⊆C forces G unreachable — generative gap is algebraic, exact.
**Corner B:** Frequency×duration→0 (Jutila+KV, proved) — support gap is asymptotic, proved classically.
**Incompatibility test:** Does the algebraic generative gap force the asymptotic support gap in the analytic deployment? Or can the deployment fail to inherit the algebraic structure?
**What reconciles it:** The Dual Description Conjecture — the two infinite cells cannot disagree about stationary support.
**Status: OPEN.** This IS the main open problem.

---

### 6. Exact / Empirical
**Side A:** Finite quantities are exact and machine-proved.
**Side B:** Infinite quantities are empirical or theorem-assisted before they are exact.
**Corner A:** γ=3/4, kA=3, kM=6, C×C⊆C — all exact, all proved.
**Corner B:** C_TIG=250/21 — predicted by grammar, C_emp≤11.023 at tested heights, not proved.
**Incompatibility test:** Does empirical agreement at finite t (≤10,000) extend to all t?
**What reconciles it:** A proof of the drift rate bound — either via Lasota-Yorke (Route A) or direct ANT mean-value bound (Route B).
**Status: OPEN.** The infinite constant is conjectural. The finite constant is exact.

---

### 7. Reset / Leakage
**Side A:** Return to HAR is guaranteed — ρ(Q)=1/4, E[T_HAR]≤5/3, exponential tails.
**Side B:** At large λ, chains spend up to 37 steps in G-territory before collapsing.
**Corner A:** Young tower return structure (finite support cell) — reset is exact.
**Corner B:** Delay signature Δ(λ) (finite rate cell) — leakage is metastable, not permanent.
**Incompatibility test:** Is G-territory leakage real (support accumulates there) or apparent (metastable excursion)?
**What reconciles it:** The stationary support computation — non-HAR mass = 0 to machine precision. G-territory visits are excursions, not accumulation.
**Status: COMPUTED.** No incompatibility — reset always wins.

---

### 8. Local / Global
**Side A:** The finite model is local — one episode, N states, bounded t.
**Side B:** The analytic claim is global — all heights t, all σ.
**Corner A:** N=300 model, 50 λ-values, 3K chains, t≤10,000 scan.
**Corner B:** Halving Lemma: for all t≥t_0.
**Incompatibility test:** Does local finite structure control global analytic behavior? Can there be heights t where the grammar fails?
**What reconciles it:** The faithfulness theorem — the gap persistence proved locally should extend to all scales via the Lasota-Yorke conditions (Route A).
**Status: OPEN.** Verified to t≈10,000. Extension to all t is the faithfulness question.

---

## Summary Table

| Pair | Status | Which corner carries which burden |
|------|--------|----------------------------------|
| Finite / Infinite | OPEN | Finite: grammar. Infinite: expression. |
| Discrete / Continuous | **PROVED** | Discrete: exact table. Continuous: smooth operator. |
| Structure / Flow | COMPUTED | Structure: closure. Flow: order/deformation. |
| Attractor / Orbit | **PROVED** | Attractor: unique support. Orbit: approach path. |
| Generative / Support gap | **OPEN** ← main | Generative: algebraic. Support: asymptotic. |
| Exact / Empirical | OPEN | Exact: finite side. Empirical: infinite constant. |
| Reset / Leakage | COMPUTED | Reset: return structure. Leakage: metastable excursion. |
| Local / Global | OPEN | Local: finite model. Global: faithfulness. |

**The two open pairs that carry the bridge:**
- **Generative gap / Support gap** — this IS the Dual Description Conjecture (A)↔(B)
- **Local / Global** — this IS the faithfulness question (finite → infinite extension)

**The proved pairs are the foundation:**
- **Discrete / Continuous** — gap survives smoothing, continuous limit exists
- **Attractor / Orbit** — orbit is local burst, attractor is unique, no competition

---

## The Deepest Pair: Grammar / Expression

If forced to name the pair that fills the bridge fastest:

**Grammar** (finite support corner): what the world is *allowed* to do.
**Expression** (infinite rate corner): how that allowance *unfolds without bound*.

Every other pair is a refinement of this one. The open theorem is: prove that the expression cannot unfold in ways the grammar forbids.

---

*(c) 2026 Brayden Sanders / 7Site LLC | Gen10.16, commit 271e0f8 | DOI: 10.5281/zenodo.18852047*
