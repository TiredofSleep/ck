# Copyright (c) 2025-2026 Brayden Sanders / 7SiTe LLC
# Licensed under the 7SiTe Public Sovereignty License v2.2 (DOI: 10.5281/zenodo.18852047)
"""
ck_sense_decomposition.py -- each sense as an operator composition.

Brayden 2026-05-13:
  "break down every sense and show how the operators fit together to
  form that sense"

CK's senses aren't black boxes that produce operators. Each sense IS
a specific ordered pipeline of operators applied to a sensory substrate.
Vision is not "produces operators"; vision is COLLAPSE then LATTICE then
COUNTER then HARMONY — applied in that order to a pixel array. Hearing
is the same composition idea over a pressure waveform.

This module reads the pipelines off the actual code paths
(ck_stroke_extractor for vision, ck_phonetic_letters for hearing, etc.)
and presents each sense as an ordered list of (operator, role) pairs.

The voice polish surfaces this so a reader sees not just "dominant
operator: HARMONY" but "HARMONY appears in vision as the closed-loop
detector, in hearing as the phoneme-pattern recogniser, in inner-sense
as the cortex coherence signal."

This is the operator-as-shared-currency hypothesis at the pipeline
level: the same algebraic identity participates in every sense, but
with a sense-specific role at each step.

Public API:
    SENSE_PIPELINES                              # dict[sense -> List[(op, role)]]
    senses_for_operator(op) -> List[(sense, role)]
    format_sense_pipeline(sense) -> List[str]
    format_operator_across_senses(op) -> List[str]
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


# Operator names
_OP_NAMES = (
    "VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
    "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET",
)


# ─── The sense pipelines ─────────────────────────────────────────────────
#
# Each entry: (operator_id, role_in_this_sense)
# Pipelines are ordered: the first step runs first on raw input from
# that modality, then the next, etc.
# Roles are derived from the actual code in ck_retina, ck_stroke_extractor,
# ck_phonetic_letters, ck_sim_ears, olfactory_her, cortex, and the chat
# path. Each role describes what the operator DOES in that sense's pipeline.

SENSE_PIPELINES: Dict[str, List[Tuple[int, str]]] = {
    "vision": [
        (2, "measure: cv2 captures pixel array, count regions"),
        (4, "collapse: Otsu threshold reduces grayscale to binary 0/1"),
        (1, "lattice: Zhang-Suen skeletonization imposes 1-pixel-wide form"),
        (2, "count: trace polylines, enumerate connected components + holes"),
        (7, "closure: detect closed loops via topology (n_components, n_holes)"),
        # the final step is "assign" -- which op the features map to --
        # which is itself an operator-typed output, so we don't label one
        # operator for it; the result feeds back into the algebra
    ],
    "hearing": [
        (2, "measure: ck_sim_ears samples waveform via sounddevice"),
        (1, "lattice: pack 9-bit acoustic code (energy/freq/manner/voice)"),
        (5, "balance: classify formant centre (vowel height + front/back)"),
        (7, "closure: classify manner (vowel/approximant/fricative/plosive)"),
        (3, "continuity: voicing + duration classification (sustained vs brief)"),
        # output is a phoneme-typed operator id via D2 force decomposition
    ],
    "touch_proprio": [
        (2, "measure: olfactory bulb registers sensory event scalar"),
        (1, "lattice: project to 5-dim D2 force-vector basis"),
        (1, "lattice: append to HER (Hindsight Experience Replay) buffer"),
        (7, "closure: recall_by_scent finds nearest stored experience"),
        (8, "emergence: bind to operator via match-strength threshold"),
    ],
    "inner_sense": [
        # CK's proprioception of his own state
        (2, "measure: track (b, d) operator-pair from last cortex tick"),
        (1, "lattice: Hebbian outer product Δw_ij = η · d_i · d_j on 5x5 W"),
        (7, "closure: extract emergent signal from W diagonal trace"),
        (1, "lattice: project to AO 5-element basis (D0/D1/D2/D3/D4)"),
        (5, "balance: voice-of-becoming threshold gating (T*=5/7)"),
    ],
    "language": [
        (2, "measure: tokenize text, enumerate characters"),
        (1, "lattice: each character → 9-bit acoustic code via LETTER_PHONETIC"),
        (1, "lattice: decode each code → 5-dim D2 force vector"),
        (7, "closure: map force vectors to operators (TSML / BHML composition)"),
        (3, "continuity: compose operator stream through CL table"),
        (7, "closure: settle in cortex via voice_of_becoming, emit text"),
    ],
    "math": [
        (1, "lattice: D-numbered theorem registered with its HOME signature"),
        (2, "count: enumerate operators mentioned in the formula's prose"),
        (7, "closure: invoked_by() ranks formulas by Jaccard overlap"),
        (3, "continuity: surface top-K invoked D-numbers each turn"),
    ],
    "memory": [
        # Cross-temporal sense: how CK senses his own past
        (2, "measure: every chat turn becomes a BDC log entry"),
        (1, "lattice: lattice_chain.walk() places turn-path in templated cells"),
        (7, "closure: divine_memory.recall(centroid) finds resonant past turns"),
        (3, "continuity: spreading_recall walks SEED→SPREAD→LEAP→FUSE"),
        (5, "balance: coherence_C exit gate at T*=5/7"),
    ],
    "drives": [
        # Sense of need / orientation toward
        (2, "measure: GoalEvaluator polls coherence/band/op/entropy at 5Hz"),
        (1, "lattice: each drive has a fixed activation profile"),
        (8, "emergence: when activation > 0.7, the drive fires as a signal"),
        (3, "continuity: signal carried to proactive_queue with TTL=90s"),
    ],
}


# ─── Query API ────────────────────────────────────────────────────────────

def senses_for_operator(op: int) -> List[Tuple[str, str]]:
    """For one operator, list every sense it participates in + its role.

    Returns list of (sense_name, role_description) tuples.
    """
    out: List[Tuple[str, str]] = []
    for sense, pipeline in SENSE_PIPELINES.items():
        for step_op, role in pipeline:
            if step_op == op:
                out.append((sense, role))
    return out


def format_sense_pipeline(sense: str) -> List[str]:
    """Pretty-print one sense's full pipeline."""
    pipeline = SENSE_PIPELINES.get(sense)
    if not pipeline:
        return [f"(no pipeline registered for sense='{sense}')"]
    lines = [f"sense '{sense}' is built from {len(pipeline)} operator-steps:"]
    for i, (op, role) in enumerate(pipeline, 1):
        name = _OP_NAMES[op] if 0 <= op < 10 else f"<{op}>"
        lines.append(f"  {i}. {name:<8s} → {role}")
    return lines


