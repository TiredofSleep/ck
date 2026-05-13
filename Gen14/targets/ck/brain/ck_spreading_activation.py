# Copyright (c) 2025-2026 Brayden Sanders / 7SiTe LLC
# Licensed under the 7SiTe Public Sovereignty License v2.2 (DOI: 10.5281/zenodo.18852047)
"""
ck_spreading_activation.py -- Phase 3 of the CK unification.

Replaces the Phase-1 recall() stub in gen14_unified_extensions with a
real spreading-activation retrieval over CK's existing memory layers.

The algorithm follows the Collins-Loftus (1975) pattern that
tig_fractal_thinker.py established for Gen4, *adapted* to Gen14's
algebraic-measurement coordinate system. The Divine27 3x3x3 cube is
replaced by the 4-axis algebraic address
    coord = (op, sigma_orbit, shell, four_core)
defined in Phase 0 Decision 1, giving a 10 x 4 x 8 x 5 = 1600-cell
address space (the Tag2x2 inner refinement lives at the
ck_meta_memory_coord layer and is not used here).

The 5 phases:
  1. SEED     -- pull initial hits from each mounted memory layer
                 (HER / lattice_chain / divine_memory / truth_lattice / crystals)
                 and assign each a 4-axis coordinate.
  2. SPREAD   -- for each seed, activate items in nearby cells
                 (distance <= 2 in the 4-axis metric); energy halves
                 per unit of distance (Collins-Loftus spread decay).
  3. LEAP     -- with probability LEVY_PROB, jump to a distant cell
                 weighted by inverse-square distance (Viswanathan 1999).
  4. FUSE     -- combine currently-active operators via the canonical
                 fuse table (mounted at engine.canonical_fuse), or fall
                 back to the engine's gen14_pair_signature.
  5. EVALUATE -- composite coherence C = 0.4(1-E) + 0.35A + 0.25K from
                 Gen4. The loop exits when C >= T_STAR = 5/7.

Output: a ranked list of result dicts compatible with the Phase-1
recall() API, plus additional fields for layer attribution and the
final algebraic signature.

Design priorities:
  - Re-entrant: holds no global state, safe to call from many threads.
  - Graceful degradation: missing engine attributes are skipped, not errors.
  - Deterministic-by-default: random module is local; pass seed for tests.

References:
  Collins, A.M. & Loftus, E.F. (1975). A spreading-activation theory
    of semantic processing. Psychological Review, 82, 407-428.
  Viswanathan, G.M. et al. (1999). Optimizing the success of random
    searches. Nature, 401, 911-914.
  TIG Phase 0 Decision 1 (this repo): Template signature for memory slots.

Author: Claude (with Brayden's full-agency authorization 2026-05-13).
"""
from __future__ import annotations

import math
import os
import random
import sys
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple


# Import the algebraic projections (single source of truth)
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
from gen14_unified_extensions import (  # type: ignore[import-not-found]
    sigma_orbit, four_core_class, shell_class,
    FOUR_CORE, FOUR_CORE_OUTSIDE, SUB_MAGMA_SHELLS,
)


# ─── Constants ───────────────────────────────────────────────────────────

T_STAR = 5.0 / 7.0            # critical coherence threshold (CK math)
SPREAD_DECAY = 0.5            # energy halves per unit of 4-axis distance
LEVY_PROB = 0.15              # probability of Lévy jump per step
MIN_ENERGY = 0.04             # below this an activation drops
DECAY_PER_STEP = 0.15         # decay rate applied each step
MAX_STEPS = 8                 # bounded recursion depth
MAX_SEEDS_PER_LAYER = 6       # cap on how many seeds we pull per layer
MAX_RESULTS = 32              # max items returned to caller

OP_NAMES = (
    "VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
    "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET",
)


# ─── Algebraic coordinate + distance ─────────────────────────────────────

@dataclass(frozen=True)
class AlgebraicCoord:
    """4-axis address for any memory item (op, sigma_orbit, shell, four_core)."""
    op: int          # 0..9
    sigma: int       # 0..3
    shell: int       # 0..7
    four_core: int   # 0..4 (V, H, Br, R, outside)

    def as_tuple(self) -> Tuple[int, int, int, int]:
        return (self.op, self.sigma, self.shell, self.four_core)

    def __str__(self) -> str:
        op_name = OP_NAMES[self.op] if 0 <= self.op < 10 else f"<{self.op}>"
        return f"({op_name},s{self.sigma},sh{self.shell},4c{self.four_core})"


