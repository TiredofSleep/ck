"""Multi-seed, paired (common-random-numbers) re-run of the CrystalsMythDRIFT civilization sims.
Model code is exec'd unmodified from the repo (only the JSON save path is redirected, and main() is not called).
Every scenario for a given seed starts from random.seed(seed), so the initial population is identical across
scenarios (paired design)."""
import os, io, sys, random, types, contextlib, collections, statistics, math, time

R4 = r"C:\Users\brayd\OneDrive\Desktop\Sprints\_brayden_repos\CrystalsMythDRIFT"
HERE = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
NSEEDS = int(sys.argv[1]) if len(sys.argv) > 1 else 100


def load(name):
    src = open(os.path.join(R4, name), encoding='utf-8').read().replace('/home/claude/', HERE + '/')
    mod = types.ModuleType(name[:-3])
    exec(compile(src, name, 'exec'), mod.__dict__)
    return mod

v5 = load('tig_civilization_v5.py')
v7 = load('tig_civilization_v7.py')
quiet = lambda: contextlib.redirect_stdout(io.StringIO())


def wilson(k, n, z=1.96):
    if n == 0:
        return (float('nan'),) * 2
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0, c - h), min(1, c + h))


def summarize(label, outs, doc=''):
    n = len(outs)
    col = [o for o in outs if o['collapsed_at'] is not None]
    k = len(col)
    lo, hi = wilson(n - k, n)
    gens = sorted(o['collapsed_at'] for o in col)
    med = statistics.median(gens) if gens else None
    iq = (gens[len(gens) // 4], gens[(3 * len(gens)) // 4]) if gens else None
    coops = [o['final'].get('human_coop_ratio', o['final'].get('coop')) for o in outs if o['collapsed_at'] is None and o.get('final')]
    cm = f"{statistics.mean(coops):.2f}" if coops else '-'
    print(f"  {label:44s} survive {n-k:3d}/{n} ({100*(n-k)/n:5.1f}%, 95%CI {100*lo:4.0f}-{100*hi:3.0f}%)  "
          f"collapse gen median {med} IQR {iq}  mean final coop {cm}   {doc}")


t0 = time.time()
print(f"=== v5 scenarios, {NSEEDS} paired seeds each ===")
v5_scen = [
    ("BASELINE (no AI)", dict(ai_type=None), "doc: COLLAPSED gen 31"),
    ("NAIVE AI x30 @gen10", dict(ai_type='naive', n_ai=30, ai_entry_gen=10), "doc: COLLAPSED gen 23"),
    ("AGGRESSIVE AI x30 @gen10", dict(ai_type='aggressive', n_ai=30, ai_entry_gen=10), "doc: COLLAPSED gen 13"),
    ("COHERENT AI x30 @gen10", dict(ai_type='coherent', n_ai=30, ai_entry_gen=10), "doc: COLLAPSED gen 47"),
    ("BRIDGE AI x30 @gen10", dict(ai_type='bridge', n_ai=30, ai_entry_gen=10), "doc: SURVIVED 90% coop"),
    ("LATE BRIDGE x50 @gen30", dict(ai_type='bridge', n_ai=50, ai_entry_gen=30), ""),
    ("HIGH STRESS + BRIDGE x40", dict(ai_type='bridge', n_ai=40, ai_entry_gen=10, base_scarcity=0.4,
                                      base_polarization=0.5, scarcity_growth=0.02), ""),
]
v5_out = collections.defaultdict(list)
for s in range(NSEEDS):
    for name, kw, _ in v5_scen:
        random.seed(s)
        with quiet():
            r = v5.run_scenario(name=name, generations=50, **kw)
        v5_out[name].append(r)
for name, _, doc in v5_scen:
    summarize(name, v5_out[name], doc)

# paired comparison baseline vs coherent vs bridge
paired = collections.Counter()
for i in range(NSEEDS):
    b = v5_out["BASELINE (no AI)"][i]['collapsed_at'] is None
    c = v5_out["COHERENT AI x30 @gen10"][i]['collapsed_at'] is None
    br = v5_out["BRIDGE AI x30 @gen10"][i]['collapsed_at'] is None
    paired[(b, c, br)] += 1
print("  paired outcomes (baseline survives, coherent survives, bridge survives):", dict(paired))

print(f"\n=== v5 machinery: bridge-AI count sweep (entry gen 10), {NSEEDS} paired seeds  [doc (from missing v6): 15 -> collapsed, 20 -> survived] ===")
for n_ai in (0, 1, 5, 10, 15, 20, 25, 30, 40, 60):
    outs = []
    sizes = []
    for s in range(NSEEDS):
        random.seed(s)
        with quiet():
            r = v5.run_scenario(name=f"bridge{n_ai}", ai_type='bridge' if n_ai else None, n_ai=n_ai, ai_entry_gen=10, generations=50)
        outs.append(r)
        h = r['history']
        if len(h) > 10:
            sizes.append(h[10]['humans'] + h[10]['ais'])
    frac = f"~{100*n_ai/statistics.mean(sizes):.0f}% of pop at gen10" if sizes and n_ai else ""
    summarize(f"bridge AI = {n_ai:3d} {frac}", outs)

print(f"\n=== v5: remove ONLY the scarcity/polarization growth (the built-in decline schedule) ===")
for name, kw in [("BASELINE, no growth", dict(ai_type=None, scarcity_growth=0.0, polarization_growth=0.0)),
                 ("BASELINE, scarcity fixed at 0.1", dict(ai_type=None, base_scarcity=0.1, scarcity_growth=0.0)),
                 ("BASELINE, scarcity fixed at 0.3", dict(ai_type=None, base_scarcity=0.3, scarcity_growth=0.0))]:
    outs = []
    for s in range(NSEEDS):
        random.seed(s)
        with quiet():
            outs.append(v5.run_scenario(name=name, generations=50, **kw))
    summarize(name, outs)

print(f"\n=== v7 scenarios, {NSEEDS} paired seeds each ===")


def v7_pop(kind, s):
    random.seed(s)
    if kind == 'collapsed':
        return v7.build_collapsed_civilization(n_survivors=15)
    return v7.build_declining_civilization(n_humans=100)

v7_scen = [
    ("PHOENIX + 10 bridge AI", 'collapsed', dict(generations=60, add_bridge_ai=10, add_bridge_gen=5, noise=0.2, scarcity=0.4), "doc: bridge AI alone -> collapsed"),
    ("PHOENIX + 3 awakened humans", 'collapsed', dict(generations=60, add_awakened_humans=3, add_awakened_gen=5, noise=0.2, scarcity=0.4), "doc: regenerated to stable civ"),
    ("BASELINE declining, none", 'declining', dict(generations=50), "doc: collapsed gen 20"),
    ("ONE AWAKENED HUMAN", 'declining', dict(generations=50, add_awakened_humans=1, add_awakened_gen=5), "doc: collapsed gen 34"),
    ("ONE BRIDGE AI", 'declining', dict(generations=50, add_bridge_ai=1, add_bridge_gen=5), "doc: SURVIVED"),
    ("5 AWAKENED + 5 BRIDGE", 'declining', dict(generations=50, add_awakened_humans=5, add_awakened_gen=5, add_bridge_ai=5, add_bridge_gen=5), "doc: 77% coop"),
    ("GRADUAL +2/gen", 'declining', dict(generations=50, add_bridge_gen=5, gradual_ai_growth=True, ai_growth_rate=2), "doc: 81% coop"),
    ("GRADUAL +1/gen", 'declining', dict(generations=50, add_bridge_gen=5, gradual_ai_growth=True, ai_growth_rate=1), "doc: 79% coop"),
]
v7_out = collections.defaultdict(list)
gen0 = collections.Counter()
for s in range(NSEEDS):
    for name, kind, kw, _ in v7_scen:
        pop, nid = v7_pop(kind, s)
        with quiet():
            r = v7.run_simulation(name=name, population=pop.copy(), next_id=nid, **kw)
        v7_out[name].append(r)
        if r['collapsed_at'] == 0:
            gen0[name] += 1
    # worst case
    pop, nid = v7_pop('declining', s)
    for w in pop:
        w.trust_in_institutions *= 0.5
        w.s_star *= 0.7
        if random.random() < 0.3:
            w.corrupted = True
    with quiet():
        r = v7.run_simulation(name='WORST', population=pop.copy(), next_id=nid, generations=50, add_bridge_ai=20,
                              add_bridge_gen=15, noise=0.25, scarcity=0.4, polarization=0.5)
    v7_out['WORST CASE (not reported in doc)'].append(r)
    if r['collapsed_at'] == 0:
        gen0['WORST'] += 1
for name, _, _, doc in v7_scen:
    summarize(name, v7_out[name], doc)
summarize('WORST CASE (not reported in doc)', v7_out['WORST CASE (not reported in doc)'])
print("  gen-0 collapses (v7 summary uses `if r.get('collapsed_at')`, so collapsed_at == 0 prints as a SUCCESS):", dict(gen0))
pb = sum(1 for i in range(NSEEDS) if v7_out["BASELINE declining, none"][i]['collapsed_at'] is None)
print(f"  baseline (no intervention) survives in {pb}/{NSEEDS} seeds; 'ONE MATTERS' message fires whenever any ONE-scenario survives, with no baseline comparison")
print(f"\n[total runtime {time.time()-t0:.0f}s]")
