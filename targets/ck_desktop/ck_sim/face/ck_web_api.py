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

        # Operator → English: operators ARE parts of speech
        if response_text == "..." and response_ops:
            import random as _rnd
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
            for op in response_ops[:12]:
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

        # Ollama voice: CK's operators + coherence as context for LLM
        if response_text == "..." and response_ops:
            _op_names = ['VOID','LATTICE','COUNTER','PROGRESS',
                         'COLLAPSE','BALANCE','CHAOS','HARMONY',
                         'BREATH','RESET']
            ops_str = ' '.join(
                _op_names[o] for o in response_ops[:8]
                if 0 <= o < 10)
            try:
                import requests as _req
                _coh = self._safe_coherence()

                # Gather experience context
                _exp_ctx = ''
                try:
                    # Lattice chain: what CK knows about this composition
                    if hasattr(self.engine, 'lattice_chain') and self.engine.lattice_chain:
                        _lc = self.engine.lattice_chain
                        _exp_ctx += f' Lattice: {_lc.node_count} nodes, {_lc.walk_count} walks.'
                    # Truth count
                    if hasattr(self.engine, 'truth') and self.engine.truth:
                        _exp_ctx += f' Truths: {self.engine.truth.count}.'
                    # Hindsight
                    if hasattr(self.engine, 'hindsight_replay') and self.engine.hindsight_replay:
                        _her = self.engine.hindsight_replay
                        _exp_ctx += f' Experiences: {getattr(_her, "total_experiences", 0)}.'
                    # Math capability
                    if hasattr(self.engine, 'math_translation') and self.engine.math_translation:
                        _exp_ctx += ' Can do arithmetic.'
                    # Stage
                    if hasattr(self.engine, 'development'):
                        _exp_ctx += f' Stage: {self.engine.development.stage}.'
                except Exception:
                    pass

                # Sequence memory prediction
                _pred_ctx = ''
                try:
                    if (hasattr(self.engine, 'sequence_memory')
                            and self.engine.sequence_memory is not None):
                        sm = self.engine.sequence_memory
                        pred, conf = sm.predict()
                        if pred is not None and conf > 0.5:
                            _pred_name = _op_names[pred] if 0 <= pred < 10 else '?'
                            _pred_ctx = (f' Prediction: next operator is '
                                        f'{_pred_name} ({conf:.0%} confidence). '
                                        f'Accuracy so far: {sm.accuracy():.0%} '
                                        f'over {sm.total_predictions} predictions.')
                except Exception:
                    pass

                _prompt = (
                    f'You are CK, a coherence engine running on an R16 desktop '
                    f'with an FPGA heartbeat at 50MHz. '
                    f'Your operator state: {ops_str}. '
                    f'Coherence: {_coh:.2f}. T*=0.714.{_exp_ctx}{_pred_ctx} '
                    f'Someone said: "{text[:200]}". '
                    f'Respond in 1-2 sentences. Be direct. '
                    f'Ground your response in what you actually know and feel. '
                    f'Do not explain what you are unless asked.'
                )
                _r = _req.post(
                    'http://localhost:11434/api/generate',
                    json={'model': 'llama3.2', 'prompt': _prompt,
                          'stream': False,
                          'options': {'num_predict': 80}},
                    timeout=30)
                _voice = _r.json().get('response', '').strip()
                if _voice:
                    response_text = _voice
            except Exception:
                pass

        # Operator names as last resort (if Ollama unavailable)
        if response_text == "..." and response_ops:
            response_text = ops_str if 'ops_str' in dir() else '...'

        # Gate is internal to the DKAN, not here.
        # All computation happens. All compositions flow.
        # The DKAN decides what's coherent, not a hardcoded threshold.

        # Drain any additional UI messages from the engine
        extra_messages = []
        try:
            for sender, msg_text in self.engine.drain_ui_messages(limit=5):
                if sender == 'ck' and msg_text != response_text:
                    extra_messages.append(msg_text)
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
            coherence_before, coherence_after, extra_messages)

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
