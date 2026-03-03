# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_btq_tests.py -- Tests for Universal BTQ Decision Kernel
=============================================================
Operator: COUNTER (2) -- measuring correctness.

Tests all new modules from Task Pack 2:
  - ck_btq.py (Universal BTQ kernel + 4 domains)
  - ck_sim_btq.py (LocomotionDomain adapter, backward compat)
  - ck_fractal_health.py (Health monitor, drift detection)
  - ck_llm_filter.py (LLM filter, MockLLM)
  - ck_zynq_dog.py (Zynq dog simulation stubs)

Run: python -m ck_sim.ck_btq_tests

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import sys
import math

# ── Test Framework (same as ck_sim_tests.py) ──

passed = 0
failed = 0
total = 0


def test(name: str, condition: bool, detail: str = ""):
    global passed, failed, total
    total += 1
    if condition:
        passed += 1
        print(f"  PASS  {name}")
    else:
        failed += 1
        print(f"  FAIL  {name}  {detail}")


def section(name: str):
    print(f"\n{'='*60}")
    print(f"  {name}")
    print(f"{'='*60}")


# ==============================================================
#  SECTION 1: Universal Kernel Protocol
# ==============================================================

def test_universal_kernel():
    section("Universal Kernel Protocol")

    from ck_sim.ck_btq import (
        UniversalBTQ, Candidate, BTQDomain,
        LanguageDomain, MemoryDomain, BioLatticeDomain,
    )

    # Test: domain registration
    btq = UniversalBTQ()
    lang = LanguageDomain(seed=42)
    mem = MemoryDomain(seed=42)
    bio = BioLatticeDomain(seed=42)

    btq.register_domain(lang)
    btq.register_domain(mem)
    btq.register_domain(bio)

    test("Register language domain", "language" in btq.domains)
    test("Register memory domain", "memory" in btq.domains)
    test("Register bio domain", "bio" in btq.domains)

    # Test: unknown domain raises ValueError
    try:
        btq.decide("nonexistent")
        test("Unknown domain raises error", False)
    except ValueError:
        test("Unknown domain raises error", True)

    # Test: Language domain decide
    chosen, approved = btq.decide("language", {}, {'target_length': 5}, n_candidates=16)
    test("Language decide returns candidates", len(approved) > 0)
    test("Language decide returns chosen", chosen is not None)
    test("Language chosen has score", chosen.score is not None)
    test("Language chosen has band", chosen.score.band in ("GREEN", "YELLOW", "RED"))
    test("Language chosen domain tag", chosen.domain == "language")

    # Test: Language candidate has text
    test("Language payload has text",
         hasattr(chosen.payload, 'text') and len(chosen.payload.text) > 0)
    test("Language payload has operators",
         hasattr(chosen.payload, 'operator_sequence'))

    # Test: Memory domain decide (with synthetic brain state)
    from ck_sim.ck_sim_brain import Crystal, BrainState
    from ck_sim.ck_sim_heartbeat import HARMONY, LATTICE, CL

    crystals = [
        Crystal(ops=[HARMONY, HARMONY], length=2,
                fuse=CL[HARMONY][HARMONY], seen=50, confidence=0.1),
        Crystal(ops=[LATTICE, HARMONY], length=2,
                fuse=CL[LATTICE][HARMONY], seen=30, confidence=0.06),
    ]
    env = {'crystals': crystals, 'tl_total': 500}

    chosen_m, approved_m = btq.decide("memory", env, {}, n_candidates=16)
    test("Memory decide returns candidates", len(approved_m) > 0)
    test("Memory decide returns chosen", chosen_m is not None)
    test("Memory chosen has score", chosen_m.score is not None)

    # Test: Bio domain decide
    chosen_b, approved_b = btq.decide("bio", {}, {}, n_candidates=16)
    test("Bio decide returns candidates", len(approved_b) > 0)
    test("Bio decide returns chosen", chosen_b is not None)
    test("Bio chosen has sequence",
         hasattr(chosen_b.payload, 'sequence') and len(chosen_b.payload.sequence) > 0)
    test("Bio chosen has force vectors",
         hasattr(chosen_b.payload, 'force_vectors') and len(chosen_b.payload.force_vectors) > 0)

    # Test: score values are sensible
    for name, ch in [("lang", chosen), ("mem", chosen_m), ("bio", chosen_b)]:
        test(f"{name} e_out in [0,1]", 0.0 <= ch.score.e_out <= 1.0,
             f"got {ch.score.e_out}")
        test(f"{name} e_in in [0,1]", 0.0 <= ch.score.e_in <= 1.0,
             f"got {ch.score.e_in}")
        test(f"{name} e_total in [0,1]", 0.0 <= ch.score.e_total <= 1.0,
             f"got {ch.score.e_total}")


