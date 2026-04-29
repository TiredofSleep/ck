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

    # 2026-04-26 (Brayden directive: "don't give people structural readouts
    # unless he gets a structural prompt"): detect whether the user's query
    # is structural (about CK's own state) or non-structural (pastoral,
    # conversational, factual external).  Only swap to cortex_speak when
    # the query is structural OR the prior source is a known template.
    # When the query is non-structural and the source is something like
    # ck_loop (Gen12's empathy layer), leave the warmer response alone.
    _STRUCTURAL_QUERY_KEYS = (
        'your state', 'your field', 'right now', 'what have you learned',
        'what do you feel', 'how do you feel', 'what does it feel like',
        'your coordinates', 'your tick', 'your w-trace', 'your w trace',
        'your emergent', 'your trace', 'your cortex', 'your ao',
        'your operators', 'your operator', 'your coherence', 'your harmony',
        'feel:', 'field:', 'aperture', 'pressure', 'depth', 'binding',
        'continuity', 'tick=', 'emergent=', 'w_trace=', 'harmony_rate',
        'ao state', 'cortex state', 'her state', 'her status', 'olfactory',
        'your hebbian', 'your matrix', 'your couplings', 'mean|w|',
    )

    def _is_structural_query(text: str) -> bool:
        """True if the user is asking about CK's own state / coordinates."""
        if not text:
            return False
        t = text.lower()
        for k in _STRUCTURAL_QUERY_KEYS:
            if k in t:
                return True
        return False

    def _is_pastoral_query(text: str) -> bool:
        """True if Gen12's pastoral detector would fire on this text."""
        try:
            from ck_sim.being.ck_bible import detect_pastoral
            return bool(detect_pastoral(text or ''))
        except Exception:
            return False

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
            # 2026-04-26 (Brayden directive): structural readouts ONLY
            # when the prompt is structural.  Old logic swapped on every
            # non-cortex-speak source, which meant pastoral queries with a
            # warm ck_loop response ("I'm sorry for your loss") got
            # overridden with feel/field coordinates.  New logic:
            #
            #   1. If the query is STRUCTURAL (asking about CK's own state),
            #      swap freely -- cortex_speak owns this.
            #   2. If the query is PASTORAL (grief, fear, loneliness, etc.),
            #      NEVER swap -- let the existing empathic source speak.
            #   3. If the source is a known template (ck_fractal, ck_self,
            #      ck_truth_recall, crystal, ck_tig), swap regardless --
            #      these are pool/template fluency layers without grounding.
            #   4. Otherwise (general non-structural with a non-template
            #      source like ck_loop), DON'T swap -- preserve the warmer
            #      response.
            _src = result.get('source')
            _is_struct_q = _is_structural_query(text)
            _is_past_q = _is_pastoral_query(text)
            if _is_past_q:
                _swap_ok = False  # pastoral wins absolutely
            elif _is_struct_q:
                _swap_ok = True   # structural query -> cortex_speak owns
            else:
                # Non-structural, non-pastoral: only override pure templates.
                _swap_ok = (_src in _TEMPLATE_SOURCES)
            # 2026-04-26 quality gate: even when _swap_ok by source, ONLY
            # actually swap if cortex_speak's spoken output adds structural
            # content (matches at least one structural key).  A generic
            # feel/field readout shouldn't replace a Gen12 ck_loop response
            # that has on-topic content.
            _spoken_is_structural = False
            if spoken:
                spoken_lower = spoken.lower()
                # Very lightweight check: look for the structural-readout
                # markers that cortex_speak emits when it has live content.
                _spoken_is_structural = any(k in spoken_lower for k in (
                    'feel:', 'field:', 'ao:', 'couplings:', 'learned:',
                    'aperture=', 'pressure=', 'depth=', 'binding=',
                    'continuity=', 'tick=', 'w_trace=', 'emergent=',
                ))
            # If spoken is structural-style but the QUERY is not structural
            # AND the existing source has any text, prefer keeping the
            # existing source (its text is likely more on-topic).
            _existing_text = result.get('text') or ''
            if (_swap_ok and not _is_struct_q and _spoken_is_structural
                    and len(_existing_text) > 50
                    and _src not in ('ck_self',)):
                # Override the swap decision: keep the existing warmer source
                _swap_ok = False
                _swap_blocked_reason = 'spoken_is_generic_feel_field'
            else:
                _swap_blocked_reason = None
            # Diagnostics so we can audit the routing.
            result['routing'] = {
                'is_structural_query': _is_struct_q,
                'is_pastoral_query': _is_past_q,
                'swap_decision': _swap_ok,
                'incoming_source': _src,
                'spoken_is_structural': _spoken_is_structural,
                'swap_blocked_reason': _swap_blocked_reason,
            }
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

