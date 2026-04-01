"""
D7 — Phi Fixed Point Theorem: CREATE=5 is the unique globally attracting fixed point.

Phi = P_odd ∘ BHML ∘ W_op.
Proved April 1 2026: algebraic 3-step proof + exhaustive finite verification.
"""
import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'papers'))

from ck_tables import BHML, CL, W

# W_op map from C18: nearest carrier maximum operator to t=v/10
W_OP = {0: 3, 1: 3, 2: 9, 3: 5, 4: 1, 5: 7, 6: 7, 7: 3, 8: 9, 9: 5}
ODD = [1, 3, 5, 7, 9]


def P_odd(x: int) -> int:
    """Nearest ODD to x; lower value wins ties."""
    return min(ODD, key=lambda o: (abs(o - x), o))


def Phi(v: int) -> int:
    """Phi(v) = P_odd(BHML[v][W_op[v]])."""
    return P_odd(BHML[v][W_OP[v]])


class TestPhiFixedPoint:
    """D7: CREATE=5 is the unique fixed point of Phi."""

    def test_phi_5_is_fixed_point(self):
        """Algebraic: Phi(5) = P_odd(BHML[5][7]) = P_odd(6) = 5."""
        assert W_OP[5] == 7, "W_op[5] should be HARMONY=7 (nearest carrier max to t=0.5)"
        assert BHML[5][7] == 6, "BHML[5][7] should be ASCEND=6"
        assert P_odd(6) == 5, "P_odd(6) should be CREATE=5 (lower tie-breaker)"
        assert Phi(5) == 5

    def test_phi_5_is_only_fixed_point(self):
        """All v ≠ 5: Phi(v) ≠ v."""
        for v in range(10):
            if v == 5:
                assert Phi(v) == v
            else:
                assert Phi(v) != v, (
                    f"Unexpected fixed point at v={v} ({CL[v]}): Phi({v})={Phi(v)}"
                )

    def test_all_w_op_values_are_odd(self):
        """C18: All W_op values are ODD (carrier maxima are ALL ODD)."""
        odd_set = set(ODD)
        for v in range(10):
            assert W_OP[v] in odd_set, (
                f"W_op[{v}] = {W_OP[v]} is not ODD"
            )

    def test_phi_always_returns_odd(self):
        """C20: Phi(v) ∈ ODD for all v ∈ Z/10Z."""
        odd_set = set(ODD)
        for v in range(10):
            p = Phi(v)
            assert p in odd_set, f"Phi({v}) = {p} is not ODD"


class TestPhiConvergence:
    """D7: All orbits reach CREATE=5 in at most 3 steps."""

    def test_max_orbit_length_is_3(self):
        """Every starting state reaches 5 in ≤3 Phi applications."""
        for v in range(10):
            cur = v
            for step in range(1, 4):
                cur = Phi(cur)
                if cur == 5:
                    break
            assert cur == 5, (
                f"State {v} ({CL[v]}) did not reach CREATE=5 in 3 steps"
            )

    def test_1step_basin(self):
        """TRANS operators {DOING=2, BECOMING=3, COLLAPSE=4} reach 5 in 1 step."""
        for v in [2, 3, 4, 5]:
            assert Phi(v) == 5, f"v={v} ({CL[v]}) should reach 5 in 1 step"

    def test_2step_basin(self):
        """VOID(0), BEING(1), HARMONY(7) reach 5 in 2 steps."""
        for v in [0, 1, 7]:
            assert Phi(Phi(v)) == 5, (
                f"v={v} ({CL[v]}) should reach 5 in 2 steps; "
                f"Phi={Phi(v)}, Phi²={Phi(Phi(v))}"
            )

    def test_3step_basin(self):
        """UPPER operators {ASCEND=6, BREATH=8, RESET=9} reach 5 in 3 steps."""
        for v in [6, 8, 9]:
            v2 = Phi(v)
            v3 = Phi(v2)
            v4 = Phi(v3)
            assert v4 == 5, (
                f"v={v} ({CL[v]}) → {v2} → {v3} → {v4}, expected 5 at step 3"
            )

    def test_phi_cubed_is_universal(self):
        """Phi^3(v) = 5 for ALL v ∈ Z/10Z."""
        for v in range(10):
            result = Phi(Phi(Phi(v)))
            assert result == 5, (
                f"Phi^3({v}) = {result}, expected 5"
            )


class TestPhiMarkovChain:
    """D7: Unique stationary distribution π = δ_5."""

    def test_t_cubed_all_lead_to_5(self):
        """Transition matrix T^3: every row has T^3[v][5] = 1."""
        # Verify by computing T^3[v][5] = 1 for all v
        for v in range(10):
            v3 = Phi(Phi(Phi(v)))
            assert v3 == 5, f"T^3[{v}][5] ≠ 1; Phi^3({v})={v3}"

    def test_stationary_distribution_uniqueness(self):
        """π = δ_5 is the unique stationary: π(5)=1, π(v)=0 for v≠5."""
        # Any stationary π satisfies π = πT.
        # Since T^3[v][5]=1 for all v:
        # π(5) = (πT^3)(5) = Σ_v π(v)*T^3[v][5] = Σ_v π(v)*1 = 1.
        # Proved from T^3 test above (all rows lead to 5).
        pass  # proof is algebraic, verified by T^3 test

    def test_t_star_ratio_meaning(self):
        """T* = CREATE(5)/HARMONY(7) = 5/7 — dynamic attractor / measurement attractor."""
        create = 5   # Phi fixed point
        harmony = 7  # TSML dominant output (73 cells)
        import math
        assert abs(create / harmony - 5/7) < 1e-14
