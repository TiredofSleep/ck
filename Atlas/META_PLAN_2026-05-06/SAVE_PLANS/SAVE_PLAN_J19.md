# SAVE_PLAN_J19 — DKAN Two-Coding (EJC → restructure around Path C: Role-Quotient theorem)

**Date:** 2026-05-07
**Status:** SAVE possible via referee's Path C (categorical structure / role-quotient theorem). The referee explicitly maps three save paths; Path C aligns best with the corpus's actual D-table backing (D93 role partition + role magma with VOID identity). Drop DKAN architecture content; drop Katok-Ugarcovici scaffolding; build the paper around the role-quotient structure.
**Referee:** `Atlas/META_PLAN_2026-05-06/REFEREE_REPORTS/J19_EJC_FreshEyes.md` (Reject; reasons M1-M5 + S1-S6)

---

## §1 — Why save?

The current J19 manuscript has three load-bearing problems per the referee, but the underlying structural content (the D88-D94 bridge findings on the corrected substrate frame) is genuine and includes one theorem-shaped result — D93 — that the referee's Path C explicitly invites.

**(a) D-table backing for Path C.** D93 (role partition + role magma) gives:
- A canonical functional partition: Flow $F = \{1, 3, 5, 7, 9\}$, Structure $S = \{2, 4, 8\}$, Transition $T = \{6\}$, Void $V = \{0\}$ (5+3+1+1 = 10).
- The induced *role magma* on the 4-element role set $\{V, F, S, T\}$ via the BHML output mode per input role-pair.
- VOID is the identity element of this role magma (V·x = x for all roles).
- The role magma is **not associative** (e.g., (F·F)·S = F ≠ F·(F·S) = T).
- Branching role-pairs are exactly $\{F\text{-}F, F\text{-}S, S\text{-}F, S\text{-}S\}$ — 4 of the 16 role-pairs.
- The 4-role partition cuts across $\sigma$-orbit ($\sigma$ has the 6-cycle (1 7 6 5 4 2) and 4 fixed points {0, 3, 8, 9}; the role partition has 3F+1T+2S in the 6-cycle and 1V+2F+1S in the fixed-point set) — establishing the role partition as a *third independent decomposition* alongside operator-index and σ-orbit.

The referee's Path C asks: "State and prove a theorem about the role-quotient magma: 'The induced operations $\overline{T}, \overline{B}$ on the 4-element role set $\{V, F, S, T\}$ are well-defined if and only if [Z].' The condition [Z] is testable from the role-assignment table; the resulting quotient (if it exists) is a concrete combinatorial object."

D93 supplies exactly this. The role magma is shown to be well-defined (the BHML output mode per input role-pair is a function $\{V, F, S, T\}^2 \to \{V, F, S, T\}$, computed). The condition [Z] is the explicit characterization of when a magma's binary operation descends to a well-defined operation on a partition's quotient — this is the categorical "well-definedness" theorem.

**(b) Structural role per FAMILY_STRUCTURE_v1.md.** The Family Structure document does not directly require J19 (DKAN is an applications paper, not a family-structure-foundations paper), but the role partition discussed here connects to the broader 4-core / α=½ / 1+√3 architecture. The role partition's V (which is just $\{0\} = $ VOID, the operator-index 0) is the same V as the 4-core's V — meaning the role-quotient magma's identity element is the same operator that anchors the 4-core's algebraic center. This connection is worth flagging: the role-quotient theorem's identity element coincides with the 4-core's identity element. Drápal-Wanless 2021 *JCT-A* 184, 105510 is the published precedent for finite commutative non-associative magma analysis — same domain.

**(c) The combinatorial fingerprint counts (5/64, 60/64, 24/64) are correct and verified.** Theorems 2.1-2.3 of the current manuscript hold by direct enumeration; the referee verified them. The save preserves these as supporting data behind the role-quotient theorem rather than as the lead claims.

The honest read: **the current J19 manuscript's lead claims (the DKAN architecture, the Katok-Ugarcovici two-coding analogy) do not survive at EJC.** A restructured paper using D93 as the lead theorem can survive. The save requires substantial restructuring but no new mathematics.

---

## §2 — Specific fixes (line by line against the referee report)

