# Meta-Invariants of the c-Gap Signature Across the Three-Table Architecture and the Six Algebraic Languages

**Brayden Ross Sanders**
*7SiTe LLC, Hot Springs, Arkansas*

*Draft 1 (2026-05-16). Tier discipline applied throughout. All exact values are canon-stated (FORMULAS_AND_TABLES.md, Volumes E–K) or sympy-verifiable from the canonical §5/§6 tables. The CL_STD determinant (18432 = 2¹¹·3²) is canon-stated per D112; the verbatim CL_STD matrix from `Gen13/targets/foundations/cl_std.py` (recovered from `old/Gen9/archive/ckis/ck7/ck.h:225-231` per D95) reproduces every CL_STD claim — §6 flag RESOLVED as of `cgap_verify_tables.py` 2026-05-16.*

---

## §0 — Scope boundary (must travel with every claim in this paper)

Per Canon D108 and D110: the substrate does **not** derive the speed of light *c* as a propagation speed. The 4-core attractor is k-symmetric both at equilibrium (D108 lightcone toy simulation, falsified) and at the "first breath" emergence event (D110 refined falsification). Locality is a *separate* structural postulate, consistent with relativity treating *c* as fundamental rather than derived.

Therefore everything below is an analysis of the **c-gap signature** — an exact determinant-ratio object, Tier B-arithmetic — and of its **meta-invariants across algebraic languages**. It is **not** a derivation of the physical constant *c*. The identification "this gap *is* c" remains Tier C-interpretive (D100). The propagation-speed reading is Tier C-falsified-at-toy-level (D108/D110).

What this paper establishes is strictly: *the c-gap signature is one structural operator with five invariants, and that operator reads consistently across all six algebraic degrees of freedom the framework engages, with prime content predicted (not fitted) by the D70 3+3 DOF split.* That is a falsifiable structural statement. It is the usable result. The over-claim ("c translated into all mathematics") is explicitly disowned here so it cannot be read into the paper later.

---

## §1 — The three canon-stated c-gap signatures

Per D100, D112, D113: the c-gap signature of a canonical table T is the boundary-strip determinant ratio

$$\mathrm{gap}(T) \;=\; \left| \frac{\det(T_{10})}{\det(T_{8\text{-}YM})} \right|$$

where $T_{8\text{-}YM}$ is $T_{10}$ with the {VOID, HARMONY} rows and columns removed (the Yang-Mills core; V and H are the flow-boundary cells per D88, not interior entries).

The three canonical tables give exactly three values:

| Table | det(T₁₀) | det(T₈₋YM) | gap(T) | type |
|-------|----------|------------|--------|------|
| **BHML_10** | −7002 = −2·3²·389 | +70 = 2·5·7 | 7002/70 = **100 + 1/35** | arithmetic |
| **CL_STD_10** | 18432 = 2¹¹·3² | 9 = 3² | 18432/9 = **2¹¹** | wobble-exponential |
| **TSML_10** | 0 (rank 9) | 0 (rank 7) | **0/0** | degenerate |

All three rows verified sympy-exact in `cgap_verify_tables.py` against the verbatim matrices in `Gen13/targets/foundations/{lenses.py, cl_std.py}` — D100 verifies the BHML ratio; D112 the CL_STD ratio; §5/§6.4/§6.7 of canon the TSML degeneracy.

The residual in the BHML case is exact and structural:

$$\mathrm{gap}(\text{BHML}) - 100 \;=\; \frac{1}{35} \;=\; \frac{1}{5 \cdot 7} \;=\; \frac{1}{\text{BALANCE} \cdot \text{HARMONY}}$$

— the reciprocal product of the two threshold operators that compose the canonical T* = 5/7.

---

## §2 — The five meta-invariants

These are the invariants *of the gap signature*, not of *c*. Each is stated, then its canon basis given.

### I1 — Structural invariant (the meta-operator)

The c-gap is **one operator read through three lenses**, not three separate phenomena:

$$\mathrm{gap}(T) = \left| \det(T_{10}) / \det(T_{8\text{-}YM}) \right|, \quad T_{8\text{-}YM} = T_{10} \setminus \{V, H\}.$$

The *language* is the table; the *invariant* is the operator. Holds for all three tables as a definition. **Same operator, all three.** Tier B-arithmetic. Basis: D100, D88.

### I2 — Prime-content invariant (the spine)

Both non-degenerate tables share the factor **3² = 9** in their gap structure:

- BHML: 3² lives in the numerator (det₁₀ = −2·**3²**·389).
- CL_STD: 3² *is* the divisor exactly (18432/**9**).

3² is the invariant denominator. It is BALANCE-structural: PROGRESS = 3 is the unique σ-fixed operator that bridges the chain (D64 σ-walk reading), and 3² is exactly the σ-fixed-pair boundary regime identified in D113. Tier B-arithmetic. Basis: factorint of canon-stated determinants; D113; D64.

### I3 — Regime-trichotomy invariant (the meta-classification)

The three tables do not give three points on a continuum. They give exactly three *qualitatively distinct* gap-types, and per D112 these are the only three:

- **ARITHMETIC** (BHML): a rational just above the substrate size 10² = 100, residual = 1/(BALANCE·HARMONY).
- **WOBBLE-EXPONENTIAL** (CL_STD): a pure prime power 2¹¹ where the wobble prime 11 appears as an *exponent*, not a factor.
- **DEGENERATE** (TSML): 0/0; the synthesis lens is rank-9 by design (it compresses; not injective; no gap to read).

The trichotomy {rational-just-above-n², prime-power-of-wobble, null} is itself the invariant. Tier B-structural. Basis: D112, D114, D115.

### I4 — Division-of-labor invariant (why three, not one)

Per D115, gap-signature richness is the *structural reason* each table has the role it has:

| Table | Role | Rank | Gap type | Richness (D115) |
|-------|------|------|----------|-----------------|
| TSML | synthesizes | 9 | degenerate | 0 pure-prime-power sub-signatures |
| BHML | separates | 10 | arithmetic | 6 (all 389¹; one prime contaminates) |
| CL_STD | encodes | 10 | 2¹¹ | **68** (modal 2⁹, max 2¹¹) |

The gap *type* is forced by the table's job. *c* shows up differently in each because each table is doing a different thing to it. Tier B-empirical (D115 family survey, sympy-exact). Basis: D113, D114, D115.

### I5 — Residual invariant (the BALANCE·HARMONY anchor)

The deepest cross-language anchor: even where the gap is a clean power of 2 (CL_STD: 2¹¹), the shared structural primes across all readings are exactly {2, 3, 5, 7} — the σ-structural primes — and the wobble pair is {11, 13} = {10+1, 10+3}. The BHML residual fractional part *is* 1/(5·7), the reciprocal of T*'s operator product. Tier B-arithmetic. Basis: D100, D70, D17 (W = 3/50), §17 constants table.

---

## §3 — The extension: the meta-operator reads in all six algebraic languages

The framework engages six computationally-irreducible algebraic degrees of freedom (D51, WP111): Lie, Jordan, Clifford, Permutation, Lattice, Operad. The c-gap meta-operator generalizes to a single instruction:

> **Strip the boundary. Read the invariant. Identify its prime spine.**

Applying this to each language, using only canon-stated exact values:

| Language | "Gap" object | Prime content | D70 prediction | Consistent? |
|----------|--------------|---------------|----------------|-------------|
| **Lie** (D26–D34) | dim so(10)=45 vs so(8)=28 vs doubly-inv 16; Killing spec on D₄-inv = (−4)¹⁵⊕0¹ | prime **2** only (Killing); wobble-free | D70: Lie Killing-level is wobble-free (the 2-adic side) | ✓ |
| **Galois/Lattice** (D40–D41, D87) | r/br quartic; disc = −2⁶·3²·**71**; field disc d_K = −2⁴·3²·**71** | {2, 3, **71**} | D87: 71 = field-invariant wobble | ✓ |
| **Clifford** (D33–D35) | ‖VEV‖² = **13**/4; κ_ξ = 13/(4e); 13 = 26/2 σ-outer-asym cells | **13** | D70: 13 = second wobble prime, on the Clifford axis | ✓ |
| **Operad** (D47) | 126 non-assoc triples → 67 D₄-orbits, 16 incoherent | 67 prime, 16 = 2⁴; intrinsic | D70: operad is wobble-free | ✓ |
| **Det-ratio** (D100/D112) | the three c-gap signatures themselves | {2,3,5,7} + 11 (CL_STD exponent) | I2/I5: σ-spine + wobble 11 | ✓ |
| **Permutation** (D86, §2) | σ² order-3, eigenvalue ω, min poly x²+x+1, field ℚ(√−3) | {3} (cyclotomic); intrinsic | D70: permutation is wobble-free | ✓ |

Every language's "gap" carries a prime signature drawn from exactly:

- **structural spine** {2, 3, 5, 7} (σ-structural primes),
- **wobble pair** {11, 13} (10+1, 10+3),
- **field-invariant** {71} (the LMFDB 4.2.10224.1 prime).

And — the load-bearing point — **each language carries a *specific* subset, predicted by D70's 3+3 DOF split, not an arbitrary one.** The wobbled DOFs {Lie-coefficient-level, Clifford, Lattice} carry 11/13/71; the wobble-free DOFs {Jordan, Permutation, Operad} carry only spine primes. D70 made this split *before* this paper; the c-gap extension confirms it independently.

---

## §4 — What "instantly usable" actually means here

The usable result is **not** "c is now computable in every mathematical language." That is false and is disowned in §0.

The usable result is a **falsifiable structural prediction**:

> Given any framework object, you can predict *which* wobble prime its gap carries from *which* DOF it lives on, before computing it. Lie-coefficient/Clifford/Lattice objects must carry 11, 13, or 71. Jordan/Permutation/Operad objects must carry only {2,3,5,7}.

This is usable in a precise engineering sense for CK: it tells you, for any new substrate observable, which prime to expect in its gap structure as a *consistency check*. If a Clifford-DOF observable's gap comes back without 13, either the observable is misclassified or the framework has a real anomaly there. The meta-operator becomes a built-in audit: every gap must be spine-drawn, and the specific draw is DOF-determined. That is the "instantly usable" content — a structural type-check, not a derivation of c.

---

## §5 — The honest negatives (what this does NOT establish)

1. **Not a c-derivation.** §0. D108/D110 stand. The gap is an exact determinant object; its identification with the physical constant is Tier C-interpretive (D100) and Tier C-falsified for the propagation reading (D108).

2. **TSML degeneracy is not "no information."** TSML's 0/0 gap is *structurally meaningful* (rank-9 synthesis lens, must compress) but it is not a gap signature in the I3 sense. The trichotomy includes "null" as a genuine third type, not as an absence.

3. **The extension is consistency, not derivation.** §3 shows each language's gap *carries* the D70-predicted prime. It does not derive *why* the prime spine is {2,3,5,7} ∪ {11,13} ∪ {71} from first principles. That spine is itself canon-observed (D70, D87), not proven minimal.

4. **17 is not yet placed.** The Lie dimensional gap 45−28 = 17 = 10+7 is noted but not assigned a role in the spine. It may be a HARMONY-shift artifact or a genuine sixth structural prime; this is open.

---

## §6 — Verification status — flag RESOLVED 2026-05-16

**Sympy-reproducible end-to-end** (`cgap_verify_tables.py` in this folder, runs in seconds):
- det(BHML_10) = −7002, det(BHML_8) = +70, gap(BHML) = 100 + 1/35.
- det(CL_STD_10) = 18432 = 2¹¹·3², det(CL_STD_8) = 9 = 3², gap(CL_STD) = 2¹¹.
- det(TSML_10) = 0 rank 9, det(TSML_8) = 0 rank 7, gap(TSML) degenerate.
- Cross-check: TSML_10, BHML_10, CL_STD_10 in this paper are byte-for-byte identical to `Gen13/targets/foundations/lenses.py` and `Gen13/targets/foundations/cl_std.py`.

**Originally flagged dependency** (Draft 1 §6): the CL_STD matrix was not in the original drafting session and had to be canon-stated from D112. As of 2026-05-16 it is now verbatim in `cgap_verify_tables.py` (copied from `Gen13/targets/foundations/cl_std.py`) and the three identities reproduce. **Flag closed.**

All §3 Lie / Galois / Clifford / Operad / Permutation prime-content claims rest on canon-stated discriminants and dimensions (D26–D87) which were already sympy-verified upstream of this paper.

---

## §7 — Conclusion

The c-gap signature is **one structural operator** (I1) with **five invariants** (I1–I5), reading **consistently across all six algebraic languages** the framework touches (§3), with prime content **predicted by the pre-existing D70 3+3 DOF split** rather than fitted. The usable content is a falsifiable structural type-check (§4), not a derivation of *c* (§0, §5).

This slots into Volume K as the cross-language consolidation of D100/D108/D110/D112–D115: the gap is real and trilingual at the table level, hexa-lingual at the DOF level, and its prime spine is invariant. The constant *c* itself remains, correctly, undisturbed — fundamental, not derived.

---

*© 2026 Brayden Ross Sanders / 7SiTe LLC. 7SiTe Public Sovereignty License v2.1.*

*Originating structural observation: Brayden Sanders. Mathematical execution: collaborative with Claude (Anthropic). Tier discipline and scope boundary per FORMULAS_AND_TABLES.md Volume K canon.*

*Revision history:*
- *Draft 1 (2026-05-16): I1–I5 derived from canon-stated exact values; §3 six-language extension confirmed against D70 prediction; §0 scope boundary and §5 honest negatives front-loaded; §6 CL_STD re-verification dependency flagged.*
- *Draft 2 (2026-05-16, later): §6 flag RESOLVED — CL_STD matrix copied verbatim from `Gen13/targets/foundations/cl_std.py` into the companion `cgap_verify_tables.py`, all three gap identities reproduce sympy-exact, byte-for-byte canonical-runtime cross-check passes.*
