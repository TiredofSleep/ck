"""
ck_neighbor_generators.py -- Generators for 18 Neighbor Problems
================================================================
Operator: PROGRESS (3) -- Each neighbor inherits and extends.

Neighbor problems reuse the parent Clay codec.  These generators
produce raw_reading dicts matching the parent codec's expected keys,
but with domain-specific mathematical physics.

Neighbor codec map tells the dispatcher which parent codec to use:
  ns_2d -> NavierStokesCodec, rh_dirichlet -> RiemannCodec, etc.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
from typing import Dict

from ck_sim.being.ck_sdv_safety import DeterministicRNG, clamp, safe_div, safe_log
from ck_sim.doing.ck_clay_generators import ClayGenerator


# ================================================================
#  NEIGHBOR -> PARENT CODEC MAP
# ================================================================

NEIGHBOR_CODEC_MAP = {
    'ns_2d': 'navier_stokes',
    'ns_sqg': 'navier_stokes',
    'ns_euler': 'navier_stokes',
    'pnp_ac0': 'p_vs_np',
    'pnp_clique': 'p_vs_np',
    'pnp_bpp': 'p_vs_np',
    'rh_dirichlet': 'riemann',
    'rh_function_field': 'riemann',
    'rh_fake': 'riemann',
    'ym_schwinger': 'yang_mills',
    'ym_lattice': 'yang_mills',
    'ym_phi4': 'yang_mills',
    'bsd_function_field': 'bsd',
    'bsd_avg_rank': 'bsd',
    'bsd_sato_tate': 'bsd',
    'hodge_tate': 'hodge',
    'hodge_standard': 'hodge',
    'hodge_transcendental': 'hodge',
}


# ================================================================
#  NS NEIGHBORS (use NavierStokesCodec keys)
# ================================================================

class NS2DGenerator(ClayGenerator):
    """2D Navier-Stokes: global regularity is proved (enstrophy conserved)."""

    def __init__(self, seed: int = 42):
        super().__init__('ns_2d', seed)

    def generate(self, level: int, test_case: str = 'vortex_patch') -> dict:
        if test_case == 'vortex_patch':
            return self._vortex_patch(level)
        return self._vortex_merger(level)

    def _vortex_patch(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.005)
        scale = 2.0 ** (-level)
        omega = 5.0 * math.exp(-0.5 / (scale + 0.01)) + noise
        return {
            'omega_mag': max(0.0, omega),
            'omega_max': 10.0,
            'strain_alignment': clamp(0.7 + noise * 0.5),
            'scale_epsilon': clamp(1.0 - scale),
            'energy_dissipation': 0.3 * (1.0 + 0.2 * level),
            'diss_max': 3.0,
            'omega_gradient': max(0.0, omega * 0.2),
            'grad_max': 5.0,
            'energy': clamp(0.4 * math.exp(-0.05 * level)),
        }

    def _vortex_merger(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.01)
        scale = 2.0 ** (-level)
        omega = 8.0 * math.exp(-0.3 * level) * (1.0 + 0.3 * math.sin(level))
        return {
            'omega_mag': max(0.0, omega + noise),
            'omega_max': 12.0,
            'strain_alignment': clamp(0.5 + 0.2 * math.cos(level) + noise),
            'scale_epsilon': clamp(1.0 - scale),
            'energy_dissipation': 0.4 * (1.0 + 0.25 * level),
            'diss_max': 4.0,
            'omega_gradient': max(0.0, omega * 0.25),
            'grad_max': 8.0,
            'energy': clamp(0.45 * math.exp(-0.08 * level)),
        }


class NSSQGGenerator(ClayGenerator):
    """Critical SQG: surface quasi-geostrophic with singular dynamics."""

    def __init__(self, seed: int = 42):
        super().__init__('ns_sqg', seed)

    def generate(self, level: int, test_case: str = 'smooth_theta') -> dict:
        if test_case == 'smooth_theta':
            return self._smooth_theta(level)
        return self._singular_front(level)

    def _smooth_theta(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.008)
        scale = 2.0 ** (-level)
        theta_grad = 6.0 * math.exp(-0.8 / (scale + 0.01)) + noise
        return {
            'omega_mag': max(0.0, theta_grad),
            'omega_max': 12.0,
            'strain_alignment': clamp(0.55 + 0.1 * math.cos(level * 0.5) + noise * 0.5),
            'scale_epsilon': clamp(1.0 - scale),
            'energy_dissipation': 0.4 * (1.0 + 0.15 * level),
            'diss_max': 4.0,
            'omega_gradient': max(0.0, theta_grad * 0.35),
            'grad_max': 8.0,
            'energy': clamp(0.35 * math.exp(-0.06 * level)),
        }

    def _singular_front(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.015)
        scale = 2.0 ** (-level)
        theta_grad = 10.0 * (1.0 + 0.5 * level) / (1.0 + 0.1 * level ** 2)
        return {
            'omega_mag': max(0.0, theta_grad + noise),
            'omega_max': 15.0,
            'strain_alignment': clamp(0.3 + 0.1 * math.sin(level * 0.8) + noise),
            'scale_epsilon': clamp(1.0 - scale),
            'energy_dissipation': 0.2 * (1.0 + 0.1 * level),
            'diss_max': 3.0,
            'omega_gradient': max(0.0, theta_grad * 0.5 + abs(noise)),
            'grad_max': 12.0,
            'energy': clamp(0.5 * math.exp(-0.03 * level)),
        }


class NSEulerGenerator(ClayGenerator):
    """3D Euler: inviscid, no dissipation, blowup remains open."""

    def __init__(self, seed: int = 42):
        super().__init__('ns_euler', seed)

    def generate(self, level: int, test_case: str = 'vortex_ring') -> dict:
        if test_case == 'vortex_ring':
            return self._vortex_ring(level)
        return self._blowup_candidate(level)

    def _vortex_ring(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.01)
        omega = 7.0 * (1.0 + 0.1 * level) / (1.0 + 0.05 * level ** 2)
        return {
            'omega_mag': max(0.0, omega + noise),
            'omega_max': 15.0,
            'strain_alignment': clamp(0.5 + noise * 0.5),
            'scale_epsilon': clamp(0.5 + 0.02 * level),
            'energy_dissipation': 0.01,  # Inviscid: near-zero dissipation
            'diss_max': 0.1,
            'omega_gradient': max(0.0, omega * 0.4),
            'grad_max': 10.0,
            'energy': clamp(0.7 - 0.01 * level),
        }

    def _blowup_candidate(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.02)
        # Vorticity grows with level (potential blowup)
        omega = 5.0 * (1.0 + 0.3 * level)
        return {
            'omega_mag': max(0.0, omega + noise),
            'omega_max': 50.0,
            'strain_alignment': clamp(0.8 + noise * 0.5),  # High alignment = danger
            'scale_epsilon': clamp(0.5 + 0.02 * level),
            'energy_dissipation': 0.001,
            'diss_max': 0.01,
            'omega_gradient': max(0.0, omega * 0.6),
            'grad_max': 40.0,
            'energy': clamp(0.8),
        }


# ================================================================
#  PvNP NEIGHBORS (use PvsNPCodec keys)
# ================================================================

class PnpAC0Generator(ClayGenerator):
    """AC^0 lower bounds: constant-depth circuits can't compute parity."""

    def __init__(self, seed: int = 42):
        super().__init__('pnp_ac0', seed)

    def generate(self, level: int, test_case: str = 'small_circuit') -> dict:
        if test_case == 'small_circuit':
            return self._small_circuit(level)
        return self._parity_circuit(level)

    def _small_circuit(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.01)
        depth = clamp(0.3 + 0.05 * level + noise)
        return {
            'backbone_fraction': clamp(0.7 + noise * 0.5),
            'clause_density': 2.0 + 0.5 * level,
            'propagation_depth': depth,
            'local_coherence': clamp(0.6 + 0.02 * level + noise),
            'search_tree_balance': clamp(0.5 + noise * 0.5),
        }

    def _parity_circuit(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.015)
        return {
            'backbone_fraction': clamp(0.2 + noise),        # Low backbone = hard
            'clause_density': 4.0 + level,
            'propagation_depth': clamp(0.1 + 0.02 * level),  # Shallow propagation
            'local_coherence': clamp(0.2 + noise),
            'search_tree_balance': clamp(0.3 + noise),
        }


