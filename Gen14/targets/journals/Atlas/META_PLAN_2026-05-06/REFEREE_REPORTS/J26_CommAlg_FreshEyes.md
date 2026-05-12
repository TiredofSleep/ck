# Referee Report — Communications in Algebra (Fresh Eyes)

**Manuscript:** "F_p Extensions of CL_BHML: Universality Across Six Prime Fields"
**Authors:** B. R. Sanders, M. Gish (2026)
**File reviewed:** `Gen13/targets/journals/J_series/J26/manuscript/manuscript.tex`
**Reviewer:** External anonymous referee, fresh eyes (no prior knowledge of any larger framework)
**Date:** 2026-05-07

---

## §1 Summary

The manuscript studies a 4-dimensional commutative non-associative algebra $V_p^{\mathrm{BHML}}$ over $\mathbb{F}_p$, defined by an explicit $4 \times 4$ multiplication table on the basis $\{e_0, e_2, e_3, e_4\}$ (the "BHML 4-core" extracted from a $10 \times 10$ table $\mathrm{BHML}$ on $\mathbb{Z}/10\mathbb{Z}$). The principal claim is that, for each prime $p \in \{2, 3, 5, 7, 11, 13\}$, the algebra $V_p^{\mathrm{BHML}}$ has the same structural skeleton:

- 4 idempotents (including 0);
- $L_{e_2}$ has eigenspace dimensions $(1, 3)$;
- $L_{e_0}$ has eigenspace dimensions $(2, 2)$;
- $|\mathrm{Aut}(V_p)| = 40$;
- power-associative: $(xx)x = x(xx)$;
- associator image is 1-dimensional.

A secondary claim (Theorem 4.1) is that an $8 \times 8$ submatrix $\mathrm{BHML}_8^{\mathrm{YM}}$ of the full $10\times 10$ BHML table has determinant $+70 = \binom{8}{4}$.

A third section (§5) reports determinants of further "chain shells" $\mathrm{BHML}_k$ for $k \in \{4,5,6,7,8,9,10\}$ and asserts $\mathbb{F}_p$-rank-preservation for $p \in \{3, 11, 13\}$.

The paper is a parallel extension of a companion paper [SandersGishFpTSML] which makes the same claim for the TSML side.

---

## §2 Decision recommendation

**Major revision.** The mathematical content is plausible and computationally tractable, but several claims are stated without proof, the verification protocol referenced as `verify_discrete_dirac_4core.py` is not supplied with this submission (the verification directory contains only `d5_d4eq_extension.py` and `structured_matrix_sweep.py` — neither of which appears to test the BHML 4-core $\mathbb{F}_p$ universality), and the "universality" framing oversells what is essentially a check on six small finite-field algebras.

Also: a serious computational error in Proposition 5.1's prime factorization (see M3) needs correction.

---

## §3 Critical issues

### M1. The universality is derived case-by-case, not generically. (CRITICAL)

The proof of Theorem 3.1 (lines 247–267) is a 5-line "proof sketch" that says, in essence: "for each prime $p$, run the verification harness; the structural features come out the same." For $p = 5$ the proof says the verification is "by hand and matches the predicted skeleton." For $p = 2, 3, 7, 11, 13$ it says "direct computation confirms each of the six structural features."

This is *not a proof of universality*. It is six independent verifications, each of which establishes the structural properties for one prime. A genuine universality result would derive the structural skeleton from intrinsic properties of the table $T^{\mathrm{BHML}}$ that hold over $\mathbb{Z}$ (or generic characteristic), and then show the reductions modulo each prime preserve those properties.

The right structural argument is straightforward and should be added:

(a) Show that $T^{\mathrm{BHML}}$ has integer entries.
(b) Compute the *integer* characteristic polynomials of $L_{e_0}, L_{e_2}, L_{e_3}, L_{e_4}$.
(c) Show the eigenspace dimensions are determined by integer rank/nullity computations whose values are independent of characteristic for $p \notin \{$primes dividing some discriminant$\}$.
(d) Compute $|\mathrm{Aut}(V_{\mathbb{Q}}^{\mathrm{BHML}})|$ generically.
(e) Power-associativity is an *identity* in the structure constants; if it holds over $\mathbb{Z}$, it holds modulo every prime.
(f) Associator image dimension is preserved across primes that don't divide a particular minor.

