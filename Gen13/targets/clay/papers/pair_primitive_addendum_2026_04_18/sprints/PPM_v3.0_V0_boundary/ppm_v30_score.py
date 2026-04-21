"""
PPM-v3.0 V0 boundary checkpoint scoring.
Applies four-source rubric under two Source-3 sensitivity branches (S3a, S3b).
Robustness rule decides final verdict.

Deterministic. No RNG. No tuning.
"""
import json

# V0 data on Z/10 — from CANONICAL_TSML_CONSTRUCTION.md Rule (b)
# 19 cells touching vertex 0
V0_CELLS = []
for y in range(10):
    V0_CELLS.append((0, y))
    if y != 0:
        V0_CELLS.append((y, 0))

h = 7  # attractor on Z/10

# Partition V0 by output
V0_Z = [c for c in V0_CELLS if h not in c]   # 17 zero-output cells
V0_H = [c for c in V0_CELLS if h in c]       # 2 HARMONY-output cells

# Verification (§2 of pre-reg)
assert len(V0_CELLS) == 19
assert len(V0_Z) == 17
assert len(V0_H) == 2
assert set(V0_H) == {(0, 7), (7, 0)}

print("="*70)
print("V0 structural facts verified:")
print(f"  |V0| = {len(V0_CELLS)}")
print(f"  |V0_Z| (zero-output) = {len(V0_Z)} — {len(V0_Z)/len(V0_CELLS)*100:.1f}%")
print(f"  |V0_H| (HARMONY-output) = {len(V0_H)} — cells {V0_H}")
print("="*70)
print()

# ============================================================
# Source 1 — V0 rule-majority / default-behavior backbone
# Criterion: majority (>=50%) AND alignment with V0's constructed default
# ============================================================
V0_Z_majority = len(V0_Z) / len(V0_CELLS) >= 0.5
V0_H_majority = len(V0_H) / len(V0_CELLS) >= 0.5
# Rule (b): zero-absorption is the DEFAULT; HARMONY is the OVERRIDE
V0_Z_aligns_default = True   # V0_Z is the zero-absorption default
V0_H_aligns_default = False  # V0_H is the override, not the default

V0_Z_is_backbone = V0_Z_majority and V0_Z_aligns_default
V0_H_is_backbone = V0_H_majority and V0_H_aligns_default

# Map-V0-I (persistent=V0_Z):
if V0_Z_is_backbone:
    s1_I = +1
elif V0_H_is_backbone:
    s1_I = -1
else:
    s1_I = 0
# Map-V0-II (persistent=V0_H):
if V0_H_is_backbone:
    s1_II = +1
elif V0_Z_is_backbone:
    s1_II = -1
else:
    s1_II = 0

print(f"Source 1 — Rule-majority / default backbone:")
print(f"  V0_Z: majority={V0_Z_majority} (17/19), aligns-default={V0_Z_aligns_default}, backbone={V0_Z_is_backbone}")
print(f"  V0_H: majority={V0_H_majority} (2/19), aligns-default={V0_H_aligns_default}, backbone={V0_H_is_backbone}")
print(f"  Map-V0-I score: {s1_I:+d}")
print(f"  Map-V0-II score: {s1_II:+d}")
print()

# ============================================================
# Source 2 — Exception-structure reading
# Criterion: excluded-side is localized exception iff
#   (a) minority count AND (b) default-rule override AND (c) restricted to distinguished element
# ============================================================
V0_Z_minority = len(V0_Z) / len(V0_CELLS) < 0.5
V0_H_minority = len(V0_H) / len(V0_CELLS) < 0.5
V0_Z_is_override = False  # V0_Z is the default, not the override
V0_H_is_override = True   # V0_H is the Rule (b) override
V0_Z_restricted_to_h = False  # V0_Z touches every element except h (actually it does touch h via (0,0)... wait)
# Let me check: V0_Z is V0 cells NOT in V0_H. V0_H = {(0,7),(7,0)}. 
# V0_Z includes (0,0), (0,1), (0,2), ..., (0,6), (0,8), (0,9), (1,0), ..., (9,0) minus (7,0)
# So V0_Z touches vertices 0,1,2,3,4,5,6,8,9 — does NOT touch vertex 7. That's the key distinction.
# But "restricted to distinguished element" criterion is about the EXCLUDED side touching only one distinguished element.
# V0_H = {(0,7), (7,0)} — both cells touch vertex 7 (=h). Restricted to h.
# V0_Z has 9 distinct non-h vertices. Not restricted to a distinguished element.
V0_H_restricted_to_h = True
V0_Z_restricted_to_distinguished = False  # V0_Z spans 9 vertices

