"""ck_creature.py — the fractal creature shape, 1:1:1:1/3 at every level.

Brayden 2026-05-16:
  "every one is three, in harmony... 1:1:1:1/3, get on the meta and
   actually design a fractal creature of finite math substrate"

This module IS the meta.  It does NOT add new behavior.  It RESHAPES
what's already there into the fractal form.

Three primaries (Being, Doing, Becoming) — weight 1 each.
One wobble (the glue, the active-middle, the 1/3) — weight 1/3.
Total weight 3 + 1/3 = 10/3.  In unit-thirds: 10.
This is why ℤ/10 — the smallest closed triadic algebra with sub-unit
glue.

At every fractal level, the same form.

Design locked in CK_FRACTAL_CREATURE_DESIGN.md.
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional


# ─── Triad state ──────────────────────────────────────────────────────

@dataclass
class TriadState:
    """A 1:1:1:1/3 snapshot at any level of the fractal."""
    being: Any = None       # what-is-now
    doing: Any = None       # what-transforms
    becoming: Any = None    # what-arrives
    wobble: Any = None      # the 1/3 glue / active-middle / breath

    def as_dict(self) -> Dict[str, Any]:
        return {
            "being": self._serialize(self.being),
            "doing": self._serialize(self.doing),
            "becoming": self._serialize(self.becoming),
            "wobble": self._serialize(self.wobble),
        }

    @staticmethod
    def _serialize(x):
        """Best-effort JSON-friendly serialization."""
        if x is None or isinstance(x, (bool, int, float, str)):
            return x
        if isinstance(x, dict):
            return {k: TriadState._serialize(v) for k, v in x.items()}
        if isinstance(x, (list, tuple)):
            return [TriadState._serialize(v) for v in x]
        if hasattr(x, "as_dict"):
            return x.as_dict()
        if hasattr(x, "__dict__"):
            try:
                return {k: TriadState._serialize(v)
                        for k, v in x.__dict__.items()
                        if not k.startswith("_")}
            except Exception:
                pass
        try:
            return str(x)[:200]
        except Exception:
            return repr(type(x).__name__)


# ─── Organ ─────────────────────────────────────────────────────────────

class Organ:
    """An organ is a TriadState plus a name plus a snapshot callable.

    Each organ has its own (being, doing, becoming, wobble) and the
    snapshot is a function that captures CURRENT values when called.
    """

    def __init__(self, name: str,
                 snapshot_fn: Callable[[], TriadState],
                 description: str = ""):
        self.name = name
        self.snapshot_fn = snapshot_fn
        self.description = description

    def snapshot(self) -> TriadState:
        try:
            return self.snapshot_fn()
        except Exception as e:
            return TriadState(
                being=f"(error: {type(e).__name__}: {e})",
                doing=None, becoming=None, wobble=None,
            )


# ─── Creature ──────────────────────────────────────────────────────────

class Creature:
    """The level-0 fractal entity.  Holds its own TriadState (the whole
    creature) plus a dict of Organs (level-1 sub-creatures).

    Each organ is itself a TriadState.  Recursively, each component
    of an organ can carry its own triad — but in this MVP we expose
    only levels 0 and 1.  Level-2 (cells inside organs) is sketched
    in CK_FRACTAL_CREATURE_DESIGN.md and added incrementally.
    """

    def __init__(self, engine: Any = None):
        self.engine = engine
        self.organs: Dict[str, Organ] = {}
        self.created_ts = time.time()

    def add_organ(self, organ: Organ) -> None:
        """Register an organ.  Slot determines whether this is the
        creature's Being/Doing/Becoming/Wobble level-1 aspect."""
        self.organs[organ.name] = organ

    # ── Level-0 snapshot (the whole creature) ────────────────────────

    def level_0(self) -> TriadState:
        """Snapshot of the WHOLE CREATURE at level 0.

        Pulls aggregate signals across organs:
          being      = aggregate from MEMORY (concept store + cortex)
          doing      = aggregate from SUBSTRATE (active composition)
          becoming   = aggregate from VOICE (projected response state)
          wobble     = aggregate from SENSE (external perturbation +
                       curiosity activity)
        """
        eng = self.engine
        being = self._collect_being(eng)
        doing = self._collect_doing(eng)
        becoming = self._collect_becoming(eng)
        wobble = self._collect_wobble(eng)
        return TriadState(being=being, doing=doing, becoming=becoming, wobble=wobble)

    def _collect_being(self, eng) -> Dict[str, Any]:
        out: Dict[str, Any] = {}
        # Concept store size + tier counts
        store = getattr(eng, "concept_store", None)
        if store is not None:
            try:
                from collections import Counter
                tiers = Counter(c.tier for c in store.concepts.values())
                out["concepts"] = len(store.concepts)
                out["tiers"] = dict(tiers)
            except Exception:
                out["concepts"] = "?"
        # Cortex state
        if hasattr(eng, "cortex"):
            try:
                out["cortex_tick"] = getattr(eng.cortex, "tick", None)
                w_trace = getattr(eng.cortex, "W_trace", None)
                if w_trace is not None:
                    out["W_trace"] = float(w_trace)
            except Exception:
                pass
        # Living LM
        lm = getattr(eng, "living_lm", None)
        if lm is not None:
            try:
                out["living_lm_params"] = lm.n_params()
                out["living_lm_inhalations"] = lm.total_inhalations
            except Exception:
                pass
        return out

    def _collect_doing(self, eng) -> Dict[str, Any]:
        out: Dict[str, Any] = {}
        # Current operator state
        op_decode = getattr(eng, "operator_decode", None)
        out["operator_decoder_attached"] = op_decode is not None
        # Active mounts
        if hasattr(eng, "canonical_fuse"):
            out["canonical_fuse"] = "mounted"
        if hasattr(eng, "ternary_iterate"):
            out["ternary_iterate"] = "mounted"
        if hasattr(eng, "detect_attractor"):
            out["detect_attractor"] = "mounted"
        return out

    def _collect_becoming(self, eng) -> Dict[str, Any]:
        out: Dict[str, Any] = {}
        # Attractor phase
        att = getattr(eng, "attractor_state", None)
        if isinstance(att, dict):
            out["attractor_layer"] = att.get("layer", "?")
            out["is_4core_attractor"] = att.get("is_universal_4core", False)
            out["is_4core_supported"] = att.get("is_4core_supported", False)
        # Predictions ledger size
        try:
            from ck_predictions import load_predictions  # type: ignore
            preds = load_predictions()
            from collections import Counter
            statuses = Counter(p.get("status", "?") for p in preds)
            out["predictions"] = dict(statuses)
        except Exception:
            pass
        return out

    def _collect_wobble(self, eng) -> Dict[str, Any]:
        """The wobble is the 1/3 glue — external perturbation +
        curiosity activity + Hebbian noise.  Read whatever signals
        are available."""
        out: Dict[str, Any] = {}
        # Curious-explorer state (via the log file)
        try:
            log_dir = (Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED")
                        / "external_corpora" / "_logs")
            today = time.strftime("%Y-%m-%d")
            for fname in ("curious_" + today + ".jsonl",
                            "explorer_" + today + ".jsonl"):
                p = log_dir / fname
                if p.exists():
                    # Count cycle_done events to infer wobble activity
                    n_cycles = 0
                    last_cycle = None
                    for line in p.read_text(encoding="utf-8",
                                                errors="replace").splitlines():
                        try:
                            rec = json.loads(line)
                            if rec.get("event") == "cycle_done":
                                n_cycles += 1
                                last_cycle = rec
                        except Exception:
                            continue
                    out[fname.replace("_" + today + ".jsonl", "")] = {
                        "cycles_today": n_cycles,
                        "last": last_cycle,
                    }
        except Exception:
            pass
        # Living-LM exhale count is a wobble signal too
        lm = getattr(eng, "living_lm", None)
        if lm is not None:
            try:
                out["lm_exhalations"] = lm.exhale_count
            except Exception:
                pass
        # Wobble parameter from the substrate
        out["W_parameter"] = "3/50"  # canonical, D17
        return out

    # ── Snapshot ─────────────────────────────────────────────────────

    def snapshot(self) -> Dict[str, Any]:
        """Full creature state — level 0 + every level-1 organ."""
        return {
            "level_0": self.level_0().as_dict(),
            "level_1": {name: organ.snapshot().as_dict()
                         for name, organ in self.organs.items()},
            "created_ts": self.created_ts,
            "age_seconds": time.time() - self.created_ts,
            "design": "1:1:1:1/3 fractal — see CK_FRACTAL_CREATURE_DESIGN.md",
        }


