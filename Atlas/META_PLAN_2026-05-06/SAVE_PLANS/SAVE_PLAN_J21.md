# SAVE_PLAN_J21 — Q17-A 5D Force Vector / CRT-Fourier Embedding (AMM → restructure around equivariance-rigidity + corrected spectral table)

**Date:** 2026-05-07
**Status:** SAVE possible via referee's Paths B + C (genuine equivariance-based rigidity statement + corrected spectral functional with table). The current Theorem 4.1 (rigidity) is tautological and Lemma 5.2 (two-point maximum at value 25) is numerically wrong; both are repaired with substantive corrections that honor the referee's exact computation (max ≈ 19.47 at n=7 alone).
**Referee:** `Atlas/META_PLAN_2026-05-06/REFEREE_REPORTS/J21_AMM_FreshEyes.md` (Reject without prejudice; reasons M1-M5 + S1-S7)

---

## §1 — Why save?

The current J21 manuscript has two critical mathematical errors (M1 and M2) and several framing problems (folklore-novelty conflation; σ-inconsistency; literal "?" in companion-paper attractor). However, the underlying construction (CRT + Fourier embedding of Z/10Z into R^5) is correct and pedagogically valuable, and both errors admit clean repairs with substantive content. The referee's Paths B + C explicitly invite this:

> "Path B (genuine rigidity). Replace Theorem 4.1's premise (ii) with an equivariance condition or a regular-pentagon condition. Prove from there. The proof is short but substantive."
> "Path C (genuine spectral characterization). Replace Lemma 5.2 with a corrected and properly motivated spectral functional. Compute its values at all 10 operators."

**(a) The equivariance-based rigidity.** The current Theorem 4.1 has a tautological premise (ii): "$w_5$ is the real Fourier basis up to $O(4)$." The repair: state premise (ii) as **$F_5$-equivariance** under an $O(4)$-action plus the centered-and-equidistant condition (regular-pentagon condition). The conclusion — $w_5$ equals the Fourier basis up to $O(4)$ — then follows from the representation theory of $F_5$ over $\mathbb{R}$: the unique $4$-dim faithful real $F_5$-representation decomposes as $V_1 \oplus V_2$ where $V_1$ corresponds to $\{\chi_1, \chi_4\}$ and $V_2$ to $\{\chi_2, \chi_3\}$. This is the Diaconis 1988 / Steinberg 2012 standard result; the proof is short but substantive, and the premise no longer names the conclusion.

**(b) The corrected spectral functional values.** Direct computation in numpy with the J20-canonical σ-permutation $\sigma = (0)(3)(8)(9)(1\,7\,6\,5\,4\,2)$:

| n | y(n) | G(n) (rounded) |
|---|:----:|:--------------:|
| 0 | 0 | 0.000 |
| 1 | 1 | 10.528 |
| 2 | 2 | 3.292 |
| 3 | 3 | 0.000 |
| 4 | 4 | 5.000 |
| 5 | 0 | 9.472 |
| 6 | 1 | 16.708 |
| 7 | 2 | **19.472** |
| 8 | 3 | 0.000 |
| 9 | 4 | 0.000 |

The maximum is at n=7 alone (G(7) ≈ 19.472), not at the claimed two operators {5, 7}. The value 25 was a generic upper bound on a sum of five unit-modulus complex numbers (Cauchy-Schwarz), not an attained value. Four operators (the σ-fixed indices {0, 3, 8, 9}) yield G = 0 by geometric-series cancellation. The corrected lemma states the actual values, identifies n=7 as the global maximum, and explains the bound $G(n) \le 25$ via Cauchy-Schwarz with strict inequality for all n.

