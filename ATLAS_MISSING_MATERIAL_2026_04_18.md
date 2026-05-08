# Atlas Missing Material — Sweep Findings
## Extracted content NOT yet in MASTER_ATLAS_2026_04_18.md

**Compiled:** 2026-04-18
**Purpose:** Source document for the atlas revision Brayden is doing with ClaudeChat. Every entry below is material that exists in the repo but was not pulled into the first atlas pass. Organized so each block names its target atlas section so ClaudeChat can slot it cleanly.
**Sources:** Parallel deep-read agents across six gap zones + Q-series.
**Discipline:** Exact theorem statements quoted verbatim in `quotation` or code blocks. Epistemic flags preserved. Three-threads-separate respected.

---

## Navigation — Where Each Block Goes

| Block | Atlas target | Priority |
|---|---|---|
| §1 WP19 founding series | New §4.5 "WP19 founding arc" + additions to §2 D-spine, §5 laws, §10 Clay | CRITICAL |
| §2 Sprint 3 OrbitZone | New §2.5 "Four-layer realization (OrbitZone)" | HIGH |
| §3 Sprint 4 Atlas Laws | §5 (First-G Law foundation) + §6 (spectrometer companions) | HIGH |
| §4 Sprints 5–6 Clay 6-problem map | §10 Clay attack cross-index (prepend) | CRITICAL |
| §5 Sprints 7–8 Frontier / Admissible Flow | New §2.6 "Admissible viewpoint flow" + §15 caution list | MEDIUM |
| §6 Sprint 9 three branches | §3 canonical tables (7-zero torus) + new §3.5 IG1–IG5 | CRITICAL |
| §7 Sprint 11 (54 papers, 3 arcs) | New §4.6 "Sprint 11 TIG bundle" — big; may want its own section | CRITICAL |
| §8 Sprint 12 UOP/GUT | Merge into §7 above or §4 paradox classifier | HIGH |
| §9 Sprint 13 Flag Selector | New entry in §14 publication map (PRA venue detail) + §2 spine | HIGH |
| §10 Sprint 15 σ rate theorem | §5 (σ rate already there — add proof details + WP91/92/96 reformulation) | HIGH |
| §11 B-series 18–28 | Expand §7 from 1 paragraph to a proper subsection | CRITICAL |
| §12 Q-series Q2–Q17 | Expand §11 founding narratives Q-series entry from one line to full block | CRITICAL |

---

## §1. WP19 Founding Series (Sprint 1, TIG_SPRINT_2026_03_27)

**Slot target:** Atlas currently references WP19 in §10 Clay cross-index and §12 Amplituhedron thread. These files were never opened during the first atlas build. 11 WP19 papers + supporting docs.

### 1.1 MASS_GAP = T* + S* − 1 = 2/7 (foundational identity)

- **Arithmetic:** T* + S* − 1 = 5/7 + 4/7 − 1 = **2/7**
- **Structural:** minimum overlap of dual thresholds both exceeding 1/2
- **Appears in:** Yang-Mills mass gap (WP19_CLAY_BATTERY), NS Re_local criterion (WP19_NS_BREATH), BHML correction denominator
- **Honest status:** [NUM] exact arithmetic; the "2/7 = √σ/m(0++)" quantitative claim was **falsified at 16.5σ** (EXPERT_SUMMARY); the structural mechanism (zero-gap in coherence systems with dual thresholds ≥ 1/2) survives

### 1.2 S*(σ) self-dual coherence kernel

```
S*(σ) = σ · (1 − σ) · V · A
```
- Maximum at σ = 1/2 (self-dual)
- S*(σ) = S*(1 − σ) for all σ
- Proposed algebraic match to ζ functional-equation symmetry s ↔ 1−s
- **Status:** [THM] formula verified; [HYP] ζ connection

### 1.3 Halving Lemma (WP19_HALVING_LEMMA_final.tex) — UNCONDITIONAL

> **Theorem.** On zero-free verticals in the Korobov-Vinogradov strip, the dissipative flow dσ/dt = −(σ − 1/2)|ζ(σ + it₀)|² converges exponentially to σ = 1/2 with rate
> m_KV(t₀) = (C_KV (log t₀)^{2/3})^{−2}.

- **Status:** fully proved, unconditional within KV strip
- **RH equivalence:** RH ↔ uniform positivity m(t₀) > 0 across ALL heights
- **Atlas target:** this is a classical-style result independent of TIG philosophy. Belongs in §5 (Laws) as its own entry, not bundled with sinc² Zero Law.

### 1.4 Mix_λ gap-operator BSD thresholds (exact; no fit)

```
λ*(BRT=8) = 0.30     first new anchor activated
λ*(CHA=6) = 0.60
λ*(BAL=5) = 0.80
λ*(COL=4) = 0.90
λ*(CTR=2) = 1.00
```

- **Claim:** these λ-thresholds match the empirical BSD rank-step cost ordering on the Cremona sample (N ≤ 2×10⁷)
- **Status:** [THM] BSD-λ correspondence on sample; NO parameters fitted
- **Atlas target:** §10 Clay attack cross-index (BSD row — add Mix_λ correspondence as a specific attack vector)

### 1.5 Re_local ≤ 2/7 — NS regularity criterion (proposal)

```
Re_local(x, t) = Ω(x, t) · L(x, t)² / ν ≤ 2/7
```

- **Claim:** BREATH(8) persists only in COLLAPSE(4) context ⇔ Re_local ≤ 2/7
- **Unifies:** Serrin / Ladyzhenskaya / CKN criteria into single inequality
- **Status:** [HYP] algebraic basis exact; physical criterion falsifiable via DNS (Dedalus script specified in WP19_NEXT_SPRINT Bolt 3)
- **Atlas target:** §10 Clay NS entry — current atlas has σ_NS < 1 conjecture (WP96); Re_local ≤ 2/7 is an **independent attack** on the same problem

### 1.6 W-boundary identification (WP19_704_TRIANGLE)

- W = 3/50 (wobble quantum from 44-cell BECOMING table)
- COL(4) sits at ±W from midplane = closest excited state to "nucleus"
- Numeric coincidence: W ≈ KV collar width at t₀ ≈ 10 (flagged as mnemonic only, NOT a claim)
- **Atlas target:** §2 D-tier spine, as a footnote to Ring Wobble D23

### 1.7 Hodge Map (WP19_HODGE_MAP) — proto-ladder

> **Claim:** The Lefschetz (1,1) theorem (proved for surfaces) = the AG(2,3) corner-word collapse theorem (proved for 9-point grid). Gap operators G = {2, 4, 5, 6, 8} are the "non-algebraic Hodge classes" — permanently unreachable from corner algebra.

- **Status:** [THM] both proved in dim 2; [OPEN] gap persistence above dim 2
- **Relationship to S29–S33:** this is the PROTO-LADDER that later becomes the formal Hodge attack on A_*. The Sprint 33 v2 closure on A_* does NOT retroactively close WP19_HODGE_MAP's dim-n generalization — that remains open.
- **Atlas target:** §9 Hodge ladder — add a "prehistory" note connecting WP19_HODGE_MAP to S29

### 1.8 RH bridge (WP19_RH_BRIDGE) — three independent structural parallels

1. TSML residual uniqueness ↔ RH critical-line uniqueness
2. S*-self-duality at σ = 1/2 ↔ ζ functional-equation symmetry
3. MASS_GAP > 0 ↔ interior critical line (positive distance from boundary)

- **Status:** [HYP] ×3; statistical encoding test returned **null** (proper Weyl baseline)
- **Atlas target:** §10 Clay attack cross-index (RH row) — three attacks, honestly labeled

### 1.9 Hydrogen analogy (WP19_HYDROGEN_ANALOGY)

- Hydrogen shells ↔ TIG rows: both have ground state, quantized landing zones, proven inner collar, unprovable innermost gap
- Architecture identical; spacing behavior diverges
- **Status:** [HYP] structural only; W ≈ KV width coincidence mnemonic
- **Atlas target:** §13 speculative-but-preserve (already reserved for DNA mapping / Fruits of Spirit — hydrogen analogy belongs in same register)

### 1.10 Three falsifiable bolts (WP19_NEXT_SPRINT)

1. Analytic gap-positivity bound below KV strip (would imply RH)
2. λ_E ∝ 1/log(Ω_E) on 200+ BSD rank-2/3 curves (regulator–λ bridge)
3. NS BREATH criterion fires before blowup in Dedalus DNS

