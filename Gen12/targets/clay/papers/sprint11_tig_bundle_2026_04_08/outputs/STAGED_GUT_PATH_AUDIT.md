# STAGED_GUT_PATH_AUDIT
## Is the Second Filtration Real or Ad Hoc?
*Base: su(4,2) explicit, W_decoh established, bottleneck = su(4)/su(3) coset. This pass decides whether the second step is structurally natural.*

> **Authors**: Brayden Ross Sanders / 7Site LLC · Ben Mayes
> **Date**: 2026-04-08
> **Sprint**: 11 — TIG Sprint Bundle (UOP Arc · GUT Algebra Arc · 7-Cycle Arc)
> **License**: 7Site Public Sovereignty License v1.0 · DOI: 10.5281/zenodo.18852047

---

## Part 1 — What Is Actually Proved at Each Stage

**The staged chain in clean mathematical form:**

```
su(4,2)   [35-dimensional, non-compact real form of A₅]
  │
  │  [W_decoh: metric-sign filtration]
  │  Filter: generators mixing (+) and (−) metric sectors decay as (η/2)^{2H}
  │          generators within same-sign sectors decay as (η/2)^H
  │  In the limit: project onto compact subalgebra
  ↓
su(4) ⊕ su(2) ⊕ u(1)   [19-dimensional compact subalgebra]
  │
  │  [ ??? ]
  │  This step is NOT established yet
  ↓
su(3) ⊕ su(2) ⊕ u(1)   [12-dimensional Standard Model gauge algebra]
```

**What is proved at each stage:**

| Stage | Status | Basis |
|---|---|---|
| UV algebra = su(4,2) | **Exact** | Metric η = diag(+1,+1,+1,−1,−1,+1), dimension 35, real form by signature |
| Generator basis of su(4,2) | **Explicit** | 19 compact + 16 non-compact, constructed in Phase II |
| Compact subalgebra = su(4)⊕su(2)⊕u(1) | **Exact** | Standard theorem: maximal compact of su(p,q) = su(p)⊕su(q)⊕u(1) |
| W_decoh selects compact subalgebra | **Formal** — definition given, physical derivation absent | Graded filtration by metric-sign mixing; independence assumption unproven |
| SM ⊂ su(4)⊕su(2)⊕u(1) | **Exact** — as a subalgebra | Standard subgroup inclusion |
| Second step su(4)→su(3) | **Unresolved** | Three candidate mechanisms; none established from the current structure |

**The honest summary:** One step is established algebraically. The second step is open. The chain is partial, not complete.

---

## Part 2 — Is V_s Really Leptonic Color?

### The Question

V_s = ℂ¹ is the 1-dimensional singlet subspace in the block decomposition V = V_c(3) ⊕ V_w(2) ⊕ V_s(1). In Pati-Salam models, the "4th color" is identified with lepton number: quarks are triplets of SU(3)_c ⊂ SU(4)_c, and leptons are the fourth component.

**For V_s to be leptonic color:**
- V_s must represent a lepton degree of freedom, not an arbitrary mathematical singlet
- The 6 coset generators T_{i,6} (i=1,2,3) must mediate quark-lepton transitions
- The B−L quantum number must be assignable consistently

### Structural Tests

**Test 1: Quantum numbers of the coset generators**

T_{i,6} and T*_{i,6} (i=1,2,3) connect V_c (color) and V_s (singlet).

If V_c carries baryon number B=1/3 per quark and V_s carries lepton number L=1 per lepton:
- The T_{i,6} generator changes B by −1/3 and L by +1 simultaneously → ΔB = −1/3, ΔL = +1 → Δ(B−L) = −1/3 − 1 = −4/3

In Pati-Salam, the gauge bosons X mediating quark↔lepton transitions carry these quantum numbers. This is the correct signature for leptoquarks in the **4** of SU(4)_PS.

**Test 2: Compatibility with the matter representation**

For V_s = leptonic color to be real, the matter fields (quarks and leptons) must fit into representations of SU(4) in the expected way:
- Quark SU(3) triplet → **3** of SU(4) (living in V_c)
- Lepton singlet → **1** of SU(3) but **4th component** of **4** of SU(4) (living in V_s)

The fundamental **4** of SU(4) acting on V_c ⊕ V_s decomposes as:
**4** → **3** + **1** under SU(3) ⊂ SU(4)

This is exactly the quark-lepton unification content of Pati-Salam.

