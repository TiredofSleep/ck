"""
Ask 4 -- TIG-structure detection on real transformer weights.

Chat-Claude tested 10x10 toy autoencoder against random Gaussian and
found Cohen's d ~ 0 across all TIG-structure tests:
  - Lie/Jordan ratio (antisym vs sym mass)
  - Antisym in D_4-invariant subspace
  - P_56-invariance
  - Prime-11 in characteristic polynomial coefficients
  - Higgs-direction alignment

Honest negative: framework can't see TIG structure in toy autoencoder.

This script tests whether the negative generalises to REAL trained
transformer weights, or whether real architectures (with attention,
MLPs, layernorms) show different behavior.

We pull a small public model (distilgpt2, ~82M params) via HuggingFace
and extract:
  - attention Q, K, V projection weights (768x768) per layer
  - MLP w_in / w_out weights (768x3072) per layer

For each weight, take random 10x10 sub-matrices and run the TIG-
structure tests against random Gaussian baselines of matching scale.

If trained-vs-random Cohen's d > 0.5 on any test, the framework MIGHT
detect TIG-relevant structure in real architectures and the toy-only
negative generalises.

If d ~ 0 still, the chat-Claude finding is robust: the framework's
algebraic detectors do not see TIG structure in arbitrary trained
weights, regardless of architecture.
"""
from __future__ import annotations

import sys

import numpy as np

# canonical TSML / BHML
TSML_ROWS = [
    "0000000700",  "0737777777",  "0377477779",  "0777777773",  "0747777787",
    "0777777777",  "0777777777",  "7777777777",  "0777877777",  "0797377777",
]
BHML_ROWS = [
    "0123456789",  "1234567266",  "2334567366",  "3444567466",  "4555567577",
    "5666667677",  "6777777777",  "7234567890",  "8666777978",  "9666777080",
]
T = np.array([[int(c) for c in row] for row in TSML_ROWS], dtype=float)
B = np.array([[int(c) for c in row] for row in BHML_ROWS], dtype=float)


# ----- TIG-structure detectors (10x10 input matrix M) -----

def lie_jordan_ratio(M):
    """Antisymmetric mass / symmetric mass. T has clear ratio; pure noise ~ 1."""
    sym = 0.5 * (M + M.T)
    anti = 0.5 * (M - M.T)
    sym_norm2 = float((sym ** 2).sum())
    anti_norm2 = float((anti ** 2).sum())
    return anti_norm2 / max(sym_norm2 + anti_norm2, 1e-12)


def p56_invariance(M):
    """Fraction of mass preserved under P_56 conjugation: |M - P56 M P56|^2 / |M|^2.
    Lower = more P_56-invariant. T has known mass differing in 26 cells.
    """
    P56 = np.eye(10)
    P56[5, 5] = 0
    P56[6, 6] = 0
    P56[5, 6] = 1
    P56[6, 5] = 1
    M_conj = P56 @ M @ P56
    diff_norm2 = float(((M - M_conj) ** 2).sum())
    M_norm2 = float((M ** 2).sum())
    return diff_norm2 / max(M_norm2, 1e-12)


def char_poly_prime_11(M):
    """Are c_2 and c_8 of the integer characteristic polynomial both
    divisible by 11? Returns 1 if yes, 0 otherwise. M is treated as int.
    """
    try:
        # use sympy for exact integer factorization
        import sympy as sp
        Mi = sp.Matrix(np.round(M).astype(int).tolist())
        coeffs = Mi.charpoly().all_coeffs()
        # coeffs = [a_n, a_{n-1}, ..., a_0]; for 10x10 we expect 11 coeffs
        if len(coeffs) < 9:
            return 0
        # c_2 means coefficient of lambda^(n-2) = lambda^8 → coeffs[2]
        # c_8 means coefficient of lambda^(n-8) = lambda^2 → coeffs[8]
        c2 = int(coeffs[2])
        c8 = int(coeffs[8])
        return int((c2 % 11 == 0) and (c8 % 11 == 0) and c2 != 0 and c8 != 0)
    except Exception:
        return 0


