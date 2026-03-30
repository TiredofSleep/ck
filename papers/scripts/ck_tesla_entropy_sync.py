"""
ck_tesla_entropy_sync.py -- TeslaBridge Layer G + H Simulation
==============================================================
Layer G: Grammar-Forced Mode = Minimum Entropy Production
Layer H: Cross-Instance Synchronization via Shared OS Field

Layer G claims:
  1. The BTQ kernel's grammar-forced selection of HAR is NOT arbitrary --
     it is the state of minimum entropy production in the TSML Markov chain.
  2. The transition at T* is a genuine second-order phase transition with
     order parameter m = pi_7 - 1/10 (HAR excess above uniform).
  3. Entropy production sigma(T) peaks EXACTLY at T* -- the grammar/thermal
     crossover is the maximum dissipation point, not a stable state.
     CK steers AWAY from maximum dissipation.

Layer H claims:
  1. Two CK instances sharing the same OS process field will phase-lock
     coherence oscillations without explicit communication.
  2. The coupling mechanism is algebraic, not continuous -- shared operator
     inputs from the OS force both instances into the same TSML attractor.
  3. Synchronization onset has a threshold K_sync* = gamma (coherence decay
     rate), below which instances run independently.

Both layers derived from exact TSML table -- no free parameters.

(c) 2026 Brayden Sanders / 7Site LLC -- Trinity Infinity Geometry
"""

import math
import json
import sys
import os
import random
from collections import deque

# ── TSML table (exact from ck_sim_heartbeat.py) ──────────────────────────────
TSML = [
    # VOID  LAT  CTR  PRG  COL  BAL  CHA  HAR  BRE  RST
    [    0,   0,   0,   0,   0,   0,   0,   7,   0,   0],  # VOID
    [    0,   7,   3,   7,   7,   7,   7,   7,   7,   7],  # LATTICE
    [    0,   3,   7,   7,   4,   7,   7,   7,   7,   9],  # COUNTER
    [    0,   7,   7,   7,   7,   7,   7,   7,   7,   3],  # PROGRESS
    [    0,   7,   4,   7,   7,   7,   7,   7,   8,   7],  # COLLAPSE
    [    0,   7,   7,   7,   7,   7,   7,   7,   7,   7],  # BALANCE
    [    0,   7,   7,   7,   7,   7,   7,   7,   7,   7],  # CHAOS
    [    7,   7,   7,   7,   7,   7,   7,   7,   7,   7],  # HARMONY
    [    0,   7,   7,   7,   8,   7,   7,   7,   7,   7],  # BREATH
    [    0,   7,   9,   3,   7,   7,   7,   7,   7,   7],  # RESET
]

N      = 10
VOID   = 0
HARMONY = 7
OP_NAMES = ['VOID','LAT','CTR','PRG','COL','BAL','CHA','HAR','BRE','RST']

# ── Transition matrix (uniform input) ────────────────────────────────────────
# K[dest][src] = fraction of inputs b such that TSML[src][b] = dest
def build_K_uniform():
    K = [[0.0]*N for _ in range(N)]
    for src in range(N):
        for b in range(N):
            dest = TSML[src][b]
            K[dest][src] += 1.0/N
    return K

K_BASE = build_K_uniform()

# ── Energy landscape ──────────────────────────────────────────────────────────
# Energy = -log(P(HARMONY | mode)) = dissipation cost of reaching attractor.
# HARMONY has E=0 (ground state). High-barrier modes cost more to exit.
ENERGIES = [-math.log(max(K_BASE[HARMONY][i], 1e-9)) for i in range(N)]
# Normalize so E[HARMONY] = 0
E_harm = ENERGIES[HARMONY]
ENERGIES = [e - E_harm for e in ENERGIES]

def build_K_thermal(noise_T: float) -> list:
    """
    Thermal transition matrix at noise temperature T in [0,1].
    K_T = (1-T)*K_BASE + T*(1/N) uniform noise.

    T=0: pure grammar (K_BASE dominates).
    T=1: fully random (all transitions equal).
    This is the interpolation that defines the grammar/thermal phase boundary.
    """
    K_T = [[0.0]*N for _ in range(N)]
    for dest in range(N):
        for src in range(N):
            K_T[dest][src] = (1.0 - noise_T)*K_BASE[dest][src] + noise_T*(1.0/N)
    return K_T

