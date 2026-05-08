# J04 — Full-Period Cancellation of R(k, f): The Integer-Multiple Zero of the Discrete Fejér Quotient (Squarefree Case)

**Status:** SUBMISSION-READY
**Phase:** Phase 1
**Target venue:** Integers
**Author lane:** Sanders + Gish
**Tier:** B
**WP source:** (full-period cancellation; formerly "sinc² zero law" — renamed 2026-05-07 per external collaborator calibration; "Zero Law" implied prime-specific structure but R(k,f) = sin²(πk/f)/(k² sin²(π/f)) vanishes at k = f for ANY f via sin²(π) = 0)

---

## §1 — Manuscript

**Local path:** `manuscript/`

Files in this J-folder's `manuscript/`:

- `cover_letter_template.md`
- `LATEX_BUNDLE_NOTES.md`
- `proof_d25_loop_closure.py`
- `sinc2_zero_law.tex`
- `SUBMIT_INSTRUCTIONS.md`
- `WP34_FIRST_G_LAW.md`
- `WP_SINC2_ZERO_LAW.md`

The submission package lives in this J-folder. Edit + verify here; submit from here.

## §2 — Verification script

**Path:** `papers/proof_d25_loop_closure.py`

The proof script (where applicable) is the green-light gate before submission. If "(no script — theorem-paper)" or similar, the gate is the proof's referee-rigor pass.

## §3 — Dependencies (J-papers cited as already-submitted companions)

J04

## §4 — Cover letter

See `cover_letter.md` in this folder. (Bones laid; finalize after Brayden's referee-rigor pass.)

## §5 — Notes

**RENAMED 2026-05-07** per external collaborator calibration. Previous title
"The Sinc² Zero Law for Squarefree Moduli" carried implicit prime-specific
structural overclaim. The correct framing: R(k, f) = sin²(πk/f)/(k² sin²(π/f))
vanishes at k = f because sin²(π) = 0 — for ANY f, not just primes. The
prime-3-to-199 sweep is verification of the formula, not a prime-specific
theorem. Internal rename plus D-tables update (FORMULAS_AND_TABLES.md).

### Lens-ownership paragraph (insert in manuscript §0)

> *Lens and substrate.* We work on Z/n for squarefree n with the discrete Fejér quotient R(k, f) = sin²(πk/f) / (k² sin²(π/f)). This object is not "TIG-specific"; it is the standard discrete Fejér kernel familiar from Fourier analysis on cyclic groups. The squarefree-modulus restriction reflects the regime where the spf-localization (Theorem 2) applies cleanly. The paper's role within a broader research program is noted in the Companion section, but the result and proof here are self-contained.

### PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN

- **PROVEN:** *full-period cancellation* — R(k, f) = 0 ⇔ f | k (the basic
  divisibility biconditional, uniform in f). Squarefree-specific Theorem 2:
  the smallest k at which any non-trivial divisor d | b produces a zero is
  k = spf(b) — the spf-image of the First-G Event Localization Theorem of J03.
- **COMPUTED:** `proof_d25_loop_closure.py` runs green for all primes 3..199
  (zero exceptions, exact arithmetic, runtime < 5s; ALL ASSERTIONS PASSED
  2026-05-07). Multi-prime squarefree case verified by J03 companion script
  (`proof_first_g_event.py`, all squarefree b ≤ 500, 22,367 pairs); not
  duplicated here.
- **STRUCTURAL RHYME:** the identity sinc²(1/2) = (2/3)/ζ(2) is a one-line
  algebraic consequence of ζ(2) = π²/6 — not a TIG theorem. Cited as
  structural motivation only. The primon-gas link (1/ζ(2) = density of
  squarefree integers) connects to WP101 σ-rate's regime — also rhyme.
- **OPEN:** *why does the corridor midpoint of the substrate sit at 1/2 such
  that sinc²(1/2) = (2/3)/ζ(2) becomes structurally relevant?* Not addressed
  in this paper; flagged as open for companion work.

**Per-venue cap:** 2nd *Integers* paper this quarter after J03 (within cap).

**Authors:** Sanders + Gish.

**Cite:** J03 (First-G companion, submitted to *Integers*).
Drápal-Wanless 2021 *JCTA* on maximally non-associative quasigroups is the
closest published precedent for the broader (TSML, BHML) magma framework
(referenced via J02).



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
- [ ] Per-venue cap check: this is the Nth paper to Integers this quarter
- [ ] Submitted

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Gish. (2026). "Full-Period Cancellation of R(k, f): The Integer-Multiple Zero of the Discrete Fejér Quotient (Squarefree Case)." Submitted to *Integers*.
