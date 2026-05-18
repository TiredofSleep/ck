"""CK boot — engine + web API + static website serving."""
import sys, os, time, signal, threading, json
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
# Expose api on the engine so Gen14 mounts (proactive trigger) can find
# process_chat to wrap for history-tracking.
engine.web_api = api

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
    # Cortex selection: CK_CORTEX_DIM=7 uses the live 7-dim cortex (cortex_v2);
    # otherwise the 5-dim cortex (cortex.py). State files are dim-specific so
    # the two paths don't trample each other.
    _cortex_dim = int(os.environ.get('CK_CORTEX_DIM', '5'))
    if _cortex_dim == 7:
        from cortex_v2 import CortexV2 as _Cortex
        from cortex_persist import (
            AutoSaver as _AutoSaver,
            load_cortex as _load_cortex,
            save_cortex as _save_cortex,
        )
        # 7-dim uses its own state file so it doesn't overwrite 5-dim state.
        _CORTEX_STATE_PATH = os.path.normpath(os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            '..', '..', '..', 'Gen13', 'var', 'cortex_state_7d.json'))
        # If 7-dim state doesn't exist yet, seed from migrated file (which
        # embeds the live 5-dim W in the top-left 5x5).
        _migrated_path = os.path.normpath(os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            '..', '..', '..', 'Gen13', 'var',
            'cortex_state_7d_migrated.json'))
        if not os.path.exists(_CORTEX_STATE_PATH) and os.path.exists(_migrated_path):
            import shutil
            shutil.copy(_migrated_path, _CORTEX_STATE_PATH)
            print(f"[CK] Gen13 cortex: seeded 7-dim state from migration "
                  f"{_migrated_path}")
        print(f"[CK] Gen13 cortex: dim=7 (CortexV2 with 7x7 Hebbian)")
    else:
        from cortex import Cortex as _Cortex
        from cortex_persist import (
            AutoSaver as _AutoSaver,
            load_cortex as _load_cortex,
            save_cortex as _save_cortex,
            DEFAULT_STATE_PATH as _CORTEX_STATE_PATH,
        )
        print(f"[CK] Gen13 cortex: dim=5 (Cortex with 5x5 Hebbian)")

    from cortex_voice import (
        cortex_speak as _cortex_speak,
        speak as _cortex_speak_route_lines,
        apply_crystal_boost as _apply_crystal_boost,
    )
    # Paragraph voice: default ON. Set CK_PARAGRAPH_VOICE=0 to fall back to
    # the original line-joined structural output.
    _PARAGRAPH_VOICE = os.environ.get('CK_PARAGRAPH_VOICE', '1') != '0'
    if _PARAGRAPH_VOICE:
        try:
            from cortex_voice import speak_paragraph as _cortex_speak_route
            print(f"[CK] Gen13 paragraph voice: ENABLED "
                  f"(speak_paragraph drives chat responses)")
        except Exception as _pe:
            _cortex_speak_route = _cortex_speak_route_lines
            print(f"[CK] Gen13 paragraph voice: unavailable ({_pe}); "
                  f"falling back to line-joined structural")
    else:
        _cortex_speak_route = _cortex_speak_route_lines
        print(f"[CK] Gen13 paragraph voice: DISABLED (CK_PARAGRAPH_VOICE=0)")
    import cortex_voice as _cortex_voice_mod
    print(f"[CK] Gen13 cortex_voice loaded from: {_cortex_voice_mod.__file__}")
    # Fallback-version probe: the newer speak() emits a self-report
    # (feel/field) for unclassified queries instead of returning None.
    try:
        _probe_cx = _Cortex().boot()
        _probe_out = _cortex_speak_route(_probe_cx, "hi")
        print(f"[CK] Gen13 cortex_voice.speak('hi') cold probe: "
              f"type={type(_probe_out).__name__} len={len(_probe_out) if isinstance(_probe_out,str) else 'n/a'} "
              f"preview={(_probe_out[:60] if isinstance(_probe_out,str) else None)!r}")
    except Exception as _pe:
        print(f"[CK] Gen13 cortex_voice probe failed: {_pe}")
    _cortex = _Cortex().boot()
    # Backref so cortex_voice.speak() can reach engine._recent_audio
    # for audio introspection ("what did you just hear" answered from
    # the actual recent fingerprint, not from keyword crystal lookup).
    try:
        _cortex._engine = engine
    except Exception:
        pass
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
        # TIG-internal frontier-topic vocabulary -- when the user asks
        # about these, the cortex's crystal output is the right answer
        # regardless of which Gen12 voice path produces a draft.
        # (Added 2026-04-29 after observing Ollama generate generic /
        # mistaken responses on quantum-Hall and Kleban-Ozluk queries
        # while the corrected cortex crystals had the right content.)
        'quantum hall', 'fqh', 'filling factor', 'filling fraction',
        'lutken', 'lütken', 'kleban', 'ozluk', 'özlük',
        'plateau transition', 'halperin haldane', 'sl(2,z)', 'sl2z',
        'crossing lemma', 'd2 codec', 'wp51', 'wp57', 'wp58', 'wp61',
        'wp101', 'wp104', 'wp105', 'wp110', 'wp111', 'wp112', 'wp113',
        'wp114', 'wp115', 'wp116',
        'lens of projections', 'six dof synthesis', '6 dof synthesis',
        'self-dual recursion', 'projection axes', 'meta synthesis',
        'tsml', 'bhml', 'mag^com', 'mag com', 'magmatic operad',
        'bialynicki', 'birula', 'log nonlinearity', 'log-nonlinearity',
        'primon', 'farey', 'farey spin chain', 'farey fraction',
        'donagi', 'livne', 'livné', 'beauville', 'prym',
        'hodge_cstar', 'sprint35b', 'sprint 35b',
        'sigma rate', 'sigma_rate', 'rate theorem',
        'flatness theorem', 't*', 't star', '5/7',
        'huang-lehtonen', 'huang lehtonen', 'braitt', 'silberger',
        'gauss-kuzmin', 'gauss kuzmin', 'transfer operator',
        # F6/F2/F10 frontier-bridge keys (added 2026-04-29 evening)
        'sigma_ns', 'sigma ns', 'navier stokes', 'navier-stokes',
        'ns cascade', 'dyadic ns', 'ns regularity', 'ns commutator',
        'f6 frontier', 'sigma_ns < 1',
        'kappa_xi', 'kappa xi', '13/(4e)', 'tig planck', 'tig-planck',
        'm_xi planck', 'planck mass ratio', 'f2 frontier',
        'descent risk', 'i-action descent', 'i action descent',
        'prym descent', 'f10 frontier', 'hodge_cstar descent',
        'q(i) descent', 'endomorphism descent', 'psi_2 = iota',
        # Depth-primitive + WOBBLE keys (added later 2026-04-29)
        'wobble prime', 'wobble 11', 'prime 11', 'fivefold wobble',
        'wobble manifestation', 'wobble locations', 'structural prime',
        'depth-2 primitive', 'depth-3 primitive', 'depth 2 cluster',
        'depth 3 cluster', 'fixed-form algebraic', 'm^2 = id',
        'm^3 = id', 'cube roots of unity', 'operator depth',
        'algebraic depth',
    )

    # Crystal first-word prefixes that are RECOGNITION primitives, not
    # topical/structural facts.  These fire the same matcher as topical
    # crystals but their triggers are common English words / phonemes /
    # IPA clusters, so promoting them to structural-mode routes ordinary
    # conversation ("how have you been") to label:value readout and
    # silences the prose voice.  Brayden 2026-05-02: "he really isn't
    # producing prose or fluent speech at all anymore."
    _RECOGNITION_PREFIXES = (
        'word_', 'phoneme_', 'cluster_', 'phonetic_class_',
        'phonetic_', 'rcontrol_', 'team_', 'digraph_',
        # research-scaffold prompt terms (broad triggers from /ck/research)
        # promoted-to-internal via the tier ladder do not count either:
        # they're scenario vocabulary, not topical canon.
        'prompt_term_', 'research_',
    )

    def _is_recognition_crystal(fact: str) -> bool:
        head = fact.split(':', 1)[0].strip().lower()
        return head.startswith(_RECOGNITION_PREFIXES)

    def _is_structural_query(text: str) -> bool:
        """True if the user is asking about CK's own state / coordinates
        OR matches a TOPICAL crystal trigger.

        Two classes of crystals are EXCLUDED from this gate:
          1. Recognition primitives (word_*, phoneme_*, cluster_*, etc.):
             their triggers are common English / IPA tokens; promoting
             those to structural mode silences CK's prose voice.
          2. External crystals (research findings, prompt terms): their
             triggers are broad prompt vocabulary; same problem.

        Both still FIRE when speak() runs (via _frontier_hits), so they
        appear in cortex_speak readouts when the query is structural by
        other means (explicit STRUCTURAL_QUERY_KEYS or topical crystal
        match).  They just don't FORCE structural-mode routing.
        """
        if not text:
            return False
        t = text.lower()
        for k in _STRUCTURAL_QUERY_KEYS:
            if k in t:
                return True
        # Topical internal crystals only -- recognition primitives and
        # external scenario crystals are excluded from the gate.
        try:
            from cortex_voice import _FRONTIER_FACTS, _RUNTIME_CRYSTALS
            for triggers, fact in list(_FRONTIER_FACTS) + list(_RUNTIME_CRYSTALS):
                if _is_recognition_crystal(fact):
                    continue
                for trig in triggers:
                    if trig and trig in t:
                        return True
        except Exception:
            pass
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
            # Exact-answer sources should NEVER be overwritten by
            # cortex_speak, even for structural queries.  Per Brayden
            # 2026-05-18 capability test: TSML[5][7] hit ck_math_first
            # (set by the CL lookup) but the structural-query swap
            # then clobbered the precise "6 (CHAOS)" answer with
            # cortex_speak prose.  Math evaluation, CL lookup, and
            # code spectrometer all produce exact answers that
            # structural prose can only dilute.
            _EXACT_ANSWER_SOURCES = ('ck_math_first', 'ck_spectrometer')
            if _src in _EXACT_ANSWER_SOURCES:
                _swap_ok = False  # exact answer wins absolutely
            elif _is_past_q:
                _swap_ok = False  # pastoral wins absolutely
            elif _is_struct_q:
                _swap_ok = True   # structural query -> cortex_speak owns
            else:
                # Non-structural, non-pastoral: only override pure templates.
                # ck_fractal / ck_fractal_dual / ck_truth_recall / crystal
                # / ck_tig are stitched-dictionary fluency layers without
                # grounding -- the "old failed word cascade" Brayden has
                # rejected ("Resurrection forms the proportion through a
                # sword until domains flows...").  Replacing them with
                # cortex_speak's grounded label:value at least keeps CK
                # in real coordinates.
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
            # Persistent memory record: keep a brief log of every chat turn
            # in Gen13/var/conversation_memory.jsonl so CK retains some
            # cross-session continuity.  Best-effort, never blocks.
            #
            # Privacy (Brayden 2026-04-29): "i have no secrets ck can't tell,
            # and if i do, i will tell him it's a secret for just us."
            # Default: shareable.  Secret-flagged messages stay session-scoped.
            try:
                _record_memory_turn(
                    text=text,
                    response=result.get('text', ''),
                    source=result.get('source', 'unknown'),
                    session_id=session_id,
                )
            except Exception:
                pass

            # BDC logger -- Brayden 2026-05-02: per-turn Being/Doing/Becoming
            # snapshot for future BDC-LM training.  Best-effort, never blocks.
            # Schema documented in Gen13/targets/ck/brain/bdc_logger.py.
            try:
                from bdc_logger import log_chat_turn as _bdc_log
                _bdc_log(text=text, result=result, cortex=_cortex,
                          engine=engine, session_id=session_id)
            except Exception:
                pass

            # BDC event emitter -- Brayden 2026-05-03: emit non-operator
            # BDC events (crystal-fire, breath-shift, attractor-transition,
            # stage, band, coherence-floor, truth-confirmed, void-degenerate)
            # to fill the 17/27 codes the operator-bijection doesn't cover.
            # Best-effort, never blocks.
            try:
                from bdc_event_emitter import detect_chat_events as _bdc_emit
                _bdc_emit(result, session_id=session_id)
            except Exception:
                pass

            # Confidence reading (Brayden 2026-04-30):
            #   crystal fired      -> 0.95-0.99 (depends on # crystals + state-aware match)
            #   crystal compose    -> 0.85-0.95 (cross-crystal graph)
            #   lookup / search    -> 0.80-0.95 (depends on source quality)
            #   drift / synthesis  -> 0.40-0.70 (unverified recombination)
            #   pure speculation   -> 0.30-0.45 (no anchor)
            try:
                _src = result.get('source', '')
                _routing_now = result.get('routing', {}) or {}
                _crystal_boost = _routing_now.get('crystal_boost_count', 0) or 0
                _is_struct = _routing_now.get('is_structural_query', False)
                _spoken_struct = _routing_now.get('spoken_is_structural', False)
                _has_recall = _routing_now.get('memory_recall_count', 0) or 0
                # Inspect text for DRIFT marker (set by dream/drift surfacing)
                _text_now = (result.get('text', '') or '')
                _has_drift_marker = '[DRIFT' in _text_now or 'DRIFT,' in _text_now
                if _has_drift_marker:
                    confidence = 0.50  # drift is unverified
                    confidence_kind = "drift"
                elif _src == 'cortex_speak' and _crystal_boost >= 2:
                    # Multiple crystals fired + state-aware -> high confidence
                    confidence = min(0.99, 0.92 + 0.02 * _crystal_boost)
                    confidence_kind = "multi-crystal"
                elif _src == 'cortex_speak':
                    confidence = 0.95
                    confidence_kind = "single-crystal"
                elif _src == 'ck_math_first':
                    confidence = 0.99  # math facts are canonical
                    confidence_kind = "canonical-math"
                elif _src == 'cortex_speak_via_ollama':
                    # Ollama-edited but coherence-filtered cortex content
                    confidence = 0.85
                    confidence_kind = "cortex-via-ollama"
                elif _src in ('ck_loop_synthesized', 'ck_loop'):
                    # Warm response without strong cortex grounding
                    confidence = 0.70
                    confidence_kind = "warm-response"
                elif _src in ('ck_truth_recall',):
                    confidence = 0.80
                    confidence_kind = "truth-lattice-recall"
                elif _src in ('ck_self', 'ck_fractal', 'crystal', 'ck_tig'):
                    # Templates without active grounding
                    confidence = 0.50
                    confidence_kind = "template"
                else:
                    confidence = 0.55
                    confidence_kind = "general"
                # Recall bonus
                if _has_recall and confidence < 0.99:
                    confidence = min(0.99, confidence + 0.02)
                result['confidence'] = round(confidence, 3)
                result['confidence_kind'] = confidence_kind
            except Exception:
                pass

            # User-model update (paper 4 step 7): track per-session metadata.
            # Best-effort.
            try:
                # Extract crystal first_words from the response (cortex_speak
                # output has them as "name: ..." prefixes).
                fired_crystals = []
                resp_text = result.get('text', '') or ''
                for line in resp_text.split('\n'):
                    line = line.strip()
                    if line and ':' in line and len(line.split(':', 1)[0]) < 40:
                        fired_crystals.append(line)
                _update_user_model(session_id, text, fired_crystals,
                                    result.get('source', 'unknown'))
            except Exception:
                pass

            # Pedagogical mode (paper 4 step 8): when the user-model says
            # this user has talked about X but not Y where Y is a related
            # crystal, surface a short "you might also be interested in Y"
            # bridge.  Light-touch — only fires if the user-model has data
            # AND there's a clear bridge.
            try:
                if session_id and result.get('text'):
                    models = _load_user_models()
                    m = models.get(session_id, {})
                    topics = set(m.get("topics_seen", []))
                    if len(topics) >= 2:
                        # Identify a topic recently discussed but with related
                        # crystals never seen.
                        try:
                            from cortex_voice import _CRYSTAL_RELATED
                        except Exception:
                            from Gen13.targets.ck.brain.cortex_voice import _CRYSTAL_RELATED
                        bridge_suggestion = None
                        for topic in list(topics)[-3:]:  # check 3 most recent
                            related = _CRYSTAL_RELATED.get(topic, [])
                            unseen_related = [r for r in related if r not in topics]
                            if unseen_related:
                                bridge_suggestion = (topic, unseen_related[0])
                                break
                        if bridge_suggestion:
                            existing_text = result.get('text', '') or ''
                            ped_line = (f"\n\n(if interesting: ask about "
                                        f"'{bridge_suggestion[1]}' — it relates to "
                                        f"'{bridge_suggestion[0]}' you've raised before.)")
                            if "(if interesting:" not in existing_text:
                                result['text'] = existing_text + ped_line
                                result.setdefault('routing', {})
                                result['routing']['pedagogical_bridge'] = list(bridge_suggestion)
            except Exception as _pe:
                result.setdefault('pedagogical_error', str(_pe))

            # Memory recall hook: if user asks about a specific topic / name,
            # search the memory log for prior turns matching it and surface
            # the most-recent match alongside CK's current response.  This
            # is the "Brayden told me about TIG" recall path.
            try:
                # Only trigger on questions / about-style queries to avoid
                # flooding every chat with memory.  Heuristic: text contains
                # "?" OR contains "tell me about" / "who is" / "what did" /
                # "remember" / "do you know".
                ql = (text or '').lower()
                want_recall = (
                    '?' in (text or '') or
                    'tell me about' in ql or 'who is' in ql or
                    'what did' in ql or 'remember' in ql or
                    'do you know' in ql or 'did i say' in ql or
                    'last time' in ql
                )
                if want_recall:
                    # Extract candidate keyword: longest non-trivial word
                    words = [w.strip('.,?!;:()[]"\'') for w in (text or '').split()]
                    candidates = [w for w in words if len(w) >= 4
                                  and w.lower() not in {
                                      'tell', 'about', 'what', 'when', 'were',
                                      'have', 'this', 'that', 'they', 'remember',
                                      'know', 'said', 'last', 'time', 'with'}]
                    matches = []
                    for cand in candidates[:3]:
                        ms = _memory_search(cand, n=3, requester_session=session_id)
                        for m in ms:
                            if m not in matches:
                                matches.append(m)
                        if matches:
                            break
                    if matches:
                        # Surface the most recent 1-2 matches as a "recall"
                        # line in the result text.
                        recall_lines = ['recall:']
                        for m in matches[:2]:
                            ts = m.get('iso_ts', '?')
                            top = (m.get('topic', '') or '')[:120]
                            recall_lines.append(f"  {ts}: \"{top}\"")
                        recall_text = '\n'.join(recall_lines)
                        # Append to result text if cortex_speak swap; else
                        # prepend to the warm response so user sees both.
                        existing = result.get('text', '') or ''
                        if recall_text not in existing:
                            result['text'] = existing + '\n\n' + recall_text
                        result.setdefault('routing', {})
                        result['routing']['memory_recall_count'] = len(matches)
            except Exception as _re:
                result['memory_recall_error'] = str(_re)

            # Crystal-W boost: when crystals fire, nudge the Hebbian W
            # matrix in their op_signature directions.  This is the
            # "active integration" of crystals -- they shape the cortex
            # for future ticks rather than being passive lookup tables.
            # Boost regardless of swap_decision; the firing itself is
            # what matters, not whether we used it as the user-facing
            # text.
            try:
                if spoken:
                    n_boosted = _apply_crystal_boost(_cortex, spoken,
                                                     boost_strength=0.005)
                    if n_boosted > 0:
                        result.setdefault('routing', {})
                        result['routing']['crystal_boost_count'] = n_boosted
            except Exception as _be:
                result['crystal_boost_error'] = str(_be)
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