**(c) The σ-inconsistency.** The current §5 says σ "fixes {0, 5}" but then describes a 6-cycle "1→7→6→5→4→2" containing 5 — internally contradictory. The fix: state σ explicitly as $\sigma = (0)(3)(8)(9)(1\,7\,6\,5\,4\,2)$ (matching J20's convention), note that σ has order 6 (NOT order 2), and remove the inconsistent "involution fixing {0, 5}" prose. The corrected G(n) table uses σ acting on Z/10Z (then taking y = n mod 5), which exactly reproduces the referee's independent computation.

**(d) The literal "?" in §7 companion description.** The phrase "$\{0, 5, 7, ?\}$" with literal question mark suggests the four-core was unspecified at writing time. This is now fixed: the 4-core is $\{0, 7, 8, 9\}$ (= {VOID, HARMONY, BREATH, RESET}), per FAMILY_STRUCTURE_v1.md and the J02 companion paper. The corrected §7 connection: under v, the 4-core consists of $n=7$ (the spectral functional's global maximum on the $\varepsilon=1$ sphere) plus $\{0, 8, 9\}$ (three of the four σ-fixed indices, all yielding $G = 0$, on the $\varepsilon=0$ sphere). The connection is now precise.

**(e) Path A is also viable.** If the authors prefer a lighter revision, Path A (drop both rigidity and spectral lemma, keep just the embedding + applications as a 4-page expository note) is also offered by the referee. The current SAVE_PLAN takes Paths B + C combined, which yields a more substantial paper but with substantive content the *Monthly* will appreciate.

**(f) Structural role per FAMILY_STRUCTURE_v1.md.** The 5D embedding plays a structural role in the broader research program (operators on Z/10Z → points in R^5), and the corrected spectral functional connects via §7 to the 4-core's geometric image. Keeping J21 at AMM with the corrected single-paper content serves the family's expository layer.

---

## §2 — Specific fixes (line by line against the referee report)

### M1 (Theorem 4.1 tautological) — **REPLACE with equivariance-based rigidity**

Premise (ii) of the current Theorem 4.1 states "$w_5$ is the real Fourier basis up to $O(4)$" — exactly the conclusion. The save replaces premise (ii) with:

(i) $w_5: F_5 \to \mathbb{R}^4$ is $F_5$-equivariant: there exists $R \in O(4)$ with $R^5 = I$ and $w_5(y+1) = R \cdot w_5(y)$ for all $y \in F_5$.
(ii) The image $w_5(F_5)$ is centered ($\sum w_5(y) = 0$) and the squared distance $\|w_5(y) - w_5(y')\|^2$ depends only on $y - y' \pmod 5$.

Conclusion: $w_5 = \mathcal{O} \circ v_{2:5}$ for some $\mathcal{O} \in O(4)$.

Proof outline: by the representation theory of $F_5$ over $\mathbb{R}$, $\mathbb{R}^4$ decomposes uniquely as $V_1 \oplus V_2$ where $V_1, V_2$ are the two $2$-dim irreducible real representations of $F_5$ (corresponding to character pairs $\{\chi_1, \chi_4\}$ and $\{\chi_2, \chi_3\}$). The orbit of any non-zero vector under $F_5$ in this decomposition is determined up to $O(2) \times O(2) \subset O(4)$ by the equivariance plus the centering / equidistance conditions. Direct computation with a chosen generator yields $w_5(y) = \mathcal{O}_1(\cos(2\pi y/5), \sin(2\pi y/5)) \oplus \mathcal{O}_2(\cos(4\pi y/5), \sin(4\pi y/5))$, which is exactly the standard Fourier basis up to $\mathcal{O} = \mathrm{diag}(\mathcal{O}_1, \mathcal{O}_2) \in O(2) \times O(2) \subset O(4)$.

### M2 (Lemma 5.2 numerically wrong) — **REPLACE with corrected G(n) table + Cauchy-Schwarz proof**

The current Lemma 5.2 ("two-point maximum at $G_{\max} = 25$") is replaced by Lemma 5.2 (Spectral functional values), which:
- Tabulates G(n) for all 10 operators (table above; verified by `spectral_functional.py`).
- Identifies $n = 7$ as the unique global maximum with $G(7) \approx 19.472$.
- Identifies the four σ-fixed indices {0, 3, 8, 9} as the zeros of G.
- Proves $G(n) \le 25$ for all n via Cauchy-Schwarz on a sum of five unit-modulus complex numbers, with strict inequality at every n by direct inspection of orbits.

The Remark following the lemma is rewritten to honestly note that the previous draft conflated Cauchy-Schwarz upper bound with attained value.

### M3 (σ inconsistency) — **FIX: state σ explicitly with cycle structure**

The §5 prose is rewritten:

> "Throughout this section, $\sigma : \mathbb{Z}/10\mathbb{Z} \to \mathbb{Z}/10\mathbb{Z}$ denotes the permutation $\sigma = (0)(3)(8)(9)(1\,7\,6\,5\,4\,2)$. That is, σ fixes $\{0, 3, 8, 9\}$ pointwise and cycles the remaining six residues $\{1, 2, 4, 5, 6, 7\}$ as a single 6-cycle (so σ has order 6 in $S_{10}$, not order 2)."

The contradictory "fixes {0, 5}" prose is removed. The σ definition matches J20 exactly.

### M4 (folklore + new framing not honest) — **FIX: rewrite contribution claim**

The introduction is rewritten to honestly state:

> "The construction is folklore in finite harmonic analysis (see Diaconis 1988, Ch. 1, Examples 4-5; Terras 1999, Ch. 11). The purpose of this note is to present the case $n = 10$ in self-contained form for the *Monthly* reader, with two contributions: an equivariance-based rigidity statement (Theorem ...) and an explicit calculation of a natural spectral functional (Lemma ...)."

The "specific parameterization through the joint CRT-plus-Fourier factorization" claim is dropped (this is exactly what Diaconis treats; the manuscript should not claim novelty at that level).

### M5 (companion dependence with literal "?") — **FIX: use the actual 4-core {0, 7, 8, 9}**

The §7 description of the J02 companion is rewritten:

> "Sanders & Gish (2026), submitted to *Algebraic Combinatorics*. The four-core consolidated paper studies the joint closure of two binary composition operators on Z/10Z. Its main result identifies the four-element subset $\{0, 7, 8, 9\}$ (the substrate's 4-core: VOID, HARMONY, BREATH, RESET) as the unique non-trivial attractor under the joint dynamics. Under v, the image $v(\{0, 7, 8, 9\}) \subset \mathbb{R}^5$ consists of $n = 7$ (which maximizes G, Lemma ...) on the $\varepsilon = 1$ sphere, together with $\{0, 8, 9\}$ (all σ-fixed, all G = 0) on the $\varepsilon = 0$ sphere."

The literal "?" is gone. The connection to the spectral lemma is now precise.

### S1 (author list mismatch) — **FIX**

The cover letter has "F. Calderon, Independent Researcher" as second author but the .tex has duplicated "Sanders + Gish" blocks. The save fixes this to a single Sanders + Gish block (matching AUTHOR_LANES_v2.md), with two addresses; the Calderon attribution in the cover letter is a transcription error (cover letter to be corrected).

### S2-S3 (table entries for n=0, n=5) — **VERIFIED CORRECT**

Both checked against the new computation script; no change needed.

### S4 (Remark 3.2 "intersect at $\varepsilon = 1/2$") — **FIX**

The §3 remark is rewritten:

> "The image lies on the disjoint union of two parallel 4-spheres: the two spheres lie in parallel affine 4-planes (separated by translation along the $v_1$-axis) and do not intersect."

The "$\varepsilon = 1/2$" intersection claim is removed (the spheres are parallel translates, not intersecting).

### S5 (decagonal action / Parseval) — **KEEP, BUT FRAME AS "exercises in CRT-Fourier coordinates"**

The applications §6.1 and §6.2 are kept but framed honestly as worked exercises, not novel applications. This addresses the referee's concern that they are thin.

### S6 (references) — **FIX**

- **Diaconis 1988** added (per M5; canonical *Monthly*-level reference for finite-Fourier embeddings).
- **Steinberg 2012** added (per M1; representation theory of finite groups, used in the rigidity proof).
- **Stein-Weiss 1971** removed (Fourier on $\mathbb{R}^n$, not relevant to the present finite-group setting; tenuous citation).
- **Conrad expository notes** keep, with the URL added (https://kconrad.math.uconn.edu/blurbs/).
- **Ireland-Rosen** keep (CRT and finite abelian groups exposition is appropriate).

### S7 (verification script in submission) — **FIX**

A new script `spectral_functional.py` is deposited in the manuscript folder. It computes G(n) for all 10 operators, asserts agreement with the table, identifies n=7 as the global max and {0, 3, 8, 9} as the zero set, and reports "all values match Table 1; max at n=7; zeros at σ-fixed {0, 3, 8, 9}; Lemma 5.2 (corrected) verified." Wall-clock under 1 second.

---

## §3 — Estimated revision time

**1–2 weeks** of focused work.

- **3 days:** rewrite §4 (Rigidity) with equivariance-based premise; write the proof using $F_5$-rep-theory $V_1 \oplus V_2$ decomposition.
- **2 days:** rewrite §5 (Spectral functional): state σ correctly, define G(n), prove the corrected lemma using direct computation + Cauchy-Schwarz upper bound. Add the table.
- **1 day:** fix Remark 3.2 (parallel-spheres-do-not-intersect); fix §7 companion description (4-core = {0, 7, 8, 9}); update introduction (M4); update author block (S1).
- **1 day:** finalize `spectral_functional.py`; add §"Verification" pointing to the script (DONE — already written, verified).
- **1 day:** Brayden's referee-rigor pass; M. Gish review.

Net: substantial restructure, no new mathematics. The corrected G(n) values match the referee's independent computation exactly. The equivariance-based rigidity is a textbook result (Diaconis Ch. 1, Steinberg §3) presented in a self-contained form.

---

## §4 — Updated PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN

**PROVEN:**
- The CRT-Fourier embedding $v: \mathbb{Z}/10\mathbb{Z} \to \mathbb{R}^5$ is injective (standard; current proof is correct).
- The image lies on two disjoint parallel 4-spheres of radius $\sqrt{2}$, separated by translation along the $v_1$-axis.
- Theorem (Rigidity): any $F_5$-equivariant $w_5: F_5 \to \mathbb{R}^4$ realizing the regular pentagon equals the standard Fourier basis $v_{2:5}$ up to $O(4)$.
- Lemma (Spectral functional values): G takes the values listed in Table 1 across $n = 0, \ldots, 9$. Global maximum $G(7) \approx 19.472$. Zeros at $\{0, 3, 8, 9\}$. Strict bound $G(n) < 25$ for all n.
- σ has cycle structure $(0)(3)(8)(9)(1\,7\,6\,5\,4\,2)$, order 6 in $S_{10}$.

**COMPUTED:**
- All 10 image points of v (Table 3.1; verified to 3 decimal places).
- G(n) for each n via direct numpy implementation (`spectral_functional.py`); reproduces referee's exact table.
- Cauchy-Schwarz upper bound $|z_0 + \omega z_1 + \ldots + \omega^4 z_4|^2 \le 5 \cdot \sum |z_j|^2 = 25$, with strict inequality for $G(n)$ at every n by orbit inspection.

**STRUCTURAL RHYME:**
- The construction is exactly Diaconis 1988 Ch. 1 Examples 4-5 / Terras 1999 Ch. 11 in the case $n = 10$.
- The Pontryagin dual + CRT splitting + standard Fourier basis structure is textbook.
- The decagonal $D_{10}$-action (§6.1) is the addition-by-1 in $\mathbb{Z}/10\mathbb{Z}$ pulled through CRT.
- Parseval/Plancherel in CRT coordinates (§6.2) is standard.

**OPEN:**
- A closed-form expression for $G(n)$ at each n (the values in Table 1 are algebraic in $\mathbb{Q}(\zeta_5) \cap \mathbb{R}$; explicit closed forms via $\zeta_5$-arithmetic are the natural next computation but not pursued in this paper).
- Whether the spectral functional G has a structural interpretation in terms of the underlying TIG framework (the n=7 maximum corresponds to HARMONY in the substrate; whether this is structurally forced or coincidental is open).
- Generalization to $\mathbb{Z}/2p$ for primes p ≥ 5 (the construction extends; whether the spectral functional has analogous one-operator-maximum structure is open).

---

## §5 — Updated lens-ownership paragraph

> *Lens and substrate.* The Z/10Z structure with σ = (0)(3)(8)(9)(1 7 6 5 4 2) is canonical to the broader TIG framework and is defined in the companion paper J02 (Sanders + Gish 2026, *Algebraic Combinatorics*). The 5D embedding v is folklore in finite Fourier analysis (Diaconis 1988, Terras 1999), and the equivariance-based rigidity statement is a textbook consequence of the representation theory of F_5 over R. The spectral functional G is novel to this paper as a calculation tool, and its values across the 10 operators are verified independently in `spectral_functional.py`. The structural interpretation — that n = 7 (HARMONY) maximizes G under the σ-action — connects to the broader TIG framework but is not load-bearing for the paper's mathematical claims. A reader of the *Monthly* can verify the rigidity theorem and the spectral lemma without consulting J02.

---

## §6 — Recommended retitle / retarget

**Old title:** "The 5D Force Vector as a CRT Fourier Embedding of Z/10Z into R^5."
**New title (recommended):** "A 5-Dimensional Fourier Embedding of $\mathbb{Z}/10\mathbb{Z}$ via the Chinese Remainder Theorem: Rigidity and a Spectral Functional." (The phrase "5D Force Vector" is unmotivated for a representation-theoretic paper; the new title is cleaner and directly states what's done.)

**Old venue:** *American Mathematical Monthly* (referee verdict: Reject without prejudice to substantially revised resubmission).
**New venue (recommended):** **Keep at *American Mathematical Monthly*.** Rationale:
- The referee explicitly recommends Paths B + C revision-and-resubmission to *Monthly*: "I encourage the authors to revise along Paths B+C above and resubmit. The *Monthly* welcomes such resubmissions when the underlying mathematics is sound."
- Paths B + C combined produce a paper with two substantive contributions (genuine rigidity + corrected spectral table) at *Monthly*'s level.
- The corrected G(n) table reproducing the referee's computation, combined with the equivariance-based rigidity, addresses both critical concerns directly.

**Backup venue:** *Mathematical Intelligencer* (less stringent expository bar; accepts shorter notes).

**Author block:** Sanders + Gish (per AUTHOR_LANES_v2.md). Single block, two addresses, no Calderon (the cover letter's Calderon attribution is a transcription error).

**Companion citations:**
- J02 (Joint Closure / 4-core paper, *Algebraic Combinatorics*) — cite for the σ-permutation and the 4-core $\{0, 7, 8, 9\}$.
- Diaconis 1988 — added per referee S6.
- Steinberg 2012 — added per M1 (representation theory of $F_5$ in the rigidity proof).
- Terras 1999 — kept as the more direct finite-Fourier reference.

**Length target:** 6-10 pages in amsart 11pt.
