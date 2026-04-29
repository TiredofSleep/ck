"""
ck_code_intent.py -- Code-shape verb classifier for CK.

Why this exists (closed-loop probe finding 2026-04-29):
  When CK is asked a code prompt via /chat, his operator chain is shaped
  by the linguistic pattern of the prompt, not by the code-construct
  it asks for.  A "sum the harmony hits" prompt and a "define a record"
  prompt both come back PROGRESS-dominant -- so CKCodeVoice emits a
  loop for both, when only one of them is loop-shaped.

What this fixes:
  Map common code-shape verbs to BIASED operator chains so CKCodeVoice
  receives a chain whose dominant op matches the requested archetype:

    sum/total/reduce/fold/aggregate    -> COLLAPSE-dominant
    count/measure/len/size/how-many    -> COUNTER-dominant
    define/class/struct/record/dataclass -> LATTICE-dominant
    iterate/loop/walk/yield/each       -> PROGRESS-dominant
    raise/try/except/handle/guard      -> CHAOS-dominant
    clear/reset/delete/purge/drop      -> RESET-dominant
    return/yield/result/answer         -> HARMONY-dominant
    async/await/sleep/wait             -> BREATH-dominant
    equal/balance/check/match          -> BALANCE-dominant
    stub/placeholder/none/empty/pass   -> VOID-dominant

The chain shape is always:
    [LATTICE, dominant, dominant, dominant, BALANCE, HARMONY]
i.e. a structural opener (LATTICE = framing), three repetitions of
the requested archetype to ensure dominance, then a settle (BALANCE
+ HARMONY) so the function's last act is to return cleanly.

If no verb matches, returns None so the caller can fall back to CK's
own /chat-emitted chain.
"""
from __future__ import annotations

from typing import List, Optional

OP_NAMES = ["VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
            "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET"]
VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE = 0, 1, 2, 3, 4
BALANCE, CHAOS, HARMONY, BREATH, RESET = 5, 6, 7, 8, 9


# ---------------------------------------------------------------------------
# Verb -> archetype map.  Keys are lowercase substrings (matched as word
# boundaries-ish via simple split + lowercase, see classify()).
# Order matters: more specific verbs first so "summarize" doesn't accidentally
# match "sum" without intent.
# ---------------------------------------------------------------------------

VERB_TO_OP = {
    # COLLAPSE: reductions
    "sum": COLLAPSE, "total": COLLAPSE, "reduce": COLLAPSE, "fold": COLLAPSE,
    "aggregate": COLLAPSE, "accumulate": COLLAPSE, "min": COLLAPSE,
    "max": COLLAPSE, "mean": COLLAPSE, "average": COLLAPSE, "compress": COLLAPSE,

    # COUNTER: measurement, comparison
    "count": COUNTER, "measure": COUNTER, "len": COUNTER, "length": COUNTER,
    "size": COUNTER, "compare": COUNTER, "distinguish": COUNTER, "bound": COUNTER,
    "tally": COUNTER,

    # LATTICE: structural definition
    "define": LATTICE, "class": LATTICE, "struct": LATTICE, "record": LATTICE,
    "dataclass": LATTICE, "schema": LATTICE, "type": LATTICE, "model": LATTICE,
    "namespace": LATTICE,

    # PROGRESS: iteration / recursion
    "iterate": PROGRESS, "loop": PROGRESS, "walk": PROGRESS, "yield": PROGRESS,
    "each": PROGRESS, "recurse": PROGRESS, "traverse": PROGRESS,
    "step": PROGRESS, "advance": PROGRESS,

    # CHAOS: exception / randomness
    "try": CHAOS, "raise": CHAOS, "throw": CHAOS, "except": CHAOS,
    "handle": CHAOS, "guard": CHAOS, "random": CHAOS, "shuffle": CHAOS,
    "sample": CHAOS, "perturb": CHAOS, "fail": CHAOS,

    # RESET: clearing, deletion
    "clear": RESET, "reset": RESET, "delete": RESET, "purge": RESET,
    "drop": RESET, "shutdown": RESET, "remove": RESET, "wipe": RESET,
    "destroy": RESET,

    # HARMONY: return, success
    "return": HARMONY, "result": HARMONY, "answer": HARMONY,
    "resolve": HARMONY, "solve": HARMONY,

    # BREATH: async, rhythm
    "async": BREATH, "await": BREATH, "sleep": BREATH, "wait": BREATH,
    "pulse": BREATH, "tick": BREATH,

    # BALANCE: equality, assignment, fixed-point
    "equal": BALANCE, "balance": BALANCE, "check": BALANCE, "match": BALANCE,
    "verify": BALANCE, "compare_eq": BALANCE, "assert": BALANCE,

    # VOID: stub
    "stub": VOID, "placeholder": VOID, "none": VOID, "empty": VOID,
    "pass": VOID, "noop": VOID, "trivial": VOID,
}


