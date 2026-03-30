#!/usr/bin/env python3
"""
R16 Job 3: Attractor Class Clustering
Reads Job 1 output and clusters by selector fingerprint.
Usage: python3 r16_job3_clustering.py --input results/reduction_b10_N10000.json
"""

import numpy as np, json, argparse
from pathlib import Path

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--input', default='results/reduction_b10_N1000.json')
    p.add_argument('--n_clusters', type=int, default=6)
    return p.parse_args()

def run_job3(args):
    with open(args.input) as f:
        data = json.load(f)
    
    trials = data['per_trial']
    X = np.array([[t['final_gate'], t['final_HAR_mass'], t['final_bhml'],
                   t['final_gap']] for t in trials])
    
    # Simple k-means clustering
    from numpy.random import RandomState
    rng = RandomState(42)
    k = args.n_clusters
    centroids = X[rng.choice(len(X), k, replace=False)]
    
    for iteration in range(50):
        dists = np.array([[np.linalg.norm(x-c) for c in centroids] for x in X])
        labels = dists.argmin(axis=1)
        new_centroids = np.array([X[labels==i].mean(axis=0) if (labels==i).any() 
                                   else centroids[i] for i in range(k)])
        if np.allclose(centroids, new_centroids, atol=1e-4): break
        centroids = new_centroids
    
    # Name the clusters
    cluster_names = {}
    for i in range(k):
        c = centroids[i]
        gate, hm, bhml, gap = c
        if gate > 0.95 and hm > 0.50 and bhml > 0.80: name = 'TSML-like'
        elif gate > 0.95 and hm > 0.40: name = 'gate-strong'
        elif gap > 0.70: name = 'high-gap oracle'
        elif bhml > 0.80: name = 'order-saturated'
        elif hm > 0.50: name = 'high-support'
        else: name = f'type-{i}'
        cluster_names[i] = name
    
    print(f"\nAttractor classes from {len(trials)} reduction trajectories:\n")
    print(f"{'Cluster':>15}  {'Count':>6}  {'%':>6}  "
          f"{'gate':>6}  {'HAR_m':>6}  {'bhml':>6}  {'gap':>6}")
    print("-"*58)
    for i in range(k):
        mask = labels==i
        if not mask.any(): continue
        c = centroids[i]
        count = mask.sum()
        print(f"  {cluster_names[i]:>13}  {count:>6}  {count/len(trials)*100:>5.1f}%  "
              f"{c[0]:>6.3f}  {c[1]:>6.3f}  {c[2]:>6.3f}  {c[3]:>6.3f}")
    
    output = {
        'input_file': args.input,
        'n_trials': len(trials),
        'n_clusters': k,
        'clusters': [{
            'id': i,
            'name': cluster_names[i],
            'count': int((labels==i).sum()),
            'fraction': float((labels==i).mean()),
            'centroid': {'gate':float(centroids[i][0]), 'HAR_mass':float(centroids[i][1]),
                        'bhml':float(centroids[i][2]), 'gap':float(centroids[i][3])},
        } for i in range(k) if (labels==i).any()],
    }
    outfile = args.input.replace('.json','_clusters.json')
    with open(outfile,'w') as f: json.dump(output,f,indent=2)
    print(f"\nSaved: {outfile}")

if __name__ == '__main__':
    args = parse_args()
    run_job3(args)