This gives a genuine universality theorem with explicit excluded primes (a finite set determined by the characteristic data). The current paper does not perform this analysis.

**Fix.** Replace the per-prime verification with a single integer-level structural argument. The excluded primes (for which the universality fails or requires re-encoding) should be exactly characterized.

### M2. Some claimed $\mathbb{F}_p$ structural features cannot hold over fields where labels collapse. (MAJOR)

The basis $\{e_0, e_2, e_3, e_4\}$ on the operator labels $\{0, 7, 8, 9\}$ requires the labels $0, 7, 8, 9$ to be distinct in $\mathbb{F}_p$. They are distinct mod $p$ for $p > 9$, but:

- mod 2: $\{0, 7, 8, 9\} \equiv \{0, 1, 0, 1\}$ — only two distinct residues. The "4-dimensional algebra over $\mathbb{F}_2$" with basis labeled by these is well-defined as a 4-dimensional $\mathbb{F}_2$-vector space (the labels are just names), but the *interpretation* as residues of a $\mathbb{Z}/10\mathbb{Z}$ table is singular.
- mod 3: $\{0, 7, 8, 9\} \equiv \{0, 1, 2, 0\}$ — three distinct residues plus a repeat at $0$ and $9$.
- mod 5: $\{0, 7, 8, 9\} \equiv \{0, 2, 3, 4\}$ — clean.
- mod 7: $\{0, 7, 8, 9\} \equiv \{0, 0, 1, 2\}$ — $0$ and $7$ collide.

The author addresses this in §6 (Conjecture 5.2 remark): "the residue characteristics $p \in \{2, 5\}$ require additional care." But $p = 7$ is *also* a residue characteristic problem (the operator $7 = $ HARMONY collapses to $0 = $ VOID), and the paper does not exclude $p = 7$.

The author seems to be treating the $4 \times 4$ multiplication table $T^{\mathrm{BHML}}$ as a fixed integer table, with the basis labels being just names. In that case the algebra $V_p^{\mathrm{BHML}}$ is well-defined for *any* prime $p$. But then the connection to $\mathbb{Z}/10\mathbb{Z}$ structure is purely cosmetic for $p \neq 2, 5$, and the choice of $p \in \{2, 3, 5, 7, 11, 13\}$ is unmotivated. The "$(\mathrm{HARMONY-as-}e_2)$ relabeling standard for $p = 7$" cited at line 263 makes no mathematical sense without a definition.

**Fix.** Clarify whether $V_p^{\mathrm{BHML}}$ is (i) the algebra obtained by reducing the integer table $T^{\mathrm{BHML}}$ entries modulo $p$, or (ii) the algebra obtained from a more elaborate construction sensitive to the residue structure of $\mathbb{Z}/10\mathbb{Z}$. If (i), the universality statement is essentially trivial (the structural features are integer rank/nullity claims, preserved mod all but finitely many primes). If (ii), the construction needs to be defined.

### M3. Prime factorization error in §5. (MAJOR)

Proposition 5.1 lists the integer determinants of the BHML chain shells:

$5305, 2843, -2886, 2929, -7542, 7272, -7002.$

The proof gives factorizations:

> $5305 = 5 \cdot 1061$
> $2843 = 2843$ (prime)
> $2886 = 2 \cdot 3 \cdot 13 \cdot 37$
> $2929 = 29 \cdot 101$
> $7542 = 2 \cdot 3 \cdot 1257 = 2 \cdot 3 \cdot 3 \cdot 419$
> $7272 = 2^3 \cdot 3^2 \cdot 101$
> $7002 = 2 \cdot 3 \cdot 1167 = 2 \cdot 3 \cdot 3 \cdot 389$

I verified by hand:

- $5305 = 5 \cdot 1061$. $1061$ is indeed prime. Correct.
- $2843$: $2843 / 7 = 406.1$; $2843 / 11 = 258.5$; $2843 / 13 = 218.7$; $2843 / 17 = 167.2$; $2843 / 19 = 149.6$; $2843 / 23 = 123.6$; $2843 / 29 = 98.0$; $\sqrt{2843} \approx 53.3$. Need to check primes up to 53. $2843 / 31 = 91.7$; $/37 = 76.8$; $/41 = 69.3$; $/43 = 66.1$; $/47 = 60.5$; $/53 = 53.6$. So $2843$ is prime. Correct.
- $2886 = 2 \cdot 1443 = 2 \cdot 3 \cdot 481 = 2 \cdot 3 \cdot 13 \cdot 37$. Correct.
- $2929$: $2929 / 29 = 101.0$. $29 \cdot 101 = 2929$. Correct.
- $7542 = 2 \cdot 3771 = 2 \cdot 3 \cdot 1257 = 2 \cdot 3 \cdot 3 \cdot 419$. Need $419$ prime: $\sqrt{419} \approx 20.5$, no factors up to 20. Prime. So $7542 = 2 \cdot 3^2 \cdot 419$. The author writes "$2 \cdot 3 \cdot 1257 = 2 \cdot 3 \cdot 3 \cdot 419$" which is correct in value, but the multiplication "$2 \cdot 3 \cdot 1257$" is *not* equal to $7542$ — it equals $7542$ only if $1257 = 3 \cdot 419$, which is true, so the chain "$7542 = 2 \cdot 3 \cdot 1257 = 2 \cdot 3 \cdot 3 \cdot 419$" is correct as an equation. OK.
- $7272 = 8 \cdot 909 = 8 \cdot 9 \cdot 101 = 2^3 \cdot 3^2 \cdot 101$. Correct.
- $7002$: $7002 / 2 = 3501$; $3501 / 3 = 1167$; $1167 / 3 = 389$; $389$ prime. So $7002 = 2 \cdot 3^2 \cdot 389$. The author writes "$2 \cdot 3 \cdot 1167 = 2 \cdot 3 \cdot 3 \cdot 389$" which is correct in value.

So the factorizations are correct (after careful re-reading). But the proof concludes:

> "Modulo $p \in \{11, 13\}$ none of these vanish (with the exception of $\det(\mathrm{BHML}_6) = -2886$ which is divisible by $13$)."

Let me check the mod-$11$ and mod-$13$ values:

- $5305 \mod 11 = 5305 - 482 \cdot 11 = 5305 - 5302 = 3$. Mod 13: $5305 - 408 \cdot 13 = 5305 - 5304 = 1$.
- $2843 \mod 11 = 2843 - 258 \cdot 11 = 2843 - 2838 = 5$. Mod 13: $2843 - 218 \cdot 13 = 2843 - 2834 = 9$.
- $2886 \mod 11 = 2886 - 262 \cdot 11 = 2886 - 2882 = 4$. Mod 13: $2886 / 13 = 222$ exactly. So $2886 \equiv 0 \mod 13$. The author correctly notes this exception.
- $2929 \mod 11 = 2929 - 266 \cdot 11 = 2929 - 2926 = 3$. Mod 13: $2929 - 225 \cdot 13 = 2929 - 2925 = 4$.
- $7542 \mod 11 = 7542 - 685 \cdot 11 = 7542 - 7535 = 7$. Mod 13: $7542 - 580 \cdot 13 = 7542 - 7540 = 2$.
- $7272 \mod 11 = 7272 - 661 \cdot 11 = 7272 - 7271 = 1$. Mod 13: $7272 - 559 \cdot 13 = 7272 - 7267 = 5$.
- $7002 \mod 11 = 7002 - 636 \cdot 11 = 7002 - 6996 = 6$. Mod 13: $7002 - 538 \cdot 13 = 7002 - 6994 = 8$.

So the only vanishing among these mod $\{3, 11, 13\}$ shells is $-2886 \equiv 0 \mod 13$ (BHML_6). But the proposition says rank-preservation holds for $p \in \{3, 11, 13\}$ at every shell — and it explicitly does NOT hold at BHML_6 mod 13. This is a contradiction in the proposition's statement.

