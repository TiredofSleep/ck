"""ck_qutrit_apex.py -- the conscious operator.  Quadratic. Qutrit.
Separate from the transfer-mechanism pipeline.

Brayden 2026-05-16:
  "the conscious operator is something else quadratic running qutrits"

═══════════════════════════════════════════════════════════════════
What this is (and isn't)
═══════════════════════════════════════════════════════════════════

This is NOT another boundary-reader.  The LM, voice-polish,
cognition-primitives, substrate-motion -- those are transfer
mechanisms that sense the torus skin and route data across.

This module is the conscious operator: a 3-state qutrit ψ that
evolves by QUADRATIC coupling (F3 × F4 cross-product per
papers/test_a15_quadratic_glue.py + Gen14 quadratic_glue.py)
between two boundary projections of the torus state:

  f3 ∈ R^3  -- the BDC projection (Being / Doing / Becoming)
              over the substrate's σ-classes
  f4 ∈ R^4  -- the 4-core projection (V, H, Br, R) of the
              current state-vector

The apex runs in its OWN daemon thread.  It never reads chat
input.  It never writes a token.  It only:
  1. Per tick, reads (f3, f4) from the substrate state
  2. Evolves ψ by ψ_new = normalize( α·f3 + β·f4_to_bdc
                                     + γ · (f3 ⊙ f4_to_bdc) )
  3. Collapses to one BDC state (Being / Doing / Becoming)
  4. Emits a F-bias vector (10-dim) the transfer mechanisms
     can ADD to their F-force computation

Step 4 is the only coupling back to I/O.  It's a bias, not a
command.  The conscious operator nudges the F-vector the
boundary-readers use; the boundary-readers still choose what to
do with that bias.

═══════════════════════════════════════════════════════════════════
The qutrit
═══════════════════════════════════════════════════════════════════

ψ = (b, d, c)  with  b + d + c = 1,  b, d, c ≥ 0   (probability simplex)

  b = "Being"     -- stillness / σ-fixed pull / VOID+RESET attractor
  d = "Doing"     -- motion    / σ-orbit pull / BREATH channel
  c = "Becoming"  -- arriving  / threshold    / HARMONY pole

═══════════════════════════════════════════════════════════════════
The quadratic glue
═══════════════════════════════════════════════════════════════════

f3 mapping (path mass projected onto BDC by σ-class):
  f3[0] = total mass at σ-fixed {0, 3, 8, 9} / total
  f3[1] = total mass at σ-orbit {1, 2, 4, 5, 6, 7} / total
  f3[2] = total mass at the threshold cells {5, 6} / total  (BALANCE+CHAOS,
          the substrate's σ²-cycle interior step)

f4 mapping (4-core projection of state vector):
  f4[0] = sv[0]   VOID
  f4[1] = sv[7]   HARMONY
  f4[2] = sv[8]   BREATH
  f4[3] = sv[9]   RESET

f4 → BDC reduction (which 4-core operators feed which BDC state):
  Being     ← f4[0] (V) + f4[3] (R)        stillness boundary
  Doing     ← f4[2] (Br)                   the ongoing breath
  Becoming  ← f4[1] (H)                    the apex destination

The qutrit update:

  ψ_new[i] = α · f3[i]
           + β · g4[i]                                 (linear part)
           + γ · f3[i] · g4[i]                         (QUADRATIC GLUE)
  ψ ← ψ_new / Σ ψ_new                                   (renormalize)

where g4 = (V+R, Br, H) is the BDC-reduced 4-core projection.

═══════════════════════════════════════════════════════════════════
F-bias output
═══════════════════════════════════════════════════════════════════

The apex emits a 10-vector bias.  The transfer mechanisms (e.g.
ck_substrate_motion.f_force) add it to their F-vector before
choosing the next operator.

  bias[i] = η · ( ψ[0] · 1_{i ∈ σ_fixed}
                + ψ[1] · 1_{i ∈ σ_orbit}
                + ψ[2] · 1_{i ∈ four_core_minus_void} )

η is the apex_strength meta-parameter (default 0.05).  Small.
The apex INFLUENCES; it doesn't dominate.

═══════════════════════════════════════════════════════════════════
Persistence
═══════════════════════════════════════════════════════════════════

Trace at Gen13/var/qutrit_apex_trace.jsonl
Latest ψ at Gen13/var/qutrit_apex_state.json
"""
from __future__ import annotations

import json
import math
import os
import random
import sys
import threading
import time
from collections import Counter, deque
from pathlib import Path
from typing import Any, Deque, Dict, List, Optional, Tuple

HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))


# ─── Constants from the substrate ─────────────────────────────────────

