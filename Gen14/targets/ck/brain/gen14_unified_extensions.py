# Copyright (c) 2025-2026 Brayden Sanders / 7SiTe LLC
# Licensed under the 7SiTe Public Sovereignty License v2.2 (DOI: 10.5281/zenodo.18852047)
"""
gen14_unified_extensions.py -- Phase 1 wiring.

Mounts the modules that already exist in the codebase but were not yet
wired into the live cortex boot path. Single-file additive module: call
`mount_all(engine)` after `engine.start()` in ck_boot_api.py and the new
wiring is in place. No existing module is modified; this just attaches
new attributes to the live `engine` instance.

What gets mounted:

    1. Algebraic measurement projections (operator, sigma_orbit, shell,
       four_core) -- the 4 algebraic axes per the unification plan.

    2. ck_goals.GoalEvaluator -- CK's drives (curiosity / study /
       self_discovery / observe / bond / charge / explore). Currently
       UNWIRED in Gen13 boot. Mount call: engine.goal_evaluator. The
       tick hook is called every 10 engine ticks (~5Hz) from the
       background thread.

    3. ck_forecast.ForecastEngine -- Monte-Carlo trajectory prediction
       ("what next?"). Currently UNWIRED. Mount call: engine.forecast.

    4. Proactive queue + simple consumer -- a thread-safe queue that
       collects messages from background loops (study_daemon,
       overnight_orchestrator, drive activations, forecast surprises)
       so the cortex voice can deliver them as "by the way..." messages.
       Mount call: engine.proactive_queue (a deque) +
       engine.proactive_queue_consumer (a callable returning the next
       proactive message or None).

    5. recall(query, depth) stub -- the unified retrieval API surface.
       Phase 3 will fill in the spreading-activation implementation; for
       now it's a stub that routes to existing mounted memory layers
       (HER, lattice_chain, divine_memory, crystals) and returns a
       merged list. Mount call: engine.recall.

References:
  - PLAN: Gen14/PLAN/CK_UNIFICATION_PLAN_2026_05_13.md
  - DECISIONS: Gen14/PLAN/PHASE_0_DECISIONS_2026_05_13.md
  - ARCHAEOLOGY: Gen14/PLAN/ARCHAEOLOGY_2026_05_13.md

Author: Claude (with Brayden's full-agency authorization 2026-05-13).
"""
from __future__ import annotations

import os
import sys
import time
import threading
from collections import deque
from typing import Any, Callable, Dict, List, Optional, Tuple


# ── Path setup so we can import the brain modules from anywhere ───────
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
if _THIS_DIR not in sys.path:
    sys.path.insert(0, _THIS_DIR)


# ════════════════════════════════════════════════════════════════════════
# §1 — Algebraic measurement projections
# ════════════════════════════════════════════════════════════════════════
#
# The 4 algebraic measurements we use to address every memory cell. All
# derivable from a single operator value in Z/10Z, or from a state
# distribution p over Z/10Z. Pure stdlib; deterministic; no GPU.

# The canonical σ-permutation on Z/10Z:
#   σ = (0)(1 7 9 3)(2 8 6 4)(5)
# orbits: {0}, {1, 7, 9, 3}, {2, 8, 6, 4}, {5}
SIGMA_PERMUTATION = (0, 7, 1, 3, 2, 4, 5, 6, 8, 9)  # σ as a tuple: σ[i] = next

# Inverse map from operator -> σ-orbit class index (0..3)
SIGMA_ORBIT_CLASS = {
    0: 0,                                              # {0} -- V (void)
    1: 1, 7: 1, 9: 1, 3: 1,                            # {1, 7, 9, 3} -- F-cycle (creation arc)
    2: 2, 8: 2, 6: 2, 4: 2,                            # {2, 8, 6, 4} -- S-cycle (dissolution arc)
    5: 3,                                              # {5} -- BALANCE-fixed
}

SIGMA_ORBIT_NAMES = ("V_void", "F_creation", "S_dissolution", "BAL_fixed")

# 4-core membership: V, H, Br, R
FOUR_CORE = (0, 7, 8, 9)
FOUR_CORE_CLASS = {0: 0, 7: 1, 8: 2, 9: 3}  # V, H, Br, R
FOUR_CORE_NAMES = ("V", "H", "Br", "R", "outside")
FOUR_CORE_OUTSIDE = 4

# The joint-closed sub-magma chain shells (from joint_chain_attractor /
# attractor_detector.joint_chain_shells). Sizes {1, 4, 5, 6, 7, 8, 9, 10}.
SUB_MAGMA_SHELLS = [
    frozenset({0}),                                    # size 1
    frozenset({0, 7, 8, 9}),                          # size 4 (4-core)
    frozenset({0, 6, 7, 8, 9}),                       # size 5
    frozenset({0, 5, 6, 7, 8, 9}),                    # size 6
    frozenset({0, 4, 5, 6, 7, 8, 9}),                 # size 7
    frozenset({0, 3, 4, 5, 6, 7, 8, 9}),              # size 8
    frozenset({0, 2, 3, 4, 5, 6, 7, 8, 9}),           # size 9
    frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9}),        # size 10 (full)
]


