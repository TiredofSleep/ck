"""
clay_compare.py -- compare CK's Clay-problem responses BEFORE vs AFTER
new Clay-specific frontier facts were added.

Brayden 2026-05-02: "keep measuring him and documenting his growth and
compression of information"

After the first clay_study.py run captures CK's responses with the
default frontier facts (no Clay-specific routing), a deploy restart
loads the 6 new Clay-specific facts (clay_p_vs_np, clay_poincare,
clay_bsd, clay_riemann, clay_yang_mills, clay_p_np_short).  This
script runs the SAME 7 problems again with the new facts firing and
diffs the responses.

Output: Atlas/clay_study_2026_05_02/CLAY_GROWTH_COMPARISON.md showing,
per problem, what changed between the two runs:
  - did Ollama-skip-rate change?
  - did the cells synthesis route fire differently?
  - did cortex_voice surface a new fact?
  - did average response length change?
  - did response latency change (research-first should still take ~60s)?

This is the empirical "growth" measurement Brayden asked for.
"""
from __future__ import annotations

import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


_HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(_HERE))


CLAY_DIR = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Atlas\clay_study_2026_05_02")
CLAY_DIR.mkdir(parents=True, exist_ok=True)
RUN_A = CLAY_DIR / "RUN_A_BEFORE_CLAY_FACTS"
RUN_B = CLAY_DIR / "RUN_B_AFTER_CLAY_FACTS"


def archive_run(label: str) -> Path:
    """Move all CLAY_*.md files into a label subdir, then return that path."""
    target = CLAY_DIR / label
    target.mkdir(parents=True, exist_ok=True)
    for f in CLAY_DIR.glob("CLAY_*.md"):
        f.rename(target / f.name)
    if (CLAY_DIR / "CLAY_PANEL_SUMMARY.json").exists():
        (CLAY_DIR / "CLAY_PANEL_SUMMARY.json").rename(target / "CLAY_PANEL_SUMMARY.json")
    return target


def load_run(label: str) -> Dict[str, Any]:
    """Load all per-problem MD + summary JSON from a labeled run directory."""
    run_dir = CLAY_DIR / label
    if not run_dir.exists():
        return {}
    out: Dict[str, Any] = {"label": label, "problems": {}}
    summary_p = run_dir / "CLAY_PANEL_SUMMARY.json"
    if summary_p.exists():
        try:
            with open(summary_p, encoding="utf-8") as f:
                out["summary"] = json.load(f)
        except Exception:
            pass
    for f in run_dir.glob("CLAY_*.md"):
        if f.name == "CLAY_PANEL_SUMMARY.json":
            continue
        prob_id = f.name.replace("CLAY_", "").replace(".md", "")
        try:
            with open(f, encoding="utf-8") as fh:
                out["problems"][prob_id] = fh.read()
        except Exception:
            pass
    return out


