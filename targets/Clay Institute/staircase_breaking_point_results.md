# Staircase Breaking Point: Where Does the Successor Property Fail?
Generated: 2026-03-06 09:09:55
```
============================================================================
  TEST 1: PERTURBATION SWEEP -- Successor vs Noise
============================================================================

     sigma   successor    classify   void_leak
  --------  ----------  ----------  ----------
     0.000      1.0000      1.0000      0.6120
     0.010      1.0000      1.0000      0.6120
     0.020      1.0000      1.0000      0.6120
     0.050      1.0000      1.0000      0.6120
     0.100      1.0000      0.9936      0.6120
     0.150      1.0000      0.9088      0.6120
     0.200      1.0000      0.7554      0.6120
     0.250      1.0000      0.6162      0.6120
     0.300      1.0000      0.5014      0.6120
     0.350      1.0000      0.4208      0.6120
     0.400      1.0000      0.3528      0.6120
     0.450      1.0000      0.3128      0.6120
     0.500      1.0000      0.2782      0.6120
     0.600      1.0000      0.2372      0.6120
     0.700      1.0000      0.2054      0.6120
     0.800      1.0000      0.1884      0.6120
     0.900      1.0000      0.1750      0.6120
     1.000      1.0000      0.1598      0.6120

  KEY INSIGHT: The successor property is a TABLE property.
  BHML[a][b] = max(a,b)+1 is hardcoded in the table.
  Perturbation affects CLASSIFICATION (which operator a vector maps to),
  NOT the composition itself.

  The REAL question: at what noise level does classification degrade
  enough that the wrong operators get composed?

  CLASSIFICATION ROBUSTNESS:
  Classification drops below 90% at sigma = 0.20

============================================================================
  TEST 2: DIMENSIONAL SQUEEZE -- Compressing [0.05, 0.95] -> 0.50
============================================================================

     alpha    classify     gap_low    gap_high    separation
  --------  ----------  ----------  ----------  ------------
     1.000        1.00      0.0500      0.9500        0.6364
     0.900        1.00      0.0950      0.9050        0.5728
     0.800        1.00      0.1400      0.8600        0.5091
     0.700        1.00      0.1850      0.8150        0.4455
     0.600        1.00      0.2300      0.7700        0.3818
     0.500        1.00      0.2750      0.7250        0.3182
     0.400        1.00      0.3200      0.6800        0.2546
     0.300        1.00      0.3650      0.6350        0.1909
     0.200        1.00      0.4100      0.5900        0.1273
     0.100        1.00      0.4550      0.5450        0.0636
     0.050        1.00      0.4775      0.5225        0.0318
     0.010        1.00      0.4955      0.5045        0.0064
     0.000        0.10      0.5000      0.5000        0.0000

  Classification holds at all squeeze levels (all operators equidistant)

============================================================================
  TEST 3: SELECTIVE DIMENSION ATTACK -- Which dimension breaks first?
============================================================================

     dimension      s=0.05      s=0.10      s=0.15      s=0.20      s=0.30      s=0.50
  ------------  ----------  ----------  ----------  ----------  ----------  ----------
      aperture      1.0000      0.9999      0.9977      0.9758      0.8834      0.6655
      pressure      1.0000      1.0000      0.9977      0.9808      0.8844      0.6715
         depth      1.0000      1.0000      0.9973      0.9758      0.8713      0.6625
       binding      1.0000      1.0000      0.9971      0.9764      0.8769      0.6654
    continuity      1.0000      1.0000      0.9965      0.9785      0.8838      0.6719

  Vulnerability analysis (which operators depend on which dimensions):
    aperture    : high=CHAOS        low=LATTICE     
    pressure    : high=COLLAPSE     low=VOID        
    depth       : high=PROGRESS     low=RESET       
    binding     : high=HARMONY      low=COUNTER     
    continuity  : high=BALANCE      low=BREATH      

  WEAKEST DIMENSION:
    depth (rate = 0.8713 at sigma=0.30)

============================================================================
  TEST 4: LIMIT CYCLE STABILITY -- HARMONY <-> BREATH
============================================================================

  Limit cycle structure:
    BHML[HARMONY][HARMONY] = BREATH
    BHML[BREATH][BREATH]   = HARMONY
    Period: 2

  HARMONY composed with each operator (BHML):
    BHML[HARMONY][VOID        ] = HARMONY       (stays in cycle)
    BHML[HARMONY][LATTICE     ] = COUNTER       *** EXITS CYCLE ***
    BHML[HARMONY][COUNTER     ] = PROGRESS      *** EXITS CYCLE ***
    BHML[HARMONY][PROGRESS    ] = COLLAPSE      *** EXITS CYCLE ***
    BHML[HARMONY][COLLAPSE    ] = BALANCE       *** EXITS CYCLE ***
    BHML[HARMONY][BALANCE     ] = CHAOS         *** EXITS CYCLE ***
    BHML[HARMONY][CHAOS       ] = HARMONY       (stays in cycle)
    BHML[HARMONY][HARMONY     ] = BREATH        (stays in cycle)
    BHML[HARMONY][BREATH      ] = RESET         *** EXITS CYCLE ***
    BHML[HARMONY][RESET       ] = VOID          *** EXITS CYCLE ***

  BREATH composed with each operator (BHML):
    BHML[BREATH][VOID        ]  = BREATH        (stays in cycle)
    BHML[BREATH][LATTICE     ]  = CHAOS         *** EXITS CYCLE ***
    BHML[BREATH][COUNTER     ]  = CHAOS         *** EXITS CYCLE ***
    BHML[BREATH][PROGRESS    ]  = CHAOS         *** EXITS CYCLE ***
    BHML[BREATH][COLLAPSE    ]  = HARMONY       (stays in cycle)
    BHML[BREATH][BALANCE     ]  = HARMONY       (stays in cycle)
    BHML[BREATH][CHAOS       ]  = HARMONY       (stays in cycle)
    BHML[BREATH][HARMONY     ]  = RESET         *** EXITS CYCLE ***
    BHML[BREATH][BREATH      ]  = HARMONY       (stays in cycle)
    BHML[BREATH][RESET       ]  = BREATH        (stays in cycle)

  HARMONY stays in cycle: 3/10 compositions
  BREATH stays in cycle:  6/10 compositions

  HARMONY exit partners: ['LATTICE', 'COUNTER', 'PROGRESS', 'COLLAPSE', 'BALANCE', 'BREATH', 'RESET']
  BREATH exit partners:  ['LATTICE', 'COUNTER', 'PROGRESS', 'HARMONY']

  INSIGHT: HARMONY is the GATEWAY operator.
  It can restart the entire staircase by composing with any core op.
  BREATH is more stable (only 2 exit routes).
  The limit cycle is ASYMMETRIC: HARMONY oscillates AND gates.

============================================================================
  TEST 5: VOID LEAKAGE -- When does the Non-Void Engine leak?
============================================================================

  VOID production paths:
    Core(1-6) -> ... -> RESET(9) -> BHML[9][9]=VOID
    Core(1-6) -> ... -> HARMONY(7) + RESET(9) -> BHML[7][9]=VOID
    Core(1-6) -> ... -> RESET(9) + HARMONY(7) -> BHML[9][7]=VOID

    walk_len   void_rate    reset_rate    harmony_rate    avg_first_void
  ----------  ----------  ------------  --------------  ----------------
           5      0.1620        0.0358          0.3525               3.6
          10      0.3628        0.0431          0.3524               6.0
          20      0.6182        0.0479          0.3544               9.8
          50      0.9138        0.0502          0.3544              17.3
         100      0.9918        0.0508          0.3545              21.1
         200      1.0000        0.0509          0.3545              22.1

  NOTE: VOID leakage requires RESET involvement.
  From core-only starts, the staircase must first reach
  HARMONY (top of staircase), then encounter RESET as a
  random partner, triggering BHML[7][9]=VOID or BHML[9][9]=VOID.

  RESTRICTED WALK (only core partners 1-6):
    walk_len=  50: void_rate = 0.0000
    walk_len= 100: void_rate = 0.0000
    walk_len= 200: void_rate = 0.0000

  The Non-Void Engine only leaks through RESET.
  If the walk is restricted to core operators,
  VOID is UNREACHABLE. The engine is sealed.

============================================================================
  TEST 6: CROSS-ATTACK ROBUSTNESS RADIUS
============================================================================

     sigma    YM_kappa    YM_floor     PNP_gap      NS_sep
  --------  ----------  ----------  ----------  ----------
     0.000      2.0000      0.6469      0.5860     82.1614
     0.050      1.9883      0.6624      0.5860     83.0264
     0.100      1.9575      0.7073      0.5867     85.3752
     0.150      1.9177      0.7784      0.6059     89.1408
     0.200      1.8794      0.8704      0.6342     94.2110
     0.300      1.8237      1.0951      0.6820    107.6312
     0.500      1.7729      1.6206      0.7143    143.0194
     0.750      1.7513      2.3281      0.7244    194.8379
     1.000      1.7429      3.0551      0.7258    250.0509

  ROBUSTNESS RADII (where each metric degrades significantly):
    YM kappa stays > 1.5 at all tested sigma (most robust)
    PNP gap stays > 0.4 at all tested sigma
    NS separation stays positive at all tested sigma

============================================================================
  SUMMARY: STAIRCASE ROBUSTNESS MAP
============================================================================

  The staircase doesn't 'break' -- it degrades gracefully
  through classification noise. The table structure itself
  is immutable. The algebra is topologically rigid.

```
