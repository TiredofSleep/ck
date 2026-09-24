import importlib.util, random
P = r"C:\Users\brayd\OneDrive\Desktop\Sprints\_brayden_repos\Dual-Lattice-Self-Healing\TIGCodexEngine.py"
spec = importlib.util.spec_from_file_location("tigcodex", P); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
ORIG = [r[:] for r in m.COMP]
def rate(T, seeds=10):
    m.COMP[:] = T
    ok = 0
    for s in range(seeds):
        L = m.Lattice(14, 12, seed=s)
        if L.tick() >= m.T_STAR: ok += 1
    return ok / seeds
rng = random.Random(11)
flat = [x for r in ORIG for x in r]
res = {"uniform": [], "shuffled-entries": [], "symmetric-shuffled": []}
for k in range(200):
    U = [[rng.randint(0, 9) for _ in range(10)] for _ in range(10)]
    res["uniform"].append(rate(U))
    f = flat[:]; rng.shuffle(f); S = [f[i*10:(i+1)*10] for i in range(10)]
    res["shuffled-entries"].append(rate(S))
    # symmetric table with same upper-triangle multiset
    ut = [ORIG[i][j] for i in range(10) for j in range(i, 10)]; rng.shuffle(ut)
    T = [[0]*10 for _ in range(10)]; it = iter(ut)
    for i in range(10):
        for j in range(i, 10):
            v = next(it); T[i][j] = v; T[j][i] = v
    res["symmetric-shuffled"].append(rate(T))
for k, v in res.items():
    allc = sum(1 for x in v if x == 1.0) / len(v)
    mean = sum(v) / len(v)
    anyc = sum(1 for x in v if x > 0) / len(v)
    print(f"{k:20s} tables converging on all 10 seeds: {allc:.1%}; mean per-seed rate {mean:.1%}; any seed {anyc:.1%}")
m.COMP[:] = ORIG
print("committed table per-seed rate:", rate(ORIG, 50))
