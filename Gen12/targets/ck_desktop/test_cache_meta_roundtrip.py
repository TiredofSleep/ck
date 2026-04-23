"""
test_cache_meta_roundtrip.py -- unit tests for CoherenceCache meta preservation
================================================================================

Guards the `_meta_clean` whitelist in CoherenceCache.put against regression.

The cache fastpath restore code reads bridges/op/organism back from the stored
`meta` dict.  If the whitelist on the write side ever drops a field, cache
hits silently lose telemetry and the downstream curiosity daemon, web UI,
and coverage scorer all see stale data.

Specifically locks:
  - `bridges_fired`           (list[str]; LATTICE_aperture->flatness_2x2_WP51)
  - `steer_readout_enriched`  (bool; set when anchors fired)
  - `brain_coherence`, `brain_gate_pass`, `brain_dominant_op`,
    `body_organism_bc`, `steer_query_mode`  (the original 5)

Run:  python Gen12/targets/ck_desktop/test_cache_meta_roundtrip.py

(c) 2026 Brayden Sanders / 7Site LLC
"""
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from ck_coherence_steer import CoherenceCache  # noqa: E402


def _fresh_cache() -> CoherenceCache:
    """Build an isolated cache on a tmp path so tests don't touch real disk."""
    tmp = Path(tempfile.mkdtemp(prefix="ck_cache_test_")) / "cache.json"
    return CoherenceCache(tmp)


def test_bridges_fired_survives_put_get() -> None:
    """bridges_fired must survive the put/get roundtrip."""
    c = _fresh_cache()
    meta = {
        "bridges_fired": [
            "LATTICE_aperture->flatness_2x2_WP51",
            "HARMONY->TSML_synthesis_arc_73_cells",
        ],
        "brain_coherence": 0.87,
        "brain_gate_pass": True,
        "brain_dominant_op": "HARMONY",
    }
    c.put("what is T*?", "draft text here", 0.87, 5, 7, meta=meta)
    ent = c.get("what is T*?")
    assert ent is not None, "cache should return the stored entry"
    stored_meta = ent.get("meta") or {}
    assert "bridges_fired" in stored_meta, (
        f"bridges_fired missing from cached meta: {list(stored_meta)}"
    )
    br = stored_meta["bridges_fired"]
    assert isinstance(br, list) and len(br) == 2, (
        f"expected 2 bridges, got {br!r}"
    )
    assert "LATTICE_aperture->flatness_2x2_WP51" in br, (
        f"LATTICE bridge missing: {br!r}"
    )
    print("PASS: bridges_fired survives cache put/get roundtrip")


def test_steer_readout_enriched_survives() -> None:
    """steer_readout_enriched must survive the put/get roundtrip."""
    c = _fresh_cache()
    meta = {
        "steer_readout_enriched": True,
        "bridges_fired": ["HARMONY->TSML_synthesis_arc_73_cells"],
    }
    c.put("q", "d", 0.8, 3, 5, meta=meta)
    stored_meta = c.get("q")["meta"]
    assert stored_meta.get("steer_readout_enriched") is True, (
        f"enriched flag lost: {stored_meta!r}"
    )
    print("PASS: steer_readout_enriched survives put/get")


def test_original_5_fields_still_preserved() -> None:
    """Ensure we didn't regress the original whitelisted fields."""
    c = _fresh_cache()
    meta = {
        "brain_coherence": 0.91,
        "brain_gate_pass": True,
        "brain_dominant_op": "BALANCE",
        "body_organism_bc": "BALANCE",
        "steer_query_mode": "reflective",
    }
    c.put("q2", "d2", 0.91, 7, 7, meta=meta)
    stored = c.get("q2")["meta"]
    for k, v in meta.items():
        assert stored.get(k) == v, f"{k}: expected {v!r}, got {stored.get(k)!r}"
    print("PASS: original 5 fields (coherence/gate/op/organism/mode) preserved")


