# Referee Report — Algebraic Combinatorics

**Manuscript:** "Joint Closure of Two Binary Operations on $\mathbb{Z}/10\mathbb{Z}$: Chain Structure and a Normalizer Identity"
**Authors:** B. R. Sanders, M. Gish (2026)
**File reviewed:** `Gen13/sprint_bundle_2026-05-07_v36_SEEDS_BUNDLE/tig_2026-05-07_bundle/seeds_for_submission/four_core_FINAL.tex`
**Reviewer:** External referee, anonymous
**Date:** 2026-05-06

---

## 1. Summary

The manuscript studies a pair of explicit commutative magmas $(T,B)$ on $\mathbb{Z}/10\mathbb{Z}$ and establishes two combinatorially clean exact identities about them.

**Theorem 1 (chain).** Among the $2^{10}-1 = 1023$ non-empty subsets of $\mathbb{Z}/10\mathbb{Z}$, exactly eight are jointly closed sub-magmas under both $T$ and $B$. The eight form a strict chain in the inclusion order with size sequence $(1,4,5,6,7,8,9,10)$; sizes $2$ and $3$ are forbidden. The chain enumeration walks the forward orbit of an explicit permutation $\sigma$ on $\mathbb{Z}/10\mathbb{Z}$ with one $\sigma$-fixed bridge step.

**Theorem 2 (normalizer identity).** On the minimal non-trivial element of the chain, $\mathcal{C} = \{0,7,8,9\}$, the per-bucket sum $Z_M(p) = \sum_{c}\widehat{M}(p)_c$ of the convolution fuse satisfies
$$
Z_T(p) = Z_B(p) = (p_0 + p_7 + p_8 + p_9)^2
$$
for all $p \in \mathbb{R}^{10}$ supported on $\mathcal{C}$, even though $T$ and $B$ disagree on $12$ of the $16$ cells of the $4\times 4$ restriction.

A companion verification script `4core_verification.py` runs the chain enumeration and the polynomial identity check by symbolic expansion. I executed it; all checks pass.

The paper is **explicitly the SEED-NARROW version**. The closed-form fixed point of the convex-combination iteration $\alpha\widehat{T} + (1-\alpha)\widehat{B}$ at $\alpha=1/2$, the quartic $f(y) = y^4 + 4y^3 - y^2 + 2y - 2$ with Galois group $D_4$ over $\mathbb{Q}$ and LMFDB number field 4.2.10224.1, the closed form $h^*/\beta^* = 1+\sqrt{3}$, and the $\alpha$-uniqueness PSLQ scan are all referenced as Forward Directions (Section 6) and deferred to in-preparation companion papers \cite{SandersGish2026FixedPoint, SandersGish2026MixingWeight, SandersGish2026FpUniversality}.

This is a clean, narrowly scoped, and verifiable paper. The two theorems are correct as stated. The dependence on the choice of $T$ and $B$ as concrete tables — rather than as instances of a structural construction — is the principal weakness, and the paper handles this with appropriate humility (Section 8). The principal *missing* item is acknowledgment of the symmetrization choice for $T$, which is currently implicit.

The author of $T$ and $B$ has produced a clearly-bounded combinatorial-algebraic anchor; the principal question for *Algebraic Combinatorics* is whether the result is sufficiently general to interest the journal's readership. I think it is, but only marginally, and this needs strengthening.

---

## 2. Decision recommendation

**Major revision.** The mathematical content of Theorems 1 and 2 is correct, the proofs are sound (and substantially verifiable from the script), and the writing is clean. However, four issues must be addressed before publication:

(i) **Numerical claim error.** The paper repeatedly states "$T$ and $B$ disagree at 93 of the 100 cells of the full Cayley table"; the actual count is **71 of 100**. (29 cells agree.) The 4-core sub-claim (4 of 16 agreeing) is correct. This needs correction wherever it appears in abstract, introduction, and main text.

