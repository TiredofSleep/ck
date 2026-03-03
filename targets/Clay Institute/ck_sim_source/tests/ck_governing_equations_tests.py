"""
ck_governing_equations_tests.py -- Tests for Governing Equations Engine
=======================================================================
Operator: PULSE (3) -- Testing the heartbeat of the equation engine.

Tests:
  1. OLS fitters (constant, linear)
  2. Power law (log-linearized)
  3. Nelder-Mead simplex (basic optimization)
  4. Exp decay fitter
  5. Damped oscillation fitter
  6. Pure oscillation fitter
  7. Model selection (BIC)
  8. Asymptotic prediction
  9. LaTeX formatting
  10. Full equation extraction
  11. Atlas extraction

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
import unittest

from ck_sim.doing.ck_governing_equations import (
    ModelFamily, AsymptoticClass,
    FitResult, GoverningEquation, EquationAtlasResult,
    _mean, _variance, _r_squared, _aic, _bic, _durbin_watson,
    _fit_constant, _fit_linear, _fit_power_law,
    _fit_exp_decay, _fit_damped_osc, _fit_pure_osc,
    _nelder_mead, _select_best_model, _predict_asymptotic,
    _format_latex,
    extract_governing_equation, extract_equation_atlas,
)


class TestStatisticalHelpers(unittest.TestCase):
    """Test basic statistical functions."""

    def test_mean(self):
        self.assertAlmostEqual(_mean([1.0, 2.0, 3.0]), 2.0)
        self.assertAlmostEqual(_mean([5.0]), 5.0)
        self.assertAlmostEqual(_mean([]), 0.0)

    def test_variance(self):
        xs = [1.0, 2.0, 3.0, 4.0, 5.0]
        mu = _mean(xs)
        self.assertAlmostEqual(_variance(xs, mu), 2.0)
        self.assertAlmostEqual(_variance([], 0.0), 0.0)

    def test_r_squared_perfect(self):
        y = [1.0, 2.0, 3.0, 4.0]
        r2 = _r_squared(y, y)
        self.assertAlmostEqual(r2, 1.0)

    def test_r_squared_bad(self):
        y_obs = [1.0, 2.0, 3.0]
        y_pred = [3.0, 1.0, 2.0]
        r2 = _r_squared(y_obs, y_pred)
        self.assertLess(r2, 0.5)

    def test_aic_bic_finite(self):
        aic_val = _aic(0.5, 10, 2)
        bic_val = _bic(0.5, 10, 2)
        self.assertTrue(math.isfinite(aic_val))
        self.assertTrue(math.isfinite(bic_val))
        # BIC penalizes more parameters more heavily for n > 7
        self.assertGreater(bic_val, aic_val - 10)

    def test_durbin_watson_uncorrelated(self):
        # Random-ish residuals should give DW near 2
        residuals = [0.1, -0.05, 0.08, -0.03, 0.02, -0.07, 0.04]
        dw = _durbin_watson(residuals)
        self.assertGreater(dw, 1.0)
        self.assertLess(dw, 3.0)

    def test_durbin_watson_short(self):
        self.assertAlmostEqual(_durbin_watson([0.1, 0.2]), 2.0)


class TestOLSFitters(unittest.TestCase):
    """Test constant and linear fits."""

    def test_constant_fit(self):
        y = [0.5, 0.5, 0.5, 0.5, 0.5]
        x = [3.0, 4.0, 5.0, 6.0, 7.0]
        fit = _fit_constant(x, y)
        self.assertEqual(fit.family, ModelFamily.CONSTANT.value)
        self.assertAlmostEqual(fit.params['c'], 0.5)
        self.assertAlmostEqual(fit.r_squared, 1.0)  # Perfect when all y equal
        self.assertAlmostEqual(fit.rss, 0.0, places=10)

    def test_linear_fit_perfect(self):
        x = [1.0, 2.0, 3.0, 4.0, 5.0]
        y = [2.0 * xi + 1.0 for xi in x]  # y = 2x + 1
        fit = _fit_linear(x, y)
        self.assertEqual(fit.family, ModelFamily.LINEAR.value)
        self.assertAlmostEqual(fit.params['a'], 2.0, places=8)
        self.assertAlmostEqual(fit.params['b'], 1.0, places=8)
        self.assertAlmostEqual(fit.r_squared, 1.0, places=8)

    def test_linear_fit_noisy(self):
        x = [3.0, 6.0, 9.0, 12.0, 15.0, 18.0, 21.0, 24.0]
        # y ~ -0.01*x + 0.5 + noise
        y = [0.47, 0.44, 0.41, 0.38, 0.35, 0.32, 0.30, 0.27]
        fit = _fit_linear(x, y)
        self.assertLess(fit.params['a'], 0)  # Negative slope
        self.assertGreater(fit.r_squared, 0.95)


class TestPowerLawFitter(unittest.TestCase):
    """Test log-linearized power law fitting."""

    def test_power_law_perfect(self):
        # delta(L) = 2.0 * L^(-1.5)
        x = [3.0, 5.0, 8.0, 12.0, 18.0, 24.0]
        y = [2.0 * xi ** (-1.5) for xi in x]
        fit = _fit_power_law(x, y)
        self.assertEqual(fit.family, ModelFamily.POWER_LAW.value)
        self.assertAlmostEqual(fit.params['alpha'], 1.5, places=3)
        self.assertAlmostEqual(fit.params['a'], 2.0, places=2)
        self.assertGreater(fit.r_squared, 0.99)

    def test_power_law_zero_values(self):
        x = [3.0, 4.0, 5.0]
        y = [0.0, 0.0, 0.0]
        fit = _fit_power_law(x, y)
        # Should handle gracefully (non-convergent)
        self.assertFalse(fit.converged)


class TestNelderMead(unittest.TestCase):
    """Test the pure-Python Nelder-Mead optimizer."""

    def test_quadratic_minimum(self):
        # Minimize (x-3)^2 + (y-2)^2
        def f(p):
            return (p[0] - 3.0) ** 2 + (p[1] - 2.0) ** 2

        best, val, conv = _nelder_mead(f, [0.0, 0.0], max_iter=500)
        self.assertTrue(conv)
        self.assertAlmostEqual(best[0], 3.0, places=3)
        self.assertAlmostEqual(best[1], 2.0, places=3)
        self.assertLess(val, 1e-6)

    def test_rosenbrock_valley(self):
        # Rosenbrock: f(x,y) = (1-x)^2 + 100*(y-x^2)^2
        # Minimum at (1, 1)
        def f(p):
            return (1.0 - p[0]) ** 2 + 100.0 * (p[1] - p[0] ** 2) ** 2

        best, val, conv = _nelder_mead(f, [0.0, 0.0], max_iter=2000, tol=1e-12)
        # Nelder-Mead may not perfectly solve Rosenbrock but should get close
        self.assertLess(abs(best[0] - 1.0), 0.1)
        self.assertLess(abs(best[1] - 1.0), 0.1)

    def test_1d_minimum(self):
        def f(p):
            return (p[0] - 5.0) ** 2
        best, val, conv = _nelder_mead(f, [4.0], initial_step=0.1)
        self.assertTrue(conv)
        self.assertLess(abs(best[0] - 5.0), 0.15)
        self.assertLess(val, 0.05)


class TestExpDecayFitter(unittest.TestCase):
    """Test exponential decay fitting."""

    def test_exp_decay_synthetic(self):
        # delta(L) = 0.8 * exp(-0.2 * L) + 0.05
        x = list(range(3, 25))
        y = [0.8 * math.exp(-0.2 * xi) + 0.05 for xi in x]
        fit = _fit_exp_decay(x, y)
        self.assertEqual(fit.family, ModelFamily.EXP_DECAY.value)
        self.assertGreater(fit.r_squared, 0.99)
        # Check parameter recovery
        self.assertAlmostEqual(fit.params['c'], 0.05, places=2)
        self.assertGreater(fit.params['lambda'], 0.1)

    def test_exp_decay_flat(self):
        x = [3.0, 6.0, 9.0, 12.0]
        y = [0.5, 0.5, 0.5, 0.5]
        fit = _fit_exp_decay(x, y)
        # Should converge to essentially constant
        self.assertTrue(fit.converged)


class TestDampedOscFitter(unittest.TestCase):
    """Test damped oscillation fitting."""

    def test_damped_osc_synthetic(self):
        # delta(L) = 0.3 * exp(-0.1*L) * cos(0.8*L) + 0.2
        x = list(range(3, 25))
        y = [0.3 * math.exp(-0.1 * xi) * math.cos(0.8 * xi) + 0.2 for xi in x]
        fit = _fit_damped_osc(x, y)
        self.assertEqual(fit.family, ModelFamily.DAMPED_OSC.value)
        self.assertGreater(fit.r_squared, 0.90)
        self.assertTrue(fit.converged)


class TestPureOscFitter(unittest.TestCase):
    """Test pure oscillation fitting."""

    def test_pure_osc_synthetic(self):
        # delta(L) = 0.1 * cos(0.5*L + 1.0) + 0.4
        x = list(range(3, 25))
        y = [0.1 * math.cos(0.5 * xi + 1.0) + 0.4 for xi in x]
        fit = _fit_pure_osc(x, y)
        self.assertEqual(fit.family, ModelFamily.PURE_OSC.value)
        self.assertGreater(fit.r_squared, 0.90)


class TestModelSelection(unittest.TestCase):
    """Test BIC-based model selection."""

    def test_constant_wins_for_flat(self):
        x = list(range(3, 25))
        y = [0.5] * len(x)
        fits = {
            ModelFamily.CONSTANT.value: _fit_constant(x, y),
            ModelFamily.LINEAR.value: _fit_linear(x, y),
        }
        best, conf = _select_best_model(fits)
        # Constant should win (fewer params, same fit)
        self.assertEqual(best, ModelFamily.CONSTANT.value)

    def test_linear_wins_for_slope(self):
        x = list(range(3, 15))
        y = [0.01 * xi + 0.1 for xi in x]
        fits = {
            ModelFamily.CONSTANT.value: _fit_constant(x, y),
            ModelFamily.LINEAR.value: _fit_linear(x, y),
        }
        best, conf = _select_best_model(fits)
        self.assertEqual(best, ModelFamily.LINEAR.value)

    def test_empty_fits(self):
        best, conf = _select_best_model({})
        self.assertEqual(best, ModelFamily.UNRESOLVED.value)


class TestAsymptoticPrediction(unittest.TestCase):
    """Test asymptotic classification."""

    def test_constant_gap(self):
        ac, val = _predict_asymptotic(ModelFamily.CONSTANT.value, {'c': 0.5})
        self.assertEqual(ac, AsymptoticClass.GAP.value)
        self.assertAlmostEqual(val, 0.5)

    def test_constant_affirmative(self):
        ac, val = _predict_asymptotic(ModelFamily.CONSTANT.value, {'c': 0.001})
        self.assertEqual(ac, AsymptoticClass.AFFIRMATIVE.value)

    def test_power_law_decay(self):
        ac, val = _predict_asymptotic(ModelFamily.POWER_LAW.value, {'a': 1.0, 'alpha': 1.5})
        self.assertEqual(ac, AsymptoticClass.AFFIRMATIVE.value)
        self.assertAlmostEqual(val, 0.0)

    def test_power_law_growth(self):
        ac, val = _predict_asymptotic(ModelFamily.POWER_LAW.value, {'a': 1.0, 'alpha': -0.5})
        self.assertEqual(ac, AsymptoticClass.GAP.value)

    def test_exp_decay_to_zero(self):
        ac, val = _predict_asymptotic(ModelFamily.EXP_DECAY.value,
                                       {'a': 1.0, 'lambda': 0.2, 'c': 0.001})
        self.assertEqual(ac, AsymptoticClass.AFFIRMATIVE.value)

    def test_exp_decay_to_gap(self):
        ac, val = _predict_asymptotic(ModelFamily.EXP_DECAY.value,
                                       {'a': 1.0, 'lambda': 0.2, 'c': 0.5})
        self.assertEqual(ac, AsymptoticClass.GAP.value)

    def test_damped_osc_to_zero(self):
        ac, val = _predict_asymptotic(ModelFamily.DAMPED_OSC.value,
                                       {'a': 0.5, 'gamma': 0.1, 'omega': 1.0,
                                        'phi': 0.0, 'c': 0.001})
        self.assertEqual(ac, AsymptoticClass.AFFIRMATIVE.value)

    def test_pure_osc_indeterminate(self):
        ac, val = _predict_asymptotic(ModelFamily.PURE_OSC.value,
                                       {'a': 0.1, 'omega': 0.5, 'phi': 0.0, 'c': 0.3})
        self.assertEqual(ac, AsymptoticClass.INDETERMINATE.value)


class TestLatexFormatting(unittest.TestCase):
    """Test LaTeX equation output."""

    def test_constant_latex(self):
        latex = _format_latex(ModelFamily.CONSTANT.value, {'c': 0.5000})
        self.assertIn('\\delta(L)', latex)
        self.assertIn('0.5000', latex)

    def test_linear_latex(self):
        latex = _format_latex(ModelFamily.LINEAR.value, {'a': -0.01, 'b': 0.5})
        self.assertIn('L', latex)
        self.assertIn('\\delta(L)', latex)

    def test_power_law_latex(self):
        latex = _format_latex(ModelFamily.POWER_LAW.value, {'a': 2.0, 'alpha': 1.5})
        self.assertIn('L^{', latex)

    def test_exp_decay_latex(self):
        latex = _format_latex(ModelFamily.EXP_DECAY.value,
                              {'a': 0.8, 'lambda': 0.2, 'c': 0.05})
        self.assertIn('e^{', latex)


class TestEquationExtraction(unittest.TestCase):
    """Test the top-level extract_governing_equation function."""

    def test_extract_from_constant(self):
        levels = list(range(3, 25))
        delta = [0.5] * len(levels)
        eq = extract_governing_equation(levels, delta, 'test', 'cal', 'tc')
        self.assertEqual(eq.problem, 'test')
        self.assertEqual(eq.best_model, ModelFamily.CONSTANT.value)
        self.assertEqual(eq.asymptotic_class, AsymptoticClass.GAP.value)
        self.assertIn('\\delta(L)', eq.latex)

    def test_extract_from_decay(self):
        levels = list(range(3, 25))
        delta = [0.8 * math.exp(-0.15 * lv) + 0.001 for lv in levels]
        eq = extract_governing_equation(levels, delta, 'decay_test', 'cal', 'tc')
        # Should pick exp_decay or power_law
        self.assertIn(eq.best_model,
                       [ModelFamily.EXP_DECAY.value, ModelFamily.POWER_LAW.value])
        self.assertEqual(eq.asymptotic_class, AsymptoticClass.AFFIRMATIVE.value)
        self.assertGreater(eq.confidence, 0.0)

    def test_extract_all_fits_present(self):
        levels = list(range(3, 15))
        delta = [0.3 + 0.01 * i for i in range(len(levels))]
        eq = extract_governing_equation(levels, delta)
        self.assertEqual(len(eq.all_fits), 6)  # All 6 families
        for fam in ModelFamily:
            if fam != ModelFamily.UNRESOLVED:
                self.assertIn(fam.value, eq.all_fits)


class TestAtlasExtraction(unittest.TestCase):
    """Test equation extraction across a mock atlas."""

    def test_mock_atlas(self):
        class MockFP:
            def __init__(self, problem, regime, test_case, levels, delta_by_level):
                self.problem = problem
                self.regime = regime
                self.test_case = test_case
                self.levels = levels
                self.delta_by_level = delta_by_level

        levels = list(range(3, 25))
        atlas = {
            'ns_cal': MockFP('navier_stokes', 'calibration', 'lamb_oseen',
                             levels, [0.001] * len(levels)),
            'pvnp_frontier': MockFP('p_vs_np', 'frontier', 'hard',
                                    levels, [0.8] * len(levels)),
        }

        result = extract_equation_atlas(atlas)
        self.assertEqual(len(result.equations), 2)
        self.assertIn('ns_cal', result.equations)
        self.assertIn('pvnp_frontier', result.equations)

        # NS calibration (near zero) should be affirmative
        ns_eq = result.equations['ns_cal']
        self.assertEqual(ns_eq.asymptotic_class, AsymptoticClass.AFFIRMATIVE.value)

        # PvNP frontier (at 0.8) should be gap
        pvnp_eq = result.equations['pvnp_frontier']
        self.assertEqual(pvnp_eq.asymptotic_class, AsymptoticClass.GAP.value)

        # Counts
        self.assertEqual(result.n_affirmative, 1)
        self.assertEqual(result.n_gap, 1)
        self.assertEqual(result.n_indeterminate, 0)


if __name__ == '__main__':
    unittest.main()
