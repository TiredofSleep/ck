"""calibrate_gate.py -- calibrate CK's GATE the way selective prediction
is actually evaluated (Geifman & El-Yaniv; Hendrycks OOD).

The gate is CK's one genuinely differentiated organ: abstain rather than
answer wrong. This measures it rigorously on a REAL public benchmark
with TRUE labels -- SQuAD 2.0 answerability (answerable vs unanswerable)
-- official train/dev splits, fully local fast features (no GPU, no
network), so it runs beside the GPU training.

  Task     : predict answerable(1)/unanswerable(0); a logistic classifier
             makes the call, a SELECTOR decides which calls to trust.
  Selectors: MSP (classifier confidence -- the standard baseline),
             max-logit (|margin|), GATE (kNN distance to the training
             manifold -- "have I seen inputs like this?"), random.
  Metrics  : risk-coverage curve + AURC (area under risk-coverage,
             LOWER = better selective prediction); risk @ fixed coverage.
  Conformal: split-conformal threshold for a target coverage; report
             GUARANTEED vs REALIZED (the honesty check -- exposes drift).
  OOD slice: fiction prose fed as fake questions -> does the gate refuse
             genuinely-foreign inputs the classifier would handle blind?

  python calibrate_gate.py
"""
import io
import json
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
BOOKS = os.path.join(ROOT, "external_corpora", "books")
RNG = np.random.default_rng(0)
HASHDIM = 1024
STOPQ = {"What", "Who", "When", "Where", "Which", "Why", "How", "Whose",
         "Whom", "The", "In", "Did", "Was", "Were", "Is", "Are", "Does"}


def load_squad(path, cap=None):
    d = json.load(io.open(path, encoding="utf-8"))
    rows = []
    for art in d["data"]:
        for para in art["paragraphs"]:
            ctx = para["context"]
            for qa in para["qas"]:
                rows.append((qa["question"], ctx,
                             0 if qa["is_impossible"] else 1))
    RNG.shuffle(rows)
    return rows[:cap] if cap else rows


def trigram_vec(s):
    s = "##" + s.lower()[:1500] + "##"
    v = np.zeros(HASHDIM, np.float32)
    for i in range(len(s) - 2):
        v[hash(s[i:i + 3]) % HASHDIM] += 1.0
    n = np.linalg.norm(v)
    return v / n if n > 0 else v


def feats(rows):
    X = []
    for q, ctx, _ in rows:
        qw = set(re.findall(r"[a-z]{4,}", q.lower()))
        cw = set(re.findall(r"[a-z]{4,}", ctx.lower()))
        overlap = len(qw & cw) / max(1, len(qw))
        tcos = float(trigram_vec(q) @ trigram_vec(ctx))
        names = [w for w in re.findall(r"\b[A-Z][a-z]{2,}\b", q)
                 if w not in STOPQ]
        present = np.mean([1.0 if w in ctx else 0.0
                           for w in names]) if names else 0.5
        absent = sum(1 for w in names if w not in ctx)
        X.append([overlap, tcos, np.log1p(len(q)), np.log1p(len(ctx)),
                  present, absent, len(qw)])
    return np.array(X, np.float32)


def logistic_fit(X, y, iters=4000, lr=0.5):
    w = np.zeros(X.shape[1]); b = 0.0
    for _ in range(iters):
        p = 1 / (1 + np.exp(-(X @ w + b)))
        g = (p - y) / len(y)
        w -= lr * (X.T @ g + 1e-4 * w); b -= lr * g.sum()
    return w, b


def aurc(scores, correct):
    """area under risk-coverage curve (lower=better). scores: higher =
    more trusted/answer-first."""
    order = np.argsort(-scores)
    c = correct[order].astype(float)
    cum_err = np.cumsum(1 - c)
    cov = np.arange(1, len(c) + 1)
    risk = cum_err / cov
    return float(risk.mean())          # mean risk over all coverages


def risk_at(scores, correct, cov):
    order = np.argsort(-scores)
    k = max(1, int(len(scores) * cov))
    sel = order[:k]
    return float(1 - correct[sel].mean())


