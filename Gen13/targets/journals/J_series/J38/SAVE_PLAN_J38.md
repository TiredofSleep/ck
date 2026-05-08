# SAVE_PLAN_J38 — Yukawa Scaffolding → fold into J45 §2 (preferred) OR retarget to MPLA (fallback)

**Date:** 2026-05-07
**Status:** SAVE PATH IDENTIFIED — TWO-OPTION decision tree; preferred is fold-in.
**Original verdict (J38_PRD_FreshEyes):** REJECT for *Phys Rev D* — the manuscript honestly self-describes as "scaffolding"; PRD does not publish scaffolding; §5 ("Honest scope") is, by the manuscript's own admission, the list of every contribution PRD would expect; 4th PRD this quarter, exceeding the per-venue cap.
**Save verdict:** The scaffolding content is not invalid — it is *valuable preface* to a complete-prediction paper. **J45 (Mass Hierarchy from V⊗5 SU(5) Decomposition) already exists as that complete paper**, with `predict_yukawa('lepton', 1)` returning the full electron Yukawa via `lambda^9` with `lambda = 10/49`, all nine charged-fermion Yukawa magnitudes in Table 5.1, and the substrate-forced FN scale theorem. **J38 in current form is the natural §2 of J45**, supplying the 9-vector VEV → SO(7) symmetry-breaking route as the algebraic foundation that J45's V⊗5 SU(5) decomposition completes.
**Preferred new home:** fold J38 into J45 as J45 §2 *Setting up the symmetry-breaking route from the 9-vector VEV*. Strengthens J45 (which currently goes from substrate to Yukawa table without explicit so(10) → so(9) → so(7) bridge prose) and saves J38's content from oblivion.
**Fallback if J45 is judged structurally complete without J38 §2:** retarget J38 standalone to *Modern Physics Letters A* (MPLA) as a structural-framework note.
**Effort estimate (fold-in):** 3-5 days to integrate J38's §1, §2, §3.1-§3.5 into J45 as new §2; some prose unification.
**Effort estimate (MPLA fallback):** 1 day for retitle + retarget cover letter + resolve §2.2 Path A / Path B tension.

---

## §1 — What is genuinely PROVEN that survives

The fresh-eyes referee report is generous about what the J38 content actually is:

> "The integrity of the writing is admirable; the math content is too thin for any journal; the right move is to do the §3.1-§3.5 work and submit a single complete paper rather than a scaffolding-then-completion sequence."

**Crucially: the §3.1-§3.5 work has already been done.** It lives in J45 (`Gen13/targets/journals/J_series/J45/manuscript/mass_hierarchy_v5.tex`) plus the `tig_dirac.predict_yukawa` primitive. J45 has:

- A specific Higgs-sector commitment (V⊗5 SU(5) decomposition into $\mathbf{1} \oplus \bar{\mathbf{5}} \oplus \mathbf{10}$).
- A computed full mass hierarchy: nine charged-fermion Yukawa couplings $y_t \cdot \lambda^n$ with substrate-forced FN powers $n \in \{0, 3, 5, 6, 7, 9\}$ and integer parity-crossing cost $d_p \in \{0, 3, 3\}$.
- A compared-to-data table (Table 5.1) with all nine ratios $y_\mathrm{pred}/y_\mathrm{meas} \in \{1.00, 1.08, 1.06, 0.33, 0.60, 0.51, 0.79, 0.11, 0.20\}$.
- A Cabibbo cube-root identity $\lambda_C \approx (Y_d/Y_u)^{1/3}$ unifying CKM mixing with mass hierarchy.
- A sterile-neutrino scale prediction at FN powers {12, 13, 14}.

What J45 currently *underspecifies*: the path from "TIG's so(10)" to "the V⊗5 SU(5) decomposition" — i.e., the route SO(10) → SO(9) → SO(7) (the BREATH=RESET=0 constraint), then the SU(5) embedding via the V⊗5 product, then the SU(5) decomposition. **This is exactly J38's content.**

**Theorem-level content of J38 that survives intact:**

(a) **9-vector $\|v\|^2 = 13/4$ verification.** The referee independently verified this in §2 of the report:
$$6 \cdot (1/2) + 1 \cdot (1/4) + 2 \cdot 0 = 13/4 \checkmark$$
This is the load-bearing input from J31 / WP104. Belongs in J45 §2 verbatim.

