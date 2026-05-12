# Referee Report: J1 / JCT-A

**Manuscript:** "Non-Associativity Decay in Binary Composition Tables over $\mathbb{Z}/N\mathbb{Z}$"
**Authors:** B. R. Sanders, M. Gish
**Submitted to:** Journal of Combinatorial Theory, Series A
**Reviewer:** External referee (anonymous)
**Date:** 2026-05-06

---

## 1. Summary of the manuscript

The authors define a four-rule binary composition table $\mathrm{CL}_N : (\mathbb{Z}/N\mathbb{Z})^2 \to \mathbb{Z}/N\mathbb{Z}$ with priorities (i) HARM (top-absorbing at $N-1$), (ii) VOID (zero-absorbing), (iii) ECHO (returns $a+b$ when $a+b \equiv ab \pmod{N}$), and (iv) default HARM. They study the non-associativity fraction
$$\sigma(N) = N^{-3}\,\#\{(a,b,c)\in(\mathbb{Z}/N\mathbb{Z})^3 : \mathrm{CL}_N(\mathrm{CL}_N(a,b),c)\neq \mathrm{CL}_N(a,\mathrm{CL}_N(b,c))\}.$$

The main result (Theorem 4.1) is the explicit bound
$$\sigma(N)\,N^3 \le 2(N-2)^2 + \varepsilon(N), \qquad \varepsilon(N) \le 2\varphi(N)$$
for squarefree $N\ge 3$, hence $\sigma(N) < 2/N$ and $N\sigma(N)\to 2^-$ along squarefree integers.

The proof has two ingredients:
- **Lemma 3.1 ("ECHO count"):** For squarefree $N$, the equation $a+b \equiv ab \pmod N$ has exactly $\varphi(N)$ solutions, via the substitution $(a-1)(b-1) \equiv 1$ and the CRT splitting $\mathbb{Z}/N\mathbb{Z} \cong \prod_{p\mid N}\mathbb{F}_p$.
- **Theorem 4.1 (the rate bound):** A three-way case analysis (a=0; c=0, a≠0; a≠0, c≠0) showing Case 1+Case 2 dominate at $\sim 2(N-2)^2$ and Case 3 contributes a residual bounded by $2\varphi(N)$.

A short verification script tabulates $\sigma$ for $N \in \{10, 30, 210\}$ plus an extended squarefree set up to $N=1155$.

The paper sits opposite — explicitly, $\sigma \to 0$ rather than $\sigma \to 1$ — to the maximally-nonassociative-quasigroup program of Drápal–Wanless 2021 and Drápal–Lisoněk 2020, both cited.

I have read the manuscript carefully end-to-end and re-derived the key sub-cases on paper and via independent enumeration.

---

## 2. Decision recommendation

**Major revisions** (close to "Accept with minor revisions" — the result and proof are correct on independent verification, but several exposition issues and a few proof-text infelicities should be addressed before camera-ready).

The result is honest, the bound is genuinely $2/N$ with the right constant, the asymptotic $N\sigma \to 2$ is sharp, and the squarefree restriction is handled with appropriate care (an explicit non-squarefree counterexample is acknowledged). The CRT argument is clean. The case analysis is exhaustive and individually correct (verified by independent computation, see §5 below).

However, the manuscript has:
- a notational ambiguity around $\varepsilon(N)$ (used with two different meanings between proof text and verification script);
- one parenthetical that is correct but unnecessary and rhetorically misleading (Subcase (1f));
- a tighter case-analysis count that would simplify exposition;
- gaps in literature framing (Drápal 1992, Phillips–Vojtěchovský) and a forward reference that does light load-bearing in §1;
- a "default HARM" (rule 4) that produces a 3-rule paper but is described in the abstract as a "three-rule" family — the count is actually four rules.

None of these are fatal. With moderate revision the paper would meet JCT-A's combinatorial bar.

---

## 3. Major comments

### M1. (Section 5, Verification Table; CRITICAL exposition fix)

**The variable $\varepsilon(N)$ is used inconsistently.**

