# WP72 — Flag Selector from Physical Anisotropy
## What Real Datum Could Supply F* in SU(3)/T?

**Date**: 2026-04-09
**Sprint**: 13 — Physical Flag Selector
**Authors**: Brayden Ross Sanders / 7Site LLC · Ben Mayes · C.A. Luther

---


## The Exact Flag Requirement

A complete flag $F^* = (V_1 \subset V_2 \subset \mathbb{C}^3)$ is equivalent to an **ordered pair of orthogonal complex lines** $(L_1, L_2)$ in $\mathbb{C}^3$:
- $L_1 = V_1$: a 1-dim complex subspace — a point in $\mathbb{CP}^2$ (**4 real dims**)
- $L_2 = V_2 \ominus V_1$: a 1-dim complex subspace orthogonal to $L_1$ — a point in $\mathbb{CP}^1$ within the orthogonal $\mathbb{C}^2$ (**2 real dims**)
- $L_3 = (L_1 \oplus L_2)^\perp$: determined by orthogonality, no additional data needed

**Total: 4 + 2 = 6 real dims = dim(SU(3)/T). ✓**

### Taxonomy of flag-adjacent data

| Datum | Real dims | Gives flag? | What's missing |
|---|---|---|---|
| Single complex line $L_1$ in $\mathbb{C}^3$ | 4 ($\mathbb{CP}^2$) | No | $L_2$: 2 more dims |
| Real orthogonal frame in $\mathbb{R}^3$ | 3 ($\text{SO}(3)$) | No | Wrong space AND wrong type |
| Vortex axis + rotation | 3–4 | No | At best one complex line (4 dims); still missing $L_2$ |
| **Ordered orthogonal pair $(L_1, L_2)$** | **6** | **Yes** | **Nothing — this IS the flag** |
| Hermitian operator on $\mathbb{C}^3$ (no eigenvalue data) | 6 | Yes | Nothing — eigenvectors give the flag exactly |
| Unit vector pair $(\hat{v}_1, \hat{v}_2)$ orthogonal | 8 | Yes + torus | Mixes flag directions and phases; gives full bridge point |

**The key separation:** an ordered pair of complex LINES (projectors) gives the flag without the torus. An ordered pair of complex unit VECTORS gives the bridge point (flag + torus phases). Physical datum candidates must be assessed against this distinction.

---

## Candidate Classification Table

| | **A: Anisotropy tensor** | **B: Vortex-axis pair** | **C: Ordered proj. channels** | **D: Principal stress axes** | **E: Cardiac geometry** | **F: Toroidal field** | **G: Defect-core + polarization** | **H: Ordered ortho pair (L1,L2)** |
|---|---|---|---|---|---|---|---|---|
| **Math object** | Hermitian tensor on $\mathbb{C}^3$ → ordered eigenvectors | Axis $(S^2)$ + rotation $(U(1))$ | Ordered rank-1 Hermitian projectors $P_1, P_2$ on $\mathbb{C}^3$ | Symmetric real tensor on $\mathbb{R}^3$ → $\text{SO}(3)$ frame | 4-node loop + vortex + torus geometry in $\mathbb{R}^3$ | Torus $T/\mathbb{Z}_3$ + axis direction | Polarization winding map $S^1 \to \text{SU}(3)/T$ | Stiefel $V_2(\mathbb{C}^3)/U(1)^2 = \text{SU}(3)/T$ |
| **Real dim** | 6 (directional part) | 3 | 4+2=6 | 3 | ~7–9 (mixed types) | ~4 | 4–6 (conditional) | 6 |
| **Gives complete flag?** | YES (if on $\mathbb{C}^3$) | NO | YES | NO | NO | NO | CONDITIONAL | YES (by definition) |
| **Overdetermines to bridge?** | No | N/A | No | N/A | Mixed | No (gives torus, misses flag) | No | No |
| **Status** | Bridge | False as flag / Bridge as partial | **Exact math; Bridge physical** | False | Bridge (witness) | **Exact for torus; False for flag** | Bridge | **Exact** |
| **Measurable?** | Yes | Yes | Yes (3-state quantum system) | Yes | Yes | Yes | Yes (spinor BEC, TI) | Yes (3-component field) |

