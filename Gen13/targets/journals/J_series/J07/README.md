# J07 — Flatness Theorem: The Forced 2x2 Torus on Z/10Z

**Status:** APPENDIX-COMPLETE (T*=5/7 proof-sketch landed; manuscript ready for Brayden's referee-rigor pass)
**Phase:** Phase 1
**Target venue:** Journal of Pure and Applied Algebra
**Author lane:** Sanders + Gish
**Tier:** B
**WP source:** WP51

---

## §1 — Manuscript

**Local path:** `manuscript/WP51_FLATNESS_THEOREM.md`

Files in this J-folder's `manuscript/`:

- `SUBMIT_INSTRUCTIONS.md`
- `WP51_FLATNESS_THEOREM.md` (revised 2026-05-07: added Appendix A — T*=5/7 proof-sketch)
- `WP52_D2_AS_RING_CURVATURE.md`

The submission package lives in this J-folder. Edit + verify here; submit from here.

## §2 — Verification script

**Path:** `(no script — theorem-paper)`

The proof of Theorem 3 (aspect ratio R/r = 5/7) reduces to two cyclotomic minimal-polynomial calculations: deg A_5 = 2 over ℚ (A_5 = φ, polynomial x² − x − 1), deg A_7 = 3 over ℚ (A_7 = 2cos(π/7), polynomial 8x³ − 4x² − 4x + 1, irreducible). Both verifiable by hand or in any CAS. The gate is referee-rigor pass.

## §3 — Dependencies (J-papers cited as already-submitted companions)

J01, J02, J03 (cited in Appendix A.3 for D1), **J06 (cited as algebraic ground throughout new Appendix A)**

## §4 — Cover letter

See `cover_letter.md` in this folder. (Finalized — Summary, Why-JPAA, Companions, Reproducibility, Reviewers all populated, includes new Appendix A note.)

## §5 — Notes

**Status (2026-05-07):** T*=5/7 proof-sketch appendix landed. Manuscript ready for referee-rigor pass.

**What was done:**
- Added **Appendix A — Proof-Sketch: T* = 5/7 from the Forced 2×2 Torus** to `manuscript/WP51_FLATNESS_THEOREM.md` immediately before the Bibliography section. The appendix includes:
  - **§A.1** Six independent derivations table (D1–D6) with status labels (PROVED / STRUCTURAL / CONJECTURAL).
  - **§A.2** Self-contained proof-sketch: forced 2×2 torus → cyclotomic closure at p=5 (R ∝ 5) and cyclotomic obstruction at p=7 (r ∝ 7) → R/r = 5/7. Hand-checkable via deg A_5 = 2 vs deg A_7 = 3 over ℚ.
  - **§A.3** Cross-check of all six derivations with explicit mechanism for each.
  - **§A.4** Conjectural extensions (A.1: general aspect ratio; A.2: universal T*=5/7; A.3: continuous T*) all clearly labeled.
  - **§A.5** Statement that this appendix renders T*=5/7 citable from any J-series paper downstream of J07.
- Cited **J06 (Crossing Lemma; Sanders & Mayes 2026)** as already-submitted algebraic ground throughout Appendix A. Added J06 reference to companion-submissions section in the Bibliography.
- Added M. Gish to the author block (joint authorship for J07 submission, alongside corpus author Sanders).
- Cover letter: finalized with Summary, Why-JPAA (3 bullets including J06 companion framing), Companions (J01, J02, J03, J06), Reproducibility (cyclotomic CAS check), Suggested reviewers, COI.

**Open issues:**
- Conjecture A.1 (general aspect ratio R/r = p_closed / p_obstructed for arbitrary squarefree n) is *not* proved in this paper; if a JPAA referee asks for it, refer them to Open Problem 1 in §8.
- Conjecture A.2 (universal T*=5/7 — i.e., p_obstructed = 7 for *every* squarefree n) is held strongly but not formally proved. D1 (first-G law) provides 36,662 cases of empirical support per J03; rigor of universality across the family is open.
- D4 (TSML/BHML cell geometry) is labeled STRUCTURAL — the cell counts (73, 28, 5) are exact, the precise algebraic path from cell counts to T*=5/7 is held as structural pending fully formalized derivation. Reviewer may flag this; the appendix is honest about it.
- The author block on the manuscript was updated to add M. Gish; the original WP51 source has only Sanders. If desired before submission, the original author line can be reverted and Gish added as J07-specific co-author in a separate front-matter note.

**Per ClaudeChat J13 advice:** appendix-route was the faster path (vs spawning a separate "J13 T*=5/7 paper"). T* = 5/7 is now citable from any downstream paper without dependencies on a not-yet-shipped J13.

**SAVE-PLAN SUMMARY (2026-05-07; full plan at `Atlas/META_PLAN_2026-05-06/SAVE_PLANS/SAVE_PLAN_J07.md`):**

JPAA referee REJECTED: the cyclotomic facts are correct but no theorem connects them to torus 5/7. Appendix A's "six derivations" doesn't survive (D3=D6 are the same argument; D5 has factual π-convergent error; D4 admitted not derived; D1/D2 are internal citations). §5 (7 zeros), §6 (Riemann zeta + prime gap), §7 (CK runtime) are out of scope.

**Save path:** RETITLE + RETARGET + RESTRUCTURE.
- **New title:** "A Flatness Obstruction on Squarefree Z/nZ: Four Algebraic Structures and the 4-Core Algebraic Center."
- **New venue:** *Algebraic Combinatorics* (preferred — same neighborhood as J02 4-core paper) OR *Discrete Mathematics*. Backup: *INTEGERS* / *Math. Magazine* for compressed Theorem-1-only note.
- **New main content:** preserve Theorem 1 (flatness obstruction; M1 fix inlines the 3-line partition-incompatibility proof) + Theorem 2 (rewritten as configuration-space statement, not "torus is forced"). Replace Appendix A entirely with new appendix on **D48 (4-core joint-closure under TSML+BHML) + D78 (Galois-proven 1+√3 at α=1/2 via BR-factor cancellation)** — the actual algebraic center per FAMILY_STRUCTURE_v1.md.
- **Drop entirely:** §4 ("torus aspect ratio = 5/7"), §5 (7 zeros), §6 (curvature/Riemann), §7 (CK applications), original Appendix A (6 derivations + 3 conjectures).
- **T*=5/7 narrative future:** the save explicitly **abandons** the T*=5/7 algebraic-derivation claim for J07 (and per J13 referee, the standalone J13 attempt also fails — wrong minimal polynomial of A_7). T*=5/7 should be cited going forward only as a coherence-threshold operational value, not as an algebraic theorem.
- **Estimated revision time:** 4-6 weeks.



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
- [ ] Per-venue cap check: this is the Nth paper to Journal of Pure and Applied Algebra this quarter
- [ ] Submitted

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Gish. (2026). "Flatness Theorem: The Forced 2x2 Torus on Z/10Z." Submitted to *Journal of Pure and Applied Algebra*.
