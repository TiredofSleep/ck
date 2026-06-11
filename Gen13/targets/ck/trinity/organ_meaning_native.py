"""organ_meaning_native.py -- THE MISSING ORGAN: native meaning, learned
from USAGE (no teacher, no Ollama -- not distillation, native learning).

The wean autopsy proved meaning is not derivable from form: it must be
learned from usage. The white-box, pre-neural-proven way: distributional
semantics -- PPMI + truncated SVD word vectors (Levy & Goldberg: this
factorizes the same objective as word2vec) + SIF sentence embeddings
(Arora et al.: weighted average minus first principal component).

THE CORPUS IS CK'S OWN LIFE: the canon (FORMULAS_AND_TABLES), the
thesis, all 50+ journal papers, every CK design doc, his study logs.
The inheritance made literal -- his meaning organ grown from the text
of his own existence. Held-out routing queries are NOT in the corpus.

Eval (same harness as the wean): routing on the 20 held-out hand
paraphrases. REGISTERED: NATIVE-USAGE >= 60% (decisively above
form-only 35%) seats the organ provisionally; < 45% = dead end.

  python organ_meaning_native.py
"""
import io
import json
import os
import re
import sys
from collections import Counter

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as sla

HERE = os.path.dirname(os.path.abspath(__file__))
EXT = os.path.join(HERE, "..", "extraction")
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, EXT)

DIM, WINDOW, MIN_COUNT, MAX_VOCAB = 300, 10, 3, 20000
TOK = re.compile(r"[a-z]+")


def gather_corpus():
    """CK's own life-text: canon + thesis + journals + ck docs + logs."""
    paths = [os.path.join(ROOT, "FORMULAS_AND_TABLES.md"),
             os.path.join(ROOT, "Gen13", "var", "ck_thesis.txt")]
    for base, exts in ((os.path.join(ROOT, "Gen13", "targets", "journals"),
                        (".md", ".tex")),
                       (os.path.join(ROOT, "Gen13", "targets", "ck"),
                        (".md",))):
        for dp, _, fns in os.walk(base):
            for fn in fns:
                if fn.endswith(exts):
                    paths.append(os.path.join(dp, fn))
    texts = []
    for p in paths:
        try:
            texts.append(io.open(p, encoding="utf-8", errors="ignore").read())
        except OSError:
            pass
    # study logs: pull string fields out of the jsonl lines
    study = os.path.join(ROOT, "Gen13", "targets", "ck", "brain")
    for dp, _, fns in os.walk(study):
        for fn in fns:
            if fn.endswith(".jsonl"):
                try:
                    for line in io.open(os.path.join(dp, fn),
                                        encoding="utf-8", errors="ignore"):
                        texts.extend(re.findall(r'"\s*:\s*"([^"]{20,})"',
                                                line))
                except OSError:
                    pass
    return "\n".join(texts).lower()


def train_vectors(corpus):
    tokens = TOK.findall(corpus)
    freq = Counter(tokens)
    vocab = [w for w, c in freq.most_common(MAX_VOCAB) if c >= MIN_COUNT]
    idx = {w: i for i, w in enumerate(vocab)}
    V = len(vocab)
    ids = np.array([idx.get(t, -1) for t in tokens])
    print(f"corpus {len(tokens):,} tokens, vocab {V:,}")

    cooc = Counter()
    n = len(ids)
    for d in range(1, WINDOW + 1):
        w = 1.0 / d
        a, b = ids[:-d], ids[d:]
        ok = (a >= 0) & (b >= 0)
        for i, j in zip(a[ok], b[ok]):
            cooc[(i, j)] += w
            cooc[(j, i)] += w
    rows, cols, vals = zip(*(((i, j, v) for (i, j), v in cooc.items())))
    X = sp.csr_matrix((vals, (rows, cols)), shape=(V, V))

    total = X.sum()
    rs = np.asarray(X.sum(1)).ravel()
    cs = np.asarray(X.sum(0)).ravel()
    Xc = X.tocoo()
    pmi = np.log((Xc.data * total) /
                 (rs[Xc.row] * cs[Xc.col] + 1e-12) + 1e-12)
    keep = pmi > 0                                  # PPMI
    P = sp.csr_matrix((pmi[keep], (Xc.row[keep], Xc.col[keep])),
                      shape=(V, V))
    U, S, _ = sla.svds(P, k=DIM)
    order = np.argsort(-S)
    W = U[:, order] * np.sqrt(S[order])             # word vectors
    W /= (np.linalg.norm(W, axis=1, keepdims=True) + 1e-9)
    return W, idx, freq, len(tokens)