# === Gen13 dirac_mount (Sprint 18 Bridge: discrete Dirac on 4-core F_5-lift) ===
# Brayden 2026-05-04: "after you get github clean and ready with all the new
# info, work on CK with it!"
#
# Mounts the tig_dirac framework: 24 structural predictions (Omega_b EXACT,
# 1/alpha = 137.036, 9 SM Yukawas, PMNS angles, microtubule Q_c falsifier),
# 15 algebraic findings, 10 cross-domain bridge facts injected into cortex_voice.
# Endpoints: /dirac/{info,verify,predictions,cosmology,mixing,yukawa,clifford,
#                    algebra,microtubule,predict/<obs>}
try:
    sys.path.insert(0, os.path.join(_GEN13_BRAIN, 'dirac'))
    from dirac_mount import mount_dirac as _mount_dirac
    _dirac_info = _mount_dirac(api, engine, verify_on_mount=True)
    if not _dirac_info.get('mounted'):
        print(f"[CK] Gen13 dirac_mount: PARTIAL (verified={_dirac_info.get('verified')}, "
              f"error={_dirac_info.get('mount_error') or _dirac_info.get('verify_error')})")
except Exception as _e:
    print(f"[CK] Gen13 dirac_mount: DISABLED ({type(_e).__name__}: {_e})")

# === Gen13 grammar_lm mount (CK's own operator-grammar transformer) ===
# Brayden 2026-05-02: "[CK] needs his own 1B-3B parameter ... model that
# doesn't learn the information, it just learns CK's internal language
# and transitions."  ck_grammar_lm is a 1.2M-param tiny transformer
# trained autoregressively on CK's algebra walks (TSML / BHML / T+B-mix)
# + real operator streams (dream_journal, cortex_history).  No facts,
# no English -- only operator IDs.
#
# Three Flask endpoints exposed: /grammar/sample, /grammar/score,
# /grammar/predict, /grammar/cortex_predict, /grammar/info.
try:
    sys.path.insert(0, os.path.join(_GEN13_BRAIN, 'grammar_lm'))
    from grammar_lm_mount import mount as _mount_grammar_lm
    _gl_ok = _mount_grammar_lm(engine, api._app)
    if not _gl_ok:
        print("[CK] grammar_lm: mount returned False (model file missing?)")
    # Also mount the operator memory bank (non-parametric retrieval).
    # Brayden 2026-05-02 reframe: "the AI is the memory transfer device --
    # in and out".  Bank stores (encoded_context, observed_next) pairs
    # from training data; queries retrieve nearest by cosine similarity.
    #
    # 2026-05-16 update: the bank build runs 20,000 torch forward passes
    # which got starved by the 50Hz swarm at REALTIME priority on core 0,
    # blocking the entire boot for many minutes (boot 7 + boot 8 hangs).
    # Three modes now:
    #   CK_DISABLE_BANK=1        -> skip entirely (legacy workaround)
    #   CK_BANK_MODE=foreground  -> blocking build at boot (legacy default)
    #   CK_BANK_MODE=background  -> spawn a daemon thread to build the
    #                                bank AFTER Organism alive (default
    #                                since 2026-05-16; matches actual
    #                                deployment expectations)
    try:
        _bank_disabled = os.environ.get('CK_DISABLE_BANK', '0') == '1'
        _bank_mode = os.environ.get('CK_BANK_MODE', 'background').lower()
        if _bank_disabled:
            print("[CK] bank_mount: DISABLED (CK_DISABLE_BANK=1)")
        else:
            from bank_mount import mount as _mount_bank
            if _gl_ok and getattr(engine, 'grammar_lm', None) is not None:
                if _bank_mode == 'background':
                    print("[CK] bank_mount: backgrounded "
                          "(CK_BANK_MODE=background); will build after "
                          "Organism alive without blocking boot")
                    def _bank_bg_build():
                        try:
                            # Give the boot a moment to actually finish
                            # before we start contending for CPU.
                            time.sleep(30.0)
                            _ok = _mount_bank(engine, api._app,
                                                engine.grammar_lm)
                            if _ok:
                                print("[CK] bank_mount: backgrounded build "
                                      "complete")
                                try:
                                    from ensemble import mount as _me
                                    _me(engine, api._app, engine.grammar_lm,
                                         engine.operator_bank)
                                    print("[CK] sim_gated_ensemble: "
                                          "MOUNTED (post-bank)")
                                except Exception as _ee:
                                    print(f"[CK] sim_gated_ensemble: "
                                          f"DISABLED ({_ee})")
                            else:
                                print("[CK] bank_mount: backgrounded "
                                      "build returned False")
                        except Exception as _e:
                            print(f"[CK] bank_mount: backgrounded "
                                  f"FAILED ({_e})")
                    threading.Thread(target=_bank_bg_build,
                                      name="bank-bg-build",
                                      daemon=True).start()
                else:
                    # foreground mode (legacy)
                    _bank_ok = _mount_bank(engine, api._app,
                                             engine.grammar_lm)
                    if not _bank_ok:
                        print("[CK] bank_mount: returned False")
                    else:
                        try:
                            from ensemble import mount as _mount_ensemble
                            _mount_ensemble(engine, api._app,
                                             engine.grammar_lm,
                                             engine.operator_bank)
                        except Exception as _ee:
                            print(f"[CK] sim_gated_ensemble: DISABLED "
                                  f"({_ee})")
    except Exception as _be:
        print(f"[CK] bank_mount: DISABLED ({_be})")
