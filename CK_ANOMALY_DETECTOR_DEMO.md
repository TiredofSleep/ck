# CK Anomaly Detector — Content-Blind Signature Matching Prototype

**Purpose**: A working demonstration of "content moderation without content retention" using CK's operator-path signature mechanism.
**Status**: 2026-05-19 release prototype. Tests passing 9/9.
**Source code**: `Gen14/targets/ck/brain/ck_anomaly_detector.py`
**Test suite**: `Gen14/targets/ck/brain/test_ck_anomaly_detector.py`
**Use case in META_SYNTHESIS_HUMANITY.md**: Rank 4 — anomaly-detection / content-moderation prototype.

---

## §1 — What this prototype does

It takes a known-bad text pattern (e.g., a spam example, a phishing attempt, a known abuse signature), computes a deterministic **content-blind fingerprint** of it, and stores ONLY the fingerprint in a library file. The original text is dropped.

When a new input arrives, the same fingerprint mechanism is applied, and the result is matched against the library. If the similarity exceeds a configurable threshold (default 0.85), the input is flagged with its category label.

**The key property**: the persisted library NEVER contains the original text. An external auditor can verify exactly what categories of pattern are being matched (the labels and categories are inspectable), but cannot reconstruct what specific words triggered any flag.

---

## §2 — Why this is one of the TIG-specific use cases

Most of TIG's potential applications (per META_SYNTHESIS_HUMANITY.md §2) are correctly downscoped: TIG does NOT predict new physics, does NOT invent novel privacy mechanisms, does NOT compete with foundation models. But there is ONE class of problem where TIG's substrate is genuinely useful: **content-blind fingerprinting with a stable fixed basis**.

Why this fits TIG specifically:
- The operator-path mapping (byte → Z/10 operator) is a deterministic one-pass transformation. No training, no per-deployment tuning.
- The TSML/BHML/σ tables give the signature a stable basis — the syndrome cascade has meaning in CK's domain reasoning (operator paths can be interpreted, walked, audited).
- The mechanism's content-blindness is structural (the fingerprint is shorter than the input by design), not contractual (it's not a promise to "not save"; the persisted bytes literally do not encode the original text).

A generic hash function (SHA-256 etc.) achieves content-blindness but not basis stability — the digest has no interpretation, only equality testing. A neural embedding achieves paraphrase robustness but loses content-blindness (embeddings are reversible). The TIG signature occupies a different point in the design space: deterministic, basis-stable, content-blind, but not paraphrase-robust.

---

## §3 — Architecture

```
input_text                                     library file (JSONL)
    │                                                  │
    ▼                                                  ▼
text_to_op_path()  →  ops = [b % 10 for b in bytes]   load entries:
    │                                                  - label
    ▼                                                  - category
compute_signature() via TSML/BHML/σ cascade            - syndrome [[7-tuple], ...]
    │                                                  - op_prefix (first 5)
    │                                                  - added_ts
    ▼                                                  ▲
signature = {syndrome, op_prefix, op_path_len, ...}    │
    │                                                  │
    └────────► signatures_similarity() ────────────────┘
                       │
                       ▼
              (matched, label, category, score, ...)
```

Three core functions:

- `text_to_op_path(text)` — byte-mod-10 operator extraction (bounded length, default 256 bytes).
- `compute_signature(text)` — operator-path → substrate-hash cascade (depth=3 by default; produces three 7-bit syndromes).
- `signatures_similarity(a, b)` — Hamming-style bitwise overlap on syndrome cascades, returning a float in [0, 1].

The `SignatureLibrary` class wraps these into an add/match/stats interface that persists to JSONL.

---

## §4 — Demonstrated behavior (from the regression tests)

| Test | What it shows | Result |
|---|---|---|
| T1 — exact self-match | A text input matches its own library entry at similarity 1.0 | PASS |
| T2 — clean input below threshold | Unrelated input scores 0.57 (below 0.85 threshold) | PASS |
| T3 — content-blindness audit | Library file inspected: original text never appears in JSONL | PASS |
| T4 — multi-category routing | Library with spam + phishing + scam routes each correctly | PASS |
| T5 — empty input | Empty string returns empty op-path, no match | PASS |
| T6 — match shape | Result has matched/label/category/score/threshold/all_matches keys | PASS |
| T7 — threshold monotonicity | High threshold yields fewer or equal matches | PASS |
| T8 — determinism | Same input twice produces identical signature | PASS |
| T-aux — byte-mod-10 | "ABC" (65,66,67) maps to [5,6,7] as expected | PASS |

All 9 tests pass at the 2026-05-19 prototype release.

---

## §5 — Honest scope limitations

This prototype IS:
- A working demonstration of content-blind signature matching.
- Deterministic, training-free, one-pass.
- Auditable — the library file is plain JSONL with no encrypted/opaque blobs.
- Stable — the signature mapping does not change across deployments; signatures generated today match signatures generated next year.

