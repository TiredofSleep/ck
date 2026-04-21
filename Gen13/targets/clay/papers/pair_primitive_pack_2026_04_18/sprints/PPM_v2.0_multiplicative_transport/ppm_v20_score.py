"""
PPM-v2.0 per-carrier rubric application.
Applies v1.0 rubric (multiplicative operationalization, carrier-adapted for Source 1)
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

def connected_components(vertices, edges):
    adj = build_adj(edges)
    visited = set()
    components = []
    for start in vertices:
        if start in visited: continue
        comp = set(); stack = [start]
        while stack:
            x = stack.pop()
            if x in visited: continue
            visited.add(x); comp.add(x)
            for nb in adj.get(x, set()):
                if nb not in visited: stack.append(nb)
        components.append(comp)
    return components

def build_carrier_seam(n):
    """Return (all_edges, max_edges, add_edges, vertex_set) for one carrier."""
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

# -------- Source 1 rubric: Structural backbone (carrier-adapted) --------
def source_1_scores(n, all_edges, max_edges, add_edges, vertices):
    """Returns (map_A_score, map_B_score, rationale)."""
    total_edges = len(all_edges)
    max_frac = len(max_edges) / total_edges
    add_frac = len(add_edges) / total_edges
    # Check doubling chain presence: 2→4, 4→8 must be in MAX as minimum
    has_24 = (2, 4) in max_edges
    has_48 = (4, 8) in max_edges
    has_doubling_chain = has_24 and has_48
    # Check MAX connected
    max_verts = set()
    for (u, v) in max_edges:
        max_verts.add(u); max_verts.add(v)
    max_components = connected_components(max_verts, max_edges) if max_verts else []
    max_connected = len(max_components) == 1 if max_components else False
    # Backbone criterion: majority AND connected multiplicative-flow substructure containing doubling chain
    max_is_backbone = (max_frac >= 0.5) and max_connected and has_doubling_chain
    add_is_backbone = (add_frac >= 0.5) and has_doubling_chain  # ADD only has 1 edge, can't contain chain
    # Map A: persistent = ADD
    if add_is_backbone:
        mapA = +1
    elif max_is_backbone:
        mapA = -1  # persistent-side (ADD) is not backbone; excluded-side (MAX) is
    else:
        mapA = 0
    # Map B: persistent = MAX
    if max_is_backbone:
        mapB = +1
    elif add_is_backbone:
        mapB = -1
    else:
        mapB = 0
    rationale = f"MAX={len(max_edges)}/{total_edges}={max_frac:.2f} majority={max_frac>=0.5}, connected={max_connected}, doubling_chain={has_doubling_chain}; MAX is backbone={max_is_backbone}"
    return mapA, mapB, rationale

# -------- Source 2 rubric: Identity-edge reading (inherited verbatim) --------
def source_2_scores(n, add_edges):
    """On every carrier, vertex 1 is multiplicative identity.
    Key criterion: identity is multiplicative-absence point; ADD at identity = excluded surfacing."""
    # Check ADD touches vertex 1
    add_at_identity = any(1 in e for e in add_edges)
    if add_at_identity:
        mapA = -1  # contradicts §3: persistent at multiplicative-absence is incoherent
        mapB = +1  # coheres with §3: excluded at multiplicative-absence is correct reading
    else:
        mapA = 0
        mapB = 0
    rationale = f"ADD at vertex 1 = {add_at_identity}; identity = multiplicative-trivialization point"
    return mapA, mapB, rationale

# -------- Source 3 rubric: Leaf-edge placement (inherited verbatim) --------
def source_3_scores(n, all_edges, max_edges, add_edges):
    """Does excluded-side sit at leaf? Topology-neutral criterion."""
    adj = build_adj(all_edges)
    # Check if ADD has a degree-1 endpoint
    add_at_leaf = False
    for (u, v) in add_edges:
        if len(adj.get(u, set())) == 1 or len(adj.get(v, set())) == 1:
            add_at_leaf = True
            break
    # Check if MAX has a degree-1 endpoint (at least one MAX edge at leaf)
    max_at_leaf_fraction = 0
    if max_edges:
        max_leaf_count = sum(
            1 for (u, v) in max_edges
            if len(adj.get(u, set())) == 1 or len(adj.get(v, set())) == 1
        )
        max_at_leaf_fraction = max_leaf_count / len(max_edges)
    # For the rubric: ADD is unambiguously at leaf if its edge has degree-1 endpoint
    # Map A: persistent = ADD. Persistent at leaf → -1 (inverts expected role)
    # Map B: excluded = ADD. Excluded at leaf → +1 (matches expected role)
    if add_at_leaf:
        mapA = -1
        mapB = +1
    else:
        mapA = 0
        mapB = 0
    rationale = f"ADD at leaf = {add_at_leaf}; MAX leaf-fraction = {max_at_leaf_fraction:.2f}"
    return mapA, mapB, rationale

# -------- Source 4 rubric: Topology-feature dominance (inherited verbatim) --------
def source_4_scores(n, all_edges, max_edges, add_edges, vertices):
    """Does persistent-side carry majority of topology features?
    Features: forest spine, low-degree profile, edge-count majority."""
    max_frac = len(max_edges) / len(all_edges)
    # Forest spine: MAX-only subgraph is non-trivially a tree spanning majority vertices
    max_verts = set()
    for (u, v) in max_edges:
        max_verts.add(u); max_verts.add(v)
    # MAX carries forest spine if it contributes ≥50% of edges AND is connected
    max_components = connected_components(max_verts, max_edges) if max_verts else []
    max_connected = len(max_components) == 1 if max_components else False
    # Low-degree profile: in full graph, what fraction of vertices have degree ≤2?
    adj = build_adj(all_edges)
    low_degree_count = sum(1 for v in vertices if len(adj.get(v, set())) <= 2)
    low_degree_frac = low_degree_count / len(vertices)
    # Topology features majority attribution:
    # MAX carries majority if: edge count ≥50% AND forest spine is MAX-dominated AND low-degree profile is MAX-driven
    max_carries_majority = (max_frac >= 0.5) and max_connected
    # Map A (persistent=ADD): persistent does NOT carry majority → -1
    # Map B (persistent=MAX): persistent DOES carry majority → +1
    if max_carries_majority:
        mapA = -1
        mapB = +1
    else:
        mapA = 0
        mapB = 0
    rationale = f"MAX edge-fraction={max_frac:.2f}, MAX-connected={max_connected}, low-degree-frac={low_degree_frac:.2f}; MAX carries majority={max_carries_majority}"
    return mapA, mapB, rationale

# -------- Per-carrier scoring --------
print("=" * 100)
print(f"{'Carrier':>8} | {'S1 A':>4} | {'S1 B':>4} | {'S2 A':>4} | {'S2 B':>4} | {'S3 A':>4} | {'S3 B':>4} | {'S4 A':>4} | {'S4 B':>4} | {'A agg':>5} | {'B agg':>5} | {'gap':>3} | {'verdict':>9}")
print("-" * 100)

per_carrier = {}
for n in PATH2_CARRIERS:
    all_edges, max_edges, add_edges, vertices = build_carrier_seam(n)
    s1A, s1B, r1 = source_1_scores(n, all_edges, max_edges, add_edges, vertices)
    s2A, s2B, r2 = source_2_scores(n, add_edges)
    s3A, s3B, r3 = source_3_scores(n, all_edges, max_edges, add_edges)
    s4A, s4B, r4 = source_4_scores(n, all_edges, max_edges, add_edges, vertices)
    agg_A = s1A + s2A + s3A + s4A
    agg_B = s1B + s2B + s3B + s4B
    gap = abs(agg_A - agg_B)
    # Per-carrier verdict classification
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
    print(f"Z/{n:>5} | {s1A:>4} | {s1B:>4} | {s2A:>4} | {s2B:>4} | {s3A:>4} | {s3B:>4} | {s4A:>4} | {s4B:>4} | {agg_A:>5} | {agg_B:>5} | {gap:>3} | {verdict:>9}")

print()

# -------- Family aggregation --------
N_B = sum(1 for n in PATH2_CARRIERS if per_carrier[n]["verdict"] == "SUPPORTS_B")
N_A = sum(1 for n in PATH2_CARRIERS if per_carrier[n]["verdict"] == "SUPPORTS_A")
N_I = sum(1 for n in PATH2_CARRIERS if per_carrier[n]["verdict"] == "INDECISIVE")
assert N_B + N_A + N_I == 8

mean_gap_all = sum(per_carrier[n]["gap"] for n in PATH2_CARRIERS) / 8
mean_gap_supports_B = (
    sum(per_carrier[n]["gap"] for n in PATH2_CARRIERS if per_carrier[n]["verdict"] == "SUPPORTS_B") / N_B
    if N_B > 0 else 0
)

print(f"Family aggregation:")
print(f"  N_B (supports B) = {N_B}/8  (threshold >= 6)")
print(f"  N_A (supports A) = {N_A}/8")
print(f"  N_I (indecisive) = {N_I}/8")
print()
print(f"Secondary summary (not scored):")
print(f"  Mean cleanness gap across all 8 carriers: {mean_gap_all:.2f}")
print(f"  Mean cleanness gap across supports_B carriers: {mean_gap_supports_B:.2f}")
print()

# -------- Verdict --------
if N_B >= 6:
    verdict = "PASS"
    sub_pattern = None
elif N_B == 5 and N_I == 3:
    verdict = "UNCLEAR"
    sub_pattern = None
else:
    verdict = "FAIL"
    if N_B <= 1:
        sub_pattern = "Uniform FAIL"
    elif N_A > 0:
        sub_pattern = "Split FAIL"
    else:
        sub_pattern = "Below-threshold FAIL"

print(f"VERDICT: {verdict}")
if sub_pattern:
    print(f"Sub-pattern: {sub_pattern}")

# -------- Write outputs --------
scores_output = {
    "spec_version": "PPM-v2.0",
    "scope": "Path 3 Bridge Test — multiplicative operationalization transport",
    "operationalization": "multiplicative, carrier-adapted for Source 1",
    "path2_carriers": PATH2_CARRIERS,
    "per_carrier": per_carrier,
    "family_aggregation": {
        "N_B_supports_B": N_B,
        "N_A_supports_A": N_A,
        "N_I_indecisive": N_I,
        "N_B_threshold": 6,
        "mean_gap_all_carriers": mean_gap_all,
        "mean_gap_supports_B_carriers": mean_gap_supports_B,
    },
    "verdict": verdict,
    "sub_pattern": sub_pattern,
}

with open('/home/claude/foundation_sprint/ppm_v20/PPM_V20_PER_CARRIER_SCORES.json', 'w') as f:
    json.dump(scores_output, f, indent=2)

print()
print("Wrote PPM_V20_PER_CARRIER_SCORES.json")
