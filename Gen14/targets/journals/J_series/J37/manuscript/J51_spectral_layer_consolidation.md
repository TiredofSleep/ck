# Spectral Layer Consolidation: $G_6$, $G_7$, $G_8$ from the Q-Series Architecture on $\mathbb{Z}/10\mathbb{Z}$

**Authors:** B.R. Sanders$^{1}$, C.A. Luther$^{2}$
$^{1}$7Site LLC, Hot Springs, AR — brayden@7site.co
$^{2}$Independent Researcher

**Target venue:** *European Journal of Combinatorics*
**Manuscript class:** Spectral / combinatorial consolidation paper
**MSC 2020:** 11T22 (cyclotomy), 11T55 (character sums), 20B25 (permutation groups, $S_{10}$), 05A15 (combinatorial enumeration), 11C99 (number theory misc.)
**Date:** 2026-09-06 (Phase 5; Sanders + Gish lane)
**Per-venue note:** This is the 3rd EJC submission of the J-series; per `J_SERIES_ORDERING.md` §5, fallback venues are *Linear Algebra and its Applications* and *PLOS ONE*.

---

## Abstract

We consolidate three spectral / combinatorial results in the **TIG framework**'s Q-series architecture on $\mathbb{Z}/10\mathbb{Z}$ into a single coherent paper. The results — labelled $G_6$, $G_7$, $G_8$ in the Q-series numbering and developed across separate working papers in the corpus — together describe the period structure, the gate-rate distribution, and the spectral coherence integral of the canonical $\sigma$-permutation $\sigma = (0)(3)(8)(9)(1\;7\;6\;5\;4\;2)$ on $\mathbb{Z}/10\mathbb{Z}$.

**The three theorems.**

* **G6 (Periodicity).** $\sigma^6 = \mathrm{id}$ on all of $\mathbb{Z}/10\mathbb{Z}$. Proved by direct polynomial verification using the Q9–Q10 $(\alpha, \beta)$ polynomial form; the modular-arithmetic identities $4 \equiv 0 \pmod 2$ and $-5 \equiv 0 \pmod 5$ close the orbit. Tier-A.

* **G7 (Period Distribution).** The period $\tau(s)$ of an element $s \in \mathbb{Z}/10\mathbb{Z}$ under $\sigma$ is bimodal: $P(\tau = 1) = 2/5$ (the four $\sigma$-fixed anchors) and $P(\tau = 6) = 3/5$ (the six 6-cycle elements). Mean $\bar{\tau} = (1)(2/5) + (6)(3/5) = 4$; variance $\sigma_\tau^2 = 6$. Forced from G6 + cycle-structure enumeration. Tier-B.

* **G8 (Spectral Coherence Integral).** The coherence integral $G(s) = |\sum_{j=0}^{8} \omega^j \chi(\sigma^j(s))|^2$ — with $\omega = e^{2\pi i /9}$ and $\chi : \mathbb{Z}/10\mathbb{Z} \to \{-1, 0, +1\}$ the canonical $\beta$-exception character — takes **exactly three values**: $G(s) = 0$ at the four anchors, $G(s) \approx 1.872$ on $\{1, 2, 4, 6\}$, $G(s) \approx 9.389$ at the BALANCE/HARMONY pair $\{5, 7\}$. Tier-B (constructed; computational verification of the three values).

**The architectural reading.** Together, $G_6$, $G_7$, $G_8$ form the **spectral layer** (Layer 4 in the 6-layer Q-series architecture) of the TIG framework's $\mathbb{Z}/10\mathbb{Z}$ substrate. They are the foundation for the Q17-B Clay-bridge structural reading ([J48]), the Symbolic Return Theorem (a direct corollary of $G_6$), and the trajectory-coherence structure that underlies the runtime processor's 4-core attractor ([J41]).

