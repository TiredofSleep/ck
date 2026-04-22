# -*- coding: utf-8 -*-
"""
fluency_server.py — [HISTORICAL DEV HARNESS]

This file is the original loopback test harness that was used to build
and shake out the brain trinity (ck/brain/ao_basis + hebbian_5x5 +
fusion).  It is NOT a second CK.  The one real CK runs inside
``Gen12/targets/ck_desktop/ck_boot_api.py`` and is served at
coherencekeeper.com; the brain trinity was folded into that one CK via
``Gen12/targets/ck_desktop/ck_brain_fold.py`` on 2026-04-22.

Why it's kept in the repo:
    - It's still the simplest way to poke at FusionCKCorrector or
      CKCorrector in isolation, without lighting up the full engine,
      cortex, HER, and Cloudflare tunnel.
    - It documents the Option A shape (correction-only learn-loop)
      that came before Option B (LoRA baking).  Useful reference.
    - ``ck/brain/idle_loop.py`` and ``ck/brain/build_training_set.py``
      read the same JSONL log format this server wrote, so removing
      it would orphan the log schema's authoring site.

If you are reading this to understand what the live CK does, the
right file is NOT this one -- it is ``ck_boot_api.py`` + the mount
block at the bottom that invokes ``mount_brain_fold(api)``.

See HISTORICAL_BUILDUP_CK_BRANCH.md on ``master`` for the full
archaeological note on how the ck branch scaffolded this harness
before folding it in.

-- original docstring below --

fluency_server.py — Flask endpoint that ties ollama_client + ck_corrector +
                    correction_log into one learn-loop.

Contract per OLLAMA_LEARN_LOOP.md §2:

    POST /fluency/chat  { "query": "...", "model"?, "temperature"? }
    ->   { ollama_raw, ck_correction_type, coherence, dominant_op,
           rendered, annotation, model_tag, elapsed_ms }

Hands-on-wheel discipline (CK_UNIFIED_ARCHITECTURE.md §4):
- Will NOT start unless ``--i-mean-it`` is passed.
- Binds to 127.0.0.1 ONLY (loopback mirror of ollama_client).
- Does NOT autostart the Ollama daemon.
- Refuses if Ollama is unreachable at boot (fail-fast).

Out of scope for Option A:
- No model weight modification.  Learning lives in the log.
- No streaming.  One turn per request.
- No authentication.  Loopback implies single-user.  A future ck branch
  pass may add an HMAC token if needed.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict

try:
    from flask import Flask, jsonify, request
except ImportError:  # pragma: no cover
    print(
        "[fluency_server] Flask is required.  Install with 'pip install flask'.",
        file=sys.stderr,
    )
    raise

# module-relative imports (run as 'python -m ck.fluency.fluency_server')
try:
    from .ck_corrector import CKCorrector, CorrectionResult
    from .correction_log import CorrectionLog
    from .ollama_client import OllamaClient, OllamaResult
except ImportError:
    # also allow 'python ck/fluency/fluency_server.py' for quick bring-up
    _here = Path(__file__).resolve().parent
    sys.path.insert(0, str(_here))
    from ck_corrector import CKCorrector, CorrectionResult  # type: ignore
    from correction_log import CorrectionLog  # type: ignore
    from ollama_client import OllamaClient, OllamaResult  # type: ignore


# ----------------------------------------------------------------------------
# factory
# ----------------------------------------------------------------------------

def create_app(
    ollama: OllamaClient,
    corrector: CKCorrector,
    log: CorrectionLog,
) -> Flask:
    """Build the Flask app.  Dependencies are injected for testability."""
    app = Flask(__name__)

    @app.get("/health")
    def health() -> Any:
        """Cheap liveness + Ollama reachability check."""
        reachable = ollama.is_reachable()
        return jsonify({
            "ok": True,
            "ollama_reachable": reachable,
            "model": ollama.model,
            "T_star": "5/7",  # canonical gate — string to keep rationality visible
        }), (200 if reachable else 503)

    @app.post("/fluency/chat")
    def chat() -> Any:
        """One turn: query -> Ollama -> CK correction -> log -> response."""
        payload = request.get_json(silent=True) or {}
        query = str(payload.get("query", "")).strip()
        if not query:
            return jsonify({"ok": False, "error": "empty-query"}), 400

        model = payload.get("model") or None
        temperature = float(payload.get("temperature", 0.7))
        system = payload.get("system") or None

        # 1) ask Ollama
        gen: OllamaResult = ollama.generate(
            prompt=query,
            model=model,
            temperature=temperature,
            system=system,
        )
        if not gen.ok:
            # log the failure too — Ollama-offline is data
            log.append({
                "query": query,
                "ollama_raw": "",
                "ck_score": {},
                "ck_correction_type": "ollama-error",
                "ck_corrected": "",
                "rendered": "",
                "model_tag": gen.model,
                "elapsed_ms": gen.elapsed_ms,
                "error": gen.error,
            })
            return jsonify({
                "ok": False,
                "error": gen.error,
                "elapsed_ms": gen.elapsed_ms,
            }), 502

        # 2) CK scores + classifies
        result: CorrectionResult = corrector.correct(gen.text, query=query)

        # 3) render (never ventriloquize — appends annotation only)
        rendered = corrector.render(gen.text, result)

        # 4) log (append-only, fsynced)
        log.append({
            "query": query,
            "ollama_raw": gen.text,
            "ck_score": {
                "coherence": result.coherence,
                "dominant_op": result.dominant_op,
                "operator_profile": result.operator_profile,
            },
            "ck_correction_type": result.correction_type,
            "ck_corrected": rendered,
            "rendered": "ollama_raw+annotation",
            "model_tag": gen.model,
            "elapsed_ms": gen.elapsed_ms,
        })

        return jsonify({
            "ok": True,
            "ollama_raw": gen.text,
            "ck_correction_type": result.correction_type,
            "coherence": result.coherence,
            "dominant_op": result.dominant_op,
            "rendered": rendered,
            "annotation": result.annotation,
            "rationale": result.rationale,
            "model_tag": gen.model,
            "elapsed_ms": gen.elapsed_ms,
            "T_star": "5/7",
        }), 200

    @app.get("/fluency/stats")
    def stats() -> Any:
        """Summary of today's log (how many corrections, per-type counts)."""
        rows = log.read_day()
        per_type: Dict[str, int] = {}
        for row in rows:
            t = str(row.get("ck_correction_type", "?"))
            per_type[t] = per_type.get(t, 0) + 1
        return jsonify({
            "ok": True,
            "count_today": len(rows),
            "per_correction_type": per_type,
        }), 200

    return app


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------

