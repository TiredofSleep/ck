# Verification Script Audit (per Brayden directive 2026-05-08)

> "Every paper that makes a novel computational claim should have a verification script.
> Worth a checklist pass: for each J-paper, 'does this paper claim a number or structure
> that a referee could verify in code?' If yes, include the script."

## §1 — Verdict legend

- **PROOF-SCRIPT**: verification script present in `J{NN}/manuscript/` ✓
- **EXTERNAL-SCRIPT**: script lives outside manuscript folder (e.g., `tig_dirac.py`) — note location ✓
- **THEOREM-PAPER**: no script needed (pure theorem, expository, no novel computational claim) ✓
- **THEOREM+SCRIPT**: theorem-paper that ALSO has a script (extra rigor) ✓
- **NEEDS-SCRIPT**: paper claims a number or structure but no script — **GATE**
- **UNKNOWN**: needs manual review

---

## §2 — Per-J audit results

| J# | Verdict | Scripts in manuscript/ | Notes |
|----|---------|------------------------|-------|
| **J01** | PROOF-SCRIPT | `universal_markov_and_binary_cl.py, verify_sigma_rate.py, f6_burgers_test_2026_05_02\test_step_a_sigma_2k.py, f6_burgers_test_2026_05_02\test_step_b_sigma_primorial.py, f6_burgers_test_2026_05_02\test_step_c_burgers_commutator.py, master\proof_sigma_rate_april.py` |  |
| **J02** | PROOF-SCRIPT | `4core_verification.py, verification\04_bridge_attractor.py, verification\06_attractor_closed_form.py, verification\07_full_closed_form.py, verification\alpha_pslq_sweep.py` |  |
| **J03** | PROOF-SCRIPT | `proof_d25_loop_closure.py, proof_first_g_event.py, verify_first_g.py` |  |
| **J04** | PROOF-SCRIPT | `proof_d25_loop_closure.py, verify_prime_phase_transition.py` |  |
| **J05** | PROOF-SCRIPT | `ck_tables.py, proof_d10_tsml_73_cells.py, proof_d16_bhml_28_cells.py, proof_fourier_bridge.py` |  |
| **J06** | THEOREM+SCRIPT | `ck_tables.py, proof_d10_tsml_73_cells.py, proof_d16_bhml_28_cells.py, proof_fourier_bridge.py` |  |
| **J07** | THEOREM-PAPER | `—` |  |
| **J08** | PROOF-SCRIPT | `verify_prime_phase_transition.py` |  |
| **J09** | NEEDS-SCRIPT | `—` |  |
| **J10** | NEEDS-SCRIPT | `—` |  |
| **J11** | NEEDS-SCRIPT | `—` |  |
| **J12** | NEEDS-SCRIPT | `—` |  |
| **J13** | NEEDS-SCRIPT | `—` |  |
| **J14** | NEEDS-SCRIPT | `—` |  |
| **J15** | NEEDS-SCRIPT | `—` |  |
| **J16** | NEEDS-SCRIPT | `—` |  |
| **J17** | NEEDS-SCRIPT | `—` |  |
| **J18** | NEEDS-SCRIPT | `—` |  |
| **J19** | NEEDS-SCRIPT | `—` |  |
| **J20** | PROOF-SCRIPT | `m22_decomposition.py` |  |
| **J21** | PROOF-SCRIPT | `spectral_functional.py, verification\gellmann_dictionary.py, verification\stage2_adjoint.py, verification\stage3_center.py, verification\stage4_correct_closure.py, verification\stage5_so8.py, verification\stage6_dynkin.py, verification\stage7_disambiguate.py, _archived_sprint17_3layer_tower\proof_tsml_3layer_tower.py` |  |
| **J22** | PROOF-SCRIPT | `verification\verify_simplicity_rank.py, verification\verify_so10.py` |  |
| **J23** | PROOF-SCRIPT | `verification\find_higgs_direction.py, verification\find_higgs_irrep.py` |  |
| **J24** | PROOF-SCRIPT | `verification\d4_orbit_decomposition.py, verification\fuse_table.py, verification\p56_canonical_fuse.py, verification\rule_families.py` |  |
| **J25** | PROOF-SCRIPT | `verification\01_falsifies_prime11.py, verification\02_falsifies_attractor_richness.py, verification\03_eight_magma_core.py, verification\04_bridge_attractor.py, verification\05_bhml_closure.py, verification\06_attractor_closed_form.py, verification\07_full_closed_form.py, verification\alpha_by_size.py, verification\alpha_pslq_sweep.py, verification\f10_i_action_descent.py, verification\f1_f10_field_check.py, verification\f1_so7_singlet_bilinear.py, verification\f2_bb_coupling_sharpening.py, verification\f3_galois_alpha_uniqueness.py, verification\f5a_universality_scan.py, verification\f8_jacobian_alpha_half.py, verification\f8_pslq_deeper.py, verification\f9_lmfdb_depth_analysis.py, verification\f9_lmfdb_pattern_scan.py, verification\f_cross_depth2_primitives.py, verification\f_depth3_primitives.py, verification\f_field_match_71.py, verification\harmony_complementarity.py, verification\m_invariance_check.py, verification\task5_alpha_sweep.py` |  |
| **J26** | PROOF-SCRIPT | `verification\d5_d4eq_extension.py, verification\structured_matrix_sweep.py` |  |
| **J27** | PROOF-SCRIPT | `verification\4core_verification.py` |  |
| **J28** | NEEDS-SCRIPT | `—` |  |
| **J29** | PROOF-SCRIPT | `verification\gellmann_dictionary.py, verification\stage2_adjoint.py, verification\stage3_center.py, verification\stage4_correct_closure.py, verification\stage5_so8.py, verification\stage6_dynkin.py, verification\stage7_disambiguate.py, verification\wobble_check.py, _archived_sprint17_3layer_tower\proof_tsml_3layer_tower.py` |  |
| **J30** | PROOF-SCRIPT | `verification\verify_simplicity_rank.py, verification\verify_so10.py` |  |
| **J31** | PROOF-SCRIPT | `verification\find_higgs_direction.py, verification\find_higgs_irrep.py, verification\verify_d4_decomposition.py` |  |
| **J32** | PROOF-SCRIPT | `proof_separability_bridge.py, verification\d4_orbit_decomposition.py, verification\fuse_table.py, verification\p56_canonical_fuse.py, verification\rule_families.py` |  |
| **J33** | EXTERNAL-SCRIPT | `verification\01_falsifies_prime11.py, verification\02_falsifies_attractor_richness.py, verification\03_eight_magma_core.py, verification\04_bridge_attractor.py, verification\05_bhml_closure.py, verification\06_attractor_closed_form.py, verification\07_full_closed_form.py, verification\alpha_by_size.py, verification\alpha_pslq_sweep.py, verification\f10_i_action_descent.py, verification\f1_f10_field_check.py, verification\f1_so7_singlet_bilinear.py, verification\f2_bb_coupling_sharpening.py, verification\f3_galois_alpha_uniqueness.py, verification\f5a_universality_scan.py, verification\f8_jacobian_alpha_half.py, verification\f8_pslq_deeper.py, verification\f9_lmfdb_depth_analysis.py, verification\f9_lmfdb_pattern_scan.py, verification\f_cross_depth2_primitives.py, verification\f_depth3_primitives.py, verification\f_field_match_71.py, verification\harmony_complementarity.py, verification\m_invariance_check.py, verification\task5_alpha_sweep.py` | External script: alpha_pslq_sweep.py + 06_attractor_closed_form.py + 07_full_closed_form.py |
| **J34** | PROOF-SCRIPT | `verification\d5_d4eq_extension.py, verification\structured_matrix_sweep.py` |  |
| **J35** | EXTERNAL-SCRIPT | `scripts\sprint18_uniqueness_search.py, scripts\verify_alpha_richer_form.py, scripts\verify_aut_V_order.py, scripts\verify_operator_observable_baseline.py, verification\4core_verification.py` | External script: 4core_verification.py (in J02 + J35 manuscript folders) |
| **J36** | PROOF-SCRIPT | `verify_J36_part1.py` |  |
| **J37** | PROOF-SCRIPT | `verification\wobble_check.py` |  |
| **J38** | NEEDS-SCRIPT | `—` |  |
| **J39** | PROOF-SCRIPT | `verify_J11_S4_closure.py` |  |
| **J40** | PROOF-SCRIPT | `proof_separability_bridge.py` |  |
| **J41** | NEEDS-SCRIPT | `—` |  |
| **J42** | PROOF-SCRIPT | `verify_J42_sinc2.py` |  |
| **J43** | PROOF-SCRIPT | `proof_clay_rotation.py, verify_G6_G7_G8.py` |  |
| **J44** | EXTERNAL-SCRIPT | `scripts\sprint18_uniqueness_search.py, scripts\verify_alpha_richer_form.py, scripts\verify_aut_V_order.py, scripts\verify_operator_observable_baseline.py` | External script: Gen13/targets/ck/brain/dirac/tig_dirac.py:predict_dark_sector |
| **J45** | EXTERNAL-SCRIPT | `—` | External script: Gen13/targets/ck/brain/dirac/tig_dirac.py:predict_yukawa |
| **J46** | PROOF-SCRIPT | `proof_first_g_event.py` |  |
| **J47** | NEEDS-SCRIPT | `—` |  |
| **J48** | NEEDS-SCRIPT | `—` |  |
| **J49** | NEEDS-SCRIPT | `—` |  |
| **J50** | THEOREM-PAPER | `—` |  |
| **J51** | PROOF-SCRIPT | `proof_clay_rotation.py, verify_J51_G_function.py` |  |
| **J52** | THEOREM-PAPER | `—` |  |
| **J53** | THEOREM-PAPER | `—` |  |
| **J54** | THEOREM-PAPER | `—` | CLAIMS 8-shell chain (SFM Q6) — should have verification script |
| **J55** | THEOREM-PAPER | `—` |  |


