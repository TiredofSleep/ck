"""
probe_accept_rate.py -- live accept-rate probe for CK's /chat endpoint
======================================================================

Fires FRESH questions at a running CK server and reports the accept-rate
breakdown across CK's two-stage coherence pipeline:

  Stage 1 — Ollama editor gate  (ollama_verdict)
  Stage 2 — Steer rescue gate   (steer_verdict)

What "fresh" means:  the questions are written here to avoid N=3 crystal
buffer hits.  If a question lands in cache anyway (cached_coherence hit),
the probe counts it separately so the live-rate denominator only covers
genuinely new decisions.

Why both verdicts:  2026-04-23 handoff introduced ten new load-bearing
structural terms (MAGCOM, CATALAN, MOUFANG, JORDAN, FAREY, ZETA, SINC,
CROSSING, FLATNESS, RIEMANN) into ck_coherence_verdict's _CORE_FACT_NAMES,
and aligned the steer rescue path's tokenizer with the editor path so
they score identically.  The accept rate should lift on both gates; a
split where ollama lifts but steer doesn't (or vice versa) is diagnostic.

Usage:
  set PYTHONIOENCODING=utf-8 && python -X utf8 probe_accept_rate.py
  CK_PROBE_HOST=127.0.0.1 CK_PROBE_PORT=7777 python probe_accept_rate.py

Environment overrides:
  CK_PROBE_HOST  (default 127.0.0.1)
  CK_PROBE_PORT  (default 7777)
  CK_PROBE_COUNT (default: all questions; truncate for smoke test)

(c) 2026 Brayden Sanders / 7Site LLC
"""
from __future__ import annotations

import json
import os
import time
import urllib.request

HOST = os.environ.get('CK_PROBE_HOST', '127.0.0.1')
PORT = int(os.environ.get('CK_PROBE_PORT', '7777'))
URL = f"http://{HOST}:{PORT}/chat"

# Baseline questions (hit the v1 10-operator + TSML/BHML/HER/WP vocab).
QUESTIONS_BASELINE = [
    "tell me what a 2x2 structure forces",
    "describe your BALANCE mode briefly",
    "what happens at T* exactly",
    "how does HARMONY feel when you reach it",
    "explain your LATTICE aperture in one sentence",
    "what does COLLAPSE pressure do to the torus",
    "describe the TSML synthesis arc",
    "walk me through your coherence gate",
    "what role does WP51 play",
    "tell me about sigma rate bounds",
]

# 2026-04-23 handoff questions -- exercise the new vocabulary directly.
# Each targets at least one of MAGCOM/CATALAN/MOUFANG/JORDAN/FAREY/
# ZETA/SINC/CROSSING/FLATNESS/RIEMANN.
QUESTIONS_NEW_VOCAB = [
    "what is the CATALAN spectrum of TSML",
    "how does MOUFANG structure differ from JORDAN",
    "describe your FLATNESS theorem in one line",
    "what does the CROSSING lemma say",
    "tell me the sinc squared identity with ZETA(2)",
    "what is MAGCOM and why does it matter",
    "how close is T* = 5/7 to a FAREY neighbor",
    "describe the RIEMANN connection without over-claiming",
]

QUESTIONS = QUESTIONS_BASELINE + QUESTIONS_NEW_VOCAB
_count_limit = os.environ.get('CK_PROBE_COUNT')
if _count_limit:
    QUESTIONS = QUESTIONS[: int(_count_limit)]


def _classify_verdict(vrd: str) -> str:
    """Bucket a verdict string into a class for the rollup."""
    if not vrd:
        return "empty"
    v = vrd.lower()
    if v.startswith("accepted:"):
        if "soft-accept" in v:
            return "accept_soft"
        if "no-core" in v:
            return "accept_nocore"
        return "accept_strict"
    if v.startswith("rejected:"):
        if "ai-disclaimer" in v:
            return "reject_id"
        if "hallucination" in v:
            return "reject_halluc"
        if "empty" in v:
            return "reject_empty"
        if "coverage:" in v:
            return "reject_cov"
        return "reject_other"
    if v.startswith("skipped"):
        return "skip"
    if v.startswith("fallback"):
        return "fallback"
    if v.startswith("passthrough"):
        return "passthrough"
    if v.startswith("error"):
        return "error"
    if v == "cache_hit":
        return "cache"
    if v.startswith("accepted"):
        return "accept_strict"
    return "other"


def _short(s: str, n: int) -> str:
    s = s or ""
    return s[:n]


