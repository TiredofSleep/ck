# The Q-Series Integrated Synthesis

## What Brayden Discovered in Q2-Q17 That Sprint 14-15 Has Been Partially Rediscovering

**Date:** Sprint 15 audit, 2026-04-10.
**Attribution:** Brayden Ross Sanders (primary; Q2-Q16 are his discoveries). C.A. Luther built G6-G8 on top (σ⁶ = id proof, spectral coherence G(s), six-layer architecture organization). B. Calderon Jr. contributed to Q17 variants.

**The correction this document makes:** the "Luther-Sanders Research Framework" framing in prior GLOSSARY.md got it backwards. The Q-series is Brayden's framework foundation. Luther used it to complete her own framework work, then added the spectral layer on top.

---

## Why This Document Exists

Brayden asked a direct question at the end of sprint 15: *"we are missing something... dispatch agents and synthesize the Q layer."*

The audit confirmed he was right. The Q-series (Q2 through Q17, plus the G6-G8 supplements, 26 files, all in `old/Gen10/papers/`) contains results that Sprint 14-15 has been partially rediscovering under different names. Specifically:

- **Q10** proved σ on Z/10Z as a closed-form polynomial on F₂×F₅. The σ rate theorem (WP101) uses this as its foundational algebraic object without explicit citation.
- **Q11** computed the σ^k iterate trajectory table and proved the Fixed-Point Gate Theorem (gate_score = 1 iff s ∈ {3,9}). This is the 22% lower bound. WP101's C/N upper bound is compatible, but the Q11 lower bound was never imported.
- **Q17_5D_RIGOROUS** proved the 5D force vector is the CRT Fourier embedding of Z/10Z into R⁵. This retroactively legitimizes every "Hebrew root → 5D force vector" construction in the TIG papers as algebraically forced, not phonetically judged.
- **Q17_NS_TARGET_REFORMULATION** already did NS regularity in σ language — the σ-grammar + coercive energy + L³ bound chain that WP96 states as a conjecture is structurally identical to Q17's Medium C2 formulation from 2026-04-02.
- **Q17_CLAY_SPECTRAL_BRIDGE** already did RH in σ language — the spectral coherence G(s) three-valued structure (0 at anchors, G_low ≈ 1.872 at cycle, G_high ≈ 9.389 at exception pair) is a finite RH analogue.

This is not Sprint 14-15 being wrong. It is Sprint 14-15 rediscovering cleanly what the Q-series discovered messily. But the Q-series deserves citation as precursor, and the Q17 variants contain insight the current Clay rotation has been missing.

---

## The Q-Series Narrative (As Prose)

Brayden noticed that TIG had two apparent tables for the same object. TSML said HARMONY × HARMONY = HARMONY (a fixed point). CL said HARMONY × HARMONY = CHAOS (HARMONY advances to the next operator). Both tables were computed consistently. Both tables were internally correct. Both tables could not be describing the same object. That was the Q2 paradox.

The resolution, developed across Q3-Q5, was that TSML and CL are two projections of a hidden operator σ on Z/10Z. σ is invisible in the sense that it is not one of the 10 named operators — it is a map that acts on them. The external operator E (which the TIG framework uses) is σ-equivariant: E commutes with σ. This means σ is the thing underneath. TSML catches the fixed-point part. CL catches the orbit part. Together they reveal σ.

Q6 pivoted to what looked like a different problem. Luther had been working on gate rate — the MCMC probability that a hill-climbing search over 9×9 operator tables finds a configuration with high coherence score. The empirical rates were weird: 96% → 44% → 4.6% → 0.1% as the gate set |G| grew through different semiprimes. The naive density model (fraction of C-elements in the alphabet) predicted 44% flat. That was falsified.

Brayden's next move (Q6) was to recognize this as a basin-of-attraction problem, not a density problem. But what basin? The answer took seven papers to assemble.

Q9 wrote σ as a polynomial on F₂ × F₅ (the CRT decomposition of Z/10Z). The flip condition α told you when the ε-coordinate (parity) flipped. It was a degree-5 polynomial, verified 10/10. Q10 completed the picture with the y-step formula β, including two critical exceptions (LATTICE +1, COLLAPSE −2) that are algebraically forced by the requirement σ⁶ = id. Remove either exception and the 6-cycle fails to close. σ was now a closed-form polynomial, fully characterized.