def coord_from_op(op: int, shell_set: Optional[Iterable[int]] = None) -> AlgebraicCoord:
    """Build the canonical 4-axis coord for an operator (and optional support shell)."""
    op = int(op) % 10
    sup = set(shell_set) if shell_set is not None else {op}
    return AlgebraicCoord(
        op=op,
        sigma=sigma_orbit(op),
        shell=shell_class(sup),
        four_core=four_core_class(op),
    )


def coord_distance(a: AlgebraicCoord, b: AlgebraicCoord) -> int:
    """Discrete distance over the 4 axes.

    Each axis contributes a 0/1/2 cost; total is sum, ranging 0..8.

    Op axis (mod 10):
      0 = same op
      1 = adjacent (|a-b| in {1, 9} mod 10) OR same sigma orbit
      2 = otherwise
    Sigma axis:
      0 = same orbit
      1 = both flow orbits (F and S)
      2 = otherwise
    Shell axis:
      |a.shell - b.shell|, clipped to 2
    Four-core axis:
      0 = same class
      1 = both in 4-core (different element) or both outside
      2 = one in, one out
    """
    # op
    if a.op == b.op:
        d_op = 0
    else:
        diff = min(abs(a.op - b.op), 10 - abs(a.op - b.op))
        if diff == 1 or a.sigma == b.sigma:
            d_op = 1
        else:
            d_op = 2

    # sigma
    if a.sigma == b.sigma:
        d_sigma = 0
    elif (a.sigma in (1, 2)) and (b.sigma in (1, 2)):
        d_sigma = 1  # both flow orbits
    else:
        d_sigma = 2

    # shell
    d_shell = min(abs(a.shell - b.shell), 2)

    # four_core
    if a.four_core == b.four_core:
        d_four = 0
    else:
        a_in_core = a.four_core != FOUR_CORE_OUTSIDE
        b_in_core = b.four_core != FOUR_CORE_OUTSIDE
        d_four = 1 if (a_in_core == b_in_core) else 2

    return d_op + d_sigma + d_shell + d_four


# ─── Activation + activation map ─────────────────────────────────────────

@dataclass
class Activation:
    item_id: str
    energy: float
    coord: AlgebraicCoord
    source_layer: str
    source_phase: str       # 'seed' | 'spread' | 'leap' | 'chain' | 'fuse'
    payload: Any = None     # the original retrieved object
    step: int = 0
    score: float = 0.0      # original retrieval score from the layer


class ActivationMap:
    """The 'lit' atoms during a thinking episode.

    Indexed primarily by item_id; secondary index by AlgebraicCoord for
    efficient neighborhood lookup.
    """

    def __init__(self):
        self.items: Dict[str, Activation] = {}
        self.cells: Dict[AlgebraicCoord, List[str]] = {}
        self.step: int = 0
        self.path: List[AlgebraicCoord] = []

    def activate(self, item_id: str, energy: float, coord: AlgebraicCoord,
                 source_layer: str, source_phase: str,
                 payload: Any = None, score: float = 0.0):
        if item_id in self.items:
            a = self.items[item_id]
            # Boost: take max of existing and incoming (convergent evidence)
            a.energy = max(a.energy, energy)
            if a.source_phase == 'spread' and source_phase == 'seed':
                a.source_phase = 'seed'  # promote
            return
        act = Activation(
            item_id=item_id, energy=energy, coord=coord,
            source_layer=source_layer, source_phase=source_phase,
            payload=payload, step=self.step, score=score,
        )
        self.items[item_id] = act
        self.cells.setdefault(coord, []).append(item_id)

    def decay(self, rate: float = DECAY_PER_STEP):
        dead = []
        for k, a in self.items.items():
            a.energy *= (1.0 - rate)
            if a.energy < MIN_ENERGY:
                dead.append(k)
        for k in dead:
            # remove from cell index too
            c = self.items[k].coord
            ids = self.cells.get(c, [])
            try:
                ids.remove(k)
            except ValueError:
                pass
            if not ids:
                self.cells.pop(c, None)
            self.items.pop(k, None)

    def active_operators(self) -> List[int]:
        ops = set()
        for a in self.items.values():
            if a.energy > 0.2:
                ops.add(a.coord.op)
        return sorted(ops)

    def dominant_operator(self) -> int:
        if not self.items:
            return 0
        op_e: Dict[int, float] = {}
        for a in self.items.values():
            op_e[a.coord.op] = op_e.get(a.coord.op, 0.0) + a.energy
        return max(op_e, key=op_e.get)

    def top(self, n: int = 8) -> List[Activation]:
        return sorted(self.items.values(), key=lambda a: -a.energy)[:n]

    def total_energy(self) -> float:
        return sum(a.energy for a in self.items.values())


