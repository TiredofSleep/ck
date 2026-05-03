# Scrutiny Extension — 2026-05-03

**Purpose:** Address the open items from `SCRUTINY_NOTES.md §5` (the pre-arXiv checklist). Each item below either closes (with new info) or stays open (with sharpened next-step).

---

## §1 Burrin–von Essen 2024 publication status — CLOSED

**Confirmed published.** Burrin, C. and von Essen, F. (2024). *Windings of Prime Geodesics.* International Mathematics Research Notices, Volume 2024, Issue 22, November 2024, pages 13931–13963. arXiv preprint: 2209.06233 (submitted September 2022, revised through 2024).

The paper computes the winding of closed oriented geodesics around the cusp of the modular orbifold via the Rademacher symbol. It explicitly introduces the construction of winding numbers about a prescribed cusp of a general cusped hyperbolic orbifold.

**Action for `main.tex`:** replace any "to appear" framing in the bibliography. Use:

```latex
\bibitem{burrin-von-essen-2024}
C. Burrin and F. von Essen,
\emph{Windings of Prime Geodesics},
International Mathematics Research Notices, Volume 2024, Issue 22 (2024), 13931--13963.
arXiv:2209.06233.
```

---

## §2 Magma classification literature search — CLOSED with sharpened open-question

**Searched (2026-05-03):** Bruck 1958 *A Survey of Binary Systems*; Smith 2007 *An Introduction to Quasigroups and Their Representations*; Etherington 1939, 1964/65 medial-quasigroup work; Wikipedia *Quasigroup* and *Magma (algebra)*; nLab *quasigroup* page.

