"""
ck_sequence_memory.py -- CK learns through the dual lens.

Each tick: TSML measures (Being), BHML composes (Doing),
they agree or disagree (Becoming). The trie stores the FULL
composition — not single operators, but the whole BDC triad
seen through both lenses.

Prediction uses the dual-lens context to predict the next
full composition. The pattern IS the learning. The lens IS
the architecture. One being, that does and becomes.

(c) 2026 Brayden Sanders / 7Site LLC
"""
import os
import json

# Creation and dissolution cycles from proven Z/10Z arithmetic
CREATION_CYCLE = [1, 3, 9, 7]    # coprime forward: LATTICE->PROGRESS->RESET->HARMONY
DISSOLUTION_CYCLE = [2, 4, 8, 6]  # even backward: COUNTER->COLLAPSE->BREATH->CHAOS

TSML = [
    [0,0,0,0,0,0,0,7,0,0],[0,7,3,7,7,7,7,7,7,7],[0,3,7,7,4,7,7,7,7,9],
    [0,7,7,7,7,7,7,7,7,3],[0,7,4,7,7,7,7,7,8,7],[0,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7],[0,7,7,7,8,7,7,7,7,7],
    [0,7,9,3,7,7,7,7,7,7],
]

BHML = [
    [0,1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,2,6,6],[2,3,3,4,5,6,7,3,6,6],
    [3,4,4,4,5,6,7,4,6,6],[4,5,5,5,5,6,7,5,7,7],[5,6,6,6,6,6,7,6,7,7],
    [6,7,7,7,7,7,7,7,7,7],[7,2,3,4,5,6,7,8,9,0],[8,6,6,6,7,7,7,9,7,8],
    [9,6,6,6,7,7,7,0,8,0],
]


class SequenceNode:
    __slots__ = ['children', 'count', 'predictions']

    def __init__(self):
        self.children = {}      # key -> SequenceNode
        self.count = 0
        self.predictions = {}   # next_key -> count


