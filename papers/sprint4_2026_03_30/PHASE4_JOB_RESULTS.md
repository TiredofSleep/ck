# Phase IV Job Results: Jobs 10, 11
## Base-Specific Seed Anatomy and Oracle Anatomy

*Brayden Sanders & C. A. Luther / 7Site LLC | March 2026*

---

## Job 10: Base-Specific Seed Discovery

**The structural correction: BHML residual cells are table-specific, not arithmetic.**

At b=10, the 6 BHML residual cells were identified by comparing TSML against the BHML=max(s,c) table — they are the cells where TSML and BHML happen to agree. They were found by construction, not derived from arithmetic.

**At b=14, there is no analog — because there is no constructed TSML.**

The "order-seed" in the Job 6 signature is not a property of the base b=14 arithmetic. It is a property of the specific TSML table at b=10. Other bases need their own constructed table first before the BHML residual concept applies.

**G×G cells at b=14:** Every G×G pair at b=14 has max ∈ G — the order structure within G never points back to C. There are no "BHML residual" cells of the G×G type.

**G×C cells at b=14:** Six G×C cells where max(s,c) ∈ C exist: (2,3), (2,9), (4,9), (6,9), (7,9), (8,9). These are structurally analogous to a subset of b=10's order-seed cells. However, biasing toward these at b=14 produced no TSML-like lift (0.0% biased vs 0.0% random) — because the classifier was calibrated for b=10 structure.

**The corrected statement:**
> Cross-base construction requires first building a b=14-analog of TSML — a table with its own closure grammar, one-way gate, and order-seed signature. Then and only then can a "BHML residual" be identified for that base, and seeded reduction applied.

The b=10 construction protocol is not portable as-is. It reveals a methodology, not a universal recipe.

---

## Job 11: Oracle Anatomy

**Why the oracle is a permanent basin — measured directly.**

Oracle tables (n=142), gate-strong (n=126), TSML-like (n=14) compared:

| Feature | Oracle | Gate-strong | TSML-like |
|---------|--------|------------|----------|
| Gap | **0.781** | 0.710 | 0.709 |
| Gate strength | 0.924 | **0.982** | 0.976 |
| HAR_mass | 1.000 | 1.000 | 1.000 |
| BHML residual | 0.423 | 0.402 | **1.000** |
| **G-reach from C** | **0.076** | **0.018** | **0.024** |
| HAR-spread | 0.404 | 0.412 | 0.414 |
| Non-assoc count | 278.7 | 266.5 | 253.6 |

**The key discriminator: G-reach from C.**

Oracle tables have G-reach = 0.076 — meaning 7.6% of C-operator applications land in G territory. Gate-strong and TSML-like have G-reach ~0.02 (essentially zero).

**Why the oracle is permanent:**

The oracle achieves high spectral gap (0.781 vs 0.710 for gate-strong) by using broad mass coverage — spreading probability across both C and G territory creates more mixing surface. High gap is easy to achieve this way: just let some C→G transitions happen.

The gate requires an additional hard constraint: block all C→G transitions completely. This constraint costs gap (0.781 → 0.710) while adding gate structure. The landscape naturally prefers the unconstrained version — high gap without the gate cost.

**The oracle is the "maximize mixing without constraints" attractor.** It is cheaper than the gate and achieves higher gap. Any table that satisfies the basic harmonic requirements (HAR absorbing, C sub-magma) without the extra gate constraint lands here. That's why ~40% of trajectories find it even under pure gate-weighting — the objective pushes toward gate, but the landscape's entropy favors oracle.

**TSML-like vs gate-strong:** The only remaining difference is BHML residual (1.000 vs 0.402). Gate strength and G-reach are nearly identical. HAR_mass is identical. The BHML residual is the final separator — and its absence is not penalized by the gate-weighted objective. Only intentional seeding toward BHML pre-alignment produces it.

---

## The Complete Picture: Four-Phase Summary

| Phase | Key finding |
|-------|------------|
| **I** | Objective determines attractor; BHML residual is the output discriminator |
| **II** | TSML-like is a real basin (stable); phase transition at w=0.1; order seed is the input predictor |
| **III** | 15.8x construction lift with seed biasing; oracle is permanent; no new basin at high w |
| **IV** | BHML residual is table-specific (not base-specific); oracle is permanent because C→G freedom is cheaper than gate constraint |

**The deep structural sentence:**

> TSML-like requires order-seed completion, not just exclusion pressure. The oracle is what happens when the system optimizes mixing freely. Gate-strong is what happens when exclusion is learned. TSML-like is what happens when exclusion and support also inherit the right order seed — and that seed is a property of the specific constructed table, not of the arithmetic base alone.

---

*(c) 2026 Brayden Sanders & C. A. Luther / 7Site LLC | Gen10.16, commit 271e0f8 | DOI: 10.5281/zenodo.18852047*
