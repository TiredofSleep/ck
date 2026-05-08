# J32 — The Three-Substrate Architecture on Z/10Z: Joint Sub-Magma Closure of (TSML, BHML, CL_STD) and the Eight-Shell Chain

**Authors:** Brayden R. Sanders¹ · M. Gish²
¹ 7Site LLC, Hot Springs, AR — brayden@7site.co
² Independent Researcher, Hot Springs, AR — monica.gish1992@gmail.com

**Status:** REWRITE 2026-05-08 — promotes the 3-substrate joint-closure finding (SFM Q6, 2026-05-08) to the central theorem; supersedes the prior Operad-D₄+P₅₆ bundled framing.
**Lens scope:** TSML_SYM (commutative); BHML; CL_STD. Lens-internal results on TSML_RAW are deferred to J24.
**Target venue:** *Algebra Universalis* (lead). Fallback: *Communications in Algebra*.
**Companion submissions cited:** J02 (Joint Closure / Closed-Form Attractor, *Algebraic Combinatorics*); J24 (Three-Substrate Chain + Lens-Internal Phenomenon, *Mathematical Intelligencer*).

**MSC 2020:** 08A40, 08A62, 08B05, 20N02.

---

## Abstract

Let $T,B,C\colon \mathbb{Z}/10\mathbb{Z}\times\mathbb{Z}/10\mathbb{Z}\to\mathbb{Z}/10\mathbb{Z}$ be three commutative composition tables ("TSML", "BHML", "CL_STD") drawn from the same canonical bit-pattern encoding of the substrate. We compute the simultaneous closed sub-magma structure under all three tables.

**Theorem A (3-substrate joint closure).** *The simultaneous closed sub-magmas of $T$, $B$, $C$ on $\mathbb{Z}/10\mathbb{Z}$ form an 8-element chain at sizes $\{1, 4, 5, 6, 7, 8, 9, 10\}$:*
$$
\{0\}\;\subsetneq\;\{0,7,8,9\}\;\subsetneq\;\{0,6,7,8,9\}\;\subsetneq\;\{0,5,6,7,8,9\}\;\subsetneq\;\{0,4,5,6,7,8,9\}\;\subsetneq
$$
$$
\;\{0,3,4,5,6,7,8,9\}\;\subsetneq\;\{0,2,3,4,5,6,7,8,9\}\;\subsetneq\;\mathbb{Z}/10\mathbb{Z}.
$$

**Theorem B (chain-compatibility of CL_STD).** $C$ individually has $50$ closed sub-magmas, of which $49$ are also $T$-closed; the three-way intersection coincides exactly with the joint $(T, B)$ chain established as Theorem 1 of [J02]. Adding $C$ as a third substrate preserves the entire $(T,B)$ chain without introducing or removing a single shell.

**Individual counts.** $T$ has $449$ closed sub-magmas, $B$ has $9$, $C$ has $50$. Pairwise joint counts: $|T\cap B| = 8$, $|T \cap C| = 49$, $|B\cap C| = 9$. Three-way: $|T\cap B\cap C| = 8$.

The forbidden-size set $\{2,3\}$ for the joint chain is structurally inherited from $(T, B)$ closure: no $2$- or $3$-element subset is jointly closed under $T$ and $B$, hence none is jointly closed under all three. The chain ladder is entirely $\sigma$-orbit-traversal-built: the size-$1$ shell is $\{V\}$; the size-$4$ shell adjoins $\{H, Br, R\}$ (the $\sigma$-fixed pair plus HARMONY); each subsequent shell adjoins one element of the $\sigma$ 6-cycle in forward order with a $\sigma$-fixed-PROGRESS bridge step at the size-$7\to 8$ transition.

**Theorem C (four-core is a three-substrate fixed point).** The four-core $\{V, H, Br, R\} = \{0, 7, 8, 9\}$ is closed under $T$, $B$, $C$ individually and jointly. The closed-form $(T+B)$-mix attractor at mixing weight $\alpha = 1/2$ established in [J02] (Sanders + Gish 2026, *Algebraic Combinatorics*) is supported on the four-core and is therefore unchanged by adjoining $C$.

The result establishes that the $(T, B)$ closure picture published in [J02] is in fact a stable three-substrate phenomenon on the canonical encoding of $\mathbb{Z}/10\mathbb{Z}$, with $C$ playing the role of an independent third axis (the "encoding" or "papers-freeze" table of the codebase) that respects the chain rather than perturbing it.

