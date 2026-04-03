"""
BSD T*^2 Curve Search via LMFDB API
Searches for rank 0 elliptic curves with |E_tors|=7, |Sha|=25

Target: L(E,1)/Omega = 25/49 = T*^2 = CREATE^2 / HARMONY^2
Conditions:
  - Rank = 0 (L(E,1) != 0)
  - |E_tors| = 7 (Z/7Z torsion = HARMONY)
  - |Sha| = 25 = CREATE^2 (analytic SHA order)
  - Tamagawa product = 1 (for clean BSD formula)

Z/10Z key:
  CREATE = 5, HARMONY = 7
  T*^2 = 25/49 = CREATE^2 / HARMONY^2

(c) 2026 Brayden Sanders / 7Site LLC
"""

import json
import math
import urllib.request
import urllib.parse
import time

T_STAR = 5/7
T_STAR_SQ = 25/49
CREATE = 5
HARMONY = 7

print("=" * 60)
print("BSD T*^2 CURVE SEARCH — LMFDB API")
print(f"Target: L(E,1)/Omega = T*^2 = {CREATE}^2/{HARMONY}^2 = {T_STAR_SQ:.6f}")
print(f"Conditions: rank=0, |tors|=7, |Sha|=25")
print("=" * 60)

LMFDB_BASE = "https://www.lmfdb.org/api/ec_curves/"

def lmfdb_query(params):
    """Query LMFDB elliptic curve API."""
    query = dict(params)
    query['_format'] = 'json'
    url = LMFDB_BASE + "?" + urllib.parse.urlencode(query)
    try:
        req = urllib.request.Request(url, headers={'Accept': 'application/json'})
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except Exception as e:
        return {'error': str(e)}

def check_bsd_ratio(curve_data):
    """Compute L(E,1)/Omega from LMFDB data if available."""
    results = {}

    # Try to get BSD ratio directly
    if 'special_value' in curve_data:
        results['special_value'] = curve_data['special_value']
    if 'omega' in curve_data:
        results['omega'] = curve_data['omega']
    if 'sha' in curve_data:
        results['sha'] = curve_data['sha']
    if 'sha_an' in curve_data:
        results['sha_an'] = curve_data['sha_an']
    if 'tamagawa_product' in curve_data:
        results['tamagawa_product'] = curve_data['tamagawa_product']
    if 'rank' in curve_data:
        results['rank'] = curve_data['rank']
    if 'torsion_order' in curve_data:
        results['torsion_order'] = curve_data['torsion_order']
    if 'label' in curve_data:
        results['label'] = curve_data['label']
    if 'ainvs' in curve_data:
        results['ainvs'] = curve_data['ainvs']

    return results

# ============================================================
# Search 1: rank=0, torsion_order=7, sha_an=25
# ============================================================
print("\n--- Search 1: rank=0, torsion=Z/7Z, sha_an=25 ---")

data = lmfdb_query({
    'rank': 0,
    'torsion_order': 7,
    'sha_an': 25,
    '_fields': 'label,ainvs,rank,torsion_order,sha_an,tamagawa_product,special_value,omega',
    '_limit': 50,
})

if 'error' in data:
    print(f"  Error: {data['error']}")
    results1 = []
else:
    results1 = data.get('data', [])
    total1 = data.get('count', len(results1))
    print(f"  Found {total1} curves (showing {len(results1)})")

    candidates = []
    for c in results1:
        info = check_bsd_ratio(c)
        label = info.get('label', '?')
        sha = info.get('sha_an', '?')
        tors = info.get('torsion_order', '?')
        rank = info.get('rank', '?')
        tam = info.get('tamagawa_product', '?')
        sv = info.get('special_value', None)
        om = info.get('omega', None)

        # Check BSD ratio
        if sv is not None and om is not None and om != 0:
            ratio = sv / om
            is_tstar2 = abs(ratio - T_STAR_SQ) < 0.001
            flag = " *** T*^2! ***" if is_tstar2 else f" (ratio={ratio:.4f})"
        else:
            flag = ""

        # Check Tamagawa = 1
        tam_flag = " [Tam=1]" if tam == 1 else f" [Tam={tam}]"

        candidates.append({
            'label': label,
            'sha': sha,
            'tors': tors,
            'rank': rank,
            'tamagawa': tam,
            'flag': flag,
            'tam_flag': tam_flag,
        })
        print(f"  {label}: rank={rank}, |Sha|={sha}, |tors|={tors}, Tam={tam}{flag}")

