# Save Plan — J05: TSML 73 / BHML 28 cells (Experimental Mathematics)

**Date:** 2026-05-08
**Status:** REVISED — referee fixes + SFM family-structure framing applied
**Author lane:** Sanders + Gish

---

## §1 — What was done

J05 was revised to address the J05 fresh-eyes referee report (`Atlas/META_PLAN_2026-05-06/REFEREE_REPORTS/J05_ExpMath_FreshEyes.md`). The major referee critique was:

> "The mathematical content cannot be saved in its present form. To make a publishable paper at *Experimental Mathematics*, the authors would need to add at least one of: (1) Why these tables. A structural / algebraic / categorical reason TSML and BHML are the 'right' tables to study. ... (3) A genuine experimental phenomenon. ..."

The revised manuscript addresses this by adding §5 Family-Structure context, which records the five conjoint membership criteria (C1–C5) that locate $\TSML$ and $\BHML$ as canonical members of the TIG family of small commutative non-associative magmas on $\Z/10\Z$, with the joint $\{0, 7, 8, 9\}$-preservation as the load-bearing structural fact (cited from companion four-core paper). Drápal–Wanless 2021 *JCTA* is named as the closest published precedent.

## §2 — Per-referee-issue mapping

- **Issue 1** (Theorem 3 is a triviality): retained but reframed honestly as a consistency check (§4 Remark explicitly calls it "a tautology about the action"); the load-bearing structural distinction is the contrast with the lens-*dependent* joint-closure chain count of the four-core companion.
- **Issue 2** (TSML/BHML unmotivated): addressed by the new §5 family-structure section + Drápal–Wanless 2021 citation + the C1–C5 membership conditions.
- **Issue 3** (proofs are direct enumeration): retained as such; the manuscript now explicitly tier-classifies these as PROVEN via disjoint-zone enumeration in §0 (Tier discipline).
- **M1** (BHML symmetry asserted not stated): addressed; symmetry is now explicitly stated and the table values for R_89 are listed in Table 2.
- **M2** (echo pairs opaque): addressed; Table 1 lists all five echo pairs with values.
- **M3** (complementarity restricted to units): addressed by the new §6 (joint-cell statistics) which records the joint harmony intersection (26 cells) and union (75 cells) explicitly without invoking the unit-subgroup restriction.
- **M4** (counts not connected to anything): addressed by §5 (membership in the TIG family) and §6 (joint-cell statistics). The integers 73, 28, 26, 75 are recorded as part of the family's algebraic invariant catalogue.
- **M5** (license issue): addressed; `ck_tables.py` carries CC-BY-4.0; the legacy "7SiTe Public Sovereignty License" / "Human use only / no government use" / "TSML proprietary IP" language has been removed.
- **M6** (unused tables): addressed; the bundled `ck_tables.py` continues to define DIS, DOING, G, etc. as derived structures, but the manuscript references only TSML, BHML, and the joint-cell statistics. The verification scripts use only TSML and BHML.

## §3 — Family-Structure framing applied

§5 of the revised manuscript records the five conjoint membership criteria (C1–C5) per `Atlas/META_PLAN_2026-05-06/FAMILY_STRUCTURE_v1.md` §1:

1. **C1** Substrate $\Z/10\Z$
2. **C2** Commutativity (TSML and BHML are both commutative, the unique RAW non-commutative variant is an internal lens issue not addressed in J05)
3. **C3** Joint $\{0, 7, 8, 9\}$-preservation (load-bearing)
4. **C4** Bounded non-associativity index $\alpha_A \in [0.5, 0.88]$
5. **C5** HARMONY-attracting iterated mixing at $\alpha_M = 1/2$ with closed-form attractor $h/\beta = 1 + \sqrt{3}$ (D78 Galois)

The 4-core $\{V, H, Br, R\} = \{0, 7, 8, 9\}$ is the algebraic center of the family per FAMILY_STRUCTURE_v1.md §2. The 73 + 28 + (joint = 26) + (CL_STD's 44) integer counts characterize $\TSML$, $\BHML$, $\TSML \cap \BHML$ (joint harmony), and CL_STD respectively. Per the SFM v1.1 + SFM_FINDINGS_v1 results: the joint TSML+BHML+CL_STD chain is the same 8-shell chain as TSML+BHML alone (sizes {1, 4, 5, 6, 7, 8, 9, 10}; forbidden sizes {2, 3}). This is **referenced but not derived** in J05 — the chain count is the four-core companion paper's result, and J05 explicitly contrasts the lens-*dependent* chain count with its own lens-invariant cell counts.

## §4 — Boilerplate adoption

§0 of the revised manuscript carries the PROVEN/COMPUTED/STRUCTURAL RHYME/OPEN tier paragraph plus the lens-ownership paragraph per `Atlas/META_PLAN_2026-05-06/J_PAPER_BOILERPLATE.md`.

## §5 — License + author-lane discipline

- License: `ck_tables.py` CC-BY-4.0 (verified; legacy "7SiTe Public Sovereignty License" / "TSML proprietary IP" language removed)
- Author lane: Sanders + Gish (no AI-attribution; no Luther on J05's title block)
- Drápal–Wanless 2021 cited

## §6 — Verification status

Both verification scripts run green:
- `proof_d10_tsml_73_cells.py` → ALL ASSERTIONS PASSED
- `proof_d16_bhml_28_cells.py` → ALL ASSERTIONS PASSED
- `ck_tables.py` direct run → ALL TABLES READY FOR IMPORT (verifies symmetry, harmony counts, derived tables)

## §7 — Files modified

- `Gen13/targets/journals/J_series/J05/manuscript/tsml_bhml_cell_counts.tex` — fully rewritten
- `Gen13/targets/journals/J_series/J05/manuscript/ck_tables.py` — license header cleaned (removed proprietary IP language; CC-BY-4.0 only)
- `Gen13/targets/journals/J_series/J05/README.md` — updated to reflect revisions
- `Gen13/targets/journals/J_series/J05/cover_letter.md` — updated to reference family-structure framing

## §8 — Submission readiness

- [x] Manuscript revised
- [x] Verification scripts green
- [x] Tier discipline applied
- [x] Lens-ownership paragraph
- [x] Drápal–Wanless 2021 cited
- [x] CC-BY-4.0 on `ck_tables.py`
- [x] Family-structure framing §5
- [ ] Brayden's referee-rigor pass (manual)
- [ ] Submit
