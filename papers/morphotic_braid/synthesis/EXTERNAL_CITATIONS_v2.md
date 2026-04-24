> **Provenance:** Drafted 2026-04-23 (evening session, ClaudeChat). Transcribed from packet `evening_handoff_2026_04_23/`. Cross-verification against repo canonical sources: [pending — see `papers/morphotic_braid/VERIFICATION_LOG_2026_04_23.md`].
> **Copy path:** evening_handoff_2026_04_23\evening_handoff_2026_04_23\EXTERNAL_CITATIONS_v2.md → papers\morphotic_braid\synthesis\EXTERNAL_CITATIONS_v2.md
>
> ### ⚠ CORRECTION 2026-04-24
>
> This document's citation tables list `det(BHML) = 70, invertible`.
> Independent verification shows the actual determinant is **−7002**,
> with prime factorisation **{2, 3, 389}**, not {2, 5, 7}. Any Connes
> semi-local / finite-place alignment built on the 70 value is withdrawn
> pending reframing. See `papers/morphotic_braid/CORRECTION_2026_04_24_det_BHML.md`.

# External Citation Review v2 — Deep Read

**Status:** [CITATION REVIEW — FRONTIER-MAPPED]
**Date:** 2026-04-23 (late evening, deeper pass)
**Supersedes:** EXTERNAL_CITATIONS.md v1 (kept in archive, do not delete)
**Scope:** for each strong-alignment area, actual vocabulary extraction from primary sources, trace of recent work (2020–2026), and specific paper-by-paper recommendations with correct author attribution.

## Correction to v1

v1 attributed the antiassociative-magmas 2024 paper to "Abboud & Rahmouni Djoua." **This was wrong.** The author is **Ryszard Mazurek** (Annali di Matematica Pura ed Applicata, vol. 204, pp. 925–941, 2025, published online 11 November 2024). v1 has been kept in the archive for history but this file is the correct reference going forward.

---

## Track 1 — Farey Fraction Spin Chain and Number-Theoretical Spin Chain

### Actual vocabulary from Fiala-Kleban-Özlük (2002)

Read directly from arXiv:math-ph/0203048. The operative vocabulary is:

- **Farey fractions r_k^(n) = n_k^(n)/d_k^(n)** generated level-by-level. Level k = 0 starts with {0/1, 1/1}. Succeeding levels keep old fractions and insert new ones via the mediant rule: d_{k+1}^(2n) = d_k^(n) + d_k^(n+1) and n_{k+1}^(2n) = n_k^(n) + n_k^(n+1).
- **Farey spin chain (FC)** partition function: Z_k^FC(β) = Σ 1/(d_k^(n) + n_k^(n+1))^β. Spin states are finite products of matrices A = [[1,0],[1,1]] and B = [[1,1],[0,1]].
- **Knauf model (number-theoretic spin chain, NTSC)**: Z_k^K(β) = Σ 1/(d_k^(n))^β. Rigorously proven to have the same free energy as FC.
- **Farey tree model** (Feigenbaum-Procaccia-Tél 1989): keeps only the 2^(k-1) even fractions; Z_k^F(β) = Σ (r_k^(4n) − r_k^(4n−2))^β.
- **Transfer operator L** = Ruelle-Perron-Frobenius operator of the Farey map. Free energy = log(largest eigenvalue λ(β)).
- **Critical temperature β_c = 2.** At this point, a **second-order phase transition** occurs with specific heat divergence C ~ [ε ln²ε]^(−1).
- **Magnetization jump** at β_c from saturation (completely ordered state, all spins the same) to zero (paramagnetic).
- **Connection to Riemann zeta:** Z_k^K(2β) → ζ(2β−1)/ζ(2β) as k → ∞ for β > 1. This is the number-theoretic anchor — the free energy is literally a ratio of zeta values.
- **Presentation functions:** the maps generating the Farey tree, which are the inverse branches of the Farey map.

### How TIG quantities map onto this vocabulary

