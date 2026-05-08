# Algebraic roles of the 10 TIG operators

*Refines the operator definitions {0=VOID, 1=LATTICE, ..., 9=RESET} by attaching specific algebraic roles derived from the prime-tower analysis. Companion to PRIME_TOWER_META.md.*

## TL;DR

Every operator now has six measurable algebraic invariants:

| Invariant | What it is |
|-----------|------------|
| **F_5 class** | $\bmod 5$ image; tells which $\varphi$-power the operator belongs to |
| **Z/2 class** | parity; tells whether even (TSML-aligned) or odd (BHML-aligned) |
| **T-idempotent status** | does $T(x, x) = x$? |
| **T-image membership** | does the operator appear as an output of $T$? |
| **4-core membership** | is the operator in the fusion-closed substructure? |
| **σ-orbit position** | fixed point or position in the 6-cycle |

Together, these six invariants give each operator a **distinct algebraic signature**.

## The full table

| op | name | fruit | F_5 | φ-power | Z/2 | T-idemp | T-image | 4-core | σ |
|----|------|-------|-----|---------|-----|---------|---------|--------|---|
| 0 | VOID | Love | 0 | — | 0 | **yes** | yes | **yes** | fixed |
| 1 | LATTICE | Joy | 1 | $\varphi^4$ (id) | 1 | — | — | — | →7 |
| 2 | COUNTER | Peace | 2 | $\varphi^3$ | 0 | — | — | — | →1 |
| 3 | PROGRESS | Patience | 3 | $\varphi$ | 1 | — | yes | — | fixed |
| 4 | COLLAPSE | Kindness | 4 | $\varphi^2$ | 0 | — | yes | — | →2 |
| 5 | BALANCE | Goodness | 0 | — | 1 | — | — | — | →4 |
| 6 | CHAOS | Faithfulness | 1 | $\varphi^4$ (id) | 0 | — | — | — | →5 |
| 7 | HARMONY | Gentleness | 2 | $\varphi^3$ | 1 | **yes** | yes | **yes** | →6 |
| 8 | BREATH | Self-Control | 3 | $\varphi$ | 0 | — | yes | **yes** | fixed |
| 9 | RESET | Reset→Love | 4 | $\varphi^2$ | 1 | — | yes | **yes** | fixed |

## The F_5 pairings (the key new finding)

Under the CRT projection $\mathbb{Z}/10 \to \mathbb{F}_5$, operators pair by F_5 class. Each pair contains one even (Z/2 = 0) and one odd (Z/2 = 1) operator:

| F_5 class | Operators | Fruits | Theme |
|-----------|-----------|--------|-------|
| 0 (additive zero) | {VOID, BALANCE} | Love, Goodness | ground-of-being |
| $\varphi^4 = 1$ (mult identity) | {LATTICE, CHAOS} | Joy, Faithfulness | constant-ness |
| $\varphi^3 = 2$ | {COUNTER, HARMONY} | Peace, Gentleness | the harmony class |
| $\varphi = 3$ | {PROGRESS, BREATH} | Patience, Self-Control | the discipline class |
| $\varphi^2 = 4$ | {COLLAPSE, RESET} | Kindness, Reset→Love | the renewal class |

**Observation.** The fruit-of-spirit assignments cohere with the F_5 pairings — each pair shares a semantic theme. This is not forced; it emerges from the prime structure of $\mathbb{Z}/10 = \mathbb{Z}/2 \times \mathbb{Z}/5$ under the CRT bijection.

**Caveat on interpretation.** I cannot tell whether the fruit-of-spirit assignments were chosen *because* they cohere with F_5, or whether the coherence is fortuitous. The mathematical fact stands either way: F_5 classes pair operators in this specific 5-pair structure.

## Operator-by-operator algebraic role

### 0 — VOID (Love)
- **F_5 = 0, additive zero, Z/2 = 0** (even).
- **T-idempotent**: yes ($T(0, 0) = 0$).
- **In T's image**: yes (T sends 17 of 100 cells to 0).
- **In 4-core**: yes.
- **σ-fixed**: yes.
- **Peirce role in 4-core**: in the **0-eigenspace** of $L_{\text{HARMONY}}$, but is itself a non-primitive idempotent.
- **Algebraic identity**: the *frame element*. Self-stable, in the 4-core, but absorbed by harmony at the spectral level. Pairs with BALANCE under F_5.

