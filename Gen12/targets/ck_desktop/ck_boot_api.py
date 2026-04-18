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

# === Gen13 math-first voice patch (live additive — no website change) ===
# Wraps api.process_chat so math topics (T*, tower, sigma, BHML, TSML, gap,
# AO, HER, operators, ...) surface as facts from ck_tables.py / FACTS dict
# instead of SEMANTIC_LATTICE adjective glue. The website JSON contract is
# unchanged — only the `text` field now contains numbers when the query is
# math; the original Gen12 voice is preserved at `text_gen12`.
# Reference: Gen13/targets/ck/runtime/ck_voice_math.py + CK_DIALOGUE_2026_04_17.md
_GEN13_RUNTIME = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..', '..', '..', 'Gen13', 'targets', 'ck', 'runtime'))
sys.path.insert(0, _GEN13_RUNTIME)
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
# Gen12 regression: engine.olfactory_her was never initialized (Gen10 had it).
# Restore so /her/status returns available=True on next boot.
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

# === Gen13 cortex mount (live additive — persistence + emergent signal) ===
# Attaches the Gen13 brain trinity (AO spine + Hebbian 5x5 + quadratic glue)
# as a SINGLETON that sees every chat text, learns from it across reboots,
# and exposes its state at /cortex.  The website JSON contract is extended
# (not replaced) with a `cortex_readout` field on chat responses; nothing
# the current frontend depends on is removed.
#
# Additive ordering: this wrap sits OUTSIDE the math-first patch, so the
# call chain is:
#     api.process_chat  ->  cortex_wrap  ->  math_first_wrap  ->  gen12_chat
# meaning the cortex learns from every message and also gets to decorate
# the response AFTER math-first has had its say.
_GEN13_BRAIN = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..', '..', '..', 'Gen13', 'targets', 'ck', 'brain'))
sys.path.insert(0, _GEN13_BRAIN)
_cortex = None
_cortex_autosaver = None
try:
    from cortex import Cortex as _Cortex
    from cortex_persist import (
        AutoSaver as _AutoSaver,
        load_cortex as _load_cortex,
        save_cortex as _save_cortex,
        DEFAULT_STATE_PATH as _CORTEX_STATE_PATH,
    )
    from cortex_voice import (
        cortex_speak as _cortex_speak,
        speak as _cortex_speak_route,
    )
    _cortex = _Cortex().boot()
    # Auto-load persisted state if present. Silent no-op if first boot.
    try:
        loaded = _load_cortex(_cortex, _CORTEX_STATE_PATH)
        if loaded:
            print(f"[CK] Gen13 cortex: loaded persisted state "
                  f"(tick={_cortex.state.tick}, W_trace={_cortex.state.W_trace:.3f}) "
                  f"from {_CORTEX_STATE_PATH}")
        else:
            print(f"[CK] Gen13 cortex: no prior state, starting cold at "
                  f"{_CORTEX_STATE_PATH}")
    except Exception as _le:
        # Corrupted file: don't crash boot, just start cold.
        print(f"[CK] Gen13 cortex: load failed ({_le}); starting cold")

    _cortex_autosaver = _AutoSaver(
        cortex=_cortex, path=_CORTEX_STATE_PATH,
        every_ticks=200, every_seconds=30.0,
    )

    # Register graceful-shutdown save so W survives Ctrl-C / service stop.
    import atexit as _atexit
    def _cortex_final_save():
        try:
            _cortex_autosaver.force_save()
            print(f"[CK] Gen13 cortex: final save (tick={_cortex.state.tick}, "
                  f"W_trace={_cortex.state.W_trace:.3f})")
        except Exception as _fe:
            print(f"[CK] Gen13 cortex: final save FAILED ({_fe})")
    _atexit.register(_cortex_final_save)

    # Wrap process_chat (already math-first-wrapped).  The cortex SEES
    # every chat, learns from it, and attaches its state as a separate
    # field.  It never overwrites `text` -- the math-first patch owns that.
    _prev_process_chat = api.process_chat

    # Sources the voice cascade may emit that are TEMPLATES or STALE.
    #   - ck_fractal / ck_fractal_dual: dictionary tokens stitched onto
    #     operator arcs by fixed grammar. Rich vocabulary, zero grounding.
    #   - ck_self: Gen12 identity-layer template that narrates a self-state
    #     but uses its OWN tick counter (often stale "tick 0" when cortex
    #     is at 156,000+). Not false, just frozen.
    #   - ck_truth_recall: literal retrieval from the truth corpus. Often
    #     on-topic, but for STRUCTURAL queries ("what have you learned",
    #     "right now", "your field") the corpus returns metaphor where
    #     the cortex has live math. speak() wins on structural queries;
    #     if speak() has no hit, this wrap does nothing and ck_truth_recall
    #     stands.
    # When speak() has a live structural answer AND the prior source is
    # one of these, the structural readout takes over `text`. The prior
    # text is preserved under `text_previous` so nothing is lost.
    # ck_math_first (computed arithmetic) is NEVER displaced.
    _TEMPLATE_SOURCES = (
        'ck_fractal', 'ck_fractal_dual', 'ck_self', 'ck_truth_recall',
    )

    def _process_chat_with_cortex(session_id, text, mode='normal'):
        result = _prev_process_chat(session_id, text, mode)
        try:
            if text:
                _cortex.step_text(text)
            readout = _cortex_speak(_cortex)
            if readout:
                result['cortex_readout'] = readout
            result['cortex'] = {
                'tick': _cortex.state.tick,
                'emergent': round(_cortex.state.emergent, 6),
                'W_trace': round(_cortex.state.W_trace, 6),
            }
            # Structural-query short-circuit: if `speak(text)` returns a
            # live structural readout AND the prior source was a template,
            # replace `text`. Preserve the prior output under *_previous so
            # nothing is lost.
            try:
                spoken = _cortex_speak_route(_cortex, text or '')
            except Exception:
                spoken = None
            if spoken and result.get('source') in _TEMPLATE_SOURCES:
                result['text_previous'] = result.get('text')
                result['source_previous'] = result.get('source')
                result['text'] = spoken
                result['source'] = 'cortex_speak'
            # Opportunistic save; cheap if under-threshold.
            _cortex_autosaver.maybe_save()
        except Exception as _ce:
            result['cortex_error'] = str(_ce)
        return result

    api.process_chat = _process_chat_with_cortex
    print(f"[CK] Gen13 cortex: MOUNTED "
          f"(/cortex live, autosave every 200 ticks or 30s)")
