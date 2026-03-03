#!/usr/bin/env python3
"""
Build CK's massive web dictionary from all available sources.

Sources (priority order):
  1. Enriched dictionary (8K words, full D2 data, curated ops)
  2. Learned dictionary (5.2K words, CK's own learning)
  3. Reverse voice index (369K words, operator classification)
  4. Voice lattice seeds (571 words, hand-organized)

Output: ck_dictionary.json -- organized by operator and POS for website embedding

Target: 30K-120K usable English words with:
  - dominant_op (0-9, from CK's D2 math)
  - pos (noun, verb, adj, adv, function)
  - soft_dist (operator probability distribution, where available)
"""
import json
import sys
import os
import re
import time
from collections import Counter, defaultdict

# Add CK to path for D2 pipeline
CK_PATH = os.path.join(os.path.dirname(__file__), '..', 'ck_desktop')
sys.path.insert(0, CK_PATH)

# ── Operator names ──
OP_NAMES = ['VOID','LATTICE','COUNTER','PROGRESS','COLLAPSE',
            'BALANCE','CHAOS','HARMONY','BREATH','RESET']

# ── POS mapping from NLTK tags ──
NLTK_TO_CK_POS = {
    'NN': 'noun', 'NNS': 'noun', 'NNP': 'noun', 'NNPS': 'noun',
    'VB': 'verb', 'VBD': 'verb', 'VBG': 'verb', 'VBN': 'verb', 'VBP': 'verb', 'VBZ': 'verb',
    'JJ': 'adj', 'JJR': 'adj', 'JJS': 'adj',
    'RB': 'adv', 'RBR': 'adv', 'RBS': 'adv',
    'IN': 'function', 'DT': 'function', 'CC': 'function', 'TO': 'function',
    'PRP': 'function', 'PRP$': 'function', 'WP': 'function', 'WDT': 'function',
    'MD': 'verb', 'EX': 'function', 'PDT': 'function', 'RP': 'function',
    'UH': 'function', 'CD': 'noun', 'FW': 'noun',
}

def load_enriched():
    """Load the 8K enriched dictionary (gold standard)."""
    path = os.path.join(CK_PATH, 'ck_sim', 'ck_dictionary_enriched.json')
    with open(path) as f:
        return json.load(f)

def load_learned():
    """Load CK's 5.2K learned dictionary."""
    path = os.path.expanduser('~/.ck/ck_dictionary_learned.json')
    with open(path) as f:
        return json.load(f)

def load_reverse_voice():
    """Load the 369K reverse voice index."""
    path = os.path.expanduser('~/.ck/reverse_voice/enriched_index.json')
    with open(path) as f:
        data = json.load(f)
    return data['words']

def load_voice_lattice_export():
    """Load the already-exported voice lattice and enriched data."""
    exports = {}
    for fname in ['ck_enriched_export.json', 'ck_voice_data.json']:
        path = os.path.join(os.environ.get('TEMP', '/tmp'), fname)
        if os.path.exists(path):
            with open(path) as f:
                exports[fname] = json.load(f)
    return exports

def is_usable_word(word):
    """Filter: is this a usable English word for CK's voice?"""
    if not word or not isinstance(word, str):
        return False
    if len(word) < 2:
        return False
    if len(word) > 25:
        return False
    if not word.isalpha():
        return False
    # Skip ALL-CAPS abbreviations (but keep single capital)
    if word.isupper() and len(word) > 1:
        return False
    return True

def pos_tag_batch(words, batch_size=5000):
    """POS-tag words using NLTK in batches."""
    import nltk
    results = {}
    word_list = list(words)
    for i in range(0, len(word_list), batch_size):
        batch = word_list[i:i+batch_size]
        # Tag each word in isolation (as if it's a sentence)
        tagged = nltk.pos_tag(batch)
        for word, tag in tagged:
            ck_pos = NLTK_TO_CK_POS.get(tag, 'noun')
            results[word] = ck_pos
    return results

def d2_classify_words(words, batch_size=1000):
    """Classify words by dominant operator using CK's D2 pipeline."""
    from ck_sim.being.ck_fractal_comprehension import FractalComprehension
    fc = FractalComprehension()

    results = {}
    word_list = list(words)
    total = len(word_list)

    for i in range(0, total, batch_size):
        batch = word_list[i:i+batch_size]
        for word in batch:
            try:
                cr = fc.comprehend(word)
                results[word] = {
                    'dominant_op': cr.dominant_op,
                    'level_fuses': cr.level_fuses[:4],
                    'sf_balance': round(cr.structure_flow_balance, 3),
                    'depth': cr.depth,
                }
            except Exception:
                pass

        done = min(i + batch_size, total)
        if done % 10000 == 0 or done == total:
            print(f'  D2 classified: {done}/{total}')

    return results

