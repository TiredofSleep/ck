"""ck_pc_recommend.py -- CK turns PC-sense readings into plain-English advice.

CK Gen14 module — bridge layer from `ck_pc_sense` (raw classification +
coherence) to user-actionable recommendations.

CK reports what it observes; recommendations are plain English with
explicit tier-tags.  CK NEVER kills, suspends, or changes process
priorities — every recommendation is advisory.

═══════════════════════════════════════════════════════════════════
What this module DOES
═══════════════════════════════════════════════════════════════════

Reads the recent buffer of PCSenseReadings (default last 60 = 1 min
at 1 Hz), looks for patterns, and emits 0..N recommendations as
plain-English strings with priority.  Patterns include:

  - SUSTAINED_HIGH_CPU: top process pegged for > 30 sec
  - MEMORY_PRESSURE:    mem_used > 80% sustained
  - UNBALANCED_LOAD:    high cpu_variance sustained (single core pegged)
  - GREEN_WINDOW:       all-green for > 30 sec → "good for heavy work"
  - MEMORY_LEAK_HINT:   one process growing in memory monotonically
  - PROCESS_STORM:      sudden jump in n_processes (50+ new processes)
  - IDLE_CONFIRMED:     consistent VOID classification → "machine is idle"

Each recommendation has:
  - priority:  INFO / NOTICE / WARN / ALERT
  - category:  cpu / memory / coherence / process
  - tier:      TIER_RECOMMENDATION_HEURISTIC (always — these are heuristics)
  - text:      plain English, 1-3 sentences
  - evidence:  the buffer subset that triggered

═══════════════════════════════════════════════════════════════════
What this module DOES NOT DO
═══════════════════════════════════════════════════════════════════

  - Never executes anything.  Recommendations are STRINGS the user reads.
  - Never modifies process state.
  - Never escalates priority on its own (no "automatic action" tier).
  - No outbound network calls.
  - No persistence beyond an optional JSONL log (user-controllable).

═══════════════════════════════════════════════════════════════════
Honest scope
═══════════════════════════════════════════════════════════════════

The patterns are HEURISTICS based on common Windows/macOS/Linux
behavior.  They are NOT theorems about CPU dynamics.  Treat the
recommendations as "a thoughtful friend looking at Task Manager
with you" — not as a system tuning oracle.  The thresholds (30 sec,
80% mem, etc.) are reasonable defaults; the user can tune.
"""
from __future__ import annotations

import time
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional, Tuple

try:
    from ck_pc_sense import PCSenseReading
except Exception:  # pragma: no cover — module exists in same package
    PCSenseReading = Any  # type: ignore


TIER_RECOMMENDATION_HEURISTIC = "TIER_RECOMMENDATION_HEURISTIC"

# Priority levels (lowest to highest)
INFO, NOTICE, WARN, ALERT = "INFO", "NOTICE", "WARN", "ALERT"


@dataclass
class Recommendation:
    """One plain-English recommendation derived from sense buffer."""
    priority: str            # INFO / NOTICE / WARN / ALERT
    category: str            # cpu / memory / coherence / process
    tier: str                # TIER_RECOMMENDATION_HEURISTIC
    code: str                # short machine-readable code, e.g. SUSTAINED_HIGH_CPU
    text: str                # 1-3 sentence English
    evidence: Dict[str, Any] = field(default_factory=dict)
    ts: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ─── Pattern detectors ────────────────────────────────────────────────

