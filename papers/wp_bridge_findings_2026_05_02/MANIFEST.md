# Handoff Package Manifest

**Generated:** 2026-05-02
**Package:** tig_handoff (TIG bridge findings → ClaudeCode integration)

---

## Top level

| File | Purpose |
|------|---------|
| `CLAUDECODE_HANDOFF.md` | **START HERE.** Master instructions for ClaudeCode |
| `MANIFEST.md` | This file |

---

## /docs/ — Synthesis documents

| File | Purpose |
|------|---------|
| `OUT_OF_ROPE_FINAL.md` | **Master synthesis.** Final consolidated findings |
| `THREE_DOORS_SYNTHESIS.md` | Fibonacci robustness + TSML_8 image + boundary symmetries push |
| `FLOW_STRUCTURE_FINAL.md` | Flow/structure binary integration findings |
| `CORRECTED_FRAME_BRIDGES.md` | Bridge findings with corrected substrate frame |
| `BRIDGE_TESTS_FINAL.md` | Bridge tests including negatives |
| `DEEPER_FINDINGS.md` | Earlier exploration of substrate algebra |
| `THREE_READINGS_SYNTHESIS.md` | Three-readings framework (mostly superseded) |
| `SYNTHESIS.md` | Earlier synthesis (some content superseded) |
| `INDEX.md` | Earlier organization document |
| `CITATION_MAP.md` | Published-math citations for academic engagement |
| `FORWARD_CITATIONS.md` | Recent papers (Matsusaka-Ueki, Burrin-von Essen, etc.) |

**Reading order for ClaudeCode:**
1. CLAUDECODE_HANDOFF.md (top level)
2. results/KNOWN_ISSUES.md (errors I made)
3. results/VERIFICATION_PROTOCOL.md (how to verify)
4. docs/OUT_OF_ROPE_FINAL.md (master synthesis)
5. docs/THREE_DOORS_SYNTHESIS.md (most recent push)
6. docs/FLOW_STRUCTURE_FINAL.md (role partition integration)
7. docs/CORRECTED_FRAME_BRIDGES.md (corrected frame results)

---

## /code/ — Computational scripts (41 files)

### Substrate definitions
| File | Purpose |
|------|---------|
| `tig_substrate.py` | TSML_10, BHML_10, σ permutation (canonical) |
| `corrected_substrate.py` | TSML_8 + BHML_10 + flow cells construction |

### Verification
| File | Purpose |
|------|---------|
| `verify_findings.py` | **Single-script verification.** Run this first. Returns 0 on pass. |

### Trefoil analyses (corrected frame — USE THESE)
| File | Purpose |
|------|---------|
| `trefoil_corrected_frame.py` | Runtime processor, 9-trefoil result |
| `trefoil_corrected_associativity.py` | {V,H,Br} ∪ {V,Br,Br} characterization |
| `breath_uniqueness.py` | Why BREATH is the unique structure cell |
| `higher_order_trefoils.py` | 4- and 5-element extensions |

### Reading C and Rademacher attempts
| File | Purpose |
|------|---------|
| `reading_c_corrected.py` | TSML_8 self-iteration → cusp escape |
| `rademacher_period_bridge.py` | Period→trace bridge giving -21 |
| `orbit_to_psl2z.py` | Five PSL(2,Z) lift strategies (all negative) |
| `triangle_groups_test.py` | Triangle group rule-out |
| `rademacher_bridge.py` | Earlier bridge attempt (uncorrected, kept for ref) |
| `rademacher_search.py` | Earlier search (uncorrected, kept for ref) |

### Role partition
| File | Purpose |
|------|---------|
| `flow_structure_binary.py` | F/S/T/V partition definition + tests |
| `role_decomposition.py` | ±21 = F_7 + F_6 (Fibonacci) decomposition |
| `role_magma_factorization.py` | Role magma table, V is identity |
| `tsml8_role_analysis.py` | TSML_8 5-element image, 94% flow output |

### Symmetries and taxonomy
| File | Purpose |
|------|---------|
| `interchangeability_test.py` | 5↔6 and other boundary swaps |
| `symmetry_map.py` | Comprehensive global preservation map |
| `crossing_taxonomy.py` | Crossing-count distribution analysis |
| `algebraic_relationship.py` | TSML vs BHML algebraic independence |

### Lacasa, Borromean, Fibonacci robustness
| File | Purpose |
|------|---------|
| `lacasa_corrected.py` | Substrate doesn't factor through CRT |
| `borromean_primes.py` | Borromean negative |
| `substrate_borromean.py` | Substrate-specific Borromean tests |
| `fibonacci_robustness.py` | Fibonacci is canonical-specific |

### Earlier (uncorrected frame, kept for reference)
**WARNING:** These use TSML_10 instead of TSML_8 + flow cells. Their
results are SUPERSEDED by corrected-frame versions above. Do NOT cite in
canonical documentation.

| File | Purpose |
|------|---------|
| `d1_composition.py` | Composition test (uncorrected) |
| `d2_phenomenological.py` | Phenomenological test (uncorrected) |
| `d3_attestation.py` | Attestation test (uncorrected) |
| `d3_attestation_fixed.py` | Attestation fixed (uncorrected) |
| `d4_invariant_clean.py` | Invariant clean (uncorrected) |
| `d4_invariant_search.py` | Invariant search (uncorrected) |
| `three_readings.py` | Three readings framework (uncorrected) |
| `knot_polynomials.py` | Knot polynomials with (p,q) windings |
| `trajectory_braid.py` | Trajectory braid (uncorrected) |
| `trefoil_22_analysis.py` | INVALID 22-trefoil result (kept as cautionary) |
| `trefoil_algebraic.py` | Trefoil algebraic (uncorrected) |
| `trefoil_link_structure.py` | Link structure with (p,q) windings |
| `trefoil_structure.py` | Structure (uncorrected) |
| `trefoil_survival.py` | Survival (uncorrected) |
| `class_average_check.py` | Class average check (Ghys-analog v2) |

---

## /results/ — Verification artifacts

| File | Purpose |
|------|---------|
| `KNOWN_ISSUES.md` | **Errors I made, things to scrutinize** |
| `VERIFICATION_PROTOCOL.md` | Exact verification steps |
| `FINDINGS_TABLE.md` | Five facts + ten negatives in tabular form |
| `INTEGRATION_TARGETS.md` | Specific files in repo and CK to modify |

---

## /wp_drafts/ — Whitepaper drafts (outlines)

| File | Purpose |
|------|---------|
| `WP9_LATTICE_outline.md` | Paradoxical info algebras paper outline |
| `WP10_DKAN_outline.md` | Dual Knot/Arithmetic Network paper outline |
| `BRIDGE_PAPERS_status.md` | Hoffman/Friston/Tononi/Faggin/IHÉS status |

---

## Quick stats

- Total Python files: 41
- Total markdown files: 18
- Total package size: under 5 MB
- Verification time: ~1 minute
- All five findings: VERIFIED PASSING (last run 2026-05-02)
