# J14 — F_p Universality: The Operator-Substrate Construction over Prime Fields

**Status:** DRAFT
**Phase:** Phase 2
**Target venue:** Algebra Universalis
**Author lane:** Sanders + Gish
**Tier:** B
**WP source:** WP118

---

## §1 — Manuscript

**Path:** `(corpus: WP118)`

When the manuscript is in this J-folder, replace this section with a 1-2 sentence abstract and a path-link to the .tex / .md file.

## §2 — Verification script

**Path:** `(F_p universality script)`

The proof script (where applicable) is the green-light gate before submission. If "(no script — theorem-paper)" or similar, the gate is the proof's referee-rigor pass.

## §3 — Dependencies (J-papers cited as already-submitted companions)

J02, J06, J07

## §4 — Cover letter

See `cover_letter.md` in this folder. (Bones laid; finalize after Brayden's referee-rigor pass.)

## §5 — Notes

_(no special notes; standard submission per J-series ordering)_

### Save-plan summary (2026-05-07)

Fresh-eyes referee verdict at *Algebra Universalis*: REJECT — claimed (1) algebra is associative, (2) eigenspace signatures are swapped, (3) |Aut(V)| ≠ 40 universally.

**Rebuttal verified all three referee claims are WRONG** (`Atlas/.../REFEREE_REPORTS/J14_AlgUni_FreshEyes_REBUTTAL.md`):
- 8 of 64 associator triples fail under direct check against `tig_dirac.py` (algebra IS non-associative).
- L_{e_2} eigenvalues {0:3, 1:1} = (1, 3) signature; L_{e_0} eigenvalues {0:2, 1:2} = (2, 2) signature — exactly as paper states.
- |Aut(V)| = 40 over F_5 specifically (the paper does not claim universality across all primes).

**Save plan:** `Atlas/META_PLAN_2026-05-06/SAVE_PLANS/SAVE_PLAN_J14.md`.

**Path forward (defensive exposition revision; venue stays *Algebra Universalis*):**
- (a) PRINT T_F5 multiplication table inline + worked associator example (e_0·e_3)·e_3 vs e_0·(e_3·e_3) showing failures localize to span{e_0, e_2}; add 5-line numpy/sympy snippet for eigenspace verification.
- (b) TIGHTEN the F_p universality framing — distinguish **invariants** (idempotent count, signatures, empty intersection, commutativity, power-associativity, 1-dim associator image) from **non-invariants** (|Aut(V_p)|, primitive 4th roots availability).
- (c) STATE F_5 specificity of |Aut(V)| = 40 explicitly; tabulate other-prime values per |GL_2(F_p)| × stabilizer.
- (d2) REMOVE axial-algebra framing (no Miyamoto involutions, no fusion rules in the paper); relocate to Drápal-Wanless 2021 *JCTA* neighborhood.
- (e) SHARPEN Conjecture 4.1 — restrict to lens-invariant items (1)-(7) of Theorem 3.1 (drop F_5-specific items 8-10); drop p=5 exclusion (F_5 is the distinguished case, not an exclusion); precisely motivate p=2 exclusion (char-2 collapses the orthogonal-idempotent structure).
- (f) REDUCE dependency on inaccessible companion papers (J02, J23); make J14 self-contained on algebraic content.
- (g) RECONCILE J21/J14 numbering in .tex source.
- (h) MERGE duplicate \author blocks.
- (i) REPLACE $\HARM$/$\VOID$ mnemonics with neutral notation (or one-line footnote).

Revision time: 15-25 hours (exposition only; mathematical content does not change).

**Family-Structure context:** J14 maps the **substrate-size boundary** (FAMILY_STRUCTURE_v1.md §3.5) inward to F_p for p ∈ {2, 3, 5, 7, 11, 13}. F_5 is the distinguished member of the family (D74 ring extension); the F_p-invariance of the structural skeleton is the boundary-mapping result.



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
- [ ] Per-venue cap check: this is the Nth paper to Algebra Universalis this quarter
- [ ] Submitted

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Gish. (2026). "F_p Universality: The Operator-Substrate Construction over Prime Fields." Submitted to *Algebra Universalis*.