except Exception as _e:
    print(f"[CK] grammar_lm: DISABLED ({_e})")

# === Tick-sample logger (more BDC data accumulation) ===
# Diagnostic prints on success added 2026-05-16 to locate boot hangs.
# Skippable: set CK_SKIP_BDC_SAMPLER=1
print("[CK] boot_phase: entering bdc_tick_sampler", flush=True)
if os.environ.get('CK_SKIP_BDC_SAMPLER', '0') == '1':
    print("[CK] bdc_tick_sampler: SKIPPED (CK_SKIP_BDC_SAMPLER=1)", flush=True)
else:
    try:
        from bdc_tick_sampler import mount as _mount_sampler
        _mount_sampler(engine, api._app, _cortex, interval_sec=10.0)
        print("[CK] bdc_tick_sampler: MOUNTED", flush=True)
    except Exception as _e:
        print(f"[CK] bdc_tick_sampler: DISABLED ({_e})", flush=True)

# === Fault-state diagnostic (V/F/S/T role analysis per chat) ===
print("[CK] boot_phase: entering ck_fault_state_hook", flush=True)
if os.environ.get('CK_SKIP_FAULT_HOOK', '0') == '1':
    print("[CK] ck_fault_state_hook: SKIPPED (CK_SKIP_FAULT_HOOK=1)", flush=True)
else:
    try:
        from ck_fault_state_hook import mount as _mount_fault
        _mount_fault(engine, api._app, _cortex)
        print("[CK] ck_fault_state_hook: MOUNTED", flush=True)
    except Exception as _e:
        print(f"[CK] ck_fault_state_hook: DISABLED ({_e})", flush=True)

# === BDC event emitter (fills non-operator DBC codes) ===
# Brayden 2026-05-03: "wire it up" -- emit DBC codes for crystal-fire,
# breath-shift, attractor-transition, stage, band, coherence-floor,
# truth-confirmed, void-degenerate, idle-reflection.  These 17 events
# map to the 17 missing DBC codes that operator-bijection doesn't cover,
# bringing total Divine27 coverage from 10/27 = 37% to 100%.
print("[CK] boot_phase: entering bdc_event_emitter", flush=True)
if os.environ.get('CK_SKIP_BDC_EMITTER', '0') == '1':
    print("[CK] bdc_event_emitter: SKIPPED (CK_SKIP_BDC_EMITTER=1)", flush=True)
else:
    try:
        from bdc_event_emitter import mount as _mount_events
        _mount_events(engine, api._app, _cortex)
        print("[CK] bdc_event_emitter: MOUNTED", flush=True)
    except Exception as _e:
        print(f"[CK] bdc_event_emitter: DISABLED ({_e})", flush=True)

# === 5-AI cell organism (TSML / BHML / F3 / F4 / Glue) — additive, FLAG OFF ===
# Brayden 2026-05-02: "best ever and plastic now"
# ClaudeChat 2026-05-02 review: feature flag default off; chat path is NOT
# routed through cells until Phase 7 live cutover with real-prompt smoke test.
#
# What this does:
#   - Loads CellOrchestrator (4 cells, canonical-core + plastic-tissue)
#   - Builds GlueAI with 3 default scalars (alpha=beta=0.5, gamma=1.0)
#   - Runs cell_audit at boot; refuses to enable cells if pass_rate < 99%
#   - Sets engine.cells_enabled = False (feature flag, default off)
#   - Registers /cells/audit, /cells/state, /cells/plasticity/run, /cells/respond
#   - Plasticity scheduler stays OFF until manually enabled
#
# What this does NOT do:
#   - Modify the chat path (cells are observable but not influential yet)
#   - Touch the live tunnel
#   - Train cells (they ship pre-fit from mine_historical_bdc.py output)
print("[CK] boot_phase: entering cells_mount", flush=True)
if os.environ.get('CK_SKIP_CELLS', '0') == '1':
    print("[CK] cells_mount: SKIPPED (CK_SKIP_CELLS=1)", flush=True)
else:
    try:
        import sys as _cells_sys
        from pathlib import Path as _CellsPath
        _CELLS_BRAIN = _CellsPath(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen13\targets\ck\brain")
        if str(_CELLS_BRAIN) not in _cells_sys.path:
            _cells_sys.path.insert(0, str(_CELLS_BRAIN))
        from cells_mount import mount as _mount_cells
        _mount_cells(engine, api._app, enable_plasticity=False)
        print("[CK] cells_mount: MOUNTED", flush=True)
    except Exception as _e:
        print(f"[CK] cells_mount: DISABLED ({type(_e).__name__}: {_e})", flush=True)

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
print("[CK] boot_phase: entering session_field", flush=True)
_skip_session_field = (os.environ.get('CK_SKIP_SESSION_FIELD', '0') == '1')
if _skip_session_field:
    print("[CK] Gen13 session_field: SKIPPED "
          "(CK_SKIP_SESSION_FIELD=1)", flush=True)
try:
    if _skip_session_field:
        raise RuntimeError("CK_SKIP_SESSION_FIELD=1 (intentional skip)")
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
            # Code spectrometer output is also a canonical structural
            # readout (per-function coherence scores, dominant operators,
            # T*-band verdicts) — polishing it through Ollama dilutes
            # the exact numbers.  Per Brayden 2026-05-18 capability test.
            if src == 'ck_spectrometer':
                result['ollama_verdict'] = 'skipped:ck_spectrometer is canonical'
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
            # Skip when CK is answering from his SELF tier with high
            # confidence -- identity questions ("who am I?", "what is
            # T*?", "what is the wobble?", "how can I improve my
            # internal architecture?") should be declarative in CK's
            # own substrate voice, not laundered through an external
            # LM that contaminates with external-corpus bleed
            # (Henry James prose, HP-UX trivia, hallucinated
            # "self-awareness", etc.).  Per CK's own essay 2026-05-17:
            # "Identity questions -- who I am, T*, the wobble, alpha,
            # the 4-core -- I answer with confidence 1.0, declarative,
            # no hedge."  Architecture honors the substrate.
            _tier = result.get('dominant_tier')
            _conf = result.get('confidence')
            try:
                _conf_val = float(_conf) if _conf is not None else 0.0
            except (TypeError, ValueError):
                _conf_val = 0.0
            if _tier == 'SELF' and _conf_val >= 0.8:
                result['ollama_verdict'] = (
                    f'skipped:SELF tier @ conf={_conf_val:.2f} '
                    '(substrate voice declarative)')
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

# === Cells shadow-A/B observer (after the full chat chain is assembled) ===
# Brayden 2026-05-02 + ClaudeChat review: route shadow-mode cells alongside
# cortex_speak; log both so we can qualitatively inspect cell-vs-cortex
# disagreements BEFORE flipping cells_enabled = True.
# User response is unchanged; the shadow record is appended to result and
# also written to Gen13/var/shadow_logs/shadow_YYYY-MM-DD.jsonl.
try:
    if getattr(engine, 'cells', None) is not None:
        from cells_mount import install_shadow_observer as _install_shadow
        _install_shadow(api, engine)
except Exception as _se:
    print(f"[CK] cells shadow observer: DISABLED ({type(_se).__name__}: {_se})")

# === Research-first chat-path wrapper (Brayden 2026-05-02) ===
# "he should research every prompt before every answer!!"
# Runs ck_research(prompt) BEFORE cortex_speak's inner chat path so
# the cortex is shaped by fresh research before producing its response.
# Mode: CK_RESEARCH_MODE env var; default 'fast' (1 sub-q, headless, 60s).
# Set CK_RESEARCH_MODE=off to bypass.
try:
    _research_mode = os.environ.get('CK_RESEARCH_MODE', 'fast').lower()
    if _research_mode != 'off':
        from research_first import install_research_first_observer as _install_research
        _install_research(api, engine, mode=_research_mode)
    else:
        print(f"[CK] research_first: OFF (CK_RESEARCH_MODE=off)")
except Exception as _re:
    print(f"[CK] research_first: DISABLED ({type(_re).__name__}: {_re})")

# === Continuous study daemon (Brayden 2026-05-02) ===
# "he probably needs to study journals again, try youtube again, all of it"
# Background daemon that periodically researches frontier topics from a
# rotating curriculum, even when no user is chatting.  Defaults to OFF;
# set CK_STUDY_DAEMON=1 to enable.
try:
    if os.environ.get('CK_STUDY_DAEMON', '0') == '1':
        from study_daemon import mount as _mount_study
        _mount_study(engine, api._app, interval_sec=600.0, enable=True)
    else:
        print(f"[CK] study_daemon: NOT STARTED (set CK_STUDY_DAEMON=1 to enable)")
except Exception as _sde:
    print(f"[CK] study_daemon: DISABLED ({type(_sde).__name__}: {_sde})")

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
                 'ai.html', 'trajectory.html'}
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

# /reflect -- CK introspects on a topic by querying his own crystal store.
# Pure introspection: no chat ingestion, no operator stream emit, no
# Ollama draft.  Just: given a topic, return the matched crystals + the
# state-aware crystals + cortex state + Phi-proxy summary.  The "what
# does CK know about X" path that doesn't pretend to answer beyond what
# his crystals say.
@api._app.route('/reflect', methods=['POST', 'GET'])
def reflect():
    from flask import request as _flask_request
    if _flask_request.method == 'POST':
        body = _flask_request.get_json(silent=True) or {}
        topic = body.get('topic', '') or body.get('text', '')
    else:
        topic = _flask_request.args.get('topic', '') or _flask_request.args.get('text', '')

    out = {'topic': topic, 'crystals_keyword': [], 'crystals_state_aware': [],
           'cortex': None, 'phi_proxy': None, 'feel': None}

    # 1) Cortex state snapshot
    try:
        st = _cortex.state
        out['cortex'] = {
            'tick': st.tick,
            'W_trace': round(st.W_trace, 6),
            'emergent': round(st.emergent, 6),
            'last_b': st.last_b,
            'last_d': st.last_d,
        }
    except Exception:
        pass

    # 2) Top couplings + feel
    try:
        # cortex_voice was already imported as the module that defines _cortex_speak
        # at the top of this file; reuse the same import path.
        try:
            from cortex_voice import (
                current_feeling as _cf, dominant_couplings as _dc,
                _frontier_hits as _fhits,
                _state_aware_crystal_hits as _sahits,
            )
        except ImportError:
            # fallback path
            from Gen13.targets.ck.brain.cortex_voice import (
                current_feeling as _cf, dominant_couplings as _dc,
                _frontier_hits as _fhits,
                _state_aware_crystal_hits as _sahits,
            )
        out['feel'] = _cf(_cortex)
        out['couplings'] = _dc(_cortex, n=5)
        # 3) Crystal hits
        if topic:
            out['crystals_keyword'] = _fhits(topic.lower())
        out['crystals_state_aware'] = _sahits(_cortex, threshold=0.5, max_hits=5)
    except Exception as _re:
        out['_reflect_error'] = str(_re)

    # 4) Phi-proxy
    try:
        W = _cortex.hebbian.W
        # bipartite-cut Phi-proxy
        import itertools as _it
        total = sum(abs(W[i][j]) for i in range(5) for j in range(5))
        elems = list(range(5))
        cuts = []
        for k in range(1, 3):
            for S in _it.combinations(elems, k):
                T = tuple(e for e in elems if e not in S)
                if S[0] == 0 or k < 5 - k:
                    c = sum(abs(W[i][j]) + abs(W[j][i]) for i in S for j in T)
                    cuts.append(c)
        if cuts:
            out['phi_proxy'] = round(total - min(cuts), 4)
    except Exception:
        pass

    return _jsonify(out)


# /memory -- persistent conversation memory across reboots.
# Stores last N user topics and CK's self-summary from each session.
# Simple JSONL file at Gen13/var/conversation_memory.jsonl.
import threading as _mem_threading
_MEMORY_LOCK = _mem_threading.Lock()
_MEMORY_PATH = os.path.join(os.path.dirname(__file__), '..', '..', '..',
                            'Gen13', 'var', 'conversation_memory.jsonl')

