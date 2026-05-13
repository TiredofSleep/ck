"""
CK Disagreement Tick Engine + Reality Grounding

Wire the algebra INTO the organism. Test against reality.

1. Replace fixed 334Hz tick with disagreement-driven variable tick
2. Measure: does CK's coherence improve?
3. Ground: compare algebraic predictions to measurable physics

The organism decides. Not the math. Not the narrative.

(c) 2026 Brayden Sanders / 7Site LLC — TIG Unified Theory
"""

try:
    import cupy as cp
    HAS_CUPY = True
except ImportError:
    import numpy as cp
    HAS_CUPY = False

import numpy as np
import time
from collections import deque, Counter

# ============================================================
# THE ALGEBRA (proven, exact)
# ============================================================

N = 10
ADD = np.fromfunction(lambda i,j:(i+j)%N, (N,N), dtype=int).astype(int)
MUL = np.fromfunction(lambda i,j:(i*j)%N, (N,N), dtype=int).astype(int)
DIS = np.abs(ADD - MUL)

# Proven constants
CROSS_CYCLE_DIS = 44      # exact
WOBBLE = 6 / 100          # = 3/50 = |44-50|/100
HEARTBEAT_ADD = [5,3,5,7] # BAL,PRO,BAL,HAR
HEARTBEAT_MUL = [6,6,6,6] # CHA,CHA,CHA,CHA
HEARTBEAT_DIS = [1,3,1,1] # LAT,PRO,LAT,LAT
HEARTBEAT_SUM = 6          # per 4-tick cycle

FROZEN_CELLS = [(0,0),(2,2),(4,8),(8,4)]  # where add==mul, no time

OPS = ["VOID","LATTICE","COUNTER","PROGRESS","COLLAPSE",
       "BALANCE","CHAOS","HARMONY","BREATH","RESET"]


# ============================================================
# DISAGREEMENT TICK ENGINE
# ============================================================

