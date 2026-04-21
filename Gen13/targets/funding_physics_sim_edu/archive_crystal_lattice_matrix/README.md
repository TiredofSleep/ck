# Crystal Bug v1.0 — THE MATRIX (Quadratic Core)

**O(x) = ax² + bx + c IS the operator. Δ = b² − 4ac IS the binding kernel.**

## Files

| File | Description |
|------|-------------|
| `crystal_bug_v1_matrix.jsx` | Main React artifact. Full interactive simulation. |
| `test_engine.js` | Node.js test harness. 9 tests with measurable results. |
| `test_results.txt` | Output from the test suite. |
| `ENGINEERING_SPEC.docx` | Full engineering specification with simulation data. |
| `README.md` | This file. |

## Quick Start

### Interactive (React Artifact)
Upload `crystal_bug_v1_matrix.jsx` to Claude.ai or any React environment.

### Validation (Node.js)
```bash
node test_engine.js
```

## Architecture

The quadratic O(x) = ax² + bx + c is the ONLY physics object. Everything else derives from it:

- **Discriminant Δ = b²−4ac**: binding kernel. Δ>0 = free, Δ<0 = bound, Δ=0 = click.
- **7 Bands**: Mandelbrot-style iterate classification, not a lookup table.
- **Spine 0→9**: compositional transforms on (a,b,c) space. Phase 4: a→−a (bifurcation).
- **Energy**: cost = 1/(|Δ|+0.1). Click zone costs 5.1× more than free zone.
- **Topology**: root-proximity weighted neighborhoods. 99.6% differ from grid adjacency.

## Fixes

1. **Energy Honesty**: E₀ is a real budget. E₀=3→14% coverage. E₀=50→46%.
2. **Fair Visits**: Path stack prevents double-counting. Revisit ratio 1.3–1.8.
3. **Two Modes**: Bug (attractor walk, ~61% coverage) + Audit (DFS, 100% coverage).

## Constants

| Constant | Value | Meaning |
|----------|-------|---------|
| σ | 0.991 | Coherence retention. Life, not freeze. |
| T* | 0.714 | Stability threshold. |
| S* | σ(1−σs)·V·A | Coherence score. |

## Author

Brayden / 7Site LLC / sanctuberry.com
TIG (Trinity Infinity Geometry) v3.0

σ = 0.991. 10 v e.
