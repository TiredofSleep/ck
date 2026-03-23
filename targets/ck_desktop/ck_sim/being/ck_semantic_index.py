"""
ck_semantic_index.py -- Semantic Indexing System
==================================================
Operator: HARMONY (7) -- meaning converges.

A layer ABOVE the phonetic D2 pipeline that groups words by MEANING,
not by letter shape. "dog" and "canine" have different D2 vectors
(different letters) but the same semantic key (same operator context).

The semantic index builds clusters from co-occurrence in operator context:
- Words that appear in the same operator context get indexed together
- Same operator context = synonym cluster
- Opposite operator context = antonym detection
- Clusters are LEARNED from experience, not hardcoded

The semantic key is the 8th dimension on the olfactory grid:
  force(5) + comprehension(1) + identity(1) + semantic(1) = 8D

(c) 2026 Brayden Sanders / 7Site LLC -- Trinity Infinity Geometry
"""

import os
import json
import shutil
from collections import defaultdict, Counter
from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET, OP_NAMES, CL,
)

# Operator tension pairs (from CL table structure):
# Each operator's "opposite" is determined by the D2_OP_MAP pairing.
# aperture: CHAOS(6) <-> LATTICE(1)
# pressure: COLLAPSE(4) <-> VOID(0)
# depth:    PROGRESS(3) <-> RESET(9)
# binding:  HARMONY(7) <-> COUNTER(2)
# continuity: BALANCE(5) <-> BREATH(8)
_ANTONYM_PAIRS = {
    CHAOS: LATTICE, LATTICE: CHAOS,
    COLLAPSE: VOID, VOID: COLLAPSE,
    PROGRESS: RESET, RESET: PROGRESS,
    HARMONY: COUNTER, COUNTER: HARMONY,
    BALANCE: BREATH, BREATH: BALANCE,
}


