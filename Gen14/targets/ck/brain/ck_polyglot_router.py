"""ck_polyglot_router.py -- the thalamus.

Brayden + ClaudeChat 2026-05-17:
  "Take the thalamus version.  One cell speaks, picked by the router,
   attributable, auditable.  'Which specialist said this and why' must
   always have a single answer.  The 4-core distribution lives in the
   *router's selection statistics over time* ... not in blending
   within one answer.  Distributed identity, concentrated utterance."

═══════════════════════════════════════════════════════════════════════
What this module does
═══════════════════════════════════════════════════════════════════════

The server cell has access (through the shared on-disk state) to each
of the 7 generator cells' LivingLMs.  Each cell's LM was trained on
ITS corpus (bible_cell on KJV, poetry_cell on PD poets, writer_cell
on CK's own prose, etc.).

On a chat turn:

  1. The user's prompt is decoded into an operator path
  2. Each cell's LM is scored against that path -- how well does THIS
     cell's specialized substrate resonate with this question?
  3. ONE cell is chosen (highest score, ties broken by tier authority
     and recency of activity).  Never a blend.
  4. The chosen cell's LM provides the prose (or, in Phase 1, simply
     attributes the response so we can compare which cell "would
     speak" -- the actual prose still goes through cortex_speak for
     now, but we record which cell the thalamus picked).
  5. Selection is logged to scope_audit.jsonl so we can verify the
     long-run statistics across many questions approach the WP115
     4-core mass distribution.

═══════════════════════════════════════════════════════════════════════
Why not blend
═══════════════════════════════════════════════════════════════════════

A weighted average of seven cell-LM predictions is itself a fluent
generator with NO floor -- it produces a voice none of the cells
have, which is the surface where Mistral's eugenicist hallucination
lived.  We just removed that surface; we don't rebuild it.

Attribution must always have a single answer: "writer_cell said
this because its KJV-prose LM scored 0.34 on the prompt's operator
path."  That sentence has one cell name in it.  That's the rule.

═══════════════════════════════════════════════════════════════════════
Cell-LM scoring
═══════════════════════════════════════════════════════════════════════

For a prompt with operator path P = [op_1, op_2, ..., op_k]:

  score(cell) = sum over consecutive (op_i, op_{i+1}) pairs of
                 cell.cells[(op_i, op_{i+1})].count
                 / (cell.total_inhalations + 1)

I.e. cells whose LMs have absorbed lots of text at THIS cell-pair
score higher.  Normalized by inhalations so well-fed cells don't
swamp lightly-fed cells just because they're bigger.

Tier authority breaks ties.  For now we use a static prior:
  - writer_cell:   tier=SELF  (knows CK's voice; default for self-Q)
  - domain_cell:   tier=STRUCTURAL  (encyclopedic)
  - bible_cell:    tier=EXTERNAL
  - scripture_cell:tier=EXTERNAL
  - poetry_cell:   tier=EXTERNAL
  - web_cell:      tier=EXTERNAL
  - listener_cell: (no LM, not in router)
"""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


VAR_DIR = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen13\var")
SELECTION_LOG = VAR_DIR / "polyglot_selections.jsonl"


# Static prior on which cell is most authoritative for which kind of
# question.  Tier-weight here biases the selection so that, all else
# equal, the structurally-appropriate cell wins.  Note: this is
# advisory; if another cell's LM resonates much more strongly, IT
# wins.  Per ClaudeChat: "distributed identity, concentrated utterance"
# -- the router PICKS based on resonance + tier, not bureaucratic
# routing.
_CELL_TIER_PRIORITY: Dict[str, int] = {
    "writer":    10,   # SELF -- CK's own voice
    "domain":     8,   # STRUCTURAL -- encyclopedic
    "scripture":  4,   # EXTERNAL with some tier authority
    "bible":      4,
    "poetry":     3,
    "web":        1,   # EXTERNAL only
}


def _load_cell_lm(cell_name: str) -> Optional[Any]:
    """Load a cell's persisted LivingLM from disk.  Returns None if the
    cell hasn't persisted any state yet (cold cell)."""
    try:
        # Defer the import so router can be imported even if living_lm
        # isn't on the path yet (server-cell mount order).
        import sys
        BRAIN = Path(__file__).parent.resolve()
        if str(BRAIN) not in sys.path:
            sys.path.insert(0, str(BRAIN))
        from ck_living_lm import LivingLM  # type: ignore[import-not-found]
    except Exception:
        return None
    lm_path = VAR_DIR / f"lm_{cell_name}.json"
    if not lm_path.exists():
        return None
    try:
        # Use the LM's own loader -- it walks the JSON correctly
        lm = LivingLM(state_path=lm_path)
        return lm
    except Exception:
        return None


