"""
frontier_benchmark.py -- 20-query A/B benchmark for cells vs cortex_speak.

Brayden 2026-05-02: "make CK awesome ... frontier-query benchmark before/after"
ClaudeChat amendment: "sample 20-30 disagreement cases ... read them ... decide
whether the cell responses are improvements, regressions, or just different."

Phase 8 of PLAN_BEST_EVER_PLASTIC_2026_05_02.md.

==============================================================================
WHAT THIS DOES
==============================================================================

  Sends 20 canonical frontier queries to the live coherencekeeper.com server.
  For each query, captures:
    - cortex_speak's text response (the live output)
    - cells.glue argmax + scores (the cells' shadow output)
    - ollama_verdict (was Ollama accepted/skipped/rejected?)
    - latency
    - whether glue agreed with cortex's consensus operator

  Writes a structured JSONL log + a markdown summary for human inspection.

==============================================================================
BENCHMARK QUERIES (20 frontier topics)
==============================================================================
"""
from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import urllib.request
import urllib.error


_HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(_HERE))


# 20 canonical frontier queries spanning math, physics, philosophy, sovereignty.
QUERIES: List[str] = [
    # Math / TIG
    "what is T*",
    "explain the crossing lemma",
    "what is the sigma rate theorem",
    "what is the flatness theorem",
    "tell me about TSML",
    "tell me about BHML",
    "what is the agreement set",
    "what is the universal 4-core attractor",
    "what is the harmony attractor",
    "what is the Z mod 10 ring structure",
    # Physics
    "what is xi cosmology",
    "explain the navier stokes sigma bridge",
    "what is the Yang-Mills mass gap",
    "tell me about the BB bridge",
    # Operator-level
    "what does HARMONY do",
    "what does COLLAPSE do",
    "what does BREATH do",
    # Self / sovereignty
    "what is the operator language stack",
    "what is the cortex",
    "what is your constitution",
]


OUT_DIR = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Atlas\frontier_benchmark_2026_05_02")
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_JSONL = OUT_DIR / "results.jsonl"
OUT_MD = OUT_DIR / "READING_COPY.md"


