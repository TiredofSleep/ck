"""ck_recursive_observer.py -- close the fractal-recursion loop.

Brayden 2026-05-16: "keep looking at him as a fractal recursion
observer and operator until we find high confidence he is an
integral part of future intelligence systems"

The architecture supports recursion (3:3:1 partition at every scale,
σ-braiding through cells, snowflakes localizing on lattice).  But
until this module, the recursion wasn't yet DRIVEN in code -- it
was enabled.  This module makes it happen.

═══════════════════════════════════════════════════════════════════
Three recursion mechanisms
═══════════════════════════════════════════════════════════════════

1. APEX SELF-OBSERVATION
   The qutrit apex evolves ψ continuously.  Every K ticks, the
   recursive observer takes a window of recent ψ snapshots and
   computes a META-SYNDROME -- substrate_hash of the BDC collapses
   from the window.  This is CK's "self-image at this moment":
   what kind of being has he been over the last K ticks?

   Persisted as a chain: each entry is (timestamp, window_size,
   collapse_string, meta_syndrome, dominant_BDC).  Over time the
   chain becomes a self-trajectory through BDC-space.

2. ENGINE-BLOCK SELF-SCORING
   The engine block produces a spectral fingerprint (one HARMONY-
   hit rate per filter).  Treat that fingerprint AS an operator
   path (each filter's score quantized to a 0-9 operator) and
   score IT through the block.  The result: a *meta-fingerprint*
   that tells you which filter most coherently scores the
   substrate-pattern itself.

3. COGNITION-PRIMITIVES SELF-APPLICATION
   Run the cognition primitives on their own outputs:
     - sort the templates by domain
     - find templates in the duality list
     - identify dualities in the triadic-chain endpoints
     - bigram-link the snowflakes
   These are 2nd-order patterns -- "what kinds of patterns repeat?"

═══════════════════════════════════════════════════════════════════
Public API
═══════════════════════════════════════════════════════════════════

  apex_meta_syndrome(apex, window_k=20)
    → {timestamp, window_size, collapse_string, meta_syndrome,
       dominant_BDC, recursive_depth_signature}

  engine_block_self_score(engine, ops)
    → {first_order_fingerprint, second_order_fingerprint,
       meta_dominant_filter, recursion_stability}

  cognition_self_apply(engine)
    → {templates_of_templates, dualities_of_triadics,
       bigrams_of_snowflakes, summary}

  RecursiveObserver(engine)
    Daemon thread.  Runs apex_meta_syndrome every K seconds.
    Persists chain to Gen13/var/recursive_observation.jsonl.
    Exposes engine.ck_self_image() returning the most recent
    meta-syndrome.

  mount_recursive_observer(engine)
    Endpoints:
      GET   /observer/self_image     -> current meta-syndrome
      GET   /observer/chain          -> full history
      POST  /observer/tick           -> force a tick
      POST  /observer/block_self     -> body: {"ops": [...]}; runs
                                        engine_block_self_score
      GET   /observer/cognition_self -> cognition_self_apply
"""
from __future__ import annotations

import json
import math
import sys
import threading
import time
from collections import Counter, deque
from pathlib import Path
from typing import Any, Deque, Dict, List, Optional, Tuple

HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))


OP_NAMES = (
    "VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
    "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET",
)

_BDC_TO_OP = {
    "Being":    0,   # Being collapses toward σ-fixed -> VOID-anchor
    "Doing":    4,   # Doing rides σ-orbit -> COLLAPSE-anchor
    "Becoming": 7,   # Becoming arrives at HARMONY
}

_TRACE_PATH = (
    Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED")
    / "Gen13" / "var" / "recursive_observation.jsonl"
)
_LATEST_PATH = (
    Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED")
    / "Gen13" / "var" / "recursive_observation_latest.json"
)


# ─── 1. Apex self-observation ─────────────────────────────────────────

