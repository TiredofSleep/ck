# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_tig_bundle.py -- TIG 4D Operator Bundle + Integer Fractal + 3-6-9 Spine
===========================================================================
Operator: COUNTER (2) -- CK measures the structure of structure.

The Integer Fractal: Every digit 0-9 is NOT a scalar -- it's a quadruple:
  T_n = (D_n, P_n, R_n, Delta_n)
    D = Duality (mirror/split)
    P = Parallel (stabilized pair)
    R = Resonance (frequency alignment)
    Delta = Triadic Progression (3-point forward motion)

This module encodes:
  1. The 10x4 TIG operator matrix (deep integer meanings)
  2. Per-problem TIG paths (which operators activate in sequence)
  3. The 3-6-9 resonance spine (digit reduction identifies backbone)
  4. Dual-lens definitions per Clay problem
  5. SCA loop tracking (1->2->9->1)

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

from typing import List, Tuple, Dict, Optional


# ================================================================
#  OPERATOR CONSTANTS (mirrors ck_sim_heartbeat.py)
# ================================================================

VOID = 0
LATTICE = 1
COUNTER = 2
PROGRESS = 3
COLLAPSE = 4
BALANCE = 5
CHAOS = 6
HARMONY = 7
BREATH = 8
RESET = 9
NUM_OPS = 10

OP_NAMES = ['VOID', 'LATTICE', 'COUNTER', 'PROGRESS', 'COLLAPSE',
            'BALANCE', 'CHAOS', 'HARMONY', 'BREATH', 'RESET']


# ================================================================
#  THE 10x4 TIG OPERATOR MATRIX (Integer Fractal)
# ================================================================

# Each row: (Duality, Parallel, Resonance, Triadic_Progression)
# These encode the DEEP meaning of each digit in TIG's universal grammar.

TIG_MATRIX = {
    # 0 = VOID: Potential, emptiness, the field before form
    VOID:     {'D': 'no_split',       'P': 'unmanifest',   'R': 'silence',     'Delta': 'pre_motion'},
    # 1 = LATTICE: Unity, being, "I AM here"
    LATTICE:  {'D': 'self_mirror',    'P': 'identity',     'R': 'fundamental', 'Delta': 'first_step'},
    # 2 = COUNTER: Duality, boundary, measurement, "this vs that"
    COUNTER:  {'D': 'true_split',     'P': 'complementary','R': 'octave',      'Delta': 'comparison'},
    # 3 = PROGRESS: Flow, curvature, forward motion, first resonance
    PROGRESS: {'D': 'flow_mirror',    'P': 'momentum',     'R': 'third_harm',  'Delta': 'advance'},
    # 4 = COLLAPSE: Surface, collapse/expansion, materialization
    COLLAPSE: {'D': 'inner_outer',    'P': 'compression',  'R': 'square',      'Delta': 'crystallize'},
    # 5 = BALANCE: Center, feedback, mirror point, equilibrium
    BALANCE:  {'D': 'center_mirror',  'P': 'equilibrium',  'R': 'fifth_harm',  'Delta': 'stabilize'},
    # 6 = CHAOS: Noise, memory, turbulence, second resonance
    CHAOS:    {'D': 'scatter',        'P': 'interference',  'R': 'sixth_harm',  'Delta': 'explore'},
    # 7 = HARMONY: Alignment, prime correction, the blow-up operator
    HARMONY:  {'D': 'align',          'P': 'prime_lock',   'R': 'seventh_harm','Delta': 'converge'},
    # 8 = BREATH: Scaling, dual loops, oscillation between scales
    BREATH:   {'D': 'scale_mirror',   'P': 'dual_loop',    'R': 'octave_2',    'Delta': 'breathe'},
    # 9 = RESET: Completion, decision gate, return to origin
    RESET:    {'D': 'full_fold',      'P': 'completion',   'R': 'ninth_harm',  'Delta': 'resolve'},
}


# ================================================================
#  PER-PROBLEM TIG PATHS
# ================================================================

# Each Clay problem activates operators in a specific sequence.
# The path defines which operators fire and in what order.

