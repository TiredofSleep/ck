# Pure computation. Tests whether the quadratic-return-map classifier (tig_engine_real.Op/Fitter,
# the surviving implementation of the README's coherence_router pipeline) is SPECIFIC:
# does it separate deterministic dynamics from noise and from shuffled surrogates?
import math, random, collections, sys
sys.dont_write_bytecode = True
from tig_engine_real import Fitter, Op, Router, Sensor

def norm01(s):
    lo, hi = min(s), max(s)
    r = (hi - lo) or 1.0
    return [(v - lo) / r for v in s]

def logistic(r, n, x0=0.3, noise=0.0, rng=None):
    s = [x0]
    for _ in range(n - 1):
        x = r * s[-1] * (1 - s[-1])
        if noise and rng:
            x = min(1.0, max(0.0, x + rng.gauss(0, noise)))
        s.append(x)
    return s

def classify(series):
    op = Fitter.fit(series)
    return op.band_name, op

GENS = {
    'uniform_noise':   lambda n, R: [R.random() for _ in range(n)],
    'gauss_noise_0.5': lambda n, R: [0.5 + 0.1 * R.gauss(0, 1) for _ in range(n)],
    'random_walk':     lambda n, R: norm01(list(__import__('itertools').accumulate(R.gauss(0, 1) for _ in range(n)))),
    'AR1_phi0.9':      None,
    'sine_p21':        lambda n, R: [0.5 + 0.3 * math.sin(2 * math.pi * i / 21 + R.random() * 6.28) for i in range(n)],
    'sine_p21+noise':  lambda n, R: [0.5 + 0.3 * math.sin(2 * math.pi * i / 21) + 0.05 * R.gauss(0, 1) for i in range(n)],
    'logistic_3.2':    lambda n, R: logistic(3.2, n, x0=0.1 + 0.8 * R.random()),
    'logistic_3.5':    lambda n, R: logistic(3.5, n, x0=0.1 + 0.8 * R.random()),
    'logistic_3.8':    lambda n, R: logistic(3.8, n, x0=0.1 + 0.8 * R.random()),
    'logistic_4.0':    lambda n, R: logistic(4.0, n, x0=0.1 + 0.8 * R.random()),
    'logistic_3.8+noise0.02': lambda n, R: logistic(3.8, n, x0=0.1 + 0.8 * R.random(), noise=0.02, rng=R),
    'logistic_3.8_SHUFFLED': lambda n, R: R.sample(logistic(3.8, n, x0=0.1 + 0.8 * R.random()), n),
}
def ar1(n, R, phi=0.9):
    s = [0.0]
    for _ in range(n - 1):
        s.append(phi * s[-1] + R.gauss(0, 1))
    return norm01(s)
GENS['AR1_phi0.9'] = ar1

for n in (50, 200):
    print(f"\n=== window length n={n}, 200 random seeds per generator; band counts ===")
    for name, g in GENS.items():
        cnt = collections.Counter()
        for seed in range(200):
            R = random.Random(seed * 7919 + n)
            s = g(n, R)
            b, op = classify(s)
            cnt[b] += 1
        print(f"  {name:26s} " + ", ".join(f"{k}:{v}" for k, v in cnt.most_common()))

# Router behaviour: is it just 'pick least-loaded'?
print("\n=== Router.route agreement with 'least recent load' (join-least-loaded) ===")
agree = total = 0
R = random.Random(1)
for trial in range(300):
    rt = Router()
    loads = {}
    for name in ('n1', 'n2', 'n3', 'n4'):
        kind = R.choice(['uniform_noise', 'AR1_phi0.9', 'sine_p21', 'logistic_3.8'])
        s = GENS[kind](40, R)
        for v in s:
            rt.update(name, v)
        loads[name] = s[-1]
    pick = rt.route()
    least = min(loads, key=loads.get)
    agree += (pick == least); total += 1
print(f"  TIG router picked the least-loaded node in {agree}/{total} trials")
