"""
ck_pos_tagger.py -- ONE-TIME build script to POS-tag + inflect CK's dictionary.

Run once, store results. Zero NLP cost at runtime.
Uses lemminflect (770KB, numpy-only) for accurate POS + all inflection forms.
Uses inflect for noun pluralization edge cases + a/an selection.

Output: ck_pos_cache.json -- keyed by word, contains:
  {
    "word": {
      "pos": "noun",     # noun / verb / adj / adv / func
      "lemma": "run",    # base form
      "forms": {
        "3ps": "runs",           # verb: 3rd person singular
        "past": "ran",           # verb: past tense
        "past_part": "run",      # verb: past participle
        "prog": "running",       # verb: present participle
        "plural": "churches",    # noun: plural form
        "comp": "bigger",        # adj: comparative
        "super": "biggest",      # adj: superlative
        "adverb": "softly",      # adj -> adverb derivation
      }
    }
  }

Usage:
  python ck_pos_tagger.py
"""

import json
import os
import sys

# ---------------------------------------------------------------------------
# Priority: POS_TAGS from ck_voice_lattice (hand-curated, authoritative)
# ---------------------------------------------------------------------------
try:
    sys.path.insert(0, os.path.dirname(__file__))
    from ck_sim.doing.ck_voice_lattice import POS_TAGS as LATTICE_POS
except ImportError:
    LATTICE_POS = {}

# ---------------------------------------------------------------------------
# Function words (closed class -- memorized, never ambiguous)
# ---------------------------------------------------------------------------
_FUNC_WORDS = frozenset([
    'the', 'a', 'an', 'this', 'that', 'these', 'those',
    'each', 'every', 'all', 'some', 'any', 'no', 'what', 'which',
    'he', 'she', 'it', 'we', 'they', 'one', 'who', 'whose',
    'in', 'on', 'of', 'to', 'for', 'by', 'at', 'from', 'with',
    'into', 'onto', 'upon', 'through', 'between', 'among',
    'within', 'without', 'beyond', 'before', 'after', 'above',
    'below', 'beneath', 'beside', 'toward', 'against', 'along',
    'and', 'but', 'or', 'yet', 'so', 'nor', 'while', 'when',
    'where', 'since', 'until', 'because', 'although', 'unless',
    'not', 'very', 'too', 'quite', 'just', 'also', 'only', 'even',
    'how', 'why', 'if', 'then', 'than', 'as', 'about', 'over',
    'under', 'around', 'near', 'far', 'here', 'there',
    'myself', 'yourself', 'himself', 'herself', 'itself',
    'ourselves', 'themselves', 'his', 'her', 'its', 'our', 'their',
    'my', 'your', 'me', 'us', 'them', 'mine', 'yours', 'ours',
    'theirs', 'hers',
])

_MODAL_VERBS = frozenset([
    'is', 'am', 'are', 'was', 'were', 'be', 'been', 'being',
    'has', 'have', 'had', 'does', 'did', 'do', 'will', 'would',
    'shall', 'should', 'may', 'might', 'can', 'could', 'must',
])

# ---------------------------------------------------------------------------
# NLTK-style Penn Treebank → CK simple POS mapping
# ---------------------------------------------------------------------------
_PTB_TO_CK = {
    'NN': 'noun', 'NNS': 'noun', 'NNP': 'noun', 'NNPS': 'noun',
    'VB': 'verb', 'VBD': 'verb', 'VBG': 'verb', 'VBN': 'verb',
    'VBP': 'verb', 'VBZ': 'verb',
    'JJ': 'adj', 'JJR': 'adj', 'JJS': 'adj',
    'RB': 'adv', 'RBR': 'adv', 'RBS': 'adv',
    'IN': 'func', 'DT': 'func', 'CC': 'func', 'PRP': 'func',
    'PRP$': 'func', 'WDT': 'func', 'WP': 'func', 'WRB': 'func',
    'MD': 'verb', 'TO': 'func', 'EX': 'func', 'PDT': 'func',
    'RP': 'func', 'UH': 'func',
}


