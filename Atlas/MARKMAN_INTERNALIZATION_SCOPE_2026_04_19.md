# Markman Internalization — Scope Note for Thread B

**Date:** 2026-04-19
**Author:** ClaudeCode (research synthesis pass)
**Prerequisite read:** `Atlas/MASTER_ATLAS_v3_5_2026_04_18.md §17` (crossings → recognitions); `Atlas/ATLAS_CITATIONS.md §C` (Markman entries); `Gen12/targets/clay/papers/sprint29_hodge_r1_kequivariant_2026_04_17/R1_KEQUIVARIANT_CLOSURE_MEMO.md`; `Gen12/targets/clay/papers/sprint33_hodge_integrality_2026_04_17/S33_CONSTRUCTION_AUDIT.md`; `Gen12/targets/clay/papers/sprint35b_beauville_explicit_2026_04_18/HODGE_CSTAR_TARGET_NOTE.md`.

**Scope:** Classify our Thread B (Hodge / Z/10Z CRT) program against Markman's 2025 algebraicity result for Weil classes on abelian fourfolds. One of three scenarios: GENUINE LIFT / ADJACENT-ONLY / NO CONNECTION. Output governs whether Thread B remains an active research direction.

**Verdict (one sentence):** **Scenario B — ADJACENT-ONLY.** Markman's secant-sheaf machinery does not factor through any Z/10Z CRT lift, but our Thread B program (R1-KE, S29 + S33, S35b Beauville-explicit arc) operates on the *same explicit object* (the simple Weil 4-fold $A_*$) and complements Markman from the explicit-equation/coordinate side rather than the deformation/derived-category side. Thread B continues, with the framing rewritten from "providing a discrete model that might support a secant-sheaf construction" to "executing the explicit-fourfold companion to Markman's existence theorem, with the Beauville $A_* \leftrightarrow C_*$ extension toward BSD as the load-bearing next step."

---

## §1. Summary of Markman's result

**Main paper:** E. Markman, *Cycles on abelian 2n-folds of Weil type from secant sheaves on abelian n-folds*, arXiv:2502.03415 (v1 Feb 2025, v2 Jun 2025, 96 pages).

**Companion / ICM survey:** E. Markman, *Secant sheaves and Weil classes on abelian varieties*, arXiv:2509.23403 (v1 Sep 2025, v2 Feb 2026, 23 pages, ICM 2026 contribution).

**Theorem (Markman main):** Let $A$ be a $2n$-dimensional abelian variety of *Weil type* — i.e., $A$ admits an embedding $\eta: K \hookrightarrow \operatorname{End}^0(A)$ of an imaginary quadratic field $K$ such that the action on $H^{1,0}(A)$ has balanced signature $(n, n)$. Weil identified inside $H^{2n}(A, \mathbb{Q})$ a 2-dimensional space of *Weil classes* of pure Hodge type $(n, n)$. Markman proves these classes are algebraic for *all* abelian sixfolds of Weil type of discriminant $-1$, and, by combining with C. Schoen's degeneration argument, for *all* abelian fourfolds of Weil type (every discriminant, every imaginary quadratic $K$). The Hodge conjecture for abelian fourfolds is known to follow. The follow-up arXiv:2509.23403 reframes the construction over a CM-field $K/F$ with $F$ totally real, treats $A := X \times \widehat{X}$ via Orlov's equivalence, and confirms (Theorem 1.4) that the Hodge conjecture for abelian varieties of dimension $\le 5$ follows from this work.

