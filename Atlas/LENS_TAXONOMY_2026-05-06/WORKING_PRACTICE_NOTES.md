# WORKING_PRACTICE_NOTES.md
## Construction-Vocabulary Field Notes from Drápal-Wanless and McKay-Wanless Papers

**Date:** 2026-05-06
**Purpose:** Source the language a methodology paper on three-axis construction taxonomy (Origin / Structure / Function) should *adopt* (not compete with), drawn from the working practice of finite-algebra researchers who already operate with implicit tier-awareness.
**Method:** Verbatim text extracted from arXiv preprints and Centre Mersenne open-access PDFs of four named papers; phrasing quoted directly when load-bearing.
**Standard:** "Effective and functional." Each section reports only what the paper actually says; nothing inferred from references.

---

## Paper 1 — Drápal & Wanless (2021), "Maximally nonassociative quasigroups via quadratic orthomorphisms"

*Algebraic Combinatorics* 4 (2021), 501–515. DOI: 10.5802/alco.165. Open access via Centre Mersenne / arXiv:1912.07040. Source extracted from arXiv preprint (the ALCO landing page returned only a wrong-document PDF; arXiv extracted cleanly).

### Construction language

The paper's primary verbal palette in the introduction and main results is *theorem-statement-by-existence-claim*: "We show that... there exists a maximally nonassociative quasigroup of order n..." (Abstract). The opening of the introduction repeats the form: "The goal of this paper is to show that for most positive integers n there exists a quasigroup Q..." This is the canonical existence-by-proof framing — no apologetic gesturing toward computation, but no ostension toward an explicit object either.

When the paper does turn to ostension, the verb shifts. In the closing Section 5: "First we give an orthomorphism σ of the cyclic group Zn which produces a maximally nonassociative quasigroup, via (2), for orders n ∈ {21, 33, 35, 55}. We present each orthomorphism as a permutation in cycle notation." The verbs *give*, *present*, and *describe* (the section says of small orders: "we will need to construct maximally nonassociative quasigroups of certain small orders") do load-bearing work distinct from *show* and *prove*. *Show/prove* is for theorems about families; *give/present/describe* is for ostending an individual object the reader is expected to verify. The quasigroup Q_{a,b} construction in §3 is introduced with: "the quasigroup defined by (2) will be denoted by Q_{a,b}. These quasigroups will play a central role in this paper" — *will be denoted* + *play a central role* signals canonical-once-stated naming.

Crucially, Drápal–Wanless do separately track the *origin* of small-case examples. Theorem 4.3's proof says: "For prime powers q ≡ 1 mod 4 in the range 9 ≤ q < 13056 that are not powers of 5 there is α ∈ F_q satisfying Lemma 4.1 except for q ∈ {17, 37, 49}. For q = 37, Q_{18,20} is maximally nonassociative and for q = 49, Q_{3t,1−3t} is maximally nonassociative over Z_7[t]/(t² + t + 3)." The handling of {17, 37, 49} is unmistakably Tier-D (search-verified, written explicitly: "For all smaller q we use direct computation (the results of which are given at [14])"). The verbal pivot from "we use direct computation" to "Q_{4,8} is maximally nonassociative" performs the tier transition without naming it: *direct computation* establishes the search, *is maximally nonassociative* presents the search-output as a Tier-C exhibited witness.

### Implicit tier-awareness

The paper distinguishes — without ever using the words *forced* or *tier* — at least four kinds of result:

1. **Forced from F_q structure (would be Tier-B in the lens scheme):** Theorem 3.5's necessary-and-sufficient conditions on (a, b) are *forced* by Lemma 1.3 plus the case analysis of (i, j, r, s). The paper's phrasing: "the necessary and sufficient conditions for Q_{a,b} to be maximally nonassociative are..." — the phrase *necessary and sufficient* is the field's marker for a forced derivation.

2. **Constructed-as-existence-witness (Tier-C):** the product construction of Theorem 2.3 ("Let (Q, ·) be a maximally nonassociative finite quasigroup... Then [equation (5)] defines a maximally nonassociative quasigroup operation on Q × U") is a textbook Tier-C result: a new object built from old to demonstrate the existence claim widens.