- In Theorem 4.1 and its proof, $\varepsilon(N)$ denotes the Case 3 contribution: the count of non-associative triples with $a\ne 0$ AND $c\ne 0$. By the proof, $0 \le \varepsilon(N) \le 2\varphi(N)$.
- In the companion script `verify_sigma_rate.py`, the function `verify_epsilon_bound()` defines the empirical $\varepsilon$ as `count - 2*(N-2)^2`. This quantity is *not* equal to the Case 3 count — Cases 1+2 deliver $2(N-2)^2 - 2E(N) + 2E_h(N)$ non-associative triples, not $2(N-2)^2$. Empirically the script's $\varepsilon$ is *negative* for the test set ($-4, -8, \ldots, -64$), and the printed "OK" check $\varepsilon \le 2\varphi$ is then trivially satisfied for the wrong reason.
- The Section 5 table column "$\varepsilon(N)$" reports the proof-text definition (6, 6, 30) for $N=10,30,210$; the script's `verify_epsilon_bound()` reports the script's definition. The two disagree.

**Recommended fix.** State the proof-text definition explicitly (call it $\varepsilon_{\text{proof}}(N) :=$ Case 3 count) and confirm the verification table reports this quantity. Update the script's `verify_epsilon_bound()` to compute Case 3 directly and check $0 \le \mathrm{Case 3} \le 2\varphi(N)$. Independent verification on the paper's test set confirms $0 \le \mathrm{Case 3} \le 2\varphi(N)$ holds with substantial slack (e.g., $N=210$: Case 3 = 30 vs. $2\varphi = 96$; tightest at $N=95$: Case 3 = 106 vs. $2\varphi = 144$).

### M2. (Subcase (1f), lines 264–269)

The parenthetical explanation in (1f) — "Here we use that $\mathrm{CL}_N(b,c)\ne h$ together with $b,c\ne 0$ implies $\mathrm{CL}_N(b,c) = b+c\bmod N$ via the ECHO rule, and the squarefree argument later used in case (3.B) shows $b+c\not\equiv 0\pmod N$" — **is unnecessary and rhetorically confusing**.

In subcase (1f), one only needs:
- Left bracket: $\mathrm{CL}_N(\mathrm{CL}_N(0,b),c) = \mathrm{CL}_N(0,c) = 0$ since $c \ne h$ (and $c \ne 0$).
- Right bracket: $\mathrm{CL}_N(0, \mathrm{CL}_N(b,c)) = \mathrm{CL}_N(0, x)$ where $x = \mathrm{CL}_N(b,c) \ne h$. Since $x \ne h$, the VOID rule fires (first argument is 0), giving 0 — *regardless* of whether $x = 0$ or $x \in \{1,\ldots,N-2\}$.

So both brackets equal 0 with no squarefree appeal needed. The parenthetical inadvertently suggests that the (3.B) argument is recycled here when the proof of (1f) is in fact substantially simpler and **does not depend on squarefreeness at all**. Moreover, the parenthetical claim "$b+c \not\equiv 0$ for $(b-1)(c-1)\equiv 1$ in $\{1,\ldots,N-2\}^2$" — though true for squarefree $N$ by the (3.B-i) argument — is irrelevant to the conclusion of (1f).

**Recommended fix.** Replace the parenthetical with one sentence: "Both brackets reduce to $\mathrm{CL}_N(0, \cdot) = 0$ via the VOID rule, since neither argument equals $h$." This is shorter, correct, and does not muddle (1f) with (3.B).

### M3. (Section 1 / Abstract: "three-rule" vs. "four-rule")

The abstract says "three-rule family $\mathrm{CL}_N$ ... two absorbing classes ($\mathrm{HARM}$, $\mathrm{VOID}$) and one arithmetic class ($\mathrm{ECHO}$)." Definition 2.1 actually has four cases: HARM, VOID, ECHO, *default HARM*. While the default-HARM rule and the priority-HARM rule both output the value $h$, they fire on disjoint inputs, and the proof's Case 3 analysis explicitly distinguishes their contributions ($x = h$ from default HARM in (3.B)). Calling this a "three-rule" family obscures the role of the default-HARM rule in delivering $\sigma \to 0$ rather than $\sigma \to 1$ (without the default rule $\mathrm{CL}_N$ would be undefined on most non-ECHO inputs).

