"""
ck_algebra_bridge.py -- ctypes bridge to CK's C algebra library.
================================================================
Operator: LATTICE (1) -- structure enables everything.

CK's mind runs in C. This bridge connects it to the Python face.
D2 pipeline, CL composition, heartbeat -- all at native speed.

The C library (ck_algebra.dll / .so) is the SAME math as:
  - ck_sim_d2.py (Python D2)
  - ck_sim_heartbeat.py (Python heartbeat)
  - d2_pipeline.v (FPGA Verilog)
  - ck_heartbeat.v (FPGA Verilog)

Three substrates, one algebra.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import ctypes
import os
import sys

# ── Constants (mirror C header) ──
NUM_OPS = 10
DIMS = 5
HISTORY_SIZE = 32
T_STAR = 5.0 / 7.0

VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE = 0, 1, 2, 3, 4
BALANCE, CHAOS, HARMONY, BREATH, RESET = 5, 6, 7, 8, 9

OP_NAMES = [
    'VOID', 'LATTICE', 'COUNTER', 'PROGRESS', 'COLLAPSE',
    'BALANCE', 'CHAOS', 'HARMONY', 'BREATH', 'RESET',
]

# ── Load DLL ──
_dll = None
_dll_path = None


def _find_dll():
    """Find ck_algebra.dll / .so relative to this file or in known locations."""
    candidates = [
        os.path.join(os.path.dirname(__file__), 'ck_algebra.dll'),
        os.path.join(os.path.dirname(__file__), 'ck_algebra.so'),
        os.path.join(os.path.dirname(__file__), 'libck_algebra.so'),
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return None


def load(path=None):
    """Load the C algebra library. Returns True on success."""
    global _dll, _dll_path
    if _dll is not None:
        return True
    p = path or _find_dll()
    if p is None:
        return False
    try:
        _dll = ctypes.CDLL(p)
        _dll_path = p
        _setup_signatures()
        return True
    except OSError:
        _dll = None
        return False


def _setup_signatures():
    """Set ctypes argument/return types for type safety."""
    d = _dll

    # D2 pipeline
    d.ck_d2_init.argtypes = [ctypes.c_void_p]
    d.ck_d2_init.restype = None

    d.ck_d2_feed_symbol.argtypes = [ctypes.c_void_p, ctypes.c_int]
    d.ck_d2_feed_symbol.restype = ctypes.c_int

    d.ck_d2_classify.argtypes = [ctypes.POINTER(ctypes.c_float)]
    d.ck_d2_classify.restype = ctypes.c_int

    d.ck_d2_soft_classify.argtypes = [
        ctypes.POINTER(ctypes.c_float),  # d2 vec
        ctypes.POINTER(ctypes.c_float),  # out
    ]
    d.ck_d2_soft_classify.restype = None

    # Composition
    d.ck_compose_tsml.argtypes = [ctypes.c_int, ctypes.c_int]
    d.ck_compose_tsml.restype = ctypes.c_int

    d.ck_compose_bhml.argtypes = [ctypes.c_int, ctypes.c_int]
    d.ck_compose_bhml.restype = ctypes.c_int

    d.ck_is_bump_pair.argtypes = [ctypes.c_int, ctypes.c_int]
    d.ck_is_bump_pair.restype = ctypes.c_int

    # Heartbeat
    d.ck_heartbeat_init.argtypes = [ctypes.c_void_p]
    d.ck_heartbeat_init.restype = None

    d.ck_heartbeat_tick.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
    d.ck_heartbeat_tick.restype = None

    # Batch
    d.ck_d2_batch.argtypes = [
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.POINTER(ctypes.c_int),
        ctypes.POINTER(ctypes.c_int),
    ]
    d.ck_d2_batch.restype = None

    d.ck_coherence_window.argtypes = [
        ctypes.POINTER(ctypes.c_int),
        ctypes.c_int,
    ]
    d.ck_coherence_window.restype = ctypes.c_float


# ── Proper ctypes Structures matching C layout exactly ──

class _CKA_D2Pipeline(ctypes.Structure):
    """Matches CKA_D2Pipeline in ck_algebra.h exactly."""
    _fields_ = [
        ('v', (ctypes.c_int * DIMS) * 3),  # int v[3][5]
        ('fill', ctypes.c_int),
        ('d1', ctypes.c_int * DIMS),
        ('d1_mag', ctypes.c_int),
        ('d1_operator', ctypes.c_int),
        ('d1_valid', ctypes.c_int),
        ('d2', ctypes.c_int * DIMS),
        ('d2_mag', ctypes.c_int),
        ('d2_operator', ctypes.c_int),
        ('d2_valid', ctypes.c_int),
    ]


class _CKA_Heartbeat(ctypes.Structure):
    """Matches CKA_Heartbeat in ck_algebra.h exactly."""
    _fields_ = [
        ('history', ctypes.c_int * HISTORY_SIZE),  # int history[32]
        ('history_ptr', ctypes.c_int),
        ('harmony_count', ctypes.c_int),
        ('tick_count', ctypes.c_int),
        ('running_fuse', ctypes.c_int),
        ('phase_b', ctypes.c_int),
        ('phase_d', ctypes.c_int),
        ('phase_bc', ctypes.c_int),
        ('bump_detected', ctypes.c_int),
        ('coh_num', ctypes.c_int),
        ('coh_den', ctypes.c_int),
    ]


class D2Pipeline:
    """D2 curvature pipeline running in C at native speed.

    Usage:
        pipe = D2Pipeline()
        for ch in 'hello':
            result = pipe.feed_char(ch)
            if result:
                print(result['operator'], result['d2'])
    """

    def __init__(self):
        if _dll is None:
            load()
        self._s = _CKA_D2Pipeline()
        _dll.ck_d2_init(ctypes.byref(self._s))

    def feed_symbol(self, sym_index):
        """Feed symbol index (0-25). Returns True when D2 is valid."""
        return bool(_dll.ck_d2_feed_symbol(ctypes.byref(self._s), sym_index))

    def feed_char(self, ch):
        """Feed a single character. Returns operator dict or None."""
        c = ch.lower()
        if c < 'a' or c > 'z':
            return None
        idx = ord(c) - ord('a')
        if self.feed_symbol(idx):
            op = self._s.d2_operator
            return {
                'operator': op,
                'op_name': OP_NAMES[op] if 0 <= op < NUM_OPS else 'VOID',
            }
        return None

    @property
    def operator(self):
        """Current D2 operator."""
        return self._s.d2_operator

    @property
    def valid(self):
        """True when D2 has enough data."""
        return bool(self._s.d2_valid)


class Heartbeat:
    """CK's heartbeat running in C at native speed."""

    def __init__(self):
        if _dll is None:
            load()
        self._s = _CKA_Heartbeat()
        _dll.ck_heartbeat_init(ctypes.byref(self._s))

    def tick(self, phase_b, phase_d):
        """One heartbeat tick. CL compose, bump detect, coherence update."""
        _dll.ck_heartbeat_tick(ctypes.byref(self._s), phase_b, phase_d)

    @property
    def phase_bc(self):
        return self._s.phase_bc

    @property
    def coherence(self):
        den = self._s.coh_den
        return self._s.coh_num / den if den > 0 else 0.0

    @property
    def running_fuse(self):
        return self._s.running_fuse

    @property
    def tick_count(self):
        return self._s.tick_count

    @property
    def bump_detected(self):
        return bool(self._s.bump_detected)