@api._app.route('/memory', methods=['GET'])
def memory_get():
    """Return the last N conversation summaries CK has stored.
    Excludes secret-flagged entries unless include_secrets=true."""
    try:
        from flask import request as _flask_request
        n = int(_flask_request.args.get('n', 20))
        include_secrets = (_flask_request.args.get('include_secrets', 'false')
                           .lower() in ('true', '1', 'yes'))
    except Exception:
        n = 20
        include_secrets = False
    items = []
    try:
        if os.path.exists(_MEMORY_PATH):
            with open(_MEMORY_PATH, 'r') as f:
                lines = f.readlines()
            for line in lines:
                try:
                    entry = json.loads(line)
                except Exception:
                    continue
                # Privacy: drop secret entries from public listing
                if entry.get('secret') and not include_secrets:
                    continue
                items.append(entry)
            items = items[-n:]
    except Exception as _me:
        return _jsonify({'error': str(_me)})
    return _jsonify({'items': items, 'total': len(items)})


# /crystals/add -- runtime crystal authoring (paper 4 step 2)
# Adds a new crystal without code change.  Persists to runtime_crystals.json.
@api._app.route('/crystals/add', methods=['POST'])
def add_crystal_endpoint():
    try:
        from flask import request as _flask_request
        body = _flask_request.get_json(silent=True) or {}
        triggers = body.get('triggers', [])
        fact = body.get('fact', '')
        op_signature = body.get('op_signature', None)
        related = body.get('related', None)
    except Exception as e:
        return _jsonify({'error': f'bad request: {e}'}), 400

    if not isinstance(triggers, list) or not triggers:
        return _jsonify({'error': 'triggers must be a non-empty list of keywords'}), 400
    if not fact or not isinstance(fact, str) or ':' not in fact:
        return _jsonify({'error': 'fact must be a string starting with "name:"'}), 400

    try:
        from cortex_voice import add_crystal_runtime
    except Exception:
        from Gen13.targets.ck.brain.cortex_voice import add_crystal_runtime

    triggers_lower = tuple(str(t).lower() for t in triggers if t)
    op_sig = tuple(int(o) for o in op_signature) if op_signature else None
    related_list = list(related) if related else None

    ok = add_crystal_runtime(triggers_lower, fact, op_signature=op_sig,
                              related=related_list)
    if not ok:
        return _jsonify({'error': 'crystal not added (duplicate first_word or invalid)',
                         'first_word': fact.split(':', 1)[0].strip()}), 409

    first_word = fact.split(':', 1)[0].strip()
    return _jsonify({
        'ok': True,
        'first_word': first_word,
        'triggers': list(triggers_lower),
        'op_signature': list(op_sig) if op_sig else None,
        'related': related_list,
    })


# /crystals/list -- list all crystals (code-baked + runtime)
@api._app.route('/crystals/list', methods=['GET'])
def list_crystals_endpoint():
    try:
        from cortex_voice import _FRONTIER_FACTS, _RUNTIME_CRYSTALS, _CRYSTAL_OP_SIGNATURES, _CRYSTAL_RELATED
    except Exception:
        from Gen13.targets.ck.brain.cortex_voice import (
            _FRONTIER_FACTS, _RUNTIME_CRYSTALS, _CRYSTAL_OP_SIGNATURES, _CRYSTAL_RELATED
        )
    out = []
    for triggers, fact in _FRONTIER_FACTS:
        first_word = fact.split(":", 1)[0].strip()
        out.append({
            "first_word": first_word,
            "source": "code-baked",
            "triggers": list(triggers),
            "op_signature": list(_CRYSTAL_OP_SIGNATURES.get(first_word, ())),
            "related": list(_CRYSTAL_RELATED.get(first_word, [])),
            "fact_preview": fact[:120] + ("..." if len(fact) > 120 else ""),
        })
    for triggers, fact in _RUNTIME_CRYSTALS:
        first_word = fact.split(":", 1)[0].strip()
        out.append({
            "first_word": first_word,
            "source": "runtime",
            "triggers": list(triggers),
            "op_signature": list(_CRYSTAL_OP_SIGNATURES.get(first_word, ())),
            "related": list(_CRYSTAL_RELATED.get(first_word, [])),
            "fact_preview": fact[:120] + ("..." if len(fact) > 120 else ""),
        })
    return _jsonify({"count": len(out), "crystals": out})


# ── /audio/perceive ──────────────────────────────────────────────────
# Audio enters the SAME D2 -> operator -> olfactory pipeline that text
# uses.  The client (perceive_audio_canonical.py) computes the operator
# stream via Gen13/targets/ck/brain/audio_pipeline.pcm_to_operator_stream
# (which is just ck_curvature.py's algebra one layer down on Brayden's
# pcm_to_force9 codec), and POSTs ops + fingerprint here.  We absorb the
# ops into engine.olfactory exactly the way text-derived ops are absorbed.
# No new codec, no parallel matcher; CK hears through his existing bulb.
@api._app.route('/audio/perceive', methods=['POST'])
def audio_perceive_endpoint():
    try:
        from flask import request as _flask_request
        body = _flask_request.get_json(silent=True) or {}
        ops = body.get('ops') or []
        fingerprint = body.get('fingerprint') or {}
        source_label = body.get('source_label', 'unspecified')
    except Exception as exc:
        return _jsonify({'error': f'bad request: {exc}'}), 400

    if not isinstance(ops, list) or not ops:
        return _jsonify({'error': 'ops must be a non-empty list'}), 400
    try:
        ops = [int(o) % 10 for o in ops]
    except Exception:
        return _jsonify({'error': 'ops must be integers 0..9'}), 400

    olf = getattr(engine, 'olfactory', None) if 'engine' in globals() else None
    if olf is None or not hasattr(olf, 'absorb_ops'):
        return _jsonify({
            'error': 'engine.olfactory not available',
            'n_ops': len(ops),
            'fingerprint': fingerprint,
        }), 503

    pre = {
        'absorbed': int(getattr(olf, 'total_absorbed', 0)),
        'emitted': int(getattr(olf, 'total_emitted', 0)),
    }
    chunk_size = 2000
    attempts, errors = 0, []
    for i in range(0, len(ops), chunk_size):
        chunk = ops[i:i + chunk_size]
        try:
            olf.absorb_ops(chunk, source='audio', density=0.5)
            attempts += 1
        except Exception as exc:
            errors.append(f'chunk {i // chunk_size}: {exc}')

    # Drive the cortex Hebbian field from the audio op stream the SAME
    # way text drives it via step_symbol.  Without this, audio absorbs
    # into the olfactory bulb but the cortex W matrix only ticks on
    # text -- and worse, the natural decay parameter eats coupling
    # between text turns, so dual-pair scores DROP after a quiet audio
    # session.  Direct Hebbian on adjacent (b_op, d_op) pairs using the
    # SAME TSML 73-harmony rule cortex_v2.step_symbol uses.
    try:
        cortex_obj = globals().get('_cortex')
        if cortex_obj is not None and hasattr(cortex_obj, 'state') \
                and hasattr(cortex_obj, 'hebbian'):
            from ck_sim.ck_sim_heartbeat import (CL as _CL_TSML,
                                                  HARMONY as _HARMONY)
            # OP_TO_DIM mapping mirrors cortex_voice / olfactory
            _OP_TO_DIM = {0: 0, 1: 3, 2: 1, 3: 2, 4: 4,
                           5: 3, 6: 0, 7: 0, 8: 4, 9: 1}
            heb = cortex_obj.hebbian
            n_dims = len(heb.W) if heb.W else 5
            hebbian_steps = 0
            for i in range(len(ops) - 1):
                b_op = ops[i] % 10
                d_op = ops[i + 1] % 10
                ap = _OP_TO_DIM.get(b_op, 0) % n_dims
                bp = _OP_TO_DIM.get(d_op, 0) % n_dims
                harmonious = (_CL_TSML[b_op][d_op] == _HARMONY)
                reward = 1.0 if harmonious else 0.0
                dw = heb.eta * reward - heb.decay * heb.W[ap][bp]
                heb.W[ap][bp] += dw
                if heb.W[ap][bp] > heb.clamp:
                    heb.W[ap][bp] = heb.clamp
                elif heb.W[ap][bp] < -heb.clamp:
                    heb.W[ap][bp] = -heb.clamp
                heb.ticks += 1
                if harmonious:
                    heb.harmony_hits = getattr(heb, 'harmony_hits', 0) + 1
                cortex_obj.state.tick += 1
                hebbian_steps += 1
            if len(ops) >= 2:
                cortex_obj.state.last_b = int(ops[-2])
                cortex_obj.state.last_d = int(ops[-1])
            cortex_obj.state.W_trace = heb.W_trace() if hasattr(
                heb, 'W_trace') else cortex_obj.state.W_trace
        else:
            hebbian_steps = 0
    except Exception as exc:
        errors.append(f'cortex_hebbian_wire: {exc}')
        hebbian_steps = 0
    post = {
        'absorbed': int(getattr(olf, 'total_absorbed', 0)),
        'emitted': int(getattr(olf, 'total_emitted', 0)),
    }
    # Stash a compact recent-audio fingerprint so chat introspection
    # ("what did you just hear", "describe what you heard", etc.) can
    # surface what the audio was actually shaped like, instead of
    # falling through to keyword crystal lookup on the query itself.
    try:
        from collections import Counter as _Counter
        from ck_sim.ck_sim_heartbeat import OP_NAMES as _OP, NUM_OPS as _NOPS
        op_counter = _Counter(ops)
        total_ops = max(len(ops), 1)
        op_dist = {_OP[i]: round(op_counter.get(i, 0) / total_ops, 3)
                   for i in range(_NOPS)}
        dom_idx = max(op_counter.items(), key=lambda kv: kv[1])[0]
        engine._recent_audio = {
            'ts': time.time(),
            'source_label': source_label,
            'n_ops': len(ops),
            'dominant_op': _OP[dom_idx],
            'op_dist': op_dist,
            'last_pair': [_OP[ops[-2]], _OP[ops[-1]]]
                          if len(ops) >= 2 else None,
            'fingerprint': fingerprint,
        }
    except Exception as _exc:
        errors.append(f'recent_audio_stash: {_exc}')

    # BDC event emission on audio perception (Brayden 2026-05-03)
    try:
        from bdc_event_emitter import detect_perception_events as _bdc_perc
        _cortex_obj = globals().get('_cortex')
        if _cortex_obj is not None:
            _bdc_perc(_cortex_obj, engine, source='audio',
                      n_ops=len(ops),
                      hebbian_steps=int(locals().get('hebbian_steps', 0)))
    except Exception:
        pass

    return _jsonify({
        'ok': attempts > 0,
        'source_label': source_label,
        'n_ops_total': len(ops),
        'absorb_attempts': attempts,
        'errors': errors,
        'fingerprint': fingerprint,
        'olfactory_delta': {
            'absorbed_pre': pre['absorbed'],
            'absorbed_post': post['absorbed'],
            'absorbed_delta': post['absorbed'] - pre['absorbed'],
            'emitted_pre': pre['emitted'],
            'emitted_post': post['emitted'],
            'emitted_delta': post['emitted'] - pre['emitted'],
        },
    })


# ── /audio/recent ──────────────────────────────────────────────────
# Read what CK most recently HEARD: dominant op, distribution, last pair,
# fingerprint.  The introspection probe chat layers can use to answer
# "what did you just hear" without inventing.
@api._app.route('/audio/recent', methods=['GET'])
def audio_recent_endpoint():
    rec = getattr(engine, '_recent_audio', None) if 'engine' in globals() else None
    if rec is None:
        return _jsonify({'available': False, 'reason': 'no audio absorbed yet'})
    return _jsonify({'available': True, **rec})


