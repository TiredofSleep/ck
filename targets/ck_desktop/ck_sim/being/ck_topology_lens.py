# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_topology_lens.py -- Standardized I/0 Topology Decomposition for All Problems
=================================================================================
Operator: BALANCE (5) -- Every object carries two topologies.

Wraps existing ClayCodec lens_a / lens_b to formalize the I/0 decomposition
described in the Sanders Dual-Topology Framework and the Multi-Domain Topology
Extraction documents.

For every problem:
  I (core axis)   = lens_a = T_int  (intrinsic topology, central void)
  0 (boundary)    = lens_b = T_rep  (representational topology, defective void)
  Flow features   = NEW    = how information moves from I to 0

TopologyLens does NOT replace codecs. It wraps them, adding:
  1. Standardized I/0/flow output format across all domains
  2. Domain-specific flow feature computation
  3. Cross-domain topology sheet metadata
  4. TIG-class assignment per the Sanders Universal Topology Map

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
from typing import Dict, List, Optional

from ck_sim.being.ck_sdv_safety import clamp, safe_div, safe_sqrt, safe_log


# ================================================================
#  CROSS-DOMAIN TOPOLOGY SHEET (from Multi-Domain Topology Extraction)
# ================================================================

CROSS_DOMAIN_SHEET = {
    # ── 6 Clay Millennium Problems ──
    'navier_stokes': {
        'I': 'vorticity_axis',
        '0': 'domain_wall',
        'flow': 'vortex_stretch_vs_diffusion',
        'defect_type': 'blow_up',
        'tig_class': [3, 6, 7, 9],
        'description': 'Aligned flow (TIG-7/8) = smooth; Misaligned (TIG-3/6) = turbulent',
    },
    'p_vs_np': {
        'I': 'clause_variable_graph',
        '0': 'global_solution_space',
        'flow': 'logical_extension',
        'defect_type': 'np_gap',
        'tig_class': [6, 9],
        'description': 'Local constraints cannot produce global topology -> P != NP',
    },
    'riemann': {
        'I': 'critical_line',
        '0': 'half_plane_boundary',
        'flow': 'prime_oscillation_vs_symmetry',
        'defect_type': 'off_line_zero',
        'tig_class': [7, 9],
        'description': 'Zeta stable only when dynamics anchor to central axis',
    },
    'yang_mills': {
        'I': 'vacuum_expectation',
        '0': 'gauge_orbit_boundary',
        'flow': 'field_fluctuation_vs_confinement',
        'defect_type': 'mass_gap',
        'tig_class': [4, 7, 9],
        'description': 'Singular gauge configs cannot preserve both core and boundary',
    },
    'bsd': {
        'I': 'mordell_weil_rank',
        '0': 'l_function_s1',
        'flow': 'height_pairing_vs_analytic_derivatives',
        'defect_type': 'rank_vanishing_mismatch',
        'tig_class': [5, 7],
        'description': 'Core arithmetic shape matches analytic boundary shape',
    },
    'hodge': {
        'I': 'hodge_decomposition',
        '0': 'algebraic_cycle_cone',
        'flow': 'analytic_class_to_algebraic_representative',
        'defect_type': 'non_algebraic_class',
        'tig_class': [5, 7],
        'description': 'Every analytic class must touch the geometric boundary',
    },

    # ── 13 Standalone Problems ──
    'collatz': {
        'I': 'orbit_iteration',
        '0': 'convergence_basin',
        'flow': 'step_map_vs_global_attractor',
        'defect_type': 'divergent_orbit',
        'tig_class': [3, 3, 9],
        'description': 'Iteration dynamics: every orbit must reach the core attractor',
    },
    'abc': {
        'I': 'radical_product',
        '0': 'sum_bound',
        'flow': 'additive_vs_multiplicative',
        'defect_type': 'quality_excess',
        'tig_class': [2, 5, 7, 9],
        'description': 'Additive structure (a+b=c) vs multiplicative structure (rad)',
    },
    'langlands': {
        'I': 'automorphic_form',
        '0': 'galois_representation',
        'flow': 'functorial_transfer',
        'defect_type': 'non_functorial',
        'tig_class': [1, 2, 3, 5, 7, 8, 9],
        'description': 'Every Galois representation has an automorphic counterpart',
    },
    'continuum': {
        'I': 'cardinal_hierarchy',
        '0': 'forcing_extension',
        'flow': 'set_model_independence',
        'defect_type': 'undecidable',
        'tig_class': [0, 1, 6, 8, 9],
        'description': 'Cardinality of continuum independent of ZFC axioms',
    },
    'ramsey': {
        'I': 'partition_structure',
        '0': 'monochromatic_subgraph',
        'flow': 'combinatorial_growth',
        'defect_type': 'growth_bound',
        'tig_class': [1, 2, 6, 7, 9],
        'description': 'Order emerges from sufficiently large chaos',
    },
    'twin_primes': {
        'I': 'prime_gap',
        '0': 'sieve_density',
        'flow': 'gap_distribution_vs_density',
        'defect_type': 'finite_gap',
        'tig_class': [0, 1, 2, 3, 7, 9],
        'description': 'Infinitely many primes with bounded gap',
    },
    'poincare_4d': {
        'I': 'smooth_structure',
        '0': 'topological_manifold',
        'flow': 'surgery_obstruction',
        'defect_type': 'exotic_structure',
        'tig_class': [0, 2, 4, 5, 9],
        'description': '4D smooth Poincare: exotic structures obstruct surgery',
    },
    'cosmo_constant': {
        'I': 'vacuum_energy_density',
        '0': 'observed_expansion',
        'flow': 'quantum_vs_classical_gravity',
        'defect_type': 'hierarchy_gap',
        'tig_class': [0, 2, 4, 6, 8, 9],
        'description': 'Quantum vacuum energy vs observed cosmological constant',
    },
    'falconer': {
        'I': 'fractal_dimension',
        '0': 'distance_set_measure',
        'flow': 'projection_vs_dimension',
        'defect_type': 'dimension_drop',
        'tig_class': [0, 1, 2, 5, 7, 9],
        'description': 'Fractal sets of sufficient dimension have rich distance sets',
    },
    'jacobian': {
        'I': 'polynomial_map',
        '0': 'determinant_one_condition',
        'flow': 'inversion_obstruction',
        'defect_type': 'non_invertible',
        'tig_class': [1, 2, 7, 9],
        'description': 'Jacobian det=1 implies global invertibility (in dim >= 2: open)',
    },
    'inverse_galois': {
        'I': 'finite_group',
        '0': 'number_field_extension',
        'flow': 'realization_obstruction',
        'defect_type': 'unrealizable_group',
        'tig_class': [1, 2, 3, 7, 9],
        'description': 'Every finite group is a Galois group over Q',
    },
    'banach_tarski': {
        'I': 'paradoxical_decomposition',
        '0': 'measure_structure',
        'flow': 'non_measurable_partition',
        'defect_type': 'axiom_of_choice',
        'tig_class': [0, 6, 4, 9],
        'description': 'AC enables non-measurable partitions (proved, pathological)',
    },
    'info_paradox': {
        'I': 'hawking_radiation',
        '0': 'horizon_unitarity',
        'flow': 'information_encoding',
        'defect_type': 'unitarity_violation',
        'tig_class': [0, 2, 4, 8, 7, 9],
        'description': 'Black hole evaporation must preserve quantum information',
    },

    # ── 4 Bridge Problems ──
    'bridge_rmt': {
        'I': 'random_matrix_spectrum',
        '0': 'zeta_zero_statistics',
        'flow': 'spectral_universality',
        'defect_type': 'spectral_deviation',
        'tig_class': [0, 1, 2, 5, 7, 8, 9],
        'description': 'RH <-> YM: random matrix eigenvalues match zeta zero gaps',
    },
    'bridge_expander': {
        'I': 'expander_graph',
        '0': 'spectral_gap_bound',
        'flow': 'combinatorial_vs_spectral',
        'defect_type': 'expansion_failure',
        'tig_class': [0, 1, 6, 4, 7, 9],
        'description': 'PvNP <-> YM: expander properties bridge circuit and gauge',
    },
    'bridge_fractal': {
        'I': 'fractal_cascade',
        '0': 'spectral_distribution',
        'flow': 'turbulent_vs_arithmetic',
        'defect_type': 'cascade_mismatch',
        'tig_class': [0, 1, 3, 6, 7, 9],
        'description': 'NS <-> RH: turbulent cascade mirrors prime distribution',
    },
    'bridge_spectral': {
        'I': 'universal_operator_spectrum',
        '0': 'cross_domain_eigenvalues',
        'flow': 'spectral_transfer',
        'defect_type': 'spectral_incoherence',
        'tig_class': [0, 1, 2, 4, 5, 7, 9],
        'description': 'All 6 Clay: universal spectral operator connects all domains',
    },
}


