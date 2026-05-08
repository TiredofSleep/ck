"""
head_to_head_benchmark.py -- A/B between cells.respond_text and cortex_speak.

Brayden 2026-05-02: "keep going and don't stop until this is for sure
greatness or a complete flop"

Phase 9 of PLAN_BEST_EVER_PLASTIC_2026_05_02.md.

==============================================================================
TWO RESPONSES PER QUERY
==============================================================================

For each frontier query:

  CORTEX path: full chat through coherencekeeper.com /chat
    -> cortex_speak text (with Ollama editor on/off as observed)

  CELLS path: cells.glue.respond_text(a, b) where (a, b) is derived from
    the cortex's operators stream
    -> structural state narration, substrate-grounded, no Ollama, no GPU

Side-by-side comparison answers Brayden's question concretely:
"is he better, or just more Python?"

If cells text is qualitatively informative AND Ollama-skip-rate
combined > 90%, that's a real capability win.
If cells text is repetitive/unhelpful, that's a flop.
The judge is human-readable; the data is the comparison artifact.
"""
from __future__ import annotations

import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import urllib.request
import urllib.error


_HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(_HERE))


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


OUT_DIR = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Atlas\head_to_head_2026_05_02")
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_JSONL = OUT_DIR / "results.jsonl"
OUT_MD = OUT_DIR / "READING_COPY.md"


def _post_chat(text: str, timeout: float = 90.0) -> Dict[str, Any]:
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