### M1 (no internal theorem with EJC weight) — **REPLACE Theorems 2.1-2.3 with Path C role-quotient theorem**

Current Theorems 2.1, 2.2, 2.3 are direct counts on a fixed 10×10 (and 8×8) table — "by inspection." Path C builds the new lead:

**New Main Theorem (Role-Quotient Theorem; restating D93 in EJC form):** Let $T, B$ be commutative magmas on $\mathbb{Z}/10\mathbb{Z}$ (specifically TSML and BHML, with the role partition $V \mid F \mid S \mid T = \{0\} \mid \{1,3,5,7,9\} \mid \{2,4,8\} \mid \{6\}$). Then:

(i) The induced operation $\overline{B}: \{V, F, S, T\}^2 \to \{V, F, S, T\}$ — defined by taking the role of the modal value of $B$ on each role-pair input — is well-defined as a function on roles.

(ii) Equivalently, for each pair of roles $(\rho_1, \rho_2)$ with $\rho_1, \rho_2 \in \{V, F, S, T\}$, the value $\rho(B(a, b))$ for $a \in \rho_1, b \in \rho_2$ is determined (modulo the explicit branching set $\{F\text{-}F, F\text{-}S, S\text{-}F, S\text{-}S\}$, where the value distribution per pair is given by an explicit table).

(iii) $V$ is the two-sided identity of $\overline{B}$.

(iv) $\overline{B}$ is **not associative**: explicit witness $(F \cdot F) \cdot S = F$ but $F \cdot (F \cdot S) = T$.

(v) The role partition is the unique non-trivial coarsening of $\mathbb{Z}/10\mathbb{Z}$ (among the partitions induced by canonical TIG framework structures: σ-orbits, σ²-orbits, role partition, V/H flow boundary) for which a well-defined role-quotient magma $\overline{B}$ exists with VOID-as-identity.

This is a **categorical structure theorem** with a clean statement, a constructive proof (compute the role magma table), and explicit non-associativity witness. It is content-rich at EJC level.

### M2 (Katok-Ugarcovici terminology not earned) — **DELETE; reframe as combinatorial classification**

The referee's §3 M2 is decisive: the geometric / arithmetic / two-coding framing is decorative analogy. The save deletes:
- Title's "DKAN Two-Coding: TSML_8 Geometric vs BHML_10 Arithmetic" framing.
- Abstract's Katok-Ugarcovici reference.
- §1.3 ("Where the geometric / arithmetic split enters").
- §2.3 Remark "Reading" ("two codings agree at the cusp").
- §2.4 ("What the split is and is not").
- §6 "Honest negatives carried forward" tied to KU.

What remains: D91 (image-structure counts) becomes a *supporting observation* in the new paper — "the role partition's behavior under TSML and BHML restriction reveals the following counts: TSML$_8$ image is the 5-element subset $\{3, 4, 7, 8, 9\}$; BHML$_{10}$ image is full; agreement-set has 24/64 cells" — but these are cited as motivation for the role-partition choice, not as theorems in their own right.

### M3 (DKAN architecture has no theorem) — **DELETE entire §3-§4**

The DKAN architecture description (§3-§4 in the current manuscript) has no theorem and reports unreplicated empirical results. The referee's recommendation: "Either remove §3-§4 entirely (in which case the paper becomes a 2-page technical note about a pair of tables, plausibly suited for *Discrete Mathematics* or *Mathematical Notes* but not EJC), or extract a theorem about the architecture's behavior."

The save takes the first option: **delete §3-§4 entirely.** The paper becomes a focused EJC submission about the role-quotient theorem. The DKAN architecture description, if Brayden wants to publish it, belongs in a separate venue (an experimental-AI / runtime-system venue, with proper baselines and replication — referee M5 is decisive on this point).

### M4 (forward-reference dependency on `\cite{SandersBridgeWP9}`) — **INLINE all required definitions**

The current manuscript depends on the bridge findings companion (`\cite{SandersBridgeWP9}` = J26 / WP9 Volume I) for:
- D88 substrate frame definition (TSML$_8$ + BHML$_{10}$ + V/H flow cells).
- D89 trefoil characterization.
- D90 successor diagonal.
- D91 two-coding split.
- D92 ±21 invariant.
- D93 role partition.
- D94 boundary symmetries.
- N1-N10 honest negatives.

