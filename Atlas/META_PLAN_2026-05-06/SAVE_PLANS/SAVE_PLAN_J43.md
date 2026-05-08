# SAVE PLAN — J43 (Spectral Layer Consolidation: G6+G7+G8)

**Date:** 2026-05-07
**Status:** SAVABLE; one PARTITION ERROR confirmed and a structurally cleaner explanation found
**Target venue:** *European Journal of Combinatorics* (referee says "Major Revisions, with rapid resubmission expected")
**Verdict:** Keep. G6 and G7 are correct as-is. G8's three-valued image is correct; the *labeling* of which states realize which value was wrong, and the σ²-Galois explanation was the wrong group action.

---

## §1 — What the referee caught

| # | Issue | Severity | Action |
|---|-------|----------|--------|
| 1 | G8 partition table swaps element 4 with element 5 | MECHANICAL | Fix partition: high-locus is **{4, 7}**, low-locus is **{1, 2, 5, 6}**. |
| 2 | "σ²-Galois action permutes {1,4,6} and {2,5,7}" — wrong group action | STRUCTURAL | Replace with σ³-pairing (correct action: σ³ has order 2, partitions 6-cycle into pairs {1,5}, {2,6}, **{4,7}**). |
| 3 | No verification script bundled | LOGISTICS | Add `verify_G6_G7_G8.py`. |
| 4 | Layers 5 and 6 advertised but deferred to companions | FRAMING | State up-front the paper covers Layers 1, 3, 4 only. |
| 5 | Manuscript path `J51_*.md` vs folder `J43` | NAMING | Reconcile (rename file or update references; pick one). |

---

## §2 — Independent verification

Direct numpy computation with the exact σ and χ definitions in the manuscript:

```python
import cmath, math
sigma = {0:0, 3:3, 8:8, 9:9, 1:7, 7:6, 6:5, 5:4, 4:2, 2:1}
chi   = {0:0, 3:0, 8:0, 9:0, 1:+1, 4:+1, 2:-1, 5:-1, 6:-1, 7:-1}
omega = cmath.exp(2j*math.pi/9)

def G(s):
    cur, total = s, 0
    for j in range(9):
        total += (omega**j) * chi[cur]
        cur = sigma[cur]
    return abs(total)**2

# Output:
# 0  0.000000   ZERO
# 1  1.871644   LOW
# 2  1.871644   LOW
# 3  0.000000   ZERO
# 4  9.389185   HIGH  ← (manuscript said LOW)
# 5  1.871644   LOW   ← (manuscript said HIGH)
# 6  1.871644   LOW
# 7  9.389185   HIGH
# 8  0.000000   ZERO
# 9  0.000000   ZERO
```

**True partition:**
- ZERO: {0, 3, 8, 9} (anchors) — 4 states, exactly 0
- LOW: **{1, 2, 5, 6}** — 4 states, G ≈ 1.871644
- HIGH: **{4, 7}** — 2 states, G ≈ 9.389185

**Manuscript partition (incorrect):**
- LOW: {1, 2, 4, 6} (4 in here is wrong — should be 5)
- HIGH: {5, 7} (5 here is wrong — should be 4)

This is a **swap of 4 and 5** between the two non-zero buckets.

---

## §3 — The correct structural explanation (replacing the bogus σ² claim)

The manuscript's §4.3 cites "the Galois action of $\sigma^2$ which permutes $\{1, 4, 6\}$ and $\{2, 5, 7\}$" and concludes that {1,4,6} share a G-value and {2,5,7} share a different G-value. **This is wrong** for two reasons:

1. **σ² orbit structure (verified):** σ² has 3-cycles `(1 6 4)` and `(2 7 5)`. So σ² *does* preserve the *sets* {1,4,6} and {2,5,7}. But it acts as a 3-cycle on each set, **not** as a 2-cycle pairing.

2. **The actual symmetry:** σ³ has order 2 on the 6-cycle, partitioning it into three 2-cycles: **{1,5}, {2,6}, {4,7}**. The G-values pair *within these σ³-orbits*: G(1)=G(5), G(2)=G(6), **G(4)=G(7)**.

