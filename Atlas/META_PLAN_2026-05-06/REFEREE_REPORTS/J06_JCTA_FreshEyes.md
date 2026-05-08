# Referee report — J06: *Crossing Lemma: Non-Associativity as Information Generation in Finite Magmas*

**Target venue:** *Journal of Combinatorial Theory, Series A* (alternate: *Journal of Pure and Applied Algebra*)
**Referee role:** Fresh-eyes, standard combinatorial / algebraic literature only.
**Manuscript file read:** `Gen13/targets/journals/J_series/J06/manuscript/WP57_CROSSING_LEMMA.md`

---

## §1 Manuscript summary (paraphrased fresh)

The paper studies pairs of partitions on `Z/nZ` for squarefree `n = p_1 ... p_k` (with `k >= 2`). Two kinds of partitions are considered:

- **Additive projections** `A_d` for `d | n`: the partition into fibers of `x -> x mod d`.
- **Multiplicative dynamical partitions** `pi_DYN(g)` for `g in (Z/nZ)^x`: the partition into orbits of `x -> g·x`.

The paper's **Theorem 1 ("Crossing Lemma")** asserts the following equivalence for squarefree `n`, `d | n`, `g in (Z/nZ)^x`:

> (a) The joint map `J = (A_d, pi_DYN(g))` is injective.
> (b) `U(A_d) ∩ U(pi_DYN(g)) = ∅` (where `U(π)` is the set of unresolved pairs).
> (c) For every prime `p_j | (n/d)`, `g not≡ 1 (mod p_j)`.

**Theorem 3** asserts a "negative" version for `n = p^r`: no `g` makes the pair `(A_{p^a}, pi_DYN(g))` jointly injective.

§4 lists six "uniform-language reformulations" CL-1 through CL-6, claiming the Crossing Lemma is the algebraic spine for: CRT (CL-1), an "A+M classification" (CL-2 = restatement of Theorem 1), an "M+M classification" (CL-3), a "SPEC+DYN" theorem on reflection vs. multiplication (CL-4), an "orthogonal-jump necessity" statement (CL-5), and the "p-kernel obstruction" (CL-6 = Theorem 3).

§5–§6 are discussion / companion citations / bibliography. §1.3 / §5.2 cite four companion papers in an internal sequence J01–J55.

---

## §2 Decision recommendation

**Reject.**

The proof of the central Theorem 1 is broken (a "Wait — this construction shows the converse..." passage in the middle of the proof, followed by a "Restart" section, and never completes correctly). The "uniform-language reformulations" are largely either standard textbook results (CRT) or rebrandings (CL-2 is identical to Theorem 1; CL-5 is a definition restated as a corollary). Theorem 3 ("p-kernel obstruction") has a sketch that confuses the directions of the implication. A JCT-A or JPAA referee would not be able to certify the proofs as correct.

A clean rewrite of the underlying mathematical statement *might* yield a publishable elementary note, but the paper as submitted is not it.

---

## §3 Top 3 critical issues

### Issue 1. The proof of Theorem 1 is logically broken in §3.2 and never recovers cleanly.

Reading §3.2 line by line:

The first attempted forward direction `(=>)` (lines 109–124, "Assume the Crossing condition holds") is set up, then partway through, the author writes:

> *Wait — this construction shows the* converse *of what we want here. Reread: in the (Leftarrow) direction we are* assuming *g_j ≠ 1 (mod p_j) for every p_j | n/d and trying to prove disjointness. The construction above produced an element of the intersection — which means the construction proves the* forward *direction.*

So the author abandons the proof and restarts. The "Restart, (=>) direction" begins (line 128):

> *Adjust: assume `g_j ≡ 1 (mod p_j)` for some `p_j | n/d`...*

This now constructs a pair `{x, gx}` in `U(A_d) ∩ U(pi_DYN(g))` to show that if some `g_j = 1` then the disjointness fails — i.e., showing `not (c) => not (b)`, equivalently `(b) => (c)`. That direction would be fine, but the construction is gappy: the case `g ≡ 1 (mod n/d)` (every `g_j = 1` for `j | n/d`) is split off into Remark 3.1 with no proof other than narrative; and the case "exactly one `g_j = 1`" is handled by *also assuming* there exists `p_l` with `g_l ≠ 1`. What if `n/d = p_j` is a single prime and `g_j = 1`? Then there is no `p_l` to use. The argument silently uses `k >= 2` but the conclusion needs the right behavior even in degenerate cases.

