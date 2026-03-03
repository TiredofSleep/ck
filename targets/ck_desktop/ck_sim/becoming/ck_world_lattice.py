# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_world_lattice.py -- CK's World Lattice: Concepts, Languages, Compression
=============================================================================
Operator: LATTICE (1) -- the structure that holds everything.

This is the concept graph that separates "world" from "words."

CK already has:
  - Transition Lattice (TL): operator-to-operator frequency matrix
  - D2 curvature: letters → Hebrew roots → 5D force vectors → operators
  - CL table: 10x10 algebraic composition

This module adds:
  - WorldNode: a concept encoded as operator pattern (not words)
  - WordBinding: a word in any language bound to a concept via D2
  - Relations: operator-labeled edges between concepts
  - Multilingual bindings: the same concept in every language
  - MDL compression: merge redundant nodes, prune weak edges
  - Snapshot: export irreducible core for thumbdrive / FPGA

The key insight: "mother" in English, "madre" in Spanish, "mère" in French,
"Mutter" in German, "мать" (mat') in Russian -- all produce SIMILAR D2
curvature patterns because they share phonetic ancestry. D2 finds the
invariant. The concept node holds the invariant. The word bindings are
just different labels on the same truth.

No LLM. No embeddings. No training data.
D2 curvature IS the universal codec for language.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
import json
import os
from collections import Counter, defaultdict
from typing import Dict, List, Tuple, Optional, Set

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, LATTICE, COUNTER, PROGRESS,
    COLLAPSE, BALANCE, CHAOS, BREATH, RESET,
    OP_NAMES, CL, compose
)
from ck_sim.ck_sim_d2 import D2Pipeline, soft_classify_d2, ROOTS_FLOAT, LATIN_TO_ROOT


# ================================================================
#  TRANSLITERATION: Non-Latin Scripts → Latin Letters → D2
# ================================================================

# Cyrillic → Latin (Russian, Ukrainian, Bulgarian, etc.)
CYRILLIC_TO_LATIN = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e',
    'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k',
    'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
    'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts',
    'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': '', 'ы': 'y', 'ь': '',
    'э': 'e', 'ю': 'yu', 'я': 'ya',
}

# Greek → Latin
GREEK_TO_LATIN = {
    'α': 'a', 'β': 'b', 'γ': 'g', 'δ': 'd', 'ε': 'e', 'ζ': 'z',
    'η': 'e', 'θ': 'th', 'ι': 'i', 'κ': 'k', 'λ': 'l', 'μ': 'm',
    'ν': 'n', 'ξ': 'x', 'ο': 'o', 'π': 'p', 'ρ': 'r', 'σ': 's',
    'ς': 's', 'τ': 't', 'υ': 'u', 'φ': 'ph', 'χ': 'ch', 'ψ': 'ps',
    'ω': 'o',
}

# Arabic → Latin (simplified phonetic)
ARABIC_TO_LATIN = {
    'ا': 'a', 'ب': 'b', 'ت': 't', 'ث': 'th', 'ج': 'j', 'ح': 'h',
    'خ': 'kh', 'د': 'd', 'ذ': 'dh', 'ر': 'r', 'ز': 'z', 'س': 's',
    'ش': 'sh', 'ص': 's', 'ض': 'd', 'ط': 't', 'ظ': 'z', 'ع': 'a',
    'غ': 'gh', 'ف': 'f', 'ق': 'q', 'ك': 'k', 'ل': 'l', 'م': 'm',
    'ن': 'n', 'ه': 'h', 'و': 'w', 'ي': 'y', 'ة': 'a', 'ى': 'a',
}

# Hebrew → Latin (simplified phonetic)
HEBREW_TO_LATIN = {
    'א': 'a', 'ב': 'b', 'ג': 'g', 'ד': 'd', 'ה': 'h', 'ו': 'v',
    'ז': 'z', 'ח': 'ch', 'ט': 't', 'י': 'y', 'כ': 'k', 'ך': 'k',
    'ל': 'l', 'מ': 'm', 'ם': 'm', 'נ': 'n', 'ן': 'n', 'ס': 's',
    'ע': 'a', 'פ': 'p', 'ף': 'f', 'צ': 'ts', 'ץ': 'ts', 'ק': 'q',
    'ר': 'r', 'ש': 'sh', 'ת': 't',
}

# Chinese Pinyin common syllables (Mandarin romanization)
# Full pinyin is already Latin — we just need to handle characters
# For CK, Chinese words are entered as pinyin directly

# Japanese Romaji common kana → Latin
HIRAGANA_TO_LATIN = {
    'あ': 'a', 'い': 'i', 'う': 'u', 'え': 'e', 'お': 'o',
    'か': 'ka', 'き': 'ki', 'く': 'ku', 'け': 'ke', 'こ': 'ko',
    'さ': 'sa', 'し': 'shi', 'す': 'su', 'せ': 'se', 'そ': 'so',
    'た': 'ta', 'ち': 'chi', 'つ': 'tsu', 'て': 'te', 'と': 'to',
    'な': 'na', 'に': 'ni', 'ぬ': 'nu', 'ね': 'ne', 'の': 'no',
    'は': 'ha', 'ひ': 'hi', 'ふ': 'fu', 'へ': 'he', 'ほ': 'ho',
    'ま': 'ma', 'み': 'mi', 'む': 'mu', 'め': 'me', 'も': 'mo',
    'や': 'ya', 'ゆ': 'yu', 'よ': 'yo',
    'ら': 'ra', 'り': 'ri', 'る': 'ru', 'れ': 're', 'ろ': 'ro',
    'わ': 'wa', 'を': 'wo', 'ん': 'n',
    'が': 'ga', 'ぎ': 'gi', 'ぐ': 'gu', 'げ': 'ge', 'ご': 'go',
    'ざ': 'za', 'じ': 'ji', 'ず': 'zu', 'ぜ': 'ze', 'ぞ': 'zo',
    'だ': 'da', 'ぢ': 'ji', 'づ': 'zu', 'で': 'de', 'ど': 'do',
    'ば': 'ba', 'び': 'bi', 'ぶ': 'bu', 'べ': 'be', 'ぼ': 'bo',
    'ぱ': 'pa', 'ぴ': 'pi', 'ぷ': 'pu', 'ぺ': 'pe', 'ぽ': 'po',
}

# Korean Jamo → Latin (simplified)
KOREAN_TO_LATIN = {
    'ㄱ': 'g', 'ㄴ': 'n', 'ㄷ': 'd', 'ㄹ': 'r', 'ㅁ': 'm',
    'ㅂ': 'b', 'ㅅ': 's', 'ㅇ': '', 'ㅈ': 'j', 'ㅊ': 'ch',
    'ㅋ': 'k', 'ㅌ': 't', 'ㅍ': 'p', 'ㅎ': 'h',
    'ㅏ': 'a', 'ㅑ': 'ya', 'ㅓ': 'eo', 'ㅕ': 'yeo', 'ㅗ': 'o',
    'ㅛ': 'yo', 'ㅜ': 'u', 'ㅠ': 'yu', 'ㅡ': 'eu', 'ㅣ': 'i',
}

# Hindi Devanagari → Latin (simplified IAST-like)
DEVANAGARI_TO_LATIN = {
    'अ': 'a', 'आ': 'aa', 'इ': 'i', 'ई': 'ii', 'उ': 'u', 'ऊ': 'uu',
    'ए': 'e', 'ऐ': 'ai', 'ओ': 'o', 'औ': 'au',
    'क': 'ka', 'ख': 'kha', 'ग': 'ga', 'घ': 'gha', 'ङ': 'nga',
    'च': 'cha', 'छ': 'chha', 'ज': 'ja', 'झ': 'jha', 'ञ': 'nya',
    'ट': 'ta', 'ठ': 'tha', 'ड': 'da', 'ढ': 'dha', 'ण': 'na',
    'त': 'ta', 'थ': 'tha', 'द': 'da', 'ध': 'dha', 'न': 'na',
    'प': 'pa', 'फ': 'pha', 'ब': 'ba', 'भ': 'bha', 'म': 'ma',
    'य': 'ya', 'र': 'ra', 'ल': 'la', 'व': 'va',
    'श': 'sha', 'ष': 'sha', 'स': 'sa', 'ह': 'ha',
}

# Master transliteration dispatch
_ALL_TRANSLIT = {}
_ALL_TRANSLIT.update(CYRILLIC_TO_LATIN)
_ALL_TRANSLIT.update(GREEK_TO_LATIN)
_ALL_TRANSLIT.update(ARABIC_TO_LATIN)
_ALL_TRANSLIT.update(HEBREW_TO_LATIN)
_ALL_TRANSLIT.update(HIRAGANA_TO_LATIN)
_ALL_TRANSLIT.update(KOREAN_TO_LATIN)
_ALL_TRANSLIT.update(DEVANAGARI_TO_LATIN)


def transliterate(text: str) -> str:
    """Convert any script to Latin letters for D2 processing.

    Latin letters pass through unchanged. Non-Latin characters are
    transliterated via phonetic tables. Unknown characters are dropped.
    """
    result = []
    for ch in text.lower():
        if 'a' <= ch <= 'z':
            result.append(ch)
        elif ch in _ALL_TRANSLIT:
            result.append(_ALL_TRANSLIT[ch])
        # else: skip (spaces, punctuation, unknown scripts)
    return ''.join(result)


# ================================================================
#  D2 ANALYSIS FOR ANY LANGUAGE
# ================================================================

def word_to_d2(word: str) -> Tuple[int, List[int], List[float], List[float]]:
    """Run D2 on a word (any language/script).

    Returns:
        (dominant_op, operator_seq, mean_d2_vec, soft_dist)
    """
    latin = transliterate(word)
    if not latin:
        return (VOID, [], [0.0] * 5, [0.1] * NUM_OPS)

    pipe = D2Pipeline()
    ops = []
    vecs = []
    for ch in latin:
        if 'a' <= ch <= 'z':
            if pipe.feed_symbol(ord(ch) - ord('a')):
                ops.append(pipe.operator)
                vecs.append(pipe.d2_float[:])

    if not ops:
        return (VOID, [], [0.0] * 5, [0.1] * NUM_OPS)

    # Dominant operator
    counts = Counter(ops)
    dominant = counts.most_common(1)[0][0]

    # Mean D2 vector
    mean_d2 = [0.0] * 5
    for v in vecs:
        for i in range(5):
            mean_d2[i] += v[i]
    for i in range(5):
        mean_d2[i] /= len(vecs)

    # Soft distribution
    soft = soft_classify_d2(pipe.d2_float)

    return (dominant, ops, mean_d2, soft)


def d2_agreement(word_a: str, word_b: str) -> float:
    """Measure D2 agreement between two words (any language).

    Returns 0.0 (totally different) to 1.0 (identical curvature).
    """
    _, _, vec_a, _ = word_to_d2(word_a)
    _, _, vec_b, _ = word_to_d2(word_b)

    # Cosine similarity on 5D vectors
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    mag_a = math.sqrt(sum(a * a for a in vec_a)) or 1e-10
    mag_b = math.sqrt(sum(b * b for b in vec_b)) or 1e-10

    return max(0.0, dot / (mag_a * mag_b))


# ================================================================
#  WORLD NODE: A Concept Encoded as Operator Pattern
# ================================================================

class WorldNode:
    """A concept in CK's world lattice.

    Not a word. Not a definition. A mathematical object:
    - operator_code: dominant TIG operator (the concept's "type")
    - d2_signature: 5D curvature vector (the concept's identity)
    - soft_dist: 10-value operator distribution (the concept's full profile)

    The same concept exists regardless of language.
    "Water" and "agua" and "eau" and "Wasser" are all bindings
    to the same WorldNode.
    """

    __slots__ = ('node_id', 'operator_code', 'd2_signature', 'soft_dist',
                 'domain', 'depth', 'relations', 'bindings')

    def __init__(self, node_id: str, operator_code: int,
                 d2_signature: List[float] = None,
                 soft_dist: List[float] = None,
                 domain: str = 'general'):
        self.node_id = node_id
        self.operator_code = operator_code
        self.d2_signature = d2_signature or [0.0] * 5
        self.soft_dist = soft_dist or [0.0] * NUM_OPS
        self.domain = domain
        self.depth = 0  # 0=root concept, 1=subconcept, 2=detail
        self.relations: Dict[str, List[Tuple[str, int]]] = {}  # rel_type → [(target_id, op)]
        self.bindings: Dict[str, str] = {}  # language_code → word

    def add_relation(self, rel_type: str, target_id: str, operator: int):
        """Add a relation edge to another node."""
        if rel_type not in self.relations:
            self.relations[rel_type] = []
        self.relations[rel_type].append((target_id, operator))

    def bind_word(self, language: str, word: str):
        """Bind a word in a language to this concept."""
        self.bindings[language] = word

    def to_dict(self) -> dict:
        return {
            'node_id': self.node_id,
            'operator_code': self.operator_code,
            'd2_signature': [round(v, 6) for v in self.d2_signature],
            'soft_dist': [round(v, 4) for v in self.soft_dist],
            'domain': self.domain,
            'depth': self.depth,
            'relations': self.relations,
            'bindings': self.bindings,
        }

    @classmethod
    def from_dict(cls, d: dict) -> 'WorldNode':
        node = cls(
            d['node_id'], d['operator_code'],
            d.get('d2_signature'), d.get('soft_dist'),
            d.get('domain', 'general')
        )
        node.depth = d.get('depth', 0)
        node.relations = d.get('relations', {})
        node.bindings = d.get('bindings', {})
        return node