---

## Detailed Analysis

### Candidate A — Chambered-flow anisotropy tensor

A Hermitian tensor on $\mathbb{C}^3$ with non-degenerate spectrum has three ordered complex eigenvectors. Those eigenvectors (as directions, ignoring phases) ARE a complete flag $F^*$ in SU(3)/T. The eigenvalues are separate data; the directional (flag) content is exactly 6 real dims.

**Critical condition:** The tensor must act on the 3-component COMPLEX field, not on physical $\mathbb{R}^3$ space. A real-space flow anisotropy tensor gives $\text{SO}(3)$ (3 real dims, wrong type). A complex anisotropy tensor on a 3-component complex field gives 6 dims and a complete flag.

**What's missing for a full bridge:** After the Hermitian tensor gives the flag (6 dims), the torus phases (2 dims, or 1 continuous + 1 discrete sign post-FS) must still be supplied. The tensor alone does not determine torus phases.

**Status: Bridge.** The structure is coherent. The physical question is whether the relevant 3-component complex field has a measurable anisotropy tensor with non-degenerate spectrum.

### Candidate B — Vortex-axis pair + transverse plane

A vortex in $\mathbb{R}^3$ has: an axis direction (2 real dims on $S^2$) + a rotation direction in the transverse plane ($U(1)$, 1 real dim) = 3 real dims total. Promoted to a complex structure: a vortex axis with its $U(1)$ rotation naturally defines a 1-dimensional complex direction in $\mathbb{C}^3$ (up to overall phase this is a point in $\mathbb{CP}^2$, 4 real dims).

**What's missing:** The single vortex axis + rotation gives at most ONE complex line $L_1$ (4 dims). The second complex direction $L_2$ (2 more real dims) is not determined. The flag requires both.

**Status: False as complete flag selector. Bridge as partial datum** (supplies $L_1$, 4 of 6 dims).

### Candidate C — Ordered pair of orthogonal measurement channels

An ordered pair of rank-1 Hermitian projectors $(P_1, P_2)$ on $\mathbb{C}^3$, with $P_1 P_2 = 0$ (orthogonality), is mathematically identical to a complete flag:
- $P_1$ specifies the complex line $V_1 \in \mathbb{CP}^2$: 4 real dims
- $P_2$ specifies the complex line $V_2 \ominus V_1$ in the orthogonal $\mathbb{C}^2$: 2 real dims
- Total: 4 + 2 = 6 real dims = SU(3)/T

Crucially: projectors give LINES (not unit vectors), so no phase information is contained. The torus $(Z_2 \times U(1)/\mathbb{Z}_3)$ is NOT determined by the projectors. This is the MINIMAL torus-free flag selector.

**Status: Exact as mathematical description. Bridge as physical identification** (what physical system has two natural orthogonal projective channels on a 3-component complex field?).

### Candidate D — Principal stress/strain axes

A symmetric real tensor in $\mathbb{R}^3$ gives 3 real orthogonal principal axes ($\text{SO}(3)$ frame, 3 real dims). This is the wrong type and wrong dimension for a flag. Upgrading to a complex medium (complexifying $\mathbb{R}^3 \to \mathbb{C}^3$) gives a Hermitian tensor with 6 directional dims — but this is then equivalent to Candidate A, not a new datum class.

**Status: False as flag selector.** Irrelevant unless the medium is genuinely complex (i.e., Candidate A).

### Candidate E — Cardiac geometry (4 chambers + vortex + torus)

The heart's geometry lives in physical $\mathbb{R}^3$, not in the abstract $\mathbb{C}^3$ of the 3-component field. Its structural features are:
- **4 chambers + directed loop**: witnesses the downstairs loop grammar (4-node directed descent); not a flag selector
- **1 vortex (LV toroidal ring)**: witnesses the K₃ cyclic structure; gives at most 3–4 real dims in $\mathbb{R}^3$; not a flag selector
- **1 toroidal field**: witnesses the torus $T/\mathbb{Z}_3$ topology; gives torus (2 dims), not the flag (6 dims)