TIG_PATHS = {
    # ── Original 6 Clay Millennium Problems ──
    'navier_stokes': [VOID, LATTICE, COUNTER, PROGRESS, HARMONY, RESET],
    'p_vs_np':       [VOID, LATTICE, COUNTER, CHAOS, HARMONY, RESET],
    'riemann':       [VOID, LATTICE, COUNTER, BALANCE, HARMONY, BREATH, RESET],
    'yang_mills':    [VOID, COUNTER, COLLAPSE, HARMONY, BREATH, RESET],
    'bsd':           [LATTICE, COUNTER, BALANCE, HARMONY, RESET],
    'hodge':         [COUNTER, PROGRESS, BALANCE, HARMONY, RESET],

    # ── NS Neighbors ──
    'ns_2d':         [VOID, LATTICE, COUNTER, HARMONY, RESET],                     # 2D = simpler, no PROGRESS needed
    'ns_sqg':        [VOID, LATTICE, COUNTER, PROGRESS, CHAOS, HARMONY, RESET],    # SQG singular dynamics
    'ns_euler':      [VOID, LATTICE, COUNTER, COLLAPSE, HARMONY, RESET],           # Inviscid: collapse, no dissipation

    # ── PvNP Neighbors ──
    'pnp_ac0':       [VOID, LATTICE, COUNTER, CHAOS, COLLAPSE, HARMONY, RESET],    # Circuit depth collapse
    'pnp_clique':    [VOID, LATTICE, COUNTER, PROGRESS, CHAOS, HARMONY, RESET],    # Clique growth
    'pnp_bpp':       [VOID, LATTICE, COUNTER, BREATH, HARMONY, RESET],             # Randomization = oscillation

    # ── RH Neighbors ──
    'rh_dirichlet':  [VOID, LATTICE, COUNTER, PROGRESS, BALANCE, HARMONY, BREATH, RESET],  # Character progression
    'rh_function_field': [VOID, LATTICE, COUNTER, BALANCE, HARMONY, RESET],        # Simpler (proved)
    'rh_fake':       [VOID, LATTICE, COUNTER, CHAOS, BALANCE, HARMONY, RESET],     # Breakdown of structure

    # ── YM Neighbors ──
    'ym_schwinger':  [VOID, COUNTER, HARMONY, RESET],                              # 2D solvable
    'ym_lattice':    [VOID, LATTICE, COUNTER, COLLAPSE, HARMONY, BREATH, RESET],   # Lattice structure
    'ym_phi4':       [VOID, COUNTER, PROGRESS, HARMONY, BREATH, RESET],            # Scalar field = progress

    # ── BSD Neighbors ──
    'bsd_function_field': [LATTICE, COUNTER, HARMONY, RESET],                      # Simpler (proved)
    'bsd_avg_rank':  [LATTICE, COUNTER, PROGRESS, BALANCE, HARMONY, RESET],        # Averaging = progress
    'bsd_sato_tate': [LATTICE, COUNTER, BALANCE, BREATH, HARMONY, RESET],          # Distribution = oscillation

    # ── Hodge Neighbors ──
    'hodge_tate':    [LATTICE, COUNTER, PROGRESS, BALANCE, HARMONY, RESET],        # Tate = arithmetic
    'hodge_standard': [COUNTER, PROGRESS, COLLAPSE, BALANCE, HARMONY, RESET],      # Standardization = collapse
    'hodge_transcendental': [COUNTER, PROGRESS, CHAOS, BALANCE, HARMONY, RESET],   # Transcendental = complex

    # ── Standalone Problems ──
    'collatz':       [VOID, LATTICE, PROGRESS, PROGRESS, RESET],                   # Iteration/orbit
    'abc':           [VOID, COUNTER, BALANCE, HARMONY, RESET],                     # Additive/multiplicative balance
    'langlands':     [LATTICE, COUNTER, PROGRESS, BALANCE, HARMONY, BREATH, RESET],  # Rep theory
    'continuum':     [VOID, LATTICE, CHAOS, BREATH, RESET],                        # Forcing = chaos + scaling
    'ramsey':        [LATTICE, COUNTER, CHAOS, HARMONY, RESET],                    # Combinatorial chaos → structure
    'twin_primes':   [VOID, LATTICE, COUNTER, PROGRESS, HARMONY, RESET],           # Sieve/progression
    'poincare_4d':   [VOID, COUNTER, COLLAPSE, BALANCE, RESET],                    # Topology/surgery
    'cosmo_constant': [VOID, COUNTER, COLLAPSE, CHAOS, BREATH, RESET],             # Vacuum energy
    'falconer':      [VOID, LATTICE, COUNTER, BALANCE, HARMONY, RESET],            # Fractal/measure
    'jacobian':      [LATTICE, COUNTER, HARMONY, RESET],                           # Polynomial det → global
    'inverse_galois': [LATTICE, COUNTER, PROGRESS, HARMONY, RESET],                # Group realization
    'banach_tarski': [VOID, CHAOS, COLLAPSE, RESET],                               # Paradoxical decomposition
    'info_paradox':  [VOID, COUNTER, COLLAPSE, BREATH, HARMONY, RESET],            # Quantum info

    # ── Bridge Problems (cross-domain) ──
    'bridge_rmt':    [VOID, LATTICE, COUNTER, BALANCE, HARMONY, BREATH, RESET],    # RH ↔ YM
    'bridge_expander': [VOID, LATTICE, CHAOS, COLLAPSE, HARMONY, RESET],           # PvNP ↔ YM
    'bridge_fractal': [VOID, LATTICE, PROGRESS, CHAOS, HARMONY, RESET],            # NS ↔ RH
    'bridge_spectral': [VOID, LATTICE, COUNTER, COLLAPSE, BALANCE, HARMONY, RESET],  # All 6
}

