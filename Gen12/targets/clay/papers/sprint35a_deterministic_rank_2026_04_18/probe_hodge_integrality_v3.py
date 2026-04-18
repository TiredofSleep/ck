"""
SPRINT 35a v3 -- HODGE INTEGRALITY, DETERMINISTIC RANK
========================================================

v2 (probe_hodge_integrality_v2.py) gave rank = 70 at 5 primes near 2^31
via PSLQ-reconstructed rationals in Q(s2, s3, s5).  Verdict:
CLOSED UNCONDITIONALLY (probabilistic Schwartz-Zippel certificate,
~10^-40).  S33 Gate 1-full audit (S33_CONSTRUCTION_AUDIT.md section 6)
flagged the sole rigor gap: PSLQ reconstruction fidelity.  v3 closes
that gap by skipping PSLQ entirely and doing EXACT algebraic arithmetic
in Q(s2, s3, s5) via a custom 8-tuple class.

DETERMINISTIC CLAIM (proved in this file, no probability):

    Let M be the stacked constraint matrix
        [ C_anti = Lambda^4 phi + I              ] (70 rows,  Z)
        [ C_prim = L : H^4 -> H^6                ] (28 rows,  Z)
        [ C_22   = Lambda^4 J - I, each basis k  ] (8 * 70 rows,  Q)
    viewed over Q, with 70 columns.  If rank(M mod p) = 70 for ONE
    prime p not dividing any denominator of M, then
    rank(M over Q) = 70 deterministically.

PROOF:  Let c = lcm of all denominators in M, so cM in Z^(nxm).  Pick
p not dividing c.  Then (cM mod p) has rank equal to (M mod p) (since c
is invertible mod p).  Any r x r minor of cM mod p that is nonzero mod
p is nonzero as an integer, hence nonzero over Q.  So
rank(cM over Q) >= rank(cM mod p) = rank(M mod p).  Since M has 70
columns, rank(M over Q) <= 70.  Single-prime certificate suffices.  QED.

NEW IN v3 vs v2:

    (1) Q235 class:  exact element of Q(s2, s3, s5) as 8-tuple of
        sympy.Rational in basis {1, s2, s3, s5, s6, s10, s15, s30}.
    (2) Exact Y, Y^-1, and J_Omega built over Q235 -- no mpmath.
    (3) Exact Lambda^4 J_Omega as 70x70 matrix of Q235 elements
        (each entry is a 4x4 determinant, exact).
    (4) Each Q235 entry of C_22 decomposes into 8 Q-rows; stack gives
        a 658 x 70 rational matrix.
    (5) Explicit denominator bound:  lcm of denominators in M.  Any
        prime > this bound and not dividing it is a "good prime".
    (6) Rank over GF(p) at 20+ primes.  One good prime with rank 70
        suffices; 20 is overkill for deterministic confirmation.

(c) 2026 7Site LLC / Brayden Ross Sanders.  Sprint 35a, 2026-04-18.
"""
from __future__ import annotations
import json
import sys
import time
from itertools import combinations
from pathlib import Path

try:
    sys.stdout.reconfigure(line_buffering=True)
except Exception:
    pass

def log(msg: str) -> None:
    print(msg, flush=True)


import numpy as np
import sympy as sp


THIS = Path(__file__).parent
CKPT = THIS / "sprint35a_v3_checkpoint.json"
OUT  = THIS / "sprint35a_verdict_v3.json"


def checkpoint(stage: str, payload: dict) -> None:
    record = {"stage": stage, "ts": time.strftime("%Y-%m-%d %H:%M:%S"), **payload}
    CKPT.write_text(json.dumps(record, indent=2))
    log(f"[checkpoint] {stage}")


