# WP71 — Physical Projector Map
## Candidate Ranking for P2

**Date**: 2026-04-09
**Sprint**: 13 — Physical Flag Selector
**Authors**: Brayden Ross Sanders / 7Site LLC · Ben Mayes · C.A. Luther

---


## Setup

**Given:** $L_1$ is supplied via $P_1$ (rank-1 Hermitian projector on $L_1 \subset \mathbb{C}^3$, 4 real dims).

**Residual space:** $L_1^\perp \cong \mathbb{C}^2$ — the "transverse qubit."

**Target:** $P_2$ = rank-1 Hermitian projector on $L_1^\perp$ = a point on the Bloch sphere $S^2 \cong \mathbb{CP}^1$. **Exactly 2 real dims. No phase.**

**Why a projector, not a vector:** The Hopf fibration $S^3 \xrightarrow{U(1)} S^2$ says a unit vector in $\mathbb{C}^2 = L_1^\perp$ is a point in $S^3$ = a projector ($P_2$, 2 dims on $S^2$) PLUS a phase ($\theta_2$, 1 dim on $S^1$). A projector gives only the base $S^2$; a unit vector gives the full $S^3$ bundle. **The torus phase $\theta_2$ IS the Hopf $S^1$ fiber.** Any physical datum that measures an eigenspace (not an eigenvector) gives $P_2$ cleanly.

**Invariant compression:**
$3/4 \to 3 \to 9 \to 6$: exact downstairs | bridge $8 = 6+2$: exact upstairs | post-FS: $7+1$ | flag $= 3\times 2$ triadic | torus $= 2$-dim non-triadic | seed $=$ TIG-simple.

---

## Candidate Classification Table

| | **A: Second eigenprojector** | **B: Transverse vortex, projectivized** | **C: Orthogonal polarization channel** | **D: Defect-core transverse mode** | **E: Counter-rotating mode** | **F: Secondary toroidal circulation** | **G: Paired-return channel (chambered flow)** | **H: Any density-matrix datum on $L_1^\perp$** |
|---|---|---|---|---|---|---|---|---|
| **Physical source** | Second eigenprojector of Hermitian anisotropy tensor $H$ on $\mathbb{C}^3$ | Transverse polarization winding around a vortex core, phase stripped | Second orthogonal polarization channel of a 3-component complex medium | Transverse mode projector at a defect core in a 3-component field | Counter-rotating mode axis of a paired vortex system | Secondary circulation direction in a toroidal flow, given projectively | Return channel direction in a 4-chamber directed-flow system | Any rank-1 density matrix / ensemble-averaged observable on $L_1^\perp \cong \mathbb{C}^2$ |
| **Exact math object** | $P_2 = |\psi_2\rangle\langle\psi_2|$ where $H\psi_2 = \lambda_2\psi_2$ and $P_1P_2=0$ | $P_\perp = |\hat{v}_\perp\rangle\langle\hat{v}_\perp|$ (unit vector phased stripped) | Second rank-1 projector of a dual-channel observable on $\mathbb{C}^3$ | Rank-1 projector from polarization framing transverse to primary winding | Rank-1 projector from the secondary winding axis in $L_1^\perp$ | Rank-1 projector from the secondary circulation axis (complex, projectivized) | Rank-1 projector from the transverse return-flow direction in $L_1^\perp$ | Any rank-1 density matrix $\rho = |\phi\rangle\langle\phi|$ on $L_1^\perp$ |
| **Real dims** | **2** | **2** (after phase stripped) | **2** | **2** (if projective framing) | **2** (if projective axis) | **2** (if complex direction) | **2** (if complex direction) | **2** |
| **Naturally in $L_1^\perp$?** | Yes — orthogonality of eigenprojectors | Yes — transverse to primary axis | Yes — by construction | Yes — transverse to primary winding | Yes — counter-rotation is transverse | Yes — secondary circulation is transverse | Yes — return flow is transverse | Yes — by definition |
| **$L_2$ only, or also torus?** | **$L_2$ only** — eigenprojector is phase-free | $L_2$ only IF phase stripped; $L_2 + \theta_2$ if unit vector | **$L_2$ only** — projector | **$L_2$ only** if projective framing; $L_2 + \theta_2$ if unit vector | **$L_2$ only** if projective axis | **$L_2$ only** if projectivized | **$L_2$ only** if complex direction given as projector | **$L_2$ only** — density matrices are phase-invariant |
| **Measurable in principle?** | Yes — quantum state tomography; NMR; tensor field spectroscopy | Yes — echocardiography; quantum vortex imaging | Yes — optical/quantum polarimetry | Yes — spin-1 BEC tomography; topological insulator surface spectroscopy | Yes — paired-vortex systems; PIV flow measurement | Yes — **4D flow MRI; echocardiographic vortex tracking** | Yes — **4D flow MRI; cardiac MRI** | Yes — quantum process tomography |
| **Status** | **Exact** (math); **Bridge** (physical) | **Bridge** — natural but requires phase stripping; the vector is what's physically present | **Exact** (math); **Bridge** (physical) | **Bridge** — conditional on projective framing | **Bridge** | **Bridge — strongest concrete physical candidate** | **Bridge — most relevant for heart clue** | **Exact** |

