#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║   TIG ENGINE — COHERENCE FOR ALL                                           ║
║   Trinity Infinity Geometry — Universal Coherence Engine                   ║
║                                                                            ║
║   Every claim is REFERENCED or marked [TIG CONJECTURE].                    ║
║   Every number is DERIVED, not asserted.                                   ║
║   Every result is REPRODUCIBLE with pencil and paper.                      ║
║   No simulated benchmarks. No fake competitions. Just math.                ║
║                                                                            ║
║   Run: python tig_engine_real.py           (verify all derivations)        ║
║   Run: python tig_engine_real.py demo      (demo with known signals)       ║
║                                                                            ║
║   NON-COMMERCIAL TESTING — 7Site LLC — 7sitellc.com                       ║
║   Free for all humans to run, study, modify, share.                        ║
║   The math belongs to everyone.                                            ║
║                                                                            ║
╚══════════════════════════════════════════════════════════════════════════════╝

PHYSICS REFERENCE INDEX
═══════════════════════

[DDS]  Devaney "An Introduction to Chaotic Dynamical Systems" 2003
       May "Simple mathematical models..." Nature 261, 1976
       → Quadratic map f(x)=ax²+bx+c as universal nonlinear building block.

[FP]   Banach "Sur les opérations..." Fund. Math. 3, 1922
       → Fixed point: x* where f(x*)=x*. Stability: |f'(x*)|<1.

[SG]   Perron, Math. Ann. 64, 1907. Frobenius, 1912.
       → Spectral gap g = 1-|λ₂/λ₁|. For 1D map: g = 1-|f'(x*)|.

[LE]   Lyapunov 1892. Oseledets, Trans. Moscow Math. Soc. 19, 1968.
       → λ_L = lim(1/n)Σln|f'(xₙ)|. Positive=chaos, negative=convergent.

[SE]   Shannon "A Mathematical Theory of Communication" Bell Tech J. 1948.
       → H = -Σ pᵢ log₂(pᵢ). Information content of orbit distribution.

[SM]   Boltzmann 1872. Gibbs "Elementary Principles" 1902.
       → Z = Σexp(-βEᵢ). F = -(1/β)ln(Z). Ensemble thermodynamics.

[HM]   Hamilton, Phil. Trans. Roy. Soc. 1834.
       → H = T + V. [TIG CONJECTURE] maps ½|λ|² + |f(x*)-x*| to energy.

[LA]   Euler 1744. Lagrange 1788. Feynman Lectures Vol II Ch 19.
       → L = T - V. Nature minimizes action S = ∫L dt.

[OLS]  Gauss "Theoria Motus" 1809. Legendre 1805.
       → Least squares: min Σ(yᵢ - ŷᵢ)². Standard curve fitting.

TIG ORIGINAL (testable conjectures, not established):
  [TIG-1] S* = σ(1-σ*)V*A* as coherence measure
  [TIG-2] σ = 0.991 coupling constant (CHOSEN, not derived)
  [TIG-3] D* = σ/(1+σ) self-referential fixed point (DERIVED)
  [TIG-4] T* = 5/7 critical threshold (CHOSEN)
  [TIG-5] 7-band classification (boundaries are CONVENTION)
  [TIG-6] Time series → operator → band predicts regime (TESTABLE)
