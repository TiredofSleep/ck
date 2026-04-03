# HARD-WALL MEMO
## What the 3 Cycles Actually Closed, and What Still Does Not Close
*Author: Brayden Ross Sanders / 7Site LLC — 2026-04-02*
*Classification: Consolidation. No new searches. No new theory. Lock only.*

---

## PART 1 — RH: Cleanest Grounded Status After 3 Cycles

### A. Established in Our Program

The following are computationally established facts — not hypotheses, not analogies.

**1. Local machine runs correctly.**
The KDE estimator δ_t(T) = h√(2π) × (1/N) Σ K_h(D_{n,t}−1) − 1 is a well-defined
function of the input zeros. It was run on 5,000 Riemann zeros computed to 15-digit
precision via mpmath. The computation is repeatable and exact given the inputs.

**2. Locking condition measured.**
Across all 116 windows (T ∈ [14.1, 1493]):
```
δ₁ ≈ δ₂ + δ₃    residual = 0.6%   (noise floor = 7%)
ρ = M/δ₂ = 1.014 ± 0.045  (116 windows, zero spikes, zero sign changes)
```
This is a measured fact about these 5,000 zeros. It is not proved to hold for all zeros.

**3. Analytic GUE match established.**
The analytic GUE prediction (from the theoretical pair-correlation R₂(u) = 1−sinc²(u)
and the Gaussian KDE approximation δ_t = h/√(h²+σ_t²)−1) gives:
```
d1_GUE = −0.5362      d1_RH = −0.5363     agreement: 0.02%
d2_GUE = −0.3323      d2_RH = −0.3334     agreement: 0.3%
d3_GUE = −0.2058      d3_RH = −0.2063     agreement: 0.2%
ρ_GUE  = +0.9942      ρ_RH  = +1.0136     difference: 0.43σ
```
These numbers agree. The agreement is computed, not assumed.

**4. Finite-N GUE excluded as explanation.**
Numerical GUE simulation (N_MATRIX=800, 4 trials, ~3640 spacings/trial):
```
d1_num = −0.668   d2_num = −0.499   rho_num = +0.544
```
The finite-N simulation fails to reproduce the RH statistics at these sample sizes.
The failure is quantitative: ρ_num = 0.544 differs from ρ_RH = 1.014 by 10.5σ.
Finite-N GUE is excluded as a complete explanation of the RH locking at N=800 matrices.

**5. Equidistribution test passes at N=500.**
The KS distances from Uniform[0,1] for {γ_n × log(p)/(2π) mod 1}:
```
All 10 primes p ∈ {2,...,29}:  D_KS < T* = 0.714
Maximum D_KS = 0.0814 (p=7)
Maximum D_KS / T* = 11.4%
```
This is a computed fact about the first 500 zeros at these 10 primes.

---

### B. Strong Numerical Support (Supported, Not Proved)

**1. The Riemann zeros follow the theoretical (infinite-N) GUE distribution.**
Evidence: d1, d2, d3 match the analytic GUE prediction to <0.3%. This is consistent
with Montgomery's theorem (GRH conditional). It is not proved unconditionally.

**2. The locking ρ ≈ 1 persists as T grows.**
Evidence: stable across 116 windows, T ranging over 2.7 log-decades. Trend slope
= −0.012/log_T unit (mild). No regime breaks. But: trend direction (ρ → 0) means
the locking is weakening at a slow rate. Whether locking survives T → ∞ is unknown.

**3. The prime equidistribution holds for p ≤ 29, N ≤ 500.**
Evidence: D_KS < T* for all tested primes. But N=500 corresponds to T ≤ 811. This is
a thin slice of the zero spectrum. It is consistent with RH; it does not confirm RH.

**4. The locking is not a finite-N GUE artifact at N=800.**
Evidence: ρ_num = 0.544 ≠ ρ_RH = 1.014. But: at N → ∞, the GUE simulation would
converge to the analytic prediction ρ_GUE = 0.994. We did not run this limit.
The claim "finite-N GUE cannot explain the locking at ANY N" is not established.

---

### C. Still Open — The Exact Remaining Obstruction

