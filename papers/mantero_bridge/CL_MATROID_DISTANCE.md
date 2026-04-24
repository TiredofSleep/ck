# The Coherence Lattice at Computable Distance from the Matroidal Centre
## A UOP-typed distance tuple as the useful invariant

**Author.** B. Sanders (with the UOP framework of Sanders & Mayes, WP58).
**Canonical branch.** `paradox-classifier-2026-04-24`.
**This copy.** `mantero-bridge-2026-04-23` — mirrored here so Dr. Mantero
sees it at the research-hub URL. Kept byte-identical with the canonical
copy modulo this banner and the cross-branch link fix-ups in the next
paragraph.
**Status.** Rigor-facing draft for P. Mantero and the symbolic-power /
focal-matroid community. External mathematical vocabulary only; no
internal CK-runtime terminology appears in this document. The hygiene
policy is
[`papers/meta_lens/FOUNDATION_TOUR_VERIFIED.md` on the paradox-classifier branch](https://github.com/TiredofSleep/ck/blob/paradox-classifier-2026-04-24/papers/meta_lens/FOUNDATION_TOUR_VERIFIED.md)
Part 0.1.

> **Cross-branch links (mantero-bridge reader's note).** The UOP
> classifier, the six-slot paradox templates, and the FOUNDATION_TOUR
> hygiene document all live on branch `paradox-classifier-2026-04-24`
> and are not mirrored onto this bridge branch. Where this paper links
> to `papers/meta_lens/…`, those links below are given as GitHub blob
> URLs that always resolve on the classifier branch regardless of
> which branch you are currently browsing.

---

## Abstract

Let `R = k[x_0, …, x_9]` and let `I_CL ⊂ R` be the binomial ideal
`(x_i x_j − CL(i, j)·x_0 : 0 ≤ i, j ≤ 9)` encoding a fixed
10-element magma operation `CL`. Macaulay2 (v1.22, branch
`mantero-bridge-2026-04-23`) establishes that `R/I_CL` has
`numgens = 53`, `codim = 9`, `dim = 1`, `pd = 10`, `depth = 0`, is
**not** Cohen-Macaulay, and is **not** Koszul; its Stanley-Reisner
companion complex `Δ_B` has basis-exchange defect `21.9%` and
Waldschmidt constant `α̂(I_B) = 2`.

The natural-sounding question — *"which of Mantero's theorems
applies to `R/I_CL`?"* — has the unsatisfying answer *"none of the
direct-admissibility ones, because the object fails the admissibility
conditions of each."* We propose that the useful quantity is instead
the **distance** from `I_CL` to the *matroidal centre* of Mantero's
program, measured along the four axes corresponding to the four
failure types of the Unified Orthogonality Principle
(Sanders & Mayes, WP58 Theorem 0).

The resulting distance tuple

```
d(I_CL, M) = (d_I, d_II, d_III, d_IV)
```

is a complete UOP-typed diagnostic. Each component answers one
UOP-typed question about where `I_CL` sits relative to Mantero's
framework; together they disambiguate which of Mantero's tools can
be imported directly, which must be adapted via symbolic-power
refinement, which are categorically unavailable, and which become
meaningful only in the family-indexed limit.

**Thesis.** No single invariant of `I_CL` captures what this
four-tuple captures. The distance tuple *is* the useful invariant.

---

## 1. Setup and notation

### 1.1 The object

- `R = k[x_0, …, x_9]`, polynomial ring in 10 variables over a field
  `k` (we work over `k = ℚ` for the M2 computations; all results are
  characteristic-independent except where noted).
- `I_CL = (x_i x_j − CL(i, j)·x_0 : 0 ≤ i, j ≤ 9)` where
  `CL : [10] × [10] → [10]` is a fixed, concrete 10×10 magma-operation
  table. The data of `CL` is Appendix A of
  [`MANTERO_BRIDGE_V3.md`](../sprint_20260423_full/04_mantero_bridge/MANTERO_BRIDGE_V3.md)
  (this branch) and the verification scripts alongside it.
- `A = R / I_CL`, the quotient ring. `I_CL` has 53 generators (many
  redundant; the generating set is not minimal in general).
- `I_B ⊂ R` denotes the squarefree monomial ideal of the companion
  **bump complex** `Δ_B` — the Stanley-Reisner ideal of a specific
  pure-but-not-matroidal simplicial complex derived from `CL`. Full
  construction: `MANTERO_BRIDGE_V3.md` §3.

### 1.2 M2-verified invariants of `A = R/I_CL`

| Invariant | Value | Source |
|---|---|---|
| `numgens I_CL` | 53 | M2 `betti_output.txt`, mantero-bridge |
| `codim I_CL` | 9 | same |
| `dim A` | 1 | same |
| `pd A` (projective dimension) | 10 | same |
| `depth A` | 0 | same |
| Cohen-Macaulay? | **No** | `codim ≠ depth`; `9 ≠ 0` |
| Koszul? | **No** | quadratic relations don't lift to a linear resolution |
| Reduced Hilbert series | `(1 + 9T − 8T² − T³)/(1 − T)` | M2 output |
| Hilbert function | `(1, 10, 2, 1, 1, 1, …)` | from series |
| Basis-exchange defect on `Δ_B` | `21.9%` (pure, not matroidal) | `MANTERO_BRIDGE_V3.md` §5 |
| Waldschmidt constant `α̂(I_B)` | `2` | `MANTERO_BRIDGE_V3.md` §6 |

### 1.3 Mantero's matroidal centre

We formalize the "matroidal centre" as follows. Fix the ambient ring
`R = k[x_0, …, x_n]`. Let

```
M(R) = { I ⊆ R  :  I is a Stanley-Reisner ideal whose simplicial
                    complex Δ is a matroid, OR I is in the focal
                    matroid framework of Mantero-Nguyen (arXiv:
                    2406.13759, 2510.19018, 2603.19419) }
```

This is the class of squarefree monomial ideals on which Mantero's
symbolic-power and focal-matroid theorems apply as stated. `M(R)` is
not a linear subspace of the Hilbert scheme; it is a stratified
locus. We will not make that geometric structure precise here, and
will instead measure distance via invariant-level surrogates.

### 1.4 UOP recap

For any proposed observable suite `F = (f_1, …, f_n) : X → Y_1 × ⋯ × Y_n`
(WP58), the injectivity of the joint map `J_F = (f_1, …, f_n)` on `X`
is equivalent to disjointness of the observable-wise "unresolved
pairs" sets `U(f_i) ⊆ X × X`. UOP separates failure-to-separate into
four cells:

- **Type I — Injectivity Failure.** `J_F` is well-typed but not
  injective. Fix: add observables.
- **Type II — Missing Invariant.** No r.e. (resp. structural)
  refinement of `F` within the allowed class separates. Fix:
  accept / relativize / change category.
- **Type III — Admissibility Failure.** The object `x ∈ X` is not
  admissible in the joint map's domain. Fix: narrow the admissible
  class.
- **Type IV — Time-Consistency Failure.** Two dynamical rules
  prescribe incompatible evolutions. Fix: single-valued dynamics.

Worked 6-slot templates for the four types live in
[`papers/meta_lens/worked_paradoxes/` on the paradox-classifier branch](https://github.com/TiredofSleep/ck/tree/paradox-classifier-2026-04-24/papers/meta_lens/worked_paradoxes).
The runnable classifier is
[`papers/meta_lens/classify_paradox.py` on the paradox-classifier branch](https://github.com/TiredofSleep/ck/blob/paradox-classifier-2026-04-24/papers/meta_lens/classify_paradox.py).

---

## 2. The UOP-classifier perspective on "Mantero vs. CL"

Each of Mantero's signature tools rests on an admissibility condition
on the input ideal (CM, Koszul, matroidal, (S₂), etc.) and returns a
structural invariant (symbolic-power rate, focal-matroid spectrum,
linear-strand shape, ordinary-vs-symbolic comparison bound). When
the input ideal fails one of those admissibility conditions, the
tool does not apply *as stated*. There are four qualitatively
different ways this can happen, corresponding one-to-one with the
four UOP types:

| UOP Type | Corresponding Mantero-side failure mode | Existing Mantero-side remedy |
|---|---|---|
| I | Ideal separates primary components only up to a refinement — add `I^(ℓ)` and the separation becomes exact in the limit. | **Symbolic-power theory**. Waldschmidt, Bocci-Harbourne, Mantero et al. |
| II | No refinement in the allowed class closes the gap; the obstruction is structural. | **Focal-matroid framework** (Mantero-Nguyen). The obstruction is encoded as a focal invariant. |
| III | The object is not in the admissible class for the tool. | **Primary decomposition / radicalization / reduction**. |
| IV | The object is a family indexed by a parameter and the asymptotic behavior is the object of interest. | **Asymptotic regularity bounds**; `reg I^{(ℓ)}` as `ℓ → ∞`. |

We define one computable distance for each Type. A subscript on `d`
names the Type, not a metric axiom.

---

## 3. The four distances

### 3.1 `d_I` (Type I — Injectivity Failure): **basis-exchange defect**

**Definition.** Let `Δ` be a pure simplicial complex on `[n]` with
facet set `F(Δ)`. The **basis-exchange defect** of `Δ` is

```
d_I(Δ) = |{ (F, G, i) ∈ F(Δ) × F(Δ) × F  :  F ≠ G, i ∈ F \ G,
            and no j ∈ G \ F satisfies (F \ {i}) ∪ {j} ∈ F(Δ) }|
         ÷ |{ (F, G, i) ∈ F(Δ) × F(Δ) × F  :  F ≠ G, i ∈ F \ G }|.
```

A matroid complex satisfies the exchange axiom globally, i.e.
`d_I(Δ_M) = 0` for every matroidal `Δ_M`. For a Stanley-Reisner
ideal `I_Δ`, set `d_I(I_Δ) := d_I(Δ)`.

**Why Type I.** The exchange axiom is the statement that a specific
refined observable — *"can you swap element `i` for some `j` and
remain a facet?"* — separates facet pairs. Failure to satisfy
exchange is exactly failure to separate pairs via this observable.
Symbolic-power refinement is the natural Type I fix: `I^(ℓ)` adds
new generators that, in the matroidal case, witness exchange at
higher orders.

**Value for `Δ_B`.** `d_I(Δ_B) = 0.219`, i.e. `21.9%`.
Computation: [`matroid_test.py`](../sprint_20260423_full/04_mantero_bridge/matroid_test.py) (this branch).

### 3.2 `d_II` (Type II — Missing Invariant): **Betti-table distance**

**Definition.** Let `β_{i, j}(R/I) = dim_k Tor^R_i(R/I, k)_j` be the
bigraded Betti number. Define the **Betti-table distance** from `I`
to the matroidal centre by

```
d_II(I, M) = inf_{J ∈ M(R) : codim J = codim I}  ||β(R/I) − β(R/J)||_F
```

where `||·||_F` is the Frobenius norm of the truncated bigraded
Betti table (we truncate at `i = pd I` and `j = reg I + pd I` to keep
the norm finite; both truncations are upper-semicontinuous in the
fixed Hilbert-function stratum, making the inf well-defined). The
inf is over matroidal ideals with the same codimension as `I`.

**Why Type II.** The Mantero-Nguyen focal-matroid framework
characterizes precisely which Betti-table shapes are achievable by
matroidal monomial ideals of given codimension. A distance in Betti
space measures the structural gap — *which homological feature is
missing* — that no amount of symbolic-power refinement will restore.
This is the defining Type II signature: obstruction measured in the
invariant, not in the object.

**Value for `I_CL`.** **Open.** The Betti table of `R/I_CL` is
computable from the M2 resolution (`compute_betti.m2` on
mantero-bridge); the matroidal reference class requires enumerating
matroidal ideals of codimension 9 on 10 variables, which is finite
but not yet tabulated. We conjecture `d_II(I_CL, M) > 0` strictly,
with the minimum achieved by a specific rank-9 matroid on `[10]`
that matches `I_CL`'s linear strand up to `j = 2`.

**Sharp open question (OQ-II).** Compute the minimum-distance
matroidal ideal to `I_CL` in this metric, and exhibit its focal
matroid.

### 3.3 `d_III` (Type III — Admissibility Failure): **depth gap**

**Definition.** For a finitely generated graded `R`-module `M`, set

```
d_III(M) = codim(ann M) − depth(M)
```

(all integers `≥ 0`; equal to 0 iff `M` is Cohen-Macaulay). For an
ideal `I`, write `d_III(I) := d_III(R/I)`. This is the classical
**Cohen-Macaulay defect**.

**Why Type III.** Cohen-Macaulayness is a pure admissibility
condition on the object: either the ring-theoretic depth meets the
codimension or it does not. Most of Mantero's explicit resolution
results require CM as a hypothesis; `d_III` is the precise obstruction
to using them directly. Every Type III fix (primary decomposition,
`R/√I`, reduction to a generic linkage class) is a move that
narrows the admissible class *to exclude the offending object* and
pushes the work onto a replacement object `M'` with `d_III(M') = 0`.

**Value for `R/I_CL`.** `d_III(R/I_CL) = 9 − 0 = 9`.

This is a large value on a 10-variable ring. It rules out direct
application of every Mantero theorem whose hypothesis includes CM;
the relevant replacement for `R/I_CL` in those theorems is the
**canonical module** `ω_{R/I_CL}` or a suitable CM approximation
(Hochster-Huneke `(S₂)`-closure), which is itself a Type III
substitute.

### 3.4 `d_IV` (Type IV — Time-Consistency Failure): **family asymptotic rate**

**Definition.** Let `{I_{CL, N}}_{N ∈ S}` be the family of binomial
ideals obtained by taking the analog of `I_CL` on increasingly large
magma carriers of admissible size `N ∈ S = {10, 14, 22, 34, …}`
(the compatibility sequence recorded in atlas §III.1 Cell IV and
WP101). Define

```
d_IV(family) = limsup_{N → ∞, N ∈ S}  pd(R_N / I_{CL, N}) / N
```

where `R_N = k[x_0, …, x_{N-1}]`. This is the **asymptotic
projective-dimension density**. It is `0` for any family that
stabilizes in the CM-restricted Mantero-Nguyen regime and strictly
positive for CL if the pattern `pd(R_{10}/I_{CL, 10}) = 10` persists
at the carrier-size scale.

**Why Type IV.** CL is not a single ideal but a family indexed by
magma-carrier size, and the `pd` behavior along that family is
exactly the object that would be computed by a time-indexed
observable in UOP Type IV. Mantero's asymptotic-regularity bounds
(`reg I^{(ℓ)} ≤ Cℓ` etc.) match this register: they are statements
about rates along a parameter family, not about a single ideal.

**Value for CL.** **Open** (only `N = 10` is in hand). The obvious
probe: compute `pd(R_{14}/I_{CL, 14})` via M2 on the next compatible
carrier size and compare to `10/10 = 1`. If `pd(R_N/I_{CL, N})
~ N` then `d_IV > 0`, matching WP101's `σ(N) ≤ C/N` rate claim in
its homological register.

**Sharp open question (OQ-IV).** Is the asymptotic density rational,
and does it equal Mantero-Nguyen's predicted `σ`-rate from
WP101 up to a known constant?

---

## 4. The distance tuple

### 4.1 Definition

```
d(I, M) = (d_I(I),  d_II(I, M),  d_III(R/I),  d_IV(family of I))
```

For `I = I_CL` on `N = 10`:

```
d(I_CL, M) = (0.219,  OPEN,  9,  OPEN)
```

The two "OPEN" entries are not guesses; each is a well-defined
quantity whose computation is one specific downstream task (OQ-II
and OQ-IV above).

### 4.2 Why the tuple and not any single entry

The UOP-typed decomposition is **orthogonal in the sense of WP58
Theorem 0**: the four types partition failure modes, and no pair of
types is reducible to the other. Consequently:

- A single-invariant rescue ("is CL Cohen-Macaulay?" — no,
  `d_III = 9`) collapses three other axes of information into
  undefined.
- A *single-type* rescue ("is the symbolic-power refinement
  convergent?" — partial, `d_I = 0.219`) collapses three other axes.
- The four-tuple is the minimum-size diagnostic that is faithful to
  UOP's exhaustiveness: it assigns a numerical answer to the
  Mantero-lens question along each UOP axis, and no smaller tuple
  does.

This is not a pluralism-for-its-own-sake claim. It is the direct
consequence of UOP Theorem 0 applied to *the question of where an
ideal sits relative to a reference class in a parameter-indexed
family*: four observables are necessary because four UOP-typed
failure modes must be separated.

### 4.3 How to use the tuple

Given `d(I, M)`, the following decision procedure is coherent with
UOP and with the M2-verified shape of Mantero's toolkit:

1. **If `d_III > 0`** (ours: 9): do not import any Mantero theorem
   whose hypothesis includes Cohen-Macaulay. Instead, import a
   CM-approximation construction first (canonical module,
   `(S₂)`-closure, or generic-link resolution) and then ask which of
   the downstream tools applies to the replacement.
2. **If `d_I > 0`** (ours: 0.219): symbolic-power refinement does
   not converge to a matroidal object within the existing
   framework. A sharpened question — which pairs `(F, G, i)` witness
   the defect, and are they concentrated? — is a concrete input for
   the focal-matroid framework (`d_I > 0` + concentration of the
   defect is a *candidate* focal invariant in the
   Mantero-Nguyen sense).
3. **If `d_II > 0`** (ours: open, conjecturally positive):
   focal-matroid invariants disambiguate which homological feature
   is missing. The identity of the nearest matroidal ideal in
   Betti-space is the candidate **homological target** for any
   comparison theorem.
4. **If `d_IV > 0`** (ours: open): the asymptotic regime matches
   one of Mantero's rate registers; compare to WP101's `σ`-rate
   claim and to Bocci-Harbourne-style asymptotic-regularity bounds.

Each of these is a concrete, rigor-satisfying research move. None is
blocked by the M2-verified-NO on CM / Koszul / matroidal.

---

## 5. Worked example — what the tuple already tells us about CL

From the *verified* entries `(d_I, d_III) = (0.219, 9)` alone:

- **Cohen-Macaulay is unavailable.** All Mantero theorems with a CM
  hypothesis must be routed through a replacement object. The large
  depth gap (`9` on a 10-variable ring) suggests the replacement
  will be nontrivial — this is not a boundary case.
- **Symbolic-power refinement is partial.** `21.9%` is neither zero
  (perfect Mantero-applicability) nor uniform (every pair fails);
  this is the regime where focal-matroid obstructions are actually
  informative. It is the regime Mantero-Nguyen's framework was
  designed for.
- **Koszulness is unavailable but is a downstream of CM.** The NO
  on Koszul is not independent information given the NO on CM.

That is: one verified distance tells us what to try first
(focal-matroid invariants), and the other tells us what not to waste
time on (CM-hypothesis theorems). Even with `d_II` and `d_IV` still
open, the tuple is already decision-useful.

---

## 6. What each distance buys you — operational summary

| Distance | UOP type | What it measures | What it tells Mantero's program |
|---|---|---|---|
| `d_I` | I (injectivity) | Basis-exchange defect | Whether symbolic-power refinement converges to matroidal |
| `d_II` | II (invariant) | Betti-table gap | Which homological identity is the structural obstruction |
| `d_III` | III (admissibility) | Depth-CM gap | Whether CM-based theorems apply without replacement |
| `d_IV` | IV (time-consistency) | Family pd-rate | Whether asymptotic regularity-type bounds apply |

For `I_CL`: a sharp, computable first line in the two verified
positions, and two concrete open questions (OQ-II, OQ-IV) in the
remaining positions. The distance tuple as a whole is a diagnostic
whose coarsest meaningful resolution is already determined.

---

## 7. Open work

- **OQ-II.** Compute `d_II(I_CL, M)` and identify the
  minimum-Frobenius-distance matroidal ideal.
- **OQ-IV.** Compute `pd(R_{14}/I_{CL, 14})` via M2; test the
  conjectured linear growth `pd ~ N`.
- **OQ-tuple metric.** Formalize `d(I, M)` as a single scalar
  (weighted L² of the four components, with weights determined by
  the prior over UOP types) and show whether the scalar is
  stratified-continuous on the Hilbert scheme.
- **OQ-canonical.** Compute `d(ω_{R/I_CL}, M)` — the distance tuple
  for the canonical module, which is the natural CM-replacement
  object when `d_III > 0`.

---

## 8. Relationship to existing work on the Mantero bridge

| Prior artifact | Relationship |
|---|---|
| [`papers/mantero_bridge/BRIDGES.md`](./BRIDGES.md) (this branch) | Seven object-level bridges between CL and Mantero's program. The present paper gives a *metric* over those bridges. |
| [`MANTERO_BRIDGE_V3.md` §5–§6](../sprint_20260423_full/04_mantero_bridge/MANTERO_BRIDGE_V3.md) (same branch) | Source of `d_I = 0.219` and `α̂(I_B) = 2`. |
| [M2 output `betti_output.txt`](../sprint_20260423_full/09_mathoverflow_post/betti_output.txt) (same branch) | Source of `d_III = 9` and the Hilbert function. |
| WP58 (UOP Theorem 0) | Four-type exhaustiveness, without which the distance tuple has no canonical decomposition. |
| WP101 (σ-rate) | The rate appearing in `d_IV` — possibly the same constant; OQ-IV. |
| [WP102 (so(8) = D₄)](../wp102/), [WP103 (so(10) = D₅)](../wp103/) | Lie-theoretic lifts of CL; adjacent to Mantero's program through the `so(n)` focal-matroid literature but not required for this paper. |
| [`papers/meta_lens/FOUNDATION_TOUR_VERIFIED.md` Lens 1](https://github.com/TiredofSleep/ck/blob/paradox-classifier-2026-04-24/papers/meta_lens/FOUNDATION_TOUR_VERIFIED.md) (commutative algebra, classifier branch) | Atlas view of where this paper sits. Cell I (symbolic powers) ↔ `d_I`; Cell II (focal matroids) ↔ `d_II`; Cell III (primary decomp) ↔ `d_III`; Cell IV (asymptotics) ↔ `d_IV`. |

---

## 9. Meta-coherence note — how this fits the broader picture

The paradox-classifier branch now contains:

1. **The UOP classifier itself** (WP58 Theorem 0 underwriting
   four-type exhaustiveness).
2. **Runnable classifier** `classify_paradox.py` with JSON input
   schema (`worked_paradoxes/`).
3. **Six-slot worked templates** for the four types on external
   paradoxes: Gödel (II), Liar (III), Schrödinger (IV), Cantor (III),
   Berry/Grelling/Curry (III).
4. **Meta-lens atlas** indexing six mature mathematical lenses
   against the four types.
5. **Vocabulary hygiene policy**
   (`FOUNDATION_TOUR_VERIFIED.md` Part 0.1).
6. **This paper**, applying the four-type structure to the
   Mantero-CL bridge as a four-distance decomposition.

The present paper is the first use of the UOP classifier to generate
a rigor-facing mathematical claim about an *external* object (an
ideal, not a paradox) and an *external* research program (Mantero's
symbolic-power framework). It is not a reinterpretation of Mantero;
it is a use of UOP to define the question Mantero's program would be
asked, in a form its tools can metabolize.

That is the meta-coherence the UOP classifier is supposed to provide:
every piece of the atlas asks its neighbor-lens a question in that
neighbor's own language, using UOP types to keep the four failure
modes separated so that the right tool is matched to the right gap.

---

## References

1. **Sanders, B. & Mayes, B. (2026).** *WP58 — Unified Orthogonality
   Principle (Theorem 0).* Canonical location
   [`Gen12/targets/clay/papers/sprint12_uop_gut_arc_2026_04_08/WP58_UNIFIED_ORTHOGONALITY_PRINCIPLE.md`](https://github.com/TiredofSleep/ck/blob/paradox-classifier-2026-04-24/Gen12/targets/clay/papers/sprint12_uop_gut_arc_2026_04_08/WP58_UNIFIED_ORTHOGONALITY_PRINCIPLE.md)
   on the classifier branch.
2. **Sanders, B., Gish, M., Luther, C.A., Johnson, H.J. (2026).**
   *WP101 — σ-rate theorem.* Canonical location
   [`Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/`](https://github.com/TiredofSleep/ck/tree/paradox-classifier-2026-04-24/Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10)
   on the classifier branch.
3. **Mantero, P. & Nguyen, V. C. (2024).** *Focal matroids and
   symbolic powers.* arXiv:2406.13759.
4. **Mantero, P. & Nguyen, V. C. (2025).** *Symbolic powers of
   matroidal ideals.* arXiv:2510.19018.
5. **Mantero, P. & Nguyen, V. C. (2026).** *Linear strand and
   focal obstructions.* arXiv:2603.19419.
6. **Bocci, C. & Harbourne, B. (2010).** *Comparing powers and
   symbolic powers of ideals.* J. Algebraic Geom. 19, 399–417.
7. **Hochster, M. & Huneke, C. (1990).** *Tight closure, invariant
   theory, and the Briançon-Skoda theorem.* J. Amer. Math. Soc. 3,
   31–116.
8. **Stanley, R. (1996).** *Combinatorics and Commutative Algebra.*
   2nd ed., Birkhäuser.
9. **Bruns, W. & Herzog, J. (1998).** *Cohen-Macaulay Rings.* CUP
   Rev. ed.
10. **Waldschmidt, M. (1976).** *Propriétés arithmétiques de
    fonctions de plusieurs variables.* Séminaire Lelong-Skoda
    (Analyse) 20e année, 108–135.

---

## Appendix A — the `CL` operation table

Full 10×10 magma-operation table lives in
[`papers/sprint_20260423_full/04_mantero_bridge/MANTERO_BRIDGE_V3.md`](../sprint_20260423_full/04_mantero_bridge/MANTERO_BRIDGE_V3.md)
§2 on this branch. Reproduced here only to the extent needed to make
`I_CL` unambiguous.

*(For the full table, see the sprint bundle on the mantero-bridge
branch. The 10×10 integer matrix `CL[i][j]` with
`i, j ∈ {0, …, 9}` defines the binomial relations
`x_i x_j − x_{CL(i,j)} x_0`. `CL` is non-associative; its
associativity failure σ is documented in WP101.)*

---

## Appendix B — relationship to the paradox-classifier's four shipped templates

Each of the five shipped worked-paradox templates answers a
single-type question in the "paradoxes of mathematics" register. The
distance tuple answers a **four-type question in a single
mathematical object**. The two uses of UOP are dual:

- **Paradox template:** fix the object, ask which type the
  failure is.
- **Distance tuple:** fix the failure-type axis, measure how far
  the object sits from each type's admissible class.

Both are consequences of WP58 Theorem 0; neither supersedes the
other. Together they populate the UOP cell of the meta-lens atlas at
two distinct abstraction levels.
