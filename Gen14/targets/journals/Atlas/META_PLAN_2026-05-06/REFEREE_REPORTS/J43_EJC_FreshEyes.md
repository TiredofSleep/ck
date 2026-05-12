# Referee Report: J43 / European Journal of Combinatorics (Fresh Eyes)

**Manuscript:** "Spectral Layer Consolidation: $G_6$, $G_7$, $G_8$ from the Q-Series Architecture on $\mathbb{Z}/10\mathbb{Z}$"
**Authors:** B. R. Sanders, C. A. Luther
**Submitted to:** European Journal of Combinatorics
**Reviewer:** External referee (fresh-eyes; no prior knowledge of the broader research program)
**Date:** 2026-05-07

---

## §1 Summary of the manuscript

The paper consolidates three previously-stated results about the permutation
$$\sigma = (0)(3)(8)(9)(1\;7\;6\;5\;4\;2)\in S_{10}$$
acting on $\mathbb{Z}/10\mathbb{Z}$:

- **G6 (Periodicity).** $\sigma^6 = \mathrm{id}$.
- **G7 (Period distribution).** $P(\tau=1)=2/5$, $P(\tau=6)=3/5$, $\bar\tau = 4$, $\mathrm{Var}(\tau)=6$.
- **G8 (Spectral coherence integral).** Defining $\chi:\mathbb{Z}/10\to\{-1,0,+1\}$ by $\chi^{-1}(0)=\{0,3,8,9\}$, $\chi^{-1}(+1)=\{1,4\}$, $\chi^{-1}(-1)=\{2,5,6,7\}$, and
$$G(s) = \Big|\sum_{j=0}^{8} \omega^{j}\,\chi(\sigma^{j}(s))\Big|^{2}, \qquad \omega=e^{2\pi i/9},$$
the paper claims $G$ takes exactly three values: $0$ at the four fixed points, $G_{\rm low}\approx 1.872$ on $\{1,2,4,6\}$, and $G_{\rm high}\approx 9.389$ on $\{5,7\}$.

Layers 1--4 of a six-layer "Q-series architecture" are claimed; layers 5 and 6 are deferred to companion papers.

I re-derived G6 and G7 by direct enumeration in `numpy/sympy` (under one second). I re-evaluated $G(s)$ for all $s\in\mathbb{Z}/10$ in `python` with $\omega=e^{2\pi i/9}$ (under five seconds).

---

## §2 Decision recommendation

**Major revisions.** There is one disqualifying inconsistency: the paper's Theorem G8 states a specific assignment of $G_{\rm low}$ and $G_{\rm high}$ to particular subsets of $\mathbb{Z}/10$, and on independent computation that assignment is wrong. The numerical values $\{0,\approx1.872,\approx9.389\}$ are correct; the partition of $\{1,2,4,5,6,7\}$ into low- and high-locus subsets is not as stated. This must be fixed before publication. The remaining content (G6, G7, the consolidation framing) is sound and well-written.

---

## §3 Major comments

### 3.1 G8 partition error: the high-locus is $\{4,7\}$, not $\{5,7\}$

This is the dominant issue.

The manuscript (§4.2 Table, §4.3 paragraph "$G(5)=G(7)$ identification follows from the $P_{56}$-action") asserts:

| $s$ | $G(s)$ |
|-----|--------|
| $\{0,3,8,9\}$ | $0$ exactly |
| $\{1,2,4,6\}$ | $\approx 1.872$ |
| $\{5,7\}$ | $\approx 9.389$ |

On independent computation with the character $\chi$ defined in §4.1 of the manuscript and the cycle $\sigma$ defined in §1, the values are:

| $s$ | $G(s)$ (computed) |
|-----|--------|
| $0$ | $0.0000$ |
| $1$ | $1.8716$ |
| $2$ | $1.8716$ |
| $3$ | $0.0000$ |
| $4$ | $\mathbf{9.3892}$ |
| $5$ | $\mathbf{1.8716}$ |
| $6$ | $1.8716$ |
| $7$ | $9.3892$ |
| $8$ | $0.0000$ |
| $9$ | $0.0000$ |

