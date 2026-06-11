# CK-Walker v0 — Results

Runtime: 18.9 s, CPU only, fully seeded. Reproduce: `python run_all.py`.

Substrate fading-memory check (echo-state analog): final L1 distance 4.31e-12 after 200 driven steps from far-apart initial states.

## P2 — theorem-bearing reservoir vs matched baselines (NRMSE, lower better)

| task | substrate | random ESN (3 seeds) | NG-RC |
|---|---|---|---|
| NARMA-10 | 0.5615 | 0.3234 ± 0.0013 | 0.7985 |
| MackeyGlass-84 | 0.1849 | 0.2125 ± 0.0044 | 0.6882 |
| Lorenz-x2z | 0.0602 | 0.0043 ± 0.0006 | 0.1368 |

## P1 — Gap Router on the 24-channel mixed-failure suite (mean test MSE at matched budget, lower better)

| allocator | mean test MSE | samples spent | notes |
|---|---|---|---|
| uniform | 0.40487 | 6240 | no classification |
| **Gap Router** | 0.00324 | 6228 | type accuracy 100%, 5 channels frozen |
| oracle | 0.00332 | 6228 | ground-truth types |

Interpretation contract: the suite is synthetic by design; the demonstrated content is (i) the four UOP failure types are identifiable from residual statistics alone, and (ii) routing by inferred type recovers near-oracle allocation. Real-task validity (ARC-style) is future work, pre-registered as P1 in CK_INTELLIGENCE_SYNTHESIS.