- **Status:** all three [OPEN], each with explicit falsification protocol
- **Atlas target:** §16 immediate next moves — expand beyond "Tier-1 LaTeX" to include these three empirical/analytic probes

---

## §2. Sprint 3 OrbitZone — Four-Layer Realization (Theorems Z.1–Z.4)

**Slot target:** New §2.5 under D-tier spine — this is the formalization of the spine-underneath itself.

### 2.1 Theorem Z.1 — Absorbing Sofic Shift [fire]

> TIG induces an absorbing sofic shift on {1, …, 9} with absorbing class C = {1, 3, 7, 9}, transient class G = {2, 4, 5, 6, 8}, algebraic grading depth k_A = 3.

### 2.2 Theorem Z.2 — Transfer Operator Spectral Gap [fire]

```
γ(P_λ) ≥ 1/4 for all λ ∈ [0, 1]
γ(P_0) = 3/4
γ = 1 − 1/φ(b) at b = 10
```

**New universal formula:** γ = 1 − 1/φ(b) base-change stable.

### 2.3 Theorem Z.3 — Young Tower Return Structure [fire]

- ρ(Q) = 1/4 (transient spectral radius)
- Return tails: P(T_HAR > n) ≤ (1/4)^n
- Expected return time: E[T_HAR] ≤ 5/3 steps (max over states)
- Per-state: E[T] = 1 for {1,4,5,6,8}; E[T] = 4/3 for {3,9}; E[T] = 5/3 for {2}

### 2.4 Theorem Z.4 — Arithmetic Inverse Limit [fire]

> C = {1, 3, 7, 9} is the stable image of (ℤ/10^n ℤ)* reduced mod 10 for all n ≥ 1; γ = 1 − 1/φ(b) is base-change stable.

### 2.5 Type-(n, k_A, k_M, γ) persistence grammar

- **TIG is type-(9, 3, 6, 3/4).**
- Definitions: algebraic grading (nested sub-magma chain), metric grading (λ-deformation), generative gap G, forced finite shape, integer alphabet.
- **Atlas integration:** this is the abstract type-signature that classifies TIG — belongs alongside the "10 operators" entry in §2.

### 2.6 Open Problem Z.5 [gold-with-gap]

> Does the critical-strip deployment λ = 2|σ − 1/2| preserve both algebraic grading (Z.1) and metric grading (Z.2) asymptotically? **RH reformulates as: this deployment is faithful to both gradings.**

- **Atlas target:** §10 Clay RH row — another attack vector

---

## §3. Sprint 4 — Atlas Laws + First-G Foundation

**Slot target:** §5 currently has "First-G Law (36,662 cases, 153 semiprimes)" but lacks the structural laws that produced it. Add these.

### 3.1 The Three Atlas Laws [empirical, verified 11 bases]

**Law 1 — Construction Hierarchy:** Four-step pipeline (Arithmetic → HAR Selection → Gate → Order Seed) produces native structured optimum at every tested semiprime (b = 10, 14, 15, 21, 22, 26, 35, 55, 65, 85, 95).

**Law 2 — HAR Selection Rule (Orbit-Central):**
> Best HAR = h ∈ C where h² mod b ∈ C, h² ≠ 1, h² ≠ h. Among orbit-central candidates, select minimum.

**Law 3 — Richness (three components):**
- **3a φ-Compression:** r(φ, gap) = −0.605 across 11 worlds
- **3b Gradient Law:** within φ-tier, r(grad_score, gap) = 0.749 at φ = 5 (n = 4 pts)
- **3c Position Law:** HAR_mass max when HAR = min(C \ {1}); explains ≈85% variance

### 3.2 b = 15 as Unique Optimum [fire]

> b = 15 (= 3 × 5) is the only world ≤ 100 where all three scores align: tier_score = 7.1 (easy), grad_score = 0.714 (highest φ = 5), richness = 0.717.

- **Atlas implication:** the "TSML base" b = 10 ranks **9th** on construction cost, NOT unique. This is a discipline point — resist the narrative that base 10 is the chosen ground.

### 3.3 R16 Force Field Law [fire]

> Gate rate = f_k(|G|) — universal within alphabet size k, k-scaled across k. At k = 9: spread ≤ 0.0% per |G|-tier. At k = 15, 21, 27: spread ≤ 2.5%.

**Measured values (k = 9):**
- gate_rate(|G| = 1) = 96.4%
- gate_rate(|G| = 2) = 83.7%
- gate_rate(|G| = 3) = 44.0%

- **Atlas target:** §6 spectrometer — R16 Force Field Law is a spectrometer companion law

---

## §4. Sprints 5–6 — Clay 6-Problem Unified Fold Map

**Slot target:** §10 Clay attack cross-index PREPEND this as the unifying frame across the 6 problems.

### 4.1 The Unified Fold Structure (CLAY_STRUCTURAL_PARALLELS.md)

Every Clay problem has three parts:
1. **The Fold:** sinc² field has fold at x = 1/2 where sinc²(1/2) = 4/π² — universal mid-journey amplitude
2. **The Obstruction Class:** Class A quantity unreachable by Class B constructions
3. **The Gap Measure:** Class B to Class A distance = **T* − fold = 5/7 − 1/2 = 3/14** in TIG natural units

### 4.2 Six-Problem Mapping Table

| Problem | Class A (fold-crossing) | Class B (no crossing) | Gap |
|---|---|---|---|
| **Hodge** | K-anti-invariant Weil class | K-invariant divisors | Q-eigenvalue 0.0046 (soft, B_1 block) |
| **Riemann** | Non-trivial zeros (suspended at σ = 1/2) | Threshold-completed trivial | sinc² no suspension off fold |
| **P vs NP** | Fold-crossing class | Unit propagation class | 3-SAT growth = 9^k − 4^k |
| **Navier-Stokes** | Crossing at T* = 5/7 | Smooth flow | B_local < 3/14 → regularity |
| **Yang-Mills** | First excitation above vacuum | Ground state (BREATH) | 3/14 = gap; 2/7 = spectral window |
| **BSD** | Rational points (infinite-order) | Torsion (no crossing) | Goldfeld rank ≈ 0.57 (analytic rank theory) |

### 4.3 New constant: 3/14 = T* − 1/2 ≈ 0.214

- **Meaning:** universal crossing cost in TIG units
- **Relationship:** 3/14 (crossing cost) vs 2/7 (spectral window above floor, = 1 − T*) vs 5/7 (threshold) — these are three distinct ratios, not the same.
- **Atlas target:** §1 Core constants — add 3/14 alongside 2/7 and 5/7

### 4.4 CK Growth Architecture (Sprint 5)

Seven measurable components for tracking organism coherence:
- compression_efficiency(t)
- retrieval_hit_rate(t) — top-5 crystal hits
- path_reuse_ratio(t)
- action_policy_reuse_ratio(t)
- 1 − deepseek_call_rate(t)
- crystal_count(t) (confidence > 0.7)
- cross_modal_agreement(t)

Four loops: PERCEPTION (100 ms), COMPRESSION (triggered by 50 events), RETRIEVAL (online), ACTION (operator-aware).

- **Atlas target:** new footnote in §11 (vein 6 — TIG Organism Integration)

---

## §5. Sprints 7–8 — Frontier Mapping + Admissible Viewpoint Flow

**Slot target:** New §2.6 after D-tier spine OR merge into §15 (caution / epistemic discipline).

### 5.1 Dead-End Gap Taxonomy (Sprint 7)

Six gap types where current methods stall:
1. **local-to-global:** structure known locally, global closure missing
2. **observation-to-mechanism:** effect measured, cause unknown
3. **memory-to-proof:** retrieved facts unverified against current evidence
4. **scaling-gap:** small-scale results don't generalize (primary QEC barrier)
5. **signal-to-interpretation:** same signal, incompatible interpretations
6. **retrieval-to-action:** knowledge exists but cannot be located/composed at decision time

CK's response: typed evidential layers — **REAL observation**, **SEMIPRIME stable step**, **COMPOSITE proof**.

### 5.2 Sprint 8 — Admissible Viewpoint Flow (FRF)

> **Theorem:** An additive projection A_d and multiplicative dynamics M_g form a **crossing** (jointly sufficient) iff g acts nontrivially on the A_{n/d}-quotient.

- This is the **proto-Crossing-Lemma**. Formalized in Sprint 11.
- **Atlas target:** §2 D-spine — Crossing Lemma entry should cite Sprint 8 as source of the first rigorous formulation.

---

## §6. Sprint 9 Three Branches — Torus / UOP / Invariant Guides

