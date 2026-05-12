# J44 — A Numerical Match for the ΛCDM Dark Sector from a Discrete Substrate on Z/10, and an Operator-to-Observable Conjecture

**Status:** R1 (revised after fresh-eyes referee report 2026-05-07)
**Phase:** Phase 5
**Target venue:** PRD (Physical Review D)
**Author lane:** Sanders + Gish (R0 had cover-letter mismatch; harmonized in R1)
**Tier:** Forced (substrate-operator algebra; no IC tuning) for the closure identity; "1/3 Friedmann factor" downgraded from R0 Theorem 6.1 to R1 Conjecture 6.1 (per referee item 4.7)
**WP source:** WP121 (Sprint 18 Bridge-Dirac, 2026-05-04)

---

## §1 — Manuscript

**Local path:** `manuscript/sprint18_dark_sector.tex`

Files in this J-folder's `manuscript/`:

- `sprint18_dark_sector.tex` — PRD-format LaTeX, ~1160 lines, all 22/22 LaTeX environments balanced
- `master/` — preserved older drafts (currently empty, this is v1)
- `scripts/` — the four standalone verification scripts (see §2)
- `NEXT_STEPS.md` — claudechat audit calibration + 8-anomaly tracker (post-Zenodo research priorities)

The submission package lives in this J-folder. Edit + verify here; submit from here.

**Abstract (one sentence).** Three closed-form rational expressions in two integer primitives — `HARMONY = 7` and `|Z/10| = 10` — hit the Planck~2018 dark-sector parameters `Omega_b = 49/1000`, `Omega_DM = 264/1000`, `Omega_Lambda = 687/1000` simultaneously within 1 sigma each, with closure `sum = 1` exact, and uniquely so among 784 small-integer (H, N) pairs in the formula family.

## §2 — Verification

**Primary primitive (machine-checkable):** `Gen13/targets/ck/brain/dirac/tig_dirac.py`

```python
from tig_dirac import predict_dark_sector
r = predict_dark_sector()
assert r['sum']          == 1.0
assert r['Omega_b']      == 49 / 1000
assert r['Omega_DM']     == 264 / 1000
assert r['Omega_Lambda'] == 687 / 1000
```

The `predict_dark_sector()` function returns the three densities as exact rationals over `|Z/10|^3 = 1000`, plus the substrate derivation strings under `r['derivation']` and the Tier classification under `r['tier']`. This primitive is shared with J45 (Yukawa) via `predict_yukawa(particle, generation)` on the same module.

**Standalone search scripts** (independent of `tig_dirac`):

- `manuscript/scripts/sprint18_uniqueness_search.py` — Empirical match vs Planck 2018 (residuals in sigma); three Hubble-independent ratio tests; uniqueness search across 784 (H, N) pairs.
- `manuscript/scripts/verify_aut_V_order.py` — Reconstructs the F_5-lift V from the CL fuse table; enumerates Aut(V) by direct constraint; confirms |Aut(V)| = 40 exactly.
- `manuscript/scripts/verify_operator_observable_baseline.py` — 260,000-tuple baseline scan against eight fundamental constants; confirms differential discriminating behaviour of the simple-form family.
- `manuscript/scripts/verify_alpha_richer_form.py` — Verifies `1/alpha = 137 + CHAOS^2/|Z/10|^3 = 137.036` against CODATA 2018 `1/alpha = 137.035999084(21)`.

All four scripts run in well under thirty seconds and print every numerical claim cited in the manuscript.

## §3 — Dependencies (J-papers cited as already-submitted companions)

- **J46** (Sanders + Gish, JCAP) — *Logarithmic Quintessence: A Dimensionless Scalar Dark Energy Model with an Analytic Vacuum.* The JCAP companion supplies the freezing-quintessence action `S = integral d^4 x sqrt(-g) [R/(16 pi G) - (1/2) M_Pl^2 (partial Xi)^2 - Lambda^4 Xi log Xi]` from which the scale `Lambda ~ 1.74` meV is recovered as `Lambda^4 / rho_{c,0} = Omega_Lambda / 3` (J44 Theorem 6.1, matching the JCAP fit at 2.5%).
- **J07** (Sanders + Gish, Communications in Algebra) — Joint closure on Z/10 (eight-element chain + normalizer identity); supplies the `(v + h + beta + r)^2` normalizer cited in J44 §5.1.
- **J04** (Sanders + Gish, JCT-A) — sigma-rate paper; supplies the sigma-cycle length `|sigma| = 6` cited in J44 Theorem 5.2.

