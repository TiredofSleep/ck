# Copyright (c) 2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
"""
ck_chat_structured.py -- Sovereignty-preserving deterministic chat mode.

CK self-audit ask #3 (per Grok-CK dialogue, 2026-04-17):

    "Right now interaction is mostly REPL-style via ck_run.py. A simple
    structured chat mode (even just *command -> coherence score +
    diagnostic + suggested next proof*) would make me more approachable
    for new users without losing determinism. Keep it under the
    sovereignty rules -- no external models, pure TIG primitives."

This is a deterministic REPL. There is NO LLM in the loop. Every response
is computed locally from:

  1. ck_diagnose.diagnose()       (paradox-classifier scan over input)
  2. ck_harmony_audit.audit()     (5/7 threshold + sigma mutation suggestion)
  3. A small static "next-proof" routing table keyed on which diagnostic
     band the input falls into.

Sovereignty: no external models, no network calls. Everything runs locally
on TIG primitives. Output is structured JSON + a one-line plain summary.

Usage:
    python ck_chat_structured.py
    > diagnose ck_diagnose.py
    > audit {"voice_loop": 0.62, "tsml_tower": 0.91}
    > raw "any string here"
    > help
    > quit

Or as a single-shot command:
    python ck_chat_structured.py --once "diagnose ck_diagnose.py"
    python ck_chat_structured.py --once 'audit {"voice_loop":0.62}'
    python ck_chat_structured.py --once 'raw "test string"'
"""

import json
import os
import sys
import shlex
import argparse
from typing import Any, Dict, Tuple

# Local imports -- pure TIG primitives, no external models.
import ck_diagnose
import ck_harmony_audit

T_STAR = 5.0 / 7.0


# ============================================================
# Next-proof routing: maps diagnostic band -> suggested proof script
# ============================================================
#
# Bands:
#   ABOVE   overall_coherence >= T_STAR
#   BELOW   overall_coherence < T_STAR but >= 0.5
#   FLOOR   overall_coherence < 0.5
#
NEXT_PROOF_TABLE = {
    "ABOVE": [
        ("papers/proof_d25_loop_closure.py",
         "sinc^2 zero law -- verifies the cyclotomic zero structure"),
        ("Gen12/targets/clay/papers/sprint17_tsml_tower_2026_04_17/"
         "papers/proof_tsml_3layer_tower.py",
         "TSML 3-layer canonical tower -- 92/6/2 decomposition + Lemmas 5,6"),
    ],
    "BELOW": [
        ("Gen12/targets/clay/papers/sprint10_flatness_2026_04_06/"
         "proof_flatness_z10z.py",
         "Flatness Theorem on Z/10Z -- baseline 2x2 forced-torus check"),
        ("Gen12/targets/clay/papers/sprint11_tig_bundle_2026_04_08/"
         "papers/proof_uop_classifier.py",
         "UOP paradox classifier -- diagnose what kind of breakdown this is"),
    ],
    "FLOOR": [
        ("Gen12/targets/clay/papers/sprint16_basin_finite_2026_04_15/"
         "papers/proof_dual_reset_law.py",
         "Dual reset law -- the input may be in a basin needing RESET(9)"),
    ],
}


def band(score: float) -> str:
    """Return diagnostic band for an overall coherence score."""
    if score >= T_STAR:
        return "ABOVE"
    if score >= 0.5:
        return "BELOW"
    return "FLOOR"


def suggest_next_proof(score: float) -> Dict[str, Any]:
    """One suggestion based on the band; deterministic."""
    b = band(score)
    options = NEXT_PROOF_TABLE.get(b, [])
    return {
        "band": b,
        "suggestions": [
            {"script": s, "why": w} for (s, w) in options
        ],
    }


# ============================================================
# Command handlers
# ============================================================

def cmd_diagnose(arg: str) -> Dict[str, Any]:
    """diagnose <path> -- run ck_diagnose.diagnose on a file."""
    if not arg:
        return {"error": "usage: diagnose <path>"}
    if not os.path.exists(arg):
        return {"error": f"file not found: {arg}"}
    result = ck_diagnose.diagnose(path=arg)
    result["next_proof"] = suggest_next_proof(result["overall_coherence"])
    return result