# ----------------------------------------------------------------------
# 0.  Q235 class -- exact arithmetic in Q(s2, s3, s5)
# ----------------------------------------------------------------------
#
# Basis:  index i in {0..7} encodes (a,b,c) in {0,1}^3 via bits of i:
#   bit 0 (i & 1)   = exponent of s5
#   bit 1 (i & 2)   = exponent of s3
#   bit 2 (i & 4)   = exponent of s2
# So:
#   i=0 (000) = 1
#   i=1 (001) = s5
#   i=2 (010) = s3
#   i=3 (011) = s15
#   i=4 (100) = s2
#   i=5 (101) = s10
#   i=6 (110) = s6
#   i=7 (111) = s30
#
# Multiplication:  (i) * (j) = (i XOR j) with coefficient mult_table[i][j]
# where mult_table handles the 2/3/5 factors from colliding bits.

_BIT_VAL = (2, 3, 5)  # bit 0 -> 5, bit 1 -> 3, bit 2 -> 2.  Wait, check:
# Actually, bit 0 is s5 (from above).  Bit 1 is s3.  Bit 2 is s2.
# So if both i, j have bit k set, they contribute _BIT_VAL[k] factor on squaring.
# Let's redefine clearly:
#   bit 0 of i: factor s5 present in basis element i
#   bit 1 of i: factor s3 present in basis element i
#   bit 2 of i: factor s2 present in basis element i
# Squaring s5 -> 5, s3 -> 3, s2 -> 2.
_SQUARE_FACTOR = {0: 5, 1: 3, 2: 2}


def _mult_coeff(i: int, j: int) -> int:
    """Integer factor when basis-i * basis-j is reduced to basis-(i XOR j)."""
    coeff = 1
    for bit in range(3):
        if (i >> bit) & 1 and (j >> bit) & 1:
            coeff *= _SQUARE_FACTOR[bit]
    return coeff


# Precompute 8x8 multiplication table: (i, j) -> (target_index, coeff)
_MULT_TABLE = [[( (i ^ j), _mult_coeff(i, j)) for j in range(8)] for i in range(8)]

_LABEL = ['1', 's5', 's3', 's15', 's2', 's10', 's6', 's30']


class Q235:
    """Exact element of Q(sqrt 2, sqrt 3, sqrt 5) as 8-tuple of sp.Rational."""
    __slots__ = ('c',)

    def __init__(self, coeffs=None):
        if coeffs is None:
            self.c = [sp.Integer(0)] * 8
        elif isinstance(coeffs, (int, sp.Integer, sp.Rational)):
            self.c = [sp.Rational(coeffs)] + [sp.Integer(0)] * 7
        else:
            assert len(coeffs) == 8
            self.c = [sp.Rational(x) for x in coeffs]

    @classmethod
    def zero(cls):
        return cls()

    @classmethod
    def one(cls):
        out = cls()
        out.c[0] = sp.Integer(1)
        return out

    @classmethod
    def s2(cls):
        out = cls()
        out.c[4] = sp.Integer(1)  # bit 2 = s2
        return out

    @classmethod
    def s3(cls):
        out = cls()
        out.c[2] = sp.Integer(1)  # bit 1 = s3
        return out

    @classmethod
    def s5(cls):
        out = cls()
        out.c[1] = sp.Integer(1)  # bit 0 = s5
        return out

    @classmethod
    def from_int(cls, n: int):
        out = cls()
        out.c[0] = sp.Integer(n)
        return out

    @classmethod
    def from_rat(cls, p, q=1):
        out = cls()
        out.c[0] = sp.Rational(p, q)
        return out

    def is_zero(self):
        return all(ci == 0 for ci in self.c)

    def __add__(self, other):
        if isinstance(other, (int, sp.Integer, sp.Rational)):
            other = Q235.from_rat(other)
        out = Q235()
        for k in range(8):
            out.c[k] = self.c[k] + other.c[k]
        return out

    def __sub__(self, other):
        if isinstance(other, (int, sp.Integer, sp.Rational)):
            other = Q235.from_rat(other)
        out = Q235()
        for k in range(8):
            out.c[k] = self.c[k] - other.c[k]
        return out

    def __neg__(self):
        out = Q235()
        for k in range(8):
            out.c[k] = -self.c[k]
        return out

    def __mul__(self, other):
        if isinstance(other, (int, sp.Integer, sp.Rational)):
            other = Q235.from_rat(other)
        out = Q235()
        sc = self.c
        oc = other.c
        for i in range(8):
            si = sc[i]
            if si == 0:
                continue
            for j in range(8):
                oj = oc[j]
                if oj == 0:
                    continue
                tgt, coeff = _MULT_TABLE[i][j]
                out.c[tgt] += si * oj * coeff
        return out

    __radd__ = __add__
    __rsub__ = lambda self, other: (-self) + other
    __rmul__ = __mul__

    def __repr__(self):
        parts = []
        for k, ck in enumerate(self.c):
            if ck != 0:
                parts.append(f"{ck}*{_LABEL[k]}")
        return "Q235(" + " + ".join(parts) + ")" if parts else "Q235(0)"

    def norm_Q(self):
        """Field norm N: Q(s2,s3,s5) -> Q.  Product over 8 Galois conjugates,
        computed exactly in Q235 (basis elements multiply, not numerically
        collapse).  Result has only basis-0 coefficient nonzero."""
        N = Q235.one()
        for sign_bits in range(8):
            conj = Q235()
            for k in range(8):
                if self.c[k] == 0:
                    continue
                sign = 1
                for bit in range(3):
                    if (k >> bit) & 1 and (sign_bits >> bit) & 1:
                        sign = -sign
                conj.c[k] = sign * self.c[k]
            N = N * conj
        # Product of Galois orbit is rational (basis-0 only)
        assert all(N.c[k] == 0 for k in range(1, 8)), \
            f"Norm is not rational: {N}"
        return N.c[0]


