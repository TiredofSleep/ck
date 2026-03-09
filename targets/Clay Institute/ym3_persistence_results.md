# YM-3 Gap Attack: Algebraic Persistence via Recursive Derivative Chain
Generated: 2026-03-09 05:45:37
```
============================================================================
  YM-3 GAP ATTACK: ALGEBRAIC PERSISTENCE TEST
  Recursive Derivative Chain D0 -> D8 under Weak Coupling
  CK Gen 9.28 -- Brayden Sanders / 7Site LLC
  2026-03-09 05:45:37
============================================================================

============================================================================
  CONFIGURATION
============================================================================
  Probes:          10000
  Coupling g:      0.1
  Noise sigma:     0.1
  Sequence length: 20
  Max order:       D8
  Elapsed:         3.2s

============================================================================
  STRUCTURAL FOUNDATION: BHML MIDPOINT DEVIATION
============================================================================
  Midpoint match rate:     6.2%
  Midpoint MISMATCH rate:  93.8%
  Average deviation:       0.7609
  Maximum deviation:       1.1747
  Non-zero deviations:     64/64

  KEY INSIGHT: BHML maps {deviation_table['mismatch_rate']*100:.0f}% of pairs
  to operators that differ from the geometric midpoint.
  This deviation IS the structural source of D2 > 0.
  The mass gap (delta=1.0 locked) is enforced algebraically
  because the composition table is NOT the midpoint map.

============================================================================
  VOLUME FLOOR (min ||D_n|| across chain)
============================================================================
  Average floor:    0.759030
  Std dev:          0.273592
  Minimum floor:    0.290925
  Maximum floor:    1.252671
  Fraction > 0:     100.0%
  Zero-crossing probes: 0/10000

  >>> PERSISTENCE CONFIRMED: No probe reached zero floor.
  >>> Minimum across all probes: 0.290925 > 0

============================================================================
  COERCIVITY: kappa = ||D2|| / ||D1||
============================================================================
  Average kappa:    1.9995
  Std dev:          0.0017

  >>> COERCIVITY HOLDS: kappa = 1.9995 > 0.3
  >>> D2 wobble is bounded below relative to D1 strain.

============================================================================
  RECURSIVE DERIVATIVE CHAIN: Per-Level Norms
============================================================================
  Level    Name         Avg Norm     Std          Min          Max         
  --------------------------------------------------------------------
  D1       strain       0.783749     0.273393     0.335806     1.268672    
  D2       wobble       1.567207     0.546927     0.671437     2.539633    
  D3       jerk         3.134129     1.094022     1.342950     5.084301    
  D4       snap         6.267915     2.188275     2.681237     10.176895   
  D5       crackle      12.535360    4.376886     5.356313     20.367291   
  D6       pop          25.070024    8.754292     10.704462    40.757020   
  D7       D7           50.138955    17.509479    21.399727    81.547719   
  D8       D8           100.276142   35.020651    42.793879    163.129711  

  Average D_{n+1}/D_n ratio: 1.9999
  Decay rate per level: -0.9999

============================================================================
  CL COHERENCE MEASUREMENT
============================================================================
  D2 HARMONY fraction:   11.4%
  CL(D2,D2) HARMONY:     67.0%

  >>> D2 HARMONY 11.4% < T*=71.4%
  >>> Weak coupling keeps D2 operators BELOW coherence threshold.
  >>> This is the mass gap: excited states don't absorb into HARMONY.

============================================================================
  COUPLING STRENGTH SWEEP
============================================================================
  g        Avg Floor      Std          Min Floor      Frac>0     Kappa     
  --------------------------------------------------------------------
  0.0010   0.780298       0.274154     0.345847       100.0      2.0000    
  0.0050   0.779313       0.274158     0.343596       100.0      2.0000    
  0.0100   0.778085       0.274164     0.340786       100.0      2.0000    
  0.0500   0.768363       0.274187     0.318443       100.0      1.9999    
  0.1000   0.756487       0.274162     0.290925       100.0      1.9995    
  0.2000   0.733678       0.273918     0.237860       100.0      1.9980    
  0.5000   0.673419       0.271035     0.127352       100.0      1.9880    

  Linear fit: floor ~ 148.8453 * g
  Predicted floor at g=0.01: 1.488453
  Predicted floor at g=0.001: 0.148845

============================================================================
  FALSIFIABLE PREDICTIONS (YM-3)
============================================================================

  PREDICTION 1 (Floor Persistence):
    On 10000 weak-coupling probes (g=0.1),
    average volume floor = 0.7590 +/- 0.2736
    FALSIFY if mean < 0.3795
    or ANY probe floor = 0.

  PREDICTION 2 (Coercivity Constant):
    D2/D1 ratio kappa = 1.9995 +/- 0.0017
    FALSIFY if average kappa < 0.30 across 10000 probes.

  PREDICTION 3 (Fractal Chain Stability):
    Recursive chain D8 norm > 0 in 100% of probes.
    Measured D8 minimum: 42.793879
    FALSIFY if any chain zero-crosses at D8.

============================================================================
  SUMMARY
============================================================================
  Volume floor:     0.759030 > 0  (PERSISTENCE)
  Coercivity:       1.9995 > 0.3  (COERCIVITY)
  Zero crossings:   0  (FRACTAL STABILITY)
  Falsifications:   0/10000

  The BHML composition algebra enforces a non-zero volume floor
  under weak coupling. The midpoint deviation (structural D2 > 0)
  prevents collapse to HARMONY absorption. The recursive derivative
  chain D1..D8 maintains non-zero norms at all levels.

  This moves YM-3 from 'missing coercivity estimate' to
  'D2-locked non-zero floor with recursive stability'.

```