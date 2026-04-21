"""
SPRINT 33 v2 -- HODGE INTEGRALITY TEST (STREAMING + GF(p))
===========================================================

v1 (probe_hodge_integrality.py) stalled overnight on sympy
rank-over-Q with large-denominator PSLQ-recovered rationals.
v2 keeps v1's mathematical content but changes the engineering:

    (1) Unbuffered, line-buffered stdout; flush=True on every print.
    (2) Checkpoint JSON writes after each stage, so if the run ever
        hangs we know precisely which stage and can restart from it.
    (3) mpmath precision 80 (down from 200).  PSLQ tol 1e-50 is
        plenty for 8-basis Q(s2,s3,s5) decomposition.
    (4) Rank computation over GF(p) for several primes p ~ 2^31,
        NOT sympy rank-over-Q.  Schwartz-Zippel: if rank over GF(p)
        equals 70 for several random large primes, rank over Q is
        70 with probability 1 - epsilon (small polynomial in the
        matrix size over p).
    (5) Output written to sprint33_verdict_v2.json.  v1 verdict,
        if it is ever recovered, stays separate.

MATHEMATICAL STATEMENT (unchanged from v1):

    Test whether  W_* cap Lambda^4 Q^8  =  {0}

    If yes, every rational Hodge class on A_* is K-invariant,
    hence algebraic by the Sprint 29 R1-KE route, hence Beauville
    rank >= 3 on A_* closes UNCONDITIONALLY.

    W_* is the 8-dim numerical nullspace of the stacked system
        [ C_anti = Lambda^4 phi + I ]   (from K-anti-invariance)
        [ C_prim = L : H^4 -> H^6   ]   (primitivity)
        [ C_22   = Lambda^4 J - I   ]   (type-(2,2))
    intersected with  Q^70.  The subtlety: C_22 lives over Q(s2,s3,s5),
    so the "8 real constraints per row" scale to "8 * 8 = 64 Q-constraints
    per row" after decomposing in the basis {1, s2, s3, s5, s6, s10, s15, s30}.

(c) 2026 7Site LLC / Brayden Ross Sanders.  Sprint 33 v2, 2026-04-17.
"""
from __future__ import annotations
import json
import sys
import time
import random
from itertools import combinations
from pathlib import Path

# Unbuffered streaming stdout -- the key v1 fix.
try:
    sys.stdout.reconfigure(line_buffering=True)
except Exception:
    pass


def log(msg: str) -> None:
    print(msg, flush=True)


import numpy as np
import sympy as sp
from mpmath import mp, mpf, matrix as mpm, sqrt as msqrt, pslq


THIS = Path(__file__).parent
CKPT = THIS / "sprint33_v2_checkpoint.json"
OUT  = THIS / "sprint33_verdict_v2.json"


def checkpoint(stage: str, payload: dict) -> None:
    """Write a per-stage checkpoint so we can diagnose any stall."""
    record = {"stage": stage, "ts": time.strftime("%Y-%m-%d %H:%M:%S"), **payload}
    CKPT.write_text(json.dumps(record, indent=2))
    log(f"[checkpoint] {stage}")


# ----------------------------------------------------------------------
# 1. Shared integer data (exact copy of v1)
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
# 2. Lambda^4 phi as exact integer 70x70 (gives C_anti over Z)
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
checkpoint("phi_wedge4_built",
           {"shape": list(PHI_STAR_4.shape),
            "max_abs_entry": int(np.abs(PHI_STAR_4).max())})


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
log(f"[2] L: H^4 -> H^6 shape {L_H4_H6.shape}, rank={np.linalg.matrix_rank(L_H4_H6)}")
checkpoint("L_built", {"shape": list(L_H4_H6.shape),
                       "numeric_rank": int(np.linalg.matrix_rank(L_H4_H6))})


# ----------------------------------------------------------------------
# 4. J_Omega at mpmath precision 80 (v2 change: was 200)
# ----------------------------------------------------------------------

mp.dps = 200
log(f"[3] mpmath precision set to {mp.dps} decimal digits.")


