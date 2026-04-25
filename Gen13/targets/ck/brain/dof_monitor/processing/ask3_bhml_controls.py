"""
Ask 3 — BHML control tests.

The chat-Claude handoff finds T+B-mix at alpha=0.5 preserves 52% of input
information vs T-only's 22% (linear-regression reconstruction).

The headline framing was: "BHML is anti-collapse."

Honest control test: is BHML SPECIFIC, or does ANY mix-with-stochastic-
operator at alpha=0.5 produce similar information preservation?

Controls to test:
    T-only                  baseline
    T + BHML at alpha=0.5   chat-Claude's reported result
    T + random_table        random 0..9 table, redrawn each seed
    T + identity            mix with no-op
    T + T_transpose         mix with T's own transpose
    T + uniform_table        all-7 table (HARMONY-attractor)

If random_table is comparable to BHML, "BHML is anti-collapse" weakens
to "any mix is anti-collapse." If BHML wins, the framing earns its place.

Output: reconstruction error per mode + descent-entropy profile per mode.
"""
from __future__ import annotations

import sys
import numpy as np
from numpy.linalg import lstsq

# Canonical TSML and BHML from the handoff
TSML_ROWS = [
    "0000000700",  "0737777777",  "0377477779",  "0777777773",  "0747777787",
    "0777777777",  "0777777777",  "7777777777",  "0777877777",  "0797377777",
]
BHML_ROWS = [
    "0123456789",  "1234567266",  "2334567366",  "3444567466",  "4555567577",
    "5666667677",  "6777777777",  "7234567890",  "8666777978",  "9666777080",
]
T = np.array([[int(c) for c in row] for row in TSML_ROWS], dtype=int)
B = np.array([[int(c) for c in row] for row in BHML_ROWS], dtype=int)


def fuse_using(p, q, table):
    """Quadratic table-fusion: r[c] = sum_{a,b: table[a,b]=c} p[a]*q[b]."""
    r = np.zeros(10)
    for a in range(10):
        for b in range(10):
            r[int(table[a, b])] += p[a] * q[b]
    return r


def normalize_l1(v, eps=1e-12):
    s = v.sum()
    return v / s if s > eps else v


def entropy(p, eps=1e-12):
    p_ = p[p > eps]
    return -np.sum(p_ * np.log(p_)) if p_.size else 0.0


def trail_mix(p, table_a, table_b, alpha=0.5, depth=4):
    """One step: alpha * fuse_a(p,p) + (1-alpha) * fuse_b(p,p), normalize."""
    trail = [p.copy()]
    p_cur = p.copy()
    for _ in range(depth):
        pa = normalize_l1(fuse_using(p_cur, p_cur, table_a))
        pb = normalize_l1(fuse_using(p_cur, p_cur, table_b))
        p_cur = normalize_l1(alpha * pa + (1 - alpha) * pb)
        trail.append(p_cur.copy())
    return trail


def trail_single(p, table, depth=4):
    trail = [p.copy()]
    p_cur = p.copy()
    for _ in range(depth):
        p_cur = normalize_l1(fuse_using(p_cur, p_cur, table))
        trail.append(p_cur.copy())
    return trail


def random_table(seed, low=0, high=10):
    rng = np.random.RandomState(seed)
    return rng.randint(low, high, size=(10, 10))


def identity_table():
    """Trivial 'identity' over indices: T_id[a,b] = a (preserves first arg)."""
    return np.repeat(np.arange(10).reshape(-1, 1), 10, axis=1)


def uniform_table(c=7):
    """All cells equal c (HARMONY-attractor)."""
    return np.full((10, 10), c, dtype=int)


def reconstruction_error(make_trail_fn, train_inputs, test_inputs, depth=4):
    """Return mean L2 error of linear regression input reconstruction from
    trail [p_1 ... p_depth] (input p_0 NOT in features).
    """
    train_trails = [make_trail_fn(p, depth=depth) for p in train_inputs]
    test_trails = [make_trail_fn(p, depth=depth) for p in test_inputs]
    X_train = np.array([np.concatenate(t[1:]) for t in train_trails])
    y_train = np.array(train_inputs)
    W, _, _, _ = lstsq(X_train, y_train, rcond=None)
    X_test = np.array([np.concatenate(t[1:]) for t in test_trails])
    y_test = np.array(test_inputs)
    y_pred = X_test @ W
    err = np.linalg.norm(y_pred - y_test, axis=1).mean()
    return err