def _derive_adverb(adj: str) -> str:
    """Derive adverb from adjective. Rule-based."""
    if adj.endswith('y'):
        return adj[:-1] + 'ily'     # happy -> happily
    if adj.endswith('le'):
        return adj[:-1] + 'y'      # gentle -> gently
    if adj.endswith('ic'):
        return adj + 'ally'         # basic -> basically
    if adj.endswith('ll'):
        return adj + 'y'            # full -> fully
    if adj.endswith('ue'):
        return adj[:-1] + 'ly'     # true -> truly
    return adj + 'ly'               # soft -> softly


def tag_and_inflect(word: str) -> dict:
    """Tag one word with POS and compute all inflection forms.

    Priority chain:
    1. Function words (closed class, memorized)
    2. Suffix-locked POS (unambiguous suffixes force POS)
    3. POS_TAGS from ck_voice_lattice (hand-curated)
    4. lemminflect (NLP-powered) with disambiguation
    5. Suffix heuristic (fallback)

    For AMBIGUOUS words (both noun and verb): store ALL valid POS tags
    in 'all_pos' list, plus inflection forms for EVERY valid POS.
    """
    from lemminflect import getInflection, getAllInflections, getLemma

    w = word.lower().strip()
    entry = {'pos': None, 'all_pos': [], 'lemma': w, 'forms': {}}

    # --- Priority 1: Function words ---
    if w in _FUNC_WORDS:
        if w in _MODAL_VERBS:
            entry['pos'] = 'verb'
            entry['all_pos'] = ['verb']
        else:
            entry['pos'] = 'func'
            entry['all_pos'] = ['func']
        return entry

    # --- Priority 1.5: Non-verb words that look like -ing/-thing ---
    _NOT_VERBS = frozenset([
        'nothing', 'something', 'anything', 'everything',
        'morning', 'evening', 'building', 'ceiling', 'feeling',
        'meaning', 'warning', 'blessing', 'offering', 'beginning',
        'clothing', 'wedding', 'pudding', 'sibling', 'string',
        'spring', 'king', 'ring', 'wing', 'thing', 'sing',
    ])
    if w in _NOT_VERBS:
        entry['pos'] = 'noun'
        entry['all_pos'] = ['noun']
        result = getInflection(w, tag='NNS')
        if result:
            entry['forms']['plural'] = result[0].lower()
        return entry

    # --- Priority 2: Suffix-locked POS (unambiguous) ---
    # These suffixes are SO strong they override everything else
    _locked = None
    # Only lock suffixes that are ALWAYS nouns (never verbs/adj).
    # NOT -ence/-ance: balance, dance, advance, fence, sentence are verbs too.
    if w.endswith(('tion', 'sion', 'ness', 'ment', 'ity',
                   'ism', 'ist', 'dom', 'ship', 'hood')):
        _locked = 'noun'
    elif w.endswith(('ful', 'less', 'ous', 'ible', 'able')) and len(w) > 4:
        _locked = 'adj'
    elif w.endswith('ly') and len(w) > 4:
        _locked = 'adv'

    if _locked:
        entry['pos'] = _locked
        entry['all_pos'] = [_locked]

    # --- Priority 3: Lattice POS (hand-curated) ---
    if entry['pos'] is None and w in LATTICE_POS:
        entry['pos'] = LATTICE_POS[w]
        entry['all_pos'] = [LATTICE_POS[w]]

    # --- Priority 4: lemminflect probing with disambiguation ---
    if entry['pos'] is None:
        valid_pos = []  # All POS this word can serve as
        _has_comp_sup = False  # Does it have comparative/superlative?

        for upos, ck_pos in [('NOUN', 'noun'), ('VERB', 'verb'),
                              ('ADJ', 'adj'), ('ADV', 'adv')]:
            inflections = getAllInflections(w, upos=upos)
            if inflections:
                all_forms = set()
                for tag_forms in inflections.values():
                    all_forms.update(f.lower() for f in tag_forms)
                if w in all_forms:
                    # For ADJ: only count if it has REAL adj forms (JJR/JJS),
                    # not just base JJ which matches almost anything
                    if ck_pos == 'adj':
                        if 'JJR' in inflections or 'JJS' in inflections:
                            valid_pos.append(ck_pos)
                            _has_comp_sup = True
                        # else: skip, it's probably not really an adjective
                    else:
                        valid_pos.append(ck_pos)

            # Also check lemma
            lemmas = getLemma(w, upos=upos)
            if lemmas:
                lemma = lemmas[0].lower()
                if lemma != w and ck_pos not in valid_pos:
                    valid_pos.append(ck_pos)
                    entry['lemma'] = lemma

        if valid_pos:
            entry['all_pos'] = valid_pos
            if len(valid_pos) == 1:
                entry['pos'] = valid_pos[0]
            else:
                # DISAMBIGUATION for ambiguous words:
                # 1. Adverb if -ly suffix (already caught above)
                # 2. Adjective if it has comparative/superlative
                # 3. Noun over verb (most base forms are nouns)
                # 4. Verb if nothing else
                if 'adj' in valid_pos and _has_comp_sup:
                    entry['pos'] = 'adj'
                elif 'noun' in valid_pos:
                    entry['pos'] = 'noun'
                elif 'verb' in valid_pos:
                    entry['pos'] = 'verb'
                elif 'adj' in valid_pos:
                    entry['pos'] = 'adj'
                elif 'adv' in valid_pos:
                    entry['pos'] = 'adv'
                else:
                    entry['pos'] = valid_pos[0]

    # --- Priority 4: Suffix heuristic (fallback) ---
    if entry['pos'] is None:
        if w.endswith('ly') and len(w) > 4:
            entry['pos'] = 'adv'
        elif w.endswith(('ing',)) and len(w) > 4:
            entry['pos'] = 'verb'
        elif w.endswith(('ize', 'ise', 'ify', 'ate')) and len(w) > 4:
            entry['pos'] = 'verb'
        elif w.endswith(('ful', 'less', 'ous', 'ive', 'able', 'ible',
                         'ent', 'ant', 'ial', 'ical', 'al')) and len(w) > 4:
            entry['pos'] = 'adj'
        elif w.endswith(('tion', 'sion', 'ness', 'ment', 'ity', 'ence',
                         'ance', 'ism', 'ist', 'dom', 'ship', 'hood')):
            entry['pos'] = 'noun'
        elif w.endswith('ed') and len(w) > 3:
            entry['pos'] = 'adj'  # Past participle as adjective
        else:
            entry['pos'] = 'noun'  # Conservative default

    # --- Compute inflection forms for ALL valid POS ---
    # This means ambiguous words get BOTH noun and verb forms.
    # At runtime, CK picks the right inflection based on template slot.
    all_pos = entry.get('all_pos', [entry['pos']])
    if not all_pos:
        all_pos = [entry['pos']]

    for pos in all_pos:
        if pos == 'verb':
            # Get lemma (base form) first
            lemmas = getLemma(w, upos='VERB')
            if lemmas:
                base = lemmas[0].lower()
                if entry['pos'] == 'verb':
                    entry['lemma'] = base
            else:
                base = w

            # All verb forms from the BASE form
            for tag, key in [('VBZ', '3ps'), ('VBD', 'past'),
                             ('VBN', 'past_part'), ('VBG', 'prog')]:
                result = getInflection(base, tag=tag)
                if result:
                    entry['forms'][key] = result[0].lower()

        elif pos == 'noun':
            # Plural
            result = getInflection(w, tag='NNS')
            if result:
                entry['forms']['plural'] = result[0].lower()
            else:
                # Fallback: inflect library
                try:
                    import inflect
                    p = inflect.engine()
                    pl = p.plural_noun(w)
                    if pl and pl != w:
                        entry['forms']['plural'] = pl.lower()
                except ImportError:
                    pass

        elif pos == 'adj':
            # Comparative + superlative
            comp = getInflection(w, tag='JJR')
            if comp:
                entry['forms']['comp'] = comp[0].lower()
            sup = getInflection(w, tag='JJS')
            if sup:
                entry['forms']['super'] = sup[0].lower()
            # Adverb derivation
            entry['forms']['adverb'] = _derive_adverb(w)

        elif pos == 'adv':
            # Store base adjective if derivable
            if w.endswith('ly') and len(w) > 4:
                adj_guess = w[:-2]
                if adj_guess.endswith('i'):
                    adj_guess = adj_guess[:-1] + 'y'  # happily -> happy
                entry['forms']['adj_root'] = adj_guess

    return entry