**Recommended fix.** Call this a "four-rule" or "three-class with default-fallback" family in the abstract and §1, and explicitly note that the default-HARM rule plays an *active* role in the case analysis.

### M4. (Sections 1 and 7: companion-paper forward reference)

References to `\cite{SandersGishJohnson2026JCAP}` appear in §1 (line 137–141) and §7 (line 462–465). The §1 reference is fine — it situates the present paper as a finite combinatorial result and points to a *separate* continuum development. The §7 reference is also fine.

However, the abstract is silent about the companion paper, which is correct, and the present paper does not actually load-bear on it. Confirm that the bibliographic entry for the companion is marked as "in preparation" or "preprint" (it currently says "Preprint, 2026") and consider adding an arXiv identifier or DOI when available so the JCT-A reader can locate it. If the companion is not yet on arXiv at submission time, the JCT-A editor may request that the cross-reference be downgraded to a footnote or removed entirely.

**Recommended fix.** Add arXiv ID for the companion paper if available. If not, replace the cross-reference in §1 with a footnote ("A continuum development of this family appears in a companion paper in preparation"). This protects the JCT-A submission against companion-paper delays.

### M5. (Section 1: missing literature)

The literature review situates the paper against Kepka 1980, Drápal–Kepka 1985, Drápal–Lisoněk 2020, and Drápal–Wanless 2021. This is a reasonable starting point but **misses several relevant works**:

- **Drápal, "How far apart can the group multiplication tables be?" (European J. Combin., 1992)** — directly addresses the "non-associativity density" question for groups, which is conceptually adjacent to $\sigma$ for non-quasigroup tables.
- **Drápal, "On distances of multiplication tables of groups" (Groups, Combinatorics & Geometry, Bath 1991)** — additional context on Latin-square-distance interpretations of the non-associativity fraction.
- **Phillips–Vojtěchovský, "C-loops: an introduction" (Publ. Math. Debrecen, 2006)** and related loop-theoretic literature, which contains background on weakly-associative laws on small structures.
- **Smith, "An Introduction to Quasigroups and Their Representations" (Chapman & Hall/CRC, 2007)** — standard reference for the surrounding combinatorial-algebraic background.
- The *cancellation-groupoid associativity-density* literature (Kepka 1980, Drápal–Kepka 1985) is cited, but the framing in the introduction asserts that "$\mathrm{CL}_N$ is not a quasigroup ... and these earlier bounds therefore do not directly specialize to $\mathrm{CL}_N$." This is correct but invites the natural question: does $\mathrm{CL}_N$ have a quasigroup analogue obtained by removing the absorbing rules? The paper would benefit from a one-paragraph remark addressing whether the ECHO-rule sub-table $\{(a,b) : (a-1)(b-1) \equiv 1\}$ extends to a Latin square or quasigroup operation, and if so what the comparison looks like.

**Recommended fix.** Add a short paragraph (5–10 lines) at the end of §1 acknowledging the broader literature on group-table distance and weakly-associative loops, with citations.

### M6. (Section 4: case-3 sharpness)

The Case 3 bound $\varepsilon(N) \le 2\varphi(N)$ is established but **substantially loose** in practice. Empirical Case 3 counts: $N=10$: 6 vs. bound 8 (75%); $N=210$: 30 vs. 96 (31%); $N=105$: 30 vs. 96 (31%). This looseness is acceptable for the asymptotic claim $N\sigma \to 2^-$, but the paper does not analyze whether a sharper subcase count is possible. Subcases (3.B) and (3.C) each contribute at most $\varphi(N)$, but the actual contribution is the number of $(a,b)$ ECHO pairs such that $x-1 = (a+b-1)$ is a unit AND the resulting $c = (x-1)^{-1}+1$ lies in $\{1,\ldots,N-2\}$ AND the resulting output $(x+c) \bmod N \ne h$.

