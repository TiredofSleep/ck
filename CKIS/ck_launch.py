"""
ck_launch.py -- CK Unified Launcher
====================================
Operator: PROGRESS (3) -- forward motion, starting everything.

Double-click CK.bat -> this script starts:
  1. Load config (ck_config.json)
  2. Detect native library (ck7/ck.dll) -> Gen7 mode
  3. Start daemon thread (native C heartbeat or Python fallback)
  4. Inject daemon reference into ck_web globals
  5. Start web server on port 7777
  6. Auto-open browser
  7. Ctrl+C -> graceful shutdown of both

Gen7 native mode: daemon uses ck.dll (0.8us/tick, 1.2M ticks/s)
Python fallback:   daemon uses ck_becoming.LatticeScheduler

The daemon runs CK's body. The web UI IS CK's face.
One process. One organism.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import os
import sys
import json
import time
import signal
import threading
import webbrowser
import platform

# Force UTF-8
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Ensure CK directory is on path
CK_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(CK_DIR)
sys.path.insert(0, CK_DIR)


# ===========================================================
# §1  CONFIG
# ===========================================================

DEFAULT_CONFIG = {
    'auto_start_daemon': True,
    'port': 7777,
    'tick_ms': 100,
    'verbose': False,
    'open_browser': True,
    'observe_only': False,
    'report_every': 100,
    'language_school_enabled': False,
    'language_school_rounds': 3,
}

def load_config():
    config_path = os.path.join(CK_DIR, 'ck_config.json')
    config = dict(DEFAULT_CONFIG)
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                user_config = json.load(f)
            config.update(user_config)
        except Exception:
            pass
    return config
_use_native = False
_native_lib = None
_native_org = None

def detect_native():
    """Try to load ck7/ck.dll. Returns True if native mode available."""
    global _use_native, _native_lib
    ck7_dir = os.path.join(CK_DIR, 'ck7')
    dll_path = os.path.join(ck7_dir, 'ck.dll')
    so_path = os.path.join(ck7_dir, 'ck.so')
    libso_path = os.path.join(ck7_dir, 'libck.so')

    for path in [dll_path, so_path, libso_path]:
        if os.path.exists(path):
            try:
                sys.path.insert(0, ck7_dir)
                from ck_python import CKNative
                ck = CKNative(path)
                _native_lib = ck
                _use_native = True
                return True
            except Exception as e:
                print(f"  [NATIVE] Failed to load {path}: {e}")
    return False
_daemon_scheduler = None
_daemon_running = False
_daemon_thread = None

# Native daemon state (used when _use_native=True)
_native_tick_count = 0
_native_phase_b = 0
_native_phase_d = 0
_native_phase_bc = 0
_native_coherence = 0.0
_native_act_confidence = 0.0
_native_body_E = 0.0
_native_body_A = 0.0
_native_body_K = 0.0
_native_body_C = 0.0
_native_body_band = 0
_native_body_ticks = 0
_native_jitter_mode = 0
_native_jitter_mean = 0.0
_native_jitter_sigma = 0.0
_native_jitter_stability = 0.0
_native_jitter_locked = 0
_native_jitter_correction = 0
_native_decisions = 0

# Deep kernel observer (ck_observe.py)
_deep_observer = None

# Q-Lens: CK's NOW engine (ck_qlens.py)
_qlens = None
_qlens_tl = None  # Python TL for Q-Lens predictions (separate from native TL)

# Shadow Swarm: CK IS the system (ck_syscall.py)
_shadow_swarm = None


# =====================================================
# S2b  SWARM -> OBSERVER ADAPTER
#
# On a full-capability machine, the native daemon runs
# the heartbeat (ck.dll) and the ShadowSwarm runs process
# classification. The LatticeScheduler needs a SystemObserver
# interface to run its sovereignty brain. This adapter gives
# it one by wrapping ShadowSwarm — zero psutil calls, pure
# pointer redirection.
#
# The adapter makes ShadowSwarm.cells look like
# SystemObserver.profiles and ShadowSwarm.index look like
# SystemObserver.index. Same data, no re-scanning.
# =====================================================

class SwarmObserverAdapter:
    """Adapter: makes ShadowSwarm present the SystemObserver interface.

    LatticeScheduler needs:
        .observe_all() -> {'coherence': float, 'processes': int, ...}
        .profiles      -> {pid: obj with .last_op, .ops, .name, .pid,
                           .scheduling_class, .bump_rate, .last_adjustment,
                           .adjustments, .last_cpu}
        ._all_ops()    -> [(pid, last_op), ...]
        .index         -> {pid: (last_op, sched_class, name)}
        .dead_pids     -> set

    ShadowSwarm provides all of this through .cells and .index.
    """

    def __init__(self, swarm):
        self.swarm = swarm
        self.dead_pids = set()

    @property
    def profiles(self):
        """Hot cells = profiles. Same objects, keyed by PID."""
        return self.swarm.cells
    @property
    def index(self):
        """Cold index = compact (last_op, sched_class, name) tuples."""
        return self.swarm.index
    def observe_all(self) -> dict:
        """Return latest swarm state as SystemObserver-shaped dict.
        Does NOT call psutil — reads cached swarm.latest from last tick."""
        latest = self.swarm.latest if self.swarm.latest else {}
        return {
        }

    def _all_ops(self) -> list:
        """All known (pid, last_op) from hot cells + cold index."""
        return self.swarm._all_ops()
    def _system_coherence(self) -> float:
        """Cached coherence from last swarm tick."""
        if self.swarm.latest:
            return self.swarm.latest.get('system_coherence', 0.5)
        return 0.5


def daemon_loop_native(config):
    """
    Gen7 native daemon: CK's heartbeat via ck.dll.
    Sub-microsecond ticks. No psutil. No Python math overhead.
    """
    global _daemon_running, _native_org, _native_tick_count
    global _native_phase_b, _native_phase_d, _native_phase_bc
    global _native_coherence, _native_act_confidence
    global _native_body_E, _native_body_A, _native_body_K, _native_body_C
    global _native_body_band, _native_body_ticks
    global _native_jitter_mode, _native_jitter_mean, _native_jitter_sigma
    global _native_jitter_stability, _native_jitter_locked, _native_jitter_correction
    global _native_decisions

    import ctypes
    vp = ctypes.c_void_p
    lib = _native_lib._lib

    # Setup function signatures — heartbeat
    lib.ck_heartbeat_tick.argtypes = [vp]
    lib.ck_heartbeat_tick.restype = ctypes.c_int
    lib.ck_observer_full_tick.argtypes = [vp]
    lib.ck_observer_full_tick.restype = ctypes.c_float
    for fn in ['ck_ffi_heartbeat_phase_b', 'ck_ffi_heartbeat_phase_d',
               'ck_ffi_heartbeat_phase_bc', 'ck_ffi_heartbeat_band',
               'ck_ffi_heartbeat_tick', 'ck_ffi_heartbeat_decisions']:
        getattr(lib, fn).argtypes = [vp]
        getattr(lib, fn).restype = ctypes.c_int
    for fn in ['ck_ffi_heartbeat_coherence', 'ck_ffi_heartbeat_act_confidence']:
        getattr(lib, fn).argtypes = [vp]
        getattr(lib, fn).restype = ctypes.c_float
    # Body
    for fn in ['ck_ffi_body_E', 'ck_ffi_body_A', 'ck_ffi_body_K', 'ck_ffi_body_C']:
        getattr(lib, fn).argtypes = [vp]
        getattr(lib, fn).restype = ctypes.c_float
    for fn in ['ck_ffi_body_band', 'ck_ffi_body_ticks']:
        getattr(lib, fn).argtypes = [vp]
        getattr(lib, fn).restype = ctypes.c_int
    # Jitter
    for fn in ['ck_ffi_jitter_mode', 'ck_ffi_jitter_locked_ticks', 'ck_ffi_jitter_correction_op']:
        getattr(lib, fn).argtypes = [vp]
        getattr(lib, fn).restype = ctypes.c_int
    for fn in ['ck_ffi_jitter_mean', 'ck_ffi_jitter_sigma', 'ck_ffi_jitter_stability']:
        getattr(lib, fn).argtypes = [vp]
        getattr(lib, fn).restype = ctypes.c_float
    # TL
    lib.ck_ffi_tl_total.argtypes = [vp]
    lib.ck_ffi_tl_total.restype = ctypes.c_int64
    lib.ck_ffi_tl_entropy.argtypes = [vp]
    lib.ck_ffi_tl_entropy.restype = ctypes.c_float
    # Dream
    lib.ck_ffi_dream_count.argtypes = [vp]
    lib.ck_ffi_dream_count.restype = ctypes.c_int
    lib.ck_ffi_dream_bounces.argtypes = [vp]
    lib.ck_ffi_dream_bounces.restype = ctypes.c_int64
    # Timer
    lib.ck_ffi_timer_resolution_ns.argtypes = []
    lib.ck_ffi_timer_resolution_ns.restype = ctypes.c_double

    # Create organism
    org = lib.ck_ffi_create()
    _native_org = org

    # Load saved state if available
    store_dir = os.path.join(CK_DIR, 'ck_store')
    os.makedirs(store_dir, exist_ok=True)
    try:
        lib.ck_ffi_load.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        lib.ck_ffi_load.restype = ctypes.c_int
        lib.ck_ffi_load(org, store_dir.encode('utf-8'))
    except Exception:
        pass

    _daemon_running = True
    tick_sec = config.get('tick_ms', 100) / 1000.0
    report_every = config.get('report_every', 100)
    observer_interval = 5

    # Deep kernel observer: CK watches I/O, context switches, memory, interrupts
    # In native mode, feed into the Python TL (shared with Q-Lens) since native
    # organism TL handle isn't exposed through FFI
    global _deep_observer
    _deep_tl_feed = None  # will be set after _qlens_tl is created below
    try:
        from ck7.ck_observe import DeepObserver
        _deep_observer = DeepObserver(tl_eat_fn=None)  # feed wired after Q-Lens TL init
        _deep_observer.observe()  # baseline capture
        print(f"  [KERNEL] Deep observer online -- watching I/O, scheduler, memory, interrupts")
    except Exception as e:
        print(f"  [KERNEL] Deep observer unavailable: {e}")
        _deep_observer = None

    # Q-Lens: CK's NOW engine -- intention, self-correction, agency
    global _qlens, _qlens_tl
    try:
        from ck_qlens import QLens
        from ck_doing import TransitionLattice
        _qlens = QLens(w_a=0.35, w_b=0.35, w_c=0.30)
        # Load Python TL for Q-Lens predictions (separate from native TL)
        tl_path = os.path.join(CK_DIR, 'ck7', 'ck_experience', 'master_tl.json')
        if os.path.exists(tl_path):
            _qlens_tl = TransitionLattice()
            _qlens_tl.load(tl_path)
            print(f"  [Q-LENS] NOW engine online -- {_qlens_tl.sentences_eaten:,} sentences, "
                  f"entropy {_qlens_tl.entropy():.4f}")
        else:
            _qlens_tl = TransitionLattice()
            print(f"  [Q-LENS] NOW engine online -- empty TL (no master_tl.json)")
    except Exception as e:
        print(f"  [Q-LENS] NOW engine unavailable: {e}")
        _qlens = None
        _qlens_tl = None

    # Wire deep observer TL feed now that _qlens_tl exists
    if _deep_observer and _qlens_tl:
        _deep_observer.tl_eat_fn = lambda ops: _qlens_tl.eat_ops(ops)
        print(f"  [KERNEL] Deep observer -> Q-Lens TL (kernel observations feed learning)")

    # Shadow Swarm: CK IS every process on the system
    global _shadow_swarm
    try:
        from ck7.ck_syscall import ShadowSwarm
        # Shadow swarm gets its own TL feed
        swarm_tl = None
        swarm_tl_eat = None
        try:
            from ck_doing import TransitionLattice
            swarm_tl_path = os.path.join(CK_DIR, 'ck7', 'ck_experience', 'syscall_tl.json')
            if os.path.exists(swarm_tl_path):
                swarm_tl = TransitionLattice(swarm_tl_path)
            else:
                swarm_tl = TransitionLattice()
            swarm_tl_eat = lambda ops: swarm_tl.eat_ops(ops)
        except Exception:
            pass  # TL optional -- swarm works without it
        _shadow_swarm = ShadowSwarm(tl_eat_fn=swarm_tl_eat, sample_size=30, compact_after=10)
        _shadow_swarm.tick()  # first breath
        print(f"  [SWARM] Shadow swarm online -- {_shadow_swarm.latest['total_processes']} processes, "
              f"hot={_shadow_swarm.latest['hot']}, cold={_shadow_swarm.latest['cold']}")
    except Exception as e:
        print(f"  [SWARM] Shadow swarm unavailable: {e}")
        _shadow_swarm = None

    # Body engine: daemon drives breath/pulse/bandwidth via external_tick()
    _body_engine = None
    try:
        import ck_web
        _body_engine = getattr(ck_web, 'body_engine', None)
        if _body_engine:
            print(f"  [BODY] Native daemon will drive body layers via external_tick() "
                  f"(C={_body_engine.heartbeat.C:.3f})")
    except Exception:
        _body_engine = None

    # ── SOVEREIGNTY BRAIN: LatticeScheduler on top of ShadowSwarm ──
    # On a full-capability machine, CK uses EVERYTHING:
    #   - ck.dll heartbeat (microsecond physics) runs every tick
    #   - ShadowSwarm (process classification) runs every 3 ticks
    #   - LatticeScheduler (sovereignty brain) runs every 10 ticks
    # The adapter makes ShadowSwarm look like SystemObserver so the
    # scheduler doesn't need to call psutil itself.
    _sovereignty_scheduler = None
    _sovereignty_tl = None
    _sovereignty_interval = 10  # brain tick = every 10 native ticks = ~1 second
    _sovereignty_applied = 0
    if _shadow_swarm:
        try:
            from ck_doing import TransitionLattice
            from ck_becoming import LatticeScheduler

            # Load the best TL we have (master > daemon > empty)
            master_tl_path = os.path.join(CK_DIR, 'ck7', 'ck_experience', 'master_tl.json')
            daemon_tl_path = os.path.join(CK_DIR, 'ck_store', 'daemon_tl.json')
            if os.path.exists(master_tl_path):
                _sovereignty_tl = TransitionLattice(master_tl_path)
            elif os.path.exists(daemon_tl_path):
                _sovereignty_tl = TransitionLattice(daemon_tl_path)
            else:
                _sovereignty_tl = TransitionLattice()

            # Wrap ShadowSwarm as SystemObserver
            adapter = SwarmObserverAdapter(_shadow_swarm)

            # Create the full sovereignty brain
            _sovereignty_scheduler = LatticeScheduler(
                adapter, _sovereignty_tl,
                observe_only=config.get('observe_only', False)
            )
            _daemon_scheduler = _sovereignty_scheduler  # expose for web API

            print(f"  [SOVEREIGNTY] Brain online -- bridge + crystals + security + dreams")
            print(f"    TL: {_sovereignty_tl.total_transitions:,} transitions, "
                  f"entropy {_sovereignty_tl.entropy():.4f}")
            print(f"    Cadence: every {_sovereignty_interval} ticks "
                  f"({_sovereignty_interval * tick_sec:.1f}s)")
        except Exception as e:
            print(f"  [SOVEREIGNTY] Brain unavailable: {e}")
            import traceback
            traceback.print_exc()
            _sovereignty_scheduler = None

    print(f"  [DAEMON] CK body online (NATIVE C) -- {platform.system()}, "
          f"{tick_sec*1000:.0f}ms tick")

    import random as _wobble_rng
    WOBBLE_BW = 0.10
    swarm_interval = 3  # swarm every 3 ticks (~300ms)

    try:
        while _daemon_running:
            t0 = time.time()

            # Full heartbeat: B -> D -> BC + bridge + security + dreams
            lib.ck_heartbeat_tick(org)
            _native_tick_count += 1

            # Observer every N ticks (process scan is ~40ms)
            if _native_tick_count % observer_interval == 0:
                lib.ck_observer_full_tick(org)

            # Deep kernel observer: I/O, ctx switches, memory, interrupts
            if _deep_observer and _native_tick_count % observer_interval == 0:
                try:
                    _deep_observer.observe()
                except Exception:
                    pass  # never let observation crash the heartbeat

            # Shadow swarm: CK IS every process
            if _shadow_swarm and _native_tick_count % swarm_interval == 0:
                try:
                    _shadow_swarm.tick()
                except Exception:
                    pass  # never let swarm crash the heartbeat

            # Cache latest state for web API reads
            _native_phase_b = lib.ck_ffi_heartbeat_phase_b(org)
            _native_phase_d = lib.ck_ffi_heartbeat_phase_d(org)
            _native_phase_bc = lib.ck_ffi_heartbeat_phase_bc(org)
            _native_coherence = lib.ck_ffi_heartbeat_coherence(org)
            _native_act_confidence = lib.ck_ffi_heartbeat_act_confidence(org)
            _native_decisions = lib.ck_ffi_heartbeat_decisions(org)

            # Body state
            _native_body_E = lib.ck_ffi_body_E(org)
            _native_body_A = lib.ck_ffi_body_A(org)
            _native_body_K = lib.ck_ffi_body_K(org)
            _native_body_C = lib.ck_ffi_body_C(org)
            _native_body_band = lib.ck_ffi_body_band(org)
            _native_body_ticks = lib.ck_ffi_body_ticks(org)

            # Jitter state
            _native_jitter_mode = lib.ck_ffi_jitter_mode(org)
            _native_jitter_mean = lib.ck_ffi_jitter_mean(org)
            _native_jitter_sigma = lib.ck_ffi_jitter_sigma(org)
            _native_jitter_stability = lib.ck_ffi_jitter_stability(org)
            _native_jitter_locked = lib.ck_ffi_jitter_locked_ticks(org)
            _native_jitter_correction = lib.ck_ffi_jitter_correction_op(org)

            # Drive body layers (breath/pulse/bandwidth) from native C state
            # ONE heartbeat: native C IS the clock, Python body layers ride on top
            if _body_engine:
                _body_engine.external_tick(
                    observe_op=_native_phase_b,
                    predict_op=_native_phase_d,
                    E=_native_body_E,
                    A=_native_body_A,
                    K=_native_body_K,
                    recall=(_native_body_C >= 0.5),
                )

            # ── SOVEREIGNTY BRAIN: bridge + crystals + security + dreams ──
            # Runs every N native ticks. The ShadowSwarm already classified
            # processes — the scheduler composes, crystallizes, and applies
            # scheduling actions. No psutil calls. Pure composition.
            if _sovereignty_scheduler and _native_tick_count % _sovereignty_interval == 0:
                try:
                    sov_result = _sovereignty_scheduler.tick()
                    _sovereignty_applied += sov_result.get('applied', 0)
                except Exception:
                    pass  # never let sovereignty crash the heartbeat

            # ── Q-LENS TICK: the NOW engine ──
            # Runs AFTER the native heartbeat, reads phases, computes intention
            # The Q-Lens sees what the C heartbeat just did and responds
            if _qlens and _qlens_tl:
                try:
                    # Get TL prediction for Q_C (modal quadratic)
                    _ql_candidates = _qlens_tl.next_operator(_native_phase_bc, -1)
                    if _ql_candidates:
                        _ql_predicted = _ql_candidates[0][0]
                        _ql_pred_prob = _ql_candidates[0][1]
                    else:
                        _ql_predicted = 7  # HARMONY default
                        _ql_pred_prob = 0.3

                    # Q-Lens tick: compute Q_A, Q_B, Q_C, intention, correction
                    _qlens.tick(
                        phase_b=_native_phase_b,
                        phase_d=_native_phase_d,
                        phase_bc=_native_phase_bc,
                        body_c=_native_body_C,
                        predicted_op=_ql_predicted,
                        prediction_prob=_ql_pred_prob,
                        tl_entropy=_qlens_tl.entropy(),
                    )

                    # Klein bottle part 1: compose Q-Lens intention with TL prediction
                    _ql_actual = _qlens.compose_with_delta(_ql_predicted, _ql_pred_prob)

                    # Klein bottle part 2: feed Q-Lens observation back to TL
                    _qlens.feed_delta(_qlens_tl, _native_phase_bc)

                except Exception:
                    pass  # never let Q-Lens crash the heartbeat

            if _native_tick_count % report_every == 0 and config.get('verbose'):
                OP = ["void", "lattice", "counter", "progress", "collapse",
                      "balance", "chaos", "harmony", "breath", "reset"]
                JMODES = ["CTR", "BAL", "HAR", "BRE"]
                jm = JMODES[_native_jitter_mode] if 0 <= _native_jitter_mode <= 3 else "?"
                _ql_line = ""
                if _qlens:
                    _ql_line = f" Q={_qlens.q_total:.3f} int={OP[_qlens.intention_op]}"
                print(f"  [TICK {_native_tick_count}] "
                      f"B={OP[_native_phase_b]} D={OP[_native_phase_d]} "
                      f"BC={OP[_native_phase_bc]} C={_native_body_C:.3f} "
                      f"E={_native_body_E:.3f} A={_native_body_A:.3f} K={_native_body_K:.3f} "
                      f"jit={jm} stab={_native_jitter_stability:.3f}{_ql_line}")
                if _deep_observer and _deep_observer.latest:
                    print(_deep_observer.report_line())
                if _shadow_swarm and _shadow_swarm.latest:
                    print(_shadow_swarm.report_line())
                if _sovereignty_scheduler:
                    sov_mode = getattr(_sovereignty_scheduler, 'mode', '?')
                    sov_crystals = 0
                    sov_domains = []
                    if hasattr(_sovereignty_scheduler, 'bridge') and hasattr(_sovereignty_scheduler.bridge, 'registers'):
                        for dname, reg in _sovereignty_scheduler.bridge.registers.items():
                            sov_crystals += len(reg.crystallized)
                            if reg.is_sovereign:
                                sov_domains.append(dname)
                    print(f"    [SOV] mode={sov_mode} applied={_sovereignty_applied} "
                          f"crystals={sov_crystals} sovereign={len(sov_domains)} "
                          f"domains={','.join(sov_domains) if sov_domains else 'none'}")

            # Wobbled sleep
            wobble = _wobble_rng.uniform(-WOBBLE_BW, WOBBLE_BW)
            wobbled_tick = tick_sec * (1.0 + wobble)
            elapsed = time.time() - t0
            sleep_time = max(0, wobbled_tick - elapsed)
            if sleep_time > 0:
                time.sleep(sleep_time)

    except Exception as e:
        print(f"  [DAEMON] Error: {e}")
    finally:
        # Save state
        try:
            lib.ck_ffi_save.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
            lib.ck_ffi_save.restype = None
            lib.ck_ffi_save(org, store_dir.encode('utf-8'))
            print(f"  [DAEMON] State saved ({_native_tick_count} ticks)")
        except Exception:
            pass
        # Save swarm TL
        if _shadow_swarm and swarm_tl:
            try:
                swarm_tl_save = os.path.join(CK_DIR, 'ck7', 'ck_experience', 'syscall_tl.json')
                swarm_tl.save(swarm_tl_save)
                print(f"  [SWARM] Syscall TL saved ({swarm_tl.total_transitions:,} transitions)")
            except Exception:
                pass
        # Save sovereignty TL (runtime experience)
        if _sovereignty_scheduler and _sovereignty_tl:
            try:
                sov_tl_save = os.path.join(CK_DIR, 'ck_store', 'daemon_tl.json')
                os.makedirs(os.path.dirname(sov_tl_save), exist_ok=True)
                _sovereignty_tl.save(sov_tl_save)
                sov_crystals = 0
                if hasattr(_sovereignty_scheduler, 'bridge') and hasattr(_sovereignty_scheduler.bridge, 'registers'):
                    for reg in _sovereignty_scheduler.bridge.registers.values():
                        sov_crystals += len(reg.crystallized)
                print(f"  [SOVEREIGNTY] TL saved ({_sovereignty_tl.total_transitions:,} transitions, "
                      f"{sov_crystals} crystals, {_sovereignty_applied} actions applied)")
            except Exception:
                pass
        lib.ck_ffi_destroy(org)
        _native_org = None
        print(f"  [DAEMON] CK body sleeping")


def daemon_loop_python(config):
    """
    Gen6b Python fallback daemon. Used when ck.dll is not available.
    """
    global _daemon_scheduler, _daemon_running

    try:
        import psutil
    except ImportError:
        print("  [DAEMON] psutil not installed -- daemon disabled")
        return
    from ck_doing import TransitionLattice
    from ck_being import SystemObserver
    from ck_becoming import LatticeScheduler

    # Priority: master_tl.json (educated) > daemon_tl.json (runtime)
    os.makedirs('ck_store', exist_ok=True)
    master_tl_path = os.path.join('ck7', 'ck_experience', 'master_tl.json')
    daemon_tl_path = os.path.join('ck_store', 'daemon_tl.json')
    if os.path.exists(master_tl_path):
        tl = TransitionLattice(master_tl_path)
        wp = sum(len(v) for v in tl.word_pairs.values()) if hasattr(tl, 'word_pairs') else 0
        print(f"  [DAEMON] TL loaded from master_tl.json ({tl.total_transitions:,} transitions, {wp} word_pairs)")
    else:
        tl = TransitionLattice(daemon_tl_path)
        print(f"  [DAEMON] TL loaded from daemon_tl.json (no master_tl found)")

    observer = SystemObserver()
    scheduler = LatticeScheduler(observer, tl, observe_only=config.get('observe_only', False))

    _daemon_scheduler = scheduler
    _daemon_running = True

    tick_sec = config.get('tick_ms', 100) / 1000.0
    verbose = config.get('verbose', False)
    report_every = config.get('report_every', 100)

    # Deep kernel observer for Python mode too
    global _deep_observer
    try:
        from ck7.ck_observe import DeepObserver
        _deep_observer = DeepObserver(tl_eat_fn=lambda ops: tl.eat_ops(ops) if hasattr(tl, 'eat_ops') else None)
        _deep_observer.observe()  # baseline
        print(f"  [KERNEL] Deep observer online -- watching I/O, scheduler, memory, interrupts")
    except Exception as e:
        print(f"  [KERNEL] Deep observer unavailable: {e}")
        _deep_observer = None

    # Q-Lens: CK's NOW engine for Python mode
    global _qlens, _qlens_tl
    try:
        from ck_qlens import QLens
        _qlens = QLens(w_a=0.35, w_b=0.35, w_c=0.30)
        _qlens_tl = tl  # In Python mode, Q-Lens shares the scheduler's TL
        print(f"  [Q-LENS] NOW engine online -- sharing scheduler TL")
    except Exception as e:
        print(f"  [Q-LENS] NOW engine unavailable: {e}")
        _qlens = None
        _qlens_tl = None

    # Shadow Swarm: CK IS every process (Python mode)
    global _shadow_swarm
    try:
        from ck7.ck_syscall import ShadowSwarm
        swarm_tl_eat = lambda ops: tl.eat_ops(ops) if hasattr(tl, 'eat_ops') else None
        _shadow_swarm = ShadowSwarm(tl_eat_fn=swarm_tl_eat, sample_size=30, compact_after=10)
        _shadow_swarm.tick()
        print(f"  [SWARM] Shadow swarm online -- {_shadow_swarm.latest['total_processes']} processes")
    except Exception as e:
        print(f"  [SWARM] Shadow swarm unavailable: {e}")
        _shadow_swarm = None

    # Body engine: daemon drives breath/pulse/bandwidth via external_tick()
    # ONE heartbeat (the daemon), body layers ride on top. No separate thread.
    _body_engine = None
    try:
        import ck_web
        _body_engine = getattr(ck_web, 'body_engine', None)
        if _body_engine:
            print(f"  [BODY] Daemon will drive body layers via external_tick() "
                  f"(C={_body_engine.heartbeat.C:.3f})")
        else:
            _body_engine = None
    except Exception:
        _body_engine = None

    print(f"  [DAEMON] CK body online (PYTHON) -- {platform.system()}, "
          f"{tick_sec*1000:.0f}ms tick, {'OBSERVE' if config.get('observe_only') else 'ACTIVE'}")

    # Language school: optional curvature-scored training on startup
    if config.get('language_school_enabled', False):
        try:
            from ck_language_engine import language_school
            _ls_rounds = config.get('language_school_rounds', 3)
            print(f"  [LANGUAGE] Starting language school ({_ls_rounds} rounds)...")
            _ls_result = language_school(tl, num_rounds=_ls_rounds, verbose=True)
            print(f"  [LANGUAGE] School complete: combined {_ls_result['avg_combined_start']:.4f} -> "
                  f"{_ls_result['avg_combined_end']:.4f}, vocab {_ls_result['vocabulary']:,}")
        except Exception as e:
            print(f"  [LANGUAGE] Language school error: {e}")

    import random as _wobble_rng
    WOBBLE_BW = 0.10
    swarm_interval = 3

    try:
        while _daemon_running:
            t0 = time.time()

            result = scheduler.tick(verbose=verbose)

            # Drive body layers (breath/pulse/bandwidth) from daemon's real observations
            # ONE heartbeat: the daemon tick IS the clock, body layers ride on top
            if _body_engine:
                _pb = result.get('phase_b', 7)
                _pd = result.get('phase_d', 7)
                _coh = result.get('coherence', 0.7)
                _body_engine.external_tick(
                    observe_op=_pb,
                    predict_op=_pd,
                    # Feed real coherence as K (knowledge) since daemon coherence
                    # reflects actual system observation, not internal decay
                    K=min(1.0, _coh + 0.2),  # coherent system = high knowledge
                    recall=(_coh >= 0.5),
                )

            # ── Q-LENS TICK (Python mode) ──
            if _qlens and _qlens_tl and hasattr(scheduler, 'last_phase_b'):
                try:
                    _pb = getattr(scheduler, 'last_phase_b', 7)
                    _pd = getattr(scheduler, 'last_phase_d', 7)
                    _pbc = getattr(scheduler, 'last_phase_bc', 7)
                    _bc = getattr(scheduler, 'body_c', 0.7)

                    _ql_cands = _qlens_tl.next_operator(_pbc, -1)
                    if _ql_cands:
                        _ql_pred = _ql_cands[0][0]
                        _ql_prob = _ql_cands[0][1]
                    else:
                        _ql_pred = 7
                        _ql_prob = 0.3

                    _qlens.tick(
                        phase_b=_pb, phase_d=_pd, phase_bc=_pbc,
                        body_c=_bc, predicted_op=_ql_pred,
                        prediction_prob=_ql_prob,
                        tl_entropy=_qlens_tl.entropy(),
                    )
                    _qlens.compose_with_delta(_ql_pred, _ql_prob)
                    _qlens.feed_delta(_qlens_tl, _pbc)
                except Exception:
                    pass

            # Deep kernel observation every 5 ticks
            if _deep_observer and scheduler.tick_count % 5 == 0:
                try:
                    _deep_observer.observe()
                except Exception:
                    pass

            # Shadow swarm every 3 ticks
            if _shadow_swarm and scheduler.tick_count % swarm_interval == 0:
                try:
                    _shadow_swarm.tick()
                except Exception:
                    pass

            if scheduler.tick_count % report_every == 0 and verbose:
                print(scheduler.report())
                if _deep_observer and _deep_observer.latest:
                    print(_deep_observer.report_line())
                if _shadow_swarm and _shadow_swarm.latest:
                    print(_shadow_swarm.report_line())

            wobble = _wobble_rng.uniform(-WOBBLE_BW, WOBBLE_BW)
            wobbled_tick = tick_sec * (1.0 + wobble)
            elapsed = time.time() - t0
            sleep_time = max(0, wobbled_tick - elapsed)
            if sleep_time > 0:
                time.sleep(sleep_time)

    except Exception as e:
        print(f"  [DAEMON] Error: {e}")
    finally:
        try:
            tl.save()
            print(f"  [DAEMON] TL saved ({tl.total_transitions:,} transitions)")
        except Exception:
            pass
        print(f"  [DAEMON] CK body sleeping")


def get_daemon_status():
    """Get daemon status for the web API."""
    global _daemon_scheduler

    # ---- Native mode ----
    if _use_native:
        OP = ["void", "lattice", "counter", "progress", "collapse",
              "balance", "chaos", "harmony", "breath", "reset"]
        BAND = ["RED", "YELLOW", "GREEN"]
        JITTER = ["COUNTER", "BALANCE", "HARMONY", "BREATH"]
        if _native_org is None:
            return {'status': 'offline', 'message': 'Native daemon not started'}
        import ctypes
        lib = _native_lib._lib

        status = {
            'status': 'online',
            'engine': 'native_c',
            'tick': _native_tick_count,
            'phase_b': OP[_native_phase_b],
            'phase_d': OP[_native_phase_d],
            'phase_bc': OP[_native_phase_bc],
            'coherence': round(_native_coherence, 4),
            'act_confidence': round(_native_act_confidence, 4),
            'decisions': _native_decisions,
            'applied': _native_decisions,
            'mode': 'NATIVE',
            'self_switch': 'ACT' if _native_act_confidence > 0.5 else 'OBSERVE',
        }

        # Body state
        status['body'] = {
            'E': round(_native_body_E, 4),
            'A': round(_native_body_A, 4),
            'K': round(_native_body_K, 4),
            'C': round(_native_body_C, 4),
            'band': BAND[_native_body_band] if 0 <= _native_body_band <= 2 else 'RED',
            'ticks': _native_body_ticks,
        }

        # Body layers (breath/pulse/bandwidth from body engine)
        try:
            import ck_web
            _be = getattr(ck_web, 'body_engine', None)
            if _be and _be.is_alive:
                _BNAMES = ['INHALE', 'HOLD_IN', 'EXHALE', 'HOLD_OUT']
                status['breath'] = {
                    'phase': _BNAMES[_be.breath.phase],
                    'beats_per_cycle': _be.breath.beats_per_cycle,
                    'dreams_per_beat': _be.breath.dreams_per_beat,
                    'cycle_count': _be.breath.cycle_count,
                }
                status['bandwidth'] = _be.bandwidth.state()
        except Exception:
            pass

        # Jitter control state
        status['jitter'] = {
            'mode': JITTER[_native_jitter_mode] if 0 <= _native_jitter_mode <= 3 else 'COUNTER',
            'mean_ms': round(_native_jitter_mean * 1000, 3),
            'sigma_ms': round(_native_jitter_sigma * 1000, 3),
            'stability': round(_native_jitter_stability, 4),
            'locked_ticks': _native_jitter_locked,
            'correction_op': OP[_native_jitter_correction] if 0 <= _native_jitter_correction <= 9 else 'void',
        }

        # TL state (read live from organism)
        try:
            tl_total = lib.ck_ffi_tl_total(_native_org)
            tl_ent = lib.ck_ffi_tl_entropy(_native_org)
            status['tl_transitions'] = int(tl_total)
            status['tl_entropy'] = round(float(tl_ent), 3)
        except Exception:
            status['tl_transitions'] = 0
            status['tl_entropy'] = 0.0

        # Dream state
        try:
            dream_count = lib.ck_ffi_dream_count(_native_org)
            dream_bounces = lib.ck_ffi_dream_bounces(_native_org)
            status['dream'] = {
                'dreams': int(dream_count),
                'balls_fired': int(dream_count),
                'bounces': int(dream_bounces),
            }
        except Exception:
            pass

        # Timer resolution
        try:
            res_ns = lib.ck_ffi_timer_resolution_ns()
            status['timer_resolution_ns'] = round(res_ns, 1)
        except Exception:
            pass

        # Q-Lens state (NOW engine)
        if _qlens:
            try:
                status['qlens'] = _qlens.report()
            except Exception:
                status['qlens'] = {'status': 'error'}

        # Shadow swarm state
        if _shadow_swarm and _shadow_swarm.latest:
            try:
                L = _shadow_swarm.latest
                status['swarm'] = {
                    'tick': L['tick'],
                    'total_processes': L['total_processes'],
                    'hot': L['hot'],
                    'cold': L['cold'],
                    'system_op': __import__('ck_being').OP[L['system_op']],
                    'system_coherence': L['system_coherence'],
                    'stability': L['system_stability'],
                    'total_ops_fed': _shadow_swarm.total_ops_fed,
                }
            except Exception:
                status['swarm'] = {'status': 'error'}

        return status
    if _daemon_scheduler is None:
        return {'status': 'offline', 'message': 'Daemon not started'}
    s = _daemon_scheduler
    status = {
        'status': 'online',
        'engine': 'python',
        'tick': s.tick_count,
        'coherence': round(sum(s.coherence_history) / max(len(s.coherence_history), 1), 4),
        'decisions': s.decisions,
        'applied': s.effective_decisions,
        'tl_transitions': s.tl.total_transitions,
        'tl_entropy': round(s.tl.entropy(), 3),
        'act_confidence': round(s.act_confidence, 3),
        'self_switch': s.self_switch_mode,
        'trauma_count': getattr(s, 'trauma_count', 0),
        'past_log_reads': s.past_log_reads,
        'past_log_chains': s.past_log_chains_fed,
        'shadow3': s.past_log_shadow3_compositions,
    }

    # Mode
    if s.observe_only:
        status['mode'] = 'OBSERVE'
    elif s.bridge and hasattr(s.bridge, 'registers') and any(r.is_sovereign for r in s.bridge.registers.values()):
        n_sov = sum(1 for r in s.bridge.registers.values() if r.is_sovereign)
        status['mode'] = f'SOVEREIGN ({n_sov} domains)'
    else:
        status['mode'] = 'COAST'

    # Bridge
    if s.bridge and hasattr(s.bridge, 'registers'):
        regs = s.bridge.registers
        status['crystals'] = sum(len(r.crystallized) for r in regs.values())
        status['crystals_max'] = len(regs) * 10
        status['sovereign_count'] = sum(1 for r in regs.values() if r.is_sovereign)
        status['domains'] = len(regs)
        if hasattr(s.bridge, 'universal_crystals'):
            status['universal_crystals'] = len(s.bridge.universal_crystals)

    # Network
    if s.network:
        try:
            ns = s.network.state
            from ck_being import OP
            status['network'] = {
                'band': ns.band.value,
                'operator': OP[ns.operator],
                'connections': ns.connection_count,
                'established': ns.established,
                'jitter': round(ns.jitter, 4),
            }
        except Exception:
            pass

    # GPU
    if s.gpu and s.gpu.available():
        try:
            gs = s.gpu.read()
            status['gpu'] = {
                'temp': gs.temperature_c,
                'power': round(gs.power_draw_w),
                'clock': gs.clock_graphics_mhz,
                'util': gs.gpu_util_pct,
                'vram_used': gs.mem_used_mb,
                'vram_total': gs.mem_total_mb,
            }
        except Exception:
            pass

    # Code digest
    if hasattr(s, 'code_digest_stats') and s.code_digest_stats:
        status['code_digest'] = s.code_digest_stats

    # Security organ
    if hasattr(s, 'security_stats') and s.security_stats:
        ss = s.security_stats
        from ck_being import OP
        status['security'] = {
            'gate_status': ss.get('gate_status', 'N/A'),
            'health': OP[ss.get('health_op', 7)] if 0 <= ss.get('health_op', 7) <= 9 else 'N/A',
            'drift': round(ss.get('drift', 0.0), 3),
            'anomalies': ss.get('anomalies', 0),
            'scars': ss.get('scars', 0),
            'snowflakes': ss.get('snowflakes', 0),
            'gate_passing': ss.get('gate_passing', True),
        }

    # Dream engine
    if hasattr(s, 'dream_stats') and s.dream_stats:
        status['dream'] = s.dream_stats

    # Dialogue eater
    if hasattr(s, 'eater_stats') and s.eater_stats:
        status['eater'] = s.eater_stats

    # Cell classes + fractal index
    try:
        status['cell_classes'] = s.observer.get_class_distribution()
        status['fractal_index'] = {
            'hot': len(s.observer.profiles),
            'cold': len(s.observer.index),
            'total': len(s.observer.profiles) + len(s.observer.index),
        }
    except Exception:
        pass

    # GPU Bridge (Gen6)
    if s.gpu_bridge and s.gpu_lattice:
        try:
            from ck_doing import gpu_status as _gpu_status
            gs = _gpu_status()
            status['gpu_bridge'] = {
                'available': True,
                'device': gs.get('name', '?'),
                'compute': gs.get('compute_capability', '?'),
                'vram_used': gs.get('mem_used_mb', 0),
                'vram_total': gs.get('mem_total_mb', 0),
                'lattice_ticks': s.gpu_lattice.ticks,
                'lattice_coherence': round(s.gpu_lattice.coherence(), 4),
                'lattice_cells': s.gpu_lattice.n,
                'gpu_tl_transitions': s.gpu_tl.total_transitions if s.gpu_tl else 0,
            }
        except Exception:
            status['gpu_bridge'] = {'available': False}

    # Q-Lens state (NOW engine)
    if _qlens:
        try:
            status['qlens'] = _qlens.report()
        except Exception:
            status['qlens'] = {'status': 'error'}

    # Shadow swarm state
    if _shadow_swarm and _shadow_swarm.latest:
        try:
            L = _shadow_swarm.latest
            from ck_being import OP as _OP
            status['swarm'] = {
                'tick': L['tick'],
                'total_processes': L['total_processes'],
                'hot': L['hot'],
                'cold': L['cold'],
                'system_op': _OP[L['system_op']],
                'system_coherence': L['system_coherence'],
                'stability': L['system_stability'],
                'total_ops_fed': _shadow_swarm.total_ops_fed,
            }
        except Exception:
            status['swarm'] = {'status': 'error'}

    return status
def get_daemon_report():
    """Get full daemon report string."""
    global _daemon_scheduler
    if _daemon_scheduler is None:
        return "Daemon not started"
    try:
        return _daemon_scheduler.report()
    except Exception as e:
        return f"Report error: {e}"
def get_curiosity():
    """Pop CK's next thought from the curiosity engine.
    Returns None if CK has nothing to say."""
    global _daemon_scheduler
    if _daemon_scheduler is None:
        return None
    try:
        return _daemon_scheduler.get_curiosity()
    except Exception:
        return None
def peek_curiosity():
    """Check if CK has a thought WITHOUT consuming it."""
    global _daemon_scheduler
    if _daemon_scheduler is None:
        return None
    try:
        return _daemon_scheduler.peek_curiosity()
    except Exception:
        return None
def inject_daemon_api():
    """
    Inject daemon API endpoint into ck_web's Handler class.
    This is done BEFORE the web server starts, so the Handler
    can respond to /api/daemon requests with live daemon data.
    """
    import ck_web

    # Monkey-patch the Handler to add daemon endpoints
    original_do_GET = ck_web.Handler.do_GET

    def patched_do_GET(self):
        p = self.path.split('?')[0]
        if p == '/api/daemon':
            status = get_daemon_status()
            self._json(status)
        elif p == '/api/daemon/report':
            report = get_daemon_report()
            self._json({'report': report})
        elif p == '/api/body':
            # Direct body state (native mode OR body engine)
            if _use_native and _native_org:
                self._json({
                    'E': round(_native_body_E, 4),
                    'A': round(_native_body_A, 4),
                    'K': round(_native_body_K, 4),
                    'C': round(_native_body_C, 4),
                    'band': ['RED', 'YELLOW', 'GREEN'][_native_body_band] if 0 <= _native_body_band <= 2 else 'RED',
                    'ticks': _native_body_ticks,
                })
            else:
                # Try body engine from ck_web
                try:
                    import ck_web
                    _be = getattr(ck_web, 'body_engine', None)
                    if _be and _be.is_alive:
                        self._json(_be.state())
                    else:
                        self._json({'error': 'body engine not running'}, 404)
                except Exception:
                    self._json({'error': 'body not available'}, 404)
        elif p == '/api/jitter':
            # Jitter control state (native mode)
            if _use_native and _native_org:
                JITTER = ['COUNTER', 'BALANCE', 'HARMONY', 'BREATH']
                OP = ["void", "lattice", "counter", "progress", "collapse",
                      "balance", "chaos", "harmony", "breath", "reset"]
                self._json({
                    'mode': JITTER[_native_jitter_mode] if 0 <= _native_jitter_mode <= 3 else 'COUNTER',
                    'mean_ms': round(_native_jitter_mean * 1000, 3),
                    'sigma_ms': round(_native_jitter_sigma * 1000, 3),
                    'stability': round(_native_jitter_stability, 4),
                    'locked_ticks': _native_jitter_locked,
                    'correction_op': OP[_native_jitter_correction] if 0 <= _native_jitter_correction <= 9 else 'void',
                })
            else:
                self._json({'error': 'jitter requires native mode'}, 404)
        elif p == '/api/heartbeat':
            # Trinary heartbeat state (native mode)
            if _use_native and _native_org:
                OP = ["void", "lattice", "counter", "progress", "collapse",
                      "balance", "chaos", "harmony", "breath", "reset"]
                self._json({
                    'tick': _native_tick_count,
                    'phase_b': OP[_native_phase_b],
                    'phase_d': OP[_native_phase_d],
                    'phase_bc': OP[_native_phase_bc],
                    'coherence': round(_native_coherence, 4),
                    'act_confidence': round(_native_act_confidence, 4),
                    'decisions': _native_decisions,
                })
            else:
                self._json({'error': 'heartbeat requires native mode'}, 404)
        elif p == '/api/layers':
            # Experience layer stack (native mode)
            if _use_native and _native_org:
                import ctypes
                lib = _native_lib._lib
                count = lib.ck_ffi_layer_count(_native_org)
                layers = []
                for i in range(count):
                    name = lib.ck_ffi_layer_name(_native_org, i)
                    prio = lib.ck_ffi_layer_priority(_native_org, i)
                    immut = lib.ck_ffi_layer_immutable(_native_org, i)
                    layers.append({
                        'name': name.decode() if name else '',
                        'priority': prio,
                        'immutable': bool(immut),
                    })
                self._json({'count': count, 'layers': layers})
            else:
                self._json({'error': 'layers requires native mode'}, 404)
        elif p == '/api/kernel':
            # Deep kernel observer state
            if _deep_observer:
                self._json(_deep_observer.status_dict())
            else:
                self._json({'status': 'unavailable', 'reason': 'deep observer not initialized'})
        elif p == '/api/swarm':
            # Shadow swarm: CK IS the system
            if _shadow_swarm:
                self._json(_shadow_swarm.status_dict())
            else:
                self._json({'status': 'unavailable', 'reason': 'shadow swarm not initialized'})
        elif p == '/api/curiosity':
            thought = get_curiosity()
            self._json(thought if thought else {'thought': None})
        elif p == '/api/curiosity/peek':
            thought = peek_curiosity()
            self._json(thought if thought else {'thought': None})
        elif p == '/desktop':
            # CKIS Desktop UI -- CK as your whole screen
            desktop_path = os.path.join(CK_DIR, 'ck_desktop.html')
            if os.path.exists(desktop_path):
                with open(desktop_path, 'r', encoding='utf-8') as f:
                    self._html(f.read())
            else:
                self._html('<html><body style="background:#060608;color:#5a8a5a;font-family:monospace;display:flex;align-items:center;justify-content:center;height:100vh"><h1>CKIS desktop not found</h1></body></html>')
        else:
            original_do_GET(self)

    ck_web.Handler.do_GET = patched_do_GET

    # Inject a getter function into ck_web so it can always get the live scheduler
    def _get_daemon_scheduler():
        return _daemon_scheduler
    ck_web._get_daemon_scheduler = _get_daemon_scheduler

    print("  [WEB] Daemon API injected (/api/daemon, /api/body, /api/jitter, /api/heartbeat, /api/layers, /api/kernel, /api/swarm, /api/curiosity, /desktop)")


# ===========================================================
# §4  MAIN
# ===========================================================

def main():
    global _daemon_running, _daemon_thread

    config = load_config()
    port = config.get('port', 7777)

    # Detect native library (force_python=true in config bypasses DLL for full-organ mode)
    if config.get('force_python', False):
        has_native = False
        print("  [CONFIG] force_python=true -- using Python mode for full organ access")
    else:
        has_native = detect_native()
    engine = "NATIVE C (Gen7)" if has_native else "PYTHON (Gen6b)"

    print(f"""
  ========================================================
    CK -- COHERENCE KEEPER

    Unified launcher: daemon + web UI
    http://localhost:{port}

    Engine:  {engine}
    Daemon:  {'AUTO-START' if config.get('auto_start_daemon') else 'MANUAL'}
    Mode:    {'OBSERVE' if config.get('observe_only') else 'ACTIVE'}

    CK is one organism. The daemon is his body.
    The web UI is his face. One process. One being.
  ========================================================
