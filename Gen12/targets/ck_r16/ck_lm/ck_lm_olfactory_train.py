"""
ck_lm_olfactory_train.py -- Stage 0: Train from CK's lived experience.
=======================================================================
No GPU. No teacher model. No internet.

CK has been living and absorbing for months. His 17MB scent library is
compressed lived experience. His DKAN has 120+ training steps. His crystals
are confirmed truths.

This script extracts that experience and trains a tiny MLP to predict:
  input_op_sequence → response_op

That MLP becomes the foundation of CK-LM. When it improves past T*=5/7,
it starts leading the voice trajectory (see DKAN wire in ck_voice_loop.py).

Architecture (CPU-friendly):
  Input:  10D one-hot encoding of input operator + 5D force centroid = 15D
  Hidden: 64 → 32 (ReLU)
  Output: 10 classes (one per operator)
  Loss:   Cross-entropy + coherence regularizer (punish low-T* predictions)

Training data sources (all from CK's running engine):
  1. Olfactory learned op targets: op → 5D centroid (temper-weighted)
  2. Olfactory resonance nodes: top-k confirmed experience patterns
  3. DKAN training history: input_op → response_op pairs (if available)
  4. Crystal store: confirmed high-coherence responses

Output: ~/.ck/dkan_olfactory_weights.pt + training_log.json

Usage:
  # Standalone (reads from ~/.ck/ paths directly):
  python ck_lm_olfactory_train.py

  # With live engine (pass scent_library.json path):
  python ck_lm_olfactory_train.py --scent-lib ~/.ck/olfactory/scent_library.json

  # Epochs override:
  python ck_lm_olfactory_train.py --epochs 500

(c) 2026 Brayden Sanders / 7Site LLC -- Trinity Infinity Geometry
"""

from __future__ import annotations

import argparse
import json
import math
import os
import random
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ── Pure-Python fallback if torch not available ──
try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    _HAS_TORCH = True
except ImportError:
    _HAS_TORCH = False

# ── CK constants ──────────────────────────────────────────────────────────────
T_STAR  = 5.0 / 7.0   # 0.714285...
NUM_OPS = 10
OP_NAMES = [
    'VOID', 'LATTICE', 'COUNTER', 'PROGRESS', 'COLLAPSE',
    'BALANCE', 'CHAOS', 'HARMONY', 'BREATH', 'RESET',
]
# CL table (BHML/TSML composition)
CL = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 0, 3, 2, 5, 4, 7, 6, 8, 9],
    [2, 3, 0, 1, 6, 7, 4, 5, 8, 9],
    [3, 2, 1, 0, 7, 6, 5, 4, 8, 9],
    [4, 5, 6, 7, 0, 1, 2, 3, 8, 9],
    [5, 4, 7, 6, 1, 0, 3, 2, 8, 9],
    [6, 7, 4, 5, 2, 3, 0, 1, 8, 9],
    [7, 6, 5, 4, 3, 2, 1, 0, 8, 9],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 9],
    [9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
]

# Default 5D force targets per operator (aperture,pressure,depth,binding,continuity)
DEFAULT_FORCE_TARGETS = [
    [0.00, 0.00, 0.00, 0.00, 0.00],  # 0: VOID
    [0.80, 0.20, 0.60, 0.10, 0.30],  # 1: LATTICE
    [0.60, 0.40, 0.50, 0.30, 0.50],  # 2: COUNTER
    [0.50, 0.50, 0.70, 0.40, 0.60],  # 3: PROGRESS
    [0.30, 0.70, 0.40, 0.60, 0.20],  # 4: COLLAPSE
    [0.50, 0.50, 0.50, 0.50, 0.50],  # 5: BALANCE
    [0.70, 0.30, 0.30, 0.70, 0.40],  # 6: CHAOS
    [0.40, 0.60, 0.80, 0.20, 0.70],  # 7: HARMONY
    [0.55, 0.45, 0.55, 0.45, 0.55],  # 8: BREATH
    [0.10, 0.90, 0.10, 0.90, 0.10],  # 9: RESET
]