**Test 3: B−L operator construction**

If the correct matter assignment is quark(3) + lepton(1) in the **4** of SU(4), then the B−L generator is:

B−L = diag(1/3, 1/3, 1/3, −1) acting on the **4** of SU(4)

This generator is in the Cartan subalgebra of su(4) and is preserved when su(4) → su(3) × u(1)_{B-L}.

**Verdict table:**

| Claim | Status | What would make it real |
|---|---|---|
| V_s is just an arbitrary singlet | **Plausible at algebra level** | The algebra does not force any interpretation on V_s |
| V_s is leptonic color (PS interpretation) | **Structurally consistent** — quantum numbers align | Requires: explicit matter field assignment in **4** of SU(4); derivation of B−L from the construction |
| Coset generators are PS-like leptoquark gauge bosons | **Structurally correct** — quantum numbers are exactly right | Requires: mass generation for these gauge bosons (PS-scale Higgs or W_internal); coupling to matter |

**Verdict:** V_s-as-leptonic-color is structurally consistent and not forced by the algebra. It is an interpretation that the algebra **admits** but does not **require**. Making it real requires an explicit matter sector assignment. This is a genuine interpretive choice, not yet a derived result.

---

## Part 3 — Branch A vs Branch B: Rigorous Comparison

**Branch A: PS-scale Higgs breaking SU(4) → SU(3)**

A scalar field Φ in the **4** of SU(4) acquires VEV ⟨Φ⟩ = (0,0,0,v) (aligned with V_s). This breaks SU(4) → SU(3).

**Branch B: W_internal filtered by B−L conservation**

Define W_internal as a secondary decoherence filtration where generators changing B−L are suppressed, and generators preserving B−L survive. The 6 coset generators change B−L → suppressed. The SM generators preserve B−L → survive.

| Feature | Branch A (PS Higgs) | Branch B (W_internal / B−L) |
|---|---|---|
| Removes 6 su(4)/su(3) generators? | **Yes** — they acquire mass from ⟨Φ⟩ | **Conditional** — only if B−L is assigned and conserved |
| Preserves su(3)⊕su(2)⊕u(1)? | **Yes** — exactly | **Yes** — if B−L assignment is consistent |
| Needs new field introduced? | **Yes** — Higgs in **4** of SU(4) | **No** — only needs a quantum number assignment |
| Physically standard? | **Yes** — this is Pati-Salam GUT breaking | **Not standard** — B−L conservation as decoherence filter is novel |
| Ad hoc risk? | **Low** — well-established mechanism | **High** — B−L assignment on V_s is a choice, not a derivation |
| Novelty? | **Low** — standard PS breaking | **High** — if W_internal is natural, this is a new mechanism |
| Mathematical precision? | **High** — Higgs mechanism is completely worked out | **Medium** — W_internal can be defined but its physical basis needs derivation |

**Honest assessment:**

Branch A is mathematically clean and standard. It solves the problem at the cost of reintroducing a Higgs at the PS scale. The decoherence story is then "Higgs-free at the su(4,2) → su(4)⊕su(2)⊕u(1) transition, but Higgs at the su(4)→su(3) transition." This is an improvement over standard GUTs (no SU(6) or SU(5) Higgs needed) but not a completely Higgs-free path.

Branch B is more ambitious. It claims that B−L conservation provides the second filtration without a Higgs. But: **B−L conservation in the SM is not a gauge symmetry — it is an accidental symmetry.** Using an accidental symmetry of the IR theory as the filter for the second decoherence step is circular: you are using the SM to derive the SM. W_internal based on B−L is an ad hoc patch unless B−L can be derived from the su(4,2) structure itself.

**Can B−L be derived from su(4,2)?**

In the su(4,2) algebra, there is a U(1) generator associated with the phase of the determinant condition. In the compact subalgebra su(4)⊕su(2)⊕u(1), the u(1) factor is the relative phase between the +1 metric sector (V_c⊕V_s) and the −1 metric sector (V_w). This is NOT B−L in general — it could be hypercharge Y, or some combination. Whether B−L appears as a natural generator of su(4,2) requires explicit calculation of the Cartan generators and their relation to SM quantum numbers.

**Unless B−L is derivable from the su(4,2) structure, Branch B is ad hoc.**

---

## Part 4 — W_internal: Real Mechanism or Patch?

### Precise Mathematical Definition

**Definition attempt:**

