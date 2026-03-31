# clay/research/ — Research Documents for Expansion Agents

*Brayden Ross Sanders (7Site LLC) | March 2026*

---

## Purpose

This folder contains research support documents for expansion agents. These are NOT
draft papers — they are structured preparation documents containing citation lists,
section outlines, and formalized claim inventories. A full-paper expansion agent should
read these documents, read the source WPs they cite, and then write the complete papers.

Do NOT commit these as papers. They are working material.

---

## Contents

### WP36_SPECTROMETER_RESEARCH.md
**For paper:** WP36 — "The CK Coherence Spectrometer: Measuring the Six Clay Problems
Through Dual-Lens Algebraic Curvature, First-G Boundaries, and Harmonic Pre-Echo"

Contains:
- **Section A:** 40 citations covering internal TIG WPs, Clay problem statements (all 6),
  coherence/physics papers (Kuramoto, Strogatz), algebraic complexity (Hardy-Ramanujan,
  Andrews), sinc²/Fejér kernel literature, recent Clay results (Markman 2025 Hodge),
  information theory (Shannon, JSD), and Baez/Hurwitz for non-associativity.
- **Section B:** 7-section academic outline with 5-6 bullet points per subsection.
  Every claim is labeled: PROVED (cite WP34/WP35), CONJECTURE (open), STRUCTURAL (analogy),
  or EMPIRICAL (measured, not derived).
- **Section C:** 13 key claims with proof status, proof sketches, and kill conditions.

Key focus: The harmonic pre-echo R(k,f) = sin²(πk/f)/(k²sin²(π/f)) as the spectrometer
signal; T* = 5/7 as algebraically derived threshold; VOID/HARMONY partition of Clay problems;
Luther's dispersion conjecture as the boundary geometry between gap and affirmative problems.

### WP37_PNP_RESEARCH.md
**For paper:** WP37 — "P vs NP Through the First-G Lens: Zero-Width Phase Transitions,
Algebraic Certificates, and the Luther Dispersion Boundary"

Contains:
- **Section A:** 38 citations covering Cook 1971, Karp 1972, Levin 1973 (NP-completeness
  foundations), Baker-Gill-Solovay / Razborov-Rudich / Aaronson-Wigderson (three barriers),
  circuit lower bounds (Razborov, Håstad, Smolensky), GCT (Mulmuley-Sohoni I & II),
  non-associativity (Baez Octonions, Hurwitz), proof complexity (Ben-Sasson-Wigderson),
  SAT phase transitions (Mézard, Monasson, Achlioptas), and Wigderson's survey.
- **Section B:** 8-section outline. Includes: where the First-G/P analogy holds and where
  it breaks; the formal claims that must be proved to make the argument rigorous;
  the barrier evasion argument; the ω(b)/polynomial hierarchy structural parallel;
  the survivor-line NP-hardness conjecture; honest statement of what WP37 cannot prove.
- **Section C:** 14 key claims. PROVED tier (First-G Law, zero-width transition,
  non-associativity rate, 2-step convergence). NEEDS PROOF tier (SAT requires 7-DoF,
  P is associative, SLS is NP-hard). CONJECTURE/STRUCTURAL tier (Luther dispersion,
  ω/PH parallel, barrier evasion, three-barriers check).

Key focus: Precision about what is proved vs. structural. The formal bridge required
to connect CL algebra to general computation (the central missing step). Luther's
dispersion as the geometric certificate of NP difficulty.

---

## Source Documents Read Before Creating These Files

All of these were read in full to ground the research documents:

| File | Key content used |
|------|-----------------|
| `WP34_FIRST_G_LAW.md` | First-G Law proof, Luther dispersion conjecture, ω-hierarchy, pre-echo survey, corridor atlas, closed form derivation |
| `WP35_PRIME_PHASE_TRANSITION.md` | Theorems 1-4, T* = 5/7 derivation, zero-width transition, ω-blindness, kinematic factoring, seeded RPS |
| `clay/WHITEPAPER_7_CLAY_SPECTROMETER.md` | TSML/BHML tables, D1/D2/CL pipeline, 6-problem calibration data, Theory of Nothing, VOID/HARMONY partition, JSD defect |
| `clay/WP25_P_NP_AG2P_COMPLEXITY.md` | Survivor-line structure, corner-gap dichotomy, SLS(p) conjecture, 2-step convergence theorem |
| `clay/WHITEPAPER_16_P_NP_SYNTHESIS.md` | DoF ladder, non-associativity rate (49.8%), Lemmas A/B/C, barrier evasion argument, Baez/Hurwitz connection |
| `sprint4_2026_03_30/ATLAS_LAW_SET.md` | Three laws (construction, HAR, richness), b=15 uniqueness proof, three-score system |
| `sprint4_2026_03_30/UNIVERSAL_LAW.md` | Four-step construction law, hardness landscape, b=22 flagship |

---

## Status Classification Used in Research Documents

| Label | Meaning |
|-------|---------|
| PROVED | Algebraic proof exists in cited WP; finitely verified |
| EMPIRICAL | Measured computationally; no algebraic proof |
| NEEDS PROOF | Formal claim stated; proof strategy given; not complete |
| CONJECTURE | Plausible; no formal proof strategy yet |
| STRUCTURAL | Analogy to established mathematics; not a formal reduction |

---

## Notes for Expansion Agent

1. Read WP34 and WP35 completely before expanding WP36 — all proved theorems are there.
2. Read WP16 (WHITEPAPER_16_P_NP_SYNTHESIS.md) and WP25 before expanding WP37.
3. All PROVED claims can be stated as theorems with proofs in the final paper.
4. CONJECTURE and NEEDS PROOF claims should be labeled clearly; do not present them as proved.
5. Luther's dispersion conjecture appears in both papers as the central open question —
   treat it consistently.
6. CK is Brayden's creature; the TIG/CK architecture is explicitly Sanders / 7Site LLC
   intellectual property. Luther's contribution is the dispersion conjecture applied to
   the number theory. Be precise about attribution.
7. Do not conflate "structural analog" with "formal reduction." Both papers make
   structural claims; WP37 in particular must be honest that it does not prove P ≠ NP.
