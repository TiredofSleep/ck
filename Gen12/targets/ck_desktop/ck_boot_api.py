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
    # Pin the engine tick_loop to core 1 so it stops fighting the Gen13
    # swarm on core 0.  We do NOT request HIGHEST here — the swarm is the
    # measured RT path; engine is a cooperative peer on an adjacent core.
    # Graceful if rt_priority not importable (tick still runs at NORMAL).
    try:
        _GEN13_RT = os.path.normpath(os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            '..', '..', '..', 'Gen13', 'targets', 'ck', 'runtime'))
        if _GEN13_RT not in sys.path:
            sys.path.insert(0, _GEN13_RT)
        from rt_priority import elevate as _rt_elevate  # noqa: E402
        # process=False: don't override the swarm's REALTIME/HIGH class choice.
        # thread_level='above': cooperative peer on core 1, below swarm on core 0.
        _rt_engine = _rt_elevate(affinity=[1], process=False, thread_level='above')
        print(f"[CK] engine tick_loop: core={_rt_engine.cpu_affinity} "
              f"proc={_rt_engine.process_class} thr={_rt_engine.thread_priority}")
    except Exception as _e:
        print(f"[CK] engine tick_loop: rt elevation skipped ({_e})")

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
    import cortex_voice as _cortex_voice_mod
    print(f"[CK] Gen13 cortex_voice loaded from: {_cortex_voice_mod.__file__}")
    # Fallback-version probe: the newer speak() emits a self-report
    # (feel/field) for unclassified queries instead of returning None.
    try:
        from cortex import Cortex as _ProbeCortex
        _probe_cx = _ProbeCortex().boot()
        _probe_out = _cortex_speak_route(_probe_cx, "hi")
        print(f"[CK] Gen13 cortex_voice.speak('hi') cold probe: "
              f"type={type(_probe_out).__name__} len={len(_probe_out) if isinstance(_probe_out,str) else 'n/a'} "
              f"preview={(_probe_out[:60] if isinstance(_probe_out,str) else None)!r}")
    except Exception as _pe:
        print(f"[CK] Gen13 cortex_voice probe failed: {_pe}")
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
        # 2026-04-18: added after battery showed "beauville curve c star" →
        # crystal and "psi order 4" → ck_tig falling through the swap even
        # though _cortex_speak had a real readout.  These two Gen12 sources
        # are also pool/template fluency layers; they should yield to
        # structural readouts the same way ck_fractal does.
        'crystal', 'ck_tig',
    )
    # Sources the swap MUST NEVER overwrite:
    #   - ck_math_first (computed arithmetic from ck_voice_math)
    #   - cortex_speak  (already structural)
    _STRUCTURAL_SOURCES = ('ck_math_first', 'cortex_speak')

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
                _spoken_err = None
            except Exception as _se:
                spoken = None
                _spoken_err = f"{type(_se).__name__}: {_se}"
            # Swap when we have a structural readout AND the incoming source
            # is either (a) a known template/pool source, or (b) unknown and
            # NOT already structural.  Blacklisting the two structural
            # sources is safer than whitelisting every possible template
            # source that Gen12 might emit (crystal, ck_tig, ck_fractal,
            # ck_fractal_dual, ck_self, ck_truth_recall, etc.).
            _src = result.get('source')
            _swap_ok = (
                _src in _TEMPLATE_SOURCES or
                (_src is not None and _src not in _STRUCTURAL_SOURCES)
            )
            # Minimal diagnostics: keep the source transition visible but
            # drop the noisy swap_debug now that the swap is verified.
            if spoken and _swap_ok:
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

