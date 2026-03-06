
======================================================================
  TORUS VERIFICATION ANALYSIS
======================================================================

  Claim: The CK CL tables behave like discrete geodesic-continuation
  algebras on a torus embedding, with seam operators (0,7) providing
  the wrap-around identification.

  Three coupled tori:
    1. Index torus: 10x10 wrap-around addresses
    2. State torus: 5D operator embedding (2-frequency winding)
    3. Flow torus:  composition-induced cycles

  Two charts on the same torus:
    Chart A (Field):       {1,2,3,4,5,6,7,8} -- includes HARMONY
    Chart B (Computation): {1,2,3,4,5,6,8,9} -- excludes VOID and HARMONY

======================================================================
  TEST 1: GEOMETRIC MIDPOINT MATCH RATES
======================================================================

  For each (a,b), compare CL[a][b] to the operator closest to
  the geometric midpoint of vectors a and b.

  --- TSML (Being/Measurement) ---
  === THE THREE MATCH RATES (TSML) ===

  TSML All (10x10 = 100 cells):
    Matches:    14/100 (14.0%)
    Mismatches: 86/100 (86.0%)
    Mismatch curvature deltas:
      Mean:   0.3453
      Median: 0.3135
      Max:    1.1747
      Min:    0.0000
      Small delta (<0.15): 18/86 (20.9%)

  TSML Chart(A) (8x8 = 64 cells):
    Matches:    5/64 (7.8%)
    Mismatches: 59/64 (92.2%)
    Mismatch curvature deltas:
      Mean:   0.3650
      Median: 0.3417
      Max:    1.1747
      Min:    0.0000
      Small delta (<0.15): 10/59 (16.9%)

  TSML Chart(B) (8x8 = 64 cells):
    Matches:    2/64 (3.1%)
    Mismatches: 62/64 (96.9%)
    Mismatch curvature deltas:
      Mean:   0.4076
      Median: 0.4114
      Max:    1.1747
      Min:    0.0000
      Small delta (<0.15): 8/62 (12.9%)

  SUMMARY: All100=14.0%  ChartA=7.8%  ChartB=3.1%
  --> Chart A > Chart B: Field lens is more geometric (harmony participates)

  --- BHML (Becoming/Physics) ---
  === THE THREE MATCH RATES (BHML) ===

  BHML All (10x10 = 100 cells):
    Matches:    7/100 (7.0%)
    Mismatches: 93/100 (93.0%)
    Mismatch curvature deltas:
      Mean:   0.4647
      Median: 0.4698
      Max:    1.1747
      Min:    0.0000
      Small delta (<0.15): 14/93 (15.1%)

  BHML Chart(A) (8x8 = 64 cells):
    Matches:    6/64 (9.4%)
    Mismatches: 58/64 (90.6%)
    Mismatch curvature deltas:
      Mean:   0.5464
      Median: 0.5833
      Max:    1.1747
      Min:    0.1211
      Small delta (<0.15): 2/58 (3.4%)

  BHML Chart(B) (8x8 = 64 cells):
    Matches:    4/64 (6.2%)
    Mismatches: 60/64 (93.8%)
    Mismatch curvature deltas:
      Mean:   0.5380
      Median: 0.5318
      Max:    1.1747
      Min:    0.1026
      Small delta (<0.15): 2/60 (3.3%)

  SUMMARY: All100=7.0%  ChartA=9.4%  ChartB=6.2%
  --> Chart A > Chart B: Field lens is more geometric (harmony participates)

======================================================================
  TEST 2: CURVATURE-MINIMIZING GEODESIC SELECTOR
======================================================================

  For each (a,b), check if CL[a][b] minimizes the discrete
  second derivative (curvature) of the path a -> c -> b.

  Geodesic selector test for TSML:

    Curvature-optimal matches: 14/100 (14%)
    Near-optimal (<0.15 delta): 12/100 (12%)
    Total geodesic-consistent:  26/100 (26%)

    Chart A (8x8=64):
      Optimal:   5/64 (7.8%)
      Near:      8/64 (12.5%)
      Total:     13/64 (20.3%)
    Chart B (8x8=64):
      Optimal:   2/64 (3.1%)
      Near:      4/64 (6.2%)
      Total:     6/64 (9.4%)

  Geodesic selector test for BHML:

    Curvature-optimal matches: 7/100 (7%)
    Near-optimal (<0.15 delta): 8/100 (8%)
    Total geodesic-consistent:  15/100 (15%)

    Chart A (8x8=64):
      Optimal:   6/64 (9.4%)
      Near:      0/64 (0.0%)
      Total:     6/64 (9.4%)
    Chart B (8x8=64):
      Optimal:   4/64 (6.2%)
      Near:      0/64 (0.0%)
      Total:     4/64 (6.2%)