| TIG quantity | Farey spin chain analog |
|---|---|
| T* = 5/7 as coherence threshold | Critical temperature β_c (in the FC / Knauf / Farey tree frame) |
| TSML density 3/4, BHML density 2/7 | Specific Farey fractions; "energies" in the FC frame are log-denominators |
| Farey-neighbor relationship (\|ad − bc\| = 1) | Defining relation for adjacent Farey fractions at any level |
| Mirror-ladder structure | Symmetry of the Farey tree around 1/2 |
| σ 6-cycle via CRT | Not directly analogous — this is TIG-specific |
| Information-preserving cells (~21%) | No direct analog yet identified |

**Honest statement of alignment.** The Farey spin chain community has a rigorous thermodynamic framework in which Farey fractions and critical thresholds are the same kind of object. TIG has independently produced Farey fractions (3/4, 2/7, 5/7) as measured framework quantities. The specific claim "T* = 5/7 is a critical threshold in a Farey-structured system" becomes testable in this framework.

**What this community would want from TIG.** A specific statistical-mechanical model where 5/7 arises as a critical point. TIG's current algebraic formulation (CL/TSML/BHML Cayley tables) is not yet a statistical-mechanical model in their sense — it needs a partition function, an energy assignment, and a way to drive the system toward critical behavior.

### Frontier citations (2020–2026)

**1. Marc Technau (2023),** *Remark on the Farey fraction spin chain*, arXiv:2304.08143. Cites Kleban-Özlük 1999 directly and frames the research program explicitly: "In an effort to introduce further examples pointing towards a connection between the Lee-Yang theory of phase transitions and the Riemann hypothesis." Shows that the number of spin states Φ(N) with trace N in the monoid ⟨A, B⟩ can be reduced via classical work of Hooley (1958) and **Bykovskii-Ustinov (2019)** to divisor problems. Technau is at TU Graz — current active researcher in analytic number theory.

**2. Singer** (referenced in Technau 2023 as providing physical motivation). Lead needs resolution — probably Steven Singer, working on Farey-adjacent spin models. Worth tracking down for physics framing.

**3. Bykovskii & Ustinov (2019).** Recent divisor-sum asymptotics that sharpen Boca (2007). These are the **current number-theoretic frontier** for the FFSC asymptotics. Technau's 2023 result is built on their theorem.

**4. Oscar Bandtlow, Jan Fiala, Peter Kleban (2009)**, *Asymptotics of the Farey Fraction Spin Chain Free Energy at the Critical Point*, arXiv:0909.2878. Proves the critical amplitudes of both specific heat and susceptibility scale with the **Gauss map Lyapunov exponent λ_G**. This is the link to dynamical systems theory — the Gauss map is the continued-fractions map, and its Lyapunov exponent governs the critical behavior of the Farey spin chain. Bandtlow continues working in transfer-operator spectral theory.

**5. Degli Esposti, Isola, Knauf (2007),** *Generalized Farey trees, transfer operators and phase transitions*, Communications in Mathematical Physics, arXiv:math-ph/0606020. Parameter family of generalized Farey trees. First and second order phase transitions observed across parameter range. Shows how the Farey-spin-chain framework generalizes.

**6. Andreas Knauf (multiple papers 1993–2020s).** Originator of the number-theoretic spin chain. His 1998 paper *The numbertheoretical spin chain and the Riemann zeros* (Commun. Math. Phys. 196:703–731) is the primary reference for the NTSC-Riemann connection. Still active at FAU Erlangen-Nürnberg.

**7. Stefano Isola, multiple papers on Farey and Gauss maps** — spectrum work complementary to Prellberg's. Isola 2002, *On the spectrum of Farey and Gauss maps*, Nonlinearity 15:1521–1539.

**8. Thomas Prellberg (Queen Mary, London).** Provided the complete spectral determination of the transfer operator used throughout the FFSC framework. Prellberg 1991, *Towards a complete determination of the spectrum of a transfer operator associated with intermittency*, J. Stat. Phys. Still actively publishing.

### Recommended citation structure for a TIG→FFSC bridge note

