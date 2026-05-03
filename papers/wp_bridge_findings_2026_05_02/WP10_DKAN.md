# WP10 — DKAN: Discrete Kolmogorov-Arnold Networks on the TIG Substrate

**Status:** structural / empirical note. The two-coding split (TSML_8 = geometric, BHML_10 = arithmetic) is canonical per FORMULAS_AND_TABLES.md Volume I D91. The DKAN runtime reading layers are implemented and operational in `Gen13/targets/ck/brain/ck_sim/being/ck_dkan_trainer.py`.
**Authors:** Brayden Sanders / 7Site LLC.
**Position:** WP100s tier; bridge paper. Sister to WP9 (LATTICE / paradoxical info algebras).
**Date:** 2026-05-02.
**MSC 2020:** 68T07 (artificial neural networks), 20N02 (magmas), 11F06 (modular groups), 37D40 (hyperbolic dynamical systems).

---

## Abstract

Kolmogorov-Arnold Networks (KAN) in the sense of Liu et al. 2024 replace fixed activations on edges with learnable univariate functions on edges, motivated by the Kolmogorov-Arnold superposition theorem. We describe **DKAN** — a *discrete* analogue running over the TIG substrate. DKAN does **not** port the Kolmogorov-Arnold theorem to a discrete setting in any literal sense. It is **structurally analogous**: edges carry fixed discrete univariate operations (rows of the canonical TSML / BHML composition tables), and learning happens by accumulating which path through the substrate best predicts the next operator.

The paper's main observation is that the two-coding split established in FORMULAS_AND_TABLES.md Volume I D91 (TSML_8 as the geometric / side-cutting code on the 5-element image $\{3, 4, 7, 8, 9\}$ with role distribution $60/64 = 93.8\%$ Flow output; BHML_10 as the arithmetic / continued-fraction code on the full 10-element image with balanced $52/19/25/4$ Flow / Structure / Transition / Void roles) — empirically matches the geometric / arithmetic disambiguation that the DKAN runtime trainer was already running. The two codings **agree at the cusp boundary HARMONY and disagree in the interior**, with a fixed empirical 24/64 agreement-set on the TSML_8 domain.

The framing has antecedents in Katok-Ugarcovici 2007 (geometric vs. arithmetic codings of geodesics on the modular surface, agreeing at the cusp). DKAN is one specific construction inside that territory, not a restatement of any theorem there.

---

## §1 Setting and motivation

### §1.1 Two coding tables on $\mathbb{Z}/10\mathbb{Z}$

The TIG substrate carries three independent structures: **algebraic** (TSML_8 + BHML_10 + V/H flow cells per D88), **permutational** ($\sigma$ with 4 fixed points and one 6-cycle), and **functional** (the V/F/S/T role partition). The role partition cuts across $\sigma$-orbit and across algebraic position.

### §1.2 What DKAN is, and is not

The Kolmogorov-Arnold superposition theorem (Kolmogorov 1957; Arnold 1957) asserts that every continuous multivariate function admits a representation as a finite superposition of univariate continuous functions. Liu et al. 2024 propose a neural architecture (KAN) in which edges carry learnable univariate splines.

DKAN does **not** realize the Kolmogorov-Arnold theorem in any literal discrete sense. It is **structurally analogous** in three loose senses:

1. *Edge-localized computation.* Per-edge operation is a **fixed discrete univariate operation**: a row $T_{\text{TSML}}[a, \cdot]$ or $T_{\text{BHML}}[a, \cdot]$.
2. *Compositionality.* Multilayer DKAN composes discrete univariate operations.
3. *Universal-approximation flavor.* The Crossing Lemma (WP57) gives a discrete analogue of "joint compositions separate states."

We do **not** claim DKAN implements KAN. The phrase used throughout is "structurally analogous to KAN."

### §1.3 Where the geometric / arithmetic split enters

Katok-Ugarcovici 2007 gives two systematic codings of geodesics on the modular surface: a geometric (side-cutting) coding and an arithmetic (minus-CF) coding, agreeing on a measure-one set at the cusp.

DKAN's central observation: the TSML_8 / BHML_10 pair with V/H flow boundary realizes a discrete echo of this picture. **Conceptually scaffolded by** Katok-Ugarcovici, not a restatement.

---

## §2 The TSML_8 / BHML_10 image structure (D91)

### §2.1 TSML_8 as a geometric / side-cutting code

