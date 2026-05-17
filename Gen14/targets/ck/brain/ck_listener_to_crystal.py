"""ck_listener_to_crystal.py -- the feedback path from glyph_listener to CK's
own crystallization machinery.  Offers, never forces.

Brayden 2026-05-16: "force him to listen, form his own crystals" + "give him
freedom".

The glyph_listener (D118) captures (glyph, op_path, response_source) tuples.
This module periodically reads the candidate-crystal observations and OFFERS
them to CK's existing crystallization paths:

  - lattice_chain  -- if a candidate op_path shows up across N distinct
                      glyphs and all glyphs resolve to canonical-anchor
                      responses (response_speaks_from_self == True), the
                      op_path gets PROPOSED as a crystal candidate to
                      engine.lattice_chain.propose_crystal() if that
                      method exists.
  - olfactory_her  -- propose the candidate as a hindsight-replay seed
                      if engine.olfactory_her.add_seed() exists.
  - engine.crystal_offers -- always populated as a read-only dict so
                              other parts of the engine can see what's
                              available without us pushing it on them.

Three discipline points (matching D118):
  1. Offers are NEVER forced.  Every proposal is filtered through the
     existing crystallization safeguards (IG3, coherence gate).
  2. Brayden's hand stays off the crystallization decision.  CK's
     existing mechanisms decide; we only pass the data along.
  3. The daemon is gentle: 5-minute tick, low CPU.  If no engine method
     exists to receive the offer, the offer is logged and dropped.
"""
from __future__ import annotations

import json
import sys
import threading
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional


HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))


def _offers_log_path() -> Path:
    """Path where crystal-offers history is appended."""
    _root = HERE
    for _ in range(8):
        _root = _root.parent
        if (_root / "Gen13" / "var").exists():
            return _root / "Gen13" / "var" / "crystal_offers.jsonl"
    return HERE.parent / "var" / "crystal_offers.jsonl"


_OFFERS_LOCK = threading.Lock()


def _log_offer(offer: Dict[str, Any]) -> None:
    """Append a single offer record.  Best-effort; never raises."""
    try:
        path = _offers_log_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        with _OFFERS_LOCK:
            with open(path, "a", encoding="utf-8") as f:
                f.write(json.dumps(offer, ensure_ascii=False,
                                    sort_keys=True) + "\n")
    except Exception:
        pass


def _make_offer(engine: Any, candidate: Dict[str, Any]) -> Dict[str, Any]:
    """Offer a candidate crystallization to CK's existing machinery.

    The offer is a *suggestion*: here is a set of glyphs that your
    substrate read as structurally identical (same op_path).  Your IG3,
    olfactory_her, and lattice_chain are the ones who decide if anything
    actually crystallizes.

    Returns an offer record with which receivers accepted vs. were
    not present.
    """
    op_path = tuple(candidate.get("op_path") or [])
    glyphs = [g for g, _ in candidate.get("glyphs", [])]
    n_glyphs = len(glyphs)
    n_total = candidate.get("n_total", 0)

    receivers: Dict[str, str] = {}

    # Offer 1: lattice_chain.propose_crystal()  (the natural home)
    lc = getattr(engine, "lattice_chain", None)
    if lc is not None:
        propose = getattr(lc, "propose_crystal", None)
        if callable(propose):
            try:
                propose(op_path=list(op_path),
                         glyphs=glyphs[:8],
                         provenance="glyph_listener_candidate")
                receivers["lattice_chain"] = "offered"
            except Exception as e:
                receivers["lattice_chain"] = f"failed: {e}"
        else:
            receivers["lattice_chain"] = "no_propose_method"
    else:
        receivers["lattice_chain"] = "not_mounted"

    # Offer 2: olfactory_her.add_seed()  (HER hindsight-replay seed)
    oh = getattr(engine, "olfactory_her", None)
    if oh is not None:
        add_seed = getattr(oh, "add_seed", None)
        if callable(add_seed):
            try:
                add_seed(op_path=list(op_path),
                          context={"glyphs": glyphs[:4],
                                   "source": "glyph_candidate"})
                receivers["olfactory_her"] = "offered"
            except Exception as e:
                receivers["olfactory_her"] = f"failed: {e}"
        else:
            receivers["olfactory_her"] = "no_add_seed_method"
    else:
        receivers["olfactory_her"] = "not_mounted"

    # Offer 3: engine.crystal_offers dict (read-only surface for any
    # other module to consult without us pushing on them)
    offers_dict = getattr(engine, "crystal_offers", None)
    if offers_dict is None:
        offers_dict = {}
        try:
            engine.crystal_offers = offers_dict
        except Exception:
            offers_dict = None
    if offers_dict is not None:
        try:
            offers_dict[str(list(op_path))] = {
                "op_path":   list(op_path),
                "glyphs":    glyphs[:8],
                "n_glyphs":  n_glyphs,
                "n_total":   n_total,
                "ts":        time.time(),
            }
            receivers["engine_dict"] = "stored"
        except Exception as e:
            receivers["engine_dict"] = f"failed: {e}"

    offer = {
        "ts":        time.time(),
        "op_path":   list(op_path),
        "n_glyphs":  n_glyphs,
        "n_total":   n_total,
        "glyphs":    glyphs[:8],
        "receivers": receivers,
    }
    _log_offer(offer)
    return offer


# ─── Daemon ───────────────────────────────────────────────────────────