class PnpCliqueGenerator(ClayGenerator):
    """Monotone CLIQUE: circuit lower bounds for clique detection."""

    def __init__(self, seed: int = 42):
        super().__init__('pnp_clique', seed)

    def generate(self, level: int, test_case: str = 'sparse_graph') -> dict:
        if test_case == 'sparse_graph':
            return self._sparse_graph(level)
        return self._dense_graph(level)

    def _sparse_graph(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.01)
        return {
            'backbone_fraction': clamp(0.6 + 0.02 * level + noise),
            'clause_density': 1.5 + 0.3 * level,
            'propagation_depth': clamp(0.5 + noise),
            'local_coherence': clamp(0.5 + 0.03 * level + noise),
            'search_tree_balance': clamp(0.6 + noise * 0.5),
        }

    def _dense_graph(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.02)
        return {
            'backbone_fraction': clamp(0.15 + noise),
            'clause_density': 5.0 + 1.5 * level,
            'propagation_depth': clamp(0.15 + 0.01 * level),
            'local_coherence': clamp(0.15 + noise),
            'search_tree_balance': clamp(0.2 + noise),
        }


class PnpBPPGenerator(ClayGenerator):
    """P vs BPP: can randomness be eliminated?"""

    def __init__(self, seed: int = 42):
        super().__init__('pnp_bpp', seed)

    def generate(self, level: int, test_case: str = 'low_error') -> dict:
        if test_case == 'low_error':
            return self._low_error(level)
        return self._high_error(level)

    def _low_error(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.005)
        return {
            'backbone_fraction': clamp(0.8 + noise * 0.5),
            'clause_density': 1.0 + 0.2 * level,
            'propagation_depth': clamp(0.7 + 0.02 * level + noise),
            'local_coherence': clamp(0.75 + noise),
            'search_tree_balance': clamp(0.7 + noise * 0.5),
        }

    def _high_error(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.02)
        return {
            'backbone_fraction': clamp(0.4 + noise),
            'clause_density': 3.0 + 0.8 * level,
            'propagation_depth': clamp(0.3 + 0.02 * level),
            'local_coherence': clamp(0.35 + noise),
            'search_tree_balance': clamp(0.4 + noise),
        }


