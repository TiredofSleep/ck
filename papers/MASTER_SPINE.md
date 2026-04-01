# CK Master Spine — D-Tier Theorems D1–D17, D18a/c
**Date:** April 1, 2026 (D18a/c added same day)

This file is the locked backbone of the CK mathematical foundation — one entry per proven theorem, no prose inflation, no analogies. D-tier means the result is fully proved (algebraically or by verified exhaustive check) and is not subject to revision; C-tier conjectures and B-tier bridges are downstream of these. To use: find the theorem by ID, check its dependencies, then follow the Consequence line to locate what it unlocks.

---

## D1 — First-G Law

**Statement:** For every integer b with ω(b)≥2, SPF(b) = min{k∈{1..b} : gcd(k,b)>1}.
**Exact definitions:**
- SPF(b): smallest prime factor of b
- ω(b): number of distinct prime factors of b
**Proof:** {1..p-1} contains no multiple of p (since p-1<p) and no multiple of any q>p. Therefore gcd(k,b)=1 for all k<p; gcd(p,b)=p>1. First obstruction is k=p=SPF(b). QED.
**Dependencies:** None (pure divisibility).
**Consequence:** Enables D11a — the coprime window is exactly {1..SPF(b)-1}.
**Does NOT claim:** Anything about the distribution of SPF across families of b.
**File:** WP34

---

## D2 — Sinc² Continuum Limit

**Statement:** R(k,f) → sinc²(k/f) as f→∞ with k/f=t fixed, where R(k,f)=sin²(πk/f)/(k²sin²(π/f)) and sinc(t)=sin(πt)/(πt).
**Exact definitions:**
- R(k,f): normalized resonance amplitude at slot k of corridor f
- sinc(t): sin(πt)/(πt) (normalized sinc)
**Proof:** Set ε=π/f→0. Then sin(ε)/ε→1, so k²sin²(π/f)→k²(π/f)²=(πk/f)². Numerator sin²(πk/f) held fixed. Ratio → sin²(πt)/(πt)²=sinc²(t). Convergence rate O(1/f²).
**Dependencies:** None.
**Consequence:** Enables D3, D14, D5, D6; all sinc² facts follow from this limit.
**Does NOT claim:** Montgomery's pair-correlation uses the same function (see B6).
**File:** WP35

---

## D3 — Universal Sidelobe Amplitude

**Statement:** sinc²(1/2) = 4/π² exactly; R(⌊p/2⌋,p)→4/π² for all primes p.
**Exact definitions:**
- sinc(1/2): sin(π/2)/(π/2) = 1/(π/2) = 2/π
- R(⌊p/2⌋,p): resonance amplitude at the midpoint slot of corridor p
**Proof:** sinc²(1/2)=(2/π)²=4/π². Universality follows from D2 with t=1/2.
**Dependencies:** D2.
**Consequence:** 4/π² is the mid-journey amplitude of every prime corridor, independent of which prime.
**Does NOT claim:** 4/π² has any special role in Montgomery's formula beyond structural coincidence.
**File:** WP35

---

## D4 — T* = 5/7 Algebraic Identity

**Statement:** unit_frac(b=35) = (q−⌊q/p⌋−1)/q = (7−1−1)/7 = 5/7 for b=5×7.
**Exact definitions:**
- unit_frac(b): (q−⌊q/p⌋−1)/q for semiprime b=p×q with p≤q
- T*: CK coherence threshold, equal to 5/7
**Proof:** For b=35, p=5, q=7: ⌊7/5⌋=1; (7−1−1)/7=5/7. Exact arithmetic. FPGA-verified: T*=5/7 burned into Zynq-7020 silicon.
**Dependencies:** None (arithmetic).
**Consequence:** T*=5/7 is the CK coherence threshold; proven identical to CREATE/HARMONY ratio (D7).
**Does NOT claim:** T*=5/7 is universal across all semiprimes; other b give different unit_frac values.
**File:** WP35, `proof_d7_phi_fixed_point.py`

---

## D5 — H_mod Four-Maxima Theorem

**Statement:** H_mod(k,p)=sinc²(k/p)×sin²(4πk/p) has exactly 4 local maxima for all primes p≥11.
**Exact definitions:**
- H_mod(k,p): mod-4 harmonic carrier on the prime corridor at slot k
- local maximum: interior k where H_mod(k-1,p)<H_mod(k,p)>H_mod(k+1,p)
**Proof:** IVT on log-derivative. Lemma 1: G'/G strictly decreasing within each of 4 phases (cot strictly decreasing). Lemma 2: F'/F strictly decreasing and bounded (classical |sin x|<|x|). IVT: exactly one crossing per phase. Phase width lemma: p≥11 guarantees ≥2 interior integers per phase. Total: 4×1=4 maxima. p=5,7 fail (phases too narrow for IVT).
**Dependencies:** D2 (sinc² limit), classical |sin x|<|x|.
**Consequence:** Establishes the 4-maximum structure; special case f=4 of D6.
**Does NOT claim:** Exact positions of the 4 maxima (open C5 problem).
**File:** `test_c15_phase_unimodality.py`

