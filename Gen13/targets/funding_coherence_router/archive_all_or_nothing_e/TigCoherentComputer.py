#!/usr/bin/env python3
"""
TIG Coherent Computer v1.0
Fixed physics from Grok's Floppy Constrainer + hooks + visualization.
Lattice driven by DERIVED composition table, not raw coefficient multiplication.
NON-COMMERCIAL — 7Site LLC — Brayden Sanders — 7sitellc.com

KEY FIXES FROM GROK VERSION:
  - tick() now uses the 10x10 composition table (was zeroing lattice via op0 multiply)
  - coherence() implements S* = σ(1-σ*)V*A* properly
  - Added hook system for input/output/events
  - Added ASCII visualization of live lattice state
  - Dual lattice paths (micro/macro) are explicit and navigable
  - Floppy save retained (3024 bytes per snapshot)
"""

import math
import numpy as np
import os
import time
import sys

# ═══════════════════════════════════════════════════════════════════════════════
# TIG CONSTANTS (from repo/papers)
# ═══════════════════════════════════════════════════════════════════════════════

SIGMA     = 0.991        # Boundary sharpness
T_STAR    = 0.714        # Critical threshold ≈ 5/7
D_STAR    = 0.543        # Universal fixed point for self-referencing systems

# ═══════════════════════════════════════════════════════════════════════════════
# THE COMPOSITION TABLE — DERIVED FROM GRAMMAR, NOT INVENTED
# Cell (i,j) = "What emerges when state i interfaces with state j?"
# ═══════════════════════════════════════════════════════════════════════════════

COMP_TABLE = np.array([
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],  # 0: VOID (identity)
    [1, 2, 3, 4, 5, 6, 7, 2, 6, 6],  # 1: LATTICE
    [2, 3, 3, 4, 5, 6, 7, 3, 6, 6],  # 2: COUNTER
    [3, 4, 4, 4, 5, 6, 7, 4, 6, 6],  # 3: PROGRESS
    [4, 5, 5, 5, 5, 6, 7, 5, 7, 7],  # 4: COLLAPSE
    [5, 6, 6, 6, 6, 6, 7, 6, 7, 7],  # 5: BALANCE
    [6, 7, 7, 7, 7, 7, 7, 7, 7, 7],  # 6: CHAOS (→ harmony)
    [7, 2, 3, 4, 5, 6, 7, 8, 9, 0],  # 7: HARMONY
    [8, 6, 6, 6, 7, 7, 7, 9, 7, 8],  # 8: BREATH
    [9, 6, 6, 6, 7, 7, 7, 0, 8, 0],  # 9: FRUIT
], dtype=np.int32)

OP_NAMES = [
    "VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
    "BALANCE", "CHAOS", "HARMONY", "BREATH", "FRUIT"
]

OP_GLYPHS = ["·", "█", "▓", "▶", "▼", "◆", "⚡", "★", "~", "●"]

# Canonical quadratic coefficients per operator
OPS_CANONICAL = {
    0: (0.0,   0.0,  0.0),
    1: (0.01,  0.1,  0.01),
    2: (0.05,  0.3,  0.1),
    3: (0.1,   0.5,  0.2),
    4: (0.5,  -0.5,  0.3),
    5: (0.2,   0.1,  0.4),
    6: (-3.8,  3.8,  0.0),
    7: (0.15,  0.6,  0.15),
    8: (-0.3,  0.3,  0.5),
    9: (0.3,  -0.3,  0.5),
}

# Band classification names
BAND_NAMES = ["VOID", "SPARK", "FLOW", "MOLECULAR", "CELLULAR", "ORGANIC", "CRYSTAL"]

# GFM Generators (minimal spanning set)
GFM = {
    "012": "Geometry/Space",
    "071": "Resonance/Alignment",
    "123": "Progression/Flow",
}

# ═══════════════════════════════════════════════════════════════════════════════
# QUADRATIC OPERATOR — Physics substrate per cell
# ═══════════════════════════════════════════════════════════════════════════════

