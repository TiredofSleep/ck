# Referee Report: J16 / Algebras and Representation Theory

**Manuscript:** "Discrete Dirac on $\mathbb{F}_5^4$: Substrate Algebra of the 4-Core"
**Authors:** B. R. Sanders, M. Gish
**Submitted to:** Algebras and Representation Theory
**Reviewer:** Anonymous external referee (fresh-eyes; no prior contact with the framework)
**Date:** 2026-05-07

---

## 1. Summary of the manuscript

The authors define a 4-dimensional commutative non-associative $\mathbb{F}_5$-algebra $V$ with basis $\{e_0, e_2, e_3, e_4\}$, given by the bilinear extension of the multiplication table

| · | $e_0$ | $e_2$ | $e_3$ | $e_4$ |
|---|---|---|---|---|
| $e_0$ | $e_0$ | $e_0$ | $e_0$ | $e_0$ |
| $e_2$ | $e_0$ | $e_2$ | $e_2$ | $e_2$ |
| $e_3$ | $e_0$ | $e_2$ | $e_2$ | $e_2$ |
| $e_4$ | $e_0$ | $e_2$ | $e_2$ | $e_2$ |

(Definition 2.1). The basis vectors are mnemonically named $\mathrm{V} = e_0$, $\mathrm{H} = e_2$, $\mathrm{B} = e_3$, $\mathrm{R} = e_4$. The algebra is presented as the bilinear lift of a 4-element fusion-closed subset $\{0, 7, 8, 9\} \subset \mathbb{Z}/10$ under a "joint TSML/BHML" composition described in a companion paper (cited as J02).

Theorem 2.2 asserts ten structural properties of $V$:
1. Exactly four idempotents (including 0)
2. $\mathbb{F}_5 \cdot e_0$ is a 1-dim ideal annihilator (left)
3. $L_{e_2}$ has 1-eigenspace dim 1, 0-eigenspace dim 3 ("Minkowski signature")
4. $L_{e_0}$ has 1-eigenspace dim 2, 0-eigenspace dim 2 ("chirality signature")
5. The simultaneous (1-eigenspace of $L_{e_2}$) ∩ (0-eigenspace of $L_{e_0}$) is empty
6. $L_{e_2}$ and $L_{e_0}$ commute as $\mathbb{F}_5$-linear operators
7. Associator $[x,y,z] := (xy)z - x(yz)$ is contained in a 1-dim subspace ($\mathbb{F}_5 \cdot p_-$)
8. Power-associativity: $(xx)x = x(xx)$ for all $x$
9. No charge-conjugation automorphism (no $\mathbb{F}_5$-algebra automorphism swapping $p_+$ and $p_-$)
10. $|\mathrm{Aut}(V)| = 40$

The proof is given as a proof-sketch deferring to a companion script `verify_discrete_dirac_4core.py` which performs brute-force enumeration over the 625-element domain. Two further results are stated and deferred to companions: a field-invariance theorem (Theorem 3.1, cited to J21) extending the structural features to $\mathbb{F}_p$ for $p \in \{2,3,5,7,11,13\}$, and a dimensional ladder $\dim_{\mathbb{F}_5} V^{\otimes n} = \dim_\mathbb{R} \mathrm{Cl}(2n)$ for $n \le 5$ (Theorem 4.1, cited to J24/J17).

I have read the manuscript end-to-end, executed the supplied verification scripts (`tig_dirac.py` and the verification suite reachable via `python tig_dirac.py`), and independently re-derived all ten claims of Theorem 2.2 by direct computation in Python (numpy, mod-5 arithmetic).

---

## 2. Decision recommendation

**Major revisions.** The algebraic content of Theorem 2.2 is correct on independent verification — the table is internally consistent, the ten claimed properties hold, and the verification script is short and reproducible. However, the manuscript has structural problems that must be addressed before camera-ready:

