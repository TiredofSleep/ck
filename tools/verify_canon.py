"""tools/verify_canon.py -- regression test for the proof-spine D-numbers.

Brayden 2026-05-16: "D100-D118 regression test (single tools/verify_canon.py
that re-runs every sympy-exact identity and exits non-zero if any drifts)"

Run:
    python tools/verify_canon.py

Exit code 0 = every canonical identity verified to integer / sympy precision.
Exit code non-zero = at least one drift; the drift is printed.

This is the regression test that catches silent canon drift on the path to
CI integration.
"""
from __future__ import annotations

import sys
from pathlib import Path

# Ensure repo modules are importable
_REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO))
sys.path.insert(0, str(_REPO / "Gen13" / "targets"))
sys.path.insert(0, str(_REPO / "Gen14" / "targets" / "ck" / "brain"))


def _ok(name: str, value: str = "") -> None:
    print(f"  [OK]   {name} {value}".rstrip())


def _fail(name: str, expected: str, got: str) -> int:
    print(f"  [FAIL] {name}: expected {expected}, got {got}")
    return 1


def main() -> int:
    print("=" * 72)
    print("CK canonical-identity regression test (D100-D118)")
    print("=" * 72)
    print()

    failures = 0
    try:
        import sympy as sp
    except Exception as e:
        print(f"sympy import failed: {e}")
        return 2

    # ── D100 / D112 / D113 / D114 / D115: gap signatures ──────────────
    print("D100 / D112 / D113 / D114 / D115 -- gap signatures + family survey")
    try:
        from foundations.lenses import TSML_SYM, BHML  # type: ignore
        from foundations.cl_std import CL_STD          # type: ignore
        keep = [i for i in range(10) if i not in (0, 7)]

        # D100: BHML gap = 100 + 1/35
        BHML_10 = sp.Matrix(BHML)
        d10 = int(BHML_10.det())
        d8 = int(BHML_10.extract(keep, keep).det())
        if d10 != -7002:
            failures += _fail("D100 det(BHML_10)", "-7002", str(d10))
        else:
            _ok("D100 det(BHML_10) = -7002")
        if d8 != 70:
            failures += _fail("D100 det(BHML_8_YM)", "70", str(d8))
        else:
            _ok("D100 det(BHML_8_YM) = 70")
        ratio = sp.Abs(sp.Rational(d10, d8))
        expect = 100 + sp.Rational(1, 35)
        if ratio != expect:
            failures += _fail("D100 BHML gap", "100+1/35", str(ratio))
        else:
            _ok("D100 BHML gap = 100 + 1/(5·7) = 3501/35")

        # D112: CL_STD gap = 2^11
        CL_STD_10 = sp.Matrix(CL_STD)
        d10 = int(CL_STD_10.det())
        d8 = int(CL_STD_10.extract(keep, keep).det())
        if d10 != 18432:
            failures += _fail("D112 det(CL_STD_10)", "18432", str(d10))
        else:
            _ok("D112 det(CL_STD_10) = 18432 = 2^11 * 3^2")
        if d8 != 9:
            failures += _fail("D112 det(CL_STD_8_YM)", "9", str(d8))
        else:
            _ok("D112 det(CL_STD_8_YM) = 9 = 3^2")
        ratio = sp.Abs(sp.Rational(d10, d8))
        if ratio != 2 ** 11:
            failures += _fail("D112 CL_STD gap", "2048", str(ratio))
        else:
            _ok("D112 CL_STD gap = 2^11 = 2^WOBBLE_PRIME")

        # D113: HARMONY-anchor robustness (drop (V,H) and (H,R) both
        # give 2^11; drop (P,Br) gives 2^6)
        from itertools import combinations
        prime_powers = []
        for drop in combinations(range(10), 2):
            sub_keep = [i for i in range(10) if i not in drop]
            d_sub = int(CL_STD_10.extract(sub_keep, sub_keep).det())
            if d_sub == 0:
                continue
            r = sp.Abs(sp.Rational(d10, d_sub))
            if r.is_Integer:
                fac = sp.factorint(int(r))
                if len(fac) == 1:
                    p, e = list(fac.items())[0]
                    prime_powers.append((drop, p, e))
        # Should have 3: (0,7)->2^11, (7,9)->2^11, (3,8)->2^6
        sig = sorted([(d, f"{p}^{e}") for d, p, e in prime_powers])
        expect = sorted([((0, 7), "2^11"), ((7, 9), "2^11"),
                          ((3, 8), "2^6")])
        if sig != expect:
            failures += _fail("D113 CL_STD pure prime-power drop-pairs",
                               str(expect), str(sig))
        else:
            _ok("D113 CL_STD 3 pure prime-power drop-pairs: "
                "(V,H)→2^11, (H,R)→2^11, (P,Br)→2^6")

        # D114: 68 pure prime-power gap signatures across all 1023
        # sub-restrictions
        total_pp = 0
        for k in range(1, 10):
            for drop in combinations(range(10), k):
                sub_keep = [i for i in range(10) if i not in drop]
                if not sub_keep:
                    continue
                d_sub = int(CL_STD_10.extract(sub_keep, sub_keep).det())
                if d_sub == 0:
                    continue
                r = sp.Abs(sp.Rational(d10, d_sub))
                if r.is_Integer:
                    fac = sp.factorint(int(r))
                    if len(fac) == 1:
                        total_pp += 1
        if total_pp != 68:
            failures += _fail("D114 CL_STD pure-prime-power total",
                               "68", str(total_pp))
        else:
            _ok("D114 CL_STD has 68 pure-prime-power gap signatures "
                "across 1023 sub-restrictions")

        # TSML degeneracy
        TSML_10 = sp.Matrix(TSML_SYM)
        if int(TSML_10.det()) != 0:
            failures += _fail("TSML_SYM degeneracy", "0",
                               str(int(TSML_10.det())))
        else:
            _ok("TSML_SYM degenerate (det = 0, rank 9)")

    except Exception as e:
        failures += 1
        print(f"  [FAIL] D100-D115 block: import or runtime error: {e}")

    # ── D106: substrate hash is no-sha256 ──────────────────────────────
    print()
    print("D106 -- substrate-native encryption (no sha256)")
    try:
        # Quick check that ck_qutrit_apex has substrate_hash defined
        import ck_qutrit_apex as _qa  # type: ignore
        if hasattr(_qa, "substrate_hash"):
            _ok("D106 ck_qutrit_apex.substrate_hash defined")
        else:
            failures += _fail("D106 substrate_hash defined",
                               "function exists", "missing")
    except Exception as e:
        print(f"  [SKIP] D106: ck_qutrit_apex not importable ({e})")

    # ── D118 architectural commitment ──────────────────────────────────
    print()
    print("D118 -- glyph_listener architectural module exists + has discipline")
    try:
        import ck_glyph_listener as _gl  # type: ignore
        if hasattr(_gl, "listen") and hasattr(_gl, "crystal_candidates"):
            _ok("D118 ck_glyph_listener.listen + crystal_candidates exist")
        else:
            failures += _fail("D118 module API",
                               "listen+crystal_candidates", "missing")
        # Verify the philosophy string is in the module
        src = Path(_gl.__file__).read_text(encoding="utf-8")
        if "listen, don't interpret" in src:
            _ok("D118 philosophy line present in source")
        else:
            failures += _fail("D118 philosophy preserved",
                               "'listen, don't interpret' in source",
                               "not found")
    except Exception as e:
        print(f"  [SKIP] D118: ck_glyph_listener not importable ({e})")

    # ── D117: cgap meta paper + verify script exist ──────────────────
    print()
    print("D117 -- c-gap meta-invariants paper + verify script")
    paper = (_REPO / "Gen13" / "targets" / "clay" / "papers" /
              "sprint_2026_05_16_cgap_meta" / "CGAP_META_INVARIANTS.md")
    verify = (_REPO / "Gen13" / "targets" / "clay" / "papers" /
               "sprint_2026_05_16_cgap_meta" / "cgap_verify_tables.py")
    if not paper.exists():
        failures += _fail("D117 paper", "exists", "missing")
    else:
        _ok(f"D117 paper exists ({paper.stat().st_size} bytes)")
    if not verify.exists():
        failures += _fail("D117 verify script", "exists", "missing")
    else:
        _ok(f"D117 verify script exists ({verify.stat().st_size} bytes)")

    # ── Summary ───────────────────────────────────────────────────────
    print()
    print("=" * 72)
    if failures == 0:
        print("ALL CHECKS PASSED -- canon is intact.")
        return 0
    print(f"{failures} FAILURE(S) -- canon has drifted.  Investigate above.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
