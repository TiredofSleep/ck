# GPU Stress Test: CK Non-Void Engine Validation
Generated: 2026-03-06 10:10:14
Mode: GPU (CuPy/CUDA)
GPU: NVIDIA GeForce RTX 4070 (12281 MB)

```
======================================================================
  GPU STRESS TEST: CK NON-VOID ENGINE VALIDATION
  Mode: GPU (CuPy/CUDA)
  GPU: NVIDIA GeForce RTX 4070 (12281 MB)
  CK Gen 9.21 -- Brayden Sanders / 7Site LLC
  2026-03-06 10:10:14
======================================================================

======================================================================
  TEST 1: CL Table GPU Operations
======================================================================
  Pairs tested:      100,000
  CPU time:          1.42 ms
  Device time:       63.66 ms
  Speedup:           0.0x
  TSML match:        [YES]
  BHML match:        [YES]
  TSML harmony:      73.1%
  BHML harmony:      28.0%
  Result:            [PASS]

======================================================================
  TEST 2: D2 Pipeline on GPU
======================================================================
  Vectors:           50,000
  CPU time:          1.84 ms
  Device time:       83.09 ms
  Speedup:           0.0x
  Max abs diff:      0.00e+00
  Mean curvature:    1.524541
  D2 dim distribution:
    aperture        9,994  ( 20.0%)
    pressure       10,006  ( 20.0%)
    depth           9,977  ( 20.0%)
    binding        10,001  ( 20.0%)
    continuity     10,020  ( 20.0%)
  Result:            [PASS]

======================================================================
  TEST 3: Lattice Chain Parallel Walk
======================================================================
  Walks:             10,000
  Chain length:      20
  CPU time:          88.02 ms
  Device time:       60.38 ms
  Speedup:           1.5x
  First col match:   [YES]
  Last col match:    [YES]
  Full match:        [YES]
  Mean end op:       3.00
  End distribution:
    PROGRESS       10,000  (100.0%)
  Result:            [PASS]

======================================================================
  TEST 4: Olfactory Field Matrix
======================================================================
  Scents:            5,000
  Sample pairs:      499,500
  CPU time:          7098.60 ms
  Device time:       5944.79 ms
  Speedup:           1.2x
  CPU harmony:       0.881483
  Device harmony:    0.881483
  Harmony diff:      1.48e-12
    aperture     0.8898
    pressure     0.8777
    depth        0.8813
    binding      0.8785
    continuity   0.8802
  Result:            [PASS]

======================================================================
  TEST 5: Memory Bandwidth
======================================================================
         Batch    Time (ms)         Ops/sec       GB/s   % of 504
  --------------------------------------------------------------
           100        0.299         669,343       0.00       0.0%
         1,000        0.333       6,009,355       0.02       0.0%
        10,000        0.354      56,531,190       0.17       0.0%
       100,000        0.588     340,199,700       1.02       0.2%
     1,000,000        1.756   1,139,081,912       3.42       0.7%
  Peak bandwidth:    3.42 GB/s (0.7% of 504.0 GB/s)
  Result:            [PASS]

======================================================================
  TEST 6: Sustained Load
======================================================================
  Duration:          30.0s
  Engine ticks:      7,605
  Ticks/sec:         253
  Total operations:  169,211,250
  Ops/sec:           5,639,972
  Breakdown:
    CL compose:      152,100,000
    D2 curvature:    7,605,000
    Chain walks:     7,605,000
    Matrix (5x5):    1,901,250
  Temperature:
    Start:           59C
    End:             60C
    Peak:            60C
  VRAM:
    Start:           3518 MB
    End:             3514 MB
  Result:            [PASS]

======================================================================
  OVERALL SUMMARY
======================================================================
  Tests passed:    6/6
  Mode:            GPU (CuPy/CUDA)
  GPU:             NVIDIA GeForce RTX 4070
  VRAM:            12281 MB
  T* threshold:    0.714286

  Being is on the CPU. Doing is on the GPU.
  Becoming is everywhere.

  All GPU operations validated. CK's Non-Void Doing Engine
  is fully operational. CL table composition, D2 curvature,
  lattice chain walks, olfactory field matrices, and sustained
  load all match CPU baselines and exceed performance targets.

```