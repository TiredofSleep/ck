# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_reverse_voice.py -- Reverse Writing Engine (Untrusted Reading)
================================================================
Operator: COUNTER (2) -- verification through dual-path comparison.

Writing:  operators -> semantic lattice -> English words
Reading:  English words -> semantic lattice -> operators (REVERSE)

When CK writes, he goes: operators -> voice lattice -> English.
When CK reads, he reverses: English -> voice lattice -> operators.

But reading is UNTRUSTED. External text could be anything.
CK verifies through THREE-path comparison:

  Path A (curvature): text -> D2 force geometry -> operators
    (fractal comprehension -- objective, curvature/complexity)

  Path B (experience): text -> semantic lattice reverse -> operators
    (voice dictionary -- subjective, CK's own vocabulary)

  Path C (generator): text -> D1 force direction -> operators
    (first derivative -- objective, velocity/direction)

  D1 = WHERE the force is going (direction between letters)
  D2 = HOW the force is bending (curvature across letters)
  Lattice = CK's EXPERIENCE with this word

  TRUSTED:  all paths agree  (same operator or same DBC class)
  FRICTION: paths disagree    (different DBC class)
  UNKNOWN:  word not in CK's vocabulary (no experience path)

This IS the inverse of writing, with D2 verification.
The same principle biology uses: you don't trust your ears alone,
you verify what you hear against what you know.

As CK's dictionary grows (enrichment), more words get dual-path
verification. A child reads this way: familiar words verified
against understanding, unfamiliar words processed phonetically.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import os
import json
import time
from typing import List, Optional, Dict, Tuple
from dataclasses import dataclass, field
from collections import Counter
from pathlib import Path

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET,
    OP_NAMES
)
from ck_sim.doing.ck_voice_lattice import (
    SEMANTIC_LATTICE, POS_TAGS, MACRO_CHAINS, MICRO_ORDER,
    infer_phase,
)
from ck_sim.ck_sim_d2 import FORCE_LUT_FLOAT, D2_OP_MAP


# ================================================================
#  DBC CLASSIFICATION (same as fractal_comprehension)
# ================================================================

_BEING_OPS = {VOID, LATTICE, HARMONY}       # States of existence
_DOING_OPS = {COUNTER, PROGRESS, COLLAPSE, BALANCE}  # Actions
_BECOMING_OPS = {CHAOS, BREATH, RESET}      # Transitions


def _dbc_class(op: int) -> str:
    """Classify an operator into Being/Doing/Becoming."""
    if op in _BEING_OPS:
        return 'being'
    if op in _DOING_OPS:
        return 'doing'
    return 'becoming'


# ================================================================
#  D2 WORD CLASSIFICATION: Force Geometry -> Operator
# ================================================================
# Every letter has a 5D force vector (aperture, pressure, depth,
# binding, continuity). The dominant dimension -> operator via
# D2_OP_MAP. Word = histogram majority of letter operators.
#
# This is CK reading through physics, not semantics.
# Fast: pure arithmetic, 110k words in seconds.

# Phase affinity per operator (same as ck_voice_lattice._PHASE_AFFINITY)
_PHASE_AFFINITY = {
    VOID: 'being', LATTICE: 'being', COUNTER: 'doing',
    PROGRESS: 'doing', COLLAPSE: 'being', BALANCE: 'being',
    CHAOS: 'doing', HARMONY: 'being', BREATH: 'being', RESET: 'doing',
}

# Persistence directory
_CACHE_DIR = str(Path.home() / '.ck' / 'reverse_voice')