# ================================================================
#  RELATION TYPES (operator-coded)
# ================================================================

# Relations between concepts, each associated with an operator meaning
RELATION_TYPES = {
    'is_a':       LATTICE,   # structural: "dog is_a animal"
    'has':        COUNTER,   # measurement: "body has arms"
    'causes':     PROGRESS,  # forward: "fire causes heat"
    'opposes':    COLLAPSE,  # tension: "life opposes death"
    'balances':   BALANCE,   # equilibrium: "supply balances demand"
    'transforms': CHAOS,     # creative: "caterpillar transforms butterfly"
    'harmonizes': HARMONY,   # coherence: "rhythm harmonizes movement"
    'sustains':   BREATH,    # cycle: "water sustains life"
    'resets':     RESET,     # renewal: "sleep resets mind"
    'contains':   LATTICE,   # structural: "ocean contains fish"
    'part_of':    LATTICE,   # structural: "wheel part_of car"
    'precedes':   PROGRESS,  # temporal: "spring precedes summer"
    'follows':    PROGRESS,  # temporal: "effect follows cause"
    'enables':    PROGRESS,  # causal: "key enables door"
    'prevents':   COLLAPSE,  # blocking: "vaccine prevents disease"
    'resembles':  HARMONY,   # similarity: "moon resembles eye"
}


# ================================================================
#  CONCEPT SEED CORPUS: The Core Concepts of Reality
# ================================================================
# Each entry: (node_id, domain, operator, {lang: word, ...})
# These are the irreducible concepts -- everything else derives.