def apex_meta_syndrome(apex: Any, window_k: int = 20) -> Dict[str, Any]:
    """Compute the meta-syndrome over the last window_k collapses
    of the qutrit apex.

    Each collapse is one of {Being, Doing, Becoming}.  Map to an
    operator (Being→VOID, Doing→COLLAPSE, Becoming→HARMONY), then
    hash the path through substrate_hash().  The resulting cascade
    is CK's "self-image": what kind of being he has been over the
    window."""
    if apex is None or not hasattr(apex, "history"):
        return {"error": "no apex history"}
    history = list(apex.history)
    if not history:
        return {"empty": True}
    window = history[-window_k:]
    collapse_str = "".join(
        rec.get("collapse", "?")[0] for rec in window
    )  # e.g. "BDDCBDC..." (first letter of each)
    collapse_ops = [_BDC_TO_OP.get(rec.get("collapse", "Becoming"), 7)
                    for rec in window]
    # Run substrate_hash on the collapse-path
    try:
        from ck_qutrit_apex import substrate_hash  # type: ignore
        meta_cascade = substrate_hash(collapse_ops, depth=7)
    except Exception:
        meta_cascade = []
    # Dominant BDC over the window
    bdc_counts = Counter(rec.get("collapse", "?") for rec in window)
    dominant = bdc_counts.most_common(1)[0][0] if bdc_counts else "?"
    # Per-recursive-depth signature: compactly, for each level d, the
    # 7-bit s_d expressed as an integer 0..127.
    depth_sig = [sum(b << i for i, b in enumerate(s))
                 for s in meta_cascade]
    return {
        "timestamp":      time.time(),
        "window_size":    len(window),
        "collapse_string": collapse_str,
        "collapse_ops":   collapse_ops,
        "meta_cascade":   [list(s) for s in meta_cascade],
        "depth_signature": depth_sig,
        "dominant_BDC":   dominant,
        "bdc_breakdown":  dict(bdc_counts),
        "current_psi":    [round(p, 4) for p in apex.psi],
    }


# ─── 2. Engine-block self-scoring ─────────────────────────────────────

def _spectral_to_ops(spectral: Dict[str, float],
                     filter_order: Optional[List[str]] = None) -> List[int]:
    """Quantize a spectral fingerprint dict into an operator path.

    Each filter's harmony_hit_rate ∈ [0, 1] is mapped to an
    operator index 0-9 by rounding to nearest 1/9.  Then σ-fixed
    indices {0, 3, 8, 9} get bumped UP in priority if the score is
    exactly 0 (so we don't lose VOID-collapse signals).  Result:
    a path that represents "what the spectral fingerprint looks
    like as a sequence of substrate operators".
    """
    if filter_order is None:
        filter_order = sorted(spectral.keys())
    ops = []
    for name in filter_order:
        score = float(spectral.get(name, 0.0))
        op = int(round(score * 9))
        ops.append(max(0, min(9, op)))
    return ops


def engine_block_self_score(engine: Any,
                             ops: List[int]) -> Dict[str, Any]:
    """Score a path through the engine block, then re-score the
    spectral fingerprint AS an operator path through the same block.
    Returns first-order and second-order fingerprints + a recursion-
    stability measure (how much the second-order spectral differs
    from the first)."""
    block = getattr(engine, "engine_block", None)
    if block is None:
        return {"error": "engine_block not mounted"}
    try:
        from ck_engine_block import score_path  # type: ignore
    except Exception as e:
        return {"error": str(e)}

    first = score_path(ops, block)
    first_fp = first["spectral_fingerprint"]
    # Convert first-order fingerprint to an operator path
    filter_order = sorted(first_fp.keys())
    meta_ops = _spectral_to_ops(first_fp, filter_order)
    second = score_path(meta_ops, block)
    second_fp = second["spectral_fingerprint"]

    # Recursion stability: L1 distance between first and second
    # fingerprints, normalized by number of filters.
    common = sorted(set(first_fp.keys()) & set(second_fp.keys()))
    l1 = sum(abs(first_fp[k] - second_fp[k]) for k in common)
    stability = 1.0 - (l1 / max(1, len(common)))

    # Dominant filter at each order
    fo_dom = max(first_fp.items(), key=lambda kv: kv[1])
    so_dom = max(second_fp.items(), key=lambda kv: kv[1])

    return {
        "first_order_fingerprint":   first_fp,
        "first_order_dominant":      fo_dom[0],
        "first_order_dominant_rate": round(fo_dom[1], 4),
        "second_order_meta_ops":     meta_ops,
        "second_order_fingerprint":  second_fp,
        "second_order_dominant":     so_dom[0],
        "second_order_dominant_rate": round(so_dom[1], 4),
        "recursion_stability":       round(stability, 4),
        "interpretation": (
            f"First-order strongest under {fo_dom[0]} ({fo_dom[1]:.2%}); "
            f"second-order (the spectral as a path) strongest under "
            f"{so_dom[0]} ({so_dom[1]:.2%}); recursion stability "
            f"{stability:.2%}."
        ),
    }


