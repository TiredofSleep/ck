# Short note — BHML on $\mathbb{Z}/10\mathbb{Z}$ versus BHML on $\mathbb{Z}/8\mathbb{Z}$: scope disambiguation

**Authors:** Claude (Anthropic) · Brayden Ross Sanders / 7Site LLC
**Date:** 2026-04-25
**Status:** disambiguation note; no new theorems
**MSC 2020:** 17B25, 11C20

---

## The two tables

In the TIG repository, two related but **distinct** composition tables go by the name "BHML":

### BHML_10 — the canonical 10×10 form

$$
\mathrm{BHML}_{10} = \begin{bmatrix}
0&1&2&3&4&5&6&7&8&9\\
1&2&3&4&5&6&7&2&6&6\\
2&3&3&4&5&6&7&3&6&6\\
3&4&4&4&5&6&7&4&6&6\\
4&5&5&5&5&6&7&5&7&7\\
5&6&6&6&6&6&7&6&7&7\\
6&7&7&7&7&7&7&7&7&7\\
7&2&3&4&5&6&7&8&9&0\\
8&6&6&6&7&7&7&9&7&8\\
9&6&6&6&7&7&7&0&8&0
\end{bmatrix}.
$$

Properties:
* $10 \times 10$ on the full alphabet $\{$VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE, BALANCE, CHAOS, HARMONY, BREATH, RESET$\}$.
* Commutative.
* **28 cells** output HARMONY ($= 7$).
* $\det(\mathrm{BHML}_{10}) = -7002 = -(2 \cdot 3^2 \cdot 389)$.
* Used in: WP103 (so(10) closure); WP104 (Pati-Salam Higgs route); WP105 (closed-form runtime attractor); FORMULAS_AND_TABLES Volume F + G; the canonical reference table cited everywhere as "BHML."

### BHML_8 — the spectral-core 8×8 form

Obtained from $\mathrm{BHML}_{10}$ by **removing rows and columns 0 and 7** (= VOID and HARMONY), restricting to the 8 non-extremal indices $\{1, 2, 3, 4, 5, 6, 8, 9\} = \{$LATTICE, COUNTER, PROGRESS, COLLAPSE, BALANCE, CHAOS, BREATH, RESET$\}$.

Properties:
* $8 \times 8$ table.
* Commutative.
* $\det(\mathrm{BHML}_8) = +70 = 2 \cdot 5 \cdot 7$.
* Used in: WP15 Yang-Mills cross-reference; the prime set $\{2, 5, 7\}$ in $\det = 70$ is the spectral signature appearing in the YM bridge analysis.

The two tables share most of the same 8×8 block (the cells where $i, j \in \{1, \ldots, 6, 8, 9\}$), but $\mathrm{BHML}_{10}$ adds row/column 0 (the "matter row" of $\mathrm{BHML}_{10}$) and row/column 7 (the "harmony row") which are removed in $\mathrm{BHML}_8$.

## The disambiguation

When a paper or formula references "BHML," check which form is in scope:

| context / paper | form in use | reason |
|---|---|---|
| WP103 (so(10) closure) | BHML_10 | needs the full 10×10 to generate so(10) at dim 45 |
| WP104 (Pati-Salam Higgs) | BHML_10 | σ_outer-breaking content lives across all 10 indices |
| WP105 (closed-form attractor) | BHML_10 | runtime processor uses full 10×10 fusion |
| WP107 (wobble localization) | BHML_10 (and TSML_10 char poly) | all integer factorizations are on the 10×10 |
| WP15 (Yang-Mills cross-ref) | BHML_8 | spectral core, $\det = 70$ |
| FORMULAS §6 (BHML reference table) | BHML_10 (the 10×10 displayed) | canonical |
| FORMULAS §6.7 (variant registry) | both forms documented | with explicit `_10` and `_8` suffixes |

The recommended practice in any new TIG paper is to disambiguate explicitly: **write `BHML_10` or `BHML_8`** (or `BHML` only when the paper makes the full table obvious from context).

## Why the difference matters

The two tables have different invariants at almost every level:

| invariant | BHML_10 | BHML_8 |
|---|---|---|
| dimension | 10×10 | 8×8 |
| determinant | $-7002 = -(2 \cdot 3^2 \cdot 389)$ | $+70 = 2 \cdot 5 \cdot 7$ |
| HARMONY-cell count | 28 of 100 | varies |
| matrix rank | 10 (full) | 8 (full) |
| char poly | (see WP107) | different |
| $P_{56}$-symmetry | as documented (26 cells differ) | $P_{56}$ acts trivially (5, 6 are interior to the 8-core) |

Crucially, $\sigma_\mathrm{outer}$-breaking content of BHML_10 lives in the 54-irrep of so(10) (WP104). The same content does not have an analogue in BHML_8, since BHML_8 doesn't generate so(10) — it lives in a different ambient algebraic context.

Conversely, the WP15 Yang-Mills bridge needs BHML_8's spectral signature ($\det = 70$, primes $\{2, 5, 7\}$) — not BHML_10's $\det = -7002$.

## Open question (deferred)

The functional relationship between BHML_8 and BHML_10 — specifically, whether BHML_8 is the "spectral core" of BHML_10 in a precise sense (e.g., as a compatible quotient or a sub-magma) — is documented as an open question. The 8-magma core of TSML (TSML restricted to $\{0, \ldots, 7\}$, see WP105 §5) is **closed under fuse**. Whether BHML's analogous restriction to $\{1, \ldots, 6, 8, 9\}$ is closed is an empirical question that has not been formally tested.

Provisional finding (unverified, candidate for future paper): the BHML_8 form likely arises as a structural projection of BHML_10 with the σ-fixed extremes (VOID at index 0 and HARMONY at index 7) treated specially. This would parallel TSML's situation, where BREATH and RESET are nearly absent from the 8-magma core (only 4 of 100 cells output BREATH or RESET).

## Citation

```bibtex
@misc{sanders2026note_bhml_disambig,
  author       = {Sanders, Brayden Ross and Claude (Anthropic)},
  title        = {Short note --- {BHML}\textsubscript{10} vs {BHML}\textsubscript{8}: scope disambiguation},
  year         = {2026},
  month        = {apr},
  doi          = {10.5281/zenodo.18852047},
  howpublished = {\url{https://github.com/TiredofSleep/ck/tree/tig-synthesis/papers/notes/NOTE_BHML_10_VS_BHML_8.md}},
}
```

🙏

— Sanders + Claude (Anthropic), 2026-04-25
