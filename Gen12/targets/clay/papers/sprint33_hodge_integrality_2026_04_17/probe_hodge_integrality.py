"""
SPRINT 33 — HODGE INTEGRALITY TEST ON W_*
==========================================

Sprint 32 earned a quantitative bound but did not close Beauville
rank >= 3 on A_*.  Memo section 7.1 identified the highest-payoff
next move:

    Test whether  W_* intersect Lambda^4 Z^8  is trivial.

If yes, Beauville rank >= 3 on A_* closes unconditionally (every
rational / integer Hodge class in W_* must vanish, hence every
Hodge class on A_* is K-invariant, hence algebraic by Sprint 29
Route R1-KE).

The subtlety:  Sprint 30 built  W_basis  as an 8-dim REAL nullspace
of  [C_anti ; C_22 ; C_prim]  via numerical SVD.  But C_22 has
entries in  Q(sqrt 2, sqrt 3, sqrt 5)  (from Y = sqrt2 I + sqrt3 M_2
+ sqrt5 M_3).  A vector  v in Q^70  satisfies  C_22 v = 0  over R
iff each of the 8 Q-components (in basis {1, s2, s3, s5, s6, s10,
s15, s30}) vanishes separately.  That is 8x more Q-constraints than
the naive R-constraint count.  The numerical 8-dim nullity of
C_stack does NOT imply an 8-dim Q-nullity.

METHOD (hybrid symbolic / numerical):
    1. Compute J_Omega numerically at 200-digit precision.
    2. Compute Lambda^4 J_Omega (70 x 70) as numerical 4x4 dets.
    3. PSLQ-decompose each entry in basis
           {1, s2, s3, s5, s6, s10, s15, s30}
       over Q; this yields 8 EXACT rational 70x70 matrices.
    4. Stack with C_anti (rational from phi) and C_prim (rational
       from polarization L) and compute rank over Q via sympy.
    5. Kernel dim = dim_Q ( W_* cap Lambda^4 Q^8 ).

(c) 2026 7Site LLC / Brayden Ross Sanders.  Sprint 33, 2026-04-17.
"""
from __future__ import annotations
import json
import sys
import time
from itertools import combinations
from pathlib import Path
from fractions import Fraction

import numpy as np
import sympy as sp
from mpmath import mp, mpf, matrix as mpm, sqrt as msqrt, pslq


# ----------------------------------------------------------------------
# 1. Shared integer data (exactly as Sprint 29 / 30)
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
H4_DIM = len(H4_BASIS)                        # 70
INDEX_OF = {t: k for k, t in enumerate(H4_BASIS)}
H2_BASIS = list(combinations(range(8), 2))
IDX2 = {t: k for k, t in enumerate(H2_BASIS)}
H6_BASIS = list(combinations(range(8), 6))
IDX6 = {t: k for k, t in enumerate(H6_BASIS)}


# ----------------------------------------------------------------------
# 2. Lambda^4 phi as an exact integer 70x70 matrix  (gives C_anti over Z)
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
print(f"[1] Lambda^4 phi  shape {PHI_STAR_4.shape},  max|entry|={np.abs(PHI_STAR_4).max()}")


# ----------------------------------------------------------------------
# 3. Polarization L : H^4 -> H^6 (integer 28 x 70)
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
print(f"[2] L: H^4->H^6  shape {L_H4_H6.shape},  rank={np.linalg.matrix_rank(L_H4_H6)}")


# ----------------------------------------------------------------------
# 4. Build J_Omega at high mpmath precision
# ----------------------------------------------------------------------

mp.dps = 200
print(f"[3] Setting mpmath precision to {mp.dps} decimal digits.")

def build_J_Omega_mpmath():
    s2m, s3m, s5m = msqrt(2), msqrt(3), msqrt(5)
    # Y = s2 I + s3 M2 + s5 M3
    Y = mpm(4, 4)
    for i in range(4):
        for j in range(4):
            v = mpf(0)
            if i == j:
                v += s2m
            v += s3m * int(M2_INT[i, j])
            v += s5m * int(M3_INT[i, j])
            Y[i, j] = v
    # X = 0.5 I
    X = mpm(4, 4)
    for i in range(4):
        X[i, i] = mpf('0.5')
    Yi = Y ** -1
    YiX = Yi * X
    XYi = X * Yi
    XYiX = X * Yi * X
    bl = Y + XYiX
    J = mpm(8, 8)
    for i in range(4):
        for j in range(4):
            J[i, j]         = YiX[i, j]
            J[i, j + 4]     = -Yi[i, j]
            J[i + 4, j]     = bl[i, j]
            J[i + 4, j + 4] = -XYi[i, j]
    return J


t0 = time.time()
J_MP = build_J_Omega_mpmath()
print(f"[3] J_Omega (mpmath {mp.dps} dp) built in {time.time()-t0:.2f}s")

# Sanity: J^2 should equal -I
t0 = time.time()
J2 = J_MP * J_MP
err = max(abs(J2[i, j] - (mpf(-1) if i == j else mpf(0)))
          for i in range(8) for j in range(8))
