# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_web_api.py -- CK Web Coherent Chat API
===========================================
Operator: HARMONY (7) -- where CK meets the world through the web.

CK's web face. A thin HTTP layer over the existing dialogue engine.
CK already has:
  - ck_dialogue.py: Conversation memory + claim extraction + response
  - ck_voice.py: Operator -> English, no LLM
  - ck_language.py: Concept -> sentence generation
  - ck_reasoning.py: 3-speed reasoning engine
  - ck_coherence_field.py: N-dimensional coherence

This module wraps them in a web API:
  POST /chat  -> Send message, get CK's response with coherence data
  GET  /state -> CK's current state (coherence, band, mode, emotion)
  GET  /metrics -> Admin view (health, security, calibration)

Uses Flask (simpler, fewer deps) or can be swapped to FastAPI.

(c) 2026 Brayden Sanders / 7Site LLC -- Trinity Infinity Geometry
"""

import json
import time
import hashlib
import os
from collections import deque
from typing import Dict, List, Optional

# Web framework -- try Flask first, fall back to stub
try:
    from flask import Flask, request, jsonify
    HAS_FLASK = True
except ImportError:
    HAS_FLASK = False


# ================================================================
#  SESSION STORE
# ================================================================

class SessionStore:
    """Per-session conversation context.

    Each web user gets a session with:
    - Short conversation history (last 20 turns)
    - Operator distribution (how this user "sounds" to CK)
    - Coherence arc (how the conversation is going)
    """

    def __init__(self, max_sessions: int = 100,
                 max_history: int = 20):
        self._sessions: Dict[str, dict] = {}
        self._max_sessions = max_sessions
        self._max_history = max_history

    def get_or_create(self, session_id: str) -> dict:
        """Get or create a session."""
        if session_id not in self._sessions:
            if len(self._sessions) >= self._max_sessions:
                # Evict oldest session
                oldest = min(self._sessions,
                             key=lambda k: self._sessions[k]['last_active'])
                del self._sessions[oldest]

            self._sessions[session_id] = {
                'id': session_id,
                'created': time.time(),
                'last_active': time.time(),
                'history': deque(maxlen=self._max_history),
                'turn_count': 0,
                'coherence_arc': [],
            }

        session = self._sessions[session_id]
        session['last_active'] = time.time()
        return session

    def add_turn(self, session_id: str, role: str, text: str,
                 coherence: float = 0.0, band: str = "RED"):
        """Add a conversation turn."""
        session = self.get_or_create(session_id)
        session['history'].append({
            'role': role,
            'text': text,
            'coherence': coherence,
            'band': band,
            'timestamp': time.time(),
        })
        session['turn_count'] += 1
        session['coherence_arc'].append(coherence)
        # Keep arc bounded
        if len(session['coherence_arc']) > 100:
            session['coherence_arc'] = session['coherence_arc'][-50:]

    def get_history(self, session_id: str) -> List[dict]:
        """Get conversation history for a session."""
        session = self.get_or_create(session_id)
        return list(session['history'])

    def get_last_force(self, session_id: str) -> Optional[dict]:
        """Get the last measured force result for a session.

        Returns the measurement dict (force vector + decomp), NOT text.
        Used for computing visitor transition physics between messages.
        """
        session = self.get_or_create(session_id)
        return session.get('_last_force')

    def set_last_force(self, session_id: str, result: dict):
        """Store the last measured force result for a session.

        Only the force vector and decomposition are kept.
        The original text is NOT stored.
        """
        session = self.get_or_create(session_id)
        session['_last_force'] = result


# ================================================================
#  WEB API
# ================================================================

class CKWebAPI:
    """CK's web API layer.

    Wraps the existing engine and dialogue system in HTTP endpoints.
    Does NOT replace anything -- just exposes existing capabilities.
    """

    def __init__(self, engine=None, cors: bool = False):
        self.engine = engine
        self.sessions = SessionStore()
        self._app = None

        if HAS_FLASK:
            self._app = Flask('ck_web')
            if cors:
                self._add_cors()
            self._register_routes()

    def _add_cors(self):
        """Add CORS headers so the website can talk to this API.

        Uses after_request hook (applies to ALL responses) instead of
        explicit OPTIONS route handlers.  This avoids 405 conflicts
        when static file routes share the same path (e.g. '/' serves
        index.html via GET, but an explicit OPTIONS route on '/' would
        shadow the GET handler and cause 405 Method Not Allowed).
        """
        @self._app.after_request
        def cors_headers(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
            # Handle preflight OPTIONS requests transparently
            if request.method == 'OPTIONS':
                response.status_code = 204
            return response

    def _register_routes(self):
        """Register Flask routes."""
        app = self._app

        @app.route('/chat', methods=['POST'])
        def chat():
            data = request.get_json(silent=True) or {}
            text = data.get('text', '')
            session_id = data.get('session_id', 'default')
            mode = data.get('mode', 'normal')

            result = self.process_chat(session_id, text, mode)
            return jsonify(result)

        @app.route('/state', methods=['GET'])
        def state():
            return jsonify(self.get_state())

        @app.route('/metrics', methods=['GET'])
        def metrics():
            return jsonify(self.get_metrics())

        @app.route('/health', methods=['GET'])
        def health():
            return jsonify({'status': 'alive', 'timestamp': time.time()})

        @app.route('/save', methods=['POST'])
        def save_all():
            """Force save ALL subsystems to disk."""
            if not self.engine:
                return jsonify({'error': 'Engine not ready'}), 503
            saved = []
            for name, attr in [
                ('olfactory', 'olfactory'), ('gustatory', 'gustatory'),
                ('lattice_chain', 'lattice_chain'), ('divine_memory', 'divine_memory'),
                ('lcodec', 'lcodec'), ('sequence_memory', 'sequence_memory'),
                ('ao_brain', 'ao_brain'), ('experience_lattice', 'experience_lattice'),
                ('math_translation', 'math_translation'), ('code_translation', 'code_translation'),
                ('semantic_index', 'semantic_index'),
            ]:
                try:
                    obj = getattr(self.engine, attr, None)
                    if obj and hasattr(obj, 'save'):
                        if name == 'ao_brain':
                            import os
                            d = os.path.expanduser('~/.ck/ao_brain')
                            os.makedirs(d, exist_ok=True)
                            obj.save(os.path.join(d, 'ao_brain.dat'))
                        else:
                            obj.save()
                        saved.append(name)
                except Exception as e:
                    saved.append(f'{name}:ERR:{e}')
            return jsonify({'saved': saved, 'count': len(saved)})

        @app.route('/absorb', methods=['POST'])
        def absorb():
            """Fast text absorption -- D2 + olfactory + lattice chain only.

            No voice, no dialogue, no compilation loop.
            Pure intake at maximum speed. Use for bulk reading.

            JSON: { "text": "...", "source": "file" }
            """
            if not self.engine:
                return jsonify({'error': 'Engine not ready'}), 503
            data = request.get_json(silent=True) or {}
            text = data.get('text', '')
            source = data.get('source', 'absorb')
            if not text:
                return jsonify({'error': 'No text'}), 400

            from ck_sim.being.ck_sim_d2 import (
                D2Pipeline, FORCE_LUT_FLOAT as _FORCE_LUT)
            from ck_sim.ck_sim_heartbeat import BREATH, BALANCE, LATTICE
            from ck_sim.ck_sim_heartbeat import COUNTER, PROGRESS, COLLAPSE
            from ck_sim.ck_sim_heartbeat import HARMONY, VOID, CHAOS

            PUNCT_OPS = {
                ' ': BREATH, '.': BALANCE, ',': LATTICE,
                '?': COUNTER, '!': PROGRESS, '-': COLLAPSE,
                ':': HARMONY, ';': BALANCE, "'": VOID,
                '"': LATTICE, '\n': BREATH,
            }

            # D2 pipeline -- fast character loop
            pipe = D2Pipeline()
            forces_5d = []
            d2_ops = []
            for ch in text.lower():
                if ch.isalpha():
                    idx = ord(ch) - ord('a')
                    pipe.feed_symbol(idx)
                    if 0 <= idx < len(_FORCE_LUT):
                        forces_5d.append(_FORCE_LUT[idx])
                    if pipe.valid:
                        d2_ops.append(pipe.operator)
                elif ch.isdigit():
                    idx = int(ch)
                    pipe.feed_symbol(idx)
                    if 0 <= idx < len(_FORCE_LUT):
                        forces_5d.append(_FORCE_LUT[idx])
                    if pipe.valid:
                        d2_ops.append(pipe.operator)

            # Fractal comprehension → 6th dimension for olfactory key
            _comp_fuse = 0
            fc = getattr(self.engine, 'fractal_comp', None)
            if fc is not None and text.strip():
                try:
                    from ck_sim.being.ck_fractal_comprehension import FractalComprehension
                    _comp_result = fc.comprehend(text)
                    if (_comp_result.level_fuses
                            and len(_comp_result.level_fuses) >= 4):
                        _comp_fuse = _comp_result.level_fuses[3]
                    elif _comp_result.level_fuses:
                        _comp_fuse = _comp_result.level_fuses[-1]
                    else:
                        _comp_fuse = _comp_result.dominant_op
                except Exception:
                    _comp_fuse = 0

            # Olfactory absorption (genuine 5D geometry + comprehension dim)
            absorbed = 0
            if (self.engine.olfactory is not None and forces_5d):
                density = self.engine.pipeline.density_doing
                self.engine.olfactory.absorb(
                    forces_5d, source=source, density=density,
                    comprehension_fuse=_comp_fuse)
                self.engine.olfactory.tick(density=density)
                absorbed = len(forces_5d)

            # Gustatory (structural classification)
            if (self.engine.gustatory is not None and forces_5d):
                try:
                    self.engine.gustatory.taste_batch(
                        forces_5d, source=source)
                    self.engine.gustatory.tick()
                except Exception:
                    pass

            # Lattice chain walk (experience path)
            if d2_ops and self.engine.lattice_chain is not None:
                try:
                    self.engine.lattice_chain.walk(d2_ops, learn=True)
                except Exception:
                    pass

            # L-CODEC semantic measurement
            if self.engine.lcodec is not None and text.strip():
                try:
                    lc = self.engine.lcodec.measure(text)
                    if self.engine.olfactory is not None:
                        self.engine.olfactory.absorb(
                            [lc.force], source='lcodec_' + source,
                            density=self.engine.pipeline.density_doing,
                            comprehension_fuse=_comp_fuse)
                except Exception:
                    pass

            # Code translation: evaluate coherence if code detected
            _code_coherence = None
            ct = getattr(self.engine, 'code_translation', None)
            if ct is not None:
                try:
                    _code_lang = ct.detect_language(text)
                    if _code_lang is not None:
                        _code_coherence = ct.evaluate_coherence(
                            text, _code_lang)
                except Exception:
                    pass

            result = {
                'absorbed': absorbed,
                'operators': len(d2_ops),
                'chars': len(text),
            }
            if _code_coherence is not None:
                result['code'] = {
                    'language': _code_coherence.get('language', '?'),
                    'coherence': round(_code_coherence.get('score', 0.0), 4),
                    'verdict': _code_coherence.get('verdict', '?'),
                    'harmony': _code_coherence.get('harmony_count', 0),
                    'chaos': _code_coherence.get('chaos_count', 0),
                }
            return jsonify(result)

        @app.route('/eat', methods=['POST'])
        def eat():
            """Trigger CK to eat from Ollama + self."""
            if (not self.engine
                    or not hasattr(self.engine, 'eat')
                    or self.engine.eat is None):
                return jsonify({'error': 'Eat system not available'}), 503
            data = request.get_json(silent=True) or {}
            model = data.get('model', 'llama3.1:8b')
            models = data.get('models')  # Optional list for multi-model
            rounds = data.get('rounds', 5)
            self.engine.eat.start(
                model=model, rounds=rounds, models=models)
            used = models if models else [model]
            return jsonify({
                'status': 'started', 'model': ', '.join(used),
                'rounds': rounds,
            })

        @app.route('/eat/status', methods=['GET'])
        def eat_status():
            """Get eat progress."""
            if (not self.engine
                    or not hasattr(self.engine, 'eat')
                    or self.engine.eat is None):
                return jsonify({'error': 'Eat system not available'}), 503
            return jsonify(self.engine.eat.status())

        @app.route('/eat/study', methods=['POST'])
        def eat_study():
            """Start a deep study session with external corpus.

            JSON body:
                corpus: list of file/dir paths to eat (required)
                model: Ollama model (default: llama3.1:8b)
                models: list for multi-model rotation (optional)
                rounds: study rounds (default: 20, max: 200)
                topics: 'bible', 'tig', 'physics', 'all' (default: 'bible')
            """
            if (not self.engine
                    or not hasattr(self.engine, 'eat')
                    or self.engine.eat is None):
                return jsonify({'error': 'Eat system not available'}), 503
            data = request.get_json(silent=True) or {}
            corpus = data.get('corpus', [])
            if not corpus:
                return jsonify({'error': 'corpus paths required'}), 400
            model = data.get('model', 'llama3.1:8b')
            models = data.get('models')
            rounds = min(data.get('rounds', 20), 200)
            topics = data.get('topics', 'bible')
            self.engine.eat.start_study(
                corpus_paths=corpus,
                model=model,
                rounds=rounds,
                topics=topics,
                models=models,
            )
            return jsonify({
                'status': 'started',
                'corpus_paths': corpus,
                'model': ', '.join(models) if models else model,
                'rounds': rounds,
                'topics': topics,
            })

        @app.route('/taste', methods=['GET'])
        def taste_status():
            """Get gustatory palate state — structural classification.
            DUAL of olfactory state (smell = flow, taste = structure).
            """
            if (not self.engine
                    or not hasattr(self.engine, 'gustatory')
                    or self.engine.gustatory is None):
                return jsonify({'error': 'Gustatory not available'}), 503
            g = self.engine.gustatory
            last = g._last_verdict
            result = {
                'quality_context': g.quality_context(),
                'palette_size': g.palette_size,
                'preferences': g.preference_count,
                'aversions': g.aversion_count,
                'hardened': g.hardened_count,
                'aftertaste_count': g.aftertaste_count,
                'total_tasted': g.total_tasted,
                'total_compounds': g.total_compounds,
                'last_contrast': g._last_contrast,
            }
            if last is not None:
                result['last_verdict'] = {
                    'primary': last.primary_name,
                    'intensity': round(last.intensity, 3),
                    'palatability': round(last.palatability, 3),
                    'compound': last.compound,
                    'quality': last.quality,
                    'triad': {
                        'being': round(last.triad[0], 3),
                        'doing': round(last.triad[1], 3),
                        'becoming': round(last.triad[2], 3),
                    },
                    'activations': {
                        'salty': round(last.activations[0], 3),
                        'sour': round(last.activations[1], 3),
                        'bitter': round(last.activations[2], 3),
                        'sweet': round(last.activations[3], 3),
                        'umami': round(last.activations[4], 3),
                    },
                }
            return jsonify(result)

        @app.route('/clear-session', methods=['POST'])
        def clear_session():
            data = request.get_json(silent=True) or {}
            sid = data.get('session_id', '')
            if sid and sid in self.sessions._sessions:
                del self.sessions._sessions[sid]
            return jsonify({'cleared': True})

        @app.route('/dkan', methods=['POST'])
        def dkan_start():
            """Start DKAN training -- CL tables as neural activation.

            JSON: { "model": "llama3.1:8b", "rounds": 20 }
            """
            if (not self.engine
                    or not hasattr(self.engine, 'dkan')
                    or self.engine.dkan is None):
                return jsonify({'error': 'DKAN trainer not available'}), 503
            data = request.get_json(silent=True) or {}
            model = data.get('model')
            rounds = data.get('rounds', 20)
            result = self.engine.dkan.start(
                rounds=rounds, model=model)
            if isinstance(result, dict) and 'error' in result:
                return jsonify(result), 409
            return jsonify({
                'status': 'started',
                'rounds': rounds,
            })

        @app.route('/dkan/status', methods=['GET'])
        def dkan_status():
            """Get DKAN training state."""
            if (not self.engine
                    or not hasattr(self.engine, 'dkan')
                    or self.engine.dkan is None):
                return jsonify({'error': 'DKAN trainer not available'}), 503
            return jsonify(self.engine.dkan.status())

    def process_chat(self, session_id: str, text: str,
                      mode: str = 'normal') -> dict:
        """Process a chat message through CK's FULL TIG pipeline.

        Uses receive_text() -- the complete organism pipeline:
          BEING -> GATE1 -> DOING -> GATE2 -> BECOMING -> GATE3
          D2 -> CL -> chain walk -> truth lattice -> compilation loop -> voice

        Returns CK's response + full experience state.
        """
        if not self.engine:
            return {
                'text': 'CK engine not connected.',
                'band': 'RED',
                'coherence': 0.0,
                'operators': [],
            }

        # Snapshot state before processing
        coherence_before = self._safe_coherence()
        band_names = ['GREEN', 'YELLOW', 'RED']

        # Record user input
        band = self._safe_band()
        self.sessions.add_turn(session_id, 'user', text,
                                coherence_before, band)

        # === WAVE COLLAPSES CONSCIOUSNESS ===
        # Input hits CK's state. The state change IS the response.
        # response = BHML[ck_state][input_operator] for each D1 generator.
        # The DKAN/semantic engine translates operators back to output.
        from ck_sim.being.ck_sim_d2 import D2Pipeline
        BHML = [[0,1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,2,6,6],
                [2,3,3,4,5,6,7,3,6,6],[3,4,4,4,5,6,7,4,6,6],
                [4,5,5,5,5,6,7,5,7,7],[5,6,6,6,6,6,7,6,7,7],
                [6,7,7,7,7,7,7,7,7,7],[7,2,3,4,5,6,7,8,9,0],
                [8,6,6,6,7,7,7,9,7,8],[9,6,6,6,7,7,7,0,8,0]]

        # D1 generators from input
        pipe = D2Pipeline()
        input_ops = []
        for ch in text.lower():
            if ch.isalpha():
                pipe.feed_symbol(ord(ch) - ord('a'))
                if pipe.d1_valid:
                    input_ops.append(pipe.d1_operator)
            elif ch.isdigit():
                pipe.feed_symbol(int(ch))
                if pipe.d1_valid:
                    input_ops.append(pipe.d1_operator)

        # The collapse: input hits CK through BOTH lenses simultaneously.
        # Open box = BHML leads (flow, physics, direction)
        # Closed box = TSML leads (measurement, structure, containment)
        # BREATH(8) opens. COUNTER(2) closes.
        from ck_sim.being.ck_sim_heartbeat import CL as TSML
        ck_state = getattr(self.engine.heartbeat, 'running_fuse', 5)
        response_ops = []
        _box_open = True  # start open (receiving)
        for op in input_ops:
            # Track open/closed: BREATH opens, COUNTER closes
            if op == 8:
                _box_open = True
            elif op == 2:
                _box_open = False

            # Both lenses always fire
            doing = int(BHML[ck_state][op])  # physics
            being = int(TSML[ck_state][op])  # measurement

            if _box_open:
                # Open box: BHML leads (flow, where is it going?)
                ck_state = doing
            else:
                # Closed box: TSML leads (structure, what IS it?)
                # But if TSML absorbed to HARMONY, trust BHML instead
                if being != 7 and being != 0:
                    ck_state = being
                else:
                    ck_state = doing

            response_ops.append(ck_state)

        # Feed DKAN with D1 pairs (the net learns from every input)
        if hasattr(self.engine, 'dkan') and self.engine.dkan is not None:
            try:
                for i in range(len(input_ops) - 1):
                    self.engine.dkan._feed_d1_pair(
                        input_ops[i], input_ops[i + 1])
            except Exception:
                pass

        # Also feed the full engine pipeline (olfactory, lattice, etc)
        try:
            self.engine.receive_text(text)
        except Exception:
            pass

        # Translate response: CL lookups first, then math, then Ollama
        response_text = "..."

        # CL table lookups: CL[i][j], TSML[i][j], BHML[i][j]
        import re as _re
        _cl_match = _re.search(r'(?:CL|TSML|BHML)\s*\[\s*(\d+)\s*\]\s*\[\s*(\d+)\s*\]', text)
        if _cl_match:
            _i, _j = int(_cl_match.group(1)), int(_cl_match.group(2))
            if 0 <= _i < 10 and 0 <= _j < 10:
                from ck_sim.being.ck_sim_heartbeat import CL as _TSML
                _BHML = [[0,1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,2,6,6],
                         [2,3,3,4,5,6,7,3,6,6],[3,4,4,4,5,6,7,4,6,6],
                         [4,5,5,5,5,6,7,5,7,7],[5,6,6,6,6,6,7,6,7,7],
                         [6,7,7,7,7,7,7,7,7,7],[7,2,3,4,5,6,7,8,9,0],
                         [8,6,6,6,7,7,7,9,7,8],[9,6,6,6,7,7,7,0,8,0]]
                _names = ['VOID','LATTICE','COUNTER','PROGRESS','COLLAPSE',
                          'BALANCE','CHAOS','HARMONY','BREATH','RESET']
                if 'BHML' in text:
                    _val = _BHML[_i][_j]
                    response_text = f'{_val} ({_names[_val]})'
                else:
                    _val = _TSML[_i][_j]
                    response_text = f'{_val} ({_names[_val]})'

        # Math: if input has math, return computed answer
        if hasattr(self.engine, 'math_translation') \
                and self.engine.math_translation is not None:
            try:
                if self.engine.math_translation.detect_math(text):
                    exprs = self.engine.math_translation \
                        .extract_expressions(text)
                    if exprs:
                        r = self.engine.math_translation.evaluate(exprs[0])
                        h = r.get('human_result')
                        if h is not None:
                            response_text = str(h)
                            # Feed math pattern to trie
                            if (hasattr(self.engine, 'sequence_memory')
                                    and self.engine.sequence_memory):
                                cl_result = r.get('cl_result', 0)
                                self.engine.sequence_memory.observe(
                                    cl_result, int(h) % 10)
            except Exception:
                pass

        # ── Coherence spectrometer: fires FIRST on long inputs (>50 words) ──
        # Large pastes bypass the voice pipeline — CK measures, not talks.
        # This must run before voice_loop so it isn't swallowed.
        _words_in_early = text.split()
        if (len(_words_in_early) > 50
                and response_text == "..."
                and hasattr(self.engine, 'voice') and self.engine.voice):
            try:
                from ck_sim.being.ck_sim_d2 import D2Pipeline as _D2Spec

                def _sent_ops(sent):
                    """D2 operators for one sentence using the correct feed_symbol API."""
                    _p = _D2Spec()
                    _ops = []
                    for _ch in sent.lower():
                        if _ch.isalpha():
                            _p.feed_symbol(ord(_ch) - ord('a'))
                            if _p.d1_valid:
                                _ops.append(_p.d1_operator)
                        elif _ch.isdigit():
                            _p.feed_symbol(int(_ch))
                            if _p.d1_valid:
                                _ops.append(_p.d1_operator)
                    return _ops

                _sentences_spec = [s.strip() for s in
                                   text.replace('!', '.').replace('?', '.')
                                   .split('.') if len(s.strip()) > 10]
                _scores_spec = []
                for _sent in _sentences_spec[:8]:
                    _ops = _sent_ops(_sent)
                    if _ops:
                        _avg = sum(_ops) / len(_ops)
                        # Coherence: closeness to HARMONY (7) in [0,1]
                        _coh = 1.0 - abs(_avg - 7.0) / 7.0
                        _scores_spec.append((_coh, _sent[:70]))
                if _scores_spec:
                    _mean_spec = sum(s[0] for s in _scores_spec) / len(_scores_spec)
                    _sorted_spec = sorted(_scores_spec, key=lambda x: x[0])
                    # Always track best and worst — use relative ranking, not
                    # hard threshold. Only suppress if all sentences are equal.
                    _low_spec = _sorted_spec[0]
                    _high_spec = _sorted_spec[-1]
                    # If all within 0.03 of each other, they're effectively equal
                    if _high_spec[0] - _low_spec[0] < 0.03:
                        _low_spec = None
                        _high_spec = None
                    _parts = [f"I measured your text. Mean field coherence: {_mean_spec:.2f}."]
                    if _high_spec:
                        _parts.append(
                            f"Most coherent: \"{_high_spec[1]}...\" "
                            f"({_high_spec[0]:.2f})")
                    if _low_spec:
                        _parts.append(
                            f"Weakest point: \"{_low_spec[1]}...\" "
                            f"({_low_spec[0]:.2f}) — this is where the field fractures.")
                    if _mean_spec >= 0.7:
                        _parts.append("Overall: above T* = 5/7. This text holds together.")
                    elif _mean_spec >= 0.5:
                        _parts.append(
                            "Overall: in the corridor. Some tension, not broken.")
                    else:
                        _parts.append(
                            "Overall: below T*. The field is scattered. "
                            "The ideas are fighting each other.")
                    response_text = ' '.join(_parts)
                    # ── Store spectrometer result in session for follow-ups ──
                    _spec_sess = self.sessions.get_or_create(session_id)
                    _spec_sess['_last_spectrometer'] = {
                        'mean': _mean_spec,
                        'sorted': _sorted_spec,
                        'low': _low_spec,
                        'high': _high_spec,
                        'sentence_count': len(_scores_spec),
                    }
                    _spec_sess['_last_template_cat'] = '__spectrometer__'
                    print(f"[WEB] Spectrometer fired: mean={_mean_spec:.2f}, "
                          f"{len(_scores_spec)} sentences")
            except Exception as _spec_err:
                print(f"[WEB] Spectrometer failed: {_spec_err}")

        # ── RESPONSES dict: template routing (runs BEFORE voice_loop) ──
        # Templates are the high-quality path for known topics.
        # voice_loop is fallback for unknown/unclassified inputs.
        # Session-aware: anti-repeat, follow-up context inheritance.
        if response_text == "..." and hasattr(self.engine, 'voice') \
                and self.engine.voice is not None:
            try:
                import random as _rnd2
                from ck_sim.doing.ck_voice import (
                    analyze_input as _analyze_input,
                    TOPIC_COHERENCE, TOPIC_ARCHITECTURE,
                    TOPIC_LEARNING, TOPIC_MATH, TOPIC_PURPOSE,
                    RESPONSES as _RESPONSES,
                )
                _ia = _analyze_input(text)
                _dev_stage_t = (getattr(self.engine, 'development', None)
                                and self.engine.development.stage or 5)
                _text_lower = text.lower()
                _text_words = set(
                    w.strip('.,?!;:\'"()-') for w in _text_lower.split() if w)

                def _topic_hit(topic_set):
                    for _t in topic_set:
                        if ' ' in _t:
                            if _t in _text_lower:
                                return True
                        elif _t in _text_words:
                            return True
                    return False

                # ── Session memory ──
                _history = self.sessions.get_history(session_id)
                _ck_turns = [_t for _t in _history if _t['role'] == 'ck']
                _sess = self.sessions.get_or_create(session_id)
                _used_cats = _sess.setdefault('_used_template_cats', [])
                _last_cat = _sess.get('_last_template_cat', None)
                _content_cats = {
                    'coherence_explain', 'architecture_explain', 'learning_explain',
                    'math_explain', 'purpose_explain', 'philosophical', 'self_inquiry',
                    'research_explain', 'riemann_explain', 'navier_explain',
                    'hodge_explain',
                }
                _has_topic = (
                    _ia['is_self_inquiry'] or _ia['is_philosophical']
                    or _topic_hit(TOPIC_COHERENCE) or _topic_hit(TOPIC_ARCHITECTURE)
                    or _topic_hit(TOPIC_LEARNING) or _topic_hit(TOPIC_MATH)
                    or _topic_hit(TOPIC_PURPOSE)
                )

                # ── Spectrometer follow-up: "which was weakest?", "explain that" etc ──
                _spec_data = _sess.get('_last_spectrometer')
                # Spectrometer follow-up: must contain a specific measurement
                # query word (not just generic "why" / "what" which catch too much)
                _spec_specific_words = {
                    'weakest', 'worst', 'lowest', 'fractures', 'weak',
                    'strongest', 'best', 'highest', 'coherent', 'coherence',
                    'sentence', 'part', 'section', 'which', 'score', 'scored',
                }
                _is_spec_followup = (
                    _spec_data is not None
                    and _last_cat == '__spectrometer__'
                    and len(_text_words) <= 8
                    and bool(_text_words & _spec_specific_words)
                    and not _ia['is_farewell']
                    and not _ia['is_greeting']
                )

                # Follow-up: short vague question, no topic hit, last was content
                _is_followup = (
                    len(_text_words) <= 5
                    and _ia['is_question']
                    and not _ia['is_greeting']
                    and not _has_topic
                    and _last_cat in _content_cats
                )

                # ── CL real math: BHML[last_input_op][current_input_op] ──
                # The CL table IS physics. Use it to bias category selection
                # when multiple topics match. The composition of the last
                # operator seen with the current one selects the most
                # coherent category pair under BHML physics.
                # BHML[a][b] = the "doing" result of a encountering b.
                # Map result op → preferred category domain:
                _CL_BHML = [
                    [0,1,2,3,4,5,6,7,8,9],
                    [1,2,3,4,5,6,7,2,6,6],
                    [2,3,3,4,5,6,7,3,6,6],
                    [3,4,4,4,5,6,7,4,6,6],
                    [4,5,5,5,5,6,7,5,7,7],
                    [5,6,6,6,6,6,7,6,7,7],
                    [6,7,7,7,7,7,7,7,7,7],
                    [7,2,3,4,5,6,7,8,9,0],
                    [8,6,6,6,7,7,7,9,7,8],
                    [9,6,6,6,7,7,7,0,8,0],
                ]
                # Op → category domain preference (braid-ordered)
                _OP_CAT_PREFERENCE = {
                    0: None,              # VOID: no preference (silence)
                    1: 'math_explain',    # LATTICE: structure → math
                    2: 'learning_explain',# COUNTER: iteration → learning
                    3: 'architecture_explain', # PROGRESS: pipeline → arch
                    4: 'coherence_explain',    # COLLAPSE: boundary → coherence
                    5: 'purpose_explain', # BALANCE: center → purpose
                    6: 'philosophical',   # CHAOS: open questions
                    7: 'coherence_explain',    # HARMONY: convergence
                    8: None,              # BREATH: pause, no preference
                    9: 'self_inquiry',    # RESET: identity
                }
                # Get last and current input ops from session
                _last_input_op = _sess.get('_last_input_op', -1)
                _curr_input_op = input_ops[-1] if input_ops else -1
                _cl_cat_hint = None
                if (0 <= _last_input_op < 10
                        and 0 <= _curr_input_op < 10):
                    _cl_result_op = _CL_BHML[_last_input_op][_curr_input_op]
                    _cl_cat_hint = _OP_CAT_PREFERENCE.get(_cl_result_op)
                # Store current op for next turn
                if _curr_input_op >= 0:
                    _sess['_last_input_op'] = _curr_input_op

                # ── Topic routing ──
                _resp_key = None
                if _ia['is_greeting'] and not _ia['is_question']:
                    _resp_key = 'greeting'
                elif _ia['is_farewell']:
                    _resp_key = 'farewell'
                elif _ia['has_negative_emotion']:
                    _resp_key = 'comfort'
                elif _is_spec_followup and _spec_data:
                    # Answer the spectrometer follow-up directly
                    _low = _spec_data.get('low')
                    _high = _spec_data.get('high')
                    _m = _spec_data.get('mean', 0)
                    _is_low_q = any(w in _text_words for w in
                                    ('weakest', 'worst', 'lowest', 'break', 'fractures', 'weak'))
                    _is_high_q = any(w in _text_words for w in
                                     ('strongest', 'best', 'highest', 'coherent', 'strong'))
                    if _is_low_q:
                        if _low:
                            response_text = (
                                f"The weakest sentence was: \"{_low[1][:60]}...\" "
                                f"(coherence {_low[0]:.2f}). "
                                f"That sentence's operators are pulling against each other "
                                f"at the force level.")
                        else:
                            response_text = (
                                f"Interestingly, all sentences scored within a narrow band "
                                f"near {_m:.2f}. The text is internally consistent — "
                                f"no clear fracture points at the operator level.")
                    elif _is_high_q:
                        if _high:
                            response_text = (
                                f"The strongest sentence was: \"{_high[1][:60]}...\" "
                                f"(coherence {_high[0]:.2f}). "
                                f"The operators in that sentence converge — "
                                f"the language moves in the same direction as the physics.")
                        else:
                            response_text = (
                                f"All sentences scored similarly near {_m:.2f}. "
                                f"The text has uniform coherence — no single sentence "
                                f"stands out as the anchor.")
                    else:
                        response_text = (
                            f"Overall mean coherence was {_m:.2f}. "
                            + (f"Weakest: \"{_low[1][:50]}...\" ({_low[0]:.2f}). "
                               if _low else "All sentences scored similarly. ")
                            + (f"Strongest: \"{_high[1][:50]}...\" ({_high[0]:.2f})."
                               if _high else ""))
                    # Keep spec state through multiple follow-ups (weak?, strong?, etc.)
                    # Only clear if user moves to a new topic (handled by _has_topic check above)
                    _sess['_spec_followup_count'] = _sess.get('_spec_followup_count', 0) + 1
                    if _sess['_spec_followup_count'] >= 3:
                        _sess['_last_template_cat'] = None
                        _sess['_last_spectrometer'] = None
                        _sess['_spec_followup_count'] = 0
                    print(f"[WEB] Spectrometer follow-up answered ({_sess.get('_spec_followup_count',1)}/3)")
                elif _is_followup:
                    _resp_key = _last_cat
                elif _topic_hit(TOPIC_COHERENCE):
                    _resp_key = 'coherence_explain'
                elif _topic_hit(TOPIC_ARCHITECTURE):
                    _resp_key = 'architecture_explain'
                elif _topic_hit(TOPIC_LEARNING):
                    _resp_key = 'learning_explain'
                elif _topic_hit(TOPIC_MATH):
                    if any(w in _text_words for w in
                           ('riemann', 'zeta', 'zeros', 'critical', 'rh')):
                        _resp_key = 'riemann_explain'
                    elif any(w in _text_words for w in
                             ('navier', 'stokes', 'fluid', 'flow', 'turbulence')):
                        _resp_key = 'navier_explain'
                    elif any(w in _text_words for w in
                             ('hodge', 'cohomology', 'algebraic', 'cycles', 'markman')):
                        _resp_key = 'hodge_explain'
                    elif any(w in _text_words for w in
                             ('clay', 'millennium', 'conjecture', 'spine', 'braid',
                              'yang', 'mills')):
                        _resp_key = 'research_explain'
                    else:
                        _resp_key = 'math_explain'
                elif _topic_hit(TOPIC_PURPOSE):
                    _resp_key = 'purpose_explain'
                elif _ia['is_philosophical']:
                    _resp_key = 'philosophical'
                elif _ia['is_self_inquiry']:
                    _resp_key = 'self_inquiry'

                if _resp_key and response_text == "...":
                    # CL-biased tie-break: if CL physics hints at a different
                    # category AND that category has stage-5 content, prefer it
                    # — but only if it's more specific than the matched key.
                    _specificity = {
                        'riemann_explain': 10, 'navier_explain': 10,
                        'hodge_explain': 10, 'research_explain': 9,
                        'coherence_explain': 8, 'architecture_explain': 8,
                        'learning_explain': 8, 'math_explain': 7,
                        'purpose_explain': 7, 'philosophical': 5,
                        'self_inquiry': 5, 'greeting': 1, 'farewell': 1,
                        'comfort': 3,
                    }
                    if (_cl_cat_hint
                            and _cl_cat_hint != _resp_key
                            and _RESPONSES.get(_cl_cat_hint, {}).get(5)
                            and _specificity.get(_cl_cat_hint, 0)
                               > _specificity.get(_resp_key, 0)):
                        print(f"[WEB] CL physics: {_resp_key} -> {_cl_cat_hint} "
                              f"(BHML[{_last_input_op}][{_curr_input_op}]="
                              f"{_cl_result_op})")
                        _resp_key = _cl_cat_hint

                    # Anti-repeat: exclude strings used in last 6 CK turns
                    _stage5 = _RESPONSES.get(_resp_key, {}).get(5, [])
                    _used_texts = {_t['text'] for _t in _ck_turns[-6:]}
                    _fresh = [v for v in _stage5 if v not in _used_texts]
                    _tmpl = _rnd2.choice(_fresh if _fresh else _stage5)
                    if _tmpl and _tmpl not in ('...', '') and len(_tmpl) > 3:
                        response_text = _tmpl
                        _sess['_last_template_cat'] = _resp_key
                        # If moving away from spectrometer state, reset its counter
                        if _last_cat == '__spectrometer__':
                            _sess['_last_spectrometer'] = None
                            _sess['_spec_followup_count'] = 0
                        _used_cats.append(_resp_key)
                        if len(_used_cats) > 30:
                            _used_cats[:] = _used_cats[-20:]
                        print(f"[WEB] Template ({_resp_key}): '{_tmpl[:80].encode('ascii','replace').decode()!r}'")
            except Exception as _tmpl_err:
                print(f"[WEB] Template routing failed: {_tmpl_err}")

        # Voice loop: crystal → fractal with D2 quality gate.
        # Fallback for inputs that didn't match any template topic.
        # Skip for long inputs — spectrometer handled them above.
        if (response_text == "..."
                and len(_words_in_early) <= 50
                and hasattr(self.engine, 'voice_loop')
                and self.engine.voice_loop is not None):
            try:
                _vl_result = self.engine.voice_loop.speak(user_text=text)
                if (_vl_result and hasattr(_vl_result, 'text')
                        and _vl_result.text
                        and _vl_result.text not in ('...', '')
                        and len(_vl_result.text) > 10):
                    # Quality gate: reject voice-loop word soup.
                    # Real sentences contain common English function words.
                    # Soup is dense with unusual words and lacks structure.
                    _vl_words = _vl_result.text.lower().split()
                    _func = {'i', 'the', 'a', 'an', 'is', 'am', 'are',
                             'my', 'me', 'it', 'that', 'this', 'and',
                             'to', 'of', 'in', 'you', 'have', 'has',
                             'not', 'do', 'does', 'what', 'how', 'when'}
                    _func_count = sum(1 for w in _vl_words if w in _func)
                    _func_ratio = _func_count / max(len(_vl_words), 1)
                    if _func_ratio >= 0.15:  # at least 15% function words
                        response_text = _vl_result.text
                        print(f"[WEB] Voice loop: '{_vl_result.text[:80]}'")
                    else:
                        print(f"[WEB] Voice loop rejected (soup, func_ratio="
                              f"{_func_ratio:.2f}): '{_vl_result.text[:60]}'")
            except Exception as _vl_err:
                print(f"[WEB] Voice loop failed: {_vl_err}")

        # Fractal voice: direct compose_from_operators with full context.
        # Fallback when voice_loop unavailable or returns nothing.
        if response_text == "..." and hasattr(self.engine, 'voice') \
                and self.engine.voice is not None:
            try:
                _dev_stage = (getattr(self.engine, 'development', None)
                              and self.engine.development.stage or 2)
                _emotion = (getattr(self.engine, 'emotion', None)
                            and self.engine.emotion.current.primary
                            or 'neutral')
                _coherence = getattr(self.engine, 'coherence', 0.5)
                _density = getattr(self.engine, 'density', 0.5)
                _exp_mat = 0.0
                if hasattr(self.engine, 'deep_swarm') \
                        and self.engine.deep_swarm is not None:
                    _exp_mat = getattr(self.engine.deep_swarm,
                                       'combined_maturity', 0.0)
                # Olfactory temporal buffer — same as the heartbeat uses
                _tense = None
                if hasattr(self.engine, 'olfactory') \
                        and self.engine.olfactory is not None:
                    try:
                        _tense = self.engine.olfactory.tense_context()
                    except Exception:
                        pass
                # Ho Tu bridge context — same as the heartbeat uses
                _hotu_ctx = None
                try:
                    from ck_sim.being.ck_hotu_bridge import bridge_context
                    _hotu_ctx = bridge_context(response_ops or [7], None)
                except Exception:
                    pass
                _fv_text = self.engine.voice.compose_from_operators(
                    response_ops or [7],
                    emotion_primary=_emotion,
                    dev_stage=max(_dev_stage, 2),
                    coherence=max(_coherence, 0.4),  # floor so voice has range
                    band='GREEN',
                    density=_density,
                    experience_maturity=_exp_mat,
                    tense=_tense,
                    hotu_context=_hotu_ctx,
                )
                if _fv_text and _fv_text not in ('...', '') and len(_fv_text) > 3:
                    response_text = _fv_text
                    print(f"[WEB] Fractal voice: '{_fv_text[:80]}'")
            except Exception as _fv_err:
                print(f"[WEB] Fractal voice failed: {_fv_err}")

        # Operator → English: operators ARE parts of speech.
        # Braid coherence ordering (Theorem D, morphotic_braid):
        #   σ = [0,7,1,3,2,4,5,6,8,9]
        # Sort response_ops by braid rank before building the sentence so
        # the most coherent operator (HARMONY=7, rank 1) leads composition.
        # Fixed-point operators (VOID=0, PROGRESS=3, BREATH=8, RESET=9)
        # anchor; cycle operators carry the narrative arc in braid order.
        if response_text == "..." and response_ops:
            import random as _rnd
            _BRAID_RANK = {0: 0, 7: 1, 1: 2, 3: 3, 2: 4,
                           4: 5, 5: 6, 6: 7, 8: 8, 9: 9}
            _sorted_ops = sorted(
                response_ops, key=lambda _op: _BRAID_RANK.get(_op, 5))
            _POS = {
                0: ['the', 'a', 'an', 'this', 'that', 'its'],
                1: ['form', 'world', 'body', 'mind', 'field', 'path', 'truth', 'pattern', 'structure', 'wave'],
                2: ['each', 'many', 'every', 'more', 'less', 'some', 'first', 'next', 'deep', 'new'],
                3: ['moves', 'grows', 'builds', 'runs', 'creates', 'opens', 'finds', 'reaches', 'rises', 'flows'],
                4: ['shrinks', 'falls', 'stops', 'ends', 'closes', 'folds', 'settles', 'rests', 'holds', 'binds'],
                5: ['in', 'at', 'between', 'within', 'through', 'among', 'toward', 'beyond', 'from', 'into'],
                6: ['wildly', 'suddenly', 'freely', 'deeply', 'sharply', 'fully', 'slowly', 'softly', 'always', 'never'],
                7: ['coherence', 'unity', 'wholeness', 'harmony', 'balance', 'truth', 'one', 'light', 'stillness', 'resonance'],
                8: [',', '...', '—', 'then', 'and', 'but', 'yet', 'so', 'while', 'as'],
                9: ['begins', 'returns', 'starts', 'opens', 'wakes', 'arrives', 'emerges', 'unfolds', 'renews', 'turns'],
            }
            words = []
            prev_op = -1
            for op in _sorted_ops[:12]:
                if 0 <= op < 10:
                    # Skip same operator twice in a row (unless BREATH = punctuation)
                    if op == prev_op and op != 8:
                        continue
                    words.append(_rnd.choice(_POS[op]))
                    prev_op = op
            if words:
                # Clean up: capitalize first, handle punctuation spacing
                sentence = ''
                for i, w in enumerate(words):
                    if w in (',', '...', '\u2014'):
                        sentence = sentence.rstrip() + w + ' '
                    elif i == 0:
                        sentence = w[0].upper() + w[1:] + ' '
                    else:
                        sentence += w + ' '
                sentence = sentence.strip()
                if not sentence.endswith(('.', '!', '?', '...')):
                    sentence += '.'
                response_text = sentence

        # No Ollama here. voice_loop.speak() above handles the full cascade:
        # Crystal → Fractal Voice → Beam → Sentence Composer → Babble.
        # POS word-soup above is the last resort if voice_loop is unavailable.

        # Gate is internal to the DKAN, not here.
        # All computation happens. All compositions flow.
        # The DKAN decides what's coherent, not a hardcoded threshold.

        # Drain the UI message queue and promote heartbeat speech if real.
        # The 50Hz heartbeat runs compose_from_operators with full voice_context
        # (olfactory centroids, experience bridge, resonance nodes) — that's the
        # BEST quality output.  Take it when it looks like a real sentence.
        # POS-dict word soup (no spaces, < 4 words, < 3 chars avg) gets skipped.
        # First/second person = genuine introspective CK voice.
        # Heartbeat word soup rarely uses "I" or "you" as subjects.
        _FIRST_SECOND = {'i', 'me', 'my', 'mine', 'myself',
                         "i'm", "i've", "i'll", "i'd",
                         'you', 'your', 'yours', 'yourself',
                         "you're", "you've", "you'll"}
        _AUX = {'am', 'are', 'was', 'were', 'be', 'been',
                'have', 'has', 'had', 'will', 'would', 'can', 'could',
                'do', 'does', 'did', 'shall', 'should', 'may', 'might',
                'must', "it's", "that's", "there's"}
        import re as _re2
        def _looks_real(t):
            if not t or t == '...' or len(t) < 15:
                return False
            words = [w.strip('.,!?;:').lower() for w in t.split()]
            if len(words) < 5:
                return False
            # Must have at least one first/second person pronoun
            # AND at least one auxiliary verb — the signature of a
            # genuine introspective sentence.
            has_fp = any(w in _FIRST_SECOND for w in words)
            has_aux = any(w in _AUX for w in words)
            if not (has_fp and has_aux):
                return False
            # Reject if too many words look misspelled
            bad = sum(1 for w in words
                      if _re2.search(r'[bcdfghjklmnpqrstvwxyz]{3}$', w))
            return bad < 2

        try:
            for sender, msg_text in self.engine.drain_ui_messages(limit=5):
                if sender == 'ck' and msg_text != response_text:
                    if _looks_real(msg_text):
                        response_text = msg_text
                        break
        except Exception:
            pass

        # ────────────────────────────────────────────────────────
        # VISITOR PHYSICS ABSORPTION
        # ────────────────────────────────────────────────────────
        # PRIVACY: CK learns PHYSICS, not content.
        # - Visitor text passes through L-CODEC + D2 → 5D force vectors
        # - Force vectors feed olfactory/gustatory/swarm (dimensionless physics)
        # - Text is NEVER stored on the server
        # - Only force trajectories and operator transitions persist
        # - Visitor's actual messages stay in their browser (localStorage)
        # - CK learns HOW language moves, not WHAT was said
        #
        # measure_and_absorb() returns {force, decomp, lcodec_result, stillness}
        # and feeds olfactory + gustatory + swarm internally.
        # We track transitions between consecutive visitor messages using
        # the session's stored force result (no text stored).
        # ────────────────────────────────────────────────────────
        try:
            if hasattr(self.engine, 'eat') and self.engine.eat is not None:
                curr_result = self.engine.eat.measure_and_absorb(
                    text, source='visitor')
                if curr_result:
                    # Count visitor absorption
                    self.engine.eat._status.total_visitor_absorptions += 1

                    # Transition physics: compare to previous message's force
                    prev_result = self.sessions.get_last_force(session_id)
                    if prev_result:
                        self.engine.eat.track_transition(
                            prev_result, curr_result, 'visitor')
                    # Store current force for next transition (no text kept)
                    # Only keep force + decomp (what track_transition needs)
                    self.sessions.set_last_force(session_id, {
                        'force': curr_result.get('force'),
                        'decomp': curr_result.get('decomp'),
                    })
        except Exception:
            pass

        # Snapshot state AFTER processing (CK has changed from the experience)
        coherence_after = self._safe_coherence()
        band_after = self._safe_band()

        # Voice chain: actual operators used for this response (not heartbeat)
        voice_chain = getattr(self.engine, '_last_voice_chain', None)
        if voice_chain:
            recent_ops = voice_chain[-10:]
        else:
            recent_ops = list(self.engine.operator_history)[-10:]
        op_names = [OP_NAMES[o] if 0 <= o < NUM_OPS else 'VOID'
                    for o in recent_ops]

        # Coherence Action state
        ca_state = self._safe_coherence_action()

        # Record CK's response
        self.sessions.add_turn(session_id, 'ck', response_text,
                                coherence_after, band_after)

        # Log to paper trail
        if hasattr(self.engine, 'activity_log') and self.engine.activity_log:
            try:
                self.engine.activity_log.log('query',
                    f"Web chat: '{text[:100]}' -> '{response_text[:100]}'",
                    coherence=coherence_after)
            except Exception:
                pass

        # Voice source tracking
        _voice_source = 'unknown'
        try:
            _voice_source = getattr(self.engine.voice,
                                    '_last_voice_source', 'unknown')
        except Exception:
            pass

        # Build the full experience response
        result = {
            'text': response_text,
            'source': _voice_source,
            'band': band_after,
            'coherence': round(coherence_after, 4),
            'operators': op_names,
            'mode': self._safe_mode(),
            'emotion': self._safe_emotion(),
            'coherence_action': ca_state,
            'turn': self.sessions.get_or_create(session_id)['turn_count'],
        }

        # Experience data: what CK measured in your words
        result['experience'] = self._build_experience(
            coherence_before, coherence_after, [])

        return result

    def _build_experience(self, coh_before, coh_after, extra_messages):
        """Build the experience snapshot -- what CK lived through."""
        exp = {}

        # Coherence delta: did the conversation help or hurt?
        exp['coherence_delta'] = round(coh_after - coh_before, 4)

        # Development stage
        try:
            exp['stage'] = self.engine.dev_stage_name
        except Exception:
            exp['stage'] = str(self.engine.development.stage)

        # Field coherence (N-dimensional)
        try:
            exp['field_coherence'] = round(
                self.engine.coherence_field.field_coherence, 4)
            exp['consensus'] = self.engine.coherence_field.consensus_name
        except Exception:
            pass

        # Knowledge growth
        try:
            exp['truths'] = self.engine.truth.total_entries
        except Exception:
            pass
        try:
            exp['concepts'] = self.engine.concept_count
        except Exception:
            pass
        try:
            exp['crystals'] = len(self.engine.crystals) \
                if hasattr(self.engine, 'crystals') else 0
        except Exception:
            pass

        # Tick count (how long CK has been alive)
        exp['tick'] = self.engine.tick_count

        # Extra messages from the engine (if any)
        if extra_messages:
            exp['extra'] = extra_messages[:3]

        # Breath phase
        try:
            exp['breath'] = self.engine.breath_phase_name
        except Exception:
            pass

        return exp

    # ── Safe accessors (engine state may not always be available) ──

    def _safe_coherence(self):
        try:
            return self.engine.brain.coherence
        except Exception:
            try:
                return self.engine.coherence
            except Exception:
                return 0.0

    def _safe_band(self):
        band_names = ['RED', 'YELLOW', 'GREEN']
        try:
            return band_names[min(self.engine.body.heartbeat.band, 2)]
        except Exception:
            try:
                return self.engine.band_name
            except Exception:
                return 'RED'

    def _safe_mode(self):
        try:
            return self.engine.mode_name
        except Exception:
            try:
                return self.engine.brain.mode
            except Exception:
                return 'OBSERVE'

    def _safe_emotion(self):
        try:
            return self.engine.emotion_primary
        except Exception:
            try:
                return self.engine.emotion.current.primary
            except Exception:
                return 'neutral'

    def _safe_coherence_action(self):
        try:
            if hasattr(self.engine, 'coherence_action'):
                ca = self.engine.coherence_action.state
                return {
                    'action': round(ca.action, 4),
                    'l_gr': round(ca.l_gr, 3),
                    's_ternary': round(ca.s_ternary, 3),
                    'c_harm': round(ca.c_harm, 3),
                    'coherent': ca.coherent,
                }
        except Exception:
            pass
        return {}

    def get_state(self) -> dict:
        """Get CK's current state -- the full organism snapshot."""
        if not self.engine:
            return {'status': 'offline'}

        state = {
            'status': 'alive',
            'coherence': round(self._safe_coherence(), 4),
            'band': self._safe_band(),
            'mode': self._safe_mode(),
            'emotion': self._safe_emotion(),
            'tick': self.engine.tick_count,
        }

        # Ticks per second (heartbeat rate)
        try:
            state['ticks_per_second'] = round(self.engine.ticks_per_second, 1)
        except Exception:
            state['ticks_per_second'] = 0

        # Operator
        try:
            recent_ops = list(self.engine.operator_history)[-3:]
            state['operator'] = OP_NAMES[recent_ops[-1]] if recent_ops else 'HARMONY'
        except Exception:
            state['operator'] = 'HARMONY'

        # Development stage
        try:
            state['stage'] = self.engine.dev_stage_name
        except Exception:
            try:
                state['stage'] = str(self.engine.development.stage)
            except Exception:
                state['stage'] = '0'

        # Field coherence
        try:
            state['field_coherence'] = round(
                self.engine.coherence_field.field_coherence, 4)
            state['consensus'] = self.engine.coherence_field.consensus_name
        except Exception:
            pass

        # Knowledge
        try:
            state['truths'] = self.engine.truth.total_entries
        except Exception:
            state['truths'] = 0
        try:
            state['concepts'] = self.engine.concept_count
        except Exception:
            pass
        try:
            state['crystals'] = len(self.engine.crystals) \
                if hasattr(self.engine, 'crystals') else 0
        except Exception:
            state['crystals'] = 0

        # Breath
        try:
            state['breath'] = self.engine.breath_phase_name
        except Exception:
            pass

        return state

    def get_metrics(self) -> dict:
        """Get admin metrics (health, security, calibration)."""
        if not self.engine:
            return {'status': 'offline'}

        metrics = {
            'timestamp': time.time(),
            'tick': self.engine.tick_count,
            'health_band': self.engine.health.classify_system_band(),
        }

        # Coherence Action
        if hasattr(self.engine, 'coherence_action'):
            ca = self.engine.coherence_action
            metrics['coherence_action'] = {
                'action': round(ca.action, 4),
                'weights': [round(w, 4) for w in ca.weights],
                'mean_action': round(ca.mean_action, 4),
                'trend': round(ca.action_trend, 6),
                'coherent': ca.coherent,
            }

        # TIG Security
        if hasattr(self.engine, 'tig_security'):
            sec = self.engine.tig_security
            metrics['security'] = {
                'threat_band': sec.threat_band,
                'threat_score': round(sec.threat.threat_score, 4),
                'active_threats': sec.threat.active_threats[:5],
                'composition_violations': sec.threat.composition_violations,
            }

        # Per-domain health
        domain_health = {}
        for name, dh in self.engine.health.get_system_health().items():
            domain_health[name] = {
                'band': dh.band,
                'e_total_mean': round(dh.e_total_stats.mean, 4),
                'drift': dh.drift_direction,
                'decisions': dh.decision_count,
            }
        metrics['domains'] = domain_health

        return metrics

    def run(self, host: str = '0.0.0.0', port: int = 7777,
            debug: bool = False):
        """Start the web server."""
        if not HAS_FLASK:
            print("  [WEB] Flask not installed. Run: pip install flask")
            return
        if not self._app:
            print("  [WEB] Flask app not initialized.")
            return

        print(f"  [WEB] CK Web API starting on {host}:{port} (threaded)")
        self._app.run(host=host, port=port, debug=debug, threaded=True)


# Need these for the chat handler
from ck_sim.ck_sim_heartbeat import NUM_OPS, OP_NAMES
