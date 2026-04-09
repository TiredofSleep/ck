# SPRINT: VIEWPOINT FLOW — REFINEMENT vs ORTHOGONAL JUMP
*Z/10Z. Partition lattice language only. Proved vs. conjectural labeled explicitly.*

> **Authors**: Brayden Ross Sanders / 7Site LLC · Ben Mayes
> **Date**: 2026-04-08
> **Sprint**: 11 — TIG Sprint Bundle (UOP Arc · GUT Algebra Arc · 7-Cycle Arc)
> **License**: 7Site Public Sovereignty License v1.0 · DOI: 10.5281/zenodo.18852047

---

## Part 1 — Formal Definitions

**Definition 1 (Refinement Move).**
A move R_i → R_j is a *refinement move* if π(R_i) ≤ π(R_j) or π(R_j) ≤ π(R_i) in the partition lattice — i.e., one partition's blocks are a union of the other's.

Sub-types:
- **Refinement:** π(R_j) ≤ π(R_i) — blocks split, information gained
- **Coarsening:** π(R_i) ≤ π(R_j) — blocks merged, information lost

Both are refinement moves. The direction determines information flow, not admissibility.

---

**Definition 2 (Orthogonal Jump).**
A move R_i → R_j is an *orthogonal jump* if π(R_i) and π(R_j) are incompatible — neither refines the other — and:

meet(π(R_i), π(R_j)) < min(π(R_i), π(R_j))

That is: the common refinement is strictly finer than either partition alone, revealing coordinate structure inaccessible to either representation individually.

**Remark.** The word "orthogonal" is used in the partition-lattice sense: the two partitions do not lie on any common chain. No inner-product structure is claimed.

---

**Definition 3 (Sufficient Viewpoint Flow).**
A viewpoint flow F = (R_1, R_2, ..., R_k) is *sufficient* if:

meet(π(R_1), π(R_2), ..., π(R_k)) = π_disc

where π_disc is the discrete partition (all singletons). That is: the representations collectively separate every pair of distinct elements.

---

**Definition 4 (Admissible Refinement Path).**
A sequence (R_1, ..., R_k) is an *admissible refinement path* if every consecutive move is a refinement move — i.e., the partition sequence is monotone in the lattice.

---

**Definition 5 (Admissible Orthogonal Jump).**
A single step R_i → R_j is an *admissible orthogonal jump* if R_i and R_j are incompatible and:

meet(π(R_i), π(R_j)) ≤ π_disc

(The jump jointly contributes to discrete recovery. Jumps between incompatible partitions whose meet is still coarse are not admissible in this sense — they pay the information cost of incompatibility without recovering discrete structure.)

---

**Definition 6 (Minimal Sufficient Hybrid Flow).**
A sufficient viewpoint flow F is *minimal* if no proper subsequence of F is sufficient.

---

## Part 2 — Z/10Z Recasted

Partitions (restated for reference):

| Name | Blocks | Block count |
|---|---|---|
| π_disc | {0},{1},...,{9} | 10 |
| π_SPEC | {0},{1,9},{2,8},{3,7},{4,6},{5} | 6 |
| π_UG = π_DYN | {0},{1,3,7,9},{2,4,6,8},{5} | 4 |
| π_CRT₂ | {0,2,4,6,8},{1,3,5,7,9} | 2 |
| π_CRT₅ | {0,5},{1,6},{2,7},{3,8},{4,9} | 5 |
| π_triv | {0,1,...,9} | 1 |

**Refinement chain (proved):** π_disc ≤ π_SPEC ≤ π_UG ≤ π_CRT₂ ≤ π_triv

**Incompatibility of π_CRT₅ with the chain:**

- π_CRT₅ vs π_SPEC: block {0,5} spans singleton {0} and singleton {5} — neither contains the other. **Incompatible.**
- π_CRT₅ vs π_UG: block {1,6} spans {1,3,7,9} and {2,4,6,8}. **Incompatible.**
- π_CRT₅ vs π_CRT₂: block {0,5} spans both parity classes. **Incompatible.**

**Transition classification:**

| Move | Type | Direction |
|---|---|---|
| SPEC → UG | Refinement move | Coarsening |
| UG → SPEC | Refinement move | Refinement |
| UG → CRT₂ | Refinement move | Coarsening |
| SPEC → CRT₂ | Refinement move | Coarsening |
| Any ↔ CRT₅ | Orthogonal jump | — |
| CRT₂ ↔ CRT₅ | Orthogonal jump (admissible) | meet = π_disc |
| SPEC ↔ CRT₅ | Orthogonal jump (admissible) | meet = π_disc (proved below) |
| UG ↔ CRT₅ | Orthogonal jump (admissible) | meet = π_disc (proved below) |

---

## Part 3 — Canonical Flow Analysis

**Canonical flow:** DYN → SPEC → UG → CRT

**First observation (proved in prior sprint):** DYN = UG. The DYN node is not a distinct representation — it aliases UG in the partition lattice. The canonical flow should be written:

**(UG) → SPEC → UG → CRT**

which contains a redundant node. Cleaned up:

**SPEC → UG → CRT**