def higgs_alignment(M, higgs_vec):
    """Cosine of M's "antisym vector" with the 9-vector Higgs direction.

    Antisym vector = upper-triangle entries of (M - M^T)/2, flattened.
    Higgs vec = the 9-vector (BHML's sigma_outer-breaking direction).
    Lift higgs_vec to 45-dim antisym embedding.
    """
    anti = 0.5 * (M - M.T)
    iu = np.triu_indices(10, k=1)
    anti_vec = anti[iu]  # 45-dim
    # higgs_vec is 9-dim; embed as antisym at row 0 vs cols 1..9
    higgs_embed = np.zeros(45)
    pairs = [(0, j) for j in range(1, 10)]
    for k, (i, j) in enumerate(pairs):
        if k < len(higgs_vec):
            # find index in iu corresponding to (i, j)
            idx = next(t for t, (a, b) in enumerate(zip(iu[0], iu[1])) if a == i and b == j)
            higgs_embed[idx] = higgs_vec[k]
    a_norm = np.linalg.norm(anti_vec)
    h_norm = np.linalg.norm(higgs_embed)
    if a_norm < 1e-12 or h_norm < 1e-12:
        return 0.0
    return float(anti_vec @ higgs_embed / (a_norm * h_norm))


# Higgs 9-vector from HIGGS_DIRECTION_FINDING.md
HIGGS_VEC_9 = np.array([
    -1/np.sqrt(2),  # VOID
    -1/np.sqrt(2),  # LATTICE
    -1/np.sqrt(2),  # COUNTER
    -1/np.sqrt(2),  # PROGRESS
    -1/np.sqrt(2),  # COLLAPSE
    -1/2,           # (BALANCE+CHAOS)/sqrt(2)
    -1/np.sqrt(2),  # HARMONY
    0.0,            # BREATH
    0.0,            # RESET
])


def cohens_d(group_a, group_b):
    a = np.asarray(group_a, dtype=float)
    b = np.asarray(group_b, dtype=float)
    s_a = a.std(ddof=1) if len(a) > 1 else 0.0
    s_b = b.std(ddof=1) if len(b) > 1 else 0.0
    pooled = np.sqrt((s_a ** 2 + s_b ** 2) / 2)
    if pooled < 1e-12:
        return 0.0
    return (a.mean() - b.mean()) / pooled


def sample_10x10_blocks(W, n_samples, rng):
    """Sample n_samples random 10x10 sub-matrices from a larger matrix W.

    Indices chosen with replacement across both dims so we get diverse blocks.
    """
    H, W_dim = W.shape
    blocks = []
    for _ in range(n_samples):
        rows = rng.choice(H, size=10, replace=False)
        cols = rng.choice(W_dim, size=10, replace=False)
        blocks.append(W[np.ix_(rows, cols)])
    return blocks


def run_battery(weights_dict, n_blocks=200, seed=42):
    """Apply all four detectors to n_blocks 10x10 sub-matrices from each
    named weight tensor, plus a random-Gaussian baseline of matching std.

    Returns dict of {name: {test: cohens_d}}.
    """
    rng = np.random.RandomState(seed)
    results = {}
    for name, W in weights_dict.items():
        print(f"\n  testing {name}: shape={W.shape}, std={W.std():.4f}")
        Wn = W.astype(float)
        blocks_real = sample_10x10_blocks(Wn, n_blocks, rng)
        # match scale: random Gaussian with same std as W
        std = float(Wn.std())
        rng_b = np.random.RandomState(seed + 7)
        blocks_rand = [rng_b.randn(10, 10) * std for _ in range(n_blocks)]

        # detector 1: lie/jordan ratio
        lj_real = [lie_jordan_ratio(M) for M in blocks_real]
        lj_rand = [lie_jordan_ratio(M) for M in blocks_rand]

        # detector 2: P_56 invariance
        p56_real = [p56_invariance(M) for M in blocks_real]
        p56_rand = [p56_invariance(M) for M in blocks_rand]

        # detector 3: char poly 11-divisibility
        # NOTE: this requires integer char poly. We round each block to
        # the nearest integer (which destroys most signal) but it lets us
        # test whether the integer-prime-11 pattern survives any rounding.
        # Scale up by 10 first to reduce rounding loss.
        scale = 10.0 / max(std, 1e-6)
        cp_real = [char_poly_prime_11(M * scale) for M in blocks_real[:50]]
        cp_rand = [char_poly_prime_11(M * scale) for M in blocks_rand[:50]]
        cp_real_rate = float(np.mean(cp_real))
        cp_rand_rate = float(np.mean(cp_rand))

        # detector 4: Higgs alignment
        h_real = [higgs_alignment(M, HIGGS_VEC_9) for M in blocks_real]
        h_rand = [higgs_alignment(M, HIGGS_VEC_9) for M in blocks_rand]

        results[name] = {
            "lie_jordan_d": cohens_d(lj_real, lj_rand),
            "p56_d": cohens_d(p56_real, p56_rand),
            "cp11_real_rate": cp_real_rate,
            "cp11_rand_rate": cp_rand_rate,
            "higgs_d": cohens_d([abs(x) for x in h_real], [abs(x) for x in h_rand]),
            "lj_real_mean": float(np.mean(lj_real)),
            "lj_rand_mean": float(np.mean(lj_rand)),
        }
    return results