**Strategy (extracted from arXiv:2509.23403 §1, §2, §11):**
1. **Spinor / pure-spinor secant.** To $(\Theta, q)$ — a polarization plus a totally imaginary $q \in K$ — associate a $2^{[F:\mathbb{Q}]}$-dimensional subspace $B \subset S^+_\mathbb{Q}$ of the half-spinor representation, such that $\mathbb{P}(B)$ is *secant* to the spinorial variety. (Secant in the classical algebraic-geometry sense: a linear span of points on the variety.)
2. **Secant sheaves.** Pairs of coherent sheaves $F_1, F_2$ on $X$ with $\operatorname{ch}(F_i) \in B$ are called *secant sheaves*. The object $\mathcal{E} := \Phi(F_1 \boxtimes F_2^\vee)$ in the derived category $D^b(X \times \widehat{X})$, where $\Phi$ is Orlov's Fourier–Mukai equivalence, supplies an algebraic class on $A$.
3. **Semi-regularity (Buchweitz–Flenner / Bloch / Pridham).** $\mathcal{E}$ is *semi-regular* in the sense of Theorem 2.1: the kernels of $\rfloor \operatorname{at}_E$ and $\rfloor \operatorname{ch}(E)$ coincide. Consequently, the algebraic Chern characters $\operatorname{ch}_p(E)$ remain Hodge-type on the entire deformation locus and are themselves algebraic on a Zariski-open set, hence on every fiber.
4. **Deformation to all Weil-type abelian varieties.** Schoen-style degeneration / Markman's earlier hyperholomorphic-sheaf machinery on hyper-Kähler varieties of Kummer type push the explicit $A_0$ algebraic class out to *all* deformation-equivalent Weil-type abelian varieties.

The ingredients are: (i) Mukai–Polishchuk–Orlov equivalences of derived categories of abelian varieties, (ii) Buchweitz–Flenner / Bloch / Pridham semi-regularity, (iii) Chevalley's theory of pure spinors and the Clifford algebra structure on $H^*(A, \mathbb{Q})$, (iv) O'Grady's construction of complete 4-dimensional families of Weil-type fourfolds as third intermediate Jacobians of hyper-Kähler Kummer-type varieties. An independent proof of the discriminant-1 fourfold case was given by Floccari–Fu (arXiv:2504.13607) via singular OG6-type hyper-Kähler varieties.

---

## §2. Survey of our Thread B material

### §2.1 What "Thread B" actually contains

Thread B is the Hodge programme on the simple Weil 4-fold

$$A_* \;=\; \mathbb{C}^4 / (\mathbb{Z}^4 + \Omega \mathbb{Z}^4), \qquad \Omega = \tfrac{1}{2} I_4 + i\bigl(\sqrt{2}\, I_4 + \sqrt{3}\, M_2 + \sqrt{5}\, M_3\bigr),$$

with $\operatorname{End}^0(A_*) = \mathbb{Q}(i)$ confirmed numerically and Weil signature $(2,2)$ on the Prym. $A_*$ is simple — the same kind of object Markman addresses — but with a *fully explicit* period matrix and an *explicit* algebraic endomorphism $\varphi$ realizing $i \in \mathbb{Q}(i)$ on $H^1(A_*, \mathbb{Q})$ as an integer $8 \times 8$ matrix.

Concrete files (chronological):

