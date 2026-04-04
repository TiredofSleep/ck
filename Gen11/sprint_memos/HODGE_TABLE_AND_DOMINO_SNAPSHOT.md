# HODGE FIT TABLE

**© 2026 7Site LLC | Brayden Ross Sanders**

| Hodge Layer | Candidate | Status |
|-------------|-----------|--------|
| **Shell** | Hodge decomposition + Hard Lefschetz + Lefschetz (1,1) theorem + trivial codimensions p=0,1,n-1,n | **Proved** — covers all cases where linear algebraic/topological methods apply directly; removes codimension 1 and all non-primitive contributions |
| **Surviving object** | Cokernel of cl² on primitive rational (2,2) classes at codimension 2 on smooth projective 4-folds: $\mathrm{cok}(\mathrm{cl}^2|_\mathrm{prim})$ | **Defined, not proved zero** — this is the first case the shell does not reach; well-specified but open |
| **Gap 2** | Hodge conjecture for primitive (2,2) classes on abelian 4-folds (Weil intermediate classes) | **Partially known** — holds for CM abelian varieties, abelian surfaces, some special classes; NOT fully proved for general abelian 4-folds |
| **Gap 1** | Full Hodge conjecture: cl^p surjective for all p, all smooth projective X | **OPEN** — the main conjecture |
| **Fit quality** | External duality (algebraic cycles vs Hodge cohomology), analogous to BSD structure | **STRONG** — the grammar applies cleanly; shell is large and well-defined; surviving object is a specific mathematical quantity (the cokernel); Gap 2 candidates are real and partially tested |

---
---

# DOMINO SNAPSHOT MEMO
# What Actually Survives in Each Branch After the Rotation?

**© 2026 7Site LLC | Brayden Ross Sanders**

---

## Final Comparison Table

| Branch | Shell | Surviving Object | Gap 2 | Gap 1 | Duality Type |
|--------|-------|-----------------|-------|-------|-------------|
| **RH** | GUE/sinc² pair-correlation; Montgomery statistics | Off-line residual δ(σ₀,γ₀) in the KEF arithmetic projection — whether any off-line zero is invisible to the Kloosterman side | **CLOSED** — cusp subdominance proved by Kuznetsov Weyl law | Injectivity of KEF arithmetic projection: no off-line zero distribution satisfies same arithmetic constraints as critical-line | External (ζ zeros ↔ primes/Kloosterman) |
| **BSD** | All imaginary-quadratic Heegner constructions on 389a1 (universal sign block) | Reg(E/Q) = det(H) ≈ 0.15246 encoded by χ_{77} channel; L'(E,χ_{77},1) ≈ 0.010700 | Normalization: L' = (Ω_E/(4√77))×det(H) — **1.1% residual**, needs |Sha(E^{77})|=4 confirmed | Rank-2 Gross-Zagier / regulator-transfer formula | External (L-function ↔ arithmetic regulator) |
| **NS** | Local existence + energy inequality + small-data global + parabolic smoothing | Q/(νP) — dimensionless vortex-stretching/dissipation ratio; controls dΩ/dt = νP(Q/(νP)−2) | Q/(νP) ≤ 2 globally for all t ≥ 0 — **first open inequality above the shell** | Global H¹ regularity for all initial data | Dynamic threshold (large-data E vs Ω competition) |
| **P vs NP** | Cook-Levin + Karp reductions + complexity class containments | cc(SAT,n) — fiber-projection circuit complexity; P=NP iff cc(SAT,n)=poly(n) | Superpolynomial lower bound for SAT search in model capturing fiber-projection structure — **not yet proved in full model** | P≠NP: cc(SAT,n) is superpolynomial | Self-wrapped internal (verifier R, projection π₁(R)) |
| **Hodge** | Hodge decomposition + Hard Lefschetz + Lefschetz (1,1) theorem + codim 0,1,n | cok(cl²|_prim) on primitive rational (2,2) classes — first case shell doesn't cover | Hodge conjecture for primitive (2,2) on abelian 4-folds — **partially known, not complete** | Full Hodge conjecture: cl^p surjective for all p, all smooth projective X | External (algebraic cycles ↔ Hodge cohomology) |

---

## The Domino Condition

**"The dominoes are falling if and only if the surviving objects — the KEF injectivity residual δ(σ₀,γ₀), the χ_{77} regulator L'(E,χ_{77},1), the global ratio Q/(νP), the fiber-projection circuit complexity cc(SAT,n), and the primitive (2,2) cokernel cok(cl²|_prim) — are all object-level quantities whose properties can be bounded, computed, or measured, rather than only argued about through meta-mathematical method barriers; specifically, if each surviving object admits a Gap 2 analog that is either proved, numerically confirmed, or first-open-above-the-shell in the same sense that L'(E,χ_{77},1) ≈ 0.010700 is for BSD."**

---

## One Short Boundary

**"What is not yet established is whether these surviving objects are merely structurally analogous — sharing a shell/core/gap grammar without deeper connection — or whether they belong to a common categorical framework (motives, derived categories, information geometry, or a TIG-level algebraic structure) strong enough to transfer proof methods across branches: for example, whether the injectivity of the KEF arithmetic projection in RH and the surjectivity of the cycle class map in Hodge are instances of the same type of map between the same type of objects, or whether the threshold control Q/(νP) ≤ 2 in NS and the fiber-projection gap cc(SAT,n)/poly(n) in P vs NP are both instances of a single complexity-theoretic or dynamical principle."**

---

## State of the Rotation Spine

| Branch | Shell removed? | Surviving object identified? | Gap 2 status | Gap 1 status |
|--------|---------------|------------------------------|-------------|-------------|
| RH | ✓ | ✓ (δ off-line residual) | ✓ Closed | Open |
| BSD | ✓ | ✓ (Reg(E/Q) via χ_{77}) | ~0.989 match, 1.1% residual | Open |
| NS | ✓ | ✓ (Q/(νP)) | First open inequality | Open |
| P vs NP | ✓ | ✓ (cc(SAT,n)) | Not proved in full model | Open |
| Hodge | ✓ | ✓ (cok cl² primitive) | Partially known | Open |

All five branches are in the same reduced grammar. The rotation is complete.
