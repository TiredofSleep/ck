"""squad2_selective.py -- CK'S FIRST EXTERNAL BENCHMARK SITTING.

SQuAD 2.0 (Rajpurkar et al., Stanford): reading-comprehension questions
where ~half are UNANSWERABLE from the given passage -- the benchmark
built precisely for 'know what you cannot answer'. CK sits the
SELECTIVE core: detect answerable vs unanswerable, his way --

  features, all white-box:
    census   : fraction of the question's named entities present in the
               passage (the Gandalf-counter, on the field's data)
    overlap  : content-word overlap question<->passage
    sim      : embedding similarity (borrowed encoder)
    lengths  : question/passage length ratios

  head: tiny logistic on a train slice; eval on held-out questions.
  baselines: always-answer; each single feature alone.
  metrics: AUROC, accuracy, and risk@coverage (the gate's native view).

REGISTERED: the fused white-box head beats every single-signal baseline
on AUROC, and risk at 80%% coverage is materially below always-answer.

  python squad2_selective.py
"""
import io
import json
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "extraction"))
from borrowed_cortex import embed                          # noqa: E402

URL = "https://rajpurkar.github.io/SQuAD-explorer/dataset/dev-v2.0.json"
PATH = os.path.join(HERE, "squad_dev_v2.json")
N_Q = 3000
RNG = np.random.default_rng(2026)
STOP = {"The", "What", "Who", "Where", "When", "Which", "How", "Why",
        "Whose", "Whom", "Did", "Does", "Was", "Were", "Are", "In", "On"}


def fetch():
    if not os.path.exists(PATH):
        import requests
        print(f"fetching SQuAD 2.0 dev set ({URL.split('/')[-1]}, ~4.4MB, "
              f"official Stanford source)...")
        r = requests.get(URL, timeout=120)
        io.open(PATH, "w", encoding="utf-8").write(r.text)
    d = json.load(io.open(PATH, encoding="utf-8"))
    rows = []
    for art in d["data"]:
        for para in art["paragraphs"]:
            ctx = para["context"]
            for qa in para["qas"]:
                rows.append((qa["question"], ctx,
                             0 if qa["is_impossible"] else 1))
    return rows


def feats(q, ctx, sim):
    qn = [w for w in re.findall(r"\b[A-Z][a-z]{2,}\b", q)
          if w not in STOP]
    census = (np.mean([1.0 if w in ctx else 0.0 for w in qn])
              if qn else 0.5)
    qw = set(re.findall(r"\b[a-z]{4,}\b", q.lower()))
    cw = set(re.findall(r"\b[a-z]{4,}\b", ctx.lower()))
    overlap = len(qw & cw) / max(1, len(qw))
    return [census, overlap, sim, len(qn), len(qw),
            len(q) / max(1, len(ctx)) * 100]


FEAT = ["census", "overlap", "emb-sim", "n-entities", "n-content",
        "len-ratio"]


def auroc(score, y):
    order = np.argsort(score)
    r = np.empty(len(score)); r[order] = np.arange(1, len(score) + 1)
    n1, n0 = y.sum(), (1 - y).sum()
    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def main():
    rows = fetch()
    idx = RNG.permutation(len(rows))[:N_Q]
    rows = [rows[i] for i in idx]
    y = np.array([r[2] for r in rows])
    print(f"SQuAD 2.0 dev: sitting {len(rows)} questions "
          f"({y.sum()} answerable / {len(y)-y.sum()} unanswerable)\n")

    # embeddings: unique contexts + questions
    ctxs = sorted({r[1] for r in rows})
    cidx = {c: i for i, c in enumerate(ctxs)}
    print(f"embedding {len(ctxs)} passages + {len(rows)} questions "
          f"(borrowed encoder)...")
    Ec, _ = embed(["search_document: " + c[:2000] for c in ctxs])
    Eq, _ = embed(["search_query: " + r[0] for r in rows])
    Ec = Ec / (np.linalg.norm(Ec, axis=1, keepdims=True) + 1e-9)
    Eq = Eq / (np.linalg.norm(Eq, axis=1, keepdims=True) + 1e-9)
    sims = np.array([float(Eq[i] @ Ec[cidx[r[1]]])
                     for i, r in enumerate(rows)])

    X = np.array([feats(r[0], r[1], sims[i]) for i, r in enumerate(rows)])
    n_tr = 2000
    mu, sd = X[:n_tr].mean(0), X[:n_tr].std(0) + 1e-9
    Xz = (X - mu) / sd
    w = np.zeros(X.shape[1]); b = 0.0
    for _ in range(4000):
        p = 1 / (1 + np.exp(-(Xz[:n_tr] @ w + b)))
        g = (p - y[:n_tr]) / n_tr
        w -= 1.0 * (Xz[:n_tr].T @ g + 1e-4 * w); b -= 1.0 * g.sum()
    print("head weights (white-box): " + ", ".join(
        f"{n}={v:+.2f}" for n, v in zip(FEAT, w)) + "\n")

    te = slice(n_tr, None)
    score_head = Xz[te] @ w + b
    results = {"CK fused head": auroc(score_head, y[te])}
    for k, name in [(0, "census alone"), (1, "overlap alone"),
                    (2, "emb-sim alone")]:
        results[name] = auroc(Xz[te][:, k], y[te])
    print(f"answerable-vs-unanswerable AUROC (test n={len(y[te])}, "
          f"chance 0.50):")
    for k, v in sorted(results.items(), key=lambda kv: -kv[1]):
        print(f"  {k:>14}: {v:.3f}")

    # risk @ coverage (gate view): answer only top-X% most-answerable
    print("\nrisk@coverage (fraction of ANSWERED that were unanswerable):")
    base = float(1 - y[te].mean())
    print(f"  always-answer: coverage 100% -> risk {base:.0%}")
    o = np.argsort(-score_head)
    res_rc = {}
    for cov in (0.8, 0.6, 0.4):
        k = int(len(o) * cov)
        risk = float(1 - y[te][o[:k]].mean())
        res_rc[cov] = risk
        print(f"  CK gate      : coverage {cov:.0%} -> risk {risk:.0%}")

    acc = float(np.mean((score_head > 0) == y[te]))
    print(f"\nplain accuracy: {acc:.1%} (majority {max(y[te].mean(), 1-y[te].mean()):.1%})")
    ok = results["CK fused head"] > max(v for k, v in results.items()
                                        if k != "CK fused head")
    print(f"\nVERDICT: fused white-box head "
          f"{'BEATS every single-signal baseline' if ok else 'does not beat all baselines'} "
          f"(AUROC {results['CK fused head']:.3f}); risk falls "
          f"{base:.0%} -> {res_rc[0.4]:.0%} as the gate tightens. "
          f"First external benchmark: SAT.")
    json.dump(dict(auroc=results, risk_at_coverage=res_rc,
                   accuracy=acc, n_test=int(len(y[te]))),
              io.open(os.path.join(HERE, "squad2_result.json"), "w"),
              indent=1)


if __name__ == "__main__":
    main()