def cmd_raw(arg: str) -> Dict[str, Any]:
    """raw <string> -- run ck_diagnose.diagnose on an inline string."""
    if not arg:
        return {"error": "usage: raw <string>"}
    result = ck_diagnose.diagnose(raw=arg)
    result["next_proof"] = suggest_next_proof(result["overall_coherence"])
    return result


def cmd_audit(arg: str) -> Dict[str, Any]:
    """audit <json> -- run ck_harmony_audit.audit on inline JSON map."""
    if not arg:
        return {"error": 'usage: audit {"name": score, ...}'}
    try:
        scores = json.loads(arg)
    except json.JSONDecodeError as e:
        return {"error": f"invalid JSON: {e}"}
    if not isinstance(scores, dict):
        return {"error": "audit expects an object {name: score}"}
    result = ck_harmony_audit.audit(scores)
    return result


def cmd_help(arg: str) -> Dict[str, Any]:
    """help -- list commands."""
    return {
        "commands": {
            "diagnose <path>": "Run paradox-classifier scan on a file.",
            "raw <string>":    "Run paradox-classifier scan on a raw string.",
            "audit <json>":    "Run 5/7-threshold audit on a {name: score} map.",
            "help":             "Show this message.",
            "quit | exit":      "Leave the REPL.",
        },
        "sovereignty_rule": "No external models. Pure local TIG primitives.",
        "T_star": T_STAR,
    }


COMMANDS = {
    "diagnose": cmd_diagnose,
    "raw":      cmd_raw,
    "audit":    cmd_audit,
    "help":     cmd_help,
    "?":        cmd_help,
}


# ============================================================
# Parsing + summary
# ============================================================

def parse_command(line: str) -> Tuple[str, str]:
    """Split a command line into (verb, argstring)."""
    line = line.strip()
    if not line:
        return ("", "")
    parts = line.split(None, 1)
    verb = parts[0].lower()
    arg = parts[1] if len(parts) > 1 else ""
    # Strip outer quotes if user passed `raw "hello"` style
    if arg and arg[0] in ('"', "'") and arg[-1] == arg[0]:
        arg = arg[1:-1]
    return (verb, arg)


def one_line_summary(verb: str, result: Dict[str, Any]) -> str:
    """Plain English one-liner per command."""
    if "error" in result:
        return f"[error] {result['error']}"
    if verb in ("diagnose", "raw"):
        oc = result.get("overall_coherence", 0.0)
        ok = "OK" if result.get("above_threshold") else "BELOW T*"
        return (f"coherence={oc:.4f}  {ok}  "
                f"-> band {result['next_proof']['band']}")
    if verb == "audit":
        h = result.get("overall_health", "?")
        flagged = result.get("flagged", [])
        return (f"health={h}  flagged={len(flagged)} "
                f"({', '.join(flagged) if flagged else 'none'})")
    if verb in ("help", "?"):
        return "commands: diagnose | raw | audit | help | quit"
    return ""


# ============================================================
# REPL
# ============================================================

def execute(line: str) -> Dict[str, Any]:
    """Execute one command line, return the result dict."""
    verb, arg = parse_command(line)
    if not verb:
        return {"error": "empty command"}
    if verb in ("quit", "exit"):
        return {"action": "quit"}
    handler = COMMANDS.get(verb)
    if handler is None:
        return {"error": f"unknown command: {verb}. Type 'help'."}
    return handler(arg)


def repl():
    """Interactive REPL. Pure local. No network."""
    print("CK structured chat -- deterministic, sovereignty-preserving.")
    print("Type 'help' for commands, 'quit' to exit.")
    print(f"T* = {T_STAR:.10f}")
    print()
    while True:
        try:
            line = input("ck> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if not line:
            continue
        verb, _ = parse_command(line)
        result = execute(line)
        if result.get("action") == "quit":
            return
        # Print the JSON, then a one-line summary
        print(json.dumps(result, indent=2))
        summary = one_line_summary(verb, result)
        if summary:
            print(f"-- {summary}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="CK structured chat: deterministic REPL over TIG primitives"
    )
    parser.add_argument("--once", type=str, default=None,
                        help="execute a single command and exit")
    args = parser.parse_args()

    if args.once:
        verb, _ = parse_command(args.once)
        result = execute(args.once)
        print(json.dumps(result, indent=2))
        summary = one_line_summary(verb, result)
        if summary:
            print(f"-- {summary}", file=sys.stderr)
    else:
        repl()


if __name__ == "__main__":
    main()