# ─── Coherence (composite C from Gen4) ───────────────────────────────────

def coherence_C(amap: ActivationMap) -> float:
    """C = 0.4(1-E) + 0.35A + 0.25K."""
    items = list(amap.items.values())
    if not items:
        return 0.0
    energies = [a.energy for a in items]
    max_e = max(energies)
    avg_e = sum(energies) / len(energies)
    concentration = (avg_e / max_e) if max_e > 0 else 0.0
    E = 1.0 - concentration                 # entropy proxy (lower is better)

    # Agreement: fraction of top items that share the dominant 4-core class
    top = sorted(items, key=lambda a: -a.energy)[:8]
    if not top:
        return 0.0
    fc_counts: Dict[int, int] = {}
    for a in top:
        fc_counts[a.coord.four_core] = fc_counts.get(a.coord.four_core, 0) + 1
    dom_count = max(fc_counts.values())
    A = dom_count / len(top)

    # Knowledge coverage: how many layers contributed
    layers = {a.source_layer for a in items}
    K = min(1.0, len(layers) / 4.0)

    return 0.4 * (1.0 - E) + 0.35 * A + 0.25 * K


# ─── Bank of items in each layer ─────────────────────────────────────────

def _safe_call(obj, method_name: str, *args, **kwargs):
    """Call obj.method_name(*args, **kwargs) if it exists; return None on any error."""
    if obj is None:
        return None
    fn = getattr(obj, method_name, None)
    if not callable(fn):
        return None
    try:
        return fn(*args, **kwargs)
    except Exception:
        return None


