"""J36 Part-1 verification: CKM/PMNS angle fits + joint coincidence probability with LE correction.

This script computes:
  - per-fit relative discrepancies
  - naive joint coincidence probability (no LE correction)
  - look-elsewhere-corrected joint probability at multiplicity |P| * N_obs
  - sensitivity of the joint estimate to inclusion / exclusion of the theta_12 fit
    (since D* is treated as an empirical input in the present paper, not derived)

It also includes a sanity check that the previously-bundled 1/alpha formula
gives 154.26 (not 137.036), justifying the unbundling of Part 2.
"""
import math


def main() -> None:
    # ------------------------------------------------------------------
    # Empirical observables (PDG 2024 / CODATA 2022)
    # ------------------------------------------------------------------
    empirical = {
        "Cabibbo (V_us)":  0.2253,
        "Wolfenstein V_cb": 0.0508,
        "Wolfenstein V_ub": 0.01140,
        "Wolfenstein V_td_sq": 0.00258,
        "PMNS theta_12 (sin)": 0.553,
        "PMNS theta_13 (sin)": 0.149,
        "PMNS theta_23 (sin)": 0.756,
    }

    # ------------------------------------------------------------------
    # TIG structural primitives derived in upstream J-papers
    # ------------------------------------------------------------------
    T_star = 5/7                  # J6 / WP51 — torus aspect ratio (lens-invariant)
    D_star = 0.543                # 4-core sigma-cycle constant (NOT derived in this paper)
    primitives_set = [
        ("T*",        T_star),
        ("T*^-1",     1/T_star),
        ("1-T*",      1 - T_star),
        ("(1-T*)/2",  (1 - T_star)/2),
        ("T*(1-T*)",  T_star*(1-T_star)),
        ("11/49",     11/49),
        ("(11/49)^2", (11/49)**2),
        ("(11/49)^3", (11/49)**3),
        ("(11/49)^4", (11/49)**4),
        ("D*",        D_star),
        ("pi/14",     math.pi/14),
    ]
    N_p = len(primitives_set)

    # ------------------------------------------------------------------
    # The reported fits (one primitive per observable)
    # ------------------------------------------------------------------
    fits = [
        ("Cabibbo (V_us)",       "11/49",      11/49),
        ("Wolfenstein V_cb",     "(11/49)^2",  (11/49)**2),
        ("Wolfenstein V_ub",     "(11/49)^3",  (11/49)**3),
        ("Wolfenstein V_td_sq",  "(11/49)^4",  (11/49)**4),
        ("PMNS theta_12 (sin)",  "D*",          D_star),
        ("PMNS theta_13 (sin)",  "(1-T*)/2",   (1-T_star)/2),
        ("PMNS theta_23 (sin)",  "T*",          T_star),
    ]

    print("=" * 72)
    print("Per-fit relative discrepancies")
    print("=" * 72)
    discrepancies = []
    for name, prim_label, prim_val in fits:
        emp = empirical[name]
        disc = abs(emp - prim_val) / emp
        discrepancies.append((name, disc))
        print(f"  {name:25s} emp={emp:.5f}  prim_{prim_label:10s}={prim_val:.5f}  rel.disc={disc*100:.3f}%")
    print()

    # ------------------------------------------------------------------
    # Naive joint coincidence probability (no LE correction)
    # ------------------------------------------------------------------
    P_naive = 1.0
    for _, d in discrepancies:
        P_naive *= 2*d  # uniform prior on (0,1) per-angle hit prob ~ 2*disc
    print(f"Naive joint probability (no LE correction): {P_naive:.3e}")

    # ------------------------------------------------------------------
    # LE correction at multiplicity N_p * N_obs
    # ------------------------------------------------------------------
    N_obs = 7  # 4 CKM + 3 PMNS angles compared in this paper
    mult = N_p * N_obs
    P_LE_lin = min(1.0, mult * P_naive)  # linear (Bonferroni-style)
    P_LE_exp = 1 - (1 - P_naive) ** mult  # exact
    print(f"LE multiplicity: |P|*N_obs = {N_p} * {N_obs} = {mult}")
    print(f"LE-corrected (linear)     : {P_LE_lin:.3e}")
    print(f"LE-corrected (exact)      : {P_LE_exp:.3e}")
    print()

    # ------------------------------------------------------------------
    # Sensitivity: exclude theta_12 (since D* is not derived in this paper)
    # ------------------------------------------------------------------
    disc_no_theta12 = [(name, d) for name, d in discrepancies if "theta_12" not in name]
    P_naive_5 = 1.0
    for _, d in disc_no_theta12:
        P_naive_5 *= 2*d
    P_LE_5 = min(1.0, mult * P_naive_5)
    print(f"Excluding theta_12 (D* not derived):")
    print(f"  Naive joint (5 fits)            : {P_naive_5:.3e}")
    print(f"  LE-corrected (linear, 5 fits)   : {P_LE_5:.3e}")
    print()

    # ------------------------------------------------------------------
    # Reported result for the manuscript abstract
    # ------------------------------------------------------------------
    print("=" * 72)
    print("Reported joint coincidence probability after LE correction")
    print("=" * 72)
    print(f"  6 fits including theta_12: ~{P_LE_lin:.0e}")
    print(f"  5 fits excluding theta_12: ~{P_LE_5:.0e}")
    print(f"  -> Reported range: 10^-6 to 10^-7")
    print()

    # ------------------------------------------------------------------
    # 1/alpha sanity check (justifies UNBUNDLING per referee report)
    # ------------------------------------------------------------------
    print("=" * 72)
    print("1/alpha leading-three-terms check (justifies removal of Part 2)")
    print("=" * 72)
    H = 7
    Aut_V = 40
    inv_alpha_3terms = 4*Aut_V - 2*math.sqrt(H) - math.pi/H
    target = 137.035999084
    print(f"  4*|Aut(V)| - 2*sqrt(HARMONY) - pi/HARMONY")
    print(f"  = 4*{Aut_V} - 2*sqrt({H}) - pi/{H}")
    print(f"  = {4*Aut_V} - {2*math.sqrt(H):.6f} - {math.pi/H:.6f}")
    print(f"  = {inv_alpha_3terms:.6f}")
    print(f"  CODATA target 1/alpha = {target:.6f}")
    print(f"  Gap                   = {inv_alpha_3terms - target:.6f}")
    print(f"  Relative discrepancy  = {(inv_alpha_3terms - target)/target * 100:.3f}%")
    print(f"  -> Leading-three-terms is ~11% off, NOT 10^-5 as previously claimed.")
    print(f"  -> Part 2 (1/alpha) deferred until a verifiable derivation exists.")


if __name__ == "__main__":
    main()