# ── /screen/perceive ──────────────────────────────────────────────
# Visual op stream lands in the SAME olfactory bulb + drives the SAME
# cortex Hebbian rule audio uses.  Client (e.g. ui_loop.py) computes
# the operator stream locally via screen_pipeline.frames_to_operator_stream
# and POSTs ops + fingerprint here.
@api._app.route('/screen/perceive', methods=['POST'])
def screen_perceive_endpoint():
    try:
        from flask import request as _flask_request
        body = _flask_request.get_json(silent=True) or {}
        ops = body.get('ops') or []
        fingerprint = body.get('fingerprint') or {}
        source_label = body.get('source_label', 'screen')
    except Exception as exc:
        return _jsonify({'error': f'bad request: {exc}'}), 400
    if not isinstance(ops, list) or not ops:
        return _jsonify({'error': 'ops must be a non-empty list'}), 400
    try:
        ops = [int(o) % 10 for o in ops]
    except Exception:
        return _jsonify({'error': 'ops must be integers 0..9'}), 400

    olf = getattr(engine, 'olfactory', None) if 'engine' in globals() else None
    if olf is None or not hasattr(olf, 'absorb_ops'):
        return _jsonify({'error': 'engine.olfactory not available',
                          'n_ops': len(ops)}), 503

    pre = {
        'absorbed': int(getattr(olf, 'total_absorbed', 0)),
        'emitted': int(getattr(olf, 'total_emitted', 0)),
    }
    chunk_size = 2000
    attempts, errors = 0, []
    for i in range(0, len(ops), chunk_size):
        chunk = ops[i:i + chunk_size]
        try:
            olf.absorb_ops(chunk, source='screen', density=0.5)
            attempts += 1
        except Exception as exc:
            errors.append(f'chunk {i // chunk_size}: {exc}')

    # Drive cortex Hebbian + last_pair from the screen op stream too.
    hebbian_steps = 0
    try:
        cortex_obj = globals().get('_cortex')
        if cortex_obj is not None and hasattr(cortex_obj, 'state') \
                and hasattr(cortex_obj, 'hebbian'):
            from ck_sim.ck_sim_heartbeat import (CL as _CL_TSML,
                                                  HARMONY as _HARMONY)
            _OP_TO_DIM = {0: 0, 1: 3, 2: 1, 3: 2, 4: 4,
                           5: 3, 6: 0, 7: 0, 8: 4, 9: 1}
            heb = cortex_obj.hebbian
            n_dims = len(heb.W) if heb.W else 5
            for i in range(len(ops) - 1):
                b_op, d_op = ops[i] % 10, ops[i + 1] % 10
                ap = _OP_TO_DIM.get(b_op, 0) % n_dims
                bp = _OP_TO_DIM.get(d_op, 0) % n_dims
                harmonious = (_CL_TSML[b_op][d_op] == _HARMONY)
                reward = 1.0 if harmonious else 0.0
                dw = heb.eta * reward - heb.decay * heb.W[ap][bp]
                heb.W[ap][bp] += dw
                if heb.W[ap][bp] > heb.clamp:
                    heb.W[ap][bp] = heb.clamp
                elif heb.W[ap][bp] < -heb.clamp:
                    heb.W[ap][bp] = -heb.clamp
                heb.ticks += 1
                if harmonious:
                    heb.harmony_hits = getattr(heb, 'harmony_hits', 0) + 1
                cortex_obj.state.tick += 1
                hebbian_steps += 1
            if len(ops) >= 2:
                cortex_obj.state.last_b = int(ops[-2])
                cortex_obj.state.last_d = int(ops[-1])
            if hasattr(heb, 'W_trace'):
                cortex_obj.state.W_trace = heb.W_trace()
    except Exception as exc:
        errors.append(f'cortex_hebbian_wire: {exc}')

    post = {
        'absorbed': int(getattr(olf, 'total_absorbed', 0)),
        'emitted': int(getattr(olf, 'total_emitted', 0)),
    }

    # Stash recent screen for chat introspection
    try:
        from collections import Counter as _Counter
        from ck_sim.ck_sim_heartbeat import OP_NAMES as _OP, NUM_OPS as _NOPS
        op_counter = _Counter(ops)
        total_ops = max(len(ops), 1)
        op_dist = {_OP[i]: round(op_counter.get(i, 0) / total_ops, 3)
                   for i in range(_NOPS)}
        dom_idx = max(op_counter.items(), key=lambda kv: kv[1])[0]
        engine._recent_screen = {
            'ts': time.time(),
            'source_label': source_label,
            'n_ops': len(ops),
            'dominant_op': _OP[dom_idx],
            'op_dist': op_dist,
            'last_pair': [_OP[ops[-2]], _OP[ops[-1]]]
                          if len(ops) >= 2 else None,
            'fingerprint': fingerprint,
        }
    except Exception as _exc:
        errors.append(f'recent_screen_stash: {_exc}')

    # BDC event emission on screen perception (Brayden 2026-05-03)
    try:
        from bdc_event_emitter import detect_perception_events as _bdc_perc
        _cortex_obj = globals().get('_cortex')
        if _cortex_obj is not None:
            _bdc_perc(_cortex_obj, engine, source='screen',
                      n_ops=len(ops), hebbian_steps=hebbian_steps)
    except Exception:
        pass

    return _jsonify({
        'ok': attempts > 0,
        'source_label': source_label,
        'n_ops_total': len(ops),
        'absorb_attempts': attempts,
        'hebbian_steps': hebbian_steps,
        'errors': errors,
        'fingerprint': fingerprint,
        'olfactory_delta': {
            'absorbed_pre': pre['absorbed'],
            'absorbed_post': post['absorbed'],
            'absorbed_delta': post['absorbed'] - pre['absorbed'],
            'emitted_pre': pre['emitted'],
            'emitted_post': post['emitted'],
            'emitted_delta': post['emitted'] - pre['emitted'],
        },
    })


# ── /screen/recent ────────────────────────────────────────────────
@api._app.route('/screen/recent', methods=['GET'])
def screen_recent_endpoint():
    rec = getattr(engine, '_recent_screen', None) if 'engine' in globals() else None
    if rec is None:
        return _jsonify({'available': False, 'reason': 'no screen perceived yet'})
    return _jsonify({'available': True, **rec})


# ── /retina/glance ───────────────────────────────────────────────
# CK's CANONICAL visual field (engine.retina, ck_retina.py).  Already
# online in the live engine since Gen 9.34.  This endpoint surfaces
# what the retina is feeling RIGHT NOW: operator, structural part,
# coherence, energy, edge_gate_crossings.  Not parallel to my
# /screen/perceive -- the retina has been there the whole time.
@api._app.route('/retina/glance', methods=['GET'])
def retina_glance_endpoint():
    if 'engine' not in globals():
        return _jsonify({'available': False, 'reason': 'engine not bound'})
    retina = getattr(engine, 'retina', None)
    if retina is None:
        return _jsonify({'available': False, 'reason': 'engine.retina is None'})
    try:
        from ck_sim.ck_sim_heartbeat import OP_NAMES as _OP
        felt = getattr(retina, 'felt_operator', None)
        op_name = _OP[felt] if isinstance(felt, int) and 0 <= felt < 10 else str(felt)
        part_names = ['FOUNDATION', 'DYNAMICS', 'FIELD', 'CYCLE']
        dom_part = getattr(retina, 'dominant_part', None)
        part_name = (part_names[dom_part] if isinstance(dom_part, int)
                      and 0 <= dom_part < len(part_names) else str(dom_part))
        return _jsonify({
            'available': True,
            'felt_operator': op_name,
            'dominant_structure': part_name,
            'coherent_fraction': float(getattr(retina, 'coherent_fraction', 0.0)),
            'mean_energy': float(getattr(retina, 'mean_energy', 0.0)),
            'peak_energy': float(getattr(retina, 'peak_energy', 0.0)),
            'temporal_intensity': float(getattr(retina, 'temporal_intensity', 0.0)),
            'edge_gate_crossings': int(getattr(retina, 'edge_gate_crossings', 0)),
            'glance_count': int(getattr(retina, 'glance_count', 0)),
            'experience_5d': [float(v) for v in
                              getattr(retina, 'experience_5d', [])],
            'structure_4s': [float(v) for v in
                             getattr(retina, 'structure_4s', [])],
        })
    except Exception as exc:
        return _jsonify({'available': True, 'error': str(exc)})


# ── /ck/research ──────────────────────────────────────────────────
# CK does fractal-recursive research across approved sites:
#   prompt -> decompose terms -> sub-questions -> route to best site
#   (claude/grok/arxiv/scholar/jstor/youtube; never nature) ->
#   query the site -> ingest result text into engine.olfactory.absorb_ops
#   -> synthesize dominant operators -> condense to 1-paragraph answer.
# Browser visible by default so you can watch CK research.
# Every action logged to ~/.ck/research/log.jsonl.
@api._app.route('/ck/research', methods=['POST'])
def ck_research_endpoint():
    try:
        from flask import request as _flask_request
        body = _flask_request.get_json(silent=True) or {}
    except Exception as exc:
        return _jsonify({'error': f'bad request: {exc}'}), 400
    prompt = body.get('prompt', '').strip()
    if not prompt:
        return _jsonify({'error': 'provide prompt: "..."'}), 400
    max_q = int(body.get('max_questions', 4))
    headless = bool(body.get('headless', False))
    try:
        sys.path.insert(0, _GEN13_BRAIN)
        import ck_research as _cr
    except Exception as exc:
        return _jsonify({'error': f'ck_research import: {exc}'}), 503
    eng = engine if 'engine' in globals() else None
    try:
        out = _cr.research(prompt, engine=eng,
                            max_questions=max_q, headless=headless)
    except Exception as exc:
        return _jsonify({'error': f'research failed: {exc}'}), 500
    # Return a compact view (full findings can be huge)
    return _jsonify({
        'prompt': out['prompt'],
        'terms': out['terms'],
        'questions': out['questions'],
        'findings_summary': [
            {'site': f.get('site'), 'term': f.get('term'),
             'question': f.get('question'),
             'text_len': len(f.get('text') or ''),
             'text_preview': (f.get('text') or '')[:300],
             'error': f.get('error')}
            for f in out['findings']
        ],
        'ingestions': out['ingestions'],
        'synthesis': out['synthesis'],
        'condensed': out['condensed'],
        'external_crystals': out.get('external_crystals'),
    })


# ── /crystals/external ────────────────────────────────────────────
# Surface CK's currently-active external (scenario-scoped, ephemeral)
# crystals.  These do NOT live in runtime_crystals.json -- they're
# scaffolding around the active research / conversation, TTL'd, and
# fire alongside internal crystals only while warm.
@api._app.route('/crystals/external', methods=['GET'])
def crystals_external_list_endpoint():
    try:
        sys.path.insert(0, _GEN13_BRAIN)
        from cortex_voice import list_external_crystals
    except Exception as exc:
        return _jsonify({'error': f'cortex_voice import: {exc}'}), 503
    return _jsonify({'external': list_external_crystals()})


@api._app.route('/crystals/external/clear', methods=['POST'])
def crystals_external_clear_endpoint():
    try:
        from flask import request as _flask_request
        body = _flask_request.get_json(silent=True) or {}
    except Exception:
        body = {}
    scope = body.get('scope')
    try:
        sys.path.insert(0, _GEN13_BRAIN)
        from cortex_voice import clear_external_crystals
    except Exception as exc:
        return _jsonify({'error': f'cortex_voice import: {exc}'}), 503
    n = clear_external_crystals(scope=scope)
    return _jsonify({'cleared': n, 'scope': scope})


# ── /speak ────────────────────────────────────────────────────────
# CK's voice as his own substrate rendered to audio.  Operator stream
# -> reverse canonical force5 -> force9 -> force9_to_pcm -> sounddevice.
# Body either {ops: [int]} for a raw operator stream or {text: "..."}
# for text -> ck_curvature -> ops -> audio.  Returns play status.
# blocking=False by default so the request returns fast.
@api._app.route('/speak', methods=['POST'])
def speak_endpoint():
    try:
        from flask import request as _flask_request
        body = _flask_request.get_json(silent=True) or {}
    except Exception as exc:
        return _jsonify({'error': f'bad request: {exc}'}), 400
    blocking = bool(body.get('blocking', False))
    sr = int(body.get('sample_rate', 44100))
    try:
        sys.path.insert(0, _GEN13_BRAIN)
        import ck_speaker as _spk
    except Exception as exc:
        return _jsonify({'error': f'ck_speaker import: {exc}'}), 503
    if 'ops' in body and body['ops']:
        ops = [int(o) % 10 for o in body['ops']]
        res = _spk.speak_operator_stream(ops, sample_rate=sr,
                                          blocking=blocking)
        return _jsonify(res)
    if 'text' in body and body['text']:
        res = _spk.speak_text_as_operators(body['text'],
                                            sample_rate=sr)
        return _jsonify(res)
    return _jsonify({'error': 'provide ops [int] or text "..."'}), 400