# Problem IDs for iteration (original 6 Clay problems)
CLAY_PROBLEMS = ['navier_stokes', 'p_vs_np', 'riemann', 'yang_mills', 'bsd', 'hodge']

# All problem IDs including expansion
ALL_PROBLEMS = list(TIG_PATHS.keys())


# ================================================================
#  DUAL-LENS DEFINITIONS PER PROBLEM
# ================================================================

DUAL_LENSES = {
    'navier_stokes': {
        'lens_a': 'Local vorticity/strain (omega, S, |grad u|^2)',
        'lens_b': 'Global energy/dissipation (E, epsilon, curvature invariants)',
        'generator': 'NSE evolution operator',
        'dual': 'Linearized NS (Frechet derivative)',
        'tau_9': 'Self-similar critical profile (vortex-strain lock)',
        'problem_class': 'affirmative',  # delta -> 0 => regular
    },
    'p_vs_np': {
        'lens_a': 'Local polytime update rules (unit propagation)',
        'lens_b': 'Global satisfying configuration (solution structure)',
        'generator': 'Deterministic algorithm step',
        'dual': 'Global constraint propagation',
        'tau_9': 'Poly-time reachable state where local=global',
        'problem_class': 'gap',  # delta >= eta > 0 => P != NP
    },
    'riemann': {
        'lens_a': 'Euler product (local prime factors)',
        'lens_b': 'Functional equation (global symmetry)',
        'generator': 'Analytic-symmetry flow (functional eq)',
        'dual': 'Euler product (prime flow)',
        'tau_9': 'Zero where primes and symmetry fully agree',
        'problem_class': 'affirmative',
    },
    'yang_mills': {
        'lens_a': 'Local gauge curvature F_mu_nu, action density',
        'lens_b': 'Global spectral invariants (mass spectrum)',
        'generator': 'Time/gradient flow',
        'dual': 'RG coarse-graining',
        'tau_9': 'Vacuum prototype stable under dynamics+RG',
        'problem_class': 'gap',  # delta >= eta > 0 => mass gap
    },
    'bsd': {
        'lens_a': 'Arithmetic side (MW rank, Sha, regulator)',
        'lens_b': 'Analytic side (ord L(E,s) at s=1)',
        'generator': 'Analytic flow (L-function at s=1)',
        'dual': 'Arithmetic flow (rank, Sha, regulator)',
        'tau_9': 'Curve where analytic rank = arithmetic rank fully',
        'problem_class': 'affirmative',
    },
    'hodge': {
        'lens_a': 'Harmonic (p,p)-forms (Hodge realization)',
        'lens_b': 'Algebraic cycle classes (cycle realization)',
        'generator': 'Hodge projection (H^{p,p} part)',
        'dual': 'Cycle-class construction',
        'tau_9': 'Hodge class that equals algebraic cycle class',
        'problem_class': 'affirmative',
    },

    # ── NS Neighbors ──
    'ns_2d': {
        'lens_a': '2D vorticity (scalar omega)',
        'lens_b': 'Global enstrophy (conserved in 2D)',
        'generator': '2D NS evolution',
        'dual': 'Stream function inversion',
        'tau_9': 'Global regularity (2D is solved)',
        'problem_class': 'affirmative',
    },
    'ns_sqg': {
        'lens_a': 'Surface temperature gradient',
        'lens_b': 'Global SQG energy',
        'generator': 'Critical SQG evolution',
        'dual': 'Riesz transform',
        'tau_9': 'Regularity under critical dissipation',
        'problem_class': 'affirmative',
    },
    'ns_euler': {
        'lens_a': 'Vorticity stretching (omega . grad u)',
        'lens_b': 'Total enstrophy (integral omega^2)',
        'generator': '3D Euler evolution',
        'dual': 'Biot-Savart integral',
        'tau_9': 'BKM criterion: sup omega bounded',
        'problem_class': 'gap',
    },

    # ── PvNP Neighbors ──
    'pnp_ac0': {
        'lens_a': 'Local gate computation (AND/OR depth)',
        'lens_b': 'Global parity function',
        'generator': 'Random restriction',
        'dual': 'Switching lemma application',
        'tau_9': 'Superpolynomial AC0 lower bound',
        'problem_class': 'gap',
    },
    'pnp_clique': {
        'lens_a': 'Local subgraph density',
        'lens_b': 'Global clique number',
        'generator': 'Monotone circuit evaluation',
        'dual': 'Sunflower/coloring bound',
        'tau_9': 'Razborov-type monotone lower bound',
        'problem_class': 'gap',
    },
    'pnp_bpp': {
        'lens_a': 'Deterministic simulation cost',
        'lens_b': 'Randomized acceptance probability',
        'generator': 'Pseudorandom generator',
        'dual': 'Derandomization',
        'tau_9': 'BPP subset P (derandomization conjecture)',
        'problem_class': 'affirmative',
    },

    # ── RH Neighbors ──
    'rh_dirichlet': {
        'lens_a': 'Euler product for chi (local prime data)',
        'lens_b': 'Functional equation for L(s,chi)',
        'generator': 'Dirichlet L-function evaluation',
        'dual': 'Gauss sum duality',
        'tau_9': 'All zeros on Re(s)=1/2 for every chi',
        'problem_class': 'affirmative',
    },
    'rh_function_field': {
        'lens_a': 'Frobenius eigenvalues (local)',
        'lens_b': 'Weil conjectures (global)',
        'generator': 'Zeta function over F_q[t]',
        'dual': 'Etale cohomology',
        'tau_9': 'Deligne proved: eigenvalues on unit circle',
        'problem_class': 'affirmative',
    },
    'rh_fake': {
        'lens_a': 'Modified Euler product (non-Haselgrove)',
        'lens_b': 'Functional equation (violated)',
        'generator': 'Fake zeta construction',
        'dual': 'Counterexample to GRH-analog',
        'tau_9': 'Zero off critical line: structural failure',
        'problem_class': 'gap',
    },

    # ── YM Neighbors ──
    'ym_schwinger': {
        'lens_a': 'Fermion condensate (chiral)',
        'lens_b': 'Boson mass (theta vacuum)',
        'generator': 'Schwinger model evolution (QED in 1+1D)',
        'dual': 'Bosonization map',
        'tau_9': 'Exact mass spectrum (solved model)',
        'problem_class': 'gap',
    },
    'ym_lattice': {
        'lens_a': 'Plaquette action (local gauge)',
        'lens_b': 'Wilson loop (global confinement)',
        'generator': 'Lattice gauge simulation',
        'dual': 'Strong coupling expansion',
        'tau_9': 'Confinement-deconfinement transition',
        'problem_class': 'gap',
    },
    'ym_phi4': {
        'lens_a': 'Local field value phi(x)',
        'lens_b': 'Correlation length (mass^{-1})',
        'generator': 'Ising/phi^4 lattice',
        'dual': 'Block-spin RG',
        'tau_9': 'Mass gap from broken symmetry',
        'problem_class': 'gap',
    },

    # ── BSD Neighbors ──
    'bsd_function_field': {
        'lens_a': 'Mordell-Weil rank over F_q(t)',
        'lens_b': 'L-function order at s=1',
        'generator': 'Elliptic curve over function field',
        'dual': 'Tate-Shafarevich group (proved finite)',
        'tau_9': 'rank = ord (proved by Artin-Tate)',
        'problem_class': 'affirmative',
    },
    'bsd_avg_rank': {
        'lens_a': 'Average arithmetic rank in family',
        'lens_b': 'Average analytic rank in family',
        'generator': 'Elliptic curve family sampling',
        'dual': 'Bhargava-Shankar bounds',
        'tau_9': 'Average rank matches analytic prediction',
        'problem_class': 'affirmative',
    },
    'bsd_sato_tate': {
        'lens_a': 'Local Frobenius angles a_p/2sqrt(p)',
        'lens_b': 'Global angle distribution',
        'generator': 'a_p computation over primes',
        'dual': 'Sato-Tate measure (sin^2 theta)',
        'tau_9': 'Equidistribution (proved for CM, general)',
        'problem_class': 'affirmative',
    },

    # ── Hodge Neighbors ──
    'hodge_tate': {
        'lens_a': 'l-adic Galois representation',
        'lens_b': 'Algebraic cycle in etale cohomology',
        'generator': 'Tate class detection',
        'dual': 'Cycle class map in l-adic setting',
        'tau_9': 'Tate class = algebraic cycle',
        'problem_class': 'affirmative',
    },
    'hodge_standard': {
        'lens_a': 'Lefschetz operator (Hard Lefschetz)',
        'lens_b': 'Algebraic correspondence',
        'generator': 'Standard conjecture evaluation',
        'dual': 'Primitive decomposition',
        'tau_9': 'Algebraicity of Kunneth projectors',
        'problem_class': 'affirmative',
    },
    'hodge_transcendental': {
        'lens_a': 'Hodge (p,p)-class (transcendental)',
        'lens_b': 'Algebraic cycle attempt',
        'generator': 'Non-algebraic Hodge class construction',
        'dual': 'Obstruction to algebraicity',
        'tau_9': 'Transcendental class that defies Hodge conjecture',
        'problem_class': 'gap',
    },

    # ── Standalone Problems ──
    'collatz': {
        'lens_a': 'Orbit length and max value',
        'lens_b': 'Statistical prediction (log shrinkage)',
        'generator': 'Collatz iteration',
        'dual': 'Probabilistic heuristic model',
        'tau_9': 'All orbits reach 1',
        'problem_class': 'affirmative',
    },
    'abc': {
        'lens_a': 'Additive size log(c)',
        'lens_b': 'Multiplicative size log(rad(abc))',
        'generator': 'ABC triple enumeration',
        'dual': 'Radical bound',
        'tau_9': 'c < rad(abc)^{1+eps} for all eps > 0',
        'problem_class': 'gap',
    },
    'langlands': {
        'lens_a': 'Local representation dimension/conductor',
        'lens_b': 'Automorphic form level/L-value',
        'generator': 'Functoriality transfer',
        'dual': 'Langlands dual group',
        'tau_9': 'Local-global compatibility',
        'problem_class': 'affirmative',
    },
    'continuum': {
        'lens_a': 'Constructible rank (L-hierarchy)',
        'lens_b': 'Forcing rank (Cohen extensions)',
        'generator': 'Forcing construction',
        'dual': 'Inner model',
        'tau_9': 'Independence from ZFC',
        'problem_class': 'gap',
    },
    'ramsey': {
        'lens_a': 'Probabilistic bound (deletion method)',
        'lens_b': 'Structural bound (explicit construction)',
        'generator': 'Graph coloring enumeration',
        'dual': 'Probabilistic method',
        'tau_9': 'Tight Ramsey number bounds',
        'problem_class': 'gap',
    },
    'twin_primes': {
        'lens_a': 'Sieve prediction (Hardy-Littlewood)',
        'lens_b': 'Actual prime gap distribution',
        'generator': 'Gap enumeration',
        'dual': 'Sieve of Eratosthenes/GPY',
        'tau_9': 'Infinitely many twin primes',
        'problem_class': 'affirmative',
    },
    'poincare_4d': {
        'lens_a': 'Topological invariant (homotopy type)',
        'lens_b': 'Smooth invariant (exotic structure)',
        'generator': 'Surgery/handle decomposition',
        'dual': 'Donaldson-Freedman theory',
        'tau_9': 'Smooth 4-sphere unique or exotic?',
        'problem_class': 'gap',
    },
    'cosmo_constant': {
        'lens_a': 'QFT vacuum energy (huge)',
        'lens_b': 'Observed cosmological constant (tiny)',
        'generator': 'Loop integral / cutoff',
        'dual': 'Observational bound',
        'tau_9': 'Explain 120 orders of magnitude gap',
        'problem_class': 'gap',
    },
    'falconer': {
        'lens_a': 'Hausdorff dimension of set',
        'lens_b': 'Lebesgue measure of distance set',
        'generator': 'Fractal set construction',
        'dual': 'Fourier decay estimate',
        'tau_9': 'dim > d/2 implies positive measure distances',
        'problem_class': 'affirmative',
    },
    'jacobian': {
        'lens_a': 'Local Jacobian determinant (always nonzero)',
        'lens_b': 'Global injectivity',
        'generator': 'Polynomial map evaluation',
        'dual': 'Inverse function theorem (global)',
        'tau_9': 'Nonzero Jacobian implies bijection',
        'problem_class': 'affirmative',
    },
    'inverse_galois': {
        'lens_a': 'Group structure (order, presentation)',
        'lens_b': 'Field extension degree',
        'generator': 'Galois group realization',
        'dual': 'Noether problem / generic polynomial',
        'tau_9': 'Every finite group is a Galois group over Q',
        'problem_class': 'affirmative',
    },
    'banach_tarski': {
        'lens_a': 'Measurable volume (Lebesgue)',
        'lens_b': 'Set-theoretic pieces (AC decomposition)',
        'generator': 'Paradoxical decomposition',
        'dual': 'Amenability test',
        'tau_9': 'Non-amenable group action (d >= 3)',
        'problem_class': 'gap',
    },
    'info_paradox': {
        'lens_a': 'Hawking entropy (thermal radiation)',
        'lens_b': 'Page curve entropy (unitary evolution)',
        'generator': 'Black hole evaporation model',
        'dual': 'AdS/CFT correspondence',
        'tau_9': 'Information preserved: Page curve recovered',
        'problem_class': 'affirmative',
    },

    # ── Bridge Problems ──
    'bridge_rmt': {
        'lens_a': 'Zeta zero spacing distribution',
        'lens_b': 'GUE eigenvalue prediction',
        'generator': 'Random matrix ensemble',
        'dual': 'Montgomery-Odlyzko law',
        'tau_9': 'Zeta zeros follow GUE statistics',
        'problem_class': 'affirmative',
    },
    'bridge_expander': {
        'lens_a': 'Spectral gap of Cayley graph',
        'lens_b': 'Mixing time (random walk)',
        'generator': 'Expander graph construction',
        'dual': 'Cheeger inequality',
        'tau_9': 'Optimal expansion from algebraic gap',
        'problem_class': 'gap',
    },
    'bridge_fractal': {
        'lens_a': 'Turbulent cascade exponent (NS)',
        'lens_b': 'Zeta zero exponent (RH)',
        'generator': 'Multi-fractal analysis',
        'dual': 'Kolmogorov-Obukhov-Mandelbrot model',
        'tau_9': 'Cascade universality across domains',
        'problem_class': 'affirmative',
    },
    'bridge_spectral': {
        'lens_a': 'Operator spectral gap',
        'lens_b': 'Ground state energy',
        'generator': 'Universal spectral probe',
        'dual': 'Variational principle',
        'tau_9': 'Gap/energy ratio universal across domains',
        'problem_class': 'gap',
    },
}