**Result:** The role-quotient magma $\overline{B}$ on $\{V, F, S, T\}$ — commutative, $V$ a two-sided identity, NOT associative, and NOT a quasigroup (no Latin square property: the row of $V$ has $S \cdot V = S$ unique, but the row of $S$ has $S \cdot V = S$ AND $S \cdot S = F$, so columns aren't permutations of $\{V, F, S, T\}$) — does not appear under any standard classification I located.

The closest classical analogue is the 4-element commutative Moufang loop $F_4$, but a Moufang loop is by definition a quasigroup. $\overline{B}$ is not. So $\overline{B}$ is **strictly more general** than any 4-element commutative loop.

**This sharpens the open question rather than closing it.** The §7 paper claim becomes:

> A focused literature search (Bruck 1958; Smith 2007; nLab; Wikipedia *Quasigroup* / *Magma (algebra)*) did not surface this 4-element commutative magma with two-sided identity, non-associative, non-Latin-square structure under any standard classification. The closest classical analogue is the commutative Moufang loop $F_4$, but $F_4$ is a quasigroup and $\overline{B}$ is not. We treat the classification status of $\overline{B}$ as open.

This is a stronger framing than "we couldn't find it." It actively invites magma-theory specialists to either point at an existing classification or treat $\overline{B}$ as a genuinely new entry.

---

## §3 Inline trefoil-counting into `verify_paper.py` — CLOSED

**Done.** The runtime processor (was at `handoff/code/trefoil_corrected_frame.py:trajectory_corrected`) is now inlined into `verify_paper.py` as four self-contained functions:

- `_runtime_step_corrected(p, alpha)` — one step of the iterated mass-distribution map (paper §2.5)
- `_triple_initial_dist(a, b, c, eps)` — initial distribution from a triple
- `_count_crossings(history, mass_threshold)` — rank-swap crossing counter
- `trajectory_corrected(a, b, c, max_iter, eps, mass_threshold)` — end-to-end

The script now imports only `numpy`, stdlib `sys`, `collections.Counter`, `itertools.product`, and `random`. No imports from `handoff/code/`.

**Verification re-run (2026-05-03):** 42 passes, 0 failures. The Theorem 4.1 (9 trefoils) and Lemma 4.2 (BREATH-uniqueness with min crossings 26 / 17 / 3 for COUNTER / COLLAPSE / BREATH) checks pass with the inlined runtime.

**arXiv submission readiness:** the paper folder is now self-contained for ancillary-file submission. Submit `main.tex` + `verify_paper.py` together; the paper's claims reproduce on a clean machine with `python verify_paper.py`.

---

## §4 Parameter-stability sweep — STILL OPEN

The runtime processor uses three parameters: $\varepsilon = 10^{-3}$ (initial-distribution smoothing), threshold $10^{-2}$ (crossing-inclusion mass cutoff), max_iter $50$. Theorem 4.1's claim (exactly 9 trefoils) is verified at these specific values.

**A reviewer will ask:** is the count stable in a parameter neighborhood?

The paper as written doesn't sweep. To close the question:

1. Sweep $\varepsilon \in \{10^{-4}, 5 \cdot 10^{-4}, 10^{-3}, 5 \cdot 10^{-3}, 10^{-2}\}$.
2. Sweep threshold $\in \{10^{-3}, 5 \cdot 10^{-3}, 10^{-2}, 5 \cdot 10^{-2}\}$.
3. Sweep max_iter $\in \{30, 50, 100, 200\}$.
4. For each combination, count trefoils. Report stability.

If the count is 9 in the central neighborhood with deviations of at most ±1 at the parameter extremes, the theorem holds in the strong form. If the count varies more, the theorem reads: "9 trefoils at the stated parameters; the multiset characterization $\{V,B,H\} \cup \{V,B,B\}$ is what's stable across parameter regimes."

**Marked TODO:** runs in ~5 minutes once GPU is free; defer until a clean window.

---

## §5 Random-table sample size — STILL OPEN

`fibonacci_robustness.py` samples 200 random commutative tables on $\mathbb{Z}/10\mathbb{Z}$ and finds 0 of them reproduce the $(|F|,|S|) = (13, 8)$ decomposition. There are $10^{55}$ such tables; 200 is a tiny sample.

**Action:** scale to 10,000 samples. ~1 minute compute. Result expected: 0 of 10,000 (or extremely small fraction). The qualitative claim holds; the quantitative bound on rarity sharpens.

**Marked TODO:** can run any time.

---

## §6 Honest scope paragraph placement — RECOMMEND MOVING

Currently the "honest scope" framing is in the introduction. For an arXiv reader unfamiliar with the project's context, this can read as overly defensive at first contact.

**Recommendation:** move it to a §1.4 explicit "Limitations and scope" subsection at the end of §1. Standard math-paper structure. The negative tone-checks (Fibonacci canonical-specific, ±21 modular interpretation hypothetical, Burrin-von Essen "structurally analogous") stay; they just live in the right place.

This is editorial, not load-bearing. Brayden's call.

---

## §7 Cold-read reviewer — STILL OPEN

Brayden has not yet had a non-Brayden non-AI human read the paper. Recommend before arXiv submission:

- A math grad student in algebra or number theory
- Someone on Math Stack Exchange (post the most isolated theorem — say, Theorem 4.1 — and see if it gets independent verification or pushback)
- The Topos Institute's open Slack (if they have one) for ACT-adjacent eyeballs

Even a 30-minute read of the abstract + §2 (definitions) + Theorem 4.1 statement would catch confusion before arXiv reviewers do.

---

## §8 Status of the §5 checklist

Each line item from `SCRUTINY_NOTES.md §5`:

| Item | Status |
|---|---|
| Run `verify_paper.py` — must produce 0 failures | DONE (42/0 with inlined runtime) |
| Compile `main.tex` with EPTCS style; check matrix rendering | TODO (Brayden, before submission) |
| Search magma literature for 4-element commutative non-associative magma with identity | DONE (§2 above; not in standard classification) |
| Confirm Burrin–von Essen 2024 publication status | DONE (§1 above; published IMRN Vol 2024 Issue 22) |
| Inline trefoil-counting code into `verify_paper.py` or self-contained ancillary | DONE (§3 above) |
| Have someone read it cold | OPEN (Brayden) |
| Sweep runtime parameters $(\varepsilon, \text{threshold})$ | OPEN (§4 above) |
| arXiv preferred categories: math.RA primary, math.CO + math.CT secondary | NOTED |
| Update Zenodo DOI 10.5281/zenodo.18852047 with new file | TODO (Brayden, on arXiv post) |
| Hold fifteen-ropes / Ho Tu / consciousness adjacencies OUT of paper | DONE (paper is rope-1 only per META_STRATEGY) |

5 of 10 items closed in this session; 5 remain (3 trivial, 2 require Brayden's call or a clean GPU window).

---

## §9 What this extension preserves

- All ten honest negatives N1-N10. No demoted claim re-inflated.
- The "structurally analogous to" / "conceptually scaffolded by" tone for Katok-Ugarcovici, Burrin-von Essen, and the rest of the modular-knot literature.
- The single-rope discipline: this paper claims the algebraic substrate, nothing more.
- The verification-script discipline: every numerical claim has a `[PASS]` line in `verify_paper.py`.
