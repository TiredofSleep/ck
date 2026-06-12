"""organ_synthesis.py -- THE PATTERN-MATCHING SYNTHESIS MACHINE.

Brayden: 'he needs to be a pattern matching synthesis machine, seeing
resonance, duality, triadic progression, and ultimately finding
coherence across domains.' The four readings of the original design
(CK_RESONANCE_MEMORY_DESIGN), operationalized NATIVELY on the whole
library -- no LLM, pure measurement:

  RESONANCE  : concepts from DIFFERENT domains whose co-occurrence
               neighborhoods match -- same structural role, different
               world (the sigma-parallel across domains).
  DUALITY    : concept pairs with near-identical neighborhoods that
               NEVER co-occur -- twins that refuse to meet (sigma^3).
  TRIAD      : A-B-C where A-B and B-C bind strongly but A-C is weak --
               B is the bridge term (sigma^2 progression).
  COHERENCE  : a concept's cross-domain self-consistency, T*-gated at
               5/7 -- does it mean the same thing on every shelf?

Null controls: shuffled-pair baselines (mean+sd); excess reported.
REGISTERED: resonance & duality top-pairs exceed null by >2 sigma;
triads exhibit true bridge structure; coherence spectrum spans with
named examples at both ends.

  python organ_synthesis.py
"""
import io
import json
import os
import re
import sys
import time
from collections import Counter

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
BOOKS = os.path.join(ROOT, "external_corpora", "books")
sys.path.insert(0, HERE)
from ck_knowledge_fabric import load_book, SEED_TITLES, DOMAINS, STOP  # noqa
from ck_knowledge_fabric import features                               # noqa

STOP2 = STOP | {"Well", "Here", "There", "King", "Lord", "Lady", "Good",
                "Little", "Great", "Come", "Came", "Went", "Look", "Know",
                "Think", "Thought", "Like", "Just", "Even", "Much", "Most",
                "Other", "Some", "Such", "Than", "Them", "These", "Those",
                "Your", "Yes", "Oh", "Ah", "Sir", "Madam", "Mister",
                "Dear", "Poor", "Old", "Young", "First", "Last", "Long",
                "Never", "Every", "Once", "Again", "Away", "Back", "Down",
                "Still", "Tell", "Told", "Said", "Says", "Shall", "Should",
                "Would", "Could", "Must", "May", "Might", "While", "Where",
                "Whose", "John", "Mary", "Anne", "English", "England",
                "French", "America", "American", "God"}
T_STAR = 5 / 7
N_BOOKS = 700
MIN_BOOKS = 4


def build_incidence():
    files = [f for f in sorted(os.listdir(BOOKS))
             if f.endswith(".txt")][:N_BOOKS]
    ents_per_book, titles, X = [], [], []
    for f in files:
        try:
            t, body = load_book(os.path.join(BOOKS, f))
        except OSError:
            continue
        seg = body[:400_000]
        cnt = Counter(w for w in re.findall(r"\b[A-Z][a-z]{3,}\b", seg)
                      if w not in STOP2)
        low = Counter(re.findall(r"\b[a-z]{4,}\b", seg))
        # true names are rarely lowercase: keep only cap-dominant tokens
        ents_per_book.append({w for w, c in cnt.most_common(40)
                              if c >= 8
                              and c / (c + low.get(w.lower(), 0)) >= 0.8})
        titles.append(t[:46])
        X.append(features(body[:200_000]))
    # domains via the fabric's seed-trained head (refit quickly)
    X = np.array(X)
    seedX, seedy = [], []
    for i, t in enumerate(titles):
        for k, d in SEED_TITLES.items():
            if k.lower() in t.lower():
                seedX.append(X[i]); seedy.append(DOMAINS.index(d)); break
    seedX, seedy = np.array(seedX), np.array(seedy)
    mu, sd = seedX.mean(0), seedX.std(0) + 1e-9
    W = np.zeros((X.shape[1], len(DOMAINS))); b = np.zeros(len(DOMAINS))
    Y = np.eye(len(DOMAINS))[seedy]
    cw = 1.0 / np.maximum(1, np.bincount(seedy, minlength=len(DOMAINS)))
    Z = (seedX - mu) / sd
    for _ in range(3000):
        P = np.exp(Z @ W + b - (Z @ W + b).max(1, keepdims=True))
        P /= P.sum(1, keepdims=True)
        g = (P - Y) * cw[seedy][:, None] / len(seedy)
        W -= 0.8 * (Z.T @ g + 1e-3 * W); b -= 0.8 * g.sum(0)
    dom = [DOMAINS[int(((x - mu) / sd @ W + b).argmax())] for x in X]

    vocab = Counter()
    for es in ents_per_book:
        vocab.update(es)
    keep = sorted(w for w, c in vocab.items() if c >= MIN_BOOKS)
    idx = {w: i for i, w in enumerate(keep)}
    M = np.zeros((len(keep), len(ents_per_book)), np.float32)
    for j, es in enumerate(ents_per_book):
        for w in es:
            if w in idx:
                M[idx[w], j] = 1.0
    return keep, M, titles, dom