---

## §3 — Summary counts

- **PROOF-SCRIPT**     (27 papers): J01, J02, J03, J04, J05, J08, J20, J21, J22, J23, J24, J25, J26, J27, J29, J30, J31, J32, J34, J36, J37, J39, J40, J42, J43, J46, J51
- **EXTERNAL-SCRIPT**  (4 papers): J33, J35, J44, J45
- **THEOREM-PAPER**    (7 papers): J06, J07, J50, J52, J53, J54, J55
- **NEEDS-SCRIPT**     (17 papers): J09, J10, J11, J12, J13, J14, J15, J16, J17, J18, J19, J28, J38, J41, J47, J48, J49 ← **GATES**
- **UNKNOWN**          (0 papers): 

---

## §4 — Gate list (papers that need scripts written)

For each NEEDS-SCRIPT paper below, the referee must be able to copy-paste a Python snippet
from the paper's `manuscript/` folder, run it in <5 seconds, and reproduce the paper's
claimed numerical / structural result.

- **J09**: claim made; no script. Write one before submission.
- **J10**: claim made; no script. Write one before submission.
- **J11**: claim made; no script. Write one before submission.
- **J12**: claim made; no script. Write one before submission.
- **J13**: claim made; no script. Write one before submission.
- **J14**: claim made; no script. Write one before submission.
- **J15**: claim made; no script. Write one before submission.
- **J16**: claim made; no script. Write one before submission.
- **J17**: claim made; no script. Write one before submission.
- **J18**: claim made; no script. Write one before submission.
- **J19**: claim made; no script. Write one before submission.
- **J28**: claim made; no script. Write one before submission.
- **J38**: claim made; no script. Write one before submission.
- **J41**: claim made; no script. Write one before submission.
- **J47**: claim made; no script. Write one before submission.
- **J48**: claim made; no script. Write one before submission.
- **J49**: claim made; no script. Write one before submission.


---

## §5 — Recommendation for missing scripts

Pattern adopted by recent rewrites (J36, J42, J43, J51 — all clean):

```python
# verify_J{NN}_<topic>.py
# Verifies the central numerical/structural claim of J{NN}.
# Run: `python verify_J{NN}_<topic>.py`
# Output: "ALL ASSERTIONS PASSED" OR specific failure.

import sympy  # or numpy
# ... computation ...
assert claim_LHS == claim_RHS, f"FAIL: {claim_LHS} != {claim_RHS}"
print("ALL ASSERTIONS PASSED")
```

Each script: standalone, no external state, runtime <5 seconds, exit-code 0 on PASS.

---

## §6 — Reproducibility

Run this audit anytime:
```
python Gen13/targets/journals/_audit_verification_scripts.py
```