The high-locus pair is $\{4,7\}$, not $\{5,7\}$, and the low-locus quadruple is $\{1,2,5,6\}$, not $\{1,2,4,6\}$.

This is not a minor typo. The claimed pair $\{5,7\}$ is what the paper calls "the BALANCE/HARMONY pair," and §4.4 reads the spectral concentration on this pair as the structural signature linking to the framework's Riemann-style demand. The actual computed pair $\{4,7\}$ doesn't have the same internal-architecture interpretation; the elements $4$ and $7$ in the cycle $(1\;7\;6\;5\;4\;2)$ sit at $\sigma$-positions $1$ and $4$ respectively (counting from element 1 as position 0), which is a relation through $\sigma^3$ (applying $\sigma$ three times to $7$ gives $4$). This relation is structurally distinct from the $P_{56}$-symmetry the paper invokes.

I cannot tell from the present manuscript whether (i) the paper's character $\chi$ assignments are slightly wrong (perhaps $\chi(4)$ should be $-1$ rather than $+1$, or $\chi(5)$ should be $+1$ rather than $-1$), or (ii) the cycle $\sigma$ is slightly different from the cycle I used, or (iii) the paper's identification of which pair is the "BALANCE/HARMONY pair" is the part that needs adjustment. The text references companion paper [J39] for the "$P_{56}$-action" justifying $G(5)=G(7)$, which I cannot independently consult; but as the manuscript stands, the claim $G(5)=G(7)\approx 9.389$ is not verified by the explicit definitions in §1 and §4.1.

The author should:
1. State $\chi$ and $\sigma$ unambiguously enough that an external referee with `python+numpy` can reproduce the table in five lines of code.
2. Either (a) provide the symbol-by-symbol enumeration that yields the claimed $\{5,7\}$ identification, or (b) update the partition to match the actual values (high-locus $\{4,7\}$, low-locus $\{1,2,5,6\}$) and rewrite the §4.4 reading accordingly.
3. Clarify whether the "$G(5)=G(7)$ via $P_{56}$" claim is an algebraic identity from the [J39] companion that contradicts (i.e., implies different $\chi$ or $\sigma$) or augments the explicit definitions of §4.1.

This must be resolved before publication; the table is the load-bearing claim of the third theorem.

### 3.2 Verification scripts not bundled

The Reproducibility section of the cover letter promises "$G_6$, $G_7$, $G_8$ all numerically reproducible from corpus scripts" but the manuscript cites only `papers/G6_*.md`, `papers/G7_*.md`, `papers/G8_*.md` as source documents. There is no script in the J43 manuscript folder. Given the §3.1 issue, a single self-contained `verify_g6_g7_g8.py` (under 50 lines, `numpy+cmath` only) that runs in seconds would close the issue at refereeing speed.

### 3.3 Q-series architecture: layers 5 and 6 are advertised but not delivered

The introduction promises a "six-layer Q-series architecture" (§1 table), but the paper covers only layers 1--4. Layers 5 (TSML/BHML 73/28 cell counts) and 6 (4-core attractor at $\alpha=1/2$) are deferred to [J9] and [J41]. This is honest, but the framing ("Together, $G_6$, $G_7$, $G_8$ form Layer 4 of the 6-layer Q-series architecture") leaves the reader expecting a unified architecture argument that the paper does not provide. If the consolidation is just of layers 1, 3, 4 (the polynomial layer 2 is "trivial / classical" per the §1 table), that should be stated up front.

---

## §4 Minor comments

### 4.1 Theorem G7 statement vs. proof