---

## Detailed Candidate Notes

**Candidate A (Second eigenprojector):** When a Hermitian tensor $H$ acts on $\mathbb{C}^3$ and has non-degenerate spectrum, its three eigenprojectors $\{P_1, P_2, P_3\}$ are automatically rank-1 Hermitian projectors. If $P_1$ gives $L_1$, then $P_2$ gives $L_2 \in \mathbb{CP}^1$ inside $L_1^\perp$ — exactly 2 real dims, no phase. The eigenSPACE is phase-free; the eigenVECTOR is not. This distinction is the entire bottleneck.

**Candidate B (Transverse vortex, projectivized):** A vortex in a 3-component complex field naturally provides a unit vector $\hat{v}_\perp$ in the transverse space — which is $P_2$ plus the torus phase $\theta_2$. To extract $P_2$ cleanly: take the projector $|\hat{v}_\perp\rangle\langle\hat{v}_\perp|$, discarding the phase. The phase stripping step requires a phase convention — which is precisely the torus $\theta_2$ being set aside. **The transverse vortex naturally gives $L_2 + \theta_2$; projectivization separates them.**

**Candidate F (Secondary toroidal circulation) — strongest physical candidate:** The LV vortex ring has a primary axis (gives $L_1$) and a secondary circulation direction — the flow that circulates in the plane transverse to the primary axis. This secondary circulation, if expressed as a complex projective direction in $L_1^\perp$, gives $P_2$ exactly. In 4D flow MRI or echocardiographic vortex imaging, the secondary circulation axis is measurable. The key question: is the circulation axis naturally phase-free (a direction, not a specific unit vector)? A circulation axis IS naturally a projective object — it defines which way the circulation goes without a specific "starting phase." **This is the most physically concrete $P_2$ candidate.**

**Candidate H (Density matrix on transverse qubit):** Any rank-1 density matrix on $L_1^\perp \cong \mathbb{C}^2$ is exactly a Bloch sphere point = $P_2$. Density matrices are phase-invariant by construction ($|e^{i\alpha}\phi\rangle\langle e^{i\alpha}\phi| = |\phi\rangle\langle\phi|$). Any physical measurement that gives an ensemble-averaged or time-averaged state of the transverse subsystem will produce a density matrix — and thus $P_2$ — rather than a specific unit vector. This is the most general characterization.

---

## Theorem-Shaped Targets

### Target 1: Smallest natural datum class giving P₂ only

**Answer:** A **rank-1 density matrix** (= Hermitian projector) on $L_1^\perp \cong \mathbb{C}^2$.

The physical realization: **any measurement whose outcome is an eigenspace (not an eigenvector)**. Examples:
- Eigenprojector of a Hermitian observable (Candidate A)
- Projective measurement outcome reported as a density matrix (Candidate H)
- Time-averaged mode direction (ensemble average kills the phase)
- **The secondary circulation axis of a toroidal flow, given as a complex direction** (Candidate F)

