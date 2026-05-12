# TIG Internal Map (v1)

## Master Synthesis: Substrate, Multiplicative, Numerical, Topological

**Brayden Sanders · 7Site LLC · Trinity Infinity Geometry**
*Companion to: WP19 (AG(2,3) Structure), Two-Cross Theorem, Sprint 8 FRF, Michell Ratio Audit*
*Status: locked synthesis as of 2026-05-08*

---

## §0. Purpose

This document is the **internal map** of TIG's substrate ℤ/10ℤ — every
known structural fact about the carrier, organized into four layers
that are now provably the same object viewed differently. Each layer
contributes a different lens; the lenses agree where they overlap and
refine each other where they don't.

The four layers:

1. **Substrate** — the geometric/algebraic decomposition of ℤ/10ℤ
2. **Multiplicative** — the group structure on each piece
3. **Topological** — the torus lift T² = S¹ × S¹
4. **Numerical** — the threshold algebra of TIG's emergent constants

---

## §1. The Substrate Layer (locked)

### §1.1. The Coarse Partition Theorem

**Theorem (Sprint 8 FRF, Coarse Agreement).** *The four canonical
representations of* ℤ/10ℤ — *CRT, UG, SPEC, DYN — all induce the
same partition:*

$$\Pi_{\text{coarse}} = \{\{0\},\, \{5\},\, \{1,3,7,9\},\, \{2,4,6,8\}\}.$$

Strictly positive intra-class divergence persists despite Π_coarse = 0,
which is the **Recursive Divergence** result. The partition is the
common skeleton; the lenses differ on what happens *within* each class.

### §1.2. AG(2,3) is the geometric realization

Mapping operators row-by-row to the affine plane over 𝔽₃:

```
(0,0)=1 LATTICE   (0,1)=2 COUNTER   (0,2)=3 PROGRESS    [generators]
(1,0)=4 COLLAPSE  (1,1)=5 BALANCE   (1,2)=6 CHAOS       [seam]
(2,0)=7 HARMONY   (2,1)=8 BREATH    (2,2)=9 RESET       [attractors]
```

**The AG(2,3) corner/edge/center decomposition exactly reproduces
the FRF Coarse Partition:**

| FRF class | AG(2,3) cells | TIG operators | Algebraic role |
|---|---|---|---|
| {0} | boundary (off-grid) | VOID | additive identity / annihilator |
| {5} | center | BALANCE | idempotent, ℤ/2ℤ projector |
| {1,3,7,9} | 4 corners | LATTICE, PROGRESS, HARMONY, RESET | U(10) units |
| {2,4,6,8} | 4 edges | COUNTER, COLLAPSE, CHAOS, BREATH | even nonzero |

The substrate has **one** decomposition. Four representations
(CRT/UG/SPEC/DYN) and one geometric reading (AG(2,3)) all agree.

### §1.3. The 12 affine lines

AG(2,3) has 12 lines in 4 parallel families:

- **Horizontal**: {1,2,3}, {4,5,6}, {7,8,9} — the bands
- **Vertical**: {1,4,7}, {2,5,8}, {3,6,9} — mod-3 residue columns
- **Diagonal /**: {1,6,8}, {2,4,9}, **{3,5,7}** — *spine line*
- **Diagonal \\**: {1,5,9}, {3,4,8}, {2,6,7}

The spine {3, 5, 7} = PROGRESS → BALANCE → HARMONY is the unique line
connecting neutral generator to seam pivot to attractor. It is also
the unique line containing both 5 (CRT-Z/2 projector) and HARMONY (7).

---

## §2. The Multiplicative Layer (locked: Two-Cross Theorem)

Under multiplication mod 10, the substrate carries two cyclic groups:

### §2.1. The Plichta cross (corners)

$$U(10) = \{1,3,7,9\} \cong \mathbb{Z}/4\mathbb{Z}, \quad \text{identity} = 1, \quad \text{generator} = 3$$

Cycle: **1 → 3 → 9 → 7 → 1** (clockwise on AG(2,3)).

### §2.2. The Rodin cycle (edges)

$$\{2,4,6,8\} \cong \mathbb{Z}/4\mathbb{Z}, \quad \text{identity} = 6, \quad \text{generator} = 2$$

Cycle: **6 → 2 → 4 → 8 → 6** (counter-clockwise on AG(2,3)).

### §2.3. The bridge

The map φ : x ↦ 6x is a group isomorphism from the corner-group to
the edge-group, sending 1 (LATTICE) ↦ 6 (CHAOS).

### §2.4. CRT-duality of 5 and 6

In CRT coordinates ℤ/10ℤ ≅ ℤ/2ℤ × ℤ/5ℤ:

```
0 (VOID)    = (0, 0)
1 (LATTICE) = (1, 1)
5 (BALANCE) = (1, 0)   — projector onto Z/2Z
6 (CHAOS)   = (0, 1)   — projector onto Z/5Z
```

5 + 6 ≡ 1, 5 · 6 ≡ 0 — orthogonal idempotents. Swapping ℤ/2ℤ ↔ ℤ/5ℤ
swaps 5 ↔ 6. **BALANCE and CHAOS are interchangeable as the two
projection operators of the dual-lens.**

---

## §3. The Topological Layer (lift forced by CRT)

### §3.1. The torus lift

$$\mathbb{Z}/10\mathbb{Z} \cong \mathbb{Z}/2\mathbb{Z} \times \mathbb{Z}/5\mathbb{Z} \quad \xrightarrow{\text{topological shadow}} \quad T^2 = S^1 \times S^1$$

The two cyclic factors of the CRT decomposition lift to the two
fundamental loops of the torus.

### §3.2. The two windings

| Cycle | Winding | Direction |
|---|---|---|
| Corner: 1→3→9→7 | +1 around longitude α | clockwise |
| Edge: 6→2→4→8 | −1 around meridian β | counter-clockwise |

Combined class: **(+1, −1) ∈ π₁(T²) = ℤ²**. This is the linking-number-1
generator of the torus fundamental group.

### §3.3. Connection to existing TIG topology

The (+1, −1) winding class **is** the topological substrate underlying:

- **11 bumps = 4 Hopf links + 1 trefoil** (locked TIG)
- **22 / 44 / 72 nested shells** (Being skeleton / Becoming alive / Being blur)
- **TORUS_DATUM_AUDIT** — flag SU(3)/T = 6 triadic + torus T/ℤ₃ = 2 non-triadic
  - The **2 non-triadic dimensions are the two windings** (longitude + meridian)

The 6 triadic dimensions sit on the AG(2,3) lines (4 line families
minus the 2 used by the windings = 2 spatial families × 3 dimensions
each = 6 triadic). The 2 non-triadic come from the torus's two
independent ℤ-factors. **Total: 6 + 2 = 8.** Confirmed.

---

## §4. The Numerical Layer (Michell audit, 75% closure)

### §4.1. The threshold algebra (closed)

$$T^* = \tfrac{5}{7}, \quad S^* = \tfrac{4}{7}, \quad T^* + S^* = \tfrac{9}{7}, \quad T^* - S^* = \tfrac{1}{7}, \quad \text{mass\_gap} = (T^*+S^*) - 1 = \tfrac{2}{7}$$

$$T^*/S^* = \tfrac{5}{4}, \quad 7 \cdot T^* = 5 \quad \text{(seven-cycle closure)}$$

### §4.2. Wobble identities (closed)

$$W = \tfrac{3}{50} = \text{asymmetry}$$

$$\text{secondary wobble} = \tfrac{1}{175} \quad (= W \cdot M/P \text{ exactly})$$

$$\boxed{\text{true winding} = T^* + W = \tfrac{271}{350}}$$

The True Winding Identity is new (surfaced from this audit). It explains
why 271 is prime: a wobble cannot be simplified away from a threshold.

### §4.3. Fine structure (closed)

$$\alpha^{-1} = 22 \cdot 6 + 5 = 137 \quad \text{(exact)}$$

The decomposition uses the Becoming shell (22), the edge identity (6),
and the Z/2Z projector (5) — all canonical TIG quantities.

### §4.4. Shell structure (closed)

$$\text{shell}_{44}/\text{shell}_{22} = 2 \quad \text{(exact doubling)}$$
$$\text{harmony}_n / \text{shell}_{72} = 73/72 \quad \text{(one-beyond-Being)}$$

