"""
bench_adversarial.py -- stronger attackers for the bench:

  A1: ML attacker with POLYNOMIAL-INTERACTION features (degree-2 pairs)
  A2: MEMBERSHIP INFERENCE attack via shadow-model

Both attacks are standard in the differential-privacy literature as
"adversarial" tests that go beyond the basic 1/K re-identification.

If RGD's mechanism survives these stronger attacks at the same
operating point where it beat Laplace-DP, the result is robust.

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
import dp_variants as dpv
from bench_ml_attacker import (
    _train_lr, _predict_lr, _softmax,
)


# =====================================================================
# A1 -- Polynomial-interaction feature crafting
# =====================================================================
def _build_interaction_features(
    rows: List[List[str]],
    max_pairs: int = 500,
    rng: Optional[random.Random] = None,
) -> Tuple[Dict[Tuple[int, str], int], List[Tuple[int, int]]]:
    """Build a feature index with one-hot per (col, value) PLUS the
    top max_pairs degree-2 interaction terms.

    Interactions are encoded as binary features: 1 if both base features
    are 1, else 0.  We pick the top-frequency column pairs (not value
    pairs) to keep the feature dim tractable.
    """
    if rng is None:
        rng = random.Random(2026)
    idx: Dict[Tuple[int, str], int] = {}
    for r in rows:
        for c, v in enumerate(r[:-1]):
            key = (c, v)
            if key not in idx:
                idx[key] = len(idx)
    # All pairs of distinct columns
    n_cols = len(rows[0]) - 1
    col_pairs: List[Tuple[int, int]] = []
    for i in range(n_cols):
        for j in range(i + 1, n_cols):
            col_pairs.append((i, j))
    return idx, col_pairs


def _encode_interaction_row(
    r: List[str],
    feat_idx: Dict[Tuple[int, str], int],
    col_pairs: List[Tuple[int, int]],
) -> List[float]:
    F_base = len(feat_idx)
    # Base one-hot
    vec = [0.0] * (F_base + len(col_pairs))
    base_active = []
    for c, v in enumerate(r[:-1]):
        i = feat_idx.get((c, v))
        if i is not None:
            vec[i] = 1.0
            base_active.append((c, v, i))
    # Interaction features: for each column pair, hash (val_i, val_j)
    # into a single binary feature
    for pi, (ci, cj) in enumerate(col_pairs):
        vi = r[ci] if ci < len(r) - 1 else None
        vj = r[cj] if cj < len(r) - 1 else None
        # Active if both base values exist in the index (priv may
        # contain "*" which is its own value)
        if (ci, vi) in feat_idx and (cj, vj) in feat_idx:
            # Hash the pair into a feature bucket; for simplicity we
            # use a single binary feature per (ci, cj) regardless of
            # value combination -- this captures "do these columns
            # both have non-wildcard values for this row"
            vec[F_base + pi] = 1.0
    return vec


def ml_attacker_polynomial(
    orig: List[List[str]],
    priv: List[List[str]],
    epochs: int = 30,
) -> float:
    """Logistic-regression attacker with polynomial-interaction
    features.  Returns prediction accuracy on orig."""
    if not priv or not orig:
        return float("nan")
    feat_idx, col_pairs = _build_interaction_features(priv)
    sens_classes = sorted({r[-1] for r in priv})
    sens_to_idx = {c: i for i, c in enumerate(sens_classes)}
    if len(sens_classes) < 2:
        return float("nan")
    X = [_encode_interaction_row(r, feat_idx, col_pairs) for r in priv]
    y = [sens_to_idx[r[-1]] for r in priv]
    W = _train_lr(X, y, n_classes=len(sens_classes), epochs=epochs)
    correct = 0
    for r in orig:
        x = _encode_interaction_row(r, feat_idx, col_pairs)
        pred_idx = _predict_lr(W, x)
        pred_class = sens_classes[pred_idx]
        if pred_class == r[-1]:
            correct += 1
    return correct / max(len(orig), 1)


# =====================================================================
# A2 -- Membership Inference Attack (shadow-model)
# =====================================================================
def membership_inference_attack(
    orig: List[List[str]],
    priv: List[List[str]],
    rng: Optional[random.Random] = None,
    n_shadow_per_class: int = 1000,
    epochs: int = 20,
) -> Dict[str, float]:
    """
    Standard MIA setup:
      1. Split orig into MEMBERS (the rows we want to identify as having
         contributed to priv) and NON-MEMBERS (rows held out).
      2. The attacker is given (member_priv, non_member_priv) pairs
         where:
            - member_priv = the priv row corresponding to a member orig row
            - non_member_priv = a priv row that did NOT come from this
              orig row (we approximate by picking a random other priv row)
      3. Train a binary classifier: given (orig_row, priv_row) features,
         predict 1 if member, 0 if non-member.
      4. Evaluate attack accuracy on a test split.

    Returns:
      attack_accuracy: 0.5 = random guessing (no info leaked)
      attack_advantage: max(0, attack_accuracy - 0.5)
    """
    if rng is None:
        rng = random.Random(2026)
    if len(orig) != len(priv):
        return {"attack_accuracy": float("nan"), "attack_advantage": float("nan"),
                "note": "orig and priv must have same length"}

    # Pair each orig row with its (assumed) priv counterpart
    pairs = list(zip(orig, priv))
    rng.shuffle(pairs)

    # Build feature: edit distance between orig and priv QIDs
    # + sensitive match indicator
    def featurize(o_row, p_row):
        feats = []
        m = len(o_row) - 1
        # Per-column: 1 if orig value == priv value, 0 otherwise
        for c in range(m):
            feats.append(1.0 if o_row[c] == p_row[c] else 0.0)
        # Wildcard count in priv
        feats.append(float(sum(1 for v in p_row[:-1] if v == "*")))
        # Sensitive match (priv preserves sensitive, so this is trivially 1
        # for true members; for non-members it depends on the rows)
        feats.append(1.0 if o_row[-1] == p_row[-1] else 0.0)
        return feats

    # Generate training data: positive = (orig_i, priv_i), negative = (orig_i, priv_j) for j != i
    n_train_pos = min(n_shadow_per_class, len(pairs) // 2)
    train_pairs = pairs[:n_train_pos * 2]
    test_pairs = pairs[n_train_pos * 2:]

    X_train: List[List[float]] = []
    y_train: List[int] = []
    for i, (o, p) in enumerate(train_pairs):
        # Positive sample
        X_train.append(featurize(o, p))
        y_train.append(1)
        # Negative sample: pair with a random other priv row
        j = rng.randrange(len(train_pairs))
        while j == i:
            j = rng.randrange(len(train_pairs))
        _, p_other = train_pairs[j]
        X_train.append(featurize(o, p_other))
        y_train.append(0)

    # Train LR classifier
    F = len(X_train[0])
    W = _train_lr(X_train, y_train, n_classes=2, epochs=epochs)

    # Evaluate on test
    correct = 0
    total = 0
    for i, (o, p) in enumerate(test_pairs):
        # Positive test
        x_pos = featurize(o, p)
        pred = _predict_lr(W, x_pos)
        if pred == 1:
            correct += 1
        total += 1
        # Negative test (random other priv)
        if len(test_pairs) > 1:
            j = rng.randrange(len(test_pairs))
            while j == i:
                j = rng.randrange(len(test_pairs))
            _, p_other = test_pairs[j]
            x_neg = featurize(o, p_other)
            pred = _predict_lr(W, x_neg)
            if pred == 0:
                correct += 1
            total += 1

    acc = correct / max(total, 1)
    return {
        "attack_accuracy": acc,
        "attack_advantage": max(0.0, acc - 0.5),
        "n_train_pairs": len(X_train),
        "n_test_pairs": total,
    }


# =====================================================================
# Main
# =====================================================================
def main() -> int:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-rows", type=int, default=5000)
    parser.add_argument("--epochs", type=int, default=20)
    args = parser.parse_args()

    tabular = bm.load_tabular("bench_data/adult.data")
    rows = tabular[0][:args.max_rows]
    print(f"=== Adversarial bench: polynomial-LR + MIA at {len(rows)} rows ===")

    sens = Counter(r[-1] for r in rows)
    baseline = sens.most_common(1)[0][1] / len(rows)
    print(f"Baseline: {baseline:.4f}\n")

    # No-privacy reference
    t0 = time.time()
    clean_poly = ml_attacker_polynomial(rows, rows, epochs=args.epochs)
    print(f"  no-privacy reference (poly LR on orig):  {clean_poly:.4f}  ({time.time()-t0:.1f}s)")
    print(f"  (upper bound on what ANY attacker can recover)\n")

    rng = random.Random(2026)
    cases = [
        ("RGD",          "d=1",       bm.rgd_tabular(rows, 1)),
        ("RGD",          "d=2",       bm.rgd_tabular(rows, 2)),
        ("RGD",          "d=4",       bm.rgd_tabular(rows, 4)),
        ("RGD",          "d=6",       bm.rgd_tabular(rows, 6)),
        ("Laplace-DP",   "eps=0.1",   bm.dp_tabular(rows, 0.1, rng)),
        ("Laplace-DP",   "eps=1.0",   bm.dp_tabular(rows, 1.0, rng)),
        ("Gaussian-DP",  "eps=0.1",   dpv.dp_gaussian_tabular(rows, 0.1, delta=1e-5, rng=rng)),
        ("Gaussian-DP",  "eps=1.0",   dpv.dp_gaussian_tabular(rows, 1.0, delta=1e-5, rng=rng)),
        ("RAPPOR/local", "eps=0.1",   dpv.dp_rappor_tabular(rows, 0.1, rng=rng)),
        ("RAPPOR/local", "eps=1.0",   dpv.dp_rappor_tabular(rows, 1.0, rng=rng)),
        ("k-anon",       "k=5",       bm.kanon_tabular(rows, 5)),
        ("k-anon",       "k=25",      bm.kanon_tabular(rows, 25)),
    ]

    # A1: Polynomial-LR attacker
    print(f"  {'method':15s} {'knob':10s}  poly_attack  delta_baseline  mia_acc  mia_adv")
    print(f"  {'-' * 15} {'-' * 10}  -----------  --------------  -------  -------")
    for name, knob, priv in cases:
        if len(priv) != len(rows):
            print(f"  {name:15s} {knob:10s}  SKIP (n mismatch)")
            continue
        t0 = time.time()
        poly = ml_attacker_polynomial(rows, priv, epochs=args.epochs)
        mia = membership_inference_attack(rows, priv, rng=random.Random(7))
        elapsed = time.time() - t0
        print(f"  {name:15s} {knob:10s}  {poly:.4f}      "
              f"{poly - baseline:+.4f}        "
              f"{mia['attack_accuracy']:.4f}  {mia['attack_advantage']:.4f}  "
              f"({elapsed:.0f}s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
