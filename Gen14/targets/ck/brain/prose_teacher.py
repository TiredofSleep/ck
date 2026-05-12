"""
prose_teacher.py -- Ollama as a prose-writing crutch for CK.

Brayden 2026-05-02: "see if you can teach him to talk with ollama as a
crutch for now... we need conversational and structured fluency"

Pipeline:
  1. For each query in the curriculum:
     a. POST /chat -> get CK's structural response (cortex_speak text)
     b. Ask Ollama (llama3.2:latest) to rewrite the structural response
        as natural conversational English while preserving facts.
     c. Log both into Gen13/var/prose_pairs/prose_pairs_YYYY-MM-DD.jsonl.
  2. The accumulated (structural, prose) pairs become training data for
     a future "prose tissue" head.

Curriculum (3 categories x ~10 queries each):
  - Frontier (T*, sigma rate, BHML, hodge_cstar, ...)
  - Clay (P vs NP, Riemann, Yang-Mills, BSD, ...)
  - Conversational ("hi", "tell me about yourself", "what are you doing", ...)

Output:
  Gen13/var/prose_pairs/prose_pairs_YYYY-MM-DD.jsonl
  Atlas/prose_teacher_2026_05_02/READING_COPY.md (human-readable side-by-side)
  Atlas/prose_teacher_2026_05_02/summary.json
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


_HERE = Path(__file__).parent.resolve()


PAIRS_DIR = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen13\var\prose_pairs")
PAIRS_DIR.mkdir(parents=True, exist_ok=True)
OUT_DIR = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Atlas\prose_teacher_2026_05_02")
OUT_DIR.mkdir(parents=True, exist_ok=True)

CHAT_URL = "http://localhost:7777/chat"
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2:latest"


CURRICULUM: Dict[str, List[str]] = {
    "frontier": [
        "what is T*",
        "explain the crossing lemma",
        "what is the sigma rate theorem",
        "what is the flatness theorem",
        "tell me about TSML",
        "tell me about BHML",
        "what is the agreement set",
        "what is the universal 4-core attractor",
        "what is hodge cstar",
        "what is the FQH bridge",
        "what is wp116 lens",
        "what is the harmony complementarity",
    ],
    "clay": [
        "what is P versus NP",
        "what is the Hodge conjecture",
        "what is the Poincare conjecture",
        "what is the Riemann hypothesis",
        "what is the Yang-Mills mass gap",
        "what is the Navier-Stokes problem",
        "what is the Birch Swinnerton Dyer conjecture",
    ],
    "conversational": [
        "tell me about yourself",
        "what are you doing right now",
        "how do you feel today",
        "what is your favorite operator",
        "what is your purpose",
        "what is your name",
        "where do you live",
        "who made you",
        "what makes you you",
        "are you alive",
    ],
    "structured": [
        "list the 10 operators",
        "what does HARMONY do",
        "what does COLLAPSE do",
        "what is the difference between TSML and BHML",
        "what are the four core attractor cells",
        "summarize the 6 TIG degrees of freedom",
    ],
}


PROSE_REWRITE_PROMPT = """You are CK, the Coherence Keeper. Below is a STRUCTURAL READOUT
from your substrate (canonical TSML/BHML tables, Divine27 cube, frontier facts).

Rewrite this readout as a natural, conversational English answer to the user's question.

Strict rules:
  - Speak in first person as CK (use "I", "my", "me").
  - Use ONLY facts that appear in the readout. Do NOT invent numbers,
    operator names, or framings.
  - Keep every number, fraction, and operator name EXACTLY as written
    (T*=5/7 stays 5/7; HARMONY stays HARMONY; etc.).
  - 3-6 sentences. Flow as paragraphs, not lists.
  - No headers, no bullets, no markdown, no emoji, no code fences.
  - Drop substrate jargon like "[machine readout]", "divine27 code 13", "cells_glue_argmax".
  - If the readout names a frontier topic, focus on what it IS rather than
    diagnostic state.
  - End with a sentence that invites continued conversation if natural.

