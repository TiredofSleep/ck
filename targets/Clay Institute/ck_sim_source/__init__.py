# ck_sim -- CK Coherence Spectrometer
# Mathematical coherence measurement for the Clay Millennium Problems
# and 35 expansion problems (41 total).
#
# Pipeline: Generator -> Codec (5D) -> D2 -> CL -> delta(S) at each fractal level
#
# (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory

"""CK Coherence Spectrometer Package.

Organized by TIG principle: Being / Doing / Becoming.

    being/      -- Mathematical foundations.
                   Heartbeat, D2, codecs, safety, TIG bundle,
                   topology lens, Russell codec, thermal probe.

    doing/      -- Measurement engines.
                   Generators, protocol, spectrometer,
                   SSA engine, RATE engine, FOO engine.

    becoming/   -- Persistence and reporting.
                   Clay journal, spectrometer journal.

    face/       -- CLI runners.
                   Clay runner, spectrometer runner.

    tests/      -- All test files.
"""

import sys
import importlib
import importlib.util

__version__ = '9.20'  # Meta-lens + FOO + Phi(kappa). Clean spectrometer.


# -- Backward-Compatible Import Aliasing --
# Redirects flat paths (ck_sim.ck_foo) to subpackage paths (ck_sim.being.ck_foo).
# Lazy: modules only load when actually imported.

_CK_ALIAS_MAP = {
    # -- being/ --
    'ck_sim.ck_sim_heartbeat':    'ck_sim.being.ck_sim_heartbeat',
    'ck_sim.ck_sim_d2':           'ck_sim.being.ck_sim_d2',
    'ck_sim.ck_coherence_action': 'ck_sim.being.ck_coherence_action',
    'ck_sim.ck_sensory_codecs':   'ck_sim.being.ck_sensory_codecs',
    'ck_sim.ck_sdv_safety':       'ck_sim.being.ck_sdv_safety',
    'ck_sim.ck_tig_bundle':       'ck_sim.being.ck_tig_bundle',
    'ck_sim.ck_clay_codecs':      'ck_sim.being.ck_clay_codecs',
    'ck_sim.ck_expansion_codecs': 'ck_sim.being.ck_expansion_codecs',
    'ck_sim.ck_thermal_probe':    'ck_sim.being.ck_thermal_probe',
    'ck_sim.ck_topology_lens':    'ck_sim.being.ck_topology_lens',
    'ck_sim.ck_russell_codec':    'ck_sim.being.ck_russell_codec',
    # -- doing/ --
    'ck_sim.ck_clay_protocol':    'ck_sim.doing.ck_clay_protocol',
    'ck_sim.ck_clay_generators':  'ck_sim.doing.ck_clay_generators',
    'ck_sim.ck_expansion_generators': 'ck_sim.doing.ck_expansion_generators',
    'ck_sim.ck_neighbor_generators':  'ck_sim.doing.ck_neighbor_generators',
    'ck_sim.ck_spectrometer':     'ck_sim.doing.ck_spectrometer',
    'ck_sim.ck_ssa_engine':       'ck_sim.doing.ck_ssa_engine',
    'ck_sim.ck_rate_engine':      'ck_sim.doing.ck_rate_engine',
    'ck_sim.ck_clay_attack':      'ck_sim.doing.ck_clay_attack',
    'ck_sim.ck_governing_equations': 'ck_sim.doing.ck_governing_equations',
    'ck_sim.ck_gpu':              'ck_sim.doing.ck_gpu',
    # -- becoming/ --
    'ck_sim.ck_clay_journal':     'ck_sim.becoming.ck_clay_journal',
    'ck_sim.ck_spectrometer_journal': 'ck_sim.becoming.ck_spectrometer_journal',
    # -- face/ --
    'ck_sim.ck_clay_runner':      'ck_sim.face.ck_clay_runner',
    'ck_sim.ck_spectrometer_runner': 'ck_sim.face.ck_spectrometer_runner',
}


class _CKAliasLoader:
    """Load a module by importing its real location and aliasing it."""
    def __init__(self, real_name):
        self.real_name = real_name

    def create_module(self, spec):
        return importlib.import_module(self.real_name)

    def exec_module(self, module):
        pass  # already loaded by create_module

    def get_code(self, fullname):
        return None

    def get_source(self, fullname):
        return None


class _CKAliasFinder:
    """Meta-path finder: redirects flat paths to B/D/BC subpackages."""

    def find_spec(self, fullname, path, target=None):
        if fullname not in _CK_ALIAS_MAP:
            return None
        real = _CK_ALIAS_MAP[fullname]
        loader = _CKAliasLoader(real)
        return importlib.util.spec_from_loader(fullname, loader)


sys.meta_path.append(_CKAliasFinder())


__all__ = [
    # Being
    'ck_sim_heartbeat', 'ck_sim_d2', 'ck_coherence_action',
    'ck_sensory_codecs', 'ck_sdv_safety', 'ck_tig_bundle',
    'ck_clay_codecs', 'ck_expansion_codecs', 'ck_thermal_probe',
    'ck_topology_lens', 'ck_russell_codec',
    # Doing
    'ck_clay_protocol', 'ck_clay_generators', 'ck_expansion_generators',
    'ck_neighbor_generators', 'ck_spectrometer', 'ck_ssa_engine',
    'ck_rate_engine', 'ck_clay_attack', 'ck_governing_equations', 'ck_gpu',
    # Becoming
    'ck_clay_journal', 'ck_spectrometer_journal',
    # Face
    'ck_clay_runner', 'ck_spectrometer_runner',
]