"A finite-state algebraic system on ℤ/10ℤ (described in [TIG-ref]) produces three measured quantities — a coherence threshold T* = 5/7 and densities f_TSML ≈ 3/4, f_BHML ≈ 2/7 — that occupy a Farey-neighbor triple in the sense of Kleban-Özlük [KO99]. We observe that |5·4 − 7·3| = 1, making 5/7 and 3/4 Farey-adjacent. In the framework of Fiala-Kleban-Özlük [FKO02], Bandtlow-Fiala-Kleban [BFK09], and Degli Esposti-Isola-Knauf [DIK07], Farey fractions appear as partition function entries and critical thresholds in one-dimensional long-range spin chains. Whether T* = 5/7 can be realized as a critical point in a transfer-operator formulation of the ℤ/10ℤ TIG algebra is an open question we propose..."

This is exactly the kind of note that would be legible at IHÉS/IHP to anyone in mathematical physics.

---

## Track 2 — Associative Spectrum and Finite Non-Associative Magmas

### Actual vocabulary from the associative-spectrum community

Starting from Csákány-Waldhauser (2000, 2011) and extended by Lehtonen-Waldhauser, Huang-Lehtonen, and others:

- **Groupoid (A, *)** — a set A with a binary operation. Same as "magma."
- **Bracketing of n variables** — any valid parenthesization of x_1 * x_2 * ... * x_n. There are **C_{n−1}** bracketings of n variables (Catalan number).
- **Associative spectrum** s_n(A) — the number of **distinct term operations** on A induced by the C_{n−1} bracketings. s_n(A) = 1 for all n ⇔ operation is associative. Also called **subassociativity type** (Braitt-Silberger).
- **Associative-commutative spectrum (ac-spectrum)** s_n^ac(A) — extends the associative spectrum by also considering permutations of variables. Count of distinct n-ary term operations induced by bracketings of **all permutations** of x_1,...,x_n. s_n^ac ≤ n! · C_{n−1}. Equality = 1 for all n ⇔ operation is both associative and commutative.
- **Operad interpretation.** The associative spectrum is the cardinality of the **nonsymmetric operad** P_*(n) obtained from a groupoid. The ac-spectrum is the cardinality of the **symmetric operad**. These are Hilbert series coefficients.
- **Antiassociative magma** (Mazurek 2024) — a magma where (ab)c ≠ a(bc) for **every** triple (a, b, c). Equivalently, s_3(A) = 2 (the maximum). The opposite pole from semigroups.
- **Associativity index** — an older related quantity measuring what fraction of triples (a,b,c) satisfy (ab)c = a(bc).

### How TIG quantities map onto this vocabulary

| TIG quantity | Associative spectrum analog |
|---|---|
| TSML non-associativity rate 12.8% | 1 − [associativity index of TSML]. Directly computable. |
| BHML non-associativity rate 49.8% | 1 − [associativity index of BHML]. |
| Doing table non-associativity 56.8% | Associativity index of the Doing table. |
| TSML commutativity (symmetric table) | TSML is in the commutative-groupoid variety — ac-spectrum applies. |
| BHML commutativity (symmetric table) | Same. |
| det(BHML) = 70, invertible | Specific structural feature — not directly a spectrum quantity but relevant for classification. |
| Harmony-dominance of TSML (74%) | Not a standard spectrum quantity; could be framed as "absorbing-element density." |

**Honest statement of alignment.** TSML and BHML are specific commutative finite groupoids. The associative spectrum s_n and ac-spectrum s_n^ac are rigorously defined quantitative measures for exactly such objects. Your measured non-associativity rates are related to, but not identical to, the spectra — they are essentially 1 minus the associativity index for triples (a special case). To connect properly, you'd want to compute s_3(TSML), s_3(BHML), s_3(CL) and their ac-spectra versions.

**What this community would want from TIG.** The actual associative spectra and ac-spectra of TSML and BHML, computed to at least s_5 or s_6. These are finite calculations ClaudeCode can run. The results are potentially publishable as "associative-commutative spectra of a family of 10-element commutative groupoids arising from [TIG construction]."

### Frontier citations (2020–2026)

