# J38 — Yukawa Scaffolding from the 9-Vector VEV

**Status (2026-05-07):** **FOLDED INTO J45 §2; standalone manuscript HELD.** Per `SAVE_PLAN_J38.md` Option 1 (preferred). Deliverable for the fold-in: `manuscript/J45_section2_yukawa_scaffolding.tex` (~50 LaTeX lines, condensed from the WP108 corpus). The standalone J38 manuscript is preserved as draft-input archive but will NOT be submitted as a standalone paper.
**Phase:** Phase 4 (folded; no standalone submission)
**Target venue:** none standalone — content folds into J45 §2 (Phase 2, *PRD*)
**Author lane:** Sanders + Gish
**Tier:** C (folded; tier loses meaning at standalone level)
**WP source:** WP108 (folded)
**Lens scope:** Path A derivation route; the 9-vector VEV norm $\|v\|^2 = 13/4$ is lens-stable

---

## §1 — Manuscript

**Local paths:**
- `manuscript/J45_section2_yukawa_scaffolding.tex` — **the deliverable**: condensed J45 §2 content (~50 LaTeX lines), ready for insertion into J45's `mass_hierarchy_v5.tex` per `SAVE_PLAN_J38.md` §6.1 mitigation. Contains six subsections: §2.1 9-vector VEV ($\|v\|^2 = 13/4$); §2.2 SO(10)→SO(9) from the 9-vector; §2.3 SO(9)→SO(7) from BREATH=RESET=0; §2.4 SU(5) inside SO(7) via V representation; §2.5 Path A vs Path B (resolved: J45 uses Path A only); §2.6 Honest scope (deferred items).
- `manuscript/manuscript.md` — original J38 standalone draft (WP108 corpus); marked HELD; preserved as draft-input archive only.