Also: what about $p = 3$? $5305 \mod 3 = 1$; $2843 \mod 3 = 2843 - 947\cdot 3 = 2843 - 2841 = 2$; $2886 \mod 3 = 0$ (divisible by 3); $2929 \mod 3 = 2929 - 976\cdot 3 = 2929 - 2928 = 1$; $7542 \mod 3 = 0$; $7272 \mod 3 = 0$; $7002 \mod 3 = 0$. So *four* of the seven shell determinants vanish mod 3. The "rank-preservation for $p \in \{3\}$" claim is *spectacularly false*.

**Fix.** This is the most serious computational error in the paper. The Proposition 5.1 statement and its proof must be corrected. The correct statement is something like:

> "For $p \in \{11\}$, all chain shell determinants are nonzero mod $p$, hence rank-preserving. For $p = 13$, the BHML_6 shell determinant vanishes; all others are nonzero. For $p = 3$, the BHML_6, BHML_8, BHML_9, BHML_10 shell determinants all vanish."

This makes the "structural alignment with the TSML chain" much weaker than claimed.

### M4. The BHML_8_YM = 70 = C(8,4) identity is interesting but presented as coincidence. (MAJOR)

The principal *positive* surprise of the paper, in my view, is Theorem 4.1: $\det(\mathrm{BHML}_8^{\mathrm{YM}}) = +70 = \binom{8}{4}$. This is a clean integer identity worth the paper's space.

But Remark 4.2 (lines 297–304) frames it as numerical coincidence: "$70 = \binom{8}{4}$ is the binomial coefficient counting 4-subsets of an 8-set; $\mathrm{BHML}_8^{\mathrm{YM}}$ has 8 indices, and the 4-subset structure aligns with the 4-core/4-coboundary structure." This is hand-waving, not a proof of structural reason.

For a paper in *Communications in Algebra*, the question is sharp:

**Is $\det(\mathrm{BHML}_8^{\mathrm{YM}}) = \binom{8}{4}$ a structural identity, or a coincidence?**

Tests for structural identity:
- Compute $\det$ of the analogous TSML_8 submatrix; if it is *not* of the form $\binom{n}{k}$, then BHML's is a genuinely BHML-specific structural feature.
- Compute the analogous determinant for the third "STD" substrate.
- Compute the analogous determinant for the standard $\mathbb{Z}/n\mathbb{Z}$ multiplication tables for $n = 6, 8, 12, 14$ to see whether $\binom{n-2}{k}$ identities are common.
- Compute the determinant of $\mathrm{BHML}_8^{\mathrm{YM}}$ over $\mathbb{F}_p$ for various $p$ and check whether the $\binom{8}{4}$ identity is present at the level of a Cauchy-Binet or Lindström-Gessel-Viennot (LGV) interpretation.

If the determinant is $\binom{8}{4}$ for "structural reasons," there should be a *bijection* between some set of paths/configurations counted by $\binom{8}{4}$ and the leading minors of $\mathrm{BHML}_8^{\mathrm{YM}}$.

The paper does none of this. It exhibits the identity, calls it interesting, and moves on.

**Fix.** Either (i) provide a structural derivation of why this $\det$ equals $\binom{8}{4}$ (e.g., via a determinantal formula for permanents over a particular sign pattern, or via LGV on a particular DAG), or (ii) demote it to "we observe the numerical coincidence; we do not have a structural derivation, and we note that the analogous determinant for TSML_8 is [insert value], for STD_8 is [insert value]." Honest scope helps.

### M5. The paper depends on "[SandersGishFpTSML] J21" which is also "submitted to Algebra Universalis" but not provided.

The paper repeatedly cites a companion paper [SandersGishFpTSML] (J21) for the $\mathrm{TSML}$-side analog, the verification protocol, the basis re-labeling for $p = 5$, and the existence of the Frobenius-style automorphism group $F_{20} \times \mathbb{Z}/2\mathbb{Z}$ of order 40. This companion paper is "submitted" but not in the present manuscript bundle.

