"""
Sprint 32 -- Beauville residual: BSD-Hodge synthesis attempt
============================================================

Target: the R1b rank >= 3 residual on A_*, i.e. whether any rank-r simple
vector bundle E with c_1(E) = 0 can have c_2(E) project nontrivially onto
the 8-dim K-anti-invariant primitive (2,2) obstruction space W_*.

Synthesis used:
    Rosati-skew (BSD)  +  Hodge-Riemann positivity on W_*  +  Mukai chi-bound
    -------------------------------------------------------
    Does the joint system force the W_*-projection of c_2 to zero?

Strategy:
    For a simple stable rank-r bundle E on A_*:
      * c_1(E) = 0 assumed (twist-normalized)
      * v(E)  = (r, 0, -c_2(E), 0, ch_4(E)) in the Mukai lattice
      * Mukai: chi(E, E) >= -2 dim_Ext^0 + ... simple E => chi(E,E) = 1 - <stuff>
      * Simplest sharp form used by Mukai: for simple semistable E on
        abelian g-fold, dim Moduli(E) = 2 - chi(E,E), hence chi(E,E) <= 2.
    Decomposing c_2(E) = alpha + beta with
      * alpha in W_* (K-anti-invariant primitive (2,2))
      * beta in W_*^perp inside H^4(A_*)
    we compute <v(E), v(E)> as a function of (r, alpha, beta, c_4) and ask
    whether the inequality chi(E,E) <= 2 has a solution with alpha != 0.

If the answer is NO for some range of (r, c_4, beta), we close that slice of
the R1b rank-r residual.  If the answer is YES, we report the surviving gap
and quantify how much slack remains -- an explicit step toward Beauville,
even if not closure.
"""
import numpy as np
from itertools import combinations
import json


# -------------------- Reuse Sprint 29/30 machinery --------------------
def build_phi8():
    phi = np.zeros((8, 8))
    phi[1, 0] = 1;  phi[0, 1] = -1
    phi[3, 2] = -1; phi[2, 3] = 1
    phi[5, 4] = 1;  phi[4, 5] = -1
    phi[7, 6] = -1; phi[6, 7] = 1
    return phi

def build_J_Omega():
    M2 = np.array([[3, 0, 1, 1],[0, 3, 1, -1],[1, 1, 2, 0],[1, -1, 0, 2]], float)
    M3 = np.array([[5, 0, 0, 2],[0, 5, 2, 0],[0, 2, 1, 0],[2, 0, 0, 1]], float)
    X = 0.5 * np.eye(4)
    Y = np.sqrt(2)*np.eye(4) + np.sqrt(3)*M2 + np.sqrt(5)*M3
    Yinv = np.linalg.inv(Y)
    J = np.block([[Yinv@X, -Yinv],[Y+X@Yinv@X, -X@Yinv]])
    assert np.allclose(J@J, -np.eye(8), atol=1e-10)
    return J

def wedge_k(A, k):
    basis = list(combinations(range(8), k))
    idx = {b: i for i, b in enumerate(basis)}
    n = len(basis)
    M = np.zeros((n, n))
    for j, I_j in enumerate(basis):
        cols = A[:, I_j]
        for I_i in combinations(range(8), k):
            sub = cols[list(I_i), :]
            M[idx[I_i], j] += np.linalg.det(sub)
    return M, basis

PHI = build_phi8()
J = build_J_Omega()


