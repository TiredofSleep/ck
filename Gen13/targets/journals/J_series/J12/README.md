# J12 — Coordinate Coverage on Z/10Z

**Status:** DRAFT
**Phase:** Phase 2
**Target venue:** European Journal of Combinatorics
**Author lane:** Sanders + Gish
**Tier:** B
**WP source:** WP64

---

## §1 — Manuscript

**Path:** `(corpus: WP64)`

When the manuscript is in this J-folder, replace this section with a 1-2 sentence abstract and a path-link to the .tex / .md file.

## §2 — Verification script

**Path:** `(coordinate coverage script)`

The proof script (where applicable) is the green-light gate before submission. If "(no script — theorem-paper)" or similar, the gate is the proof's referee-rigor pass.

## §3 — Dependencies (J-papers cited as already-submitted companions)

J10

## §4 — Cover letter

See `cover_letter.md` in this folder. (Bones laid; finalize after Brayden's referee-rigor pass.)

## §5 — Notes

UOP arc closeout.

**Status update (2026-05-07):**

- Manuscript: `manuscript/manuscript.tex` — amsart, ~10 pages. Coordinate-coverage and partition-lattice paper for European Journal of Combinatorics. Synthesized from WP64 (Sprint 12 corpus, source-of-truth at `Gen12/targets/clay/papers/sprint12_uop_gut_arc_2026_04_08/`). Main results: rigidity of the prime-factor family (k-1 jumps), three sufficient 2-partition families on Z/30Z (one orthogonal jump each, giving MVJN(Z/30Z) = 1), the orbit-pair classification via coprime-order at every CRT prime, the three mechanisms (focused / same-prime coprime-orders / mixed) with criterion for mechanism (M2) existence (some p_i - 1 has >= 2 distinct prime factors). Detailed treatment of the n = 10 partition lattice. Conjecture: MVJN(Z/nZ) = 1 for all squarefree n >= 6.
- Cover letter: `cover_letter.md` finalized, ~500 words.
- Companion citation: J10 (UOP lead, JNT) cited for the joint-map injectivity criterion. J11 (Corrected Theorem C, JNT) cited for the M+A correction.



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
- [ ] Per-venue cap check: this is the Nth paper to European Journal of Combinatorics this quarter
- [ ] Submitted

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Mayes. (2026). "Coordinate Coverage on Z/10Z." Submitted to *European Journal of Combinatorics*.
