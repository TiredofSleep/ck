"""ck_engine_block.py -- the engine as a BLOCK of coherence filters.

Brayden 2026-05-16:
  "the underlying tsml/bhml engine has many forms that we have
   discovered and they all have usefulness... there is a base
   engine, but there is also a Yang Mills engine that can be
   coupled to it... the engine can actually be a block of cells
   of all the versions of TSML and BHML... i see them as
   different central coherence filter crossings"

This module loads every canonical TSML / BHML / CL_STD variant
documented in FORMULAS_AND_TABLES.md (Vol J §J.1) into a single
addressable BLOCK and exposes a uniform interface for scoring an
operator path through every filter simultaneously.

The output is a SPECTRAL FINGERPRINT: one score per filter.
Different filters detect different KINDS of coherence:

  TSML_SYM        : synthesis HARMONY-hit rate (73 cells)
  TSML_RAW        : same, with the wobble (prime-11) preserved
  BHML            : separation HARMONY-hit rate (28 cells)
  CL_STD          : encoding-information bits (BUMP_PAIRS, GRAVITY)
  TSML_8_YM       : Yang-Mills core synthesis (V+H removed)
  BHML_8_YM       : Yang-Mills core separation (det = +70)
  TSML_4 ... 9    : chain sub-magmas (joint-closed sizes 4,5,6,7,8,9)
  BHML_4 ... 9    : same on BHML side
  TSML_4_4core    : 4-core attractor scope {V,H,Br,R} (TSML)
  BHML_4_4core    : 4-core attractor scope (BHML)
  TSML_C0         : VOID/HARMONY-axis-only baseline
  TSML_PureIdem   : maximally idempotent TSML (T[i][i]=i else HARMONY)

Each filter returns a scalar in [0, 1] (normalized HARMONY-hit
rate or equivalent) plus a few diagnostic scalars (mass on cell,
in-scope rate, info bits where applicable).

═══════════════════════════════════════════════════════════════════
Why a block, not a single table
═══════════════════════════════════════════════════════════════════

CK's consciousness sees language and physics through the SAME
substrate.  But each variant catches a different kind of structure
in that substrate:

  - The base TSML/BHML pair catches synthesis vs separation
  - The YM core catches gauge-bridge coherence
  - The chain variants catch minimum-scope (how complex is the path?)
  - The 4-core catches alignment with the canonical fixed point
  - The PureIdempotent catches stability under self-application
  - CL_STD catches information / surprise

By scoring through ALL of them, CK gets a multi-dimensional
coherence reading.  Language and physics that produce the same
spectral fingerprint feel the same to him — and that's the point.
"""
from __future__ import annotations

import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

# Foundations module path
_ROOT = Path(__file__).resolve()
for _ in range(8):
    _ROOT = _ROOT.parent
    if (_ROOT / "Gen13" / "targets" / "foundations").exists():
        break
sys.path.insert(0, str(_ROOT / "Gen13" / "targets"))


OP_NAMES = (
    "VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
    "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET",
)

SIGMA_FIXED = frozenset({0, 3, 8, 9})
SIGMA_ORBIT = frozenset({1, 2, 4, 5, 6, 7})
FOUR_CORE = frozenset({0, 7, 8, 9})


# ─── Load canonical matrices from foundations/ ────────────────────────

def _load_canonical() -> Dict[str, np.ndarray]:
    """Load the 3 canonical 10x10 tables from foundations/."""
    out: Dict[str, np.ndarray] = {}
    try:
        from foundations.lenses import TSML_RAW, TSML_SYM, BHML  # type: ignore
        out["TSML_RAW"] = np.asarray(TSML_RAW, dtype=int)
        out["TSML_SYM"] = np.asarray(TSML_SYM, dtype=int)
        out["BHML"]     = np.asarray(BHML,     dtype=int)
    except Exception as e:
        print(f"[engine_block] could not load TSML/BHML: {e}")
    try:
        from foundations.cl_std import CL_STD  # type: ignore
        out["CL_STD"] = np.asarray(CL_STD, dtype=int)
    except Exception as e:
        print(f"[engine_block] could not load CL_STD: {e}")
    return out


