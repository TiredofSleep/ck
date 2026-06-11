"""board.py -- the 8x8 pathway board. Atoms become walks.

8 movers {1,2,3,4,5,6,8,9} are the board ranks/files; absorbers VOID(0)
and HARMONY(7) are the off-board resting squares. A letter is measured
to an operator (ord mod 10); a word is the TSML-composed WALK its letters
trace; its memory trace is the path's shape (64-cell move histogram +
where it landed + its sigma/CRT readings) -- the FORM pathway, computed
without ever consulting meaning.

CC-BY-4.0. Sanders + Claude. 2026-06-11.
"""
import os
import re
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ck_tables  # noqa: E402

N = 10
SIGMA = [0, 7, 1, 3, 2, 4, 5, 6, 8, 9]
MOVERS = [1, 2, 3, 4, 5, 6, 8, 9]            # the 8x8 board
MIDX = {o: k for k, o in enumerate(MOVERS)}   # operator -> board file 0..7
_T = np.array(ck_tables.TSML)


def letter_op(ch):
    """Atom measurement: a letter's operator. 'a'->1, 'b'->2, ... 'j'->0."""
    return (ord(ch) - ord('a') + 1) % N      # a=1..z=26, mod 10


def form_pathway(word):
    """Walk the word's letters through TSML; return FORM features (88-dim).
    Uses letters ONLY -- never the word's meaning."""
    seq = [letter_op(c) for c in word if c.isalpha()]
    if not seq:
        return np.zeros(88)
    board = np.zeros((8, 8))                   # 64 move cells
    footprint = np.zeros(N)                    # states visited
    p = np.full(N, 1.0 / N)
    prev_mover = None
    for op in seq:
        nxt = np.zeros(N)
        for i in range(N):
            if p[i] > 0:
                nxt[_T[i, op]] += p[i]         # compose: T(state_i, letter_op)
        s = nxt.sum()
        p = nxt / s if s > 0 else p
        footprint += p
        cur = int(np.argmax(p))
        if cur in MIDX and prev_mover is not None and prev_mover in MIDX:
            board[MIDX[prev_mover], MIDX[cur]] += 1.0
        prev_mover = cur
    fp = footprint / footprint.sum()
    bg = board.flatten()
    if bg.sum() > 0:
        bg /= bg.sum()
    sigma_orbit = np.array([p[0] + p[3] + p[8] + p[9],
                            p[1] + p[2] + p[4] + p[5] + p[6] + p[7]])
    final_arg = int(np.argmax(p))
    crt = np.array([final_arg % 2, final_arg % 5]) / 5.0     # binary/ternary face
    return np.concatenate([bg, p, fp, sigma_orbit, crt])     # 64+10+10+2+2 = 88


_word_re = re.compile(r"[a-z']+")


def form_pathway_text(text):
    """Mean form-pathway over the words of a text (for routing use)."""
    ws = _word_re.findall(text.lower())
    if not ws:
        return np.zeros(88)
    return np.mean([form_pathway(w) for w in ws], axis=0)