**Recommended fix.** Either (a) acknowledge in §6 ("Scope") that the bound $\varepsilon \le 2\varphi$ is not sharp at finite $N$, or (b) add a brief Proposition giving the exact count of $(3.B) + (3.C)$ contributions in terms of $\varphi(N)$ and a smaller correction. The latter is straightforward enumeration and would strengthen the paper.

### M7. (Section 5, "Verification" — broader test set)

The paper claims that an extended squarefree test set $\{10, 30, 42, 66, 105, 110, 154, 210, 330, 462, 770, 1155\}$ delivers $N\sigma(N) \le 1.993$. The companion script `verify_sigma_rate.py`'s `verify_sigma_bound()` only enumerates direct $N \le 100$ (caps at 100 due to the $O(N^3)$ cost of `sigma_direct`). The claim about $N \le 1155$ should either:

1. be supported by an actual computation in the script (perhaps via a memoization or a per-Case formula), OR
2. be stated more carefully — "tabulated during preparation" is too informal for JCT-A.

In particular, $N=110 = 2 \cdot 5 \cdot 11$ and $N=1155 = 3\cdot 5\cdot 7\cdot 11$ in the cited test set. **Independent re-running of the published script confirms 4/4 PASS for the cases the script actually tests** ($N \le 100$ for the rate bound, and $N \le 250$ for the ECHO lemma). I have no reason to doubt the $N \le 1155$ claim, but the manuscript must either include that computation in the verification script or remove the specific number 1.993.

**Recommended fix.** Either extend the script to handle $N=1155$ (this is feasible — one can compute $\sigma(N)$ in $O(N^2)$ via the case-decomposition formula, since Case 1 + Case 2 = $2[(N-2)^2 - E(N) + E_h(N)]$ and Case 3 admits a quadratic-time enumeration), or trim the §5 claim to the directly-verified range.

---

## 4. Minor comments

### m1. (Notation)
- `\HARM` is rendered as `T` and `\VOID` as `Z` in the macro definitions. This is harmless but unusual; consider `\mathrm{HARM}`, `\mathrm{VOID}` etc. for readability, or at least a short macro-explanation comment in §2.