# ==============================================================
#  SECTION 2: Locomotion Domain Adapter
# ==============================================================

def test_locomotion_adapter():
    section("Locomotion Domain Adapter")

    from ck_sim.ck_btq import UniversalBTQ
    from ck_sim.ck_sim_btq import (
        LocomotionDomain, BTQStack, MotorConstraints
    )

    # Test: LocomotionDomain registers
    btq = UniversalBTQ()
    loco = LocomotionDomain(seed=42)
    btq.register_domain(loco)
    test("Locomotion domain registers", "locomotion" in btq.domains)

    # Test: decide produces results
    chosen, approved = btq.decide("locomotion", {}, {}, n_candidates=32)
    test("Locomotion decide returns approved", len(approved) > 0)
    test("Locomotion decide returns chosen", chosen is not None)
    test("Locomotion chosen has GaitCandidate payload",
         hasattr(chosen.payload, 'trajectory'))
    test("Locomotion chosen has score", chosen.score is not None)
    test("Locomotion chosen score has band",
         chosen.score.band in ("GREEN", "YELLOW", "RED"))

    # Test: existing BTQStack still works (backward compatibility)
    stack = BTQStack(seed=42)
    old_chosen, old_approved = stack.decide(n_candidates=32)
    test("BTQStack.decide still works", old_chosen is not None)
    test("BTQStack.decide produces scored candidates",
         old_chosen.score is not None)
    test("BTQStack.decide score has band",
         old_chosen.score.band in ("GREEN", "YELLOW", "RED"))


# ==============================================================
#  SECTION 3: Backward Compatibility
# ==============================================================

def test_backward_compat():
    section("Backward Compatibility")

    from ck_sim.ck_sim_btq import CandidateScore

    # Test: CandidateScore details field exists with default
    score = CandidateScore()
    test("CandidateScore has details field", hasattr(score, 'details'))
    test("CandidateScore details default is empty dict",
         score.details == {})

    # Test: CandidateScore with details
    score2 = CandidateScore(e_out=0.3, e_in=0.2, details={'key': 'value'})
    test("CandidateScore accepts details", score2.details == {'key': 'value'})
    test("CandidateScore preserves e_out", score2.e_out == 0.3)

    # Test: existing imports still work
    from ck_sim.ck_sim_btq import (
        BBlock, TBlock, QBlock, BTQStack,
        GaitCandidate, GaitParams, MotorConstraints,
        einstein_score, tesla_score, score_candidate,
        generate_trajectory, apply_perturbation, measure_recovery,
        GAIT_TROT, GAIT_WALK, GAIT_BOUND, GAIT_PRONK,
        N_LEGS, N_JOINTS, N_JOINTS_PER_LEG,
    )
    test("All existing ck_sim_btq imports work", True)

    # Test: score_candidate still works
    params = GaitParams()
    cand = generate_trajectory(params)
    constraints = MotorConstraints()
    score = score_candidate(cand, constraints)
    test("score_candidate produces valid score", score.e_total >= 0)
    test("score_candidate band valid", score.band in ("GREEN", "YELLOW", "RED"))


# ==============================================================
#  SECTION 4: Fractal Health Monitor
# ==============================================================