def build_cache(dictionary_path: str, output_path: str):
    """Tag every word in the enriched dictionary. One-time cost."""
    print(f"Loading dictionary from {dictionary_path}...")
    with open(dictionary_path) as f:
        dictionary = json.load(f)

    print(f"Tagging {len(dictionary)} words with POS + inflection forms...")
    cache = {}
    changed = 0

    for i, word in enumerate(dictionary):
        old_pos = dictionary[word].get('pos', 'noun')
        entry = tag_and_inflect(word)
        cache[word] = entry

        if entry['pos'] != old_pos:
            changed += 1

        if (i + 1) % 500 == 0:
            print(f"  {i + 1}/{len(dictionary)} tagged...")

    # Stats
    pos_counts = {}
    forms_count = 0
    for w, e in cache.items():
        pos_counts[e['pos']] = pos_counts.get(e['pos'], 0) + 1
        forms_count += len(e['forms'])

    print(f"\nResults:")
    print(f"  Total words: {len(cache)}")
    print(f"  POS changed from old tagger: {changed}")
    print(f"  Inflection forms computed: {forms_count}")
    print(f"  POS distribution:")
    for k, v in sorted(pos_counts.items(), key=lambda x: -x[1]):
        print(f"    {k}: {v}")

    print(f"\nWriting cache to {output_path}...")
    with open(output_path, 'w') as f:
        json.dump(cache, f, indent=1)

    print("Done!")
    return cache


