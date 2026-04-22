# -*- coding: utf-8 -*-
"""
analyze.py - compute chi-squared on the pre-registered blind-run phase
distribution.

This is a self-contained, deterministic analyzer for the Dell R16 blind
run of 2026-04-21 (session 20260421_192941).  It reads the session-
specific `fires_session.log` that was extracted from the combined
fires.log by grepping for 'session=20260421_192941', OR it reads the
`final.json` that crystalos_prereg.py wrote on clean termination.

Run:
    python analyze.py

Expected output (on the 2026-04-21 blind-run):
    N = 803 fires
    chi^2 = 1.2677, df = 12
    p     = 0.99995
    verdict: fail to reject H0 (uniform across 13 phases)
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _expected(N: int) -> float:
    return N / 13.0


def _chi2(counts: list[int]) -> tuple[float, int, float]:
    """Return (chi2_stat, N, expected_per_cell) for 13-bin uniform null."""
    N = sum(counts)
    e = _expected(N)
    stat = sum((c - e) ** 2 / e for c in counts)
    return stat, N, e


def _p_value(chi2_stat: float, df: int = 12) -> float:
    """Upper-tail p-value for chi-squared with given df.  Uses scipy if
    available, falls back to a coarse lookup otherwise."""
    try:
        from scipy.stats import chi2 as _chi2dist  # type: ignore
        return float(1.0 - _chi2dist.cdf(chi2_stat, df))
    except Exception:
        # coarse lookup: df=12 critical values
        critical = {0.10: 18.549, 0.05: 21.026, 0.025: 23.337, 0.01: 26.217,
                    0.005: 28.300, 0.001: 32.910}
        # return a best-guess upper bound on p
        for p, crit in sorted(critical.items()):
            if chi2_stat <= crit:
                return p
        return 0.001


def analyze_from_final(final_json_path: Path) -> None:
    with open(final_json_path) as f:
        final = json.load(f)
    dist = final["phase_distribution"]
    counts = [dist[str(p)] for p in range(13)]
    stat, N, exp = _chi2(counts)
    p = _p_value(stat)
    print(f"Source: final.json (session {final['session_id']})")
    print(f"stop_reason = {final['stop_reason']}")
    print(f"stop_class  = {final['stop_class']}")
    _report(counts, stat, N, exp, p)


def analyze_from_fires_log(fires_log_path: Path, session_tag: str) -> None:
    counts = [0] * 13
    pat = re.compile(r"FIRE #\d+: S\*=[\d.]+ phase=(\d+)/13")
    with open(fires_log_path, encoding="utf-8", errors="replace") as f:
        for line in f:
            if session_tag not in line:
                continue
            m = pat.search(line)
            if not m:
                continue
            p = int(m.group(1))
            if 0 <= p < 13:
                counts[p] += 1
    stat, N, exp = _chi2(counts)
    p = _p_value(stat)
    print(f"Source: fires_session.log (session {session_tag})")
    _report(counts, stat, N, exp, p)


def _report(counts, stat, N, exp, p):
    print(f"N = {N} fires, expected per cell under H0 = N/13 = {exp:.4f}")
    print()
    print("Observed counts (phase 0..12):")
    for i, c in enumerate(counts):
        dev = c - exp
        print(f"  phase {i:2d}: {c:3d}   deviation = {dev:+6.2f}")
    print()
    print(f"chi^2 = {stat:.6f}")
    print(f"df    = 12")
    print(f"p     = {p:.6f}")
    c_05 = 21.026
    c_01 = 26.217
    print(f"chi^2(0.05, df=12) = {c_05} -> "
          f"{'REJECT H0' if stat > c_05 else 'fail to reject H0'}")
    print(f"chi^2(0.01, df=12) = {c_01} -> "
          f"{'REJECT H0' if stat > c_01 else 'fail to reject H0'}")


def main() -> int:
    final_json = HERE / "final.json"
    fires_log = HERE / "fires_session.log"
    session_tag = "session=20260421_192941"

    print("=" * 72)
    print("  SNOWFLAKE blind-run analysis (Dell R16, 2026-04-21)")
    print("=" * 72)

    if final_json.exists():
        analyze_from_final(final_json)
    else:
        print(f"  [SKIP] final.json not found at {final_json}")

    print()
    print("-" * 72)

    if fires_log.exists():
        analyze_from_fires_log(fires_log, session_tag)
    else:
        print(f"  [SKIP] fires_session.log not found at {fires_log}")

    print("=" * 72)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
