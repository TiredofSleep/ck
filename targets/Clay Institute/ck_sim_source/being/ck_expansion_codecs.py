"""
ck_expansion_codecs.py -- Codecs for 17 Expansion Problems (13 standalone + 4 bridges)
======================================================================================
Operator: COUNTER (2) -- CK measures new domains.

Each codec maps domain-specific raw readings into CK's 5D force space:
  [aperture, pressure, depth, binding, continuity]

Every codec implements:
  - map_to_force_vector(raw) -> 5D vector
  - lens_a(raw) -> local measurements
  - lens_b(raw) -> global measurements
  - master_lemma_defect(raw) -> float (per-problem delta)

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
from typing import List

from ck_sim.being.ck_clay_codecs import ClayCodec
from ck_sim.being.ck_sdv_safety import clamp, safe_div, safe_log, safe_sqrt


# ================================================================
#  COLLATZ CONJECTURE
# ================================================================

class CollatzCodec(ClayCodec):
    """Collatz: orbit length vs statistical prediction."""

    def __init__(self):
        super().__init__('collatz_codec', 'collatz')

    def map_to_force_vector(self, raw: dict) -> List[float]:
        orbit = raw.get('orbit_length', 10)
        predicted = raw.get('predicted_length', 10)
        max_val = raw.get('max_value', 100)
        start_val = raw.get('start_value', 10)
        shrinkage = raw.get('log_shrinkage', 0.5)

        aperture = clamp(safe_div(orbit, predicted + orbit))
        pressure = clamp(safe_div(safe_log(max_val + 1), safe_log(start_val + 1)))
        depth = clamp(shrinkage)
        binding = clamp(1.0 - abs(orbit - predicted) / max(orbit, predicted, 1))
        continuity = clamp(1.0 / (1.0 + abs(orbit - predicted)))
        return [aperture, pressure, depth, binding, continuity]

    def lens_a(self, raw: dict) -> List[float]:
        return [raw.get('orbit_length', 10), raw.get('max_value', 100)]

    def lens_b(self, raw: dict) -> List[float]:
        return [raw.get('predicted_length', 10), raw.get('log_shrinkage', 0.5)]

    def master_lemma_defect(self, raw: dict) -> float:
        orbit = raw.get('orbit_length', 10)
        predicted = raw.get('predicted_length', 10)
        return clamp(abs(orbit - predicted) / max(orbit, predicted, 1))


class ABCCodec(ClayCodec):
    """ABC: additive size vs multiplicative size."""

    def __init__(self):
        super().__init__('abc_codec', 'abc')

    def map_to_force_vector(self, raw: dict) -> List[float]:
        log_c = raw.get('log_c', 1.0)
        log_rad = raw.get('log_rad', 1.0)
        quality = raw.get('quality', 1.0)

        aperture = clamp(safe_div(log_c, log_c + log_rad))
        pressure = clamp(quality / 2.0)
        depth = clamp(safe_div(log_rad, log_c + 1e-10))
        binding = clamp(1.0 / (1.0 + abs(quality - 1.0)))
        continuity = clamp(safe_div(log_rad, log_c) if log_c > 0 else 0.5)
        return [aperture, pressure, depth, binding, continuity]

    def lens_a(self, raw: dict) -> List[float]:
        return [raw.get('log_c', 1.0)]

    def lens_b(self, raw: dict) -> List[float]:
        return [raw.get('log_rad', 1.0)]

    def master_lemma_defect(self, raw: dict) -> float:
        log_c = raw.get('log_c', 1.0)
        log_rad = raw.get('log_rad', 1.0)
        if log_rad < 1e-10:
            return 1.0
        return clamp(log_c / log_rad - 1.0)


class LanglandsCodec(ClayCodec):
    """Langlands: local representation vs global automorphic form."""

    def __init__(self):
        super().__init__('langlands_codec', 'langlands')

    def map_to_force_vector(self, raw: dict) -> List[float]:
        local_dim = raw.get('local_dim', 2)
        conductor = raw.get('conductor', 100)
        auto_level = raw.get('automorphic_level', 100)
        l_value = raw.get('l_value', 0.5)
        transfer = raw.get('transfer_score', 0.5)

        aperture = clamp(safe_div(local_dim, local_dim + 4))
        pressure = clamp(safe_div(safe_log(conductor + 1), 10.0))
        depth = clamp(safe_div(safe_log(auto_level + 1), 10.0))
        binding = clamp(transfer)
        continuity = clamp(l_value)
        return [aperture, pressure, depth, binding, continuity]

    def lens_a(self, raw: dict) -> List[float]:
        return [raw.get('local_dim', 2), raw.get('conductor', 100)]

    def lens_b(self, raw: dict) -> List[float]:
        return [raw.get('automorphic_level', 100), raw.get('l_value', 0.5)]

    def master_lemma_defect(self, raw: dict) -> float:
        return clamp(1.0 - raw.get('transfer_score', 0.5))


class ContinuumCodec(ClayCodec):
    """Continuum hypothesis: constructible rank vs forcing rank."""

    def __init__(self):
        super().__init__('continuum_codec', 'continuum')

    def map_to_force_vector(self, raw: dict) -> List[float]:
        l_rank = raw.get('constructible_rank', 1)
        f_rank = raw.get('forcing_rank', 2)

        aperture = clamp(safe_div(l_rank, l_rank + f_rank))
        pressure = clamp(safe_div(abs(l_rank - f_rank), max(l_rank, f_rank, 1)))
        depth = clamp(0.5)  # Structural: always indeterminate
        binding = clamp(1.0 / (1.0 + abs(l_rank - f_rank)))
        continuity = clamp(0.5)
        return [aperture, pressure, depth, binding, continuity]

    def lens_a(self, raw: dict) -> List[float]:
        return [raw.get('constructible_rank', 1)]

    def lens_b(self, raw: dict) -> List[float]:
        return [raw.get('forcing_rank', 2)]

    def master_lemma_defect(self, raw: dict) -> float:
        l_rank = raw.get('constructible_rank', 1)
        f_rank = raw.get('forcing_rank', 2)
        return clamp(abs(l_rank - f_rank) / max(l_rank, f_rank, 1))


class RamseyCodec(ClayCodec):
    """Ramsey bounds: probabilistic vs structural bounds."""

    def __init__(self):
        super().__init__('ramsey_codec', 'ramsey')

    def map_to_force_vector(self, raw: dict) -> List[float]:
        lower = max(raw.get('lower_bound', 1), 1)
        upper = max(raw.get('upper_bound', 10), 1)
        prob_bound = raw.get('probabilistic_bound', 5)

        aperture = clamp(safe_div(safe_log(lower + 1), safe_log(upper + 1)))
        pressure = clamp(safe_div(upper - lower, upper))
        depth = clamp(safe_div(safe_log(prob_bound + 1), safe_log(upper + 1)))
        binding = clamp(safe_div(lower, upper))
        continuity = clamp(1.0 / (1.0 + safe_log(upper) - safe_log(lower)))
        return [aperture, pressure, depth, binding, continuity]

    def lens_a(self, raw: dict) -> List[float]:
        return [raw.get('probabilistic_bound', 5)]

    def lens_b(self, raw: dict) -> List[float]:
        return [raw.get('upper_bound', 10)]

    def master_lemma_defect(self, raw: dict) -> float:
        lower = max(raw.get('lower_bound', 1), 1)
        upper = max(raw.get('upper_bound', 10), 1)
        return clamp(safe_log(upper) / max(safe_log(lower), 0.01) - 1.0)


class TwinPrimesCodec(ClayCodec):
    """Twin primes: sieve prediction vs actual gap."""

    def __init__(self):
        super().__init__('twin_primes_codec', 'twin_primes')

    def map_to_force_vector(self, raw: dict) -> List[float]:
        sieve_pred = raw.get('sieve_prediction', 0.5)
        actual_gap = raw.get('actual_gap', 2)
        prime_density = raw.get('prime_density', 0.1)

        aperture = clamp(sieve_pred)
        pressure = clamp(safe_div(actual_gap, actual_gap + 10))
        depth = clamp(prime_density)
        binding = clamp(1.0 if actual_gap == 2 else 0.5 / (actual_gap / 2.0))
        continuity = clamp(1.0 / (1.0 + abs(actual_gap - 2)))
        return [aperture, pressure, depth, binding, continuity]

    def lens_a(self, raw: dict) -> List[float]:
        return [raw.get('sieve_prediction', 0.5)]

    def lens_b(self, raw: dict) -> List[float]:
        return [raw.get('actual_gap', 2)]

    def master_lemma_defect(self, raw: dict) -> float:
        gap = raw.get('actual_gap', 2)
        return clamp(gap / 2.0 - 1.0)


class Poincare4DCodec(ClayCodec):
    """Smooth 4D Poincare: topological vs smooth invariant."""

    def __init__(self):
        super().__init__('poincare_4d_codec', 'poincare_4d')

    def map_to_force_vector(self, raw: dict) -> List[float]:
        top_inv = raw.get('topological_invariant', 0.0)
        smooth_inv = raw.get('smooth_invariant', 0.0)
        surgery_score = raw.get('surgery_score', 0.5)

        aperture = clamp(top_inv)
        pressure = clamp(abs(top_inv - smooth_inv))
        depth = clamp(surgery_score)
        binding = clamp(1.0 - abs(top_inv - smooth_inv))
        continuity = clamp(0.5 * (top_inv + smooth_inv))
        return [aperture, pressure, depth, binding, continuity]

    def lens_a(self, raw: dict) -> List[float]:
        return [raw.get('topological_invariant', 0.0)]

    def lens_b(self, raw: dict) -> List[float]:
        return [raw.get('smooth_invariant', 0.0)]

    def master_lemma_defect(self, raw: dict) -> float:
        return clamp(abs(raw.get('topological_invariant', 0.0)
                         - raw.get('smooth_invariant', 0.0)))


class CosmoConstantCodec(ClayCodec):
    """Cosmological constant: QFT vacuum energy vs observed Lambda."""

    def __init__(self):
        super().__init__('cosmo_constant_codec', 'cosmo_constant')

    def map_to_force_vector(self, raw: dict) -> List[float]:
        qft_energy = raw.get('qft_vacuum_energy', 1e60)
        observed = raw.get('observed_lambda', 1e-52)
        log_ratio = safe_log(max(qft_energy, 1e-100)) - safe_log(max(observed, 1e-100))

        aperture = clamp(safe_div(safe_log(max(observed, 1e-100) + 1), 10.0))
        pressure = clamp(min(abs(log_ratio) / 300.0, 1.0))
        depth = clamp(0.5)
        binding = clamp(1.0 / (1.0 + abs(log_ratio) / 10.0))
        continuity = clamp(1.0 / (1.0 + abs(log_ratio) / 50.0))
        return [aperture, pressure, depth, binding, continuity]

    def lens_a(self, raw: dict) -> List[float]:
        return [safe_log(max(raw.get('qft_vacuum_energy', 1e60), 1e-100))]

    def lens_b(self, raw: dict) -> List[float]:
        return [safe_log(max(raw.get('observed_lambda', 1e-52), 1e-100))]

    def master_lemma_defect(self, raw: dict) -> float:
        qft = max(raw.get('qft_vacuum_energy', 1e60), 1e-100)
        obs = max(raw.get('observed_lambda', 1e-52), 1e-100)
        ratio = safe_log(qft) - safe_log(obs)
        return clamp(min(abs(ratio) / 300.0, 1.0))


class FalconerCodec(ClayCodec):
    """Falconer distance: Hausdorff dimension vs distance set measure."""

    def __init__(self):
        super().__init__('falconer_codec', 'falconer')

    def map_to_force_vector(self, raw: dict) -> List[float]:
        h_dim = raw.get('hausdorff_dim', 1.0)
        ambient_d = raw.get('ambient_dim', 2)
        dist_measure = raw.get('distance_measure', 0.5)
        threshold = ambient_d / 2.0

        aperture = clamp(safe_div(h_dim, ambient_d))
        pressure = clamp(max(0, threshold - h_dim) / max(threshold, 0.01))
        depth = clamp(dist_measure)
        binding = clamp(1.0 if h_dim > threshold else h_dim / max(threshold, 0.01))
        continuity = clamp(dist_measure)
        return [aperture, pressure, depth, binding, continuity]

    def lens_a(self, raw: dict) -> List[float]:
        return [raw.get('hausdorff_dim', 1.0)]

    def lens_b(self, raw: dict) -> List[float]:
        return [raw.get('distance_measure', 0.5)]

    def master_lemma_defect(self, raw: dict) -> float:
        h_dim = raw.get('hausdorff_dim', 1.0)
        ambient_d = raw.get('ambient_dim', 2)
        threshold = ambient_d / 2.0
        return clamp(max(0, threshold - h_dim) / max(threshold, 0.01))


class JacobianCodec(ClayCodec):
    """Jacobian conjecture: local det vs global injectivity."""

    def __init__(self):
        super().__init__('jacobian_codec', 'jacobian')

    def map_to_force_vector(self, raw: dict) -> List[float]:
        det = raw.get('jacobian_det', 1.0)
        injectivity = raw.get('injectivity_score', 0.5)
        degree = raw.get('degree', 2)

        aperture = clamp(safe_div(abs(det), abs(det) + 1.0))
        pressure = clamp(safe_div(degree, degree + 5))
        depth = clamp(injectivity)
        binding = clamp(injectivity)
        continuity = clamp(1.0 if abs(det) > 0.01 else 0.0)
        return [aperture, pressure, depth, binding, continuity]

    def lens_a(self, raw: dict) -> List[float]:
        return [raw.get('jacobian_det', 1.0)]

    def lens_b(self, raw: dict) -> List[float]:
        return [raw.get('injectivity_score', 0.5)]

    def master_lemma_defect(self, raw: dict) -> float:
        return clamp(1.0 - raw.get('injectivity_score', 0.5))


class InverseGaloisCodec(ClayCodec):
    """Inverse Galois: group structure vs field realization."""

    def __init__(self):
        super().__init__('inverse_galois_codec', 'inverse_galois')

    def map_to_force_vector(self, raw: dict) -> List[float]:
        group_order = raw.get('group_order', 6)
        realization_degree = raw.get('realization_degree', 6)
        fraction = raw.get('realization_fraction', 0.5)

        aperture = clamp(safe_div(safe_log(group_order + 1), 10.0))
        pressure = clamp(safe_div(safe_log(realization_degree + 1), 10.0))
        depth = clamp(fraction)
        binding = clamp(fraction)
        continuity = clamp(safe_div(group_order, realization_degree) if realization_degree > 0 else 0.5)
        return [aperture, pressure, depth, binding, continuity]

    def lens_a(self, raw: dict) -> List[float]:
        return [raw.get('group_order', 6)]

    def lens_b(self, raw: dict) -> List[float]:
        return [raw.get('realization_degree', 6)]

    def master_lemma_defect(self, raw: dict) -> float:
        return clamp(1.0 - raw.get('realization_fraction', 0.5))


class BanachTarskiCodec(ClayCodec):
    """Banach-Tarski: measurable volume vs set-theoretic pieces."""

    def __init__(self):
        super().__init__('banach_tarski_codec', 'banach_tarski')

    def map_to_force_vector(self, raw: dict) -> List[float]:
        dim = raw.get('dimension', 3)
        amenability = raw.get('amenability_score', 0.0)
        n_pieces = raw.get('n_pieces', 5)

        aperture = clamp(safe_div(dim, 5.0))
        pressure = clamp(1.0 - amenability)
        depth = clamp(safe_div(n_pieces, n_pieces + 5))
        binding = clamp(amenability)
        continuity = clamp(1.0 if dim <= 2 else 0.0)
        return [aperture, pressure, depth, binding, continuity]

    def lens_a(self, raw: dict) -> List[float]:
        return [raw.get('dimension', 3)]

    def lens_b(self, raw: dict) -> List[float]:
        return [raw.get('amenability_score', 0.0)]

    def master_lemma_defect(self, raw: dict) -> float:
        dim = raw.get('dimension', 3)
        if dim <= 2:
            return 0.0  # Amenable: no paradox
        return 1.0  # Non-amenable: paradox exists


class InfoParadoxCodec(ClayCodec):
    """Black hole info paradox: Hawking entropy vs Page curve."""

    def __init__(self):
        super().__init__('info_paradox_codec', 'info_paradox')

    def map_to_force_vector(self, raw: dict) -> List[float]:
        s_hawking = raw.get('hawking_entropy', 1.0)
        s_page = raw.get('page_entropy', 0.5)
        scrambling_time = raw.get('scrambling_time', 0.5)

        aperture = clamp(safe_div(s_hawking, s_hawking + s_page + 1e-10))
        pressure = clamp(abs(s_hawking - s_page) / max(s_hawking, s_page, 1e-10))
        depth = clamp(scrambling_time)
        binding = clamp(1.0 - abs(s_hawking - s_page) / max(s_hawking, s_page, 1e-10))
        continuity = clamp(safe_div(min(s_hawking, s_page), max(s_hawking, s_page, 1e-10)))
        return [aperture, pressure, depth, binding, continuity]

    def lens_a(self, raw: dict) -> List[float]:
        return [raw.get('hawking_entropy', 1.0)]

    def lens_b(self, raw: dict) -> List[float]:
        return [raw.get('page_entropy', 0.5)]

    def master_lemma_defect(self, raw: dict) -> float:
        s_h = raw.get('hawking_entropy', 1.0)
        s_p = raw.get('page_entropy', 0.5)
        return clamp(abs(s_h - s_p) / max(s_h, s_p, 1e-10))


# ================================================================
#  BRIDGE CODECS (cross-domain)
# ================================================================

class BridgeRMTCodec(ClayCodec):
    """Random Matrix Theory bridge: zeta spacing vs GUE prediction."""

    def __init__(self):
        super().__init__('bridge_rmt_codec', 'bridge_rmt')

    def map_to_force_vector(self, raw: dict) -> List[float]:
        empirical = raw.get('spacing_distribution', 0.5)
        gue_pred = raw.get('gue_prediction', 0.5)

        aperture = clamp(empirical)
        pressure = clamp(abs(empirical - gue_pred))
        depth = clamp(gue_pred)
        binding = clamp(1.0 - abs(empirical - gue_pred))
        continuity = clamp(safe_div(min(empirical, gue_pred), max(empirical, gue_pred, 1e-10)))
        return [aperture, pressure, depth, binding, continuity]

    def lens_a(self, raw: dict) -> List[float]:
        return [raw.get('spacing_distribution', 0.5)]

    def lens_b(self, raw: dict) -> List[float]:
        return [raw.get('gue_prediction', 0.5)]

    def master_lemma_defect(self, raw: dict) -> float:
        return clamp(abs(raw.get('spacing_distribution', 0.5)
                         - raw.get('gue_prediction', 0.5)))


class BridgeExpanderCodec(ClayCodec):
    """Expander graphs bridge: spectral gap vs mixing time."""

    def __init__(self):
        super().__init__('bridge_expander_codec', 'bridge_expander')

    def map_to_force_vector(self, raw: dict) -> List[float]:
        gap = max(raw.get('spectral_gap', 0.1), 1e-10)
        mixing = raw.get('mixing_time', 10)

        aperture = clamp(gap)
        pressure = clamp(safe_div(1.0, gap * mixing + 1e-10))
        depth = clamp(safe_div(mixing, mixing + 20))
        binding = clamp(safe_div(gap, gap + 0.5))
        continuity = clamp(1.0 / (1.0 + abs(1.0 / gap - mixing)))
        return [aperture, pressure, depth, binding, continuity]

    def lens_a(self, raw: dict) -> List[float]:
        return [raw.get('spectral_gap', 0.1)]

    def lens_b(self, raw: dict) -> List[float]:
        return [raw.get('mixing_time', 10)]

    def master_lemma_defect(self, raw: dict) -> float:
        gap = max(raw.get('spectral_gap', 0.1), 1e-10)
        mixing = raw.get('mixing_time', 10)
        return clamp(abs(1.0 / gap - mixing) / max(1.0 / gap, mixing, 1))


class BridgeFractalCodec(ClayCodec):
    """Multi-fractal cascades bridge: NS cascade vs RH zeta exponent."""

    def __init__(self):
        super().__init__('bridge_fractal_codec', 'bridge_fractal')

    def map_to_force_vector(self, raw: dict) -> List[float]:
        tau_ns = raw.get('cascade_exponent', 0.5)
        tau_zeta = raw.get('zeta_exponent', 0.5)

        aperture = clamp(tau_ns)
        pressure = clamp(abs(tau_ns - tau_zeta))
        depth = clamp(tau_zeta)
        binding = clamp(1.0 - abs(tau_ns - tau_zeta))
        continuity = clamp(safe_div(min(tau_ns, tau_zeta), max(tau_ns, tau_zeta, 1e-10)))
        return [aperture, pressure, depth, binding, continuity]

    def lens_a(self, raw: dict) -> List[float]:
        return [raw.get('cascade_exponent', 0.5)]

    def lens_b(self, raw: dict) -> List[float]:
        return [raw.get('zeta_exponent', 0.5)]

    def master_lemma_defect(self, raw: dict) -> float:
        return clamp(abs(raw.get('cascade_exponent', 0.5)
                         - raw.get('zeta_exponent', 0.5)))


class BridgeSpectralCodec(ClayCodec):
    """Universal spectral gaps bridge: operator gap vs ground state energy."""

    def __init__(self):
        super().__init__('bridge_spectral_codec', 'bridge_spectral')

    def map_to_force_vector(self, raw: dict) -> List[float]:
        gap = max(raw.get('operator_gap', 0.1), 1e-10)
        energy = max(raw.get('ground_state_energy', 1.0), 1e-10)

        ratio = gap / energy
        aperture = clamp(safe_div(gap, gap + energy))
        pressure = clamp(abs(ratio - 1.0) / (ratio + 1.0))
        depth = clamp(safe_div(energy, energy + 5.0))
        binding = clamp(safe_div(gap, energy))
        continuity = clamp(1.0 / (1.0 + abs(ratio - 1.0)))
        return [aperture, pressure, depth, binding, continuity]

    def lens_a(self, raw: dict) -> List[float]:
        return [raw.get('operator_gap', 0.1)]

    def lens_b(self, raw: dict) -> List[float]:
        return [raw.get('ground_state_energy', 1.0)]

    def master_lemma_defect(self, raw: dict) -> float:
        gap = max(raw.get('operator_gap', 0.1), 1e-10)
        energy = max(raw.get('ground_state_energy', 1.0), 1e-10)
        return clamp(abs(gap / energy - 1.0))


# ================================================================
#  REGISTRY
# ================================================================

EXPANSION_CODEC_REGISTRY = {
    'collatz': CollatzCodec,
    'abc': ABCCodec,
    'langlands': LanglandsCodec,
    'continuum': ContinuumCodec,
    'ramsey': RamseyCodec,
    'twin_primes': TwinPrimesCodec,
    'poincare_4d': Poincare4DCodec,
    'cosmo_constant': CosmoConstantCodec,
    'falconer': FalconerCodec,
    'jacobian': JacobianCodec,
    'inverse_galois': InverseGaloisCodec,
    'banach_tarski': BanachTarskiCodec,
    'info_paradox': InfoParadoxCodec,
    'bridge_rmt': BridgeRMTCodec,
    'bridge_expander': BridgeExpanderCodec,
    'bridge_fractal': BridgeFractalCodec,
    'bridge_spectral': BridgeSpectralCodec,
}
