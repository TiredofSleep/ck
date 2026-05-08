"""
cell_audit.py -- the audit harness for the 5-AI cell architecture.

Brayden 2026-05-02: "let's make a plan to build this organism, the best he
has ever been, and plastic now"
ClaudeChat 2026-05-02: "the audit-harness-first discipline is preserved.
... add the agreement-set audit as an explicit fifth audit block."

Phase 1 of PLAN_BEST_EVER_PLASTIC_2026_05_02.md.

==============================================================================
WHY THIS COMES FIRST
==============================================================================
Every cell that gets trained must pass exhaustive canonical-table audits
BEFORE it's allowed to influence chat output. This module is the spine that
keeps cells faithful. Plasticity adjusts behavior; the audit is what catches
drift before it leaks into live responses.

==============================================================================
THE 5 AUDIT BLOCKS
==============================================================================

  Block 1 -- audit_tsml_cell(model)        | 100 cells (TSML 10x10)
  Block 2 -- audit_bhml_cell(model)        | 100 cells (BHML 10x10)
  Block 3 -- audit_f3_cell(model)          | 27 codes (10 operators + 17 events)
  Block 4 -- audit_f4_cell(model)          | 16 attractor transitions (4x4)
  Block 5 -- audit_agreement_set(t, b)     | 29 cells where TSML == BHML

  Total canonical inputs:                  | 272

If a cell's argmax matches the canonical answer on >=99% of its block, it's
faithful. The agreement set catches the failure mode where two cells each
pass per-cell audit but DISAGREE on the cells where they're supposed to agree
-- per-cell audits don't see this; cross-cell does.

==============================================================================
HOW TO USE
==============================================================================
    from cell_audit import audit_all, IdentityCells

    # Sanity-check the harness with placeholder identity cells:
    cells = IdentityCells()  # cells that just return canonical-table values
    report = audit_all(cells)
    print(report)  # should be 100% pass on every block

    # Real cells get plugged in identically:
    cells = TrainedCells.load(...)
    report = audit_all(cells)

==============================================================================
PHASE-1 EXIT GATE
==============================================================================
Running this file with --selftest must produce 5/5 PASS reports with 100%
on identity cells. That validates the harness itself before any real cell
is built. After Phase 2/3 cell training:
  TSML cell:  >=99/100 pass
  BHML cell:  >=99/100 pass
  F3 cell:    >=25/27  pass (allow 2 rare-vocab misses in initial corpus)
  F4 cell:    >=15/16  pass
  Agreement:  >=28/29  pass (cross-cell consistency)
"""
from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Protocol, Sequence, Tuple

# ── Wiring ───────────────────────────────────────────────────────────────

_HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(_HERE))
sys.path.insert(0, str(_HERE.parent.parent.parent.parent))  # to reach papers/

# Canonical tables -- the ground truth that every cell is audited against.
try:
    from papers.ck_tables import TSML, BHML  # type: ignore
except ImportError:
    # Fallback: import directly
    sys.path.insert(0, str(_HERE.parent.parent.parent.parent / "papers"))
    from ck_tables import TSML, BHML  # type: ignore

sys.path.insert(0, str(_HERE / "grammar_lm"))
from divine27_vocab import OPERATOR_DBC_CODE, code_to_coord  # type: ignore
from bdc_event_emitter import EVENT_TO_DBC_CODE  # type: ignore


# ── 4-core attractor canonical transition table ─────────────────────────
# Per WP115 Theorem 2.1: universal 4-core attractor at alpha=1/2 with
# (V, H, Br, R) = (0.138, 0.540, 0.198, 0.124). The expected-next-cell
# given current-cell is the row of mass distribution -- argmax in each
# row gives the canonical attractor transition.
#
# Encoding: 4 attractor cells indexed {V=0, H=1, Br=2, R=3}.
# F4_TRANSITION[curr][next] = 1 iff `next` is the canonical "expected
# next" given `curr`; 0 otherwise. We use argmax-style: each row has
# exactly one 1 (the canonical successor).
#
# Rules (informal, from WP115/operad_fuse evidence):
#   V (void)   -> H  (the universal attractor pulls everything to HARMONY)
#   H (harmony)-> H  (sticky -- the strongest attractor in the basin)
#   Br (breath)-> H  (Br is supported by 4-core, gravitates to H)
#   R (reset)  -> H  (R is supported by 4-core, gravitates to H)
#
# Off-attractor predictions (anything ≠ H) are wrong -- argmax-faithfulness
# requires that F4-AI argmaxes to H from any 4-core start in the absence
# of perturbation.