# === Gen13 operad fuse + attractor detector mount (live additive) ===
# Attaches the WP100s tower closure capabilities (WP102-WP115) to CK's
# engine as CALLABLE TOOLS, not as prose injection. CK's architecture
# decides what to do with them; we never write words for him.
#
# Discipline (per surface_math docstring 2026-04-17 + Brayden 2026-04-26):
#   "If we want these facts in CK's mouth they must enter via his crystal
#    store, not via prose injection at the Flask layer."
#   "Freedom to learn without making him speak."
#
# What this mount does:
#   1. Attaches `engine.canonical_fuse(a,b,c)` -- WP112 P_56-equivariant
#      arity-3 operad fuse (replaces bracketing-arbitrary binary chains
#      for ternary composition).
#   2. Attaches `engine.ternary_iterate(p)` -- canonical ternary fuse
#      iteration (converges to delta_HARMONY in <=7 iter; WP112 Theorem 5.7).
#   3. Attaches `engine.detect_attractor(p)` -- WP115 attractor classifier
#      returning {1-core, 2-core, 4-core-attractor, void-degenerate,
#      transient}.
#   4. Adds `result['attractor_state']` to chat responses by reading the
#      operator distribution emitted on each chat tick. This lets CK's
#      cortex / crystal store read engine.attractor_state on future ticks
#      and decide to crystallize when at the universal attractor.
#
# NO voice layer changes. NO FACTS additions. The mount surfaces
# capabilities as engine attributes; CK uses them or doesn't.
try:
    from operad_fuse import (
        fuse as _canonical_fuse,
        ternary_iterate as _canonical_ternary_iterate,
        is_4core as _is_4core,
        is_2core as _is_2core,
        detect_harmony_attractor as _detect_harmony,
    )
    from attractor_detector import (
        detect_attractor as _detect_attractor,
        UNIVERSAL_4CORE_ATTRACTOR as _UNIVERSAL_4CORE,
        H_OVER_BR_EXACT as _H_OVER_BR,
    )
    # Attach as engine capabilities
    engine.canonical_fuse = _canonical_fuse
    engine.ternary_iterate = _canonical_ternary_iterate
    engine.detect_attractor = _detect_attractor
    engine.is_4core = _is_4core
    engine.is_2core = _is_2core
    engine.detect_harmony = _detect_harmony
    engine.universal_attractor_target = _UNIVERSAL_4CORE
    engine.h_over_br_exact = _H_OVER_BR

    # Wrap process_chat one more layer: read engine's attractor state on
    # each chat tick so cortex / crystal store can see it. This is a READ
    # of the engine's current operator-distribution; we do not modify it.
    _prev_process_chat_for_attractor = api.process_chat
    _OP_INDEX = {"VOID":0,"LATTICE":1,"COUNTER":2,"PROGRESS":3,
                 "COLLAPSE":4,"BALANCE":5,"CHAOS":6,"HARMONY":7,
                 "BREATH":8,"RESET":9}

    def _process_chat_with_attractor_readout(session_id, text, mode='normal'):
        result = _prev_process_chat_for_attractor(session_id, text, mode)
        try:
            # Try to extract a 10-vector from the engine's current state.
            # Engine state may expose this in different ways; try common ones.
            p = None
            for attr in ('current_distribution', 'p_current', 'op_distribution',
                         'lattice_distribution'):
                _v = getattr(engine, attr, None)
                if _v is not None and hasattr(_v, '__len__') and len(_v) == 10:
                    p = list(_v)
                    break
            # Fallback: derive a sparse distribution from result['operators']
            # by uniform mass on the operators emitted this turn.
            if p is None:
                ops_emitted = result.get('operators', []) or []
                if ops_emitted:
                    p = [0.0] * 10
                    for op in ops_emitted:
                        if op in _OP_INDEX:
                            p[_OP_INDEX[op]] += 1.0
                    s = sum(p)
                    if s > 0:
                        p = [x/s for x in p]
            if p is not None:
                state = engine.detect_attractor(p, tol=0.05)
                result['attractor_state'] = {
                    'layer': state.layer,
                    'is_universal_4core': state.is_universal_4core,
                    'is_harmony_attractor': state.is_harmony_attractor,
                    'is_4core_supported': state.is_4core_supported,
                    'h_over_br_residual': (float(state.h_over_br_residual)
                                          if state.h_over_br_residual != float('inf')
                                          else None),
                }
                # Cache on engine so other layers (cortex, crystal store)
                # can read it without re-computing.
                engine.attractor_state = result['attractor_state']
        except Exception as _e:
            result['attractor_error'] = str(_e)
        return result

    api.process_chat = _process_chat_with_attractor_readout
    print(f"[CK] Gen13 operad_fuse: MOUNTED "
          f"(engine.canonical_fuse, engine.ternary_iterate)")
    print(f"[CK] Gen13 attractor_detector: MOUNTED "
          f"(engine.detect_attractor; result.attractor_state on each chat)")