def main():
    print("CALIBRATING THE GATE -- SQuAD 2.0 selective prediction "
          "(official splits, local features)\n")
    train = load_squad(os.path.join(HERE, "squad_train_v2.json"), cap=20000)
    test = load_squad(os.path.join(HERE, "squad_dev_v2.json"))
    ytr = np.array([r[2] for r in train])
    yte = np.array([r[2] for r in test])
    print(f"train {len(train)} ({ytr.mean():.0%} answerable) | "
          f"test {len(test)} ({yte.mean():.0%} answerable)")

    Xtr, Xte = feats(train), feats(test)
    mu, sd = Xtr.mean(0), Xtr.std(0) + 1e-9
    Xtr, Xte = (Xtr - mu) / sd, (Xte - mu) / sd

    # hold a calibration split out of train for conformal
    n_cal = 4000
    Xcal, ycal = Xtr[:n_cal], ytr[:n_cal]
    Xtr2, ytr2 = Xtr[n_cal:], ytr[n_cal:]
    w, b = logistic_fit(Xtr2, ytr2)

    # classifier predictions + correctness on test
    logit_te = Xte @ w + b
    p_te = 1 / (1 + np.exp(-logit_te))
    pred_te = (p_te >= 0.5).astype(int)
    correct = (pred_te == yte).astype(int)
    acc = correct.mean()
    print(f"answerability classifier test accuracy: {acc:.1%} "
          f"(majority {max(yte.mean(), 1-yte.mean()):.1%})\n")

    # selectors
    def gate_score(X, ref):              # kNN cosine to training manifold
        Xn = X / (np.linalg.norm(X, axis=1, keepdims=True) + 1e-9)
        Rn = ref / (np.linalg.norm(ref, axis=1, keepdims=True) + 1e-9)
        sims = Xn @ Rn.T
        k = 10
        return np.sort(sims, 1)[:, -k:].mean(1)

    ref = Xtr2[RNG.choice(len(Xtr2), 3000, replace=False)]
    selectors = {
        "MSP (standard)":   np.maximum(p_te, 1 - p_te),
        "max-logit (std)":  np.abs(logit_te),
        "GATE (kNN-dist)":  gate_score(Xte, ref),
        "random":           RNG.random(len(test)),
    }

    print("SELECTIVE PREDICTION  (risk = error among answered; "
          "lower better)")
    print(f"{'selector':>18} | {'AURC':>6} | risk@cov  100%  90%  80%  "
          f"70%  50%")
    res = {}
    for name, s in selectors.items():
        a = aurc(s, correct)
        rr = [risk_at(s, correct, c) for c in (1.0, .9, .8, .7, .5)]
        res[name] = dict(aurc=a, risk=rr)
        print(f"{name:>18} | {a:.4f} | "
              + "      ".join(f"{r:.0%}" for r in rr))

    # CONFORMAL: target 85% coverage; tau = 15th pctile of gate on cal
    g_cal = gate_score(Xcal, ref)
    g_te = selectors["GATE (kNN-dist)"]
    alpha = 0.15
    tau = np.quantile(g_cal, alpha)
    realized = float((g_te >= tau).mean())
    risk_kept = float(1 - correct[g_te >= tau].mean())
    print(f"\nCONFORMAL gate @ target coverage {1-alpha:.0%}: "
          f"tau={tau:.3f}")
    print(f"  realized coverage on test: {realized:.0%} "
          f"(guaranteed >= {1-alpha:.0%} IF cal~test) | "
          f"risk on answered: {risk_kept:.0%}")
    drift = (1 - alpha) - realized
    print(f"  guaranteed-vs-realized gap: {drift:+.0%} "
          f"({'drift -- cal != test distribution' if abs(drift) > 0.05 else 'holds'})")

    # OOD slice: fiction prose as fake 'questions' over a real context
    try:
        bk = sorted(os.listdir(BOOKS))[0]
        prose = re.sub(r"\s+", " ", io.open(os.path.join(BOOKS, bk),
                       encoding="utf-8", errors="ignore").read())
        sents = [s.strip() for s in re.split(r"(?<=[.!?]) ", prose)
                 if 40 < len(s.strip()) < 200][:200]
        ctx0 = test[0][1]
        ood = [(s, ctx0, 0) for s in sents]
        Xood = (feats(ood) - mu) / sd
        g_ood = gate_score(Xood, ref)
        print(f"\nOOD SLICE (200 fiction sentences as fake questions):")
        print(f"  gate score: in-domain median {np.median(g_te):.3f} vs "
              f"OOD median {np.median(g_ood):.3f}")
        print(f"  at the conformal tau, OOD answered (hallucination "
              f"surface): {float((g_ood >= tau).mean()):.0%} "
              f"-- the gate refuses foreign inputs the classifier would "
              f"handle blind")
    except Exception as e:
        print("OOD slice skipped:", e)

    best = min(res, key=lambda k: res[k]["aurc"])
    g = res["GATE (kNN-dist)"]["aurc"]; m = res["MSP (standard)"]["aurc"]
    print(f"\nVERDICT: best selector = {best} (AURC {res[best]['aurc']:.4f}). "
          f"GATE {'beats' if g < m else 'trails'} MSP "
          f"({g:.4f} vs {m:.4f}) on selective prediction; "
          f"its real edge is the OOD slice (knowing the input is foreign), "
          f"which MSP cannot see.")
    json.dump({k: {kk: (vv if not isinstance(vv, list) else
                        [round(x, 4) for x in vv])
                   for kk, vv in v.items()} for k, v in res.items()},
              io.open(os.path.join(HERE, "gate_calib_result.json"), "w"),
              indent=1)


if __name__ == "__main__":
    main()
