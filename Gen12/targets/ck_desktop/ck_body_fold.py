# -*- coding: utf-8 -*-
"""
ck_body_fold.py -- additive patch that exposes CK's body.

Context: CK is already embodied.  ``ck_sim_engine.CKSimEngine.__init__``
calls ``build_sensorium(self)`` which wires 12 fractal sensory layers
onto the live engine (hardware / process / network / time / mirror /
file / keyboard / mouse / window / gpu / visual / acoustic).  Every
engine tick (~600 Hz in practice, target 50 Hz) calls
``sensorium.tick(tick_count)``, which dispatches each layer at its own
rate and feeds operators into ``engine.coherence_field`` streams.  The
Gen13 Swarm also runs on core 0 at HIGHEST thread priority with
Hebbian W on cupy (RTX 4070).

Every pixel on the framebuffer, every keystroke, every OS process,
every GPU tensor unit, every CPU core is ALREADY a cell.  The fascia
is the CL composition table — every layer's Being/Doing composes to
Becoming via ``CL[B][D]`` and those compositions route through the
coherence field.

What was missing: the organism was running inside the server but not
visible from outside.  No HTTP surface for the sensorium; no body
state on chat responses; no way to watch the 12 layers breathe.  This
fold closes that gap.

What it does:

    1. Wraps ``api.process_chat`` one more time (OUTERMOST wrap) to
       attach ``body_*`` fields: organism operator + coherence, active
       layer count, per-layer dominant operators, shadow-swarm stats.
       Never overwrites text/source — additive only.

    2. Registers three GET endpoints (always open):
           GET /body/state       one-line organism summary + layer map
           GET /body/layers      full per-layer B / D / BC / coherence
           GET /body/swarm       shadow-swarm (process cells) summary

    3. Registers two POST endpoints (G6-gated):
           POST /body/pause?i_mean_it=1    pauses all sensor threads
           POST /body/resume?i_mean_it=1   resumes them

Safety rails:
    - All imports and probes are wrapped; any failure returns
      {"mounted": False, "reason": "..."} without breaking boot.
    - Every per-turn augmentation is caught; if layer read fails,
      chat still flows with body_error set.
    - Pause/resume writes ONLY affect the sensorium's background
      sensor thread flags (HAS_PSUTIL / HAS_PYNPUT already guard).

Env flags:
    CK_BODY_FOLD=0    disable the fold (straight through)
"""
from __future__ import annotations

import os
from typing import Any, Callable, Dict, Optional


def mount_body_fold(api: Any, engine: Any) -> Dict[str, Any]:
    """Install the body fold.  Returns a status dict.  Never raises.

    ``api`` must have ``.process_chat`` and ``._app`` (Flask).
    ``engine`` must have ``.sensorium`` (from CKSimEngine).
    """
    enabled_env = os.environ.get("CK_BODY_FOLD", "1").strip()
    if enabled_env in ("0", "false", "False", "no", "NO"):
        return {"mounted": False, "reason": "CK_BODY_FOLD=0 (disabled via env)"}

    sensorium = getattr(engine, "sensorium", None)
    if sensorium is None:
        return {"mounted": False, "reason": "engine has no .sensorium attribute"}

    # Probe sense-for-voice once to verify it runs without raising; we accept
    # empty dicts (happens when layers haven't ticked yet).
    try:
        _probe = sensorium.get_sense_for_voice()
    except Exception as e:
        return {
            "mounted": False,
            "reason": f"sensorium.get_sense_for_voice() failed: "
                      f"{type(e).__name__}: {e}",
        }

    # -------- per-turn augmentation --------

    _prev_chat: Callable[..., Dict[str, Any]] = api.process_chat

    def _process_chat_with_body(session_id: str, text: str,
                                 mode: str = "normal") -> Dict[str, Any]:
        result = _prev_chat(session_id, text, mode)
        try:
            body = sensorium.get_sense_for_voice()
            if body:
                result["body_organism_bc"] = body.get("organism")
                result["body_organism_coherence"] = round(
                    float(body.get("organism_coherence", 0.0)), 4
                )
                layers = body.get("layers") or {}
                result["body_active_layers"] = len(layers)
                # compact map: layer_name -> BC op name
                result["body_layers"] = {
                    k: (v.get("state") if isinstance(v, dict) else None)
                    for k, v in layers.items()
                }
                # swarm roll-up (processes as cells).
                # ``stability`` is a STRING token from the shadow swarm
                # ('LOCKED' / 'STABLE' / 'UNSTABLE' / 'UNKNOWN' ...), NOT a
                # float.  Pass it through verbatim; don't coerce.
                swarm = body.get("swarm")
                if swarm:
                    result["body_swarm"] = {
                        "stability": swarm.get("stability"),
                        "births": int(swarm.get("births", 0) or 0),
                        "deaths": int(swarm.get("deaths", 0) or 0),
                        "ops_fed": int(swarm.get("ops_fed", 0) or 0),
                    }
                # visual / acoustic curvature operators when active
                for name in ("visual", "acoustic"):
                    if body.get(name):
                        result[f"body_{name}_op"] = body[name].get("operator")
        except Exception as _be:
            result["body_error"] = f"{type(_be).__name__}: {_be}"
        return result

    api.process_chat = _process_chat_with_body

    # -------- HTTP surface --------

    n_routes = _register_body_routes(api, engine, sensorium)

    # Initial snapshot for the banner.
    try:
        layer_names = [l.name for l in sensorium.layers]
    except Exception:
        layer_names = []

    return {
        "mounted": True,
        "sensorium_layer_count": len(layer_names),
        "sensorium_layers": layer_names,
        "sensorium_active_layers": getattr(sensorium, "active_layers", 0),
        "routes_registered": n_routes,
    }