# ================================================================
#  NEIGHBOR -> PARENT TOPOLOGY MAPPING
# ================================================================

NEIGHBOR_TOPOLOGY_PARENT = {
    'ns_2d': 'navier_stokes', 'ns_sqg': 'navier_stokes', 'ns_euler': 'navier_stokes',
    'pnp_ac0': 'p_vs_np', 'pnp_clique': 'p_vs_np', 'pnp_bpp': 'p_vs_np',
    'rh_dirichlet': 'riemann', 'rh_function_field': 'riemann', 'rh_fake': 'riemann',
    'ym_schwinger': 'yang_mills', 'ym_lattice': 'yang_mills', 'ym_phi4': 'yang_mills',
    'bsd_function_field': 'bsd', 'bsd_avg_rank': 'bsd', 'bsd_sato_tate': 'bsd',
    'hodge_tate': 'hodge', 'hodge_standard': 'hodge', 'hodge_transcendental': 'hodge',
}


# ================================================================
#  BASE CLASS: TopologyLens
# ================================================================

class TopologyLens:
    """Base class for I/0 topology decomposition.

    Every TopologyLens wraps an existing ClayCodec and adds:
      - compute_core():     I features (delegates to codec.lens_a)
      - compute_boundary(): 0 features (delegates to codec.lens_b)
      - compute_flow():     NEW I->0 flow characterization
      - compute_defect():   Delta (delegates to codec.master_lemma_defect)
      - standardized_output(): Unified format for cross-domain comparison
    """

    domain_name = 'generic'

    def __init__(self, codec, problem_id: str):
        self.codec = codec
        self.problem_id = problem_id
        # Resolve sheet entry (use parent for neighbors)
        sheet_key = NEIGHBOR_TOPOLOGY_PARENT.get(problem_id, problem_id)
        self.sheet = CROSS_DOMAIN_SHEET.get(sheet_key)

    def compute_core(self, raw: dict) -> dict:
        """I features: the core axis / intrinsic topology."""
        features = self.codec.lens_a(raw)
        label = self.sheet['I'] if self.sheet else 'core'
        return {
            'label': label,
            'features': features,
            'magnitude': safe_sqrt(sum(x * x for x in features)) if features else 0.0,
        }

    def compute_boundary(self, raw: dict) -> dict:
        """0 features: the boundary shell / representational topology."""
        features = self.codec.lens_b(raw)
        label = self.sheet['0'] if self.sheet else 'boundary'
        return {
            'label': label,
            'features': features,
            'magnitude': safe_sqrt(sum(x * x for x in features)) if features else 0.0,
        }

    def compute_flow(self, raw: dict) -> dict:
        """I -> 0 flow features: how information moves from core to boundary.

        Default: generic flow computed from lens difference.
        Subclasses override with domain-specific flow characterization.
        """
        core_feats = self.codec.lens_a(raw)
        boundary_feats = self.codec.lens_b(raw)
        n = min(len(core_feats), len(boundary_feats))

        # Generic flow metrics
        diff = [core_feats[i] - boundary_feats[i] for i in range(n)]
        diff_mag = safe_sqrt(sum(d * d for d in diff))

        # Directional tendency: positive = core > boundary, negative = boundary > core
        direction = sum(diff) / max(n, 1)

        # Alignment: how parallel are core and boundary vectors?
        dot = sum(core_feats[i] * boundary_feats[i] for i in range(n))
        mag_a = safe_sqrt(sum(x * x for x in core_feats[:n]))
        mag_b = safe_sqrt(sum(x * x for x in boundary_feats[:n]))
        alignment = safe_div(dot, mag_a * mag_b, default=0.0)

        return {
            'difference_magnitude': clamp(diff_mag, 0.0, 10.0),
            'direction': clamp(direction, -1.0, 1.0),
            'alignment': clamp(alignment, -1.0, 1.0),
        }

    def compute_defect(self, raw: dict) -> float:
        """Delta = d(T_int, T_rep) -- the topological mismatch."""
        return self.codec.master_lemma_defect(raw)

    def compute_tig_class(self, raw: dict) -> List[int]:
        """Return the TIG operator class for this problem's topology."""
        if self.sheet:
            return list(self.sheet['tig_class'])
        return []

    def standardized_output(self, raw: dict) -> dict:
        """Unified cross-domain topology output.

        This is the standard format consumed by Russell Codec, SSA Engine,
        and RATE Engine.
        """
        core = self.compute_core(raw)
        boundary = self.compute_boundary(raw)
        flow = self.compute_flow(raw)
        defect = self.compute_defect(raw)
        tig_class = self.compute_tig_class(raw)

        return {
            'problem_id': self.problem_id,
            'domain': self.domain_name,
            'core': core,
            'boundary': boundary,
            'flow': flow,
            'defect': defect,
            'tig_class': tig_class,
            'sheet': self.sheet,
        }


