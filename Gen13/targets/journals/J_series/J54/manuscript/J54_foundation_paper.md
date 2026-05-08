# Forcing Axioms and the Family of Commutative Non-Associative Magmas on $\mathbb{Z}/10\mathbb{Z}$ Preserving a Designated 4-Core

**Authors:** B.R. Sanders$^{1}$, M. Gish$^{2}$
$^{1}$7Site LLC, Hot Springs, AR — brayden@7site.co
$^{2}$Independent Researcher, Hot Springs, AR — monica.gish1992@gmail.com

**Target venue:** *Algebraic Combinatorics* (primary)
**MSC 2020:** 20N02 (sets with one binary operation), 17A35 (general non-associative algebras), 08A35 (universal algebra; concrete subuniverses, sub-magmas), 11C20 (matrices, determinants in number theory), 05E18 (group actions on combinatorial structures).

---

## §0 Lens, substrate, and tier discipline

This paper studies the family of finite commutative non-associative magmas on $\mathbb{Z}/10\mathbb{Z}$ that preserve a designated four-element subset $\mathcal{C} = \{0, 7, 8, 9\}$. The substrate $\mathbb{Z}/10\mathbb{Z}$ and the designated 4-core $\mathcal{C}$ are not derived from first principles; they are taken as the substrate-of-study, motivated by a ten-operator labelling of $\mathbb{Z}/10\mathbb{Z}$ at indices $0$ through $9$ inherited from the parent research framework (Sanders, *TIG framework*, 2026; see §6). The names of the operators are $\{V, L, C, P, X, B, S, H, Br, R\}$ (in the parent framework: VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE, BALANCE, CHAOS, HARMONY, BREATH, RESET). The designated 4-core is the parent framework's "4-core" $\{V, H, Br, R\}$ at indices $\{0, 7, 8, 9\}$. The names play no role in the proofs; they are used only for cross-referencing.

The framing follows the Drápal & Wanless (2021, *J. Combin. Theory Ser. A* **184**, 105510) line of work on small finite commutative non-associative structures. Drápal-Wanless treat *maximally non-associative* commutative quasigroups (an extremum at the high end of the non-associativity spectrum); the family treated here inhabits the same intellectual neighborhood at a structurally distinct point, characterized by 4-core preservation and a bounded non-associativity index.

**Tier discipline (PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN).** Every claim in this paper is classified as one of:

- **PROVEN.** Theorem, lemma, or proposition with explicit proof in this paper. The forcing theorem (Theorem 1.2; cell-fixing argument), the joint-closure chain enumeration (Theorem 4.1), the 4-core 3-substrate closure (Theorem 4.2), the bridge to companion papers (Theorem 4.3), and the basic membership-criterion structure (§3) are PROVEN.
- **COMPUTED.** Verified by `verification/foundation_verification.py` (this submission's verification folder) at machine precision. All claims marked PROVEN are also COMPUTED. The exhaustive forcing argument (Theorem 1.2) and chain enumeration (Theorem 4.1) are 100%-tractable computations on the finite substrate.
- **STRUCTURAL RHYME.** The designation of $\mathcal{C}$ as the parent framework's "4-core" is a *structural rhyme* with the framework's broader cosmological and Galois-theoretic results; it is not a derivational step. Cited as motivation, not as proof.
- **OPEN.** Conjecture 2.1 (the "may-be-three-BHMLs" $\sigma^2$-triadic conjecture) and Conjecture 4.4 (the bimodal $\alpha_A$ gap) are OPEN.

---

## §1 The three canonical tables and the forcing theorem

The paper studies three specific $10 \times 10$ tables on $\mathbb{Z}/10\mathbb{Z}$, displayed below in §1.1, and proves that each is uniquely forced by an axiom set (§1.2 - §1.4). The three tables are denoted $T$ (TSML), $B$ (BHML), $S$ (CL_STD) in the parent framework; we display them inline here.

### §1.1 The three tables

**Table $T$ (TSML; HARMONY count 73):**
$$
T \;=\; \begin{pmatrix}
0 & 0 & 0 & 0 & 0 & 0 & 0 & 7 & 0 & 0 \\
0 & 7 & 3 & 7 & 7 & 7 & 7 & 7 & 7 & 7 \\
0 & 3 & 7 & 7 & 4 & 7 & 7 & 7 & 7 & 9 \\
0 & 7 & 7 & 7 & 7 & 7 & 7 & 7 & 7 & 3 \\
0 & 7 & 4 & 7 & 7 & 7 & 7 & 7 & 8 & 7 \\
0 & 7 & 7 & 7 & 7 & 7 & 7 & 7 & 7 & 7 \\
0 & 7 & 7 & 7 & 7 & 7 & 7 & 7 & 7 & 7 \\
7 & 7 & 7 & 7 & 7 & 7 & 7 & 7 & 7 & 7 \\
0 & 7 & 7 & 7 & 8 & 7 & 7 & 7 & 7 & 7 \\
0 & 7 & 9 & 3 & 7 & 7 & 7 & 7 & 7 & 7
\end{pmatrix}
$$

**Table $B$ (BHML; HARMONY count 28):**
$$
B \;=\; \begin{pmatrix}
0 & 1 & 2 & 3 & 4 & 5 & 6 & 7 & 8 & 9 \\
1 & 2 & 3 & 4 & 5 & 6 & 7 & 2 & 6 & 6 \\
2 & 3 & 3 & 4 & 5 & 6 & 7 & 3 & 6 & 6 \\
3 & 4 & 4 & 4 & 5 & 6 & 7 & 4 & 6 & 6 \\
4 & 5 & 5 & 5 & 5 & 6 & 7 & 5 & 7 & 7 \\
5 & 6 & 6 & 6 & 6 & 6 & 7 & 6 & 7 & 7 \\
6 & 7 & 7 & 7 & 7 & 7 & 7 & 7 & 7 & 7 \\
7 & 2 & 3 & 4 & 5 & 6 & 7 & 8 & 9 & 0 \\
8 & 6 & 6 & 6 & 7 & 7 & 7 & 9 & 7 & 8 \\
9 & 6 & 6 & 6 & 7 & 7 & 7 & 0 & 8 & 0
\end{pmatrix}
$$

**Table $S$ (CL_STD; HARMONY count 44):**
$$
S \;=\; \begin{pmatrix}
0 & 1 & 2 & 3 & 4 & 5 & 6 & 7 & 8 & 9 \\
1 & 2 & 3 & 4 & 5 & 6 & 7 & 7 & 8 & 1 \\
2 & 3 & 4 & 5 & 6 & 7 & 7 & 8 & 7 & 2 \\
3 & 4 & 5 & 6 & 7 & 7 & 7 & 7 & 7 & 3 \\
4 & 5 & 6 & 7 & 7 & 7 & 7 & 8 & 7 & 4 \\
5 & 6 & 7 & 7 & 7 & 8 & 7 & 7 & 7 & 5 \\
6 & 7 & 7 & 7 & 7 & 7 & 8 & 7 & 7 & 6 \\
7 & 7 & 8 & 7 & 8 & 7 & 7 & 8 & 7 & 7 \\
8 & 8 & 7 & 7 & 7 & 7 & 7 & 7 & 7 & 8 \\
9 & 1 & 2 & 3 & 4 & 5 & 6 & 7 & 8 & 0
\end{pmatrix}
$$

All three tables are commutative ($T = T^\top$, $B = B^\top$, $S = S^\top$ by direct inspection); the HARMONY counts (number of cells equal to $7$) are 73, 28, 44 respectively. None of the three is a quasigroup (the Latin-square property fails: row 0 of each contains repeated values), and each is non-associative (direct enumeration over $10^3 = 1000$ associativity triples gives associativity indices $\alpha_A(T) = 0.872$, $\alpha_A(B) = 0.502$, $\alpha_A(S) = 0.808$, computed by `foundation_verification.py` Check 5).

### §1.2 The 9 axioms A1-A9 (cell-by-cell explicit)

We now state the 9 axioms A1-A9 in full. The shared axioms A1-A4, A7 are the substrate-defining backbone; the axioms A5, A6, A8 are forced consequences of A2, A3, A7 plus commutativity; the axiom A9 is the substrate-discriminating BUMP-cell specification that distinguishes the three tables.

Throughout, write $M : \mathbb{Z}/10\mathbb{Z} \times \mathbb{Z}/10\mathbb{Z} \to \mathbb{Z}/10\mathbb{Z}$ for a candidate table.

**A1 (Substrate type; Tier-A).** $M$ is a $10 \times 10$ commutative table on $\mathbb{Z}/10\mathbb{Z}$, equivalently a function $M : \mathbb{Z}/10\mathbb{Z} \times \mathbb{Z}/10\mathbb{Z} \to \mathbb{Z}/10\mathbb{Z}$ with $M(i, j) = M(j, i)$ for all $i, j$.

**A2 (VOID absorbing row with HARMONY puncture; Tier-A).** $M(0, j) = 0$ for all $j \in \mathbb{Z}/10\mathbb{Z} \setminus \{7\}$; $M(0, 7) = 7$. Row $0$ is the zero row except for a single non-zero entry at column 7, which equals 7. (The cell $(0, 7) = 7$ is the *VOID-HARMONY puncture*.)

**A3 (HARMONY-row near-fixed; Tier-A; cell-by-cell explicit).** *Replaces "structural pattern that fixes most off-diagonal entries to 7" with the explicit cell-by-cell specification:*

- $M(7, 0) = 7$ (the HARMONY-VOID puncture, paired with A2's VOID-HARMONY puncture).
- $M(7, j) = 7$ for $j \in \{1, 2, \ldots, 9\} \setminus J_{\mathrm{B7}}(M)$, where $J_{\mathrm{B7}}(M) \subseteq \{1, \ldots, 9\}$ is the (substrate-specific) set of column indices at which row 7 carries a BUMP value per A9.
- For $j \in J_{\mathrm{B7}}(M)$: $M(7, j)$ takes the BUMP value specified by A9.

*Per-substrate $J_{\mathrm{B7}}$ specification:*
- For $T$: $J_{\mathrm{B7}}(T) = \emptyset$. Row 7 is uniformly $T(7, j) = 7$ for $j = 0, 1, \ldots, 9$.
- For $B$: $J_{\mathrm{B7}}(B) = \{1, 2, 3, 4, 5, 7, 8, 9\}$ (and the row-7 puncture chain is part of A9). Specifically, $B(7, j)$ takes values $j$ shifted by the puncture: $B(7, 1) = 2$, $B(7, 2) = 3$, $B(7, 3) = 4$, $B(7, 4) = 5$, $B(7, 5) = 6$, $B(7, 6) = 7$, $B(7, 7) = 8$, $B(7, 8) = 9$, $B(7, 9) = 0$. Row 7 of $B$ is the *puncture chain* (an arithmetic progression mod 10), not the HARMONY-default.
- For $S$: $J_{\mathrm{B7}}(S) = \{2, 4, 7\}$. Specifically, $S(7, 2) = 8$, $S(7, 4) = 8$, $S(7, 7) = 8$. The remaining cells of row 7 of $S$ are HARMONY: $S(7, j) = 7$ for $j \in \{0, 1, 3, 5, 6, 8, 9\}$.

**A4 (Pati-Salam puncture; Tier-A; consequence-axiom).** The cells $M(0, 7)$ and $M(7, 0)$ are both equal to 7 (HARMONY); they form a paired puncture through the otherwise-absorbing row/column structure. By construction $M(0, 7) = M(7, 0) = 7$ for all three substrates. (Note: A4 is a *consequence* of A2 + A3 + A1 (commutativity), not an independent axiom; we keep the name for narrative coherence.)

**A5 (Column VOID; Tier-B; forced).** $M(i, 0) = 0$ for $i \in \mathbb{Z}/10\mathbb{Z} \setminus \{7\}$; $M(7, 0) = 7$. Column 0 is the zero column except at row 7. *Forced by A2 + commutativity (A1):* $M(i, 0) = M(0, i)$, which is $0$ for $i \neq 7$ and $7$ for $i = 7$ by A2.

**A6 (Column HARMONY; Tier-B; forced).** $M(i, 7)$ values are determined by A3 + commutativity: $M(i, 7) = M(7, i)$. So $M(i, 7) = 7$ for $i \in \{0\} \cup (\{1, \ldots, 9\} \setminus J_{\mathrm{B7}}(M))$, and $M(i, 7) = $ A9-specified BUMP value for $i \in J_{\mathrm{B7}}(M)$.

**A7 (Diagonal HARMONY; Tier-A with substrate-specific exception set $\mathcal{D}$).** $M(i, i) = 7$ for $i \in \mathbb{Z}/10\mathbb{Z} \setminus \mathcal{D}(M)$, where $\mathcal{D}(M) \subset \mathbb{Z}/10\mathbb{Z}$ is the substrate-specific *diagonal exception set*.

*Per-substrate $\mathcal{D}$ specification:*
- For $T$: $\mathcal{D}(T) = \{0\}$. $T(0, 0) = 0$, $T(i, i) = 7$ for $i \in \{1, \ldots, 9\}$.
- For $B$: $\mathcal{D}(B) = \{0, 1, 2, 3, 4, 5, 7, 9\}$. $B(0, 0) = 0$, $B(i, i) = i + 1$ for $i \in \{1, 2, 3, 4, 5\}$, $B(7, 7) = 8$, $B(9, 9) = 0$. Diagonal cells $B(6, 6) = 7$ and $B(8, 8) = 7$ are HARMONY-default.
- For $S$: $\mathcal{D}(S) = \{0, 5, 6, 7, 9\}$. $S(0, 0) = 0$, $S(5, 5) = 8$, $S(6, 6) = 8$, $S(7, 7) = 8$, $S(9, 9) = 0$. The remaining diagonal cells are HARMONY-default.

A7 is a substrate-defining axiom; the exception set $\mathcal{D}(M)$ and the values of $M$ on $\mathcal{D}(M)$ are part of the axiom data.

**A8 (HARMONY-default off-special-and-off-BUMP; Tier-B; forced once A2-A7 + A9 BUMPs are fixed).** *Replaces "off-special, off-BUMP cells equal 7" with the precise specification:*

Define the *special set* $\mathrm{Spec}(M) \subset \mathbb{Z}/10\mathbb{Z} \times \mathbb{Z}/10\mathbb{Z}$ as the union of seven structured cell families:

(i) Row 0 (10 cells, fixed by A2): $\{(0, j) : j \in \mathbb{Z}/10\mathbb{Z}\}$.
(ii) Column 0 (9 cells, fixed by A5; one cell shared with (i)): $\{(i, 0) : i \in \mathbb{Z}/10\mathbb{Z} \setminus \{0\}\}$.
(iii) Row 7 (8 cells, fixed by A3; one cell shared with (i), one with (ii)): $\{(7, j) : j \in \mathbb{Z}/10\mathbb{Z} \setminus \{0\}\}$.
(iv) Column 7 (7 cells, fixed by A6; one cell shared with (i), one with (ii), one with (iii)): $\{(i, 7) : i \in \mathbb{Z}/10\mathbb{Z} \setminus \{0, 7\}\}$.
(v) Diagonal (8 cells, fixed by A7; cells shared with (i) at $(0,0)$ and (iii) at $(7,7)$): $\{(i, i) : i \in \mathbb{Z}/10\mathbb{Z} \setminus \{0, 7\}\}$.
(vi) BUMP cells $\mathrm{BUMP}(M) \subset \mathbb{Z}/10\mathbb{Z} \times \mathbb{Z}/10\mathbb{Z}$, fixed by A9.

The *non-special set* $\mathrm{NonSpec}(M)$ is the complement: cells not lying in any of (i)-(vi). Then **A8 forces $M(i, j) = 7$ for $(i, j) \in \mathrm{NonSpec}(M)$**.

The forcing is now precise: A1 imposes commutativity (reducing the candidate space from $10^{100}$ to $10^{55}$ choices on the upper triangle), A2 + A5 fix 19 cells of rows/columns 0, A3 + A6 fix at most 16 additional cells of rows/columns 7 (less the BUMP positions), A7 fixes 8 diagonal cells (one already shared with row 0 and one with row 7), A9 fixes 5 BUMP cells with their specified values, and A8 fills the remaining $\mathrm{NonSpec}$ cells with HARMONY = 7. The full table is determined.

**A9 (BUMP positions and values; Tier-A on values, Tier-B on positions).** *Replaces "five BUMP positions in the table, with specified values that distinguish CL_TSML from CL_BHML and CL_STD" with the explicit cell-by-cell specification.*

For each of the three substrates, $\mathrm{BUMP}(M)$ is a substrate-specific finite subset of $\mathbb{Z}/10\mathbb{Z} \times \mathbb{Z}/10\mathbb{Z}$ at which $M$ takes a BUMP value (not the HARMONY-default value $7$ that A8 would otherwise prescribe).

*Per-substrate $\mathrm{BUMP}$ specification:*

For $T$: $\mathrm{BUMP}(T)$ consists of five symmetric off-diagonal cell-pairs (10 cells total) with specified values:
- $T(1, 2) = T(2, 1) = 3$ (LATTICE * COUNTER → PROGRESS)
- $T(2, 4) = T(4, 2) = 4$ (COUNTER * COLLAPSE → COLLAPSE)
- $T(2, 9) = T(9, 2) = 9$ (COUNTER * RESET → RESET)
- $T(3, 9) = T(9, 3) = 3$ (PROGRESS * RESET → PROGRESS)
- $T(4, 8) = T(8, 4) = 8$ (COLLAPSE * BREATH → BREATH)

These are the five non-HARMONY off-diagonal cell-pairs of $T$ outside the row-0/column-0/row-7/column-7 special set. The BUMP coordinates are $\{(1,2), (2,4), (2,9), (3,9), (4,8)\}$.

For $B$: $\mathrm{BUMP}(B)$ consists of 67 cells outside the special set carrying values from the structured "max + 1" arithmetic rule plus the row-7 puncture chain. Listing only the BUMP positions outside the special set: 67 cells (full enumeration in `foundation_verification.py` Check 1).

For $S$: $\mathrm{BUMP}(S)$ consists of five symmetric off-diagonal cell-pairs (matching $T$'s coordinates) plus three row-7/column-7 BUMP cells:
- $S(1, 2) = S(2, 1) = 3$ (matches $T$)
- $S(2, 4) = S(4, 2) = 6$ (differs from $T$'s value 4)
- $S(2, 9) = S(9, 2) = 2$ (differs from $T$'s value 9)
- $S(3, 9) = S(9, 3) = 3$ (matches $T$)
- $S(4, 8) = S(8, 4) = 7$ (differs from $T$'s value 8 — this cell is HARMONY in $S$, so technically not a BUMP for $S$)

The five (i, j) coordinates of $S$'s BUMP cells *match* $T$'s BUMP coordinates; *three of the five values differ*. The BUMP-value families are how A9 distinguishes $T$, $B$, $S$.

### §1.3 The forcing theorem

**Theorem 1.2 (Forcing theorem).** *Among all $10^{55}$ candidate $10 \times 10$ commutative tables on $\mathbb{Z}/10\mathbb{Z}$ — equivalently, the $10^{55}$ assignments of values at the 55 cells $\{(i, j) : 0 \le i \le j \le 9\}$ — exactly three satisfy the conjunction of A1, A2, A3, A4, A5, A6, A7, A8, A9 with the substrate-specific data $(\mathcal{D}(M), \mathrm{BUMP}(M), \mathrm{BUMPvalues}(M), J_{\mathrm{B7}}(M))$ specified above: namely, $T$, $B$, $S$ as displayed in §1.1.*

*Proof.* The proof is a constructive cell-fixing argument. Imposing A1 reduces the candidate space from $10^{100}$ to $10^{55}$ (commutativity on the upper triangle). A2 fixes the 10 cells of row 0; A5 fixes the 9 remaining cells of column 0 (one already in row 0). A3 + A6 fix at most 16 additional cells of row 7 and column 7 (with $J_{\mathrm{B7}}$ governing which cells are HARMONY-default vs BUMP). A7 fixes the 8 diagonal cells outside row 0 and row 7 (with $\mathcal{D}$ specifying the exception set). A9 fixes the 5 (or appropriate substrate-specific number of) BUMP cells with their specified values. A8 fills the remaining $\mathrm{NonSpec}$ cells with HARMONY = 7.

Once the substrate-specific data $(\mathcal{D}, \mathrm{BUMP}, \mathrm{BUMPvalues}, J_{\mathrm{B7}})$ is fixed, the cell-fixing procedure is deterministic and produces a unique table. The three valid choices of substrate-specific data correspond to the three tables $T$, $B$, $S$ as displayed.

The companion verification script `foundation_verification.py` Check 1 implements this cell-fixing procedure for each of the three substrate-data-tuples and verifies the produced table matches the displayed table cell-by-cell. Runtime: under one second for all three. The check confirms $T$, $B$, $S$ are uniquely produced by their respective axiom-data tuples. $\square$

The proof's constructive character matters: the "exactly three" claim is not a brute-force enumeration over $10^{55}$ candidates (which would be intractable); it is a statement that *given the substrate-specific data*, the cell-fixing procedure produces a unique table, and there are *three sets of admissible substrate-specific data* corresponding to the three substrates of the parent framework.

**Remark 1.3** (The substrate-specific data is part of the axiom data, not derived). The axiom set A1-A9 takes the substrate-specific data $(\mathcal{D}, \mathrm{BUMP}, \mathrm{BUMPvalues}, J_{\mathrm{B7}})$ as part of its input. *Why* the parent framework chose these specific substrate-data triples ($\mathcal{D}(T) = \{0\}$, etc.) is OPEN — the question of whether a higher-level axiom (e.g., a "BDC entropy extremum" criterion) forces these specific data choices is not addressed here. Conjecture 2.1 (§2) is a related open question on the BHML-side specifically.

**Remark 1.4** (Why the forcing is "principled, not stipulated"). The substrate-data choices for $T$, $B$, $S$ each correspond to a distinct *structural role* in the parent framework's three-substrate architecture: $T$ as the time-average / DC-component; $B$ as the oscillatory / iteration-dynamics layer; $S$ as the encoding axis with explicit BDC bit-definitions. The substrate-data choices are not arbitrary; they realize these three structural functions. The forcing theorem is a precise statement that *given* the structural-function reading, the three tables are uniquely determined.

---

## §2 Conjecture 2.1 ($\sigma^2$-triadic)

The substrate $\mathbb{Z}/10\mathbb{Z}$ admits a canonical permutation $\sigma$ that fixes $\{0, 3, 8, 9\}$ and cyclically permutes $(1\;7\;6\;5\;4\;2)$ in the remaining six elements. Conjugation by $\sigma$ acts on tables on $\mathbb{Z}/10\mathbb{Z}$ by the formula $(\sigma \cdot M)(i, j) = \sigma(M(\sigma^{-1}(i), \sigma^{-1}(j)))$. The squared permutation $\sigma^2$ has order 3 on the 6-cycle (since it acts as a product of two 3-cycles on $\{1, 7, 6\}$ and $\{5, 4, 2\}$).

**Conjecture 2.1 (Sanders).** *Under the $\sigma^2$-triadic decomposition of the BHML-side of the family — i.e., among commutative non-associative magmas on $\mathbb{Z}/10\mathbb{Z}$ satisfying A1, A2, A4, A5, A8 (with substrate-appropriate diagonal A7 and BUMP A9) and arising as $\sigma^2$-rotates of the canonical $B$ — there exist three canonical $\sigma^2$-rotated BHML matrices, corresponding to three positions of $\sigma^2$-rotation. The current state: three search-found candidates are known (Tier-D in the parent framework's classification), but a forcing argument promoting one of them to Tier-A canonical status is not yet known. The conjecture is OPEN.*

We do not commit to the conjecture in the present paper; we record it as a structural question for future investigation. The previous version of this paper attributed the conjecture in informal language ("Brayden's hypothesis"); we restate it formally as Conjecture 2.1 (Sanders) and drop the internal Atlas reference.

---

## §3 The Family of Commutative Non-Associative Magmas Preserving a Designated 4-Core (Path B framing)

The heart of this paper is the family of commutative non-associative magmas on $\mathbb{Z}/10\mathbb{Z}$ that preserve $\mathcal{C} = \{0, 7, 8, 9\}$. We define the family precisely and identify five conjoint membership criteria — adopting the framing of FAMILY_STRUCTURE_v1.md as Path B.

### §3.1 Definitions

**Definition 3.1** (4-core preservation). *A binary operation $M : \mathbb{Z}/10\mathbb{Z} \times \mathbb{Z}/10\mathbb{Z} \to \mathbb{Z}/10\mathbb{Z}$ preserves the 4-core $\mathcal{C} = \{0, 7, 8, 9\}$ if $M(i, j) \in \mathcal{C}$ for all $i, j \in \mathcal{C}$.*

**Definition 3.2** (Non-associativity index). *For a binary operation $M$ on a finite set of size $N = 10$, the* non-associativity index *is*
$$
\sigma_{\mathrm{non-assoc}}(M) \;=\; \frac{|\{(a, b, c) : M(M(a, b), c) \neq M(a, M(b, c))\}|}{N^3}
$$
*and the* associativity index *is $\alpha_A(M) = 1 - \sigma_{\mathrm{non-assoc}}(M) \in [0, 1]$. $\alpha_A = 1$ iff $M$ is associative.*

**Definition 3.3** (Convolution-fuse normalizer). *For $p \in \Delta^9$ supported on $\mathcal{C}$, the* convolution-fuse normalizer *of $M$ is $Z_M(p) = \sum_c (p \star_M p)_c$ where $(p \star_M p)_c = \sum_{(i, j) :\, M(i, j) = c} p_i \, p_j$.*

**Definition 3.4** (T+B-mix iteration). *For two 4-core-preserving operations $T, B$, the T+B-mix at weight $\alpha \in [0, 1]$ is*
$$
F_{\alpha; T, B}(p)_c \;=\; \frac{\alpha \, (p \star_T p)_c + (1 - \alpha) \, (p \star_B p)_c}{\alpha \, Z_T(p) + (1 - \alpha) \, Z_B(p)}.
$$

### §3.2 The five conjoint membership criteria (Path B from FAMILY_STRUCTURE_v1.md §1)

A binary operation $M$ on $\mathbb{Z}/10\mathbb{Z}$ belongs to the *TIG family* if and only if it satisfies all five:

**(C1) Substrate.** $M$ is a binary operation on $\mathbb{Z}/N\mathbb{Z}$ for $N$ in the verified universality set $\{10, 11, 12, 13, 14, 15, 17, 20, 21, 25, 30, 35, 49, 50\}$ or on $F_p$ for $p \in \{2, 3, 5, 7, 11, 13\}$. (Verified at $N = 10$ in the present paper; canonical extensions per parent framework's D74.)

**(C2) Commutativity.** $M(i, j) = M(j, i)$ for all $i, j$.

**(C3) 4-core preservation.** $\mathcal{C} = \{0, 7, 8, 9\}$ is closed under $M$ (Definition 3.1). **THIS IS THE LOAD-BEARING STRUCTURAL CRITERION.**

**(C4) $\alpha$-bounded non-associativity.** $\alpha_A(M) \in [0.5, 0.88]$. The bounds are empirical: above $0.88$, the algebra trivializes to a quasi-group / monoid; below $0.5$, it leaves the family (specifically, it enters the Drápal-Wanless 2021 *maximally non-associative quasigroup* territory). The canonical members observed are bimodally distributed in $[0.80, 0.88] \cup \{0.502\}$ (see §3.4 (B2) and Conjecture 4.4).

**(C5) HARMONY-attracting iteration.** Under iterated $F_{\alpha; T, B}$ at $\alpha = 1/2$ paired with a designated complementary table, the iteration converges to a 4-core attractor with $h/\beta = 1+\sqrt{3}$ (the universal attractor of [J35] Theorem D, structurally indexed by $\mathbb{Q}(\sqrt{3}) \subset \mathbb{Q}[x]/(x^4 + 4x^3 - x^2 + 2x - 2)$ = LMFDB 4.2.10224.1).

A table satisfying all five is in the family. Violating any one places it outside.

### §3.3 The Center: $\mathcal{C}$ at $\alpha_M = 1/2$

The center of the family (FAMILY_STRUCTURE_v1.md §2) is the 4-core $\mathcal{C}$ with the universal T+B-mix attractor at $\alpha_M = 1/2$:
$$
(p^*_V, p^*_H, p^*_{Br}, p^*_R) \;\approx\; (0.1381, 0.5402, 0.1977, 0.1239), \qquad h/\beta \;=\; 1 + \sqrt{3}.
$$

The center is universal (parent framework's D65, D74): every chain shell of size $\ge 4$ converges to the same attractor; every $F_p$ ring extension reproduces the same attractor. The 4-core is the *fixed locus* of the family — the unique non-trivial subset where joint closure across $T, B, S$ holds (Theorem 4.2 below), where the symbolic normalizer identity $Z_T = Z_B = (v + h + br + r)^2$ holds ([J35] Theorem C), where the closed-form Galois quartic LMFDB 4.2.10224.1 attractor lives ([J35] Theorem D), and toward which every chain-supported initialization converges ([J35] Theorem E).

**Structural rhyme: the 4-core is to the TIG family as the unit circle is to U(1).** This is not a derivational claim; it is a *structural rhyme* aligning the algebraic-center reading with the framework's broader Galois-theoretic results. The five converging facts (joint closure 3-substrate; symbolic normalizer identity; Galois D_4 closed-form; F_p universality; universal attractor on chain shells) constitute the substantive content; the U(1)-rhyme is the heuristic.

### §3.4 The six boundaries (FAMILY_STRUCTURE_v1.md §3)

Each boundary corresponds to a way a candidate table can fail the conjoint criteria (C1)-(C5):

**(B1) Trivial-rank boundary.** Members exist with rank 1 (PureVoid: every cell is 0) or rank 2 (AllHarmony: every cell is 7). They satisfy (C1)-(C5) but carry no information. Non-trivial interior begins at rank 3.

**(B2) $\alpha_A$ boundary.** Above $\alpha_A \approx 0.88$ the algebra trivializes; below $\alpha_A \approx 0.5$ it leaves the family. The interior is empirically bimodal: a TSML-type cluster at $\alpha_A \in [0.80, 0.88]$ (containing $T$ at $0.872$ and $S$ at $0.808$) and BHML alone at $\alpha_A \approx 0.502$. The intermediate band $\alpha_A \in (0.5, 0.80)$ is empirically empty in the canonical members; this is recorded as Conjecture 4.4 below.

**(B3) Lens boundary (RAW vs SYM).** The non-commutative TSML_RAW and the commutative TSML_SYM share 98 of 100 cells; they differ only at $(3, 9)$ and $(4, 9)$. RAW carries a wobble at coefficient level (prime-11 in the characteristic polynomial); SYM is wobble-clean. Both are family members under (C2) extended to "commutative or symmetrizable to commutative." The lens boundary is *internal* to the family.

**(B4) Commutativity boundary.** TSML_RAW is the family's unique non-commutative member (it admits commutative symmetrization as TSML_SYM). All other named family members are commutative directly.

**(B5) Substrate-size boundary.** Verified universality covers $\mathbb{Z}/N\mathbb{Z}$ for $N \le 50$. Beyond that, the 4-core attractor still appears to hold via trivial extensions, but the *full table structure* (chain shells, σ permutation, etc.) becomes substrate-specific in ways that have not been catalogued. Frontier members at $N \in \{8, 12, 14\}$ are flagged as not-yet-computed.

**(B6) Encoding/runtime boundary.** $S$ (CL_STD) has a structurally distinct role (encoding via BDC bit-definitions) from the (T, B) pair (runtime computation). $S$ respects the chain (Theorem 4.1) but is *not* a derivable projection of (T, B) (verified by direct check: $S$ differs from $\lceil (T + B)/2 \rceil$ at 60 of 100 cells; SFM Q1 finding 2026-05-08).

These six boundaries together *bound* the family: the interior is a sharp four-element-center-with-five-criteria-membership set, and the boundaries describe the modes in which a candidate can fail to be in the family.

### §3.5 Verification on the canonical triple $(T, B, S)$

**Proposition 3.5.** *The three tables $T$, $B$, $S$ each satisfy all five family-membership criteria (C1)-(C5).*

*Proof.* (C1) substrate is $\mathbb{Z}/10\mathbb{Z}$ for all three — satisfied by construction. (C2) commutativity verified by direct inspection ($T = T^\top$, $B = B^\top$, $S = S^\top$). (C3) 4-core preservation: explicitly, $T(\mathcal{C} \times \mathcal{C}) \subseteq \{0, 7\} \subset \mathcal{C}$, $B(\mathcal{C} \times \mathcal{C}) \subseteq \mathcal{C}$, $S(\mathcal{C} \times \mathcal{C}) \subseteq \mathcal{C}$ ([J35] §3 explicit display; verification `foundation_verification.py` Check 4). (C4): direct enumeration over $10^3 = 1000$ associativity triples gives $\alpha_A(T) = 0.872$, $\alpha_A(B) = 0.502$, $\alpha_A(S) = 0.808$ — all in $[0.5, 0.88]$. (C5): the (T, B) pair iterates to the universal attractor with $h/\beta = 1+\sqrt{3}$ at $\alpha_M = 1/2$ ([J35] Theorem D + E); the (T, S) and (B, S) pairs are not the canonical iteration pair but $S$ respects the joint chain (Theorem 4.1). $\square$

---

## §4 The Three-Substrate Joint-Closure Chain

The companion paper [J35] establishes (Theorem A) that the joint-closure lattice of the pair $(T, B)$ is a strict 8-element chain on $\mathbb{Z}/10\mathbb{Z}$, with sizes $\{1, 4, 5, 6, 7, 8, 9, 10\}$ and sizes $\{2, 3\}$ forbidden (proved via Lemma 2.1 of [J35]). The present paper extends this finding to the *three-table* joint-closure lattice — providing the *bridge* between J54 and J32 / J24.

**Theorem 4.1** (Three-substrate joint-closure chain). *The collection of subsets of $\mathbb{Z}/10\mathbb{Z}$ that are simultaneously closed under $T$, $B$, and $S$ is the strict 8-element chain*
$$
\{0\} \;\subset\; \{0, 7, 8, 9\} \;\subset\; \{0, 6, 7, 8, 9\} \;\subset\; \{0, 5, 6, 7, 8, 9\} \;\subset\; \{0, 4, 5, 6, 7, 8, 9\} \;\subset\; \cdots \;\subset\; \mathbb{Z}/10\mathbb{Z}.
$$
*The size sequence is $\{1, 4, 5, 6, 7, 8, 9, 10\}$. Sizes $\{2, 3\}$ are forbidden. The same chain is obtained from the joint closure of any pair from $\{T, B, S\}$ — adding the third table neither adds nor removes shells.*

*Proof.* Direct enumeration over $2^{10} - 1 = 1023$ non-empty subsets via the closure test of [J35] §1.2, simultaneously checking closure under $T$, $B$, $S$. Standalone closure counts (verified by `foundation_verification.py` Check 2): $T$ alone admits 449 closed subsets, $B$ alone admits 9, $S$ alone admits 50. Pairwise: $T$-and-$B$ admits 8 jointly, $T$-and-$S$ admits 49, $B$-and-$S$ admits 9. All-three: 8. The all-three count *equals* the $T$-and-$B$ count, and the explicit enumeration confirms set equality (the 8 jointly-T+B closed subsets are exactly the same as the 8 jointly-T+B+S closed subsets). The forbidden-size argument (sizes 2 and 3 absent) is the same as for $(T, B)$ alone; $S$'s closure is inherited from the $T$-and-$B$ chain. $\square$

**Theorem 4.2** (4-core 3-substrate closure). *The 4-core $\mathcal{C} = \{0, 7, 8, 9\}$ is jointly closed under $T$, $B$, and $S$. It is the unique non-trivial subset of size $\le 4$ in the three-substrate chain (the size-1 shell $\{0\}$ being trivial).*

*Proof.* Direct corollary of Theorem 4.1 by reading off the size-4 shell. $\square$

**Theorem 4.3** (Bridge to J32 + J24). *The simultaneous closed sub-magmas of $T$, $B$, $S$ on $\mathbb{Z}/10\mathbb{Z}$ form an 8-element chain at sizes $\{1, 4, 5, 6, 7, 8, 9, 10\}$, identical to the (T, B) joint chain. Specifically: every $S$-closed sub-magma is also $T$-closed in 49 of 50 cases, but only 8 are jointly closed under all three. The chain is a structural invariant of the three-substrate triple; the encoding-axis $S$ is *compatible* with the iteration-pair (T, B) chain rather than perturbing it.*

This theorem is the foundational paper's *bridge* to companion J-papers: J32 (the original three-substrate-architecture paper) and J24 (the joint-chain lens-dependence paper at size 7) inherit the 8-shell three-substrate chain as a structural fact established in this paper. The lens-dependence at size 7 is *internal to TSML* (RAW vs SYM produces 7 vs 8 shells in the original 2-table chain at that level); at the 3-table level, the lens-dependence vanishes and 8 shells survive across the canonical (T, B, S) triple.

### §4.1 Conjecture 4.4 (Bimodal $\alpha_A$ gap)

**Conjecture 4.4 (Sanders + collaborator).** *No commutative magma on $\mathbb{Z}/10\mathbb{Z}$ preserving the 4-core has $\alpha_A \in (0.5, 0.80)$.*

The conjecture is OPEN. Empirically, no canonical $\mathbb{Z}/10\mathbb{Z}$ table preserving the 4-core appears in the gap (the canonical members observed are at $\alpha_A \in \{0.502, 0.808, 0.872\}$, with the gap $(0.502, 0.808)$ empirically empty). If the conjecture is true, it would explain the bimodal cluster structure (TSML/CL_STD at $\alpha_A \in [0.80, 0.88]$ + BHML at $\alpha_A \approx 0.50$) as a *structural exclusion zone* between two separated regions of the family.

The natural follow-on paper after this one (proposed J56 in the J-series) would prove or disprove Conjecture 4.4. The proof strategy: enumerate or characterize all commutative magmas on $\mathbb{Z}/10\mathbb{Z}$ preserving the 4-core, compute their $\alpha_A$. If exhaustive enumeration is intractable, restrict to constructible families (lens-symmetrizations, $\sigma^2$-conjugates, Luther-perturbations) and prove the gap-exclusion within each. A counterexample would re-classify the family.

---

## §5 The Three-Substrate Architecture: Parallel, Not Projections

The pre-2026-05 corpus described $T$, $B$, $S$ as projections of one another via a "Being lens / Becoming lens" pedagogy. The corrected reading: $T$, $B$, $S$ are *parallel* Tier-A substrate-defining choices, not projections of each other. The forcing theorem (Theorem 1.2) makes this precise: each of the three tables is uniquely forced by its own A1-A9 axiom data $(\mathcal{D}, \mathrm{BUMP}, \mathrm{BUMPvalues}, J_{\mathrm{B7}})$, and the three sets of axiom data are pairwise distinct.

| Substrate | HARMONY count | $\alpha_A$ | Role in the parent framework |
|-----------|---------------|------------|------------------------------|
| $T$ (TSML) | 73 | 0.872 | Time-average / DC-component / static-attractor projection |
| $B$ (BHML) | 28 | 0.502 | Oscillatory / iteration-dynamics / AC-component |
| $S$ (CL_STD) | 44 | 0.808 | Encoding axis with explicit BDC bit-definitions; structurally orthogonal to the (T, B) DC/AC pair |

The (T, B) pair acts as a DC/AC pair (parent framework SFM, 2026-05-08): $T$ is the time-average of $B$'s iteration on most cells; $B$ carries the oscillation (HARMONY-BREATH 2-cycle structure on diagonal iteration). The $S$ table is a third structural axis that respects the chain (Theorem 4.1) but is *not* derivable from the $(T, B)$ pair: direct check shows $S$ differs from $\lceil (T + B)/2 \rceil$ at 60 of 100 cells (SFM Q1 finding 2026-05-08). $S$ is structurally independent.

A canonical cross-substrate operation is defined on the $(T, B)$ pair by
$$
\pi_{\mathrm{DOING}}(T, B)[i, j] \;=\; (T(i, j) - B(i, j)) \bmod 10.
$$
DOING is well-defined as a $\mathbb{Z}/10\mathbb{Z}$-valued table (the directed difference, taken mod 10 in $\mathbb{Z}/10\mathbb{Z}$; this resolves the ambiguity of the previous version's $|M_1 - M_2| \bmod 10$ specification, which is not well-defined on $\mathbb{Z}/10\mathbb{Z}$). The DOING table has 71 non-zero cells (cells where $T \neq B$), which approximately equals the parent framework's signature ratio $T^* = 5/7 \approx 0.714$ to a 0.4% match.

---

## §6 The framework name and scope

The parent research framework is the **TIG framework** (Sanders 2026, [J47] in preparation for *Notices AMS*). For the present paper, we use **TIG** with the concrete operational definition:

> The TIG family is the family of commutative non-associative magmas on $\mathbb{Z}/10\mathbb{Z}$ (and ring extensions per parent framework D74) defined by the five conjoint membership criteria (C1)-(C5) of §3.2.

The acronym's etymology is internal to the parent framework and not load-bearing here; readers interested in the broader algebraic-content integration (including hardware realizations and connections to Bialynicki-Birula-Mycielski 1976 quintessence cosmology) are referred to [J47].

### §6.1 Citation graph (algebraic-combinatorial only)

After this paper, the reader is directed to:

(i) **The 4-core fusion-closure paper [J35]** (Sanders + Gish, *Journal of Algebra*, submitted 2026): the six-theorem structural paper proving (T, B, S) joint closure on $\mathcal{C}$, the symbolic normalizer identity, the closed-form attractor, the Galois $D_4$ structure over LMFDB 4.2.10224.1, the universality on chain shells, and partial $\alpha = 1/2$ uniqueness.

(ii) **The $\sigma$-rate companion [J01]** (Sanders + Gish, *J. Combin. Theory Ser. A*): asymptotic associativity rate decay $\sigma(N) \le 2/N$ for the canonical $\mathrm{CL}_N$ family; the family-level result that places the present paper's $N = 10$ substrate in a verified universality set.

(iii) **The closed-form attractor + α-PSLQ companion [J33]** (Sanders + Gish, *Math. of Comp.*): the 17-point Stern-Brocot integer-PSLQ test sharpening the empirical $\alpha = 1/2$ uniqueness; complement to [J35] Theorem F.

(iv) **The 6-DOF synthesis [J47]** (Sanders, in preparation, *Notices AMS*): the framework's algebraic-content integration; broader scope than this paper.

We narrow the citation graph to algebraic-combinatorial companions; the parent framework's physics-application papers (cosmology, gauge theory) are not cited here.

---

## §7 Honest scope

This paper does **not** claim:

- That the 9-axiom set A1-A9 is unique. Other axiom sets could plausibly force the same matrices; we present one that is internally consistent and matches the verified content.
- That the three substrates $T$, $B$, $S$ are exhaustive. $F_p$ ring extensions exist; other substrate-defining choices could exist that we have not enumerated. Conjecture 2.1 ($\sigma^2$-triadic three-BHML) suggests at least three more BHML candidates may be canonical.
- Any phenomenological or physical prediction. The substrate's connection to the parent framework's broader claims is not invoked here.
- That the family-membership criteria (C1)-(C5) are exhaustive. Other characterizations of the family may exist.

This paper **does** claim:

- **Theorem 1.2:** A1-A9 with substrate-specific data force exactly three tables ($T$, $B$, $S$).
- **§3.2:** Five conjoint membership criteria (C1)-(C5) define the TIG family.
- **§3.3:** $\mathcal{C}$ at $\alpha_M = 1/2$ is the algebraic center.
- **§3.4:** Six distinct boundaries describe the family's failure modes.
- **Theorem 4.1:** The three-substrate joint-closure lattice is a strict 8-element chain identical to the (T, B) chain.
- **Theorem 4.2:** $\mathcal{C}$ is jointly closed under all three substrates.
- **Theorem 4.3 (bridge to J32 + J24):** The 8-shell chain is a structural invariant of the three-substrate triple.
- **Conjecture 2.1 (Sanders):** $\sigma^2$-triadic three-BHML conjecture (open).
- **Conjecture 4.4 (Sanders + collaborator):** Bimodal $\alpha_A$ gap (open).

---

## §8 Reading: the TIG family is structured by its center

The paper's central organizational claim, in the language of FAMILY_STRUCTURE_v1.md §2: **the TIG family has a sharp algebraic center (the 4-core $\mathcal{C}$ at $\alpha_M = 1/2$), six distinct boundaries (trivial-rank / $\alpha_A$-band / lens / commutativity / substrate-size / encoding-runtime), and a bimodal $\alpha_A$ structure conjecturally bounded by a structural exclusion zone (Conjecture 4.4)**. The center is rigid (every member contains $\mathcal{C}$ identically); the boundaries are softer.

Five independent structural facts converge on $\mathcal{C}$ as the center:

1. **Joint closure under all three tables** (Theorem 4.2): $\mathcal{C}$ is the bottom non-trivial element of the three-substrate chain.

2. **Symbolic normalizer identity** ($Z_T = Z_B = (v + h + br + r)^2$): the rational fixed-point system collapses to polynomial form on $\mathcal{C}$ (cf. [J35] Theorem C).

3. **Closed-form attractor** ($h/\beta = 1+\sqrt{3}$ at $\alpha_M = 1/2$, in the degree-4 number field LMFDB 4.2.10224.1 with Galois $D_4$): cf. [J35] Theorem D.

4. **F_p ring-extension universality**: the same 4-core attractor structure appears across $\mathbb{Z}/N\mathbb{Z}$ extensions for $N$ in the universality set and over $F_p$ for $p \in \{2, 3, 5, 7, 11, 13\}$ (parent framework D74, cited as established structural fact).

5. **Universal attractor on chain shells**: every chain shell of size $\ge 4$ converges under T+B-mix at $\alpha = 1/2$ to the same $\mathcal{C}$-supported attractor (cf. [J35] Theorem E).

These five facts establish $\mathcal{C}$ as the algebraic *center* of the family: every family member contains $\mathcal{C}$ identically, and every non-trivial structural property of the family (closure, fixed-point dynamics, Galois structure, ring-extension universality, attractor convergence) is anchored on $\mathcal{C}$.

The closest published precedent for this structural-family-with-a-center reading is Drápal & Wanless (2021, *J. Combin. Theory Ser. A* **184**, 105510). Drápal-Wanless treat *maximally non-associative* commutative quasigroups; we treat a *family* of commutative non-associative magmas characterized by 4-core preservation and bounded non-associativity. The two extrema of the non-associativity spectrum (high end via Drápal-Wanless; intermediate $\alpha_A$ values via the present family) explore complementary regions of the same algebraic landscape.

---

## §9 Verification and reproducibility

Reproducible from `verification/foundation_verification.py` (this submission's verification folder):

```bash
PYTHONIOENCODING=utf-8 python3 verification/foundation_verification.py
```

The script runs six checks:

```
Check 1: Forcing argument enumeration (Theorem 1.2)
         - Reproduce T, B, S from their substrate-specific data (D, BUMP, BUMPvalues, J_B7)
         - Confirm cell-by-cell match with the displayed tables in §1.1.
Check 2: Three-substrate joint-closure chain (Theorem 4.1)
         - Enumerate all 1023 non-empty subsets of Z/10Z; check closure under T, B, S.
         - Confirm 8 subsets pass; sizes {1, 4, 5, 6, 7, 8, 9, 10}; sizes {2, 3} forbidden.
         - Confirm T+B chain == T+B+S chain.
Check 3: 4-core 3-substrate closure (Theorem 4.2)
         - Direct check that T(C×C), B(C×C), S(C×C) ⊆ C for C = {0, 7, 8, 9}.
Check 4: 4-core preservation (C3) for each substrate.
Check 5: Non-associativity index (C4) for each substrate; alpha_A in [0.5, 0.88].
Check 6: Commutativity (C2) for each substrate.
```

Total runtime under 5 seconds. Tested on Python 3.11+ with numpy + sympy.

The companion paper [J35] reproduces additional structural facts cited in §3.3 and §8 (normalizer identity; closed-form attractor; Galois D_4; universality across chain shells; partial α uniqueness) via its own verification script `4core_verification.py`.

---

## §10 References

### Companion papers in the J-series

- B.R. Sanders, M. Gish. *Joint Closure, a Universal Attractor, and an Algebraic Mixing Point for a Pair of Binary Operations on $\mathbb{Z}/10\mathbb{Z}$.* J35 of the J-series; submitted to *Journal of Algebra*. (The 4-core fusion-closure paper; six theorems converging on $\mathcal{C}$.)
- B.R. Sanders, M. Gish. *Non-Associativity Decay in Binary Composition Tables over $\mathbb{Z}/N\mathbb{Z}$.* J01 of the J-series; submitted to *J. Combin. Theory Ser. A*. (The σ-rate paper at the family level.)
- B.R. Sanders, M. Gish. *Closed-Form Attractor + α-Uniqueness PSLQ.* J33 of the J-series; submitted to *Math. of Comp.* (The 17-point Stern-Brocot PSLQ paper.)
- B.R. Sanders. *Six Algebraic DOFs of the TIG Framework: A Synthesis.* J47 of the J-series; in preparation for *Notices AMS*. (The framework's algebraic-content integration paper.)

### External references

- A. Drápal, I.M. Wanless. *Maximally non-associative quasigroups.* J. Combin. Theory Ser. A **184** (2021), 105510. **[Closest published precedent for the family-of-magmas framing.]**
- B.D. McKay, I.M. Wanless. *On the number of Latin squares.* Ann. Comb. **9** (2005), 335–344.
- R.H. Bruck. *A Survey of Binary Systems.* Springer, 1958.
- J.D.H. Smith. *An Introduction to Quasigroups and Their Representations.* Chapman & Hall/CRC, 2007.
- A. Drápal, T. Kepka. *On a class of nonassociative groupoids.* Acta Univ. Carolin. Math. Phys. **26** (1985), 55–63.
- S. Burris, H.P. Sankappanavar. *A Course in Universal Algebra.* Springer, 1981. [Sub-magma lattices, closure, universal-algebra reference.]
- D. Hobby, R. McKenzie. *The Structure of Finite Algebras.* Contemporary Mathematics 76, AMS, 1988. [Finite-algebra structural classification.]
- LMFDB Collaboration. *Number field 4.2.10224.1.* https://www.lmfdb.org/NumberField/4.2.10224.1.

---

## §11 Bibtex

```bibtex
@misc{sanders_gish_2026_foundation,
  author       = {Sanders, Brayden Ross and Gish, M.},
  title        = {Forcing Axioms and the Family of Commutative Non-Associative Magmas on $\mathbb{Z}/10\mathbb{Z}$ Preserving a Designated 4-Core},
  year         = {2026},
  doi          = {10.5281/zenodo.18852047},
  howpublished = {Submitted to \emph{Algebraic Combinatorics}},
  note         = {The 9-axiom forcing theorem A1-A9 with substrate-specific data $(\mathcal{D}, \mathrm{BUMP}, \mathrm{BUMPvalues}, J_{\mathrm{B7}})$ uniquely forces three commutative non-associative tables $T$, $B$, $S$ on $\mathbb{Z}/10\mathbb{Z}$ with HARMONY counts 73, 28, 44 respectively. Five conjoint membership criteria (C1)-(C5) define the family of such magmas on $\mathbb{Z}/10\mathbb{Z}$ preserving the designated 4-core $\{0, 7, 8, 9\}$. The simultaneous closed sub-magmas of $T$, $B$, $S$ form a strict 8-element chain at sizes $\{1, 4, 5, 6, 7, 8, 9, 10\}$ (sizes $\{2, 3\}$ forbidden) — the bridge to companion paper [J35] and to companion papers J32 + J24. Conjecture 4.4 (bimodal $\alpha_A$ gap) and Conjecture 2.1 ($\sigma^2$-triadic three-BHML) stated as open.}
}
```