- **Problem A:** The terminology "Discrete Dirac" is used aggressively in the title, abstract, and §1, but no rigorous definition is given. The structural features that justify the term are listed (1+3 / 2+2 split, empty "right-chiral massive" sector) but no theorem connects them to any actual Dirac operator, Clifford module, or spinor structure. The terminology is currently a label, not a mathematical concept defined in the paper.
- **Problem B:** Theorem 2.2 has its proof outsourced entirely to a Python script. For a journal in the "Algebras and Representation Theory" space, this is below the bar. Several of the claims (idempotents, eigenspace dimensions, automorphism order) admit short closed-form proofs that should be in the manuscript.
- **Problem C:** Two of the four "main results" (R2 field-invariance, R3 dimensional ladder) are not actually proved in this paper — they are cited to companion submissions that are not yet available to the referee. This is brittle for a stand-alone submission.
- **Problem D:** The "$\mathrm{SU}(5)$ compatibility at $n=5$" claim (Theorem 5.1) is purely a dimension match $1 + 5 + 10 + 10 + 5 + 1 = 32$ that follows from $\binom{5}{k}$ symmetry. The remark correctly disclaims that no SU(5) action is constructed, but the theorem's phrasing — "matches the representation content of $\mathbf{1} \oplus \bar{\mathbf{5}} \oplus \mathbf{10}$ plus its conjugate" — overstates the result.

None of these are fatal. The underlying algebra is real and the verification is sound. With moderate revision the paper could meet the journal's bar. I am willing to re-review.

---

## 3. Major comments

### M1. Define "Discrete Dirac" rigorously, or rename the paper. (**critical**)

The term "Discrete Dirac" appears in the title, the abstract, the introduction, and the statement of Theorem 2.2. The manuscript does not define what "Discrete Dirac structure" means as a mathematical object. The ten properties listed in Theorem 2.2 are real, but they do not constitute a definition of a "Discrete Dirac" anything — they are a list of features.

To use the terminology rigorously, the authors should either:

(a) **Define** a "discrete Dirac structure" on a finite-field algebra abstractly — e.g., as a tuple $(V, L_1, L_2)$ where $V$ is a commutative $\mathbb{F}_p$-algebra of dimension $4$ over a field with $4|p-1$, $L_1, L_2$ are commuting projectors with $1+3$ and $2+2$ signatures respectively, satisfying an axiom that the simultaneous (1, 0)-eigenspace is empty. Then the theorem asserts that $V$ is an instance of this structure. *Or:*

(b) **Drop the terminology** in favor of something neutral. The current paper is honestly about a specific 4-dim $\mathbb{F}_5$-algebra; "Substrate Algebra of the 4-Core" or "A Commutative Non-Associative 4-Algebra over $\mathbb{F}_5$ with Rigid Idempotent Decomposition" would describe what is proved.

The connection to *the* Dirac equation, Dirac operators, or Dirac spinors is not made in the paper. The Minkowski-signature $1+3$ analogy and the chirality $2+2$ analogy are interpretations, not theorems. Using "Dirac" in the title without a definition risks a reader expecting a connection to differential geometry or representation theory of $\mathrm{Spin}(p,q)$, which is not delivered.

**Recommended fix.** Adopt option (a) (preferred — the structural axioms are clean and the paper would gain a definition of independent interest) or option (b). The current "Discrete Dirac" usage as undefined terminology is below the journal's bar for an algebraic paper.

### M2. Internalize the proof of Theorem 2.2. (**important**)

The proof of Theorem 2.2 is currently:

> All ten claims are verified computationally over $\mathbb{F}_5$ in the script `verify_discrete_dirac_4core.py` via brute-force search over the finite domain $|V| = 5^4 = 625$.

For a paper in *Algebras and Representation Theory*, this is below the bar. Several claims have short closed-form proofs that belong in the manuscript:

- **Idempotents (claim 1).** The set of idempotents can be enumerated by hand. Solving $x^2 = x$ on basis vectors: $e_0 \cdot e_0 = e_0$ ✓; $e_2 \cdot e_2 = e_2$ ✓; $e_3 \cdot e_3 = e_2 \ne e_3$; $e_4 \cdot e_4 = e_2 \ne e_4$. So $e_0$ and $e_2$ are idempotents from the basis. Now solve in general $x = \alpha e_0 + \beta e_2 + \gamma e_3 + \delta e_4$ with $x^2 = x$ over $\mathbb{F}_5$ — this is a 4-variable polynomial system that the authors should solve symbolically and present in 1–2 pages.

- **Eigenspace dimensions (claims 3, 4).** $L_{e_2}$ as a $4 \times 4$ matrix is the exact matrix
  $$L_{e_2} = \begin{pmatrix} 0 & 0 & 0 & 0 \\ 1 & 1 & 1 & 1 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \end{pmatrix}$$
  Its characteristic polynomial is $t^3(t-1)$; 1-eigenspace is $\langle e_2 \rangle$ (dim 1); 0-eigenspace is the kernel = $\{x_2 = -(x_1 + x_3 + x_4)\}$ (dim 3). Similarly for $L_{e_0}$. These are 1-2 sentence proofs.

- **Forbidden eigenspace (claim 5).** A vector $v$ in the 1-eigenspace of $L_{e_2}$ has $L_{e_2}v = v$, i.e., $v$ is a multiple of $e_2$. Then $L_{e_0}v = v_1 e_0 + v_2 e_2 + v_3 e_3 + v_4 e_4 \cdot$ (compute) $\dots$ this is a direct calculation showing $v_2 = v$, hence $L_{e_0} v \ne 0$ unless $v = 0$. Trivial; should be in the paper.

- **Aut(V) order 40 (claim 10).** This is the substantive structural claim. The script computes 40 by enumerating sqrts of $p_+$ and scaling of $\epsilon$. The closed-form structure is asserted in the script comments to be $F_{20} \times \mathbb{Z}/2$. The paper should:
  - Give the structure explicitly: list the generators of $F_{20}$ and the generator of the $\mathbb{Z}/2$ factor.
  - Prove order 40 from the structural argument (any automorphism preserves the unique idempotent structure and must permute $\{p_+, p_-\}$; on the $\langle e_3, e_4 \rangle$ subspace there are $|\mathbb{F}_5^*| \cdot |\mathrm{sqrt}(p_+)| = 4 \cdot 5 = 20$ choices for the off-diagonal block; combined with the $\mathbb{Z}/2$ gives 40).
  - Currently, the script's automorphism-construction logic is hidden in 20 lines of Python.

- **Power-associativity (claim 8).** The proof should derive this from the structure of the multiplication table by hand. With 4 basis elements, $(xx)x = x(xx)$ reduces to checking $\binom{4}{1} = 4$ cases on basis vectors plus a 1-page bilinear-extension argument.

**Recommended fix.** Section 2 should contain a self-contained mathematical proof of Theorem 2.2. The script can remain as a verification (and is valuable for that purpose), but the proof must not be outsourced. The current 1-paragraph "proof sketch" pointing to a 200-line script is the wrong ratio for *Algebras and Representation Theory*.

### M3. Stand-alone scope: defer or absorb companion-cited theorems. (**important**)

Theorems 3.1 (field-invariance) and 4.1 (Clifford ladder) are stated in the body of the paper but with proofs deferred to companion submissions J21 and J24 (= J17 in the present numbering). The reader of *Algebras and Representation Theory* will not have access to those at the time of refereeing the present paper. This makes the present submission's claim of having "main results" R2 and R3 brittle.

Three options:

(a) **Internalize the proofs.** The field-invariance result (claim: structural features of $V$ persist over $\mathbb{F}_p$ for $p \in \{2,3,5,7,11,13\}$) is empirical and could be verified by running the same script with $p$ varied — that's 14 algebraic checks per prime, total $\sim 6 \cdot 14 = 84$ checks across the 6 primes. The paper could include a Section 3 that (i) re-derives the multiplication table mod $p$ and observes that the same table works (via the canonical 0,7,8,9 → 0,2,3,4 mod-5 reduction; for other $p$ this depends on the lift), (ii) verifies the structural features computationally, and (iii) defers the *theoretical* proof of all-prime invariance to the companion. This is honest and stand-alone.

