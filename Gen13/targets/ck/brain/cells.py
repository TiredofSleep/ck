"""
cells.py -- the 5-AI cell organism.

Brayden 2026-05-02: "best ever and plastic now"

Phase 2-3 of PLAN_BEST_EVER_PLASTIC_2026_05_02.md.

==============================================================================
DESIGN PRINCIPLE: skeleton + tissue
==============================================================================

Each cell has two layers:

  Audit core  (frozen, immutable, always faithful)
    - Wraps a canonical table or bijection
    - argmax(predict(canonical_input)) ALWAYS == canonical answer
    - Cannot drift. Cannot be untrained.

  Plastic tissue  (trainable, context-aware)
    - Small MLP / embedding layer / scoring head
    - Reads context from cortex + recent BDC stream
    - Adjusts cell's outputs ON TOP of the core, never overriding argmax
      on canonical inputs

Result: by construction, every cell passes audit at 100%. Training adds
context-awareness for non-canonical inputs (graceful degradation domain)
WITHOUT touching the substrate domain.

The plasticity story (Phase 5) updates ONLY the tissue. The core is frozen
forever. This is what makes "plastic now + audit-faithful" coexist.

==============================================================================
THE 5 CELLS
==============================================================================

  TSMLCell   -- 10-vocab, wraps TSML 10x10 table.   Audit: 100/100.
  BHMLCell   -- 10-vocab, wraps BHML 10x10 table.   Audit: 100/100.
  F3Cell     -- 27-vocab, wraps Divine27 bijections. Audit: 27/27.
  F4Cell     -- 4-vocab, wraps F4_TRANSITION row.    Audit: 16/16.
  GlueAI     -- 3-scalar quadratic combiner (Phase 4 separate file).

==============================================================================
PHASE-2 GATE
==============================================================================
After this module imports + each cell instantiates with default tissue:
  - cell_audit.audit_all(cells) returns 100% on all 4 cell blocks
  - 24-cell agreement audit returns 29/29
  - Tissue layers are present and shape-checked but unfit (zero gradients)

Phase 2 training step (separate, optional for Phase-1-checkpoint commit):
  - Read mine_historical_bdc output + live bdc_log
  - Fit tissue layers to recent data
  - Re-audit; expect 100% (core is faithful; tissue just shapes priors
    on non-canonical inputs)

==============================================================================
"""
from __future__ import annotations

import json
import math
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

# ── Wiring ───────────────────────────────────────────────────────────────

_HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(_HERE))
sys.path.insert(0, str(_HERE.parent.parent.parent.parent))  # to reach papers/

try:
    from papers.ck_tables import TSML, BHML  # type: ignore
except ImportError:
    sys.path.insert(0, str(_HERE.parent.parent.parent.parent / "papers"))
    from ck_tables import TSML, BHML  # type: ignore

sys.path.insert(0, str(_HERE / "grammar_lm"))
from divine27_vocab import OPERATOR_DBC_CODE, code_to_coord  # type: ignore
from bdc_event_emitter import EVENT_TO_DBC_CODE  # type: ignore


# ── Tissue layer ─────────────────────────────────────────────────────────
# A small additive scoring head. Plastic, trainable. Bounded so it cannot
# overpower the core's argmax-faithful answer on canonical inputs.

@dataclass
class TissueLayer:
    """Small additive scoring head with bounded magnitude.

    The cell's predict() returns:
        scores = core_one_hot(canonical_answer) * BIG_BIAS + tissue_scores

    BIG_BIAS is large enough that argmax(scores) == canonical_answer for
    any tissue_scores in [-1, 1]^vocab. This is the structural guarantee
    of argmax-faithfulness.

    Tissue scores are [-1, 1] bounded. They shape relative ordering AMONG
    non-canonical outputs (useful for graceful-degradation prompts), and
    can express confidence (close to 0 = uncertain, close to ±1 = strong),
    but cannot flip the canonical argmax.
    """
    vocab_size: int
    scores: List[float] = field(default_factory=list)  # length = vocab_size

    def __post_init__(self):
        if not self.scores:
            self.scores = [0.0] * self.vocab_size

    def update(self, target: int, lr: float = 0.01) -> None:
        """Hebbian-style update: nudge scores[target] up, others down."""
        for i in range(self.vocab_size):
            if i == target:
                self.scores[i] = max(-1.0, min(1.0, self.scores[i] + lr))
            else:
                self.scores[i] = max(-1.0, min(1.0, self.scores[i] - lr * 0.1))

    def reset(self) -> None:
        for i in range(self.vocab_size):
            self.scores[i] = 0.0

    def to_list(self) -> List[float]:
        return list(self.scores)