def test_fractal_health():
    section("Fractal Health Monitor")

    from ck_sim.ck_fractal_health import (
        RunningStats, CrystalHealth, DomainHealth, HealthMonitor
    )
    from ck_sim.ck_sim_btq import CandidateScore
    from ck_sim.ck_sim_heartbeat import HARMONY

    # Test: RunningStats
    stats = RunningStats()
    for v in [1.0, 2.0, 3.0, 4.0, 5.0]:
        stats.update(v)
    test("RunningStats count", stats.count == 5)
    test("RunningStats mean", abs(stats.mean - 3.0) < 0.001,
         f"got {stats.mean}")
    test("RunningStats min", stats.min_val == 1.0)
    test("RunningStats max", stats.max_val == 5.0)
    test("RunningStats std > 0", stats.std > 0)

    # Test: RunningStats trend detection
    trend_stats = RunningStats()
    for i in range(20):
        trend_stats.update(float(i) * 0.1)  # Ascending values
    test("Trend slope positive for ascending",
         trend_stats.trend_slope > 0.001,
         f"got {trend_stats.trend_slope}")

    descending = RunningStats()
    for i in range(20):
        descending.update(2.0 - float(i) * 0.1)
    test("Trend slope negative for descending",
         descending.trend_slope < -0.001,
         f"got {descending.trend_slope}")

    # Test: CrystalHealth
    ch = CrystalHealth()
    ch.feed(HARMONY, 0.1)
    ch.feed(HARMONY, 0.2)
    ch.feed(0, 0.05)  # Non-HARMONY
    test("Crystal formation count", ch.formation_count == 3)
    test("Crystal fuse stability", abs(ch.fuse_stability - 2.0/3.0) < 0.001)
    test("Crystal avg confidence", abs(ch.avg_confidence - 0.35/3.0) < 0.01)

    # Test: HealthMonitor
    monitor = HealthMonitor(window_size=20)

    # Feed GREEN scores
    for _ in range(15):
        monitor.feed("motion", CandidateScore(e_out=0.1, e_in=0.1, e_total=0.1, band="GREEN"))
    health = monitor.get_health("motion")
    test("Health monitor tracks domain", health.domain == "motion")
    test("Health monitor decision count", health.decision_count == 15)
    test("Health band GREEN for low scores", health.band == "GREEN")
    test("Band distribution GREEN dominant",
         health.band_distribution["GREEN"] == 1.0)

    # Feed RED scores to degrade
    for _ in range(10):
        monitor.feed("motion", CandidateScore(e_out=0.8, e_in=0.7, e_total=0.75, band="RED"))
    health2 = monitor.get_health("motion")
    test("Health band changes with RED scores",
         health2.band in ("YELLOW", "RED"))

    # Test: drift detection
    drift_mon = HealthMonitor(window_size=100)
    for i in range(30):
        val = 0.1 + i * 0.02  # Ascending
        drift_mon.feed("test", CandidateScore(
            e_out=val, e_in=val, e_total=val,
            band="GREEN" if val < 0.3 else "YELLOW"))
    direction, slope = drift_mon.detect_drift("test")
    test("Drift detects degrading", direction == "degrading",
         f"got {direction} slope={slope}")

    # Test: system band worst-domain rule
    sys_mon = HealthMonitor(window_size=10)
    for _ in range(10):
        sys_mon.feed("a", CandidateScore(e_total=0.1, band="GREEN"))
        sys_mon.feed("b", CandidateScore(e_total=0.8, band="RED"))
    test("System band RED when one domain RED",
         sys_mon.classify_system_band() == "RED")

    all_green = HealthMonitor(window_size=10)
    for _ in range(10):
        all_green.feed("x", CandidateScore(e_total=0.1, band="GREEN"))
        all_green.feed("y", CandidateScore(e_total=0.15, band="GREEN"))
    test("System band GREEN when all GREEN",
         all_green.classify_system_band() == "GREEN")


# ==============================================================
#  SECTION 5: LLM Filter
# ==============================================================

def test_llm_filter():
    section("LLM Filter")

    from ck_sim.ck_llm_filter import (
        MockLLM, LLMFilterDomain, LLMFilter, LLMCandidate
    )
    from ck_sim.ck_btq import UniversalBTQ

    # Test: MockLLM deterministic
    llm1 = MockLLM(seed=42)
    llm2 = MockLLM(seed=42)
    r1 = llm1.generate("explain CK", temperature=0.7)
    r2 = llm2.generate("explain CK", temperature=0.7)
    test("MockLLM deterministic same seed", r1 == r2)
    test("MockLLM produces text", len(r1) > 10)

    # Different seeds produce different text
    llm3 = MockLLM(seed=99)
    r3 = llm3.generate("explain CK", temperature=0.7)
    # May or may not differ due to template selection, so just check it runs
    test("MockLLM different seed runs", len(r3) > 10)

    # Test: LLMFilterDomain as BTQ domain
    domain = LLMFilterDomain(seed=42)
    test("LLM domain name", domain.name == "llm")

    btq = UniversalBTQ()
    btq.register_domain(domain)

    goal = {'prompt': 'explain coherence', 'target_length': 100}
    chosen, approved = btq.decide("llm", {}, goal, n_candidates=8)
    test("LLM decide returns approved", len(approved) > 0)
    test("LLM decide returns chosen", chosen is not None)
    test("LLM chosen has text", len(chosen.payload.text) > 0)
    test("LLM chosen has score", chosen.score is not None)
    test("LLM chosen band valid",
         chosen.score.band in ("GREEN", "YELLOW", "RED"))

    # Test: LLMFilter high-level API
    f = LLMFilter(seed=42)
    result = f.query("explain the CK coherence machine", n_candidates=8)
    test("LLMFilter.query returns result", result is not None)
    test("LLMFilter result has response", 'response' in result)
    test("LLMFilter result has band", 'band' in result)
    test("LLMFilter response is string", isinstance(result['response'], str))
    test("LLMFilter response has content", len(result['response']) > 10)

    # Test: query_safe returns string
    text = f.query_safe("explain CK")
    test("LLMFilter.query_safe returns string", isinstance(text, str))
    test("LLMFilter.query_safe has content", len(text) > 10)

    # Test: health monitor is fed
    test("LLM health monitor fed",
         f.health.get_health("llm").decision_count >= 1)


