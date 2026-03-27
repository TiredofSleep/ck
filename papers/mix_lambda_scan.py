"""
Mix_λ Anchor Threshold Scanner
TIG Sprint 2026-03-26
Mix_λ[a][b] = (1-λ)·TSML[a][b] + λ·BHML[a][b]
"""
TSML = [
    [0,0,0,0,0,0,0,0,0,0],[0,7,3,7,7,7,7,7,7,7],[0,3,7,7,4,7,7,7,7,9],
    [0,7,7,7,7,7,7,7,7,3],[0,7,4,7,7,7,7,7,8,7],[0,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,7,7,7,7,7,7],[0,7,7,7,7,7,7,7,7,7],[0,7,7,7,8,7,7,7,7,7],
    [0,7,9,3,7,7,7,7,7,7],
]
BHML = [
    [0,0,0,0,0,0,0,0,0,0],[0,1,3,4,4,5,6,7,8,9],[0,3,2,4,4,5,6,7,8,9],
    [0,4,4,3,4,5,6,7,8,9],[0,4,4,4,4,5,6,7,8,9],[0,5,5,5,5,5,6,7,8,9],
    [0,6,6,6,6,6,6,7,8,9],[0,7,7,7,7,7,7,7,8,9],[0,8,8,8,8,8,8,8,8,9],
    [0,9,9,9,9,9,9,9,9,9],
]
NAMES = {1:'LAT',2:'CTR',3:'PRG',4:'COL',5:'BAL',6:'CHA',7:'HAR',8:'BRT',9:'RST'}
G = {2,4,5,6,8}

def anchors(g, lam):
    return [b for b in range(1,10)
            if abs((1-lam)*TSML[g][b] + lam*BHML[g][b] - g) < 0.5]

def threshold(g, resolution=100):
    base = set(anchors(g, 0.0))
    for i in range(1, resolution+1):
        lam = i/resolution
        new = set(anchors(g, lam)) - base
        if new:
            return lam, new
    return 1.0, set()

print("Mix_λ anchor thresholds:")
print(f"{'Operator':>10}  {'λ*':>5}  {'New anchors gained':>25}")
print("-"*45)
for g in sorted(G):
    lam, new = threshold(g)
    print(f"  {NAMES[g]:>8}({g})  {lam:>5.2f}  {[NAMES[a] for a in sorted(new)]}")

print()
print("Expected ordering: BRT(0.30) < CHA(0.60) < BAL(0.80) < COL(0.90) < CTR(1.00)")

# Assertions
thresholds = {g: threshold(g)[0] for g in G}
assert thresholds[8] < thresholds[6] < thresholds[5] < thresholds[4] < thresholds[2], \
    "Threshold ordering violated"
print("Ordering assertion: PASS")
