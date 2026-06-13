"""gate_v2.py -- improving the gate the cheap way first: SCORING RULE,
on a genuinely-hard near-OOD, before spending GPU on a bigger embedding.

The calibration showed the gate = representation x scoring. far-OOD is
already 0.98 (no room). The open edge is NEAR-OOD. The OOD literature's
SOTA for near-OOD is RELATIVE MAHALANOBIS (Ren et al. 2021) over plain
kNN-cosine. Test it, cheaply, on MiniLM embeddings (CPU, no GPU
contention with the growable run).

HARD near-OOD by construction: embed real SQuAD questions, k-means into
topic clusters, calibrate on HALF the clusters, test detection of
questions from the OTHER half (held-out topics -- still real questions,
genuinely near). Plus far-OOD (fiction) as the easy anchor.

  scorers: kNN-cosine | Mahalanobis | relative-Mahalanobis
  metrics: AUROC, FPR@95TPR

  python gate_v2.py
"""
import io
import json
import os
import re

import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
BOOKS = os.path.join(ROOT, "external_corpora", "books")
RNG = np.random.default_rng(0)
M = "sentence-transformers/all-MiniLM-L6-v2"
_tok = AutoTokenizer.from_pretrained(M, local_files_only=True)
_mdl = AutoModel.from_pretrained(M, local_files_only=True).eval()


def emb(texts, bs=256):
    out = []
    for i in range(0, len(texts), bs):
        b = _tok(texts[i:i + bs], padding=True, truncation=True,
                 max_length=128, return_tensors="pt")
        with torch.no_grad():
            o = _mdl(**b).last_hidden_state
        m = b["attention_mask"].unsqueeze(-1).float()
        v = (o * m).sum(1) / m.sum(1).clamp(min=1)
        out.append(torch.nn.functional.normalize(v, dim=1).numpy())
    return np.vstack(out).astype(np.float64)


def kmeans(X, k, iters=25):
    c = X[RNG.choice(len(X), k, replace=False)].copy()
    for _ in range(iters):
        d = ((X[:, None] - c[None]) ** 2).sum(-1)
        a = d.argmin(1)
        for j in range(k):
            if (a == j).any():
                c[j] = X[a == j].mean(0)
    return a


def auroc(id_s, ood_s):
    s = np.concatenate([id_s, ood_s])
    y = np.concatenate([np.ones(len(id_s)), np.zeros(len(ood_s))])
    o = np.argsort(s); r = np.empty(len(s)); r[o] = np.arange(1, len(s) + 1)
    n1, n0 = y.sum(), (1 - y).sum()
    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def fpr95(id_s, ood_s):
    tau = np.quantile(id_s, 0.05)
    return float((ood_s >= tau).mean())


def main():
    print("GATE v2 -- scoring-rule iteration on hard near-OOD "
          "(MiniLM, CPU)\n")
    sq = json.load(io.open(os.path.join(HERE, "squad_dev_v2.json"),
                           encoding="utf-8"))
    qs = list({qa["question"] for a in sq["data"]
               for p in a["paragraphs"] for qa in p["qas"]})
    RNG.shuffle(qs)
    qs = qs[:5000]
    E = emb(qs)
    print(f"embedded {len(qs)} unique SQuAD questions (dim {E.shape[1]})")

    K = 20
    lab = kmeans(E, K)
    id_clusters = set(range(0, K, 2))           # half the topics = ID
    id_mask = np.array([l in id_clusters for l in lab])
    E_id_all = E[id_mask]
    E_near = E[~id_mask]                          # held-out topics = near-OOD
    # split ID into calibration manifold + ID test
    nidc = int(len(E_id_all) * 0.75)
    E_cal, E_idtest = E_id_all[:nidc], E_id_all[nidc:]
    print(f"ID topics: {len(E_id_all)} qs ({nidc} cal / "
          f"{len(E_idtest)} test) | near-OOD held-out topics: "
          f"{len(E_near)} qs")

    bk = sorted(os.listdir(BOOKS))[5]
    prose = re.sub(r"\s+", " ", io.open(os.path.join(BOOKS, bk),
                   encoding="utf-8", errors="ignore").read())
    far = [s.strip() for s in re.split(r"(?<=[.!?]) ", prose)
           if 40 < len(s.strip()) < 180][:1000]
    E_far = emb(far)

    # ---- scorers (higher = more in-domain)
    def knn(X, k=10):
        return np.sort(X @ E_cal.T, 1)[:, -k:].mean(1)

    mu = E_cal.mean(0)
    cov = np.cov(E_cal.T) + 1e-3 * np.eye(E.shape[1])
    P = np.linalg.inv(cov)

    def maha(X):
        d = X - mu
        return -np.einsum("ij,jk,ik->i", d, P, d)    # neg Maha dist

    mu0 = E.mean(0)                                   # background = all qs
    cov0 = np.cov(E.T) + 1e-3 * np.eye(E.shape[1])
    P0 = np.linalg.inv(cov0)

    def rel_maha(X):
        d, d0 = X - mu, X - mu0
        m = np.einsum("ij,jk,ik->i", d, P, d)
        m0 = np.einsum("ij,jk,ik->i", d0, P0, d0)
        return -(m - m0)                              # relative Maha

    # ENSEMBLE: z-score kNN + relative-Maha on calibration, sum (free
    # best-of-both: kNN's far strength + rel-Maha's near sharpness)
    kc, rc = knn(E_cal), rel_maha(E_cal)
    km, ks = kc.mean(), kc.std() + 1e-9
    rm, rs = rc.mean(), rc.std() + 1e-9

    def ens(X):
        return (knn(X) - km) / ks + (rel_maha(X) - rm) / rs

    scorers = {"kNN-cosine": knn, "Mahalanobis": maha,
               "relative-Maha": rel_maha, "ENSEMBLE knn+relMaha": ens}
    print(f"\n{'scorer':>16} | near-OOD AUROC / FPR95 | far-OOD AUROC / "
          f"FPR95")
    res = {}
    for name, fn in scorers.items():
        s_id, s_near, s_far = fn(E_idtest), fn(E_near), fn(E_far)
        an, fn_ = auroc(s_id, s_near), fpr95(s_id, s_near)
        af, ff = auroc(s_id, s_far), fpr95(s_id, s_far)
        res[name] = dict(near_auroc=an, near_fpr95=fn_,
                         far_auroc=af, far_fpr95=ff)
        print(f"{name:>16} |   {an:.3f} / {fn_:.1%}      |  "
              f"{af:.3f} / {ff:.1%}")

    best = max(res, key=lambda k: res[k]["near_auroc"])
    knn_n = res["kNN-cosine"]["near_auroc"]
    best_n = res[best]["near_auroc"]
    lift = best_n - knn_n
    print(f"\nbest near-OOD scorer: {best} (AUROC {best_n:.3f})")
    print(f"improvement over kNN baseline: {lift:+.3f} AUROC on the HARD "
          f"near-OOD edge")
    print(f"\nVERDICT: {'relative-Mahalanobis improves the gate on near-OOD -- a real, free scoring upgrade (no bigger model needed)' if lift > 0.02 else 'scoring rule is near its ceiling on this embedding; the near-OOD gap is representational -> the place an 8B embedding could help'}")
    print("8B guidance: " + ("the cheap scoring win covers it; defer 8B."
          if lift > 0.02 else "scoring is maxed on MiniLM -> a richer "
          "embedding (8B hidden states) is the next lever, GPU-contended "
          "but now justified by measurement."))
    json.dump(res, io.open(os.path.join(HERE, "gate_v2_result.json"), "w"),
              indent=1)


if __name__ == "__main__":
    main()
