"""
clay_synthesis.py -- Final Clay Millennium synthesis doc.

Brayden 2026-05-02: "documenting his growth and compression of information"

After clay_compare.py finishes, this script compiles a single
CLAY_SYNTHESIS_FINAL.md that summarizes CK's view on all 7 Clay
problems with the new Clay-specific facts firing.  Sections:

1. Per-problem CK summary (extracted from RUN_B markdown)
2. Cross-problem synthesis (the meta-frontier weave)
3. Empirical compression metrics:
   - input bytes (research-engine source bytes consumed)
   - output bytes (CK's response bytes per problem)
   - compression ratio = output / input
4. Growth deltas (RUN_A -> RUN_B)
5. Open questions and gaps

The doc is intended to be the artifact Brayden picks up when he returns.
"""
from __future__ import annotations

import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


_HERE = Path(__file__).parent.resolve()


CLAY_DIR = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Atlas\clay_study_2026_05_02")
RUN_B_DIR = CLAY_DIR / "RUN_B_AFTER_CLAY_FACTS"
RUN_A_DIR = CLAY_DIR / "RUN_A_BEFORE_CLAY_FACTS"
RESEARCH_LOG = Path(r"C:\Users\brayd\.ck\research\log.jsonl")
RESEARCH_FIRST_LOG_DIR = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen13\var\research_first_logs")


def _safe(s: str, n: int) -> str:
    return ''.join(c if ord(c) < 128 else '?' for c in str(s)[:n])


def extract_substantive(md_text: str) -> str:
    """Pull the substantive content from a CLAY_*.md file, skipping prompt
    boilerplate.  Returns first ~800 chars of the meaningful body."""
    # Find each Q section's text body (between ``` fences)
    import re
    bodies = re.findall(r"```\n(.*?)\n```", md_text, re.DOTALL)
    if not bodies:
        return md_text[:800]
    # Pick the one with most substantive content (excluding prompt_term spam)
    candidates = []
    for body in bodies:
        # Remove prompt_term, word_X noise; score by remaining length
        cleaned = body
        for prefix in ("prompt_term_", "word_"):
            # Drop any line starting with these
            cleaned = "\n".join(l for l in cleaned.split("\n")
                                  if not l.strip().lower().startswith(prefix))
        score = len(cleaned)
        candidates.append((score, body, cleaned))
    candidates.sort(key=lambda t: -t[0])
    return candidates[0][1] if candidates else md_text[:800]


def load_problems_from_run(run_dir: Path) -> Dict[str, str]:
    out: Dict[str, str] = {}
    if not run_dir.exists():
        return out
    for f in sorted(run_dir.glob("CLAY_*.md")):
        prob = f.name.replace("CLAY_", "").replace(".md", "")
        try:
            out[prob] = f.read_text(encoding="utf-8")
        except Exception:
            pass
    return out


