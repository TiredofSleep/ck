# CK Gen 10 — The Coherence Keeper
**Author:** Brayden Sanders / 7Site LLC | **DOI:** 10.5281/zenodo.18852047 | **Live:** [coherencekeeper.com](https://coherencekeeper.com)

---

## What CK Is

- A coherence organism: every word derived from physics, nothing borrowed
- **D2:** Hebrew-root 5D force vectors (aperture, pressure, depth, binding, continuity)
- **TSML:** 9×9 composition table, 10 operators (VOID → RESET), SHA: `7726d8a6...`
- **T\* = 5/7:** The only fixed truth threshold; TIG type (9, 3, 6, 3/4)

---

## Verification Scripts

Run any script: `python -X utf8 papers/scripts/<script>.py`

| Script | What it proves | Score |
|--------|---------------|-------|
| `ck_four_layer.py` | P1–P4 simultaneously by exact computation | 35/35 |
| `ck_smoothing.py` | Gap persistence; σ≥0.26 threshold | 16/16 |
| `ck_classification.py` | Type-(9,3,6,3/4); two gradings; support gap bounds | 26/26 |
| `ck_field_analysis.py` | T1–T7 field analysis; gap deficit ~ λ^0.72 | 28/28 |
| `ck_transfer_metastable.py` | BRT corridor gap=1.0; metastable component count | 12/12 |
| `ck_phase_drift.py` | Phase-drift correlation: corr=-0.997 at t=100 | 6/6 |
| `ck_cemp_bound.py` | KV floor gap-positivity; 49/50 heights pass α≥1.376 | 6/6 |
| `tig_unit_tests_v2.py` | Full TIG unit tests | 65/65 |
| `ck_orbit_zone.py` | Orbit zone B/T/Δ; two-mechanism split; HAR bifurcation | 30/30 |
| `ck_dual_description.py` | Dual Description 2×2; C_TIG=250/21; Paradox Pairs | 33/33 |
| `ck_open_cells.py` | One-Way Gate; Three Levels G/E/S; Primitive Order Backbone | 31/31 |

---

## TIG Formal Status (Gen 10.19 — March 2026)

### PROVED — exact algebraic results

| Claim | Where |
|-------|-------|
| Corner sub-magma: C×C ⊆ C (C={1,3,7,9}) | `ck_four_layer.py` P1 |
| Spectral gap γ=3/4 at λ=0; γ≥1/4 for all λ∈[0,1] | `ck_four_layer.py` P2 |
| Return tail: P(T_HAR>n) ≤ 2·(1/4)^n | `ck_four_layer.py` P3 |
| (Z/10^nZ)* mod 10 = {1,3,7,9} for all n≥1 | `ck_four_layer.py` P4 |
| Halving Lemma: exponential KV-strip convergence | `papers/data/WP19_HALVING_LEMMA_final.tex` |
| Gap persistence: σ≥0.26 Gaussian smoothing restores gap ≥ 0.10 | `ck_smoothing.py` |

### STRUCTURAL — new framework, honest about scope

| Claim | Paper |
|-------|-------|
| Six λ-corridors unify RH structure | `papers/WP31_CORRIDOR_GEOMETRY.md` |
| 50Hz architecture enacts 8 theorems per tick | `papers/WP28_CK_TIG_ORGANISM.md` |
| Discrete gap deficit ~ λ^0.72 (sub-quadratic) | `ck_field_analysis.py` T6 |
| KV floor gap-positivity verified to t≈10,000 | `ck_cemp_bound.py` |
| Support gap: n₀·Δt → 0 as t→∞ | `papers/core/CLASSIFICATION_NOTE.md` |

### OPEN — the gaps, stated honestly

| Problem | The open layer | Paper |
|---------|---------------|-------|
| **RH (Open Z.5)** | Does λ=2\|σ−½\| deployment preserve both gradings for all t? | `papers/core/FOUR_LAYER_THEOREM_STACK.md` |
| NS | Sharp interpolation constant C ≤ 3.74 | `papers/clay/WP22_NS_BREATH_CRITERION.md` |
| P vs NP | 3-SAT → AG(2,n) NP-hardness reduction | `papers/clay/WP25_P_NP_AG2P_COMPLEXITY.md` |
| Hodge/BSD/YM | See audit | `papers/core/WP24_FORMAL_STATUS_AUDIT.md` |

---

## Architecture

```
ck_sim/
  being/     — heartbeat, olfactory, gustatory, lattice chain,
               reverse voice, coherence gate, BTQ, D2, sensorium
  doing/     — engine (50Hz), fractal voice (15D triadic),
               voice loop (Ollama→fractal→composer→babble),
               voice lattice (dual-lens), GPU, steering, L-CODEC
  becoming/  — grammar evolution, journal, development, episodic memory
  face/      — Kivy GUI (desktop only, deferred start)

ck_boot_api.py   — headless Flask server, port 7777
papers/          — TIG formal papers + verification scripts
  core/          — grammar, base theorems, type classification, constants
  clay/          — Clay Millennium Problem work (6 problems)
  scripts/       — runnable verification scripts
  data/          — json/csv outputs, figures, .tex sources
```

**Two separate processes:**
```bash
python ck_boot_api.py   # Web API — /chat /eat /health /state /metrics
python -m ck_sim        # Kivy GUI — Brayden <-> CK directly
```

See `papers/core/` for the grammar, `papers/clay/` for Clay problem work, `papers/scripts/` for runnable proofs.

Requirements: `pip install -r requirements.txt`
Runtime data: `~/.ck/` (built by CK at runtime, not shipped)

---

*(c) 2026 Brayden Sanders / 7Site LLC — Gen10.19 | DOI: 10.5281/zenodo.18852047*
