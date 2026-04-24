# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0 (DOI: 10.5281/zenodo.18852047)
"""
cortex_catalog.py -- YAML-backed classification catalogs for CK.

Phase 2 of the meta-level rebuild (2026-04-24).

The problem it solves:
  cortex_voice._FRONTIER_FACTS is a hardcoded Python tuple.  Adding new
  structural facts, paradox classifications, or DoF-kind exemplars
  required editing Python and restarting the server.  That is not "learn
  and remember persistently and grow with us."

The fix:
  Three YAML files under Gen13/targets/ck/brain/catalog/ carry the
  classifications in machine-readable form.  This module loads them at
  first call and exposes:
    - hits(query)          -> List[str] of compact facts for speak()
    - classify_paradox(x)  -> dict, for /paradox/classify endpoint
    - dof_taxonomy()       -> dict, for /dof/taxonomy endpoint
    - constants_table()    -> List[dict], for /meta/constants endpoint
    - reload()             -> rereads YAML from disk (dev convenience)

The runtime conserves the existing _frontier_hits contract: facts are
one-line label=value readouts, one fact per match, de-duped by value.

PyYAML is an already-available runtime dependency (confirmed 2026-04-24;
PyYAML 6.0.3).  If it isn't importable the catalog disables itself and
CK falls back to the hardcoded _FRONTIER_FACTS -- no crash.
"""

from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

try:
    import yaml  # type: ignore
    _YAML_OK = True
except ImportError:
    _YAML_OK = False


# Directory layout
_HERE = os.path.dirname(os.path.abspath(__file__))
_CATALOG_DIR = os.path.join(_HERE, "catalog")

_FILES = {
    "dof": "dof_kinds.yaml",
    "paradoxes": "paradoxes.yaml",
    "constants": "cross_kind_constants.yaml",
    "frontier": "frontier_facts.yaml",
}


# Module-level cache
_LOADED: Dict[str, Any] = {}
_LOAD_ERRORS: List[str] = []


def load_catalog(force: bool = False) -> Dict[str, Any]:
    """Load the three YAML catalogs.  Idempotent; call `reload()` to re-read."""
    global _LOADED, _LOAD_ERRORS
    if _LOADED and not force:
        return _LOADED
    if not _YAML_OK:
        _LOAD_ERRORS.append("pyyaml not importable; catalogs disabled")
        _LOADED = {"dof": None, "paradoxes": None, "constants": None}
        return _LOADED
    out: Dict[str, Any] = {}
    for key, fname in _FILES.items():
        path = os.path.join(_CATALOG_DIR, fname)
        if not os.path.isfile(path):
            _LOAD_ERRORS.append(f"catalog file missing: {path}")
            out[key] = None
            continue
        try:
            with open(path, "r", encoding="utf-8") as fh:
                out[key] = yaml.safe_load(fh)
        except Exception as exc:  # pragma: no cover - I/O is defensive
            _LOAD_ERRORS.append(f"yaml load failed for {fname}: {exc}")
            out[key] = None
    _LOADED = out
    return _LOADED


def reload() -> Dict[str, Any]:
    """Force a re-read from disk (Phase 3 will expose this via endpoint)."""
    _LOAD_ERRORS.clear()
    return load_catalog(force=True)


def load_errors() -> List[str]:
    """Return any errors encountered during the last load (for /health)."""
    return list(_LOAD_ERRORS)


# ── Hit search ─────────────────────────────────────────────────────────
#
# Mirrors cortex_voice._frontier_hits.  Given a lowercased query, walk
# every catalog's `triggers` fields and return the matched `fact`.  Each
# fact fires at most once.

def hits(query: str) -> List[str]:
    """Return catalog facts whose triggers appear in `query` (lowercased)."""
    cat = load_catalog()
    q = (query or "").lower()
    facts: List[str] = []
    seen = set()

    def _emit(entry: dict) -> None:
        fact = (entry.get("fact") or "").strip()
        if not fact or fact in seen:
            return
        triggers = entry.get("triggers") or []
        for trig in triggers:
            if trig and trig.lower() in q:
                facts.append(fact)
                seen.add(fact)
                return

    dof = (cat.get("dof") or {}).get("kinds") or []
    for kind in dof:
        _emit(kind)

    paradoxes = (cat.get("paradoxes") or {}).get("paradoxes") or []
    for p in paradoxes:
        _emit(p)

    constants = (cat.get("constants") or {}).get("constants") or []
    for c in constants:
        _emit(c)

    frontier = (cat.get("frontier") or {}).get("facts") or []
    for f in frontier:
        _emit(f)

    return facts


# ── Public classifiers ────────────────────────────────────────────────

# Mirrors classify_paradox.STAGE_TO_TYPE so the endpoint can honor both
# paradox-slug lookup AND a stage-keyed JSON instance.
_STAGE_TO_TYPE = {
    "joint_map":     ("I",   "add observable / refine symbolic powers / coordinate extension"),
    "invariant":     ("II",  "accept gap / relativize / change category / climb ordinal tower"),
    "admissibility": ("III", "narrow admissible class / change logic / ascend type hierarchy"),
    "dynamics":      ("IV",  "single-valued dynamics via decoherence / MWI / GRW / Bohm / QBism"),
}
_TYPE_LONG = {
    "I":   "Injectivity Failure",
    "II":  "Missing Invariant",
    "III": "Admissibility Failure",
    "IV":  "Time-Consistency Failure",
}