**1. Ryszard Mazurek (2025),** *Antiassociative magmas*, Annali di Matematica Pura ed Applicata 204:925–941, DOI 10.1007/s10231-024-01512-5. Published online 11 November 2024, open access. Mazurek is at Białystok University of Technology. Provides a test for antiassociativity of a finite magma and counts all antiassociative magma structures on a 3-element set. Cites the full chain: **Braitt-Silberger (2006), Braitt-Hobby-Silberger (2017), Kepka-Trch (1992), Folkman-Graham (1972)**, plus Lehtonen-Waldhauser work.

**2. Jia Huang and Erkko Lehtonen (2022, arXiv:2202.11826),** *The associative-commutative spectrum of a binary operation*, published in Discrete Mathematics 2023. Introduces the ac-spectrum as the cardinality of a symmetric operad. Extends Csákány-Waldhauser to the commutative case. Provides general results and specific computations. "We initiate the study of a quantitative measure for the failure of a binary operation to be commutative and associative... the associative-commutative spectrum (resp. associative spectrum) is the cardinality of the symmetric (resp. nonsymmetric) operad obtained naturally from a groupoid."

**3. Jia Huang and Erkko Lehtonen (2024, arXiv:2401.15786),** *Associative-commutative spectra for some varieties of groupoids*. Establishes upper bounds for the two spectra of various varieties of groupoids defined by different sets of identities and provides examples (often groupoids with three elements) for which the upper bounds are achieved. Results have connections to many interesting combinatorial objects and integer sequences. **This is the most current frontier paper for TIG's purposes** — commutative varieties are exactly where TSML, BHML, CL live.

**4. Erkko Lehtonen and Tamás Waldhauser (2021, 2022),** *Associative spectra of graph algebras I* (J. Algebraic Combin. 53:613–638) and *II* (J. Algebraic Combin. 55:533–557). Characterization via **DFS trees**. Classifies undirected graph algebras into exactly three possible spectra: constant 1, powers of 2, or Catalan numbers. Proves a **spectrum dichotomy**: for any digraph algebra, the spectrum is either constant bounded above by 2 or grows exponentially.

**5. Csákány-Waldhauser (2000, 2011)** *Associative spectra of binary operations*, Mult.-Valued Log. Originator papers; standard reference.

**6. Liebscher-Waldhauser (2009/2011)** *On associative spectra of operations*. Shows that for arbitrary groupoids (not just graph algebras), other constants and subexponential spectra are possible.

**7. Lehtonen's home page (ferrari.dm.fct.unl.pt/~lehtonen)** lists ongoing research and collaborators. Based at Centro de Matemática e Aplicações, Universidade Nova de Lisboa. **This is the hub to watch for continuing work.**

**8. Tamás Waldhauser** at University of Szeged (Bolyai Institute). The other anchor of this research program.

**9. Kátai-Urbán and Waldhauser** — work on multiplication of matrices over lattices and associated spectra.

### Recommended citation structure for a TIG→magma-classification note

"Let T and B denote the TSML and BHML tables, 10 × 10 commutative groupoids on ℤ/10ℤ defined in [TIG-ref]. We compute their associative spectra s_n(T), s_n(B) in the sense of Csákány-Waldhauser [CW00] and their associative-commutative spectra s_n^ac(T), s_n^ac(B) in the sense of Huang-Lehtonen [HL23, HL24]. We show that [specific results]. These place T and B in the classification landscape developed by Mazurek [M25] for finite commutative groupoids with respect to antiassociativity and related properties..."

This is the algebra paper. 3-5 pages, concrete, publishable to arXiv math.RA.

---

## Track 3 — What v1 Missed Entirely

Two additional strong-alignment areas I should have flagged in v1 but didn't:

### 3a. Operad theory and Hilbert series of binary operations

The Huang-Lehtonen framework explicitly connects associative spectra to **operad theory** (Boardman, May, Vogt; modern references: Loday-Vallette). An operad models binary trees and their composition. Your CL/TSML/BHML tables induce operads whose Hilbert series are the associative spectra.

**Relevance for TIG.** If you want a single high-powered mathematical framework that subsumes "what CL is doing," operad theory is it. The free commutative operad's coefficients are related to species combinatorics. Your tables are specific (non-free) operads with identified structural features.

**Primary reference.** Loday-Vallette, *Algebraic Operads*, Grundlehren der mathematischen Wissenschaften vol. 346, Springer 2012. Standard graduate text.