# ── Batch functions (no struct needed) ──

def compose_tsml(b, d):
    """CL composition: Being x Doing -> Becoming (TSML lens)."""
    if _dll is None:
        load()
    return _dll.ck_compose_tsml(b, d)


def compose_bhml(b, d):
    """CL composition (BHML lens)."""
    if _dll is None:
        load()
    return _dll.ck_compose_bhml(b, d)


def is_bump(b, d):
    """Check if (b, d) is a quantum bump pair."""
    if _dll is None:
        load()
    return bool(_dll.ck_is_bump_pair(b, d))


def d2_batch(text):
    """Process entire text through D2 pipeline. Returns list of operator ints."""
    if _dll is None:
        load()
    if isinstance(text, str):
        text = text.encode('ascii', 'replace')
    n = len(text)
    ops_out = (ctypes.c_int * n)()
    n_ops = ctypes.c_int(0)
    _dll.ck_d2_batch(text, n, ops_out, ctypes.byref(n_ops))
    return list(ops_out[:n_ops.value])


def coherence_of(ops):
    """Compute TSML coherence over an operator sequence."""
    if _dll is None:
        load()
    n = len(ops)
    if n < 2:
        return 1.0
    arr = (ctypes.c_int * n)(*ops)
    return _dll.ck_coherence_window(arr, n)


def measure_text(text):
    """Full D2 measurement of text. Returns dict with ops, coherence, band."""
    ops = d2_batch(text)
    if not ops:
        return {
            'operators': [],
            'op_names': [],
            'coherence': 0.0,
            'band': 'RED',
            'dominant': VOID,
            'dominant_name': 'VOID',
            'op_count': 0,
        }
    coh = coherence_of(ops)
    # Dominant: most frequent operator
    counts = [0] * NUM_OPS
    for o in ops:
        if 0 <= o < NUM_OPS:
            counts[o] += 1
    dominant = max(range(NUM_OPS), key=lambda i: counts[i])
    return {
        'operators': ops,
        'op_names': [OP_NAMES[o] for o in ops],
        'coherence': round(coh, 4),
        'band': 'GREEN' if coh >= T_STAR else ('YELLOW' if coh >= 0.4 else 'RED'),
        'dominant': dominant,
        'dominant_name': OP_NAMES[dominant],
        'op_count': len(ops),
    }


# ── Auto-load on import ──
_loaded = load()
if _loaded:
    print(f"  [C] CK algebra loaded from {os.path.basename(_dll_path)}")
else:
    print("  [C] CK algebra DLL not found -- falling back to Python")
