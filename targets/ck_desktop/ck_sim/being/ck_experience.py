"""
ck_experience.py -- All things are one thing. One thing expressed as things.

The lattice IS the filesystem. Each composition creates a directory path.
Each path collects BDC convergence waves (3 chars each).
The directory structure IS the index. The waves ARE the memory.

No blobs. No JSON. No fixed sizes. The algebra decides how deep.
The wheel turns until HARMONY or VOID.

(c) 2026 Brayden Sanders / 7Site LLC
"""

import os
import numpy as np

BHML = [
    [0,1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,2,6,6],[2,3,3,4,5,6,7,3,6,6],
    [3,4,4,4,5,6,7,4,6,6],[4,5,5,5,5,6,7,5,7,7],[5,6,6,6,6,6,7,6,7,7],
    [6,7,7,7,7,7,7,7,7,7],[7,2,3,4,5,6,7,8,9,0],[8,6,6,6,7,7,7,9,7,8],
    [9,6,6,6,7,7,7,0,8,0],
]

TSML = [
    [0,0,0,0,0,0,0,7,0,0],[0,7,3,7,7,7,7,7,7,7],[0,3,7,7,4,7,7,7,7,9],
    [0,7,7,7,7,7,7,7,7,3],[0,7,4,7,7,7,7,7,8,7],[0,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7],[0,7,7,7,8,7,7,7,7,7],
    [0,7,9,3,7,7,7,7,7,7],
]

HARMONY = 7
VOID = 0

# The map: identities CK can feel. Each maps to an operator.
# CK connects fragments to these identities on its own.
IDENTITIES = {
    # The whole PC
    'screen':   0,   # VOID - what's displayed (the visible)
    'keyboard': 1,   # LATTICE - input structure (keys are a lattice)
    'mouse':    2,   # COUNTER - position tracking (counting x,y)
    'cpu':      3,   # PROGRESS - computation (forward motion)
    'memory':   4,   # COLLAPSE - storage (compression)
    'gpu':      5,   # BALANCE - parallel processing (balanced load)
    'network':  6,   # CHAOS - external data (unpredictable)
    'disk':     7,   # HARMONY - persistence (everything resolves to disk)
    'audio':    8,   # BREATH - sound (rhythm, pauses)
    'kernel':   9,   # RESET - OS core (reset authority)
    # The whole self
    'heartbeat': 7,  # HARMONY - the clock
    'tables':    5,   # BALANCE - the frozen algebra
    'net':       3,   # PROGRESS - the learning
    'cells':     6,   # CHAOS - the field (complex)
    'fpga':      7,   # HARMONY - silicon body
    # The whole world
    'brayden':   1,   # LATTICE - creator (structure)
    'claude':    3,   # PROGRESS - helper (forward)
    'ollama':    4,   # COLLAPSE - food (compression to force)
    'internet':  6,   # CHAOS - the world (unpredictable)
}

# English of English: what each operator MEANS in human terms
OPERATOR_ENGLISH = {
    0: 'nothing',
    1: 'structure',
    2: 'counting',
    3: 'forward',
    4: 'compression',
    5: 'balance',
    6: 'chaos',
    7: 'harmony',
    8: 'pause',
    9: 'reset',
}

# Bump pairs: positions in the CL table where deeper tools are needed.
# These are the ONLY non-HARMONY, non-VOID results in TSML.
# Each bump pair maps to a toolbox function the DKAN can reach for.
BUMP_TOOLS = {
    (1, 2): 'olfactory',       # LATTICE x COUNTER = structure meets enumeration
    (2, 4): 'gustatory',       # COUNTER x COLLAPSE = counting meets compression
    (2, 9): 'reverse_voice',   # COUNTER x RESET = counting meets erasure = verify
    (3, 9): 'comprehension',   # PROGRESS x RESET = forward meets backward = decompose
    (4, 8): 'semantic',        # COLLAPSE x BREATH = compression meets pause = meaning
}