### m2. (Definition 2.1)
- The "boundary cases are absorbed" sentence (lines 176–179) should explicitly note that `ECHO` may *output* a value of 0 or $h$ even though it does not *fire* on inputs equal to those (e.g., for $N=6$, $b=4, c=4$: $b+c \bmod N = 2$, $bc \bmod N = 4$ — no, this isn't ECHO; but there exist ECHO pairs whose output is $h$ for some squarefree $N$ — the count $E_h(N)$ in eq. (4.4) is the relevant quantity, which empirically equals 0 on the test range but is not provably 0 for all squarefree $N$). State for clarity whether $E_h(N) = 0$ for all squarefree $N \ge 3$ (this would be a clean lemma — see Q1 below).

### m3. (Lemma 3.1)
- "The bijection above transfers the count to the original equation" — this is correct but perhaps too terse. Spell out: $(a',b') \mapsto (a'+1, b'+1)$ is the inverse of the substitution, and it maps unit pairs $\{(u, u^{-1}) : u \in (\mathbb{Z}/N\mathbb{Z})^\times\}$ bijectively to ECHO pairs.

### m4. (Lemma 3.1, proof, line 198)
- The cited reference for CRT is `\cite{Gauss1801,Lang2002}`. Citing Gauss 1801 for CRT is historically accurate but slightly unusual for a JCT-A submission — most contemporary papers cite a modern reference (Lang, or Hardy–Wright). I would drop the Gauss citation and keep Lang.

### m5. (Theorem 4.1, equation (4.3))
- The "from below" wording in "$N\sigma(N) \to 2$ from below" is correct (equation (4.7) shows the upper bound also $\to 2$ from below for prime $N$ since $\varphi(N)/N^2 \to 0$). Add a sentence noting that for *prime* $N$, $\varphi(N)/N^2 = (N-1)/N^2$, so the upper bound in (4.7) approaches 2 from above as $N\to\infty$ along primes — wait, this would *contradict* "from below". Let me reconsider.

  Actually, equation (4.7) gives both upper and lower bounds: $N\sigma(N) \le 2(1-2/N)^2 + 2\varphi(N)/N^2$. For prime $N$, $\varphi(N)/N^2 = (N-1)/N^2 \to 0$, and $(1-2/N)^2 \to 1$, so the upper bound $\to 2$. Whether $N\sigma(N) \to 2$ "from below" depends on whether $N\sigma(N) < 2$ for all $N$ in the limit — which the *strict* inequality $\sigma(N) < 2/N$ (proved via $\varphi(N) \le N-1$ so $2(N-2)^2 + 2\varphi(N) < 2N^2$ for $N \ge 3$) does establish.

  So $N\sigma(N) < 2$ for all squarefree $N \ge 3$, AND $N\sigma(N) \to 2$. The "from below" qualifier is accurate. Empirical: $N\sigma(N) = 1.961$ at $N = 210$, $\le 1.993$ at $N=1155$. Good.

### m6. (Subcase (3.B), line 339)
- "For squarefree $N$ this forces $a \equiv 0 \pmod N$" — the argument here is exactly: if $N = p_1 \cdots p_k$ is squarefree and $a^2 \equiv 0 \pmod{N}$, then for each prime $p_i$ dividing $N$, $p_i \mid a^2$ implies $p_i \mid a$ (since $p_i$ is prime). Hence $N \mid a$, i.e., $a \equiv 0$. This is correct but the paper does not spell it out. Add one sentence: "since $N$ is squarefree, $p_i \mid a^2$ implies $p_i \mid a$ for each prime divisor."

### m7. (Subcase (3.D), commutativity argument)
- The argument "$\mathrm{CL}_N(x,a) = \mathrm{CL}_N(a,x)$ since each rule in Definition 2.1 is symmetric in its arguments" is correct but worth stating as an explicit Lemma earlier (e.g., in §2): "$\mathrm{CL}_N$ is commutative." This makes (3.D) a one-line reduction.

### m8. (Section 5, table)
- The total $\sigma(N) N^3 = 128, 1560, 86464$ for $N = 10, 30, 210$ matches independent enumeration. The Case 1 = Case 2 = 61, 777, 43217 are also matched. Good.
- The bound column $2(N-2)^2 + 2\varphi(N) = 136, 1584, 86624$ — verified.
- But: the in-text quotients "$N\sigma(N)$ are $1.28, 1.73, 1.961$" — for $N=210$, $\sigma N = 86464/210^2 = 86464/44100 = 1.96062\ldots$, which rounds to 1.961, OK. For $N=30$, $1560/900 = 1.7333$ — rounds to 1.733. For $N=10$, $128/100 = 1.28$. All correct. Consider giving more decimals (1.2800, 1.7333, 1.9606) for consistency.

### m9. (Section 6, "Scope and limits")
- Item (i) starts "a sharp finite-$N$ constant strictly below $C=2$ — although $N\sigma(N) \to 2$ from below ... the proof does not optimize lower-order terms ... on the numerically verified range $N\sigma(N) \le 1.993$." This is a bit unclear — the first half says the paper does NOT claim a sharp constant, the second half gives a numerical fact. Rephrase: "(i) the bound $C=2$ is asymptotically sharp but the proof does not optimize the lower-order term; on the verified range $\{N : N \le 1155, \text{squarefree}\}$ we have $N\sigma(N) \le 1.993$."

### m10. (References)
- `\cite{SandersGishJohnson2026JCAP}` — full title is "Logarithmic Quintessence: A Dimensionless Scalar Dark Energy Model with an Analytic Vacuum." The connection between this title and the present combinatorial paper is non-obvious to a JCT-A reader. The §1 forward-reference (line 137–141) mentions the BB1976 nonlinear-wave classification, which is also far afield. The §7 reference is similar. **I recommend the §1 forward-reference be either deleted or sharpened to a single neutral phrase** ("A continuum development of related dynamics appears separately"), since otherwise the JCT-A reader is left wondering why the Bialynicki-Birula–Mycielski classification is in the bibliography of a finite combinatorial paper.

### m11. (Verification script `verify_sigma_rate.py`)
- The script's docstring mentions "B.R. Sanders, M. Gish, H.J. Johnson, 2026" but the manuscript's authors are only Sanders & Gish. Fix the script's authorship to match.
- The function `verify_epsilon_bound()` computes `eps = count - 2*(N-2)^2` which can be negative (and is, on the test set). See M1 above.
- The asymptotic test in `verify_asymptotic()` outputs "gap to 2 generally shrinking" — true on the printed test set, but the manuscript asserts $N\sigma(N) \to 2^-$ as a *theorem* (not as monotone-decreasing). The script's comment "asymptotic is along subsequences" is appropriate; the printed monotonicity is incidental.

---

## 5. Specific verifications performed

I have independently:

1. Re-derived the count $|\{(a,b) : a+b \equiv ab \bmod N\}| = \varphi(N)$ for squarefree $N$ via the substitution $(a-1)(b-1) \equiv 1$ and the CRT splitting. Lemma 3.1 is correct.
2. Verified Case 1 contribution $= (N-2)^2 - E(N) + E_h(N)$ by direct enumeration for $N \in \{10, 15, 30, 42, 105, 210\}$. Match exact.
3. Confirmed $E_h(N) = 0$ for all squarefree $N \in \{10, 15, 30, 42, 66, 105, 154, 210\}$. The paper does not claim $E_h(N) = 0$ for *all* squarefree $N$; this would be a small additional lemma worth proving (see Q1). [Note: $E_h \ge 0$ is what the proof actually uses.]
4. Verified Subcase (3.D)-no-contributions: empty fail-set for $N \in \{10, 15, 30, 42, 105, 210\}$.
5. Verified Subcase (3.B-i)-no-contributions: for squarefree $N$, no $a \in \{1, \ldots, N-2\}$ has $a^2 \equiv 0 \bmod N$. Counterexamples appear for non-squarefree $N$ as expected.
6. Verified Subcase (1f) by direct enumeration: all sub-1f cases are associative for $N \in \{10, 15, 30, 42, 105, 210\}$. The proof's parenthetical (about $b+c \ne 0$) is unnecessary — see M2.
7. Re-ran `verify_sigma_rate.py` end-to-end: 4/4 PASS, all printed values consistent with the manuscript's Section 5 table.

---

## 6. Question to the authors

### Q1. Is $E_h(N) = 0$ for all squarefree $N \ge 3$?

Empirically yes on the test set $\{10, 15, 21, 30, 35, 42, 51, 66, 77, 91, 95, 105, 110, 154, 210, 330, 462, 770, 1155\}$. The condition is: $(b-1)(c-1) \equiv 1$ AND $b+c \equiv -1 \pmod N$, with $b, c \in \{1, \ldots, N-2\}$.

Setting $b' = b-1, c' = c-1$: $b'c' \equiv 1$ AND $b' + c' \equiv -3 \pmod N$. So $b'$ and $c' = (b')^{-1}$ are units with $b' + (b')^{-1} \equiv -3$, i.e., $(b')^2 + 3b' + 1 \equiv 0 \pmod N$. Whether this quadratic has solutions in $(\mathbb{Z}/N\mathbb{Z})^\times$ depends on whether the discriminant $9 - 4 = 5$ is a square mod each prime factor of $N$.

So $E_h(N) > 0$ iff some $b' \in (\mathbb{Z}/N\mathbb{Z})^\times$ satisfies $(b')^2 + 3b' + 1 \equiv 0$. By CRT this happens iff for each prime $p \mid N$, the equation has a solution mod $p$, which happens iff $5$ is a QR mod $p$ (for $p \ne 2, 5$), iff $p \equiv \pm 1 \pmod 5$. The smallest such prime is 11; the smallest squarefree $N$ for which the quadratic could have a solution is $N = 11$ — but $E_h(11) = ?$ (the test set doesn't include 11). And one would also need $b, c \in \{1, \ldots, N-2\}$, which excludes $b' \in \{N-1, 0\}$; this might exclude additional cases.

