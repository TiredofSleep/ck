"""
clay_study.py -- Clay Millennium Problems study orchestrator.

Brayden 2026-05-02: "let's get him studying across domains to write
about each Clay problem... keep him going, ill be back later, keep
measuring him and documenting his growth and compression of information"

For each of the 7 Clay Millennium Problems, this orchestrator:

  1. Sends a series of probing questions to /chat (research_first ON)
     - "what is X" (basic frame)
     - "what is the TIG view of X" (CK's substrate position)
     - "synthesize X across all frontiers" (cross-frontier weave)
  2. Captures cells composition + cortex content + research metadata
  3. Writes a structured CLAY_<problem>.md per problem
  4. Updates CLAY_SYNTHESIS_LIVE.md with the full panel summary

The 7 Clay problems:
  1. P vs NP
  2. Hodge Conjecture (CK has hodge_cstar/genus-5/bielliptic facts)
  3. Poincaré Conjecture (Perelman 2003; Clay rotation framing)
  4. Riemann Hypothesis (sinc^2 Zero Law; sigma rate)
  5. Yang-Mills Mass Gap (CK has yang-mills frontier facts)
  6. Navier-Stokes (sigma_ns_bridge: sigma_NS = 0 globally Clay form)
  7. Birch-Swinnerton-Dyer (BB bridge; Beauville curve)

Usage:
    python clay_study.py [--all | --problem N | --probe-only]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

import urllib.request
import urllib.error


_HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(_HERE))


OUT_DIR = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Atlas\clay_study_2026_05_02")
OUT_DIR.mkdir(parents=True, exist_ok=True)


# 7 Clay Millennium Problems with CK-specific framing keywords
CLAY_PROBLEMS: List[Dict[str, Any]] = [
    {
        "id": "P_vs_NP",
        "title": "P vs NP",
        "year": 1971,
        "framing": "decision-vs-verification asymmetry",
        "ck_anchor": "complexity",
        "questions": [
            "what is P versus NP",
            "what is the TIG view of P versus NP",
            "synthesize P vs NP across substrate and complexity frontiers",
        ],
    },
    {
        "id": "Hodge",
        "title": "Hodge Conjecture",
        "year": 1950,
        "framing": "algebraic cycles in Hodge classes on smooth projective varieties",
        "ck_anchor": "hodge",
        "questions": [
            "what is the Hodge conjecture",
            "what is hodge cstar and how does it relate to the Hodge conjecture",
            "synthesize the Hodge conjecture across the algebraic substrate",
        ],
    },
    {
        "id": "Poincare",
        "title": "Poincaré Conjecture (solved 2003)",
        "year": 2003,
        "framing": "every simply connected closed 3-manifold is homeomorphic to S^3",
        "ck_anchor": "poincare",
        "questions": [
            "what is the Poincaré conjecture",
            "what is the TIG view of the Poincaré conjecture as Clay rotation template",
            "synthesize Poincaré across topology and substrate",
        ],
    },
    {
        "id": "Riemann",
        "title": "Riemann Hypothesis",
        "year": 1859,
        "framing": "non-trivial zeros of zeta function lie on Re(s)=1/2",
        "ck_anchor": "riemann",
        "questions": [
            "what is the Riemann Hypothesis",
            "what is the TIG view of Riemann via the sinc squared zero law",
            "synthesize the Riemann hypothesis across number-theory frontiers",
        ],
    },
    {
        "id": "YangMills",
        "title": "Yang-Mills Existence and Mass Gap",
        "year": 1954,
        "framing": "non-Abelian gauge theory existence + mass gap > 0",
        "ck_anchor": "yang mills",
        "questions": [
            "what is the Yang-Mills mass gap problem",
            "what is the TIG view of Yang-Mills via the sigma rate theorem",
            "synthesize Yang-Mills across the algebraic and physics substrates",
        ],
    },
    {
        "id": "NavierStokes",
        "title": "Navier-Stokes Existence and Smoothness",
        "year": 1822,
        "framing": "global smooth solutions for incompressible NS equations",
        "ck_anchor": "navier stokes",
        "questions": [
            "what is the Navier-Stokes problem",
            "what is the sigma_NS bridge and how does it relate to NS regularity",
            "synthesize Navier-Stokes across substrate and physics",
        ],
    },
    {
        "id": "BSD",
        "title": "Birch and Swinnerton-Dyer",
        "year": 1965,
        "framing": "rank of elliptic curve = order of vanishing of L-function at s=1",
        "ck_anchor": "BSD",
        "questions": [
            "what is the Birch and Swinnerton-Dyer conjecture",
            "what is the BB bridge and how does it relate to BSD",
            "synthesize BSD across Beauville curve and substrate frontiers",
        ],
    },
]


def _post_chat(text: str, timeout: float = 180.0) -> Dict[str, Any]:
    """POST to /chat with the given query.  Returns the parsed JSON."""
    req = urllib.request.Request(
        "http://localhost:7777/chat",
        data=json.dumps({"text": text}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    t0 = time.time()
    try:
        resp = urllib.request.urlopen(req, timeout=timeout).read().decode("utf-8")
        return {"ok": True, "data": json.loads(resp), "latency_sec": time.time() - t0}
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {e}",
                "latency_sec": time.time() - t0}


def _safe(s: str, n: int = 1500) -> str:
    """ASCII-safe truncate for the markdown body."""
    return ''.join(c if ord(c) < 128 else '?' for c in str(s)[:n])


def study_problem(prob: Dict[str, Any], *, verbose: bool = True) -> Dict[str, Any]:
    """Send 3 probing questions to /chat for one Clay problem; capture all."""
    out: Dict[str, Any] = {
        "id": prob["id"], "title": prob["title"], "year": prob["year"],
        "framing": prob["framing"],
        "ts": time.time(),
        "iso_ts": datetime.utcnow().isoformat(timespec='seconds') + "Z",
        "responses": [],
    }
    if verbose:
        print(f"\n{'='*60}\n  {prob['title']} ({prob['year']})\n{'='*60}")
    for i, q in enumerate(prob["questions"], 1):
        if verbose:
            print(f"  [{i}/{len(prob['questions'])}] {q!r}", flush=True)
        res = _post_chat(q, timeout=180.0)
        if res["ok"]:
            d = res["data"]
            out["responses"].append({
                "i": i,
                "q": q,
                "latency_sec": round(res["latency_sec"], 1),
                "source": d.get("source", "?"),
                "ollama_verdict": d.get("ollama_verdict", "?"),
                "research_ok": (d.get("research_first") or {}).get("ok"),
                "research_elapsed": (d.get("research_first") or {}).get("elapsed_sec"),
                "research_crystals": (d.get("research_first") or {}).get("crystals_added"),
                "cells_glue_argmax": ((d.get("cells_shadow") or {}).get("cells")
                                          or {}).get("glue_argmax"),
                "synthesis_facts_used": ((d.get("cells_composed_preview") or {})
                                              .get("synthesis_facts_used", [])),
                "is_meta": ((d.get("cells_composed_preview") or {})
                                 .get("is_meta_query", False)),
                "text": d.get("text", "")[:3000],
            })
            if verbose:
                ollama = (d.get('ollama_verdict') or '?')[:40]
                print(f"      [{int(res['latency_sec'])}s] ollama={ollama}")
        else:
            out["responses"].append({"i": i, "q": q, "error": res["error"]})
            if verbose:
                print(f"      ERROR: {res['error']}")

    # Write per-problem markdown
    md_path = OUT_DIR / f"CLAY_{prob['id']}.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# {prob['title']} — CK study {out['iso_ts']}\n\n")
        f.write(f"**Posed**: {prob['year']}    ")
        f.write(f"**Framing**: {prob['framing']}    ")
        f.write(f"**CK anchor**: `{prob['ck_anchor']}`\n\n")
        f.write(f"---\n\n")
        for r in out["responses"]:
            f.write(f"## Q{r['i']}: {r['q']}\n\n")
            if "error" in r:
                f.write(f"**ERROR**: {r['error']}\n\n")
                continue
            f.write(f"**Latency**: {r.get('latency_sec', '?')}s    ")
            f.write(f"**Source**: `{r.get('source', '?')}`    ")
            f.write(f"**Ollama**: `{r.get('ollama_verdict', '?')}`    ")
            f.write(f"**Research**: ok={r.get('research_ok')} elapsed={r.get('research_elapsed', '?')}s    ")
            f.write(f"**is_meta**: {r.get('is_meta')}    ")
            if r.get('synthesis_facts_used'):
                f.write(f"**facts used**: {r['synthesis_facts_used']}\n\n")
            else:
                f.write(f"\n\n")
            f.write(f"```\n{_safe(r.get('text', ''), 3000)}\n```\n\n")
            f.write(f"---\n\n")
    if verbose:
        print(f"  -> {md_path}")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--problem", type=str, help="Run only this problem id (e.g. Hodge)")
    ap.add_argument("--probe-only", action="store_true",
                     help="Only run the first question per problem")
    args = ap.parse_args()

    print("=" * 70)
    print("  CLAY MILLENNIUM PROBLEMS -- CK study orchestrator")
    print("=" * 70)
    print(f"  date: {datetime.utcnow().isoformat(timespec='seconds')}Z")
    print(f"  output: {OUT_DIR}")
    print(f"  research_first: ON (each chat budgets 60s of Chrome research)")
    print()

    targets = CLAY_PROBLEMS
    if args.problem:
        targets = [p for p in CLAY_PROBLEMS if p["id"] == args.problem]
        if not targets:
            print(f"  unknown --problem {args.problem!r}; choose from "
                    f"{[p['id'] for p in CLAY_PROBLEMS]}")
            return 1

    all_results = []
    panel_t0 = time.time()
    for prob in targets:
        if args.probe_only:
            prob = dict(prob)
            prob["questions"] = prob["questions"][:1]
        out = study_problem(prob)
        all_results.append(out)

    # Write panel summary
    summary_path = OUT_DIR / "CLAY_PANEL_SUMMARY.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump({
            "iso_ts": datetime.utcnow().isoformat(timespec='seconds') + "Z",
            "n_problems": len(all_results),
            "n_questions_total": sum(len(p["responses"]) for p in all_results),
            "elapsed_sec": time.time() - panel_t0,
            "results": all_results,
        }, f, indent=2, default=str)
    print()
    print(f"  panel summary: {summary_path}")
    print(f"  per-problem md: {OUT_DIR}/CLAY_*.md")
    print(f"  total elapsed: {time.time() - panel_t0:.0f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