# Sanity check the Q235 arithmetic
def _selftest_Q235():
    s2 = Q235.s2()
    s3 = Q235.s3()
    s5 = Q235.s5()
    assert (s2 * s2).c[0] == 2, "s2^2 should be 2"
    assert (s2 * s3).c[6] == 1, "s2*s3 should be s6"
    # Check s6 * s10 = s60 = 2*s15
    s6 = s2 * s3
    s10 = s2 * s5
    prod = s6 * s10
    assert prod.c[3] == 2, f"s6*s10 should be 2*s15, got {prod}"
    # Check (1 + s2)(1 - s2) = 1 - 2 = -1
    a = Q235.one() + s2
    b = Q235.one() - s2
    c = a * b
    assert c.c[0] == -1, f"(1+s2)(1-s2) = -1, got {c}"
    assert all(c.c[k] == 0 for k in range(1, 8)), f"(1+s2)(1-s2) should be rational, got {c}"
    log("  Q235 arithmetic self-test: PASS")


_selftest_Q235()


# ----------------------------------------------------------------------
# 1. Shared integer data (same as v1 / v2)
# ----------------------------------------------------------------------

def build_phi8_int():
    phi4 = np.zeros((4, 4), dtype=int)
    phi4[1, 0] = 1; phi4[0, 1] = -1
    phi4[3, 2] = -1; phi4[2, 3] = 1
    out = np.zeros((8, 8), dtype=int)
    out[:4, :4] = phi4; out[4:, 4:] = phi4
    return out


PHI8_INT = build_phi8_int()
M2_INT = np.array([[3, 0, 1, 1], [0, 3, 1, -1], [1, 1, 2, 0], [1, -1, 0, 2]], dtype=int)
M3_INT = np.array([[5, 0, 0, 2], [0, 5, 2, 0], [0, 2, 1, 0], [2, 0, 0, 1]], dtype=int)

H4_BASIS = list(combinations(range(8), 4))
H4_DIM = len(H4_BASIS)
INDEX_OF = {t: k for k, t in enumerate(H4_BASIS)}
H2_BASIS = list(combinations(range(8), 2))
IDX2 = {t: k for k, t in enumerate(H2_BASIS)}
H6_BASIS = list(combinations(range(8), 6))
IDX6 = {t: k for k, t in enumerate(H6_BASIS)}