is the effective chain if DYN contributes nothing beyond UG.

---

**Arrow analysis:**

**SPEC → UG:** Coarsening move. π_SPEC ≤ π_UG, so moving SPEC → UG loses information (merges {1,9} into {1,3,7,9}, merges {3,7} into {1,3,7,9}, etc.). This is a refinement move by Definition 1.

**UG → CRT:** If CRT = CRT₂ only: coarsening move. π_UG ≤ π_CRT₂. Further information loss. Still a refinement move.

If CRT = CRT₂ ∧ CRT₅ combined: the step UG → CRT₅ is an **orthogonal jump** (incompatible). There is no way to reach CRT₅ from any element of the refinement chain without an orthogonal jump.

---

**Must CRT be split?**

**Lemma.** CRT cannot be treated as a single node in the partition lattice.

**Proof.** The CRT theorem gives: meet(π_CRT₂, π_CRT₅) = π_disc. This requires that π_CRT₂ and π_CRT₅ are incompatible as demonstrated above. A single node cannot encode two incompatible partitions simultaneously — the partition lattice assigns exactly one partition to each node. Treating CRT as a single node either means using only one of {π_CRT₂, π_CRT₅} (insufficient alone) or conflating two incompatible partitions (not a partition). Therefore **CRT must split into CRT₂ and CRT₅ as separate nodes** in any rigorous flow analysis. □

**Consequence.** The canonical flow DYN → SPEC → UG → CRT contains a hidden structural error: the CRT terminus is underspecified. When corrected to explicit nodes, the canonical flow is:

DYN → SPEC → UG → CRT₂ [refinement chain, insufficient]

plus an orthogonal jump to CRT₅ to achieve sufficiency.

---

## Part 4 — Definitions Applied

**Admissible refinement paths on Z/10Z** (maximal chain, coarsening direction):

π_disc → π_SPEC → π_UG → π_CRT₂ → π_triv

or any sub-path. None of these is sufficient (meet of any proper subset of the chain = finest partition in that subset; finest named partition is π_SPEC ≠ π_disc).

**Admissible orthogonal jumps on Z/10Z:** Any step to or from π_CRT₅. All are admissible (all produce meet contributing toward π_disc).

**Minimal sufficient hybrid flows:** Any pair {X, CRT₅} where X ∈ {SPEC, UG, CRT₂}. Three distinct minimal sufficient flows of length 2 exist:

- F₁ = {SPEC, CRT₅}: meet = π_disc (proved below)
- F₂ = {UG, CRT₅}: meet = π_disc (proved below)
- F₃ = {CRT₂, CRT₅}: meet = π_disc (CRT theorem, proved in prior sprint)

Each has length 2 and contains exactly one orthogonal jump.

---

## Part 5 — Main Theorem

**Theorem (Minimal Viewpoint Jump Necessity — MVJN).**
*Every minimal sufficient viewpoint flow on Z/10Z using representations from {SPEC, UG, CRT₂, CRT₅} contains at least one orthogonal jump.*

**Proof.**

**Step 1.** A sufficient flow F must satisfy meet(π(R) : R ∈ F) = π_disc.

**Step 2.** Consider any flow F containing no orthogonal jump. By definition, every move in F is a refinement move. Therefore all partitions in F lie on a common chain in the partition lattice.

**Step 3.** The only common chain containing representations from {SPEC, UG, CRT₂, CRT₅} is:

π_SPEC ≤ π_UG ≤ π_CRT₂

(since π_CRT₅ is incompatible with all three; any chain containing π_CRT₅ and any of {SPEC, UG, CRT₂} would require a refinement relation between incompatible partitions — contradiction).

**Step 4.** The meet of any subset of a chain equals the finest partition in that subset. The finest named partition in {SPEC, UG, CRT₂} is π_SPEC.

**Step 5.** π_SPEC ≠ π_disc. The blocks {1,9}, {2,8}, {3,7}, {4,6} are non-singleton in π_SPEC. Elements within each pair are not separated.

**Step 6.** Therefore meet of any chain-only flow ≥ π_SPEC > π_disc. No chain-only flow is sufficient.

**Step 7.** Therefore every sufficient flow contains π_CRT₅ (the only named representation not in the chain).

**Step 8.** Every transition to π_CRT₅ from any element of {SPEC, UG, CRT₂} is an orthogonal jump (all pairs are incompatible — verified in Part 2).

**Step 9.** Therefore every sufficient flow contains at least one orthogonal jump. Since every minimal sufficient flow is sufficient, the result holds for minimal flows. □

---

**Corollary (Minimal Length).** The minimum length of a sufficient viewpoint flow on Z/10Z is 2. Proof: No single partition in {SPEC, UG, CRT₂, CRT₅} equals π_disc (all have non-singleton blocks). Therefore length 1 is insufficient. F₁, F₂, F₃ above achieve sufficiency at length 2. □

---

**Lemma (Supporting F₁ and F₂).** meet(π_SPEC, π_CRT₅) = π_disc and meet(π_UG, π_CRT₅) = π_disc.