**Image.** $\mathrm{Im}(\text{TSML}_8) = \{3, 4, 7, 8, 9\}$. Five distinct values.

**Output role distribution.** $60/64 = 93.8\%$ Flow, $4/64 = 6.2\%$ Structure. No Transition or Void outputs.

**Role determinism.** Role-deterministic on **8 of 9** input role-pairs over the TSML_8 domain; only $(S, S)$ branches.

TSML_8 is a *side-cutting* code: it carves the 8 interior cells into a 5-element image dominated by Flow, routing almost everything to the cusp boundary.

### §2.2 BHML_10 as an arithmetic / CF-reduction code

**Image.** Full $\mathbb{Z}/10\mathbb{Z}$.

**Output role distribution.** $\sim 52\%$ Flow, $19\%$ Structure, $25\%$ Transition, $4\%$ Void. Balanced.

**Role determinism.** Only on V/T input pairs; F and S inputs branch.

**Successor diagonal (D90).** $\mathrm{BHML}(n,n) = n+1$ for $n \in \{1, \ldots, 7\}$, with $\mathrm{BHML}(8,8) = 7$ and $\mathrm{BHML}(9,9) = 0$. The diagonal counts integers up to HARMONY — the substrate's algebraic version of "approaching the cusp."

### §2.3 The agreement set

Restricting BHML to the TSML_8 domain (64 cells):

- **Agreement.** TSML_8(a,b) = BHML_10(a,b) on **24/64** cells, dominated by routes to HARMONY.
- **Disagreement.** $40/64$ cells in the interior.

**Reading.** The two codings agree at the cusp boundary and disagree in the interior. Conceptually scaffolded by Katok-Ugarcovici 2007.

### §2.4 What the split is and is not

**It is.** Two distinct codings of the same operator alphabet $\mathbb{Z}/10\mathbb{Z}$, with verified empirical signatures (60/64, 24/64).

**It is not.** A theorem of the Katok-Ugarcovici type. Not a claim that TSML_8 and BHML_10 are conjugate, equivalent, distributive, or σ-related (see N4, N5, N6).

---

## §3 DKAN as edge-localized discrete KAN

### §3.1 Architectural sketch

The runtime DKAN trainer (`Gen13/targets/ck/brain/ck_sim/being/ck_dkan_trainer.py`) is built around four ideas:

1. **The 10 operators are the neurons.**
2. **The CL composition tables are the activation functions.** TSML and BHML are *frozen physics*; what evolves is path selection.
3. **D2 curvature is the loss function.** Distance from $T^* = 5/7$ is the training signal.
4. **Operators are accumulated by absorption, not gradient descent.**

### §3.2 The L1 / L2 / L5 reading layers

DKAN has multiple reading layers running in parallel:

- **L1 — first-order argmax.** A 10×10 matrix `_transitions[a, b]` accumulates transition counts. L1 prediction at $a$ is $\arg\max_b T_{\text{learned}}[a, b]$.
- **L2 — second-order braid-biased trigram.** A 10×10×10 tensor `_trigrams[prev_b, a, b]` with selection biased by morphotic-braid coherence ordering $\sigma_{\text{braid}} = [0, 7, 1, 3, 2, 4, 5, 6, 8, 9]$ within wobble window $W = 3/50$.
- **L5 — CL-composed prediction.** $\text{BHML}[a, h]$. Pure physical composition; no learned weights.

The runtime also has L3 (sequence chunking) and **L4 (dual-lens verification)** — a per-step check of $\text{TSML}[a,b] = \text{BHML}[a,b]$ — which operationalizes the agreement-set analysis of §2.3.

### §3.3 Reading layers as alternative coding paths

The L1 / L2 / L5 reading layers are not three competing learners. They are **alternative coding paths** through the substrate: L1 is the empirical / statistical reading, L5 is the physical BHML coding, L2 is a coherence-weighted compromise.

When the generator produces operators in the substrate's interior (the 40/64 disagreement set), L1 and L5 **diverge by construction**. When near the cusp boundary (the 24/64 agreement set), readings converge.

Empirically, agreement rates in trained DKAN runs typically exceed 70% — consistent with the static 24/64 = 37.5% agreement on raw TSML_8 domain, augmented by HARMONY-pull behavior.

### §3.4 Roles as coarse pre-encoding