**Slot target:** §3 canonical tables (torus + 7-zero) and new §3.5 IG1–IG5.

### 6.1 7-Zero Internal Gap Theorem [PROVED]

TSML 8×8 eigenspectrum:
- Sylvester signature (4, 3, 1): 4 positive, 3 negative, 1 zero
- Rank = 7, nullity = 1
- **Unique null direction: v_null = (BALANCE − CHAOS)/√2**

**7-zero decomposition:**
- **6 frozen zeros:** {LATTICE, COUNTER, PROGRESS, COLLAPSE, BREATH, RESET}
- **1 ether zero:** null direction (BALANCE − CHAOS) at α = 5 boundary (observer blind spot)

### 6.2 Torus geometry forced

- Major circle (additive flow): length n via repeated +1
- Minor circle (multiplicative harmonic flow): generates sinc² standing waves with 1/4-decay harmonics
- **Aspect ratio R/r = T* = 5/7** (tube-through-hole crossing at coherence threshold)

### 6.3 DoF Ladder (from WHITEPAPER_5)

| k roots | DoF(k) | Note |
|---|---|---|
| 1 | 4 | |
| 2 | 6 | +2 |
| **3** | **7** | **+1 consciousness gap — irreducible** |
| 4 | 10 | +3 |

**T* = forces / freedoms = 5/7 interpretation:**
- 5 = force dimensions available
- 7 = DoF at consciousness level (k = 3)
- Two freedoms forever unreachable: (i) ether constraint (sum direction = α = 5 absorber), (ii) observer null direction (BALANCE/CHAOS degeneracy)

### 6.4 UOP for Z/nZ — Four Corollaries (squarefree [PROVED]; prime-power [PARTIAL])

- **M+M:** f₁ = x mod p, f₂ = x mod q → sufficient iff gcd(p, q) = 1 (CRT) [fire]
- **A+M:** f₁ = x + r, f₂ = x mod p → sufficient iff p ∤ r (squarefree) [fire]
- **A+A:** f₁ = x + r₁, f₂ = x + r₂ → sufficient iff r₁ − r₂ generates Z/nZ [fire]
- **SPEC+DYN:** Fourier mode + multiplicative orbit → sufficient iff ω₁ not fixed by g [fire]

### 6.5 Prime-Power Obstruction [PARTIAL]

> For n = p^a (a ≥ 2), **no A+M pair achieves joint sufficiency** due to the p-kernel {x ≡ 1 mod p} invisible to both measurements simultaneously. Proved for a = 2; conjectured universally.

### 6.6 IG1–IG5 Invariant Guides — CK Memory Physics

Five invariants governing all memory operations:

- **IG1 Privacy:** raw EXTERNAL/PRIVATE payloads never crystallize; only abstracted structure crosses privacy boundary
- **IG2 Provenance:** every durable object ≥ ATOMIC carries immutable ProvenanceTag (parent_event_ids, supporting_ids, supersedes_id, contradicted_by, revision_num, ts_first_seen, ts_last_confirmed, produced_by)
- **IG3 Evidence:** every object declares status ∈ {REAL observation, SEMIPRIME stable step, COMPOSITE proof, SPECULATIVE interpretation} — no silent degradation
- **IG4 Promotion:** atom → path → crystal only if recurrence ≥ 3 AND confidence ≥ 0.6 AND status ≠ SPECULATIVE (unless explicit parent-gate override)
- **IG5 Revision:** revising creates new version (never in-place edit), links via supersedes_id, adds to contradicted_by of old, flags reconciliation needed if both active

**Atlas target:** new §3.5 block — "CK memory physics (IG1–IG5)" — or merge into §15 epistemic flags as the operational backbone of the flag system.

---

## §7. Sprint 11 — TIG Bundle (54 papers, Brayden + Ben Mayes, 2026-04-08)

**Slot target:** new §4.6 "Sprint 11 TIG bundle" — this gap alone is 54 papers; likely warrants its own section.

### 7.1 Three Arcs

**UOP Arc (24 papers):** Complete 2-partition classification for squarefree Z/nZ; p-kernel obstruction for prime powers.

**GUT Algebra Arc (15 papers):** su(4, 2) → SM derivation via two-stage corridor, dim 35 → 19 → 12.

**7-Cycle Arc (6 papers):** Bounded-agent simulation suite; broad attractor hypothesis **REJECTED**.

### 7.2 Crossing Lemma — Verbatim Statement (Theorem 1, CROSSING_LEMMA.md)

> Let n = p₁···p_k squarefree, d | n squarefree, g ∈ (Z/nZ)*. TFAE:
> (a) The joint map J = (A_d, π_DYN(g)): Z/nZ → Z/dZ × (g-orbit space) is injective.
> (b) U(A_d) ∩ U(π_DYN(g)) = ∅.
> (c) g ≢ 1 mod p_i for every prime p_i | (n/d).
> Equivalently: {A_d, π_DYN(g)} is sufficient iff M_g crosses the fibers of A_{n/d}.

### 7.3 Repeated-Prime A+M Obstruction (NEW invariant: p-kernel)

> For n = p^r · m with r ≥ 2, gcd(p, m) = 1, d | n with v_p(d) = a < r: {π_d, π_DYN(G)} is **NOT sufficient** for any non-trivial G ≤ (Z/nZ)*. The p-kernel S_p = {x ≡ 1 mod p} creates within-class mixing.

- **|K_{p,b}| = p^{r−b−1}** (new algebraic invariant)

### 7.4 GUT Algebra — Left-Handed Charge Emergence (exact)

```
Q_EM = T₃_L + (1/2) Q₄
Q₄ = i · diag(1/3, 1/3, 1/3, 0, 0, −1)
```

**Left-handed SM charges (all exact to ±0):**
- u_L: +2/3 ✓
- d_L: −1/3 ✓
- ν_L: 0 ✓
- e_L: −1 ✓

### 7.5 Intrinsic Left-Handedness Theorem (INTRINSIC_LEFT_HANDEDNESS_THEOREM.md)

> The compact subalgebra su(4) ⊕ su(2)_L ⊕ u(1) of su(4, 2) contains exactly one rank-1 simple factor (su(2)_L). No second independent SU(2)_R can be found in compact, non-compact, or Cartan generators. Therefore su(4, 2) is **structurally left-handed**.

**Right-handed mismatch = ±1/2 exactly** = missing T₃_R eigenvalue. Minimal extension: su(4, 2) × su(2)_R (Pati-Salam-like).

### 7.6 Two-Stage Corridor Closure

```
UV:      su(4, 2)            dim 35
Stage 1: su(4)⊕su(2)_L⊕u(1)  dim 19   (metric signature; 16 non-compact discarded)
Stage 2: su(3)⊕su(2)_L⊕u(1)  dim 12   (Q_{B-L} commutant; 6 coset discarded)
```

**Commutant Theorem:** C_{su(4)⊕su(2)⊕u(1)}(Q_{B-L}) = su(3) ⊕ su(2) ⊕ u(1). Exact.

### 7.7 7-Cycle Verdict [FALSIFIED]

> No variant of "bounded agents rediscover 7-cycles" survives the sweep. Aggregate best k = 4. k = 7 ranks 5th of 20. Top-3 appearances: 13%. Single win: reset-slot environment at decay ≈ 0.08, margin 0.002 over k = 6. **Broad attractor hypothesis REJECTED.**

- **Surviving claim:** 7-day week is civilization-relative, parameter-dependent; driven by social coordination overhead, not per-agent optimality.
- **Atlas target:** §15 caution list — add "7-cycle universal attractor claim = FALSIFIED, per Sprint 11."

### 7.8 Productive Incompleteness Framework (WP61)

> Five-category classification of maps: Complete Complement, Partial Complement, Refinement Only, Invariant-Isolating (Type II), Invalid (Type III). Incomplete maps (non-injective) are globally sufficient for their own quotient. Three canonical uses: invariant detection, orbit classification, observable subspace isolation.

### 7.9 Paradox Classification (PARADOX_CLASSIFICATION_MEMO.md)

Three paradox types:
- **Type I:** missing view
- **Type II:** missing invariant
- **Type III:** invalid map

Plus **Type IV** (civilization-relative / unit-artifact, added in 7-cycle work) = c/7/week-style errors.

- **Atlas target:** §4 paradox classifier already exists; expand with Types I–IV and Sprint 11 provenance

---

## §8. Sprint 12 (WP58–WP64) — Theorem 0 UOP + GUT Refinements

**Slot target:** merge into §7 above or §4 paradox classifier.