**Theorem-shaped gap:** There is no unconditional proof that the pair-correlation of
normalized Riemann zero spacings converges to R₂(u) = 1 − sinc²(u). Montgomery's
proof of this requires the Generalized Riemann Hypothesis. The narrow-strip condition
(arXiv:2501.14545) weakens the hypothesis but does not eliminate it. The connection
from First-G → Fejér → sinc² → zero-spacing is proved through the continuum limit
(k → ∞) only, and the limit step requires GRH or equivalent.

**Exact formulation:** Let R₂^{(T)}(u) be the empirical pair-correlation of zeros
γ_n ≤ T. The open theorem is:
```
lim_{T→∞} R₂^{(T)}(u) = 1 − sinc²(u)     unconditionally.
```
This is not proved. Every known proof assumes GRH or a hypothesis of comparable strength.
Our measurements are consistent with this limit. They do not establish it.

---

### D. Strongest Honest One-Paragraph Verdict

The first 5,000 Riemann zeros, measured by a sliding-window KDE pair-correlation
estimator at bandwidth h=0.20, produce statistics (d1, d2, d3, ρ) that match the
theoretical GUE pair-correlation prediction to within 0.3% on individual estimators
and 0.43σ on the derived locking ratio ρ. A finite-N GUE matrix simulation (N=800)
fails to reproduce these statistics by 10.5σ, establishing that the locking is not
a finite-sample matrix artifact at this scale. A prime equidistribution test on the
first 500 zeros shows D_KS < T* for all primes tested up to 29. Taken together, these
results constitute strong numerical evidence that the Riemann zeros are consistent with
the GUE universality class at all measured scales. They do not prove RH, do not prove
the Montgomery pair-correlation theorem unconditionally, and do not connect the TIG
algebraic spine (First-G, T*, sinc² limit) to the zero distribution by any path that
avoids the GRH assumption. The program has measured precisely; it has not proved.

---

## PART 2 — Branch-by-Branch Hard Wall

---

### Branch: Riemann Hypothesis

**A. What Round 1 closed:**
Local machine operational. δ₁, δ₂, δ₃ measured from 5,000 zeros. Locking condition
δ₁ ≈ δ₂ + δ₃ found with 0.6% residual. Dual-lens scalar D/r² ≈ 0. ρ = 1.014 ± 0.045.

**B. What Round 2 closed:**
Finite-N GUE (N=800) excluded as explanation of locking (10.5σ discrepancy). Analytic
(infinite-N) GUE confirmed as consistent explanation (0.43σ gap). GUE universality
class confirmed at Level 1. The locking is theoretical-GUE calibration, not matrix artifact.

**C. What Round 3 closed:**
Prime equidistribution test passes for all p ≤ 29, N=500 zeros. D_KS/T* ≤ 11.4%.
Zeros are consistent with equidistribution at Level 2. No arithmetic deviation detected.

**D. Exact hard wall:**
*"This branch still fails to close because the analytical connection from sinc²
continuum limit to Riemann zero-spacing distribution requires GRH (or equivalent),
and no unconditional proof of this connection exists."*

**E. Type of hard wall:**
**Theorem gap.** The missing object is a proof of Montgomery's pair-correlation formula
without GRH assumption. This is a standard open problem in analytic number theory.

---

### Branch: BSD (Rank 0 and 1)

**A. What Round 1 closed:**
BSD Euler product local machine computed for three curves (E0, E1, E2). Partial
L-function S(47) = 2.124, 3.256, 1.973. Selmer tower recursion structure stated.
Gap object Sha identified as the non-local remainder.

**B. What Round 2 closed:**
Kolyvagin's theorem (1989, external) closes BSD for rank ≤ 1 curves analytically:
rank = analytic rank, Sha finite. This is not our result — it is the established external
theorem. Our local machine is consistent with it. Two falsifications documented:
rank staircase (16/16 misses) and CM-2 twist (rank=0, L≈8.909≠0).

**C. What Round 3 closed:**
Gross-Zagier formula identified as Level 2 machine for rank-1 curves. Search target
for T* appearance defined: |Sha|=25, |E_tors|=ℤ/7ℤ → L(E,1)/Ω = T*² = 25/49.
Search not run. Closure candidate identified, not confirmed.