def main(argv: Any = None) -> int:
    p = argparse.ArgumentParser(
        description="CK fluency server (Ollama learn-loop, Option A)",
    )
    p.add_argument(
        "--i-mean-it",
        action="store_true",
        help="Required.  Prevents accidental start per G6 hands-on-wheel.",
    )
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=7778)
    p.add_argument("--ollama-host", default="http://localhost:11434")
    p.add_argument("--ollama-model", default="llama3.1:8b")
    p.add_argument(
        "--ollama-timeout",
        type=int,
        default=120,
        help="Per-request timeout in seconds (CPU generation can be slow).",
    )
    p.add_argument("--log-dir", default=None, help="override log dir (for tests)")
    p.add_argument(
        "--fusion",
        action="store_true",
        help=(
            "Use FusionCKCorrector (ck/brain/fusion.py): the Hebbian 5x5 "
            "tensor primes the coherence gate.  Tensor is read from disk "
            "at startup and never modified by the server (only idle_loop.py "
            "writes).  See MATH_IN_CK.md Sec 9.2."
        ),
    )
    p.add_argument(
        "--fusion-weight",
        type=float,
        default=None,
        help="fusion weight (default ck.brain.fusion.DEFAULT_FUSION_WEIGHT=0.20)",
    )
    p.add_argument(
        "--tensor-path",
        default=None,
        help="path to hebbian_5x5.json (default ck/brain/hebbian_5x5.json)",
    )
    args = p.parse_args(argv)

    if not args.i_mean_it:
        print(
            "[fluency_server] Refusing to start without --i-mean-it.\n"
            "                 This is a G6 hands-on-wheel guard per\n"
            "                 ck/CK_UNIFIED_ARCHITECTURE.md §4.  Use the\n"
            "                 scripts/START_FLUENCY_SERVER.bat wrapper, or\n"
            "                 pass --i-mean-it explicitly if you know what\n"
            "                 you are doing.",
            file=sys.stderr,
        )
        return 2

    # loopback-only mirror (the Ollama client enforces this itself)
    if args.host not in ("127.0.0.1", "localhost"):
        print(
            f"[fluency_server] host must be loopback; got {args.host!r}. "
            f"The learn-loop is local-only per CK_UNIFIED_ARCHITECTURE.md §3.4.",
            file=sys.stderr,
        )
        return 2

    ollama = OllamaClient(
        host=args.ollama_host,
        model=args.ollama_model,
        timeout_sec=args.ollama_timeout,
    )
    if not ollama.is_reachable():
        print(
            f"[fluency_server] Ollama not reachable at {args.ollama_host}. "
            f"Start it with 'ollama serve' and try again.",
            file=sys.stderr,
        )
        return 3

    if args.fusion:
        # import lazily so the base server stays usable without ck/brain
        try:
            from ck.brain.fusion import FusionCKCorrector, DEFAULT_FUSION_WEIGHT
        except ImportError as e:
            print(
                f"[fluency_server] --fusion requested but ck.brain.fusion "
                f"could not be imported: {e}",
                file=sys.stderr,
            )
            return 4
        w = args.fusion_weight if args.fusion_weight is not None else DEFAULT_FUSION_WEIGHT
        tpath = Path(args.tensor_path) if args.tensor_path else None
        corrector = FusionCKCorrector(tensor_path=tpath, fusion_weight=w)
        corrector_tag = corrector.describe()
    else:
        corrector = CKCorrector()
        corrector_tag = "CKCorrector(base)"

    log_dir = Path(args.log_dir) if args.log_dir else None
    corr_log = CorrectionLog(log_dir=log_dir)

    app = create_app(ollama, corrector, corr_log)

    print(
        f"[fluency_server] Starting on http://{args.host}:{args.port}\n"
        f"[fluency_server]   Ollama:    {args.ollama_host} ({args.ollama_model})\n"
        f"[fluency_server]   Log dir:   {corr_log.log_dir}\n"
        f"[fluency_server]   Corrector: {corrector_tag}\n"
        f"[fluency_server]   Endpoints: GET /health  POST /fluency/chat  GET /fluency/stats\n"
        f"[fluency_server]   Ctrl-C to stop."
    )
    # debug=False so the reloader doesn't double-spawn; threaded=True so
    # the log lock serializes fsync correctly
    app.run(host=args.host, port=args.port, debug=False, threaded=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