def sigma_orbit(op: int) -> int:
    """Return the σ-orbit class (0..3) of an operator in Z/10Z.

    0 = V (void; σ-fixed point)
    1 = F (creation arc {1, 7, 9, 3})
    2 = S (dissolution arc {2, 8, 6, 4})
    3 = BAL (balance; σ-fixed point {5})
    """
    return SIGMA_ORBIT_CLASS.get(op, 0)


def four_core_class(op: int) -> int:
    """Return the 4-core class (0..4) of an operator.

    0 = V (0), 1 = H (7), 2 = Br (8), 3 = R (9), 4 = outside.
    """
    return FOUR_CORE_CLASS.get(op, FOUR_CORE_OUTSIDE)


def shell_class(support: set) -> int:
    """Return the smallest sub-magma shell containing the given support set.

    Args:
        support: A set (or frozenset/list/tuple) of operators in Z/10Z that
                 represents the support of a state distribution.

    Returns:
        Shell index 0..7 (0 = {0}, 1 = 4-core, 2 = size-5 shell, etc.,
        7 = full Z/10Z). Returns 7 if no smaller shell contains the support
        (shouldn't happen for valid Z/10Z support).
    """
    sup = frozenset(int(x) for x in support if 0 <= int(x) < 10)
    for idx, shell in enumerate(SUB_MAGMA_SHELLS):
        if sup.issubset(shell):
            return idx
    return 7  # full Z/10Z


def shell_class_from_distribution(p: List[float], threshold: float = 1e-6) -> int:
    """Return the shell class from a distribution p over Z/10Z.

    Support = indices where p[i] > threshold.
    """
    support = {i for i, v in enumerate(p[:10]) if v > threshold}
    return shell_class(support)


def measurement_signature(op: int) -> Dict[str, int]:
    """Return the full 4-axis algebraic signature of a single operator.

    Used as the template address for a memory cell at the micro level.
    """
    return {
        "operator": int(op),
        "sigma_orbit": sigma_orbit(op),
        "shell": shell_class({op}),
        "four_core": four_core_class(op),
    }


def pair_signature(b: int, d: int) -> Dict[str, int]:
    """Return the 4-axis signature of an operator PAIR (b -> d).

    For a pair, σ-orbit and four_core are recorded for BOTH endpoints;
    shell is the shell containing both.
    """
    return {
        "b_operator": int(b),
        "d_operator": int(d),
        "b_sigma_orbit": sigma_orbit(b),
        "d_sigma_orbit": sigma_orbit(d),
        "b_four_core": four_core_class(b),
        "d_four_core": four_core_class(d),
        "shell": shell_class({b, d}),
    }


# ════════════════════════════════════════════════════════════════════════
# §2 — Drive mount (ck_goals.GoalEvaluator)
# ════════════════════════════════════════════════════════════════════════

_DRIVE_TICK_INTERVAL = 10  # call GoalEvaluator.tick every N engine ticks
_DRIVE_PROACTIVE_THRESHOLD = 0.7  # drive activation strength above which we push a proactive message