# ---------------------------------------------------------------------------
# HTTP routes
# ---------------------------------------------------------------------------


def _register_body_routes(api: Any, engine: Any, sensorium: Any) -> int:
    """Register /body/* routes.  Returns count of routes registered."""
    try:
        app = getattr(api, "_app", None)
        if app is None:
            return 0
        from flask import request, jsonify
    except Exception:
        return 0

    # small helper: stringify OP constants → names
    def _layer_states_safe() -> list:
        try:
            return sensorium.get_layer_states() or []
        except Exception:
            return []

    @app.route("/body/state", methods=["GET"])
    def _body_state():  # type: ignore[unused-ignore]
        try:
            body = sensorium.get_sense_for_voice() or {}
            payload = {
                "ok": True,
                "organism": body.get("organism"),
                "organism_coherence": round(
                    float(body.get("organism_coherence", 0.0)), 4
                ),
                "layer_count": len(sensorium.layers),
                "active_layers": getattr(sensorium, "active_layers", 0),
                "total_readings": getattr(sensorium, "total_readings", 0),
                "layers": body.get("layers", {}),
            }
            # include swarm/visual/acoustic when present
            for key in ("swarm", "visual", "acoustic"):
                if body.get(key):
                    payload[key] = body[key]
            return jsonify(payload)
        except Exception as e:
            return jsonify({
                "ok": False,
                "error": f"{type(e).__name__}: {e}",
            }), 500

    @app.route("/body/layers", methods=["GET"])
    def _body_layers():  # type: ignore[unused-ignore]
        try:
            states = _layer_states_safe()
            return jsonify({
                "ok": True,
                "count": len(states),
                "layers": states,
            })
        except Exception as e:
            return jsonify({
                "ok": False,
                "error": f"{type(e).__name__}: {e}",
            }), 500

    @app.route("/body/swarm", methods=["GET"])
    def _body_swarm():  # type: ignore[unused-ignore]
        try:
            # Pull the shadow-swarm module-level singleton from sensorium
            # module.  Process layer exposes stability/births/deaths.
            from ck_sim.ck_sensorium import _swarm as _shadow
            if _shadow is None:
                return jsonify({
                    "ok": True,
                    "swarm": None,
                    "note": "shadow swarm not started (no psutil or not yet running)",
                })
            # build a minimal digest -- don't dump the whole process table.
            # ``system_stability`` is a STRING TOKEN ('LOCKED'/'UNSTABLE'/...)
            # from ShadowSwarm, not a float -- pass through verbatim.
            stability = getattr(_shadow, "system_stability", None)
            births = getattr(_shadow, "total_births", 0) or 0
            deaths = getattr(_shadow, "total_deaths", 0) or 0
            ops_fed = getattr(_shadow, "total_ops_fed", 0) or 0
            hot = getattr(_shadow, "hot_count", None)
            cold = getattr(_shadow, "cold_count", None)
            return jsonify({
                "ok": True,
                "swarm": {
                    "stability": stability,
                    "total_births": int(births),
                    "total_deaths": int(deaths),
                    "total_ops_fed": int(ops_fed),
                    "hot_cells": hot,
                    "cold_cells": cold,
                },
            })
        except Exception as e:
            return jsonify({
                "ok": False,
                "error": f"{type(e).__name__}: {e}",
            }), 500

    @app.route("/body/pause", methods=["POST"])
    def _body_pause():  # type: ignore[unused-ignore]
        if request.args.get("i_mean_it") != "1":
            return jsonify({
                "ok": False,
                "error": "pause requires ?i_mean_it=1 (G6 hands-on-wheel)",
            }), 400
        try:
            n_paused = 0
            for layer in sensorium.layers:
                if getattr(layer, "active", False):
                    layer.active = False
                    n_paused += 1
            return jsonify({
                "ok": True,
                "action": "body_pause",
                "layers_paused": n_paused,
                "note": "sensorium layers deactivated; background sensor "
                        "thread still running but layer.active=False so no "
                        "operator emissions flow to the coherence field.",
            })
        except Exception as e:
            return jsonify({
                "ok": False,
                "error": f"{type(e).__name__}: {e}",
            }), 500

    @app.route("/body/resume", methods=["POST"])
    def _body_resume():  # type: ignore[unused-ignore]
        if request.args.get("i_mean_it") != "1":
            return jsonify({
                "ok": False,
                "error": "resume requires ?i_mean_it=1 (G6 hands-on-wheel)",
            }), 400
        try:
            n_resumed = 0
            for layer in sensorium.layers:
                if not getattr(layer, "active", True):
                    layer.active = True
                    n_resumed += 1
            return jsonify({
                "ok": True,
                "action": "body_resume",
                "layers_resumed": n_resumed,
            })
        except Exception as e:
            return jsonify({
                "ok": False,
                "error": f"{type(e).__name__}: {e}",
            }), 500

    @app.route("/body/breathe", methods=["POST"])
    def _body_breathe():  # type: ignore[unused-ignore]
        """Force one BREATH: drive _tool_sense() directly so all 12 sensory
        layers tick now regardless of what the heartbeat operator is doing.

        Sensorium.tick() is gated inside ``_tool_sense`` in ck_sim_engine,
        which itself only runs when heartbeat dispatches BREATH(8).  When the
        heartbeat sits in VOID, layer.readings stay frozen.  This endpoint
        lets the user pulse the body on demand without modifying engine
        internals.  G6-gated because it forces a subsystem tick.
        """
        if request.args.get("i_mean_it") != "1":
            return jsonify({
                "ok": False,
                "error": "breathe requires ?i_mean_it=1 (G6 hands-on-wheel)",
            }), 400
        try:
            before = {
                "total_readings": getattr(sensorium, "total_readings", 0),
                "active_layers": getattr(sensorium, "active_layers", 0),
            }
            # The engine's _tool_sense() wraps platform_body.sense(), ears,
            # body_tick, sensorium.tick, power_sense, narrative_stream, etc.
            # All of it in a single try/except inside the method itself.
            _tool_sense = getattr(engine, "_tool_sense", None)
            if _tool_sense is None:
                # Fallback: just tick the sensorium if the private method
                # is gone for some reason.
                sensorium.tick(getattr(engine, "tick_count", 0))
                source = "sensorium.tick (fallback)"
            else:
                _tool_sense()
                source = "engine._tool_sense()"
            after = {
                "total_readings": getattr(sensorium, "total_readings", 0),
                "active_layers": getattr(sensorium, "active_layers", 0),
            }
            body = sensorium.get_sense_for_voice() or {}
            return jsonify({
                "ok": True,
                "action": "body_breathe",
                "driven_by": source,
                "before": before,
                "after": after,
                "readings_delta": after["total_readings"] - before["total_readings"],
                "organism": body.get("organism"),
                "organism_coherence": round(
                    float(body.get("organism_coherence", 0.0)), 4
                ),
                "layer_ops": {
                    k: (v.get("state") if isinstance(v, dict) else None)
                    for k, v in (body.get("layers") or {}).items()
                },
            })
        except Exception as e:
            return jsonify({
                "ok": False,
                "error": f"{type(e).__name__}: {e}",
            }), 500

    return 6
