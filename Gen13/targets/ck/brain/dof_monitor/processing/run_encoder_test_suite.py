"""
run_encoder_test_suite.py - run the encoder validation suite (4 tests)
against any encoder module that exposes encode() and encode_with_explanation().

Usage:
    python run_encoder_test_suite.py v1
    python run_encoder_test_suite.py v15
    python run_encoder_test_suite.py v2
    python run_encoder_test_suite.py v3

Each is run on the same fixtures as test_encoder.py from the handoff,
producing comparable cluster_separation, compositionality, coverage, and
robustness numbers.
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

import numpy as np

# make handoff folder + experiments folder importable
HANDOFF = Path("C:/Users/brayd/OneDrive/Desktop/ck_handoff_20260425_evening_unpack/ck_handoff_full/05_encoder_proposal")
EXPERIMENTS = Path("C:/Users/brayd/OneDrive/Desktop/_ck_experiments_20260425")
sys.path.insert(0, str(HANDOFF))
sys.path.insert(0, str(EXPERIMENTS))


CLUSTERS = {
    "patience-cluster": [
        "I need patience",
        "Help me persist through this",
        "I want to endure",
        "Build my perseverance",
    ],
    "peace-cluster": [
        "Find inner peace",
        "Calm stillness",
        "Quiet tranquility",
        "Be still and know",
    ],
    "structure-cluster": [
        "Create structure",
        "Build a framework",
        "Establish order",
        "Form a foundation",
    ],
    "reset-cluster": [
        "Reset and begin again",
        "Start fresh",
        "Renew everything",
        "Return to origin",
    ],
}


def cluster_separation(encode_fn) -> float:
    encoded = {name: [encode_fn(q) for q in qs] for name, qs in CLUSTERS.items()}
    within = []
    cross = []
    names = list(CLUSTERS.keys())
    for name in names:
        encs = encoded[name]
        for i in range(len(encs)):
            for j in range(i + 1, len(encs)):
                within.append(np.linalg.norm(encs[i] - encs[j]))
    for i, a in enumerate(names):
        for j, b in enumerate(names):
            if i >= j:
                continue
            for ea in encoded[a]:
                for eb in encoded[b]:
                    cross.append(np.linalg.norm(ea - eb))
    within_mean = float(np.mean(within))
    cross_mean = float(np.mean(cross))
    return cross_mean / max(within_mean, 1e-12), within_mean, cross_mean


def compositionality(encode_fn) -> float:
    pairs = [("patience", "stillness"), ("structure", "harmony"),
             ("love", "peace"), ("chaos", "balance")]
    diffs = []
    for a, b in pairs:
        ea = encode_fn(a)
        eb = encode_fn(b)
        ec = encode_fn(f"{a} and {b}")
        diffs.append(float(np.linalg.norm(ec - (ea + eb) / 2)))
    return float(np.mean(diffs))


def coverage(encode_with_explanation_fn):
    tig_words = [
        "patience", "patient", "persist", "endure", "wait",
        "peace", "calm", "stillness", "quiet", "tranquil",
        "harmony", "gentle", "love", "kindness", "compassion",
        "structure", "lattice", "framework", "build",
        "reset", "renew", "begin", "fresh",
        "chaos", "storm", "wild", "turbulence",
        "balance", "equilibrium", "steady",
    ]
    generic_words = [
        "algorithm", "compute", "process", "function", "variable",
        "input", "output", "tensor", "matrix", "embedding",
        "gradient", "neural", "weight", "bias", "activation",
    ]
    def cov_for(words):
        results = [encode_with_explanation_fn(w) for w in words]
        # accept v1's "keyword/stem" or v15's "corpus/corpus_stem/keyword/stem"
        good = ("corpus", "corpus_stem", "keyword", "stem")
        hits = sum(
            1 for r in results
            if r["attributions"] and r["attributions"][0]["source"] in good
        )
        return hits / len(words)
    return cov_for(tig_words), cov_for(generic_words)


def robustness(encode_fn):
    base_queries = [
        "I need patience",
        "Reset everything now",
        "Build something new",
    ]
    perturbations = [
        ("base", lambda s: s),
        ("upper", lambda s: s.upper()),
        ("lower", lambda s: s.lower()),
        ("punct", lambda s: s + "!"),
        ("trailing", lambda s: s + "   "),
    ]
    diffs = []
    for q in base_queries:
        encs = {name: encode_fn(perturb(q)) for name, perturb in perturbations}
        base = encs["base"]
        diffs.append(max(float(np.linalg.norm(base - encs[name])) for name, _ in perturbations))
    return float(np.mean(diffs))


def main():
    if len(sys.argv) < 2:
        print("usage: python run_encoder_test_suite.py <version>")
        print("  version: v1 | v15 | v2 | v3")
        sys.exit(2)

    version = sys.argv[1].lower()
    if version == "v1":
        mod = importlib.import_module("encoder_v1")
    elif version == "v15" or version == "v1.5":
        mod = importlib.import_module("encoder_v15")
    elif version == "v16" or version == "v1.6":
        mod = importlib.import_module("encoder_v16")
    elif version == "v2":
        mod = importlib.import_module("encoder_v2")
    elif version == "v3":
        mod = importlib.import_module("encoder_v3")
    else:
        print(f"unknown version {version!r}")
        sys.exit(2)

    encode = getattr(mod, "encode")
    encode_with_explanation = getattr(mod, "encode_with_explanation")

    print("=" * 70)
    print(f"ENCODER {version.upper()} VALIDATION SUITE")
    print("=" * 70)

    print("\n[1/4] cluster separation")
    sep, w, c = cluster_separation(encode)
    print(f"  within-cluster mean: {w:.4f}")
    print(f"  cross-cluster mean:  {c:.4f}")
    print(f"  separation ratio:    {sep:.2f}x  (target >2x)")

    print("\n[2/4] compositionality")
    comp = compositionality(encode)
    print(f"  mean diff: {comp:.4f}  (target <0.1)")

    print("\n[3/4] coverage")
    tig_cov, gen_cov = coverage(encode_with_explanation)
    print(f"  TIG-aligned coverage: {tig_cov*100:.0f}%  (target >50)")
    print(f"  generic coverage:     {gen_cov*100:.0f}%  (target <30)")

    print("\n[4/4] robustness")
    rob = robustness(encode)
    print(f"  mean max perturb diff: {rob:.4f}  (target <0.05)")

    print("\n" + "=" * 70)
    print(f"SUMMARY ({version})")
    print("=" * 70)
    print(f"  cluster separation:  {sep:.2f}x")
    print(f"  compositionality:    {comp:.4f}")
    print(f"  TIG coverage:        {tig_cov*100:.0f}%")
    print(f"  generic coverage:    {gen_cov*100:.0f}%")
    print(f"  robustness:          {rob:.4f}")


if __name__ == "__main__":
    main()