# ==============================================================
#  SECTION 6: Zynq Dog Simulation
# ==============================================================

def test_zynq_dog():
    section("Zynq Dog Simulation")

    from ck_sim.ck_zynq_dog import (
        SharedMemory, PSCore0, PSCore1, PLFabric,
        DockController, ZynqDogSim
    )

    # Test: SharedMemory
    shared = SharedMemory()
    test("SharedMemory coherence window size",
         len(shared.coherence_window) == 32)
    test("SharedMemory initial tick", shared.tick_count == 0)
    test("SharedMemory initial state", shared.chosen_idx == -1)

    # Test: DockController state machine
    dock = DockController()
    test("Dock initial state IDLE", dock.state == "IDLE")

    dock.set_target(3.0, 0.0)
    test("Dock transitions to WALK", dock.state == "WALK")
    test("Dock distance computed", abs(dock.distance - 3.0) < 0.01)

    # Walk a few steps toward target (not enough to finish)
    for _ in range(3):
        dock.update()
    test("Dock advances position", dock.distance < 3.0)
    test("Dock still WALK after 3 steps", dock.state == "WALK",
         f"got {dock.state} at dist={dock.distance:.3f}")

    # Track all states visited during full walk
    visited_states = set()
    for _ in range(200):
        visited_states.add(dock.state)
        dock.update()
        if dock.state == "IDLE":
            visited_states.add("IDLE")
            break
    test("Dock visits APPROACH during walk", "APPROACH" in visited_states,
         f"visited: {visited_states}")
    test("Dock completes to IDLE",
         dock.state == "IDLE",
         f"got {dock.state}")

    # Test: DockController constraints change by state
    dock2 = DockController()
    c_idle = dock2.get_constraints()
    dock2.set_target(3.0, 0.0)  # -> WALK
    c_walk = dock2.get_constraints()
    # Force into APPROACH
    dock2.current_pos[0] = 2.6
    dock2.distance = 0.4
    dock2.state = "APPROACH"
    c_approach = dock2.get_constraints()
    test("APPROACH has lower max_velocity", c_approach.max_velocity < c_walk.max_velocity)

    # Test: ZynqDogSim full system
    sim = ZynqDogSim()
    sim.dock.set_target(1.0, 0.0)

    # Run 50 ticks
    for _ in range(50):
        sim.run_tick()

    test("ZynqDogSim ticks advance", sim.shared.tick_count == 50)
    test("ZynqDogSim brain advances", sim.core0.brain.brain_ticks > 0)
    test("ZynqDogSim body advances", sim.core1.body.heartbeat.phase > 0)
    test("ZynqDogSim has status", len(sim.status()) > 0)

    # Test: IMU simulation produces data
    test("IMU accel has gravity component",
         sim.shared.imu_accel[2] > 9.0)


# ==============================================================
#  MAIN
# ==============================================================

def main():
    print("CK BTQ Universal Kernel Tests")
    print("=" * 60)

    test_universal_kernel()
    test_locomotion_adapter()
    test_backward_compat()
    test_fractal_health()
    test_llm_filter()
    test_zynq_dog()

    # Summary
    print(f"\n{'='*60}")
    print(f"  RESULTS: {passed}/{total} passed, {failed} failed")
    print(f"{'='*60}")

    if failed > 0:
        print(f"\n  ** {failed} TESTS FAILED **")
        sys.exit(1)
    else:
        print(f"\n  ALL {total} TESTS PASSED")
        sys.exit(0)


if __name__ == '__main__':
    main()