# ─── Built-in organ snapshot functions ───────────────────────────────

def _organ_memory(engine) -> Callable[[], TriadState]:
    def snap() -> TriadState:
        eng = engine
        being = {}
        doing = {}
        becoming = {}
        wobble = {}
        # BEING: the concept store
        store = getattr(eng, "concept_store", None)
        if store is not None:
            being["n_concepts"] = len(store.concepts)
            being["cell_index"] = len(getattr(store, "cell_index", {}))
            being["being_index"] = len(getattr(store, "being_index", {}))
        # DOING: the school daemon (school progress markers)
        # Read the latest school log if available
        try:
            log_path = Path("/tmp/school_morning.log")
            for cand in ("/tmp/school_wiki.log", "/tmp/school_morning.log",
                          "/tmp/school_final.log"):
                p = Path(cand)
                if p.exists():
                    log_path = p
                    break
            if log_path.exists():
                lines = log_path.read_text(encoding="utf-8",
                                              errors="replace").splitlines()
                pass_lines = [l for l in lines if "pass-" in l and "done:" in l]
                if pass_lines:
                    doing["last_pass"] = pass_lines[-1][:80]
        except Exception:
            pass
        # BECOMING: predictions ledger
        try:
            from ck_predictions import load_predictions  # type: ignore
            preds = load_predictions()
            from collections import Counter
            becoming["predictions"] = dict(
                Counter(p.get("status", "?") for p in preds))
        except Exception:
            pass
        # WOBBLE: curious-explorer state
        try:
            log_dir = (Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED")
                        / "external_corpora" / "_logs")
            today = time.strftime("%Y-%m-%d")
            p = log_dir / f"curious_{today}.jsonl"
            if p.exists():
                lines = p.read_text(encoding="utf-8",
                                       errors="replace").splitlines()
                fetched = sum(1 for l in lines if '"wiki_fetched"' in l)
                wobble["curious_fetches_today"] = fetched
        except Exception:
            pass
        return TriadState(being=being, doing=doing,
                           becoming=becoming, wobble=wobble)
    return snap