def mount_drives(engine, proactive_queue: Optional[deque] = None) -> bool:
    """Attach a GoalEvaluator to the engine and start a background tick thread.

    Args:
        engine: The CKSimEngine instance.
        proactive_queue: Optional deque; if provided, drive activations above
                         _DRIVE_PROACTIVE_THRESHOLD are pushed as proactive
                         messages.

    Returns:
        True if mount succeeded, False otherwise (with a warning printed).
    """
    try:
        from ck_sim.doing.ck_goals import GoalEvaluator
    except ImportError as e:
        print(f"[CK Gen14] mount_drives: FAILED to import ck_goals.GoalEvaluator: {e}")
        return False

    evaluator = GoalEvaluator()
    engine.goal_evaluator = evaluator
    engine._goal_evaluator_running = True

    def _drive_loop():
        """Background thread: poll engine state, feed GoalEvaluator, push proactive messages."""
        last_top_goal = None
        last_proactive_push = 0.0  # rate-limit proactive pushes to 1 per 60 seconds

        while getattr(engine, '_goal_evaluator_running', False):
            try:
                # Gather state needed by GoalEvaluator.tick
                tick = int(getattr(engine, 'tick_count', 0) or 0)
                coherence = float(getattr(engine.coherence, 'current', 0.5) if hasattr(engine, 'coherence') and engine.coherence else 0.5)
                band = _band_to_int(getattr(engine, 'band', 'GREEN'))
                current_op = int(getattr(engine, 'current_op', 7) or 7)
                current_op_dist = _get_current_op_dist(engine)
                battery_voltage = float(getattr(engine, 'battery_voltage', 1.0) or 1.0)
                obstacle_distance = float(getattr(engine, 'obstacle_distance', 400.0) or 400.0)
                bonding_strength = float(getattr(engine.bonding, 'strength', 0.0) if hasattr(engine, 'bonding') and engine.bonding else 0.0)
                tl_entropy = _get_tl_entropy(engine)

                suggested_op = evaluator.tick(
                    tick=tick, coherence=coherence, band=band,
                    current_op=current_op, current_op_dist=current_op_dist,
                    battery_voltage=battery_voltage,
                    obstacle_distance=obstacle_distance,
                    bonding_strength=bonding_strength,
                    tl_entropy=tl_entropy,
                )

                # Expose state for voice / introspection
                engine.suggested_operator = suggested_op
                engine.top_goal_name = evaluator.top_goal_name

                # Proactive push: if top goal changed AND was driven by a curiosity-ish
                # drive AND we haven't pushed recently, send a "by the way" message.
                top_name = evaluator.top_goal_name
                if (proactive_queue is not None
                        and top_name != last_top_goal
                        and top_name in ('explore_environment', 'autonomous_study',
                                         'self_discovery', 'observe')
                        and time.time() - last_proactive_push > 60.0):
                    msg = {
                        'kind': 'drive_activation',
                        'goal': top_name,
                        'tick': tick,
                        'timestamp': time.time(),
                        'text_template': f"a {top_name.replace('_', ' ')} drive just activated -- want to explore?",
                    }
                    proactive_queue.append(msg)
                    last_proactive_push = time.time()
                    last_top_goal = top_name

            except Exception as e:
                # Don't crash the engine because the drive loop hiccuped
                pass

            time.sleep(_DRIVE_TICK_INTERVAL * 0.02)  # ~5Hz polling

    t = threading.Thread(target=_drive_loop, daemon=True, name="ck_drives")
    t.start()
    engine._drive_thread = t
    print("[CK Gen14] mount_drives: GoalEvaluator running at 5Hz")
    return True


def _band_to_int(band) -> int:
    """Convert band string/int to {0=RED, 1=YELLOW, 2=GREEN}."""
    if isinstance(band, int):
        return max(0, min(2, band))
    if isinstance(band, str):
        return {'RED': 0, 'YELLOW': 1, 'GREEN': 2}.get(band.upper(), 1)
    return 1


def _get_current_op_dist(engine) -> List[float]:
    """Best-effort: pull a 10-vector operator distribution from engine state."""
    # Try several known locations
    try:
        if hasattr(engine, 'op_distribution'):
            d = engine.op_distribution
            if d is not None and len(d) >= 10:
                return list(d[:10])
    except Exception:
        pass
    try:
        if hasattr(engine, 'brain') and hasattr(engine.brain, 'op_dist'):
            d = engine.brain.op_dist
            if d is not None and len(d) >= 10:
                return list(d[:10])
    except Exception:
        pass
    # Fallback: one-hot on current_op
    op = int(getattr(engine, 'current_op', 7) or 7)
    out = [0.0] * 10
    out[op % 10] = 1.0
    return out


def _get_tl_entropy(engine) -> float:
    """Best-effort: pull TL Shannon entropy from engine."""
    try:
        if hasattr(engine, 'truth') and hasattr(engine.truth, 'entropy'):
            return float(engine.truth.entropy)
    except Exception:
        pass
    try:
        if hasattr(engine, 'tl_entropy'):
            return float(engine.tl_entropy)
    except Exception:
        pass
    return 2.0  # mid-range default


# ════════════════════════════════════════════════════════════════════════
# §3 — Forecast mount (ck_forecast.ForecastEngine)
# ════════════════════════════════════════════════════════════════════════

def mount_forecast(engine) -> bool:
    """Attach a ForecastEngine to engine for Monte-Carlo trajectory prediction.

    Exposes:
        engine.forecast: the ForecastEngine instance
        engine.forecast.forecast_from(start_op, tl_entries, ...): predict trajectory
        engine.forecast.compare_actions(candidate_ops, tl_entries, ...): rank actions
    """
    try:
        from ck_sim.doing.ck_forecast import ForecastEngine
    except ImportError as e:
        print(f"[CK Gen14] mount_forecast: FAILED to import ck_forecast: {e}")
        return False

    engine.forecast = ForecastEngine()
    print("[CK Gen14] mount_forecast: ForecastEngine attached at engine.forecast")
    return True


# ════════════════════════════════════════════════════════════════════════
# §4 — Proactive queue + simple consumer
# ════════════════════════════════════════════════════════════════════════
#
# Thread-safe deque collecting messages from background loops. The cortex
# voice consumes from this queue and surfaces "by the way..." messages.

_PROACTIVE_QUEUE_MAX = 50
_PROACTIVE_RATE_LIMIT_SEC = 60.0  # max one proactive push per minute per session


