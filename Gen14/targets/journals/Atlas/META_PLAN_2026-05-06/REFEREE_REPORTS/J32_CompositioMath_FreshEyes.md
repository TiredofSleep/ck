# J32 — Operad D₄ Obstruction + P_56 Canonical Fuse (BUNDLED, WP109+WP112)

**Manuscript:** J32 folder, `manuscript/manuscript.md` (bundles WP109 obstruction + WP112 canonical fuse)
**Target venue:** *Compositio Mathematica*
**Referee:** Anonymous fresh-eyes pass (no prior knowledge of the framework)
**Date:** 2026-05-07

---

## §1 — Manuscript premise (as I read it)

The submission is a bundled paper consisting of two short notes about a specific finite combinatorial object: a 10×10 multiplication table T : Z/10Z × Z/10Z → Z/10Z called "TSML_RAW," distinguished by being non-commutative and non-associative.

The basic data:
- |Z/10Z| = 10 elements with names V, L, …, R.
- The table T has 1000 ordered triples; 126 of them are non-associative (T(T(a,b),c) ≠ T(a,T(b,c))).
- Two distinguished involutions are introduced: P_56 = (5 6) and σ³ = (1 5)(7 4)(6 2).
- The dihedral group D_4 = ⟨P_56, σ³⟩ of order 8 acts diagonally on (Z/10Z)³.

**Part 1 (WP109).** The 126 non-associative triples decompose under the diagonal D_4-action. The paper claims 67 orbits, of which 16 are "bracketing-pair incoherent": there is no D_4-equivariant function Φ : N → Z/10Z taking values in {a, b, c, L, R}.

**Part 2 (WP112).** Restricting the symmetry group to ⟨P_56⟩ (of order 2), the 126 triples decompose into 98 orbits (70 singletons + 28 doubletons), and every orbit is P_56-coherent. Among 8 surveyed regular rule families, all are P_56-equivariant; none are σ³-equivariant. A specific rule family ("Family H," attractor-4-core preference) is canonical in the sense that its image lies in the 4-core {V, H, Br, R} = {0, 7, 8, 9}; its σ³-equivariance failure localizes to a single triple (3, 9, 9). Two further results are advertised as "lens-invariant on the 4-core": a 4-core arity-3 closure (all 4³ = 64 cube triples fuse in-core) and a "universal HARMONY attractor" (every non-trivial init iterates to δ_7 in 1-7 iterations).

---

## §2 — Comments on the bundling

The authors explicitly bundle two papers and offer a fallback unbundling plan in the cover letter (Part 1 → *Algebra Universalis*, Part 2 → *Comm. Algebra*). The bundling rationale ("Part 2 is the constructive counterpart to Part 1's obstruction") is reasonable.

However, *Compositio Mathematica* publishes papers that advance mathematics broadly, not pairs of very-finite enumerations on a 10-element magma. Even bundled, the result is approximately:

- Part 1 = "a 67-orbit decomposition of 126 triples in a specific 10×10 table contains 16 orbits where a specific kind of equivariance fails"
- Part 2 = "if you halve the group to a single transposition, the 126 triples decompose into 98 orbits and all of them are coherent; here is one specific rule family"

