"""braid_memory.py -- CK's memory as a fractal recursive braid, not a
flat board.

CORRECTION (Brayden 2026-06-11): "each cell of the 8x8 is not just an
integer, it is the representation of that integer in its zero form vs
its integer... it's a pathway, it's not static... it's a fractal
recursive braid pathway that stores memory."

So:
  * 8 strands = the board's movers; VOID(0)/HARMONY(7) are the ground
    rests (the "zero forms" a strand can rest in).
  * each letter is a CROSSING (braid generator sigma_s on strands s,s+1).
    Its OVER/UNDER -- the integer-vs-zero-form duality -- is the
    canonical binary face sigma^3 = (1 5)(2 6)(4 7): over for {1,2,4}
    (and fixed grounds), under for {5,6,7}. Not a static cell: a crossing.
  * a word is a BRAID WORD (sequence of signed crossings). Composition is
    concatenation; the braid's topological class is the memory.
  * FRACTAL RECURSION: the same braiding rule is applied at the letter
    scale AND the bigram scale (self-similar, depth 2).
  * the braid is read by its BURAU representation at the 10th root of
    unity t = e^{2 pi i /10} (the substrate modulus) -- a homomorphism
    B_8 -> GL_8(C), so composed braids = matrix products. The signature
    (trace phase = writhe, eigenvalue phases, norm) is robust to small
    edits: misspellings stay near the same braid class -> the DRIFT
    tolerance flat memory never had. (B_3 -> SL_2(Z): same modular world
    as J55.)

CC-BY-4.0. Sanders + Claude. 2026-06-11.
"""
import numpy as np

N = 8                                   # strands (the 8 movers)
SIGMA3_OVER = {1, 2, 4}                 # over-crossings (integer form)
SIGMA3_UNDER = {5, 6, 7}                # under-crossings (zero form)
T = np.exp(2j * np.pi / 10)             # Burau evaluation: substrate root


def _gen(site, sign):
    """Unreduced Burau matrix of sigma_site^{sign} on N strands.
    site in 0..N-2 acts on strands site, site+1."""
    M = np.eye(N, dtype=complex)
    if sign >= 0:                       # sigma_i : [[1-t, t],[1,0]]
        M[site, site] = 1 - T
        M[site, site + 1] = T
        M[site + 1, site] = 1
        M[site + 1, site + 1] = 0
    else:                               # sigma_i^{-1}: [[0,1],[1/t,1-1/t]]
        ti = 1.0 / T
        M[site, site] = 0
        M[site, site + 1] = 1
        M[site + 1, site] = ti
        M[site + 1, site + 1] = 1 - ti
    return M


def _letter_crossing(ch):
    """A letter -> (site on the 8-strand board, over/under sign, writhe)."""
    k = ord(ch) - ord('a')
    site = k % (N - 1)                  # which adjacent strand pair (0..6)
    op = (k + 1) % 10                   # its substrate operator
    if op in SIGMA3_UNDER:
        return site, -1, -1
    return site, +1, (+1 if op in SIGMA3_OVER else 0)   # fixed = ground


def op_crossing(op):
    """A substrate operator (0..9) -> crossing. Lets ANY atom that maps to
    operators -- letters, digits of a wavelength, phoneme codes -- braid by
    the SAME rule. site = op mod 7; over/under = sigma^3 binary face."""
    op = int(op) % 10
    site = op % (N - 1)
    if op in SIGMA3_UNDER:
        return site, -1, -1
    return site, +1, (+1 if op in SIGMA3_OVER else 0)


def _burau_word(crossings):
    M = np.eye(N, dtype=complex)
    writhe = 0
    for site, sign, w in crossings:
        M = M @ _gen(site, sign)
        writhe += w
    return M, writhe


def _sig(M, writhe):
    """Topological signature of a braid matrix: trace phase (writhe-like),
    |trace|, sorted eigenvalue phases, log-norm, det phase."""
    tr = np.trace(M)
    ev = np.linalg.eigvals(M)
    phases = np.sort(np.angle(ev))
    det = np.linalg.det(M)
    return np.concatenate([
        [np.abs(tr), np.angle(tr) / np.pi],
        phases / np.pi,                                  # 8
        [np.log1p(np.linalg.norm(M)), np.angle(det) / np.pi,
         writhe / 10.0],
    ])                                                   # 2 + 8 + 3 = 13