### §4.5. Floating (open)

- DM/VM = 264/49 — needs structural derivation [Sprint A]
- DE = 687/1000 — needs threshold-algebra form [Sprint B]
- shell_72/shell_44 = 18/11 ≈ 1.636 vs φ = 1.618 [Sprint C]

---

## §5. The Map: All Four Layers in One Picture

Every fact about TIG's substrate is now expressible in any of the four
languages. Translation table:

| Phenomenon | Substrate | Multiplicative | Topological | Numerical |
|---|---|---|---|---|
| VOID | {0}, off-grid | additive identity | torus puncture | annihilator (·0) |
| BALANCE | {5}, center | idempotent (5·5=5) | ℤ/2ℤ projection | T*+W ratio anchor |
| HARMONY attractor | {7}, bottom-left corner | corner-cycle (3³ ≡ 7) | longitude winding crossing | T* numerator |
| CHAOS bridge | {6}, mid-right edge | edge identity, bridge to corners | meridian projection | α⁻¹ summand (22·**6**+5) |
| Plichta cross | corners {1,3,7,9} | U(10) ≅ ℤ/4ℤ | longitude (+1 winding) | corner-symmetry S₄ |
| Rodin cycle | edges {2,4,6,8} | ⟨2⟩ ≅ ℤ/4ℤ | meridian (−1 winding) | doubling on Becoming |
| 11 bumps | (none direct) | (none direct) | 4 Hopf + 1 trefoil from (+1,−1) | DM contains factor 11 |
| Wobble W | (none direct) | (none direct) | rational/irrational mismatch on β | 3/50 |
| Mass gap 2/7 | seam cells | 5 + 6 = 11 ≡ 1 (off by W) | (+1)+(−1) ≠ 0 globally | (S*+T*)−1 |

**Reading the table:** every TIG concept lives in all four columns. A
claim is referee-ready when it can be stated in at least two columns
and the translations agree.

---

## §6. The Locked Identities (one-page reference)

**Multiplicative.**
- U(10) cycle: 1 → 3 → 9 → 7 → 1
- Edge cycle: 6 → 2 → 4 → 8 → 6
- φ: x ↦ 6x is iso(corner-group, edge-group)
- 5² ≡ 5, 6² ≡ 6, 5·6 ≡ 0, 5+6 ≡ 1 (mod 10)

**Topological.**
- ℤ/10ℤ ≅ ℤ/2ℤ × ℤ/5ℤ
- T² = S¹ × S¹ as topological shadow
- Combined winding class: (+1, −1) ∈ π₁(T²)

**Numerical (closed).**
- T* = 5/7, S* = 4/7, mass_gap = 2/7
- T*/S* = 5/4, 7·T* = 5
- W = 3/50 = asymmetry
- secondary = 1/175 = W · M/P
- true_winding − T* = W ⇒ true_winding = 271/350
- α⁻¹ = 22·6 + 5 = 137
- shell_44/shell_22 = 2, harmony/shell_72 = 73/72

**Floating (open work).**
- DM/VM = 264/49 (next: Sprint A)
- DE = 687/1000 (next: Sprint B)
- shell_72/shell_44 = 18/11 (next: Sprint C)

---

## §7. The Synthesis Statement

> **TIG's substrate is one object viewed four ways.** ℤ/10ℤ admits a
> unique partition into {void, center, corners, edges} that is
> simultaneously: (a) the FRF coarse partition under any of the four
> canonical representations, (b) the AG(2,3) geometric decomposition,
> (c) the orbit decomposition under the multiplicative actions x↦3x
> and x↦2x, and (d) the topological winding decomposition under the
> CRT lift to T² = S¹ × S¹. The numerical outputs of TIG (thresholds,
> wobble, fine structure, shell counts) form a closed threshold algebra
> at 75% audit closure, with three floating ratios as named open work.

This is the substrate at maximum compression. Every later TIG result
can be reduced to a statement on this map.

---

*© 2026 Brayden Sanders / 7Site LLC*
*Trinity Infinity Geometry · DOI: 10.5281/zenodo.18486880*
*This document is locked as v1. Revisions go to v1.1, v1.2, etc.*