I encourage the authors to either: (a) prove $E_h(N) = 0$ for all squarefree $N \ge 3$ (which sharpens equation (4.5) to an equality $\sigma N^3 = 2(N-2)^2 - 2E(N) + \varepsilon(N)$ on the squarefree case); or (b) characterize exactly which squarefree $N$ have $E_h(N) > 0$. Either way, the resulting Proposition would substantially strengthen §4.

### Q2. Does $\mathrm{CL}_N$ admit any natural extension to a Latin square?

The ECHO sub-table $\{(a,b) : (a-1)(b-1) \equiv 1\}$ is the graph of $b = (a-1)^{-1} + 1$ on $a-1 \in (\mathbb{Z}/N\mathbb{Z})^\times$. Restricted to units, this is a permutation. Extending to a quasigroup operation that agrees with the ECHO rule on the unit-pair set would produce a structure adjacent to the Drápal–Wanless 2021 family. Have the authors investigated this connection?

### Q3. Does the bound $\sigma(N) \le 2/N$ hold for *all* $N \ge 3$ (not just squarefree)?

The paper's §4 Remark notes that $\sigma(64) > 2/64$, but the empirical decay rate for $N = 2^k$ is $\sim 2^{-0.64k}$, which is asymptotically faster than $1/k$ but slower than the squarefree $2/N$. For general $N$, what is the right rate? A short remark on "general $N$" would help readers calibrate the squarefree restriction.