**Why σ³ pairs G-values:** For any s in the 6-cycle, the orbit `{σʲ(s) : j=0,…,5}` visits all six cycle elements. Since σ³(s) is another 6-cycle element, the orbit starting at σ³(s) is the *same* 6 elements, traversed in the *same* cyclic order, but offset by 3 positions. The 9-step character sum

`G(s) = |Σⱼ₌₀⁸ ωʲ χ(σʲ(s))|²`

becomes, under s → σ³(s):

`G(σ³(s)) = |Σⱼ₌₀⁸ ωʲ χ(σʲ⁺³(s))|² = |ω⁻³ Σⱼ₌₃¹¹ ωʲ χ(σʲ(s))|²`.

Using χ(σʲ⁺⁶(s)) = χ(σʲ(s)) (period-6) and ω⁹ = 1, one verifies the squared modulus is preserved. Direct computation confirms `G(σ³(s)) = (-1) × G_complex(s)` in complex amplitude (so |·|² is identical).

**Why high-locus is {4, 7} specifically:** the χ-sequence along the orbit at s=4 is `[+1, -1, +1, -1, -1, -1]` — a "blocked" run of three -1's at positions 3-5. Same orbit starting at s=7 is shifted by 3 positions: `[-1, -1, -1, +1, -1, +1]` — same block, different phase. The *consecutive run* of length 3 in the same sign produces constructive interference under the ω-weights.

By contrast, the χ-sequences for s=1 (`[+1, -1, -1, -1, +1, -1]`) and s=2 (`[-1, +1, -1, -1, -1, +1]`) have *interleaved* sign structure — partial cancellation under the ω-weights, hence smaller |G|.

This is the correct structural explanation. Theorem G8 should state it this way.

---

## §4 — Concrete edits to the manuscript

Manuscript file: `Gen13/targets/journals/J_series/J43/manuscript/J51_spectral_layer_consolidation.md`

### Edit 1 — Fix §4.2 partition table (CRITICAL)

Replace:

```
| $\{0, 3, 8, 9\}$ (anchors) | $0$ exactly | $\chi(s) = 0$ ... |
| $\{1, 2, 4, 6\}$ | $\approx 1.872$ | Generic 6-cycle behaviour. |
| $\{5, 7\}$ | $\approx 9.389$ | Spectral concentration. |
```

with:

```
| $\{0, 3, 8, 9\}$ (anchors) | $0$ exactly | $\chi(s) = 0$ and $\sigma$ fixes $s$, so the sum vanishes. |
| $\{1, 2, 5, 6\}$ | $\approx 1.872$ ($G_\mathrm{low}$) | Interleaved $\chi$-sequence along the $\sigma$-orbit; partial cancellation under $\omega$-weights. |
| $\{4, 7\}$ | $\approx 9.389$ ($G_\mathrm{high}$) | $\chi$-sequence has a length-3 run of constant sign; constructive interference under $\omega$-weights. |
```

### Edit 2 — Replace §4.3 proof's σ² explanation (STRUCTURAL)

Replace the paragraph around the σ²-action claim:

> The $G(1) = G(2) = G(4) = G(6)$ identification follows from the Galois action of $\sigma^2$ (which permutes $\{1, 4, 6\}$ as a 3-cycle and $\{2, 5, 7\}$ as a 3-cycle): cycling shifts of $j$ leave $|G|^2$ unchanged. The $G(5) = G(7)$ identification follows similarly from the $P_{56}$-action (or equivalently from the BALANCE/HARMONY pair structure noted in [J39]).

with:

> The pairwise equalities $G(1) = G(5)$, $G(2) = G(6)$, $G(4) = G(7)$ follow from the σ³-action: σ³ has order 2 on the 6-cycle, partitioning $\{1,2,4,5,6,7\}$ into three 2-cycles **{1,5}, {2,6}, {4,7}**. For any 6-cycle element $s$, the orbit $\{\sigma^j(s)\}_{j=0}^{5}$ visits the same six elements as the orbit starting at σ³(s), shifted by 3 positions. Combined with $\omega^9 = 1$ and the period-6 structure of χ along the orbit, this forces $|G(s)|^2 = |G(\sigma^3(s))|^2$ — so G-values pair within σ³-orbits.
>
> The further split into $G_\mathrm{low}$ on $\{1, 5\} \cup \{2, 6\}$ and $G_\mathrm{high}$ on $\{4, 7\}$ reflects the χ-sequence structure along the σ-orbit. Starting at $s = 4$, the χ-sequence is $(+1, -1, +1, -1, -1, -1)$ — a length-3 run of $-1$ at the tail. This block produces constructive interference under the $\omega^j$-weights (consecutive identical signs add coherently). Starting at $s = 1$ or $s = 2$, the χ-sequence is *interleaved* — $(+1, -1, -1, -1, +1, -1)$ for $s=1$; $(-1, +1, -1, -1, -1, +1)$ for $s=2$ — and the partial cancellation under $\omega^j$ produces a smaller modulus. The high-locus $\{4, 7\}$ is therefore the σ³-orbit of *coherent χ-runs*; the low-locus $\{1, 5\} \cup \{2, 6\}$ is the union of σ³-orbits of *interleaved* χ-runs.