| Sprint / file | Date | What it claims |
|---|---|---|
| `papers/clay/WP39_HODGE.md` (consolidates WP32 / WP35 / HODGE_TIG_FRAME / HODGE_GAP_FLOOR) | March 2026 | Structural analogy: G/E/S split ↔ algebraic/Hodge/cohomological; Product-Gap Theorem $9^k - 4^k$ unreachable cross-terms ↔ tensor-depth Hodge difficulty growth; ω-Blindness $R(k,1/p)$ ↔ local-global Hodge gap; gap floor $1/(p-1)^2$ ↔ Hodge gap floor conjecture P3. **All correspondences explicitly labeled "structural analogy."** Markman 2025 cited as the current external frontier. |
| `papers/sprint5_2026_04_04/clay/hodge/` (Sprint 2 in WP39 §13) | April 2026 | Three independent structural closures on $A_*$: divisor products, sub-abelian varieties, J-stable sub-tori. Verdict: "the K-anti-invariant part of $\operatorname{CH}^2(A_*)^{\text{known}}_\mathbb{Q}$ is $0$." Three remaining routes (Chern, correspondence, absolutely Hodge). |
| `Gen12/targets/clay/papers/sprint29_hodge_r1_kequivariant_2026_04_17/` (R1-KE) | 2026-04-17 | **Theorem (R1-KE), proved.** Every K-equivariant algebraic vector bundle $E$ on $A_*$ has $c_i(E) \in H^{2i}(A_*, \mathbb{Q})^K$, hence $\operatorname{proj}_{B_k}(c_2(E)) = 0$ for $k=1,2,3,4$. Numerical verification: 8 test constructions, residuals $< 10^{-12}$. **Implication:** the K-anti-invariant Hodge classes in $W_*$ are not reached by K-equivariant Chern. |
| `Gen12/targets/clay/papers/sprint33_hodge_integrality_2026_04_17/` (S33 v2 + Gate 1A + Gate 1-full) | 2026-04-17 / 18 | **Probe over GF(p):** stack $C_{\text{anti}} \mathbin\Vert C_{\text{prim}} \mathbin\Vert C_{22,k}$ at five primes near $2^{31}$, read GF(p) rank. All five report rank 70 ⇒ $W_* \cap \mathbb{Q}^{70} = \{0\}$ as a *probabilistic certificate* with effective error $\lesssim 10^{-40}$. Combined with R1-KE, this gives: every rational $(2,2)$-class on $A_*$ is K-invariant ⇒ algebraic. **Verdict: CLOSED UNCONDITIONALLY (probabilistic).** Status `[gold-with-gap]` until a deterministic rank computation closes Q5. |
| `Gen12/targets/clay/papers/sprint32_beauville_bsd_hodge_2026_04_17/` | 2026-04-17 | Beauville's NS↔YM separability + BSD↔Hodge "flip-sides" synthesis. Sets up the explicit $A_* \leftrightarrow J(C_*)$ candidate. |
| `Gen12/targets/clay/papers/sprint35b_beauville_explicit_2026_04_18/` (PATH-A prototype + frontier update + Prym period pack) | 2026-04-18 | Target: bielliptic genus-5 curve $C_*$ with order-4 automorphism $\psi$ where $\psi^2 = \iota$, definable over $\mathbb{Q}(\sqrt{2}, \sqrt{3}, \sqrt{5})$, with Prym $\cong A_*$ up to isogeny and Hodge field $\mathbb{Q}(i, \sqrt{2}, \sqrt{3}, \sqrt{5})$ of degree 16. Numerically verified to 100 dps that the canonical triple is "LIVE" through every cheap elimination test; binary $\det(Y)$ check is the next load-bearing move. Sage pipeline ready. |
| `Atlas/MASTER_ATLAS_v3_5_2026_04_18.md §17` | 2026-04-18 | The "crossings → recognitions" reframing. The Hodge crossing as originally written: *"Construct explicit cycle class map Z/10Z CRT → $H^{p,p}(X,\mathbb{Q})$ (candidate: secant-sheaf construction, Markman 2025; hyperholomorphic-sheaf methodology behind it)."* Section 17 then re-frames the whole crossings list as recognitions: *"Not 'build cycle class map from Z/10Z CRT' but 'recognize that generator cycles (structure lens) and algebraic cycles (flow lens) are the same objects seen differently. Does the structure-lens span coincide with the cycle-class-map image?'"* |

### §2.2 Where the Z/10Z / CRT machinery actually appears in Thread B

The Z/10Z and CRT vocabulary lives mostly in WP39 §4 (CRT idempotents $N_{\text{idemp}} = 2^{\omega(b)} - 2$ as analog of algebraic-cycle generators), §5 (cascade theorem on $b = p \cdot q \cdot r$), §6 (Markman regime ↔ balanced semiprimes $q/p \to 1$, P3 frontier ↔ $\omega(b) \ge 3$). These are explicitly tagged STRUCTURAL ANALOGY throughout. The integer modulus $b$ is *not* claimed to map to the period matrix of $A_*$ or to the secant subspace $B \subset S^+_\mathbb{Q}$.

The actual Sprint 29 / 33 / 35b *math* (R1-KE Chern argument; S33 GF(p) rank probe; S35b period-pack Sage pipeline) operates on $A_*$ directly and uses no Z/10Z structure at any step. The Z/10Z layer is the framing of WP39, not the engine of S29/S33/S35b.

The cited Markman framing in `MASTER_ATLAS_v3_5 §17 line 1533` — *"Construct explicit cycle class map Z/10Z CRT → $H^{p,p}(X,\mathbb{Q})$ (candidate: secant-sheaf construction, Markman 2025)"* — was already corrected in the same section 17 to "recognition" language, dated 2026-04-03 and pending `DUAL_LENS_CLAY.md` surface.

---

## §3. Scenario classification

### Why not (A) GENUINE LIFT