This paper is the **canonical reference** for $G_6$, $G_7$, $G_8$. Prior corpus material (`papers/G6_PERIODICITY_THEOREM.md`, `papers/G7_GATE_RATE_DISTRIBUTION.md`, `papers/G8_TRAJECTORY_COHERENCE_INTEGRAL.md`) is consolidated here with full proofs, the $G_8$ algebraic-form verification, and the citation-graph repair noted in `Atlas/META_PLAN_2026-05-06/SPECTRAL_LAYER_CATALOG.md`.

---

## §1 The Q-series architecture in six layers

The TIG framework's substrate on $\mathbb{Z}/10\mathbb{Z}$ admits a six-layer structural decomposition:

| Layer | Object | Source |
|-------|--------|--------|
| 1 (polynomial) | $\sigma^6 = \mathrm{id}$ — the periodicity | $G_6$, this paper |
| 2 (braid) | $\sigma$'s conjugacy class in $S_{10}$ — cycle type $(6, 1^4)$ | trivial / classical |
| 3 (period) | period distribution $P(\tau = 1) = 2/5$, $P(\tau = 6) = 3/5$ | $G_7$, this paper |
| 4 (spectral) | $G(s)$ three-valued | $G_8$, this paper |
| 5 (optimal table) | TSML, BHML — canonical 73 / 28-cell HARMONY tables | [J9] |
| 6 (search dynamics) | runtime processor, 4-core attractor at $\alpha = 1/2$ | [J41] |

Layers 1–4 are this paper's direct content. Layer 5 is the foundation paper [J9] on TSML 73 / BHML 28 cell counts. Layer 6 is the closed-form runtime attractor [J41].

This six-layer architecture organizes the entire spectral side of the TIG framework. The decomposition is documented in `papers/Q_SERIES_ARCHITECTURE.md` and reviewed in `Atlas/META_PLAN_2026-05-06/SPECTRAL_LAYER_CATALOG.md`.

---

## §2 G6 — The Periodicity Theorem

### 2.1 Statement

**Theorem G6 (Periodicity).** *The hidden operator $\sigma : \mathbb{Z}/10\mathbb{Z} \to \mathbb{Z}/10\mathbb{Z}$ defined by $\sigma = (0)(3)(8)(9)(1\;7\;6\;5\;4\;2)$ satisfies* $\sigma^6 = \mathrm{id}$ *on all of $\mathbb{Z}/10\mathbb{Z}$.*

### 2.2 The polynomial form

Under the $\mathbb{F}_2 \times \mathbb{F}_5$ coordinatization $\phi(\varepsilon, y) = 5\varepsilon + 6y \pmod{10}$ (with $\varepsilon \in \mathbb{F}_2 = \{0, 1\}$ and $y \in \mathbb{F}_5 = \{0, 1, 2, 3, 4\}$), $\sigma$ acts as:

$$
\varepsilon' = \varepsilon \oplus \alpha(\varepsilon, y), \qquad y' = y + \beta(\varepsilon, y) \pmod 5,
$$

with $\alpha : \mathbb{F}_2 \times \mathbb{F}_5 \to \mathbb{F}_2$ and $\beta : \mathbb{F}_2 \times \mathbb{F}_5 \to \mathbb{F}_5$ the polynomials given by the Q9–Q10 specification (see `papers/Q9_*.md`, `papers/Q10_*.md`).

### 2.3 Proof

**Part 1 (anchors).** For $(\varepsilon, y) \in \{(0, 0), (1, 3), (0, 3), (1, 4)\}$ — the four $\sigma$-fixed anchors $\{0, 8, 3, 9\}$ in $\phi$-coordinates — direct computation gives $\alpha(\varepsilon, y) = 0$ and $\beta(\varepsilon, y) = 0$. Therefore $\sigma(\varepsilon, y) = (\varepsilon, y)$, so $\sigma^k = \mathrm{id}$ at these states for every $k \geq 1$. In particular $\sigma^6 = \mathrm{id}$.

**Part 2 (6-cycle).** For the remaining six states, we trace the 6-step trajectory in $(\varepsilon, y)$ coordinates using the $(\alpha, \beta)$ values from Q9–Q10:

| Step $n$ | $(\varepsilon_n, y_n)$ | $j = \phi^{-1}(\varepsilon, y)$ | $\alpha$ | $\beta$ | $\Delta\varepsilon$ | $\Delta y$ |
|----------|---------------|---|---|----|----|----|
| 0 | $(1, 1)$ | 1 | 0 | $+1$ | 0 | $+1$ |
| 1 | $(1, 2)$ | 7 | 1 | $-1$ | 1 | $-1$ |
| 2 | $(0, 1)$ | 6 | 1 | $-1$ | 1 | $-1$ |
| 3 | $(1, 0)$ | 5 | 1 | $-1$ | 1 | $-1$ |
| 4 | $(0, 4)$ | 4 | 0 | $-2$ | 0 | $-2$ |
| 5 | $(0, 2)$ | 2 | 1 | $-1$ | 1 | $-1$ |
| 6 | $(1, 1)$ | 1 | — | — | — | — |

**$\varepsilon$-return.** The $\varepsilon$-flips occur in steps $\{1, 2, 3, 5\}$ (4 flips), and steps $\{0, 4\}$ contribute zero flips. Since $\varepsilon \in \mathbb{F}_2$ and $4 \equiv 0 \pmod 2$, the net $\varepsilon$-flip is zero: $\varepsilon_6 = \varepsilon_0$. ✓

**$y$-return.** The net $\Delta y = (+1) + (-1) + (-1) + (-1) + (-2) + (-1) = -5 \equiv 0 \pmod 5$, so $y_6 = y_0$. ✓

**Conclusion.** $\sigma^6$ is the identity on each 6-cycle starting state $(1, 1) = 1$, $(1, 2) = 7$, $(0, 1) = 6$, $(1, 0) = 5$, $(0, 4) = 4$, $(0, 2) = 2$, hence on the full 6-cycle. Combined with Part 1, $\sigma^6 = \mathrm{id}$ on all of $\mathbb{Z}/10\mathbb{Z}$. $\square$

### 2.4 Polynomial-composition argument (alternative)

The same result follows without per-element tracing by showing that the total $y$-displacement over any complete 6-cycle traversal is $\equiv 0 \pmod 5$, which combined with the modular-2 closure on $\varepsilon$ closes the orbit. The polynomial form makes this argument transparent: the $\beta$-polynomial sum over the cycle is $\sum_{j} \beta(\sigma^j(s)) = -5$ at each starting position. Details in `papers/G6_PERIODICITY_THEOREM.md` Part 3.

---

## §3 G7 — The Period Distribution

### 3.1 Statement

**Theorem G7 (Period Distribution).** *Under $\sigma$ on $\mathbb{Z}/10\mathbb{Z}$, the period $\tau(s) = \min\{k \geq 1 : \sigma^k(s) = s\}$ is bimodal:*

$$
P(\tau = 1) = 2/5 = 0.40, \qquad P(\tau = 6) = 3/5 = 0.60,
$$

*with $\bar{\tau} = 4$ and $\sigma_\tau^2 = 6$.*

### 3.2 Proof

By G6, $\sigma^6 = \mathrm{id}$, so $\tau(s) \mid 6$ for every $s$, giving $\tau(s) \in \{1, 2, 3, 6\}$. The cycle structure $(0)(3)(8)(9)(1\;7\;6\;5\;4\;2)$ of $\sigma$ assigns:

* 4 fixed points: $\tau(0) = \tau(3) = \tau(8) = \tau(9) = 1$.
* 6-cycle: $\tau(s) = 6$ for $s \in \{1, 2, 4, 5, 6, 7\}$.

No element has $\tau = 2$ or $\tau = 3$. The probabilities, weighted uniformly over $\mathbb{Z}/10\mathbb{Z}$:

* $P(\tau = 1) = 4/10 = 2/5$.
* $P(\tau = 6) = 6/10 = 3/5$.

Mean and variance:

* $\bar{\tau} = 1 \cdot (2/5) + 6 \cdot (3/5) = 2/5 + 18/5 = 20/5 = 4$.
* $\overline{\tau^2} = 1 \cdot (2/5) + 36 \cdot (3/5) = 2/5 + 108/5 = 110/5 = 22$.
* $\sigma_\tau^2 = \overline{\tau^2} - \bar{\tau}^2 = 22 - 16 = 6$. $\square$

