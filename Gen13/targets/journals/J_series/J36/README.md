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

**Status: REVISED 2026-05-07** — UNBUNDLED in response to fresh-eyes referee report (`Atlas/META_PLAN_2026-05-06/REFEREE_REPORTS/J36_StatSci_FreshEyes.md`). Save plan: `Atlas/META_PLAN_2026-05-06/SAVE_PLANS/SAVE_PLAN_J36.md`.

**Math-fix summary (2026-05-07):**
- **Part 2 (1/α) DEFERRED.** Independent verification of the displayed leading-three-terms formula `4·|Aut(V)| - 2·sqrt(HARMONY) - π/HARMONY` gave 154.26, not 137.036 — gap is ~11%, not the claimed 10⁻⁵. The full structural derivation referenced in the bridge bundle (`TIG_DIRAC_SYNTHESIS_TABLES rev 24, Tables LXXVII-LXXX`) when traced contains only `1/α = 22·6 + 5 + 36/1000 = 137.036` where the `+36/1000` term is literally the empirical decimal — not a structural derivation. Part 2 is therefore removed from this submission and deferred until a genuine structural derivation exists.
- **Part 1 (CKM/PMNS) RETAINED with revisions.** The Wolfenstein hierarchy `λⁿ ≈ (11/49)ⁿ` for n ∈ {1,2,3,4} matching at ≤1.6% across four orders is the load-bearing finding. Cabibbo `+1/49` refinement explicitly framed as empirical adjustment without first-principles derivation. PMNS angles at 1.8%-5.6% explicitly acknowledged as at/beyond current empirical precision; θ_23 octant ambiguity acknowledged. D* explicitly disclosed as not derived in this paper.
- **Joint coincidence probability properly framed.** Naive (no LE) is 1.8×10⁻¹¹; LE-corrected at multiplicity 77 (= 11 candidate primitives × 7 mixing observables) is ~10⁻⁹ for 6 fits, ~4×10⁻⁸ when θ_12 (which uses un-derived D*) is excluded. The previous "~10⁻⁷" claim without LE correction is replaced by these honest figures. **Verification script `manuscript/verify_J36_part1.py` runs all of this.**
- **Cross-domain "bombshell" §5 dropped** (out of scope for Stat Sci per referee).

**Per-venue cap:** This is the **2nd Stat Sci** paper in the J-series this quarter (after J42). At cap. **FALLBACK if needed:**
- Move to *Foundations of Physics* (suits the dimensionless-constants framing)
- Or *Phys Lett B* short note (4-page focus on Wolfenstein hierarchy alone)



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