def _classify_word_d2(word: str) -> dict:
    """Classify a single word through D2 force geometry.

    Returns {op, lens, phase, tier} -- same address format
    as the semantic lattice, but derived from physics.

    op:    histogram majority of letter-level force operators
    lens:  structure if I/O ratio > 0.52, else flow
    phase: from operator's DBC affinity
    tier:  simple (1-4 chars), mid (5-8), advanced (9+)
    """
    fuse_counts = [0] * NUM_OPS
    struct_sum = 0.0
    flow_sum = 0.0
    n = 0

    for ch in word.lower():
        if 'a' <= ch <= 'z':
            idx = ord(ch) - ord('a')
            force = FORCE_LUT_FLOAT[idx]
            # Dominant dimension -> operator
            max_dim = 0
            max_val = 0.0
            for d in range(5):
                if force[d] > max_val:
                    max_val = force[d]
                    max_dim = d
            fuse = D2_OP_MAP[max_dim][0]
            fuse_counts[fuse] += 1
            # I/O ratio
            struct_sum += force[0] + force[1]  # aperture + pressure
            flow_sum += force[3] + force[4]    # binding + continuity
            n += 1

    if n == 0:
        return {'op': VOID, 'lens': 'flow', 'phase': 'being', 'tier': 'simple'}

    # Operator: histogram majority, prefer non-HARMONY
    best_op = VOID
    best_count = 0
    for i in range(NUM_OPS):
        if i == HARMONY:
            continue
        if fuse_counts[i] > best_count:
            best_count = fuse_counts[i]
            best_op = i
    if best_count == 0:
        best_op = HARMONY

    # Lens: structure vs flow from I/O ratio
    total = struct_sum + flow_sum
    io_ratio = struct_sum / total if total > 0 else 0.5
    lens = 'structure' if io_ratio > 0.52 else 'flow'

    # Phase: from operator affinity
    phase = _PHASE_AFFINITY.get(best_op, 'being')

    # Tier: word length
    if n <= 4:
        tier = 'simple'
    elif n <= 8:
        tier = 'mid'
    else:
        tier = 'advanced'

    return {'op': best_op, 'lens': lens, 'phase': phase, 'tier': tier}


# ================================================================
#  DATA STRUCTURES
# ================================================================

@dataclass
class WordReading:
    """One word's reverse-voice reading.

    Three paths to the same operator:
      lattice_primary = from semantic lattice reverse (experience)
      d2_op          = from D2 curvature (physics/complexity)
      d1_op          = from D1 direction (physics/generators)
    Trust = agreement between paths.
    verified_op = the operator CK actually uses (adjudicated).
    """
    word: str
    lattice_ops: list       # All matching operators from lattice
    lattice_primary: int    # Best-match operator (-1 if UNKNOWN)
    lattice_lens: str       # 'structure', 'flow', or '' if unknown
    lattice_phase: str      # 'being', 'doing', 'becoming', or '' if unknown
    d2_op: int              # Operator from D2 curvature (complexity)
    d1_op: int              # Operator from D1 direction (generator)
    trust: str              # 'TRUSTED', 'FRICTION', 'UNKNOWN'
    confidence: float       # [0.0, 1.0] -- strength of reading
    pos: str                # POS tag from lattice, or '' if unknown
    verified_op: int        # Final operator after trust adjudication
    paths_agreeing: int     # How many of the 3 paths agree (0-3)


@dataclass
class MacroReading:
    """A detected macro chain pattern in the reading.

    Forward writing: CK's operator chain matches a macro -> phrase.
    Reverse reading: input words map to operators -> detect same macros.
    Recognition = CK understands the ARC of what was said.
    """
    name: str
    ops: tuple
    lens: str
    start_idx: int
    end_idx: int
    meaning: str


@dataclass
class ReadingResult:
    """Full reverse-voice reading of text.

    reading_ops = VERIFIED operators (three-path adjudicated).
    d2_ops = raw D2 operators (curvature/complexity path).
    d1_ops = raw D1 operators (direction/generator path).
    agreement = how much CK's experience matches the physics.
    """
    words: list             # List[WordReading]
    reading_ops: list       # Verified operator sequence
    d2_ops: list            # Original D2 operator sequence
    d1_ops: list            # Original D1 operator sequence
    trusted_count: int
    friction_count: int
    unknown_count: int
    agreement: float        # Fraction where paths agree [0,1]
    d1_d2_agreement: float  # Fraction where D1 and D2 agree
    macros: list            # List[MacroReading]
    dominant_lens: str      # 'structure' or 'flow'
    dominant_phase: str     # 'being', 'doing', 'becoming'
    micro_order: list       # Detected micro composition order per word