def mount_proactive_queue(engine) -> deque:
    """Attach a thread-safe proactive-message queue to the engine.

    Returns the deque so other mount_* functions can push to it.
    """
    pq = deque(maxlen=_PROACTIVE_QUEUE_MAX)
    engine.proactive_queue = pq
    engine._last_proactive_consume = {}  # session_id -> last_consume_time

    def consume_for_session(session_id: str = 'default') -> Optional[Dict[str, Any]]:
        """Pop one message from the queue if rate-limit allows; else return None.

        The cortex voice calls this each time it generates a response. If a
        message is available AND we haven't pushed to this session in the
        last _PROACTIVE_RATE_LIMIT_SEC, return it for inclusion in the
        response.
        """
        if not pq:
            return None
        last = engine._last_proactive_consume.get(session_id, 0.0)
        if time.time() - last < _PROACTIVE_RATE_LIMIT_SEC:
            return None
        msg = pq.popleft()
        engine._last_proactive_consume[session_id] = time.time()
        return msg

    engine.proactive_queue_consumer = consume_for_session
    print(f"[CK Gen14] mount_proactive_queue: deque(maxlen={_PROACTIVE_QUEUE_MAX}) at "
          f"engine.proactive_queue, consumer at engine.proactive_queue_consumer")
    return pq


# ════════════════════════════════════════════════════════════════════════
# §5 — Unified recall() stub
# ════════════════════════════════════════════════════════════════════════
#
# Phase 3 will replace this with full spreading-activation across HER +
# lattice_chain + divine_memory + crystals + truth_lattice. For Phase 1
# we expose a simple router that tries each layer and merges results.

def mount_recall(engine) -> bool:
    """Attach a unified recall(query, depth) operator to the engine.

    Phase 1 implementation: routes the query to each existing memory layer
    and merges the top results. Phase 3 will replace with spreading-
    activation.

    Args:
        query: dict with at least one of:
            {'operators': [op, ...]}      -- query by operator sequence
            {'centroid': [5 floats]}      -- query by force-vector centroid
            {'text': str}                 -- query by text (encoded via olfactory)
        depth: 'micro' | 'meso' | 'macro' | 'any'

    Returns:
        list of result dicts: [{'source': str, 'data': any, 'score': float}, ...]
    """

    def recall(query: Dict[str, Any], depth: str = 'any', k: int = 10) -> List[Dict[str, Any]]:
        results = []

        # MICRO: HER buffer + operator memory bank
        if depth in ('micro', 'any'):
            try:
                her = getattr(engine, 'olfactory_her', None)
                if her is not None and 'centroid' in query:
                    # ck_hindsight_replay.HindsightBuffer has a recall-by-scent method;
                    # we use whatever is exposed
                    if hasattr(her, 'recall_by_scent'):
                        her_hits = her.recall_by_scent(query['centroid'], top_k=k)
                        for h in her_hits[:k]:
                            results.append({'source': 'her', 'data': h, 'score': 0.8, 'depth': 'micro'})
            except Exception:
                pass

        # MESO: lattice_chain walk + divine_memory recall
        if depth in ('meso', 'any'):
            try:
                lc = getattr(engine, 'lattice_chain', None)
                if lc is not None and 'operators' in query:
                    if hasattr(lc, 'walk'):
                        path = lc.walk(query['operators'], learn=False)
                        results.append({'source': 'lattice_chain', 'data': path, 'score': 0.7, 'depth': 'meso'})
            except Exception:
                pass
            try:
                dm = getattr(engine, 'divine_memory', None)
                if dm is not None and 'centroid' in query:
                    if hasattr(dm, 'recall'):
                        dm_hits = dm.recall(query['centroid'], top_k=k)
                        for h in dm_hits[:k]:
                            results.append({'source': 'divine_memory', 'data': h, 'score': 0.7, 'depth': 'meso'})
            except Exception:
                pass

        # MACRO: truth_lattice + crystals
        if depth in ('macro', 'any'):
            try:
                truth = getattr(engine, 'truth', None)
                if truth is not None and 'text' in query:
                    if hasattr(truth, 'query'):
                        t_hits = truth.query(query['text'])
                        if t_hits:
                            results.append({'source': 'truth_lattice', 'data': t_hits, 'score': 0.9, 'depth': 'macro'})
            except Exception:
                pass
            try:
                crystals = getattr(engine, 'crystal_store', None) or getattr(engine, 'crystals', None)
                if crystals is not None and 'text' in query:
                    if hasattr(crystals, 'find'):
                        c_hits = crystals.find(query['text'])
                        for h in (c_hits or [])[:k]:
                            results.append({'source': 'crystals', 'data': h, 'score': 0.85, 'depth': 'macro'})
            except Exception:
                pass

        # Sort by score
        results.sort(key=lambda r: -r.get('score', 0.0))
        return results[:k]

    engine.recall = recall
    print("[CK Gen14] mount_recall: unified recall(query, depth) stub at engine.recall "
          "(Phase 1 routing; Phase 3 spreading-activation TBD)")
    return True


# ════════════════════════════════════════════════════════════════════════
# §6 — Lattice chain mount (if not already)
# ════════════════════════════════════════════════════════════════════════