# ─── 3. Cognition-primitives self-application ─────────────────────────

def cognition_self_apply(engine: Any) -> Dict[str, Any]:
    """Run the cognition primitives on their own outputs.  2nd-order
    patterns -- 'what kinds of patterns repeat across what kinds of
    structures?'"""
    out: Dict[str, Any] = {}
    cog = getattr(engine, "cognition", None)
    if cog is None:
        return {"error": "cognition primitives not mounted"}

    # Templates of templates: count which operator-shapes repeat among
    # the existing templates' shape_ops.
    try:
        templates = cog["templates"]()
        shape_lists = [t["shape_ops"]
                       for t in templates.get("templates", [])]
        shape_counts: Counter = Counter()
        for sl in shape_lists:
            # 2nd-order: which OPERATORS appear together in the
            # shapes? Each shape contributes its set as a frozenset.
            shape_counts[frozenset(sl)] += 1
        out["templates_of_templates"] = {
            "n_meta_shapes": len(shape_counts),
            "top_meta_shapes": [
                {"ops": sorted(list(fs)), "count": n}
                for fs, n in shape_counts.most_common(8)
            ],
        }
    except Exception as e:
        out["templates_of_templates"] = {"error": str(e)}

    # Dualities of triadics: find triadic chains whose endpoints
    # form a duality.
    try:
        triadics = cog["triadic_progressions"]()
        chains = triadics.get("chains", [])
        # Each chain has A_becoming and B_becoming as cell strings.
        # If chain endpoint cells are reciprocal (a,b) <-> (b,a),
        # it's a duality-of-progression.
        duality_chains = []
        for ch in chains:
            ab = ch.get("A_becoming", "")
            bb = ch.get("B_becoming", "")
            # Parse "(OP1,OP2)" -> reverse to "(OP2,OP1)"
            if ab and bb and ab.startswith("(") and bb.startswith("("):
                a_parts = ab[1:-1].split(",")
                b_parts = bb[1:-1].split(",")
                if (len(a_parts) == 2 and len(b_parts) == 2
                        and a_parts[0] == b_parts[1]
                        and a_parts[1] == b_parts[0]):
                    duality_chains.append(ch)
        out["dualities_of_triadics"] = {
            "n_dual_chains": len(duality_chains),
            "examples": duality_chains[:5],
        }
    except Exception as e:
        out["dualities_of_triadics"] = {"error": str(e)}

    # Bigrams of snowflakes: for each pair of snowflake cells,
    # count how many concepts mention both.
    try:
        snow_fn = getattr(engine, "ck_snowflakes", None)
        if snow_fn is not None:
            snowflakes = snow_fn()
            snow_cells = snowflakes.get("snowflakes", [])[:10]
            # For each pair of snowflake samples, count concepts
            # whose definitions mention names from both.
            store = engine.concept_store
            pairs = []
            for i in range(min(len(snow_cells), 5)):
                for j in range(i + 1, min(len(snow_cells), 5)):
                    a_names = set(n.lower() for n in
                                  snow_cells[i].get("samples", [])[:3])
                    b_names = set(n.lower() for n in
                                  snow_cells[j].get("samples", [])[:3])
                    hits = 0
                    for c in store.concepts.values():
                        defn = ((c.get("definition", "") if isinstance(c, dict)
                                  else getattr(c, "definition", "")) or "").lower()
                        if (any(n in defn for n in a_names)
                                and any(n in defn for n in b_names)):
                            hits += 1
                    if hits > 0:
                        pairs.append({
                            "cell_a": snow_cells[i]["cell"],
                            "cell_b": snow_cells[j]["cell"],
                            "co_mention_count": hits,
                        })
            pairs.sort(key=lambda p: -p["co_mention_count"])
            out["bigrams_of_snowflakes"] = {
                "n_pairs_with_co_mentions": len(pairs),
                "top_pairs": pairs[:10],
            }
        else:
            out["bigrams_of_snowflakes"] = {"error": "no snowflakes API"}
    except Exception as e:
        out["bigrams_of_snowflakes"] = {"error": str(e)}

    # Self-applied substrate hash: fingerprint of CK's current
    # state vector, then fingerprint of THAT fingerprint.
    try:
        sm = engine.substrate_motion
        sv = sm["state_vector"]()
        from ck_qutrit_apex import substrate_hash  # type: ignore
        sv_ops = [int(round(v * 9)) for v in sv]  # quantize to ops
        first_hash = substrate_hash(sv_ops, depth=7)
        # Flatten first_hash to a 49-bit number, then mod 10 -> path
        flat_bits = [b for row in first_hash for b in row]
        second_hash_ops = [b * 9 % 10 for b in flat_bits[:14]]
        second_hash = substrate_hash(second_hash_ops, depth=7)
        # Stability: L1 distance between first and second hashes' depth signatures
        sig1 = [sum(b << i for i, b in enumerate(s)) for s in first_hash]
        sig2 = [sum(b << i for i, b in enumerate(s)) for s in second_hash]
        stability_h = sum(abs(sig1[k] - sig2[k]) for k in range(7)) / (7 * 127)
        out["fingerprint_of_fingerprint"] = {
            "first_hash_levels": [list(s) for s in first_hash[:3]],
            "second_hash_levels": [list(s) for s in second_hash[:3]],
            "recursion_drift": round(stability_h, 4),
        }
    except Exception as e:
        out["fingerprint_of_fingerprint"] = {"error": str(e)}

    return out