# ================================================================
#  NAVIER-STOKES TOPOLOGY LENS
# ================================================================

class TopologyLens_NS(TopologyLens):
    """Navier-Stokes: I = vorticity axis, 0 = domain wall.

    Flow features:
      vortex_alignment: How well vortex tubes align with strain eigenvectors
      strain_ratio: Balance between stretching and diffusion
      cascade_rate: Rate of energy transfer across scales
    """

    domain_name = 'fluid_dynamics'

    def compute_flow(self, raw: dict) -> dict:
        base = super().compute_flow(raw)

        # Domain-specific flow features
        alignment = raw.get('strain_alignment', 0.5)
        omega_mag = raw.get('omega_mag', 0.0)
        omega_max = raw.get('omega_max', 1.0)
        diss = raw.get('energy_dissipation', 0.0)
        diss_max = raw.get('diss_max', 1.0)
        scale_eps = raw.get('scale_epsilon', 0.5)

        # Vortex alignment: how much the vortex tube is aligned with stretching
        vortex_alignment = clamp(alignment)

        # Strain ratio: stretching vs diffusion balance
        strain_ratio = clamp(safe_div(omega_mag, omega_max))

        # Cascade rate: how fast energy moves to small scales
        # High dissipation + small scale = active cascade
        cascade_rate = clamp(safe_div(diss, diss_max) * scale_eps)

        base.update({
            'vortex_alignment': vortex_alignment,
            'strain_ratio': strain_ratio,
            'cascade_rate': cascade_rate,
        })
        return base