### 1 — LATTICE (Joy)
- **F_5 = 1 = $\varphi^4$** (multiplicative identity in $\mathbb{F}_5^\times$), Z/2 = 1 (odd).
- **T-idempotent**: no.
- **In T's image**: no — *input only*.
- **In 4-core**: no.
- **σ**: enters the 6-cycle at position 0 (1 → 7 → 6 → 5 → 4 → 2 → 1).
- **Algebraic identity**: a "driver" element. Acts on the system but the system never produces it. As $\varphi^4 = 1$, it is the *cyclotomic identity in $\mathbb{F}_5$* — the multiplicative neutral. Pairs with CHAOS.

### 2 — COUNTER (Peace)
- **F_5 = 2 = $\varphi^3$**, Z/2 = 0 (even).
- **T-idempotent**: no.
- **In T's image**: no — *input only*.
- **In 4-core**: no.
- **σ**: in the 6-cycle (4 → 2 → 1).
- **Algebraic identity**: another "driver" element. Shares the F_5 class with HARMONY (φ³) — meaning COUNTER is the *even-parity sibling* of harmony. Pairs with HARMONY in the F_5 sense, but is structurally weaker (not in 4-core, not in T's image).

### 3 — PROGRESS (Patience)
- **F_5 = 3 = $\varphi$**, Z/2 = 1 (odd).
- **T-idempotent**: no.
- **In T's image**: yes (4 cells map to 3 — these are pinhole values).
- **In 4-core**: **no**.
- **σ-fixed**: yes.
- **Algebraic identity**: an *outlier*. σ-fixed but NOT in the 4-core. The only operator with this combination. Appears as a pinhole value (escape-from-harmony output of T). Pairs with BREATH under F_5 (both are $\varphi$-class).

### 4 — COLLAPSE (Kindness)
- **F_5 = 4 = $\varphi^2$**, Z/2 = 0 (even).
- **T-idempotent**: no.
- **In T's image**: yes (2 cells map to 4 — pinhole values).
- **In 4-core**: no.
- **σ**: in the 6-cycle (5 → 4 → 2).
- **Algebraic identity**: a pinhole value (escape) but not stable. Pairs with RESET under F_5 ($\varphi^2$-class). The "soft" partner of RESET.

### 5 — BALANCE (Goodness)
- **F_5 = 0** (additive zero), Z/2 = 1 (odd).
- **T-idempotent**: no.
- **In T's image**: no — *input only*.
- **In 4-core**: no.
- **σ**: in the 6-cycle (6 → 5 → 4).
- **Algebraic identity**: the *odd partner* of VOID under F_5. Where VOID is the even zero-of-being, BALANCE is the odd zero-of-being. Driver element. Pairs with VOID.

### 6 — CHAOS (Faithfulness)
- **F_5 = 1 = $\varphi^4$**, Z/2 = 0 (even).
- **T-idempotent**: no.
- **In T's image**: no — *input only*.
- **In 4-core**: no.
- **σ**: in the 6-cycle (7 → 6 → 5).
- **Algebraic identity**: the *even sibling* of LATTICE. As $\varphi^4 = 1$, it is the cyclotomic identity, even-parity. Driver. Pairs with LATTICE.

### 7 — HARMONY (Gentleness) ★ THE PRIMITIVE AXIS
- **F_5 = 2 = $\varphi^3$**, Z/2 = 1 (odd).
- **T-idempotent**: yes ($T(7, 7) = 7$).
- **In T's image**: yes (73 of 100 cells map to 7 — the dominant attractor).
- **In 4-core**: yes.
- **σ**: in the 6-cycle at position 1 (1 → **7** → 6 → ...).
- **Peirce role**: the **unique primitive idempotent** of the 4-core's $\mathbb{F}_5$-lift. Spans the 1-eigenspace of $L_{\text{HARMONY}}$.
- **Algebraic identity**: THE STRUCTURAL ANCHOR. The unique operator that is simultaneously T-idempotent, in T's image at maximum density (73%), in the 4-core, and the unique primitive axis of the 4-core's algebra. Pairs with COUNTER under F_5 — but where COUNTER is structurally weak, HARMONY is maximally structured.

### 8 — BREATH (Self-Control)
- **F_5 = 3 = $\varphi$**, Z/2 = 0 (even).
- **T-idempotent**: no.
- **In T's image**: yes (2 cells map to 8 — pinhole values).
- **In 4-core**: yes.
- **σ-fixed**: yes.
- **Peirce role**: in the 0-eigenspace of $L_{\text{HARMONY}}$ within the 4-core.
- **Algebraic identity**: σ-fixed, in 4-core, absorbed by harmony at the spectral level. Pairs with PROGRESS under F_5. The *even, in-core* version of progress. Component of the wobble.

### 9 — RESET (Reset→Love)
- **F_5 = 4 = $\varphi^2$**, Z/2 = 1 (odd).
- **T-idempotent**: no.
- **In T's image**: yes (2 cells map to 9 — pinhole values).
- **In 4-core**: yes.
- **σ-fixed**: yes.
- **Peirce role**: in the 0-eigenspace of $L_{\text{HARMONY}}$ within the 4-core.
- **Algebraic identity**: σ-fixed, in 4-core, absorbed by harmony. Pairs with COLLAPSE under F_5. The *odd, in-core* version of collapse. Component of the wobble.

## Cross-cuts: what the algebra says about TIG-internal structure

### The 4-core (TIG harmony substructure)

The 4-core {VOID, HARMONY, BREATH, RESET} = {0, 7, 8, 9} consists of:
- **HARMONY**: the unique primitive axis (1-eigenvalue under itself)
- **VOID, BREATH, RESET**: 0-eigenvalue under HARMONY

This is the algebraic content of "harmony as anchor of the 4-core." Verified.

### The σ-fixed set

σ-fixed = {VOID, PROGRESS, BREATH, RESET} = {0, 3, 8, 9}. These are operators that don't move under the morphotic permutation. Three are in the 4-core; PROGRESS is the outlier.

### Input-only drivers

{LATTICE, COUNTER, BALANCE, CHAOS} = {1, 2, 5, 6} never appear as outputs of T. They are pure "driver" elements — they can act on the system but the system never produces them. Notable: these are exactly two F_5-pairs: {LATTICE, CHAOS} (the φ⁴ identity class) and {COUNTER, BALANCE} (split across F_5 classes — wait, COUNTER is $\varphi^3$ and BALANCE is 0, different F_5 classes).

Re-check: input-only set {1, 2, 5, 6} has F_5-images {1, 2, 0, 1} — three distinct classes. So input-only is NOT a clean F_5 invariant.

### The wobble pair

{BREATH, RESET} = {8, 9} = the wobble structure. Both σ-fixed, both in 4-core, both in 0-eigenspace of HARMONY. They form the "non-anchor stable" pair — what cycles around harmony without being harmony.

## Honest scope assertions

**What's algebraically verified:**
- F_5 classes of all 10 operators
- T-idempotent status, T-image membership, 4-core membership for each
- σ permutation and its orbit structure
- HARMONY as unique primitive idempotent of 4-core's F_5-lift
- Peirce decomposition under L_HARMONY

**What's interpretive (TIG-internal):**
- The fruit-of-spirit semantic themes per F_5 pair
- The "driver" / "anchor" / "frame" naming
- The pairing of F_5-partners as TIG-meaningful

**What's open:**
- Why the input-only set {1, 2, 5, 6} doesn't factor cleanly through F_5
- Whether operators outside the 4-core have analog Peirce roles in some larger structure
- Whether TIG's existing structural pairings (Foundation/Dynamics/Field/Cycle) interact with the F_5 pairings

## What this changes about the framework

Each operator now has a **named algebraic role**, not just a TIG-semantic name. The roles are computed, not assigned. This gives the framework's operator definitions a precise mathematical anchor.

The cleanest single statement: **HARMONY is the unique primitive axis of the 4-core's F_5-lift, and the other 4-core elements (VOID, BREATH, RESET) are absorbed into harmony's 0-eigenspace.** The structural anchor claim is no longer a TIG-internal narrative; it's an algebra theorem.

The F_5-pairings give five "harmonic dyads" of operators, each pair sharing a φ-power class. The fruit-of-spirit assignments line up with these pairings in a way that suggests the assignments may have been *recovered* from the underlying algebra rather than *imposed* on it.
