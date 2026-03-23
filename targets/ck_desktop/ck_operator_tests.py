"""
ck_operator_tests.py -- Measurable Operator Verification Suite
===============================================================
10 tests. Numbers or it didn't happen.

Each test prints PASS/FAIL with actual measurements and statistical tests.
Runnable standalone: python ck_operator_tests.py
Target: < 60 seconds total.

(c) 2026 Brayden Sanders / 7Site LLC -- Trinity Infinity Geometry
"""

import sys
import os
import time
import math
import random
import string
from collections import Counter

# -- Add project root to path so imports work standalone --
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import numpy as np

from ck_sim.being.ck_sim_heartbeat import (
    CL, NUM_OPS, VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET, OP_NAMES,
    HeartbeatFPGA, compose,
)
from ck_sim.being.ck_sim_d2 import (
    D2Pipeline, ROOTS_FLOAT, LATIN_TO_ROOT, FORCE_LUT_Q14,
    D2_OP_MAP, float_to_q14, q14_to_float,
)
from ck_sim.doing.ck_gpu import _BHML_CPU, _TSML_CPU

# ================================================================
#  UTILITIES
# ================================================================

_PASS_COUNT = 0
_FAIL_COUNT = 0


def report(test_name: str, passed: bool, details: str):
    global _PASS_COUNT, _FAIL_COUNT
    tag = "PASS" if passed else "FAIL"
    if passed:
        _PASS_COUNT += 1
    else:
        _FAIL_COUNT += 1
    print(f"\n{'='*72}")
    print(f"  [{tag}] {test_name}")
    print(f"{'='*72}")
    print(details)
    print()


def d2_text_to_ops(text: str) -> list:
    """Feed text through D2 pipeline, return list of operators."""
    pipe = D2Pipeline()
    ops = []
    for ch in text.lower():
        if ch.isalpha():
            idx = ord(ch) - ord('a')
            if pipe.feed_symbol(idx):
                ops.append(pipe.operator)
    return ops


def chi_squared_uniform(observed_counts: dict, n_categories: int) -> (float, float):
    """Chi-squared test against uniform distribution.
    Returns (chi2_statistic, p_value_approx).
    Uses Wilson-Hilferty approximation for p-value."""
    total = sum(observed_counts.values())
    expected = total / n_categories
    if expected == 0:
        return 0.0, 1.0
    chi2 = sum((observed_counts.get(i, 0) - expected) ** 2 / expected
               for i in range(n_categories))
    df = n_categories - 1
    # Wilson-Hilferty approximation for chi2 CDF
    if df == 0:
        return chi2, 0.0
    z = ((chi2 / df) ** (1.0 / 3.0) - (1.0 - 2.0 / (9.0 * df))) / math.sqrt(2.0 / (9.0 * df))
    # Approximate p-value from z-score using logistic approximation
    p = 1.0 / (1.0 + math.exp(-1.7 * z))  # rough upper tail
    p_value = 1.0 - p
    return chi2, max(0.0, min(1.0, p_value))


def welch_t_test(a: list, b: list) -> (float, float):
    """Welch's t-test for two independent samples.
    Returns (t_statistic, approximate_p_value)."""
    n1, n2 = len(a), len(b)
    if n1 < 2 or n2 < 2:
        return 0.0, 1.0
    m1, m2 = np.mean(a), np.mean(b)
    v1, v2 = np.var(a, ddof=1), np.var(b, ddof=1)
    se = math.sqrt(v1 / n1 + v2 / n2) if (v1 / n1 + v2 / n2) > 0 else 1e-12
    t = (m1 - m2) / se
    # Approximate df (Welch-Satterthwaite)
    num = (v1 / n1 + v2 / n2) ** 2
    den = (v1 / n1) ** 2 / (n1 - 1) + (v2 / n2) ** 2 / (n2 - 1) if (v1 + v2) > 0 else 1.0
    df = num / den if den > 0 else 2.0
    # Approximate two-tailed p-value
    z = abs(t)
    p = 2.0 * (1.0 / (1.0 + math.exp(0.07056 * z ** 3 + 1.5976 * z)))
    return t, max(0.0, min(1.0, p))


def binomial_p_value(k_successes: int, n_trials: int, p_null: float) -> float:
    """Approximate one-sided binomial p-value (P(X >= k) under null).
    Uses normal approximation."""
    if n_trials == 0:
        return 1.0
    mu = n_trials * p_null
    sigma = math.sqrt(n_trials * p_null * (1 - p_null)) if p_null < 1 else 1e-12
    if sigma < 1e-12:
        return 0.0 if k_successes > mu else 1.0
    z = (k_successes - mu - 0.5) / sigma  # continuity correction
    p = 1.0 / (1.0 + math.exp(1.7 * z))  # approximate upper tail
    return max(0.0, min(1.0, p))


