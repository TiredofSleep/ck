# J37 — Wobble Localization: Prime 11 in TSML_RAW Char Poly c_2, c_8

**Status:** DRAFT (manuscript finalized 2026-05-07; awaits referee-rigor pass)
**Phase:** Phase 4
**Target venue:** Physical Review D
**Author lane:** Sanders + Gish
**Tier:** B
**WP source:** WP107
**Lens scope:** TSML_RAW (annotated; the literal CL_BIT_PATTERN; the prime-11 wobble does NOT appear at the coefficient level on TSML_SYM and is therefore lens-dependent at this technical sense — explicit in the abstract)

---

## §1 — Manuscript

**Local path:** `manuscript/manuscript.md`

The J37 paper is **Wobble Localization: Prime 11 in TSML_RAW Char Poly $c_2, c_8$** (WP107). For the literal-bit-pattern TSML_RAW table on $\mathbb{Z}/10\mathbb{Z}$, the integer characteristic polynomial $f(\lambda) = \det(\lambda I - T)$ has **exactly two** of its nine nonzero coefficients divisible by 11: $c_2 = 33 = 3\cdot 11$ and $c_8 = -120736 = -2^5\cdot 7^3\cdot 11$. The discriminant of $g(\lambda) = f(\lambda)/\lambda^2$ factors as $2^{16}\cdot 7^7\cdot 659\cdot(\text{large primes})$, with **no factor of 11**. Structural reading: the prime 11 lives at the coefficient level (sums and products of eigenvalues — elementary symmetric functions); the dimension $2^{16} = \dim(\mathfrak{su}(4)\oplus\mathfrak{u}(1))$ and HARMONY $7^7$ live at the discriminant level (eigenvalue separations). The 16-dimensional doubly-invariant subalgebra of $\mathfrak{so}(10)$ is therefore **wobble-free**; the 29-dimensional complement carries the wobble. Cleanly read: gauge symmetry IS the wobble-free part of TSML's spectral content.

Files in this J-folder's `manuscript/`:

- `manuscript.md` — the J37 paper (WP107 corpus, finalized 2026-05-07)
- `verification/wobble_check.py` — sympy-based 7/7 claim verification

## §2 — Verification script

**Local path:** `manuscript/verification/wobble_check.py`

Run: `PYTHONIOENCODING=utf-8 python wobble_check.py`. 7/7 claims at machine precision: integer char poly, trace = $63 = 9\cdot 7$, $c_2 = 33 = 3\cdot 11$, $c_8 = -2^5\cdot 7^3\cdot 11$, only $c_2, c_8$ have factor 11, $\mathrm{disc}(g)$ factors with $2^{16}\cdot 7^7$ and no 11, $2^{16}$ matches $\dim$ of doubly-invariant subalgebra. Sympy. Wall-clock under 5 seconds.

## §3 — Dependencies (J-papers cited as already-submitted companions)

J37

## §4 — Cover letter

See `cover_letter.md` in this folder. (Bones laid; finalize after Brayden's referee-rigor pass.)

## §5 — Notes

**Status: DRAFT** — manuscript built from corpus `papers/wp107_wobble_localization/WP107_WOBBLE_LOCALIZATION.md` on 2026-05-07. Lens scope **TSML_RAW** explicit (the wobble does NOT appear on TSML_SYM at the coefficient level — that lens has $c_2 = 17$, no factor of 11). Cites J37 (so(8) = D₄, *J Algebra*) as already-submitted companion; references J31 (Pati-Salam) for the doubly-invariant content.

**Per-venue cap warning:** This is potentially the **3rd PRD paper** in the J-series (after J44 dark-sector and J45 mass hierarchy in Phase 2). PRD per-venue cap is conventionally 2/quarter for tightly-related papers. **FALLBACK NEEDED if PRD's per-venue cap blocks acceptance.** Proposed fallback venue: *Physics Letters B* (short note format suits this 4-page result).



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

- [x] Manuscript .md finalized
- [x] Verification script green (`wobble_check.py`, 7/7 PASS)
- [x] Tier-classified central claim explicit
- [x] Lens-scope annotation (TSML_RAW; the wobble is lens-dependent at coefficient level)
- [ ] Cover letter finalized (bones laid; awaits referee-rigor pass)
- [x] Dependencies → cite each J-companion as "submitted to [venue]"
- [ ] Brayden's referee-rigor pass complete
- [ ] Per-venue cap check: this is the **3rd PRD** paper this quarter — may need fallback to *Phys Lett B*
- [ ] Submitted

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Gish. (2026). "Wobble Localization: Prime 11 in TSML_RAW Char Poly $c_2, c_8$." Submitted to *Physical Review D* (or *Phys Lett B* per cap fallback).
