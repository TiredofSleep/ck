# Reality Anchors -- CL Table Analysis Results
Generated: 2026-03-05 14:10:30
```
========================================================================
  REALITY ANCHORS -- Rigorous CL Table Analysis
  CK Gen 9.21 -- The Coherence Keeper
  Brayden Sanders / 7Site LLC
========================================================================

  Date: 2026-03-05 14:10:07
  T* = 5/7 = 0.714285714285714
  TSML HARMONY count: 73/100
  BHML HARMONY count: 31/100

========================================================================
  ANALYSIS 1: Markov Chain / Semigroup Analysis
========================================================================

--- TSML Table Statistics ---
  Total entries:     100
  HARMONY (7) count: 73
  HARMONY fraction:  73/100 = 0.7300
  T* = 5/7 =        0.7142857143
  Difference:        0.0157142857

--- Value Distribution in TSML ---
  0 (    VOID):  17 entries (17%)
  3 (PROGRESS):   4 entries (4%)
  4 (COLLAPSE):   2 entries (2%)
  7 ( HARMONY):  73 entries (73%)
  8 (  BREATH):   2 entries (2%)
  9 (   RESET):   2 entries (2%)

--- BHML Table Statistics ---
  HARMONY (7) count: 31
  HARMONY fraction:  31/100 = 0.3100

--- Value Distribution in BHML ---
  0 (    VOID):  17 entries (17%)
  1 ( LATTICE):   6 entries (6%)
  2 ( COUNTER):   2 entries (2%)
  3 (PROGRESS):   8 entries (8%)
  4 (COLLAPSE):   6 entries (6%)
  5 ( BALANCE):   6 entries (6%)
  6 (   CHAOS):  17 entries (17%)
  7 ( HARMONY):  31 entries (31%)
  8 (  BREATH):   3 entries (3%)
  9 (   RESET):   4 entries (4%)

--- Normalized Transition Matrix (TSML) ---
  Row sums before normalization:
        VOID: 7
     LATTICE: 59
     COUNTER: 58
    PROGRESS: 59
    COLLAPSE: 61
     BALANCE: 63
       CHAOS: 63
     HARMONY: 70
      BREATH: 64
       RESET: 61

--- Eigenvalues of Normalized TSML ---
  lambda_0: +1.0000000000 +0.0000000000i  |lambda| = 1.0000000000
  lambda_1: -0.3052126828 +0.0000000000i  |lambda| = 0.3052126828
  lambda_2: +0.2904422897 +0.0000000000i  |lambda| = 0.2904422897
  lambda_3: +0.0970128442 +0.0000000000i  |lambda| = 0.0970128442
  lambda_4: -0.0941267995 +0.0000000000i  |lambda| = 0.0941267995
  lambda_5: +0.0578666934 +0.0000000000i  |lambda| = 0.0578666934
  lambda_6: -0.0269078450 +0.0000000000i  |lambda| = 0.0269078450
  lambda_7: +0.0096931923 +0.0000000000i  |lambda| = 0.0096931923
  lambda_8: -0.0096844825 +0.0000000000i  |lambda| = 0.0096844825
  lambda_9: +0.0000000000 +0.0000000000i  |lambda| = 0.0000000000

--- Stationary Distribution (left eigenvector for lambda=1) ---
  Eigenvalue used: 1.0000000000 (index 0)
  Stationary distribution:
        VOID: 0.0123893805
     LATTICE: 0.1044247788
     COUNTER: 0.1026548673
    PROGRESS: 0.1044247788
    COLLAPSE: 0.1079646018
     BALANCE: 0.1115044248
       CHAOS: 0.1115044248
     HARMONY: 0.1238938053
      BREATH: 0.1132743363
       RESET: 0.1079646018

  HARMONY weight in stationary dist: 0.1238938053
  Target (73%):                      0.7300000000
  Difference:                        0.6061061947

--- Spectral Gap ---
  Largest |lambda|:  1.0000000000
  2nd largest:       0.3052126828
  Spectral gap:      0.6947873172
  Approx mixing time: 1.4393 steps

--- Eigenvalues of Normalized BHML ---
  lambda_0: +1.0000000000 +0.0000000000i  |lambda| = 1.0000000000
  lambda_1: -0.3086779767 +0.0000000000i  |lambda| = 0.3086779767
  lambda_2: +0.2782244646 +0.0000000000i  |lambda| = 0.2782244646
  lambda_3: +0.2124287702 +0.0000000000i  |lambda| = 0.2124287702
  lambda_4: +0.1919004304 +0.0000000000i  |lambda| = 0.1919004304
  lambda_5: -0.1337548757 +0.0000000000i  |lambda| = 0.1337548757
  lambda_6: -0.0960266125 +0.0000000000i  |lambda| = 0.0960266125
  lambda_7: +0.0838409378 +0.0000000000i  |lambda| = 0.0838409378
  lambda_8: +0.0292812636 +0.0000000000i  |lambda| = 0.0292812636
  lambda_9: -0.0045555169 +0.0000000000i  |lambda| = 0.0045555169

========================================================================
  ANALYSIS 2: Physical Constant Search
========================================================================

--- Matches within 1% tolerance ---
  (1-T*)^1 = 0.2857142857
    ~ 1 - T* = 0.2857142857
    relative error: 0.000000e+00 (0.0000%)

  27/73 = 0.3698630137
    ~ 1/e = 0.3678794412
    relative error: 5.391909e-03 (0.5392%)

  73/27 = 2.7037037037
    ~ e (Euler) = 2.7182818285
    relative error: 5.362992e-03 (0.5363%)

  T*^1 = 0.7142857143
    ~ T* = 5/7 = 0.7142857143
    relative error: 0.000000e+00 (0.0000%)

  T*^2 = 0.5102040816
    ~ T*^2 = 0.5102040816
    relative error: 0.000000e+00 (0.0000%)

  T*^3 = 0.3644314869
    ~ 1/e = 0.3678794412
    relative error: 9.372511e-03 (0.9373%)

  stat[BREATH]/stat[HARMONY] = 0.9142857143
    ~ Catalan constant = 0.9159655941
    relative error: 1.833999e-03 (0.1834%)

  stat[COUNTER]/stat[BALANCE] = 0.9206349206
    ~ Catalan constant = 0.9159655941
    relative error: 5.097710e-03 (0.5098%)

  stat[COUNTER]/stat[CHAOS] = 0.9206349206
    ~ Catalan constant = 0.9159655941
    relative error: 5.097710e-03 (0.5098%)

  stat[HARMONY]/stat[COUNTER] = 1.2068965517
    ~ Apery's constant zeta(3) = 1.2020569031
    relative error: 4.026139e-03 (0.4026%)

  stat[LATTICE]/stat[BREATH] = 0.9218750000
    ~ Catalan constant = 0.9159655941
    relative error: 6.451559e-03 (0.6452%)

  stat[PROGRESS]/stat[BREATH] = 0.9218750000
    ~ Catalan constant = 0.9159655941
    relative error: 6.451559e-03 (0.6452%)

  |lambda_1|/|lambda_3| = 3.1461059145
    ~ pi = 3.1415926536
    relative error: 1.436616e-03 (0.1437%)

  |lambda_4|/|lambda_5| = 1.6266144479
    ~ golden ratio phi = 1.6180339887
    relative error: 5.303015e-03 (0.5303%)


--- Matches within 2% tolerance ---
  (1-T*)^1 = 0.2857142857
    ~ 1 - T* = 0.2857142857
    relative error: 0.000000e+00 (0.0000%)

  27/73 = 0.3698630137
    ~ 1/e = 0.3678794412
    relative error: 5.391909e-03 (0.5392%)

  73/27 = 2.7037037037
    ~ e (Euler) = 2.7182818285
    relative error: 5.362992e-03 (0.5363%)

  T*^1 = 0.7142857143
    ~ 1/sqrt(2) = 0.7071067812
    relative error: 1.015254e-02 (1.0153%)

  T*^1 = 0.7142857143
    ~ T* = 5/7 = 0.7142857143
    relative error: 0.000000e+00 (0.0000%)

  T*^2 = 0.5102040816
    ~ T*^2 = 0.5102040816
    relative error: 0.000000e+00 (0.0000%)

  T*^3 = 0.3644314869
    ~ 1/e = 0.3678794412
    relative error: 9.372511e-03 (0.9373%)

  eigenvalue[2] = 0.2904422897
    ~ 1 - T* = 0.2857142857
    relative error: 1.654801e-02 (1.6548%)

  log2(73) = 6.1898245589
    ~ 2*pi = 6.2831853072
    relative error: 1.485882e-02 (1.4859%)

  stat[BALANCE]/stat[HARMONY] = 0.9000000000
    ~ Catalan constant = 0.9159655941
    relative error: 1.743034e-02 (1.7430%)

  stat[BREATH]/stat[HARMONY] = 0.9142857143
    ~ Catalan constant = 0.9159655941
    relative error: 1.833999e-03 (0.1834%)

  stat[CHAOS]/stat[HARMONY] = 0.9000000000
    ~ Catalan constant = 0.9159655941
    relative error: 1.743034e-02 (1.7430%)

  stat[COUNTER]/stat[BALANCE] = 0.9206349206
    ~ Catalan constant = 0.9159655941
    relative error: 5.097710e-03 (0.5098%)

  stat[COUNTER]/stat[BREATH] = 0.9062500000
    ~ Catalan constant = 0.9159655941
    relative error: 1.060694e-02 (1.0607%)

  stat[COUNTER]/stat[CHAOS] = 0.9206349206
    ~ Catalan constant = 0.9159655941
    relative error: 5.097710e-03 (0.5098%)

  stat[HARMONY]/stat[COUNTER] = 1.2068965517
    ~ Apery's constant zeta(3) = 1.2020569031
    relative error: 4.026139e-03 (0.4026%)

  stat[HARMONY]/stat[LATTICE] = 1.1864406780
    ~ Apery's constant zeta(3) = 1.2020569031
    relative error: 1.299125e-02 (1.2991%)

  stat[HARMONY]/stat[PROGRESS] = 1.1864406780
    ~ Apery's constant zeta(3) = 1.2020569031
    relative error: 1.299125e-02 (1.2991%)

  stat[LATTICE]/stat[BREATH] = 0.9218750000
    ~ Catalan constant = 0.9159655941
    relative error: 6.451559e-03 (0.6452%)

  stat[PROGRESS]/stat[BREATH] = 0.9218750000
    ~ Catalan constant = 0.9159655941
    relative error: 6.451559e-03 (0.6452%)

  |lambda_1|/|lambda_3| = 3.1461059145
    ~ pi = 3.1415926536
    relative error: 1.436616e-03 (0.1437%)

  |lambda_2|/|lambda_4| = 3.0856492662
    ~ pi = 3.1415926536
    relative error: 1.780733e-02 (1.7807%)

  |lambda_4|/|lambda_5| = 1.6266144479
    ~ golden ratio phi = 1.6180339887
    relative error: 5.303015e-03 (0.5303%)


--- Matches within 5% tolerance ---
  (1-T*)^1 = 0.2857142857
    ~ 1 - T* = 0.2857142857
    relative error: 0.000000e+00 (0.0000%)

  27/73 = 0.3698630137
    ~ 1/e = 0.3678794412
    relative error: 5.391909e-03 (0.5392%)

  73/100 = 0.7300000000
    ~ 1/sqrt(2) = 0.7071067812
    relative error: 3.237590e-02 (3.2376%)

  73/100 = 0.7300000000
    ~ T* = 5/7 = 0.7142857143
    relative error: 2.200000e-02 (2.2000%)

  73/27 = 2.7037037037
    ~ e (Euler) = 2.7182818285
    relative error: 5.362992e-03 (0.5363%)

  BHML_harmony/100 = 0.3100000000
    ~ 1/pi = 0.3183098862
    relative error: 2.610628e-02 (2.6106%)

  T*^1 = 0.7142857143
    ~ 1/sqrt(2) = 0.7071067812
    relative error: 1.015254e-02 (1.0153%)

  T*^1 = 0.7142857143
    ~ ln(2) = 0.6931471806
    relative error: 3.049646e-02 (3.0496%)

  T*^1 = 0.7142857143
    ~ T* = 5/7 = 0.7142857143
    relative error: 0.000000e+00 (0.0000%)

  T*^2 = 0.5102040816
    ~ T*^2 = 0.5102040816
    relative error: 0.000000e+00 (0.0000%)

  T*^3 = 0.3644314869
    ~ 1/e = 0.3678794412
    relative error: 9.372511e-03 (0.9373%)

  TSML_h / BHML_h = 2.3548387097
    ~ ln(10) = 2.3025850930
    relative error: 2.269346e-02 (2.2693%)

  eigenvalue[2] = 0.2904422897
    ~ 1 - T* = 0.2857142857
    relative error: 1.654801e-02 (1.6548%)

  log2(73) = 6.1898245589
    ~ 2*pi = 6.2831853072
    relative error: 1.485882e-02 (1.4859%)

  stat[BALANCE]/stat[HARMONY] = 0.9000000000
    ~ Catalan constant = 0.9159655941
    relative error: 1.743034e-02 (1.7430%)

  stat[BREATH]/stat[HARMONY] = 0.9142857143
    ~ Catalan constant = 0.9159655941
    relative error: 1.833999e-03 (0.1834%)

  stat[CHAOS]/stat[HARMONY] = 0.9000000000
    ~ Catalan constant = 0.9159655941
    relative error: 1.743034e-02 (1.7430%)

  stat[COLLAPSE]/stat[BREATH] = 0.9531250000
    ~ Catalan constant = 0.9159655941
    relative error: 4.056856e-02 (4.0569%)

  stat[COLLAPSE]/stat[HARMONY] = 0.8714285714
    ~ Catalan constant = 0.9159655941
    relative error: 4.862303e-02 (4.8623%)

  stat[COUNTER]/stat[BALANCE] = 0.9206349206
    ~ Catalan constant = 0.9159655941
    relative error: 5.097710e-03 (0.5098%)

  stat[COUNTER]/stat[BREATH] = 0.9062500000
    ~ Catalan constant = 0.9159655941
    relative error: 1.060694e-02 (1.0607%)

  stat[COUNTER]/stat[CHAOS] = 0.9206349206
    ~ Catalan constant = 0.9159655941
    relative error: 5.097710e-03 (0.5098%)

  stat[COUNTER]/stat[COLLAPSE] = 0.9508196721
    ~ Catalan constant = 0.9159655941
    relative error: 3.805173e-02 (3.8052%)

  stat[COUNTER]/stat[RESET] = 0.9508196721
    ~ Catalan constant = 0.9159655941
    relative error: 3.805173e-02 (3.8052%)

  stat[HARMONY]/stat[COLLAPSE] = 1.1475409836
    ~ Apery's constant zeta(3) = 1.2020569031
    relative error: 4.535220e-02 (4.5352%)

  stat[HARMONY]/stat[COUNTER] = 1.2068965517
    ~ Apery's constant zeta(3) = 1.2020569031
    relative error: 4.026139e-03 (0.4026%)

  stat[HARMONY]/stat[LATTICE] = 1.1864406780
    ~ Apery's constant zeta(3) = 1.2020569031
    relative error: 1.299125e-02 (1.2991%)

  stat[HARMONY]/stat[PROGRESS] = 1.1864406780
    ~ Apery's constant zeta(3) = 1.2020569031
    relative error: 1.299125e-02 (1.2991%)

  stat[HARMONY]/stat[RESET] = 1.1475409836
    ~ Apery's constant zeta(3) = 1.2020569031
    relative error: 4.535220e-02 (4.5352%)

  stat[LATTICE]/stat[BALANCE] = 0.9365079365
    ~ Catalan constant = 0.9159655941
    relative error: 2.242698e-02 (2.2427%)

  stat[LATTICE]/stat[BREATH] = 0.9218750000
    ~ Catalan constant = 0.9159655941
    relative error: 6.451559e-03 (0.6452%)

  stat[LATTICE]/stat[CHAOS] = 0.9365079365
    ~ Catalan constant = 0.9159655941
    relative error: 2.242698e-02 (2.2427%)

  stat[PROGRESS]/stat[BALANCE] = 0.9365079365
    ~ Catalan constant = 0.9159655941
    relative error: 2.242698e-02 (2.2427%)

  stat[PROGRESS]/stat[BREATH] = 0.9218750000
    ~ Catalan constant = 0.9159655941
    relative error: 6.451559e-03 (0.6452%)

  stat[PROGRESS]/stat[CHAOS] = 0.9365079365
    ~ Catalan constant = 0.9159655941
    relative error: 2.242698e-02 (2.2427%)

  stat[RESET]/stat[BREATH] = 0.9531250000
    ~ Catalan constant = 0.9159655941
    relative error: 4.056856e-02 (4.0569%)

  stat[RESET]/stat[HARMONY] = 0.8714285714
    ~ Catalan constant = 0.9159655941
    relative error: 4.862303e-02 (4.8623%)

  |lambda_0|/|lambda_1| = 3.2764038202
    ~ pi = 3.1415926536
    relative error: 4.291173e-02 (4.2912%)

  |lambda_1|/|lambda_3| = 3.1461059145
    ~ pi = 3.1415926536
    relative error: 1.436616e-03 (0.1437%)

  |lambda_1|/|lambda_4| = 3.2425694339
    ~ pi = 3.1415926536
    relative error: 3.214191e-02 (3.2142%)

  |lambda_2|/|lambda_3| = 2.9938539804
    ~ pi = 3.1415926536
    relative error: 4.702668e-02 (4.7027%)

  |lambda_2|/|lambda_4| = 3.0856492662
    ~ pi = 3.1415926536
    relative error: 1.780733e-02 (1.7807%)

  |lambda_3|/|lambda_5| = 1.6764884695
    ~ golden ratio phi = 1.6180339887
    relative error: 3.612686e-02 (3.6127%)

  |lambda_3|/|lambda_5| = 1.6764884695
    ~ sqrt(3) = 1.7320508076
    relative error: 3.207893e-02 (3.2079%)

  |lambda_4|/|lambda_5| = 1.6266144479
    ~ golden ratio phi = 1.6180339887
    relative error: 5.303015e-03 (0.5303%)

  |lambda_5|/|lambda_6| = 2.1505510109
    ~ sqrt(5) = 2.2360679775
    relative error: 3.824435e-02 (3.8244%)

  |lambda_5|/|lambda_7| = 5.9698282375
    ~ 2*pi = 6.2831853072
    relative error: 4.987233e-02 (4.9872%)

  |lambda_5|/|lambda_8| = 5.9751972666
    ~ 2*pi = 6.2831853072
    relative error: 4.901782e-02 (4.9018%)

  |lambda_6|/|lambda_7| = 2.7759528639
    ~ e (Euler) = 2.7182818285
    relative error: 2.121599e-02 (2.1216%)

  |lambda_6|/|lambda_8| = 2.7784494468
    ~ e (Euler) = 2.7182818285
    relative error: 2.213443e-02 (2.2134%)


--- T* vs 73% Direct Comparison ---
  T* = 5/7         = 0.714285714285714
  73/100           = 0.730000000000000
  Difference:        0.015714285714286
  Relative diff:     2.200000%
  73/100 / T* =      1.022000000000000
  T* / (73/100) =    0.978473581213307

  Nearest integer to T* * 100: 71
  Actual HARMONY count:        73
  Floor(T* * 100):             71
  Ceil(T* * 100):              72

========================================================================
  ANALYSIS 3: Expanded Monte Carlo (CL Table Uniqueness)
========================================================================

--- Strict Constraints (100,000 random tables) ---
  Constraints:
    - Values 0-9 only
    - Row 0 (VOID): all zeros except one random position = 7
    - Row 7 (HARMONY): all entries = 7 (absorbing)
    - Column 0: all zeros except row 7 = 7
    - Remaining 72 free cells: random 0-9
  Elapsed: 19.0s

  HARMONY count distribution (strict):
    Mean:   18.10
    Std:    2.57
    Min:    10
    Max:    32
    Median: 18

  Actual TSML HARMONY count: 73
  Tables with >= 73 HARMONY: 0 / 100,000 (0.0000%)
  Tables with == 73 HARMONY: 0 / 100,000
  Percentile of 73: 100.0000%
  Z-score of 73:    21.3308 standard deviations above mean

--- Histogram of HARMONY counts (strict constraints) ---
     10:  (8)
     11:  (70)
     12: # (518)
     13: ###### (1,916)
     14: ############### (4,632)
     15: ########################## (8,302)
     16: ######################################## (12,453)
     17: ################################################ (14,931)
     18: ################################################## (15,398)
     19: ############################################ (13,678)
     20: ################################### (10,844)
     21: ######################## (7,484)
     22: ############## (4,610)
     23: ######## (2,694)
     24: #### (1,372)
     25: ## (643)
     26:  (278)
     27:  (115)
     28:  (39)
     29:  (12)
     30:  (2)
     32:  (1)

--- Relaxed Constraints (100,000 random tables) ---
  Constraints:
    - Values 0-9 only
    - One designated absorbing row: all entries = 7
    - Column 0: all zeros except absorbing row = 7
    - All other 81 cells: random 0-9
  Elapsed: 1.5s

  HARMONY count distribution (relaxed):
    Mean:   18.10
    Std:    2.70
    Min:    10
    Max:    33

  Tables with >= 73 HARMONY: 0 / 100,000 (0.0000%)
  Percentile of 73: 100.0000%
  Z-score of 73:    20.3022 standard deviations above mean

========================================================================
  ANALYSIS 4: CL Semigroup Properties
========================================================================

--- Associativity: CL[CL[a][b]][c] == CL[a][CL[b][c]]? ---
  Total triples:      1000
  Associative:        872 (87.20%)
  Non-associative:    128 (12.80%)

  First 10 failures:
    (VOID * LATTICE) * LATTICE = VOID  but  VOID * (LATTICE * LATTICE) = HARMONY
    (VOID * LATTICE) * PROGRESS = VOID  but  VOID * (LATTICE * PROGRESS) = HARMONY
    (VOID * LATTICE) * COLLAPSE = VOID  but  VOID * (LATTICE * COLLAPSE) = HARMONY
    (VOID * LATTICE) * BALANCE = VOID  but  VOID * (LATTICE * BALANCE) = HARMONY
    (VOID * LATTICE) * CHAOS = VOID  but  VOID * (LATTICE * CHAOS) = HARMONY
    (VOID * LATTICE) * BREATH = VOID  but  VOID * (LATTICE * BREATH) = HARMONY
    (VOID * LATTICE) * RESET = VOID  but  VOID * (LATTICE * RESET) = HARMONY
    (VOID * COUNTER) * COUNTER = VOID  but  VOID * (COUNTER * COUNTER) = HARMONY
    (VOID * COUNTER) * PROGRESS = VOID  but  VOID * (COUNTER * PROGRESS) = HARMONY
    (VOID * COUNTER) * BALANCE = VOID  but  VOID * (COUNTER * BALANCE) = HARMONY

--- Associativity in BHML ---
  Associative triples: 746 / 1000 (74.60%)

--- Bump Pairs (non-HARMONY results in TSML) ---
  Total bump pairs: 27 (out of 100)
  These are the 'non-trivial' compositions:
        VOID * VOID     = VOID (0)
        VOID * LATTICE  = VOID (0)
        VOID * COUNTER  = VOID (0)
        VOID * PROGRESS = VOID (0)
        VOID * COLLAPSE = VOID (0)
        VOID * BALANCE  = VOID (0)
        VOID * CHAOS    = VOID (0)
        VOID * BREATH   = VOID (0)
        VOID * RESET    = VOID (0)
     LATTICE * VOID     = VOID (0)
     LATTICE * COUNTER  = PROGRESS (3)
     COUNTER * VOID     = VOID (0)
     COUNTER * LATTICE  = PROGRESS (3)
     COUNTER * COLLAPSE = COLLAPSE (4)
     COUNTER * RESET    = RESET (9)
    PROGRESS * VOID     = VOID (0)
    PROGRESS * RESET    = PROGRESS (3)
    COLLAPSE * VOID     = VOID (0)
    COLLAPSE * COUNTER  = COLLAPSE (4)
    COLLAPSE * BREATH   = BREATH (8)
     BALANCE * VOID     = VOID (0)
       CHAOS * VOID     = VOID (0)
      BREATH * VOID     = VOID (0)
      BREATH * COLLAPSE = BREATH (8)
       RESET * VOID     = VOID (0)
       RESET * COUNTER  = RESET (9)
       RESET * PROGRESS = PROGRESS (3)

--- Idempotent Operators: CL[a][a] = a ---
  VOID (0) is idempotent
  LATTICE (1): CL[1][1] = 7 (HARMONY)
  COUNTER (2): CL[2][2] = 7 (HARMONY)
  PROGRESS (3): CL[3][3] = 7 (HARMONY)
  COLLAPSE (4): CL[4][4] = 7 (HARMONY)
  BALANCE (5): CL[5][5] = 7 (HARMONY)
  CHAOS (6): CL[6][6] = 7 (HARMONY)
  HARMONY (7) is idempotent
  BREATH (8): CL[8][8] = 7 (HARMONY)
  RESET (9): CL[9][9] = 7 (HARMONY)

--- Nilpotent Operators (self-compose until VOID or cycle) ---
  VOID: reaches VOID in 1 steps: VOID -> VOID
  LATTICE: cycles at step 2 (period 1): LATTICE -> HARMONY -> HARMONY
  COUNTER: cycles at step 2 (period 1): COUNTER -> HARMONY -> HARMONY
  PROGRESS: cycles at step 2 (period 1): PROGRESS -> HARMONY -> HARMONY
  COLLAPSE: cycles at step 2 (period 1): COLLAPSE -> HARMONY -> HARMONY
  BALANCE: cycles at step 2 (period 1): BALANCE -> HARMONY -> HARMONY
  CHAOS: cycles at step 2 (period 1): CHAOS -> HARMONY -> HARMONY
  HARMONY: cycles at step 1 (period 1): HARMONY -> HARMONY
  BREATH: cycles at step 2 (period 1): BREATH -> HARMONY -> HARMONY
  RESET: cycles at step 2 (period 1): RESET -> HARMONY -> HARMONY

--- Operator Periods (repeated a*a*a*...) ---
  VOID: period = 1
  LATTICE: absorbs to cycle starting at step 1, period 1: HARMONY
  COUNTER: absorbs to cycle starting at step 1, period 1: HARMONY
  PROGRESS: absorbs to cycle starting at step 1, period 1: HARMONY
  COLLAPSE: absorbs to cycle starting at step 1, period 1: HARMONY
  BALANCE: absorbs to cycle starting at step 1, period 1: HARMONY
  CHAOS: absorbs to cycle starting at step 1, period 1: HARMONY
  HARMONY: period = 1
  BREATH: absorbs to cycle starting at step 1, period 1: HARMONY
  RESET: absorbs to cycle starting at step 1, period 1: HARMONY

--- Absorbing / Left-Zero / Right-Zero Elements ---
  HARMONY: ABSORBING (left-zero AND right-zero)

--- Commutativity: CL[a][b] == CL[b][a]? ---
  Commutative pairs: 45 / 45 (100.00%)
  Non-commutative:   0

========================================================================
  ANALYSIS 5: Conservation Laws / Invariants
========================================================================

--- Canonical 5D Force Vectors ---
      VOID: [ 0.  0.  0.  0. -1.]
   LATTICE: [1. 0. 0. 0. 0.]
   COUNTER: [0. 1. 0. 0. 0.]
  PROGRESS: [0. 0. 1. 0. 0.]
  COLLAPSE: [-1.  0.  0.  0.  0.]
   BALANCE: [ 0. -1.  0.  0.  0.]
     CHAOS: [ 0.  0. -1.  0.  0.]
   HARMONY: [0. 0. 0. 0. 1.]
    BREATH: [0. 0. 0. 1. 0.]
     RESET: [ 0.  0.  0. -1.  0.]

--- Linear Invariant Search ---
  Testing: does there exist w such that w . F(CL[a][b]) = w . F(a) + w . F(b)?
  (A linear conserved 'charge' under CL composition)
  Singular values of constraint matrix: [7.751688 6.595106 6.331311 5.966761 5.720853]
  Number of near-zero singular values: 0
  No exact linear invariant exists.
  Smallest singular value: 5.720853 (approximate invariant)
  Approximate invariant direction: [-0.231359 -0.403368 -0.429326  0.755076  0.17119 ]

--- Multiplicative Invariant Search ---
  Testing: does there exist a mapping Q: operators -> R such that
  Q(CL[a][b]) = Q(a) * Q(b)  (semigroup homomorphism to (R, *))?
  HARMONY is absorbing => Q(HARMONY) must be 0 or all Q(x)=1
  Non-trivial homomorphism requires Q(HARMONY) = 0

--- Random CL Walk Variance Analysis ---
  Running 10,000 random CL composition chains of length 50
  Tracking 5D 'current' (running sum of force vectors)

  Final current statistics (after 50 steps):
     Dimension        Mean         Std         Var
      aperture     -0.0127      0.4923      0.2423
      pressure      0.0045      0.4433      0.1965
         depth      0.0544      0.5303      0.2812
       binding     -0.0038      0.5630      0.3170
    continuity     46.1352     11.5420    133.2181

  HARMONY fraction in walks:
    Mean: 0.943333
    Std:  0.112303
    Expected from stationary: ~0.714286

  Continuity dimension growth (HARMONY=+1, VOID=-1):
    Variance at step 5:  24.4372
    Variance at step 50: 2261.6748
    Ratio: 92.5505

--- Dimension-Pair Correlation in Final Currents ---
  Correlation matrix of final 5D currents:
                  aperture    pressure       depth     binding  continuity
      aperture    1.000000   -0.045566    0.051676   -0.051047   -0.002778
      pressure   -0.045566    1.000000    0.049582   -0.040402   -0.030103
         depth    0.051676    0.049582    1.000000   -0.050216   -0.008406
       binding   -0.051047   -0.040402   -0.050216    1.000000    0.011436
    continuity   -0.002778   -0.030103   -0.008406    0.011436    1.000000

========================================================================
  ANALYSIS 6: T* and 73% Relationships
========================================================================

--- Numerical Relationships ---
  T*     = 5/7    = 0.714285714285714
  73/100          = 0.730000000000000
  Difference:       -0.015714285714286
  Ratio 73/100 / T*: 1.022000000000000

  73/100 = 73/100 (already in lowest terms, gcd(73,100) = 1)
  5/7    = 5/7    (already in lowest terms)
  73*7   = 511
  100*5  = 500
  Difference 73*7 - 100*5 = 11
  So: 73/100 - 5/7 = (73*7 - 100*5) / 700 = 11/700 = 0.015714285714286

--- The 27% (Non-HARMONY) ---
  Non-HARMONY entries: 27
  27/100 = 0.27
  1 - T* = 2/7 = 0.285714285714286 = 0.285714285714286
  27/100 vs 2/7: difference = -0.015714285714286
  27 = 3^3 (a perfect cube)
  73 = prime
  73 + 27 = 100 = 10^2 = (5*2)^2
  73 - 27 = 46
  73 * 27 = 1971
  73 / 27 = 2.703703703703704
  27 / 73 = 0.369863013698630

  27/73 = 0.3698630137
  1/e   = 0.3678794412  (diff: 0.0019835725)
  1/phi = 0.6180339887  (diff: 0.2481709751)

--- Rational Approximations of 73/100 with Small Denominators ---
       p/q         Value         Error
  5/  7    0.7142857143  0.0157142857
  8/ 11    0.7272727273  0.0027272727
  10/ 14    0.7142857143  0.0157142857
  11/ 15    0.7333333333  0.0033333333
  13/ 18    0.7222222222  0.0077777778
  14/ 19    0.7368421053  0.0068421053
  15/ 21    0.7142857143  0.0157142857
  16/ 22    0.7272727273  0.0027272727
  17/ 23    0.7391304348  0.0091304348
  18/ 25    0.7200000000  0.0100000000
  19/ 26    0.7307692308  0.0007692308
  20/ 27    0.7407407407  0.0107407407
  20/ 28    0.7142857143  0.0157142857
  21/ 29    0.7241379310  0.0058620690
  22/ 30    0.7333333333  0.0033333333
  23/ 31    0.7419354839  0.0119354839
  23/ 32    0.7187500000  0.0112500000
  24/ 33    0.7272727273  0.0027272727
  25/ 34    0.7352941176  0.0052941176
  26/ 35    0.7428571429  0.0128571429
  26/ 36    0.7222222222  0.0077777778
  27/ 37    0.7297297297  0.0002702703
  28/ 38    0.7368421053  0.0068421053
  28/ 39    0.7179487179  0.0120512821
  29/ 40    0.7250000000  0.0050000000
  30/ 41    0.7317073171  0.0017073171
  31/ 42    0.7380952381  0.0080952381
  31/ 43    0.7209302326  0.0090697674
  32/ 44    0.7272727273  0.0027272727
  33/ 45    0.7333333333  0.0033333333
  34/ 46    0.7391304348  0.0091304348
  34/ 47    0.7234042553  0.0065957447
  35/ 48    0.7291666667  0.0008333333
  36/ 49    0.7346938776  0.0046938776
  36/ 50    0.7200000000  0.0100000000

--- Continued Fraction Expansion of 73/100 ---
  73/100 = [0; 1; 2; 1; 2; 2; 1; 2]
  5/7    = [0; 1; 2; 2]

--- Number-Theoretic Properties of 73 ---
  73 is prime: True
  73 is the 21st prime
  73 in binary: 0b1001001 = 1001001 (palindrome!)
  73 in octal: 0o111
  73 in hex: 0x49
  7 * 3 = 21, and 73 is the 21st prime
  Mirror: 37 is the 12th prime (mirror of 21)
  73 is a star number: 73 = 6*3*4/2 + 1? Actually: star numbers = 6k(k-1)+1
    Yes! 73 is the 4th star number (6*4*3+1 = 73)
  73 = 64 + 8 + 1 = 2^6 + 2^3 + 2^0
  Sum of digits: 7 + 3 = 10
  Product of digits: 7 * 3 = 21

  Sheldon Cooper properties:
    73 reversed = 37
    37 is the 12th prime
    12 reversed = 21
    73 is the 21st prime
    73 in binary: 1001001 (palindrome)
    This makes 73 the 'unique' Sheldon prime

--- Information Entropy of TSML Table ---
  Value probabilities:
    0 (    VOID): 0.1700  (-p*log2(p) = 0.434587)
    3 (PROGRESS): 0.0400  (-p*log2(p) = 0.185754)
    4 (COLLAPSE): 0.0200  (-p*log2(p) = 0.112877)
    7 ( HARMONY): 0.7300  (-p*log2(p) = 0.331443)
    8 (  BREATH): 0.0200  (-p*log2(p) = 0.112877)
    9 (   RESET): 0.0200  (-p*log2(p) = 0.112877)

  Shannon entropy H(TSML):  1.2904155788 bits
  Maximum entropy (uniform): 3.3219280949 bits
  Efficiency H/H_max:        0.3884537961
  Redundancy 1 - H/H_max:    0.6115462039

  Entropy relationships:
    H(TSML) = 1.2904155788
    T*      = 0.7142857143
    H / T*  = 1.8065818103
    T* / H  = 0.5535315336

  Binary entropy H_b(0.73):  0.8414646362 bits
  Binary entropy H_b(T*):    0.8631205686 bits

--- Information Entropy of BHML Table ---
  Shannon entropy H(BHML):  2.8654758424 bits
  Efficiency H/H_max:       0.8625941804
  TSML vs BHML entropy ratio: 0.4503320390

--- CL Table as Number ---
  Sum of all 100 entries: 565
  Mean entry value:       5.65
  If all were HARMONY:    700
  'Missing' HARMONY sum:  135

  Non-HARMONY entries:
    Count: 27
    Sum:   54
    Mean:  2.0000

--- Powers of T* = 5/7 ---
  T*^ 1 = 0.714285714285714
  T*^ 2 = 0.510204081632653
  T*^ 3 = 0.364431486880467
  T*^ 4 = 0.260308204914619
  T*^ 5 = 0.185934432081871
  T*^ 6 = 0.132810308629908
  T*^ 7 = 0.094864506164220
  T*^ 8 = 0.067760361545871
  T*^ 9 = 0.048400258247051
  T*^10 = 0.034571613033608
  T*^11 = 0.024694009309720
  T*^12 = 0.017638578078371
  T*^13 = 0.012598984341694
  T*^14 = 0.008999274529781

--- Powers of (1 - T*) = 2/7 ---
  (2/7)^ 1 = 0.285714285714286
  (2/7)^ 2 = 0.081632653061224
  (2/7)^ 3 = 0.023323615160350
  (2/7)^ 4 = 0.006663890045814
  (2/7)^ 5 = 0.001903968584518
  (2/7)^ 6 = 0.000543991024148
  (2/7)^ 7 = 0.000155426006899
  (2/7)^ 8 = 0.000044407430543
  (2/7)^ 9 = 0.000012687837298
  (2/7)^10 = 0.000003625096371
  (2/7)^11 = 0.000001035741820
  (2/7)^12 = 0.000000295926234
  (2/7)^13 = 0.000000084550353
  (2/7)^14 = 0.000000024157244

========================================================================
  FINAL SUMMARY
========================================================================
  1. TSML has 73 HARMONY entries (73%), T* = 0.7142857143 (71.43%)
     73/100 overshoots T* by 1.5714 percentage points
     73/100 - 5/7 = 11/700 = 0.0157142857

  2. Monte Carlo: 73 HARMONY entries is 21.3 sigma above random expectation
     Under strict constraints, mean=18.1, std=2.6

  3. Semigroup: 872/1000 triples associative (87.2%)
     HARMONY is absorbing (left-zero and right-zero)

  4. 73 is prime, the 21st prime, binary palindrome 1001001
     73 reversed = 37 (12th prime), 12 reversed = 21

  5. The CL table is a composition algebra, not a transition matrix.
     The HARMONY attractor ensures all sufficiently long compositions
     converge to HARMONY -- this is coherence by construction.
```