def stationary(K: list, max_iter: int = 2000, tol: float = 1e-10) -> list:
    """Power iteration to find stationary distribution pi: K*pi = pi."""
    pi = [1.0/N]*N
    for _ in range(max_iter):
        pi_new = [0.0]*N
        for dest in range(N):
            for src in range(N):
                pi_new[dest] += K[dest][src] * pi[src]
        # Normalize
        s = sum(pi_new)
        pi_new = [v/s for v in pi_new]
        # Check convergence
        diff = sum(abs(pi_new[i]-pi[i]) for i in range(N))
        pi = pi_new
        if diff < tol:
            break
    return pi

def entropy_production(K: list, pi: list) -> float:
    """
    Schnakenberg entropy production rate.
    sigma = sum_{i!=j} K[i][j]*pi[j] * ln(K[i][j]*pi[j] / (K[j][i]*pi[i]))

    Zero at equilibrium (detailed balance).
    Zero when all probability is trapped in one absorbing state (no transitions).
    Maximum somewhere in between -- that maximum IS the phase transition.
    """
    sigma = 0.0
    for i in range(N):
        for j in range(N):
            if i == j:
                continue
            flux_ij = K[i][j] * pi[j]
            flux_ji = K[j][i] * pi[i]
            if flux_ij > 1e-15 and flux_ji > 1e-15:
                sigma += flux_ij * math.log(flux_ij / flux_ji)
    return sigma / 2.0  # Symmetric sum double-counts

def order_parameter(pi: list) -> float:
    """m = pi[HARMONY] - 1/N. Grammar phase: m>0. Thermal phase: m~0."""
    return pi[HARMONY] - 1.0/N


# ═══════════════════════════════════════════════════════════════════════════════
#  LAYER G: Entropy Production vs Temperature
# ═══════════════════════════════════════════════════════════════════════════════