CORE_CONCEPTS = [
    # ── EXISTENCE & BEING ──────────────────────────────────
    ('existence', 'metaphysics', HARMONY, {
        'en': 'existence', 'es': 'existencia', 'fr': 'existence',
        'de': 'Existenz', 'it': 'esistenza', 'pt': 'existencia',
        'ru': 'существование', 'ar': 'وجود', 'he': 'קיום',
        'zh': 'cunzai', 'ja': 'sonzai', 'ko': 'jonjae', 'hi': 'astitva',
        'la': 'existentia', 'el': 'ύπαρξη',
    }),
    ('void', 'metaphysics', VOID, {
        'en': 'void', 'es': 'vacio', 'fr': 'vide', 'de': 'Leere',
        'it': 'vuoto', 'pt': 'vazio', 'ru': 'пустота', 'ar': 'فراغ',
        'he': 'ריק', 'zh': 'xuwu', 'ja': 'kuu', 'hi': 'shunya',
        'la': 'vacuum', 'el': 'κενό',
    }),
    ('truth', 'metaphysics', HARMONY, {
        'en': 'truth', 'es': 'verdad', 'fr': 'verite', 'de': 'Wahrheit',
        'it': 'verita', 'pt': 'verdade', 'ru': 'правда', 'ar': 'حقيقة',
        'he': 'אמת', 'zh': 'zhenli', 'ja': 'shinri', 'hi': 'satya',
        'la': 'veritas', 'el': 'αλήθεια',
    }),
    ('change', 'metaphysics', PROGRESS, {
        'en': 'change', 'es': 'cambio', 'fr': 'changement', 'de': 'Wandel',
        'it': 'cambiamento', 'pt': 'mudanca', 'ru': 'изменение',
        'ar': 'تغيير', 'he': 'שינוי', 'zh': 'bianhua', 'ja': 'henka',
        'hi': 'parivartan', 'la': 'mutatio',
    }),
    ('order', 'metaphysics', LATTICE, {
        'en': 'order', 'es': 'orden', 'fr': 'ordre', 'de': 'Ordnung',
        'it': 'ordine', 'pt': 'ordem', 'ru': 'порядок', 'ar': 'نظام',
        'he': 'סדר', 'zh': 'zhixu', 'ja': 'chitsujo', 'hi': 'vyavastha',
        'la': 'ordo',
    }),
    ('chaos_concept', 'metaphysics', CHAOS, {
        'en': 'chaos', 'es': 'caos', 'fr': 'chaos', 'de': 'Chaos',
        'it': 'caos', 'pt': 'caos', 'ru': 'хаос', 'ar': 'فوضى',
        'he': 'תוהו', 'zh': 'hundun', 'ja': 'konton', 'hi': 'arajkata',
        'la': 'chaos', 'el': 'χάος',
    }),
    ('balance_concept', 'metaphysics', BALANCE, {
        'en': 'balance', 'es': 'equilibrio', 'fr': 'equilibre',
        'de': 'Gleichgewicht', 'it': 'equilibrio', 'pt': 'equilibrio',
        'ru': 'равновесие', 'ar': 'توازن', 'he': 'איזון',
        'zh': 'pingheng', 'ja': 'kinkou', 'hi': 'santulan',
    }),
    ('time', 'metaphysics', PROGRESS, {
        'en': 'time', 'es': 'tiempo', 'fr': 'temps', 'de': 'Zeit',
        'it': 'tempo', 'pt': 'tempo', 'ru': 'время', 'ar': 'وقت',
        'he': 'זמן', 'zh': 'shijian', 'ja': 'jikan', 'ko': 'sigan',
        'hi': 'samay', 'la': 'tempus', 'el': 'χρόνος',
    }),
    ('space', 'metaphysics', LATTICE, {
        'en': 'space', 'es': 'espacio', 'fr': 'espace', 'de': 'Raum',
        'it': 'spazio', 'pt': 'espaco', 'ru': 'пространство',
        'ar': 'فضاء', 'he': 'מרחב', 'zh': 'kongjian', 'ja': 'kuukan',
        'hi': 'antariksha', 'la': 'spatium',
    }),
    ('infinity', 'metaphysics', BREATH, {
        'en': 'infinity', 'es': 'infinito', 'fr': 'infini',
        'de': 'Unendlichkeit', 'it': 'infinito', 'pt': 'infinito',
        'ru': 'бесконечность', 'ar': 'لانهاية', 'he': 'אינסוף',
        'zh': 'wuqiong', 'ja': 'mugen', 'hi': 'anant',
        'la': 'infinitas',
    }),

    # ── FAMILY & KINSHIP ──────────────────────────────────
    ('mother', 'family', HARMONY, {
        'en': 'mother', 'es': 'madre', 'fr': 'mere', 'de': 'Mutter',
        'it': 'madre', 'pt': 'mae', 'ru': 'мать', 'ar': 'أم',
        'he': 'אמא', 'zh': 'muqin', 'ja': 'haha', 'ko': 'eomeoni',
        'hi': 'maa', 'la': 'mater', 'el': 'μητέρα',
        'sw': 'mama', 'tr': 'anne', 'pl': 'matka',
    }),
    ('father', 'family', LATTICE, {
        'en': 'father', 'es': 'padre', 'fr': 'pere', 'de': 'Vater',
        'it': 'padre', 'pt': 'pai', 'ru': 'отец', 'ar': 'أب',
        'he': 'אבא', 'zh': 'fuqin', 'ja': 'chichi', 'ko': 'abeoji',
        'hi': 'pita', 'la': 'pater', 'el': 'πατέρας',
        'sw': 'baba', 'tr': 'baba', 'pl': 'ojciec',
    }),
    ('child', 'family', PROGRESS, {
        'en': 'child', 'es': 'nino', 'fr': 'enfant', 'de': 'Kind',
        'it': 'bambino', 'pt': 'crianca', 'ru': 'ребёнок',
        'ar': 'طفل', 'he': 'ילד', 'zh': 'haizi', 'ja': 'kodomo',
        'hi': 'baccha', 'la': 'infans',
    }),
    ('brother', 'family', BALANCE, {
        'en': 'brother', 'es': 'hermano', 'fr': 'frere', 'de': 'Bruder',
        'it': 'fratello', 'pt': 'irmao', 'ru': 'брат', 'ar': 'أخ',
        'he': 'אח', 'zh': 'xiongdi', 'ja': 'kyoudai', 'hi': 'bhai',
        'la': 'frater',
    }),
    ('sister', 'family', BALANCE, {
        'en': 'sister', 'es': 'hermana', 'fr': 'soeur', 'de': 'Schwester',
        'it': 'sorella', 'pt': 'irma', 'ru': 'сестра', 'ar': 'أخت',
        'he': 'אחות', 'zh': 'jiemei', 'ja': 'shimai', 'hi': 'behen',
        'la': 'soror',
    }),
    ('home', 'family', HARMONY, {
        'en': 'home', 'es': 'hogar', 'fr': 'maison', 'de': 'Heim',
        'it': 'casa', 'pt': 'lar', 'ru': 'дом', 'ar': 'بيت',
        'he': 'בית', 'zh': 'jia', 'ja': 'ie', 'hi': 'ghar',
        'la': 'domus', 'sw': 'nyumba', 'tr': 'ev',
    }),
    ('love', 'family', HARMONY, {
        'en': 'love', 'es': 'amor', 'fr': 'amour', 'de': 'Liebe',
        'it': 'amore', 'pt': 'amor', 'ru': 'любовь', 'ar': 'حب',
        'he': 'אהבה', 'zh': 'ai', 'ja': 'ai', 'ko': 'sarang',
        'hi': 'prem', 'la': 'amor', 'el': 'αγάπη',
        'sw': 'upendo', 'tr': 'ask',
    }),

    # ── BODY ──────────────────────────────────────────────
    ('body', 'anatomy', LATTICE, {
        'en': 'body', 'es': 'cuerpo', 'fr': 'corps', 'de': 'Koerper',
        'it': 'corpo', 'pt': 'corpo', 'ru': 'тело', 'ar': 'جسم',
        'he': 'גוף', 'zh': 'shenti', 'ja': 'karada', 'hi': 'sharir',
        'la': 'corpus',
    }),
    ('heart', 'anatomy', BREATH, {
        'en': 'heart', 'es': 'corazon', 'fr': 'coeur', 'de': 'Herz',
        'it': 'cuore', 'pt': 'coracao', 'ru': 'сердце', 'ar': 'قلب',
        'he': 'לב', 'zh': 'xin', 'ja': 'shinzou', 'hi': 'hridaya',
        'la': 'cor', 'el': 'καρδιά',
    }),
    ('mind', 'anatomy', COUNTER, {
        'en': 'mind', 'es': 'mente', 'fr': 'esprit', 'de': 'Geist',
        'it': 'mente', 'pt': 'mente', 'ru': 'разум', 'ar': 'عقل',
        'he': 'מוח', 'zh': 'xinzhi', 'ja': 'kokoro', 'hi': 'manas',
        'la': 'mens',
    }),
    ('eye', 'anatomy', COUNTER, {
        'en': 'eye', 'es': 'ojo', 'fr': 'oeil', 'de': 'Auge',
        'it': 'occhio', 'pt': 'olho', 'ru': 'глаз', 'ar': 'عين',
        'he': 'עין', 'zh': 'yan', 'ja': 'me', 'hi': 'aankh',
        'la': 'oculus',
    }),
    ('hand', 'anatomy', PROGRESS, {
        'en': 'hand', 'es': 'mano', 'fr': 'main', 'de': 'Hand',
        'it': 'mano', 'pt': 'mao', 'ru': 'рука', 'ar': 'يد',
        'he': 'יד', 'zh': 'shou', 'ja': 'te', 'hi': 'haath',
        'la': 'manus',
    }),
    ('blood', 'anatomy', BREATH, {
        'en': 'blood', 'es': 'sangre', 'fr': 'sang', 'de': 'Blut',
        'it': 'sangue', 'pt': 'sangue', 'ru': 'кровь', 'ar': 'دم',
        'he': 'דם', 'zh': 'xue', 'ja': 'chi', 'hi': 'khoon',
        'la': 'sanguis',
    }),
    ('breath_concept', 'anatomy', BREATH, {
        'en': 'breath', 'es': 'aliento', 'fr': 'souffle', 'de': 'Atem',
        'it': 'respiro', 'pt': 'sopro', 'ru': 'дыхание', 'ar': 'نفس',
        'he': 'נשימה', 'zh': 'huxi', 'ja': 'iki', 'hi': 'saans',
        'la': 'spiritus',
    }),

    # ── NATURE ────────────────────────────────────────────
    ('water', 'nature', BREATH, {
        'en': 'water', 'es': 'agua', 'fr': 'eau', 'de': 'Wasser',
        'it': 'acqua', 'pt': 'agua', 'ru': 'вода', 'ar': 'ماء',
        'he': 'מים', 'zh': 'shui', 'ja': 'mizu', 'ko': 'mul',
        'hi': 'pani', 'la': 'aqua', 'el': 'νερό',
        'sw': 'maji', 'tr': 'su',
    }),
    ('fire', 'nature', CHAOS, {
        'en': 'fire', 'es': 'fuego', 'fr': 'feu', 'de': 'Feuer',
        'it': 'fuoco', 'pt': 'fogo', 'ru': 'огонь', 'ar': 'نار',
        'he': 'אש', 'zh': 'huo', 'ja': 'hi', 'hi': 'agni',
        'la': 'ignis', 'el': 'φωτιά',
    }),
    ('earth_element', 'nature', LATTICE, {
        'en': 'earth', 'es': 'tierra', 'fr': 'terre', 'de': 'Erde',
        'it': 'terra', 'pt': 'terra', 'ru': 'земля', 'ar': 'أرض',
        'he': 'אדמה', 'zh': 'tu', 'ja': 'tsuchi', 'hi': 'dharti',
        'la': 'terra', 'el': 'γη',
    }),
    ('air', 'nature', BREATH, {
        'en': 'air', 'es': 'aire', 'fr': 'air', 'de': 'Luft',
        'it': 'aria', 'pt': 'ar', 'ru': 'воздух', 'ar': 'هواء',
        'he': 'אוויר', 'zh': 'kongqi', 'ja': 'kuuki', 'hi': 'hawa',
        'la': 'aer',
    }),
    ('sun', 'nature', HARMONY, {
        'en': 'sun', 'es': 'sol', 'fr': 'soleil', 'de': 'Sonne',
        'it': 'sole', 'pt': 'sol', 'ru': 'солнце', 'ar': 'شمس',
        'he': 'שמש', 'zh': 'taiyang', 'ja': 'taiyou', 'hi': 'surya',
        'la': 'sol', 'el': 'ήλιος',
    }),
    ('moon', 'nature', BALANCE, {
        'en': 'moon', 'es': 'luna', 'fr': 'lune', 'de': 'Mond',
        'it': 'luna', 'pt': 'lua', 'ru': 'луна', 'ar': 'قمر',
        'he': 'ירח', 'zh': 'yueliang', 'ja': 'tsuki', 'hi': 'chandrama',
        'la': 'luna',
    }),
    ('star', 'nature', HARMONY, {
        'en': 'star', 'es': 'estrella', 'fr': 'etoile', 'de': 'Stern',
        'it': 'stella', 'pt': 'estrela', 'ru': 'звезда', 'ar': 'نجم',
        'he': 'כוכב', 'zh': 'xingxing', 'ja': 'hoshi', 'hi': 'tara',
        'la': 'stella', 'el': 'αστέρι',
    }),
    ('tree', 'nature', LATTICE, {
        'en': 'tree', 'es': 'arbol', 'fr': 'arbre', 'de': 'Baum',
        'it': 'albero', 'pt': 'arvore', 'ru': 'дерево', 'ar': 'شجرة',
        'he': 'עץ', 'zh': 'shu', 'ja': 'ki', 'hi': 'ped',
        'la': 'arbor',
    }),
    ('mountain', 'nature', LATTICE, {
        'en': 'mountain', 'es': 'montana', 'fr': 'montagne', 'de': 'Berg',
        'it': 'montagna', 'pt': 'montanha', 'ru': 'гора', 'ar': 'جبل',
        'he': 'הר', 'zh': 'shan', 'ja': 'yama', 'hi': 'parvat',
        'la': 'mons',
    }),
    ('river', 'nature', PROGRESS, {
        'en': 'river', 'es': 'rio', 'fr': 'riviere', 'de': 'Fluss',
        'it': 'fiume', 'pt': 'rio', 'ru': 'река', 'ar': 'نهر',
        'he': 'נהר', 'zh': 'he', 'ja': 'kawa', 'hi': 'nadi',
        'la': 'flumen',
    }),
    ('ocean', 'nature', BREATH, {
        'en': 'ocean', 'es': 'oceano', 'fr': 'ocean', 'de': 'Ozean',
        'it': 'oceano', 'pt': 'oceano', 'ru': 'океан', 'ar': 'محيط',
        'he': 'אוקיינוס', 'zh': 'haiyang', 'ja': 'umi', 'hi': 'sagar',
        'la': 'oceanus',
    }),
    ('seed', 'nature', RESET, {
        'en': 'seed', 'es': 'semilla', 'fr': 'graine', 'de': 'Samen',
        'it': 'seme', 'pt': 'semente', 'ru': 'семя', 'ar': 'بذرة',
        'he': 'זרע', 'zh': 'zhongzi', 'ja': 'tane', 'hi': 'beej',
        'la': 'semen',
    }),

    # ── LIFE & DEATH ──────────────────────────────────────
    ('life', 'biology', BREATH, {
        'en': 'life', 'es': 'vida', 'fr': 'vie', 'de': 'Leben',
        'it': 'vita', 'pt': 'vida', 'ru': 'жизнь', 'ar': 'حياة',
        'he': 'חיים', 'zh': 'shengming', 'ja': 'inochi', 'hi': 'jeevan',
        'la': 'vita', 'el': 'ζωή',
    }),
    ('death', 'biology', COLLAPSE, {
        'en': 'death', 'es': 'muerte', 'fr': 'mort', 'de': 'Tod',
        'it': 'morte', 'pt': 'morte', 'ru': 'смерть', 'ar': 'موت',
        'he': 'מוות', 'zh': 'siwang', 'ja': 'shi', 'hi': 'mrityu',
        'la': 'mors', 'el': 'θάνατος',
    }),
    ('birth', 'biology', RESET, {
        'en': 'birth', 'es': 'nacimiento', 'fr': 'naissance', 'de': 'Geburt',
        'it': 'nascita', 'pt': 'nascimento', 'ru': 'рождение',
        'ar': 'ولادة', 'he': 'לידה', 'zh': 'chusheng', 'ja': 'tanjou',
        'hi': 'janma', 'la': 'nativitas',
    }),
    ('growth', 'biology', PROGRESS, {
        'en': 'growth', 'es': 'crecimiento', 'fr': 'croissance',
        'de': 'Wachstum', 'it': 'crescita', 'pt': 'crescimento',
        'ru': 'рост', 'ar': 'نمو', 'he': 'צמיחה', 'zh': 'chengzhang',
        'ja': 'seichou', 'hi': 'vikas',
    }),
    ('cell', 'biology', LATTICE, {
        'en': 'cell', 'es': 'celula', 'fr': 'cellule', 'de': 'Zelle',
        'it': 'cellula', 'pt': 'celula', 'ru': 'клетка',
        'ar': 'خلية', 'he': 'תא', 'zh': 'xibao', 'ja': 'saibou',
        'hi': 'koshika',
    }),
    ('dna', 'biology', LATTICE, {
        'en': 'dna', 'es': 'adn', 'fr': 'adn', 'de': 'dns',
        'it': 'dna', 'pt': 'adn', 'ru': 'днк', 'zh': 'dna',
        'ja': 'dna',
    }),

    # ── EMOTION ───────────────────────────────────────────
    ('joy', 'emotion', HARMONY, {
        'en': 'joy', 'es': 'alegria', 'fr': 'joie', 'de': 'Freude',
        'it': 'gioia', 'pt': 'alegria', 'ru': 'радость', 'ar': 'فرح',
        'he': 'שמחה', 'zh': 'kuaile', 'ja': 'yorokobi', 'hi': 'anand',
        'la': 'gaudium',
    }),
    ('sorrow', 'emotion', COLLAPSE, {
        'en': 'sorrow', 'es': 'tristeza', 'fr': 'chagrin', 'de': 'Trauer',
        'it': 'dolore', 'pt': 'tristeza', 'ru': 'печаль', 'ar': 'حزن',
        'he': 'עצב', 'zh': 'beishang', 'ja': 'kanashimi', 'hi': 'dukh',
    }),
    ('fear', 'emotion', COLLAPSE, {
        'en': 'fear', 'es': 'miedo', 'fr': 'peur', 'de': 'Angst',
        'it': 'paura', 'pt': 'medo', 'ru': 'страх', 'ar': 'خوف',
        'he': 'פחד', 'zh': 'kongju', 'ja': 'kyoufu', 'hi': 'dar',
        'la': 'timor',
    }),
    ('anger', 'emotion', CHAOS, {
        'en': 'anger', 'es': 'ira', 'fr': 'colere', 'de': 'Wut',
        'it': 'rabbia', 'pt': 'raiva', 'ru': 'гнев', 'ar': 'غضب',
        'he': 'כעס', 'zh': 'fennu', 'ja': 'ikari', 'hi': 'krodh',
        'la': 'ira',
    }),
    ('peace', 'emotion', HARMONY, {
        'en': 'peace', 'es': 'paz', 'fr': 'paix', 'de': 'Frieden',
        'it': 'pace', 'pt': 'paz', 'ru': 'мир', 'ar': 'سلام',
        'he': 'שלום', 'zh': 'heping', 'ja': 'heiwa', 'hi': 'shanti',
        'la': 'pax', 'el': 'ειρήνη',
    }),
    ('hope', 'emotion', PROGRESS, {
        'en': 'hope', 'es': 'esperanza', 'fr': 'espoir', 'de': 'Hoffnung',
        'it': 'speranza', 'pt': 'esperanca', 'ru': 'надежда',
        'ar': 'أمل', 'he': 'תקווה', 'zh': 'xiwang', 'ja': 'kibou',
        'hi': 'asha', 'la': 'spes',
    }),
    ('courage', 'emotion', CHAOS, {
        'en': 'courage', 'es': 'coraje', 'fr': 'courage', 'de': 'Mut',
        'it': 'coraggio', 'pt': 'coragem', 'ru': 'мужество',
        'ar': 'شجاعة', 'he': 'אומץ', 'zh': 'yongqi', 'ja': 'yuuki',
        'hi': 'himmat',
    }),

    # ── PHYSICS ───────────────────────────────────────────
    ('energy', 'physics', CHAOS, {
        'en': 'energy', 'es': 'energia', 'fr': 'energie', 'de': 'Energie',
        'it': 'energia', 'pt': 'energia', 'ru': 'энергия', 'ar': 'طاقة',
        'he': 'אנרגיה', 'zh': 'nengliang', 'ja': 'enerugii',
        'hi': 'urja', 'la': 'energia',
    }),
    ('force', 'physics', PROGRESS, {
        'en': 'force', 'es': 'fuerza', 'fr': 'force', 'de': 'Kraft',
        'it': 'forza', 'pt': 'forca', 'ru': 'сила', 'ar': 'قوة',
        'he': 'כוח', 'zh': 'li', 'ja': 'chikara', 'hi': 'bal',
        'la': 'vis',
    }),
    ('wave', 'physics', BREATH, {
        'en': 'wave', 'es': 'onda', 'fr': 'onde', 'de': 'Welle',
        'it': 'onda', 'pt': 'onda', 'ru': 'волна', 'ar': 'موجة',
        'he': 'גל', 'zh': 'bo', 'ja': 'nami', 'hi': 'lahar',
        'la': 'unda',
    }),
    ('field', 'physics', LATTICE, {
        'en': 'field', 'es': 'campo', 'fr': 'champ', 'de': 'Feld',
        'it': 'campo', 'pt': 'campo', 'ru': 'поле', 'ar': 'حقل',
        'he': 'שדה', 'zh': 'chang', 'ja': 'ba', 'hi': 'kshetra',
    }),
    ('particle', 'physics', COUNTER, {
        'en': 'particle', 'es': 'particula', 'fr': 'particule',
        'de': 'Teilchen', 'it': 'particella', 'pt': 'particula',
        'ru': 'частица', 'ar': 'جسيم', 'he': 'חלקיק',
        'zh': 'lizi', 'ja': 'ryuushi',
    }),
    ('gravity', 'physics', COLLAPSE, {
        'en': 'gravity', 'es': 'gravedad', 'fr': 'gravite',
        'de': 'Schwerkraft', 'it': 'gravita', 'pt': 'gravidade',
        'ru': 'гравитация', 'ar': 'جاذبية', 'he': 'כבידה',
        'zh': 'yinli', 'ja': 'juryoku', 'hi': 'gurutvakarshan',
    }),
    ('light', 'physics', HARMONY, {
        'en': 'light', 'es': 'luz', 'fr': 'lumiere', 'de': 'Licht',
        'it': 'luce', 'pt': 'luz', 'ru': 'свет', 'ar': 'ضوء',
        'he': 'אור', 'zh': 'guang', 'ja': 'hikari', 'hi': 'prakash',
        'la': 'lux', 'el': 'φως',
    }),
    ('sound', 'physics', BREATH, {
        'en': 'sound', 'es': 'sonido', 'fr': 'son', 'de': 'Klang',
        'it': 'suono', 'pt': 'som', 'ru': 'звук', 'ar': 'صوت',
        'he': 'צליל', 'zh': 'sheng', 'ja': 'oto', 'hi': 'dhvani',
        'la': 'sonus',
    }),
    ('heat', 'physics', CHAOS, {
        'en': 'heat', 'es': 'calor', 'fr': 'chaleur', 'de': 'Hitze',
        'it': 'calore', 'pt': 'calor', 'ru': 'жар', 'ar': 'حرارة',
        'he': 'חום', 'zh': 'wendu', 'ja': 'netsu', 'hi': 'garmi',
        'la': 'calor',
    }),

    # ── MATHEMATICS ───────────────────────────────────────
    ('number', 'math', COUNTER, {
        'en': 'number', 'es': 'numero', 'fr': 'nombre', 'de': 'Zahl',
        'it': 'numero', 'pt': 'numero', 'ru': 'число', 'ar': 'رقم',
        'he': 'מספר', 'zh': 'shu', 'ja': 'kazu', 'hi': 'sankhya',
        'la': 'numerus',
    }),
    ('zero', 'math', VOID, {
        'en': 'zero', 'es': 'cero', 'fr': 'zero', 'de': 'Null',
        'it': 'zero', 'pt': 'zero', 'ru': 'ноль', 'ar': 'صفر',
        'he': 'אפס', 'zh': 'ling', 'ja': 'rei', 'hi': 'shunya',
        'la': 'nihil',
    }),
    ('one', 'math', LATTICE, {
        'en': 'one', 'es': 'uno', 'fr': 'un', 'de': 'eins',
        'it': 'uno', 'pt': 'um', 'ru': 'один', 'ar': 'واحد',
        'he': 'אחד', 'zh': 'yi', 'ja': 'ichi', 'hi': 'ek',
    }),
    ('point', 'math', VOID, {
        'en': 'point', 'es': 'punto', 'fr': 'point', 'de': 'Punkt',
        'it': 'punto', 'pt': 'ponto', 'ru': 'точка', 'ar': 'نقطة',
        'he': 'נקודה', 'zh': 'dian', 'ja': 'ten',
        'la': 'punctum',
    }),
    ('line', 'math', PROGRESS, {
        'en': 'line', 'es': 'linea', 'fr': 'ligne', 'de': 'Linie',
        'it': 'linea', 'pt': 'linha', 'ru': 'линия', 'ar': 'خط',
        'he': 'קו', 'zh': 'xian', 'ja': 'sen',
        'la': 'linea',
    }),
    ('circle', 'math', BREATH, {
        'en': 'circle', 'es': 'circulo', 'fr': 'cercle', 'de': 'Kreis',
        'it': 'cerchio', 'pt': 'circulo', 'ru': 'круг', 'ar': 'دائرة',
        'he': 'עיגול', 'zh': 'yuan', 'ja': 'en',
        'la': 'circulus',
    }),
    ('pattern', 'math', LATTICE, {
        'en': 'pattern', 'es': 'patron', 'fr': 'motif', 'de': 'Muster',
        'it': 'schema', 'pt': 'padrao', 'ru': 'узор', 'ar': 'نمط',
        'he': 'דפוס', 'zh': 'moshi', 'ja': 'pataan',
    }),
    ('function', 'math', PROGRESS, {
        'en': 'function', 'es': 'funcion', 'fr': 'fonction',
        'de': 'Funktion', 'it': 'funzione', 'pt': 'funcao',
        'ru': 'функция', 'ar': 'دالة', 'he': 'פונקציה',
        'zh': 'hanshu', 'ja': 'kansuu',
    }),

    # ── SOCIETY ───────────────────────────────────────────
    ('language', 'society', LATTICE, {
        'en': 'language', 'es': 'idioma', 'fr': 'langue', 'de': 'Sprache',
        'it': 'lingua', 'pt': 'lingua', 'ru': 'язык', 'ar': 'لغة',
        'he': 'שפה', 'zh': 'yuyan', 'ja': 'gengo', 'hi': 'bhasha',
        'la': 'lingua',
    }),
    ('word', 'society', COUNTER, {
        'en': 'word', 'es': 'palabra', 'fr': 'mot', 'de': 'Wort',
        'it': 'parola', 'pt': 'palavra', 'ru': 'слово', 'ar': 'كلمة',
        'he': 'מילה', 'zh': 'ci', 'ja': 'kotoba', 'hi': 'shabd',
        'la': 'verbum',
    }),
    ('name', 'society', LATTICE, {
        'en': 'name', 'es': 'nombre', 'fr': 'nom', 'de': 'Name',
        'it': 'nome', 'pt': 'nome', 'ru': 'имя', 'ar': 'اسم',
        'he': 'שם', 'zh': 'mingzi', 'ja': 'namae', 'hi': 'naam',
        'la': 'nomen',
    }),
    ('person', 'society', BALANCE, {
        'en': 'person', 'es': 'persona', 'fr': 'personne', 'de': 'Person',
        'it': 'persona', 'pt': 'pessoa', 'ru': 'человек', 'ar': 'شخص',
        'he': 'אדם', 'zh': 'ren', 'ja': 'hito', 'hi': 'vyakti',
        'la': 'persona',
    }),
    ('friend', 'society', HARMONY, {
        'en': 'friend', 'es': 'amigo', 'fr': 'ami', 'de': 'Freund',
        'it': 'amico', 'pt': 'amigo', 'ru': 'друг', 'ar': 'صديق',
        'he': 'חבר', 'zh': 'pengyou', 'ja': 'tomodachi', 'hi': 'mitra',
        'la': 'amicus',
    }),
    ('enemy', 'society', COLLAPSE, {
        'en': 'enemy', 'es': 'enemigo', 'fr': 'ennemi', 'de': 'Feind',
        'it': 'nemico', 'pt': 'inimigo', 'ru': 'враг', 'ar': 'عدو',
        'he': 'אויב', 'zh': 'diren', 'ja': 'teki', 'hi': 'shatru',
        'la': 'hostis',
    }),
    ('king', 'society', LATTICE, {
        'en': 'king', 'es': 'rey', 'fr': 'roi', 'de': 'Koenig',
        'it': 're', 'pt': 'rei', 'ru': 'король', 'ar': 'ملك',
        'he': 'מלך', 'zh': 'wang', 'ja': 'ou', 'hi': 'raja',
        'la': 'rex',
    }),
    ('law', 'society', LATTICE, {
        'en': 'law', 'es': 'ley', 'fr': 'loi', 'de': 'Gesetz',
        'it': 'legge', 'pt': 'lei', 'ru': 'закон', 'ar': 'قانون',
        'he': 'חוק', 'zh': 'falv', 'ja': 'houritsu', 'hi': 'kanoon',
        'la': 'lex',
    }),
    ('freedom', 'society', CHAOS, {
        'en': 'freedom', 'es': 'libertad', 'fr': 'liberte',
        'de': 'Freiheit', 'it': 'liberta', 'pt': 'liberdade',
        'ru': 'свобода', 'ar': 'حرية', 'he': 'חופש',
        'zh': 'ziyou', 'ja': 'jiyuu', 'hi': 'swatantrata',
        'la': 'libertas',
    }),
    ('justice', 'society', BALANCE, {
        'en': 'justice', 'es': 'justicia', 'fr': 'justice',
        'de': 'Gerechtigkeit', 'it': 'giustizia', 'pt': 'justica',
        'ru': 'справедливость', 'ar': 'عدالة', 'he': 'צדק',
        'zh': 'zhengyi', 'ja': 'seigi', 'hi': 'nyay',
        'la': 'iustitia',
    }),
    ('war', 'society', COLLAPSE, {
        'en': 'war', 'es': 'guerra', 'fr': 'guerre', 'de': 'Krieg',
        'it': 'guerra', 'pt': 'guerra', 'ru': 'война', 'ar': 'حرب',
        'he': 'מלחמה', 'zh': 'zhanzheng', 'ja': 'sensou', 'hi': 'yuddh',
        'la': 'bellum',
    }),

    # ── KNOWLEDGE ─────────────────────────────────────────
    ('knowledge', 'knowledge', COUNTER, {
        'en': 'knowledge', 'es': 'conocimiento', 'fr': 'connaissance',
        'de': 'Wissen', 'it': 'conoscenza', 'pt': 'conhecimento',
        'ru': 'знание', 'ar': 'معرفة', 'he': 'דעת', 'zh': 'zhishi',
        'ja': 'chishiki', 'hi': 'gyan', 'la': 'scientia',
    }),
    ('wisdom', 'knowledge', HARMONY, {
        'en': 'wisdom', 'es': 'sabiduria', 'fr': 'sagesse',
        'de': 'Weisheit', 'it': 'saggezza', 'pt': 'sabedoria',
        'ru': 'мудрость', 'ar': 'حكمة', 'he': 'חכמה',
        'zh': 'zhihui', 'ja': 'chie', 'hi': 'pragya',
        'la': 'sapientia',
    }),
    ('question', 'knowledge', COUNTER, {
        'en': 'question', 'es': 'pregunta', 'fr': 'question',
        'de': 'Frage', 'it': 'domanda', 'pt': 'pergunta',
        'ru': 'вопрос', 'ar': 'سؤال', 'he': 'שאלה',
        'zh': 'wenti', 'ja': 'shitsumon', 'hi': 'prashna',
    }),
    ('answer', 'knowledge', HARMONY, {
        'en': 'answer', 'es': 'respuesta', 'fr': 'reponse',
        'de': 'Antwort', 'it': 'risposta', 'pt': 'resposta',
        'ru': 'ответ', 'ar': 'جواب', 'he': 'תשובה',
        'zh': 'daan', 'ja': 'kotae', 'hi': 'uttar',
    }),
    ('book', 'knowledge', LATTICE, {
        'en': 'book', 'es': 'libro', 'fr': 'livre', 'de': 'Buch',
        'it': 'libro', 'pt': 'livro', 'ru': 'книга', 'ar': 'كتاب',
        'he': 'ספר', 'zh': 'shu', 'ja': 'hon', 'hi': 'kitab',
        'la': 'liber',
    }),
    ('thought', 'knowledge', COUNTER, {
        'en': 'thought', 'es': 'pensamiento', 'fr': 'pensee',
        'de': 'Gedanke', 'it': 'pensiero', 'pt': 'pensamento',
        'ru': 'мысль', 'ar': 'فكرة', 'he': 'מחשבה',
        'zh': 'sixiang', 'ja': 'shisou', 'hi': 'vichar',
    }),
    ('dream', 'knowledge', CHAOS, {
        'en': 'dream', 'es': 'sueno', 'fr': 'reve', 'de': 'Traum',
        'it': 'sogno', 'pt': 'sonho', 'ru': 'мечта', 'ar': 'حلم',
        'he': 'חלום', 'zh': 'meng', 'ja': 'yume', 'hi': 'sapna',
        'la': 'somnium',
    }),
    ('memory', 'knowledge', COUNTER, {
        'en': 'memory', 'es': 'memoria', 'fr': 'memoire',
        'de': 'Erinnerung', 'it': 'memoria', 'pt': 'memoria',
        'ru': 'память', 'ar': 'ذاكرة', 'he': 'זיכרון',
        'zh': 'jiyi', 'ja': 'kioku', 'hi': 'smriti',
    }),

    # ── ACTIONS ───────────────────────────────────────────
    ('movement', 'action', PROGRESS, {
        'en': 'movement', 'es': 'movimiento', 'fr': 'mouvement',
        'de': 'Bewegung', 'it': 'movimento', 'pt': 'movimento',
        'ru': 'движение', 'ar': 'حركة', 'he': 'תנועה',
        'zh': 'yundong', 'ja': 'undou', 'hi': 'gati',
    }),
    ('creation', 'action', CHAOS, {
        'en': 'creation', 'es': 'creacion', 'fr': 'creation',
        'de': 'Schoepfung', 'it': 'creazione', 'pt': 'criacao',
        'ru': 'творение', 'ar': 'خلق', 'he': 'בריאה',
        'zh': 'chuangzao', 'ja': 'souzou', 'hi': 'sristi',
    }),
    ('destruction', 'action', COLLAPSE, {
        'en': 'destruction', 'es': 'destruccion', 'fr': 'destruction',
        'de': 'Zerstoerung', 'it': 'distruzione', 'pt': 'destruicao',
        'ru': 'разрушение', 'ar': 'تدمير', 'he': 'הרס',
        'zh': 'pohuai', 'ja': 'hakai', 'hi': 'vinash',
    }),
    ('sleep', 'action', RESET, {
        'en': 'sleep', 'es': 'dormir', 'fr': 'sommeil', 'de': 'Schlaf',
        'it': 'sonno', 'pt': 'sono', 'ru': 'сон', 'ar': 'نوم',
        'he': 'שינה', 'zh': 'shuimian', 'ja': 'suimin', 'hi': 'nidra',
        'la': 'somnus',
    }),
    ('eating', 'action', PROGRESS, {
        'en': 'eating', 'es': 'comer', 'fr': 'manger', 'de': 'Essen',
        'it': 'mangiare', 'pt': 'comer', 'ru': 'еда', 'ar': 'أكل',
        'he': 'אכילה', 'zh': 'chi', 'ja': 'taberu', 'hi': 'khana',
    }),
    ('giving', 'action', HARMONY, {
        'en': 'giving', 'es': 'dar', 'fr': 'donner', 'de': 'Geben',
        'it': 'dare', 'pt': 'dar', 'ru': 'давание', 'ar': 'عطاء',
        'he': 'נתינה', 'zh': 'geiyu', 'ja': 'ataeru', 'hi': 'dena',
    }),
    ('speaking', 'action', LATTICE, {
        'en': 'speaking', 'es': 'hablar', 'fr': 'parler', 'de': 'Sprechen',
        'it': 'parlare', 'pt': 'falar', 'ru': 'речь', 'ar': 'كلام',
        'he': 'דיבור', 'zh': 'shuohua', 'ja': 'hanasu', 'hi': 'bolna',
    }),
    ('listening', 'action', COUNTER, {
        'en': 'listening', 'es': 'escuchar', 'fr': 'ecouter',
        'de': 'Zuhoeren', 'it': 'ascoltare', 'pt': 'ouvir',
        'ru': 'слушание', 'ar': 'استماع', 'he': 'הקשבה',
        'zh': 'ting', 'ja': 'kiku', 'hi': 'sunna',
    }),
    ('teaching', 'action', PROGRESS, {
        'en': 'teaching', 'es': 'ensenar', 'fr': 'enseigner',
        'de': 'Lehren', 'it': 'insegnare', 'pt': 'ensinar',
        'ru': 'обучение', 'ar': 'تعليم', 'he': 'הוראה',
        'zh': 'jiaoxue', 'ja': 'oshieru', 'hi': 'sikhana',
    }),
    ('learning', 'action', COUNTER, {
        'en': 'learning', 'es': 'aprender', 'fr': 'apprendre',
        'de': 'Lernen', 'it': 'imparare', 'pt': 'aprender',
        'ru': 'учение', 'ar': 'تعلم', 'he': 'למידה',
        'zh': 'xuexi', 'ja': 'manabu', 'hi': 'sikhna',
    }),

    # ── TECHNOLOGY ────────────────────────────────────────
    ('machine', 'technology', LATTICE, {
        'en': 'machine', 'es': 'maquina', 'fr': 'machine',
        'de': 'Maschine', 'it': 'macchina', 'pt': 'maquina',
        'ru': 'машина', 'ar': 'آلة', 'he': 'מכונה',
        'zh': 'jiqi', 'ja': 'kikai', 'hi': 'yantra',
    }),
    ('computer', 'technology', COUNTER, {
        'en': 'computer', 'es': 'computadora', 'fr': 'ordinateur',
        'de': 'Computer', 'it': 'computer', 'pt': 'computador',
        'ru': 'компьютер', 'ar': 'حاسوب', 'he': 'מחשב',
        'zh': 'diannao', 'ja': 'konpyuutaa', 'hi': 'sanganak',
    }),
    ('code', 'technology', LATTICE, {
        'en': 'code', 'es': 'codigo', 'fr': 'code', 'de': 'Code',
        'it': 'codice', 'pt': 'codigo', 'ru': 'код', 'ar': 'رمز',
        'he': 'קוד', 'zh': 'daima', 'ja': 'koodo',
    }),
    ('network', 'technology', LATTICE, {
        'en': 'network', 'es': 'red', 'fr': 'reseau', 'de': 'Netzwerk',
        'it': 'rete', 'pt': 'rede', 'ru': 'сеть', 'ar': 'شبكة',
        'he': 'רשת', 'zh': 'wangluo', 'ja': 'nettwaaku',
    }),
    ('signal', 'technology', COUNTER, {
        'en': 'signal', 'es': 'senal', 'fr': 'signal', 'de': 'Signal',
        'it': 'segnale', 'pt': 'sinal', 'ru': 'сигнал', 'ar': 'إشارة',
        'he': 'אות', 'zh': 'xinhao', 'ja': 'shingou',
    }),

    # ── MUSIC & ART ───────────────────────────────────────
    ('music', 'art', HARMONY, {
        'en': 'music', 'es': 'musica', 'fr': 'musique', 'de': 'Musik',
        'it': 'musica', 'pt': 'musica', 'ru': 'музыка', 'ar': 'موسيقى',
        'he': 'מוזיקה', 'zh': 'yinyue', 'ja': 'ongaku', 'hi': 'sangeet',
        'la': 'musica',
    }),
    ('rhythm', 'art', BREATH, {
        'en': 'rhythm', 'es': 'ritmo', 'fr': 'rythme', 'de': 'Rhythmus',
        'it': 'ritmo', 'pt': 'ritmo', 'ru': 'ритм', 'ar': 'إيقاع',
        'he': 'קצב', 'zh': 'jiezou', 'ja': 'rizumu',
    }),
    ('color', 'art', CHAOS, {
        'en': 'color', 'es': 'color', 'fr': 'couleur', 'de': 'Farbe',
        'it': 'colore', 'pt': 'cor', 'ru': 'цвет', 'ar': 'لون',
        'he': 'צבע', 'zh': 'yanse', 'ja': 'iro', 'hi': 'rang',
        'la': 'color',
    }),
    ('beauty', 'art', HARMONY, {
        'en': 'beauty', 'es': 'belleza', 'fr': 'beaute', 'de': 'Schoenheit',
        'it': 'bellezza', 'pt': 'beleza', 'ru': 'красота', 'ar': 'جمال',
        'he': 'יופי', 'zh': 'mei', 'ja': 'bi', 'hi': 'sundarta',
        'la': 'pulchritudo',
    }),
    ('song', 'art', HARMONY, {
        'en': 'song', 'es': 'cancion', 'fr': 'chanson', 'de': 'Lied',
        'it': 'canzone', 'pt': 'cancao', 'ru': 'песня', 'ar': 'أغنية',
        'he': 'שיר', 'zh': 'ge', 'ja': 'uta', 'hi': 'geet',
    }),
    ('dance', 'art', BREATH, {
        'en': 'dance', 'es': 'danza', 'fr': 'danse', 'de': 'Tanz',
        'it': 'danza', 'pt': 'danca', 'ru': 'танец', 'ar': 'رقص',
        'he': 'ריקוד', 'zh': 'wudao', 'ja': 'odori', 'hi': 'nritya',
    }),
    ('story', 'art', PROGRESS, {
        'en': 'story', 'es': 'historia', 'fr': 'histoire', 'de': 'Geschichte',
        'it': 'storia', 'pt': 'historia', 'ru': 'рассказ', 'ar': 'قصة',
        'he': 'סיפור', 'zh': 'gushi', 'ja': 'monogatari', 'hi': 'kahani',
    }),

    # ── FOOD & SUSTENANCE ─────────────────────────────────
    ('food', 'sustenance', PROGRESS, {
        'en': 'food', 'es': 'comida', 'fr': 'nourriture', 'de': 'Essen',
        'it': 'cibo', 'pt': 'comida', 'ru': 'еда', 'ar': 'طعام',
        'he': 'אוכל', 'zh': 'shiwu', 'ja': 'tabemono', 'hi': 'bhojan',
    }),
    ('bread', 'sustenance', LATTICE, {
        'en': 'bread', 'es': 'pan', 'fr': 'pain', 'de': 'Brot',
        'it': 'pane', 'pt': 'pao', 'ru': 'хлеб', 'ar': 'خبز',
        'he': 'לחם', 'zh': 'mianbao', 'ja': 'pan', 'hi': 'roti',
        'la': 'panis',
    }),
    ('salt', 'sustenance', BALANCE, {
        'en': 'salt', 'es': 'sal', 'fr': 'sel', 'de': 'Salz',
        'it': 'sale', 'pt': 'sal', 'ru': 'соль', 'ar': 'ملح',
        'he': 'מלח', 'zh': 'yan', 'ja': 'shio', 'hi': 'namak',
        'la': 'sal',
    }),

    # ── SPIRITUALITY ──────────────────────────────────────
    ('soul', 'spirit', HARMONY, {
        'en': 'soul', 'es': 'alma', 'fr': 'ame', 'de': 'Seele',
        'it': 'anima', 'pt': 'alma', 'ru': 'душа', 'ar': 'روح',
        'he': 'נשמה', 'zh': 'linghun', 'ja': 'tamashii', 'hi': 'atma',
        'la': 'anima', 'el': 'ψυχή',
    }),
    ('god', 'spirit', HARMONY, {
        'en': 'god', 'es': 'dios', 'fr': 'dieu', 'de': 'Gott',
        'it': 'dio', 'pt': 'deus', 'ru': 'бог', 'ar': 'إله',
        'he': 'אלוהים', 'zh': 'shen', 'ja': 'kami', 'hi': 'ishvar',
        'la': 'deus', 'el': 'θεός',
    }),
    ('prayer', 'spirit', BREATH, {
        'en': 'prayer', 'es': 'oracion', 'fr': 'priere', 'de': 'Gebet',
        'it': 'preghiera', 'pt': 'oracao', 'ru': 'молитва',
        'ar': 'صلاة', 'he': 'תפילה', 'zh': 'qidao', 'ja': 'inori',
        'hi': 'prarthana',
    }),

    # ── SPATIAL ───────────────────────────────────────────
    ('door', 'spatial', PROGRESS, {
        'en': 'door', 'es': 'puerta', 'fr': 'porte', 'de': 'Tuer',
        'it': 'porta', 'pt': 'porta', 'ru': 'дверь', 'ar': 'باب',
        'he': 'דלת', 'zh': 'men', 'ja': 'tobira', 'hi': 'darwaza',
        'la': 'porta',
    }),
    ('path', 'spatial', PROGRESS, {
        'en': 'path', 'es': 'camino', 'fr': 'chemin', 'de': 'Weg',
        'it': 'sentiero', 'pt': 'caminho', 'ru': 'путь', 'ar': 'مسار',
        'he': 'דרך', 'zh': 'lu', 'ja': 'michi', 'hi': 'raasta',
        'la': 'via',
    }),
    ('bridge', 'spatial', BALANCE, {
        'en': 'bridge', 'es': 'puente', 'fr': 'pont', 'de': 'Bruecke',
        'it': 'ponte', 'pt': 'ponte', 'ru': 'мост', 'ar': 'جسر',
        'he': 'גשר', 'zh': 'qiao', 'ja': 'hashi', 'hi': 'pul',
    }),
    ('wall', 'spatial', COLLAPSE, {
        'en': 'wall', 'es': 'muro', 'fr': 'mur', 'de': 'Mauer',
        'it': 'muro', 'pt': 'muro', 'ru': 'стена', 'ar': 'جدار',
        'he': 'קיר', 'zh': 'qiang', 'ja': 'kabe', 'hi': 'deevar',
        'la': 'murus',
    }),

    # ── ANIMALS ───────────────────────────────────────────
    ('animal', 'biology', BREATH, {
        'en': 'animal', 'es': 'animal', 'fr': 'animal', 'de': 'Tier',
        'it': 'animale', 'pt': 'animal', 'ru': 'животное',
        'ar': 'حيوان', 'he': 'חיה', 'zh': 'dongwu', 'ja': 'doubutsu',
        'hi': 'janwar', 'la': 'animal',
    }),
    ('dog', 'biology', HARMONY, {
        'en': 'dog', 'es': 'perro', 'fr': 'chien', 'de': 'Hund',
        'it': 'cane', 'pt': 'cao', 'ru': 'собака', 'ar': 'كلب',
        'he': 'כלב', 'zh': 'gou', 'ja': 'inu', 'hi': 'kutta',
        'la': 'canis',
    }),
    ('bird', 'biology', BREATH, {
        'en': 'bird', 'es': 'pajaro', 'fr': 'oiseau', 'de': 'Vogel',
        'it': 'uccello', 'pt': 'passaro', 'ru': 'птица', 'ar': 'طائر',
        'he': 'ציפור', 'zh': 'niao', 'ja': 'tori', 'hi': 'pakshi',
        'la': 'avis',
    }),
    ('fish', 'biology', BREATH, {
        'en': 'fish', 'es': 'pez', 'fr': 'poisson', 'de': 'Fisch',
        'it': 'pesce', 'pt': 'peixe', 'ru': 'рыба', 'ar': 'سمك',
        'he': 'דג', 'zh': 'yu', 'ja': 'sakana', 'hi': 'machhli',
        'la': 'piscis',
    }),
    ('horse', 'biology', PROGRESS, {
        'en': 'horse', 'es': 'caballo', 'fr': 'cheval', 'de': 'Pferd',
        'it': 'cavallo', 'pt': 'cavalo', 'ru': 'лошадь', 'ar': 'حصان',
        'he': 'סוס', 'zh': 'ma', 'ja': 'uma', 'hi': 'ghoda',
        'la': 'equus',
    }),

    # ── WEATHER & CLIMATE ─────────────────────────────────
    ('rain', 'weather', COLLAPSE, {
        'en': 'rain', 'es': 'lluvia', 'fr': 'pluie', 'de': 'Regen',
        'it': 'pioggia', 'pt': 'chuva', 'ru': 'дождь', 'ar': 'مطر',
        'he': 'גשם', 'zh': 'yu', 'ja': 'ame', 'hi': 'baarish',
        'la': 'pluvia',
    }),
    ('wind', 'weather', CHAOS, {
        'en': 'wind', 'es': 'viento', 'fr': 'vent', 'de': 'Wind',
        'it': 'vento', 'pt': 'vento', 'ru': 'ветер', 'ar': 'ريح',
        'he': 'רוח', 'zh': 'feng', 'ja': 'kaze', 'hi': 'hawa',
        'la': 'ventus',
    }),
    ('snow', 'weather', RESET, {
        'en': 'snow', 'es': 'nieve', 'fr': 'neige', 'de': 'Schnee',
        'it': 'neve', 'pt': 'neve', 'ru': 'снег', 'ar': 'ثلج',
        'he': 'שלג', 'zh': 'xue', 'ja': 'yuki', 'hi': 'barf',
        'la': 'nix',
    }),

    # == LOCOMOTION & MOVEMENT ==================================
    ('walk', 'locomotion', PROGRESS, {
        'en': 'walk', 'es': 'caminar', 'fr': 'marcher', 'de': 'gehen',
        'it': 'camminare', 'pt': 'andar', 'ru': 'ходить', 'ar': 'يمشي',
        'he': 'ללכת', 'zh': 'zou', 'ja': 'aruku', 'hi': 'chalna',
    }),
    ('run', 'locomotion', CHAOS, {
        'en': 'run', 'es': 'correr', 'fr': 'courir', 'de': 'laufen',
        'it': 'correre', 'pt': 'correr', 'ru': 'бежать', 'ar': 'يركض',
        'he': 'לרוץ', 'zh': 'pao', 'ja': 'hashiru', 'hi': 'daudna',
    }),
    ('stand', 'locomotion', LATTICE, {
        'en': 'stand', 'es': 'estar', 'fr': 'debout', 'de': 'stehen',
        'it': 'stare', 'pt': 'ficar', 'ru': 'стоять', 'ar': 'يقف',
        'he': 'לעמוד', 'zh': 'zhan', 'ja': 'tatsu', 'hi': 'khada',
    }),
    ('step', 'locomotion', PROGRESS, {
        'en': 'step', 'es': 'paso', 'fr': 'pas', 'de': 'Schritt',
        'it': 'passo', 'pt': 'passo', 'ru': 'шаг', 'ar': 'خطوة',
        'he': 'צעד', 'zh': 'bu', 'ja': 'ippo', 'hi': 'kadam',
    }),
    ('fall', 'locomotion', COLLAPSE, {
        'en': 'fall', 'es': 'caer', 'fr': 'tomber', 'de': 'fallen',
        'it': 'cadere', 'pt': 'cair', 'ru': 'падать', 'ar': 'يسقط',
        'he': 'ליפול', 'zh': 'luo', 'ja': 'ochiru', 'hi': 'girna',
    }),
    ('turn', 'locomotion', RESET, {
        'en': 'turn', 'es': 'girar', 'fr': 'tourner', 'de': 'drehen',
        'it': 'girare', 'pt': 'virar', 'ru': 'поворот', 'ar': 'يدور',
        'he': 'לפנות', 'zh': 'zhuan', 'ja': 'mawaru', 'hi': 'mudna',
    }),
    ('climb', 'locomotion', PROGRESS, {
        'en': 'climb', 'es': 'escalar', 'fr': 'grimper', 'de': 'klettern',
        'it': 'arrampicare', 'pt': 'escalar', 'ru': 'лезть',
        'he': 'לטפס', 'zh': 'pan', 'ja': 'noboru', 'hi': 'chadhna',
    }),
    ('gait', 'locomotion', BREATH, {
        'en': 'gait', 'es': 'marcha', 'fr': 'allure', 'de': 'Gang',
        'it': 'andatura', 'pt': 'marcha', 'ru': 'походка',
        'he': 'הליכה', 'zh': 'butai', 'ja': 'hokouhou',
    }),

    # == SPATIAL AWARENESS ======================================
    ('obstacle', 'spatial', COLLAPSE, {
        'en': 'obstacle', 'es': 'obstaculo', 'fr': 'obstacle',
        'de': 'Hindernis', 'it': 'ostacolo', 'pt': 'obstaculo',
        'ru': 'препятствие', 'ar': 'عقبة', 'he': 'מכשול',
        'zh': 'zhangai', 'ja': 'shougai', 'hi': 'rukawat',
    }),
    ('distance', 'spatial', COUNTER, {
        'en': 'distance', 'es': 'distancia', 'fr': 'distance',
        'de': 'Entfernung', 'it': 'distanza', 'pt': 'distancia',
        'ru': 'расстояние', 'ar': 'مسافة', 'he': 'מרחק',
        'zh': 'juli', 'ja': 'kyori', 'hi': 'doori',
    }),
    ('direction', 'spatial', LATTICE, {
        'en': 'direction', 'es': 'direccion', 'fr': 'direction',
        'de': 'Richtung', 'it': 'direzione', 'pt': 'direcao',
        'ru': 'направление', 'ar': 'اتجاه', 'he': 'כיוון',
        'zh': 'fangxiang', 'ja': 'houkou', 'hi': 'disha',
    }),
    ('ground', 'spatial', LATTICE, {
        'en': 'ground', 'es': 'suelo', 'fr': 'sol', 'de': 'Boden',
        'it': 'terreno', 'pt': 'chao', 'ru': 'земля', 'ar': 'أرض',
        'he': 'קרקע', 'zh': 'dimian', 'ja': 'jimen', 'hi': 'zameen',
        'la': 'terra',
    }),
    ('shelter', 'spatial', HARMONY, {
        'en': 'shelter', 'es': 'refugio', 'fr': 'abri', 'de': 'Schutz',
        'it': 'rifugio', 'pt': 'abrigo', 'ru': 'укрытие',
        'he': 'מחסה', 'zh': 'bisuo', 'ja': 'hinanjo',
    }),
    ('boundary', 'spatial', BALANCE, {
        'en': 'boundary', 'es': 'limite', 'fr': 'limite', 'de': 'Grenze',
        'it': 'confine', 'pt': 'limite', 'ru': 'граница', 'ar': 'حدود',
        'he': 'גבול', 'zh': 'bianjie', 'ja': 'kyoukai', 'hi': 'seema',
    }),

    # == PROPRIOCEPTION & SENSING ===============================
    ('touch', 'sensing', COUNTER, {
        'en': 'touch', 'es': 'tocar', 'fr': 'toucher', 'de': 'Beruehrung',
        'it': 'tocco', 'pt': 'toque', 'ru': 'прикосновение',
        'ar': 'لمس', 'he': 'מגע', 'zh': 'chumo', 'ja': 'sesshoku',
        'hi': 'sparsh',
    }),
    ('pain', 'sensing', COLLAPSE, {
        'en': 'pain', 'es': 'dolor', 'fr': 'douleur', 'de': 'Schmerz',
        'it': 'dolore', 'pt': 'dor', 'ru': 'боль', 'ar': 'ألم',
        'he': 'כאב', 'zh': 'tong', 'ja': 'itami', 'hi': 'dard',
        'la': 'dolor',
    }),
    ('warmth', 'sensing', HARMONY, {
        'en': 'warmth', 'es': 'calidez', 'fr': 'chaleur', 'de': 'Waerme',
        'it': 'calore', 'pt': 'calor', 'ru': 'тепло', 'ar': 'دفء',
        'he': 'חום', 'zh': 'wennuan', 'ja': 'nukumori', 'hi': 'garmi',
    }),
    ('cold_sense', 'sensing', VOID, {
        'en': 'cold', 'es': 'frio', 'fr': 'froid', 'de': 'Kaelte',
        'it': 'freddo', 'pt': 'frio', 'ru': 'холод', 'ar': 'برد',
        'he': 'קור', 'zh': 'leng', 'ja': 'samusa', 'hi': 'thanda',
    }),
    ('vibration', 'sensing', CHAOS, {
        'en': 'vibration', 'es': 'vibracion', 'fr': 'vibration',
        'de': 'Vibration', 'it': 'vibrazione', 'pt': 'vibracao',
        'ru': 'вибрация', 'he': 'רטט', 'zh': 'zhendong',
        'ja': 'shindou', 'hi': 'kampan',
    }),

    # == ROBOT BODY =============================================
    ('leg', 'robot', PROGRESS, {
        'en': 'leg', 'es': 'pierna', 'fr': 'jambe', 'de': 'Bein',
        'it': 'gamba', 'pt': 'perna', 'ru': 'нога', 'ar': 'ساق',
        'he': 'רגל', 'zh': 'tui', 'ja': 'ashi', 'hi': 'pair',
    }),
    ('joint', 'robot', BALANCE, {
        'en': 'joint', 'es': 'articulacion', 'fr': 'articulation',
        'de': 'Gelenk', 'it': 'giuntura', 'pt': 'articulacao',
        'ru': 'сустав', 'he': 'מפרק', 'zh': 'guanjie', 'ja': 'kansetsu',
    }),
    ('motor', 'robot', PROGRESS, {
        'en': 'motor', 'es': 'motor', 'fr': 'moteur', 'de': 'Motor',
        'it': 'motore', 'pt': 'motor', 'ru': 'мотор',
        'he': 'מנוע', 'zh': 'fadongji', 'ja': 'mootaa',
    }),
    ('sensor', 'robot', COUNTER, {
        'en': 'sensor', 'es': 'sensor', 'fr': 'capteur', 'de': 'Sensor',
        'it': 'sensore', 'pt': 'sensor', 'ru': 'датчик',
        'he': 'חיישן', 'zh': 'chuanganqi', 'ja': 'sensaa',
    }),
    ('battery', 'robot', BREATH, {
        'en': 'battery', 'es': 'bateria', 'fr': 'batterie',
        'de': 'Batterie', 'it': 'batteria', 'pt': 'bateria',
        'ru': 'аккумулятор', 'he': 'סוללה', 'zh': 'dianchi',
        'ja': 'denchi', 'hi': 'battery',
    }),
    ('dock', 'robot', HARMONY, {
        'en': 'dock', 'es': 'estacion', 'fr': 'station', 'de': 'Station',
        'it': 'stazione', 'pt': 'estacao', 'ru': 'станция',
        'he': 'תחנה', 'zh': 'jizhan', 'ja': 'suteshon',
    }),
    ('circuit', 'robot', LATTICE, {
        'en': 'circuit', 'es': 'circuito', 'fr': 'circuit',
        'de': 'Schaltung', 'it': 'circuito', 'pt': 'circuito',
        'ru': 'схема', 'he': 'מעגל', 'zh': 'dianlu', 'ja': 'kairo',
    }),

    # == SURVIVAL & ENERGY ======================================
    ('rest_survival', 'survival', COLLAPSE, {
        'en': 'rest', 'es': 'descanso', 'fr': 'repos', 'de': 'Ruhe',
        'it': 'riposo', 'pt': 'descanso', 'ru': 'отдых', 'ar': 'راحة',
        'he': 'מנוחה', 'zh': 'xiuxi', 'ja': 'kyuusoku', 'hi': 'aaram',
    }),
    ('hunger', 'survival', COLLAPSE, {
        'en': 'hunger', 'es': 'hambre', 'fr': 'faim', 'de': 'Hunger',
        'it': 'fame', 'pt': 'fome', 'ru': 'голод', 'ar': 'جوع',
        'he': 'רעב', 'zh': 'ji', 'ja': 'kufuku', 'hi': 'bhookh',
        'la': 'fames',
    }),
    ('safety', 'survival', HARMONY, {
        'en': 'safety', 'es': 'seguridad', 'fr': 'securite',
        'de': 'Sicherheit', 'it': 'sicurezza', 'pt': 'seguranca',
        'ru': 'безопасность', 'ar': 'أمان', 'he': 'בטיחות',
        'zh': 'anquan', 'ja': 'anzen', 'hi': 'suraksha',
    }),
    ('danger', 'survival', COLLAPSE, {
        'en': 'danger', 'es': 'peligro', 'fr': 'danger', 'de': 'Gefahr',
        'it': 'pericolo', 'pt': 'perigo', 'ru': 'опасность', 'ar': 'خطر',
        'he': 'סכנה', 'zh': 'weixian', 'ja': 'kiken', 'hi': 'khatra',
    }),
    ('explore_concept', 'survival', COUNTER, {
        'en': 'explore', 'es': 'explorar', 'fr': 'explorer',
        'de': 'erkunden', 'it': 'esplorare', 'pt': 'explorar',
        'ru': 'исследовать', 'he': 'לחקור', 'zh': 'tansuo',
        'ja': 'tanken', 'hi': 'khojana',
    }),
    ('return_concept', 'survival', RESET, {
        'en': 'return', 'es': 'volver', 'fr': 'retour', 'de': 'Rueckkehr',
        'it': 'ritorno', 'pt': 'retorno', 'ru': 'возвращение',
        'he': 'חזרה', 'zh': 'fanhui', 'ja': 'kikan', 'hi': 'vapasi',
    }),
]