def _signature_from_crossings(L0):
    """Depth-2 FRACTAL Burau signature from a base crossing list. The
    shared core: letters, digits, and any atom-stream braid identically."""
    if not L0:
        L0 = [(0, 1, 0)]
    M0, w0 = _burau_word(L0)
    L1 = []                            # level 1: braid the bigrams (recursion)
    for a, b in zip(L0, L0[1:]):
        site = (a[0] + b[0] + 1) % (N - 1)
        L1.append((site, a[1] * b[1], a[2] + b[2]))
    M1, w1 = _burau_word(L1 if L1 else L0)
    return np.concatenate([_sig(M0, w0), _sig(M1, w1)])   # 26-dim


def braid_signature(word):
    """FRACTAL depth-2 braid signature of a word (letters)."""
    word = "".join(c for c in word.lower() if c.isalpha())
    if len(word) < 2:
        word = (word + "aa")[:2]
    return _signature_from_crossings([_letter_crossing(c) for c in word])


def braid_signature_ops(ops):
    """Braid signature of an OPERATOR stream (digits of a wavelength,
    phoneme codes, etc.) -- the SAME machinery as letters, different atom."""
    ops = list(ops)
    if len(ops) < 2:
        ops = (ops + [0, 0])[:2]
    return _signature_from_crossings([op_crossing(o) for o in ops])


def abelianized_key(word):
    """The order-FORGOTTEN braid invariant (H_1 of the braid): signed
    crossing count per site. Edit-stable -- a letter SWAP leaves it
    unchanged, a sub/del perturbs it by one crossing -- so it is the
    IDENTITY key for recall, complementing the order-sensitive Burau
    signature (the MEANING correlate). Two signatures, two jobs."""
    word = "".join(c for c in word.lower() if c.isalpha())
    exps = np.zeros(N - 1)                 # signed exponent sum per site
    counts = np.zeros(N - 1)               # |crossings| per site (unsigned)
    for c in word:
        site, sign, _ = _letter_crossing(c)
        exps[site] += sign
        counts[site] += 1.0
    return np.concatenate([exps, counts, [len(word)]])     # 15-dim


def text_signature(text):
    ws = [w for w in "".join(c if c.isalpha() else " "
                            for c in text.lower()).split() if w]
    if not ws:
        return np.zeros(26)
    return np.mean([braid_signature(w) for w in ws], axis=0)


class BraidMemory:
    """Stores words as braids; recalls by braid-class proximity. The
    topological signature makes recall robust to misspelling = drift."""

    def __init__(self):
        self.keys, self.raw = [], []
        self._mu = None
        self._sd = None

    def store(self, word, payload=None):
        self.keys.append((word, payload))
        # identity key = abelianized (edit-stable) + Burau signature
        # (meaning-rich); fused so recall uses both jobs' invariants.
        self.raw.append(np.concatenate([abelianized_key(word),
                                         braid_signature(word)]))
        self._mu = None                      # invalidate whitening cache

    def _whiten(self, v):
        # remove the common-mode (the 0.885 cone) + scale per dimension,
        # so recall discriminates braid CLASS, not the shared baseline.
        if self._mu is None:
            R = np.array(self.raw)
            self._mu = R.mean(0)
            self._sd = R.std(0) + 1e-9
        w = (v - self._mu) / self._sd
        return w / (np.linalg.norm(w) + 1e-9)

    def _vec(self, word):
        return np.concatenate([abelianized_key(word), braid_signature(word)])

    def recall(self, query, k=1):
        if not self.raw:
            return []
        W = np.array([self._whiten(r) for r in self.raw])
        q = self._whiten(self._vec(query))
        sims = W @ q
        order = np.argsort(sims)[::-1][:k]
        return [(self.keys[i][0], self.keys[i][1], float(sims[i]))
                for i in order]

    @property
    def sigs(self):                          # back-compat for the floor stat
        return [self._whiten(r) for r in self.raw]