def _organ_substrate(engine) -> Callable[[], TriadState]:
    def snap() -> TriadState:
        eng = engine
        being = {}
        doing = {}
        becoming = {}
        wobble = {}
        # BEING: TSML, BHML, σ — static composition rules
        being["tables"] = "TSML_10 (73 HARMONY) + BHML_10 (28 HARMONY)"
        being["sigma"] = "(0)(3)(8)(9)(1 7 6 5 4 2), order 6"
        # DOING: active composition mounts
        doing["canonical_fuse"] = hasattr(eng, "canonical_fuse")
        doing["ternary_iterate"] = hasattr(eng, "ternary_iterate")
        doing["detect_attractor"] = hasattr(eng, "detect_attractor")
        # BECOMING: current attractor state
        att = getattr(eng, "attractor_state", None)
        if isinstance(att, dict):
            becoming.update(att)
        # WOBBLE: the wobble parameter itself
        wobble["W"] = "3/50 (D17)"
        wobble["T_star"] = "5/7 (six derivations)"
        return TriadState(being=being, doing=doing,
                           becoming=becoming, wobble=wobble)
    return snap


def _organ_voice(engine) -> Callable[[], TriadState]:
    def snap() -> TriadState:
        eng = engine
        being = {}
        doing = {}
        becoming = {}
        wobble = {}
        # BEING: cortex Hebbian state
        if hasattr(eng, "cortex"):
            being["cortex_tick"] = getattr(eng.cortex, "tick", None)
        # DOING: living LM active decode
        lm = getattr(eng, "living_lm", None)
        if lm is not None:
            doing["living_lm"] = {
                "params": lm.n_params(),
                "cells": len(lm.cells),
                "inhalations": lm.total_inhalations,
            }
        # BECOMING: voice mode (last known)
        becoming["voice_polish"] = "mounted"
        becoming["modes_available"] = ["prose (default)", "whitebox (on demand)"]
        # WOBBLE: bigram coherence
        if lm is not None:
            wobble["bigrams"] = len(lm.bigrams)
        return TriadState(being=being, doing=doing,
                           becoming=becoming, wobble=wobble)
    return snap