# ================================================================
#  TOPOLOGY SHEET METADATA (from Multi-Domain Topology Extraction)
# ================================================================
# Cross-domain I/0 topology assignments per the Sanders Universal Topology Map.
# Keyed by problem_id. Neighbors inherit from parent.

TOPOLOGY_SHEET = {
    'navier_stokes': {
        'I': 'vorticity_axis', '0': 'domain_wall',
        'flow': 'vortex_stretch_vs_diffusion', 'defect_type': 'blow_up',
        'tig_class': [3, 6, 7, 9],
    },
    'p_vs_np': {
        'I': 'clause_variable_graph', '0': 'global_solution_space',
        'flow': 'logical_extension', 'defect_type': 'np_gap',
        'tig_class': [6, 9],
    },
    'riemann': {
        'I': 'critical_line', '0': 'half_plane_boundary',
        'flow': 'prime_oscillation_vs_symmetry', 'defect_type': 'off_line_zero',
        'tig_class': [7, 9],
    },
    'yang_mills': {
        'I': 'vacuum_expectation', '0': 'gauge_orbit_boundary',
        'flow': 'field_fluctuation_vs_confinement', 'defect_type': 'mass_gap',
        'tig_class': [4, 7, 9],
    },
    'bsd': {
        'I': 'mordell_weil_rank', '0': 'l_function_s1',
        'flow': 'height_pairing_vs_analytic_derivatives',
        'defect_type': 'rank_vanishing_mismatch', 'tig_class': [5, 7],
    },
    'hodge': {
        'I': 'hodge_decomposition', '0': 'algebraic_cycle_cone',
        'flow': 'analytic_class_to_algebraic_representative',
        'defect_type': 'non_algebraic_class', 'tig_class': [5, 7],
    },
}