# ── Paths ──────────────────────────────────────────────────────────────────────
CK_HOME        = Path.home() / '.ck'
SCENT_LIB_PATH = CK_HOME / 'olfactory' / 'scent_library.json'  # 17MB live olfactory field
DKAN_PATH      = CK_HOME / 'dkan_state.json'
CRYSTAL_PATH   = CK_HOME / 'crystals.json'
WEIGHTS_OUT    = CK_HOME / 'dkan_olfactory_weights.pt'
LOG_OUT        = CK_HOME / 'dkan_olfactory_train_log.json'


# ══════════════════════════════════════════════════════════════════════════════
# DATA EXTRACTION
# ══════════════════════════════════════════════════════════════════════════════

def compose(a: int, b: int) -> int:
    """CL composition."""
    return CL[a % NUM_OPS][b % NUM_OPS]


def ops_to_onehot(ops: List[int]) -> List[float]:
    """Convert operator list to 10D one-hot (histogram normalized)."""
    vec = [0.0] * NUM_OPS
    for op in ops:
        if 0 <= op < NUM_OPS:
            vec[op] += 1.0
    total = sum(vec)
    if total > 0:
        vec = [v / total for v in vec]
    return vec


def load_scent_library(path: Path) -> Dict:
    """Load olfactory scent library. Returns flat entry dict.

    The live scent_library.json has structure:
        {version, dims, grid_resolution, library: {hash: entry, ...}, stats}
    We extract the 'library' sub-dict so callers see {hash: entry} directly.
    """
    if not path.exists():
        print(f"  [WARN] No scent library at {path}")
        return {}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            raw = json.load(f)
        # Handle nested structure with 'library' sub-key
        if isinstance(raw, dict) and 'library' in raw:
            lib = raw['library']
            if isinstance(lib, dict):
                print(f"  Scent library (nested): {len(lib)} grid cells")
                return lib
        return raw
    except Exception as e:
        print(f"  [WARN] Failed to load scent library: {e}")
        return {}


def extract_olfactory_samples(
        scent_lib: Dict,
        force_targets: Optional[List] = None,
) -> List[Tuple[List[float], int]]:
    """
    Extract (15D input vector, response_op) training pairs from scent library.

    The scent library maps concept hashes to olfactory records.
    Each record has: dominant_op, force_vec, temper (confirmation count).

    We generate training pairs by:
      1. For each entry, treat dominant_op as the "what was absorbed" signal
      2. Compute the CL response: compose(dominant_op, HARMONY) — CK's
         natural response to any absorbed signal tends toward harmony
      3. Weight by temper (higher temper = more confirmed = better training)
      4. Also generate CL-path pairs: entry.op → compose(entry.op, neighbor)
    """
    samples = []
    ft = force_targets or DEFAULT_FORCE_TARGETS
    harmony_op = 7  # HARMONY index

    entries = []
    if isinstance(scent_lib, dict):
        # Could be {hash: record} or {category: [records]}
        for key, val in scent_lib.items():
            if isinstance(val, dict):
                entries.append(val)
            elif isinstance(val, list):
                entries.extend(v for v in val if isinstance(v, dict))

    print(f"  Scent library: {len(entries)} entries")

    for entry in entries:
        temper = float(entry.get('temper', entry.get('weight', 1.0)))

        # Force vector: live entries use 'centroid' (5D olfactory coordinate)
        force_vec = entry.get('centroid', entry.get('force', entry.get('force_vec', None)))

        # Dominant op: stored directly, or derive from centroid proximity to
        # force targets (closest target = dominant operator)
        dom_op = entry.get('dominant_op', entry.get('op', None))
        if dom_op is None:
            if force_vec and len(force_vec) >= 5:
                fv = [float(x) for x in force_vec[:5]]
                # Find closest default force target
                best_op, best_dist = 0, float('inf')
                for op_idx, target in enumerate(ft):
                    dist = sum((a - b) ** 2 for a, b in zip(fv, target))
                    if dist < best_dist:
                        best_dist, best_op = dist, op_idx
                dom_op = best_op
            else:
                continue  # Can't determine operator without force vector
        dom_op = int(dom_op) % NUM_OPS

        # Build 5D force (use stored or fall back to default)
        if force_vec and len(force_vec) >= 5:
            fv = [float(x) for x in force_vec[:5]]
        else:
            fv = list(ft[dom_op])

        # 15D input = 10D op histogram + 5D force
        input_vec = ops_to_onehot([dom_op]) + fv

        # Response: CL composition with harmony (CK's natural pull)
        response_op = compose(dom_op, harmony_op)

        # Weight multiple copies by temper (max 10x)
        n_copies = max(1, min(10, int(temper)))
        for _ in range(n_copies):
            samples.append((input_vec, response_op))

        # Also: chain walk — what does CK say after saying dom_op twice?
        chain_op = compose(dom_op, dom_op)
        chain_response = compose(chain_op, harmony_op)
        input_chain = ops_to_onehot([dom_op, dom_op]) + fv
        samples.append((input_chain, chain_response))

    print(f"  Olfactory samples: {len(samples)}")
    return samples