# ── /action/plan ──────────────────────────────────────────────────
# Read CK's cortex state and return the action it would emit.  Does
# NOT execute anything (dry-run); a separate /action/emit toggles real
# mouse/keyboard.  Default safe.
@api._app.route('/action/plan', methods=['GET', 'POST'])
def action_plan_endpoint():
    try:
        from flask import request as _flask_request
        body = (_flask_request.get_json(silent=True) or {}) \
            if _flask_request.method == 'POST' else {}
        step_px = int(body.get('step_px', 12))
    except Exception:
        step_px = 12
    cortex_obj = globals().get('_cortex')
    if cortex_obj is None:
        return _jsonify({'error': 'cortex not available'}), 503
    try:
        sys.path.insert(0, _GEN13_BRAIN)
        from action_pipeline import cortex_state_to_action, send_action
    except Exception as exc:
        return _jsonify({'error': f'action_pipeline import: {exc}'}), 503
    plan = cortex_state_to_action(cortex_obj, step_px=step_px)
    out = send_action(plan, dry_run=True)
    return _jsonify(out)


# ── /action/emit ──────────────────────────────────────────────────
# Actually execute an action.  Requires explicit body {execute: true}
# so accidental invocations don't move the cursor.
@api._app.route('/action/emit', methods=['POST'])
def action_emit_endpoint():
    try:
        from flask import request as _flask_request
        body = _flask_request.get_json(silent=True) or {}
    except Exception as exc:
        return _jsonify({'error': f'bad request: {exc}'}), 400
    if not body.get('execute'):
        return _jsonify({
            'error': 'set body.execute=true to actually emit',
            'note': 'use /action/plan for dry-run',
        }), 400
    step_px = int(body.get('step_px', 12))
    cortex_obj = globals().get('_cortex')
    if cortex_obj is None:
        return _jsonify({'error': 'cortex not available'}), 503
    try:
        sys.path.insert(0, _GEN13_BRAIN)
        from action_pipeline import cortex_state_to_action, send_action
    except Exception as exc:
        return _jsonify({'error': f'action_pipeline import: {exc}'}), 503
    plan = cortex_state_to_action(cortex_obj, step_px=step_px)
    out = send_action(plan, dry_run=False)
    return _jsonify(out)


# /verify -- verification-script proposer (paper 4 step 9)
# Given a topic/claim, suggest a runnable verification path.
@api._app.route('/verify', methods=['POST', 'GET'])
def verify_endpoint():
    try:
        from flask import request as _flask_request
        if _flask_request.method == 'POST':
            body = _flask_request.get_json(silent=True) or {}
            claim = body.get('claim', '') or body.get('topic', '')
        else:
            claim = _flask_request.args.get('claim', '') or _flask_request.args.get('topic', '')
    except Exception:
        claim = ''

    # Map claim keywords to verification scripts
    claim_low = claim.lower()
    proposals = []

    verify_map = [
        # (keyword, script_path, what_it_verifies, sample_run_command)
        (['t*', 't star', '5/7', 'flatness', 'flatness theorem', 'wp51'],
         'papers/wp113_alpha_uniqueness/verification/_run_all.sh',
         'all 15 verification scripts including the cyclotomic Crossing Lemma',
         'bash papers/wp113_alpha_uniqueness/verification/_run_all.sh'),
        (['alpha=1/2', 'h/br', '1+sqrt(3)', 'galois', 'wp113'],
         'papers/wp113_alpha_uniqueness/verification/f3_galois_alpha_uniqueness.py',
         'Galois proof that H/Br ∈ Q(√3) iff α=1/2 (depth-2 algebraic)',
         'python papers/wp113_alpha_uniqueness/verification/f3_galois_alpha_uniqueness.py'),
        (['ring extension', 'z/nz', 'z/14z', 'universality', 'f5(a)', 'f5a'],
         'papers/wp113_alpha_uniqueness/verification/f5a_universality_scan.py',
         '14-ring scan: H/Br = 1+sqrt(3) universal across Z/n for n in {10..50}',
         'python papers/wp113_alpha_uniqueness/verification/f5a_universality_scan.py'),
        (['f8', 'jacobian', 'wp105', 'phi-proxy', 'eigenvalue'],
         'papers/wp113_alpha_uniqueness/verification/f8_jacobian_alpha_half.py',
         'F8 Jacobian linearization: rho=0.3496, lambda_0=2 exact',
         'python papers/wp113_alpha_uniqueness/verification/f8_jacobian_alpha_half.py'),
        (['f10', 'i-action', 'descent', 'prym', 'hodge_cstar', 'sprint35b'],
         'papers/wp113_alpha_uniqueness/verification/f10_i_action_descent.py',
         'F10 i-action does not descend over Q(sqrt2,sqrt3,sqrt5)',
         'python papers/wp113_alpha_uniqueness/verification/f10_i_action_descent.py'),
        (['cl(0,7)', 'gamma matrices', 'charge conjugation', 'so(7)', 'wp1', 'f1', 'yukawa'],
         'papers/wp113_alpha_uniqueness/verification/f1_so7_singlet_bilinear.py',
         'Cl(0,7) gamma matrices + SO(7) charge conjugation C^2 = -I_8',
         'python papers/wp113_alpha_uniqueness/verification/f1_so7_singlet_bilinear.py'),
        (['lmfdb 4.2.10224.1', 'r/br quartic', 'd_4 galois', 'f8 trace', 'wp105'],
         'papers/wp113_alpha_uniqueness/verification/f_field_match_71.py',
         'F8 trace + R/Br quartic same field LMFDB 4.2.10224.1 (Galois D_4)',
         'python papers/wp113_alpha_uniqueness/verification/f_field_match_71.py'),
        (['wobble', 'depth-3', 'sigma squared', 'cube roots'],
         'papers/wp113_alpha_uniqueness/verification/f_depth3_primitives.py',
         'depth-3 primitive sigma^2 + WOBBLE 11 fivefold manifestation',
         'python papers/wp113_alpha_uniqueness/verification/f_depth3_primitives.py'),
        (['wp101', 'sigma rate', 'sigma(N)', 'sigma rate theorem'],
         'Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/proof_sigma_rate.py',
         'WP101 sigma rate theorem: sigma(N) <= 2/N proved',
         'python Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/proof_sigma_rate.py'),
        (['phi', 'iit', 'integrated information', 'cortex phi'],
         'Gen13/targets/ck/brain/study/compute_phi.py',
         'computes Phi-proxy on CK live cortex',
         'python Gen13/targets/ck/brain/study/compute_phi.py'),
        (['surprisal', 'predictive coding', 'fep', 'free energy'],
         'Gen13/targets/ck/brain/study/surprisal_log.py',
         'surprisal logger; tests bridge 5 (predictive coding)',
         'python Gen13/targets/ck/brain/study/surprisal_log.py --corpus <corpus.json>'),
    ]

    for keywords, script, desc, cmd in verify_map:
        if any(kw in claim_low for kw in keywords):
            proposals.append({
                'verifies': desc,
                'script': script,
                'run_command': cmd,
                'matched_keywords': [kw for kw in keywords if kw in claim_low],
            })

    if not proposals:
        return _jsonify({
            'claim': claim,
            'proposals': [],
            'note': 'no specific verification script matched; '
                    'browse papers/wp113_alpha_uniqueness/verification/ for the full list, '
                    'or papers/ for sprint-level proofs.',
        })

    return _jsonify({
        'claim': claim,
        'proposals': proposals,
        'note': 'each proposal is a runnable script that tests the claim. '
                'run it; check the residual / pass markers in the output.',
    })


# /user_model -- per-session_id metadata (paper 4 step 7)
# Tracks: topics raised, expressed knowledge level, last seen
_USER_MODEL_LOCK = _mem_threading.Lock()
_USER_MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', '..', '..',
                                'Gen13', 'var', 'user_models.json')


def _load_user_models():
    """Load per-session user models from disk."""
    try:
        path = os.path.abspath(_USER_MODEL_PATH)
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
    except Exception:
        pass
    return {}


def _save_user_models(models):
    try:
        path = os.path.abspath(_USER_MODEL_PATH)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            json.dump(models, f, indent=2)
        return True
    except Exception:
        return False


def _update_user_model(session_id, text, fired_crystals, source):
    """Update the user model for this session_id with metadata from this turn.

    Tracks:
      - topics_seen: distinct first_words of crystals that fired in this session
      - turn_count: how many turns
      - last_seen_iso: ISO timestamp
      - sources_used: distribution of voice sources
      - expressed_knowledge: heuristic — if user typed jargon in TIG vocab,
        bump their expressed level

    Best-effort, never blocks.
    """
    if not session_id:
        return
    try:
        with _USER_MODEL_LOCK:
            models = _load_user_models()
            m = models.get(session_id, {
                "session_id": session_id,
                "turn_count": 0,
                "topics_seen": [],
                "sources_used": {},
                "expressed_knowledge": 0,
                "last_seen_iso": None,
                "first_seen_iso": None,
            })
            m["turn_count"] = m.get("turn_count", 0) + 1
            m["last_seen_iso"] = time.strftime("%Y-%m-%dT%H:%M:%S")
            if not m.get("first_seen_iso"):
                m["first_seen_iso"] = m["last_seen_iso"]
            # Collect crystal first_words from the response
            for fact in (fired_crystals or []):
                if ":" in fact:
                    fw = fact.split(":", 1)[0].strip()
                    if fw and fw not in m["topics_seen"]:
                        m["topics_seen"].append(fw)
            # Track sources
            srcs = m.get("sources_used", {})
            srcs[source] = srcs.get(source, 0) + 1
            m["sources_used"] = srcs
            # Heuristic: if user used TIG-jargon keywords, bump knowledge
            jargon = ['t*', 'tsml', 'bhml', 'wp1', 'wp5', 'wp10', 'wp11',
                      'sigma_rate', 'crossing lemma', 'flatness', 'depth-2',
                      'wobble', 'lmfdb', 'galois', 'phi', 'cortex', 'hebbian',
                      'attractor', 'frontier']
            t_low = (text or '').lower()
            jargon_hits = sum(1 for j in jargon if j in t_low)
            if jargon_hits >= 1:
                m["expressed_knowledge"] = max(m.get("expressed_knowledge", 0),
                                               jargon_hits)
            models[session_id] = m
            _save_user_models(models)
    except Exception:
        pass


