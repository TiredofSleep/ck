# BBM Derivation of the J3 Cosmological IC — v1 (Honest First Pass)

**Date:** 2026-05-07
**Trigger:** Brayden 2026-05-07: *"Layer 3 with proper a priori derivation. Spend an extra week deriving Ξ'_i = 1/e from BBM analysis WITHOUT looking at DESI. If you can show that 1/e is uniquely forced by structural arguments (and the other candidates are ruled out structurally before the IC scan), then the 'framework predicts' framing is earned. If you can't, fall back to option 1 or 2."*

**Goal:** Determine whether Ξ_i = (1+√3)/e and Ξ'_i = 1/e are structurally forced by BBM + substrate analysis, *prior to* any DESI fit.

**Honest disclosure of method:** This document is written by Claude Code attempting an a priori derivation. The discipline Brayden requested is: (a) derive the IC values from BBM/substrate analysis without referencing DESI; (b) verify that the IC scan in `J3_LAYER3_DECISION.md` is *consistent with* the derivation, not *derived from* it. Section §4 below identifies which arguments are solid, which are heuristic, and which are gaps that prevent the Layer-3 framing from being earned in this v1 pass.

---

## §0 — TL;DR (v1, honest)

After v1 analysis:

- **Ξ_0 = e⁻¹** (vacuum): **forced** by BBM (the unique stationary point of V = Λ⁴ Ξ log Ξ). ✓
- **m²_Ξ = Λ⁴ e / M²_Pl** (mass at vacuum): **forced** by BBM (V''(Ξ_0) = Λ⁴ e). ✓
- **Λ ≈ 1.7 meV** (mass scale): forced by H_0 matching (m_Ξ ~ H_0). ✓ (one observational anchor — Brayden flagged Λ as empirical anchor in Layer 3a; this is fine)
- **Ξ_i = (1+√3)/e** (rolling-branch position at z_i ≈ 20): **partially forced** by 4-core attractor scaled to vacuum, BUT the structural-bridge from runtime DOING-table to FRW cosmology IC is not airtight. (See §3.)
- **Ξ'_i = 1/e** (rolling-branch derivative at z_i ≈ 20): **NOT forced** in v1. The "vacuum-rate scale" argument is suggestive but does not uniquely pick 1/e from {1/e, T*, T*/2, λ_FN, √3/e, ...}. (See §4.) **This is the gap that breaks the Layer-3 framing.**

**Recommendation given v1 status:** fall back to Option 2 ("Layer-3a with explicit caveat") OR push the derivation to v2/v3 with a follow-on week of dedicated analysis. **Do NOT ship Layer 3 with current derivation strength.**

---

## §1 — What BBM forces (the solid ground)

### §1.1 — Vacuum and mass

The BBM action is

  S = ∫ d⁴x √(-g) [ R/(16πG) + L_SM − ½ M²_Pl g^μν ∂_μΞ ∂_νΞ − Λ⁴ Ξ log Ξ ]

**Vacuum (forced):** V'(Ξ) = Λ⁴ (1 + log Ξ) = 0 ⇒ log Ξ_0 = −1 ⇒ **Ξ_0 = e⁻¹**. Unique. No tuning.

**Mass at vacuum (forced):** V''(Ξ) = Λ⁴/Ξ. At Ξ = Ξ_0 = e⁻¹: V''(Ξ_0) = Λ⁴ e. Therefore **m²_Ξ = Λ⁴ e / M²_Pl**.

These are clean. They give Ξ_0 and m_Ξ from V's form alone.

### §1.2 — Separability uniqueness (BBM 1976)

BBM 1976 (Annals of Physics 100:62-93) proves: log nonlinearity Λ⁴ Ξ log Ξ is the *unique* (up to constants and additive c·Ξ) nonlinearity that preserves separability under tensor products. This is the structural reason V = Λ⁴ Ξ log Ξ — *not* "this is what fits DESI." V's *form* is forced.