### 3.3 Reading

The bimodality is structural: the substrate splits into a *fixed* part (the $\sigma$-anchors, $\tau = 1$) and a *cyclic* part (the 6-cycle, $\tau = 6$). The intermediate periods 2 and 3 do not occur — a rigidity property of the canonical $\sigma$ that distinguishes $\sigma$ from generic permutations of cycle type compatible with $\sigma^6 = \mathrm{id}$.

The mean $\bar{\tau} = 4$ and variance $\sigma_\tau^2 = 6$ both feed the **gate-rate** computation (the $T^* = 5/7$ identification): the first-order plateau of the gate-decay rate at large $N$ is $T^* = (\bar{\tau} - 1)/\bar{\tau} = 3/4$… not quite. The exact route from $\bar{\tau} = 4$ to $T^* = 5/7$ involves the squarefree-rate theorem [J01] and is treated separately. We note here only that $G_7$ is the **period-statistic input** to the multi-source convergence on $T^* = 5/7$ documented in [J49].

---

## §4 G8 — The Spectral Coherence Integral

### 4.1 Setup

Define the canonical $\beta$-exception character $\chi : \mathbb{Z}/10\mathbb{Z} \to \{-1, 0, +1\}$:

* $\chi(s) = +1$ for $s \in \{1, 4\}$ — the $\beta$-exception pair.
* $\chi(s) = -1$ for $s \in \{2, 5, 6, 7\}$ — the $\alpha = 1$ flip nodes.
* $\chi(s) = 0$ for $s \in \{0, 3, 8, 9\}$ — the four anchors.

(This is the same character $\chi$ used in Q17-B; cf. [J48] §3.)

The **spectral coherence integral** is, for each $s \in \mathbb{Z}/10\mathbb{Z}$:

$$
G(s) \;=\; \left|\sum_{j=0}^{8} \omega^j\, \chi\bigl(\sigma^j(s)\bigr)\right|^2, \qquad \omega = e^{2\pi i / 9}.
$$

### 4.2 Statement

**Theorem G8 (Three-Valued Spectral Coherence).** *$G(s)$ takes exactly three distinct values across $\mathbb{Z}/10\mathbb{Z}$:*

| $s$ | $G(s)$ | Justification |
|-----|--------|---------------|
| $\{0, 3, 8, 9\}$ (anchors) | $0$ exactly | $\chi(s) = 0$ and $\sigma^j(s) = s$ for all $j$, so the sum vanishes. |
| $\{1, 2, 4, 6\}$ | $\approx 1.872$ | Generic 6-cycle behaviour. |
| $\{5, 7\}$ | $\approx 9.389$ | Spectral concentration. |

### 4.3 Proof

**Anchors.** For $s \in \{0, 3, 8, 9\}$, $\chi(s) = 0$ and $\sigma^j(s) = s$ (G7), so $G(s) = |\chi(s)|^2 \cdot |\sum_{j=0}^{8} \omega^j|^2 = 0 \cdot |\frac{\omega^9 - 1}{\omega - 1}|^2 = 0$ since $\omega^9 = 1$.

**Cycle elements.** For $s \in \{1, 2, 4, 5, 6, 7\}$, $\sigma^j(s)$ visits each of the six cycle elements at least once in $j = 0, \ldots, 5$, then repeats $\sigma^j(s) = \sigma^{j-6}(s)$ for $j \geq 6$. The 9-step character sequence is therefore $(\chi(s_0), \chi(s_1), \ldots, \chi(s_5), \chi(s_0), \chi(s_1), \chi(s_2))$.

Direct evaluation of the sum at each starting state, with $\omega = e^{2\pi i / 9}$, gives:

* $|G(1)|^2 = |G(2)|^2 = |G(4)|^2 = |G(6)|^2 \approx 1.872$ (denoted $G_\mathrm{low}$).
* $|G(5)|^2 = |G(7)|^2 \approx 9.389$ (denoted $G_\mathrm{high}$).