# ============================================================
# Search 2: rank=0, torsion_order=7, tamagawa_product=1
# (find all 7-torsion rank-0 curves with Tamagawa=1, check Sha)
# ============================================================
print("\n--- Search 2: rank=0, torsion=Z/7Z, Tamagawa=1 ---")
time.sleep(0.5)

data2 = lmfdb_query({
    'rank': 0,
    'torsion_order': 7,
    'tamagawa_product': 1,
    '_fields': 'label,ainvs,rank,torsion_order,sha_an,tamagawa_product,special_value,omega',
    '_limit': 100,
})

if 'error' in data2:
    print(f"  Error: {data2['error']}")
    results2 = []
else:
    results2 = data2.get('data', [])
    total2 = data2.get('count', len(results2))
    print(f"  Found {total2} curves (showing {len(results2)})")

    sha25 = []
    for c in results2:
        sha = c.get('sha_an', 0)
        label = c.get('label', '?')
        sv = c.get('special_value', None)
        om = c.get('omega', None)

        if sha == 25:
            sha25.append(c)
            if sv is not None and om is not None and om != 0:
                ratio = sv / om
                flag = " *** T*^2! ***" if abs(ratio - T_STAR_SQ) < 0.001 else f" ratio={ratio:.6f}"
            else:
                flag = ""
            print(f"  SHA=25 CANDIDATE: {label}, Sha={sha}, Tam={c.get('tamagawa_product','?')}{flag}")
        elif sha and sha > 1:
            print(f"  {label}: Sha={sha}")

    if not sha25:
        print("  No SHA=25 curves in this batch.")

# ============================================================
# Search 3: Broader — rank=0, torsion=7, any Sha
# ============================================================
print("\n--- Search 3: rank=0, torsion=Z/7Z (broad scan, first 200) ---")
time.sleep(0.5)

data3 = lmfdb_query({
    'rank': 0,
    'torsion_order': 7,
    '_fields': 'label,ainvs,rank,torsion_order,sha_an,tamagawa_product',
    '_limit': 200,
    '_sort': 'conductor',
})

if 'error' in data3:
    print(f"  Error: {data3['error']}")
    results3 = []
else:
    results3 = data3.get('data', [])
    total3 = data3.get('count', len(results3))
    print(f"  Total rank-0, 7-torsion curves in LMFDB: {total3}")

    # Count SHA distribution
    sha_dist = {}
    sha25_list = []
    for c in results3:
        sha = c.get('sha_an', 1)
        sha_dist[sha] = sha_dist.get(sha, 0) + 1
        if sha == 25:
            sha25_list.append(c)

    print("\n  SHA distribution (first 200 curves):")
    for s in sorted(sha_dist.keys()):
        print(f"    |Sha| = {s:4d}: {sha_dist[s]} curves")

    if sha25_list:
        print(f"\n  *** SHA=25 candidates found: {len(sha25_list)} ***")
        for c in sha25_list:
            print(f"    {c.get('label','?')}: rank={c.get('rank','?')}, "
                  f"Sha={c.get('sha_an','?')}, Tam={c.get('tamagawa_product','?')}")
    else:
        print("\n  No SHA=25 in first 200. Need higher conductor search.")

        # What's the largest SHA seen?
        max_sha = max(sha_dist.keys()) if sha_dist else 0
        print(f"  Largest SHA observed: {max_sha}")

        # What SHA values are perfect squares (could be Sha²)?
        sq_shas = [s for s in sha_dist.keys() if int(math.isqrt(s))**2 == s and s > 1]
        if sq_shas:
            print(f"  Perfect-square SHA values: {sq_shas}")

# ============================================================
# Search 4: Any rank-0 curve with SHA=25 (no torsion constraint)
# ============================================================
print("\n--- Search 4: rank=0, sha_an=25 (any torsion) ---")
time.sleep(0.5)

data4 = lmfdb_query({
    'rank': 0,
    'sha_an': 25,
    '_fields': 'label,ainvs,rank,torsion_order,sha_an,tamagawa_product,special_value,omega',
    '_limit': 50,
    '_sort': 'conductor',
})

if 'error' in data4:
    print(f"  Error: {data4['error']}")
    results4 = []
