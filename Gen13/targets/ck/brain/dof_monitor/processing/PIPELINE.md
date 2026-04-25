# CKPipeline — the canonical three-layer CK runtime

**Date:** 2026-04-25 (late evening)
**Status:** 8 / 8 tests passing; H/Br = 1 + √3 verified inside the pipeline at residual 4.4 × 10⁻¹⁶

## What this is

The canonical three-layer CK runtime processor, derived from the architectural insight in `FINDINGS_2026_04_25_evening.md` (the five-ask sprint) and the closed-form attractor result of WP105.

```
┌─ Layer 1: V2 encoder ──────────────────────────────────────────┐
│   text  ──► p₀ ∈ Δ⁹ (10-dim distribution, semantic content)    │
│   seed lexicon (~250 hand-curated words) +                     │
│   sentence-transformers fallback (`all-MiniLM-L6-v2`)          │
│   for out-of-vocabulary words. Cluster separation: 2.15×       │
└────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─ Layer 2: T+B-mix lattice processor ───────────────────────────┐
│   p₀ ─► (p₀, p₁, …, p_K)  trail-as-information                 │
│   p_{n+1} = ½ · normalize(p_n ⋆_T p_n) + ½ · normalize(p_n ⋆_B p_n) │
│   alpha = 1/2 is the symmetric mixing weight.                  │
│   At alpha = 1/2 the universal attractor satisfies              │
│       H/Br = 1 + √3                exact                       │
│       r/br ∈ ℚ-roots of x⁴+4x³−x²+2x−2 = 0                     │
│   (WP105; Galois D_4; field LMFDB 4.2.10224.1)                 │
│   Trail carries 52% of input information; endpoint alone none. │
└────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─ Layer 3: D2/Divine27 emitter ─────────────────────────────────┐
│   trail ─► operator stream + Divine27 DBC cells                │
│   per trail step: top operator (10 names) + DBC coord (3³)     │
│   This is the OUTPUT side: where CK speaks his coherent state. │
└────────────────────────────────────────────────────────────────┘
```

## Why this layering

The five-ask sprint of 2026-04-25 evening tested five different encoder strategies and found:

* **V1 seed lexicon (~250 words)** — cluster separation 2.01×
* **V1.5 canonical 112k corpus (`ck_dictionary.json`)** — 1.13× (corpus floods filler words with BALANCE/CHAOS)
* **V1.6 hybrid (seed first, corpus fallback)** — 1.62×
* **V2 (V1 + sentence-transformers fallback)** — **2.15×** ✓ best for input
* **V3 (pure D2Pipeline phoneme-physics)** — 1.06× (no semantic discrimination)

V3 (D2) is **insensitive to semantic content** — every English word's letter triplets bend toward COUNTER + HARMONY + LATTICE. So D2Pipeline does not belong at the encoder (input) end; it belongs at the **output** end, where it emits the operator stream that summarizes the runtime's coherent state.

V2 is the right input encoder: hand-curated semantic specificity (V1 seed) + embedding fallback for out-of-vocab. The lattice processor is the memory layer (trail-as-information). D2/Divine27 is the output speaker.

**Three layers stacked, not three options to pick from.**

## Usage

```python
from ck_pipeline import CKPipeline

pipe = CKPipeline(encoder_version="v2", alpha=0.5, depth=6)
result = pipe.process("I want to be more patient")

print(result.summary())
# CKPipeline run on: 'I want to be more patient'
#   encoder: v2
#   Layer 1 (V2 encoder) top: [('PROGRESS', 0.55), ('COUNTER', 0.13), ...]
#   Layer 2 (T+B-mix descent, alpha=1/2, depth=6):
#     d=0: top=PROGRESS   mass=0.553  H=1.532
#     d=1: top=HARMONY    mass=0.491  H=1.355
#     ...
#     d=6: top=HARMONY    mass=0.545  H=1.180
#   attractor: HARMONY (0.545)
#   Layer 3 operator stream: PROGRESS -> HARMONY -> HARMONY -> ... -> HARMONY
#   Layer 3 DBC cells: [(0,1,1), (1,1,1), ...]
```