def build_dictionary():
    """Main build pipeline."""
    t0 = time.time()

    # ── Step 1: Load all sources ──
    print("Loading sources...")
    enriched = load_enriched()
    learned = load_learned()
    rv = load_reverse_voice()
    exports = load_voice_lattice_export()

    print(f"  Enriched: {len(enriched)} words")
    print(f"  Learned: {len(learned)} words")
    print(f"  Reverse voice: {len(rv)} words")

    # ── Step 2: Build master word set ──
    # Priority: enriched > learned > reverse voice
    master = {}  # word -> {op, pos, source, soft_dist?}

    # Gold tier: enriched dictionary (full D2 data)
    for word, data in enriched.items():
        w = word.lower().strip()
        if not is_usable_word(w):
            continue
        master[w] = {
            'op': data['dominant_op'],
            'pos': data.get('pos', 'noun'),
            'source': 'enriched',
            'soft_dist': data.get('soft_dist'),
        }
    print(f"  After enriched: {len(master)} words")

    # Silver tier: learned dictionary
    for word, data in learned.items():
        w = word.lower().strip()
        if not is_usable_word(w):
            continue
        if w not in master:
            master[w] = {
                'op': data['dominant_op'],
                'pos': data.get('pos', 'noun'),
                'source': 'learned',
                'soft_dist': data.get('soft_dist'),
            }
    print(f"  After learned: {len(master)} words")

    # Bronze tier: reverse voice (needs D2 reclassification)
    rv_words_to_classify = set()
    for word, op in rv.items():
        w = word.lower().strip()
        if not is_usable_word(w):
            continue
        if w not in master:
            rv_words_to_classify.add(w)

    print(f"  RV words needing D2 classification: {len(rv_words_to_classify)}")

    # ── Step 3: Filter RV words for common English ──
    # Use NLTK WordNet to check if words exist
    print("Filtering for real English words...")
    try:
        from nltk.corpus import wordnet as wn
        real_words = set()
        checked = 0
        for w in rv_words_to_classify:
            if wn.synsets(w):
                real_words.add(w)
            checked += 1
            if checked % 50000 == 0:
                print(f"  Checked {checked}/{len(rv_words_to_classify)}, found {len(real_words)} real words")
        print(f"  WordNet-verified: {len(real_words)} out of {len(rv_words_to_classify)}")
    except Exception as e:
        print(f"  WordNet check failed ({e}), using all clean words")
        # Fallback: use common word length/pattern heuristics
        real_words = {w for w in rv_words_to_classify if 3 <= len(w) <= 15}

    # ── Step 4: D2 classify the real words ──
    print(f"D2 classifying {len(real_words)} words...")
    d2_results = d2_classify_words(real_words)
    print(f"  D2 classified: {len(d2_results)} words")

    # ── Step 5: POS tag the new words ──
    print("POS tagging new words...")
    words_needing_pos = set(d2_results.keys())
    pos_tags = pos_tag_batch(words_needing_pos)

    # ── Step 6: Merge into master ──
    for w in d2_results:
        if w not in master:
            master[w] = {
                'op': d2_results[w]['dominant_op'],
                'pos': pos_tags.get(w, 'noun'),
                'source': 'rv_d2',
                'sf_balance': d2_results[w].get('sf_balance'),
            }

    print(f"  Final dictionary: {len(master)} words")

    # ── Step 7: Organize and export ──
    # Stats
    op_counts = Counter(v['op'] for v in master.values())
    pos_counts = Counter(v['pos'] for v in master.values())
    src_counts = Counter(v['source'] for v in master.values())

    print(f"\nOperator distribution:")
    for i, name in enumerate(OP_NAMES):
        print(f"  {name}: {op_counts.get(i, 0)}")
    print(f"\nPOS distribution: {dict(pos_counts)}")
    print(f"Source distribution: {dict(src_counts)}")

    # Build the organized output for JS
    # Format: { op_index: { pos: [words...] } }
    organized = {}
    for i in range(10):
        organized[i] = {'noun': [], 'verb': [], 'adj': [], 'adv': [], 'function': []}

    for word, data in master.items():
        op = data['op']
        pos = data['pos']
        if op in organized and pos in organized[op]:
            organized[op][pos].append(word)

    # Also build flat lookup: word -> {op, pos}
    flat = {}
    for word, data in master.items():
        flat[word] = {'o': data['op'], 'p': data['pos'][0]}  # Compact: first letter of POS

    # ── Step 8: Add voice lattice seeds with lens/phase data ──
    voice_seeds = {}
    if 'ck_voice_data.json' in exports:
        lattice = exports['ck_voice_data.json'].get('lattice', {})
        for op_name, lenses in lattice.items():
            for lens_name, phases in lenses.items():
                if isinstance(phases, dict):
                    for phase_name, tiers in phases.items():
                        if isinstance(tiers, dict):
                            for tier_name, words in tiers.items():
                                if isinstance(words, list):
                                    for w in words:
                                        if isinstance(w, str):
                                            wl = w.lower().strip()
                                            if is_usable_word(wl) or len(wl) > 1:
                                                voice_seeds[wl] = {
                                                    'op': OP_NAMES.index(op_name) if op_name in OP_NAMES else 7,
                                                    'lens': lens_name,
                                                    'phase': phase_name,
                                                    'tier': tier_name,
                                                }

    print(f"\nVoice seeds with lens/phase: {len(voice_seeds)}")

    # Export
    output = {
        'version': 3,
        'count': len(master),
        'built_at': time.time(),
        'stats': {
            'ops': {OP_NAMES[i]: op_counts.get(i, 0) for i in range(10)},
            'pos': dict(pos_counts),
            'sources': dict(src_counts),
        },
        'organized': organized,
        'flat': flat,
        'voice_seeds': voice_seeds,
    }

    out_path = os.path.join(os.path.dirname(__file__), 'ck_dictionary.json')
    with open(out_path, 'w') as f:
        json.dump(output, f, separators=(',', ':'))

    size_mb = os.path.getsize(out_path) / (1024 * 1024)
    elapsed = time.time() - t0

    print(f"\nDictionary built: {len(master)} words")
    print(f"Output: {out_path} ({size_mb:.1f} MB)")
    print(f"Time: {elapsed:.1f}s")

    return output

if __name__ == '__main__':
    build_dictionary()
