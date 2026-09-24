# Pure computation. Reproduces repo-5 D* (the "self-reference constant" 0.543) and shows it is a
# readout of a fixed map on 27 codes (functional graph), then runs the SPECIFIC gate with random letter maps.
import re, os, itertools, random, collections
B, D, C = 0, 1, 2
CODE = {B: 'B', D: 'D', C: 'C'}
LETTERS = {
    'A':(D,D,B), 'B':(B,C,C), 'C':(C,B,D), 'D':(B,C,B), 'E':(B,D,B), 'F':(B,D,B), 'G':(C,B,D), 'H':(B,D,B),
    'I':(B,B,B), 'J':(B,B,C), 'K':(B,D,D), 'L':(B,D,B), 'M':(B,D,B), 'N':(B,D,B), 'O':(C,C,C), 'P':(B,C,B),
    'Q':(C,C,D), 'R':(B,C,D), 'S':(C,D,C), 'T':(D,B,B), 'U':(C,B,B), 'V':(D,D,B), 'W':(D,C,D), 'X':(D,D,D),
    'Y':(D,D,C), 'Z':(D,B,D)}
def to_tig(t):
    d, s, r = t
    if d == B:
        if s == B: return 0 if r == B else (1 if r == D else 5)
        if s == D: return 1 if r == B else (3 if r == D else 5)
        if s == C: return 5 if r == B else (1 if r == D else 8)
    elif d == D:
        if s == B: return 4 if r == B else (2 if r == D else 3)
        if s == D: return 4 if r == B else (6 if r == D else 3)
        if s == C: return 9 if r == B else (2 if r == D else 7)
    else:
        if s == B: return 9 if r == B else (3 if r == D else 8)
        if s == D: return 9 if r == B else (4 if r == D else 7)
        if s == C: return 8 if r == B else (7 if r == D else 7)
TIG_OPS = {0:"void",1:"lattice",2:"counter",3:"progress",4:"collapse",5:"balance",6:"chaos",7:"harmony",8:"breath",9:"reset"}

def word_triple(w, L):
    t = (0, 0, 0)
    for ch in w.upper():
        if ch in L:
            x = L[ch]; t = ((t[0]+x[0]) % 3, (t[1]+x[1]) % 3, (t[2]+x[2]) % 3)
    return t
def sym(t): return ''.join(CODE[x] for x in t)
def gap(codes, L):
    cnt = collections.Counter(p for w in codes for ch in w for p in L[ch])
    tot = sum(cnt.values()); return 1 - max(cnt.values()) / tot

# 1) The SYM map f on the 27 codes and its cycles
codes27 = [''.join(p) for p in itertools.product('BDC', repeat=3)]
f = {w: sym(word_triple(w, LETTERS)) for w in codes27}
def cycles(fmap):
    seen, cyc = set(), []
    for x in fmap:
        path = []; y = x
        while y not in path and y not in seen:
            path.append(y); y = fmap[y]
        if y in path:
            c = path[path.index(y):]; cyc.append(c)
        seen.update(path)
    return cyc
cy = cycles(f)
print("SYM map on 27 codes: cycles =", cy)
for c in cy:
    print(f"   cycle {c}: gap of a text made only of this cycle = {gap(c, LETTERS):.4f}")

# 2) Reproduce D* on the repo texts
R5 = r"C:/Users/brayd/OneDrive/Desktop/Sprints/_brayden_repos/TIME-FOR-HELP-AND-SCRUTINY-please-No-more-AI-MYTHDRIFT"
names = ["CRYSTAL_BUG.py","ollie_semantics.py","README.md","TIG_SCIENTIFIC_FRAMEWORK.md","TIG_OPERATORS_COMPLETE.md",
         "VALIDATION_REPORT.md","CELESTE_LETTER.md","PRESS_BRIEF.md","LICENSE.md"]
def chain(text, L, passes=12):
    out = []
    for _ in range(passes):
        words = re.findall(r'[A-Za-z]+', text)
        sc = [sym(word_triple(w, L)) for w in words]
        out.append(gap(sc, L)); text = ' '.join(sc)
    return out
vals = []
for n in names:
    with open(os.path.join(R5, n), encoding='utf-8', errors='replace') as fh:
        g = chain(fh.read(), LETTERS)
    vals.append(g[-1]); print(f"   {n:32s} gap by pass: " + ' '.join(f'{x:.4f}' for x in g[:6]) + f" ... final {g[-1]:.4f}")
print(f"   mean final gap (D*) = {sum(vals)/len(vals):.5f}; spread {max(vals)-min(vals):.4f}")
# random-word text (no English at all)
R = random.Random(0)
junk = ' '.join(''.join(R.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(R.randint(1, 9))) for _ in range(3000))
print(f"   random gibberish text final gap = {chain(junk, LETTERS)[-1]:.4f}")

# 3) OP chain: word -> operator name -> ... is a map on 10 names
g = {nm: TIG_OPS[to_tig(word_triple(nm, LETTERS))] for nm in TIG_OPS.values()}
print("OP map on 10 operator names:", g)
print("   cycles:", cycles(g))

# 4) SPECIFIC gate: random letter->triple maps. How many give a SYM fixed-point-only map? what gaps?
fixed_only = 0; gaps = []
for k in range(2000):
    RL = {ch: (R.randrange(3), R.randrange(3), R.randrange(3)) for ch in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'}
    fk = {w: sym(word_triple(w, RL)) for w in codes27}
    cyk = cycles(fk)
    if all(len(c) == 1 for c in cyk): fixed_only += 1
    t = chain(junk, RL, passes=10); gaps.append(t[-1])
gaps.sort()
print(f"Random letter maps (2000): SYM map has only fixed points (no longer cycles) in {fixed_only/20:.1f}% of maps;"
      f" final gap quantiles 5/50/95% = {gaps[100]:.3f}/{gaps[1000]:.3f}/{gaps[1900]:.3f}")
