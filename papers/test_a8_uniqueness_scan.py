"""
test_a8_uniqueness_scan.py
==========================
A8 — b=35 Goldilocks Uniqueness Scan

Claim: b=35 = 5×7 has a D2-balance curvature signature that no other
semiprime (within the scanned range) shares. The d2_balance metric is:

    d2_balance(b=p×q) = |D2_sig(p) - D2_sig(q)| / D2_sig(p)

where D2_sig(prime) = sum of |D2(k, prime)| for k = 2..floor(prime/2)
and D2(k, f) = R(k+1,f) - 2R(k,f) + R(k-1,f)  [second difference of R].

Scan: all semiprimes b ≤ SCAN_LIMIT.
For each: compute d2_balance, d2_sig_p, d2_sig_q, ratio q/p, unit_frac.
Find any b ≠ 35 with d2_balance within TOLERANCE of b=35.

Kill condition for A8: a second semiprime with matching profile.
Promotion condition: no match found → bounded negative result → Tier B.

Luther-Sanders Research Framework, March 31, 2026
DOI: 10.5281/zenodo.18852047
"""

import math
import os
import json

SCAN_LIMIT = 10000       # scan all semiprimes up to this value
TOLERANCE  = 0.001       # absolute tolerance for d2_balance match
REPORT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")

PI = math.pi


# ── Primes ───────────────────────────────────────────────────────────────────

def sieve(n):
    """Return sorted list of primes up to n."""
    is_p = bytearray([1]) * (n + 1)
    is_p[0] = is_p[1] = 0
    for i in range(2, int(n**0.5) + 1):
        if is_p[i]:
            for j in range(i*i, n + 1, i):
                is_p[j] = 0
    return [i for i in range(2, n + 1) if is_p[i]]


def factorize_semiprimes(limit, primes):
    """Return list of (b, p, q) for all semiprimes b = p*q ≤ limit, p < q."""
    sp = []
    prime_set = set(primes)
    for i, p in enumerate(primes):
        if p * p > limit:
            break
        for q in primes[i+1:]:
            b = p * q
            if b > limit:
                break
            sp.append((b, p, q))
    return sorted(sp)


# ── D2 curvature signature ────────────────────────────────────────────────────

def R(k, f):
    """Harmonic resonance R(k,f) = sin²(πk/f) / (k² sin²(π/f))"""
    den_sin = math.sin(PI / f)
    if abs(den_sin) < 1e-15:
        return 0.0
    num = math.sin(PI * k / f)
    return (num * num) / (k * k * den_sin * den_sin)


def d2_sig(prime):
    """
    D2 curvature signature for a prime:
    sum of |R(k+1,p) - 2R(k,p) + R(k-1,p)| for k = 2..floor(p/2)
    This is prime-specific (ω-blind: does not depend on any partner prime).
    """
    kmax = prime // 2
    if kmax < 2:
        return 0.0
    total = 0.0
    for k in range(2, kmax + 1):
        if k + 1 >= prime:
            continue
        d2 = R(k+1, prime) - 2*R(k, prime) + R(k-1, prime)
        total += abs(d2)
    return total


# Cache D2 signatures for primes (they repeat across semiprimes)
_d2_cache = {}

def d2_sig_cached(prime):
    if prime not in _d2_cache:
        _d2_cache[prime] = d2_sig(prime)
    return _d2_cache[prime]


# ── Unit fraction (T* formula) ────────────────────────────────────────────────

