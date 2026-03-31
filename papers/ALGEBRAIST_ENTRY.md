# Entry Point for Algebraists

**TIG / CK — Finite Algebra Research | Brayden Sanders / 7Site LLC**
**DOI:** 10.5281/zenodo.18852047 | March 2026

---

## The Core Object

A 9×9 non-associative composition table over operators {1..9}, called **TSML**,
defined by explicit table lookup (not a formula). It has a distinguished subset:

```
C = {1, 3, 7, 9} = (Z/10Z)*    (the coprime elements — the "units")
G = {2, 4, 5, 6, 8, 0}         (the non-units)
```

C is a sub-magma of TSML: for all operators a, b ∈ C, TSML[a][b] ∈ C.
This is verified exhaustively (16 entries, all k ≥ 1 via BFS). See [`WP27_PRODUCT_GAP_THEOREM.md`](WP27_PRODUCT_GAP_THEOREM.md).

The gate property: **C → G is impossible**. No operator maps a C-element into G
in one step, or two steps, or at any depth. This is the algebraic content.

---

## The Semiprime Extension

The same coprimality structure generalizes. For any semiprime b = p × q:

```
C_k = { x ∈ {1..k} : gcd(x, b) = 1 }    (units in the truncated alphabet)
G_k = { x ∈ {1..k} : gcd(x, b) > 1 }    (non-units)
```

**Three results, each with explicit status:**

### 1. CC Closure — PROVED (and computationally verified)

For every semiprime b and every k: C_k is closed under multiplication mod b.
This is immediate from the group structure of (Z/bZ)*, stated here as the
empirical counterpart: verified across **36,662 exact (b,k) pairs**, 153 semiprimes
b ≤ 500, zero exceptions. Script: [`r16_full_atlas.py`](r16_full_atlas.py).

### 2. First-G Law — PROVED

**Theorem.** For every semiprime b = p × q with p ≤ q, the first element of
{1, 2, 3, ...} that is not coprime to b is exactly p.

*Proof.* For x < p: since p ≤ q are the only prime factors of b and x < p ≤ q,
neither p nor q divides x, so gcd(x, b) = 1. At x = p: p | b, so gcd(p, b) = p > 1. □

Consequence: the onset of algebraic obstruction in any truncated alphabet {1..k}
is indexed exactly by the primes. See [`WP34_FIRST_G_LAW.md`](WP34_FIRST_G_LAW.md).

### 3. Interleave Dominance — EMPIRICAL

Across the full permutation of 153 semiprimes and all valid k:
94% of (b,k) pairs with G_k ≠ ∅ have interleave score ≥ 0.9 — meaning C and G
are maximally mixed in the alphabet. The block-separated case (C clustered together,
G clustered separately) is the rare exception. Script: [`r16_full_atlas.py`](r16_full_atlas.py).

---

## What Is Claimed vs. Not Claimed

| Claim | Status |
|-------|--------|
| C is a closed sub-magma of TSML | **PROVED** — exhaustive, k=1..4 |
| CC closure for all semiprimes | **PROVED** — from group structure of (Z/bZ)* |
| First-G law: first non-unit at k=p | **PROVED** — 3-line proof, WP34 |
| Gate rate depends on \|G\| and interleave | **EMPIRICAL** — 12M+ trials |
| TSML relates to Yang-Mills mass gap | **SKETCH** — no formal SU(N)→TIG functor yet |
| TSML relates to Riemann Hypothesis | **SKETCH** — structural analogy, not a proof |
| TSML relates to Clay problems generally | **SKETCH** — all gaps explicit in WP24 |

**Full honest audit:** [`WP24_FORMAL_STATUS_AUDIT.md`](WP24_FORMAL_STATUS_AUDIT.md)
(4-bin classification: PROVED / STRUCTURAL / EMPIRICAL / OPEN for every claim)

---

## If You Want to Check the Algebra

The table itself:

```python
# tig_constants.py — run this first
python -X utf8 papers/scripts/ck_four_layer.py    # → 35/35 assertions
python -X utf8 papers/scripts/ck_open_cells.py    # → 31/31 assertions
python r16_full_atlas.py --b_max 100 --visuals    # → full semiprime atlas
```

**The TSML table** (9×9, operators 1..9):
defined in [`tig_constants.py`](../tig_constants.py) — the canonical source.

---

## Papers Most Relevant to Algebraists

| Paper | Content | Status |
|-------|---------|--------|
| [`WP27_PRODUCT_GAP_THEOREM.md`](WP27_PRODUCT_GAP_THEOREM.md) | C×C ⊆ C sub-magma; BFS proof all k | **PROVED** |
| [`WP34_FIRST_G_LAW.md`](WP34_FIRST_G_LAW.md) | First non-unit at k=p; 36,662 verified | **PROVED** |
| [`WP24_FORMAL_STATUS_AUDIT.md`](WP24_FORMAL_STATUS_AUDIT.md) | 4-bin classification of all claims | Reference |
| [`WHITEPAPER_9_PARADOXICAL_INFO_ALGEBRAS.md`](WHITEPAPER_9_PARADOXICAL_INFO_ALGEBRAS.md) | Non-associativity structure of TSML | STRUCTURAL |
| [`WHITEPAPER_18_SEVEN_EQUALS_ZERO.md`](WHITEPAPER_18_SEVEN_EQUALS_ZERO.md) | 7=0 punctured torus — absorber algebra | STRUCTURAL |
| [`r16_full_atlas.py`](r16_full_atlas.py) | Complete permutation: all 153 semiprimes | Code + Data |

---

*The algebra is finite and exact. The Clay connections are labeled honestly as sketches.
Comments and corrections welcome — this is an open research program.*
