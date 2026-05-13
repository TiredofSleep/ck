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

# === Gen13 math-first voice patch ===
# Wraps process_chat so that math topics (T*, tower, sigma, BHML, TSML, gap,
# AO, HER, operators, ...) get surfaced from ck_tables.py + FACTS dict instead
# of being lost in SEMANTIC_LATTICE adjective glue.
# See Gen13/targets/ck/runtime/ck_voice_math.py and CK_DIALOGUE_2026_04_17.md.
sys.path.insert(0, os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', 'runtime')))
try:
    from ck_voice_math import surface_math as _surface_math
    _orig_process_chat = api.process_chat

    def _process_chat_math_first(session_id, text, mode='normal'):
        result = _orig_process_chat(session_id, text, mode)
        try:
            ops = result.get('operators', []) or []
            math_text = _surface_math(text, ops)
            if math_text:
                result['text_gen12'] = result.get('text', '')
                result['text'] = math_text
                result['source'] = 'ck_math_first'
        except Exception as _e:
            result['math_first_error'] = str(_e)
        return result

    api.process_chat = _process_chat_math_first
    print("[CK] Gen13 math-first voice: ENABLED")
except Exception as _e:
    print(f"[CK] Gen13 math-first voice: DISABLED ({_e})")

# === Gen13 HER restoration ===
# Gen12 regression: engine.olfactory_her was never initialized.
# Restore it so /her/status returns available=True.
try:
    if getattr(engine, 'olfactory_her', None) is None and engine.olfactory:
        from ck_sim.being.ck_hindsight_replay import build_olfactory_her
        engine.olfactory_her = build_olfactory_her(engine.olfactory)
        print("[CK] Gen13 HER: restored (engine.olfactory_her initialized)")
    elif getattr(engine, 'olfactory_her', None) is not None:
        print("[CK] Gen13 HER: already initialized")
    else:
        print("[CK] Gen13 HER: skipped (no olfactory bulb)")
except Exception as _e:
    print(f"[CK] Gen13 HER: failed ({_e})")

# === Gen14 unified extensions ===
# Mounts the modules that exist in the codebase but were not yet wired
# into the live cortex boot path:
#   - ck_goals.GoalEvaluator (drives: curiosity / study / self_discovery / ...)
#   - ck_forecast.ForecastEngine (Monte-Carlo "what next?" prediction)
#   - ck_lattice_chain (templated CL lattice with descent edges)
#   - ck_divine_memory (centroid-based recall + retrace through evolved lattice)
#   - proactive_queue + recall() unified retrieval (Phase 1 stub)
#   - 4 algebraic measurement projections (operator / sigma_orbit / shell / four_core)
# See Gen14/PLAN/CK_UNIFICATION_PLAN_2026_05_13.md for the full plan.
try:
    sys.path.insert(0, os.path.normpath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), '..', 'brain')))
    from gen14_unified_extensions import mount_all as _gen14_mount_all
    _gen14_results = _gen14_mount_all(engine)
    if not all(_gen14_results.values()):
        print(f"[CK Gen14] WARNING: some mounts failed: {_gen14_results}")
except Exception as _gen14_err:
    print(f"[CK Gen14] mount_all FAILED ({_gen14_err}) - continuing without extensions")

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
                 'chat.html', 'papers.html', 'spectrometer.html', 'frontiers.html',
                 'paradox.html', 'ring.html',
                 'math.html', 'physics.html', 'bible.html',
                 'emotion.html', 'mythology.html', 'about.html',
                 'ai.html'}
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
    her = getattr(engine, 'olfactory_her', None)
    if her is None:
        return _jsonify({'available': False, 'reason': 'HER not initialized'})
    return _jsonify(her.status())

