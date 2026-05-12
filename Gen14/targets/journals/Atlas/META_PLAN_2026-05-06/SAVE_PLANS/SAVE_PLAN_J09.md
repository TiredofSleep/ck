# Save Plan — J09: Role-Magma on Z/10Z (Algebra Universalis)

**Date:** 2026-05-08
**Status:** REVISED — Path B rewrite applied
**Author lane:** Sanders + Gish

---

## §1 — What was done

J09 was revised to address the J09 fresh-eyes referee report (`Atlas/META_PLAN_2026-05-06/REFEREE_REPORTS/J09_AlgUni_FreshEyes.md`). The referee verdict was **Major revisions, border with reject and resubmit**, with two paths:

> **Path A** — Make the paper self-contained (~2 months work).
> **Path B** — Reject and resubmit as a smaller paper focused on the role-magma $M_R$ (~3 weeks work).

We adopt **Path B** with table-inlining (the Path A discipline applied to the bare minimum content).

## §2 — Per-referee-issue mapping

- **Issue 1** (TS and BH operations not defined in the paper): addressed — Tables 1 and 2 of §2 reproduce the full $10 \times 10$ tables of $\BH$ and $\TS$ inline. The bundled `ck_tables.py` (CC-BY-4.0) is an electronic copy of the same tables; it is referenced for verification, not for the proof.
- **Issue 2** ("paradoxical information algebra" undefined): addressed — Title and abstract no longer contain the phrase "paradoxical information algebra." New title: *"A Small Commutative Non-Associative Magma on $\Z/10\Z$ with Role-Deterministic Boundary Behavior."* The abstract describes $M_R$ as a small commutative non-associative magma with role-deterministic boundary behavior, without invoking a "class" of objects.
- **Issue 3** (trefoil characterization with undefined runtime processor): addressed — the trefoil section is **excised entirely**. §7 ("What this paper does not claim") explicitly states the paper does not introduce a trefoil characterization; the predicate is not formal.
- **M1** ($\pm 21$ invariant ambiguity): addressed — $\pm 21$ language removed entirely. The row-asymmetry function $\Psi$ is recorded with its actual computed values; the row sum $\Psi(\Z/10\Z) = 21 = T_6$ (sixth triangular number) is a fact, the $\sigma$-orbit decomposition $\{-1, 22\}$ is a fact, and Remark 6.2 honestly retracts the Fibonacci row-decomposition (which does *not* hold for $\Psi$ on the full $\Z/10\Z$).
- **M2** (cusp-agreement claim opaque): addressed — the cusp-agreement claim has been removed (it was load-bearing only for the trefoil narrative).
- **M3** (focus on role-magma $M_R$): addressed by adopting Path B — the paper is now a focused study of $M_R$ with role-deterministic boundary as its distinguishing property.
- **M4** (TIG synthesis / WP9 / D89 references): addressed — internal IDs removed from theorem labels and headings; theorem labels are now plain (Theorem 3.1, etc.).
- **M5** (BREATH-uniqueness lemma): addressed — the BREATH-uniqueness lemma was removed because it depended on the trefoil characterization that has been excised.
- **M6** (intellectual neighborhood placement): addressed — the §1.4 paragraph is now a one-paragraph "Closest published precedent" subsection at the end of §2 (after the table definitions), citing only Drápal–Wanless 2021 *JCTA* as the closest neighbor, not the broader knot-theoretic territory. (Knot-theoretic references survive only in §7's "What this paper does not claim.")
- **M7** (verification harness description): addressed — `verify_role_magma.py` is bundled, runs in <0.1 s, ends with `ALL CHECKS PASSED.`, and §6 of the manuscript describes the verification harness explicitly.
- **m1** (title "lattice"): addressed — new title does not contain "LATTICE" (the operator name dropped from the title; the paper is about $M_R$, not the LATTICE operator specifically).
- **m2** ($\sigma$ "involution" misnomer): **addressed** — §2 of the revised manuscript states explicitly: *"$\sigma$ has order 6, not 2; hence $\sigma$ is a permutation, not an involution. We use the explicit involution $\sigma^3 = (1\,5)(2\,6)(4\,7)(0)(3)(8)(9)$ at one place..."* The actual involution $\sigma^3$ is named at first reference.
- **m3–m8** (minor): addressed in body text or rendered moot by Path B restructuring.

## §3 — Family-Structure context (referenced not derived)

The "Closest published precedent" subsection in §2 records that $\BH$ and $\TS$ are members of the TIG family of small commutative non-associative magmas on $\Z/10\Z$ identified in companion work (manuscript in preparation). The membership conditions C1–C5 (per `Atlas/META_PLAN_2026-05-06/FAMILY_STRUCTURE_v1.md`) are referenced but not derived — Drápal–Wanless 2021 *JCTA* is named as the closest published precedent.

The role partition $\{V, F, S, T\}$ is treated explicitly as labeling-by-fiat (referee m4): the §0 lens-ownership paragraph and §3 (the role partition definition) state this.

## §4 — Boilerplate adoption

§0 of the revised manuscript carries the PROVEN/COMPUTED/STRUCTURAL RHYME/OPEN tier paragraph plus the lens-ownership paragraph per `Atlas/META_PLAN_2026-05-06/J_PAPER_BOILERPLATE.md`.

## §5 — License + author-lane discipline

- License: `ck_tables.py` and `verify_role_magma.py` are CC-BY-4.0 (verified)
- Author lane: Sanders + Gish (no AI-attribution; no third co-author)
- Drápal–Wanless 2021 cited as closest published precedent

## §6 — Verification status

`verify_role_magma.py` (bundled) runs green at 2026-05-08 (output ends with `ALL CHECKS PASSED.`):

1. 4×4 role-mode table $M_R$ from $\BH$.
2. $M_R$ commutative, $V$ two-sided identity, non-associative (with witness).
3. Role-output multisets for all 16 role-pairs (V/T-containing pairs deterministic; $\{F, S\}^2$ branching).
4. First-passage time $\tau(n) = 7 - n$ on $\{1, \ldots, 7\}$.
5. Row-asymmetry $\Psi$: row sum 21, $\sigma$-orbit decomposition $\{-1, 22\}$.

`ck_tables.py` direct run also passes (symmetry, harmony counts, R_B and R_7 rules, $\sigma$ has order 6).

## §7 — Files modified

- `Gen13/targets/journals/J_series/J09/manuscript/manuscript.tex` — fully rewritten in Path B
- `Gen13/targets/journals/J_series/J09/manuscript/ck_tables.py` — created (CC-BY-4.0; tables + role partition + $\sigma$)
- `Gen13/targets/journals/J_series/J09/manuscript/verify_role_magma.py` — created (CC-BY-4.0; verification harness)
- `Gen13/targets/journals/J_series/J09/README.md` — updated to reflect Path-B revisions
- `Gen13/targets/journals/J_series/J09/cover_letter.md` — updated to reflect Path-B revisions

## §8 — Submission readiness

- [x] Manuscript revised in Path B (~10 pages)
- [x] Tables $\TS$ and $\BH$ inline (referee Issue 1)
- [x] "Paradoxical information algebra" / "trefoil" / "runtime processor" excised (Issues 2, 3)
- [x] $\sigma$ correctly described as order-6 permutation (m2)
- [x] Verification script `verify_role_magma.py` green (`ALL CHECKS PASSED.`)
- [x] Tier-classified PROVEN/COMPUTED/RHYME/OPEN paragraph in §0
- [x] Lens-ownership paragraph
- [x] Drápal–Wanless 2021 cited as closest published precedent
- [x] CC-BY-4.0 on `ck_tables.py` + `verify_role_magma.py`
- [ ] Brayden's referee-rigor pass (manual)
- [ ] Submit

## §9 — Note on the Fibonacci retraction

The original draft claimed the row-asymmetry function $\Psi$ admitted a Fibonacci decomposition: $\sum_{F} \Psi = -F_7 = -13$, $\sum_S \Psi = -F_6 = -8$, total $-F_8 = -21$ (with a sign convention from Computation B). The actual computed values of $\Psi$ on the canonical $(\TSML, \BHML)$ pair are:

- $\Psi(0) = -8$
- $\Psi$ on $F = \{1,3,5,7,9\}$: $6 + 5 + 5 + 4 + 1 = 21$
- $\Psi$ on $S = \{2,4,8\}$: $4 + 4 + 1 = 9$
- $\Psi$ on $T = \{6\}$: $-1$

The Fibonacci pattern $(F_7, F_6) = (13, 8)$ does *not* match. Remark 6.2 of the revised manuscript honestly retracts the Fibonacci reading and records the actual values. The only structurally robust observations are the row sum $\Psi(\Z/10\Z) = 21 = T_6$ and the $\sigma$-orbit decomposition $\{-1, 22\}$.