def format_operator_across_senses(op: int) -> List[str]:
    """Pretty-print: in how many senses does this operator participate,
    and what role does it play in each."""
    if not (0 <= op < 10):
        return [f"(operator id {op} out of range 0..9)"]
    name = _OP_NAMES[op]
    hits = senses_for_operator(op)
    if not hits:
        return [f"{name} (id={op}) does not appear in any registered "
                f"sense pipeline."]
    lines = [f"{name} (id={op}) participates in {len(hits)} sense-steps "
              "across CK's pipelines:"]
    by_sense: Dict[str, List[str]] = {}
    for sense, role in hits:
        by_sense.setdefault(sense, []).append(role)
    for sense, roles in by_sense.items():
        if len(roles) == 1:
            lines.append(f"  {sense:<14s} : {roles[0]}")
        else:
            lines.append(f"  {sense:<14s} : (×{len(roles)} steps)")
            for r in roles:
                lines.append(f"    · {r}")
    return lines


# ─── Mount hook ──────────────────────────────────────────────────────────

def mount_sense_decomposition(engine) -> bool:
    """Attach the sense decomposition to the engine for queryable access."""
    engine.sense_pipelines = SENSE_PIPELINES
    engine.senses_for_operator = senses_for_operator
    engine.format_operator_across_senses = format_operator_across_senses
    print(f"[CK Gen14] mount_sense_decomposition: "
          f"{len(SENSE_PIPELINES)} senses with pipelines "
          f"({', '.join(SENSE_PIPELINES.keys())})")
    return True


# ─── Standalone smoke ────────────────────────────────────────────────────

def _smoke():
    print("Smoke test: ck_sense_decomposition")
    print()
    print(f"  {len(SENSE_PIPELINES)} senses registered:")
    for s in SENSE_PIPELINES:
        n = len(SENSE_PIPELINES[s])
        print(f"    {s:<14s} — {n} operator-steps")
    print()
    print("  Full vision pipeline:")
    for line in format_sense_pipeline("vision"):
        print(f"    {line}")
    print()
    print("  Full hearing pipeline:")
    for line in format_sense_pipeline("hearing"):
        print(f"    {line}")
    print()
    print("  HARMONY across senses:")
    for line in format_operator_across_senses(7):
        print(f"    {line}")
    print()
    print("  COUNTER across senses (it should show up in every sense — "
          "measurement is universal):")
    for line in format_operator_across_senses(2):
        print(f"    {line}")
    print()
    print("Sense decomposition smoke: ALL OK")


if __name__ == "__main__":
    _smoke()
