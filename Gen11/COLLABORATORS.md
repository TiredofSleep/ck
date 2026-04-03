# COLLABORATORS.md
## Seeking Critical Review and Bridge Construction
*CK Gen11 Clay Mathematics Program*
*Author: Brayden Ross Sanders / 7Site LLC — 2026-04-03*
*DOI: 10.5281/zenodo.18852047 | GitHub: github.com/TiredofSleep/ck*

---

## Direct Statement

This work has not been reviewed by professional mathematicians. We are actively seeking that review.

The algebraic structure documented here — the forced threshold T* = 5/7 in Z/10Z, the K*(n) cascade computed from 5000 Riemann zeros, the ternary partition {0, 1/2, 5/7}, the Sandwich Theorem, the Recycling Rule — is internally consistent and independently verifiable from the source data (`riemann_zeros_5000.json`). What it is not is a solution to any Clay problem, and the framework is explicit about why: every bridge from the algebraic (Z/10Z arithmetic) to the analytic or geometric domain of each problem remains unconstructed.

We are looking for mathematicians who would engage with these specific open bridges. The invitation is genuine. Critical review, counterexample search, and falsification of the structural arguments are as valuable as confirmation. We would rather know quickly where the framework is wrong than slowly paper over gaps.

---

## What the Framework Has

Before describing what is needed, here is what the framework actually contains — stated precisely, without overselling.

**Proved algebraically:**
- T* = 5/7 is the unique ratio constructible from the complement-equivariant fixed point (5) and the generator-inverse (7) of (Z/10Z)*. Proof is one line.
- The Sandwich Theorem: (5/6)² < 5/7 < (6/7)² — both sides reduce to 1 > 0. This establishes n = 6 as the unique foundation boundary index.
- The K*(n) cascade computed exactly from 5000 mpmath zeros: K*(6) = 99, K*(7) = 14, K*(8) = 6, K*(9) = 4, K*(10) = 3, K*(11) = K*(12) = 2, K*(n ≥ 13) = 1. Every shadow value has an exact algebraic expression: K*(6)−1 = 2·7² = 98, K*(7)−1 = 2·7−1 = 13.
- All zeros inside the bridge zone [1/2, 5/7) at n = 7 are in opposing phase (cos(7·θ_k) > 0), computed and verified to K = 5000.
- K*(6) = 7×14 + 1 = 99: the "+1" is a carried remainder from the sub-threshold level, algebraically identified.
- Three structured gap layers before the bandwidth floor — the count of three is algebraically forced, not empirically selected.

**Structural arguments (not proofs):**
- Sha (Tate-Shafarevich group) identified as the carried remainder in BSD by analogy with the Recycling Rule.
- B_local < T*·E₀ as the NS regularity criterion, supported by Kolmogorov scaling but not proved from NS constants.
- K*(7) = 14 vs. K*(6) = 99 as a structural analogue of the P vs. NP gap — the gap is real in Z/10Z, the correspondence to circuit complexity is not proved.
- CRT decomposition of Z/10Z as structurally analogous to the Hodge decomposition — no algebraic geometry constructed.

---

## RH Bridge

**What the framework establishes:** T* = 5/7 as the algebraic threshold in Z/10Z. The K*(n) cascade from 5000 zeros. The three-layer gap structure. The K-S statistic D_KS/T* ≈ 10% — the zero distribution is well inside the generator regime. The opposing-phase structure inside the bridge zone, computed to K = 5000. The Sandwich Theorem establishing n = 6 as the unique boundary index.

**What is missing:** A correspondence between T* = 5/7 (the algebraic fixed point of Z/10Z) and Re(s) = 1/2 (the analytic midpoint of the critical strip). These are not the same number. The framework does not construct this correspondence. Without it, the algebraic structure cannot reach the Riemann Hypothesis.

**Candidate bridge:** The sinc²/Fejér kernel identification (called F1 in the formal record). The Fejér kernel F_K(θ) = (1/K)·|Σ_{n=0}^{K-1} e^{inθ}|² is the natural smoothing kernel for the Li sum, and the zero-free region of ζ(s) near Re(s) = 1/2 has a sinc² structure. The conjecture is that T* = 5/7 and Re(s) = 1/2 are the same threshold under this kernel identification. This has not been proved. It has not been falsified either — no computation to K = 5000 contradicts it.

**Needed:** A number theorist familiar with Li coefficients, the explicit formula for ζ(s), and the Fejér/sinc² kernel theory. The bridge question is: can the algebraic forced threshold T* = 5/7 be identified with Re(s) = 1/2 via a specific, constructible kernel correspondence, without assuming GRH? If yes, the identification would give the Li criterion a new algebraic underpinning. If no, the framework's structural argument collapses cleanly.

**What collaboration means here:** Either a proof sketch that the F1 identification is constructible, or a demonstration that it is not (a counterexample or a no-go theorem for this class of correspondences). A conversation about whether this candidate bridge is even the right approach would be valuable.

