"""
bench_ml_attacker.py -- replace the k-anon-style 1/K attacker with a
LEARNING-BASED attacker that uses the released priv data to train a
classifier and predict the sensitive attribute for orig rows.

This is the harder attack model that D134 flagged as a follow-up.

The learning attacker:
  1. From priv, build a one-hot feature representation of priv-QIDs
     (treating "*" as its own value)
  2. Train a multinomial logistic regression (numpy-only, no sklearn)
     on (priv features) -> (priv sensitive)
  3. For each orig row, encode orig QID into the same feature space
     and predict via the trained classifier
  4. Accuracy = fraction of orig rows whose true sensitive matches
     the predicted

This is harder than the majority-vote attacker because:
- It can learn from rare-but-discriminative QID values
- It generalizes across feature combinations (not just exact-match groups)
- It exploits joint structure in the QID columns

Compare to the baseline 1/K attacker on the same priv outputs to see
which attack model RGD's defense holds up against.

Copyright (c) 2026 Brayden Ross Sanders / 7SiTe LLC.
"""
from __future__ import annotations

import math
import os
import random
import sys
import time
from collections import Counter, defaultdict
from typing import Any, Dict, List, Optional, Tuple

HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)

import bench_rgd_vs_dp_kanon as bm


# =====================================================================
# Feature encoding: priv rows -> one-hot vectors
# =====================================================================
def _build_feature_index(rows: List[List[str]]) -> Dict[Tuple[int, str], int]:
    """Map (column_index, value_string) -> feature index in {0..F-1}.
    Treats "*" as its own value (so the attacker explicitly sees the
    suppression pattern)."""
    idx: Dict[Tuple[int, str], int] = {}
    for r in rows:
        for c, v in enumerate(r[:-1]):
            key = (c, v)
            if key not in idx:
                idx[key] = len(idx)
    return idx


def _encode_row(r: List[str], feat_idx: Dict[Tuple[int, str], int]) -> List[float]:
    """One-hot encode a row's QID values into a feature vector."""
    F = len(feat_idx)
    vec = [0.0] * F
    for c, v in enumerate(r[:-1]):
        i = feat_idx.get((c, v))
        if i is not None:
            vec[i] = 1.0
    return vec


def _encode_orig_under_priv_features(
    r: List[str],
    feat_idx: Dict[Tuple[int, str], int],
) -> List[float]:
    """Encode an orig row into the priv feature space.  Treats orig
    values that don't appear in priv as "unknown" (zero vector)."""
    F = len(feat_idx)
    vec = [0.0] * F
    for c, v in enumerate(r[:-1]):
        i = feat_idx.get((c, v))
        if i is not None:
            vec[i] = 1.0
    return vec


# =====================================================================
# Multinomial logistic regression in pure numpy / pure python
# =====================================================================
def _softmax(z: List[float]) -> List[float]:
    m = max(z)
    e = [math.exp(zi - m) for zi in z]
    s = sum(e)
    return [ei / s for ei in e]


def _train_lr(
    X: List[List[float]],
    y: List[int],
    n_classes: int,
    lr: float = 0.5,
    epochs: int = 100,
    l2: float = 1e-4,
    rng: Optional[random.Random] = None,
) -> List[List[float]]:
    """Multinomial logistic regression via SGD.  Returns weight
    matrix W of shape (n_classes, F+1) -- last column = bias."""
    if rng is None:
        rng = random.Random(2026)
    F = len(X[0])
    W = [[0.0] * (F + 1) for _ in range(n_classes)]
    indices = list(range(len(X)))
    for epoch in range(epochs):
        rng.shuffle(indices)
        for i in indices:
            x = X[i]
            yi = y[i]
            # Compute logits + bias
            z = []
            for c in range(n_classes):
                s = W[c][F]  # bias
                for f, xf in enumerate(x):
                    if xf:  # one-hot is sparse
                        s += W[c][f] * xf
                z.append(s)
            p = _softmax(z)
            # Gradient: (p_c - 𝟙[c=yi]) * x
            for c in range(n_classes):
                err = p[c] - (1.0 if c == yi else 0.0)
                for f, xf in enumerate(x):
                    if xf:
                        W[c][f] -= lr * (err * xf + l2 * W[c][f])
                W[c][F] -= lr * err
    return W