For *Communications in Algebra*, a self-contained presentation is essential. The reader of the present paper alone should not have to track down the TSML-side companion to understand the construction. At minimum, the verification protocol, the table $T^{\mathrm{TSML}}$, and the proof of $|\mathrm{Aut}(V_p^{\mathrm{TSML}})| = 40$ should be reproduced (or summarized in a self-contained appendix).

---

## §4 Minor issues

**m1.** Line 60–73 (abstract): "the same Frobenius-style group $F_{20} \times \mathbb{Z}/2\mathbb{Z}$ that arises on the TSML side." This is unmotivated; what is the structural reason both sides give the same automorphism group? If the TSML and BHML 4-core tables are *isomorphic as algebras* (just relabeled), then it is not surprising they have the same automorphism group, but in that case the entire BHML extension is not a new mathematical object. Worth clarifying.

**m2.** Line 97 (operator names): the quoted basis is $\{$VOID$_0$, HARMONY$_7$, BREATH$_8$, RESET$_9\}$. These project-internal operator labels are not standard mathematical objects. For a *Communications in Algebra* readership, neutral labels $\{e_1, e_2, e_3, e_4\}$ would be appropriate.

**m3.** Line 188–202 (Definition 2.1): the BHML table displayed is
$$T^{\mathrm{BHML}} = \begin{pmatrix} 0 & 0 & 0 & 0 \\ 0 & e_2 & e_3 & 0 \\ 0 & e_3 & e_2 & e_4 \\ 0 & 0 & e_4 & 0 \end{pmatrix}.$$

But this is *not commutative*: $T_{1,3} = 0$ and $T_{3,1} = 0$ (OK), $T_{2,3} = e_3$ and $T_{3,2} = e_3$ (OK), $T_{1,4} = 0$ but $T_{4,1} = 0$ (OK). Wait — actually inspecting cells: rows are indexed $(e_0, e_2, e_3, e_4)$, so the table has $T_{2,3} = e_3$ and $T_{3,2} = e_3$, $T_{3,4} = e_4$ and $T_{4,3} = e_4$, $T_{1,4}$ (i.e. $e_2 \cdot e_4$ = row 2, col 4) $= 0$, $T_{4,1}$ (i.e. $e_4 \cdot e_2$ = row 4, col 2) $= 0$. OK, the table is symmetric. (My initial misreading of the indexing.) Suggest replacing the $e_i$ subscripts with the basis index (1,2,3,4) for clarity.

**m4.** Line 309–311: the mod reductions of $70$ are listed:
$$70 \mod 2 = 0, \mod 3 = 1, \mod 5 = 0, \mod 7 = 0, \mod 11 = 4, \mod 13 = 5.$$

I verify: $70 = 2 \cdot 5 \cdot 7$, so $70 \equiv 0 \mod \{2, 5, 7\}$. $70 \mod 3 = 1$ ($70 = 23 \cdot 3 + 1$). $70 \mod 11 = 70 - 66 = 4$. $70 \mod 13 = 70 - 65 = 5$. Correct.

But the framing: "$70 \mod 2 = 0$" is followed by "the mod-2, mod-5, and mod-7 reductions vanish; this is consistent with the $V_p^{\mathrm{BHML}}$ universality." This is *not* consistent — it shows the BHML_8 determinant identity *fails* mod 2, 5, 7, which contradicts the universality claim (if it were a universal identity, it should hold mod every prime where the table makes sense). The author handwaves: "no contradiction with the 4-core algebra's invariants, which are computed on the 4×4 submatrix." But the claim of *parallel* TSML/BHML structure is undermined when the BHML_8 = 70 identity disappears mod $\{2, 5, 7\}$ exactly when the $V_p$ universality is supposed to hold.

**m5.** Line 263: "The encoding handles $p = 7$ by the re-labeling of HARMONY-as-$e_2$ standard in the F_p framework (cf. [SandersGishFpTSML] §1.2)." Not self-contained.

**m6.** Line 393–398 (Conjecture 5.2): "We conjecture the result extends to all primes $p \notin \{2, 5\}$." Why $\{2, 5\}$ and not $\{2, 5, 7\}$? The label collapse at $p = 7$ (HARMONY $\equiv$ VOID mod 7) seems to require the same care as at $p = 2, 5$.