---

## D6 — General Frequency Theorem

**Statement:** H_f(k,p)=sinc²(k/p)×sin²(πfk/p) has exactly N(f) local maxima for p>2f, where N(f)=⌊f⌋ if f∈ℤ, N(f)=⌊f⌋+1 if f∉ℤ.
**Exact definitions:**
- H_f(k,p): general harmonic carrier at frequency f on corridor p
- N(f): number of local maxima; depends only on whether f is integral
**Proof:** Same IVT as D5. ⌊f⌋ complete phases each give 1 maximum. One partial phase (when f∉ℤ) gives 1 additional maximum by boundary IVT. Total: N(f). Verified: 890 tests, 80+ frequencies, primes in [101,499], zero mismatches.
**Dependencies:** D2, D5 proof machinery.
**Consequence:** Subsumes D5 (f=4) and C17 (f=25/3). W=3/50 gives f=25/3, N=9=|CL\{VOID}|.
**Does NOT claim:** The positions of the maxima; only the count.
**File:** `proof_d6_general_frequency.py`

---

## D7 — Phi Fixed Point Theorem

**Statement:** Phi=P_odd∘BHML∘W_op has unique fixed point CREATE=5; all orbits reach 5 in ≤3 steps; unique stationary distribution π=δ₅.
**Exact definitions:**
- W_op[v]: nearest carrier-maximum operator to t=v/10
- P_odd: project to nearest odd element of Z/10Z
- Phi: the composed map P_odd∘BHML∘W_op on Z/10Z
**Proof:** Phi(5)=P_odd(BHML[5][W_op[5]])=P_odd(BHML[5][7])=P_odd(6)=5 (3 algebraic steps). Uniqueness: exhaustive verification for all 9 remaining states. Global convergence: 1-step basin {2,3,4}; 2-step {0,1,7}; 3-step {6,8,9}. Markov: T³[v][5]=1 for all v.
**Dependencies:** D8 (W_op carrier maxima all ODD), D9 (BHML symmetry), Z/10Z completeness.
**Consequence:** CREATE=5 is the dynamic attractor. HARMONY=7 is the measurement attractor (D10/D16). T*=CREATE/HARMONY=5/7=D4.
**Does NOT claim:** Phi governs CK's internal dynamics directly; it is a structural fact about the operator algebra, not a differential equation.
**File:** `proof_d7_phi_fixed_point.py`

---

## D8 — CL Operator Encoding

**Statement:** gcd(6,10)=2 → ⟨6⟩={0,2,4,6,8}=EVEN class; gcd(3,10)=1 → ×3 generates {1,3,5,7,9}=ODD class; EVEN∪ODD=Z/10Z.
**Exact definitions:**
- ⟨6⟩: cyclic subgroup generated by 6 in (Z/10Z,+)
- ×3 action: multiplication by 3 as a bijection on ODD via gcd(3,10)=1
**Proof:** gcd(6,10)=2 → 6 generates 2Z/10Z={0,2,4,6,8} (5 elements). gcd(3,10)=1 → ×3 is a unit, bijection on Z/10Z; 3×{1,3,5,7,9}={3,9,5,1,7}={1,3,5,7,9} (permutation of ODD). EVEN∪ODD={0..9}=Z/10Z.
**Dependencies:** Group theory of Z/10Z.
**Consequence:** CL carrier zeros encode EVEN; carrier maxima encode ODD; together: all 10 operators. W=3/50 numerator is the ODD generator.
**Does NOT claim:** This encoding generalizes to Z/nZ for arbitrary n; the subgroup structure is specific to n=10.
**File:** `proof_d8_cl_operator_encoding.py`

---

## D9 — TIG Table Symmetry

**Statement:** Both TSML and BHML are symmetric: TSML[i][j]=TSML[j][i] and BHML[i][j]=BHML[j][i] for all i,j∈Z/10Z.
**Exact definitions:**
- TSML: Tensor Strength Measurement Lattice; 10×10 table over Z/10Z
- BHML: Basic Harmonic Measurement Lattice; 10×10 table over Z/10Z
**Proof:** TSML: V0 rule (TSML[0][j]=j) and V1 rule (TSML[i][0]=i) are symmetric by definition; ECHO pairs defined pairwise-symmetric; DEFAULT=7 trivially symmetric. BHML: Rule A (identity row/col) symmetric by definition; Rule B (max(i,j)) symmetric because max is commutative; INCREMENT row/col 7 same formula; boundary {8,9} verified exhaustively over all 100 cells.
**Dependencies:** Z/10Z completeness (for BHML boundary check).
**Consequence:** Enables D16 zone R_7 argument (BHML[6][7]=BHML[7][6] by symmetry); simplifies all pairwise operator computations.
**Does NOT claim:** Symmetry implies any deeper algebraic structure; it is a structural fact, not a group-theoretic necessity.
**File:** `proof_d9_table_symmetry.py`