# ----------------------------------------------------------------------
# 2.  Lambda^4 phi exact (integer)
# ----------------------------------------------------------------------

def wedge_k_integer(A_int: np.ndarray, k: int):
    bs = list(combinations(range(8), k))
    n = len(bs)
    M = np.zeros((n, n), dtype=np.int64)
    for col, I in enumerate(bs):
        B = A_int[:, list(I)]
        for row, J in enumerate(bs):
            sub = B[list(J), :]
            d = int(round(np.linalg.det(sub)))
            if abs(d) > 0:
                M[row, col] = d
    return M


PHI_STAR_4 = wedge_k_integer(PHI8_INT, 4)
log(f"[1] Lambda^4 phi shape {PHI_STAR_4.shape}, max|entry|={np.abs(PHI_STAR_4).max()}")


# ----------------------------------------------------------------------
# 3.  Polarization L : H^4 -> H^6  (integer 28 x 70)
# ----------------------------------------------------------------------

def build_L_matrix_H4_to_H6():
    L = np.zeros((len(H6_BASIS), H4_DIM), dtype=int)
    for col, I in enumerate(H4_BASIS):
        Iset = set(I)
        for j in range(4):
            pair = (j, 4 + j)
            if pair[0] in Iset or pair[1] in Iset:
                continue
            combined = sorted(set(I) | set(pair))
            if len(combined) != 6:
                continue
            seq = list(pair) + list(I)
            sign = 1
            for a in range(len(seq)):
                for b in range(a + 1, len(seq)):
                    if seq[a] > seq[b]:
                        sign = -sign
            L[IDX6[tuple(combined)], col] += sign
    return L


L_H4_H6 = build_L_matrix_H4_to_H6()
log(f"[2] L: H^4 -> H^6 shape {L_H4_H6.shape}")


# ----------------------------------------------------------------------
# 4.  Build Y, X, Y^-1 over Q235 exactly
# ----------------------------------------------------------------------

log("[3] Building Y (4x4) exactly over Q(s2,s3,s5) ...")
Y = [[Q235() for _ in range(4)] for _ in range(4)]
for i in range(4):
    for j in range(4):
        v = Q235()
        if i == j:
            v = v + Q235.s2()
        v = v + Q235.s3() * int(M2_INT[i, j])
        v = v + Q235.s5() * int(M3_INT[i, j])
        Y[i][j] = v

# X = (1/2) I_4
X = [[Q235() for _ in range(4)] for _ in range(4)]
for i in range(4):
    X[i][i] = Q235.from_rat(1, 2)


# Exact 4x4 determinant of a list-of-lists of Q235
def det4_Q235(M):
    a, b, c, d = M[0]
    e, f, g, h = M[1]
    i, j, k, l = M[2]
    m, n, o, p = M[3]
    return (
        a*(f*(k*p - l*o) - g*(j*p - l*n) + h*(j*o - k*n))
      - b*(e*(k*p - l*o) - g*(i*p - l*m) + h*(i*o - k*m))
      + c*(e*(j*p - l*n) - f*(i*p - l*m) + h*(i*n - j*m))
      - d*(e*(j*o - k*n) - f*(i*o - k*m) + g*(i*n - j*m))
    )


log("[3] Computing det(Y) over Q235 ...")
t0 = time.time()
detY = det4_Q235(Y)
dt = time.time() - t0
log(f"    det(Y) = {detY}  (dt={dt:.2f}s)")

# Norm of det(Y): Q-rational number, equals product over 8 Galois conjugates
log("[3] Computing N(det Y) ...")
NdetY = detY.norm_Q()
log(f"    N(det Y) = {NdetY}   (type: {type(NdetY).__name__})")

