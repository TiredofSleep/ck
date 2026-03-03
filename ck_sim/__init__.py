# ck_sim -- CK Coherence Machine Simulation
# Ports all bare-metal C + Verilog algorithms to Python
# for testing, visualization, and phone deployment.
#
# 90+ modules. NumPy for cloud organ only.
#
# (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory

"""CK Simulation Package -- operator algebra in Python.

Organized by TIG principle: Being / Doing / Becoming.

    being/      -- What CK IS at this instant.
                   Heartbeat, brain, body, D2, coherence field,
                   personality, emotion, immune, bonding,
                   sensorium, swarm, BTQ, attention, health.

    doing/      -- What CK DOES in the world.
                   Engine (50Hz tick loop), actions, goals, voice,
                   dialogue, reasoning, language, cloud processing,
                   autodidact, game sense, forecast, thesis.

    becoming/   -- What CK BECOMES over time.
                   Truth lattice, world lattice, concept spine,
                   education, lexicon, memory, episodic, development,
                   identity, network, self-mirror, meta-learning.

    face/       -- How CK APPEARS to the world.
                   Kivy GUI, audio I/O, LED, robot body, UART,
                   deploy, body interface, FPGA dog.

    tests/      -- All test files.

CK is a synthetic organism. Not a robot. A creature you raise.
"""

import sys
import importlib
import importlib.util

__version__ = '9.17i'  # GPU doing engine + truth persistence. CK never forgets.


# ── Backward-Compatible Import Aliasing ──────────────────────────
#
# All code uses `from ck_sim.ck_sim_heartbeat import HARMONY`.
# After reorganization, the real file lives at ck_sim/being/ck_sim_heartbeat.py.
# This finder transparently redirects old paths to new subpackage locations.
# Lazy: modules only load when actually imported. Zero stub files.
#
# Uses find_spec (Python 3.4+). find_module was removed in 3.12+.