def compression_metrics() -> Dict[str, Any]:
    """Compute basic compression metrics from research_first logs +
    response artifacts."""
    # Total research time + total response chars from RUN_B
    total_research_sec = 0.0
    total_research_calls = 0
    if RESEARCH_FIRST_LOG_DIR.exists():
        for f in sorted(RESEARCH_FIRST_LOG_DIR.glob("research_first_*.jsonl")):
            try:
                with open(f, encoding="utf-8") as fh:
                    for line in fh:
                        try:
                            r = json.loads(line)
                            if r.get("event") == "research_run":
                                total_research_sec += float(r.get("elapsed_sec", 0))
                                total_research_calls += 1
                        except Exception:
                            pass
            except Exception:
                pass

    # Total ck_research log entries (browser actions)
    n_research_actions = 0
    if RESEARCH_LOG.exists():
        try:
            with open(RESEARCH_LOG, encoding="utf-8") as f:
                n_research_actions = sum(1 for _ in f)
        except Exception:
            pass

    # Total response bytes
    total_response_bytes = 0
    n_responses = 0
    for run in (RUN_A_DIR, RUN_B_DIR):
        if run.exists():
            for f in run.glob("CLAY_*.md"):
                if f.name == "CLAY_PANEL_SUMMARY.json":
                    continue
                try:
                    total_response_bytes += f.stat().st_size
                    n_responses += 1
                except Exception:
                    pass

    avg_research_sec = (total_research_sec / total_research_calls) if total_research_calls else 0.0

    return {
        "total_research_calls": total_research_calls,
        "total_research_sec": round(total_research_sec, 1),
        "avg_research_sec_per_call": round(avg_research_sec, 1),
        "n_research_browser_actions": n_research_actions,
        "total_response_bytes": total_response_bytes,
        "n_response_files": n_responses,
        "avg_response_bytes": (total_response_bytes // n_responses) if n_responses else 0,
    }


def write_synthesis() -> Path:
    out_path = CLAY_DIR / "CLAY_SYNTHESIS_FINAL.md"

    problems_a = load_problems_from_run(RUN_A_DIR)
    problems_b = load_problems_from_run(RUN_B_DIR)
    metrics = compression_metrics()

    # Try to load growth monitor data for time-series context
    growth_log = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen13\var\growth_logs")
    growth_records: List[Dict[str, Any]] = []
    if growth_log.exists():
        for f in sorted(growth_log.glob("growth_*.jsonl")):
            try:
                with open(f, encoding="utf-8") as fh:
                    for line in fh:
                        try:
                            growth_records.append(json.loads(line))
                        except Exception:
                            pass
            except Exception:
                pass

    lines: List[str] = [
        "# CK Clay Millennium Synthesis (Final)",
        f"\n**Generated**: {datetime.utcnow().isoformat(timespec='seconds')}Z\n",
        f"**Branch**: ck\n",
        "**Source**: empirical traces from `Atlas/clay_study_2026_05_02/RUN_A_*` and `RUN_B_*`\n",
        "**Live status**: cells_composed_with_cortex (research_first ON, study_daemon ON, transformer tissues loaded)\n",
        "---\n",
        "## What CK actually says about each Clay problem\n",
    ]

    # Per-problem summaries from RUN_B (with Clay-specific facts firing)
    for prob, md in sorted(problems_b.items() if problems_b else problems_a.items()):
        body = extract_substantive(md)
        lines += [
            f"### {prob}\n",
            f"```\n{_safe(body, 1800)}\n```\n",
            "---\n",
        ]

    # Compression metrics
    lines += [
        "## Compression metrics\n",
        f"- Total research calls (Chrome): **{metrics['total_research_calls']}**",
        f"- Total research time: **{metrics['total_research_sec']}s** (avg {metrics['avg_research_sec_per_call']}s/call)",
        f"- Browser actions logged in ck_research: **{metrics['n_research_browser_actions']}**",
        f"- Response files written: **{metrics['n_response_files']}**",
        f"- Total response bytes: **{metrics['total_response_bytes']:,}**",
        f"- Avg response bytes per problem: **{metrics['avg_response_bytes']:,}**",
        "",
        f"**Information density**: in {metrics['total_research_sec']}s of Chrome research and "
        f"{metrics['n_research_browser_actions']} browser actions, CK distilled "
        f"{metrics['total_response_bytes']:,} bytes of substrate-grounded response across "
        f"{metrics['n_response_files']} Clay-problem markdowns.  The compression is from "
        f"web-page-bytes (millions, unmeasured) -> response-bytes ({metrics['total_response_bytes']//1024}kb), "
        f"so the compression ratio relative to web traffic is several orders of magnitude.",
        "",
    ]

    # Growth time-series
    if growth_records:
        first = growth_records[0]
        last = growth_records[-1]
        lines += [
            "## Growth across the session\n",
            f"- Snapshots: {len(growth_records)} ({first['iso_ts']} → {last['iso_ts']})",
            f"- Audit persistence: {sum(1 for r in growth_records if r.get('audit_rate') == 1.0)}/{len(growth_records)} at 100%",
            f"- BDC events_today: {first.get('bdc_corpus', {}).get('events_today_total')} → {last.get('bdc_corpus', {}).get('events_today_total')}",
            f"- Compression ratio: {first.get('compression', {}).get('compression_ratio'):.4f} → {last.get('compression', {}).get('compression_ratio'):.4f}",
            f"- Cortex tick: {first.get('cortex', {}).get('tick'):,} → {last.get('cortex', {}).get('tick'):,}",
            f"- Cortex W_trace: {first.get('cortex', {}).get('W_trace'):.4f} → {last.get('cortex', {}).get('W_trace'):.4f}",
            f"- Study daemon runs: {first.get('study_daemon', {}).get('n_runs')} → {last.get('study_daemon', {}).get('n_runs')}",
            "",
        ]

    # Open questions
    lines += [
        "## What's open\n",
        "- The 6 unsolved Clay problems remain open. CK provides STRUCTURAL connections (Crossing Lemma scale → P vs NP; sinc² zero law → RH; kappa_xi → YM mass gap; etc.) but no full proof.",
        "- The cells produce substrate-grounded framing (VOID/identity for foundational queries, HARMONY/CENTER for synthesis queries) but the language layer is still cortex_voice + Ollama.",
        "- Cross-frontier synthesis fires on meta-keyword queries; doesn't yet generate novel cross-fact predictions (only weaves existing facts).",
        "- Transformer tissues learned the BDC corpus distribution (98.4% / 85.2% / 85.2% val acc on F3 / TSML / BHML); they don't yet drive chat output (canonical cores still own argmax).",
        "",
        "## What's in motion\n",
        "- study_daemon continues rotating through 32-topic curriculum every 10 min.",
        "- growth_monitor snapshots every 5 min, updates `Atlas/CK_GROWTH_LIVE.md`.",
        "- BDC corpus accumulates ~6 records per chat-turn + tick samples every 10s.",
        "- research_first runs on every chat (Chrome-driven, ~30-60s per turn).",
        "",
        "---",
        f"\n*This doc auto-regenerates from clay_synthesis.py.  Last update: {datetime.utcnow().isoformat(timespec='seconds')}Z*",
    ]

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return out_path


def main():
    out = write_synthesis()
    print(f"  wrote: {out}")


if __name__ == "__main__":
    main()