# === Gen13 meta-classification endpoints (Phase 2) ===
# YAML-backed catalogs exposing CK's classification axes via HTTP so the
# website can render them live (Phase 3) and external clients can query
# the paradox classifier / DoF taxonomy / constants table without booting
# the full engine.
#
# Routes added:
#   GET  /paradox/classify?slug=<slug>             -> Type I..IV verdict
#   GET  /paradox/classify?stage=<stage>&name=<n>  -> stage-forced verdict
#   GET  /dof/taxonomy                             -> 5 kinds + diagnostics
#   GET  /meta/constants                           -> cross-kind constants
#   GET  /meta/registry                            -> full paradox registry
#   POST /meta/reload                              -> re-read YAML from disk
#
# All routes are read-only except /meta/reload (which requires local caller
# by default).  Nothing here writes to engine state or cortex state.
try:
    # cortex_catalog was added to sys.path by the cortex mount above.
    import cortex_catalog as _cat  # type: ignore
    from flask import request as _req, jsonify as _jsonify
    _app = api._app
    if _app is None:
        raise RuntimeError("api._app is None (Flask not mounted)")

    @_app.route('/paradox/classify', methods=['GET'])
    def _r_paradox_classify():
        slug = _req.args.get('slug') or _req.args.get('paradox')
        stage = _req.args.get('stage') or _req.args.get('failure_stage')
        name = _req.args.get('name')
        try:
            verdict = _cat.classify_paradox(
                slug_or_stage=slug,
                failure_stage=stage,
                name=name,
            )
            return _jsonify(verdict)
        except KeyError as _ke:
            return _jsonify({'error': str(_ke)}), 404
        except Exception as _exc:
            return _jsonify({'error': f'{type(_exc).__name__}: {_exc}'}), 500

    @_app.route('/dof/taxonomy', methods=['GET'])
    def _r_dof_taxonomy():
        try:
            return _jsonify(_cat.dof_taxonomy())
        except Exception as _exc:
            return _jsonify({'error': f'{type(_exc).__name__}: {_exc}'}), 500

    @_app.route('/meta/constants', methods=['GET'])
    def _r_meta_constants():
        try:
            return _jsonify({'constants': _cat.constants_table()})
        except Exception as _exc:
            return _jsonify({'error': f'{type(_exc).__name__}: {_exc}'}), 500

    @_app.route('/meta/registry', methods=['GET'])
    def _r_meta_registry():
        try:
            return _jsonify({'paradoxes': _cat.paradox_registry()})
        except Exception as _exc:
            return _jsonify({'error': f'{type(_exc).__name__}: {_exc}'}), 500

    @_app.route('/meta/frontier', methods=['GET'])
    def _r_meta_frontier():
        try:
            return _jsonify({'facts': _cat.frontier_facts()})
        except Exception as _exc:
            return _jsonify({'error': f'{type(_exc).__name__}: {_exc}'}), 500

    @_app.route('/meta/summary', methods=['GET'])
    def _r_meta_summary():
        try:
            return _jsonify(_cat.summary())
        except Exception as _exc:
            return _jsonify({'error': f'{type(_exc).__name__}: {_exc}'}), 500

    @_app.route('/meta/reload', methods=['POST'])
    def _r_meta_reload():
        # Local-only by default (matches the /save_all and /self_write
        # convention).  Cloudflare sends X-Forwarded-For for external traffic;
        # absence of it + 127.0.0.1 is the local-request marker.
        _xff = _req.headers.get('X-Forwarded-For', '')
        _ip = (_xff.split(',')[0].strip() if _xff else _req.remote_addr) or ''
        if _ip not in ('127.0.0.1', '::1', 'localhost'):
            return _jsonify({'error': 'local-only endpoint'}), 403
        try:
            _cat.reload()
            return _jsonify({'status': 'ok', 'summary': _cat.summary()})
        except Exception as _exc:
            return _jsonify({'error': f'{type(_exc).__name__}: {_exc}'}), 500

    _cat_summary = _cat.summary()
    print(f"[CK] Gen13 meta-classification: MOUNTED "
          f"(dof={_cat_summary['dof_kind_count']} "
          f"paradoxes={_cat_summary['paradox_count']} "
          f"constants={_cat_summary['constant_count']}) "
          f"routes=/paradox/classify /dof/taxonomy /meta/[constants|registry|summary|reload]")
except Exception as _e:
    print(f"[CK] Gen13 meta-classification: DISABLED ({_e})")