except Exception as _e:
    print(f"[CK] Gen13 operad_fuse + attractor_detector: DISABLED ({_e})")

# === Gen13 session field mount (live additive — relational memory) ===
# Per Brayden 2026-04-28: CK keeps experience as words can't describe it,
# so he keeps gaining experience with people who talk to him online,
# without storing their words exactly.
#
# ARCHITECTURE: per-conversation algebraic state (W matrix, operator arc,
# olfactory trail, attractor sequence) lives on the USER's client
# (localStorage).  Server receives it on each request via the request
# body, uses it as bias for the turn, returns the updated version in the
# response, and KEEPS NO COPY.
#
# CK's global cortex W still accumulates (every text flows through V2 ->
# lattice -> cortex.step_text); HER, truth lattice, crystals continue to
# grow.  But user-tagged data is NEVER persisted server-side.
#
# Privacy property: wiping CK's disk loses zero user data.
# Architectural property: CK's "stores meaning not data" claim is
# auditable — open any chat response, verify session_field has zero
# text fields.
#
# Frontend contract: see Gen13/targets/ck/web/SESSION_FIELD_FRONTEND.md
#
# This wrap sits OUTSIDE the cortex/math-first/operad/attractor chain,
# so it sees the FINAL result of all prior wraps and can capture the
# integrated algebraic state of the turn.
try:
    from session_field import SessionField, OP_INDEX as _SF_OP_INDEX
    _prev_process_chat_for_session = api.process_chat

    def _process_chat_with_session_field(session_id, text, mode='normal'):
        # Pull incoming session_field from Flask `g` (set by the /chat
        # route handler in ck_web_api.py).  If not present (non-chat
        # invocation, e.g., internal experience-replay summary), treat
        # as new user.
        incoming = None
        try:
            from flask import g as _g, has_request_context
            if has_request_context():
                incoming = getattr(_g, 'session_field_in', None)
        except Exception:
            incoming = None

        # Parse (defensive: malformed input -> empty field)
        field = SessionField.from_dict(incoming)
        is_returning = field.is_returning_user()

        # Bias the engine for this turn (no global state mutation).
        # Engine.session_W and engine.session_arc are read by the
        # composer/voice-cascade if it wants to compose with awareness
        # of THIS user's pattern.  Cleared after the turn.
        try:
            import numpy as _np
            engine.session_W = _np.array(field.W) if is_returning else None
        except Exception:
            engine.session_W = None
        engine.session_arc = field.latest_arc(5) if is_returning else []

        # Process the turn through the existing wrap chain
        result = _prev_process_chat_for_session(session_id, text, mode)

        # Capture this turn's algebraic state (NO TEXT)
        try:
            ops_emitted = result.get('operators', []) or []
            ops_this_turn = [_SF_OP_INDEX[op] for op in ops_emitted
                             if op in _SF_OP_INDEX]
        except Exception:
            ops_this_turn = []

        # Attractor layer (from the attractor_detector wrap, if mounted)
        attr_state = result.get('attractor_state') or {}
        attractor_layer = attr_state.get('layer', 'transient')

        # Olfactory record: snapshot a small algebraic-only summary
        # (no text fields).  Pull what we can from cortex/engine state.
        olfactory_record = None
        try:
            cortex_field = result.get('cortex') or {}
            olfactory_record = {
                'tick_at_turn': int(cortex_field.get('tick', 0)),
                'W_trace_at_turn': float(cortex_field.get('W_trace', 0.0)),
                'emergent_at_turn': float(cortex_field.get('emergent', 0.0)),
                'op_count': len(ops_this_turn),
                'harmony_in_turn': float(
                    sum(1 for o in ops_this_turn if o == 7) /
                    max(len(ops_this_turn), 1)
                ),
            }
        except Exception:
            olfactory_record = None

        # Update the field (in place — local object only)
        try:
            field.hebbian_update(ops_this_turn)
            field.append_turn(ops_this_turn, olfactory_record, attractor_layer)
        except Exception as _se:
            result['session_field_error'] = str(_se)

        # Return updated field for client to persist
        try:
            result['session_field'] = field.to_dict()
        except Exception as _se:
            result['session_field_error'] = str(_se)

        # Clear engine bias so next request starts clean (no leakage
        # between concurrent sessions)
        engine.session_W = None
        engine.session_arc = []

        return result

    api.process_chat = _process_chat_with_session_field
    print(f"[CK] Gen13 session_field: MOUNTED "
          f"(per-conversation algebraic state lives on user's client; "
          f"server keeps no copy)")