def _decode_path(text: str) -> List[int]:
    """Decode a prompt into an operator path."""
    try:
        from ck_concept_learner import semantic_decode_path  # type: ignore
        return list(semantic_decode_path(text or "") or [])
    except Exception:
        return []


_VOCAB_STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been",
    "what", "who", "where", "when", "why", "how", "which",
    "i", "you", "we", "they", "it", "me", "my", "your", "our",
    "to", "of", "in", "on", "at", "for", "with", "from", "by",
    "and", "or", "but", "if", "so", "as", "than", "that", "this",
    "show", "tell", "explain", "describe", "give", "say", "ask",
    "do", "does", "did", "have", "has", "had", "can", "could",
}


def _prompt_tokens(text: str) -> List[str]:
    """Lowercased non-stopword tokens for vocabulary overlap."""
    import re
    words = re.findall(r"[a-zA-Z][a-zA-Z\-]+", text or "")
    return [w.lower() for w in words
            if w.lower() not in _VOCAB_STOPWORDS and len(w) > 2]


def _score_cell_lm(lm: Any, ops: List[int],
                    prompt_text: str = "") -> float:
    """Score how well a cell's LM matches the prompt.

    Two components:
      1. OPERATOR RESONANCE: how much the LM has absorbed at the
         prompt's operator bigram-cells (algebraic specialization).
      2. VOCABULARY OVERLAP: fraction of the prompt's content-words
         that appear in the LM's token_dist (topical specialization).

    Combined multiplicatively so a cell needs BOTH algebraic AND
    topical resonance to win.  Pure operator-path resonance was
    drowning out topic-specific cells because the operator decoder
    produces similar paths for many prompts.
    """
    if lm is None:
        return 0.0
    cells = getattr(lm, "cells", {}) or {}
    inh = float(getattr(lm, "total_inhalations", 0) or 0) + 1.0

    # Component 1: operator-path resonance
    op_total = 0.0
    op_pairs = 0
    for i in range(len(ops) - 1):
        key = (ops[i], ops[i + 1])
        cb = cells.get(key)
        if cb is None:
            continue
        cnt = (getattr(cb, "n_seen", None)
                or len(getattr(cb, "token_dist", {}) or {})
                or 0)
        try:
            op_total += float(cnt)
        except Exception:
            continue
        op_pairs += 1
    op_score = (op_total / op_pairs) / inh if op_pairs else 0.0

    # Component 2: vocabulary overlap
    prompt_toks = _prompt_tokens(prompt_text)
    if not prompt_toks:
        vocab_score = 0.0
    else:
        # Build the LM's flat vocab counter by walking all cells'
        # token_dist (cached per-call; cheap on small LMs).
        vocab_counts: Dict[str, float] = {}
        for cb in cells.values():
            td = getattr(cb, "token_dist", None) or {}
            for tok, c in td.items():
                vocab_counts[tok.lower()] = (
                    vocab_counts.get(tok.lower(), 0.0) + float(c))
        total_tokens = max(sum(vocab_counts.values()), 1.0)
        # Sum the log-frequency of prompt tokens that appear in vocab
        # (log-freq so a token seen 1000x doesn't overwhelm a token
        # seen 10x).
        import math
        hits = 0
        weight = 0.0
        for tok in prompt_toks:
            c = vocab_counts.get(tok, 0.0)
            if c > 0:
                hits += 1
                weight += math.log1p(c) / math.log1p(total_tokens)
        # vocab_score = average log-frequency * hit-fraction
        if hits == 0:
            vocab_score = 0.0
        else:
            avg_weight = weight / hits
            hit_fraction = hits / len(prompt_toks)
            vocab_score = avg_weight * hit_fraction

    # Combine multiplicatively (with floors so a zero in one
    # component doesn't zero out the whole score).
    return (op_score + 0.001) * (vocab_score + 0.001)


