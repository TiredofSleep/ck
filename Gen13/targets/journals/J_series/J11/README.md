# J11 — Corrected Theorem C: UOP Sharpening

**Status:** DRAFT
**Phase:** Phase 2
**Target venue:** JNT companion
**Author lane:** Sanders + Gish
**Tier:** B
**WP source:** WP59

---

## §1 — Manuscript

**Path:** `(corpus: WP59)`

When the manuscript is in this J-folder, replace this section with a 1-2 sentence abstract and a path-link to the .tex / .md file.

## §2 — Verification script

**Path:** `(UOP sharpening script)`

The proof script (where applicable) is the green-light gate before submission. If "(no script — theorem-paper)" or similar, the gate is the proof's referee-rigor pass.

## §3 — Dependencies (J-papers cited as already-submitted companions)

J10

## §4 — Cover letter

See `cover_letter.md` in this folder. (Bones laid; finalize after Brayden's referee-rigor pass.)

## §5 — Notes

Per-venue cap: 2nd JNT paper after J10.

**Status update (2026-05-07):**

- Manuscript: `manuscript/manuscript.tex` — amsart, ~7 pages. Focused note on the corrected M+A condition. Synthesized from WP59 (Sprint 12 corpus, source-of-truth at `Gen12/targets/clay/papers/sprint12_uop_gut_arc_2026_04_08/`). Treats the n=15 counterexample explicitly, gives the corrected condition, the zero-fiber analysis (Proposition on the action of G on F_d), and the verification that prior applications (SPEC + half-modulus on n = 2m for m odd squarefree) continue to satisfy the corrected condition.
- Cover letter: `cover_letter.md` finalized, ~400 words. Per-venue cap noted: 2nd JNT paper this quarter, with cumulative word count well below typical author-quarter conventions.
- Companion citation: J10 cited as already-submitted JNT lead. UOP is invoked once (in the proof of Theorem 1) to convert the M+A criterion to the symmetric A+M form via joint-map injectivity.



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
- [ ] Per-venue cap check: this is the Nth paper to JNT companion this quarter
- [ ] Submitted

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Mayes. (2026). "Corrected Theorem C: UOP Sharpening." Submitted to *JNT companion*.