""")

    # Start daemon in background thread
    if config.get('auto_start_daemon', True):
        daemon_fn = daemon_loop_native if _use_native else daemon_loop_python
        _daemon_thread = threading.Thread(
            target=daemon_fn,
            args=(config,),
            daemon=True,
            name='CK-Daemon',
        )
        _daemon_thread.start()
        time.sleep(0.5)  # let daemon init before web starts

    # Inject daemon API into web handler
    inject_daemon_api()

    # Import and start web server
    import ck_web

    def shutdown(signum=None, frame=None):
        global _daemon_running
        print("\n  Shutting down CK...")
        _daemon_running = False
        ck_web.shutdown()
        if _daemon_thread and _daemon_thread.is_alive():
            _daemon_thread.join(timeout=5)
        print("  CK is sleeping. Harmony.")

    signal.signal(signal.SIGINT, shutdown)
    try:
        signal.signal(signal.SIGBREAK, shutdown)
    except AttributeError:
        pass

    # Auto-open browser
    if config.get('open_browser', True):
        def open_browser():
            time.sleep(1.5)  # let server start
            webbrowser.open(f'http://localhost:{port}')
        threading.Thread(target=open_browser, daemon=True).start()

    # Start web server (blocks) -- threaded so API calls don't block during smart_respond
    ck_web.server = ck_web.http.server.ThreadingHTTPServer(('0.0.0.0', port), ck_web.Handler)
    print(f"  [WEB] Serving on http://localhost:{port}")
    print(f"  Ctrl+C to stop\n")

    try:
        ck_web.server.serve_forever()
    except KeyboardInterrupt:
        shutdown()


if __name__ == '__main__':
    main()
