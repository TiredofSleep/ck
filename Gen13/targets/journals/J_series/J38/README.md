# J38 — Yukawa Scaffolding from the 9-Vector VEV

**Status:** DRAFT (manuscript finalized 2026-05-07; awaits referee-rigor pass; **scaffolding paper — does NOT complete the Yukawa computation**)
**Phase:** Phase 4
**Target venue:** PRD (FALLBACK NEEDED — 4th PRD paper this quarter, exceeds per-venue cap)
**Author lane:** Sanders + Gish
**Tier:** C
**WP source:** WP108
**Lens scope:** TSML_SYM derivation route via WP103 so(10); the 9-vector VEV norm $\|v\|^2 = 13/4$ is lens-stable

---

## §1 — Manuscript

**Local path:** `manuscript/manuscript.md`

The J38 paper is **Yukawa Scaffolding from the 9-Vector VEV** (WP108). A scaffolding paper that sets up the Yukawa-coupling computation from the 9-vector VEV identified in J31 (WP104, Path A: BHML's σ_outer-breaking content lives 100% in the $\mathbf{54}$ irrep of $\mathfrak{so}(10)$, with explicit 9-vector squared norm $\|v\|^2 = 13/4$).

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
- [x] Verification: scaffolding paper, no standalone script (load-bearing input verified in J31)
- [x] Tier-classified central claim explicit (Tier C — sets up framework, no completed prediction)
- [x] Lens-scope annotation (TSML_SYM derivation route)
- [ ] Cover letter finalized (bones laid; awaits referee-rigor pass)
- [x] Dependencies → cite each J-companion as "submitted to [venue]"
- [ ] Brayden's referee-rigor pass complete
- [ ] **Per-venue cap check: 4th PRD paper this quarter — FALLBACK NEEDED to *Mod Phys Lett A* or hold until next quarter**
- [ ] Submitted

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Mayes. (2026). "Yukawa Scaffolding from the 9-Vector VEV." Submitted to *PRD* (or fallback per cap).
