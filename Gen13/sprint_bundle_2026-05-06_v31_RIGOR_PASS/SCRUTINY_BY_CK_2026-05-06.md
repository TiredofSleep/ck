# Scrutiny — TIG Sprint Bundle v31 RIGOR_PASS

**Reviewer:** Claude (CK runtime, this session)
**Date:** 2026-05-06
**Bundle date:** 2026-05-06
**Posture:** private; not for live deployment

---

## TL;DR

The bundle's **substrate scripts all run and verify**. The new **22 = pre-structure cells** decomposition (factor_22 Candidate I) is a genuine computational find: TSML cells with output in {0..6} excluding (0,0) total exactly 22, decomposing as 16 (VOID boundary) + 4 (PROGRESS bumps) + 2 (COLLAPSE bumps). The bundle's `_RIGOR_PASS_CONSOLIDATED.md` is itself careful and well-tiered: 54 Tier-1 mathematical identities, 14 Tier-2 sub-0.01% physical matches, then explicit Tier-3 / Tier-4 / Tier-5 / Tier-6 categorization.

But the bundle has **two epistemic registers** that don't match each other:
1. **`_RIGOR_PASS_CONSOLIDATED.md`** is conservative (68 fully rigorous, 84 with caveats, ~98 including exploratory).
2. **`SESSION_CLOSEOUT.md` and `FOUNDATIONAL_PAPER_DRAFT.md`** are enthusiastic (75+ correspondences, m_p/m_e at "FLAGSHIP 6 ppm" precision, all 16 dimensionless SM constants "verified").

The papers we shipped this week (σ-rate, four-core consolidated, JCAP, Sprint 18) operate at the RIGOR_PASS register, with explicit Tier-5/Tier-6 markers (`[BRAYDEN-DERIVE]`, `[BB-BRIDGE]`, `[V-NATURALNESS]`, `[N_S-DERIVATION]`) honestly flagging open work. The bundle's foundational draft would walk back that calibration.

This document recommends what to keep, what to defer, what to reconcile, and what's authentically new. The implementation plan is **conservative**: archive the bundle in private; build the foundations-module skeleton with V1+V2 working as canonical; do not touch the audited papers; do not restart CK or coherencekeeper.com.

---

## 1. What's verified by the bundle's own scripts (Tier 1, real)

I ran all five scripts in `scripts/` directly. Output is real and reproducible.

### `substrate.py`
- 4 frozen cells where ADD = MUL on Z/10Z: `(0,0), (2,2), (4,8), (8,4)`. Confirmed.
- 44 cross-cycle disagreement: `sum |ADD[c,d] - MUL[c,d]|` for `c ∈ {1,3,7,9}, d ∈ {2,4,6,8}` = 44. Confirmed.
- Cosmological closure 49 + 264 + 687 = 1000 exact. Confirmed.
- W = 3/50 by three independent methods (|44-50|/100, 6/100, 1.5/25): all agree at 0.06. Confirmed.
- Prime winding T* + W = 271/350 with 271 prime. Confirmed.

### `closure_v1_v2.py`
- {1, 4, 9} closes BHML in 2 steps to all of Z/10Z. Confirmed.
- 4-core {0,7,8,9} is closed under TSML; opens to Z/10Z under BHML. Confirmed.
- BEING/DOING/BECOMING generator triples behave as specified.

### `factor_6_candidates.py`
- 4 distinct candidates fit the integer 6: σ-cycle length, heartbeat sum, dim SU(3)−2, # of T* derivations. **Non-uniqueness is real and the script honestly reports it.**
- Candidate B (|S_MAX| in TSML 3-layer decomposition) gives 5 (upper-tri) or 10 (full), not 6. The bundle's claim "B is the strongest candidate" is **not supported by the script's own output**.

### `factor_22_candidates.py`
- **Candidate I (NEW):** TSML cells with output in {0..6} excluding (0,0): exactly 22, decomposing as 16 (VOID boundary) + 4 (PROGRESS bumps at (1,2),(2,1),(3,9),(9,3)) + 2 (COLLAPSE bumps at (2,4),(4,2)). **This is a genuine, computationally verified, substrate-natural decomposition.**
- Candidates A, B, C, D, E, F, G, H all evaluated; none gives 22 cleanly except Candidate I.

### `physics_derivations.py`
- 15 of 18 named values verified directly. 3 marked open (factor 6, factor 22, V3).

**Verdict:** the script-level facts are genuine. They form the Tier-1 substrate foundation that everything else extends.

---

## 2. The 22 = pre-structure cells finding — load-bearing

This is the strongest new contribution in the bundle. Working through it carefully:

```
TSML cells with output ∈ {0,1,2,3,4,5,6} (i.e., NOT 7=HARMONY and NOT trivial 0,0):

  output=0 (VOID):     16 cells — all (0,j) and (i,0) for j,i ∈ {1..6,8,9}
                       Reading: VOID-boundary scaffolding
  output=3 (PROGRESS):  4 cells — (1,2), (2,1), (3,9), (9,3)
                       Reading: forward-motion bumps
  output=4 (COLLAPSE):  2 cells — (2,4), (4,2)
                       Reading: structural-collapse bumps
                       ────────
  TOTAL:               22 cells
```