Mixed count: roughly 7–9 real dims of mixed types, spanning both loop grammar and torus, but neither alone gives the flag. The cardiac geometry would provide a flag selector only if there is a formal map from the cardiac field (measured as a 3-component complex field) to the relevant $\mathbb{C}^3$ — a map that does not currently exist in the proved stack.

**Status: Bridge witness across both layers; not a flag selector.** The heart WITNESSES the grammar at both the downstairs (loop) and upstairs (torus) levels but does not SUPPLY the missing 6-dim directional datum.

### Candidate F — Toroidal field axis + phase-lag structure

A toroidal field has a natural 2-dimensional torus structure (the $U(1)/\mathbb{Z}_3$ phase calibration). This is exactly the TORUS RESIDUE in the bridge — the smaller component (2 dims), not the flag (6 dims).

The toroidal field gives the PHASE SIDE of the bridge, while the flag is the DIRECTION SIDE. These are independent: specifying the torus does not help with the flag. It is precisely BACKWARDS in priority: the torus is what's left AFTER the flag is fixed; fixing the torus without fixing the flag leaves the dominant ambiguity open.

**Status: Exact for the torus; False as a flag selector.** It resolves the smaller open piece while leaving the larger piece untouched. This is an important clarification of the heart clue: the toroidal field addresses $\theta_2$ (1 cont. dim post-FS) and the orientation (1 bit), not the flag (6 dims).

### Candidate G — Defect-core + polarization framing

In a spin-1 system (spinor Bose-Einstein condensate, topological insulator surface state, or liquid crystal with 3-component order parameter), a vortex defect-core sits at a point where the 3-component order parameter vanishes. The polarization winding around the defect — the map from a circle surrounding the core into the order parameter space — is a map $S^1 \to G/H$ where $G/H$ is the relevant coset space.

For a spin-1 BEC with full $\text{SU}(2)$ symmetry: the order parameter space contains $\text{SU}(3)/T$ as a subspace when the 3-component field has the right symmetry. A full polarization framing (winding in all 3 complex components, phase-free) could define a map $S^1 \to \text{SU}(3)/T$ and, for a specific winding, a specific point in the flag variety.

**Status: Bridge — potentially the strongest naturally-occurring flag selector candidate**, but requires: (a) the physical field genuinely has 3 complex components with $\text{SU}(3)$-like symmetry; (b) the defect carries a full polarization framing (not just an axis winding). Measurable in principle with quantum state tomography.

### Candidate H — Abstract ordered orthogonal pair (L₁, L₂)

This is the definition of the flag variety. Any physical system that provides two ORDERED ORTHOGONAL COMPLEX LINES in its $\mathbb{C}^3$-valued field provides a flag selector. Mathematically: the Stiefel manifold $V_2(\mathbb{C}^3)$ modulo overall phases $U(1)^2$ is $\text{SU}(3)/T$.

**Status: Exact.** This is the target description. All other candidates are physical attempts to realize this abstract datum. The physical question is always: does this system have a 3-component complex field with identifiable ordered orthogonal complex subspaces?

---

## Theorem-Shaped Targets

### Target 1: Smallest physically meaningful external datum that gives a complete flag without automatically giving the torus

**Answer:** An **ordered pair of rank-1 Hermitian projectors** $(P_1, P_2)$ on the relevant $\mathbb{C}^3$-valued field, with $P_1 P_2 = 0$.

Properties:
- Exactly 6 real dims (4 for $P_1 \in \mathbb{CP}^2$, 2 for $P_2 \in \mathbb{CP}^1$ in $\mathbb{C}^3 \ominus L_1$)
- Gives lines, not unit vectors: the torus phases are NOT determined
- Minimal: no datum of fewer than 6 real dims generically specifies a complete flag
- Physically: measurable as two orthogonal projective measurements on a 3-state quantum system

**Status: Exact as mathematical characterization. The physical realization is open.**

### Target 2: Chambered flow + dominant vortex axis — which level?

