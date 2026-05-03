"""
bank_mount.py -- mount the OperatorMemoryBank on CK's engine + Flask
endpoints.  Loaded after grammar_lm_mount in ck_boot_api.py.

Endpoints:
    POST /grammar/retrieve   body {history: [int|str], k: int}
                              -> {top_k: [{sim, retrieved_next, ...}],
                                  vote: {op: count}, distribution: {op: prob}}

    POST /grammar/compare    body {history: [int|str], k: int, alpha: float}
                              -> {LM: dist, BANK: dist, ENSEMBLE: dist,
                                  diff_KL: float}

    GET  /grammar/bank_info  -> {n_entries, d_model, source_streams}
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Union, List

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


def mount(engine, app, model, streams_path: Path = None) -> bool:
    """Build the bank from training_streams.jsonl and register endpoints."""
    streams_path = streams_path or (HERE / "training_streams.jsonl")
    if not streams_path.exists():
        print(f"[CK] bank_mount: streams file not found: {streams_path}")
        return False
    bank = OperatorMemoryBank(model)
    print(f"[CK] bank_mount: building bank (this takes ~10s)...")
    bank.build_from_streams(streams_path, max_examples=20000)
    engine.operator_bank = bank
    n = bank.keys.size(0) if bank.keys is not None else 0
    print(f"[CK] bank_mount: bank ready, {n} (key, value) entries")

    from flask import jsonify, request

    @app.route('/grammar/bank_info', methods=['GET'])
    def bank_info():
        return jsonify({
            "n_entries": n,
            "d_model": model.cfg.d_model,
            "vocab": {"operators": OP_NAMES, "specials": SPECIAL_NAMES},
            "key_window_length": 5,
        })

    @app.route('/grammar/retrieve', methods=['POST'])
    def grammar_retrieve():
        body = request.get_json(silent=True) or {}
        history = body.get('history') or [SPECIAL_IDS["BOS"]]
        k = int(body.get('k', 16))
        try:
            ids = _resolve_seq(history)
        except Exception as exc:
            return jsonify({"error": str(exc)}), 400
        sims, _, vals = bank.retrieve(ids, k=k)
        from collections import Counter
        vote = Counter(int(v.item()) for v in vals)
        dist = bank.predict_next(ids, k=k)
        return jsonify({
            "history": [token_name(t) for t in ids],
            "k": k,
            "top_k": [
                {"sim": float(s), "retrieved_next": token_name(int(v.item()))}
                for s, v in zip(sims, vals)
            ],
            "vote": {token_name(t): c for t, c in vote.most_common()},
            "distribution": {
                token_name(i): float(dist[i].item())
                for i in range(VOCAB_SIZE) if float(dist[i].item()) > 0.001
            },
            "max_similarity": float(sims[0].item()) if len(sims) > 0 else 0.0,
        })

    @app.route('/grammar/compare', methods=['POST'])
    def grammar_compare():
        body = request.get_json(silent=True) or {}
        history = body.get('history') or [SPECIAL_IDS["BOS"]]
        k = int(body.get('k', 16))
        alpha = float(body.get('alpha', 0.5))
        try:
            ids = _resolve_seq(history)
        except Exception as exc:
            return jsonify({"error": str(exc)}), 400
        p_lm = lm_predict_dist(model, ids)
        p_bank = bank.predict_next(ids, k=k)
        p_ens = alpha * p_lm + (1 - alpha) * p_bank
        sims, _, _ = bank.retrieve(ids, k=k)
        max_sim = float(sims[0].item()) if len(sims) > 0 else 0.0

        def dist_dict(p):
            return {token_name(i): float(p[i].item()) for i in range(VOCAB_SIZE)
                    if float(p[i].item()) > 0.005}

        def top1(p):
            return token_name(int(p.argmax()))

        # Where do they disagree?
        diff_KL = float((p_lm * (p_lm.clamp(min=1e-9).log()
                                  - p_bank.clamp(min=1e-9).log())).sum())
        return jsonify({
            "history": [token_name(t) for t in ids],
            "max_retrieval_similarity": max_sim,
            "alpha": alpha,
            "k": k,
            "LM_top1": top1(p_lm),
            "BANK_top1": top1(p_bank),
            "ENSEMBLE_top1": top1(p_ens),
            "agree": top1(p_lm) == top1(p_bank),
            "LM_distribution": dist_dict(p_lm),
            "BANK_distribution": dist_dict(p_bank),
            "ENSEMBLE_distribution": dist_dict(p_ens),
            "KL_LM_to_BANK": diff_KL,
        })

    print("[CK] bank_mount: MOUNTED (/grammar/retrieve, /grammar/compare, "
          "/grammar/bank_info)")
    return True