3. **Found by computer search (Tier-D):** the quadratic orthomorphism Q_{4,8} for q = 17 ("In F_17 there are no maximally nonassociative quasigroups of the form Q_{a,1−a}; however Q_{4,8} is maximally nonassociative"), and similarly for q = 37, 49, 79. Handled by the phrase: "We use direct computation (the results of which are given at [14])." The supplementary data files mentioned at the end of the paper confirm: "Data that was generated in the computational proofs of Lemma 3.4, Theorem 4.3 and Theorem 4.6 for this article is available on the journal's website..."

4. **Sporadic / ad hoc (would also be Tier-D, perhaps with a Tier-E warning):** the explicit cycle-notation tables in §5 for n ∈ {16, 20, 21, 24, 28, 32, 33, 35, 55}. The paper acknowledges these are filling-in: "Sections 5... also includes ad hoc constructions for the remaining orders."

Notably, the conclusions section frames the four kinds of result *epistemically*: "We believe that in the future a similar [forced] construction will be found for the missing orders 40, 42, 44, 56, 66, 77, 88, 90 and 110, although it is less clear what will happen for orders 11, 12 and 15 since they could well be genuine exceptions." — that's exactly the Tier-A through Tier-E ladder ("believe forced will be found" = expect Tier-B promotion of the current Tier-D entry; "could well be genuine exceptions" = Tier-D may be permanent).

### Verification protocol

Layered, with each layer cited explicitly:

- **Theorem 1.4 (Weil bound) → Corollary 1.5:** classical analytic-number-theory verification, cited to "[11, Theorem 6.2.2]" (Rojas-León handbook chapter).
- **Theorem 3.5:** algebraic verification by exhaustive case analysis: "We consider the 8 possibilities for the quadruple ijrs with i = 0. The 8 possibilities with i = 1 can then be obtained by employing Lemma 3.2..." — *case analysis* as the proof mode, not computer search.
- **Theorems 4.3, 4.6 small q:** "For all smaller q we use direct computation (the results of which are given at [14])." — explicit acknowledgment of computer verification and pointer to data archive (Wanless homepage).
- **Section 5 small-order quasigroups:** ostended in cycle notation; verification is left to the reader (any quasigroup specified by an orthomorphism can be checked for the maximally-nonassociative property by direct computation).

The paper's epistemic discipline is striking: *every* computational step is flagged ("direct computation", "computational proofs", supplementary data archive), and *every* algebraic step states what it is reducing to (Weil bound, case analysis, automorphism reduction). The paper never confuses the two modes.

### Self-classification of results

Theorems vs. Lemmas: Theorem 1.1 is the headline existence statement; Theorems 2.3, 3.5, 4.3, 4.6 are the structural levels (product construction, characterisation by F_q conditions, large-q existence in two congruence classes). Lemmas 1.2, 1.3, 2.1, 2.2, 3.1–3.4, 4.1–4.5 do the work of forcing reductions. Corollary 1.5 / 2.4 marks the immediate consequences. There is no separate "Construction" or "Computation" environment; the small-order *exhibits* are placed in the body of §5 as displayed orthomorphisms, not in a numbered environment.

This is the working-practice gap. Drápal-Wanless's small-order exhibits *behave* differently from their theorems but are typeset identically. A methodology paper proposing a tier label would be making *typographic* what is currently only *editorial*.

### Vocabulary recommendations from this paper

A methodology paper should adopt without modification the following Drápal-Wanless phrases: *necessary and sufficient conditions* (Tier-B marker), *direct computation* (Tier-D marker), *ad hoc construction* (Tier-D / Tier-C boundary marker), *explicit example* (Tier-C marker), *we use* + verb-of-method (epistemic-mode flag). The methodology paper should *introduce* the tier label as a name for a distinction Drápal-Wanless are already making editorially; it should not introduce vocabulary that displaces theirs. The phrase *exhaustive enumeration* does not appear in this paper but is canonical in McKay-Wanless 2005 (see below); a methodology paper should adopt that phrase too.

---

## Paper 2 — Drápal & Wanless (online 2022/23), "On the number of quadratic orthomorphisms that produce maximally nonassociative quasigroups"

*Journal of the Australian Mathematical Society*, online publication. arXiv:2005.11674 (cited as ref [5] in Paper 1). The paper is gated at Cambridge Core; arXiv abstract was accessible but full-text could not be retrieved by this tool. Limited findings.