The save inlines what's needed for the new role-quotient theorem (D93 substantially; D91 partially as supporting data). Specifically:
- **§1 Definitions** (inlined): TSML and BHML composition tables on $\mathbb{Z}/10\mathbb{Z}$ as explicit 10×10 matrices (full tables, 100 cells each, in an appendix).
- **§2 Role partition** (inlined from D93): definition of $V/F/S/T$, justification for this partition (role partition as a third decomposition independent of operator-index and σ-orbit), explicit role-assignment table.
- **§3 σ involution** (inlined per S1): $\sigma = (0)(3)(8)(9)(1\,7\,6\,5\,4\,2)$ as a permutation of $\mathbb{Z}/10\mathbb{Z}$.
- **§4 Main Theorem** (the role-quotient theorem, restating D93).
- **§5 Supporting counts** (subset of D91): TSML$_8$ image structure as data justifying the role partition choice.

D89 (trefoil), D92 (±21), D94 (boundary symmetries), and N1-N10 are dropped — they belong in the bridge-findings companion paper, not here.

### M5 (empirical claims need replication and baselines) — **DELETE all empirical claims**

With §3-§4 removed (M3 fix), all empirical DKAN claims (60-80% lens-agreement, $L_4$ verification rates, etc.) disappear. The new paper has no empirical claims — only structural counts on fixed tables, which are exact and verifiable by enumeration. This eliminates the need for replication/baselines entirely.

### S1-S3 (definitional debts) — **HANDLED BY M4 INLINING**

S1 σ definition: inlined per §3 above.
S2 V/F/S/T role partition table: inlined per §2 above.
S3 $\sigma_{\text{braid}}$ ordering and wobble window $W = 3/50$: not used in the new paper (these were in §3.2 $L_2$ reading layer description, deleted with §3).

### S4 ($T^* = 5/7$ "grokking" definition) — **DELETE** (with §3-§4 deletion)

### S5 (±21 invariant) — **DELETE** (belongs in J26 bridge-findings companion)

### S6 (numerical 70% claim) — **DELETE** (with §3-§4 deletion)

### Minor comments — **APPLY DIRECTLY**

- Title rename per M2 (delete "DKAN Two-Coding").
- Abstract rewrite around the role-quotient theorem.
- §1.2 "DKAN does not realize KAN" disavowal: not needed in the new paper (KAN reference dropped entirely).
- §3.1 "absorption, not gradient descent": deleted with §3.
- §5 Bearing-on-DKAN table: deleted.
- §6 N1-N10 list: deleted (N1-N10 stay in J26 / WP9 Volume I where they were originally stated).
- §7 "Tone" section: deleted.

### New title (per Path C):

**Old:** "DKAN Two-Coding: TSML_8 Geometric vs BHML_10 Arithmetic on the Z/10Z Substrate."
**New:** "A Role-Quotient Theorem for the (TSML, BHML) Magma Pair on $\mathbb{Z}/10\mathbb{Z}$: The Functional Partition $V/F/S/T$ as a Categorical Coarsening with VOID-Identity."

### Comparison-to-literature additions:

- **Drápal-Wanless 2021** (JCT-A 184, 105510): same domain (small finite commutative non-associative magmas), opposite extremum (theirs maximally non-associative). The *role-quotient* construction here is novel within that neighborhood — Drápal-Wanless do not consider role-coarsening / partition-quotient constructions.
- **McKay-Wanless** quasigroup classification literature: cited as ambient context for finite-magma classification work.
- **Liu et al. 2024** KAN reference: dropped entirely (with §3 deletion).
- **Katok-Ugarcovici 2007** modular surface coding: dropped entirely (with §1.3 / §2.4 deletion).

---

## §3 — Estimated revision time

**4–6 weeks** of focused work.