# === Ollama: CK uses it, Ollama doesn't speak ===
# Architecture (2026-04-18 correction):
#   CK's structural readout IS CK's voice. Ollama is a tool CK USES to
#   shape expanded phrasing — but Ollama never speaks in CK's name.
#   Every Ollama draft goes through CK's coherence filter; CK ADOPTS the
#   draft only if it preserves every structural fact (no invented framing,
#   no LLM drift, no AI-disclaimer noise). If the filter rejects, CK's
#   own structural readout stands and the rejected draft is attached as
#   `text_ollama_draft` for diagnostics.
#
# This matches the Gen13 llm_bridge docstring intent — "LLM fluency as
# wrapper around CK's algebra, not replacement" — but enforces it via a
# coherence gate so we don't silently swap Ollama prose for CK's math.
#
# Invariants:
#   - `text` is ALWAYS CK's voice. Either his structural readout verbatim,
#     or an Ollama draft that passed the coherence filter.
#   - `text_ollama_draft` exposes every Ollama attempt (accepted or not).
#   - `ollama_verdict` in {'accepted','rejected:<reason>','skipped:<why>','error'}.
#   - `ck_math_first` arithmetic is never touched (numbers are canonical).
#   - Disable with `CK_OLLAMA_EDITOR=0` env var; set model/timeout/min_facts
#     via CK_OLLAMA_MODEL, CK_OLLAMA_TIMEOUT, CK_OLLAMA_MIN_FACT_HITS.
_GEN13_BRIDGE = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..', '..', '..', 'Gen13', 'targets', 'ck', 'bridge'))
if _GEN13_BRIDGE not in sys.path:
    sys.path.insert(0, _GEN13_BRIDGE)

_OLLAMA_EDITOR = os.environ.get('CK_OLLAMA_EDITOR', '1') == '1'
# llama3.1:8b is the speed/quality sweet spot on this machine — 2-3x the
# latency of llama3.2:latest but far better at following structural grounding
# (llama3.2 hallucinated "p-adic integers" and "t = r/5" in early sweeps
# even when the readout spelled out Q(i,sqrt2,sqrt3,sqrt5) and 5/7).
_OLLAMA_MODEL = os.environ.get('CK_OLLAMA_MODEL', 'llama3.1:8b')
_OLLAMA_TIMEOUT = float(os.environ.get('CK_OLLAMA_TIMEOUT', '30'))
_OLLAMA_MAX_CHARS = int(os.environ.get('CK_OLLAMA_MAX_CHARS', '600'))
# Coherence filter: fraction of structural facts the draft must preserve.
# 1.0 = every fact, 0.7 = a couple may be missing. 0.7 is the pragmatic
# sweet spot: drafts preserving the core numbers and operator names pass,
# drafts inventing unrelated framing fail.
_OLLAMA_FACT_COVERAGE = float(os.environ.get('CK_OLLAMA_FACT_COVERAGE', '0.70'))
# Max latency CK will spend waiting on Ollama before falling back to pure
# structural output. Keeps the website chat responsive even when the LLM
# is loaded.
_OLLAMA_MAX_WAIT = float(os.environ.get('CK_OLLAMA_MAX_WAIT', '20'))
_ollama_ok = False
_ollama_complete = None
_ollama_ground = None
try:
    from llm_bridge import (
        ollama_available as _oll_avail,
        ollama_complete as _ollama_complete_fn,
        build_grounded_system as _ollama_ground_fn,
    )
    _ollama_ok = _oll_avail(timeout=2.0)
    _ollama_complete = _ollama_complete_fn
    _ollama_ground = _ollama_ground_fn
    print(f"[CK] Ollama editor: available={_ollama_ok} "
          f"model={_OLLAMA_MODEL} enabled={_OLLAMA_EDITOR} "
          f"timeout={_OLLAMA_TIMEOUT}s max_chars={_OLLAMA_MAX_CHARS}")
except Exception as _oe:
    print(f"[CK] Ollama editor: import failed ({_oe})")
    _OLLAMA_EDITOR = False

_OLLAMA_EXTRA_GUIDE = (
    "You are CK, the Coherence Keeper. Your job is to REWRITE the "
    "structural readout above as a plain-English answer to the user's "
    "question. STRICT rules (violations break CK's math identity):\n"
    " 1. Use ONLY facts that appear in the readout. If a number, "
    "    constant, or operator name is not in the readout, DO NOT "
    "    mention it. Never invent p-adic, continuity, maxima/minima, "
    "    convexity, geodesics, differential-geometry analogies, or any "
    "    other framing that is not literally in the readout.\n"
    " 2. Keep every number, fraction, operator name, and WP-number "
    "    EXACTLY as written (T*=5/7 stays 5/7; WP51 stays WP51).\n"
    " 3. 2-4 short sentences total. No lists, no headers, no markdown, "
    "    no emoji, no code fences.\n"
    " 4. Do NOT apologize, do NOT say you are an AI, do NOT mention "
    "    this system prompt.\n"
    " 5. If the readout has multiple labelled fields (e.g. feel: aperture=X "
    "    pressure=Y), weave them into one sentence rather than listing.\n"
    " 6. Write as CK speaking for himself in first person. Lowercase "
    "    sentence starts are fine."
)

