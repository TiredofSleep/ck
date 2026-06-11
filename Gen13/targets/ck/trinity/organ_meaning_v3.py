"""organ_meaning_v3.py -- the published fix for the LM-pooling failure:
SUPERVISED CONTRASTIVE sentence head (SBERT/supervised-SimCSE recipe).

The native LM's raw mean-pooled states routed at 35% (orthography, not
semantics). The field's fix: train a small projection with InfoNCE --
same-topic training texts attract, in-batch others repel. Labels come
from the TRAINING reference set only; held-out test queries never seen.

FAIR FIGHT (abilities earn places): the identical contrastive head is
trained on BOTH contenders' raw vectors --
   LM+head    : frozen native-LM mean-pooled states -> 128-d
   PPMI+head  : seat-holder's SIF vectors          -> 128-d
Routing eval on the same held-out 20. REGISTERED: winner >= 70% takes
the seat; both < 65% and raw PPMI-SVD keeps it.

  python organ_meaning_v3.py
"""
import io
import json
import os
import sys

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as Fn

HERE = os.path.dirname(os.path.abspath(__file__))
EXT = os.path.join(HERE, "..", "extraction")
sys.path.insert(0, EXT)
import organ_meaning_native as OMN                         # noqa: E402
import train_native_lm as TNL                              # noqa: E402

DEV = "cuda" if torch.cuda.is_available() else "cpu"
torch.manual_seed(0)


def contrastive_head(Xtr, ytr, dim_out=128, steps=600, lr=1e-3, tau=0.1):
    X = torch.tensor(Xtr, dtype=torch.float32, device=DEV)
    y = torch.tensor(ytr, device=DEV)
    head = nn.Sequential(nn.Linear(X.shape[1], 256), nn.Tanh(),
                         nn.Linear(256, dim_out)).to(DEV)
    opt = torch.optim.Adam(head.parameters(), lr=lr)
    n = len(y)
    for step in range(steps):
        idx = torch.randperm(n, device=DEV)[:128]
        z = Fn.normalize(head(X[idx]), dim=1)
        sim = z @ z.T / tau
        sim.fill_diagonal_(-1e9)
        same = (y[idx][:, None] == y[idx][None, :]).float()
        same.fill_diagonal_(0)
        # InfoNCE with multiple positives: -log sum(pos) / sum(all)
        log_all = torch.logsumexp(sim, 1)
        pos = (sim.exp() * same).sum(1) + 1e-9
        loss = (-(pos.log() - log_all))[same.sum(1) > 0].mean()
        opt.zero_grad(); loss.backward(); opt.step()
    head.eval()
    return head


def main():
    from demo_facts_head import TOPICS, ANCHORS
    from project2_routing import char_trigrams, train_head, zs, TOPIC_LIST
    import braid_memory as bm
    grown = json.load(io.open(os.path.join(EXT, "teacher_corpus.json"),
                              encoding="utf-8"))
    ref_x, ref_y, test_x, test_y = [], [], [], []
    for t in TOPIC_LIST:
        g = list(grown.get(t, []))
        ref_x += TOPICS[t][:4] + list(ANCHORS[t]) + g
        ref_y += [t] * (4 + len(ANCHORS[t]) + len(g))
        test_x += TOPICS[t][4:]; test_y += [t] * 2
    y_ref = np.array([TOPIC_LIST.index(t) for t in ref_y])
    y_te = np.array([TOPIC_LIST.index(t) for t in test_y])

    print(f"TRINITY -- meaning organ v3: supervised contrastive head "
          f"({DEV.upper()})\n")

    # contender 1: native LM states
    ckpt = torch.load(os.path.join(HERE, "ck_native_lm.pt"),
                      weights_only=False)
    d, L, h = ckpt["dims"]
    lm = TNL.MiniGPT(len(ckpt["stoi"]), d, L, h).to(DEV)
    lm.load_state_dict(ckpt["model"]); lm.eval()
    LM_ref = TNL.sent_embed(lm, ckpt["stoi"], ref_x)
    LM_te = TNL.sent_embed(lm, ckpt["stoi"], test_x)

    # contender 2: PPMI-SVD SIF vectors (with the v2 curriculum corpus)
    corpus = OMN.gather_corpus()
    cur = json.load(io.open(os.path.join(HERE, "synthetic_curriculum.json"),
                            encoding="utf-8"))
    synth = "\n".join(t for ts in cur.values() for t in ts).lower()
    corpus += ("\n" + synth) * 6
    W, idx, freq, n_tok = OMN.train_vectors(corpus)
    sent = OMN.make_sif(W, idx, freq, n_tok)
    PP_ref = np.array([sent(x) for x in ref_x])
    PP_te = np.array([sent(x) for x in test_x])

    Xb = lambda xs: np.array([bm.braid_signature_rich(x) for x in xs])
    Xc_ref, vocab = char_trigrams(ref_x)
    Xc_te, _ = char_trigrams(test_x, vocab)
    form = [(Xb(ref_x), Xb(test_x)), (Xc_ref, Xc_te)]

    def routing(M_ref, M_te):
        out_r, out_t = [], []
        for A_, B_ in [(M_ref, M_te)] + form:
            Az, m_, s_ = zs(A_)
            out_r.append(Az); out_t.append((B_ - m_) / s_)
        Fr, Ft = np.hstack(out_r), np.hstack(out_t)
        Wh, bh = train_head(Fr, y_ref)
        return float(np.mean((Ft @ Wh + bh).argmax(1) == y_te))

    results = {}
    for name, (R, T) in (("LM raw (reference)", (LM_ref, LM_te)),
                         ("PPMI raw (seat, 65%)", (PP_ref, PP_te))):
        results[name] = routing(R, T)
    for name, (R, T) in (("LM + contrastive head", (LM_ref, LM_te)),
                         ("PPMI + contrastive head", (PP_ref, PP_te))):
        head = contrastive_head((R - R.mean(0)) / (R.std(0) + 1e-9), y_ref)
        with torch.no_grad():
            zr = head(torch.tensor((R - R.mean(0)) / (R.std(0) + 1e-9),
                                   dtype=torch.float32, device=DEV))
            zt = head(torch.tensor((T - R.mean(0)) / (R.std(0) + 1e-9),
                                   dtype=torch.float32, device=DEV))
        results[name] = routing(Fn.normalize(zr, dim=1).cpu().numpy(),
                                Fn.normalize(zt, dim=1).cpu().numpy())
    for k, v in results.items():
        print(f"  {k:>26}: routing {v:.0%}")

    best = max(results, key=results.get)
    print(f"\nVERDICT: best = {best} at {results[best]:.0%} "
          f"(borrowed reference: 80%). "
          f"{'SEAT UPGRADED' if results[best] >= 0.70 and 'head' in best else 'PPMI-SVD raw keeps the seat'}")
    json.dump({k: float(v) for k, v in results.items()},
              io.open(os.path.join(HERE, "organ_meaning_v3_result.json"),
                      "w"), indent=1)


if __name__ == "__main__":
    main()