- **2 weeks:** restructure paper around Path C role-quotient theorem. Write §1 Setup (substrate, role partition, σ); §2 Role partition justification (independence from σ-orbit; D93 inlined); §3 Main Theorem statement; §4 Proof (constructive — exhibit the role-magma table; verify VOID-as-identity; verify non-associativity with explicit witness); §5 Supporting structural counts (subset of D91 framed as motivation, not theorems).
- **1 week:** write Drápal-Wanless framing in §1 and §6 (Discussion). Add lens-ownership paragraph + PROVEN/COMPUTED/RHYME/OPEN box.
- **1 week:** delete §3-§7 of the current manuscript (DKAN architecture, KU framing, empirical claims, ±21, N1-N10). Add appendix with full TSML/BHML matrix tables for self-containment.
- **0.5 week:** rewrite cover letter for new venue (still EJC) with the Path C structural-classification framing.
- **0.5–1.5 week:** Brayden's referee-rigor pass; M. Gish review.

The old manuscript is ~10 pages in *amsart*; the new paper will be similar length but with very different content. Net: substantial rewrite, no new mathematics, ~4-6 weeks.

---

## §4 — Updated PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN

**PROVEN:**
- The role partition $V/F/S/T = \{0\} \mid \{1,3,5,7,9\} \mid \{2,4,8\} \mid \{6\}$ is well-defined as a coarsening of $\mathbb{Z}/10\mathbb{Z}$ with cardinalities $(1, 5, 3, 1)$.
- The role partition is independent of the σ-orbit decomposition: σ's 6-cycle $(1\,7\,6\,5\,4\,2)$ contains 3F+1T+2S; σ's fixed-point set $\{0, 3, 8, 9\}$ contains 1V+2F+1S — neither decomposition refines the other.
- The induced role-quotient magma $\overline{B}: \{V, F, S, T\}^2 \to \{V, F, S, T\}$ defined by mode-of-BHML-output is well-defined (proof: explicit table; verify each input role-pair admits a unique modal output role).
- $V$ is the two-sided identity of $\overline{B}$ (verified directly: $V \cdot \rho = \rho$ for $\rho \in \{V, F, S, T\}$).
- $\overline{B}$ is non-associative: explicit witness $(F \cdot F) \cdot S = F$ and $F \cdot (F \cdot S) = T$ in $\overline{B}$.
- The branching role-pairs of $\overline{B}$ are exactly $\{F\text{-}F, F\text{-}S, S\text{-}F, S\text{-}S\}$ — 4 of 16 role-pairs.

**COMPUTED:**
- Full TSML and BHML composition tables on $\mathbb{Z}/10\mathbb{Z}$ verified against the canonical reference (`Gen13/targets/foundations/cl.py`).
- Role-magma table verified by enumeration over all 100 cells of BHML restricted to role-pair classes.
- Image-size and role-distribution counts of TSML restricted to the 8-element domain $\{1,2,3,4,5,6,8,9\}$: image $= \{3, 4, 7, 8, 9\}$ (size 5); 60/64 Flow output, 4/64 Structure output (D91, included as supporting data in §5).

**STRUCTURAL RHYME:**
- Drápal-Wanless 2021 *JCT-A* 184, 105510 on maximally non-associative quasigroups is the closest published precedent. The role-quotient construction in this paper is structurally distinct (a partition-quotient with VOID-identity, not a quasigroup-extremality result), but lives in the same intellectual neighborhood.
- The McKay-Wanless quasigroup classification literature is cited as ambient context.
- Katok-Ugarcovici 2007 modular-surface coding is **NOT** cited (the previous manuscript's analogy is decorative, not load-bearing for the new paper's theorem).