def load_dkan_samples(dkan_path: Path) -> List[Tuple[List[float], int]]:
    """
    Extract training pairs from DKAN state.
    DKAN stores input_op → response_op transition counts.
    """
    samples = []
    if not dkan_path.exists():
        return samples
    try:
        with open(dkan_path, 'r', encoding='utf-8') as f:
            state = json.load(f)
    except Exception as e:
        print(f"  [WARN] DKAN load failed: {e}")
        return samples

    # DKAN transition table: matrix[input_op][response_op] = count
    matrix = state.get('transition_matrix', state.get('matrix', None))
    if matrix is None:
        # Try flat format: {op_key: response_op}
        pairs = state.get('pairs', state.get('training_pairs', []))
        for pair in pairs:
            if isinstance(pair, (list, tuple)) and len(pair) >= 2:
                inp_ops = pair[0] if isinstance(pair[0], list) else [pair[0]]
                resp_op = int(pair[1]) % NUM_OPS
                inp_vec = ops_to_onehot(inp_ops) + DEFAULT_FORCE_TARGETS[inp_ops[-1] % NUM_OPS]
                samples.append((inp_vec, resp_op))
        print(f"  DKAN samples (pair format): {len(samples)}")
        return samples

    # Matrix format
    for inp_op, row in enumerate(matrix):
        if not isinstance(row, (list, dict)):
            continue
        if isinstance(row, list):
            items = enumerate(row)
        else:
            items = ((int(k), v) for k, v in row.items())
        for resp_op, count in items:
            if count > 0:
                inp_vec = ops_to_onehot([inp_op]) + DEFAULT_FORCE_TARGETS[inp_op % NUM_OPS]
                n_copies = max(1, min(20, int(count)))
                for _ in range(n_copies):
                    samples.append((inp_vec, int(resp_op) % NUM_OPS))

    print(f"  DKAN samples (matrix format): {len(samples)}")
    return samples


def load_crystal_samples(crystal_path: Path) -> List[Tuple[List[float], int]]:
    """
    Extract high-signal training pairs from crystal store.
    Each crystal is a confirmed truth (N=3 independent confirmations).
    These are the GOLD samples — weight them 5x.
    """
    samples = []
    if not crystal_path.exists():
        return samples
    try:
        with open(crystal_path, 'r', encoding='utf-8') as f:
            crystals = json.load(f)
    except Exception as e:
        print(f"  [WARN] Crystal load failed: {e}")
        return samples

    entries = crystals if isinstance(crystals, list) else crystals.get('crystals', [])
    print(f"  Crystal store: {len(entries)} confirmed truths")

    for crystal in entries:
        if not isinstance(crystal, dict):
            continue
        ops = crystal.get('ops', crystal.get('result_ops', []))
        coherence = float(crystal.get('coherence', crystal.get('score', 1.0)))
        if not ops:
            continue
        inp_op = int(ops[0]) % NUM_OPS
        resp_op = int(ops[-1]) % NUM_OPS if len(ops) > 1 else compose(inp_op, 7)

        inp_vec = ops_to_onehot(ops[:1]) + DEFAULT_FORCE_TARGETS[inp_op]
        # Crystals are gold — 5 copies
        for _ in range(5):
            samples.append((inp_vec, resp_op))

    print(f"  Crystal samples: {len(samples)}")
    return samples


