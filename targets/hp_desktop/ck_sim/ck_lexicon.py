"""
ck_lexicon.py -- Universal Lexicon Store: Every Word → Concept → Operator
=========================================================================
Operator: LATTICE (1) -- the lexicon IS a lattice of meaning.

CK's universal lexicon. Maps words across languages to concept nodes via
operator signatures computed from PHONEMES, not spelling.

Key insight: "Spelling is a lossy historical artifact; phonemes
are closer to motor physics." The IPA-to-Hebrew-root mapping preserves
articulatory physics: bilabials → PE/BET/MEM, velars → KAF/GIMEL,
nasals → MEM/NUN, glides → VAV/YOD.

Architecture:
  PhonemeCodec    -- IPA phonemes → Hebrew roots → D2 → operator signature
  Lexeme          -- One word: form + lemma + phonemes + signature + senses
  LexiconStore    -- All words, all languages. Lookup by word, sound, concept.

Translation is NOT a separate task. It's a LOOKUP:
  word_A → concept_id → word_B

Memory: ~200 bytes per lexeme. 50k words = 10MB. Dictionary-scale, not LLM-scale.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
from collections import Counter
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Set

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, COLLAPSE, CHAOS, PROGRESS, BREATH,
    BALANCE, COUNTER, LATTICE, RESET, OP_NAMES, compose
)
from ck_sim.ck_sim_d2 import ROOTS_FLOAT
from ck_sim.ck_sensory_codecs import CurvatureEngine


# ================================================================
#  CONSTANTS
# ================================================================

MAX_LEXEMES = 100_000       # Max lexemes in store
MAX_SENSES = 8              # Max senses per lexeme
SIMILARITY_THRESHOLD = 0.5  # Cosine threshold for sound-alike matching


# ================================================================
#  IPA PHONEME → HEBREW ROOT MAPPING
# ================================================================

# Articulatory phonetics → Hebrew roots.
# Hebrew roots ARE organized by place/manner of articulation.
# This mapping preserves motor physics: how the mouth MOVES.
#
# Place of articulation:
#   Bilabial:      p,b,m,w    → PE, BET, MEM, VAV
#   Labiodental:   f,v        → PE, VAV
#   Alveolar:      t,d,n,s,z  → TAV, DALET, NUN, SAMEKH, ZAYIN
#   Postalveolar:  ʃ,ʒ        → SHIN, ZAYIN
#   Palatal:       j           → YOD
#   Velar:         k,g,ŋ      → KAF, GIMEL, NUN
#   Pharyngeal:    ħ,ʕ        → CHET, AYIN
#   Glottal:       ʔ,h        → ALEPH, HE
# Vowels by height:
#   High:   i,u → YOD, VAV
#   Mid:    e,o → HE, AYIN
#   Low:    a   → ALEPH

IPA_TO_ROOT = {
    # Vowels
    'a': 'ALEPH',  'ɑ': 'ALEPH',  'æ': 'ALEPH',  'ɐ': 'ALEPH',
    'e': 'HE',     'ɛ': 'HE',     'ə': 'HE',
    'i': 'YOD',    'ɪ': 'YOD',
    'o': 'AYIN',   'ɔ': 'AYIN',
    'u': 'VAV',    'ʊ': 'VAV',

    # Bilabial stops
    'p': 'PE',     'b': 'BET',

    # Alveolar stops
    't': 'TAV',    'd': 'DALET',

    # Velar stops
    'k': 'KAF',    'g': 'GIMEL',   'ɡ': 'GIMEL',

    # Glottal stop
    'ʔ': 'ALEPH',

    # Uvular stop
    'q': 'QOF',

    # Labiodental fricatives
    'f': 'PE',     'v': 'VAV',

    # Dental fricatives
    'θ': 'TAV',    'ð': 'DALET',

    # Alveolar fricatives
    's': 'SAMEKH', 'z': 'ZAYIN',

    # Postalveolar fricatives
    'ʃ': 'SHIN',   'ʒ': 'ZAYIN',

    # Pharyngeal / glottal fricatives
    'h': 'HE',     'ħ': 'CHET',    'ʕ': 'AYIN',
    'x': 'CHET',   'ɣ': 'GIMEL',

    # Nasals
    'm': 'MEM',    'n': 'NUN',     'ŋ': 'NUN',    'ɲ': 'NUN',

    # Liquids
    'l': 'LAMED',  'r': 'RESH',    'ɹ': 'RESH',
    'ɾ': 'RESH',   'ʁ': 'RESH',

    # Glides
    'w': 'VAV',    'j': 'YOD',

    # Affricates (digraphs)
    'ts': 'TSADE', 'dz': 'ZAYIN',

    # Retroflex (nearest equivalents)
    'ʈ': 'TAV',    'ɖ': 'DALET',   'ʂ': 'SHIN',   'ʐ': 'ZAYIN',
}

# ASCII fallback for when real IPA is not available
ASCII_PHONEME_MAP = {
    'a': 'ALEPH', 'b': 'BET',   'ch': 'CHET',  'd': 'DALET',
    'e': 'HE',    'f': 'PE',    'g': 'GIMEL',  'h': 'HE',
    'i': 'YOD',   'j': 'YOD',   'k': 'KAF',    'l': 'LAMED',
    'm': 'MEM',   'n': 'NUN',   'ng': 'NUN',    'o': 'AYIN',
    'p': 'PE',    'q': 'QOF',   'r': 'RESH',    's': 'SAMEKH',
    'sh': 'SHIN', 't': 'TAV',   'th': 'TAV',    'ts': 'TSADE',
    'u': 'VAV',   'v': 'VAV',   'w': 'VAV',     'x': 'CHET',
    'y': 'YOD',   'z': 'ZAYIN', 'zh': 'ZAYIN',
}


# ================================================================
#  LEXICAL SIGNATURE
# ================================================================

@dataclass
class LexicalSignature:
    """Operator signature of a word, computed from phonemes.

    This is the "fingerprint" of a word in operator space.
    Words expressing the same concept converge to similar signatures
    across languages because meaning constrains sound patterns.
    """
    dominant_op: int = VOID
    d2_vector: tuple = (0.0, 0.0, 0.0, 0.0, 0.0)
    soft_dist: tuple = tuple([1.0 / NUM_OPS] * NUM_OPS)
    chain_length: int = 0

    def cosine_similarity(self, other: 'LexicalSignature') -> float:
        """Cosine similarity on D2 vectors."""
        dot = sum(a * b for a, b in zip(self.d2_vector, other.d2_vector))
        norm_a = math.sqrt(sum(a * a for a in self.d2_vector)) + 1e-10
        norm_b = math.sqrt(sum(b * b for b in other.d2_vector)) + 1e-10
        return max(0.0, dot / (norm_a * norm_b))

    def dist_similarity(self, other: 'LexicalSignature') -> float:
        """Cosine similarity on operator distributions."""
        dot = sum(a * b for a, b in zip(self.soft_dist, other.soft_dist))
        norm_a = math.sqrt(sum(a * a for a in self.soft_dist)) + 1e-10
        norm_b = math.sqrt(sum(b * b for b in other.soft_dist)) + 1e-10
        return max(0.0, dot / (norm_a * norm_b))


# ================================================================
#  PHONEME CODEC
# ================================================================

class PhonemeCodec:
    """Maps phoneme sequences → D2 curvature → operator signature.

    This is the PHONEME-FIRST approach: compute operator signatures
    from how words SOUND, not how they're spelled.

    Pipeline:
      IPA phonemes → Hebrew roots → 5D force vectors → D2 curvature → operator
    """

    def _parse_phonemes(self, ipa_string: str) -> List[str]:
        """Parse IPA string into individual phoneme tokens.

        Handles digraphs (ts, dz, ch, sh, ng, th, zh) by greedy longest-match.
        Strips stress marks, length marks, and whitespace.
        """
        tokens = []
        i = 0
        s = ipa_string.strip().replace(' ', '').replace('ˈ', '').replace('ˌ', '')
        s = s.replace('ː', '')  # Strip length marks

        while i < len(s):
            matched = False
            # Try 2-char then 1-char (greedy)
            for length in (2, 1):
                if i + length <= len(s):
                    candidate = s[i:i + length]
                    if candidate in IPA_TO_ROOT or candidate in ASCII_PHONEME_MAP:
                        tokens.append(candidate)
                        i += length
                        matched = True
                        break
            if not matched:
                i += 1  # Skip unknown characters
        return tokens

    def _phoneme_to_force(self, phoneme: str) -> Optional[List[float]]:
        """Map a single phoneme to its 5D force vector via Hebrew root."""
        root = IPA_TO_ROOT.get(phoneme)
        if root is None:
            root = ASCII_PHONEME_MAP.get(phoneme)
        if root is None:
            return None

        force = ROOTS_FLOAT.get(root)
        if force is None:
            return None

        return list(force)

    def compute_signature(self, phonemes: str) -> LexicalSignature:
        """Compute operator signature from phoneme string.

        Args:
            phonemes: IPA string or simplified phoneme representation.

        Returns:
            LexicalSignature with D2 curvature and operator distribution.
        """
        tokens = self._parse_phonemes(phonemes)
        if not tokens:
            return LexicalSignature()

        engine = CurvatureEngine()
        operators = []
        d2_vecs = []

        for token in tokens:
            force = self._phoneme_to_force(token)
            if force is None:
                continue

            if engine.feed(force):
                operators.append(engine.operator)
                d2_vecs.append(engine.d2_float[:])

        if not operators:
            return LexicalSignature()

        # Dominant operator
        dominant = Counter(operators).most_common(1)[0][0]

        # Mean D2 vector
        mean_d2 = tuple(
            sum(v[i] for v in d2_vecs) / len(d2_vecs)
            for i in range(5)
        )

        # Soft distribution
        dist = [0.0] * NUM_OPS
        for op in operators:
            if 0 <= op < NUM_OPS:
                dist[op] += 1.0
        total = sum(dist)
        if total > 0:
            dist = [d / total for d in dist]
        else:
            dist = [1.0 / NUM_OPS] * NUM_OPS

        return LexicalSignature(
            dominant_op=dominant,
            d2_vector=mean_d2,
            soft_dist=tuple(dist),
            chain_length=len(operators),
        )

    def compute_from_spelling(self, word: str) -> LexicalSignature:
        """Fallback: compute signature from spelling (via transliteration).

        Used when no phoneme data is available. Less accurate than phoneme-first
        because spelling is lossy, but better than nothing.
        """
        from ck_sim.ck_world_lattice import word_to_d2
        dominant, ops, mean_d2, soft = word_to_d2(word)
        return LexicalSignature(
            dominant_op=dominant,
            d2_vector=tuple(mean_d2),
            soft_dist=tuple(soft),
            chain_length=len(ops),
        )


# ================================================================
#  LEXEME
# ================================================================

@dataclass
class Lexeme:
    """One word entry in the universal lexicon.

    A lexeme is a word in a specific language, with its pronunciation,
    operator signature, and links to concept nodes.
    """
    lexeme_id: int = 0
    lang: str = 'en'
    wordform: str = ''
    lemma: str = ''
    phonemes: str = ''
    freq: int = 0
    signature: LexicalSignature = field(default_factory=LexicalSignature)
    sense_ids: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            'id': self.lexeme_id,
            'lang': self.lang,
            'wordform': self.wordform,
            'lemma': self.lemma,
            'phonemes': self.phonemes,
            'freq': self.freq,
            'dominant_op': self.signature.dominant_op,
            'chain_length': self.signature.chain_length,
            'senses': list(self.sense_ids),
        }


# ================================================================
#  LEXICON STORE
# ================================================================

class LexiconStore:
    """Universal lexicon: every word → concept → operator.

    The missing link between CK's perception and language. Words are
    stored with phoneme-based operator signatures and linked to
    concept nodes in the WorldLattice.

    Lookup modes:
      1. By word:    "water" → Lexeme(s)
      2. By sound:   phonemes → Lexeme(s) with similar D2 signatures
      3. By concept: concept_id → {"en": [water], "es": [agua], ...}
      4. Translate:   word_A (lang_A) → concept → word_B (lang_B)
    """

    def __init__(self, lattice=None):
        self.lexemes: Dict[int, Lexeme] = {}
        self._word_index: Dict[str, Dict[str, List[int]]] = {}
        self._lemma_index: Dict[str, Dict[str, List[int]]] = {}
        self._concept_index: Dict[str, List[int]] = {}
        self.lattice = lattice
        self._codec = PhonemeCodec()
        self._next_id: int = 0
        self.languages: Set[str] = set()

    def add_lexeme(self, lang: str, wordform: str, lemma: str = None,
                   phonemes: str = '', freq: int = 0,
                   sense_ids: List[str] = None) -> Lexeme:
        """Add a word to the lexicon.

        Automatically computes operator signature from phonemes (preferred)
        or spelling (fallback).
        """
        if lemma is None:
            lemma = wordform.lower()
        if sense_ids is None:
            sense_ids = []

        # Compute signature: phoneme-first, spelling-fallback
        if phonemes:
            sig = self._codec.compute_signature(phonemes)
        else:
            sig = self._codec.compute_from_spelling(wordform)

        lex = Lexeme(
            lexeme_id=self._next_id,
            lang=lang,
            wordform=wordform,
            lemma=lemma,
            phonemes=phonemes,
            freq=freq,
            signature=sig,
            sense_ids=list(sense_ids),
        )

        self.lexemes[self._next_id] = lex
        self._next_id += 1
        self.languages.add(lang)

        # Index by wordform
        if lang not in self._word_index:
            self._word_index[lang] = {}
        key = wordform.lower()
        if key not in self._word_index[lang]:
            self._word_index[lang][key] = []
        self._word_index[lang][key].append(lex.lexeme_id)

        # Index by lemma
        if lang not in self._lemma_index:
            self._lemma_index[lang] = {}
        lkey = lemma.lower()
        if lkey not in self._lemma_index[lang]:
            self._lemma_index[lang][lkey] = []
        self._lemma_index[lang][lkey].append(lex.lexeme_id)

        # Index by concept
        for cid in sense_ids:
            if cid not in self._concept_index:
                self._concept_index[cid] = []
            self._concept_index[cid].append(lex.lexeme_id)

        return lex

    def lookup_word(self, word: str, lang: str = None) -> List[Lexeme]:
        """Find lexemes matching a word."""
        key = word.lower()
        results = []

        if lang:
            ids = self._word_index.get(lang, {}).get(key, [])
            results.extend(self.lexemes[i] for i in ids if i in self.lexemes)
        else:
            for lang_idx in self._word_index.values():
                ids = lang_idx.get(key, [])
                results.extend(self.lexemes[i] for i in ids if i in self.lexemes)

        return results

    def lookup_lemma(self, lemma: str, lang: str = None) -> List[Lexeme]:
        """Find all word forms for a lemma."""
        key = lemma.lower()
        results = []

        if lang:
            ids = self._lemma_index.get(lang, {}).get(key, [])
            results.extend(self.lexemes[i] for i in ids if i in self.lexemes)
        else:
            for lang_idx in self._lemma_index.values():
                ids = lang_idx.get(key, [])
                results.extend(self.lexemes[i] for i in ids if i in self.lexemes)

        return results

    def lookup_concept(self, concept_id: str) -> Dict[str, List[Lexeme]]:
        """Find all words expressing a concept, grouped by language."""
        ids = self._concept_index.get(concept_id, [])
        by_lang: Dict[str, List[Lexeme]] = {}

        for lid in ids:
            lex = self.lexemes.get(lid)
            if lex:
                if lex.lang not in by_lang:
                    by_lang[lex.lang] = []
                by_lang[lex.lang].append(lex)

        return by_lang

    def lookup_by_sound(self, phonemes: str,
                        threshold: float = SIMILARITY_THRESHOLD
                        ) -> List[Tuple[Lexeme, float]]:
        """Find words that sound similar (cosine on D2 signatures).

        Returns list of (lexeme, similarity_score) sorted best-first.
        """
        query_sig = self._codec.compute_signature(phonemes)
        if query_sig.chain_length == 0:
            return []

        results = []
        for lex in self.lexemes.values():
            if lex.signature.chain_length == 0:
                continue
            sim = query_sig.cosine_similarity(lex.signature)
            if sim >= threshold:
                results.append((lex, sim))

        results.sort(key=lambda x: x[1], reverse=True)
        return results

    def translate(self, word: str, from_lang: str, to_lang: str) -> List[str]:
        """Translate word via concept pivot.

        word → Lexeme(from_lang) → concept_id → Lexeme(to_lang) → word

        Returns list of possible translations.
        """
        source_lexemes = self.lookup_word(word, from_lang)
        if not source_lexemes:
            return []

        translations = []
        seen = set()

        for src in source_lexemes:
            for concept_id in src.sense_ids:
                target_ids = self._concept_index.get(concept_id, [])
                for tid in target_ids:
                    target = self.lexemes.get(tid)
                    if target and target.lang == to_lang:
                        if target.wordform not in seen:
                            translations.append(target.wordform)
                            seen.add(target.wordform)

        return translations

    def all_translations(self, word: str, from_lang: str) -> Dict[str, List[str]]:
        """Get translations to ALL known languages."""
        source_lexemes = self.lookup_word(word, from_lang)
        if not source_lexemes:
            return {}

        result: Dict[str, List[str]] = {}
        for src in source_lexemes:
            for concept_id in src.sense_ids:
                by_lang = self.lookup_concept(concept_id)
                for lang, lexemes in by_lang.items():
                    if lang == from_lang:
                        continue
                    if lang not in result:
                        result[lang] = []
                    for lex in lexemes:
                        if lex.wordform not in result[lang]:
                            result[lang].append(lex.wordform)
        return result

    def concept_words(self, concept_id: str, lang: str = None) -> List[str]:
        """Get all words for a concept, optionally filtered by language."""
        by_lang = self.lookup_concept(concept_id)
        if lang:
            return [lex.wordform for lex in by_lang.get(lang, [])]
        return [lex.wordform for lexemes in by_lang.values() for lex in lexemes]

    def load_seed_lexicon(self):
        """Load built-in core vocabulary (50 concepts × 7 languages)."""
        for concept_id, entries in SEED_LEXICON.items():
            for lang, wordform, phonemes in entries:
                self.add_lexeme(
                    lang=lang,
                    wordform=wordform,
                    lemma=wordform.lower(),
                    phonemes=phonemes,
                    freq=1000,
                    sense_ids=[concept_id],
                )

    @property
    def word_count(self) -> int:
        return len(self.lexemes)

    @property
    def concept_count(self) -> int:
        return len(self._concept_index)

    @property
    def language_count(self) -> int:
        return len(self.languages)

    def stats(self) -> dict:
        return {
            'total_lexemes': self.word_count,
            'concepts_covered': self.concept_count,
            'languages': sorted(self.languages),
            'language_count': self.language_count,
            'lexemes_per_language': {
                lang: sum(len(ids) for ids in idx.values())
                for lang, idx in self._word_index.items()
            },
        }


# ================================================================
#  SEED LEXICON: 50 Core Concepts × 7 Languages
# ================================================================

# Format: concept_id → [(lang, wordform, phonemes), ...]
# Phonemes use IPA where parseable, simplified otherwise.
# 7 languages: en, es, fr, de, he, ar, zh
#
# These 50 concepts span the most fundamental human experiences:
#   physical elements, body, family, nature, animals,
#   actions, states, time, abstract universals.

SEED_LEXICON = {
    # --- Physical Elements ---
    'water': [
        ('en', 'water', 'woter'),   ('es', 'agua', 'agwa'),
        ('fr', 'eau', 'o'),         ('de', 'Wasser', 'vaser'),
        ('he', 'mayim', 'majim'),   ('ar', 'maa', 'ma'),
        ('zh', 'shui', 'ʃuei'),
    ],
    'fire': [
        ('en', 'fire', 'fair'),     ('es', 'fuego', 'fwego'),
        ('fr', 'feu', 'fo'),        ('de', 'Feuer', 'foier'),
        ('he', 'esh', 'eʃ'),        ('ar', 'naar', 'nar'),
        ('zh', 'huo', 'xwo'),
    ],
    'earth': [
        ('en', 'earth', 'erθ'),     ('es', 'tierra', 'tiera'),
        ('fr', 'terre', 'ter'),     ('de', 'Erde', 'erde'),
        ('he', 'adama', 'adama'),   ('ar', 'ard', 'ard'),
        ('zh', 'tu', 'tu'),
    ],
    'light': [
        ('en', 'light', 'lait'),    ('es', 'luz', 'lus'),
        ('fr', 'lumiere', 'lumier'), ('de', 'Licht', 'lixt'),
        ('he', 'or', 'or'),         ('ar', 'nur', 'nur'),
        ('zh', 'guang', 'gwang'),
    ],
    'air': [
        ('en', 'air', 'er'),        ('es', 'aire', 'aire'),
        ('fr', 'air', 'er'),        ('de', 'Luft', 'luft'),
        ('he', 'avir', 'avir'),     ('ar', 'hawa', 'hawa'),
        ('zh', 'qi', 'tʃi'),
    ],

    # --- Body ---
    'hand': [
        ('en', 'hand', 'hænd'),     ('es', 'mano', 'mano'),
        ('fr', 'main', 'men'),      ('de', 'Hand', 'hant'),
        ('he', 'yad', 'jad'),       ('ar', 'yad', 'jad'),
        ('zh', 'shou', 'ʃou'),
    ],
    'eye': [
        ('en', 'eye', 'ai'),        ('es', 'ojo', 'oxo'),
        ('fr', 'oeil', 'oj'),       ('de', 'Auge', 'auge'),
        ('he', 'ayin', 'ajin'),     ('ar', 'ayn', 'ajn'),
        ('zh', 'yan', 'jan'),
    ],
    'head': [
        ('en', 'head', 'hed'),      ('es', 'cabeza', 'kabesa'),
        ('fr', 'tete', 'tet'),      ('de', 'Kopf', 'kopf'),
        ('he', 'rosh', 'roʃ'),      ('ar', 'ras', 'ras'),
        ('zh', 'tou', 'tou'),
    ],
    'heart': [
        ('en', 'heart', 'hart'),    ('es', 'corazon', 'korason'),
        ('fr', 'coeur', 'ker'),     ('de', 'Herz', 'herts'),
        ('he', 'lev', 'lev'),       ('ar', 'qalb', 'qalb'),
        ('zh', 'xin', 'ʃin'),
    ],
    'blood': [
        ('en', 'blood', 'blod'),    ('es', 'sangre', 'sangre'),
        ('fr', 'sang', 'sang'),     ('de', 'Blut', 'blut'),
        ('he', 'dam', 'dam'),       ('ar', 'dam', 'dam'),
        ('zh', 'xue', 'ʃue'),
    ],

    # --- Family ---
    'mother': [
        ('en', 'mother', 'moðer'),  ('es', 'madre', 'madre'),
        ('fr', 'mere', 'mer'),      ('de', 'Mutter', 'muter'),
        ('he', 'ima', 'ima'),       ('ar', 'umm', 'um'),
        ('zh', 'mama', 'mama'),
    ],
    'father': [
        ('en', 'father', 'faðer'),  ('es', 'padre', 'padre'),
        ('fr', 'pere', 'per'),      ('de', 'Vater', 'fater'),
        ('he', 'aba', 'aba'),       ('ar', 'ab', 'ab'),
        ('zh', 'baba', 'baba'),
    ],
    'child': [
        ('en', 'child', 'tʃaild'),  ('es', 'hijo', 'ixo'),
        ('fr', 'enfant', 'enfan'),  ('de', 'Kind', 'kint'),
        ('he', 'yeled', 'jeled'),   ('ar', 'tifl', 'tifl'),
        ('zh', 'haizi', 'haizi'),
    ],
    'brother': [
        ('en', 'brother', 'broðer'), ('es', 'hermano', 'ermano'),
        ('fr', 'frere', 'frer'),     ('de', 'Bruder', 'bruder'),
        ('he', 'akh', 'ax'),         ('ar', 'akh', 'ax'),
        ('zh', 'gege', 'gege'),
    ],
    'sister': [
        ('en', 'sister', 'sister'),  ('es', 'hermana', 'ermana'),
        ('fr', 'soeur', 'ser'),      ('de', 'Schwester', 'ʃvester'),
        ('he', 'akhot', 'axot'),     ('ar', 'ukht', 'uxt'),
        ('zh', 'jiejie', 'dʒiedʒie'),
    ],

    # --- Nature ---
    'sun': [
        ('en', 'sun', 'san'),       ('es', 'sol', 'sol'),
        ('fr', 'soleil', 'solej'),   ('de', 'Sonne', 'zone'),
        ('he', 'shemesh', 'ʃemeʃ'), ('ar', 'shams', 'ʃams'),
        ('zh', 'taiyang', 'taijang'),
    ],
    'moon': [
        ('en', 'moon', 'mun'),      ('es', 'luna', 'luna'),
        ('fr', 'lune', 'lun'),      ('de', 'Mond', 'mont'),
        ('he', 'yareach', 'jareax'), ('ar', 'qamar', 'qamar'),
        ('zh', 'yue', 'jue'),
    ],
    'star': [
        ('en', 'star', 'star'),     ('es', 'estrella', 'estreja'),
        ('fr', 'etoile', 'etwal'),  ('de', 'Stern', 'ʃtern'),
        ('he', 'kokhav', 'koxav'),  ('ar', 'najm', 'nadʒm'),
        ('zh', 'xing', 'ʃing'),
    ],
    'tree': [
        ('en', 'tree', 'tri'),      ('es', 'arbol', 'arbol'),
        ('fr', 'arbre', 'arbr'),    ('de', 'Baum', 'baum'),
        ('he', 'etz', 'ets'),       ('ar', 'shajara', 'ʃadʒara'),
        ('zh', 'shu', 'ʃu'),
    ],
    'stone': [
        ('en', 'stone', 'ston'),    ('es', 'piedra', 'piedra'),
        ('fr', 'pierre', 'pier'),   ('de', 'Stein', 'ʃtain'),
        ('he', 'even', 'even'),     ('ar', 'hajar', 'hadʒar'),
        ('zh', 'shi', 'ʃi'),
    ],
    'river': [
        ('en', 'river', 'river'),   ('es', 'rio', 'rio'),
        ('fr', 'riviere', 'rivier'), ('de', 'Fluss', 'flus'),
        ('he', 'nahar', 'nahar'),   ('ar', 'nahr', 'nahr'),
        ('zh', 'he', 'he'),
    ],
    'mountain': [
        ('en', 'mountain', 'maunten'), ('es', 'montana', 'montana'),
        ('fr', 'montagne', 'montanj'), ('de', 'Berg', 'berg'),
        ('he', 'har', 'har'),          ('ar', 'jabal', 'dʒabal'),
        ('zh', 'shan', 'ʃan'),
    ],

    # --- Animals ---
    'dog': [
        ('en', 'dog', 'dog'),       ('es', 'perro', 'pero'),
        ('fr', 'chien', 'ʃien'),    ('de', 'Hund', 'hunt'),
        ('he', 'kelev', 'kelev'),   ('ar', 'kalb', 'kalb'),
        ('zh', 'gou', 'gou'),
    ],
    'cat': [
        ('en', 'cat', 'kæt'),       ('es', 'gato', 'gato'),
        ('fr', 'chat', 'ʃa'),       ('de', 'Katze', 'katse'),
        ('he', 'khatul', 'xatul'),   ('ar', 'qitt', 'qit'),
        ('zh', 'mao', 'mao'),
    ],
    'bird': [
        ('en', 'bird', 'berd'),     ('es', 'pajaro', 'paxaro'),
        ('fr', 'oiseau', 'wazo'),   ('de', 'Vogel', 'fogel'),
        ('he', 'tsipor', 'tsipor'), ('ar', 'tayr', 'tajr'),
        ('zh', 'niao', 'niao'),
    ],
    'fish': [
        ('en', 'fish', 'fiʃ'),      ('es', 'pez', 'peθ'),
        ('fr', 'poisson', 'pwason'), ('de', 'Fisch', 'fiʃ'),
        ('he', 'dag', 'dag'),        ('ar', 'samak', 'samak'),
        ('zh', 'yu', 'ju'),
    ],

    # --- Actions ---
    'eat': [
        ('en', 'eat', 'it'),        ('es', 'comer', 'komer'),
        ('fr', 'manger', 'mandʒe'), ('de', 'essen', 'esen'),
        ('he', 'lekhol', 'lexol'),   ('ar', 'akala', 'akala'),
        ('zh', 'chi', 'tʃi'),
    ],
    'drink': [
        ('en', 'drink', 'drink'),   ('es', 'beber', 'beber'),
        ('fr', 'boire', 'bwar'),    ('de', 'trinken', 'trinken'),
        ('he', 'lishtot', 'liʃtot'), ('ar', 'shariba', 'ʃariba'),
        ('zh', 'he', 'he'),
    ],
    'sleep': [
        ('en', 'sleep', 'slip'),    ('es', 'dormir', 'dormir'),
        ('fr', 'dormir', 'dormir'), ('de', 'schlafen', 'ʃlafen'),
        ('he', 'lishon', 'liʃon'),  ('ar', 'nama', 'nama'),
        ('zh', 'shui', 'ʃuei'),
    ],
    'walk': [
        ('en', 'walk', 'wok'),      ('es', 'caminar', 'kaminar'),
        ('fr', 'marcher', 'marʃe'),  ('de', 'gehen', 'gen'),
        ('he', 'lalekhet', 'lalexet'), ('ar', 'mashaa', 'maʃa'),
        ('zh', 'zou', 'zou'),
    ],
    'see': [
        ('en', 'see', 'si'),        ('es', 'ver', 'ver'),
        ('fr', 'voir', 'vwar'),     ('de', 'sehen', 'zen'),
        ('he', 'lirot', 'lirot'),   ('ar', 'raa', 'ra'),
        ('zh', 'kan', 'kan'),
    ],
    'hear': [
        ('en', 'hear', 'hir'),      ('es', 'oir', 'oir'),
        ('fr', 'entendre', 'entandr'), ('de', 'hoeren', 'horen'),
        ('he', 'lishmoa', 'liʃmoa'), ('ar', 'samia', 'samia'),
        ('zh', 'ting', 'ting'),
    ],
    'speak': [
        ('en', 'speak', 'spik'),    ('es', 'hablar', 'ablar'),
        ('fr', 'parler', 'parle'),  ('de', 'sprechen', 'ʃprexen'),
        ('he', 'ledaber', 'ledaber'), ('ar', 'takallama', 'takalama'),
        ('zh', 'shuo', 'ʃuo'),
    ],

    # --- States ---
    'big': [
        ('en', 'big', 'big'),       ('es', 'grande', 'grande'),
        ('fr', 'grand', 'gran'),    ('de', 'gross', 'gros'),
        ('he', 'gadol', 'gadol'),   ('ar', 'kabir', 'kabir'),
        ('zh', 'da', 'da'),
    ],
    'small': [
        ('en', 'small', 'smol'),    ('es', 'pequeno', 'pekeno'),
        ('fr', 'petit', 'peti'),    ('de', 'klein', 'klain'),
        ('he', 'katan', 'katan'),   ('ar', 'saghir', 'sagir'),
        ('zh', 'xiao', 'ʃiao'),
    ],
    'good': [
        ('en', 'good', 'gud'),      ('es', 'bueno', 'bweno'),
        ('fr', 'bon', 'bon'),       ('de', 'gut', 'gut'),
        ('he', 'tov', 'tov'),       ('ar', 'jayyid', 'dʒajid'),
        ('zh', 'hao', 'hao'),
    ],
    'new': [
        ('en', 'new', 'nu'),        ('es', 'nuevo', 'nwevo'),
        ('fr', 'nouveau', 'nuvo'),  ('de', 'neu', 'noi'),
        ('he', 'khadash', 'xadaʃ'), ('ar', 'jadid', 'dʒadid'),
        ('zh', 'xin', 'ʃin'),
    ],
    'old': [
        ('en', 'old', 'old'),       ('es', 'viejo', 'viexo'),
        ('fr', 'vieux', 'vio'),     ('de', 'alt', 'alt'),
        ('he', 'yashan', 'jaʃan'),  ('ar', 'qadim', 'qadim'),
        ('zh', 'lao', 'lao'),
    ],

    # --- Time ---
    'day': [
        ('en', 'day', 'dei'),       ('es', 'dia', 'dia'),
        ('fr', 'jour', 'ʒur'),      ('de', 'Tag', 'tag'),
        ('he', 'yom', 'jom'),       ('ar', 'yawm', 'jaum'),
        ('zh', 'tian', 'tian'),
    ],
    'night': [
        ('en', 'night', 'nait'),    ('es', 'noche', 'notʃe'),
        ('fr', 'nuit', 'nui'),      ('de', 'Nacht', 'naxt'),
        ('he', 'layla', 'laila'),   ('ar', 'layl', 'lajl'),
        ('zh', 'ye', 'je'),
    ],
    'year': [
        ('en', 'year', 'jir'),      ('es', 'ano', 'ano'),
        ('fr', 'annee', 'ane'),     ('de', 'Jahr', 'jar'),
        ('he', 'shana', 'ʃana'),    ('ar', 'sana', 'sana'),
        ('zh', 'nian', 'nian'),
    ],

    # --- Abstract Universals ---
    'love': [
        ('en', 'love', 'lav'),      ('es', 'amor', 'amor'),
        ('fr', 'amour', 'amur'),    ('de', 'Liebe', 'libe'),
        ('he', 'ahava', 'ahava'),   ('ar', 'hubb', 'hub'),
        ('zh', 'ai', 'ai'),
    ],
    'death': [
        ('en', 'death', 'deθ'),     ('es', 'muerte', 'mwerte'),
        ('fr', 'mort', 'mor'),      ('de', 'Tod', 'tot'),
        ('he', 'mavet', 'mavet'),   ('ar', 'mawt', 'maut'),
        ('zh', 'si', 'si'),
    ],
    'life': [
        ('en', 'life', 'laif'),     ('es', 'vida', 'vida'),
        ('fr', 'vie', 'vi'),        ('de', 'Leben', 'leben'),
        ('he', 'khayim', 'xajim'), ('ar', 'hayat', 'hajat'),
        ('zh', 'sheng', 'ʃeng'),
    ],
    'truth': [
        ('en', 'truth', 'truθ'),    ('es', 'verdad', 'verdad'),
        ('fr', 'verite', 'verite'),  ('de', 'Wahrheit', 'varhait'),
        ('he', 'emet', 'emet'),      ('ar', 'haqq', 'haq'),
        ('zh', 'zhen', 'ʒen'),
    ],
    'name': [
        ('en', 'name', 'neim'),     ('es', 'nombre', 'nombre'),
        ('fr', 'nom', 'nom'),       ('de', 'Name', 'name'),
        ('he', 'shem', 'ʃem'),      ('ar', 'ism', 'ism'),
        ('zh', 'ming', 'ming'),
    ],
    'god': [
        ('en', 'god', 'god'),       ('es', 'dios', 'dios'),
        ('fr', 'dieu', 'dio'),      ('de', 'Gott', 'got'),
        ('he', 'elohim', 'elohim'), ('ar', 'allah', 'ala'),
        ('zh', 'shen', 'ʃen'),
    ],
    'peace': [
        ('en', 'peace', 'pis'),     ('es', 'paz', 'paθ'),
        ('fr', 'paix', 'pe'),       ('de', 'Frieden', 'friden'),
        ('he', 'shalom', 'ʃalom'),  ('ar', 'salaam', 'salam'),
        ('zh', 'heping', 'heping'),
    ],
    'home': [
        ('en', 'home', 'hom'),      ('es', 'hogar', 'ogar'),
        ('fr', 'maison', 'mezon'),  ('de', 'Heim', 'haim'),
        ('he', 'bayit', 'bajit'),   ('ar', 'bayt', 'bajt'),
        ('zh', 'jia', 'dʒia'),
    ],
    'war': [
        ('en', 'war', 'wor'),       ('es', 'guerra', 'gera'),
        ('fr', 'guerre', 'ger'),    ('de', 'Krieg', 'krig'),
        ('he', 'milkhama', 'milxama'), ('ar', 'harb', 'harb'),
        ('zh', 'zhan', 'ʒan'),
    ],
}

# Verify seed integrity
assert len(SEED_LEXICON) == 50, f"SEED_LEXICON has {len(SEED_LEXICON)} concepts, expected 50"
for _cid, _entries in SEED_LEXICON.items():
    assert len(_entries) == 7, f"Concept '{_cid}' has {len(_entries)} entries, expected 7"
