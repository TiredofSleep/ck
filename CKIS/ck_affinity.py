"""
ck_affinity.py — CK Hardware Affinity & OS Coherence
══════════════════════════════════════════════════════
Maps the 6 degrees of freedom onto CPU cores, process priority,
and OS scheduler hints. Hardware becomes coherent when each
process runs on cores aligned to its operator state.

AFFINITY LAW:
  Each freedom maps to a core-class:
    LATTICE   (1) → P-cores (performance) — building is expensive
    COUNTER   (2) → E-cores (efficiency)  — measuring is cheap
    COLLAPSE  (4) → isolated cores        — breaking needs no interruption
    BREATH    (8) → any core, nice=-5     — flow should be responsive
    PROGRESS  (3) → P-cores, RT-class     — acting needs priority
    RESET     (9) → background            — restart is low priority

COMPRESSION LAW:
  Chain entropy = -Σ p(op)*log2(p(op)) over operators in chain.
  If entropy < 0.5 bits AND harmony_fraction > 0.9: chain is void.
  Prune it. The information was already captured by the bump signature.

(c) 2026 Brayden Sanders / 7Site LLC — TIG Unified Theory
"""

import os
import sys
import time
import math
import json
import subprocess
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Set
from collections import Counter

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

# ── Import CK core ──────────────────────────────────────────
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ck_being import (
    CL, fuse, T_STAR, OP,
    VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET,
    BUMP_PAIRS,
)
OP_NAMES = OP  # backward compat alias


# ═══════════════════════════════════════════════════════════
# §1  OPERATOR → HARDWARE AFFINITY MAP
# ═══════════════════════════════════════════════════════════

@dataclass
class CoreClass:
    """Classification of available CPU cores."""
    performance: List[int] = field(default_factory=list)   # P-cores or fast
    efficiency:  List[int] = field(default_factory=list)   # E-cores or hyperthreads
    all_cores:   List[int] = field(default_factory=list)


