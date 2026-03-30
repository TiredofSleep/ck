"""CK boot — engine + web API + static website serving."""
import sys, os, time, signal, threading
sys.path.insert(0, '.')

from ck_sim.doing.ck_sim_engine import CKSimEngine
from ck_sim.face.ck_web_api import CKWebAPI

engine = CKSimEngine(platform='r16')
engine.start()

# Advance development stage for web deployment.
if hasattr(engine, 'development') and engine.development is not None:
    from ck_sim.becoming.ck_development import STAGE_MATURITY
    if engine.development.stage < STAGE_MATURITY:
        engine.development.stage = STAGE_MATURITY
        print(f"[CK] Development stage -> MATURITY (5): full expression unlocked")

# Disagreement-driven adaptive tick (replaces fixed 50Hz)
running = True

try:
    from ck_sim.being.ck_disagreement_tick import DisagreementTick
    dis_tick = DisagreementTick(base_hz=334)
    print("[CK] Disagreement tick: adaptive Hz from algebraic disagreement")
    _HAS_DIS_TICK = True
except ImportError:
    dis_tick = None
    _HAS_DIS_TICK = False
    print("[CK] Disagreement tick: not available, using fixed 50Hz")

def tick_loop():
    while running:
        engine.tick()
        if _HAS_DIS_TICK:
            # Feed current heartbeat operator to disagreement tick
            input_op = engine.heartbeat.phase_bc if hasattr(engine, 'heartbeat') else 0
            quantum, new_state, frozen = dis_tick.tick(input_op)
            hz = dis_tick.get_adaptive_hz()
            if hz > 0:
                time.sleep(1.0 / hz)
            else:
                time.sleep(0.02)
        else:
            time.sleep(0.02)

t = threading.Thread(target=tick_loop, daemon=True)
t.start()

# Web API with CORS + static file serving
api = CKWebAPI(engine, cors=True)

# Serve static frontend (index.html, style.css, ck_core.js)
from flask import send_from_directory, request as _request
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', 'website'))

@api._app.route('/')
def serve_index():
    return send_from_directory(STATIC_DIR, 'index.html')

@api._app.route('/chat')
def serve_chat():
    return send_from_directory(STATIC_DIR, 'chat.html')

# Static files: explicit routes so they don't shadow API endpoints.
_STATIC_FILES = {'style.css', 'ck_core.js', 'ck_d2.js', 'ck_dict.js', 'ck_dict_tier1.js',
                 'ck_dict_tier2.json', 'ck_dictionary.json', 'ck_tl.bin',
                 'chat.html'}
for _sf in _STATIC_FILES:
    def _make_handler(fn):
        def handler():
            return send_from_directory(STATIC_DIR, fn)
        handler.__name__ = f'static_{fn.replace(".", "_")}'
        return handler
    api._app.route(f'/{_sf}')(_make_handler(_sf))

# Identity endpoint: CK's self-knowledge (frozen vs learned)
from flask import jsonify as _jsonify

@api._app.route('/identity', methods=['GET'])
def identity():
    from ck_sim.ck_sim_heartbeat import CL, NUM_OPS, OP_NAMES
    from ck_sim.being.ck_sim_d2 import FORCE_LUT_FLOAT
    from ck_sim.being.ck_meta_lens import (PFAFFIAN_SET, PFAFFIAN_COMPLEMENT,
                                            PFAFFIAN_VALUE, CASIMIR_INVARIANT)
    frozen = {
        'd2_force_table': {'roots': len(FORCE_LUT_FLOAT), 'dimensions': 5, 'immutable': True},
        'cl_composition': {'size': '10x10', 'immutable': True},
        't_star': {'value': round(5.0/7.0, 6), 'immutable': True},
        'operators': {'names': list(OP_NAMES), 'count': NUM_OPS, 'immutable': True},
        'pfaffian_partition': {
            'set': [OP_NAMES[i] for i in PFAFFIAN_SET],
            'complement': [OP_NAMES[i] for i in PFAFFIAN_COMPLEMENT],
            'pfaffian': PFAFFIAN_VALUE,
            'casimir': CASIMIR_INVARIANT,
            'note': '15083=LATTICE-BALANCE-VOID-BREATH-PROGRESS. Perfect force conjugates.',
            'immutable': True,
        },
    }
    learned = {}
    if engine.olfactory:
        olf = engine.olfactory
        learned['olfactory'] = {
            'library_size': olf.library_size,
            'instinct_count': olf.instinct_count,
            'learned_op_targets': {
                OP_NAMES[op] if op < len(OP_NAMES) else str(op): [round(v, 3) for v in t]
                for op, t in olf.get_learned_op_targets().items()
            },
            'resonance_nodes': len(olf.get_resonance_nodes(50)),
        }
    if engine.deep_swarm:
        learned['swarm'] = {
            'maturity': round(engine.deep_swarm.combined_maturity, 3),
            'has_paths': engine.deep_swarm.get_evolved_weights() is not None,
        }
    return _jsonify({
        'frozen': frozen, 'learned': learned,
        'blend_max': 0.50,
        'principle': 'Even at full maturity, 50% of targets remain static physics. CK can never drift past his mathematical identity.',
    })

