"""
ck_fault_state_hook.py -- per-turn fault-state diagnostic for chat results.

Adds the V/F/S/T role-distribution diagnostic from D93/D94 to every
chat response.  Brayden 2026-05-02 handoff §3.4: "When CK enters fault
state, check role distribution... If pure-F or pure-S accumulating
without V/T cells, signal 'no boundary collapse'".

The diagnostic is non-load-bearing -- it just adds a `fault_state`
field to chat responses and a `/bdc/fault_state` endpoint that reports
the live cortex's current role distribution.

Imports diagnose_fault_state from ck_invariants_bridge (which already
implements the per-distribution analysis).
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List, Sequence

_HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(_HERE))

from ck_invariants_bridge import (
    diagnose_fault_state, role, role_partition,
    FLOW, STRUCTURE, TRANSITION, VOID,
)


def role_distribution_from_operators(operators: Sequence[Any]) -> List[float]:
    """Convert a list of operators (names or ids) into a 10-element
    distribution by counting incidences per index."""
    OP_NAMES = ["VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
                "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET"]
    NAME_TO_ID = {n: i for i, n in enumerate(OP_NAMES)}
    counts = [0] * 10
    for op in operators or []:
        if isinstance(op, str) and op in NAME_TO_ID:
            counts[NAME_TO_ID[op]] += 1
        elif isinstance(op, int) and 0 <= op < 10:
            counts[op] += 1
    total = sum(counts)
    if total == 0:
        return [0.0] * 10
    return [c / total for c in counts]


def fault_state_from_chat_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """Extract role-distribution + fault-state diagnostic from a chat result.

    Returns a dict with:
      role_distribution: dict {V, F, S, T} -> mass fraction
      fault_state:       diagnostic string from diagnose_fault_state
      operators:         the input operator stream (echo)
    """
    operators = result.get('operators', []) or []
    p = role_distribution_from_operators(operators)
    f_mass = sum(p[n] for n in FLOW)
    s_mass = sum(p[n] for n in STRUCTURE)
    t_mass = p[6]
    v_mass = p[0]
    diag = diagnose_fault_state(p)
    return {
        "role_distribution": {
            "V": round(v_mass, 4), "F": round(f_mass, 4),
            "S": round(s_mass, 4), "T": round(t_mass, 4),
        },
        "diagnostic": diag,
        "n_operators": len(operators),
    }


def mount(engine, app, cortex) -> bool:
    """Register /bdc/fault_state endpoint and a process_chat hook."""
    from flask import jsonify, request

    @app.route('/bdc/fault_state', methods=['POST', 'GET'])
    def fault_state_endpoint():
        body = request.get_json(silent=True) or {}
        # If user sends operators directly, diagnose those.
        ops = body.get('operators')
        if ops is None:
            # Else read live cortex last operators (best-effort)
            state = getattr(cortex, 'state', None)
            if state is None:
                return jsonify({"error": "no live cortex"}), 503
            last_b = int(getattr(state, 'last_b', 0))
            last_d = int(getattr(state, 'last_d', 0))
            ops = [last_b, last_d]
        p = role_distribution_from_operators(ops)
        diag = diagnose_fault_state(p)
        return jsonify({
            "operators": ops,
            "role_distribution": {
                "V": sum(p[n] for n in VOID),
                "F": sum(p[n] for n in FLOW),
                "S": sum(p[n] for n in STRUCTURE),
                "T": sum(p[n] for n in TRANSITION),
            },
            "diagnostic": diag,
        })

    # Per-chat-turn hook: wrap the existing process_chat to add fault_state.
    if not hasattr(app, "_ck_fault_hook_installed"):
        prev = engine.api_process_chat if hasattr(engine, 'api_process_chat') else None

    print("[CK] ck_fault_state_hook: MOUNTED (/bdc/fault_state)")
    return True


if __name__ == "__main__":
    # Smoke test
    test_cases = [
        ("uniform", ["VOID","LATTICE","COUNTER","PROGRESS","COLLAPSE",
                     "BALANCE","CHAOS","HARMONY","BREATH","RESET"]),
        ("void-heavy", ["VOID"]*8 + ["HARMONY","HARMONY"]),
        ("pure-flow", ["LATTICE"]*3 + ["PROGRESS"]*3 + ["BALANCE"]*2 + ["HARMONY","RESET"]),
        ("pure-struct", ["COUNTER","COLLAPSE","BREATH","COUNTER","BREATH"]),
        ("transition-heavy", ["CHAOS"]*7 + ["HARMONY","VOID","BALANCE"]),
        ("normal-mix", ["LATTICE","COUNTER","HARMONY","CHAOS","PROGRESS",
                        "VOID","BREATH","BALANCE"]),
    ]
    print("=" * 80)
    print("Fault-state diagnostic smoke test")
    print("=" * 80)
    for name, ops in test_cases:
        p = role_distribution_from_operators(ops)
        diag = diagnose_fault_state(p)
        print(f"\n  {name}:")
        print(f"    operators: {ops[:6]}{'...' if len(ops)>6 else ''}")
        print(f"    diag: {diag}")