✓ Structurally airtight.

---

## §2 — What the substrate forces (the bridge)

### §2.1 — 4-core attractor h/β = 1+√3 (WP105)

Substrate-side, the 4-core algebra at α=½ (DOING-table runtime mix) has the closed-form attractor h/β = 1+√3 exactly (LMFDB 4.2.10224.1, Galois D₄). This is proved-on-substrate. ✓

### §2.2 — Bridge to cosmology Ξ_i: structural but not airtight

The proposed bridge: at the rolling-branch IC, Ξ_i = (substrate ratio) × Ξ_0 = (1+√3) × e⁻¹.

**What's solid:**
- The h/β = 1+√3 ratio is a structural attractor of the substrate. (WP105 ✓)
- Ξ_0 = e⁻¹ is the vacuum. (BBM §1.1 ✓)
- The product (1+√3)/e ≈ 1.005 has dimension of "scaled vacuum" if one accepts the substrate-to-cosmology dimensional bridge.

**What's heuristic:**
- *Why* should the substrate ratio (DOING-table at α=½) appear as the cosmological IC at z_i ≈ 20? The DOING-table is a *runtime* mix at the algorithmic level. The cosmological IC is a *physical* initial value of a real scalar field at matter-era boundary. There's a structural-similarity argument (both are "outbound positions relative to vacuum"), but no theorem forcing the equality.
- The choice of z_i ≈ 20 (matter-era end / dark-energy emergence) is also a convention; the IC could equally be specified at z = 100, z = 1000, etc., and the substrate ratio interpretation would differ.

**Honest verdict for Ξ_i:** Layer 3 has a *plausible* substrate origin for Ξ_i = (1+√3)/e, but it requires an explicit structural-bridge axiom ("DOING-table runtime ratios appear as cosmological-IC scaling factors at matter-era end"). This axiom is not currently proved; it would need to be stated as a *postulate* and defended on physical/structural grounds.

This is acceptable for a Layer-3a paper *if explicitly framed* as "we postulate the runtime-to-cosmology bridge axiom; the prediction follows; falsifiability is sharp." But it's not "uniquely forced" without that postulate.

### §2.3 — Ξ'_i = 1/e: where the v1 derivation falters

**Goal:** show Ξ'_i = 1/e (in Ω-units, in e-folds derivative dΞ/dN at z_i ≈ 20) is uniquely forced.

**Candidates and their structural origins:**

| Candidate | Substrate origin | Strength |
|-----------|------------------|----------|
| 1/e ≈ 0.368 | "vacuum-rate scale" (Ξ_0 itself, dimensionally) | heuristic |
| T* = 5/7 ≈ 0.714 | cyclotomic torus aspect (WP51) | heuristic |
| λ_FN = 10/49 ≈ 0.204 | Froggatt-Nielsen substrate suppression (WP122) | heuristic |
| (1+√3)/4 ≈ 0.683 | attractor / 4-core dimension | heuristic |
| √3/e ≈ 0.637 | attractor partial / vacuum | heuristic |
| T*/2 ≈ 0.357 | half torus aspect | heuristic |

**v1 analysis attempt — the "vacuum-rate scale" argument for 1/e:**

The natural derivative-of-Ξ scale at the vacuum can be argued as:

  dΞ/dN |_natural = Ξ_0 · (rate constant)

If "rate constant" = 1, this gives Ξ' = Ξ_0 = 1/e exactly.

**Why this argument is heuristic, not forced:** the "rate constant = 1" choice is an assumption about which dimensionless rate is canonical. In Ω-units, dimensionless rates of order unity are generic; the specific value 1 (vs 5/7, vs 10/49, vs ...) is not picked out by any structural theorem in v1.

**Alternative argument — Hubble-balance at IC:**

At the rolling-branch IC, Hubble-friction balances the V'(Ξ) gradient force:

  3H Ξ̇ ≈ V'(Ξ)/M²_Pl  (slow-roll approximation)