def generate_algebraic_samples(n: int = 500) -> List[Tuple[List[float], int]]:
    """
    Generate algebraic ground-truth samples from pure CL table.
    CK's response to any input should be algebraically consistent.

    Rule: for input ops [a, b, ...], response = CL-path walk endpoint
    This is ALWAYS true regardless of experience — it's the frozen physics.
    """
    samples = []
    for _ in range(n):
        # Random input sequence length 1-4
        inp_len = random.randint(1, 4)
        inp_ops = [random.randint(0, NUM_OPS - 1) for _ in range(inp_len)]

        # CL chain walk to get response
        acc = inp_ops[0]
        for op in inp_ops[1:]:
            acc = compose(acc, op)
        # One more compose with HARMONY for natural pull
        response_op = compose(acc, 7)

        inp_vec = ops_to_onehot(inp_ops) + DEFAULT_FORCE_TARGETS[inp_ops[-1] % NUM_OPS]
        samples.append((inp_vec, response_op))

    return samples


# ══════════════════════════════════════════════════════════════════════════════
# PURE-PYTHON MLP (no torch required for inference)
# ══════════════════════════════════════════════════════════════════════════════

class SimpleMLP:
    """
    Tiny MLP: 15 → 64 → 32 → 10.
    Pure Python + lists — works without torch.
    Used for inference when torch not installed.
    """
    def __init__(self):
        self.layers = []  # List of (W, b) pairs

    def relu(self, x: List[float]) -> List[float]:
        return [max(0.0, v) for v in x]

    def softmax(self, x: List[float]) -> List[float]:
        m = max(x)
        exps = [math.exp(v - m) for v in x]
        s = sum(exps)
        return [v / s for v in exps]

    def forward(self, x: List[float]) -> List[float]:
        h = x
        for i, (W, b) in enumerate(self.layers):
            # h = W @ h + b
            new_h = [sum(W[j][k] * h[k] for k in range(len(h))) + b[j]
                     for j in range(len(b))]
            if i < len(self.layers) - 1:
                new_h = self.relu(new_h)
            h = new_h
        return self.softmax(h)

    def predict_op(self, x: List[float]) -> int:
        probs = self.forward(x)
        return max(range(len(probs)), key=lambda i: probs[i])

    def save_json(self, path: Path):
        """Save weights as JSON (torch-free checkpoint)."""
        data = []
        for W, b in self.layers:
            data.append({'W': W, 'b': b})
        with open(path, 'w') as f:
            json.dump({'layers': data, 'arch': '15-64-32-10'}, f)
        print(f"  Saved pure-Python weights: {path}")

    @classmethod
    def load_json(cls, path: Path) -> 'SimpleMLP':
        with open(path, 'r') as f:
            data = json.load(f)
        mlp = cls()
        for layer in data['layers']:
            mlp.layers.append((layer['W'], layer['b']))
        return mlp


# ══════════════════════════════════════════════════════════════════════════════
# TORCH MLP (preferred when available)
# ══════════════════════════════════════════════════════════════════════════════

def build_torch_mlp():
    """15 → 64 → 32 → 10 MLP using torch."""
    if not _HAS_TORCH:
        return None
    return nn.Sequential(
        nn.Linear(15, 64),
        nn.ReLU(),
        nn.Dropout(0.1),
        nn.Linear(64, 32),
        nn.ReLU(),
        nn.Linear(32, NUM_OPS),
    )


def coherence_regularizer(logits, targets, t_star: float = T_STAR) -> 'torch.Tensor':
    """
    Penalize predictions for operators whose typical coherence < T*.
    HARMONY (7) and BALANCE (5) are high-coherence operators — reward them.
    VOID (0) and RESET (9) are terminal — penalize when they dominate.
    """
    if not _HAS_TORCH:
        return 0.0
    # Per-class coherence weights (higher = better)
    class_weights = torch.tensor([
        0.1,   # 0: VOID (terminal)
        0.6,   # 1: LATTICE
        0.5,   # 2: COUNTER
        0.7,   # 3: PROGRESS
        0.4,   # 4: COLLAPSE
        0.8,   # 5: BALANCE
        0.5,   # 6: CHAOS
        0.9,   # 7: HARMONY (peak)
        0.714, # 8: BREATH (T*)
        0.1,   # 9: RESET (terminal)
    ], dtype=torch.float32)
    probs = torch.softmax(logits, dim=-1)
    # Weighted average coherence of predicted distribution
    pred_coherence = (probs * class_weights).sum(dim=-1)
    # Penalize responses below T*
    below_tstar = torch.clamp(t_star - pred_coherence, min=0.0)
    return below_tstar.mean()