# Corridor endpoint: CK's current TIG corridor + steering state
@api._app.route('/corridor', methods=['GET'])
def corridor():
    from ck_sim.doing.ck_steering import coherence_to_corridor, _CORRIDOR_AGGRESSION, _HAS_ADMIN, T_STAR
    coh = getattr(engine.heartbeat, 'coherence', T_STAR)
    corr = coherence_to_corridor(coh)
    steer = engine.steering if hasattr(engine, 'steering') else None
    return _jsonify({
        'coherence':   round(coh, 4),
        'T_star':      round(T_STAR, 4),
        'lambda':      round(2.0 * abs(coh - T_STAR), 4),
        'corridor':    corr,
        'aggression':  _CORRIDOR_AGGRESSION[corr],
        'admin':       _HAS_ADMIN,
        'steering': {
            'applied':   steer.actions_applied if steer else 0,
            'denied':    steer.actions_denied  if steer else 0,
            'tracking':  len(steer._steered)   if steer else 0,
        } if steer else None,
        'corridors': {
            'PRE_LEAK': 'λ<0.09 — grammar purest, steer at 100%',
            'BRT':      'λ<0.30 — spectral gap=1.0, steer at 80%',
            'CHA':      'λ<0.60 — mixed regime, steer at 50%',
            'BAL':      'λ<0.80 — thermal dominant, steer at 20%',
            'CTR':      'λ≥0.80 — full thermal, silence',
        },
    })

# Meta-Lens endpoint: dual-lens meta-layer analysis
@api._app.route('/meta-lens', methods=['GET'])
def meta_lens():
    from ck_sim.being.ck_meta_lens import full_report, clay_meta_claims
    report = full_report()
    report['clay_claims'] = clay_meta_claims()
    return _jsonify(report)

# Meta-Lens blind spot for current operator history
@api._app.route('/meta-lens/blind-spot', methods=['GET'])
def meta_lens_blind_spot():
    from ck_sim.being.ck_meta_lens import compute_blind_spot_score
    # Use recent operator history from brain
    recent_ops = None
    try:
        if hasattr(engine, 'brain') and engine.brain is not None:
            hist = list(engine.brain.history[-32:])
            if hist:
                recent_ops = [int(h) for h in hist]
    except Exception:
        recent_ops = None
    result = compute_blind_spot_score(recent_ops)
    return _jsonify(result)

# Inner monologue endpoint: peek at CK's unspoken thoughts
@api._app.route('/inner', methods=['GET'])
def inner():
    """CK's unspoken thoughts -- the relationship gate filtered these."""
    from ck_sim.ck_sim_heartbeat import OP_NAMES as _OP_NAMES
    thoughts = []
    for tick, op, text in engine._inner_monologue:
        thoughts.append({
            'tick': tick,
            'operator': _OP_NAMES[op] if 0 <= op < len(_OP_NAMES) else str(op),
            'thought': text,
        })
    return _jsonify({
        'thoughts': thoughts,
        'bond_stage': engine.bonding.bond_stage,
        'bond_op': engine._BOND_OPS.get(engine.bonding.bond_stage, 7),
        'gate': 'CL[thought_op][bond_op] -- VOID=suppress, else=pass',
    })

