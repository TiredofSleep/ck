# CORE Version History

## v1.4 (March 2026) — CURRENT

### Changes from v1.3
- Meta-Lens Architecture: TopologyLens (I/0 decomposition), Russell Codec (6D toroidal), SSA trilemma, SIGA classifier
- RATE Engine: R_inf recursive topological emergence with delta-modulated seeds
- FOO Engine: Fractal Optimality Operator, Phi(kappa) complexity horizons for all 41 problems
- Breath Engine: Breath-Defect Flow Model (B_idx, fear-collapse detection, E/C decomposition)
- 41-problem coherence manifold: 6 Clay + 13 standalone + 18 neighbor + 4 bridge
- ScanMode extended: 8 depth levels (SURFACE=3, SHALLOW=6, MEDIUM=9, DEEP=12, EXTENDED=15, THOROUGH=18, INTENSIVE=21, OMEGA=24)
- COMPLEXITY_KAPPA and PHI_CALIBRATED extended from 6 to 41 problems
- Critical bug fix: defect_delta → delta_value (engines were reading zeros)
- New files: ck_topology_lens.py, ck_russell_codec.py, ck_ssa_engine.py, ck_rate_engine.py, ck_foo_engine.py, ck_breath_engine.py
- TIGOS tig_foo kernel spec and MCO integration notes for R16 target

### Validation
- 529/529 tests pass (all previous + 33 breath + meta-lens operational tests)
- All 41 problems produce valid TopologyLens, SSA, RATE, FOO, Breath analyses
- Breath atlas: 6 Clay problems measured (B_idx range 0.00-0.37)
- SSA trilemma matches predictions: affirmative problems break C1, gap problems break C3
- RATE convergence confirmed for all 6 Clay problems
- Phi(kappa) horizons consistent with calibrated values

### New CORE Document
- Breath_Defect_Flow.md — Breath-defect flow model formalism (v1.0)

---

## v1.3 (March 2026)

### Changes from v1.1
- Deep Experiment Protocol: L48/L96 partition stability, 10K-seed counter-example hunt
- Scaling law extraction: convergence exponents for all 6 problems
- Cross-problem correlation matrix: trajectory-level two-class evidence
- New files: `ck_deep_experiments.py`, `ck_experiment_runner.py`
- No CORE document changes — all updates are empirical evidence

### Validation
- 151/151 tests pass (107 base + 44 attack)
- 60,000+ probes: 0 falsifications
- Partition stability verified at L48 AND L96
- Scaling laws extracted for all 6 problems
- Cross-problem correlation confirms two-class partition

---

## v1.1 (February 2026)

### Documents
- TIG_Operator_Grammar_0-9.md — 10 operators, 4D bundle, composition table, fractal recursion (FROZEN v1.0)
- SDV_Axiom_Definition.md — Dual-void axiom, two problem classes, SCA loop (FROZEN v1.0 + topology extension)
- Delta_Defect_Framework.md — Universal defect functional, 6 instantiations, coherence law (FROZEN v1.0)
- **Dual_Topology_Framework.md** — NEW: Topological reformulation of SDV (intrinsic vs representational topology)

### Changes from v1.0
- Added `Dual_Topology_Framework.md`: formal dual-topology axiom, per-problem topology table, two-class partition recast as topological classification
- Added Section 7 (Topological Interpretation) to `SDV_Axiom_Definition.md` — extension only, no modifications to frozen v1.0 axiom statements
- All v1.0 FROZEN INVARIANTS remain unchanged

### Status
Original three documents remain FROZEN INVARIANTS.
Dual_Topology_Framework.md is FROZEN as v1.0 of the topology layer.

### Validation
- 36 experimental runs (4 seeds x 3 depths x 3 modes): 0 anomalies, 0 contradictions
- 151/151 tests pass (107 base + 44 attack)
- All verdicts and decisions seed-stable
- v1.2 Hardware Attack: 1000-seed sweep, 0 falsifications

---

## v1.0 (February 2026) — FROZEN BASELINE

### Documents
- TIG_Operator_Grammar_0-9.md — 10 operators, 4D bundle, composition table, fractal recursion
- SDV_Axiom_Definition.md — Dual-void axiom, two problem classes, SCA loop
- Delta_Defect_Framework.md — Universal defect functional, 6 instantiations, coherence law

### Status
All three documents are FROZEN INVARIANTS.
No modifications permitted without explicit version bump authorized by project owner.

### Validation
- 36 experimental runs (4 seeds x 3 depths x 3 modes): 0 anomalies, 0 contradictions
- 107/107 tests pass
- All verdicts and decisions seed-stable