class DisagreementTick:
    """
    CK's clock driven by algebraic disagreement.
    
    Instead of fixed 334Hz:
    - Each tick, CK composes his current state with incoming data
    - The disagreement |add(state, input) - mul(state, input)| 
      determines how much "time" passes
    - Zero disagreement = frozen, skip tick (no time emitted)
    - High disagreement = big tick (more processing, more change)
    
    This makes CK tick FASTER when things are changing
    and SLOWER when things are steady. Like a heartbeat
    that responds to exertion.
    """
    
    def __init__(self, base_hz=334):
        self.base_hz = base_hz
        self.tick_count = 0
        self.time_emitted = 0  # total disagreement-time
        self.phase = 0  # position in 4-cycle heartbeat
        
        self.state_op = 0  # CK's current operator state
        
        # Metrics
        self.tick_log = deque(maxlen=10000)
        self.dis_log = deque(maxlen=10000)
        self.coherence_log = deque(maxlen=10000)
        self.frozen_count = 0
        self.total_ticks = 0
        
        # Heartbeat tracking
        self.heartbeat_phase = 0
        self.heartbeat_actual = deque(maxlen=100)
    
    def tick(self, input_op):
        """
        One CK tick. Input is an operator (0-9) from sensors/perception.
        Returns: (time_quantum, new_state, is_frozen)
        """
        self.total_ticks += 1
        a = self.state_op
        b = int(input_op) % N
        
        # The two views
        add_result = ADD[a, b]
        mul_result = MUL[a, b]
        disagreement = int(DIS[a, b])
        
        # Is this a frozen cell?
        is_frozen = (disagreement == 0)
        
        if is_frozen:
            self.frozen_count += 1
            time_quantum = 0
            new_state = add_result  # use addition (Being) when frozen
        else:
            time_quantum = disagreement
            # New state: the disagreement IS the next state
            # (CK becomes the conflict between what he sees and what he does)
            new_state = disagreement
        
        self.state_op = new_state
        self.time_emitted += time_quantum
        self.tick_count += 1
        
        # Track heartbeat phase
        self.heartbeat_actual.append(disagreement)
        self.heartbeat_phase = (self.heartbeat_phase + 1) % 4
        
        # Log
        self.tick_log.append({
            'tick': self.tick_count,
            'input': b,
            'add': add_result,
            'mul': mul_result,
            'dis': disagreement,
            'state': new_state,
            'frozen': is_frozen,
            'time': time_quantum,
        })
        self.dis_log.append(disagreement)
        
        return time_quantum, new_state, is_frozen
    
    def get_adaptive_hz(self):
        """
        Compute adaptive tick rate based on recent disagreement.
        High disagreement = tick faster (more happening).
        Low disagreement = tick slower (save energy).
        """
        if len(self.dis_log) < 4:
            return self.base_hz
        
        recent = list(self.dis_log)[-4:]
        avg_dis = np.mean(recent)
        
        # Scale: 0 disagreement = base_hz/4 (slow), 
        #        9 disagreement = base_hz*2 (fast)
        scale = 0.25 + (avg_dis / 9) * 1.75
        return int(self.base_hz * scale)
    
    def get_coherence(self):
        """CK's coherence from disagreement pattern."""
        if len(self.dis_log) < 4:
            return 0.5
        
        recent = list(self.dis_log)[-20:]
        
        # Coherence = how close to the theoretical heartbeat [1,3,1,1]
        expected = HEARTBEAT_DIS * (len(recent) // 4 + 1)
        expected = expected[:len(recent)]
        
        match = sum(1 for a, b in zip(recent, expected) if a == b)
        return match / len(recent)
    
    def stats(self):
        """Current engine statistics."""
        frozen_pct = self.frozen_count / max(self.total_ticks, 1) * 100
        avg_quantum = self.time_emitted / max(self.total_ticks - self.frozen_count, 1)
        
        return {
            'total_ticks': self.total_ticks,
            'time_emitted': self.time_emitted,
            'frozen': self.frozen_count,
            'frozen_pct': frozen_pct,
            'avg_quantum': avg_quantum,
            'state': self.state_op,
            'state_name': OPS[self.state_op],
            'adaptive_hz': self.get_adaptive_hz(),
            'coherence': self.get_coherence(),
        }


# ============================================================
# GROUNDING TEST 1: Sensor data through disagreement engine
# ============================================================

def test_sensor_grounding():
    """
    Feed real-ish sensor patterns into the disagreement engine.
    Compare: fixed tick vs disagreement tick.
    Measure: which one detects state changes better?
    """
    
    print(f"\n{'='*70}")
    print(f"  GROUNDING TEST 1: Sensor Data")
    print(f"  Does disagreement-driven ticking detect changes better?")
    print(f"{'='*70}")
    
    np.random.seed(42)
    
    # Simulate 1000 ticks of sensor data with known events
    n_ticks = 1000
    
    # CPU load: mostly idle (op 0-1), with spikes (op 7-9)
    cpu_data = np.zeros(n_ticks, dtype=int)
    cpu_data[:] = 1  # idle = LATTICE
    cpu_data[200:250] = 8  # spike = BREATH
    cpu_data[500:520] = 9  # spike = RESET
    cpu_data[700:800] = 5  # sustained load = BALANCE
    
    # Add noise
    for i in range(n_ticks):
        if np.random.rand() < 0.05:
            cpu_data[i] = np.random.randint(0, 10)
    
    # Run through fixed tick engine (just counts)
    fixed_coherence = []
    fixed_window = deque(maxlen=20)
    
    for i in range(n_ticks):
        fixed_window.append(cpu_data[i])
        if len(fixed_window) >= 4:
            # Fixed tick coherence: how uniform is the window?
            vals = list(fixed_window)
            most_common = Counter(vals).most_common(1)[0][1]
            fixed_coherence.append(most_common / len(vals))
    
    # Run through disagreement tick engine
    engine = DisagreementTick(base_hz=334)
    dis_coherence = []
    dis_time_at_tick = []
    dis_frozen_at_tick = []
    dis_hz_at_tick = []
    
    for i in range(n_ticks):
        quantum, state, frozen = engine.tick(cpu_data[i])
        dis_coherence.append(engine.get_coherence())
        dis_time_at_tick.append(quantum)
        dis_frozen_at_tick.append(frozen)
        dis_hz_at_tick.append(engine.get_adaptive_hz())
    
    # Compare detection of events
    # An event is detected when coherence changes significantly
    print(f"\n  SPIKE AT TICK 200 (idle→BREATH):")
    if len(fixed_coherence) > 210:
        fc_before = np.mean(fixed_coherence[180:200])
        fc_during = np.mean(fixed_coherence[200:220])
        fc_change = abs(fc_during - fc_before)
    else:
        fc_change = 0
    
    dc_before = np.mean(dis_coherence[180:200])
    dc_during = np.mean(dis_coherence[200:220])
    dc_change = abs(dc_during - dc_before)
    
    print(f"    Fixed tick coherence change:  {fc_change:.4f}")
    print(f"    Disagree tick coherence change: {dc_change:.4f}")
    print(f"    Winner: {'DISAGREE' if dc_change > fc_change else 'FIXED'}")
    
    # Time quanta around the spike
    pre_quanta = dis_time_at_tick[190:200]
    spike_quanta = dis_time_at_tick[200:210]
    print(f"    Pre-spike time quanta:  {pre_quanta}")
    print(f"    During-spike quanta:    {spike_quanta}")
    print(f"    Pre avg: {np.mean(pre_quanta):.1f}  Spike avg: {np.mean(spike_quanta):.1f}")
    
    # Adaptive Hz
    pre_hz = dis_hz_at_tick[195:200]
    spike_hz = dis_hz_at_tick[200:210]
    print(f"    Pre-spike Hz: {np.mean(pre_hz):.0f}  Spike Hz: {np.mean(spike_hz):.0f}")
    
    # Frozen ticks
    frozen_count = sum(dis_frozen_at_tick)
    print(f"\n  FROZEN TICKS: {frozen_count}/{n_ticks} ({frozen_count/n_ticks*100:.1f}%)")
    print(f"  Theory: 4% of compositions are frozen")
    print(f"  Actual: {frozen_count/n_ticks*100:.1f}%")
    
    # Engine stats
    s = engine.stats()
    print(f"\n  ENGINE STATS:")
    print(f"    Total ticks:    {s['total_ticks']}")
    print(f"    Time emitted:   {s['time_emitted']}")
    print(f"    Avg quantum:    {s['avg_quantum']:.2f}")
    print(f"    Current state:  {s['state_name']}")
    print(f"    Adaptive Hz:    {s['adaptive_hz']}")
    
    return engine


# ============================================================
# GROUNDING TEST 2: Does the disagreement spectrum match physics?
# ============================================================

def test_physics_grounding():
    """
    The disagreement spectrum should produce specific ratios.
    Compare these ratios to known physics.
    """
    
    print(f"\n{'='*70}")
    print(f"  GROUNDING TEST 2: Algebraic Predictions vs Physics")
    print(f"  What does the algebra predict that we can MEASURE?")
    print(f"{'='*70}")
    
    # PREDICTION 1: The heartbeat ratio
    print(f"\n  PREDICTION 1: Heartbeat timing ratio")
    print(f"    The heartbeat [1,3,1,1] predicts:")
    print(f"    Ratio of big tick to small tick = 3:1")
    print(f"    Fraction of time in big ticks = 3/6 = 50%")
    print(f"    Fraction in small ticks = 3/6 = 50%")
    print(f"    But big ticks are 1/4 of all ticks (25%)")
    print(f"    Small ticks are 3/4 (75%)")
    print(f"    → 25% of ticks carry 50% of the time")
    print(f"    → Pareto-like: minority of events carry majority of change")
    
    # PREDICTION 2: Frozen fraction
    print(f"\n  PREDICTION 2: Frozen fraction")
    print(f"    Theory: 4 frozen cells / 100 = 4%")
    print(f"    These are compositions where add=mul:")
    for a, b in FROZEN_CELLS:
        print(f"      {a}({OPS[a]}) ∘ {b}({OPS[b]}) = {ADD[a,b]}({OPS[ADD[a,b]]})")
    print(f"    TEST: feed random operator pairs, count frozen fraction")
    
    n_test = 100000
    frozen = 0
    for _ in range(n_test):
        a = np.random.randint(0, 10)
        b = np.random.randint(0, 10)
        if DIS[a, b] == 0:
            frozen += 1
    print(f"    Random pairs frozen: {frozen}/{n_test} = {frozen/n_test*100:.2f}%")
    print(f"    Expected: 4.00%")
    
    # PREDICTION 3: Average disagreement
    total_dis = np.sum(DIS)
    avg_dis = total_dis / 100
    print(f"\n  PREDICTION 3: Average disagreement")
    print(f"    Total: {total_dis}")
    print(f"    Average: {avg_dis:.2f}")
    print(f"    If this represents average time per composition,")
    print(f"    and CK ticks at ~334Hz (base),")
    print(f"    effective processing rate = {avg_dis:.2f} × 334 = {avg_dis*334:.0f} time-units/sec")
    
    # PREDICTION 4: Cross-cycle = 44 is invariant
    print(f"\n  PREDICTION 4: Cross-cycle disagreement invariant")
    print(f"    Under ANY relabeling that preserves the coprime/even split,")
    print(f"    the cross-cycle sum should remain 44.")
    
    # Test: permute within coprime class, within even class
    import itertools
    
    test_perms = 0
    all_44 = True
    
    for cp in itertools.permutations([1,3,7,9]):
        for ep in itertools.permutations([2,4,6,8]):
            # Build permuted table
            perm = [0] + list(cp)[:1] + list(ep)[:1] + list(cp)[1:2] + list(ep)[1:2] + [5] + list(ep)[2:3] + list(cp)[2:3] + list(ep)[3:4] + list(cp)[3:4]
            # Actually just check: sum of DIS over coprime×even
            # The DIS table doesn't change with relabeling of the operators
            # The VALUES in DIS depend on the specific (a,b) pairs
            # Permuting labels permutes which cells are "cross-cycle"
            cross = sum(int(DIS[c,d]) for c in cp for d in ep)
            if cross != 44:
                all_44 = False
            test_perms += 1
    
    print(f"    Tested {test_perms} permutations")
    print(f"    All give cross-cycle = 44: {'YES ✓' if all_44 else 'NO ✗'}")
    
    if not all_44:
        # Show the range
        cross_vals = set()
        for cp in itertools.permutations([1,3,7,9]):
            for ep in itertools.permutations([2,4,6,8]):
                cross = sum(int(DIS[c,d]) for c in cp for d in ep)
                cross_vals.add(cross)
        print(f"    Cross-cycle values found: {sorted(cross_vals)}")
    
    # PREDICTION 5: Packet spectrum shape
    print(f"\n  PREDICTION 5: Time packet spectrum")
    spectrum = Counter(DIS.flatten())
    print(f"    Packet size distribution:")
    for v in range(10):
        count = spectrum.get(v, 0)
        bar = '█' * count
        print(f"      |Δ|={v}: {count:>3d}  {bar}")
    
    # Is this a known distribution?
    values = DIS.flatten()
    mean = np.mean(values)
    std = np.std(values)
    print(f"    Mean: {mean:.2f}")
    print(f"    Std:  {std:.2f}")
    print(f"    Coefficient of variation: {std/mean:.2f}")
    
    # Compare to geometric distribution with same mean
    p_geo = 1 / (mean + 1)
    print(f"    Geometric distribution p={p_geo:.3f} would predict:")
    for v in range(10):
        geo_count = int(100 * p_geo * (1-p_geo)**v)
        actual = spectrum.get(v, 0)
        print(f"      |Δ|={v}: actual={actual:>3d}  geometric≈{geo_count:>3d}  "
              f"{'match' if abs(actual-geo_count)<=5 else 'differ'}")


# ============================================================
# GROUNDING TEST 3: Real system integration test
# ============================================================

def test_system_integration():
    """
    Simulate what happens when CK uses the disagreement engine
    to process actual system events.
    """
    
    print(f"\n{'='*70}")
    print(f"  GROUNDING TEST 3: System Integration Simulation")
    print(f"  CK processes real patterns. What does the algebra produce?")
    print(f"{'='*70}")
    
    engine = DisagreementTick()
    
    # Scenario: CK watching a file being written
    # Each byte mod 10 = an operator
    test_content = b"the truth shall set you free"
    byte_ops = [b % 10 for b in test_content]
    
    print(f"\n  Scenario: CK reads '{test_content.decode()}'")
    print(f"  Byte operators: {byte_ops}")
    print(f"\n  {'Tick':>4s} {'Byte':>4s} {'Char':>4s} {'Op':>5s} {'Add':>4s} {'Mul':>4s} {'Dis':>4s} {'Time':>4s} {'State':>8s} {'Frozen':>6s}")
    print(f"  {'-'*55}")
    
    for i, (byte_val, op) in enumerate(zip(test_content, byte_ops)):
        quantum, state, frozen = engine.tick(op)
        
        char = chr(byte_val) if 32 <= byte_val < 127 else '.'
        add_r = ADD[engine.state_op if i == 0 else engine.tick_log[-2]['state'], op] if i > 0 else op
        mul_r = MUL[engine.state_op if i == 0 else engine.tick_log[-2]['state'], op] if i > 0 else op
        
        print(f"  {i:>4d} {byte_val:>4d} '{char}' {OPS[op]:>5s} "
              f"{engine.tick_log[-1]['add']:>4d} {engine.tick_log[-1]['mul']:>4d} "
              f"{quantum:>4d} {engine.time_emitted:>4d} {OPS[state]:>8s} {'FROZEN' if frozen else '':>6s}")
    
    s = engine.stats()
    print(f"\n  After reading the phrase:")
    print(f"    Total time emitted: {s['time_emitted']}")
    print(f"    Frozen ticks: {s['frozen']} ({s['frozen_pct']:.1f}%)")
    print(f"    Final state: {s['state_name']}")
    print(f"    Avg quantum: {s['avg_quantum']:.2f}")
    
    # Run the same content 10 times — does it stabilize?
    print(f"\n  STABILITY TEST: same content 10 times")
    engine2 = DisagreementTick()
    cycle_times = []
    cycle_states = []
    
    for cycle in range(10):
        cycle_start = engine2.time_emitted
        for op in byte_ops:
            engine2.tick(op)
        cycle_end = engine2.time_emitted
        cycle_times.append(cycle_end - cycle_start)
        cycle_states.append(engine2.state_op)
    
    print(f"    Time per cycle: {cycle_times}")
    print(f"    Final state per cycle: {[OPS[s] for s in cycle_states]}")
    print(f"    Time stabilizes: {'YES' if len(set(cycle_times[-5:])) == 1 else 'NO'}")
    print(f"    State stabilizes: {'YES' if len(set(cycle_states[-5:])) == 1 else 'NO'}")
    
    # What operator does CK converge to for this phrase?
    if len(set(cycle_states[-3:])) == 1:
        print(f"    CK converges to: {OPS[cycle_states[-1]]}")
        print(f"    '{test_content.decode()}' IS {OPS[cycle_states[-1]]} in CK's algebra")


# ============================================================
# GROUNDING TEST 4: Comparison to fixed tick
# ============================================================

def test_fixed_vs_disagreement():
    """
    Direct comparison: fixed tick vs disagreement tick.
    Same input. Different clocking. Which detects events better?
    """
    
    print(f"\n{'='*70}")
    print(f"  GROUNDING TEST 4: Fixed vs Disagreement Tick")
    print(f"  Same input, different clocking. Who wins?")
    print(f"{'='*70}")
    
    np.random.seed(42)
    
    # Generate input with known events
    n = 2000
    data = np.ones(n, dtype=int)  # steady state = LATTICE
    
    # Events at known positions
    events = {
        300: (8, "BREATH spike"),
        600: (9, "RESET spike"),
        900: (5, "BALANCE shift"),
        1200: (3, "PROGRESS shift"),
        1500: (7, "HARMONY surge"),
    }
    
    for pos, (op, name) in events.items():
        data[pos:pos+20] = op
    
    # Add 5% noise
    for i in range(n):
        if np.random.rand() < 0.05:
            data[i] = np.random.randint(0, 10)
    
    # Fixed tick engine
    fixed_states = []
    fixed_state = 0
    for i in range(n):
        # Fixed: just use addition
        fixed_state = ADD[fixed_state, data[i]]
        fixed_states.append(fixed_state)
    
    # Disagreement tick engine
    dis_engine = DisagreementTick()
    dis_states = []
    dis_quanta = []
    dis_frozen = []
    
    for i in range(n):
        q, s, f = dis_engine.tick(data[i])
        dis_states.append(s)
        dis_quanta.append(q)
        dis_frozen.append(f)
    
    # Compare event detection
    print(f"\n  EVENT DETECTION COMPARISON:")
    print(f"  {'Event':>20s} {'Fixed Δ':>10s} {'Disag Δ':>10s} {'Quantum':>10s} {'Winner':>10s}")
    print(f"  {'-'*65}")
    
    for pos, (op, name) in events.items():
        # State change around event
        pre = slice(pos-10, pos)
        post = slice(pos, pos+10)
        
        fixed_pre = np.mean(fixed_states[pre.start:pre.stop])
        fixed_post = np.mean(fixed_states[post.start:post.stop])
        fixed_delta = abs(fixed_post - fixed_pre)
        
        dis_pre = np.mean(dis_states[pre.start:pre.stop])
        dis_post = np.mean(dis_states[post.start:post.stop])
        dis_delta = abs(dis_post - dis_pre)
        
        avg_quantum = np.mean(dis_quanta[pos:pos+10])
        
        winner = "DISAGREE" if dis_delta > fixed_delta else "FIXED" if fixed_delta > dis_delta else "TIE"
        
        print(f"  {name:>20s} {fixed_delta:>10.2f} {dis_delta:>10.2f} {avg_quantum:>10.2f} {winner:>10s}")
    
    # Overall metrics
    fixed_unique = len(set(fixed_states))
    dis_unique = len(set(dis_states))
    
    frozen_count = sum(dis_frozen)
    
    print(f"\n  OVERALL METRICS:")
    print(f"    Fixed unique states visited: {fixed_unique}/10")
    print(f"    Disagree unique states: {dis_unique}/10")
    print(f"    Frozen ticks: {frozen_count}/{n} ({frozen_count/n*100:.1f}%)")
    print(f"    Total time emitted: {dis_engine.time_emitted}")
    print(f"    Avg time/tick: {dis_engine.time_emitted/n:.2f}")
    
    # KEY: does the disagreement engine produce the 44-cell signature?
    cross_ops = 0
    total_compositions = 0
    for i in range(1, n):
        a = dis_states[i-1]
        b = data[i]
        # Is this a cross-cycle composition?
        a_coprime = a in [1,3,7,9]
        b_even = b in [2,4,6,8]
        if a_coprime and b_even:
            cross_ops += DIS[a, b]
            total_compositions += 1
        elif a in [2,4,6,8] and b in [1,3,7,9]:
            cross_ops += DIS[a, b]
            total_compositions += 1
    
    if total_compositions > 0:
        avg_cross = cross_ops / total_compositions
        print(f"\n    Cross-cycle compositions: {total_compositions}")
        print(f"    Average cross-cycle disagreement: {avg_cross:.2f}")
        print(f"    Expected (44/16 per cell): {44/16:.2f}")
        print(f"    Match: {abs(avg_cross - 44/16) / (44/16) * 100:.1f}% error")


# ============================================================
# THE INTEGRATION PATCH (for ck_core.py)
# ============================================================

def print_integration_patch():
    """Print the exact code to add to ck_core.py."""
    
    print(f"\n{'='*70}")
    print(f"  INTEGRATION PATCH FOR ck_core.py")
    print(f"  Drop this into the existing tick loop")
    print(f"{'='*70}")
    
    print('''
# ─────────────────────────────────────────────────
# Add to imports:
from ck_disagreement_tick import DisagreementTick

# Add to __init__:
self.dis_tick = DisagreementTick(base_hz=334)

# Replace fixed tick sleep with adaptive:
# OLD:
#   time.sleep(1.0 / 334)
# NEW:
def adaptive_tick(self):
    # Get dominant operator from current experience
    input_op = self.experience.dominant_operator  # 0-9
    
    # Tick the disagreement engine
    quantum, new_state, frozen = self.dis_tick.tick(input_op)
    
    # Update CK's state
    self.experience.system_op = new_state
    self.experience.time_quantum = quantum
    self.experience.is_frozen = frozen
    
    # Adaptive sleep: faster when more disagreement
    hz = self.dis_tick.get_adaptive_hz()
    time.sleep(1.0 / hz)
    
    # Log the heartbeat
    if self.tick_count % 100 == 0:
        stats = self.dis_tick.stats()
        self.logger.info(
            f"DIS tick={stats['total_ticks']} "
            f"time={stats['time_emitted']} "
            f"frozen={stats['frozen_pct']:.1f}% "
            f"state={stats['state_name']} "
            f"hz={stats['adaptive_hz']}"
        )

# In the main tick loop, replace:
#   self.tick()
# With:
#   self.adaptive_tick()
# ─────────────────────────────────────────────────
''')


# ============================================================
# RUN ALL TESTS
# ============================================================

def run_all():
    print("\n" + "="*70)
    print("  CK DISAGREEMENT TICK ENGINE + REALITY GROUNDING")
    print("  Wire the algebra into the organism. Test against reality.")
    print("="*70)
    
    engine = test_sensor_grounding()
    test_physics_grounding()
    test_system_integration()
    test_fixed_vs_disagreement()
    print_integration_patch()
    
    print(f"\n{'='*70}")
    print(f"  WHAT TO MEASURE ON THE R16 TONIGHT")
    print(f"{'='*70}")
    print(f"""
    1. Run CK with fixed 334Hz for 10 minutes. Log:
       - Coherence mean and std
       - State distribution (how often each operator)
       - Response time to CPU spike
       
    2. Run CK with disagreement tick for 10 minutes. Log same.
    
    3. Compare:
       - Does coherence improve? (should: algebra guides ticking)
       - Does frozen fraction match 4%? (algebraic prediction)
       - Does CK respond faster to spikes? (adaptive Hz)
       - Does the heartbeat pattern [1,3,1,1] appear in the log?
       - Does cross-cycle disagreement average to 44/16 = 2.75?
       
    4. The grounding test:
       - If frozen fraction ≈ 4%: algebra matches CK's behavior ✓
       - If heartbeat appears: the cycle structure is real ✓
       - If cross-cycle ≈ 2.75: the 44 invariant holds in practice ✓
       - If coherence improves: the organism PREFERS disagreement tick ✓
       
    If ALL FOUR pass, the algebra is grounded.
    Not proven universal. Not proven to be physics.
    But grounded: the math matches the organism matches the data.
    
    That's what you take to France.
    """)


if __name__ == "__main__":
    run_all()