The theorem states "$\tau(s) \in \{1,6\}$" implicitly through the bimodal claim; the proof (§3.2) shows $\tau \mid 6$ first (so $\tau\in\{1,2,3,6\}$) and then rules out $\tau\in\{2,3\}$ via the cycle structure. This is fine but could be made tighter: state Theorem G7 with the divisibility structure first, then note that $2, 3$ are realized by no element. Right now the proof has to do this work for the reader.

### 4.2 G7 mean and variance computed for completeness

$\bar\tau = 4$, $\mathrm{Var}(\tau)=6$. The §3.3 paragraph attempts a connection to $T^*=5/7$ via $T^* = (\bar\tau-1)/\bar\tau=3/4$ but admits this is "not quite" right and flags the route through the squarefree-rate theorem [J01] as the actual derivation. This is honest scoping but reads as a half-finished thought; either drop the half-derivation or state the actual route (briefly) so that the reader of the standalone consolidation doesn't carry away the wrong impression of why $T^*=5/7$.

### 4.3 G8 closed forms in $\mathbb{Q}(\zeta_9)$

§4.3 promises that "the closed forms in $\mathbb{Q}(\zeta_9)$ are algebraic (sums of cyclotomic units) and are documented in `papers/G8_TRAJECTORY_COHERENCE_INTEGRAL.md`. We do not present the closed forms here." For an EJC paper, the cleanest closed-form expression of $G_{\rm low}$ and $G_{\rm high}$ as elements of $\mathbb{Q}(\zeta_9)$ would be the natural thing to include; if the closed form is not yet known, that should be stated clearly as an open question (Conjecture? Open Problem?) rather than as a deferred-to-corpus side note. The "not presented here" framing leaves the reader unsure whether the closed forms exist and have been suppressed for length, or whether they remain open. (Given the spectral-combinatorics audience EJC has, this is a question they would want a definitive answer to.)

### 4.4 The character $\chi$ feels unmotivated

§4.1 introduces $\chi:\mathbb{Z}/10\to\{-1,0,+1\}$ with the assignments $\{1,4\}\mapsto+1$, $\{2,5,6,7\}\mapsto-1$, $\{0,3,8,9\}\mapsto 0$, citing "the canonical $\beta$-exception character" of [J48]. The justification reads as if it requires the [J48] context, but the character itself is the central spectral object of G8. An EJC reader does not have [J48] open. The paper would be substantially stronger with one paragraph explaining where $\chi$ comes from in self-contained terms (e.g., "$\chi(s) = +1$ iff the $\beta$-polynomial value at $s$ is $+1$, $\chi(s)=-1$ iff $\beta(s)=-1$, $\chi(s)=0$ iff $s$ is a $\sigma$-fixed anchor with $\beta(s)=0$"). Otherwise the character looks like the choice that makes the spectral theorem work, which is what the §4.4 reading is trying to escape.

### 4.5 Per-venue note in cover letter is non-standard

The cover letter explicitly flags this as "the 3rd EJC submission of the J-series" and names fallback venues (Linear Algebra and its Applications, PLOS ONE). EJC editors may find this odd. Per-venue cap management is an internal logistics question and ought not to be visible in the submission letter; let the editor decide whether the EJC slate is over-subscribed. (Recommend: drop the per-venue note from the cover letter; keep it in internal documents.)

### 4.6 Citation hygiene

The §5.1 citation list refers to "this paper [J51]," but in the published version this paper IS the cited reference; if the paper is intended to be cited as J43, that string should be normalized. Internal renumbering between J51 and J43 is visible throughout (the manuscript path is `J51_spectral_layer_consolidation.md` but the folder is `J43`). Final-version manuscript should pick one number and use it consistently, including in the BibTeX entry.

### 4.7 Theorem statement style

The three theorems are stated as "Theorem G6", "Theorem G7", "Theorem G8" — these labels match the corpus naming but read as obscure mnemonic-tags in the published paper. EJC convention would be Theorem 2.1 (Periodicity), Theorem 3.1 (Period Distribution), Theorem 4.1 (Spectral Coherence) with the G-labels parenthesized or footnoted. Cosmetic; no action required, but worth considering.