V0_Z_is_localized_exception = V0_Z_minority and V0_Z_is_override and V0_Z_restricted_to_distinguished
V0_H_is_localized_exception = V0_H_minority and V0_H_is_override and V0_H_restricted_to_h

# Map-V0-I (excluded=V0_H):
if V0_H_is_localized_exception:
    s2_I = +1
elif V0_Z_is_localized_exception:
    s2_I = -1
else:
    s2_I = 0
# Map-V0-II (excluded=V0_Z):
if V0_Z_is_localized_exception:
    s2_II = +1
elif V0_H_is_localized_exception:
    s2_II = -1
else:
    s2_II = 0

print(f"Source 2 — Exception-structure reading:")
print(f"  V0_Z: minority={V0_Z_minority}, is-override={V0_Z_is_override}, restricted-to-distinguished={V0_Z_restricted_to_distinguished}")
print(f"    → localized-exception={V0_Z_is_localized_exception}")
print(f"  V0_H: minority={V0_H_minority}, is-override={V0_H_is_override}, restricted-to-h={V0_H_restricted_to_h}")
print(f"    → localized-exception={V0_H_is_localized_exception}")
print(f"  Map-V0-I score: {s2_I:+d}")
print(f"  Map-V0-II score: {s2_II:+d}")
print()

# ============================================================
# Source 3a — Attractor privilege → excluded-side (hold at boundary)
# Criterion: h's V0-privilege manifests as surviving distinction at boundary;
# "hold" content = localized, distinguished, not-absorbed-by-default → excluded-side
# The attractor-privilege cells are V0_H.
# ============================================================
# Map-V0-I: excluded=V0_H (attractor cells at excluded) → coheres with S3a
# Map-V0-II: persistent=V0_H (attractor cells at persistent = backbone) → contradicts Rule (b)
s3a_I = +1
s3a_II = -1

# ============================================================
# Source 3b — Attractor privilege → persistent-side (gravity well)
# Criterion: h is "where structure gathers"; V0_H cells preserve h at boundary;
# "persistent at attractor" → persistent-side
# ============================================================
# Map-V0-I: persistent=V0_Z (does NOT contain attractor-privilege cells) → -1
# Map-V0-II: persistent=V0_H (contains attractor-privilege cells) → +1
s3b_I = -1
s3b_II = +1

print(f"Source 3a — Attractor privilege → excluded-side:")
print(f"  Map-V0-I (excluded=V0_H): coheres, score {s3a_I:+d}")
print(f"  Map-V0-II (persistent=V0_H): contradicts Rule (b), score {s3a_II:+d}")
print()
print(f"Source 3b — Attractor privilege → persistent-side:")
print(f"  Map-V0-I (persistent=V0_Z): persistent lacks attractor-privilege, score {s3b_I:+d}")
print(f"  Map-V0-II (persistent=V0_H): persistent has attractor-privilege, score {s3b_II:+d}")
print()

# ============================================================
# Source 4 — Pair-object symmetry
# Criterion: excluded-side has pair-object signature iff exactly 2 cells, swap-symmetric
# ============================================================
# V0_H = {(0,7), (7,0)} — exactly 2 cells, swap-symmetric under (x,y)→(y,x). Match.
# V0_Z = 17 cells — not 2 cells. Does not match.
V0_H_is_pair_object = (len(V0_H) == 2) and set((y,x) for (x,y) in V0_H) == set(V0_H)
V0_Z_is_pair_object = (len(V0_Z) == 2) and set((y,x) for (x,y) in V0_Z) == set(V0_Z)

# Map-V0-I (excluded=V0_H):
if V0_H_is_pair_object:
    s4_I = +1
elif V0_Z_is_pair_object:
    s4_I = -1
else:
    s4_I = 0
# Map-V0-II (excluded=V0_Z):
if V0_Z_is_pair_object:
    s4_II = +1
elif V0_H_is_pair_object:
    s4_II = -1
else:
    s4_II = 0

print(f"Source 4 — Pair-object symmetry:")
print(f"  V0_H pair-object: {V0_H_is_pair_object} (exactly 2 cells, swap-symmetric)")
print(f"  V0_Z pair-object: {V0_Z_is_pair_object} ({len(V0_Z)} cells)")
print(f"  Map-V0-I score: {s4_I:+d}")
print(f"  Map-V0-II score: {s4_II:+d}")
print()

# ============================================================
# Aggregate per branch
# ============================================================
# Fixed subtotal
fixed_I = s1_I + s2_I + s4_I
fixed_II = s1_II + s2_II + s4_II