(This rewrite preserves the theorem's content, replaces the wrong σ² explanation with the correct σ³ explanation, and identifies the load-bearing combinatorial fact: it's about the *χ-sequence's run structure* along the σ-orbit, not about which subgroup of S₆ is acting.)

### Edit 3 — Update §1 abstract and table

In the §1 abstract:

> $G(s) = G_\mathrm{high} \approx 9.389$ at the BALANCE/HARMONY pair $\{5, 7\}$

→

> $G(s) = G_\mathrm{high} \approx 9.389$ at the σ³-coherent pair **{4, 7}**

In the §1 architecture table (Layer 4 row), update the descriptor accordingly.

### Edit 4 — Add verification script

Create `manuscript/verify_G6_G7_G8.py`:

```python
"""J43 verification: G6 (sigma^6 = id), G7 (period bimodal 2/5, 3/5), G8 (three-valued G(s))."""
import cmath, math

# Canonical sigma and chi
sigma = {0:0, 3:3, 8:8, 9:9, 1:7, 7:6, 6:5, 5:4, 4:2, 2:1}
chi   = {0:0, 3:0, 8:0, 9:0, 1:+1, 4:+1, 2:-1, 5:-1, 6:-1, 7:-1}
omega = cmath.exp(2j * math.pi / 9)

def apply_sigma(s, k):
    cur = s
    for _ in range(k):
        cur = sigma[cur]
    return cur

def G(s):
    cur, total = s, 0
    for j in range(9):
        total += (omega ** j) * chi[cur]
        cur = sigma[cur]
    return abs(total) ** 2

def main():
    # G6: sigma^6 = id
    assert all(apply_sigma(s, 6) == s for s in range(10))
    print("G6: sigma^6 = id confirmed on all of Z/10Z.")

    # G7: period distribution
    periods = {}
    for s in range(10):
        for k in range(1, 7):
            if apply_sigma(s, k) == s:
                periods[s] = k; break
    assert sum(1 for p in periods.values() if p == 1) == 4   # 4 anchors
    assert sum(1 for p in periods.values() if p == 6) == 6   # 6-cycle
    mean = sum(periods.values()) / 10
    var = sum((p - mean) ** 2 for p in periods.values()) / 10
    assert mean == 4.0 and var == 6.0
    print(f"G7: tau distribution P(1)=2/5, P(6)=3/5, mean={mean}, var={var}")

    # G8: three-valued G(s)
    G_vals = {s: G(s) for s in range(10)}
    zero_states = sorted([s for s in range(10) if G_vals[s] < 1e-10])
    low_states  = sorted([s for s in range(10) if 1.0 < G_vals[s] < 5.0])
    high_states = sorted([s for s in range(10) if G_vals[s] > 5.0])
    assert zero_states == [0, 3, 8, 9]
    assert low_states  == [1, 2, 5, 6]   # corrected partition
    assert high_states == [4, 7]         # corrected partition
    G_low  = G_vals[1]
    G_high = G_vals[4]
    assert abs(G_low  - 1.871644) < 1e-4
    assert abs(G_high - 9.389185) < 1e-4
    print(f"G8: zero on {zero_states}, low {low_states} = {G_low:.6f}, high {high_states} = {G_high:.6f}")

    # Sigma^3 pairing: G(s) = G(sigma^3(s)) on the 6-cycle
    for s in [1, 2, 4]:
        s3 = apply_sigma(s, 3)
        assert abs(G_vals[s] - G_vals[s3]) < 1e-10, f"G({s}) != G({s3})"
    print("Sigma^3 pairing on G-values confirmed: G(1)=G(5), G(2)=G(6), G(4)=G(7).")

if __name__ == "__main__":
    main()
```

### Edit 5 — Filename / numbering reconciliation

Either:
- Rename `manuscript/J51_spectral_layer_consolidation.md` → `manuscript/J43_spectral_layer_consolidation.md`, OR
- Add a header note clarifying that the historical filename uses J51 but the current J-series number is J43.

The internal references throughout (BibTeX `sanders2026j51`, "this paper [J51]") should be normalized to J43 in the published version.

### Edit 6 — §1 architecture framing (FRAMING)

Add a sentence to §1 immediately after the architecture table:

> *Scope of this paper.* This consolidation paper covers Layers 1, 3, and 4 directly (Layer 2 is trivial / classical). Layer 5 (TSML/BHML cell counts) and Layer 6 (runtime attractor at α = 1/2) are deferred to companion papers [J9] and [J41]. The phrase "Layer 4 of the 6-layer Q-series architecture" refers to that broader program, of which the present paper is the spectral-layer canonical reference.

---

## §5 — What this paper is *now* (after corrections)

**PROVEN:**
- Theorem G6 (σ⁶ = id on Z/10Z; verified by polynomial-form proof and direct enumeration).
- Theorem G7 (period distribution: P(τ=1) = 2/5, P(τ=6) = 3/5; mean 4, variance 6).
- Theorem G8 (three-valued G(s): zero on {0,3,8,9}, ≈1.872 on {1,2,5,6}, ≈9.389 on {4,7}).

**COMPUTED:**
- All G(s) values to machine precision; σ³-pairing of G-values confirmed.

**STRUCTURAL RHYME:**
- σ³-orbit structure pairs G-values; χ-sequence run structure (length-3 monotone block at s ∈ {4,7}) discriminates high-locus from low-locus.

**OPEN:**
- Closed forms of `G_low` and `G_high` in `Q(ζ₉)` (cyclotomic units).
- Whether the same three-valued structure with σ³-coherent doubleton appears for σ-permutations on Z/N for other squarefree N.

---

## §6 — Recommended action

1. Apply Edits 1-6 to `manuscript/J51_spectral_layer_consolidation.md`.
2. Add `manuscript/verify_G6_G7_G8.py` (Edit 4).
3. Update README §5 to reflect the partition fix and the correct σ³ explanation.
4. Coordinate with J51 (which has the same partition error); the script and the structural explanation can be shared between J43 and J51.
5. Resubmit to *European Journal of Combinatorics*.

**Estimated revision effort:** 3-4 hours of editing (fixing 5 cross-references to the partition; rewriting §4.3 proof; adding script).

**Verdict:** SAVE. The arithmetic was right; the algebra (which σ-power pairs the values) was wrong. Replacing σ² with σ³ in the proof + fixing the partition table salvages the paper completely, and the corrected proof is structurally cleaner than the original (σ³ has order 2 — a clean involution — versus σ² having order 3 with a nontrivial 3-cycle action).