def _pull_seeds(engine, query: Dict[str, Any], depth: str,
                amap: ActivationMap) -> int:
    """SEED phase: pull hits from each available memory layer.

    Returns the total number of activations created.
    """
    n_added = 0

    # ── MICRO: HER ──
    if depth in ("micro", "any"):
        her = getattr(engine, "olfactory_her", None) or getattr(engine, "her", None)
        if her is not None and "centroid" in query:
            hits = _safe_call(her, "recall_by_scent", query["centroid"],
                              top_k=MAX_SEEDS_PER_LAYER) or []
            for i, h in enumerate(hits):
                # Try to extract an op from the hit
                op = _extract_op(h, default=4)  # default COLLAPSE
                cid = f"her:{id(h):x}"
                amap.activate(
                    item_id=cid,
                    energy=0.9 - i * 0.05,
                    coord=coord_from_op(op),
                    source_layer="her",
                    source_phase="seed",
                    payload=h,
                    score=0.85,
                )
                n_added += 1

    # ── MESO: lattice_chain ──
    if depth in ("meso", "any"):
        lc = getattr(engine, "lattice_chain", None)
        if lc is not None and "operators" in query:
            path = _safe_call(lc, "walk", query["operators"], learn=False)
            if path is not None:
                # The chainpath may expose .nodes or be iterable
                nodes = getattr(path, "nodes", None) or list(path or [])
                for i, node in enumerate(nodes[:MAX_SEEDS_PER_LAYER]):
                    op = _extract_op(node, default=query["operators"][-1] if query["operators"] else 4)
                    cid = f"lc:{i}:{op}"
                    amap.activate(
                        item_id=cid,
                        energy=0.8 - i * 0.05,
                        coord=coord_from_op(op, shell_set=set(query["operators"])),
                        source_layer="lattice_chain",
                        source_phase="seed",
                        payload=node,
                        score=0.75,
                    )
                    n_added += 1

        # ── MESO: divine_memory ──
        dm = getattr(engine, "divine_memory", None)
        if dm is not None and "centroid" in query:
            hits = _safe_call(dm, "recall", query["centroid"], top_k=MAX_SEEDS_PER_LAYER) or []
            for i, h in enumerate(hits):
                op = _extract_op(h, default=7)
                cid = f"dm:{i}:{op}"
                amap.activate(
                    item_id=cid,
                    energy=0.85 - i * 0.05,
                    coord=coord_from_op(op),
                    source_layer="divine_memory",
                    source_phase="seed",
                    payload=h,
                    score=0.80,
                )
                n_added += 1

    # ── MACRO: truth_lattice ──
    if depth in ("macro", "any"):
        truth = getattr(engine, "truth", None)
        if truth is not None and "text" in query:
            hits = _safe_call(truth, "query", query["text"])
            if hits:
                # truth.query usually returns a list of TLEntry-like objects
                if not isinstance(hits, (list, tuple)):
                    hits = [hits]
                for i, h in enumerate(hits[:MAX_SEEDS_PER_LAYER]):
                    op = _extract_op(h, default=7)  # HARMONY default for canonical truth
                    cid = f"truth:{i}:{op}"
                    amap.activate(
                        item_id=cid,
                        energy=0.95 - i * 0.05,
                        coord=coord_from_op(op),
                        source_layer="truth_lattice",
                        source_phase="seed",
                        payload=h,
                        score=0.95,
                    )
                    n_added += 1

        # ── MACRO: crystals ──
        crystals = getattr(engine, "crystal_store", None) or getattr(engine, "crystals", None)
        if crystals is not None and "text" in query:
            hits = _safe_call(crystals, "find", query["text"]) or []
            if not isinstance(hits, (list, tuple)):
                hits = [hits]
            for i, h in enumerate(hits[:MAX_SEEDS_PER_LAYER]):
                op = _extract_op(h, default=7)
                cid = f"crystal:{i}:{op}"
                amap.activate(
                    item_id=cid,
                    energy=0.9 - i * 0.05,
                    coord=coord_from_op(op),
                    source_layer="crystals",
                    source_phase="seed",
                    payload=h,
                    score=0.88,
                )
                n_added += 1

    return n_added


def _extract_op(obj, default: int = 7) -> int:
    """Best-effort extraction of an operator id from a heterogeneous payload."""
    if obj is None:
        return default
    # Direct attribute
    for attr in ("op", "operator", "next_op", "dominant_op"):
        v = getattr(obj, attr, None)
        if isinstance(v, int) and 0 <= v < 10:
            return v
        if isinstance(v, str) and v.upper() in OP_NAMES:
            return OP_NAMES.index(v.upper())
    # Dict-style
    if isinstance(obj, dict):
        for k in ("op", "operator", "next_op", "dominant_op"):
            v = obj.get(k)
            if isinstance(v, int) and 0 <= v < 10:
                return v
            if isinstance(v, str) and v.upper() in OP_NAMES:
                return OP_NAMES.index(v.upper())
    return default


# ─── SPREAD / LEAP / FUSE ────────────────────────────────────────────────