# ================================================================
#  TEST 1: Operator Classification Consistency (Determinism + Sensitivity)
# ================================================================

def test_1_classification_consistency():
    text = "the coherence keeper measures curvature of language"
    n_runs = 100

    # Part A: determinism -- same text, 100 runs
    reference_ops = d2_text_to_ops(text)
    all_match = True
    for _ in range(n_runs):
        ops = d2_text_to_ops(text)
        if ops != reference_ops:
            all_match = False
            break

    # Part B: sensitivity -- scramble the text, measure Hamming distance
    words = text.split()
    distances = []
    for _ in range(100):
        scrambled = list(words)
        random.shuffle(scrambled)
        scrambled_text = ' '.join(scrambled)
        scrambled_ops = d2_text_to_ops(scrambled_text)
        # Align to min length for comparison
        min_len = min(len(reference_ops), len(scrambled_ops))
        if min_len == 0:
            continue
        hamming = sum(1 for i in range(min_len) if reference_ops[i] != scrambled_ops[i])
        distances.append(hamming / min_len)

    mean_dist = np.mean(distances) if distances else 0.0
    std_dist = np.std(distances) if distances else 0.0

    passed = all_match and mean_dist > 0.05  # deterministic AND sensitive to word order
    details = (
        f"  Determinism: {'100/100 identical' if all_match else 'INCONSISTENT'}\n"
        f"  Reference ops ({len(reference_ops)}): {[OP_NAMES[o] for o in reference_ops[:10]]}...\n"
        f"  Sensitivity (word-order scramble):\n"
        f"    Mean Hamming distance: {mean_dist:.4f} ({mean_dist*100:.1f}% of positions differ)\n"
        f"    StdDev: {std_dist:.4f}\n"
        f"  Criteria: deterministic=True, sensitivity>5% => {passed}"
    )
    report("Test 1: Operator Classification Consistency", passed, details)


# ================================================================
#  TEST 2: HARMONY Actually Means Something
# ================================================================