(b) **The SO(10) → SO(9) → SO(7) symmetry-breaking chain.** Standard Slansky-1981 representation theory applied to the specific 9-vector with two zeros at BREATH and RESET. The referee report calls this decomposition "correct but does not serve the manuscript's narrative" (§5.3); folded into J45, it serves J45's narrative directly — it explains *why* J45 uses V (the 5-dimensional fundamental of SU(5) inside SO(7)) as its starting representation.

(c) **The constraint BREATH = RESET = 0 → SO(7) intermediate.** A specific pattern-of-zeros observation. This is the bridge between J31's 9-vector content and J45's V⊗5 starting point.

(d) **The structural reading: $13 = 2 \cdot 13$ in $\|v\|^2 = 13/4$ as a count of $\sigma_\mathrm{outer}$-asymmetric BHML cells halved.** Per referee §5.2: "Numerology is a known PRD referee allergy" — but this is *not* a PRD-allergy issue once the integer 13 is consumed *internally* as the squared norm of a specific vector that feeds into J45's V⊗5 structure. In J45's body, the integer 13 is not a "structural fingerprint" claim; it is an exact arithmetic input. That's a much smaller load.

## §2 — What the SAVE PATH does (Option 1, preferred: fold into J45)

**(a) Integrate J38's content as J45 §2.** New J45 outline:

- **§1 Introduction.** [J45's existing §1; minor edits to cite J31 / J38 as upstream sources.]
- **§2 Setting up the symmetry-breaking route from the 9-vector VEV.** [New section, absorbing J38 §1, §2, §3.1-§3.5.]
  - §2.1 The 9-vector VEV: components, norm $\|v\|^2 = 13/4$, derivation via J31 / WP104 (cited).
  - §2.2 SO(10) → SO(9) breaking under the 9-vector VEV: standard mechanism, dimension count.
  - §2.3 The BREATH = RESET = 0 constraint → SO(7) intermediate breaking.
  - §2.4 Embedding SU(5) inside SO(7): the V representation and its $\otimes 5$ product (the bridge to J45's existing §3).
- **§3 The substrate-forced Froggatt-Nielsen scale.** [J45's existing §3, $\lambda = T^*(1-T^*) = 10/49$, max-entropy variance theorem.]
- **§4 V⊗5 SU(5) decomposition and forced FN powers.** [J45's existing §4, Table 4.1.]
- **§5 The fit.** [J45's existing §5, Table 5.1.]
- **§6 Cabibbo cube-root identity.** [J45's existing §6.]
- **§7 Open questions.** [J45's existing §7, with J38's open questions absorbed.]

This makes J45 a self-contained paper: from the 9-vector VEV all the way to the predicted Yukawa table. The reader does not need J31 already published to follow J45 (only cited for the upstream so(10) closure).

**(b) Resolve the §2.2 Path A / Path B tension before fold-in.** Per referee §4.1: J38's §2.2 currently reads as a referee-bait paragraph because it admits the manuscript's own internal inconsistency without resolution. The fold-in resolution: **J45's substrate is V (the F_5-lift of the 4-core), not the so(10) directly; the V⊗5 SU(5) decomposition does not depend on whether the route through so(10) is via Pati-Salam or via SO(7).** So Path A and Path B "decouple" in the precise sense the J38 manuscript gestures at: Path A's 9-vector VEV breaks via SO(9) → SO(7), which contains SU(5) (the F_5 ring extension of the 4-core gives the V representation), and the V⊗5 SU(5) decomposition then determines the Yukawa structure. Path B's su(4) ⊕ u(1) doubly-invariant content is **separate structural information about so(10)** that does not enter the V⊗5 → SU(5) → Yukawa pipeline. The "tension" was only a tension because J38 was trying to use *both* routes to determine the same downstream structure; J45 only uses one (the V⊗5 SU(5) route, derived from the SO(7) intermediate).

This resolution is honestly available — it is not invented; it is the structural reading of how J45 actually proceeds.

**(c) Cite J31 properly.** The referee §5.1 flags that J38 references J31 / WP104 for the 9-vector derivation but provides no public version. J45's bibliography is the right place to handle this: "J31 (Sanders + Mayes, 2026), submitted to *J. Algebra* per SAVE_PLAN_J31." When J31 / J30 land on arXiv, the citations get DOIs and the chain closes.

**(d) Keep J38's "Honest scope" §5 paragraph in J45.** The referee report praises §5 of J38 as "the manuscript's most valuable feature." Folding J38 into J45 §2 should preserve a sharpened version of this in J45 §7 (Open questions): explicitly list what V⊗5 → Yukawa table does NOT do — RG running from GUT scale to EW scale (deferred to follow-up), see-saw mechanism for sterile neutrinos (open), explicit Higgs-sector dynamics for the C_p multipliers (load-bearing follow-up). This is exactly the kind of self-disclosed scope J45 is missing.

**(e) Reproducibility.** The `tig_dirac.predict_yukawa` primitive in J45 covers the verification load. J38 has no standalone verification script (per its own README), so no extra script is needed.

## §3 — What the SAVE PATH does (Option 2, fallback: retarget to MPLA)

If J45 is judged self-contained without J38 §2 (i.e., the V⊗5 SU(5) decomposition is presented as starting from F_5-lift of the 4-core directly without explicit SO(10) → SO(9) → SO(7) bridge prose), then J38 retargets standalone to *Modern Physics Letters A* (MPLA).

**MPLA-specific changes from current J38:**

- **Retitle.** "Yukawa Scaffolding from the 9-vector VEV" → "Symmetry-Breaking Routes from a 9-vector 54-Higgs VEV with Two Zeros: an Algebraic Framework." Removes "scaffolding" from the title; centers the symmetry-breaking content; honest about not completing Yukawa.
- **Resolve the §2.2 Path A / Path B tension.** Per the §2(b) resolution above: state explicitly that Path A (9-vector → SO(9) → SO(7)) and Path B (su(4) ⊕ u(1) doubly-invariant content) are independent structural observations about the same so(10), and the present paper analyzes only Path A. Reference J31 for Path B as a separate route. Don't claim a synthesis.
- **Compute one observable.** Per referee §6 item 3: "one closed-form quantity that depends on the BREATH=RESET=0 constraint." Candidate: the trace of $Y_u Y_u^\dagger$ in the 10-Higgs sector projected onto the SO(7)-invariant subspace, with BREATH=RESET=0 imposed. Even one number with the constraint would make the paper a "result," not "scaffolding." This is 1-2 days of work using `tig_dirac` and `find_higgs_direction.py`.
- **Strip "scaffolding" framing.** Per referee §3: rewrite the abstract and §5 to read as a structural-framework paper that reports the algebraic content (SO(7) intermediate, two-zero pattern) and the one new observable, rather than as an explicit non-completion of Yukawa.
- **Add the SO(7) phenomenological story.** Per referee §5.3: "does the SO(7) endpoint preserve quark-color triality? lepton number? left-right symmetry?" This is straightforward representation theory: under SU(5) ⊂ SO(7), the SM content emerges via the standard SU(5) GUT route; SO(7) → SU(4) → SU(3) × U(1)_em via Pati-Salam. State this in one paragraph; no novel computation, but the referee question gets a textbook answer.

MPLA accepts theoretical-framework papers more permissively than PRD. With these changes, the referee's estimate of ~30% acceptance probability at MPLA improves to ~50-60%.

## §4 — What the SAVE PATH does NOT change

The mathematical content is preserved verbatim (under either option):

- The 9-vector with $\|v\|^2 = 13/4$ — kept (in J45 §2.1 or J38-MPLA §1).
- The SO(10) → SO(9) → SO(7) breaking chain — kept.
- The BREATH = RESET = 0 constraint — kept.
- The standard Yukawa structure $\mathbf{16} \otimes \mathbf{16} = \mathbf{10} \oplus \mathbf{120} \oplus \overline{\mathbf{126}}$ background — kept.
- The 54-VEV → first-stage symmetry breaker observation — kept.
- The "Honest scope" paragraph — kept (in revised form, expanded into J45's §7 or sharpened in MPLA's §5).
- The structural-fingerprint observation about $13 = 2 \cdot 13$ — kept *as an arithmetic input*, not as a "fingerprint" claim.

## §5 — Per-venue cap

J38 was the 4th PRD paper of the quarter (per its own README §6). **Both options remove J38 from PRD entirely:**

- Option 1 (fold into J45): J45 is already PRD's 2nd of the quarter (after J44). Folding J38 in does not create a 3rd paper; it merges existing planned content. Net PRD count this quarter: 2 (J44, J45).
- Option 2 (MPLA): MPLA is a fresh venue for the J-series. Net PRD count this quarter: 2 (J44, J45). MPLA cap not in play.

Combined with SAVE_PLAN_J37 (retarget J37 to LAA), this **resolves the entire PRD per-venue cap problem for the quarter**: PRD load goes from 4 (J37, J38, J44, J45) to 2 (J44, J45). The original cap concern dissolves.

## §6 — Honest assessment of what could still go wrong

**Option 1 (fold-in):** the risk is that J45's existing structure may be reluctant to absorb a substantial new §2. J45's mass_hierarchy_v5.tex is ~340 lines, PRD-format. Adding J38's content as a new §2 expands J45 to perhaps ~480 lines, which is on the long side for PRD but still acceptable (PRD article length cap is 9500 words ~ 14 pages typeset). A J45 editor might prefer J38 as a separate paper for length reasons.

**Mitigation:** absorb J38 in a *condensed* form (~50 lines of LaTeX, not the full ~150 lines of the J38 manuscript). The essential algebraic content fits in 3-5 paragraphs:
- 9-vector VEV with $\|v\|^2 = 13/4$: 1 paragraph + 1 equation.
- SO(10) → SO(9) breaking: 1 paragraph + 1 chain-decomposition equation.
- BREATH=RESET=0 → SO(7) intermediate: 1 paragraph + 1 representation-theory equation.
- SU(5) inside SO(7) via V representation: 1 paragraph + the V definition.

That is a defensible §2 length for J45 and lets the rest of J45 proceed as currently structured.

**Option 2 (MPLA):** the risk is that MPLA's referees, like PRD's, will object to the framework-paper status without a derived observable. The §3 mitigation (compute one observable) addresses this directly. If the one-observable computation turns out to be unstable or hard to derive cleanly, the fold-in option becomes the only safe path.

**Recommendation:** go with Option 1 (fold-in) as the default. If J45's editorial flow makes that infeasible, fall back to Option 2 (MPLA + compute one observable). The "hold as arXiv research note" path the referee mentions is also acceptable, but Option 1 better preserves J38's content as published-and-citable rather than preprint-only.

## §7 — Action checklist (for the eventual revision sprint)

**Option 1 (fold-in to J45):**
- [ ] Draft a condensed version of J38's §1, §2, §3 as new J45 §2 (3-5 paragraphs)
- [ ] Insert into J45's mass_hierarchy_v5.tex as §2 (existing §3 onwards renumber)
- [ ] Add J31 / WP104 citation for the 9-vector derivation
- [ ] Resolve the Path A / Path B tension per §2(b): explicit statement that J45 uses Path A only (V⊗5 → SU(5) via SO(7)); Path B's su(4) ⊕ u(1) is independent structural content cited from J31
- [ ] Sharpen J45's §7 (Open questions) with J38's §5 ("Honest scope") absorbed
- [ ] Update J45 cover_letter.md to mention "absorbs J38's symmetry-breaking-route scaffolding"
- [ ] Update J45 README.md (§5 Status update)
- [ ] **Mark J38 in J-series ordering as "FOLDED INTO J45 — do not submit as standalone"**
- [ ] Update J38 README.md to reflect fold-in status; preserve manuscript.md as draft input for archive

**Option 2 (MPLA standalone, fallback only):**
- [ ] Retitle J38 per §3 above
- [ ] Resolve Path A / Path B tension per §2(b) above
- [ ] Compute one falsifiable observable per referee §6.3 (1-2 days)
- [ ] Add SO(7) phenomenological story per §3 above
- [ ] Strip "scaffolding" framing
- [ ] Update cover_letter.md to MPLA
- [ ] Update README.md target venue → MPLA

**Expected outcome:**
- Option 1 (fold-in): **strengthens J45**, removes 1 paper from the quarter's submission load, preserves all of J38's content. Net positive on every dimension. This is the recommended path.
- Option 2 (MPLA): ~50-60% acceptance probability; J38 remains a published standalone paper. Acceptable if Option 1 is editorially infeasible.

Both options are honest saves: J38's content is real algebraic material and survives intact in either home. **The only outcome that "loses" J38 is submitting it as currently constituted to PRD as the 4th paper of the quarter; both save options avoid that explicitly.**