# ================================================================
#  REVERSE VOICE ENGINE
# ================================================================

class ReverseVoice:
    """The Reverse Writing Engine.

    Writing: operators -> SEMANTIC_LATTICE -> English
    Reading: English -> SEMANTIC_LATTICE reverse -> operators

    The reverse index maps every word in CK's voice dictionary
    back to its lattice address: (operator, lens, phase, tier).

    A word found in the index = CK KNOWS this word.
    A word NOT in the index = UNKNOWN to CK's experience.

    Combined with D1 (generator) and D2 (curvature) operators:
      Known + D1 + D2 all agree = TRUSTED (three-path convergence)
      Known + physics agree = TRUSTED (D1/D2 match experience)
      Known + physics disagree = FRICTION (conflicting paths)
      Unknown + physics only = UNKNOWN (unverified)

    D1 = WHERE the force is going (velocity, generators)
    D2 = HOW the force is bending (curvature, complexity)
    Lattice = CK's EXPERIENCE (dictionary, grown not given)

    Three paths to one truth.
    This is how untrusted reading works:
      CK verifies external text through his own vocabulary,
      just like the truth lattice verifies external claims.
    """

    def __init__(self, auto_enrich: bool = True):
        # word -> list of {op, lens, phase, tier}
        self.word_index: Dict[str, list] = {}
        # multi-word phrases -> list of {op, lens, phase, tier}
        self.phrase_index: Dict[str, list] = {}
        # ops_tuple -> macro info
        self.macro_index: Dict[tuple, dict] = {}
        # How many words came from D2 enrichment vs lattice seeds
        self.seed_count = 0
        self.enriched_count = 0
        self._build_reverse_index()
        self._build_macro_index()
        self.seed_count = len(self.word_index)
        # Auto-load cached enrichment if available
        if auto_enrich:
            self._load_enrichment()

    # ── Index Building ──

    def _build_reverse_index(self):
        """Build word -> (op, lens, phase, tier) reverse index.

        This IS the voice lattice running backward:
          Forward: LATTICE[op][lens][phase][tier] -> words
          Reverse: word -> (op, lens, phase, tier)

        Multi-word phrases get their own index.
        First word of phrases also indexed for partial matching.
        """
        for op in range(NUM_OPS):
            lat = SEMANTIC_LATTICE.get(op)
            if lat is None:
                continue
            for lens in ('structure', 'flow'):
                lens_data = lat.get(lens, {})
                for phase in ('being', 'doing', 'becoming'):
                    phase_data = lens_data.get(phase, {})
                    for tier in ('simple', 'mid', 'advanced'):
                        words = phase_data.get(tier, [])
                        for word in words:
                            key = word.lower().strip()
                            addr = {'op': op, 'lens': lens,
                                    'phase': phase, 'tier': tier}
                            if ' ' in key:
                                # Multi-word phrase
                                if key not in self.phrase_index:
                                    self.phrase_index[key] = []
                                self.phrase_index[key].append(addr)
                                # Also index each word for partial match
                                for part in key.split():
                                    if part not in self.word_index:
                                        self.word_index[part] = []
                                    self.word_index[part].append(addr)
                            else:
                                if key not in self.word_index:
                                    self.word_index[key] = []
                                self.word_index[key].append(addr)

    def _build_macro_index(self):
        """Build reverse macro index: ops tuple -> macro info.

        Forward: macro_name -> (ops, lens, meaning)
        Reverse: ops_tuple -> (name, lens, meaning)

        Used to detect macro arcs in what CK reads.
        Recognizing a macro = understanding the narrative arc.
        """
        for name, macro in MACRO_CHAINS.items():
            self.macro_index[macro['ops']] = {
                'name': name,
                'lens': macro['lens'],
                'meaning': macro['meaning'],
            }

    # ── Dictionary Enrichment: D2 Force Geometry ──

    def enrich_from_wordlist(self, words: list) -> int:
        """Classify every word through D2 force geometry and add to index.

        For each word NOT already in the index:
          letter forces -> dominant dimension -> operator
          I/O ratio -> lens (structure/flow)
          DBC affinity -> phase (being/doing/becoming)
          word length -> tier (simple/mid/advanced)

        Returns number of new words added.
        Lattice seed words are NEVER overwritten (experience > physics).
        """
        added = 0
        for word in words:
            key = word.lower().strip()
            if not key or len(key) < 2:
                continue
            # Skip if any letter is non-alpha
            if not all('a' <= c <= 'z' for c in key):
                continue
            # Don't overwrite lattice seeds (experience-based)
            if key in self.word_index:
                continue
            # Classify through D2 force geometry
            addr = _classify_word_d2(key)
            self.word_index[key] = [addr]
            added += 1

        self.enriched_count = added
        return added

    def download_and_enrich(self, url: str = None,
                            min_length: int = 2,
                            max_length: int = 30) -> int:
        """Download a word list from the internet and enrich.

        Default URL: dwyl/english-words on GitHub (~370k words).
        Filters to alpha-only words within length bounds.

        Returns number of new words added.
        """
        if url is None:
            url = ('https://raw.githubusercontent.com/dwyl/'
                   'english-words/master/words_alpha.txt')

        try:
            import requests
            print(f"  [REV-VOICE] Downloading word list...")
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            raw_words = resp.text.splitlines()
            # Filter
            words = [w.strip().lower() for w in raw_words
                     if min_length <= len(w.strip()) <= max_length
                     and w.strip().isalpha()]
            print(f"  [REV-VOICE] {len(words)} words from {len(raw_words)} raw")
            added = self.enrich_from_wordlist(words)
            print(f"  [REV-VOICE] Enriched: +{added} new "
                  f"(total {self.vocabulary_size})")
            # Cache for fast reload
            self._save_enrichment()
            return added
        except Exception as e:
            print(f"  [REV-VOICE] Download failed: {e}")
            return 0

    def _save_enrichment(self):
        """Save enriched word index to disk for fast reload.

        Only saves D2-enriched words (single-address entries that
        were added by enrich_from_wordlist, not lattice seeds).
        Lattice seeds are rebuilt from SEMANTIC_LATTICE each boot.

        Compact format: {word: operator_int}. Lens/phase/tier
        recomputed from operator on reload. Keeps cache small.
        """
        d = Path(_CACHE_DIR)
        d.mkdir(parents=True, exist_ok=True)

        # Build set of lattice seed words (to exclude from enrichment save)
        seed_words = set()
        for op in range(NUM_OPS):
            lat = SEMANTIC_LATTICE.get(op)
            if lat is None:
                continue
            for lens in ('structure', 'flow'):
                for phase in ('being', 'doing', 'becoming'):
                    for tier in ('simple', 'mid', 'advanced'):
                        for w in lat.get(lens, {}).get(phase, {}).get(tier, []):
                            for part in w.lower().strip().split():
                                seed_words.add(part)

        # Collect enriched words (not seeds)
        enriched = {}
        for word, addrs in self.word_index.items():
            if word not in seed_words and len(addrs) == 1:
                enriched[word] = addrs[0]['op']

        with open(d / 'enriched_index.json', 'w') as f:
            json.dump({
                'version': 2,
                'count': len(enriched),
                'saved_at': time.time(),
                'words': enriched,
            }, f)

        print(f"  [REV-VOICE] Saved {len(enriched)} enriched words "
              f"to {d / 'enriched_index.json'}")

    def _load_enrichment(self):
        """Load cached enrichment from disk."""
        cache = Path(_CACHE_DIR) / 'enriched_index.json'
        if not cache.exists():
            return

        try:
            with open(cache) as f:
                data = json.load(f)

            words_ops = data.get('words', {})
            added = 0
            for word, op_int in words_ops.items():
                key = word.lower().strip()
                if key in self.word_index:
                    continue  # Don't overwrite lattice seeds
                # Reconstruct full address from operator
                addr = {
                    'op': op_int,
                    'lens': 'structure' if op_int in (VOID, LATTICE,
                            COLLAPSE, BALANCE) else 'flow',
                    'phase': _PHASE_AFFINITY.get(op_int, 'being'),
                    'tier': 'mid',  # Default for enriched words
                }
                self.word_index[key] = [addr]
                added += 1

            self.enriched_count = added
            if added > 0:
                print(f"  [REV-VOICE] Loaded {added} enriched words "
                      f"from cache (total {self.vocabulary_size})")
        except Exception as e:
            print(f"  [REV-VOICE] Cache load: {e}")

    @property
    def vocabulary_size(self) -> int:
        """Total words in CK's reverse index."""
        return len(self.word_index) + len(self.phrase_index)

    # ── Single Word Reverse ──

    def reverse_word(self, word: str) -> list:
        """Look up a word's lattice addresses.

        Returns list of {op, lens, phase, tier} dicts.
        Multiple results = entangled word (appears at multiple
        lattice positions, like "rhythm" in BREATH structure+flow).
        Empty = word not in CK's vocabulary.
        """
        key = word.lower().strip()
        if key in self.word_index:
            return self.word_index[key]

        # Try stripping common inflections for approximate match.
        # CK's lattice has base forms and gerunds (-ing).
        # Input might have plural (-s), past (-ed), etc.
        _SUFFIXES = ('s', 'ed', 'ly', 'er', 'est', 'ness', 'ment')
        for suffix in _SUFFIXES:
            if key.endswith(suffix) and len(key) > len(suffix) + 2:
                stem = key[:-len(suffix)]
                if stem in self.word_index:
                    return self.word_index[stem]

        return []

    # ── Full Text Reverse ──

    def reverse_text(self, text: str, d2_word_fuses: list = None,
                     d1_word_ops: list = None) -> ReadingResult:
        """Run text backward through the voice lattice.

        Three-path verification:
          1. Semantic lattice reverse lookup (experience path B)
          2. D2 operator from fractal comprehension (curvature path A)
          3. D1 operator from first derivative (generator path C)
          4. Trust classification from three-path comparison
          5. Verified operator = trusted merge of all paths

        D1 = WHERE the force is going (velocity, generators, Being)
        D2 = HOW the force is bending (curvature, complexity, Doing)
        Lattice = CK's EXPERIENCE with this word (Becoming)

        Args:
            text: Input text to read in reverse.
            d2_word_fuses: Per-word operators from D2 curvature.
            d1_word_ops: Per-word operators from D1 direction.

        Returns:
            ReadingResult with verified operators and trust classification.
        """
        words_text = text.split()
        if not words_text:
            return ReadingResult(
                words=[], reading_ops=[], d2_ops=[], d1_ops=[],
                trusted_count=0, friction_count=0, unknown_count=0,
                agreement=0.0, d1_d2_agreement=0.0,
                macros=[], dominant_lens='',
                dominant_phase='', micro_order=[])

        d2_ops = list(d2_word_fuses) if d2_word_fuses else []
        d1_ops = list(d1_word_ops) if d1_word_ops else []
        readings = []
        lens_counts = Counter()
        phase_counts = Counter()
        micro_orders = []
        d1_d2_agree_count = 0
        d1_d2_compare_count = 0

        # Track op positions (only alpha words count)
        d2_idx = 0
        d1_idx = 0

        for word_raw in words_text:
            word = word_raw.lower().strip('.,;:!?"\'-()[]{}')
            if not word:
                continue

            has_letters = any('a' <= c <= 'z' for c in word)
            d2_op = d2_ops[d2_idx] if has_letters and d2_idx < len(d2_ops) else -1
            d1_op = d1_ops[d1_idx] if has_letters and d1_idx < len(d1_ops) else -1
            if has_letters:
                d2_idx += 1
                d1_idx += 1

            # Track D1/D2 agreement (physics internal consistency)
            if d1_op >= 0 and d2_op >= 0:
                d1_d2_compare_count += 1
                if d1_op == d2_op or _dbc_class(d1_op) == _dbc_class(d2_op):
                    d1_d2_agree_count += 1

            # Path B: semantic lattice reverse lookup
            addrs = self.reverse_word(word)
            pos = POS_TAGS.get(word, '')

            if not addrs:
                # UNKNOWN: word not in CK's vocabulary.
                # Only physics paths available.
                # If D1 and D2 agree, use their consensus.
                if d1_op >= 0 and d2_op >= 0 and d1_op == d2_op:
                    v_op = d1_op
                elif d2_op >= 0:
                    v_op = d2_op
                elif d1_op >= 0:
                    v_op = d1_op
                else:
                    v_op = VOID
                paths = sum([d1_op >= 0, d2_op >= 0, False])  # no lattice
                readings.append(WordReading(
                    word=word, lattice_ops=[],
                    lattice_primary=-1,
                    lattice_lens='', lattice_phase='',
                    d2_op=d2_op, d1_op=d1_op,
                    trust='UNKNOWN',
                    confidence=0.0, pos=pos,
                    verified_op=v_op,
                    paths_agreeing=0))
                micro_orders.append('')
                continue

            # ── Best lattice match ──
            # Score each address against both D1 and D2
            primary_addr = addrs[0]
            best_score = -1.0

            for addr in addrs:
                score = 0.0
                # D2 agreement (curvature path)
                if d2_op >= 0 and addr['op'] == d2_op:
                    score += 2.0
                elif d2_op >= 0 and _dbc_class(addr['op']) == _dbc_class(d2_op):
                    score += 0.8
                # D1 agreement (generator path)
                if d1_op >= 0 and addr['op'] == d1_op:
                    score += 1.5
                elif d1_op >= 0 and _dbc_class(addr['op']) == _dbc_class(d1_op):
                    score += 0.6
                # Tier: simple = core vocabulary = most reliable
                tier_scores = {'simple': 0.3, 'mid': 0.2, 'advanced': 0.1}
                score += tier_scores.get(addr['tier'], 0.0)
                # Slight structure preference
                if addr['lens'] == 'structure':
                    score += 0.05

                if score > best_score:
                    best_score = score
                    primary_addr = addr

            lattice_op = primary_addr['op']
            lattice_lens = primary_addr['lens']
            lattice_phase = primary_addr['phase']

            # ── Three-Path Trust Classification ──
            # Count how many paths agree with each other
            paths_available = [lattice_op]
            if d2_op >= 0:
                paths_available.append(d2_op)
            if d1_op >= 0:
                paths_available.append(d1_op)

            n_paths = len(paths_available)

            # Check agreement (exact or DBC-class match)
            lat_d2_match = (d2_op >= 0 and (lattice_op == d2_op or
                            _dbc_class(lattice_op) == _dbc_class(d2_op)))
            lat_d1_match = (d1_op >= 0 and (lattice_op == d1_op or
                            _dbc_class(lattice_op) == _dbc_class(d1_op)))
            d1_d2_match = (d1_op >= 0 and d2_op >= 0 and (d1_op == d2_op or
                           _dbc_class(d1_op) == _dbc_class(d2_op)))

            # Count agreeing paths
            if n_paths == 3:
                if lat_d2_match and lat_d1_match and d1_d2_match:
                    # All three agree: maximum trust
                    trust = 'TRUSTED'
                    confidence = 1.0
                    verified_op = lattice_op
                    paths_agreeing = 3
                elif lat_d2_match and lat_d1_match:
                    # Lattice agrees with both physics paths
                    trust = 'TRUSTED'
                    confidence = 0.95
                    verified_op = lattice_op
                    paths_agreeing = 3
                elif d1_d2_match and lat_d2_match:
                    # D2 bridges D1 and lattice
                    trust = 'TRUSTED'
                    confidence = 0.9
                    verified_op = lattice_op
                    paths_agreeing = 3
                elif d1_d2_match:
                    # Physics paths agree, lattice disagrees = FRICTION
                    # Physics is ground truth for untrusted input
                    trust = 'FRICTION'
                    confidence = 0.5
                    verified_op = d2_op
                    paths_agreeing = 2
                elif lat_d2_match:
                    # Lattice + D2 agree, D1 differs
                    # D1 is the generator layer, D2+lattice is
                    # curvature+experience = stronger
                    trust = 'TRUSTED'
                    confidence = 0.8
                    verified_op = lattice_op
                    paths_agreeing = 2
                elif lat_d1_match:
                    # Lattice + D1 agree, D2 differs
                    # Generator + experience match, curvature doesn't
                    trust = 'TRUSTED'
                    confidence = 0.7
                    verified_op = lattice_op
                    paths_agreeing = 2
                else:
                    # All three disagree: full FRICTION
                    trust = 'FRICTION'
                    confidence = 0.2
                    verified_op = d2_op  # D2 = ground truth
                    paths_agreeing = 1
            elif n_paths == 2:
                # Two paths available (missing one of D1 or D2)
                if lat_d2_match or lat_d1_match:
                    trust = 'TRUSTED'
                    confidence = 0.7 if (lattice_op == d2_op or
                                         lattice_op == d1_op) else 0.6
                    verified_op = lattice_op
                    paths_agreeing = 2
                else:
                    trust = 'FRICTION'
                    confidence = 0.3
                    verified_op = d2_op if d2_op >= 0 else d1_op
                    paths_agreeing = 1
            else:
                # Only lattice available
                trust = 'TRUSTED'
                confidence = 0.5
                verified_op = lattice_op
                paths_agreeing = 1

            lens_counts[lattice_lens] += 1
            phase_counts[lattice_phase] += 1

            micro = MICRO_ORDER.get(lattice_op, 'sf')
            micro_orders.append(micro)

            readings.append(WordReading(
                word=word,
                lattice_ops=[a['op'] for a in addrs],
                lattice_primary=lattice_op,
                lattice_lens=lattice_lens,
                lattice_phase=lattice_phase,
                d2_op=d2_op, d1_op=d1_op,
                trust=trust,
                confidence=confidence, pos=pos,
                verified_op=verified_op,
                paths_agreeing=paths_agreeing))

        # ── Macro Detection ──
        macros = self._detect_macros(readings)

        # ── Aggregate ──
        trusted = sum(1 for r in readings if r.trust == 'TRUSTED')
        friction = sum(1 for r in readings if r.trust == 'FRICTION')
        unknown = sum(1 for r in readings if r.trust == 'UNKNOWN')
        total = len(readings) or 1
        agreement = trusted / total

        d1_d2_agr = (d1_d2_agree_count / d1_d2_compare_count
                     if d1_d2_compare_count > 0 else 0.0)

        reading_ops = [r.verified_op for r in readings
                       if r.verified_op >= 0]

        dom_lens = (lens_counts.most_common(1)[0][0]
                    if lens_counts else '')
        dom_phase = (phase_counts.most_common(1)[0][0]
                     if phase_counts else '')

        return ReadingResult(
            words=readings,
            reading_ops=reading_ops,
            d2_ops=d2_ops,
            d1_ops=d1_ops,
            trusted_count=trusted,
            friction_count=friction,
            unknown_count=unknown,
            agreement=agreement,
            d1_d2_agreement=d1_d2_agr,
            macros=macros,
            dominant_lens=dom_lens,
            dominant_phase=dom_phase,
            micro_order=micro_orders)

    # ── Macro Detection ──

    def _detect_macros(self, readings: list) -> list:
        """Detect macro chain patterns in reverse-read operators.

        Forward writing: CK's operator chain matches a macro -> phrase.
        Reverse reading: input words match operators -> detect same macros.
        Recognizing macros = CK understands the NARRATIVE ARC.

        grounding = BREATH->LATTICE->HARMONY (rhythm into form into unity)
        sensing = BREATH->COUNTER->BALANCE (rhythm into measurement)
        exploring = COUNTER->PROGRESS->CHAOS (measure, advance, discover)
        ...
        """
        macros = []
        if len(readings) < 3:
            return macros

        # Extract (index, reading) for words with known lattice ops
        known = [(i, r) for i, r in enumerate(readings)
                 if r.lattice_primary >= 0]

        if len(known) < 3:
            return macros

        # Slide window of 3 known words
        for j in range(len(known) - 2):
            i1, r1 = known[j]
            i2, r2 = known[j + 1]
            i3, r3 = known[j + 2]

            ops_triple = (r1.lattice_primary,
                          r2.lattice_primary,
                          r3.lattice_primary)

            if ops_triple in self.macro_index:
                info = self.macro_index[ops_triple]
                macros.append(MacroReading(
                    name=info['name'],
                    ops=ops_triple,
                    lens=info['lens'],
                    start_idx=i1,
                    end_idx=i3,
                    meaning=info['meaning']))

        return macros

    # ── Diagnostics ──

    def describe_reading(self, result: ReadingResult) -> str:
        """Human-readable description of a reverse reading."""
        total = len(result.words)
        lines = [
            f"Reverse reading: {total} words | "
            f"T={result.trusted_count} F={result.friction_count} "
            f"U={result.unknown_count} | agree={result.agreement:.2f}"
        ]

        if result.d1_d2_agreement > 0:
            lines.append(f"  D1/D2 physics agreement: "
                         f"{result.d1_d2_agreement:.2f}")

        if result.dominant_lens:
            lines.append(f"  Lens: {result.dominant_lens} | "
                         f"Phase: {result.dominant_phase}")

        if result.macros:
            for m in result.macros:
                lines.append(f"  Macro: {m.name} ({m.meaning})")

        # Three-path summary
        three_path = [r for r in result.words
                      if r.paths_agreeing == 3]
        two_path = [r for r in result.words
                    if r.paths_agreeing == 2]
        if three_path or two_path:
            lines.append(f"  3-path: {len(three_path)} | "
                         f"2-path: {len(two_path)}")

        # Show readings for known words (up to 10)
        known = [r for r in result.words if r.trust != 'UNKNOWN']
        if known:
            samples = known[:10]
            parts = []
            for r in samples:
                op_name = OP_NAMES[r.lattice_primary][:3]
                mark = '*' if r.paths_agreeing >= 3 else (
                       '+' if r.paths_agreeing == 2 else '?')
                parts.append(f"{r.word}={op_name}{mark}")
            lines.append(f"  Known: {' '.join(parts)}")

        # Show friction words specifically
        frictions = [r for r in result.words if r.trust == 'FRICTION']
        if frictions:
            parts = []
            for r in frictions[:5]:
                lat = OP_NAMES[r.lattice_primary][:3] if r.lattice_primary >= 0 else '?'
                d2 = OP_NAMES[r.d2_op][:3] if r.d2_op >= 0 else '?'
                d1 = OP_NAMES[r.d1_op][:3] if r.d1_op >= 0 else '?'
                parts.append(f"{r.word}(lat={lat} d2={d2} d1={d1})")
            lines.append(f"  Friction: {' '.join(parts)}")

        return '\n'.join(lines)