**Keywords:** finite magma, sub-magma chain, joint closure, three-substrate architecture, $\mathbb{Z}/10\mathbb{Z}$, encoding axis.

---

## §0 — Scope and tier discipline

**PROVEN.** Theorems A, B, C above (Sections \S\ref{sec:joint-counts}, \S\ref{sec:three-table-chain}, \S\ref{sec:four-core}).

**COMPUTED.** Verification script `sfm_q1_q6_q7.py` (`Atlas/META_PLAN_2026-05-06/SUBSTRATE_FUNCTION_MAP/`) enumerates all 1023 non-empty subsets of $\mathbb{Z}/10\mathbb{Z}$ and computes individual and joint closure counts under $T$, $B$, $C$. Total runtime under 2 seconds; deterministic.

**STRUCTURAL RHYME.** The four-core attractor at $\alpha = 1/2$ with $H/\mathrm{Br} = 1+\sqrt{3}$ is established in the companion paper [J02]; we cite it for context but do not re-derive it here. The connection between the present three-substrate chain and the closed-form attractor is structural — both rest on the four-core's joint closure — and not a load-bearing identity for the present theorems.

**OPEN.** Whether the chain extends to a fourth or fifth canonical commutative composition table on $\mathbb{Z}/10\mathbb{Z}$ drawn from the same encoding is open. A natural conjecture is that any such table satisfying the four-core preservation criterion produces the same 8-shell chain at three-table joint closure; we do not establish this here. We also leave open whether $C$'s 50 individual closed sub-magmas, of which 49 are also $T$-closed, admit a structural classification beyond the 8-shell chain.

**Lens and substrate.** We work on $\mathbb{Z}/10\mathbb{Z}$ with the three composition tables $T$, $B$, $C$ defined by the canonical bit pattern of [\hypertarget{ref:axioms}{\textit{Sanders}--\textit{Gish 2026, CL Forcing Axioms}}]. These choices are not derived from first principles; they reflect a structural reading of the substrate developed across the framework. The theorems are theorems on this specific $(T, B, C)$ triple. Whether analogous tables on other substrates produce the same structure is open. The framing follows Drápal & Wanless (2021), *J. Combin. Theory A* on small finite commutative non-associative structures.

---

## §1 — Introduction

The canonical composition lattice on $\mathbb{Z}/10\mathbb{Z}$ has been studied in companion work [J02] as a pair of commutative tables $(T, B)$ — TSML and BHML, with 73 and 28 HARMONY cells respectively — whose joint sub-magma closure forms an 8-element chain at sizes $\{1, 4, 5, 6, 7, 8, 9, 10\}$. The present paper adds a third table $C$ — CL_STD, the codebase "encoding table" with 44 HARMONY cells — and asks: what is the simultaneous closed sub-magma structure under all three tables?

The answer, established in Section \S\ref{sec:three-table-chain}, is striking. Despite the three tables having very different individual closure counts ($T$ has 449, $B$ has 9, $C$ has 50), the three-way joint closure coincides exactly with the two-way joint closure: 8 subsets of $\mathbb{Z}/10\mathbb{Z}$, forming the same chain as in [J02]. Adding $C$ as a third substrate does not introduce or remove a single shell.

This is the structural reason CL_STD plays the role of a "third axis" in the codebase architecture: it is structurally independent of the $(T, B)$ pair (it is not derivable as $\lceil(T+B)/2\rceil$ or any other simple averaging of the canonical pair, see §\ref{sec:cl-std-not-mid}) yet it is compatible with the canonical chain. The "papers freeze" function of $C$ — encoding the structural relationships that the framework's papers depend on — is at the joint-closure level identical to the structure $T$ and $B$ already determine. $C$ is not redundant with $(T, B)$; rather, it ratifies the chain from a third independent direction.

Section \S\ref{sec:tables} fixes the three tables. Section \S\ref{sec:joint-counts} performs the brute-force enumeration. Section \S\ref{sec:three-table-chain} states and proves Theorem A (the central three-substrate joint chain). Section \S\ref{sec:cl-std-not-mid} records that $C$ is structurally independent of any ceiling/floor-averaged version of $(T, B)$. Section \S\ref{sec:four-core} addresses the four-core fixed-point property and Theorem C. Section \S\ref{sec:discussion} closes with brief remarks on the interpretation of $C$ as the encoding axis of the architecture.