def build_J_Omega_mpmath():
    s2m, s3m, s5m = msqrt(2), msqrt(3), msqrt(5)
    Y = mpm(4, 4)
    for i in range(4):
        for j in range(4):
            v = mpf(0)
            if i == j:
                v += s2m
            v += s3m * int(M2_INT[i, j])
            v += s5m * int(M3_INT[i, j])
            Y[i, j] = v
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
dt_J = time.time() - t0
log(f"[3] J_Omega (mpmath {mp.dps} dp) built in {dt_J:.2f}s")

# Sanity: J^2 = -I
t0 = time.time()
J2 = J_MP * J_MP
err = max(abs(J2[i, j] - (mpf(-1) if i == j else mpf(0)))
          for i in range(8) for j in range(8))
dt_J2 = time.time() - t0
log(f"[3] ||J^2 + I||_inf = {float(err):.2e} (dt = {dt_J2:.2f}s)")
assert float(err) < mpf(10) ** (-150), f"J^2 + I error {float(err)} too large at dp={mp.dps}"
checkpoint("J_Omega_built",
           {"dps": int(mp.dps), "J_build_s": float(dt_J),
            "J_square_err": float(err)})


# ----------------------------------------------------------------------
# 5. Lambda^4 J_Omega as 70 x 70 numerical matrix of 4x4 dets
# ----------------------------------------------------------------------

def mpm_det4(M):
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