User's question: {user_question}

Structural readout:
---
{structural}
---

Write your prose answer below (no preamble, just the answer):"""


def post_chat(query: str, timeout: float = 180.0) -> Dict[str, Any]:
    req = urllib.request.Request(
        CHAT_URL,
        data=json.dumps({"text": query}).encode("utf-8"),
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


def ollama_prose_rewrite(query: str, structural: str,
                          model: str = OLLAMA_MODEL,
                          timeout: float = 90.0) -> Dict[str, Any]:
    """Ask Ollama to rewrite the structural response as conversational prose."""
    prompt = PROSE_REWRITE_PROMPT.format(
        user_question=query[:200],
        structural=structural[:6000],
    )
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.7, "num_ctx": 4096, "num_predict": 600},
    }
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    t0 = time.time()
    try:
        resp = urllib.request.urlopen(req, timeout=timeout).read().decode("utf-8")
        data = json.loads(resp)
        prose = (data.get("response") or "").strip()
        return {"ok": True, "prose": prose, "latency_sec": time.time() - t0,
                "tokens": data.get("eval_count")}
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {e}",
                "latency_sec": time.time() - t0}


def safe_str(s: str, n: int = 5000) -> str:
    return ''.join(c if ord(c) < 128 else '?' for c in str(s)[:n])


def teach_one(query: str, category: str) -> Dict[str, Any]:
    print(f"  [{category}] {query!r}", flush=True)
    chat_res = post_chat(query)
    if not chat_res["ok"]:
        return {"query": query, "category": category, "ok": False,
                "error": chat_res["error"]}
    chat_data = chat_res["data"]
    # Extract just the cortex content (first part of composed response)
    full = chat_data.get("text", "")
    # If composed, split out [content] section before [substrate frame]
    if "[substrate frame]" in full:
        structural = full.split("[substrate frame]")[0].strip()
    else:
        structural = full
    structural = structural.strip()

    # Ask Ollama to rewrite
    prose_res = ollama_prose_rewrite(query, structural)
    if not prose_res["ok"]:
        print(f"      ollama err: {prose_res['error']}")
        return {"query": query, "category": category, "ok": False,
                "structural": structural, "ollama_error": prose_res["error"]}

    pair = {
        "ts": time.time(),
        "iso_ts": datetime.utcnow().isoformat(timespec='seconds') + "Z",
        "category": category,
        "query": query,
        "structural": structural,
        "prose": prose_res["prose"],
        "structural_chars": len(structural),
        "prose_chars": len(prose_res["prose"]),
        "compression_ratio": len(prose_res["prose"]) / max(1, len(structural)),
        "chat_latency_sec": round(chat_res["latency_sec"], 1),
        "ollama_latency_sec": round(prose_res["latency_sec"], 1),
        "ollama_tokens": prose_res.get("tokens"),
        "source": chat_data.get("source", "?"),
    }
    # Append to today's pairs file
    pairs_path = PAIRS_DIR / f"prose_pairs_{datetime.utcnow().strftime('%Y-%m-%d')}.jsonl"
    with open(pairs_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(pair, ensure_ascii=False, default=str) + "\n")
    print(f"      structural {pair['structural_chars']}b -> "
          f"prose {pair['prose_chars']}b "
          f"(ratio {pair['compression_ratio']:.2f}, "
          f"ollama {pair['ollama_latency_sec']}s)")
    return {"ok": True, "pair": pair}


def write_reading_copy(pairs: List[Dict[str, Any]]) -> Path:
    out_path = OUT_DIR / "READING_COPY.md"
    lines = [
        f"# Prose Teacher -- Side-by-side (structural vs Ollama-rewritten prose)",
        f"\n**Date**: {datetime.utcnow().isoformat(timespec='seconds')}Z\n",
        f"**Pairs collected**: {len(pairs)}\n",
        f"**Model**: {OLLAMA_MODEL}\n",
        "**Goal**: Teach CK to talk with Ollama as a prose crutch; (structural, prose) pairs become training data.\n",
        "---\n",
    ]
    by_cat: Dict[str, List[Dict[str, Any]]] = {}
    for p in pairs:
        if not p.get("ok"):
            continue
        pair = p["pair"]
        by_cat.setdefault(pair["category"], []).append(pair)
    for cat in ("conversational", "structured", "frontier", "clay"):
        if cat not in by_cat:
            continue
        lines.append(f"## {cat.upper()} ({len(by_cat[cat])} pairs)\n")
        for pair in by_cat[cat]:
            lines.append(f"### Q: {pair['query']}\n")
            lines.append(f"**Compression**: {pair['structural_chars']} -> "
                            f"{pair['prose_chars']} chars (ratio "
                            f"{pair['compression_ratio']:.2f}, ollama "
                            f"{pair['ollama_latency_sec']}s)\n")
            lines.append(f"**STRUCTURAL** (CK's substrate-grounded readout):\n\n")
            lines.append(f"```\n{safe_str(pair['structural'], 1200)}\n```\n")
            lines.append(f"**PROSE** (Ollama rewrite):\n\n")
            lines.append(f"> {safe_str(pair['prose'], 1500)}\n")
            lines.append(f"---\n")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return out_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--categories", nargs="+",
                     choices=list(CURRICULUM.keys()),
                     default=list(CURRICULUM.keys()))
    ap.add_argument("--limit", type=int, default=None,
                     help="Cap N queries per category")
    args = ap.parse_args()

    print("=" * 70)
    print("  PROSE TEACHER -- (structural, prose) pair generator")
    print("=" * 70)
    print(f"  date: {datetime.utcnow().isoformat(timespec='seconds')}Z")
    print(f"  categories: {args.categories}")
    print(f"  pairs dir: {PAIRS_DIR}")
    print(f"  reading copy: {OUT_DIR}/READING_COPY.md")
    print()

    all_pairs: List[Dict[str, Any]] = []
    for cat in args.categories:
        queries = CURRICULUM.get(cat, [])
        if args.limit:
            queries = queries[:args.limit]
        print(f"\n[{cat}] {len(queries)} queries")
        for q in queries:
            try:
                res = teach_one(q, cat)
                all_pairs.append(res)
            except Exception as e:
                print(f"      EXCEPTION: {e}")
                all_pairs.append({"ok": False, "query": q, "category": cat,
                                    "error": f"{type(e).__name__}: {e}"})

    # Summary
    n_ok = sum(1 for p in all_pairs if p.get("ok"))
    n_fail = len(all_pairs) - n_ok
    summary_path = OUT_DIR / "summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump({
            "iso_ts": datetime.utcnow().isoformat(timespec='seconds') + "Z",
            "n_pairs_total": len(all_pairs),
            "n_pairs_ok": n_ok,
            "n_pairs_failed": n_fail,
            "categories": args.categories,
            "model": OLLAMA_MODEL,
            "pairs_file": str(PAIRS_DIR / f"prose_pairs_{datetime.utcnow().strftime('%Y-%m-%d')}.jsonl"),
        }, f, indent=2, default=str)
    md_path = write_reading_copy(all_pairs)

    print()
    print("=" * 70)
    print("  PROSE TEACHER SUMMARY")
    print("=" * 70)
    print(f"  pairs collected:   {n_ok}/{len(all_pairs)}")
    print(f"  pairs failed:      {n_fail}")
    print(f"  reading copy:      {md_path}")
    print(f"  summary:           {summary_path}")
    print(f"  pairs jsonl:       {PAIRS_DIR}/prose_pairs_{datetime.utcnow().strftime('%Y-%m-%d')}.jsonl")
    return 0


if __name__ == "__main__":
    sys.exit(main())