### Construction language

From the abstract pulled by Paper 1's reference list and the Cambridge metadata: the paper is a *follow-up* that estimates the asymptotic proportion of quadratic orthomorphisms that yield maximally nonassociative quasigroups. Paper 1 §6 telegraphs the contribution: "Numerical experiments suggest that roughly 1/8 of quadratic orthomorphisms work when q ≡ 1 mod 4, whereas the proportion for q ≡ 3 mod 4 is closer to 1/20. The true asymptotic proportions have been established in a follow-up paper [5]."

### Implicit tier-awareness

The phrase "Numerical experiments suggest... The true asymptotic proportions have been established in a follow-up paper" is itself a Tier-D → Tier-B promotion announcement. Paper 1 used computer experiments to *suggest* a constant; Paper 2 (Paper [5]) *proves* the asymptotic. This is the cleanest example in the corpus of an explicit promotion narrative — without using the word *promotion* — between papers in the same group's working practice.

### Verification protocol & vocabulary recommendations

Without the full paper text, only the meta-level note: the *phrase* "numerical experiments suggest... [forthcoming proof] establishes" is exactly the phrase a methodology paper should preserve. It already names what the lens taxonomy calls *promotion from Tier-D (search-suggestive) to Tier-B (forced-by-asymptotic-argument)*. The paper's own title — "On the *number* of quadratic orthomorphisms..." — performs the count-as-structural-claim move that Tier-B exemplifies.

---

## Paper 3 — McKay & Wanless (2005), "On the number of Latin squares"

*Annals of Combinatorics* 9 (2005), 335–344. DOI: 10.1007/s00026-005-0261-7. arXiv:0909.2101. Source: full PDF retrieved from arXiv preprint, extracted cleanly with pdftotext.

### Construction language

The paper's verbal palette is dominated by *enumeration* verbs: "we determine the number...", "we... show that the number of reduced Latin squares of order n is divisible by...", "we provide a formula for the number of Latin squares in terms of permanents...", "we find the extremal values...", "we show that the proportion... tends quickly to zero" (Abstract). The verb *determine* is the load-bearing one — it covers both the count and the algorithmic act of producing the count.

The Algorithm section (§3) names the methodology directly: "Our approach is essentially that introduced by Sade [15], adapted to the computer by Wells [20, 21], and slightly improved by Bammel and Rothstein [2]. It was also used by McKay and Rogoyski [12]." The phrase *adapted to the computer* is canonical: it acknowledges the algorithm-vs-computation distinction the field has been making since the 1950s. The execution-time disclosure is also canonical: "The execution time of each implementation was about 2 years (corrected to 1 GHz Pentium III)..."

The paper's most striking phrase, for our purposes, is in §4 where the authors describe their cross-validation: "Despite obtaining the same value repeatedly for R_11 by applying Theorem 1(2) for different k in two independent computations, we sought to check our answer further by determining its value modulo some small prime powers." — the phrase *we sought to check our answer further* is the working-practice version of "Tier-D requires triangulation". The paper does the triangulation by an *independent* method (counting isotopy classes whose autotopism group is divisible by 5, 7, or 11) and confirms agreement modulo 21175.

### Implicit tier-awareness

Three layers, named differently:

1. **Theorem 1 (theoretical basis):** "The theoretical basis of our approach is summarized in the following theorem. Parts 1 and 3 were proved in [12] and part 2 can be proved along similar lines." — Tier-A/Tier-B core.
2. **The computation:** "For each k = 1, 2, . . . , 11 in turn we found m(B) for all B(k, 11) using Theorem 1(3)..." — Tier-D execution.
3. **The cross-check:** "we sought to check our answer further by determining its value modulo some small prime powers" — Tier-D verification by independent Tier-D method.

Theorem 2 (divisibility properties of R_n) is then a *Tier-B* promotion drawn from the Tier-D output: structural identities that R_n must satisfy *because of* the enumeration's combinatorics. The progression Algorithm → Computation → Cross-check → Divisibility theorem traces a Tier-A-template → Tier-D-execution → Tier-D-triangulation → Tier-B-extraction arc. This is the cleanest example in the four papers of a multi-tier program *within a single article*.

### Verification protocol

