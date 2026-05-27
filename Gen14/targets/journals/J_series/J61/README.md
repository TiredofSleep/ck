# J61 — Magma-by-ETP-Profile Taxonomy: Closure-Realizers at Small Orders

**Target venue:** *Journal of Symbolic Computation* (Elsevier)
**Alternative venues:** *Algebra Universalis* (Springer), *International Journal of Algebra and Computation*, *Mathematics of Computation*
**Status:** DRAFT — survey/methodology paper drawing on J58, J59, J60 + outside-research scan
**Author lane:** Sanders + Gish
**Tier:** A (methodology paper, all worked examples verified at machine precision via ETP)
**Source:** outside-research scan confirms novelty of magma-by-profile taxonomy approach (2026-05-27)

---

## §1 — Summary

We introduce a systematic methodology for classifying finite magmas by their ETP (Equational Theories Project, Tao et al. 2024–2025) equation profile, using the ETP catalog of 4,694 equational laws and its implication graph (44,471 verified pairwise implications, 22 million transitive implications). The methodology has three pillars:

1. **Profile cataloging**: For each magma $M$, compute $\mathrm{Profile}(M) \subset \{1, \ldots, 4694\}$ = the set of ETP equations $M$ satisfies. Tabulate by profile size and by full equation set.

2. **Closure-realizer identification**: For each implication-closure $C \subseteq \{1, \ldots, 4694\}$ in the ETP graph, identify magmas $M$ with $\mathrm{Profile}(M) = C$ exactly (= "realizers" of $C$). Distinguish realizers from supersets (magmas with $C \subset \mathrm{Profile}(M)$).

3. **Uniqueness conjectures for specific closures**: For each closure $C$ realized by magmas, ask whether the realizers form a structurally meaningful class (commutative, identity-free, congruence-simple, etc.) and prove or refute uniqueness within that class.

The methodology is applied to four concrete case studies:
- **Lo Shu D₄ orbit mod 3** (J58): 4 mod-3 magma tables, 3 ETP profile classes {60, 179, 313}, with the σ-magma's "Family C" closure (= closure of commutativity, eq 43) NOT realized at order 3.
- **σ-magma at order 10** (J59): the unique commutative-loop-realizer of Family C at order 10 (within the rigidity-theorem-distinguished class).
- **Linear classification (J60)**: linear magmas $(ax+by+c) \bmod n$ profile catalog; ℤ/n stable at profile 32, negation-magma at 294, Family C realized at $n \geq 5$.
- **Closure-class enumeration**: of the 4,694 ETP equations, 19 have implication-closure size exactly 14, forming 8 distinct closures. Family C (anchor = eq 43) is one; the others have varied anchors (all-squares-equal, depth-5 single-variable identities, etc.).

This paper synthesizes the methodology and provides a framework for future closure-realizer work.

## §2 — Why this is needed

The ETP framework (Tao et al. 2024–2025) provides:
- The 4,694-equation catalog
- The implication graph (22M directed edges)
- Tools for testing equations against magmas (`explore_magma.py`)
- Datasets of tabulated magmas (Generated/All4x4Tables/data/ — 1,355 magmas)

The ETP framework does NOT provide:
- A systematic catalog of which *magmas* realize specific closures
- Uniqueness results for specific closure classes
- Engineering recipes for constructing magmas at target profile sizes

This paper fills the gap by formalizing the magma-by-profile classification methodology.

## §3 — Outside research positioning

Outside our work, no other research effort appears to be doing systematic magma-by-ETP-profile taxonomy. Related but distinct efforts:
- **Schröder's 990 quasigroup laws revival** (arXiv 2603.29909, 2026): implication semilattice on a smaller 990-equation list. Uses ETP infrastructure but on equation relationships, not magma cataloging.
- **"The latent space of equational theories"** (arXiv 2601.20759, 2026): ML embedding of ETP equations by satisfaction probability. Classifies equations, not magmas.
- **Drápal-Wanless (2021)** on maximally non-associative quasigroups: structural extremum, not profile classification.
- **McKay-Meynert-Myrvold (2007)**: classical Latin square enumeration, no profile annotation.

Our work uses ETP's infrastructure but pursues the orthogonal taxonomy question.

## §4 — Tier discipline

- **PROVED.** Every profile-size claim verified at machine precision via ETP. The implication-closure of commutativity = 14 specific IDs (proved via ETP's `implications.json`).
- **COMPUTED.** All worked examples (Lo Shu, σ-magma, BHML, CL_STD, σ_10^min, 480 order-5 commutative QGs) verified.
- **CONJECTURED (Tier C).** Family C is the unique commutative profile-14 family at all orders ≥ 5 (verified at order 5; open at orders 6+).

## §5 — Citation footprint

Sanders, B.R., Gish, M. (2026). "Magma-by-ETP-Profile Taxonomy: Closure-Realizers at Small Orders." Submitted to *Journal of Symbolic Computation*.