**D. Exact hard wall:**
*"This branch (rank ≤ 1) still fails to connect to TIG because no algebraic map
from Z/10Z to the Gross-Zagier / Heegner height formula has been constructed, and
the T*² = 25/49 search target has not been confirmed in any curve database."*

**E. Type of hard wall:**
**Missing construction.** The Gross-Zagier formula is proved. What is missing is
any identification of TIG objects with Heegner heights, Selmer conditions, or
the BSD correction terms. This is a construction gap, not a measurement gap.

---

### Branch: BSD (Rank ≥ 2)

**A. What Round 1 closed:**
Same local machine as rank ≤ 1. Partial Euler products computable. Gap structure same.

**B. What Round 2 closed:**
Level 1 opens. Kolyvagin does not extend to rank ≥ 2. Sha finiteness unproved.
The Level 1 gap for rank ≥ 2 is an open Clay-level problem.

**C. What Round 3 closed:**
Nothing. No Level 2 machine was reached because Level 1 did not close.

**D. Exact hard wall:**
*"This branch still fails to close because the finiteness of Sha(E/ℚ) for rank ≥ 2
curves is not proved, and no TIG algebraic object corresponds to Sha."*

**E. Type of hard wall:**
**Branch-specific unknown.** Sha finiteness is one of the central open problems in
arithmetic geometry. TIG provides no path to it.

---

### Branch: Yang-Mills

**A. What Round 1 closed:**
SU(2) plaquette local machine computed analytically (strong-coupling and weak-coupling
expansions) at 6 coupling values. Delta(beta) table produced. Regime variable ρ_YM
computed. T* = 5/7 matches SU(2) glueball mass ratio m(0++)/m(2++) within 0.1%
(structural coincidence, not derived).

**B. What Round 2 closed:**
Lattice QCD results (external) confirm mass gap G_YM^1 = E_1 − E_0 > 0 for SU(2) and
SU(3). Level 1 gap is measured non-zero. Our plaquette expansion is consistent with
this. The analytical proof of mass gap positivity does not exist.

**C. What Round 3 closed:**
Lambda_QCD identified as Level 2 gap object (non-perturbative scale, essential
singularity of perturbation theory). Three-level fractal structure for YM stated.
No numerical closure of Level 2 — Lambda_QCD is not computable from our tools.

**D. Exact hard wall:**
*"This branch still fails to close because no analytical proof that the SU(N)
Yang-Mills mass gap is strictly positive exists, and the T* coincidence with the
SU(2) mass ratio is structural — it has not been derived from gauge group dynamics."*

**E. Type of hard wall:**
**Theorem gap.** The missing proof is the Clay Prize itself. The T* coincidence is
currently numerical; deriving it would require connecting Z/10Z algebra to the
representation theory of SU(2), which has not been done.

---

### Branch: Navier-Stokes

**A. What Round 1 closed:**
Dyadic shell machine computed. Under Kolmogorov −5/3 scaling: B_local = 0.315·E₀ < T*·E₀.
G_NS gap object = inter-shell transfer T_j formally defined. Five-scale table produced.

**B. What Round 2 closed:**
Level 1 opens immediately. The Kolmogorov scaling assumed in Round 1 is not a
consequence of the NS equations — it is the regularity assumption itself. The Level 0
closure is circular. No independent closure of Level 1 achieved.

**C. What Round 3 closed:**
Nothing. CKN partial regularity (singularities on measure-zero set) is referenced but
not computed. Level 2 not reached because Level 1 did not close independently.

**D. Exact hard wall:**
*"This branch still fails to close because the Level 0 result (B_local < T*·E₀) assumed
Kolmogorov scaling, which is equivalent to regularity, making the argument circular;
no a priori estimate deriving B_local < T*·E₀ from NS constants alone exists."*

**E. Type of hard wall:**
**Theorem gap.** The missing object is an interpolation constant estimate:
C ≤ T*·E₀^{1/2} in the Ladyzhenskaya inequality, derivable from viscosity ν and
initial energy E₀ alone. This is the precise form of the C2 bridge requirement.

---

### Branch: Hodge

**A. What Round 1 closed:**
The H^{p,q} Hodge decomposition and the G/E/S partition analog were noted. Markman's
2025 theorem (external) settled the Hodge conjecture for abelian fourfolds. Frontier
is now dimension ≥ 5.