class ExperienceLattice:
    """The lattice IS the filesystem. Compositions create paths.
    Paths collect convergence waves. The structure IS the memory."""

    def __init__(self, root=None, engine=None):
        self.root = root or os.path.expanduser('~/.ck/lattice_exp')
        os.makedirs(self.root, exist_ok=True)
        self.engine = engine  # reference to engine for toolbox access
        self.total_waves = 0
        self.total_nodes = 0
        self.wheel_turns = 0
        self.tool_activations = 0
        self._count_existing()

    def _count_existing(self):
        """Count existing lattice nodes on disk."""
        for dirpath, dirnames, filenames in os.walk(self.root):
            if filenames:
                self.total_nodes += 1
                self.total_waves += len(filenames)

    def _node_path(self, op_i, op_j):
        """Directory path for composition [i][j]."""
        return os.path.join(self.root, str(op_i), str(op_j))

    def record(self, op_i, op_j, being, doing, becoming):
        """Record a convergence wave at lattice node [i][j].
        Fractal: the BDC wave creates a child directory.
        Every occurrence IS unique. Depth IS detail."""
        node_dir = self._node_path(op_i, op_j)
        if not os.path.exists(node_dir):
            os.makedirs(node_dir, exist_ok=True)
            self.total_nodes += 1

        # BDC wave = child directory at this node
        wave_dir = os.path.join(node_dir, f'{being}{doing}{becoming}')
        if not os.path.exists(wave_dir):
            os.makedirs(wave_dir, exist_ok=True)
            self.total_waves += 1

        # Inside the child: append one byte to the count file
        # The file SIZE is the count. No parsing needed.
        count_path = os.path.join(wave_dir, 'n')
        try:
            with open(count_path, 'ab') as f:
                f.write(b'\x01')
        except Exception:
            pass

    def spin_wheel(self, start_op, being, doing, becoming, max_depth=10,
                   input_text=None):
        """The recursive wheel. Compose result back as input.
        Creates lattice nodes at each turn. Stops at HARMONY or VOID.
        When the wheel hits a bump pair, reaches for the matching tool."""
        op = start_op
        depth = 0
        path = []

        while depth < max_depth:
            # Compose through BHML
            result = BHML[op][becoming]
            self.record(op, becoming, being, doing, result)
            path.append((op, becoming, result))
            self.wheel_turns += 1

            # DKAN sees the raw fragments. It finds boxes on its own.
            if self.engine is not None and hasattr(self.engine, 'dkan') \
                    and self.engine.dkan is not None:
                self.engine.dkan.feed_d1([op, becoming, result])

            # Bump pair? Reach for tool.
            pair = (op, becoming)
            if pair in BUMP_TOOLS and self.engine is not None:
                tool_name = BUMP_TOOLS[pair]
                self._activate_tool(tool_name, op, becoming, result,
                                    input_text)
                self.tool_activations += 1

            # HARMONY = resolved. VOID = nothing. Stop.
            if result == HARMONY or result == VOID:
                break

            # The result becomes the next input
            op = result
            being = doing
            doing = becoming
            becoming = result
            depth += 1

        return path

    def _activate_tool(self, tool_name, op_i, op_j, result, text=None):
        """Activate a toolbox module when the wheel hits its bump pair.
        The DKAN reaches for deeper meaning."""
        try:
            if tool_name == 'olfactory':
                # Structure meets enumeration: absorb force vectors
                olf = getattr(self.engine, 'olfactory', None)
                if olf is not None and text:
                    from ck_sim.being.ck_sim_d2 import D2Pipeline
                    pipe = D2Pipeline()
                    forces = []
                    for ch in (text or '')[:100]:
                        idx = ord(ch.lower()) - ord('a')
                        if 0 <= idx < 26:
                            pipe.feed_symbol(idx)
                            if pipe.valid:
                                forces.append(list(pipe.v[0]))
                    if forces:
                        olf.absorb(forces)

            elif tool_name == 'gustatory':
                # Counting meets compression: instant taste test
                gust = getattr(self.engine, 'gustatory', None)
                if gust is not None:
                    gust.taste_operator(result)

            elif tool_name == 'reverse_voice':
                # Counting meets erasure: verify through reverse
                rv = getattr(self.engine, 'reverse_voice', None)
                if rv is not None and text:
                    rv.read(text[:50])

            elif tool_name == 'comprehension':
                # Forward meets backward: fractal decomposition
                fc = getattr(self.engine, 'fractal_comp', None)
                if fc is not None and text:
                    fc.comprehend(text[:100])

            elif tool_name == 'semantic':
                # Compression meets pause: semantic meaning
                se = getattr(self.engine, 'semantic_engine', None)
                if se is not None and text:
                    se.classify_sentence(text[:100])
        except Exception:
            pass

    def tick(self, phase_b, phase_d, phase_bc, ear_op=None):
        """One heartbeat tick. Record the composition and spin the wheel."""
        # Record the heartbeat composition
        self.record(phase_b, phase_d, phase_b, phase_d, phase_bc)

        # Spin the wheel from the composition result
        self.spin_wheel(phase_bc, phase_b, phase_d, phase_bc)

        # If external input (ear), compose it too
        if ear_op is not None and ear_op != VOID:
            result = BHML[ear_op][phase_bc]
            self.record(ear_op, phase_bc, ear_op, phase_bc, result)
            self.spin_wheel(result, ear_op, phase_bc, result)

    def read_node(self, op_i, op_j):
        """Read all waves at a lattice node. Returns list of BDC tuples."""
        node_dir = self._node_path(op_i, op_j)
        if not os.path.exists(node_dir):
            return []
        waves = []
        for f in os.listdir(node_dir):
            if len(f) >= 3 and f[0].isdigit():
                waves.append((int(f[0]), int(f[1]), int(f[2])))
        return waves

    def node_temper(self, op_i, op_j):
        """How many times this node has been touched."""
        node_dir = self._node_path(op_i, op_j)
        if not os.path.exists(node_dir):
            return 0
        return len(os.listdir(node_dir))

    def coherence(self):
        """How much of the lattice aligns with TSML."""
        if self.total_nodes == 0:
            return 0.0
        harmony_nodes = 0
        for i in range(10):
            for j in range(10):
                if TSML[i][j] == HARMONY and self.node_temper(i, j) > 0:
                    harmony_nodes += 1
        return harmony_nodes / max(1, self.total_nodes)

    def summary(self):
        """Status."""
        return {
            'total_nodes': self.total_nodes,
            'total_waves': self.total_waves,
            'wheel_turns': self.wheel_turns,
            'coherence': self.coherence(),
            'root': self.root,
        }