# 1/det(Y) = (product of 7 non-identity Galois conjugates of detY) / N(detY)
# We multiply detY by each of its 7 non-trivial Galois conjugates and divide by N.

def galois_conj(q: Q235, sign_bits: int) -> Q235:
    """Apply Galois automorphism: s2 -> (-1)^bit2 s2, s3 -> (-1)^bit1 s3, s5 -> (-1)^bit0 s5."""
    out = Q235()
    for k in range(8):
        if q.c[k] == 0:
            continue
        sign = 1
        for bit in range(3):
            if (k >> bit) & 1 and (sign_bits >> bit) & 1:
                sign = -sign
        out.c[k] = sign * q.c[k]
    return out


log("[3] Computing det(Y)^-1 via Galois-conjugate product / N ...")
t0 = time.time()
inv_numer = Q235.one()
for sb in range(1, 8):
    inv_numer = inv_numer * galois_conj(detY, sb)
# Divide by N(detY)
inv_detY = Q235()
for k in range(8):
    inv_detY.c[k] = sp.Rational(inv_numer.c[k], NdetY)
# Sanity: inv_detY * detY = 1
check = inv_detY * detY
assert check.c[0] == 1 and all(check.c[k] == 0 for k in range(1, 8)), \
    f"detY * inv_detY != 1, got {check}"
log(f"    det(Y)^-1 built and verified  (dt={time.time()-t0:.2f}s)")


# Adjugate of 4x4: classical cofactor expansion
def minor3_Q235(M, skip_row, skip_col):
    rows = [r for r in range(4) if r != skip_row]
    cols = [c for c in range(4) if c != skip_col]
    sub = [[M[r][c] for c in cols] for r in rows]
    a, b, c = sub[0]
    d, e, f = sub[1]
    g, h, i = sub[2]
    return a*(e*i - f*h) - b*(d*i - f*g) + c*(d*h - e*g)


log("[3] Computing adj(Y) (16 cofactors) ...")
t0 = time.time()
adjY = [[Q235() for _ in range(4)] for _ in range(4)]
for i in range(4):
    for j in range(4):
        sign = 1 if (i + j) % 2 == 0 else -1
        cof = minor3_Q235(Y, i, j)  # minor(i,j)
        if sign == -1:
            cof = -cof
        adjY[j][i] = cof  # note transpose: adj = (cofactor)^T
log(f"    adj(Y) computed  (dt={time.time()-t0:.2f}s)")

log("[3] Y^-1 = adj(Y) / det(Y) ...")
t0 = time.time()
Yi = [[adjY[i][j] * inv_detY for j in range(4)] for i in range(4)]
# Sanity: Y * Yi = I
log("    Verifying Y * Y^-1 = I ...")
for i in range(4):
    for j in range(4):
        s = Q235()
        for k in range(4):
            s = s + Y[i][k] * Yi[k][j]
        expected = 1 if i == j else 0
        assert s.c[0] == expected, f"Y*Yi[{i},{j}] = {s}, expected {expected}"
        assert all(s.c[k] == 0 for k in range(1, 8)), f"Y*Yi[{i},{j}] = {s}, non-rational!"
log(f"    Y * Y^-1 = I verified  (dt={time.time()-t0:.2f}s)")
checkpoint("Y_inverted", {"elapsed_s": float(time.time() - t0)})


# ----------------------------------------------------------------------
# 5.  Build J_Omega over Q235 exactly
# ----------------------------------------------------------------------

log("[4] Building J_Omega as 8x8 Q235 matrix ...")
t0 = time.time()