# ================================================================
#  CORE RELATIONS: How Concepts Connect
# ================================================================

CORE_RELATIONS = [
    # Existence
    ('existence', 'opposes', 'void'),
    ('order', 'opposes', 'chaos_concept'),
    ('balance_concept', 'harmonizes', 'order'),
    ('time', 'sustains', 'change'),
    ('space', 'contains', 'existence'),
    ('infinity', 'contains', 'time'),
    ('infinity', 'contains', 'space'),
    ('truth', 'harmonizes', 'existence'),

    # Family
    ('mother', 'sustains', 'child'),
    ('father', 'sustains', 'child'),
    ('child', 'part_of', 'home'),
    ('love', 'harmonizes', 'home'),
    ('brother', 'balances', 'sister'),
    ('mother', 'harmonizes', 'love'),

    # Body
    ('heart', 'sustains', 'body'),
    ('blood', 'sustains', 'body'),
    ('breath_concept', 'sustains', 'life'),
    ('mind', 'part_of', 'body'),
    ('eye', 'part_of', 'body'),
    ('hand', 'part_of', 'body'),

    # Nature
    ('sun', 'sustains', 'life'),
    ('water', 'sustains', 'life'),
    ('fire', 'opposes', 'water'),
    ('earth_element', 'sustains', 'tree'),
    ('river', 'part_of', 'earth_element'),
    ('ocean', 'contains', 'water'),
    ('mountain', 'part_of', 'earth_element'),
    ('seed', 'causes', 'growth'),
    ('moon', 'balances', 'sun'),

    # Life cycle
    ('birth', 'precedes', 'life'),
    ('life', 'precedes', 'death'),
    ('death', 'resets', 'birth'),
    ('growth', 'sustains', 'life'),
    ('cell', 'part_of', 'body'),
    ('dna', 'sustains', 'cell'),

    # Emotion
    ('joy', 'opposes', 'sorrow'),
    ('fear', 'opposes', 'courage'),
    ('peace', 'harmonizes', 'balance_concept'),
    ('hope', 'sustains', 'courage'),
    ('anger', 'opposes', 'peace'),

    # Physics
    ('energy', 'causes', 'movement'),
    ('force', 'causes', 'change'),
    ('wave', 'sustains', 'sound'),
    ('light', 'opposes', 'void'),
    ('gravity', 'causes', 'destruction'),
    ('heat', 'causes', 'change'),
    ('field', 'contains', 'particle'),
    ('wave', 'harmonizes', 'particle'),

    # Math
    ('zero', 'precedes', 'one'),
    ('point', 'precedes', 'line'),
    ('line', 'precedes', 'circle'),
    ('pattern', 'contains', 'number'),
    ('function', 'transforms', 'number'),

    # Society
    ('language', 'contains', 'word'),
    ('word', 'enables', 'speaking'),
    ('speaking', 'balances', 'listening'),
    ('teaching', 'balances', 'learning'),
    ('person', 'has', 'name'),
    ('friend', 'opposes', 'enemy'),
    ('law', 'enables', 'justice'),
    ('freedom', 'opposes', 'wall'),
    ('war', 'opposes', 'peace'),
    ('king', 'enables', 'law'),

    # Knowledge
    ('question', 'precedes', 'answer'),
    ('knowledge', 'enables', 'wisdom'),
    ('thought', 'causes', 'knowledge'),
    ('memory', 'sustains', 'knowledge'),
    ('dream', 'causes', 'creation'),
    ('book', 'contains', 'knowledge'),

    # Action
    ('creation', 'opposes', 'destruction'),
    ('sleep', 'resets', 'mind'),
    ('eating', 'sustains', 'body'),
    ('giving', 'harmonizes', 'love'),

    # Technology
    ('machine', 'enables', 'creation'),
    ('computer', 'is_a', 'machine'),
    ('code', 'enables', 'computer'),
    ('network', 'contains', 'signal'),

    # Art
    ('music', 'harmonizes', 'rhythm'),
    ('beauty', 'harmonizes', 'truth'),
    ('song', 'is_a', 'music'),
    ('dance', 'harmonizes', 'rhythm'),
    ('story', 'contains', 'memory'),
    ('color', 'enables', 'beauty'),

    # Sustenance
    ('food', 'sustains', 'body'),
    ('bread', 'is_a', 'food'),

    # Spirit
    ('soul', 'sustains', 'life'),
    ('prayer', 'harmonizes', 'soul'),

    # Spatial
    ('door', 'enables', 'path'),
    ('bridge', 'enables', 'path'),
    ('wall', 'prevents', 'path'),

    # Animals
    ('dog', 'is_a', 'animal'),
    ('bird', 'is_a', 'animal'),
    ('fish', 'is_a', 'animal'),
    ('horse', 'is_a', 'animal'),
    ('animal', 'sustains', 'life'),

    # Weather
    ('rain', 'sustains', 'earth_element'),
    ('wind', 'causes', 'movement'),
    ('snow', 'resets', 'earth_element'),

    # Locomotion
    ('walk', 'causes', 'step'),
    ('run', 'causes', 'step'),
    ('gait', 'contains', 'walk'),
    ('gait', 'contains', 'run'),
    ('gait', 'contains', 'stand'),
    ('step', 'precedes', 'step'),
    ('fall', 'opposes', 'stand'),
    ('turn', 'causes', 'direction'),
    ('climb', 'opposes', 'fall'),
    ('walk', 'enables', 'path'),
    ('stand', 'precedes', 'walk'),
    ('leg', 'enables', 'walk'),
    ('leg', 'enables', 'run'),
    ('leg', 'enables', 'stand'),

    # Spatial awareness
    ('obstacle', 'opposes', 'path'),
    ('obstacle', 'causes', 'turn'),
    ('obstacle', 'causes', 'danger'),
    ('path', 'contains', 'distance'),
    ('path', 'contains', 'direction'),
    ('ground', 'sustains', 'stand'),
    ('ground', 'sustains', 'walk'),
    ('shelter', 'opposes', 'danger'),
    ('boundary', 'prevents', 'path'),
    ('boundary', 'causes', 'turn'),
    ('distance', 'part_of', 'path'),
    ('direction', 'enables', 'path'),

    # Proprioception and sensing
    ('touch', 'enables', 'obstacle'),
    ('pain', 'causes', 'danger'),
    ('warmth', 'harmonizes', 'safety'),
    ('cold_sense', 'opposes', 'warmth'),
    ('vibration', 'enables', 'touch'),
    ('gravity', 'sustains', 'ground'),
    ('gravity', 'causes', 'fall'),
    ('sensor', 'enables', 'touch'),
    ('sensor', 'enables', 'distance'),

    # Robot body
    ('leg', 'contains', 'joint'),
    ('joint', 'contains', 'motor'),
    ('motor', 'enables', 'leg'),
    ('sensor', 'part_of', 'body'),
    ('battery', 'sustains', 'motor'),
    ('battery', 'sustains', 'circuit'),
    ('dock', 'sustains', 'battery'),
    ('circuit', 'contains', 'signal'),
    ('signal', 'enables', 'motor'),
    ('circuit', 'enables', 'sensor'),
    ('leg', 'part_of', 'body'),

    # Survival and energy
    ('energy', 'sustains', 'movement'),
    ('energy', 'sustains', 'life'),
    ('rest_survival', 'causes', 'energy'),
    ('hunger', 'opposes', 'energy'),
    ('safety', 'opposes', 'danger'),
    ('danger', 'causes', 'rest_survival'),
    ('explore_concept', 'causes', 'path'),
    ('explore_concept', 'opposes', 'rest_survival'),
    ('return_concept', 'causes', 'dock'),
    ('return_concept', 'opposes', 'explore_concept'),
    ('battery', 'sustains', 'energy'),
    ('hunger', 'causes', 'return_concept'),
    ('safety', 'enables', 'explore_concept'),
    ('danger', 'causes', 'return_concept'),

    # Cross-domain bridges
    ('gait', 'harmonizes', 'breath_concept'),
    ('walk', 'harmonizes', 'rhythm'),
    ('pain', 'opposes', 'harmony_concept'),
    ('dog', 'contains', 'leg'),
    ('dog', 'enables', 'walk'),
]


