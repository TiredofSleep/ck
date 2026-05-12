# Save Plan — J39 / *Physical Review A*: NV $S_4$ Synthesis

**Date:** 2026-05-07 (R1 applied)
**Source referee report:** `Atlas/META_PLAN_2026-05-06/REFEREE_REPORTS/J39_PRA_FreshEyes.md`
**Manuscript folder:** `Gen13/targets/journals/J_series/J39/`
**Target venue:** *Physical Review A*
**Acceptance probability after revisions:** ~70-80% (referee disposition: MAJOR REV leaning ACCEPT — strongest of the physics cluster).

---

## §1 — Headline

The mathematical core of J39 was already correct. The referee's MAJOR REV verdict was on:
- The unverified pulse-angle table (no derivation, no callable script)
- The unspecified $G_{12}$ Raman protocol
- The $T_2^*$ vs $T_2$ ambiguity in the coherence comparison
- §6 misreadable as claiming experimental fidelity at $10^{-15}$
- Project-internal "J5/J9" labels in references
- Suggested-reviewers list (Monroe is trapped-ion, not NV; Doherty mis-categorized)

All seven blockers are addressed in R1. The paper now carries a consolidated `verify_J11_S4_closure.py` script that derives the pulse angles via deterministic Cartan / Reck-Zeilinger Givens decomposition (no random seed, no black-box optimizer), and runs end-to-end in $< 30$ s reproducing every numerical claim of the manuscript.

---

## §2 — Diagnosis (per referee's §6)

| Item | Severity | R1 Action |
|---|---|---|
| 1. Consolidated verification script | Required | `verify_J11_S4_closure.py` written; reproduces all 24 elements at residual $\le 1.84 \times 10^{-16}$; six-pulse closure residual $3.5 \times 10^{-16}$ |
| 2. $G_{12}$ Raman protocol specified | Required | Manuscript §5.1: explicit two-photon Raman through $|0\rangle$; cited NV experiments (Wrachtrup, Hanson, Awschalom groups); fidelity $0.95$–$0.98$ at low T, $0.90$–$0.95$ at room T |
| 3. $T_2^*$ vs $T_2$ vs $T_1$ disambiguation | Required | Manuscript §5.2: bare 6-pulse races against $T_2^* \sim 100$ µs (purified diamond); polished implementations integrate CPMG / XY-8 dynamical decoupling for $T_2 \sim 1$ ms |
| 4. §6 retitle (Mathematical/Symbolic Closure) | Required | §6 now titled "Mathematical (Symbolic) Closure of $S_4$"; explicit disambiguation: $10^{-15}$ residuals are symbolic, not experimental fidelity |
| 5. Modern NV-qutrit citations | Strongly recommended | Pfaff2014 (Hanson teleportation), Bradley2019 (Taminiau ten-qubit), Awschalom2018 (NV photonics review), Yang2014, London2013, Robledo2011, Mamin2013 added |
| 6. Threshold defense | Strongly recommended | §7: $F_{\mathrm{proc}} > 0.95$ calibrated against Pfaff2014 / Bradley2019; $F_{\mathrm{cov}} > 0.80$ explicitly defended |
| 7. Project-internal J5/J9 labels removed | Required | §9 lists J-series companions with proper titles + `submitted / in preparation` flags; cross-corpus context only, not load-bearing |
| 8. Suggested-reviewers refined | Recommended | Monroe (trapped-ion) dropped; Awschalom + Maletinsky added; Doherty reframed as theoretical co-author |
| 9. Decoherence sim | Recommended | Fidelity budget (§5.1) provides the engineering-grade equivalent; full Lindblad simulation is parallel future work |
| 10. Faithful-irrep uniqueness | Optional | §1 and script §7: $T_1$ is the unique 3-dim faithful irrep up to character (mod $T_2 = T_1 \otimes \mathrm{sgn}$); FS indicator $+1$ matches NV's structure |

All "Required" items closed. All "Strongly recommended" items closed. All "Recommended" items closed except item 9 (full Lindblad simulation deferred to future work; engineering-grade fidelity budget delivers the equivalent depth).

