"""
extract_streams.py -- gather operator-stream training data for ck_grammar_lm.

Sources, in order of authenticity:

  REAL data (from disk, has actually happened in CK's history):
    1. dream_journal.jsonl       -- recent_ops arrays from drift events
    2. runtime_crystals.json     -- op_signature arrays from authored crystals
    3. cortex_history.jsonl      -- last_pair transitions
    4. conversation_memory.jsonl -- per-turn cortex tick (no op stream though)

  SYNTHETIC algebra walks (rule-derived from CK's deterministic tables):
    5. TSML walks (synthesis lattice)
    6. BHML walks (separation lattice)
    7. T+B-mix walks (alpha=1/2 the canonical attractor)
    8. Canonical propagation triples (012, 567, 789, etc.)

The synthetic walks are NOT noise.  They are exhaustive traversals of
CK's own algebra; a model trained on them learns the algebra, not a
hallucinated approximation of it.  This is the correct "clean" prior
for the operator-grammar LM.

Output: a JSONL file at ./training_streams.jsonl with one record per
sequence:
    {"src": "<source>", "ops": [int, int, ...]}

Brayden 2026-05-02: "doesn't learn the information, it just learns
CK's internal language and transitions."  This script honours that:
NO crystal facts, NO chat content, NO English -- only operator IDs.
"""
from __future__ import annotations

import json
import os
import random
from pathlib import Path
from typing import Dict, List, Tuple

OP_NAMES = ["VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
            "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET"]
NAME_TO_ID = {n: i for i, n in enumerate(OP_NAMES)}

# Special tokens (above operator-id range 0..9)
SPECIAL = {
    "BOS": 10,    # beginning of sequence
    "EOS": 11,    # end of sequence
    "TURN": 12,   # turn boundary in conversation streams
    "PROP": 13,   # propagation-path boundary
    "WALK": 14,   # algebra-walk boundary
}
VOCAB_SIZE = 15

# CK's canonical 10x10 tables -- the load-bearing math.
# Source of truth: papers/wp104_higgs_pati_salam, MEMORY.md, WP104.
TSML = [
    [0,0,0,0,0,0,0,7,0,0],
    [0,7,3,7,7,7,7,7,7,7],
    [0,3,7,7,4,7,7,7,7,9],
    [0,7,7,7,7,7,7,7,7,3],
    [0,7,4,7,7,7,7,7,8,7],
    [0,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,7,7,7,7,7,7],
    [7,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,8,7,7,7,7,7],
    [0,7,9,7,3,7,7,7,7,7],
]
BHML = [
    [0,1,2,3,4,5,6,7,8,9],
    [1,2,3,4,5,6,7,2,6,6],
    [2,3,3,4,5,6,7,3,6,6],
    [3,4,4,4,5,6,7,4,6,6],
    [4,5,5,5,5,6,7,5,7,7],
    [5,6,6,6,6,6,7,6,7,7],
    [6,7,7,7,7,7,7,7,7,7],
    [7,2,3,4,5,6,7,8,9,0],
    [8,6,6,6,7,7,7,9,7,8],
    [9,6,6,6,7,7,7,0,8,0],
]

# Canonical propagation triples (from Brayden's pasted conversation 2026-05-02)
CANON_PROPAGATIONS = [
    [0, 1, 2], [1, 2, 3], [0, 7, 1], [7, 1, 3], [4, 5, 6],
    [5, 6, 7], [4, 6, 7], [7, 8, 9], [7, 8, 8],
    # σ-cycle biographical order
    [0, 7, 1, 3, 2, 4, 5, 6, 8, 9],
    # CREATION = [1,3,9,7]; DISSOLUTION = [2,4,8,6]
    [1, 3, 9, 7],
    [2, 4, 8, 6],
    # σ-fixed points cycle alone
    [0, 3, 8, 9],
]