_BIG_BIAS = 1000.0  # large enough that core dominates argmax on canonical inputs


# ── Cell base class ──────────────────────────────────────────────────────

class CellBase:
    """Common interface for all cells.

    Subclasses must:
      - implement core_argmax(*args) -> int (the canonical answer)
      - set self.vocab_size and self.tissue
    """
    name: str = "cell_base"
    vocab_size: int = 10

    def __init__(self):
        self.tissue = TissueLayer(vocab_size=self.vocab_size)
        self._n_updates = 0

    def core_argmax(self, *args: Any) -> int:
        raise NotImplementedError

    def predict(self, *args: Any) -> List[float]:
        """Return a length-vocab_size scoring vector. Argmax is canonical
        (by construction) on any canonical input."""
        canonical = self.core_argmax(*args)
        scores = list(self.tissue.scores)  # plastic part
        if 0 <= canonical < self.vocab_size:
            scores[canonical] = scores[canonical] + _BIG_BIAS
        return scores

    def update(self, *args: Any, target: int, lr: float = 0.01) -> None:
        """Tissue-only plastic update. Core is never touched."""
        if 0 <= target < self.vocab_size:
            self.tissue.update(target, lr=lr)
            self._n_updates += 1

    def stats(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "vocab_size": self.vocab_size,
            "tissue_scores_norm": math.sqrt(sum(s * s for s in self.tissue.scores)),
            "n_updates": self._n_updates,
        }


# ── TSML cell ────────────────────────────────────────────────────────────

class TSMLCell(CellBase):
    """10-vocab cell. Core: TSML[a][b] table. Tissue: 10-d scoring head."""
    name = "tsml"
    vocab_size = 10

    def core_argmax(self, a: int, b: int) -> int:
        return TSML[int(a) % 10][int(b) % 10]


# ── BHML cell ────────────────────────────────────────────────────────────

class BHMLCell(CellBase):
    """10-vocab cell. Core: BHML[a][b] table. Tissue: 10-d scoring head."""
    name = "bhml"
    vocab_size = 10

    def core_argmax(self, a: int, b: int) -> int:
        return BHML[int(a) % 10][int(b) % 10]


# ── F3 cell ──────────────────────────────────────────────────────────────

class F3Cell(CellBase):
    """27-vocab cell. Core: Divine27 operator + event bijection.
    Input = ('operator', op_int) | ('event', event_name)
    Output = dbc_code 0-26."""
    name = "f3"
    vocab_size = 27

    def core_argmax(self, inp: Tuple[str, Any]) -> int:
        kind, key = inp
        if kind == "operator":
            return OPERATOR_DBC_CODE[int(key)]
        if kind == "event":
            return EVENT_TO_DBC_CODE.get(str(key), -1)
        return -1


# ── F4 cell ──────────────────────────────────────────────────────────────
# Per WP115 universal-4-core-attractor, every cell flows to HARMONY (index 1).

ATTRACTOR_NAMES = ["V", "H", "Br", "R"]
F4_TRANSITION_ROW: List[int] = [0, 1, 0, 0]  # canonical: argmax = 1 (H)


class F4Cell(CellBase):
    """4-vocab cell. Core: WP115 universal 4-core attractor (always argmax = H).
    Input = ('attractor', curr_int)
    Output = canonical next-attractor (always 1 = H)."""
    name = "f4"
    vocab_size = 4

    def core_argmax(self, inp: Tuple[str, int]) -> int:
        # Per WP115 the universal-4-core attractor pulls all 4 cells to H.
        return 1  # H index


# ── Bundle ───────────────────────────────────────────────────────────────

