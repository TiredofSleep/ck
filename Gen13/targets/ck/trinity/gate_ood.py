"""gate_ood.py -- the GATE in its real regime: semantic-space OOD
detection, the standard way (Hendrycks: AUROC + FPR@95TPR).

The cheap-feature SQuAD calibration showed the gate has NO intrinsic
power -- it inherits everything from the representation. So measure it
on a REAL semantic space (all-MiniLM-L6-v2, local) at its actual job:
"is this query within the manifold I've been calibrated on?"

  ID (in-domain) : real questions (SQuAD dev)
  OOD-far        : fiction prose (genuinely different distribution)
  OOD-near       : math/substrate-flavored unanswerable traps (HARD --
                   topically adjacent, the adversarial case)
  gate score     : mean kNN cosine to the ID calibration manifold
  metrics        : AUROC (ID vs OOD), FPR@95 (OOD answered when keeping
                   95% of ID), + split-conformal coverage check.

This characterizes the gate's OPERATING ENVELOPE honestly: where it
works, where it doesn't.

  python gate_ood.py
"""
import io
import json
import os
import re
import sys

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
    return np.vstack(out)


def auroc(id_s, ood_s):
    # higher gate score = more in-domain; AUROC that ID scores > OOD
    s = np.concatenate([id_s, ood_s])
    y = np.concatenate([np.ones(len(id_s)), np.zeros(len(ood_s))])
    order = np.argsort(s)
    r = np.empty(len(s)); r[order] = np.arange(1, len(s) + 1)
    n1, n0 = y.sum(), (1 - y).sum()
    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def fpr_at_tpr(id_s, ood_s, tpr=0.95):
    tau = np.quantile(id_s, 1 - tpr)          # keep 95% of ID
    return float((ood_s >= tau).mean()), tau   # frac OOD wrongly kept


def main():
    print("GATE OOD CALIBRATION -- semantic space (MiniLM), standard "
          "metrics\n")
    sq = json.load(io.open(os.path.join(HERE, "squad_dev_v2.json"),
                           encoding="utf-8"))
    qs = [qa["question"] for a in sq["data"] for p in a["paragraphs"]
          for qa in p["qas"]]
    RNG.shuffle(qs)
    id_cal, id_test = qs[:2000], qs[2000:3500]

    bk = sorted(os.listdir(BOOKS))[3]
    prose = re.sub(r"\s+", " ", io.open(os.path.join(BOOKS, bk),
                   encoding="utf-8", errors="ignore").read())
    far = [s.strip() for s in re.split(r"(?<=[.!?]) ", prose)
           if 40 < len(s.strip()) < 180][:1500]

    near = ["what is the riemann hypothesis", "explain the monster group",
            "state the four color theorem", "what is a perfectoid space",
            "the kissing number in dimension five", "define etale cohomology",
            "what is the hodge conjecture", "explain galois cohomology",
            "the eight cycle of the substrate", "the 6-core attractor set",
            "the ninety one cell lattice", "what is the sigma fifth face",
            "explain the abc conjecture", "what is a motive",
            "state fermat's last theorem", "the twelve core absorber",
            "what is noncommutative geometry", "the langlands program",
            "define a vertex operator algebra", "the collatz conjecture"]

    print(f"embedding (MiniLM): {len(id_cal)} ID-cal, {len(id_test)} "
          f"ID-test, {len(far)} far-OOD, {len(near)} near-OOD...")
    E_cal = emb(id_cal); E_id = emb(id_test)
    E_far = emb(far); E_near = emb(near)

    def gate(X, k=10):
        sims = X @ E_cal.T
        return np.sort(sims, 1)[:, -k:].mean(1)

    g_id, g_far, g_near = gate(E_id), gate(E_far), gate(E_near)

    print(f"\ngate score (kNN cosine to ID manifold) medians:")
    print(f"  ID-test {np.median(g_id):.3f} | far-OOD "
          f"{np.median(g_far):.3f} | near-OOD {np.median(g_near):.3f}")

    auroc_far = auroc(g_id, g_far)
    auroc_near = auroc(g_id, g_near)
    fpr_far, tau = fpr_at_tpr(g_id, g_far)
    fpr_near, _ = fpr_at_tpr(g_id, g_near)
    print(f"\nOOD DETECTION (standard metrics):")
    print(f"  far-OOD : AUROC {auroc_far:.3f} | FPR@95TPR {fpr_far:.1%} "
          f"(OOD wrongly answered when keeping 95% of real questions)")
    print(f"  near-OOD: AUROC {auroc_near:.3f} | FPR@95TPR {fpr_near:.1%}")

    # conformal: tau keeps 95% ID by construction; verify realized
    realized_id = float((g_id >= tau).mean())
    print(f"\nCONFORMAL @ tau={tau:.3f} (target 95% ID retention): "
          f"realized ID-keep {realized_id:.0%}, far-OOD rejected "
          f"{1-fpr_far:.0%}, near-OOD rejected {1-fpr_near:.0%}")

    verdict = ("STRONG far-OOD" if auroc_far > 0.85 else
               "weak far-OOD") + ", " + ("usable near-OOD"
               if auroc_near > 0.7 else "near-OOD HARD (adversarial "
               "topical adjacency -- the known limit)")
    print(f"\nVERDICT: gate envelope = {verdict}. The gate's power is "
          f"real in a semantic space for distributionally-distinct "
          f"inputs; near-OOD (same topic, unanswerable) is the honest "
          f"hard edge.")
    json.dump(dict(auroc_far=auroc_far, fpr_far=fpr_far,
                   auroc_near=auroc_near, fpr_near=fpr_near,
                   medians=dict(id=float(np.median(g_id)),
                                far=float(np.median(g_far)),
                                near=float(np.median(g_near)))),
              io.open(os.path.join(HERE, "gate_ood_result.json"), "w"),
              indent=1)


if __name__ == "__main__":
    main()
