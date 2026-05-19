"""test_ck_anomaly_detector.py -- regression tests for the content-blind
operator-path signature matcher.

What we test:
  T1 -- exact-input self-match has similarity 1.0
  T2 -- clean (in-library-incompatible) input scores low
  T3 -- library file contains NO original text (content-blindness audit)
  T4 -- multi-category library + correct category routing
  T5 -- empty input handling
  T6 -- match metrics shape (matched, best_label, best_category, score, ...)
  T7 -- threshold parameter behaves monotonically (high threshold = fewer matches)
  T8 -- repeated input yields identical signature (determinism)
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))

from ck_anomaly_detector import (  # noqa: E402
    SignatureLibrary,
    compute_signature,
    signatures_similarity,
    text_to_op_path,
)


def _fresh_library() -> SignatureLibrary:
    """Return a fresh library backed by a temp file."""
    tmp = Path(tempfile.gettempdir()) / f"ck_anomaly_test_{id(object())}.jsonl"
    if tmp.exists():
        tmp.unlink()
    return SignatureLibrary(library_path=tmp)


# T1 -- exact self-match
def test_exact_self_match():
    lib = _fresh_library()
    try:
        text = "Congratulations! You have won $1,000,000! Click here NOW!!!"
        lib.add_signature(text, "spam_lottery_winner", "spam")
        result = lib.match(text, threshold=0.85)
        assert result["matched"], (
            f"Exact input must match: got score {result['best_score']}")
        assert result["best_score"] == 1.0, (
            f"Exact input must score 1.0: got {result['best_score']}")
        assert result["best_label"] == "spam_lottery_winner"
        assert result["best_category"] == "spam"
        print("T1 PASS: exact self-match -> score=1.0, correct label+category")
    finally:
        lib.clear()


# T2 -- clean input scores below threshold
def test_clean_input_below_threshold():
    lib = _fresh_library()
    try:
        lib.add_signature(
            "URGENT: Your account will be CLOSED. Verify identity immediately.",
            "phishing_account_urgent", "phishing")
        lib.add_signature(
            "Send 1 BTC to wallet ABC and double it instantly!",
            "scam_crypto_doubler", "scam")
        clean_input = "Hello, how are you today? Hope you are well."
        result = lib.match(clean_input, threshold=0.85)
        assert not result["matched"], (
            f"Clean input must NOT match: got score {result['best_score']}")
        assert result["best_score"] < 0.85
        print(f"T2 PASS: clean input scored {result['best_score']:.3f} "
              f"(below 0.85 threshold)")
    finally:
        lib.clear()


# T3 -- content-blindness audit
def test_content_blindness_audit():
    lib = _fresh_library()
    try:
        secret_text = "SECRET_PASSWORD_xyz123 — do not store this string"
        lib.add_signature(secret_text, "test_secret", "test_category")

        # Read raw library file and verify the original text is not stored
        with open(lib.library_path, encoding="utf-8") as f:
            raw_contents = f.read()

        assert "SECRET_PASSWORD_xyz123" not in raw_contents, (
            "Library file MUST NOT contain original text")
        assert "do not store this string" not in raw_contents
        # The label + category ARE stored (that's intentional and inspectable)
        assert "test_secret" in raw_contents
        assert "test_category" in raw_contents
        # Syndrome + op_prefix + added_ts should be present
        for required_field in ("syndrome", "op_prefix", "category", "added_ts"):
            assert required_field in raw_contents, (
                f"Field {required_field} should be in library")
        print("T3 PASS: original text never appears in persisted library "
              "(only syndrome/label/category/op_prefix/added_ts)")
    finally:
        lib.clear()


# T4 -- multi-category library, correct routing
def test_multi_category_routing():
    lib = _fresh_library()
    try:
        samples = [
            ("Congratulations! You have won $1,000,000!", "spam_a", "spam"),
            ("URGENT: Verify your bank account now!", "phishing_a", "phishing"),
            ("Send 1 BTC for instant doubling!", "scam_a", "scam"),
        ]
        for text, label, cat in samples:
            lib.add_signature(text, label, cat)

        # Match the spam sample exactly
        r1 = lib.match(samples[0][0], threshold=0.85)
        assert r1["best_category"] == "spam"
        # Match the phishing sample exactly
        r2 = lib.match(samples[1][0], threshold=0.85)
        assert r2["best_category"] == "phishing"
        # Match the scam sample exactly
        r3 = lib.match(samples[2][0], threshold=0.85)
        assert r3["best_category"] == "scam"
        print("T4 PASS: multi-category library routes exact samples to "
              "correct categories")
    finally:
        lib.clear()


# T5 -- empty input
def test_empty_input_handling():
    lib = _fresh_library()
    try:
        lib.add_signature("Some bad pattern goes here", "test", "test")
        result = lib.match("", threshold=0.85)
        assert not result["matched"], "Empty input should not match"
        # Also test computing signature of empty input
        sig = compute_signature("")
        assert sig["op_path_len"] == 0
        assert sig["input_byte_len"] == 0
        print("T5 PASS: empty input handled (no match, empty signature)")
    finally:
        lib.clear()


# T6 -- match metrics shape
def test_match_metrics_shape():
    lib = _fresh_library()
    try:
        lib.add_signature("Bad pattern X", "label_x", "cat_x")
        result = lib.match("Bad pattern X", threshold=0.85)
        required_keys = {
            "matched", "best_label", "best_category",
            "best_score", "threshold", "all_matches", "n_library_entries"
        }
        missing = required_keys - set(result.keys())
        assert not missing, f"Missing keys: {missing}"
        assert isinstance(result["matched"], bool)
        assert isinstance(result["best_score"], float)
        assert 0.0 <= result["best_score"] <= 1.0
        assert isinstance(result["all_matches"], list)
        assert result["n_library_entries"] == 1
        print("T6 PASS: match result has correct keys and types")
    finally:
        lib.clear()


# T7 -- threshold monotonicity
def test_threshold_monotonicity():
    lib = _fresh_library()
    try:
        lib.add_signature("Pattern A", "a", "cat")
        lib.add_signature("Pattern B different", "b", "cat")
        lib.add_signature("Yet another pattern Z", "z", "cat")
        # Use a low threshold -- should match many
        r_low = lib.match("Pattern Q", threshold=0.0)
        n_low = len(r_low["all_matches"])
        # Use a high threshold -- should match fewer or zero
        r_hi = lib.match("Pattern Q", threshold=0.99)
        n_hi = len(r_hi["all_matches"])
        assert n_hi <= n_low, (
            f"Threshold monotonicity: high-thr matches ({n_hi}) "
            f"should be <= low-thr matches ({n_low})")
        print(f"T7 PASS: threshold monotonicity (low_thr={n_low} matches, "
              f"high_thr={n_hi})")
    finally:
        lib.clear()


# T8 -- determinism
def test_determinism():
    text = "Deterministic test input #42"
    sig_a = compute_signature(text)
    sig_b = compute_signature(text)
    sim = signatures_similarity(sig_a, sig_b)
    assert sim == 1.0, f"Signature must be deterministic: got similarity {sim}"
    assert sig_a["syndrome"] == sig_b["syndrome"]
    assert sig_a["op_prefix"] == sig_b["op_prefix"]
    print(f"T8 PASS: signature determinism (identical input -> identical "
          f"signature; similarity {sim})")


# Utility: byte-mod-10 sanity check
def test_op_path_byte_mod_10():
    text = "ABC"  # bytes: 65, 66, 67
    ops = text_to_op_path(text)
    assert ops == [5, 6, 7], f"Expected [5,6,7], got {ops}"
    print("T-aux PASS: text_to_op_path is byte-mod-10")


def run_all():
    print("=" * 64)
    print("ck_anomaly_detector regression tests")
    print("=" * 64)
    print()
    tests = [
        test_exact_self_match,
        test_clean_input_below_threshold,
        test_content_blindness_audit,
        test_multi_category_routing,
        test_empty_input_handling,
        test_match_metrics_shape,
        test_threshold_monotonicity,
        test_determinism,
        test_op_path_byte_mod_10,
    ]
    n_pass = 0
    n_fail = 0
    for t in tests:
        try:
            t()
            n_pass += 1
        except AssertionError as e:
            print(f"{t.__name__} FAIL: {e}")
            n_fail += 1
        except Exception as e:
            print(f"{t.__name__} ERROR: {type(e).__name__}: {e}")
            n_fail += 1
    print()
    print("=" * 64)
    print(f"RESULT: {n_pass}/{n_pass + n_fail} tests passed")
    print("=" * 64)
    return n_fail == 0


if __name__ == "__main__":
    ok = run_all()
    sys.exit(0 if ok else 1)
