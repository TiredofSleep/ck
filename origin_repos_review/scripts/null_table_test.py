# Pure computation (numpy). SPECIFIC-gate test of tig_coherent_computer.py's "proven configuration":
# majority vote of compositions over Moore neighbourhood (+ self), V* = neighbour diversity,
# A* = fraction of cells in states 4..8, S* = 3/(1/sigma + 1/V* + 1/A*), threshold T* = 0.714.
# Question: do RANDOM 10x10 tables also reach T* from random initial states?
import numpy as np
SIGMA, T_STAR = 0.991, 0.714
ROWS, COLS, TICKS = 14, 12, 100
TIG = np.array([
    [0,1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,2,6,6],[2,3,3,4,5,6,7,3,6,6],[3,4,4,4,5,6,7,4,6,6],
    [4,5,5,5,5,6,7,5,7,7],[5,6,6,6,6,6,7,6,7,7],[6,7,7,7,7,7,7,7,7,7],[7,2,3,4,5,6,7,8,9,0],
    [8,6,6,6,7,7,7,9,7,8],[9,6,6,6,7,7,7,0,8,0]], dtype=np.int64)
SHIFTS = [(di, dj) for di in (-1, 0, 1) for dj in (-1, 0, 1) if (di, dj) != (0, 0)]

def neighbours(S):
    return [np.roll(np.roll(S, -di, axis=0), -dj, axis=1) for di, dj in SHIFTS]

def tick(S, T):
    comps = [T[S, N] for N in neighbours(S)] + [T[S, S]]
    counts = np.zeros(S.shape + (10,), dtype=np.int64)
    for c in comps:
        np.add.at(counts, (np.arange(S.shape[0])[:, None], np.arange(S.shape[1])[None, :], c), 1)
    return counts.argmax(axis=2)          # ties -> lowest state, as np.argmax(bincount) in the original

def score(S, T):
    nb = neighbours(S)
    diverse = np.zeros(S.shape, dtype=bool)
    for N in nb:
        diverse |= (T[S, N] != S)
    diverse |= (S == 7)
    v = diverse.mean(); a = np.isin(S, [4, 5, 6, 7, 8]).mean()
    if v < 1e-10 or a < 1e-10: return 0.0, v, a
    return 3.0 / (1 / SIGMA + 1 / v + 1 / a), v, a

def run(T, rng, starts=40):
    reached = 0; finals = []
    for _ in range(starts):
        S = rng.integers(0, 10, size=(ROWS, COLS))
        for _ in range(TICKS):
            S = tick(S, T)
        s, v, a = score(S, T)
        finals.append(s); reached += (s >= T_STAR)
    return reached / starts, float(np.mean(finals))

rng = np.random.default_rng(12345)
frac, mean_s = run(TIG, rng)
print(f"TIG table:            reached T* in {frac*100:.0f}% of random starts, mean final S* = {mean_s:.4f}")

fr = []; ms = []
for k in range(150):
    T = rng.integers(0, 10, size=(10, 10))
    f, m = run(T, rng, starts=20)
    fr.append(f); ms.append(m)
fr = np.array(fr); ms = np.array(ms)
print(f"150 uniform random tables: fraction of tables with >=95% starts reaching T*: {(fr>=0.95).mean()*100:.0f}%;"
      f" median reach rate {np.median(fr)*100:.0f}%; mean final S* {ms.mean():.4f} (min {ms.min():.3f}, max {ms.max():.3f})")

# random tables that keep TIG's 'row 0 = identity' property (VOID as left identity)
fr2 = []
for k in range(150):
    T = rng.integers(0, 10, size=(10, 10)); T[0] = np.arange(10)
    f, _ = run(T, rng, starts=20); fr2.append(f)
fr2 = np.array(fr2)
print(f"150 random tables with row0=identity: >=95% reach in {(fr2>=0.95).mean()*100:.0f}% of tables; median reach {np.median(fr2)*100:.0f}%")

# What does a lattice frozen in a single state score?  (all cells = 7)
for st in (5, 6, 7, 8):
    S = np.full((ROWS, COLS), st)
    print(f"  all cells = {st}: S* = {score(S, TIG)[0]:.4f}  (V*={score(S, TIG)[1]:.2f}, A*={score(S, TIG)[2]:.2f})")
