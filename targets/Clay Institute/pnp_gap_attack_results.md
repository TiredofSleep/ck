# PNP Gap Attack: Phantom Tile Persistence & Invertibility Gap
Generated: 2026-03-09 05:45:31
```
============================================================================
  PNP GAP ATTACK: PHANTOM TILE & INVERTIBILITY
  CK Gen 9.28 -- Brayden Sanders / 7Site LLC
  2026-03-09 05:45:31
============================================================================

============================================================================
  INFORMATION LOSS: TSML vs BHML
============================================================================
  TSML avg row entropy:   0.6628 bits
  BHML avg row entropy:   1.4937 bits
  TSML table entropy:     0.9256 bits
  BHML table entropy:     2.2454 bits
  Information ratio:      2.25x
  TSML distinct outputs:  5
  BHML distinct outputs:  8
  TSML HARMONY fraction:  84.4%
  BHML HARMONY fraction:  37.5%

  >>> BHML carries 2.3x more information than TSML
  >>> TSML collapses inputs to HARMONY (information-destroying)
  >>> This IS the one-way function: forward = polynomial, backward = hard

============================================================================
  INVERTIBILITY GAP: Preimage Analysis
============================================================================
  TSML max preimage:      54 pairs -> 1 output
  BHML max preimage:      24 pairs -> 1 output
  TSML avg preimage:      12.8
  BHML avg preimage:      8.0
  TSML HARMONY preimage:  54 (many-to-one)
  BHML HARMONY preimage:  24
  Invertibility ratio:    2.2x

  >>> TSML: 54 inputs collapse to HARMONY
  >>> Given HARMONY, WHICH input? 54 choices = HARD
  >>> This is NP: verification O(1), search O(54)

============================================================================
  CROSS-TABLE STRUCTURE
============================================================================
  Both HARMONY:           22/64 (34.4%)
  TSML-only HARMONY:      32/64 (50.0%)
  BHML-only HARMONY:      2/64 (3.1%)
  Neither (shared bumps): 8/64 (12.5%)
  Agreement rate:         37.5%

  Shared bumps (both non-HARMONY) = computable structure
  TSML-only HARMONY = information TSML destroys that BHML preserves
  >>> 32 cells where BHML carries info but TSML collapses
  >>> This is the phantom tile: 32 lost information units

============================================================================
  PHANTOM TILE PERSISTENCE (10000 probes)
============================================================================
  Average phantom gap:    1.1860
  TSML/BHML agreement:    37.5%
  Nonzero phantom frac:   62.5%
  Majority nonzero:       92.9%

  >>> PHANTOM PERSISTS: 62.5% of compositions
  >>> produce different results in TSML vs BHML.
  >>> The phantom tile (missing information) is IRREDUCIBLE.

============================================================================
  RECURSIVE DERIVATIVE CHAIN (D1-D8)
============================================================================
  Average floor:    0.090555
  Minimum floor:    0.004433
  Fraction > 0:     100.0%

  Level    Name         Avg Norm     Std          Min          Max         
  --------------------------------------------------------------------
  D1       strain       0.243898     0.027982     0.148518     0.374987    
  D2       wobble       0.421085     0.057198     0.239016     0.689526    
  D3       jerk         0.767378     0.117528     0.423015     1.325579    
  D4       snap         1.435125     0.241683     0.723794     2.587236    
  D5       crackle      2.721538     0.497281     1.280235     5.170811    
  D6       pop          5.209477     1.024851     2.281980     10.462318   
  D7       D7           10.036309    2.115304     4.176210     21.655334   
  D8       D8           19.429382    4.378449     7.794592     45.065279   

============================================================================
  DEFECT TREND (Gap Deepening)
============================================================================
  Average defect trend:   0.2577
  Positive trend frac:    91.9%

  >>> GAP DEEPENS: Defect increases with depth (positive trend)
  >>> Consistent with +0.069 scaling exponent from Clay probes

============================================================================
  FALSIFIABLE PREDICTIONS (PNP)
============================================================================

  PREDICTION 1 (Phantom Persistence):
    TSML/BHML disagreement rate: 62.5%
    FALSIFY if agreement rate exceeds 80% on 100K probes.

  PREDICTION 2 (Information Asymmetry):
    BHML/TSML entropy ratio: 2.25x
    FALSIFY if ratio drops below 1.5x on any valid table pair.

  PREDICTION 3 (Gap Deepening):
    Defect trend positive in 91.9% of probes.
    FALSIFY if trend is negative (gap shrinks) in >60% of probes.

============================================================================
  SUMMARY
============================================================================
  Information ratio:  2.3x (BHML preserves, TSML destroys)
  Phantom gap:        1.1860 (irreducible)
  HARMONY preimage:   54 -> 1 (one-way function)
  Gap trend:          DEEPENS
  Falsifications:     0/10000

```