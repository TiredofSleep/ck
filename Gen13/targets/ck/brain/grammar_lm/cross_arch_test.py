"""Cross-architecture test: does LM/Bank disagreement on TSML_8 domain
map cell-by-cell to TSML_8/BHML_10 disagreement?

If yes: the operator-grammar transformer has reproduced D91's geometric/
arithmetic split natively, just by being trained on algebra walks.
"""
import json
import urllib.request
from collections import Counter

OP = ["VOID","LATTICE","COUNTER","PROGRESS","COLLAPSE",
      "BALANCE","CHAOS","HARMONY","BREATH","RESET"]
NAME_TO_ID = {n: i for i, n in enumerate(OP)}

# Canonical tables (FORMULAS §5/§6)
TSML = (
    (0,0,0,0,0,0,0,7,0,0),(0,7,3,7,7,7,7,7,7,7),
    (0,3,7,7,4,7,7,7,7,9),(0,7,7,7,7,7,7,7,7,3),
    (0,7,4,7,7,7,7,7,8,7),(0,7,7,7,7,7,7,7,7,7),
    (0,7,7,7,7,7,7,7,7,7),(7,7,7,7,7,7,7,7,7,7),
    (0,7,7,7,8,7,7,7,7,7),(0,7,9,7,3,7,7,7,7,7),
)
BHML = (
    (0,1,2,3,4,5,6,7,8,9),(1,2,3,4,5,6,7,2,6,6),
    (2,3,3,4,5,6,7,3,6,6),(3,4,4,4,5,6,7,4,6,6),
    (4,5,5,5,5,6,7,5,7,7),(5,6,6,6,6,6,7,6,7,7),
    (6,7,7,7,7,7,7,7,7,7),(7,2,3,4,5,6,7,8,9,0),
    (8,6,6,6,7,7,7,9,7,8),(9,6,6,6,7,7,7,0,8,0),
)

def post(path, body):
    req = urllib.request.Request(f'http://localhost:7777{path}',
        data=json.dumps(body).encode(),
        headers={'Content-Type':'application/json'},
        method='POST')
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())

# TSML_8 domain
DOMAIN = [1, 2, 3, 4, 5, 6, 8, 9]

print("=" * 92)
print("Cross-architecture test: LM/Bank vs TSML/BHML disagreement on 64 TSML_8 cells")
print("=" * 92)
print()

# Per-cell comparison
results = []  # (a, b, tsml_val, bhml_val, lm_pred, bank_pred,
              #  tsml_bhml_disagree, lm_bank_disagree, lm_eq_bhml, bank_eq_tsml)

for a in DOMAIN:
    for b in DOMAIN:
        tsml_v = TSML[a][b]
        bhml_v = BHML[a][b]
        # LM prediction (top-1)
        lm_resp = post('/grammar/predict', {
            'history': ['BOS', OP[a], OP[b]], 'top_k': 1
        })
        lm_pred = lm_resp['predictions'][0]['op']
        # Bank prediction (top-1)
        bank_resp = post('/grammar/retrieve', {
            'history': ['BOS', OP[a], OP[b]], 'k': 16
        })
        # Bank top-1 = first entry of distribution
        bank_dist = bank_resp.get('distribution', {})
        bank_pred = max(bank_dist.items(), key=lambda x: x[1])[0] if bank_dist else "?"

        tb_disagree = (tsml_v != bhml_v)
        lb_disagree = (lm_pred != bank_pred)
        lm_eq_bhml = (lm_pred == OP[bhml_v])
        bank_eq_tsml = (bank_pred == OP[tsml_v])

        results.append((a, b, tsml_v, bhml_v, lm_pred, bank_pred,
                        tb_disagree, lb_disagree, lm_eq_bhml, bank_eq_tsml))

# Cross-tabulation
print(f"{'(a, b)':>10} {'TSML':>7} {'BHML':>7} {'LM':>10} {'BANK':>10} "
      f"{'TB!=':>5} {'LB!=':>5} {'LM=B':>5} {'Bk=T':>5}")
