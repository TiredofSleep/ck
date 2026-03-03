"""
ck_expansion_generators.py -- Generators for 17 Expansion Problems
==================================================================
Operator: PROGRESS (3) -- New domains, new data.

13 standalone generators + 4 bridge generators.
Each produces raw_reading dicts matching its corresponding expansion codec.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
from typing import Dict

from ck_sim.being.ck_sdv_safety import DeterministicRNG, clamp, safe_div, safe_log
from ck_sim.doing.ck_clay_generators import ClayGenerator


# ================================================================
#  COLLATZ
# ================================================================

class CollatzGenerator(ClayGenerator):
    """Collatz orbit generator."""

    def __init__(self, seed: int = 42):
        super().__init__('collatz', seed)

    def generate(self, level: int, test_case: str = 'small_orbit') -> dict:
        if test_case == 'large_orbit':
            return self._large_orbit(level)
        return self._small_orbit(level)

    def _small_orbit(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.005)
        n = 7 + level * 3
        orbit = int(10 + 3 * math.log(n + 1) + noise * 2)
        predicted = int(10 + 3 * math.log(n + 1))
        return {
            'orbit_length': max(1, orbit),
            'predicted_length': max(1, predicted),
            'max_value': max(n, int(n * (1.5 + abs(noise)))),
            'start_value': n,
            'log_shrinkage': clamp(0.7 + noise * 0.3),
        }

    def _large_orbit(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.01)
        n = 1000 + level * 500
        orbit = int(50 + 10 * math.log(n + 1) + noise * 10)
        predicted = int(45 + 10 * math.log(n + 1))
        return {
            'orbit_length': max(1, orbit),
            'predicted_length': max(1, predicted),
            'max_value': max(n, int(n * 3 + abs(noise) * 100)),
            'start_value': n,
            'log_shrinkage': clamp(0.5 + noise),
        }


class ABCGenerator(ClayGenerator):
    """ABC triple generator."""

    def __init__(self, seed: int = 42):
        super().__init__('abc', seed)

    def generate(self, level: int, test_case: str = 'low_quality') -> dict:
        if test_case == 'high_quality':
            return self._high_quality(level)
        return self._low_quality(level)

    def _low_quality(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.005)
        c_val = 10 + level * 5
        rad_val = c_val * (0.9 + abs(noise))
        return {
            'log_c': safe_log(max(c_val, 1)),
            'log_rad': safe_log(max(rad_val, 1)),
            'quality': 1.0 + abs(noise) * 0.1,
        }

    def _high_quality(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.01)
        c_val = 100 + level * 50
        rad_val = c_val ** 0.7  # High quality: rad << c
        return {
            'log_c': safe_log(max(c_val, 1)),
            'log_rad': safe_log(max(rad_val, 1)),
            'quality': 1.5 + 0.1 * level + abs(noise),
        }


class LanglandsGenerator(ClayGenerator):
    """Langlands functoriality generator."""

    def __init__(self, seed: int = 42):
        super().__init__('langlands', seed)

    def generate(self, level: int, test_case: str = 'gl2_case') -> dict:
        if test_case == 'gl3_case':
            return self._gl3_case(level)
        return self._gl2_case(level)

    def _gl2_case(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.005)
        return {
            'local_dim': 2,
            'conductor': 11 + level * 5,
            'automorphic_level': 11 + level * 5 + int(noise * 2),
            'l_value': clamp(0.5 + noise * 0.3),
            'transfer_score': clamp(0.85 + noise * 0.3),
        }

    def _gl3_case(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.01)
        return {
            'local_dim': 3,
            'conductor': 50 + level * 20,
            'automorphic_level': 50 + level * 20 + int(noise * 5),
            'l_value': clamp(0.3 + noise),
            'transfer_score': clamp(0.5 + noise),
        }


class ContinuumGenerator(ClayGenerator):
    """Continuum hypothesis generator."""

    def __init__(self, seed: int = 42):
        super().__init__('continuum', seed)

    def generate(self, level: int, test_case: str = 'constructible') -> dict:
        if test_case == 'forcing_extension':
            return self._forcing(level)
        return self._constructible(level)

    def _constructible(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.005)
        return {
            'constructible_rank': 1,
            'forcing_rank': 1 + int(abs(noise) * 2),
        }

    def _forcing(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.01)
        return {
            'constructible_rank': 1,
            'forcing_rank': 2 + level // 5 + int(abs(noise) * 3),
        }


class RamseyGenerator(ClayGenerator):
    """Ramsey number bounds generator."""

    def __init__(self, seed: int = 42):
        super().__init__('ramsey', seed)

    def generate(self, level: int, test_case: str = 'small_colors') -> dict:
        if test_case == 'many_colors':
            return self._many_colors(level)
        return self._small_colors(level)

    def _small_colors(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.005)
        k = 3
        lower = max(1, int(2 ** (k + level * 0.3) + noise * 2))
        upper = max(lower + 1, int(4 ** (k + level * 0.2) + abs(noise) * 5))
        return {
            'lower_bound': lower,
            'upper_bound': upper,
            'probabilistic_bound': int((lower + upper) / 2),
        }

    def _many_colors(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.01)
        k = 4 + level // 3
        lower = max(1, int(2 ** k + noise * 5))
        upper = max(lower + 10, int(4 ** k + abs(noise) * 20))
        return {
            'lower_bound': lower,
            'upper_bound': upper,
            'probabilistic_bound': int((lower + upper) / 3),
        }


class TwinPrimesGenerator(ClayGenerator):
    """Twin primes gap generator."""

    def __init__(self, seed: int = 42):
        super().__init__('twin_primes', seed)

    def generate(self, level: int, test_case: str = 'small_gap') -> dict:
        if test_case == 'large_gap':
            return self._large_gap(level)
        return self._small_gap(level)

    def _small_gap(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.005)
        return {
            'sieve_prediction': clamp(0.8 + noise * 0.3),
            'actual_gap': 2,  # Twin prime
            'prime_density': clamp(0.3 - 0.01 * level + noise),
        }

    def _large_gap(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.01)
        gap = max(2, int(2 * math.log(10 + level * 50) + abs(noise) * 4))
        gap = gap + (gap % 2)  # Make even
        return {
            'sieve_prediction': clamp(0.3 + noise),
            'actual_gap': gap,
            'prime_density': clamp(0.1 - 0.005 * level + noise),
        }


class Poincare4DGenerator(ClayGenerator):
    """Smooth 4D Poincare generator."""

    def __init__(self, seed: int = 42):
        super().__init__('poincare_4d', seed)

    def generate(self, level: int, test_case: str = 'standard_sphere') -> dict:
        if test_case == 'exotic_candidate':
            return self._exotic(level)
        return self._standard(level)

    def _standard(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.005)
        return {
            'topological_invariant': clamp(0.95 + noise * 0.3),
            'smooth_invariant': clamp(0.95 + noise * 0.3),
            'surgery_score': clamp(0.9 + noise * 0.3),
        }

    def _exotic(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.015)
        return {
            'topological_invariant': clamp(0.9 + noise),
            'smooth_invariant': clamp(0.5 + noise),
            'surgery_score': clamp(0.3 + noise),
        }


class CosmoConstantGenerator(ClayGenerator):
    """Cosmological constant generator."""

    def __init__(self, seed: int = 42):
        super().__init__('cosmo_constant', seed)

    def generate(self, level: int, test_case: str = 'low_cutoff') -> dict:
        if test_case == 'planck_cutoff':
            return self._planck(level)
        return self._low_cutoff(level)

    def _low_cutoff(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.01)
        cutoff = 1e10 * (1.0 + level * 2.0)
        return {
            'qft_vacuum_energy': cutoff ** 2,
            'observed_lambda': 1e-52 * (1.0 + noise * 0.1),
        }

    def _planck(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.01)
        return {
            'qft_vacuum_energy': 1e76 * (1.0 + noise * 0.01),
            'observed_lambda': 1e-52 * (1.0 + noise * 0.05),
        }


class FalconerGenerator(ClayGenerator):
    """Falconer distance problem generator."""

    def __init__(self, seed: int = 42):
        super().__init__('falconer', seed)

    def generate(self, level: int, test_case: str = 'high_dimension') -> dict:
        if test_case == 'threshold_dimension':
            return self._threshold(level)
        return self._high_dim(level)

    def _high_dim(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.005)
        d = 2
        h_dim = d / 2.0 + 0.3 + 0.02 * level + noise * 0.1
        return {
            'hausdorff_dim': max(0.01, h_dim),
            'ambient_dim': d,
            'distance_measure': clamp(0.8 + noise * 0.3),
        }

    def _threshold(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.01)
        d = 2
        h_dim = d / 2.0 + noise * 0.1  # Right at threshold
        return {
            'hausdorff_dim': max(0.01, h_dim),
            'ambient_dim': d,
            'distance_measure': clamp(0.4 + noise),
        }


class JacobianGenerator(ClayGenerator):
    """Jacobian conjecture generator."""

    def __init__(self, seed: int = 42):
        super().__init__('jacobian', seed)

    def generate(self, level: int, test_case: str = 'degree_2') -> dict:
        if test_case == 'degree_5':
            return self._degree_5(level)
        return self._degree_2(level)

    def _degree_2(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.005)
        return {
            'jacobian_det': 1.0 + noise * 0.01,  # Constant nonzero
            'injectivity_score': clamp(0.95 + noise * 0.3),
            'degree': 2,
        }

    def _degree_5(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.01)
        return {
            'jacobian_det': 1.0 + noise * 0.05,
            'injectivity_score': clamp(0.6 + noise),
            'degree': 5,
        }


class InverseGaloisGenerator(ClayGenerator):
    """Inverse Galois problem generator."""

    def __init__(self, seed: int = 42):
        super().__init__('inverse_galois', seed)

    def generate(self, level: int, test_case: str = 'cyclic_group') -> dict:
        if test_case == 'sporadic_group':
            return self._sporadic(level)
        return self._cyclic(level)

    def _cyclic(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.003)
        order = max(2, 5 + level)
        return {
            'group_order': order,
            'realization_degree': order,
            'realization_fraction': clamp(0.95 + noise * 0.3),
        }

    def _sporadic(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.01)
        order = max(60, 60 * (1 + level))
        return {
            'group_order': order,
            'realization_degree': order * (2 + level),
            'realization_fraction': clamp(0.3 + noise),
        }


class BanachTarskiGenerator(ClayGenerator):
    """Banach-Tarski paradox generator."""

    def __init__(self, seed: int = 42):
        super().__init__('banach_tarski', seed)

    def generate(self, level: int, test_case: str = 'dimension_2') -> dict:
        if test_case == 'dimension_3':
            return self._dim_3(level)
        return self._dim_2(level)

    def _dim_2(self, level: int) -> dict:
        return {
            'dimension': 2,
            'amenability_score': 1.0,  # Amenable in d=2
            'n_pieces': 0,
        }

    def _dim_3(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.005)
        return {
            'dimension': 3,
            'amenability_score': 0.0,  # Non-amenable in d>=3
            'n_pieces': 5,
        }


class InfoParadoxGenerator(ClayGenerator):
    """Black hole information paradox generator."""

    def __init__(self, seed: int = 42):
        super().__init__('info_paradox', seed)

    def generate(self, level: int, test_case: str = 'large_bh') -> dict:
        if test_case == 'small_bh':
            return self._small_bh(level)
        return self._large_bh(level)

    def _large_bh(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.005)
        t = 0.1 * level  # Time evolution parameter
        s_h = 1.0 * (1.0 - 0.02 * t)  # Hawking: slowly decreasing
        s_p = 0.5 * (1.0 + 0.05 * t)  # Page: slowly increasing
        return {
            'hawking_entropy': max(0.01, s_h + noise * 0.05),
            'page_entropy': max(0.01, s_p + noise * 0.05),
            'scrambling_time': clamp(0.3 + 0.03 * level + noise),
        }

    def _small_bh(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.01)
        t = 0.2 * level
        s_h = 0.5 * math.exp(-0.1 * t)
        s_p = 0.5 * (1.0 - math.exp(-0.2 * t))
        return {
            'hawking_entropy': max(0.01, s_h + noise * 0.05),
            'page_entropy': max(0.01, s_p + noise * 0.05),
            'scrambling_time': clamp(0.5 + 0.05 * level + noise),
        }


# ================================================================
#  BRIDGE GENERATORS
# ================================================================

class BridgeRMTGenerator(ClayGenerator):
    """Random Matrix Theory bridge generator."""

    def __init__(self, seed: int = 42):
        super().__init__('bridge_rmt', seed)

    def generate(self, level: int, test_case: str = 'low_zeros') -> dict:
        if test_case == 'high_zeros':
            return self._high_zeros(level)
        return self._low_zeros(level)

    def _low_zeros(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.005)
        gue = 0.8 + noise * 0.1
        empirical = gue + noise * 0.05  # Close to GUE
        return {
            'spacing_distribution': clamp(empirical),
            'gue_prediction': clamp(gue),
        }

    def _high_zeros(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.01)
        gue = 0.85 + noise * 0.05
        empirical = gue + noise * 0.15  # Some deviation
        return {
            'spacing_distribution': clamp(empirical),
            'gue_prediction': clamp(gue),
        }


class BridgeExpanderGenerator(ClayGenerator):
    """Expander graphs bridge generator."""

    def __init__(self, seed: int = 42):
        super().__init__('bridge_expander', seed)

    def generate(self, level: int, test_case: str = 'regular_graph') -> dict:
        if test_case == 'ramanujan_graph':
            return self._ramanujan(level)
        return self._regular(level)

    def _regular(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.005)
        gap = 0.3 + 0.02 * level + noise * 0.05
        mixing = max(1, int(1.0 / max(gap, 0.01) + noise * 2))
        return {
            'spectral_gap': max(0.01, gap),
            'mixing_time': mixing,
        }

    def _ramanujan(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.008)
        k = 3 + level // 2
        gap = 1.0 - 2.0 * math.sqrt(k - 1) / k + noise * 0.02
        mixing = max(1, int(safe_log(10 + level * 5) / max(gap, 0.01)))
        return {
            'spectral_gap': max(0.01, gap),
            'mixing_time': mixing,
        }


class BridgeFractalGenerator(ClayGenerator):
    """Multi-fractal cascades bridge generator."""

    def __init__(self, seed: int = 42):
        super().__init__('bridge_fractal', seed)

    def generate(self, level: int, test_case: str = 'k41_cascade') -> dict:
        if test_case == 'intermittent_cascade':
            return self._intermittent(level)
        return self._k41(level)

    def _k41(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.005)
        # Kolmogorov 1941: tau(q) = q/3
        tau_ns = 1.0 / 3.0 + noise * 0.02
        tau_zeta = 1.0 / 3.0 + noise * 0.03
        return {
            'cascade_exponent': clamp(tau_ns),
            'zeta_exponent': clamp(tau_zeta),
        }

    def _intermittent(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.01)
        tau_ns = 0.3 + 0.05 * math.sin(level * 0.5) + noise
        tau_zeta = 0.35 + noise * 0.1
        return {
            'cascade_exponent': clamp(tau_ns),
            'zeta_exponent': clamp(tau_zeta),
        }


class BridgeSpectralGenerator(ClayGenerator):
    """Universal spectral gaps bridge generator."""

    def __init__(self, seed: int = 42):
        super().__init__('bridge_spectral', seed)

    def generate(self, level: int, test_case: str = 'laplacian') -> dict:
        if test_case == 'dirac_operator':
            return self._dirac(level)
        return self._laplacian(level)

    def _laplacian(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.005)
        energy = 1.0 + 0.1 * level
        gap = 0.3 + noise * 0.05
        return {
            'operator_gap': max(0.01, gap),
            'ground_state_energy': max(0.01, energy + noise * 0.1),
        }

    def _dirac(self, level: int) -> dict:
        noise = self.rng.next_gauss(0.0, 0.01)
        energy = 2.0 + 0.2 * level
        gap = 0.5 + noise * 0.1
        return {
            'operator_gap': max(0.01, gap),
            'ground_state_energy': max(0.01, energy + noise * 0.2),
        }


# ================================================================
#  REGISTRY
# ================================================================

EXPANSION_GENERATOR_REGISTRY = {
    'collatz': CollatzGenerator,
    'abc': ABCGenerator,
    'langlands': LanglandsGenerator,
    'continuum': ContinuumGenerator,
    'ramsey': RamseyGenerator,
    'twin_primes': TwinPrimesGenerator,
    'poincare_4d': Poincare4DGenerator,
    'cosmo_constant': CosmoConstantGenerator,
    'falconer': FalconerGenerator,
    'jacobian': JacobianGenerator,
    'inverse_galois': InverseGaloisGenerator,
    'banach_tarski': BanachTarskiGenerator,
    'info_paradox': InfoParadoxGenerator,
    'bridge_rmt': BridgeRMTGenerator,
    'bridge_expander': BridgeExpanderGenerator,
    'bridge_fractal': BridgeFractalGenerator,
    'bridge_spectral': BridgeSpectralGenerator,
}