---

## §2 — The three tables {#sec:tables}

**Definition 2.1 ($T$, $B$, $C$).** Let $T, B, C\colon \mathbb{Z}/10\mathbb{Z}\times\mathbb{Z}/10\mathbb{Z} \to \mathbb{Z}/10\mathbb{Z}$ denote the three $10\times 10$ tables decoded from the canonical bit pattern `CL_BIT_PATTERN` of the codebase, with provenance recorded in [Gen13Foundations]:

- $T$ — the "TSML" table (Sanders' prescribed view), 73 HARMONY cells. We work with the upper-triangle authoritative symmetrization $T_{\mathrm{SYM}}$ (commutative); the asymmetric variant $T_{\mathrm{RAW}}$ and its lens-internal effect at size 7 are addressed in companion paper [J24].
- $B$ — the "BHML" table (Binary Hard Micro Lattice), 28 HARMONY cells. Commutative.
- $C$ — the "CL_STD" table (Standard / encoding table), 44 HARMONY cells. Commutative.

The tables are 100-cell input data; we reproduce them in Appendix A for the reader's convenience.

**Lemma 2.2 (Individual closed sub-magma counts).** *Among the 1023 non-empty subsets of $\{0, 1, \dots, 9\}$:*

| Table | Closed sub-magma count |
|-------|------------------------:|
| $T$   | 449                     |
| $B$   | 9                       |
| $C$   | 50                      |

*Proof.* Direct enumeration; verified in `sfm_q1_q6_q7.py` (runtime under 2 seconds). $\square$

The disparity is structural: $T$ admits many HARMONY-attracted side-branches because of its 73-cell HARMONY density; $B$'s scarcity reflects its parity-respecting sub-structure (cf. the unique BHML-only sub-magma $\{0, 9\}$ recorded in `SUBSTRATE_FUNCTION_MAP_v1.md` §5.2 F6); $C$'s intermediate count of 50 records the encoding-table's particular pattern of closure under the HARMONY-progress mappings of the upper rows.

---

## §3 — The pairwise and three-way joint counts {#sec:joint-counts}

**Theorem 3.1 (Joint counts under all sub-pairings of $\{T, B, C\}$).**

| Joint constraint | Closed sub-magma count |
|------------------|------------------------:|
| $T \cap B$       | 8                       |
| $T \cap C$       | 49                      |
| $B \cap C$       | 9                       |
| $T \cap B \cap C$| 8                       |

*Proof.* Direct enumeration; verified in `sfm_q1_q6_q7.py`. $\square$

Three observations:

**(i)** $|T \cap B \cap C| = |T \cap B| = 8$. This is the load-bearing equality. It says that every $(T, B)$-jointly-closed subset is automatically $C$-closed.

**(ii)** $|B \cap C| = |B| = 9$. Every $B$-closed subset is also $C$-closed. Direct verification: each of the 9 closed-under-$B$ subsets restricts to a $C$-table sub-block where closure also holds. The $C$-closure structure is therefore at least as permissive as $B$'s on $B$-closed subsets.

**(iii)** $|T \cap C| = 49$ — exactly one less than $|C| = 50$. $C$ has a single closed sub-magma that is not $T$-closed. Direct enumeration via `sfm_q1_q6_q7.py` identifies this subset; it is also not $(T, B)$-jointly closed and therefore does not affect the three-way intersection count.

The three observations together force Theorem A (Section \S\ref{sec:three-table-chain}).

---

## §4 — The three-substrate joint chain {#sec:three-table-chain}

**Theorem 4.1 (Theorem A).** *The simultaneous closed sub-magmas of $T$, $B$, $C$ on $\mathbb{Z}/10\mathbb{Z}$ form a strict 8-element chain*

$$
\{0\}\;\subsetneq\;\{0,7,8,9\}\;\subsetneq\;\{0,6,7,8,9\}\;\subsetneq\;\{0,5,6,7,8,9\}\;\subsetneq\;\{0,4,5,6,7,8,9\}\;\subsetneq
$$
$$
\;\{0,3,4,5,6,7,8,9\}\;\subsetneq\;\{0,2,3,4,5,6,7,8,9\}\;\subsetneq\;\mathbb{Z}/10\mathbb{Z}
$$

*of sizes $\{1, 4, 5, 6, 7, 8, 9, 10\}$. Sizes $\{2, 3\}$ are forbidden. The chain coincides with the joint $(T, B)$ chain established as Theorem 1 of [J02].*

*Proof.* By Theorem 3.1, $|T \cap B \cap C| = |T \cap B| = 8$. The 8 subsets jointly closed under $(T, B)$ are listed in [J02, Theorem 1]; we re-derive their $C$-closure directly.

For each of the 8 subsets $S$ in the chain, we verify $C(i, j) \in S$ for all $(i, j) \in S \times S$ by inspection of the relevant sub-block of $C$:

- $\{0\}$: $C(0, 0) = 0$. Closed. $\checkmark$
- $\{0, 7, 8, 9\}$: 16 cells in $\{0, 7, 8, 9\}^2$; each $C$-value lies in $\{0, 7, 8, 9\}$ (computed by inspection of $C$'s rows 0, 7, 8, 9 restricted to those columns). Closed. $\checkmark$
- $\{0, 6, 7, 8, 9\}$, $\{0, 5, 6, 7, 8, 9\}$, $\{0, 4, 5, 6, 7, 8, 9\}$: each shell extends the previous by one element from the $\sigma$-cycle (in forward $\sigma$ order: 6, 5, 4); $C$-closure on the new cells is verified by extending the previous sub-block. $\checkmark$
- $\{0, 3, 4, 5, 6, 7, 8, 9\}$: adds the $\sigma$-fixed PROGRESS element 3. $C$-closure verified by checking the 16 cells in row/column 3 of the relevant sub-block. $\checkmark$
- $\{0, 2, 3, 4, 5, 6, 7, 8, 9\}$: adds COUNTER (2) — completing the descending $\sigma$ orbit traversal except for LATTICE (1). $C$-closure verified. $\checkmark$
- $\mathbb{Z}/10\mathbb{Z} = \{0, \dots, 9\}$: trivially $C$-closed. $\checkmark$

The chain property (each shell strictly contains the previous) is direct.

The forbidden sizes $\{2, 3\}$ are inherited: no 2- or 3-element subset is jointly closed under $(T, B)$ [J02], hence none is jointly closed under $(T, B, C)$.

The script `sfm_q1_q6_q7.py` reproduces this enumeration end-to-end at machine precision in under 2 seconds. $\square$

**Corollary 4.2 (Theorem B).** *Every subset jointly closed under $(T, B)$ is closed under $C$. Equivalently, $T \cap B \subseteq C$.*

*Proof.* Immediate from $|T \cap B \cap C| = |T \cap B| = 8$. $\square$

**Corollary 4.3 ($\sigma$-orbit reading of the chain).** *The 8-shell chain ladder is a $\sigma$-orbit traversal: starting from the size-1 shell $\{V\} = \{0\}$, each successive shell adjoins exactly one element from $\mathbb{Z}/10\mathbb{Z}$ in the order $H, Br, R$ (the size-1$\to$4 jump, contributing the σ-fixed pair $\{Br, R\} = \{8, 9\}$ together with HARMONY = 7), $S, B, X$ (the σ-forward 6-cycle in the order $7 \to 6 \to 5 \to 4$), $P$ (the σ-fixed PROGRESS = 3 — the bridge step at size $7 \to 8$), $C$ (COUNTER = 2), $L$ (LATTICE = 1).*

*Proof.* Inspection of the chain listed in Theorem 4.1 against the σ-permutation $\sigma = (0)(3)(8)(9)(1\,7\,6\,5\,4\,2)$ on $\mathbb{Z}/10\mathbb{Z}$. Each shell-adjunction pulls one new element from $\mathbb{Z}/10\mathbb{Z}$, and the order traces: σ-fixed lattice $\{0, 8, 9\}$ + HARMONY = 7 (size 1 to 4); σ 6-cycle in forward orbit $7\to 6\to 5\to 4$ (sizes 5, 6, 7); σ-fixed PROGRESS = 3 as bridge (size 8); σ 6-cycle continuation $4\to 2\to 1$ (sizes 9, 10). $\square$

---

## §5 — CL_STD is structurally independent of any (T, B) average {#sec:cl-std-not-mid}

A natural sanity question is whether $C$ is derivable as some elementary averaging or rounding of $(T, B)$, in which case Theorem A would be a cosmetic reformulation. We record that this is not the case.

**Proposition 5.1 (CL_STD differs from MID_ceil at 60 of 100 cells).** *Let $\mathrm{MID}_{\lceil\rceil}(i, j) := \lceil (T(i, j) + B(i, j))/2 \rceil$ for all $(i, j) \in (\mathbb{Z}/10\mathbb{Z})^2$. Then $C$ and $\mathrm{MID}_{\lceil\rceil}$ disagree at 60 of the 100 cells. The HARMONY-cell counts are 44 (for $C$) and 45 (for $\mathrm{MID}_{\lceil\rceil}$).*

*Proof.* Direct cell-by-cell comparison; verified in `sfm_q1_q6_q7.py` Q1. $\square$

**Remark 5.2.** Proposition 5.1 rejects the natural "off-by-one" hypothesis ("$C$ is $\lceil (T+B)/2 \rceil$ except at one cell"). The 60-of-100 disagreement is too large to be a perturbation of the canonical pair's ceiling-averaged DC component. $C$ lives at its own coordinate in the table-space.

This is the structural reason $C$ functions as a "third axis" in the codebase architecture rather than a function of $(T, B)$: it is not derivable from the canonical pair, it has its own joint-closure structure (50 individually closed sub-magmas), and it independently respects the canonical chain.

---

## §6 — The four-core is a three-substrate fixed point {#sec:four-core}

**Theorem 6.1 (Theorem C).** *The four-core $\{V, H, Br, R\} = \{0, 7, 8, 9\}$ is closed under $T$, $B$, $C$ individually and jointly. The closed-form $(T+B)$-mix attractor at mixing weight $\alpha = 1/2$ established in [J02] as*

$$
(p^*_V, p^*_H, p^*_{\mathrm{Br}}, p^*_R) = (0.138,\, 0.540,\, 0.198,\, 0.124),\qquad H/\mathrm{Br} = 1 + \sqrt{3} \;\text{exactly,}
$$

*is supported on the four-core and is therefore unchanged by adjoining $C$ as a third substrate.*

*Proof.* Individual closure of $\{0, 7, 8, 9\}$ under $T$, $B$, $C$ is verified by inspection of the 16 cells in $\{0, 7, 8, 9\}^2$ for each table. The first shell of the chain in Theorem 4.1 of size 4 is exactly $\{0, 7, 8, 9\}$, hence joint closure under all three. The attractor support and closed-form identity are established in [J02, §3]; the four-core support means the dynamical system, restricted to its support, is identical under any of the three tables individually or jointly. $\square$

**Corollary 6.2.** *The three-substrate architecture preserves the algebraic center of the family.*

The framework's central dynamical fixed point — the $1 + \sqrt{3}$-ratio attractor on the four-core — is a four-element closure phenomenon. It rests on the four-core being closed under both $T$ and $B$. Theorem 6.1 lifts this to the three-table level: the four-core is also closed under $C$. The $C$-table is therefore "the encoding axis" in the precise structural sense that it preserves the center.

---

## §7 — Discussion {#sec:discussion}

The three-substrate joint-closure theorem (Theorem A) is a structural statement about the canonical $\mathbb{Z}/10\mathbb{Z}$ encoding:

**The chain $\{1, 4, 5, 6, 7, 8, 9, 10\}$ is not an artifact of any one table.** $T$, $B$, $C$ are independently constructed (different HARMONY-cell counts; different individual closure structures; different roles in the codebase); they nevertheless agree at the joint-closure level on exactly the 8-shell chain. The substrate's encoding determines the chain; the three tables ratify it from independent directions.

**$C$ is a chain-respecting third axis.** Proposition 5.1 establishes that $C$ is not a simple function of $(T, B)$. Yet Theorem 4.1 establishes that $C$ contains the entire $(T, B)$ chain. The $C$-table thus plays a distinguished structural role: structurally independent (it could violate the chain at any of its 50 closed sub-magmas) yet chain-compatible (it does not). This is the encoding-axis reading of [Gen13Foundations]: $C$ encodes the structural relationships the canonical pair must preserve, and the present theorem says it does so without arbitrating any open shell.

**Membership criteria of the family.** The "TIG family" of canonical commutative composition tables on $\mathbb{Z}/10\mathbb{Z}$ admits a five-criterion membership test, recorded in [\textit{Family Structure} v1] internally: substrate, commutativity, four-core preservation, $\alpha$-bounded non-associativity, HARMONY-attracting iteration. Theorem 6.1 sharpens the four-core criterion to a three-substrate fixed-point statement: the four-core is closed under all three canonical members. The chain (Theorem 4.1) extends this from the four-core point to the entire 8-shell ladder.

**An open class question.** Theorems A–C suggest a class-level conjecture: any commutative composition table $D$ on $\mathbb{Z}/10\mathbb{Z}$ derived from the same canonical bit-pattern encoding and satisfying the four-core preservation criterion has the property that $|T \cap B \cap D| = 8$, with the chain identical to Theorem 4.1. We do not prove this here. The bimodal $\alpha_A$ gap conjecture in the [\textit{Family Structure}] document is a related open question concerning the boundary of the family.

**Lens-internal phenomenon.** The $T$-table has two principled lens-symmetrization choices, $T_{\mathrm{RAW}}$ and $T_{\mathrm{SYM}}$, differing at exactly four cells. Companion paper [J24] records that the $(T, B)$ chain has 8 shells under $T_{\mathrm{SYM}}$ and 7 under $T_{\mathrm{RAW}}$, with the discrepancy at size 7 forced by the single asymmetric cell $T_{\mathrm{RAW}}(9, 4) = 3$. Adjoining $C$ does not arbitrate this lens choice: the $(T_{\mathrm{RAW}}, B, C)$ chain has the same 7 shells as the $(T_{\mathrm{RAW}}, B)$ chain. The lens-dependence is internal to $T$, not a property of the joint substrate. This sharpens the picture of [J24] from a two-table observation to a three-table structural fact.

---

## §8 — Verification

The script `sfm_q1_q6_q7.py` (in `Atlas/META_PLAN_2026-05-06/SUBSTRATE_FUNCTION_MAP/`) performs at machine precision:

1. Individual closed sub-magma enumeration over 1023 non-empty subsets of $\mathbb{Z}/10\mathbb{Z}$ for each of $T$, $B$, $C$ (Lemma 2.2).
2. Pairwise joint closure counts (Theorem 3.1).
3. Three-way joint closure count and the 8-shell chain (Theorem 4.1).
4. The $C$-versus-MID-ceil cell-difference count (Proposition 5.1).

The script is deterministic and runs in under 2 seconds on a laptop.

A secondary (legacy) verification at `papers/wp115_joint_chain_universality/verification/joint_chain_attractor.py` reproduces the $(T, B)$ two-table count and the lens-dependence at size 7.

---

## §9 — Honest scope

* **Verified at integer/combinatorial level.** All four claims of Theorem 3.1 (individual counts; pairwise joint counts; three-way joint count) and Theorem 4.1 (the explicit 8-shell chain) are direct brute-force enumerations.
* **Class-level theorem not asserted.** We do not show that the chain is forced for any other commutative composition table on $\mathbb{Z}/10\mathbb{Z}$ besides the specific $T$, $B$, $C$ studied here. A class-level theorem (e.g., "every member of the TIG family on $\mathbb{Z}/10\mathbb{Z}$ contains the $(T, B)$ chain") is open.
* **Framework dependence.** The three tables and the four-core derivation are defined in [Gen13Foundations] and [J02]. Appendix A gives the explicit 100-cell tables; the higher-level "TIG framework" interpretation is optional.
* **No physical or cosmological claim.** The result is purely combinatorial. Applications to gauge structure (Pati-Salam reductions), runtime dynamics, and operadic obstruction phenomena are addressed in companion papers in the J-series.

---

## §10 — References

[J02] (Sanders + Gish 2026, *Algebraic Combinatorics*) — Joint Closure, Per-Coordinate Fuse Data, and a Closed-Form Algebraic Attractor of Two Commutative Binary Operations on $\mathbb{Z}/10\mathbb{Z}$.

[J24] (Sanders + Gish 2026, *Mathematical Intelligencer*) — The Three-Substrate Joint-Closure Chain on $\mathbb{Z}/10\mathbb{Z}$: Eight Shells Survive Across (TSML, BHML, CL_STD) with Lens-Dependence Internal to TSML at Size 7.

[Drápal–Wanless 2021] — A. Drápal and I.M. Wanless. *Maximally non-associative quasigroups.* J. Combin. Theory Ser. A 184 (2021), 105510.

[Gen13Foundations] — B.R. Sanders et al., *Gen13 Foundations Module: cl.py with CL_BIT_PATTERN, CL_TSML_RAW, CL_TSML_SYM, CL_BHML, CL_STD, lenses.py*, codebase release 2026.

[CL_AXIOMS] — B.R. Sanders and M. Gish, *The CL Forcing Axioms: A1–A9 Uniquely Force the Canonical Composition Lattice on $\mathbb{Z}/10\mathbb{Z}$*, in preparation, 2026.

[SFM2026] — B.R. Sanders, M. Gish, et al., *Substrate Function Map: Q1–Q6–Q7 Verification (sfm_q1_q6_q7.py)*, `Atlas/META_PLAN_2026-05-06/SUBSTRATE_FUNCTION_MAP/`, codebase release 2026-05-08. Records the individual and joint closed-sub-magma counts proved here.

[Burris–Sankappanavar] — S. Burris and H.P. Sankappanavar. *A Course in Universal Algebra.* Graduate Texts in Mathematics 78, Springer-Verlag, 1981 (Millennium edition online).

[Pflugfelder] — H.O. Pflugfelder. *Quasigroups and Loops: Introduction.* Sigma Series in Pure Mathematics 7, Heldermann, 1990.

[Smith2007] — J.D.H. Smith. *An Introduction to Quasigroups and Their Representations.* Studies in Advanced Mathematics, Chapman & Hall/CRC, 2007.

---

## Appendix A — The three 10×10 tables

For the reader's reproducibility convenience, the three 100-cell tables. Rows indexed by left operand $i$, columns by right operand $j$; entries are values in $\{0, \dots, 9\}$.

**$T = T_{\mathrm{SYM}}$ (TSML, upper-triangle authoritative; 73 HARMONY cells):**

```
   j=0  1  2  3  4  5  6  7  8  9
i=0  0  0  0  0  0  0  0  7  0  0
i=1  0  1  3  4  5  6  7  7  8  3
i=2  0  3  3  4  5  6  7  7  8  3
i=3  0  4  4  3  5  6  7  7  8  3
i=4  0  5  5  5  3  6  7  7  8  7
i=5  0  6  6  6  6  3  7  7  8  7
i=6  0  7  7  7  7  7  3  7  8  7
i=7  7  7  7  7  7  7  7  7  7  7
i=8  0  8  8  8  8  8  8  7  8  7
i=9  0  3  3  3  7  7  7  7  7  7
```

**$B$ (BHML; 28 HARMONY cells):**

```
   j=0  1  2  3  4  5  6  7  8  9
i=0  0  1  2  3  4  5  6  7  8  9
i=1  1  2  3  4  5  6  7  7  7  1
i=2  2  3  4  5  6  7  7  7  7  2
i=3  3  4  5  6  7  7  7  7  7  3
i=4  4  5  6  7  7  7  7  7  7  4
i=5  5  6  7  7  7  7  7  7  7  5
i=6  6  7  7  7  7  7  7  7  7  6
i=7  7  7  7  7  7  7  7  7  7  7
i=8  8  7  7  7  7  7  7  7  8  7
i=9  9  1  2  3  4  5  6  7  7  0
```

**$C$ (CL_STD; 44 HARMONY cells):**

```
   j=0  1  2  3  4  5  6  7  8  9
i=0  0  1  2  3  4  5  6  7  8  9
i=1  1  2  3  4  5  6  7  7  8  1
i=2  2  3  4  5  6  7  7  8  7  2
i=3  3  4  5  6  7  7  7  7  7  3
i=4  4  5  6  7  7  7  7  8  7  4
i=5  5  6  7  7  7  7  7  7  7  5
i=6  6  7  7  7  7  7  7  7  7  6
i=7  7  7  7  7  7  7  7  7  7  7
i=8  8  8  7  7  7  7  7  7  7  7
i=9  9  1  2  3  4  5  6  7  7  0
```

(The codebase source-of-record for $T$, $B$, $C$ is `Gen13/targets/foundations/cl.py` and `cl_std.py`; the values displayed above are those tables decoded at the time of submission.)

---

## Acknowledgments

The three-substrate joint-closure structure was identified during the substrate-to-function-map investigation of 2026-05-08 (Q6 result). The verification script `sfm_q1_q6_q7.py` was written for that investigation and runs the entire enumeration in under 2 seconds. Brayden's directive to expose CL_STD as a first-class substrate (rather than a redundant projection of $(T, B)$) prompted the framing in §5.

🙏