**B. What Round 2 closed:**
Nothing new. No Level 1 machine exists from TIG. The algebraic cycle map requires
algebraic geometry tools outside Z/10Z algebra.

**C. What Round 3 closed:**
Nothing. Parked.

**D. Exact hard wall:**
*"This branch still fails to close because Z/10Z has no algebraic geometry, no Hodge
classes, and no cohomology with rational coefficients; the only TIG analog is a
structural partition (G/E/S), which is not a mechanism."*

**E. Type of hard wall:**
**Missing construction.** No TIG object can be algebraic cycle. This is a
structural impossibility, not a gap to be closed by better measurement.

---

## PART 3 — Confirmed vs. Proved: Ruthless Status Table

| Claim | Exact Math | Numerical Support | Conditional | Excluded/False |
|-------|-----------|------------------|-------------|----------------|
| Z/10Z spine (T*, TSML, BHML, First-G, Braid) | **YES — proved** | — | — | — |
| First-G = Fejér kernel / k (exact identity) | **YES — proved** | — | — | — |
| sinc²(1/2) = 4/π² | **YES — proved** | — | — | — |
| sinc² continuum limit R(k,f) → sinc²(f) | **YES — proved** | — | — | — |
| Corridor portrait ordering | **YES — proved** | — | — | — |
| RH locking δ₁≈δ₂+δ₃ at 0.6% residual | — | **YES — measured, 116 windows** | — | — |
| Analytic GUE compatibility (d1,d2,d3 <0.3%) | — | **YES — computed comparison** | — | — |
| ρ_RH − ρ_GUE = 0.43σ (not significant) | — | **YES — computed** | — | — |
| Finite-N GUE (N=800) as explanation of locking | — | — | — | **EXCLUDED — 10.5σ discrepancy** |
| Finite-N GUE at ALL scales excluded | — | — | **Conditional** (only tested N=800) | — |
| RH equidistribution D_KS < T* (p≤29, N=500) | — | **YES — computed** | — | — |
| RH equidistribution D_KS → 0 as N → ∞ | — | — | **Conditional** (RH or GRH) | — |
| Montgomery R₂(u)=1−sinc²(u) unconditionally | — | — | **Conditional** (requires GRH) | — |
| First-G → zero-spacing (no GRH) | — | — | **Conditional/open** | — |
| BSD rank ≤ 1 fully verified (Kolyvagin) | **YES — external theorem** | — | — | — |
| BSD Euler product S(47) values computed | **YES — algorithm correct** | — | — | — |
| BSD rank staircase rank=⌊(p−1)/10⌋ | — | — | — | **FALSIFIED — 16/16 misses** |
| CM-2 twist condition forces rank ≥ 2 | — | — | — | **FALSIFIED — 9725.a1 rank=0** |
| BSD rank ≥ 2 closed | — | — | **Conditional** (Sha finite?) | — |
| T*² = 25/49 in BSD for some curve | — | — | **Conditional** (search not run) | — |
| YM mass gap G_YM > 0 (SU(2), lattice) | — | **YES — external lattice data** | — | — |
| T* = m(0++)/m(2++) for SU(2) derived | — | — | **Conditional** (not derived) | — |
| T* ≈ m(0++)/m(2++) for SU(2) (0.1%) | — | **YES — numerical coincidence** | — | — |
| YM analytical mass gap proof | — | — | **Conditional** (Clay Prize) | — |
| NS shell cascade B_local < T*·E₀ unconditionally | — | — | **Conditional** (assumes K41) | — |
| NS B_local < T*·E₀ from NS constants alone | — | — | **Open** (not established) | — |
| NS regularity (no blowup) | — | — | **Conditional** (Clay Prize) | — |
| Hodge conjecture dim ≤ 4 (Markman 2025) | **YES — external theorem** | — | — | — |
| Hodge conjecture dim ≥ 5 | — | — | **Open** (Clay Prize frontier) | — |
| TIG as proof engine for any Clay branch | — | — | — | **FALSE — no branch proved** |

---

## PART 4 — Real Dominoes and Non-Dominoes

### Real Dominoes (Things That Actually Fell)

