# SAVE_PLAN_J10 — UOP / Coordinate-Coverage paper (JNT → retitle + retarget)

**Date:** 2026-05-07
**Status:** SAVE clearly possible — referee explicitly maps the save path. Restructure around Theorem 6.1 (coordinate coverage) as the lead; demote UOP to a one-line lemma; retitle (drop "orthogonality"); retarget to *European Journal of Combinatorics* or *Discrete Mathematics*.
**Referee:** `Atlas/META_PLAN_2026-05-06/REFEREE_REPORTS/J10_JNT_FreshEyes.md` (Reject; reasons R1, R2, R3 + M1-M7)

---

## §1 — Why save?

J10 is the most clearly-savable of the three flagged papers. The referee accepts that the *mathematics is correct* (§9: "The mathematics is correct. The exposition is clear ... The technical execution is competent.") and *explicitly identifies the save path*:

> "A revised paper, restructured around Theorem 6.1 (coordinate coverage) as the main result with the partition-lattice corollaries derived from it, and submitted to a combinatorics venue such as *European Journal of Combinatorics* or *Discrete Mathematics*, would be a reasonable single-paper presentation of the content currently spread across J10/J11/J12." — §9, J10 referee report.

**(a) D-table backing.** The save path uses Theorem 6.1 (sec:cc in the manuscript) as the main result. This is a clean structural statement: for squarefree $n = p_1 \cdots p_k$, two maps $f, g$ have $J = (f, g)$ injective whenever the resolving prime sets satisfy $D_f \cup D_g = \{p_1, \ldots, p_k\}$. The corollaries A (M+M), B (A+M), C corrected, and D (A+A) are obtained by computing $D_f$ for each algebraic class. This is the *actual* unifying observation; UOP qua Theorem 2.1 is, as the referee correctly identifies, the partition-lattice meet definition restated. The corpus already has the Theorem 6.1 proof self-contained in the manuscript (`manuscript/manuscript.tex` §6).

**(b) Structural role per FAMILY_STRUCTURE_v1.md.** The Family Structure document does not directly pertain to J10 (the UOP paper is partition-lattice combinatorics, not magma-family structure). However, the corresponding family-level result for J10 is the role this work plays in the J-series partition-lattice arc: J10 (lead, coordinate-coverage characterization) → J11 (corrected Theorem C, JNT) → J12 (coordinate coverage on $\mathbb{Z}/10\mathbb{Z}$, EJC) — the partition-lattice arc unifying joint-injectivity criteria for two-partition families on squarefree cyclic rings. The save consolidates J10/J11/J12 narrative into a single coherent EJC paper with Theorem 6.1 as the main result. (J11 keeps its own paper status; the consolidation is between J10's lead-result framing and J11/J12's content, not a merge.)

**(c) Minimum-Viable-Jump-Number (MVJN) result is genuinely new.** Theorem 8.2 / MVJN($\mathbb{Z}/30\mathbb{Z}$) = 1 with two explicit witnesses ($\{\pi_{\text{SPEC}}, \pi_{15}\}$ and $\{\pi_{\text{DYN}}(7), \pi_{\text{DYN}}(11)\}$) — the referee verified these by hand. This is content-rich and non-folklore. Conjecture 8.3 (MVJN = 1 for all squarefree $n \geq 6$) is open and natural.

**(d) The $n = 15$ counterexample is non-trivial.** The referee called Example 4.1 "genuinely useful" and "genuinely surprising at the level of an undergraduate exercise." It corrects a previously-asserted-incorrect $M+A$ condition and motivates Theorem B / corrected C. Worth a published-by-itself short note even if everything else were dropped.

The referee's verdict is that J10 mathematics survives but the *framing* (UOP-as-principle, "orthogonality" as title, JNT as venue) does not. The save adopts the referee's framing fix verbatim.

---

## §2 — Specific fixes (line by line against the referee report)