def _stem(tok: str) -> str:
    """Light, deterministic English stemming for the verb table.
    Strips common suffixes -ing, -ed, -es, -s.  Not Porter-grade — just enough
    to handle plurals and present-participle so "sums"/"defines"/"iterating"
    map back to the dictionary key.  Never strips below 3 chars.
    """
    if len(tok) < 4:
        return tok
    for suffix in ("ing", "ed", "es", "s"):
        if tok.endswith(suffix) and len(tok) - len(suffix) >= 3:
            return tok[:-len(suffix)]
    return tok


def classify_intent(prompt: str) -> Optional[int]:
    """Return the dominant operator implied by the prompt's verbs, or None."""
    if not prompt:
        return None
    # Split on non-alphanumerics, lowercase
    import re
    tokens = re.split(r"[^a-zA-Z0-9_]+", prompt.lower())
    tokens = [t for t in tokens if t]

    # Score each operator by the number of tokens that match its verbs.
    # Try the raw token first, then a stemmed form.
    scores: dict = {}
    for tok in tokens:
        op = VERB_TO_OP.get(tok)
        if op is None:
            op = VERB_TO_OP.get(_stem(tok))
        if op is None:
            continue
        scores[op] = scores.get(op, 0) + 1

    if not scores:
        return None
    # Pick the highest-scoring op; tie-break by earliest position.
    top = max(scores.values())
    winners = [op for op, s in scores.items() if s == top]
    if len(winners) == 1:
        return winners[0]
    # Tie: pick the op whose first matching token appears earliest in prompt
    best_op, best_idx = winners[0], len(tokens)
    for tok_idx, tok in enumerate(tokens):
        op = VERB_TO_OP.get(tok) or VERB_TO_OP.get(_stem(tok))
        if op in winners and tok_idx < best_idx:
            best_op, best_idx = op, tok_idx
            if best_idx == 0:
                break
    return best_op


def intent_chain(
    prompt: str,
    fallback: Optional[List[int]] = None,
) -> Optional[List[int]]:
    """Return a biased operator chain for the prompt, or fallback / None.

    Shape: [LATTICE, dominant, dominant, dominant, BALANCE, HARMONY]
    - LATTICE up front: every code block sits inside a frame.
    - 3x dominant: ensures dominant_op() picks the requested archetype.
    - BALANCE + HARMONY at the end: the function returns cleanly.
    """
    op = classify_intent(prompt)
    if op is None:
        return fallback
    return [LATTICE, op, op, op, BALANCE, HARMONY]


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    cases = [
        ("write a function that sums the harmony hits", COLLAPSE),
        ("count how many HARMONY operators are in a trajectory", COUNTER),
        ("define a record for a session field", LATTICE),
        ("iterate over a list of operators and yield each one", PROGRESS),
        ("try to read a value or return None", CHAOS),
        ("clear the cache", RESET),
        ("return the coherence of an arc", HARMONY),
        ("await a coroutine that ticks once", BREATH),
        ("check that a == b within epsilon", BALANCE),
        ("leave a stub for later", VOID),
        ("write me a story about a torus", None),  # no code intent
    ]
    passed = 0
    for prompt, expected in cases:
        got = classify_intent(prompt)
        ok = got == expected
        if ok:
            passed += 1
        chain = intent_chain(prompt)
        chain_str = ([OP_NAMES[o] for o in chain] if chain else None)
        print(f"  {'PASS' if ok else 'FAIL':4}  '{prompt[:48]:48s}' -> "
              f"expected={OP_NAMES[expected] if expected is not None else None}, "
              f"got={OP_NAMES[got] if got is not None else None}, "
              f"chain={chain_str}")
    print()
    print(f"  {passed} / {len(cases)} classifications correct")