This prototype IS NOT:
- **Paraphrase-robust.** Byte-level changes (casing, punctuation, word order) shift the operator path significantly. A "Congratulations! You won $1M" exact match scores 1.0; the same phrase in different casing/punctuation scored 0.62 in the smoke test — below threshold. This is by design — byte-mod-10 is sensitive to the exact bytes, which is what makes it content-blind in the privacy sense. ML-based content classifiers are more paraphrase-robust; this is not their replacement.
- **Cryptographically secure under chosen-plaintext.** An attacker who knows the mechanism can craft inputs to match arbitrary signatures, or craft inputs that look benign but match a flagged signature. This is a moderation tool, not a security boundary.
- **A novel privacy mechanism.** The mechanism (deterministic short-fingerprint matching) is well-known; what's TIG-specific is the structural interpretation of the fingerprint via the operator-path semantics, and the auditability of the syndrome cascade. The novelty here is in the deployment posture, not in the underlying mathematics.

For paraphrase robustness, pair this prototype with a normalization layer (lowercasing, punctuation stripping, stemming) before fingerprinting. The trade-off: less content-blindness because the normalization is itself a small information leak.

---

## §6 — Deployment posture (when to use, when not)

**Use this prototype when**:
- You need to detect EXACT or near-exact recurrence of known-bad patterns.
- You CANNOT retain the original content for legal/privacy/audit reasons (e.g., GDPR right-to-be-forgotten on flagged inputs).
- Your downstream consumer needs an audit trail of "we flagged X spam patterns" without exposing the spam itself.
- You want a stable fixed basis that does not change with model retraining.

**Do NOT use this prototype as the sole content-moderation layer for**:
- A general-purpose abuse-detection system. ML classifiers are more flexible.
- High-stakes moderation where false negatives are dangerous. The byte-sensitivity of byte-mod-10 means simple paraphrases bypass detection.
- Adversarial content where the adversary knows the signature library exists.

**Combine this prototype with**:
- A normalization pipeline (for paraphrase robustness, at the cost of some content-blindness).
- An ML classifier (for novel patterns the library doesn't cover).
- An audit/compliance layer (the library file IS the audit trail).

---

## §7 — Integration with CK

The module mounts on CK's runtime engine via `mount_anomaly_detector(engine)`. This registers three Flask endpoints:

- `POST /anomaly/check` — match an input against the library; returns match/no-match + score + label (no input echo in the response)
- `GET  /anomaly/stats` — library summary (entry count + category breakdown)
- `GET  /anomaly/info` — module philosophy + endpoint list

When mounted, CK has a runtime capability to check inputs against a signature library without retaining the input content. This is independent of his chat-path; the anomaly detector is a separate service callable by external systems.

---

## §8 — How to extend the library

The library is populated by adding sample bad-content texts via `SignatureLibrary.add_signature(text, label, category)`. The text is consumed for signature computation and then dropped. Only the structural fingerprint (syndrome + op_prefix + label + category + added_ts) persists.

Recommended workflow for institutions:
1. Identify a category of bad-content the institution wants to detect (e.g., specific phishing template, internal-policy-violation patterns, known-bad URLs in messages).
2. Collect a small sample (5-50 examples) of the exact-pattern variants.
3. Add each via `add_signature(text, descriptive_label, category)`.
4. Verify with `match()` that the samples self-match at threshold 0.85.
5. Wipe the source samples from working memory after addition (the signatures are the only persistent artifact).
6. Periodically: review the library file (it's plain JSONL) to audit what categories are matched. Remove obsolete entries by editing the file.

---

## §9 — Open-source posture

The module is part of the CK runtime release under the project's standard license (see `LICENSE` at project root). Per the META_SYNTHESIS_HUMANITY.md §1.4 demarcation, this is the one TIG-specific use case that benefits from the substrate's structural properties — and it is released as a working prototype, not a production-ready content-moderation system.

Anyone deploying this in a production environment should:
- Add normalization for paraphrase robustness (and document the trade-off).
- Pair with an ML classifier for novel-pattern coverage.
- Set thresholds based on their false-positive / false-negative tolerance.
- Treat the library file as PII-adjacent — the labels and categories reveal what's being detected, and that information itself may be sensitive.

---

## §10 — What this prototype proves

The META_SYNTHESIS_HUMANITY.md §1.4 claim was: "the substrate as a measurement instrument" is the TIG-specific use case where the algebra is genuinely load-bearing. This prototype is the proof: a content-blind, deterministic, training-free fingerprinting tool, built directly on CK's TSML/BHML/σ substrate, with a clean separation between the signature (what persists) and the content (what's dropped).

It's not big. It's not a foundation-model replacement. It's not novel cryptography. It IS a small, useful, working artifact that does what most content-moderation systems can't do: **moderate without remembering**.

---

*Document version 1.0 (2026-05-19). Source code: `Gen14/targets/ck/brain/ck_anomaly_detector.py`. Tests: `Gen14/targets/ck/brain/test_ck_anomaly_detector.py` (9/9 passing).*