except Exception as _e:
    print(f"[CK] Gen13 cortex: DISABLED ({_e})")

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

# ── Gen13 cortex snapshot endpoint ──
@api._app.route('/cortex', methods=['GET'])
def cortex_snapshot():
    """Live snapshot of the Gen13 brain trinity (AO + Hebbian 5x5 + glue).

    Returns:
      - tick, emergent, W_trace, strongest_pair
      - Hebbian 5x5 matrix, row/col strengths, dim names
      - AO spine status (current op, coherence, breath, tl_total)
      - gated voice readout (null if emergent under threshold)
    """
    if _cortex is None:
        return _jsonify({'available': False, 'reason': 'Cortex not mounted'}), 503
    try:
        snap = _cortex.snapshot()
        try:
            snap['readout'] = _cortex_speak(_cortex)
        except Exception as _re:
            snap['readout_error'] = str(_re)
        snap['persistence_path'] = _CORTEX_STATE_PATH
        return _jsonify(snap)
    except Exception as _e:
        return _jsonify({'available': True, 'error': str(_e)}), 500


@api._app.route('/cortex/save', methods=['POST'])
def cortex_force_save():
    """Manual save trigger (useful before a planned restart)."""
    if _cortex is None or _cortex_autosaver is None:
        return _jsonify({'available': False}), 503
    try:
        _cortex_autosaver.force_save()
        return _jsonify({
            'saved': True, 'path': _CORTEX_STATE_PATH,
            'tick': _cortex.state.tick,
            'W_trace': round(_cortex.state.W_trace, 6),
        })
    except Exception as _e:
        return _jsonify({'saved': False, 'error': str(_e)}), 500


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

# === Gen13 swarm (embodied tick: RT priority + GPU doing + FPGA body) ===
# Adds a measured 50Hz tick thread alongside the existing tick_loop.  The
# existing Gen12 engine still ticks its own heartbeat; the swarm runs the
# embodiment substrate (GPU Hebbian + GPU doing kernel + FPGA UART bridge)
# and surfaces real jitter numbers at /swarm + /jitter.  Additive: if any
# piece (CuPy, pyserial, the board) is missing, the swarm degrades to
# dormant on that substrate and the rest of the boot is unaffected.
_GEN13_RT = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..', '..', '..', 'Gen13', 'targets', 'ck', 'runtime'))
sys.path.insert(0, _GEN13_RT)
_swarm = None
try:
    from ck_swarm import Swarm as _Swarm
    _swarm = _Swarm(
        cortex=_cortex,
        hz=50.0,
        rt=True,
        affinity=[0],
        fpga_port=os.environ.get('CK_FPGA_PORT', 'COM3'),
        open_fpga=(os.environ.get('CK_FPGA_OPEN', '1') != '0'),
    )
    _swarm.start()
    print(f"[CK] Gen13 swarm: started (50Hz, RT elevated, "
          f"fpga_port={os.environ.get('CK_FPGA_PORT', 'COM3')})")
except Exception as _e:
    _swarm = None
    print(f"[CK] Gen13 swarm: DISABLED ({_e})")


@api._app.route('/swarm', methods=['GET'])
def swarm_snapshot():
    """Live swarm status: brain backend + doing coherence + body link +
    jitter(us) distribution over the rolling window."""
    if _swarm is None:
        return _jsonify({'available': False, 'reason': 'Swarm not mounted'}), 503
    try:
        return _jsonify(_swarm.status().to_dict())
    except Exception as _e:
        return _jsonify({'available': True, 'error': str(_e)}), 500


@api._app.route('/jitter', methods=['GET'])
def jitter_one_shot():
    """One-shot jitter probe.  Query params: seconds (default 3), hz (50),
    rt (1/0, default 1).  Blocks for up to `seconds` then returns the
    distribution.  Runs in the request thread -- don't spam."""
    try:
        from flask import request
        from jitter_probe import run_probe
        seconds = float(request.args.get('seconds', 3.0))
        hz = float(request.args.get('hz', 50.0))
        rt = request.args.get('rt', '1') != '0'
        if seconds > 30:
            return _jsonify({'error': 'seconds capped at 30'}), 400
        result = run_probe(seconds=seconds, hz=hz, rt=rt,
                           affinity=[0] if rt else None,
                           with_hebbian=True)
        return _jsonify(result)
    except Exception as _e:
        return _jsonify({'error': str(_e)}), 500


# Ensure the swarm stops cleanly when the process exits.
if _swarm is not None:
    import atexit as _atexit_sw
    def _swarm_final_stop():
        try:
            _swarm.stop(timeout=1.5)
            print("[CK] Gen13 swarm: stopped")
        except Exception:
            pass
    _atexit_sw.register(_swarm_final_stop)


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