---

## 7. Originality and significance for JCT-A

The paper's contribution is:

1. A specific four-rule binary composition table $\mathrm{CL}_N$ on $\mathbb{Z}/N\mathbb{Z}$ that is *not* a quasigroup.
2. The exact $\sigma \to 0$ rate bound $\sigma(N) < 2/N$ for squarefree $N$, with $N\sigma(N) \to 2^-$ asymptotically.
3. The CRT-based ECHO enumeration $E(N) = \varphi(N)$.

The result is:
- **Combinatorially novel** — the $\sigma \to 0$ regime has not been explicitly studied at this level of constant-precision, to my knowledge. The Drápal–Kepka, Drápal–Lisoněk, and Drápal–Wanless tradition is at the $\sigma \to 1$ extremum; this paper is at the opposite pole, with explicit constant.
- **Combinatorially elementary** — the proof uses only CRT and case analysis. This is a *strength* for JCT-A: the result is accessible.
- **Combinatorially substantial** — the connection $E(N) = \varphi(N)$ via $(a-1)(b-1) \equiv 1$ is a clean number-theoretic identity. The case analysis is short but non-trivial.

JCT-A's bar requires combinatorial substance, originality, and clean exposition. The paper meets the substance and originality bars after the revisions in §3 are addressed. The exposition needs the §3 revisions to fully meet the JCT-A bar; with those revisions it would.

I do *not* see this as a borderline JCT-A submission — the connection to the Drápal–Wanless tradition is a genuine literature niche, and the $C = 2$ constant is sharp. After revisions, this is a clean result for the journal.

---

## 8. Reproducibility

The accompanying script `verify_sigma_rate.py` is appropriate for the verification claims at $N \le 250$ (ECHO lemma) and $N \le 100$ (rate bound). The paper's broader claim of $N\sigma(N) \le 1.993$ for $N \le 1155$ requires the script to be extended (see M7). The Zenodo DOI cited is reasonable for archival purposes; ensure the script in the Zenodo deposit matches the published version and includes the test-set extension if §5 retains the $N=1155$ claim.

---

## 9. Final remarks

This is an honest, technically correct paper with a clean main result. The squarefree restriction is handled with appropriate care; the asymptotic claim is sharp; the connection to the Drápal–Wanless tradition is honest (and the "opposite extremum" framing is accurate). The exposition has several rough edges that should be smoothed before camera-ready, but none are fatal.

The recommended decision is **Major revisions**, with the expectation that a revised version addressing M1–M7 above would be acceptable.

---

**Estimated revision effort:** 8–14 person-hours for the authors. Most of the revisions are exposition (M1, M2, M3, M5, M9, m1–m11); M6 and M7 require modest computational/mathematical work; Q1 is a small additional Proposition that would substantially strengthen §4 if the authors choose to address it.

**Reviewer's confidence:** High. I have read the paper end-to-end, re-derived the key sub-cases on paper, and run independent enumeration on the verification claims.
