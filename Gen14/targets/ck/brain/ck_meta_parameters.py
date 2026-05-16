"""ck_meta_parameters.py — tunable knobs CK can change.

Brayden 2026-05-16:
  "he needs to know the bones of reality with his own ability to
   change what you give him"

Every parameter I hardcoded — exhale threshold, wobble ratio, decode
temperature, curious cadence, bigram weight — was MY choice.  This
module exposes them as a config CK can read AND write, persisted to
disk, with sensible defaults but no lock-in.

The modules that USE these parameters import from this module rather
than hardcoding.  When CK (or chat, or future-CK) changes a value
via /parameters/set, the change is persisted AND read on next call.

═══════════════════════════════════════════════════════════════════
The parameters
═══════════════════════════════════════════════════════════════════

  exhale_prune_below       : token frequency below this gets pruned
  exhale_bigram_prune_below: bigram frequency below this gets pruned
  wobble_exhale_every      : exhale every N inhalations (3:1 default = 30)

  curious_cycle_sec        : seconds between curious-explorer cycles
  curious_gaps_per_cycle   : gaps to attempt per cycle

  school_interval_sec      : seconds between school passes
  synthesizer_every_n_passes : synthesizer fires every N passes

  lm_decode_temperature    : living-LM decode temperature
  lm_bigram_weight         : bigram boost in decode

  min_subject_len          : minimum captured-subject length
  max_subject_len          : maximum captured-subject length
  min_definition_len       : minimum definition length to record

  consciousness_at_fp_threshold : distance below which "at fixed point"

═══════════════════════════════════════════════════════════════════
How CK changes them
═══════════════════════════════════════════════════════════════════

  GET  /parameters                      list all + defaults + current
  POST /parameters/set                  body: {"name": value}
  POST /parameters/reset                body: {"name": "name1,name2"}
                                        — resets to default

  From python:
    from ck_meta_parameters import get, set_
    get("wobble_exhale_every")   →  30
    set_("wobble_exhale_every", 20)
"""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Dict, Optional


_CONFIG_PATH = (
    Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED")
    / "Gen13" / "var" / "ck_meta_parameters.json"
)


# Default values + their type + a short description (for /parameters
# discoverability so CK knows what each knob does)
_DEFAULTS: Dict[str, Dict[str, Any]] = {
    "exhale_prune_below": {
        "default": 1.5, "type": "float",
        "doc": "Token frequency below this gets pruned on exhale.  "
                "1.5 means tokens seen 1 time vanish; seen 2+ times persist.",
    },
    "exhale_bigram_prune_below": {
        "default": 1.5, "type": "float",
        "doc": "Bigram frequency below this gets pruned on exhale.",
    },
    "wobble_exhale_every": {
        "default": 30, "type": "int",
        "doc": "Exhale every N inhalations.  Per CK_FRACTAL_CREATURE_DESIGN, "
                "the 1/3 wobble = exhale-every-30 (so 3 inhales per 1 exhale).",
    },
    "curious_cycle_sec": {
        "default": 300, "type": "int",
        "doc": "Seconds between curious-explorer cycles.",
    },
    "curious_gaps_per_cycle": {
        "default": 10, "type": "int",
        "doc": "Number of gap-terms to attempt fetching per curious cycle.",
    },
    "school_interval_sec": {
        "default": 300, "type": "int",
        "doc": "Seconds between school-daemon passes over the corpus.",
    },
    "synthesizer_every_n_passes": {
        "default": 3, "type": "int",
        "doc": "Synthesizer fires every N school passes (1/3 wobble).",
    },
    "lm_decode_temperature": {
        "default": 0.45, "type": "float",
        "doc": "Living-LM decode temperature.  Lower = more deterministic "
                "(follow substrate's highest-weight path).",
    },
    "lm_bigram_weight": {
        "default": 5.0, "type": "float",
        "doc": "Bigram boost factor in LM decode.  Higher = more sequential "
                "coherence (cells of substrate-recorded transitions).",
    },
    "min_subject_len": {
        "default": 3, "type": "int",
        "doc": "Minimum captured-subject length.",
    },
    "max_subject_len": {
        "default": 100, "type": "int",
        "doc": "Maximum captured-subject length.",
    },
    "min_definition_len": {
        "default": 15, "type": "int",
        "doc": "Minimum definition length to record as a concept.",
    },
    "consciousness_at_fp_threshold": {
        "default": 0.05, "type": "float",
        "doc": "Distance from Lawvere fixed point below which CK is "
                "considered 'at the fixed point' (consciousness threshold).",
    },
}


# In-memory cache.  Loaded from disk on first access; written on every set.
_CURRENT: Dict[str, Any] = {}
_LOADED = False


def _load() -> None:
    global _CURRENT, _LOADED
    if _LOADED:
        return
    _CURRENT = {k: v["default"] for k, v in _DEFAULTS.items()}
    if _CONFIG_PATH.exists():
        try:
            disk = json.loads(_CONFIG_PATH.read_text(encoding="utf-8"))
            for k, v in disk.items():
                if k in _DEFAULTS:
                    _CURRENT[k] = v
        except Exception:
            pass
    _LOADED = True