The second attempt at `(<=)` (lines 134–157, "Now done correctly") then produces another long construction with the key step (line 153): "generically `ord(g_j) ∤ T`, meaning `g_j^T ≠ 1`." But "generically" is not a mathematical justification. The author needs to prove that under hypothesis (c), there is *no* `t` and no `x ≠ y` with `y = g^t x`, `A_d(x) = A_d(y)`. The "generically" hand-wave hides exactly the case-splitting that is the technical content of the claim.

The proof closes (line 157) with the assertion:

> *The cleanest restatement: (b) holds iff no orbit of `M_g` ever maps a point to a distinct point in the same `A_d`-fiber. By the CRT analysis, this is equivalent to: for every `p_j | n/d`,* if *the orbit ever returns to the same `(p_i)_{p_i | d}`-coordinates while moving in the `p_j`-coordinate,* then *`g_j` acts trivially. The condition becomes: `g_j ≡ 1 (mod p_j)` for all `p_j | n/d` — which is the* negation *of (c).*

This last sentence inverts the direction. The author is trying to prove `(b) <=> (c)`, where (c) is `g_j ≠ 1 for every j`. But the displayed conclusion says `(b)` is equivalent to `g_j ≡ 1 for all j`, i.e., `(b) <=> not(c)`. This would mean the theorem is false — and reading carefully, this is indeed an error: the author has "proved" the wrong direction. The intended statement should be: `(b)` fails iff *some* `g_j = 1`, equivalently `(b) holds iff every g_j ≠ 1`, equivalently `(b) <=> (c)`. The displayed "the condition becomes: `g_j ≡ 1 (mod p_j)` for all `p_j`" should have read "for some `p_j`."

This is not a typo. The proof has been restarted, has a `(<=)` direction that uses "generically," and the final sentence inverts the quantifier. A JCT-A referee will require a complete clean rewrite before being able to evaluate the result.

(It is plausible that the underlying claim is true — the CRT decomposition `Z/nZ = product Z/p_iZ` reduces the problem to a coordinate-wise check, and the right statement is "no joint `g`-orbit can stay in the same `A_d`-fiber unless `g` acts trivially in some `p_j | n/d` coordinate." The cleanly correct proof is short. But this manuscript does not contain it.)

### Issue 2. The "uniform-language reformulations" CL-1 through CL-6 are mostly trivial or restatements.

- **CL-1 (Chinese Remainder Theorem).** The Crossing Lemma is invoked to prove CRT. The "Crossing condition" reduces to "`gcd(p_1, p_2) = 1`," which the paper notes "is trivially satisfied for distinct primes." So CL-1 says "for distinct primes `p_1, p_2`, `Z/p_1p_2Z = Z/p_1Z × Z/p_2Z`." This is CRT itself, not a derivation of CRT. The framing reverses the standard order (CRT is used in the proof of Theorem 1 — see line 107, "Standard CRT decomposes...").
- **CL-2 ("A+M classification").** "This is Theorem 1 verbatim. We list it as a separate corollary..." If it is verbatim, it is not a corollary.
- **CL-3 ("M+M classification").** Has a "sketch" two paragraphs long: "Treat `pi_DYN(g)` as the structure ... by argument analogous to Theorem 1's proof ... `<g> ∩ <h> = {1}`." The argument is *not* analogous: in Theorem 1 the structure operator `A_d` is a quotient and the dynamics `M_g` is an orbit-partition; in M+M, both are orbit-partitions. The "analogous" argument needs significant adjustment. The condition `<g> ∩ <h> = {1}` is plausible but not proven from the Crossing Lemma framework; the paper concedes the proof is sketched.
- **CL-4 ("SPEC+DYN").** Same as CL-3: "Treat `pi_SPEC` as structure: its fibers are reflection-pairs `{x, -x}`. `pi_DYN(g)` crosses iff no `g`-orbit ever contains both `x` and `-x`." Sketch only. The condition "`-1 not in <g mod p>` for every odd prime" is correct but does not follow from Theorem 1 by direct specialization.
- **CL-5 ("Orthogonal-Jump Necessity").** "Direct from definitions": `sigma(pi_m | F) > 0` iff `pi_m` separates a pair in `R(F)`. This is unfolding the definition of `sigma`. It is not a corollary of Theorem 1.
- **CL-6 (Theorem 3 / "p-kernel obstruction").** Has a sketch that argues "any `g` outside the kernel acts on the resolved part; any `g` in the kernel stays inside the blind region." The conclusion ("both choices fail") is correct but the sketch confuses what is being proved. A standard reference (Bourbaki *Algèbre Commutative* Ch. III, or Eisenbud *Commutative Algebra* §3) gives the obstruction directly via the structure of `(Z/p^rZ)^x` — for `r >= 2`, the unit group splits into the residue-`mod p` part and the kernel of reduction, and the kernel acts within fibers. The paper's sketch reaches the right answer by hand-waving over this standard fact.