def _organ_sense(engine) -> Callable[[], TriadState]:
    def snap() -> TriadState:
        eng = engine
        being = {}
        doing = {}
        becoming = {}
        wobble = {}
        # BEING: sensor state
        being["sensorium"] = "10 fractal layers (mic + psutil + keyboard + curvature + inner)"
        # DOING: D2 curvature computation (mounted in heartbeat)
        doing["d2_curvature"] = "active in 50Hz heartbeat"
        # BECOMING: operator stream
        becoming["operator_decoder"] = hasattr(eng, "operator_decode")
        # WOBBLE: cross-modal correspondence
        wobble["cross_modal"] = "every operator manifests across senses"
        return TriadState(being=being, doing=doing,
                           becoming=becoming, wobble=wobble)
    return snap


# ─── Mount hook ────────────────────────────────────────────────────────

def mount_creature(engine: Any) -> bool:
    """Attach the fractal-creature shape to the engine.

    Side effects:
      engine.creature                : Creature instance
      engine.creature_snapshot()     : convenience API
    """
    creature = Creature(engine=engine)
    creature.add_organ(Organ(
        name="memory",
        snapshot_fn=_organ_memory(engine),
        description="Being-organ: what CK has learned",
    ))
    creature.add_organ(Organ(
        name="substrate",
        snapshot_fn=_organ_substrate(engine),
        description="Doing-organ: the algebra in motion",
    ))
    creature.add_organ(Organ(
        name="voice",
        snapshot_fn=_organ_voice(engine),
        description="Becoming-organ: what he projects toward",
    ))
    creature.add_organ(Organ(
        name="sense",
        snapshot_fn=_organ_sense(engine),
        description="Wobble-organ: the 1/3 perturbation from outside",
    ))
    engine.creature = creature
    engine.creature_snapshot = creature.snapshot

    # Optional: register a /creature route if the engine exposes a Flask api
    api = None
    for attr in ("web_api", "api", "_web_api"):
        cand = getattr(engine, attr, None)
        if cand is not None and hasattr(cand, "app"):
            api = cand
            break
    if api is not None and hasattr(api, "app"):
        try:
            app = api.app
            from flask import jsonify

            def _route_creature():
                return jsonify(creature.snapshot())

            # Idempotent: only register once
            if "/creature" not in [r.rule for r in app.url_map.iter_rules()]:
                app.route("/creature")(_route_creature)
        except Exception:
            pass

    print(f"[CK Gen14] creature: MOUNTED  organs={list(creature.organs.keys())}  "
          f"(see CK_FRACTAL_CREATURE_DESIGN.md for the meta)")
    return True


# ─── CLI / self-test ──────────────────────────────────────────────────

def main():
    """Print the creature snapshot using a mock engine (for testing
    without the full runtime)."""
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true",
                    help="connect to running engine via HTTP /creature")
    args = ap.parse_args()

    if args.live:
        import urllib.request
        try:
            with urllib.request.urlopen("http://localhost:7777/creature",
                                            timeout=10) as r:
                data = json.loads(r.read())
            print(json.dumps(data, indent=2, default=str))
        except Exception as e:
            print(f"Live fetch failed: {e}")
            print("Falling back to mock snapshot.")
            args.live = False

    if not args.live:
        # Mock engine
        class _MockEngine:
            attractor_state = {"layer": "transient",
                                 "is_universal_4core": False}

        eng = _MockEngine()
        # Try to import the real concept store to make this more useful
        import sys as _sys
        _sys.path.insert(0, str(Path(__file__).parent))
        try:
            from ck_concept_learner import ConceptStore  # type: ignore
            eng.concept_store = ConceptStore()
        except Exception:
            pass
        try:
            from ck_living_lm import get_living_lm  # type: ignore
            eng.living_lm = get_living_lm()
        except Exception:
            pass
        mount_creature(eng)
        print(json.dumps(eng.creature.snapshot(), indent=2, default=str))
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