---

## BSD Bridge

**What the framework establishes:** Sha (the Tate-Shafarevich group) is identified structurally with the "+1" in K*(6) = 7×14 + 1 = 99. Both are global remainder terms that no local accumulation (Euler product / Li sum) generates independently. The identification is precise in character: the Recycling Rule says that the level-n data equals the exact-hold at level n plus the carried remainder from level n−1. In BSD terms: the BSD formula contains Sha as the carried remainder from the local-global gap. BSD is proved for ranks 0 and 1 (Kolyvagin) — exactly the cases where the remainder is zero (Sha = 0 or finite, rank forcing it to zero).

**What is missing:** A TIG object (a specific algebraic structure within the framework, not yet constructed) that carries the Sha remainder for rank ≥ 2. The framework provides the shape of what is needed: it must be a global object that accumulates from local Euler factors in the same way the Li sum accumulates from individual zeros, and it must have a finite/infinite bridge width question analogous to K*(n).

**Two falsified bridges:** B_new-1 (rank staircase approach) and B_new-2 (CM-2 twist approach) were tested against published BSD data and falsified. They predicted specific numerical values that were wrong. This is documented in `FORMAL_BSD.md`. The falsifications were clean and the positions are parked — no active candidate bridge exists for BSD as of 2026-04-03.

**Needed:** An arithmetic geometer familiar with Sha, Euler products, and the structure of Selmer groups. The specific question is whether any object in the arithmetic geometry of elliptic curves has the algebraic structure of the Recycling Rule's carried remainder — meaning: something that accumulates from local data, is zero precisely when BSD holds for rank 0 and 1, and whose finiteness for rank ≥ 2 is the open question. Alternatively: a demonstration that no such object can exist, which would definitively close the BSD bridge from this direction.

**What collaboration means here:** This bridge is parked and we know why — two specific approaches failed. What is needed is either a new candidate bridge construction from someone with deeper BSD expertise, or confirmation that the structural analogy (Sha = carried remainder) is unproductive and why.

---

## NS Bridge

**What the framework establishes:** T*·E₀ as the energy threshold separating the smooth (generator) regime from the potential blowup (complexity) regime. The Cascade Rule (energy flows from large to small scales, not the reverse) as the structural argument against blowup. Kolmogorov scaling gives B₁/E₀ ≈ 0.315 < T* = 0.714, placing smooth flow well inside the generator regime. The bridge conjecture (F2): prove B_local < T*·E₀ a priori from NS constants alone.

**What is missing:** An a priori functional analytic estimate. The framework provides the threshold and the structural argument (blowup would require inverting the one-way energy cascade). It does not provide the bound. The estimate needed is of the form: for smooth initial data in appropriate Sobolev spaces, there exists a constant C (derivable from NS viscosity and domain geometry) such that B_local ≤ C·E₀ with C < T* = 5/7. The framework estimates C ≤ 3.74 from dimensional analysis, but this is not an a priori proof.

**Needed:** A PDE analyst familiar with energy methods, Ladyzhenskaya-type estimates, and enstrophy bounds. The specific question is whether the NS equations, with standard smooth initial data assumptions, admit an a priori estimate bounding B_local relative to total energy E₀ by a constant strictly less than 5/7. If such an estimate exists and can be derived from NS constants alone (without assuming smoothness of the solution, which would be circular), it would constitute the NS bridge. If no such estimate can exist, that negative result is also valuable — it would clarify why the NS blowup question is genuinely open.

**What collaboration means here:** The framework provides the threshold and the intuition. A PDE analyst with experience in Navier-Stokes global regularity questions could quickly determine whether the F2 bridge conjecture is the right form of the estimate, and whether it is stronger or weaker than known partial results.

---

## P vs. NP Bridge

**What the framework establishes:** K*(7) = 14 (polynomial-cost threshold crossing — 14 zeros suffice for the generator level n = 7) vs. K*(6) = 99 (super-polynomial-cost threshold crossing — 99 zeros needed for the complexity level n = 6). The gap between 14 and 99 is real in Z/10Z. The shadow at K = 98 = 2·7² is the last sub-threshold state before the complexity threshold is crossed. The gap is algebraically forced and not adjustable.

**What is missing:** Any connection between this algebraic gap and circuit complexity. The framework does not have a circuit model. It does not have a complexity class definition. The gap in Z/10Z is structural; whether it corresponds to the P/NP separation is a question the framework cannot answer internally.

**Why this bridge is weak:** Of all five Clay bridges, P vs. NP has the least active path from this framework. The structural analogy (K*(7) = polynomial, K*(6) = super-polynomial) is intuitively appealing but has no formal content. The framework is honest about this: the P vs. NP position is marked PARKED in the formal record. It is included because the ternary partition forces it into the structure — not because the framework has anything genuinely useful to offer the complexity community.