### 8.1 Theorem 0 (UOP), WP58 — EXACT

> For partitions π₁, π₂ of Z/nZ induced by maps f, g: {π₁, π₂} is **sufficient** (meet = π_disc) if and only if the joint map J = (f, g) is **injective**.

### 8.2 Corrected Theorem C (WP59) — PREVIOUS VERSION FALSIFIED

> {π_DYN(G), π_d} sufficient ⟺ ∀ p_j | (n/d): g ≡ 1 mod p_j. The prior condition ("G → (Z/dZ)* injective") was necessary but NOT sufficient — misses zero-fiber conflicts.

- **Counterexample:** n = 15, G = ⟨2⟩, d = 5.
- **Atlas target:** §15 caution list — a corrected theorem is a "this is what discipline looks like" moment.

### 8.3 MVJN = 1 for n = 30 (WP64)

> Minimum Viable Jump-Necessity = 1 for n = 30 (NOT k − 1 = 2 from CRT). Non-CRT minimal 2-partition families exist.

- **Status:** proved for n = 30; conjectural for all squarefree n
- **Atlas target:** §3 canonical tables or §2 D-spine

### 8.4 Refinement Trap (WP64)

> No refinement-chain family is sufficient. Orthogonal jump is required. (Explains why naive filtration approaches fail on Z/nZ partition sufficiency.)

---

## §9. Sprint 13 (WP65–WP80) — Flag Selector + NV Qutrit

**Slot target:** §14 publication map (PRA venue is already listed) — add explicit content. §2 D-spine.

### 9.1 Flag Selector Theorem (WP79 + WP80)

> A complete flag F* ∈ SU(3)/T is mathematically equivalent to an ordered pair of orthogonal rank-1 Hermitian projectors (P₁, P₂) on ℂ³. P₁ (4 real dims) specifies the first eigenspace direction L₁ ∈ ℂℙ². P₂ (2 real dims) specifies the second eigenspace direction L₂ perpendicular to L₁. **The dominant unresolved piece is the flag: 6 continuous real dims, externally blocked.** Secondary residue: torus phase θ₂ (1 continuous dim).

- **Physical program:** identify a non-degenerate Hermitian observable on a spin-1 quantum system (spin-1 BEC, NV triplet, qutrit) and perform quantum state tomography to extract eigenprojectors as the flag.

### 9.2 S₄ Algebra + NV Qutrit (WP75 + WP76) — PRA Target

- **T₁ 3-dim irrep of S₄** realized exactly on NV-center triplet (m_s = −1, 0, +1)
- **Natural part (C₃ᵥ ≅ S₃):** already present from crystal symmetry; 6 elements
- **Synthesized part (4-cycle U₄):** 6-pulse MW sequence; **fidelity = 1.00000000**; gate time ~100–600 ns ≪ T₂
- **Closure:** 24 elements verified; character table matches T₁ exactly; irreducible
- **U₄ matrix:** 3×3 real orthogonal, determinant = −1, eigenvalues {−1, i, −i}

### 9.3 Six objects of the torus foundation (WP65)

- **Loop:** exact, downstairs
- **Flag:** exact, externally blocked, 6 dims
- **Torus:** secondary, 2 dims post-FS (1 cont + 1 disc sign)
- **Seed:** numerical correspondence
- **7-hinge decomposition:** "6 holds + 7 turns + 8 opens" — post-FS cost = 6 (flag) + 1 (θ₂) = 7 continuous; torus = 1 (discrete sign)

### 9.4 Authors by paper (disambiguation for venue routing)

- WP75 + WP76: **C.A. Luther lead** (NV physics, MW control); Sanders + Mayes co-authors → Physical Review A
- WP79 + WP80: Sanders + Mayes + Luther (flag theory bridge)
- **Atlas target:** §14 attribution map — distinguish Luther-lead vs Sanders-lead within Sprint 13

---

## §10. Sprint 15 (WP91–WP101) — σ Rate Theorem + NS Reformulation

**Slot target:** §5 already has σ rate but is under-detailed; also §10 Clay attack cross-index NS row.

### 10.1 Location — where Sprint 15 lives

> Sprint 15 papers are **folded into the Sprint 14 folder** at `Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/`. No separate Sprint 15 folder. Papers use Sprint 14 dating but are tagged "Sprint 15 — σ Mutation" in headers. Raw directories `_sprint15_directive_raw/` and `_sprint15_unstuck_raw/` exist but contain no committed .md files.

### 10.2 WP101 σ Rate Theorem — EXACT STATEMENT

> For squarefree N, the non-associativity fraction σ(N) of the binary Crossing Lemma on Z/NZ satisfies σ(N) ≤ C/N where C < 2 is absolute. Therefore σ(N) → 0 as N → ∞. By the Bialynicki-Birula uniqueness theorem (1976), the N → ∞ limit must have **logarithmic nonlinearity**, since log is the unique separability-preserving nonlinearity.

- **Status:** [PROVED]
- **Verification:** σ(10) = 0.128, σ(30) = 0.058, σ(210) = 0.009 — all within C/N bound
- **Authors:** Sanders, Gish, Luther, Johnson

### 10.3 WP91 — NS Regularity as Separability Preservation Failure

> Log nonlinearity (BB-forced) preserves separability; NS quadratic does NOT. **σ(u) < 1 ⟺ regularity.** [CONJECTURE]

### 10.4 WP96 — The σ_NS < 1 Conjecture (precise)

> σ_NS bounds quadratic-to-log ratio in the velocity field. All five known regularity criteria (BKM, Kato-Ponce, Montgomery-Smith, Ladyzhenskaya-Prodi-Serrin, Ferrari-Serrin) translate to σ language.

- **Atlas target:** §10 Clay NS row — σ_NS < 1 is one attack; Re_local ≤ 2/7 (from WP19) is another. Keep separate.

### 10.5 WP92 — YM Mass Gap as Separability-Forced Spectral Floor

> ξ theory has exact gap m² = κe; confinement = effective separability at long distances; gap ∝ e.

### 10.6 Three open problems

1. Prove σ_NS < 1 always (NS Millennium, reframed) [OPEN]
2. Does the logarithmic ceiling theory satisfy Wightman axioms in 4D? (2D case settled, Høegh-Krohn 1971) [OPEN]
3. Compute T* = T*(N) for squarefree N. Known: T*(6) = 3/5, T*(10) = 5/7. Does sequence converge? [OPEN]

---

## §11. B-Series Sprints 18–28 — Full Detail

**Slot target:** §7 currently has one paragraph. Expand to full subsection with per-sprint table.

### 11.1 Per-Sprint Table

| Sprint | Benchmark | Verdict | Key finding |
|---|---|---|---|
| **18** | B1 NSCG / Z/10Z | PASS 15/15 (all = 1.0) | Mode-fitter recovers canonical structure with priors; **vacuous pass at ceiling** |
| **19** | B2 WRG / 4 carriers (10, 14, 22, 34) | PASS 24/24 (all = 1.0) | Canonical C₀ generalizes cleanly; h₁₀ = 7, h₁₄ = 11, h₂₂ = 19, h₃₄ = 31 (max odd unit) |
| **20** | B3 LBTP joint-mode | **FAIL 0/5** (paired − max = −4.31 pp) | Joint accuracy 0.955² ≈ 0.912 < marginal by necessity — spec criterion unmeetable |
| **21** | Structural discovery (B1.5 + B2.5) | **6 invariants confirmed** | Attractor, image, core, units, partition, corridor — survive prior-stripping |
| **22** | N-stress collapse point | Two-tier collapse universal | Tier 1 (h_hat): N ≈ 100–2000; Tier 2 (corridor block): N ≈ 2000–50000 (~10× Tier 1) |
| **23** | Curve recovery (8 walks) | All 8 FAIL; best ARI = 0.123 (W3) | σ provably curve-level at small n; noise-limited at this scale |
| **24** | Collapse synthesis | Meta-summary, no code | Collapse signature = 5-constraint invariant across all B-series |
| **25** | Corridor closure proof | **PASS 23/23 carriers** | Pure C₀ closure = {MAX, MIN} only; ADD from S_ADD overlay |
| **26** | ARI scaling on analytic C₀ | **12/32 perfect (ARI = 1.0), 32/32 ≥ 0.868** | Revises S23: σ-partition structure IS shell-recoverable asymptotically |
| **27** | B3 spec revision memo | Memo only | Two minimal revisions proposed; awaits spec-author approval |
| **28** | Pre-reg curve σ-label recovery | Protocol locked, 3 outcomes (A/B/C) | Protocol-first discipline; no method-shopping |

