"""
qec_hska.py -- QEC-Encoded HSKA, the genuinely TIG-specific privacy mechanism.

The standing question after D137: TIG's substrate-algebra didn't
materially improve HSKA empirically.  One unexplored avenue: the
qutrit QEC stack (D102-D116) -- specifically the [[6,1]]_3 code on
the 4-core attractor (D116) and the depth-3 ML decoder.

This module tests whether QEC-encoding the SENSITIVE attribute (the
one thing HSKA leaves unprotected) gives:
  (a) Lower MIA accuracy (because the encoded sensitive is no longer
      a deterministic linkage signal)
  (b) Preserved AGGREGATE utility (the population marginal recoverable
      via majority decoding)
  (c) Stronger ATTRIBUTE protection at lower per-row utility cost

The mechanism, call it **QEC-HSKA**:

  1. HSKA protects the QID columns (RGD + k-anon, as in D137)
  2. Each row's sensitive y_i is encoded as a 3-symbol REPETITION
     code over the 4-core alphabet {VOID, HARMONY, BREATH, RESET}
     = {0, 7, 8, 9}:
       y = 0 (e.g. '<=50K') -> (VOID, VOID, VOID)
       y = 1 (e.g. '>50K') -> (HARMONY, HARMONY, HARMONY)
     For c > 2 classes, each class gets its own 4-core symbol.
  3. Each symbol is independently replaced with a uniformly-random
     4-core symbol with probability q (the "code noise level")
  4. Released: (priv-QID from HSKA, noisy-3-tuple encoding sensitive)
  5. Legitimate analyst decodes via majority vote over the 3 symbols
  6. Attacker has access to the same release but no privileged
     decoder access (in this benchmark, attackers see the released
     data and can run the same majority-vote decoder)

The key claim under test: even though attacker and analyst run the
SAME decoder, the per-symbol noise injects RANDOMNESS into the
released sensitive that breaks MIA's deterministic-linkage signal.
This is the difference from HSKA: the released sensitive is no
longer exactly equal to orig sensitive even for member pairs.

The QEC framing makes the noise tolerance explicit: for repetition
code (3,1), the decoder corrects any single error.  Per-row decode
accuracy at noise rate q (binary symbol flips, treating wrong-4-core
selection as a "flip"):

  P(decode correct) = (1-q)^3 + 3*q*(1-q)^2 = 1 - 3q^2 + 2q^3

For q = 0.3: P(correct) = 0.784 -- about 78% per-row accuracy.
For q = 0.5: P(correct) = 0.500 -- no signal (random noise).

Aggregate utility: population fraction of y=1 is recoverable to
within O(1/sqrt(N)) precision under noise q < 0.5.

TIG-specific structural property: the encoding alphabet IS the
4-core {V,H,Br,R}, which is:
  - the dynamical attractor (WP115 Theorem 2.1)
  - closed under BHML composition
  - the canonical Pati-Salam 3+1 frame (D130)

Whether THIS structural choice matters empirically (vs. encoding
into any 4-element alphabet) is the same question as the D134 4-core
ablation answered for QIDs: probably not.  But it makes the mechanism
TIG-flavored by construction.

Copyright (c) 2026 Brayden Ross Sanders / 7SiTe LLC.
"""
from __future__ import annotations

import os
import random
import sys
from collections import Counter
from typing import List, Optional, Tuple

HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)

import bench_rgd_vs_dp_kanon as bm


# The 4-core attractor (WP115; also D130 Pati-Salam structural map)
FOUR_CORE_ALPHABET = ['V', 'H', 'Br', 'R']  # = 0, 7, 8, 9


def encode_sensitive(value: str, class_to_symbol: dict, repetitions: int = 3) -> List[str]:
    """Encode a sensitive value as a repetition code over the 4-core."""
    sym = class_to_symbol.get(value, FOUR_CORE_ALPHABET[0])
    return [sym] * repetitions


def add_qec_noise(
    encoded: List[str],
    q: float,
    rng: random.Random,
    alphabet: List[str] = FOUR_CORE_ALPHABET,
) -> List[str]:
    """Apply per-symbol Bernoulli noise: with probability q, replace
    each symbol with a uniformly-random OTHER symbol from alphabet."""
    out = []
    for sym in encoded:
        if rng.random() < q:
            choices = [s for s in alphabet if s != sym]
            out.append(rng.choice(choices))
        else:
            out.append(sym)
    return out


def majority_decode(encoded: List[str], symbol_to_class: dict) -> str:
    """Majority vote decoder.  Ties broken by lowest-index class."""
    counts = Counter(encoded)
    # Sort by count desc, then by class index for tiebreak
    sorted_syms = sorted(
        counts.items(),
        key=lambda x: (-x[1], FOUR_CORE_ALPHABET.index(x[0]) if x[0] in FOUR_CORE_ALPHABET else 99),
    )
    if not sorted_syms:
        return next(iter(symbol_to_class.values()))
    best_sym, _ = sorted_syms[0]
    return symbol_to_class.get(best_sym, next(iter(symbol_to_class.values())))