A chambered flow system with a dominant vortex axis is most naturally:
- **Closer to a point in $\mathbb{CP}^2$** (a single complex line, 4 real dims) — because the vortex axis + rotation defines one complex direction

Not a complete flag (needs 2 more dims). Not a bridge point (would need torus phases too).

**More precisely:** chambered flow + dominant vortex = (flow direction: 2 dims on $S^2$) + (vortex rotation: 1–2 dims on $U(1)$ or $S^1$) = roughly 3–4 real dims. If this promotes to a complex line in a 3-component complex field: 4 dims ($\mathbb{CP}^2$ point). Still missing the second complex line (2 more dims to reach the flag).

### Target 3: "4 chambers, 1 vortex, 1 torus" — what does it determine?

| Feature | Determines | Real dims | Level |
|---|---|---|---|
| 4 chambers | A directed 4-node cycle (grammar witness) | 0 (discrete) | Downstairs loop |
| 1 vortex | At most one complex line in $\mathbb{C}^3$ | ≤4 | Partial flag ($\mathbb{CP}^2$ point) |
| 1 torus | Torus phase structure $T/\mathbb{Z}_3$ | 2 | Bridge fiber (not flag) |

**Combined:** the "4 chambers + 1 vortex + 1 torus" grammar determines:
- The downstairs loop structure (not a geometric selector)
- At most one complex line $L_1$ (4 dims) from the vortex
- The torus $t^* \in T/\mathbb{Z}_3$ (2 dims) from the toroidal phase structure

What it does NOT determine: the second complex line $L_2$ (the additional 2 dims needed to complete the flag). The heart grammar reaches for the TORUS (which it witnesses) and for ONE complex direction (from the vortex), but does not independently specify the full flag.

**The bottleneck:** the "second complex direction" $L_2$ — what physical feature of the heart (or another system) could supply the additional 2 real dims to complete the flag? This is the exact open question.

### Target 4: Heart clue — final verdict

| Assessment | Status |
|---|---|
| Selector for one complex line $L_1$ | Bridge (vortex → $L_1$, 4 dims, conditional on formal map to $\mathbb{C}^3$) |
| Selector for complete flag $F^*$ | **False** (missing $L_2$, 2 dims) |
| Selector for bridge point $M$ | **False** (missing both $L_2$ and proper torus phases) |
| Structural witness for loop grammar | **Bridge** (4-chamber directed cycle) |
| Structural witness for torus topology | **Bridge** (toroidal return field) |
| Overdetermined source | **No** (the cardiac geometry doesn't overdetermine; it underdetermines the flag) |

**Verdict: Witness, not selector.** The heart provides: structural grammar for the downstairs loop (bridge), topological analogue for the torus residue (bridge), and at most one complex direction from the vortex structure (bridge, conditional on the formal map). It is underdetermined relative to the flag: the heart clue gives at most 4 of the 6 required flag dimensions. The missing piece is the second complex direction $L_2$ — what provides the "transverse complex framing" beyond the dominant vortex axis.

---

## Summary: Where the Bottleneck Is

The flag $F^* \in \text{SU}(3)/T$ requires an ordered pair of orthogonal complex lines $(L_1, L_2)$ in a 3-component complex field. The bottleneck has two parts:

**Part 1 — $L_1$ (4 dims):** Provided by any datum that specifies a preferred complex direction in the 3-component field. Candidates: dominant vortex axis (if system has 3-component complex field), first eigenvector of a Hermitian operator, first polarization direction of a defect winding. **The vortex + rotation grammar can supply this.**

**Part 2 — $L_2$ (2 dims):** The second orthogonal complex direction, specifying which way the SECOND eigenspace points within the orthogonal complement of $L_1$. This is a point in $\mathbb{CP}^1$ (a 2-sphere). No known natural feature of the heart supplies this independently. Candidates: a second independent measurement channel; a transverse polarization framing; the second eigenvector of a Hermitian anisotropy tensor. **This is what's missing.**

**The open question:** what physical feature of a chambered-flow anisotropic system with toroidal return provides the second complex direction $L_2$, completing the flag, without automatically fixing the torus phases? The answer to this question is the flag selector.
