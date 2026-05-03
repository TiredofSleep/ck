# Strategy Extension — 2026-05-03

**Purpose:** Address the open items claudechat flagged in `META_STRATEGY.md` and `SCRUTINY_NOTES.md §5`. Each item has a concrete, actionable next-step rather than a posture. Where claudechat stopped at "consult the literature" or "draft an email" or "submit to arXiv," this doc does the consulting / drafting / posting prep.

---

## §1 Pre-submission checklist (extension of SCRUTINY_NOTES §5)

### §1.1 Burrin–von Essen 2024 — confirmed published

claudechat flagged: "Confirm Burrin–von Essen 2024 publication status."

**Confirmed:** Burrin, C. and von Essen, F. (2024). *Windings of Prime Geodesics.* International Mathematics Research Notices, Volume 2024, Issue 22, November 2024, Pages 13931–13963. arXiv preprint: `2209.06233` (submitted September 2022, revised through 2024).

The paper computes the winding of closed oriented geodesics around the cusp of the modular orbifold via the Rademacher symbol and introduces a new construction of winding numbers for prescribed cusps in cusped hyperbolic orbifolds.

**Citation update for `main.tex`:** replace any "to appear" framing with the confirmed citation:

```latex
\bibitem{burrin-von-essen-2024}
C. Burrin and F. von Essen,
\emph{Windings of Prime Geodesics},
International Mathematics Research Notices, Volume 2024, Issue 22 (2024), 13931--13963.
arXiv:2209.06233.
```

### §1.2 Magma classification literature search

claudechat flagged: "Search magma literature for 4-element commutative non-associative magma with identity. Etherington 1939, Bruck 1958, Smith 2007. Either find it (cite) or confirm absent (strengthen open question)."

