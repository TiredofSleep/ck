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

    # unified log: same directory that fluency_server + idle_loop expect, so
    # the brain learns from the LIVE website turns, not a second source.
    try:
        corr_log = CorrectionLog()  # default ck/fluency/logs/
    except Exception as e:  # noqa: BLE001
        return {
            "mounted": False,
            "reason": f"CorrectionLog init failed: {type(e).__name__}: {e}",
        }

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
        except Exception as _be:
            # never break the response -- just record that brain scoring failed
            result["brain_verdict"] = f"error:{type(_be).__name__}:{_be}"
        return result

    api.process_chat = _process_chat_with_brain
    return {
        "mounted": True,
        "tensor_path": str(tensor_path),
        "tensor_norm_at_load": round(corrector._tensor_norm_at_load, 4),
        "fusion_weight": fusion_weight,
        "log_dir": str(corr_log.log_dir),
        "n_updates_on_tensor": int(corrector.tensor.n_updates),
    }