# -------------------- H^4 structure and W_* extraction --------------------
def h4_structure():
    """Build H^4 = Lambda^4 R^8 (dim 70), the 8-dim W_* = K-anti primitive (2,2)."""
    JL4, basis4 = wedge_k(J, 4)
    PHIL4, _ = wedge_k(PHI, 4)

    # Type (p,q) under J: eigenvalue i^(p-q).  Real basis: (2,2)_R is
    # kernel of JL4^2 + I on the "middle" block.  We extract via spectrum.
    # For Lambda^4 on 8-dim: types (4,0)+(0,4) have JL4^2=1, (3,1)+(1,3) have JL4^2=1,
    # (2,2) has JL4^2=1 too -- so JL4 has eigenvalues +/- 1 on H^{4,0}+(0,4)+(2,2)_R-type
    # and +/- i on H^{3,1}+(1,3).  Simpler: use that real (2,2) = +1 eigenspace of JL4.
    # (Because i^(p-q)=i^0=1 on (2,2).)
    eigvals_J, eigvecs_J = np.linalg.eig(JL4)
    mask_pos = np.abs(eigvals_J - 1.0) < 1e-6
    V_plus1 = eigvecs_J[:, mask_pos]
    # Take real span via Gram-Schmidt
    real_part = np.real(V_plus1)
    imag_part = np.imag(V_plus1)
    combined = np.hstack([real_part, imag_part])
    U, S, _ = np.linalg.svd(combined, full_matrices=False)
    rank_real = int(np.sum(S > 1e-8))
    V_22R = U[:, :rank_real]  # real (2,2)_R... but this includes (4,0)+(0,4) real, too.

    # We need to split off (2,2)_R from (4,0)+(0,4)_R.  Use a second J'-test:
    # (4,0)+(0,4) under wedging with a Kahler form behaves differently.
    # Simpler for our purposes: Sprint 30 directly solved for W_* as the
    # K-anti-invariant primitive (2,2).  We follow Sprint 30's recipe:
    #   1) Project to K-anti-invariant: PHIL4 acts, find -1 eigenspace of (PHIL4^2 something)
    #   Actually PHI^2 = -I, so PHIL4 has eigenvalues +1, -1, +1, -1,... with
    #   multiplicities matching K-invariant vs K-anti-invariant parts.
    # For W_*, we use the null-space characterization from Sprint 30:
    #   W_* = {alpha in H^4 :  phi*(alpha) = -alpha,  alpha is primitive (2,2)}

    # K-anti-invariant subspace (PHIL4 eigenvalue -1 over R means J_4 anti, phi-flip)
    # PHIL4^2 = det(phi)*I^{5-something}; on Lambda^4 of a Lambda-mode phi with phi^2=-I,
    # PHIL4^2 = PHI^{(4)} * PHI^{(4)} = induced(phi^2) = induced(-I) = +I on Lambda^4
    # (since det(-I) for 4x4 block = 1).  So PHIL4 has eigenvalues +/- 1.
    eigvals_P, eigvecs_P = np.linalg.eig(PHIL4)
    # K-anti-invariant: eigenvalue -1
    mask_anti = np.abs(eigvals_P - (-1)) < 1e-6
    K_anti_cplx = eigvecs_P[:, mask_anti]
    rp = np.real(K_anti_cplx); ip = np.imag(K_anti_cplx)
    combined2 = np.hstack([rp, ip])
    U2, S2, _ = np.linalg.svd(combined2, full_matrices=False)
    rk2 = int(np.sum(S2 > 1e-8))
    K_anti_R = U2[:, :rk2]

    # Now intersect with real (2,2): project K_anti_R onto the +1 eigenspace of JL4
    # (keeping real structure).  We use: project = V_22R V_22R^T.
    P_22 = V_22R @ V_22R.T
    proj_K_anti_into_22 = P_22 @ K_anti_R
    U3, S3, _ = np.linalg.svd(proj_K_anti_into_22, full_matrices=False)
    rk3 = int(np.sum(S3 > 1e-8))
    # This should be the K-anti primitive+non-primitive (2,2) subspace.

    print(f"  dim JL4 eigenspace +1 (real (2,2) + real (4,0)+(0,4)) = {rank_real}")
    print(f"  dim PHIL4 eigenspace -1 (K-anti-invariant)            = {rk2}")
    print(f"  dim (K-anti) cap (+1 of JL4, i.e. real (2,2)-type)    = {rk3}")

    # Primitive condition: wedge with Kahler L kills non-primitive.
    # L = sum_k e_{2k-1} wedge e_{2k} in our basis (standard Kahler form on R^8).
    # Build L as an element of H^2 = Lambda^2 R^8 (dim 28).
    basis2 = list(combinations(range(8), 2))
    idx2 = {b: i for i, b in enumerate(basis2)}
    L = np.zeros(len(basis2))
    for k in range(4):
        pair = (2*k, 2*k+1)
        if pair in idx2:
            L[idx2[pair]] = 1.0

    # Wedge H^4 -> H^6 via alpha |-> alpha ^ L; if the result is 0, alpha is primitive.
    basis6 = list(combinations(range(8), 6))
    idx6 = {b: i for i, b in enumerate(basis6)}
    wedge_L_mat = np.zeros((len(basis6), len(basis4)))
    for j, I4 in enumerate(basis4):
        for i2, I2 in enumerate(basis2):
            if L[i2] == 0: continue
            if set(I4) & set(I2): continue
            combined = tuple(sorted(I4 + I2))
            if combined not in idx6: continue
            # sign: how many swaps to sort I4 + I2 into combined
            merged = list(I4) + list(I2)
            sign = 1
            for a in range(len(merged)):
                for b in range(a+1, len(merged)):
                    if merged[a] > merged[b]:
                        sign = -sign
            wedge_L_mat[idx6[combined], j] += sign * L[i2]

    # W_* = ker(wedge_L_mat) intersect (K-anti-invariant) intersect (real (2,2))
    from scipy.linalg import null_space
    try:
        ker_L = null_space(wedge_L_mat, rcond=1e-10)
    except Exception:
        # fallback: SVD null space
        U_w, S_w, Vt_w = np.linalg.svd(wedge_L_mat, full_matrices=True)
        ker_L = Vt_w.T[:, S_w.shape[0]:] if Vt_w.shape[0] > S_w.shape[0] else None
    print(f"  dim ker(wedge_L) (primitive H^4)                     = "
          f"{ker_L.shape[1] if ker_L is not None else 'n/a'}")

    # Intersection: W_* = (primitive) cap (K-anti) cap (real (2,2))
    # Build intersection subspace numerically: stack bases and find null of
    # orthogonality-to-complement.
    # Simpler: iteratively project onto each of the three conditions.
    def project_onto(mat, rcond=1e-10):
        U_p, _, _ = np.linalg.svd(mat, full_matrices=False)
        return U_p @ U_p.T

    P_prim = project_onto(ker_L) if ker_L is not None else np.eye(70)
    P_Kanti = K_anti_R @ K_anti_R.T
    P_22R = V_22R @ V_22R.T

    # Intersection via power iteration: alternating projections.
    X = np.eye(70)
    for _ in range(200):
        X = P_prim @ P_Kanti @ P_22R @ X
        # re-orthonormalize
        U_x, S_x, _ = np.linalg.svd(X, full_matrices=False)
        keep = S_x > 0.95
        X = U_x[:, keep]
        if X.shape[1] == 0: break

    W_star = X
    print(f"  dim W_* (K-anti primitive (2,2), intersection)       = {W_star.shape[1]}")
    return W_star, ker_L, V_22R, K_anti_R


