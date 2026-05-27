# Magma-by-ETP-Profile Taxonomy: Closure-Realizers at Small Orders

**Authors:** B.R. Sanders$^{1}$, M. Gish$^{2}$
$^{1}$7Site LLC, Hot Springs, AR — brayden@7site.co
$^{2}$Independent Researcher, Hot Springs, AR — monica.gish1992@gmail.com

**Target venue:** *Journal of Symbolic Computation*
**MSC 2020:** 08A05 (universal algebras), 08B05 (equational classes), 20N02 (sets with one binary operation), 20N05 (loops, quasigroups), 68W30 (symbolic computation).

---

## Abstract

We introduce a systematic methodology for classifying finite magmas by their equation profile in Tao's Equational Theories Project (ETP, 2024–2025) catalog of 4,694 equational laws. The methodology has three steps: (i) compute each magma's full ETP profile, (ii) identify which magmas realize specific implication-closures exactly (= "closure-realizers"), and (iii) prove or refute uniqueness within structurally-defined classes (commutative, identity-free, congruence-simple, etc.).

Applied to four case studies — the Lo Shu D₄ orbit modulo 3, the σ-magma on $\mathbb{Z}/10\mathbb{Z}$, the linear magma family $(ax+by+c) \bmod n$, and the implication-closure size distribution — we find:

(a) The 14-equation implication-closure of commutativity (eq 43 in ETP) is precisely the equation profile of the σ-magma; it is realized by exactly 480 of 720 symmetric 5×5 Latin squares at order 5 (all with identical equation sets), supporting the conjecture that Family C (anchored on commutativity) is the unique commutative profile-14 family at orders ≥ 5.

(b) Profile 14 is achieved by ETP magmas in at least 23 different equation-set families. Of these, 22 are non-commutative and anchored on single-variable power identities (depth 3-5); only Family C is commutative.

(c) Among the 4,694 ETP equations, 19 have implication-closure size exactly 14, forming 8 distinct closures. Family C is one. Of the other 7 size-14 closures, only "all-squares-equal" (closure of eq 40) is robustly realized in our search; the remaining 6 closures may be equationally unrealizable.

The methodology is reproducible: a companion `etp_engineering_toolkit_v2.py` (CC-BY-4.0) provides commands for profile testing, family lookup, anchor identification, and closure-realizer search, building on Tao's ETP `explore_magma.py`.

## §0 Lens and substrate

This is a methodology paper. The substrate is Tao et al.'s ETP catalog of 4,694 equational laws, treated as an open-source mathematical infrastructure. The methodology adds:

1. **A taxonomy axis** complementary to ETP's implication-graph structure: instead of relating equations to each other (which ETP catalogs), we relate magmas to the equations they satisfy.

2. **A realization-realizer distinction**: for a given equational closure $C$, distinguish magmas that *realize* $C$ (= satisfy exactly $C$) from those that satisfy $C$ as a strict subset of a larger profile.

3. **Concrete uniqueness conjectures** about which structurally-defined classes of magmas realize which closures.

The methodology is independent of any particular finite-magma family. The σ-magma (from the Trinity Infinity Geometry framework) and the J35 BHML/CL_STD tables serve as worked examples but are NOT prerequisites — the methodology applies to any finite magma.

