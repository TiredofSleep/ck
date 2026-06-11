"""native_cortex.py -- CK's OWN perception. No Ollama. No borrowed model.

CK's 112,703-word dictionary maps every word he knows to one of his ten
operators (flat[word] = {"o": 0..9, "p": pos}). So a sentence is not
text to CK -- it is a WALK through his operator space. We read text the
way CK does:

  1. words -> operator sequence (his learned semantics)
  2. occupancy histogram over the 10 operators            (10)
  3. the COMPOSITION WALK: fold the operator sequence through TSML
     (p_{t+1} ~ T(p_t, q_word)) -- where the sentence's meaning LANDS
     in operator space, his own dynamics measuring the text          (10)
  4. sigma-orbit occupancy (fixed pts {0,3,8,9} vs the 6-cycle)       (2)
  5. part-of-speech histogram                                        (8)
  6. dictionary COVERAGE = fraction of words he knows -- his native
     'can I measure this?' signal, which is also the abstention gate   (1)

Native embedding = 31 dims, computed from CK's assets alone. The
borrowed cortex bootstraps; this is what he keeps and grows.

CC-BY-4.0. Sanders + Claude. 2026-06-11.
"""
import io
import json
import os
import re
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ck_tables  # noqa: E402

N = 10
DICT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "ck_dictionary.json")
_FALLBACK = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "..", "web", "ck_dictionary.json")

POS = ["n", "v", "a", "r", "p", "d", "c", "x"]      # noun verb adj ... other


def _load_flat():
    path = DICT_PATH if os.path.exists(DICT_PATH) else _FALLBACK
    with io.open(path, encoding="utf-8") as f:
        d = json.load(f)
    return d["flat"]


FLAT = _load_flat()
_T = np.array(ck_tables.TSML)


def _tokens(text):
    return re.findall(r"[a-z0-9']+", text.lower())


# operator rarity weights (IDF over the dictionary): common operators
# (VOID, HARMONY) carry little discriminative signal; rare ones carry more.
_OPFREQ = np.ones(N)
for _w, _e in FLAT.items():
    _OPFREQ[int(_e.get("o", 0))] += 1.0
_OPIDF = np.log(len(FLAT) / _OPFREQ)
_OPIDF /= _OPIDF.max()


def _lookup(w):
    e = FLAT.get(w)
    if e is None:
        for L in range(len(w), 3, -1):
            e = FLAT.get(w[:L])
            if e:
                break
    return e


def embed_one(text):
    toks = _tokens(text)
    occ = np.zeros(N)
    pos = np.zeros(len(POS))
    bigram = np.zeros((N, N))        # operator-trajectory: op_t -> op_{t+1}
    p = np.full(N, 1.0 / N)          # composition-walk state
    ops, known = [], 0
    for w in toks:
        e = _lookup(w)
        if e is None:
            continue
        known += 1
        o = int(e.get("o", 0))
        wt = _OPIDF[o]                # rare-operator emphasis
        occ[o] += wt
        ops.append(o)
        pi = e.get("p", "x")
        pos[POS.index(pi) if pi in POS else len(POS) - 1] += 1.0
        nxt = np.zeros(N)
        for i in range(N):
            if p[i] > 0:
                nxt[_T[i, o]] += p[i]
        s = nxt.sum()
        p = nxt / s if s > 0 else p
    for a, b in zip(ops, ops[1:]):   # the WALK the sentence traces
        bigram[a, b] += _OPIDF[a] * _OPIDF[b]
    cov = known / max(len(toks), 1)
    for v in (occ, pos):
        if v.sum() > 0:
            v /= v.sum()
    bg = bigram.flatten()
    if bg.sum() > 0:
        bg /= bg.sum()
    sigma_orbit = np.array([occ[0] + occ[3] + occ[8] + occ[9],
                            occ[1] + occ[2] + occ[4] + occ[5]
                            + occ[6] + occ[7]])
    return np.concatenate([occ, p, bg, sigma_orbit, pos, [cov]])  # 131 dims


def embed(texts):
    M = np.array([embed_one(t) for t in texts])
    return M, "native:ck_dictionary(%d words, walk-trajectory)" % len(FLAT)