# YiX = Y^-1 * X, XYi = X * Y^-1, XYiX = X * Y^-1 * X
def matmul4_Q235(A, B):
    out = [[Q235() for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            s = Q235()
            for k in range(4):
                s = s + A[i][k] * B[k][j]
            out[i][j] = s
    return out


YiX = matmul4_Q235(Yi, X)
XYi = matmul4_Q235(X, Yi)
XYiX = matmul4_Q235(X, matmul4_Q235(Yi, X))

J_OMEGA = [[Q235() for _ in range(8)] for _ in range(8)]
for i in range(4):
    for j in range(4):
        J_OMEGA[i][j]         = YiX[i][j]
        J_OMEGA[i][j + 4]     = -Yi[i][j]
        J_OMEGA[i + 4][j]     = Y[i][j] + XYiX[i][j]
        J_OMEGA[i + 4][j + 4] = -XYi[i][j]

dt = time.time() - t0
log(f"    J_Omega built  (dt={dt:.2f}s)")

# Sanity: J^2 = -I
log("[4] Verifying J_Omega^2 = -I ...")
t0 = time.time()
for i in range(8):
    for j in range(8):
        s = Q235()
        for k in range(8):
            s = s + J_OMEGA[i][k] * J_OMEGA[k][j]
        expected = -1 if i == j else 0
        assert s.c[0] == expected, f"J^2[{i},{j}] rational part = {s.c[0]}, expected {expected}"
        assert all(s.c[k] == 0 for k in range(1, 8)), f"J^2[{i},{j}] has non-rational part: {s}"
log(f"    J_Omega^2 = -I verified EXACTLY  (dt={time.time()-t0:.2f}s)")
checkpoint("J_Omega_exact", {"elapsed_s": float(time.time() - t0)})


# ----------------------------------------------------------------------
# 6.  Compute Lambda^4 J_Omega as 70 x 70 matrix of Q235 (exact)
# ----------------------------------------------------------------------

log(f"[5] Computing Lambda^4 J_Omega (exact, {H4_DIM}x{H4_DIM} = {H4_DIM*H4_DIM} dets) ...")

def submatrix_Q235(M, rows, cols):
    return [[M[r][c] for c in cols] for r in rows]


t0 = time.time()
J_STAR_4 = [[Q235() for _ in range(H4_DIM)] for _ in range(H4_DIM)]
progress_mod = max(1, H4_DIM // 10)
for col, I in enumerate(H4_BASIS):
    # B: 8x4 submatrix (all rows, cols I)
    B = submatrix_Q235(J_OMEGA, list(range(8)), list(I))
    for row, J in enumerate(H4_BASIS):
        # sub: 4x4 (rows J of B, all 4 cols)
        sub = submatrix_Q235(B, list(J), list(range(4)))
        J_STAR_4[row][col] = det4_Q235(sub)
    if (col + 1) % progress_mod == 0:
        log(f"    col {col+1}/{H4_DIM}  elapsed={time.time()-t0:.1f}s")
dt_J4 = time.time() - t0
log(f"[5] Lambda^4 J_Omega (exact) computed in {dt_J4:.1f}s")
checkpoint("J_star_4_exact", {"elapsed_s": float(dt_J4)})


# ----------------------------------------------------------------------
# 7.  C_22 = Lambda^4 J - I.  Subtract I from basis-0 (rational) coefficient.
# ----------------------------------------------------------------------

log("[6] Subtracting I from C_22 basis-0 ...")
C22 = [[J_STAR_4[i][j] for j in range(H4_DIM)] for i in range(H4_DIM)]
for i in range(H4_DIM):
    # subtract 1 from basis-0 of diagonal
    C22[i][i] = C22[i][i] - 1


# ----------------------------------------------------------------------
# 8.  Build stacked constraint matrix over Q.
#     Each Q235 entry of C_22 contributes 8 Q-rows (one per basis element).
# ----------------------------------------------------------------------

log("[7] Building stacked Q-matrix ...")
t0 = time.time()

rows_Q = []  # list of tuples (p_list, q_list) where entries are sp.Rational

# C_anti = Lambda^4 phi + I  (integer 70x70)
C_anti_np = PHI_STAR_4 + np.eye(H4_DIM, dtype=int)
for i in range(H4_DIM):
    row = [sp.Rational(int(C_anti_np[i, j])) for j in range(H4_DIM)]
    if any(x != 0 for x in row):
        rows_Q.append(row)

# C_prim = L: H^4 -> H^6  (integer 28x70)
for i in range(L_H4_H6.shape[0]):
    row = [sp.Rational(int(L_H4_H6[i, j])) for j in range(H4_DIM)]
    if any(x != 0 for x in row):
        rows_Q.append(row)

# C_22: 8 blocks of 70 rows (one per Q235 basis element).
# For each basis index k, row i contributes row of c[k] components.
for k in range(8):
    for i in range(H4_DIM):
        row = [C22[i][j].c[k] for j in range(H4_DIM)]
        if any(x != 0 for x in row):
            rows_Q.append(row)

total_rows = len(rows_Q)
log(f"[7] stacked rows (nonzero): {total_rows}, cols: {H4_DIM}  (dt={time.time()-t0:.1f}s)")
checkpoint("stack_built_v3",
           {"rows_nz": total_rows, "cols": H4_DIM,
            "elapsed_s": float(time.time() - t0)})


# ----------------------------------------------------------------------
# 9.  Denominator bound: find all denominators that appear, compute their LCM.
# ----------------------------------------------------------------------

log("[8] Computing denominator LCM ...")
t0 = time.time()
den_lcm = sp.Integer(1)
for row in rows_Q:
    for q in row:
        d = q.q
        if d != 1:
            den_lcm = sp.lcm(den_lcm, d)
_den_bits = int(den_lcm).bit_length()
log(f"    denominator LCM has {_den_bits} bits  (den_lcm type: {type(den_lcm).__name__})")
log(f"    (good primes: any prime not dividing this; primes > den_lcm are automatically good)")
checkpoint("den_lcm", {"den_lcm_bits": _den_bits,
                       "elapsed_s": float(time.time() - t0)})


# ----------------------------------------------------------------------
# 10.  Rank over GF(p) for 20 primes near 2^31 (all > den_lcm).
# ----------------------------------------------------------------------

CANDIDATE_PRIMES = [
    2147483647, 2147483629, 2147483587, 2147483579, 2147483563,
    2147483549, 2147483543, 2147483497, 2147483489, 2147483477,
    2147483423, 2147483399, 2147483353, 2147483323, 2147483269,
    2147483249, 2147483237, 2147483179, 2147483171, 2147483137,
]


def rank_mod_p(rows_q, ncols, p):
    nrows = len(rows_q)
    A = np.zeros((nrows, ncols), dtype=np.int64)
    for i, row in enumerate(rows_q):
        for j, q in enumerate(row):
            num = int(q.p)
            den = int(q.q)
            if den % p == 0:
                raise ValueError(f"prime p={p} divides denominator at ({i},{j})")
            den_inv = pow(den % p, -1, p)
            A[i, j] = ((num % p) * den_inv) % p
    rp = 0
    for col in range(ncols):
        if rp >= nrows:
            break
        pivot = -1
        for r in range(rp, nrows):
            if A[r, col] != 0:
                pivot = r
                break
        if pivot == -1:
            continue
        if pivot != rp:
            A[[rp, pivot]] = A[[pivot, rp]]
        inv = pow(int(A[rp, col]), -1, p)
        A[rp] = (A[rp].astype(object) * inv % p).astype(np.int64)
        for r in range(nrows):
            if r != rp and A[r, col] != 0:
                factor = int(A[r, col])
                A[r] = ((A[r].astype(object) - factor * A[rp].astype(object)) % p).astype(np.int64)
        rp += 1
    return rp


log("[9] Computing rank over GF(p) for 20 primes near 2^31 ...")
rank_results = {}
for p in CANDIDATE_PRIMES:
    t0 = time.time()
    try:
        r = rank_mod_p(rows_Q, H4_DIM, p)
        dt = time.time() - t0
        log(f"    p = {p}:  rank_GF(p) = {r}  (dt = {dt:.1f}s)")
        rank_results[str(p)] = {"rank": r, "seconds": float(dt), "ok": True}
    except ValueError as ex:
        log(f"    p = {p}:  SKIP ({ex})")
        rank_results[str(p)] = {"rank": None, "ok": False, "reason": str(ex)}
    except Exception as ex:
        log(f"    p = {p}:  ERROR ({ex})")
        rank_results[str(p)] = {"rank": None, "ok": False, "reason": str(ex)}


# ----------------------------------------------------------------------
# 11.  Aggregate verdict -- single good prime with rank 70 is deterministic
# ----------------------------------------------------------------------

valid_ranks = [v["rank"] for v in rank_results.values()
               if v.get("ok") and v.get("rank") is not None]
max_rank = max(valid_ranks) if valid_ranks else None
all_match = len(valid_ranks) > 0 and all(r == valid_ranks[0] for r in valid_ranks)

any_good_prime_full_rank = any(v.get("ok") and v.get("rank") == H4_DIM
                               for v in rank_results.values())

verdict = {
    "sprint": "35a",
    "version": "v3",
    "test": ("Deterministic rank over Q for  W_* cap Q^70  via exact Q(s2,s3,s5) "
             "construction of Lambda^4 J_Omega (no PSLQ)."),
    "variety": "A_* = C^4 / (Z^4 + Omega Z^4),  End^0 = Q(i)",
    "exact_arithmetic": "Q235 (8-tuple over Q in basis {1,s2,s3,s5,s6,s10,s15,s30})",
    "pslq_used": False,
    "J_square_verified_exactly": True,
    "denominator_lcm_bits": int(int(den_lcm).bit_length()),
    "constraint_rows_nonzero": total_rows,
    "constraint_cols": H4_DIM,
    "n_primes_tested": len(CANDIDATE_PRIMES),
    "rank_results_per_prime": rank_results,
    "max_rank_observed": max_rank,
    "all_primes_agree": all_match,
    "deterministic_rank_claim":
        ("rank(M over Q) = H4_DIM = 70, deterministically: since at least one "
         "good prime p (not dividing any denominator) gave rank(M mod p) = 70, "
         "and rank-mod-p is always <= rank-over-Q, we have rank(M over Q) >= 70; "
         "combined with M having only 70 columns, rank(M over Q) = 70 exactly."
         if any_good_prime_full_rank else
         "NOT ESTABLISHED -- no good prime produced rank = 70."),
    "kernel_dim_Q": (H4_DIM - max_rank) if max_rank is not None else None,
}

if any_good_prime_full_rank and max_rank == H4_DIM:
    verdict["closure_verdict"] = "CLOSED DETERMINISTICALLY"
    verdict["implication"] = (
        "W_* cap Q^70 = {0}  =>  every rational Hodge class on A_* is "
        "K-invariant, hence algebraic by S29 R1-KE, hence Beauville rank >= 3 "
        "closes on A_* with DETERMINISTIC rigor (no probabilistic step)."
    )
    log("\n" + "=" * 72)
    log("VERDICT (DETERMINISTIC):")
    log("  W_*  cap  Q^70  =  {0}")
    log("  rank over Q = 70 proved via single-good-prime mod-p rank")
    log("  => every rational Hodge class on A_* is K-invariant")
    log("  => every rational Hodge class on A_* is algebraic (S29 R1-KE)")
    log("  => Beauville rank >= 3 CLOSES on A_* DETERMINISTICALLY.")
    log("=" * 72)
else:
    verdict["closure_verdict"] = "NOT CLOSED"
    log("\n" + "=" * 72)
    log(f"VERDICT:  rank {max_rank} < {H4_DIM}, or no good prime.")
    log("=" * 72)

OUT.write_text(json.dumps(verdict, indent=2))
log(f"\nVerdict written to {OUT.name}")
checkpoint("verdict_v3_written", {"path": str(OUT.name)})