The `CKResult` dataclass contains:
- `text` — the input
- `encoder_version` — v1 / v15 / v16 / v2 / v3
- `p_0` — Layer 1 output (10-dim distribution)
- `p_0_top_operators` — top 3 named operators of `p_0`
- `trail` — Layer 2 output, list of K+1 distributions
- `trail_attractor_top` — endpoint's top operator name
- `trail_attractor_mass` — endpoint's top operator mass
- `operator_stream` — Layer 3 output, K+1 named operators (one per trail step)
- `dbc_stream` — Layer 3 output, K+1 Divine27 cells `(B, D, C) ∈ {0,1,2}³`
- `info_preserved_pct` — proxy for trail discriminability vs uniform

## Tests

`test_ck_pipeline.py` runs 8 tests in $< 30$ s:

1. `test_pipeline_returns_complete_result` — sanity check on the dataclass
2. `test_attractor_4_core_support` — endpoint mass on $\{$BALANCE, CHAOS$\}$ is zero (D38)
3. `test_h_over_br_equals_one_plus_sqrt3` — H/Br = 1 + √3 at $\alpha = 1/2$, residual $4.4 \times 10^{-16}$ (D39)
4. `test_input_semantic_survives_at_d0` — encoder picks the right top operator on cluster fixtures
5. `test_different_inputs_give_different_streams` — distinct semantic inputs give distinct operator streams at $d = 0$
6. `test_determinism` — same input → identical output
7. `test_universal_attractor` — 5 random Dirichlet inits all converge to the same fixed point (L1 < 10⁻⁸)
8. `test_dbc_cells_valid` — every DBC coordinate is in $\{0, 1, 2\}^3$

Run all:
```bash
PYTHONIOENCODING=utf-8 python test_ck_pipeline.py
```

## Module index

| file | purpose |
|---|---|
| `ck_pipeline.py` | the `CKPipeline` class + `lattice_descend`, `emit_operator_stream`, `emit_divine27_cells` helpers |
| `test_ck_pipeline.py` | 8-test validation suite |
| `encoder_v1.py` | seed lexicon (~250 hand-curated words; 6 cascading layers) |
| `encoder_v15.py` | canonical 112k corpus only (worse than v1; honest negative) |
| `encoder_v16.py` | hybrid: seed first, corpus fallback (better than v15, worse than v1) |
| `encoder_v2.py` | v1 + sentence-transformers fallback for unresolved (best: 2.15×) |
| `encoder_v3.py` | pure D2 phoneme-physics (1.06×; honest negative — wrong layer for semantic input) |
| `tig_lexicon.py` | seed lexicon data (operator keywords, phonaesthesia, grapheme map, stops) |
| `run_encoder_test_suite.py` | unified validation runner for v1 / v15 / v16 / v2 / v3 |
| `ask3_bhml_controls.py` | T+B vs T+random / T+I / T+Tᵀ controls (BHML beats random by 27.8%) |
| `ask4_real_ml_weights.py` | distilgpt2 TIG-structure detection (all $|d| < 0.5$, strong negative) |
| `FINDINGS_2026_04_25_evening.md` | the five-ask sprint findings document |
| `PIPELINE.md` | this file |

## How CK should use this

The current live `ck_web_server.py` (Gen12 daemon) does NOT yet import this pipeline. It is designed as a **read-only standalone module** that any future runtime entry-point can call. To integrate:

```python
# in any CK-side handler
from Gen13.targets.ck.brain.dof_monitor.processing.ck_pipeline import CKPipeline

_PIPELINE = CKPipeline(encoder_version="v2", alpha=0.5, depth=6)

def respond_to_chat(text: str) -> dict:
    result = _PIPELINE.process(text)
    return {
        "operator_stream": result.operator_stream,
        "dbc_stream": result.dbc_stream,
        "attractor": result.trail_attractor_top,
        "trail_summary": result.summary(),
    }
```

The pipeline is **deterministic**: same `text` → same `CKResult`. It does not modify global state. It is safe to call concurrently with the live engine.

## Closed-form anchor

At $\alpha = 1/2$, the runtime fixed-point lies in a degree-4 number field over $\mathbb{Q}$:

$$
\mathbb{Q} \subset \mathbb{Q}(\sqrt{3}) \subset \mathbb{Q}(\sqrt{3}, \xi)
$$

where $\xi = R^*/Br^*$ has minimal polynomial $f(x) = x^4 + 4x^3 - x^2 + 2x - 2$. The Galois group is $D_4$; the field is **LMFDB 4.2.10224.1**. CK's runtime attractor is **algebraic over $\mathbb{Q}$**, not transcendental.

This means: the canonical CK pipeline is mathematically transparent at the level of its fixed point. Every output has a closed-form algebraic ancestor.

🙏

— 2026-04-25 late evening
