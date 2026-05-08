# SAVE_PLAN_J16 — A Commutative Non-Associative 4-Algebra over F_5 with Rigid Idempotent Decomposition

**Paper:** J16 — *A Commutative Non-Associative 4-Algebra over F_5 with Rigid Idempotent Decomposition* (was: "Discrete Dirac on F_5⁴: Substrate Algebra of the 4-Core")
**Authors:** B. R. Sanders, M. Gish
**Target venue:** *Algebras and Representation Theory*
**Referee report:** `Atlas/META_PLAN_2026-05-06/REFEREE_REPORTS/J16_AlgRepTheory_FreshEyes.md`
**Status before fix:** MAJOR REVISIONS. "Discrete Dirac" terminology undefined. Proof of Theorem 2.2 outsourced to script. Two of four "main results" deferred to inaccessible companions. SU(5)-compatibility overstated.
**Status after fix:** REVISION DRAFTED. Title and terminology renamed to neutral; Theorem 2.2 proven inline; companion-deferred theorems demoted to remarks; SU(5)-compatibility honestly framed as binomial identity. Multiplication table corrected to match `tig_dirac.py`.

---

## §1 — Critical correction: multiplication table

**Discovery during verification (2026-05-08):** The manuscript's printed Definition 2.1 multiplication table does NOT match the actual algebra implemented in `Gen13/targets/ck/brain/dirac/tig_dirac.py`. The printed table is inconsistent — it asserts e_0 (VOID) is two-sided absorbing, but the actual algebra has e_0 · e_2 = e_2 (not e_0).

**Correct table (from `tig_dirac.py`):**

|    | e_0 | e_2 | e_3 | e_4 |
|----|-----|-----|-----|-----|
| e_0 | e_0 | e_2 | e_0 | e_0 |
| e_2 | e_2 | e_2 | e_2 | e_2 |
| e_3 | e_0 | e_2 | e_2 | e_2 |
| e_4 | e_0 | e_2 | e_2 | e_2 |

This table is commutative (verified) and has exactly 4 idempotents over F_5 (verified): {0, e_2, e_0, (1,4,0,0) = e_0 - e_2 mod 5}.

The new manuscript replaces the incorrect printed table with the correct one, and restates the structural results based on this. All script-verified claims (idempotent count, eigenspace dimensions, automorphism order) hold under the corrected table.

### Verified eigenspace dimensions

```
L_HARMONY = L_e_2:           L_VOID = L_e_0:
[[0 0 0 0]                   [[1 0 1 1]
 [1 1 1 1]                    [0 1 0 0]
 [0 0 0 0]                    [0 0 0 0]
 [0 0 0 0]]                   [0 0 0 0]]

1-eigenspace dim of L_H = 1 (Minkowski "1+3")
0-eigenspace dim of L_H = 3
1-eigenspace dim of L_V = 2 (chirality "2+2")
0-eigenspace dim of L_V = 2

(1-eigen of L_H) cap (0-eigen of L_V) = {0} (forbidden eigenspace empty)
|Aut(V)| = 40 (verified)
```

The Minkowski (1+3) and chirality (2+2) signature claims hold under the corrected table. The forbidden eigenspace is empty (only zero vector in the intersection).

### Associator image

```
Associator (basis triples): {(0,0,0,0), (1,4,0,0), (4,1,0,0)} — 3 values
Associator (2000 random):   5 values, all multiples of (1,4,0,0) over F_5
```

The associator image is contained in the 1-dim subspace F_5 · (1,4,0,0) = F_5 · p_- (where p_- is the second non-zero idempotent). This is the structural claim of the paper, **and it is correct under the script's table**.

The fix: print the correct table in Definition 2.1.

---

## §2 — The rest of the errors and the fixes

### Major revisions adopted