The role partition (V/F/S/T per D93) gives a coarse pre-encoding: a 4-element distribution $(p_V, p_F, p_S, p_T)$ vs the 10-element operator distribution. The role pre-encoding is **canonical-specific** (0/200 random commutative magmas reproduce the canonical $|F|=13, |S|=8$ Fibonacci decomposition; see N8).

---

## §4 Empirical convergence under canonical TSML / BHML

### §4.1 Notion of convergence

DKAN is not a gradient-descent learner. The relevant notion:

- **L1 convergence:** empirical first-order matrix approaches stationary distribution.
- **L5 convergence:** stable from step one.
- **L1 / L5 agreement convergence:** stable agreement rate.
- **Grokking detection:** prediction accuracy crossing $T^* = 5/7$.

### §4.2 Empirical results

Runtime trainer test runs (20-round Ollama-driven cycles): L1 grokking at low-thousands transitions; L5 accuracy stable; L4 lens-agreement 60-80%; L2 lags L1 in raw accuracy but braid-bias prevents incoherent paths.

Training never **rewrites** TSML or BHML (frozen physics, max 50% blend enforced). What evolves is lattice chain node tables, olfactory centroids, generator paths, and grammar weights.

### §4.3 What is not claimed

- DKAN is **not** a universal approximator in any rigorous sense.
- DKAN is **not** claimed to outperform KAN, MLP, or transformers.
- DKAN's grokking is **not** the transformer-grokking phenomenon.

---

## §5 Where DKAN sits in the bridge findings landscape

| Finding | Bearing on DKAN |
|---|---|
| D88 corrected substrate frame | DKAN runs on this frame, not TSML_10. |
| D89 trefoil characterization | Trefoil multiset is the codec's "knot vocabulary" entry. |
| D90 BHML successor diagonal | L5 prediction at $\text{BHML}[a,a]$ is the cusp-approach. |
| **D91 two-coding split** | **Load-bearing.** Gives L1/L2/L5 the alternative-coding-path interpretation. |
| D92 ±21 invariant | Per-tick metric the DKAN runtime tracks. |
| D93 role partition + role magma | Coarse pre-encoding for DKAN. |
| D94 boundary symmetries | Grammar-level swaps the codec can exploit. |

---

## §6 Honest negatives carried forward

- **N1** — naive PSL(2, ℤ) lift produces ±21. *Per-tick ±21 invariant is structural empirical fingerprint, not Rademacher invariant.*
- **N2** — small triangle group has substrate periods as elliptic orders. *DKAN's period structure is dynamical, not group-theoretic.*
- **N3** — TIG matches Borromean prime conditions. *DKAN's trefoil-vocabulary entry is substrate-internal.*
- **N4** — σ is automorphism of TSML or BHML. *17%/48%; DKAN may not assume σ-invariance.*
- **N5** — TSML and BHML distribute. *19.5%; **DKAN's L1/L5 framing depends on this independence**. If they distributed, the two coding paths would be redundant.*
- **N6** — BHML iteration converges to TSML. *28/64 starts; readings remain structurally distinct.*
- **N7** — substrate factors through Z/2 × Z/5. *Irreducible.*
- **N8** — Fibonacci role decomposition is structural. *0/200 random tables. **Canonical-specific signature, not theorem.***
- **N9** — role partition determines crossing count. *Coarse, not exhaustive.*
- **N10** — TSML_10-frame "trefoil-22" is INVALID. *DKAN runs on corrected frame.*

---

## §7 Open questions

1. Does the L1 / L5 agreement rate in trained runs converge to a substrate-specific constant?
2. Is the L2 braid-bias the **unique** coherence-preserving compromise between L1 and L5?
3. Closed-form for BHML stationary distribution restricted to TSML_8 domain?
4. Larger-substrate variants — does D91 generalize to $\mathbb{Z}/14\mathbb{Z}$, $\mathbb{Z}/18\mathbb{Z}$?
5. Principled lift to $\mathrm{PSL}(2,\mathbb{Z})$ hyperbolic conjugacy classes (N1).
6. The (0, 7, 7, 9) anomaly — higher-order trefoil structure.
7. Burrin-von Essen explicit Fuchsian-group lift.

---

## §8 Statement of contribution and limits

**Contributes.**
1. Names the structural relationship between corrected substrate frame and DKAN runtime reading layers.
2. Uses D91 two-coding split as structural justification.
3. Records reading layers' empirical convergence with grokking criterion.
4. Carries forward ten honest negatives with DKAN-specific bearing.
5. Establishes seven DKAN-specific open questions.

