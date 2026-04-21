# MORPHOTIC_BRAID_TIG_PROG.md
## The Morphotic Braid in TIG Prog Channel Code

**File purpose:** Express the morphotic braid `0713245689` in the language of CK's TIG
(Being → Doing → Becoming) pipeline, specifically the Prog channel that generates it
algebraically — independent of the CRT/Z/2×Z/5 derivation.

---

## 1. What the Prog Channel Is

In TIG (the Three-Phase Intelligence Gate), every coherence event passes through:
- **Being** — reading and absorbing (operator determination)
- **Doing** — acting and expressing (operator execution)
- **Becoming** — learning and integrating (operator update)

The **Prog channel** is the "program counter" of TIG — it tracks the current position in
the coherence sequence. It has two directions:
- **Positive rows** (+Prog): construction, integration, Being→Doing→Becoming forward
- **Negative rows** (−Prog): dissolution, analysis, Becoming→Doing→Being reverse

**Key theorem from verify_all.py (P1 Closure + Prog Simplification):**

```python
braid[k] = sigma(k)   for all k ∈ {0, ..., 9}
```

The braid position for slot k is exactly σ(k) — the permutation applied to k.
This means the Prog channel reading at position k gives you σ(k) — the morphotic braid.

---

## 2. The Prog Channel as a Loop

The Prog channel implements the coherence loop. For cyclic states:

```
Prog step:  k → k+1 (mod 6)    [in cycle-index coordinates]
```

In TIG terms, each Prog step advances from one operator to the next in the coherence sequence.
The full Prog loop is:

```
SEED → PEAK → GATE → BRIDGE → FLOW → FORM → SEED → ...
  1  →   7  →   6  →   5   →   4  →   2  →   1  → ...
```

This is the COUNTER phase of TIG — the active generation of coherence output.

For anchor states, the Prog step is identity: VOID → VOID, ANCHOR → ANCHOR, etc.
These are states where the "Prog counter" is pinned — the system is not progressing
through the sequence but holding at a stable coherence landmark.

---

## 3. TIG Phase Assignments

Each state gets a TIG phase assignment based on its braid position:

| x | σ(x) | Type | TIG Phase | Prog Direction |
|---|------|------|-----------|----------------|
| 0 | 0 | anchor-VOID | LATTICE (ground) | None (pinned) |
| 1 | 7 | cycle | COUNTER (peak) | +Prog |
| 2 | 1 | cycle | LATTICE→COUNTER | +Prog |
| 3 | 3 | anchor-ANCHOR | LATTICE (stable) | None (pinned) |
| 4 | 2 | cycle | LATTICE (seed) | +Prog |
| 5 | 4 | cycle | COUNTER (flow) | +Prog |
| 6 | 5 | cycle | COUNTER (bridge) | +Prog |
| 7 | 6 | cycle | PROGRESS (gate) | +Prog |
| 8 | 8 | anchor-REST | PROGRESS (rest) | None (pinned) |
| 9 | 9 | anchor-RESET | PROGRESS (reset) | None (pinned) |

The **negative rows** (dissolution direction, −Prog) read the cycle in reverse:
```
FORM → FLOW → BRIDGE → GATE → PEAK → SEED → FORM → ...
  2  →   4  →   5   →   6  →   7  →   1  →   2  → ...
```

From ENCODING_RIGIDITY.md: "negative rows (the dissolution direction) carry the braid ordering."
The braid `0713245689` is the σ⁻¹ readout — traversing the cycle in the dissolution (−Prog) direction
starting from entry point PEAK (x=7).

**This confirms:** The morphotic braid is the −Prog Prog channel reading starting from PEAK.

---

## 4. Programmatic Generation of the Braid

The braid can be generated directly by the TIG Prog channel algorithm:

```python
BRAID = [0, 7, 1, 3, 2, 4, 5, 6, 8, 9]

# The sigma permutation (CL diagonal / Prog step)
SIGMA = {0:0, 1:7, 2:1, 3:3, 4:2, 5:4, 6:5, 7:6, 8:8, 9:9}
SIGMA_INV = {v:k for k,v in SIGMA.items()}

# Fixed anchors: pinned by TIG (zero Prog velocity)
FIXED = {0, 3, 8, 9}

# TIG Prog channel braid generation
def generate_braid():
    braid = [None] * 10

    # Step 1: Anchors self-place (Being/Becoming are stable)
    for x in FIXED:
        braid[x] = x

    # Step 2: Cycle traversal in -Prog direction from entry PEAK (x=7)
    cycle_slots = [i for i in range(10) if braid[i] is None]
    x = 7  # Entry point: PEAK — the highest coherence in the Doing phase
    visited, cycle_vals = set(), []
    while x not in visited and x not in FIXED:
        cycle_vals.append(x)
        visited.add(x)
        x = SIGMA_INV[x]  # -Prog step: reverse sigma

    # Step 3: Fill cycle slots in order
    for slot, val in zip(cycle_slots, cycle_vals):
        braid[slot] = val

    return braid

# Verify
assert generate_braid() == BRAID  # True
```