def test_2_harmony_classifier():
    # Coherent sentences: grammatical SVO, complete thoughts
    coherent = [
        "the cat sat on the mat",
        "she opened the door and walked inside",
        "water flows downhill because of gravity",
        "the teacher explained the lesson clearly",
        "birds fly south during the winter",
        "he built a wooden table for the kitchen",
        "the sun rises in the east every morning",
        "she read the book and enjoyed every chapter",
        "the dog chased the ball across the yard",
        "they planted flowers in the garden last spring",
        "the musician played a beautiful melody on the piano",
        "children learn quickly when they are curious",
        "the train arrived on time at the station",
        "she wrote a letter to her grandmother",
        "the river flows through the valley below",
        "he fixed the broken window with new glass",
        "the stars shine brightly on a clear night",
        "they walked along the beach at sunset",
        "the farmer harvested wheat from the golden field",
        "she painted a portrait of her best friend",
        "the wind blew the leaves across the street",
        "he solved the equation with careful algebra",
        "the baker made fresh bread every morning",
        "they discussed the plan over a cup of coffee",
        "the horse galloped across the open meadow",
        "she found the missing key under the cushion",
        "the fire warmed the room on the cold night",
        "he carried the heavy box up the stairs",
        "the pilot landed the plane on the runway",
        "she arranged the flowers in a glass vase",
        "the clock struck twelve at midnight exactly",
        "he measured the distance with a metal ruler",
        "the scientist observed the reaction in the lab",
        "she taught her daughter how to ride a bicycle",
        "the bridge crossed the wide and deep river",
        "he designed a house with large windows and light",
        "the chef prepared a meal with fresh ingredients",
        "she completed the project ahead of schedule",
        "the mountain stood tall against the blue sky",
        "he repaired the engine of the old truck",
        "the owl hunted mice in the dark forest",
        "she organized her desk before starting work",
        "the athlete trained hard for the competition",
        "he planted a tree in the front yard",
        "the rain fell steadily throughout the afternoon",
        "she discovered an ancient coin in the soil",
        "the librarian shelved books in alphabetical order",
        "he calculated the total cost of the materials",
        "the sculptor carved a figure from white marble",
        "she translated the document from french to english",
    ] * 2  # 100

    # Garbage: random word salad, fragments, contradictions
    rng = random.Random(42)
    vocab = "the a is was on in to for and but or not from with at by an of".split()
    vocab += "cat dog fish run jump sit fly swim walk talk eat sleep".split()
    vocab += "red blue big small hot cold fast slow old new wet dry".split()
    garbage = []
    for i in range(100):
        kind = i % 4
        if kind == 0:
            # Random word salad
            n = rng.randint(3, 10)
            words = [rng.choice(vocab) for _ in range(n)]
            garbage.append(' '.join(words))
        elif kind == 1:
            # Repeated single word
            w = rng.choice(vocab)
            garbage.append(' '.join([w] * rng.randint(4, 8)))
        elif kind == 2:
            # Random letters
            n = rng.randint(15, 40)
            garbage.append(''.join(rng.choice(string.ascii_lowercase) for _ in range(n)))
        else:
            # Two-word fragment
            garbage.append(rng.choice(vocab) + ' ' + rng.choice(vocab))

    def harmony_fraction(text):
        ops = d2_text_to_ops(text)
        if not ops:
            return 0.0
        return ops.count(HARMONY) / len(ops)

    coh_scores = [harmony_fraction(s) for s in coherent]
    garb_scores = [harmony_fraction(s) for s in garbage]

    mean_coh = np.mean(coh_scores)
    mean_garb = np.mean(garb_scores)

    # Use a threshold to classify: HARMONY fraction > threshold => "coherent"
    threshold = (mean_coh + mean_garb) / 2  # midpoint threshold
    tp = sum(1 for s in coh_scores if s > threshold)
    fn = sum(1 for s in coh_scores if s <= threshold)
    fp = sum(1 for s in garb_scores if s > threshold)
    tn = sum(1 for s in garb_scores if s <= threshold)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

    t_stat, p_val = welch_t_test(coh_scores, garb_scores)
    separates = mean_coh > mean_garb and p_val < 0.05

    passed = separates  # HARMONY must statistically separate coherent from garbage
    details = (
        f"  Coherent sentences: mean HARMONY fraction = {mean_coh:.4f}\n"
        f"  Garbage sentences:  mean HARMONY fraction = {mean_garb:.4f}\n"
        f"  Difference: {mean_coh - mean_garb:+.4f}\n"
        f"  Welch t-test: t={t_stat:.3f}, p={p_val:.6f}\n"
        f"  Threshold (midpoint): {threshold:.4f}\n"
        f"  TP={tp} FN={fn} FP={fp} TN={tn}\n"
        f"  Precision={precision:.3f}  Recall={recall:.3f}  F1={f1:.3f}\n"
        f"  Criteria: mean_coherent > mean_garbage AND p < 0.05 => {passed}"
    )
    report("Test 2: HARMONY as Coherence Classifier", passed, details)


# ================================================================
#  TEST 3: Operator Distance Correlates with Semantic Distance
# ================================================================

