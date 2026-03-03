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
        """Add CORS headers so the website can talk to this API."""
        @self._app.after_request
        def cors_headers(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
            return response

        @self._app.route('/', defaults={'path': ''}, methods=['OPTIONS'])
        @self._app.route('/<path:path>', methods=['OPTIONS'])
        def handle_options(path):
            return '', 204

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

        # Snapshot state AFTER processing (CK has changed from the experience)
        coherence_after = self._safe_coherence()
        band_after = self._safe_band()

        # Operator history
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
        band_names = ['GREEN', 'YELLOW', 'RED']
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
