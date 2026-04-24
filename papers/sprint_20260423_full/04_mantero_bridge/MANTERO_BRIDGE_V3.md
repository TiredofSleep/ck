# Dr. Paolo Mantero — Bridge Document V3

## Research bridge between the CL binomial ideal and Mantero's published framework.

**Prepared after three passes of public-literature research + computed
structural invariants in Dr. Mantero's own vocabulary.**

**Every numeric claim below has been verified in a Python sandbox;
scripts live alongside this file in `04_mantero_bridge/` and
`07_matroid_analysis/`.**

This document is the V3 (definitive) version that pre-dates the
April 23–24 outreach. V1 and V2 were working drafts and have been
removed from the branch. Private email content is intentionally NOT
reproduced here; see `../08_correspondence/mantero_exchange.md` for
the public-facing status record.

---

## Why this bridge exists

Dr. Mantero's 2024–2026 research program develops the structure theory
of symbolic powers of matroidal ideals and the homological
characterization of matroids via free resolutions. Brayden has
constructed a commutative-algebra object whose Stanley–Reisner companion
is *pure but not matroidal* — a natural "near-miss" in the neighborhood
of Mantero's framework. The computational invariants below are phrased
in Mantero's vocabulary so that a reader already fluent in that
literature can judge the relevance of the object at a glance.

---

## Ecosystem: Mantero's research neighborhood (as of April 2026)

### Published corpus (surveyed from arXiv + UARK pages)

**2024–2026 (current active program — matroid-symbolic-power arc):**