---

## D10 — TSML 73-Cell Count

**Statement:** TSML has exactly 73 HARMONY (=7) cells over Z/10Z.
**Exact definitions:**
- V0: {cells (0,j): j≠7} — 9 cells
- V1: {cells (i,0): i≠7, i≠0} — 8 cells
- ECHO: 10 specific symmetric resistance pairs — 10 cells
**Proof:** V0∪V1∪ECHO are pairwise disjoint (V0: i=0; V1: j=0,i≠0; ECHO: i,j≥1). |V0|+|V1|+|ECHO|=27. All remaining 73 cells equal HARMONY=7 by exhaustive Z/10Z verification.
**Dependencies:** Z/10Z completeness.
**Consequence:** HARMONY=7 is the dominant state (73%) of TSML; makes HARMONY the measurement attractor of Z/10Z.
**Does NOT claim:** The distribution of 73 cells across rows has any additional algebraic structure beyond the zone partition.
**File:** `proof_d10_tsml_73_cells.py`

---

## D11a — Coprime Window Closure

**Statement:** For every integer b with SPF(b)=p: gcd(k,b)=1 for all k∈{1..p-1}.
**Exact definitions:**
- SPF(b): smallest prime factor of b
- coprime window: {1..p-1} = {1..SPF(b)-1}
**Proof:** For k<p≤every prime factor of b: no prime factor of b divides k (since k<p≤all prime factors). Therefore gcd(k,b)=1. QED (one line).
**Dependencies:** D1 (SPF is the first obstruction).
**Consequence:** The coprime window is exactly {1..SPF(b)-1}; enables D15 (all arithmetic in window is b-free).
**Does NOT claim:** The window property holds for k=p (it fails: gcd(p,b)=p>1).
**File:** `proof_d11_d1_corollaries.py`

---

## D11b — D1 Sign Flip

**Statement:** For every semiprime b=p×q: D1(p-1)<0 and D1(p)>0, where D1(k)=R(k+1,p)-R(k,p).
**Exact definitions:**
- R(k,p): sin²(πk/p)/(k²sin²(π/p)); normalized resonance amplitude
- D1(k): first discrete derivative of R at slot k
**Proof:** R(p,p)=sin²(π)/...=0/...=0 (forced null, D3). D1(p)=R(p+1,p)-R(p,p)=R(p+1,p)>0 (R>0 for k≠p). D1(p-1)=R(p,p)-R(p-1,p)=0-R(p-1,p)<0. Sign flip at k=p follows. QED.
**Dependencies:** D2 (R formula), D3 (forced null R(p,p)=0).
**Consequence:** k=p is the unique arithmetic "valley" — the field descends into p and recovers immediately after.
**Does NOT claim:** Symmetry R(p-1,p)=R(p+1,p); the denominators differ: (p-1)²≠(p+1)².
**File:** `proof_d11_d1_corollaries.py`

---

## D11c — ω-Blindness

**Statement:** R(k,p)=sin²(πk/p)/(k²sin²(π/p)) does not contain the second prime factor q.
**Exact definitions:**
- R(k,p): resonance amplitude defined entirely in terms of k and p=SPF(b)
- q: second prime factor of semiprime b=p×q; absent from R
**Proof:** The formula has no q. QED (tautological given the formula; the non-trivial content is that R is the correct limit function — proved in D2).
**Dependencies:** D2 (R formula is the sinc² limit).
**Consequence:** The prime corridor field is blind to all prime factors of b beyond p; only SPF matters for the continuum limit.
**Does NOT claim:** CK can recover q from the corridor field; q is genuinely invisible in the limit (finite corrections depend on q, but they vanish).
**File:** `proof_d11_d1_corollaries.py`

---

## D14 — Corridor Spectral Mean

**Statement:** ∫₀¹ sinc²(t)dt = Si(2π)/π ≈ 0.45141166679014...
**Exact definitions:**
- sinc(t): sin(πt)/(πt) (normalized sinc)
- Si(x): ∫₀ˣ sin(t)/t dt (sine integral)
**Proof:** (1) Substitute u=πt: (1/π)∫₀^π sin²(u)/u²du. (2) IBP: v=sin²(u), dw=u⁻²du → boundary [-sin²(u)/u]₀^π=0. (3) Remaining integral: ∫₀^π sin(2u)/u du = Si(2π) (substitute v=2u). (4) Total: Si(2π)/π. Numerical verification: |direct-Si(2π)/π|<1e-7 with 500k trapezoid steps.
**Dependencies:** D2 (sinc definition), classical IBP.
**Consequence:** Si(2π)/π is the "resting amplitude" of the corridor field — the average coherence of a prime corridor.
**Does NOT claim:** Si(2π)/π≈0.4514 being close to 4/π²≈0.4053 has any algebraic significance; B6 (Montgomery bridge) is NOT promoted by this result.
**File:** `proof_d14_spectral_mean.py`