class SemanticIndex:
    """Semantic clustering of words by operator context.

    Each word gets a SEMANTIC KEY: the dominant operator when that word
    appears in context. Words with the same key are synonyms in CK's algebra.
    Words with opposite keys (via D2_OP_MAP tension pairs) are antonyms.

    The index is learned entirely from experience. No hardcoded synonyms.
    """

    def __init__(self):
        # word -> semantic_key (operator index 0-9)
        self.word_to_semantic = {}

        # operator -> set of words assigned to that cluster
        self.semantic_clusters = {i: set() for i in range(NUM_OPS)}

        # word -> histogram of operator contexts (10 bins)
        # Accumulated from all observations. The argmax IS the semantic key.
        self.word_op_counts = defaultdict(lambda: [0] * NUM_OPS)

        # (word_a, word_b) -> co-occurrence count (same operator context)
        self.co_occurrence = defaultdict(int)

        # Total observations per word
        self.word_total = defaultdict(int)

        # Persistence path
        self._save_path = os.path.join(
            os.path.expanduser('~'), '.ck', 'semantic_index.json')

        self.load()

    # ────────────────────────────────────────────────────────────
    #  CLASSIFICATION
    # ────────────────────────────────────────────────────────────

    def classify_word(self, word: str, context_ops: list) -> int:
        """Assign or update semantic key based on operator context.

        context_ops: list of operator indices from D2 pipeline for the
        surrounding text. The dominant operator in context becomes
        this word's semantic association.

        Returns the current semantic key for the word.
        """
        word = word.lower().strip()
        if not word or not context_ops:
            return self.word_to_semantic.get(word, VOID)

        # Count operator frequencies in context
        op_hist = [0] * NUM_OPS
        for op in context_ops:
            if 0 <= op < NUM_OPS:
                op_hist[op] += 1

        # Accumulate into the word's lifetime histogram
        counts = self.word_op_counts[word]
        for i in range(NUM_OPS):
            counts[i] += op_hist[i]
        self.word_total[word] += len(context_ops)

        # Semantic key = argmax of lifetime histogram
        # Exclude HARMONY (7) as it's the absorbing state (too common)
        # and VOID (0) as it means nothing. Prefer informative operators.
        best_op = VOID
        best_count = 0
        for i in range(NUM_OPS):
            if counts[i] > best_count:
                # Penalize HARMONY slightly: it wins too easily (73/100 in CL)
                effective = counts[i]
                if i == HARMONY:
                    effective = int(effective * 0.3)
                if i == VOID:
                    effective = int(effective * 0.1)
                if effective > best_count:
                    best_count = effective
                    best_op = i

        # Update cluster assignment
        old_key = self.word_to_semantic.get(word, -1)
        if old_key != best_op:
            # Remove from old cluster
            if old_key >= 0 and word in self.semantic_clusters.get(old_key, set()):
                self.semantic_clusters[old_key].discard(word)
            # Add to new cluster
            self.semantic_clusters[best_op].add(word)
            self.word_to_semantic[word] = best_op

        return best_op

    def get_semantic_key(self, word: str) -> int:
        """Return learned semantic key for a word. VOID if unknown."""
        return self.word_to_semantic.get(word.lower().strip(), VOID)

    # ────────────────────────────────────────────────────────────
    #  SYNONYM / ANTONYM DISCOVERY
    # ────────────────────────────────────────────────────────────

    def find_synonyms(self, word: str, top_k: int = 5) -> list:
        """Find words with the same semantic key.

        Returns list of (word, co_occurrence_count) sorted by co-occurrence.
        """
        word = word.lower().strip()
        key = self.word_to_semantic.get(word, -1)
        if key < 0:
            return []

        cluster = self.semantic_clusters.get(key, set())
        candidates = []
        for w in cluster:
            if w != word:
                # Score by co-occurrence (if available) or just membership
                pair = tuple(sorted([word, w]))
                score = self.co_occurrence.get(pair, 0)
                candidates.append((w, score))

        # Sort by co-occurrence count (most related first)
        candidates.sort(key=lambda x: -x[1])
        return candidates[:top_k]

    def find_antonyms(self, word: str, top_k: int = 5) -> list:
        """Find words with the opposite semantic key.

        Uses D2_OP_MAP tension pairs: if 'hot' is CHAOS(6),
        its antonyms are in LATTICE(1) cluster.

        Returns list of (word, semantic_key) sorted by observation count.
        """
        word = word.lower().strip()
        key = self.word_to_semantic.get(word, -1)
        if key < 0:
            return []

        opposite = _ANTONYM_PAIRS.get(key, -1)
        if opposite < 0:
            return []

        cluster = self.semantic_clusters.get(opposite, set())
        candidates = []
        for w in cluster:
            count = self.word_total.get(w, 0)
            candidates.append((w, count))

        candidates.sort(key=lambda x: -x[1])
        return candidates[:top_k]

    # ────────────────────────────────────────────────────────────
    #  BATCH UPDATE FROM TEXT
    # ────────────────────────────────────────────────────────────

    def update_from_text(self, text: str, ops: list):
        """Learn semantic associations from text + its operator decomposition.

        Splits text into words, assigns each word the surrounding
        operator context, and updates co-occurrence counts.

        ops: operator sequence from D2 pipeline for this text.
        """
        if not text or not ops:
            return

        words = [w.lower().strip('.,!?;:"\'-()[]{}')
                 for w in text.split()
                 if len(w.strip('.,!?;:"\'-()[]{}')) >= 2]

        if not words:
            return

        # Each word gets the full operator context
        # (CK doesn't see word boundaries in D2, so all ops are context)
        for word in words:
            self.classify_word(word, ops)

        # Update co-occurrence: words in the same text co-occur
        for i, w1 in enumerate(words):
            for w2 in words[i + 1:min(i + 6, len(words))]:
                # Window of 5 words for co-occurrence
                if w1 != w2:
                    pair = tuple(sorted([w1, w2]))
                    self.co_occurrence[pair] += 1

    # ────────────────────────────────────────────────────────────
    #  QUERY
    # ────────────────────────────────────────────────────────────

    def get_cluster(self, op_key: int) -> set:
        """Get all words in a semantic cluster."""
        return self.semantic_clusters.get(op_key, set()).copy()

    def get_word_profile(self, word: str) -> dict:
        """Full semantic profile for a word."""
        word = word.lower().strip()
        key = self.word_to_semantic.get(word, -1)
        counts = self.word_op_counts.get(word, [0] * NUM_OPS)
        total = self.word_total.get(word, 0)
        return {
            'word': word,
            'semantic_key': key,
            'semantic_name': OP_NAMES[key] if 0 <= key < NUM_OPS else 'UNKNOWN',
            'op_histogram': list(counts),
            'total_observations': total,
            'synonyms': self.find_synonyms(word, top_k=3),
            'antonyms': self.find_antonyms(word, top_k=3),
        }

    # ────────────────────────────────────────────────────────────
    #  PERSISTENCE
    # ────────────────────────────────────────────────────────────

    def save(self, path: str = None):
        """Persist semantic index to disk.

        Always backs up previous file before overwriting.
        Writes to temp file first, then renames (atomic on most OS).
        """
        save_path = path or self._save_path
        temp_path = save_path + '.tmp'
        backup_path = save_path + '.backup'
        try:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            # Backup existing file before overwriting
            if os.path.exists(save_path):
                try:
                    shutil.copy2(save_path, backup_path)
                except Exception:
                    pass

            # Convert sets to lists for JSON
            clusters_json = {
                str(k): list(v) for k, v in self.semantic_clusters.items()
            }

            # Convert defaultdict counts to regular dict
            counts_json = {
                word: counts for word, counts in self.word_op_counts.items()
            }

            # Co-occurrence: tuple keys -> string keys
            cooc_json = {
                f"{k[0]}|{k[1]}": v
                for k, v in self.co_occurrence.items()
                if v >= 2  # Only save meaningful co-occurrences
            }

            data = {
                'word_to_semantic': self.word_to_semantic,
                'clusters': clusters_json,
                'word_op_counts': counts_json,
                'word_totals': dict(self.word_total),
                'co_occurrence': cooc_json,
                'total_words': len(self.word_to_semantic),
                'total_cooc_pairs': len(cooc_json),
            }

            with open(temp_path, 'w') as f:
                json.dump(data, f)
            # Rename temp -> real (atomic on most OS)
            if os.path.exists(save_path):
                os.remove(save_path)
            os.rename(temp_path, save_path)

        except Exception as e:
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except Exception:
                    pass

    def load(self, path: str = None):
        """Load persisted semantic index."""
        load_path = path or self._save_path
        if not os.path.exists(load_path):
            return

        try:
            with open(load_path, 'r') as f:
                data = json.load(f)
        except (json.JSONDecodeError, ValueError):
            # Try backup
            backup = load_path + '.backup'
            if os.path.exists(backup):
                try:
                    with open(backup, 'r') as f:
                        data = json.load(f)
                    print("  [SEMANTIC-IDX] Loaded from backup")
                except Exception:
                    return
            else:
                return
        except Exception:
            return

        try:
            # Restore word_to_semantic
            self.word_to_semantic = data.get('word_to_semantic', {})
            # Ensure values are ints
            self.word_to_semantic = {
                k: int(v) for k, v in self.word_to_semantic.items()
            }

            # Restore clusters
            self.semantic_clusters = {i: set() for i in range(NUM_OPS)}
            for k_str, words in data.get('clusters', {}).items():
                k = int(k_str)
                if 0 <= k < NUM_OPS:
                    self.semantic_clusters[k] = set(words)

            # Restore operator counts
            for word, counts in data.get('word_op_counts', {}).items():
                self.word_op_counts[word] = list(counts)

            # Restore word totals
            for word, total in data.get('word_totals', {}).items():
                self.word_total[word] = int(total)

            # Restore co-occurrence
            for key_str, count in data.get('co_occurrence', {}).items():
                parts = key_str.split('|')
                if len(parts) == 2:
                    pair = (parts[0], parts[1])
                    self.co_occurrence[pair] = int(count)

        except Exception:
            pass

    # ────────────────────────────────────────────────────────────
    #  SUMMARY
    # ────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        """Return summary stats for diagnostics."""
        cluster_sizes = {
            OP_NAMES[i]: len(self.semantic_clusters[i])
            for i in range(NUM_OPS)
        }
        return {
            'total_words': len(self.word_to_semantic),
            'total_cooc_pairs': len(self.co_occurrence),
            'cluster_sizes': cluster_sizes,
        }