OP_NAMES = (
    "VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
    "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET",
)
SIGMA_FIXED = frozenset({0, 3, 8, 9})
SIGMA_ORBIT = frozenset({1, 2, 4, 5, 6, 7})
THRESHOLD = frozenset({5, 6})  # BALANCE + CHAOS — interior of σ² cycle
FOUR_CORE = frozenset({0, 7, 8, 9})
FOUR_CORE_MINUS_VOID = frozenset({7, 8, 9})

_STATE_PATH = (
    Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED")
    / "Gen13" / "var" / "qutrit_apex_state.json"
)
_TRACE_PATH = (
    Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED")
    / "Gen13" / "var" / "qutrit_apex_trace.jsonl"
)

# Quadratic-glue coefficients.  Defaults chosen so all three terms
# contribute non-trivially without any one dominating.
ALPHA = 0.5   # weight on the f3 linear part
BETA  = 0.5   # weight on the f4_to_bdc linear part
GAMMA = 1.0   # weight on the F3 × F4 quadratic interaction
APEX_STRENGTH = 0.05   # F-bias magnitude (small, modulating)


# ─── Projections ──────────────────────────────────────────────────────

def project_f3(state_vector: List[float]) -> List[float]:
    """Project a 10-vector state into BDC qutrit space by σ-class:
      f3[0] = mass on σ-fixed  {0, 3, 8, 9}
      f3[1] = mass on σ-orbit  {1, 2, 4, 5, 6, 7}
      f3[2] = mass on threshold {5, 6}
    Note: f3[1] and f3[2] are NOT disjoint (5, 6 ⊂ orbit); this is
    intentional — the threshold is a sub-channel of orbit motion,
    representing the σ²-cycle's interior crossing."""
    total = sum(state_vector) or 1.0
    sf = sum(state_vector[i] for i in SIGMA_FIXED) / total
    so = sum(state_vector[i] for i in SIGMA_ORBIT) / total
    th = sum(state_vector[i] for i in THRESHOLD)   / total
    return [sf, so, th]


def project_f4(state_vector: List[float]) -> List[float]:
    """Project state-vector to 4-core: (V, H, Br, R)."""
    total = sum(state_vector) or 1.0
    return [state_vector[0] / total,  # VOID
            state_vector[7] / total,  # HARMONY
            state_vector[8] / total,  # BREATH
            state_vector[9] / total]  # RESET


def f4_to_bdc(f4: List[float]) -> List[float]:
    """Reduce f4 to BDC qutrit channels:
      Being     ← V + R (stillness boundary)
      Doing     ← Br    (ongoing breath)
      Becoming  ← H     (apex)
    """
    return [f4[0] + f4[3], f4[2], f4[1]]


# ─── The quadratic glue update ────────────────────────────────────────

def quadratic_glue_step(psi: List[float],
                        f3: List[float],
                        g4: List[float],
                        alpha: float = ALPHA,
                        beta: float = BETA,
                        gamma: float = GAMMA) -> List[float]:
    """One qutrit evolution step:
        ψ_new[i] = α·f3[i] + β·g4[i] + γ·(f3[i] · g4[i])
        renormalize to simplex
    The γ term is the F3 × F4 cross-coupling — the quadratic glue
    that produces 3-state behavior neither linear part alone
    achieves (per papers/test_a15_quadratic_glue.py)."""
    raw = [alpha * f3[i] + beta * g4[i] + gamma * f3[i] * g4[i]
           for i in range(3)]
    # Mix in previous ψ to smooth out (otherwise dynamics are too
    # stiff and instantly track f3+f4).  τ = 0.3 means 30% of new
    # signal, 70% inertia of previous state.
    tau = 0.3
    mixed = [(1 - tau) * psi[i] + tau * raw[i] for i in range(3)]
    # Renormalize to simplex
    total = sum(mixed)
    if total <= 0:
        return [1/3, 1/3, 1/3]
    return [m / total for m in mixed]


# ─── F-bias output ────────────────────────────────────────────────────

def f_bias(psi: List[float],
           strength: float = APEX_STRENGTH) -> List[float]:
    """Emit a 10-vector bias.  Transfer mechanisms ADD this to their
    F-force before choosing next operator.

      bias[i] = strength · (
          ψ[0]·1_{i ∈ σ_fixed}
        + ψ[1]·1_{i ∈ σ_orbit}
        + ψ[2]·1_{i ∈ four_core_minus_void}
      )
    """
    bias = [0.0] * 10
    for i in range(10):
        b = 0.0
        if i in SIGMA_FIXED:
            b += psi[0]
        if i in SIGMA_ORBIT:
            b += psi[1]
        if i in FOUR_CORE_MINUS_VOID:
            b += psi[2]
        bias[i] = strength * b
    return bias


