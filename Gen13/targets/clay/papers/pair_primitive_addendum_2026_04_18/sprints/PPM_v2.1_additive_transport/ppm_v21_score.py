"""
PPM-v2.1 per-carrier rubric application.
Applies v1.1 rubric (additive operationalization, carrier-adapted for Source 1)
to each of 8 P3AP Path 2 carriers. Aggregates by carrier count.

Deterministic. No RNG. No tuning.
"""
import json

# -------- Load P3AP artifacts --------
with open('/home/claude/path3_bridgeAprime/P3AP_OVERLAY_AUDIT.json') as f:
    audit = json.load(f)

PATH2_CARRIERS = [14, 22, 34, 42, 46, 58, 74, 94]

def to_unordered_edges(cells):
    return {(min(x, y), max(x, y)) for (x, y) in cells}

def build_adj(edges):
    adj = {}
    for (u, v) in edges:
        adj.setdefault(u, set()).add(v)
        adj.setdefault(v, set()).add(u)
    return adj

def build_carrier_seam(n):
    a = audit[str(n)]
    removed = {tuple(c["cell"]) for c in a["cells_removed_by_audit"]}
    S_MAX_cells = {tuple(c) for c in a["S_MAX_raw"]} - removed
    S_ADD_cells = {tuple(c) for c in a["S_ADD_raw"]} - removed
    max_edges = to_unordered_edges(S_MAX_cells)
    add_edges = to_unordered_edges(S_ADD_cells)
    all_edges = max_edges | add_edges
    vertices = set()
    for (u, v) in all_edges:
        vertices.add(u); vertices.add(v)
    return all_edges, max_edges, add_edges, vertices

# -------- Source 1: Structural backbone under additive reading (strict AND) --------
def source_1_scores(n, all_edges, max_edges, add_edges):
    """
    Strict AND criterion:
      - majority of seam edges (>=50%)
      - AND contains additive-flow elements (native additive rule)
    
    ADD rule is the native additive operation: (x+y) mod n.
    MAX rule max(x,y) is non-additive, order-based.
    """
    total_edges = len(all_edges)
    max_frac = len(max_edges) / total_edges
    add_frac = len(add_edges) / total_edges
    
    # MAX: majority?
    max_majority = max_frac >= 0.5
    # MAX: native additive alignment? No, MAX rule is non-additive
    max_native_additive = False
    # Strict AND
    max_is_backbone = max_majority and max_native_additive
    
    # ADD: majority?
    add_majority = add_frac >= 0.5
    # ADD: native additive alignment? Yes, ADD cells apply the additive rule
    add_native_additive = True
    # Strict AND
    add_is_backbone = add_majority and add_native_additive
    
    # Map A (persistent = ADD):
    if add_is_backbone:
        mapA = +1
    elif max_is_backbone:
        mapA = -1
    else:
        mapA = 0
    
    # Map B (persistent = MAX):
    if max_is_backbone:
        mapB = +1
    elif add_is_backbone:
        mapB = -1
    else:
        mapB = 0
    
    rationale = (f"MAX: majority={max_majority} ({max_frac:.2f}), native-additive={max_native_additive}; "
                 f"ADD: majority={add_majority} ({add_frac:.2f}), native-additive={add_native_additive}; "
                 f"strict AND → MAX backbone={max_is_backbone}, ADD backbone={add_is_backbone}")
    return mapA, mapB, rationale

# -------- Source 2: Identity-edge reading under additive reading --------
def source_2_scores(n, add_edges):
    """
    Key criterion v1.1 §5.2: vertex 1 is additive generator, not additive identity.
    Additive identity is 0, in V0 boundary outside seam.
    No clean parallel to v1.0's multiplicative-trivialization argument.
    No substitute argument permitted per v1.1 §5.2 (explicitly prohibited per §8).
    Score 0/0 when no clean parallel.
    """
    # Check ADD touches vertex 0 (additive identity)? If yes, structural parallel exists.
    add_at_additive_identity = any(0 in e for e in add_edges)
    # Check ADD touches vertex 1 (additive generator)? Generator is not identity.
    add_at_additive_generator = any(1 in e for e in add_edges)
    
    if add_at_additive_identity:
        # Hypothetically would trigger non-zero scores, but this never happens in P3AP data
        mapA = -1
        mapB = +1
    else:
        # No clean parallel; substitute arguments prohibited per §5.2
        mapA = 0
        mapB = 0
    
    rationale = (f"ADD at additive-identity (0)={add_at_additive_identity}; "
                 f"ADD at additive-generator (1)={add_at_additive_generator}; "
                 f"no clean additive parallel → 0/0 per §5.2")
    return mapA, mapB, rationale

# -------- Source 3: Leaf-edge placement (topology-neutral) --------
def source_3_scores(n, all_edges, max_edges, add_edges):
    adj = build_adj(all_edges)
    add_at_leaf = False
    for (u, v) in add_edges:
        if len(adj.get(u, set())) == 1 or len(adj.get(v, set())) == 1:
            add_at_leaf = True
            break
    if add_at_leaf:
        mapA = -1  # persistent (ADD) at leaf inverts expected role
        mapB = +1  # excluded (ADD) at leaf matches expected role
    else:
        mapA = 0
        mapB = 0
    rationale = f"ADD at leaf={add_at_leaf}"
    return mapA, mapB, rationale