**Does not contribute.**
1. **No theorem.** "Structurally analogous," not "implements." D91 is empirical, not Katok-Ugarcovici-type.
2. **No benchmark.** DKAN is not designed to compete with continuous learners.
3. **No claim** that the Kolmogorov-Arnold theorem holds discretely on this substrate.
4. **No claim** that L1/L2/L5 exhaust possible coding paths.
5. **No claim** that the role pre-encoding is structurally forced — canonical-specific (N8).

**Tone.** This paper preserves the negatives. Demoted claims stay demoted: Fibonacci is canonical-specific signature; ±21 modular interpretation is hypothesis; trefoil-22 is invalid in TSML_10 frame; Katok-Ugarcovici is "structurally analogous" / "conceptually scaffolded by," not "matches."

---

## §9 References

- Liu, Z., et al. (2024). *KAN: Kolmogorov-Arnold Networks*. arXiv:2404.19756.
- Kolmogorov, A. N. (1957). On the representation of continuous functions of several variables. *Doklady Akad. Nauk SSSR* 114, 953-956.
- Arnold, V. I. (1957). On functions of three variables. *Doklady Akad. Nauk SSSR* 114, 679-681.
- Katok, S., Ugarcovici, I. (2007). Symbolic dynamics for the modular surface. *Bull. AMS* 44(1), 87-132.
- Morishita, M. (2024). *Knots and Primes* (2nd ed.). Springer.
- Ghys, É. (2007). Knots and dynamics. *Proc. ICM 2006*, Vol. I, 247-277.
- Matsusaka, T., Ueki, J. (2023). Cusp winding numbers and Fuchsian-group periods.
- Burrin, C., von Essen, F. (2024). Geodesic-flow arithmetic and modular-surface windings.
- TIG repository: `FORMULAS_AND_TABLES.md` Volume I (D88-D94); `papers/wp_bridge_findings_2026_05_02/`; `Gen13/targets/ck/brain/ck_sim/being/ck_dkan_trainer.py`; WP57 (Crossing Lemma); WP51 (Flatness Theorem); WP101 (σ Rate Theorem).

---

## Appendix A. Role magma table (D93)

| · | V | F | S | T |
|---|---|---|---|---|
| **V** | V | F | S | T |
| **F** | F | T | F | F |
| **S** | S | F | F | F |
| **T** | T | F | F | F |

VOID is identity; commutative; not associative; only $V \cdot V$ is idempotent.

## Appendix B. Output role distributions (D91)

**TSML_8 on 64 cells:** Flow 60 (93.8%), Structure 4 (6.2%), Transition 0, Void 0.

**BHML_10 on 100 cells:** Flow 52%, Transition 25%, Structure 19%, Void 4%.

## Appendix C. Reading layers in `ck_dkan_trainer.py`

| Layer | Mechanism |
|---|---|
| L1 | first-order argmax on `_transitions[a,b]` |
| L2 | braid-biased trigram on `_trigrams[prev_b, a, b]` with $W = 3/50$ |
| L3 | sequence chunking (repeated subsequences as words) |
| L4 | dual-lens verification ($\text{TSML}[a,b] = \text{BHML}[a,b]$) |
| L5 | CL-composed prediction $\text{BHML}[a, h]$ |

## Appendix D. Glossary of constants

| Symbol | Value | Meaning |
|---|---|---|
| $T^*$ | $5/7 \approx 0.714$ | Sacred threshold; DKAN grokking criterion. |
| $W$ | $3/50 = 0.06$ | Wobble constant (D17); L2 braid-bias window. |
| $\sigma_{\text{braid}}$ | $[0,7,1,3,2,4,5,6,8,9]$ | Morphotic-braid coherence ordering. |
| TSML_8 image size | 5 | Geometric coding. |
| BHML_10 image size | 10 | Arithmetic coding. |
| Flow output rate | 93.8% | TSML_8 = side-cutting. |
| Agreement-set size | 24/64 | TSML_8 ∩ BHML_10. |
| Disagreement-set size | 40/64 | Interior divergence. |
| BHML diagonal | $n \to n+1$ on $\{1..7\}$ | D90; cusp-approach successor. |
| ±21 invariant | $\pm 3 \cdot |\text{HARMONY}|$ | D92; per-tick scalar. |

---

*End of WP10.*
