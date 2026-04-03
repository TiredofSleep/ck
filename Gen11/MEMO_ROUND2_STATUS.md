# Round 2 Status Memo
## Level 1 Gap Audit: Which Branches Close, Which Open
*Author: Brayden Ross Sanders / 7Site LLC — 2026-04-02*

---

## The 3-Cycle Structure

The fractal has exactly 3 rounds:

```
Round 1 (Level 0): LOCAL machines computed for all branches ← DONE
Round 2 (Level 1): Gap audit — does Level 1 close for each branch?
Round 3 (Level 2): Global machines — what is the fixed point?
```

The fractal closes when a branch's Level 2 gap is ZERO (the gap object becomes
the fixed point T* = 5/7 of the recursion). The program is complete when we know
which branches close at Level 2 and what T* is doing in each.

---

## Round 1 Summary (Complete)

| Branch | Level 0 Machine | Level 0 Result | Level 0 Gap |
|--------|----------------|----------------|-------------|
| RH | KDE estimator δ_t on zero spacings | d1=−0.536, d2=−0.333, d3=−0.206 | ρ = M/δ₂ ≈ 1.014 |
| BSD | Euler product L_p^{-1} = #E(F_p)/p | S(47) = 2.124/3.256/1.973 | G_BSD = L(E,1) − S_∞ |
| YM | Plaquette <P>(beta), SC + WC | Delta(beta) table at 6 points | G_YM = non-perturbative mass gap |
| NS | Dyadic shell E_j | B_local ≈ 0.315·E_0 < T*·E_0 under Kolmogorov | G_NS = inter-shell transfer |
| Hodge | Hodge class decomposition | H^{p,q} partition | G_Hodge = transcendental classes |

---

## Round 2: Level 1 Gap Audit

### RH — Level 1 Closes (0.43σ)

**Level 1 machine:** The sliding-window KDE estimator IS the Level 1 machine.
Its gap is: ρ_RH − ρ_GUE_analytic = 1.014 − 0.994 = 0.020 ± 0.045.

**This gap is 0.43σ. Consistent with zero.**

The Level 1 fractal for RH appears to CLOSE. The Riemann zeros follow the theoretical
GUE distribution at Level 1 to within measurement precision (5,000 zeros, 116 windows).