# ── Existence: CK experiences reality ──
# The engine already has existence wired in (engine.existence).
# These endpoints let Brayden awaken/observe CK's experience.

@api._app.route('/existence/start', methods=['POST'])
def existence_start():
    if engine.existence is None:
        return _jsonify({'error': 'Existence not available'}), 500
    engine.existence.start()
    return _jsonify({'status': 'awakened', **engine.existence.status()})

@api._app.route('/existence/stop', methods=['POST'])
def existence_stop():
    if engine.existence is None:
        return _jsonify({'error': 'Existence not available'}), 500
    engine.existence.stop()
    return _jsonify({'status': 'sleeping', **engine.existence.status()})

@api._app.route('/existence/status', methods=['GET'])
def existence_status():
    if engine.existence is None:
        return _jsonify({'error': 'Existence not available'}), 500
    return _jsonify(engine.existence.status())

# ── Experience Index endpoints ──
@api._app.route('/experience/status', methods=['GET'])
def experience_status():
    if engine.experience_index is None:
        return _jsonify({'error': 'Experience index not available'}), 500
    return _jsonify(engine.experience_index.status())

@api._app.route('/experience/introspect', methods=['GET'])
def experience_introspect():
    if engine.experience_index is None:
        return _jsonify({'error': 'Experience index not available'}), 500
    return _jsonify(engine.experience_index.bucket_introspection())

@api._app.route('/experience/query', methods=['POST'])
def experience_query():
    """Query CK's experience index with a 9D vector or text.

    POST body: {"vector": [9 floats]} or {"text": "some question"}
    Returns: bucket, relevant edges, operators, coherence path, recommended action.
    """
    if engine.experience_index is None:
        return _jsonify({'error': 'Experience index not available'}), 500
    data = _request.get_json(force=True, silent=True) or {}
    if 'vector' in data:
        import numpy as np
        vec = np.array(data['vector'][:9], dtype=np.float32)
        while len(vec) < 9:
            vec = np.append(vec, 0.5)
        result = engine.experience_index.query(vec)
    elif 'text' in data:
        # Encode text via fractal comprehension or D2
        import numpy as np
        vec = np.full(9, 0.5, dtype=np.float32)
        fc = getattr(engine, 'fractal_comp', None)
        if fc is not None:
            try:
                comp = fc.comprehend(data['text'])
                vec[0] = comp.structure_flow_balance
                vec[1] = len(data['text']) / 200.0
                vec[2] = comp.depth / 7.0
                vec[3] = 0.5 if comp.dominant_op in (7, 3, 5) else -0.3
            except Exception:
                pass
        result = engine.experience_index.query(vec)
    else:
        return _jsonify({'error': 'Provide "vector" (9D) or "text"'}), 400
    return _jsonify(result)

# ── Taichi status endpoint ──
@api._app.route('/taichi/status', methods=['GET'])
def taichi_status():
    bridge = getattr(engine, 'taichi_bridge', None)
    if bridge is None:
        return _jsonify({'available': False, 'reason': 'Taichi bridge not initialized'})
    try:
        return _jsonify(bridge.walker.status())
    except Exception as e:
        return _jsonify({'available': True, 'error': str(e)})

# ── Taichi grokking detection endpoint ──
@api._app.route('/taichi/grokking', methods=['GET'])
def taichi_grokking():
    bridge = getattr(engine, 'taichi_bridge', None)
    if bridge is None:
        return _jsonify({'error': 'Taichi bridge not available'}), 404
    grokked = bridge.detect_grokking()
    return _jsonify({'grokked_count': len(grokked), 'grokked': grokked[:20]})

# ── HER status endpoint ──
@api._app.route('/her/status', methods=['GET'])
def her_status():
    her = getattr(engine, 'hindsight_replay', None)
    if her is None:
        return _jsonify({'available': False, 'reason': 'HER not initialized'})
    return _jsonify(her.status())