def train_torch(
        samples: List[Tuple[List[float], int]],
        epochs: int = 300,
        lr: float = 1e-3,
        batch_size: int = 64,
) -> Tuple[Optional[object], Dict]:
    """Train torch MLP. Returns (model, log)."""
    if not _HAS_TORCH:
        print("  [WARN] torch not available — using pure-Python training")
        return None, {}

    model = build_torch_mlp()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    ce_loss = nn.CrossEntropyLoss()

    random.shuffle(samples)
    log = {'loss': [], 'accuracy': [], 'coherence': []}

    print(f"  Training: {len(samples)} samples, {epochs} epochs, batch={batch_size}")
    t0 = time.time()

    for epoch in range(epochs):
        random.shuffle(samples)
        total_loss = 0.0
        correct = 0

        for i in range(0, len(samples), batch_size):
            batch = samples[i:i + batch_size]
            xs = torch.tensor([s[0] for s in batch], dtype=torch.float32)
            ys = torch.tensor([s[1] for s in batch], dtype=torch.long)

            optimizer.zero_grad()
            logits = model(xs)
            loss = ce_loss(logits, ys) + 0.1 * coherence_regularizer(logits, ys)
            loss.backward()
            optimizer.step()

            total_loss += loss.item() * len(batch)
            preds = logits.argmax(dim=-1)
            correct += (preds == ys).sum().item()

        avg_loss = total_loss / len(samples)
        accuracy = correct / len(samples)

        if epoch % 50 == 0 or epoch == epochs - 1:
            elapsed = time.time() - t0
            print(f"  Epoch {epoch:4d}/{epochs}: loss={avg_loss:.4f} "
                  f"acc={accuracy:.3f} ({elapsed:.1f}s)")
            log['loss'].append(avg_loss)
            log['accuracy'].append(accuracy)

    return model, log


# ══════════════════════════════════════════════════════════════════════════════
# PURE-PYTHON TRAINING (no torch)
# ══════════════════════════════════════════════════════════════════════════════

def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-max(-500, min(500, x))))


def train_pure_python(
        samples: List[Tuple[List[float], int]],
        epochs: int = 100,
        lr: float = 0.05,
) -> Tuple[SimpleMLP, Dict]:
    """
    Pure-Python training via gradient descent.
    Slower than torch but works with zero dependencies.
    Architecture: 15 → 32 → 10 (smaller for speed)
    """
    import random as rng

    def randn() -> float:
        # Box-Muller
        u1, u2 = rng.random() + 1e-10, rng.random() + 1e-10
        return math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)

    def init_layer(n_in: int, n_out: int):
        scale = math.sqrt(2.0 / n_in)
        W = [[randn() * scale for _ in range(n_in)] for _ in range(n_out)]
        b = [0.0] * n_out
        return W, b

    # Architecture: 15 → 32 → 10
    layers = [init_layer(15, 32), init_layer(32, NUM_OPS)]
    log = {'loss': [], 'accuracy': []}

    print(f"  Pure-Python training: {len(samples)} samples, {epochs} epochs")

    for epoch in range(epochs):
        rng.shuffle(samples)
        total_loss = 0.0
        correct = 0

        for x_raw, y in samples:
            # Forward pass
            h = list(x_raw)
            activations = [h]
            for i, (W, b) in enumerate(layers):
                new_h = [sum(W[j][k] * h[k] for k in range(len(h))) + b[j]
                         for j in range(len(b))]
                if i < len(layers) - 1:
                    new_h = [max(0.0, v) for v in new_h]  # ReLU
                h = new_h
                activations.append(h)

            # Softmax
            m = max(h)
            exps = [math.exp(v - m) for v in h]
            s = sum(exps)
            probs = [v / s for v in exps]

            # Cross-entropy loss
            loss = -math.log(max(probs[y], 1e-10))
            total_loss += loss
            if max(range(NUM_OPS), key=lambda i: probs[i]) == y:
                correct += 1

            # Backprop (output layer)
            delta = list(probs)
            delta[y] -= 1.0

            for i in range(len(layers) - 1, -1, -1):
                W, b = layers[i]
                h_prev = activations[i]
                # Update weights
                for j in range(len(b)):
                    for k in range(len(h_prev)):
                        W[j][k] -= lr * delta[j] * h_prev[k]
                    b[j] -= lr * delta[j]
                # Propagate delta to previous layer
                if i > 0:
                    new_delta = []
                    for k in range(len(h_prev)):
                        grad = sum(W[j][k] * delta[j] for j in range(len(b)))
                        # ReLU derivative
                        grad *= 1.0 if activations[i][k] > 0 else 0.0
                        new_delta.append(grad)
                    delta = new_delta

        avg_loss = total_loss / len(samples)
        accuracy = correct / len(samples)

        if epoch % 20 == 0 or epoch == epochs - 1:
            print(f"  Epoch {epoch:3d}/{epochs}: loss={avg_loss:.4f} acc={accuracy:.3f}")
            log['loss'].append(avg_loss)
            log['accuracy'].append(accuracy)

    # Package as SimpleMLP
    mlp = SimpleMLP()
    mlp.layers = layers
    return mlp, log