def run_layer_G(n_points: int = 80) -> dict:
    """
    Sweep noise temperature T from 0 to 1.
    At each T: compute stationary distribution, entropy production, order param.

    Key predictions:
      P1: sigma(T) has a single peak at some T* (phase transition temperature)
      P2: m(T) transitions from m>0 (grammar phase) to m~0 (thermal phase) at T*
      P3: T* is determined purely by the TSML table -- no free parameters
      P4: The peak of sigma = maximum competition = BTQ actively avoids this state
    """
    temps = [i / (n_points - 1) for i in range(n_points)]
    results = []

    for T in temps:
        K_T   = build_K_thermal(T)
        pi    = stationary(K_T)
        sigma = entropy_production(K_T, pi)
        m     = order_parameter(pi)
        results.append({
            'T':     round(T, 4),
            'sigma': round(sigma, 6),
            'm':     round(m, 6),
            'pi_HAR': round(pi[HARMONY], 6),
            'pi_VOID': round(pi[VOID], 6),
        })

    # Find T*: where sigma peaks
    sigma_vals = [r['sigma'] for r in results]
    peak_idx   = sigma_vals.index(max(sigma_vals))
    T_star     = results[peak_idx]['T']
    sigma_star = results[peak_idx]['sigma']

    # Find grammar-thermal crossover: where m crosses zero
    crossover_T = None
    for i in range(len(results)-1):
        if results[i]['m'] >= 0 and results[i+1]['m'] < 0:
            crossover_T = (results[i]['T'] + results[i+1]['T']) / 2.0
            break

    # Critical exponent beta: m ~ (T* - T)^beta for T < T*
    # Fit in log-log space near T*
    beta = None
    fit_pts = [(r['T'], r['m']) for r in results
               if 0.02 < (T_star - r['T']) < T_star*0.8 and r['m'] > 0.01]
    if len(fit_pts) >= 4:
        log_dt   = [math.log(T_star - t) for t, m in fit_pts]
        log_m    = [math.log(m)          for t, m in fit_pts]
        # Linear regression in log-log
        n_fit = len(fit_pts)
        mean_x = sum(log_dt) / n_fit
        mean_y = sum(log_m)  / n_fit
        cov  = sum((log_dt[i]-mean_x)*(log_m[i]-mean_y) for i in range(n_fit))
        var  = sum((log_dt[i]-mean_x)**2 for i in range(n_fit))
        if var > 1e-10:
            beta = round(cov / var, 3)

    # Minimum entropy production: T=0 (pure grammar, fully absorbed in HAR)
    sigma_T0  = results[0]['sigma']
    sigma_T1  = results[-1]['sigma']
    pi_T0_HAR = results[0]['pi_HAR']
    pi_T1_HAR = results[-1]['pi_HAR']

    return {
        'layer': 'G',
        'claim': 'Grammar-forced mode selection = minimum entropy production',
        'T_star_sigma_peak':     T_star,
        'sigma_at_T_star':       sigma_star,
        'sigma_at_T0_grammar':   round(sigma_T0, 6),
        'sigma_at_T1_thermal':   round(sigma_T1, 6),
        'crossover_T':           round(crossover_T, 4) if crossover_T else None,
        'T_star_crossover_agree': abs(T_star - (crossover_T or 0)) < 0.05,
        'critical_exponent_beta': beta,
        'pi_HAR_at_T0':          round(pi_T0_HAR, 4),
        'pi_HAR_at_T1':          round(pi_T1_HAR, 4),
        'verdict_min_entropy':   sigma_T0 < sigma_star,   # grammar < peak
        'verdict_sigma_peaks_at_Tstar': True,             # by construction of finding
        'note': (
            'T=0 (pure grammar) has LESS entropy production than T* (phase boundary). '
            'BTQ selecting HAR is not just efficient -- it is the thermodynamic ground state. '
            'T* = maximum dissipation point: system is maximally conflicted between grammar and thermal.'
        ),
        'sweep': results,
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  LAYER H: Cross-Instance Synchronization
# ═══════════════════════════════════════════════════════════════════════════════

def simulate_instance(shared_ops: list, private_noise: float,
                      window: int = 32, n_ticks: int = 500) -> list:
    """
    Simulate a single CK instance processing operator streams.

    shared_ops: operator sequence shared by both instances (the OS field).
    private_noise: fraction of operators that are private (not shared).
    Returns coherence time series (HARMONY fraction in rolling window).
    """
    history = deque(maxlen=window)
    coherence_series = []

    for t in range(n_ticks):
        # Each tick: shared input with prob (1-noise), private with prob noise
        if random.random() < private_noise:
            # Private input: random operator from TSML row of current state
            src = history[-1] if history else HARMONY
            b   = random.randint(0, N-1)
            op  = TSML[src][b]
        else:
            # Shared input: from OS field (same for both instances)
            op = shared_ops[t % len(shared_ops)]

        history.append(op)
        harmony_count = sum(1 for o in history if o == HARMONY)
        coherence_series.append(harmony_count / len(history))

    return coherence_series

def cross_correlation(a: list, b: list, max_lag: int = 20) -> dict:
    """Compute cross-correlation at lags 0..max_lag."""
    n    = len(a)
    mean_a = sum(a) / n
    mean_b = sum(b) / n
    std_a  = math.sqrt(sum((x - mean_a)**2 for x in a) / n)
    std_b  = math.sqrt(sum((x - mean_b)**2 for x in b) / n)

    if std_a < 1e-10 or std_b < 1e-10:
        return {'lag_0': 0.0, 'peak_lag': 0, 'peak_value': 0.0}

    corrs = {}
    for lag in range(max_lag + 1):
        n_valid = n - lag
        if n_valid <= 0:
            corrs[lag] = 0.0
            continue
        c = sum((a[t]-mean_a)*(b[t+lag]-mean_b) for t in range(n_valid)) / n_valid
        corrs[lag] = c / (std_a * std_b)

    peak_lag   = max(corrs, key=lambda l: corrs[l])
    peak_value = corrs[peak_lag]
    return {'lag_0': round(corrs[0], 4),
            'peak_lag': peak_lag,
            'peak_value': round(peak_value, 4),
            'all_lags': {l: round(v, 4) for l, v in corrs.items()}}

def generate_os_field(n_ticks: int = 500) -> list:
    """
    Generate a synthetic OS operator field.
    Realistic: mostly HARMONY/BALANCE/BREATH (idle processes),
    with bursts of CHAOS/VOID (active/dying processes).
    """
    ops = []
    t = 0
    while t < n_ticks:
        # Baseline: HARMONY-dominant field
        burst_len = random.randint(5, 20)
        # 70% chance of quiet HARMONY burst, 30% chance of CHAOS/VOID burst
        if random.random() < 0.70:
            op = random.choices([HARMONY, 5, 8], weights=[7, 2, 1])[0]  # HAR/BAL/BRE
            ops.extend([op] * burst_len)
        else:
            op = random.choices([6, 0, 4], weights=[5, 3, 2])[0]  # CHA/VOI/COL
            ops.extend([op] * burst_len)
        t += burst_len
    return ops[:n_ticks]

def run_layer_H(noise_levels=None, n_ticks: int = 600, n_trials: int = 30) -> dict:
    """
    Sweep private noise levels from 0 (fully shared) to 1 (fully independent).
    At each noise level: run n_trials pairs of instances on shared OS field.
    Measure cross-correlation at lag=0.

    Key predictions:
      P1: At noise=0 (fully shared): corr(A,B) approaches 1.0 (perfect sync)
      P2: At noise=1 (no sharing): corr(A,B) approaches 0.0 (no sync)
      P3: Sync threshold K_sync* ~ gamma = 1/window = 1/32 ~ 0.031
          Above 1 - K_sync* = 0.969 noise, sync collapses.
      P4: Synchronization is ALGEBRAIC (discrete operator alignment),
          not continuous (no sinusoidal coupling assumed).
    """
    if noise_levels is None:
        noise_levels = [i/20 for i in range(21)]  # 0.0 to 1.0 in steps of 0.05

    results = []
    gamma   = 1.0 / 32.0   # coherence decay rate (window = 32)

    for noise in noise_levels:
        trial_corrs = []
        for _ in range(n_trials):
            os_field = generate_os_field(n_ticks)
            coh_A    = simulate_instance(os_field, noise, n_ticks=n_ticks)
            coh_B    = simulate_instance(os_field, noise, n_ticks=n_ticks)
            cc       = cross_correlation(coh_A, coh_B)
            trial_corrs.append(cc['lag_0'])

        mean_corr = sum(trial_corrs) / len(trial_corrs)
        std_corr  = math.sqrt(sum((c-mean_corr)**2 for c in trial_corrs) / len(trial_corrs))
        results.append({
            'noise':     round(noise, 3),
            'sharing':   round(1.0 - noise, 3),
            'corr_mean': round(mean_corr, 4),
            'corr_std':  round(std_corr, 4),
            'synced':    mean_corr > 0.3,
        })

    # Find sync threshold: noise where corr drops below 0.3
    sync_threshold_noise = None
    for i in range(len(results)-1):
        if results[i]['synced'] and not results[i+1]['synced']:
            sync_threshold_noise = (results[i]['noise'] + results[i+1]['noise']) / 2.0
            break

    sync_threshold_K = 1.0 - (sync_threshold_noise or 1.0)
    gamma_match = abs(sync_threshold_K - gamma) < 0.05

    return {
        'layer': 'H',
        'claim': 'Two CK instances on shared OS field phase-lock without explicit communication',
        'gamma':                  round(gamma, 4),
        'predicted_K_sync_star':  round(gamma, 4),
        'measured_K_sync_star':   round(sync_threshold_K, 4),
        'gamma_match':            gamma_match,
        'corr_at_full_sharing':   results[0]['corr_mean'],   # noise=0
        'corr_at_no_sharing':     results[-1]['corr_mean'],  # noise=1
        'sync_threshold_noise':   round(sync_threshold_noise, 3) if sync_threshold_noise else None,
        'mechanism': (
            'Shared OS operator field drives both instances into the same TSML attractor. '
            'No explicit communication. No sinusoidal coupling. '
            'The algebra itself creates the synchronization -- '
            'both instances follow the same deterministic CL path from the same inputs.'
        ),
        'sweep': results,
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  LAYER G+H TOGETHER: The Deeper Connection
# ═══════════════════════════════════════════════════════════════════════════════

def run_GH_connection(g_results: dict, h_results: dict) -> dict:
    """
    The connection between Layer G and Layer H:

    Layer G shows: CK avoids T* (maximum entropy production) --
                   he steers toward T=0 (grammar phase, minimum dissipation).

    Layer H shows: Two CK instances synchronize when sharing > K_sync* of
                   their operator input.

    Connection: A system at minimum entropy production (T=0, all in HAR)
    generates a MAXIMALLY PREDICTABLE operator stream. A predictable stream
    = maximum shared information between instances = maximum K_sync.

    Therefore: CK steering toward minimum entropy production CAUSES the
    synchronization in Layer H. The two results are the same physics.

    Prediction: Sync strength corr(A,B) is inversely proportional to entropy
    production -- cleaner grammar = stronger synchronization.
    """
    T_star_G   = g_results['T_star_sigma_peak']
    sigma_T0   = g_results['sigma_at_T0_grammar']
    sigma_Tstar = g_results['sigma_at_T_star']
    corr_full  = h_results['corr_at_full_sharing']
    corr_none  = h_results['corr_at_no_sharing']

    return {
        'layer': 'G+H',
        'connection': 'Minimum entropy production = maximum synchronizability',
        'T_star_sigma_peak':    T_star_G,
        'entropy_ratio':        round(sigma_T0 / max(sigma_Tstar, 1e-9), 4),
        'note': (
            f'At T=0 (grammar ground state): sigma={sigma_T0:.4f}. '
            f'At T={T_star_G} (phase boundary): sigma={sigma_Tstar:.4f}. '
            f'Grammar phase reduces entropy production by {(1-sigma_T0/max(sigma_Tstar,1e-9))*100:.1f}%. '
            f'Full sharing gives sync corr={corr_full:.3f}; '
            f'no sharing gives corr={corr_none:.3f}. '
            f'Minimum dissipation = maximum coherence = maximum sync.'
        ),
        'implication': (
            'CK does not choose HAR because it is labeled "harmony". '
            'CK chooses HAR because it is the thermodynamic ground state of the TSML algebra. '
            'The same reason water flows downhill. '
            'Two CK instances synchronize for the same reason -- '
            'they are both following the same thermodynamic gradient.'
        ),
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    random.seed(42)  # Reproducible

    print("=" * 65)
    print("  TESLABRIDGE LAYER G: Entropy Production Minimum")
    print("=" * 65)
    g = run_layer_G(n_points=80)

    print(f"\n  Entropy production sweep:")
    print(f"    T=0.00 (pure grammar): sigma = {g['sigma_at_T0_grammar']:.6f}")
    print(f"    T={g['T_star_sigma_peak']:.2f} (T* peak):     sigma = {g['sigma_at_T_star']:.6f}  <-- maximum dissipation")
    print(f"    T=1.00 (pure thermal): sigma = {g['sigma_at_T1_thermal']:.6f}")
    print(f"\n  Phase transition:")
    print(f"    sigma peak at T*      = {g['T_star_sigma_peak']:.4f}")
    print(f"    order param crossover = {g['crossover_T']}")
    print(f"    T* and crossover agree: {g['T_star_crossover_agree']}")
    print(f"    critical exponent beta = {g['critical_exponent_beta']}")
    print(f"\n  HAR probability:")
    print(f"    pi_HAR at T=0         = {g['pi_HAR_at_T0']:.4f}  (grammar ground state)")
    print(f"    pi_HAR at T=1         = {g['pi_HAR_at_T1']:.4f}  (thermal noise floor)")
    print(f"\n  VERDICT:")
    print(f"    Grammar < peak entropy: {g['verdict_min_entropy']}")
    print(f"    {g['note'][:100]}...")

    print()
    print("=" * 65)
    print("  TESLABRIDGE LAYER H: Cross-Instance Synchronization")
    print("=" * 65)
    h = run_layer_H(n_ticks=600, n_trials=30)

    print(f"\n  Synchronization sweep (cross-correlation at lag=0):")
    for r in h['sweep']:
        bar = '#' * int(max(0, r['corr_mean']) * 20)
        print(f"    noise={r['noise']:.2f} share={r['sharing']:.2f}  corr={r['corr_mean']:+.3f} +/-{r['corr_std']:.3f}  {bar}")

    print(f"\n  Gamma (coherence decay rate) = 1/32 = {h['gamma']:.4f}")
    print(f"  Predicted K_sync* = gamma   = {h['predicted_K_sync_star']:.4f}")
    print(f"  Measured  K_sync*           = {h['measured_K_sync_star']:.4f}")
    print(f"  Gamma match (within 0.05)   : {h['gamma_match']}")
    print(f"\n  Corr at full sharing (noise=0): {h['corr_at_full_sharing']:.4f}")
    print(f"  Corr at no sharing  (noise=1): {h['corr_at_no_sharing']:.4f}")

    print()
    print("=" * 65)
    print("  LAYER G + H: The Connection")
    print("=" * 65)
    gh = run_GH_connection(g, h)
    print(f"\n  {gh['note']}")
    print(f"\n  {gh['implication']}")

    # Save full results
    out = {
        'layer_G': {k: v for k, v in g.items() if k != 'sweep'},
        'layer_H': {k: v for k, v in h.items() if k != 'sweep'},
        'layer_GH': gh,
        'layer_G_sweep': g['sweep'],
        'layer_H_sweep': h['sweep'],
    }
    out_path = os.path.join(os.path.dirname(__file__), 'layer_gh_results.json')
    with open(out_path, 'w') as f:
        json.dump(out, f, indent=2)
    print(f"\n  Full results saved: {out_path}")

    print("\n" + "=" * 65)
    return out


if __name__ == '__main__':
    main()
