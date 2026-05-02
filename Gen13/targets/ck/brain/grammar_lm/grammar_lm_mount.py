"""
grammar_lm_mount.py -- mount ck_grammar_lm on the running engine and
expose three Flask endpoints for testing.

Endpoints:
    POST /grammar/sample      body {prefix: [int|str], n: int, temp: float, top_k: int}
                              -> {sequence: [str], sequence_ids: [int]}
    POST /grammar/score       body {sequence: [int|str]}
                              -> {log_likelihood_per_token: float, n_tokens: int}
    POST /grammar/predict     body {history: [int|str], top_k: int}
                              -> {predictions: [{op: str, prob: float}, ...]}
    GET  /grammar/info        -> {model_path, n_params, vocab_size, block_size, ...}

Engine attachment: engine.grammar_lm = GrammarLM (loaded model)
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import List, Union

# Allow import from the grammar_lm folder
_HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(_HERE))

from ck_grammar_lm import (
    GrammarLM, GrammarLMConfig, load_model,
    OP_NAMES, NAME_TO_ID, SPECIAL_NAMES, SPECIAL_IDS,
    VOCAB_SIZE, token_name,
)


def _resolve_token(tok: Union[str, int]) -> int:
    if isinstance(tok, int):
        return tok
    s = str(tok).upper().strip()
    if s in NAME_TO_ID:
        return NAME_TO_ID[s]
    if s in SPECIAL_IDS:
        return SPECIAL_IDS[s]
    raise ValueError(f"unknown token: {tok!r}")


def _resolve_seq(seq) -> List[int]:
    return [_resolve_token(t) for t in seq]


def mount(engine, app, model_path: Path = None) -> bool:
    """Load the LM, attach to engine, register endpoints. Returns True on success."""
    try:
        model = load_model(model_path)
    except Exception as exc:
        print(f"[CK] grammar_lm: load FAILED ({exc})")
        return False

    engine.grammar_lm = model
    n_params = model.n_params()
    print(f"[CK] grammar_lm: loaded {n_params:,} params, "
          f"vocab={VOCAB_SIZE}, block_size={model.cfg.block_size}, "
          f"d_model={model.cfg.d_model}, n_layer={model.cfg.n_layer}")

    from flask import jsonify, request

    @app.route('/grammar/info', methods=['GET'])
    def grammar_info():
        return jsonify({
            "vocab_size": VOCAB_SIZE,
            "operator_names": OP_NAMES,
            "special_names": SPECIAL_NAMES,
            "n_parameters": n_params,
            "block_size": model.cfg.block_size,
            "n_layer": model.cfg.n_layer,
            "d_model": model.cfg.d_model,
            "device": str(next(model.parameters()).device),
        })

    @app.route('/grammar/sample', methods=['POST'])
    def grammar_sample():
        body = request.get_json(silent=True) or {}
        prefix = body.get('prefix') or [SPECIAL_IDS["BOS"]]
        n = int(body.get('n', 16))
        temp = float(body.get('temp', 0.8))
        top_k = body.get('top_k', 5)
        if top_k is not None:
            top_k = int(top_k)
        try:
            ids = _resolve_seq(prefix)
        except Exception as exc:
            return jsonify({"error": str(exc)}), 400
        seq = model.sample(ids, n_tokens=n, temperature=temp, top_k=top_k)
        names = [token_name(t) for t in seq]
        return jsonify({
            "prefix_ids": ids,
            "sequence_ids": seq,
            "sequence": names,
            "n_new": n,
            "temperature": temp,
            "top_k": top_k,
        })

    @app.route('/grammar/score', methods=['POST'])
    def grammar_score():
        body = request.get_json(silent=True) or {}
        seq = body.get('sequence') or []
        try:
            ids = _resolve_seq(seq)
        except Exception as exc:
            return jsonify({"error": str(exc)}), 400
        if len(ids) < 2:
            return jsonify({"error": "sequence must have >=2 tokens"}), 400
        ll = model.score(ids)
        return jsonify({
            "log_likelihood_per_token": ll,
            "perplexity_per_token": float(2.71828182846 ** (-ll)),
            "n_tokens": len(ids),
            "sequence_ids": ids,
            "sequence": [token_name(t) for t in ids],
        })

    @app.route('/grammar/predict', methods=['POST'])
    def grammar_predict():
        body = request.get_json(silent=True) or {}
        history = body.get('history') or []
        top_k = int(body.get('top_k', 5))
        try:
            ids = _resolve_seq(history)
        except Exception as exc:
            return jsonify({"error": str(exc)}), 400
        preds = model.predict_next(ids, top_k=top_k)
        return jsonify({
            "history_ids": ids,
            "history": [token_name(t) for t in ids],
            "predictions": [{"op": token_name(i), "id": i, "prob": p}
                            for i, p in preds],
        })

    @app.route('/grammar/cortex_predict', methods=['GET'])
    def grammar_cortex_predict():
        """Predict next operator from CK's CURRENT cortex state.
        Reads cortex.state.last_b/last_d and feeds them to predict_next."""
        try:
            from cortex_voice import _cortex  # avoid circular; runtime ref
        except Exception:
            _cortex = None
        # Try a few ways to find the live cortex
        cortex = None
        for ref in [getattr(engine, 'cortex', None),
                    getattr(engine, '_cortex', None)]:
            if ref is not None and hasattr(ref, 'state'):
                cortex = ref
                break
        if cortex is None:
            # Best-effort: rebuild from /cortex endpoint via direct module load
            return jsonify({"error": "no live cortex on engine"}), 503
        last_b = int(getattr(cortex.state, 'last_b', 0))
        last_d = int(getattr(cortex.state, 'last_d', 0))
        history = [SPECIAL_IDS["BOS"], last_b, last_d]
        preds = model.predict_next(history, top_k=5)
        return jsonify({
            "cortex_last_pair": f"{token_name(last_b)}->{token_name(last_d)}",
            "history": [token_name(t) for t in history],
            "predictions": [{"op": token_name(i), "id": i, "prob": p}
                            for i, p in preds],
        })

    print("[CK] grammar_lm: MOUNTED (/grammar/sample, /grammar/score, "
          "/grammar/predict, /grammar/cortex_predict, /grammar/info)")
    return True