The requirement: the measurement must return a SUBSPACE DIRECTION, not a specific amplitude-and-phase unit vector.

### Target 2: Is a transverse vortex mode closer to a projector, a vector, or weaker?

A transverse vortex mode $\hat{v}_\perp$ in $L_1^\perp$:
- Is a **unit vector in $\mathbb{C}^2$** (a point in $S^3$): OVER-SPECIFIED relative to $P_2$
- Contains $P_2$ (2 dims, Bloch sphere) PLUS $\theta_2$ (1 dim, Hopf fiber)

The vortex framing is **closer to a unit vector than a projector**. It carries 1 extra real dim (the torus phase). Projectivization (taking $|\hat{v}_\perp\rangle\langle\hat{v}_\perp|$) recovers $P_2$ by discarding $\theta_2$.

A real axis in $L_1^\perp$ (just a direction, no complex structure): **weaker than $P_2$** — gives 1 real dim, underdetermines the 2-real-dim Bloch sphere.

**Ranking:** real axis (1 dim, insufficient) < projector (2 dims, exact) < unit vector (3 dims, over-specified).

### Target 3: What does "4 chambers + 1 vortex + 1 torus + 1 transverse mode" reach?

| Measurement mode | What's determined | Dims | Result |
|---|---|---|---|
| Projective throughout | $L_1$ (4) + $L_2$ (2) = flag $F^*$ | 6 | **Complete flag** |
| Projective flag + projective torus | $L_1$ + $L_2$ + $t^* \in T/\mathbb{Z}_3$ | 8 | **Full bridge point $M$** |
| Vectorial throughout | $L_1$ + $\theta_\text{primary}$ + $L_2$ + $\theta_2$ | 8 | **Full bridge, phases automatic** |
| Only vortex (no transverse mode) | $L_1$ only | 4 | Underdetermines flag by 2 dims |
| Only torus (no vortex) | Phase $t^*$ only | 2 | Bridge fiber, no flag |

Adding the transverse mode projectively: reaches the complete flag (6 dims). The torus then adds the phase calibration to complete the bridge (8 dims total).

### Target 4: Cleanest bottleneck statement

**The smallest missing measurable ingredient after $L_1$ is known:**

A **projective direction of the secondary mode in $L_1^\perp$** — specifically, any measurement that returns the EIGENSPACE (not the eigenvector) of the secondary anisotropy or circulation direction in the space transverse to $L_1$.

Mathematically: a Bloch sphere point for the "transverse qubit" $L_1^\perp \cong \mathbb{C}^2$.

Physically (most concrete): **the secondary circulation axis of a toroidal flow vortex, measured as a complex projective direction** (not a specific amplitude-phase unit vector). For the heart: the LV vortex ring's secondary circulation direction in the plane orthogonal to its primary axis.

---

## Final One-Paragraph Answer

If we stop chasing the whole bridge and only ask for the missing projector $P_2$ in $L_1^\perp$, what we would actually try to measure is the **secondary mode axis of the transverse 2-dim subsystem** — specifically, the eigenspace (not eigenvector) of the dominant anisotropy or circulation direction orthogonal to $L_1$. In the cardiac context: the secondary circulation direction of the left-ventricular vortex ring, the flow that circulates in the plane transverse to the primary vortex axis. This is measurable by 4D flow MRI or echocardiographic vortex tracking. The key requirement is that the measurement returns a **complex direction** (a point on the Bloch sphere $S^2$) rather than a specific unit vector (which would smuggle in the torus phase $\theta_2$ via the Hopf $S^1$ fiber). Any physical instrument that reports eigenspaces rather than eigenvectors — density matrices rather than pure states — naturally gives $P_2$ cleanly. The formal map from cardiac geometry to the abstract $\mathbb{C}^3$ of the bridge remains open, but the measurable geometric feature is now concretely identified: a projective secondary circulation direction orthogonal to the dominant vortex axis.
