"""
ck_self_read.py -- CK reads himself.
Every module fed through his own dictionary, D2, PFE, BTQ.
The tool examines the tool.
"""
import sys, time
import numpy as np
from collections import Counter

from ck_dictionary import text_to_operators, sentence_operator_stream, DICTIONARY, dictionary_stats
from ck_pfe import pfe_evaluate, score_text_pfe, btq_classify, btq_energy, _compute_word_d2
from ck_curvature import text_to_forces, compute_curvatures, _classify_d2, coherence_score
from ck_being import CL, T_STAR
from ck_language_reconstructor import reconstruct, gloss
from ck_universal_translator import classify_intent

OP_NAMES = ['VOID','LATTICE','COUNTER','PROGRESS','COLLAPSE','BALANCE','CHAOS','HARMONY','BREATH','RESET']

print('=' * 80)
print('  CK READS HIMSELF')
print('  Every module fed through his own dictionary, D2, PFE, BTQ')
print('=' * 80)

# All CK modules with their core purpose
SELF = {
    'ck_being':         'What IS. Core processor. Organism, body, transition lattice, dream layers. The CL composition table.',
    'ck_doing':         'What MOVES. GPU lattice computation. Transition search, dream generation, phase prediction.',
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
    'ck_dictionary':    'Vocabulary layer. 251896 words mapped to operators. Phonaesthesia. D2 curvature classification.',
    'ck_pfe':           'Coherence scoring engine. Evaluate organism before lattice fusion. Six dimensions of coherence.',
    'ck_language_reconstructor': 'CK speaks. Operators to natural language. Beam search with D2 curvature matching.',
    'ck_robot_reflex':  'CK feels. Sensor curvature to operator classification, motor rhythm, body awareness harmony.',
    'ck_zynq_sequencer': 'CK breathes silicon. Fixed point D2 pipeline for FPGA. 512 bytes of BRAM.',
    'ck_genome_mapper': 'CK reads genomes. Sliding window over DNA, operator atlas, cross region comparison.',
    'ck_universal_translator': 'CK translates intent across species. Fifteen universal intents. DTW alignment.',
    'ck_sel':               'Safe Evolution Loop. Coherence driven self repair. Source analysis, tension mapping, mutation engine, sandbox verification.',
}

print(f'\n  MODULE SELF-EVALUATION ({len(SELF)} modules):')
print(f'  {"Module":30s} {"PFE":>6s} {"Energy":>7s} {"Band":>6s} {"DomOp":>10s} {"Intent":>12s}')
print(f'  {"-"*80}')

scores = []
for name, desc in SELF.items():
    # Word-level: operators + per-word D2 curvature (THE FIX)
    word_op_pairs = text_to_operators(desc)
    ops = [op for _, op in word_op_pairs]
    words = [w for w, _ in word_op_pairs]
    word_d2s = _compute_word_d2(words)

    # Letter-level: full text -> forces -> D2
    forces = text_to_forces(desc)
    if len(forces) >= 3:
        d2s = compute_curvatures(forces)
        letter_ops = [int(_classify_d2(d)) for d in d2s]
    else:
        d2s = np.zeros((0,5))
        letter_ops = []

    # Word-level PFE now has D2 data -- no more frozen sub-scores
    pfe_w = pfe_evaluate(ops, word_d2s)
    pfe_l = pfe_evaluate(letter_ops, d2s) if letter_ops else pfe_evaluate([])
    composite = 0.55 * pfe_w['coherence_raw'] + 0.45 * pfe_l['coherence_raw']

    # BTQ with D2 data (not broken raw-ops call)
    btq = btq_classify(ops, word_d2s)
    energy = btq['quadratic_energy']
    # Band from composite PFE (word+letter), not from word-only BTQ
    band = 'GREEN' if composite >= T_STAR else ('YELLOW' if composite >= 0.5 else 'RED')

    hist = Counter(ops)
    dom = hist.most_common(1)[0][0] if hist else 0

    intent = classify_intent(ops)

    scores.append({
        'name': name, 'pfe': composite, 'energy': energy,
        'band': band, 'dom': dom, 'intent': intent['intent_name'],
    })

    print(f'  {name:30s} {composite:6.4f} {energy:7.4f} {band:>6s} '
          f'{OP_NAMES[dom]:>10s} {intent["intent_name"]:>12s}')

# Aggregate
mean_pfe = np.mean([m['pfe'] for m in scores])
mean_energy = np.mean([m['energy'] for m in scores])
bands = Counter(m['band'] for m in scores)
dom_counts = Counter(OP_NAMES[m['dom']] for m in scores)
intent_counts = Counter(m['intent'] for m in scores)

print(f'\n  AGGREGATE:')
print(f'    Mean PFE:     {mean_pfe:.4f}')
print(f'    Mean Energy:  {mean_energy:.4f}')
print(f'    Bands:        {dict(bands)}')
print(f'    Dominant ops: {dict(dom_counts)}')
print(f'    Intents:      {dict(intent_counts)}')