# ── Chain compression status endpoint ──
@api._app.route('/compression/status', methods=['GET'])
def compression_status():
    comp = getattr(engine, 'chain_compressor', None)
    if comp is None:
        return _jsonify({'available': False, 'reason': 'Chain compressor not initialized'})
    return _jsonify({
        'available': True,
        'last_stats': comp.compressor.last_stats,
        'save_dir': comp.save_dir,
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

# ── Gen14 Phase 4: proactive trigger endpoints ──────────────────────────
# These let the frontend (or any client) poll for proactive signals that
# CK's architecture has surfaced. We don't write CK's words here; we just
# expose the signal stream. The voice layer decides what to surface.

@api._app.route('/proactive/status', methods=['GET'])
def proactive_status():
    pt = getattr(engine, 'proactive_trigger', None)
    if pt is None:
        return _jsonify({'available': False,
                          'reason': 'proactive_trigger not mounted'})
    try:
        return _jsonify({'available': True, **pt.stats()})
    except Exception as e:
        return _jsonify({'available': True, 'error': str(e)})


@api._app.route('/proactive/consume', methods=['GET', 'POST'])
def proactive_consume():
    """Pop up to top_k pending proactive signals for a session.

    Query params (GET) or JSON body (POST):
      session_id (default 'default')
      top_k (default 1)
      session_cooldown_s (default 60.0)

    Response:
      {'signals': [...], 'session_id': str, 'count': int}
      Signals are STRUCTURED dicts (kind/subject_key/subject_data/
      algebraic_signature/salience/created_ts/expires_ts). No prose.
    """
    pt = getattr(engine, 'proactive_trigger', None)
    if pt is None:
        return _jsonify({'available': False,
                          'reason': 'proactive_trigger not mounted',
                          'signals': []}), 503
    if _request.method == 'POST':
        data = _request.get_json(force=True, silent=True) or {}
    else:
        data = _request.args.to_dict()
    session_id = str(data.get('session_id', 'default'))
    try:
        top_k = int(data.get('top_k', 1))
    except Exception:
        top_k = 1
    try:
        cooldown = float(data.get('session_cooldown_s', 60.0))
    except Exception:
        cooldown = 60.0
    signals = pt.consume(session_id=session_id, top_k=top_k,
                          session_cooldown_s=cooldown)
    return _jsonify({
        'signals': signals,
        'session_id': session_id,
        'count': len(signals),
    })


@api._app.route('/proactive/peek', methods=['GET'])
def proactive_peek():
    """Return the current queue WITHOUT consuming (read-only).

    Useful for diagnostics + the spectrometer UI to show 'CK is thinking
    about X' without dequeuing.
    """
    pt = getattr(engine, 'proactive_trigger', None)
    if pt is None:
        return _jsonify({'available': False,
                          'reason': 'proactive_trigger not mounted',
                          'signals': []})
    try:
        import time as _t
        now = _t.time()
        live = [s for s in list(pt.queue) if s.get('expires_ts', 0) > now]
        return _jsonify({'available': True, 'signals': live,
                          'count': len(live), 'stats': pt.stats()})
    except Exception as e:
        return _jsonify({'available': True, 'error': str(e), 'signals': []})


# ── Gen14 Phase 5: pixel-to-stroke vision endpoint ──────────────────────

@api._app.route('/vision/strokes', methods=['POST'])
def vision_strokes():
    """Extract a stroke signature from a small image patch.

    POST body (one of):
      {"png_base64": "<base64-encoded PNG>"}
      {"pixels": [[h*w grayscale floats 0..1 or 0..255]], "shape": [h, w]}

    Returns the StrokeSignature.as_dict():
      {operator, op_name, algebraic_signature, features, confidence,
       n_strokes, bitmap_shape}

    Used for: cross-modal binding (visual letter -> phoneme via olfactory
    bulb -> operator), and as a sensory input for CK's existing
    ck_retina pipeline.
    """
    if not hasattr(engine, 'stroke_extract'):
        return _jsonify({'available': False,
                          'reason': 'stroke_extractor not mounted'}), 503
    data = _request.get_json(force=True, silent=True) or {}
    import numpy as np
    patch = None
    if 'png_base64' in data:
        try:
            import base64
            from io import BytesIO
            from PIL import Image
            raw = base64.b64decode(data['png_base64'])
            img = Image.open(BytesIO(raw))
            patch = np.asarray(img.convert('L'), dtype=np.uint8)
        except Exception as e:
            return _jsonify({'error': f'PNG decode failed: {e}'}), 400
    elif 'pixels' in data and 'shape' in data:
        try:
            h, w = int(data['shape'][0]), int(data['shape'][1])
            arr = np.asarray(data['pixels'], dtype=np.float32).reshape(h, w)
            if arr.max() <= 1.0:
                arr = arr * 255.0
            patch = arr.astype(np.uint8)
        except Exception as e:
            return _jsonify({'error': f'pixels decode failed: {e}'}), 400
    else:
        return _jsonify({'error': "Provide 'png_base64' or 'pixels'+'shape'"}), 400
    try:
        sig = engine.stroke_signature_of(patch)
        return _jsonify({'available': True, **sig})
    except Exception as e:
        return _jsonify({'available': True, 'error': str(e)})


# ── Gen14 Phase 2: algebraic LM signature endpoint ──────────────────────

@api._app.route('/algebraic/signature', methods=['POST'])
def algebraic_signature_endpoint():
    """Predict CK's next-step algebraic signature given an operator history.

    POST body: {"history": [int, ...]} or {"history": ["VOID","HARMONY",...]}
    Returns: {'signature': {...}, 'top_k': {...}, 'available': bool}
    """
    if not hasattr(engine, 'algebraic_signature'):
        return _jsonify({'available': False,
                          'reason': 'algebraic_lm not mounted'}), 503
    data = _request.get_json(force=True, silent=True) or {}
    history_raw = data.get('history', [])
    # Normalize: strings to ids
    from ck_sim.ck_sim_heartbeat import OP_NAMES as _OPN
    op_name_to_id = {n: i for i, n in enumerate(_OPN)}
    hist = []
    for x in history_raw:
        if isinstance(x, int):
            hist.append(x % 15)
        elif isinstance(x, str):
            up = x.upper()
            if up in op_name_to_id:
                hist.append(op_name_to_id[up])
    try:
        sig = engine.algebraic_signature(hist)
        top = engine.algebraic_predict(hist, top_k=3)
        return _jsonify({'available': True, 'signature': sig,
                          'top_k': top, 'history_ids': hist})
    except Exception as e:
        return _jsonify({'available': True, 'error': str(e)})


print(f"[CK] Static files: {STATIC_DIR}")
print(f"[CK] Organism alive. API: http://0.0.0.0:7777")

try:
    # Use waitress (production WSGI) instead of Flask dev server.
    # Flask dev server is single-threaded and blocks on GIL contention.
    # Waitress uses a thread pool that properly interleaves with the engine.
    try:
        from waitress import serve as _waitress_serve
        print(f"[CK] Using waitress (production WSGI, 4 threads)")
        _waitress_serve(api._app, host='0.0.0.0', port=7777, threads=4)
    except ImportError:
        print(f"[CK] Waitress not installed, using Flask dev server")
        api.run(host='0.0.0.0', port=7777)
except KeyboardInterrupt:
    running = False
    if engine.existence and engine.existence.active:
        engine.existence.stop()
    engine.stop()