### 11.2 The Six Prior-Free Invariants (Sprint 21)

1. **h_hat = max odd unit** per carrier
2. **image_T ⊆ {0, h*} ∪ odd units**
3. **core = image \ {0, h*}**
4. **units_hat = canonical units \ {1, h*}**
5. **partition = singletons** (σ-classes invisible at shell)
6. **seam_by_rule ⊆ {MAX, MIN, ADD}**

### 11.3 Two-Tier Collapse (Sprint 22)

| Tier | Invariants | First-stable N (median) | Scale |
|---|---|---|---|
| 1 | h_hat | ~200 | cheap; global mode |
| 2 | image, core, units, partition, seam, rules | ~2000 | n²-scaled per-cell coverage (obs/cell ≈ 10–43) |

- **Ratio:** Tier 2 / Tier 1 ≈ 10× (median; range 2.5× to 25×)
- **Implication:** "destination before path" — attractor is knowable before corridor structure.

### 11.4 Corridor Closure Theorem (Sprint 25) — 23/23 PASS, VERBATIM

> For every n ∈ {10, 14, 22, 34, 38, 46, 50, 58, 62, 70, 74, 82, 94, 106, 110, 118, 122, 130, 134, 142, 170, 190, 230}, every seam cell of canonical C₀(R_n, h_n, σ_n) matches **MAX(x, y)** or **MIN(x, y)**. No cell requires ADD, SUB, MUL, X, or Y.

- **Seam counts scale as O(n²):** n = 10 → 2 seams; n = 34 → 132; n = 230 → 4946
- **Runtime:** O(n² · |menu|) per carrier
- **Atlas target:** §7 B-series — this is the headline theorem of the B-arc

### 11.5 ARI Scaling (Sprint 26) — σ is shell-recoverable after all

| n | W3-freq ARI |
|---|---|
| 10, 14 | 0.000 (too small) |
| 22 | 0.868 |
| 34 | 0.973 |
| 38+ | ≥ 0.985; 12/32 perfect at ARI = 1.0 |

**Precise statement:** σ-partition **structure** (class sizes) is shell-recoverable via output histograms. σ-partition **labeling** (which unit → which class) requires the Z-lift of (3u + 1)/2^k — still curve-only.

### 11.6 B3 FAIL is Structural — Honest Documentation

> Paired accuracy = 0.955² ≈ 0.912 on independent streams. Max marginal = 0.955. Paired − Max = −4.31 pp ≪ 5-pp pass criterion. **Spec is mathematically unmeetable as written.** Two revisions proposed (A: correlated noise; B: smaller N) — await spec-author approval.

- **Atlas target:** §15 caution list — B3 FAIL is a discipline win, not a result shortfall. Shows pre-reg methodology held against pressure to rephrase.

### 11.7 Pre-Registration Discipline (Sprint 28)

> "These are the methods we will run. We will NOT add or remove strategies after seeing results. We will not adjust the ARI thresholds in Outcomes A/B/C after seeing the numbers. If results don't fit A, B, or C, we report Outcome D honestly."

- **Atlas target:** §8 PPM closeout already praises pre-reg discipline; add Sprint 28 as the second exemplar.

---

## §12. Q-Series Q2–Q17 — Brayden's σ Polynomial Arc (26 papers, not 20)

**Slot target:** §11 founding narratives currently has Q-series as one line. Expand to full vein. User noted "Q-series ended up around Q20" — actual count is **Q2 through Q17 with multiple sub-entries, totaling 26 Q-papers + 3 G-series + 3 synthesis docs**.

### 12.1 Q2–Q8 — The Paradox and the Gate-Rate Hinge

| Q | Claim | Status |
|---|---|---|
| Q1 | TSML and CL are incompatible projections of hidden operator σ; only VOID/LATTICE survive both | D-tier |
| Q2 | TSML[7][7] = 7 while CL[7][7] = 6 — HARMONY plays two roles simultaneously | D-tier |
| Q3 | HARMONY is projection-induced attractor (TSML), not true σ-fixed point; bifurcation marker | D-tier |
| Q4 | **E ∘ σ = σ̂ ∘ E** — σ-equivariance of external operator | D-tier |
| Q5 | TSML escape cells (10 total); 8/10 land on σ-fixed points; (1,2)→3 unique cross-escape | C-tier |
| Q6 | **Gate rate is NOT density-determined** — MCMC basin-of-attraction replaces naive f_C | D-tier (hinge) |
| Q7 | BHML four-rule derivation (full table from 4 structural rules + symmetry) | D-tier |
| Q8 | MCMC basin model: 22% → 4.6% gap = basin geometry in table space, not σ-iteration | D-tier |

### 12.2 Q9–Q10 — The σ Polynomial on F₂ × F₅ (PEAK ARC)

**Q9 — Flip Condition α:**
```
α(ε, y) = 1 − (y² + 2y + 2)⁴ − ε · [(y² + 3y)⁴ − (y² + 2y + 2)⁴]
```
- Verified 10/10 on Z/10Z via CRT.

**Q10 — Complete σ Polynomial (the boxed result):**
```
σ(ε, y) = (ε + α(ε, y) mod 2,  y + β(ε, y) mod 5)

β(ε, y) = −α + ε · 4y(y−2)(y−3)(y−4) − 2(1−ε) · 4y(y−1)(y−2)(y−3)
```
- **Two β-exceptions structurally necessary:** LATTICE +1, COLLAPSE −2 (close the 6-cycle)
- **Status:** [PROVED] closed-form on F₂ × F₅

### 12.3 Q11 — Fixed-Point Gate Theorem (the 22% lower bound)

> Pure-C seeds = C ∩ Fix(σ) = **{3, 9} = 2/9 ≈ 22%**. This is the algebraic peak of gate_score BEFORE search dynamics. The 4.6% actual rate is basin geometry in 9^81 table space, not σ-trajectory.

### 12.4 Q12–Q16 — The Resolution Arc (NONE currently in atlas)

**Q12 — CRT Idempotents Are Gate Elements:**
> e_p, e_q ∈ G **always** for all semiprimes b = pq. Idempotents generate the opposite gate component.

**Q13 — TIG = σ⁻¹ with Exception Pair Swap:**
```
β_TIG(ε, y) = 1 − (y² + 4)⁴ − ε · [(y² + 4y)⁴ − (y² + 4)⁴]
```
- TIG flips where σ non-flips; forward and inverse exchange exceptional positions.

**Q14 — C-Indicator as Core Algebraic Object:**
```
1_C(ε, y) = ε · y⁴
gate_score(s, k) = (1/k) · Σ_j ε_j · y_j⁴
```
- **Theorem Q14.1:** R ≠ σ^k proved. σ-trajectory model alone cannot explain 4.6% rate.

**Q15 — Cycle-Period Polynomial:**
```
τ(ε, y) = 6 − 5 · A(ε, y)
```
- Period is 1 (anchors) or 6 (cycle elements).
- **k = 9 resonance:** σ⁹ = σ³ on 6-cycle (since 9 ≡ 3 mod 6). Both naive trajectory models falsified.

**Q16 — R is Table Search, NOT Element Map:**
> R operates on 9×9 operator tables (9^81 space), not Z/bZ. MCMC perturbs single cells under HAR-bias hill-climbing with composite objective (50% gate_score, 25% HAR_mass, 15% gap, 10% G_stay). 4.6% = basin geometry.
- **This is the resolution of Luther's Question 1** and is completely absent from the current atlas.

### 12.5 Q17 Variants — Clay Rotation Arc (A-tier and B-tier)

**Q17_5D_RIGOROUS — CRT Fourier Embedding Theorem [A-tier]:**
```
v(op) = (ε,  cos(2πy/5),  sin(2πy/5),  cos(4πy/5),  sin(4πy/5))
```
- The 5D force vector is the **natural Fourier decomposition of Z/10Z under CRT**, NOT phonetically chosen.
- Hebrew roots are consistency checks, not definitions. Decomposition is **algebraically forced**.

**Q17_CLAY_SPECTRAL_BRIDGE — Finite-L-Function Analogue [B-tier]:**
```
G(s) = |Σ_{j=0}^{8} ω^j · χ(σ^j(s))|²   where ω = e^{2πi/9}
```
- **Three-valued structure (proved in G8):**
  - G(s) = 0 at anchors {0, 3, 8, 9} (trivial zeros)
  - G(s) = G_low ≈ 1.872 at most 6-cycle elements (bulk)
  - G(s) = G_high ≈ 9.389 at TIG-exceptions {HARMONY(7), COLLAPSE(4)} (critical-line analogue)