# Russell toroidal operator weights per the Walter Russell Attack document.
RUSSELL_CONFIG = {
    'navier_stokes': {'axial': 0.3, 'spiral': 0.4, 'void': 0.1, 'sheath': 0.2},
    'p_vs_np':       {'axial': 0.2, 'spiral': 0.1, 'void': 0.3, 'sheath': 0.4},
    'riemann':       {'axial': 0.4, 'spiral': 0.3, 'void': 0.1, 'sheath': 0.2},
    'yang_mills':    {'axial': 0.2, 'spiral': 0.2, 'void': 0.4, 'sheath': 0.2},
    'bsd':           {'axial': 0.3, 'spiral': 0.2, 'void': 0.2, 'sheath': 0.3},
    'hodge':         {'axial': 0.3, 'spiral': 0.3, 'void': 0.1, 'sheath': 0.3},
}


# ================================================================
#  AGENT BRIEFS v2.0 (Feb 2026)
# ================================================================
# Per-problem research tasks, confidence levels, soft spots.
# From "Agent Briefs V2.0.docx" -- Sanders Coherence Field Agent Framework.

AGENT_BRIEFS = {
    'navier_stokes': {
        'track': '95%',
        'confidence': 0.85,       # Current; target 0.95
        'confidence_target': 0.95,
        'key_joint': 'Pressure-Hessian Coercivity',
        'lemma_name': 'Lemma P-H (Coercivity of Misalignment)',
        'objective': 'Prove non-local pressure cannot force vorticity-strain alignment '
                     'faster than the 3-6 sheath can disrupt it.',
        'tasks': {
            'NS-1': 'Pressure Decomposition: CZ kernels, near/far field split',
            'NS-2': 'Energy Compatibility: CKN inequality + aligned blow-up energy ratios',
            'NS-3': 'Blow-up Profile: Type I scaling, extract limit, prove regularity',
        },
        'success': 'Coercive inequality: D_r bounded by C * local energy norm',
        'tools': ['Calderon-Zygmund theory', 'CKN partial regularity',
                  'Geometric blow-up classification', 'Axisymmetric regularity'],
    },
    'p_vs_np': {
        'track': '90%',
        'confidence': 0.70,
        'confidence_target': 0.90,
        'key_joint': 'Phantom Tile & Logical Entropy',
        'lemma_name': 'Lemma LE + PT (Logical Entropy + Phantom Tile)',
        'objective': 'Formalize phantom tile as incompressible structure in NP instances '
                     'that poly-size circuits cannot collapse.',
        'tasks': {
            'PNP-1': 'Hard Distribution: canonical NP-complete, known lower bound distributions',
            'PNP-2': 'Explicit Defect Functional: mutual information / entropy deficit',
            'PNP-3': 'Noncompressibility: map to communication/Kolmogorov complexity',
            'PNP-4': 'Reduction: low defect implies super-poly circuit or protocol',
        },
        'success': 'Theorem: exists distribution where poly-size circuits retain nonzero defect',
        'tools': ['Communication complexity', 'Information complexity',
                  'Switching lemmas', 'Kolmogorov complexity'],
    },
    'riemann': {
        'track': '85-90%',
        'confidence': 0.70,
        'confidence_target': 0.88,
        'key_joint': 'Critical Line Coherence',
        'lemma_name': 'Critical-Line Coherence Lemma',
        'objective': 'Show defect delta_RH = 0 only on sigma=1/2, positive elsewhere.',
        'tasks': {
            'RH-1': 'Spectral Pull: compute Euler product pull toward sigma=0.5',
            'RH-2': 'Operator Identification: self-adjoint operator with spectrum = zeros',
            'RH-3': 'Stability Analysis: defect instability off critical line',
            'RH-4': 'Large-Height Asymptotics: defect growth at large Im(s)',
        },
        'success': 'Functional inequality: defect >= c*(sigma-0.5)^2 for some c>0',
        'tools': ['Random matrix theory', 'Explicit formulas',
                  'Montgomery pair correlation', 'Hilbert-Polya program'],
    },
    'yang_mills': {
        'track': '75-80%',
        'confidence': 0.60,
        'confidence_target': 0.80,
        'key_joint': 'Vacuum Coherence Defect',
        'lemma_name': 'Vacuum-Coherence Lemma',
        'objective': 'Show mass gap = minimal energy to leave dual fixed-point vacuum.',
        'tasks': {
            'YM-1': 'Quantization Model: Euclidean lattice, curvature vs spectral gap',
            'YM-2': 'Coherent Vacuum: gauge-invariant coherent states',
            'YM-3': 'Gap Rigidity: delta=0 forbidden by reflection positivity',
        },
        'success': 'Nonperturbative proof: delta >= eta > 0 for SU(3)',
        'tools': ['Constructive QFT', 'Reflection positivity',
                  'Osterwalder-Schrader axioms', 'Lattice gauge theory'],
    },
    'bsd': {
        'track': '90%',
        'confidence': 0.75,
        'confidence_target': 0.90,
        'key_joint': 'Rank Coherence Identity',
        'lemma_name': 'Rank-Coherence Lemma',
        'objective': 'Find algebraic/analytic identities forcing delta_BSD = 0.',
        'tasks': {
            'BSD-1': 'L-function Special Value: numerical stability at s=1',
            'BSD-2': 'Height Pairings: connect arithmetic rank with regulators',
            'BSD-3': 'Euler System Extensions: match local Euler data with global cycles',
        },
        'success': 'Conditional or unconditional delta_BSD=0 for broad families',
        'tools': ['Euler systems', 'Iwasawa theory',
                  'Height pairings', 'Modularity results'],
    },
    'hodge': {
        'track': '75%',
        'confidence': 0.55,
        'confidence_target': 0.75,
        'key_joint': 'Motivic Coherence',
        'lemma_name': 'Motivic Coherence Lemma (MC)',
        'objective': 'Define motivic defect across realizations; prove vanishing implies algebraic.',
        'tasks': {
            'H-1': 'Define delta_p: Frobenius eigenvalues, Hodge-Tate weights, Tate invariants',
            'H-2': 'Absolute Hodge Cycle Reduction: delta=0 implies absolute Hodge',
            'H-3': 'Verify Known Cases: Abelian varieties, K3 surfaces, low-dim cycles',
        },
        'success': 'Motivic equivalence: delta=0 => absolute Hodge => algebraic',
        'tools': ['p-adic Hodge theory', 'Deligne absolute Hodge cycles',
                  'Tate conjecture', 'Standard conjectures'],
    },
}