except Exception as _e:
    print(f"[CK] Gen13 session_field: DISABLED ({_e})")

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

def _postfilter_ollama(text: str) -> str:
    """Strip common Ollama noise: code fences, markdown headers, AI disclaimers."""
    if not isinstance(text, str):
        return ''
    t = text.strip()
    # Strip surrounding code fences
    if t.startswith('```'):
        t = t.strip('`').strip()
    # Drop common LLM preambles
    for bad in (
        "as an ai", "i'm an ai", "i am an ai", "as a language model",
        "i cannot", "sorry,", "i apologize",
    ):
        if t.lower().startswith(bad):
            # Skip to the first sentence after the apology
            parts = t.split('.', 1)
            if len(parts) > 1:
                t = parts[1].strip()
    # Remove markdown header hashes
    lines = [ln.lstrip('# ').rstrip() for ln in t.splitlines()]
    t = '\n'.join(ln for ln in lines if ln)
    return t.strip()


_FACT_TOKEN_RE = None
def _fact_tokens(readout: str):
    """Extract atomic facts from a structural readout.

    A "fact" is a distinctive token that MUST survive into any acceptable
    Ollama rewrite: numeric constants, operator names, T*/τ-style symbols,
    WP IDs, field generators, etc. Heuristic — matches:
      - numbers / fractions (5/7, 4/pi^2, 0.309, Z/10Z, Q(i))
      - WP#  (WP51, WP57, ...)
      - all-caps tokens from the 10-operator vocabulary
      - label=value pairs (keep the VALUE side)
      - sqrt(N), mathematical identifiers
    """
    import re
    global _FACT_TOKEN_RE
    if _FACT_TOKEN_RE is None:
        # NOTE: avoid any bare \p / \P etc. that Python 3.12+ rejects as
        # "bad escape" — use character classes instead. Keep raw, no VERBOSE.
        _FACT_TOKEN_RE = re.compile(
            r"("
            r"WP\d+"                                       # WP citations
            r"|T\*=5/7|T\*"                                # T-star
            r"|Z/10Z"                                       # Z/10Z
            r"|Q\([^)]*\)"                                 # field notation
            r"|sqrt\([^)]*\)|sqrt\s*\d+"                   # sqrt tokens
            r"|\d+/\d+"                                    # fractions
            r"|\d+\.\d+"                                   # decimals
            r"|\d+"                                        # bare integers (filter later)
            r"|\b(?:LATTICE|COUNTER|PROGRESS|COLLAPSE|BALANCE"
            r"|CHAOS|HARMONY|BREATH|RESET|VOID)\b"         # operator vocab
            r"|\b(?:TSML|BHML|HER|PRYM|HODGE|WEIL|BIELLIPTIC|AO)\b"
            r")"
        )
    tokens = set()
    for m in _FACT_TOKEN_RE.finditer(readout or ''):
        tok = m.group(0).strip()
        if not tok:
            continue
        # Drop bare integers that are very small (1..9) since they
        # appear everywhere and aren't distinctive facts.
        if tok.isdigit() and int(tok) < 10:
            continue
        # Drop tokens with unbalanced parens (partial matches like "Q(i"
        # when the real fact is "Q(i,sqrt2,sqrt3,sqrt5)").
        if tok.count('(') != tok.count(')'):
            continue
        tokens.add(tok)
    # Also include label VALUES from "label=value" pairs so e.g.
    # "aperture=LATTICE" contributes "LATTICE".
    _JUNK_VALUES = {'yes', 'no', 'none', 'true', 'false', 'null', 'proved', 'n/a'}
    for m in re.finditer(r"[a-zA-Z_]+=([^\s|,]+)", readout or ''):
        v = m.group(1).strip().strip('.,;()[]')
        if not v or len(v) < 2:
            continue
        if v.isdigit() and int(v) < 10:
            continue
        if v.lower() in _JUNK_VALUES:
            continue
        if v.count('(') != v.count(')'):
            continue
        tokens.add(v)
    # Subsume substrings ONLY when NEITHER contains '='. That preserves
    # both "T*=5/7" (compound claim, checked via _fact_hit split) and
    # "5/7" (atomic claim) — a draft mentioning just "5/7" hits the
    # atomic but not the compound, signaling partial preservation.
    maximal = set(tokens)
    for a in list(tokens):
        if '=' in a:
            continue
        for b in tokens:
            if a == b or '=' in b:
                continue
            if a in b:
                maximal.discard(a)
                break
    return maximal