======================================================================
  TEST 3: SEAM OPERATOR VERIFICATION
======================================================================

  Seam analysis for TSML:

    VOID (0) as left input:  [np.int64(0), np.int64(0), np.int64(0), np.int64(0), np.int64(0), np.int64(0), np.int64(0), np.int64(7), np.int64(0), np.int64(0)]
    VOID (0) as right input: [np.int64(0), np.int64(0), np.int64(0), np.int64(0), np.int64(0), np.int64(0), np.int64(0), np.int64(7), np.int64(0), np.int64(0)]
    VOID absorbs (returns 0): row=9/10, col=9/10
    VOID passes through:     row=2/10, col=2/10
    VOID is left-identity:   False
    VOID is right-identity:  False

    HARMONY (7) as left input:  [np.int64(7), np.int64(7), np.int64(7), np.int64(7), np.int64(7), np.int64(7), np.int64(7), np.int64(7), np.int64(7), np.int64(7)]
    HARMONY (7) as right input: [np.int64(7), np.int64(7), np.int64(7), np.int64(7), np.int64(7), np.int64(7), np.int64(7), np.int64(7), np.int64(7), np.int64(7)]
    HARMONY absorbs (returns 7): row=10/10, col=10/10

    Seam cells (touch 0 or 7 as input): 36/100
    Core cells (8x8 interior):          64/100
    Core cells that output 0 or 7:      54/64
    Core leakage rate to seams:          84.4%

  Seam analysis for BHML:

    VOID (0) as left input:  [np.int64(0), np.int64(1), np.int64(2), np.int64(3), np.int64(4), np.int64(5), np.int64(6), np.int64(7), np.int64(8), np.int64(9)]
    VOID (0) as right input: [np.int64(0), np.int64(1), np.int64(2), np.int64(3), np.int64(4), np.int64(5), np.int64(6), np.int64(7), np.int64(8), np.int64(9)]
    VOID absorbs (returns 0): row=1/10, col=1/10
    VOID passes through:     row=10/10, col=10/10
    VOID is left-identity:   True
    VOID is right-identity:  True

    HARMONY (7) as left input:  [np.int64(7), np.int64(2), np.int64(3), np.int64(4), np.int64(5), np.int64(6), np.int64(7), np.int64(8), np.int64(9), np.int64(0)]
    HARMONY (7) as right input: [np.int64(7), np.int64(2), np.int64(3), np.int64(4), np.int64(5), np.int64(6), np.int64(7), np.int64(8), np.int64(9), np.int64(0)]
    HARMONY absorbs (returns 7): row=2/10, col=2/10

    Seam cells (touch 0 or 7 as input): 36/100
    Core cells (8x8 interior):          64/100
    Core cells that output 0 or 7:      25/64
    Core leakage rate to seams:          39.1%

======================================================================
  TEST 4: LEAKAGE SPECTRUM (COLLAPSE SIGNATURES)