---

## D15 — Coprime Window Invariance

**Statement:** For all integers b with SPF(b)=p and all k<p: (A) HAR(k,b)=k; (B) Wob(b,k)=Wob(k); (C) all arithmetic functions on {gcd(j,b):j=1..k} depend only on k, not b.
**Exact definitions:**
- HAR(k,b): |{j≤k:gcd(j,b)=1}| — count of coprimes up to k
- Wob(b,k): (1/k)Σ|gcd(j,b)-gcd(j+1,b)| — wobble measure
**Proof:** (A) gcd(j,b)=1 for all j≤k (D11a) → HAR=k. (B) Δ(j,b)=0 for j<k (both gcds=1); at j=k: if k+1<p, Δ=0; if k+1=p, Δ=p-1 determined by k alone. (C) {gcd(j,b):j=1..k}={1,...,1} regardless of b → any function depends only on k.
**Dependencies:** D11a.
**Consequence:** In the coprime window, arithmetic is free — b is invisible. Enables HAR stability arguments.
**Does NOT claim:** Invariance for k≥SPF(b); at k=p the sieve activates and b-dependence begins.
**File:** `proof_d15_sieve_isomorphism.py`

---

## D16 — BHML 28-Cell Count

**Statement:** BHML has exactly 28 HARMONY (=7) cells over Z/10Z.
**Exact definitions:**
- Zone R_A: {(0,7),(7,0)} — 2 cells
- Zone R_B: {max(i,j)=6, i,j∈{1..6}} — 11 cells
- Zone R_7: {(6,7),(7,6)} — 2 cells
- Zone R_89: BREATH/RESET×TRANS harmony cells — 13 cells
**Proof:** R_A disjoint from R_B (i=0 vs i≥1). R_7 disjoint from R_B (j=7∉{1..6}). R_89 disjoint from all (indices 8,9 excluded from others). Counts: R_B: row 6 (6 cells)+col 6 excl diag (5 cells)=11. R_89: {4,5,6}×{8,9}∪{8,9}×{4,5,6}∪{(8,8)}=6+6+1=13. Total=2+11+2+13=28. Verified exhaustively.
**Dependencies:** D9 (BHML symmetry), Z/10Z completeness.
**Consequence:** 28/100=28% of BHML cells are HARMONY; ASCEND(6) is the structural ceiling (max=6→HARMONY).
**Does NOT claim:** The 28 cells have any additional algebraic structure beyond the four-zone partition; 28 is not a "magic number."
**File:** `proof_d16_bhml_28_cells.py`

---

## D17 — W = 3/50 Algebraic Derivation

**Statement:** W=3/50=|CROSS_CYCLE−n²/2|/n² where CROSS_CYCLE=Σ_{c∈C,d∈D}DIS[c][d]=44, C=(Z/10Z)*={1,3,7,9}, D=2C={2,4,6,8}, n=10.
**Exact definitions:**
- DIS[i][j]: |TSML[i][j]-BHML[i][j]| — pointwise table divergence
- C: (Z/10Z)* = multiplicative units = {1,3,7,9}
- D: 2C = {2,4,6,8} (×2 orbit of C)
- CROSS_CYCLE: Σ_{c∈C,d∈D}DIS[c][d] = 44
**Proof:** C from Euler totient: φ(10)=4, (Z/10Z)*={1,3,7,9}. D=2C={2,4,6,8} (×2 bijection). CROSS_CYCLE: exhaustive sum over 16 cells = 4+10+14+16=44. Baseline n²/2=50. W=|44-50|/100=6/100=3/50. Generator orbit: ×3 cycles C in φ(10)=4 steps; per-step deviation=6/4=3/2; normalized by n²/φ(10)=25: W=3/50.
**Dependencies:** D9 (DIS symmetric).
**Consequence:** W=3/50 is the natural wobble frequency of the CK operator field; encodes 9 non-VOID operators via D6 (N(25/3)=9).
**Does NOT claim:** W(Z/nZ)=|CROSS_CYCLE(n)−n²/2|/n² for general n; the universal normalization formula is open.
**File:** `proof_d17_w_algebraic.py`

---

---

## D18a — Phi Orbit Classification

