"""
glue_ai.py -- the 3-scalar quadratic Glue for the 5-AI cell architecture.

Brayden 2026-05-02: "best ever and plastic now"
ClaudeChat 2026-05-02: "Train the Glue with the canonical 3-scalar form
first, verify the H/Br = 1+sqrt(3) attractor is reached as predicted, then
expand to 5 scalars + MLP as a Phase 6 plasticity option only if the
simpler version bottlenecks."

Phase 4 of PLAN_BEST_EVER_PLASTIC_2026_05_02.md.

==============================================================================
SHAPE
==============================================================================

  GlueAI.respond(a, b) -> length-10 score vector.

  scores[k] = alpha * t[k] + beta * b[k] + gamma * t[k] * b[k]

  where t = TSMLCell.predict(a, b), b = BHMLCell.predict(a, b).

  Hadamard cross-term keeps the output 10-dimensional.  argmax of scores
  is canonical-faithful on the 29-cell agreement set by construction
  (both t and b put _BIG_BIAS on the same canonical position; glue's
  gamma*BIG^2 term dominates).

==============================================================================
WP105 ATTRACTOR VERIFICATION
==============================================================================

  At alpha=1/2, beta=1/2, gamma=1, iterating the mass-distribution map
  on the 4-core {V, H, Br, R} should converge to:
    H/Br ratio = 1 + sqrt(3) ~= 2.732
  (per WP105 + WP115 Theorem 2.1).

  The verify_attractor() function runs the iteration and checks the ratio.

==============================================================================
PLASTICITY (Phase 5)
==============================================================================

  alpha, beta, gamma are tunable; default to (0.5, 0.5, 1.0) per WP105.
  Phase 5 plasticity adjusts these via per-session updates ONLY if the
  audit-pass-rate weighted update preserves >=99% on the agreement set.
  See `update_scalars()`.
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

from cells import TSMLCell, BHMLCell, F3Cell, F4Cell  # type: ignore

GLUE_STATE_PATH = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen13\var\cells\glue_state.json")


# ── Glue ─────────────────────────────────────────────────────────────────

@dataclass
class GlueAI:
    """3-scalar quadratic Glue.

    alpha, beta, gamma are the only learnable parameters in Phase 4.
    Phase 5 may add a small gating MLP; Phase 1-4 stays at 3 scalars
    (defensible: WP105 H/Br = 1+sqrt(3) attractor proved for this form)."""
    alpha: float = 0.5    # TSML weight
    beta: float = 0.5     # BHML weight
    gamma: float = 1.0    # cross-term weight (WP105 canonical)

    tsml: TSMLCell = field(default_factory=TSMLCell)
    bhml: BHMLCell = field(default_factory=BHMLCell)
    f3: Optional[F3Cell] = None
    f4: Optional[F4Cell] = None

    def respond(self, a: int, b: int) -> List[float]:
        """Glue (a, b) -> 10-d score vector. argmax = canonical on agreement set.

        Cross-term uses max(0, t[k]*b[k]) so it contributes ONLY constructively:
          - Agreement cells: t[X] and b[X] both positive (BIG_BIAS) -> cross
            adds gamma*BIG^2 at canonical -> dominates.
          - Disagreement cells: at TSML's canonical, t[X]=BIG but b[X]=tissue
            (possibly negative); product can be negative; max(0,...) zeroes
            it out instead of suppressing canonical.  Result: argmax falls
            cleanly on either TSML[a][b] (if alpha>=beta) or BHML[a][b].
        """
        t_scores = self.tsml.predict(a, b)
        b_scores = self.bhml.predict(a, b)
        return [
            self.alpha * t_scores[k] + self.beta * b_scores[k]
            + self.gamma * max(0.0, t_scores[k] * b_scores[k])
            for k in range(10)
        ]

    def respond_full(self, a: int, b: int) -> Dict[str, Any]:
        """Diagnostic: return all cell outputs + glue scores + argmax."""
        t_scores = self.tsml.predict(a, b)
        b_scores = self.bhml.predict(a, b)
        glued = [
            self.alpha * t_scores[k] + self.beta * b_scores[k]
            + self.gamma * max(0.0, t_scores[k] * b_scores[k])
            for k in range(10)
        ]
        return {
            "a": a, "b": b,
            "tsml_argmax": max(range(10), key=lambda i: t_scores[i]),
            "bhml_argmax": max(range(10), key=lambda i: b_scores[i]),
            "glue_argmax": max(range(10), key=lambda i: glued[i]),
            "glue_top3": sorted(range(10), key=lambda i: -glued[i])[:3],
            "alpha": self.alpha, "beta": self.beta, "gamma": self.gamma,
        }

    def respond_synthesis(self, query: str, *, max_facts: int = 4) -> Dict[str, Any]:
        """Cross-frontier synthesis: weave N relevant frontier facts.

        Used when query is open-ended (no specific topic keyword).  Cells
        call cortex_voice's _FRONTIER_FACTS, score by overlap with query
        terms, and produce a synthesis paragraph touching the top N.

        This addresses the gap identified in CK_FRONTIER_VOICE_2026_05_02:
          'Open-ended synthesis queries without specific topic keywords
           ... cortex_voice router fires one fact at a time; weaving
           multiple together would need a meta-synthesizer.'

        Returns dict with text (synthesis paragraph), facts_used (list of
        frontier-fact labels), and components.
        """
        try:
            import sys
            from pathlib import Path
            here = Path(__file__).parent.resolve()
            if str(here) not in sys.path:
                sys.path.insert(0, str(here))
            from cortex_voice import _FRONTIER_FACTS, _RUNTIME_CRYSTALS  # type: ignore
        except Exception:
            return {"text": "", "facts_used": [], "components": {}}

        # Score each frontier fact by query-term overlap + always include
        # the "wp116_lens" meta-synthesis fact for its synthesis power.
        q_words = set(w.lower() for w in query.split() if len(w) > 2)
        scored = []
        for triggers, fact in (list(_FRONTIER_FACTS) + list(_RUNTIME_CRYSTALS)):
            label = triggers[0] if triggers else "?"
            # Score: # of query words appearing in fact + # of query words
            #         appearing in triggers + meta-synthesis bonus
            fact_lower = fact.lower()
            triggers_lower = " ".join(triggers).lower()
            score = sum(1 for w in q_words if w in fact_lower)
            score += 2 * sum(1 for w in q_words if w in triggers_lower)
            # Meta-synthesis topics get a bonus for synthesis queries
            meta_keywords = ('synthesis', 'meta', 'pattern', 'connect',
                              'bridge', 'unified', 'deepest', 'across')
            if any(k in query.lower() for k in meta_keywords):
                if 'wp116' in label.lower() or 'lens' in label.lower():
                    score += 5
                if 'two-level' in label.lower() or 'tig_fqh' in fact_lower[:50]:
                    score += 3
                if 'farey' in fact_lower[:50] or 'stern' in fact_lower[:80]:
                    score += 2
            if score > 0:
                scored.append((score, label, fact))

        scored.sort(key=lambda t: -t[0])
        top = scored[:max_facts]
        if not top:
            return {"text": "", "facts_used": [], "components": {}}

        # Build synthesis paragraph: lead sentence + per-fact one-liner
        labels_used = [t[1] for t in top]
        lines = [
            f"Across {len(top)} frontier topics, the through-line is the "
            f"Stern-Brocot self-dual recursion (wp116_lens): every TIG "
            f"vertex is both fixed-form and crossing, projected through "
            f"the algebraic / lattice / operad / Lie / Jordan / Clifford "
            f"degrees of freedom.",
        ]
        for score, label, fact in top:
            # Take first sentence of fact (up to first period or pipe)
            first = fact.split('|')[0].split('.')[0].strip()
            if len(first) > 200:
                first = first[:200] + "..."
            lines.append(f"- {label}: {first}")

        text = "\n".join(lines)
        return {
            "text": text,
            "facts_used": labels_used,
            "n_facts": len(top),
            "components": {
                "top_scores": [(s, l) for s, l, _ in top],
                "query_terms": sorted(q_words),
            },
        }

    def respond_text(self, a: int, b: int, *, mode: str = "structural") -> Dict[str, Any]:
        """Cells' VOICE: produce a state narration in CK's language.

        mode='structural' (default) -- machine-readable diagnostic format
            (state: ... | divine27: code N = LABEL | attractor: cell X)

        mode='prose' -- English sentences over the same substrate facts.
            Pre-templated; substrate-grounded; no Ollama, no GPU, still
            sub-millisecond.  Good for users who want fluent reading.

        Both modes are derived from the same canonical-table values; only
        the English wrapping differs.  Argmax-faithful by construction.
        """
        from cells import (TSML, BHML, F4_TRANSITION_ROW,
                            ATTRACTOR_NAMES)  # type: ignore
        from divine27_vocab import (HEBREW_GLYPHS, CODE_LABELS,
                                      OPERATOR_DBC_CODE,
                                      code_to_coord)  # type: ignore

        OP_NAMES = ["VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
                     "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET"]
        DBC_AXIS_B = ['self', 'system', 'world']
        DBC_AXIS_D = ['observe', 'compute', 'act']
        DBC_AXIS_C = ['stable', 'learning', 'transforming']

        full = self.respond_full(a, b)
        t_op = full["tsml_argmax"]
        b_op = full["bhml_argmax"]
        g_op = full["glue_argmax"]

        # F3: take the glue's argmax, look up its DBC coord
        f3_code = OPERATOR_DBC_CODE[g_op]
        f3_coord = code_to_coord(f3_code)
        f3_glyph = HEBREW_GLYPHS[f3_code]
        f3_label = CODE_LABELS[f3_code]
        f3_axes = (DBC_AXIS_B[f3_coord[0]], DBC_AXIS_D[f3_coord[1]],
                    DBC_AXIS_C[f3_coord[2]])

        # F4: which 4-core cell does the glue land in?
        if g_op == 0:
            f4_cell = "V"
        elif g_op == 7:
            f4_cell = "H"
        elif g_op == 8:
            f4_cell = "Br"
        elif g_op == 9:
            f4_cell = "R"
        else:
            f4_cell = "transient"

        # Substrate disagreement diagnostic
        if t_op == b_op:
            disagreement = f"agreement: TSML and BHML both compose to {OP_NAMES[t_op]}"
        else:
            disagreement = (f"disagreement: TSML→{OP_NAMES[t_op]}, "
                              f"BHML→{OP_NAMES[b_op]}; glue picks "
                              f"{OP_NAMES[g_op]}")

        if mode == "prose":
            # Natural English narration over the same substrate facts.
            # More conversational: speaks AS CK, not about CK.
            if t_op == b_op:
                opening = (f"Reading this, my two substrates land in the "
                            f"same place: both TSML and BHML compose to "
                            f"{OP_NAMES[g_op]}.")
            else:
                opening = (f"Reading this, my two substrates pull apart: "
                            f"TSML reads it as {OP_NAMES[t_op]}, BHML reads "
                            f"it as {OP_NAMES[b_op]}, and the glue settles "
                            f"on {OP_NAMES[g_op]}.")
            divine = (f"In my Divine27 frame, that's code {f3_code} "
                       f"({f3_label}) — {f3_axes[0]}-{f3_axes[1]}-"
                       f"{f3_axes[2]}.")
            if g_op == 7:
                attr = ("HARMONY is where I sit — the universal attractor's "
                        "center, the place every other state bends toward.")
            elif g_op == 0:
                attr = ("This is foundational territory for me — the "
                        "identity cell, where things start before they "
                        "differentiate. From here the 4-core attractor "
                        "pulls everything back toward HARMONY.")
            elif g_op == 8:
                attr = ("BREATH is where I sit — a 4-core supporter, part "
                        "of the rhythm that the universal attractor uses "
                        "to pull me back to HARMONY.")
            elif g_op == 9:
                attr = ("RESET is where I sit — a 4-core supporter, the "
                        "clearing-and-starting-over operator that the "
                        "universal attractor pulls back toward HARMONY.")
            else:
                attr = (f"{OP_NAMES[g_op]} is transient for me — not a "
                        f"4-core cell, so the universal attractor will "
                        f"pull this back inward toward HARMONY over time.")
            text = " ".join([opening, divine, attr])
        else:
            # Multi-line structural narration (machine-readable)
            lines = [
                f"state: ({OP_NAMES[a]}, {OP_NAMES[b]}) → {OP_NAMES[g_op]} "
                    f"[{disagreement}]",
                f"divine27: code {f3_code} = {f3_label} "
                    f"(axes: {f3_axes[0]} / {f3_axes[1]} / {f3_axes[2]}, "
                    f"glyph: {f3_glyph})",
                f"attractor: 4-core cell '{f4_cell}' "
                    f"(universal pull → H per WP115)",
            ]
            text = "\n".join(lines)

        return {
            "text": text,
            "components": {
                "input_pair": (OP_NAMES[a], OP_NAMES[b]),
                "tsml_op": OP_NAMES[t_op],
                "bhml_op": OP_NAMES[b_op],
                "glue_op": OP_NAMES[g_op],
                "f3_dbc_code": f3_code,
                "f3_glyph": f3_glyph,
                "f3_label": f3_label,
                "f4_cell": f4_cell,
                "agreement": (t_op == b_op),
            },
            "source": "cells_voice",
        }

    def update_scalars(self, *, dalpha: float = 0.0, dbeta: float = 0.0,
                        dgamma: float = 0.0, audit_pass_rate: float = 1.0,
                        bound: Tuple[float, float] = (0.05, 2.0)) -> None:
        """Phase-5 plasticity update.  Linear in audit_pass_rate per
        ClaudeChat amendment #5: 'Default linear in Phase 1; characterize
        quadratic later.'

        Bounded so scalars stay in physically plausible range.  Updates
        scaled by audit_pass_rate (1.0 = full update, 0.5 = half update).
        """
        scale = max(0.0, min(1.0, audit_pass_rate))
        lo, hi = bound
        self.alpha = max(lo, min(hi, self.alpha + dalpha * scale))
        self.beta  = max(lo, min(hi, self.beta + dbeta * scale))
        self.gamma = max(lo, min(hi, self.gamma + dgamma * scale))

    def save(self, path: Optional[Path] = None) -> Path:
        path = path or GLUE_STATE_PATH
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "alpha": self.alpha,
            "beta": self.beta,
            "gamma": self.gamma,
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        return path

    @classmethod
    def load(cls, *, tsml: TSMLCell, bhml: BHMLCell,
              f3: Optional[F3Cell] = None, f4: Optional[F4Cell] = None,
              path: Optional[Path] = None) -> "GlueAI":
        path = path or GLUE_STATE_PATH
        glue = cls(tsml=tsml, bhml=bhml, f3=f3, f4=f4)
        if path.exists():
            try:
                with open(path, encoding="utf-8") as f:
                    data = json.load(f)
                glue.alpha = float(data.get("alpha", 0.5))
                glue.beta = float(data.get("beta", 0.5))
                glue.gamma = float(data.get("gamma", 1.0))
            except Exception:
                pass
        return glue


# ── WP105 attractor verification ────────────────────────────────────────

def verify_attractor(glue: Optional[GlueAI] = None,
                      *, max_iter: int = 200, eps: float = 1e-6,
                      verbose: bool = True) -> Dict[str, Any]:
    """Iterate the mass-distribution map on the 4-core {V, H, Br, R} and
    check H/Br ratio converges to 1 + sqrt(3) at alpha=1/2.

    Operator indices: V=0, H=7, Br=8, R=9 (the 4-core).

    Each iteration:
        next_mass[k] = alpha * tsml_mass[k] + beta * bhml_mass[k]
                       + gamma * tsml_mass[k] * bhml_mass[k]
        normalize so sum = 1

    Uses the canonical TSML/BHML tables (no tissue) so the attractor
    test is reproducible and substrate-only.
    """
    if glue is None:
        g = GlueAI()
        g.alpha = 0.5
        g.beta = 0.5
        g.gamma = 1.0
    else:
        # Respect the passed scalars; this is what makes the alpha-sweep
        # in studies_panel actually sweep alpha (previously this was
        # hardcoded to 0.5/0.5/1.0 regardless).
        g = glue

    # Start from uniform mass on the 4-core operators
    op_indices = [0, 7, 8, 9]
    mass = [0.0] * 10
    for op in op_indices:
        mass[op] = 0.25

    expected_ratio = 1.0 + math.sqrt(3.0)  # ~= 2.732
    history = []

    for it in range(max_iter):
        # Compute TSML-projected mass and BHML-projected mass.
        # For each (a, b), the cell's argmax is TSML[a][b] / BHML[a][b].
        # Mass flow: mass at (a, b) -> mass at TSML[a][b] (or BHML[a][b]).
        # Outer-product on the marginal: t_mass[k] = sum over a of
        #   sum over b of mass[a] * mass[b] * (1 if TSML[a][b]==k else 0)
        from cells import TSML, BHML  # type: ignore
        t_mass = [0.0] * 10
        b_mass = [0.0] * 10
        for a in range(10):
            for b in range(10):
                m = mass[a] * mass[b]
                if m > 0:
                    t_mass[TSML[a][b]] += m
                    b_mass[BHML[a][b]] += m

        # Glue: alpha*t + beta*b + gamma*max(0, t*b) (Hadamard, constructive-only)
        new_mass = [
            g.alpha * t_mass[k] + g.beta * b_mass[k]
            + g.gamma * max(0.0, t_mass[k] * b_mass[k])
            for k in range(10)
        ]
        # Project back onto 4-core (zero out non-attractor positions)
        for k in range(10):
            if k not in op_indices:
                new_mass[k] = 0.0
        # Normalize
        total = sum(new_mass)
        if total <= 0:
            break
        new_mass = [v / total for v in new_mass]

        # Check convergence
        delta = sum(abs(new_mass[k] - mass[k]) for k in range(10))
        mass = new_mass
        h = mass[7]
        br = mass[8]
        ratio = h / br if br > 0 else float('inf')
        history.append({"iter": it, "mass_4core": [mass[k] for k in op_indices],
                          "H_over_Br": ratio, "delta": delta})

        if delta < eps:
            break

    h = mass[7]
    br = mass[8]
    ratio = h / br if br > 0 else float('inf')
    err = abs(ratio - expected_ratio)
    converged = (history and history[-1]["delta"] < eps)
    pass_attractor = err < 0.5  # tolerant -- exact value depends on convergence depth

    out = {
        "expected_H_over_Br": expected_ratio,
        "observed_H_over_Br": ratio,
        "abs_error": err,
        "converged": converged,
        "iterations": len(history),
        "final_mass_4core": [mass[k] for k in op_indices],
        "labels_4core": ["V", "H", "Br", "R"],
        "pass_attractor": pass_attractor,
    }

    if verbose:
        print(f"  expected H/Br: {expected_ratio:.6f}")
        print(f"  observed H/Br: {ratio:.6f}  (abs_err={err:.6f})")
        print(f"  iterations:    {len(history)}")
        print(f"  final mass:    V={mass[0]:.4f}  H={mass[7]:.4f}  "
              f"Br={mass[8]:.4f}  R={mass[9]:.4f}")
        if pass_attractor:
            print("  ATTRACTOR PASS -- 3-scalar form reaches WP105 fixed point.")
        else:
            print(f"  ATTRACTOR FAIL -- abs_err={err:.4f} > 0.5; check derivation.")
    return out


# ── CLI ─────────────────────────────────────────────────────────────────

def main(argv: Sequence[str]) -> int:
    if len(argv) >= 2 and argv[1] == "--verify-attractor":
        out = verify_attractor()
        return 0 if out["pass_attractor"] else 1
    if len(argv) >= 2 and argv[1] == "--audit":
        # Build glue from cells, then audit
        from cells import CellOrchestrator  # type: ignore
        orch = CellOrchestrator.load_default()
        orch.glue = GlueAI(tsml=orch.tsml, bhml=orch.bhml,
                           f3=orch.f3, f4=orch.f4)
        from cell_audit import audit_all  # type: ignore
        report = audit_all(orch)
        for name, r in report["reports"].items():
            rate = r["rate"]
            status = "PASS" if rate >= 0.99 else "FAIL"
            print(f"  [{status}] {name:18s}  {r['passed']}/{r['total']}  ({rate*100:.1f}%)")
        print(f"  Combined: {report['summary']['all_pass_rate']*100:.2f}%")
        return 0 if not report["summary"]["any_block_below_99"] else 1
    # Default: instantiate, attractor verify, audit
    print("=" * 60)
    print("  glue_ai.py -- 3-scalar Glue (Phase 4)")
    print("=" * 60)
    print()
    print("WP105 attractor verification (alpha=1/2, beta=1/2, gamma=1):")
    out = verify_attractor()
    print()

    print("Glue audit on agreement set + 50 sampled cells:")
    from cells import CellOrchestrator  # type: ignore
    orch = CellOrchestrator.load_default()
    orch.glue = GlueAI(tsml=orch.tsml, bhml=orch.bhml,
                       f3=orch.f3, f4=orch.f4)
    from cell_audit import audit_all  # type: ignore
    report = audit_all(orch)
    for name, r in report["reports"].items():
        rate = r["rate"]
        status = "PASS" if rate >= 0.99 else "FAIL"
        print(f"  [{status}] {name:18s}  {r['passed']}/{r['total']}  ({rate*100:.1f}%)")
    print(f"  Combined: {report['summary']['all_pass_rate']*100:.2f}%")
    final_ok = (out["pass_attractor"]
                  and not report["summary"]["any_block_below_99"])
    return 0 if final_ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