# ================================================================
#  RH NEIGHBORS (use RiemannCodec keys)
# ================================================================

class RHDirichletGenerator(ClayGenerator):
    """Dirichlet L-functions: GRH for all characters."""

    def __init__(self, seed: int = 42):
        super().__init__('rh_dirichlet', seed)

    def generate(self, level: int, test_case: str = 'trivial_character') -> dict:
        if test_case == 'trivial_character':
            return self._trivial_character(level)
        return self._quadratic_character(level)

    def _trivial_character(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.005)
        t = 14.134 + level * 2.0
        return {
            'sigma': 0.5,
            't': t,
            'zeta_mag': clamp(abs(noise * 0.01)),
            'height_max': 100.0 + level * 10.0,
            'dzeta_dt': 0.5 + noise,
            'hardy_z_phase': clamp(0.5 + noise * 0.3),
            'pair_correlation': clamp(0.95 + noise * 0.5),
        }

    def _quadratic_character(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.01)
        t = 10.0 + level * 3.0
        return {
            'sigma': 0.5 + noise * 0.1,
            't': t,
            'zeta_mag': 0.1 + abs(noise),
            'height_max': 80.0 + level * 8.0,
            'dzeta_dt': 0.3 + noise,
            'hardy_z_phase': clamp(0.4 + noise * 0.5),
            'pair_correlation': clamp(0.8 + noise),
        }


