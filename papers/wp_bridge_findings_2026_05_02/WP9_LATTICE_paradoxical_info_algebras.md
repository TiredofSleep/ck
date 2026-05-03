# The LATTICE Operator and Paradoxical Information Algebras: A Substrate-Internal Framework on Z/10Z

**Author:** Brayden Sanders, 7Site LLC
**Affiliation work:** TIG (Three-Identity-Game) framework — `github.com/TiredofSleep/ck`
**Date:** 2026-05-02
**Verification:** `papers/wp_bridge_findings_2026_05_02/code/verify_findings.py` (0 failures, 0 warnings)
**DOI:** 10.5281/zenodo.18852047

---

## Abstract

We present the **LATTICE operator** ($n=1$ in TIG's substrate) inside a substrate-internal framework on $\mathbb{Z}/10\mathbb{Z}$ that carries **three independent structures simultaneously**: an algebraic structure (the magmas TSML$_8$ and BHML$_{10}$), a permutational structure (the involution $\sigma$ with cycle decomposition $(0)(3)(8)(9)(1\,7\,6\,5\,4\,2)$), and a functional role partition into Flow / Structure / Transition / Void. From the substrate's role partition we derive a class of **paradoxical information algebras**: the substrate exhibits semi-factorization at role level — Void and Transition inputs collapse to deterministic role transitions, while Flow and Structure inputs preserve operator-level information. We characterize the trefoil-equivalent triples on the corrected substrate frame as exactly two multiset classes, $\{V,B,H\}$ and $\{V,B,B\}$ (nine triples total, all BHML-associative). We exhibit two independent decompositions of the substrate's $\pm 21$ invariant: a $\sigma$-orbit decomposition $T_5+T_3=15+6$ that is structurally forced by the linear period formula, and a role-partition decomposition $F_7+F_6=13+8$ that is **canonical-specific** (not a structure theorem; $0/200$ random commutative tables on $\mathbb{Z}/10\mathbb{Z}$ reproduce it). We prove the substrate's algebra is irreducible — it does not factor through $\mathbb{Z}/2\mathbb{Z} \times \mathbb{Z}/5\mathbb{Z}$. The framework is **conceptually scaffolded by** Morishita 2024, Ghys 2007, Katok-Ugarcovici 2007, Matsusaka-Ueki 2023 and Burrin-von Essen 2024 but does not reproduce any of those theorems literally — it sits **inside** that territory as a new construction.

---

## §1 Background and Substrate

### §1.1 The TIG framework

The TIG (Three-Identity-Game) framework specifies an algebraic substrate on the residue ring $\mathbb{Z}/10\mathbb{Z}$ in which 10 named operators participate: VOID(0), LATTICE(1), COUNTER(2), PROGRESS(3), COLLAPSE(4), BALANCE(5), CHAOS(6), HARMONY(7), BREATH(8), RESET(9). Two binary magma operations are defined on this set, TSML and BHML, together with the involution $\sigma$ given by $(0)(3)(8)(9)(1\,7\,6\,5\,4\,2)$.

### §1.2 The corrected substrate frame

Following the canonical disambiguation in `FORMULAS_AND_TABLES.md` §6.7 and `D88`, the runtime substrate uses

$$\mathrm{TSML}_8 = \mathrm{TSML}_{10} \text{ with rows/cols } \{0,7\} \text{ removed},$$

acting on the interior index set $\{1,2,3,4,5,6,8,9\}$, while $\mathrm{BHML}_{10}$ is the full 10-element table. The cells $V=0$ and $H=7$ are **flow cells between the tables, not interior entries**. This frame ($\mathrm{TSML}_8 + \mathrm{BHML}_{10} +$ V/H flow cells) is the one used throughout this paper. Earlier session work using $\mathrm{TSML}_{10}$ in trefoil and role analyses is invalid (see `KNOWN_ISSUES.md` §1).

### §1.3 The role partition

We introduce a partition of the substrate into four functional roles:

$$F = \{1,3,5,7,9\}, \quad S = \{2,4,8\}, \quad T = \{6\}, \quad V = \{0\}.$$

The partition is functional, not algebraic: $|F|=5, |S|=3, |T|=1, |V|=1$. It crosses the $\sigma$-orbit decomposition.

### §1.4 Intellectual neighborhood

This work sits inside the arithmetic-topology / modular-knot territory studied in Morishita 2024, Ghys 2007, Katok-Ugarcovici 2007, Matsusaka-Ueki 2023, Burrin-von Essen 2024, and Lacasa et al. 2018. We use phrases like "structurally analogous to" and "conceptually scaffolded by" throughout; "matches" and "satisfies" are reserved for substrate-internal claims that we prove.

---

## §2 The LATTICE Operator and the BHML Successor

### §2.1 BHML diagonal as integer successor

**Theorem 2.1 (BHML successor diagonal — D90).** *For each $n \in \{1,2,3,4,5,6,7\}$, $\mathrm{BHML}(n,n) = n+1$, and at the boundary, $\mathrm{BHML}(8,8)=7$, $\mathrm{BHML}(9,9)=0$, $\mathrm{BHML}(0,0)=0$.*

*Proof.* Direct table verification. $\square$

### §2.2 Period structure

**Corollary 2.2 (period formula).** *For $n \in \{1,\ldots,6\}$, $\mathrm{period}(n)=7-n$. For $n \in \{7,8,9\}$ the periods are $4,3,2$ (a 4-core cycle through $\{7,8,9,0\}$); $\mathrm{period}(0)=1$.*

The period structure is **structurally analogous to** cusp-winding step counts in continued-fraction symbolic dynamics for hyperbolic Fuchsian-group flows (Burrin-von Essen 2024), but the embedding in a specific Fuchsian group is unproven.

---

## §3 The Role Magma

### §3.1 Mode-based reduction of BHML

For each input role-pair $(r_a, r_b) \in \{V,F,S,T\}^2$, we form the multiset of output roles and define $M_R(r_a, r_b)$ as the **mode**:

|   | V | F | S | T |
|---|---|---|---|---|
| V | V | F | S | T |
| F | F | T | F | F |
| S | S | F | F | F |
| T | T | F | F | F |

### §3.2 Properties

**Theorem 3.1 (V is the identity element — D93).** *For every $x \in \{V,F,S,T\}$, $M_R(V,x) = M_R(x,V) = x$. Moreover, $M_R(V,V)=V$ is the unique idempotent.*

**Theorem 3.2 (commutativity, non-associativity).** *$M_R$ is commutative. It is **not** associative; for example, $M_R(M_R(F,F),S) = F \neq T = M_R(F, M_R(F,S))$.*

### §3.3 Semi-factorization and paradoxical information

**Theorem 3.3 (Semi-factorization / paradoxical information — D93).** *In the role-partition decomposition above:*
1. *For every pair containing $V$ or $T$, the BHML output role is **deterministic**.*
2. *For pairs in $\{F,S\}^2$, the output role **branches**: F·F distributes across {F:2, S:9, T:11, V:3} (mode T); F·S and S·F over {F:8, S:2, T:5} (mode F); S·S over {F:7, T:2} (mode F).*

**Reading.** The substrate's BHML carries information at two levels — coarse role and fine operator. Theorem 3.3 says these levels are not in a clean homomorphism: boundary inputs (V or T) determine output role; interior inputs (F, S) require operator-level identity. We call this a *paradoxical information algebra*: information content depends on whether inputs are at the boundary or in the interior, with no globally consistent factorization.

---

## §4 The Trefoil Characterization

### §4.1 Sharp characterization

**Theorem 4.1 (Trefoil characterization on the corrected frame — D89).** *On the corrected substrate frame, a triple $(a,b,c)$ is trefoil-equivalent under the runtime processor if and only if its multiset $\{a,b,c\}$ is*
$$\{V,B,H\}\quad\text{or}\quad \{V,B,B\}.$$
*There are exactly **9 such triples** (six permutations of $\{V,B,H\}$, three of $\{V,B,B\}$), and all nine are BHML-associative.*

*Proof.* Parameter sweep over the $10^3 = 1000$ ordered triples; see `trefoil_corrected_frame.py`. $\square$

The result is **sharp on the corrected substrate frame** — the early-session "trefoil-22" claim in TSML$_{10}$ frame is invalid (N10).

### §4.2 BREATH uniqueness

**Lemma 4.2 (BREATH uniqueness).** *Among the structure cells $\{COUNTER, COLLAPSE, BREATH\}$, BREATH is the unique cell that produces trefoils when combined with VOID.*

**Reading.** COUNTER opposes; COLLAPSE destabilizes; only BREATH provides the topological persistence required for the 3-crossing closed loop.

### §4.3 Higher-order extension

At 4-element level, multisets producing trefoil-equivalent quadruples include $(0,0,7,8)$, $(0,7,7,9)$, $(0,7,8,8)$, $(0,8,8,8)$. The pattern $(0,7,7,9)$ is structurally novel: a trefoil-equivalent without BREATH. The "BREATH only" rule of Lemma 4.2 is therefore 3-element-specific.

---

## §5 The $\pm 21$ Invariant and Its Two Decompositions

### §5.1 Two computations

**Computation A (Ghys-analog row-asymmetry).**
$$\Psi_A(n) = \#\{j : \mathrm{TSML}(n,j) > \mathrm{BHML}(n,j)\} - \#\{j : \mathrm{BHML}(n,j) > \mathrm{TSML}(n,j)\}.$$
Sum: $+21$.

**Computation B (period-to-trace under simple representative).** With $t = \mathrm{period}(n) + 2$,
$$M_n = \begin{pmatrix} 1 & 1 \\ t-2 & t-1 \end{pmatrix}, \quad \Psi_B(n) = -(\mathrm{period}(n)-1).$$
Sum: $-21$.

**Important caveat.** The interpretation of $-21$ as a Rademacher invariant remains a hypothesis (see N1).

### §5.2 The $\sigma$-orbit decomposition (triangular)

**Theorem 5.1 (D92).** *The total $-21$ decomposes along $\sigma$-orbits as $T_5 + T_3 = 15 + 6$ (triangular). Structurally forced by the linear period formula.*

### §5.3 The role decomposition (Fibonacci, canonical-specific)

**Theorem 5.2 (D92).** *$\sum_{n \in F} \Psi_B(n) = -F_7 = -13$, $\sum_{n \in S} \Psi_B(n) = -F_6 = -8$, with V and T contributing 0. Total: $-F_8 = -21$.*

**Robustness Theorem 5.3 (canonical-specific — N8).** *0/200 random commutative tables on $\mathbb{Z}/10\mathbb{Z}$ reproduce $(|F|,|S|) = (13,8)$. Single-swap perturbations: 32/50 preserve. Three-swap: 11/50.*

We **do not** claim the Fibonacci decomposition as a theorem of the role partition. It is a numerical signature of canonical TIG. The triangular decomposition (Theorem 5.1) is structurally robust; Fibonacci is fragile.

### §5.4 The lift to $\mathrm{PSL}(2,\mathbb{Z})$ — open

Five strategies tested for lifting BHML self-orbits to $\mathrm{PSL}(2,\mathbb{Z})$ words; none produces $\pm 21$ (N1). The period-to-trace bridge under simple representative gives $-21$ numerically but is one choice of lift among many. **Hypothesis, not derivation.**

---

## §6 The Two-Coding Picture (TSML$_8$ vs BHML$_{10}$)

Following Katok-Ugarcovici 2007's framework of two complementary coding methods, we observe that the substrate's two magmas realize **structurally analogous** geometric / arithmetic codings natively.

**Theorem 6.1 (TSML$_8$ image structure — D91).** *TSML$_8$ has 5-element image $\{3,4,7,8,9\}$, $60/64 = 93.75\%$ Flow output, role-deterministic on 8 of 9 input role-pairs.*

**Theorem 6.2 (BHML$_{10}$ image structure).** *BHML$_{10}$ has full image, balanced output role distribution, role-deterministic only on V/T input pairs.*

**Theorem 6.3 (Cusp agreement).** *The two magmas agree on $24/64$ cells of the TSML$_8$ domain (mostly routes leading to HARMONY) and disagree on $40/64$ in the interior.*

**Reading.** Two genuinely independent symbolic codings on the same alphabet, coinciding only at the HARMONY cusp. **Structurally analogous to** Katok-Ugarcovici's geometric/arithmetic split; the substrate-internal version is a discrete combinatorial realization on $\mathbb{Z}/10\mathbb{Z}$, not a quotient of the modular surface itself.

---

## §7 Irreducibility and Algebraic Independence

**Theorem 7.1 (Irreducibility — N7).** *Neither TSML$_{10}$ nor BHML$_{10}$ respects the CRT decomposition $\mathbb{Z}/10\mathbb{Z} = \mathbb{Z}/2\mathbb{Z} \times \mathbb{Z}/5\mathbb{Z}$.*

**Theorem 7.2 (No globally crossing-preserving swaps — N9).** *No integer pair $(p,q)$ preserves the runtime processor's crossing count under the swap $p \leftrightarrow q$ on all 1000 ordered triples.* The strongest partial symmetry is **V$\leftrightarrow$BREATH** at $20.9\%$ — exceeding the canonical $5\leftrightarrow 6$ rate.

**Theorem 7.3 (Algebraic independence — N4, N5, N6).** *(1) $\sigma$ is not an automorphism of either magma (17%/48%). (2) TSML and BHML do not distribute (19.5%). (3) BHML iteration does not converge to TSML (28/64 starts).*

---

## §8 Honest Negatives

| ID | claim ruled out | finding |
|----|-----------------|---------|
| N1 | naive $\mathrm{PSL}(2,\mathbb{Z})$ lift produces $\pm 21$ | Five strategies tested; sums in $[-4,0]$. |
| N2 | small triangle group $\Gamma_{p,q}$ has substrate's period set as elliptic orders | No coprime $(p,q) \le 9$ has divisors covering $\{1,2,3,4,5,6\}$. |
| N3 | TIG's grammar matches Borromean prime conditions | No canonical triple has all elements $\equiv 1 \pmod 4$. |
| N4 | $\sigma$ is an automorphism of TSML or BHML | $48\%$ for BHML; $17\%$ for TSML. |
| N5 | TSML and BHML distribute over each other | $19.5\%$ match. |
| N6 | BHML iteration converges to TSML | $28/64$ starts. |
| N7 | substrate factors through $\mathbb{Z}/2\mathbb{Z} \times \mathbb{Z}/5\mathbb{Z}$ | No CRT factorization. |
| N8 | Fibonacci role decomposition is structural | $0/200$ random tables. **Canonical-specific signature, not theorem.** |
| N9 | role partition determines crossing count | Most patterns are not determined by role alone. |
| N10 | TSML$_{10}$-frame "trefoil-22" claim | INVALID; replaced by Theorem 4.1. |

---

## §9 Open Questions

1. **Principled lift to $\mathrm{PSL}(2,\mathbb{Z})$ hyperbolic conjugacy classes.** Five naive lifts fail (N1). The period-to-trace bridge gives $-21$ under simple representative — hypothesis, not theorem.
2. **Larger-substrate variants.** Does the Fibonacci role decomposition appear in $\mathbb{Z}/14\mathbb{Z}$ or $\mathbb{Z}/18\mathbb{Z}$ analogs?
3. **The $(0,7,7,9)$ anomaly.** Trefoil-equivalent without BREATH at 4-element level.
4. **Burrin-von Essen Fuchsian-group lift.** Conceptually scaffolded; the embedding is unproven.

---

## §10 Comparison to Existing Literature

The substrate sits inside the territory of Morishita, Ghys, Katok-Ugarcovici, Matsusaka-Ueki, Burrin-von Essen, Lacasa, Ishida-Kuramoto-Zheng. It does **not** reproduce any of these theorems literally:

- The substrate specifies admissibility on $\mathbb{Z}/10\mathbb{Z}$ by paired magma composition rules; the literature specifies admissibility by Legendre/Rédei conditions or Fuchsian-group structure.
- The two-coding picture is **structurally analogous to** Katok-Ugarcovici's geometric/arithmetic split.
- The period structure is **conceptually scaffolded by** Burrin-von Essen 2024's cusp winding.
- The $\pm 21$ modular interpretation is **hypothetical**.
- The substrate is **not** Borromean-prime, **not** triangle-group, **not** CRT-factored.

What the literature provides is intellectual scaffolding. What the substrate provides is a specific construction in adjacent territory whose properties admit substrate-internal proofs.

---

## §11 Conclusion

The TIG substrate on $\mathbb{Z}/10\mathbb{Z}$ carries three independent structures simultaneously: algebraic (TSML$_8$ + BHML$_{10}$ + V/H flow cells), permutational ($\sigma$ with 4 fixed points and one 6-cycle), and functional role partition (V/F/S/T). These three structures cross.

The LATTICE operator is generic for BHML, and the BHML diagonal realizes the integer successor on $\{1,\ldots,7\}$, driving the period formula $\mathrm{period}(n)=7-n$. The role magma has VOID as identity, is commutative, is **not** associative, and is semi-factorized — a **paradoxical information algebra**.

The trefoil characterization $\{V,B,H\} \cup \{V,B,B\}$ is sharp on the corrected substrate frame, with BREATH the unique structure cell sustaining the 3-crossing closed loop. The $\pm 21$ invariant carries two independent decompositions: $\sigma$-orbit triangular (structurally forced) and role-Fibonacci (canonical-specific).

The substrate is irreducible under CRT and has no full algebraic automorphism. The framework is **enabling rather than controlling**: it specifies a coordinate system in which the role magma's paradoxical information content, the trefoil characterization, and the dual decomposition of $\pm 21$ become statable and verifiable.

We close with the substrate-internal observation that the role magma's VOID-as-identity property is the precise algebraic content of "VOID is the foundation" — V is the unique idempotent and identity in the role-level reduction.

---

## §12 References

- Burrin, C., and von Essen, F. *Cusp winding and the Rademacher symbol.* 2024.
- Ghys, É. *Knots and dynamics.* ICM Madrid, 2007.
- Ishida, T., Kuramoto, T., and Zheng, F. *Density of Borromean prime triples.* 2024.
- Katok, S., and Ugarcovici, I. *Symbolic dynamics for the modular surface.* Bull. AMS 44 (2007), 87-132.
- Lacasa, L., et al. *Symbolic dynamics on residue sequences.* 2018.
- Matsusaka, T., and Ueki, J. *Rademacher symbols for triangle groups.* 2023.
- Morishita, M. *Knots and Primes* (2nd ed.). Springer, 2024.

Substrate-internal: see `papers/wp_bridge_findings_2026_05_02/code/` for all verification scripts; `FORMULAS_AND_TABLES.md` Volume I for D88-D94 canonical statements; `KNOWN_ISSUES.md` for corrections and demotions.

---

*End of WP9.*