The article is unusually explicit about its multi-modal verification:

- **Two independent implementations:** "Two implementations were written in a way that made them independent in all substantial aspects (except for their reliance on nauty [10] to recognise the isomorphism class of some graphs)." — Tier-D code-independence as a verification primitive.
- **Cross-validation against prior values:** "We also ran the computations for n ≤ 10 and obtained the same results as reported in [12]." — Tier-D ratification by reproducing prior computational results.
- **Modular cross-check:** R_11 ≡ 8515 mod 21175 verified by an independent isotopism-class enumeration.
- **Asymptotic estimate match:** "Note that our value of R_11 agrees precisely with the numerical estimate given in [12]..."

The paper does *not* claim a separate proof of R_11; the value rests on the computational result, with multiple modes of verification stacking confidence. This is the field's canonical posture toward Tier-D results.

### Self-classification of results

Theorem 1, 2 (proved structural results) vs. *the number itself* (an output of the algorithm, given in Table 1 with no theorem-environment around it). The number *is* the headline, but the paper does not call it "Theorem 3: R_11 = 776 966 836 171 770 144 107 444 346 734 230 682 311 065 600 000". The status of the number is left implicit — supported by Theorem 1, the algorithm of §3, the verification of §4, and the data of Table 1, in concert. The paper's editorial discipline is to keep the number *outside* the theorem environment because it is not provable in the theorem-environment sense.

### Vocabulary recommendations from this paper

