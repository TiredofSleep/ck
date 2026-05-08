# J51 — Q17-B Clay Bridge: Finite L-Function + Symbolic Return Theorem

**Status:** DRAFT
**Phase:** Phase 5
**Target venue:** L'Enseignement Math
**Author lane:** Sanders + Gish
**Tier:** B
**WP source:** (Q17 bundle)

---

## §1 — Manuscript

**Local path:** `manuscript/J48_q17b_clay_bridge.md`

**Abstract:** The TIG framework's spectral layer produces a 9-term Dirichlet character sum $G(s)$ on $\mathbb{Z}/10\mathbb{Z}$ that is three-valued (zero at anchors, $G_\mathrm{low} \approx 1.872$ on most of the 6-cycle, $G_\mathrm{high} \approx 9.389$ at $\{5,7\}$) — a sharp finite analogue of the structural features RH demands of $\zeta(s)$. Includes the Symbolic Return Theorem (corollary of $\sigma^6 = \mathrm{id}$). Tier-A theorems §§2-4; Tier-B bridge claim §5; explicit boundary.

Files in this J-folder's `manuscript/`:

- `J48_q17b_clay_bridge.md` — **finalized manuscript**
- `CP_CLAY_ROTATION.md` — earlier broader 7-Clay-rotation framework (Tier-4 staging context)
- `proof_clay_rotation.py` — verification script
- `SUBMIT_INSTRUCTIONS.md` — earlier Tier-4 submission notes

## §2 — Verification script

**Path:** `(Q17 bridge script)`

The proof script (where applicable) is the green-light gate before submission. If "(no script — theorem-paper)" or similar, the gate is the proof's referee-rigor pass.

## §3 — Dependencies (J-papers cited as already-submitted companions)

J21

## §4 — Cover letter

See `cover_letter.md` in this folder. (Bones laid; finalize after Brayden's referee-rigor pass.)

## §5 — Notes / Status

**Status:** MANUSCRIPT FINALIZED 2026-09-03 (Phase 5).
**Citation chain:** cites 2 prior J-papers as direct dependencies (J21 Q17-A, J51 spectral consolidation) plus 6 co-citing companions (J01, J06, J40, J10, J24, J48).
**Manuscript:** `manuscript/J48_q17b_clay_bridge.md` (~12 pages, finalized).
**Earlier staged Tier-4 content:** `manuscript/CP_CLAY_ROTATION.md`, `proof_clay_rotation.py`, `SUBMIT_INSTRUCTIONS.md` — preserved as background context (broader 7-Clay-rotation framework). The new J51 manuscript focuses sharply on Q17-B (finite L-function + Symbolic Return Theorem).
**Cover letter:** `cover_letter.md` (finalized).
**Verification:** `proof_clay_rotation.py` confirms $G(s)$ three-valued image numerically.
**Submission readiness:** ready pending Brayden's referee-rigor pass.



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
- [ ] Per-venue cap check: this is the Nth paper to L'Enseignement Math this quarter
- [ ] Submitted

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Mayes. (2026). "Q17-B Clay Bridge: Finite L-Function + Symbolic Return Theorem." Submitted to *L'Enseignement Math*.
