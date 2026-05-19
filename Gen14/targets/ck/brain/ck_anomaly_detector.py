"""ck_anomaly_detector.py -- content-blind anomaly detection via operator-path signature matching.

═══════════════════════════════════════════════════════════════════════
The premise
═══════════════════════════════════════════════════════════════════════

This is the one TIG-specific use case where the substrate genuinely
outperforms generic alternatives.  Per META_SYNTHESIS_HUMANITY.md §1.4:

  "where you need a content-blind fingerprint + a stable fixed basis"

CK's substrate has both:
  (a) the operator-path mapping (byte → Z/10 op) is a deterministic
      one-pass fingerprint, training-free, content-blind beyond the
      resolution depth
  (b) the TSML/BHML/σ tables provide a stable fixed basis -- the
      signature has a meaningful operator-path interpretation that
      fits CK's domain reasoning

What this module does:
  - Takes input text
  - Computes a content-blind signature (operator path → substrate hash)
  - Matches against a library of known-bad signatures
  - Returns match/no-match + similarity score
  - NEVER retains the original content beyond the signature

This is "content moderation without content retention".  The signature
library stores only syndrome cascades + labels (e.g., "spam",
"phishing") -- never the original text.

═══════════════════════════════════════════════════════════════════════
Honest scope
═══════════════════════════════════════════════════════════════════════

This is NOT:
  - a replacement for ML-based content classifiers (which are more
    flexible to paraphrase)
  - a privacy guarantee against an attacker who knows the signature
    mapping (they can craft inputs to match arbitrary signatures)
  - a novel cryptographic primitive (the substrate hash is
    deterministic; signatures are NOT secure under chosen-plaintext)

This IS:
  - a deterministic, one-pass fingerprint for short text inputs
  - a content-blind audit trail (the institution can prove they
    detected pattern X without storing what pattern X looked like)
  - a stable-basis fixed-vocabulary tool (no model retraining;
    signatures generated once persist across the system's lifetime)

═══════════════════════════════════════════════════════════════════════
Architecture
═══════════════════════════════════════════════════════════════════════

  input_text  →  bytes  →  ops = [b % 10 for b in bytes]
                              ↓
                      substrate_hash(ops, depth=3)
                              ↓
                      signature = (op_path_short, syndrome_cascade)
                              ↓
                  match against library of known-bad signatures
                              ↓
                  return (matched: bool, label, similarity)

Similarity metric: Hamming-style overlap on syndrome cascades.
Match threshold: configurable (default: 0.85 similarity).

═══════════════════════════════════════════════════════════════════════
Library file format (JSONL, append-only)
═══════════════════════════════════════════════════════════════════════

Each line:
  {
    "label":     "spam_lottery_winner",
    "category":  "spam",
    "syndrome":  [[0,1,1,0,1,0,1], [1,1,0,1,0,0,1], [0,0,1,0,1,1,1]],
    "op_prefix": [3, 4, 5, 9, 2],  # first 5 ops only, for sanity check
    "added_ts":  1716100000.0
  }

The library is auditable: an external reviewer can see what categories
of pattern are matched, but cannot reconstruct the original content
from the syndrome.
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))


# ─── Fingerprinting ────────────────────────────────────────────────────

def text_to_op_path(text: str, max_len: int = 256) -> List[int]:
    """Convert text to a Z/10 operator path via byte-mod-10.

    Bounded to max_len bytes to keep signatures O(1) per input.
    """
    if not text:
        return []
    raw = text.encode("utf-8")[:max_len]
    return [b % 10 for b in raw]


def _fallback_syndrome(ops: List[int], depth: int = 3) -> List[Tuple[int, ...]]:
    """Fallback syndrome computation if ck_qutrit_apex.substrate_hash
    is unavailable.  Uses TSML/BHML-style local disagreement counts
    via a simple deterministic hash cascade.

    NOT cryptographically secure -- but stable and content-blind.
    """
    if not ops:
        return []
    cascade = []
    current = list(ops)
    for d in range(depth):
        synd = [0] * 7
        for i in range(len(current) - 1):
            a, b = current[i], current[i + 1]
            cell = (a + b) % 7
            # disagreement: parity-flavored
            if ((a * b) % 7) != ((a + b) % 7):
                synd[cell] ^= 1
        cascade.append(tuple(synd))
        # rotate
        current = [(o + d + 1) % 10 for o in current]
    return cascade


def compute_signature(text: str,
                       depth: int = 3,
                       max_len: int = 256) -> Dict[str, Any]:
    """Compute the content-blind signature of an input text.

    Returns:
      {
        "syndrome":  [[...], [...], [...]],   # depth-many 7-tuples
        "op_prefix": [...],                   # first 5 ops for sanity
        "op_path_len": N,                     # length of full op path
        "input_byte_len": N,                  # bytes consumed (≤ max_len)
      }

    The original text is NOT included in the return value.  Only the
    structural fingerprint.
    """
    ops = text_to_op_path(text, max_len=max_len)
    cascade: List[Tuple[int, ...]] = []
    try:
        import ck_qutrit_apex as _qa  # type: ignore[import-not-found]
        fn = getattr(_qa, "substrate_hash", None)
        if fn is not None:
            result = fn(ops, depth=depth)
            if result and isinstance(result, list) and isinstance(result[0], tuple):
                cascade = result
    except Exception:
        pass
    if not cascade:
        cascade = _fallback_syndrome(ops, depth=depth)
    return {
        "syndrome":     [list(c) for c in cascade],
        "op_prefix":    ops[:5],
        "op_path_len":  len(ops),
        "input_byte_len": min(len(text.encode("utf-8")) if text else 0, max_len),
    }


def signatures_similarity(sig_a: Dict[str, Any],
                            sig_b: Dict[str, Any]) -> float:
    """Hamming-style similarity over syndrome cascades.

    Returns: float in [0, 1].  1.0 = identical syndromes; 0.0 = total
    disagreement on every bit.
    """
    a = sig_a.get("syndrome") or []
    b = sig_b.get("syndrome") or []
    if not a or not b:
        return 0.0
    # Truncate to matching depth
    depth = min(len(a), len(b))
    matches = 0
    total = 0
    for d in range(depth):
        for i in range(7):
            total += 1
            if d < len(a) and d < len(b) and i < len(a[d]) and i < len(b[d]):
                if a[d][i] == b[d][i]:
                    matches += 1
    if total == 0:
        return 0.0
    return matches / total


# ─── Library ───────────────────────────────────────────────────────────

class SignatureLibrary:
    """A library of known-bad signatures, persisted to JSONL.

    NEVER stores the original text content.  Only:
      - label (category-specific name)
      - category (high-level grouping)
      - syndrome (the content-blind fingerprint)
      - op_prefix (first 5 ops, for sanity check)
      - added_ts (when added)
    """

    def __init__(self, library_path: Optional[Path] = None):
        self.library_path = library_path or HERE / "anomaly_signatures.jsonl"
        self.entries: List[Dict[str, Any]] = []
        self._load()

    def _load(self) -> None:
        if not self.library_path.exists():
            return
        try:
            with open(self.library_path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        self.entries.append(json.loads(line))
                    except Exception:
                        continue
        except Exception:
            pass

    def add_signature(self,
                       text_sample: str,
                       label: str,
                       category: str,
                       depth: int = 3) -> Dict[str, Any]:
        """Compute the signature of a sample, store under (category, label).

        The text_sample is consumed for signature computation and then
        DROPPED -- only the signature persists.
        """
        sig = compute_signature(text_sample, depth=depth)
        entry = {
            "label":         str(label),
            "category":      str(category),
            "syndrome":      sig["syndrome"],
            "op_prefix":     sig["op_prefix"],
            "op_path_len":   sig["op_path_len"],
            "added_ts":      float(time.time()),
        }
        self.entries.append(entry)
        try:
            self.library_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.library_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False,
                                    sort_keys=True) + "\n")
        except Exception:
            pass
        # text_sample goes out of scope here.  Signature is what persists.
        return {"added": True, "label": label, "category": category}

    def match(self,
               text: str,
               threshold: float = 0.85,
               depth: int = 3) -> Dict[str, Any]:
        """Match input text against library.

        Returns:
          {
            "matched":     bool,
            "best_label":  str or None,
            "best_category": str or None,
            "best_score":  float,
            "all_matches": [(score, label, category), ...] above threshold
          }

        The input `text` is consumed for signature computation only.
        After this call returns, the function holds no reference to the
        original text content.
        """
        input_sig = compute_signature(text, depth=depth)
        all_scores: List[Tuple[float, str, str]] = []
        best_score = 0.0
        best_label = None
        best_category = None
        for entry in self.entries:
            score = signatures_similarity(input_sig, entry)
            if score >= threshold:
                all_scores.append((score, entry["label"], entry["category"]))
            if score > best_score:
                best_score = score
                best_label = entry["label"]
                best_category = entry["category"]
        all_scores.sort(reverse=True)
        return {
            "matched":        best_score >= threshold,
            "best_label":     best_label if best_score >= threshold else None,
            "best_category":  best_category if best_score >= threshold else None,
            "best_score":     best_score,
            "threshold":      threshold,
            "all_matches":    all_scores[:10],
            "n_library_entries": len(self.entries),
        }

    def stats(self) -> Dict[str, Any]:
        """Summary of the library."""
        from collections import Counter
        cats = Counter(e["category"] for e in self.entries)
        return {
            "n_entries":  len(self.entries),
            "categories": dict(cats),
            "library_path": str(self.library_path),
        }

    def clear(self) -> None:
        """Wipe the library (for testing).  Removes both the in-memory
        entries and the persisted file."""
        self.entries = []
        try:
            if self.library_path.exists():
                self.library_path.unlink()
        except Exception:
            pass


# ─── Engine mount (Flask endpoints) ────────────────────────────────────

def mount_anomaly_detector(engine: Any,
                             library: Optional[SignatureLibrary] = None
                             ) -> bool:
    """Mount the anomaly detector on the engine + register endpoints.

    Endpoints (read-only; no input retention):
      POST /anomaly/check    -- match an input against the library
      GET  /anomaly/stats    -- library summary
      GET  /anomaly/info     -- module philosophy
    """
    lib = library or SignatureLibrary()
    engine.ck_anomaly_detector = {
        "library":            lib,
        "compute_signature":  compute_signature,
        "match":              lib.match,
        "stats":              lib.stats,
    }

    api = getattr(engine, "web_api", None) or getattr(engine, "api", None)
    if api is not None:
        app = getattr(api, "_app", None) or getattr(api, "app", None)
        if app is not None:
            try:
                from flask import jsonify, request  # type: ignore

                def _info():
                    return jsonify({
                        "module":     "ck_anomaly_detector",
                        "philosophy": ("content-blind signature matching; "
                                        "input content never retained"),
                        "endpoints": [
                            "POST /anomaly/check",
                            "GET  /anomaly/stats",
                            "GET  /anomaly/info",
                        ],
                    })

                def _check():
                    payload = request.get_json(silent=True) or {}
                    text = payload.get("text") or ""
                    thr = float(payload.get("threshold", 0.85))
                    result = lib.match(text, threshold=thr)
                    # do NOT echo the input in the response
                    return jsonify(result)

                def _stats():
                    return jsonify(lib.stats())

                existing = set(r.rule for r in app.url_map.iter_rules())
                for rule, ep, fn, methods in (
                    ("/anomaly/info",   "anomaly_info",   _info,  ["GET"]),
                    ("/anomaly/check",  "anomaly_check",  _check, ["POST"]),
                    ("/anomaly/stats",  "anomaly_stats",  _stats, ["GET"]),
                ):
                    if rule not in existing:
                        app.add_url_rule(rule, endpoint=ep,
                                          view_func=fn, methods=methods)
            except Exception as e:
                print(f"[CK Gen14] anomaly_detector route registration "
                      f"failed: {e}")

    print(f"[CK Gen14] anomaly_detector: MOUNTED  "
          f"entries={len(lib.entries)}  library={lib.library_path.name}")
    return True


# ─── CLI smoke ────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("ck_anomaly_detector smoke test:")
    print()

    # Use a temp library for testing
    import tempfile
    tmp = Path(tempfile.gettempdir()) / "ck_anomaly_smoke.jsonl"
    if tmp.exists():
        tmp.unlink()
    lib = SignatureLibrary(library_path=tmp)

    # Add some known-bad patterns (synthetic, for demonstration)
    print("Step 1: populate library with synthetic bad-content patterns")
    print("-" * 60)
    bad_samples = [
        ("Congratulations! You have won $1,000,000! Click here NOW!!!",
         "spam_lottery_winner", "spam"),
        ("URGENT: Your account will be CLOSED. Verify identity immediately.",
         "phishing_account_urgent", "phishing"),
        ("Hot singles in your area want to meet you tonight!",
         "spam_dating", "spam"),
        ("Send 1 BTC to wallet ABC and double it instantly!",
         "scam_crypto_doubler", "scam"),
        ("Your PayPal account has been suspended. Click link to restore.",
         "phishing_paypal", "phishing"),
    ]
    for text, label, cat in bad_samples:
        result = lib.add_signature(text, label, cat)
        print(f"  + {result['category']:10s} / {result['label']}")
    print()
    print(f"  Library: {lib.stats()}")
    print()

    # Test with paraphrases of bad patterns
    print("Step 2: test matching on near-duplicate bad inputs")
    print("-" * 60)
    test_inputs = [
        ("Congratulations! You have won $1,000,000! Click here NOW!!!",
         "exact match expected"),
        ("CONGRATULATIONS! you won 1000000$ click HERE now",
         "casing/punct paraphrase"),
        ("Hello, how are you today?",
         "clean input -- should NOT match"),
        ("Your bank account has been suspended. Verify identity now.",
         "near-phishing -- may match"),
    ]
    for text, note in test_inputs:
        result = lib.match(text, threshold=0.85)
        verdict = "FLAG" if result["matched"] else "PASS"
        print(f"  [{verdict}] score={result['best_score']:.3f}  "
              f"note: {note}")
        if result["matched"]:
            print(f"         -> matched: {result['best_category']} / "
                  f"{result['best_label']}")
    print()

    # Demonstrate content-blindness
    print("Step 3: confirm library never stores original text")
    print("-" * 60)
    print(f"  Library file: {lib.library_path}")
    print(f"  First entry: {json.dumps(lib.entries[0], indent=2)[:300]}")
    print()
    print("  NOTE: only 'syndrome', 'label', 'category', 'op_prefix',")
    print("        'added_ts' are stored.  Original text is gone.")
    print()

    # Cleanup
    print("Step 4: clean up smoke test artifacts")
    print("-" * 60)
    lib.clear()
    print(f"  Library cleared.  File exists: {tmp.exists()}")
    print()
    print("Smoke test complete.")