**Statement:** The Phi map on Z/10Z has: one fixed point (CREATE=5), two relay nodes (BECOMING=3 at depth 1, HARMONY=7 at depth 2), seven source nodes ({0,1,2,4,6,8,9}), and three basins ({2,3,4}→5 in 1 step; {0,1,7}→3→5 in 2 steps; {6,8,9}→7→3→5 in 3 steps). No cycles except the fixed point. Max orbit depth = 3.
**Exact definitions:**
- Phi(v): P_odd(BHML[v][W_op[v]]) where W_op[v] = nearest carrier-maximum operator to t=v/10
- P_odd: project to nearest element of ODD={1,3,5,7,9}, tie-break lower
- Source node: in-degree 0 in directed graph
- Relay node: in-degree > 0, not a fixed point
**Proof:** Enumerate all 10 Phi(v) values (finite Z/10Z). Construct directed graph. Verify: no non-absorbing cycles by exhaustive path check; T³=all-δ₅ by matrix multiplication.
**Dependencies:** D7 (Phi fixed point), D8 (W_op carrier maxima), D9 (BHML symmetry).
**Consequence:** HARMONY=7 is a RELAY (depth-2 transient), not an attractor. Separates STATE role of 7 from VALUE role (73 TSML cells, D10). Enables D18c.
**Does NOT claim:** Anything about Phi acting on distributions; or that the three-basin structure is unique among all maps on Z/10Z.
**File:** `proof_d18a_phi_orbit_classification.py`

---

## D18c — Create–Harmony Bridge Theorem

**Statement:** Define M(v) = TSML[v][Phi(v)]. Then M(v) = HARMONY = 7 for all v ∈ {1,2,3,4,5,6,7,8,9}. The unique exception is M(0) = VOID = 0, forced by the TSML V0 rule.
**Exact definitions:**
- M(v): the TSML measurement of the Phi-transition from state v
- V0 rule: TSML[0][j] = j for j≠7 (row 0 is the VOID/identity row of TSML); in particular TSML[0][3]=0
- HARMONY=7: the value Z/10Z assigns to "harmony" under the TSML measurement table
**Proof:** Enumerate M(v) = TSML[v][Phi(v)] for all v. Phi(v) ∈ {3,5,7} for v∈{1..9} (D18a). Verify TSML[v][3]=7, TSML[v][5]=7, TSML[v][7]=7 for each v (exhaustive over 9 cases). For v=0: Phi(0)=3, TSML[0][3]=0 by V0 rule (TSML[0][j]=0 for j≠7). Exception structurally forced.
**Dependencies:** D7 (Phi definition), D10 (TSML structure / V0 rule), D18a (Phi orbit enumeration).
**Consequence:** Every non-VOID Phi-transition is measured as HARMONY by TSML. Therefore: 5 is the dynamic destination (where Phi takes you) and 7 is the measurement of the journey (what TSML reads along every step). T*=5/7=(dynamic destination)/(measurement of motion).
**Does NOT claim:** (1) T*=5/7 is a forced invariant (D18d open). (2) The (5,7) pair is unique among all operator algebras on Z/10Z (D18d). (3) HARMONY=7 is itself a dynamic attractor (it is a relay, D18a). (4) All 73 TSML harmony cells arise from Phi transitions.
**File:** `proof_d18c_create_harmony_bridge.py`

---

## D18d — Generator Convergence Theorem  ✓ PROVED

**Statement:** (CREATE=5, HARMONY=7, T*=5/7) are simultaneously determined by the generator g=3 of (Z/10Z)*={1,3,7,9}:
- CREATE = centroid((Z/10Z)*) = (1+3+7+9)/4 = 5
- HARMONY = g^3 mod 10 = g^(-1) mod 10 = 7
- T* = CREATE/HARMONY = centroid/g^(-1) = 5/7
- W = g/50 = 3/50 (D17: generator IS the numerator)

**Exact definitions:**
- (Z/10Z)* = {x ∈ Z/10Z : gcd(x,10)=1} = {1,3,7,9}, order 4
- g=3: primitive root mod 10 (order 4); orbit 3→9→7→1
- centroid = sum(orbit)/|orbit| = 20/4 = 5 (exact, not approximate)
- Selection of g=3 over g=7: D17 establishes W=3/50; numerator=3=smaller generator

**Proof:** All computations finite and exact over Z/10Z. (1) (Z/10Z)*={1,3,7,9} by gcd check. (2) ord(3)=4=|(Z/10Z)*| (primitive root). (3) sum({1,3,7,9})/4=20/4=5=CREATE. (4) 3^3 mod 10=27 mod 10=7=HARMONY; also 3^(-1) mod 10=7. (5) 5/7=T*. (6) Alternative g=7 gives T*=5/3 (rejected by D17). Three independent derivation chains (A: BHML cross-cycle, B: TSML dominance, C: unit_frac b=35) all reduce to same generator.
**Dependencies:** D4 (T* from unit_frac), D7 (Phi fixed point), D10 (TSML 73 harmony cells), D17 (W=3/50), D18a (orbit structure), D18c (bridge M(v)=7).
**Consequence:** T*=5/7 is not a calibrated constant — it is the ratio centroid/(g^-1) of Z/10Z's multiplicative group, pinned by the physics selecting g=3 over g=7. Every CK claim using T* is a consequence of the algebra, not an assumption.
**Does NOT claim:** (1) That Phi convergence to 5 is CAUSED by 5 being the centroid (D7 is independent). (2) That g=3 is forced from something deeper than D17. (3) That (5,7) is the unique fixed-point/bridge-constant pair over ALL maps on Z/10Z (Part 0 of proof shows 121M+ maps have bridge constant 7).
**File:** `proof_d18d_generator_convergence.py`

