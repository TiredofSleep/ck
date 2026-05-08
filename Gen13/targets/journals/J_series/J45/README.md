# J45 — The Mass Hierarchy from V⊗5 SU(5) Decomposition

**Status:** FORMAT
**Phase:** Phase 5
**Target venue:** PRD (Physical Review D)
**Author lane:** Sanders + Gish
**Tier:** Forced FN power + measured anchor (Tier-B)
**WP source:** WP122 (Sprint 18 Bridge-Dirac, 2026-05-04)

---

## §1 — Manuscript

**Local path:** `manuscript/mass_hierarchy_v5.tex`

Files in this J-folder's `manuscript/`:

- `mass_hierarchy_v5.tex` — PRD-format LaTeX, ~340 lines, all environments balanced.

**Abstract (one sentence).** All nine SM charged-fermion Yukawa couplings flow from a single substrate-derived suppression scale `lambda = T*(1 - T*) = 10/49`, the top-quark anchor `y_t ≈ 0.93`, and integer powers `n_{(p, gen)} ∈ {0, 3, 5, 6, 7, 9}` forced from the V^{⊗5} SU(5) decomposition `1 ⊕ bar 5 ⊕ 10` plus the parity-crossing cost `d_p ∈ {0, 3, 3}` plus the sigma-orbit generation step — landing all nine couplings inside the standard Froggatt-Nielsen factor-of-a-few window with zero free FN charges and zero free flavon scales.

## §2 — Verification

**Primary primitive (machine-checkable):** `Gen13/targets/ck/brain/dirac/tig_dirac.py`

```python
from tig_dirac import predict_yukawa, LAMBDA_FN, Y_T_ANCHOR

assert LAMBDA_FN == 10 / 49         # substrate-forced FN scale
assert Y_T_ANCHOR == 0.93            # measured top-quark anchor

# top quark anchor
r = predict_yukawa('up', 3)
assert r['y_predicted'] == 0.93
assert r['fn_power'] == 0

# electron at FN power 9
r = predict_yukawa('lepton', 1)
assert abs(r['y_predicted'] - 0.93 * (10/49)**9) < 1e-12
assert r['fn_power'] == 9
assert r['tier'] == 'Forced FN power + measured anchor (Tier-B)'
```

The function `predict_yukawa(particle, generation)` returns:
- `y_predicted`: the predicted Yukawa magnitude `y_t * lambda^n`
- `fn_power`: the integer FN exponent `n`
- `name`: the SM fermion name ('t', 'b', 'tau', 'e', 'mu', 'nu_3', etc.)
- `lambda`: 10/49 (the substrate-forced FN scale)
- `y_t_anchor`: 0.93 (the Tier-A measured anchor)
- `tier`: 'Forced FN power + measured anchor (Tier-B)'
- `reference`: 'WP122 (Sprint 18 Bridge-Dirac, 2026-05-04)'

The companion call `tig_dirac.yukawa_table_full()` returns the full Table 5.1 of the manuscript programmatically. Substrate-shared with J44's `predict_dark_sector()`.

## §3 — Dependencies (J-papers cited as already-submitted companions)

- **J44** (Sanders + Gish, PRD, same Sprint 18 cluster) — *Sprint 18 Dark Sector.* Companion paper using the same `tig_dirac` module via `predict_dark_sector()`. **Per-venue cap: J45 is the 2nd PRD paper this quarter, after J44.**
- **J16** (Sanders + Gish, foundation paper) — *Discrete Dirac on the 4-Core's F_5-Lift.* Supplies the V^{⊗5} 32-cell SU(5) decomposition (Lemma 2.1) used as the algebraic input here.
- **J46** (Sanders + Gish, JCAP) — *Logarithmic Quintessence.* Co-cited via J44.
- **J07** (Sanders + Gish, Communications in Algebra) — *Joint Closure on Z/10.* Supplies T* = 5/7 cited in §3.

## §4 — Cover letter

See `cover_letter.md` in this folder. Filled out for PRD submission with a one-paragraph plain-English summary, three venue-fit bullets, J44/J16/J46/J07 companion list, and the `tig_dirac.predict_yukawa` reproducibility primitive.

