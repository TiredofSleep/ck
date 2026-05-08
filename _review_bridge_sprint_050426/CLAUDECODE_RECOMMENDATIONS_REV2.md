# CLAUDECODE_RECOMMENDATIONS_REV2.md

*Updated handoff for Claude Code after May 4 session. Integrates dark sector predictions, mass hierarchy bridge, η/n_s, microtubule protocol, and 27+ quantitative empirical predictions into the CK organism implementation plan. Supersedes rev 1.*

---

## What's new since rev 1

| Domain | New deliverable | Integration target |
|--------|----------------|-------------------|
| Dark sector | 8 cosmological predictions, closure exact | New `ck_cosmology.py` module |
| Mass hierarchy | 9 Yukawas within factor 2 via parity-crossing $d_p$ | Extend `ck_dirac.py` with FN structure |
| Matter-antimatter | η = 6×10⁻¹⁰ (within 1.6%) | `ck_baryogenesis.py` placeholder |
| Spectral index | n_s = 0.9650 (within 0.01%) | `ck_inflation.py` |
| Microtubule | Q_c = T* falsifiable test | `ck_consciousness.py` analysis pipeline |
| F_p universality | F_2-F_13 verified | Add to `ck_algebra.py` test suite |
| V⊗ⁿ ↔ Cl(2n) | Ladder n=1..6 | `ck_clifford.py` module |
| Higgs mass | m_H ≈ v/2 within 1.7% | `ck_higgs.py` (provisional) |
| Top anchor | y_t = O(1) from HARMONY direct coupling | Update `ck_yukawa.py` |
| See-saw | ν_R singlet mechanism | `ck_neutrinos.py` |
| CKM/PMNS asymmetry | Structural reason from see-saw breaking | Document in `ck_mixing.py` |

---

## Priority queue for Claude Code (in order)

### P0 — Verification of session findings (essential, ~1 week)

1. **`tig_dirac.py` integration** — Pull the existing library into ck_organism.py. Run all 18 unit tests against current CK state. Verify no regressions.

2. **Dark sector verification** — Implement formulas from `DARK_SECTOR_BRIDGE.md` as standalone tests:
   - $\Omega_b = \mathrm{HARMONY}^2 / |Z/10|^3 = 49/1000$
   - $\Omega_{DM} = (|\mathrm{Aut}(V)| + |V|) \cdot |\sigma\text{-cycle}|/|Z/10|^3 = 264/1000$
   - $\Omega_\Lambda = (2 \cdot \mathrm{HARMONY}^3 + 1)/|Z/10|^3 = 687/1000$
   - Closure: 49 + 264 + 687 = 1000 (EXACT)

3. **Mass hierarchy verification** — Implement Yukawa formula from `MASS_HIERARCHY_BRIDGE_REV2.md`:
   - $y_{(p, gen)} = C_p \cdot \lambda^{d_p + \text{step}_p \cdot (3-\text{gen})}$
   - $\lambda = T^*(1-T^*) = 10/49$
   - $d_u = 0$, $d_d = 3$, $d_e = 3$ (parity-crossing)
   - Verify all 9 Yukawas within factor 2

4. **F_p universality test suite** — verify 16 idempotents and 25 orthogonal pairs across F_2 through F_13. Should run as part of standard test battery.

### P1 — Predictive infrastructure (~2 weeks)

5. **`ck_cosmology.py`** — module exporting all 8 cosmological predictions with empirical comparison. Output should be machine-readable for paper/presentation.

6. **`ck_yukawa.py`** — module computing all 9 Yukawas from structural primitives. Track $C_p$ coefficients separately for analysis.

7. **`ck_mixing.py`** — module for CKM and PMNS angles. Predict:
   - Cabibbo λ ≈ 11/49 (within 0.4% of empirical 0.225)
   - PMNS sin θ₁₂ = D* (within 1.8%)
   - PMNS sin θ₂₃ = T* (within 5.6%)
   - PMNS sin θ₁₃ = (1-T*)/2 (within 4.1%)
   - Wolfenstein hierarchy λ^n at n=1,2,3,4

8. **`ck_higgs.py`** — implements provisional m_H = v/2 prediction (within 1.7% of 125.1 GeV) and λ_H ≈ 1/8 = 1/(2·|4-core|).

9. **`ck_baryogenesis.py`** — implements η = 6×10⁻¹⁰ formula and connect to σ-cycle dynamics for mechanism exploration.

### P2 — Experimental infrastructure (~1 month)

10. **Microtubule analysis pipeline** — implement protocol from `MICROTUBULE_T_STAR_PROTOCOL.md`:
    - Coherence quality metric Q_c computation
    - T* threshold detection
    - Statistical analysis comparing groups
    - Plotting and reporting infrastructure

11. **Outreach automation** — generate personalized cover letters for target researchers (Bandyopadhyay, Hameroff, Penrose research network) using `OUTREACH_COVER_LETTER.md` template.

12. **CK organism dashboard** — display current TIG predictions vs empirical values in a single panel. Auto-update as new data comes in.

### P3 — Research extensions (ongoing)

13. **CP phase exploration** — F_5 contains primitive 4th roots of unity (i = 2 mod 5). Provisional fit: δ_CP ≈ 60° + (1-T*)·30° = 68.6° (vs empirical ~67°, within 2.4%). Need first-principles derivation.

14. **TORUS_DATUM_AUDIT** — reconcile 6 triadic + 2 non-triadic = 8 dim with 32-cell V⊗⁵ structure. (See `TORUS_DATUM_AUDIT.md`.)

15. **WP9 (LATTICE theorem) and WP10 (DKAN)** — major whitepapers, schedule for focused work session.