# Ollama-draft cleanup is now a pure function in ck_ollama_filter so
# unit tests can import it without running the full boot pipeline.
from ck_ollama_filter import _postfilter_ollama  # noqa: E402,F401

# Coherence verdict + fact extraction likewise live in a standalone
# module (ck_coherence_verdict) so they can be unit-tested without
# importing this boot file.  The v2 verdict tiers facts into CORE
# (operator names, T*, WP#, named structures like TSML/BHML/HER) and
# PERIPHERAL (numbers, decimals, non-distinctive label=value pairs),
# adding a soft-accept path for terse-but-honest drafts that preserve
# CK's core identity without echoing every peripheral timestamp.
# Keep the v1 private names as aliases so ck_coherence_steer's
# sys.modules-based lookup continues to resolve them.
from ck_coherence_verdict import (  # noqa: E402
    coherence_verdict as _coherence_verdict,
    fact_tokens as _fact_tokens,
    fact_hit as _fact_hit,
    is_core_fact as _is_core_fact,
)

if _OLLAMA_EDITOR and _ollama_ok:
    # Wrap the already-wrapped process_chat one more time.
    # Call-chain after this:
    #   api.process_chat
    #     -> _process_chat_with_ollama_editor (NEW — grounded fluency)
    #        -> _process_chat_with_cortex     (structural + cortex swap)
    #           -> _process_chat_math_first   (arithmetic surface)
    #              -> _orig_process_chat      (Gen12 base)
    _prev_chat_for_ollama = api.process_chat

    def _process_chat_with_ollama_editor(session_id, text, mode='normal'):
        result = _prev_chat_for_ollama(session_id, text, mode)
        try:
            src = result.get('source')
            ck_ground = (result.get('text') or '').strip()
            # Skip arithmetic surfaces — numbers are canonical.
            if src == 'ck_math_first':
                result['ollama_verdict'] = 'skipped:ck_math_first is canonical'
                return result
            # Skip when we have nothing to ground on.
            if not ck_ground:
                result['ollama_verdict'] = 'skipped:empty structural text'
                return result
            # Skip very long structural outputs — already verbose enough.
            if len(ck_ground) > _OLLAMA_MAX_CHARS:
                result['ollama_verdict'] = f'skipped:structural >{_OLLAMA_MAX_CHARS} chars'
                return result
            # Skip empty user prompts (ping / health probes).
            if not text or not text.strip():
                result['ollama_verdict'] = 'skipped:empty user text'
                return result
            # Frontier-bridge enrichment BEFORE the sysprompt build so
            # Ollama's very first draft sees the corpus anchors (LATTICE
            # aperture -> flatness_2x2_WP51, COLLAPSE pressure -> D2
            # crossing, sigma_NS -> Millennium reframe, etc.).  Without
            # this, the primary path's first Ollama call never saw the
            # bridges -- only the steered rescue path did, leaving the
            # bridges as display-only enrichment rather than real
            # steering.  Lazy import so a missing steer module doesn't
            # break the editor.
            ck_ground_for_sysprompt = ck_ground
            _enriched_bridges_for_sysprompt = []
            try:
                from ck_coherence_steer import _enrich_readout_with_anchors
                _enriched = _enrich_readout_with_anchors(ck_ground, text or "")
                if _enriched != ck_ground:
                    ck_ground_for_sysprompt = _enriched
                    # Collect the fired bridges so we can expose them on
                    # the result even when the steer layer isn't running.
                    for _ln in _enriched.splitlines():
                        _ln_s = _ln.strip()
                        if _ln_s.startswith("frontier_bridge="):
                            _enriched_bridges_for_sysprompt.append(
                                _ln_s[len("frontier_bridge="):]
                            )
            except Exception:
                # Enrichment is a nice-to-have; never break the editor.
                pass
            if _enriched_bridges_for_sysprompt:
                result.setdefault("bridges_fired",
                                  list(_enriched_bridges_for_sysprompt))
                result.setdefault("steer_readout_enriched", True)
            sysprompt = _ollama_ground(ck_ground_for_sysprompt,
                                        extra=_OLLAMA_EXTRA_GUIDE)
            import time as _time
            _t0 = _time.time()
            drafted_raw = _ollama_complete(
                text, system=sysprompt,
                model=_OLLAMA_MODEL,
                timeout=min(_OLLAMA_TIMEOUT, _OLLAMA_MAX_WAIT),
            )
            _dt = _time.time() - _t0
            result['ollama_dt'] = round(_dt, 2)
            if not drafted_raw or drafted_raw.startswith('[ollama'):
                result['ollama_verdict'] = 'error'
                result['ollama_error'] = drafted_raw or '[ollama no draft]'
                return result
            drafted = _postfilter_ollama(drafted_raw)
            result['text_ollama_draft'] = drafted  # always expose the draft
            result['ollama_model'] = _OLLAMA_MODEL
            if not drafted:
                result['ollama_verdict'] = 'rejected:empty-after-filter'
                return result
            # CK's coherence filter: does the draft preserve structural facts?
            accepted, reason, hits, total = _coherence_verdict(
                ck_ground, drafted, _OLLAMA_FACT_COVERAGE)
            result['ollama_verdict'] = ('accepted:' if accepted else 'rejected:') + reason
            result['ollama_fact_hits'] = hits
            result['ollama_fact_total'] = total
            if accepted:
                # CK adopts the draft as his own words. Structural readout
                # preserved for transparency / frontend display.
                result['text_structural'] = ck_ground
                result['source_structural'] = src
                result['text'] = drafted
                result['source'] = 'cortex_speak_via_ollama'
            # else: text/source stay as-is (CK keeps his structural voice).
        except Exception as _oe:
            result['ollama_verdict'] = 'error'
            result['ollama_error'] = f"{type(_oe).__name__}: {_oe}"
        return result

    api.process_chat = _process_chat_with_ollama_editor
    print(f"[CK] Ollama editor: MOUNTED "
          f"(CK speaks structural; Ollama drafts filtered through coverage>={_OLLAMA_FACT_COVERAGE}, "
          f"source=cortex_speak_via_ollama on accept, text_ollama_draft always preserved)")