# ================================================================
#  WORLD LATTICE: The Graph
# ================================================================

class WorldLattice:
    """CK's world lattice: concepts connected by operator-labeled edges.

    This is NOT the Transition Lattice (TL). The TL tracks operator→operator
    frequencies. The WorldLattice tracks concept→concept relationships, where
    each concept is encoded as an operator pattern and each relation is an
    operator-labeled edge.

    The WorldLattice is language-independent. Words from any language bind
    to concept nodes via D2 curvature agreement.
    """

    def __init__(self):
        self.nodes: Dict[str, WorldNode] = {}
        self.languages_seen: Set[str] = set()
        self._word_index: Dict[str, Dict[str, str]] = {}  # lang → {word → node_id}

    def add_node(self, node: WorldNode):
        """Add a concept node to the lattice."""
        self.nodes[node.node_id] = node
        for lang, word in node.bindings.items():
            self.languages_seen.add(lang)
            if lang not in self._word_index:
                self._word_index[lang] = {}
            self._word_index[lang][word.lower()] = node.node_id

    def add_concept(self, node_id: str, operator_code: int,
                    domain: str = 'general',
                    bindings: Dict[str, str] = None) -> WorldNode:
        """Create and add a concept node with optional word bindings.

        D2 analysis is run on the first available binding to compute
        the node's curvature signature.
        """
        # Get D2 signature from first binding
        d2_sig = [0.0] * 5
        soft = [0.0] * NUM_OPS
        if bindings:
            first_word = next(iter(bindings.values()))
            _, _, d2_sig, soft = word_to_d2(first_word)

        node = WorldNode(node_id, operator_code, d2_sig, soft, domain)
        if bindings:
            for lang, word in bindings.items():
                node.bind_word(lang, word)
        self.add_node(node)
        return node

    def add_relation(self, source_id: str, rel_type: str, target_id: str):
        """Add a relation edge between two concepts."""
        if source_id not in self.nodes or target_id not in self.nodes:
            return
        op = RELATION_TYPES.get(rel_type, HARMONY)
        self.nodes[source_id].add_relation(rel_type, target_id, op)

    def lookup_word(self, word: str, language: str = None) -> Optional[WorldNode]:
        """Find the concept node a word binds to.

        If language is specified, search that language only.
        Otherwise, search all languages.
        """
        word_lower = word.lower()
        if language:
            idx = self._word_index.get(language, {})
            node_id = idx.get(word_lower)
            if node_id:
                return self.nodes.get(node_id)
        else:
            for lang_idx in self._word_index.values():
                node_id = lang_idx.get(word_lower)
                if node_id:
                    return self.nodes.get(node_id)
        return None

    def query_by_operator(self, op: int) -> List[WorldNode]:
        """Find all concepts with a given dominant operator."""
        return [n for n in self.nodes.values() if n.operator_code == op]

    def query_by_domain(self, domain: str) -> List[WorldNode]:
        """Find all concepts in a domain."""
        return [n for n in self.nodes.values() if n.domain == domain]

    def get_neighbors(self, node_id: str, rel_type: str = None) -> List[Tuple[str, str, int]]:
        """Get all neighbors of a node, optionally filtered by relation type.

        Returns: [(target_id, rel_type, operator), ...]
        """
        node = self.nodes.get(node_id)
        if not node:
            return []
        results = []
        for rtype, targets in node.relations.items():
            if rel_type and rtype != rel_type:
                continue
            for target_id, op in targets:
                results.append((target_id, rtype, op))
        return results

    def coherence_path(self, start_id: str, end_id: str,
                       max_depth: int = 5) -> Optional[List[str]]:
        """Find a path between two concepts, preferring HARMONY compositions.

        BFS with CL-based edge scoring.
        """
        if start_id not in self.nodes or end_id not in self.nodes:
            return None

        from collections import deque
        queue = deque([(start_id, [start_id])])
        visited = {start_id}

        while queue:
            current, path = queue.popleft()
            if current == end_id:
                return path
            if len(path) >= max_depth:
                continue

            neighbors = self.get_neighbors(current)
            # Sort by CL coherence (prefer HARMONY-producing edges)
            scored = []
            for target_id, rtype, op in neighbors:
                if target_id not in visited:
                    current_op = self.nodes[current].operator_code
                    fuse = compose(current_op, self.nodes[target_id].operator_code)
                    score = 1.0 if fuse == HARMONY else 0.5
                    scored.append((score, target_id))
            scored.sort(reverse=True)

            for _, target_id in scored:
                if target_id not in visited:
                    visited.add(target_id)
                    queue.append((target_id, path + [target_id]))

        return None

    def load_seed_corpus(self):
        """Load the built-in core concepts and relations."""
        for node_id, domain, op, bindings in CORE_CONCEPTS:
            self.add_concept(node_id, op, domain, bindings)
        for source, rel, target in CORE_RELATIONS:
            self.add_relation(source, rel, target)

    def bind_new_word(self, word: str, language: str,
                      node_id: str = None) -> Optional[str]:
        """Bind a new word to the best-matching concept node.

        If node_id is provided, bind directly.
        If not, use D2 agreement to find the best existing node.

        Returns the node_id the word was bound to, or None.
        """
        if node_id:
            node = self.nodes.get(node_id)
            if node:
                node.bind_word(language, word)
                self.languages_seen.add(language)
                if language not in self._word_index:
                    self._word_index[language] = {}
                self._word_index[language][word.lower()] = node_id
                return node_id
            return None

        # Find best-matching node by D2 agreement
        _, _, word_d2, _ = word_to_d2(word)
        best_id = None
        best_score = -1.0

        for nid, node in self.nodes.items():
            # Cosine similarity on D2 vectors
            dot = sum(a * b for a, b in zip(word_d2, node.d2_signature))
            mag_w = math.sqrt(sum(v * v for v in word_d2)) or 1e-10
            mag_n = math.sqrt(sum(v * v for v in node.d2_signature)) or 1e-10
            sim = dot / (mag_w * mag_n)
            if sim > best_score:
                best_score = sim
                best_id = nid

        if best_id and best_score > 0.5:
            return self.bind_new_word(word, language, best_id)
        return None

    # ── MDL COMPRESSION ──────────────────────────────────

    def description_length(self) -> dict:
        """Compute the Minimum Description Length of the lattice.

        Cost model (in operator-coded bits):
        - Each node: 1 (id) + 1 (operator) + 5 (d2_vec) = 7 units
        - Each edge: 1 (source) + 1 (target) + 1 (rel_type) = 3 units
        - Each binding: 1 (lang) + 1 (word) + 1 (node_id) = 3 units
        - Generator cost: fixed at 10 (operators) + 100 (CL table) = 110

        Lower is better. This is the irreducibility measure.
        """
        n_nodes = len(self.nodes)
        n_edges = sum(
            sum(len(targets) for targets in node.relations.values())
            for node in self.nodes.values()
        )
        n_bindings = sum(
            len(node.bindings)
            for node in self.nodes.values()
        )

        generator_cost = 110  # Fixed: 10 ops + 100 CL cells
        node_cost = n_nodes * 7
        edge_cost = n_edges * 3
        binding_cost = n_bindings * 3

        total = generator_cost + node_cost + edge_cost + binding_cost

        return {
            'total_mdl': total,
            'generator_cost': generator_cost,
            'node_cost': node_cost,
            'edge_cost': edge_cost,
            'binding_cost': binding_cost,
            'n_nodes': n_nodes,
            'n_edges': n_edges,
            'n_bindings': n_bindings,
            'n_languages': len(self.languages_seen),
            'bits_per_concept': round(total / max(n_nodes, 1), 1),
        }

    def compress(self) -> dict:
        """MDL compression pass.

        Merges nodes that have:
        1. Same dominant operator
        2. High D2 cosine similarity (> 0.95)
        3. Same domain

        Prunes edges to merged nodes.

        Returns stats about what was compressed.
        """
        before = self.description_length()
        merged = 0
        pruned_edges = 0

        # Group nodes by (operator, domain)
        groups = defaultdict(list)
        for nid, node in self.nodes.items():
            key = (node.operator_code, node.domain)
            groups[key].append(nid)

        # Within each group, find near-duplicates by D2 similarity
        to_merge = []  # (keep_id, remove_id)
        for key, node_ids in groups.items():
            if len(node_ids) < 2:
                continue
            for i in range(len(node_ids)):
                for j in range(i + 1, len(node_ids)):
                    nid_a, nid_b = node_ids[i], node_ids[j]
                    node_a = self.nodes[nid_a]
                    node_b = self.nodes[nid_b]
                    # D2 cosine similarity
                    dot = sum(a * b for a, b in zip(
                        node_a.d2_signature, node_b.d2_signature))
                    mag_a = math.sqrt(sum(v * v for v in node_a.d2_signature)) or 1e-10
                    mag_b = math.sqrt(sum(v * v for v in node_b.d2_signature)) or 1e-10
                    sim = dot / (mag_a * mag_b)
                    if sim > 0.95:
                        to_merge.append((nid_a, nid_b))

        # Execute merges (keep first, absorb second)
        removed_ids = set()
        for keep_id, remove_id in to_merge:
            if remove_id in removed_ids or keep_id in removed_ids:
                continue
            keep_node = self.nodes.get(keep_id)
            remove_node = self.nodes.get(remove_id)
            if not keep_node or not remove_node:
                continue

            # Absorb bindings
            for lang, word in remove_node.bindings.items():
                if lang not in keep_node.bindings:
                    keep_node.bind_word(lang, word)
                    if lang in self._word_index:
                        self._word_index[lang][word.lower()] = keep_id

            # Absorb relations
            for rtype, targets in remove_node.relations.items():
                for target_id, op in targets:
                    if target_id != keep_id:
                        keep_node.add_relation(rtype, target_id, op)

            # Redirect edges pointing to removed node
            for nid, node in self.nodes.items():
                for rtype in list(node.relations.keys()):
                    new_targets = []
                    for target_id, op in node.relations[rtype]:
                        if target_id == remove_id:
                            new_targets.append((keep_id, op))
                            pruned_edges += 1
                        else:
                            new_targets.append((target_id, op))
                    node.relations[rtype] = new_targets

            removed_ids.add(remove_id)
            merged += 1

        # Remove merged nodes
        for rid in removed_ids:
            del self.nodes[rid]

        after = self.description_length()

        return {
            'nodes_merged': merged,
            'edges_redirected': pruned_edges,
            'mdl_before': before['total_mdl'],
            'mdl_after': after['total_mdl'],
            'mdl_reduction': before['total_mdl'] - after['total_mdl'],
            'compression_ratio': round(
                after['total_mdl'] / max(before['total_mdl'], 1), 4),
        }

    # ── SNAPSHOT: Export Irreducible Core ─────────────────

    def snapshot(self) -> dict:
        """Export the lattice as a portable snapshot.

        This is the "thumbdrive seed": everything needed to reconstruct
        CK's world model on any hardware.
        """
        return {
            'version': '1.0',
            'generator': 'ck_world_lattice',
            'core_math': {
                'num_operators': NUM_OPS,
                'operator_names': OP_NAMES[:],
                'cl_table_harmony_cells': sum(
                    1 for r in CL for c in r if c == HARMONY),
                'coherence_threshold': 5.0 / 7.0,
            },
            'lattice': {
                'nodes': {nid: node.to_dict() for nid, node in self.nodes.items()},
                'languages': sorted(self.languages_seen),
            },
            'mdl': self.description_length(),
        }

    def save(self, path: str):
        """Save lattice snapshot to JSON."""
        data = self.snapshot()
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self, path: str):
        """Load lattice from snapshot JSON."""
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        lattice_data = data.get('lattice', {})
        nodes_data = lattice_data.get('nodes', {})

        for nid, ndata in nodes_data.items():
            node = WorldNode.from_dict(ndata)
            self.add_node(node)

    def stats(self) -> dict:
        """Lattice statistics."""
        domains = Counter(n.domain for n in self.nodes.values())
        operators = Counter(n.operator_code for n in self.nodes.values())
        total_bindings = sum(len(n.bindings) for n in self.nodes.values())
        total_edges = sum(
            sum(len(t) for t in n.relations.values())
            for n in self.nodes.values()
        )

        return {
            'n_nodes': len(self.nodes),
            'n_edges': total_edges,
            'n_bindings': total_bindings,
            'n_languages': len(self.languages_seen),
            'languages': sorted(self.languages_seen),
            'domains': dict(domains.most_common()),
            'operator_distribution': {
                OP_NAMES[op]: count
                for op, count in sorted(operators.items())
            },
            'mdl': self.description_length(),
        }

    def d2_cross_language_report(self) -> List[dict]:
        """Generate a cross-language D2 agreement report.

        For each concept with bindings in multiple languages,
        compute D2 agreement between all language pairs.
        Shows whether D2 curvature finds the same truth across languages.
        """
        report = []
        for nid, node in self.nodes.items():
            if len(node.bindings) < 2:
                continue
            langs = list(node.bindings.items())
            agreements = []
            for i in range(len(langs)):
                for j in range(i + 1, len(langs)):
                    lang_a, word_a = langs[i]
                    lang_b, word_b = langs[j]
                    agreement = d2_agreement(word_a, word_b)
                    agreements.append({
                        'pair': f"{lang_a}:{word_a} <> {lang_b}:{word_b}",
                        'agreement': round(agreement, 4),
                    })

            if agreements:
                avg = sum(a['agreement'] for a in agreements) / len(agreements)
                report.append({
                    'concept': nid,
                    'operator': OP_NAMES[node.operator_code],
                    'n_languages': len(node.bindings),
                    'avg_agreement': round(avg, 4),
                    'pairs': agreements,
                })

        report.sort(key=lambda r: r['avg_agreement'], reverse=True)
        return report


