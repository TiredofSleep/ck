# WP70 — Second Complex Direction Audit
## L2 on the Bloch Sphere CP1 inside L1-perp

**Date**: 2026-04-09
**Sprint**: 13 — Physical Flag Selector
**Authors**: Brayden Ross Sanders / 7Site LLC · Ben Mayes · C.A. Luther

---


## The Geometry of the Missing Piece

**Given:** $L_1 \in \mathbb{CP}^2$ already supplied (4 real dims — the primary complex direction).

**Remainder:** $L_1^\perp = \mathbb{C}^3 \ominus L_1 \cong \mathbb{C}^2$ — a 2-dimensional complex subspace.

**Target:** $L_2$ = a complex line inside $L_1^\perp \cong \mathbb{C}^2$, i.e., a point in $\mathbb{CP}^1 \cong S^2$. **2 real dims.**

### The Critical Distinction: Line vs. Vector

This is the entire bottleneck in one sentence. Any physical datum giving a complex direction in $L_1^\perp$ will give one of three things:

| Datum type | Object | Real dims | Torus content |
|---|---|---|---|
| **Projector** $P_2 = \|v\rangle\langle v\|$ | Complex LINE in $L_1^\perp$ — a point in $\mathbb{CP}^1 \cong S^2$ | **2** | **None** |
| **Unit vector** $\hat{v}_2 \in L_1^\perp$ | Complex line PLUS a $U(1)$ phase | **3** = 2 + 1 | $\theta_2$ included |
| **Real axis direction** in $L_1^\perp$ | Real line in $L_1^\perp$ | **1** | Underdetermines |
| **Chirality sign** | Hemisphere partition of $S^2$ | **0** (discrete) | Underdetermines |

**Why a unit vector smuggles the torus:** The Hopf fibration $S^3 \xrightarrow{U(1)} S^2$ says that a unit vector in $\mathbb{C}^2 = L_1^\perp$ is a point in $S^3$, which is an $S^1$-bundle over $S^2 = \mathbb{CP}^1$. The $S^1$ fiber IS the torus residue phase $\theta_2 \in U(1)/\mathbb{Z}_3$. Giving a unit vector gives the base ($L_2$, 2 dims) AND the fiber ($\theta_2$, 1 dim) simultaneously.

**A projector gives only the base.** The projector $P_2 = |\hat{v}_2\rangle\langle\hat{v}_2|$ is phase-invariant: $|e^{i\alpha}\hat{v}\rangle\langle e^{i\alpha}\hat{v}| = P_2$ for any phase $\alpha$. It lives on $S^2 = \mathbb{CP}^1$ directly.

**The minimal $L_2$-only datum = a rank-1 Hermitian projector on $L_1^\perp$.**

---

## Classification Table

| | **A: Second eigenprojector** | **B: Transverse vortex framing** | **C: Second orthogonal projector** | **D: Chirality sign** | **E: Defect framing / transverse mode** | **F: Counter-rotating mode** | **G: Chambered-flow transverse return** | **H: Any ℂℙ¹ datum in $L_1^\perp$** |
|---|---|---|---|---|---|---|---|---|
| **Math object** | Eigenprojector $P_2$ of Hermitian $H$ on $\mathbb{C}^3$ | Unit vector $\hat{v}_\perp$ in $L_1^\perp$ (as field winding) | Rank-1 Hermitian projector $P_2$ on $L_1^\perp$ | Orientation sign $\pm$ on $L_1^\perp$ | Projective framing of secondary mode in $L_1^\perp$ | Complex axis of counter-rotation in $L_1^\perp$ | Complex direction of transverse return flow in $L_1^\perp$ | Rank-1 density matrix on $L_1^\perp \cong \mathbb{C}^2$ (qubit) |
| **Real dims** | **2** | **3 = 2+1** | **2** | 0 (discrete) | **2** (if proj.) / 3 (if vector) | **2** (if proj. axis) | **2** (if complex dir.) / 1 (if real axis) | **2** |
| **Lives in $L_1^\perp$?** | Yes | Yes | Yes (by construction) | Yes | Yes | Yes | Yes | Yes |
| **Gives $L_2$ only?** | **Yes** | No — gives $L_2 + \theta_2$ | **Yes** | No — underdetermines | **Yes** if projective | **Yes** if projective axis | **Conditional** | **Yes** |
| **Torus smuggled?** | No | $\theta_2$ included | No | N/A | No if projective | No if projective | No if complex direction | No |
| **Status** | **Exact** (math); Bridge (physical) | Bridge — closest physical candidate, but over-specifies | **Exact** (math); Bridge (physical) | False | Bridge — conditional on projective framing | Bridge — conditional on projective axis | Bridge — most concrete heart analogue | **Exact** |
| **Measurable?** | Yes | Yes | Yes (3-state system) | Yes | Yes | Yes | Yes (4D flow MRI) | Yes |