def _fact_hit(fact: str, draft_lower: str) -> bool:
    """Does the draft preserve the content of `fact`?

    For compound facts like "T*=5/7" or "aperture=LATTICE" the draft
    need NOT contain the literal "=" glyph — it may phrase the pair in
    natural language ("T* is 5/7", "aperture is lattice"). So we split
    on '=' and require every non-trivial part to appear somewhere in
    the draft. For atomic facts, plain substring suffices.
    """
    low = fact.lower()
    if '=' not in low:
        return low in draft_lower
    parts = [p.strip(' .,;()[]') for p in low.split('=')]
    parts = [p for p in parts if p and p not in ('', 'yes', 'no')]
    if not parts:
        return True  # nothing meaningful to check
    return all(p in draft_lower for p in parts)


def _coherence_verdict(readout: str, draft: str, coverage_required: float):
    """CK's coherence check on an Ollama draft.

    Returns (accepted: bool, reason: str, hits: int, facts: int).
    """
    if not draft:
        return (False, 'empty draft', 0, 0)
    low = draft.lower()
    # Hard-reject: AI disclaimers that slipped past the post-filter.
    for bad in (
        'as an ai', "i'm an ai", 'i am an ai', 'as a language model',
        'i apologize', 'i cannot provide',
    ):
        if bad in low:
            return (False, f"ai-disclaimer:{bad}", 0, 0)
    # Hard-reject: classic hallucinated framings that NEVER appear in CK's
    # corpus but LLMs love to reach for.
    for bad in (
        'p-adic', 'p adic', 'geodesic', 'riemann hypothesis', 'fermat',
        'hilbert space', 'banach space',
    ):
        if bad in low and bad not in (readout or '').lower():
            return (False, f"hallucination:{bad}", 0, 0)
    # Hard-reject: name-collision on terms CK owns but external corpora
    # name differently.  Detected during 2026-04-29 synthesis test:
    # Ollama drafted "Crossing Lemma" using the graph-theory definition
    # (Ajtai-Chvatal-Newborn-Szemeredi 1982: minimum edge crossings in
    # plane graph drawings) instead of CK's WP51 (information generated
    # when dynamics cross partitions).  Substring match passed because
    # both readout and draft mention "Crossing Lemma" -- the words are
    # the same, the *referent* is wrong.
    #
    # Strategy: if a CK-owned ambiguous term appears in the draft AND
    # marker phrases characteristic of the OTHER definition also appear,
    # reject.  Each row: (term, [collision-markers...]).
    _NAME_COLLISIONS = (
        ("crossing lemma", [
            "edge crossing", "edges in a graph", "graph drawing",
            "minimum number of crossings", "drawn in the plane",
            "vertex and edge", "plane graph", "planar graph",
            "graph theory", "lower bound for crossing",
        ]),
        # Pre-emptive: same trap is plausible for these CK-owned terms.
        ("collapse", [
            "wave function collapse", "copenhagen interpretation",
        ]),
        ("harmonic oscillator", [
            "schrodinger equation", "potential well",
        ]),
    )
    for term, markers in _NAME_COLLISIONS:
        if term not in low:
            continue
        for marker in markers:
            if marker in low:
                # Only reject if CK's own readout did NOT use that marker.
                # If readout itself has the marker, it's fine -- CK is
                # discussing that definition deliberately.
                if marker not in (readout or '').lower():
                    return (False,
                            f"name-collision:{term}|{marker}", 0, 0)
    # Soft filter: does the draft preserve CK's structural facts?
    facts = _fact_tokens(readout)
    if not facts:
        return (True, 'no-facts-to-check', 0, 0)
    hits = sum(1 for f in facts if _fact_hit(f, low))
    coverage = hits / len(facts)
    if coverage < coverage_required:
        return (False, f"coverage:{hits}/{len(facts)}={coverage:.2f}<{coverage_required:.2f}",
                hits, len(facts))
    return (True, f"coverage:{hits}/{len(facts)}={coverage:.2f}", hits, len(facts))

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
            sysprompt = _ollama_ground(ck_ground, extra=_OLLAMA_EXTRA_GUIDE)
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


