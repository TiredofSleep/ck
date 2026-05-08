# J21 — Q17-A: 5D Force Vector as CRT Fourier Embedding of Z/10Z into R^5

**Status:** DRAFT (manuscript finalized 2026-05-07; awaiting referee-rigor pass)
**Phase:** Phase 2
**Target venue:** AMM
**Author lane:** Sanders + Gish
**Tier:** B
**WP source:** `papers/Q17_5D_RIGOROUS.md`

---

## §1 — Manuscript

**Path:** `manuscript/manuscript.tex`

**Abstract (1-2 sentences):** We give the unique 5-dimensional embedding of $\mathbb{Z}/10\mathbb{Z}$ that respects both the CRT isomorphism $\mathbb{Z}/10\mathbb{Z} \cong \mathbb{F}_2 \times \mathbb{F}_5$ and the standard real Fourier basis on $\mathbb{F}_5$, prove a rigidity statement (the embedding is unique up to block-diagonal $O(1) \times O(4)$), and identify the two-point spectral maximum. The result is folklore in finite Fourier analysis; the rigidity statement and the two-point identification have not previously appeared together at this level.

## §2 — Verification script

**Path:** `(no script — short note; the embedding is verified by ≤30 lines of NumPy in the appendix of the manuscript)`

The proof script (where applicable) is the green-light gate before submission. Here the gate is the rigidity proof's referee-rigor pass.

## §3 — Dependencies (J-papers cited as already-submitted companions)

J03

## §4 — Cover letter

See `cover_letter.md` in this folder. (Bones laid; finalize after Brayden's referee-rigor pass.)

## §5 — Notes

- Calderon's one paper in the J-series.
- Per-venue cap: 2nd AMM paper after J20 (M_22 substrate-prime). AMM still has slot capacity in the quarterly window; no FALLBACK NEEDED.
- Manuscript finalized 2026-05-07 by J21-J28 cluster agent (re-confirmed by J21-J24 finalization batch agent 2026-05-07). Source: `papers/Q17_5D_RIGOROUS.md`. Cites J03 (First-G Law) as already-submitted companion.
- Pedagogical, no Tier-A claims. Rigidity statement is the load-bearing theorem; two-point spectral maximum (Lemma) lands cleanly. No lens-scope annotation needed (the embedding is base-substrate, not a CL_TSML/CL_BHML projection).
- **Status (2026-05-07 finalization batch):** DRAFT. Manuscript at `manuscript/manuscript.tex` is complete (471 lines, AMS amsart class, 4 bibliography entries including J03 companion). Cover letter at `cover_letter.md` complete. Awaiting Brayden's referee-rigor pass.



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
- [ ] Per-venue cap check: this is the Nth paper to AMM this quarter
- [ ] Submitted

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Calderon. (2026). "Q17-A: 5D Force Vector as CRT Fourier Embedding of Z/10Z into R^5." Submitted to *AMM*.