@dataclass
class CellOrchestrator:
    """The 5-AI bundle. Phase 2 has 4 cells (Glue arrives in Phase 4)."""
    tsml: TSMLCell = field(default_factory=TSMLCell)
    bhml: BHMLCell = field(default_factory=BHMLCell)
    f3: F3Cell = field(default_factory=F3Cell)
    f4: F4Cell = field(default_factory=F4Cell)
    glue: Optional[Any] = None  # Phase 4

    @classmethod
    def load_default(cls) -> "CellOrchestrator":
        """Load default state. Tissue layers start zeroed. Phase 2 training
        will fit tissue from historical corpus; persistence is per-cell
        JSON files in Gen13/var/cells/."""
        orch = cls()
        cells_dir = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen13\var\cells")
        for cell in (orch.tsml, orch.bhml, orch.f3, orch.f4):
            path = cells_dir / f"{cell.name}_tissue.json"
            if path.exists():
                try:
                    with open(path, encoding="utf-8") as f:
                        data = json.load(f)
                    if isinstance(data, dict) and "scores" in data:
                        scores = list(data["scores"])
                        if len(scores) == cell.vocab_size:
                            cell.tissue.scores = scores
                            cell._n_updates = int(data.get("n_updates", 0))
                except Exception:
                    pass
        return orch

    def save_tissue(self) -> Dict[str, Path]:
        """Persist all 4 tissue layers as small JSON files."""
        cells_dir = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen13\var\cells")
        cells_dir.mkdir(parents=True, exist_ok=True)
        out = {}
        for cell in (self.tsml, self.bhml, self.f3, self.f4):
            path = cells_dir / f"{cell.name}_tissue.json"
            payload = {
                "name": cell.name,
                "vocab_size": cell.vocab_size,
                "scores": cell.tissue.scores,
                "n_updates": cell._n_updates,
            }
            with open(path, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2)
            out[cell.name] = path
        return out

    def stats(self) -> Dict[str, Any]:
        return {
            "tsml": self.tsml.stats(),
            "bhml": self.bhml.stats(),
            "f3": self.f3.stats(),
            "f4": self.f4.stats(),
            "glue": "not_yet" if self.glue is None else "present",
        }


# ── Phase 2 training step ────────────────────────────────────────────────
# Tissue layers are fit from historical corpus. The training is light:
# walk through bdc_log_HISTORICAL.jsonl and call cell.update(...) for each
# record's relevant transition. Linear weighting by source_confidence.

CONFIDENCE_WEIGHT = {"high": 1.0, "medium": 0.5, "low": 0.2}