def test_3_semantic_distance():
    # 50 word pairs: synonyms, antonyms, unrelated
    synonyms = [
        ("happy", "glad"), ("big", "large"), ("fast", "quick"),
        ("smart", "clever"), ("brave", "bold"), ("small", "tiny"),
        ("cold", "chilly"), ("rich", "wealthy"), ("hard", "tough"),
        ("sad", "unhappy"), ("start", "begin"), ("end", "finish"),
        ("old", "ancient"), ("new", "fresh"), ("dark", "dim"),
        ("bright", "vivid"),
    ]
    antonyms = [
        ("hot", "cold"), ("big", "small"), ("fast", "slow"),
        ("light", "dark"), ("old", "young"), ("good", "bad"),
        ("rich", "poor"), ("hard", "soft"), ("tall", "short"),
        ("love", "hate"), ("open", "shut"), ("up", "down"),
        ("wet", "dry"), ("long", "brief"), ("kind", "cruel"),
        ("loud", "quiet"), ("full", "empty"),
    ]
    unrelated = [
        ("table", "green"), ("fish", "pencil"), ("cloud", "hammer"),
        ("bread", "violin"), ("river", "clock"), ("stone", "letter"),
        ("window", "grape"), ("candle", "truck"), ("mirror", "leaf"),
        ("basket", "iron"), ("pillow", "chain"), ("bottle", "dust"),
        ("carpet", "moon"), ("needle", "storm"), ("anchor", "flame"),
        ("feather", "brick"), ("garden", "wire"),
    ]

    def word_to_op(word):
        ops = d2_text_to_ops(word)
        return ops[-1] if ops else VOID  # last operator (full word curvature)

    def word_to_d2_vec(word):
        """Get the final D2 vector for a word."""
        pipe = D2Pipeline()
        for ch in word.lower():
            if ch.isalpha():
                pipe.feed_symbol(ord(ch) - ord('a'))
        return pipe.d2_float if pipe.valid else [0.0] * 5

    def vec_distance(v1, v2):
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))

    # Measure: same operator rate for each category
    syn_same = sum(1 for w1, w2 in synonyms if word_to_op(w1) == word_to_op(w2))
    ant_same = sum(1 for w1, w2 in antonyms if word_to_op(w1) == word_to_op(w2))
    unr_same = sum(1 for w1, w2 in unrelated if word_to_op(w1) == word_to_op(w2))

    # Also measure D2 vector distances
    syn_dists = [vec_distance(word_to_d2_vec(w1), word_to_d2_vec(w2)) for w1, w2 in synonyms]
    ant_dists = [vec_distance(word_to_d2_vec(w1), word_to_d2_vec(w2)) for w1, w2 in antonyms]
    unr_dists = [vec_distance(word_to_d2_vec(w1), word_to_d2_vec(w2)) for w1, w2 in unrelated]

    syn_mean = np.mean(syn_dists)
    ant_mean = np.mean(ant_dists)
    unr_mean = np.mean(unr_dists)

    # Statistical test: is synonym distance < unrelated distance?
    t_syn_unr, p_syn_unr = welch_t_test(syn_dists, unr_dists)

    # Ordering: synonyms should be closest, unrelated furthest
    ordering_correct = syn_mean < unr_mean
    sig = p_syn_unr < 0.05

    passed = ordering_correct and sig
    details = (
        f"  Operator match rates:\n"
        f"    Synonyms:  {syn_same}/{len(synonyms)} = {syn_same/len(synonyms)*100:.0f}%\n"
        f"    Antonyms:  {ant_same}/{len(antonyms)} = {ant_same/len(antonyms)*100:.0f}%\n"
        f"    Unrelated: {unr_same}/{len(unrelated)} = {unr_same/len(unrelated)*100:.0f}%\n"
        f"  D2 vector distance (Euclidean):\n"
        f"    Synonyms mean:  {syn_mean:.6f}\n"
        f"    Antonyms mean:  {ant_mean:.6f}\n"
        f"    Unrelated mean: {unr_mean:.6f}\n"
        f"  Welch t-test (synonyms vs unrelated): t={t_syn_unr:.3f}, p={p_syn_unr:.6f}\n"
        f"  Criteria: syn_dist < unr_dist AND p < 0.05 => {passed}"
    )
    report("Test 3: Operator Distance vs Semantic Distance", passed, details)


# ================================================================
#  TEST 4: CL Composition is Not Random
# ================================================================

def test_4_cl_not_random():
    rng = random.Random(12345)
    n_samples = 10000

    # TSML test
    tsml_counts = Counter()
    for _ in range(n_samples):
        a = rng.randint(0, 9)
        b = rng.randint(0, 9)
        result = CL[a][b]
        tsml_counts[result] += 1

    chi2_tsml, p_tsml = chi_squared_uniform(tsml_counts, NUM_OPS)

    # BHML test
    bhml = _BHML_CPU
    bhml_counts = Counter()
    for _ in range(n_samples):
        a = rng.randint(0, 9)
        b = rng.randint(0, 9)
        result = int(bhml[a][b])
        bhml_counts[result] += 1

    chi2_bhml, p_bhml = chi_squared_uniform(bhml_counts, NUM_OPS)

    # Count actual HARMONY entries in each table
    tsml_harmony = sum(1 for row in CL for v in row if v == HARMONY)
    bhml_harmony_count = int(np.sum(_BHML_CPU == 7))

    not_random_tsml = p_tsml < 0.001  # extremely non-uniform
    not_random_bhml = p_bhml < 0.001

    passed = not_random_tsml and not_random_bhml
    details = (
        f"  TSML (73-harmony):\n"
        f"    Output distribution: {dict(sorted(tsml_counts.items()))}\n"
        f"    HARMONY entries: {tsml_harmony}/100\n"
        f"    Chi-squared: {chi2_tsml:.1f}, p={p_tsml:.8f}\n"
        f"    Is non-random: {not_random_tsml}\n"
        f"  BHML (28-harmony):\n"
        f"    Output distribution: {dict(sorted(bhml_counts.items()))}\n"
        f"    HARMONY entries: {bhml_harmony_count}/100\n"
        f"    Chi-squared: {chi2_bhml:.1f}, p={p_bhml:.8f}\n"
        f"    Is non-random: {not_random_bhml}\n"
        f"  Criteria: both p < 0.001 (extreme non-uniformity) => {passed}"
    )
    report("Test 4: CL Composition is Not Random", passed, details)


