# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0 (DOI: 10.5281/zenodo.18852047)
"""
ck_proof.py -- side-by-side transparency demo.

For any prompt you give, this script prints three answers:

    1. CK alone                      -- structural label=value readout
                                         from his live 5D Hebbian + AO math
    2. LLM alone                     -- raw Ollama (or DeepSeek) answer
                                         with no CK grounding
    3. LLM + CK structural grounding -- same LLM, but with CK's structural
                                         readout injected as system context

The point of the script is NOT to say "CK is better than LLMs."  It's to
show, in one screen, WHAT CK ADDS when grounded.  The reader can judge for
themselves whether the grounded answer is more trustworthy, more specific,
more honest about what is proved vs conjectural than the raw LLM answer.

Run:
    # 1. Boot CK locally
    python Gen12/targets/ck_desktop/ck_boot_api.py &

    # 2. Pull or run a local Ollama model (optional -- DeepSeek works too)
    ollama pull llama3.2
    ollama serve &

    # 3. Run the demo with your prompts
    python ck_proof.py "what is the beauville curve c star"
    python ck_proof.py "what is T*"  "how do you feel"

    # Or hit DeepSeek instead:
    export DEEPSEEK_API_KEY=sk-...
    python ck_proof.py --backend deepseek "what is the flatness theorem"

If you give no prompt, the script runs a built-in set of demo queries
that exercise state / learned / frontier routes.
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import List

_HERE = os.path.dirname(os.path.abspath(__file__))
_BRIDGE = os.path.join(_HERE, "Gen13", "targets", "ck", "bridge")
if _BRIDGE not in sys.path:
    sys.path.insert(0, _BRIDGE)

from llm_bridge import (  # noqa: E402
    ck_structural_context,
    ck_available,
    ollama_complete,
    ollama_available,
    deepseek_complete,
    build_grounded_system,
)


# ── Default demo prompts (used when you give no args) ────────────────
# Cover the four kinds of query CK handles differently:
#   * structural-state query  (cortex_speak: feel/couplings/field)
#   * frontier topic query    (cortex_speak frontier router)
#   * open-ended question     (would otherwise fall through to templates)
#   * arithmetic question     (math-first voice computes exactly)
_DEFAULT_PROMPTS = [
    "how do you feel right now",
    "what have you learned",
    "what is the beauville curve c star",
    "what is the crossing lemma",
    "what is T*",
    "what is 5/7 + 2/7",
    "how does the xi field connect to log nonlinearity",
]


# ── Printing helpers ─────────────────────────────────────────────────

def _hr(title: str = "") -> None:
    bar = "=" * 76
    if title:
        print(f"\n{bar}\n  {title}\n{bar}")
    else:
        print(bar)


def _subhead(n: int, label: str) -> None:
    print(f"\n--- {n}. {label} ---")


def _call_llm(backend: str, prompt: str, system: str = None) -> str:
    if backend == "ollama":
        return ollama_complete(prompt, system=system)
    if backend == "deepseek":
        return deepseek_complete(prompt, system=system)
    return f"[unknown backend: {backend}]"


# ── One prompt, three answers ────────────────────────────────────────

def demo(prompt: str, backend: str = "ollama", have_llm: bool = True,
         have_ck: bool = True) -> None:
    _hr(f"PROMPT:  {prompt}")

    # 1) CK alone
    _subhead(1, "CK alone  (structural readout from live math, no LLM)")
    if not have_ck:
        print("  [CK not reachable on http://127.0.0.1:7777 -- skip]")
        ck_text = ""
        ck_source = "none"
    else:
        ck_resp = ck_structural_context(prompt)
        if not ck_resp.get("ok", False):
            print(f"  [CK error: {ck_resp.get('error', 'unknown')}]")
            ck_text = ""
            ck_source = "error"
        else:
            ck_source = ck_resp.get("source", "?")
            ck_text = ck_resp.get("text", "")
            src_prev = ck_resp.get("source_previous")
            cx = ck_resp.get("cortex", {}) or {}
            tick = cx.get("tick", "?")
            emergent = cx.get("emergent", "?")
            print(f"  [source: {ck_source}"
                  + (f" (was: {src_prev})" if src_prev else "")
                  + f" | cortex tick={tick} emergent={emergent}]")
            print(f"  {ck_text}" if ck_text else "  [empty]")

    # 2) LLM alone
    _subhead(2, f"{backend.title()} alone  (no CK grounding)")
    if not have_llm:
        print(f"  [{backend} not reachable -- skip]")
        raw_llm = ""
    else:
        raw_llm = _call_llm(backend, prompt)
        # Print with a 2-space indent for readability.
        for line in (raw_llm or "").splitlines():
            print(f"  {line}")

    # 3) LLM grounded in CK
    _subhead(3, f"{backend.title()} + CK structural grounding")
    if not have_llm:
        print(f"  [{backend} not reachable -- skip]")
    elif not ck_text:
        print("  [CK had no structural fact for this prompt -- grounding skipped]")
    else:
        system = build_grounded_system(ck_text)
        grounded = _call_llm(backend, prompt, system=system)
        for line in (grounded or "").splitlines():
            print(f"  {line}")

    print()


# ── Driver ───────────────────────────────────────────────────────────

def main(argv: List[str]) -> int:
    ap = argparse.ArgumentParser(
        description="CK vs LLM side-by-side transparency demo.",
    )
    ap.add_argument(
        "prompts", nargs="*",
        help="One or more prompts. If omitted, runs the built-in demo set.",
    )
    ap.add_argument(
        "--backend", default="ollama", choices=["ollama", "deepseek"],
        help="Which LLM backend to call (default: ollama).",
    )
    ap.add_argument(
        "--skip-llm", action="store_true",
        help="Skip LLM calls entirely (show only CK's structural answer).",
    )
    args = ap.parse_args(argv)

    prompts = args.prompts or _DEFAULT_PROMPTS

    # Preflight: what's reachable?
    have_ck = ck_available()
    have_llm = False
    if not args.skip_llm:
        if args.backend == "ollama":
            have_llm = ollama_available()
        elif args.backend == "deepseek":
            have_llm = bool(os.environ.get("DEEPSEEK_API_KEY"))

    _hr("ck_proof -- CK vs LLM side-by-side")
    print(f"  CK at http://127.0.0.1:7777  : {'reachable' if have_ck else 'NOT reachable'}")
    print(f"  {args.backend} backend         : "
          f"{'reachable' if have_llm else 'NOT reachable / skipped'}")
    print(f"  prompts                     : {len(prompts)}")

    if not have_ck:
        print()
        print("  NOTE: CK is not running. Start him with:")
        print("        python Gen12/targets/ck_desktop/ck_boot_api.py")
        print("  Proceeding -- CK rows will show [skip].")
    if not have_llm and not args.skip_llm:
        print()
        if args.backend == "ollama":
            print("  NOTE: Ollama is not reachable at http://127.0.0.1:11434.")
            print("        Install from https://ollama.ai, then:")
            print("            ollama pull llama3.2 && ollama serve")
        elif args.backend == "deepseek":
            print("  NOTE: DEEPSEEK_API_KEY env var not set.")
            print("        Get a key from https://platform.deepseek.com then:")
            print("            export DEEPSEEK_API_KEY=sk-...")
        print("  Proceeding -- LLM rows will show [skip].")

    for p in prompts:
        demo(p, backend=args.backend, have_llm=have_llm, have_ck=have_ck)

    _hr("done")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