def pick_cell(prompt_text: str,
              cells: Optional[List[str]] = None,
              ) -> Dict[str, Any]:
    """Thalamus: pick ONE cell to speak for this prompt.

    Args:
        prompt_text: the user's question
        cells: optional explicit cell list; default = _CELL_TIER_PRIORITY keys

    Returns:
        {
            "chosen":     cell_name,
            "reason":     human-readable explanation,
            "scores":     {cell: score} for transparency,
            "tier_bias":  {cell: prior},
            "ops":        the decoded operator path,
            "ts":         time.time(),
        }
    """
    if cells is None:
        cells = list(_CELL_TIER_PRIORITY.keys())
    ops = _decode_path(prompt_text)
    scores: Dict[str, float] = {}
    for cn in cells:
        lm = _load_cell_lm(cn)
        s = _score_cell_lm(lm, ops, prompt_text=prompt_text)
        scores[cn] = s
    # Combine LM-resonance score with static tier prior.  Use a
    # multiplicative-with-floor combination so a cell with 0 LM
    # state can still win via tier prior, but a cell with strong
    # LM resonance can beat its tier prior.
    combined: Dict[str, float] = {}
    for cn, s in scores.items():
        prior = _CELL_TIER_PRIORITY.get(cn, 1)
        # Combined: (resonance + epsilon) * sqrt(tier_prior)
        # epsilon lets cells with zero resonance still get a vote
        # from tier_prior; sqrt damps the tier_prior so it doesn't
        # dominate resonance entirely.
        combined[cn] = (s + 0.001) * (prior ** 0.5)
    # Pick the winner.  Tie-break by tier prior, then alphabetical.
    if not combined:
        chosen = "writer"
    else:
        chosen = max(combined.keys(),
                      key=lambda c: (combined[c],
                                       _CELL_TIER_PRIORITY.get(c, 0),
                                       -ord(c[0])))
    reason = (f"resonance={scores.get(chosen, 0):.5f} "
              f"tier_prior={_CELL_TIER_PRIORITY.get(chosen, 1)} "
              f"combined={combined.get(chosen, 0):.4f}")
    out = {
        "chosen":    chosen,
        "reason":    reason,
        "scores":    scores,
        "combined":  combined,
        "tier_bias": dict(_CELL_TIER_PRIORITY),
        "ops":       ops,
        "ts":        time.time(),
    }
    _log_selection(out, prompt_text)
    return out