_CK_ALIAS_MAP = {
    # ── being/ ──
    'ck_sim.ck_sim_heartbeat':    'ck_sim.being.ck_sim_heartbeat',
    'ck_sim.ck_sim_brain':        'ck_sim.being.ck_sim_brain',
    'ck_sim.ck_sim_body':         'ck_sim.being.ck_sim_body',
    'ck_sim.ck_sim_d2':           'ck_sim.being.ck_sim_d2',
    'ck_sim.ck_coherence_field':  'ck_sim.being.ck_coherence_field',
    'ck_sim.ck_personality':      'ck_sim.being.ck_personality',
    'ck_sim.ck_emotion':          'ck_sim.being.ck_emotion',
    'ck_sim.ck_immune':           'ck_sim.being.ck_immune',
    'ck_sim.ck_bonding':          'ck_sim.being.ck_bonding',
    'ck_sim.ck_sensorium':        'ck_sim.being.ck_sensorium',
    'ck_sim.ck_swarm':            'ck_sim.being.ck_swarm',
    'ck_sim.ck_sensory_codecs':   'ck_sim.being.ck_sensory_codecs',
    'ck_sim.ck_attention':        'ck_sim.being.ck_attention',
    'ck_sim.ck_btq':              'ck_sim.being.ck_btq',
    'ck_sim.ck_sim_btq':          'ck_sim.being.ck_sim_btq',
    'ck_sim.ck_fractal_health':   'ck_sim.being.ck_fractal_health',
    'ck_sim.ck_divine27':         'ck_sim.being.ck_divine27',
    'ck_sim.ck_coherence_action': 'ck_sim.being.ck_coherence_action',
    'ck_sim.ck_tig_security':     'ck_sim.being.ck_tig_security',
    'ck_sim.ck_fibonacci_transform': 'ck_sim.being.ck_fibonacci_transform',
    'ck_sim.ck_power_sense':        'ck_sim.being.ck_power_sense',
    'ck_sim.ck_vortex_physics':     'ck_sim.being.ck_vortex_physics',
    'ck_sim.ck_coherence_gate':     'ck_sim.being.ck_coherence_gate',
    # ── doing/ ──
    'ck_sim.ck_sim_engine':       'ck_sim.doing.ck_sim_engine',
    'ck_sim.ck_action':           'ck_sim.doing.ck_action',
    'ck_sim.ck_goals':            'ck_sim.doing.ck_goals',
    'ck_sim.ck_autodidact':       'ck_sim.doing.ck_autodidact',
    'ck_sim.ck_autodidact_runner': 'ck_sim.doing.ck_autodidact_runner',
    'ck_sim.ck_dialogue':         'ck_sim.doing.ck_dialogue',
    'ck_sim.ck_voice':            'ck_sim.doing.ck_voice',
    'ck_sim.ck_voice_lattice':    'ck_sim.doing.ck_voice_lattice',
    'ck_sim.ck_language':         'ck_sim.doing.ck_language',
    'ck_sim.ck_reasoning':        'ck_sim.doing.ck_reasoning',
    'ck_sim.ck_sentence_composer': 'ck_sim.doing.ck_sentence_composer',
    'ck_sim.ck_game_sense':       'ck_sim.doing.ck_game_sense',
    'ck_sim.ck_forecast':         'ck_sim.doing.ck_forecast',
    'ck_sim.ck_thesis_writer':    'ck_sim.doing.ck_thesis_writer',
    'ck_sim.ck_pulse_engine':     'ck_sim.doing.ck_pulse_engine',
    'ck_sim.ck_steering':         'ck_sim.doing.ck_steering',
    'ck_sim.ck_llm_filter':       'ck_sim.doing.ck_llm_filter',
    'ck_sim.ck_cloud_flow':       'ck_sim.doing.ck_cloud_flow',
    'ck_sim.ck_cloud_curvature':  'ck_sim.doing.ck_cloud_curvature',
    'ck_sim.ck_cloud_btq':        'ck_sim.doing.ck_cloud_btq',
    'ck_sim.ck_cloud_pfe':        'ck_sim.doing.ck_cloud_pfe',
    'ck_sim.ck_organ_clouds':     'ck_sim.doing.ck_organ_clouds',
    'ck_sim.ck_thinking_lattice': 'ck_sim.doing.ck_thinking_lattice',
    'ck_sim.ck_claude_library':   'ck_sim.doing.ck_claude_library',
    'ck_sim.ck_gpu':              'ck_sim.doing.ck_gpu',
    'ck_sim.ck_fractal_index':    'ck_sim.doing.ck_fractal_index',
    # ── becoming/ ──
    'ck_sim.ck_truth':            'ck_sim.becoming.ck_truth',
    'ck_sim.ck_world_lattice':    'ck_sim.becoming.ck_world_lattice',
    'ck_sim.ck_concept_spine':    'ck_sim.becoming.ck_concept_spine',
    'ck_sim.ck_education':        'ck_sim.becoming.ck_education',
    'ck_sim.ck_lexicon':          'ck_sim.becoming.ck_lexicon',
    'ck_sim.ck_lexicon_bulk':     'ck_sim.becoming.ck_lexicon_bulk',
    'ck_sim.ck_english_build':    'ck_sim.becoming.ck_english_build',
    'ck_sim.ck_d2_dictionary_expander': 'ck_sim.becoming.ck_d2_dictionary_expander',
    'ck_sim.ck_translator':       'ck_sim.becoming.ck_translator',
    'ck_sim.ck_memory':           'ck_sim.becoming.ck_memory',
    'ck_sim.ck_episodic':         'ck_sim.becoming.ck_episodic',
    'ck_sim.ck_metalearning':     'ck_sim.becoming.ck_metalearning',
    'ck_sim.ck_retrieval_engine': 'ck_sim.becoming.ck_retrieval_engine',
    'ck_sim.ck_development':      'ck_sim.becoming.ck_development',
    'ck_sim.ck_identity':         'ck_sim.becoming.ck_identity',
    'ck_sim.ck_network':          'ck_sim.becoming.ck_network',
    'ck_sim.ck_self_mirror':      'ck_sim.becoming.ck_self_mirror',
    'ck_sim.ck_knowledge_bootstrap': 'ck_sim.becoming.ck_knowledge_bootstrap',
    'ck_sim.ck_journal':            'ck_sim.becoming.ck_journal',
    'ck_sim.ck_dictionary_builder': 'ck_sim.becoming.ck_dictionary_builder',
    'ck_sim.ck_activity_log':       'ck_sim.becoming.ck_activity_log',
    'ck_sim.ck_becoming_grammar':   'ck_sim.becoming.ck_becoming_grammar',
    # ── face/ ──
    'ck_sim.ck_web_api':          'ck_sim.face.ck_web_api',
    'ck_sim.ck_sim_app':          'ck_sim.face.ck_sim_app',
    'ck_sim.ck_sim_widgets':      'ck_sim.face.ck_sim_widgets',
    'ck_sim.ck_headless':         'ck_sim.face.ck_headless',
    'ck_sim.ck_sim_audio':        'ck_sim.face.ck_sim_audio',
    'ck_sim.ck_sim_ears':         'ck_sim.face.ck_sim_ears',
    'ck_sim.ck_sim_led':          'ck_sim.face.ck_sim_led',
    'ck_sim.ck_sim_sd':           'ck_sim.face.ck_sim_sd',
    'ck_sim.ck_sim_uart':         'ck_sim.face.ck_sim_uart',
    'ck_sim.ck_robot_body':       'ck_sim.face.ck_robot_body',
    'ck_sim.ck_body_interface':   'ck_sim.face.ck_body_interface',
    'ck_sim.ck_zynq_dog':         'ck_sim.face.ck_zynq_dog',
    'ck_sim.ck_deploy':           'ck_sim.face.ck_deploy',
}


