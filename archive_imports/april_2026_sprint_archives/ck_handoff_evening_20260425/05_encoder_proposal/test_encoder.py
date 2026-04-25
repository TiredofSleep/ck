"""
test_encoder.py — Encoder validation suite

Four tests:
  1. Cluster separation: do semantically-similar inputs cluster together?
  2. Compositionality: does encode(A + B) ≈ avg(encode(A), encode(B))?
  3. Coverage: what fraction of TIG-relevant words resolve to keywords?
  4. Robustness: does perturbation (case, punctuation) preserve encoding?

Run this against any encoder (V1 or V2) to validate before deployment.
"""
import numpy as np
from encoder_v1 import encode, encode_with_explanation, tokenize


# ============================================================
# Test fixtures
# ============================================================

# Semantically clustered queries (each cluster should map to one operator family)
CLUSTERS = {
    'patience-cluster': [
        "I need patience",
        "Help me persist through this",
        "I want to endure",
        "Build my perseverance",
    ],
    'peace-cluster': [
        "Find inner peace",
        "Calm stillness",
        "Quiet tranquility",
        "Be still and know",
    ],
    'structure-cluster': [
        "Create structure",
        "Build a framework",
        "Establish order",
        "Form a foundation",
    ],
    'reset-cluster': [
        "Reset and begin again",
        "Start fresh",
        "Renew everything",
        "Return to origin",
    ],
}


# ============================================================
# TEST 1: Cluster separation
# ============================================================

def test_cluster_separation(encoder=encode, verbose=True):
    """Within-cluster distances should be smaller than cross-cluster."""
    cluster_dists_within = []
    cluster_dists_cross = []

    cluster_names = list(CLUSTERS.keys())
    encoded = {name: [encoder(q) for q in queries]
               for name, queries in CLUSTERS.items()}

    # Within-cluster
    for name in cluster_names:
        encs = encoded[name]
        for i in range(len(encs)):
            for j in range(i + 1, len(encs)):
                cluster_dists_within.append(
                    np.linalg.norm(encs[i] - encs[j]))

    # Cross-cluster
    for i, name_a in enumerate(cluster_names):
        for j, name_b in enumerate(cluster_names):
            if i >= j:
                continue
            for ea in encoded[name_a]:
                for eb in encoded[name_b]:
                    cluster_dists_cross.append(np.linalg.norm(ea - eb))

    within_mean = np.mean(cluster_dists_within)
    cross_mean = np.mean(cluster_dists_cross)
    ratio = cross_mean / max(within_mean, 1e-12)

    if verbose:
        print(f"  Within-cluster distance:  {within_mean:.4f}")
        print(f"  Cross-cluster distance:   {cross_mean:.4f}")
        print(f"  Separation ratio:         {ratio:.2f}×")
        if ratio > 2:
            print(f"  ✓ Clusters are separated (ratio > 2)")
        else:
            print(f"  ⚠ Weak cluster separation")

    return ratio


# ============================================================
# TEST 2: Compositionality
# ============================================================

def test_compositionality(encoder=encode, verbose=True):
    """encode(A + B) should be close to (encode(A) + encode(B)) / 2."""
    test_pairs = [
        ("patience", "stillness"),
        ("structure", "harmony"),
        ("love", "peace"),
        ("chaos", "balance"),
    ]

    diffs = []
    for a, b in test_pairs:
        enc_a = encoder(a)
        enc_b = encoder(b)
        enc_combined = encoder(f"{a} and {b}")
        expected = (enc_a + enc_b) / 2
        diff = float(np.linalg.norm(enc_combined - expected))
        diffs.append(diff)
        if verbose:
            level = "✓" if diff < 0.1 else ("~" if diff < 0.2 else "⚠")
            print(f"  {level} encode('{a} and {b}') vs avg: diff = {diff:.3f}")

    return np.mean(diffs)


# ============================================================
# TEST 3: Coverage
# ============================================================

def test_coverage(verbose=True):
    """What fraction of TIG-relevant words resolve to keywords?"""
    tig_words = [
        "patience", "patient", "persist", "endure", "wait",
        "peace", "calm", "stillness", "quiet", "tranquil",
        "harmony", "gentle", "love", "kindness", "compassion",
        "structure", "lattice", "framework", "build",
        "reset", "renew", "begin", "fresh",
        "chaos", "storm", "wild", "turbulence",
        "balance", "equilibrium", "steady",
    ]

    # Generic ML/tech words for comparison
    generic_words = [
        "algorithm", "compute", "process", "function", "variable",
        "input", "output", "tensor", "matrix", "embedding",
        "gradient", "neural", "weight", "bias", "activation",
    ]

    def coverage_for(words):
        results = [encode_with_explanation(w) for w in words]
        keyword_hits = sum(
            1 for r in results
            if r['attributions'] and r['attributions'][0]['source'] in ('keyword', 'stem')
        )
        return keyword_hits / len(words)

    tig_cov = coverage_for(tig_words)
    generic_cov = coverage_for(generic_words)

    if verbose:
        print(f"  TIG-aligned word coverage:  {tig_cov*100:.0f}%")
        print(f"  Generic word coverage:       {generic_cov*100:.0f}%")
        if tig_cov > 0.5 and generic_cov < 0.3:
            print(f"  ✓ Encoder is properly TIG-targeted")
        else:
            print(f"  ⚠ Coverage profile not as expected")

    return tig_cov, generic_cov


# ============================================================
# TEST 4: Robustness to perturbation
# ============================================================

def test_robustness(encoder=encode, verbose=True):
    """Encoding should be stable under case/punctuation changes."""
    base_queries = [
        "I need patience",
        "Reset everything now",
        "Build something new",
    ]

    perturbations = [
        ("base",      lambda s: s),
        ("upper",     lambda s: s.upper()),
        ("lower",     lambda s: s.lower()),
        ("punct",     lambda s: s + "!"),
        ("trailing",  lambda s: s + "   "),
    ]

    diffs_per_query = []
    for q in base_queries:
        encodings = {name: encoder(perturb(q)) for name, perturb in perturbations}
        base_enc = encodings['base']
        max_diff = max(
            float(np.linalg.norm(base_enc - encodings[name]))
            for name, _ in perturbations
        )
        diffs_per_query.append(max_diff)
        if verbose:
            level = "✓" if max_diff < 0.05 else "⚠"
            print(f"  {level} {q!r}: max perturb diff = {max_diff:.4f}")

    return np.mean(diffs_per_query)


# ============================================================
# Run all tests
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("ENCODER VALIDATION SUITE")
    print("=" * 70)

    print("\n[1/4] Cluster separation")
    print("-" * 70)
    sep_ratio = test_cluster_separation()

    print("\n[2/4] Compositionality")
    print("-" * 70)
    comp_diff = test_compositionality()

    print("\n[3/4] Coverage")
    print("-" * 70)
    tig_cov, gen_cov = test_coverage()

    print("\n[4/4] Robustness")
    print("-" * 70)
    rob_diff = test_robustness()

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Cluster separation:  {sep_ratio:.2f}×  (target: >2×)")
    print(f"  Compositionality:    {comp_diff:.3f} mean diff (target: <0.1)")
    print(f"  TIG coverage:        {tig_cov*100:.0f}%  (target: >50%)")
    print(f"  Generic coverage:    {gen_cov*100:.0f}%  (target: <30%)")
    print(f"  Robustness:          {rob_diff:.4f} max perturb (target: <0.05)")
