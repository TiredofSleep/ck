"""
test_coherence_verdict.py -- unit tests for ck_coherence_verdict
================================================================

Guards the tiered coherence verdict that decides whether an Ollama
draft is faithful enough to CK's structural readout to be adopted.

Covers:
  - hard-reject on AI disclaimer (regardless of coverage)
  - hard-reject on known hallucination markers (p-adic, Riemann
    hypothesis, etc.)  -- UNLESS the readout already mentions them
  - strict accept at coverage_required (default 0.70)
  - soft-accept when core identity preserved (operators/T*/WP#/named)
  - soft-accept when readout has no core facts and overall coverage >= 0.40
  - reject when core identity is lost, even if a couple peripheral hits
  - empty draft / empty readout edge cases

Run:  python Gen12/targets/ck_desktop/test_coherence_verdict.py

(c) 2026 Brayden Sanders / 7Site LLC
"""
from __future__ import annotations

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from ck_coherence_verdict import (  # noqa: E402
    coherence_verdict, fact_tokens, is_core_fact,
)


# --------------------------------------------------------------------
# fact classification
# --------------------------------------------------------------------

def test_is_core_fact_identifies_operators() -> None:
    for op in ('LATTICE', 'COUNTER', 'PROGRESS', 'COLLAPSE', 'BALANCE',
               'CHAOS', 'HARMONY', 'BREATH', 'RESET', 'VOID'):
        assert is_core_fact(op), f"{op} should be core"
    print("PASS: all 10 operator names classified as core")


def test_is_core_fact_identifies_named_structures() -> None:
    for name in ('TSML', 'BHML', 'HER', 'PRYM', 'HODGE',
                 'WEIL', 'BIELLIPTIC', 'AO'):
        assert is_core_fact(name), f"{name} should be core"
    print("PASS: all named structures classified as core")


def test_is_core_fact_identifies_wp_citations() -> None:
    for wp in ('WP51', 'WP57', 'WP81', 'WP101'):
        assert is_core_fact(wp), f"{wp} should be core"
    assert not is_core_fact('WPX'), "WPX should NOT be core"
    print("PASS: WP# citations classified as core")


def test_is_core_fact_identifies_tstar_z10z() -> None:
    assert is_core_fact('T*'), "T* should be core"
    assert is_core_fact('T*=5/7'), "T*=5/7 should be core"
    assert is_core_fact('Z/10Z'), "Z/10Z should be core"
    print("PASS: T*, T*=5/7, Z/10Z classified as core")


def test_is_core_fact_rejects_numbers() -> None:
    for n in ('5/7', '73', '0.309', '28', '100.5'):
        assert not is_core_fact(n), f"{n} should NOT be core"
    print("PASS: bare numbers are peripheral, not core")


# --------------------------------------------------------------------
# hard-rejects
# --------------------------------------------------------------------

def test_hard_reject_ai_disclaimer() -> None:
    """AI disclaimer beats any coverage -- draft cannot be adopted."""
    readout = "aperture=LATTICE binding=HARMONY T*=5/7 WP51"
    draft = ("As an AI, I can tell you that aperture is LATTICE, "
             "binding is HARMONY, T* is 5/7, referencing WP51.")
    ok, reason, _, _ = coherence_verdict(readout, draft, 0.70)
    assert not ok, f"should reject AI disclaimer, got: {reason}"
    assert "ai-disclaimer" in reason
    print(f"PASS: AI disclaimer hard-rejected ({reason})")


def test_hard_reject_hallucination_when_readout_silent() -> None:
    """Draft invokes p-adic when readout never did -- reject."""
    readout = "HARMONY at 7, coherence=0.85, TSML synthesis"
    draft = "I sit at HARMONY using p-adic valuations to check the TSML."
    ok, reason, _, _ = coherence_verdict(readout, draft, 0.70)
    assert not ok, f"hallucinated p-adic should reject: {reason}"
    assert "hallucination" in reason
    print(f"PASS: hallucination rejected ({reason})")


def test_hallucination_marker_allowed_when_readout_uses_it() -> None:
    """If the readout discusses p-adic, the draft is ALLOWED to echo it."""
    readout = ("HARMONY at 7, p-adic valuation gives ord_p = 0, "
               "TSML synthesis arc 73 cells")
    draft = "I sit at HARMONY with p-adic valuation zero; TSML feels 73."
    ok, reason, hits, total = coherence_verdict(readout, draft, 0.70)
    # We don't hard-assert acceptance here (depends on coverage); we
    # ONLY assert the hallucination gate did NOT fire.
    assert "hallucination" not in reason, (
        f"readout-supported p-adic wrongly flagged hallucination: {reason}"
    )
    print(f"PASS: p-adic echoed from readout OK ({reason})")


