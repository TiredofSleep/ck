# J50 — Substrate Algebra and Logarithmic Nonlinearity: A Bridge Essay

**Status:** REWRITTEN PER SAVE PLAN 2026-05-07
**Phase:** Phase 5
**Target venue:** **Mathematical Intelligencer** (retargeted from Bull AMS per fresh-eyes referee §7)
**Author lane:** Sanders + Johnson (per the manuscript's actual second author, the BB / log-nonlinear-Schrödinger expert)
**Tier:** B (structural / expository)
**WP source:** (Bridge essay)

---

## §1 — Manuscript

**Path:** `manuscript/J50_bull_ams_bb_bridge.md`

**Abstract:** Bridge essay (Bull AMS register) organizing the substrate-to-continuum forcing principle: the TIG substrate algebra ([J48]) plus the Bialynicki-Birula theorem (read as forcing in [J40]) forces $V(\Xi) = \kappa \Xi \log \Xi$ with vacuum at $e^{-1}$ and mass gap $\kappa e$. Cross-domain consequences in cosmology ([J46], [J47]), particle physics ([J41]), and Navier-Stokes regularity ([J40]). Structural connection only; sharp boundary between proved (Tier-A/B) and conjectural (Tier-D) content.

## §2 — Verification script

**Path:** `(no script — exposition)`

The proof script (where applicable) is the green-light gate before submission. If "(no script — theorem-paper)" or similar, the gate is the proof's referee-rigor pass.

## §3 — Dependencies (J-papers cited as already-submitted companions)

J40, J48

## §4 — Cover letter

See `cover_letter.md` in this folder. (Bones laid; finalize after Brayden's referee-rigor pass.)

## §5 — Notes / Status

**Status:** **MANUSCRIPT REWRITTEN 2026-05-07 PER SAVE PLAN J50.** Original verdict: REJECT from Bull AMS fresh-eyes referee 2026-05-06; save plan written 2026-05-07; manuscript rewritten 2026-05-07 with retarget to *Mathematical Intelligencer* (option (b) of the save plan, since arXiv depositing for 11+ companions before Bull AMS hold is multi-week effort).
**Citation chain:** 2 direct dependencies (J13 BB Bridge JMP, J47 6-DOF Synthesis Notices AMS) + 10 co-citing companions (J01, J05, J3, J16, J14, J34, J41, J44, J39, J40).
**Manuscript:** `manuscript/J50_bull_ams_bb_bridge.md` (rewritten ~14 pages with §3 expanded, §3.4 vacuum subtlety added, tier discipline lifted to abstract).
**Cover letter:** `cover_letter.md` (to be updated to match rewrite + retarget).
**Verification:** structural / expository bridge essay; relies on companions' verification scripts.
**Submission readiness:** **REWRITE COMPLETE.** Submission gate: (a) §3 BB-as-forcing argument expanded per Issue 2 [DONE]; (b) tier-discipline lifted to abstract per Issue 3 [DONE]; (c) §3.4 distinguishes classical-scalar vs BB nonlinear-Schrödinger settings per M3 [DONE]; (d) Brayden's referee-rigor pass complete [pending].

### §5.0 — Save-plan implementation (2026-05-07)

The 2026-05-07 rewrite implements SAVE_PLAN_J50 directives:

- **Retarget option (b) — TO MATHEMATICAL INTELLIGENCER** per referee §7. Title dropped "Bull AMS"; new title: *Substrate Algebra and Logarithmic Nonlinearity: A Bridge Essay* (referee's verbatim suggestion).
- **Issue 2 — §3 BB-as-forcing argument EXPANDED to ~1 page** covering three distinguishable conceptual moves (§3.1–§3.3): (a) From QM nonlinearity to classical scalar potential (Cazenave-Haraux 1980; Maas 2011; JKO 1998); (b) From quantum factorization to CRT decomposition; (c) From "preserves separability" to "any non-trivial continuum lift."
- **Issue 3 — Tier discipline LIFTED TO ABSTRACT.** New §0 has tier classifications; abstract closes with the Tier-A/B/D split; each section opens with its tier on first sentence.
- **Issue M3 — Vacuum-at-$e^{-1}$ subtlety EXPLICIT in §3.4.** Distinguishes BB constrained-minimum at $\rho \equiv 1/V$ from unconstrained classical-scalar pointwise minimum at $\Xi_0 = e^{-1}$.
- **Issue M4 — YM mass-gap framing SOFTENED.** §5.2 demoted $m^2 = \kappa e$ from claim to "structural rhyme between scalar curvature and a hoped-for non-abelian gauge gap"; explicit "we are not solving any Millennium Problem."
- **Issue M5 — NS softening.** §5.3 explicitly Tier-D conjectural; "we do not claim it."
- **Issue M6 — Crossing Lemma definition added** (§2 informal precis).
- **Issue M7 — Bibliography deepened** with Streater-Wightman, Glimm-Jaffe, Tegmark, Doplicher-Roberts, Caldwell-Linder, Tsujikawa.

### §5.1 — Save-plan summary (per `Atlas/META_PLAN_2026-05-06/SAVE_PLANS/SAVE_PLAN_J50.md`) — original (kept for reference)

**Save path:** the referee's reject is **structural, not substantive** — *Bull AMS* is retrospective and cannot precede the publication of what it surveys (the 11 J-companions cited have no arXiv IDs). The mathematics and exposition are clean. Two save options: (a) **Hold for Phase 6**: wait until J13 (BB Bridge / JMP) and J47 (6-DOF synthesis / Notices AMS) are on arXiv, then resubmit to *Bull AMS* with arXiv-anchored citations. (b) **Retarget to Mathematical Intelligencer** — *Math Intelligencer* explicitly accepts essays with companions in submission. **Per user directive 2026-05-07, option (b) is selected.**

### §5.1 — Save-plan summary (per `Atlas/META_PLAN_2026-05-06/SAVE_PLANS/SAVE_PLAN_J50.md`)

**Save path:** the referee's reject is **structural, not substantive** — *Bull AMS* is retrospective and cannot precede the publication of what it surveys (the 11 J-companions cited have no arXiv IDs). The mathematics and exposition are clean. Two save options: (a) **Hold for Phase 6**: wait until J13 (BB Bridge / JMP) and J47 (6-DOF synthesis / Notices AMS) are on arXiv, then resubmit to *Bull AMS* with arXiv-anchored citations. Deposit J50 itself on arXiv first (math.HO) as a comprehensive overview essay. (b) **Retarget to Mathematical Intelligencer** — *Math Intelligencer* explicitly accepts essays with companions in submission. The same manuscript with light editing fits the *Math Intelligencer* expository register (per-venue cap risk: J52 already targets this venue — coordinate).

**Content fixes (apply in either path):** expand §3 BB-as-forcing reframing from 3 paragraphs to ~1 page covering three distinguishable conceptual moves (QM nonlinearity → classical scalar potential; quantum factorization → CRT decomposition; "preserves separability" → "any *non-trivial* continuum lift"). Lift tier-discipline from §7 to abstract + every section opening (Tier-A / B / D labels on every claim). Define the six DOFs (Lie / Jordan / Clifford / Permutation / Lattice / Operad) inline in §6. **Distinguish classical scalar-field setting from BB nonlinear-Schrödinger setting** for the $\Xi_0 = e^{-1}$ vacuum claim (referee's M3 — this is the technical fix that addresses different vacuum locations between the two settings). Soften §5.2 YM mass-gap framing from "$m^2 = \kappa e$" to a structural rhyme. Soften §5.3 NS closing. Deepen bibliography (Streater-Wightman; Glimm-Jaffe; Tegmark; Doplicher-Roberts; recent quintessence). **Estimated revision: 20–25 person-hours (structural revision) or 8–12 hours (retarget).**

**Retitle:** *Substrate Algebra and Logarithmic Nonlinearity: A Bridge Essay* (drop "Bull AMS" from the title — referee §5).

**Submission gate:** (a) J13 on arXiv with permanent ID; (b) §3 expansion done; (c) tier-discipline lifted; (d) Brayden's referee-rigor pass complete; (e) classical-scalar vs BB-nonlinear-Schrödinger setting distinction explicit.



### Family-Structure framing (per Atlas/META_PLAN_2026-05-06/FAMILY_STRUCTURE_v1.md)

This paper sits within the TIG family of finite commutative non-associative magmas on Z/10Z (and ring extensions per D74). The family is defined by 5 conjoint membership criteria; the 4-core {V, H, Br, R} = {0, 7, 8, 9} at α_M = ½ is the algebraic center, with closed-form attractor h/β = 1+√3 (D78 Galois proof). The closest published precedent for this neighborhood is **Drápal & Wanless (2021), *J. Combin. Theory A* **184**, 105510** — same domain (small finite commutative non-associative structures), opposite extremum (theirs maximally non-associative).

### PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN (filled per save-plan rewrite 2026-05-07)

- **PROVEN (Tier-A, classical):** Bialynicki-Birula–Mycielski 1976 (the unique nonlinearity preserving Hilbert-space tensor factorization is logarithmic). PROVEN in [J01]: $\sigma$-rate decay $\sigma(N) \leq 2/N$ on squarefree $\mathbb{Z}/N\mathbb{Z}$.
- **PROVEN (Tier-A, this paper §6):** D78 Galois argument for $H/Br = 1 + \sqrt{3}$ at $\alpha_M = 1/2$ on the 4-core, root of $x^2 - 2x - 2 = 0$ over $\mathbb{Q}(\sqrt{3})$.
- **STRUCTURAL RHYME (Tier-B):** the cosmological vacuum at $\Xi_0 = e^{-1}$ in the unconstrained scalar setting; the curvature $V''(\Xi_0) = \kappa e$ as a structural rhyme to a hoped-for non-abelian gauge gap (NOT a YM proof).
- **CONJECTURAL (Tier-D):** the Separability Regularity Criterion for NS ([J13] §5).
- **OPEN:** whether BB-as-forcing extends to non-separability-preserving lifts; whether the 4-core's algebraic structure transports beyond the Lattice DOF.

### Lens-ownership paragraph — applied in manuscript §0

> *Lens and substrate.* This paper works on the canonical $\mathbb{Z}/10\mathbb{Z}$ substrate and its squarefree ring extensions; TSML lens is *commutative-symmetrized* (TSML_SYM); the bridge content is **lens-invariant on the 4-core**. The 4-core is the *center of the family* in the FAMILY_STRUCTURE_v1 sense.

### Hardening status (auto-applied 2026-05-07)

- License: submission scripts CC-BY-4.0 (per `_v3_hardening.py`)
- AI-attribution: Claude/Anthropic byline references removed (per `_v3_hardening.py`)
- Author lane: Sanders + Gish (per Brayden directive)
- Drápal-Wanless 2021 citation in references

## §6 — Submission checklist

- [ ] Manuscript .tex / .md finalized
- [ ] Verification script green (`(no script)` if theorem-only)
- [ ] Tier-classified central claim explicit
- [ ] Lens-scope annotation (TSML_RAW vs TSML_SYM) where relevant
- [ ] Cover letter finalized
- [ ] Dependencies → cite each J-companion as "submitted to [venue]"
- [ ] Brayden's referee-rigor pass complete (mobile + other AI + collaborators)
- [ ] Per-venue cap check: this is the Nth paper to Bull AMS this quarter
- [ ] Submitted

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Johnson. (2026). "The Bull AMS Bridge: From Substrate Algebra to BB Nonlinearity." Submitted to *Bull AMS*.