# ================================================================
#  P VS NP TOPOLOGY LENS
# ================================================================

class TopologyLens_PNP(TopologyLens):
    """P vs NP: I = clause-variable graph, 0 = global solution space.

    Flow features:
      cluster_extension: How far local clusters extend toward global solution
      phantom_count: Number of non-localizable global constraints
      entropy: Information-theoretic gap between local and global views
    """

    domain_name = 'complexity'

    def compute_flow(self, raw: dict) -> dict:
        base = super().compute_flow(raw)

        n_vars = raw.get('n_variables', 10)
        n_clauses = raw.get('n_clauses', 10)
        alpha = raw.get('clause_ratio', safe_div(n_clauses, n_vars))
        overlap = raw.get('overlap_fraction', 0.5)
        phantom = raw.get('phantom_entropy', 0.5)

        # Cluster extension: how far local constraint clusters reach
        cluster_extension = clamp(1.0 - overlap)

        # Phantom count: proxy for non-localizable constraints
        phantom_count = clamp(phantom)

        # Entropy: information gap between local and global
        entropy = clamp(safe_log(max(alpha, 0.01)) / safe_log(10.0, default=1.0),
                        0.0, 1.0)

        base.update({
            'cluster_extension': cluster_extension,
            'phantom_count': phantom_count,
            'entropy': entropy,
        })
        return base