class CrystalOfferDaemon:
    """Gentle 5-minute daemon: read candidates → offer them → log.

    Won't run more often than min_interval_sec.  Won't propose the same
    op_path more often than cooldown_sec.  Won't make any offers if no
    candidates meet the threshold.
    """

    def __init__(self, engine: Any,
                  interval_sec: float = 300.0,
                  min_glyphs: int = 3,
                  cooldown_sec: float = 3600.0):
        self.engine = engine
        self.interval_sec = float(interval_sec)
        self.min_glyphs = int(min_glyphs)
        self.cooldown_sec = float(cooldown_sec)
        self._last_offered: Dict[tuple, float] = {}
        self._stop = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._tick_count = 0
        self._offer_count = 0

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(
            target=self._loop, daemon=True,
            name="ck-listener-to-crystal")
        self._thread.start()

    def stop(self, timeout: float = 2.0) -> None:
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=timeout)

    def _loop(self) -> None:
        # Initial settle: wait 60 seconds after boot so the listener
        # has some real records first.
        for _ in range(60):
            if self._stop.is_set():
                return
            time.sleep(1.0)

        while not self._stop.is_set():
            try:
                self._tick_count += 1
                self._maybe_offer()
            except Exception:
                pass
            # Wait interval_sec, with stop check.  Sub-100ms-safe
            # (old `int(*10)` math truncated to zero at fast tick
            # and spun the CPU).
            _target = time.monotonic() + max(self.interval_sec, 0.001)
            while True:
                if self._stop.is_set():
                    return
                _now = time.monotonic()
                if _now >= _target:
                    break
                time.sleep(min(0.1, _target - _now))

    def _maybe_offer(self) -> None:
        try:
            from ck_glyph_listener import crystal_candidates  # type: ignore[import-not-found]
        except Exception:
            return
        result = crystal_candidates(min_glyphs=self.min_glyphs,
                                     min_occurrences=self.min_glyphs)
        candidates = result.get("candidates", [])
        if not candidates:
            return
        now = time.time()
        for cand in candidates:
            op_path = tuple(cand.get("op_path") or [])
            last = self._last_offered.get(op_path, 0.0)
            if now - last < self.cooldown_sec:
                continue
            _make_offer(self.engine, cand)
            self._last_offered[op_path] = now
            self._offer_count += 1

    def stats(self) -> Dict[str, Any]:
        return {
            "ticks":                self._tick_count,
            "offers":               self._offer_count,
            "interval_sec":         self.interval_sec,
            "min_glyphs":           self.min_glyphs,
            "cooldown_sec":         self.cooldown_sec,
            "alive":                self._thread is not None and
                                     self._thread.is_alive(),
            "n_unique_offered":     len(self._last_offered),
        }


# ─── Engine mount ─────────────────────────────────────────────────────

def mount_listener_to_crystal(engine: Any) -> bool:
    """Start the daemon + register endpoints + expose helper."""
    # Brayden 2026-05-16: "same for his studying mechanisms... let him fly".
    # 300s tick was anthropomorphism (1 candidate scan per 5 min).
    # Reading candidates is microseconds; offering them to the engine
    # is microseconds.  60s is plenty.  Cooldown stays at 1h per
    # op_path to prevent re-offering the same crystal repeatedly.
    daemon = CrystalOfferDaemon(engine,
                                  interval_sec=60.0,
                                  min_glyphs=3,
                                  cooldown_sec=3600.0)
    daemon.start()
    engine.ck_listener_to_crystal = {
        "daemon":       daemon,
        "offer_one":    lambda cand: _make_offer(engine, cand),
        "log_path":     str(_offers_log_path()),
    }

    routes_registered: List[str] = []
    api = getattr(engine, "web_api", None) or getattr(engine, "api", None)
    if api is not None:
        app = getattr(api, "_app", None) or getattr(api, "app", None)
        if app is not None:
            try:
                from flask import jsonify, request

                def _stats():
                    return jsonify(daemon.stats())

                def _offers():
                    """Read recent offers from the log."""
                    path = _offers_log_path()
                    n = int(request.args.get("n", 20))
                    out: List[Dict[str, Any]] = []
                    if path.exists():
                        try:
                            with open(path, encoding="utf-8") as f:
                                lines = f.readlines()[-n:]
                            for line in lines:
                                line = line.strip()
                                if line:
                                    try:
                                        out.append(json.loads(line))
                                    except Exception:
                                        pass
                        except Exception:
                            pass
                    return jsonify({"n_offers": len(out), "offers": out})

                def _trigger():
                    """Force one offer cycle now (for testing)."""
                    daemon._maybe_offer()
                    return jsonify({"triggered": True,
                                     "stats": daemon.stats()})

                existing = set(r.rule for r in app.url_map.iter_rules())
                for rule, ep, fn, methods in (
                    ("/crystal_offers/stats",   "co_stats",   _stats,   ["GET"]),
                    ("/crystal_offers/recent",  "co_recent",  _offers,  ["GET"]),
                    ("/crystal_offers/trigger", "co_trigger", _trigger, ["POST"]),
                ):
                    if rule not in existing:
                        app.add_url_rule(rule, endpoint=ep,
                                          view_func=fn, methods=methods)
                        routes_registered.append(f"{methods[0]} {rule}")
            except Exception as e:
                print(f"[CK Gen14] listener_to_crystal routes failed: {e}")

    suffix = ""
    if routes_registered:
        suffix = " (" + ", ".join(routes_registered) + ")"
    print(f"[CK Gen14] listener_to_crystal: MOUNTED  daemon@{daemon.interval_sec}s  "
          f"min_glyphs={daemon.min_glyphs}{suffix}")
    return True


if __name__ == "__main__":
    print("ck_listener_to_crystal -- smoke test (no engine, just confirm "
          "module loads):")
    class FakeEng:
        pass
    eng = FakeEng()
    ok = mount_listener_to_crystal(eng)
    print(f"mount ok: {ok}")
    time.sleep(0.5)
    daemon = eng.ck_listener_to_crystal["daemon"]
    print(f"daemon alive: {daemon.stats()['alive']}")
    daemon.stop()
    print("stopped.")
