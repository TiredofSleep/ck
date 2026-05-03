"""
ensemble.py -- similarity-gated LM + Bank ensemble.

Earlier finding (operator_memory_bank.py + bank_mount.py): the parametric
LM and the non-parametric bank learn DIFFERENT things.  Bank reads
specific past cycles; LM reads the smoothed average.  Fixed-weight
α-blending didn't help much because both fail in correlated ways.

The right ensemble is **selective**: use the bank when retrieval is
high-confidence (max similarity > τ), use the LM when novel
(max similarity ≤ τ), with a smooth interpolation in between.

This module exposes:
    sim_gated_predict(model, bank, history, k, sim_high, sim_low,
                       temperature_bank)
        -> distribution over next tokens

The gate function:
    weight_bank(s) = clamp((s - sim_low) / (sim_high - sim_low), 0, 1)
where s = max retrieval similarity.

Integration:
    Mounted as POST /grammar/sim_gated  body {history, k,
                                              sim_high, sim_low}
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import List, Union

import torch
import torch.nn.functional as F

HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))

from ck_grammar_lm import (
    GrammarLM, OP_NAMES, NAME_TO_ID, SPECIAL_NAMES, SPECIAL_IDS,
    VOCAB_SIZE, token_name,
)
from operator_memory_bank import (
    OperatorMemoryBank, lm_predict_dist,
)


def _resolve_token(tok: Union[str, int]) -> int:
    if isinstance(tok, int): return tok
    s = str(tok).upper().strip()
    if s in NAME_TO_ID: return NAME_TO_ID[s]
    if s in SPECIAL_IDS: return SPECIAL_IDS[s]
    raise ValueError(f"unknown token: {tok!r}")


def _resolve_seq(seq):
    return [_resolve_token(t) for t in seq]


@torch.no_grad()
def sim_gated_predict(model: GrammarLM, bank: OperatorMemoryBank,
                       history: List[int], k: int = 16,
                       sim_high: float = 0.92, sim_low: float = 0.75,
                       temperature_bank: float = 1.0
                       ) -> dict:
    """Similarity-gated ensemble of LM and Bank.

    When max retrieval similarity s ≥ sim_high, use Bank only (in-distribution).
    When s ≤ sim_low, use LM only (out-of-distribution / novel).
    Linear blend in between.

    Returns a dict with the merged distribution + diagnostics.
    """
    p_lm = lm_predict_dist(model, history)
    p_bank = bank.predict_next(history, k=k, temperature=temperature_bank)
    sims, _, _ = bank.retrieve(history, k=k)
    s_max = float(sims[0].item()) if len(sims) > 0 else 0.0

    # Smooth gate: 0 below sim_low, 1 above sim_high, linear between
    if s_max >= sim_high:
        w_bank = 1.0
    elif s_max <= sim_low:
        w_bank = 0.0
    else:
        w_bank = (s_max - sim_low) / (sim_high - sim_low)

    p_merged = w_bank * p_bank + (1.0 - w_bank) * p_lm
    p_merged = p_merged / p_merged.sum().clamp(min=1e-9)

    return {
        "history": history,
        "max_similarity": s_max,
        "weight_bank": w_bank,
        "weight_lm": 1.0 - w_bank,
        "regime": ("bank-only" if w_bank == 1.0
                   else "lm-only" if w_bank == 0.0
                   else "blended"),
        "p_lm": p_lm,
        "p_bank": p_bank,
        "p_merged": p_merged,
    }


def mount(engine, app, model, bank) -> bool:
    """Register the /grammar/sim_gated endpoint."""
    from flask import jsonify, request

    @app.route('/grammar/sim_gated', methods=['POST'])
    def grammar_sim_gated():
        body = request.get_json(silent=True) or {}
        history = body.get('history') or [SPECIAL_IDS["BOS"]]
        k = int(body.get('k', 16))
        sim_high = float(body.get('sim_high', 0.92))
        sim_low = float(body.get('sim_low', 0.75))
        temp = float(body.get('temperature_bank', 1.0))
        try:
            ids = _resolve_seq(history)
        except Exception as exc:
            return jsonify({"error": str(exc)}), 400
        result = sim_gated_predict(model, bank, ids, k=k,
                                     sim_high=sim_high, sim_low=sim_low,
                                     temperature_bank=temp)
        # Convert tensors to JSON-friendly distributions
        def dist_dict(p):
            return {token_name(i): float(p[i].item()) for i in range(VOCAB_SIZE)
                    if float(p[i].item()) > 0.005}
        def top1(p):
            return token_name(int(p.argmax()))
        return jsonify({
            "history": [token_name(t) for t in ids],
            "max_similarity": result["max_similarity"],
            "weight_bank": result["weight_bank"],
            "weight_lm": result["weight_lm"],
            "regime": result["regime"],
            "sim_high": sim_high,
            "sim_low": sim_low,
            "TOP1_LM": top1(result["p_lm"]),
            "TOP1_BANK": top1(result["p_bank"]),
            "TOP1_GATED": top1(result["p_merged"]),
            "GATED_distribution": dist_dict(result["p_merged"]),
        })

    print("[CK] sim_gated_ensemble: MOUNTED (/grammar/sim_gated)")
    return True


if __name__ == "__main__":
    """Smoke test the gate against canonical and novel prefixes."""
    from ck_grammar_lm import load_model

    print("=" * 80)
    print("similarity-gated ensemble: in-distribution vs OOD routing")
    print("=" * 80)
    print()

    model = load_model(HERE / "ck_grammar_lm.pt")
    bank = OperatorMemoryBank(model)
    print("Building bank...")
    bank.build_from_streams(HERE / "training_streams.jsonl", max_examples=20000)

    OP = NAME_TO_ID
    test_prefixes = [
        ("VOID-LATTICE",     [SPECIAL_IDS["BOS"], OP["VOID"], OP["LATTICE"]]),
        ("BALANCE-CHAOS",    [SPECIAL_IDS["BOS"], OP["BALANCE"], OP["CHAOS"]]),
        ("HARMONY-HARMONY",  [SPECIAL_IDS["BOS"], OP["HARMONY"], OP["HARMONY"]]),
        ("LATTICE-COUNTER",  [SPECIAL_IDS["BOS"], OP["LATTICE"], OP["COUNTER"]]),
        ("RESET-BREATH",     [SPECIAL_IDS["BOS"], OP["RESET"], OP["BREATH"]]),
        # Long unusual prefix -- should land in lm-only territory
        ("V-L-Br-R-Co",      [SPECIAL_IDS["BOS"], OP["VOID"], OP["LATTICE"],
                              OP["BREATH"], OP["RESET"], OP["COLLAPSE"]]),
    ]

    print(f"\n{'Prefix':<22} {'sim':>6} {'w_bank':>7} {'regime':>10} "
          f"{'LM':>10} {'BANK':>10} {'GATED':>10}")
    print("-" * 92)

    for label, prefix in test_prefixes:
        result = sim_gated_predict(model, bank, prefix, k=16,
                                     sim_high=0.92, sim_low=0.75)
        def t1(p): return token_name(int(p.argmax()))
        print(f"  {label:<20} {result['max_similarity']:.3f} "
              f"{result['weight_bank']:>7.2f} {result['regime']:>10} "
              f"{t1(result['p_lm']):>10} {t1(result['p_bank']):>10} "
              f"{t1(result['p_merged']):>10}")