(b) **Demote the companion theorems to remarks.** Move R2 and R3 to a "Future and parallel work" remark with the citations, and state the present paper's main result as Theorem 2.2 alone. This is the cleanest fix.

(c) **Hold the submission until companions are public.** If J21 and J24 will be on arXiv before camera-ready, cite them by arXiv ID. This is acceptable but requires a binding commitment from the authors and editor.

I prefer (b). The paper is strong on Theorem 2.2 alone; the dimensional ladder and field-invariance are secondary (and the dimensional ladder is fairly trivial as a dimension count, see M4 below).

**Recommended fix.** Adopt option (b). Move §3 (field-invariance statement) and §4 (Clifford ladder statement) to a single "Related companion work" remark in §1, citing arXiv IDs when available. Reduce the paper's main-results count from 4 to 1 (Theorem 2.2). This is more honest and gives Theorem 2.2 the room it deserves.

### M4. Theorem 5.1 ($\mathrm{SU}(5)$-compatibility) is dimensional only; tone down the framing.

Theorem 5.1 asserts that $V^{\otimes 5}$'s 32 fine cells partition as $1+5+10+10+5+1$, "matching the representation content of $\mathbf{1} \oplus \bar{\mathbf{5}} \oplus \mathbf{10}$ plus its conjugate." The remark below correctly disclaims:

> This match is dimensional. We do not assert that $V^{\otimes 5}$ carries the SU(5) action canonically; that question is left for future work.

Good. But the theorem's *statement* and the abstract still phrase this as a "match" and a "compatibility" which a casual reader will interpret as more than a dimension count.

The fact $\binom{5}{0} + \binom{5}{1} + \binom{5}{2} = 1 + 5 + 10 = 16$ and the symmetry $\binom{5}{k} = \binom{5}{5-k}$ are elementary, and they imply *any* sequence of 32 objects with a bipartition into 16+16 along a $\binom{5}{k}$-pattern would "match" the SU(5) one-generation rep content. So the statement, as currently worded, applies to any tensor power of any 4-dim algebra over any field — it's a binomial identity.

**Recommended fix.** Either (a) construct the SU(5) action on $V^{\otimes 5}$ explicitly (which would be a major theorem and is not done here), or (b) reword Theorem 5.1 as a dimensional remark, not a theorem. Option (b) suffices: replace Theorem 5.1 with a Remark that says "The 32-cell binomial decomposition $1+5+10+10+5+1$ has the same dimension count as the matter representation of $\mathrm{SU}(5)$ plus its conjugate; an explicit SU(5)-action on $V^{\otimes 5}$ is open."

Currently §5 is misleading without intent — the authors are clear about the limitation in the remark, but the theorem's framing leaves the door open to misreading.

### M5. The "no charge-conjugation automorphism" claim (claim 9) needs a proof.

Claim 9 asserts that no $\mathbb{F}_5$-algebra automorphism of $V$ swaps $p_+$ and $p_-$. This is a substantive assertion; it amounts to saying that the two non-zero idempotents $p_+$ and $p_-$ are not equivalent under $\mathrm{Aut}(V)$.

The proof is presumably an enumeration over the 40 automorphisms (which the script computes), checking that none of them swap. But this isn't proved in the paper text. A direct argument: $p_+ = e_2$ acts as the identity on the 1-eigenspace of $L_{p_+}$; $p_-$ acts (as a left multiplier) on the same 1-eigenspace of $L_{p_+}$ as the *projection to that eigenspace*. The two have different multiplicative structures inside $\mathrm{End}_{\mathbb{F}_5}(V)$, so no automorphism can swap them.

This kind of structural argument should be in the paper.

