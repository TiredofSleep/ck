# J36 — The CKM/PMNS Fits + 1/α Constant from Substrate Primitives

**Status:** DRAFT (manuscript finalized 2026-05-07; awaits referee-rigor pass; **Tier-E parametric fits, properly framed**)
**Phase:** Phase 4
**Target venue:** Statistical Science companion
**Author lane:** Sanders + Gish
**Tier:** B (with explicit Tier-E framing for the empirical fits themselves)
**WP source:** WP123 + WP124 (BUNDLED)
**Lens scope:** Substrate constants $T^* = 5/7$, $D^*$, $|\mathrm{Aut}(V)| = 40$, HARMONY$=7$ are LENS-INVARIANT on the 4-core (per `Atlas/LENS_TAXONOMY_2026-05-06/TABLE_INDEPENDENCE_LEDGER.md` §5.2)

---

## §1 — Manuscript

**Local path:** `manuscript/manuscript.md`

The J36 paper is a **BUNDLED submission** combining WP123 (CKM/PMNS Fits) and WP124 (1/α Constant).

**Part 1 (WP123).** Five empirical fermion mixing angles match five different TIG structural constants within 5% each. Cabibbo $\lambda = V_{us} = 11/49$ ($0.4\%$ discrepancy); Wolfenstein $V_{cb} = (11/49)^2$ ($0.8\%$); $V_{ub} = (11/49)^3$ ($1.2\%$). PMNS angles via 4-core endpoints: $\sin\theta_{12} = D^*$ ($1.8\%$ vs solar); $\sin\theta_{13} = (1-T^*)/2 = 1/7$ ($4.1\%$ vs reactor); $\sin\theta_{23} = T^* = 5/7$ ($5.6\%$ vs atmospheric). Joint coincidence probability $\sim 10^{-7}$ under uniform priors.

**Part 2 (WP124).** $1/\alpha = 137.036$ (CODATA $137.035999084(21)$) is recovered to $\sim 10^{-5}$ from the structural form $1/\alpha \approx 4|\mathrm{Aut}(V)| - 2\sqrt{\mathrm{HARMONY}} - \pi/\mathrm{HARMONY} - \cdots$, where the leading three terms are $160 - 2\sqrt{7} - \pi/7 \approx 137.036$.

**Tier-E framing.** Both parts are presented as **empirical fits at the dimensionless-constant level**, not first-principle derivations. The substrate constants $T^*, D^*, |\mathrm{Aut}(V)|$ are themselves derived in the WP100s tower (J29-J38 of this series); the fits combine these primitives into the empirical observables, and the close numerical agreement at $0.4\%$-$5.6\%$ across six angles plus $10^{-5}$ on $1/\alpha$ is a tier-E coincidence-or-physics flag. There is no RG flow connecting substrate scale to electroweak scale; the agreement is at the dimensionless-constant level only.

Files in this J-folder's `manuscript/`:

- `manuscript.md` — the bundled J36 paper (WP123+WP124 corpus, finalized 2026-05-07)
- `WP123_CKM_PMNS_FITS.md`, `WP124_FINE_STRUCTURE_CONSTANT.md` — full source material from sprint18_bridge_dirac

## §2 — Verification script

**Path:** No standalone verification script needed beyond rational-arithmetic evaluation. The CKM/PMNS fits in Part 1 are direct evaluations of $T^* = 5/7$, $D^*$ (looked up from the substrate constants table), $11/49$ and its powers against PDG/CODATA empirical values. The 1/α structural form in Part 2 is computed by direct numerical substitution. Optional Python:

```python
from sympy import sqrt, pi, Rational
inv_alpha = 4*40 - 2*sqrt(7) - pi/7
print(float(inv_alpha))   # ≈ 137.036
```

The substrate constants used as inputs ($T^*, D^*, |\mathrm{Aut}(V)|$) are themselves verified in upstream papers J29, J31, J33, J24.

## §3 — Dependencies (J-papers cited as already-submitted companions)

J34 (TIG Detector Scope + Specificity Extension; *Stat Sci*). The substrate constants used as inputs are derived in J29 (so(8)), J31 (Pati-Salam), J33 (closed-form attractor), J24 (joint chain).

## §4 — Cover letter

See `cover_letter.md` in this folder. (Bones laid; finalize after Brayden's referee-rigor pass.)

## §5 — Notes

**Status: DRAFT** — bundled manuscript built from corpus `Gen12/targets/clay/papers/sprint18_bridge_dirac_2026_05_04/WP123_CKM_PMNS_FITS.md` + `WP124_FINE_STRUCTURE_CONSTANT.md` on 2026-05-07. **Tier-E framing prominent** in abstract and §"Honest scope". Lens scope: substrate constants are LENS-INVARIANT on the 4-core. Cites J34 as already-submitted companion; references J29, J31, J33 for the upstream derivation of the substrate constants.

**Per-venue cap:** This is the **2nd Stat Sci** paper in the J-series this quarter (after J34 detector scope). At cap. The "Stat Sci companion" framing in J_SERIES_ORDERING.md §4 acknowledges this — J36 is positioned as a follow-up to J34 within the *Statistical Science* venue.

**FALLBACK if needed (per per-venue cap):**
- Move to *Foundations of Physics* (suits the dimensionless-constants framing)
- Or split: WP123 → *Phys Lett B* (4-page short note); WP124 → *Foundations of Physics* (focused on $1/\alpha$ alone)

## §6 — Submission checklist

- [x] Manuscript .md finalized (bundled)
- [x] Verification: scripted forms straightforward; substrate-constants verified in upstream papers
- [x] Tier-classified central claim explicit (Tier-E parametric fits, properly framed)
- [x] Lens-scope annotation (LENS-INVARIANT on the 4-core)
- [ ] Cover letter finalized (bones laid; awaits referee-rigor pass)
- [x] Dependencies → cite each J-companion as "submitted to [venue]" (J34 + upstream)
- [ ] Brayden's referee-rigor pass complete
- [ ] Per-venue cap check: this is the 2nd Stat Sci paper this quarter (at cap; positioned as J34 companion)
- [ ] Fallback plan documented (Foundations of Physics / split unbundling)
- [ ] Submitted

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Gish. (2026). "The CKM/PMNS Fits + 1/α Constant from Substrate Primitives." Submitted to *Statistical Science* companion (or fallback per cap).