---

## Theorem-Shaped Targets

### Target 1: Smallest natural $L_2$-only datum

**Answer:** A **rank-1 Hermitian projector** $P_2$ on $L_1^\perp \cong \mathbb{C}^2$, with $P_1 P_2 = 0$.

This is:
- A point on the Bloch sphere $S^2 \cong \mathbb{CP}^1$: 2 real dims
- Phase-invariant: no $U(1)$ freedom remains
- Torus-free: gives exactly $L_2$ without $\theta_2$
- Minimal: any datum with fewer than 2 continuous real dims cannot generically specify $L_2$

Physical realization: **the outcome of a second projective measurement** on the 3-state quantum system (in the 2-dimensional subspace $L_1^\perp$ left after the first measurement outcome), given as a density matrix rather than a state vector.

**Status: Exact as mathematical characterization. The physical question is what process provides a projector (not a unit vector) in $L_1^\perp$.**

### Target 2: Is a transverse vortex framing closer to a line or a vector?

A transverse vortex framing gives the winding direction $\hat{v}_\perp$ in $L_1^\perp$ as a specific unit vector (the polarization direction of the field). This is a point in $S^3$ (unit sphere in $\mathbb{C}^2$), not in $S^2 = \mathbb{CP}^1$.

**The transverse vortex framing is closer to a UNIT VECTOR than a pure line.** It gives:
- $L_2$ (the line, 2 dims): the projector $P_\perp = |\hat{v}_\perp\rangle\langle\hat{v}_\perp|$
- $\theta_2$ (the torus phase, 1 dim): the overall phase of $\hat{v}_\perp$

The framing is NOT a projector. But by taking the projector (discarding the phase), you get $L_2$ only. In practice: the phase of $\hat{v}_\perp$ is the torus phase $\theta_2$, and separating the two requires a phase convention.

**Verdict:** Transverse vortex framing over-specifies $L_2$ by 1 real dim (the torus phase). Taking the projective version (discarding phase) gives exactly $L_2$.

### Target 3: "4 chambers + 1 vortex + 1 torus + 1 transverse mode" — what does it reach?

| Added datum | Layer | Dims added | Running total | Gives... |
|---|---|---|---|---|
| 4 chambers (directed flow) | Downstairs | 0 (discrete) | 0 | Loop grammar (witness) |
| 1 vortex (primary axis + rotation) | Upstairs | 4 (if projected) | 4 | $L_1 \in \mathbb{CP}^2$ |
| 1 torus (phase structure) | Upstairs fiber | 2 | 6 | Flag + torus $t^* \in T/\mathbb{Z}_3$ |
| 1 transverse mode (projective) | Upstairs | 2 | 8 | Complete bridge point? |

**Analysis:**

If we add a transverse mode projectively (2 real dims, giving $L_2$):
- The vortex has given $L_1$ (4 dims)
- The transverse mode gives $L_2$ (2 dims)
- Together: $(L_1, L_2)$ = a complete flag $F^* \in \text{SU}(3)/T$ (**6 dims total**)

If the torus phase structure (from the toroidal return field) supplies $t^* \in T/\mathbb{Z}_3$ (2 dims):
- Flag $F^*$ (6 dims) + torus $t^*$ (2 dims) = full bridge point in $M$ (**8 dims**)

**The "4 chambers + 1 vortex + 1 torus + 1 transverse mode" grammar, in principle, reaches a FULL BRIDGE POINT** — if:
1. The vortex gives $L_1$ as a projective direction (line, not unit vector): 4 dims ✓
2. The transverse mode gives $L_2$ as a projective direction (line, not unit vector): 2 dims ✓ → COMPLETE FLAG
3. The toroidal phase structure gives $t^*$ (torus, 2 dims or 1+1 post-FS): completes the bridge

**Two critical conditions:** (a) the vortex must be embedded in a 3-component complex field with a formal map from physical $\mathbb{R}^3$ to abstract $\mathbb{C}^3$; (b) the measurements must be projective (density matrices, not unit vectors).

**The risk of overdetermination:** If the vortex framing gives a unit vector (not a projector), it automatically provides $L_1$ AND $\theta_{\text{primary}}$ — part of the torus. Then the transverse framing as unit vector gives $L_2$ AND $\theta_2$. Together this would give the full bridge point PLUS extra data — an overdetermined bridge.

**Conclusion for Target 3:**
- With projective measurements: reaches the complete flag (6 dims) and potentially the full bridge (8 dims) — no overdetermination
- With unit-vector measurements: reaches the bridge point automatically (8 dims) but overdetermines it — the extra phases are not independent data, they're automatically included