else:
    results4 = data4.get('data', [])
    total4 = data4.get('count', len(results4))
    print(f"  Found {total4} rank-0 curves with |Sha|=25 in LMFDB")

    print("\n  All SHA=25 rank-0 curves:")
    tstar2_found = []
    for c in results4:
        label = c.get('label', '?')
        tors = c.get('torsion_order', '?')
        tam = c.get('tamagawa_product', '?')
        sv = c.get('special_value', None)
        om = c.get('omega', None)

        # BSD ratio
        if sv is not None and om is not None and om != 0:
            ratio = sv / om
            # BSD: L(E,1)/Omega = sha * tamagawa / tors^2
            # For tors=7, sha=25, tam=1: ratio should be 25/49 = T*^2
            bsd_pred = 25 * (tam if isinstance(tam, (int,float)) else 1) / (tors**2 if isinstance(tors, int) else 1)
            flag = ""
            if abs(ratio - T_STAR_SQ) < 0.01:
                flag = " *** T*^2! ***"
                tstar2_found.append(c)
            print(f"  {label}: tors={tors}, Tam={tam}, L/Omega={ratio:.6f} (pred={bsd_pred:.4f}){flag}")
        else:
            # Predict BSD ratio
            if isinstance(tors, int) and isinstance(tam, (int,float)):
                bsd_pred = 25 * tam / tors**2
                flag = " *** T*^2! ***" if abs(bsd_pred - T_STAR_SQ) < 0.001 else ""
            else:
                bsd_pred = None
                flag = ""
            print(f"  {label}: tors={tors}, Tam={tam}, pred_ratio={bsd_pred:.4f if bsd_pred else 'N/A'}{flag}")

    if tstar2_found:
        print(f"\n*** FOUND {len(tstar2_found)} T*^2 CURVES ***")
        for c in tstar2_found:
            print(f"  Label: {c.get('label','?')}")
            print(f"  Ainvs: {c.get('ainvs','?')}")
    else:
        # Check which torsion orders dominate
        tors_dist = {}
        for c in results4:
            t = c.get('torsion_order', 0)
            tors_dist[t] = tors_dist.get(t, 0) + 1
        print("\n  Torsion distribution among SHA=25 curves:")
        for t in sorted(tors_dist.keys()):
            pred = 25 / t**2 if t else 0
            mark = " <-- T*^2!" if t == 7 else ""
            print(f"    |tors|={t}: {tors_dist[t]} curves (pred L/Omega=25/{t}^2={pred:.4f}){mark}")

# ============================================================
# Pure algebraic BSD check
# ============================================================
print("\n--- Algebraic Check: BSD formula for (sha=25, tors=7, tam=1) ---")
sha = 25
tors = 7
tam = 1
# BSD (rank 0): L(E,1)/Omega = sha * tam / tors^2
bsd = sha * tam / tors**2
print(f"  L(E,1)/Omega = {sha} * {tam} / {tors}^2 = {sha*tam}/{tors**2} = {bsd:.8f}")
print(f"  T*^2 = {CREATE}^2/{HARMONY}^2 = {CREATE**2}/{HARMONY**2} = {T_STAR_SQ:.8f}")
print(f"  Match: {abs(bsd - T_STAR_SQ) < 1e-10}")
print(f"  The T*^2 curve EXISTS algebraically — BSD formula guarantees it IF such a curve exists.")
print(f"  Need: rank 0 curve with Z/7Z torsion and |Sha|=25.")

# Save results
output = {
    'target': {'sha': 25, 'torsion': 7, 'tamagawa': 1, 'predicted_ratio': T_STAR_SQ},
    'algebraic_bsd_ratio': bsd,
    'bsd_matches_tstar2': abs(bsd - T_STAR_SQ) < 1e-10,
    'lmfdb_search1_count': len(results1) if isinstance(results1, list) else 0,
    'lmfdb_search3_total': total3 if 'total3' in dir() else 0,
    'lmfdb_search4_total': total4 if 'total4' in dir() else 0,
    'tstar2_curves_found': [c.get('label','?') for c in (tstar2_found if 'tstar2_found' in dir() else [])],
}

with open('Gen11/bsd_lmfdb_results.json', 'w') as f:
    json.dump(output, f, indent=2)

print(f"\nResults saved to Gen11/bsd_lmfdb_results.json")
print("=" * 60)