def verify_samples(cache: dict):
    """Print some samples to verify accuracy."""
    test_words = [
        # Should be nouns
        'nothing', 'church', 'fulfillment', 'priest', 'architecture',
        'redemption', 'nourishment', 'blueprint', 'prophecy', 'apostle',
        # Should be verbs
        'run', 'converge', 'balance', 'mortify', 'sustain', 'explore',
        'pronounce', 'resonate', 'establish', 'complete',
        # Should be adjectives
        'fruitful', 'faultless', 'faithful', 'fatherless', 'beautiful',
        'deep', 'soft', 'gentle', 'bright', 'sacred',
        # Should be adverbs
        'softly', 'gently', 'faithfully', 'solemnly', 'spiritually',
    ]

    print("\nVerification samples:")
    print(f"{'Word':<20} {'POS':<6} {'Lemma':<15} {'Forms'}")
    print("-" * 80)
    for w in test_words:
        if w in cache:
            e = cache[w]
            forms_str = ', '.join(f"{k}={v}" for k, v in e['forms'].items())
            print(f"{w:<20} {e['pos']:<6} {e['lemma']:<15} {forms_str}")
        else:
            print(f"{w:<20} NOT IN DICTIONARY")


if __name__ == '__main__':
    dict_path = os.path.join(os.path.dirname(__file__),
                             'ck_sim', 'ck_dictionary_enriched.json')
    # Also check parent directory
    if not os.path.exists(dict_path):
        alt = os.path.join(os.path.dirname(__file__),
                           '..', '..', 'ck_sim', 'ck_dictionary_enriched.json')
        if os.path.exists(alt):
            dict_path = alt

    out_path = os.path.join(os.path.dirname(__file__), 'ck_pos_cache.json')

    cache = build_cache(dict_path, out_path)
    verify_samples(cache)