---

## §5 Independent verification

I executed a five-line `python` script:

```python
import cmath, math
sigma = {0:0, 3:3, 8:8, 9:9, 1:7, 7:6, 6:5, 5:4, 4:2, 2:1}
chi = {0:0, 3:0, 8:0, 9:0, 1:+1, 4:+1, 2:-1, 5:-1, 6:-1, 7:-1}
omega = cmath.exp(2j*math.pi/9)
def G(s):
    cur, total = s, 0
    for j in range(9):
        total += (omega**j) * chi[cur]
        cur = sigma[cur]
    return abs(total)**2
for s in range(10): print(s, round(G(s),4))
```

Output:

```
0 0.0   1 1.8716   2 1.8716   3 0.0     4 9.3892
5 1.8716  6 1.8716  7 9.3892   8 0.0    9 0.0
```

This (i) confirms G6 and G7 (reading $\sigma$-orbits and periods from the same dictionary), (ii) confirms the three-valued image $\{0, \approx 1.872, \approx 9.389\}$, but (iii) contradicts the §4.2 table's partition: high-locus is $\{4,7\}$ and low-locus is $\{1,2,5,6\}$, not the manuscript's $\{5,7\}$ and $\{1,2,4,6\}$.

---

## §6 Stronger contributions of the paper, not at issue

- **The integration framing** (§5) is genuinely useful: Periodicity → orbit-structure split → spectral concentration is a clean three-step story that does form a coherent layer in the larger architecture.
- **G6 proof is clean.** The $\mathbb{F}_2 \times \mathbb{F}_5$ coordinatization with the $(\alpha, \beta)$ polynomial form makes the closure of the orbit transparent, and the modular-arithmetic argument $4 \equiv 0 \pmod 2$ + $-5 \equiv 0 \pmod 5$ is exactly the right kind of two-line elementary proof.
- **G7 is forced from G6** + cycle structure. The bimodality is structurally inevitable; the explicit mean/variance computation is a useful service to downstream papers.
- **The honest scope (§6)** correctly identifies that the closed forms in $\mathbb{Q}(\zeta_9)$ are open and that generalization to higher $N$ is a separate question.

The paper deserves to be in EJC after the §3.1 issue is resolved. The bones are good.

---

## §7 Recommended action

1. **Fix the §4.2 G8 table.** Either (a) update to high-locus $\{4,7\}$, low-locus $\{1,2,5,6\}$, OR (b) provide the explicit definitions of $\chi$ and $\sigma$ that yield the claimed $\{5,7\}$ partition with a worked example, OR (c) provide the [J39] $P_{56}$-action argument in self-contained form so an EJC reader can see why $G(5)=G(7)$ algebraically despite the explicit numerical computation.

2. **Add a short verification script** (`verify_G_layer.py`, under 50 lines, `numpy+cmath` only) bundled in the submission.

3. **State $\chi$'s origin self-containedly** (§4.1).

4. **Tighten the §1 architecture framing** to make clear the paper covers layers 1--4 only.

5. **Consider whether the G-labels are useful** in the final EJC version.

After these changes, I expect this to be a clean accept.

---

## §8 Score sheet

| Criterion | Score (1--5) | Comment |
|-----------|-------|---------|
| Correctness of stated results | 3 | G8 partition mis-stated; G6, G7 correct |
| Novelty | 3 | Consolidation of corpus material; layered reading is the new contribution |
| Significance for combinatorics | 3 | Niche but coherent; the three-valued spectral signature is a genuine observation |
| Exposition | 4 | Clear, well-organized, honest scope |
| Reproducibility | 3 | Numerical claims independently checkable; G8 partition claim fails on first check; no bundled script |
| Fit for EJC | 4 | Spectral + permutation-group + cyclotomic combinatorics is on-topic |

**Recommendation:** Major revisions, with rapid resubmission expected after the §3.1 G8-table fix.