def qec_hska(
    rows: List[List[str]],
    rgd_depth: int = 2,
    kanon_k: int = 25,
    qec_noise: float = 0.0,
    repetitions: int = 3,
    rng: Optional[random.Random] = None,
) -> Tuple[List[List[str]], dict, dict]:
    """
    QEC-Encoded HSKA mechanism.

    Returns:
        priv_rows: list of [QID_cols..., encoded_sensitive_str]
            where encoded_sensitive_str is a comma-joined repetition-code
            tuple, e.g. "V,V,H" (one out of 3 flipped)
        class_to_symbol: dict mapping orig sensitive class -> 4-core symbol
        symbol_to_class: inverse dict (for decoding)
    """
    if rng is None:
        rng = random.Random(2026)
    if not rows:
        return rows, {}, {}

    # Identify sensitive classes and assign each to a 4-core symbol
    sens_classes = sorted({r[-1] for r in rows})
    if len(sens_classes) > len(FOUR_CORE_ALPHABET):
        raise ValueError(
            f"QEC-HSKA repetition code supports up to {len(FOUR_CORE_ALPHABET)} "
            f"classes; got {len(sens_classes)}.  Use a larger code for more classes."
        )
    class_to_symbol = dict(zip(sens_classes, FOUR_CORE_ALPHABET))
    symbol_to_class = {v: k for k, v in class_to_symbol.items()}

    # Apply HSKA to QIDs only
    priv_with_orig_sens = bm.kanon_tabular(bm.rgd_tabular(rows, rgd_depth), kanon_k)

    # Encode each row's sensitive (the priv has same length as orig,
    # rows are aligned)
    priv = []
    for r in priv_with_orig_sens:
        orig_sens = r[-1]
        encoded = encode_sensitive(orig_sens, class_to_symbol, repetitions)
        noisy = add_qec_noise(encoded, qec_noise, rng)
        # Store the noisy encoding as a comma-joined string in the
        # sensitive column position
        priv.append(r[:-1] + [",".join(noisy)])
    return priv, class_to_symbol, symbol_to_class


def decode_priv(priv: List[List[str]], symbol_to_class: dict) -> List[str]:
    """Decode each priv row's encoded sensitive via majority vote.
    Returns the list of decoded class labels (one per priv row)."""
    decoded = []
    for r in priv:
        encoded_str = r[-1]
        if not encoded_str or encoded_str == "*":
            decoded.append(next(iter(symbol_to_class.values())))
            continue
        symbols = encoded_str.split(",")
        decoded.append(majority_decode(symbols, symbol_to_class))
    return decoded


# =====================================================================
# Bench wrappers: re-implement attacker / utility for the encoded-sensitive form
# =====================================================================
def attacker_tabular_qec(orig: List[List[str]], priv: List[List[str]],
                         symbol_to_class: dict) -> float:
    """k-anon-style re-identification rate.  Uses the DECODED sensitive
    for compatibility with the standard attacker function."""
    decoded = decode_priv(priv, symbol_to_class)
    # Build a priv copy with decoded sensitive
    priv_decoded = [r[:-1] + [d] for r, d in zip(priv, decoded)]
    return bm.attacker_tabular(orig, priv_decoded)


def utility_tabular_qec(orig: List[List[str]], priv: List[List[str]],
                        symbol_to_class: dict) -> float:
    """Population-marginal utility: decode each priv row's sensitive,
    compute the fraction of orig rows correctly predicted via decoded
    priv-group majority."""
    decoded = decode_priv(priv, symbol_to_class)
    priv_decoded = [r[:-1] + [d] for r, d in zip(priv, decoded)]
    return bm.utility_tabular(orig, priv_decoded)


def attribute_disclosure_qec(orig: List[List[str]], priv: List[List[str]],
                              symbol_to_class: dict) -> float:
    """Attribute-disclosure attack: attacker decodes priv, then uses
    standard wildcard-match prediction on the decoded data."""
    from bench_extensions import attribute_disclosure_attacker
    decoded = decode_priv(priv, symbol_to_class)
    priv_decoded = [r[:-1] + [d] for r, d in zip(priv, decoded)]
    return attribute_disclosure_attacker(orig, priv_decoded)