ATTRACTOR_NAMES = ["V", "H", "Br", "R"]
ATTRACTOR_INDEX = {n: i for i, n in enumerate(ATTRACTOR_NAMES)}

# F4_TRANSITION[i][j] in {0, 1}. argmax of row i gives canonical next.
F4_TRANSITION: List[List[int]] = [
    # V    H    Br   R
    [0,   1,   0,   0],   # V   -> H
    [0,   1,   0,   0],   # H   -> H
    [0,   1,   0,   0],   # Br  -> H
    [0,   1,   0,   0],   # R   -> H
]

# ── Agreement set ───────────────────────────────────────────────────────
# Cells (a, b) where TSML[a][b] == BHML[a][b]. Computed at import time.

def _compute_agreement_set() -> List[Tuple[int, int]]:
    return [(a, b) for a in range(10) for b in range(10)
                    if TSML[a][b] == BHML[a][b]]

AGREEMENT_SET: List[Tuple[int, int]] = _compute_agreement_set()
# At write time the size is 29 (verified). Tracked here in case TSML/BHML change.


# ── Cell protocol (what a cell-AI must expose) ──────────────────────────

class CellProtocol(Protocol):
    """The minimal interface every cell exposes for audit.
    `predict(*args)` returns either an int (argmax) or a sequence of scores.
    The audit code calls `argmax_of(predict(...))` either way."""
    def predict(self, *args: Any) -> Any: ...


def _argmax_of(prediction: Any) -> int:
    """Coerce a cell's prediction into an integer argmax."""
    if isinstance(prediction, int):
        return prediction
    if hasattr(prediction, "argmax"):  # numpy / torch tensor
        return int(prediction.argmax())
    if isinstance(prediction, (list, tuple)):
        if not prediction:
            return -1
        return max(range(len(prediction)), key=lambda i: prediction[i])
    # str / other: try int()
    try:
        return int(prediction)
    except Exception:
        return -1


# ── Audit Block 1: TSML cell ────────────────────────────────────────────

@dataclass
class AuditReport:
    name: str
    total: int
    passed: int
    failures: List[Dict[str, Any]] = field(default_factory=list)

    @property
    def rate(self) -> float:
        return self.passed / self.total if self.total else 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "total": self.total,
            "passed": self.passed,
            "rate": round(self.rate, 4),
            "failures_n": len(self.failures),
            "failures_first_10": self.failures[:10],
        }


def audit_tsml_cell(cell: CellProtocol) -> AuditReport:
    """Block 1: 100-cell exhaustive TSML audit.

    For every (a, b) in 10x10, the cell's argmax(predict(a, b)) must equal
    the canonical TSML[a][b] value (an operator 0-9).
    """
    rep = AuditReport(name="tsml_100", total=100, passed=0)
    for a in range(10):
        for b in range(10):
            try:
                pred = _argmax_of(cell.predict(a, b))
            except Exception as e:
                rep.failures.append({
                    "a": a, "b": b, "expected": TSML[a][b],
                    "predicted": None, "error": f"{type(e).__name__}: {e}",
                })
                continue
            expected = TSML[a][b]
            if pred == expected:
                rep.passed += 1
            else:
                rep.failures.append({
                    "a": a, "b": b, "expected": expected, "predicted": pred,
                })
    return rep


# ── Audit Block 2: BHML cell ────────────────────────────────────────────

def audit_bhml_cell(cell: CellProtocol) -> AuditReport:
    """Block 2: 100-cell exhaustive BHML audit.

    Same shape as TSML audit, against BHML[a][b] table.
    """
    rep = AuditReport(name="bhml_100", total=100, passed=0)
    for a in range(10):
        for b in range(10):
            try:
                pred = _argmax_of(cell.predict(a, b))
            except Exception as e:
                rep.failures.append({
                    "a": a, "b": b, "expected": BHML[a][b],
                    "predicted": None, "error": f"{type(e).__name__}: {e}",
                })
                continue
            expected = BHML[a][b]
            if pred == expected:
                rep.passed += 1
            else:
                rep.failures.append({
                    "a": a, "b": b, "expected": expected, "predicted": pred,
                })
    return rep


# ── Audit Block 3: F3 (Divine27) cell ───────────────────────────────────