(ii) **Symmetrization scope.** The two tables in Definition 2.1 are presented as commutative without acknowledgment that they are *symmetrized* versions of an underlying possibly-asymmetric construction. The classification of jointly-closed sub-magmas is sensitive to this choice (per the authors' own internal records, which have surfaced a variant of $T$ where the size-7 shell is *not* closed). A short scope remark naming the symmetrization convention and flagging that the size-7 shell is fragile under modest perturbations would be honest scholarship.

(iii) **Significance for the journal's audience.** The paper currently reads as "two structural identities about a hand-picked pair of $10\times 10$ tables." For an *Algebraic Combinatorics* readership, this needs a clearer connection to either (a) the $\mathrm{CL}_N$ family of \cite{SandersGish2026Sigma} (a meaningful family of moduli rather than $N=10$ in isolation), or (b) a quasigroup/Latin-square literature thread (Drápal–Wanless 2021 on max non-associative quasigroups; McKay–Wanless on Latin square enumeration) showing where the construction sits.

(iv) **Forward-directions discipline.** Section 6 cites three companion papers in preparation. The paper currently leans on these forward references for context. The convention in *Algebraic Combinatorics* (and most mainstream venues) is that a paper should be self-sustaining; a reader of the present paper alone should not need the unwritten companions. The three companion citations either need to be (a) reduced to an "anticipated future work" remark with no asserted content, or (b) the paper needs to incorporate at least the closed-form fixed-point calculation, which is short and elementary.

If these four items are addressed, I would recommend acceptance.

---

## 3. Major comments

### M1. The numerical disagreement claim is incorrect (CRITICAL)

**Location.** Abstract (line 79), Section 1 paragraph 4 (lines 132–134).

**Issue.** Both passages assert "the two tables disagree at 93 of the 100 cells of the full Cayley table." Direct cell-by-cell comparison gives 29 agreements and 71 disagreements — which is still a substantial dissimilarity, but markedly different from the claim. (For reference: cells where $T(i,j) = B(i,j)$ include all of column 0, parts of row 7, and several scattered cells.)

The companion 4-core claim "agree on exactly 4 of the 16 cells" is correct ($T$ and $B$ agree on $(0,0), (0,7), (7,0), (8,8)$, all routing to either $0$ or $7$).

**Fix.** Replace "$93$" with "$71$" and "$7$" (cells of agreement) with "$29$" wherever it appears. The qualitative claim "near-total pointwise disagreement" is still defensible at $71/100$ but is overstated — I would soften to "differ at $71$ of the $100$ cells, including $12$ of the $16$ cells of the $\mathcal{C} \times \mathcal{C}$ restriction."

**Severity.** Critical. A simple numerical error of this kind in the abstract erodes trust before the reader reaches the substantive claims.

### M2. The symmetrization choice for $T$ should be made explicit (MAJOR)

**Location.** Definition 2.1 (Section 2, lines 217–251); Remark on origin (lines 261–281).

**Issue.** The two tables in Definition 2.1 are presented as commutative-by-fiat. The verification script confirms that the displayed $T$ is symmetric. However, the underlying construction (referenced in the companion $\sigma$-rate paper) admits both a literal/asymmetric variant and a symmetrized variant; choosing one or the other affects the sub-magma chain.

In particular, the authors' internal records (which I would not normally see, but are visible in supporting Atlas materials in the bundle) state that the literal bit-pattern (non-symmetrized) variant of $T$ has $T[9,4] \neq T[4,9]$ and $T[3,9] \neq T[9,3]$, in such a way that the size-7 shell $S_7 = \{0,4,5,6,7,8,9\}$ fails closure. Under that variant, the chain has $7$ elements (sizes $\{1,4,5,6,8,9,10\}$, with size $7$ also forbidden), not $8$.

The claim "the chain has size $8$" is therefore **lens-dependent**: it holds for the symmetrized $T$ presented in Definition 2.1, but not for the literal variant.

This is *not* a fatal issue — the paper is entirely consistent with itself once one accepts the displayed $T$ as the object of study. But the choice should be named, justified, and the alternative briefly acknowledged.

**Fix.** Add a remark after Definition 2.1, e.g.:

> *Symmetrization convention.* The table for $T$ in Definition 2.1 is the symmetrized form $T_{\mathrm{sym}}(i,j) = T_{\mathrm{lit}}(\min(i,j), \max(i,j))$ of the underlying construction in \cite{SandersGish2026Sigma}. The literal (non-symmetrized) variant differs at four cells: $T_{\mathrm{lit}}[9,4]$, $T_{\mathrm{lit}}[3,9]$, and their transposes. The sub-magma chain of Theorem 1 is sensitive to this choice; under the literal variant, the size-7 shell $\{0,4,5,6,7,8,9\}$ fails $T$-closure. Throughout this paper we work with the symmetrized $T$.

**Severity.** Major. Without this remark, a reader following the construction back to the companion $\sigma$-rate paper will encounter a different table and be unable to reconcile.

### M3. The chain-rigidity ("no branching") claim is implicit (MAJOR)

**Location.** Theorem 1 statement (lines 318–334), proof Part (b) (lines 368–422).

**Issue.** The theorem statement asserts a strict chain (one element per non-forbidden size). The proof Part (b) covers sizes 2 and 3 directly, then says "Sizes 4 through 10. At each size, direct enumeration over the $\binom{10}{k}$ candidates verifies that the listed $S_k$ is the unique jointly-closed subset of its size class." This is the chain-rigidity claim, and it is verifiable by the script.

For sizes 4 and 5, where $\binom{10}{k}$ is small ($210$ and $252$ respectively), a few words of structural reasoning would substantially strengthen the proof. For size 4 in particular: any jointly closed $S$ of size 4 must be $\sigma$-invariant on its non-fixed elements (because of the $\sigma$-walk structure of Remark 3.4), so the only candidate is $\mathcal{C} = \{0,7,8,9\}$. A line of this kind would replace one line of "by the script" with one line of structural insight.

**Fix.** Add a one-paragraph structural argument for sizes 4 and 5, leaving sizes 6–9 to the script. Alternatively, ensure the script output explicitly displays, for each non-jointly-closed subset, the cell that fails closure — this would let a reader spot-check by hand without re-running the script.

**Severity.** Major. The theorem statement's "no branching" content is the principal result; the proof should treat it more visibly.

### M4. Significance for *Algebraic Combinatorics* (MAJOR)

**Location.** Whole paper.

**Issue.** *Algebraic Combinatorics* publishes papers at the intersection of combinatorics and algebra — it has a strong heritage in Latin squares (McKay–Wanless), quasigroups (Drápal–Wanless), and structural classification questions. The present paper sits in that broad neighborhood: it is a sub-magma classification result.

However, the paper currently presents $(T,B)$ as a specific hand-picked pair, with the substrate ($\mathrm{CL}_N$ family, "coarse projection") referenced only by citation. For an *Algebraic Combinatorics* reader unfamiliar with the substrate, the central question — *why this pair?* — is not answered.

If the paper is to land cleanly with this audience, I would suggest one of the following:

(a) Strengthen the connection to the $\mathrm{CL}_N$ family. Even a single sentence noting that the chain phenomenon is observed for $N \in \{10, ?, ?\}$ would help — or, conversely, a sentence saying it is *not* observed for $N = 6, 8, 12$ would also help, by way of distinguishing the $N=10$ case as special.

(b) Position the result against the Latin-square / quasigroup literature. The two operations are non-cancellative magmas (so not Latin squares in the strict sense), but the classification of jointly-closed sub-objects is a recognizable question. A short mention of where, in that literature, jointly-closed-sub-magma chains have or have not been studied would situate the paper.

(c) Frame the normalizer identity (Theorem 2) as a polynomial identity in commutative algebra, separate from the magma structure. The identity $Z_T = Z_B = (\sum p_c)^2$ on $\mathcal{C}$-supported $p$ is unusual: it is a global cancellation across cells of two different convolution operators. For *Algebraic Combinatorics*, this is the more interesting half of the paper and could be highlighted as such.

**Severity.** Major. The technical content is solid; the framing for the journal's audience is what needs work.

### M5. Forward-directions citations are aspirational (MAJOR)

**Location.** Section 6 (Forward Directions), references [SandersGish2026FixedPoint, MixingWeight, FpUniversality].

**Issue.** Three of the five references in the bibliography are "in preparation." The paper leans on these for the key distinguishing claims:

- The closed form $h^*/\beta^* = 1+\sqrt{3}$ at $\alpha=1/2$ is asserted in §6 with no proof.
- The Galois group $D_4$ identification of the quartic $y^4 + 4y^3 - y^2 + 2y - 2$ is asserted with no resolvent computation.
- The $\alpha$-uniqueness conjecture is gestured at via "five sample mixing weights."

These three forward references are the *substance* that makes the paper interesting for an algebraic-combinatorics reader. Without them, the paper is two structural identities about a specific pair of tables. With them, it is the entry point to a structurally rich algebraic story.

The convention in mainstream venues is that a paper should not lean on unwritten companions for its core distinguishing claims. The right move is one of:

(a) Promote one (the closed-form fixed point) into the present paper. The proof, per the verification script, is short: substitute $h = x\beta$ into the fixed-point equations on $\mathcal{C}$-restricted $p$, divide by $\beta$, simplify to $x^2 - 2x - 2 = 0$, and read off $x = 1+\sqrt{3}$. This is a natural Theorem 3 of the present paper and would make the paper substantially more interesting.

(b) Demote Section 6 to a half-page concluding remark with no asserted content beyond "the iteration on $\mathcal{C}$ has rich algebraic structure that we take up in subsequent work." This is honest and concise.

I would lean toward (a). The closed-form fixed-point computation is exactly the kind of small algebraic identity that a Theorem 1 + Theorem 2 paper would crown nicely.

**Severity.** Major.

---

## 4. Minor comments

### m1. The notation $(v,h,\beta,r)$ is introduced but its meaning is unmotivated (MINOR)

Line 257–258: "In proofs over $\mathcal{C}$ we sometimes write $(p_0, p_7, p_8, p_9) = (v, h, \beta, r)$." The choice of letters is opaque to a reader without context. (My understanding from the supporting materials is that these stand for "VOID", "HARMONY", "BREATH", "RESET" — TIG operator names that are not part of the paper's stated content.)

**Fix.** Either explain the letter choice (one sentence acknowledging that these are evocative labels from the broader project, with no claim made about them in the present paper), or replace with neutral labels $(p_a, p_b, p_c, p_d)$.

### m2. Definition 2.4 (fuse and normalizer) — ordering convention (MINOR)

Lines 291–301: "$\widehat{M}(p)_c = \sum_{(i,j) \in \mathbb{Z}/10\mathbb{Z}^2 : M(i,j) = c} p_i p_j$." This sums over **ordered** pairs. The notation does not say "ordered" explicitly. Since $M$ is commutative, $(i,j)$ and $(j,i)$ both contribute the same value to the same bucket; for $i=j$ there is one cell.

**Fix.** Add "(ordered pairs)" to the definition for clarity.

### m3. Cite Drápal–Wanless 2021 (MINOR)

The bibliography has Drápal–Kepka 1985 and Kepka 1980 but not the more recent Drápal–Wanless work on max non-associative quasigroups (Algebraic Combinatorics 4 (2021), 501–515). The latter is in this journal and on a closely related topic; citing it would help with the journal-fit issue (M4).

### m4. The role of $\sigma$ deserves a one-line definition (MINOR)

Remark 3.4 (lines 424–455) introduces $\sigma$ as "the permutation defined by $\sigma = (0)(3)(8)(9)(1\;7\;6\;5\;4\;2)$ in cycle notation." This is the entirety of the definition. It would help a reader to know:
- Where does this $\sigma$ come from? Is it $\sigma(j) = T(j,?)$ for some fixed slot? An automorphism of $(\mathbb{Z}/10\mathbb{Z}, T)$? An external structural object?

**Fix.** Add one sentence locating $\sigma$ structurally. E.g., "$\sigma$ is the permutation conjugating the $T$-residue cells $\{(1,2),(2,4),(4,8)? \dots\}$" — or whatever the actual structural origin is.

### m5. "Polynomial identity" terminology (MINOR)

The remark at lines 303–313 says "$Z_M(p) = (\sum_i p_i)^2$ ... because the fuse is bilinear and each ordered pair $(i,j)$ contributes $p_i p_j$ to exactly one output bucket." This is correct for the *full* normalizer, but the substantive content is for the **$\mathcal{C}$-restricted** normalizer. The remark could be made tighter.

**Fix.** Clarify: "For arbitrary $p \in \mathbb{R}^{10}$, $Z_M(p) = (\sum_i p_i)^2$ because every ordered pair contributes once. The substantive claim of Theorem 2 is that for $p$ supported on $\mathcal{C}$, the **partial** sum $\sum_{c \in \mathcal{C}} \widehat{M}(p)_c$ already equals $(p_0 + p_7 + p_8 + p_9)^2$ — that is, $\widehat{M}(p)_c = 0$ for $c \notin \mathcal{C}$, which is equivalent to $\mathcal{C}$ being a sub-magma."

### m6. The 4-core symmetric-pair count (MINOR)

Line 273–276: "Outside the absorbing rows and columns, $T$ takes the absorber value $7$ at most cells, with $10$ cells (the *residue cells*, forming five symmetric pairs) preserving non-absorbing values in $\{3,4,8,9\}$." Verification: $T(1,2)=T(2,1)=3$; $T(2,4)=T(4,2)=4$; $T(2,9)=T(9,2)=9$; $T(3,9)=T(9,3)=3$; $T(4,8)=T(8,4)=8$. These are 5 unordered pairs (10 cells) — correct.

### m7. Field discriminant breakdown (MINOR)

Section 6, line 590: "field discriminant $-10224 = -2^4 \cdot 3^2 \cdot 71$." Verified: $2^4 \cdot 3^2 \cdot 71 = 16 \cdot 9 \cdot 71 = 10224$. The polynomial discriminant $-40896 = -2^6 \cdot 3^2 \cdot 71$ (verified). Index $\sqrt{40896/10224} = 2$, also verified.

### m8. References discipline (MINOR)

Reference [SandersGish2026Sigma] is "Preprint, 2026" — provide an arXiv identifier or DOI when available. Same for the three "in preparation" companions. *Algebraic Combinatorics* requires verifiable identifiers for citations to the extent possible.

### m9. LMFDB cross-reference (MINOR)

Line 590 cites LMFDB № 4.2.10224.1. Provide a stable URL: `https://www.lmfdb.org/NumberField/4.2.10224.1`. *Algebraic Combinatorics* generally requires URLs for LMFDB references for archival reasons.

---

## 5. Line-by-line comments

- **L70 (abstract).** "given explicitly by their Cayley tables" — fine.
- **L78–80 (abstract).** "The two tables disagree on $93$ of the $100$ cells … and on $12$ of the $16$ cells of the four-element restriction below." → see M1: $71$ disagreements, not $93$. The 4-core $12/16$ figure is correct.
- **L88.** "fuse-normalizer $Z_T(p) = Z_B(p) = (p_0 + p_7 + p_8 + p_9)^2$" — correct.
- **L98–100.** "the Galois extension governing the runtime ratio $r/\beta$ … are the subjects of companion papers in preparation." See M5: this is acceptable as forward-pointing remark *if* Section 6 is correspondingly demoted, or if the closed form is incorporated.
- **L132–134.** Same numerical claim as L78. Same fix: 71 not 93.
- **L137–139.** Non-associativity densities $\sigma(T) \approx 0.128$ and $\sigma(B) \approx 0.498$ — directly verified, both correct.
- **L161 (chain).** "Verification of the chain enumeration over $\mathbb{F}_p$ for several primes $p$ … is a target of future work." Fine as written.
- **L227–251.** Cayley tables. Symmetric, transcribed correctly.
- **L256.** "$(p_0, p_7, p_8, p_9) = (v, h, \beta, r)$" — see m1.
- **L283–289.** Definitions of sub-magma, joint closure, $\mathcal{L}(T,B)$. Clean.
- **L290–301.** Fuse and normalizer definitions. Add "ordered pairs" (m2).
- **L322–334 (Theorem 1).** Statement is correct. The strictness claim deserves one extra sentence in the proof (M3).
- **L336–422 (proof of Theorem 1).** Part (a) is convincing. Part (b) for sizes 2 and 3 is complete and well-written. Part (b) for sizes 4–10 is verifiable from the script; would benefit from one paragraph of structural argument for sizes 4 and 5 (M3).
- **L350–362.** $4 \times 4$ restriction tables. Verified correct cell-by-cell. Image of $T|_{\mathcal{C}\times\mathcal{C}}$ is $\{0,7\}$; image of $B|_{\mathcal{C}\times\mathcal{C}}$ is $\mathcal{C} = \{0,7,8,9\}$.
- **L385.** "for $a=8$, $B(8,8)=7 \notin \{0,8\}$" — verified. (Diagonal of $B$ is $(0,2,3,4,5,6,7,8,7,0)$.)
- **L389–390.** "$\{0,9\}$ is $B$-closed. However $T(9,9)=7 \notin \{0,9\}$, so $\{0,9\}$ fails $T$-closure." Verified.
- **L405–411.** Size-3 case: only $\{0,7,8\}$ and $\{6,7,8\}$ pass diagonal constraints; both fail at $B(7,8)=9$. Verified.
- **L414–421.** Sizes 4–10 by enumeration. See M3.
- **L424–455 (Remark 3.4).** $\sigma$-walk reading. The cycle structure $\sigma = (0)(3)(8)(9)(1\,7\,6\,5\,4\,2)$ produces the forward orbit $7 \to 6 \to 5 \to 4 \to 2 \to 1$ (verified by direct iteration). The chain entries match: $S_4 \to S_5$ adds $6 = \sigma(7)$; $S_5 \to S_6$ adds $5 = \sigma^2(7)$; $S_6 \to S_7$ adds $4 = \sigma^3(7)$; $S_8 \to S_9$ adds $2 = \sigma^4(7)$; $S_9 \to S_{10}$ adds $1 = \sigma^5(7)$. The bridge step $S_7 \to S_8$ adds $3$ (a $\sigma$-fixed element), consistent with the description. The remark is correct. See m4 for a request to motivate $\sigma$ structurally.
- **L484–493 (Remark 3.7, rank disparity).** Verified: $T|_\mathcal{C}$ has image $\{0,7\}$ (rank 2), $B|_\mathcal{C}$ has image $\mathcal{C}$ (rank 4). Cells of agreement: $(0,0)\to 0$; $(0,7)\to 7$; $(7,0)\to 7$; $(8,8)\to 7$. All verified.
- **L514–523 ($T$-fuse computation on $\mathcal{C}$).** Verified by sympy:
  - $\widehat{T}(p)_0 = v^2 + 2v\beta + 2vr$ ✓
  - $\widehat{T}(p)_7 = 2vh + h^2 + 2h\beta + 2hr + \beta^2 + 2\beta r + r^2$ ✓
  - $\widehat{T}(p)_8 = 0$, $\widehat{T}(p)_9 = 0$ ✓
- **L530–544 ($B$-fuse computation on $\mathcal{C}$).** Verified:
  - $\widehat{B}(p)_0 = v^2 + 2hr + r^2$ ✓
  - $\widehat{B}(p)_7 = 2vh + \beta^2$ ✓
  - $\widehat{B}(p)_8 = 2v\beta + h^2 + 2\beta r$ ✓
  - $\widehat{B}(p)_9 = 2vr + 2h\beta$ ✓
- **L527, L543.** Both summations equal $(v+h+\beta+r)^2$. Polynomial identity verified by `sympy.expand`.
- **L582–594 (Section 6).** Forward agenda. The closed-form fixed point is asserted to satisfy $h^*/\beta^* = 1+\sqrt{3}$ exactly; the companion ratio satisfies the irreducible quartic $y^4 + 4y^3 - y^2 + 2y - 2 = 0$ with Galois group $D_4$ over $\mathbb{Q}$, generating LMFDB number field 4.2.10224.1. I confirmed each of these computationally:
  - The quartic is irreducible over $\mathbb{Q}$ (sympy `factor_list`).
  - Its Galois group is of order 8 isomorphic to $D_4$ (sympy `galois_group`).
  - Polynomial discriminant $-40896 = -2^6 \cdot 3^2 \cdot 71$.
  - Field discriminant $-10224 = -2^4 \cdot 3^2 \cdot 71$, index $2$.
  - The quartic factors over $\mathbb{Q}(\sqrt 3)$ as $(y^2 + (2-\sqrt 3)y + (\sqrt 3 - 1))(y^2 + (2+\sqrt 3)y - (1+\sqrt 3))$ (verified).
  - LMFDB 4.2.10224.1: signature $(2,1)$, class number 1 — both confirmed.
  - The fixed-point convergence at $\alpha=1/2$ produces $h/\beta = 1+\sqrt 3$ to $> 30$-digit precision in $99$ iterations.

  These facts are deferred to the companion paper [SandersGish2026FixedPoint]. See M5.
- **L596–607 (mixing-weight observations).** $\alpha$-sweep at five sample weights. Direct PSLQ-by-brute-force at $|a|, |b|, |c| \le 20$ admits a small relation only at $\alpha=1/2$ (verified: relation $y^2 - 2y - 2 = 0$, residual $\sim 10^{-45}$). At $\alpha \in \{0, 1/4, 3/4\}$, the best residual at the same coefficient bound is $\ge 10^{-4}$, so no relation is found. At $\alpha=1$, the iteration collapses to $\delta_7$ in 8 iterations. The observations are correct; they are framed as observations rather than theorems.

  **Note.** The system prompt mentioned a "Stern-Brocot grid" of 17 rationals $p/q$ with $q \le 7$. This grid is not in the present paper (only 5 sample $\alpha$ values are described). The full PSLQ scan over the 17-point Stern-Brocot grid appears in a separate script `alpha_pslq_sweep.py` and is positioned as supporting evidence for [SandersGish2026MixingWeight]. The present paper makes no claim about the 17-point scan.
- **L630–636 (verification script enumeration).** "tests joint closure of all 1023 non-empty subsets." Verified — script does enumerate.
- **L654–664 (scope and limits).** Honest disclaimer of what is *not* claimed. Good.

---

## 6. Questions to the authors

**Q1.** Is the $\sigma$-walk reading (Remark 3.4) merely descriptive, or is there a *proof* that any other order of adding elements to the chain would produce a non-jointly-closed subset? If the latter, that would substantially strengthen the chain-rigidity claim.

**Q2.** Is the chain-rigidity result a special case of any classical sub-algebra-lattice theorem? (For instance, in tame congruence theory à la Hobby–McKenzie, the lattice of congruences is constrained; in universal algebra, the lattice of sub-algebras of a finite algebra has known constraints.) A sentence locating the result in either tradition would help the journal-fit issue.

**Q3.** The normalizer identity (Theorem 2) is a non-trivial polynomial identity. Is there a representation-theoretic or character-theoretic reason for it? My naive guess: the two operations differ by a "rearrangement" that preserves total cell-count per output value across $\{0,7,8,9\}$ — but this is a re-statement, not an explanation. Is there an automorphism of $\mathcal{C}$ (as a 4-element set, not as a magma) that conjugates $T|_\mathcal{C}$ to $B|_\mathcal{C}$ up to a coboundary? If so, the identity would be a direct consequence and the paper would gain substantially in interest.

**Q4.** What is the cell-by-cell agreement count for the **larger** chain elements? E.g., for $S_5 = \{0,6,7,8,9\}$, how many of the 25 cells of $T|_{S_5\times S_5}$ agree with $B$? If this count grows with the chain index in a clean pattern, that would be a genuinely new structural observation.

**Q5.** Has the analogous chain phenomenon been checked for smaller moduli? The companion $\sigma$-rate paper studies the family $\mathrm{CL}_N$. For $N \in \{4, 6, 8\}$, do the analogous tables produce a chain, no chain, or a partially-ordered structure with branching? A single sentence comparing $N=10$ to (say) $N=8$ would substantially clarify the *why this $N$?* question.

**Q6.** The companion paper [SandersGish2026FixedPoint] is the principal forward reference. Could a draft be made available to the editor for cross-reading at the revision stage? It is hard to evaluate the "anchor" status of the present paper without sight of what it is anchoring.

---

## Reproducibility and verification log

I executed `4core_verification.py` against the displayed tables. All six checks PASS:

| Check | Status | Notes |
|---|---|---|
| 1. Joint-closure enumeration of all 1023 subsets | **PASS** | Returns the listed 8-element chain; sizes 2 and 3 forbidden; chain strictly increasing. |
| 2. Normalizer identity $Z_T = Z_B = (v+h+\beta+r)^2$ on $\mathcal{C}$ | **PASS** | Sympy `expand` returns 0 for both differences. Per-bucket fuse expressions match the manuscript's lines 514–544. |
| 3. Closed-form attractor (companion paper) | **PASS** | At 50-digit precision, $h^*/\beta^* - (1+\sqrt 3) < 10^{-45}$ in 99 iterations. |
| 4. Universality across chain shells | **PASS** | At every shell of size $\ge 4$, mass outside $\mathcal{C}$ converges to $< 10^{-32}$ and $h^*/\beta^* \to 1+\sqrt 3$. |
| 5. Galois structure of the quartic | **PASS** | Irreducible over $\mathbb{Q}$; resolvent $z^3 + z^2 + 16z + 36 = (z+2)(z^2-z+18)$ verified; field disc $-10224$ matches LMFDB. |
| 6. $\alpha$-sweep PSLQ at $\alpha \in \{0, 1/4, 1/2, 3/4, 1\}$ | **PASS** | Only $\alpha=1/2$ admits a small-coefficient quadratic ($y^2 - 2y - 2$, residual $\sim 10^{-45}$). |

**Independent spot-checks I performed:**

- Cayley table symmetry: verified.
- Cell agreement count: $T$ and $B$ agree on **29** of $100$ cells (paper states "$7$"; see M1).
- 4-core cell agreement: 4 of 16 (verified, matches paper).
- Image of $T$ on full domain: $\{0,3,4,7,8,9\}$ (verified, matches paper).
- Image of $B$ on full domain: $\mathbb{Z}/10\mathbb{Z}$ (verified, matches paper).
- Diagonal of $B$: $(0,2,3,4,5,6,7,8,7,0)$ (verified, matches paper's diagonal table at L373–378).
- Galois group identification: sympy `galois_group(f, y, domain='QQ')` returns a permutation group of order 8 isomorphic to $D_4$ (verified via `is_subgroup(DihedralGroup(4))` plus order check).
- LMFDB record 4.2.10224.1: real signature 2, complex signature 1 (verified by counting real roots of $f$).
- $\sigma$-orbit walk: $\sigma(7) = 6$, $\sigma^2(7) = 5$, $\sigma^3(7) = 4$, $\sigma^4(7) = 2$, $\sigma^5(7) = 1$ (verified, matches Remark 3.4).

**Reproducibility verdict.** The script is short ($\sim 470$ lines), self-contained, deterministic, runs in $\sim 3$ seconds, and uses only `sympy` and `mpmath`. Adequate for *Algebraic Combinatorics* reproducibility standards. The Zenodo DOI 10.5281/zenodo.18852047 is cited in the paper; I did not attempt to verify the DOI is live but recommend the editor confirm at acceptance.

---

## Closing assessment

The paper documents a small, clean, verifiable combinatorial-algebraic fact about a specific pair of $10\times 10$ commutative magmas. The two theorems are correct. The exposition is competent. The principal weaknesses are:

1. A numerical error in the abstract and intro (93 → 71).
2. The symmetrization choice for $T$ is implicit and should be made explicit.
3. The chain-rigidity claim deserves a stronger structural argument for the small cases.
4. The journal-fit framing for *Algebraic Combinatorics* is currently weak, and the paper leans heavily on three unwritten companion papers for its principal interest.

After major revision addressing items M1–M5, the paper would be a publishable short note in *Algebraic Combinatorics*, particularly if the closed-form fixed-point computation is incorporated as a third theorem. Without that incorporation, the paper is on the marginal side for the journal.

I emphasize: I would not recommend rejection. The mathematics is correct, the verification is robust, and the result is the kind of small clean structural identity that the journal does publish. The revision asks are all about presentation and journal-fit, not about the underlying mathematics.

**Recommendation: Major revision.**