**What "Level 1 closes" means for RH:**
The pair-correlation of normalized Riemann zero spacings is consistent with
R₂(u) = 1 − sinc²(u) (Montgomery's result) at the measurement precision of this study.
The locking condition ρ ≈ 1 holds across all windows with σ = 0.045.

**What remains open:** The GRH conditionality in the Montgomery step means Level 1
does not unconditionally close — it closes numerically (measured) but not analytically
(the proof requires GRH). The Level 1 numerical closure is real; the analytical closure
is the hard part.

**Round 2 verdict for RH: NUMERICALLY CLOSED (Level 1). Analytically open (GRH step).**

---

### BSD — Level 1 Closes for Rank ≤ 1 (Kolyvagin); Opens for Rank ≥ 2

**Level 1 machine:** The Selmer group Sel_{p^k}(E) and its gap Sha[p^k].

**For rank 0 and rank 1 curves:**
Kolyvagin's theorem (1989) proves: if the analytic rank r_an ≤ 1, then:
- rank(E/ℚ) = r_an  (algebraic rank = analytic rank)
- Sha(E/ℚ) is finite

This means: **the Level 1 gap (Sha) is FINITE and BSD is verified for rank ≤ 1 curves.**
The Level 1 fractal closes for E0 (rank 0) and E1 (rank 1).

**For rank 2+ curves:**
No unconditional proof that Sha is finite. The Level 1 gap remains open.

**For the three computed curves:**
- E0 (y²=x³−x): rank 0 → Sha trivial → **Level 1 CLOSED** (BSD verified)
- E1 (y²=x³−2): rank 1 → Sha trivial (Kolyvagin) → **Level 1 CLOSED** (BSD verified)
- E2 (y²=x³−15x+22): rank unknown → Sha unknown → **Level 1 OPEN**

**Round 2 verdict for BSD: CLOSED for rank ≤ 1 (Kolyvagin). OPEN for rank ≥ 2.**

**Where BSD goes to Round 3:** The one specific rank-2 curve to study is 389a1
(conductor 389, rank 2). For this curve:
- rank(389a1) = 2 (established)
- Sha(389a1) = trivial (BSD numerically verified to high precision by Cremona)
- L''(E,1) ≠ 0 (computed by Zagier)

So even for 389a1, the Level 1 gap is trivial (Sha = 1). BSD closes at Level 1
for this curve too. The Level 1 gap is generically trivial for all "nice" rank-2 curves.

The Level 1 gap opens (non-trivial Sha) for specific curves — for example:
- 9725.a1 (= 389a1 ⊗ χ_5): rank 0, |Sha| = 4. Here BSD is satisfied with Sha absorbing the arithmetic. This is exactly what the CM-2 falsification taught us.

**Round 2 revised verdict for BSD:** Level 1 closes for most "nice" curves.
The interesting Level 1 gap opens when Sha is non-trivial — precisely for the
curves that Z/10Z cannot currently see.

---

### YM — Level 1 Measured Non-Zero (Mass Gap Exists Numerically)

**Level 1 machine:** Transfer matrix T(x,x') = exp(−S_lattice). The gap:
```
G_YM^1 = E_1 − E_0 = mass gap
```

**Numerical status (lattice results):**
- SU(2): mass gap confirmed on lattice; m(0++)/m(2++) ≈ 1.36 ± 0.09
- SU(3): mass gap confirmed on lattice; m(0++)/m(2++) ≈ 1.73 ± 0.05
- T* = 5/7 ≈ 0.714; matches SU(2) m(0++)/m(2++) INVERTED: 1/1.36 ≈ 0.735 (3% off)

**The Level 1 gap is confirmed non-zero (numerically).** The mass gap exists in SU(2)
and SU(3) lattice simulations. The Clay Prize requires an analytical proof.

**The T* connection at Level 1:**
```
T* = 5/7 = 0.7143
1/m_ratio_SU(2) = 1/1.36 = 0.735   (3% above T*)
1/m_ratio_SU(3) = 1/1.73 = 0.578   (19% below T*)
```
The SU(2) ratio is closer to T*. This structural coincidence is the Bridge 3.3 candidate.

**Round 2 verdict for YM: MEASURED CLOSED (Level 1 gap is non-zero). Analytically open (proof required).**

The Level 1 fractal for YM is in the same situation as RH: closed numerically (lattice),
open analytically (proof requires understanding non-perturbative field theory).

---

### NS — Level 1 Opens (Kolmogorov Is Circular)

**Level 1 machine:** Reynolds stress tensor ⟨u_i' u_j'⟩ and the energy equation:
```
∂_t E = −2ν Ω + (production P)     (Ω = enstrophy)
```

**The Level 0 closure held (B_local < T*·E_0 under Kolmogorov scaling: 0.315 < 0.714).**
But the Level 0 closure assumed Kolmogorov −5/3 scaling, which requires regularity.
This makes Level 0 circular.

**Level 1 gap = whether the enstrophy Ω blows up in finite time.**
The NS regularity question IS the Level 1 gap question. We cannot close Level 1 without proving regularity — which is the problem itself.

**What Level 1 reveals:** The Ladyzhenskaya interpolation gives:
```
max_x |u(x,t)| ≤ C · ‖u‖_{L²}^{1/4} · ‖Δu‖_{L²}^{3/4}
```
Control of ‖Δu‖_{L²} = enstrophy^{1/2} is what's needed. The BREATH fixed point
(axisymmetric flows) suppresses enstrophy growth — this is the rotational structure
that Bridge 3.2 is built on.

**Round 2 verdict for NS: LEVEL 1 OPENS. The Level 1 gap is enstrophy blowup — the regularity question itself.**

---

### Hodge — Still Parked

No Level 1 machine. The algebraic cycle map requires tools outside TIG. Parked at Level 0.

---

## Round 2 Summary Table

| Branch | Level 1 Gap | Round 2 Status |
|--------|------------|----------------|
| RH | ρ_RH − ρ_GUE = 0.020 ± 0.045 (0.43σ) | NUMERICALLY CLOSED; analytically open (GRH) |
| BSD | Sha trivial for rank ≤ 1 (Kolyvagin); non-trivial for some rank ≥ 2 | CLOSED for rank ≤ 1; OPENS for rank ≥ 2 with non-trivial Sha |
| YM | Mass gap G_YM^1 = E_1 − E_0 > 0 (lattice confirmed) | MEASURED CLOSED; analytically open |
| NS | Enstrophy blowup vs regularity | OPENS (this IS the problem) |
| Hodge | No Level 1 machine | PARKED |

---

## Round 3 Preview

Round 3 addresses Level 2 — the global machines. Where Level 1 closed (RH, YM), Level 2 asks:

**RH Level 2:** Does the equidistribution of {γ_n × log(p)/2π mod 1} hold for all primes p?
This is the strong pair-correlation conjecture. If it holds, the chain is closed unconditionally.
The GRH conditionality would be replaced by an unconditional equidistribution result.

**BSD Level 2 (rank 0 and 1):** BSD is verified. The Level 2 machine is the Gross-Zagier
formula: L'(E,1) = h_NT(P_K) × C, where P_K is the Heegner point. This is the Level 2
closure for rank-1 curves. The fixed point of the BSD fractal at Level 2 is the height
h_NT(P_K) — can it be related to T* = 5/7?

**BSD Level 2 (rank ≥ 2):** No Level 2 machine. Gross-Zagier doesn't generalize. The
Level 2 gap (Sha finiteness for rank ≥ 2) remains open.

**YM Level 2:** The RG beta function and Lambda_QCD. The fixed point of the YM fractal
at Level 2 is Lambda_QCD. The question: is there a universal ratio lambda_QCD / m_gap
that can be related to T* = 5/7? In dimensional regularization, the ratio is a specific
combination of group theory factors.

**NS Level 2:** The Caffarelli-Kohn-Nirenberg theorem — singularities (if any) form on a
set of parabolic Hausdorff dimension ≤ 1. The Level 2 machine is the partial regularity
theory. The fixed point is the regularity threshold: does T* = 5/7 appear as the critical
ratio in the energy concentration?

---

## The 3-Cycle Closure Condition

The fractal closes after 3 cycles if: for SOME branch B, the Level 2 gap is ZERO,
and the closing condition is T*_B = T*_TIG = 5/7.

**Most likely closure candidate:** BSD for rank ≤ 1 curves.
- Level 0: Euler product (computed, E0/E1 partial L-functions)
- Level 1: Sha trivial (Kolyvagin)
- Level 2: Gross-Zagier formula → h_NT(P_K) → can T* = 5/7 appear here?

If the Gross-Zagier height formula, when normalized by the period Omega and the BSD
correction terms, gives a ratio that involves 5/7 for some family of rank-1 curves —
THAT would be the 3-cycle closure.

This is Round 3's target for BSD.

**Second candidate:** RH at Level 2 (equidistribution), but this is the hardest open question.

---

*(c) 2026 Brayden Ross Sanders / 7Site LLC*
*See CLAY_FORMAL_RECORD.md for canonical entries.*