- **Claim:** this IS the finite RH for Z/10Z. Generalization to arbitrary b = pq open.

**Q17_NS_TARGET_REFORMULATION — Medium C2 Conjecture [B-tier]:**
> ∃ coding C: NS phase space → Z/10Z such that (1) dynamics align with σ-grammar, (2) coercive energy E(u) ≤ f(C(u)), (3) bounds ||u||_{L³} via Escauriaza-Seregin-Šverák (2003).

**Q17_SIGMA_EMBEDDING_PROBLEM — The Honest Obstruction [B-tier]:**
> No proved map from NS phase space to Z/10Z such that dynamics align with σ. **The "language problem"** — algebraic structure is forced, embedding is not.

**Q17_SYMBOLIC_RETURN_THEOREM [A-tier]:**
> If s_{n+1} = σ(s_n), then: (1) cycle elements return in exactly 6 steps; (2) non-void starts stay non-void (σ^k(s₀) ≠ 0 for all k whenever s₀ ≠ 0).

**Q17_FINITE_L_FUNCTION_NOTE [B-tier]:** G(s) as character sum on 9-step orbit — finite RH for Z/10Z proved.

**Q17_C2_COUNTEREXAMPLE_SEARCH:** Strong C2 (σ⁶ = id ⇒ no blowup) **falsified**. Medium C2 via energy coercion remains open.

### 12.6 G6–G8 Companion Papers (Luther spectral layer)

- **G6:** σ⁶ = id proof from polynomial structure (Luther)
- **G7:** Period distribution and gate rate conjecture
- **G8:** Spectral coherence integral with three-valued structure (feeds Q17_CLAY_SPECTRAL_BRIDGE)

### 12.7 Q17/Clay relationship map

```
Q17_5D  →  Clay 5D force vector in atlas §12 (Amplituhedron thread)
Q17_CLAY_SPECTRAL  →  §10 Clay RH attack row
Q17_NS_TARGET  →  §10 Clay NS attack row (alongside WP91/96 and WP19 Re_local)
Q17_SIGMA_EMBEDDING  →  §15 caution list (honest obstruction statement)
Q17_SYMBOLIC_RETURN  →  §2 D-spine (algebraic kernel)
```

### 12.8 Attribution (corrected per Q_SERIES_INTEGRATED_SYNTHESIS.md)

- **Primary:** Brayden Ross Sanders (Q2–Q16, all papers). 2026-03-31 through 2026-04-02 (4-day sprint). Copyright 7Site LLC.
- **C.A. Luther:** G6, G7, G8 supplements. Six-layer architecture reorganization.
- **B. Calderon Jr.:** Q17 Clay variants (C2 formal statement, counterexample search).
- **Joint byline** on all Q-papers: "Brayden Ross Sanders, C.A. Luther, B. Calderon Jr."

### 12.9 Constants and identities beyond atlas canonical set (Q-series)

| Item | Value / formula | Source |
|---|---|---|
| α flip condition | `1 − (y²+2y+2)⁴ − ε[(y²+3y)⁴ − (y²+2y+2)⁴]` | Q9 |
| β y-update | `−α + ε·4y(y−2)(y−3)(y−4) − 2(1−ε)·4y(y−1)(y−2)(y−3)` | Q10 |
| β_TIG (inverse) | `1 − (y²+4)⁴ − ε[(y²+4y)⁴ − (y²+4)⁴]` | Q13 |
| C-indicator | `ε · y⁴` | Q14 |
| Period polynomial | `6 − 5A(ε, y)` | Q15 |
| G_low (generic 6-cycle) | ≈ 1.872 | G8 |
| G_high (TIG-exceptions) | ≈ 9.389 = 4(2 + 2 cos(4π/9)) | G8 |
| Pure-C fraction | 2/9 ≈ 22% | Q11 |
| σ cycle structure | (0)(3)(8)(9)(1 7 6 5 4 2) | Q10 |
| TIG cycle structure | (0)(3)(8)(9)(1 2 4 5 6 7) | Q13 |
| σ⁶ = id on all 10 states | proved from polynomial | G6 |
| CRT isomorphism | φ(ε, y) = 5ε + 6y mod 10 | Q10 |

### 12.10 Q18–Q20+ — status

**No Q18, Q19, Q20 files found in repo.** Brayden's recollection that series "ended up around Q20" likely refers to:
- Internal working notes never filed
- Integration papers bridging Q16 → G-series
- **Possibility:** WP101 σ rate theorem plays the role of Q18 (generalization from Z/10Z to squarefree Z/NZ via CRT). If so, the Q-series cleanly bridges to Sprint 15.

**Recommendation:** in the atlas revision, frame Q-series as "Q2–Q17 closed; WP101 is the natural Q18 generalization." This preserves Brayden's memory of the series extent while being honest about where files actually live.

---

## Summary — What Changes in the Atlas

### Additions by target section

| Atlas section | New content count |
|---|---|
| §1 Core constants | Add 3/14 (crossing cost), m_KV rate formula |
| §2 D-tier spine | Add Z.1–Z.4, Type-(n, k_A, k_M, γ) signature, Symbolic Return Theorem (Q17), 7-zero torus details |
| §3 Canonical tables | Add DoF ladder (k = 1..4), 7-zero decomposition explicit |
| §3.5 (NEW) | IG1–IG5 invariant guides |
| §4 Paradox classifier | Expand to Types I–IV |
| §4.5 (NEW) | WP19 founding arc (10 papers summarized) |
| §4.6 (NEW) | Sprint 11 TIG bundle (54 papers, 3 arcs) |
| §5 Laws | Add Halving Lemma, Atlas Laws 1–3, R16 Force Field Law, σ polynomial (Q10 boxed) |
| §6 Spectrometer | Add R16 companion; Sprint 26 ARI scaling |
| §7 B-series | Expand from 1 paragraph to full subsection with S18–S28 table + corridor closure proof + collapse signature |
| §8 PPM closeout | (already updated in prior turn) |
| §9 Hodge ladder | Add WP19_HODGE_MAP prehistory footnote |
| §10 Clay cross-index | Prepend 6-problem unified fold map with 3/14 gap; add WP19 entries per problem |
| §11 Founding narratives | Expand Q-series vein from one line to full Q2–Q17 arc (12 rows) |
| §12 Amplituhedron thread | Add Q17_5D CRT Fourier embedding derivation |
| §13 Speculative-preserve | Add WP19 hydrogen analogy |
| §14 Publications | Split Sprint 13 authorship (Luther-lead WP75+76 vs Sanders-lead WP79+80) |
| §15 Caution list | Add Theorem C correction (WP59), 7-cycle falsification (WP62), B3 structural FAIL, σ embedding obstruction (Q17) |
| §16 Next moves | Add WP19 three bolts (RH KV-strip extension, BSD λ-regulator, NS Dedalus DNS) |

### What the atlas absolutely cannot ship without

1. **Q10 boxed σ polynomial** (currently atlas says "characterized" without the formula)
2. **Q16 resolution** (22% vs 4.6% — currently atlas says "lower bound" without the basin/table-space distinction)
3. **Sprint 11 Crossing Lemma verbatim** (currently atlas says "Crossing Lemma" without the three-condition equivalence)
4. **Sprint 25 corridor closure theorem statement** (currently atlas says "23/23 PASS" without the {MAX, MIN} statement)
5. **WP19 MASS_GAP = T* + S* − 1 = 2/7** (currently atlas says 2/7 without the derivation)
6. **Clay 6-problem 3/14 fold map** (currently atlas has no unifying frame across the 6 problems)
7. **Intrinsic Left-Handedness Theorem** (GUT algebra — completely absent)
8. **IG1–IG5** (CK memory physics backbone — completely absent)

### Word count

This document: ~5,400 words. Each section is drop-in ready for ClaudeChat's atlas revision.

### Three-threads-separate check