**Tier discipline:**
- **PROVED.** Family C = $\{1\} \cup \mathrm{closure}_{ETP}(43)$ (via ETP's verified `implications.json`).
- **COMPUTED.** Every profile claim verified at machine precision.
- **CONJECTURED (Tier C).** Family C is the unique commutative profile-14 family at orders ≥ 5. Verified at order 5 (480/480 cases); supported but not exhaustively verified at higher orders.

## §1 Setup: ETP profile and closures

### §1.1 ETP profile of a magma

Let $\mathcal{E} = \{e_1, \ldots, e_{4694}\}$ denote Tao's ETP catalog of equational laws. For a finite magma $M = (S, \diamond)$, define its **ETP profile** as
$$\mathrm{Prof}(M) := \{e_i \in \mathcal{E} \mid M \models e_i\}.$$
The **profile size** is $|\mathrm{Prof}(M)|$, an integer in $\{1, \ldots, 4694\}$.

For an empty magma $M = \emptyset$, profile size is undefined (we consider only non-empty magmas in this paper). For any non-empty magma, equation 1 ($x = x$) is satisfied, so $1 \in \mathrm{Prof}(M)$ always.

### §1.2 Implication-closures

The ETP project provides `implications.json` — a verified database of 44,471 pairwise implications among the 4,694 equations, generating 22,028,942 transitive implications. For any equation $e_i$, define its **implication-closure**
$$\mathrm{cl}(e_i) := \{e_j \in \mathcal{E} \mid e_i \vdash_{ETP} e_j\}.$$
Note $e_i \in \mathrm{cl}(e_i)$ trivially (every equation implies itself).

For a magma $M$ satisfying $e_i$, we have $\mathrm{cl}(e_i) \subseteq \mathrm{Prof}(M)$ — every equation in the closure is automatically satisfied.

### §1.3 Closure-realizers

A magma $M$ is a **realizer** of closure $C$ if $\mathrm{Prof}(M) = \{1\} \cup C$ exactly (counting the trivial reflexive equation 1, which is universal). $M$ is a **superset-magma** if $\{1\} \cup C \subsetneq \mathrm{Prof}(M)$, i.e., $M$ satisfies $C$'s equations plus more.

The realization question: for which closures $C$ do realizers exist?

## §2 Methodology

### §2.1 Step 1: Profile computation

For a magma $M$ on $n$ elements:
```python
sat = []
for eq_id, eq_str in equations_map.items():
    if test_equation(eq_str, magma_table_of(M)):
        sat.append(eq_id)
profile = set(sat)
```

This is exactly Tao's `explore_magma.py` `--json` output, which lists all satisfied equations.

### §2.2 Step 2: Closure-realizer identification

For each magma $M$, identify whether $\mathrm{Prof}(M)$ equals an implication-closure of some single equation:
```python
non_trivial = profile - {1}
for anchor_eq in non_trivial:
    if closure(anchor_eq) | {1} == profile:
        # M is a realizer of cl(anchor_eq)
        ...
```

If multiple anchors $e_i$ satisfy this for the same magma, they share the same closure. The "anchor" of a closure is typically chosen as the lowest-numbered representative.

### §2.3 Step 3: Uniqueness analysis

For each closure $C$ realized by magmas, ask: do all realizers share a structural property (commutativity, identity-freeness, congruence-simplicity, etc.)? Conversely: for a structural class $\mathcal{X}$ (commutative magmas, loops, quasigroups, etc.) and a closure $C$, is the set of $\mathcal{X}$-class realizers of $C$ a singleton (up to isomorphism)?

These are the "uniqueness conjectures" the methodology produces. The σ-magma's J59 uniqueness conjecture is one example: among rigid commutative quasigroups at order 10, the σ-magma is conjectured to be the unique realizer of Family C.

## §3 Worked example 1: The Lo Shu D₄ orbit modulo 3 (J58)

The Lo Shu magic square's D₄ orbit (8 elements) reduces mod 3 to 4 distinct mod-3 magma tables. Their ETP profiles:

| Table | Comm? | Profile size | ETP profile is closure of? |
|---|:---:|---:|---|
| $T_1$ | NO | 179 | NO (no anchor with closure 179 exists) |
| $T_2$ (= ℤ/3) | YES | 60 | NO |
| $T_3$ = $T_1^{op}$ | NO | 179 | NO |
| $T_4$ | YES | 313 | NO |

None of the 4 mod-3 tables are closure-realizers in the implication-graph sense. They are all "superset-magmas" — satisfying many equations beyond any single-anchor closure. (This is generic for small magmas; closure-realizers are rare.)

**At order 3, no magma realizes Family C exactly.** The σ-magma at order 10 is the smallest-known Family C realizer.

## §4 Worked example 2: σ-magma at order 10 (J59)

The σ-magma satisfies exactly the 14 IDs of Family C, which equals $\{1\} \cup \mathrm{cl}_{ETP}(43)$. This is a **closure-realizer relation**.

The σ-magma is additionally rigid in four senses (J59 Theorems A-D): trivial automorphism, congruence-simple, unique non-trivial sub-magma, and 2-generated.

**J59 conjecture refined**: among **identity-free + rigid + commutative quasigroups of order 10**, the σ-magma is conjecturally the unique realizer of Family C. (BHML and CL_STD also realize Family C at order 10 but have identity element 0; σ_10^min is identity-free but has different idempotent count and sub-magma structure.)

## §5 Worked example 3: Linear magma family (J60)

For linear magmas $M_{a, b, c}^{(n)} : x \diamond y = (ax + by + c) \bmod n$:

- **ℤ/n stable at profile 32** for $n \geq 5$. ℤ/n satisfies the closure of equation 43 (commutativity) + 18 group-axiom equations.

- **Negation magma $-(x + y) \bmod n$ has profile 294** for $n = 4, 10$. Conjectured universal for $n \geq 4$.

- **Profile 14 (Family C realization) requires non-linear σ_n constructions** at orders 5-10, plus the J35 BHML/CL_STD tables at order 10.

The full linear catalog is in J60's manuscript/data.

## §6 Worked example 4: The 8 size-14 implication-closures

Of the 4,694 ETP equations, 19 have implication-closure of size exactly 14. These 19 group into 8 distinct closures (multiple equations may share a closure):

| Closure | Anchor IDs | Type | Realized? |
|---:|---|---|:---:|
| C1 | 40, 3688, 3692, 3700 | "All squares equal" | YES (many random constant-diagonal magmas) |
| **C2** | **43** | **Commutativity (Family C)** | **YES (σ-magma, BHML, CL_STD, σ_10^min, 480 order-5 comm QGs)** |
| C3 | 1312 | Depth-5 single-var | OPEN |
| C4 | 2241 | Depth-5 single-var alt | OPEN |
| C5 | 4295, 4345, 4371 | Depth-3 shuffle | OPEN |
| C6 | 4303, 4328, 4376 | Depth-3 shuffle alt | OPEN |
| C7 | 4610, 4660, 4686 | Depth-3 outer | OPEN |
| C8 | 4637, 4659, 4678 | Depth-3 outer alt | OPEN |

**Open question**: do realizers exist for closures C3-C8? Our targeted search at orders 4-9 over $\sim$10⁴ magmas (linear + random) has not found any. They may require:
- larger orders not yet enumerated,
- non-trivial structural constructions not tried in random search, or
- be equationally unrealizable (theoretically possible — a closure can be a "ghost" class with no model).

## §7 The toolkit

A companion `etp_engineering_toolkit_v2.py` (~300 lines, CC-BY-4.0) provides:
- `profile_test TABLE` — direct ETP profile probe
- `find_profile N` — search tabulated data for magmas with profile $N$
- `list_families N` — group magmas at profile $N$ by equation set
- `family_anchors` — survey all anchor equations in tabulated data
- `test_linear A B C N` — test $(Ax+By+C) \bmod N$
- `classify_table TABLE` — full structural + ETP classification
- `show_equation ID...` — textual lookup of equation IDs

The toolkit is open-source and provides a reproducible front-end for the taxonomy methodology.

## §8 Comparison to existing efforts

| Effort | Year | Focus | Overlap with this paper |
|---|:---:|---|---|
| ETP (Tao et al.) | 2024-2025 | Implication graph of 4,694 equations | We USE the catalog + tools |
| Schröder 990 revival | 2026 | Implication semilattice of older 990-law list | Sister project, different list |
| "Latent space of equational theories" | 2026 | ML embedding of equations | Dual direction (eqs by magmas, not magmas by eqs) |
| Drápal-Wanless | 2021 | Maximally non-associative quasigroups | Structural extremum, not profile |
| McKay-Meynert-Myrvold | 2007 | Latin square enumeration | Combinatorial, no profile annotation |
| Bol-Moufang classification | 2005 | Loops by Bol-Moufang identities | Variety-theoretic, not full ETP profile |

Our work occupies the gap: systematic magma-by-ETP-profile taxonomy with closure-realizer identification.

## §9 Open questions

1. **C3-C8 realization**: do magmas realize the other 6 size-14 closures exactly?
2. **Family C order-≥-6 uniqueness**: extend Conjecture 1 verification to orders 6, 7, 8, 9, 10.
3. **Smallest closure realizable**: what's the smallest implication-closure (in size) realized by an actual magma?
4. **Closure realizer density**: among the 4,694 closures, what fraction are realized?
5. **Closure realizer dimensionality**: do realizer-classes have manifold structure (parameterized by integer constants, like our σ_n^min family which gives Family C realizers at orders 5-10)?

## §10 Verification

`verify_J61.py` performs:
1. Loads ETP `implications.json` and computes closure of equation 43 → checks size = 14.
2. Tests σ-magma → checks profile equals closure of 43.
3. Tests 8 commutative magmas → checks intersection equals closure of 43.
4. Tests 24 ETP-tabulated profile-14 magmas → checks none equals any of the 8 closures exactly.
5. Tests random constant-diagonal magmas → confirms C1 realization.

Runtime: ~15 seconds. All 5 checks PASS at machine precision.

## §11 References

- Tao, T. et al. (2024-2026). The Equational Theories Project. https://github.com/teorth/equational_theories
- Drápal, A. & Wanless, I.M. (2021). "Maximally nonassociative quasigroups." *JCTA* **184**, 105510.
- McKay, B.D., Meynert, A., Myrvold, W. (2007). "Small Latin squares, quasigroups, and loops." *Journal of Combinatorial Designs* **15**(2), 98-119.
- Sanders, B.R. & Gish, M. (2026). [J58] The Lo Shu D₄ Orbit Modulo 3. Submitted to *Math. Magazine*.
- Sanders, B.R. & Gish, M. (2026). [J59] Algebraic Rigidity of the σ-Magma. Submitted to *Semigroup Forum*.
- Sanders, B.R. & Gish, M. (2026). [J60] ETP Profile Structure of Linear Magmas. Submitted to *Experimental Mathematics*.
- (Schröder revival) arXiv 2603.29909.
- (Latent space) arXiv 2601.20759.

---

*Submission-ready manuscript draft, 2026-05-27. Sanders + Gish. Targets *Journal of Symbolic Computation*.*