def _sustained_high_cpu(buf: List[Any], threshold: float = 0.80,
                          sustain_sec: float = 30.0) -> List[Recommendation]:
    """Top process pegged > threshold for > sustain_sec consecutive seconds."""
    if not buf:
        return []
    out: List[Recommendation] = []
    # Build per-process timeline
    by_proc: Dict[str, List[Tuple[float, float]]] = defaultdict(list)
    for r in buf:
        for p in r.top_cpu_processes[:3]:
            by_proc[p["name"]].append((r.ts, p.get("pct", 0) / 100.0))
    for name, ticks in by_proc.items():
        if len(ticks) < 5:
            continue
        # Find longest run above threshold
        run_start: Optional[float] = None
        run_max_pct = 0.0
        run_duration = 0.0
        for ts, pct in ticks:
            if pct >= threshold:
                if run_start is None:
                    run_start = ts
                run_duration = ts - run_start
                run_max_pct = max(run_max_pct, pct)
            else:
                if run_duration >= sustain_sec:
                    out.append(Recommendation(
                        priority=WARN if run_max_pct > 0.95 else NOTICE,
                        category="cpu",
                        tier=TIER_RECOMMENDATION_HEURISTIC,
                        code="SUSTAINED_HIGH_CPU",
                        text=(
                            f"{name} has been pegging the CPU "
                            f"({run_max_pct*100:.0f}% peak) for "
                            f"{run_duration:.0f}s. If it's not a task you "
                            f"started, consider closing or investigating it."
                        ),
                        evidence={"process": name,
                                   "duration_sec": round(run_duration, 1),
                                   "peak_pct": round(run_max_pct, 3)},
                    ))
                run_start = None
                run_duration = 0.0
                run_max_pct = 0.0
        # Edge case: still in a run at end of buffer
        if run_duration >= sustain_sec:
            out.append(Recommendation(
                priority=WARN if run_max_pct > 0.95 else NOTICE,
                category="cpu",
                tier=TIER_RECOMMENDATION_HEURISTIC,
                code="SUSTAINED_HIGH_CPU_ONGOING",
                text=(
                    f"{name} is currently pegging the CPU "
                    f"({run_max_pct*100:.0f}% peak) — {run_duration:.0f}s "
                    f"sustained so far. Investigate if unexpected."
                ),
                evidence={"process": name, "ongoing": True,
                           "duration_sec": round(run_duration, 1)},
            ))
    return out


def _memory_pressure(buf: List[Any], threshold: float = 0.80,
                       sustain_sec: float = 30.0) -> List[Recommendation]:
    """mem_used > threshold sustained."""
    if not buf:
        return []
    out: List[Recommendation] = []
    over = [(r.ts, r.mem_used, r.mem_available_gb) for r in buf if r.mem_used >= threshold]
    if not over:
        return []
    duration = over[-1][0] - over[0][0]
    if duration < sustain_sec:
        return []
    peak = max(o[1] for o in over)
    available_gb = over[-1][2]
    # Find the worst memory hog at the end of the run
    last = buf[-1]
    top_mem = last.top_mem_processes[:1]
    hog_text = ""
    if top_mem:
        h = top_mem[0]
        hog_text = (f" Top memory hog: {h['name']} at "
                    f"{h.get('pct_gb', 0):.2f} GB.")
    out.append(Recommendation(
        priority=ALERT if peak > 0.90 else WARN,
        category="memory",
        tier=TIER_RECOMMENDATION_HEURISTIC,
        code="MEMORY_PRESSURE",
        text=(
            f"Memory at {peak*100:.0f}% used for {duration:.0f}s — "
            f"{available_gb:.2f} GB available.{hog_text} "
            f"Consider closing some apps; risk of OS swap-thrash above 95%."
        ),
        evidence={"peak_pct": round(peak, 3),
                   "duration_sec": round(duration, 1),
                   "available_gb": round(available_gb, 2)},
    ))
    return out


def _unbalanced_load(buf: List[Any], var_threshold: float = 0.10,
                       sustain_sec: float = 30.0) -> List[Recommendation]:
    """High cpu_variance sustained = one core pegged while others idle."""
    if not buf:
        return []
    over = [r.ts for r in buf if r.cpu_variance >= var_threshold]
    if not over:
        return []
    duration = over[-1] - over[0]
    if duration < sustain_sec:
        return []
    last = buf[-1]
    out = [Recommendation(
        priority=NOTICE,
        category="cpu",
        tier=TIER_RECOMMENDATION_HEURISTIC,
        code="UNBALANCED_LOAD",
        text=(
            f"Load is unbalanced across cores ({duration:.0f}s sustained) — "
            f"a single-threaded task is likely pegging one core. "
            f"Mean overall CPU is only {last.cpu_overall*100:.0f}%, but "
            f"variance is {last.cpu_variance:.3f}. "
            f"If it's a compute task that supports threading, check its config."
        ),
        evidence={"cpu_variance": round(last.cpu_variance, 4),
                   "cpu_overall": round(last.cpu_overall, 4),
                   "duration_sec": round(duration, 1)},
    )]
    return out