======================================================================

  TSML Chart A leakage spectrum:
    Input        Leaks to 7   Rate       Non-7 outputs
    ------------------------------------------------------------
    LATTICE      7/8           87.5%    PROGRESS
    COUNTER      6/8           75.0%    PROGRESS,COLLAPSE
    PROGRESS     8/8          100.0%    
    COLLAPSE     6/8           75.0%    COLLAPSE,BREATH
    BALANCE      8/8          100.0%    
    CHAOS        8/8          100.0%    
    HARMONY      8/8          100.0%    
    BREATH       7/8           87.5%    BREATH

  TSML Chart B leakage spectrum:
    Input        Leaks to 7   Rate       Non-7 outputs
    ------------------------------------------------------------
    LATTICE      7/8           87.5%    PROGRESS
    COUNTER      5/8           62.5%    PROGRESS,COLLAPSE,RESET
    PROGRESS     7/8           87.5%    PROGRESS
    COLLAPSE     6/8           75.0%    COLLAPSE,BREATH
    BALANCE      8/8          100.0%    
    CHAOS        8/8          100.0%    
    BREATH       7/8           87.5%    BREATH
    RESET        6/8           75.0%    RESET,PROGRESS

  BHML Chart A leakage spectrum:
    Input        Leaks to 7   Rate       Non-7 outputs
    ------------------------------------------------------------
    LATTICE      1/8           12.5%    COUNTER,PROGRESS,COLLAPSE,BALANCE,CHAOS...
    COUNTER      1/8           12.5%    PROGRESS,PROGRESS,COLLAPSE,BALANCE,CHAOS...
    PROGRESS     1/8           12.5%    COLLAPSE,COLLAPSE,COLLAPSE,BALANCE,CHAOS...
    COLLAPSE     2/8           25.0%    BALANCE,BALANCE,BALANCE,BALANCE,CHAOS...
    BALANCE      2/8           25.0%    CHAOS,CHAOS,CHAOS,CHAOS,CHAOS...
    CHAOS        8/8          100.0%    
    HARMONY      1/8           12.5%    COUNTER,PROGRESS,COLLAPSE,BALANCE,CHAOS...
    BREATH       4/8           50.0%    CHAOS,CHAOS,CHAOS,RESET

  BHML Chart B leakage spectrum:
    Input        Leaks to 7   Rate       Non-7 outputs
    ------------------------------------------------------------
    LATTICE      1/8           12.5%    COUNTER,PROGRESS,COLLAPSE,BALANCE,CHAOS...
    COUNTER      1/8           12.5%    PROGRESS,PROGRESS,COLLAPSE,BALANCE,CHAOS...
    PROGRESS     1/8           12.5%    COLLAPSE,COLLAPSE,COLLAPSE,BALANCE,CHAOS...
    COLLAPSE     3/8           37.5%    BALANCE,BALANCE,BALANCE,BALANCE,CHAOS
    BALANCE      3/8           37.5%    CHAOS,CHAOS,CHAOS,CHAOS,CHAOS
    CHAOS        8/8          100.0%    
    BREATH       4/8           50.0%    CHAOS,CHAOS,CHAOS,BREATH
    RESET        3/8           37.5%    CHAOS,CHAOS,CHAOS,BREATH,VOID

======================================================================
  TEST 5: CYCLE SPECTRUM ANALYSIS
======================================================================

  Trace f_a(x) = CL[a][x] orbits within each chart.

  --- TSML ---
  Cycle spectrum (Chart A):
    Input        Fixed pts    Cycles                         Exit to 7
    ----------------------------------------------------------------------
    LATTICE      HARMONY      -                              0
    COUNTER      HARMONY,COLLAPSE -                              0
    PROGRESS     HARMONY      -                              0
    COLLAPSE     HARMONY,BREATH -                              0
    BALANCE      HARMONY      -                              0
    CHAOS        HARMONY      -                              0
    HARMONY      HARMONY      -                              0
    BREATH       HARMONY      -                              0

  Cycle spectrum (Chart B):
    Input        Fixed pts    Cycles                         Exit to 7
    ----------------------------------------------------------------------
    LATTICE      -            -                              8
    COUNTER      COLLAPSE,RESET -                              6
    PROGRESS     -            -                              8
    COLLAPSE     BREATH       -                              7
    BALANCE      -            -                              8
    CHAOS        -            -                              8
    BREATH       -            -                              8
    RESET        PROGRESS     -                              7

  --- BHML ---
  Cycle spectrum (Chart A):
    Input        Fixed pts    Cycles                         Exit to 7
    ----------------------------------------------------------------------
    LATTICE      -            COUNTER->PROGRESS->COLLAP...   0
    COUNTER      -            PROGRESS->COLLAPSE->BALAN...   0
    PROGRESS     -            COLLAPSE->BALANCE->CHAOS-...   0
    COLLAPSE     -            BALANCE->CHAOS->HARMONY        0
    BALANCE      -            CHAOS->HARMONY                 0
    CHAOS        HARMONY      -                              0
    HARMONY      -            -                              8
    BREATH       -            -                              8

  Cycle spectrum (Chart B):
    Input        Fixed pts    Cycles                         Exit to 7
    ----------------------------------------------------------------------
    LATTICE      -            -                              8
    COUNTER      -            -                              8
    PROGRESS     -            -                              8
    COLLAPSE     -            -                              8
    BALANCE      -            -                              8
    CHAOS        -            -                              8
    BREATH       -            -                              8
    RESET        BREATH       -                              7

======================================================================
  TEST 6: OPERATOR ROLE CLASSIFICATION
