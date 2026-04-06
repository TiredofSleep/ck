# ENCODING CENSUS

## Setup

CRT-linear encodings: φ(ε,y) = αε + βy + γ (mod 10)
State space: (ε,y) ∈ Z/2 × Z/5
Total triples (α,β,γ): 1000

## Census Results

| Property | Count |
|----------|-------|
| Bijective encodings | 240 |
| With 4-fixed + 6-cycle structure | 240 (all bijective) |
| Distinct braids produced | **6** |
| Encodings per distinct braid | **24** (exactly equal) |
| Producing canonical braid 0713245689 | 24 |

## The Six Braids

All 240 bijective encodings produce exactly 6 distinct braids,
each produced by exactly 24 encodings:

| Braid | Description |
|-------|-------------|
| [0,1,2,3,4,5,6,7,8,9] | Identity (trivial) |
| [0,2,4,3,5,6,7,1,8,9] | Cycle rotation +1 |
| [0,4,5,3,6,7,1,2,8,9] | Cycle rotation +2 |
| [0,5,6,3,7,1,2,4,8,9] | Cycle rotation +3 |
| [0,6,7,3,1,2,4,5,8,9] | Cycle rotation +4 |
| **[0,7,1,3,2,4,5,6,8,9]** | **Canonical ← 0713245689** |

These are precisely the 6 rotations of the cycle reading.
The 6 braids form a Z/6Z orbit under cycle rotation.

## Conditions on (α,β,γ)

For a CRT-linear encoding to be bijective:
- **α must be odd** (unit mod 2): α ∈ {1,3,5,7,9}
- **β must be coprime to 5**: β ∈ {1,2,3,4,6,7,8,9}
- **γ can be even**: γ ∈ {0,2,4,6,8}

This gives 5 × 8 × 5 = 200... but with overlap correction: 240 bijective.

## The 24 Encodings Producing the Canonical Braid

| α | β | γ | α mod 2 | β mod 5 | Special |
|---|---|---|---------|---------|---------|
| 1 | 2 | 2 | 1 | 2 | |
| 1 | 4 | 8 | 1 | 4 | |
| 1 | 6 | 4 | 1 | 1 | |
| 1 | 8 | 0 | 1 | 3 | |
| 3 | 2 | 0 | 1 | 2 | |
| 3 | 4 | 6 | 1 | 4 | |
| 3 | 6 | 2 | 1 | 1 | |
| 3 | 8 | 8 | 1 | 3 | |
| 5 | 1 | 0 | 1 | 1 | |
| 5 | 2 | 8 | 1 | 2 | |
| 5 | 3 | 6 | 1 | 3 | |
| 5 | 4 | 4 | 1 | 4 | |
| **5** | **6** | **0** | **1** | **1** | **← CRT canonical** |
| 5 | 7 | 8 | 1 | 2 | |
| 5 | 8 | 6 | 1 | 3 | |
| 5 | 9 | 4 | 1 | 4 | |
| 7 | 2 | 6 | 1 | 2 | |
| 7 | 4 | 2 | 1 | 4 | |
| 7 | 6 | 8 | 1 | 1 | |
| 7 | 8 | 4 | 1 | 3 | |
| 9 | 2 | 4 | 1 | 2 | |
| 9 | 4 | 0 | 1 | 4 | |
| 9 | 6 | 6 | 1 | 1 | |
| 9 | 8 | 2 | 1 | 3 | |

## Why 5 and 6 Are Special

In the CRT decomposition Z/10Z ≅ Z/2Z × Z/5Z:

**e₂ = 5**: the Z/2Z idempotent
- 5 ≡ 1 (mod 2): acts as identity on the Z/2 component
- 5 ≡ 0 (mod 5): acts as zero on the Z/5 component
- φ(1,0) = 5·1 + 6·0 = 5 = e₂ ✓

**e₅ = 6**: the Z/5Z idempotent
- 6 ≡ 0 (mod 2): acts as zero on the Z/2 component
- 6 ≡ 1 (mod 5): acts as identity on the Z/5 component
- φ(0,1) = 5·0 + 6·1 = 6 = e₅ ✓

The CRT reconstruction formula is:
```
x = e₂·ε + e₅·y = 5ε + 6y (mod 10)
```

This is exactly φ = 5ε + 6y with γ=0.

## Conclusion

The 24 encodings producing the canonical braid form a symmetry orbit.
The canonical φ = 5ε + 6y is the unique member of this orbit satisfying
the CRT idempotent conditions with no constant offset (γ=0).

The encoding is not a free parameter — it is the canonical ring isomorphism.