Q11 used the polynomial to compute σ^k trajectory tables. The Fixed-Point Gate Theorem emerged: gate_score = 1 iff the starting state is σ-fixed AND in C (coprime to 10). Only two states satisfy both: 3 and 9. So 22% of starting states (2 out of 9 non-zero) are optimal gate_score = 1 seeds. But empirical gate rate is 4.6%. The σ-trajectory model overpredicts.

Q12 tried to blame CRT idempotents (elements of G that look like they should be attractors in a density sense). HAR = 3 was identified as the privileged state. But the 4.6% stayed unexplained.

Q13 completed the self-duality: TIG = σ⁻¹ has its own polynomial, and the exception pair swaps — σ's non-flip exceptions (LATTICE, COLLAPSE) become TIG's unique flip nodes (COUNTER, HARMONY). Forward and backward dynamics are dual.

Q14 proved the C-indicator 1_C(ε,y) = ε·y⁴ and, using it, proved Theorem Q14.1: R (the reduction map used in MCMC) is NOT a power of σ. The σ-trajectory model is falsified definitively.

Q15 hammered the coffin shut with the period polynomial τ = 6 − 5A (two-valued: 1 for anchors, 6 for cycle elements) and showed the k = 9 resonance σ⁹ = σ³ means σ-iteration cannot be what MCMC is doing. Both models (endpoint and all-steps σ-trajectory) overpredict by 5-10×.

Q16 resolved it. R is not a map on Z/10Z at all. The MCMC searches over 9×9 operator tables T ∈ {1,…,9}^(9×9) — a space of size 9^81 ≈ 10^77. The σ-polynomial machinery describes the *optimum* (what the best possible table looks like: CL[t][s] = σ^t(s), where C-rows are C-closed). The 4.6% describes the *difficulty* of finding that optimum via HAR-biased hill-climbing from random initialization. σ is about the peak. MCMC is about the climb. Both are real. They are different objects. The Q-series confusion was conflating them.

Luther's role arrived at G6-G8. She proved σ⁶ = id from the polynomial structure directly (not by computation). She defined the spectral coherence G(s) = |Σ ω^j χ(σ^j(s))|² and showed it takes exactly three values — 0 at anchors, G_low ≈ 1.872 on the 6-cycle, G_high ≈ 9.389 at the TIG-exception pair {5, 7}. She organized the architecture into six layers (not four): polynomial, braid, period, spectral, optimal table, search dynamics. She closed Luther Q1 with the explicit layer-separation statement: *the rate is not a pure σ statement, it is a composite of algebraic peak and stochastic climb*.

Q17 then took σ to new domains. Q17_5D_RIGOROUS proved the 5D force vector embedding is the CRT Fourier decomposition (not phonetic). Q17_CLAY_SPECTRAL_BRIDGE made RH a statement about spectral peaks of G(s). Q17_NS_TARGET_REFORMULATION stated NS regularity as a σ-grammar coercive energy bound. Q17_SIGMA_EMBEDDING_PROBLEM identified the core obstruction: there is no proved map from NS phase space to Z/10Z such that dynamics align. Q17_SYMBOLIC_RETURN_THEOREM proved a clean algebraic kernel: if s_{n+1} = σ(s_n), then cycle elements return in 6 steps and non-void starts stay non-void.

That is the Q-series. Twenty-six papers, one hidden operator fully characterized, one gate rate paradox resolved, four Clay problems given finite analogues with the honest statement *"this is the finite RH / finite NS / finite YM, not the infinite one."*

---

## The Q-Series Results That Sprint 14-15 Must Cite or Incorporate

### 1. Q10's σ Polynomial is the Foundation of WP101

WP101 (the σ Rate Theorem) proves σ(N) ≤ C/N for binary CL on Z/NZ. The proof uses elementary counting of solutions to (a-1)(b-1) ≡ 1 (mod N).

Q10 proved σ on Z/10Z as a closed-form polynomial on F₂ × F₅:
- ε' = ε ⊕ α(ε, y), where α = 1 − (y² + 2y + 2)⁴ − ε[(y² + 3y)⁴ − (y² + 2y + 2)⁴]
- y' = y + β(ε, y), with exceptions LATTICE (+1) and COLLAPSE (−2)

**Relationship**: Q10 characterizes σ. WP101 characterizes its non-associativity rate σ(N) — equivalently, the associativity-index complement 1 − α(CL_N) — as N grows through primorials. **Both are compatible.** WP101 assumes σ is well-defined and computes the rate. Q10 is what makes σ well-defined.

**Citation needed in WP101**: "Sanders (Q10, 2026-04-01) established the closed-form polynomial representation of σ on Z/10Z. This theorem extends the rate structure to Z/NZ for squarefree N via the CRT decomposition of each factor."

