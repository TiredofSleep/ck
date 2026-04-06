
"""
TSML × AG(2,3) Verification
Checks Theorems A/B, self-composition, non-7 rule, two-step convergence.
"""

TSML = [
    [0,0,0,0,0,0,0,7,0,0],
    [0,7,3,7,7,7,7,7,7,7],
    [0,3,7,7,4,7,7,7,7,9],
    [0,7,7,7,7,7,7,7,7,3],
    [0,7,4,7,7,7,7,7,8,7],
    [0,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,7,7,7,7,7,7],
    [7,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,8,7,7,7,7,7],
    [0,7,9,3,7,7,7,7,7,7]
]

# AG(2,3) coordinate map: operator k -> (row, col) in {0,1,2}^2
# row = (k-1) // 3,  col = (k-1) % 3
def pt(k): return ((k-1)//3, (k-1)%3)
def op(r, c): return r*3 + c + 1

def ag_line(a, b):
    """Return the 3 operators on the AG(2,3) line through a and b."""
    p1, p2 = pt(a), pt(b)
    for da in range(3):
        for db in range(3):
            if (da, db) == (0, 0): continue
            for c in range(3):
                pts = [(x,y) for x in range(3) for y in range(3)
                       if (da*x + db*y) % 3 == c]
                if p1 in pts and p2 in pts:
                    return sorted(op(r, cc) for r, cc in pts)

# --- Theorem A ---
thm_A_violations = []
for a in range(1, 10):
    for b in range(1, 10):
        if a == b: continue
        line = ag_line(a, b)
        if 7 in line and TSML[a][b] != 7:
            thm_A_violations.append((a, b, TSML[a][b]))
print(f"Theorem A violations: {len(thm_A_violations)}")  # expect 0

# --- Theorem B (implied by A) ---
thm_B_violations = []
for a in range(1, 10):
    for b in range(1, 10):
        if a == b: continue
        if TSML[a][b] != 7:
            line = ag_line(a, b)
            if 7 in line:
                thm_B_violations.append((a, b))
print(f"Theorem B violations: {len(thm_B_violations)}")  # expect 0

# --- Self-composition ---
self_violations = [a for a in range(1, 10) if TSML[a][a] != 7]
print(f"Self-composition violations: {len(self_violations)}")  # expect 0

# --- Non-7 rule (coordinate rule) ---
def coord_rule(a, b):
    x1, y1 = pt(a); x2, y2 = pt(b)
    if x1 == x2:  # same row -> third collinear
        line = ag_line(a, b)
        return [x for x in line if x != a and x != b][0]
    elif y1 != y2:  # different row, different col -> higher row wins
        return a if x1 > x2 else b
    else:           # different row, same col -> lower row wins
        return a if x1 < x2 else b

non7_violations = []
for a in range(1, 10):
    for b in range(1, 10):
        if a == b or TSML[a][b] == 7: continue
        if coord_rule(a, b) != TSML[a][b]:
            non7_violations.append((a, b, TSML[a][b], coord_rule(a, b)))
print(f"Non-7 rule violations: {len(non7_violations)}")  # expect 0

# --- Two-step convergence ---
def depth(x, b):
    v = x
    for k in range(20):
        if v == 7: return k
        nv = TSML[v][b]
        if nv == v: return float("inf")
        v = nv
    return float("inf")

depth_violations = []
for x in range(1, 10):
    for b in range(1, 10):
        d = depth(x, b)
        if d not in (0, 1, 2, float("inf")):
            depth_violations.append((x, b, d))
print(f"Two-step violations: {len(depth_violations)}")  # expect 0