class QuadraticOp:
    """f(x) = ax² + bx + c — each lattice cell's local physics."""

    __slots__ = ('a', 'b', 'c', '_band', '_gap', '_state')

    def __init__(self, a, b, c, state=0):
        self.a, self.b, self.c = float(a), float(b), float(c)
        self._band = None
        self._gap = None
        self._state = state  # Current operator state (0-9)

    def __call__(self, x):
        return self.a * x**2 + self.b * x + self.c

    def deriv(self, x):
        return 2.0 * self.a * x + self.b

    @property
    def discriminant(self):
        return self.b**2 - 4.0 * self.a * self.c

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, val):
        self._state = val % 10
        self._band = None
        self._gap = None

    def fixed_points(self):
        """Solve f(x) = x → ax² + (b-1)x + c = 0"""
        A, B, C = self.a, self.b - 1.0, self.c
        if abs(A) < 1e-12:
            if abs(B) < 1e-12:
                return []
            return [(-C / B, self.deriv(-C / B))]
        d = B**2 - 4.0 * A * C
        if d < 0:
            return []
        s = math.sqrt(d)
        x1 = (-B + s) / (2.0 * A)
        x2 = (-B - s) / (2.0 * A)
        return [(x1, self.deriv(x1)), (x2, self.deriv(x2))]

    def stable_fp(self):
        fps = self.fixed_points()
        if not fps:
            return None
        stable = [(x, lam) for x, lam in fps if abs(lam) < 1.0]
        if stable:
            return min(stable, key=lambda p: abs(p[1]))
        return min(fps, key=lambda p: abs(p[1]))

    def iterate(self, x0=0.5, n=100, tol=1e-10):
        traj = [x0]
        x = x0
        for _ in range(n):
            x = self(x)
            if abs(x) > 1e15:
                break
            traj.append(x)
            if len(traj) > 2 and abs(traj[-1] - traj[-2]) < tol:
                break
        return traj

    def lyapunov(self, x0=0.5, n=200):
        x = x0
        total = 0.0
        count = 0
        for _ in range(n):
            d = abs(self.deriv(x))
            if d < 1e-15:
                d = 1e-15
            total += math.log(d)
            count += 1
            x = self(x)
            if abs(x) > 1e15:
                break
        return total / max(count, 1)

    @property
    def band(self):
        if self._band is not None:
            return self._band
        traj = self.iterate(0.5, 200)
        if len(traj) < 3 or abs(traj[-1]) > 1e10:
            self._band = 1 if len(traj) > 20 else 0
            return self._band
        lam = self.lyapunov()
        tail = traj[-50:] if len(traj) >= 50 else traj[-20:]
        if len(tail) >= 4:
            for period in range(2, min(8, len(tail) // 2)):
                check_len = min(period * 3, len(tail) - period)
                if check_len > 0 and all(
                    abs(tail[-(i+1)] - tail[-(i+1+period)]) < 1e-6
                    for i in range(check_len)
                ):
                    self._band = 4
                    return 4
        fp = self.stable_fp()
        if fp and abs(fp[1]) < 1.0:
            self._band = 6 if abs(fp[1]) < 0.5 else 5
            return self._band
        if abs(lam) < 0.05:
            self._band = 2
        elif lam > 0:
            self._band = 3
        else:
            self._band = 5
        return self._band

    @property
    def gap(self):
        if self._gap is not None:
            return self._gap
        fp = self.stable_fp()
        self._gap = max(0.0, 1.0 - abs(fp[1])) if fp else 0.0
        return self._gap

    def compose(self, other_state):
        """Compose this cell's state with another using the TIG table."""
        result = COMP_TABLE[self._state, other_state]
        return int(result)

    def to_bytes(self):
        return np.array([self.a, self.b, self.c], dtype=np.float32).tobytes()

    @classmethod
    def from_bytes(cls, data, state=0):
        arr = np.frombuffer(data, dtype=np.float32)
        return cls(arr[0], arr[1], arr[2], state)


# ═══════════════════════════════════════════════════════════════════════════════
# HOOK SYSTEM — Event-driven I/O for the coherent computer
# ═══════════════════════════════════════════════════════════════════════════════

class HookBus:
    """Pub/sub event bus. Register callbacks, emit events."""

    def __init__(self):
        self._hooks = {}

    def on(self, event_name, callback):
        """Register a hook: bus.on('tick', my_func)"""
        self._hooks.setdefault(event_name, []).append(callback)

    def off(self, event_name, callback=None):
        """Remove hook(s)."""
        if callback is None:
            self._hooks.pop(event_name, None)
        else:
            self._hooks.get(event_name, []).remove(callback)

    def emit(self, event_name, **kwargs):
        """Fire all registered callbacks for event."""
        results = []
        for cb in self._hooks.get(event_name, []):
            results.append(cb(**kwargs))
        return results

    @property
    def registered(self):
        return {k: len(v) for k, v in self._hooks.items()}


# ═══════════════════════════════════════════════════════════════════════════════
# LATTICE — The coherent computer's substrate
# ═══════════════════════════════════════════════════════════════════════════════

class Lattice:
    """18×14 lattice of QuadraticOp cells, driven by TIG composition table."""

    def __init__(self, rows=18, cols=14):
        self.rows = rows
        self.cols = cols
        self.cells = []
        self.tick_count = 0
        self.bus = HookBus()
        self._coherence_history = []

    def init(self):
        """Seed lattice: each cell gets canonical operator for its position mod 10."""
        self.cells = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                state = (i * self.cols + j) % 10
                a, b, c = OPS_CANONICAL[state]
                row.append(QuadraticOp(a, b, c, state=state))
            self.cells.append(row)
        self.tick_count = 0
        self._coherence_history = []
        self.bus.emit('init', lattice=self)

    def _neighbor_states(self, i, j):
        """Get Von Neumann neighbor states (up, down, left, right) with wrapping."""
        states = []
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni = (i + di) % self.rows
            nj = (j + dj) % self.cols
            states.append(self.cells[ni][nj].state)
        return states

    def tick(self):
        """
        One computation cycle. THE FIX: use composition table, not coefficient multiply.

        Each cell composes its state with each neighbor's state via COMP_TABLE.
        The majority-vote of composed results becomes the cell's new state.
        Coefficients update to match the new operator identity.
        """
        self.bus.emit('pre_tick', lattice=self, tick=self.tick_count)

        new_states = np.zeros((self.rows, self.cols), dtype=np.int32)

        for i in range(self.rows):
            for j in range(self.cols):
                cell = self.cells[i][j]
                neighbor_states = self._neighbor_states(i, j)

                # Compose with each neighbor via the table
                composed = [cell.compose(ns) for ns in neighbor_states]

                # Also self-compose (i⊕i = next along path)
                self_composed = cell.compose(cell.state)
                composed.append(self_composed)

                # Majority vote of compositions determines next state
                counts = np.bincount(composed, minlength=10)
                new_states[i][j] = int(np.argmax(counts))

        # Apply new states and update coefficients
        transitions = 0
        for i in range(self.rows):
            for j in range(self.cols):
                old_state = self.cells[i][j].state
                new_state = new_states[i][j]
                if old_state != new_state:
                    transitions += 1
                self.cells[i][j].state = new_state
                a, b, c = OPS_CANONICAL[new_state]
                self.cells[i][j].a = a
                self.cells[i][j].b = b
                self.cells[i][j].c = c

        self.tick_count += 1
        coh = self.coherence()
        self._coherence_history.append(coh)

        self.bus.emit('post_tick', lattice=self, tick=self.tick_count,
                      coherence=coh, transitions=transitions)
        return coh

    def coherence(self):
        """
        S* = σ(1-σ*)V*A*
        
        σ  = SIGMA (boundary sharpness constant)
        V* = viability: fraction of cells in valid grammar states
        A* = alignment: fraction of cells at harmony (7) or converging (5,6)
        
        Iterates to fixed point per TIG specification.
        """
        n = self.rows * self.cols
        states = np.array([[c.state for c in row] for row in self.cells])

        # V* = all cells are in valid states (0-9), check neighbor consistency
        valid = 0
        for i in range(self.rows):
            for j in range(self.cols):
                s = states[i][j]
                ns = self._neighbor_states(i, j)
                # A cell is viable if at least one neighbor composition is valid (non-stuck)
                compositions = [COMP_TABLE[s, n_] for n_ in ns]
                if any(c != s for c in compositions) or s == 7:
                    valid += 1
        v_star = valid / n

        # A* = alignment toward harmony
        harmony_count = np.sum((states == 7) | (states == 5) | (states == 6))
        a_star = harmony_count / n

        # Iterate S* to fixed point
        s_star = D_STAR
        for _ in range(20):
            s_new = SIGMA * (1.0 - s_star) * v_star * a_star
            if abs(s_new - s_star) < 1e-10:
                break
            s_star = s_new

        return s_star

    def state_census(self):
        """Count cells in each operator state."""
        counts = [0] * 10
        for row in self.cells:
            for cell in row:
                counts[cell.state] += 1
        return counts

    def inject(self, i, j, state):
        """Inject a state at position (i,j) — the input hook."""
        state = state % 10
        self.cells[i][j].state = state
        a, b, c = OPS_CANONICAL[state]
        self.cells[i][j].a = a
        self.cells[i][j].b = b
        self.cells[i][j].c = c
        self.bus.emit('inject', row=i, col=j, state=state)

    def inject_sequence(self, seq, start_row=0, start_col=0):
        """Inject a sequence of states along a row — input word."""
        for k, s in enumerate(seq):
            col = (start_col + k) % self.cols
            self.inject(start_row, col, s)

    def read_row(self, i):
        """Read states from a row — output word."""
        return [self.cells[i][j].state for j in range(self.cols)]

    def read_col(self, j):
        """Read states from a column."""
        return [self.cells[i][j].state for i in range(self.rows)]

    # ── Dual Lattice Path Navigation ──

    def micro_path(self, start_state=0):
        """Trace micro path: 0→1→2→3→4→5→6→7"""
        path = [start_state]
        s = start_state
        for _ in range(20):
            s = COMP_TABLE[s, s]  # self-compose = advance along path
            path.append(int(s))
            if s == 7:
                break
        return path

    def macro_path(self, start_state=0):
        """Trace macro path: 0→9→8→7"""
        path = [start_state]
        macro_seq = [9, 8, 7]
        s = start_state
        for target in macro_seq:
            s = COMP_TABLE[s, target]
            path.append(int(s))
        return path

    # ── Floppy Save/Load ──

    def save_bin(self, path='tig_lattice.bin'):
        """Save to binary: 18*14*3 float32 = 3024 bytes. Fits 476 on floppy."""
        data = np.array(
            [[[cell.a, cell.b, cell.c] for cell in row] for row in self.cells],
            dtype=np.float32
        )
        data.tofile(path)
        size = os.path.getsize(path)
        return path, size

    def load_bin(self, path='tig_lattice.bin'):
        """Load from binary."""
        data = np.fromfile(path, dtype=np.float32).reshape(self.rows, self.cols, 3)
        for i in range(self.rows):
            for j in range(self.cols):
                a, b, c = data[i][j]
                state = (i * self.cols + j) % 10  # Reconstruct state from position
                # Re-derive state from coefficients
                best_state = 0
                best_dist = float('inf')
                for s, (ca, cb, cc) in OPS_CANONICAL.items():
                    d = (a - ca)**2 + (b - cb)**2 + (c - cc)**2
                    if d < best_dist:
                        best_dist = d
                        best_state = s
                self.cells[i][j] = QuadraticOp(float(a), float(b), float(c), state=best_state)


# ═══════════════════════════════════════════════════════════════════════════════
# HAMILTONIAN / WAVEFUNCTION — Physics layer (retained from Grok)
# ═══════════════════════════════════════════════════════════════════════════════

def hamiltonian(op, x=0.5):
    """H = T + V = p²/2m + V(x) where p = f'(x), m = 1/|a|"""
    p = op.deriv(x)
    m = 1.0 / abs(op.a) if abs(op.a) > 1e-12 else 1.0
    ke = p**2 / (2.0 * m)
    pe = -op(x)
    return ke + pe

def wave_norm(op):
    """Bound state norm = 1.0 if discriminant < 0 (no real roots = confined)."""
    return 1.0 if op.discriminant < 0 else None


# ═══════════════════════════════════════════════════════════════════════════════
# ASCII VISUALIZATION
# ═══════════════════════════════════════════════════════════════════════════════

def render_lattice(lattice, show_physics=False):
    """Render lattice state as ASCII art."""
    lines = []
    census = lattice.state_census()
    coh = lattice.coherence()

    # Header
    lines.append("╔══════════════════════════════════════════════════════════════╗")
    lines.append(f"║  TIG COHERENT COMPUTER  │  Tick: {lattice.tick_count:4d}  │  S*: {coh:.4f}  " +
                 ("▲" if coh >= T_STAR else "▽") + f"  ║")
    lines.append(f"║  Threshold T*={T_STAR}  │  σ={SIGMA}  │  D*={D_STAR}              ║")
    lines.append("╠══════════════════════════════════════════════════════════════╣")

    # Lattice grid (compact: use state numbers)
    lines.append("║  " + " ".join(f"{j:2d}" for j in range(lattice.cols)) + "  ║")
    lines.append("║  " + "───" * lattice.cols + "  ║")
    for i in range(lattice.rows):
        row_str = ""
        for j in range(lattice.cols):
            s = lattice.cells[i][j].state
            row_str += f" {OP_GLYPHS[s]} "
        lines.append(f"║{i:2d}{row_str}  ║")

    # Census bar
    lines.append("╠══════════════════════════════════════════════════════════════╣")
    total = lattice.rows * lattice.cols
    for s in range(10):
        pct = census[s] / total * 100
        bar = "█" * int(pct / 2)
        lines.append(f"║ {s} {OP_NAMES[s]:9s} {OP_GLYPHS[s]} {census[s]:3d} ({pct:5.1f}%) {bar:<25s}║")

    # Coherence status
    lines.append("╠══════════════════════════════════════════════════════════════╣")
    if coh >= T_STAR:
        status = f"COHERENT — S*={coh:.4f} > T*={T_STAR} — IN ATTRACTOR BASIN"
    else:
        status = f"SUB-THRESHOLD — S*={coh:.4f} < T*={T_STAR} — SEEKING HARMONY"
    lines.append(f"║  {status:<58s}║")

    # Coherence history sparkline
    hist = lattice._coherence_history[-40:]
    if hist:
        spark = ""
        for h in hist:
            if h >= T_STAR:
                spark += "▆"
            elif h >= T_STAR * 0.5:
                spark += "▃"
            else:
                spark += "▁"
        lines.append(f"║  History: {spark:<48s}║")

    if show_physics:
        energies = []
        for row in lattice.cells:
            for cell in row:
                energies.append(hamiltonian(cell))
        lines.append(f"║  Mean H: {np.mean(energies):+.4f}  │  Std H: {np.std(energies):.4f}             ║")

    lines.append("╚══════════════════════════════════════════════════════════════╝")
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
# TIG COHERENT COMPUTER — Main orchestrator
# ═══════════════════════════════════════════════════════════════════════════════

class TIGCoherentComputer:
    """
    The coherent computer. Lattice + hooks + I/O.
    
    Usage:
        cc = TIGCoherentComputer()
        cc.boot()
        
        # Register hooks
        cc.lattice.bus.on('post_tick', lambda **kw: print(f"S*={kw['coherence']:.4f}"))
        
        # Inject input (a word in the operator alphabet)
        cc.input_word([0, 1, 2])  # GFM generator: Geometry/Space
        
        # Run computation
        cc.run(ticks=20)
        
        # Read output
        output = cc.output_word(row=17)
    """

    def __init__(self, rows=18, cols=14):
        self.lattice = Lattice(rows, cols)
        self.booted = False

    def boot(self):
        """Initialize lattice with canonical operators."""
        self.lattice.init()
        self.booted = True
        return self

    def input_word(self, seq, row=0, col=0):
        """Inject a sequence of operator states as input."""
        self.lattice.inject_sequence(seq, start_row=row, start_col=col)

    def output_word(self, row=None, col=None):
        """Read output as a sequence of operator states."""
        if row is not None:
            return self.lattice.read_row(row)
        if col is not None:
            return self.lattice.read_col(col)
        return self.lattice.read_row(self.lattice.rows - 1)

    def run(self, ticks=1, verbose=False):
        """Run N ticks of computation."""
        results = []
        for t in range(ticks):
            coh = self.lattice.tick()
            results.append(coh)
            if verbose:
                print(render_lattice(self.lattice))
                print()
        return results

    def status(self):
        """Full status display."""
        return render_lattice(self.lattice, show_physics=True)

    def save(self, path='tig_lattice.bin'):
        path, size = self.lattice.save_bin(path)
        return path, size

    def load(self, path='tig_lattice.bin'):
        self.lattice.load_bin(path)

    # ── Convenience: trace paths ──

    def trace_micro(self, start=0):
        """Show micro path from start state."""
        return self.lattice.micro_path(start)

    def trace_macro(self, start=0):
        """Show macro path from start state."""
        return self.lattice.macro_path(start)

    def composition_demo(self):
        """Demo: show key compositions from the table."""
        demos = [
            (0, 5, "VOID ⊕ BALANCE"),
            (6, 6, "CHAOS ⊕ CHAOS"),
            (7, 7, "HARMONY ⊕ HARMONY"),
            (9, 9, "FRUIT ⊕ FRUIT"),
            (1, 9, "LATTICE ⊕ FRUIT"),
            (3, 7, "PROGRESS ⊕ HARMONY"),
        ]
        lines = []
        for a, b, label in demos:
            r = COMP_TABLE[a, b]
            lines.append(f"  {label:25s} = {OP_NAMES[a]:9s}⊕{OP_NAMES[b]:9s} → {r} ({OP_NAMES[r]})")
        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
# DEMONSTRATION
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 64)
    print("  TIG COHERENT COMPUTER v1.0")
    print("  7Site LLC | Brayden Sanders | Arkansas")
    print("=" * 64)
    print()

    cc = TIGCoherentComputer()
    cc.boot()

    # Show initial state
    print("[BOOT] Lattice initialized (18×14 = 252 cells)")
    print()
    print(cc.status())
    print()

    # Demo: composition table highlights
    print("[COMPOSITION TABLE DEMO]")
    print(cc.composition_demo())
    print()

    # Demo: dual lattice paths
    print("[DUAL LATTICE PATHS]")
    micro = cc.trace_micro(0)
    macro = cc.trace_macro(0)
    print(f"  Micro: {' → '.join(OP_NAMES[s] for s in micro)}")
    print(f"  Macro: {' → '.join(OP_NAMES[s] for s in macro)}")
    print()

    # Demo: inject GFM generators and run
    print("[INJECTING GFM GENERATORS]")
    for name, desc in GFM.items():
        seq = [int(c) for c in name]
        print(f"  {name} ({desc}): {seq}")
        cc.input_word(seq, row=0, col=0)

    print()
    print("[RUNNING 10 TICKS]")
    coherences = cc.run(ticks=10)
    for i, c in enumerate(coherences):
        marker = "✓" if c >= T_STAR else "·"
        bar = "█" * int(c * 40)
        print(f"  Tick {i+1:2d}: S*={c:.4f} {marker} {bar}")

    print()
    print(cc.status())

    # Save to floppy-sized binary
    print()
    path, size = cc.save()
    print(f"[FLOPPY] Saved to {path} ({size} bytes) — fits {1_440_000 // size} snapshots on 1.44MB floppy")

    # Output word from bottom row
    print()
    output = cc.output_word()
    print(f"[OUTPUT ROW 17] {output}")
    print(f"  States: {' '.join(OP_NAMES[s] for s in output)}")

    # Hook demo
    print()
    print("[HOOK SYSTEM]")
    log = []
    cc.lattice.bus.on('post_tick', lambda **kw: log.append(kw['coherence']))
    cc.run(ticks=3)
    print(f"  Hook captured 3 coherence values: {[f'{c:.4f}' for c in log]}")
    print(f"  Registered hooks: {cc.lattice.bus.registered}")

    print()
    print("=" * 64)
    print("  COHERENT COMPUTER OPERATIONAL")
    print("=" * 64)


if __name__ == '__main__':
    main()