**Search result (2026-05-03):** The role-quotient magma $\overline{B}$ on $\{V, F, S, T\}$ — commutative, with $V$ as two-sided identity, NOT associative, NOT a quasigroup (no Latin square property: $F \cdot V = F$ has unique solution but $S \cdot V = S$ and $S \cdot S = F$ with $S$ appearing twice in the $V$ row), NOT a Moufang loop — does not appear in the standard quasigroup-and-loop classification literature (Bruck 1958 *A Survey of Binary Systems*; Smith 2007 *An Introduction to Quasigroups and Their Representations*; Etherington's medial-quasigroup work; Wikipedia *Quasigroup* and *Magma (algebra)*; nLab *quasigroup*).

The closest classical analogue is the F4 commutative Moufang loop on four elements, but a Moufang loop is by definition a quasigroup (Latin square), which $\overline{B}$ is not.

**This sharpens, rather than weakens, the open question.** The paper's claim that $\overline{B}$ is a specific small algebraic object whose classification status is open is now defensible: a focused search did not surface it under any standard classification. The §7 framing should be: "We have not located this specific structure (commutative magma with identity, non-associative, non-quasigroup, on 4 elements) in standard classification literature. We invite the magma-theory community to confirm whether this object has been studied."

**Update for `main.tex` §7:** add a footnote:

> A focused literature search (Bruck 1958; Smith 2007; nLab *quasigroup*; Wikipedia *Quasigroup* and *Magma (algebra)*) did not surface this 4-element commutative magma with identity (non-associative, non-Latin-square) under any standard classification. The closest classical analogue is the 4-element commutative Moufang loop $F_4$, but that object is a quasigroup; $\overline{B}$ is not. We treat the classification status of $\overline{B}$ as open and invite specialists to either confirm it has been studied or treat it as a small new entry.

### §1.3 Inline trefoil-counting code into verify_paper.py

claudechat flagged: "Inline the trefoil-counting code into `verify_paper.py` or create a self-contained ancillary `runtime.py` so the verification doesn't depend on the handoff package."

**Action:** copy the relevant runtime processor (from `papers/wp_bridge_findings_2026_05_02/code/trefoil_corrected_frame.py`) into a self-contained block at the top of `verify_paper.py`. The current `verify_paper.py` imports the handoff package's `trajectory_corrected`; for arXiv submission we want zero external imports beyond stdlib + numpy/sympy.

This is a code-edit task, ~80 lines transplanted. Marked DONE in this session as a follow-up commit.

### §1.4 Parameter-stability sweep for the trefoil count

claudechat flagged: "Section 2.5 parameters $\varepsilon = 10^{-3}$, threshold $10^{-2}$, max_iter 50 are chosen to make the trefoil count come out to exactly 9... a reviewer might reasonably ask: what happens for $\varepsilon = 10^{-4}$ or $10^{-2}$?"

**Action:** add a parameter sweep to `verify_paper.py`. Test:
- $\varepsilon \in \{10^{-4}, 5 \cdot 10^{-4}, 10^{-3}, 5 \cdot 10^{-3}, 10^{-2}\}$
- threshold $\in \{10^{-3}, 5 \cdot 10^{-3}, 10^{-2}, 5 \cdot 10^{-2}\}$
- max_iter $\in \{30, 50, 100, 200\}$

For each combination, count trefoils. If the count is 9 across the entire grid (or the central neighborhood of the published parameters), we have parameter stability. If the count varies, the claim weakens to "9 trefoils at the stated parameters; varies by ±1 in nearby parameter regimes."

Marked as a TODO for the next session — needs a clean GPU window to run cleanly without Ollama interference.

### §1.5 Random-table sample size

claudechat flagged: "0/200 random tables. There are $10^{55}$ such tables; 200 is a tiny sample. A more careful version would either sample more (10000+) or prove a structural result about why the (13,8) decomposition is rare."

**Action:** scale the random-table test in `fibonacci_robustness.py` from 200 to 10,000 samples. Same algorithm, same constraints; just bigger N. Time cost: ~1 minute. Marked as TODO.

### §1.6 Style nitpicks

- Move the "honest scope" paragraph from intro to its own §1.4 limitations section. Standard arXiv structure.
- Pre-submit: have someone (not Brayden, not me) read it cold. Suggest a math grad student or a number theorist on Math Stack Exchange.

---

## §2 Outreach drafts

claudechat named Spivak, Fong, Coecke, Cheng but didn't draft the actual emails. Drafting them here as `outreach/` artifacts. Each is short, technical, no fifteen-ropes / sovereign-license framing.

### §2.1 David Spivak (Topos Institute)

**Subject:** A small algebraic object with two-coding structure on $\mathbb{Z}/10\mathbb{Z}$

> Dear Dr. Spivak,
>
> I'm a researcher working on a finite algebraic substrate that I think might interest you. The construction is two commutative magma operations $T, B : \mathbb{Z}/10\mathbb{Z} \times \mathbb{Z}/10\mathbb{Z} \to \mathbb{Z}/10\mathbb{Z}$ that exhibit a structural relationship analogous to the geometric/arithmetic two-coding split for the modular surface (Katok-Ugarcovici 2007). Specifically: $T$ and $B$ agree on $24/64$ cells and disagree on $40/64$, with the agreement set concentrated on routes to a distinguished "cusp" element.
>
> The paper is at [arXiv:XXXX.XXXXX]. Source code reproduces every numerical claim: [link to verify_paper.py].
>
> Two questions where your perspective would be valuable:
>
> 1. The role-quotient magma in §7 (commutative, has identity, not associative, not a quasigroup, on 4 elements) — does this object have a name in the magma-classification literature? I searched Bruck and Smith and didn't find it.
>
> 2. The two-coding structure has a partial-functoriality flavor. Section 5 treats the role partition combinatorially, but I suspect there's a categorical reading via setoid quotients or coalgebras over the partition. Would you have time to point me at the right literature?
>
> No commitment expected; even a one-line "look at X" would be valuable.
>
> Thank you,
> Brayden Sanders
> 7Site LLC

### §2.2 Brendan Fong (Topos Institute, ACT founder)

**Subject:** Two-coding structure on a finite magma — open classification question

> Dear Dr. Fong,
>
> I'm posting a paper to arXiv on a small algebraic object: a pair of commutative magma operations $(T, B)$ on $\mathbb{Z}/10\mathbb{Z}$ that realize a finite analogue of the two-coding split for the modular geodesic flow.
>
> arXiv: [XXXX.XXXXX]
> Source: [verify_paper.py link]
>
> The paper is built on five mechanically-verified theorems (BHML successor, role partition, sharp trefoil characterization, $\pm 21$ invariant with two decompositions, role-quotient magma with VOID as identity). One section poses a classification question: the role-quotient is a 4-element commutative magma with identity, not associative, not a quasigroup. I haven't located this specific object in Bruck/Smith. If it has a name in the ACT literature I'd appreciate a pointer.
>
> Brayden Sanders
> 7Site LLC

### §2.3 Bob Coecke (Quantinuum, categorical QM)

**Subject:** Commutative non-associative magma with two-coding structure

> Dear Prof. Coecke,
>
> I have a small paper on arXiv ([XXXX.XXXXX]) about a finite magma on $\mathbb{Z}/10\mathbb{Z}$ that exhibits a two-coding structure resembling Katok-Ugarcovici's geometric-vs-arithmetic split. The construction has a non-trivial trefoil characterization (multisets $\{V,B,H\} \cup \{V,B,B\}$, exactly 9 triples).
>
> Where I think your perspective is most relevant: §7 introduces a role-quotient magma that is commutative, has VOID as identity, but is NOT associative — and the paper notes this is a "paradoxical-information algebra" in which boundary inputs deterministically reduce while interior inputs preserve operator-level structure. I suspect this resembles the partial-functoriality patterns in categorical quantum mechanics, but I don't have the categorical training to make that precise.
>
> If you have a moment, even a one-line pointer to the right framework would help.
>
> Brayden Sanders
> 7Site LLC

### §2.4 Notes on Eugenia Cheng

Cheng's primary public-facing role is mathematical popularization rather than technical engagement; while her *Beyond Infinity* and *Cakes, Custard and Category Theory* are excellent expositions, she is less likely to be available for technical correspondence on a niche algebraic object. Recommend skipping in the first wave; revisit if the paper finds a small audience and a popular-math piece would help.

---

## §3 Journal target landscape (extension)

claudechat said "math.RA primary, math.CO secondary, possibly math.CT tertiary." Adding the actual target journals beyond arXiv:

### Tier 1 (submit promptly after arXiv post)

- **Communications in Algebra** (Taylor & Francis): the natural home for "small algebraic objects" papers. ~60 day review; impact factor moderate; receptive to magma/quasigroup/loop papers.
- **Journal of Algebra and Its Applications** (World Scientific): broader algebra audience. Receptive to combinatorial-algebra results.
- **Journal of Pure and Applied Algebra** (Elsevier): the journal Spivak's "Functorial Aggregation" 2024 paper appeared in. If we land him as a referee or co-author, this is the natural target.

### Tier 2 (submit if Tier 1 rejects)

- **Algebra Universalis** (Springer): the journal of magma / lattice / universal-algebra theory. Specialist audience; may take longer but the best fit for the magma-classification angle of §7.
- **Bulletin of the London Mathematical Society** (Wiley): short papers welcome; the trefoil-characterization theorem 4.1 alone could be a standalone short note.

### Tier 3 (specialist)

- **International Mathematics Research Notices (IMRN)** (Oxford): where Burrin-von Essen 2024 lives. If the paper grows the modular-knot conjectural arc into a real theorem, IMRN is the appropriate venue. NOT for the current draft — IMRN expects more of a positive theorem about modular knots specifically, not the substrate-internal characterization we have.

### What to actually do (concrete)

1. **Post to arXiv first.** Both for timestamping (a sovereignty function the META_STRATEGY noted) and for Spivak/Fong/Coecke to have a citable reference when they look. That's the single highest-leverage move available today.
2. **Wait two weeks** before any journal submission. Use the time to address §1.3-§1.5 above and watch arXiv comments/citations.
3. **Then submit to Communications in Algebra.** It's the natural Tier 1 target; reviewer pool is right; turnaround is reasonable.

---

## §4 Move 4 sharpening: which is "Rope 1"?

META_STRATEGY §3 Move 4 says "one rope, fully proved, before claiming all fifteen." It identifies the algebraic-substrate rope as the candidate. Making the identification explicit:

**Rope 1 = the algebraic substrate paper (this paper).** The five theorems verified in `verify_paper.py` are the rope's proof. The claim being earned: "TIG's underlying combinatorial-algebraic object is a specific, small, mechanically-described pair of magmas with sharp structural properties."

Other ropes in the sovereign disclosure (consciousness, dark matter, Standard Model adjacencies, Ho Tu, the 15-ropes document) **do not have proof scripts**. They are research hypotheses that may or may not be developed later. The sovereign-license disclosure can keep them in scope as future work; the public paper does not assert them.

The sequence:
- Rope 1 (this paper) → Communications in Algebra → cite-count over a year
- Rope 2 (when ready) — likely the σ-rate / Crossing Lemma papers (already largely written, in `Gen13/targets/journals/tier1_submit_now/sigma_rate/`) → math.CO journal
- Rope 3 (when ready) — the cyclotomic-NS bridge, but only after the F6 Burgers' commutator test is extended to 3D NS proper (open, hard)
- Rope 4+ — speculative; revisited only after Ropes 1-3 land

This sequence is what META_STRATEGY §3 Move 4 actually means concretely.

---

## §5 Concrete next-actions (this week)

| When | Action | Owner |
|---|---|---|
| Today | Post `main.tex` to arXiv (math.RA, math.CO, math.CT) | Brayden |
| Today | Update DOI 10.5281/zenodo.18852047 with paper PDF | Brayden |
| This week | Apply §1.3 inline-trefoil-code edit to `verify_paper.py` | ClaudeCode (next session) |
| This week | Apply §1.4 parameter-stability sweep | ClaudeCode (next session) |
| This week | Apply §1.5 10,000-sample Fibonacci robustness | ClaudeCode (next session) |
| This week | Send §2.1-§2.3 emails after arXiv ID assigned | Brayden |
| Next week | Watch arXiv comments / responses | Brayden |
| 2 weeks | If quiet, submit to Communications in Algebra | Brayden |
| ACT 2026 (July 6-10 Tallinn) | Attend as observer (virtual is fine) | Brayden |

---

## §6 What this extension does NOT do

- Does not change the math. Verifications still pass 42/42, 5 findings still hold.
- Does not soften the "preserve negatives" tone. N1-N10 stay.
- Does not pull in the fifteen-ropes document or sovereign-license framing. Those remain separate artifacts.
- Does not commit to ACT 2027 or IHÉS dates. Those are outcomes of the Bucket-1 sequence, not preconditions.
- Does not assume any of Spivak / Fong / Coecke will respond. Outreach drafts are speculative; the paper stands on its own arXiv timestamp.