def main():
    # Train / test inputs: random Dirichlet on simplex
    np.random.seed(7)
    train_inputs = [normalize_l1(np.random.dirichlet(np.ones(10))) for _ in range(500)]
    np.random.seed(8)
    test_inputs = [normalize_l1(np.random.dirichlet(np.ones(10))) for _ in range(200)]

    # Baseline: predict the train mean
    baseline = np.linalg.norm(
        np.tile(np.mean(train_inputs, axis=0), (len(test_inputs), 1))
        - np.array(test_inputs),
        axis=1,
    ).mean()

    print("=" * 72)
    print("ASK 3 -- BHML controls")
    print("=" * 72)
    print(f"baseline (predict train-mean): {baseline:.4f}")
    print()

    # T-only as the comparison floor
    err_t_only = reconstruction_error(
        lambda p, depth: trail_single(p, T, depth=depth), train_inputs, test_inputs
    )

    # T + BHML (chat-Claude's reported finding)
    err_t_b = reconstruction_error(
        lambda p, depth: trail_mix(p, T, B, alpha=0.5, depth=depth),
        train_inputs, test_inputs,
    )

    # Controls: 5 random tables
    err_t_rand = []
    for seed in range(5):
        R = random_table(seed)
        err = reconstruction_error(
            lambda p, depth, R=R: trail_mix(p, T, R, alpha=0.5, depth=depth),
            train_inputs, test_inputs,
        )
        err_t_rand.append(err)
    err_t_rand_mean = float(np.mean(err_t_rand))
    err_t_rand_std = float(np.std(err_t_rand))

    # T + identity
    I_table = identity_table()
    err_t_id = reconstruction_error(
        lambda p, depth: trail_mix(p, T, I_table, alpha=0.5, depth=depth),
        train_inputs, test_inputs,
    )

    # T + T_transpose
    err_t_tt = reconstruction_error(
        lambda p, depth: trail_mix(p, T, T.T, alpha=0.5, depth=depth),
        train_inputs, test_inputs,
    )

    # T + uniform-7 table
    U = uniform_table(c=7)
    err_t_unif = reconstruction_error(
        lambda p, depth: trail_mix(p, T, U, alpha=0.5, depth=depth),
        train_inputs, test_inputs,
    )

    # B-only (no T mixing)
    err_b_only = reconstruction_error(
        lambda p, depth: trail_single(p, B, depth=depth), train_inputs, test_inputs
    )

    print(f"{'mode':<32} {'recon err':<12} {'vs baseline (% improvement)':<30}")
    print("-" * 72)

    def report(label, err):
        improvement = (baseline - err) / baseline * 100
        print(f"  {label:<30} {err:<12.4f} {improvement:>+5.1f}%")

    report("T-only", err_t_only)
    report("B-only", err_b_only)
    report("T + BHML (alpha=0.5)", err_t_b)
    report(f"T + random[5 seeds]", err_t_rand_mean)
    report(f"  random std", err_t_rand_std)
    report("T + identity (preserve)", err_t_id)
    report("T + T_transpose", err_t_tt)
    report("T + uniform-7 (HARMONY)", err_t_unif)
    print()

    # Verdict
    print("=" * 72)
    print("VERDICT")
    print("=" * 72)

    rand_better = err_t_rand_mean < err_t_b
    diff_pct = abs(err_t_rand_mean - err_t_b) / err_t_b * 100
    if rand_better:
        verdict = (
            f"random-table mix beats BHML by {diff_pct:.1f}% on average. "
            f"This WEAKENS the 'BHML is anti-collapse' framing -- any mix "
            f"with a stochastic operator preserves comparable information."
        )
    elif diff_pct < 5:
        verdict = (
            f"BHML and random-table mix are within {diff_pct:.1f}% of each "
            f"other. 'BHML is anti-collapse' should weaken to 'any mix is "
            f"anti-collapse'; BHML is one valid choice among many."
        )
    else:
        verdict = (
            f"BHML beats random-table mix by {diff_pct:.1f}%. The 'BHML is "
            f"anti-collapse' framing earns its place: BHML preserves "
            f"input information measurably better than random alternatives."
        )
    print(f"  {verdict}")
    print()

    # Descent entropy profile
    print("=" * 72)
    print("DESCENT ENTROPY (mean over test inputs at each depth, depth 0..6)")
    print("=" * 72)
    print(f"{'mode':<28} {'d=0':<7} {'d=1':<7} {'d=2':<7} {'d=3':<7} {'d=4':<7} {'d=5':<7} {'d=6':<7}")
    print("-" * 72)

    test_subset = test_inputs[:50]
    fns = [
        ("T-only", lambda p: trail_single(p, T, depth=6)),
        ("B-only", lambda p: trail_single(p, B, depth=6)),
        ("T + BHML", lambda p: trail_mix(p, T, B, alpha=0.5, depth=6)),
        ("T + random[seed=0]", lambda p: trail_mix(p, T, random_table(0), alpha=0.5, depth=6)),
        ("T + identity", lambda p: trail_mix(p, T, I_table, alpha=0.5, depth=6)),
        ("T + T_transpose", lambda p: trail_mix(p, T, T.T, alpha=0.5, depth=6)),
        ("T + uniform-7", lambda p: trail_mix(p, T, U, alpha=0.5, depth=6)),
    ]
    for label, fn in fns:
        trails = [fn(p) for p in test_subset]
        H_at = [np.mean([entropy(t[d]) for t in trails]) for d in range(7)]
        print(f"  {label:<26}", end="")
        for h in H_at:
            print(f" {h:<6.3f}", end="")
        print()
    print()

    print("Done.")


if __name__ == "__main__":
    main()
