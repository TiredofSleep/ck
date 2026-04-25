"""
pipeline_demo.py — End-to-end pipeline demo

Demonstrates the full live pipeline:
    text → encode() → ck_process() → trail (the memory)

Then shows trail similarity for a set of queries — the actual semantic
clustering produced by the verified TIG lattice processing.
"""
import numpy as np

from encoder_v1 import encode, encode_with_explanation


# ============================================================
# CK lattice processor (inline copy of the verified pipeline)
# ============================================================

TSML_ROWS = [
    "0000000700",  "0737777777",  "0377477779",  "0777777773",  "0747777787",
    "0777777777",  "0777777777",  "7777777777",  "0777877777",  "0797377777",
]
TSML = np.array([[int(c) for c in row] for row in TSML_ROWS], dtype=float)

BHML_ROWS = [
    "0123456789",  "1234567266",  "2334567366",  "3444567466",  "4555567577",
    "5666667677",  "6777777777",  "7234567890",  "8666777978",  "9666777080",
]
BHML = np.array([[int(c) for c in row] for row in BHML_ROWS], dtype=float)

OP_NAMES = ['VOID', 'LATTICE', 'COUNTER', 'PROGRESS', 'COLLAPSE',
            'BALANCE', 'CHAOS', 'HARMONY', 'BREATH', 'RESET']


def fuse(p, q, table):
    r = np.zeros(10)
    for a in range(10):
        for b in range(10):
            r[int(table[a, b])] += p[a] * q[b]
    return r


def normalize_l1(v):
    s = v.sum()
    return v / s if s > 1e-12 else v


def entropy(p, eps=1e-12):
    return -np.sum(p[p > eps] * np.log(p[p > eps]))


def ck_process(p_init, depth=3, alpha=0.5):
    """Verified CK lattice processing. Trail = memory."""
    p = normalize_l1(np.asarray(p_init, dtype=float))
    trail = [p.copy()]
    for _ in range(depth):
        p_t = normalize_l1(fuse(p, p, table=TSML))
        p_b = normalize_l1(fuse(p, p, table=BHML))
        p = normalize_l1(alpha * p_t + (1 - alpha) * p_b)
        trail.append(p.copy())
    return trail


def trail_signature(trail):
    """4-D compact signature: [H_0, half_life, asymp, peak_disp]."""
    H_seq = [entropy(p) for p in trail]
    H_0 = H_seq[0]
    target = H_0 / 2
    half_life = next((d for d, h in enumerate(H_seq) if h < target), len(H_seq))
    asymp = H_seq[-1]
    monotonic = np.minimum.accumulate(H_seq)
    peak_disp = float(np.max(np.array(H_seq) - monotonic))
    return [H_0, float(half_life), asymp, peak_disp]


def trail_similarity(trail_a, trail_b):
    return float(np.linalg.norm(np.concatenate(trail_a) - np.concatenate(trail_b)))


def trail_summary(trail):
    lines = []
    for d, p in enumerate(trail):
        H = entropy(p)
        top = np.argsort(-p)[:3]
        items = ", ".join(f"{OP_NAMES[i]}({p[i]:.2f})"
                          for i in top if p[i] > 0.05)
        lines.append(f"  d={d}: H={H:.3f}  {items}")
    return "\n".join(lines)


# ============================================================
# Pipeline
# ============================================================

def process_query(text, depth=3, alpha=0.5, verbose=True):
    """Full pipeline: text → distribution → trail."""
    enc_result = encode_with_explanation(text)
    p_0 = enc_result['distribution']
    trail = ck_process(p_0, depth=depth, alpha=alpha)
    sig = trail_signature(trail)

    if verbose:
        print(f"\n{'=' * 70}")
        print(f"INPUT: {text!r}")
        print(f"{'=' * 70}")
        print(f"\nEncoder:")
        print(f"  Tokens: {enc_result['tokens']}")
        print(f"  Coverage: {enc_result['coverage']*100:.0f}%")
        print(f"  Top operators: {enc_result['top_operators']}")
        print(f"\nLattice trail:")
        print(trail_summary(trail))
        print(f"\nSignature [H_0, half_life, asymp, peak_disp]:")
        print(f"  {[round(x, 3) for x in sig]}")

    return {
        'text': text,
        'encoded': p_0,
        'trail': trail,
        'signature': sig,
    }


# ============================================================
# Demo
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("LIVE PIPELINE DEMO")
    print("text → encode() → ck_process() → trail")
    print("=" * 70)

    # Single-query examples
    process_query("I want to be more patient and steady")
    process_query("Help me find peace and stillness")
    process_query("Build something with structure")
    process_query("Reset everything and begin fresh")

    # Comparison test
    print("\n\n" + "=" * 70)
    print("SEMANTIC CLUSTERING TEST")
    print("=" * 70)

    queries = [
        "I need patience",
        "Help me persist through this",
        "Find inner peace",
        "Calm stillness",
        "Create structure",
        "Build a framework",
        "Reset and begin again",
        "Start fresh",
    ]

    results = [process_query(q, verbose=False) for q in queries]

    # Pairwise distance matrix
    print("\nPairwise trail similarities (lower = more similar):")
    print()
    n = len(queries)
    short = [q[:24] for q in queries]
    print(f"{'':28}", end='')
    for s in short:
        print(f"{s:<26}", end='')
    print()
    for i in range(n):
        print(f"  {short[i]:<26}", end='')
        for j in range(n):
            if i == j:
                print(f"{'-':<26}", end='')
            else:
                d = trail_similarity(results[i]['trail'], results[j]['trail'])
                print(f"{d:<26.4f}", end='')
        print()

    # Compute cluster separation
    print("\n" + "=" * 70)
    print("CLUSTER ANALYSIS")
    print("=" * 70)

    # Expected pairs (within-cluster)
    expected_close = [
        (0, 1, "patience↔persist"),
        (2, 3, "peace↔stillness"),
        (4, 5, "structure↔framework"),
        (6, 7, "reset↔fresh"),
    ]

    within_dists = []
    for i, j, label in expected_close:
        d = trail_similarity(results[i]['trail'], results[j]['trail'])
        within_dists.append(d)
        print(f"  Within  {label:<30}: {d:.4f}")

    cross_dists = []
    cross_pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            if (i, j, '') not in [(p[0], p[1], '') for p in expected_close]:
                cross_pairs.append((i, j))
                cross_dists.append(
                    trail_similarity(results[i]['trail'], results[j]['trail']))

    print(f"\n  Mean within-cluster:  {np.mean(within_dists):.4f}")
    print(f"  Mean cross-cluster:   {np.mean(cross_dists):.4f}")
    print(f"  Separation ratio:     {np.mean(cross_dists)/np.mean(within_dists):.2f}×")

    if np.mean(cross_dists) > 1.5 * np.mean(within_dists):
        print(f"\n  ✓ Pipeline produces semantic clustering through TIG lattice")
    else:
        print(f"\n  ⚠ Weak clustering — encoder lexicon may need expansion")