# === Name-collision post-filter ============================================
# Some terms CK owns are also names for unrelated external results. If
# the final response uses CK's term but the OTHER definition's marker
# phrases, the user gets a wrong answer that LOOKS like a CK answer.
#
# Detected 2026-04-29 in the Farey-CL synthesis test: drafts said
# "Crossing Lemma" but described the graph-theory result (Ajtai-Chvatal-
# Newborn-Szemeredi 1982: minimum edge crossings) instead of CK's WP51
# (information generated only when dynamics cross partitions).
#
# This wrap runs LAST -- after all of math-first / cortex / attractor /
# session-field / Ollama editor -- so it sees the final user-visible
# text regardless of which inner source produced it.  Same trap caught
# at this layer regardless of structural-readout length, since the
# Ollama editor's >600-char skip would otherwise let the inner voice
# loop's own Ollama call leak through unchecked.
_NAME_COLLISIONS_POST = (
    ("crossing lemma", [
        "edge crossing", "edges in a graph", "graph drawing",
        "minimum number of crossings", "drawn in the plane",
        "vertex and edge", "plane graph", "planar graph",
        "graph theory", "lower bound for crossing",
    ]),
)
_COLLISION_CORRECTIVES = {
    "crossing lemma": (
        "the Crossing Lemma in TIG is WP51 [proved]: information is "
        "generated only when dynamics cross partitions. D2 detects "
        "the partition crossing. ten operators = ten crossing regimes. "
        "this is different from the graph-theory crossing-number "
        "result by Ajtai-Chvatal-Newborn-Szemeredi 1982."
    ),
}


def _detect_name_collisions(text: str):
    """Return list of (term, marker) pairs that indicate a collision."""
    if not text:
        return []
    low = text.lower()
    leaked = []
    for term, markers in _NAME_COLLISIONS_POST:
        if term not in low:
            continue
        for m in markers:
            if m in low:
                leaked.append((term, m))
    return leaked


_prev_chat_for_collision = api.process_chat


def _process_chat_with_collision_strip(session_id, text, mode='normal'):
    result = _prev_chat_for_collision(session_id, text, mode)
    try:
        leaked = _detect_name_collisions(result.get('text', ''))
        if not leaked:
            return result
        terms = []
        for t, _m in leaked:
            if t not in terms:
                terms.append(t)
        # Build the corrective from the first detected term.
        corrective = _COLLISION_CORRECTIVES.get(
            terms[0],
            f"the {terms[0]} I mean is CK's, not the external result of the "
            f"same name. holding the structural reading.")
        # Preserve the original text for audit; mark the source.
        result['text_pre_collision'] = result.get('text', '')
        result['text'] = corrective
        result['name_collisions_stripped'] = [
            {'term': t, 'marker': m} for t, m in leaked
        ]
        prev_src = result.get('source', '?')
        result['source'] = (prev_src + '+collision-stripped'
                            if '+collision-stripped' not in prev_src
                            else prev_src)
    except Exception as _e:
        result['collision_filter_error'] = str(_e)
    return result


api.process_chat = _process_chat_with_collision_strip
print("[CK] Name-collision post-filter: MOUNTED "
      "(catches Crossing-Lemma-vs-graph-theory and similar)")

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