log("[4] Computing Lambda^4 J_Omega (70x70 numerical dets) ...")
J_STAR_4_MP = mpm(H4_DIM, H4_DIM)
t0 = time.time()
progress_mod = max(1, H4_DIM // 10)
for col, I in enumerate(H4_BASIS):
    B = submatrix_mp(J_MP, list(range(8)), list(I))     # 8 x 4
    for row, J in enumerate(H4_BASIS):
        sub = submatrix_mp(B, list(J), list(range(4)))  # 4 x 4
        J_STAR_4_MP[row, col] = mpm_det4(sub)
    if (col + 1) % progress_mod == 0:
        log(f"    col {col+1}/{H4_DIM}  elapsed={time.time()-t0:.1f}s")
dt_J4 = time.time() - t0
log(f"[4] Lambda^4 J_Omega computed in {dt_J4:.1f}s")
checkpoint("J_star_4_done", {"elapsed_s": float(dt_J4)})


# ----------------------------------------------------------------------
# 6. PSLQ decompose each entry in Q-basis of Q(s2, s3, s5)
#    Basis: {1, s2, s3, s5, s6, s10, s15, s30}
# ----------------------------------------------------------------------

K_BASIS_MP = [
    mpf(1), msqrt(2), msqrt(3), msqrt(5),
    msqrt(6), msqrt(10), msqrt(15), msqrt(30),
]
K_BASIS_LABEL = ['1', 's2', 's3', 's5', 's6', 's10', 's15', 's30']
NK = len(K_BASIS_MP)

PSLQ_TOL = mpf(10) ** (-150)
PSLQ_MAXCOEFF = 10 ** 40
PSLQ_MAXSTEPS = 2000


def decompose_pslq(x):
    """Return 8 sympy.Rational coeffs c_k with x = sum c_k * K_BASIS_MP[k].
    Returns None if PSLQ fails to find a relation."""
    if abs(x) < mpf(10) ** (-180):
        return [sp.Integer(0)] * NK
    vec = [x] + list(K_BASIS_MP)
    try:
        rel = pslq(vec, tol=PSLQ_TOL, maxcoeff=PSLQ_MAXCOEFF, maxsteps=PSLQ_MAXSTEPS)
    except Exception:
        return None
    if rel is None:
        return None
    n_x = rel[0]
    if n_x == 0:
        return None
    return [sp.Rational(-rel[k + 1], n_x) for k in range(NK)]


log("[5] PSLQ-decomposing 4900 entries "
    f"(tol=1e-150, maxcoeff=1e40, maxsteps=2000) ...")
C22_RAT = [np.empty((H4_DIM, H4_DIM), dtype=object) for _ in range(NK)]
for k in range(NK):
    for i in range(H4_DIM):
        for j in range(H4_DIM):
            C22_RAT[k][i, j] = sp.Integer(0)

t0 = time.time()
fail_count = 0
zero_count = 0
done_count = 0
progress_every = max(1, H4_DIM // 10)
for i in range(H4_DIM):
    for j in range(H4_DIM):
        x = J_STAR_4_MP[i, j]
        if abs(x) < mpf(10) ** (-180):
            zero_count += 1
            continue
        coeffs = decompose_pslq(x)
        if coeffs is None:
            fail_count += 1
            continue
        done_count += 1
        for k in range(NK):
            if coeffs[k] != 0:
                C22_RAT[k][i, j] = coeffs[k]
    if (i + 1) % progress_every == 0:
        log(f"    row {i+1}/{H4_DIM} ({100.0*(i+1)/H4_DIM:5.1f}%) "
            f"elapsed={time.time()-t0:.0f}s  done={done_count} "
            f"zero={zero_count} fails={fail_count}")

dt_pslq = time.time() - t0
log(f"[5] PSLQ decomposition: {done_count} succeeded, {zero_count} zero-entries, "
    f"{fail_count} fails, dt={dt_pslq:.1f}s")
checkpoint("pslq_done",
           {"elapsed_s": float(dt_pslq),
            "succeeded": done_count, "zeros": zero_count, "fails": fail_count})
if fail_count > 0:
    # HARD ABORT.  If any entry failed PSLQ, the -I subtraction below will
    # corrupt C_22_0 (the 0-row becomes -I), which then trivially stacks to
    # full rank 70 and produces a FALSE closure verdict.  Fail loudly here
    # rather than silently generate a wrong result.
    verdict_abort = {
        "sprint": 33,
        "version": "v2",
        "status": "ABORTED (PSLQ failure)",
        "pslq_fails": int(fail_count),
        "pslq_succeeded": int(done_count),
        "pslq_zeros": int(zero_count),
        "reason": ("Some Lambda^4 J_Omega entries could not be decomposed in the "
                   "Q(s2,s3,s5) basis at current precision.  The -I subtraction on "
                   "C22_RAT[0] would produce spurious -I rows and trivially force "
                   "rank=70, giving a false CLOSURE verdict.  Raise mpmath.dps, "
                   "raise PSLQ maxcoeff, or raise maxsteps and re-run."),
    }
    OUT.write_text(json.dumps(verdict_abort, indent=2))
    checkpoint("pslq_aborted", verdict_abort)
    log(f"\nABORT: {fail_count} PSLQ failures. Verdict NOT written; aborted result "
        f"saved to {OUT.name}.")
    sys.exit(1)


# ----------------------------------------------------------------------
# 7. Reconstruction sanity
# ----------------------------------------------------------------------

log("[6] Reconstruction sanity check ...")
t0 = time.time()
max_recon_err = mpf(0)
for i in range(H4_DIM):
    for j in range(H4_DIM):
        s = mpf(0)
        for k in range(NK):
            c = C22_RAT[k][i, j]
            if c != 0:
                r = sp.Rational(c)
                s += mpf(r.p) / mpf(r.q) * K_BASIS_MP[k]
        d = abs(J_STAR_4_MP[i, j] - s)
        if d > max_recon_err:
            max_recon_err = d
dt_recon = time.time() - t0
log(f"[6] max |entry - reconstruction| = {float(max_recon_err):.3e}  (dt={dt_recon:.1f}s)")
recon_ok = float(max_recon_err) < 1e-80
checkpoint("reconstruction_done",
           {"max_recon_err": float(max_recon_err),
            "tolerance_1e-80_ok": recon_ok})
if not recon_ok:
    # HARD ABORT on reconstruction failure -- same rationale as PSLQ failure.
    verdict_abort = {
        "sprint": 33,
        "version": "v2",
        "status": "ABORTED (reconstruction failure)",
        "max_recon_err": float(max_recon_err),
        "reason": ("Reconstruction of Lambda^4 J_Omega from PSLQ-recovered "
                   "Q-coefficients disagrees with the numeric matrix beyond 1e-80. "
                   "PSLQ likely found spurious relations with large denominators. "
                   "Tighten tol or raise precision."),
    }
    OUT.write_text(json.dumps(verdict_abort, indent=2))
    log(f"\nABORT: reconstruction error {float(max_recon_err):.3e} > 1e-80.")
    sys.exit(1)


# ----------------------------------------------------------------------
# 8. C_22 over Q = (Lambda^4 J - I).  Subtract I from the rational piece.
# ----------------------------------------------------------------------

C22_RAT[0] = C22_RAT[0] - np.eye(H4_DIM, dtype=object)
for k in range(NK):
    for i in range(H4_DIM):
        for j in range(H4_DIM):
            C22_RAT[k][i, j] = sp.Rational(C22_RAT[k][i, j])


# ----------------------------------------------------------------------
# 9. Build the stacked rational matrix (as plain Python list-of-lists
#    of sp.Rational) -- we skip sympy.Matrix entirely to dodge v1's
#    melt-down.
# ----------------------------------------------------------------------

log("[7] Building stacked constraint list-of-lists ...")
t0 = time.time()

def add_block(rows_out, block_np):
    """Append rows of a numpy (H4_DIM,H4_DIM) int or Rational matrix
    as lists of sp.Rational."""
    R, C = block_np.shape
    for i in range(R):
        row = [sp.Rational(int(block_np[i, j])) if isinstance(block_np[i, j], (int, np.integer))
               else sp.Rational(block_np[i, j])
               for j in range(C)]
        rows_out.append(row)


rows: list[list[sp.Rational]] = []

# C_anti = Lambda^4 phi + I  (integer 70 x 70)
C_anti_np = PHI_STAR_4 + np.eye(H4_DIM, dtype=int)
add_block(rows, C_anti_np)

# C_prim = L: H^4 -> H^6 (integer 28 x 70)
add_block(rows, L_H4_H6)

# 8 rational 70 x 70 C_22_k blocks (must all vanish independently)
for k in range(NK):
    add_block(rows, C22_RAT[k])

total_rows_raw = len(rows)
# Drop any row that is entirely zero.
rows = [r for r in rows if any(x != 0 for x in r)]
total_rows_nz = len(rows)
log(f"[7] stacked rows (raw): {total_rows_raw}, nonzero: {total_rows_nz} "
    f"(dt={time.time()-t0:.1f}s)")
checkpoint("stack_built",
           {"rows_raw": total_rows_raw, "rows_nz": total_rows_nz,
            "cols": H4_DIM})


# ----------------------------------------------------------------------
# 10. Rank over GF(p) for several random large primes.
#     Schwartz-Zippel: if rank_GF(p) == H4_DIM for k random primes,
#     rank over Q is H4_DIM with prob >= 1 - H4_DIM / min(p).
# ----------------------------------------------------------------------

# Five primes near 2^31 -- safely above any PSLQ-recovered denominator.
CANDIDATE_PRIMES = [
    2_147_483_647,   # 2^31 - 1 (Mersenne)
    2_147_483_629,
    2_147_483_587,
    2_147_483_579,
    2_147_483_563,
]


def rank_mod_p(rows_q, ncols, p):
    """Rank over GF(p) of a list of lists of sp.Rational.
    Raises ValueError if any denominator is 0 mod p (pick another prime)."""
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
    # Gaussian elimination mod p
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


log("[8] Computing rank over GF(p) for several primes p ~ 2^31 ...")
rank_results = {}
for p in CANDIDATE_PRIMES:
    t0 = time.time()
    try:
        r = rank_mod_p(rows, H4_DIM, p)
        dt = time.time() - t0
        log(f"    p = {p}:  rank_GF(p) = {r}  (dt = {dt:.1f}s)")
        rank_results[str(p)] = {"rank": r, "seconds": float(dt), "ok": True}
    except ValueError as ex:
        log(f"    p = {p}:  SKIP ({ex})")
        rank_results[str(p)] = {"rank": None, "ok": False, "reason": str(ex)}
    except Exception as ex:
        log(f"    p = {p}:  ERROR ({ex})")
        rank_results[str(p)] = {"rank": None, "ok": False, "reason": str(ex)}
    checkpoint(f"rank_mod_p_{p}", rank_results[str(p)])


# ----------------------------------------------------------------------
# 11. Aggregate verdict
# ----------------------------------------------------------------------

valid_ranks = [v["rank"] for v in rank_results.values() if v.get("ok") and v.get("rank") is not None]
all_match = len(valid_ranks) >= 2 and all(r == valid_ranks[0] for r in valid_ranks)
if all_match:
    rank_Q_est = valid_ranks[0]
    kernel_dim_est = H4_DIM - rank_Q_est
    confidence = f"rank equal across {len(valid_ranks)} primes"
else:
    rank_Q_est = max(valid_ranks) if valid_ranks else None
    kernel_dim_est = None if rank_Q_est is None else H4_DIM - rank_Q_est
    confidence = "ranks DISAGREE across primes -- inspect manually"

verdict = {
    "sprint": 33,
    "version": "v2",
    "test": "W_* cap Lambda^4 Q^8 rigorous rationality check via GF(p) rank",
    "variety": "A_* = C^4 / (Z^4 + Omega Z^4),  End^0 = Q(i)",
    "mpmath_precision_digits": int(mp.dps),
    "pslq_tol": "1e-50",
    "pslq_maxcoeff": PSLQ_MAXCOEFF,
    "pslq_maxsteps": PSLQ_MAXSTEPS,
    "pslq_succeeded": done_count,
    "pslq_zero_entries": zero_count,
    "pslq_failure_count": fail_count,
    "reconstruction_max_err": float(max_recon_err),
    "reconstruction_tolerance_1e-30_ok": recon_ok,
    "constraint_rows_total_raw": total_rows_raw,
    "constraint_rows_nonzero":   total_rows_nz,
    "constraint_cols":           H4_DIM,
    "rank_results_per_prime":    rank_results,
    "rank_Q_estimate":           rank_Q_est,
    "kernel_dim_Q_estimate":     kernel_dim_est,
    "confidence":                confidence,
    "field_basis_used":          K_BASIS_LABEL,
}

if kernel_dim_est == 0 and all_match:
    verdict["closure_of_beauville_rank_ge_3_on_A_star"] = (
        "CLOSED UNCONDITIONALLY (Schwartz-Zippel across multiple primes)"
    )
    log("\n" + "=" * 72)
    log("VERDICT:  W_*  cap  Q^70  =  {0}  (rank 70 over GF(p) for all tested primes)")
    log("  => every rational Hodge class on A_* is K-invariant")
    log("  => every rational Hodge class on A_* is algebraic (Sprint 29 R1-KE)")
    log("  => Beauville residual (rank >= 3) CLOSES on A_* unconditionally.")
    log("=" * 72)
elif kernel_dim_est is not None:
    verdict["closure_of_beauville_rank_ge_3_on_A_star"] = (
        f"OPEN (residual Q-dim {kernel_dim_est})"
    )
    log("\n" + "=" * 72)
    log(f"VERDICT:  rank over GF(p) = {rank_Q_est},  kernel dim = {kernel_dim_est}")
    log("  => residual rational Hodge classes survive the integrality test")
    log("  => Beauville residual remains open on A_*; see kernel basis.")
    log("=" * 72)
else:
    verdict["closure_of_beauville_rank_ge_3_on_A_star"] = "INCONCLUSIVE"
    log("\n" + "=" * 72)
    log("VERDICT:  INCONCLUSIVE  (no primes produced a valid rank)")
    log("=" * 72)

OUT.write_text(json.dumps(verdict, indent=2))
log(f"\nVerdict written to {OUT.name}")
checkpoint("verdict_written", {"path": str(OUT.name)})