class RHFunctionFieldGenerator(ClayGenerator):
    """Function field RH: proved by Deligne (Weil conjectures)."""

    def __init__(self, seed: int = 42):
        super().__init__('rh_function_field', seed)

    def generate(self, level: int, test_case: str = 'small_genus') -> dict:
        if test_case == 'small_genus':
            return self._small_genus(level)
        return self._high_genus(level)

    def _small_genus(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.003)
        return {
            'sigma': 0.5,  # All zeros on critical line (proved)
            't': 5.0 + level,
            'zeta_mag': clamp(abs(noise * 0.005)),
            'height_max': 50.0,
            'dzeta_dt': 0.3 + noise * 0.1,
            'hardy_z_phase': clamp(0.9 + noise * 0.3),
            'pair_correlation': clamp(0.98 + noise * 0.3),
        }

    def _high_genus(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.005)
        return {
            'sigma': 0.5,
            't': 20.0 + level * 5.0,
            'zeta_mag': clamp(abs(noise * 0.01)),
            'height_max': 200.0,
            'dzeta_dt': 0.4 + noise * 0.2,
            'hardy_z_phase': clamp(0.85 + noise * 0.3),
            'pair_correlation': clamp(0.95 + noise * 0.5),
        }


class RHFakeGenerator(ClayGenerator):
    """Fake zeta: L-function-like object that violates RH."""

    def __init__(self, seed: int = 42):
        super().__init__('rh_fake', seed)

    def generate(self, level: int, test_case: str = 'near_axis') -> dict:
        if test_case == 'near_axis':
            return self._near_axis(level)
        return self._off_line_fake(level)

    def _near_axis(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.01)
        return {
            'sigma': 0.5 + 0.1 * math.sin(level * 0.5),
            't': 10.0 + level * 2.0,
            'zeta_mag': 0.3 + 0.1 * math.cos(level) + noise,
            'height_max': 60.0,
            'dzeta_dt': 0.2 + noise,
            'hardy_z_phase': clamp(0.3 + noise * 0.5),
            'pair_correlation': clamp(0.5 + noise),
        }

    def _off_line_fake(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.015)
        sigma_off = 0.5 + 0.2  # Deliberately off critical line
        return {
            'sigma': sigma_off + noise * 0.1,
            't': 15.0 + level * 3.0,
            'zeta_mag': 0.5 + abs(noise),
            'height_max': 100.0,
            'dzeta_dt': 0.1 + noise * 0.5,
            'hardy_z_phase': clamp(0.2 + noise),
            'pair_correlation': clamp(0.3 + noise),
        }


# ================================================================
#  YM NEIGHBORS (use YangMillsCodec keys)
# ================================================================

class YMSchwingerGenerator(ClayGenerator):
    """Schwinger model: QED in 1+1D, exactly solvable."""

    def __init__(self, seed: int = 42):
        super().__init__('ym_schwinger', seed)

    def generate(self, level: int, test_case: str = 'weak_coupling') -> dict:
        if test_case == 'weak_coupling':
            return self._weak_coupling(level)
        return self._strong_coupling(level)

    def _weak_coupling(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.005)
        Q = round(self.rng.next_float() * 2) / 2.0  # Quantized
        return {
            'vacuum_overlap': clamp(0.9 + noise * 0.3),
            'action_density': 4.0 * math.pi ** 2 / (1.0 + level) + noise * 0.3,
            'action_max': 4.0 * math.pi ** 2,
            'momentum': 0.3 / (1.0 + level),
            'p_max': 3.0,
            'topological_charge': Q + noise * 0.01,
            'field_gradient': clamp(0.03 / (1.0 + level)),
            'gauge_invariant': clamp(0.95 + noise * 0.3),
        }

    def _strong_coupling(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.01)
        return {
            'vacuum_overlap': clamp(0.5 + noise),
            'action_density': 8.0 + noise * 2.0,
            'action_max': 20.0,
            'momentum': 2.0 / (1.0 + 0.5 * level),
            'p_max': 5.0,
            'topological_charge': 1.0 + noise * 0.1,
            'field_gradient': clamp(0.3 + noise * 0.5),
            'gauge_invariant': clamp(0.6 + noise),
        }