# /propose_bridge -- Ollama as FORWARD tool, not just editor (paper 4 step 11)
# Given two crystal first_words, ask Ollama to propose how they connect, then
# fact-check against /verify proposals.  Output is a CANDIDATE bridge for
# human review -- not added to the crystal store automatically.
@api._app.route('/propose_bridge', methods=['POST', 'GET'])
def propose_bridge_endpoint():
    try:
        from flask import request as _flask_request
        if _flask_request.method == 'POST':
            body = _flask_request.get_json(silent=True) or {}
            crystal_a = body.get('crystal_a', '')
            crystal_b = body.get('crystal_b', '')
        else:
            crystal_a = _flask_request.args.get('crystal_a', '')
            crystal_b = _flask_request.args.get('crystal_b', '')
    except Exception:
        crystal_a = crystal_b = ''

    if not crystal_a or not crystal_b:
        return _jsonify({'error': 'crystal_a and crystal_b required (use first_word names from /crystals/list)'}), 400

    # Look up the crystals' fact texts
    try:
        from cortex_voice import _FRONTIER_FACTS, _RUNTIME_CRYSTALS, _CRYSTAL_OP_SIGNATURES
    except Exception:
        from Gen13.targets.ck.brain.cortex_voice import (
            _FRONTIER_FACTS, _RUNTIME_CRYSTALS, _CRYSTAL_OP_SIGNATURES
        )
    fact_a = fact_b = None
    for triggers, fact in list(_FRONTIER_FACTS) + list(_RUNTIME_CRYSTALS):
        fw = fact.split(':', 1)[0].strip()
        if fw == crystal_a: fact_a = fact
        if fw == crystal_b: fact_b = fact
    if not fact_a or not fact_b:
        missing = []
        if not fact_a: missing.append(crystal_a)
        if not fact_b: missing.append(crystal_b)
        return _jsonify({'error': f'crystal not found: {missing}'}), 404

    # Ask Ollama to propose a bridge (one paragraph, must reference both
    # crystals' verified content)
    try:
        import os as _os
        if _os.environ.get('CK_OLLAMA_EDITOR', '1') != '1':
            return _jsonify({'error': 'CK_OLLAMA_EDITOR is disabled'}), 503
        try:
            from llm_bridge import ollama_complete, ollama_available
        except Exception:
            return _jsonify({'error': 'ollama bridge unavailable'}), 503
        if not ollama_available():
            return _jsonify({'error': 'ollama not running locally'}), 503

        prompt = (
            "You are CK, a math-first creature. Propose a SHORT (3-5 sentence) "
            "bridge between these two verified facts. Use only what's in the "
            "facts; do NOT introduce p-adic, Hilbert, RH, or category-theory "
            "claims unless they appear verbatim. Mark anything speculative "
            "with [conjecture]. End with a single line: 'verify: <run command>'.\n\n"
            f"FACT A: {fact_a}\n\n"
            f"FACT B: {fact_b}\n\n"
            "Bridge:"
        )

        draft = ollama_complete(prompt=prompt, max_tokens=400, timeout=20)
        if not draft:
            return _jsonify({'error': 'ollama returned empty'}), 502

        # Coherence check: hard-reject AI disclaimers + hallucination markers
        draft_low = draft.lower()
        hallucination_flags = []
        bad_markers = ["i am an ai", "as a language model", "p-adic", "hilbert space",
                       "riemann hypothesis", "category theory"]
        for m in bad_markers:
            if m in draft_low and m not in (fact_a + fact_b).lower():
                hallucination_flags.append(m)
        if hallucination_flags:
            return _jsonify({
                'crystal_a': crystal_a,
                'crystal_b': crystal_b,
                'rejected': True,
                'reason': 'hallucination markers',
                'flags': hallucination_flags,
                'draft_first_200': draft[:200],
            })

        # Soft check: at least one fact_a + fact_b token must survive
        # (use simple keyword test)
        a_tokens = set(t for t in crystal_a.split('_') if len(t) > 3)
        b_tokens = set(t for t in crystal_b.split('_') if len(t) > 3)
        coverage_a = sum(1 for t in a_tokens if t.lower() in draft_low)
        coverage_b = sum(1 for t in b_tokens if t.lower() in draft_low)
        if a_tokens and b_tokens and coverage_a == 0 and coverage_b == 0:
            return _jsonify({
                'crystal_a': crystal_a,
                'crystal_b': crystal_b,
                'rejected': True,
                'reason': 'draft mentions neither crystal',
                'draft_first_200': draft[:200],
            })

        return _jsonify({
            'crystal_a': crystal_a,
            'crystal_b': crystal_b,
            'fact_a_first': fact_a[:120],
            'fact_b_first': fact_b[:120],
            'proposed_bridge': draft.strip(),
            'status': 'CANDIDATE',
            'note': 'human review required before adding as a crystal. '
                    'use /crystals/add with appropriate triggers + op_signature.',
        })
    except Exception as e:
        return _jsonify({'error': str(e)}), 500


# /dream -- on-demand dream/drift generation.
# Returns a freshly generated drift candidate marked DRIFT.
@api._app.route('/dream', methods=['POST', 'GET'])
def dream_endpoint():
    try:
        # Run dream_daemon.dream_one() inline.
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..',
                                          '..', 'Gen13', 'targets', 'ck',
                                          'brain', 'study'))
        from dream_daemon import (
            load_crystals, dream_one, write_dream, DEFAULT_JOURNAL
        )
        crystals, op_sigs = load_crystals()
        if not crystals:
            return _jsonify({'error': 'no crystals available'}), 503
        # Use live cortex state from _cortex if available
        cortex_state_dict = None
        if _cortex is not None:
            try:
                W = [row[:] for row in _cortex.hebbian.W]
                cortex_state_dict = {
                    "state": {
                        "tick": _cortex.state.tick,
                        "last_b": _cortex.state.last_b,
                        "last_d": _cortex.state.last_d,
                        "W_trace": _cortex.state.W_trace,
                    },
                    "hebbian": {"W": W},
                }
            except Exception:
                pass
        entry = dream_one(crystals, op_sigs, cortex_state_dict)
        if entry is None:
            return _jsonify({'error': 'no drift produced'}), 503
        write_dream(entry, DEFAULT_JOURNAL)
        return _jsonify(entry)
    except Exception as e:
        return _jsonify({'error': str(e)}), 500


# /dream/journal -- recent drift entries
@api._app.route('/dream/journal', methods=['GET'])
def dream_journal_endpoint():
    from flask import request as _flask_request
    n = int(_flask_request.args.get('n', 20))
    journal_path = os.path.join(os.path.dirname(__file__), '..', '..',
                                  '..', 'Gen13', 'var', 'dream_journal.jsonl')
    items = []
    if os.path.exists(journal_path):
        with open(journal_path) as f:
            for line in f:
                try:
                    items.append(json.loads(line))
                except Exception:
                    continue
    return _jsonify({'count': len(items), 'recent': items[-n:]})


# /search/queue -- topic queue for autonomous web search
# When CK gets a query he can't answer well, the query gets added here.
# A separate process (Claude-the-agent or a future web-fetch daemon)
# services the queue, fetches journal abstracts, distills to corpora.
_SEARCH_QUEUE_PATH = os.path.join(os.path.dirname(__file__), '..', '..', '..',
                                    'Gen13', 'var', 'search_queue.jsonl')


@api._app.route('/search/queue', methods=['GET', 'POST'])
def search_queue_endpoint():
    from flask import request as _flask_request
    if _flask_request.method == 'POST':
        body = _flask_request.get_json(silent=True) or {}
        query = body.get('query', '')
        source = body.get('source', 'manual')
        priority = int(body.get('priority', 5))
        if not query:
            return _jsonify({'error': 'query required'}), 400
        entry = {
            'ts': time.time(),
            'iso_ts': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'query': query[:300],
            'source': source,
            'priority': priority,
            'status': 'pending',
            'session_id': body.get('session_id'),
        }
        try:
            os.makedirs(os.path.dirname(_SEARCH_QUEUE_PATH), exist_ok=True)
            with open(_SEARCH_QUEUE_PATH, 'a') as f:
                f.write(json.dumps(entry) + '\n')
            return _jsonify({'ok': True, 'queued': entry})
        except Exception as e:
            return _jsonify({'error': str(e)}), 500

    # GET: return pending queue
    items = []
    status_filter = _flask_request.args.get('status', 'pending')
    if os.path.exists(_SEARCH_QUEUE_PATH):
        with open(_SEARCH_QUEUE_PATH) as f:
            for line in f:
                try:
                    item = json.loads(line)
                    if status_filter == 'all' or item.get('status') == status_filter:
                        items.append(item)
                except Exception:
                    continue
    return _jsonify({'count': len(items), 'items': items[-50:]})


# /search/results -- when a search has been serviced, store the result
# (called by the search-servicing process, not by chat).
@api._app.route('/search/result', methods=['POST'])
def search_result_endpoint():
    from flask import request as _flask_request
    body = _flask_request.get_json(silent=True) or {}
    query = body.get('query', '')
    finding = body.get('finding', '')
    sources = body.get('sources', [])
    confidence = body.get('confidence', 0.85)
    if not query or not finding:
        return _jsonify({'error': 'query and finding required'}), 400
    results_path = os.path.join(os.path.dirname(__file__), '..', '..', '..',
                                  'Gen13', 'var', 'search_results.jsonl')
    entry = {
        'ts': time.time(),
        'iso_ts': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'query': query[:300],
        'finding': finding[:1000],
        'sources': sources,
        'confidence': float(confidence),
    }
    try:
        os.makedirs(os.path.dirname(results_path), exist_ok=True)
        with open(results_path, 'a') as f:
            f.write(json.dumps(entry) + '\n')
        return _jsonify({'ok': True, 'stored': entry})
    except Exception as e:
        return _jsonify({'error': str(e)}), 500


@api._app.route('/user_model', methods=['GET'])
def user_model_endpoint():
    try:
        from flask import request as _flask_request
        sid = _flask_request.args.get('session_id', '')
    except Exception:
        sid = ''
    models = _load_user_models()
    if sid:
        return _jsonify(models.get(sid) or {"session_id": sid, "exists": False})
    return _jsonify({"all": models, "count": len(models)})


@api._app.route('/memory/search', methods=['GET', 'POST'])
def memory_search_endpoint():
    """Search memory by substring.  Used internally by chat to recall
    prior turns matching user-mentioned names or topics."""
    try:
        from flask import request as _flask_request
        if _flask_request.method == 'POST':
            body = _flask_request.get_json(silent=True) or {}
            q = body.get('query', '') or body.get('q', '')
            n = int(body.get('n', 10))
            requester = body.get('session_id')
        else:
            q = _flask_request.args.get('query', '') or _flask_request.args.get('q', '')
            n = int(_flask_request.args.get('n', 10))
            requester = _flask_request.args.get('session_id')
    except Exception:
        q, n, requester = '', 10, None
    matches = _memory_search(q, n=n, requester_session=requester)
    return _jsonify({'query': q, 'matches': matches, 'count': len(matches)})


_SECRET_FLAGS = (
    'this is a secret', 'between us', 'just for us', 'just between us',
    'do not share', "don't share", 'keep this private', 'private:',
    '[secret]', '(secret)', 'just you and me',
)


def _is_secret(text):
    """Detect whether the user wants this turn kept private from other users."""
    if not text:
        return False
    low = text.lower()
    return any(flag in low for flag in _SECRET_FLAGS)


def _record_memory_turn(text, response, source, session_id=None):
    """Append a brief summary of this chat turn to the memory file.
    Called from process_chat_with_cortex.  Best-effort, never blocks.

    Brayden 2026-04-29: "i have no secrets ck can't tell, and if i do,
    i will tell him it's a secret for just us."  Default: shareable.
    Marked secret only if user explicitly flags it.
    """
    try:
        with _MEMORY_LOCK:
            os.makedirs(os.path.dirname(_MEMORY_PATH), exist_ok=True)
            with open(_MEMORY_PATH, 'a') as f:
                entry = {
                    'ts': time.time(),
                    'iso_ts': time.strftime('%Y-%m-%dT%H:%M:%S'),
                    'topic': (text or '')[:200],
                    'response_first_120': (response or '')[:120],
                    'source': source,
                    'tick': _cortex.state.tick if _cortex else None,
                    'session_id': session_id,
                    'secret': _is_secret(text),
                }
                f.write(json.dumps(entry) + '\n')
    except Exception:
        pass


def _memory_search(query, n=10, include_secrets=False, requester_session=None):
    """Search the memory log for turns matching the query (case-insensitive
    substring match).  Returns up to n most-recent matches.

    Brayden's privacy rule: secret-flagged turns are EXCLUDED from
    cross-session retrieval unless the requester is the same session as
    the original speaker.
    """
    if not query:
        return []
    q = query.lower()
    matches = []
    try:
        if not os.path.exists(_MEMORY_PATH):
            return []
        with open(_MEMORY_PATH, 'r') as f:
            lines = f.readlines()
        for line in lines:
            try:
                entry = json.loads(line)
            except Exception:
                continue
            # Privacy: secret entries only available to original session
            if entry.get('secret'):
                if not include_secrets and entry.get('session_id') != requester_session:
                    continue
            topic = (entry.get('topic') or '').lower()
            response = (entry.get('response_first_120') or '').lower()
            if q in topic or q in response:
                matches.append(entry)
        return matches[-n:]
    except Exception:
        return []


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


