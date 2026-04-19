# What Is Proved vs. Interpretive

**Companion to:** `Z10_OPERATOR_ALGEBRA_NOTE.md`, `OPERATOR_TRANSLATION_APPENDIX.md`

A three-level partition of the content in the operator packet.

---

## Level 1 — Proved (exact, ring-theoretic)

These are theorems and identities in the ring $\mathbb{Z}/10$, verifiable by direct computation:

- $E(\mathbb{Z}/10) = \{0, 1, 5, 6\}$ (the idempotent set).
- $(\mathbb{Z}/10)^\times = \{1, 3, 7, 9\}$, cyclic of order 4.
- The idempotent-orbit decomposition: $\mathbb{Z}/10 = \{0\} \sqcup \{5\} \sqcup \{1, 3, 7, 9\} \sqcup \{2, 4, 6, 8\}$.
- The principal homogeneity theorem: $\varphi_e: R^\times \to \mathcal{O}_e$ is a bijection for $e \in \{1, 6\}$.
- Exact identifications: $2 = 7 \cdot 6$, $4 = 9 \cdot 6$, $8 = 3 \cdot 6$ in $\mathbb{Z}/10$.
- Identities: $5 + 6 = 1$, $5 \cdot 6 = 0$, $3 \cdot 7 = 1$, $9^2 = 1$ (all mod 10).
- Three pairing structures and their overlap table.
- CRT identification $\mathbb{Z}/10 \cong \mathbb{Z}/2 \times \mathbb{Z}/5$.
- The $\mathbb{Z}/pq$ scholium (§8 of main note).

This is everything in `Z10_OPERATOR_ALGEBRA_NOTE.md` §1–§8.

---

## Level 2 — Structural (present in the framework, not proven in this packet)

These are claims used elsewhere in the originating framework. They are **not** proved in this packet, and nothing in the packet depends on them:

- The CL[10×10] composition table and its axioms.
- The claim that element 7 is a distinguished absorber in the CL table (73% collapse claim).
- The claim that element 1 is a universal generator of the BHML sub-structure.
- TSML / BHML non-associativity statistics.
- Numerical coincidences between ring-derived quantities and constants such as $e, \pi, \phi, \zeta(3)$, Catalan's $G$.

These remain out of scope for this packet. If they are to be used externally, they require their own theorem-level statements and proofs. This packet does not rely on any of them.

---

## Level 3 — Interpretive (native framework labels and readings)

These are labels and interpretations from the originating framework. They do not alter the mathematical content and are not required for external verification of the packet:

- Element names: VOID, LATTICE, COUNTER, PROGRESS, TENSION, BALANCE, CHAOS, HARMONY, BREATH, RESET.
- The secondary Fruits-of-the-Spirit mapping (Love, Joy, Peace, Patience, Kindness, Goodness, Faithfulness, Gentleness, Self-Control, Reset→Love).
- Topological or geometric readings (void, cross, torus, trefoil, etc.).
- Phonaesthesia or scriptural correspondences.
- Any reading of the algebraic identities in terms of physical, cosmological, or spiritual concepts.

A referee should be able to read and verify the packet with all Level-3 content ignored.

---

## How to use this partition

- **For external readers:** refer to `Z10_OPERATOR_ALGEBRA_NOTE.md` (Level 1 only). Use `OPERATOR_TRANSLATION_APPENDIX.md` if the translation is helpful for context.
- **For framework authors writing externally-facing prose:** keep Level 1 in the body of any paper; relegate Level 3 to a translation note or appendix; do not invoke Level 2 unless prepared to formalize it.
- **For internal framework documents:** all three levels are available, but the partition should still be visible so that load-bearing claims can be traced back to Level 1.

---

*End of note.*