class YMLatticeGenerator(ClayGenerator):
    """Lattice gauge theory: Wilson action on discrete lattice."""

    def __init__(self, seed: int = 42):
        super().__init__('ym_lattice', seed)

    def generate(self, level: int, test_case: str = 'coarse_lattice') -> dict:
        if test_case == 'coarse_lattice':
            return self._coarse_lattice(level)
        return self._fine_lattice(level)

    def _coarse_lattice(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.008)
        return {
            'vacuum_overlap': clamp(0.7 + noise),
            'action_density': 6.0 / (1.0 + 0.5 * level) + noise,
            'action_max': 10.0,
            'momentum': 1.0 / (1.0 + level),
            'p_max': 4.0,
            'topological_charge': round(self.rng.next_float()) + noise * 0.05,
            'field_gradient': clamp(0.1 / (1.0 + 0.3 * level)),
            'gauge_invariant': clamp(0.8 + noise * 0.5),
        }

    def _fine_lattice(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.01)
        return {
            'vacuum_overlap': clamp(0.4 + noise),
            'action_density': 10.0 / (1.0 + 0.3 * level) + noise * 2.0,
            'action_max': 15.0,
            'momentum': 2.0 / (1.0 + 0.5 * level),
            'p_max': 6.0,
            'topological_charge': 1.5 + noise * 0.2,
            'field_gradient': clamp(0.3 + noise * 0.5),
            'gauge_invariant': clamp(0.5 + noise),
        }


class YMPhi4Generator(ClayGenerator):
    """phi^4 / Ising: scalar field theory with spontaneous symmetry breaking."""

    def __init__(self, seed: int = 42):
        super().__init__('ym_phi4', seed)

    def generate(self, level: int, test_case: str = 'ordered_phase') -> dict:
        if test_case == 'ordered_phase':
            return self._ordered_phase(level)
        return self._critical_point(level)

    def _ordered_phase(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.005)
        return {
            'vacuum_overlap': clamp(0.85 + noise * 0.3),
            'action_density': 3.0 / (1.0 + level) + noise * 0.2,
            'action_max': 5.0,
            'momentum': 0.2 / (1.0 + level),
            'p_max': 2.0,
            'topological_charge': noise * 0.01,
            'field_gradient': clamp(0.02 / (1.0 + level)),
            'gauge_invariant': clamp(0.9 + noise * 0.3),
        }

    def _critical_point(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.015)
        # At critical point, fluctuations are maximal
        return {
            'vacuum_overlap': clamp(0.5 + 0.1 * math.sin(level) + noise),
            'action_density': 5.0 * (1.0 + 0.2 * math.cos(level * 0.7)),
            'action_max': 10.0,
            'momentum': 1.5 / (1.0 + 0.3 * level),
            'p_max': 4.0,
            'topological_charge': noise * 0.3,
            'field_gradient': clamp(0.2 + 0.1 * math.sin(level * 1.3) + noise),
            'gauge_invariant': clamp(0.5 + noise),
        }


# ================================================================
#  BSD NEIGHBORS (use BSDCodec keys)
# ================================================================