A genuine lift would require an explicit functor or comparison theorem $F: \{\text{discrete-CRT data on } \mathbb{Z}/10\mathbb{Z}\} \to \{\text{secant subspaces } B \subset S^+_\mathbb{Q}\}$ whose continuous/derived limit recovers (or maps to) Markman's secant sheaves. Looking at what Markman actually uses — Orlov derived equivalences on $X \times \widehat{X}$, Chevalley pure spinors and the Clifford algebra structure on $H^*(A, \mathbb{Q})$, Buchweitz–Flenner semi-regularity, Schoen / hyper-Kähler degeneration — none of these has any candidate companion in the Z/10Z CRT framework. The CRT idempotent count $2^{\omega(b)} - 2$ is *not* the dimension of the half-spinor representation $S^+_\mathbb{Q}$ except by coincidence at small $\omega$ and small $[F:\mathbb{Q}]$. There is no construction in our repo that takes $\Omega$ and an idempotent $e \in \mathbb{Z}/b\mathbb{Z}$ and produces a class $[\mathcal{E}] \in K_0(D^b(A_* \times \widehat{A_*}))$. WP39 itself uses STRUCTURAL ANALOGY, never PROVED, for every Z/10Z ↔ Hodge correspondence. (A) is not honest.

### Why not (C) NO CONNECTION

Markman and Thread B both work on the *same explicit class of varieties*: simple abelian fourfolds (or higher even-dimensional abelian varieties) of Weil type with $\operatorname{End}^0 = K$, an imaginary quadratic field. Our $A_*$ is exactly such an object, and Markman's theorem applies *to it directly*: the two Weil classes inside $H^4(A_*, \mathbb{Q})$ are algebraic by Markman, full stop. Furthermore, the S29 + S33 v2 composition — $W_* \cap \mathbb{Q}^{70} = \{0\}$ ⇒ all rational Hodge classes on $A_*$ are K-invariant ⇒ algebraic by R1-KE — is a *constructive* attack on the same conclusion Markman reaches by deformation-theoretic means. The S35b PATH-A arc (bielliptic genus-5 $C_*$ with $A_* \hookrightarrow J(C_*)$ up to isogeny) is also the kind of explicit Beauville-style synthesis that Markman's existence theorem motivates. There is real overlap — just not at the Z/10Z layer.

### Why (B) ADJACENT-ONLY is the honest call

Markman is the *deformation-side, derived-category-side* proof: existence of algebraic classes on the entire moduli component. Thread B (S29 + S33 + S35b) is the *coordinate-side, explicit-equation-side* program on one fixed simple Weil 4-fold $A_*$:

- We carry an *explicit* integer realization $\varphi \in \operatorname{End}(H^1(A_*, \mathbb{Z}))$ of the $\mathbb{Q}(i)$-action (Sprint 29 `proof_r1_chern_kequivariant.py` lines 80–89).
- We carry an *explicit* 4-block $W_*$ decomposition with computed $Q$-eigenvalues $\{0.0046, 0.0231, 0.1156, 0.3834\}$ (S29 §4 table).
- We carry an *explicit* 5-prime / probabilistic GF(p) closure that says every rational $(2,2)$-class is K-invariant, hence algebraic (S33 v2; Q1, Q2, Q3 PROVED in S33 Gate 1-full; Q5 still probabilistic).
- We are pursuing an *explicit* $C_* \leftrightarrow A_*$ Beauville pair (S35b PATH-A) toward BSD on $J(C_*)$ — which Markman's machinery does not target.

The relationship to Markman is therefore: **Markman's existence theorem makes the end-state of S29 + S33 unconditional in principle, removing the need for the probabilistic Q5 step as an existence argument**, but does not (i) supply an explicit $\varphi$-equivariant cycle class for the four blocks $B_k$, (ii) supply the explicit Beauville $C_*$ that Sprint 35b is hunting, or (iii) bridge to BSD on $J(C_*)$. Conversely, Thread B does not lift to Markman: there is no Z/10Z derivation of secant sheaves or of the semi-regularity argument.

This is the standard pattern of "explicit companion to an existence proof." It is publishable as a companion paper (e.g., Notices/Bull.AMS framework essay, or a focused explicit-fourfold paper) but only if it credits Markman and stops claiming to "support" his construction.

