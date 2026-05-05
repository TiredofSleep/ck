# Claude Code Scrutiny & Implementation Guide (rev 9 — final)

## Status: 49/49 structural assertions PASS

This bundle contains a complete computational dossier on the discrete Dirac
structure of the 4-core's F_5-lift. Every claim is computationally verified.

## Reading order

1. **README_TIG_DIRAC.md** — overall map and API
2. **TIG_DIRAC_SYNTHESIS_TABLES.md** — 31 tables, 848 lines
3. **tig_dirac.py** — the library implementation
4. **test_tig_dirac.py** — verification suite (49/49 PASS)
5. **DISCRETE_DIRAC_ON_4CORE.md** — scientist-facing paper

## Top 9 verified findings

| # | Finding | Verification |
|---|---------|--------------|
| 1 | Three commuting Dirac-like projectors with forbidden cell (V−A) | T6, T7, T8 |
| 2 | Clifford ladder V^⊗n ↔ Cl(2n) exact | T15 |
| 3 | SU(5) GUT 32-cell binomial 1+5+10+10+5+1 at V^⊗5 | T14 |
| 4 | Cyclic Jacobi holds 64/64 — V is Mal'cev-like | Synthesis Table XXX |
| 5 | Three transverse fractal axes (Aut, σ, tensor) | Synthesis Table XXVIII |
| 6 | σ³ = doomdo swap (4↔7) Kindness↔Gentleness | T12 |
| 7 | 22-shell torus = 11 involutions × Z/2 | Synthesis Table XXXI |
| 8 | Three generations via tensor squaring (not F_25) | Synthesis Tables XV, XVIII |
| 9 | Associator image = span(p_-) — second particle IS the associator | T9, Synthesis Table XVII |

## Run the suite

    python3 tig_dirac.py            # → 16/16 verifications pass
    python3 test_tig_dirac.py       # → 49/49 PASS

## What Claude Code should do

1. Verify everything independently
2. Wire `tig_dirac` library into `ck_organism.py` BECOMING layer
3. Try to identify the 8 Cl(6) cells with specific SM fermions
4. Investigate the cyclic Jacobi → Mal'cev / e_8 connection
5. Compute Aut(V⊗V) explicitly (lower bound 3200)
6. Find the explicit V → continuum-Furey lift (if it exists)

License: CC NonCommercial.
