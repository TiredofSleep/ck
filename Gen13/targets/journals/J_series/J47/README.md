# J47 — Freezing-Quintessence Letter: A Two-Parameter $w(z)$ Profile

**Status:** DEPENDS_ON_J03
**Phase:** Phase 5
**Target venue:** Physics Letters B (Letter format, ~4 pages)
**Author lane:** Sanders + Gish
**Tier:** B (contingent on J46 v4)
**WP source:** Letter-format extraction of J46 (`paper1_freeze_thaw_v3.tex`)

---

## §1 — Manuscript

**Local path:** `manuscript/J16_FreezingQuintessence_Letter_PLB.md`

**Abstract (one paragraph).** A real positive dimensionless scalar $\Xi$ with $V(\Xi) = \Lambda^4 \Xi \log \Xi$ has analytic vacuum $\Xi_0 = e^{-1}$, fluctuation mass $m_\Xi^2 = \Lambda^4 e/M_{\rm Pl}^2$, and (with $m_\Xi \sim H_0$) $\Lambda \approx 1.7$ meV. The FRW trajectory with outbound IC at $z_i \approx 20$ is dual-regime: thawing outbound, frozen turnaround at $z_\star$, asymptotic refreeze toward $\Xi_0$. Observational signature: non-monotone $w_{\rm DE}(z)$ with a local minimum near $-1$ at intermediate $z$ — falsification criterion (F5). Two-parameter $w(z)$ profile consistent with DESI 2024 DR1 $(w_0, w_a)$ Gaussian summary.

**Source corpus:** Letter is extracted from `Gen13/sprint_bundle_2026-05-07_v36_SEEDS_BUNDLE/tig_2026-05-07_bundle/seeds_for_submission/paper1_freeze_thaw_v3.tex` (the J46 full version).

**Letter structure:** ~4 pages, sections (1) Model, (2) Dual-regime trajectory, (3) Two-parameter $w(z)$ profile, (4) Falsification (F1-F5), (5) Status / scope / J-series context.

## §2 — Verification script

**Path:** Same as J46 — `compute_zstar_v3.py` (or `compute_zstar_v4.py` once J46 reconciles). Runs `numpy + scipy` on a standard laptop in under 5 minutes. DOI: 10.5281/zenodo.18852047.

## §3 — Dependencies (J-papers cited as already-submitted companions)

J46 (the FULL companion paper this letter extracts from), J01, J02, J40.

## §4 — Cover letter

See `cover_letter.md` in this folder. Drafted; submission timing **HELD** pending J46 reconciliation.

## §5 — Notes & Status

**Status: DEPENDS_ON_J03 (manuscript drafted with J46-RECONCILE placeholders; HELD pending J46 v4 numerics).**

### Why J47 is HELD

J46 (companion full paper, target JCAP) currently has a CRITICAL numerical reconciliation issue flagged by the JCAP referee (May 2026): the v3 paper's claims about $z_\star \approx 1.3$ at the stated initial conditions (Eq. 31) were not reproducible from the supplied scripts; referee-independent execution gave $z_\star \approx 2.131$. The Abstract/body/$\chi^2$ values are also internally inconsistent in v3.

**J46 is currently being reconciled by a separate agent.** Until J46 lands its v4 with internally consistent numbers, J47 cannot lock its numerical claims (since J47 is the letter extraction of J46 — same model, same fit, same falsification criteria).

### What this means operationally

- Manuscript draft is in place at `manuscript/J16_FreezingQuintessence_Letter_PLB.md` with `[J46-RECONCILE]` placeholders for: $z_\star$, $w(z=0)$, $\chi^2$, $(w_0, w_a)$ values, $\Lambda$ (the latter is robust at $\approx 1.7$ meV but listed for completeness).
- The structural content (the action, the analytic vacuum at $\Xi_0 = e^{-1}$, the dual-regime classification, the five falsification criteria) is *not* in flux and is locked.
- Once J46 v4 lands, J47 swaps in the reconciled numerical values and ships within hours.
- Tier: **B / Tier 2 contingent on J46**. Action and analytic vacuum are exact theorems; trajectory is a numerical claim conditional on J46 reconciliation.

### Per-venue cap

**1st PLB submission** in the J-series — no cap conflict.

## §6 — Submission checklist

- [x] Manuscript .md drafted (PLB Letter format, ~4 pages)
- [ ] LaTeX (revtex4) conversion pending
- [ ] **J46 reconciliation pending** — verification script and numerical claims swap-in upon J46 v4
- [x] Tier-classified central claim explicit (Tier 2 contingent on J46)
- [x] Lens-scope annotation: lens-invariant
- [x] Cover letter drafted (with status note about J46 dependency, suggested reviewers)
- [ ] Dependencies → cite J01, J02, J46, J40 as "submitted to [venue]"
- [ ] J46 v4 lands
- [ ] Brayden's referee-rigor pass complete
- [x] Per-venue cap check: 1st PLB, no conflict
- [ ] Submitted (HELD until J46 reconciles)

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Gish, M., Johnson, H.J. (2026). "Freezing-Quintessence Letter: A Two-Parameter $w(z)$ Profile from a Logarithmic Potential." Submitted to *Physics Letters B* (HELD pending J46 reconciliation).
