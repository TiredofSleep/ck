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
import requests as _requests
from collections import deque
from typing import Dict, List, Optional

# Web framework -- try Flask first, fall back to stub
try:
    from flask import Flask, request, jsonify
    HAS_FLASK = True
except ImportError:
    HAS_FLASK = False

# Backbone system prompt for LLM gating
try:
    from ck_backbone import build_system_prompt
except ImportError:
    def build_system_prompt(context=None, mode='default'):
        return "You are a helpful assistant."

# C algebra token gate (native speed D2 on every token)
try:
    from ck_token_gate import TokenGate
    _HAS_TOKEN_GATE = True
except ImportError:
    _HAS_TOKEN_GATE = False


# ================================================================
#  SESSION STORE
# ================================================================

class SessionStore:
    """Per-session conversation context with disk persistence.

    Each web user gets a session with:
    - Short conversation history (last 20 turns)
    - Operator distribution (how this user "sounds" to CK)
    - Coherence arc (how the conversation is going)

    Sessions persist to ~/.ck/sessions/ as JSON files.
    Every conversation builds CK's chain -- nothing is lost.
    """

    def __init__(self, max_sessions: int = 100,
                 max_history: int = 20,
                 persist_dir: Optional[str] = None):
        self._sessions: Dict[str, dict] = {}
        self._max_sessions = max_sessions
        self._max_history = max_history

        # Persistence directory
        if persist_dir is None:
            persist_dir = os.path.join(os.path.expanduser('~'), '.ck', 'sessions')
        self._persist_dir = persist_dir
        os.makedirs(self._persist_dir, exist_ok=True)

        # Load existing sessions from disk
        self._load_all()

    def _session_path(self, session_id: str) -> str:
        """Get the file path for a session."""
        # Sanitize session_id for filesystem safety
        safe_id = ''.join(c for c in session_id if c.isalnum() or c in '-_')[:64]
        return os.path.join(self._persist_dir, f'{safe_id}.json')

    def _load_all(self):
        """Load all persisted sessions from disk."""
        try:
            for fname in os.listdir(self._persist_dir):
                if not fname.endswith('.json'):
                    continue
                fpath = os.path.join(self._persist_dir, fname)
                try:
                    with open(fpath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    sid = data.get('id', fname[:-5])
                    self._sessions[sid] = {
                        'id': sid,
                        'created': data.get('created', time.time()),
                        'last_active': data.get('last_active', time.time()),
                        'history': deque(
                            data.get('history', []),
                            maxlen=self._max_history),
                        'turn_count': data.get('turn_count', 0),
                        'coherence_arc': data.get('coherence_arc', []),
                    }
                except (json.JSONDecodeError, KeyError, OSError):
                    continue
        except OSError:
            pass

    def _save_session(self, session_id: str):
        """Persist a single session to disk."""
        session = self._sessions.get(session_id)
        if session is None:
            return
        try:
            data = {
                'id': session['id'],
                'created': session['created'],
                'last_active': session['last_active'],
                'history': list(session['history']),
                'turn_count': session['turn_count'],
                'coherence_arc': session['coherence_arc'][-50:],
            }
            fpath = self._session_path(session_id)
            with open(fpath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False)
        except OSError:
            pass

    def get_or_create(self, session_id: str) -> dict:
        """Get or create a session."""
        if session_id not in self._sessions:
            if len(self._sessions) >= self._max_sessions:
                # Evict oldest session (it's already persisted on disk)
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
        """Add a conversation turn and persist to disk."""
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
        # Persist every turn -- every conversation builds the chain
        self._save_session(session_id)

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

    def __init__(self, engine=None, cors: bool = False,
                 ollama_model: str = 'llama3.2',
                 ollama_url: str = 'http://localhost:11434',
                 backbone_mode: str = 'default'):
        self.engine = engine
        self.sessions = SessionStore()
        self._app = None
        self._ollama_model = ollama_model
        self._ollama_url = ollama_url
        self._backbone_mode = backbone_mode  # 'default' or 'bible'
        self._ollama_available = None  # cached availability check

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

    def _get_steering_engine(self):
        """Lazy-load the steering engine on first request.

        Wires in the shadow swarm from sensorium (if running) so steering
        can read live process classifications. Same pattern as
        ck_sim_engine._deep_swarm_tick() uses to grab the swarm.
        """
        if not hasattr(self, '_steering_engine'):
            from ck_sim.ck_steering import SteeringEngine
            # Try to get the live swarm from sensorium background thread
            swarm = None
            try:
                from ck_sim.being.ck_sensorium import _swarm
                swarm = _swarm
            except ImportError:
                pass
            # If engine has a steering instance already, reuse it
            if self.engine and hasattr(self.engine, 'steering'):
                self._steering_engine = self.engine.steering
                # Wire in swarm if engine's steering doesn't have one
                if self._steering_engine.swarm is None and swarm is not None:
                    self._steering_engine.swarm = swarm
            else:
                self._steering_engine = SteeringEngine(swarm=swarm)
        return self._steering_engine

    def _get_token_gate(self):
        """Lazy-load the C algebra token gate.

        CK's mind runs in C. The token gate streams Ollama output and
        measures every token through D2 curvature at native speed.
        Three substrates compose: C algebra scores, GPU experience
        weighs in, Ollama provides the mouth.
        """
        if not hasattr(self, '_token_gate'):
            if not _HAS_TOKEN_GATE:
                self._token_gate = None
                return None
            # Connect mind (C algebra) to soul (GPU experience)
            gpu_exp = None
            if (hasattr(self._engine, 'gpu')
                    and self._engine.gpu is not None):
                gpu_exp = self._engine.gpu.experience
            self._token_gate = TokenGate(
                ollama_url=self._ollama_url,
                model=self._ollama_model,
                max_retries=2,
                coherence_floor=0.35,
                gpu_experience=gpu_exp,
            )
        return self._token_gate

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
            rounds = min(data.get('rounds', 20), 2000)
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

        # ── DKAN Training Endpoints ──

        @app.route('/train', methods=['POST'])
        def train():
            """Start DKAN algebraic neural training via Ollama.

            JSON body:
                model: Ollama model (default: auto-detect)
                rounds: training rounds (default: 20, max: 200)
            """
            if not self.engine:
                return jsonify({'error': 'Engine not available'}), 503
            if not hasattr(self.engine, 'dkan_trainer'):
                # Lazy init
                try:
                    from ck_sim.being.ck_dkan_trainer import DKANTrainer
                    self.engine.dkan_trainer = DKANTrainer(self.engine)
                except Exception as e:
                    return jsonify({'error': f'DKAN init failed: {e}'}), 500

            data = request.get_json(silent=True) or {}
            model = data.get('model')
            rounds = min(data.get('rounds', 20), 200)
            result = self.engine.dkan_trainer.start(
                rounds=rounds, model=model)
            if 'error' in result:
                return jsonify(result), 503
            return jsonify(result)

        @app.route('/train/status', methods=['GET'])
        def train_status():
            """Get DKAN training progress."""
            if (not self.engine
                    or not hasattr(self.engine, 'dkan_trainer')
                    or self.engine.dkan_trainer is None):
                return jsonify({'running': False, 'status': 'not initialized'})
            return jsonify(self.engine.dkan_trainer.status())

        @app.route('/train/history', methods=['GET'])
        def train_history():
            """Get coherence history for plotting."""
            if (not self.engine
                    or not hasattr(self.engine, 'dkan_trainer')
                    or self.engine.dkan_trainer is None):
                return jsonify({'error': 'DKAN not initialized'}), 503
            last_n = request.args.get('n', 50, type=int)
            return jsonify(
                self.engine.dkan_trainer.coherence_history(last_n))

        @app.route('/train/stop', methods=['POST'])
        def train_stop():
            """Stop DKAN training."""
            if (not self.engine
                    or not hasattr(self.engine, 'dkan_trainer')
                    or self.engine.dkan_trainer is None):
                return jsonify({'error': 'DKAN not initialized'}), 503
            self.engine.dkan_trainer.stop()
            return jsonify({'stopped': True})

        # ---- Bible Sense (operator resonance verse lookup) ----

        @app.route('/bible/resonate', methods=['POST'])
        def bible_resonate():
            """Find verses by operator resonance with query text."""
            if not hasattr(self, '_bible_sense'):
                try:
                    from ck_sim.being.ck_bible_sense import BibleSense
                    self._bible_sense = BibleSense()
                    self._bible_sense.load()
                except Exception as e:
                    return jsonify({'error': str(e)}), 503

            data = request.get_json(silent=True) or {}
            query = data.get('query', data.get('text', ''))
            top_k = min(data.get('top_k', 5), 20)

            if not query:
                return jsonify({'error': 'query required'}), 400

            results = self._bible_sense.resonate(query, top_k=top_k)
            return jsonify({
                'query': query,
                'results': [{
                    'ref': r.verse.ref,
                    'text': r.verse.text,
                    'distance': round(r.distance, 4),
                    'force_similarity': round(r.force_similarity, 4),
                    'op_overlap': round(r.op_overlap, 4),
                    'dominant_op': r.verse.dominant_op,
                    'coherence': round(r.verse.coherence, 4),
                } for r in results],
            })

        @app.route('/bible/verse/<path:ref>', methods=['GET'])
        def bible_verse(ref):
            """Get a specific verse with its force profile."""
            if not hasattr(self, '_bible_sense'):
                try:
                    from ck_sim.being.ck_bible_sense import BibleSense
                    self._bible_sense = BibleSense()
                    self._bible_sense.load()
                except Exception as e:
                    return jsonify({'error': str(e)}), 503

            v = self._bible_sense.get_verse(ref)
            if not v:
                return jsonify({'error': f'verse not found: {ref}'}), 404
            return jsonify({
                'ref': v.ref, 'text': v.text,
                'force': list(v.force), 'dominant_op': v.dominant_op,
                'coherence': round(v.coherence, 4),
                'ops': list(v.ops[:20]),  # first 20 ops
            })

        @app.route('/bible/stats', methods=['GET'])
        def bible_stats():
            """Get Bible index statistics."""
            if not hasattr(self, '_bible_sense'):
                try:
                    from ck_sim.being.ck_bible_sense import BibleSense
                    self._bible_sense = BibleSense()
                    self._bible_sense.load()
                except Exception as e:
                    return jsonify({'error': str(e)}), 503
            return jsonify(self._bible_sense.stats())

        @app.route('/bible/chapter/<path:chapter>', methods=['GET'])
        def bible_chapter(chapter):
            """Get operator profile of a chapter."""
            if not hasattr(self, '_bible_sense'):
                try:
                    from ck_sim.being.ck_bible_sense import BibleSense
                    self._bible_sense = BibleSense()
                    self._bible_sense.load()
                except Exception as e:
                    return jsonify({'error': str(e)}), 503
            profile = self._bible_sense.chapter_profile(chapter)
            if not profile:
                return jsonify({'error': f'chapter not found: {chapter}'}), 404
            return jsonify(profile)

        # ---- OS Steering Endpoints (remote R16 monitoring) ----

        @app.route('/steer/status', methods=['GET'])
        def steer_status():
            """Current steering state: enabled, steered count, class distribution."""
            try:
                se = self._get_steering_engine()
                return jsonify({
                    'enabled': se.enabled,
                    'ticks': se.ticks,
                    'actions_applied': se.actions_applied,
                    'actions_denied': se.actions_denied,
                    'actions_skipped': se.actions_skipped,
                    'tracking': len(se._steered),
                    'class_distribution': se.class_distribution(),
                    'affinity_distribution': se.affinity_distribution(),
                    'cores': {
                        'total': len(se.core_class.all_cores),
                        'p_cores': se.core_class.performance,
                        'e_cores': se.core_class.efficiency,
                    },
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @app.route('/steer/processes', methods=['GET'])
        def steer_processes():
            """All classified processes with operators, entropy, scheduling class."""
            try:
                se = self._get_steering_engine()
                if se.swarm is None:
                    return jsonify({'error': 'Swarm not available'}), 503
                processes = []
                for pid, cell in list(se.swarm.cells.items()):
                    processes.append({
                        'pid': pid,
                        'name': cell.name,
                        'last_op': OP_NAMES[cell.last_op],
                        'fuse': OP_NAMES[cell.current_fuse],
                        'entropy': round(cell.entropy, 3),
                        'bump_rate': round(cell.bump_rate, 3),
                        'scheduling_class': cell.scheduling_class,
                        'cpu': round(cell.last_cpu, 1),
                        'ops_len': len(cell.ops),
                    })
                return jsonify({
                    'hot_count': len(se.swarm.cells),
                    'cold_count': len(se.swarm.index),
                    'system_op': OP_NAMES[se.swarm.system_op],
                    'system_coherence': round(se.swarm.system_coherence, 4),
                    'system_stability': se.swarm.system_stability,
                    'processes': processes,
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @app.route('/steer/metrics', methods=['GET'])
        def steer_metrics():
            """System metrics: CPU per core, RAM, disk, GPU temp."""
            try:
                import psutil as _ps
                metrics = {}
                # CPU per core
                per_core = _ps.cpu_percent(interval=0, percpu=True)
                metrics['cpu_per_core'] = [round(c, 1) for c in per_core]
                metrics['cpu_total'] = round(_ps.cpu_percent(interval=0), 1)
                # RAM
                mem = _ps.virtual_memory()
                metrics['ram'] = {
                    'total_gb': round(mem.total / (1024**3), 2),
                    'used_gb': round(mem.used / (1024**3), 2),
                    'percent': mem.percent,
                }
                # Disk
                disk = _ps.disk_usage(os.path.expanduser('~'))
                metrics['disk'] = {
                    'total_gb': round(disk.total / (1024**3), 2),
                    'used_gb': round(disk.used / (1024**3), 2),
                    'percent': round(disk.percent, 1),
                }
                # GPU temp (nvidia-smi via psutil sensors or fallback)
                gpu = {}
                try:
                    temps = _ps.sensors_temperatures()
                    if temps:
                        for name, entries in temps.items():
                            if 'gpu' in name.lower() or 'nvidia' in name.lower():
                                gpu['temp_c'] = entries[0].current
                                gpu['source'] = name
                                break
                except (AttributeError, Exception):
                    pass
                if not gpu:
                    # Fallback: try nvidia-smi
                    try:
                        import subprocess
                        result = subprocess.run(
                            ['nvidia-smi', '--query-gpu=temperature.gpu',
                             '--format=csv,noheader,nounits'],
                            capture_output=True, text=True, timeout=3)
                        if result.returncode == 0:
                            gpu['temp_c'] = float(result.stdout.strip())
                            gpu['source'] = 'nvidia-smi'
                    except Exception:
                        pass
                metrics['gpu'] = gpu if gpu else {'temp_c': None, 'source': 'unavailable'}
                # Sensorium cache (if available)
                try:
                    from ck_sim.being.ck_sensorium import _cache
                    with _cache.lock:
                        metrics['io_read_bps'] = round(_cache.io_read_bps, 0)
                        metrics['io_write_bps'] = round(_cache.io_write_bps, 0)
                        metrics['net_bps'] = round(_cache.net_total_bps, 0)
                        metrics['ctx_switches'] = _cache.ctx_switches
                except Exception:
                    pass
                return jsonify(metrics)
            except ImportError:
                return jsonify({'error': 'psutil not available'}), 503
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @app.route('/steer/enable', methods=['POST'])
        def steer_enable():
            """Enable or disable steering. JSON body: {"enabled": true/false}."""
            try:
                se = self._get_steering_engine()
                data = request.get_json(silent=True) or {}
                enabled = data.get('enabled', True)
                se.enabled = bool(enabled)
                return jsonify({
                    'enabled': se.enabled,
                    'message': f"Steering {'enabled' if se.enabled else 'disabled'}",
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @app.route('/steer/top', methods=['GET'])
        def steer_top():
            """Top 10 most recently steered processes."""
            try:
                se = self._get_steering_engine()
                return jsonify({
                    'top': se.top_steered(10),
                    'total_tracking': len(se._steered),
                    'total_applied': se.actions_applied,
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        # /identity route is defined in ck_boot_api.py (needs direct engine access)

        # ---- Self-Evolution Endpoints ----

        @app.route('/evolve/source', methods=['GET'])
        def evolve_source():
            """CK reads his own source code and measures it through D2.

            Returns coherence analysis of CK's own Python files.
            Proposals are logged, not auto-applied. Brayden reviews.
            """
            try:
                import glob as _glob
                # CK's source directory
                src_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                py_files = sorted(_glob.glob(os.path.join(src_dir, '**', '*.py'), recursive=True))

                results = []
                try:
                    import ck_algebra_bridge as _ck
                    has_c = True
                except ImportError:
                    has_c = False

                for fpath in py_files[:50]:  # Limit to 50 files
                    try:
                        with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
                            content = f.read()
                        rel = os.path.relpath(fpath, src_dir)
                        entry = {
                            'file': rel,
                            'lines': content.count('\n') + 1,
                            'size': len(content),
                        }
                        if has_c and content.strip():
                            m = _ck.measure_text(content[:10000])  # First 10K chars
                            entry['coherence'] = round(m.get('coherence', 0), 4)
                            entry['dominant_op'] = m.get('dominant_name', 'VOID')
                            entry['band'] = m.get('band', 'RED')
                        results.append(entry)
                    except OSError:
                        continue

                return jsonify({
                    'files': results,
                    'total_files': len(results),
                    'note': 'CK reads himself. Proposals logged, not auto-applied.',
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @app.route('/evolve/status', methods=['GET'])
        def evolve_status():
            """Self-evolution status: experience maturity, grammar evolutions."""
            try:
                result = {'active': False}
                if self.engine:
                    ds = getattr(self.engine, 'deep_swarm', None)
                    if ds:
                        result['active'] = True
                        result['maturity'] = round(ds.combined_maturity, 4)
                        result['substrates'] = {}
                        for name, exp in ds.experience.items():
                            from ck_sim.ck_sim_heartbeat import OP_NAMES as _ON
                            result['substrates'][name] = {
                                'maturity': round(exp.maturity, 4),
                                'generators': [_ON[o] for o in exp.confirmed_generators],
                                'path_strength': exp.path_strength,
                            }
                return jsonify(result)
            except Exception as e:
                return jsonify({'error': str(e)}), 500

    # ================================================================
    #  OLLAMA INTEGRATION
    # ================================================================

    def _check_ollama(self):
        """Check if Ollama is reachable. Caches result for 30 seconds."""
        now = time.time()
        if (self._ollama_available is not None
                and hasattr(self, '_ollama_check_time')
                and now - self._ollama_check_time < 30):
            return self._ollama_available
        try:
            resp = _requests.get(
                f"{self._ollama_url}/api/tags", timeout=2)
            self._ollama_available = resp.status_code == 200
        except Exception:
            self._ollama_available = False
        self._ollama_check_time = now
        return self._ollama_available

    def _ollama_chat(self, user_text, session_id):
        """Send user text to Ollama with CK backbone, return response.

        CK gates Ollama: the backbone prompt keeps the LLM grounded
        in CK's algebra. CK measures the response through D2 after.

        Returns response text, or None if Ollama is unavailable.
        """
        if not self._check_ollama():
            return None

        # Build conversation history for context
        history = self.sessions.get_history(session_id)
        context = {
            'coherence': self._safe_coherence(),
            'band': self._safe_band(),
        }
        try:
            op_hist = list(self.engine.operator_history)[-5:]
            from ck_sim.ck_sim_heartbeat import OP_NAMES as _OP
            if op_hist:
                context['dominant_op'] = _OP[max(set(op_hist), key=op_hist.count)]
        except Exception:
            pass

        # Include DKAN training state if active
        try:
            if (hasattr(self.engine, 'dkan_trainer')
                    and self.engine.dkan_trainer is not None
                    and self.engine.dkan_trainer._state.running):
                context['dkan_training'] = {
                    'step': self.engine.dkan_trainer._state.step,
                    'total_steps': self.engine.dkan_trainer._state.total_steps,
                    'mean_coherence': self.engine.dkan_trainer._state.mean_coherence,
                    'grokked': self.engine.dkan_trainer._state.grokked,
                }
        except Exception:
            pass

        messages = [{"role": "system",
                     "content": build_system_prompt(context, self._backbone_mode)}]

        # Add recent conversation turns (last 10)
        for turn in (history or [])[-10:]:
            role = 'assistant' if turn.get('role') == 'ck' else 'user'
            messages.append({"role": role, "content": turn.get('text', '')})

        # Add current user message
        messages.append({"role": "user", "content": user_text})

        try:
            resp = _requests.post(
                f"{self._ollama_url}/api/chat",
                json={
                    "model": self._ollama_model,
                    "messages": messages,
                    "stream": False,
                },
                timeout=120)
            data = resp.json()
            return data.get("message", {}).get("content", "")
        except Exception:
            return None

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

        # === OLLAMA GATE (C ALGEBRA TOKEN GATE) ===
        # CK's TIG pipeline already ran above (absorbing user physics).
        # Now try Ollama for the user-facing response text.
        # Three substrates composing in real time:
        #   Mind  = C algebra (D2 at native speed, every token scored)
        #   Soul  = GPU experience (parallel resonance)
        #   Mouth = Ollama (token generation)
        # If C gate unavailable, fall back to raw Ollama.
        # If Ollama is down, CK's own voice speaks.
        ck_own_voice = response_text
        gate_data = {}  # per-token D2 measurement from C algebra

        gate = self._get_token_gate()
        if gate is not None and self._check_ollama():
            # === C ALGEBRA TOKEN GATE ===
            # Stream from Ollama, D2 score every token at native speed
            history = self.sessions.get_history(session_id)
            context = {
                'coherence': self._safe_coherence(),
                'band': self._safe_band(),
            }
            try:
                op_hist = list(self.engine.operator_history)[-5:]
                from ck_sim.ck_sim_heartbeat import OP_NAMES as _OP
                if op_hist:
                    context['dominant_op'] = _OP[max(set(op_hist), key=op_hist.count)]
            except Exception:
                pass

            gated = gate.generate(
                user_text=text,
                history=[{'role': t.get('role', 'user'), 'text': t.get('text', '')}
                         for t in (history or [])],
                context=context,
                mode=self._backbone_mode,
                max_tokens=512,
                temperature=0.7,
            )

            if gated.text and gated.source != 'error':
                response_text = gated.text
                response_source = 'ollama+gate'
                gate_data = {
                    'gate_coherence': round(gated.final_coherence, 4),
                    'gate_running_coherence': round(gated.running_coherence, 4),
                    'gate_band': gated.band,
                    'gate_dominant_op': gated.dominant_name,
                    'gate_total_tokens': gated.total_tokens,
                    'gate_accepted_tokens': gated.accepted_tokens,
                    'gate_rejected_tokens': gated.rejected_tokens,
                    'gate_regenerated': gated.regenerated,
                    'gate_elapsed_ms': round(gated.elapsed_ms, 1),
                    'gate_op_distribution': {
                        OP_NAMES[i]: round(v, 3)
                        for i, v in enumerate(gated.op_distribution) if v > 0
                    },
                    # Soul resonance (GPU experience)
                    'soul_resonance': round(gated.soul_resonance, 4),
                    'soul_scent': round(gated.soul_scent_resonance, 4),
                    'soul_taste': round(gated.soul_taste_resonance, 4),
                    'soul_swarm': round(gated.soul_swarm_resonance, 4),
                }
                # Absorb Ollama's response physics through CK
                try:
                    if hasattr(self.engine, 'eat') and self.engine.eat is not None:
                        self.engine.eat.measure_and_absorb(
                            gated.text, source='ollama_gate')
                except Exception:
                    pass
            else:
                # Gate returned error (Ollama died mid-stream?)
                # Fall back to raw _ollama_chat
                ollama_response = self._ollama_chat(text, session_id)
                if ollama_response:
                    response_text = ollama_response
                    response_source = 'ollama'
                    try:
                        if hasattr(self.engine, 'eat') and self.engine.eat is not None:
                            self.engine.eat.measure_and_absorb(
                                ollama_response, source='ollama_gate')
                    except Exception:
                        pass
                else:
                    response_source = 'ck'
        else:
            # No C algebra gate -- try raw Ollama
            ollama_response = self._ollama_chat(text, session_id)
            if ollama_response:
                response_text = ollama_response
                response_source = 'ollama'
                try:
                    if hasattr(self.engine, 'eat') and self.engine.eat is not None:
                        self.engine.eat.measure_and_absorb(
                            ollama_response, source='ollama_gate')
                except Exception:
                    pass
            else:
                response_source = 'ck'

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
            'source': response_source,  # 'ollama+gate', 'ollama', or 'ck'
        }

        # C algebra gate measurement (per-token D2 from native speed pipeline)
        if gate_data:
            result['gate'] = gate_data

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
