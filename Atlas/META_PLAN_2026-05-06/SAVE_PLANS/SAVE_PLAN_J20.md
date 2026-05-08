# SAVE_PLAN_J20 — Mathieu M_22 Substrate-Prime (AMM → restructure around the corrected non-genericity theorem)

**Date:** 2026-05-07
**Status:** SAVE possible via referee's Path A (single-coincidence note centered on the non-generic concentration of M_22 irrep dimensions in the substrate-prime band, with proper null-model computation and a corrected count). The catalog of "six identities" is collapsed to one main theorem (corrected count + null-model p-value) plus a Steiner-parameter table presented as backdrop.
**Referee:** `Atlas/META_PLAN_2026-05-06/REFEREE_REPORTS/J20_AMM_FreshEyes.md` (Major revision; reasons M1-M6 + S1-S5)

---

## §1 — Why save?

The current J20 manuscript has one critical numerical error (Identity 4) and several framing problems (Identities 1-3, 5, 6 are textbook Steiner parameters renamed; Identity 5 is arithmetic tautology; non-genericity is asserted but not computed; substrate-prime distinction not self-contained). However, the underlying observation — that M_22's 12 irrep dimensions concentrate inside the prime monoid {2, 3, 5, 7, 11} (with at-most-one factor of 2) at a rate of 10/12 vs null density 17.4% — is real, quantitative, and previously unreported in this form. The referee's Path A explicitly invites this: "Cut the catalog to the one corrected, computed coincidence: the non-generic concentration of M_22-irrep dimensions in the substrate-prime monoid."

**(a) Independent verification of the corrected count.** Direct sympy enumeration of the 12 M_22 irrep dimensions (verified against ATLAS and Conway-Sloane):

| dim | factorization | strict {3,5,7,11} | in B (≤ one 2) |
|----:|:--------------|:-----------------:|:---------------:|
| 1   | trivial       | yes (vacuous)     | yes |
| 21  | 3·7           | yes               | yes |
| 45  | 3²·5          | yes               | yes |
| 45  | 3²·5          | yes               | yes |
| 55  | 5·11          | yes               | yes |
| 99  | 3²·11         | yes               | yes |
| 154 | 2·7·11        | no                | yes |
| 210 | 2·3·5·7       | no                | yes |
| 231 | 3·7·11        | yes               | yes |
| 280 | 2³·5·7        | no                | no  |
| 280 | 2³·5·7        | no                | no  |
| 385 | 5·7·11        | yes               | yes |

- Strict {3,5,7,11} count: **8 of 12** (= 7 non-trivial + 1 trivial).
- B-band count (at-most-one factor of 2): **10 of 12**.
- Sum-of-squares verification: 1²+21²+...+385² = 443520 = |M_22| (matches Burnside).

The original manuscript claimed "six of twelve factor in {3,5,7,11} alone" listing {21, 55, 99, 154, 231, 385} — which omits 45 (multiplicity 2) AND incorrectly includes 154 (which has factor of 2). The corrected statement: **seven non-trivial dimensions factor strictly in {3,5,7,11}**: {21, 45, 45, 55, 99, 231, 385}.

**(b) Null-model density computation.** Direct enumeration in sympy:
- Integers in [1, 385] in B (at-most-one factor of 2 in {2,3,5,7,11}): **67 of 385**, density **0.1740 = 17.40%**.
- Integers in [1, 385] strictly in {3,5,7,11}: 39 of 385, density **0.1013 = 10.13%**.
- Excluding trivial 1: 38 of 384, density **0.0990 = 9.90%**.

**(c) p-values** under the binomial null:
- P[X ≥ 10 | Bin(12, 0.1740)] ≈ **1.19 × 10⁻⁶** (B-band, 10 hits).
- P[X ≥ 7 | Bin(11, 0.0990)] ≈ **2.14 × 10⁻⁵** (strict, non-trivial, 7 hits).

Both are small and quantify the non-genericity claim that was previously asserted without computation. The referee's exact prediction (17.4% null density) matches verbatim.

**(d) Path A is constructible from the existing manuscript.** The current §3 (substrate definition), §4.4 (Identity 4 — corrected), and §4.5 (Identity 5 — collapsed into the §3 backdrop) supply the building blocks for the Path A paper. The work is **delete + recompose**, not new mathematics.