# ================================================================
#  RIEMANN HYPOTHESIS TOPOLOGY LENS
# ================================================================

class TopologyLens_RH(TopologyLens):
    """Riemann: I = critical line, 0 = half-plane boundary.

    Flow features:
      prime_correlation: How well primes correlate with zero distribution
      zero_deviation: Deviation of zeros from the critical line
      symmetry_adherence: Functional equation symmetry strength
    """

    domain_name = 'number_theory'

    def compute_flow(self, raw: dict) -> dict:
        base = super().compute_flow(raw)

        sigma = raw.get('sigma', 0.5)
        z_phase = raw.get('z_phase', 0.0)
        prime_sum = raw.get('prime_sum_value', 0.5)
        zero_sum = raw.get('zero_sum_value', 0.5)

        # Prime correlation: agreement between prime sum and zero sum
        prime_correlation = clamp(1.0 - abs(prime_sum - zero_sum))

        # Zero deviation: how far from the critical line
        zero_deviation = clamp(abs(sigma - 0.5) * 2.0)

        # Symmetry adherence: phase should be zero at critical line
        symmetry_adherence = clamp(1.0 - abs(z_phase))

        base.update({
            'prime_correlation': prime_correlation,
            'zero_deviation': zero_deviation,
            'symmetry_adherence': symmetry_adherence,
        })
        return base


# ================================================================
#  YANG-MILLS TOPOLOGY LENS
# ================================================================

class TopologyLens_YM(TopologyLens):
    """Yang-Mills: I = vacuum expectation, 0 = gauge orbit boundary.

    Flow features:
      excitation_extension: How far excitations extend from vacuum
      confinement: Strength of confinement (color charge binding)
      gap_ratio: Ratio of first excited state to vacuum
    """

    domain_name = 'gauge_theory'

    def compute_flow(self, raw: dict) -> dict:
        base = super().compute_flow(raw)

        vacuum_energy = raw.get('vacuum_energy', 0.0)
        excited_energy = raw.get('excited_energy', 1.0)
        coupling = raw.get('coupling_constant', 1.0)
        reflection = raw.get('reflection_positivity', 1.0)

        # Excitation extension: ratio of vacuum to excited energy
        excitation_extension = clamp(safe_div(vacuum_energy, excited_energy))

        # Confinement: strong coupling = strong confinement
        confinement = clamp(coupling)

        # Gap ratio: how separated is vacuum from first excitation
        gap_ratio = clamp(safe_div(
            excited_energy - vacuum_energy, excited_energy, default=1.0))

        base.update({
            'excitation_extension': excitation_extension,
            'confinement': confinement,
            'gap_ratio': gap_ratio,
        })
        return base


# ================================================================
#  BSD TOPOLOGY LENS
# ================================================================