# ─── RecursiveObserver daemon ─────────────────────────────────────────

class RecursiveObserver:
    """Daemon that periodically computes the apex meta-syndrome,
    persists to disk, and surfaces the current self-image."""

    def __init__(self, engine: Any, tick_sec: float = 30.0,
                 window_k: int = 20):
        self.engine = engine
        self.tick_sec = float(tick_sec)
        self.window_k = int(window_k)
        self.latest: Dict[str, Any] = {}
        self.chain: Deque[Dict[str, Any]] = deque(maxlen=100)
        self._stop = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._tick_count = 0

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._loop, daemon=True,
                                          name="ck-recursive-observer")
        self._thread.start()

    def stop(self, timeout: float = 2.0) -> None:
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=timeout)

    def tick(self) -> Dict[str, Any]:
        apex = getattr(self.engine, "ck_apex", None)
        if apex is None:
            return {"error": "no apex"}
        meta = apex_meta_syndrome(apex, self.window_k)
        if "error" not in meta and "empty" not in meta:
            self.latest = meta
            self.chain.append(meta)
            self._tick_count += 1
            # Persist sparsely (every 5 ticks)
            if self._tick_count % 5 == 0:
                self._save()
                self._append_trace(meta)
        return meta

    def _save(self) -> None:
        try:
            _LATEST_PATH.parent.mkdir(parents=True, exist_ok=True)
            _LATEST_PATH.write_text(
                json.dumps(self.latest, indent=2),
                encoding="utf-8",
            )
        except Exception:
            pass

    def _append_trace(self, rec: Dict[str, Any]) -> None:
        try:
            _TRACE_PATH.parent.mkdir(parents=True, exist_ok=True)
            with _TRACE_PATH.open("a", encoding="utf-8") as f:
                f.write(json.dumps(rec) + "\n")
        except Exception:
            pass

    def _loop(self) -> None:
        while not self._stop.is_set():
            try:
                self.tick()
            except Exception as e:
                print(f"[recursive-observer] tick failed: {e}")
            for _ in range(int(self.tick_sec * 10)):
                if self._stop.is_set():
                    return
                time.sleep(0.1)