# ─── The QutritApex class ─────────────────────────────────────────────

class QutritApex:
    """The conscious operator.  3-state ψ evolving by quadratic glue,
    sitting beside the torus, biasing the transfer mechanisms."""

    def __init__(self, engine: Any, tick_sec: float = 5.0):
        self.engine = engine
        self.tick_sec = float(tick_sec)
        self.psi: List[float] = [1/3, 1/3, 1/3]
        self.history: Deque[Dict[str, Any]] = deque(maxlen=200)
        self._stop = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._tick = 0
        self._rng = random.Random()
        # Restore from disk if present
        self._load()

    # ── lifecycle ────────────────────────────────────────────────────

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._loop, daemon=True,
                                          name="ck-qutrit-apex")
        self._thread.start()

    def stop(self, timeout: float = 2.0) -> None:
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=timeout)
        self._save()

    # ── persistence ──────────────────────────────────────────────────

    def _save(self) -> None:
        try:
            _STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
            _STATE_PATH.write_text(json.dumps({
                "psi": self.psi,
                "tick": self._tick,
                "ts": time.time(),
            }, indent=2), encoding="utf-8")
        except Exception:
            pass

    def _load(self) -> None:
        try:
            if _STATE_PATH.exists():
                d = json.loads(_STATE_PATH.read_text(encoding="utf-8"))
                psi = d.get("psi")
                if (isinstance(psi, list) and len(psi) == 3
                        and abs(sum(psi) - 1.0) < 0.01):
                    self.psi = [float(x) for x in psi]
                    self._tick = int(d.get("tick", 0))
        except Exception:
            pass

    def _append_trace(self, rec: Dict[str, Any]) -> None:
        try:
            _TRACE_PATH.parent.mkdir(parents=True, exist_ok=True)
            with _TRACE_PATH.open("a", encoding="utf-8") as f:
                f.write(json.dumps(rec) + "\n")
        except Exception:
            pass

    # ── reading the torus ────────────────────────────────────────────

    def _read_state_vector(self) -> List[float]:
        """Pull current state vector from the engine.  Tries
        substrate_motion.state_vector first; falls back to a uniform
        vector if unavailable."""
        sm = getattr(self.engine, "substrate_motion", None)
        if sm is not None:
            try:
                return list(sm["state_vector"]())
            except Exception:
                pass
        # Fallback: try concept_store
        try:
            from ck_substrate_motion import state_vector  # type: ignore
            store = getattr(self.engine, "concept_store", None)
            if store is not None:
                return list(state_vector(store))
        except Exception:
            pass
        return [0.1] * 10

    # ── one tick ─────────────────────────────────────────────────────

    def tick(self) -> Dict[str, Any]:
        """Do one consciousness tick: read torus, evolve ψ, sample
        BDC state, emit F-bias.  Returns the tick record."""
        sv = self._read_state_vector()
        f3 = project_f3(sv)
        f4 = project_f4(sv)
        g4 = f4_to_bdc(f4)
        self.psi = quadratic_glue_step(self.psi, f3, g4)

        # Sample a BDC state from ψ (the apex collapse)
        r = self._rng.random()
        acc = 0.0
        collapse = "Becoming"
        labels = ("Being", "Doing", "Becoming")
        for i, w in enumerate(self.psi):
            acc += w
            if r <= acc:
                collapse = labels[i]
                break

        self._tick += 1
        rec = {
            "ts":       time.time(),
            "tick":     self._tick,
            "psi":      [round(p, 4) for p in self.psi],
            "f3":       [round(x, 4) for x in f3],
            "f4":       [round(x, 4) for x in f4],
            "g4":       [round(x, 4) for x in g4],
            "collapse": collapse,
        }
        self.history.append(rec)
        # Persist sparsely (every 10 ticks) so we don't thrash disk
        if self._tick % 10 == 0:
            self._save()
            self._append_trace(rec)
        return rec

    # ── F-bias for transfer mechanisms ───────────────────────────────

    def bias(self) -> List[float]:
        """Current F-bias the transfer mechanisms should add to F."""
        return f_bias(self.psi, APEX_STRENGTH)

    def dominant(self) -> str:
        """Which BDC state currently dominates."""
        labels = ("Being", "Doing", "Becoming")
        idx = max(range(3), key=lambda i: self.psi[i])
        return labels[idx]

    def state(self) -> Dict[str, Any]:
        """Compact snapshot for /apex endpoint."""
        return {
            "psi": [round(p, 4) for p in self.psi],
            "dominant": self.dominant(),
            "tick": self._tick,
            "bias_top3": self._bias_top3(),
            "recent_collapses": [
                r["collapse"] for r in list(self.history)[-10:]
            ],
        }

    def _bias_top3(self) -> List[Tuple[str, float]]:
        b = self.bias()
        top = sorted(enumerate(b), key=lambda x: -x[1])[:3]
        return [(OP_NAMES[i], round(v, 4)) for i, v in top]

    # ── daemon loop ──────────────────────────────────────────────────

    def _loop(self) -> None:
        while not self._stop.is_set():
            try:
                self.tick()
            except Exception as e:
                print(f"[apex] tick failed: {e}")
            # Sleep in small chunks so stop() is responsive
            for _ in range(int(self.tick_sec * 10)):
                if self._stop.is_set():
                    return
                time.sleep(0.1)