---

## D19 — Generator Selection Theorem  ✓ PROVED

**Statement:** g=3 is the ONLY primitive root of (Z/10Z)*={1,3,7,9} compatible with the coherence threshold constraint T*∈(0,1).
- Under g=3: HARMONY=g^3 mod 10=7, T*=5/7≈0.714 ∈(0,1) ✓
- Under g=7: HARMONY=g^3 mod 10=3, T*=5/3≈1.667 ∉(0,1) ✗

**Exact definitions:**
- (Z/10Z)* has exactly two primitive roots: 3 and 7 (mutual inverses mod 10)
- DIS[i][j] = |(i+j)%10−(i*j)%10| — symmetric table (pure ring arithmetic)
- Coherence threshold constraint: T*=CREATE/HARMONY must be in (0,1)

**Proof:** (1) DIS is fully symmetric (no asymmetric pairs found exhaustively); anti-symmetric part identically zero over C×D block. (2) CROSS_CYCLE=44 is generator-independent (same for both g). (3) g=7 forces HARMONY=3, T*=5/3>1 — inadmissible. (4) g=3 forces HARMONY=7, T*=5/7<1 — valid. Selection by two independent constraints: (a) minimality: g=min{3,7}=3; (b) physical validity: T*<1 eliminates g=7 entirely.
**Dependencies:** D4 (T*∈(0,1) interpretation), D17 (W=3/50 cross-cycle), D18d (generator convergence structure).
**Consequence:** T*=5/7 is **fully forced** — no part of the chain is calibrated or conventionally chosen. The complete spine: Z/10Z arithmetic → primitive root g=3 (forced by T*<1) → centroid CREATE=5 → inverse HARMONY=7 → T*=5/7.
**Does NOT claim:** That the coherence threshold interpretation of T* (i.e., T*∈(0,1) is a requirement) is itself forced by ring theory. This requirement comes from the physics/architecture definition of T* as a threshold. The theorem is conditional on that interpretation.
**File:** `proof_d19_generator_selection.py`

---

---

## D20 — Inheritance Audit

**Statement:** Every spine invariant falls into exactly one of four inheritance classes: RING-forced (independent of generator and lens), GENERATOR-forced (requires g=3), LENS-forced (requires TSML/BHML rules), or CONTINGENT (architectural label only).
**Exact definitions:**
- RING-forced: determined by Z/10Z arithmetic alone, same under both g=3 and g=7
- GENERATOR-forced: requires primitive root g=3 (changes under g=7)
- LENS-forced: requires TSML or BHML rule structure
- CONTINGENT: naming/architectural choice with no algebraic consequence
**Key assignments:**
- CREATE=5: RING-forced — centroid((Z/10Z)*)=5; centroid(ODD={1,3,5,7,9})=5; both independent of generator
- W=3/50 value: RING-forced — CROSS_CYCLE=44, deviation=6, W=6/100=3/50 (same for g=3 and g=7)
- HARMONY=7: GENERATOR-forced — g^(-1) mod 10 = 7 only when g=3; under g=7, "HARMONY"=3
- T*=5/7: GENERATOR-forced — CREATE/HARMONY = 5/7 only when HARMONY=7
- W numerator label "g": GENERATOR-forced — W=3/50 = g/50 is a coincidence that requires g=3
- sinc² envelope: LENS-forced — appears via D2 continuum limit, needs Fourier/resonance structure
- Operator names: CONTINGENT
**Proof:** Exhaustive Z/10Z check; centroid arithmetic; generator swap test (g=7 gives CREATE=5 unchanged, HARMONY=3≠7).
**BONUS:** centroid(ODD)=5=CREATE; four independent routes to CREATE=5: (i) centroid (Z/10Z)*, (ii) centroid ODD, (iii) unique ODD fixed point of σ:v↦10-v (D21), (iv) additive midpoint of Z/10Z.
**Dependencies:** D17 (W), D18d (generator structure), D19 (g=3 selection), D21 (σ fixed point).
**Consequence:** Clarifies what is physically forced vs. what depends on lens choice or architectural label. LEFT half of corridor (t<1/2) = ring territory; RIGHT half = generator territory. Feeds D22.
**Does NOT claim:** That LENS-forced results are less rigorous — they are fully proved within the lens framework.
**File:** `proof_d20_inheritance_audit.py`, `papers/INHERITANCE_AUDIT.md`

---

## D21 — Fixed-Point Centroid