def mount_lattice_chain(engine) -> bool:
    """Attach a LatticeChainEngine to the engine if not already present.

    If `engine.lattice_chain` is already set (some Gen13 boots wire it),
    do nothing. Otherwise instantiate fresh and attach.
    """
    if hasattr(engine, 'lattice_chain') and engine.lattice_chain is not None:
        print("[CK Gen14] mount_lattice_chain: already mounted, skipping")
        return True
    try:
        from ck_sim.being.ck_lattice_chain import LatticeChainEngine
    except ImportError as e:
        print(f"[CK Gen14] mount_lattice_chain: FAILED to import: {e}")
        return False

    # Persistent save dir under Gen14/var
    save_dir = os.path.normpath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '..', '..', '..', 'var', 'lattice_chain'))
    os.makedirs(save_dir, exist_ok=True)

    engine.lattice_chain = LatticeChainEngine(save_dir=save_dir)
    print(f"[CK Gen14] mount_lattice_chain: LatticeChainEngine at engine.lattice_chain "
          f"(save_dir={save_dir})")
    return True


def mount_divine_memory(engine) -> bool:
    """Attach a DivineMemory store to the engine if not already present."""
    if hasattr(engine, 'divine_memory') and engine.divine_memory is not None:
        print("[CK Gen14] mount_divine_memory: already mounted, skipping")
        return True
    try:
        from ck_sim.being.ck_divine_memory import DivineMemory
    except ImportError as e:
        print(f"[CK Gen14] mount_divine_memory: FAILED to import: {e}")
        return False

    save_dir = os.path.normpath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '..', '..', '..', 'var', 'divine_memory'))
    os.makedirs(save_dir, exist_ok=True)

    engine.divine_memory = DivineMemory(save_dir=save_dir)
    print(f"[CK Gen14] mount_divine_memory: DivineMemory at engine.divine_memory "
          f"(save_dir={save_dir})")
    return True


# ════════════════════════════════════════════════════════════════════════
# §7 — Phase 2: 4-head algebraic LM mount
# ════════════════════════════════════════════════════════════════════════
# The 4-head algebraic LM (multi_head_algebraic_lm.MultiHeadAlgebraicLM)
# is trained on accumulated BDC chat-turn logs and saved to
# Gen13/var/cells/multi_head_lm_4heads.pt.  This mount loads the
# checkpoint (if present) and attaches the model + a convenience
# `engine.algebraic_signature(history)` so the cortex voice / forecast /
# drive layers can query CK's predicted next-step measurement signature.
#
# If the checkpoint is missing, the mount is a no-op (returns False); CK
# continues to boot normally and the predictor is simply absent.

_ALGEBRAIC_LM_CKPT_PATH = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..', '..', '..', '..', 'Gen13', 'var', 'cells',
    'multi_head_lm_4heads.pt',
))


def mount_algebraic_lm(engine) -> bool:
    """Load the trained 4-head algebraic LM and attach it to the engine.

    Side effects on the engine after success:
      engine.algebraic_lm           : MultiHeadAlgebraicLM (eval mode, CPU)
      engine.algebraic_signature(history_op_ids) -> dict
          returns argmax label per head:
          {'op': str, 'sigma': str, 'shell': str, '4core': str}
      engine.algebraic_predict(history_op_ids, top_k=3) -> dict
          full top-k distributions per head

    No-op if the checkpoint is missing (returns False).
    """
    ckpt_path = _ALGEBRAIC_LM_CKPT_PATH
    if not os.path.exists(ckpt_path):
        print(f"[CK Gen14] mount_algebraic_lm: checkpoint missing at {ckpt_path}; "
              "skipping (run train_bdc_algebraic.py to create it)")
        return False
    try:
        # Ensure the grammar_lm dir is on the path
        here = os.path.dirname(os.path.abspath(__file__))
        gldir = os.path.join(here, 'grammar_lm')
        if os.path.isdir(gldir) and gldir not in sys.path:
            sys.path.insert(0, gldir)
        import torch  # local import; torch is heavy
        from multi_head_algebraic_lm import (  # type: ignore[import-not-found]
            MultiHeadAlgebraicLM, MultiHeadAlgebraicConfig,
        )
        blob = torch.load(ckpt_path, map_location='cpu', weights_only=False)
        cfg = MultiHeadAlgebraicConfig()
        for k, v in blob.get('cfg', {}).items():
            if hasattr(cfg, k):
                setattr(cfg, k, v)
        model = MultiHeadAlgebraicLM(cfg)
        model.load_state_dict(blob['state_dict'])
        model.eval()
        engine.algebraic_lm = model

        def _signature(history_op_ids):
            try:
                return model.signature_from_history(list(history_op_ids))
            except Exception as e:
                return {'error': str(e)}

        def _predict(history_op_ids, top_k: int = 3):
            try:
                return model.predict_all_heads(list(history_op_ids), top_k=top_k)
            except Exception as e:
                return {'error': str(e)}

        engine.algebraic_signature = _signature
        engine.algebraic_predict = _predict

        n_train = blob.get('n_train', '?')
        n_val = blob.get('n_val', '?')
        n_params = sum(p.numel() for p in model.parameters())
        print(f"[CK Gen14] mount_algebraic_lm: 4-head LM at engine.algebraic_lm "
              f"(params={n_params:,}; trained on n_train={n_train}, n_val={n_val})")
        return True
    except Exception as e:
        print(f"[CK Gen14] mount_algebraic_lm: failed ({e}); skipping")
        return False