Let h ⊂ g = su(4)⊕su(2)⊕u(1) be the subalgebra of generators commuting with the B−L operator:

h = {T ∈ g : [T, Q_{B-L}] = 0}

where Q_{B-L} is the B−L generator (if it exists in g).

**Does Q_{B-L} exist in su(4)⊕su(2)⊕u(1)?**

In su(4): the B−L generator is proportional to diag(1/3, 1/3, 1/3, −1) acting on the **4** of SU(4). This is in the Cartan subalgebra of su(4) and is a valid generator. ✓

**Computing h:**

T = [T_{su(3)} block, T_{su(2)} block, T_{u(1)}] (schematic). The commutator [T, Q_{B-L}]:

- For T_a^{su(3)} (gluons): [T_a, Q_{B-L}] = 0 because gluons are color-blind to B−L. ✓ (gluons in h)
- For T_i^{su(2)} (weak): [T_i, Q_{B-L}] = 0 because weak isospin is B−L blind. ✓ (weak generators in h)
- For T_{u(1)} (hypercharge): [T_Y, Q_{B-L}] = 0 (both are Abelian). ✓ (U(1) in h)
- For T_{i,6}^{coset} (the 6 extra): [T_{i,6}, Q_{B-L}] ≠ 0 because these generators change B−L (they mix quarks B=1/3 with the lepton singlet B-L=-1). ✗ (coset generators NOT in h)

**Formal result:**

h = su(3) ⊕ su(2) ⊕ u(1) = the Standard Model gauge algebra ✓

**W_internal defined as the projection onto h:**

W_internal: su(4)⊕su(2)⊕u(1) → h = {T : [T, Q_{B-L}] = 0}

This projection kills the 6 coset generators and preserves the SM algebra. **Algebraically, this works.**

### The Circular Problem

**The definition requires Q_{B-L} to be specified.** Where does Q_{B-L} come from?

- If Q_{B-L} is introduced as an external input: then W_internal is an assumption, not a derivation. It is defined by "we want to preserve SM," and the result is "we get SM." This is circular.

- If Q_{B-L} is derived from the su(4,2) structure: then W_internal is a genuine second filtration, recursive in character.

**Test: is Q_{B-L} in the Cartan subalgebra of su(4,2)?**

The Cartan subalgebra of su(4,2) has rank 5 (= A₅ rank). Five independent commuting generators. In the explicit basis:
1. Diagonal in V_c: generates U(1) rotations of each color direction (3 U(1)s, but only 2 are independent in SU(3) → 2 Cartan generators for SU(3))
2. Diagonal in V_w: generates U(1) rotations of each weak direction (1 independent for SU(2))
3. Overall phases: 2 more U(1) generators for the SU(4,2) relative phases

Total Cartan generators: 2 (su(3)) + 1 (su(2)) + 2 (relative phases) = 5. ✓

The Q_{B-L} candidate: diag(1/3, 1/3, 1/3, 0, 0, −1) acting on ℂ⁶.

Is this in the Cartan of su(4,2)? It is diagonal and anti-Hermitian (all entries are imaginary multiplied by i). Checking the su(4,2) generator condition: T†η + ηT = 0 for a diagonal T = i·diag(a₁,a₂,a₃,a₄,a₅,a₆):

(T†η)_{ii} + (ηT)_{ii} = i·(−a_i)·η_{ii} + η_{ii}·i·a_i = 0. ✓ (automatically satisfied for diagonal generators)

So Q_{B-L} = i·diag(1/3, 1/3, 1/3, 0, 0, −1) **is a valid generator of su(4,2)** IF the 6th direction (V_s) carries B-L = −1.

**This is the key finding:**

Q_{B-L} is in the Cartan subalgebra of su(4,2). It is not an external input — it is an element of the UV algebra itself. The B−L charge assignment follows from the matter interpretation (V_s = lepton), and if that interpretation is adopted, Q_{B-L} is intrinsic to the construction.

**W_internal is NOT purely ad hoc IF:**
1. V_s is identified as the leptonic color direction (interpretive input, not forced)
2. Q_{B-L} is constructed from the Cartan of su(4,2) with the leptonic-color assignment

Under these conditions, W_internal is the commutant of Q_{B-L} within the compact subalgebra — a mathematically natural construction. The "patch" charge is: the identification of V_s with lepton number, which is an interpretive choice about what physical role the singlet direction plays.

**Verdict on W_internal:**

