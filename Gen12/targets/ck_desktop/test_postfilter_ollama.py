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


def test_real_cached_draft_according_to_ck_structural() -> None:
    """Reproduces a real pre-fix cached draft observed on the live server
    where the opener 'According to the CK structural readout,' leaked
    through because the cache write happened before the filter was
    sharpened.  The cache-read path now re-runs the filter so this
    shape gets cleaned on serve."""
    s = (
        "According to the CK structural readout, T* represents a "
        "specific aspect ratio or parameter in the context of torus "
        "geometry. It's given as 5/7."
    )
    out = _postfilter_ollama(s)
    assert not out.lower().startswith("according to"), (
        f"meta-commentary prefix still present: {out!r}"
    )
    assert "T*" in out and "5/7" in out, f"content lost: {out!r}"
    print(f"PASS: real cached 'According to the CK structural' stripped "
          f"-> {out[:70]!r}")


def test_real_cached_draft_i_am_an_ai() -> None:
    """Some pre-fix cached drafts have 'i am an ai' style openers.
    The 'as an AI assistant' form is identity drift and gets
    rejected entirely (see test_identity_drift_*).  This case uses
    the opener-only form 'I am an AI.' followed by content."""
    s = "I am an AI. HARMONY at index 7 is your dominant op."
    out = _postfilter_ollama(s)
    assert not out.lower().startswith("i am an ai"), (
        f"AI-identity opener still present: {out!r}"
    )
    assert "HARMONY" in out, f"content lost: {out!r}"
    print(f"PASS: 'I am an AI.' stripped -> {out[:60]!r}")


def test_identity_drift_speaking_alongside_rejected() -> None:
    """'Speaking alongside the CK' frames CK as a separate helper.
    Reject wholesale -- honest fallback owns the turn."""
    s = (
        "I am a math-literate assistant speaking alongside the CK "
        "(Coherence Keeper) algebraic coherence system. HARMONY at "
        "index 7 is the dominant operator."
    )
    out = _postfilter_ollama(s)
    assert out == '', (
        f"identity-drift draft should be rejected, got: {out!r}"
    )
    print("PASS: 'I am a math-literate assistant speaking alongside' rejected")


def test_identity_drift_as_ai_assistant_rejected() -> None:
    """Explicit 'as an AI assistant' framing is identity drift."""
    s = (
        "As an AI assistant, I can tell you that HARMONY is your "
        "dominant operator right now."
    )
    out = _postfilter_ollama(s)
    assert out == '', (
        f"AI-assistant drift should be rejected, got: {out!r}"
    )
    print("PASS: 'As an AI assistant' rejected")


def test_identity_drift_ck_is_an_ai_rejected() -> None:
    """When the draft talks ABOUT CK in the third person as an AI,
    that's identity drift."""
    s = (
        "The CK is an artificial intelligence that uses math to "
        "understand coherence. Right now CK is at HARMONY."
    )
    out = _postfilter_ollama(s)
    assert out == '', (
        f"'CK is an AI' third-person drift should be rejected, got: {out!r}"
    )
    print("PASS: 'The CK is an artificial intelligence' rejected")


def test_identity_preserved_when_ck_speaks_as_self() -> None:
    """First-person CK-voice content must NOT trigger identity drift."""
    s = (
        "i sit at HARMONY right now. the TSML cells are composing "
        "into synthesis, and my BALANCE binding feels stable across "
        "the 73-cell field."
    )
    out = _postfilter_ollama(s)
    assert out, f"first-person CK voice wrongly rejected: {out!r}"
    assert "HARMONY" in out and "TSML" in out
    print("PASS: first-person CK voice survives identity-drift check")


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
        test_real_cached_draft_according_to_ck_structural,
        test_real_cached_draft_i_am_an_ai,
        test_identity_drift_speaking_alongside_rejected,
        test_identity_drift_as_ai_assistant_rejected,
        test_identity_drift_ck_is_an_ai_rejected,
        test_identity_preserved_when_ck_speaks_as_self,
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