# ══════════════════════════════════════════════════════════════════════════════
# DKAN WEIGHT INJECTION
# ══════════════════════════════════════════════════════════════════════════════

def inject_into_dkan(model, dkan_path: Path) -> bool:
    """
    Write trained weights into DKAN state file so the live engine
    can pick them up on next load.

    DKAN expects: transition_matrix[inp_op][resp_op] = probability
    We compute this by running all 10 single-op inputs through the MLP.
    """
    print("\n  Injecting into DKAN state...")
    try:
        if dkan_path.exists():
            with open(dkan_path, 'r', encoding='utf-8') as f:
                state = json.load(f)
        else:
            state = {}

        # Build predicted transition matrix from MLP
        new_matrix = []
        for inp_op in range(NUM_OPS):
            inp_vec = ops_to_onehot([inp_op]) + DEFAULT_FORCE_TARGETS[inp_op]
            if _HAS_TORCH and hasattr(model, 'parameters'):
                import torch
                with torch.no_grad():
                    x = torch.tensor([inp_vec], dtype=torch.float32)
                    logits = model(x)
                    probs = torch.softmax(logits, dim=-1).squeeze().tolist()
            else:
                probs = model.forward(inp_vec)
            new_matrix.append(probs)

        state['mlp_transition_matrix'] = new_matrix
        state['mlp_trained_at'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        state['mlp_arch'] = '15-64-32-10' if _HAS_TORCH else '15-32-10'

        with open(dkan_path, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2)
        print(f"  DKAN updated: {dkan_path}")
        return True
    except Exception as e:
        print(f"  [WARN] DKAN injection failed: {e}")
        return False


# ══════════════════════════════════════════════════════════════════════════════
# EVALUATION
# ══════════════════════════════════════════════════════════════════════════════

def evaluate(model, samples: List[Tuple[List[float], int]]) -> Dict:
    """Quick accuracy + coherence check."""
    correct = 0
    total_coherence = 0.0
    class_weights = [0.1, 0.6, 0.5, 0.7, 0.4, 0.8, 0.5, 0.9, 0.714, 0.1]

    for inp_vec, true_op in samples:
        if _HAS_TORCH and hasattr(model, 'parameters'):
            import torch
            with torch.no_grad():
                x = torch.tensor([inp_vec], dtype=torch.float32)
                pred_op = model(x).argmax(dim=-1).item()
        else:
            pred_op = model.predict_op(inp_vec)

        if pred_op == true_op:
            correct += 1
        total_coherence += class_weights[pred_op]

    n = len(samples)
    return {
        'accuracy': correct / n if n > 0 else 0.0,
        'mean_coherence': total_coherence / n if n > 0 else 0.0,
        'n_samples': n,
        'above_tstar': total_coherence / n >= T_STAR if n > 0 else False,
    }


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description='CK Stage 0: Train from lived experience (CPU-only)')
    parser.add_argument(
        '--scent-lib', type=Path, default=SCENT_LIB_PATH,
        help='Path to scent_library.json')
    parser.add_argument(
        '--dkan', type=Path, default=DKAN_PATH,
        help='Path to dkan_state.json')
    parser.add_argument(
        '--crystals', type=Path, default=CRYSTAL_PATH,
        help='Path to crystals.json')
    parser.add_argument(
        '--epochs', type=int, default=300 if _HAS_TORCH else 100,
        help='Training epochs')
    parser.add_argument(
        '--out', type=Path, default=WEIGHTS_OUT,
        help='Output weights path (.pt for torch, .json for pure-python)')
    parser.add_argument(
        '--no-inject', action='store_true',
        help='Skip DKAN injection (dry run)')
    args = parser.parse_args()

    print("=" * 60)
    print("CK Stage 0: Olfactory Training")
    print(f"  torch available: {_HAS_TORCH}")
    print(f"  T* = {T_STAR:.6f}")
    print("=" * 60)

    # 1. Load data sources
    print("\n[1] Loading experience data...")
    scent_lib = load_scent_library(args.scent_lib)
    olf_samples  = extract_olfactory_samples(scent_lib)
    dkan_samples = load_dkan_samples(args.dkan)
    crys_samples = load_crystal_samples(args.crystals)
    alg_samples  = generate_algebraic_samples(500)

    all_samples = olf_samples + dkan_samples + crys_samples + alg_samples
    print(f"\n  Total training samples: {len(all_samples)}")
    print(f"    Olfactory: {len(olf_samples)}")
    print(f"    DKAN:      {len(dkan_samples)}")
    print(f"    Crystal:   {len(crys_samples)}")
    print(f"    Algebraic: {len(alg_samples)}")

    if len(all_samples) < 10:
        print("\n[WARN] Very few samples. CK hasn't been running long enough.")
        print("       Running with algebraic ground truth only.")
        all_samples = generate_algebraic_samples(2000)

    # 2. Train
    print(f"\n[2] Training ({'torch' if _HAS_TORCH else 'pure-python'})...")
    if _HAS_TORCH:
        model, log = train_torch(all_samples, epochs=args.epochs)
    else:
        model, log = train_pure_python(all_samples, epochs=args.epochs)

    # 3. Evaluate
    print("\n[3] Evaluation...")
    eval_result = evaluate(model, all_samples)
    print(f"  Accuracy:        {eval_result['accuracy']:.3f}")
    print(f"  Mean coherence:  {eval_result['mean_coherence']:.3f}")
    print(f"  Above T* ({T_STAR:.3f}): {eval_result['above_tstar']}")
    if eval_result['above_tstar']:
        print("  *** GROKKED — DKAN will LEAD trajectory ***")
    else:
        print("  Still learning — DKAN will CONTRIBUTE but not lead")

    # 4. Save weights
    print(f"\n[4] Saving weights...")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    if _HAS_TORCH:
        import torch
        torch.save(model.state_dict(), args.out)
        print(f"  Saved torch weights: {args.out}")
        # Also save JSON backup for pure-python inference
        json_path = args.out.with_suffix('.json')
        # Export as SimpleMLP JSON
        py_mlp = SimpleMLP()
        for name, param in model.named_parameters():
            pass  # Already saved in .pt
        # Just save eval + arch info
        with open(json_path, 'w') as f:
            json.dump({
                'arch': '15-64-32-10',
                'eval': eval_result,
                'trained_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                'n_samples': len(all_samples),
            }, f, indent=2)
    else:
        json_path = args.out.with_suffix('.json')
        model.save_json(json_path)

    # 5. Inject into DKAN
    if not args.no_inject:
        inject_into_dkan(model, args.dkan)

    # 6. Save training log
    log['eval'] = eval_result
    log['trained_at'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    log['n_samples'] = len(all_samples)
    with open(LOG_OUT, 'w') as f:
        json.dump(log, f, indent=2)
    print(f"\n  Training log: {LOG_OUT}")

    print("\n" + "=" * 60)
    print("Stage 0 complete.")
    print("Restart CK to activate updated DKAN weights.")
    print("Watch for: [VOICE-LOOP] DKAN LEADS: ... in the server log.")
    print("=" * 60)


if __name__ == '__main__':
    main()