# -------- Source 4: Topology-feature dominance (topology-neutral) --------
def source_4_scores(n, all_edges, max_edges, add_edges, vertices):
    max_frac = len(max_edges) / len(all_edges)
    max_verts = set()
    for (u, v) in max_edges:
        max_verts.add(u); max_verts.add(v)
    # Connected MAX subgraph check
    if max_verts:
        adj = build_adj(max_edges)
        visited = set()
        stack = [sorted(max_verts)[0]]
        while stack:
            x = stack.pop()
            if x in visited: continue
            visited.add(x)
            for nb in adj.get(x, set()):
                if nb not in visited: stack.append(nb)
        max_connected = (visited == max_verts)
    else:
        max_connected = False
    max_carries_majority = (max_frac >= 0.5) and max_connected
    if max_carries_majority:
        mapA = -1
        mapB = +1
    else:
        mapA = 0
        mapB = 0
    rationale = f"MAX edge-frac={max_frac:.2f}, MAX connected={max_connected}, majority={max_carries_majority}"
    return mapA, mapB, rationale

# -------- Per-carrier scoring --------
print("=" * 110)
print(f"{'Carrier':>8} | {'S1 A':>4} | {'S1 B':>4} | {'S2 A':>4} | {'S2 B':>4} | {'S3 A':>4} | {'S3 B':>4} | {'S4 A':>4} | {'S4 B':>4} | {'A agg':>5} | {'B agg':>5} | {'gap':>3} | {'verdict':>11}")
print("-" * 110)

per_carrier = {}
for n in PATH2_CARRIERS:
    all_edges, max_edges, add_edges, vertices = build_carrier_seam(n)
    s1A, s1B, r1 = source_1_scores(n, all_edges, max_edges, add_edges)
    s2A, s2B, r2 = source_2_scores(n, add_edges)
    s3A, s3B, r3 = source_3_scores(n, all_edges, max_edges, add_edges)
    s4A, s4B, r4 = source_4_scores(n, all_edges, max_edges, add_edges, vertices)
    agg_A = s1A + s2A + s3A + s4A
    agg_B = s1B + s2B + s3B + s4B
    gap = abs(agg_A - agg_B)
    if agg_B >= 3 and agg_A <= 1 and gap >= 2:
        verdict = "SUPPORTS_B"
    elif agg_A >= 3 and agg_B <= 1 and gap >= 2:
        verdict = "SUPPORTS_A"
    else:
        verdict = "INDECISIVE"
    per_carrier[n] = {
        "n": n,
        "source_1": {"A": s1A, "B": s1B, "rationale": r1},
        "source_2": {"A": s2A, "B": s2B, "rationale": r2},
        "source_3": {"A": s3A, "B": s3B, "rationale": r3},
        "source_4": {"A": s4A, "B": s4B, "rationale": r4},
        "agg_A": agg_A,
        "agg_B": agg_B,
        "gap": gap,
        "verdict": verdict,
    }
    print(f"Z/{n:>5} | {s1A:>4} | {s1B:>4} | {s2A:>4} | {s2B:>4} | {s3A:>4} | {s3B:>4} | {s4A:>4} | {s4B:>4} | {agg_A:>5} | {agg_B:>5} | {gap:>3} | {verdict:>11}")

print()

# -------- Family aggregation --------
N_B = sum(1 for n in PATH2_CARRIERS if per_carrier[n]["verdict"] == "SUPPORTS_B")
N_A = sum(1 for n in PATH2_CARRIERS if per_carrier[n]["verdict"] == "SUPPORTS_A")
N_I = sum(1 for n in PATH2_CARRIERS if per_carrier[n]["verdict"] == "INDECISIVE")
assert N_B + N_A + N_I == 8

mean_gap_all = sum(per_carrier[n]["gap"] for n in PATH2_CARRIERS) / 8

print(f"Family aggregation:")
print(f"  N_B (supports B) = {N_B}/8  (threshold >= 6)")
print(f"  N_A (supports A) = {N_A}/8  (threshold >= 6)")
print(f"  N_I (indecisive) = {N_I}/8")
print()
print(f"Secondary summary (not scored):")
print(f"  Mean cleanness gap across all 8 carriers: {mean_gap_all:.2f}")
print()

# -------- Verdict --------
if N_B >= 6:
    verdict = "PASS-B"
    sub_pattern = None
elif N_A >= 6:
    verdict = "PASS-A"
    sub_pattern = None
elif (N_B == 5 and N_A == 0 and N_I == 3) or (N_A == 5 and N_B == 0 and N_I == 3):
    verdict = "UNCLEAR"
    sub_pattern = None
else:
    verdict = "FAIL"
    if N_B == 0 and N_A == 0:
        sub_pattern = "Uniform FAIL"
    elif N_B > 0 and N_A > 0:
        sub_pattern = "Split FAIL"
    else:
        sub_pattern = "Below-threshold FAIL"

print(f"VERDICT: {verdict}")
if sub_pattern:
    print(f"Sub-pattern: {sub_pattern}")

# -------- Write outputs --------
scores_output = {
    "spec_version": "PPM-v2.1",
    "scope": "Path 3 Bridge Test — additive operationalization transport",
    "operationalization": "additive, carrier-adapted for Source 1 under strict AND",
    "path2_carriers": PATH2_CARRIERS,
    "per_carrier": per_carrier,
    "family_aggregation": {
        "N_B_supports_B": N_B,
        "N_A_supports_A": N_A,
        "N_I_indecisive": N_I,
        "N_B_threshold": 6,
        "N_A_threshold": 6,
        "mean_gap_all_carriers": mean_gap_all,
    },
    "verdict": verdict,
    "sub_pattern": sub_pattern,
}

with open('/home/claude/foundation_sprint/ppm_v21/PPM_V21_PER_CARRIER_SCORES.json', 'w') as f:
    json.dump(scores_output, f, indent=2)

print()
print("Wrote PPM_V21_PER_CARRIER_SCORES.json")