def mia_qec(orig: List[List[str]], priv: List[List[str]],
            symbol_to_class: dict, rng: Optional[random.Random] = None) -> dict:
    """MIA on QEC-HSKA priv.  The MIA classifier sees:
      - per-column orig == priv QID indicator
      - wildcard count in priv-QID
      - encoded-sensitive symbol-by-symbol match indicator
        (the new TIG-specific signal: 3 binary features instead of 1)

    Whether the attacker can recover member/non-member depends on
    whether the noisy 3-symbol encoding still leaks the source row.
    """
    from bench_adversarial import _train_lr, _predict_lr

    if rng is None:
        rng = random.Random(2026)
    if len(orig) != len(priv):
        return {"attack_accuracy": float("nan"), "attack_advantage": float("nan")}

    pairs = list(zip(orig, priv))
    rng.shuffle(pairs)

    def featurize(o_row, p_row):
        feats = []
        m = len(o_row) - 1
        # QID-column matches
        for c in range(m):
            feats.append(1.0 if o_row[c] == p_row[c] else 0.0)
        feats.append(float(sum(1 for v in p_row[:m] if v == "*")))
        # Encoded-sensitive features
        orig_sens = o_row[-1]
        priv_encoded = p_row[-1].split(",") if p_row[-1] else []
        # Symbol-by-symbol match: for each encoded position, does the
        # symbol match the orig's would-be encoding?
        if orig_sens in symbol_to_class.values():
            # orig sens is a class label; can't directly compare to encoded
            class_to_symbol = {v: k for k, v in symbol_to_class.items()}
            expected_sym = class_to_symbol.get(orig_sens)
        else:
            class_to_symbol = {v: k for k, v in symbol_to_class.items()}
            expected_sym = class_to_symbol.get(orig_sens)
        for sym in priv_encoded:
            feats.append(1.0 if sym == expected_sym else 0.0)
        return feats

    n_train_pos = min(1500, len(pairs) // 2)
    train_pairs = pairs[:n_train_pos * 2]
    test_pairs = pairs[n_train_pos * 2:]

    X_train = []
    y_train = []
    for i, (o, p) in enumerate(train_pairs):
        X_train.append(featurize(o, p))
        y_train.append(1)
        j = rng.randrange(len(train_pairs))
        while j == i:
            j = rng.randrange(len(train_pairs))
        _, p_other = train_pairs[j]
        X_train.append(featurize(o, p_other))
        y_train.append(0)

    W = _train_lr(X_train, y_train, n_classes=2, epochs=12)

    correct = 0
    total = 0
    for i, (o, p) in enumerate(test_pairs):
        x_pos = featurize(o, p)
        if _predict_lr(W, x_pos) == 1:
            correct += 1
        total += 1
        if len(test_pairs) > 1:
            j = rng.randrange(len(test_pairs))
            while j == i:
                j = rng.randrange(len(test_pairs))
            _, p_other = test_pairs[j]
            x_neg = featurize(o, p_other)
            if _predict_lr(W, x_neg) == 0:
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
    args = parser.parse_args()

    tabular = bm.load_tabular("bench_data/adult.data")
    rows = tabular[0][:args.max_rows]
    print(f"=== QEC-HSKA benchmark ({len(rows)} Adult rows) ===\n")

    sens = Counter(r[-1] for r in rows)
    baseline = sens.most_common(1)[0][1] / len(rows)
    print(f"Baseline: {baseline:.4f}\n")

    # Plain HSKA reference (no QEC)
    priv_hska = bm.kanon_tabular(bm.rgd_tabular(rows, 2), 25)
    a_reid = bm.attacker_tabular(rows, priv_hska)
    from bench_extensions import attribute_disclosure_attacker
    from bench_adversarial import membership_inference_attack
    a_attr = attribute_disclosure_attacker(rows, priv_hska)
    u = bm.utility_tabular(rows, priv_hska)
    mia = membership_inference_attack(rows, priv_hska, rng=random.Random(7),
                                       n_shadow_per_class=1500, epochs=8)
    print(f"REFERENCE: plain HSKA (no QEC encoding)")
    print(f"  reid={a_reid:.4f}  attr_d={a_attr-baseline:+.4f}  "
          f"MIA={mia['attack_accuracy']:.4f}  util={u:.4f}\n")

    print("=== QEC-HSKA across noise levels q ===")
    print(f"  {'q':>5s}  {'reid':>8s}  {'attr_d':>8s}  {'MIA':>8s}  {'util':>8s}  {'aggregate_marginal_err':>22s}")
    for q in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]:
        rng = random.Random(42)
        priv, c2s, s2c = qec_hska(rows, rgd_depth=2, kanon_k=25, qec_noise=q,
                                    repetitions=3, rng=rng)
        a_reid = attacker_tabular_qec(rows, priv, s2c)
        a_attr = attribute_disclosure_qec(rows, priv, s2c)
        u = utility_tabular_qec(rows, priv, s2c)
        mia = mia_qec(rows, priv, s2c, rng=random.Random(7))
        # Aggregate marginal error: fraction of decoded sensitive that
        # matches the population marginal (decoded class y_maj
        # frequency vs. true)
        decoded = decode_priv(priv, s2c)
        decoded_majority_frac = sum(1 for d in decoded if d == sens.most_common(1)[0][0]) / max(len(decoded), 1)
        agg_err = abs(decoded_majority_frac - baseline)
        print(f"  {q:>5.2f}  {a_reid:>8.4f}  {a_attr-baseline:>+8.4f}  "
              f"{mia['attack_accuracy']:>8.4f}  {u:>8.4f}  {agg_err:>22.4f}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