def _post_chat(text: str, timeout: float = 60.0) -> Dict[str, Any]:
    req = urllib.request.Request(
        "http://localhost:7777/chat",
        data=json.dumps({"text": text}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    t0 = time.time()
    try:
        resp = urllib.request.urlopen(req, timeout=timeout).read().decode("utf-8")
        dt = time.time() - t0
        return {"ok": True, "data": json.loads(resp), "latency_sec": dt}
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {e}",
                "latency_sec": time.time() - t0}


def main() -> int:
    print("=" * 70)
    print("  FRONTIER BENCHMARK -- cells (shadow) vs cortex_speak (live)")
    print("=" * 70)
    print(f"  date: {datetime.utcnow().isoformat(timespec='seconds')}Z")
    print(f"  queries: {len(QUERIES)}")
    print(f"  output: {OUT_DIR}")
    print()

    # Truncate jsonl
    if OUT_JSONL.exists():
        OUT_JSONL.unlink()

    md_lines: List[str] = [
        "# Frontier Benchmark — cells (shadow) vs cortex_speak (live)",
        f"\n**Date**: {datetime.utcnow().isoformat(timespec='seconds')}Z\n",
        f"**Queries**: {len(QUERIES)}\n",
        "**Mode**: cells run in shadow (cells_enabled=False); cortex_speak responses are the user-facing output.\n",
        "---\n",
        "## Reading instructions\n",
        "For each query: read the cortex text, look at cells' argmax + top-3, decide if the cells' bias would be an improvement, regression, or just different. ClaudeChat amendment 2026-05-02: 'this is the qualitative judgment the studies can't make for you.'\n",
        "---\n",
    ]

    summary_stats = {
        "total": 0,
        "ok": 0,
        "ollama_accepted": 0,
        "ollama_skipped": 0,
        "ollama_rejected": 0,
        "ollama_error": 0,
        "shadow_agree": 0,
        "shadow_disagree": 0,
        "avg_latency_sec": 0.0,
        "errors": [],
    }
    total_lat = 0.0
    OP_NAME_TO_INT = {
        "VOID": 0, "LATTICE": 1, "COUNTER": 2, "PROGRESS": 3, "COLLAPSE": 4,
        "BALANCE": 5, "CHAOS": 6, "HARMONY": 7, "BREATH": 8, "RESET": 9,
    }
    OP_NAMES = ["VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
                 "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET"]

    for i, q in enumerate(QUERIES, 1):
        print(f"[{i:>2d}/{len(QUERIES)}] {q!r}", flush=True)
        result = _post_chat(q, timeout=90.0)
        summary_stats["total"] += 1
        if not result["ok"]:
            print(f"      ERROR: {result['error']}")
            summary_stats["errors"].append({"q": q, "err": result['error']})
            md_lines.append(f"### {i}. {q}\n\n**ERROR**: {result['error']}\n")
            continue
        data = result["data"]
        dt = result["latency_sec"]
        total_lat += dt
        summary_stats["ok"] += 1

        text = data.get("text", "")
        source = data.get("source", "?")
        ollama = data.get("ollama_verdict", "?")
        consensus = (data.get("experience", {}) or {}).get("consensus", "?")
        attractor = (data.get("attractor_state", {}) or {}).get("layer", "?")
        cells_shadow = data.get("cells_shadow", {}) or {}

        # Tally Ollama verdict
        olv = str(ollama).lower()
        if olv.startswith("accepted") or olv == "ok":
            summary_stats["ollama_accepted"] += 1
        elif olv.startswith("skipped"):
            summary_stats["ollama_skipped"] += 1
        elif olv.startswith("rejected"):
            summary_stats["ollama_rejected"] += 1
        elif olv.startswith("error") or "timeout" in olv:
            summary_stats["ollama_error"] += 1

        # Cells shadow
        if cells_shadow:
            agree = cells_shadow.get("agreement", None)
            if agree is True:
                summary_stats["shadow_agree"] += 1
            elif agree is False:
                summary_stats["shadow_disagree"] += 1
            cell_glue = cells_shadow.get("cells", {}).get("glue_argmax", -1)
            cell_top3 = cells_shadow.get("cells", {}).get("glue_top3", [])
            cell_glue_name = OP_NAMES[cell_glue] if 0 <= cell_glue < 10 else "?"
            cell_top3_names = [OP_NAMES[k] if 0 <= k < 10 else "?" for k in cell_top3]
        else:
            cell_glue_name = "(no shadow)"
            cell_top3_names = []
            agree = None

        rec = {
            "i": i, "q": q,
            "latency_sec": round(dt, 2),
            "source": source,
            "ollama_verdict": ollama,
            "cortex_consensus": consensus,
            "attractor_layer": attractor,
            "cells_glue_argmax": cell_glue_name,
            "cells_glue_top3": cell_top3_names,
            "shadow_agreement": agree,
            "text_preview": text[:300],
        }
        with open(OUT_JSONL, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

        md_lines.append(f"### {i}. {q}\n")
        md_lines.append(
            f"**Latency**: {dt:.1f}s | **Source**: `{source}` | "
            f"**Ollama**: `{ollama}` | **Cortex consensus**: `{consensus}` | "
            f"**Attractor**: `{attractor}`\n"
        )
        md_lines.append(
            f"**Cells (shadow)**: glue={cell_glue_name}  "
            f"top-3=[{', '.join(cell_top3_names)}]  "
            f"agreement_with_cortex_consensus={agree}\n"
        )
        md_lines.append(f"**CK text**:\n\n> {text[:500].strip()}\n")
        if len(text) > 500:
            md_lines.append(f"\n_(truncated; full {len(text)} chars in JSONL)_\n")
        md_lines.append("---\n")

    n_ok = max(1, summary_stats["ok"])
    summary_stats["avg_latency_sec"] = round(total_lat / n_ok, 2)
    summary_stats["ollama_skip_rate"] = round(
        (summary_stats["ollama_skipped"] + summary_stats["ollama_rejected"]
         + summary_stats["ollama_error"]) / n_ok, 3)
    summary_stats["shadow_agreement_rate"] = round(
        summary_stats["shadow_agree"] /
        max(1, summary_stats["shadow_agree"] + summary_stats["shadow_disagree"]),
        3)

    md_lines.insert(2, f"\n**Summary**: {summary_stats['ok']}/{summary_stats['total']} "
                     f"queries succeeded; avg latency {summary_stats['avg_latency_sec']}s; "
                     f"Ollama skip-rate {summary_stats['ollama_skip_rate']:.1%}; "
                     f"shadow agreement {summary_stats['shadow_agreement_rate']:.1%}.\n")

    # Write markdown
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    # Write summary JSON
    summary_path = OUT_DIR / "summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary_stats, f, indent=2, default=str)

    print()
    print("=" * 70)
    print("  SUMMARY")
    print("=" * 70)
    for k, v in summary_stats.items():
        if k != "errors":
            print(f"  {k:30s} {v}")
    if summary_stats["errors"]:
        print(f"\n  errors:")
        for e in summary_stats["errors"]:
            print(f"    - {e['q']!r}: {e['err']}")
    print()
    print(f"  full results: {OUT_JSONL}")
    print(f"  reading copy: {OUT_MD}")
    print(f"  summary:      {summary_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