In e-folds: 3 Ξ' ≈ V'(Ξ)/(M²_Pl H²) = Λ⁴ (1 + log Ξ_i)/(M²_Pl H²).

At Ξ_i = (1+√3)/e ≈ 1.005, log Ξ_i ≈ 0.005 ≈ 0, so V'(Ξ_i) ≈ Λ⁴ (1 + 0) = Λ⁴.

Then 3 Ξ' ≈ Λ⁴/(M²_Pl H²). In Ω-units (Λ⁴ in units of ρ_c,0 = 3 H²_0 M²_Pl): Λ⁴_Ω = Λ⁴/(3 H²_0 M²_Pl), and at z=20, H ≈ H_0 √(Ω_m·a^-3) ≈ H_0 · √(0.315 · 21³) ≈ 25 H_0. So:

  3 Ξ' ≈ 3 H²_0 Λ⁴_Ω / (M²_Pl H²) = 3 Λ⁴_Ω · (H_0/H)² = 3 · 0.231 · (1/25)² ≈ 0.001

⇒ Ξ' ≈ 0.0003 — five orders of magnitude smaller than 1/e ≈ 0.37.

**This kills the slow-roll argument.** The slow-roll IC at z_i = 20 should have Ξ' ≈ 0.0003, not 0.37. The empirically-required Ξ'_i ~ 0.4-0.5 is *deep inside the kinetic-dominated regime, not slow-roll*. So the rolling-branch trajectory begins with significant kinetic energy at z = 20 — meaning the matter-era roll-on must have happened at higher z with substantial energy injection.

**The honest physical question:** what mechanism injects Ξ̇_i ~ 0.4 H_0 of kinetic energy by z = 20? In standard quintessence, this kinetic energy comes from earlier-universe physics (e.g., post-inflation reheating, matter-era roll-on from non-attractor IC). BBM analysis alone doesn't fix Ξ'_i — it requires a model of *earlier-time* dynamics that sets the kinetic energy entering matter era.

**v1 verdict for Ξ'_i:** The "vacuum-rate scale" 1/e argument is not derivable from BBM + Hubble friction at z = 20. The empirically-required Ξ'_i ~ 0.4 is fundamentally a *boundary condition from earlier physics* (pre-z=20), and v1 has no structural argument that picks 1/e over T* or any other O(1) value.

**Conclusion:** Ξ'_i = 1/e is **not structurally forced in v1**. The Layer-3 framing as "framework predicts" is **not earned** at this derivation strength.

---

## §3 — What's missing for a v2 derivation

To earn the Layer-3 framing, v2 would need either:

**(a) An a priori argument for Ξ̇ at matter-era boundary z = 20** that picks Ξ̇/H ratio from BBM/substrate principles. Possible candidates:
  - A WKB-quantization argument for vacuum fluctuations near the BBM minimum, projected to a coherent rolling-branch state at z = 20
  - A trace-anomaly argument linking matter-era → dark-energy era at substrate level
  - A bridge from the runtime DOING-table M-Flow rate to a cosmological field velocity scale