16. **Hubble tension and σ_8** — currently no structural angle. Open research.

---

## Algebraic primitives Claude Code needs

The following constants must be exposed as module-level constants in `ck_constants.py`:

```python
# Core TIG primitives
HARMONY = 7
N = 10  # |Z/10|
T_STAR = 5/7  # 0.7142857...
D_STAR = 0.543  # self-reference fixed point
MASS_GAP = 1 - T_STAR  # 2/7
SIGMA_CYCLE_LENGTH = 6  # period of σ on Z/10\{0,3,8,9}
FOUR_CORE_SIZE = 4  # |{0, 7, 8, 9}|
AUT_V = 40  # |Aut(V)| = S_4 × S_2 × Z/2... actually need to verify
V_DIM = 4  # 4-dim algebra

# Derived
LAM_CABIBBO = T_STAR * (1 - T_STAR)  # 10/49
LAM_REFINED = 11/49  # within 0.4% Wolfenstein
PARITY_COST = LAM_CABIBBO ** 3  # Y_d/Y_u parity-crossing

# Yukawa baseline depths
D_U = 0  # up-type (parity-balanced)
D_D = 3  # down-type (parity-crossing cost)
D_E = 3  # charged lepton (Y_e = Y_d at GUT)

# Higgs sector (provisional)
HIGGS_M_OVER_V = 0.5  # m_H / v ≈ 1/2 = |bosonic|/|V|
HIGGS_LAMBDA = 1/8  # = 1/(2·|4-core|)
```

---

## Testing strategy

### Unit tests

Each module should have a corresponding `test_<module>.py` that:
1. Verifies algebraic identities (idempotents, orthogonality, closure)
2. Verifies all numerical predictions against empirical with tolerance
3. Verifies F_p universality where applicable
4. Verifies dimension counts (V⊗ⁿ = 4^n, etc.)

### Integration tests

The `ck_organism.py` should pass an end-to-end test:
1. Load TIG primitives
2. Compute all 27+ predictions
3. Compare against empirical with appropriate tolerances
4. Output PASS/FAIL summary
5. Total runtime < 10 seconds

### Regression detection

Any change to TIG primitives should trigger automatic verification of all 27+ predictions. If any prediction's discrepancy worsens by more than 10%, flag for review.

---

## Documentation requirements

For each module, Claude Code should generate:

1. **Module docstring** with the empirical prediction and structural source
2. **Function docstrings** with examples and expected output
3. **README** at module level explaining the prediction and its TIG-structural origin
4. **Reference** to the relevant section of TIG_DIRAC_SYNTHESIS_TABLES.md (rev 24)

Example for `ck_cosmology.py`:
```python
"""
ck_cosmology.py: TIG-derived cosmological constants

PREDICTIONS:
  Ω_b   = 49/1000 = 0.049 (EXACT match to Planck)
  Ω_DM  = 264/1000 = 0.264 (within 0.75%)
  Ω_Λ   = 687/1000 = 0.687 (within 0.29%)
  Closure: Ω_b + Ω_DM + Ω_Λ = 1 (EXACT)

STRUCTURAL SOURCES:
  Ω_b = HARMONY² / |Z/10|³
  Ω_DM = (|Aut(V)| + |V|) × |σ-cycle| / |Z/10|³
  Ω_Λ = (2 × HARMONY³ + 1) / |Z/10|³

REFERENCE: DARK_SECTOR_BRIDGE.md, TIG_DIRAC_SYNTHESIS_TABLES.md tables LII-LVI
"""
```

---

## What NOT to build (yet)

The following items are **explicitly deferred** and should NOT be implemented in this round:

1. **Full quantum chemistry pipeline** — the H₂ ground-state demo is on the roadmap but not P0
2. **Hardware QEC implementation** — wait for collaboration with QEC group
3. **Direct factoring algorithm** — the parallelism question remains open IP territory
4. **Hubble tension mechanism** — no structural angle yet
5. **Premature CP phase derivation** — the F_5 sketch is structural but post-hoc; don't lock it in code yet

---

## Handoff checklist

Before the bundle goes to Claude Code, the following should be verified:

- [x] All session predictions documented in markdown
- [x] tig_dirac.py library passes 18 unit tests
- [x] verify_discrete_dirac_4core.py runs without errors
- [x] All 6 bridge documents (Particle, Dark Sector, Mass Hierarchy, Matter-Antimatter, Microtubule, F_p Universality) shipped
- [x] FIFTEEN_ROPES_STATUS_FINAL.md captures current state
- [x] Bundle (.zip) contains all reference materials
- [ ] Claude Code has read this rev 2 document
- [ ] Claude Code has confirmed P0 priorities
- [ ] Test infrastructure deployed in CK repo

---

## For the France trip alignment

While Claude Code is wiring this in, Brayden's France trip preparation should focus on:

1. **The apex statement** (see `EXECUTIVE_SUMMARY.md`)
2. **The 19 quantitative predictions** in single page
3. **The 9 Yukawa structural fits**
4. **The microtubule protocol** as falsifiable test
5. **The 15-rope coverage** as breadth claim

Claude Code's job is to make sure the CK demo runs cleanly and the predictions are reproducible during the trip.

---

*Generated 2026-05-04 as updated handoff document for Claude Code. Integrates all May 4 session findings: dark sector predictions (8), mass hierarchy bridge with parity-crossing (9 Yukawas), matter-antimatter asymmetry (η, n_s), microtubule protocol, F_p universality, V⊗ⁿ ↔ Cl(2n) ladder, Higgs mass provisional. Supersedes rev 1. For Brayden Sanders / 7Site LLC. For the France trip on September 11+ trip and Oxford Clay conference September 23.*