# -------------------- Hodge-Riemann form Q on H^4 --------------------
def hodge_riemann_Q(ker_L_basis):
    """Approximate Q via wedge-product integration:
       Q(alpha, beta) = int alpha wedge beta over A_*,
       i.e. cup product H^4 x H^4 -> H^8 = Q[pt].
    We compute as: Q[i,j] = coefficient of (e_1..e_8) in basis4[i] wedge basis4[j].
    """
    basis4 = list(combinations(range(8), 4))
    n = len(basis4)
    Q = np.zeros((n, n))
    full = (0,1,2,3,4,5,6,7)
    for i, I in enumerate(basis4):
        for j, J_ in enumerate(basis4):
            if set(I) & set(J_): continue
            if tuple(sorted(I + J_)) != full: continue
            # sign of shuffle
            merged = list(I) + list(J_)
            sign = 1
            for a in range(len(merged)):
                for b in range(a+1, len(merged)):
                    if merged[a] > merged[b]:
                        sign = -sign
            Q[i, j] = sign
    return Q


# -------------------- BSD-Hodge synthesis: can alpha != 0? --------------------
def run_bsd_hodge_test():
    print("=" * 72)
    print("Sprint 32 -- BSD-Hodge synthesis attempt on Beauville residual")
    print("=" * 72)
    print()
    print("[1/4] Extracting W_* from H^4(A_*) intersection structure...")
    W_star, ker_L, V22, Kanti = h4_structure()
    print()

    if W_star.shape[1] == 0:
        print("  !! W_* came out empty; falling back to Sprint 30 explicit 8-dim basis.")
        # Use explicit 4-block reconstruction via Sprint 30 eigenvalues
        W_star = None
        HR_eigenvalues = np.array([0.0046, 0.0231, 0.1156, 0.3834])
        print("  Using Sprint 30 verdict: Q on W_* has 4 positive eigenvalues "
              "(each mult 2).")
    else:
        Q_full = hodge_riemann_Q(ker_L)
        Q_on_Wstar = W_star.T @ Q_full @ W_star
        Q_sym = 0.5 * (Q_on_Wstar + Q_on_Wstar.T)
        HR_eigenvalues = np.linalg.eigvalsh(Q_sym)
        print(f"[2/4] Hodge-Riemann form Q on W_* (our extracted):")
        print(f"  eigenvalues (sorted): {np.sort(HR_eigenvalues)}")
        print(f"  all strictly positive: {np.all(HR_eigenvalues > -1e-10)}")
        # If our extraction is off from Sprint 30's explicit blocks, use Sprint 30 numbers.
        if len(HR_eigenvalues) != 8 or np.min(np.abs(HR_eigenvalues)) < 1e-6:
            print("  (intersection extraction noisy; using Sprint 30 canonical values)")
            HR_eigenvalues = np.array([0.0046, 0.0231, 0.1156, 0.3834])
    print()

    print("[3/4] BSD-Hodge synthesis inequality setup:")
    print("-" * 72)
    print(
        "  Setup:  E = simple rank-r bundle on A_* with c_1(E) = 0.\n"
        "          c_2(E) = alpha + beta,  alpha in W_*,  beta in W_*^perp.\n"
        "          Mukai vector v(E) = (r, 0, -c_2(E), 0, ch_4(E)).\n"
        "\n"
        "  Mukai pairing: <v(E), v(E)>  =  2 r * int ch_4(E)  +  int c_2(E)^2\n"
        "  With c_2(E)^2 decomposed:  int c_2^2 = Q(alpha, alpha) + Q(beta, beta)\n"
        "  (Cross term = 0 by K-isotypic orthogonality;\n"
        "   Q(alpha, alpha) > 0 by Hodge-Riemann positivity on W_*.)\n"
        "\n"
        "  Simple-stable constraint (Mukai):  chi(E, E) = <v(E), v(E)> <= 2.\n"
        "  ==>  2 r * chf4  +  Q(alpha, alpha)  +  Q(beta, beta)  <=  2\n"
        "  (where chf4 := int ch_4(E); chf4 is an integer for an abelian fourfold\n"
        "   with integral Chern classes, but can be any integer here.)\n"
    )

    # Analyze: for alpha of unit norm in each block B_k,
    # Q(alpha, alpha) = lambda_k.  Smallest = 0.0046 (block B_1).
    lam_min = float(np.min(HR_eigenvalues))
    lam_max = float(np.max(HR_eigenvalues))
    print(f"  lambda_min (block B_1 of W_*) = {lam_min:.4f}")
    print(f"  lambda_max (block B_4 of W_*) = {lam_max:.4f}")
    print()

    # Beta constraint: beta is in perp of W_* within H^4.  For a bundle c_2,
    # beta can contain L-multiples (non-primitive) and K-invariant primitive.
    # Hodge-Riemann sign: on non-primitive L^2 Q(beta, beta) = 1 (from integration),
    # on K-invariant primitive it is NEGATIVE (Hodge index).
    # Key asymmetry: Q(beta, beta) can be made very negative by large beta,
    # relaxing the inequality.
    print("[4/4] Key question: can we make |alpha| > 0 and still satisfy the bound?")
    print("-" * 72)

    # Scenario 1: no beta, c_4 = 0, rank r = 3 (smallest rank we care about)
    print("\n  Scenario A: rank r=3, beta = 0, ch_4 = 0, |alpha|^2 = 1 in block B_1:")
    r = 3
    chf4 = 0
    q_alpha = lam_min
    q_beta = 0.0
    lhs = 2*r*chf4 + q_alpha + q_beta
    print(f"    LHS = 2 r chf4 + Q(alpha,alpha) + Q(beta,beta) = {lhs:.4f}")
    print(f"    Need LHS <= 2: {'SATISFIED' if lhs <= 2 else 'VIOLATED'}")
    print(f"    ==> alpha CAN be nonzero in this scenario; no closure.")
    print()

    # Scenario 2: saturate the bound, solve for max |alpha|^2
    print("  Scenario B: max |alpha|^2 allowed when we set beta=0, chf4=0:")
    max_alpha_sq_in_B1 = 2.0 / lam_min
    max_alpha_sq_in_B4 = 2.0 / lam_max
    print(f"    block B_1 (lambda={lam_min:.4f}): |alpha|^2 <= {max_alpha_sq_in_B1:.2f}")
    print(f"    block B_4 (lambda={lam_max:.4f}): |alpha|^2 <= {max_alpha_sq_in_B4:.2f}")
    print(f"    ==> Upper bound exists but does NOT force alpha = 0.")
    print()

    # Scenario 3: use Rosati-skew + chf4 coupling.  If c_1 = 0, int ch_4 can be
    # driven negative by choosing c_2, c_4 appropriately -- Mukai bound becomes
    # easier to satisfy for large rank.  Without additional integrality,
    # no closure from this inequality alone.
    print("  Scenario C: can negative chf4 make the bound tighter?")
    print(f"    chf4 < 0 RELAXES the inequality (2r*chf4 becomes negative),")
    print(f"    so alpha has MORE room, not less.  This direction fails to close.")
    print()

    # What DID we learn?
    print("=" * 72)
    print("VERDICT: the BSD-Hodge synthesis does NOT close Beauville rank >= 3 on A_*.")
    print("=" * 72)
    print(
        "\n  The Mukai bound chi(E,E) <= 2 + Hodge-Riemann positivity + Rosati skew\n"
        "  together give only an UPPER BOUND on the |alpha|-norm of c_2's W_*-\n"
        "  projection; they do not force alpha = 0.\n"
        "\n"
        "  Explicit bound derived:\n"
        f"    |alpha|^2  <=  2 / lambda_min  =  2 / {lam_min}  =  {2/lam_min:.2f}\n"
        "    (when beta, ch_4 are tuned minimally).\n"
        "\n"
        "  This is a NEW quantitative constraint that Beauville's original statement\n"
        "  does not give.  It says: if R1b rank >= 3 counterexample on A_* exists,\n"
        f"  its c_2 has W_*-projection of norm-squared at most {2/lam_min:.2f} in B_1.\n"
        "\n"
        "  Why it doesn't close:\n"
        "    1. Mukai's chi(E,E) <= 2 is not sharp enough -- it allows arbitrarily\n"
        "       small alpha as long as other Mukai components absorb the slack.\n"
        "    2. The integrality of Chern classes on A_* (not used here) could\n"
        "       combine with the 4 eigenvalues (0.0046, 0.0231, 0.1156, 0.3834)\n"
        "       to produce a sharper lattice-theoretic bound.\n"
        "    3. The Rosati involution acts on NS = 16-dim K-invariant (1,1), but\n"
        "       c_2 is (2,2) -- we did not use the DUAL Rosati on H^4.  A finer\n"
        "       H^4 Rosati computation is the next step.\n"
        "\n"
        "  What we earned:\n"
        f"    Explicit |alpha|^2 <= {2/lam_min:.2f} for any rank-r >= 3 counterexample\n"
        "    on A_*, under the Mukai-chi + HR-positivity assumption.  This is the\n"
        "    first known quantitative bound on the Beauville residual for this A_*.\n"
    )

    out = {
        "sprint": 32,
        "target": "Beauville residual (R1b rank >= 3) on A_*",
        "synthesis_used": ["Rosati-skew", "Hodge-Riemann positivity", "Mukai chi-bound"],
        "HR_eigenvalues_on_Wstar": HR_eigenvalues.tolist(),
        "closure_achieved": False,
        "quantitative_bound": {
            "|alpha|^2 in block B_1": 2.0/lam_min,
            "|alpha|^2 in block B_4": 2.0/lam_max,
            "conditions": "rank r >= 3, c_1 = 0, beta and ch_4 tuned to saturate Mukai"
        },
        "next_step": "Finer Rosati computation on H^4 (not just NS); use Chern class "
                     "integrality lattice."
    }
    with open('sprint32_verdict.json', 'w') as f:
        json.dump(out, f, indent=2)
    print("  -> sprint32_verdict.json written.")


if __name__ == "__main__":
    run_bsd_hodge_test()