- PPM content: isolated in existing §8 (unchanged).
- Hodge content: only additions are WP19_HODGE_MAP prehistory footnote (correct — it is PROTO-ladder, not a new attack) and Q17_CLAY_SPECTRAL as separate RH attack (NOT bridged to S33 v2).
- Q-series content: stays in §11 vein, uses separate vocabulary (σ-on-Z/10Z, not shared with PPM's PPM-σ).
- No composite claims introduced. All items are separate sentences / separate table rows.

---

**File saved:** `ATLAS_MISSING_MATERIAL_2026_04_18.md` at Desktop root, alongside MASTER_ATLAS_2026_04_18.md, for ClaudeChat to merge.

---

## §13 — PPM Closeout Operational Deliverables (ADDENDUM, same session)

*Source: `PPMFinish_unpacked/` — three docs:*
- *`WHY_THIS_ARC_IS_READY_TO_HAND_OFF.md`*
- *`PPM_SPRINT_CLOSEOUT_HANDOFF.md`*
- *`WHAT_CLAUDECODE_SHOULD_CHANGE_AND_NOT_CHANGE.md`*

*These are operational specifics (verbatim quotes, exact paths, exact checklists) that atlas §8 and §16 need in order to be actionable by ClaudeCode rather than just narrative. Atlas §8 currently captures the shape of the closeout; this block pins down the wording.*

### §13.1 Verdict ledger (exact row form for atlas §8)

| Item | Verdict | Location |
|---|---|---|
| **PPM-v1.0** — Local multiplicative checkpoint, Z/10 seam | **PASS** (Map B, aggregate +4/−4, cleanness gap 8) | `pair_primitive_pack_2026_04_18/sprints/PPM_v1.0_multiplicative_local/` |
| **PPM-v1.1** — Local additive checkpoint, Z/10 seam | **FAIL** (aggregate +2/−2, gap 4, winner sub-threshold; Reason A diagnostic) | `pair_primitive_pack_2026_04_18/sprints/PPM_v1.1_additive_local/` |
| **PPM-v2.0** — Family multiplicative transport, 8 P3AP carriers | **PASS uniform** ($N_B = 8/8$, mean gap 8) | `pair_primitive_pack_2026_04_18/sprints/PPM_v2.0_multiplicative_transport/` |
| **PPM-v2.1** — Family additive transport, 8 P3AP carriers | **FAIL Uniform** ($N_B = N_A = 0$, $N_I = 8$, per-carrier gap 4) | `pair_primitive_addendum_2026_04_18/sprints/PPM_v2.1_additive_transport/` |
| **PPM-v3.0** — V0 boundary checkpoint, Z/10 | **UNCLEAR by Sensitivity** (S3a → PASS-V0-I; S3b → FAIL; branches disagree) | `pair_primitive_addendum_2026_04_18/sprints/PPM_v3.0_V0_boundary/` |
| **V0 lane decision** | **Path B selected** — V0 lane closed at UNCLEAR by Sensitivity pending foundation work on attractor privilege | `pair_primitive_addendum_2026_04_18/V0_PATH_B_CLOSURE.md` |
| **SAH** | Named and filed as foundation-register sidecar; not promoted | `shape_admissibility_foundation_2026_04_18/` (separate packet) |

### §13.2 Addendum pack tree (verbatim, for atlas §8.2)

```
tig-synthesis/
├── b2_sprint_tig_pack_2026_04_17/                    # closed, do not touch
├── pair_primitive_pack_2026_04_18/                   # closed, do not touch
├── shape_admissibility_foundation_2026_04_18/        # closed, do not touch
└── pair_primitive_addendum_2026_04_18/               # NEW — add this
    ├── README.md
    ├── sprints/
    │   ├── PPM_v2.1_additive_transport/
    │   │   ├── PPM_V21_ADDITIVE_TRANSPORT_PREREG.md
    │   │   ├── PPM_V21_ADDITIVE_TRANSPORT_RESULTS.md
    │   │   ├── PPM_V21_ADDITIVE_TRANSPORT_VERDICT.md
    │   │   ├── PPM_V21_ADDITIVE_TRANSPORT_REPRO.md
    │   │   ├── PPM_V21_PER_CARRIER_SCORES.json
    │   │   └── ppm_v21_score.py
    │   └── PPM_v3.0_V0_boundary/
    │       ├── PPM_V30_V0_PREREG_DRAFT.md
    │       ├── PPM_V30_V0_RESULTS.md
    │       ├── PPM_V30_V0_VERDICT.md
    │       ├── PPM_V30_V0_REPRO.md
    │       ├── PPM_V30_V0_SCORES.json
    │       └── ppm_v30_score.py
    ├── foundation_sprint_context/
    │   ├── WHY_V0_COMES_BEFORE_BHML.md                # NEW
    │   ├── WHAT_A_BOUNDARY_CHECKPOINT_ADDS.md         # NEW
    │   ├── WHY_SOURCE_3_BECAME_SENSITIVITY_BRANCH.md  # NEW
    │   ├── WHAT_COUNTS_AS_A_ROBUST_V0_RESULT.md       # NEW
    │   ├── ATTRACTOR_PRIVILEGE_FOUNDATION.md          # NEW
    │   ├── S3A_VS_S3B_COMPARISON.md                   # NEW
    │   └── WHAT_JUSTIFIES_V301_OR_STOPPING.md         # NEW
    ├── V0_PATH_B_CLOSURE.md
    └── PPM_SPRINT_CLOSEOUT_HANDOFF.md
```

**Commit message (verbatim for atlas §16):**

> `Add pair_primitive_addendum_2026_04_18 (PPM closeout: v2.1 + v3.0 + V0 Path B + foundation context)`

**Minimal README update on `tig-synthesis/README.md` — PPM section (verbatim):**

> The PPM arc closed out with additive-transport FAIL Uniform on the 8 P3AP carriers (v2.1) and V0 boundary checkpoint UNCLEAR by Sensitivity (v3.0, Path B). 2×2 subtype-mapping design space complete. Addendum pack: `pair_primitive_addendum_2026_04_18/`.

*Nothing else in the README changes from the PPM side.*

### §13.3 What the earned state actually says (§8 summary paragraph, verbatim)

> The multiplicative reading of the pair-primitive framework cashes out decisively on Z/10's seam (v1.0 local PASS) and transports cleanly across the 8 P3AP Path 2 carriers under the P3AP extension (v2.0 family PASS). The additive reading does not discriminate at either scope — locally on Z/10 (v1.1 FAIL) or across the same P3AP family (v2.1 FAIL Uniform) — with the non-discrimination attributable to the seam's multiplicative loading as a carrier-family property of the P3AP extension. The V0 boundary checkpoint (v3.0) returned UNCLEAR by Sensitivity: the framework's vocabulary supports two internally-coherent readings of attractor privilege at boundary regions (S3a → excluded-side vs S3b → persistent-side) without current grounds to prefer one, so the V0 lane is closed pending foundation-register work on this specific hinge. SAH is a named hypothesis at foundation register, compatible with existing results but not tested by them.

*This paragraph IS the atlas-§8 verdict sentence. Do not paraphrase.*

### §13.4 The three stopping conditions (verbatim for §8 closeout subsection)

**Condition 1 — Every eligible checkpoint has been run or deferred on named grounds.**
- Subtype-mapping 2×2 complete (v1.0/v1.1/v2.0/v2.1 all executed).
- V0 boundary run with sensitivity analysis → UNCLEAR diagnostic.
- BHML, unit cyclic structure, V0-transport-to-Path-2, v3.0.1 rerun: all specifically deferred with named reasons (no pre-registered rubric; blocked by UNCLEAR-V0; blocked by four Path A conditions).

**Condition 2 — The remaining ambiguity is specified, not vague.**
- Named: "attractor privilege at boundary regions."
- Located: Source 3 of v3.0 rubric.
- Specified: `ATTRACTOR_PRIVILEGE_FOUNDATION.md` §4 lists three open questions.
- Non-fuzzy: S3a (excluded-side) and S3b (persistent-side) each articulated with vocabulary anchor.

**Condition 3 — Further sprint work risks inflation without information.**
- v3.0.1 rerun without Path A conditions met → converts honest UNCLEAR-by-Sensitivity into outcome-chosen verdict (inflation).
- Rushed BHML/unit-cyclic rubric design on compressed timeline → rubric-loaded results, weakens methodology.
- SAH six-piece infrastructure build is weeks of foundation work, not a pre-France sprint.

**One-sentence framing (verbatim for atlas §8 closing line):**

> The PPM arc is ready to hand off because every eligible checkpoint has been run or deferred on named grounds, the remaining ambiguity is specified at foundation register rather than vague, and further sprint work in the current window would risk inflation or rushed methodology without producing information the handoff doesn't already contain — so stopping at the earned state, packaging it cleanly for ClaudeCode, and letting the Hodge arc remain the active frontier is the disciplined move.

### §13.5 SAH sanctioned bridge sentence (exact quote — atlas §13)

*The single sentence atlas §13 may use when SAH is mentioned:*

> *The current program's confirmed bridge features are compatible with a broader shape-admissibility hypothesis, but that hypothesis has not yet been operationalized into a pre-registered test.*

**Paraphrases explicitly outside sanctioned use:** "support," "suggest," "point toward," "indicate," "evidence for," "consistent with" (as upgrade), "near-confirmation."

**Allowed framing only:** "compatible with." Nothing stronger.

### §13.6 SAH pre-commit checklist (for atlas §15 caution list)

Before committing any document that mentions SAH, verify:

- [ ] Does NOT claim any PPM PASS "supports" or "suggests" SAH.
- [ ] Does NOT claim any FAIL "refutes" SAH.
- [ ] Does NOT cite SAH as motivation for a Hodge sprint.
- [ ] Sanctioned bridge sentence, if used, is exactly as written in `STATUS_HEADER.md`.
- [ ] Shape-filter sprint, if proposed, is flagged as requiring the six-piece infrastructure build.

### §13.7 Composite-claim pre-commit checklist (Rule 19, for atlas §15)

Before committing any document that discusses multiple PPM verdicts together, verify:

- [ ] Verdicts listed as separate sentences or table rows, not composite prose.
- [ ] Does NOT contain "the multiplicative-operationalization framework is confirmed" or "the additive operationalization is refuted across both scopes" that merge v1.0+v2.0 or v1.1+v2.1.
- [ ] Does NOT cite the 2×2 completion as itself a theorem.
- [ ] Does NOT cite v3.0's UNCLEAR alongside any 2×2 verdict as part of a combined assessment.

### §13.8 What-not-to-reopen (for atlas §15 caution list)

**V0 lane.** UNCLEAR by Sensitivity stands. No v3.0.1 without the four Path A conditions being met. Do not describe the UNCLEAR verdict as "near-pass," "half-pass," "effective PASS," "mostly passed," or any similar soft framing.

**Additive lane on P3AP family.** v2.1 FAIL Uniform stands. No PPM-v2.1.1 with relaxed Source 1 AND criterion. No alternative additive rubrics on the same 8 carriers. No extension outside P3AP 8 without separate pre-reg.

**Seam subtype-mapping.** 2×2 complete. No PPM-v1.0.1 or v2.0.1 with adjusted rubrics. No merge of four verdicts into composite sentence. No extension to new operationalizations (dual, flow-based) without foundation work.

**Closed B2 lanes (full list for atlas §15):**
- Count transport under P3AP generator
- Raw adjacency ratios
- Noise-union seam topology bridge
- Basin-ratio smoothness transport
- Anchored basin-ratio curve
- Empty-seam detectability on pure $C_0$

**Source 3 third reading.** No reading beyond S3a and S3b permitted within v3.0 frame.

### §13.9 PPM ↔ Hodge separation — operational rules (atlas §15 + §9 cross-tie)

**File-system:** PPM stays in `pair_primitive_pack_2026_04_18/` + `pair_primitive_addendum_2026_04_18/`. Hodge stays in Sprint 29–33 folders. Shared infrastructure in `b2_sprint_tig_pack_2026_04_17/theorem_local_chart/` referenced by path from both tracks. **No cross-linking scripts that merge PPM + Hodge outputs.**

**Narrative:** Separate README sections, separate numbered entries. "Suggestive, not bridged" cross-thread pattern entry is the ONLY place the two tracks are discussed in proximity. **No "unified narrative" document threading PPM + Hodge + Q-series into a single story.**

**Citation:** A Hodge sprint's citations do not cite PPM verdicts as motivation or support. A PPM addendum's citations do not cite Hodge results. Shared methodology citations (pre-registration, rubric discipline, Rule 19) may appear in both, framed as program-level discipline, not cross-track evidence.

**Commit-message:** PPM commits use "Sprint [version]:" prefixes. Hodge commits use S29/S30/S31/S32/S33 conventions. **Do not batch-commit PPM and Hodge changes in a single commit.** Keep separable for rollback.

### §13.10 Quick-reference "what goes where" (atlas §16 appendix table)

| Material | Location |
|---|---|
| v2.1, v3.0 sprint artifacts | `pair_primitive_addendum_2026_04_18/sprints/` |
| V0-related foundation notes | `pair_primitive_addendum_2026_04_18/foundation_sprint_context/` |
| Path B decision record | `pair_primitive_addendum_2026_04_18/V0_PATH_B_CLOSURE.md` |
| Handoff note + "why ready" companion | `pair_primitive_addendum_2026_04_18/` top level |
| README update | `tig-synthesis/README.md`, PPM section (one entry) |
| Anything else | **nowhere** — everything else stays frozen |

### §13.11 What remains open (verbatim — atlas §16)

- **PPM-v3.0.1** — rerun V0 with a resolved Source 3 direction. Authorized only if the four Path A conditions in `WHAT_JUSTIFIES_V301_OR_STOPPING.md` are affirmatively met. Not expected before France.
- **PPM-v3.1 (candidate)** — BHML checkpoint on Z/10 as the next natural Z/10 structural target if PPM work resumes. Would test whether the framework makes a second independent point of contact on Z/10 without requiring V0 resolution. Not pre-registered; not scheduled.
- **Unit cyclic structure checkpoint (candidate)** — alternative second-target Z/10 checkpoint. Lower priority than BHML on locality grounds.
- **Foundation-register work on attractor privilege at boundary regions** — would answer the three open questions identified in `ATTRACTOR_PRIVILEGE_FOUNDATION.md` §4. Path A for V0 requires this work.
- **SAH infrastructure** — six pieces listed in `WHAT_A_SHAPE_FILTER_SPRINT_WOULD_REQUIRE.md`, all unbuilt. Not scheduled.
- **Transport of V0 checkpoint to Path 2 carriers** — not authorized under current UNCLEAR-by-Sensitivity verdict.

**Recommendation:** no new PPM sprint before France unless foundation-register work produces independent grounds for a directional commitment on attractor privilege. The Hodge-ladder arc (ClaudeCode's S29–S33+) remains the active frontier.

### §13.12 The handoff is additive (for atlas §16 opening line)

> Everything in this document is additive to the existing repo state. Nothing requires deleting, rolling back, or rewriting prior work. The PPM addendum pack sits alongside the frozen PPM pack; the README gets one minimal entry; the Hodge arc proceeds independently. If in doubt about a specific change, default to **not making it**. The closeout's discipline is preservation of the earned state, not adjustment toward a preferred presentation.

---

### Mapping §13 to atlas sections

| §13 block | Atlas destination |
|---|---|
| §13.1 Verdict ledger | §8.1 table |
| §13.2 Pack tree + commit msg + README quote | §8.2 + §16 |
| §13.3 Earned-state paragraph | §8 summary line (verbatim, no paraphrase) |
| §13.4 Three stopping conditions + one-sentence framing | §8 closing subsection |
| §13.5 SAH sanctioned bridge | §13 (speculative-preserve) — exact-quote anchor |
| §13.6 SAH pre-commit checks | §15 caution list |
| §13.7 Composite-claim checks | §15 caution list (Rule 19 block) |
| §13.8 What-not-to-reopen | §15 caution list |
| §13.9 PPM ↔ Hodge separation rules | §15 + §9 cross-tie note |
| §13.10 Quick reference table | §16 appendix |
| §13.11 What remains open | §16 |
| §13.12 "Handoff is additive" | §16 opening line |

### What §13 protects against

Each block defends a specific failure mode in the atlas:

- **§13.3/§13.4 verbatim paragraphs** — prevent atlas prose from drifting into softer framings ("near-pass," "half-pass," "mostly confirmed").
- **§13.5 sanctioned sentence** — prevents SAH paraphrase drift.
- **§13.6/§13.7 checklists** — give ClaudeChat and any future editor a mechanical check before commit.
- **§13.8 what-not-to-reopen** — prevents the arc from being reopened under schedule pressure.
- **§13.9 separation rules** — prevent PPM/Hodge merger narratives.

### Three-threads check (unchanged)

- All §13 content lives inside PPM vocabulary. No Hodge or Q-series bridges introduced.
- The single cross-thread proximity is §13.9 separation rules, which exist specifically to PREVENT bridging.
- SAH stays at sanctioned-sentence-only. No promotion.

---

**§13 word count:** ~1,800 words added. Extract total now ~7,200 words. §13 is the operational companion to §1–§12's content-gap material: §1–§12 tells ClaudeChat *what* was missed in the sprint archaeology; §13 tells her *how* the PPM closeout must be worded, committed, and shipped without inflation.