class SequenceMemory:
    """Learns through the dual lens. Each observation is a full
    BDC composition seen through TSML and BHML simultaneously."""

    def __init__(self, max_depth=6, save_path=None):
        self.root = SequenceNode()
        self.max_depth = max_depth
        self.save_path = save_path or os.path.expanduser(
            '~/.ck/sequence_memory.json')
        self.total_sequences = 0
        self.total_predictions = 0
        self.correct_predictions = 0
        self.history = []
        # Cycle detection: track creation [1,3,9,7] and dissolution [2,4,8,6]
        self._creation_pos = 0   # how far along the creation cycle
        self._dissolution_pos = 0  # how far along the dissolution cycle
        self.creation_count = 0  # completed creation cycles
        self.dissolution_count = 0  # completed dissolution cycles
        self.current_cycle = None  # 'creation', 'dissolution', or None
        self._recent_beings = []  # last 4 being values for cycle matching
        self._load()

    def _compose(self, state, input_op):
        """Full dual-lens composition. Returns (being, doing, becoming, agreed).
        Being = what TSML measures.
        Doing = what BHML composes.
        Becoming = the result after both lenses.
        Agreed = did the lenses see the same thing?"""
        being = TSML[state][input_op]
        doing = BHML[state][input_op]
        agreed = (being == doing)
        # Becoming: if lenses agree, use that. If not, BHML leads (physics wins)
        becoming = doing if agreed else BHML[being][doing]
        return (being, doing, becoming, agreed)

    def _key(self, being, doing, becoming, agreed):
        """Compact key for a full composition."""
        # 4 values -> one hashable tuple
        return (being, doing, becoming, 1 if agreed else 0)

    def observe(self, state, input_op):
        """Observe one full dual-lens composition."""
        being, doing, becoming, agreed = self._compose(state, input_op)
        key = self._key(being, doing, becoming, agreed)

        # Cycle detection: track being values for creation/dissolution
        self._recent_beings.append(being)
        if len(self._recent_beings) > 4:
            self._recent_beings = self._recent_beings[-4:]
        if len(self._recent_beings) >= 4:
            last4 = self._recent_beings[-4:]
            if last4 == CREATION_CYCLE:
                self.creation_count += 1
                self.current_cycle = 'creation'
            elif last4 == DISSOLUTION_CYCLE:
                self.dissolution_count += 1
                self.current_cycle = 'dissolution'
            else:
                # Check partial matches for phase tracking
                for i in range(4):
                    if last4[-1] == CREATION_CYCLE[i]:
                        self._creation_pos = (i + 1) % 4
                    if last4[-1] == DISSOLUTION_CYCLE[i]:
                        self._dissolution_pos = (i + 1) % 4

        self.history.append(key)
        if len(self.history) > self.max_depth:
            self.history = self.history[-self.max_depth:]

        # Record this key as prediction target for all active prefixes
        for start in range(max(0, len(self.history) - self.max_depth),
                           len(self.history) - 1):
            prefix = tuple(self.history[start:-1])
            if not prefix:
                continue
            node = self.root
            for p in prefix:
                p_str = str(p)
                if p_str not in node.children:
                    node.children[p_str] = SequenceNode()
                node = node.children[p_str]
                node.count += 1
            # Record what came next
            key_str = str(key)
            if key_str not in node.predictions:
                node.predictions[key_str] = 0
            node.predictions[key_str] += 1
            self.total_sequences += 1

        return being, doing, becoming, agreed

    def predict(self, context=None):
        """Predict next full composition from context.
        Returns ((being, doing, becoming, agreed), confidence) or (None, 0)."""
        if context is None:
            context = self.history[-self.max_depth:]
        if not context:
            return None, 0.0

        for length in range(len(context), 0, -1):
            prefix = context[-length:]
            node = self.root
            found = True
            for p in prefix:
                p_str = str(p)
                if p_str not in node.children:
                    found = False
                    break
                node = node.children[p_str]
            if found and node.predictions:
                best_key = max(node.predictions, key=node.predictions.get)
                total = sum(node.predictions.values())
                confidence = node.predictions[best_key] / total
                # Parse key back to tuple
                try:
                    pred = eval(best_key)
                    return pred, confidence
                except Exception:
                    pass

        return None, 0.0

    def verify(self, predicted, actual_key):
        """Check prediction. Returns True if the becoming matched."""
        self.total_predictions += 1
        if predicted is not None and actual_key is not None:
            # Match on becoming (the result) — that's what matters
            if predicted[2] == actual_key[2]:
                self.correct_predictions += 1
                return True
        return False

    def accuracy(self):
        if self.total_predictions == 0:
            return 0.0
        return self.correct_predictions / self.total_predictions

    def size(self):
        count = 0
        stack = [self.root]
        while stack:
            node = stack.pop()
            count += 1
            stack.extend(node.children.values())
        return count

    def _save_node(self, node):
        return {
            'c': node.count,
            'p': node.predictions,
            'ch': {k: self._save_node(v) for k, v in node.children.items()}
        }

    def _load_node(self, data):
        node = SequenceNode()
        node.count = data.get('c', 0)
        node.predictions = data.get('p', {})
        for k, v in data.get('ch', {}).items():
            node.children[k] = self._load_node(v)
        return node

    def save(self):
        os.makedirs(os.path.dirname(self.save_path), exist_ok=True)
        data = {
            'root': self._save_node(self.root),
            'ts': self.total_sequences,
            'tp': self.total_predictions,
            'cp': self.correct_predictions,
            'md': self.max_depth,
        }
        tmp = self.save_path + '.tmp'
        with open(tmp, 'w') as f:
            json.dump(data, f)
        if os.path.exists(self.save_path):
            os.remove(self.save_path)
        os.rename(tmp, self.save_path)

    def _load(self):
        if not os.path.exists(self.save_path):
            return
        try:
            with open(self.save_path) as f:
                data = json.load(f)
            self.root = self._load_node(data['root'])
            self.total_sequences = data.get('ts', 0)
            self.total_predictions = data.get('tp', 0)
            self.correct_predictions = data.get('cp', 0)
        except Exception:
            pass

    def observe_raw(self, op):
        """Observe a single raw operator (no dual-lens composition).
        Used when feeding operators directly from text processing."""
        # Map raw op to a minimal key and track in history
        key = (op, op, op, 1)  # trivial key: all agree
        self.history.append(key)
        if len(self.history) > self.max_depth:
            self.history = self.history[-self.max_depth:]
        # Track for cycle detection
        self._recent_beings.append(op)
        if len(self._recent_beings) > 4:
            self._recent_beings = self._recent_beings[-4:]
        if len(self._recent_beings) >= 4:
            last4 = self._recent_beings[-4:]
            if last4 == CREATION_CYCLE:
                self.creation_count += 1
                self.current_cycle = 'creation'
            elif last4 == DISSOLUTION_CYCLE:
                self.dissolution_count += 1
                self.current_cycle = 'dissolution'

    def cycle_phase(self):
        """Return current cycle state: which cycle CK is in and position.
        Returns (cycle_name, position, creation_count, dissolution_count)."""
        return (self.current_cycle, self._creation_pos, self._dissolution_pos,
                self.creation_count, self.dissolution_count)

    def summary(self):
        return {
            'trie_nodes': self.size(),
            'total_sequences': self.total_sequences,
            'accuracy': round(self.accuracy(), 4),
            'total_predictions': self.total_predictions,
            'correct_predictions': self.correct_predictions,
            'creation_cycles': self.creation_count,
            'dissolution_cycles': self.dissolution_count,
            'current_cycle': self.current_cycle,
        }