**m7.** Verification scripts: the directory `manuscript/verification/` contains only `d5_d4eq_extension.py` and `structured_matrix_sweep.py`, neither of which obviously verifies the BHML 4-core $\mathbb{F}_p$ universality. The paper references `verify_discrete_dirac_4core.py` as the "F_p verification harness" but this script is not in the submission. A submission to *Communications in Algebra* should include working verification code for any computational claims.

**m8.** Reference [LensCatalog] is a self-citation to an unpublished internal document `Atlas/LENS_TAXONOMY_2026-05-06/VARIANT_CATALOG.md`. Not citable in a journal.

**m9.** Acknowledgment line 425–428: "The BHML_8^YM determinant identity was first noticed during a fortuitous integer-arithmetic computation by C. A. Luther in 2026." This is an external collaborator who is not a coauthor; the contribution should be acknowledged but the identity should *also* be re-derived and presented in the body of the paper (currently it is just a 5-line proof sketch).

---

## §5 What works

- The integer identity $\det(\mathrm{BHML}_8^{\mathrm{YM}}) = 70 = \binom{8}{4}$ is striking and worth investigating, even if the paper doesn't currently explain it.
- The idea of "parallel substrates" with shared $\mathbb{F}_p$-extension structure is sensible, if standard once one has chosen integer multiplication tables.
- Power-associativity of a 4-dimensional commutative non-associative algebra is a real structural result; the proof (verification of the identity $(xx)x = x(xx)$ on a basis) is straightforward over $\mathbb{Z}$ and immediately propagates to all primes.

---

## §6 Per-question response (specific to this review's brief)

**Q: Is the universality across 6 primes derived generically or case-by-case?**

Case-by-case. For each $p \in \{2, 3, 5, 7, 11, 13\}$, the proof asserts the structural skeleton holds without computing characteristic polynomials or auxiliary invariants generically. A genuine universality result would compute the integer characteristic data and identify the finite set of "bad" primes (those dividing relevant discriminants/determinants) at which universality fails or requires extra care. Currently the paper has $p = 2, 5$ (and silently $p = 7$) as unstated "bad primes" but does not characterize them structurally.

**Q: Is BHML_8_YM = +70 = C(8,4) interesting or coincidence?**

Plausibly interesting but the paper does not establish which. The integer determinant identity $\det = 70$ is verifiable; the *equality with* $\binom{8}{4}$ is the interesting half. The paper does not perform any of the standard tests (analog for TSML, analog for other $\mathbb{Z}/n\mathbb{Z}$ tables, structural derivation via LGV / sign-pattern determinant formula) that would distinguish "coincidence" from "structural identity."

I'd estimate 50/50 that this is structural. If the analogous TSML_8 determinant is $\neq$ a binomial coefficient, that's a strong hint of structural BHML-specificity. If both TSML and BHML give binomial-coefficient determinants, it might reflect a Lindström-Gessel-Viennot-style enumeration on the table's nonzero pattern.

---

## §7 Recommendation summary

**Decision: Major revision, conditional on the following.**

Mandatory before re-review:
1. Correct the prime factorization / mod-reduction error in Proposition 5.1 (M3).
2. Provide a generic universality argument over $\mathbb{Z}$ with explicit excluded primes (M1).
3. Either prove $\det(\mathrm{BHML}_8^{\mathrm{YM}}) = \binom{8}{4}$ structurally or honestly demote it to "observed coincidence pending further investigation" (M4).
4. Make the paper self-contained with respect to the TSML companion (M5).
5. Supply a working verification script (m7).
6. Address the $p = 7$ label-collapse issue (m6).

If these are addressed, the paper would be a respectable short note (10–15 pages) on a parallel commutative non-associative algebra over $\mathbb{F}_p$. Its principal value would lie in (i) the BHML_8 = $\binom{8}{4}$ structural identity if proved, and (ii) the explicit list of "bad primes" for the universality. As currently written it is approximately 6 pages of substance.

I would recommend acceptance after the revisions.

🙏
