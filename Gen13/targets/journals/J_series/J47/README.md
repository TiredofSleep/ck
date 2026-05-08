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

**Status: SAVE_PLAN_PENDING + DEPENDS_ON_J46 (2026-05-07).** Referee verdict (`Atlas/META_PLAN_2026-05-06/REFEREE_REPORTS/J47_PLB_FreshEyes.md`): MAJOR REV pre-submission; CONDITIONAL ACCEPT after Sequence A applied and J46 v4 reconciled. Save plan landed at `Atlas/META_PLAN_2026-05-06/SAVE_PLANS/SAVE_PLAN_J47.md`.

**Save-plan summary.** The load-bearing content — dual-regime $w(z)$ trajectory with (F5) Stage-IV falsification handle from a $\Xi \log \Xi$ potential — is genuinely letter-shaped, novel, and surveyable. The save path is package cleanup + J46 wait: (a) wait for J46 v4 reconciliation (Layer-3a strict-postulate per `BBM_IC_DERIVATION_v2.md`: $z_\star = 2.31$, $\chi^2 = 1.53$, $(\Xi_i, \Xi'_i) = ((1+\sqrt{3})/e, 1/e)$); (b) strip `[J46-RECONCILE]` placeholder markup from manuscript body; (c) strip the "Status note (read first)" block from manuscript head (move to cover letter only); (d) resolve J03 vs J46 cross-reference label inconsistency — pick **J46** consistently across manuscript / cover letter / README; (e) replace wrong file at `manuscript/manuscript.tex` (currently J23 Discrete Dirac content) with REVTeX-letter version of the actual letter; (f) rename `J16_FreezingQuintessence_Letter_PLB.md` to `J47_FreezingQuintessence_Letter_PLB.md`; (g) convert to REVTeX-letter format; (h) add Figure 1: $w(z)$ overlay on DESI 2024 DR1 Gaussian; (i) add one-sentence distinction from logotropic dark energy (Tsujikawa-Sami 2007, Ferreira-Avelino 2018) — uses $V \propto \Xi \log \Xi$ in field, not $V \propto -A \log(\rho/\rho_*)$ in energy density; (j) add one-sentence distinction from Albrecht-Skordis 2000 — dual-regime T → F → A vs tracking → freezing; (k) tighten F1–F4 language ("consistency checks" / "model fingerprints," reserve "falsification" for F5); (l) deposit J46, J01, J02 on arXiv before submission; cite by arXiv ID. Structural content (action, analytic vacuum at $\Xi_0 = e^{-1}$, dual-regime classification, F5 signature) is locked.

**Recommended retitle / retarget:** Option A (preferred — keep PLB target, ship after J46 v4 + Sequence A cleanup; title can stay or sharpen to *"Dual-Regime Quintessence from $V(\Xi) = \Lambda^4 \Xi \log \Xi$: A Letter"* / *"A Non-Monotone $w_{\rm DE}(z)$ Signature from a Logarithmic Quintessence Potential"*; survival probability moderate-to-good). Option C (PRL) not recommended due to content-overlap-with-J46 risk. Don't pursue PRL until after PLB outcome.

**Revision time:** 1–2 weeks AFTER J46 v4 lands.

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
