"""run_all.py -- CK-Walker v0: one command, CPU-only, fully seeded.

  python run_all.py

Produces RESULTS.md + results.json in this folder:
  P2  substrate (theorem-bearing) reservoir vs matched random ESN
      (3 seeds) vs NG-RC, on NARMA-10 / MackeyGlass-84 / Lorenz-x2z.
  P1  Gap Router vs uniform allocation vs oracle on the 24-channel
      mixed-failure suite, + UOP type-classification accuracy.

Honesty contract: numbers are written to RESULTS.md exactly as
measured, including any loss to baselines.

CC-BY-4.0. Sanders + Claude. 2026-06-10.
"""
import io
import json
import os
import time

import numpy as np

from substrate import SubstrateReservoir, ridge_fit, nrmse
from baselines import RandomESN, NGRC
from benchmarks import make_tasks
import gap_router

HERE = os.path.dirname(os.path.abspath(__file__))
WASHOUT = 200


def eval_model(feat_fn, u_tr, y_tr, u_te, y_te):
    Ftr = feat_fn(u_tr)[WASHOUT:]
    ytr = y_tr[WASHOUT:]
    w, lam = ridge_fit(Ftr, ytr)
    Fte = feat_fn(u_te)[WASHOUT:]
    yte = y_te[WASHOUT:]
    return nrmse(Fte @ w, yte), lam


def main():
    t0 = time.time()
    results = {"P2": {}, "P1": {}}
    tasks = make_tasks()

    sub0 = SubstrateReservoir()
    fm = sub0.fading_memory_check(tasks["NARMA-10"][0])
    print(f"substrate fading-memory check (L1 dist after 200 steps): "
          f"{fm:.2e}")
    results["fading_memory_L1"] = fm
    n_feat = sub0.run(np.zeros(3)).shape[1]
    print(f"feature width (matched across models): {n_feat}\n")

    # fair per-task hyperparameter grids, selected on a train-tail split
    SUB_GRID = [dict(leak=l) for l in (0.5, 0.7, 0.85, 0.95)]
    ESN_GRID = [dict(rho=r, leak=l) for r in (0.8, 0.95, 1.05)
                for l in (0.3, 0.55)]

    def tune(model_cls, grid, u_tr, y_tr, seed=None):
        n_val = len(u_tr) // 5
        best = (None, np.inf)
        for cfg in grid:
            m = (model_cls(n_feat, seed=seed, **cfg) if seed is not None
                 else model_cls(**cfg))
            F = m.run(u_tr)[WASHOUT:]
            yy = y_tr[WASHOUT:]
            w, _ = ridge_fit(F[:-n_val], yy[:-n_val])
            err = nrmse(F[-n_val:] @ w, yy[-n_val:])
            if err < best[1]:
                best = (m, err)
        return best[0]

    print(f"{'task':>15} | {'substrate':>10} | {'ESN mean+-sd':>16} | "
          f"{'NG-RC':>8}")
    for name, (u_tr, y_tr, u_te, y_te) in tasks.items():
        sub = tune(SubstrateReservoir, SUB_GRID, u_tr, y_tr)
        s_err, _ = eval_model(sub.run, u_tr, y_tr, u_te, y_te)
        esn_errs = []
        for seed in (0, 1, 2):
            esn = tune(RandomESN, ESN_GRID, u_tr, y_tr, seed=seed)
            e, _ = eval_model(esn.run, u_tr, y_tr, u_te, y_te)
            esn_errs.append(e)
        ng = NGRC()
        g_err, _ = eval_model(ng.run, u_tr, y_tr, u_te, y_te)
        results["P2"][name] = {
            "substrate": s_err,
            "esn_mean": float(np.mean(esn_errs)),
            "esn_std": float(np.std(esn_errs)),
            "ngrc": g_err,
        }
        print(f"{name:>15} | {s_err:>10.4f} | "
              f"{np.mean(esn_errs):>8.4f} +- {np.std(esn_errs):.4f} | "
              f"{g_err:>8.4f}")

    print("\nGap Router (P1):")
    p1 = gap_router.run_experiment()
    results["P1"] = p1
    print(json.dumps(p1, indent=1))

    results["runtime_s"] = round(time.time() - t0, 1)
    with io.open(os.path.join(HERE, "results.json"), "w") as f:
        json.dump(results, f, indent=1)

    # RESULTS.md
    lines = ["# CK-Walker v0 — Results", "",
             f"Runtime: {results['runtime_s']} s, CPU only, fully seeded. "
             f"Reproduce: `python run_all.py`.", "",
             f"Substrate fading-memory check (echo-state analog): final L1 "
             f"distance {fm:.2e} after 200 driven steps from far-apart "
             f"initial states.", "",
             "## P2 — theorem-bearing reservoir vs matched baselines "
             "(NRMSE, lower better)", "",
             "| task | substrate | random ESN (3 seeds) | NG-RC |",
             "|---|---|---|---|"]
    for name, r in results["P2"].items():
        lines.append(f"| {name} | {r['substrate']:.4f} | "
                     f"{r['esn_mean']:.4f} ± {r['esn_std']:.4f} | "
                     f"{r['ngrc']:.4f} |")
    p = results["P1"]
    lines += ["", "## P1 — Gap Router on the 24-channel mixed-failure suite "
              "(mean test MSE at matched budget, lower better)", "",
              "| allocator | mean test MSE | samples spent | notes |",
              "|---|---|---|---|",
              f"| uniform | {p['uniform']['mean_test_mse']:.5f} | "
              f"{p['uniform']['samples']} | no classification |",
              f"| **Gap Router** | {p['router']['mean_test_mse']:.5f} | "
              f"{p['router']['samples']} | type accuracy "
              f"{p['router']['type_accuracy']:.0%}, "
              f"{p['router']['frozen_channels']} channels frozen |",
              f"| oracle | {p['oracle']['mean_test_mse']:.5f} | "
              f"{p['oracle']['samples']} | ground-truth types |", "",
              "Interpretation contract: the suite is synthetic by design; "
              "the demonstrated content is (i) the four UOP failure types "
              "are identifiable from residual statistics alone, and (ii) "
              "routing by inferred type recovers near-oracle allocation. "
              "Real-task validity (ARC-style) is future work, "
              "pre-registered as P1 in CK_INTELLIGENCE_SYNTHESIS."]
    with io.open(os.path.join(HERE, "RESULTS.md"), "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"\nRESULTS.md + results.json written. "
          f"Total {results['runtime_s']} s.")


if __name__ == "__main__":
    main()