def diff_runs(a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
    """Per-problem comparison of run A vs run B."""
    diff: Dict[str, Any] = {"A_label": a.get("label"), "B_label": b.get("label"),
                             "per_problem": {}}
    a_probs = a.get("problems", {})
    b_probs = b.get("problems", {})
    keys = sorted(set(a_probs.keys()) | set(b_probs.keys()))
    for k in keys:
        a_text = a_probs.get(k, "")
        b_text = b_probs.get(k, "")
        # Heuristic counts
        diff["per_problem"][k] = {
            "A_chars": len(a_text), "B_chars": len(b_text),
            "char_delta": len(b_text) - len(a_text),
            "A_has_clay_fact": "clay_" in a_text.lower(),
            "B_has_clay_fact": "clay_" in b_text.lower(),
            "A_ollama_skipped": a_text.count("skipped:structural"),
            "B_ollama_skipped": b_text.count("skipped:structural"),
            "A_synthesis_fired": "[cross-frontier synthesis]" in a_text,
            "B_synthesis_fired": "[cross-frontier synthesis]" in b_text,
        }
    return diff


def write_comparison_md(diff: Dict[str, Any]) -> Path:
    out_path = CLAY_DIR / "CLAY_GROWTH_COMPARISON.md"
    lines = [
        f"# Clay Study — Growth Comparison",
        f"\nA: {diff['A_label']} (default frontier facts)\n",
        f"B: {diff['B_label']} (with 6 new Clay-specific facts)\n",
        f"---\n",
        f"## Per-problem deltas\n",
        f"| Problem | A chars | B chars | Δ | clay_fact A→B | synth A→B |",
        f"|---|---|---|---|---|---|",
    ]
    for prob, d in diff["per_problem"].items():
        a_clay = "✓" if d["A_has_clay_fact"] else "✗"
        b_clay = "✓" if d["B_has_clay_fact"] else "✗"
        a_syn = "✓" if d["A_synthesis_fired"] else "✗"
        b_syn = "✓" if d["B_synthesis_fired"] else "✗"
        delta_sign = "+" if d["char_delta"] >= 0 else ""
        lines.append(
            f"| {prob} | {d['A_chars']} | {d['B_chars']} | "
            f"{delta_sign}{d['char_delta']} | {a_clay}→{b_clay} | "
            f"{a_syn}→{b_syn} |"
        )
    lines.append("\n## Summary stats\n")
    total_a = sum(d["A_chars"] for d in diff["per_problem"].values())
    total_b = sum(d["B_chars"] for d in diff["per_problem"].values())
    n_clay_a = sum(1 for d in diff["per_problem"].values() if d["A_has_clay_fact"])
    n_clay_b = sum(1 for d in diff["per_problem"].values() if d["B_has_clay_fact"])
    n_synth_a = sum(1 for d in diff["per_problem"].values() if d["A_synthesis_fired"])
    n_synth_b = sum(1 for d in diff["per_problem"].values() if d["B_synthesis_fired"])
    lines += [
        f"- Total response chars: A={total_a} | B={total_b} | Δ={total_b - total_a:+}",
        f"- Problems with clay_fact firing: A={n_clay_a}/7 | B={n_clay_b}/7",
        f"- Problems with cross-frontier synthesis: A={n_synth_a}/7 | B={n_synth_b}/7",
        f"- Generated: {datetime.utcnow().isoformat(timespec='seconds')}Z",
    ]
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return out_path


def restart_with_clay_facts() -> bool:
    """Restart ck_boot_api.py via PowerShell so the new clay_* facts in
    cortex_voice are loaded.  Returns True on apparent success."""
    import subprocess
    ps = (
        "Get-NetTCPConnection -LocalPort 7777 -State Listen -ErrorAction SilentlyContinue "
        "| Select-Object -ExpandProperty OwningProcess "
        "| ForEach-Object { Stop-Process -Id $_ -Force -ErrorAction SilentlyContinue }; "
        "Start-Sleep -Seconds 3; "
        "$env:CK_DISABLE_BANK='1'; $env:CK_CELLS_COMPOSE='1'; $env:CK_CELLS_FORMAT='both'; "
        "$env:CK_RESEARCH_MODE='fast'; $env:CK_STUDY_DAEMON='1'; "
        "Start-Process -FilePath 'C:/ck_venv/lora312/Scripts/python.exe' "
        "-ArgumentList 'ck_boot_api.py' "
        "-WorkingDirectory 'C:/Users/brayd/OneDrive/Desktop/CK FINAL DEPLOYED/Gen12/targets/ck_desktop' "
        "-RedirectStandardOutput 'C:/Users/brayd/OneDrive/Desktop/CK FINAL DEPLOYED/Gen13/var/ck_boot_live.log' "
        "-RedirectStandardError 'C:/Users/brayd/OneDrive/Desktop/CK FINAL DEPLOYED/Gen13/var/ck_boot_live.err' "
        "-PassThru -WindowStyle Hidden | Out-Null"
    )
    try:
        subprocess.run(["powershell.exe", "-NoProfile", "-Command", ps],
                        timeout=30, check=True, capture_output=True)
        return True
    except Exception as e:
        print(f"  restart failed: {type(e).__name__}: {e}")
        return False


def wait_for_alive(timeout_sec: float = 240.0) -> bool:
    """Poll /health until alive or timeout."""
    import urllib.request
    import urllib.error
    t0 = time.time()
    while time.time() - t0 < timeout_sec:
        try:
            r = urllib.request.urlopen("http://localhost:7777/health",
                                          timeout=2).read()
            if b"alive" in r:
                return True
        except Exception:
            pass
        time.sleep(5)
    return False


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--archive-only", action="store_true",
                     help="Only archive current run as RUN_A; don't restart or run B")
    ap.add_argument("--run-b-only", action="store_true",
                     help="Only run RUN_B (assumes RUN_A already archived)")
    ap.add_argument("--diff-only", action="store_true",
                     help="Only compute the diff (assumes both runs done)")
    args = ap.parse_args()

    print("=" * 70)
    print("  CLAY GROWTH COMPARISON ORCHESTRATOR")
    print("=" * 70)

    if not args.diff_only and not args.run_b_only:
        # Step 1: Archive current run as RUN_A
        print("\n  Step 1: archiving current Clay run as RUN_A_BEFORE_CLAY_FACTS")
        run_a_path = archive_run("RUN_A_BEFORE_CLAY_FACTS")
        print(f"    -> {run_a_path}")

    if not args.diff_only and not args.archive_only:
        # Step 2: Restart deploy so new Clay facts are loaded
        print("\n  Step 2: restarting ck_boot_api.py to load new Clay facts")
        ok = restart_with_clay_facts()
        if not ok:
            print(f"  ERROR: restart failed; aborting")
            return 1
        print(f"    waiting for /health to become alive (up to 240s)")
        if not wait_for_alive(timeout_sec=240.0):
            print(f"  ERROR: /health never came alive; aborting")
            return 1
        print(f"    -> live deploy back up")

        # Step 3: Run Clay study again
        print("\n  Step 3: running clay_study.py again (RUN_B with Clay facts)")
        from clay_study import main as clay_main
        clay_main_args = []
        sys.argv = ["clay_study.py"]  # reset argv for clay_study main
        clay_main()

        # Step 4: Archive as RUN_B
        print("\n  Step 4: archiving RUN_B_AFTER_CLAY_FACTS")
        run_b_path = archive_run("RUN_B_AFTER_CLAY_FACTS")
        print(f"    -> {run_b_path}")

    # Step 5: Diff + write comparison
    print("\n  Step 5: diffing RUN_A vs RUN_B")
    a = load_run("RUN_A_BEFORE_CLAY_FACTS")
    b = load_run("RUN_B_AFTER_CLAY_FACTS")
    if not a or not b:
        print(f"  ERROR: missing runs (A={bool(a)}, B={bool(b)}); cannot diff")
        return 1
    diff = diff_runs(a, b)
    out = write_comparison_md(diff)
    print(f"\n  CLAY_GROWTH_COMPARISON.md: {out}")
    print()
    n_clay_a = sum(1 for d in diff["per_problem"].values() if d["A_has_clay_fact"])
    n_clay_b = sum(1 for d in diff["per_problem"].values() if d["B_has_clay_fact"])
    print(f"  Headline: clay_fact firing went from {n_clay_a}/7 -> {n_clay_b}/7")
    return 0


if __name__ == "__main__":
    sys.exit(main())