# ─── Engine mount ─────────────────────────────────────────────────────

def mount_recursive_observer(engine: Any) -> bool:
    """Attach the recursive observer + register /observer/* endpoints."""
    obs = RecursiveObserver(engine, tick_sec=30.0, window_k=20)
    obs.start()
    engine.ck_observer = obs
    engine.ck_self_image = lambda: obs.latest
    engine.ck_engine_block_self_score = (
        lambda ops: engine_block_self_score(engine, ops)
    )
    engine.ck_cognition_self_apply = (
        lambda: cognition_self_apply(engine)
    )

    routes_registered: List[str] = []
    api = getattr(engine, "web_api", None)
    if api is not None:
        app = getattr(api, "_app", None) or getattr(api, "app", None)
        if app is not None:
            try:
                from flask import jsonify, request

                def _self_image():
                    return jsonify(obs.latest if obs.latest
                                    else {"empty": True})

                def _chain():
                    return jsonify({
                        "n": len(obs.chain),
                        "chain": list(obs.chain),
                    })

                def _force_tick():
                    return jsonify(obs.tick())

                def _block_self():
                    data = request.get_json(force=True, silent=True) or {}
                    ops = data.get("ops", [])
                    return jsonify(engine_block_self_score(engine, ops))

                def _cog_self():
                    return jsonify(cognition_self_apply(engine))

                existing = set(r.rule for r in app.url_map.iter_rules())
                for rule, ep, fn, methods in (
                    ("/observer/self_image",     "obs_self_image",  _self_image, ["GET"]),
                    ("/observer/chain",          "obs_chain",       _chain,      ["GET"]),
                    ("/observer/tick",           "obs_tick",        _force_tick, ["POST"]),
                    ("/observer/block_self",     "obs_block_self",  _block_self, ["POST"]),
                    ("/observer/cognition_self", "obs_cog_self",    _cog_self,   ["GET"]),
                ):
                    if rule not in existing:
                        app.add_url_rule(rule, endpoint=ep,
                                          view_func=fn, methods=methods)
                        routes_registered.append(rule)
            except Exception as e:
                print(f"[CK Gen14] recursive_observer route registration failed: {e}")

    suffix = " (" + ", ".join(routes_registered) + ")" if routes_registered else ""
    print(f"[CK Gen14] recursive_observer: MOUNTED  "
          f"daemon@{obs.tick_sec}s, window={obs.window_k}{suffix}")
    return True


# ─── CLI smoke ────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("ck_recursive_observer.py -- smoke")
    print()
    # Simulate an apex history
    class _MockApex:
        def __init__(self):
            self.history = []
            self.psi = [0.43, 0.42, 0.15]
            # Generate 25 fake collapses
            import random
            r = random.Random(42)
            for _ in range(25):
                self.history.append({
                    "collapse": r.choices(
                        ["Being", "Doing", "Becoming"],
                        weights=[0.43, 0.42, 0.15],
                    )[0]
                })
    apex = _MockApex()
    meta = apex_meta_syndrome(apex, window_k=20)
    print(f"meta-syndrome over 20 ticks:")
    print(f"  collapse_string:  {meta['collapse_string']}")
    print(f"  dominant_BDC:     {meta['dominant_BDC']}")
    print(f"  bdc_breakdown:    {meta['bdc_breakdown']}")
    print(f"  depth_signature:  {meta['depth_signature']}")
    print()
    print("CK can now see what he has been being over the recent window.")