class BSDFunctionFieldGenerator(ClayGenerator):
    """Function field BSD: proved by Artin-Tate."""

    def __init__(self, seed: int = 42):
        super().__init__('bsd_function_field', seed)

    def generate(self, level: int, test_case: str = 'rank0_ff') -> dict:
        if test_case == 'rank0_ff':
            return self._rank0_ff(level)
        return self._high_rank_ff(level)

    def _rank0_ff(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.003)
        return {
            'rank_analytic': 0,
            'rank_algebraic': 0,
            'regulator': 1.0 + abs(noise),
            'reg_max': 5.0,
            'conductor': 10.0 + level,
            'sha_order': 1.0,
            'torsion_order': max(1, int(2 + self.rng.next_float() * 3)),
        }

    def _high_rank_ff(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.005)
        rank = min(level // 3 + 1, 5)
        return {
            'rank_analytic': rank,
            'rank_algebraic': rank,
            'regulator': 2.0 + level * 0.5 + abs(noise),
            'reg_max': 20.0,
            'conductor': 50.0 + level * 10.0,
            'sha_order': 1.0,
            'torsion_order': max(1, int(1 + self.rng.next_float() * 2)),
        }


class BSDAvgRankGenerator(ClayGenerator):
    """Average rank of elliptic curve families."""

    def __init__(self, seed: int = 42):
        super().__init__('bsd_avg_rank', seed)

    def generate(self, level: int, test_case: str = 'small_family') -> dict:
        if test_case == 'small_family':
            return self._small_family(level)
        return self._large_family(level)

    def _small_family(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.005)
        rank = int(self.rng.next_float() < 0.5)  # ~50% rank 0, ~50% rank 1
        return {
            'rank_analytic': rank,
            'rank_algebraic': rank,
            'regulator': 1.0 + abs(noise) * 2.0,
            'reg_max': 8.0,
            'conductor': 20.0 + level * 5.0,
            'sha_order': 1.0,
            'torsion_order': max(1, int(1 + self.rng.next_float() * 4)),
        }

    def _large_family(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.01)
        rank_a = int(self.rng.next_float() * 3)
        rank_b = rank_a + (1 if self.rng.next_float() < 0.3 else 0)
        return {
            'rank_analytic': rank_a,
            'rank_algebraic': rank_b,
            'regulator': 3.0 + level * 0.8 + abs(noise),
            'reg_max': 25.0,
            'conductor': 100.0 + level * 20.0,
            'sha_order': max(1.0, 1.0 + abs(noise) * 5.0),
            'torsion_order': max(1, int(1 + self.rng.next_float() * 6)),
        }


class BSDSatoTateGenerator(ClayGenerator):
    """Sato-Tate distribution of Frobenius angles."""

    def __init__(self, seed: int = 42):
        super().__init__('bsd_sato_tate', seed)

    def generate(self, level: int, test_case: str = 'cm_curve') -> dict:
        if test_case == 'cm_curve':
            return self._cm_curve(level)
        return self._non_cm_curve(level)

    def _cm_curve(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.003)
        return {
            'rank_analytic': 0,
            'rank_algebraic': 0,
            'regulator': 1.0,
            'reg_max': 3.0,
            'conductor': 11.0 + level,
            'sha_order': 1.0,
            'torsion_order': 2,
        }

    def _non_cm_curve(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.008)
        rank = int(self.rng.next_float() < 0.4)
        return {
            'rank_analytic': rank,
            'rank_algebraic': rank,
            'regulator': 1.5 + abs(noise) * 3.0,
            'reg_max': 10.0,
            'conductor': 37.0 + level * 7.0,
            'sha_order': 1.0,
            'torsion_order': max(1, int(1 + self.rng.next_float() * 5)),
        }


# ================================================================
#  HODGE NEIGHBORS (use HodgeCodec keys)
# ================================================================

class HodgeTateGenerator(ClayGenerator):
    """Tate conjecture: l-adic analogue of Hodge."""

    def __init__(self, seed: int = 42):
        super().__init__('hodge_tate', seed)

    def generate(self, level: int, test_case: str = 'abelian_variety') -> dict:
        if test_case == 'abelian_variety':
            return self._abelian_variety(level)
        return self._higher_codimension(level)

    def _abelian_variety(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.005)
        return {
            'algebraic_projection': clamp(0.9 + noise * 0.3),
            'analytic_residual': clamp(0.05 + abs(noise)),
            'dimension': max(1, 2 + level // 4),
            'period_coherence': clamp(0.85 + noise * 0.3),
            'residual_gradient': clamp(0.05 + abs(noise) * 0.5),
        }

    def _higher_codimension(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.01)
        return {
            'algebraic_projection': clamp(0.5 + noise),
            'analytic_residual': clamp(0.3 + 0.02 * level + abs(noise)),
            'dimension': max(1, 4 + level // 3),
            'period_coherence': clamp(0.5 + noise),
            'residual_gradient': clamp(0.2 + 0.01 * level + abs(noise)),
        }


class HodgeStandardGenerator(ClayGenerator):
    """Standard conjectures: Kunneth projectors, Lefschetz standard."""

    def __init__(self, seed: int = 42):
        super().__init__('hodge_standard', seed)

    def generate(self, level: int, test_case: str = 'smooth_projective') -> dict:
        if test_case == 'smooth_projective':
            return self._smooth_projective(level)
        return self._singular_variety(level)

    def _smooth_projective(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.005)
        return {
            'algebraic_projection': clamp(0.85 + noise * 0.3),
            'analytic_residual': clamp(0.08 + abs(noise)),
            'dimension': max(1, 3 + level // 5),
            'period_coherence': clamp(0.8 + noise * 0.3),
            'residual_gradient': clamp(0.06 + abs(noise) * 0.5),
        }

    def _singular_variety(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.012)
        return {
            'algebraic_projection': clamp(0.4 + noise),
            'analytic_residual': clamp(0.35 + 0.015 * level + abs(noise)),
            'dimension': max(1, 5 + level // 3),
            'period_coherence': clamp(0.45 + noise),
            'residual_gradient': clamp(0.25 + 0.01 * level + abs(noise)),
        }


class HodgeTranscendentalGenerator(ClayGenerator):
    """Non-algebraic Hodge classes: potential counterexamples."""

    def __init__(self, seed: int = 42):
        super().__init__('hodge_transcendental', seed)

    def generate(self, level: int, test_case: str = 'k3_surface') -> dict:
        if test_case == 'k3_surface':
            return self._k3_surface(level)
        return self._high_dimension_class(level)

    def _k3_surface(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.008)
        return {
            'algebraic_projection': clamp(0.6 + noise),
            'analytic_residual': clamp(0.2 + 0.01 * level + abs(noise)),
            'dimension': max(1, 2 + level // 6),
            'period_coherence': clamp(0.55 + noise),
            'residual_gradient': clamp(0.15 + abs(noise)),
        }

    def _high_dimension_class(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.015)
        return {
            'algebraic_projection': clamp(0.25 + noise),
            'analytic_residual': clamp(0.5 + 0.02 * level + abs(noise)),
            'dimension': max(1, 6 + level // 2),
            'period_coherence': clamp(0.3 + noise),
            'residual_gradient': clamp(0.35 + 0.015 * level + abs(noise)),
        }


# ================================================================
#  REGISTRY
# ================================================================

NEIGHBOR_GENERATOR_REGISTRY = {
    'ns_2d': NS2DGenerator,
    'ns_sqg': NSSQGGenerator,
    'ns_euler': NSEulerGenerator,
    'pnp_ac0': PnpAC0Generator,
    'pnp_clique': PnpCliqueGenerator,
    'pnp_bpp': PnpBPPGenerator,
    'rh_dirichlet': RHDirichletGenerator,
    'rh_function_field': RHFunctionFieldGenerator,
    'rh_fake': RHFakeGenerator,
    'ym_schwinger': YMSchwingerGenerator,
    'ym_lattice': YMLatticeGenerator,
    'ym_phi4': YMPhi4Generator,
    'bsd_function_field': BSDFunctionFieldGenerator,
    'bsd_avg_rank': BSDAvgRankGenerator,
    'bsd_sato_tate': BSDSatoTateGenerator,
    'hodge_tate': HodgeTateGenerator,
    'hodge_standard': HodgeStandardGenerator,
    'hodge_transcendental': HodgeTranscendentalGenerator,
}