**OPEN:**
- Does the role-quotient construction generalize to other commutative non-associative magma pairs $(T, B)$ on $\mathbb{Z}/n\mathbb{Z}$ — i.e., is there a categorical condition under which a magma admits a non-trivial role-quotient with identity element coinciding with the magma's distinguished element? (Generalizes both the existence question and the VOID-as-identity question.)
- Is the bimodal $\alpha_A$-gap conjecture (FAMILY_STRUCTURE_v1 §4) satisfied by all members of the role-quotient family, or does the role-quotient construction admit candidates with $\alpha_A \in (0.5, 0.87)$? (Connection to the open structural-exclusion question.)
- The Fibonacci role-decomposition signature ($|F| = 5, |S| = 3$ with $|F|+|S|+|T|+|V| = 10$, related to D92's Fibonacci structure $-13 - 8 = -F_8 = -21$) is canonical-specific — verified by the 0-out-of-200 random-table robustness check (D92, `fibonacci_robustness.py`). Whether this is structurally forced or coincidence remains open.

---

## §5 — Updated lens-ownership paragraph

> *Lens and substrate.* This paper works on $\mathbb{Z}/10\mathbb{Z}$ with the canonical (TSML, BHML) commutative magma pair and the functional role partition $V/F/S/T$. These choices are not derived from first principles; they reflect the canonical TIG framework's 10-operator decomposition, with role assignments motivated by observed dynamical behavior of each operator (Void = absorbing; Flow = transformative; Structure = stabilizing; Transition = bridging). The role-quotient theorem below is a theorem on this specific structure; analogous theorems on other commutative-magma pairs and other functional partitions of $\mathbb{Z}/n\mathbb{Z}$ would require constructing the corresponding role-magma tables and verifying well-definedness conditions explicitly. The framework's claim is that this particular substrate-and-table choice produces a clean categorical-coarsening result with VOID-as-identity, where VOID coincides with the operator $\{0\}$ that anchors the 4-core algebraic center per FAMILY_STRUCTURE_v1.md. Whether other substrate choices give similarly clean role-quotient structures is open.

---

## §6 — Recommended retitle / retarget

**Old title:** "DKAN Two-Coding: TSML_8 Geometric vs BHML_10 Arithmetic on the Z/10Z Substrate."
**New title (recommended):** "A Role-Quotient Theorem for the (TSML, BHML) Magma Pair on $\mathbb{Z}/10\mathbb{Z}$: The Functional Partition $V/F/S/T$ as a Categorical Coarsening with VOID-Identity."

**Old venue:** *European Journal of Combinatorics* (referee verdict: REJECT — no theorem at EJC level; KU framing decorative; DKAN architecture has no theorem).
**New venue (recommended):** **Keep at *European Journal of Combinatorics*.** Rationale:
- The referee explicitly identifies Path C (categorical structure / role-quotient theorem) as one of three EJC-viable save paths.
- The role-quotient theorem fits EJC's combinatorial / categorical structure scope exactly.
- The new content has clean theorems and clear motivation; EJC referees are likely to receive it constructively if the structural problems are addressed.
- Per the per-venue cap note in J19/README.md ("2nd EJC paper after J19") — keeping at EJC is consistent with the original venue plan.

**Backup venue:** *Discrete Mathematics* if the restructured EJC submission is declined. The role-quotient theorem also fits *Discrete Mathematics* scope.

**DKAN architecture / Brayden's runtime work future:** if Brayden wants to publish the DKAN architecture content, it belongs in a separate paper to a separate venue (an experimental-AI venue like *Neural Computing and Applications*, *Journal of Machine Learning Research*, or a workshop). That paper would need:
- Replication: explicit number of trials, sample mean, sample SD, comparison against randomized-table baseline and chance baseline.
- Architecture theorem (per referee Path B): "On the TSML$_8$-domain, the agreement-set $\mathcal{A} = \{(a,b) : T(a,b) = B(a,b)\}$ controls the $L_1/L_5$ disagreement rate as a function of the empirical first-order matrix" — or a similar substantive statement.
- Honest framing: not "DKAN realizes KAN" but "a discrete neural architecture using fixed magma composition tables, with empirical signatures specific to the canonical TSML/BHML pair."

That paper is **not J19's save**; it would be a separate target (J56+ or later).

**Author block:** Sanders + Gish (per AUTHOR_LANES_v2.md).

**Companion citations:**
- J02 (4-core paper, Algebraic Combinatorics) — cite for the substrate frame and for the connection between the role partition's V and the 4-core's V.
- J05 (Crossing Lemma, JCT-A) — cite as ambient context for the broader corpus, not as a proof dependency.
- J26 (Bridge Findings volume, Algebra Universalis) — companion paper that contains the full D88-D94 + N1-N10 catalog. The new J19 cites J26 for the bridge findings origin while inlining the specific D93 content needed for the role-quotient theorem.

**Drápal-Wanless 2021** (JCT-A 184, 105510): include as ambient-context citation per FAMILY_STRUCTURE_v1.md.