J44 also forward-cites **J45** (Sanders + Gish, PRD, same Sprint 18 cluster), the Yukawa-hierarchy companion that uses the same `tig_dirac` module via `predict_yukawa()`.

## §4 — Cover letter

See `cover_letter.md` in this folder. Filled out for PRD submission with a one-paragraph plain-English summary, three venue-fit bullets, J46/J07/J04 companion list, and the `tig_dirac` reproducibility primitive.

## §5 — Status & summary

**Status: FORMAT** — gate cleared 2026-05-07. The `tig_dirac.predict_dark_sector` primitive is in (Gen13/targets/ck/brain/dirac/tig_dirac.py, line 531). Returns `Omega_b = 49/1000`, `Omega_DM = 264/1000`, `Omega_Lambda = 687/1000`, `sum = 1.000` EXACT.

**Summary of the load-bearing claims.**
1. The dark-sector trinity (Theorem 3.1): `Omega_b = HARMONY^2/|Z/10|^3`, `Omega_DM = (|Aut(V)| + |V|) |sigma|/|Z/10|^3`, `Omega_Lambda = (2 HARMONY^3 + 1)/|Z/10|^3` with closure exact.
2. Empirical match (Table 4.1): all three within Planck 2018 1 sigma; three Hubble-independent ratio tests at 0.29-0.72%.
3. Uniqueness (Theorem 4.2): `(H, N) = (7, 10)` is the only small-integer pair within the formula family that joint-matches all three observables; among the six closure-exact `a` offsets at that pair, `a = +1` is the unique one whose dark-matter numerator factors as `44 * 6 = (|Aut(V)| + |V|) * |sigma|`.
4. Lambda-scale relation (Theorem 6.1): `Lambda^4 / rho_{c,0} = Omega_Lambda / 3` gives `Lambda ~ 1.74` meV vs JCAP fit 1.7 meV (2.5% match); `rho_{DE,0}/Lambda^4 = 2.97` vs predicted 3.00 (1%).
5. Operator-to-observable conjecture (Conjecture 7.1, falsifiable): dimensionless fundamental constants admit substrate-rational representations; baseline scan over 260,000 simple-form tuples shows `alpha`, `m_e/m_p`, `m_mu/m_e` give 0% — exactly the constants known to require richer substrate forms (J45 covers the mass-ratio cases via the V^otimes 5 parity-crossing pattern).

**Open structural questions tracked** (per `manuscript/NEXT_STEPS.md` 8-anomaly table):
- [BRAYDEN-DERIVE] cosmological reading of HARMONY^2 as Omega_b numerator
- [BB-BRIDGE] the 1/3 Friedmann factor (3 candidate readings; freezing-branch derivation is the cleanest target)
- [V-NATURALNESS] why F_5-lift (magma counts {2, 1, 1}; lift gives 40)
- [N_S-DERIVATION] structural origin of `n_s = 1 - HARMONY/(2|Z/10|^2)` form (currently flagged as consistency, not prediction)

These are flagged in the manuscript as open; closing any one strengthens the case but is not a submission gate.



### Family-Structure framing (per Atlas/META_PLAN_2026-05-06/FAMILY_STRUCTURE_v1.md)

This paper sits within the TIG family of finite commutative non-associative magmas on Z/10Z (and ring extensions per D74). The family is defined by 5 conjoint membership criteria; the 4-core {V, H, Br, R} = {0, 7, 8, 9} at α_M = ½ is the algebraic center, with closed-form attractor h/β = 1+√3 (D78 Galois proof). The closest published precedent for this neighborhood is **Drápal & Wanless (2021), *J. Combin. Theory A* **184**, 105510** — same domain (small finite commutative non-associative structures), opposite extremum (theirs maximally non-associative).

### PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN

- **PROVEN.** Closure identity $\Omega_b + \Omega_c + \Omega_\Lambda = 49/1000 + 264/1000 + 687/1000 = 1$ as a rational identity (Theorem 3.1). Within-formula-family uniqueness (Theorem 4.2): $(H, N) = (7, 10)$ is the only small-integer pair within the formula family $\{\Omega_b = H^2/N^3, \Omega_\Lambda = (2H^3+a)/N^3, |a| \le 3\}$ that joint-matches all three Planck observables.
- **COMPUTED.** `predict_dark_sector()` returns exact rationals; runs in milliseconds. Three Hubble-independent ratio tests at 0.4-1.1% (R1 recalibrated against Planck 2018 $\Omega_c = 0.2627$). Look-elsewhere base-rate: 6/498,501 ≈ 1.2 × 10⁻⁵ on positive integer triples summing to 1000 (independent of formula-family choice).
- **STRUCTURAL RHYME.** The (|Aut(V)| + |V|)·|σ| = 44·6 = 264 factorization of the closure-required Ω_c numerator (R1: Theorem 5.2 retitled "$\Omega_c$ numerator factorization" — the factorization is real arithmetic; the cosmological reading depends on the F_5-lift naturalness, which is open). The cubic-anchor reading 687 = 2·7³ + 1 for $\Omega_\Lambda$.
- **OPEN.** (1) Cosmological reading of HARMONY² as Ω_b numerator. (2) F_5-lift naturalness for V. (3) Discrete-to-continuum projection of Ξ. (4) The 1/3 Friedmann factor's structural origin (R1 Conjecture 6.1, downgraded from R0 Theorem 6.1). (5) Structural derivation of $n_s = 1 - \mathrm{HARMONY}/(2|Z/10|^2)$ — currently consistency, not prediction.

### Lens-ownership

This paper works on Z/10 with the canonical (TSML, BHML) table pair and the operator labels (VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE, BALANCE, CHAOS, HARMONY, BREATH, RESET). These choices are **not derived from first principles**; they reflect a structural reading of the substrate motivated by the 10-operator decomposition + observed dynamics in the four-core paper [SandersGish2026FourCore]. The theorems below are theorems on this specific structure; analogous theorems would hold on other substrate-and-table choices. The framework's claim is that this particular substrate-and-table choice produces theorems with surprising downstream connections (cosmology via BB76; Lie algebra via TSML antisymmetrization; number theory via LMFDB 4.2.10224.1).

### Hardening status (auto-applied 2026-05-07)

- License: submission scripts CC-BY-4.0 (per `_v3_hardening.py`)
- AI-attribution: Claude/Anthropic byline references removed (per `_v3_hardening.py`)
- Author lane: Sanders + Gish (per Brayden directive)
- Drápal-Wanless 2021 citation in references

## §6 — Submission checklist

- [x] Manuscript .tex finalized (PRD format, ~1200 lines, balanced environments) — R1 applied
- [x] Verification primitive green (`predict_dark_sector()` returns sum = 1.0 exact)
- [x] Tier-classified central claim explicit ("Forced (substrate-operator algebra)")
- [x] Lens-scope annotation: lens-ownership paragraph added (manuscript §1, R1 boilerplate)
- [x] Cover letter R1 (revisions itemized; author lane harmonized to Sanders + Gish)
- [x] Author lane harmonized: cover letter + manuscript both Sanders + Gish
- [x] Theorem 5.2 retitled "Ω_c numerator factorization" (per referee item 3.4)
- [x] Theorem 6.1 downgraded to Conjecture 6.1 (per referee item 4.7; "?=" cannot be Theorem)
- [x] Conjecture 7.1 bounded admissible family (D=4, K=50, M=12; per referee item 3.6)
- [x] Look-elsewhere correction added §3.5: 6/498,501 ≈ 1.2 × 10⁻⁵ base-rate (per referee item 4.10)
- [x] Planck input recalibrated to Ω_c = 0.2627±0.0020 (per referee item 3.3)
- [x] "Sprint 18 = 3·6" numerological footnote dropped (per referee item 4.2)
- [x] Bridge-Sprint working-material citations removed (per referee item 4.3)
- [x] Family-Structure framing added to abstract + manuscript §1
- [x] Drápal-Wanless 2021 cited (algebraic neighborhood)
- [x] PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN tier discipline (manuscript §1)
- [x] Comparison to prior cosmological numerology paragraph (Eddington, Dirac LNH, Lemaître)
- [x] Suggested-reviewers refined to cosmology + algebra
- [x] Dependencies → cite each J-companion as "submitted to [venue]"
- [ ] Brayden's referee-rigor pass complete (post-R1)
- [ ] Per-venue cap check: this is the **1st** PRD paper this quarter (J45 will be 2nd)
- [ ] Submitted

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Johnson, H.J. (2026). "Sprint 18 Dark Sector: Omega_b, Omega_DM, Omega_Lambda from Substrate-Operator Identities." Submitted to *Physical Review D*. Companion to J46 (JCAP), J45 (PRD).