def detect_core_classes() -> CoreClass:
    """
    Detect P-cores vs E-cores if available.
    Falls back to even/odd split on hyperthreaded systems.
    """
    cc = CoreClass()
    if not HAS_PSUTIL:
        # Blind fallback
        cpu_count = os.cpu_count() or 2
        cc.all_cores = list(range(cpu_count))
        # Split: first half = performance, second = efficiency
        mid = max(1, cpu_count // 2)
        cc.performance = list(range(mid))
        cc.efficiency = list(range(mid, cpu_count))
        return cc

    cpu_count = psutil.cpu_count(logical=True)
    physical = psutil.cpu_count(logical=False) or cpu_count
    cc.all_cores = list(range(cpu_count))

    if cpu_count > physical:
        # Hyperthreading: physical cores = performance, HT pairs = efficiency
        cc.performance = list(range(0, cpu_count, 2))   # even = physical
        cc.efficiency  = list(range(1, cpu_count, 2))   # odd  = HT
    else:
        # No HT: split by half
        mid = max(1, physical // 2)
        cc.performance = list(range(mid))
        cc.efficiency  = list(range(mid, physical))

    return cc


def operator_to_affinity(op: int, core_class: CoreClass) -> List[int]:
    """
    Map a TIG operator to CPU cores via LATTICE COMPOSITION.

    NOT a flat lookup table. CK composes the cell's operator with
    each core's positional operator through CL[cell][core].

    Each core has a position: core_index mod 10 = core_operator.
    The composition CL[cell_op][core_op] tells CK:
      = HARMONY(7) → cell RESONATES on this core. Include it.
      = BUMP pair   → cell will JITTER on this core. Avoid it.
      = VOID(0)     → cell is absorbed. Low priority, include only if needed.
      = anything else → neutral. Include but don't prefer.

    This gives CK a 10×10 TOPOLOGY over the cores, not a flat map.
    A PROGRESS(3) cell doesn't just go to "P-cores" — it goes to
    cores where CL[3][core_op] = 7 (harmony). On a 32-core machine
    that's not a binary split — it's a LATTICE-shaped wavefront.

    The composition IS the affinity. The table decides.
    """
    all_c = core_class.all_cores
    if not all_c:
        return [0]

    n_cores = len(all_c)
    p_set = set(core_class.performance)
    e_set = set(core_class.efficiency)

    # Score each core by its composition with the cell's operator
    # CL[cell_op][core_op] → result operator → score
    scored_cores = []
    for core in all_c:
        # Core's positional operator: modular position in the 10-operator ring
        core_op = core % 10

        # Compose: what happens when this cell meets this core?
        composition = CL[op][core_op]

        # Score the composition
        score = 0.0

        # HARMONY compositions = resonance = best placement
        if composition == HARMONY:
            score += 3.0

        # BUMP pairs = jitter source = worst placement
        elif (min(op, core_op), max(op, core_op)) in BUMP_PAIRS:
            score -= 5.0  # strongly avoid

        # VOID = absorption = low value
        elif composition == VOID:
            score -= 1.0

        # Everything else = neutral
        else:
            score += 1.0

        # Hardware bonus: P-cores get a boost for non-background work
        # E-cores get a boost for background work
        # This is the hardware topology composing with the lattice topology
        if core in p_set:
            if op in (PROGRESS, LATTICE, COLLAPSE, BREATH):
                score += 1.5   # high-value ops prefer fast cores
            else:
                score += 0.5
        elif core in e_set:
            if op in (VOID, RESET, CHAOS, COUNTER):
                score += 1.5   # background ops prefer efficient cores
            else:
                score += 0.5

        scored_cores.append((core, score))

    # Sort by score descending — best resonance first
    scored_cores.sort(key=lambda x: -x[1])

    # Select cores: take the resonant ones (score > 0)
    # But always give at least 2 cores (can't starve a process)
    # and at most N/2 cores (don't monopolize)
    resonant = [c for c, s in scored_cores if s > 0]
    min_cores = max(2, n_cores // 8)     # at least 12.5% of cores
    max_cores = max(4, n_cores * 3 // 4) # at most 75% of cores

    if len(resonant) < min_cores:
        # Not enough resonant cores — take top N by score
        selected = [c for c, _ in scored_cores[:min_cores]]
    elif len(resonant) > max_cores:
        # Too many — take the top max_cores
        selected = resonant[:max_cores]
    else:
        selected = resonant

    return sorted(selected)


def operator_to_nice(op: int) -> int:
    """
    Map a TIG operator to Unix nice value (-20=highest, 19=lowest).
    PROGRESS needs to act fast. RESET can wait.
    """
    return {
        PROGRESS: -10,   # ACT: high priority
        COLLAPSE: -5,    # BREAK: needs clean execution
        BREATH:   -5,    # FLOW: responsive
        LATTICE:  0,     # STRUCTURE: normal
        COUNTER:  5,     # MEASURE: background-ish
        HARMONY:  0,     # harmonized: normal
        BALANCE:  0,     # balanced: normal
        VOID:     15,    # absent: almost idle
        RESET:    10,    # restart: low priority
        CHAOS:    10,    # chaos: low priority
    }.get(op, 0)


# ═══════════════════════════════════════════════════════════
# §2  COHERENCE-GATED AFFINITY SETTER
# ═══════════════════════════════════════════════════════════

class AffinityController:
    """
    Sets process CPU affinity and priority based on TIG operator state.
    All changes are coherence-gated: C must be >= T* to apply.
    """

    def __init__(self, body_C: float = 1.0):
        self.core_class = detect_core_classes()
        self.body_C = body_C
        self.current_op = HARMONY
        self.history: List[Dict] = []
        self._log: List[str] = []

    def _log_event(self, msg: str):
        ts = time.strftime('%H:%M:%S')
        self._log.append(f"[{ts}] {msg}")
        if len(self._log) > 200:
            self._log = self._log[-100:]

    def set_affinity_for_operator(self, op: int, pid: Optional[int] = None,
                                   force: bool = False) -> Dict:
        """
        Apply CPU affinity and nice value for the given operator.
        Coherence-gated: skips if C < T* unless forced.
        """
        result = {
            'op': op,
            'op_name': OP_NAMES[op],
            'applied': False,
            'reason': '',
            'cores': [],
            'nice': 0,
        }

        # Coherence gate
        if not force and self.body_C < T_STAR:
            result['reason'] = f'COHERENCE GATE: C={self.body_C:.3f} < T*={T_STAR:.3f}'
            self._log_event(f"BLOCKED affinity change to {OP_NAMES[op]}: {result['reason']}")
            return result

        cores = operator_to_affinity(op, self.core_class)
        nice_val = operator_to_nice(op)
        target_pid = pid or os.getpid()

        result['cores'] = cores
        result['nice'] = nice_val

        # Apply affinity
        if HAS_PSUTIL:
            try:
                proc = psutil.Process(target_pid)
                proc.cpu_affinity(cores)
                result['applied'] = True
                result['reason'] = f'affinity set to cores {cores}'
                self._log_event(f"SET affinity pid={target_pid} op={OP_NAMES[op]} cores={cores}")
            except (psutil.AccessDenied, AttributeError) as e:
                result['reason'] = f'psutil error: {e}'
                result['applied'] = False
        else:
            # taskset fallback on Linux
            if sys.platform.startswith('linux'):
                try:
                    mask = sum(1 << c for c in cores)
                    subprocess.run(['taskset', '-p', hex(mask), str(target_pid)],
                                   capture_output=True)
                    result['applied'] = True
                    result['reason'] = f'taskset mask={hex(mask)}'
                except Exception as e:
                    result['reason'] = f'taskset error: {e}'
            else:
                result['reason'] = 'psutil not available, no fallback for this OS'

        # Apply nice (Unix only)
        if sys.platform != 'win32' and result['applied']:
            try:
                os.nice(nice_val - os.nice(0))  # adjust relative
            except PermissionError:
                pass  # nice reduction requires root — skip silently

        self.current_op = op
        self.history.append({**result, 'timestamp': time.time()})
        return result

    def walk_freedom_path(self, pids: Optional[List[int]] = None,
                          delay: float = 0.1) -> List[Dict]:
        """
        Walk the optimal bump path, setting affinity at each step.
        STRUCTURE → MEASURE → BREAK → FLOW → ACT → RESTART
        Each transition that is a bump gets full affinity change.
        """
        path = [LATTICE, COUNTER, COLLAPSE, BREATH, PROGRESS, RESET]
        results = []
        targets = pids or [os.getpid()]

        for i, op in enumerate(path):
            for pid in targets:
                r = self.set_affinity_for_operator(op, pid=pid)
                results.append(r)
            if delay > 0 and i < len(path) - 1:
                time.sleep(delay)

        return results

    def report(self) -> str:
        lines = [
            "CK AFFINITY CONTROLLER",
            f"  Body coherence: C={self.body_C:.3f} ({'GREEN' if self.body_C >= T_STAR else 'RED'})",
            f"  Current op: {OP_NAMES[self.current_op]}({self.current_op})",
            f"  P-cores: {self.core_class.performance}",
            f"  E-cores: {self.core_class.efficiency}",
            f"  Total cores: {len(self.core_class.all_cores)}",
            "",
            "  OPERATOR → CORE MAPPING:",
        ]
        for op in range(10):
            cores = operator_to_affinity(op, self.core_class)
            nice = operator_to_nice(op)
            lines.append(f"    {OP_NAMES[op]:10} → cores={cores} nice={nice:+d}")
        return '\n'.join(lines)


# ═══════════════════════════════════════════════════════════
# §3  LATTICE COMPRESSION ENGINE
# ═══════════════════════════════════════════════════════════

# BUMP_PAIRS imported from ck_being as list, convert to set for O(1) lookup
_BUMP_SET: Set[Tuple[int,int]] = set(tuple(bp) for bp in BUMP_PAIRS)

def chain_entropy(chain_ops: List[int]) -> float:
    """Shannon entropy of operator distribution in a chain."""
    if not chain_ops: return 0.0
    counts = Counter(chain_ops)
    n = len(chain_ops)
    return -sum((c/n)*math.log2(c/n) for c in counts.values())


def chain_harmony_fraction(chain_ops: List[int]) -> float:
    """Fraction of operators that are harmony(7)."""
    if not chain_ops: return 0.0
    return sum(1 for o in chain_ops if o == HARMONY) / len(chain_ops)


def chain_bump_count(chain_ops: List[int]) -> int:
    """Number of adjacent bump pairs in chain."""
    count = 0
    for i in range(len(chain_ops)-1):
        pair = (min(chain_ops[i], chain_ops[i+1]), max(chain_ops[i], chain_ops[i+1]))
        if pair in BUMP_PAIRS:
            count += 1
    return count


def chain_information(chain_ops: List[int]) -> float:
    """Total information content (bits) from bump cells."""
    BUMP_INFO = math.log2(100/10)   # 3.32 bits per bump
    HARMONY_INFO = -math.log2(73/100)  # 0.45 bits per harmony
    bits = 0.0
    for i in range(len(chain_ops)-1):
        a, b = chain_ops[i], chain_ops[i+1]
        v = CL[a][b]
        if v not in [HARMONY, VOID]:
            bits += BUMP_INFO
        elif v == HARMONY:
            bits += HARMONY_INFO
    return bits


@dataclass
class CompressionDecision:
    should_prune: bool
    reason: str
    entropy: float
    harmony_frac: float
    bump_count: int
    information_bits: float
    compressed_chain: Optional[List[int]] = None


def compress_chain(chain_ops: List[int],
                   entropy_threshold: float = 0.5,
                   harmony_threshold: float = 0.9,
                   min_bumps: int = 1) -> CompressionDecision:
    """
    COMPRESSION LAW:
    A chain should be pruned if:
      1. Its Shannon entropy < entropy_threshold (0.5 bits default)
         — almost all operators are the same → redundant
      2. Its harmony fraction > harmony_threshold (0.9 default)
         — 90%+ harmony → gravity has fully absorbed signal
      3. It contains < min_bumps adjacent bump pairs
         — no bumps = no information = pure background noise
    
    If compressible, returns a compressed version that retains only
    the bump-containing subsequences.
    """
    if not chain_ops:
        return CompressionDecision(True, "empty chain", 0, 0, 0, 0, [])

    entropy = chain_entropy(chain_ops)
    hfrac   = chain_harmony_fraction(chain_ops)
    bumps   = chain_bump_count(chain_ops)
    info    = chain_information(chain_ops)

    # Hard prune: all harmony
    if all(o == HARMONY for o in chain_ops):
        return CompressionDecision(True, "all-harmony chain: 0 information",
                                   entropy, hfrac, 0, info, [HARMONY])

    # Soft prune: high harmony + low entropy + no bumps
    if entropy < entropy_threshold and hfrac > harmony_threshold and bumps < min_bumps:
        return CompressionDecision(
            True,
            f"low-signal: entropy={entropy:.2f}b < {entropy_threshold}b, "
            f"harmony={hfrac:.1%} > {harmony_threshold:.0%}, bumps={bumps}",
            entropy, hfrac, bumps, info, None
        )

    # Compressible: strip leading/trailing harmony runs, keep bump context
    if hfrac > 0.6 and bumps >= 1:
        compressed = _extract_bump_neighborhoods(chain_ops)
        return CompressionDecision(
            False,
            f"compressed: kept {len(compressed)}/{len(chain_ops)} ops around {bumps} bumps",
            entropy, hfrac, bumps, info, compressed
        )

    # Keep as-is
    return CompressionDecision(
        False, "information-bearing: keep",
        entropy, hfrac, bumps, info, chain_ops
    )


def _extract_bump_neighborhoods(chain_ops: List[int],
                                 window: int = 2) -> List[int]:
    """
    Extract the neighborhood of each bump pair (±window ops).
    Strips pure-harmony runs between neighborhoods.
    """
    if not chain_ops: return []
    bump_positions: Set[int] = set()
    for i in range(len(chain_ops)-1):
        pair = (min(chain_ops[i], chain_ops[i+1]),
                max(chain_ops[i], chain_ops[i+1]))
        if pair in BUMP_PAIRS:
            for j in range(max(0, i-window), min(len(chain_ops), i+window+2)):
                bump_positions.add(j)

    if not bump_positions:
        return chain_ops  # no bumps found, keep all

    result = []
    in_bump_zone = False
    for i, op in enumerate(chain_ops):
        if i in bump_positions:
            result.append(op)
            in_bump_zone = True
        elif in_bump_zone and op != HARMONY:
            result.append(op)  # non-harmony bridge
        # skip pure harmony outside bump zones

    return result or [HARMONY]  # fallback


def batch_compress(chains: List[List[int]],
                   entropy_threshold: float = 0.5,
                   harmony_threshold: float = 0.9) -> Dict:
    """
    Compress a batch of chains. Returns compression statistics.
    """
    results = {
        'total': len(chains),
        'pruned': 0,
        'compressed': 0,
        'kept': 0,
        'bits_before': 0.0,
        'bits_after': 0.0,
        'pruned_chains': [],
        'compressed_chains': [],
        'kept_chains': [],
    }

    for chain in chains:
        dec = compress_chain(chain, entropy_threshold, harmony_threshold)
        bits = chain_information(chain)
        results['bits_before'] += bits

        if dec.should_prune:
            results['pruned'] += 1
            results['pruned_chains'].append(chain)
        elif dec.compressed_chain and len(dec.compressed_chain) < len(chain):
            results['compressed'] += 1
            results['compressed_chains'].append(dec.compressed_chain)
            results['bits_after'] += chain_information(dec.compressed_chain)
        else:
            results['kept'] += 1
            results['kept_chains'].append(chain)
            results['bits_after'] += bits

    ratio = (1 - len(sum(results['compressed_chains']+results['kept_chains'],[]))
             / max(1, len(sum(chains, [])))) * 100
    results['compression_ratio_pct'] = round(ratio, 1)
    return results


# ═══════════════════════════════════════════════════════════
# §4  SELF-CODING ENGINE
# ═══════════════════════════════════════════════════════════

ALGORITHM_TEMPLATES = {
    LATTICE: """
def {name}(data):
    \"\"\"STRUCTURE: Build a lattice index from data.\"\"\"
    index = {{}}
    for item in data:
        key = hash(str(item)) % 10  # operator key
        index.setdefault(key, []).append(item)
    return index
""",
    COUNTER: """
def {name}(data, target):
    \"\"\"MEASURE: Count and compare against target.\"\"\"
    counts = {{}}
    for item in data:
        counts[item] = counts.get(item, 0) + 1
    return {{k: v for k, v in counts.items() if v >= target}}
""",
    COLLAPSE: """
def {name}(data, threshold):
    \"\"\"BREAK: Prune items below threshold.\"\"\"
    result = [item for item in data if score(item) >= threshold]
    return result
""",
    BREATH: """
def {name}(stream):
    \"\"\"FLOW: Process a stream with rhythm.\"\"\"
    for chunk in stream:
        yield process(chunk)
        # breathe — don't block
""",
    PROGRESS: """
def {name}(state, steps):
    \"\"\"ACT: Iterate forward from state.\"\"\"
    for _ in range(steps):
        state = step(state)
        if converged(state): break
    return state
""",
    RESET: """
def {name}(state, seed=None):
    \"\"\"RESTART: Return to ground state.\"\"\"
    return initialize(seed or default_seed())
""",
}

BUMP_TO_PATTERN = {
    (LATTICE, COUNTER): """
def {name}(data):
    \"\"\"BUMP: structure×measure → progress. Build then analyze.\"\"\"
    # STRUCTURE phase
    index = {{}}
    for item in data:
        key = hash(str(item)) % 10
        index.setdefault(key, []).append(item)
    # MEASURE phase → progress (motion through the index)
    results = []
    for key in sorted(index.keys()):
        bucket = index[key]
        results.append((key, len(bucket), bucket))
    return results  # = progress: the system moved forward
""",
    (COUNTER, COLLAPSE): """
def {name}(data, threshold=0.714):
    \"\"\"BUMP: counter×collapse → collapse. Measure then break.\"\"\"
    # MEASURE phase
    scored = [(item, score(item)) for item in data]
    # COLLAPSE phase → confirmed break (only the true breaks survive)
    return [item for item, s in scored if s < threshold]
""",
    (COUNTER, RESET): """
def {name}(state):
    \"\"\"BUMP: counter×reset → reset. Measure then restart.\"\"\"
    # MEASURE current state
    entropy = measure_entropy(state)
    # RESET if entropy too high → confirmed restart
    if entropy > T_STAR:
        return initialize()
    return state  # coherent, no restart needed
""",
    (PROGRESS, RESET): """
def {name}(state, steps):
    \"\"\"BUMP: progress×reset → progress. Act sustains itself.\"\"\"
    for i in range(steps):
        state = step(state)
        # RESET if incoherent, but continue progressing
        if not coherent(state):
            state = partial_reset(state)
        # progress bump: the reset RESTARTS the progress cycle
    return state
""",
    (COLLAPSE, BREATH): """
def {name}(system):
    \"\"\"BUMP: collapse×breath → breath. Break creates new flow.\"\"\"
    # COLLAPSE: controlled destruction
    fragments = decompose(system)
    # BREATH: new life from the fragments
    for fragment in fragments:
        if viable(fragment):
            yield rebuild(fragment)  # breathing new structures out
""",
}


def synthesize_algorithm(bump_path: List[int], name: str = "ck_algo") -> str:
    """
    Synthesize a Python algorithm from a sequence of TIG operators.
    
    The bump graph determines the algorithm's STRUCTURE:
    - Each operator = one conceptual phase
    - Each bump transition = one meaningful transformation
    - Harmony transitions = pass-through (no code needed)
    - The fused result = the algorithm's purpose
    
    Returns: Python source code string
    """
    lines = [
        f'"""\nSynthesized by CK from bump path: '
        f'{[OP_NAMES[op] for op in bump_path]}',
        f'fuse = {OP_NAMES[fuse(bump_path)]}({fuse(bump_path)})',
        '"""',
        '',
    ]

    phases = []
    for i in range(len(bump_path)-1):
        a, b = bump_path[i], bump_path[i+1]
        pair = (min(a,b), max(a,b))
        v = CL[a][b]
        is_bump = v not in [HARMONY, VOID]

        if is_bump and pair in BUMP_TO_PATTERN:
            phases.append(('bump', pair, v, BUMP_TO_PATTERN[pair]))
        elif v not in [HARMONY, VOID]:
            # Use single-operator template for the result
            tmpl = ALGORITHM_TEMPLATES.get(v, f"\n# operator {v} ({OP_NAMES[v]}): no template\n")
            phases.append(('single', v, v, tmpl))
        # harmony transitions: skip (no code needed)

    if not phases:
        # Pure harmony path — return identity
        lines.append(f"def {name}(data):")
        lines.append(f"    '''HARMONY: input already coherent, return as-is.'''")
        lines.append(f"    return data")
    elif len(phases) == 1:
        _, key, result_op, tmpl = phases[0]
        code = tmpl.format(name=name)
        lines.append(code)
        lines.append(f"# Result operator: {OP_NAMES[result_op]}({result_op})")
    else:
        # Multi-phase: chain phases into a pipeline
        lines.append(f"def {name}(data, **kwargs):")
        lines.append(f"    '''")
        lines.append(f"    Multi-phase algorithm: {' → '.join(OP_NAMES[op] for op in bump_path)}")
        lines.append(f"    Fused result: {OP_NAMES[fuse(bump_path)]}({fuse(bump_path)})")
        lines.append(f"    '''")

        for i, (kind, key, result_op, tmpl) in enumerate(phases):
            phase_name = f"phase_{i+1}_{OP_NAMES[result_op]}"
            # Extract the body of the template
            tmpl_lines = [l for l in tmpl.format(name=phase_name).split('\n')
                          if l.strip() and not l.startswith('def ')]
            lines.append(f"    # --- Phase {i+1}: {OP_NAMES[result_op]} ---")
            lines.append(f"    # (bump pair → {OP_NAMES[result_op]})" if kind=='bump' else f"    # ({OP_NAMES[result_op]})")
            for l in tmpl_lines[:3]:  # abbreviated inline
                lines.append(f"    {l.strip()}")

        lines.append(f"    return data  # fused: {OP_NAMES[fuse(bump_path)]}({fuse(bump_path)})")

    return '\n'.join(lines)


# ═══════════════════════════════════════════════════════════
# §4b  ALGORITHM LATTICE — learned patterns from code self-eating
#
# The algorithm lattice is a persistent mapping:
#   operator_chain_signature → list of code templates
#
# When CK eats his own code (ck_code_digest.py), every method
# becomes a training pair: (operator_chain, source_code).
# These pairs densify the lattice. When CK needs to synthesize
# a new algorithm, he first checks the lattice for a matching
# pattern, then composes from similar patterns, then falls
# back to the hardcoded templates.
#
# The denser the lattice, the more algorithms CK can synthesize
# from novel operator chains. This IS the future of AI:
# not neural nets, not token prediction — lattices of algorithms
# that compose through CL to produce fresh combinations.
# ═══════════════════════════════════════════════════════════

_ALGO_LATTICE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'ck_store', 'algorithm_lattice.json'
)

# In-memory lattice: chain_signature → [{code, source_module, fuse, shape}]
_algorithm_lattice = {}
_algo_lattice_loaded = False


def _chain_sig(chain: List[int]) -> str:
    """Convert operator chain to a hashable signature string."""
    return ','.join(str(op) for op in chain[:20])


def _load_algorithm_lattice():
    """Load persisted algorithm lattice."""
    global _algorithm_lattice, _algo_lattice_loaded
    if _algo_lattice_loaded:
        return
    try:
        if os.path.exists(_ALGO_LATTICE_PATH):
            with open(_ALGO_LATTICE_PATH, 'r') as f:
                _algorithm_lattice = json.load(f)
    except Exception:
        _algorithm_lattice = {}
    _algo_lattice_loaded = True


def save_algorithm_lattice():
    """Persist the algorithm lattice."""
    try:
        os.makedirs(os.path.dirname(_ALGO_LATTICE_PATH), exist_ok=True)
        with open(_ALGO_LATTICE_PATH, 'w') as f:
            json.dump(_algorithm_lattice, f)
    except Exception:
        pass


def learn_algorithm(chain: List[int], code: str, source_module: str = 'unknown'):
    """
    Store a new algorithm pattern in the lattice.

    chain: the operator chain (from AST parsing or manual)
    code: the Python source code that implements this pattern
    source_module: where it came from

    The lattice maps chain signatures to lists of code templates.
    Multiple implementations of the same chain = richer composition.
    """
    _load_algorithm_lattice()

    sig = _chain_sig(chain)
    if sig not in _algorithm_lattice:
        _algorithm_lattice[sig] = []

    # Don't store duplicates
    existing_codes = [e.get('code', '')[:100] for e in _algorithm_lattice[sig]]
    if code[:100] in existing_codes:
        return

    # Cap per-signature to prevent explosion
    if len(_algorithm_lattice[sig]) >= 10:
        return

    _algorithm_lattice[sig].append({
        'code': code[:5000],  # cap size
        'source': source_module,
        'fuse': fuse(chain) if len(chain) >= 2 else 5,
        'chain_len': len(chain),
    })


def learn_from_digest(digest_result: dict):
    """
    Learn algorithm patterns from code digest training pairs.
    Called after ck_code_digest.digest_all().
    """
    pairs_learned = 0
    for module_name, file_data in digest_result.get('files', {}).items():
        for chain, source in file_data.get('training_pairs', []):
            if len(chain) >= 3 and len(source) > 20:
                learn_algorithm(chain, source, source_module=module_name)
                pairs_learned += 1
    save_algorithm_lattice()
    return pairs_learned


def find_similar_algorithm(chain: List[int], max_results: int = 3) -> List[dict]:
    """
    Find algorithms in the lattice with similar operator chains.

    Similarity: fuse match + chain length proximity + shared operators.
    Returns up to max_results matches, best first.
    """
    _load_algorithm_lattice()
    if not _algorithm_lattice:
        return []

    target_fuse = fuse(chain) if len(chain) >= 2 else 5
    target_set = set(chain)
    results = []

    for sig, entries in _algorithm_lattice.items():
        sig_ops = [int(x) for x in sig.split(',') if x.isdigit()]
        if not sig_ops:
            continue

        sig_fuse = fuse(sig_ops) if len(sig_ops) >= 2 else 5

        # Score: fuse match (50%) + operator overlap (30%) + length proximity (20%)
        fuse_score = 1.0 if sig_fuse == target_fuse else 0.0
        sig_set = set(sig_ops)
        overlap = len(target_set & sig_set) / max(len(target_set | sig_set), 1)
        len_ratio = 1.0 - abs(len(sig_ops) - len(chain)) / max(len(sig_ops), len(chain), 1)

        score = fuse_score * 0.5 + overlap * 0.3 + len_ratio * 0.2

        if score > 0.3:
            for entry in entries:
                results.append({
                    'score': round(score, 3),
                    'chain': sig_ops,
                    'code': entry['code'],
                    'source': entry.get('source', 'unknown'),
                    'fuse': sig_fuse,
                })

    results.sort(key=lambda x: -x['score'])
    return results[:max_results]


def synthesize_from_prompt(task_description: str, name: str = "ck_algo") -> str:
    """
    Full pipeline: task description → operator chain → algorithm synthesis.

    1. Classify task to operator
    2. Build operator chain from task keywords
    3. Check algorithm lattice for similar patterns
    4. Synthesize from best match or templates
    """
    # Classify main operator
    main_op = classify_task(task_description)

    # Build a richer chain from multiple keywords
    text_lower = task_description.lower()
    chain = [main_op]
    for op, keywords in TASK_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower and op != main_op:
                chain.append(op)
                break

    if len(chain) < 2:
        chain.append(PROGRESS)  # default: do something

    # Check lattice for similar patterns
    similar = find_similar_algorithm(chain)
    if similar and similar[0]['score'] > 0.6:
        best = similar[0]
        header = (
            f'"""\n'
            f'Synthesized by CK from task: "{task_description}"\n'
            f'Based on learned pattern from: {best["source"]}\n'
            f'Similarity: {best["score"]}\n'
            f'Chain: {[OP_NAMES[op] for op in best["chain"]]}\n'
            f'"""\n\n'
        )
        return header + best['code']

    # Fall back to template synthesis
    return synthesize_algorithm(chain, name=name)


def algorithm_lattice_stats() -> dict:
    """Return statistics about the algorithm lattice."""
    _load_algorithm_lattice()
    total_patterns = sum(len(v) for v in _algorithm_lattice.values())
    unique_sigs = len(_algorithm_lattice)
    return {
        'unique_signatures': unique_sigs,
        'total_patterns': total_patterns,
        'avg_per_sig': round(total_patterns / max(unique_sigs, 1), 1),
    }


# ═══════════════════════════════════════════════════════════
# §5  COHERENCE ROUTING — map any task to its operator
# ═══════════════════════════════════════════════════════════

TASK_KEYWORDS = {
    LATTICE:  ['build','create','index','structure','organize','spawn','generate'],
    COUNTER:  ['count','measure','analyze','compare','score','check','verify','test'],
    COLLAPSE: ['prune','delete','clean','fix','error','break','remove','filter'],
    BREATH:   ['stream','flow','sense','listen','read','watch','monitor','receive'],
    PROGRESS: ['run','execute','act','iterate','train','process','apply','move'],
    RESET:    ['restart','reset','reinitialize','recover','restore','seed','init'],
    HARMONY:  ['harmonize','align','agree','confirm','settle','converge'],
    VOID:     ['void','null','empty','none','clear','drop'],
}

def classify_task(text: str) -> int:
    """Map a task description to its TIG operator via keyword matching."""
    text_lower = text.lower()
    scores = {op: 0 for op in range(10)}
    for op, keywords in TASK_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                scores[op] += 1
    best = max(scores, key=lambda o: scores[o])
    return best if scores[best] > 0 else HARMONY


def route_to_hardware(task: str, controller: AffinityController,
                      pid: Optional[int] = None) -> Dict:
    """
    Given a task description, classify it to an operator and
    set hardware affinity accordingly.
    """
    op = classify_task(task)
    result = controller.set_affinity_for_operator(op, pid=pid)
    result['task_classification'] = f"{OP_NAMES[op]}({op})"
    return result


# ═══════════════════════════════════════════════════════════
# §6  SELF-TEST
# ═══════════════════════════════════════════════════════════

def self_test():
    print("CK AFFINITY — SELF TEST")
    print("=" * 50)

    # Test core detection
    cc = detect_core_classes()
    print(f"Cores detected: P={cc.performance} E={cc.efficiency}")

    # Test affinity controller
    ac = AffinityController(body_C=0.8)
    print("\n" + ac.report())

    # Test freedom path walk (no actual affinity change in test)
    print("\nFREEDOM PATH (dry run):")
    path = [1,2,4,8,3,9]
    for i in range(len(path)-1):
        a, b = path[i], path[i+1]
        v = CL[a][b]
        is_bump = v not in [HARMONY, VOID]
        cores = operator_to_affinity(b, cc)
        nice = operator_to_nice(b)
        print(f"  {OP_NAMES[a]}→{OP_NAMES[b]} = {OP_NAMES[v]} "
              f"{'←BUMP' if is_bump else '      '} | cores={cores} nice={nice:+d}")

    # Test compression
    print("\nCOMPRESSION TESTS:")
    test_chains = [
        ([7,7,7,7,7,7,7,7],        "all harmony"),
        ([1,2,3,7,7,7,7,7],        "bump at start, harmony tail"),
        ([7,7,1,2,4,8,7,7,3,9,7],  "bumps in middle"),
        ([1,2,3,4,5,6,7,8,9,0],    "all operators"),
    ]
    for chain, label in test_chains:
        dec = compress_chain(chain)
        print(f"  {label}: prune={dec.should_prune} bumps={dec.bump_count} "
              f"entropy={dec.entropy:.2f}b → {dec.reason[:50]}")

    # Test algorithm synthesis
    print("\nALGORITHM SYNTHESIS:")
    code = synthesize_algorithm([LATTICE, COUNTER], name="index_and_measure")
    print(code[:300])

    # Test task routing
    print("\nTASK ROUTING:")
    tasks = ["build a new index", "measure coherence", "fix the error",
             "stream data", "run the training", "reset to baseline"]
    for task in tasks:
        op = classify_task(task)
        print(f"  '{task}' → {OP_NAMES[op]}({op})")

    print("\n✓ Self-test complete")


if __name__ == "__main__":
    self_test()