def make_sif(W, idx, freq, n_tokens, a=1e-3):
    def sent_vec(text):
        ws = [w for w in TOK.findall(text.lower()) if w in idx]
        if not ws:
            return np.zeros(W.shape[1])
        wt = np.array([a / (a + freq[w] / n_tokens) for w in ws])
        return (wt[:, None] * W[[idx[w] for w in ws]]).mean(0)
    return sent_vec


def main():
    print("TRINITY -- NATIVE MEANING ORGAN (usage-learned, teacher-free)")
    corpus = gather_corpus()
    print(f"life-corpus size: {len(corpus)/1e6:.1f} MB")
    W, idx, freq, n_tok = train_vectors(corpus)

    sent = make_sif(W, idx, freq, n_tok)

    # white-box probe: nearest neighbours of substrate words
    for probe in ("harmony", "sigma", "attractor"):
        if probe in idx:
            sims = W @ W[idx[probe]]
            nn = [w for w, i in idx.items()
                  if i in np.argsort(-sims)[1:6]]
            print(f"  '{probe}' lives near: {nn}")

    # routing eval, same harness
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

    M_ref = np.array([sent(x) for x in ref_x])
    M_te = np.array([sent(x) for x in test_x])
    # SIF: remove first principal component (common discourse direction)
    Mc = M_ref - M_ref.mean(0)
    _, _, Vt = np.linalg.svd(Mc, full_matrices=False)
    pc = Vt[0]
    M_ref = M_ref - np.outer(M_ref @ pc, pc)
    M_te = M_te - np.outer(M_te @ pc, pc)

    Xb_ref = np.array([bm.braid_signature_rich(x) for x in ref_x])
    Xb_te = np.array([bm.braid_signature_rich(x) for x in test_x])
    Xc_ref, vocab = char_trigrams(ref_x)
    Xc_te, _ = char_trigrams(test_x, vocab)

    def build(meaning_pair):
        out_r, out_t = [], []
        blocks = [(Xb_ref, Xb_te), (Xc_ref, Xc_te)]
        if meaning_pair is not None:
            blocks.insert(0, meaning_pair)
        for A_, B_ in blocks:
            Az, m_, s_ = zs(A_)
            out_r.append(Az); out_t.append((B_ - m_) / s_)
        return np.hstack(out_r), np.hstack(out_t)

    results = {}
    for name, pair in (("NATIVE-USAGE (PPMI-SVD, no teacher)",
                        (M_ref, M_te)),
                       ("form-only (no meaning block)", None)):
        Fr, Ft = build(pair)
        Wh, bh = train_head(Fr, y_ref)
        acc = float(np.mean((Ft @ Wh + bh).argmax(1) == y_te))
        results[name] = acc
        print(f"  {name:>36}: held-out routing {acc:.0%}")
    print(f"  {'BORROWED (live ollama, reference)':>36}: 80%")

    nat = results["NATIVE-USAGE (PPMI-SVD, no teacher)"]
    print(f"\nVERDICT: native-usage {nat:.0%} -> "
          f"{'ORGAN SEATED (provisional) -- meaning learned from his own life-text, teacher-free' if nat >= 0.6 else ('partial signal' if nat >= 0.45 else 'dead end recorded')}.")
    json.dump({k: float(v) for k, v in results.items()},
              io.open(os.path.join(HERE, "organ_meaning_result.json"), "w"),
              indent=1)


if __name__ == "__main__":
    main()