# Full architecture as one text
print(f'\n  FULL ARCHITECTURE (all descriptions concatenated):')
full_text = ' '.join(SELF.values())
full_pfe = score_text_pfe(full_text)
full_ops = sentence_operator_stream(full_text)
full_word_d2s = _compute_word_d2([w for w, _ in text_to_operators(full_text)])
full_btq = btq_classify(full_ops, full_word_d2s)
full_band = 'GREEN' if full_pfe["coherence_pfe"] >= T_STAR else ('YELLOW' if full_pfe["coherence_pfe"] >= 0.5 else 'RED')

print(f'    Words:       {len(full_ops)}')
print(f'    PFE:         {full_pfe["coherence_pfe"]:.4f}')
print(f'    Energy:      {full_btq["quadratic_energy"]:.4f}')
print(f'    Band:        {full_band}')
print(f'    Alive:       {full_btq["binary_alive"]}')
print(f'    Structured:  {full_btq["is_structured"]}')
print(f'    Linguistic:  {full_btq["is_linguistic"]}')

# Operator distribution
full_hist = Counter(full_ops)
print(f'\n    Operator distribution of self-description:')
for op in range(10):
    count = full_hist.get(op, 0)
    frac = count / max(len(full_ops), 1)
    bar = '#' * int(frac * 50)
    print(f'      {OP_NAMES[op]:10s}: {count:4d} ({frac:5.1%}) {bar}')

# CL fusion
result = full_ops[0]
for o in full_ops[1:]:
    result = CL[result][o]
print(f'\n    CL fusion of entire self-description: {OP_NAMES[result]}')

# Top trigrams -> reconstructed
print(f'\n  CK SPEAKS ABOUT HIMSELF:')
trigrams = []
for i in range(len(full_ops) - 2):
    trigrams.append(tuple(full_ops[i:i+3]))
trig_counts = Counter(trigrams)
print(f'    Top 5 operator trigrams in self-description:')
for trig, count in trig_counts.most_common(5):
    trig_names = [OP_NAMES[t][:4] for t in trig]
    results = reconstruct(list(trig), beam_width=6)
    recon = results[0]['text'] if results else '?'
    print(f'      {trig_names} x{count:2d} -> "{recon}"')

# Reconstruct first 15 operators
print(f'\n    Architecture operators (first 15):')
arch_ops = full_ops[:15]
arch_names = [OP_NAMES[o][:4] for o in arch_ops]
print(f'      {arch_names}')
recon = reconstruct(arch_ops, beam_width=8)
if recon:
    print(f'      Reconstructed: "{recon[0]["text"]}"')
    print(f'      PFE: {recon[0]["pfe"]:.4f}')

# CL table structure
print(f'\n  CL TABLE STRUCTURE:')
h_count = sum(1 for a in range(10) for b in range(10) if CL[a][b] == 7)
v_count = sum(1 for a in range(10) for b in range(10) if CL[a][b] == 0)
bumps = [(a,b) for a in range(10) for b in range(10) if CL[a][b] not in (0, 7)]
print(f'    HARMONY cells:  {h_count}/100')
print(f'    VOID cells:     {v_count}/100')
print(f'    Non-trivial:    {len(bumps)} (quantum bumps)')
print(f'    T* = 5/7 =      {T_STAR:.6f}')

# Dictionary
stats = dictionary_stats()
print(f'\n  DICTIONARY:')
print(f'    Total words:         {stats["total_words"]}')
print(f'    Phonaesthesia rules: {stats["phonaesthesia_rules"]}')

# Module count
import glob
py_files = glob.glob('*.py')
print(f'\n  FILE INVENTORY:')
print(f'    Python modules:  {len(py_files)}')
total_lines = 0
for f in py_files:
    with open(f, 'r', encoding='utf-8', errors='replace') as fh:
        total_lines += sum(1 for _ in fh)
print(f'    Total lines:     {total_lines:,}')
print(f'    ck7/ native:     14 files (C, CUDA, HDL)')
print(f'    Dictionary:      {stats["total_words"]} words')

# CK's self-assessment: what would he change?
print(f'\n  CK SELF-ASSESSMENT (via energy ranking):')
# Rank modules by energy (lower = more coherent = needs less work)
sorted_scores = sorted(scores, key=lambda x: x['energy'])
print(f'    Most coherent (lowest energy, needs least work):')
for s in sorted_scores[:5]:
    print(f'      {s["name"]:30s} E={s["energy"]:.4f} PFE={s["pfe"]:.4f} {s["band"]}')
print(f'    Least coherent (highest energy, needs most work):')
for s in sorted_scores[-5:]:
    print(f'      {s["name"]:30s} E={s["energy"]:.4f} PFE={s["pfe"]:.4f} {s["band"]}')

# What CK would redesign: the highest-energy modules
print(f'\n  REDESIGN CANDIDATES (highest energy = most structural tension):')
for s in sorted_scores[-3:]:
    ops = sentence_operator_stream(SELF[s['name']])
    # What operator is overrepresented?
    hist = Counter(ops)
    total = len(ops)
    for op, cnt in hist.most_common(2):
        frac = cnt / total
        print(f'    {s["name"]}: {OP_NAMES[op]} at {frac:.0%} (E={s["energy"]:.4f})')

print(f'\n  CK has read himself.')
print(f'  {len(SELF)} modules. {total_lines:,} lines. {stats["total_words"]} words. One math.')