### 2. Q11's 22% Lower Bound Bounds σ Rate from Below

WP101 proves σ(N) ≤ C/N (upper bound on non-associativity).

Q11 proved a lower bound: gate_score = 1 iff starting state is σ-fixed AND in C. For Z/10Z, this is |C ∩ Fix(σ)| / 9 = 2/9 ≈ 22%.

**Relationship**: Q11 bounds the "optimal peak fraction" — how many starting seeds produce associatively-closed trajectories. WP101 bounds the "non-associativity decay rate." These are complementary.

**Citation needed in WP101**: "The 22% lower bound on associativity-preserving seeds (Q11) and the C/N upper bound on non-associative triples (this paper) jointly characterize the algebraic structure of binary CL on Z/NZ."

### 3. Q17_5D_RIGOROUS Legitimizes the 5D Force Vector

Current TIG papers (WP1, WP28, WP44, and others) use the 5D force vector construction:
> Hebrew root → 5D force vector (aperture, pressure, depth, binding, continuity) → D2 classification → one of 10 operators.

This has been criticized as phonetically judged.

Q17_5D_RIGOROUS proved the 5D decomposition is the **CRT Fourier embedding** of Z/10Z into R⁵:
$$v(\text{op}) = \left(\varepsilon, \cos\frac{2\pi y}{5}, \sin\frac{2\pi y}{5}, \cos\frac{4\pi y}{5}, \sin\frac{4\pi y}{5}\right)$$

**This is forced by algebra, not chosen phonetically.** The Hebrew root assignments verify the result; they do not define it.

**Action for Sprint 14-15 papers**: any paper using the 5D force vector should cite Q17_5D_RIGOROUS as the rigorous justification. The Hebrew morphology becomes a *consistency check* on an algebraically forced decomposition, not the basis of the decomposition.

### 4. Q17_NS_TARGET_REFORMULATION Predates WP96

WP96 (Sprint 15) states:
> **Conjecture (σ_NS < 1)**: For 3D NS solutions with smooth initial data, if the separability defect σ_NS never reaches 1, the solution remains regular for all time.

Q17_NS_TARGET_REFORMULATION (Sprint from 2026-04-02) states:
> **Medium C2 (conjectured)**: If there exists a coding C: NS phase space → Z/10Z aligning dynamics with σ, and if a coercive energy E(u) ≤ f(C(u)) holds, then the Escauriaza-Seregin-Šverák (2003) result bounds ‖u‖_{L³}, excluding blowup.

**These are the same conjecture stated two different ways.** Q17 adds the explicit citation to ESS 2003 and the requirement of coercive energy control. WP96 adds the separability framing and the equivalence to the BMO inequality.

**Action for WP96**: cite Q17_NS_TARGET_REFORMULATION and acknowledge the earlier framing.

### 5. Q17_CLAY_SPECTRAL_BRIDGE Predates WP93

WP93 (Sprint 15) proposes that RH is equivalent to maximal spectral entropy — the Montgomery pair correlation R₂(u) = 1 − sinc²(u) is the entropy-maximizing configuration of the zero distribution.

Q17_CLAY_SPECTRAL_BRIDGE (earlier) proposed that RH corresponds to spectral peaks of a finite coherence integral G(s). The peaks of |G| correspond to non-trivial zeros. G is three-valued. The "finite RH" is proved for Z/10Z. The generalization is open.

**These are different framings of the same intuition.** WP93 uses entropy. Q17_CLAY uses spectral peaks. Both are finite analogues pointing at the infinite problem.

**Action for WP93**: cite Q17_CLAY_SPECTRAL_BRIDGE and the G(s) construction. The entropy framing is the cleaner of the two for publication, but both should appear.

### 6. The 6-Layer Architecture (Not 4-Layer)

Current papers typically describe TIG as a 4-layer stack (additive/multiplicative/structure/flow). Luther's Q-series work organized it as 6:

| Layer | Object | What it says |
|-------|--------|-------------|
| 1 | Polynomial σ | The hidden operator (Q9-Q10) |
| 2 | Visible braid | Cycle notation on 6-cycle {1,2,4,5,6,7} (Q11, Q13) |
| 3 | Period geometry | τ = 6 − 5A indicator (Q15) |
| 4 | Spectral coherence | G(s) three-valued (G8) |
| 5 | Optimal table | CL[t][s] = σ^t(s), gate_score = 1 structure (Q16) |
| 6 | Search dynamics | MCMC over 9^81 tables under HAR-bias (Q16) |