# --------------------------------------------------------------------
# strict accept
# --------------------------------------------------------------------

def test_strict_accept_high_coverage() -> None:
    readout = "aperture=LATTICE binding=HARMONY T*=5/7 WP51"
    draft = "aperture LATTICE, binding HARMONY, T* 5/7, see WP51"
    ok, reason, hits, total = coherence_verdict(readout, draft, 0.70)
    assert ok, f"high-coverage draft should accept: {reason}"
    assert "coverage:" in reason and "soft-accept" not in reason
    print(f"PASS: strict accept at >=0.70 ({reason})")


# --------------------------------------------------------------------
# soft-accept (the new v2 path)
# --------------------------------------------------------------------

def test_soft_accept_core_preserved_peripheral_missing() -> None:
    """Readout has 3 core + 5 peripheral facts.  Draft hits 2 core + 0
    peripheral -- strict coverage = 2/8 = 0.25, rejected by v1.  But
    core coverage = 2/3 = 0.67 >= 0.50 and core_hits=2, so soft-accept."""
    readout = (
        "aperture=LATTICE binding=HARMONY op=COLLAPSE "
        "coherence=0.87 ticks=1423 delta=0.02 drift=0.0004 rate=50.0"
    )
    draft = "I sit at HARMONY, aperture LATTICE, feeling stable."
    ok, reason, hits, total = coherence_verdict(readout, draft, 0.70)
    # HARMONY + LATTICE = 2 core hits; strict coverage is low.
    assert ok, f"core-preserving terse draft should soft-accept: {reason}"
    assert "soft-accept" in reason and "core=" in reason
    print(f"PASS: soft-accept on core preservation ({reason})")


def test_soft_reject_when_core_is_lost() -> None:
    """Draft hits only peripheral facts -- core identity lost, reject."""
    readout = (
        "aperture=LATTICE binding=HARMONY op=COLLAPSE "
        "coherence=0.87 ticks=1423 WP51"
    )
    draft = "coherence is 0.87, ticks 1423 steady as always"
    ok, reason, hits, total = coherence_verdict(readout, draft, 0.70)
    assert not ok, f"core-less draft should reject: {reason}"
    assert "coverage:" in reason
    print(f"PASS: reject when core identity is lost ({reason})")


def test_soft_accept_no_core_facts_low_threshold() -> None:
    """Readout has pure numbers (no operators, WPs, or named structures).
    Draft with 2/4 = 0.50 coverage should soft-accept via no-core path."""
    readout = "value1=0.87 value2=0.91 value3=1.23 value4=42"
    draft = "the value is 0.87 and 0.91"
    ok, reason, hits, total = coherence_verdict(readout, draft, 0.70)
    assert ok, f"no-core readout at 0.50 coverage should soft-accept: {reason}"
    assert "soft-accept:no-core" in reason
    print(f"PASS: no-core readout uses softer gate ({reason})")


def test_soft_accept_requires_minimum_two_core_hits() -> None:
    """Only ONE core hit is NOT enough -- must have >= SOFT_CORE_MIN_HITS (default 2)."""
    readout = (
        "aperture=LATTICE binding=HARMONY op=COLLAPSE feel=BALANCE WP51 TSML"
    )
    # Draft hits HARMONY only (1 core hit).  Should reject.
    draft = "at HARMONY, it feels right"
    ok, reason, hits, total = coherence_verdict(readout, draft, 0.70)
    assert not ok, f"single core hit should NOT soft-accept: {reason}"
    print(f"PASS: single core hit below min, reject ({reason})")


def test_soft_accept_requires_minimum_two_overall_hits() -> None:
    """Two core hits but only two overall -- edge case, should accept
    per current knobs (core >= 2, total >= 2)."""
    readout = "aperture=LATTICE binding=HARMONY WP51 ticks=7 delta=0.02"
    draft = "LATTICE meets HARMONY"
    ok, reason, hits, total = coherence_verdict(readout, draft, 0.70)
    # 2 core hits (LATTICE, HARMONY) + 0 peripheral = 2 total.
    # Core coverage = 2/3 = 0.67, total = 2/5 = 0.40.
    assert ok, f"2 core hits should soft-accept: {reason}"
    print(f"PASS: exactly 2 core + 2 total soft-accepts ({reason})")