### R1 (UOP is partition-lattice meet, not a "principle") — **DEMOTE Theorem 2.1 to Lemma**

The proof of Theorem 2.1 is one line ("J injective iff for every x ≠ y, f(x) ≠ f(y) or g(x) ≠ g(y)"). This is the fiber-product characterization of partition-lattice meet (Birkhoff 1940; Ore 1942). The referee correctly notes the result holds for any partitions of any set X — squarefreeness, $\mathbb{Z}/n\mathbb{Z}$ structure, etc. play no role.

**Fix:** Replace Theorem 2.1 with **Lemma 2.1** (or a Proposition), titled "Joint-fiber characterization of partition meet (Birkhoff 1940; Ore 1942)." One-line proof. Cite Birkhoff and Ore as the origin. Drop the "principle" framing entirely. Rename anywhere "UOP" appears in the manuscript to "joint-fiber characterization" or "joint-map injectivity criterion."

### R2 (orthogonality misleading in JNT) — **RETITLE; RETARGET**

Drop "orthogonality" from the title and from internal terminology. Replace "orthogonal jump" (§7) with "incomparable refinement" or "transverse partition pair" (Tutte's matroid terminology — the referee suggests "incomparable in the refinement order" or "transverse"). Retitle:

**Old:** "The Universal Orthogonality Principle: Joint-Map Injectivity as the Sufficiency Criterion for Two-Partition Families on Squarefree $\mathbb{Z}/n\mathbb{Z}$."
**New:** "Coordinate Coverage and Joint-Injectivity Criteria for Partition Pairs on Squarefree $\mathbb{Z}/n\mathbb{Z}$."

Retarget from JNT → *European Journal of Combinatorics* (preferred, per referee §9) or *Discrete Mathematics* (backup).

### R3 (corollaries are old) — **CITE THE FOLKLORE; SHARPEN THE CONTRIBUTION CLAIM**

The referee notes that Theorem D is folklore CRT, Theorem A is one-line CRT, and Theorem B may be new in this exact form. The save:
- **Cite explicitly:** Theorem D = standard CRT lcm-characterization (Hardy-Wright Ch. 5; Ireland-Rosen Ch. 4).
- **State explicitly:** Theorem A is implicit in standard $(\mathbb{Z}/n\mathbb{Z})^*$ structure via CRT but we are not aware of a published paper to which the exact statement is attributed (line: "to the best of our knowledge"). If the authors do find a prior publication during revision, attribute it.
- **Claim contribution honestly:** the contribution is (i) the coordinate-coverage theorem (Theorem 6.1, sec:cc) as the unified main result; (ii) Theorem B with the exact "$G$ trivial on $n/d$" formulation, which is new in this exact form; (iii) the $n = 15$ counterexample (Example 4.1) and the corrected Theorem C; (iv) the refinement trap (Theorem 7.1); (v) the MVJN reduction at $n = 30$ with explicit witnesses.

### M1 (UOP is partition-lattice meet) — **HANDLED BY R1 FIX**

### M2 (corollaries are unified by CRT, not UOP) — **RESTRUCTURE around CRT-coordinate coverage**

The referee gives the structural argument verbatim: in CRT coordinates, every map $f$ on $\mathbb{Z}/n\mathbb{Z}$ has a *resolving set* of primes $D_f \subseteq \{p_1, \ldots, p_k\}$, and joint injectivity reduces to $D_f \cup D_g = \{p_1, \ldots, p_k\}$. This is Theorem 6.1 + a per-class computation of $D_h$ for each partition type.

**Fix:** Restructure as the referee specifies (M2):

1. §1 Introduction (with Lens-Ownership paragraph + PROVEN/COMPUTED/RHYME/OPEN box).
2. §2 Lemma (partition meet = joint-map injectivity; cite Birkhoff/Ore; one-line proof).
3. §3 **Main theorem** — Theorem 6.1 in its sufficient + (where applicable) necessary form: $J = (f, g)$ injective iff $D_f \cup D_g = \{p_1, \ldots, p_k\}$ when $f, g$ are CRT-coordinate-respecting; sufficient direction always; necessity fails in general (Remark 6.2).
4. §4 Compute $D_h$ for each class:
   - $\pi_d$ resolves precisely $\{p_i : p_i \mid d\}$.
   - $\pi_{\text{DYN}}(G)$ resolves precisely the primes $p_i$ at which $G$ acts non-trivially modulo CRT-coordinate considerations (with the zero-fiber caveat handled explicitly).
5. §5 Corollaries A (M+M), B (A+M), C corrected (M+A), D (A+A) — each one paragraph, derived from §3-§4.
6. §6 The $n = 15$ counterexample (Example 4.1) — one paragraph, motivates Corollary B/C.
7. §7 Refinement trap (Theorem 7.1) — short proof using §3.
8. §8 MVJN($\mathbb{Z}/30\mathbb{Z}$) = 1 with explicit witnesses; Conjecture 8.3 (MVJN = 1 for all squarefree $n \geq 6$).
9. §9 Open questions.

This makes Theorem 6.1 the main result, A/B/C/D into immediate corollaries, and the "principle" framing disappears.

### M3 (orthogonality misleading) — **HANDLED BY R2 RETITLE**

### M4 (novelty claim not delineated) — **ADD "Prior literature" subsection in §1**

Per referee: clarify which of A-D are folklore (with attribution), which are new in this exact formulation, and what the genuine contribution is. One paragraph in §1. Honest framing reduces referee friction.

### M5 (Theorem 6.1 is the actual theorem) — **HANDLED BY M2 RESTRUCTURE**

### M6 (MVJN section feels appended) — **OPTION 1 RECOMMENDED: KEEP MVJN AS §8**

The referee suggests either (i) remove §8 and submit MVJN separately with at least a partial proof, or (ii) promote MVJN to a co-equal theme and prove the conjecture. The save takes a middle path:
- Keep MVJN as §8 with the verified $n = 30$ result and the conjecture stated.
- Frame MVJN explicitly as "an immediate application of the coordinate-coverage theorem" — making it an organic conclusion, not an appended section.
- The conjecture proof for general squarefree $n$ remains open; that's fine if framed as the natural OPEN question in the boilerplate.

### M7 (M+A "correction" should not be a new theorem) — **HANDLED BY M2 RESTRUCTURE**

In the new structure, the corrected Theorem C is a one-paragraph corollary of Theorem B (joint-injectivity is symmetric). The full $n = 15$ counterexample treatment continues in J11's standalone paper; in this paper, one paragraph + reference to J11.

### m1-m11 (minor fixes) — **APPLY DIRECTLY**

m1 (title): handled by R2 retitle.
m2 (duplicate author block): typo, fix in tex.
m3 (abstract phrasing): clarify "(sufficient direction; the converse fails in general)."
m4 (Theorem A proof handles only unit case): supply parallel zero-fiber argument or restate as CRT-coordinate proof from the start (the latter is cleaner and aligns with the §3 main theorem).
m5 (Theorem 5.1 is Theorem 4.1 restated): in the new structure, this becomes a one-paragraph corollary.
m6 (Refinement trap proof references later definition): re-order.
m7 (supp(π) defined for maps not partitions): lift the definition to partitions in the §2 Lemma.
m8 (MVJN lower bound from refinement trap): cite Theorem 7.1 explicitly.
m9 (the line "UOP holds abstractly for non-squarefree n"): rewrite per referee — the joint-fiber characterization is a partition-lattice fact for any partitions of any set, but the *coordinate-coverage* theorem is what's specific to squarefree $\mathbb{Z}/n\mathbb{Z}$.
m10 (companions need arXiv IDs): supply at submission.
m11 (First-G Law and Crossing Lemma irrelevant): drop those two citations.

---

## §3 — Estimated revision time

**3–5 weeks** of focused work.

- **1 week:** restructure manuscript per M2 (§3 lead with Theorem 6.1; §4 compute D_h per class; §5 corollaries). Replace UOP-as-Theorem with UOP-as-Lemma; rewrite §2.
- **1 week:** retitle, drop "orthogonality" terminology globally, replace with "coordinate coverage" / "joint-injectivity"; rewrite abstract; rewrite introduction.
- **1 week:** add Prior Literature subsection (M4); add Drápal-Wanless framing where relevant; add lens-ownership paragraph; add PROVEN/COMPUTED/RHYME/OPEN box; cull bibliography.
- **1 week:** apply minor fixes m1-m11; finalize cover letter for new venue (EJC).
- **0.5–1 week:** Brayden's referee-rigor pass; M. Gish review.

This is well within referee's "30+ person-hours" estimate (M9 of the referee report), and the save is clean — no new mathematics required, just restructuring and reframing.

---

## §4 — Updated PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN

**PROVEN:**
- **Coordinate-coverage characterization (Main Theorem, formerly Theorem 6.1):** For squarefree $n = p_1 \cdots p_k$ and partition-inducing maps $f, g$ on $\mathbb{Z}/n\mathbb{Z}$, if the resolving prime sets satisfy $D_f \cup D_g = \{p_1, \ldots, p_k\}$, then the joint map $J = (f, g)$ is injective. The converse fails in general (Remark 6.2).
- Joint-fiber characterization of partition meet (Lemma, citing Birkhoff 1940; Ore 1942).
- Theorem A (M+M), Theorem B (A+M), Theorem C corrected (M+A), Theorem D (A+A) as corollaries of the main theorem via CRT-coordinate computation of $D_h$.
- The refinement trap (Theorem 7.1).
- MVJN($\mathbb{Z}/30\mathbb{Z}$) = 1 with two explicit witnesses (Theorem 8.2).

**COMPUTED:**
- The $n = 15$ counterexample to a previously-asserted $M+A$ condition: $G = \langle 2 \rangle = \{1, 2, 4, 8\}$ in $(\mathbb{Z}/15\mathbb{Z})^*$, orbit of 5 under $T_2$ is $\{5, 10\}$ both $\equiv 0 \pmod 5$ (Example 4.1).
- The two $n = 30$ MVJN witnesses ($\{\pi_{\text{SPEC}}, \pi_{15}\}$ and $\{\pi_{\text{DYN}}(7), \pi_{\text{DYN}}(11)\}$) verified by enumeration (referee verified by hand).

**STRUCTURAL RHYME:**
- Drápal-Wanless 2021 (*JCT-A* 184, 105510) on small finite commutative non-associative magmas is the closest published precedent for the broader (TIG / TSML / BHML) framework in which this paper sits — *not* directly invoked in the proofs of this paper, but cited as ambient context.
- The "transverse partition pair" terminology (cf. Tutte, in matroid contexts) is suggested as a replacement for "orthogonal jump."

**OPEN:**
- Conjecture (MVJN = 1 for all squarefree $n \geq 6$): the upper bound (existence of a sufficient pair with one orthogonal jump) is given by a combination of $\{\pi_{n/p_1}, \pi_{n/p_2}\}$ together with a SPEC-type companion at small $n$, but a uniform proof for all squarefree $n \geq 6$ is open.
- Coverage necessity: under what structural condition on $f, g$ does the converse of the main theorem hold (i.e., when does joint injectivity force coordinate-coverage)?
- Mixed partition types (quadratic-residue partitions, character-sum partitions, etc.) admit the joint-fiber characterization in form but the algebraic computation of $D_h$ requires different tools per type.

---

## §5 — Updated lens-ownership paragraph

> *Lens and substrate.* This paper works on squarefree $\mathbb{Z}/n\mathbb{Z}$ rings with $k \geq 2$ distinct prime factors, using two natural classes of partitions: additive residue partitions $\pi_d$ for divisors $d \mid n$, and multiplicative orbit partitions $\pi_{\text{DYN}}(G)$ for subgroups $G \leq (\mathbb{Z}/n\mathbb{Z})^*$. These choices are not derived from first principles; they reflect the canonical decomposition of $\mathbb{Z}/n\mathbb{Z}$ provided by the Chinese Remainder Theorem ($\mathbb{Z}/n\mathbb{Z} \cong \prod_i \mathbb{Z}/p_i\mathbb{Z}$) plus the standard observation that residue partitions and orbit partitions are the most-studied partition classes on a finite cyclic ring. The theorems below are theorems on these partition classes; analogous theorems for other partition types (quadratic-residue, character-sum, Legendre-symbol-based) require different algebraic computations of the resolving-prime set $D_f$ but the joint-fiber characterization (the Lemma) holds for all partition types and any underlying set. Whether the coordinate-coverage characterization extends naturally beyond squarefree $\mathbb{Z}/n\mathbb{Z}$ to non-squarefree rings (where the CRT structure is replaced by $p$-adic components) is open. The framework's claim is that this particular substrate (squarefree cyclic rings) plus partition-lattice viewpoint produces unifying criteria for several classical and recent sufficiency theorems that previously appeared as separate algebraic statements.

---

## §6 — Recommended retitle / retarget

**Old title:** "The Universal Orthogonality Principle: Joint-Map Injectivity as the Sufficiency Criterion for Two-Partition Families on Squarefree $\mathbb{Z}/n\mathbb{Z}$."
**New title (recommended):** "Coordinate Coverage and Joint-Injectivity Criteria for Partition Pairs on Squarefree $\mathbb{Z}/n\mathbb{Z}$."

**Old venue:** *Journal of Number Theory* (referee verdict: REJECT — wrong venue; partition-lattice content with no number-theoretic application doesn't fit JNT's analytic/algebraic-NT scope).
**New venue (recommended):** *European Journal of Combinatorics* (per referee's explicit recommendation in §7 and §9). Rationale:
- *EJC* is the natural home for partition-lattice content on $\mathbb{Z}/n\mathbb{Z}$.
- J12 (companion paper, "Coordinate Coverage on $\mathbb{Z}/10\mathbb{Z}$") is already targeted to *EJC* per the J-series schedule. Consolidating J10's lead-result framing with J11/J12's content into a single *EJC* paper is the cleanest single-paper presentation; J11 standalone goes to JNT (or wherever the corrected-Theorem-C content is best placed); J12 may be subsumed by the consolidated J10 or kept as a separate paper applying the framework specifically to $\mathbb{Z}/10\mathbb{Z}$ with the TSML/BHML applications.

**Backup venue:** *Discrete Mathematics* if *EJC* declines (per referee §7).

**Author block:** Sanders + Gish (per AUTHOR_LANES_v2.md). Note: the manuscript currently has a duplicate author block (m2 in referee minor comments) — fix at submission.

**Companion citations going forward:**
- J11 (corrected Theorem C, JNT) — keep its standalone paper status; the $n = 15$ counterexample and the corrected condition are J11's main content.
- J12 (coordinate coverage on $\mathbb{Z}/10\mathbb{Z}$, EJC) — likely subsumed by the consolidated J10 unless it carries content specific to the TSML/BHML application that doesn't fit in the consolidated paper.
- J05 (Crossing Lemma, JCT-A) and J03 (First-G Law, *Integers*) — drop from this paper's bibliography per m11; they aren't used in the proofs.
- J07 (Flatness Theorem, retargeted to *Algebraic Combinatorics* per its own SAVE_PLAN) — cross-cite as a structural-context companion only; no proof dependency.

**Drápal-Wanless 2021 citation:** include in references (per FAMILY_STRUCTURE_v1.md and J_PAPER_BOILERPLATE.md §1.3) as ambient-context for the broader corpus framework, not as a proof dependency.