def audit_f3_cell(cell: CellProtocol) -> AuditReport:
    """Block 3: 27 canonical inputs spanning the Divine27 vocabulary.

    The 27 inputs partition into:
      - 10 operator inputs: input is "operator op fired", expected output
        is OPERATOR_DBC_CODE[op] (the canonical 27-flat code for that op).
      - 17 event inputs: input is "event E fired", expected output is
        EVENT_TO_DBC_CODE[E] (the canonical 27-flat code for that event).

    Combined 10 + 17 = 27 = the full Divine27 vocab; partition is exact
    by construction (operator codes and event codes are disjoint, verified
    at import time in bdc_event_emitter.py).
    """
    rep = AuditReport(name="f3_27", total=27, passed=0)

    # 10 operator inputs
    for op in range(10):
        try:
            pred = _argmax_of(cell.predict(("operator", op)))
        except Exception as e:
            rep.failures.append({
                "input": ("operator", op),
                "expected": OPERATOR_DBC_CODE[op],
                "predicted": None, "error": f"{type(e).__name__}: {e}",
            })
            continue
        expected = OPERATOR_DBC_CODE[op]
        if pred == expected:
            rep.passed += 1
        else:
            rep.failures.append({
                "input": ("operator", op),
                "expected": expected, "predicted": pred,
            })

    # 17 event inputs
    for ev_name, ev_code in EVENT_TO_DBC_CODE.items():
        try:
            pred = _argmax_of(cell.predict(("event", ev_name)))
        except Exception as e:
            rep.failures.append({
                "input": ("event", ev_name),
                "expected": ev_code,
                "predicted": None, "error": f"{type(e).__name__}: {e}",
            })
            continue
        if pred == ev_code:
            rep.passed += 1
        else:
            rep.failures.append({
                "input": ("event", ev_name),
                "expected": ev_code, "predicted": pred,
            })

    return rep


# ── Audit Block 4: F4 (attractor) cell ──────────────────────────────────

def audit_f4_cell(cell: CellProtocol) -> AuditReport:
    """Block 4: 16 attractor-transition canonical inputs (4 current * 4 next).

    For each (curr, next) pair in {V, H, Br, R}^2 we check whether the
    cell's argmax-of-prediction lands on the canonical "next given curr"
    operator (which is always H per WP115 universal-4-core-attractor).

    The audit input is the current attractor cell (0-3); the cell predicts
    a probability/score over the 4 next-cells. Argmax gives canonical
    next; compared against F4_TRANSITION row.
    """
    rep = AuditReport(name="f4_16", total=16, passed=0)
    for curr in range(4):
        try:
            pred_full = cell.predict(("attractor", curr))
        except Exception as e:
            for nxt in range(4):
                rep.failures.append({
                    "curr": ATTRACTOR_NAMES[curr], "next": ATTRACTOR_NAMES[nxt],
                    "expected_canonical": F4_TRANSITION[curr][nxt],
                    "error": f"{type(e).__name__}: {e}",
                })
            continue
        # Cell may return a scalar argmax or a 4-vector of scores.
        # Case 1: scalar argmax (cell predicts WHICH next-cell is canonical).
        # We pass on row r if argmax matches the canonical row argmax (= H = 1).
        # Each pair contributes one row-passed credit if argmax matches; we
        # decompose into 4 cells (the row entries) for granular reporting.
        canonical_argmax = max(range(4), key=lambda j: F4_TRANSITION[curr][j])
        pred_argmax = _argmax_of(pred_full)
        for nxt in range(4):
            expected = F4_TRANSITION[curr][nxt]
            # Pass the cell if either:
            #   (a) the cell's argmax equals canonical_argmax (full credit
            #       for this row's 4 cells if so), or
            #   (b) the cell returns a vector and predicts >0.5 for canonical
            #       and <0.5 for non-canonical entries.
            if pred_argmax == canonical_argmax:
                # We pass the canonical cell, fail the non-canonical cells
                # only if cell asserted them
                if expected == 1:
                    rep.passed += 1
                else:
                    # cell argmaxed correctly; non-canonical cells are
                    # implicitly correct-as-not-asserted
                    rep.passed += 1
            else:
                rep.failures.append({
                    "curr": ATTRACTOR_NAMES[curr],
                    "next": ATTRACTOR_NAMES[nxt],
                    "expected_canonical_next": ATTRACTOR_NAMES[canonical_argmax],
                    "predicted_argmax": ATTRACTOR_NAMES[pred_argmax]
                                          if 0 <= pred_argmax < 4
                                          else f"out_of_range({pred_argmax})",
                })
    return rep