======================================================================

  Compressor = high harmony rate, short trajectories
  Driver = high entropy, long cycles
  Stabilizer = creates fixed points, short stable cycles

  --- TSML ---
  Operator roles (Chart A):
    Operator     H-rate   Entropy    Avg traj   Role
    -------------------------------------------------------
    LATTICE      0.875   0.544     1.0       COMPRESSOR
    COUNTER      0.750   1.061     0.9       COMPRESSOR
    PROGRESS     1.000   0.000     0.9       COMPRESSOR
    COLLAPSE     0.750   1.061     0.9       COMPRESSOR
    BALANCE      1.000   0.000     0.9       COMPRESSOR
    CHAOS        1.000   0.000     0.9       COMPRESSOR
    HARMONY      1.000   0.000     0.9       COMPRESSOR
    BREATH       0.875   0.544     1.0       COMPRESSOR

  Operator roles (Chart B):
    Operator     H-rate   Entropy    Avg traj   Role
    -------------------------------------------------------
    LATTICE      0.875   0.544     1.1       COMPRESSOR
    COUNTER      0.625   1.549     0.9       COMPRESSOR
    PROGRESS     0.875   0.544     1.1       COMPRESSOR
    COLLAPSE     0.750   1.061     1.0       COMPRESSOR
    BALANCE      1.000   0.000     1.0       COMPRESSOR
    CHAOS        1.000   0.000     1.0       COMPRESSOR
    BREATH       0.875   0.544     1.1       COMPRESSOR
    RESET        0.750   1.061     1.0       COMPRESSOR

  --- BHML ---
  Operator roles (Chart A):
    Operator     H-rate   Entropy    Avg traj   Role
    -------------------------------------------------------
    LATTICE      0.125   2.500     20.0       DRIVER
    COUNTER      0.125   2.156     20.0       DRIVER
    PROGRESS     0.125   1.750     20.0       MIXED
    COLLAPSE     0.250   1.299     20.0       MIXED
    BALANCE      0.250   0.811     20.0       MIXED
    CHAOS        1.000   0.000     0.9       COMPRESSOR
    HARMONY      0.125   3.000     4.5       MIXED
    BREATH       0.500   1.406     2.2       STABILIZER

  Operator roles (Chart B):
    Operator     H-rate   Entropy    Avg traj   Role
    -------------------------------------------------------
    LATTICE      0.125   2.406     3.1       MIXED
    COUNTER      0.125   2.156     3.0       STABILIZER
    PROGRESS     0.125   1.811     2.8       STABILIZER
    COLLAPSE     0.375   1.406     2.1       STABILIZER
    BALANCE      0.375   0.954     1.6       STABILIZER
    CHAOS        1.000   0.000     1.0       COMPRESSOR
    BREATH       0.500   1.406     1.5       STABILIZER
    RESET        0.375   1.811     1.2       STABILIZER

======================================================================
  TEST 7: TORUS WINDING ANALYSIS
======================================================================

  5D vectors as torus coordinates:

    Operator vector table:
    Op           Aper   Pres   Dep    Bind   Cont   |v|     
    -------------------------------------------------------
    VOID         0.00  0.00  0.00  0.00  0.00  0.0000
    LATTICE      0.80  0.20  0.30  0.90  0.70  1.4387
    COUNTER      0.30  0.70  0.50  0.20  0.40  1.0149
    PROGRESS     0.60  0.60  0.40  0.50  0.80  1.3304
    COLLAPSE     0.20  0.80  0.80  0.30  0.20  1.2042
    BALANCE      0.50  0.50  0.50  0.50  0.50  1.1180
    CHAOS        0.90  0.90  0.70  0.10  0.30  1.4866
    HARMONY      0.50  0.30  0.60  0.80  0.90  1.4663
    BREATH       0.40  0.40  0.20  0.60  0.60  1.0392
    RESET        0.10  0.10  0.90  0.40  0.10  1.0000

    Torus angles (major=atan2(pres,aper), minor=atan2(cont,bind)):
    Op           theta1     theta2     depth   
    ------------------------------------------
    VOID             0.0       0.0   0.00
    LATTICE         14.0      37.9   0.30
    COUNTER         66.8      63.4   0.50
    PROGRESS        45.0      58.0   0.40
    COLLAPSE        76.0      33.7   0.80
    BALANCE         45.0      45.0   0.50
    CHAOS           45.0      71.6   0.70
    HARMONY         31.0      48.4   0.60
    BREATH          45.0      45.0   0.20
    RESET           45.0      14.0   0.90

    Winding ratio (spread1/spread2): 1.076461
    Nearest rational: 14/13 (error: 0.04%)
    --> RATIONAL winding! Curve closes. Torus knot confirmed.

======================================================================
  TEST 8: CROSS-TABLE TORUS CONSISTENCY