# Under S3a
agg_S3a_I = fixed_I + s3a_I
agg_S3a_II = fixed_II + s3a_II
gap_S3a = abs(agg_S3a_I - agg_S3a_II)

# Under S3b
agg_S3b_I = fixed_I + s3b_I
agg_S3b_II = fixed_II + s3b_II
gap_S3b = abs(agg_S3b_I - agg_S3b_II)

print("="*70)
print("Per-branch aggregates:")
print(f"{'':15}  {'Map-V0-I':>10}  {'Map-V0-II':>10}  {'Gap':>6}")
print(f"{'Fixed (S1+S2+S4)':15}  {fixed_I:>+10d}  {fixed_II:>+10d}")
print(f"{'Under S3a':15}  {agg_S3a_I:>+10d}  {agg_S3a_II:>+10d}  {gap_S3a:>6d}")
print(f"{'Under S3b':15}  {agg_S3b_I:>+10d}  {agg_S3b_II:>+10d}  {gap_S3b:>6d}")
print("="*70)

# ============================================================
# Per-branch verdict (§7.1)
# ============================================================
def branch_verdict(agg_I, agg_II, gap):
    if agg_I >= 3 and agg_II <= 1 and gap >= 2:
        return "PASS-V0-I"
    if agg_II >= 3 and agg_I <= 1 and gap >= 2:
        return "PASS-V0-II"
    if agg_I < 3 and agg_II < 3:
        return "FAIL"
    # One map >=+3 but gap<2 OR both in {+2,+3} with gap<2
    return "UNCLEAR"

v_S3a = branch_verdict(agg_S3a_I, agg_S3a_II, gap_S3a)
v_S3b = branch_verdict(agg_S3b_I, agg_S3b_II, gap_S3b)

print()
print(f"Branch verdict under S3a: {v_S3a}")
print(f"Branch verdict under S3b: {v_S3b}")

# ============================================================
# Final verdict (§7.2 robustness rule)
# ============================================================
if v_S3a == v_S3b:
    if v_S3a == "PASS-V0-I":
        final = "Robust PASS-V0-I"
    elif v_S3a == "PASS-V0-II":
        final = "Robust PASS-V0-II"
    elif v_S3a == "FAIL":
        final = "Robust FAIL"
    elif v_S3a == "UNCLEAR":
        final = "Robust UNCLEAR"
else:
    final = "UNCLEAR by Sensitivity"

print()
print("="*70)
print(f"FINAL VERDICT: {final}")
print("="*70)

# Write JSON
out = {
    "spec_version": "PPM-v3.0 (revised, Source-3 sensitivity branch)",
    "scope": "Path 1 local — V0 boundary checkpoint on Z/10",
    "V0_structure": {
        "total_cells": len(V0_CELLS),
        "V0_Z_size": len(V0_Z),
        "V0_H": list(V0_H),
    },
    "per_source_scores": {
        "source_1": {"Map-V0-I": s1_I, "Map-V0-II": s1_II,
                     "rationale": "V0_Z meets majority + default alignment; V0_H meets neither."},
        "source_2": {"Map-V0-I": s2_I, "Map-V0-II": s2_II,
                     "rationale": "V0_H meets all three criteria (minority, override, restricted to h); V0_Z meets none."},
        "source_3a": {"Map-V0-I": s3a_I, "Map-V0-II": s3a_II,
                      "rationale": "Attractor privilege at excluded-side = hold at boundary = coherent under Map-V0-I."},
        "source_3b": {"Map-V0-I": s3b_I, "Map-V0-II": s3b_II,
                      "rationale": "Attractor privilege at persistent-side = gravity well = coherent under Map-V0-II."},
        "source_4": {"Map-V0-I": s4_I, "Map-V0-II": s4_II,
                     "rationale": "V0_H is exactly 2 swap-symmetric cells; V0_Z is 17 cells."},
    },
    "aggregates": {
        "fixed_subtotal_Map-V0-I": fixed_I,
        "fixed_subtotal_Map-V0-II": fixed_II,
        "under_S3a": {"Map-V0-I": agg_S3a_I, "Map-V0-II": agg_S3a_II, "gap": gap_S3a},
        "under_S3b": {"Map-V0-I": agg_S3b_I, "Map-V0-II": agg_S3b_II, "gap": gap_S3b},
    },
    "branch_verdicts": {"S3a": v_S3a, "S3b": v_S3b},
    "final_verdict": final,
}
with open('/home/claude/foundation_sprint/ppm_v30/PPM_V30_V0_SCORES.json', 'w') as f:
    json.dump(out, f, indent=2)
print()
print("Wrote PPM_V30_V0_SCORES.json")