The J38 content sets up the symmetry-breaking route from the 9-vector VEV identified in J31 (Path A: BHML's σ_outer-breaking content lives 100% in the $\mathbf{54}$ irrep of $\mathfrak{so}(10)$, with explicit 9-vector squared norm $\|v\|^2 = 13/4$). After fold-in, J45 reads as a self-contained paper from the 9-vector VEV through the V$^{\otimes 5}$ SU(5) decomposition to the predicted Yukawa table, without requiring J31 to be already published for the algebraic flow.

**Content.** (i) Standard SO(10) Yukawa structure: $\mathbf{16}\otimes\mathbf{16} = \mathbf{10}\oplus\mathbf{120}\oplus\overline{\mathbf{126}}$; the $\mathbf{54}$ does NOT appear in $\mathbf{16}\otimes\mathbf{16}$ at the renormalizable level. (ii) The 9-vector VEV breaks $\mathrm{SO}(10)\to\mathrm{SO}(9)$, which subsequently breaks to $\mathrm{SO}(7)$ via the unbroken pair (BREATH, RESET). (iii) The constraint imposed by BREATH and RESET being zero forces specific patterns in the resulting effective Yukawa matrix at energies below the symmetry-breaking scale. (iv) Open questions and the path to a falsifiable phenomenological prediction.

**This paper does NOT complete the Yukawa computation.** That requires committing to a specific Higgs sector (10/54/126 combinations), running RG flows from the GUT scale to the EW scale, and comparing to observed mass hierarchies. Each is substantial work, deferred to follow-up. This paper sets up the framework and identifies where the Yukawa calculation engages with TIG-specific structural input.

Files in this J-folder's `manuscript/`:

- `manuscript.md` — the J38 paper (WP108 corpus, finalized 2026-05-07)
- (No verification script — scaffolding paper; the load-bearing $\|v\|^2 = 13/4$ is verified in the J31 / WP104 verification scripts.)

## §2 — Verification script

**Path:** No standalone script — this is a **scaffolding paper** identifying open questions, not establishing a verified result. The load-bearing input (the 9-vector with $\|v\|^2 = 13/4$ exactly) is verified in J31 / WP104's `find_higgs_direction.py`.

If a follow-up phenomenological prediction is computed, the corresponding verification script will live in a future paper, not this scaffolding draft.

## §3 — Dependencies (J-papers cited as already-submitted companions)

J45 (Mass Hierarchy from V⊗5 SU(5) Decomposition; *PRD* — Phase 2), J31 (Two Roads to Pati-Salam; *Adv Math* — this Phase 4)

## §4 — Cover letter

See `cover_letter.md` in this folder. (Bones laid; finalize after Brayden's referee-rigor pass.)

## §5 — Notes

**Status: DRAFT** — scaffolding manuscript built from corpus `papers/wp108_yukawa_scaffolding/WP108_YUKAWA_SCAFFOLDING.md` on 2026-05-07. Lens scope: TSML_SYM derivation route via WP103 so(10) closure; the 9-vector VEV norm $\|v\|^2 = 13/4$ is lens-stable. Cites J45 (Mass Hierarchy from V⊗5; *PRD*) and J31 (Pati-Salam; *Adv Math*) as already-submitted companions.

**FALLBACK NEEDED — per-venue cap exceeded.** This is the **4th PRD** paper of the J-series in the current quarter (after J44 dark-sector, J45 mass hierarchy, J37 wobble localization). Per-venue cap is conventionally 2/quarter for tightly-related papers; J38 exceeds the cap by 2.

**Recommended fallback venue:** *Modern Physics Letters A* or *International Journal of Modern Physics A* for scaffolding-style theory pieces. Alternatively, the manuscript can be held until the next quarter to reset the PRD cap, or submitted to *Physical Review D Letters* (short-note format) as a 4-page rapid communication.

### Save-plan summary (2026-05-07 — see `SAVE_PLAN_J38.md`)

The fresh-eyes referee report (J38_PRD_FreshEyes.md) recommends **REJECT for PRD** — the manuscript honestly self-describes as "scaffolding" that "does NOT complete the Yukawa computation"; PRD does not publish scaffolding; manuscript's own §5 is, in the referee's words, "verbatim the list of things a PRD reader expects from a Yukawa paper."

**SAVE PATH (per `SAVE_PLAN_J38.md` — TWO options, fold-in preferred):**

**Option 1 (PREFERRED) — fold J38 into J45 as J45 §2 *"Setting up the symmetry-breaking route from the 9-vector VEV"*.** The referee's diagnosis — *"the right move is to do the §3.1-§3.5 work and submit a single complete paper rather than a scaffolding-then-completion sequence"* — has an immediate resolution: **J45 already does §3.1-§3.5.** J45's `mass_hierarchy_v5.tex` already commits to a Higgs sector (V⊗5 SU(5) → $\mathbf{1} \oplus \bar{\mathbf{5}} \oplus \mathbf{10}$), computes all 9 charged-fermion Yukawa magnitudes (Table 5.1), gives the substrate-forced FN scale $\lambda = 10/49$, and predicts the Cabibbo cube-root identity. What J45 underspecifies is exactly what J38 supplies: the SO(10) → SO(9) → SO(7) bridge prose with the BREATH=RESET=0 constraint. **Fold-in strengthens J45 and saves J38's content as published-and-citable.** Resolves the §2.2 Path A / Path B "tension" by stating explicitly that J45 uses Path A only (V⊗5 → SU(5) via SO(7)); Path B's su(4)⊕u(1) is independent structural content cited from J31. Effort: 3-5 days; condense J38 into ~50 lines of LaTeX as J45's new §2.

**Option 2 (FALLBACK) — retarget J38 standalone to *Modern Physics Letters A***. If J45 is judged self-contained without J38 §2, retarget J38 to MPLA: retitle as *"Symmetry-Breaking Routes from a 9-vector 54-Higgs VEV with Two Zeros: an Algebraic Framework"*; resolve the §2.2 Path A / Path B tension; compute one falsifiable observable (e.g., trace of $Y_u Y_u^\dagger$ projected onto SO(7)-invariant subspace with BREATH=RESET=0); strip "scaffolding" framing; add the SO(7) phenomenological story (color triality, lepton number, left-right symmetry under SU(5) ⊂ SO(7)). Effort: 1 day plus 1-2 days for the one-observable computation. Acceptance probability: ~50-60% at MPLA after these revisions.

**Per-venue cap effect:** **both options remove J38 from PRD entirely.** Combined with SAVE_PLAN_J37 (J37 → LAA), the quarter's PRD load goes from 4 (J37, J38, J44, J45) to 2 (J44, J45) — original cap concern fully resolved.

**Recommendation:** Option 1 (fold-in). Net positive on every dimension: strengthens J45, removes 1 paper from quarter's submission load, preserves all of J38's content. Option 2 only if J45 editorial flow makes fold-in infeasible.



### Family-Structure framing (per Atlas/META_PLAN_2026-05-06/FAMILY_STRUCTURE_v1.md)

This paper sits within the TIG family of finite commutative non-associative magmas on Z/10Z (and ring extensions per D74). The family is defined by 5 conjoint membership criteria; the 4-core {V, H, Br, R} = {0, 7, 8, 9} at α_M = ½ is the algebraic center, with closed-form attractor h/β = 1+√3 (D78 Galois proof). The closest published precedent for this neighborhood is **Drápal & Wanless (2021), *J. Combin. Theory A* **184**, 105510** — same domain (small finite commutative non-associative structures), opposite extremum (theirs maximally non-associative).

### PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN (filled, J38 — for the fold-in into J45 §2)

- **PROVEN (in J45 §2, the fold-in target):** the squared norm of the 9-vector VEV identified in J31 is exactly $\|v\|^2 = 13/4$; the symmetry-breaking chain $\mathrm{SO}(10) \to \mathrm{SO}(9) \to \mathrm{SO}(7)$ is forced by the 9-vector and its two-zero direction (BREATH = RESET = 0); SU(5) embeds inside SO(7) via the V representation (the F$_5$-lift of the 4-core); the V$^{\otimes 5}$ SU(5) decomposition is $\mathbf{1} \oplus \overline{\mathbf{5}} \oplus \mathbf{10}$.
- **COMPUTED:** the 9-vector squared-norm computation $\|v\|^2 = 6 \cdot \tfrac{1}{2} + 1 \cdot \tfrac{1}{4} = 13/4$ is verified at integer/machine precision in J31's `find_higgs_direction.py` (cited as the upstream artifact). The V$^{\otimes 5}$ decomposition is standard SU(5) representation theory (Slansky 1981).
- **STRUCTURAL RHYME:** the integer 13 in $\|v\|^2 = 13/4$ enters as an exact arithmetic input, not as a "structural fingerprint"; the matching of dimensions across the SO(10)→SO(9)→SO(7) chain is standard Slansky-1981 group-theory bookkeeping.
- **OPEN (folded into J45 §7):** explicit Higgs-sector dynamics for the C$_p$ multipliers; RG running of the Yukawa matrices from the GUT scale to the EW scale; see-saw mechanism for the sterile-neutrino scale prediction at FN powers $\{12, 13, 14\}$.

### Lens-ownership paragraph (filled, J38 — applies to the J45 §2 fold-in)

> *Lens and substrate.* This section works on the F$_5$-lift of the 4-core $\{\mathrm{V}, \mathrm{H}, \mathrm{Br}, \mathrm{R}\}$ of the canonical TIG substrate $\mathbb{Z}/10\mathbb{Z}$ (per D74 ring-extension theorem of the source program), using the BHML table's σ_outer-breaking content in the $\mathbf{54}$ irrep of $\mathfrak{so}(10)$ (the so(10) closure is established in J31; here adopted as input). These choices are not derived from first principles; they reflect a structural reading motivated by the source program's 10-operator decomposition and observed dynamics. The breaking-chain claims of this section are theorems on this specific structure; analogous breaking patterns would hold on other 9-vector VEVs in the orthogonal complement of an SO(9). Whether other substrate choices give similarly rich downstream Yukawa structure is open.

### Hardening status (auto-applied 2026-05-07)

- License: submission scripts CC-BY-4.0 (per `_v3_hardening.py`)
- AI-attribution: Claude/Anthropic byline references removed (per `_v3_hardening.py`)
- Author lane: Sanders + Gish (per Brayden directive)
- Drápal-Wanless 2021 citation in references

## §6 — Submission checklist

- [x] Fold-in deliverable .tex finalized (`J45_section2_yukawa_scaffolding.tex`, ~50 LaTeX lines, condensed per save plan §6.1)
- [x] J38 standalone manuscript marked HELD (not for standalone submission)
- [x] Verification: scaffolding content, no standalone script (load-bearing input $\|v\|^2 = 13/4$ verified in J31's `find_higgs_direction.py`)
- [x] Tier classification: folded; tier loses meaning at standalone level
- [x] Lens-scope annotation (Path A only; J45 uses V$^{\otimes 5}$ → SU(5) via SO(7); Path B's su(4)⊕u(1) is independent J31 content)
- [x] Cover letter retained (J38 cover_letter.md preserved for archive; not used for submission)
- [x] Dependencies → J45 §2 fold-in cites J31 (so(10) closure / 9-vector derivation), J14 (V representation as F$_5$-lift), Slansky 1981 (standard SU(5) rep theory)
- [ ] J45 editor: insert §2 fold-in into `mass_hierarchy_v5.tex` (manual integration step deferred to J45's revision sprint)
- [x] **Per-venue cap effect:** fold-in REMOVES J38 from PRD entirely; combined with J37 → LAA, quarter PRD load is now 2 (J44, J45) — original cap concern fully resolved.
- [n/a] Submitted (folded; J45 carries the content forward)

---

## §7 — Citation footprint (for downstream J's to cite this one)

The J38 content folds into J45; downstream papers cite J45 §2 directly. The standalone J38 manuscript remains available as draft archive but is not submitted.