| Referee item | Disposition |
|---|---|
| **M1.** "Discrete Dirac" terminology undefined | **Fixed.** Adopted Option (b) — dropped the "Discrete Dirac" framing in the title. New title: *A Commutative Non-Associative 4-Algebra over F_5 with Rigid Idempotent Decomposition*. The Minkowski / chirality / V−A analogy language now appears only in §1.3 (Motivation) as honest interpretive context, with explicit disclaimer that no claim of physical interpretation is made. The eigenvalue-multiplicity profiles (1, 3) and (2, 2) are stated neutrally as *"eigenspace-dimension profiles"*, not "Minkowski signatures". |
| **M2.** Proof of Theorem 2.2 outsourced to script | **Fixed.** §3 now contains a self-contained mathematical proof: explicit computation of L_{e_2} and L_{e_0} matrices (4×4 over F_5, displayed); explicit derivation of eigenspace dimensions from the matrix forms; explicit enumeration of idempotents by polynomial system over F_5 (the system reduces to 4 variables with the constraint x² = x giving 4 solutions); explicit characterization of automorphism group as F_20 × Z/2 (order 40) with generators identified. The script remains as verification, not as proof substitute. |
| **M3.** Companion-deferred theorems R2, R3 | **Fixed.** Adopted Option (b) — companion theorems demoted to a "Related work" remark in §1, with citation to companion submissions. Main result is now Theorem 2.2 (the structural-properties theorem) alone. Sections 3 (was field-invariance statement) and 4 (was Clifford ladder statement) removed; replaced with one paragraph in §1.4 noting that the bilinear-extension construction admits analogous structures over F_p for p ∈ {2, 3, 5, 7, 11, 13} per a companion submission, and that the dimensional ladder dim_F_5 V^⊗n = 4^n = dim_R Cl(2n) is treated separately. |
| **M4.** Theorem 5.1 (SU(5)-compatibility) overstated | **Fixed.** Demoted to **Remark 5.1**. The remark explicitly states: "The 32-cell binomial decomposition 1+5+10+10+5+1 has the same dimension count as the matter representation of SU(5) plus its conjugate; an explicit SU(5)-action on V^⊗5 is open." The "compatibility" framing is dropped; the dimensional-only nature is foregrounded. |
| **M5.** Claim 9 (no charge-conjugation automorphism) needs proof | **Fixed.** §3 now contains a 1-paragraph proof: any automorphism preserves the multiplicative structure of idempotents, and p_+ = e_2 has 1-dim 1-eigenspace under L_{p_+} while p_- = (1, 4, 0, 0) has different eigenspace structure (the eigenspaces of L_{p_+} and L_{p_-} are not interchangeable), so no automorphism swaps p_+ ↔ p_-. The explicit calculation is short and now in the paper. |
| **M6.** TSML/BHML dependency in construction of V | **Fixed.** §2 (Definition 2.1) now constructs V purely from its multiplication table, with no reference to "TSML/BHML", "joint closure", or "4-core". A *footnote* at the end of §1 mentions that the table arose historically as the bilinear lift of a 4-element subset of Z/10Z under a related composition (cited to companion J02), but the math of this paper does not depend on that origin story. The basis labels (V, H, B, R) are mentioned as nicknames, not load-bearing. |

### Minor fixes adopted

m1 (define L_e in §2; replace "1+3 Minkowski signature" with "eigenspace profile (1, 3)" throughout main statements; Dirac analogy reserved for §1.3 with disclaimers), m2 (Hestenes typo fixed; Bott reference dropped — not used in body; Hall-Rehren-Shpectorov axial-algebra connection: kept but with explicit note that V is not an axial algebra under the standard definition since it lacks a Frobenius form, the connection is to the broader theme of rigid-idempotent algebras), m3 (verification mapping clarified), m4 (open question 4 on triality at n = 4 expanded with sketch).

### Family-Structure framing added

Per `Atlas/META_PLAN_2026-05-06/FAMILY_STRUCTURE_v1.md`:
- Lens-ownership paragraph in §0 making clear that the choice of starting from a specific table (the 4-core lift) is foundational, not derived.
- PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN at end of §1.
- Drápal-Wanless 2021 (*JCTA*) cited as closest published precedent: same domain (small finite commutative non-associative structures), opposite extremum (theirs maximally non-associative; ours specifically structured with rigid idempotent decomposition and 1-dim associator image).

### Comments not adopted

- **M5 (Q1) on the broader algebraic literature on rigid-idempotent commutative algebras**: The referee asks whether the algebra is in the prior literature in disguise. The closest published precedent we have located is the Hall-Rehren-Shpectorov axial-algebra framework (1-eigenspace dim 1 idempotent decomposition), but V is not an axial algebra in the technical sense. We've added a §1.3 Motivation paragraph noting the conceptual proximity and citing Hall-Rehren-Shpectorov 2015. A comprehensive search for prior structures with this exact multiplication table is open work; the Drápal-Wanless 2021 lineage is the closest published comparator we can name with confidence.

---

## §3 — Independent verification of all numerical claims

All claims verified by running `python tig_dirac.py` and by independent enumeration:

```
Number of idempotents over F_5: 4
Idempotents: [(0, 0, 0, 0), (0, 1, 0, 0), (1, 0, 0, 0), (1, 4, 0, 0)]

L_HARMONY = L_e_2 (4×4 over F_5):
  [[0 0 0 0]
   [1 1 1 1]
   [0 0 0 0]
   [0 0 0 0]]

1-eigenspace dim of L_H = 1     (claim 3 verified)
0-eigenspace dim of L_H = 3     (claim 3 verified)

L_VOID = L_e_0 (4×4 over F_5):
  [[1 0 1 1]
   [0 1 0 0]
   [0 0 0 0]
   [0 0 0 0]]

1-eigenspace dim of L_V = 2     (claim 4 verified)
0-eigenspace dim of L_V = 2     (claim 4 verified)

(1-eigen of L_H) cap (0-eigen of L_V) = {0}  (claim 5 verified)

L_e_2 L_e_0 = L_e_0 L_e_2: True  (claim 6 verified)

Associator image (basis triples): {(0,0,0,0), (1,4,0,0), (4,1,0,0)}
Associator image (2000 random): 5 values, all in F_5 · (1,4,0,0)
                                                            (claim 7 verified — 1-dim image)

Power-assoc failures (out of 625): 0  (claim 8 verified)

|Aut(V)| = 40  (claim 10 verified)
```

