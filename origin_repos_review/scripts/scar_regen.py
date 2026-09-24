"""Is '99.8% regeneration at original coordinates' just re-thresholding an undamaged field?
Re-implements the committed update rule (simulate_dual_lattice.py.txt) in scratch; pure computation."""
import numpy as np

N, DT, D, LAM, ALPHA, ETA, THETA, MU = 100, 0.01, 0.1, 0.2, 0.05, 0.1, 0.7, 0.5


def lap(f):
    return np.roll(f, -1, 0) + np.roll(f, 1, 0) + np.roll(f, -1, 1) + np.roll(f, 1, 1) - 4 * f


def grad(f):
    gx = (np.roll(f, -1, 0) - np.roll(f, 1, 0)) / 2
    gy = (np.roll(f, -1, 1) - np.roll(f, 1, 1)) / 2
    return np.sqrt(gx ** 2 + gy ** 2)


def step(phi, m, sc, sv, dual, rng, freeze_noise=False):
    m = (1 - ALPHA) * m + ALPHA * phi
    g = grad(phi)
    new = (g > THETA) & ~sc
    sc = sc | new
    sv = np.where(new, phi, sv)
    noise = 0 if freeze_noise else ETA * rng.normal(size=phi.shape) * phi
    phi = np.clip(phi + DT * (-(phi ** 3 - phi) + D * lap(phi) + LAM * (dual - phi) + m + MU * sc * (sv - phi) + noise), -3, 3)
    return phi, m, sc, sv


for seed in (1, 2, 3):
    rng = np.random.default_rng(seed)
    phi = 0.01 * rng.normal(size=(N, N)); dual = phi.copy()
    m = np.zeros_like(phi); sc = np.zeros_like(phi, bool); sv = np.zeros_like(phi)
    for _ in range(3000):
        phi, m, sc, sv = step(phi, m, sc, sv, dual, rng)
    idx = np.argwhere(sc)
    kill = idx[rng.choice(len(idx), int(0.3 * len(idx)), replace=False)]
    removed = np.zeros_like(sc); removed[kill[:, 0], kill[:, 1]] = True
    # how many removed sites still exceed the threshold in the (untouched) field right now?
    still_above = (grad(phi) > THETA) & removed
    sc2 = sc & ~removed
    phi2, m2, sc2b, sv2 = step(phi, m, sc2, sv, dual, rng)
    back1 = (sc2b & removed).sum() / removed.sum()
    extra1 = (sc2b & ~sc).sum()
    for _ in range(49):
        phi2, m2, sc2b, sv2 = step(phi2, m2, sc2b, sv2, dual, rng)
    back50 = (sc2b & removed).sum() / removed.sum()
    extra50 = (sc2b & ~sc).sum()
    print(f"seed {seed}: scars={sc.sum()} removed={removed.sum()}; removed sites whose |grad phi|>theta "
          f"at damage time={still_above.sum()/removed.sum():.1%}; re-scarred after 1 step={back1:.1%}, "
          f"after 50 steps={back50:.1%}; brand-new scar sites after 1/50 steps={extra1}/{extra50}")
    # 'position accuracy' as the papers compute it: regenerated scars matching an original position
    regen = sc2b & ~sc2
    print(f"          regenerated scars at original coordinates: {(regen & sc).sum()}/{regen.sum()} = {(regen & sc).sum()/max(1,regen.sum()):.1%}")