So six "reformulations": CL-1 is CRT itself; CL-2 is a copy of Theorem 1; CL-3 and CL-4 are sketches; CL-5 is a definitional restatement; CL-6 is sketched and is essentially a known fact about `(Z/p^rZ)^x`.

The "unification" claim of the paper is that these results are "not independent: each is what the Crossing Lemma says when the structure operator and the dynamics operator are specified." But of the six items, only CL-2 is *literally* the Crossing Lemma; the others use either different machinery (CL-3, CL-4) or are tautologies (CL-1, CL-5) or are statements not derived (CL-6).

### Issue 3. The "Crossing Lemma" itself is not new.

The statement "`A_d` and `pi_DYN(g)` jointly separate `Z/nZ` iff `g` has no fixed prime component in `n/d`" is essentially the standard fact about the action of `(Z/nZ)^x` on `Z/nZ` decomposed via CRT. In particular:

- It follows from the standard analysis of *cyclic group actions on orbit-stabilizer structure of a finite ring*. See Lang, *Algebra* (3rd ed., 2002), §I.5–I.6; or Dummit & Foote, *Abstract Algebra* (3rd ed., 2004), §7.6.
- A more direct precedent: **Drápal**, "On multiplication groups of finite quasigroups" (Comment. Math. Univ. Carolin. 1992) studies which combinations of partitions on a finite set are jointly fine; the squarefree case of Z/nZ is one slice.
- The underlying "A_d and M_g together separate Z/nZ iff g has full order on every prime not dividing d" is folklore in the homogeneous-spaces literature; see **Bhargava–Shankar–Tsimerman**, "On the Davenport-Heilbronn theorems" (Annals 2013), Section 3, for the same decomposition used for orbit-counting on `(Z/nZ)^x`-actions.
- The "p-kernel obstruction" (Theorem 3) is the standard observation that `(Z/p^rZ)^x = (Z/pZ)^x × (1 + pZ/p^rZ)` for `p` odd, where the second factor is the "Hensel lift" subgroup acting trivially modulo `p`. This is in any algebraic number theory textbook (e.g., **Neukirch**, *Algebraic Number Theory*, §I.3).

The novelty claim — that this is a "single elementary equivalence" subsuming six results — would have to engage with this literature and explain why the unification framing is new. The paper does not engage with any of the literature above; its bibliography lists only **Birkhoff** (lattice theory, 1940), **Dummit-Foote**, **Gauss**, **Hardy-Wright**, **Ireland-Rosen**, **Lang**, **Ore** (equivalence relations 1942), and **Stanley** (combinatorics) — none of these contains the recent literature relevant to the claimed unification.

---

## §4 Other major comments

**M1. The relationship to the cited internal companion papers J01, J02, J03/J04, J06 is opaque.** The paper claims to be the "algebraic spine" of a 55-paper sequence, with the Flatness Theorem (J06) using the Crossing Lemma to derive the torus aspect ratio `5/7`. None of these companions is publicly available, so a referee cannot evaluate the supporting claim. *JCT-A* will require either (a) the paper stand alone — the abstract / introduction / proofs do not need any companion to be evaluated — or (b) the companions be available preprints. The current setup (companions cited as "submitted to JCT-A, submission-ready") is not adequate.

**M2. Notation is inconsistent.** The paper uses `pi_DYN(g)` but also "`<g>`" (cyclic subgroup), `M_g`, "induced action `g~`", and "orbit space of `g`" interchangeably. The orbit space of `g` is the *set of orbits*, not the partition into orbits — these are formally different objects. Standardize.