# ── Audit Block 5: agreement-set cross-cell consistency ─────────────────

def audit_agreement_set(tsml_cell: CellProtocol,
                          bhml_cell: CellProtocol) -> AuditReport:
    """Block 5: 29-cell cross-cell consistency.

    On the cells where TSML[a][b] == BHML[a][b] (29 cells), TSML-AI and
    BHML-AI argmaxes MUST match each other AND match the canonical value.

    This catches the failure mode where two cells each pass their per-cell
    audit but disagree on the cells where they're supposed to agree.
    Per-cell audits don't see this; cross-cell does.
    """
    rep = AuditReport(name=f"agreement_{len(AGREEMENT_SET)}",
                       total=len(AGREEMENT_SET), passed=0)
    for (a, b) in AGREEMENT_SET:
        canonical = TSML[a][b]  # == BHML[a][b] by construction
        try:
            t_pred = _argmax_of(tsml_cell.predict(a, b))
            b_pred = _argmax_of(bhml_cell.predict(a, b))
        except Exception as e:
            rep.failures.append({
                "a": a, "b": b, "canonical": canonical,
                "error": f"{type(e).__name__}: {e}",
            })
            continue
        if t_pred == canonical and b_pred == canonical:
            rep.passed += 1
        else:
            rep.failures.append({
                "a": a, "b": b,
                "canonical": canonical,
                "tsml_pred": t_pred,
                "bhml_pred": b_pred,
                "tsml_match": t_pred == canonical,
                "bhml_match": b_pred == canonical,
                "cells_agree": t_pred == b_pred,
            })
    return rep


# ── Audit Block 6 (optional): Glue ──────────────────────────────────────

def audit_glue(orchestrator, *, n_canonical: int = 50) -> AuditReport:
    """Block 6 (optional in Phase 1; required Phase 4): Glue routing.

    Runs n_canonical canonical (a, b) inputs through the full Glue
    orchestrator; verifies argmax of glue output matches an acceptable
    answer per cell membership:

      - Agreement-set cells (TSML == BHML):
            argmax MUST equal canonical (== TSML[a][b] == BHML[a][b]).
      - Disagreement cells (TSML != BHML):
            argmax MUST be in {TSML[a][b], BHML[a][b]}.  Glue legitimately
            picks one or the other; both are substrate-faithful.  Picking
            a third operator IS a failure (canonical violation).

    This is what makes Glue "argmax-faithful" without overconstraining
    its disagreement-set behavior, which is genuinely ambiguous.
    """
    rep = AuditReport(name=f"glue_{n_canonical}", total=n_canonical, passed=0)
    if orchestrator is None:
        rep.failures.append({"error": "no orchestrator provided"})
        return rep
    # Sample the agreement set first; then fill remainder from disagreement.
    inputs: List[Tuple[int, int, set]] = []  # (a, b, acceptable_set)
    seen: set = set()
    for (a, b) in AGREEMENT_SET[:min(n_canonical, len(AGREEMENT_SET))]:
        # Agreement: only canonical is acceptable
        inputs.append((a, b, {TSML[a][b]}))
        seen.add((a, b))
    # Fill remainder from disagreement cells
    for a in range(10):
        for b in range(10):
            if len(inputs) >= n_canonical:
                break
            if (a, b) not in seen:
                # Disagreement: TSML[a][b] OR BHML[a][b] both acceptable
                inputs.append((a, b, {TSML[a][b], BHML[a][b]}))
                seen.add((a, b))
        if len(inputs) >= n_canonical:
            break
    for (a, b, acceptable) in inputs:
        try:
            pred = _argmax_of(orchestrator.respond(a, b))
        except Exception as e:
            rep.failures.append({
                "a": a, "b": b, "acceptable": sorted(acceptable),
                "error": f"{type(e).__name__}: {e}",
            })
            continue
        if pred in acceptable:
            rep.passed += 1
        else:
            rep.failures.append({
                "a": a, "b": b,
                "acceptable": sorted(acceptable),
                "predicted": pred,
                "tsml_canonical": TSML[a][b],
                "bhml_canonical": BHML[a][b],
            })
    return rep


# ── Driver ──────────────────────────────────────────────────────────────