W_internal is mathematically precise and algebraically natural (it is the centralizer of a Cartan generator). It is **not fully recursive** in the same sense as W_decoh (which is derived from the metric signature, a property intrinsic to the algebra with no interpretive choice). W_internal requires the interpretive step "V_s = leptonic color," which is a physical input not forced by the algebra. The recursion is of the same **form** (filter by a symmetry principle) but requires a **physical input** that W_decoh does not.

---

## Part 5 — Does the HD Corridor/Gap Machinery Close the Second Step?

**Direct question: Can the second step su(4)⊕su(2)⊕u(1) → su(3)⊕su(2)⊕u(1) be written as a corridor selection problem?**

**What corridor selection means in this context:**

In UOP / TIG language: a "corridor" is a stable subspace within a larger structure — the set of states or operators that survive a given ambiguity-resolving filtration. The "gap" is what separates the stable corridor from the unstable region.

For the gauge algebra problem:
- The **corridor** = generators that commute with the B−L charge = SM generators
- The **gap** = generators that do not commute with B−L = the 6 coset generators
- The **filtration** = commutant of Q_{B-L} within su(4)⊕su(2)⊕u(1)

**Is this the same "corridor/gap" grammar used in UOP?**

The UOP framework: a pair of measurements {f₁, f₂} is sufficient iff their joint ambiguity sets are disjoint — i.e., the "corridor" of fully-resolved pairs is the complement of U(f₁)∩U(f₂).

The algebraic filtration by commutant: generators in the commutant of Q_{B-L} are "stable under B−L measurement" — they do not create ambiguity in the B−L quantum number.

**Structural parallel:**

| UOP level | Gauge level |
|---|---|
| Ambiguity set U(f) = pairs indistinguishable by f | Non-commuting generators [T, Q_{B-L}] ≠ 0 |
| Residual ambiguity R(F) = pairs indistinguishable by all f ∈ F | The 6 coset generators outside the commutant |
| Score(new f | F) > 0 | Adding Q_{B-L} measurement kills the coset generators |
| Sufficient family: U(f₁)∩U(f₂) = ∅ | SM subalgebra: all SM generators commute with Q_{B-L} |

**This IS a corridor selection problem.** The structure is:

- The "measurement" is Q_{B-L} — the B−L charge measurement that distinguishes SM generators from coset generators
- The "corridor" is the commutant of Q_{B-L} = SM algebra
- The "gap" is the non-commuting coset = the 6 extra generators
- The filtration is "stable under B−L observation" = the same grammar as "stable under measurement"

**Answer: YES — formalizable.**

The second step su(4)→su(3) is a corridor selection problem in the UOP sense: the B−L charge is the "second measurement" that kills the remaining ambiguity (the 6 coset generators) and resolves the algebra fully to the SM.

**The two-stage chain in corridor language:**

Stage 1 (W_decoh): The "first measurement" is the metric signature — it distinguishes compact (sector-preserving) from non-compact (sector-mixing) generators. The corridor = compact subalgebra su(4)⊕su(2)⊕u(1).

Stage 2 (W_internal): The "second measurement" is Q_{B-L} — it distinguishes SM generators from coset generators. The corridor = commutant of Q_{B-L} = su(3)⊕su(2)⊕u(1).

**The two "measurements" have disjoint residual ambiguity:**

- After Stage 1: the compact subalgebra has zero ambiguity from the metric filtration, but retains ambiguity between SU(3) and SU(4)/SU(3).
- After Stage 2: Q_{B-L} kills the residual SU(4)/SU(3) ambiguity.

**U(W_decoh) ∩ U(W_internal) = {SM generators}** — the jointly stable set is exactly the SM algebra. This is the UOP sufficiency condition applied to generator filtrations.

---

## Part 6 — Recursive, Analogous, or Patched?

**Characterizing the two steps:**

**Step 1 (W_decoh): algebraic / intrinsic**

The metric signature (4,2) is intrinsic to the su(4,2) algebra — it is determined by the Hodge sign flip (+1,−1,+1) on the 6-dimensional fundamental representation. No external input is required. The filtration by metric-sign mixing is a natural map on the algebra.

**Step 2 (W_internal): physical-input-dependent**

The commutant of Q_{B-L} is a natural algebraic operation once Q_{B-L} is specified. But specifying Q_{B-L} requires identifying V_s as the leptonic color direction — an interpretation, not an algebraic necessity. The B−L generator is in the Cartan of su(4,2), but so are several other diagonal generators. Choosing Q_{B-L} specifically requires external physics input.