**Needed:** A complexity theorist to do one of two things: either find a formalization of the K*(7)/K*(6) gap in terms of circuit lower bounds or oracle separation results, or confirm clearly that the structural analogy has no formal content and the bridge should be closed. Either answer is progress.

**What collaboration means here:** Mostly a sanity check. The complexity community would know immediately whether the K*(7) = 14 / K*(6) = 99 gap has any formal relationship to known complexity class separations. A brief conversation with someone in circuit complexity would resolve this quickly.

---

## Hodge Bridge

**What the framework establishes:** A CRT decomposition of Z/10Z that is structurally analogous to the Hodge decomposition (generator cycles ↔ algebraic classes, bridge zone ↔ transcendental classes, sub-threshold ↔ non-Hodge). The BSD → Hodge chain (documented in `FORMAL_HODGE.md`) argues that the Recycling Rule applied to motives gives the Hodge conjecture for algebraic cycles as a special case of the BSD remainder termination. Markman's 2025 result (abelian fourfolds) is cited as the current boundary of what is proved; the frontier is dim ≥ 5.

**What is missing:** Everything algebraic-geometric. No Hodge classes have been constructed from this framework. No cycle map has been defined. No motive has been specified. The analogy is structural only — the framework does not engage with the actual mathematics of the Hodge conjecture.

**Why this bridge is the weakest:** The Hodge position is the most honest example of the framework's limitation. The structural argument is real (the ternary partition does map cleanly onto the Hodge decomposition at the formal level). But there is no mathematical content bridging the two. The framework is a spectator here.

**Needed:** An algebraic geometer familiar with Hodge theory and motives, particularly post-Markman 2025. The specific question is whether the Bloch-Kato conjecture (applied to all motives) gives a formalization of the Recycling Rule's remainder structure — i.e., whether "Sha-finiteness for motives" is a meaningful statement that would generalize the BSD→Hodge chain into a proof-level argument. If it is not meaningful in this form, the Hodge bridge should be closed and the framework's position revised accordingly.

**What collaboration means here:** The framework needs an algebraic geometer to read `FORMAL_HODGE.md` and give an honest assessment of whether the BSD→Hodge chain has any formal content worth pursuing, or whether it is a structural metaphor with no mathematical traction.

---

## Summary: What Kind of Collaboration Is Sought

| Clay Problem | Bridge Status | Discipline Needed | Type of Engagement |
|---|---|---|---|
| **Riemann** | Active (F1 candidate) | Analytic number theory, Li coefficients, explicit formula | Bridge construction or falsification |
| **BSD** | Parked (two bridges falsified) | Arithmetic geometry, Sha, Selmer groups | New candidate construction or direction-closing |
| **Navier-Stokes** | Active (F2 candidate) | PDE analysis, energy methods, Ladyzhenskaya | A priori estimate construction or no-go |
| **P vs. NP** | Parked (structural only) | Circuit complexity | Quick sanity check: formal or dismiss |
| **Hodge** | Spectator (no active path) | Algebraic geometry, Hodge theory, motives | Assessment of BSD→Hodge chain |

"Collaboration" means any of the following, depending on what you find useful:

- **Critical review**: read the formal record, identify errors in the algebraic arguments, inconsistencies in the structural analogies, or places where the framework overclaims.
- **Counterexample search**: find a K*(n) value that contradicts the cascade, a Li coefficient behavior that contradicts the Sandwich Theorem, or a BSD example that falsifies the Sha = carried remainder identification.
- **Bridge construction**: engage with one of the active candidates (F1 for RH, F2 for NS) and either advance it toward a proof sketch or demonstrate it is the wrong form.
- **Direction-closing**: confirm that a parked bridge (BSD, P vs. NP, Hodge) is unproductive and explain precisely why. This is as valuable as positive progress.
- **Conversation**: if any part of this framework touches an area you work in and you have a reaction — agreement, disagreement, or "this reminds me of X" — that conversation is worth having.

---

## How to Engage

**GitHub issues**: github.com/TiredofSleep/ck
Open an issue with any question, objection, or comment. All positions are documented and no argument is hidden. The formal record (`CLAY_FORMAL_RECORD.md`) contains every computation and every position taken, including the falsified bridges and the parked positions.

**DOI**: 10.5281/zenodo.18852047
The archived version of the Gen9 and Gen11 Clay documentation is citable here.

**Expectations**: We are not asking for peer review of a paper. We are asking for expert eyes on specific open questions. Any level of engagement — from "your K*(n) computation has an error at n=8" to "I have a proof sketch for F1" — is welcome. The framework is honest about its limits. Engagement that sharpens those limits is the goal.

---

*(c) 2026 Brayden Ross Sanders / 7Site LLC*
*7Site Public Sovereignty License v1.0 — Human use only. Free forever.*
*DOI: 10.5281/zenodo.18852047*