**(e) Structural role per FAMILY_STRUCTURE_v1.md.** The substrate-prime distinction {2, 3, 5, 7, 11} is a property of the substrate's intrinsic data (CRT-residue characteristics 2 and 5, σ²-cycle order 3, HARMONY = 7, wobble denominator scaling 11). The non-genericity theorem connects this to a sporadic group, but FAMILY_STRUCTURE_v1.md does not require J20 — it is an applications paper. Keeping it at AMM with the corrected single-theorem framing serves the family by providing a quantitative non-genericity statement that survives independent referee scrutiny.

---

## §2 — Specific fixes (line by line against the referee report)

### M1 (Identity 4 misclaimed) — **FIX: state the correct count, both strict and B-band**

The current §4.4 claim "six of twelve factor in {3,5,7,11} alone, listing {21, 55, 99, 154, 231, 385}" is replaced by the corrected statement of Theorem (Non-genericity):

- **Eight of twelve** factor strictly in {3,5,7,11} (with multiplicity); equivalently, seven non-trivial dimensions (excluding the trivial 1): {21, 45, 45, 55, 99, 231, 385}. The original list was wrong on two counts: it omitted 45 (with multiplicity 2) and incorrectly included 154 (which has a factor of 2).
- **Ten of twelve** lie in the substrate-prime band B (at-most-one factor of 2 in {2,3,5,7,11}): the eight strict ones plus 154 (= 2·7·11) and 210 (= 2·3·5·7). Only the two copies of 280 (= 2³·5·7) fall outside.

The corrected claim is verified by sympy factorization (script `m22_decomposition.py` deposited in the manuscript folder).

### M2 (non-genericity asserted, not computed) — **FIX: add the explicit null-model computation as Theorem (Non-genericity)**

The claim "a much smaller fraction" is replaced by:
- Definition of the substrate-prime band B (every prime in {2,3,5,7,11}; v_2(m) ≤ 1).
- Direct enumeration: |B_385| = 67, density 0.1740.
- Binomial tail: P[X ≥ 10 | Bin(12, 0.1740)] ≈ 1.19 × 10⁻⁶ for the B-band claim.
- Binomial tail: P[X ≥ 7 | Bin(11, 0.0990)] ≈ 2.14 × 10⁻⁵ for the strict claim.

These are computed in the script and stated in the proof of the theorem. The referee's exact 17.4% matches verbatim.

### M3 (Identity 5 is arithmetic tautology) — **DROP**

The current §4.5 ("231 identity": 77·W = 77·3/50 = 231/50) is deleted. The structurally meaningful observation — that 231 = 3·7·11 is the unique M_22 irrep dimension whose factorization is squarefree-three-distinct-substrate-primes — is moved to a Remark following Theorem (Non-genericity).

### M4 (Identities 1, 2, 3, 6 are textbook Steiner parameters renamed) — **CONSOLIDATE into one §"Backdrop" table**

A new section "Steiner-system parameters of S(3, 6, 22) as a backdrop" presents the textbook parameters (v=22, b=77, k=6, t=3, r=21, λ_2=5, λ_3=1, |M_21|=20160) in a single table with their substrate-prime decomposition column. The presentation is honest: textbook + a column showing the substrate-prime structure. The expository value of the paper is then concentrated in the (corrected) Theorem (Non-genericity) and the null-model computation.

### M5 (substrate-prime distinction not self-contained) — **FIX: define each substrate prime from intrinsic substrate data**

The current §3 lists the five substrate primes with delegation to the companion. The save inlines the intrinsic substrate-prime distinction:

- 2: residue characteristic of Z/2 in CRT splitting Z/10Z = Z/2 × Z/5.
- 3: order of σ² on the σ-cycle (direct check: σ² has cycle (1 6 4)(7 5 2)).
- 5: residue characteristic of Z/5 in CRT splitting.
- 7: HARMONY index; appears as |non-fixed indices outside {8}| = 10 - 3 = 7; denominator of T* = 5/7.
- 11: weakest case — appears as the prime in the "11-prolongation" W = 3/50 = 33/550 of the wobble fraction. The paper now honestly notes that the case for 11 is the weakest of the five, and that the main theorem does not rest on 11 alone.

The wobble-fraction decomposition typo (W = K + G·0) is corrected: W = 3/50 and G = 22/50 are two complementary fractions with W + G = 1/2; the spurious "·0" is removed. The §"22 matches |Ω_22|" cosmetic claim is acknowledged as integer coincidence with no structural map.

