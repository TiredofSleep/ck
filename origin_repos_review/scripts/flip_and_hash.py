# Pure computation (sympy + stdlib).
# (1) The TIG master equation as a map: f(x) = s*(1-x). Fixed point, multiplier, 2-cycles.
# (2) The tri-prime word hash: order blindness vs a position-weighted checksum.
import sympy as sp, itertools, random
x, s = sp.symbols('x s', real=True)
f = s * (1 - x)
fp = sp.solve(sp.Eq(f, x), x)
print("fixed point of x -> s(1-x):", fp, "  multiplier f'(x*) =", sp.diff(f, x))
print("  at s=0.991: x* =", sp.nsimplify(0.991) / (1 + sp.nsimplify(0.991)), "=", float(0.991 / 1.991))
ff = sp.expand(f.subs(x, f))
print("f(f(x)) =", ff, "  -> at s=1:", sp.simplify(ff.subs(s, 1)), "(involution: every x is on a 2-cycle {x,1-x}; only x=1/2 is fixed)")
for sv in (0.5, 0.991, 1.0, 1.2):
    xs = [0.9]
    for _ in range(6):
        xs.append(sv * (1 - xs[-1]))
    print(f"  s={sv}: orbit from 0.9 -> " + ", ".join(f"{v:.3f}" for v in xs) + f"   (edge x*={sv/(1+sv):.4f})")

# (2) tri-prime hash is a homomorphism from words to (Z3)^3: blind to order
B, D, C = 0, 1, 2
L = {'A':(D,D,B),'B':(B,C,C),'C':(C,B,D),'D':(B,C,B),'E':(B,D,B),'F':(B,D,B),'G':(C,B,D),'H':(B,D,B),'I':(B,B,B),
     'J':(B,B,C),'K':(B,D,D),'L':(B,D,B),'M':(B,D,B),'N':(B,D,B),'O':(C,C,C),'P':(B,C,B),'Q':(C,C,D),'R':(B,C,D),
     'S':(C,D,C),'T':(D,B,B),'U':(C,B,B),'V':(D,D,B),'W':(D,C,D),'X':(D,D,D),'Y':(D,D,C),'Z':(D,B,D)}
def h(w):
    t = (0, 0, 0)
    for ch in w: t = tuple((t[i] + L[ch][i]) % 3 for i in range(3))
    return t
def weighted(w):   # position-weighted checksum mod 29 (prime > 26): detects every adjacent transposition of distinct letters
    return sum((i + 1) * (ord(ch) - 64) for i, ch in enumerate(w)) % 29
R = random.Random(3)
words = [''.join(R.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(R.randint(3, 9))) for _ in range(5000)]
tri_miss = w_miss = subs_tri = n = 0
for w in words:
    i = R.randrange(len(w) - 1)
    if w[i] == w[i+1]: continue
    t = w[:i] + w[i+1] + w[i] + w[i+2:]; n += 1
    tri_miss += h(w) == h(t); w_miss += weighted(w) == weighted(t)
sub_n = 0
for w in words:
    i = R.randrange(len(w)); c = R.choice([ch for ch in L if ch != w[i]])
    t = w[:i] + c + w[i+1:]; sub_n += 1; subs_tri += h(w) == h(t)
print(f"\nadjacent transpositions: tri-prime hash misses {tri_miss}/{n} ({100*tri_miss/n:.0f}%), weighted mod-29 misses {w_miss}/{n}")
print(f"single-letter substitutions: tri-prime hash misses {subs_tri}/{sub_n} ({100*subs_tri/sub_n:.0f}%)  (e.g. E,F,H,L,M,N share one triple)")
print("LOVE vs VOLE:", h('LOVE'), h('VOLE'), "| distinct letter triples:", len(set(L.values())), "of 27")
