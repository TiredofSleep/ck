# J18 — The σ²-Triadic Decomposition: Conservation/Manifestation Duality on Z/10Z

**Status:** DRAFT
**Phase:** Phase 2
**Target venue:** Algebraic Combinatorics
**Author lane:** Sanders + Gish
**Tier:** B
**WP source:** (Conservation/Manifestation)

---

## §1 — Manuscript

**Path:** `(corpus: Conservation/Manifestation paper)`

When the manuscript is in this J-folder, replace this section with a 1-2 sentence abstract and a path-link to the .tex / .md file.

## §2 — Verification script

**Path:** `(triadic decomposition script)`

The proof script (where applicable) is the green-light gate before submission. If "(no script — theorem-paper)" or similar, the gate is the proof's referee-rigor pass.

## §3 — Dependencies (J-papers cited as already-submitted companions)

J02

## §4 — Cover letter

See `cover_letter.md` in this folder. (Bones laid; finalize after Brayden's referee-rigor pass.)

## §5 — Notes

Per-venue cap: 2nd AlgComb paper after J02.

**Save plan (2026-05-07):** see `Atlas/META_PLAN_2026-05-06/SAVE_PLANS/SAVE_PLAN_J18.md`.

Fresh-eyes referee report `J18_AlgComb_FreshEyes.md` flagged: **(M2)** Proposition 5.4 sign-swap between statement (`O_1 = -7, O_2 = -8`) and proof (`O_1 = -8, O_2 = -7`); **(M1, M3)** `Ψ_B` defined via inaccessible companion + linear/boundary period formulas in mutual contradiction; **(M4)** "conservation/manifestation duality" undefined.

**Fixes applied:** (a) Proposition statement corrected to `O_1 = -8, O_2 = -7` (matches the proof). (b) `Ψ_B` defined inline by an explicit 10-value table (Table 1) that simultaneously satisfies the σ-orbit triangular split (`-T_5, -T_3 = -15, -6`), the role-Fibonacci split (`-F_7, -F_6 = -13, -8`), and the σ²-orbit split (`-8, -7`) by direct integer addition. (c) "Conservation/manifestation duality" replaced by precise Definition 3.4 (table-independent vs. table-specific) with a concrete random-perturbation criterion. (d) New title: *Two Crossing Decompositions of a -21 Invariant on Z/10Z with the σ²-Triadic Refinement*.

All numerical claims verified by direct addition; the explicit Ψ_B table in revision is `{0: +1, 1: -5, 2: -3, 3: -2, 4: -2, 5: -1, 6: -1, 7: -3, 8: -3, 9: -2}`.



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
- [ ] Per-venue cap check: this is the Nth paper to Algebraic Combinatorics this quarter
- [ ] Submitted

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Gish. (2026). "The σ²-Triadic Decomposition: Conservation/Manifestation Duality on Z/10Z." Submitted to *Algebraic Combinatorics*.