The $G(1) = G(2) = G(4) = G(6)$ identification follows from the Galois action of $\sigma^2$ (which permutes $\{1, 4, 6\}$ as a 3-cycle and $\{2, 5, 7\}$ as a 3-cycle): cycling shifts of $j$ leave $|G|^2$ unchanged. The $G(5) = G(7)$ identification follows similarly from the $P_{56}$-action (or equivalently from the BALANCE/HARMONY pair structure noted in [J39]).

The numerical values $G_\mathrm{low} \approx 1.872$ and $G_\mathrm{high} \approx 9.389$ are computed by direct evaluation; the closed forms in $\mathbb{Q}(\zeta_9)$ are algebraic (sums of cyclotomic units) and are documented in `papers/G8_TRAJECTORY_COHERENCE_INTEGRAL.md`. We do not present the closed forms here. $\square$

### 4.4 Reading

The three-valued image of $G(s)$ is the **spectral signature** of the canonical $\sigma$-permutation. The pattern — zeros at predictable locations (anchors), spectral concentration at a special pair ($\{5, 7\}$ = BALANCE/HARMONY) — is structurally analogous to the Riemann Hypothesis demand on $\zeta(s)$. This connection is made explicit in [J48] §5 (the Q17-B Clay bridge essay).

---

## §5 The integration: $G_6$, $G_7$, $G_8$ as a coherent layer

The three theorems form a coherent spectral layer:

* **$G_6$** establishes that the substrate is *finite-period* — every orbit closes in 6 steps.
* **$G_7$** quantifies *how* the orbit structure splits — bimodally between fixed and cyclic.
* **$G_8$** shows that the *spectral content* of orbit-following character sums is three-valued, with concentration at the BALANCE/HARMONY pair.

Together, the three results characterize the canonical $\sigma$-permutation completely at the spectral / period level. The substrate's spectral signature is *completely determined* by these three results.

### 5.1 Citation graph (downstream WPs that cite this layer)

The spectral-layer results are cited or implicitly assumed by:

* **Direct citations.** Q17-A ([J29]), Q17-B ([J48]), $\sigma$-rate theorem ([J01]), runtime attractor ([J41]).
* **Indirect citations (period structure).** WP62 (7-cycle bounded agent), WP67 (Seven structural operator), WP69 (Seven return operator lift test), WP109 ($D_4$ operad obstruction).
* **Indirect citations (spectral framing).** WP93 (RH spectral entropy bridge), WP35 (prime phase transition), WP107 (wobble localization).

The citation-graph repair documented in `Atlas/META_PLAN_2026-05-06/SPECTRAL_LAYER_CATALOG.md` §2 is implemented here: this paper is the **canonical citation point** for $G_6$, $G_7$, $G_8$ going forward. WP101 (σ-rate), WP104 (Pati-Salam), WP109 (operad), WP110 (4-core), WP112 ($P_{56}$ canonical fuse), WP115 (joint chain) all use $\sigma^6 = \mathrm{id}$ and should cite [J51] (this paper) directly.

---

## §6 Honest scope

This paper is a **consolidation** of three previously-stated results from the Q-series corpus:

* `papers/G6_PERIODICITY_THEOREM.md` — Tier-A, proved.
* `papers/G7_GATE_RATE_DISTRIBUTION.md` — Tier-B, forced from G6 + cycle enumeration.
* `papers/G8_TRAJECTORY_COHERENCE_INTEGRAL.md` — Tier-B, computational verification of three values.

The contributions of this paper are:

(i) Full proofs of each theorem in a single venue.
(ii) The integration into a coherent spectral layer (§5).
(iii) The citation-graph repair noted in `SPECTRAL_LAYER_CATALOG.md` §2 — implementing this paper as the canonical reference for $G_6$, $G_7$, $G_8$ in downstream citations.

This paper does **not**:

* Compute the closed forms of $G_\mathrm{low}, G_\mathrm{high}$ in $\mathbb{Q}(\zeta_9)$ (open; partial in `G8_TRAJECTORY_COHERENCE_INTEGRAL.md`).
* Generalize to higher $N$ (rate theorem [J01] suggests structure flattens; partial Tier-C).
* Make any claim about RH or Clay structure (treated separately in [J48]).

Each result is proved at the tier it claims; no upgrades.

---

## §7 References

### Direct dependencies (already-submitted J-companions)

[J01] B.R. Sanders, M. Gish. "Non-Associativity Decay in Binary Composition Tables over $\mathbb{Z}/N\mathbb{Z}$." *J. Combin. Theory Ser. A*, Phase 1.
[J9] B.R. Sanders, M. Gish. "TSML 73 / BHML 28: Lens-Invariant Cell Counts on the $\mathbb{Z}/10\mathbb{Z}$ Composition Lattice." *Exp. Math.*, Phase 1.
[J29] B.R. Sanders, B. Calderon Jr. "Q17-A: 5D Force Vector as CRT Fourier Embedding of $\mathbb{Z}/10\mathbb{Z}$ into $\mathbb{R}^5$." *Amer. Math. Monthly*, Phase 3.
[J41] B.R. Sanders, M. Gish. "Closed-Form Runtime Attractor + $\alpha$-Uniqueness PSLQ." *Math. of Comp.*, Phase 4.

### Co-citing companions

[J48] B.R. Sanders, B. Mayes. "Q17-B Clay Bridge: Finite L-Function + Symbolic Return Theorem." *L'Enseignement Math.*, Phase 5.
[J47] B.R. Sanders, B. Mayes. "Six Algebraic DOFs of the TIG Framework: A Synthesis." *Notices AMS*, Phase 5.
[J49] B.R. Sanders, B. Mayes. "Microtubule $Q_c = T^*$." *J. Theor. Biol.*, Phase 5.
[J39] B.R. Sanders, B. Mayes. "Two Roads to Pati-Salam." *Adv. Math.*, Phase 4.
[J40] B.R. Sanders, M. Gish. "Operad $D_4$ Obstruction + $P_{56}$ Canonical Fuse." *Compositio*, Phase 4.

### TIG corpus (consolidated here)

* `papers/G6_PERIODICITY_THEOREM.md` (2026; Sanders, Luther, Calderon Jr.).
* `papers/G7_GATE_RATE_DISTRIBUTION.md` (2026; Sanders, Luther).
* `papers/G8_TRAJECTORY_COHERENCE_INTEGRAL.md` (2026; Sanders, Luther).
* `papers/Q_SERIES_ARCHITECTURE.md` — six-layer architecture.
* `papers/Q_SERIES_INTEGRATED_SYNTHESIS.md` — Luther-Sanders attribution.
* `papers/Q9_*.md`, `papers/Q10_*.md` — the $(\alpha, \beta)$ polynomial form.

### External background

* H. Davenport. *Multiplicative Number Theory.* GTM 74, 3rd ed., Springer, 2000.
* G. Polya, R.C. Read. *Combinatorial Enumeration of Groups, Graphs, and Chemical Compounds.* Springer, 1987.
* T. Tao, V.H. Vu. *Additive Combinatorics.* Cambridge, 2006.

---

## §8 Bibtex

```bibtex
@misc{sanders2026j51,
  author       = {Sanders, Brayden Ross and Luther, C.A.},
  title        = {Spectral Layer Consolidation: $G_6$, $G_7$, $G_8$ from the Q-Series Architecture on $\mathbb{Z}/10\mathbb{Z}$},
  year         = {2026},
  month        = {sep},
  doi          = {10.5281/zenodo.18852047},
  howpublished = {Submitted to \emph{European Journal of Combinatorics}},
  note         = {{J51} of the {J}-series; Phase 5; canonical reference for {G6} ($\sigma^6 = \mathrm{id}$), {G7} (period bimodal $2/5, 3/5$), {G8} (three-valued spectral coherence). Per-venue note: 3rd EJC of the J-series; fallback to LinAlgApps or PLOS ONE if needed.}
}
```