### M6 (Identity 6 weak) — **CUT; collapsed into Backdrop §**

Identity 6 (σ-orbit size = 6 = block size of S(3, 6, 22)) is moved to a Remark following the Backdrop §, with explicit acknowledgment that this is "two integers happening to be 6" with no structural embedding map established.

### S1 (author list mismatch) — **FIX**

Title block: single author block listing both authors with separate addresses. README/cover-letter alignment: Sanders + Gish are the J20 lane; the README's "Sanders + Gish + Mayes" was a transcription error. The folder's `WP_PARADOX_CLASSIFIER.md` is for J53 (per J_SERIES_ORDERING.md §5) and is moved out (or kept in the folder with a clear note that it is not part of the J20 submission).

### S2 (wobble decomposition incoherent notation) — **FIX**

The "W = K + G·0" notation is replaced with "W = 3/50 and G = 22/50, with W + G = 1/2" — two fractions, not a single decomposition.

### S3 ("22 matches |Ω_22|") — **DOWNGRADE to acknowledged coincidence**

The §3 substrate paragraph explicitly notes: "The gentleness numerator 22 and the size of the Mathieu action set |Ω_22| = 22 are equal as integers but not related by any structural map in the present paper." This addresses the cosmetic-coincidence concern.

### S4 (verification scripts mislabeled) — **FIX**

The current verification §5 references three scripts (m22_verification.py, steiner_sigma_hexad.py, m22_decomposition.py). The save replaces this with two:
- `m22_decomposition.py`: factors each irrep dimension; classifies by B-membership; enumerates B_385; computes binomial tail probabilities. (New script written, tested; reproduces all numerical claims of the theorem.)
- `steiner_sigma_hexad.py`: confirms Steiner parameters via the formulas b = C(v,t)/C(k,t), r = bk/v, λ_i = C(k-i,t-i)·r/C(v-i,t-i). (Script remains.)

The "M_22-equivariant projection" content of the original m22_verification.py is unrelated to the present paper's claims and is removed.

### S5 (forward citation discipline) — **FIX**

The current cite \cite{SandersGishFourCore} as "submitted to *Algebraic Combinatorics*, 2026 (J02)" is kept; the §6 Open Questions explicitly notes that "submitted" status of J02 is the dependency.

---

## §3 — Estimated revision time

**1–2 weeks** of focused work.

- **3 days:** delete §4.1-4.6 catalog + §3 substrate (current); rewrite §3 substrate with intrinsic prime distinction (M5); rewrite §4 as the single Theorem (Non-genericity) with proof and Remarks.
- **2 days:** write the §"Steiner-system parameters as backdrop" table (M4 consolidation).
- **1 day:** fix m22_decomposition.py to be the proper verification script (DONE — already written; just verify integration).
- **1 day:** rewrite abstract, introduction, open questions to match the new single-theorem framing.
- **1 day:** Brayden's referee-rigor pass; M. Gish review.