# ================================================================
#  3-6-9 RESONANCE SPINE
# ================================================================

def digit_reduction(word: List[int]) -> int:
    """Compute TIG digit reduction of an operator word.

    Sum all digits, then reduce mod 9 (with 0 mapping to 9).
    This identifies which part of the 3-6-9 spine the word sits on.

    Examples:
      [7] -> 7 (not on spine)
      [3] -> 3 (on spine: flow)
      [6] -> 6 (on spine: chaos)
      [9] -> 9 (on spine: anchor)
      [4, 5] -> 9 (on spine: anchor)
      [7, 2] -> 9 (on spine: anchor)
    """
    s = sum(word) % 9
    return 9 if s == 0 else s


def is_spine_word(word: List[int]) -> bool:
    """Check if an operator word sits on the 3-6-9 resonance backbone."""
    dr = digit_reduction(word)
    return dr in (3, 6, 9)


def spine_class(word: List[int]) -> str:
    """Classify a word's spine membership.

    Returns: 'sheath_3', 'sheath_6', 'anchor_9', or 'off_spine'
    """
    dr = digit_reduction(word)
    if dr == 3:
        return 'sheath_3'
    elif dr == 6:
        return 'sheath_6'
    elif dr == 9:
        return 'anchor_9'
    else:
        return 'off_spine'