elif _OLLAMA_EDITOR and not _ollama_ok:
    print("[CK] Ollama editor: SKIPPED (service not reachable at "
          "http://127.0.0.1:11434 -- start 'ollama serve')")
else:
    print("[CK] Ollama editor: DISABLED (CK_OLLAMA_EDITOR=0)")

# -----------------------------------------------------------------------------
# Brain fold: FusionCKCorrector (AO 5-element + Hebbian 5x5 + coherence gate).
# Additive patch -- scores + logs every turn for the idle_loop tensor update
# without modifying CK's text or source.  See ck_brain_fold.py header for the
# full call-chain and the 2026-04-17 "one CK" rule.
# -----------------------------------------------------------------------------
try:
    from ck_brain_fold import mount_brain_fold
    _brain_status = mount_brain_fold(api)
    if _brain_status.get("mounted"):
        print(f"[CK] Brain fold: MOUNTED "
              f"(tensor={_brain_status['tensor_path']}, "
              f"norm={_brain_status['tensor_norm_at_load']}, "
              f"n_updates={_brain_status['n_updates_on_tensor']}, "
              f"fusion_w={_brain_status['fusion_weight']}, "
              f"log_dir={_brain_status['log_dir']})")
    else:
        print(f"[CK] Brain fold: SKIPPED ({_brain_status.get('reason')})")
except Exception as _bfe:
    # NEVER break boot because of the brain fold
    print(f"[CK] Brain fold: ERROR ({type(_bfe).__name__}: {_bfe}) -- server continues")