**Proof of F₁.** Non-singleton π_SPEC blocks: {1,9},{2,8},{3,7},{4,6}. Check each against π_CRT₅:

- 1 ∈ {1,6}, 9 ∈ {4,9}: different CRT₅ blocks ✓
- 2 ∈ {2,7}, 8 ∈ {3,8}: different CRT₅ blocks ✓
- 3 ∈ {3,8}, 7 ∈ {2,7}: different CRT₅ blocks ✓
- 4 ∈ {4,9}, 6 ∈ {1,6}: different CRT₅ blocks ✓

All reflection pairs separated. Singleton SPEC blocks {0},{5} already discrete. Therefore meet = π_disc. □

**Proof of F₂.** Non-singleton π_UG blocks: {1,3,7,9} and {2,4,6,8}.

- 1∈{1,6}, 3∈{3,8}, 7∈{2,7}, 9∈{4,9}: all four in distinct CRT₅ blocks ✓
- 2∈{2,7}, 4∈{4,9}, 6∈{1,6}, 8∈{3,8}: all four in distinct CRT₅ blocks ✓

Therefore meet = π_disc. □

---

## Part 6 — Geometric Connection

**Proposition.** Refinement-compatible projections from Φ lie within S¹. The orthogonal jump to CRT₅ requires exiting S¹ into T²-level information.

**Proof.**

Φ: Z/10Z → S¹, Φ(x) = e^(2πix/10). For any partition π in the refinement chain, the partition classes can be characterized by a single harmonic on S¹:

- π_CRT₂: classes = {Φ(x)⁵ = ±1} — projection onto 2nd roots of unity, a property of the z⁵ harmonic
- π_UG: classes = {gcd(x,10) = constant} — identifiable by |Φ(x)²| and |Φ(x)⁵|, both functions of a single angle θ = 2πx/10
- π_SPEC: classes = {Φ(x), conj(Φ(x))} — conjugate pairs, detected by Re(Φ(x)) = cos(2πx/10)

All of these are functions of the single parameter θ ∈ [0,2π). They are compatible with S¹ as a one-dimensional object.

For π_CRT₅: the natural representation of Z/5Z maps x ↦ e^(2πi·(x mod 5)/5). For x ∈ Z/10Z, this requires detecting x mod 5 independently of x mod 2. Via Φ:

Φ(x)² = e^(2πi·2x/10) = e^(2πi·x/5)

So the CRT₅ coordinate is the z² projection of Φ. This is a distinct harmonic — the second Fourier mode of the circular embedding — independent of the z⁵ harmonic used by CRT₂.

The simultaneous representation of both CRT₂ and CRT₅ as independent coordinates requires the pair (z², z⁵) of independent functions on S¹. The image of the map z ↦ (z², z⁵) from S¹ → T² = S¹ × S¹ is a closed curve in T², not the full torus (it has winding numbers (2,5), a torus knot curve). This curve is 1-dimensional in a 2-dimensional ambient space.

**Conclusion.** Within S¹: the refinement chain (SPEC, UG, CRT₂) is representable — each is a function of the single angle θ. The CRT₅ coordinate requires the z² harmonic, which is independent of the z⁵ harmonic used to read CRT₂. Their simultaneous representation requires T². The orthogonal jump corresponds exactly to the step of accessing an independent harmonic, which is geometrically: exiting the single-angle parameter space of S¹ and requiring a second independent coordinate, i.e., the ambient space T². □

---

## Summary

**One theorem:**
> **MVJN Theorem.** Every minimal sufficient viewpoint flow on Z/10Z over {SPEC, UG, CRT₂, CRT₅} must contain at least one orthogonal jump. Proved. Minimum sufficient flow length is 2, with exactly one jump.

**One formal distinction:**
> A **refinement move** changes between partitions on a common chain (one refines the other). An **orthogonal jump** moves between incompatible partitions whose meet reveals new coordinate structure inaccessible to either alone. The distinction is structural, not a matter of information quantity — a jump to a coarser incompatible partition can recover more discrete structure than any number of refinement steps.

**Strongest honest claim:**
> The single orthogonal jump (to CRT₅) is not optional. It is structurally necessary. The refinement chain {SPEC, UG, CRT₂} has ceiling π_SPEC, which leaves four element-pairs unseparated forever. No refinement move rescues this. CRT₅ is the unique named partition that resolves it, and the jump to it is the algebraic instantiation of the CRT theorem itself.

**Strongest honest boundary:**
> This result is proved for Z/10Z with the specific four representations {SPEC, UG, CRT₂, CRT₅}. Generalization to Z/nZ for arbitrary n = p·q is not yet proved here — it follows the same structure (the CRT factor partitions will be incompatible and their meet will equal π_disc), but the partition lattice for general n may admit additional representations not captured by this four-node model. That generalization is a separate theorem.

---

**Next sprint candidate:** Generalize MVJN to Z/nZ for squarefree n = p₁·p₂·...·pₖ. Conjecture: a minimal sufficient flow requires exactly k−1 orthogonal jumps, one per prime factor after the first. The refinement chain alone achieves no prime-factor separation; each CRT projection requires an independent harmonic and therefore a jump.