**1. Finite-N GUE excluded as complete explanation.**
The specific claim "the RH locking ρ ≈ 1 is just what any GUE matrix ensemble produces
at bandwidth h=0.20" is false at N=800. The finite-N simulation gives ρ ≈ 0.544, not 1.014.
This is a 10.5σ exclusion. It is a real result. It means the locking is specifically
associated with the theoretical (infinite-N) GUE, not with finite matrix models.

**2. Analytic GUE compatibility strengthened to <0.3% on individual estimators.**
The theoretical GUE prediction matches the RH measurement to <0.3% on d1, d2, d3.
This is a stronger compatibility statement than was possible before the calibration.
The RH zeros and the infinite-N GUE theory are co-calibrated at these sample sizes.

**3. The recursion spine grammar is stable across all five branches.**
After 3 cycles, the common structure (local machine → accumulate → gap) is confirmed
in each branch independently. This is a structural finding about how these problems
are organized, not about their solutions. It is stable — adding more cycles will not
break it.

**4. Exactly two BSD candidates eliminated.**
The rank staircase and CM-2 twist are dead. Any future BSD bridge proposal that
relies on conductor-only arithmetic or naive Z/5Z twist conditions is pre-falsified.

**5. Branch-specific hard walls precisely located.**
After 3 cycles, we know exactly which level each branch fails at and why. This is not
a trivial result — before the 3-cycle analysis, the failure modes were described in
general terms. They are now specifically named.

**6. Equidistribution evidence established at N=500, p≤29.**
The prime equidistribution test is a new measurement. The result (D_KS < T* for all
tested primes) is a clean numerical fact. It was not known before this session.

---

### Non-Dominoes (Things That Did Not Fall)

**RH is not proved.**
Nothing in the 3-cycle analysis constitutes a proof or partial proof of the Riemann
Hypothesis. The zeros are consistent with RH. Consistency is not implication.

**BSD is not solved.**
The Euler product computation, the Selmer tower structure, and the T*² search target
are organizational tools. BSD for rank ≥ 2 is fully open. BSD for rank ≤ 1 is closed
by Kolyvagin — not by our program.

**YM is not solved.**
The plaquette computation and the T* mass ratio coincidence are structural observations.
No analytical mass gap proof exists. The coincidence, however precise, is not a derivation.

**NS is not solved.**
The shell machine assumed Kolmogorov scaling. The Level 0 result is circular. The
regularity problem is untouched.

**The TIG bridge to any Clay branch is not established.**
No algebraic map from Z/10Z to any Clay-branch mathematical object has been constructed.
The recursion spine is a structural parallel, not a mechanism. The spectrometer is
measuring; it has not caused anything.

**The GRH conditionality is not removed.**
The GUE calibration, the locking measurement, and the equidistribution test are all
consistent with Montgomery's theorem. They do not prove it unconditionally.

---

## PART 5 — "The Program Knows Its Own Shape"

**"The program now knows its own shape in the sense that it has precisely located,
for each of the five Clay branches, the level at which TIG's local machine runs out
and the branch-specific hard wall begins: NS and BSD rank≥2 at Level 1, RH and YM
at Level 2, Hodge structurally, and it has characterized each wall as a specific
missing theorem or construction rather than as a vague open problem."**

**What that buys:**
- No more mis-aimed effort. A proposal that tries to prove RH by reading off the TIG
  algebra is pre-blocked by the Level 2 analysis.
- Clear prioritization. The most tractable closure target is BSD Level 2 (T*² search),
  because it is a computable database query, not a proof.
- Honest external communication. The program can state exactly what it has and has
  not established, without overstating or understating.
- Future sessions start from bedrock, not from momentum.

**What it does not buy:**
- A proof of anything. Knowing the shape of a problem is not solving it.
- A bridge to any Clay branch. The walls are named; they are not crossed.
- Validation from the Clay Prize committee. The committee requires proof, not structure.
- Evidence that T* = 5/7 is the right fixed point for any branch. It is the TIG fixed
  point. Whether it is a fixed point of YM, RH, or BSD is still a conjecture.

---

## PART 6 — Strongest Synthesis

**"After 3 cycles, the Clay program has closed the recursion spine grammar across all
five branches and isolated the exact theorem-shaped gap that separates each branch's
local machine from its global closure — establishing a precise map of where the
mathematics of TIG reaches and where it runs out."**

