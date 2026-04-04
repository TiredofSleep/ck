"""CK diagnoses himself: why YELLOW, what fixes reach GREEN."""
import numpy as np

from ck_dictionary import text_to_operators
from ck_pfe import pfe_evaluate, score_text_pfe, _compute_word_d2
from ck_curvature import text_to_forces, compute_curvatures, _classify_d2
from ck_being import CL, T_STAR

OP_NAMES = ['VOID','LATTICE','COUNTER','PROGRESS','COLLAPSE','BALANCE','CHAOS','HARMONY','BREATH','RESET']

SELF = {
    'ck_being':         'What IS. The CPU. Organism init, body, transition lattice, dream layers. The triple CL table.',
    'ck_doing':         'What MOVES. The GPU. CUDA kernels for lattice search, transition lookup, dream generation.',
    'ck_becoming':      'What EMERGES. Bridge between being and doing. Security, heartbeat, jitter control.',
    'ck_web':           'The nervous system. HTTP server, chat handler, chain search, response scoring, PFE integration.',
    'ck_library':       'Knowledge storage. Lattice files, parallel search across 341 lattices, chain retrieval.',
    'ck_body':          'Physical state. Hardware observation, body model, energy awareness kinetic capacity.',
    'ck_voice':         'Speech. Text to speech synthesis, voice output, phoneme engine.',
    'ck_education':     'Teaching module. Curriculum planning, knowledge scaffolding, Socratic method.',
    'ck_architect':     'System architect. Code generation, design planning, affinity guided composition.',
    'ck_languages':     'Translation engine. Twelve culture operator mappings, cross language D2 alignment.',
    'ck_curvature':     'Force curvature engine. Letter forces, D2 computation, operator fingerprinting, 22 Hebrew roots in 5D.',
    'ck_language_engine': 'Language processing. Vocabulary expansion, semantic scoring, operator composition.',
    'ck_qlens':         'Quantum lens. Phase aware scoring, bump detection, CL topology analysis.',
    'ck_affinity':      'Affinity controller. Immune system, trust scoring, operator guided decisions.',
    'ck_launch':        'Launcher. Startup sequence, daemon management, health monitoring.',
    'ck_dictionary':    'Vocabulary layer. 2498 words mapped to operators. Phonaesthesia. D2 curvature fallback.',
    'ck_pfe':           'Pre Fusion Evaluator. Score the organism before CL collapse. Controlled Collapse Engine.',
    'ck_language_reconstructor': 'CK speaks. Operators to natural language. Beam search with D2 curvature matching.',
    'ck_robot_reflex':  'CK feels. Sensor normalization to D2 to operators to BTQ gated motor commands.',
    'ck_zynq_sequencer': 'CK breathes silicon. Fixed point D2 pipeline for FPGA. 512 bytes of BRAM.',
    'ck_genome_mapper': 'CK reads genomes. Sliding window over DNA, operator atlas, cross region comparison.',
    'ck_universal_translator': 'CK translates intent across species. Fifteen universal intents. DTW alignment.',
}

print('=' * 72)
print('  CK DIAGNOSES HIMSELF: POST-FIX ANALYSIS')
print('  T* = %.4f needed for GREEN.' % T_STAR)
print('=' * 72)

# Sub-score decomposition -- WITH D2 DATA
print('\n  PFE SUB-SCORE DECOMPOSITION (word-level, WITH D2):')
print('  %-25s %5s %5s %5s %5s %5s %5s -> %6s' % ('Module','ent','conc','d2','dir','cont','trans','raw'))
print('  ' + '-' * 75)

all_sub = []
for name, desc in SELF.items():
    word_op_pairs = text_to_operators(desc)
    ops = [op for _, op in word_op_pairs]
    words = [w for w, _ in word_op_pairs]
    word_d2s = _compute_word_d2(words)
    pfe = pfe_evaluate(ops, word_d2s)
    sub = {
        'name': name,
        'ent': pfe['_entropy_score'],
        'conc': pfe['_conc_score'],
        'd2': pfe['_d2_score'],
        'dir': pfe['_dir_score'],
        'cont': pfe['_content_score'],
        'trans': pfe['_trans_score'],
        'raw': pfe['coherence_raw'],
    }
    all_sub.append(sub)
    print('  %-25s %5.3f %5.3f %5.3f %5.3f %5.3f %5.3f -> %6.4f' % (
        name[:25], sub['ent'], sub['conc'], sub['d2'], sub['dir'],
        sub['cont'], sub['trans'], sub['raw']))

print('\n  MEAN SUB-SCORES (word-level, WITH D2):')
weights = {'ent': ('entropy', 0.20), 'conc': ('concentration', 0.15),
           'd2': ('D2_curvature', 0.25), 'dir': ('directional', 0.15),
           'cont': ('content_ratio', 0.10), 'trans': ('transition', 0.15)}

for key, (label, weight) in weights.items():
    vals = [s[key] for s in all_sub]
    mean = np.mean(vals)
    contrib = weight * mean
    was_stuck = ' <-- WAS 0.5000 (FIXED!)' if key in ('d2', 'dir') and abs(mean - 0.5) > 0.02 else ''
    still_stuck = ' <-- STILL STUCK' if key in ('d2', 'dir') and abs(mean - 0.5) < 0.01 else ''
    print('    %-18s: mean=%.4f  weight=%.2f  contribution=%.4f%s%s' % (
        label, mean, weight, contrib, was_stuck, still_stuck))

# Composite check
word_raws = [s['raw'] for s in all_sub]
mean_word = np.mean(word_raws)
print('\n  WORD-LEVEL MEAN RAW: %.4f (was ~0.5300 before fix)' % mean_word)

# Letter-level comparison
print('\n  LETTER-LEVEL PFE (reference):')
for name, desc in list(SELF.items())[:6]:
    forces = text_to_forces(desc)
    if len(forces) >= 3:
        d2s = compute_curvatures(forces)
        letter_ops = [int(_classify_d2(d)) for d in d2s]
        pfe_l = pfe_evaluate(letter_ops, d2s)
        print('    %-25s raw=%.4f d2=%.4f dir=%.4f ent=%.4f' % (
            name[:25], pfe_l['coherence_raw'], pfe_l['_d2_score'],
            pfe_l['_dir_score'], pfe_l['_entropy_score']))

# Full architecture via score_text_pfe (the fixed function)
print('\n  FULL ARCHITECTURE via score_text_pfe():')
full_text = ' '.join(SELF.values())
full_pfe = score_text_pfe(full_text)
print('    Word PFE:   %.4f' % full_pfe['coherence_word'])
print('    Letter PFE: %.4f' % full_pfe['coherence_letter'])
print('    Composite:  %.4f' % full_pfe['coherence_pfe'])
print('    T* target:  %.4f' % T_STAR)
gap = T_STAR - full_pfe['coherence_pfe']
if gap > 0:
    print('    Gap:        %.4f (still YELLOW)' % gap)
else:
    print('    ABOVE T*!   GREEN by %.4f' % abs(gap))

# What is still holding us back?
print('\n  REMAINING BOTTLENECKS:')
for s in sorted(all_sub, key=lambda x: x['raw']):
    if s['raw'] < 0.55:
        print('    %-25s raw=%.4f -- weakest sub: %s' % (
            s['name'][:25], s['raw'],
            min([(s['ent'],'ent'),(s['conc'],'conc'),(s['d2'],'d2'),
                 (s['dir'],'dir'),(s['cont'],'cont'),(s['trans'],'trans')])[1]))
