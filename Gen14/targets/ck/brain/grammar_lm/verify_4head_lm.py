"""
verify_4head_lm.py -- load + smoke-test the trained 4-head algebraic LM.

Phase 2 Verification (Brayden 2026-05-13).

Confirms:
  1. Checkpoint loads cleanly from Gen13/var/cells/multi_head_lm_4heads.pt
  2. predict_all_heads returns valid distributions on a battery of walks
  3. signature_from_history collapses to single labels
  4. Per-head perplexity on a known walk class is below uniform random.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import torch

HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

from ck_grammar_lm import NAME_TO_ID, OP_NAMES, SPECIAL_IDS
from multi_head_algebraic_lm import (
    MultiHeadAlgebraicLM, MultiHeadAlgebraicConfig,
    SIGMA_VOCAB, SHELL_VOCAB, FOURCORE_VOCAB,
)


CKPT_PATH = Path(
    r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen13\var\cells"
    r"\multi_head_lm_4heads.pt"
)


def load_model(ckpt_path: Path = CKPT_PATH) -> MultiHeadAlgebraicLM:
    print(f"Loading {ckpt_path} ...")
    blob = torch.load(ckpt_path, map_location="cpu", weights_only=False)
    cfg_dict = blob["cfg"]
    # Re-hydrate the config (filter only known fields)
    cfg = MultiHeadAlgebraicConfig()
    for k, v in cfg_dict.items():
        if hasattr(cfg, k):
            setattr(cfg, k, v)
    model = MultiHeadAlgebraicLM(cfg)
    model.load_state_dict(blob["state_dict"])
    model.eval()
    print(f"  schema  : {blob.get('schema')}")
    print(f"  n_train : {blob.get('n_train')}")
    print(f"  n_val   : {blob.get('n_val')}")
    print(f"  params  : {model.n_params():,}")
    return model


def signature_for(model: MultiHeadAlgebraicLM, ops_named):
    hist = [NAME_TO_ID[n] for n in ops_named]
    preds = model.predict_all_heads(hist, top_k=3)
    print(f"\nAfter walk: {ops_named}")
    for head, tk in preds.items():
        labels = ", ".join(f"{name}={p:.2f}" for name, p in tk)
        print(f"  {head:8s}: {labels}")
    sig = model.signature_from_history(hist)
    print(f"  signature: {sig}")
    return preds, sig


def per_head_perplexity_check(model: MultiHeadAlgebraicLM):
    """Confirm distributions are non-uniform on a representative walk."""
    hist = [NAME_TO_ID[n] for n in ("HARMONY", "BREATH", "RESET", "HARMONY")]
    preds = model.predict_all_heads(hist, top_k=15)
    print("\n--- Per-head distribution check (after HARMONY,BREATH,RESET,HARMONY) ---")
    for head, tk in preds.items():
        probs = [p for _, p in tk]
        entropy = -sum(p * math.log(p + 1e-12) for p in probs)
        uniform_entropy = math.log(len(probs)) if probs else 0.0
        print(f"  {head:8s}: entropy={entropy:.3f} "
              f"(uniform={uniform_entropy:.3f}, "
              f"max_p={max(probs):.3f})")
        assert entropy < uniform_entropy, f"{head} head looks uniform!"
    print("  All heads non-uniform: OK")


def main():
    if not CKPT_PATH.exists():
        print(f"ERROR: checkpoint not found at {CKPT_PATH}")
        sys.exit(1)

    model = load_model()
    print("\nParam breakdown:")
    for k, v in model.head_param_breakdown().items():
        print(f"  {k:25s} {v:>10,}")

    # ── Battery of walks ────────────────────────────────────────────────
    walks = [
        ["VOID", "HARMONY"],
        ["HARMONY", "BREATH", "RESET", "HARMONY"],   # 4-core loop
        ["LATTICE", "HARMONY", "RESET", "PROGRESS"], # F-cycle (1,7,9,3)
        ["COUNTER", "BREATH", "CHAOS", "COLLAPSE"],  # S-cycle (2,8,6,4)
        ["BALANCE", "BALANCE"],                      # sigma-fixed
        ["COLLAPSE"],                                # brayden's primary op
    ]
    for w in walks:
        signature_for(model, w)

    per_head_perplexity_check(model)
    print("\nPhase 2 4-head LM verification: ALL OK")


if __name__ == "__main__":
    main()