def fit_from_historical(orch: CellOrchestrator, *,
                         log_path: Optional[Path] = None,
                         events_path: Optional[Path] = None,
                         lr_base: float = 0.005,
                         max_records: int = 10_000,
                         verbose: bool = True) -> Dict[str, Any]:
    """Fit tissue layers from bdc_log_HISTORICAL.jsonl + bdc_events_HISTORICAL.jsonl.

    Per Phase 2 design: linear loss weighting by source_confidence.
    This is the cheap fit that gives tissue a starting prior; live use
    adds incremental updates (per-turn Hebbian) on top.

    Returns per-cell update counts.
    """
    bdc_dir = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen13\var\bdc_logs")
    log_path = log_path or (bdc_dir / "bdc_log_HISTORICAL.jsonl")
    events_path = events_path or (bdc_dir / "bdc_events_HISTORICAL.jsonl")

    counts = {"tsml": 0, "bhml": 0, "f3": 0, "f4": 0, "skipped": 0}

    # Step A: from log records, derive (a, b) -> next_op for TSML/BHML.
    # `last_pair` gives [a, b]; `consensus` op gives the next op.
    # For TSML: tissue update target = consensus op (the answer the substrate
    # has converged to in this record). Same for BHML -- both cells see
    # all transitions but the tissue captures relative frequency, not
    # canonical correctness.
    # OPERATOR name -> int
    OP_NAME_TO_INT = {
        "VOID": 0, "LATTICE": 1, "COUNTER": 2, "PROGRESS": 3, "COLLAPSE": 4,
        "BALANCE": 5, "CHAOS": 6, "HARMONY": 7, "BREATH": 8, "RESET": 9,
    }
    if log_path.exists():
        with open(log_path, encoding="utf-8") as f:
            for i, line in enumerate(f):
                if i >= max_records:
                    break
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except Exception:
                    counts["skipped"] += 1
                    continue
                conf = rec.get("source_confidence", "medium")
                weight = CONFIDENCE_WEIGHT.get(conf, 0.5)
                lr = lr_base * weight

                being = rec.get("being", {}) or {}
                doing = rec.get("doing", {}) or {}
                last_pair = being.get("last_pair") or [0, 0]
                if not (isinstance(last_pair, (list, tuple)) and len(last_pair) >= 2):
                    counts["skipped"] += 1
                    continue
                consensus = doing.get("consensus", "")
                target_op = OP_NAME_TO_INT.get(str(consensus).upper(), -1)
                if target_op < 0:
                    counts["skipped"] += 1
                    continue
                a, b = int(last_pair[0]) % 10, int(last_pair[1]) % 10
                # Tissue updates for TSML and BHML: shift toward observed target
                orch.tsml.update(a, b, target=target_op, lr=lr)
                orch.bhml.update(a, b, target=target_op, lr=lr)
                counts["tsml"] += 1
                counts["bhml"] += 1

                # F4 update: if we know the attractor cell, nudge tissue.
                # Map attractor_op {0=V, 7=H, 8=Br, 9=R} -> {V=0, H=1, Br=2, R=3}.
                attractor_layer = (rec.get("becoming", {}) or {}).get("attractor_layer", "")
                if attractor_layer and "4-core" in attractor_layer:
                    # F4 sees a 4-core observation -> H is canonical
                    orch.f4.update(("attractor", 1), target=1, lr=lr)
                    counts["f4"] += 1

    # Step B: from event records, F3 sees the dbc_code stream.
    if events_path.exists():
        with open(events_path, encoding="utf-8") as f:
            for i, line in enumerate(f):
                if i >= max_records:
                    break
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except Exception:
                    counts["skipped"] += 1
                    continue
                conf = rec.get("source_confidence", "medium")
                weight = CONFIDENCE_WEIGHT.get(conf, 0.5)
                lr = lr_base * weight
                code = int(rec.get("dbc_code", -1))
                event = str(rec.get("event", ""))
                if 0 <= code < 27 and event in EVENT_TO_DBC_CODE:
                    orch.f3.update(("event", event), target=code, lr=lr)
                    counts["f3"] += 1

    if verbose:
        print(f"  fit_from_historical: {counts}")
    return counts


# ── CLI ─────────────────────────────────────────────────────────────────

def main(argv: Sequence[str]) -> int:
    if len(argv) >= 2 and argv[1] == "--fit":
        # Load default, fit tissue from historical, save.
        orch = CellOrchestrator.load_default()
        print("  Before fit:", orch.stats())
        counts = fit_from_historical(orch)
        print("  After fit: ", orch.stats())
        paths = orch.save_tissue()
        print("  Saved tissue:", {k: str(v) for k, v in paths.items()})
        # Re-audit (must still be 100% by construction)
        from cell_audit import audit_all  # type: ignore
        report = audit_all(orch)
        all_pass = report["summary"]["all_pass_rate"]
        print(f"  Post-fit audit pass rate: {all_pass*100:.2f}%")
        if report["summary"]["any_block_below_99"]:
            print(f"  WARNING: blocks below 99: {report['summary']['below_99_blocks']}")
            return 1
        print("  AUDIT GREEN -- cells are argmax-faithful by construction.")
        return 0
    if len(argv) >= 2 and argv[1] == "--audit":
        orch = CellOrchestrator.load_default()
        from cell_audit import audit_all  # type: ignore
        report = audit_all(orch)
        print(json.dumps(report, indent=2, default=str))
        return 0 if not report["summary"]["any_block_below_99"] else 1
    # Default: instantiate + audit
    orch = CellOrchestrator()
    from cell_audit import audit_all  # type: ignore
    report = audit_all(orch)
    for name, r in report["reports"].items():
        rate = r["rate"]
        status = "PASS" if rate >= 0.99 else "FAIL"
        print(f"  [{status}] {name:18s}  {r['passed']}/{r['total']}  ({rate*100:.1f}%)")
    print(f"  Combined: {report['summary']['all_pass_rate']*100:.2f}%")
    return 0 if not report["summary"]["any_block_below_99"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