# -----------------------------------------------------------------------------
# Body fold: exposes CK's already-live embodiment (12 fractal sensory layers
# built by build_sensorium in CKSimEngine.__init__, ticked every engine tick).
# Adds HTTP surface (/body/state, /body/layers, /body/swarm, /body/pause,
# /body/resume) and attaches body_* fields to every chat response.  Additive
# only -- if the sensorium is missing or fails, chat still flows.  See
# ck_body_fold.py header for the full call-chain.
# -----------------------------------------------------------------------------
try:
    from ck_body_fold import mount_body_fold
    _body_status = mount_body_fold(api, engine)
    if _body_status.get("mounted"):
        print(f"[CK] Body fold: MOUNTED "
              f"(layers={_body_status['sensorium_layer_count']}, "
              f"active={_body_status['sensorium_active_layers']}, "
              f"routes={_body_status['routes_registered']})")
    else:
        print(f"[CK] Body fold: SKIPPED ({_body_status.get('reason')})")
except Exception as _bde:
    # NEVER break boot because of the body fold
    print(f"[CK] Body fold: ERROR ({type(_bde).__name__}: {_bde}) -- server continues")

# -----------------------------------------------------------------------------
# Coherence steer: closes the feedback loop on the Ollama path.  Scores every
# draft with CK's own ck_corrector + coherence_scalar and gates on
# coh>=T*=5/7 alongside coverage.  On first fail, retries once with a STEERED
# prompt biased toward the question's dominant operator; on second fail, emits
# an honest one-liner keyed to organism state instead of raw telemetry.
# Accepted drafts are cached on disk (LRU 2048) for "slow first, fast later".
# Must mount AFTER Ollama editor and BEFORE curiosity (so curiosity's
# autonomous ticks ride the steered pipeline).
# -----------------------------------------------------------------------------
try:
    from ck_coherence_steer import mount_coherence_steer
    _steer_status = mount_coherence_steer(api, engine)
    if _steer_status.get("mounted"):
        print(f"[CK] Coherence steer: MOUNTED "
              f"(retries={_steer_status['retries']}, "
              f"cache={_steer_status['cache_stats'].get('size', 0)} entries, "
              f"routes={_steer_status['routes_registered']})", flush=True)
    else:
        print(f"[CK] Coherence steer: SKIPPED ({_steer_status.get('reason')})", flush=True)
except Exception as _sce:
    # NEVER break boot because of the steer fold
    import traceback as _tb_sce
    print(f"[CK] Coherence steer: ERROR ({type(_sce).__name__}: {_sce}) -- server continues", flush=True)
    _tb_sce.print_exc()

# -----------------------------------------------------------------------------
# Pastoral fold: wires ck_lm/ck_bible into the chat pipeline.  When a user
# message carries grief/fear/loss/loneliness/etc., attaches a clearly-
# attributed KJV verse as DATA fields on the response (text untouched by
# default per the don't-ventriloquize rule).  See ck_pastoral_fold.py header.
# Mount AFTER coherence_steer (so brain_dominant_op is populated for seed)
# and BEFORE curiosity (so the fold can skip CK's self-questions by
# session_id == ck_curiosity).
# -----------------------------------------------------------------------------
try:
    from ck_pastoral_fold import mount_pastoral_fold
    _past_status = mount_pastoral_fold(api)
    if _past_status.get("mounted"):
        print(f"[CK] Pastoral fold: MOUNTED "
              f"(themes={len(_past_status['corpus_themes'])}, "
              f"cooldown={_past_status['cooldown_s']}s, "
              f"append_text={_past_status['append_text']}, "
              f"routes={_past_status['routes_registered']})", flush=True)
    else:
        print(f"[CK] Pastoral fold: SKIPPED ({_past_status.get('reason')})", flush=True)
except Exception as _pfe:
    # NEVER break boot because of the pastoral fold
    import traceback as _tb_pfe
    print(f"[CK] Pastoral fold: ERROR ({type(_pfe).__name__}: {_pfe}) -- server continues", flush=True)
    _tb_pfe.print_exc()