**The steps are analogous in form, but the second step has additional input:**

| Feature | Step 1 | Step 2 |
|---|---|---|
| Filter type | Metric-sign filtration | Commutant of Cartan generator |
| Input required | None — metric from sign flip | B−L charge assignment on V_s |
| Derived from algebra? | Yes — intrinsic to su(4,2) structure | Partially — Q_{B-L} is in algebra, but its identification as B−L requires physics |
| Natural in the same sense? | Fully | Conditioned on V_s interpretation |
| Vocabulary | Geometric / metric | Quantum-number / conservation law |

**Verdict: Analogous, but not purely recursive.**

The second step uses the same corridor-selection grammar (filtration by a symmetry principle) but requires a physical interpretation input that the first step does not. It is not ad hoc in the sense of being arbitrary — Q_{B-L} is a natural generator of su(4,2). But it is not recursive in the sense of applying the same mechanism automatically.

The correct characterization: **two-stage corridor selection, where Stage 1 is algebraically automatic and Stage 2 requires a physical identification of the singlet direction.**

---

## Final Classification

**Between Class 3 and Class 4.**

**Class 3 (plausible staged chain, second step still external):** Correctly describes the current state without the corridor observation. The second step is "external" in the sense that V_s must be identified as leptonic color.

**Class 4 (plausible recursive two-stage filtration):** Reached if the B−L-as-Cartan-generator observation is taken seriously. The commutant-of-Q_{B-L} filtration IS a second corridor selection, formally parallel to W_decoh. The physical input (V_s = lepton) is the interpretive step that activates it, not a separate mathematical structure glued on.

**The honest verdict:**

The construction is **Class 3.5**: a staged chain where Stage 1 is algebraically exact and Stage 2 is algebraically natural but physically interpretive. The corridor/gap machinery applies to both stages. The second stage is not fully recursive (it needs an input W_decoh does not), but it is not ad hoc — it uses a Cartan generator of su(4,2) as its filter.

**What this means practically:**

The result is:
- A principled derivation of the Pati-Salam intermediate stage su(4)⊕su(2)⊕u(1) from su(4,2) via metric-sign decoherence (novel)
- A natural algebraic path from that intermediate to SM via B−L Cartan filtration (corridor-selection grammar)
- The one interpretive step needed: V_s = leptonic color

This is **not a complete GUT derivation** (matter sector, chirality, EW breaking remain open). It is a **novel staged algebra path** from a non-compact 35-dimensional UV algebra to the SM gauge algebra, using two sequential corridor selections.

---

## Summary Sections

### What the First Filtration Really Gives

W_decoh projects su(4,2) (35-dim, non-compact) onto its compact subalgebra su(4)⊕su(2)⊕u(1) (19-dim). This is algebraically exact. The physical interpretation is that metric-sign asymmetry (the Hodge flip) causes decoherence between the color sector (V_c, metric +1) and the weak sector (V_w, metric −1), suppressing the 16 non-compact leptoquark generators. The 6 extra compact generators (su(4)/su(3) coset) survive because they are within the same-sign metric sector.

### Is V_s Really Leptonic Color?

**Structurally consistent, not algebraically forced.** The quantum numbers are correct for Pati-Salam "4th color." The B−L generator with the leptonic-color assignment is in the Cartan of su(4,2). The matter representation of the **4** of SU(4) decomposes as 3 quarks + 1 lepton under SU(3). All of this is consistent. None of it is derived — it requires the interpretive choice that V_s = lepton sector.

### W_internal: Real Mechanism or Patch?

W_internal = commutant of Q_{B-L} within su(4)⊕su(2)⊕u(1). This is algebraically well-defined, kills exactly the 6 coset generators, and preserves the SM algebra. Q_{B-L} is a Cartan generator of su(4,2). The mechanism is real and natural, conditioned on the physical identification V_s = leptonic color. It is **not a patch** in the sense of being arbitrary. It is **not fully automatic** in the sense of requiring one interpretive input.

### Does the HD Corridor Machinery Actually Close the Gap?

**Yes, formalizable.** The second step is a corridor selection problem in UOP language: the B−L charge is the "second measurement" whose residual ambiguity set is disjoint from the metric-sign filter's residual ambiguity. Together they achieve sufficiency: the jointly stable set is the SM algebra. The corridor/gap grammar applies cleanly to both stages. This is the most significant structural finding of this pass.