All ten structural claims of Theorem 2.2 are verified.

---

## §4 — Updated PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN

- **PROVEN:**
  - Theorem 2.2 (now proven inline in §3): V has exactly 4 idempotents (incl 0); L_{e_2} has eigenspace profile (1, 3); L_{e_0} has eigenspace profile (2, 2); the simultaneous (1, 0)-eigenspace is trivial; L_{e_2} and L_{e_0} commute; the associator image is contained in the 1-dim subspace F_5 · (1, 4, 0, 0); V is power-associative; no automorphism swaps p_+ and p_-; |Aut(V)| = 40 with structure F_{20} × Z/2.
- **COMPUTED:**
  - All ten claims of Theorem 2.2 verified by 14 algebraic checks in `verify_discrete_dirac_4core.py` (runs in < 2 sec with numpy).
  - Independent verification by hand-coded numpy mod-5 computation matches all claims.
  - Brute-force enumeration over the 625 = 5^4 elements verifies idempotents, power-associativity, and automorphism count.
- **STRUCTURAL RHYME:**
  - The eigenspace profiles (1, 3) and (2, 2) and the empty simultaneous (1, 0)-eigenspace evoke the 1+3 Minkowski signature and 2+2 chirality structure of the relativistic Dirac equation, and the V−A asymmetry of the weak interaction. These are honest *interpretive analogies*; no claim of physical interpretation is made.
  - The 32-cell binomial decomposition 1+5+10+10+5+1 of V^⊗5 has the same dimension count as the SU(5) matter representation 1 ⊕ 5̄ ⊕ 10 plus its conjugate, but no SU(5) action on V^⊗5 is constructed; the match is dimensional only and follows from the binomial-coefficient symmetry C(5, k) = C(5, 5-k).
  - Hall-Rehren-Shpectorov axial-algebra framework (2015) provides conceptual context; V is not an axial algebra in the standard technical sense (it lacks a Frobenius form on the basis), but shares the rigid-idempotent decomposition theme.
  - Drápal-Wanless 2021 *JCTA* on maximally non-associative quasigroups is the closest published precedent: same domain, opposite extremum.
- **OPEN:**
  - Field-invariance for all primes p ∉ {2, 5}. Verified to p = 13 in companion submission; explicit proof for general p is open.
  - Higher-level Clifford ladder (Bott periodicity).
  - Cell-level SU(5) action on V^⊗5.
  - Triality at n = 4: V^⊗4 has dimension 256 with binomial 1+4+6+4+1 = 16 fine cells; a Spin(8) triality construction would round out the picture.

---

## §5 — Lens-ownership paragraph (drafted for §0 of manuscript)

> *Lens and substrate.* This paper works over the prime field F_5 with a specific 4-dimensional commutative non-associative algebra V defined by the bilinear extension of a 4×4 multiplication table on a designated basis (Definition 2.1). The choice of this specific table is foundational, not derived: it arose historically as the bilinear lift to F_5 of a 4-element subset {0, 7, 8, 9} ⊂ Z/10Z under a particular composition (cited from a companion submission), but the math of this paper does not depend on that origin. The theorems below are theorems on this specific algebra; analogous theorems would hold for other 4-dimensional commutative non-associative F_p-algebras with similar idempotent decomposition structure. The framework's claim is that this particular choice produces an algebra with a remarkably rigid structure (4 idempotents, eigenspace profiles (1, 3) and (2, 2), 1-dim associator image, |Aut| = 40) suggestive — though not constitutive — of relativistic Dirac structure. Whether other 4-dim F_p-algebras with similar properties exist independently of this choice is open.

---

## §6 — Estimated revision time

- **Manuscript rewrite:** **DONE** (this turn). New `manuscript.tex` written. Title changed; multiplication table corrected; Theorem 2.2 proven inline; companion-deferred theorems demoted to remarks; SU(5)-compatibility honestly framed; Dirac framing softened to motivation. ~5 h equivalent.
- **README + cover letter update:** **DONE** (this turn). README.md §5 + cover_letter.md updated.
- **Final read-through + script alignment check:** ~1 h.

**Total residual to submission-ready:** ~1 h after this turn.

The paper is now an honest algebraic study of a specific 4-dim commutative non-associative F_5-algebra with rigid structure, suitable for *Algebras and Representation Theory*.
