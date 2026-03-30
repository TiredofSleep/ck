#!/usr/bin/env python3
"""
R16 Job 2: Gate Rarity Sweep Across Composite Bases
Usage: python3 r16_job2_gate_sweep.py --n_per_base 5000 --seed 42
Output: results/gate_rarity_sweep.json
"""

import numpy as np, math, json, argparse, time
from pathlib import Path

BASES = [6,10,14,15,21,22,26,33,35,39]

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--n_per_base', type=int, default=2000)
    p.add_argument('--seed', type=int, default=42)
    p.add_argument('--bases', nargs='+', type=int, default=BASES)
    return p.parse_args()

def world_setup(b, cap=9):
    A = list(range(1, min(b, cap+1)))
    C = frozenset(k for k in A if math.gcd(k,b)==1)
    G = frozenset(k for k in A if k not in C)
    C_sorted = sorted(C)
    HAR = C_sorted[len(C_sorted)//2] if C_sorted else None
    return A, C, G, C_sorted, HAR

def spec_gap(T, A, C_sorted, N=40):
    if not C_sorted: return 0.0
    P = np.zeros((N,N)); n = len(A)
    def ts(i): return A[min(n-1,int(i*n/N))]
    HAR = C_sorted[len(C_sorted)//2]
    for i in range(N):
        s = ts(i)
        for c in C_sorted:
            v = T.get((s,c), HAR)
            vi = A.index(v) if v in A else n//2
            vf = vi/n; j = max(0,min(N-1,int(vf*N))); w = vf*N-int(vf*N)
            P[i][j] += (1-w)/len(C_sorted)
            if j+1 < N: P[i][j+1] += w/len(C_sorted)
    rs = P.sum(axis=1,keepdims=True); rs[rs==0]=1; P /= rs
    ev = sorted(abs(np.linalg.eigvals(P)), reverse=True)
    return 1-ev[1]

def HAR_mass(T, A, C_sorted, HAR, N=40):
    if not C_sorted: return 1.0
    P = np.zeros((N,N)); n = len(A)
    def ts(i): return A[min(n-1,int(i*n/N))]
    for i in range(N):
        s = ts(i)
        for c in C_sorted:
            v = T.get((s,c), HAR)
            vi = A.index(v) if v in A else n//2
            vf = vi/n; j = max(0,min(N-1,int(vf*N))); w = vf*N-int(vf*N)
            P[i][j] += (1-w)/len(C_sorted)
            if j+1 < N: P[i][j+1] += w/len(C_sorted)
    rs = P.sum(axis=1,keepdims=True); rs[rs==0]=1; P /= rs
    v = np.ones(N)/N
    for _ in range(200): v = P.T@v; v /= v.sum()
    def ts(i): return A[min(n-1,int(i*n/N))]
    return sum(v[i] for i in range(N) if ts(i)==HAR)

def full_gate(T, A, C, G):
    return not any(T.get((s,c), list(C)[0]) in G for s in C for c in A)

def bhml_count(T):
    pairs = [(2,4),(4,2),(4,8),(8,4),(2,9),(9,2)]
    return sum(1 for s,c in pairs if T.get((s,c),0)==max(s,c))

def run_job2(args):
    rng = np.random.RandomState(args.seed)
    Path("results").mkdir(exist_ok=True)
    results = []
    
    for b in args.bases:
        A, C, G, C_sorted, HAR = world_setup(b)
        if not C or not G:
            print(f"  b={b}: G=∅, skipping"); continue
        
        print(f"  b={b}: C={C_sorted}, G={sorted(G)}, HAR={HAR}")
        t0 = time.time()
        
        gaps=[]; hms=[]; gates=[]; bhmls=[]
        for _ in range(args.n_per_base):
            T = {}
            for s in A:
                T[(s,HAR)]=HAR; T[(HAR,s)]=HAR
            for s in A:
                for c in A:
                    if s==HAR or c==HAR: continue
                    v = rng.choice(C_sorted) if (s in C and c in C) else rng.choice(A)
                    T[(s,c)]=v; T[(c,s)]=v
            
            gaps.append(spec_gap(T, A, C_sorted, N=40))
            hms.append(HAR_mass(T, A, C_sorted, HAR, N=40))
            gates.append(full_gate(T, A, C, G))
            bhmls.append(bhml_count(T))
        
        gaps=np.array(gaps); hms=np.array(hms); bhmls=np.array(bhmls)
        r = np.corrcoef(gaps,hms)[0,1] if hms.std()>0.01 else float('nan')
        
        row = {
            'b': b, 'phi': len(C), 'G_size': len(G),
            'HAR': HAR, 'C': C_sorted, 'n_states': len(A),
            'N_samples': args.n_per_base,
            'gap_mean': float(gaps.mean()), 'gap_std': float(gaps.std()),
            'HAR_mean': float(hms.mean()), 'HAR_std': float(hms.std()),
            'HAR_max': float(hms.max()),
            'gate_fraction': float(np.mean(gates)),
            'bhml_mean': float(bhmls.mean()), 'bhml_max': int(bhmls.max()),
            'r_gap_HAR': float(r) if not math.isnan(r) else None,
            'elapsed_s': time.time()-t0,
        }
        results.append(row)
        print(f"    gap={row['gap_mean']:.4f}, HAR={row['HAR_mean']:.4f}/{row['HAR_max']:.4f}, "
              f"gate={row['gate_fraction']*100:.1f}%, bhml={row['bhml_mean']:.2f}")
    
    with open("results/gate_rarity_sweep.json","w") as f:
        json.dump({'bases':args.bases,'N_per_base':args.n_per_base,'results':results}, f, indent=2)
    print(f"\nSaved: results/gate_rarity_sweep.json")
    return results

if __name__ == '__main__':
    args = parse_args()
    run_job2(args)