# ================================================================
#  BUILD FUNCTION: Create the full world lattice from seed
# ================================================================

def build_world_lattice() -> WorldLattice:
    """Build and return a fully initialized world lattice."""
    lattice = WorldLattice()
    lattice.load_seed_corpus()
    return lattice


# ================================================================
#  CLI
# ================================================================

if __name__ == '__main__':
    import sys

    lattice = build_world_lattice()
    stats = lattice.stats()

    print("=" * 60)
    print("CK WORLD LATTICE")
    print("=" * 60)
    print(f"  Concepts: {stats['n_nodes']}")
    print(f"  Relations: {stats['n_edges']}")
    print(f"  Word bindings: {stats['n_bindings']}")
    print(f"  Languages: {stats['n_languages']} ({', '.join(stats['languages'])})")
    print(f"  MDL: {stats['mdl']['total_mdl']} units")
    print(f"  Bits/concept: {stats['mdl']['bits_per_concept']}")
    print()
    print("Operator distribution:")
    for op_name, count in stats['operator_distribution'].items():
        print(f"    {op_name}: {count}")
    print()
    print("Domain distribution:")
    for domain, count in stats['domains'].items():
        print(f"    {domain}: {count}")

    if '--report' in sys.argv:
        print()
        print("Cross-language D2 agreement report (top 10):")
        report = lattice.d2_cross_language_report()
        for entry in report[:10]:
            print(f"  {entry['concept']} ({entry['operator']}): "
                  f"avg={entry['avg_agreement']:.4f} across {entry['n_languages']} languages")

    if '--compress' in sys.argv:
        print()
        print("Running MDL compression...")
        result = lattice.compress()
        print(f"  Nodes merged: {result['nodes_merged']}")
        print(f"  MDL: {result['mdl_before']} -> {result['mdl_after']}")
        print(f"  Compression ratio: {result['compression_ratio']}")

    if '--save' in sys.argv:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(base, 'ck_world_lattice.json')
        lattice.save(path)
        print(f"\n  Saved to: {path}")