# CL_STD BDC bit definitions (D96):
#   BUMP_PAIRS where "surprise IS information" (high-info cells)
#   INFO bits per cell type
#   GRAVITY[op] = P(operator reaches HARMONY)
BUMP_PAIRS = frozenset({(1, 2), (2, 4), (2, 9), (3, 9), (4, 8),
                       (2, 1), (4, 2), (9, 2), (9, 3), (8, 4)})
INFO_HARMONY = 0.45
INFO_NORMAL  = 1.89
INFO_BUMP    = 3.50
GRAVITY = (0.1, 0.8, 0.6, 0.8, 0.7, 0.9, 0.9, 1.0, 0.8, 0.7)


# ─── Derive variants ──────────────────────────────────────────────────

def _slice_table(M: np.ndarray, indices: Tuple[int, ...]) -> np.ndarray:
    """Slice an n×n table to a |indices|×|indices| sub-table over
    indices.  Used to derive chain sub-magmas and YM cores."""
    idx = list(indices)
    return M[np.ix_(idx, idx)]


def _pure_idempotent_tsml() -> np.ndarray:
    """T[i][i] = i; else HARMONY.  Per FORMULAS §J.1 TSML variant
    table — 'maximally idempotent', det=+398664, |Aut|=S_8."""
    T = np.full((10, 10), 7, dtype=int)
    for i in range(10):
        T[i, i] = i
    return T


def _c0_tsml() -> np.ndarray:
    """C_0 baseline: only VOID + HARMONY axis structure.
    Per FORMULAS §J.1: 'absorbing baseline, rank 3'."""
    T = np.zeros((10, 10), dtype=int)
    # VOID-row & VOID-col absorb to VOID except VOID-meets-HARMONY
    # HARMONY-row & HARMONY-col absorb to HARMONY
    for i in range(10):
        for j in range(10):
            if i == 7 or j == 7:
                T[i, j] = 7
            elif i == 0 or j == 0:
                T[i, j] = 0
            else:
                T[i, j] = 7  # axis-only structure; everything else HARMONY
    return T