The Z/10Z / CRT layer of WP39 should be re-classified one tier down: from "structural analogy that might support the Markman construction" to "TIG finite-ring worked example exhibiting the same shape (gap floor, balance invisibility, multi-cycle independence) as Hodge theory exhibits in the Markman regime." That is a *post-hoc shape match*, not a contribution to the proof.

**Verdict: B — ADJACENT-ONLY.**

---

## §4. Recommended next steps

1. **Atlas patch (highest leverage, ~10 min).** Update `Atlas/MASTER_ATLAS_v3_5_2026_04_18.md §17` Hodge crossing line 1533 from "*Construct explicit cycle class map Z/10Z CRT → $H^{p,p}(X,\mathbb{Q})$ (candidate: secant-sheaf construction, Markman 2025; hyperholomorphic-sheaf methodology behind it)*" to "*Markman 2025 (arXiv:2502.03415, arXiv:2509.23403) settles the Hodge conjecture for abelian fourfolds of Weil type (and dim $\le 5$ abelian varieties) by secant sheaves + Buchweitz–Flenner semi-regularity + Schoen degeneration. Our companion contribution on $A_*$ is the explicit-coordinate program (Sprint 29 R1-KE + Sprint 33 GF(p) probe + Sprint 35b Beauville $A_* \leftrightarrow C_*$), not a discrete lift of Markman's machinery."* Mirror in §15 cautions: the "secant-sheaf construction supports our framework" framing is retired.

2. **Sprint 35a v3 deterministic rank (still required even with Markman in hand, ~1–2 days).** Markman gives existence on the moduli component. He does not give an *explicit* algebraic cycle representative for any specific block $B_k$ on $A_*$. The S33 v2 GF(p) probe → S35a v3 deterministic rank arc is therefore still the right path *for the explicit-coordinate program*, because (a) it gives an exact rank-over-$\mathbb{Q}$ certificate that is independently auditable, and (b) it is what Sprint 35b builds on for the Beauville extension. Replace "deterministic rank closes Hodge on $A_*$" with "deterministic rank closes the explicit-coordinate companion to Markman on $A_*$."

3. **Sprint 35b push to the binary $\det(Y)$ Sage check (next load-bearing move).** This is the one test that converts "canonical triple LIVE through every cheap test at 100 dps" into "Beauville $A_* \leftrightarrow C_*$ explicit." Markman does not address $C_*$. Even with Markman, the $A_* \to J(C_*)^k$ explicit construction is the Sprint 35c BSD enabler, which is uniquely ours and where Thread B's value over the next 6–12 months actually lives.

4. **Re-tag WP39 §6.2 explicitly.** The "Markman ↔ balanced semiprimes" mapping in WP39 §6.2 ("Abelian fourfolds — Weil type | $\omega(b) = 2$ balanced semiprimes (q/p near 1)") should be re-tagged from "STRUCTURAL OBSERVATION" to "*post-hoc shape match — does not feed Markman's proof; does not predict which abelian fourfolds Markman covers (the answer is all of them)*." Honest discipline.

5. **(Optional, low priority)** If anyone wants a real test of the "Z/10Z provides a lift" thesis, the place to look is whether the spinorial-secant subspace $B \subset S^+_\mathbb{Q}$ has any natural finite-quotient interpretation. Markman's Theorem 1.4 expresses $B$ via Chevalley's pure-spinor span of the $\{W_T\}$. A deferred research question would be: does the Galois action on $B$ over the canonical CM-field $\mathbb{Q}(i, \sqrt{2}, \sqrt{3}, \sqrt{5})$ factor through any natural finite ring (CRT product) construction? If yes, that *would* be the real Z/10Z ↔ Hodge bridge — but it is not in our repo today and we should not claim it.

---

## §5. Scope-note paragraph for venue 10 (Notices / Clay rotation CP1 retranslation paper)

The following can be pasted into `Gen12/targets/journal_attempts/10_poincare_retranslation/CP_CLAY_ROTATION.md` (and its Gen13 mirror `Gen13/targets/journals/tier4_framework/notices_clay_rotation/CP_CLAY_ROTATION.md`) as a footnote or sub-section in the CP6 (Hodge) block, after the "What's Proved" list:

> **Markman scope note (added 2026-04-19).** E. Markman, *Cycles on abelian 2n-folds of Weil type from secant sheaves on abelian n-folds* (arXiv:2502.03415, Feb 2025; v2 Jun 2025) and the ICM 2026 survey *Secant sheaves and Weil classes on abelian varieties* (arXiv:2509.23403, Sep 2025; v2 Feb 2026) prove the algebraicity of the Weil classes on all abelian fourfolds of Weil type — and hence the Hodge conjecture for abelian varieties of dimension $\le 5$ — by combining (i) Chevalley's theory of pure spinors and a secant-subspace construction $B \subset S^+_\mathbb{Q}$, (ii) Mukai–Polishchuk–Orlov derived equivalences on $X \times \widehat{X}$, (iii) the Buchweitz–Flenner semi-regularity theorem (extending Bloch's), and (iv) deformation through Schoen-style degeneration of hyper-Kähler Kummer-type varieties. An independent proof of the discriminant-1 fourfold case was given concurrently by Floccari and Fu (arXiv:2504.13607). Our Thread B program on the simple Weil 4-fold $A_* = \mathbb{C}^4 / (\mathbb{Z}^4 + \Omega \mathbb{Z}^4)$ with $\Omega = \tfrac{1}{2} I_4 + i(\sqrt{2}\,I_4 + \sqrt{3}\,M_2 + \sqrt{5}\,M_3)$ does not lift to Markman's secant-sheaf machinery; it operates as the explicit-coordinate companion: an integer-matrix realization $\varphi$ of the $\mathbb{Q}(i)$-action on $H^1(A_*, \mathbb{Z})$, an explicit 8-dimensional K-anti-invariant subspace $W_*$ with computed Hodge–Riemann eigenvalues $\{0.0046, 0.0231, 0.1156, 0.3834\}$, a K-equivariant Chern obstruction theorem (Sprint 29 R1-KE, residuals $< 10^{-12}$), and a 5-prime GF(p) probabilistic certificate (Sprint 33 v2) that $W_* \cap \mathbb{Q}^{70} = \{0\}$ — together strengthening Markman's existence statement on $A_*$ to the explicit conclusion that *every* rational $(2,2)$-class on this specific fourfold is K-invariant and hence Chern-class algebraic. Sprint 35b extends this to an explicit Beauville pair $A_* \leftrightarrow J(C_*)$ over $\mathbb{Q}(\sqrt{2}, \sqrt{3}, \sqrt{5})$ as the pivot toward BSD on $J(C_*)$, an extension Markman's deformation-theoretic proof does not target. The Z/10Z / CRT framing in WP39 (this volume) — where idempotent counts $2^{\omega(b)} - 2$, the cascade theorem, and balance invisibility on semiprimes appear as finite-ring shapes parallel to the Hodge structure — is, post-Markman, a structural shape match rather than a candidate lift, and is presented as such.

(Approximately 320 words; trim or expand as the final venue 10 LaTeX permits.)

---

## §6. What this scope note does NOT do

- Does not retire Sprint 29 R1-KE, Sprint 33 v2, or Sprint 35b. All three remain active under the revised "explicit-coordinate companion" framing.
- Does not modify the atlas. Atlas patch (§4 item 1) is *recommended* and routed to Brayden; this scope note does not write to `MASTER_ATLAS_v3_5_2026_04_18.md`.
- Does not retract WP39's structural framing. WP39 already labels every Z/10Z ↔ Hodge correspondence as STRUCTURAL ANALOGY; only the post-hoc Markman ↔ balanced-semiprime mapping in §6.2 should be re-tagged.
- Does not retract the "crossings → recognitions" reframing in `MASTER_ATLAS §17`. That correction is independent of and consistent with this scope note: the recognition framing already says "the bridges are done; the question is whether the lenses are coherent." Markman makes the cycle-class map's image explicit; we measure the K-anti-invariant Hodge subspace explicitly; the recognition is whether they coincide on $A_*$ — and S29 + S33 says they do, with Markman corroborating from the existence side.
- Does not propose changes to Threads A (PPM), C (Q-series / σ), or D (ξ cosmology). Three-thread + adjacent-D discipline preserved.

---

*© 2026 Brayden Ross Sanders / 7Site LLC. 7Site Human Use License v1.0. DOI: 10.5281/zenodo.18852047.*
*Compiled by ClaudeCode, 2026-04-19. Routed to Brayden for §4 atlas-patch decision and §5 venue-10 paragraph approval.*

**End of Markman internalization scope note.**