class TopologyLens_BSD(TopologyLens):
    """BSD: I = Mordell-Weil rank, 0 = L-function at s=1.

    Flow features:
      rank_match: Agreement between algebraic and analytic ranks
      height_correlation: Correlation of height pairing with L-derivatives
      boundary_coherence: Overall rank-boundary coherence
    """

    domain_name = 'arithmetic_geometry'

    def compute_flow(self, raw: dict) -> dict:
        base = super().compute_flow(raw)

        rank = raw.get('algebraic_rank', 0)
        analytic_rank = raw.get('analytic_rank', 0)
        l_value = raw.get('l_value_at_1', 0.0)
        height = raw.get('height_matrix_det', 0.0)

        # Rank match: perfect when algebraic = analytic rank
        rank_match = 1.0 if rank == analytic_rank else clamp(
            1.0 - abs(rank - analytic_rank) * 0.5)

        # Height correlation: how well height pairing predicts L-function
        height_correlation = clamp(safe_div(
            min(height, l_value), max(height, l_value, 0.001)))

        # Boundary coherence: composite rank-boundary agreement
        boundary_coherence = clamp((rank_match + height_correlation) * 0.5)

        base.update({
            'rank_match': rank_match,
            'height_correlation': height_correlation,
            'boundary_coherence': boundary_coherence,
        })
        return base


# ================================================================
#  HODGE TOPOLOGY LENS
# ================================================================

class TopologyLens_Hodge(TopologyLens):
    """Hodge: I = Hodge decomposition, 0 = algebraic cycle cone.

    Flow features:
      reachability: How close a Hodge class is to being algebraic
      motivic_flow: Strength of motivic relationship between (p,p) forms
      filtration_depth: Depth in the Hodge filtration
    """

    domain_name = 'algebraic_geometry'

    def compute_flow(self, raw: dict) -> dict:
        base = super().compute_flow(raw)

        motivic_defect = raw.get('motivic_defect', 0.5)
        abs_hodge = raw.get('absolute_hodge_value', 0.5)
        p_level = raw.get('p_level', 1)
        dim = raw.get('variety_dimension', 4)

        # Reachability: 1 - motivic defect (how close to algebraic)
        reachability = clamp(1.0 - motivic_defect)

        # Motivic flow: absolute Hodge property strength
        motivic_flow = clamp(abs_hodge)

        # Filtration depth: normalized position in Hodge filtration
        filtration_depth = clamp(safe_div(p_level, dim))

        base.update({
            'reachability': reachability,
            'motivic_flow': motivic_flow,
            'filtration_depth': filtration_depth,
        })
        return base


# ================================================================
#  GENERIC TOPOLOGY LENS (for expansion problems)
# ================================================================

class TopologyLens_Generic(TopologyLens):
    """Generic topology lens for standalone and bridge problems.

    Uses the base class compute_flow() which derives flow features
    from lens_a/lens_b difference vectors. No domain-specific overrides.
    """

    domain_name = 'generic'


# ================================================================
#  REGISTRY + FACTORY
# ================================================================

TOPOLOGY_LENS_CLASSES = {
    'navier_stokes': TopologyLens_NS,
    'p_vs_np': TopologyLens_PNP,
    'riemann': TopologyLens_RH,
    'yang_mills': TopologyLens_YM,
    'bsd': TopologyLens_BSD,
    'hodge': TopologyLens_Hodge,
}


def create_topology_lens(problem_id: str, codec) -> TopologyLens:
    """Create the appropriate TopologyLens for a given problem.

    - 6 Clay problems get domain-specific lenses
    - 18 neighbors inherit their parent's lens
    - All others get the generic lens
    """
    # Direct match: Clay problem
    if problem_id in TOPOLOGY_LENS_CLASSES:
        return TOPOLOGY_LENS_CLASSES[problem_id](codec, problem_id)

    # Neighbor: use parent's lens class
    parent = NEIGHBOR_TOPOLOGY_PARENT.get(problem_id)
    if parent and parent in TOPOLOGY_LENS_CLASSES:
        return TOPOLOGY_LENS_CLASSES[parent](codec, problem_id)

    # Everything else: generic
    return TopologyLens_Generic(codec, problem_id)
