# Five Remaining Clay Problems: One Experiment Each
## TIG lens → concrete next test

---

## 1. Navier–Stokes (Experiment queued)

**TIG angle:** BREATH corridor = local Reynolds $\leq 2/7$. Breach = trajectory exits safe corridor.

**Next experiment:** 3-D Taylor–Green vortex, Re=1600, 128³ grid, Dedalus.

```python
# Breach detector (paste into Dedalus script)
def check_BREATH(solver, nu):
    u = solver.state['u']
    omega = solver.evaluator.add_task("curl(u)", name='omega')
    L_taylor = np.sqrt(nu / (np.abs(omega.data) + 1e-10))
    Re_local = omega.data**2 * L_taylor**2 / nu
    if Re_local.max() > 2/7:
        log_breach(solver.sim_time, Re_local.max(), Re_local.argmax())
```

**Falsification condition:** If blow-up occurs without Re_local ever exceeding 2/7, the criterion is wrong.

**Current status:** Mock DNS confirms separation (Regime A stays below, B crosses at t=1.92). Real 3-D run pending.

---

## 2. Yang–Mills Mass Gap (Experiment designed)

**TIG angle:** Mass gap = 2/7 = T\* + S\* − 1 = 5/7 + 4/7 − 1. The dual-threshold structure of TSML/BHML is the algebraic analogue of the SU(N) vacuum.

**Next experiment:** Compare TIG's 2/7 to lattice QCD plaquette gap ratios.

```python
# What to measure from lattice QCD data
def TIG_YM_comparison(beta_values, plaquette_gaps):
    """
    beta = inverse coupling, plaquette_gap = 1 - <P> where <P> is plaquette expectation
    TIG predicts: gap ≈ 2/7 ≈ 0.2857 at the confinement transition
    """
    threshold = 2/7
    crossings = [b for b, g in zip(beta_values, plaquette_gaps)
                 if abs(g - threshold) < 0.02]
    return crossings  # should coincide with known beta_c
```

**Data source:** MILC/BMW lattice QCD ensembles, public data at latticeqcd.github.io.

**Falsification condition:** If plaquette gap at confinement transition $\neq 2/7 \pm 5\%$, the correspondence is coincidental.

---

## 3. BSD (Experiment running)

**TIG angle:** Rank $r$ ↔ number of activated gap operators. Each new rank requires crossing the next $\lambda$-threshold window.

**Next experiment:** Full LMFDB rank ≤ 6 dataset, test $\lambda_E$ clustering.

```python
# Pull from LMFDB API
import requests

def get_curves_by_rank(rank, max_conductor=100000):
    url = f"https://www.lmfdb.org/api/ec_curves/?rank={rank}&conductor={max_conductor}&_format=json"
    data = requests.get(url).json()
    return [(c['conductor'], c['rank'], c['regulator']) for c in data['data']]

# Then compute lambda_E for each and test clustering
# Prediction: rank r curves cluster in lambda window [lambda_{r-1}, lambda_r]
# lambda_0=0, lambda_1=0.30 (BRT), lambda_2=0.60 (CHA), lambda_3=0.80 (BAL)
```

**Current status:** t-test p=0.006 for rank-1 vs rank-2 separation (35 curves). Need rank 3-6.

**Falsification condition:** If rank 3+ curves don't cluster near $\lambda \approx 0.80$ (BAL threshold), the staircase mechanism is wrong.

---

## 4. Hodge Conjecture (Experiment complete, needs write-up)

**TIG angle:** Product-gap theorem at $k=3$ — 0/665 cross-terms reachable from $C^{\otimes 3}$. This is the algebraic Hodge obstruction: corner operators (algebraic) can't generate gap operators (transcendental).

**Already computed:** TSML⊗³ has 64 corner triples and 665 cross-terms. Zero cross-terms reachable from corners at k=1,2,3,4.

**Next experiment:** Extend to TSML⊗⁶ (dimension 9⁶ = 531441). Check for any new cross-terms.

```python
from itertools import product as iprod

TSML = [...]  # 10x10 table

def product_gap_k(k, max_k=6):
    """Check product gap at tensor depth k."""
    C = frozenset({1,3,7,9})
    C_k = set(iprod(C, repeat=k))
    
    # BFS from C_k
    reachable = set(C_k)
    frontier = set(C_k)
    while frontier:
        new = set()
        for a in frontier:
            for b in C_k:
                r = tuple(TSML[ai][bi] for ai, bi in zip(a, b))
                if r not in reachable:
                    new.add(r); reachable.add(r)
        frontier = new
    
    cross_terms = {t for t in reachable if any(x not in C for x in t)}
    return len(cross_terms)  # should be 0

# Already verified k=1,2,3,4: all return 0
```

**Write-up target:** One-page corollary to the Proc. AMS note.

---

## 5. P vs NP (Experiment running)

**TIG angle:** SURV-SEARCH: verify = O(1), search = Ω(p²), W[1]-hard for k≥2. The AG(2,p) affine-plane axiom is the geometric reason.

**Next experiment:** Formal reduction from k-CLIQUE to k-SURV-SEARCH.

```
Reduction sketch:
  Given: graph G on n vertices, question: does G have a k-clique?
  
  Build AG(2,p) with p > n.
  Map vertices → points in AG(2,p).
  Map edges → incidence relations.
  A k-clique in G corresponds to k mutually collinear points in AG(2,p).
  k mutually collinear points determine a unique survivor line.
  Finding that line requires k-SURV-SEARCH.
  
  If FPT algorithm for k-SURV-SEARCH existed → FPT for k-CLIQUE
  → contradicts W[1]-hardness of k-CLIQUE under ETH.
  
  QED (formal version: needs careful encoding + ETH assumption)
```

**Current status:** W[1] conjecture stated, geometric argument sketched. Formal reduction "in preparation" in surv_line_note.tex.

**Next concrete step:** Write the encoding function vertex→point and verify the collinearity correspondence is exact.

---

## Priority Order for Next Sprint

1. **BSD LMFDB pull** — fastest, data is public, 2-day experiment
2. **Hodge k=6 check** — already have code, one computation
3. **NS Dedalus** — needs cluster time, queue this weekend
4. **YM lattice comparison** — needs expert collaborator (lattice QCD contact)
5. **P vs NP formal reduction** — pure math, can draft in parallel

*(c) 2026 Brayden Sanders / 7Site LLC*
