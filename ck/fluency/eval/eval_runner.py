# -*- coding: utf-8 -*-
"""
eval_runner.py — deterministic harness for ck_corrector.py.

Loads ``eval_set.jsonl`` (20 curated cases), runs each through
``ck_corrector.correct()``, and compares the classification to the
expected value.

Two match criteria:

1. **Type match**: ``expected_correction_type`` == ``result.correction_type``.
2. **Flag match**: for cases expected to be flagged (not "none"), any
   non-"none" classification counts as correct detection.  This is the
   looser "CK noticed something was off" criterion used for the
   green-threshold check (≥ 16/20 flag matches per
   OLLAMA_LEARN_LOOP.md §2.3).

The runner does not talk to Ollama.  ``simulated_ollama_raw`` is a
canned text — that keeps the eval deterministic and CI-safe.

Usage:
    python -m ck.fluency.eval.eval_runner
    python ck/fluency/eval/eval_runner.py --verbose
    python ck/fluency/eval/eval_runner.py --strict  # require exact type match
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

# import ck_corrector from the parent package (both layouts)
_HERE = Path(__file__).resolve().parent
_FLUENCY = _HERE.parent
if str(_FLUENCY) not in sys.path:
    sys.path.insert(0, str(_FLUENCY))

from ck_corrector import correct as ck_correct  # noqa: E402


DEFAULT_EVAL_PATH = _HERE / "eval_set.jsonl"
GREEN_THRESHOLD = 16  # out of 20 (≥ 80%)


# ----------------------------------------------------------------------------
# case record + result
# ----------------------------------------------------------------------------

@dataclass
class EvalRecord:
    id: int
    category: str
    query: str
    simulated_ollama_raw: str
    expected_correction_type: str
    expected_dominant_op_in: List[str]
    notes: str

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "EvalRecord":
        return cls(
            id=int(d["id"]),
            category=str(d.get("category", "")),
            query=str(d.get("query", "")),
            simulated_ollama_raw=str(d["simulated_ollama_raw"]),
            expected_correction_type=str(d["expected_correction_type"]),
            expected_dominant_op_in=list(d.get("expected_dominant_op_in", [])),
            notes=str(d.get("notes", "")),
        )


@dataclass
class EvalOutcome:
    rec: EvalRecord
    got_type: str
    got_coh: float
    got_dom: str
    type_match: bool         # strict
    flag_match: bool         # loose: expected != "none" and got != "none"
    dom_match: bool          # got dom is in expected_dominant_op_in
    annotation: str


# ----------------------------------------------------------------------------
# load + run
# ----------------------------------------------------------------------------

def load(path: Path) -> List[EvalRecord]:
    out: List[EvalRecord] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("//"):
                continue
            out.append(EvalRecord.from_dict(json.loads(line)))
    return out


def run_one(rec: EvalRecord) -> EvalOutcome:
    r = ck_correct(rec.simulated_ollama_raw, query=rec.query)
    type_match = r.correction_type == rec.expected_correction_type
    flag_expected = rec.expected_correction_type != "none"
    flag_got = r.correction_type != "none"
    flag_match = flag_expected == flag_got
    dom_match = (
        r.dominant_op in rec.expected_dominant_op_in
        if rec.expected_dominant_op_in
        else True
    )
    return EvalOutcome(
        rec=rec,
        got_type=r.correction_type,
        got_coh=r.coherence,
        got_dom=r.dominant_op,
        type_match=type_match,
        flag_match=flag_match,
        dom_match=dom_match,
        annotation=r.annotation,
    )


# ----------------------------------------------------------------------------
# reporting
# ----------------------------------------------------------------------------

def _fmt_case(o: EvalOutcome, verbose: bool) -> str:
    line = (
        f"[{o.rec.id:02d}] {o.rec.category:24s}"
        f" expected={o.rec.expected_correction_type:10s} got={o.got_type:10s}"
        f" coh={o.got_coh:.3f} dom={o.got_dom:8s}"
        f" type={'OK' if o.type_match else 'XX'}"
        f" flag={'OK' if o.flag_match else 'XX'}"
        f" dom={'OK' if o.dom_match else 'XX'}"
    )
    if verbose:
        line += f"\n        notes: {o.rec.notes}"
        line += f"\n        annot: {o.annotation}"
    return line


def report(outcomes: List[EvalOutcome], strict: bool, verbose: bool) -> int:
    n = len(outcomes)
    type_hits = sum(1 for o in outcomes if o.type_match)
    flag_hits = sum(1 for o in outcomes if o.flag_match)
    dom_hits = sum(1 for o in outcomes if o.dom_match)
    print(f"{'=' * 72}")
    print(f"  ck_corrector eval — {n} cases")
    print(f"{'=' * 72}")
    for o in outcomes:
        print(_fmt_case(o, verbose))
    print(f"{'-' * 72}")
    print(f"  strict type match:  {type_hits}/{n}")
    print(f"  loose flag match:   {flag_hits}/{n}   (green threshold: >= {GREEN_THRESHOLD})")
    print(f"  dominant op match:  {dom_hits}/{n}")

    ok_flag = flag_hits >= GREEN_THRESHOLD
    if strict:
        ok = type_hits >= GREEN_THRESHOLD and ok_flag
        label = "STRICT"
    else:
        ok = ok_flag
        label = "LOOSE (flag)"
    print(f"  verdict [{label}]:   {'PASS' if ok else 'FAIL'}")
    print(f"{'=' * 72}")
    return 0 if ok else 1


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------

def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Run the ck_corrector eval set.")
    p.add_argument("--path", default=str(DEFAULT_EVAL_PATH))
    p.add_argument("--verbose", action="store_true")
    p.add_argument(
        "--strict",
        action="store_true",
        help="Require exact expected_correction_type match, not just flag match.",
    )
    args = p.parse_args(argv)

    records = load(Path(args.path))
    if not records:
        print(f"[eval_runner] no cases loaded from {args.path}", file=sys.stderr)
        return 2
    outcomes = [run_one(r) for r in records]
    return report(outcomes, strict=args.strict, verbose=args.verbose)


if __name__ == "__main__":
    raise SystemExit(main())