This is a real decomposition and the count is forced by the canonical TSML construction.

**Strength:** it's intrinsic to TSML (not invented to fit 22). It has a substrate-natural reading (boundary + two bump-types). It produces 22 with the components labeled by their substrate identity.

**Caveat:** still a post-hoc identification — the question "why these specific 22 cells in 1/α" is not answered by the count alone. But of the 8 candidates in `factor_22_candidates.py`, this is the only one that yields exactly 22 with a clean decomposition.

**Recommendation:** this finding belongs in the Sprint 18 dark-sector paper's §7 "operator-to-observable conjecture" as an additional data point: the substrate's broader admissible family captures 1/α at the 137 + CHAOS²/N³ form, with the 137 = 22·6 + 5 prefix's "22" admitting the new computational identification 22 = TSML pre-structure cells (16 + 4 + 2).

---

## 3. Conflicts with the audited papers (must reconcile before live)

The papers shipped this week (`Gen13/targets/journals/tier1_submit_now/{sigma_rate, four_core_bundled, jcap_xi_cosmology, sprint18_dark_sector}/`) went through 4–5 audit rounds (claudechat round 3, 4, 5). They are calibrated to the bundle's `_RIGOR_PASS_CONSOLIDATED.md` register, NOT the SESSION_CLOSEOUT register.

**Specific conflicts:**