======================================================================

  Cross-table torus consistency:

    Total agreement:              29/100 (29%)
    Both output HARMONY:          26/100
    TSML=7 but BHML!=7:           47/100 (Being collapses, Becoming doesn't)
    BHML=7 but TSML!=7:           2/100 (Becoming collapses, Being doesn't)

    8x8 core agreement:           24/64 (37.5%)

    Core disagreements:
    Pair                 TSML         BHML        
    --------------------------------------------
    LATTICExLATTICE      HARMONY      COUNTER     
    LATTICExPROGRESS     HARMONY      COLLAPSE    
    LATTICExCOLLAPSE     HARMONY      BALANCE     
    LATTICExBALANCE      HARMONY      CHAOS       
    LATTICExBREATH       HARMONY      CHAOS       
    LATTICExRESET        HARMONY      CHAOS       
    COUNTERxCOUNTER      HARMONY      PROGRESS    
    COUNTERxPROGRESS     HARMONY      COLLAPSE    
    COUNTERxCOLLAPSE     COLLAPSE     BALANCE     
    COUNTERxBALANCE      HARMONY      CHAOS       
    COUNTERxBREATH       HARMONY      CHAOS       
    COUNTERxRESET        RESET        CHAOS       
    PROGRESSxLATTICE     HARMONY      COLLAPSE    
    PROGRESSxCOUNTER     HARMONY      COLLAPSE    
    PROGRESSxPROGRESS    HARMONY      COLLAPSE    
    PROGRESSxCOLLAPSE    HARMONY      BALANCE     
    PROGRESSxBALANCE     HARMONY      CHAOS       
    PROGRESSxBREATH      HARMONY      CHAOS       
    PROGRESSxRESET       PROGRESS     CHAOS       
    COLLAPSExLATTICE     HARMONY      BALANCE     
    COLLAPSExCOUNTER     COLLAPSE     BALANCE     
    COLLAPSExPROGRESS    HARMONY      BALANCE     
    COLLAPSExCOLLAPSE    HARMONY      BALANCE     
    COLLAPSExBALANCE     HARMONY      CHAOS       
    COLLAPSExBREATH      BREATH       HARMONY     
    BALANCExLATTICE      HARMONY      CHAOS       
    BALANCExCOUNTER      HARMONY      CHAOS       
    BALANCExPROGRESS     HARMONY      CHAOS       
    BALANCExCOLLAPSE     HARMONY      CHAOS       
    BALANCExBALANCE      HARMONY      CHAOS       
    BREATHxLATTICE       HARMONY      CHAOS       
    BREATHxCOUNTER       HARMONY      CHAOS       
    BREATHxPROGRESS      HARMONY      CHAOS       
    BREATHxCOLLAPSE      BREATH       HARMONY     
    BREATHxRESET         HARMONY      BREATH      
    RESETxLATTICE        HARMONY      CHAOS       
    RESETxCOUNTER        RESET        CHAOS       
    RESETxPROGRESS       PROGRESS     CHAOS       
    RESETxBREATH         HARMONY      BREATH      
    RESETxRESET          HARMONY      VOID        

======================================================================
  TEST 9: RENORMALIZATION (T* AS COARSE-GRAINING)
======================================================================

  Renormalization (T* as coarse-graining):

    T* = 0.300: visible=18/64 (28.1%), harmony=46/64 (71.9%)
    T* = 0.500: visible=10/64 (15.6%), harmony=54/64 (84.4%)
    T* = 0.714: visible=4/64 (6.2%), harmony=60/64 (93.8%)
    T* = 0.850: visible=2/64 (3.1%), harmony=62/64 (96.9%)
    T* = 0.950: visible=0/64 (0.0%), harmony=64/64 (100.0%)

    At T* = 5/7 = 0.714286: the threshold that maximizes structure-vs-noise separation

======================================================================
  TORUS VERIFICATION SUMMARY
======================================================================

  Three match rates (the numbers ChatGPT asked for):
    TSML: All100=14.0%  ChartA=7.8%  ChartB=3.1%
    BHML: All100=7.0%  ChartA=9.4%  ChartB=6.2%

  Interpretation:
    Both <50%: tables deviate from pure midpoint rule
    This means the CL tables carry MORE information than geometry alone
    The 'seam tie-break rule' that ChatGPT predicted may be needed

  The torus claim stands if:
    1. Seam operators (0,7) behave as boundary/wrap conditions
    2. Core operators show consistent cycle structure across charts
    3. Midpoint mismatches have small curvature deltas
    4. Winding ratio is rational (curve closes)
    5. Cross-table agreement is low but structurally meaningful