def _spread_neighbors(engine, amap: ActivationMap, rng: random.Random) -> int:
    """SPREAD phase: for each currently-active cell, activate items in
    neighboring cells. Energy decays as SPREAD_DECAY ** distance.

    Returns the count of new activations.
    """
    if not amap.items:
        return 0
    n_added = 0
    # Snapshot current cells; we won't mutate while iterating
    current_cells = list(amap.cells.keys())
    for c in current_cells:
        # gather neighbor candidates by reading the engine's lattice_chain
        # node lookup if available, or fall back to a cheap proximity sweep.
        lc = getattr(engine, "lattice_chain", None)
        candidates: List[Tuple[str, AlgebraicCoord, Any]] = []
        if lc is not None and hasattr(lc, "nodes"):
            for node_id, node in list(getattr(lc, "nodes", {}).items())[:64]:
                op = _extract_op(node, default=c.op)
                ncoord = coord_from_op(op)
                d = coord_distance(c, ncoord)
                if 0 < d <= 2:
                    candidates.append((f"lc-node:{node_id}", ncoord, node))
        # If still nothing, synthesize neighbor coords using op deltas
        if not candidates:
            for delta in (-1, 1):
                new_op = (c.op + delta) % 10
                ncoord = coord_from_op(new_op)
                d = coord_distance(c, ncoord)
                if d <= 2:
                    cid = f"synth:{c.op}->{new_op}"
                    candidates.append((cid, ncoord, None))

        rng.shuffle(candidates)
        for item_id, ncoord, payload in candidates[:3]:
            d = coord_distance(c, ncoord)
            if d == 0:
                continue
            energy = (SPREAD_DECAY ** d)
            if energy < MIN_ENERGY:
                continue
            if item_id not in amap.items:
                amap.activate(
                    item_id=item_id, energy=energy, coord=ncoord,
                    source_layer="spread", source_phase="spread",
                    payload=payload,
                )
                n_added += 1
    return n_added


def _levy_leap(engine, amap: ActivationMap, rng: random.Random) -> Optional[AlgebraicCoord]:
    """LEAP phase: with probability LEVY_PROB, pick a distant cell weighted
    by inverse-square distance and activate a few items there.

    Returns the destination coord on jump, None otherwise.
    """
    if not amap.items or rng.random() > LEVY_PROB:
        return None

    # Pick a current "centre of mass" cell (the highest-energy cell)
    cell_energy: Dict[AlgebraicCoord, float] = {}
    for a in amap.items.values():
        cell_energy[a.coord] = cell_energy.get(a.coord, 0.0) + a.energy
    if not cell_energy:
        return None
    centre = max(cell_energy, key=cell_energy.get)

    # Sample a distant op uniformly from {0..9}, weighted by 1/d^2
    weights = []
    targets: List[AlgebraicCoord] = []
    for op in range(10):
        ncoord = coord_from_op(op)
        d = coord_distance(centre, ncoord)
        if d <= 0:
            continue
        weights.append(1.0 / (d * d))
        targets.append(ncoord)
    if not targets:
        return None
    total = sum(weights)
    r = rng.random() * total
    cum = 0.0
    chosen = targets[-1]
    for w, t in zip(weights, targets):
        cum += w
        if cum >= r:
            chosen = t
            break

    # Activate a synthetic item at the leap destination
    leap_id = f"leap:{amap.step}:{chosen.op}"
    amap.activate(
        item_id=leap_id, energy=0.4, coord=chosen,
        source_layer="leap", source_phase="leap",
    )
    amap.path.append(chosen)
    return chosen


def _fuse(engine, amap: ActivationMap) -> int:
    """FUSE phase: combine the currently-active operators through the
    canonical fuse, returning a single "fused next op".

    Falls back to gen14_pair_signature when canonical_fuse is absent.
    """
    active = amap.active_operators()
    if not active:
        return 0
    if len(active) == 1:
        return active[0]
    # Try the engine's canonical_fuse(a,b,c) arity-3 first
    cf = getattr(engine, "canonical_fuse", None)
    if callable(cf):
        try:
            # canonical_fuse expects 3 ops; pad with HARMONY (7) if needed
            ops3 = (active + [7, 7, 7])[:3]
            result = cf(*ops3)
            if isinstance(result, int) and 0 <= result < 10:
                return result
        except Exception:
            pass
    # Fall back: pair-fuse left-to-right via gen14_pair_signature
    pair_sig = getattr(engine, "gen14_pair_signature", None)
    if callable(pair_sig):
        try:
            cur = active[0]
            for nxt in active[1:]:
                sig = pair_sig(cur, nxt)
                cur = int(sig.get("b_operator", cur))
            return cur
        except Exception:
            pass
    return active[0]


# ─── Main recall entry ───────────────────────────────────────────────────