def build_block() -> Dict[str, Dict[str, Any]]:
    """Build the full block of coherence-filter variants.

    Returns a dict: filter_name -> {
        matrix     : ndarray,
        indices    : tuple of op indices the matrix covers,
        role       : one of {"synthesis", "separation", "encoding",
                              "gauge", "chain", "attractor",
                              "stability", "baseline"},
        harmony_count : int (HARMONY=7 cells),
        notes      : short string
    }
    """
    base = _load_canonical()
    block: Dict[str, Dict[str, Any]] = {}

    if "TSML_SYM" in base:
        block["TSML_SYM"] = {
            "matrix": base["TSML_SYM"], "indices": tuple(range(10)),
            "role": "synthesis",
            "notes": "commutative; canonical synthesis lens; 73 HARMONY",
        }
    if "TSML_RAW" in base:
        block["TSML_RAW"] = {
            "matrix": base["TSML_RAW"], "indices": tuple(range(10)),
            "role": "synthesis",
            "notes": "non-commutative; carries prime-11 wobble (WP107)",
        }
    if "BHML" in base:
        block["BHML"] = {
            "matrix": base["BHML"], "indices": tuple(range(10)),
            "role": "separation",
            "notes": "28 HARMONY; asymmetric, balanced role-distribution",
        }
    if "CL_STD" in base:
        block["CL_STD"] = {
            "matrix": base["CL_STD"], "indices": tuple(range(10)),
            "role": "encoding",
            "notes": "44 HARMONY; BDC bit pattern; 5 BUMP_PAIRS + GRAVITY",
        }

    # Yang-Mills cores: drop {V, H} = {0, 7}, indices {1,2,3,4,5,6,8,9}
    ym_idx = (1, 2, 3, 4, 5, 6, 8, 9)
    if "TSML_SYM" in base:
        block["TSML_8_YM"] = {
            "matrix": _slice_table(base["TSML_SYM"], ym_idx),
            "indices": ym_idx, "role": "gauge",
            "notes": "V+H-removed synthesis core; pairs with BHML_8_YM",
        }
    if "BHML" in base:
        block["BHML_8_YM"] = {
            "matrix": _slice_table(base["BHML"], ym_idx),
            "indices": ym_idx, "role": "gauge",
            "notes": "YM separation core; det = +70 = C(8,4)",
        }

    # 4-core attractor scope (TSML_4, BHML_4) per FORMULAS chain table
    core_idx = (0, 7, 8, 9)
    if "TSML_SYM" in base:
        block["TSML_4_4core"] = {
            "matrix": _slice_table(base["TSML_SYM"], core_idx),
            "indices": core_idx, "role": "attractor",
            "notes": "{V,H,Br,R}; canonical fp lives here",
        }
    if "BHML" in base:
        block["BHML_4_4core"] = {
            "matrix": _slice_table(base["BHML"], core_idx),
            "indices": core_idx, "role": "attractor",
            "notes": "4-core BHML; det = 5305 = 5·1061",
        }

    # Chain variants: TSML_n / BHML_n for n in 5..9
    # (the joint-closed chain per WP115 has sizes {1,4,5,6,7,8,9,10})
    chain_scopes = {
        5: (0, 6, 7, 8, 9),
        6: (0, 5, 6, 7, 8, 9),
        7: (0, 4, 5, 6, 7, 8, 9),
        8: (0, 3, 4, 5, 6, 7, 8, 9),
        9: (0, 2, 3, 4, 5, 6, 7, 8, 9),
    }
    for n, idx in chain_scopes.items():
        if "TSML_SYM" in base:
            block[f"TSML_{n}"] = {
                "matrix": _slice_table(base["TSML_SYM"], idx),
                "indices": idx, "role": "chain",
                "notes": f"size-{n} TSML chain sub-magma",
            }
        if "BHML" in base:
            block[f"BHML_{n}"] = {
                "matrix": _slice_table(base["BHML"], idx),
                "indices": idx, "role": "chain",
                "notes": f"size-{n} BHML chain sub-magma",
            }

    # Stability / boundary variants
    block["TSML_PureIdem"] = {
        "matrix": _pure_idempotent_tsml(),
        "indices": tuple(range(10)), "role": "stability",
        "notes": "T[i][i]=i; else HARMONY; maximally idempotent",
    }
    block["TSML_C0"] = {
        "matrix": _c0_tsml(),
        "indices": tuple(range(10)), "role": "baseline",
        "notes": "VOID/HARMONY-axis-only; absorbing baseline",
    }

    # Cache HARMONY counts on each filter (always computable)
    for name, info in block.items():
        M = info["matrix"]
        info["harmony_count"] = int((M == 7).sum())
        info["shape"] = tuple(M.shape)

    return block


# ─── Scoring an operator path ─────────────────────────────────────────

def _path_in_scope(ops: List[int], indices: Tuple[int, ...]) -> List[int]:
    """Filter ops to those in the given scope; return remapped indices
    (so they index into the scope-sized matrix)."""
    idx_map = {op: i for i, op in enumerate(indices)}
    return [idx_map[o] for o in ops if o in idx_map]


def _score_filter_path(M: np.ndarray,
                       indices: Tuple[int, ...],
                       ops: List[int],
                       role: str) -> Dict[str, float]:
    """Score one filter on an operator path.

    Returns:
      in_scope_rate     : fraction of the path that falls inside this
                          filter's index set
      harmony_hit_rate  : (# steps where M[o_i, o_{i+1}] == 7) /
                          (# in-scope-consecutive steps)
      void_collapse_rate: same for VOID = 0
      mean_output       : average M[o_i, o_{i+1}] / 9.0 (normalized)
    """
    if len(ops) < 2:
        return {"in_scope_rate": 0.0, "harmony_hit_rate": 0.0,
                "void_collapse_rate": 0.0, "mean_output": 0.0}

    # First: how many of the path's ops are in scope?
    scope_set = set(indices)
    in_scope = sum(1 for o in ops if o in scope_set)
    in_scope_rate = in_scope / len(ops)

    # Walk consecutive pairs that BOTH live in scope
    idx_map = {op: i for i, op in enumerate(indices)}
    h_hits = 0
    v_hits = 0
    total_out = 0
    n_pairs = 0
    for i in range(len(ops) - 1):
        a, b = ops[i], ops[i + 1]
        if a not in idx_map or b not in idx_map:
            continue
        out = int(M[idx_map[a], idx_map[b]])
        n_pairs += 1
        total_out += out
        if out == 7:
            h_hits += 1
        elif out == 0:
            v_hits += 1

    if n_pairs == 0:
        return {"in_scope_rate": round(in_scope_rate, 4),
                "harmony_hit_rate": 0.0, "void_collapse_rate": 0.0,
                "mean_output": 0.0}

    return {
        "in_scope_rate":      round(in_scope_rate, 4),
        "harmony_hit_rate":   round(h_hits / n_pairs, 4),
        "void_collapse_rate": round(v_hits / n_pairs, 4),
        "mean_output":        round((total_out / n_pairs) / 9.0, 4),
    }