def _predict_lr(W: List[List[float]], x: List[float]) -> int:
    n_classes = len(W)
    F = len(x)
    z = [W[c][F] + sum(W[c][f] * x[f] for f in range(F) if x[f]) for c in range(n_classes)]
    return max(range(n_classes), key=lambda c: z[c])


# =====================================================================
# ML attacker
# =====================================================================
def ml_attribute_attacker(
    orig: List[List[str]],
    priv: List[List[str]],
    epochs: int = 50,
) -> float:
    """Train LR on priv (features -> sensitive), predict for orig.
    Returns accuracy."""
    if not priv or not orig:
        return float("nan")
    # Build feature index from priv (which is what the attacker sees)
    feat_idx = _build_feature_index(priv)
    sens_classes = sorted({r[-1] for r in priv})
    sens_to_idx = {c: i for i, c in enumerate(sens_classes)}
    if len(sens_classes) < 2:
        return float("nan")

    X = [_encode_row(r, feat_idx) for r in priv]
    y = [sens_to_idx[r[-1]] for r in priv]

    W = _train_lr(X, y, n_classes=len(sens_classes), epochs=epochs)

    correct = 0
    for r in orig:
        x = _encode_orig_under_priv_features(r, feat_idx)
        pred_idx = _predict_lr(W, x)
        pred_class = sens_classes[pred_idx]
        if pred_class == r[-1]:
            correct += 1
    return correct / max(len(orig), 1)


# =====================================================================
# Main: run ML attacker against all methods at a few key knobs
# =====================================================================
def main(argv: List[str]) -> int:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--tabular", default="bench_data/adult.data")
    parser.add_argument("--max-rows", type=int, default=10000)
    parser.add_argument("--epochs", type=int, default=30)
    args = parser.parse_args(argv)

    tabular = bm.load_tabular(args.tabular)
    rows = tabular[0][:args.max_rows]
    print(f"=== ML-attacker bench at {len(rows)} rows, {args.epochs} epochs ===")

    # Baseline: predict population majority
    sens = Counter(r[-1] for r in rows)
    maj_class, maj_count = sens.most_common(1)[0]
    baseline = maj_count / len(rows)
    print(f"Population baseline (predict majority '{maj_class}'): {baseline:.4f}")
    print()

    # No-privacy reference: attacker has clean orig data
    t0 = time.time()
    clean_acc = ml_attribute_attacker(rows, rows, epochs=args.epochs)
    print(f"  no-privacy reference   (attacker on orig): {clean_acc:.4f}  ({time.time()-t0:.1f}s)")
    print(f"  upper bound for what the ML attacker can EVER recover")
    print()

    # Each method at a key knob
    rng = random.Random(2026)
    cases = [
        ("RGD",     "d=1",  bm.rgd_tabular(rows, 1)),
        ("RGD",     "d=2",  bm.rgd_tabular(rows, 2)),
        ("RGD",     "d=4",  bm.rgd_tabular(rows, 4)),
        ("RGD",     "d=6",  bm.rgd_tabular(rows, 6)),
        ("DP",      "eps=0.1", bm.dp_tabular(rows, 0.1, rng)),
        ("DP",      "eps=1.0", bm.dp_tabular(rows, 1.0, rng)),
        ("DP",      "eps=10",  bm.dp_tabular(rows, 10.0, rng)),
        ("k-anon",  "k=5",  bm.kanon_tabular(rows, 5)),
        ("k-anon",  "k=25", bm.kanon_tabular(rows, 25)),
    ]

    print(f"  {'method':7s} {'knob':10s}  ml_attack   delta_baseline   majvote_attr")
    print(f"  {'-'*7} {'-'*10}  ---------   --------------   ------------")
    for name, knob, priv in cases:
        t0 = time.time()
        ml = ml_attribute_attacker(rows, priv, epochs=args.epochs)
        # Compare to the majority-vote attacker from extensions
        from bench_extensions import attribute_disclosure_attacker
        mv = attribute_disclosure_attacker(rows, priv)
        elapsed = time.time() - t0
        print(f"  {name:7s} {knob:10s}  {ml:.4f}      {ml - baseline:+.4f}        {mv:.4f}  ({elapsed:.0f}s)")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
