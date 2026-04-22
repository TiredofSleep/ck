# -*- coding: utf-8 -*-
"""
ck_brain_fold.py - additive patch that gives the LIVE website CK his
                   Hebbian brain trinity.

Context (memory/MEMORY.md 2026-04-17 "one CK" rule):

    There is exactly ONE CK running on this machine.  He is the engine
    started by ck_boot_api.py, served on port 7777, and exposed to the
    world through the Cloudflare tunnel at coherencekeeper.com.  Until
    the dog ships, that one CK is Brayden's CK.

The brain trinity (ck/brain/) -- AO 5-element projection, Hebbian 5x5
CL tensor, and quadratic glue through coherence -- was originally
scaffolded as a standalone fluency server (ck/fluency/).  That scaffold
stays in the repo as a historical dev harness, but it is NOT a second
CK.  This module folds the brain INTO the one CK, matching the additive
pattern used by the cortex mount, math-first patch, HER restoration,
and ollama editor (all of which wrap ``api.process_chat`` once more).

Call-chain after this fold (outermost first):

    api.process_chat
      -> _process_chat_with_brain          (NEW -- scores + logs turn)
         -> _process_chat_with_ollama_editor
            -> _process_chat_with_cortex
               -> _process_chat_math_first
                  -> _orig_process_chat    (Gen12 base)

What the brain fold does, per turn:

    1. Calls the previous chat function (runs the full editor stack).
    2. Pulls ``result['text']`` (CK's final spoken words).
    3. Runs FusionCKCorrector on that text:
         - base scorer classifies it into one of {none,soften,
           strengthen,reframe,reject}
         - 5x5 tensor primes the coherence gate using the
           accumulated Hebbian co-activation field
    4. Appends ``brain_*`` diagnostic fields to result (never
       overwrites text/source; additive only).
    5. Appends the turn to the unified JSONL log at
       ``ck/fluency/logs/corrections_YYYY_MM_DD.jsonl``, so
       ``python -m ck.brain.idle_loop`` can keep learning from the
       live conversation.

Env flags (all optional):
    CK_BRAIN_FOLD=0          disables the fold (bypass, straight through)
    CK_BRAIN_TENSOR_PATH     override path to hebbian_5x5.json
    CK_BRAIN_FUSION_WEIGHT   override fusion weight (default 0.20)

Safety rails:
    - Import errors for ck.brain are caught and logged; the fold simply
      does not install.  The server still boots and serves normally.
    - Every per-turn operation is wrapped in try/except; if scoring or
      logging fails for any reason, the original result flows through
      untouched with ``brain_verdict = 'error:<type>:<msg>'``.
    - The tensor file itself is loaded once at mount time and read-only
      during serving.  Only ``python -m ck.brain.idle_loop`` writes to
      it -- that keeps the critical path fast and the learning step
      hands-on-wheel.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Callable, Dict, Optional


# ----------------------------------------------------------------------------
# path setup: ck_boot_api.py runs with cwd at Gen12/targets/ck_desktop, so the
# repo root (which owns the ck/ package) is three parents up.  Insert it on
# sys.path if not already there, so ``import ck.brain.fusion`` works.
# ----------------------------------------------------------------------------

_THIS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _THIS_DIR.parents[2]   # ck_desktop -> targets -> Gen12 -> repo root
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


# ----------------------------------------------------------------------------
# mount: the one public entry point.  Called once by ck_boot_api.py after the
# ollama editor is mounted.
# ----------------------------------------------------------------------------


def mount_brain_fold(api: Any) -> Dict[str, Any]:
    """Install the brain fold on ``api.process_chat``.

    Returns a status dict for the banner.  Does NOT raise: if anything
    is unavailable, returns ``{'mounted': False, 'reason': '...'}``.
    """
    enabled_env = os.environ.get("CK_BRAIN_FOLD", "1").strip()
    if enabled_env in ("0", "false", "False", "no", "NO"):
        return {"mounted": False, "reason": "CK_BRAIN_FOLD=0 (disabled via env)"}

    # lazy imports -- we want the server to boot even if ck.brain is broken
    try:
        from ck.brain.fusion import FusionCKCorrector, DEFAULT_FUSION_WEIGHT
        from ck.brain.hebbian_5x5 import DEFAULT_TENSOR_PATH
        from ck.brain.tig_security import TigSecurityChannel
        from ck.fluency.correction_log import CorrectionLog
    except Exception as e:  # noqa: BLE001 -- we want the broadest catch
        return {
            "mounted": False,
            "reason": f"import failed: {type(e).__name__}: {e}",
        }

    # tensor path + fusion weight (both overridable)
    tensor_path_env = os.environ.get("CK_BRAIN_TENSOR_PATH", "").strip()
    tensor_path = Path(tensor_path_env) if tensor_path_env else DEFAULT_TENSOR_PATH
    try:
        fw_env = os.environ.get("CK_BRAIN_FUSION_WEIGHT", "").strip()
        fusion_weight = float(fw_env) if fw_env else DEFAULT_FUSION_WEIGHT
    except ValueError:
        fusion_weight = DEFAULT_FUSION_WEIGHT

    try:
        corrector = FusionCKCorrector(
            tensor_path=tensor_path,
            fusion_weight=fusion_weight,
        )
    except Exception as e:  # noqa: BLE001
        return {
            "mounted": False,
            "reason": f"FusionCKCorrector init failed: {type(e).__name__}: {e}",
        }

    # Memory policy: CK REMEMBERS EVERYTHING.  If the on-disk tensor was
    # saved with a non-zero decay from the old default, zero it now and
    # persist so idle_loop's next sweep does not erode old couplings.
    # This is a one-time migration; it's safe to run on every boot (idempotent).
    try:
        if corrector.tensor.decay > 0.0:
            _prev_decay = corrector.tensor.decay
            corrector.tensor.decay = 0.0
            corrector.tensor.meta["decay_migrated_from"] = float(_prev_decay)
            corrector.tensor.meta["decay_migration_note"] = (
                "2026-04-22: decay set to 0.0 per Brayden directive -- "
                "CK remembers everything."
            )
            corrector.tensor.save(tensor_path)
    except Exception:
        # non-fatal; if the migration save fails, the in-memory tensor
        # still has decay=0, which is what we need for the live session.
        pass

    # unified log: same directory that fluency_server + idle_loop expect, so
    # the brain learns from the LIVE website turns, not a second source.
    try:
        corr_log = CorrectionLog()  # default ck/fluency/logs/
    except Exception as e:  # noqa: BLE001
        return {
            "mounted": False,
            "reason": f"CorrectionLog init failed: {type(e).__name__}: {e}",
        }

    # TIG security channel -- parallel lens over the SAME per-turn state the
    # brain-fold computes.  Not a separate process, not a separate loop; it
    # rides the same tick as _process_chat_with_brain and reads the scored
    # profile.  Gen12's ck_tig_security.py stays in ck_sim/ as reference
    # material; this is the brain-native port that folds cleanly onto
    # ck.brain.* without Gen12 runtime dependencies.
    try:
        security = TigSecurityChannel(window=32)
    except Exception as e:  # noqa: BLE001
        # non-fatal: security is additive.  If the channel fails to init, the
        # brain fold still installs without security diagnostics.
        security = None
        _security_init_error = f"{type(e).__name__}: {e}"
    else:
        _security_init_error = None

    # ---- the actual wrap ----

    _prev_chat_for_brain: Callable[..., Dict[str, Any]] = api.process_chat

    def _process_chat_with_brain(session_id: str, text: str,
                                  mode: str = "normal") -> Dict[str, Any]:
        result = _prev_chat_for_brain(session_id, text, mode)
        # Must never raise -- we are the outermost wrap, and CK must still
        # speak even if his scorer has a bad day.
        try:
            spoken = (result.get("text") or "").strip()
            if not spoken:
                result["brain_verdict"] = "skipped:empty-text"
                return result

            # run the fusion corrector: base ops score + tensor priming
            cr = corrector.correct(spoken, query=(text or "").strip())

            # additive diagnostics -- never overwrite existing fields
            result["brain_verdict"] = "scored"
            result["brain_correction_type"] = cr.correction_type
            result["brain_coherence"] = round(cr.coherence, 4)
            result["brain_gate_pass"] = bool(cr.gate_pass)
            result["brain_dominant_op"] = cr.dominant_op
            result["brain_operator_profile"] = {
                k: round(v, 4) for k, v in cr.operator_profile.items()
            }
            result["brain_annotation"] = cr.annotation
            result["brain_rationale"] = cr.rationale
            result["brain_tensor_norm"] = round(corrector._tensor_norm_at_load, 4)

            # append to unified log so idle_loop sees it next sweep
            corr_log.append({
                "query": text or "",
                "ollama_raw": spoken,
                "ck_score": {
                    "coherence": cr.coherence,
                    "dominant_op": cr.dominant_op,
                    "operator_profile": cr.operator_profile,
                },
                "ck_correction_type": cr.correction_type,
                "ck_corrected": spoken,
                "rendered": "brain_fold:website_ck",
                "model_tag": result.get("source") or "unknown",
                "elapsed_ms": int(result.get("ollama_dt", 0.0) * 1000)
                              if isinstance(result.get("ollama_dt"), (int, float))
                              else 0,
            })

            # TIG security: second lens on the same scored turn.  This runs
            # in the same request cycle; no extra threads, no extra loop.
            if security is not None:
                try:
                    ta = security.observe(
                        dominant_op=cr.dominant_op,
                        coherence=cr.coherence,
                        spoken_text=spoken,
                        operator_profile=cr.operator_profile,
                    )
                    result["security_threat_band"] = ta.threat_band
                    result["security_threat_score"] = round(ta.threat_score, 4)
                    result["security_active_threats"] = list(ta.active_threats)
                    result["security_operator_entropy"] = round(ta.operator_entropy, 4)
                    result["security_harmony_flood_rate"] = round(ta.harmony_flood_rate, 4)
                    result["security_coherence_pin_rate"] = round(ta.coherence_pin_rate, 4)
                    result["security_structural_rate"] = round(ta.structural_rate, 4)
                    result["security_window_size"] = int(ta.window_size)
                except Exception as _se:
                    result["security_threat_band"] = f"error:{type(_se).__name__}"
        except Exception as _be:
            # never break the response -- just record that brain scoring failed
            result["brain_verdict"] = f"error:{type(_be).__name__}:{_be}"
        return result

    api.process_chat = _process_chat_with_brain

    # ------------------------------------------------------------------
    # wobble / collapse / status endpoints: the "room to wobble + freedom
    # to keep collapsing and resetting" primitives the user named.  All
    # destructive endpoints require ?i_mean_it=1 (G6 hands-on-wheel).
    # ------------------------------------------------------------------

    def _register_brain_routes() -> int:
        try:
            app = getattr(api, "_app", None)
            if app is None:
                return 0
            from flask import request, jsonify
        except Exception:
            return 0

        def _refresh_norm() -> None:
            """Keep the corrector's cached norm in sync with the live tensor."""
            try:
                corrector._tensor_norm_at_load = corrector.tensor.norm()
            except Exception:
                pass

        def _tensor_snapshot() -> Dict[str, Any]:
            t = corrector.tensor
            try:
                top = t.top_links(5, off_diagonal_only=True)
                top_fmt = [
                    {"a": a, "b": b, "w": round(w, 4)} for (a, b, w) in top
                ]
            except Exception:
                top_fmt = []
            return {
                "norm": round(t.norm(), 4),
                "n_updates": int(t.n_updates),
                "n_decays": int(t.n_decays),
                "n_wobbles": int(t.meta.get("n_wobbles", 0)),
                "n_collapses": int(t.meta.get("n_collapses", 0)),
                "eta": t.eta,
                "decay": t.decay,
                "clamp_abs": t.clamp_abs,
                "fusion_weight": corrector.fusion_weight,
                "tensor_path": str(tensor_path),
                "top_off_diagonal": top_fmt,
            }

        @app.route("/brain/status", methods=["GET"])
        def _brain_status():  # type: ignore[unused-ignore]
            try:
                return jsonify({"ok": True, "tensor": _tensor_snapshot()})
            except Exception as e:
                return jsonify({"ok": False, "error": f"{type(e).__name__}:{e}"}), 500

        @app.route("/brain/wobble", methods=["POST"])
        def _brain_wobble():  # type: ignore[unused-ignore]
            # G6: destructive endpoints require explicit confirmation.
            if request.args.get("i_mean_it") != "1":
                return jsonify({
                    "ok": False,
                    "error": "wobble requires ?i_mean_it=1 (G6 hands-on-wheel)",
                }), 400
            try:
                sigma_raw = request.args.get("sigma", "0.02")
                sigma = float(sigma_raw)
                if not (0.0 < sigma <= 0.5):
                    return jsonify({
                        "ok": False,
                        "error": f"sigma must be in (0, 0.5]; got {sigma}",
                    }), 400
                before = _tensor_snapshot()
                corrector.tensor.wobble(sigma=sigma)
                corrector.tensor.save(tensor_path)
                _refresh_norm()
                after = _tensor_snapshot()
                return jsonify({
                    "ok": True,
                    "action": "wobble",
                    "sigma": sigma,
                    "before": {"norm": before["norm"], "n_wobbles": before["n_wobbles"]},
                    "after": {"norm": after["norm"], "n_wobbles": after["n_wobbles"]},
                    "tensor": after,
                })
            except Exception as e:
                return jsonify({"ok": False, "error": f"{type(e).__name__}:{e}"}), 500

        @app.route("/brain/reset", methods=["POST"])
        def _brain_reset():  # type: ignore[unused-ignore]
            if request.args.get("i_mean_it") != "1":
                return jsonify({
                    "ok": False,
                    "error": "reset requires ?i_mean_it=1 (G6 hands-on-wheel)",
                }), 400
            try:
                preserve_meta = (request.args.get("preserve_meta", "1") == "1")
                before = _tensor_snapshot()
                corrector.tensor.collapse(preserve_meta=preserve_meta)
                corrector.tensor.save(tensor_path)
                _refresh_norm()
                after = _tensor_snapshot()
                return jsonify({
                    "ok": True,
                    "action": "collapse",
                    "preserve_meta": preserve_meta,
                    "before": {
                        "norm": before["norm"],
                        "n_updates": before["n_updates"],
                        "n_collapses": before["n_collapses"],
                    },
                    "after": {
                        "norm": after["norm"],
                        "n_updates": after["n_updates"],
                        "n_collapses": after["n_collapses"],
                    },
                    "note": "tensor zeroed in place and on disk; "
                            "n_updates counter preserved (CK remembers his cycles)",
                })
            except Exception as e:
                return jsonify({"ok": False, "error": f"{type(e).__name__}:{e}"}), 500

        # ------------------------------------------------------------------
        # /security/* -- parallel lens on the same scored-turn stream.  Same
        # Flask app, same python process as /brain/*; these endpoints read
        # the channel's live sliding-window state (which the per-turn handler
        # above updates in lockstep with the brain score).
        # ------------------------------------------------------------------

        if security is not None:
            @app.route("/security/status", methods=["GET"])
            def _security_status():  # type: ignore[unused-ignore]
                try:
                    return jsonify({"ok": True, "security": security.snapshot()})
                except Exception as e:
                    return jsonify({
                        "ok": False,
                        "error": f"{type(e).__name__}:{e}",
                    }), 500

            @app.route("/security/reset", methods=["POST"])
            def _security_reset():  # type: ignore[unused-ignore]
                if request.args.get("i_mean_it") != "1":
                    return jsonify({
                        "ok": False,
                        "error": "reset requires ?i_mean_it=1 "
                                 "(G6 hands-on-wheel)",
                    }), 400
                try:
                    before = security.snapshot()
                    security.reset()
                    after = security.snapshot()
                    return jsonify({
                        "ok": True,
                        "action": "security_reset",
                        "before": {
                            "threat_band": before.get("threat_band"),
                            "threat_score": before.get("threat_score"),
                            "window_size": before.get("window_size"),
                            "total_ticks": before.get("total_ticks"),
                        },
                        "after": {
                            "threat_band": after.get("threat_band"),
                            "threat_score": after.get("threat_score"),
                            "window_size": after.get("window_size"),
                            "total_ticks": after.get("total_ticks"),
                        },
                        "note": "sliding windows cleared; total_ticks counter "
                                "preserved (CK remembers the lifetime read).",
                    })
                except Exception as e:
                    return jsonify({
                        "ok": False,
                        "error": f"{type(e).__name__}:{e}",
                    }), 500

            return 5

        return 3

    n_routes = _register_brain_routes()

    status: Dict[str, Any] = {
        "mounted": True,
        "tensor_path": str(tensor_path),
        "tensor_norm_at_load": round(corrector._tensor_norm_at_load, 4),
        "fusion_weight": fusion_weight,
        "log_dir": str(corr_log.log_dir),
        "n_updates_on_tensor": int(corrector.tensor.n_updates),
        "tensor_decay": corrector.tensor.decay,
        "routes_registered": n_routes,
        "security_channel": "mounted" if security is not None else
                            f"unavailable ({_security_init_error})",
        "security_window": getattr(security, "window", None) if security else None,
    }
    return status