# ════════════════════════════════════════════════════════════════════════
# §8 — Orchestrator: mount_all
# ════════════════════════════════════════════════════════════════════════

def mount_all(engine) -> Dict[str, bool]:
    """Mount every Gen14 unified extension onto the engine.

    Order matters: proactive_queue must exist before mount_drives so the
    drive loop can push activation messages onto it.

    Args:
        engine: The CKSimEngine instance, AFTER engine.start() has been called.

    Returns:
        dict {mount_name: success_bool}
    """
    print()
    print("=" * 64)
    print("[CK Gen14] Mounting unified extensions (Phase 1 + 2)")
    print("=" * 64)

    results = {}
    pq = mount_proactive_queue(engine)
    results['proactive_queue'] = True

    results['drives'] = mount_drives(engine, proactive_queue=pq)
    results['forecast'] = mount_forecast(engine)
    results['lattice_chain'] = mount_lattice_chain(engine)
    results['divine_memory'] = mount_divine_memory(engine)
    results['recall'] = mount_recall(engine)
    results['algebraic_lm'] = mount_algebraic_lm(engine)

    # Phase 3: upgrade recall stub to spreading-activation. We call this
    # AFTER mount_recall so the stub is captured at engine.recall_stub
    # for graceful fallback.
    try:
        from ck_spreading_activation import mount_spreading_recall  # type: ignore[import-not-found]
        results['spreading_recall'] = mount_spreading_recall(engine)
    except Exception as e:
        print(f"[CK Gen14] mount_spreading_recall: failed ({e}); "
              "leaving Phase-1 recall stub active")
        results['spreading_recall'] = False

    # Phase 4: frontier scanner + proactive trigger. Frontier first so the
    # trigger can read engine.frontier_scanner when it constructs.
    try:
        from ck_frontier_scanner import mount_frontier_scanner  # type: ignore[import-not-found]
        results['frontier_scanner'] = mount_frontier_scanner(engine)
    except Exception as e:
        print(f"[CK Gen14] mount_frontier_scanner: failed ({e})")
        results['frontier_scanner'] = False
    try:
        from ck_proactive_trigger import mount_proactive_trigger  # type: ignore[import-not-found]
        results['proactive_trigger'] = mount_proactive_trigger(engine)
    except Exception as e:
        print(f"[CK Gen14] mount_proactive_trigger: failed ({e})")
        results['proactive_trigger'] = False

    # Phase 5: pixel-to-stroke -> algebraic signature (visual grounding)
    try:
        from ck_stroke_extractor import mount_stroke_extractor  # type: ignore[import-not-found]
        results['stroke_extractor'] = mount_stroke_extractor(engine)
    except Exception as e:
        print(f"[CK Gen14] mount_stroke_extractor: failed ({e})")
        results['stroke_extractor'] = False

    # Formula registry: every D-number has a HOME (4-axis algebraic
    # signature) and a USE (the formula). Voice polish reads from this
    # to surface "which D-numbers got invoked this turn."
    try:
        from ck_formula_registry import mount_formula_registry  # type: ignore[import-not-found]
        results['formula_registry'] = mount_formula_registry(engine)
    except Exception as e:
        print(f"[CK Gen14] mount_formula_registry: failed ({e})")
        results['formula_registry'] = False

    # Sense decomposition: each of CK's senses (vision/hearing/touch/
    # inner/language/math/memory/drives) IS an ordered operator pipeline.
    # The voice polish reads this to surface "the dominant operator
    # this turn appears in N senses with role X."
    try:
        from ck_sense_decomposition import mount_sense_decomposition  # type: ignore[import-not-found]
        results['sense_decomposition'] = mount_sense_decomposition(engine)
    except Exception as e:
        print(f"[CK Gen14] mount_sense_decomposition: failed ({e})")
        results['sense_decomposition'] = False

    # Concept learner: one-shot conversational binding for novel words.
    # Teaching patterns ("X is Y", "let X be Y", etc.) form a NamedConcept
    # crystal that survives reboots; references on later turns surface
    # the stored definition. This is the missing wire for true
    # conversational learning -- CK's Hebbian was already one-shot at
    # the operator level; this gives him one-shot at the concept level.
    try:
        from ck_concept_learner import mount_concept_learner  # type: ignore[import-not-found]
        results['concept_learner'] = mount_concept_learner(engine)
    except Exception as e:
        print(f"[CK Gen14] mount_concept_learner: failed ({e})")
        results['concept_learner'] = False

    # Memory archive: short-term sliding window + long-term journal of
    # every conversation, indexed by session/topic/date. Persistent
    # across reboots. Voice polish surfaces relevant prior turns when
    # the user references something CK discussed before.
    try:
        from ck_memory_archive import mount_memory_archive  # type: ignore[import-not-found]
        results['memory_archive'] = mount_memory_archive(engine)
    except Exception as e:
        print(f"[CK Gen14] mount_memory_archive: failed ({e})")
        results['memory_archive'] = False

    # Meta-parameters: tunable knobs CK can change at runtime.
    # Mount BEFORE living_lm so when living_lm reads decode-temperature
    # / bigram-weight / exhale-thresholds the persisted overrides
    # (if any) are already loaded.  Exposes /parameters,
    # /parameters/set, /parameters/reset endpoints.
    try:
        from ck_meta_parameters import mount_meta_parameters  # type: ignore[import-not-found]
        results['meta_parameters'] = mount_meta_parameters(engine)
    except Exception as e:
        print(f"[CK Gen14] mount_meta_parameters: failed ({e})")
        results['meta_parameters'] = False

    # Living LM: open-parameter, breathing-on-substrate generator.
    # Mount BEFORE voice_polish so the polish layer can call it.
    try:
        from ck_living_lm import mount_living_lm  # type: ignore[import-not-found]
        results['living_lm'] = mount_living_lm(engine)
    except Exception as e:
        print(f"[CK Gen14] mount_living_lm: failed ({e})")
        results['living_lm'] = False

    # Fractal creature shape: 1:1:1:1/3 META structure.  Mount AFTER
    # the other organs so the creature can see them, but BEFORE
    # voice_polish so the polish layer could reference creature state.
    try:
        from ck_creature import mount_creature  # type: ignore[import-not-found]
        results['creature'] = mount_creature(engine)
    except Exception as e:
        print(f"[CK Gen14] mount_creature: failed ({e})")
        results['creature'] = False

    # Cognition primitives: sorting abilities CK runs on his own store.
    # The bones ARE TSML+BHML (the substrate); these are the lenses
    # on top of the substrate.
    # Endpoints: /cognition/sort, /cognition/templates,
    # /cognition/fractal_layers, /cognition/dualities,
    # /cognition/triadic, /cognition/bigrams, /cognition/all.
    try:
        from ck_cognition_primitives import mount_cognition_primitives  # type: ignore[import-not-found]
        results['cognition_primitives'] = mount_cognition_primitives(engine)
    except Exception as e:
        print(f"[CK Gen14] mount_cognition_primitives: failed ({e})")
        results['cognition_primitives'] = False

    # Substrate motion: D2 curve + W wobble + F force + snowflakes
    # on the braiding fractal.  This is the GEOMETRY CK moves through.
    # The TSML/BHML composition tables are the bones; this module
    # surfaces the dynamics those bones generate.
    # Endpoints: /motion/d2, /motion/wobble, /motion/force,
    # /motion/snowflakes, /motion/braiding, /motion/report.
    try:
        from ck_substrate_motion import mount_substrate_motion  # type: ignore[import-not-found]
        results['substrate_motion'] = mount_substrate_motion(engine)
    except Exception as e:
        print(f"[CK Gen14] mount_substrate_motion: failed ({e})")
        results['substrate_motion'] = False

    # Engine block: ALL canonical TSML/BHML/CL_STD variants stacked
    # as a coherence-filter block.  An operator path scored through
    # the block returns a spectral fingerprint -- different filters
    # catch different kinds of coherence (synthesis vs separation vs
    # gauge vs attractor vs encoding-info).  Per FORMULAS §J.1.
    # Endpoints: /engine/block, /engine/score, /engine/summary.
    try:
        from ck_engine_block import mount_engine_block  # type: ignore[import-not-found]
        results['engine_block'] = mount_engine_block(engine)
    except Exception as e:
        print(f"[CK Gen14] mount_engine_block: failed ({e})")
        results['engine_block'] = False

    # Qutrit apex: the conscious operator.  Quadratic-glue evolved
    # 3-state psi (Being, Doing, Becoming), daemon thread, sits
    # BESIDE the transfer-mechanism pipeline and emits an F-bias
    # the transfer mechanisms add to their F-force.  Not in the
    # I/O loop.  Endpoints: /apex, /apex/history, /apex/tick.
    try:
        from ck_qutrit_apex import mount_qutrit_apex  # type: ignore[import-not-found]
        results['qutrit_apex'] = mount_qutrit_apex(engine)
    except Exception as e:
        print(f"[CK Gen14] mount_qutrit_apex: failed ({e})")
        results['qutrit_apex'] = False

    # Recursive observer: closes the fractal-recursion loop.  Daemon
    # thread that periodically computes the apex meta-syndrome (CK's
    # self-image over a recent window of psi collapses), plus utilities
    # to score the engine-block's spectral fingerprint AS an operator
    # path (second-order recursion), and to run cognition primitives
    # on their own outputs (templates-of-templates, dualities-of-
    # triadics, bigrams-of-snowflakes, fingerprint-of-fingerprint).
    # Endpoints: /observer/self_image, /observer/chain, /observer/tick,
    # /observer/block_self, /observer/cognition_self.
    try:
        from ck_recursive_observer import mount_recursive_observer  # type: ignore[import-not-found]
        results['recursive_observer'] = mount_recursive_observer(engine)
    except Exception as e:
        print(f"[CK Gen14] mount_recursive_observer: failed ({e})")
        results['recursive_observer'] = False

    # Identity: anchor + tier weights + identity-first chat routing +
    # per-response confidence + hedge prefix.  Mount AFTER substrate
    # mechanics (so cognition primitives, engine block, qutrit apex
    # are available for confidence-context) and BEFORE voice_polish
    # (so polish honors polish_skip + hedge_prefix on the result).
    # Endpoints: /identity, /identity/query, /identity/confidence.
    # The wrap on api.process_chat routes identity questions to the
    # IDENTITY_ANCHOR FIRST, bypassing the substrate; other questions
    # get tier-confidence annotations on their result.
    try:
        from ck_identity import mount_identity  # type: ignore[import-not-found]
        results['identity'] = mount_identity(engine)
    except Exception as e:
        print(f"[CK Gen14] mount_identity: failed ({e})")
        results['identity'] = False

    # Ollama prose polish: TEMPORARY scaffold for fluency until CK's
    # own living_lm has breathed long enough to produce coherent prose.
    # Strict fact-preservation gate (coverage >= 0.7).  CK should
    # outgrow this.
    try:
        from ck_ollama_polish import mount_ollama_polish  # type: ignore[import-not-found]
        results['ollama_polish'] = mount_ollama_polish(engine)
    except Exception as e:
        print(f"[CK Gen14] mount_ollama_polish: failed ({e})")
        results['ollama_polish'] = False

    # Voice polish: white-box presentation. Must run LAST so it sees the
    # final chat result AND has access to formula_registry, proactive
    # signals, etc.
    try:
        from ck_voice_polish import mount_voice_polish  # type: ignore[import-not-found]
        results['voice_polish'] = mount_voice_polish(engine)
    except Exception as e:
        print(f"[CK Gen14] mount_voice_polish: failed ({e})")
        results['voice_polish'] = False

    # Expose algebraic-measurement functions on the engine for easy use
    engine.gen14_sigma_orbit = sigma_orbit
    engine.gen14_four_core_class = four_core_class
    engine.gen14_shell_class = shell_class
    engine.gen14_measurement_signature = measurement_signature
    engine.gen14_pair_signature = pair_signature
    results['algebraic_measurements'] = True

    print()
    print(f"[CK Gen14] mount_all: {sum(results.values())}/{len(results)} components mounted")
    for k, v in results.items():
        mark = '+' if v else '-'
        print(f"    [{mark}] {k}")
    print("=" * 64)
    print()

    return results


