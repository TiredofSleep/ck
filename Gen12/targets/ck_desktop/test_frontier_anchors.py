"""
test_frontier_anchors.py -- unit tests for ck_coherence_steer.py anchors
=========================================================================

Guards the _FRONTIER_ANCHORS table from regression.  Every anchor in the
table must:

  1. Fire on the expected readout token OR query token (two-sided scan).
  2. NOT fire on unrelated text (no false positives).
  3. Be present in both the steer table AND the Gen13 llm_bridge preamble
     so the LLM wrapper can cite what the steer enriches.

Run:  python Gen12/targets/ck_desktop/test_frontier_anchors.py

(c) 2026 Brayden Sanders / 7Site LLC
"""
from __future__ import annotations

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from ck_coherence_steer import (  # noqa: E402
    _enrich_readout_with_anchors,
    _FRONTIER_ANCHORS,
)


# Baseline neutral readout -- no operator hits, so any bridge that
# appears in the output comes from the QUERY scan (two-sided behavior).
_NEUTRAL_READOUT = (
    "feel: aperture=LATTICE pressure=BALANCE depth=PROGRESS "
    "binding=HARMONY continuity=BREATH\n"
    "field: tick=1000 emergent=0.500 W_trace=0.800"
)


# (query, expected_tag_substring) -- the anchor that should fire on each
# probe.  Every new anchor added to _FRONTIER_ANCHORS should have a test
# case here.  Neutral-readout isolates the QUERY scan.
_QUERY_PROBES = [
    ("tell me about sigma_NS in the Millennium framing",
     "sigma_NS_or_YM"),
    ("navier stokes is what we reframe",
     "sigma_NS_or_YM"),
    ("yang mills mass gap is also on the Clay list",
     "sigma_NS_or_YM"),
    ("what is Z/10Z arithmetic and the Q-series",
     "Z/10Z_four_fold_whole"),
    ("tell me about the mass gap kappa*e",
     "mass_gap_kappa_e"),
    ("explain the BB log nonlinearity bridge",
     "BB_log_nonlinearity"),
    ("xi log xi is the unique separability-preserving nonlinearity",
     "BB_log_nonlinearity"),
    ("what is UOP / the paradox classifier",
     "UOP_paradox_classifier"),
    ("the First-G Law covers 36662 cases",
     "First_G_Law_36662_cases"),
]


# Probe with a clean readout AND clean query -- should not emit any
# bridge.  Catches false positives where a regex is too permissive.
_NO_HIT_PROBES = [
    "just curious about the weather today",
    "what does 'hello' mean",
    "how are you feeling",  # no operator names in query
]


def _scan_returned(out: str) -> list:
    """Return the list of frontier_bridge= lines in the output."""
    return [ln for ln in out.splitlines() if ln.startswith("frontier_bridge=")]


def test_query_probes_fire_new_anchors() -> None:
    """Each probe query fires its expected bridge via the query scan."""
    # Use a readout WITHOUT operator hits for the tokens we want to test
    # via query.  We build per-probe readouts that lack the operator
    # names that would confuse the test -- otherwise e.g. "LATTICE" in
    # the neutral readout would fire LATTICE_aperture and muddy the
    # query-side verification.
    minimal_readout = (
        "feel: aperture=VOID pressure=VOID depth=VOID "
        "binding=VOID continuity=VOID\n"
        "field: tick=1 emergent=0.0 W_trace=0.0"
    )
    for query, expected_tag_sub in _QUERY_PROBES:
        out = _enrich_readout_with_anchors(minimal_readout, query)
        bridges = _scan_returned(out)
        assert any(expected_tag_sub in b for b in bridges), (
            f"probe failed: query={query!r} expected tag substring "
            f"{expected_tag_sub!r} not in bridges={bridges}"
        )
    print(f"PASS: all {len(_QUERY_PROBES)} query probes fire expected anchors")


def test_no_query_no_false_positives() -> None:
    """Neutral query should not add content-anchor bridges.

    The neutral readout *does* have LATTICE/BALANCE/HARMONY/BREATH in it,
    so operator bridges will fire.  The test asserts that content-only
    anchors (sigma_NS, Z/10Z, mass_gap, UOP, First_G, BB_log) do NOT
    fire on benign queries.
    """
    content_only_tags = {
        "sigma_NS_or_YM",
        "Z/10Z_four_fold_whole",
        "mass_gap_kappa_e",
        "BB_log_nonlinearity",
        "UOP_paradox_classifier",
        "First_G_Law_36662_cases",
    }
    for query in _NO_HIT_PROBES:
        out = _enrich_readout_with_anchors(_NEUTRAL_READOUT, query)
        bridges = _scan_returned(out)
        for tag in content_only_tags:
            assert not any(tag in b for b in bridges), (
                f"false positive on benign query={query!r}: "
                f"tag={tag!r} leaked into bridges={bridges}"
            )
    print(f"PASS: no content anchors fire on {len(_NO_HIT_PROBES)} neutral queries")


