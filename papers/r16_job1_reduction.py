#!/usr/bin/env python3
"""
R16 Job 1: Coherent Reduction from Random Family Starts
Test: does reduction toward gate+HAR+gap objectives recover TSML-like kernels?

Usage: python3 r16_job1_reduction.py --b 10 --n_start 10000 --n_steps 100 --seed 42
Output: results/reduction_b{b}_N{n_start}.json
"""

import numpy as np, math, json, argparse, time, hashlib
from pathlib import Path

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--b', type=int, default=10)
    p.add_argument('--n_start', type=int, default=1000)
    p.add_argument('--n_steps', type=int, default=50)
    p.add_argument('--seed', type=int, default=42)
    p.add_argument('--weights', nargs=4, type=float, default=[0.4,0.3,0.2,0.1],
                   help='weights for [gate, HAR_mass, bhml_residual, gap]')
    return p.parse_args()

def world_setup(b, cap=9):
    A = list(range(1, min(b, cap+1)))
    C = frozenset(k for k in A if math.gcd(k,b)==1)
    G = frozenset(k for k in A if k not in C)
    C_sorted = sorted(C)
    HAR = C_sorted[len(C_sorted)//2]
    return A, C, G, C_sorted, HAR

def spec_gap(T_dict, A, C_sorted, N=30):
    P = np.zeros((N,N)); n = len(A)
    def ts(i): return A[min(n-1,int(i*n/N))]
    HAR = C_sorted[len(C_sorted)//2]
    for i in range(N):
        s = ts(i)
        for c in C_sorted:
            v = T_dict.get((s,c), HAR)
            vi = A.index(v) if v in A else n//2
            vf = vi/n; j = max(0,min(N-1,int(vf*N))); w = vf*N - int(vf*N)
            P[i][j] += (1-w)/len(C_sorted)
            if j+1 < N: P[i][j+1] += w/len(C_sorted)
    rs = P.sum(axis=1,keepdims=True); rs[rs==0]=1; P /= rs
    ev = sorted(abs(np.linalg.eigvals(P)), reverse=True)
    return 1-ev[1]

def HAR_mass(T_dict, A, C_sorted, HAR, N=30):
    P = np.zeros((N,N)); n = len(A)
    def ts(i): return A[min(n-1,int(i*n/N))]
    for i in range(N):
        s = ts(i)
        for c in C_sorted:
            v = T_dict.get((s,c), HAR)
            vi = A.index(v) if v in A else n//2
            vf = vi/n; j = max(0,min(N-1,int(vf*N))); w = vf*N - int(vf*N)
            P[i][j] += (1-w)/len(C_sorted)
            if j+1 < N: P[i][j+1] += w/len(C_sorted)
    rs = P.sum(axis=1,keepdims=True); rs[rs==0]=1; P /= rs
    v = np.ones(N)/N
    for _ in range(150): v = P.T@v; v /= v.sum()
    def ts(i): return A[min(n-1,int(i*n/N))]
    return sum(v[i] for i in range(N) if ts(i)==HAR)

def gate_strength(T_dict, A, C, G):
    """Fraction of (C-state, any-operator) pairs that DON'T reach G."""
    total = len(C) * len(A)
    safe = sum(1 for s in C for c in A if T_dict.get((s,c), list(C)[0]) not in G)
    return safe / total if total > 0 else 0.0

def bhml_residual(T_dict):
    pairs = [(2,4),(4,2),(4,8),(8,4),(2,9),(9,2)]
    return sum(1 for s,c in pairs if T_dict.get((s,c),0) == max(s,c)) / 6.0

def compute_score(T_dict, A, C, G, C_sorted, HAR, weights):
    w = weights
    gate = gate_strength(T_dict, A, C, G)
    hm   = HAR_mass(T_dict, A, C_sorted, HAR, N=30)
    bhml = bhml_residual(T_dict)
    gap  = spec_gap(T_dict, A, C_sorted, N=30)
    return (w[0]*gate + w[1]*hm + w[2]*bhml + w[3]*gap,
            {'gate':gate, 'HAR_mass':hm, 'bhml':bhml, 'gap':gap})

def sample_table(A, C, C_sorted, HAR, rng):
    T = {}
    for s in A:
        T[(s,HAR)] = HAR; T[(HAR,s)] = HAR
    for s in A:
        for c in A:
            if s==HAR or c==HAR: continue
            v = rng.choice(C_sorted) if (s in C and c in C) else rng.choice(A)
            T[(s,c)] = v; T[(c,s)] = v
    return T

def mutate_table(T_dict, A, C, G, C_sorted, HAR, rng, n_mut=3):
    T2 = dict(T_dict)
    for _ in range(n_mut):
        s = rng.choice(A)
        c = rng.choice(A)
        if s==HAR or c==HAR: continue
        if s in C and c in C:
            v = rng.choice(C_sorted)
        else:
            v = rng.choice(A)
        T2[(s,c)] = v; T2[(c,s)] = v
    return T2

def classify_attractor(selectors):
    gate, hm, bhml, gap = selectors['gate'], selectors['HAR_mass'], selectors['bhml'], selectors['gap']
    if gate > 0.95 and hm > 0.50 and bhml > 0.80: return 'TSML-like'
    if gate > 0.95 and hm > 0.50: return 'gate-strong'
    if gap > 0.70 and hm < 0.35: return 'high-gap oracle'
    if bhml > 0.80 and hm < 0.35: return 'order-saturated'
    if hm > 0.50 and gate < 0.85: return 'high-support/no-gate'
    return 'balanced'

def run_job1(args):
    A, C, G, C_sorted, HAR = world_setup(args.b)
    rng = np.random.RandomState(args.seed)
    weights = args.weights
    
    Path("results").mkdir(exist_ok=True)
    outfile = f"results/reduction_b{args.b}_N{args.n_start}.json"
    
    print(f"Job 1: b={args.b}, n_start={args.n_start}, n_steps={args.n_steps}")
    print(f"       C={C_sorted}, HAR={HAR}, weights={weights}")
    print(f"       Output: {outfile}")
    print()
    
    all_results = []
    attractor_counts = {}
    t0 = time.time()
    
    for trial in range(args.n_start):
        if trial % 100 == 0:
            elapsed = time.time()-t0
            print(f"  trial {trial}/{args.n_start}  elapsed={elapsed:.1f}s  "
                  f"attractors={dict(list(attractor_counts.items())[:3])}")
        
        T = sample_table(A, C, C_sorted, HAR, rng)
        score, sels = compute_score(T, A, C, G, C_sorted, HAR, weights)
        trajectory = [{'step':0, 'score':score, **sels}]
        
        for step in range(1, args.n_steps+1):
            T_mut = mutate_table(T, A, C, G, C_sorted, HAR, rng, n_mut=2)
            s2, sels2 = compute_score(T_mut, A, C, G, C_sorted, HAR, weights)
            if s2 >= score:  # accept if better or equal
                T = T_mut; score = s2; sels = sels2
            trajectory.append({'step':step, 'score':score, **sels})
        
        attractor = classify_attractor(sels)
        attractor_counts[attractor] = attractor_counts.get(attractor,0)+1
        
        # Store compressed: initial score, final score, final selectors, class
        all_results.append({
            'init_score': trajectory[0]['score'],
            'final_score': score,
            'final_gate': sels['gate'],
            'final_HAR_mass': sels['HAR_mass'],
            'final_bhml': sels['bhml'],
            'final_gap': sels['gap'],
            'attractor_class': attractor,
        })
    
    summary = {
        'b': args.b, 'n_start': args.n_start, 'n_steps': args.n_steps,
        'weights': weights, 'C': C_sorted, 'HAR': HAR,
        'attractor_distribution': attractor_counts,
        'mean_final_gate': float(np.mean([r['final_gate'] for r in all_results])),
        'mean_final_HAR': float(np.mean([r['final_HAR_mass'] for r in all_results])),
        'TSML_like_fraction': attractor_counts.get('TSML-like',0)/args.n_start,
        'per_trial': all_results,
    }
    
    with open(outfile, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print()
    print("=== RESULTS ===")
    print(f"Attractor distribution: {attractor_counts}")
    print(f"TSML-like fraction: {summary['TSML_like_fraction']*100:.2f}%")
    print(f"Saved to: {outfile}")
    return summary

if __name__ == '__main__':
    args = parse_args()
    run_job1(args)
