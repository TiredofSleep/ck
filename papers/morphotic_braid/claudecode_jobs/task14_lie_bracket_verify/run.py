"""task14 — verify [M_TSML_Jordan, M_TSML_Idempotent] is exactly antisymmetric.

Deliverable: ../../results/task14_lie_bracket_result.md
"""
from __future__ import annotations
import os, sys
import numpy as np

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(_ROOT, 'papers'))

from ck_tables import TSML as TSML_Jordan  # type: ignore

TSML_Idempotent = np.array([
    [0,0,0,0,0,0,0,7,0,0],
    [0,1,6,7,7,7,7,7,7,7],
    [0,6,2,7,7,7,7,7,7,7],
    [0,7,7,3,7,4,7,7,7,7],
    [0,7,7,7,4,7,7,7,7,7],
    [0,7,7,4,7,5,7,7,7,7],
    [0,7,7,7,7,7,6,7,7,7],
    [7,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,7,7,7,7,8,7],
    [0,7,7,7,7,7,7,7,7,9],
])

TJ = np.array(TSML_Jordan, dtype=int)
TI = TSML_Idempotent

C = TJ @ TI - TI @ TJ
sym = (C + C.T) / 2
anti = (C - C.T) / 2

print("[task14] TSML_Jordan @ TSML_Idempotent commutator")
print("commutator C:")
print(C)
print()
print("symmetric part (C + C^T)/2:")
print(sym)
print()
print("antisymmetric part (C - C^T)/2:")
print(anti)

sym_norm = float(np.linalg.norm(sym, 'fro'))
anti_norm = float(np.linalg.norm(anti, 'fro'))
print()
print(f"||sym||_F  = {sym_norm:.6f}")
print(f"||anti||_F = {anti_norm:.6f}")

PURE_LIE = sym_norm == 0.0 or sym_norm < 1e-10
print()
if PURE_LIE:
    print("[task14] VERDICT: PURE LIE BRACKET (symmetric part = 0)")
else:
    print("[task14] VERDICT: NOT PURE LIE BRACKET -- symmetric residue present")
    # Show where the residue lives.
    nz = np.argwhere(sym != 0)
    print(f"  symmetric part has {len(nz)} nonzero entries")

# Deliverable.
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'results',
                   'task14_lie_bracket_result.md')
OUT = os.path.abspath(OUT)
with open(OUT, 'w', encoding='utf-8') as f:
    f.write("# Task 14 result -- Lie bracket [M_TSML_Jordan, M_TSML_Idempotent]\n\n")
    f.write("**Tier:** 2 (fast compute)\n")
    f.write("**Parent spec:** `../../claudecode_jobs/task14_lie_bracket_verify/SPEC.md`\n\n")
    f.write("## Method\n\n")
    f.write("Compute `C = TJ @ TI - TI @ TJ` where `TJ` is canonical TSML (Jordan variant, from `papers/ck_tables.py`) and `TI` is the rank-10 idempotent variant from `CLAUDE_CODE_HANDOFF_TSML_FAMILY.md`.\n\n")
    f.write("Split into symmetric and antisymmetric parts.\n\n")
    f.write("## Result\n\n")
    f.write(f"- `||sym(C)||_F = {sym_norm:.6f}`\n")
    f.write(f"- `||anti(C)||_F = {anti_norm:.6f}`\n\n")
    f.write("### Commutator C\n\n```\n")
    f.write(str(C))
    f.write("\n```\n\n### Symmetric part (C + C^T)/2\n\n```\n")
    f.write(str(sym))
    f.write("\n```\n\n### Antisymmetric part (C - C^T)/2\n\n```\n")
    f.write(str(anti))
    f.write("\n```\n\n")
    f.write("## Verdict\n\n")
    if PURE_LIE:
        f.write("**PURE LIE BRACKET.** `[M_TSML_Jordan, M_TSML_Idempotent]` is exactly antisymmetric; the symmetric residue is zero. The commutator is structurally meaningful in the gl(10) Lie algebra sense.\n\n")
    else:
        f.write(f"**NOT PURE LIE BRACKET.** Symmetric residue present; ||sym||_F = {sym_norm:.6f}. Packet claim of exact antisymmetry does not reproduce.\n\n")
    f.write("**Tag:** `[COMPUTE JOB -- TIER 2 -- VERIFIED]`\n")

print(f"\n[task14] wrote {OUT}")