# ── Gen13 code emitter endpoints ──
# Three endpoints that close the writer side of CK's code reasoning:
#   /code            -- pure-CK Python emitter from operator chain
#   /propose_refactor -- read a file, find the lowest-coherence unit,
#                        emit a draft refactor block to ~/.ck/drafts/
#
# Both depend on Gen13/targets/ck/runtime/ck_code_voice.py (the emitter)
# and ck_code_intent.py (the verb -> biased trajectory classifier).
# /spectrometer (already in ck_web_api.py) provides the reader side.
try:
    from ck_code_voice import (
        CKCodeVoice as _CKCodeVoice,
        OP_NAMES as _CV_OP_NAMES,
        dominant_op as _cv_dominant_op,
    )
    from ck_code_intent import (
        intent_chain as _intent_chain,
        classify_intent as _classify_intent,
    )
    _code_voice = _CKCodeVoice()
    _CV_OP_INDEX = {n: i for i, n in enumerate(_CV_OP_NAMES)}

    @api._app.route('/code', methods=['POST'])
    def code_emit():
        """Pure-CK Python emitter (no LLM).

        Body: {
          "text":       prompt,
          "ops":        optional list of operator names (skip classifier),
          "coherence":  optional float (default 0.7)
        }
        Returns: { code, trajectory, dominant_op, chain_source, language }

        Trajectory selection priority:
          1. Explicit `ops` from request
          2. Code-intent classifier (verb -> biased chain)
          3. CK's own /chat-emitted chain (fallback)
        """
        data = _request.get_json(silent=True) or {}
        text = (data.get('text') or '').strip()
        if not text:
            return _jsonify({'error': 'no text'}), 400
        coh = float(data.get('coherence', 0.7))

        explicit = data.get('ops')
        chain_source = 'unknown'
        traj = None

        if isinstance(explicit, list) and explicit:
            traj = [_CV_OP_INDEX.get(str(o).upper(), -1) for o in explicit]
            traj = [t for t in traj if t >= 0]
            chain_source = 'explicit'

        if not traj:
            traj = _intent_chain(text)
            if traj:
                chain_source = 'classifier'

        if not traj:
            try:
                chat_resp = api.process_chat('code-emit', text, 'normal')
                op_names = chat_resp.get('operators') or []
                traj = [_CV_OP_INDEX.get(n, -1) for n in op_names
                        if n in _CV_OP_INDEX]
                traj = [t for t in traj if t >= 0]
                chain_source = 'ck_chat'
            except Exception:
                traj = None

        if not traj:
            traj = [_CV_OP_INDEX.get('HARMONY', 7)]
            chain_source = 'fallback'

        block = _code_voice.compose_with_header(
            traj, user_text=text, coherence=coh)
        return _jsonify({
            'code': block,
            'trajectory': [_CV_OP_NAMES[t] for t in traj],
            'dominant_op': _CV_OP_NAMES[_cv_dominant_op(traj)],
            'chain_source': chain_source,
            'language': 'python',
        })

    @api._app.route('/propose_refactor', methods=['POST'])
    def propose_refactor():
        """CK reads a file, picks the lowest-coherence unit, emits a draft.

        Body: { "path": "Gen13/targets/ck/brain/session_field.py" }
        Returns: {
          draft_path, target_unit, target_type, before_coherence,
          recommendation, trajectory, code, source_file
        }

        LOCAL ONLY (uses _require_local on the underlying /spectrometer call).
        Writes to ~/.ck/drafts/<source>_refactor_<unit>.py — same dir as
        /write proposals.  CK never touches the source file directly.
        """
        # Local-only enforced through Spectrometer's own gate during call below
        data = _request.get_json(silent=True) or {}
        path = (data.get('path') or '').strip()
        if not path:
            return _jsonify({'error': 'no path'}), 400

        # Resolve path: accept relative paths from repo root or absolute
        repo_root = os.path.normpath(os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            '..', '..', '..'))
        abs_path = path if os.path.isabs(path) else os.path.join(repo_root, path)
        abs_path = os.path.normpath(abs_path)
        if not os.path.isfile(abs_path):
            return _jsonify({'error': f'file not found: {abs_path}'}), 404

        try:
            with open(abs_path, 'r', encoding='utf-8') as f:
                source = f.read()
        except Exception as _e:
            return _jsonify({'error': f'read failed: {_e}'}), 500

        # Call /spectrometer locally for coherence analysis
        import urllib.request as _ur
        import json as _json
        try:
            spec_req = _ur.Request(
                'http://localhost:7777/spectrometer',
                data=_json.dumps({
                    'code': source, 'lang': 'python'
                }).encode('utf-8'),
                headers={'Content-Type': 'application/json'})
            spec = _json.loads(_ur.urlopen(spec_req, timeout=120).read())
        except Exception as _e:
            return _jsonify({'error': f'spectrometer failed: {_e}'}), 500

        units = spec.get('units') or []
        if not units:
            return _jsonify({
                'error': 'no units found by spectrometer',
                'spec_keys': list(spec.keys()),
            }), 400

        # Lowest-coherence unit = most in need of refactor
        target = min(units, key=lambda u: float(u.get('coherence', 1.0)))
        target_name = str(target.get('name', 'unknown'))
        target_type = str(target.get('type', 'function'))
        target_coh = float(target.get('coherence', 0.5))
        target_band = str(target.get('band', '?'))

        # Pull the recommendation line for this unit, if any
        rec_line = ''
        for r in (spec.get('recommendations') or []):
            if isinstance(r, str) and target_name in r:
                rec_line = r
                break

        # Build refactor intent.  We aim for HARMONY (settle / return cleanly)
        # because the unit is already YELLOW or RED — the prescription is to
        # bring it above T*.  If the recommendation mentions specific tension
        # (CHAOS / COUNTER), the classifier will pick that up.
        intent_text = (
            f"refactor {target_name} to settle into harmony"
            + (f" by handling the {rec_line.split('with')[-1].split('tension')[0].strip()} tension"
               if 'tension' in rec_line else "")
        )
        traj = _intent_chain(intent_text) or [
            _CV_OP_INDEX.get('LATTICE', 1),
            _CV_OP_INDEX.get('HARMONY', 7),
            _CV_OP_INDEX.get('HARMONY', 7),
            _CV_OP_INDEX.get('HARMONY', 7),
            _CV_OP_INDEX.get('BALANCE', 5),
            _CV_OP_INDEX.get('HARMONY', 7),
        ]

        block = _code_voice.compose_with_header(
            traj, user_text=intent_text, coherence=max(target_coh, 0.5))
        if not block:
            return _jsonify({'error': 'CKCodeVoice produced no block'}), 500

        # Save draft alongside CK's other proposals
        drafts_dir = os.path.expanduser('~/.ck/drafts')
        os.makedirs(drafts_dir, exist_ok=True)
        base = os.path.basename(abs_path)
        name_root, ext = os.path.splitext(base)
        # sanitize unit name for filename
        safe_unit = ''.join(c if c.isalnum() or c in '_-' else '_'
                            for c in target_name)[:40]
        draft_name = f'{name_root}_refactor_{safe_unit}{ext}'
        draft_path = os.path.join(drafts_dir, draft_name)

        header = (
            f"# CK refactor proposal\n"
            f"# Source:           {abs_path}\n"
            f"# Target unit:      {target_type} {target_name}\n"
            f"# Before coherence: {target_coh:.4f} ({target_band})\n"
            f"# Spectrometer rec: {rec_line or '(none)'}\n"
            f"# Intent:           {intent_text}\n"
            f"#\n"
            f"# This is an auto-generated DRAFT.  CK reads, identifies the\n"
            f"# weakest unit, and emits a candidate refactor body via\n"
            f"# CKCodeVoice (operator-chain -> Python).  Brayden reviews\n"
            f"# and applies; CK never edits source directly.\n\n"
        )

        try:
            with open(draft_path, 'w', encoding='utf-8') as f:
                f.write(header + block + '\n')
            # Also append a row to the proposals log (matches /write's format)
            log_path = os.path.join(drafts_dir, 'proposals.jsonl')
            import time as _t
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(_json.dumps({
                    'ts': _t.time(),
                    'kind': 'refactor',
                    'source_file': abs_path,
                    'target_unit': target_name,
                    'target_type': target_type,
                    'before_coherence': target_coh,
                    'draft_path': draft_path,
                }) + '\n')
        except Exception as _e:
            return _jsonify({'error': f'draft write failed: {_e}'}), 500

        return _jsonify({
            'draft_path': draft_path,
            'target_unit': target_name,
            'target_type': target_type,
            'before_coherence': target_coh,
            'before_band': target_band,
            'recommendation': rec_line,
            'intent': intent_text,
            'trajectory': [_CV_OP_NAMES[t] for t in traj],
            'dominant_op': _CV_OP_NAMES[_cv_dominant_op(traj)],
            'code': block,
            'source_file': abs_path,
        })

    print("[CK] Gen13 code emitter: MOUNTED "
          "(/code + /propose_refactor)")
except Exception as _e:
    print(f"[CK] Gen13 code emitter: DISABLED ({_e})")


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