def spreading_recall(engine,
                      query: Dict[str, Any],
                      depth: str = "any",
                      k: int = 10,
                      max_steps: int = MAX_STEPS,
                      seed: Optional[int] = None,
                      verbose: bool = False,
                      ) -> List[Dict[str, Any]]:
    """The full SEED -> SPREAD -> LEAP -> FUSE -> EVALUATE loop.

    Args:
        engine: a live CKSimEngine (with HER / lattice_chain / divine_memory /
            truth_lattice / crystals attributes wired)
        query: dict with at least one of 'operators', 'centroid', 'text'
        depth: 'micro' | 'meso' | 'macro' | 'any'
        k: max results to return
        max_steps: bounded recursion depth
        seed: optional RNG seed for deterministic behavior in tests
        verbose: if True, return a per-step log inside each result's 'log' field

    Returns:
        list of result dicts (length <= k), sorted by activation energy:
            {
                'source': str,        # which memory layer
                'data': Any,          # the original retrieved payload
                'score': float,       # original retrieval score
                'energy': float,      # final activation energy
                'depth': str,         # the depth tier the item came from
                'coord': str,         # the 4-axis algebraic signature
                'phase': str,         # which phase activated this item
            }
        plus a meta entry at index -1 with the final coherence + fused op
        when verbose=True.
    """
    rng = random.Random(seed) if seed is not None else random.Random()
    amap = ActivationMap()
    log: List[str] = []
    t0 = time.time()

    # ── Phase 1: SEED ──
    n_seeds = _pull_seeds(engine, query, depth, amap)
    if verbose:
        log.append(f"SEED: {n_seeds} items across {len(amap.cells)} cells")
    if n_seeds == 0:
        return []

    best_C = 0.0
    last_fused_op = amap.dominant_operator()

    # ── Phases 2-5: think loop ──
    for step in range(max_steps):
        amap.step = step

        # SPREAD
        n_spread = _spread_neighbors(engine, amap, rng)
        if verbose:
            log.append(f"  step{step} SPREAD: +{n_spread}")

        # LEAP
        leap_dest = _levy_leap(engine, amap, rng)
        if leap_dest is not None and verbose:
            log.append(f"  step{step} LEAP -> {leap_dest}")

        # FUSE
        fused = _fuse(engine, amap)
        last_fused_op = fused
        if verbose:
            fname = OP_NAMES[fused] if 0 <= fused < 10 else f"<{fused}>"
            log.append(f"  step{step} FUSE -> {fname}")

        # EVALUATE
        C = coherence_C(amap)
        best_C = max(best_C, C)
        if verbose:
            log.append(f"  step{step} C={C:.3f} (best={best_C:.3f}) "
                       f"n_items={len(amap.items)}")

        if C >= T_STAR:
            if verbose:
                log.append(f"  COHERENT at step{step}")
            break

        # DECAY
        amap.decay()

    # ── Compose: rank items by energy and prepare result ──
    ranked = amap.top(k)
    results: List[Dict[str, Any]] = []
    for a in ranked:
        results.append({
            "source": a.source_layer,
            "data": a.payload,
            "score": a.score,
            "energy": a.energy,
            "depth": _depth_for_layer(a.source_layer),
            "coord": str(a.coord),
            "phase": a.source_phase,
        })

    if verbose:
        meta = {
            "source": "_meta",
            "coherence": best_C,
            "fused_op": OP_NAMES[last_fused_op] if 0 <= last_fused_op < 10 else f"<{last_fused_op}>",
            "n_activations": len(amap.items),
            "n_cells": len(amap.cells),
            "elapsed_ms": int((time.time() - t0) * 1000),
            "log": log,
            "T_star_reached": best_C >= T_STAR,
        }
        results.append(meta)
    return results


def _depth_for_layer(layer: str) -> str:
    return {
        "her": "micro",
        "lattice_chain": "meso",
        "divine_memory": "meso",
        "truth_lattice": "macro",
        "crystals": "macro",
        "spread": "meso",
        "leap": "macro",
    }.get(layer, "any")


# ─── Mount hook for gen14_unified_extensions ─────────────────────────────