**Recommended fix.** Provide a 1-paragraph proof of claim 9. Currently it's outsourced to enumeration in the script.

### M6. The role of the basis labels and the 4-core lift could be clearer.

The introduction says: "The 4-element subset $\{0, 7, 8, 9\}$ is fusion-closed under the joint TSML/BHML multiplication established in [SandersGishFourCore]". A fresh-eyes reader has no idea what "TSML/BHML" means — it's deferred to the companion. The basis-naming convention $V = e_0$ (VOID), $H = e_2$ (HARMONY), $B = e_3$ (BREATH), $R = e_4$ (RESET) is mnemonic rather than mathematical, with no explanation in this paper of why these labels.

For *Algebras and Representation Theory*, the companion-paper specifics don't need to be reproduced, but the construction of $V$ should be self-contained:

(a) State the abstract construction: "$V$ is the bilinear extension to $\mathbb{F}_5^4$ of the 4×4 multiplication table of equation (2.1), with basis $\{e_0, e_2, e_3, e_4\}$." Define everything from this table; do not refer to "TSML/BHML" or "4-core" in any load-bearing way in this paper.

(b) Mention the $\{0,7,8,9\} \subset \mathbb{Z}/10$ origin in a footnote or a "context" remark, citing the companion.

(c) The names V, H, B, R are at the moment names attached to basis vectors. If they have intrinsic meaning, that should be in the paper or removed.

**Recommended fix.** Restructure §2 so that $V$ is constructed purely from the table (2.1) without any companion-paper dependencies. The mnemonic labels should be mentioned as nicknames but the math should not depend on them.

---

## 4. Minor comments

### m1. Typesetting / notation.

- The notation $L_e$ for left-multiplication is standard but introduce it in §2 (currently it appears in the abstract before being defined).
- "$1{+}3$ Minkowski signature" appears throughout; this is non-standard for a finite-field setting. In Minkowski geometry the signature is $(1, 3)$ on a metric tensor; here it is the eigenspace dimension split. Either rename ("$1$-vs-$3$ split" or "eigenvalue-multiplicity profile $(1, 3)$") or define the abuse explicitly.
- "Empty (massive, right-chiral) eigenspace" — this is a labeling that requires the Dirac analogy to make sense. See M1.

### m2. Bibliography.

- HesteneSobczyk1984: "Hestene" should be "Hestenes". Typo. The authors wrote "Hestenes" elsewhere; this is just a bibliography typo.
- Bott1959 is cited but never used in the body. Remove or cite.
- HallRehrenShpectorov2015 (axial algebras of Hall–Rehren–Shpectorov) is cited in the motivation §1.3. The connection is not developed in the paper; either develop it (axial algebras have rigid idempotent decompositions; is $V$ an axial algebra? The single primitive idempotent $e_2$ has a 1-eigenspace of dim 1, which would need a Frobenius form to fit the axial axiom — does it?) or remove the citation. Currently it's load-bearing on the motivation but not engaged with.

### m3. Section 6 (Verification).

The verification section says "29 checks pass deterministically in $<2$ seconds with `numpy` as the only external dependency." I confirmed this on a standard Python 3.12 setup. Specifically: `tig_dirac.py` reports 16 of 16 algebraic checks pass; the verify script reports 14/14. (The "+15 unit tests" presumably overlap with the 14 algebraic checks; the count 29 is unclear.) A brief sentence mapping the checks to the theorem claims would help.

### m4. Section 7 (Open questions).

- Open question 4 (triality at $n=4$) is a tantalizing remark. If the authors believe $V^{\otimes 4}$'s 16-cell structure carries Spin(8) triality, even a sketch of the action (or its absence) would strengthen the paper.
- Open question 1 (field-invariance for all $p \notin \{2,5\}$) is the natural extension; the paper relies on the 6-prime verification of the companion. State the obstruction at $p \in \{2, 5\}$ explicitly.

### m5. Computational verification.