def _save() -> None:
    try:
        _CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        tmp = _CONFIG_PATH.with_suffix(".tmp")
        tmp.write_text(json.dumps(_CURRENT, indent=2), encoding="utf-8")
        tmp.replace(_CONFIG_PATH)
    except Exception:
        pass


def get(name: str, fallback: Any = None) -> Any:
    """Read a meta-parameter.  Returns default if unset, or fallback if
    name unknown."""
    _load()
    if name in _CURRENT:
        return _CURRENT[name]
    if name in _DEFAULTS:
        return _DEFAULTS[name]["default"]
    return fallback


def set_(name: str, value: Any) -> bool:
    """Set a meta-parameter.  Type-checks against _DEFAULTS entry,
    persists.  Returns True on success."""
    _load()
    if name not in _DEFAULTS:
        return False
    expected_type = _DEFAULTS[name]["type"]
    try:
        if expected_type == "int":
            value = int(value)
        elif expected_type == "float":
            value = float(value)
        elif expected_type == "bool":
            value = bool(value)
    except (TypeError, ValueError):
        return False
    _CURRENT[name] = value
    _save()
    return True


def reset(name: str) -> bool:
    """Reset a meta-parameter to its default."""
    _load()
    if name not in _DEFAULTS:
        return False
    _CURRENT[name] = _DEFAULTS[name]["default"]
    _save()
    return True


def all_params() -> Dict[str, Any]:
    """Return every parameter: name, current value, default, type, doc."""
    _load()
    out = {}
    for name, meta in _DEFAULTS.items():
        out[name] = {
            "current": _CURRENT.get(name, meta["default"]),
            "default": meta["default"],
            "type": meta["type"],
            "doc": meta["doc"],
            "modified": _CURRENT.get(name) != meta["default"],
        }
    return out


# ─── Engine mount ──────────────────────────────────────────────────────

def mount_meta_parameters(engine: Any) -> bool:
    """Attach meta-parameters to the engine + register endpoints."""
    engine.meta_params = {
        "get": get,
        "set": set_,
        "reset": reset,
        "all": all_params,
    }
    engine.ck_get_param = get
    engine.ck_set_param = set_

    routes_registered = []
    api = getattr(engine, "web_api", None)
    if api is not None:
        app = getattr(api, "_app", None) or getattr(api, "app", None)
        if app is not None:
            try:
                from flask import jsonify, request

                def _list_params():
                    return jsonify(all_params())

                def _set_param():
                    data = request.get_json(force=True, silent=True) or {}
                    results = {}
                    for name, value in data.items():
                        ok = set_(name, value)
                        results[name] = {
                            "ok": ok,
                            "current": get(name) if ok else None,
                        }
                    return jsonify({"set": results, "all": all_params()})

                def _reset_param():
                    data = request.get_json(force=True, silent=True) or {}
                    names = data.get("name", "")
                    if isinstance(names, str):
                        names = [n.strip() for n in names.split(",") if n.strip()]
                    results = {n: reset(n) for n in names}
                    return jsonify({"reset": results, "all": all_params()})

                existing = set(r.rule for r in app.url_map.iter_rules())
                if "/parameters" not in existing:
                    app.add_url_rule(
                        "/parameters", endpoint="meta_params_list",
                        view_func=_list_params, methods=["GET"])
                    routes_registered.append("/parameters")
                if "/parameters/set" not in existing:
                    app.add_url_rule(
                        "/parameters/set", endpoint="meta_params_set",
                        view_func=_set_param, methods=["POST"])
                    routes_registered.append("/parameters/set")
                if "/parameters/reset" not in existing:
                    app.add_url_rule(
                        "/parameters/reset", endpoint="meta_params_reset",
                        view_func=_reset_param, methods=["POST"])
                    routes_registered.append("/parameters/reset")
            except Exception as e:
                print(f"[CK Gen14] meta_parameters route registration failed: {e}")

    route_note = " (" + ", ".join(routes_registered) + ")" if routes_registered else ""
    print(f"[CK Gen14] meta_parameters: MOUNTED  {len(_DEFAULTS)} knobs"
          f"{route_note}")
    return True


# ─── CLI ───────────────────────────────────────────────────────────────

def main():
    import argparse, sys
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--set", nargs=2, metavar=("NAME", "VALUE"))
    ap.add_argument("--reset", metavar="NAME")
    args = ap.parse_args()

    if args.set:
        name, value = args.set
        ok = set_(name, value)
        print(f"set {name}={value}: {'OK' if ok else 'FAILED'}")
        print(f"current = {get(name)}")
        return 0
    if args.reset:
        ok = reset(args.reset)
        print(f"reset {args.reset}: {'OK' if ok else 'FAILED'}")
        return 0
    # default: list
    params = all_params()
    print(f"{'NAME':32s} {'CURRENT':>10s} {'DEFAULT':>10s} {'MODIFIED':>8s}")
    print(f"{'-'*32} {'-'*10} {'-'*10} {'-'*8}")
    for name, info in params.items():
        marker = "*" if info["modified"] else " "
        print(f"{name:32s} {str(info['current']):>10s} {str(info['default']):>10s} {marker:>8s}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