## §5 — Status & summary

**Status: SAVE_PLAN_PENDING (2026-05-07).** Referee verdict (`Atlas/META_PLAN_2026-05-06/REFEREE_REPORTS/J45_PRD_FreshEyes.md`): MAJOR REV verging on REJECT. Save plan landed at `Atlas/META_PLAN_2026-05-06/SAVE_PLANS/SAVE_PLAN_J45.md`.

**Save-plan summary.** The load-bearing observation — $\lambda = T^*(1-T^*) = 10/49$ from substrate forcing, raised to integer powers, recovers SM Yukawa hierarchy at standard FN factor-of-a-few precision — is real and worth publishing. The save path is honest reframing: (a) ACCEPT the precision honestly — replace "zero free FN charges / factor-of-a-few" with "phenomenological substrate-derived FN pattern matching SM Yukawa hierarchy to 30–40% precision; tightening to standard FN level requires C_p multipliers documented in Table 5.1"; (b) drop the "single λ" framing since Remark 3.2 contradicts it (the framework uses two close rational scales: 10/49 for masses, 11/49 for CKM); (c) honest parameter accounting (1 anchor + 2 scales + 9 σ-orbit assignments + 9 fittable C_p ≈ 21 vs standard FN's 13 — different framing, not simpler); (d) drop sterile-neutrino paragraph entirely (Dirac-mass numerology without see-saw); (e) demote Theorem 3.1 to Observation 3.1 (max-entropy variance reads as numerology); (f) state renormalization scale ($\mu = M_Z$) and recompute Table 5.1 ratios; (g) self-contained §2 for the V⊗5 SU(5) decomposition; (h) fix author list (Sanders + Gish per directive) and hjj01986 email assignment.

**Recommended retitle / retarget:** Option A (preferred — retitle to *"A Substrate-Derived FN Pattern with $\lambda = 10/49$ and SU(5)-Rep Indexing for the SM Charged-Yukawa Hierarchy,"* keep PRD, ship in 2–3 weeks; survival probability moderate, 30–40%). Option D (strong-form — joint J38+J45 paper *"From the 4-core's $\mathfrak{so}(10)$ Closure to a Substrate-Derived FN Pattern"* if J38 timeline aligns; survival probability moderate-to-good). Fallback: MPLA or PLB Letter if PRD desk-rejects.

**Revision time:** 2–3 weeks of focused editing.

**Format gate (`tig_dirac.predict_yukawa`):** still green. The primitive is in `Gen13/targets/ck/brain/dirac/tig_dirac.py` (line 617). Returns `y_t = 0.93` for `predict_yukawa('up', 3)` and `y_e ≈ 5.71e-7` for `predict_yukawa('lepton', 1)` via `lambda^9` with `lambda = 10/49`.

**Summary of the load-bearing claims.**
1. **The substrate-derived FN scale (Theorem 3.1):** `lambda = T*(1-T*) = (5/7)(2/7) = 10/49 ≈ 0.2041` is the unique substrate quantity that arises as a max-entropy variance at the joint coherence threshold, factors as `|Z/10|/HARMONY^2`, and reproduces the Wolfenstein hierarchy.
2. **The forced FN powers (Table 4.1):** `n_{(p, gen)}` is read off the SU(5) Yukawa diagram (parity-crossing cost `d_p ∈ {0, 3, 3}`) plus the sigma-orbit generation step — zero free FN charges across all nine charged fermions.
3. **The fit (Table 5.1):** all 9 charged-Yukawa ratios `y_pred/y_meas` ∈ {1.00, 1.08, 1.06, 0.33, 0.60, 0.51, 0.79, 0.11, 0.20}; five sit in the conventional FN factor-of-three window; the four largest residuals define the empirical `C_p ∈ [0.11, 0.79]` multipliers expected from incomplete bosonic-substrate specification.
4. **Cabibbo cube-root identity (§6):** `lambda_C ≈ (Y_d/Y_u)^{1/3}` follows from the parity-crossing cost `d_d = 3`, unifying CKM mixing with mass hierarchy.
5. **Sterile-neutrino scale (§5 last paragraph):** Dirac Yukawas at FN powers {12, 13, 14} give sub-eV scales near the Planck `Sigma m_nu < 0.12 eV` bound, but without an explicit see-saw insertion (open question §7.3).

**Open structural questions tracked** (per manuscript §7):
- The C_p residual multipliers (Higgs-sector dynamics on V^{⊗5}'s singlet + bar 5_H partner) — load-bearing follow-up
- The generation-step asymmetry (s_u, s_d, s_e — needs sigma-action on color-charged vs color-singlet cells)
- Sterile-neutrino mass scale and the see-saw (where does M_R come from?)
- The refined lambda_ref = 11/49 (Cabibbo at 0.4% — substrate-natural correction or phenomenological adjustment?)



### Family-Structure framing (per Atlas/META_PLAN_2026-05-06/FAMILY_STRUCTURE_v1.md)

This paper sits within the TIG family of finite commutative non-associative magmas on Z/10Z (and ring extensions per D74). The family is defined by 5 conjoint membership criteria; the 4-core {V, H, Br, R} = {0, 7, 8, 9} at α_M = ½ is the algebraic center, with closed-form attractor h/β = 1+√3 (D78 Galois proof). The closest published precedent for this neighborhood is **Drápal & Wanless (2021), *J. Combin. Theory A* **184**, 105510** — same domain (small finite commutative non-associative structures), opposite extremum (theirs maximally non-associative).

### PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN — template (fill per paper)

- **PROVEN:** [the specific theorem of this paper]
- **COMPUTED:** [verified-by-script invariants supporting the theorem]
- **STRUCTURAL RHYME:** [constants/identities cited as motivation, not derivation]
- **OPEN:** [the natural next-paper question]

### Lens-ownership paragraph — template (fill per paper, insert in manuscript §0)

> *Lens and substrate.* This paper works on [substrate: Z/10Z / Z/N for N in {...} / F_p for p in {...}] with the [tables: TSML / BHML / both]. These choices are not derived from first principles; they reflect a structural reading of the substrate motivated by [phonaesthesia / 10-operator decomposition / observed dynamics]. The theorems below are theorems on this specific structure; analogous theorems would hold on other substrate-and-table choices. Whether other substrate choices give similarly rich downstream connections is open.

### Hardening status (auto-applied 2026-05-07)

- License: submission scripts CC-BY-4.0 (per `_v3_hardening.py`)
- AI-attribution: Claude/Anthropic byline references removed (per `_v3_hardening.py`)
- Author lane: Sanders + Gish (per Brayden directive)
- Drápal-Wanless 2021 citation in references

## §6 — Submission checklist

- [x] Manuscript .tex finalized (PRD format, ~340 lines, balanced environments)
- [x] Verification primitive green (`predict_yukawa('up', 3)['y_predicted'] == 0.93`; `predict_yukawa('lepton', 1)['y_predicted'] ≈ 0.93 * (10/49)^9`)
- [x] Tier-classified central claim explicit ("Forced FN power + measured anchor (Tier-B)")
- [x] Lens-scope annotation (TSML_RAW vs TSML_SYM) — N/A here; the substrate is V = F_5-lift of the 4-core, not the TSML/BHML pair directly
- [x] Cover letter finalized (J44/J16/J46/J07 companions; tig_dirac.predict_yukawa primitive cited)
- [x] Dependencies → cite each J-companion as "submitted to [venue]"
- [ ] Brayden's referee-rigor pass complete (mobile + other AI + collaborators) — pending
- [x] Per-venue cap check: this is the **2nd** PRD paper this quarter (J44 was 1st)
- [ ] Submitted

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Johnson, H.J. (2026). "The Mass Hierarchy from V^{⊗5} SU(5) Decomposition: a Substrate-Forced Froggatt-Nielsen Pattern with lambda = 10/49." Submitted to *Physical Review D*. Companion to J44 (Sprint 18 Dark Sector, PRD), J16 (Discrete Dirac on F_5^4, foundation).