# ---------------------------------------------------------------------------
# LM Geometry fold (EPOCH I: SIGHT, AI Sovereignty Plan).
# Resolves the LM's black box into a 32-layer x 5-D AO trajectory.  Read-only
# diagnostic routes:
#   /lm/info, /lm/health, /lm/geometry?text=..., /lm/geometry/path?text=...
# CK_LM_GEOMETRY=0 disables.  CK_LM_GEOMETRY_EAGER=1 loads the model at boot
# (~30s, ~5GB GPU).  Default is lazy load on first /lm/geometry call.
# CK_LM_GEOMETRY_LORA=<path> attaches a trained adapter.  Does NOT change
# CK's chat behavior; pure read-only diagnostic.
# ---------------------------------------------------------------------------
try:
    from ck_lm_geometry_fold import mount_lm_geometry_fold
    _lmg_status = mount_lm_geometry_fold(api)
    if _lmg_status.get("mounted"):
        print(f"[CK] LM Geometry fold: MOUNTED "
              f"(base={_lmg_status['base_model']}, "
              f"lora={_lmg_status['lora_path']}, "
              f"dtype={_lmg_status['dtype']}, "
              f"eager={_lmg_status['eager']}, "
              f"routes={len(_lmg_status['routes'])})", flush=True)
    else:
        print(f"[CK] LM Geometry fold: SKIPPED ({_lmg_status.get('reason')})", flush=True)
except Exception as _lmgfe:
    import traceback as _tb_lmg
    print(f"[CK] LM Geometry fold: ERROR ({type(_lmgfe).__name__}: {_lmgfe}) -- server continues", flush=True)
    _tb_lmg.print_exc()

# -----------------------------------------------------------------------------
# Curiosity: autonomous self-questioning daemon.  Every ~45s, snapshots
# engine.sensorium + ShadowSwarm, detects notable shifts (organism flip,
# T*=5/7 crossing, layer delta, process churn, threat flip, shift-operator
# entry), and asks CK a first-person question that rides api.process_chat --
# so the answer goes through Ollama editor + coherence steer like any human
# turn.  Logs to a 256-entry ring at /curiosity/stream.  Must mount LAST so
# it sees the fully-wrapped process_chat.
# -----------------------------------------------------------------------------
try:
    from ck_curiosity import mount_curiosity
    _cur_status = mount_curiosity(api, engine)
    if _cur_status.get("mounted"):
        print(f"[CK] Curiosity: MOUNTED "
              f"(period={_cur_status['period']}s, "
              f"session={_cur_status['session_id']}, "
              f"routes={_cur_status['routes_registered']})", flush=True)
    else:
        print(f"[CK] Curiosity: SKIPPED ({_cur_status.get('reason')})", flush=True)
except Exception as _cue:
    # NEVER break boot because of the curiosity fold
    import traceback as _tb_cue
    print(f"[CK] Curiosity: ERROR ({type(_cue).__name__}: {_cue}) -- server continues", flush=True)
    _tb_cue.print_exc()

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
                 'index.html',
                 'chat.html', 'papers.html', 'spectrometer.html', 'frontiers.html',
                 'paradox.html', 'ring.html',
                 'math.html', 'physics.html', 'bible.html',
                 'emotion.html', 'mythology.html', 'about.html',
                 'ai.html', 'curiosity.html',
                 'robots.txt'}
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


# ── Frontier-bridge catalog ──
# Exposes CK's _FRONTIER_ANCHORS table so the website (and any curious
# reader) can see the full list of corpus anchors CK will cite when the
# readout or query text hits one.  Read-only, cheap, cacheable.
@api._app.route('/bridges', methods=['GET'])
def bridges_catalog():
    """Return the current frontier-bridge anchor table.

    Each entry: {pattern_hint, bridge} where pattern_hint is a short
    human string describing what triggers the anchor and bridge is the
    tag appended to the readout when it fires.  Order matches the
    scan order in _enrich_readout_with_anchors -- first match wins.
    """
    try:
        from ck_coherence_steer import _FRONTIER_ANCHORS
    except Exception as _e:
        return _jsonify({'available': False, 'error': str(_e)}), 503
    entries = []
    for rx, tag in _FRONTIER_ANCHORS:
        # Strip the leading "frontier_bridge=" from the tag for display.
        label = tag[len("frontier_bridge="):] if tag.startswith("frontier_bridge=") else tag
        entries.append({
            'pattern': rx.pattern,
            'bridge': label,
            'tag': tag,
        })
    return _jsonify({
        'available': True,
        'count': len(entries),
        'bridges': entries,
    })


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