print(f"[3] ||J^2 + I||_inf = {float(err):.2e}   (should be ~0; time {time.time()-t0:.1f}s)")
assert float(err) < mpf(10) ** (-100)


# ----------------------------------------------------------------------
# 5. Compute Lambda^4 J_Omega as 70x70 numerical matrix
# ----------------------------------------------------------------------

def mpm_det4(M):
    """Determinant of a 4x4 mpmath matrix via permutation expansion."""
    # 24 terms; simple explicit formula (safe numerically at 200 dp).
    a, b, c, d = (M[0, 0], M[0, 1], M[0, 2], M[0, 3])
    e, f, g, h = (M[1, 0], M[1, 1], M[1, 2], M[1, 3])
    i, j, k, l = (M[2, 0], M[2, 1], M[2, 2], M[2, 3])
    m, n, o, p = (M[3, 0], M[3, 1], M[3, 2], M[3, 3])
    return (
        a*(f*(k*p - l*o) - g*(j*p - l*n) + h*(j*o - k*n))
      - b*(e*(k*p - l*o) - g*(i*p - l*m) + h*(i*o - k*m))
      + c*(e*(j*p - l*n) - f*(i*p - l*m) + h*(i*n - j*m))
      - d*(e*(j*o - k*n) - f*(i*o - k*m) + g*(i*n - j*m))
    )


def submatrix_mp(M, rows, cols):
    Q = mpm(len(rows), len(cols))
    for r, rr in enumerate(rows):
        for c, cc in enumerate(cols):
            Q[r, c] = M[rr, cc]
    return Q


print("[4] Computing Lambda^4 J_Omega (70x70 numerical dets) ...")
J_STAR_4_MP = mpm(H4_DIM, H4_DIM)
t0 = time.time()
for col, I in enumerate(H4_BASIS):
    B = submatrix_mp(J_MP, list(range(8)), list(I))   # 8 x 4
    for row, J in enumerate(H4_BASIS):
        sub = submatrix_mp(B, list(J), list(range(4)))  # 4 x 4
        J_STAR_4_MP[row, col] = mpm_det4(sub)
print(f"[4] Lambda^4 J_Omega computed in {time.time()-t0:.1f}s")


# ----------------------------------------------------------------------
# 6. PSLQ-decompose each entry in Q-basis of Q(s2, s3, s5)
#    Basis: {1, s2, s3, s5, s6, s10, s15, s30}
# ----------------------------------------------------------------------

K_BASIS_MP = [
    mpf(1), msqrt(2), msqrt(3), msqrt(5),
    msqrt(6), msqrt(10), msqrt(15), msqrt(30),
]
K_BASIS_LABEL = ['1', 's2', 's3', 's5', 's6', 's10', 's15', 's30']
NK = len(K_BASIS_MP)


def decompose_pslq(x):
    """Return list of 8 sympy.Rational c_k with x == sum c_k * K_BASIS_MP[k]
       up to numerical tolerance.  Returns None on failure."""
    # PSLQ: find integer relation among [x, b_0, b_1, ..., b_7]
    # i.e. integers n_x, n_0, ..., n_7 with n_x * x + sum n_k * b_k ~= 0
    # then x = -(1/n_x) * sum n_k * b_k  => c_k = -n_k / n_x.
    if abs(x) < mpf(10) ** (-180):
        return [sp.Integer(0)] * NK
    vec = [x] + list(K_BASIS_MP)
    try:
        rel = pslq(vec, tol=mpf(10) ** (-150), maxcoeff=10**40, maxsteps=2000)
    except Exception:
        return None
    if rel is None:
        return None
    n_x = rel[0]
    if n_x == 0:
        return None
    return [sp.Rational(-rel[k + 1], n_x) for k in range(NK)]


print("[5] PSLQ-decomposing 4900 entries in K-basis ...")
C22_RAT = [np.empty((H4_DIM, H4_DIM), dtype=object) for _ in range(NK)]
for k in range(NK):
    for i in range(H4_DIM):
        for j in range(H4_DIM):
            C22_RAT[k][i, j] = sp.Integer(0)