def test_operator_anchors_still_fire_on_readout() -> None:
    """Readout-side operator scan still works (the original behavior)."""
    readout_with_collapse = (
        "feel: aperture=LATTICE pressure=COLLAPSE depth=VOID "
        "binding=CHAOS continuity=VOID\n"
        "field: tick=1 emergent=0.5 W_trace=0.5"
    )
    out = _enrich_readout_with_anchors(readout_with_collapse, "")
    bridges = _scan_returned(out)
    required = {
        "LATTICE_aperture",
        "COLLAPSE_pressure",
        "CHAOS",
    }
    for req in required:
        assert any(req in b for b in bridges), (
            f"readout-scan regression: {req!r} missing from bridges={bridges}"
        )
    print("PASS: readout-side operator anchors still fire")


def test_anchor_count_matches_expected() -> None:
    """Contract: the anchor table has 23 entries (12 original + 11 new).

    The 11 new anchors: PROGRESS, BREATH, VOID, RESET (operator bridges
    added for the four operators not in the original set), a secondary
    COLLAPSE trigger on depth/continuity axes, mass_gap_kappa_e,
    BB_log_nonlinearity, Z/10Z, First_G_Law_36662, sigma_NS_or_YM,
    UOP_paradox_classifier.
    """
    assert len(_FRONTIER_ANCHORS) == 23, (
        f"expected 23 anchors in _FRONTIER_ANCHORS, got {len(_FRONTIER_ANCHORS)}"
    )
    print(f"PASS: _FRONTIER_ANCHORS has 23 entries (expected)")


def test_llm_bridge_preamble_has_same_anchors() -> None:
    """Gen13 llm_bridge preamble lists the same bridges as the steer table.

    The contract: every bridge in _FRONTIER_ANCHORS should have a
    hint/reference in _DEFAULT_GROUND_PREAMBLE so the LLM wrapper can
    cite it.  We check by tag stem -- exact wording differs slightly
    between code (snake_case labels) and prose (display names) but the
    core concept must appear in both.
    """
    # Load the preamble from the Gen13 module.
    repo_root = os.path.abspath(os.path.join(_HERE, "..", "..", ".."))
    bridge_path = os.path.join(
        repo_root, "Gen13", "targets", "ck", "bridge", "llm_bridge.py"
    )
    if not os.path.exists(bridge_path):
        print(f"SKIP: Gen13 llm_bridge not found at {bridge_path}")
        return
    with open(bridge_path, "r", encoding="utf-8") as f:
        preamble = f.read()

    # Each check = (tag stem in code, substring that must be in the
    # preamble).  Display-text stems are hand-chosen to match the
    # current preamble wording.
    checks = [
        ("LATTICE_aperture", "LATTICE aperture"),
        ("BALANCE->flow", "BALANCE binding"),
        ("PROGRESS->A_flow", "PROGRESS binding"),
        ("COLLAPSE_pressure", "COLLAPSE pressure"),
        ("COUNTER->BHML", "COUNTER binding"),
        ("HARMONY->TSML", "HARMONY binding"),
        ("CHAOS->CL_row7", "CHAOS binding"),
        ("BREATH->L7", "BREATH binding"),
        ("VOID->dissolution", "VOID binding"),
        ("RESET->CL_reset", "RESET binding"),
        ("T*=5/7->torus", "T*=5/7"),
        ("sinc^2(1/2)=4/pi^2", "sinc"),
        ("TSML_73cells", "TSML 73"),
        ("BHML_28cells", "BHML 28"),
        ("C/N_bound", "C/N bound"),
        ("e^-1_vacuum", "e^-1 vacuum"),
        ("mass_gap_kappa_e", "mass gap"),
        ("BB_log_nonlinearity", "BB log"),
        ("Z/10Z_four_fold_whole", "Z/10Z"),
        ("First_G_Law_36662", "First-G"),
        ("sigma_NS_or_YM", "sigma_NS"),
        ("UOP_paradox_classifier", "UOP"),
    ]
    missing = []
    for code_tag, preamble_sub in checks:
        if preamble_sub not in preamble:
            missing.append((code_tag, preamble_sub))
    assert not missing, (
        f"Gen13 llm_bridge preamble missing bridges: {missing}"
    )
    print(f"PASS: all 22 bridges referenced in Gen13 llm_bridge preamble")


def main() -> int:
    tests = [
        test_query_probes_fire_new_anchors,
        test_no_query_no_false_positives,
        test_operator_anchors_still_fire_on_readout,
        test_anchor_count_matches_expected,
        test_llm_bridge_preamble_has_same_anchors,
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