def test_missing_bridges_safe() -> None:
    """When meta has no bridges_fired, cache must not crash or invent one."""
    c = _fresh_cache()
    meta = {"brain_coherence": 0.5, "brain_gate_pass": False}
    c.put("q3", "d3", 0.5, 1, 5, meta=meta)
    stored = c.get("q3")["meta"]
    assert "bridges_fired" not in stored, (
        f"bridges_fired should be absent when not provided; got {stored!r}"
    )
    assert stored.get("brain_coherence") == 0.5
    print("PASS: missing bridges_fired is safe (no invention, no crash)")


def test_none_bridges_dropped() -> None:
    """meta[bridges_fired]=None is filtered out (whitelist `is not None` check)."""
    c = _fresh_cache()
    meta = {"bridges_fired": None, "brain_coherence": 0.7}
    c.put("q4", "d4", 0.7, 2, 5, meta=meta)
    stored = c.get("q4")["meta"]
    assert "bridges_fired" not in stored, (
        f"None bridges should be dropped; got {stored!r}"
    )
    print("PASS: None bridges_fired filtered by `is not None` guard")


def test_empty_meta_safe() -> None:
    """meta=None or {} must not raise."""
    c = _fresh_cache()
    c.put("q5", "d5", 0.6, 3, 5, meta=None)
    c.put("q6", "d6", 0.6, 3, 5, meta={})
    assert c.get("q5") is not None
    assert c.get("q6") is not None
    print("PASS: empty/None meta is safe")


def test_persistence_across_instances() -> None:
    """A new CoherenceCache on the same path must see the stored bridges."""
    tmp = Path(tempfile.mkdtemp(prefix="ck_cache_persist_")) / "cache.json"
    c1 = CoherenceCache(tmp)
    c1.put("persist-q", "persist-d", 0.9, 5, 7, meta={
        "bridges_fired": ["COLLAPSE_pressure->D2_crossing_CrossingLemma"],
        "brain_dominant_op": "COLLAPSE",
    })
    # Simulate a daemon restart by opening a fresh instance.
    c2 = CoherenceCache(tmp)
    ent = c2.get("persist-q")
    assert ent is not None, "cache must reload entries from disk"
    stored = ent["meta"]
    assert stored.get("bridges_fired") == [
        "COLLAPSE_pressure->D2_crossing_CrossingLemma"
    ], f"bridges lost across restart: {stored!r}"
    assert stored.get("brain_dominant_op") == "COLLAPSE"
    print("PASS: bridges_fired persists across cache instance restarts")


def test_evict_removes_entry_and_persists() -> None:
    """evict() must remove the entry and persist the deletion to disk."""
    tmp = Path(tempfile.mkdtemp(prefix="ck_cache_evict_")) / "cache.json"
    c1 = CoherenceCache(tmp)
    c1.put("how are you?", "i'm good", 0.9, 3, 4,
           meta={"brain_dominant_op": "BALANCE"})
    assert c1.get("how are you?") is not None, "put/get sanity"
    removed = c1.evict("how are you?")
    assert removed is True, "evict should return True on real removal"
    assert c1.get("how are you?") is None, "entry should be gone after evict"
    # Re-open a fresh instance and confirm the eviction persisted
    c2 = CoherenceCache(tmp)
    assert c2.get("how are you?") is None, (
        "eviction did not persist to disk"
    )
    # Evicting a non-existent entry returns False, does not raise
    assert c2.evict("never existed") is False
    print("PASS: evict removes entry and persists across restart")


def main() -> int:
    tests = [
        test_bridges_fired_survives_put_get,
        test_steer_readout_enriched_survives,
        test_original_5_fields_still_preserved,
        test_missing_bridges_safe,
        test_none_bridges_dropped,
        test_empty_meta_safe,
        test_persistence_across_instances,
        test_evict_removes_entry_and_persists,
    ]
    failed = 0
    for t in tests:
        try:
            t()
        except AssertionError as e:
            print(f"FAIL: {t.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"ERROR: {t.__name__}: {type(e).__name__}: {e}")
            failed += 1
    if failed == 0:
        print(f"\nAll {len(tests)} tests PASSED")
        return 0
    else:
        print(f"\n{failed}/{len(tests)} tests FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