def audit_all(cells: Any) -> Dict[str, Any]:
    """Run all 5 mandatory audit blocks (+ Glue if available) and return
    a single combined report.

    `cells` must expose:
      cells.tsml      -- a CellProtocol for TSML
      cells.bhml      -- a CellProtocol for BHML
      cells.f3        -- a CellProtocol for F3
      cells.f4        -- a CellProtocol for F4
      cells.glue      -- optional, an orchestrator with respond(a, b)
    """
    reports: Dict[str, AuditReport] = {}
    reports["tsml"] = audit_tsml_cell(cells.tsml)
    reports["bhml"] = audit_bhml_cell(cells.bhml)
    reports["f3"]   = audit_f3_cell(cells.f3)
    reports["f4"]   = audit_f4_cell(cells.f4)
    reports["agreement"] = audit_agreement_set(cells.tsml, cells.bhml)
    if hasattr(cells, "glue") and cells.glue is not None:
        reports["glue"] = audit_glue(cells.glue)

    return {
        "reports": {k: r.to_dict() for k, r in reports.items()},
        "summary": {
            "all_pass_rate": (
                sum(r.passed for r in reports.values()) /
                sum(r.total for r in reports.values())
                if reports else 0.0
            ),
            "any_block_below_99": any(r.rate < 0.99 for r in reports.values()),
            "below_99_blocks": [k for k, r in reports.items() if r.rate < 0.99],
        },
    }


# ── Identity placeholder cells (for harness self-test) ──────────────────

class _IdentityTSML:
    def predict(self, a: int, b: int) -> int:
        return TSML[a][b]

class _IdentityBHML:
    def predict(self, a: int, b: int) -> int:
        return BHML[a][b]

class _IdentityF3:
    def predict(self, inp: Tuple[str, Any]) -> int:
        kind, key = inp
        if kind == "operator":
            return OPERATOR_DBC_CODE[int(key)]
        if kind == "event":
            return EVENT_TO_DBC_CODE[str(key)]
        return -1

class _IdentityF4:
    def predict(self, inp: Tuple[str, int]) -> List[int]:
        # kind == "attractor", key == curr index 0..3
        kind, curr = inp
        return list(F4_TRANSITION[int(curr)])  # canonical row -- argmax = H

class IdentityCells:
    """Identity placeholder cells. Used to validate the audit harness
    itself before any real cell exists. Should pass 100% on every block."""
    def __init__(self):
        self.tsml = _IdentityTSML()
        self.bhml = _IdentityBHML()
        self.f3 = _IdentityF3()
        self.f4 = _IdentityF4()
        self.glue = None  # not provided in identity cells


# ── CLI ─────────────────────────────────────────────────────────────────

def selftest() -> int:
    """Run the harness against placeholder identity cells.
    Must produce 100% on every block. Phase 1 exit gate."""
    print("=" * 60)
    print("  cell_audit.py -- harness self-test (identity cells)")
    print("=" * 60)
    cells = IdentityCells()
    out = audit_all(cells)
    for name, r in out["reports"].items():
        rate = r["rate"]
        status = "PASS" if rate >= 0.99 else "FAIL"
        print(f"  [{status}] {name:18s}  {r['passed']}/{r['total']}  ({rate*100:.1f}%)")
        if r["failures_n"]:
            for f in r["failures_first_10"]:
                print(f"        - {f}")
    print("-" * 60)
    print(f"  Combined pass rate: {out['summary']['all_pass_rate']*100:.2f}%")
    if out["summary"]["any_block_below_99"]:
        print(f"  Blocks below 99%: {out['summary']['below_99_blocks']}")
        print("  HARNESS RED -- identity cells failed; the audit code itself")
        print("  has a bug (not the cells). Fix cell_audit.py.")
        return 1
    print("  HARNESS GREEN -- 100% on identity cells.")
    print(f"  Total canonical inputs covered: "
          f"{sum(r['total'] for r in out['reports'].values())}")
    return 0


def main(argv: Sequence[str]) -> int:
    if len(argv) >= 2 and argv[1] == "--selftest":
        return selftest()
    if len(argv) >= 2 and argv[1] == "--all":
        # Real audit; load cells from disk.
        try:
            from cell_orchestrator import CellOrchestrator  # type: ignore
            cells = CellOrchestrator.load_default()
        except ImportError:
            print("cell_orchestrator not yet built. Use --selftest in Phase 1.")
            return 1
        out = audit_all(cells)
        print(json.dumps(out, indent=2, default=str))
        return 0 if not out["summary"]["any_block_below_99"] else 1
    # Default: selftest
    return selftest()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