def _green_window(buf: List[Any], sustain_sec: float = 30.0) -> List[Recommendation]:
    """All-green for sustained period = good for heavy work."""
    if not buf:
        return []
    greens = [r.ts for r in buf if r.coherence_band == "GREEN"]
    if len(greens) < 5:
        return []
    if len(greens) != len(buf):
        return []  # not all green
    duration = greens[-1] - greens[0]
    if duration < sustain_sec:
        return []
    return [Recommendation(
        priority=INFO,
        category="coherence",
        tier=TIER_RECOMMENDATION_HEURISTIC,
        code="GREEN_WINDOW",
        text=(
            f"All-green coherence for {duration:.0f}s. Good window for "
            f"heavy compute, batch jobs, or anything CPU-intensive you "
            f"have queued."
        ),
        evidence={"duration_sec": round(duration, 1),
                   "n_readings_green": len(greens)},
    )]


def _memory_leak_hint(buf: List[Any], min_growth_gb: float = 0.5,
                       window_sec: float = 60.0) -> List[Recommendation]:
    """Single process grows monotonically over the window."""
    if len(buf) < 10:
        return []
    duration = buf[-1].ts - buf[0].ts
    if duration < window_sec:
        return []
    # Build per-process mem timeline
    by_proc: Dict[str, List[Tuple[float, float]]] = defaultdict(list)
    for r in buf:
        for p in r.top_mem_processes[:5]:
            by_proc[p["name"]].append((r.ts, p.get("pct_gb", 0)))
    out: List[Recommendation] = []
    for name, ticks in by_proc.items():
        if len(ticks) < 5:
            continue
        start_mem = ticks[0][1]
        end_mem = ticks[-1][1]
        growth = end_mem - start_mem
        if growth < min_growth_gb:
            continue
        # Check monotonicity: at least 80% of consecutive pairs are non-decreasing
        non_dec = sum(
            1 for i in range(1, len(ticks)) if ticks[i][1] >= ticks[i-1][1] - 0.01
        )
        if non_dec / max(1, len(ticks) - 1) < 0.8:
            continue
        out.append(Recommendation(
            priority=WARN,
            category="memory",
            tier=TIER_RECOMMENDATION_HEURISTIC,
            code="MEMORY_LEAK_HINT",
            text=(
                f"{name} grew from {start_mem:.2f} GB to {end_mem:.2f} GB "
                f"over {duration:.0f}s (Δ +{growth:.2f} GB, "
                f"mostly monotonic). Possible memory leak. Consider "
                f"restarting that process if it's not actively loading data."
            ),
            evidence={"process": name,
                       "start_gb": round(start_mem, 3),
                       "end_gb": round(end_mem, 3),
                       "growth_gb": round(growth, 3),
                       "duration_sec": round(duration, 1)},
        ))
    return out


def _idle_confirmed(buf: List[Any], min_seconds: float = 30.0
                     ) -> List[Recommendation]:
    """Sustained VOID classification."""
    if len(buf) < 5:
        return []
    voids = [r.ts for r in buf if r.op_name == "VOID"]
    if len(voids) != len(buf):
        return []
    duration = voids[-1] - voids[0]
    if duration < min_seconds:
        return []
    return [Recommendation(
        priority=INFO,
        category="coherence",
        tier=TIER_RECOMMENDATION_HEURISTIC,
        code="IDLE_CONFIRMED",
        text=(
            f"Machine has been idle for {duration:.0f}s. "
            f"Safe to start anything; no contention."
        ),
        evidence={"duration_sec": round(duration, 1)},
    )]


def _process_storm(buf: List[Any], jump: int = 50) -> List[Recommendation]:
    """Sudden jump in n_processes (50+ new processes in one tick)."""
    if len(buf) < 2:
        return []
    out: List[Recommendation] = []
    for i in range(1, len(buf)):
        delta = buf[i].n_processes - buf[i-1].n_processes
        if delta >= jump:
            out.append(Recommendation(
                priority=NOTICE,
                category="process",
                tier=TIER_RECOMMENDATION_HEURISTIC,
                code="PROCESS_STORM",
                text=(
                    f"+{delta} new processes appeared at "
                    f"t={int(buf[i].ts - buf[0].ts)}s (total now "
                    f"{buf[i].n_processes}). Possible app launch, "
                    f"installer, or background job kickoff."
                ),
                evidence={"delta": delta,
                           "total_after": buf[i].n_processes,
                           "ts": buf[i].ts},
            ))
    return out


# All detectors in priority order (most actionable first)
_DETECTORS = [
    _sustained_high_cpu,
    _memory_pressure,
    _unbalanced_load,
    _memory_leak_hint,
    _process_storm,
    _green_window,
    _idle_confirmed,
]