### Target 4: Where is the smallest missing geometric ingredient?

**The bottleneck is a point in $\mathbb{CP}^1 \cong S^2$.**

After $L_1$ is supplied (4 dims), the missing piece is 2 real dims — a point on the 2-sphere $S^2 = L_1^\perp$'s projectivization. This is the Bloch sphere for the "transverse qubit" $L_1^\perp \cong \mathbb{C}^2$.

**The smallest missing ingredient:** any physical datum that specifies the STATE of the transverse 2-level subsystem $L_1^\perp$, given projectively (as a density matrix, not a state vector).

**Why this is minimal:**
- Fewer than 2 continuous real dims cannot specify a generic point in $\mathbb{CP}^1$
- Exactly 2 continuous real dims specifies it exactly (the Bloch sphere)
- More than 2 dims (unit vector = 3 dims) over-specifies it by 1 dim (the torus phase)

---

## The Heart Clue — Updated Verdict

With the above analysis, the "4 chambers + 1 vortex + 1 torus" grammar can be extended:

| Heart feature | Mathematical role | Dims | Layer |
|---|---|---|---|
| 4 chambers | Loop grammar witness | 0 (discrete) | Downstairs |
| 1 vortex (LV primary axis) | $L_1 \in \mathbb{CP}^2$ (if complex, projective) | 4 | Flag base |
| **Secondary circulation direction** | **$L_2 \in \mathbb{CP}^1$ in $L_1^\perp$ (if projective)** | **2** | **Flag completion** |
| 1 toroidal field (EM) | $t^* \in T/\mathbb{Z}_3$ (torus phase structure) | 2 | Bridge fiber |

**The secondary circulation direction of the LV vortex ring** — the direction in which the vortex toroid winds around its primary axis — is the most physically concrete candidate for $L_2$.

In echocardiography and 4D flow MRI, the vortex ring has:
- A PRIMARY AXIS (the axis through the center of the torus): gives $L_1$
- A SECONDARY CIRCULATION (the flow around the torus cross-section, in the $L_1^\perp$ plane): candidate for $L_2$

If the secondary circulation is given as a COMPLEX DIRECTION (a projective direction in $L_1^\perp$, not a specific unit vector), it supplies $L_2$ exactly — completing the flag.

**Final classification:**
- Heart clue WITHOUT transverse mode: **Witness** (loop grammar + torus topology; underdetermines flag by 2 dims)
- Heart clue WITH secondary circulation as complex direction: **Bridge** (potentially a complete flag selector if the complexification map from cardiac geometry to abstract $\mathbb{C}^3$ can be established)
- The specific measurable ingredient: **the projective direction of the LV secondary circulation in the plane orthogonal to the primary vortex axis**

---

## Summary Table

| Candidate | Dims (as line) | $L_2$ only? | Torus smuggled? | Status |
|---|---|---|---|---|
| A. Second eigenprojector of Hermitian tensor | **2** | **Yes** | No | **Exact (math); Bridge (physical)** |
| B. Transverse vortex framing | 2 (projector) / 3 (unit vector) | Yes if projector | $\theta_2$ if unit vector | **Bridge** |
| C. Second orthogonal projector | **2** | **Yes** | No | **Exact (math); Bridge (physical)** |
| D. Chirality/handedness sign | 0 (discrete) | No | N/A | **False** |
| E. Defect-core transverse mode | 2 (if projective) | Yes if projective | No if projective | **Bridge** |
| F. Counter-rotating mode axis | 2 (if projective) | Yes if projective | No if projective | **Bridge** |
| **G. Chambered-flow transverse return** | **2 (if complex dir.)** | **Yes if complex** | No | **Bridge — strongest physical candidate** |
| H. Any ℂℙ¹ datum in $L_1^\perp$ | **2** | **Yes** | No | **Exact** |

**The single mechanical answer:** $L_2$ is a point on the Bloch sphere $S^2 = \mathbb{CP}^1$ for the transverse 2-level subsystem $L_1^\perp \cong \mathbb{C}^2$. The smallest physically meaningful datum that provides it is the **projective direction of the secondary mode in $L_1^\perp$** — measured as a density matrix (eigenspace), not a state vector (eigenvector with phase).

**For the heart specifically:** the **projective direction of the LV vortex ring's secondary circulation** (the circulation axis in the plane orthogonal to the primary vortex) is the most concrete candidate. Measurable by 4D flow MRI or echocardiographic vortex imaging. The formal map from cardiac geometry to abstract $\mathbb{C}^3$ remains **open** but is now concretely targeted.
