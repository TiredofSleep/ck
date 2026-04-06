"""
TSML⊗TSML Product Algebra Verification
TIG Sprint 2026-03-26
SHA-256(TSML): 7726d8a620c24b1e461ff03742f7cd4f775baed772f8357db913757cf4945787
"""

TSML = [
    [0,0,0,0,0,0,0,0,0,0],[0,7,3,7,7,7,7,7,7,7],[0,3,7,7,4,7,7,7,7,9],
    [0,7,7,7,7,7,7,7,7,3],[0,7,4,7,7,7,7,7,8,7],[0,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,7,7,7,7,7,7],[0,7,7,7,7,7,7,7,7,7],[0,7,7,7,8,7,7,7,7,7],
    [0,7,9,3,7,7,7,7,7,7],
]
def c(a, b): return TSML[a][b]

C = frozenset({1, 3, 7, 9})
G = frozenset({2, 4, 5, 6, 8})
prod_C = frozenset((a, b) for a in C for b in C)
cross_terms = frozenset(
    (a, b) for a in range(1, 10) for b in range(1, 10)
    if (a in C and b in G) or (a in G and b in C)
)

# BFS from product corners
reachable = set(prod_C)
frontier = set(prod_C)
for _ in range(50):
    new = {(c(a1, b1), c(a2, b2))
           for (a1, a2) in frontier
           for (b1, b2) in prod_C
           if (c(a1,b1), c(a2,b2)) not in reachable}
    if not new:
        break
    reachable |= new
    frontier = new

# Assertions
assert len(reachable) == 16,           f"Expected 16 reachable, got {len(reachable)}"
assert len(cross_terms & reachable) == 0, "Cross-terms should be unreachable"
assert all(c(a,b) in {3,7} for a in C for b in C for _ in [None]), \
    "C×C should land in {3,7}"

print("TSML⊗TSML verification: ALL ASSERTIONS PASS")
print(f"  Product corners reachable:   {len(reachable)}")
print(f"  Cross-terms unreachable:     {len(cross_terms)} (of 40 possible)")
print(f"  C⊗C × C⊗C → C⊗C: 100%")