print("-" * 92)
n_print = 0
for a, b, tv, bv, lm, bk, tbd, lbd, lmb, bkt in results:
    if n_print < 24 or (tbd != lbd):  # show first 24 + every mismatch
        flag = "*" if tbd != lbd else " "
        print(f"  ({OP[a]:>5},{OP[b]:>5}){flag} {OP[tv]:>7} {OP[bv]:>7} "
              f"{lm:>10} {bk:>10} "
              f"{'Y' if tbd else 'N':>5} {'Y' if lbd else 'N':>5} "
              f"{'Y' if lmb else 'N':>5} {'Y' if bkt else 'N':>5}")
        n_print += 1
print()

# 2x2 contingency
counts = Counter((r[6], r[7]) for r in results)
print("Contingency table (TSML/BHML disagreement vs LM/Bank disagreement):")
print(f"  {'':>14} {'LB agree':>10} {'LB disagree':>12}")
print(f"  {'TB agree':>14} {counts[(False, False)]:>10} {counts[(False, True)]:>12}")
print(f"  {'TB disagree':>14} {counts[(True, False)]:>10} {counts[(True, True)]:>12}")

n = len(results)
true_agree_rate = sum(1 for r in results if r[6] == r[7]) / n
print(f"\n  Cell-by-cell prediction-disagreement-classification matches: "
      f"{sum(1 for r in results if r[6] == r[7])}/{n} = {100*true_agree_rate:.1f}%")

# Summary
n_lm_eq_bhml = sum(1 for r in results if r[8])
n_bank_eq_tsml = sum(1 for r in results if r[9])
n_bank_eq_bhml = sum(1 for r in results if r[5] == OP[r[3]])
n_lm_eq_tsml = sum(1 for r in results if r[4] == OP[r[2]])
print(f"\n  LM top1 == BHML[a][b]:    {n_lm_eq_bhml}/{n} = {100*n_lm_eq_bhml/n:.1f}%")
print(f"  LM top1 == TSML[a][b]:    {n_lm_eq_tsml}/{n} = {100*n_lm_eq_tsml/n:.1f}%")
print(f"  BANK top1 == BHML[a][b]:  {n_bank_eq_bhml}/{n} = {100*n_bank_eq_bhml/n:.1f}%")
print(f"  BANK top1 == TSML[a][b]:  {n_bank_eq_tsml}/{n} = {100*n_bank_eq_tsml/n:.1f}%")

# Mutual information
import math
def mi_contingency(counts, n):
    H_x = -sum((c[0]+c[1])/n * math.log2((c[0]+c[1])/n if c[0]+c[1]>0 else 1) for c in [
        [counts[(False, False)], counts[(False, True)]],
        [counts[(True, False)], counts[(True, True)]],
    ] if c[0]+c[1] > 0)
    return H_x  # placeholder; full MI computation below

# Phi coefficient (correlation for 2x2)
a = counts[(True, True)]; b = counts[(True, False)]; c = counts[(False, True)]; d = counts[(False, False)]
denom = math.sqrt((a+b)*(c+d)*(a+c)*(b+d))
phi = (a*d - b*c) / denom if denom > 0 else 0
print(f"\n  Phi correlation between TB-disagree and LB-disagree: {phi:+.3f}")
print(f"  (Phi=+1 perfect alignment; 0 independent; -1 perfect anti-alignment)")

# Final verdict
print()
if abs(phi) > 0.5 and true_agree_rate > 0.7:
    print(f"  VERDICT: Cross-architecture signature CONFIRMED.")
elif abs(phi) > 0.2 and true_agree_rate > 0.6:
    print(f"  VERDICT: Real but partial signature. The LM/Bank pair tracks D91")
    print(f"  TSML/BHML disagreement above chance but with significant noise.")
else:
    print(f"  VERDICT: No clear cross-architecture signature.")