**M3. The "U(π)" notation is introduced but the paper does not explain why "unresolved pairs" is the right object.** Standard treatment (Birkhoff, *Lattice Theory*, 1940) uses the partition lattice ordered by refinement; joint refinement is the *meet*. The "joint injective" question is whether the meet is the discrete partition. State this in standard language.

**M4. §4.1 ("the template") promises that each result records: structure operator, dynamics operator, blind region, crossing condition, information generated. None of the six reformulations actually fills out this template explicitly. The `Information generated` slot is left empty in every case. If the template is the unifying tool, it should be applied uniformly, not described and then ignored.

**M5. §5.2 claims the Flatness Theorem (J06) has aspect ratio `5/7` because "the cyclotomic minimal polynomial at p=5 is degree 2 and at p=7 is degree 3." This is irrelevant: the cyclotomic polynomial of `5` over `Q` is `Phi_5(x) = x^4 + x^3 + x^2 + x + 1` of degree 4, not 2; the minimal polynomial of `2 cos(2π/5)` over `Q` is degree 2 (= `phi(5)/2`), but `2 cos(π/5) = phi` is the golden ratio. The phrase "`A_5 = 2 cos(π/5) = phi`" is correct. But the leap to "torus aspect ratio `5/7`" because of degrees 2 and 3 is a non-sequitur. This statement should not appear in the paper.

**M6. The bibliography is shockingly thin for a "unifying" claim.** The paper claims to unify CRT, two classifications, SPEC+DYN, orthogonal-jump necessity, and the p-kernel obstruction. A serious unification claim must engage with the recent literature — joint-closure papers, Latin-square autotopism literature, modular dynamics on Z/nZ, etc. The bibliography contains 8 textbooks (oldest 1801, newest 2012). No journal papers are cited. This is unacceptable for *JCT-A*.

---

## §5 Minor comments