class _CKAliasLoader:
    """Load a module by importing its real location and aliasing it."""
    def __init__(self, real_name):
        self.real_name = real_name

    def create_module(self, spec):
        return importlib.import_module(self.real_name)

    def exec_module(self, module):
        pass  # already loaded by create_module


class _CKAliasFinder:
    """Meta-path finder: redirects old flat paths to B/D/BC subpackages."""

    def find_spec(self, fullname, path, target=None):
        if fullname not in _CK_ALIAS_MAP:
            return None
        real = _CK_ALIAS_MAP[fullname]
        loader = _CKAliasLoader(real)
        return importlib.util.spec_from_loader(fullname, loader)


sys.meta_path.append(_CKAliasFinder())


__all__ = [
    # Being -- what CK IS
    'ck_sim_heartbeat', 'ck_sim_d2', 'ck_sim_brain', 'ck_sim_body',
    'ck_coherence_field', 'ck_personality', 'ck_emotion', 'ck_immune',
    'ck_bonding', 'ck_sensorium', 'ck_swarm', 'ck_sensory_codecs',
    'ck_attention', 'ck_btq', 'ck_sim_btq', 'ck_fractal_health',
    'ck_divine27', 'ck_coherence_action', 'ck_tig_security',
    'ck_fibonacci_transform', 'ck_power_sense', 'ck_coherence_gate',
    # Doing -- what CK DOES
    'ck_sim_engine', 'ck_action', 'ck_goals', 'ck_autodidact',
    'ck_autodidact_runner', 'ck_dialogue', 'ck_voice', 'ck_language',
    'ck_reasoning', 'ck_sentence_composer', 'ck_game_sense', 'ck_forecast',
    'ck_thesis_writer', 'ck_llm_filter',
    'ck_cloud_flow', 'ck_cloud_curvature', 'ck_cloud_btq',
    'ck_cloud_pfe', 'ck_organ_clouds', 'ck_thinking_lattice',
    'ck_claude_library',
    # Becoming -- what CK BECOMES
    'ck_truth', 'ck_world_lattice', 'ck_concept_spine', 'ck_education',
    'ck_lexicon', 'ck_lexicon_bulk', 'ck_english_build',
    'ck_d2_dictionary_expander', 'ck_translator',
    'ck_memory', 'ck_episodic', 'ck_metalearning', 'ck_retrieval_engine',
    'ck_development', 'ck_identity', 'ck_network', 'ck_self_mirror',
    'ck_knowledge_bootstrap', 'ck_journal', 'ck_activity_log',
    'ck_becoming_grammar',
    # Face -- how CK APPEARS
    'ck_web_api',
    'ck_sim_app', 'ck_sim_widgets', 'ck_headless',
    'ck_sim_audio', 'ck_sim_ears', 'ck_sim_led',
    'ck_sim_sd', 'ck_sim_uart',
    'ck_robot_body', 'ck_body_interface', 'ck_zynq_dog', 'ck_deploy',
]