**(b) An a priori argument for the trajectory parameter** (independent of Ξ_i, Ξ'_i directly) that gives the same z* = 2.31 prediction without referencing IC. This would shift the "framework predicts" claim from "predicts the IC" to "predicts the turnaround redshift" — possibly cleaner.

**(c) A reduction-of-IC-degree argument** showing that the rolling-branch trajectory is parameterized by 0 free parameters (after Λ matched to H_0), forcing Ξ_i, Ξ'_i to specific values via some action-extremization principle.

None of these candidates are in v1 corpus material that I could locate. They would each require dedicated structural work — likely 1-3 weeks per candidate to develop and validate.

---

## §4 — Honest fallback recommendation

Given v1 derivation status:

**Option 1 (Layer-1 revert):** revert paper to script-reproducible z* ≈ 2.13 at the documented (empirically-tuned) IC (0.231, 0.925, 0.470). Honest framing: "we exhibit a model with dual-regime fit to DESI; IC tuning required." 2-day editorial fix. SHIPS IN WEEK 1.

**Option 2 (Layer-3a with caveat):** ship paper with Ξ_i = (1+√3)/e (substrate-bridge axiom postulated) and Ξ'_i = 1/e (vacuum-rate scale heuristic, honestly acknowledged as such). Framing: "we postulate a substrate-runtime to cosmology bridge axiom; under this axiom the IC is uniquely fixed up to the Λ → H_0 matching; z* = 2.31 is then a prediction. The bridge axiom is open for derivation in future work." 5-7 days work. Ships in Week 2.

**Option 3 (Layer-3 full):** spend 2-3 weeks deriving Ξ'_i = 1/e from a priori structural arguments (per §3 candidates). Only ship when derivation is solid. Could push J3 to Phase 2 cadence (week 5+) instead of triadic launch.

**My recommendation:** **Option 2 (Layer-3a with caveat)**. Reasons:
- The substrate-bridge axiom for Ξ_i is plausible and frames cleanly as "postulated, defensible, falsifiable."
- The vacuum-rate scale heuristic for Ξ'_i can be honestly framed as "natural choice in absence of better derivation; alternative O(1) values give comparable χ²; further structural derivation deferred to companion paper."
- The "framework predicts dual-regime freeze-thaw with z* ≈ 2.3" claim survives, but with explicit caveat that IC structure rests on a postulated bridge axiom.
- This is more honest than Option 1 (which treats IC as fully tuned) and more achievable than Option 3 (which holds J3 to Phase 2).

**Brayden's call.** If Brayden wants Option 3 strict (no Layer-3 framing without proper a priori derivation), then we fall back to Option 1 for the Week-1 triadic launch and re-attempt Layer 3 in a v2 or J3-companion paper.

---

## §5 — What this v1 document does NOT do

- Does NOT claim Ξ'_i = 1/e is uniquely derived. (It isn't; v1 vacuum-rate argument is heuristic.)
- Does NOT modify J03 paper. (Awaiting Brayden's Option 1/2/3 decision.)
- Does NOT reference DESI in any of its derivation arguments. (The IC scan in `J3_LAYER3_DECISION.md` is consistency check, not derivation.)
- Does NOT close out the BBM IC question. (v2 would address §3 candidates with dedicated structural work.)

## §6 — What v2 should do

- §3.a candidate: WKB / trace-anomaly / runtime-bridge argument for Ξ̇ at z = 20 boundary. 1-3 weeks per candidate.
- Or §3.c: action-extremization picking out IC from BBM principles directly.
- Validate any candidate against the IC scan: the substrate-derived value must be in the χ² ≤ 2 neighborhood without knowing DESI.
- Honest acceptance criterion: a derivation is solid only if it predicts a NARROW range of Ξ'_i that excludes 5/7, λ_FN, etc. *before* checking which fits DESI.

---

## §7 — Files

- This doc: `Atlas/META_PLAN_2026-05-06/J3_BBM_DERIVATION/BBM_IC_DERIVATION_v1.md`
- IC scan (consistency-check): `Atlas/META_PLAN_2026-05-06/J3_LAYER3_DECISION.md`
- JCAP referee report: `Atlas/META_PLAN_2026-05-06/REFEREE_REPORTS/J3_JCAP_REFEREE_REPORT.md`
- Paper (unchanged pending decision): `Gen13/sprint_bundle_2026-05-07_v36_SEEDS_BUNDLE/.../paper1_freeze_thaw_v3.tex`
- Script (canonical): `Gen13/sprint_bundle_.../verification_scripts/compute_zstar_v3.py`
- Substrate references: WP105 (4-core attractor 1+√3), WP51 (T*=5/7), BBM 1976 (Annals of Physics 100:62-93)