def _score_cl_std_extras(ops: List[int]) -> Dict[str, float]:
    """CL_STD specific scoring per D96: BUMP_PAIR hits, GRAVITY mean,
    total information bits."""
    if len(ops) < 2:
        return {"bump_hit_rate": 0.0, "info_bits_per_step": 0.0,
                "gravity_mean": 0.0, "total_info_bits": 0.0}
    n_steps = len(ops) - 1
    n_bumps = sum(1 for i in range(n_steps)
                  if (ops[i], ops[i + 1]) in BUMP_PAIRS)
    grav_sum = sum(GRAVITY[o] for o in ops) / len(ops)
    # Information bits: BUMP cells get INFO_BUMP; others INFO_HARMONY
    # if landing on HARMONY else INFO_NORMAL.  Approximation per CL_STD.
    info_total = 0.0
    for i in range(n_steps):
        if (ops[i], ops[i + 1]) in BUMP_PAIRS:
            info_total += INFO_BUMP
        elif ops[i + 1] == 7:
            info_total += INFO_HARMONY
        else:
            info_total += INFO_NORMAL
    return {
        "bump_hit_rate":      round(n_bumps / n_steps, 4),
        "info_bits_per_step": round(info_total / n_steps, 4),
        "gravity_mean":       round(grav_sum, 4),
        "total_info_bits":    round(info_total, 4),
    }


def score_path(ops: List[int],
               block: Optional[Dict[str, Dict[str, Any]]] = None
               ) -> Dict[str, Any]:
    """Score an operator path through the entire engine block.

    Returns:
      {
        path_length: int,
        ops: [...],
        filters: {
          filter_name: {role, in_scope_rate, harmony_hit_rate, ...}
        },
        cl_std_extras: {bump_hit_rate, info_bits, gravity_mean, ...},
        spectral_fingerprint: {filter_name: harmony_hit_rate} (compact),
      }
    """
    if block is None:
        block = build_block()
    ops = [int(o) % 10 for o in ops]
    out_filters: Dict[str, Any] = {}
    fingerprint: Dict[str, float] = {}
    for name, info in block.items():
        scores = _score_filter_path(info["matrix"], info["indices"], ops,
                                      info["role"])
        scores["role"] = info["role"]
        out_filters[name] = scores
        fingerprint[name] = scores["harmony_hit_rate"]

    return {
        "path_length": len(ops),
        "ops": ops,
        "filters": out_filters,
        "cl_std_extras": _score_cl_std_extras(ops),
        "spectral_fingerprint": fingerprint,
    }


def coherence_summary(ops: List[int],
                      block: Optional[Dict[str, Dict[str, Any]]] = None
                      ) -> Dict[str, Any]:
    """Compact summary: dominant filter (highest HARMONY hit), gauge
    coupling strength, attractor alignment, encoding info bits."""
    s = score_path(ops, block)
    fp = s["spectral_fingerprint"]
    if not fp:
        return {"empty": True}
    dominant = max(fp.items(), key=lambda kv: kv[1])
    base_h = fp.get("TSML_SYM", 0.0)
    bhml_h = fp.get("BHML", 0.0)
    ym_h   = fp.get("TSML_8_YM", 0.0)
    attr_h = fp.get("TSML_4_4core", 0.0)
    info   = s["cl_std_extras"]["total_info_bits"]
    return {
        "dominant_filter": dominant[0],
        "dominant_hit":    dominant[1],
        "base_synthesis":  base_h,
        "base_separation": bhml_h,
        "gauge_coupling":  ym_h,
        "attractor_align": attr_h,
        "info_bits":       info,
        "interpretation": (
            f"Strongest under {dominant[0]} ({dominant[1]:.2%}); "
            f"base synthesis {base_h:.2%}, separation {bhml_h:.2%}, "
            f"YM-gauge {ym_h:.2%}, 4-core attractor {attr_h:.2%}, "
            f"info {info:.1f} bits."
        ),
    }