def recommendations_for(buf: List[Any]) -> List[Recommendation]:
    """Run all detectors over the buffer and return collected
    recommendations (deduplicated by code)."""
    out: List[Recommendation] = []
    seen_codes = set()
    for det in _DETECTORS:
        try:
            for rec in det(buf):
                if rec.code in seen_codes:
                    continue
                seen_codes.add(rec.code)
                out.append(rec)
        except Exception:
            continue
    # Sort by priority (ALERT > WARN > NOTICE > INFO)
    priority_order = {ALERT: 0, WARN: 1, NOTICE: 2, INFO: 3}
    out.sort(key=lambda r: priority_order.get(r.priority, 99))
    return out


# ─── Engine mount ─────────────────────────────────────────────────

def mount_pc_recommend(engine: Any) -> bool:
    """Attach the recommendation bridge to engine + register Flask routes.

    Endpoints:
      GET /pc/recommend           — recommendations from current buffer
      GET /pc/recommend?n=N       — recommendations from last N readings
      GET /pc/recommend/info      — module philosophy
    """
    pc_sense = getattr(engine, "ck_pc_sense", None)
    if not pc_sense:
        print("[CK Gen14] mount_pc_recommend: ck_pc_sense not mounted; "
              "skipping. Mount ck_pc_sense first.")
        return False

    daemon = pc_sense.get("daemon")
    if daemon is None:
        print("[CK Gen14] mount_pc_recommend: no daemon on ck_pc_sense; "
              "skipping.")
        return False

    engine.ck_pc_recommend = {
        "recommendations_for": recommendations_for,
        "detectors": [d.__name__ for d in _DETECTORS],
    }

    api = getattr(engine, "web_api", None) or getattr(engine, "api", None)
    if api is not None:
        app = getattr(api, "_app", None) or getattr(api, "app", None)
        if app is not None:
            try:
                from flask import jsonify, request  # type: ignore

                def _recommend():
                    n = request.args.get("n", default=None, type=int)
                    buf = daemon.history(n=n)
                    recs = recommendations_for(buf)
                    return jsonify({
                        "n_readings_analyzed": len(buf),
                        "n_recommendations": len(recs),
                        "recommendations": [r.to_dict() for r in recs],
                    })

                def _info():
                    return jsonify({
                        "module": "ck_pc_recommend",
                        "philosophy": ("CK reports patterns; user acts. "
                                        "Every recommendation tagged "
                                        "TIER_RECOMMENDATION_HEURISTIC."),
                        "scope": ("Heuristics, not theorems. CK NEVER "
                                   "kills, suspends, or modifies "
                                   "processes."),
                        "detectors": [d.__name__ for d in _DETECTORS],
                        "priority_levels": [INFO, NOTICE, WARN, ALERT],
                        "endpoints": ["GET /pc/recommend",
                                       "GET /pc/recommend?n=N",
                                       "GET /pc/recommend/info"],
                    })

                existing = {r.rule for r in app.url_map.iter_rules()}
                for rule, ep, fn, methods in (
                    ("/pc/recommend",      "pc_recommend",      _recommend, ["GET"]),
                    ("/pc/recommend/info", "pc_recommend_info", _info,      ["GET"]),
                ):
                    if rule not in existing:
                        app.add_url_rule(rule, endpoint=ep,
                                          view_func=fn, methods=methods)
            except Exception as e:
                print(f"[CK Gen14] mount_pc_recommend: routes failed: {e}")

    print(f"[CK Gen14] mount_pc_recommend: {len(_DETECTORS)} detectors active")
    return True


# ─── CLI smoke ────────────────────────────────────────────────────

if __name__ == "__main__":
    import time
    from ck_pc_sense import PCSenseDaemon

    print("ck_pc_recommend smoke test")
    print("=" * 60)
    print()
    print("Step 1: warm up ck_pc_sense for 5 seconds")
    print("-" * 60)
    d = PCSenseDaemon(poll_hz=1.0, buffer_size=60)
    d.start()
    time.sleep(5.5)
    d.stop()
    buf = d.history()
    print(f"  Collected {len(buf)} readings")
    print()
    print("Step 2: run recommendations against the buffer")
    print("-" * 60)
    recs = recommendations_for(buf)
    print(f"  {len(recs)} recommendation(s):")
    for r in recs:
        print(f"  [{r.priority:6s}] [{r.category:10s}] {r.code}")
        print(f"          {r.text}")
        print()
    if not recs:
        print("  (No patterns triggered; machine is unremarkable.)")
    print("Smoke test complete.")