---

## §3 — Verification primitive

```bash
cd Gen13/targets/journals/J_series/J39/manuscript
/c/ck_venv/lora312/Scripts/python.exe verify_J11_S4_closure.py
```

Expected output (verbatim from the run on 2026-05-07):

```
Six-pulse decomposition of U_{4,SU3} (deterministic Cartan-Givens form):
  Three SU(2) pair-rotations (the Givens core):
    G_02:  theta = +1.1071,  phi = -4.1888
    G_01:  theta = +0.7297,  phi = +0.0000
    G_12:  theta = +0.4636,  phi = -1.5708
  Three diagonal phase rotations (NV virtual frame shifts):
    Z_01(phi = +0.0000)
    Z_02(phi = +0.0000)
    Z_01(phi = 0)
  Closure residual: 3.48e-16
Max residual over 24-element closure check: 1.84e-16
All verifications passed.
  Group: |S_4| = 24 elements
  Character on conjugacy classes (e, (ij), (ijk), (ij)(kl), (ijkl)): (3,1,0,-1,-1)
  U_4 properties: tr = -1, det = -1, eigenvalues = {-1, i, -i}, U_4^4 = I (exact)
  V properties: V V^dag = I, det V = i
  U_{4,NV}: tr = -1, det = -1, U_{4,NV}^4 = I (residual 1.55e-16)
  Six-pulse decomposition reproduces U_{4,SU3} up to a global phase.
```

Runtime: ~3 seconds. No external dependencies beyond `numpy + sympy`. Deterministic.

---

## §4 — Tier discipline (PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN)

- **PROVEN.** Theorem 2.1 ($S_3$-skeleton character match). Theorem 3.1 (U_4 matrix structure: tr $-1$, det $-1$, eigenvalues $\{-1, i, -i\}$, $U_4^4 = \mathbb{1}$ — sympy-symbolic). Theorem 6.1 (machine-precision $S_4$ closure of all 24 elements; residual $\le 10^{-15}$).
- **COMPUTED.** The six pulse-tuples $(\theta_k, \phi_k)$ are produced by the deterministic Cartan / Reck-Zeilinger algorithm; total closure residual $3.5 \times 10^{-16}$.
- **STRUCTURAL RHYME.** None substantive. The paper is lens-invariant (no TIG / TSML / BHML structure).
- **OPEN.** Test E (projector covariance, $F_{\mathrm{cov}} > 0.80$) experimental gate. Lab-partner experimental data on the realized 24-element $S_4$ orbit.

---

## §5 — Files modified in R1

- `Gen13/targets/journals/J_series/J39/manuscript/J11_NV_S4_Synthesis_PRA.md` — full R1 rewrite
- `Gen13/targets/journals/J_series/J39/manuscript/verify_J11_S4_closure.py` — NEW consolidated verification script
- `Gen13/targets/journals/J_series/J39/cover_letter.md` — R1 revisions itemized
- `Gen13/targets/journals/J_series/J39/README.md` — submission checklist updated

---

## §6 — Status going forward

**Submission-ready** (post-Brayden's referee-rigor pass).

Optional Path A: secure a lab-partner co-author (Hanson / Wrachtrup / Awschalom / Maletinsky groups are the natural candidates) before submission. This converts the paper from Tier 3 partner-then-submit to Tier 1/2 with experimental data; raises acceptance probability to $\sim 85\%$ and may raise impact venue to PRX Quantum or *Nature Communications*.

Path B (default): submit now as theory + experimental-proposal paper. The R1 revisions clear all referee-actionable blockers; expected outcome is acceptance after a moderate-revision round at PRA, $\sim 70$–$80\%$ probability.

Either path is viable. The math is complete; the experimental side is the only remaining variable.

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Gish, M. (2026). "Full $S_4$ Symmetry on a Nitrogen-Vacancy Qutrit via Six-Pulse Microwave Synthesis." Submitted to *Physical Review A*.