def classify_paradox(slug_or_stage: Optional[str] = None,
                     failure_stage: Optional[str] = None,
                     name: Optional[str] = None) -> dict:
    """Return a UOP classification verdict.

    Two modes:
      (a) slug_or_stage matches a known paradox slug in paradoxes.yaml
          -> return the stored verdict (Type, fix_family, DoF kinds, template).
      (b) failure_stage is one of the four stages -> return the forced Type.

    Raises KeyError if neither mode resolves.
    """
    cat = load_catalog()
    paradoxes = (cat.get("paradoxes") or {}).get("paradoxes") or []

    # Mode (a): slug lookup
    if slug_or_stage:
        key = slug_or_stage.lower().strip().replace(" ", "_")
        for entry in paradoxes:
            if (entry.get("slug") or "").lower() == key:
                code = entry.get("type")
                fix = next(
                    (fx for (ty, fx) in _STAGE_TO_TYPE.values() if ty == code),
                    "",
                )
                return {
                    "source": "catalog",
                    "paradox": entry.get("name") or key,
                    "slug": entry.get("slug"),
                    "type": code,
                    "type_long": _TYPE_LONG.get(code or "", "unknown"),
                    "fix_family": fix,
                    "dof_kinds": entry.get("dof_kinds") or [],
                    "conditional": bool(entry.get("conditional", False)),
                    "primary_lens": entry.get("primary_lens"),
                    "template_file": entry.get("template_file"),
                    "fact": entry.get("fact"),
                    "cite": entry.get("cite"),
                }

    # Mode (b): stage forces type
    stage = (failure_stage or slug_or_stage or "").lower().strip()
    if stage in _STAGE_TO_TYPE:
        code, fix = _STAGE_TO_TYPE[stage]
        return {
            "source": "stage",
            "paradox": name or "<unnamed>",
            "type": code,
            "type_long": _TYPE_LONG[code],
            "fix_family": fix,
            "slot3_failure_stage": stage,
        }

    raise KeyError(
        f"classify_paradox: {slug_or_stage!r} is neither a known slug nor a "
        f"valid failure stage. Known slugs: "
        f"{[p.get('slug') for p in paradoxes]}; "
        f"known stages: {sorted(_STAGE_TO_TYPE)}"
    )


def dof_taxonomy() -> dict:
    """Return the five DoF Kinds, diagnostic questions, and exemplars."""
    cat = load_catalog()
    dof = cat.get("dof") or {}
    return {
        "axis": dof.get("axis", "DoF Kinds"),
        "canonical_home": dof.get("canonical_home"),
        "count": dof.get("count"),
        "exhaustive_over": dof.get("exhaustive_over"),
        "kinds": dof.get("kinds") or [],
        "cross_kind_constants": dof.get("cross_kind_constants") or [],
        "multi_kind_examples": dof.get("multi_kind_examples") or [],
    }


def constants_table() -> List[dict]:
    """Return the cross-kind constants registry."""
    cat = load_catalog()
    return (cat.get("constants") or {}).get("constants") or []


def paradox_registry() -> List[dict]:
    """Return the full paradox registry (for /meta/registry)."""
    cat = load_catalog()
    return (cat.get("paradoxes") or {}).get("paradoxes") or []


def frontier_facts() -> List[dict]:
    """Return the frontier-fact registry (replaces _FRONTIER_FACTS)."""
    cat = load_catalog()
    return (cat.get("frontier") or {}).get("facts") or []


def summary() -> dict:
    """Quick introspection: counts and load status."""
    cat = load_catalog()
    return {
        "yaml_available": _YAML_OK,
        "errors": list(_LOAD_ERRORS),
        "dof_kind_count": len((cat.get("dof") or {}).get("kinds") or []),
        "paradox_count": len((cat.get("paradoxes") or {}).get("paradoxes") or []),
        "constant_count": len((cat.get("constants") or {}).get("constants") or []),
        "frontier_count": len((cat.get("frontier") or {}).get("facts") or []),
    }


# ── Self-test ──────────────────────────────────────────────────────────

def _smoke() -> None:
    """Confirm load + hit + classify on known values."""
    s = summary()
    assert s["yaml_available"], "pyyaml missing (install: pip install pyyaml)"
    assert s["errors"] == [], f"catalog load errors: {s['errors']}"
    assert s["dof_kind_count"] == 5, f"expected 5 DoF kinds, got {s['dof_kind_count']}"
    assert s["paradox_count"] >= 10, f"expected >=10 paradoxes, got {s['paradox_count']}"
    assert s["constant_count"] >= 5, f"expected >=5 constants, got {s['constant_count']}"
    assert s["frontier_count"] >= 12, f"expected >=12 frontier facts, got {s['frontier_count']}"

    # Trigger-to-fact
    hh = hits("what is T*?")
    assert any("T* = 5/7" in h for h in hh), f"T* trigger failed: {hh}"

    hh2 = hits("tell me about godel")
    assert any("godel" in h.lower() for h in hh2), f"godel trigger failed: {hh2}"

    hh3 = hits("what kind is a reversible flow")
    assert any("K2" in h for h in hh3), f"K2 trigger failed: {hh3}"

    # Slug lookup
    v = classify_paradox("godel")
    assert v["type"] == "II", f"godel slug lookup failed: {v}"

    # Stage lookup
    v2 = classify_paradox(failure_stage="dynamics", name="cat")
    assert v2["type"] == "IV", f"stage lookup failed: {v2}"

    # DoF taxonomy
    tax = dof_taxonomy()
    assert tax["count"] == 5
    ids = [k["id"] for k in tax["kinds"]]
    assert ids == ["K1", "K2", "K3", "K4", "K5"], f"kind order wrong: {ids}"

    print("cortex_catalog self-test OK:", s)


if __name__ == "__main__":
    _smoke()