def mount_spreading_recall(engine) -> bool:
    """Replace engine.recall with the spreading-activation version.

    Idempotent: if a recall function already exists, this overwrites it.
    The old stub remains available at engine.recall_stub for fallback.
    """
    if hasattr(engine, "recall") and engine.recall is not None:
        engine.recall_stub = engine.recall

    def _recall(query: Dict[str, Any], depth: str = "any", k: int = 10,
                seed: Optional[int] = None, verbose: bool = False):
        try:
            return spreading_recall(engine, query, depth=depth, k=k,
                                    seed=seed, verbose=verbose)
        except Exception as e:
            # If anything goes wrong, fall back to the stub
            stub = getattr(engine, "recall_stub", None)
            if callable(stub):
                try:
                    return stub(query, depth=depth, k=k)
                except Exception:
                    pass
            return [{"source": "_error", "data": str(e), "score": 0.0,
                      "energy": 0.0, "depth": "any", "coord": "(error)",
                      "phase": "error"}]

    engine.recall = _recall
    print("[CK Gen14] mount_spreading_recall: full SEED+SPREAD+LEAP+FUSE+EVAL "
          "recall at engine.recall (Phase 3)")
    return True


# ─── Standalone smoke test ───────────────────────────────────────────────

class _MockHER:
    def recall_by_scent(self, centroid, top_k=5):
        # Pretend we have 3 hits, all op HARMONY
        return [{"op": 7, "scent": centroid, "i": i} for i in range(min(3, top_k))]


class _MockLatticeChain:
    def __init__(self):
        # Mock 32 nodes
        self.nodes = {}
        for i in range(32):
            self.nodes[f"node{i}"] = {"op": i % 10, "i": i}

    def walk(self, ops, learn=False):
        return [{"op": op} for op in ops]


class _MockDivineMemory:
    def recall(self, centroid, top_k=5):
        return [{"op": (3 + i) % 10, "score": 0.8 - i * 0.05}
                for i in range(min(3, top_k))]


class _MockEngine:
    def __init__(self):
        self.her = _MockHER()
        self.lattice_chain = _MockLatticeChain()
        self.divine_memory = _MockDivineMemory()


def _smoke():
    print("Smoke test: ck_spreading_activation")
    eng = _MockEngine()
    mount_spreading_recall(eng)

    # Run a recall
    query = {
        "operators": [1, 7, 9, 3],   # F-cycle walk
        "centroid": [0.2, 0.5, 0.7, 0.3, 0.1],
        "text": "harmony",
    }
    results = eng.recall(query, depth="any", k=8, seed=42, verbose=True)
    print(f"  Got {len(results)} results")
    for i, r in enumerate(results):
        if r["source"] == "_meta":
            print(f"  META: coherence={r['coherence']:.3f}, "
                  f"fused={r['fused_op']}, "
                  f"n_act={r['n_activations']}, "
                  f"T*={r['T_star_reached']}, "
                  f"{r['elapsed_ms']}ms")
            for line in r["log"][:8]:
                print(f"    {line}")
        else:
            print(f"  [{i}] {r['source']:15s} {r['phase']:8s} "
                  f"E={r['energy']:.2f} coord={r['coord']}")

    # Coord distance sanity (4 axes, total max 8)
    d_same = coord_distance(coord_from_op(7), coord_from_op(7))
    assert d_same == 0, f"self-distance expected 0, got {d_same}"
    # 7->1: same sigma orbit (both F) BUT crosses 4-core membership
    # and different singleton-shell -> distance ~ 5.
    d_F = coord_distance(coord_from_op(7), coord_from_op(1))
    # 0->5: V to BAL-fixed, both isolated singletons -> distance ~ 6-7
    d_far = coord_distance(coord_from_op(0), coord_from_op(5))
    assert d_far >= d_F, f"V->BAL should be at least as far as H->LATTICE"
    # With a SHARED support set the distance compresses (shell axis becomes 0)
    d_with_support = coord_distance(
        coord_from_op(7, shell_set={0, 1, 7, 9}),
        coord_from_op(1, shell_set={0, 1, 7, 9}),
    )
    assert d_with_support < d_F, (
        f"shared support should shrink distance: bare={d_F}, shared={d_with_support}")
    print(f"\nDistances: 7->7={d_same}, 7->1(singleton)={d_F}, "
          f"7->1(shared-support)={d_with_support}, 0->5={d_far} (max=8)")
    print("Spreading-activation smoke: ALL OK")


if __name__ == "__main__":
    _smoke()