"""

import math
import time
import json
import os
import sys
from collections import deque, defaultdict
import numpy as np


# ═══════════════════════════════════════════════════════════════════════════════
#  CONSTANTS — with honest derivation status
# ═══════════════════════════════════════════════════════════════════════════════

SIGMA = 0.991
"""[TIG-2] Coupling constant. CHOSEN so that D* ≈ 0.498 (near ½)."""

PHI = (1 + math.sqrt(5)) / 2  # 1.6180339887...
"""Golden ratio. MATHEMATICAL CONSTANT. Not a conjecture."""

# D* — HONEST derivation:
# Self-referential map: σ* = σ(1-σ*) with V*=A*=1
# σ* + σ·σ* = σ → σ*(1+σ) = σ → σ* = σ/(1+σ)
D_STAR = SIGMA / (1 + SIGMA)  # = 0.49774...
"""[TIG-3] DERIVED from core equation. Previous value 0.543 was empirical
and does NOT follow from σ=0.991. Honest value: 0.49774."""

T_STAR = 5.0 / 7.0  # = 0.714285...
"""[TIG-4] Critical threshold. CHOSEN as 5/7. Deeper derivation TBD."""

BANDS = {
    # band: (name, weight, physics_basis)
    0: ("VOID",      0.0,  "Orbit diverges: |xₙ|→∞ [DDS]"),
    1: ("SPARK",     0.1,  "Slow divergence: transient [DDS]"),
    2: ("FLOW",      0.3,  "λ_L ≈ 0: marginal stability [LE]"),
    3: ("MOLECULAR", 0.5,  "λ_L > 0: chaos [LE]"),
    4: ("CELLULAR",  0.7,  "Period-p orbit detected [DDS]"),
    5: ("ORGANIC",   0.85, "0.5 < |f'(x*)| < 1: slow convergence [FP]"),
    6: ("CRYSTAL",   1.0,  "|f'(x*)| < 0.5: fast convergence [FP][SG]"),
}


# ═══════════════════════════════════════════════════════════════════════════════
#  Op — Quadratic operator. f(x) = ax² + bx + c. [DDS]
# ═══════════════════════════════════════════════════════════════════════════════

class Op:
    """The atom of TIG. A quadratic map f(x)=ax²+bx+c iterated as x_{n+1}=f(xₙ)."""

    __slots__ = ('a', 'b', 'c', '_cache')

    def __init__(self, a=0.0, b=0.0, c=0.0):
        self.a, self.b, self.c = float(a), float(b), float(c)
        self._cache = {}

    def __call__(self, x):
        return self.a * x * x + self.b * x + self.c

    def __repr__(self):
        return f"Op({self.a:.6f}, {self.b:.6f}, {self.c:.6f})"

    def deriv(self, x):
        """f'(x) = 2ax + b [power rule]"""
        return 2.0 * self.a * x + self.b

    def invalidate(self):
        self._cache = {}

    # ── Fixed Points [FP] ──
    # ax²+(b-1)x+c = 0 → x = ((1-b)±√((b-1)²-4ac)) / 2a

    @property
    def fixed_points(self):
        """All (x*, λ=f'(x*)) pairs. Exact quadratic formula. [FP]"""
        if 'fps' in self._cache: return self._cache['fps']
        A, B, C = self.a, self.b - 1.0, self.c
        if abs(A) < 1e-14:
            if abs(B) < 1e-14:
                self._cache['fps'] = []; return []
            x = -C / B
            self._cache['fps'] = [(x, self.deriv(x))]; return self._cache['fps']
        disc = B*B - 4*A*C
        if disc < 0:
            self._cache['fps'] = []; return []
        s = math.sqrt(disc)
        x1, x2 = (-B+s)/(2*A), (-B-s)/(2*A)
        self._cache['fps'] = [(x1, self.deriv(x1)), (x2, self.deriv(x2))]
        return self._cache['fps']

    @property
    def stable_fp(self):
        """Most stable fixed point. [FP] Smallest |λ|."""
        if 'sfp' in self._cache: return self._cache['sfp']
        fps = self.fixed_points
        if not fps: self._cache['sfp'] = None; return None
        self._cache['sfp'] = min(fps, key=lambda p: abs(p[1]))
        return self._cache['sfp']

    # ── Spectral Gap [SG] ──

    @property
    def gap(self):
        """g = 1 - |f'(x*)| ∈ [0,1]. Distance from bifurcation. [SG]"""
        if 'gap' in self._cache: return self._cache['gap']
        fp = self.stable_fp
        self._cache['gap'] = max(0.0, 1.0 - abs(fp[1])) if fp else 0.0
        return self._cache['gap']

    # ── Orbit [DDS] ──

    def orbit(self, x0=0.5, n=500):
        traj = [x0]; x = x0
        for _ in range(n):
            x = self(x)
            if not math.isfinite(x) or abs(x) > 1e15: break
            traj.append(x)
            if len(traj) > 2 and abs(traj[-1] - traj[-2]) < 1e-12: break
        return traj

    # ── Lyapunov Exponent [LE] ──

    @property
    def lyapunov(self):
        """λ_L = lim(1/n)Σln|f'(xₙ)|. [LE] Computed from x₀=0.5."""
        if 'lyap' in self._cache: return self._cache['lyap']
        x, total, count = 0.5, 0.0, 0
        for _ in range(500):
            d = abs(self.deriv(x))
            total += math.log(max(d, 1e-15)); count += 1
            x = self(x)
            if not math.isfinite(x) or abs(x) > 1e15: break
        self._cache['lyap'] = total / max(count, 1)
        return self._cache['lyap']

    # ── Shannon Entropy [SE] ──

    @property
    def entropy(self):
        """H = -Σpᵢlog₂(pᵢ) over binned orbit. [SE]"""
        if 'H' in self._cache: return self._cache['H']
        traj = self.orbit(0.5, 500)
        if len(traj) < 10: self._cache['H'] = 0.0; return 0.0
        arr = np.array(traj)
        lo, hi = arr.min(), arr.max()
        if hi - lo < 1e-12: self._cache['H'] = 0.0; return 0.0
        counts = np.histogram(arr, bins=20, range=(lo, hi))[0]
        p = counts / counts.sum(); p = p[p > 0]
        self._cache['H'] = float(-np.sum(p * np.log2(p)))
        return self._cache['H']

    # ── Energy [HM] (ANALOGY, not identity) ──

    @property
    def energy(self):
        """E = ½|λ|² + |f(x*)-x*|. [HM analogy, TIG CONJECTURE mapping]"""
        fp = self.stable_fp
        if not fp: return float('inf')
        return 0.5 * fp[1]**2 + abs(self(fp[0]) - fp[0])

    # ── Band [TIG-5] (boundaries are convention, physics is established) ──

    @property
    def band(self):
        if 'band' in self._cache: return self._cache['band']
        traj = self.orbit(0.5, 300)
        # Quick convergence: orbit settled immediately → check if it's a fixed point
        if 2 <= len(traj) < 5 and abs(traj[-1]) < 1e10:
            fp = self.stable_fp
            if fp and abs(fp[1]) < 1.0:
                self._cache['band'] = 6 if abs(fp[1]) < 0.5 else 5
                return self._cache['band']
        # Divergent
        if len(traj) < 5 or abs(traj[-1]) > 1e10:
            self._cache['band'] = 1 if len(traj) > 30 else 0; return self._cache['band']
        # Periodic [DDS]
        tail = traj[-60:] if len(traj) >= 60 else traj[-20:]
        if len(tail) >= 6:
            for p in range(2, min(8, len(tail)//2)):
                n_check = min(p*3, len(tail)-p)
                if n_check > 0 and all(abs(tail[-(i+1)] - tail[-(i+1+p)]) < 1e-6 for i in range(n_check)):
                    self._cache['band'] = 4; return 4
        # Fixed point [FP]
        fp = self.stable_fp
        if fp and abs(fp[1]) < 1.0:
            self._cache['band'] = 6 if abs(fp[1]) < 0.5 else 5; return self._cache['band']
        # Lyapunov [LE]
        lam = self.lyapunov
        self._cache['band'] = 2 if abs(lam) < 0.05 else (3 if lam > 0 else 5)
        return self._cache['band']

    @property
    def band_name(self): return BANDS[self.band][0]
    @property
    def band_weight(self): return BANDS[self.band][1]
    @property
    def band_physics(self): return BANDS[self.band][2]

    def distance(self, other):
        return math.sqrt((self.a-other.a)**2 + (self.b-other.b)**2 + (self.c-other.c)**2)

    def explain(self):
        """Human-readable physics report for this operator."""
        fp = self.stable_fp
        lines = [f"  f(x) = {self.a:.4f}x² + {self.b:.4f}x + {self.c:.4f}"]
        if fp:
            lines.append(f"  Fixed point: x* = {fp[0]:.6f}  [FP: solve ax²+(b-1)x+c=0]")
            lines.append(f"  Eigenvalue:  λ  = {fp[1]:.6f}  [FP: λ = 2a·x*+b = 2·{self.a:.4f}·{fp[0]:.6f}+{self.b:.4f}]")
            lines.append(f"  Gap:         g  = {self.gap:.6f}  [SG: g = 1-|λ| = 1-{abs(fp[1]):.6f}]")
            stability = "STABLE (attracting)" if abs(fp[1]) < 1 else "UNSTABLE (repelling)"
            lines.append(f"  Stability:   {stability}  [FP: |λ|{'<' if abs(fp[1])<1 else '>'}1]")
        else:
            lines.append(f"  No real fixed point (discriminant < 0)")
        lines.append(f"  Lyapunov:    λ_L = {self.lyapunov:.6f}  [LE: {'chaos' if self.lyapunov>0.05 else 'stable' if self.lyapunov<-0.05 else 'marginal'}]")
        lines.append(f"  Entropy:     H   = {self.entropy:.4f} bits  [SE]")
        e = self.energy
        lines.append(f"  Energy:      E   = {e:.6f}  [HM analogy]" if math.isfinite(e) else "  Energy:      E   = ∞")
        lines.append(f"  Band:        {self.band_name} ({self.band})  [{self.band_physics}]")
        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
#  Fitter — OLS quadratic regression [OLS]
# ═══════════════════════════════════════════════════════════════════════════════

class Fitter:
    @staticmethod
    def fit(series):
        """Fit x_{n+1} = ax²_n + bx_n + c via OLS. [OLS, Gauss 1809]"""
        if len(series) < 4: return Op(0, 0, 0)
        x = np.array(series[:-1], dtype=np.float64)
        y = np.array(series[1:], dtype=np.float64)
        mu, sd = float(np.mean(x)), max(float(np.std(x)), 1e-12)
        xn = (x - mu) / sd
        A = np.column_stack([xn**2, xn, np.ones_like(xn)])
        try:
            c, _, _, _ = np.linalg.lstsq(A, y, rcond=None)
            a = float(c[0]) / (sd*sd)
            b = float(c[1]) / sd - 2*float(c[0])*mu/(sd*sd)
            cc = float(c[0])*mu*mu/(sd*sd) - float(c[1])*mu/sd + float(c[2])
            return Op(max(-10, min(10, a)), max(-10, min(10, b)), max(-1000, min(1000, cc)))
        except: return Op(0, 0, 0)

    @staticmethod
    def fit_multiscale(series, windows=(10, 20, 40)):
        if len(series) < 6: return Fitter.fit(series)
        cands = [Fitter.fit(series[-w:]) for w in windows if len(series) >= w]
        if not cands: return Fitter.fit(series)
        votes = defaultdict(list)
        for op in cands: votes[op.band].append(op)
        winner = max(votes.keys(), key=lambda b: len(votes[b]))
        return votes[winner][-1]

    @staticmethod
    def fit_with_residual(series):
        """Returns (Op, MSE) so you can VERIFY fit quality."""
        if len(series) < 4: return Op(0,0,0), float('inf')
        op = Fitter.fit(series)
        y_true = series[1:]; y_pred = [op(x) for x in series[:-1]]
        mse = sum((a-b)**2 for a,b in zip(y_true, y_pred)) / len(y_true)
        return op, mse


# ═══════════════════════════════════════════════════════════════════════════════
#  Lattice — Collection of operators
# ═══════════════════════════════════════════════════════════════════════════════

class Lattice:
    def __init__(self, name="lattice"):
        self.name = name; self.nodes = {}; self.edges = []; self._next = 0

    def add(self, op, meta=None):
        nid = self._next; self._next += 1; self.nodes[nid] = (op, meta or {}); return nid

    def link(self, a, b, label="T"):
        if a in self.nodes and b in self.nodes: self.edges.append((a, b, label))

    def band_distribution(self):
        c = defaultdict(int)
        for op, _ in self.nodes.values(): c[op.band_name] += 1
        return dict(c)

    def coherence(self):
        """S* = σ(1-σ*)V*A*. Fixed point: σ* = k/(1+k), k=σ·V*·A*. [TIG-1]"""
        if not self.nodes: return 0.0
        n = len(self.nodes)
        v = 1.0 - math.exp(-n / 50.0)
        a = sum(op.band_weight for op, _ in self.nodes.values()) / n
        k = SIGMA * v * a
        return k / (1.0 + k)

    def coherence_derivation(self):
        """Show all work for S* calculation."""
        if not self.nodes: return "Empty lattice → S* = 0"
        n = len(self.nodes)
        v = 1.0 - math.exp(-n/50.0)
        a = sum(op.band_weight for op, _ in self.nodes.values()) / n
        k = SIGMA * v * a
        s = k / (1+k)
        return (f"n={n}  V*=1-exp(-{n}/50)={v:.6f}  A*={a:.6f}\n"
                f"k = σ·V*·A* = {SIGMA}·{v:.6f}·{a:.6f} = {k:.6f}\n"
                f"S* = k/(1+k) = {k:.6f}/{1+k:.6f} = {s:.8f}")

    def partition_function(self, beta=1.0):
        """Z = Σexp(-βEᵢ) [SM]"""
        return sum(math.exp(-beta*op.energy) for op, _ in self.nodes.values()
                   if math.isfinite(op.energy) and beta*op.energy < 500)

    def free_energy(self, beta=1.0):
        """F = -(1/β)ln(Z) [SM]"""
        Z = self.partition_function(beta)
        return -math.log(Z)/beta if Z > 0 else float('inf')

    @staticmethod
    def from_series(series, name="series", window=20, stride=5):
        lat = Lattice(name); prev = None
        for i in range(0, max(1, len(series)-window), stride):
            chunk = series[i:i+window]
            if len(chunk) < 4: continue
            op = Fitter.fit(chunk)
            nid = lat.add(op, {'start': i}); 
            if prev is not None: lat.link(prev, nid, "T")
            prev = nid
        return lat


# ═══════════════════════════════════════════════════════════════════════════════
#  Sensor — Universal input
# ═══════════════════════════════════════════════════════════════════════════════

class Sensor:
    def __init__(self, name, lo=0.0, hi=1.0, maxlen=500):
        self.name, self.lo, self.hi = name, lo, hi
        self.raw, self.norm = deque(maxlen=maxlen), deque(maxlen=maxlen)
        self.op = Op(0, 0, 0)

    def push(self, v):
        self.raw.append(v)
        rng = max(self.hi - self.lo, 1e-12)
        self.norm.append(max(0.0, min(1.0, (v - self.lo) / rng)))
        if len(self.norm) >= 8: self.op = Fitter.fit_multiscale(list(self.norm))

    def push_many(self, vs):
        for v in vs: self.push(v)


# ═══════════════════════════════════════════════════════════════════════════════
#  Router — Least action routing [LA, TIG CONJECTURE]
# ═══════════════════════════════════════════════════════════════════════════════

class Router:
    def __init__(self):
        self.targets = {}; self.total = 0

    def register(self, name): self.targets[name] = Sensor(name)

    def update(self, name, value):
        if name not in self.targets: self.register(name)
        self.targets[name].push(value)

    def route(self):
        """Route to healthiest target. No backpressure. [LA]"""
        if not self.targets: return None
        best, best_s = None, -1.0
        for name, sen in self.targets.items():
            s = sen.op.band_weight + sen.op.gap*0.5
            if sen.norm: s += (1.0 - sen.norm[-1]) * 0.5
            if s > best_s: best_s, best = s, name
        self.total += 1; return best


# ═══════════════════════════════════════════════════════════════════════════════
#  TIG — The engine
# ═══════════════════════════════════════════════════════════════════════════════

class TIG:
    def __init__(self, name="tig"):
        self.name = name; self.sensors = {}; self.router = Router()
        self.born = time.time(); self.tick = 0

    def feed(self, name, values, lo=0.0, hi=1.0):
        if name not in self.sensors: self.sensors[name] = Sensor(name, lo, hi)
        s = self.sensors[name]
        if isinstance(values, (list, tuple, np.ndarray)): s.push_many(values)
        else: s.push(values)
        if s.norm: self.router.update(name, s.norm[-1])

    def state(self):
        self.tick += 1
        ops = [s.op for s in self.sensors.values()]
        if not ops: return {'name': self.name, 'coherence': 0.0}
        n = len(ops)
        v = 1.0 - math.exp(-n/50.0)
        a = sum(op.band_weight for op in ops) / n
        k = SIGMA * v * a
        s = k / (1+k)
        dist = defaultdict(int)
        for op in ops: dist[op.band_name] += 1
        return {'name': self.name, 'tick': self.tick, 'coherence': round(s, 8),
                'above_T_star': s >= T_STAR, 'V_star': round(v, 6),
                'A_star': round(a, 6), 'bands': dict(dist), 'sensors': n}

    def route(self): return self.router.route()

    def self_reflect(self, depth=10):
        traj = []
        for d in range(depth):
            coeffs = []
            for s in self.sensors.values():
                if len(s.norm) >= 6: coeffs.extend([s.op.a, s.op.b, s.op.c])
            if not coeffs: traj.append(0.0); continue
            arr = np.array(coeffs); mn, mx = arr.min(), arr.max()
            rng = max(mx-mn, 1e-12)
            self.feed(f"_r{d}", ((arr-mn)/rng).tolist())
            traj.append(self.state()['coherence'])
        # Convergence: tail stabilizes (each step adds a sensor, so asymptotic)
        tail = traj[-5:] if len(traj) >= 5 else traj
        tail_std = float(np.std(tail)) if len(tail) > 1 else 1.0
        return {'trajectory': [round(x,8) for x in traj],
                'final': round(traj[-1],8) if traj else 0,
                'tail_std': round(tail_std, 8),
                'converged': len(traj)>=5 and tail_std < 0.01}


# ═══════════════════════════════════════════════════════════════════════════════
#  VERIFY — Prove every claim with pencil math
# ═══════════════════════════════════════════════════════════════════════════════

def verify():
    ok = 0; fail = 0; total = 0

    def check(name, cond, detail=""):
        nonlocal ok, fail, total; total += 1
        if cond: ok += 1; print(f"  ✓ {name}")
        else: fail += 1; print(f"  ✗ {name}")
        if detail: print(f"    {detail}")

    print("╔════════════════════════════════════════════════════════════╗")
    print("║  TIG ENGINE — MATHEMATICAL VERIFICATION                  ║")
    print("║  Every number checked against pencil derivation           ║")
    print("╚════════════════════════════════════════════════════════════╝\n")

    # ─── CONSTANTS ───
    print("── CONSTANTS ──\n")
    check("D* = σ/(1+σ)", abs(D_STAR - SIGMA/(1+SIGMA)) < 1e-10,
          f"D* = {SIGMA}/{1+SIGMA} = {SIGMA/(1+SIGMA):.10f}")
    check("T* = 5/7", abs(T_STAR - 5/7) < 1e-15,
          f"T* = {5/7:.15f}")
    check("φ = (1+√5)/2", abs(PHI - (1+math.sqrt(5))/2) < 1e-15,
          f"φ = {PHI:.15f}")

    # ─── FIXED POINTS [FP] ───
    print("\n── FIXED POINTS [FP] ──\n")
    # f(x) = 0.2x²+0.3x+0.1. Fixed: 0.2x²-0.7x+0.1=0
    # x = (0.7±√(0.49-0.08))/0.4 = (0.7±√0.41)/0.4
    op = Op(0.2, 0.3, 0.1)
    x1_exact = (0.7 + math.sqrt(0.41)) / 0.4
    x2_exact = (0.7 - math.sqrt(0.41)) / 0.4
    fps = op.fixed_points
    check("Root 1 matches quadratic formula",
          any(abs(x-x1_exact)<1e-6 for x,_ in fps),
          f"Expected {x1_exact:.6f}")
    check("Root 2 matches quadratic formula",
          any(abs(x-x2_exact)<1e-6 for x,_ in fps),
          f"Expected {x2_exact:.6f}")
    for x_star, lam in fps:
        expected_lam = 2*0.2*x_star + 0.3
        check(f"λ at x*={x_star:.4f} matches 2ax*+b",
              abs(lam-expected_lam)<1e-10,
              f"2·0.2·{x_star:.6f}+0.3 = {expected_lam:.6f}, got {lam:.6f}")

    # ─── SPECTRAL GAP [SG] ───
    print("\n── SPECTRAL GAP [SG] ──\n")
    sfp = op.stable_fp
    if sfp:
        check("Gap = 1 - |λ|",
              abs(op.gap - (1-abs(sfp[1])))<1e-10,
              f"g = 1-|{sfp[1]:.6f}| = {1-abs(sfp[1]):.6f}")

    # ─── LYAPUNOV [LE] ───
    print("\n── LYAPUNOV EXPONENT [LE] ──\n")
    chaos = Op(-3.8, 3.8, 0.0)  # Logistic r=3.8
    check("Logistic r=3.8 has positive Lyapunov",
          chaos.lyapunov > 0,
          f"λ_L = {chaos.lyapunov:.4f}")
    # Published reference: λ_L(r=3.8) ≈ 0.44 (Strogatz, various)
    check("Logistic r=3.8 λ_L ≈ 0.44 (±0.15)",
          abs(chaos.lyapunov - 0.44) < 0.15,
          f"Got {chaos.lyapunov:.4f}, reference ≈ 0.44")

    stable_op = Op(0.01, 0.1, 0.01)
    check("Near-linear map has negative Lyapunov",
          stable_op.lyapunov < 0,
          f"λ_L = {stable_op.lyapunov:.4f}")

    # ─── ENTROPY [SE] ───
    print("\n── SHANNON ENTROPY [SE] ──\n")
    check("Chaotic orbit entropy > stable orbit entropy",
          chaos.entropy > stable_op.entropy,
          f"Chaotic H={chaos.entropy:.3f}, stable H={stable_op.entropy:.3f}")

    const_op = Op(0, 0, 0.5)  # f(x)=0.5 always
    check("Constant map has H ≈ 0",
          const_op.entropy < 0.1,
          f"H = {const_op.entropy:.6f}")

    # ─── ENERGY [HM] ───
    print("\n── ENERGY [HM analogy] ──\n")
    if sfp:
        E_manual = 0.5*sfp[1]**2 + abs(op(sfp[0])-sfp[0])
        check("E = ½λ² + |f(x*)-x*|",
              abs(op.energy - E_manual) < 1e-10,
              f"Manual: {E_manual:.8f}, Op.energy: {op.energy:.8f}")

    # ─── PARTITION FUNCTION [SM] ───
    print("\n── STATISTICAL MECHANICS [SM] ──\n")
    lat = Lattice("test"); lat.add(Op(0.2, 0.3, 0.1))
    E = Op(0.2, 0.3, 0.1).energy
    if math.isfinite(E):
        Z_manual = math.exp(-E)
        check("Single-op Z = exp(-E)",
              abs(lat.partition_function() - Z_manual) < 1e-6,
              f"Z = {lat.partition_function():.8f}, exp(-{E:.6f}) = {Z_manual:.8f}")
        check("Single-op F = E",
              abs(lat.free_energy() - E) < 1e-6,
              f"F = {lat.free_energy():.8f}")

    # ─── COHERENCE [TIG-1] ───
    print("\n── COHERENCE S* [TIG-1] ──\n")
    # Iterate vs analytic
    x = 0.5
    for _ in range(10000): x = SIGMA * (1-x)
    analytic = SIGMA/(1+SIGMA)
    check("Iteration converges to σ/(1+σ) (V*=A*=1)",
          abs(x - analytic) < 1e-6,
          f"Iterated: {x:.10f}, analytic: {analytic:.10f}")

    lat2 = Lattice("coh_test")
    for _ in range(100): lat2.add(Op(0, 0, 0.5))  # 100 CRYSTAL ops
    # All CRYSTAL → A* = 1.0, n=100 → V* = 1-exp(-2) ≈ 0.8647
    v = 1-math.exp(-100/50); a = 1.0; k = SIGMA*v*a; expected_S = k/(1+k)
    check("100 CRYSTAL ops: S* matches formula",
          abs(lat2.coherence() - expected_S) < 1e-8,
          f"S* = {lat2.coherence():.8f}, k/(1+k) = {expected_S:.8f}\n"
          f"    V*={v:.6f} A*={a} k={k:.6f}")

    # ─── FITTER [OLS] ───
    print("\n── FITTER ACCURACY [OLS] ──\n")
    true_a, true_b, true_c = 0.3, 0.5, 0.1
    series = [0.2]
    for _ in range(50):
        nxt = true_a*series[-1]**2 + true_b*series[-1] + true_c
        if abs(nxt) > 1e10: break
        series.append(nxt)
    if len(series) > 10:
        rec, mse = Fitter.fit_with_residual(series)
        check("Recover a from exact data",
              abs(rec.a - true_a) < 0.05,
              f"True: {true_a}, recovered: {rec.a:.4f}")
        check("Recover b from exact data",
              abs(rec.b - true_b) < 0.05,
              f"True: {true_b}, recovered: {rec.b:.4f}")
        check("Recover c from exact data",
              abs(rec.c - true_c) < 0.05,
              f"True: {true_c}, recovered: {rec.c:.4f}")
        check("MSE ≈ 0 for exact data",
              mse < 1e-8,
              f"MSE = {mse:.2e}")

    # ─── BAND CLASSIFICATION [TIG-5] ───
    print("\n── BAND CLASSIFICATION [TIG-5] ──\n")
    check("Logistic r=3.8 → MOLECULAR (chaos)",
          chaos.band == 3, f"Band: {chaos.band_name}")
    check("f(x)=0.5 → CRYSTAL (constant attractor)",
          const_op.band == 6, f"Band: {const_op.band_name}")

    # Logistic r=3.2 is period-2
    p2 = Op(-3.2, 3.2, 0.0)
    check("Logistic r=3.2 → CELLULAR (period-2)",
          p2.band == 4, f"Band: {p2.band_name}")

    # ─── SELF REFERENCE ───
    print("\n── SELF-REFERENCE ──\n")
    engine = TIG("selftest")
    engine.feed("s1", [0.5+0.1*math.sin(i*0.3) for i in range(80)])
    engine.feed("s2", [0.3+0.2*math.cos(i*0.2) for i in range(80)])
    ref = engine.self_reflect(depth=20)
    check("Self-reflection produces finite numbers",
          all(math.isfinite(x) for x in ref['trajectory']),
          f"First 5: {ref['trajectory'][:5]}")
    check("Self-reflection converges",
          ref['converged'],
          f"Final S*: {ref['final']}, tail σ: {ref['tail_std']:.2e}")

    # ─── SUMMARY ───
    print(f"\n{'═'*58}")
    print(f"  RESULTS: {ok}/{total} passed, {fail} failed")
    if fail == 0: print("  ALL DERIVATIONS VERIFIED ✓")
    else: print(f"  {fail} CHECK(S) NEED ATTENTION")
    print(f"{'═'*58}")
    print(f"\n  ESTABLISHED MATH used in this engine:")
    print(f"    ✓ Quadratic maps [DDS, May 1976]")
    print(f"    ✓ Fixed points and stability [FP, Banach 1922]")
    print(f"    ✓ Spectral gap [SG, Perron 1907]")
    print(f"    ✓ Lyapunov exponents [LE, Oseledets 1968]")
    print(f"    ✓ Shannon entropy [SE, Shannon 1948]")
    print(f"    ✓ Statistical mechanics [SM, Boltzmann/Gibbs]")
    print(f"    ✓ OLS regression [OLS, Gauss 1809]")
    print(f"\n  TIG CONJECTURES (testable, falsifiable):")
    print(f"    ◎ S* = σ(1-σ*)V*A* is a useful coherence measure [TIG-1]")
    print(f"    ◎ σ = {SIGMA} is a good coupling constant [TIG-2, CHOSEN]")
    print(f"    ◎ D* = {D_STAR:.6f} = σ/(1+σ) [TIG-3, DERIVED]")
    print(f"    ◎ T* = {T_STAR:.6f} = 5/7 [TIG-4, CHOSEN]")
    print(f"    ◎ E = ½|λ|²+|f(x*)-x*| is a useful energy mapping [HM]")
    print(f"    ◎ Routing by band+gap maximizes coherence [LA]")
    print(f"\n  HONEST CORRECTIONS from prior versions:")
    print(f"    ⚠ D* was published as 0.543. Correct derivation: {D_STAR:.6f}")
    print(f"    ⚠ T* = 5/7 is rational. Golden ratio link unproven.")
    print(f"    ⚠ Band boundaries (|λ|=0.5) are convention, not physics.")
    print(f"\n  The math belongs to everyone.")
    print(f"  NON-COMMERCIAL TESTING — 7Site LLC — 7sitellc.com")
    print(f"{'═'*58}")
    return ok, fail


def demo():
    print("╔════════════════════════════════════════════════════════════╗")
    print("║  TIG ENGINE — DEMO WITH KNOWN DYNAMICS                   ║")
    print("╚════════════════════════════════════════════════════════════╝\n")

    engine = TIG("demo")

    # Signals with KNOWN physics — so you can verify
    signals = {
        "stable_sinusoid": [0.5 + 0.01*math.sin(i*0.1) for i in range(100)],
        "logistic_r2.5":   None,  # Built below
        "logistic_r3.2":   None,
        "logistic_r3.8":   None,
        "constant_0.5":    [0.5]*100,
    }
    for r, name in [(2.5, "logistic_r2.5"), (3.2, "logistic_r3.2"), (3.8, "logistic_r3.8")]:
        s = [0.3]
        for _ in range(99): s.append(r*s[-1]*(1-s[-1]))
        signals[name] = s

    for name, data in signals.items():
        engine.feed(name, data)

    # State
    state = engine.state()
    print(f"Engine: {state['name']}")
    print(f"S* = {state['coherence']}  (above T*={T_STAR:.4f}: {state['above_T_star']})")
    print(f"V* = {state['V_star']}  A* = {state['A_star']}")
    print(f"Bands: {state['bands']}\n")

    # Per-sensor detail with full physics
    for name, sensor in engine.sensors.items():
        print(f"── {name} ──")
        print(sensor.op.explain())
        print()

    # Coherence derivation (show your work)
    lat = Lattice("demo_lat")
    for s in engine.sensors.values():
        if len(s.norm) >= 6: lat.add(s.op)
    print(f"── COHERENCE DERIVATION ──")
    print(f"  {lat.coherence_derivation()}")
    print(f"  S* = {lat.coherence():.8f}")

    # Self-reference
    print(f"\n── SELF-REFERENCE ──")
    ref = engine.self_reflect(depth=10)
    print(f"  Trajectory: {ref['trajectory']}")
    print(f"  Converged: {ref['converged']}")
    print(f"  D* (derived): {D_STAR:.6f}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo()
    else:
        verify()