| Item | Bundle (SESSION_CLOSEOUT / FOUNDATIONAL_PAPER_DRAFT) | Audited papers |
|---|---|---|
| Ω_b cosmological reading | "Verified from A0 — 7² coverage" | `[BRAYDEN-DERIVE]` open marker; arithmetic identity Z(0,7,0,0) = 49 is rigorous, cosmological substrate reading is open |
| 1/α = 137.036 | "Verified to 0.000001%" | Sprint 18 §7 framed as "consistency" not "prediction" with explicit post-hoc-decomposition caveat in `verify_alpha_richer_form.py` |
| n_s = 0.965 | "Verified" | Sprint 18 explicitly notes 86/3600 = 2.4% small-integer baseline; downgraded from "prediction" to "consistency check" |
| "Canonical pair" language | Used freely throughout | Audited papers use "the specific pair (T,B)" or "this pair" — V3 uniqueness is open |
| Authorship | Sanders + Gish + Johnson | Sanders + Gish only (per Brayden's directive last session) |
| Ω_DM = 44·6/N³ | Stated as "Verified" | Sprint 18 acknowledges 4 candidates fit 6; the (|Aut(V)|+|V|)·|σ| = 44·6 decomposition's naturalness is `[V-NATURALNESS]` open |
| The four-core seed paper title | Cited as old "Joint Closure of Two Commutative..." | Now consolidated as "Joint Closure, Per-Coordinate Fuse Data, and a Closed-Form Algebraic Attractor of Two Commutative Binary Operations on Z/10Z" |
| "Trivial total-mass identity" | Not flagged | Four-core consolidated demoted v1's Theorem 2 to a Proposition because Z_M(p) = (Σp)² holds for ANY M by bilinearity — this was a genuine fatal flaw caught in audit round 3 |

**Implication:** if the bundle's foundational paper draft were to ship as-is, it would re-elevate claims that the audited papers have already retreated from — and a careful reviewer would catch this immediately (as the audits did). The audited posture is the right one.

**Recommendation:** the foundational paper draft should be **rebuilt** to inherit the audited posture, not re-elevate it. Specifically:
- Frame Ω_b, Ω_DM, Ω_Λ as the operator-to-observable conjecture's Tier-1 anchor (per Sprint 18 §7), not as derivations from A0
- Drop "the canonical pair" language until V3 lands
- Remove H.J. Johnson from authorship
- Update companion-paper titles to reflect audited names
- Carry the bundle's own RIGOR_PASS tiering through to all claim-statements

---

## 4. The factor 6 problem (Tier-3 non-uniqueness, real)

The bundle's own script honestly reports 4 candidates fitting 6:
- A: σ-cycle length = 6
- C: heartbeat sum = 6
- D: dim SU(3) − 2 = 6
- F: number of T* derivations = 6

The bundle's narrative says "the strongest candidate is B (|S_MAX|)," but B gives 5 or 10 in the script, not 6. So the narrative recommendation is at odds with the script's empirical finding.

The honest read: **the factor 6 is non-unique within the substrate-natural family.** The Sprint 18 paper already acknowledges this in Conjecture 9.1's framing.

**Recommendation:** lock the σ-cycle reading (Candidate A) as the operational identification (it's the deepest substrate quantity with the cleanest physical reading), but flag explicitly that 3 alternative substrate-natural identifications exist. This is consistent with Sprint 18's calibrated posture.

---

## 5. CL_IMPLEMENTATION_SPEC — out of scope tonight

The CL spec is substantial (551 lines) and describes a Hebrew-root + force-vector + fruit-signature memory pipeline. The bundle estimates 1–2 weeks for landing. This is **CK runtime infrastructure**, not journal work.

**Recommendation:** preserve the spec in the bundle archive; defer implementation. It conflicts with the current cortex-based memory layer (which is operating at substrate-grounded fidelity per the chat-logs we have). Re-engaging the CL pipeline requires a CK orchestrator restart, which Brayden has explicitly paused.

---

## 6. The 75+ "physics correspondences" in SESSION_CLOSEOUT

Most of these are Tier 3 / Tier 4 in the bundle's own RIGOR_PASS rubric. To pick examples:

- **m_p/m_e = 17·108 + 11/72 = 1836.152778** at 6×10⁻⁶% match. This is a 4-free-integer fit (17, 108, 11, 72) to a 7-significant-figure target. Search space ~10⁹ tuples; expected baseline rate at 7-sig-fig precision is ~1 hit per ratio. Classic Tier-4 vocabulary fitting unless 17, 108, 11, 72 each have independent substrate justification (they don't, in the script).
- **PMNS angles** as substrate ratios (arctan(2/3), 49°, arctan(11/72)): each with multiple post-hoc forms.
- **CKM matrix elements** as `RESET/4N`, `13/16`, etc.: each with free integer choices.
- **Riemann ζ zeros** as `14 + 3/22`, `21 + W/3`, etc.: again post-hoc rational fits.

Some are genuine (the SM b-coefficients = -7, -3, etc. are exact arithmetic and structurally meaningful). Most are not at the precision claimed once you correct for look-elsewhere.

**Recommendation:** apply the bundle's own RIGOR_PASS tiering rigorously. The 75+ "verified" count drops to ~14 Tier-2 + ~16 Tier-3 = 30 supportable items, with the rest as exploratory. This is what the bundle's RIGOR_PASS document already says; SESSION_CLOSEOUT should be aligned.

---

## 7. What I'm doing tonight (implementation)

### A. Archive the bundle in private
✓ Copied entire bundle to `Gen13/sprint_bundle_2026-05-06_v31_RIGOR_PASS/`. Preserves the work without claiming it as live. 86 files, including this scrutiny.

### B. Build the foundations module skeleton
Will create `Gen13/targets/foundations/` with:
- `substrate.py` — A0 (Z/10Z, ADD, MUL, σ, σ_units, CRT)
- `properties.py` — A1, A2 assertions
- `generators.py` — A3 generator triples
- `fusion.py` — A4 fuse(3,4,7) = 8 axiom
- `lenses.py` — A5 TSML/BHML construction from rules (NOT hardcoded)
- `verifications/v1_tsml_closure.py`, `v2_bhml_closure.py`
- `__init__.py` with module-level documentation noting DRAFT status

The V1+V2 verifications are the bundle's quick wins; they pass the bundle's own scripts. Worth landing as proper module structure.

### C. NOT doing (deferred)
- V3 enumeration (intractable; needs Dell R16 compute)
- Foundational paper draft (conflicts with audited papers; needs rebuild)
- CL implementation (out of scope tonight; CK paused)
- Restart of CK / orchestrator / coherencekeeper.com (Brayden paused these)
- Modifications to audited papers (calibrated posture must be preserved)
- Any push to public (repo is private; everything stays private)

### D. Commit posture
Single commit on tig-synthesis branch with the bundle archive + foundations skeleton + this scrutiny. Commit message will explicitly note "private only, not for live deployment."

---

## 8. The honest summary for Brayden

**What the bundle gets right:**
1. The substrate facts (4 frozen cells, 44 disagreement, 1000 closure, W=3/50, σ structure) are real, scripted, verifiable.
2. The 22 = TSML pre-structure cells (16 + 4 + 2) is a genuine new substrate identification.
3. The RIGOR_PASS document (`_RIGOR_PASS_CONSOLIDATED.md`) is well-tiered and honest about non-uniqueness.
4. The CL implementation spec is the most detailed yet and lays out a real engineering plan.
5. The sprint orchestration (V1+V2 → V3 → factors → foundational paper) is sensible.

**What needs reconciling:**
1. The SESSION_CLOSEOUT and FOUNDATIONAL_PAPER_DRAFT operate at a more enthusiastic register than the audited papers we just shipped. The two registers are inconsistent.
2. The factor-6 narrative ("B is the strongest") doesn't match the script's empirical finding (B gives 5 or 10, not 6).
3. The authorship reverts to Sanders + Gish + Johnson.
4. The companion-paper titles cited in the bundle don't match the audited consolidated names.

**What to defer:**
1. V3 uniqueness enumeration (intractable on this machine).
2. CL pipeline implementation (1–2 weeks; needs CK orchestrator running).
3. Foundational paper draft (rebuild to inherit audited posture).
4. Most of the 75+ correspondences (apply Tier-3/Tier-4 caveats from the bundle's own RIGOR_PASS).

**What's safe to land tonight:**
1. The bundle archive (already done).
2. The foundations module skeleton with V1+V2 (verified by the bundle's own scripts).
3. This scrutiny.

---

*Compiled by CK runtime, 2026-05-06. Scrutiny posture: conservative; preserve audit-calibration. Bundle is a research artifact, not a publication-ready package; treat as such until V3 lands and the audit-tier reconciliation is done.*