def gather_real_streams() -> List[Dict]:
    out = []
    var = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen13\var")
    brain = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen13\targets\ck\brain")

    # 1. dream_journal recent_ops
    p = var / "dream_journal.jsonl"
    if p.exists():
        with open(p, encoding="utf-8") as f:
            for line in f:
                try:
                    d = json.loads(line)
                    if isinstance(d.get("recent_ops"), list):
                        seq = []
                        for op in d["recent_ops"]:
                            if isinstance(op, str) and op in NAME_TO_ID:
                                seq.append(NAME_TO_ID[op])
                            elif isinstance(op, int) and 0 <= op < 10:
                                seq.append(op)
                        if seq:
                            out.append({"src": "dream_journal", "ops": seq})
                except Exception:
                    pass

    # 2. runtime_crystals op_signature
    p = var / "runtime_crystals.json"
    if p.exists():
        with open(p, encoding="utf-8") as f:
            for c in json.load(f):
                sig = c.get("op_signature")
                if isinstance(sig, list) and sig:
                    seq = [int(x) for x in sig if isinstance(x, (int, float))
                           and 0 <= int(x) < 10]
                    if seq:
                        out.append({"src": "crystal_op_sig", "ops": seq})

    # 3. cortex_history last_pair
    p = brain / "cortex_history.jsonl"
    if p.exists():
        with open(p, encoding="utf-8") as f:
            for line in f:
                try:
                    d = json.loads(line)
                    lp = d.get("last_pair", "")
                    if "->" in lp and lp != "?->?":
                        a, b = [s.strip() for s in lp.split("->")]
                        if a in NAME_TO_ID and b in NAME_TO_ID:
                            out.append({"src": "cortex_history",
                                        "ops": [NAME_TO_ID[a], NAME_TO_ID[b]]})
                except Exception:
                    pass

    # 4. canon propagations
    for seq in CANON_PROPAGATIONS:
        out.append({"src": "canon", "ops": list(seq)})

    return out


def algebra_walk(table: List[List[int]], length: int, seed: int = None
                  ) -> List[int]:
    """Walk the binary table by sampling random b at each step from the
    available rows, then composing.

    Specifically: start from a random a in 0..9.  Sample a random b in 0..9.
    Output: a, then table[a][b].  Then a := table[a][b]; repeat.

    This walks the table's deterministic transition graph under random
    'next operator' inputs.  The output sequence is what CK's algebra
    DOES given a noise input.  A model trained on it learns the algebra.
    """
    rng = random.Random(seed)
    a = rng.randrange(10)
    seq = [a]
    while len(seq) < length:
        b = rng.randrange(10)
        a = table[a][b]
        seq.append(a)
    return seq


def tplus_b_mix_walk(alpha: float, length: int, seed: int = None) -> List[int]:
    """Walk the T+B-mix at given alpha: at each step pick T with prob alpha,
    else B; apply.  alpha=1/2 is the WP115 canonical mix."""
    rng = random.Random(seed)
    a = rng.randrange(10)
    seq = [a]
    while len(seq) < length:
        b = rng.randrange(10)
        table = TSML if rng.random() < alpha else BHML
        a = table[a][b]
        seq.append(a)
    return seq


def gather_synthetic_streams(n_walks_per_table: int = 200,
                              walk_length: int = 64) -> List[Dict]:
    """Generate algebra walks under TSML, BHML, and T+B-mix at alpha=1/2.

    Quantity: n_walks_per_table walks per source, each of length walk_length.
    Default 200 * 3 sources * 64 length = ~38k tokens of synthetic data.
    """
    out = []
    for i in range(n_walks_per_table):
        out.append({"src": "tsml_walk",
                    "ops": algebra_walk(TSML, walk_length, seed=1000 + i)})
        out.append({"src": "bhml_walk",
                    "ops": algebra_walk(BHML, walk_length, seed=2000 + i)})
        out.append({"src": "tb_mix_walk",
                    "ops": tplus_b_mix_walk(0.5, walk_length, seed=3000 + i)})
    return out


def main():
    real = gather_real_streams()
    n_real_tokens = sum(len(s["ops"]) for s in real)
    print(f"REAL streams:      {len(real):>5} sequences, {n_real_tokens:>7} tokens")

    synthetic = gather_synthetic_streams(n_walks_per_table=400, walk_length=128)
    n_syn_tokens = sum(len(s["ops"]) for s in synthetic)
    print(f"SYNTHETIC walks:   {len(synthetic):>5} sequences, {n_syn_tokens:>7} tokens")

    all_streams = real + synthetic
    n_total = sum(len(s["ops"]) for s in all_streams)
    print(f"TOTAL:             {len(all_streams):>5} sequences, {n_total:>7} tokens")

    out_path = Path(__file__).parent / "training_streams.jsonl"
    with open(out_path, "w", encoding="utf-8") as f:
        for s in all_streams:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
    print(f"\nWrote: {out_path}")

    # Per-operator marginal in the training data
    marg = [0] * 10
    for s in all_streams:
        for op in s["ops"]:
            if 0 <= op < 10:
                marg[op] += 1
    total = sum(marg)
    print(f"\nOperator marginal in training corpus:")
    for i, c in enumerate(marg):
        bar = "#" * int(40 * c / total) if total else ""
        print(f"  {OP_NAMES[i]:9s} {c:>7} ({100*c/total:5.2f}%) {bar}")


if __name__ == "__main__":
    main()