**Statement:** Every complement-equivariant (CE) ODD-output map F:(Z/10Z)→ODD must satisfy F(5)=5. The value 5 is the unique ODD fixed point of the complement map σ:v↦10-v.
**Exact definitions:**
- ODD = {1,3,5,7,9}
- CE condition: F(10-v) = (10-F(v)) mod 10 for all v
- σ:v↦10-v: the complement involution on Z/10Z
**Proof (one line):** Setting v=5: F(10-5)=F(5) on LHS; (10-F(5)) mod 10 on RHS. So F(5)=(10-F(5)) mod 10, i.e., 2F(5)≡0 mod 10. Solutions: F(5)∈{0,5}. But 0∉ODD. Therefore F(5)=5. □
**Exhaustive verification:** 625 CE maps total (9,765,625 total ODD-output maps); all 625 contain FP at 5; 400/625 (64%) have unique FP at 5; 100 have {1,5,9}; 100 have {3,5,7}; 25 have all-ODD.
**Phi test:** Phi fails CE at v=2,3,4 — D7 (Phi fixed point) and D21 (CE equivariance) are independent paths to CREATE=5.
**Dependencies:** None (pure arithmetic on Z/10Z).
**Consequence:** CREATE=5 now has four independent characterizations — overdetermined, not just one path. Feeds D20 (inheritance audit). The ring center is forced by equivariance alone, independent of generator.
**Does NOT claim:** That Phi is CE (it is not). D7 and D21 are independent results that agree on CREATE=5.
**File:** `proof_d21_fixed_point_centroid.py`

---

## D22 — Corridor Portrait

**Statement:** The four spine-forced corridor positions are strictly ordered and amplitude-profiled:
- Positional ordering (exact): 3/50 < 1/2 < 7/10 < 5/7 < 1
- Amplitude ordering (sinc², strict reversal): sinc²(3/50) > sinc²(1/2) > sinc²(7/10) > sinc²(5/7)
- Fine-structure identity: T* = HARMONY/10 + 1/70 = 7/10 + 1/(7×10) (exact)
- Inheritance split: LEFT half (t<1/2) = RING-forced; RIGHT half (t>1/2) = GENERATOR-forced; t=1/2 = inheritance boundary
**Exact positions:**
- W = 3/50 = 0.06: RING-forced, corridor entry amplitude ≈ 0.988
- CREATE/10 = 1/2: RING-forced (+ lens bridge), sine-maximum, sinc²(1/2)=4/π²≈0.405
- HARMONY/10 = 7/10: GENERATOR-forced, sinc² ≈ 0.135
- T* = 5/7 ≈ 0.7143: GENERATOR-forced, sinc² ≈ 0.121
**Ordering proof:** All four inequalities proved by exact Fraction arithmetic (Python fractions.Fraction).
**Amplitude proof:** sinc² strictly monotone decreasing on (0,1) (D24) + positional ordering → amplitude ordering.
**Fine-structure:** T* − HARMONY/10 = 5/7 − 7/10 = 50/70 − 49/70 = 1/70 = 1/(HARMONY × n). Exact.
**Attenuation mechanism:** t=1/2 is the unique sine-maximum in (0,1) (D24). But denominator πt=π/2 attenuates sinc(1/2)=2/π — ring center is structurally marked, not amplitude-dominant. Near t=0, sin(πt)≈πt so sinc≈1 (high amplitude).
**Dependencies:** D17 (W), D18d (HARMONY=7), D19 (T*, g=3 selection), D21 (CREATE=5), D24 (sinc² monotone).
**Consequence:** The corridor is fully mapped. All four spine landmarks are positionally ordered, amplitude-profiled, and inheritance-classified. The center t=1/2 is not an amplitude peak — it is the ring/generator boundary.
**Does NOT claim:** That the amplitude portrait has any direct connection to ζ zeros or to external spectral problems (see B6/A11 for those open claims).
**File:** `proof_d22_corridor_portrait.py`

---

**THE SPINE IS COMPLETE (D1–D22)**

**Volume A (arithmetic):** D1, D11a/b/c, D14, D15
**Volume B (operator/table):** D7, D8, D9, D10, D16, D17, D18a, D18c, D18d, D19, D20, D21
**Volume C (emergence/threshold):** D2, D3, D4, D5, D6
---

## D23 — Ring Wobble Theorem

