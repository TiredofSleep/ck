# THEOREM E: CONJUGACY TO ROTATION + ANCHORS

## Statement

The hidden operator on Z/2 × Z/5 is conjugate to the simplest possible dynamics:
**identity on 4 anchor states, cyclic rotation k → k+1 (mod 6) on the 6-cycle.**

The apparent algebraic complexity of the split operator (piecewise polynomials, parity rules)
is entirely an artifact of the (ε, y) coordinate encoding — not of the underlying dynamics.

---

## The Conjugacy Map

Define the cycle index coordinate k ∈ Z/6 on the 6 cycling states:

| k | (ε, y) | x (visible) |
|---|--------|-------------|
| 0 | (1, 1) | 1           |
| 1 | (1, 2) | 7           |
| 2 | (0, 1) | 6           |
| 3 | (1, 0) | 5           |
| 4 | (0, 4) | 4           |
| 5 | (0, 2) | 2           |

On the 4 anchor states, define the trivial coordinate (identity):

| anchor | (ε, y) | x (visible) |
|--------|--------|-------------|
| a₀     | (0, 0) | 0           |
| a₁     | (1, 3) | 3           |
| a₂     | (0, 3) | 8           |
| a₃     | (1, 4) | 9           |

---

## The Simple Operator in (k, anchor) Coordinates

In conjugated coordinates:

```
cycle states:  k → k + 1 (mod 6)
anchor states: aᵢ → aᵢ   (identity)
```

**That is the entire operator. Nothing more.**

---

## Verification

The 6-cycle in (ε, y) space:

```
(1,1) → (1,2) → (0,1) → (1,0) → (0,4) → (0,2) → (1,1)
  k=0     k=1     k=2     k=3     k=4     k=5     k=0
```

Each step advances k by 1 (mod 6). ✓

The 4 fixed points:

```
(0,0) → (0,0) ✓
(1,3) → (1,3) ✓
(0,3) → (0,3) ✓
(1,4) → (1,4) ✓
```

**End-to-end verification: all 10 transitions match. ✓**

---

## Why This Matters

Before this theorem, the hidden operator appeared to require:
- A piecewise Boolean formula for ε'
- Two distinct degree-4 polynomials mod 5 for y'

After conjugacy, the operator is:
- One cyclic addition mod 6
- One identity map

The coordinate system (ε, y) = (parity, mod-5 residue) encodes the rotation 
in a nonlinear way, creating the illusion of algebraic complexity.

**The dynamics are maximally simple. The encoding is nontrivial.**

---

## Formal Statement

**Theorem E.** Let φ: Z/2 × Z/5 → {anchors} ∪ Z/6 be the coordinate map defined above.
Then the hidden operator F satisfies:

```
φ ∘ F = σ_simple ∘ φ
```

where σ_simple is:
- k → k+1 (mod 6) on Z/6
- identity on {anchors}

The conjugacy is exact. No approximation. ✓

---

## Implication for the Speed-of-Light Analogy

The "speed" of the system is now precise:
- The cycle advances at rate 1 per step in k-coordinates
- v_coh = 1 is not just empirical — it is the definition of the dynamics
- The 4 anchors are zero-velocity states by construction

The wobble W_BHML = 3/50 = (cycle occupancy 6/10) / 10 now has a clean home:
**the 6-cycle occupies exactly 6 of 10 visible states.**