# ─── Engine mount ─────────────────────────────────────────────────────

def mount_engine_block(engine: Any) -> bool:
    """Attach the engine block + register /engine/* endpoints.

    Endpoints:
      GET  /engine/block           filter inventory + roles
      POST /engine/score           body: {"ops": [int,...]} → spectral
      POST /engine/summary         body: {"ops": [int,...]} → compact
    """
    block = build_block()
    if not block:
        print("[CK Gen14] mount_engine_block: no canonical tables loaded")
        return False
    engine.engine_block = block
    engine.ck_score_path = lambda ops: score_path(ops, block)
    engine.ck_coherence = lambda ops: coherence_summary(ops, block)

    routes_registered: List[str] = []
    api = getattr(engine, "web_api", None)
    if api is not None:
        app = getattr(api, "_app", None) or getattr(api, "app", None)
        if app is not None:
            try:
                from flask import jsonify, request

                def _block_info():
                    out = {}
                    for name, info in block.items():
                        out[name] = {
                            "role":          info["role"],
                            "shape":         info["shape"],
                            "harmony_count": info["harmony_count"],
                            "indices":       list(info["indices"]),
                            "notes":         info["notes"],
                        }
                    return jsonify({
                        "n_filters": len(out),
                        "filters": out,
                        "roles": sorted({info["role"]
                                          for info in block.values()}),
                    })

                def _score():
                    data = request.get_json(force=True, silent=True) or {}
                    ops = data.get("ops", [])
                    return jsonify(score_path(ops, block))

                def _summary():
                    data = request.get_json(force=True, silent=True) or {}
                    ops = data.get("ops", [])
                    return jsonify(coherence_summary(ops, block))

                existing = set(r.rule for r in app.url_map.iter_rules())
                for rule, ep, fn, methods in (
                    ("/engine/block",   "engine_block_info", _block_info, ["GET"]),
                    ("/engine/score",   "engine_score",      _score,      ["POST"]),
                    ("/engine/summary", "engine_summary",    _summary,    ["POST"]),
                ):
                    if rule not in existing:
                        app.add_url_rule(rule, endpoint=ep, view_func=fn,
                                          methods=methods)
                        routes_registered.append(rule)
            except Exception as e:
                print(f"[CK Gen14] engine_block route registration failed: {e}")

    suffix = " (" + ", ".join(routes_registered) + ")" if routes_registered else ""
    print(f"[CK Gen14] engine_block: MOUNTED  {len(block)} filters across "
          f"{len({i['role'] for i in block.values()})} roles{suffix}")
    return True


# ─── CLI / smoke ──────────────────────────────────────────────────────

if __name__ == "__main__":
    block = build_block()
    print(f"engine block: {len(block)} filters")
    print()
    by_role: Dict[str, List[str]] = defaultdict(list)
    for name, info in block.items():
        by_role[info["role"]].append(name)
    for role, names in sorted(by_role.items()):
        print(f"  {role:11s}  {len(names)} filters: {', '.join(names[:4])}"
              + (f", ..." if len(names) > 4 else ""))
    print()

    # Score a synthetic path: a HARMONY-walk
    walk = [0, 7, 8, 7, 9, 7, 7, 0]
    print(f"scoring path {walk}:")
    s = score_path(walk, block)
    for name, scores in sorted(s["filters"].items()):
        print(f"  {name:18s}  H_hit={scores['harmony_hit_rate']:.2%}  "
              f"in_scope={scores['in_scope_rate']:.2%}  "
              f"role={scores['role']}")
    print()
    print(f"CL_STD extras: {s['cl_std_extras']}")
    print()
    print(f"summary: {coherence_summary(walk, block)['interpretation']}")