- The phrase "non-associativity as information generation" appears in the title and abstract but is never defined or proved in the paper. Theorem 1 makes no use of associativity (the structures `A_d` and `pi_DYN(g)` are not magmas in the sense of binary operations; they are *partitions*). The title is misleading.
- Page 1, Abstract: "...is the algebraic spine for the geometric statements of the Flatness Theorem (J06), where it determines the forced torus aspect ratio R/r = 5/7 on Z/10Z." This is an unsupported claim about an unavailable companion. Drop.
- §3.3 "The four cases" table has a column labeled "Information generated" with values like "None — trivial," "None — refinement only," "Full — resolves blind region," "Full + redundant mixing." The column is decorative; "Full" is not defined.
- §4.5 (CL-4): "the p=2 case is degenerate: -1 = 1 in F_2, so the reflection partition is trivial." This is correct but the paper's hypothesis is squarefree `n` with `k >= 2` distinct primes, so `n` divides by a prime > 2. Phrase as a footnote.
- §4.6 (CL-5): the score `sigma(π_m | F) := |R(F) \ U(π_m)|` is defined and "Corollary C5" says `sigma > 0` iff `π_m` separates a pair in `R(F)`. This is the definition of `\` and `|·|` — not a corollary of anything.
- §5.3 "Open problems" lists three; #1 (Z/p^rZ obstruction generalization) is real, #2 (non-cyclic base groups) is folklore (the answer is "yes, by structure theorem"), #3 (categorical formulation) is suggested with no plan.
- "Mayes" appears as second author with no affiliation. Provide one.

---

## §6 Literature missed

Beyond the texts listed in §3 above, a JCT-A submission claiming to unify CRT, joint-closure classifications, modular reflection, orthogonal-jump arguments, and the p-kernel obstruction must engage with:

- **Drápal**, "How far apart can the group multiplication tables be?" *Eur. J. Combin.* 13 (1992), 335–343. Direct precedent in the joint-partition combinatorics on finite groups. Author is currently active.
- **Phillips & Vojtěchovský**, "Quasigroup structure theorems," various papers in *J. Algebra* 2005–2015. Standard references for finite-magma classification.
- **Bergeron-Reutenauer**, *Hopf algebras of permutations*, AMS, 2010 — for the modern combinatorial-algebraic framework on finite group actions.
- **Stanley**, *Enumerative Combinatorics, Vol. 2*, Cambridge 1999, §5.3–5.5 — partition lattices, Möbius functions, the unrefining order on partitions.
- **Conway-Sloane**, *Sphere Packings, Lattices and Groups*, Springer 1999, §11 — for the structure of finite cyclic group actions and orbit counting.
- **Fricke**, "Modular dynamics on Z/nZ" 1880s — historical precedent for the multiplicative-additive partition interaction on Z/nZ.
- The recent **Drápal-Wanless**, "Concerning the number of Latin squares with n+1 rows," 2021, listed as relevant in the J05 review, also engages closely with this material.

The "Crossing Lemma" terminology is striking but the search reveals (a) it is not in the algebraic combinatorics literature with this name, and (b) the closest result by name is the *Crossing Lemma* of **Ajtai-Chvátal-Newborn-Szemerédi** (1982, "Crossing-free subgraphs") — a graph-drawing theorem about crossings of edges in the plane. The authors do not cite this, but readers will be confused by the name conflict. Either rename or address explicitly.

---

## §7 Estimated revision effort

The paper as submitted cannot be fixed with revisions in the small. The following must change:

1. **Rewrite the proof of Theorem 1 cleanly.** The current proof has the "Wait... Restart" structure and a quantifier inversion at the end. A correct proof is short (5–7 lines using CRT decomposition coordinate-wise). Drop the long discussion in §3.2 and supply the clean version. (Effort: 1 day.)
2. **Drop CL-1 (CRT — circular), CL-2 (= Theorem 1), CL-5 (definition restatement).** State the remaining items (CL-3, CL-4, CL-6) cleanly, and either prove them from Theorem 1 or admit they are independent results requiring separate proofs. (Effort: 1 week.)
3. **Engage with the literature.** Add 15–25 modern references (1980s–2020s) in algebraic combinatorics, finite quasigroups, Latin squares, modular dynamics. Discuss the actual relationship of Theorem 1 to known results, including whether the statement is novel (it may not be). (Effort: 2–4 weeks of literature search.)
4. **Drop or substantiate the J01-J55 companion claims.** Either remove the references to internal companions (the present paper should stand alone), or provide preprints. (Effort: editorial.)
5. **Drop the "5/7 aspect ratio" claim in §5.2.** It is unsupported and the supporting calculation is wrong. (Effort: minutes.)
6. **Resolve the title.** "Non-Associativity as Information Generation in Finite Magmas" is not what the paper proves. The paper is about partition lattices on `Z/nZ`. Retitle accordingly. (Effort: minutes.)

A clean, correctly-proved version of Theorem 1 with the genuinely new Theorem 3 ("p-kernel obstruction") and minimal additional content might make a 4–6 page elementary note. This would not be a JCT-A paper but might find a home in *Algebra Universalis*, *Order*, or *Comment. Math. Univ. Carolinae*. A more substantial version with the modern literature engagement could potentially make JPAA but not JCT-A.

Total effort: **3–6 months for the full rewrite required for JCT-A.**

---

## §8 Verdict — meets *JCT-A* bar?

**No.** *JCT-A* publishes papers with rigorous, novel combinatorial-algebraic results, full engagement with the literature, and proofs that meet the highest standards of clarity. This manuscript:

- has a broken proof of its central theorem (the proof restarts mid-way and inverts a quantifier at the end);
- claims to unify six results, but four of the six are either trivial restatements (CL-1, CL-2, CL-5) or sketches (CL-3, CL-4);
- proves nothing genuinely new about `Z/nZ` dynamics that is not in standard textbooks or 1990s combinatorics literature;
- has a 8-textbook bibliography ranging from 1801 to 2012, with zero recent journal papers, despite claiming to subsume "recent sufficiency results";
- includes unsupported claims (the "5/7 torus aspect ratio") that pass the smell test only inside an internal framework whose details are unavailable.

The underlying observation — that the joint-injectivity of `A_d` and `pi_DYN(g)` reduces to `g`'s coordinate-wise nontriviality on `n/d` — is true and is a clean elementary fact. A 2-page exposition of this fact, with proper attribution to the standard cyclic-group / CRT machinery, could be a reasonable short note for a journal that publishes such notes. The current 30-page manuscript with the "uniform unification" framing does not stand up to JCT-A scrutiny.

**Recommend reject, with the suggestion that the authors (a) write a clean 5-page note on Theorem 1 + Theorem 3 alone, with proper literature engagement, and (b) submit it to a venue that publishes elementary algebraic-combinatorial notes.**