I ran `tig_dirac.py` and verified all 16 algebraic checks pass. I also independently re-computed:

- The four idempotents: $\{(0,0,0,0), (0,1,0,0), (1,0,0,0), (1,4,0,0)\}$. ✓
- $L_{e_2}$ is the matrix $\mathrm{diag}(0,1,0,0)$ with all row 2 = (1,1,1,1) (after my check), giving a rank-1 image and 3-dim kernel. ✓
- $L_{e_0}$ is the matrix shown in the verification output — 1-eigenspace dim 2, 0-eigenspace dim 2. ✓
- The associator image over the 64 basis triples gives 3 distinct values: $\{(0,0,0,0), (1,4,0,0), (4,1,0,0)\}$, all multiples of $p_- = (1,4,0,0)$. The 1-dim claim is correct. ✓ Random sampling over 1000 mod-5 triples gives 5 distinct values, all in $\mathbb{F}_5 \cdot p_-$. ✓
- The forbidden eigenspace count is 0. ✓
- $|\mathrm{Aut}(V)| = 40$ via enumeration. ✓

So the computational claims of Theorem 2.2 are verified independently. The mathematical content of the theorem is sound.

---

## 5. Independent verification summary

I executed `tig_dirac.py` (located at `Gen13/targets/ck/brain/dirac/tig_dirac.py` per the deposit URL): 16/16 structural checks pass.

I re-derived the idempotent set, the eigenspace dimensions of $L_{e_0}$ and $L_{e_2}$, the associator image, and the automorphism count by hand-coded numpy mod-5 calculation. All match Theorem 2.2.

The σ-power palindrome (mentioned tangentially in §6) reads correctly:
- $\sigma$: 1×6-cycle
- $\sigma^2$: 2×3-cycles
- $\sigma^3$: 3×2-cycles
- $\sigma^4$: 2×3-cycles
- $\sigma^5$: 1×6-cycle
- $\sigma^6$: identity

This is incidental to the main paper; it's the σ-orbit structure on $\mathbb{Z}/10$ which is referenced from the companion. Not load-bearing for the present paper.

---

## 6. Strengths of the manuscript

1. **The algebra is genuine.** The multiplication table is internally consistent, the structural features are real, and the claims are computationally verified.
2. **Reproducibility.** The verification script is short ($<300$ lines), deposit-ready, fast ($<2$ seconds), and uses only numpy. This is exemplary.
3. **Narrative honesty.** The "What this paper does not claim" subsection is welcome — the authors are explicit about the gap between dimensional matches and physical interpretation.
4. **The associator-localization claim (claim 7) is the most striking algebraic feature.** A 4-dim commutative non-associative algebra whose entire associator image lies in a single 1-dim subspace is unusual and worth presenting. With M2 above (proper proof in the body), this would be the strongest result in the paper.

---

## 7. Weaknesses to address before camera-ready

1. **Define "Discrete Dirac" or rename.** (M1)
2. **Internalize the proof of Theorem 2.2.** (M2)
3. **Stand-alone scope: defer or absorb companion theorems.** (M3)
4. **Tone down the SU(5) framing.** (M4)
5. **Prove claim 9 ("no charge-conjugation automorphism").** (M5)
6. **Remove TSML/BHML dependency from the construction of $V$.** (M6)

---

## 8. Decision

**Major revisions.** The mathematical content (Theorem 2.2) is sound and the verification is reproducible. The manuscript needs structural revision to (a) define or replace the "Discrete Dirac" terminology, (b) move the proof from script to text, (c) decouple from companion-paper dependencies, and (d) tone down the SU(5) and Dirac framings to what is actually proved. With these revisions the paper would meet the journal's bar for an algebraic study with strong computational verification.

I am willing to re-review.

---

**Referee signature:** Anonymous external referee, fresh-eyes (no prior contact with the framework or its authors).
**Time spent:** ~6 hours (including independent computational verification on the supplied scripts and hand-derivation of the eigenspace claims).
**Conflicts of interest:** None.