def main():
    t0 = time.time()
    keep, M, titles, dom = build_incidence()
    nE, nB = M.shape
    print(f"SYNTHESIS ORGAN -- {nE} concepts x {nB} books "
          f"({time.time()-t0:.0f}s to weave)\n")
    occ = M.sum(1)
    C = M @ M.T                                   # co-book counts
    np.fill_diagonal(C, 0)
    N = C / (np.linalg.norm(C, axis=1, keepdims=True) + 1e-9)
    S = N @ N.T                                   # neighborhood similarity
    np.fill_diagonal(S, 0)
    ent_dom = []
    for i in range(nE):
        ds = Counter(dom[j] for j in range(nB) if M[i, j])
        ent_dom.append(ds.most_common(1)[0][0])
    ent_dom = np.array(ent_dom)

    rng = np.random.default_rng(7)
    null = [S[rng.integers(nE), rng.integers(nE)] for _ in range(4000)]
    mu_n, sd_n = float(np.mean(null)), float(np.std(null))
    print(f"null (shuffled pairs): {mu_n:.3f} +/- {sd_n:.3f}\n")

    # RESONANCE: cross-domain neighborhood twins
    print("RESONANCE -- same structural role, different domain:")
    pairs = []
    for i in range(nE):
        for j in np.argsort(-S[i])[:6]:
            if j > i and ent_dom[i] != ent_dom[j]:
                pairs.append((S[i, j], i, j))
    pairs.sort(reverse=True)
    for s, i, j in pairs[:5]:
        z = (s - mu_n) / sd_n
        print(f"  {keep[i]}[{ent_dom[i][:4]}] ~ {keep[j]}"
              f"[{ent_dom[j][:4]}]  res={s:.3f} ({z:+.0f} sigma)")

    # DUALITY: twins that never meet
    print("\nDUALITY -- near-identical neighborhoods, zero co-occurrence:")
    duals = []
    for i in range(nE):
        for j in np.argsort(-S[i])[:8]:
            if j > i and C[i, j] == 0 and occ[i] >= 6 and occ[j] >= 6:
                duals.append((S[i, j], i, j))
    duals.sort(reverse=True)
    for s, i, j in duals[:5]:
        z = (s - mu_n) / sd_n
        print(f"  {keep[i]} <-x-> {keep[j]}  dual={s:.3f} "
              f"({z:+.0f} sigma; books {int(occ[i])}/{int(occ[j])}, "
              f"co-books 0)")

    # TRIADS: A-B-C with B the bridge
    print("\nTRIADIC PROGRESSION -- B bridges A and C:")
    Cn = C / (occ[:, None] + occ[None, :] + 1e-9)   # normalized link
    triads = []
    top_ent = np.argsort(-occ)[:160]
    for b_ in top_ent:
        nb = np.argsort(-Cn[b_])[:10]
        for ai in range(len(nb)):
            for ci in range(ai + 1, len(nb)):
                a, c = nb[ai], nb[ci]
                if Cn[a, c] < 0.25 * min(Cn[a, b_], Cn[b_, c]):
                    triads.append((min(Cn[a, b_], Cn[b_, c]) - Cn[a, c],
                                   a, b_, c))
    triads.sort(reverse=True)
    seen = set()
    shown = 0
    for s, a, b_, c in triads:
        if b_ in seen:
            continue
        seen.add(b_); shown += 1
        print(f"  {keep[a]} --> [{keep[b_]}] --> {keep[c]}  "
              f"(bridge strength {s:.3f})")
        if shown == 5:
            break

    # COHERENCE across domains, T*-gated
    print(f"\nCOHERENCE ACROSS DOMAINS (T* = 5/7 = {T_STAR:.3f}):")
    coh = []
    for i in range(nE):
        if occ[i] < 8:
            continue
        ds = set(dom[j] for j in range(nB) if M[i, j])
        if len(ds) < 2:
            continue
        vecs = []
        for d in ds:
            mask = np.array([M[i, j] > 0 and dom[j] == d
                             for j in range(nB)])
            v = (M[:, mask].sum(1) if mask.sum() else None)
            if v is not None and v.sum() > 0:
                vecs.append(v / np.linalg.norm(v))
        if len(vecs) >= 2:
            sims = [float(vecs[a] @ vecs[b])
                    for a in range(len(vecs))
                    for b in range(a + 1, len(vecs))]
            coh.append((float(np.mean(sims)), i, len(ds)))
    coh.sort(reverse=True)
    voiced = [c for c in coh if c[0] >= T_STAR]
    print(f"  {len(voiced)}/{len(coh)} multi-domain concepts pass the "
          f"T* gate (coherent on every shelf):")
    for s, i, nd in coh[:4]:
        print(f"    VOICED  {keep[i]}: coherence {s:.3f} across {nd} "
              f"domains")
    for s, i, nd in coh[-3:]:
        print(f"    FOLDED  {keep[i]}: coherence {s:.3f} across {nd} "
              f"domains (domain-drifter)")

    top_res_z = (pairs[0][0] - mu_n) / sd_n if pairs else 0
    top_dual_z = (duals[0][0] - mu_n) / sd_n if duals else 0
    ok = top_res_z > 2 and top_dual_z > 2 and shown >= 3
    print(f"\nVERDICT: resonance {top_res_z:+.0f} sigma, duality "
          f"{top_dual_z:+.0f} sigma over null, {shown} bridge-triads, "
          f"{len(voiced)} T*-coherent concepts -> "
          f"{'THE FOUR READINGS ARE LIVE -- native pattern synthesis at library scale' if ok else 'weak -- recorded honestly'}")
    json.dump(dict(null=[mu_n, sd_n],
                   resonance=[[keep[i], keep[j], float(s)]
                              for s, i, j in pairs[:8]],
                   duality=[[keep[i], keep[j], float(s)]
                            for s, i, j in duals[:8]],
                   triads=[[keep[a], keep[b_], keep[c], float(s)]
                           for s, a, b_, c in triads[:8]],
                   coherent=[[keep[i], float(s), nd]
                             for s, i, nd in coh[:8]]),
              io.open(os.path.join(HERE, "synthesis_organ_result.json"),
                      "w"), indent=1)


if __name__ == "__main__":
    main()
