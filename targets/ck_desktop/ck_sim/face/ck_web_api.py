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

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
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

        # === FULL TIG PIPELINE ===
        # receive_text() runs the complete organism:
        #   D2 operator pipeline, dialogue, truth lattice,
        #   world lattice, compilation loop (9 passes max),
        #   voice composition with D2 self-verification
        try:
            response_text = self.engine.receive_text(text)
        except Exception:
            # Fallback: try dialogue engine directly
            try:
                response_text = self.engine.dialogue.process(
                    text, self._safe_coherence())
            except Exception:
                # Last resort: voice system
                try:
                    response_text = self.engine.voice.get_response(
                        'conversation',
                        self.engine.development.stage,
                        self.engine.emotion.current.primary)
                except Exception:
                    response_text = "..."

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

        # Build the full experience response
        result = {
            'text': response_text,
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

        print(f"  [WEB] CK Web API starting on {host}:{port}")
        self._app.run(host=host, port=port, debug=debug)


# Need these for the chat handler
from ck_sim.ck_sim_heartbeat import NUM_OPS, OP_NAMES
