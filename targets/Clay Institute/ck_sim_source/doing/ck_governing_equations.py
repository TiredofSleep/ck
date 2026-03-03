"""
ck_governing_equations.py -- Parametric Equation Extraction for the Coherence Manifold
======================================================================================
Operator: VOID (0) -- From nothing, the equation emerges.

Fits parametric models to delta(L) trajectories from the Fractal Coherence Atlas,
extracts governing equations, and classifies asymptotic behavior.

The spectrometer produces data.  This module finds the law.

Six model families compete for each trajectory:
  CONSTANT:   delta(L) = c
  LINEAR:     delta(L) = a*L + b
  POWER_LAW:  delta(L) = a * L^(-alpha)   (log-linearized fit)
  EXP_DECAY:  delta(L) = a * exp(-lambda*L) + c
  DAMPED_OSC: delta(L) = a * exp(-gamma*L) * cos(omega*L + phi) + c
  PURE_OSC:   delta(L) = a * cos(omega*L + phi) + c

Model selection: BIC (Bayesian Information Criterion) with parsimony tiebreaker.
Asymptotic prediction: classify delta(L -> inf) as AFFIRMATIVE, GAP, or INDETERMINATE.

Pure Python. No numpy, no scipy.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple

from ck_sim.being.ck_sdv_safety import safe_div, safe_log, safe_sqrt, clamp


# ================================================================
#  ENUMS
# ================================================================

class ModelFamily(str, Enum):
    """Parametric model families for delta(L) trajectories."""
    CONSTANT = 'constant'
    LINEAR = 'linear'
    POWER_LAW = 'power_law'
    EXP_DECAY = 'exp_decay'
    DAMPED_OSC = 'damped_osc'
    PURE_OSC = 'pure_osc'
    UNRESOLVED = 'unresolved'


class AsymptoticClass(str, Enum):
    """Asymptotic prediction for delta(L -> infinity)."""
    AFFIRMATIVE = 'affirmative'    # delta -> 0
    GAP = 'gap'                     # delta -> eta > 0
    INDETERMINATE = 'indeterminate' # cannot classify


# ================================================================
#  DATA CLASSES
# ================================================================

@dataclass
class FitResult:
    """Result of fitting one parametric model to a trajectory."""
    family: str                     # ModelFamily value
    params: Dict[str, float]        # Fitted parameter values
    residuals: List[float]          # y_pred - y_obs for each point
    rss: float                      # Residual sum of squares
    r_squared: float                # Coefficient of determination
    aic: float                      # Akaike Information Criterion
    bic: float                      # Bayesian Information Criterion
    n_params: int                   # Number of free parameters
    converged: bool = True          # Did the optimizer converge?


@dataclass
class GoverningEquation:
    """The extracted governing equation for one trajectory."""
    problem: str                    # Problem ID
    regime: str                     # 'calibration' or 'frontier'
    test_case: str
    best_model: str                 # ModelFamily value
    best_fit: FitResult
    all_fits: Dict[str, FitResult]  # family -> FitResult
    asymptotic_class: str           # AsymptoticClass value
    asymptotic_value: float         # Predicted delta(L -> inf)
    latex: str                      # LaTeX representation
    confidence: float               # 0..1: how much better is best vs runner-up


@dataclass
class EquationAtlasResult:
    """Governing equations for the full coherence atlas."""
    equations: Dict[str, GoverningEquation]  # key -> GoverningEquation
    n_affirmative: int = 0
    n_gap: int = 0
    n_indeterminate: int = 0


# ================================================================
#  STATISTICAL HELPERS
# ================================================================

def _mean(xs: List[float]) -> float:
    """Arithmetic mean."""
    if not xs:
        return 0.0
    return sum(xs) / len(xs)


def _variance(xs: List[float], mean_x: float) -> float:
    """Population variance."""
    if len(xs) < 2:
        return 0.0
    return sum((x - mean_x) ** 2 for x in xs) / len(xs)


def _r_squared(y_obs: List[float], y_pred: List[float]) -> float:
    """Coefficient of determination R^2."""
    n = len(y_obs)
    if n < 2:
        return 0.0
    y_mean = _mean(y_obs)
    ss_tot = sum((y - y_mean) ** 2 for y in y_obs)
    ss_res = sum((y_obs[i] - y_pred[i]) ** 2 for i in range(n))
    if ss_tot < 1e-30:
        return 1.0 if ss_res < 1e-30 else 0.0
    return 1.0 - safe_div(ss_res, ss_tot)


def _aic(rss: float, n: int, k: int) -> float:
    """Akaike Information Criterion.

    AIC = n * ln(RSS/n) + 2*k
    RSS=0 is a perfect fit (best possible), use a floor of 1e-30.
    """
    if n <= 0:
        return 1e30
    rss_safe = max(rss, 1e-30)
    return n * math.log(rss_safe / n) + 2.0 * k


def _bic(rss: float, n: int, k: int) -> float:
    """Bayesian Information Criterion.

    BIC = n * ln(RSS/n) + k * ln(n)
    RSS=0 is a perfect fit (best possible), use a floor of 1e-30.
    """
    if n <= 0:
        return 1e30
    rss_safe = max(rss, 1e-30)
    return n * math.log(rss_safe / n) + k * math.log(max(n, 2))


def _durbin_watson(residuals: List[float]) -> float:
    """Durbin-Watson statistic for autocorrelation in residuals.

    DW near 2 = no autocorrelation.
    DW near 0 = positive autocorrelation.
    DW near 4 = negative autocorrelation.
    """
    n = len(residuals)
    if n < 3:
        return 2.0
    num = sum((residuals[i] - residuals[i - 1]) ** 2 for i in range(1, n))
    den = sum(r ** 2 for r in residuals)
    return safe_div(num, den, 2.0)


def _make_fit_result(family: str, params: dict, x: List[float],
                     y_obs: List[float], y_pred: List[float],
                     n_params: int, converged: bool = True) -> FitResult:
    """Build a FitResult from observed and predicted values."""
    n = len(y_obs)
    residuals = [y_pred[i] - y_obs[i] for i in range(n)]
    rss = sum(r ** 2 for r in residuals)
    r2 = _r_squared(y_obs, y_pred)
    return FitResult(
        family=family,
        params=params,
        residuals=residuals,
        rss=rss,
        r_squared=r2,
        aic=_aic(rss, n, n_params),
        bic=_bic(rss, n, n_params),
        n_params=n_params,
        converged=converged,
    )


# ================================================================
#  OLS FITTERS
# ================================================================

def _fit_constant(x: List[float], y: List[float]) -> FitResult:
    """Fit delta(L) = c (1 parameter)."""
    c = _mean(y)
    y_pred = [c] * len(y)
    return _make_fit_result(
        ModelFamily.CONSTANT.value, {'c': c},
        x, y, y_pred, n_params=1,
    )


def _fit_linear(x: List[float], y: List[float]) -> FitResult:
    """Fit delta(L) = a*L + b  (2 parameters, OLS)."""
    n = len(x)
    if n < 2:
        return _fit_constant(x, y)

    x_mean = _mean(x)
    y_mean = _mean(y)
    ss_xx = sum((xi - x_mean) ** 2 for xi in x)
    ss_xy = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))

    if abs(ss_xx) < 1e-30:
        return _fit_constant(x, y)

    a = ss_xy / ss_xx
    b = y_mean - a * x_mean
    y_pred = [a * xi + b for xi in x]
    return _make_fit_result(
        ModelFamily.LINEAR.value, {'a': a, 'b': b},
        x, y, y_pred, n_params=2,
    )


# ================================================================
#  LOG-LINEARIZED POWER LAW
# ================================================================

def _fit_power_law(x: List[float], y: List[float]) -> FitResult:
    """Fit delta(L) = a * L^(-alpha) via log-linearization (2 parameters).

    ln(delta) = ln(a) - alpha * ln(L)
    OLS on (ln(L), ln(delta)).
    """
    n = len(x)
    # Filter out non-positive y values (can't take log)
    valid = [(x[i], y[i]) for i in range(n) if x[i] > 0 and y[i] > 1e-15]
    if len(valid) < 2:
        # Can't fit -- return a terrible fit
        return _make_fit_result(
            ModelFamily.POWER_LAW.value, {'a': 0.0, 'alpha': 0.0},
            x, y, [0.0] * n, n_params=2, converged=False,
        )

    log_x = [math.log(v[0]) for v in valid]
    log_y = [math.log(v[1]) for v in valid]

    m = len(log_x)
    lx_mean = _mean(log_x)
    ly_mean = _mean(log_y)
    ss_xx = sum((log_x[i] - lx_mean) ** 2 for i in range(m))
    ss_xy = sum((log_x[i] - lx_mean) * (log_y[i] - ly_mean) for i in range(m))

    if abs(ss_xx) < 1e-30:
        return _make_fit_result(
            ModelFamily.POWER_LAW.value, {'a': 0.0, 'alpha': 0.0},
            x, y, [0.0] * n, n_params=2, converged=False,
        )

    neg_alpha = ss_xy / ss_xx
    ln_a = ly_mean - neg_alpha * lx_mean
    a = math.exp(ln_a) if abs(ln_a) < 500 else 0.0
    alpha = -neg_alpha

    y_pred = []
    for xi in x:
        if xi > 0 and abs(alpha) < 100:
            y_pred.append(a * xi ** (-alpha))
        else:
            y_pred.append(a)

    return _make_fit_result(
        ModelFamily.POWER_LAW.value, {'a': a, 'alpha': alpha},
        x, y, y_pred, n_params=2,
    )


# ================================================================
#  NELDER-MEAD SIMPLEX OPTIMIZER (pure Python, ~60 lines)
# ================================================================

def _nelder_mead(
    objective,
    x0: List[float],
    max_iter: int = 500,
    tol: float = 1e-10,
    initial_step: float = 0.5,
) -> Tuple[List[float], float, bool]:
    """Minimize objective(params) using Nelder-Mead simplex.

    Args:
        objective: callable(List[float]) -> float
        x0: initial parameter vector
        max_iter: maximum iterations
        tol: convergence tolerance on simplex range
        initial_step: initial simplex edge length

    Returns:
        (best_params, best_value, converged)
    """
    n = len(x0)
    # Build initial simplex: n+1 vertices
    simplex = [list(x0)]
    for i in range(n):
        vertex = list(x0)
        vertex[i] += initial_step
        simplex.append(vertex)

    # Evaluate
    values = [objective(v) for v in simplex]

    # Reflection/expansion/contraction coefficients
    alpha_r = 1.0
    gamma = 2.0
    rho = 0.5
    sigma = 0.5

    converged = False
    for iteration in range(max_iter):
        # Sort by value
        order = sorted(range(n + 1), key=lambda i: values[i])
        simplex = [simplex[i] for i in order]
        values = [values[i] for i in order]

        # Check convergence: range of values
        val_range = values[-1] - values[0]
        if val_range < tol:
            converged = True
            break

        # Centroid of all except worst
        centroid = [0.0] * n
        for i in range(n):
            for j in range(n):
                centroid[j] += simplex[i][j]
            # dividing after loop
        centroid = [c / n for c in centroid]

        # Reflection
        worst = simplex[-1]
        reflected = [centroid[j] + alpha_r * (centroid[j] - worst[j]) for j in range(n)]
        f_r = objective(reflected)

        if values[0] <= f_r < values[-2]:
            # Accept reflection
            simplex[-1] = reflected
            values[-1] = f_r
        elif f_r < values[0]:
            # Try expansion
            expanded = [centroid[j] + gamma * (reflected[j] - centroid[j]) for j in range(n)]
            f_e = objective(expanded)
            if f_e < f_r:
                simplex[-1] = expanded
                values[-1] = f_e
            else:
                simplex[-1] = reflected
                values[-1] = f_r
        else:
            # Contraction
            contracted = [centroid[j] + rho * (worst[j] - centroid[j]) for j in range(n)]
            f_c = objective(contracted)
            if f_c < values[-1]:
                simplex[-1] = contracted
                values[-1] = f_c
            else:
                # Shrink toward best
                best = simplex[0]
                for i in range(1, n + 1):
                    simplex[i] = [best[j] + sigma * (simplex[i][j] - best[j]) for j in range(n)]
                    values[i] = objective(simplex[i])

    return simplex[0], values[0], converged


# ================================================================
#  NONLINEAR FITTERS (via Nelder-Mead)
# ================================================================

def _fit_exp_decay(x: List[float], y: List[float]) -> FitResult:
    """Fit delta(L) = a * exp(-lambda * L) + c  (3 parameters).

    Initial guess:
      c ~ min(y)
      a ~ max(y) - min(y)
      lambda ~ estimated from log-slope
    """
    n = len(x)
    if n < 3:
        return _fit_constant(x, y)

    y_min = min(y)
    y_max = max(y)
    y_range = y_max - y_min

    # Initial guesses
    c0 = y_min
    a0 = y_range if y_range > 1e-15 else 0.01
    # Estimate lambda from first-to-last ratio
    if y_range > 1e-15 and y[0] > y_min + 1e-15:
        x_span = x[-1] - x[0]
        if x_span > 0:
            lam0 = safe_div(safe_log((y[0] - y_min + 1e-15) / (y[-1] - y_min + 1e-15)),
                            x_span, 0.1)
            lam0 = max(0.001, min(lam0, 10.0))
        else:
            lam0 = 0.1
    else:
        lam0 = 0.1

    def objective(params):
        a, lam, c = params
        total = 0.0
        for i in range(n):
            pred = a * math.exp(-max(-50, min(50, lam * x[i]))) + c
            total += (pred - y[i]) ** 2
        return total

    best, _, conv = _nelder_mead(objective, [a0, lam0, c0], max_iter=800)
    a, lam, c = best

    y_pred = [a * math.exp(-max(-50, min(50, lam * xi))) + c for xi in x]
    return _make_fit_result(
        ModelFamily.EXP_DECAY.value, {'a': a, 'lambda': lam, 'c': c},
        x, y, y_pred, n_params=3, converged=conv,
    )


def _fit_damped_osc(x: List[float], y: List[float]) -> FitResult:
    """Fit delta(L) = a * exp(-gamma*L) * cos(omega*L + phi) + c  (5 parameters).

    Initial guess from spectral analysis + decay envelope.
    """
    n = len(x)
    if n < 5:
        return _fit_constant(x, y)

    y_min = min(y)
    y_max = max(y)
    y_mean = _mean(y)
    y_range = y_max - y_min

    # Estimate frequency from zero-crossings around mean
    crossings = 0
    for i in range(1, n):
        if (y[i] - y_mean) * (y[i - 1] - y_mean) < 0:
            crossings += 1
    omega0 = math.pi * crossings / max(1, n - 1) if crossings > 0 else 0.5

    c0 = y_mean
    a0 = y_range / 2 if y_range > 1e-15 else 0.01
    gamma0 = 0.05
    phi0 = 0.0

    def objective(params):
        a, gamma, omega, phi, c = params
        total = 0.0
        for i in range(n):
            arg = -max(-50, min(50, gamma * x[i]))
            pred = a * math.exp(arg) * math.cos(omega * x[i] + phi) + c
            total += (pred - y[i]) ** 2
        return total

    best, _, conv = _nelder_mead(
        objective, [a0, gamma0, omega0, phi0, c0],
        max_iter=1000, initial_step=0.3,
    )
    a, gamma, omega, phi, c = best

    y_pred = []
    for xi in x:
        arg = -max(-50, min(50, gamma * xi))
        y_pred.append(a * math.exp(arg) * math.cos(omega * xi + phi) + c)

    return _make_fit_result(
        ModelFamily.DAMPED_OSC.value,
        {'a': a, 'gamma': gamma, 'omega': omega, 'phi': phi, 'c': c},
        x, y, y_pred, n_params=5, converged=conv,
    )


def _fit_pure_osc(x: List[float], y: List[float]) -> FitResult:
    """Fit delta(L) = a * cos(omega*L + phi) + c  (3 parameters).

    Pure oscillation without decay -- for truly oscillating trajectories.
    """
    n = len(x)
    if n < 3:
        return _fit_constant(x, y)

    y_mean = _mean(y)
    y_range = max(y) - min(y)

    # Estimate frequency from zero crossings around mean
    crossings = 0
    for i in range(1, n):
        if (y[i] - y_mean) * (y[i - 1] - y_mean) < 0:
            crossings += 1
    omega0 = math.pi * crossings / max(1, n - 1) if crossings > 0 else 0.5

    a0 = y_range / 2 if y_range > 1e-15 else 0.01
    c0 = y_mean
    phi0 = 0.0

    def objective(params):
        a, omega, phi, c = params
        total = 0.0
        for i in range(n):
            pred = a * math.cos(omega * x[i] + phi) + c
            total += (pred - y[i]) ** 2
        return total

    best, _, conv = _nelder_mead(
        objective, [a0, omega0, phi0, c0],
        max_iter=800, initial_step=0.3,
    )
    a, omega, phi, c = best

    y_pred = [a * math.cos(omega * xi + phi) + c for xi in x]
    return _make_fit_result(
        ModelFamily.PURE_OSC.value,
        {'a': a, 'omega': omega, 'phi': phi, 'c': c},
        x, y, y_pred, n_params=4, converged=conv,
    )


# ================================================================
#  MODEL SELECTION
# ================================================================

def _select_best_model(fits: Dict[str, FitResult]) -> Tuple[str, float]:
    """Select best model by BIC with parsimony tiebreaker.

    Returns (best_family, confidence) where confidence is the
    BIC advantage of best over runner-up, mapped to [0, 1].
    """
    if not fits:
        return ModelFamily.UNRESOLVED.value, 0.0

    # Filter to converged fits
    valid = {k: v for k, v in fits.items() if v.converged}
    if not valid:
        valid = fits  # Fall back to all if none converged

    # Sort by BIC (lower is better), then by n_params (parsimony tiebreaker)
    ranked = sorted(valid.items(), key=lambda kv: (kv[1].bic, kv[1].n_params))

    best_key = ranked[0][0]
    best_bic = ranked[0][1].bic

    if len(ranked) >= 2:
        runner_bic = ranked[1][1].bic
        delta_bic = runner_bic - best_bic
        # Map BIC difference to confidence: delta_bic > 10 is "very strong"
        confidence = clamp(delta_bic / 20.0)
    else:
        confidence = 1.0

    return best_key, confidence


# ================================================================
#  ASYMPTOTIC PREDICTION
# ================================================================

def _predict_asymptotic(family: str, params: dict) -> Tuple[str, float]:
    """Predict delta(L -> infinity) from the fitted model.

    Returns (AsymptoticClass value, predicted limit value).
    """
    EPS = 0.005  # Threshold: below this = AFFIRMATIVE

    if family == ModelFamily.CONSTANT.value:
        c = params.get('c', 0.0)
        if abs(c) < EPS:
            return AsymptoticClass.AFFIRMATIVE.value, c
        return AsymptoticClass.GAP.value, c

    elif family == ModelFamily.LINEAR.value:
        a = params.get('a', 0.0)
        b = params.get('b', 0.0)
        # Linear: delta -> +/- infinity if a != 0
        if abs(a) < 1e-10:
            # Essentially constant
            if abs(b) < EPS:
                return AsymptoticClass.AFFIRMATIVE.value, b
            return AsymptoticClass.GAP.value, b
        if a < 0:
            # Decreasing -- but delta is non-negative, so it hits 0
            return AsymptoticClass.AFFIRMATIVE.value, 0.0
        # Increasing -- gap grows
        return AsymptoticClass.GAP.value, float('inf')

    elif family == ModelFamily.POWER_LAW.value:
        alpha = params.get('alpha', 0.0)
        if alpha > 0:
            # delta ~ L^(-alpha) -> 0
            return AsymptoticClass.AFFIRMATIVE.value, 0.0
        elif alpha < -1e-10:
            # delta ~ L^|alpha| -> infinity (gap grows)
            return AsymptoticClass.GAP.value, float('inf')
        else:
            # alpha ~ 0 -> constant
            a = params.get('a', 0.0)
            if abs(a) < EPS:
                return AsymptoticClass.AFFIRMATIVE.value, a
            return AsymptoticClass.GAP.value, a

    elif family == ModelFamily.EXP_DECAY.value:
        lam = params.get('lambda', 0.0)
        c = params.get('c', 0.0)
        if lam > 0:
            # Decays to c
            if abs(c) < EPS:
                return AsymptoticClass.AFFIRMATIVE.value, c
            return AsymptoticClass.GAP.value, c
        elif lam < 0:
            # Grows exponentially (gap grows)
            return AsymptoticClass.GAP.value, float('inf')
        else:
            a = params.get('a', 0.0)
            val = a + c
            if abs(val) < EPS:
                return AsymptoticClass.AFFIRMATIVE.value, val
            return AsymptoticClass.GAP.value, val

    elif family == ModelFamily.DAMPED_OSC.value:
        gamma = params.get('gamma', 0.0)
        c = params.get('c', 0.0)
        if gamma > 0:
            # Oscillation dies, converges to c
            if abs(c) < EPS:
                return AsymptoticClass.AFFIRMATIVE.value, c
            return AsymptoticClass.GAP.value, c
        # Undamped or growing oscillation
        return AsymptoticClass.INDETERMINATE.value, abs(c)

    elif family == ModelFamily.PURE_OSC.value:
        # Oscillates forever -> indeterminate
        c = params.get('c', 0.0)
        a = params.get('a', 0.0)
        # If amplitude is tiny, it's effectively constant
        if abs(a) < 1e-6:
            if abs(c) < EPS:
                return AsymptoticClass.AFFIRMATIVE.value, c
            return AsymptoticClass.GAP.value, c
        return AsymptoticClass.INDETERMINATE.value, abs(c)

    return AsymptoticClass.INDETERMINATE.value, 0.0


# ================================================================
#  LATEX FORMATTING
# ================================================================

def _format_latex(family: str, params: dict) -> str:
    """Format the fitted equation as a LaTeX string."""

    def _fmt(v, prec=4):
        return f'{v:.{prec}f}'

    if family == ModelFamily.CONSTANT.value:
        return f'\\delta(L) = {_fmt(params["c"])}'

    elif family == ModelFamily.LINEAR.value:
        a, b = params['a'], params['b']
        sign = '+' if b >= 0 else '-'
        return f'\\delta(L) = {_fmt(a)} L {sign} {_fmt(abs(b))}'

    elif family == ModelFamily.POWER_LAW.value:
        a, alpha = params['a'], params['alpha']
        return f'\\delta(L) = {_fmt(a)} \\cdot L^{{{_fmt(-alpha)}}}'

    elif family == ModelFamily.EXP_DECAY.value:
        a, lam, c = params['a'], params['lambda'], params['c']
        sign = '+' if c >= 0 else '-'
        return (f'\\delta(L) = {_fmt(a)} e^{{{_fmt(-lam)} L}} '
                f'{sign} {_fmt(abs(c))}')

    elif family == ModelFamily.DAMPED_OSC.value:
        a = params['a']
        gamma = params['gamma']
        omega = params['omega']
        phi = params['phi']
        c = params['c']
        sign = '+' if c >= 0 else '-'
        return (f'\\delta(L) = {_fmt(a)} e^{{{_fmt(-gamma)} L}} '
                f'\\cos({_fmt(omega)} L + {_fmt(phi)}) '
                f'{sign} {_fmt(abs(c))}')

    elif family == ModelFamily.PURE_OSC.value:
        a = params['a']
        omega = params['omega']
        phi = params['phi']
        c = params['c']
        sign = '+' if c >= 0 else '-'
        return (f'\\delta(L) = {_fmt(a)} '
                f'\\cos({_fmt(omega)} L + {_fmt(phi)}) '
                f'{sign} {_fmt(abs(c))}')

    return '\\delta(L) = \\text{{unresolved}}'


# ================================================================
#  TOP-LEVEL API
# ================================================================

def extract_governing_equation(
    levels: List[int],
    delta_by_level: List[float],
    problem: str = '',
    regime: str = '',
    test_case: str = '',
) -> GoverningEquation:
    """Fit all model families to a delta(L) trajectory and select the best.

    Args:
        levels: Fractal levels [3, 4, ..., 24]
        delta_by_level: Delta values at each level
        problem: Problem ID (for labeling)
        regime: 'calibration' or 'frontier'
        test_case: Test case name

    Returns:
        GoverningEquation with best model, all fits, and asymptotic prediction.
    """
    x = [float(lv) for lv in levels]
    y = list(delta_by_level)

    # Fit all families
    fits = {}
    fits[ModelFamily.CONSTANT.value] = _fit_constant(x, y)
    fits[ModelFamily.LINEAR.value] = _fit_linear(x, y)
    fits[ModelFamily.POWER_LAW.value] = _fit_power_law(x, y)
    fits[ModelFamily.EXP_DECAY.value] = _fit_exp_decay(x, y)
    fits[ModelFamily.DAMPED_OSC.value] = _fit_damped_osc(x, y)
    fits[ModelFamily.PURE_OSC.value] = _fit_pure_osc(x, y)

    # Select best
    best_family, confidence = _select_best_model(fits)
    best_fit = fits.get(best_family, fits.get(ModelFamily.CONSTANT.value))

    # Asymptotic prediction
    asym_class, asym_value = _predict_asymptotic(best_family, best_fit.params)

    # LaTeX
    latex = _format_latex(best_family, best_fit.params)

    return GoverningEquation(
        problem=problem,
        regime=regime,
        test_case=test_case,
        best_model=best_family,
        best_fit=best_fit,
        all_fits=fits,
        asymptotic_class=asym_class,
        asymptotic_value=asym_value,
        latex=latex,
        confidence=confidence,
    )


def extract_equation_atlas(
    atlas: Dict[str, object],
) -> EquationAtlasResult:
    """Extract governing equations for every entry in a fractal atlas.

    Args:
        atlas: Dict mapping key -> FractalFingerprint (or any object
               with .levels, .delta_by_level, .problem, .regime, .test_case)

    Returns:
        EquationAtlasResult with all equations and classification counts.
    """
    equations = {}
    n_aff = 0
    n_gap = 0
    n_ind = 0

    for key, fp in atlas.items():
        eq = extract_governing_equation(
            levels=fp.levels,
            delta_by_level=fp.delta_by_level,
            problem=fp.problem,
            regime=fp.regime,
            test_case=fp.test_case,
        )
        equations[key] = eq

        if eq.asymptotic_class == AsymptoticClass.AFFIRMATIVE.value:
            n_aff += 1
        elif eq.asymptotic_class == AsymptoticClass.GAP.value:
            n_gap += 1
        else:
            n_ind += 1

    return EquationAtlasResult(
        equations=equations,
        n_affirmative=n_aff,
        n_gap=n_gap,
        n_indeterminate=n_ind,
    )