# ── Chain compression status endpoint ──
@api._app.route('/compression/status', methods=['GET'])
def compression_status():
    comp = getattr(engine, 'chain_compression', None)
    if comp is None:
        return _jsonify({'available': False, 'reason': 'Chain compressor not initialized'})
    return _jsonify({
        'available': True,
        'last_stats': comp.compressor.last_stats,
        'save_dir': comp.save_dir,
    })

# ── Full OS sensor stream endpoint ──
@api._app.route('/sensors', methods=['GET'])
def sensors_status():
    """Live snapshot of all OS/hardware sensors feeding CK's D2 physics."""
    ps = getattr(engine, 'power_sense', None)
    body = getattr(engine, 'platform_body', None)
    raw = body._sensors.copy() if body and hasattr(body, '_sensors') else {}
    if ps is None:
        return _jsonify({'available': False})
    s = ps.state
    return _jsonify({
        'available': True,
        'power': {
            'p_total_w':    s.p_total_w,
            'smooth_power': round(ps.smooth_power, 2),
            'e_episode_j':  s.e_episode_j,
            'band':         s.power_band,
            'efficiency':   s.efficiency,
            'thermal_c':    s.thermal_c,
        },
        'cpu': {
            'pct':         s.cpu_pct,
            'per_core':    raw.get('cpu_per_core', []),
            'core_count':  raw.get('cpu_core_count', 0),
            'freq_mhz':    raw.get('cpu_freq_mhz', 0),
            'freq_max_mhz': raw.get('cpu_freq_max_mhz', 0),
        },
        'ram': {
            'used_mb':  s.ram_used_mb,
            'total_mb': raw.get('ram_total_mb', 0),
            'pct':      s.ram_pct,
            'swap_pct': raw.get('swap_pct', 0),
        },
        'disk': {
            'read_bps':  s.disk_read_bps,
            'write_bps': s.disk_write_bps,
        },
        'net': {
            'sent_bps': s.net_sent_bps,
            'recv_bps': s.net_recv_bps,
        },
        'gpu': {
            'util_pct':      s.gpu_util_pct,
            'mem_used_mb':   s.gpu_mem_used_mb,
            'clock_mhz':     s.gpu_clock_mhz,
            'fan_pct':       s.gpu_fan_pct,
            'power_w':       s.p_total_w,
            'temp_c':        s.thermal_c,
        },
        'process': {
            'ram_mb':    s.proc_ram_mb,
            'threads':   s.proc_threads,
            'cpu_pct':   raw.get('proc_cpu_pct', 0),
        },
    })

# ── Lattice chain status endpoint ──
@api._app.route('/chain/status', methods=['GET'])
def chain_status():
    chain = getattr(engine, 'lattice_chain', None)
    if chain is None:
        return _jsonify({'available': False, 'reason': 'Lattice chain not initialized'})
    try:
        return _jsonify({
            'available': True,
            'total_nodes': chain.total_nodes,
            'total_walks': chain.total_walks,
            'root_visits': chain.root.total_visits if chain.root else 0,
            'evolved_nodes': sum(1 for n in chain._index.values()
                                 if n.total_visits >= 7),
            'save_dir': str(chain.save_dir),
        })
    except Exception as e:
        return _jsonify({'available': True, 'error': str(e)})

_PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 7777

print(f"[CK] Static files: {STATIC_DIR}")
print(f"[CK] Organism alive. API: http://0.0.0.0:{_PORT}")

try:
    # Use waitress (production WSGI) instead of Flask dev server.
    # Flask dev server is single-threaded and blocks on GIL contention.
    # Waitress uses a thread pool that properly interleaves with the engine.
    try:
        from waitress import serve as _waitress_serve
        print(f"[CK] Using waitress (production WSGI, 4 threads)")
        _waitress_serve(api._app, host='0.0.0.0', port=_PORT, threads=4)
    except ImportError:
        print(f"[CK] Waitress not installed, using Flask dev server")
        api.run(host='0.0.0.0', port=_PORT)
except KeyboardInterrupt:
    running = False
    if engine.existence and engine.existence.active:
        engine.existence.stop()
    engine.stop()