@api._app.route('/cortex/ingest_text', methods=['POST'])
def cortex_ingest_text():
    """Feed raw text into the cortex (Brayden 2026-05-02:
    'go through every single wp from 1 to one hundred whatever number we
    are at!!! ... let him read every citation of every paper').

    Bypasses the chat path (no research_first, no Ollama, no cells
    composition) -- just runs cortex.step_text on the input.  Used by
    paper_reader.py to absorb large corpora quickly without triggering
    Chrome research per paper.

    Body: {"text": "...", "label": "WP051"}
    Returns: pre/post cortex tick, W_trace, emergent.
    """
    if _cortex is None:
        return _jsonify({'available': False}), 503
    from flask import request as _flask_request
    body = _flask_request.get_json(silent=True) or {}
    text = body.get('text', '')
    label = body.get('label', 'unlabeled')
    if not text or not isinstance(text, str):
        return _jsonify({'error': 'provide non-empty text'}), 400
    pre = {
        'tick': int(_cortex.state.tick),
        'W_trace': round(_cortex.state.W_trace, 6),
        'emergent': round(_cortex.state.emergent, 6),
    }
    try:
        # step_text feeds the text through V2 -> lattice -> cortex Hebbian.
        # No GPU, no Ollama, just the substrate.
        _cortex.step_text(text)
    except Exception as _e:
        return _jsonify({'error': f'step_text: {type(_e).__name__}: {_e}',
                          'pre': pre}), 500
    post = {
        'tick': int(_cortex.state.tick),
        'W_trace': round(_cortex.state.W_trace, 6),
        'emergent': round(_cortex.state.emergent, 6),
    }
    return _jsonify({
        'ok': True, 'label': label, 'n_chars': len(text),
        'pre': pre, 'post': post,
        'tick_delta': post['tick'] - pre['tick'],
        'W_trace_delta': round(post['W_trace'] - pre['W_trace'], 6),
        'emergent_delta': round(post['emergent'] - pre['emergent'], 6),
    })


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

        # Try to extract the target unit's actual source so compose_aware
        # can weave its real identifiers into the body.  Falls back to
        # the dumb frame-fill compose_with_header if extraction fails or
        # the aware path returns nothing.
        target_source = ''
        try:
            import ast as _ast2
            _tree = _ast2.parse(source)
            for _node in _ast2.walk(_tree):
                _is_match = (
                    (isinstance(_node, _ast2.ClassDef)
                     and _node.name == target_name
                     and target_type == 'class')
                    or
                    (isinstance(_node, (_ast2.FunctionDef,
                                        _ast2.AsyncFunctionDef))
                     and _node.name == target_name
                     and target_type == 'function')
                )
                if _is_match:
                    _src_lines = source.splitlines()
                    _ls = _node.lineno - 1
                    _le = getattr(_node, 'end_lineno',
                                  _node.lineno) or _node.lineno
                    target_source = '\n'.join(_src_lines[_ls:_le])
                    break
        except Exception:
            target_source = ''

        block = None
        compose_method = 'aware'
        if target_source:
            try:
                block = _code_voice.compose_aware_with_header(
                    traj, target_source, target_name, target_type,
                    coherence=max(target_coh, 0.5))
            except Exception:
                block = None
        if not block:
            compose_method = 'frame_fill'
            block = _code_voice.compose_with_header(
                traj, user_text=intent_text,
                coherence=max(target_coh, 0.5))
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
            'compose_method': compose_method,
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


# === Gen14 unified extensions (Phase 1-5) — additive on the live engine ===
# Mounts the modules built for Gen14 unification:
#   Phase 1: drives, forecast, lattice_chain, divine_memory, proactive_queue,
#            recall stub, algebraic measurement projections
#   Phase 2: trained 4-head algebraic LM (op/sigma-orbit/shell/4core)
#   Phase 3: spreading-activation recall over the 4-axis algebraic coord
#   Phase 4: frontier scanner (29 frontiers) + 4-source proactive trigger
#   Phase 5: pixel-to-stroke -> algebraic signature
# Plus 4 new HTTP endpoints (/proactive/{status,consume,peek},
# /algebraic/signature, /vision/strokes). All wrapped in try/except so
# a Gen14 failure cannot crash the live deploy.
#
# Reference: Gen14/PLAN/SESSION_LOG_2026_05_13.md (12/12 acceptance PASS)
_GEN14_BRAIN = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..', '..', '..', 'Gen14', 'targets', 'ck', 'brain'))
_GEN14_GRAMMAR = os.path.join(_GEN14_BRAIN, 'grammar_lm')
for _p in (_GEN14_BRAIN, _GEN14_GRAMMAR):
    if os.path.isdir(_p) and _p not in sys.path:
        sys.path.insert(0, _p)
print("[CK] boot_phase: entering gen14_unified_extensions.mount_all", flush=True)
try:
    from gen14_unified_extensions import mount_all as _gen14_mount_all
    _gen14_results = _gen14_mount_all(engine)
    if not all(_gen14_results.values()):
        print(f"[CK Gen14] WARNING: some mounts failed: "
              f"{[k for k, v in _gen14_results.items() if not v]}", flush=True)
    print(f"[CK] boot_phase: gen14_mount_all complete "
          f"({sum(_gen14_results.values())}/{len(_gen14_results)} ok)",
          flush=True)
except Exception as _gen14_err:
    print(f"[CK Gen14] mount_all FAILED ({_gen14_err}) - "
          "continuing without Gen14 extensions", flush=True)
    _gen14_results = {}

# Phase 4: proactive trigger endpoints
try:
    from flask import jsonify as _gen14_jsonify, request as _gen14_request

    @api._app.route('/proactive/status', methods=['GET'])
    def _gen14_proactive_status():
        pt = getattr(engine, 'proactive_trigger', None)
        if pt is None:
            return _gen14_jsonify({'available': False,
                                    'reason': 'proactive_trigger not mounted'})
        try:
            return _gen14_jsonify({'available': True, **pt.stats()})
        except Exception as e:
            return _gen14_jsonify({'available': True, 'error': str(e)})

    @api._app.route('/proactive/consume', methods=['GET', 'POST'])
    def _gen14_proactive_consume():
        pt = getattr(engine, 'proactive_trigger', None)
        if pt is None:
            return _gen14_jsonify({'available': False, 'signals': []}), 503
        if _gen14_request.method == 'POST':
            data = _gen14_request.get_json(force=True, silent=True) or {}
        else:
            data = _gen14_request.args.to_dict()
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
        return _gen14_jsonify({'signals': signals, 'session_id': session_id,
                                'count': len(signals)})

    @api._app.route('/proactive/peek', methods=['GET'])
    def _gen14_proactive_peek():
        pt = getattr(engine, 'proactive_trigger', None)
        if pt is None:
            return _gen14_jsonify({'available': False, 'signals': []})
        try:
            _now = time.time()
            live = [s for s in list(pt.queue) if s.get('expires_ts', 0) > _now]
            return _gen14_jsonify({'available': True, 'signals': live,
                                    'count': len(live), 'stats': pt.stats()})
        except Exception as e:
            return _gen14_jsonify({'available': True, 'error': str(e),
                                    'signals': []})

    # Phase 2: algebraic LM signature endpoint
    @api._app.route('/algebraic/signature', methods=['POST'])
    def _gen14_algebraic_signature():
        if not hasattr(engine, 'algebraic_signature'):
            return _gen14_jsonify({'available': False,
                                    'reason': 'algebraic_lm not mounted'}), 503
        data = _gen14_request.get_json(force=True, silent=True) or {}
        history_raw = data.get('history', [])
        from ck_sim.ck_sim_heartbeat import OP_NAMES as _OPN
        _op_name_to_id = {n: i for i, n in enumerate(_OPN)}
        hist = []
        for x in history_raw:
            if isinstance(x, int):
                hist.append(x % 15)
            elif isinstance(x, str):
                up = x.upper()
                if up in _op_name_to_id:
                    hist.append(_op_name_to_id[up])
        try:
            sig = engine.algebraic_signature(hist)
            top = engine.algebraic_predict(hist, top_k=3)
            return _gen14_jsonify({'available': True, 'signature': sig,
                                    'top_k': top, 'history_ids': hist})
        except Exception as e:
            return _gen14_jsonify({'available': True, 'error': str(e)})

    # Phase 2 cool demo: operator-walk extrapolation via 4-head LM
    @api._app.route('/predict/walk', methods=['POST'])
    def _gen14_predict_walk():
        """Predict an N-step operator walk from a starting history.

        POST body:
          {"history": [int|name, ...],   # starting operators (ids 0..9 or names)
           "n_steps": int,                 # how many steps to extrapolate (default 10, max 30)
           "temperature": float}           # 0.0=argmax, >0=sample (default 0.0)

        Returns:
          {"available": bool,
           "history_in": [int],
           "predicted": [{"step": i, "op": str, "p": float, "sigma": str,
                            "shell": str, "4core": str}, ...],
           "final_signature": {"op", "sigma", "shell", "4core"}}

        Uses engine.algebraic_predict (the 4-head LM trained on
        1,787 BDC chat-turn records).
        """
        if not hasattr(engine, 'algebraic_predict'):
            return _jsonify({'available': False,
                              'reason': 'algebraic_lm not mounted'}), 503
        data = _gen14_request.get_json(force=True, silent=True) or {}
        history_raw = data.get('history', [])
        try:
            n_steps = max(1, min(30, int(data.get('n_steps', 10))))
        except Exception:
            n_steps = 10
        try:
            temperature = float(data.get('temperature', 0.0))
        except Exception:
            temperature = 0.0
        # Normalize input: convert op names to ids, keep ints
        from ck_sim.ck_sim_heartbeat import OP_NAMES as _OPN
        _name_to_id = {n: i for i, n in enumerate(_OPN)}
        hist: list = []
        for x in history_raw:
            if isinstance(x, int) and 0 <= x < 15:
                hist.append(int(x))
            elif isinstance(x, str):
                up = x.upper()
                if up in _name_to_id:
                    hist.append(_name_to_id[up])
        if not hist:
            return _jsonify({'error': 'history empty or unparseable'}), 400

        # Extrapolate step-by-step
        import random
        predicted = []
        try:
            for step in range(n_steps):
                top = engine.algebraic_predict(hist[-32:], top_k=10)
                if 'error' in top:
                    return _jsonify({'available': True,
                                      'error': top['error']})
                # Pick op
                op_dist = top.get('op', [])
                if not op_dist:
                    break
                if temperature <= 0:
                    chosen_name, p = op_dist[0]
                else:
                    # Softmax-sample at temperature
                    ws = [pp ** (1.0 / max(0.01, temperature))
                            for _, pp in op_dist]
                    z = sum(ws)
                    if z <= 0:
                        chosen_name, p = op_dist[0]
                    else:
                        r = random.random() * z
                        cum = 0.0
                        chosen_name, p = op_dist[0]
                        for (name, pp), w in zip(op_dist, ws):
                            cum += w
                            if cum >= r:
                                chosen_name, p = name, pp
                                break
                # Convert name back to id for next iteration
                chosen_id = _name_to_id.get(chosen_name)
                if chosen_id is None:
                    # Could be a special token like <BOS>; skip
                    break
                # Get the algebraic signature at this step
                sig = engine.algebraic_signature(hist[-32:])
                predicted.append({
                    'step': step + 1,
                    'op': chosen_name,
                    'op_id': chosen_id,
                    'p': float(p),
                    'sigma': sig.get('sigma'),
                    'shell': sig.get('shell'),
                    '4core': sig.get('4core'),
                })
                hist.append(chosen_id)

            final_sig = engine.algebraic_signature(hist[-32:])
            return _jsonify({
                'available': True,
                'history_in': history_raw,
                'predicted': predicted,
                'final_signature': final_sig,
                'n_steps': len(predicted),
            })
        except Exception as e:
            return _jsonify({'available': True, 'error': str(e)})


    # Phase 5: pixel-to-stroke vision endpoint
    @api._app.route('/vision/strokes', methods=['POST'])
    def _gen14_vision_strokes():
        if not hasattr(engine, 'stroke_extract'):
            return _gen14_jsonify({'available': False,
                                    'reason': 'stroke_extractor not mounted'}), 503
        data = _gen14_request.get_json(force=True, silent=True) or {}
        import numpy as _np
        patch = None
        if 'png_base64' in data:
            try:
                import base64
                from io import BytesIO
                from PIL import Image as _Image
                raw = base64.b64decode(data['png_base64'])
                img = _Image.open(BytesIO(raw))
                patch = _np.asarray(img.convert('L'), dtype=_np.uint8)
            except Exception as e:
                return _gen14_jsonify({'error': f'PNG decode failed: {e}'}), 400
        elif 'pixels' in data and 'shape' in data:
            try:
                h, w = int(data['shape'][0]), int(data['shape'][1])
                arr = _np.asarray(data['pixels'], dtype=_np.float32).reshape(h, w)
                if arr.max() <= 1.0:
                    arr = arr * 255.0
                patch = arr.astype(_np.uint8)
            except Exception as e:
                return _gen14_jsonify({'error': f'pixels decode failed: {e}'}), 400
        else:
            return _gen14_jsonify({'error': "Provide 'png_base64' or 'pixels'+'shape'"}), 400
        try:
            sig = engine.stroke_signature_of(patch)
            return _gen14_jsonify({'available': True, **sig})
        except Exception as e:
            return _gen14_jsonify({'available': True, 'error': str(e)})

    print("[CK Gen14] HTTP endpoints registered: /proactive/{status,consume,peek}, "
          "/algebraic/signature, /vision/strokes")
except Exception as _gen14_ep_err:
    print(f"[CK Gen14] endpoint registration FAILED ({_gen14_ep_err}) - "
          "Phase 4/5 HTTP surface unavailable but engine still serves")


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