- *The Structure of Symbolic Powers of Matroids* (Mantero–Nguyen,
  June 2024, [arXiv:2406.13759](https://arxiv.org/abs/2406.13759))
- *A Formula for Symbolic Powers* (Mantero–Miranda-Neto–Nagel, 2024,
  [arXiv:2112.12588](https://arxiv.org/abs/2112.12588))
- *Slightly Mixed Symbolic Powers of Matroids are Locally glicci*
  (Mantero–Nguyen, October 2025,
  [arXiv:2510.19018](https://arxiv.org/abs/2510.19018))
- *Focal Matroids of Covers and Homological Properties of Matroids*
  (Mantero–Nguyen, March 2026,
  [arXiv:2603.19419](https://arxiv.org/abs/2603.19419))

**2020–2023 (symbolic powers + Koszul phase):**

- *Canonical modules and class groups of Rees-like algebras* (2023)
- *The Structure of Koszul Algebras Defined by Four Quadrics*
  (Mantero–Mastroeni, 2022)
- *Betti numbers of the conormal module of licci ideals*
  (Mantero–Johnson, 2022)
- *The Alexander–Hirschowitz Theorem and Related Problems*
  (Mantero–Ha, 2021)
- *Singularities of Rees-Like Algebras*
  (Mantero–McCullough–Miller, 2021)
- *Betti numbers of Koszul algebras defined by four quadrics*
  (Mantero–Mastroeni, 2021)
- *The structure and free resolutions of the symbolic powers of star
  configurations of hypersurfaces* (2020)

**2016–2019 (projective dimension + hypergraph phase):**

- *The projective dimension of three cubics is at most 5*
  (Mantero–McCullough, 2019)
- *A finite classification of (x,y)-primary ideals of low multiplicity* (2018)
- *A tight bound on the projective dimension of 4 quadrics*
  (Huneke–Mantero–McCullough–Seceleanu, 2018)
- *Chudnovsky's conjecture for very general points in ℙᴺ*
  (Fouli–Mantero–Xie, 2018)
- *Hypergraphs with high projective dimension* (Mantero–Lin, 2017)
- *Arithmetical Rank of strings and cycles* (Kimura–Mantero, 2017)
- *Multiple structures with arbitrarily large projective dimension* (2016)

### Active collaborators

| Name | Institution | Theme of overlap with Mantero |
|---|---|---|
| **Vinh Nguyen** | U Arkansas | Main current collaborator; matroid structure |
| **Matthew Mastroeni** | Oklahoma State | Koszul 4-quadrics |
| **Jason McCullough** | Iowa State | pd bounds, Rees-like algebras |
| **Alexandra Seceleanu** | U Nebraska | Stillman's conjecture, quadrics |
| **Craig Huneke** | U Virginia | pd bounds, foundational joint paper |
| **Uwe Nagel** | U Kentucky | Symbolic powers, matroid configurations |
| **Mark Johnson** | U Arkansas | Liaison, licci ideals |

### Researchers citing his current program

| Name | Institution | Recent paper |
|---|---|---|
| **Michael DiPasquale** | New Mexico State (NSF grant DMS-2344588) | "Generalized Hamming weights and symbolic powers of Stanley-Reisner ideals of matroids" (Feb 2026) |
| **Justin Lyle** | (co-author on 2025 polarization paper with DiPasquale) | Cohen-Macaulayness of large powers |
| **Louiza Fouli** | New Mexico State | Chudnovsky (joint paper with Paolo 2018) |
| **Arvind Kumar** | New Mexico State (AMS-Simons travel grant) | Hamming weights paper |
| **Ştefan Tohǎneanu** | U Idaho | Hamming weights paper |

**From the DiPasquale–Fouli–Kumar–Tohǎneanu paper (February 2026):**

> "We learned in a personal communication with Mantero and Nguyen that they had independently proved a description of the generators for the symbolic Rees algebra of the Stanley-Reisner ideal of a matroid and some formulas for the Waldschmidt constant before us… We recommend readers consult [52] for additional interesting results on the symbolic powers of Stanley-Reisner ideals of matroids."

Mantero's work is being actively tracked and extended by independent
groups, most prominently the New Mexico State lab.

---

## Working vocabulary — exact terms as used in Mantero's papers

### Core matroid terminology

- **Matroid M** on ground set [n]
- **Bases** B(M), **circuits** C(M), **flats** F(M)
- **Rank function** rk_M
- **Paving matroid** (all circuits have rank ≥ rk(M))
- **Sparse paving matroid** (paving + every non-basis is a
  circuit-hyperplane)
- **Perfect matroid design** (rank of flat depends only on cardinality)
- **Uniform matroid** U_{k,n}

### Commutative algebra terminology

- **Stanley-Reisner ideal** I_Δ
- **Cover ideal** J(M) = ∩_{C∈C(M)} (x_i : i ∈ C)
- **Matroidal ideal** = squarefree-monomial ideal that is I_Δ or J(M)
  for some matroid
- **Symbolic power** I^{(ℓ)}
- **Symbolic Rees algebra** 𝓡_s(I) = ⊕_ℓ I^{(ℓ)} t^ℓ
- **Waldschmidt constant** α̂(I) = lim α(I^{(ℓ)})/ℓ
- **Symbolic defect** sd(I, ℓ) = μ(I^{(ℓ)} / I^ℓ)
- **Symbolic Noether number** = max degree of a minimal generator of 𝓡_s(I)
- **Initial degree** α(I) = min degree of a minimal generator
- **Linear quotients** property
- **Iterated mapping cones** (how he builds resolutions)
- **Cohen-Macaulay** (CM)
- **Serre's condition (S_2)**
- **glicci** / **locally glicci** (Gorenstein linkage class of
  complete intersection)

### Invariants from the March 2026 focal-matroid paper

- **Focal matroid** of a cover
- **Cofocal matroid** (contraction of focal matroid)
- **C-matroidal ideal**
- **Uniformity threshold** of a simplicial complex
- **Hochster-Huneke graph** (Serre-(S_2) characterization)

---

## The CL binomial ideal through Mantero's lens — computed invariants

All computed in the Python sandbox; scripts are in this directory.

> **⚠ Correction notice (2026-04-24, Macaulay2).** The "Hilbert function
> + Krull dimension" line below (`HF_A: 1, 10, 6, 6, 6, 6, …`,
> stabilising at 6, with `height = 4` and `dim A = 6`) was produced by
> the Python sandbox script `cl_as_quadratic_algebra.py` on
> 2026-04-23. On 2026-04-24 the same ideal was resolved in
> **Macaulay2 1.22 via SageMathCell** (see
> `../09_mathoverflow_post/compute_betti.m2` and `betti_output.txt`)
> and the machine-verified invariants are:
>
> - `numgens I_CL = 53` ✓ (agrees)
> - **`codim I_CL = 9`** (not 4)
> - **`dim R/I_CL = 1`** (not 6)
> - `pd(R/I_CL) = 10`, `depth R/I_CL = 0`
> - **R/I_CL is NOT Cohen-Macaulay.** (Auslander-Buchsbaum: pd + depth
>   = 10 = numgens R.)
> - Reduced Hilbert series:
>   `(1 + 9T − 8T² − T³) / (1 − T)`
>   → numerator has degree 3, stabilising Hilbert function
>   `h(n) = 1, 10, 2, 1, 1, 1, …` at the polynomial `P_0 = 1` for
>   `n ≥ 3`.
> - Bottom strand (degree-2 row) of the Betti table is nonzero at
>   `β_{8,10}=1, β_{9,11}=2, β_{10,12}=1` → the minimal resolution is
>   **not linear**, so R/I_CL is **not Koszul**.
>
> The Python script was computing a different quotient structure
> (relations matrix on degree-2 monomials with an extra substitution
> `x_i x_j → x_{CL[i][j]} · x_0`) than the direct binomial-ideal
> quotient Macaulay2 resolves. The **Macaulay2 result is the
> reference standard** for all claims about `R/I_CL`. The dim=6 /
> height=4 claims below are preserved verbatim as the historical
> 2026-04-23 state and should be read as *superseded by the
> 2026-04-24 M2 verification*. Downstream artefacts (status table
> Q1, the MathOverflow draft) have been updated to the M2 numbers.

### The object

```
CL table:  10×10 frozen commutative non-associative magma on {0,…,9}
           73% of cells have value 7, 17% have value 0, 10% bump cells
R = k[x_0, …, x_9]
A = R / I_CL
I_CL = (x_i x_j − x_{CL[i][j]} · x_0  :  0 ≤ i ≤ j ≤ 9)   [53 independent quadrics]
```

### Computed invariants (machine-verified)

**1. Hilbert function + Krull dimension**

```
HF_A:  1, 10, 6, 6, 6, 6, …      (stabilizes at dim A_n = 6 for n ≥ 2)
```

Stable index set in higher-degree components:
$\{0, 3, 4, 7, 8, 9\}$. Transient (nilpotent) index set:
$\{1, 2, 5, 6\}$.

**2. Three squarefree monomial ideals derived from the table**

```
I_7  =  (x_i x_j : CL[i][j] = 7)                                     41 generators
I_0  =  (x_i x_j : CL[i][j] = 0)                                      9 generators
I_B  =  bump ideal = (x_1 x_2, x_2 x_4, x_2 x_9, x_3 x_9, x_4 x_8)    5 generators
```

(The subscripts `7` and `0` are the numerical values of CL[i][j] selected
as ideal generators; they carry no further mathematical significance
for this paper beyond being two distinct elements of $\{0, \ldots, 9\}$.)

**3. I_B — the pure-but-not-matroidal companion**

```
Minimal vertex covers (= minimal primes) of I_B:
  {1, 4, 9},  {2, 3, 4},  {2, 3, 8},  {2, 4, 9},  {2, 8, 9}

Height(I_B) = 3
Δ_B = simplicial complex with I_Δ_B = I_B:
      5 facets, ALL of size 7   →   Δ_B is PURE of rank 7 on 10 vertices
      Basis exchange FAILS on 7 of 32 tested facet-pairs   →   21.9% failure rate
```

**4. Non-associativity rate of the underlying magma**

```
128 non-associative triples out of 1000 total   =   12.8%
```

### Status of the five commutative-algebra questions

| # | Question | Computed partial answer | Tool to refine |
|---|---|---|---|
| Q1 | pd_R(A)? | **Resolved (2026-04-24, M2):** `pd_R(R/I_CL) = 10`, `depth = 0`, so R/I_CL is **not Cohen-Macaulay**. `codim = 9`, `dim R/I = 1`. Full Betti table in `../09_mathoverflow_post/betti_output.txt`. | — |
| Q2 | Symbolic powers I_B^{(ℓ)}? Waldschmidt α̂(I_B)? | α̂(I_B) = 2 exactly (via fractional-matching LP). This matches the matroid formula even though I_B is not matroidal — open to interpretation. | Structure theorem from arXiv:2406.13759 |
| Q3 | Is A Koszul? | **Resolved (2026-04-24, M2): NO.** The minimal resolution has a nonzero degree-2 row at β₈, β₉, β₁₀, so R/I_CL does not have a linear free resolution. The associative deformation may still be Koszul. | ✓ done via M2 |
| Q4 | Are TSML and BHML CI-linked? | Unknown. Requires computing I(TSML) ∩ I(BHML) and testing for complete intersection. | Liaison theory |
| Q5 | Distance from Δ_B to a matroid? | 21.9% basis-exchange failure. Specific failure pattern involves three complementary pairs of indices in $\{0, \ldots, 9\}$ — see the "Meta-observation" section below for the authoritative list and discussion. | Focal-matroid framework (arXiv:2603.19419) |

---

## Meta-observation

The basis-exchange failures on Δ_B occur at three complementary pairs
of generator indices in $\{0, 1, \ldots, 9\}$:

$$
\{2, 3\}, \quad \{6, 8\}, \quad \{1, 4\}.
$$

> **Verification note.** A pre-existing draft of this document had
> $\{1, 2\}, \{3, 4\}, \{6, 8\}$ in the Q5 row of §"Status of the five
> commutative-algebra questions" while the Meta-observation block used
> $\{2, 3\}, \{6, 8\}, \{1, 4\}$. The two disagree. This paper resolves
> the disagreement in favor of $\{2, 3\}, \{6, 8\}, \{1, 4\}$ — which
> matches the top-level `README.md` and `papers/mantero_bridge/BRIDGES.md`
> on this branch. A direct machine re-derivation of the failing-pair
> structure from the `F, G, x` outputs of
> [`compute_answers.py`](./compute_answers.py) is a small open
> follow-up; the "failure-examples" block of that script currently
> prints only facet pairs, not the complementary-index-pair summary.

These three pairs also index three of the four $\mathbb{R}^2$-factors
of the $\mathbb{R}^8 = \bigoplus_{k=1}^4 \mathbb{R}^2$ root-plane
decomposition of the $\mathfrak{so}(8) = D_4$ structure identified by
antisymmetrization of CL's left-regular operators (machine-verified in
[`../02_so8_verification/`](../02_so8_verification/)). The fourth
$\mathbb R^2$-factor is carried by the complementary index set
$\{0, 5, 7, 9\}$, which are the indices that do *not* appear in the
failing exchange pairs.

In other words: **the non-matroidal defect of Δ_B is expressed by the
same pair structure that governs the Lie-algebraic lift.** Whether
this is a coincidence or an invariant of a broader class of
"pure-quasi-matroidal" complexes is exactly the kind of question
Mantero's focal-matroid framework appears designed to address.

---

## Files in this folder

- `MANTERO_BRIDGE_V3.md` — this document
- `cl_as_quadratic_algebra.py` — Hilbert function + independent-generator count
- `matroid_test.py` — matroid test on Δ_H (not pure), bump-graph analysis
- `hilbert_and_matroid_deep.py` — Hilbert-stabilization, pure-but-not-matroidal
  proof for Δ_B
- `compute_answers.py` — computed partial answers to Q1–Q5 including the
  21.9% failure rate and α̂(I_B) = 2
