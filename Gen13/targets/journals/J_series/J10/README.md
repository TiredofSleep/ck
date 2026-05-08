# J10 — Universal Orthogonality Principle (UOP): Theorem 0

**Status:** FORMAT
**Phase:** Phase 2
**Target venue:** JNT
**Author lane:** Sanders + Gish
**Tier:** B
**WP source:** WP58

---

## §1 — Manuscript

**Local path:** `manuscript/`

Files in this J-folder's `manuscript/`:

- `SUBMIT_INSTRUCTIONS.md`
- `WP58_UNIFIED_ORTHOGONALITY_PRINCIPLE.md`
- `WP59_CORRECTED_THEOREM_C.md`
- `WP64_COORDINATE_COVERAGE.md`

The submission package lives in this J-folder. Edit + verify here; submit from here.

## §2 — Verification script

**Path:** `(UOP verification script — corpus)`

The proof script (where applicable) is the green-light gate before submission. If "(no script — theorem-paper)" or similar, the gate is the proof's referee-rigor pass.

## §3 — Dependencies (J-papers cited as already-submitted companions)

J03, J06, J07

## §4 — Cover letter

See `cover_letter.md` in this folder. (Bones laid; finalize after Brayden's referee-rigor pass.)

## §5 — Notes

UOP arc opener. Cited by J11, J12.

**Status update (2026-05-07):**

- Manuscript: `manuscript/manuscript.tex` — amsart, ~9 pages, lead UOP paper. Synthesized from WP58 (Sprint 12 corpus, source-of-truth at `Gen12/targets/clay/papers/sprint12_uop_gut_arc_2026_04_08/`). Provides the joint-map injectivity statement and derives Theorems A (M+M), B (A+M), C corrected (M+A), D (CRT k-1 / A+A), the coordinate-coverage characterization (sufficient direction), the refinement trap, and MVJN as corollaries of UOP.
- Source corpus retained: `manuscript/WP58_UNIFIED_ORTHOGONALITY_PRINCIPLE.md`, `manuscript/WP59_CORRECTED_THEOREM_C.md`, `manuscript/WP64_COORDINATE_COVERAGE.md` — kept under "never delete + cite" preservation discipline; tex draws from WP58 primarily, with brief inclusion of the Theorem C correction (full treatment in J11) and the coordinate-coverage statement (full treatment in J12).
- Cover letter: `cover_letter.md` finalized, ~500 words.
- Companions cited as submitted: J03 (Sanders–Gish "First-G Law", Integers), J06 (Sanders–Mayes "Crossing Lemma", JCT-A), J07 (Sanders–Gish "Flatness Theorem", JPAA), and the J11/J12 spinoffs as JNT/EJC submissions.

**SAVE-PLAN SUMMARY (2026-05-07; full plan at `Atlas/META_PLAN_2026-05-06/SAVE_PLANS/SAVE_PLAN_J10.md`):**

JNT referee REJECTED: (R1) UOP / Theorem 2.1 is a one-line unfolding of the partition-lattice meet definition (Birkhoff/Ore folklore); (R2) "orthogonality" misleading at JNT (means character orthogonality there); (R3) corollaries A/B/D are CRT folklore; only Theorem 6.1 (coordinate coverage) and the n=15 counterexample are content-rich. Mathematics is **correct**; framing/venue is wrong.

**Save path:** referee EXPLICITLY MAPS the save path. RESTRUCTURE around Theorem 6.1 + RETITLE + RETARGET.
- **New title:** "Coordinate Coverage and Joint-Injectivity Criteria for Partition Pairs on Squarefree Z/nZ."
- **New venue:** *European Journal of Combinatorics* (referee §9 explicit recommendation). Backup: *Discrete Mathematics*.
- **Restructure:** §3 lead with **Theorem 6.1 (coordinate coverage)** as the main result — for squarefree n = p_1...p_k, J=(f,g) injective iff D_f ∪ D_g = {p_1,...,p_k}; §4 compute D_h for each partition class (residue, dynamical-orbit); §5 corollaries A (M+M), B (A+M), C corrected (M+A), D (A+A) — each a one-paragraph derivation. **Demote UOP/Theorem 2.1 to a Lemma** (one-line proof, citing Birkhoff 1940 + Ore 1942). Drop "orthogonality" / "orthogonal jump" terminology globally; replace with "transverse partition pair" or "coordinate coverage."
- **Add:** Prior-Literature subsection in §1 (per M4) honestly delineating what's folklore vs novel. Lens-ownership paragraph + PROVEN/COMPUTED/RHYME/OPEN box.
- **Keep:** §8 MVJN with the n=30 result and Conjecture 8.3 (recast as "immediate application of coordinate-coverage theorem"). The n=15 counterexample (Example 4.1) — referee called it "genuinely surprising."
- **Estimated revision time:** 3-5 weeks.



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

- [ ] Manuscript .tex / .md finalized
- [ ] Verification script green (`(no script)` if theorem-only)
- [ ] Tier-classified central claim explicit
- [ ] Lens-scope annotation (TSML_RAW vs TSML_SYM) where relevant
- [ ] Cover letter finalized
- [ ] Dependencies → cite each J-companion as "submitted to [venue]"
- [ ] Brayden's referee-rigor pass complete (mobile + other AI + collaborators)
- [ ] Per-venue cap check: this is the Nth paper to JNT this quarter
- [ ] Submitted

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Mayes. (2026). "Universal Orthogonality Principle (UOP): Theorem 0." Submitted to *JNT*.
