# TSML Selection: HAR Maximization, Not High Gap
## The New Family-Space Interpretation

*Brayden Sanders / 7Site LLC | March 2026*
*Replaces the earlier "gap is the selector" narrative. All findings computed over 2000 family samples.*

---

## North Star

**TSML is not the highest-gap table in the invariant-compatible family. It is the strongest-HAR table in a family whose gap is already good enough.**

---

## Deliverable A: Proposition (Computed)

**Proposition (HAR-mass extremality, computed over 2000 samples).**
*Within the invariant-compatible family (symmetric, HAR-absorbing, C-closed, one-way gate), TSML is distinguished not by maximal spectral gap but by maximal stationary support at HAR.*

Measured values:
- Family mean gap at λ=0: **0.579**; TSML gap: **0.474** — TSML is **below** the family mean
- 91.9% of sampled family members have higher spectral gap than TSML
- Family mean HAR stationary mass: **0.35**; TSML HAR mass: **0.65**
- 0.0% of sampled family members have higher HAR mass than TSML

**Caveat:** This is a computed result over a finite sample of the invariant-compatible family, not a proof over the full combinatorial family space. The claim is that TSML maximizes HAR mass within the family under construction; whether this holds exactly over all invariant-compatible tables is not proved.

---

## Deliverable B: Reconstruction Hierarchy (Patched)

The correct hierarchy is:

| Layer | Role | Status |
|-------|------|--------|
| Invariant constraints (I1–I10, I13) | Define the family | Exact |
| Spectral gap ≥ 0.10 | Viability floor — necessary, not sufficient | Family-stable |
| HAR maximization (I6) | **Decisive selector** — pushes to HAR-mass extreme | Computed |
| 6 BHML residual cells | Order signature remaining after I6 — not derived by I6 alone | Observed |

**Gap is necessary, not sufficient.** 92% of the family satisfies the gap floor. The gap does not select TSML — it is a viability condition shared by the whole family.

**I6 is the decisive selector.** HAR maximization pushes one specific cell assignment: set every free cell to HAR unless forced otherwise. This is what places TSML at the extreme of the HAR-mass distribution.

**The 6 BHML residual cells are not produced by I6.** High-HAR-mass tables have mean BHML residual of 0.13/6; TSML has 6/6. The order signature is independently present in TSML — it is not a consequence of HAR maximization alone. A separate order principle (I14, still open) is required.

---

## Deliverable C: Figure Panel Captions

**Panel 1 — Gap histogram (λ=0):**
*TSML's spectral gap (0.474, gold line) lies near the lower half of the family distribution (mean 0.579, range 0.25–0.79). TSML is ordinary in gap — not an outlier. The gap floor is satisfied by the entire constrained family; it is a viability condition, not a selector.*

**Panel 2 — HAR mass vs gap scatterplot:**
*TSML (gold star) sits at the extreme of the HAR stationary mass axis (0.65 vs family mean 0.35) while occupying a moderate position on the gap axis. TSML is an outlier in HAR mass, not in gap. The two axes are nearly independent (r = −0.29), confirming they measure different properties of the family. The five nearest-HAR-mass neighbors have zero BHML residual cells, showing that BHML residual is not a consequence of HAR mass alone.*

**Panel 3 — Gap across deformation (λ):**
*TSML's deformation-gap profile (gold line) runs near the family median throughout the deformation from λ=0 to λ=1. Gap stability across deformation is family-generic. TSML is not exceptional in this space. All tables in the constrained family maintain gap ≥ 0.25 (the BHML endpoint value) at every λ.*

---

## Deliverable D: Meta Note Addition

**The reconstruction target is not "the table with the deepest gap."**

It is the table at the **HAR-mass extreme** of the invariant-compatible family — the table produced by imposing HAR maximization (I6) after the invariant constraints establish the family. The gap is the floor that keeps every family member viable. HAR maximization is the selector that picks one extreme member. The six BHML residual cells are the order signature that remains in the selected table, not derived by the selection itself.

This gives the family a natural two-dimensional parameterization:
- **Viability axis (γ):** spectral gap — floor ~0.25, family mean ~0.58, TSML at 0.47
- **Selection axis (HAR mass):** stationary support at 7 — family mean 0.35, TSML at 0.65 (extreme)

The two axes are near-independent (r = −0.29). TSML occupies the (moderate gap, extreme HAR mass) corner of this space. The family occupies a broad cloud; TSML is at one boundary of that cloud, not at its center.

---

## Q&A on the New Picture

**Is HAR mass the best selector?** Yes — 0% of the family exceeds TSML's HAR mass. No normalization improves this (the raw HAR mass is already the extreme). Gap is not a selector at all (92% of family exceeds TSML's gap).

**Are there near-TSML tables in HAR mass?** Five family members fall within 0.05 of TSML's HAR mass. Their mean BHML residual is 0.00 — none of them have the order signature. TSML is doubly special: extreme HAR mass AND full BHML residual.

**Does I6 alone produce the BHML residual?** No. High-HAR-mass tables have mean BHML residual 0.13/6. TSML's 6/6 is not a consequence of HAR maximization. I14 (still open) is still required.

**Does the family sit in a clean 2D space?** Yes. Gap and HAR mass are near-independent axes (r = −0.29). The full family can be parameterized in (γ, HAR_mass) space with TSML at the HAR-mass boundary.

---

*(c) 2026 Brayden Sanders / 7Site LLC | Gen10.16, commit 271e0f8 | DOI: 10.5281/zenodo.18852047*