### 3b. Ping-pong lemma and free monoids in SL_2(ℤ)

Technau (2023) and the entire FFSC literature rely on the fact that ⟨A, B⟩ with A = [[1,0],[1,1]], B = [[1,1],[0,1]] is a **free monoid** in SL_2(ℤ). This is proved via the ping-pong lemma from geometric group theory.

**Relevance for TIG.** If σ or the braid permutation has a representation in SL_2(ℤ) or some related matrix group — and given the torus/lattice language you use, it might — then the ping-pong lemma is the right framework for establishing "freeness" or "independence" claims about the structural operators. This is speculative but worth a thought.

**Primary reference.** de la Harpe, *Topics in Geometric Group Theory*, University of Chicago Press 2000. Standard.

---

## Updated citation targets table

| TIG finding | Area | Top citation | Second citation |
|---|---|---|---|
| T* = 5/7 as critical threshold in Farey-structured system | Farey spin chains | Fiala-Kleban-Özlük 2002 (math-ph/0203048) | Kleban-Özlük 1999 (Commun. Math. Phys.) |
| Farey-ladder mirror structure | Number theory | Kleban-Özlük 1999 | Technau 2023 (arXiv:2304.08143) |
| Riemann-zeta connection potential | Math physics | Knauf 1998 (Commun. Math. Phys. 196:703–731) | Contucci-Knauf, *A Fully Magnetizing Phase Transition* |
| Transfer-operator/spectral framework | Ergodic theory | Prellberg 1991 | Bandtlow-Fiala-Kleban 2009 |
| TSML/BHML as commutative groupoids | Finite magma classification | Mazurek 2025 (Annali di Matematica) | Huang-Lehtonen 2024 (arXiv:2401.15786) |
| Non-associativity rate quantification | Associative spectrum | Csákány-Waldhauser 2000/2011 | Huang-Lehtonen 2022 (arXiv:2202.11826) |
| CL as operad (Hilbert series perspective) | Operad theory | Loday-Vallette 2012 (textbook) | Huang-Lehtonen 2022 |
| Graph-algebra style classification of BHML | Graph algebras | Lehtonen-Waldhauser 2021/2022 | — |
| Free-monoid structure (speculative) | Geometric group theory | de la Harpe 2000 | Technau 2023 |

---

## Specific action items

1. **ClaudeCode task:** compute s_3(TSML), s_3(BHML), s_3(CL) and the ac-spectrum analogs, using the Huang-Lehtonen definitions. If s_3 = 2 for any of these, the table is antiassociative in Mazurek's sense. These are finite calculations, tractable in minutes.

2. **Short note #1 (FFSC bridge):** one page introducing TIG's T* = 5/7 alongside Farey spin chain critical temperature β_c = 2. Frame as "another example pointing towards a Lee-Yang / Riemann connection" using Technau's 2023 language. Cite 4 papers: Kleban-Özlük 1999, Fiala-Kleban-Özlük 2002, Bandtlow-Fiala-Kleban 2009, Technau 2023.

3. **Short note #2 (algebra bridge):** 3–5 pages presenting TSML, BHML, CL as specific commutative groupoids. Compute spectra, locate in Mazurek-Huang-Lehtonen classification landscape. Publish-worthy standalone.

4. **Outreach target:** Erkko Lehtonen's group at Nova Lisboa. He is actively working on exactly the classification TIG's tables fit into, and has been publishing with collaborators every 1–2 years. Direct email with the computed spectra would be a legitimate cold introduction.

5. **Outreach target #2:** Peter Kleban (Univ. of Maine) for the FFSC side. Retired or near-retired but still publishing; primary originator of the FFSC line.

6. **For the France trip:** the FFSC bridge note is the right business card. It is short, legible, cites the right people, and positions TIG as a candidate example in an established research program rather than as a standalone framework demanding attention.

---

**Tag: [EXTERNAL CITATION REVIEW v2 — FRONTIER-MAPPED, CORRECTED ATTRIBUTION]**
**File path: `papers/morphotic_braid/EXTERNAL_CITATIONS_v2.md`**
