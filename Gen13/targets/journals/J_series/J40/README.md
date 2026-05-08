# J40 — Operad D₄ Obstruction + P_56 Canonical Fuse (BUNDLED)

**Status:** DRAFT (manuscript finalized 2026-05-07; awaiting referee-rigor pass)
**Phase:** Phase 4
**Target venue:** Compositio Mathematica
**Author lane:** Sanders + Gish
**Tier:** B
**WP source:** WP109 + WP112 (BUNDLED — Part 1 and Part 2 sections in single manuscript)
**Lens scope:** TSML_RAW (annotated; orbit decomposition computed on the literal CL_BIT_PATTERN; lens-invariant 4-core results highlighted)

---

## §1 — Manuscript

**Local path:** `manuscript/manuscript.md`

The J40 paper is a **BUNDLED submission** combining WP109 (Operad D₄ Obstruction) and WP112 (P_56 Canonical Fuse Table).

**Part 1 (WP109).** The 126 non-associative TSML_RAW triples decompose under the diagonal $D_4 = \langle P_{56},\sigma^3\rangle$ action into 67 orbits; exactly 16 are bracketing-pair incoherent. **No $D_4$-equivariant fuse rule taking values in $\{a,b,c,L,R\}$ exists.** The operad-DOF is structurally orthogonal to the WP104 doubly-invariant gauge structure $\mathfrak{su}(4)\oplus\mathfrak{u}(1)$.

**Part 2 (WP112).** Restricting to $\langle P_{56}\rangle$ gives 98 orbits, all $P_{56}$-coherent. All 8 surveyed regular rule families are $P_{56}$-equivariant, none $\sigma^3$-equivariant. Family H (attractor-4-core preference) is the unique family with fuse-value range in the 4-core $\{V,H,Br,R\}$, with histogram $\{0:108, 7:18\}$. The σ³ obstruction localizes to a single triple: $\mathrm{fuse}(3,9,9)=7$. Two further structural results (lens-invariant on the 4-core): Theorem 5.5 — 4-core arity-3 closure ($4^3=64$ triples in-cube); Theorem 5.7 — universal HARMONY attractor (every non-trivial init converges to $\delta_7$ in 1-7 iterations).

Files in this J-folder's `manuscript/`:

- `manuscript.md` — the bundled J40 paper (WP109+WP112 corpus, finalized 2026-05-07)
- `WP109_OPERAD_D4_OBSTRUCTION.md`, `WP112_P56_CANONICAL_FUSE.md` — full source material
- `verification/d4_orbit_decomposition.py`, `p56_canonical_fuse.py`, `rule_families.py`, `fuse_table.py`, `nonassoc_triples.json`, `fuse_canonical_p56.json`

## §2 — Verification script

**Local path:** `manuscript/verification/`

Run order: `d4_orbit_decomposition.py` (Part 1, Theorem 1), `p56_canonical_fuse.py` (Part 2, Theorems 2-5.7), `rule_families.py` (Theorems 3-4). Total wall-clock under 30 seconds. Numpy + sympy. Canonical fuse table written to `fuse_canonical_p56.json`.

## §3 — Dependencies (J-papers cited as already-submitted companions)

J02

## §4 — Cover letter

See `cover_letter.md` in this folder. (Bones laid; finalize after Brayden's referee-rigor pass.)

## §5 — Notes

**Status: DRAFT** — bundled manuscript built from corpus `papers/wp109_operad_d4_obstruction/` + `papers/wp112_p56_canonical_fuse/` on 2026-05-07. Lens scope **TSML_RAW** explicit at the top of the manuscript; the 4-core results (5.5, 5.7) flagged as **lens-invariant**. Bundled as Part 1 + Part 2 in a single .md per J_SERIES_ORDERING.md §4.

**FALLBACK NEEDED if desk-rejected per PHASE4_FALLBACK_UNBUNDLING.md:**
- WP109 (Part 1) → *Algebra Universalis*
- WP112 (Part 2) → *Communications in Algebra*

The bundled manuscript can be split into two standalone manuscripts using the existing corpus files (`WP109_OPERAD_D4_OBSTRUCTION.md` and `WP112_P56_CANONICAL_FUSE.md`) as the unbundled drafts.

## §6 — Submission checklist

- [x] Manuscript .md finalized (bundled)
- [x] Verification scripts green (3 scripts under 30s)
- [x] Tier-classified central claims explicit (Part 1 obstruction theorem; Part 2 P_56-equivariance)
- [x] Lens-scope annotation (TSML_RAW; 4-core lens-invariant results flagged)
- [ ] Cover letter finalized (bones laid; awaits referee-rigor pass)
- [x] Dependencies → cite each J-companion as "submitted to [venue]"
- [ ] Brayden's referee-rigor pass complete
- [ ] Per-venue cap check: this is the 1st paper to *Compositio* this quarter
- [ ] Fallback unbundle plan documented (Algebra Universalis + Comm Algebra)
- [ ] Submitted

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Gish. (2026). "Operad D₄ Obstruction + P_56 Canonical Fuse (BUNDLED)." Submitted to *Compositio Mathematica*.