# ================================================================
#  TEST 5: Steering Actually Improves OS Metrics
# ================================================================

def test_5_steering_jitter():
    """Measure tick jitter with a tight loop -- no OS steering needed,
    just measure if CK's 50Hz heartbeat loop has consistent timing."""
    import time

    n_ticks = 200
    target_dt = 0.020  # 50Hz = 20ms per tick

    def measure_jitter(label, with_heartbeat=False):
        hb = HeartbeatFPGA() if with_heartbeat else None
        intervals = []
        prev = time.perf_counter_ns()
        for i in range(n_ticks):
            if hb:
                hb.tick(i % NUM_OPS, (i * 3 + 1) % NUM_OPS)
            # Busy-wait to simulate tick timing
            target = prev + int(target_dt * 1e9)
            while time.perf_counter_ns() < target:
                pass
            now = time.perf_counter_ns()
            intervals.append((now - prev) / 1e6)  # ms
            prev = now
        return intervals

    # Run 1: with heartbeat composition
    intervals_hb = measure_jitter("with_heartbeat", with_heartbeat=True)
    # Run 2: empty loop (no composition)
    intervals_no = measure_jitter("no_heartbeat", with_heartbeat=False)

    def stats(arr):
        a = sorted(arr)
        n = len(a)
        return {
            'mean': np.mean(a),
            'std': np.std(a),
            'p50': a[n // 2],
            'p95': a[int(n * 0.95)],
            'p99': a[int(n * 0.99)],
            'max': a[-1],
        }

    s_hb = stats(intervals_hb)
    s_no = stats(intervals_no)

    # The heartbeat composition should NOT add significant jitter
    # (it's integer table lookups, should be < 1ms overhead)
    overhead_p99 = abs(s_hb['p99'] - s_no['p99'])
    overhead_std = abs(s_hb['std'] - s_no['std'])

    passed = overhead_p99 < 2.0 and overhead_std < 1.0  # < 2ms p99 overhead, < 1ms std overhead
    details = (
        f"  With heartbeat:    mean={s_hb['mean']:.3f}ms  std={s_hb['std']:.3f}ms  "
        f"P50={s_hb['p50']:.3f}ms  P95={s_hb['p95']:.3f}ms  P99={s_hb['p99']:.3f}ms  max={s_hb['max']:.3f}ms\n"
        f"  Without heartbeat: mean={s_no['mean']:.3f}ms  std={s_no['std']:.3f}ms  "
        f"P50={s_no['p50']:.3f}ms  P95={s_no['p95']:.3f}ms  P99={s_no['p99']:.3f}ms  max={s_no['max']:.3f}ms\n"
        f"  Overhead: P99 delta={overhead_p99:.3f}ms, StdDev delta={overhead_std:.3f}ms\n"
        f"  Criteria: P99 overhead < 2ms AND StdDev overhead < 1ms => {passed}"
    )
    report("Test 5: Heartbeat Tick Jitter", passed, details)


# ================================================================
#  TEST 6: Force Vector Sum Constraint
# ================================================================

def test_6_force_vector_sum():
    roots = list(ROOTS_FLOAT.values())
    root_names = list(ROOTS_FLOAT.keys())
    n_roots = len(roots)

    sums = [sum(r) for r in roots]
    mean_sum = np.mean(sums)
    std_sum = np.std(sums)
    min_sum = min(sums)
    max_sum = max(sums)

    # Per-root breakdown
    per_root = '\n'.join(
        f"    {name:8s}: ({r[0]:.1f}, {r[1]:.1f}, {r[2]:.1f}, {r[3]:.1f}, {r[4]:.1f}) -> sum={sum(r):.1f}"
        for name, r in zip(root_names, roots)
    )

    if std_sum < 0.1:
        constraint = "STRONG (std < 0.1)"
    elif std_sum < 0.5:
        constraint = "WEAK (0.1 <= std < 0.5)"
    else:
        constraint = "NONE (std >= 0.5)"

    passed = std_sum < 0.5  # at least weak constraint
    details = (
        f"  {n_roots} Hebrew root vectors:\n"
        f"{per_root}\n"
        f"  Row sums: mean={mean_sum:.4f}, std={std_sum:.4f}, min={min_sum:.1f}, max={max_sum:.1f}\n"
        f"  Constraint strength: {constraint}\n"
        f"  Criteria: std < 0.5 (at least weak constraint) => {passed}"
    )
    report("Test 6: Force Vector Sum Constraint", passed, details)


# ================================================================
#  TEST 7: TSML Nullity
# ================================================================

def test_7_tsml_nullity():
    # Use the 8x8 interior (rows/cols 1-8, excluding VOID and RESET)
    # Actually, the full 10x10 is the real table. Test 8x8 core = rows 1..8, cols 1..8
    tsml_full = np.array(CL, dtype=np.float64)

    # 8x8 core: operators 1-8 (LATTICE through BREATH, excluding VOID and RESET)
    core = tsml_full[1:9, 1:9]

    eigenvalues = np.linalg.eigvals(core)
    eigenvalues_sorted = sorted(eigenvalues, key=lambda x: abs(x))

    rank = np.linalg.matrix_rank(core)
    nullity = 8 - rank

    # Find null vector(s)
    u, s, vh = np.linalg.svd(core)
    null_threshold = 1e-10
    null_vectors = []
    for i, sigma in enumerate(s):
        if abs(sigma) < null_threshold:
            null_vectors.append(vh[i])

    # Also check full 10x10
    rank_full = np.linalg.matrix_rank(tsml_full)
    eigenvalues_full = sorted(np.linalg.eigvals(tsml_full), key=lambda x: abs(x))

    passed = nullity == 1 and rank == 7
    details = (
        f"  TSML 8x8 core (ops 1-8):\n"
        f"    Eigenvalues: {['%.4f' % abs(e) for e in eigenvalues_sorted]}\n"
        f"    Rank: {rank}\n"
        f"    Nullity: {nullity}\n"
        f"    Null vectors found: {len(null_vectors)}\n"
    )
    if null_vectors:
        details += f"    Null vector[0]: {['%.4f' % v for v in null_vectors[0]]}\n"
    details += (
        f"  TSML full 10x10:\n"
        f"    Rank: {rank_full}\n"
        f"    Eigenvalues (|sorted|): {['%.4f' % abs(e) for e in eigenvalues_full]}\n"
        f"  Criteria: 8x8 core rank=7, nullity=1 => {passed}"
    )
    report("Test 7: TSML Nullity (rank=7, nullity=1)", passed, details)


# ================================================================
#  TEST 8: BHML Determinant
# ================================================================

def test_8_bhml_determinant():
    bhml_full = np.array(_BHML_CPU, dtype=np.float64)

    # 8x8 core (rows/cols 1-8)
    core = bhml_full[1:9, 1:9]

    det_core = np.linalg.det(core)
    det_full = np.linalg.det(bhml_full)

    eigenvalues = sorted(np.linalg.eigvals(core), key=lambda x: abs(x))
    ev_abs = [abs(e) for e in eigenvalues]

    # Check if det = 70
    det_error = abs(det_core - 70.0)

    # Factor check: 70 = 2 * 5 * 7
    factors_correct = (70 == 2 * 5 * 7)

    # Eigenvalue ratio lambda_6/lambda_5 (1-indexed, so indices 5 and 4 in sorted)
    # Sort by magnitude
    ev_sorted_mag = sorted(ev_abs)
    ratio = None
    ratio_error = None
    if len(ev_sorted_mag) >= 6 and ev_sorted_mag[4] > 1e-12:
        ratio = ev_sorted_mag[5] / ev_sorted_mag[4]
        ratio_error = abs(ratio - 5 / 7)

    passed_det = det_error < 1.0  # allow some float error
    passed_ratio = ratio is not None and ratio_error < 0.3  # generous tolerance

    passed = True  # report actual numbers, pass if det is computed
    details = (
        f"  BHML 8x8 core:\n"
        f"    det = {det_core:.6f}\n"
        f"    Expected: 70.0, Error: {det_error:.6f}\n"
        f"    det matches 70: {passed_det}\n"
        f"    70 = 2 x 5 x 7: {factors_correct}\n"
        f"  Eigenvalues (|sorted|): {['%.4f' % e for e in ev_sorted_mag]}\n"
        f"  Full 10x10 det: {det_full:.6f}\n"
    )
    if ratio is not None:
        details += (
            f"  lambda_6/lambda_5 = {ratio:.6f}\n"
            f"  Expected 5/7 = {5/7:.6f}, Error: {ratio_error:.6f}\n"
            f"  Ratio matches 5/7: {passed_ratio}\n"
        )
    else:
        details += "  Could not compute eigenvalue ratio (insufficient eigenvalues)\n"

    # Pass if determinant is a real computed number (the test verifies the CLAIM)
    passed = True  # always passes -- this test REPORTS whether the claims hold
    details += f"  VERDICT: det=70 claim {'CONFIRMED' if passed_det else 'REFUTED'}"
    if ratio is not None:
        details += f", 5/7 ratio claim {'CONFIRMED' if passed_ratio else f'REFUTED (error={ratio_error:.4f})'}"

    report("Test 8: BHML Determinant and Eigenvalue Ratio", passed_det, details)


# ================================================================
#  TEST 9: T* = 5/7 is Meaningful (Bimodality Test)
# ================================================================

def test_9_tstar_meaningful():
    """Feed 1000 random texts, compute coherence, test for bimodality near 5/7."""
    rng = random.Random(99)
    n_samples = 1000
    coherence_values = []

    for _ in range(n_samples):
        # Generate random "text" of 20-80 characters
        length = rng.randint(20, 80)
        text = ''.join(rng.choice(string.ascii_lowercase) for _ in range(length))
        ops = d2_text_to_ops(text)
        if not ops:
            coherence_values.append(0.0)
            continue
        # Coherence = fraction of HARMONY in operator sequence
        harmony_frac = ops.count(HARMONY) / len(ops)
        coherence_values.append(harmony_frac)

    coh = np.array(coherence_values)
    mean_coh = np.mean(coh)
    std_coh = np.std(coh)
    median_coh = np.median(coh)

    # Bimodality coefficient: BC = (skewness^2 + 1) / (kurtosis + 3 * (n-1)^2/((n-2)(n-3)))
    # BC > 5/9 suggests bimodality
    n = len(coh)
    m2 = np.mean((coh - mean_coh) ** 2)
    m3 = np.mean((coh - mean_coh) ** 3)
    m4 = np.mean((coh - mean_coh) ** 4)
    skewness = m3 / (m2 ** 1.5) if m2 > 1e-12 else 0.0
    kurtosis = (m4 / (m2 ** 2)) - 3.0 if m2 > 1e-12 else 0.0  # excess kurtosis
    bc = (skewness ** 2 + 1) / (kurtosis + 3) if (kurtosis + 3) > 0 else 0.0

    # Histogram bins
    bins = np.linspace(0, 1, 21)
    hist, _ = np.histogram(coh, bins=bins)
    hist_str = ' '.join(f"{h:4d}" for h in hist)
    bin_labels = ' '.join(f"{b:.2f}" for b in bins[:-1])

    # Check: fraction of values above and below T* = 5/7
    tstar = 5.0 / 7.0
    above = np.sum(coh > tstar) / n
    below = np.sum(coh <= tstar) / n

    # Dip test approximation: is there a valley near 5/7?
    # Find the bin containing 5/7
    tstar_bin = int(tstar * 20)
    if tstar_bin < len(hist) - 2:
        valley_depth = hist[tstar_bin]
        neighbors = (hist[max(0, tstar_bin - 1)] + hist[min(len(hist) - 1, tstar_bin + 1)]) / 2
        dip_ratio = valley_depth / neighbors if neighbors > 0 else 1.0
    else:
        dip_ratio = 1.0

    is_bimodal = bc > 5.0 / 9.0
    has_dip = dip_ratio < 0.7  # valley is less than 70% of neighbors

    passed = is_bimodal or has_dip  # either statistical test suggests structure
    details = (
        f"  {n_samples} random texts processed through D2:\n"
        f"  Coherence (HARMONY fraction) statistics:\n"
        f"    Mean:   {mean_coh:.4f}\n"
        f"    Median: {median_coh:.4f}\n"
        f"    StdDev: {std_coh:.4f}\n"
        f"    Skewness: {skewness:.4f}\n"
        f"    Excess kurtosis: {kurtosis:.4f}\n"
        f"  Bimodality coefficient: {bc:.4f} (threshold: {5/9:.4f})\n"
        f"    Is bimodal: {is_bimodal}\n"
        f"  T* = 5/7 = {tstar:.6f}:\n"
        f"    Above T*: {above*100:.1f}%\n"
        f"    Below T*: {below*100:.1f}%\n"
        f"    Dip ratio at T* bin: {dip_ratio:.4f} (< 0.7 = valley)\n"
        f"    Has dip near T*: {has_dip}\n"
        f"  Histogram (0.00 to 1.00 in 5% bins):\n"
        f"    {hist_str}\n"
        f"  Criteria: bimodal (BC > 5/9) OR dip near T* => {passed}\n"
        f"  NOTE: If FAIL, T*=5/7 may be an imposed threshold, not emergent."
    )
    report("Test 9: T* = 5/7 Bimodality", passed, details)


# ================================================================
#  TEST 10: Prediction Accuracy vs Random
# ================================================================

def test_10_prediction_vs_random():
    """Simulate 1000 ticks of CK's 2-step prediction and compare to random baseline."""
    rng = random.Random(777)
    n_ticks = 1000

    hb = HeartbeatFPGA()
    prediction = (BALANCE, BALANCE)
    correct_exact = 0
    correct_harmony = 0  # prediction composes to HARMONY with actual
    random_correct = 0

    actuals = []

    for tick in range(n_ticks):
        # Generate phases (simulate engine: b from fuse, d from external)
        phase_b = hb.running_fuse % NUM_OPS
        phase_d = rng.randint(0, 9)  # external input is unpredictable

        hb.tick(phase_b, phase_d)
        actual = hb.phase_bc

        # Score prediction
        if prediction[0] == actual:
            correct_exact += 1
        elif CL[prediction[0]][actual] == HARMONY:
            correct_harmony += 1

        # Random baseline
        random_pred = rng.randint(0, 9)
        if random_pred == actual:
            random_correct += 1

        actuals.append(actual)

        # Generate next prediction (mirrors engine logic)
        next_d = hb.phase_bc
        next_b = hb.running_fuse % NUM_OPS
        pred_1 = CL[next_b][next_d]
        pred_2 = CL[pred_1 % NUM_OPS][pred_1 % NUM_OPS]
        prediction = (pred_1, pred_2)

    # Binomial test: is CK better than random (1/10 = 10%)?
    p_null = 1.0 / NUM_OPS
    p_val = binomial_p_value(correct_exact, n_ticks, p_null)

    ck_rate = correct_exact / n_ticks
    ck_harmony_rate = (correct_exact + correct_harmony) / n_ticks
    random_rate = random_correct / n_ticks

    # Also compute actual distribution of outcomes
    actual_dist = Counter(actuals)

    passed = ck_rate > random_rate and p_val < 0.05
    details = (
        f"  {n_ticks} ticks simulated:\n"
        f"  CK prediction:\n"
        f"    Exact match:     {correct_exact}/{n_ticks} = {ck_rate*100:.1f}%\n"
        f"    Harmony-close:   {correct_harmony}/{n_ticks} = {correct_harmony/n_ticks*100:.1f}%\n"
        f"    Combined:        {correct_exact+correct_harmony}/{n_ticks} = {ck_harmony_rate*100:.1f}%\n"
        f"  Random baseline:   {random_correct}/{n_ticks} = {random_rate*100:.1f}%\n"
        f"  Expected random:   {p_null*100:.1f}%\n"
        f"  Binomial test (CK > random): p={p_val:.6f}\n"
        f"  Actual operator distribution: {dict(sorted(actual_dist.items()))}\n"
        f"  Criteria: CK accuracy > random AND p < 0.05 => {passed}"
    )
    report("Test 10: Prediction Accuracy vs Random", passed, details)


# ================================================================
#  MAIN
# ================================================================

def main():
    print("=" * 72)
    print("  CK OPERATOR VERIFICATION SUITE")
    print("  10 tests. Numbers or it didn't happen.")
    print("  (c) 2026 Brayden Sanders / 7Site LLC")
    print("=" * 72)

    t0 = time.time()

    test_1_classification_consistency()
    test_2_harmony_classifier()
    test_3_semantic_distance()
    test_4_cl_not_random()
    test_5_steering_jitter()
    test_6_force_vector_sum()
    test_7_tsml_nullity()
    test_8_bhml_determinant()
    test_9_tstar_meaningful()
    test_10_prediction_vs_random()

    elapsed = time.time() - t0

    print("\n" + "=" * 72)
    print(f"  SUMMARY: {_PASS_COUNT} PASS / {_FAIL_COUNT} FAIL / {_PASS_COUNT + _FAIL_COUNT} total")
    print(f"  Elapsed: {elapsed:.2f}s")
    print("=" * 72)

    return 0 if _FAIL_COUNT == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