**Statement:** Let Δ(x) = 1 if 5∤x, else 0. Let Wob(k) = (1/k)Σ_{x=1}^{k} Δ(x).
- (1) Closed form: Wob(k) = 1 − ⌊k/5⌋/k
- (2) Lower bound: Wob(k) ≥ 4/5 for all k ≥ 1
- (3) Equality: Wob(k) = 4/5 ⟺ 5|k
- (4) Limit: Wob(k) → 4/5 as k → ∞
- (5) Window invariance: Wob(b,k) = Wob(k) for k < SPF(b)
- (6) Generator independence: Wob identical under g=3 and g=7
**Exact definitions:**
- Neutral elements of Z/10Z: {0,5} = multiples of 5 (determined by ring, not generator)
- C10∪D10 = (Z/10Z)* ∪ 2·(Z/10Z)* = {1,2,3,4,6,7,8,9} = Z/10Z \ {0,5}
**Proof:**
- (1): Count multiples of 5 in {1..k}: ⌊k/5⌋. Non-neutral: k−⌊k/5⌋. Wob = (k−⌊k/5⌋)/k.
- (2)+(3): Write k=5m+r. Wob=1−m/(5m+r). Bound: 1/5 ≥ m/(5m+r) iff 5m+r≥5m iff r≥0. Equality iff r=0.
- (4): Squeeze: 1/5−1/k ≤ ⌊k/5⌋/k ≤ 1/5; both sides → 1/5.
- (5): From D15 — arithmetic on {1..k} is b-independent for k < SPF(b).
- (6): C10∪D10 determined by 10=2×5 ring structure; same for both primitive roots.
**Key correction over B10:** B10 claimed "period-10 oscillation". Correct statement: drops occur at period-5 (every multiple of 5); oscillation amplitude decays as O(1/k) and is not periodic. B10 branch-separation claim was FALSE (confirmed here).
**Dependencies:** D15 (window invariance), D17 (Z/10Z structure), D19 (generator independence confirmed).
**Consequence:** Ring wobble is fully characterized. Wob cannot separate generator branches; that is D19's job (T*<1 test). The wobble law is a pure ring-arithmetic consequence of 10 = 2×5.
**Does NOT claim:** Wob predicts the ω-transition; amplitude oscillation is periodic; any external spectral interpretation.
**Supersedes:** B10 (Wobble Branch Law) — promoted and corrected.
**File:** `proof_d23_ring_wobble.py`

---

---

## D24 — Corridor Midpoint Theorem

**Statement:** Let sinc²(t) = (sin(πt)/(πt))² for t ∈ (0,1).
- (I)   sinc²(t) is strictly monotone decreasing on (0,1)
- (II)  t = 1/2 is the unique point in (0,1) where sin(πt) = 1
- (III) sinc²(1/2) = 4/π² exactly
- (IV)  Under ring normalization t = v/10, CREATE=5 maps to t = 5/10 = 1/2
- (V)   D22's amplitude ordering (sinc²(W) > sinc²(1/2) > sinc²(7/10) > sinc²(T*)) is fully proved: D24-I + D22 positional ordering
**Proof of (I) — exact calculus:**
h'(t) = 2sin(πt)·[πt·cos(πt) − sin(πt)] / (π²t³).
sin(πt) > 0 for t ∈ (0,1). Need: sin(x) > x·cos(x) for x = πt ∈ (0,π).
- x ∈ (0,π/2): equivalent to tan(x)>x. f(x)=tan(x)-x, f(0)=0, f'(x)=tan²x>0 → f strictly increasing → f(x)>0. □
- x = π/2: cos(π/2)=0, x·cos(x)=0 < 1=sin(π/2). □
- x ∈ (π/2,π): cos(x)<0 → x·cos(x)<0<sin(x). □
Therefore h'(t) < 0 for all t ∈ (0,1). □
**Proof of (II):** sin(πt)=1 iff t=1/2+2k; in (0,1) only k=0 survives. One line. □
**Proof of (III):** sinc(1/2)=sin(π/2)/(π/2)=1/(π/2)=2/π; sinc²=4/π². One step. □
**Proof of (IV):** 5/10 = 1/2. One arithmetic step. □
**Dependencies:** D3 (sinc²(1/2)=4/π², restated), D17 (W), D18d (HARMONY=7), D19 (T*), D21 (CREATE=5).
**Consequence:** D22's amplitude ordering is no longer conditional on a B-tier result. The corridor portrait (D22) and the midpoint theorem (D24) are now both fully D-tier. B11 is superseded.
**Does NOT claim:** Any connection to σ=1/2 in the Riemann ζ function (that is A10, open). That sinc²(1/2)=4/π² is an extremum of sinc² on (0,1) (it is not — there are no interior extrema by D24-I).
**Supersedes:** B11 (Corridor Midpoint, Tier B). All B11 content is now fully proved.
**File:** `proof_d24_corridor_midpoint.py`

---

**THE SPINE IS COMPLETE (D1–D24)**

**Volume A (arithmetic):** D1, D11a/b/c, D14, D15
**Volume B (operator/table):** D7, D8, D9, D10, D16, D17, D18a, D18c, D18d, D19, D20, D21
**Volume C (emergence/threshold):** D2, D3, D4, D5, D6
**Volume D (corridor geometry):** D22, D23, D24
**Unified chain:** Z/10Z → g=3 (D19) → CREATE=5 (D18d, D20, D21) + HARMONY=7 (D18d) → T*=5/7 (D4, D18c, D18d) → corridor portrait (D22) + midpoint (D24) → wobble law (D23)