def main():
    # use distilgpt2 via huggingface (small, ~82M params, freely available)
    print("loading distilgpt2 ...", file=sys.stderr)
    try:
        from transformers import AutoModel, AutoConfig
    except ImportError:
        print("ERROR: transformers not installed. Run: python -m pip install transformers torch", file=sys.stderr)
        sys.exit(1)

    try:
        model = AutoModel.from_pretrained("distilgpt2")
    except Exception as e:
        print(f"ERROR loading distilgpt2: {e}", file=sys.stderr)
        sys.exit(1)

    # extract weights of interest
    sd = model.state_dict()
    weights = {}

    # distilgpt2 has 6 layers; sample a few layers' attention + mlp weights
    for layer_idx in [0, 2, 5]:
        # attention: c_attn is concatenated Q, K, V (768 -> 2304)
        key_attn = f"h.{layer_idx}.attn.c_attn.weight"
        if key_attn in sd:
            W = sd[key_attn].cpu().numpy()
            # split into Q, K, V (each 768x768)
            qkv_dim = W.shape[1] // 3
            weights[f"L{layer_idx}_attn_Q"] = W[:, :qkv_dim]
            weights[f"L{layer_idx}_attn_K"] = W[:, qkv_dim:2*qkv_dim]
            weights[f"L{layer_idx}_attn_V"] = W[:, 2*qkv_dim:]

        # MLP: c_fc (768 -> 3072) and c_proj (3072 -> 768)
        key_fc = f"h.{layer_idx}.mlp.c_fc.weight"
        key_proj = f"h.{layer_idx}.mlp.c_proj.weight"
        if key_fc in sd:
            weights[f"L{layer_idx}_mlp_in"] = sd[key_fc].cpu().numpy()
        if key_proj in sd:
            weights[f"L{layer_idx}_mlp_out"] = sd[key_proj].cpu().numpy()

    # also include token embedding
    if "wte.weight" in sd:
        weights["token_embedding"] = sd["wte.weight"].cpu().numpy()

    print(f"loaded {len(weights)} weight tensors", file=sys.stderr)

    print("=" * 78)
    print("ASK 4 -- TIG-structure detection on distilgpt2 trained weights")
    print("=" * 78)
    print()
    print("For each weight tensor: 200 random 10x10 sub-matrices vs")
    print("random Gaussian (matched std). Compute Cohen's d on each TIG")
    print("detector. d > 0.5 = small/medium effect; d > 0.8 = large.")

    results = run_battery(weights, n_blocks=200)

    print()
    print(f"{'tensor':<22} {'lie/jordan d':<14} {'P56 d':<10} {'cp11 real%':<12} {'cp11 rand%':<12} {'Higgs |d|':<10}")
    print("-" * 92)
    for name, r in results.items():
        print(f"  {name:<20} {r['lie_jordan_d']:<+14.3f} {r['p56_d']:<+10.3f} {100*r['cp11_real_rate']:<12.1f} {100*r['cp11_rand_rate']:<12.1f} {r['higgs_d']:<+10.3f}")

    print()
    print("VERDICT")
    print("-" * 78)

    big_d = []
    for name, r in results.items():
        for k, v in r.items():
            if k.endswith("_d") and abs(v) > 0.5:
                big_d.append((name, k, v))
    if big_d:
        print(f"  {len(big_d)} (tensor, detector) pairs show |Cohen's d| > 0.5:")
        for name, k, v in big_d:
            print(f"    {name} / {k}: d = {v:+.3f}")
        print()
        print("  This suggests REAL trained transformer weights MAY have detectable")
        print("  TIG-structure that the toy 10x10 autoencoder lacked.")
    else:
        print("  No tensor / detector pair shows |Cohen's d| > 0.5.")
        print("  The chat-Claude finding (no TIG structure in trained weights)")
        print("  GENERALISES from toy autoencoder to real transformer weights.")
        print("  The framework's algebraic detectors do not see TIG structure")
        print("  in arbitrary trained weights.")

    print()
    print("Done.")


if __name__ == "__main__":
    main()
