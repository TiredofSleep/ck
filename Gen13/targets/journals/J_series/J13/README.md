# J13 — The Forced 5/7 Torus Aspect Ratio: Cyclotomic Forcing

**Status:** DRAFT
**Phase:** Phase 2
**Target venue:** Acta Arithmetica
**Author lane:** Sanders + Gish
**Tier:** A/B
**WP source:** (forced-torus 5/7)

---

## §1 — Manuscript

**Path:** `(corpus: forced-torus 5/7 derivation)`

When the manuscript is in this J-folder, replace this section with a 1-2 sentence abstract and a path-link to the .tex / .md file.

## §2 — Verification script

**Path:** `(cyclotomic forcing script)`

The proof script (where applicable) is the green-light gate before submission. If "(no script — theorem-paper)" or similar, the gate is the proof's referee-rigor pass.

## §3 — Dependencies (J-papers cited as already-submitted companions)

J07

## §4 — Cover letter

See `cover_letter.md` in this folder. (Bones laid; finalize after Brayden's referee-rigor pass.)

## §5 — Notes

T* derivation. Companion to J07 Flatness Theorem.

**Save-plan summary (2026-05-07):** see `Atlas/META_PLAN_2026-05-06/SAVE_PLANS/SAVE_PLAN_J13.md` for the full plan.

The fresh-eyes referee report (`Atlas/META_PLAN_2026-05-06/REFEREE_REPORTS/J13_ActaArith_FreshEyes.md`) flagged two hard errors plus four structural issues. Both hard errors are fixed in `manuscript/manuscript.tex`:

- **Error 1 (M1):** The polynomial $8x^3 - 4x^2 - 4x + 1$ originally cited as the minimal polynomial of $A_7 = 2\cos(\pi/7)$ is actually the minimal polynomial of $\cos(\pi/7)$. The correct minimal polynomial of $A_7$ is $x^3 - x^2 - 2x + 1$. Sympy-verified. Both are degree-3 irreducible, so the structural conclusion (deg-3 obstruction at $p = 7$) is preserved; the manuscript now cites the correct polynomial.
- **Error 2 (M2):** Lemma 4.2 evaluated $f(-1/2) = 3$ when the correct value (for the paper's original polynomial) is $1$ — error in the cube's sign. Moot after M1 fix; rewritten using the correct polynomial $g(x) = x^3 - x^2 - 2x + 1$, where the rational root test reduces to $g(1) = -1, g(-1) = 1$.

Structural corrections (M3–M6, m1–m8):

- **M3 — Calibration retreat.** Theorem 1.1 is retitled "Cyclotomic-calibrated 5/7 aspect ratio" and explicitly conditioned on a new Definition 2.4 (cyclotomic-embedding calibration). The forcing is conditional on this calibration, which is itself imported from J07 (Flatness Theorem). Open question (b) added: a calibration-free derivation would make 5/7 unconditional. Paper retitled "**The Forced 5/7 Torus Aspect Ratio (Up to a Calibration Choice)**".
- **M4 — Companion derivations honesty pass.** §6 reorganized: two were reformulations of the same theorem (so labeled), two are independent appearances of the same threshold (not independent derivations of the ratio itself), two were deleted entirely (BTQ balance and the $5/7 = (\sin(\pi/5)\sin(\pi/7))^?$ bridge had no self-contained content). The earlier claim that $73/101 = 5/7$ exactly is **retracted**: $73/101 - 5/7 = 6/707 \approx 1.2\%$, recorded as an open numerical question.
- **M6 — Conjecture scope restricted.** Conjecture 7.1 now requires that some prime divisor $p_i \mid n$ has $A_{p_i}$ irrational and degree $\le 2$ over $\mathbb{Q}$. New Proposition 7.2 identifies the domain as $\{n : 5 \mid n, \text{squarefree}, n > 5\}$. Cases $n = 14, 21$ (with $7 \mid n$) are explicitly outside the conjecture.
- **m1, m3, m4, m7:** duplicate `\author` blocks fixed; "narrow-major" terminology replaced; abstract uses precise language; "structural 7 zeros" deleted from open questions.

**What survives.** The structural deg-2 / deg-3 cyclotomic obstruction (the cyclotomic threshold between $p = 5$ and $p = 7$) is real and is what drives the $5/7$ ratio under the calibration. Conditional on the cyclotomic-embedding calibration, the theorem is now rigorous and verifiable. The $73/101$ "near-derivation" is honestly demoted from claim to open problem.

**Retarget recommendation.** Acta Arithmetica is likely still the wrong venue — the result is a calibration-conditional cyclotomic threshold theorem, which fits **Integers** (open access, short notes) better. Alternative: fold into J07 retarget. Brayden's call.

**Manuscript state.** `manuscript/manuscript.tex` revised in place; LaTeX environment balance verified (30 begin / 30 end, all matched); ready for Brayden's referee-rigor pass (~1 hour to submission-ready).

---

**Original note (2026-05-07):**

- Manuscript: `manuscript/manuscript.tex` — amsart, ~10 pages. Source: WP51 Section 4 ("The Aspect Ratio R/r = T* = 5/7") at `Gen12/targets/clay/papers/sprint10_flatness_2026_04_06/WP51_FLATNESS_THEOREM.md`.
- Cover letter: `cover_letter.md` (needs update to reflect calibration-conditional framing).
- Companion citation: J07 (Flatness Theorem, JPAA) cited as parent result. J03 (First-G Law, Integers) cited for the sinc^2 framework. J06 (Crossing Lemma, JCT-A) cited for incompatible CRT factor partitions. J10 (UOP, JNT) cross-cited.
- Independent of J10–J12 chain: separate cyclotomic argument; does not depend on UOP for its proof.



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
- [ ] Per-venue cap check: this is the Nth paper to Acta Arithmetica this quarter
- [ ] Submitted

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Mayes. (2026). "The Forced 5/7 Torus Aspect Ratio: Cyclotomic Forcing." Submitted to *Acta Arithmetica*.