t0 = time.time()
fail_count = 0
progress_every = max(1, H4_DIM // 20)
for i in range(H4_DIM):
    for j in range(H4_DIM):
        x = J_STAR_4_MP[i, j]
        # sanity: at zero
        if abs(x) < mpf(10) ** (-150):
            continue
        coeffs = decompose_pslq(x)
        if coeffs is None:
            fail_count += 1
            continue
        for k in range(NK):
            if coeffs[k] != 0:
                C22_RAT[k][i, j] = coeffs[k]
    if (i + 1) % progress_every == 0:
        print(f"    row {i+1}/{H4_DIM}  ({100.0*(i+1)/H4_DIM:5.1f}%)  "
              f"elapsed={time.time()-t0:.0f}s   fails={fail_count}")

print(f"[5] PSLQ decomposition done in {time.time()-t0:.1f}s;  failures={fail_count}")
if fail_count > 0:
    print(f"    WARNING: {fail_count} PSLQ failures — treat verdict with caution.")


# ----------------------------------------------------------------------
# 7. Sanity-reconstruct:  verify  sum_k C22_k * K_BASIS_MP[k]  matches J_STAR_4_MP
# ----------------------------------------------------------------------
print("[6] Reconstruction sanity check ...")
max_recon_err = mpf(0)
for i in range(H4_DIM):
    for j in range(H4_DIM):
        s = mpf(0)
        for k in range(NK):
            c = C22_RAT[k][i, j]
            if c != 0:
                s += mpf(str(sp.Rational(c).p)) / mpf(str(sp.Rational(c).q)) * K_BASIS_MP[k]
        d = abs(J_STAR_4_MP[i, j] - s)
        if d > max_recon_err:
            max_recon_err = d
print(f"[6] max |entry - reconstruction| = {float(max_recon_err):.3e}")
assert float(max_recon_err) < 1e-100, "reconstruction mismatch — PSLQ failed somewhere"


# ----------------------------------------------------------------------
# 8. C_22 over Q decomposes as (J_STAR_4 - I) = sum_k C22_k * b_k
#    The rational piece (k=0) picks up the -I:  C22_0 := C22_RAT[0] - I.
# ----------------------------------------------------------------------
C22_RAT[0] = C22_RAT[0] - np.eye(H4_DIM, dtype=object)
# Clean up (-0 weirdness)
for k in range(NK):
    for i in range(H4_DIM):
        for j in range(H4_DIM):
            C22_RAT[k][i, j] = sp.Rational(C22_RAT[k][i, j])


# ----------------------------------------------------------------------
# 9. Stack all rational constraints and compute rank over Q
# ----------------------------------------------------------------------

print("[7] Stacking rational constraint matrix ...")

def np_obj_to_sympy(M):
    return sp.Matrix([[sp.Rational(M[i, j]) for j in range(M.shape[1])]
                      for i in range(M.shape[0])])

C_anti_sym = sp.Matrix(PHI_STAR_4.tolist()) + sp.eye(H4_DIM)        # 70 x 70
C_prim_sym = sp.Matrix(L_H4_H6.tolist())                            # 28 x 70
C22_sym_list = [np_obj_to_sympy(C22_RAT[k]) for k in range(NK)]     # 8 * (70 x 70)

C_STACK = sp.Matrix.vstack(C_anti_sym, C_prim_sym, *C22_sym_list)
print(f"[7] stacked shape: {C_STACK.shape}")

# Pre-filter zero rows for speed
nonzero_rows = [i for i in range(C_STACK.rows)
                if any(C_STACK[i, j] != 0 for j in range(H4_DIM))]
C_STACK_nz = C_STACK.extract(nonzero_rows, list(range(H4_DIM)))
print(f"[7] nonzero rows: {C_STACK_nz.rows} (dropped {C_STACK.rows - C_STACK_nz.rows} zero rows)")

print("[8] Computing rank over Q ...")
t0 = time.time()
rank = C_STACK_nz.rank()
kernel_dim = H4_DIM - rank
print(f"[8] rank_Q = {rank}   (dt = {time.time()-t0:.1f}s)")
print(f"[8] dim_Q ( W_* cap Lambda^4 Q^8 ) = {kernel_dim}")


# ----------------------------------------------------------------------
# 10. Verdict
# ----------------------------------------------------------------------

verdict = {
    "sprint": 33,
    "test": "W_* intersect Lambda^4 Q^8 rigorous rationality check",
    "variety": "A_* = C^4 / (Z^4 + Omega Z^4),  End^0 = Q(i)",
    "mpmath_precision_digits": mp.dps,
    "pslq_failure_count": fail_count,
    "reconstruction_max_err": float(max_recon_err),
    "numerical_W_basis_R_dim": 8,
    "rational_W_star_Q_dim": int(kernel_dim),
    "rank_over_Q_of_full_constraint_system": int(rank),
    "constraint_rows_total": int(C_STACK.rows),
    "constraint_rows_nonzero": int(C_STACK_nz.rows),
    "closure_of_beauville_rank_ge_3_on_A_star":
        "CLOSED UNCONDITIONALLY" if kernel_dim == 0 else f"OPEN (residual Q-dim {kernel_dim})",
    "field_basis_used": K_BASIS_LABEL,
}

if kernel_dim == 0:
    print("\n" + "=" * 72)
    print("VERDICT:  W_*  intersect  Q^70  =  {0}")
    print("  => every rational Hodge class on A_* is K-invariant")
    print("  => every rational Hodge class on A_* is algebraic (Sprint 29 R1-KE)")
    print("  => Beauville residual (rank >= 3) CLOSES on A_* unconditionally.")
    print("=" * 72)
else:
    print("\n" + "=" * 72)
    print(f"VERDICT:  W_*  intersect  Q^70  has Q-dimension {kernel_dim}.")
    print("  => residual rational Hodge classes survive the integrality test.")
    print("  => Beauville residual remains open on A_*; see kernel basis.")
    print("=" * 72)

out_path = Path(__file__).with_name("sprint33_verdict.json")
out_path.write_text(json.dumps(verdict, indent=2))
print(f"\nVerdict written to {out_path.name}")