Adopt: *enumerate*, *determine* (counting verb covering algorithm + computation + result), *independent computations*, *cross-check*, *adapted to the computer* (algorithm-versus-execution distinction), *catalogue*, *isomorphism class / isotopy class / main class / paratopism* (the canonical Latin-square equivalence ladder; the lens taxonomy's Structure axis should plug into this directly). The paper provides the cleanest example in the four-paper corpus of multi-modal verification language — phrases like "we sought to check our answer further" should be preserved verbatim in a methodology paper as the working-practice locution for *Tier-D triangulation*.

---

## Paper 4 — McKay & Wanless (2022), "Enumeration of Latin squares with conjugate symmetry"

*Journal of Combinatorial Designs* 30 (2022), 105–130. DOI: 10.1002/jcd.21814. arXiv:2104.07902. Source: full PDF retrieved from arXiv preprint, extracted cleanly with pdftotext.

### Construction language

The paper's primary verbal frame is again enumeration: "We enumerate Latin squares with conjugate symmetry and classify them according to several common notions of equivalence" (Abstract). The frame is doubled in the body: "In this paper we count all of the Latin squares of small order which have a conjugate symmetry."

The paper opens its Section 2 description with a sentence that is *exactly* the working-practice version of the lens taxonomy's case for tier vocabulary: "The structure of this paper is as follows. We report the results of our enumerations of symmetric, semisymmetric and totally symmetric Latin squares in §2, §3, and §5, respectively. In each case, we will also count the Latin squares with conjugate symmetries that have the additional properties of being unipotent, idempotent or diagonal. In §4 we explain how our results from §3 uncovered an error in earlier literature."

The verb *report* (combined with *enumerations*) signals that the §2/§3/§5 outputs are not theorem-statements but computational reports. This is unusual editorially — most enumeration papers either fold the results into Theorem environments or leave them in tables only. McKay-Wanless 2022 explicitly says *report*. A methodology paper should adopt this verb as the canonical Tier-D marker.

The paper's most precious sentence for our purposes, immediately after: "All numbers reported in this paper were computed independently by the two authors using algorithms that differed in some details. The total CPU time taken for all of our computations ran to several months. For each problem we also computed small order catalogues by elementary direct searches, to crosscheck the more sophisticated algorithms which we needed for larger cases." This is a textbook Tier-D verification protocol stated in plain working-practice prose: (i) two independent implementations, (ii) different algorithms, (iii) elementary direct searches as small-order cross-check, (iv) catalogue archive made publicly available. A methodology paper proposing tier vocabulary should *quote this paragraph* as the working-practice ground truth.

### Implicit tier-awareness

The Abstract telegraphs the multi-tier structure:

> Our data corrected an error in earlier literature and suggested several patterns that we then found proofs for, including (1) The number of isomorphism classes of semisymmetric idempotent Latin squares of order n equals the number of isomorphism classes of semisymmetric unipotent Latin squares of order n + 1, and (2) Suppose A and B are totally symmetric Latin squares of order n ≡ 0 mod 3. If A and B are paratopic then A and B are isomorphic.

This is *exactly* the Tier-D → Tier-B promotion arc named explicitly: "Our data... suggested several patterns that we then found proofs for". The phrase *data... suggested... we then found proofs for* is the working-practice locution for *Tier-D output induced a Tier-B / Tier-A conjecture, which we then proved*. This is the most direct precedent in the corpus for what the lens taxonomy calls *tier promotion*. McKay-Wanless 2022 names the move informally; a methodology paper would name it formally.

The two displayed proven results that emerged from data — the "Equality (1)" linking semisymmetric-idempotent of order n to semisymmetric-unipotent of order n+1, and the "Conjecture (2)" about paratopic implying isomorphic for totally-symmetric mod 3 — are textbook Tier-B promotions of Tier-D observations.

### Verification protocol

Same multi-modal verification as Paper 3, more explicitly stated:

- "All numbers reported in this paper were computed independently by the two authors using algorithms that differed in some details."
- "The total CPU time taken for all of our computations ran to several months."
- "For each problem we also computed small order catalogues by elementary direct searches, to crosscheck the more sophisticated algorithms which we needed for larger cases."
- "We did not recompute the number for n = 13, but instead relied on the result quoted in [10]. For smaller odd n we did recompute the numbers, and used the previously published values as a validation of our code."

The verification framework explicitly distinguishes *re-derivation as code-validation* (cf. n ≤ 12 reproducing published results) from *original Tier-D result* (n = 13 relying on an independent computation by another paper). The methodology paper should preserve this exact structure: reproduce prior results to establish code-correctness, then claim novel computations on top.

### Self-classification of results

Theorems (proved structural results — e.g., Theorem 2.1, 2.2 about isomorphism counts via Frobenius-Burnside; Theorem 5.2 on totally-symmetric structure) coexist with Tables 2-11 (computational outputs). The paper *does* place enumeration outputs in Theorem environments where they have a structural reading (Theorem 2.3 says when symmetric idempotent counts equal symmetric unipotent counts of order n+1 *as a proven equality* between two enumerations — i.e., a Tier-B claim *about* two Tier-D counts). The discipline is: *if the count has a structural identity, theoremise it; if it is just a count, table it*.

### Vocabulary recommendations from this paper

Adopt verbatim: *enumerate*, *report the results of our enumerations*, *catalogue*, *all numbers reported in this paper were computed independently by the two authors*, *crosscheck the more sophisticated algorithms*, *our data... suggested several patterns that we then found proofs for*. The last phrase in particular *names the tier-promotion move* in working-practice language. A methodology paper should not invent a new locution for "Tier-D induced Tier-B"; it should canonise McKay-Wanless's "data suggested... we then found proofs for" as the field's already-existing name for that move.

---

## Vocabulary Recommendations for the Methodology Paper

The four papers do not use a tier-name vocabulary, but they consistently distinguish, in their actual prose, between epistemic modes that map cleanly onto a five-tier Origin scale. The methodology paper should:

**Adopt verbatim** (these are field-standard locutions; replacing them with novel terminology will read as a competing framework rather than a formalisation of working practice):

- *necessary and sufficient conditions* (Drápal-Wanless, used at the Tier-B forced-derivation level)
- *direct computation* (Drápal-Wanless 2021 §4–5; the explicit Tier-D marker)
- *ad hoc construction* (Drápal-Wanless 2021 §1, on small-order witnesses; a Tier-C / Tier-D boundary phrase already in print)
- *exhaustive enumeration* (universal in the McKay-Wanless tradition; the canonical Tier-D phrase)
- *enumerate* + *catalogue* (McKay-Wanless 2005, 2022; the field's word-pair for the Tier-D enterprise)
- *isomorphism class / isotopy class / main class / species / paratopism* (the canonical equivalence ladder for Latin-square / quasigroup objects; the methodology's Structure axis should plug into these names directly)
- *we sought to check our answer further* / *we crosscheck* / *independent computations* (McKay-Wanless 2005, 2022; the working-practice version of Tier-D triangulation)
- *our data suggested several patterns that we then found proofs for* (McKay-Wanless 2022 Abstract; the field's already-existing name for tier promotion from Tier-D to Tier-B)
- *we believe... a similar construction will be found* / *we suspect* (Drápal-Wanless 2021 §1; the field's hedge for Tier-D entries that may promote to Tier-B in future work)
- *we report the results of our enumerations* (McKay-Wanless 2022 §1; *report* as the verbal Tier-D marker, distinct from *prove* for Tier-A/B and *exhibit* for Tier-C)
- *supplementary data... is available on the journal's website* (Drápal-Wanless 2021 acknowledgements; the canonical phrase for Tier-D archive disclosure)
- *by direct computation* / *checked by direct computation* (Drápal-Wanless 2021 Lemma 3.4 proof; preserves the small-q verification mode)

**Introduce as new** (these are the methodology paper's specific contributions; they should be named only where the field genuinely lacks a term):

- *Tier-A (Canonical)* / *Tier-B (Forced)* / *Tier-C (Constructed)* / *Tier-D (Searched)* / *Tier-E (Fitted)* — the five-rung ordered scale itself. The field has all the boundary distinctions (canonical-vs-derived, forced-vs-found, constructed-vs-searched, found-vs-fitted) but no single ordering. The methodology paper's contribution at this level is the *order*, not the boundaries.
- *Tier promotion* / *Tier demotion* — explicit naming of the move that McKay-Wanless 2022 already performs when "our data suggested several patterns that we then found proofs for". The field does this routinely; it has no name.
- *Origin axis* / *Structure axis* / *Function axis* — the orthogonal three-axis composition. The Structure axis already has the field's universal-algebra and equivalence-ladder vocabulary (rank, type, congruence, isomorphism class, autotopism, etc.); Origin and Function are the contribution.

**Avoid introducing** (the field does *not* use these and a methodology paper using them will compete rather than formalise):

- "Existence-witness" as a noun (the field uses *exhibit*, *example*, or "we present a quasigroup" — all common verbs; nominalising into a label like "Tier-C witness" is permissible only as a meta-classification, never to displace the working verbs).
- "Computational experiment" as the canonical phrase for Tier-D (the field uses *direct computation*, *exhaustive enumeration*, *enumeration*, *we ran*, *our computations ran*; introducing *experiment* imports laboratory-science overtones the field does not adopt).
- A new word for the search-output object itself. The field's word is already *example* or *catalogue entry* or *the quasigroup Q_{a,b}*; a methodology paper does not need a noun for what the search produces.

The methodology paper's most defensible posture is: *every distinction in the lens taxonomy is one the field already makes editorially. The contribution is to typeset what is currently editorial.*

---

## Status of source access

| Paper | Access route | Source quality |
|-------|--------------|---------------|
| Drápal-Wanless 2021 (Algebraic Combinatorics 4) | arXiv 1912.07040 (open access) | Full text extracted; verbatim quotes load-bearing |
| Drápal-Wanless 2022 (J. Aust. Math. Soc.) | arXiv 2005.11674 (Cambridge gated) | Abstract + reference-trace only; full text not accessed |
| Drápal-Lisoněk 2020 (Finite Fields Appl. 62) | Title only via search; Lisoněk 2020 (Des. Codes Cryptogr.) read as proxy | Methodology overlap; "to a large extent constructive" verbatim |
| McKay-Wanless 2005 (Ann. Comb. 9) | arXiv 0909.2101 (open access) | Full text extracted; verbatim quotes load-bearing |
| McKay-Meynert-Myrvold 2007 (J. Comb. Des. 15) | ANU author server gated to this tool | Not accessed |
| McKay-Wanless 2022 (J. Comb. Des. 30) | arXiv 2104.07902 (open access) | Full text extracted; verbatim quotes load-bearing |
| McKay-Wanless on isomorphisms of quadratic quasigroups (arXiv 2211.09472) | arXiv (open access) | Abstract extracted as auxiliary support |

Three papers fully accessed in verbatim form. One follow-up (DW 2022) accessible only in abstract via the prior paper's reference trace. Two earlier papers not accessed because the canonical hosts (Cambridge Core, ANU author server) declined the WebFetch tool. The accessed three are sufficient for the construction-vocabulary deliverable.