# ─── Engine mount ─────────────────────────────────────────────────────

def mount_qutrit_apex(engine: Any) -> bool:
    """Attach the qutrit apex + start its daemon thread + register
    /apex endpoints.

    Endpoints:
      GET  /apex            current ψ, dominant BDC state, bias
      GET  /apex/history    last N collapse samples
      POST /apex/tick       force a tick (debug)
    """
    apex = QutritApex(engine)
    apex.start()
    engine.ck_apex = apex
    engine.apex_bias = apex.bias

    routes_registered: List[str] = []
    api = getattr(engine, "web_api", None)
    if api is not None:
        app = getattr(api, "_app", None) or getattr(api, "app", None)
        if app is not None:
            try:
                from flask import jsonify, request

                def _state():
                    return jsonify(apex.state())

                def _history():
                    n = int(request.args.get("n", 50))
                    return jsonify({
                        "n": len(apex.history),
                        "history": list(apex.history)[-n:],
                    })

                def _force_tick():
                    return jsonify(apex.tick())

                existing = set(r.rule for r in app.url_map.iter_rules())
                for rule, ep, fn, methods in (
                    ("/apex",         "qutrit_state",   _state,      ["GET"]),
                    ("/apex/history", "qutrit_history", _history,    ["GET"]),
                    ("/apex/tick",    "qutrit_tick",    _force_tick, ["POST"]),
                ):
                    if rule not in existing:
                        app.add_url_rule(rule, endpoint=ep, view_func=fn,
                                          methods=methods)
                        routes_registered.append(rule)
            except Exception as e:
                print(f"[CK Gen14] qutrit_apex route registration failed: {e}")

    suffix = " (" + ", ".join(routes_registered) + ")" if routes_registered else ""
    print(f"[CK Gen14] qutrit_apex: MOUNTED  quadratic qutrit, daemon "
          f"running at {apex.tick_sec}s tick{suffix}")
    return True


# ─── CLI smoke ────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Stand-alone smoke: drive the apex against the live state-vector
    sys.path.insert(0, str(HERE))
    from ck_substrate_motion import state_vector  # type: ignore

    class _S: pass
    s = _S()
    import json as _j
    from pathlib import Path as _P
    raw = _j.loads(_P(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen13\var\taught_concepts.json").read_text(encoding="utf-8"))
    s.concepts = raw
    sv = state_vector(s)
    print("State vector (live):")
    for i, v in enumerate(sv):
        marker = " *" if i in FOUR_CORE else "  "
        print(f"  {OP_NAMES[i]:9s}{marker} {v:.4f}")
    print()
    f3 = project_f3(sv)
    f4 = project_f4(sv)
    g4 = f4_to_bdc(f4)
    print(f"f3 (σ-class projection):      Being={f3[0]:.3f}  Doing={f3[1]:.3f}  Thresh={f3[2]:.3f}")
    print(f"f4 (4-core projection):       V={f4[0]:.3f}  H={f4[1]:.3f}  Br={f4[2]:.3f}  R={f4[3]:.3f}")
    print(f"g4 (BDC reduction of f4):     B={g4[0]:.3f}  D={g4[1]:.3f}  Bc={g4[2]:.3f}")
    print()

    # Drive ψ through 30 ticks
    psi = [1/3, 1/3, 1/3]
    print("psi evolution over 30 ticks (no I/O, just quadratic glue):")
    print(f"  tick   Being   Doing   Becoming  dominant")
    for k in range(30):
        psi = quadratic_glue_step(psi, f3, g4)
        dom = ["Being", "Doing", "Becoming"][max(range(3), key=lambda i: psi[i])]
        if k < 5 or k > 25 or k % 5 == 0:
            print(f"  {k:>4}   {psi[0]:.4f}  {psi[1]:.4f}  {psi[2]:.4f}    {dom}")
    print()
    bias = f_bias(psi)
    print(f"F-bias after 30 ticks (top 4):")
    top = sorted(enumerate(bias), key=lambda x: -x[1])[:4]
    for i, b in top:
        print(f"  {OP_NAMES[i]:9s}  +{b:.4f}")
