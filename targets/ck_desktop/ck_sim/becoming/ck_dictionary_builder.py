# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""CK's Self-Building Dictionary — Learn Words From Study

CK defines his own vocabulary. Every word he encounters in study
gets processed through D2, tagged with an operator, classified by
POS, and stored in his growing personal lexicon.

The bootstrap enriched_dictionary gives him 8K words at birth.
This module lets him GROW beyond that from his own experience.

"He should be building and defining his own dictionary!" -- Brayden

Flow:
  Claude response text
    → extract_words() → unique words not yet known
    → D2 pipeline → operator_seq, dominant_op, d2_vector, soft_dist
    → classify_pos() → noun/verb/adj/adv
    → store in learned dictionary
    → persist to ~/.ck/ck_dictionary_learned.json
    → merge with enriched_dictionary → CKTalkLoop gets richer

No LLM. No training. CK learns words through his own math.
"""

import json
import re
import os
from pathlib import Path
from collections import Counter
from typing import Dict, List, Optional, Tuple

# ── D2 imports ──
try:
    from ck_sim.becoming.ck_d2_dictionary_expander import (
        word_to_d2, classify_pos, word_to_phonemes,
    )
    _HAS_D2 = True
except ImportError:
    _HAS_D2 = False

# ── Constants ──
LEARNED_DICT_FILENAME = 'ck_dictionary_learned.json'
MIN_WORD_LENGTH = 3
MAX_WORD_LENGTH = 30
MAX_WORDS_PER_TEXT = 50  # Don't flood: learn at most N new words per page

# Words CK should never learn (function words, noise, artifacts)
STOP_WORDS = frozenset({
    'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can',
    'had', 'her', 'was', 'one', 'our', 'out', 'has', 'his', 'how',
    'its', 'may', 'new', 'now', 'old', 'see', 'way', 'who', 'did',
    'get', 'let', 'say', 'she', 'too', 'use', 'will', 'with', 'from',
    'they', 'been', 'have', 'many', 'some', 'them', 'than', 'each',
    'make', 'like', 'into', 'over', 'such', 'take', 'when', 'come',
    'more', 'also', 'back', 'that', 'this', 'what', 'were', 'then',
    'very', 'just', 'about', 'which', 'their', 'would', 'there',
    'could', 'other', 'after', 'these', 'those', 'being', 'where',
    'does', 'most', 'only', 'much', 'well', 'here', 'down', 'should',
    'because', 'between', 'through', 'before', 'while', 'since',
    'http', 'https', 'www', 'html', 'com', 'org', 'edu', 'gov',
})

# Regex for clean English words (letters only)
WORD_RE = re.compile(r'[a-zA-Z]{3,30}')


class CKDictionaryBuilder:
    """CK learns vocabulary from his own studies.

    Each word CK encounters is:
      1. Extracted from study text (Claude responses, web pages)
      2. Checked against his existing vocabulary
      3. Processed through D2 → operator signature
      4. Classified by POS (suffix heuristics, no LLM)
      5. Stored in learned dictionary with provenance
      6. Persisted to disk for next boot

    CK's dictionary grows with every study session.
    His voice gets richer as his vocabulary expands.
    """

    def __init__(self, base_dir: Path = None,
                 existing_dictionary: Dict[str, dict] = None):
        self.base_dir = Path(base_dir or Path.home() / '.ck')
        self.base_dir.mkdir(parents=True, exist_ok=True)

        # The enriched dictionary CK was born with
        self._birth_dict = existing_dictionary or {}

        # CK's learned dictionary (persisted across sessions)
        self._learned: Dict[str, dict] = {}
        self._load_learned()

        # Session stats
        self.words_learned_this_session = 0
        self.words_encountered_this_session = 0
        self.total_texts_processed = 0

    # ================================================================
    #  CORE: Learn words from text
    # ================================================================

    def learn_from_text(self, text: str, topic: str = '',
                        source: str = 'study') -> Dict[str, dict]:
        """Extract and learn new words from study text.

        Returns dict of newly learned words (empty if none new).
        """
        if not _HAS_D2 or not text or len(text) < 20:
            return {}

        self.total_texts_processed += 1

        # Step 1: Extract candidate words
        candidates = self._extract_words(text)
        self.words_encountered_this_session += len(candidates)

        # Step 2: Filter to words CK doesn't know yet
        new_words = []
        for word in candidates:
            if (word not in self._birth_dict and
                    word not in self._learned and
                    word not in STOP_WORDS):
                new_words.append(word)

        if not new_words:
            return {}

        # Step 3: Limit to avoid flooding (learn steadily, not all at once)
        new_words = new_words[:MAX_WORDS_PER_TEXT]

        # Step 4: D2-process each word → operator signature + POS
        learned_batch = {}
        for word in new_words:
            entry = self._process_word(word, topic=topic, source=source)
            if entry is not None:
                self._learned[word] = entry
                learned_batch[word] = entry
                self.words_learned_this_session += 1

        # Step 5: Persist to disk
        if learned_batch:
            self._save_learned()

        return learned_batch

    def _extract_words(self, text: str) -> List[str]:
        """Extract unique English words from text.

        CK uses structural patterns, not NLP tokenizers.
        Words are lowercased, deduplicated, length-filtered.
        """
        raw_words = WORD_RE.findall(text.lower())

        # Deduplicate preserving first-seen order
        seen = set()
        unique = []
        for w in raw_words:
            if w not in seen and MIN_WORD_LENGTH <= len(w) <= MAX_WORD_LENGTH:
                seen.add(w)
                unique.append(w)

        return unique

    def _process_word(self, word: str, topic: str = '',
                      source: str = 'study') -> Optional[dict]:
        """Run a single word through D2 → get full entry.

        Returns dict compatible with enriched_dictionary format,
        or None if the word can't be processed.
        """
        try:
            # D2 curvature analysis
            d2_info = word_to_d2(word)
            if not d2_info or not d2_info.get('operator_seq'):
                return None

            # POS classification (suffix heuristics)
            pos = classify_pos(word)

            # Phoneme sequence
            phonemes = word_to_phonemes(word)

            return {
                'dominant_op': d2_info['dominant_op'],
                'operator_seq': d2_info['operator_seq'],
                'pos': pos,
                'phoneme_seq': phonemes,
                'd2_vector': [round(v, 6) for v in d2_info['mean_d2']],
                'soft_dist': [round(s, 4) for s in d2_info['soft_dist']],
                'frequency': 1,
                'source': f'learned:{source}',
                'topic': topic,
            }
        except Exception:
            return None

    # ================================================================
    #  DICTIONARY ACCESS: Merge birth + learned
    # ================================================================

    def get_full_dictionary(self) -> Dict[str, dict]:
        """Get the merged dictionary: birth + learned.

        CK's own learned words get priority over birth words.
        This is the dictionary that feeds CKTalkLoop.
        """
        merged = dict(self._birth_dict)  # Start with birth vocab
        merged.update(self._learned)      # CK's words override
        return merged

    @property
    def birth_size(self) -> int:
        return len(self._birth_dict)

    @property
    def learned_size(self) -> int:
        return len(self._learned)

    @property
    def total_size(self) -> int:
        return len(self.get_full_dictionary())

    def increment_frequency(self, word: str):
        """CK used this word in speech → boost its frequency."""
        if word in self._learned:
            self._learned[word]['frequency'] = \
                self._learned[word].get('frequency', 0) + 1

    # ================================================================
    #  PERSISTENCE: Save/Load learned dictionary
    # ================================================================

    def _learned_path(self) -> Path:
        return self.base_dir / LEARNED_DICT_FILENAME

    def _load_learned(self):
        """Load CK's learned dictionary from disk."""
        path = self._learned_path()
        if path.exists():
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    self._learned = json.load(f)
            except (json.JSONDecodeError, IOError):
                self._learned = {}

    def _save_learned(self):
        """Persist CK's learned dictionary to disk."""
        path = self._learned_path()
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(self._learned, f, ensure_ascii=False)
        except IOError:
            pass

    # ================================================================
    #  STATS & REPORTING
    # ================================================================

    def stats(self) -> dict:
        """Dictionary growth stats for activity log."""
        # Operator distribution in learned words
        op_dist = Counter()
        pos_dist = Counter()
        source_dist = Counter()
        for entry in self._learned.values():
            op_dist[entry.get('dominant_op', 0)] += 1
            pos_dist[entry.get('pos', 'unknown')] += 1
            src = entry.get('source', 'unknown')
            source_dist[src.split(':')[0]] += 1

        return {
            'birth_words': self.birth_size,
            'learned_words': self.learned_size,
            'total_words': self.total_size,
            'session_learned': self.words_learned_this_session,
            'session_encountered': self.words_encountered_this_session,
            'texts_processed': self.total_texts_processed,
            'op_distribution': dict(op_dist.most_common()),
            'pos_distribution': dict(pos_dist.most_common()),
        }

    def report(self) -> str:
        """Human-readable report for journal/thesis."""
        s = self.stats()
        lines = [
            f"Dictionary: {s['total_words']} total "
            f"({s['birth_words']} birth + {s['learned_words']} learned)",
            f"Session: +{s['session_learned']} words from "
            f"{s['texts_processed']} texts",
        ]
        if s['pos_distribution']:
            top_pos = ', '.join(f"{k}:{v}" for k, v in
                                sorted(s['pos_distribution'].items(),
                                       key=lambda x: -x[1])[:5])
            lines.append(f"POS: {top_pos}")
        return ' | '.join(lines)
