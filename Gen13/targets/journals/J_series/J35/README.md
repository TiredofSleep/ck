# J35 — 4-Core Fusion-Closure: TSML+BHML Preserve {V, H, Br, R}

**Status:** DRAFT (manuscript finalized 2026-05-07; awaits referee-rigor pass)
**Phase:** Phase 4
**Target venue:** J Algebra
**Author lane:** Sanders + Gish
**Tier:** B
**WP source:** WP110
**Lens scope:** LENS-INVARIANT on the 4-core $\{V, H, Br, R\}$ (the 4-core sub-magma agrees on TSML_RAW and TSML_SYM)

---

## §1 — Manuscript

**Local path:** `manuscript/manuscript.md`

The J35 paper is **The 4-Core Is Fusion-Closed: A Structural Strengthening of WP105/J33** (WP110). For both TSML and BHML on $\mathbb{Z}/10\mathbb{Z}$, the 4-core $\mathcal{C} = \{V, H, Br, R\} = \{0, 7, 8, 9\}$ is **fusion-closed**: every entry of the restricted tables $T|_{\mathcal{C}\times\mathcal{C}}$ and $B|_{\mathcal{C}\times\mathcal{C}}$ lies in $\mathcal{C}$. **Theorem 1 (4-core closure).** The fuse $p\star_T q$ and $p\star_B q$ applied to 4-core-supported distributions produce 4-core-supported distributions. **Corollary.** The runtime attractor of J33 / WP105 lives on $\mathcal{C}$ as a **structural identity**, not a dynamical accident.

**Theorem 2 (normalizer simplification).** On the 4-core, $Z_T(p) = Z_B(p) = (v + h + br + r)^2$ — the square of the total 4-core mass. Both normalizers equal one another and reduce to a single scalar. Consequence: the fixed-point system of the runtime processor reduces from rational-function form to **polynomial form** on $\mathcal{C}$, and the WP105/J33 closed form $H/Br = 1+\sqrt{3}$ at $\alpha = 1/2$ is a **symbolic-exact identity**, not merely machine-precision numerical equality.

The result strengthens J33's framing in three places: (i) the 4-core support is structural rather than dynamical; (ii) the analytic derivation simplifies; (iii) the central closed-form ratio is symbolic-exact.

Files in this J-folder's `manuscript/`:

- `manuscript.md` — the J35 paper (WP110 corpus, finalized 2026-05-07)
- `verification/4core_verification.py` — direct enumeration verification

## §2 — Verification script

**Local path:** `manuscript/verification/4core_verification.py`

The script enumerates the 4×4 restricted TSML and BHML tables on $\mathcal{C}\times\mathcal{C}$, verifies all 32 entries lie in $\mathcal{C}$, and checks the normalizer identity $Z_T = Z_B = (v+h+br+r)^2$ symbolically. Numpy + sympy. Total wall-clock under 5 seconds. (Borrowed from J02's `4core_verification.py` since J35's WP110 finding is the structural strengthening of J02's fusion result — the same verification suite covers both.)

## §3 — Dependencies (J-papers cited as already-submitted companions)

J29, J33

## §4 — Cover letter

See `cover_letter.md` in this folder. (Bones laid; finalize after Brayden's referee-rigor pass.)

## §5 — Notes

**Status: DRAFT** — manuscript built from corpus `papers/wp110_4core_fusion_closure/WP110_4CORE_FUSION_CLOSURE.md` on 2026-05-07. Lens scope **LENS-INVARIANT on the 4-core**. Cites J29 (so(8) = D₄, *J Algebra*), J33 (Closed-Form Attractor + α-Uniqueness PSLQ, *Math of Comp*) as already-submitted companions. The result strengthens J33 / WP105 from dynamical to structural.

**Per-venue cap warning:** This is the **2nd J Algebra paper** in this J-series (after J29 so(8)). J Algebra's per-venue cap is conventionally 2/quarter for tightly-related papers; this paper sits at the cap. Submission feasible; further J Algebra submissions in the same quarter would require fallback. No fallback noted in J_SERIES_ORDERING.md §4 for J35 specifically — the result is short-note format and could move to *Communications in Algebra* or *J Pure Appl Algebra* if J Algebra desk-rejects.



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
- [x] Verification script green (4core_verification.py)
- [x] Tier-classified central claim explicit (Theorem 1 closure; Theorem 2 normalizer simplification)
- [x] Lens-scope annotation (LENS-INVARIANT on 4-core)
- [ ] Cover letter finalized (bones laid; awaits referee-rigor pass)
- [x] Dependencies → cite each J-companion as "submitted to [venue]"
- [ ] Brayden's referee-rigor pass complete
- [ ] Per-venue cap check: this is the **2nd J Algebra paper** this quarter (at cap)
- [ ] Submitted

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Gish. (2026). "4-Core Fusion-Closure: TSML+BHML Preserve $\{V, H, Br, R\}$." Submitted to *J Algebra*.