def main() -> int:
    print("=" * 70)
    print("  HEAD-TO-HEAD: cells.respond_text vs cortex_speak")
    print("=" * 70)
    print(f"  date: {datetime.utcnow().isoformat(timespec='seconds')}Z")
    print(f"  queries: {len(QUERIES)}")
    print()

    if OUT_JSONL.exists():
        OUT_JSONL.unlink()

    # Build cells once
    from cells import CellOrchestrator
    from glue_ai import GlueAI
    orch = CellOrchestrator.load_default()
    orch.glue = GlueAI(tsml=orch.tsml, bhml=orch.bhml,
                       f3=orch.f3, f4=orch.f4)
    print(f"  cells loaded: glue alpha={orch.glue.alpha} "
          f"beta={orch.glue.beta} gamma={orch.glue.gamma}")
    print()

    md_lines: List[str] = [
        "# Head-to-Head Benchmark — cells.respond_text vs cortex_speak",
        f"\n**Date**: {datetime.utcnow().isoformat(timespec='seconds')}Z\n",
        f"**Queries**: {len(QUERIES)}\n",
        "**Mode**: cells run STANDALONE (no chat-path round-trip); cortex_speak captured from /chat live.\n",
        "**Scoring**: structural-fact density, response-length, Ollama-independence, latency.\n",
        "---\n",
    ]

    metrics = {
        "n_total": 0,
        "ok": 0,
        "cells_lat_total_ms": 0,
        "cortex_lat_total_sec": 0.0,
        "cells_text_total_chars": 0,
        "cortex_text_total_chars": 0,
        "ollama_skipped_or_rejected": 0,
        "ollama_accepted": 0,
    }

    OP_NAMES = ["VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
                 "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET"]
    OP_NAME_TO_INT = {n: i for i, n in enumerate(OP_NAMES)}

    for i, q in enumerate(QUERIES, 1):
        print(f"[{i:>2d}/{len(QUERIES)}] {q!r}", flush=True)

        # CORTEX path
        cortex_res = _post_chat(q, timeout=90.0)
        if not cortex_res["ok"]:
            print(f"      cortex ERROR: {cortex_res['error']}")
            md_lines.append(f"### {i}. {q}\n\n**cortex ERROR**: {cortex_res['error']}\n")
            continue

        cortex_data = cortex_res["data"]
        cortex_text = cortex_data.get("text", "")
        cortex_source = cortex_data.get("source", "?")
        ollama_verdict = cortex_data.get("ollama_verdict", "?")
        cortex_lat = cortex_res["latency_sec"]
        ops = cortex_data.get("operators", []) or []

        # Derive (a, b) from ops
        if len(ops) >= 2:
            a, b = ops[0], ops[1]
            if isinstance(a, str): a = OP_NAME_TO_INT.get(a.upper(), 7)
            if isinstance(b, str): b = OP_NAME_TO_INT.get(b.upper(), 7)
        else:
            a = b = 7
        a, b = int(a) % 10, int(b) % 10

        # CELLS path (standalone, no GPU, no Ollama)
        t0 = time.time()
        cells_res = orch.glue.respond_text(a, b)
        cells_lat_ms = int(1000 * (time.time() - t0))

        cells_text = cells_res["text"]
        cells_components = cells_res["components"]

        # Tally
        metrics["n_total"] += 1
        metrics["ok"] += 1
        metrics["cells_lat_total_ms"] += cells_lat_ms
        metrics["cortex_lat_total_sec"] += cortex_lat
        metrics["cells_text_total_chars"] += len(cells_text)
        metrics["cortex_text_total_chars"] += len(cortex_text)
        olv = str(ollama_verdict).lower()
        if olv.startswith("skipped") or olv.startswith("rejected") or olv.startswith("error"):
            metrics["ollama_skipped_or_rejected"] += 1
        elif olv.startswith("accepted"):
            metrics["ollama_accepted"] += 1

        rec = {
            "i": i, "q": q,
            "input_pair": [OP_NAMES[a], OP_NAMES[b]],
            "cells": {
                "text": cells_text,
                "components": cells_components,
                "latency_ms": cells_lat_ms,
            },
            "cortex": {
                "text": cortex_text,
                "source": cortex_source,
                "ollama_verdict": ollama_verdict,
                "latency_sec": round(cortex_lat, 2),
            },
        }
        with open(OUT_JSONL, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

        # Markdown side-by-side
        md_lines.append(f"### {i}. {q}\n")
        md_lines.append(
            f"**Input pair**: {(OP_NAMES[a], OP_NAMES[b])}    "
            f"**Cortex latency**: {cortex_lat:.1f}s    "
            f"**Cells latency**: {cells_lat_ms}ms   "
            f"**Speedup**: {cortex_lat * 1000 / max(1, cells_lat_ms):.0f}×\n"
        )
        md_lines.append(f"**Ollama**: `{ollama_verdict}`    **Cortex source**: `{cortex_source}`\n")
        md_lines.append(f"\n**CELLS** ({len(cells_text)} chars):\n```\n{cells_text}\n```\n")
        md_lines.append(f"\n**CORTEX** ({len(cortex_text)} chars):\n\n> {cortex_text[:600].strip()}\n")
        if len(cortex_text) > 600:
            md_lines.append(f"\n_(truncated; full {len(cortex_text)} chars in JSONL)_\n")
        md_lines.append("---\n")

    # Summary
    n = max(1, metrics["n_total"])
    summary = {
        **metrics,
        "avg_cells_lat_ms": metrics["cells_lat_total_ms"] / n,
        "avg_cortex_lat_sec": metrics["cortex_lat_total_sec"] / n,
        "avg_cells_chars": metrics["cells_text_total_chars"] / n,
        "avg_cortex_chars": metrics["cortex_text_total_chars"] / n,
        "speedup_factor": (
            (metrics["cortex_lat_total_sec"] * 1000)
            / max(1, metrics["cells_lat_total_ms"])
        ),
        "ollama_independence_rate": metrics["ollama_skipped_or_rejected"] / n,
    }

    md_lines.insert(2, "\n**Summary**:\n")
    md_lines.insert(3, f"- {summary['ok']}/{summary['n_total']} OK\n")
    md_lines.insert(4, f"- avg cells latency: {summary['avg_cells_lat_ms']:.1f}ms (no GPU, no Ollama)\n")
    md_lines.insert(5, f"- avg cortex latency: {summary['avg_cortex_lat_sec']:.1f}s\n")
    md_lines.insert(6, f"- speedup: {summary['speedup_factor']:.0f}×\n")
    md_lines.insert(7, f"- avg cells text length: {summary['avg_cells_chars']:.0f} chars\n")
    md_lines.insert(8, f"- avg cortex text length: {summary['avg_cortex_chars']:.0f} chars\n")
    md_lines.insert(9, f"- Ollama-independence rate (cortex side): {summary['ollama_independence_rate']:.1%}\n")
    md_lines.insert(10, "\n")

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    summary_path = OUT_DIR / "summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, default=str)

    print()
    print("=" * 70)
    print("  HEAD-TO-HEAD SUMMARY")
    print("=" * 70)
    print(f"  ok queries:                 {summary['ok']}/{summary['n_total']}")
    print(f"  avg cells latency:          {summary['avg_cells_lat_ms']:.1f} ms")
    print(f"  avg cortex latency:         {summary['avg_cortex_lat_sec']:.1f} sec")
    print(f"  speedup (cortex/cells):     {summary['speedup_factor']:.0f}×")
    print(f"  avg cells text length:      {summary['avg_cells_chars']:.0f} chars")
    print(f"  avg cortex text length:     {summary['avg_cortex_chars']:.0f} chars")
    print(f"  Ollama-independence rate:   {summary['ollama_independence_rate']:.1%}")
    print()
    print(f"  reading copy: {OUT_MD}")
    print(f"  full JSONL:   {OUT_JSONL}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