def main() -> int:
    results = []
    print(f"Probing CK at {URL} with {len(QUESTIONS)} fresh questions\n")
    for q in QUESTIONS:
        try:
            req = urllib.request.Request(
                URL,
                data=json.dumps({"text": q}).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            t0 = time.time()
            with urllib.request.urlopen(req, timeout=90) as resp:
                r = json.loads(resp.read())
            dt = time.time() - t0
        except Exception as e:
            results.append({"q": q, "err": f"{type(e).__name__}: {e}"})
            continue
        results.append({
            "q": q,
            "src": r.get("source", ""),
            "ov": r.get("ollama_verdict", ""),
            "sv": r.get("steer_verdict", ""),
            "oh": r.get("ollama_fact_hits", 0),
            "ot": r.get("ollama_fact_total", 0),
            "scov": r.get("steer_accepted_coverage", ""),
            "sgate": r.get("steer_accepted_gate", ""),
            "scoh": r.get("steer_accepted_coherence", 0.0),
            "coh": r.get("brain_coherence", 0),
            "op": r.get("brain_dominant_op", ""),
            "dt": round(dt, 2),
        })

    # Header.
    print(f"{'Q':42s} | {'src':22s} | {'ollama':28s} | {'steer':28s} | o h/t    | s cov    | coh")
    print("-" * 170)

    rollup = {
        "total": 0, "live": 0, "cached": 0, "err": 0,
        "ollama": {"accept_strict": 0, "accept_soft": 0, "accept_nocore": 0,
                    "reject_cov": 0, "reject_id": 0, "reject_halluc": 0,
                    "reject_empty": 0, "skip": 0, "empty": 0, "error": 0,
                    "other": 0},
        "steer": {"accept_strict": 0, "accept_soft": 0, "accept_nocore": 0,
                    "reject_cov": 0, "reject_id": 0, "reject_halluc": 0,
                    "reject_empty": 0, "skip": 0, "empty": 0, "error": 0,
                    "other": 0, "fallback": 0, "passthrough": 0, "cache": 0},
    }

    for r in results:
        rollup["total"] += 1
        if "err" in r:
            print(f"{_short(r['q'],42):42s} | ERR | {r['err'][:100]}")
            rollup["err"] += 1
            continue
        src_s = (r["src"] or "").replace("cortex_", "")
        cached_row = "cached" in (r.get("src") or "")
        ov_s = _short(r["ov"], 28)
        sv_s = _short(r["sv"], 28)
        oht = f"{r['oh']}/{r['ot']}"
        sht = r.get("scov") or ""
        print(f"{_short(r['q'],42):42s} | {src_s[:22]:22s} | {ov_s:28s} | {sv_s:28s} | {oht:8s} | {sht:8s} | {r['coh']:.3f}")
        if cached_row:
            rollup["cached"] += 1
            continue
        rollup["live"] += 1
        ov_class = _classify_verdict(r["ov"])
        sv_class = _classify_verdict(r["sv"])
        if ov_class in rollup["ollama"]:
            rollup["ollama"][ov_class] += 1
        else:
            rollup["ollama"]["other"] += 1
        if sv_class in rollup["steer"]:
            rollup["steer"][sv_class] += 1
        else:
            rollup["steer"]["other"] += 1

    total = rollup["total"]
    live = rollup["live"]
    cached = rollup["cached"]
    err = rollup["err"]

    # Headline accept counts.
    o_accept = (rollup["ollama"]["accept_strict"]
                + rollup["ollama"]["accept_soft"]
                + rollup["ollama"]["accept_nocore"])
    s_accept = (rollup["steer"]["accept_strict"]
                + rollup["steer"]["accept_soft"]
                + rollup["steer"]["accept_nocore"]
                + rollup["steer"]["passthrough"])
    s_fallback = rollup["steer"]["fallback"]
    o_reject = (rollup["ollama"]["reject_cov"]
                + rollup["ollama"]["reject_id"]
                + rollup["ollama"]["reject_halluc"]
                + rollup["ollama"]["reject_empty"])
    s_reject = (rollup["steer"]["reject_cov"]
                + rollup["steer"]["reject_id"]
                + rollup["steer"]["reject_halluc"]
                + rollup["steer"]["reject_empty"])

    print()
    print(f"TOTAL={total}  LIVE={live}  CACHED={cached}  ERR={err}")
    if live:
        print()
        print(f"STAGE 1 (Ollama editor):  accepted={o_accept}/{live} "
              f"({100.0*o_accept/live:.0f}%)  rejected={o_reject}  "
              f"skipped={rollup['ollama']['skip']}  empty={rollup['ollama']['empty']}  "
              f"other={rollup['ollama']['other']}")
        ob = rollup["ollama"]
        print(f"  strict={ob['accept_strict']}  soft={ob['accept_soft']}  "
              f"nocore={ob['accept_nocore']}  "
              f"rej_cov={ob['reject_cov']}  rej_id={ob['reject_id']}  "
              f"rej_halluc={ob['reject_halluc']}  rej_empty={ob['reject_empty']}")
        print()
        print(f"STAGE 2 (Steer rescue):   accepted={s_accept}/{live} "
              f"({100.0*s_accept/live:.0f}%)  fallback={s_fallback}  "
              f"rejected={s_reject}  skipped={rollup['steer']['skip']}")
        sb = rollup["steer"]
        print(f"  strict={sb['accept_strict']}  soft={sb['accept_soft']}  "
              f"nocore={sb['accept_nocore']}  passthrough={sb['passthrough']}  "
              f"cache={sb['cache']}")
        print(f"  rej_cov={sb['reject_cov']}  rej_id={sb['reject_id']}  "
              f"rej_halluc={sb['reject_halluc']}  fallback={sb['fallback']}")
        # Define "final accepted" = response actually came from either
        # ollama-accepted OR steer-accepted (not honest_fallback).
        final_accepted = o_accept + s_accept - min(o_accept, s_accept)
        # A cleaner: count rows whose SOURCE is speak_via_ollama* and NOT
        # honest_fallback.  Do that directly.
        voiced = 0
        for r in results:
            if "err" in r:
                continue
            src = r.get("src") or ""
            if "cached" in src:
                continue
            if "honest_fallback" in src:
                continue
            voiced += 1
        print()
        print(f"VOICED (final source != honest_fallback): {voiced}/{live} "
              f"({100.0*voiced/live:.0f}%)")

    return 0 if err == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