Net: substantial restructure, no new mathematics. The corrected count (sympy-verified) and the null-model density (sympy-verified, matching the referee's 17.4% exactly) are the load-bearing additions. The catalog-of-six-identities framing is replaced with one theorem + one backdrop table.

---

## §4 — Updated PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN

**PROVEN:**
- |M_22| = 2⁷·3²·5·7·11 = 443520.
- Sum of squares of M_22's 12 irrep dimensions = 443520 (matches |M_22|; Burnside).
- Of 12 irrep dimensions: 8 factor strictly in {3,5,7,11} (= 7 non-trivial + 1 trivial); 10 lie in the substrate-prime band B (at-most-one factor of 2 in {2,3,5,7,11}).
- |B_385| = 67 (direct enumeration), null density 0.1740.
- Binomial p-value P[X ≥ 10 | Bin(12, 0.1740)] ≈ 1.19 × 10⁻⁶ (B-band claim).
- Binomial p-value P[X ≥ 7 | Bin(11, 0.0990)] ≈ 2.14 × 10⁻⁵ (strict-non-trivial claim).
- The substrate's σ-permutation has cycle structure (0)(3)(8)(9)(1 7 6 5 4 2); σ² has order 3 on the σ-cycle.

**COMPUTED:**
- Each M_22 irrep dimension factored; classification table verified against ATLAS character table.
- |B_385| via direct enumeration in sympy.
- Steiner-system parameters of S(3, 6, 22): (v, b, k, r, λ_2, λ_3) = (22, 77, 6, 21, 5, 1) verified by formula.

**STRUCTURAL RHYME:**
- The substrate-prime distinction {2, 3, 5, 7, 11} matches the prime divisors of |M_22| with the same multiplicities. The non-genericity theorem makes this match quantitative.
- 231 = 3·7·11 is the unique M_22 irrep dimension whose factorization is squarefree-three-distinct-substrate-primes (no 2, no 5). The factorization-pattern uniqueness identifies 231 as the most substrate-prime-saturated dimension.
- Mathieu moonshine (Eguchi-Ooguri-Tachikawa 2011 for M_24) connects sporadic-group character tables to elliptic-genus generating functions; the present paper's non-genericity is arithmetic, not analytic, and does not connect to the moonshine literature.

**OPEN:**
- Structural origin of the non-genericity: is it a shadow of an M_22-substrate identification, or a deep arithmetic coincidence?
- M_22 action on the substrate respecting the magma operations (the substrate has only 10 elements, far fewer than |Ω_22| = 22).
- Extension to other Mathieu groups (M_11, M_12, M_23, M_24) — same substrate-prime distinction, different irrep tables.
- Tighter null model: condition on the sum-of-squares constraint Σ d_i² = 443520 instead of uniform on [1, 385].
- σ-orbit as a distinguished hexad of S(3, 6, 22): a representation-theoretic embedding question, separate from the non-genericity theorem.

---

## §5 — Updated lens-ownership paragraph

> *Lens and substrate.* The substrate (Z/10Z, σ, W) and its distinguished prime set {2, 3, 5, 7, 11} are defined in the companion paper J02 (Sanders + Gish 2026, *Algebraic Combinatorics*). The roles of each prime are stated in §3 of the present paper from intrinsic substrate data — CRT residue characteristics, σ²-cycle order, HARMONY-index appearance, threshold T* = 5/7 numerator/denominator, and the wobble fraction's 11-prolongation. The non-genericity theorem (Theorem 4.1) is a quantitative claim about M_22's irrep-dimension factorization profile relative to the substrate prime monoid; it does not depend on the deeper TIG-framework interpretation of the substrate. A reader of the *Monthly* can verify the theorem from §3's intrinsic-prime definitions and the §4 binomial-tail computation, without consulting J02.

---

## §6 — Recommended retitle / retarget

**Old title:** "Mathieu M_22 Substrate-Prime: Order-Factorization Coincidences."
**New title (recommended):** "A Non-Generic Concentration of Mathieu M_22's Irreducible Representation Dimensions in a Five-Prime Substrate Monoid." (Or the original title kept, with the abstract revised to lead with the non-genericity theorem rather than the catalog.)

**Old venue:** *American Mathematical Monthly* (referee verdict: Major revision).
**New venue (recommended):** **Keep at *American Mathematical Monthly*.** Rationale:
- The referee explicitly recommends Path A revision-and-resubmission to *Monthly*: "If these are addressed, the resulting paper would be a 4-6 page expository note suitable for the *Monthly* — with a tighter, sharper claim than the present six-item catalog."
- Path A's content (one corrected, computed coincidence with a clean null-model test) fits *Monthly*'s scope and length norms exactly.
- The corrected count + null-model p-value is a quantitative, expository number-theory result of the kind *Monthly* publishes regularly.

**Backup venue:** *Mathematical Intelligencer* (less stringent expository bar; same general scope).

**Author block:** Sanders + Gish (per AUTHOR_LANES_v2.md). Single block, two addresses, no Mayes (the README's "Sanders + Gish + Mayes" is a transcription error per the cover letter).

**Companion citations:**
- J02 (Joint Closure / 4-core paper, *Algebraic Combinatorics*) — cite for substrate (Z/10Z, σ, W) and the substrate-prime origin.
- ATLAS of Finite Groups (Conway et al. 1985), Conway-Sloane 1999, Cameron 1999, Wilson 2009 — textbook references for M_22, S(3,6,22), and the irrep table.
- Diaconis 1988 — added per referee S6; canonical *Monthly*-level reference for finite-group representations.
- Eguchi-Ooguri-Tachikawa 2011 — kept as ambient context for Mathieu moonshine (referee §6).

**Length target:** 4-6 pages in amsart 11pt.
