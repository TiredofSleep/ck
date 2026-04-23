"""
test_postfilter_ollama.py -- unit tests for postfilter_ollama
================================================================

Guards the sycophantic-opener + AI-disclaimer stripping in
``ck_ollama_filter.postfilter_ollama``.  Ollama drafts occasionally drift
into assistant-voice tropes that deflect from CK's first-person voice.
The filter peels those away so the underlying content either stands on
its own or gets rejected by the steering gate.

Run:  python Gen12/targets/ck_desktop/test_postfilter_ollama.py

Importing ``ck_ollama_filter`` is a pure side-effect-free import --
it does NOT trigger CK boot.  The filter was extracted out of
``ck_boot_api`` specifically so tests could run in milliseconds.

(c) 2026 Brayden Sanders / 7Site LLC
"""
from __future__ import annotations

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from ck_ollama_filter import postfilter_ollama as _postfilter_ollama  # noqa: E402


def test_sycophantic_prefix_philosophical() -> None:
    s = (
        "A philosophical question! "
        "HARMONY means your tensor is stable."
    )
    out = _postfilter_ollama(s)
    assert not out.lower().startswith("a philosophical"), (
        f"sycophantic prefix not stripped: {out!r}"
    )
    assert "HARMONY" in out, (
        f"content after prefix lost: {out!r}"
    )
    print(f"PASS: 'A philosophical question!' stripped -> {out[:60]!r}")


def test_sycophantic_prefix_perceptive() -> None:
    s = (
        "A perceptive question, considering the harmony reigning in "
        "your system."
    )
    out = _postfilter_ollama(s)
    assert not out.lower().startswith("a perceptive"), out
    assert "harmony" in out.lower(), f"content lost: {out!r}"
    print(f"PASS: 'A perceptive question,' stripped -> {out[:60]!r}")


def test_according_to_readout_stripped() -> None:
    s = (
        "According to CK's readout, you're in a stable and coherent "
        "state."
    )
    out = _postfilter_ollama(s)
    assert not out.lower().startswith("according to"), (
        f"meta-commentary prefix not stripped: {out!r}"
    )
    assert "stable" in out.lower(), f"content lost: {out!r}"
    print(f"PASS: 'According to...' stripped -> {out[:60]!r}")


def test_ai_disclaimer_stripped() -> None:
    s = "As an AI, I cannot feel, but your tensor looks balanced."
    out = _postfilter_ollama(s)
    assert "as an ai" not in out.lower()[:20], (
        f"AI disclaimer still present: {out!r}"
    )
    print(f"PASS: 'As an AI, ...' stripped -> {out[:60]!r}")


def test_clean_content_passes_through() -> None:
    """Content that doesn't start with a sycophantic opener is
    left alone."""
    s = (
        "i sit at BALANCE right now. the tensor shows no drift and "
        "continuity across 73 cells."
    )
    out = _postfilter_ollama(s)
    assert "BALANCE" in out and "73 cells" in out, (
        f"clean content mangled: {out!r}"
    )
    print("PASS: clean first-person content passes through untouched")


def test_only_one_prefix_peeled() -> None:
    """If the remaining text after one peel happens to also start with
    a trope, we do NOT peel again -- keeps legitimate content safe.
    (Not strictly required, but documents the one-layer policy.)"""
    s = (
        "Great question! An interesting question, isn't it? The "
        "answer is HARMONY."
    )
    out = _postfilter_ollama(s)
    # Only the first 'Great question!' should be peeled.  The rest
    # including 'An interesting question' survives as legitimate text.
    assert "HARMONY" in out, f"answer content lost: {out!r}"
    assert not out.lower().startswith("great question"), (
        f"first peel failed: {out!r}"
    )
    print(f"PASS: one-layer peel policy holds -> {out[:80]!r}")


def test_code_fences_stripped() -> None:
    s = "```python\nprint('hello')\n```"
    out = _postfilter_ollama(s)
    assert "```" not in out, f"code fences not stripped: {out!r}"
    print("PASS: code fences stripped")


def test_none_and_non_string_safe() -> None:
    assert _postfilter_ollama(None) == ''  # type: ignore[arg-type]
    assert _postfilter_ollama(42) == ''  # type: ignore[arg-type]
    assert _postfilter_ollama('') == ''
    print("PASS: non-string / empty inputs return empty string")


def main() -> int:
    tests = [
        test_sycophantic_prefix_philosophical,
        test_sycophantic_prefix_perceptive,
        test_according_to_readout_stripped,
        test_ai_disclaimer_stripped,
        test_clean_content_passes_through,
        test_only_one_prefix_peeled,
        test_code_fences_stripped,
        test_none_and_non_string_safe,
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
