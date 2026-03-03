"""
ck_clay_codecs.py -- Mathematical Sensory Codecs for Clay SDV Protocol
======================================================================
Operator: COUNTER (2) -- CK measures mathematics.

6 codecs that map mathematical objects into CK's 5D force space:
  [aperture, pressure, depth, binding, continuity]

Each codec encodes the MISMATCH between two lenses:
  Lens A (local/analytic) vs Lens B (global/geometric)

When lenses agree  -> components near midpoint -> low D2 -> HARMONY
When lenses diverge -> components swing to extremes -> high D2 -> CHAOS/COLLAPSE

The D2 pipeline then computes second-derivative curvature and classifies
to one of 10 TIG operators. This IS the coherence measurement.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
from typing import Dict, List, Optional, Tuple

from ck_sim.being.ck_sensory_codecs import SensorCodec
from ck_sim.being.ck_sdv_safety import (
    clamp, clamp_vector, safe_div, safe_sqrt, safe_log, CompressOnlySafety
)


# ================================================================
#  BASE CLASS: All Clay codecs extend this
# ================================================================

class ClayCodec(SensorCodec):
    """Base class for Clay mathematical codecs.

    Adds dual-lens accessors and Master Lemma defect computation
    on top of the standard SensorCodec pattern.

    Every Clay codec MUST implement:
      - map_to_force_vector(raw) -> [aperture, pressure, depth, binding, continuity]
      - lens_a(raw) -> List[float]  (local/analytic measurements)
      - lens_b(raw) -> List[float]  (global/geometric measurements)
      - master_lemma_defect(raw) -> float  (per-problem delta)
    """

    def __init__(self, name: str, problem_id: str):
        super().__init__(name, sample_rate_hz=50.0)
        self.problem_id = problem_id
        self.safety = CompressOnlySafety()

    def lens_a(self, raw: dict) -> List[float]:
        """Extract Lens A (local/analytic) measurements."""
        raise NotImplementedError

    def lens_b(self, raw: dict) -> List[float]:
        """Extract Lens B (global/geometric) measurements."""
        raise NotImplementedError

    def lens_mismatch(self, raw: dict) -> float:
        """Compute ||A - B||^2 mismatch between lenses."""
        a = self.lens_a(raw)
        b = self.lens_b(raw)
        n = min(len(a), len(b))
        return sum((a[i] - b[i]) ** 2 for i in range(n))

    def master_lemma_defect(self, raw: dict) -> float:
        """Compute the per-problem Master Lemma defect delta.

        This is the mathematical defect from Clay Lemmas.docx:
          NS:  delta_NS = 1 - |cos(omega, e1)|^2
          RH:  delta_RH = |zeta_symmetry - zeta_primes|
          etc.
        """
        raise NotImplementedError

    def feed(self, raw_reading: dict) -> int:
        """Feed with safety checks."""
        if self.safety.halted:
            return 0  # VOID
        force_vec = self.map_to_force_vector(raw_reading)
        force_vec = self.safety.check_force_vector(force_vec, self.name)
        self.last_force_vec = force_vec

        if self.engine.feed(force_vec):
            self.last_operator = self.engine.operator
            self.operator_history.append(self.last_operator)

        self._tick_count += 1
        return self.last_operator


# ================================================================
#  1. NAVIER-STOKES CODEC (HIGHEST PRIORITY)
# ================================================================

class NavierStokesCodec(ClayCodec):
    """Navier-Stokes vorticity/strain -> D2 -> Operator.

    Lens A (local): vorticity omega, strain S, gradient |nabla u|^2
    Lens B (global): energy E, dissipation epsilon, curvature invariants

    The 5D force vector encodes the MISMATCH between vorticity-strain
    alignment (local) and energy-dissipation balance (global).

    Master Lemma 1: delta_NS = 1 - |cos(omega, e1)|^2
      where e1 = max-stretching eigenvector of strain S.
      D_r -> 0 => regular (no blow-up).

    Expected raw_reading keys:
      omega_mag:        float >= 0  -- vorticity magnitude |omega|
      omega_max:        float > 0   -- normalization scale
      strain_alignment: float [0,1] -- |cos(omega, e1)|^2 (vortex-strain alignment)
      scale_epsilon:    float [0,1] -- current scale level (0=large, 1=Kolmogorov)
      energy_dissipation: float >= 0 -- viscous dissipation rate
      diss_max:         float > 0   -- dissipation normalization
      omega_gradient:   float >= 0  -- |nabla omega|
      grad_max:         float > 0   -- gradient normalization
    """

    def __init__(self):
        super().__init__('navier_stokes', 'navier_stokes')

    def map_to_force_vector(self, raw: dict) -> List[float]:
        omega_mag = raw.get('omega_mag', 0.0)
        omega_max = raw.get('omega_max', 1.0)
        alignment = raw.get('strain_alignment', 0.5)
        scale_eps = raw.get('scale_epsilon', 0.5)
        diss = raw.get('energy_dissipation', 0.0)
        diss_max = raw.get('diss_max', 1.0)
        omega_grad = raw.get('omega_gradient', 0.0)
        grad_max = raw.get('grad_max', 1.0)

        # aperture = 1 - strain_alignment (misalignment = openness)
        aperture = clamp(1.0 - alignment)

        # pressure = omega_magnitude / omega_max (vorticity force)
        pressure = clamp(safe_div(omega_mag, omega_max))

        # depth = 1 - scale_epsilon (how deep into small scales)
        depth = clamp(1.0 - scale_eps)

        # binding = energy_dissipation / diss_max (viscous binding)
        binding = clamp(safe_div(diss, diss_max))

        # continuity = 1 - omega_gradient / grad_max (smoothness)
        continuity = clamp(1.0 - safe_div(omega_grad, grad_max))

        return [aperture, pressure, depth, binding, continuity]

    def lens_a(self, raw: dict) -> List[float]:
        """Local lens: vorticity/strain measurements."""
        omega_mag = raw.get('omega_mag', 0.0)
        omega_max = raw.get('omega_max', 1.0)
        alignment = raw.get('strain_alignment', 0.5)
        omega_grad = raw.get('omega_gradient', 0.0)
        grad_max = raw.get('grad_max', 1.0)
        return [
            clamp(safe_div(omega_mag, omega_max)),
            clamp(alignment),
            clamp(safe_div(omega_grad, grad_max)),
        ]

    def lens_b(self, raw: dict) -> List[float]:
        """Global lens: energy/dissipation measurements."""
        diss = raw.get('energy_dissipation', 0.0)
        diss_max = raw.get('diss_max', 1.0)
        energy = raw.get('energy', 0.5)
        scale_eps = raw.get('scale_epsilon', 0.5)
        return [
            clamp(safe_div(diss, diss_max)),
            clamp(energy),
            clamp(scale_eps),
        ]

    def master_lemma_defect(self, raw: dict) -> float:
        """delta_NS = 1 - |cos(omega, e1)|^2

        Perfect alignment (alignment=1) => delta=0 => coherent.
        Misalignment => delta>0 => defect present.
        """
        alignment = raw.get('strain_alignment', 0.5)
        return clamp(1.0 - alignment)


# ================================================================
#  2. RIEMANN CODEC
# ================================================================

class RiemannCodec(ClayCodec):
    """Riemann zeta function -> D2 -> Operator.

    Lens A (local): Explicit formula prime-side functional
    Lens B (global): Explicit formula zero-side functional

    Upgraded codec (Celeste v1.0 -- Feb 2026):
      delta_RH = alpha * delta_explicit + beta * delta_phase

      delta_explicit: Averaged explicit formula mismatch (primes <-> zeros)
        Global structural invariant; seed-stable by construction.

      delta_phase: Hardy Z-function phase defect
        On critical line: Z(t) is real, so optimal phase alignment = 0.
        Off critical line: no global phase makes zeta real -> defect > 0.

    This replaces the naive |zeta_sym - zeta_euler| which was too local
    and inherited zeta's oscillation off the critical line (CV=0.576).

    Expected raw_reading keys:
      sigma:              float -- Re(s)
      t:                  float -- Im(s)
      zeta_mag:           float -- |zeta(s)|
      height_max:         float -- normalization for Im(s)
      dzeta_dt:           float -- |d|zeta|/d(Im)|  magnitude derivative
      phase:              float -- arg(zeta(s)) in [-pi, pi]
      explicit_prime:     float -- Averaged prime-side functional (0-1)
      explicit_zero:      float -- Averaged zero-side functional (0-1)
      hardy_z_phase:      float -- Phase defect of Hardy Z-function (0=real, 1=max)
      zeta_euler_real:    float -- (legacy) Re(Euler product)
      zeta_euler_imag:    float -- (legacy) Im(Euler product)
      zeta_sym_real:      float -- (legacy) Re(functional eq)
      zeta_sym_imag:      float -- (legacy) Im(functional eq)
    """

    def __init__(self):
        super().__init__('riemann', 'riemann')

    def map_to_force_vector(self, raw: dict) -> List[float]:
        sigma = raw.get('sigma', 0.5)
        t = raw.get('t', 14.0)
        zeta_mag = raw.get('zeta_mag', 1.0)
        height_max = raw.get('height_max', 100.0)
        dzeta_dt = raw.get('dzeta_dt', 0.0)
        hardy_z_phase = raw.get('hardy_z_phase', 0.0)

        # aperture = 1 - 4*|sigma - 0.5| (distance from critical line)
        aperture = clamp(1.0 - 4.0 * abs(sigma - 0.5))

        # pressure = 1/(1+|zeta|) (zero proximity)
        pressure = clamp(safe_div(1.0, 1.0 + zeta_mag))

        # depth = Im(s) / height_max (height on critical strip)
        depth = clamp(safe_div(abs(t), height_max))

        # binding = phase coherence + GUE pair correlation signal
        # On critical line: phase=0, pair_corr~1.0 -> binding~1.0
        # Off line: phase>0, pair_corr~0.3 -> binding low
        pair_corr = raw.get('pair_correlation', 0.5)
        gue_term = 0.2 * (pair_corr - 0.5)  # [-0.1, +0.1] modest enrichment
        binding = clamp(1.0 - hardy_z_phase + gue_term)

        # continuity = 1 - |d|zeta|/d(Im)| (magnitude smoothness)
        continuity = clamp(1.0 - min(abs(dzeta_dt), 1.0))

        return [aperture, pressure, depth, binding, continuity]

    def lens_a(self, raw: dict) -> List[float]:
        """Explicit formula: prime-side functional."""
        ep = raw.get('explicit_prime', 0.5)
        # Legacy fallback
        if 'explicit_prime' not in raw:
            er = raw.get('zeta_euler_real', raw.get('zeta_real', 0.0))
            ei = raw.get('zeta_euler_imag', raw.get('zeta_imag', 0.0))
            return [clamp(0.5 + er * 0.1, -5.0, 5.0),
                    clamp(0.5 + ei * 0.1, -5.0, 5.0)]
        return [clamp(ep), clamp(ep)]

    def lens_b(self, raw: dict) -> List[float]:
        """Explicit formula: zero-side functional."""
        ez = raw.get('explicit_zero', 0.5)
        # Legacy fallback
        if 'explicit_zero' not in raw:
            sr = raw.get('zeta_sym_real', raw.get('zeta_real', 0.0))
            si = raw.get('zeta_sym_imag', raw.get('zeta_imag', 0.0))
            return [clamp(0.5 + sr * 0.1, -5.0, 5.0),
                    clamp(0.5 + si * 0.1, -5.0, 5.0)]
        return [clamp(ez), clamp(ez)]

    def master_lemma_defect(self, raw: dict) -> float:
        """delta_RH = alpha * delta_explicit + beta * delta_phase

        Explicit formula mismatch (structural, seed-averaged) combined with
        Hardy Z-function phase defect (stillness on critical line).

        On critical line: both terms -> 0, so delta_RH -> 0.
        Off critical line: both terms > 0, structurally stable.
        """
        # Explicit formula component: |prime_functional - zero_functional|
        ep = raw.get('explicit_prime', None)
        ez = raw.get('explicit_zero', None)

        if ep is not None and ez is not None:
            delta_explicit = abs(ep - ez)
        else:
            # Legacy: Euler vs symmetry mismatch
            er = raw.get('zeta_euler_real', raw.get('zeta_real', 0.0))
            ei = raw.get('zeta_euler_imag', raw.get('zeta_imag', 0.0))
            sr = raw.get('zeta_sym_real', raw.get('zeta_real', 0.0))
            si = raw.get('zeta_sym_imag', raw.get('zeta_imag', 0.0))
            delta_explicit = safe_sqrt((er - sr) ** 2 + (ei - si) ** 2)

        # Hardy Z-phase component: how far from "real-valued"
        delta_phase = raw.get('hardy_z_phase', 0.0)

        # GUE pair correlation contribution
        pair_corr = raw.get('pair_correlation', 0.5)
        gue_defect = 0.1 * (1.0 - pair_corr)  # Low pair_corr adds defect

        # Combined
        return clamp(delta_explicit + delta_phase + gue_defect, 0.0, 5.0)


# ================================================================
#  3. P vs NP CODEC
# ================================================================

class PvsNPCodec(ClayCodec):
    """SAT instance structure -> D2 -> Operator.

    Lens A (local): Polytime update rules (unit propagation, BCP)
    Lens B (global): Global satisfying configuration (solution structure)

    Master Lemma 2: delta_SAT = d_TV(G_local, G_global)
      D_bar >= eta > 0 for all poly-time => P != NP.

    Expected raw_reading keys:
      backbone_fraction:   float [0,1] -- fraction of frozen variables
      clause_density:      float >= 0  -- clauses/variables ratio
      propagation_depth:   float [0,1] -- how far unit propagation reaches
      local_coherence:     float [0,1] -- local -> global predictivity
      search_tree_balance: float [0,1] -- search landscape smoothness
    """

    # Critical density for 3-SAT phase transition
    ALPHA_CRITICAL = 4.267

    def __init__(self):
        super().__init__('p_vs_np', 'p_vs_np')

    def map_to_force_vector(self, raw: dict) -> List[float]:
        backbone = raw.get('backbone_fraction', 0.5)
        alpha = raw.get('clause_density', self.ALPHA_CRITICAL)
        prop_depth = raw.get('propagation_depth', 0.5)
        local_coh = raw.get('local_coherence', 0.5)
        balance = raw.get('search_tree_balance', 0.5)

        aperture = clamp(1.0 - backbone)
        pressure = clamp(safe_div(alpha, self.ALPHA_CRITICAL))
        depth = clamp(1.0 - prop_depth)
        binding = clamp(local_coh)
        continuity = clamp(balance)

        return [aperture, pressure, depth, binding, continuity]

    def lens_a(self, raw: dict) -> List[float]:
        """Local algorithmic lens."""
        return [
            clamp(raw.get('propagation_depth', 0.5)),
            clamp(raw.get('local_coherence', 0.5)),
        ]

    def lens_b(self, raw: dict) -> List[float]:
        """Global constraint lens."""
        return [
            clamp(raw.get('backbone_fraction', 0.5)),
            clamp(raw.get('search_tree_balance', 0.5)),
        ]

    def master_lemma_defect(self, raw: dict) -> float:
        """delta_SAT: local-global coherence gap."""
        local_coh = raw.get('local_coherence', 0.5)
        backbone = raw.get('backbone_fraction', 0.5)
        # Proxy for total variation: |local predictivity - global rigidity|
        return abs(local_coh - backbone)


# ================================================================
#  4. YANG-MILLS CODEC
# ================================================================

class YangMillsCodec(ClayCodec):
    """Gauge field configurations -> D2 -> Operator.

    Lens A (local): Gauge curvature F_mu_nu, action density
    Lens B (global): Spectral invariants, mass spectrum, Wilson loops

    Master Lemma 4: Delta(psi) = inf||psi-v|| + d_obs(F(v),F'(v))
      Delta >= eta > 0 for psi perp Omega => mass gap m >= c*eta.

    Expected raw_reading keys:
      vacuum_overlap:     float [0,1] -- ground state overlap
      action_density:     float >= 0  -- local action density
      action_max:         float > 0   -- normalization
      momentum:           float >= 0  -- energy scale
      p_max:              float > 0   -- momentum normalization
      topological_charge: float       -- Q (should be near integer)
      field_gradient:     float >= 0  -- |nabla(field_strength)|
    """

    def __init__(self):
        super().__init__('yang_mills', 'yang_mills')

    def map_to_force_vector(self, raw: dict) -> List[float]:
        vac_overlap = raw.get('vacuum_overlap', 0.5)
        action_dens = raw.get('action_density', 0.0)
        action_max = raw.get('action_max', 1.0)
        momentum = raw.get('momentum', 0.5)
        p_max = raw.get('p_max', 1.0)
        Q = raw.get('topological_charge', 0.0)
        field_grad = raw.get('field_gradient', 0.0)

        aperture = clamp(vac_overlap)
        pressure = clamp(safe_div(action_dens, action_max))
        depth = clamp(1.0 - safe_div(momentum, p_max))
        gauge_inv = raw.get('gauge_invariant', 0.5)
        charge_quant = 1.0 - abs(Q - round(Q))
        binding = clamp(0.7 * charge_quant + 0.3 * gauge_inv)
        continuity = clamp(1.0 - min(abs(field_grad), 1.0))

        return [aperture, pressure, depth, binding, continuity]

    def lens_a(self, raw: dict) -> List[float]:
        """Local gauge curvature lens."""
        return [
            clamp(safe_div(raw.get('action_density', 0.0), raw.get('action_max', 1.0))),
            clamp(min(abs(raw.get('field_gradient', 0.0)), 1.0)),
        ]

    def lens_b(self, raw: dict) -> List[float]:
        """Global spectral lens."""
        return [
            clamp(raw.get('vacuum_overlap', 0.5)),
            clamp(1.0 - abs(raw.get('topological_charge', 0.0) -
                            round(raw.get('topological_charge', 0.0)))),
        ]

    def master_lemma_defect(self, raw: dict) -> float:
        """Vacuum coherence defect: distance from dual fixed-point vacuum."""
        vac_overlap = raw.get('vacuum_overlap', 0.5)
        Q = raw.get('topological_charge', 0.0)
        gauge_inv = raw.get('gauge_invariant', 0.5)
        charge_defect = abs(Q - round(Q))
        gauge_defect = 0.1 * (1.0 - gauge_inv)
        return clamp((1.0 - vac_overlap) + charge_defect + gauge_defect)


# ================================================================
#  5. BSD CODEC
# ================================================================

class BSDCodec(ClayCodec):
    """Elliptic curve data -> D2 -> Operator.

    Lens A (arithmetic): MW rank, Sha group, regulator, Tamagawa numbers
    Lens B (analytic): ord L(E,s) at s=1, leading coefficient

    Master Lemma 5: delta_BSD = |r_analytic - r_algebraic| + |c_analytic - c_arithmetic|
      delta=0 iff BSD holds for E.

    Expected raw_reading keys:
      rank_analytic:   int >= 0   -- ord_{s=1} L(E,s)
      rank_algebraic:  int >= 0   -- rank of E(Q)
      regulator:       float >= 0 -- Neron-Tate regulator
      reg_max:         float > 0  -- regulator normalization
      conductor:       float >= 1 -- conductor of E
      sha_order:       float >= 1 -- |Sha(E/Q)| (1 if trivial)
      torsion_order:   int >= 1   -- |E(Q)_tors|
      leading_coeff_analytic:  float -- c* from L-function
      leading_coeff_arithmetic: float -- c* from BSD formula
    """

    def __init__(self):
        super().__init__('bsd', 'bsd')

    def map_to_force_vector(self, raw: dict) -> List[float]:
        r_an = raw.get('rank_analytic', 0)
        r_al = raw.get('rank_algebraic', 0)
        reg = raw.get('regulator', 1.0)
        reg_max = raw.get('reg_max', 10.0)
        conductor = raw.get('conductor', 1.0)
        sha = raw.get('sha_order', 1.0)
        torsion = raw.get('torsion_order', 1)

        rank_diff = abs(r_an - r_al)
        aperture = clamp(safe_div(1.0, 1.0 + rank_diff))
        pressure = clamp(safe_div(reg, reg_max))
        depth = clamp(safe_div(safe_log(conductor + 1), safe_log(1e6)))
        binding = clamp(safe_div(1.0, 1.0 + safe_log(sha + 1)))
        continuity = clamp(safe_div(torsion, 16.0))

        return [aperture, pressure, depth, binding, continuity]

    def lens_a(self, raw: dict) -> List[float]:
        """Arithmetic lens."""
        return [
            float(raw.get('rank_algebraic', 0)),
            raw.get('leading_coeff_arithmetic', 0.0),
        ]

    def lens_b(self, raw: dict) -> List[float]:
        """Analytic lens."""
        return [
            float(raw.get('rank_analytic', 0)),
            raw.get('leading_coeff_analytic', 0.0),
        ]

    def master_lemma_defect(self, raw: dict) -> float:
        """delta_BSD = |r_analytic - r_algebraic| + |c_analytic - c_arithmetic|"""
        r_an = raw.get('rank_analytic', 0)
        r_al = raw.get('rank_algebraic', 0)
        c_an = raw.get('leading_coeff_analytic', 0.0)
        c_ar = raw.get('leading_coeff_arithmetic', 0.0)
        return abs(r_an - r_al) + abs(c_an - c_ar)


# ================================================================
#  6. HODGE CODEC
# ================================================================

class HodgeCodec(ClayCodec):
    """Cohomology class data -> D2 -> Operator.

    Lens A (analytic): Harmonic (p,p)-forms (Hodge realization)
    Lens B (algebraic): Algebraic cycle classes (cycle realization)

    Master Lemma 6: delta_Hodge = inf_Z ||pi^{p,p}(alpha) - cl(Z)||
      delta=0 iff alpha is algebraic.

    Expected raw_reading keys:
      algebraic_projection: float [0,1] -- how algebraic the class is
      analytic_residual:    float [0,1] -- non-algebraic resistance
      dimension:            int >= 1    -- variety complex dimension
      period_coherence:     float [0,1] -- period matrix integrality
      residual_gradient:    float [0,1] -- flow convergence rate
    """

    def __init__(self):
        super().__init__('hodge', 'hodge')

    def map_to_force_vector(self, raw: dict) -> List[float]:
        alg_proj = raw.get('algebraic_projection', 0.5)
        an_resid = raw.get('analytic_residual', 0.5)
        dim = raw.get('dimension', 2)
        period_coh = raw.get('period_coherence', 0.5)
        resid_grad = raw.get('residual_gradient', 0.5)

        aperture = clamp(alg_proj)
        pressure = clamp(an_resid)
        depth = clamp(safe_div(dim, 10.0))
        binding = clamp(period_coh)
        continuity = clamp(1.0 - resid_grad)

        return [aperture, pressure, depth, binding, continuity]

    def lens_a(self, raw: dict) -> List[float]:
        """Hodge analytic lens."""
        return [
            clamp(raw.get('algebraic_projection', 0.5)),
            clamp(raw.get('period_coherence', 0.5)),
        ]

    def lens_b(self, raw: dict) -> List[float]:
        """Algebraic cycle lens."""
        return [
            clamp(1.0 - raw.get('analytic_residual', 0.5)),
            clamp(1.0 - raw.get('residual_gradient', 0.5)),
        ]

    def master_lemma_defect(self, raw: dict) -> float:
        """delta_Hodge: distance from Hodge projection to algebraic cycle."""
        return clamp(raw.get('analytic_residual', 0.5))


# ================================================================
#  CODEC REGISTRY
# ================================================================

CLAY_CODEC_REGISTRY = {
    'navier_stokes': NavierStokesCodec,
    'riemann': RiemannCodec,
    'p_vs_np': PvsNPCodec,
    'yang_mills': YangMillsCodec,
    'bsd': BSDCodec,
    'hodge': HodgeCodec,
}


def create_codec(problem_id: str) -> ClayCodec:
    """Factory: create a Clay codec by problem ID.

    Checks Clay registry, then neighbor codec map, then expansion registry.
    """
    cls = CLAY_CODEC_REGISTRY.get(problem_id)
    if cls is not None:
        return cls()

    # Check neighbor codec map (reuses parent Clay codec)
    try:
        from ck_sim.doing.ck_neighbor_generators import NEIGHBOR_CODEC_MAP
        parent_id = NEIGHBOR_CODEC_MAP.get(problem_id)
        if parent_id is not None:
            cls = CLAY_CODEC_REGISTRY.get(parent_id)
            if cls is not None:
                return cls()
    except ImportError:
        pass

    # Check expansion codecs
    try:
        from ck_sim.being.ck_expansion_codecs import EXPANSION_CODEC_REGISTRY
        cls = EXPANSION_CODEC_REGISTRY.get(problem_id)
        if cls is not None:
            return cls()
    except ImportError:
        pass

    raise ValueError(f'Unknown problem: {problem_id}')