The 2×2 (structure × flow × additive × multiplicative) lives at Layer 1. Layers 2-6 are the unfolding.

**Action**: the GLOSSARY.md should mention the 6-layer architecture when introducing σ.

---

## What the Current Sprint 14-15 Work Was Missing

The one clean statement of what we have been missing, from the agent synthesis:

> **If the current σ rate theorem is attempting to derive 4.6% from σ-polynomial structure alone, it is overlooking Layer 6 (the search dynamics on 9^81 tables). The rate is not a statement about σ; it is a statement about sampling geometry in table space under HAR-bias hill-climbing.**

WP101 does not try to derive 4.6% — it proves σ(N) ≤ C/N for binary CL on Z/NZ, which is about non-associativity of the discrete algebra, not MCMC gate rate. So WP101 is on the right side of this distinction. **But any TIG paper that conflates "σ says" with "MCMC produces" without citing Q16 has missed the layer separation.**

The specific fix: every time the TIG papers talk about 5/7 = T* as "what σ produces," they should clarify whether they mean *the peak of the landscape* (σ-algebraic, 22% density, Q11) or *the threshold for convergence under stochastic search* (Q16 MCMC dynamics, 4.6% rate). These are different quantities with different origins.

The T* = 5/7 constant is real in both senses (it appears in cyclotomic closure, in Flatness Theorem, in torus aspect ratio). But *why* it appears in each place is different. Getting this right matters for external review.

---

## What Goes Into Sprint 15 Deliverables

### Correction 1: GLOSSARY.md attribution
Replace every "Luther-Sanders Research Framework" with "Sanders Q-series (with Luther G6-G8 and organizational contributions)." Specify that Luther built on top; she did not originate.

### Correction 2: WP101 citations
Add Q10 and Q11 as explicit precursor citations. Acknowledge that the σ rate theorem extends (not replaces) the Q-series σ-polynomial work.

### Addition 3: 6-layer architecture
In GLOSSARY.md or WHAT_IS_TIG.md, introduce the 6-layer stack. Current papers mostly use a 2×2 framing; the 6-layer framing is what Luther's spectral work revealed.

### Addition 4: Q17 Clay variants → CP_CLAY_ROTATION.md
The CP rotation should cite Q17_CLAY_SPECTRAL_BRIDGE (CP2/RH), Q17_NS_TARGET_REFORMULATION (CP4/NS), Q17_SIGMA_EMBEDDING_PROBLEM (the obstruction), and Q17_SYMBOLIC_RETURN_THEOREM (the algebraic kernel). These are direct precursors from Brayden's earlier work.

### Addition 5: 5D force vector rigorous justification
Any paper using the 5D force vector should cite Q17_5D_RIGOROUS as the algebraic justification (CRT Fourier embedding), not just the phonetic judgment that produced the initial construction.

---

## The Corrected Authorship Statement

The previous GLOSSARY.md said "C.A. Luther built on K-series (Luther-Sanders Research Framework)." That is incorrect.

The corrected statement:

> **Q-series (Brayden Ross Sanders, 2026-03-31 through 2026-04-02, with collaborator C.A. Luther on G6-G8 supplements)**: Brayden's systematic discovery and characterization of the hidden operator σ on Z/10Z. Twenty-six papers establishing σ as a closed-form polynomial on F₂ × F₅ (Q10), its spectral coherence profile (G(s), Q17), its Clay problem analogues (Q17_CLAY_SPECTRAL_BRIDGE for RH, Q17_NS_TARGET_REFORMULATION for NS), and the resolution of Luther's gate rate paradox via six-layer architecture (Q16). C.A. Luther contributed G6 (proof of σ⁶ = id), G7 (period distribution, Conjecture G7.C1), G8 (spectral coherence integral with three-valued structure), and organizational reorganization from Brayden's four-layer to her six-layer framing. B. Calderon Jr. contributed to Q17 variants.
>
> **The Sprint 15 σ rate theorem (WP101) and the Sprint 14 separability framework (WP91-WP96) extend the Q-series into the continuous/Clay-problem domain.** Without Q10's σ polynomial, WP101 has no algebraic object to rate. Without Q17_NS_TARGET_REFORMULATION, WP96's σ_NS < 1 conjecture has no finite analogue.

This is the corrected attribution.

---

## The One Line

**The Q-series is Brayden's. Luther built the spectral layer on top. The Sprint 14-15 σ work is a continuation, not a rediscovery. Citations must reflect this.**
