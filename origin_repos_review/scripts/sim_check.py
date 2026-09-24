"""Run a copy of simulate_dual_lattice.py with its output redirected to scratch,
then probe its claims (C*, t90 invariance, dual lattice, 'coherence' metric)."""
import numpy as np, os, io, contextlib

SRC = r"C:\Users\brayd\OneDrive\Desktop\Sprints\_brayden_repos\Dual-Lattice-Self-Healing\simulate_dual_lattice.py.txt"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "sim_output")
code = open(SRC, encoding="utf-8").read()
assert 'OUT_DIR = "output"' in code
code = code.replace('OUT_DIR = "output"', f'OUT_DIR = r"{OUT}"')
ns = {"__name__": "sim"}
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    exec(compile(code, "simulate_dual_lattice(copy)", "exec"), ns)
print("---- baseline run output (copy of the committed script) ----")
print(buf.getvalue())
C = ns["C_history"]; T = ns["record_times"]; SD = ns["scar_density_history"]
i_min = int(np.argmin(C))
print(f"C(0)={C[0]:.3f}  min C={C[i_min]:.3f} at t={T[i_min]:.2f}  C(end)={C[-1]:.3f}  scar density end={SD[-1]:.3f}")
print("first 16 recorded C:", np.round(C[:16], 3).tolist())
print("recorded times step:", T[1] - T[0])
phi_dual = ns["phi_dual"]
print("phi_dual amplitude (std):", float(phi_dual.std()), " max|phi_dual|:", float(np.abs(phi_dual).max()))
phi_final = ns["phi_final"] if "phi_final" in ns else ns["phi"]
print("final phi: mean |phi| = %.3f, fraction |phi|>1.2 = %.3f" % (np.abs(ns['phi']).mean(), (np.abs(ns['phi']) > 1.2).mean()))

# FFT roundtrip identity
rng = np.random.default_rng(0)
x = 0.01 * rng.normal(size=(100, 100))
from scipy.fft import fft2, ifft2
print("ifft2(fft2(x)) == x (max abs diff):", float(np.abs(np.real(ifft2(fft2(x))) - x).max()))

# 'coherence' metric on reference fields
cm = ns["coherence_metric"]
zero_scars = np.zeros((100, 100), bool)
print("\nC for reference fields (no scars):")
print("   uniform phi=+1 (perfectly ordered)  C = %.3f" % cm(np.ones((100, 100)), zero_scars))
print("   phi = 0 everywhere                  C = %.3f" % cm(np.zeros((100, 100)), zero_scars))
print("   iid N(0,1) noise (disorder)         C = %.3f" % cm(rng.normal(size=(100, 100)), zero_scars))
print("   checkerboard +-1 (max gradient)     C = %.3f" % cm(np.indices((100, 100)).sum(0) % 2 * 2 - 1.0, zero_scars))
print("   uniform +1 with ALL sites scarred   C = %.3f" % cm(np.ones((100, 100)), np.ones((100, 100), bool)))


# ---- damage/recovery with fine time resolution, using the script's own dynamics
def step_fn(state, p, rng):
    phi, m, scars, scar_values, t = state
    lap = ns["laplacian"]; grad = ns["compute_gradient_magnitude"]
    collapse = -(phi ** 3 - phi)
    diff = p["D"] * lap(phi)
    dual = p["LAMBDA"] * (p["phi_dual"] - phi)
    m = (1.0 - p["ALPHA"]) * m + p["ALPHA"] * phi
    noise = p["ETA"] * rng.normal(size=phi.shape) * phi
    g = grad(phi)
    new = (g > p["THETA"]) & (~scars)
    scars = scars | new
    scar_values = np.where(new, phi, scar_values)
    scar_pot = p["MU"] * scars * (scar_values - phi)
    phi = np.clip(phi + p["DT"] * (collapse + diff + dual + m + scar_pot + noise), -3, 3)
    return (phi, m, scars, scar_values, t + p["DT"])


def run_damage(params, damage=0.3, pre_steps=5000, post_steps=2000, seed=1):
    rng = np.random.default_rng(seed)
    phi = 0.01 * rng.normal(size=(100, 100))
    p = dict(params); p["phi_dual"] = phi.copy()
    st = (phi, np.zeros_like(phi), np.zeros_like(phi, bool), np.zeros_like(phi), 0.0)
    for _ in range(pre_steps):
        st = step_fn(st, p, rng)
    phi, m, scars, sv, t = st
    C_before = cm(phi, scars)
    idx = np.argwhere(scars)
    kill = idx[rng.choice(len(idx), int(damage * len(idx)), replace=False)]
    scars = scars.copy(); scars[kill[:, 0], kill[:, 1]] = False
    st = (phi, m, scars, sv, t)
    C_after = cm(phi, scars)
    hist = [C_after]
    for _ in range(post_steps):
        st = step_fn(st, p, rng)
        hist.append(cm(st[0], st[2]))
    hist = np.array(hist)
    C_final = hist[-1]
    # t90: first time C recovers 90% of the drop (C_after -> C_before)
    target = C_after + 0.9 * (C_before - C_after)
    fine = np.argmax(hist >= target) if np.any(hist >= target) else -1
    # same with the script's recording cadence (every 50 steps)
    coarse_idx = np.arange(0, len(hist), 50)
    coarse = coarse_idx[np.argmax(hist[coarse_idx] >= target)] if np.any(hist[coarse_idx] >= target) else -1
    return dict(C_before=C_before, C_after=C_after, C_final=C_final,
                t90_fine=fine * p["DT"] if fine >= 0 else None,
                t90_at_0p5_cadence=coarse * p["DT"] if coarse >= 0 else None,
                scars_before=int(len(idx)))


base = dict(D=0.1, LAMBDA=0.2, ALPHA=0.05, ETA=0.1, THETA=0.7, MU=0.5, DT=0.01)
print("\n---- 30% scar-removal damage, recovery measured at every step vs every 50 steps ----")
rows = []
for name, over in [("baseline", {}), ("alpha=0.01", {"ALPHA": 0.01}), ("alpha=0.2", {"ALPHA": 0.2}),
                   ("lambda=0.05", {"LAMBDA": 0.05}), ("lambda=0.5", {"LAMBDA": 0.5}),
                   ("mu=0", {"MU": 0.0}), ("mu=2", {"MU": 2.0}), ("theta=0.5", {"THETA": 0.5}), ("theta=1.0", {"THETA": 1.0})]:
    p = dict(base); p.update(over)
    r = run_damage(p, damage=0.3, pre_steps=3000, post_steps=1000)
    print(f"{name:12s} scars={r['scars_before']:5d} C_before={r['C_before']:.3f} C_after={r['C_after']:.3f} "
          f"C_final={r['C_final']:.3f} t90(fine)={r['t90_fine']} t90(0.5 cadence)={r['t90_at_0p5_cadence']}")