def unit_frac(p, q):
    """unit_frac(b=p×q) = (q - floor(q/p) - 1) / q"""
    return (q - (q // p) - 1) / q


# ── Atlas score (from sprint4 laws) ──────────────────────────────────────────

def unit_group_alphabet(b, alphabet=range(1, 10)):
    """C = {x ∈ {1..9} : gcd(x, b) = 1}"""
    return [x for x in alphabet if math.gcd(x, b) == 1]


def orbit_central_har(b, C):
    """
    HAR selection rule (revised): h = min{h ∈ C : h²%b ∈ C, h²≠1, h²≠h}
    Returns (har, orbit_central_elements).
    """
    candidates = []
    for h in C:
        if h == 1:
            continue
        h2 = (h * h) % b
        if h2 in C and h2 != 1 and h2 != h:
            candidates.append(h)
    if not candidates:
        return None, []
    return min(candidates), candidates


# ── Main scan ─────────────────────────────────────────────────────────────────

def main():
    lines = []
    lines.append("A8 — GOLDILOCKS UNIQUENESS SCAN")
    lines.append("Luther-Sanders Research Framework | March 31 2026")
    lines.append(f"Scan range: all semiprimes b ≤ {SCAN_LIMIT}")
    lines.append(f"Tolerance:  d2_balance match within ±{TOLERANCE}")
    lines.append("")

    primes = sieve(SCAN_LIMIT)
    semiprimes = factorize_semiprimes(SCAN_LIMIT, primes)
    lines.append(f"Semiprimes found: {len(semiprimes)}")
    lines.append("")

    # Reference: b=35
    ref_b, ref_p, ref_q = 35, 5, 7
    ref_d2p = d2_sig_cached(ref_p)
    ref_d2q = d2_sig_cached(ref_q)
    ref_balance = abs(ref_d2p - ref_d2q) / ref_d2p if ref_d2p > 0 else float('nan')
    ref_ratio   = ref_q / ref_p
    ref_uf      = unit_frac(ref_p, ref_q)
    ref_C       = unit_group_alphabet(ref_b)
    ref_har, _  = orbit_central_har(ref_b, ref_C)
    ref_phi_C   = len(ref_C)

    lines.append("REFERENCE: b=35 = 5×7")
    lines.append(f"  D2_sig(p=5)    = {ref_d2p:.8f}")
    lines.append(f"  D2_sig(q=7)    = {ref_d2q:.8f}")
    lines.append(f"  d2_balance     = {ref_balance:.8f}")
    lines.append(f"  ratio q/p      = {ref_ratio:.6f}")
    lines.append(f"  unit_frac T*   = {ref_uf:.8f}  (= 5/7 = {5/7:.8f})")
    lines.append(f"  |C ∩ {{1..9}}|  = {ref_phi_C}")
    lines.append(f"  HAR            = {ref_har}")
    lines.append("")

    # Full scan
    results = []
    for b, p, q in semiprimes:
        d2p = d2_sig_cached(p)
        d2q = d2_sig_cached(q)
        if d2p < 1e-15:
            continue
        balance = abs(d2p - d2q) / d2p
        ratio   = q / p
        uf      = unit_frac(p, q)
        C       = unit_group_alphabet(b)
        har, _  = orbit_central_har(b, C)
        phi_C   = len(C)
        results.append({
            "b": b, "p": p, "q": q,
            "d2p": d2p, "d2q": d2q, "d2_balance": balance,
            "ratio": ratio, "unit_frac": uf,
            "phi_C": phi_C, "har": har,
        })

    # --- Check 1: d2_balance match ---
    lines.append("=" * 70)
    lines.append("CHECK 1 — d2_balance MATCHES (within tolerance)")
    lines.append("=" * 70)
    balance_matches = [r for r in results
                       if abs(r["d2_balance"] - ref_balance) < TOLERANCE and r["b"] != 35]
    lines.append(f"Matches found (b ≠ 35, |d2_balance - {ref_balance:.4f}| < {TOLERANCE}): "
                 f"{len(balance_matches)}")
    if balance_matches:
        lines.append(f"  {'b':>8}  {'p':>6}  {'q':>6}  {'d2_balance':>12}  "
                     f"{'ratio':>8}  {'unit_frac':>10}  {'phi_C':>6}  {'HAR':>4}")
        for r in balance_matches[:30]:
            lines.append(f"  {r['b']:>8}  {r['p']:>6}  {r['q']:>6}  "
                         f"{r['d2_balance']:>12.6f}  {r['ratio']:>8.4f}  "
                         f"{r['unit_frac']:>10.6f}  {r['phi_C']:>6}  {r['har'] or 'None':>4}")
    else:
        lines.append("  NONE. b=35 is UNIQUE in d2_balance within the scanned range.")
    lines.append("")

    # --- Check 2: full profile match (balance + ratio + phi_C + HAR) ---
    lines.append("=" * 70)
    lines.append("CHECK 2 — FULL PROFILE MATCH (balance + ratio + phi_C + HAR)")
    lines.append("=" * 70)
    profile_matches = [
        r for r in results
        if abs(r["d2_balance"] - ref_balance) < TOLERANCE
        and abs(r["ratio"] - ref_ratio) < 0.01
        and r["phi_C"] == ref_phi_C
        and r["har"] == ref_har
        and r["b"] != 35
    ]
    lines.append(f"Full profile matches: {len(profile_matches)}")
    if not profile_matches:
        lines.append("  NONE. b=35 is UNIQUE in full (d2_balance, ratio, phi_C, HAR) profile.")
    else:
        for r in profile_matches:
            lines.append(f"  b={r['b']}: d2_balance={r['d2_balance']:.6f}, "
                         f"ratio={r['ratio']:.4f}, phi_C={r['phi_C']}, HAR={r['har']}")
    lines.append("")

    # --- Check 3: unit_frac = T* match ---
    lines.append("=" * 70)
    lines.append("CHECK 3 — unit_frac NEAR T* = 5/7")
    lines.append("=" * 70)
    T_STAR = 5 / 7
    near_tstar = [r for r in results if abs(r["unit_frac"] - T_STAR) < 0.001]
    lines.append(f"Semiprimes with unit_frac ≈ 5/7 = {T_STAR:.6f} (within 0.001): "
                 f"{len(near_tstar)}")
    for r in near_tstar:
        lines.append(f"  b={r['b']} = {r['p']}×{r['q']}: unit_frac={r['unit_frac']:.8f}")
    lines.append("")

    # --- Check 4: phi_C = 7 worlds ---
    lines.append("=" * 70)
    lines.append("CHECK 4 — |C ∩ {1..9}| = 7 WORLDS")
    lines.append("=" * 70)
    phi7_worlds = [r for r in results if r["phi_C"] == ref_phi_C]
    lines.append(f"Semiprimes with |C ∩ {{1..9}}| = {ref_phi_C}: {len(phi7_worlds)}")
    lines.append(f"  {'b':>8}  {'p×q':>12}  {'d2_balance':>12}  {'HAR':>4}  {'unit_frac':>10}")
    for r in phi7_worlds[:20]:
        lines.append(f"  {r['b']:>8}  {r['p']:>4}×{r['q']:<6}  "
                     f"{r['d2_balance']:>12.6f}  {r['har'] or '-':>4}  "
                     f"{r['unit_frac']:>10.6f}")
    if len(phi7_worlds) > 20:
        lines.append(f"  ... ({len(phi7_worlds) - 20} more)")
    lines.append("")

    # --- Verdict ---
    lines.append("=" * 70)
    lines.append("VERDICT")
    lines.append("=" * 70)
    lines.append("")
    if not balance_matches:
        lines.append("CHECK 1: UNIQUE — no second semiprime with same d2_balance")
        lines.append(f"  -> A8 receives BOUNDED NEGATIVE RESULT within b ≤ {SCAN_LIMIT}")
        lines.append("  -> Path to Tier B: prove algebraically why no other (p,q) pair")
        lines.append("     satisfies |D2_sig(p) - D2_sig(q)|/D2_sig(p) = 2.742...")
    else:
        lines.append(f"CHECK 1: MATCH FOUND — A8 KILLED as stated.")
        lines.append("  -> The d2_balance uniqueness claim is false.")
        lines.append("  -> Revise: what IS unique about b=35?")

    if not profile_matches:
        lines.append("CHECK 2: FULL PROFILE UNIQUE — no matching (balance+ratio+phi_C+HAR)")
        lines.append("  -> b=35 is isolated in the full 4-dimensional profile space")
    else:
        lines.append("CHECK 2: PROFILE MATCH FOUND — uniqueness requires finer criterion")

    lines.append("")
    lines.append(f"T* worlds (unit_frac ≈ 5/7): {len(near_tstar)}")
    lines.append(f"phi_C=7 worlds: {len(phi7_worlds)}")
    lines.append(f"Scan complete: {len(semiprimes)} semiprimes up to b={SCAN_LIMIT}")

    # Save
    report = "\n".join(lines)
    print(report.encode('ascii', errors='replace').decode('ascii'))

    os.makedirs(REPORT_DIR, exist_ok=True)
    out_txt = os.path.join(REPORT_DIR, "a8_uniqueness_scan_report.txt")
    out_json = os.path.join(REPORT_DIR, "a8_uniqueness_scan.json")

    with open(out_txt, "w", encoding="utf-8") as f:
        f.write(report)
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump({
            "scan_limit": SCAN_LIMIT,
            "n_semiprimes": len(semiprimes),
            "reference": {
                "b": 35, "p": 5, "q": 7,
                "d2_balance": ref_balance,
                "unit_frac": ref_uf,
                "phi_C": ref_phi_C,
                "HAR": ref_har,
            },
            "d2_balance_matches": balance_matches[:50],
            "full_profile_matches": profile_matches[:50],
            "near_tstar_worlds": near_tstar[:50],
            "phi_C_eq_ref_worlds": phi7_worlds[:50],
        }, f, indent=2)
    print(f"\n[A8 report: {out_txt}]")
    print(f"[A8 data:   {out_json}]")


if __name__ == "__main__":
    main()