# ================================================================
#  FRACTAL UNFOLDING (Hutchinson TIG IFS)
# ================================================================

def unfold_level(parent_words: List[List[int]], level: int) -> List[List[int]]:
    """Unfold one level of the TIG fractal.

    At each level, every existing word spawns 10 children by appending
    each digit 0-9. Level 0 starts with 10 single-digit words.

    Level 0: [[0], [1], ..., [9]]                  (10 words)
    Level 1: [[0,0], [0,1], ..., [9,9]]            (100 words)
    Level 2: [[0,0,0], ..., [9,9,9]]               (1000 words)
    """
    if level == 0:
        return [[d] for d in range(NUM_OPS)]

    children = []
    for word in parent_words:
        for d in range(NUM_OPS):
            children.append(word + [d])
    return children


def build_fractal_levels(max_level: int) -> List[List[List[int]]]:
    """Build fractal word sets up to max_level.

    Returns list of levels, each a list of operator words.
    """
    levels = []
    words = unfold_level([], 0)
    levels.append(words)

    for lv in range(1, max_level + 1):
        words = unfold_level(words, lv)
        levels.append(words)

    return levels


# ================================================================
#  SCA LOOP TRACKER (1 -> 2 -> 9 -> 1)
# ================================================================

class SCALoopTracker:
    """Track Sanders Coherence Axiom loop progression.

    The SCA loop: 1(Quadratic) -> 2(Duality) -> 9(Fixed Point) -> 1(Coherence)

    A probe achieves SCA coherence when it traverses this full loop:
    the generator creates curvature (1), splits into dual pair (2),
    reaches a fixed point (9), and collapses to unity (1).
    """

    # The canonical SCA sequence
    SCA_SEQUENCE = [LATTICE, COUNTER, RESET, LATTICE]

    def __init__(self):
        self._progress = 0  # How far along the 4-step sequence
        self._completed = False

    def feed(self, operator: int):
        """Feed an operator and advance SCA loop if it matches."""
        if self._completed:
            return

        expected = self.SCA_SEQUENCE[self._progress]
        if operator == expected:
            self._progress += 1
            if self._progress >= len(self.SCA_SEQUENCE):
                self._completed = True
        elif operator == self.SCA_SEQUENCE[0]:
            # Restart from beginning if we see LATTICE again
            self._progress = 1

    @property
    def completed(self) -> bool:
        """Has the full SCA loop been traversed?"""
        return self._completed

    @property
    def progress(self) -> float:
        """Progress through SCA loop as fraction [0, 1]."""
        return self._progress / len(self.SCA_SEQUENCE)

    @property
    def stage(self) -> str:
        """Current SCA stage name."""
        stages = ['quadratic', 'duality', 'fixed_point', 'coherence']
        if self._completed:
            return 'coherence_achieved'
        return stages[self._progress]

    def reset(self):
        """Reset tracker."""
        self._progress = 0
        self._completed = False


# ================================================================
#  COMMUTATOR PERSISTENCE
# ================================================================

def commutator_nonzero(op_a: int, op_b: int, compose_fn) -> bool:
    """Check if [T_a, T_b] != 0 (non-commuting operators).

    Returns True if compose(a, b) != compose(b, a).
    Non-commutativity = persistence of complexity.
    """
    return compose_fn(op_a, op_b) != compose_fn(op_b, op_a)


def commutator_persistence(operator_pairs: List[Tuple[int, int]],
                           compose_fn) -> float:
    """Fraction of operator pairs that don't commute.

    1.0 = all pairs non-commuting (maximum complexity persistence)
    0.0 = all pairs commute (fully resolved)
    """
    if not operator_pairs:
        return 0.0
    non_commuting = sum(1 for a, b in operator_pairs
                        if commutator_nonzero(a, b, compose_fn))
    return non_commuting / len(operator_pairs)