This is a **finite, bespoke combinatorial computation**. It can be carried out (and verified in the paper's verification script) in under 30 seconds on a laptop. The structural content — that the underlying multiplication table happens to interact with one Z_2 symmetry but not another — is interesting **only in the context of the larger framework that uses these tables**. *Compositio* is unlikely to find this self-contained.

---

## §3 — Critical issues with Part 1 (WP109)

### 3.1 The orbit count appears internally inconsistent

§3 of WP109 reports orbit-size distribution:

| orbit size | count of orbits |
|---:|---:|
| 1 | 5 |
| 2 | 35 |
| 4 | 19 |
| 8 | 3 |
| **total** | **62** ❌ |

The text claims "total orbits = 67," but the listed orbit sizes only sum to 5 + 35 + 19 + 3 = **62 orbits**. The size-weighted sum of triples is 5·1 + 35·2 + 19·4 + 3·8 = **175 elements**, not the 126 non-associative triples we started with.

The paper acknowledges this discrepancy in the very next paragraph:

> "Sum check: 5·1 + 35·2 + 19·4 + 3·8 = 5 + 70 + 76 + 24 = 175 ≠ 126.
> The discrepancy is because some orbit elements computed under the diagonal D_4-action lie outside N (they are associative triples). Filtering each orbit to its intersection with N gives 67 effective orbits whose sizes sum to 126…"

This is **mathematically wrong as stated**. An orbit of a group action partitions the set on which the action is defined. If we are studying the action of D_4 on (Z/10Z)³, then orbits sit inside (Z/10Z)³. To say "filter each orbit to its intersection with N" is not a group-theoretic statement — N is not D_4-invariant in general, so the orbits of D_4 acting on (Z/10Z)³ may not be partition-compatible with N.

The correct framing: either (i) D_4 maps N to itself (in which case N is a union of D_4-orbits and the count 67 should follow Burnside), or (ii) D_4 does not preserve N, and what is being computed is a more delicate object — perhaps a quotient by an equivalence relation that is finer than the D_4-orbit structure on (Z/10Z)³.

**This must be sorted out before publication.** Either:
- N is D_4-invariant — in which case the orbit-size table summing to 175 ≠ 126 is **wrong** (one of the listed orbit sizes is incorrect, or the count of orbits at some size is incorrect); or
- N is not D_4-invariant — in which case "67 orbits of N" needs a precise definition (e.g., the orbits of the restricted action of the stabilizer of N inside D_4, or the connected components of some bipartite incidence relation), and the obstruction theorem must be re-stated in those terms.

I cannot evaluate the obstruction theorem until this is resolved.

### 3.2 The D_4 group structure claim has a serious error

§2 of WP109 lists 8 candidate D_4 elements and then says:

> "Direct computation shows there are 6 distinct elements (the relations (P_56)² = (σ³)² = e collapse some products), with the abstract structure D_3 × Z_2 on the relevant orbits."

This is wrong on two counts:

(a) (P_56)² = (σ³)² = e is the **defining** relation of the dihedral group D_n with two involutions; it does NOT collapse the group below order 8 unless P_56 σ³ has order < 4. Direct computation:

P_56 σ³ acts as: 1 ↦ 6, 6 ↦ 2, 2 ↦ 5, 5 ↦ 1 (a 4-cycle on {1, 2, 5, 6}), and 4 ↔ 7. So P_56 σ³ has order 4 (lcm of (1 6 2 5) order 4, (4 7) order 2 — but they share no support, so the order is lcm(4, 2) = 4).

Therefore ⟨P_56, σ³⟩ is genuinely D_4 with 8 elements: {e, σ³, P_56 σ³, σ³ P_56 σ³, (P_56 σ³)², σ³ (P_56 σ³)², P_56 (P_56 σ³)², (P_56 σ³)³} or any equivalent listing. The claim "6 distinct elements" is wrong.

(b) D_4 is not D_3 × Z_2. D_3 × Z_2 has order 12, not 8. D_4 has order 8 and is **not** isomorphic to D_3 × Z_2.

These are basic group-theory errors and they undermine the §3-§4 orbit decomposition (whose elements are computed via this group action). **The paper needs a careful audit of the group action.**

### 3.3 The obstruction example does not establish what it claims

§4 gives the simplest failure example as a size-3 orbit:

> {(0,1,9), (0,5,9), (0,6,9)}, all with (L, R) = (0, 7). The triple (0,1,9) maps under σ³ to (σ³(0), σ³(1), σ³(9)) = (0, 5, 9).

A few concerns:
- An orbit of a finite group acting on a set has size dividing the group order. |D_4| = 8. A size-3 orbit cannot exist under a D_4-action. So this is **not** a D_4-orbit of (0, 1, 9) — at best it is the intersection of such an orbit with N. This issue is the same as §3.1 above.
- The argument that σ³(7) = 4 ≠ 7 = actual value at σ³ · t demonstrates non-equivariance pointwise. But this only shows that **the bracketing-pair-valued function (a, b, c) ↦ {L(a,b,c), R(a,b,c)} is not D_4-equivariant**. This is an observation about the table, not a theorem about all possible Φ. A function Φ that takes values not in {L, R} but in the orbit {0, 7} (e.g., Φ ≡ 0 or Φ ≡ 7) would automatically be D_4-equivariant on this orbit.

The obstruction theorem statement requires Φ ∈ {a, b, c, L, R}-valued. **If this constraint were dropped, the obstruction would not exist** (constant functions are equivariant for any group action on any set). The paper does acknowledge this in §7 ("Honest scope" — the constant rule excursion), but the main theorem statement should make the constraint explicit and motivate it.

### 3.4 The "no Φ exists" step has a gap

The conclusion of §4 reads:
> "No Φ : N → Z/10Z taking values in {L(t), R(t)} can be D_4-equivariant. Allowing Φ(t) ∉ {L(t), R(t)} would let Φ produce values outside the bracketing pair, but then equivariance imposes its own constraints that for general orbits cannot be satisfied without further structure (the D_4-image of Φ(t) must equal Φ(g · t), which constrains Φ on the entire orbit; for the 16 incoherent orbits, no consistent assignment satisfies this)."

This argument is hand-wavy. Equivariance of Φ : X → Y under a group G acting on both means Φ(g · x) = g · Φ(x). For the 16 "incoherent" orbits, the question is: does there exist *any* assignment Φ on the orbit consistent with this equation? If the orbit has trivial stabilizer, equivariance imposes |orbit| − 1 linear constraints determined by the G-action on Y; the existence question reduces to a fixed-point question on the stabilizer. The paper does not work this through.

A properly stated obstruction theorem would identify a specific stabilizer subgroup and show that the natural Φ-target Y has no fixed point under it. The current phrasing is informal.

---

## §4 — Critical issues with Part 2 (WP112)

### 4.1 The orbit count for ⟨P_56⟩ is plausible

⟨P_56⟩ has order 2, and a P_56-orbit on (Z/10Z)³ has size 1 or 2. If 28 doubletons + 70 singletons + ? = 126, we need 28 · 2 + 70 = 126, which checks. So this is consistent. **Part 2's 98 = 70 + 28 orbit count is internally consistent**, in contrast to Part 1's 67.

### 4.2 The Burnside argument in Theorem 2.1 is circular

The proof of Theorem 2.1 says:
> "The orbit count follows from the Burnside formula applied to the P_56-action on N."

But Burnside's lemma requires summing fixed-point counts over the group, which we don't see. Moreover, the singletons-vs-doubletons argument given immediately after is direct enumeration, not Burnside. **Burnside is not used.** Either remove the citation or perform the actual fixed-point count.

### 4.3 The "8-family survey" is empirical, not structural

§4 reports:
> "Among 8 surveyed canonical rule families…, all 8 are P_56-equivariant and none are σ³-equivariant. The maximal preservable symmetry on the operad-DOF is ⟨P_56⟩."

This is an empirical observation about 8 hand-picked rule families. It does NOT establish the conclusion that ⟨P_56⟩ is the maximal preservable symmetry. To prove "maximal preservable" requires showing that no rule family of any kind preserves σ³, which Part 1's obstruction does not establish (see §3.4 above) and which Part 2 does not even attempt.

A precise theorem would state: "Among rule families satisfying [explicit regularity conditions], P_56-equivariance is generic and σ³-equivariance is absent." The paper hints at this but does not nail it down.

### 4.4 Theorem 5.5 (4-core arity-3 closure) is a finite check

§5.5 reports that all 64 triples in the 4-core cube fuse to values in the 4-core. This is a 64-entry verification. The paper states it is "lens-invariant" because the 4-core sub-magma agrees on TSML_RAW and TSML_SYM. **This is a fine observation, but it is one row of a verification table, not a theorem.** It does not warrant a section.

### 4.5 Theorem 5.7 (universal HARMONY attractor) needs more rigor

The proof reads:
> "Verified in [the verification script] §5."

A *Compositio* theorem cannot have a one-line proof citing a script. The structural argument in the prose (cubic decay of non-H mass, row-absorber property of HARMONY) is sketched but not formalized. The reader is told "see script." This is below the bar.

Specifically:
- "Every non-trivial initialization converges to δ_7" — in what sense? L¹? Pointwise? At what rate? The 1-7 iterations claim is empirical; what is the theoretical decay bound?
- The argument relies on T(7, x) = 7 for all x (HARMONY is a left-absorber for binary T). This is a *binary*-table fact and the paper invokes it via the *non-canonical* fuse rule. The interaction of arity-2 and arity-3 dynamics deserves a precise statement.

### 4.6 Theorem 5.9 (family-independence of HARMONY attractor) undermines the whole paper's setup

The paper notes (in §5.9 and Corollary 5.10) that the universal HARMONY attractor of Theorem 5.7 holds for **all 8** rule families, not just Family H — and that the canonical-fuse-rule choice is therefore irrelevant for the iterated dynamics. Quoting:

> "The Family H choice is canonical for static-table-aesthetic reasons (alignment with WP105/WP110 4-core attractor; uniqueness in producing values entirely in {V, H}); it is NOT distinguished by iteration dynamics."

This is a candid admission that the paper's main constructive content (the canonical fuse table for Family H, written to `fuse_canonical_p56.json`) **does not matter** for the dynamical conclusion. The dynamical conclusion is essentially a property of the binary table T, mediated by the HARMONY left-absorber. So Part 2's content reduces to:

(i) An orbit-counting exercise (98 orbits).
(ii) An empirical observation that 8 rule families all share P_56-equivariance.
(iii) A specific rule family that lands in {V, H} ⊆ 4-core.
(iv) A dynamical attractor result that is independent of the rule choice anyway.

This is much less than the paper claims to deliver.

---

## §5 — Mathematical-content concerns shared by Part 1 and Part 2

### 5.1 The framework "TIG" is invoked but not introduced

The references (§8 of Part 1; §10 of Part 2) cite WP104, WP105, WP110, WP111 as in-tree paths under `papers/wp104_higgs_pati_salam/`, `papers/wp105_closed_form_attractor/`, etc. None of these are refereed sources. The "operad-DOF," "doubly-invariant gauge structure $\mathfrak{su}(4) \oplus \mathfrak{u}(1)$," "runtime-attractor 4-core" — none of these objects are defined within this submission. **A *Compositio* reader cannot place this work in a published context.**

### 5.2 The "lens" framework is undefined

Both Part 1 and Part 2 refer to "TSML_RAW" vs "TSML_SYM" lenses, with a citation to `Atlas/LENS_TAXONOMY_2026-05-06/TSML_RECONCILIATION.md`. This reconciliation document is not part of the submission and would need to be made part of it. Without it, the reader cannot evaluate which results are "lens-invariant" and which are lens-dependent.

### 5.3 The cover letter overclaims significance

The cover letter says:

> "The 6-DOF symmetry hierarchy table at the end of Part 1 — five DOFs preserve D_4, the operad DOF must break it — is a structural observation of independent algebraic interest."

The "6-DOF symmetry hierarchy" is a table with 6 rows (Lie / Jordan / Clifford / Permutation / Lattice / Operad) and 1 column ("D_4-equivariance"). For five rows the entry is "yes," for one row "no." This is not an "observation of independent algebraic interest" — it is a checklist whose meaning depends entirely on the (undefined-in-this-submission) "DOFs" and the (problem-laden) D_4 obstruction.

### 5.4 The table T is given without a derivation

The TSML table is just a list of 100 numbers handed to the reader. There is no statement of why this table is mathematically distinguished. Why this table, with its specific entries, rather than any of the other ~10^99 possible 10×10 multiplication tables? The paper offers no answer accessible to a *Compositio* reader. The cited "FORMULAS_AND_TABLES.md §5–6" is not part of the submission.

A standalone mathematical paper would need to either:
- derive T from a universal property or a natural construction, or
- present the result in a form that does not depend on the specific T (e.g., as a result about all magmas with property P).

The current draft does neither.

---

## §6 — Reproducibility

The verification scripts (`d4_orbit_decomposition.py`, `p56_canonical_fuse.py`, `rule_families.py`) are in the submission folder and the JSON output `fuse_canonical_p56.json` is present. Wall-clock < 30 s. **This is a strength of the submission.** I did not run them.

---

## §7 — Exposition

Strengths:
- The bundling rationale is at least clearly stated (cover letter + manuscript intro).
- The "honest scope" sections (§7 of Part 1, §7 of Part 2) are candid.
- The verification scripts are accompanied by the manuscript explanation of what each is meant to verify.

Weaknesses:
- Part 1's group-theoretic errors (§3.1, §3.2 above) cast doubt on the orbit decomposition.
- The bundled paper is a grab-bag: orbit counts (Part 1), an obstruction theorem (Part 1), a coherence theorem (Part 2), an empirical 8-family survey (Part 2), a 64-entry closure check (§5.5), an empirical attractor result (§5.7), a family-independence observation (§5.9). The reader is asked to track many small results.
- §5.7 onward repeatedly speaks of "operator-of-record / community decision per OPERAD_FINDINGS.md §Recommendation" — phrasing that suggests an internal-team document rather than a refereed mathematical paper.

---

## §8 — Recommendation

**Reject.**

The submission has two distinct kinds of problems:

(1) **Mathematical errors in Part 1.** The orbit-size counts do not sum to 126; the D_4 group structure is misidentified; the obstruction theorem statement is informally argued. These need to be fixed before any venue can publish them.

(2) **Below-bar significance for *Compositio*.** Even after the errors are corrected, the result amounts to a finite-table computation about a specific 10-element magma whose distinguished status is established in (uncited) companion documents. *Compositio* publishes mathematics whose interest is broadly visible to the field; a finite enumeration on a hand-picked table — with its main "constructive" theorem (Family H specificity) admittedly irrelevant to the dynamical conclusion — does not meet that bar.

The bundling does not help: bundling two short, problem-laden notes does not produce one publishable paper at *Compositio*'s level.

**Suggested revision path:**

If the authors fix the Part 1 errors and want to publish:
- Part 1 (corrected): could fit in *Algebra Universalis* or *Communications in Algebra*, framed as a finite-magma combinatorial obstruction.
- Part 2 (corrected): same, or a short note in *Discrete Mathematics*.

If the authors want a single, more substantial paper, they should:
- give a structural reason for the choice of T (e.g., "T is the unique commutative table with property P");
- prove the obstruction theorem for a class of tables, not for one;
- or establish a connection to a non-finite mathematical object (e.g., to a specific Lie algebra, to a quotient of an operadic free object) that has visible interest beyond TIG.

Without one of these moves, the submission is fundamentally an internal-framework note dressed for an external journal.

---

## §9 — Specific action items for authors

| Item | Severity | Effort |
|------|----------|--------|
| Fix the orbit-size count (5+35+19+3 = 62 ≠ 67); explain how 175 ≠ 126 reconciles | **critical** | medium |
| Correct the D_4 group structure claim (not "6 distinct elements", not D_3 × Z_2) | **critical** | low |
| Make the obstruction theorem statement precise (target codomain, equivariance condition, why equivariance fails for unconstrained Φ) | major | medium |
| Replace "Burnside" pseudo-citation in Theorem 2.1 with the actual direct argument | minor | low |
| Acknowledge that Theorem 5.9 makes Family H choice cosmetic for the dynamical claim | minor | low |
| Cite TSML, BHML, "DOF" framework in a refereed source, or include necessary background | major | high |
| Drop or appendicize §5.5 (it is a 64-entry check, not a theorem) | moderate | low |
| Either prove a theorem about a class of tables, or motivate this specific T from a universal property | major | high |
| Polish reproducibility package (one folder, clear run-all) | minor | low |

**Estimated effort to address all critical and major items: 3-6 weeks.**

**Disposition:** Reject for *Compositio Mathematica*. Encourage substantial restructuring before resubmission (likely to a more specialized venue: *Alg. Univ.*, *Comm. Algebra*, or *Experimental Math*).