---

## PART 7 — Strongest Boundary

**"What still separates the current program from actual Clay-level closure is the
absence of any algebraic map from Z/10Z to a mathematical object internal to any
Clay problem — no such map has been constructed, and without it, TIG's role is
measurement and structural framing, not proof."**

---

## OUTPUT SECTION

### Exact Status Table (Condensed)

| Branch | Level Reached | Hard Wall | Wall Type |
|--------|--------------|-----------|-----------|
| RH | L2 (measured) | GRH conditionality in Montgomery step | Theorem gap |
| BSD rank≤1 | L2 (Kolyvagin, external) | No TIG map to Gross-Zagier / Heegner heights | Missing construction |
| BSD rank≥2 | L1 (fails) | Sha finiteness unproved, no TIG object | Branch-specific unknown |
| YM | L2 (lattice, external) | No analytical mass gap proof; T* not derived | Theorem gap |
| NS | L1 (fails, circular) | No a priori B_local bound from NS constants alone | Theorem gap |
| Hodge | L0 (parked) | Z/10Z has no algebraic geometry | Missing construction (structural impossibility) |

---

### Domino / Non-Domino Table

| Item | Domino? | Evidence |
|------|---------|----------|
| Finite-N GUE (N=800) excluded | YES | 10.5σ discrepancy; computed |
| Analytic GUE compatibility <0.3% on d1,d2,d3 | YES | Direct comparison; computed |
| Common recursion spine grammar | YES | Structural; confirmed across 5 branches |
| Two BSD candidates falsified | YES | Empirical test; 16/16 misses + LMFDB |
| Branch hard walls precisely named | YES | 3-cycle analysis; structural |
| RH proved | NO | Not established by anything in the program |
| BSD solved (any rank) | NO | Not established |
| YM solved | NO | Not established |
| NS solved | NO | Not established |
| GRH conditionality removed | NO | All proofs still require it |
| TIG bridge to any Clay branch | NO | No algebraic map constructed |
| T* = 5/7 is fixed point of any Clay branch | NO | Conjecture; not proved for any branch |

---

### Collaborator-Facing Paragraph

The 3-cycle analysis has produced the following verifiable results: (1) the first 5,000
Riemann zeros match the theoretical GUE pair-correlation prediction to within 0.3% on
individual lag estimators, with a locking ratio ρ = 1.014 ± 0.045 consistent with the
analytic GUE prediction of ρ = 0.994 (0.43σ difference); (2) a finite-matrix GUE
simulation at N=800 fails to reproduce this locking by 10.5σ, establishing that the
effect is specific to the infinite-N GUE universality class rather than to finite matrix
models; (3) a prime equidistribution test on 500 zeros at 10 primes produces D_KS < T* for
all cases; and (4) the recursion spine structure (local machine → accumulate → gap) is
confirmed as a common organizing framework across all five Clay branches, with each
branch's hard wall precisely identified as a specific missing theorem or construction.
None of these results constitute a proof of any Clay conjecture. The TIG algebraic
framework (Z/10Z, T* = 5/7, First-G) operates as a measurement and organizational
instrument; no algebraic map from Z/10Z to any Clay-branch mathematical object has been
constructed.

---

### Public-Safe Paragraph

This research program (CK / TIG / 7Site LLC) has developed a novel measurement framework
applied to the Clay Millennium Problems. Using an algebraic structure derived from the
ring Z/10Z, the program has identified a common recursive grammar shared by all five
active Clay problems, measured the pair-correlation statistics of the first 5,000
Riemann zeros with high precision, and confirmed numerical consistency with the GUE
universality class. The program has also documented two falsified conjectures in the
Birch and Swinnerton-Dyer direction. None of the Clay problems have been solved. The
program's contribution is a precise structural map of where algebraic measurement
reaches, and where proof-level mathematics begins.

---

*(c) 2026 Brayden Ross Sanders / 7Site LLC*
*7Site Public Sovereignty License v1.0 — Human use only. Free forever.*
*DOI: 10.5281/zenodo.18852047*
*This memo supersedes all exploratory memos for the purpose of stating program status.*
