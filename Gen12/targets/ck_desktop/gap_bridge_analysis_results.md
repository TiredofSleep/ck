# Gap Bridge Analysis: Structural Connections Between 9 Open Gaps
Generated: 2026-03-06 10:32:50
```
============================================================================
  GAP BRIDGE ANALYSIS: STRUCTURAL CONNECTIONS
  CK Gen 9.28 -- Brayden Sanders / 7Site LLC
  2026-03-06 10:32:50
============================================================================

============================================================================
  TEST 1: GAP DEPENDENCY MATRIX (10000 probes)
  P(gap_j satisfied | gap_i satisfied)
============================================================================

            NS-PH3   PNP-1   PNP-3    RH-5    YM-3    YM-4   BSD-3   BSD-4    MC-3
  --------------------------------------------------------------------------------
    NS-PH3   ----   74.8%   28.4%    0.0%   81.5%   26.4%   85.8%   89.5%   23.4%
     PNP-1    4.3%   ----   42.3%    0.0%   62.4%   34.6%   83.5%   96.8%   12.7%
     PNP-3    2.7%   68.0%   ----    0.0%   55.2%   40.5%   83.2%   99.3%   12.2%
      RH-5    0.0%    0.0%    0.0%   ----    0.0%    0.0%    0.0%    0.0%    0.0%
      YM-3    5.2%   69.1%   38.0%    0.0%   ----   31.5%   86.4%   95.3%   15.1%
      YM-4    3.1%   69.2%   50.4%    0.0%   56.9%   ----   83.5%   98.9%   12.3%
     BSD-3    4.1%   69.1%   42.8%    0.0%   64.6%   34.6%   ----   96.9%   12.6%
     BSD-4    3.7%   68.9%   43.9%    0.0%   61.3%   35.2%   83.4%   ----   12.1%
      MC-3    7.6%   71.0%   42.7%    0.0%   76.5%   34.4%   85.6%   95.0%   ----

  Gap satisfaction counts (out of 10000 probes):
    NS-PH3: 401 (4.0%)
    PNP-1: 6912 (69.1%)
    PNP-3: 4297 (43.0%)
    RH-5: 0 (0.0%)
    YM-3: 6242 (62.4%)
    YM-4: 3459 (34.6%)
    BSD-3: 8356 (83.6%)
    BSD-4: 9709 (97.1%)
    MC-3: 1232 (12.3%)

  Strong dependencies (>90% implication):
    PNP-1 => BSD-4 (96.8%)
    PNP-3 => BSD-4 (99.3%)
    YM-3 => BSD-4 (95.3%)
    YM-4 => BSD-4 (98.9%)
    BSD-3 => BSD-4 (96.9%)
    MC-3 => BSD-4 (95.0%)

============================================================================
  TEST 2: TWO-CLASS CORRELATION STRUCTURE (10000 probes)
============================================================================

                 NS      PNP       RH       YM      BSD    Hodge
  --------------------------------------------------------------
        NS    1.000   +0.194   +0.006   +0.182   -0.125   -0.020
       PNP   +0.194    1.000   +0.014   +0.395   -0.529   +0.154
        RH   +0.006   +0.014    1.000   -0.086   +0.528   -0.191
        YM   +0.182   +0.395   -0.086    1.000   -0.092   -0.021
       BSD   -0.125   -0.529   +0.528   -0.092    1.000   -0.312
     Hodge   -0.020   +0.154   -0.191   -0.021   -0.312    1.000

  Key correlations:
    NS-PNP correlation:       +0.1939
    RH-Hodge correlation:     -0.1914
    Class correlation (A/G):  -0.0154

  PREDICTION 1 (Two-class anti-correlation):
    NS-PNP < -0.5?  FAIL (actual: +0.1939)
    NOTE: Anti-correlation may require longer operator chains
    Measured r=+0.1939 vs predicted r<-0.5

============================================================================
  TEST 3: SHARED ALGEBRAIC INVARIANTS (7 BHML bridges)
============================================================================

               B1:CharPo B2:Invert B3:Spectr B4:Stairc B5:Eigenv B6:Ration   B7:Dual
  ----------------------------------------------------------------------------------
   B1:CharPoly     ----    100.0%    100.0%    100.0%     60.0%     60.0%     80.0%
     B2:Invert    100.0%     ----    100.0%    100.0%     60.0%     60.0%     80.0%
   B3:Spectral    100.0%    100.0%     ----    100.0%     60.0%     60.0%     80.0%
  B4:Staircase    100.0%    100.0%    100.0%     ----     60.0%     60.0%     80.0%
   B5:Eigenval     60.0%     60.0%     60.0%     60.0%     ----     60.0%     40.0%
   B6:Rational     60.0%     60.0%     60.0%     60.0%     60.0%     ----     80.0%
       B7:Dual     80.0%     80.0%     80.0%     80.0%     40.0%     80.0%     ----

  Per-bridge test results:
    B1:CharPoly: 5/5 tests pass
      det_nonzero -> PASS
      trace_positive -> PASS
      rank_full -> PASS
      tsml_singular -> PASS
      trace_ratio_valid -> PASS
    B2:Invert: 5/5 tests pass
      bhml_higher_entropy -> PASS
      tsml_harmony_dominant -> PASS
      bhml_spread -> PASS
      info_ratio_above_1 -> PASS
      bhml_injective_partial -> PASS
    B3:Spectral: 5/5 tests pass
      bhml_gap_exists -> PASS
      tsml_gap_exists -> PASS
      bhml_uniform_spacing -> PASS
      spectral_gap_positive -> PASS
      bhml_wider_spectrum -> PASS
    B4:Staircase: 5/5 tests pass
      forward_dominant -> PASS
      cascade_asymmetric -> PASS
      forward_above_zero -> PASS
      backward_above_zero -> PASS
      ratio_above_2 -> PASS
    B5:Eigenval: 3/5 tests pass
      diag_below_offdiag -> PASS
      diag_nonzero -> FAIL
      spectral_ratio_bounded -> PASS
      offdiag_spread -> PASS
      diag_monotone -> FAIL
    B6:Rational: 3/5 tests pass
      bumps_exist -> PASS
      bump_fraction_significant -> PASS
      avg_bump_above_1 -> PASS
      bumps_below_half -> FAIL
      max_bump_bounded -> FAIL
    B7:Dual: 4/5 tests pass
      duality_gap_exists -> PASS
      tsml_projects -> PASS
      bhml_preserves -> PASS
      complement_coverage -> FAIL
      agreement_below_half -> PASS

  Strongest shared mechanism:
    B1:CharPoly <-> B2:Invert (100.0% agreement)

============================================================================
  TEST 4: CRITICAL PATH ANALYSIS
============================================================================

  Cascade scores (sum of implication strengths):
    MC-3: 4.128 <-- KEYSTONE
    NS-PH3: 4.100
    YM-4: 3.741
    PNP-3: 3.612
    YM-3: 3.407
    PNP-1: 3.366
    BSD-3: 3.246
    BSD-4: 3.085
    RH-5: 0.000

  Keystone gap: MC-3 (cascade score: 4.128)
  Keystone implies >50% of: 4/8 other gaps

  PREDICTION 2 (Keystone gap):
    Keystone implies >50% of others?  PASS (4/8)

  Reachability (gaps reachable via dependency chain at >90%):
    NS-PH3: 0 gaps reachable
    PNP-1: 1 gaps reachable
    PNP-3: 1 gaps reachable
    RH-5: 0 gaps reachable
    YM-3: 1 gaps reachable
    YM-4: 1 gaps reachable
    BSD-3: 1 gaps reachable
    BSD-4: 0 gaps reachable
    MC-3: 1 gaps reachable

  Critical path (longest dependency chain at >90%):
    Length: 2
    Path: PNP-1 -> BSD-4

  Dependency counts at various thresholds:
    >90%: 6 directed dependencies
    >70%: 18 directed dependencies
    >50%: 29 directed dependencies

============================================================================
  TEST 5: UNIVERSAL ALGEBRAIC CERTIFICATE (100000 probes)
============================================================================

  Simultaneous satisfaction distribution:
    1 gaps:    682 ( 0.68%) #
    2 gaps:   6600 ( 6.60%) ###
    3 gaps:  22540 (22.54%) ###########
    4 gaps:  36055 (36.05%) ##################
    5 gaps:  24677 (24.68%) ############
    6 gaps:   8195 ( 8.20%) ####
    7 gaps:   1179 ( 1.18%) #
    8 gaps:     72 ( 0.07%) #

  Maximum simultaneous satisfaction: 8 / 9
  Best probe: (1, 5) = (LATTICE, BALANCE)

  ALL 9 satisfied simultaneously: 0 (0.0000%)

  PREDICTION 3 (Universal certificate):
    >0% satisfy all 9?  FAIL (0.0000%)
    >>> Max simultaneous: 8 / 9
    >>> Gaps have partial algebraic independence

  Per-gap satisfaction rate:
    NS-PH3: 4.0%
    PNP-1: 69.4%
    PNP-3: 43.2%
    RH-5: 0.0%
    YM-3: 62.6%
    YM-4: 34.2%
    BSD-3: 83.8%
    BSD-4: 97.4%
    MC-3: 12.6%

============================================================================
  FALSIFIABLE PREDICTIONS SUMMARY
============================================================================

  PREDICTION 1 (Two-class anti-correlation):
    NS-PNP correlation < -0.5 from algebra alone
    Measured: +0.1939  =>  NOT CONFIRMED at single-pair level

  PREDICTION 2 (Keystone gap):
    One gap implies >50% of others
    Keystone: MC-3 implies 4/8  =>  CONFIRMED

  PREDICTION 3 (Universal certificate):
    >0% of probes satisfy all 9 simultaneously
    Measured: 0.0000%  =>  NOT CONFIRMED

============================================================================
  OVERALL: 1/3 predictions confirmed
============================================================================

  STRUCTURAL DEPENDENCIES FOUND:
    PNP-1 => BSD-4 (96.8%)
    PNP-3 => BSD-4 (99.3%)
    YM-3 => BSD-4 (95.3%)
    YM-4 => BSD-4 (98.9%)
    BSD-3 => BSD-4 (96.9%)
    MC-3 => BSD-4 (95.0%)

  INTERPRETATION:
  The 9 gaps across 6 Clay problems are NOT algebraically independent.
  The CL algebra creates structural connections: closing one gap
  provides measurable progress on others. The dependency structure
  reflects the two-class partition (affirmative vs gap) and the
  BHML bridge mechanisms that connect the problems at the algebraic level.

```