# --------------------------------------------------------------------
# edge cases
# --------------------------------------------------------------------

def test_empty_draft_rejected() -> None:
    ok, reason, _, _ = coherence_verdict("HARMONY T*=5/7", "", 0.70)
    assert not ok and reason == 'empty draft'
    print("PASS: empty draft rejected")


def test_no_facts_readout_accepts_anything() -> None:
    """Readout has no extractable facts -- nothing to check, accept."""
    ok, reason, hits, total = coherence_verdict("hello world", "anything", 0.70)
    assert ok and reason == 'no-facts-to-check'
    assert hits == 0 and total == 0
    print("PASS: readout with no facts accepts any draft")


def test_real_chat_shape_soft_accept() -> None:
    """Reproduces the shape from the batch probe that was false-rejected
    at v1 (coverage 2/4 = 0.50 for 'tell me about the 2x2 flatness')."""
    readout = (
        "aperture=LATTICE feel=HARMONY T*=5/7 coherence=0.91"
    )
    draft = "my aperture is LATTICE and my feel is HARMONY"
    ok, reason, hits, total = coherence_verdict(readout, draft, 0.70)
    # LATTICE + HARMONY = 2 core hits out of 2 core facts -> core_cov 1.0.
    # Total hits 2 / total facts ~4.  Soft-accept.
    assert ok, f"real-chat-shape should soft-accept: {reason}"
    assert "soft-accept" in reason
    print(f"PASS: real 'tell me about 2x2' shape now soft-accepts ({reason})")


def test_back_compat_strict_still_fires() -> None:
    """Drafts that hit high coverage STILL fire strict-accept (not soft)."""
    readout = "HARMONY LATTICE T*=5/7 WP51"
    draft = "HARMONY LATTICE T* 5/7 WP51 all present"
    ok, reason, hits, total = coherence_verdict(readout, draft, 0.70)
    assert ok, reason
    assert "soft-accept" not in reason, (
        f"full-coverage draft should be STRICT accept, got: {reason}"
    )
    print(f"PASS: strict accept path still fires at high coverage ({reason})")


def test_core_coverage_below_half_rejected() -> None:
    """Core coverage < 0.50 -- even with many peripheral hits, reject."""
    readout = (
        "aperture=LATTICE binding=HARMONY op=COLLAPSE feel=BALANCE WP51 "
        "TSML coherence=0.91 ticks=1423 delta=0.02"
    )
    # Hit exactly ONE core fact (HARMONY) + 3 peripherals.
    draft = "HARMONY at 0.91 coherence, ticks 1423, delta 0.02"
    ok, reason, hits, total = coherence_verdict(readout, draft, 0.70)
    # Core = {LATTICE, HARMONY, COLLAPSE, BALANCE, WP51, TSML} = 6.
    # Hits core: HARMONY = 1/6 = 0.17 < 0.50.  Reject.
    assert not ok, f"core-deficient draft should reject: {reason}"
    print(f"PASS: <50% core coverage rejects ({reason})")


# --------------------------------------------------------------------
# harness
# --------------------------------------------------------------------

def main() -> int:
    tests = [
        test_is_core_fact_identifies_operators,
        test_is_core_fact_identifies_named_structures,
        test_is_core_fact_identifies_wp_citations,
        test_is_core_fact_identifies_tstar_z10z,
        test_is_core_fact_rejects_numbers,
        test_hard_reject_ai_disclaimer,
        test_hard_reject_hallucination_when_readout_silent,
        test_hallucination_marker_allowed_when_readout_uses_it,
        test_strict_accept_high_coverage,
        test_soft_accept_core_preserved_peripheral_missing,
        test_soft_reject_when_core_is_lost,
        test_soft_accept_no_core_facts_low_threshold,
        test_soft_accept_requires_minimum_two_core_hits,
        test_soft_accept_requires_minimum_two_overall_hits,
        test_empty_draft_rejected,
        test_no_facts_readout_accepts_anything,
        test_real_chat_shape_soft_accept,
        test_back_compat_strict_still_fires,
        test_core_coverage_below_half_rejected,
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