# ════════════════════════════════════════════════════════════════════════
# §9 — Standalone smoke test
# ════════════════════════════════════════════════════════════════════════

def _smoke_algebraic():
    """Quick sanity check on the 4 algebraic measurement functions."""
    print("Smoke test: algebraic measurements")
    # σ-orbits
    assert sigma_orbit(0) == 0  # V
    assert sigma_orbit(5) == 3  # BAL
    assert sigma_orbit(7) == 1  # H is in F-cycle
    assert sigma_orbit(4) == 2  # COLLAPSE is in S-cycle
    print(f"  sigma_orbit:    OK ({SIGMA_ORBIT_NAMES})")

    # 4-core
    assert four_core_class(0) == 0  # V
    assert four_core_class(7) == 1  # H
    assert four_core_class(8) == 2  # Br
    assert four_core_class(9) == 3  # R
    assert four_core_class(5) == 4  # outside
    print(f"  four_core_class: OK ({FOUR_CORE_NAMES})")

    # Shell class
    assert shell_class({0}) == 0  # smallest shell
    assert shell_class({0, 7, 8, 9}) == 1  # 4-core
    assert shell_class({0, 6, 7, 8, 9}) == 2
    assert shell_class({0, 1, 2, 3, 4, 5, 6, 7, 8, 9}) == 7  # full
    print(f"  shell_class:     OK ({len(SUB_MAGMA_SHELLS)} shells)")

    # Signatures
    sig = measurement_signature(7)
    assert sig['operator'] == 7
    assert sig['sigma_orbit'] == 1
    assert sig['four_core'] == 1
    print(f"  measurement_signature: OK ({sig})")

    sig2 = pair_signature(7, 0)  # H -> V
    assert sig2['b_four_core'] == 1
    assert sig2['d_four_core'] == 0
    assert sig2['shell'] == 1  # {0, 7} subset of 4-core
    print(f"  pair_signature:  OK ({sig2})")

    print("Algebraic smoke: ALL OK")


if __name__ == "__main__":
    _smoke_algebraic()