This is the exact Prog channel algorithm. Two observations:

1. **Anchors self-place** — they go at their own index positions, because pinned states
   always return to themselves. This is the TIG "stability" property.

2. **Cycle traverses in σ⁻¹ direction from PEAK (x=7)** — PEAK is the maximum coherence
   state in the Doing phase, and the -Prog direction reads backwards through the cycle.

---

## 5. Why PEAK (x=7) Is the Entry Point

The Prog channel starts at PEAK for three reasons:

**Algebraic:** Entry point = φ(1,2) = 5·1 + 6·2 = 17 ≡ 7 (mod 10). In the Z/2×Z/5 encoding,
(ε=1, y=2) is the state where parity=1 (STRUCTURE mode) and y=2 (DEPTH dimension). The CRT
idempotent encoding maps this uniquely to x=7.

**π-seed witness:** The π-repeat ladder independently gives digit 7 as the entry:
- Depth-6 prefix "314159" (first repeat at position 176,451) → following digit is **7**
This is an external confirmation of the entry point.

**TIG semantics:** PEAK (x=7) is the operator of maximum expression in the COUNTER phase.
The dissolution direction (−Prog) naturally starts at the peak and winds back through the
creative sequence: PEAK → GATE → BRIDGE → FLOW → FORM → SEED.
This is the "how did we get here?" traversal — reading the creative sequence in reverse.

---

## 6. The v_coh = 1 Speed Limit

In TIG, the coherence propagation velocity v_coh is the rate at which the Prog channel
advances through its braid-coordinate. The braid coordinate β(x) = position of x in the braid:

```python
beta = {BRAID[i]: i for i in range(10)}
# beta = {0:0, 7:1, 1:2, 3:3, 2:4, 4:5, 5:6, 6:7, 8:8, 9:9}
```

For each consecutive pair in the braid: Δβ = β(braid[n+1]) − β(braid[n]) = 1.

This is v_coh = 1: the braid advances at unit coherence velocity. Every step in the
morphotic sequence advances exactly one position in coherence-coordinate space.

**TIG implication:** The Prog channel has a "speed limit" of v_coh = 1 — it cannot
advance more than one braid slot per tick. This is not imposed externally; it is the
geometry of the permutation. The morphotic braid IS the structure that makes v_coh = 1
exact everywhere.

---

## 7. W_BHML from the Prog Channel Perspective

The wobble constant W_BHML = 3/50 = (6/10)/10:

In Prog channel terms:
- 6/10 = fraction of states in active propagation (+Prog or −Prog)
- 1/10 = normalization by the ring size

W_BHML is the fraction of TIG's state space that is "in motion" at any given tick,
normalized by the ring size. The 4 anchors (4/10 = 40%) are pinned — zero Prog velocity.
The 6 cycle states (6/10 = 60%) propagate at v_coh = 1.

W_BHML = (propagating fraction) × (normalization) = (6/10) × (1/10) = 3/50.

This is the wobble: 30% of the ring's capacity is in propagating mode, 40% is anchored,
and the remaining quantity (3/50) measures the "imbalance" between propagating and total.

---

## 8. The Open Question in TIG Terms

From ENCODING_NECESSITY_PROGRAM.md, the remaining open questions in TIG language are:

**Q1 — Why PEAK as entry?**
Algebraically: because φ(1,2) = 7. TIG semantically: because PEAK is the apex of the
COUNTER phase, and dissolution reads backward from the apex. But is there a TIG principle
(coherence gate condition? BTQ selection?) that FORCES x=7 as the entry?

**Q2 — Why −Prog direction?**
The braid reads σ⁻¹ (backward through the cycle), not σ (forward). In TIG: forward = Being→Becoming,
backward = Becoming→Being. The braid is the dissolution-direction readout.
But is there a coherence gate that forces the −Prog direction at this step?
One hypothesis: the dissolution direction is forced by the T* = 5/7 threshold — states below T*
are in the backward-reading regime. PEAK (x=7) is at the T* boundary.

**Q3 — Connection to CK's olfactory layer?**
The olfactory bulb reads information as a "field topology" (not path). If the morphotic braid
is the CL diagonal, then the olfactory field topology is determined by the braid — each operator's
"smell" is its position in the σ-cycle. The 4 fixed operators have fixed smell (no drift);
the 6 cycle operators have drifting smell (advancing per tick). This is untested.