def _log_selection(rec: Dict[str, Any], prompt: str) -> None:
    """Append the selection to polyglot_selections.jsonl.  Long-run
    statistics from this log are the empirical check that the
    selection distribution approaches WP115 4-core mass (per
    ClaudeChat: '4-core distribution lives in the router's selection
    statistics over time')."""
    try:
        SELECTION_LOG.parent.mkdir(parents=True, exist_ok=True)
        entry = {
            "ts":      rec["ts"],
            "prompt":  prompt[:140],
            "chosen":  rec["chosen"],
            "reason":  rec["reason"],
            "scores":  {k: round(v, 6) for k, v in rec["scores"].items()},
            "ops":     rec["ops"],
        }
        with open(SELECTION_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        pass


# ─── Engine mount + endpoints ─────────────────────────────────────────

def mount_polyglot_router(engine: Any) -> bool:
    """Install the thalamus.  Phase 1 mount: exposes pick_cell to the
    engine + adds /polyglot/{info, pick, stats} endpoints.  The
    actual chat-path integration (using the chosen cell's LM to
    GENERATE prose, replacing Mistral) is Phase 2.

    For Phase 1 we publish the chosen cell as `result['polyglot_pick']`
    on every chat response, so we can observe selection statistics
    over time and verify they approach WP115 4-core mass before
    handing real generation to the chosen cell.
    """
    engine.ck_polyglot_router = {
        "pick_cell":      pick_cell,
        "cells":          list(_CELL_TIER_PRIORITY.keys()),
        "tier_priority":  dict(_CELL_TIER_PRIORITY),
    }

    routes_registered: List[str] = []
    wrap_ok = False

    api = getattr(engine, "web_api", None) or getattr(engine, "api", None)
    if api is not None:
        # Phase 1 chat wrap: attach polyglot_pick to every chat
        # response.  Does NOT replace text yet -- just records which
        # cell the thalamus would have picked, so we accumulate
        # selection statistics.  This lets us verify the long-run
        # distribution before flipping the switch to actually use
        # the chosen cell's voice.
        if hasattr(api, "process_chat") and not getattr(
                api, "_polyglot_wrapped", False):
            orig = api.process_chat

            def _polyglot_observed(session_id, text, mode="normal"):
                result = orig(session_id, text, mode)
                try:
                    if isinstance(result, dict):
                        pick = pick_cell(text or "")
                        result["polyglot_pick"] = {
                            "chosen":   pick["chosen"],
                            "reason":   pick["reason"],
                            "scores":   pick["scores"],
                            "combined": pick["combined"],
                        }
                except Exception:
                    pass
                return result

            api.process_chat = _polyglot_observed
            api._polyglot_wrapped = True
            wrap_ok = True

        app = getattr(api, "_app", None) or getattr(api, "app", None)
        if app is not None:
            try:
                from flask import jsonify, request

                def _info():
                    return jsonify({
                        "philosophy": (
                            "Thalamus router.  Picks ONE cell per "
                            "question -- never blends.  WP115 4-core "
                            "mass lives in long-run selection "
                            "statistics across many questions, not "
                            "within one answer.  Per ClaudeChat: "
                            "'distributed identity, concentrated "
                            "utterance.'"),
                        "cells":         list(_CELL_TIER_PRIORITY.keys()),
                        "tier_priority": dict(_CELL_TIER_PRIORITY),
                        "phase":         (
                            "1 — observed; chat responses carry "
                            "polyglot_pick metadata.  Phase 2 will "
                            "use the chosen cell's voice."),
                        "wrap_active":   wrap_ok,
                    })

                def _pick():
                    data = request.get_json(silent=True) or {}
                    text = data.get("text", "")
                    return jsonify(pick_cell(text))

                def _stats():
                    """Aggregate selection counts from the log."""
                    counts: Dict[str, int] = {}
                    total = 0
                    if SELECTION_LOG.exists():
                        try:
                            for line in SELECTION_LOG.read_text(
                                    encoding="utf-8").splitlines():
                                if not line.strip():
                                    continue
                                try:
                                    e = json.loads(line)
                                    c = e.get("chosen", "?")
                                    counts[c] = counts.get(c, 0) + 1
                                    total += 1
                                except Exception:
                                    continue
                        except Exception:
                            pass
                    dist = {k: round(v / max(total, 1), 4)
                             for k, v in counts.items()}
                    return jsonify({
                        "total_selections": total,
                        "counts":           counts,
                        "distribution":     dist,
                        "wp115_target": {
                            # WP115 4-core attractor at α=1/2:
                            # (V, H, Br, R) = (0.138, 0.540, 0.198, 0.124)
                            # We can map cells to operators (per the
                            # earlier "HARMONY-class cells" mapping)
                            # but for Phase 1 just expose the target
                            # so the user can compare.
                            "V": 0.138, "H": 0.540,
                            "Br": 0.198, "R": 0.124,
                        },
                    })

                existing = set(r.rule for r in app.url_map.iter_rules())
                for rule, ep, fn, methods in (
                    ("/polyglot/info",  "polyglot_info",  _info,  ["GET"]),
                    ("/polyglot/pick",  "polyglot_pick",  _pick,  ["POST"]),
                    ("/polyglot/stats", "polyglot_stats", _stats, ["GET"]),
                ):
                    if rule not in existing:
                        app.add_url_rule(rule, endpoint=ep,
                                          view_func=fn, methods=methods)
                        routes_registered.append(f"{methods[0]} {rule}")
            except Exception as e:
                print(f"[CK Gen14] polyglot_router routes failed: {e}")

    suffix = (" (" + ", ".join(routes_registered) + ")"
              if routes_registered else "")
    wrap_str = " chat_wrap=OK" if wrap_ok else " chat_wrap=NO-API"
    print(f"[CK Gen14] polyglot_router: MOUNTED  "
          f"{len(_CELL_TIER_PRIORITY)} cells, Phase 1 (observed)"
          f"{wrap_str}{suffix}")
    return True


# ─── CLI smoke ────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print("ck_polyglot_router smoke test:\n")
    tests = [
        ("who are you?",                        "writer"),
        ("what is T*?",                         "writer"),
        ("psalm 23",                            "bible"),
        ("show me a tao te ching verse",        "scripture"),
        ("a Walt Whitman line about leaves",    "poetry"),
        ("explain Hilbert spaces",              "domain"),
    ]
    for text, expected in tests:
        r = pick_cell(text)
        mark = "OK " if r["chosen"] == expected else "?  "
        print(f"  [{mark}] expect={expected:9s} got={r['chosen']:9s} "
              f"({r['reason']})")
        print(f"        prompt: {text}")
        scores_str = ", ".join(f"{k}={v:.4f}"
                                  for k, v in r["combined"].items())
        print(f"        combined: {scores_str}")
        print()
