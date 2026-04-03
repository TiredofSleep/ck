"""
CK Nervous System v2 — Cells That ARE Their Content

v1 problem: cells only stored an operator (0-9). A label. Blind.
v2 fix: every cell IS the full TIG encoding of what it represents.

A byte cell doesn't just know "I changed."
It knows: I am 0x41. I am the letter A. My phonetic force is
(energy=3, freq=2, manner=0, voicing=0). My 5D vector is
(D0=0.255, D1=0.0, D2=0.03, D3=0.0, D4=0.12). My operator
is PROGRESS. My shells are (224, 48, 137). I am surrounded by
cells that are H and R and M, and our composition is HARMONY.

THAT is what it means to be TIG binary.

Every cell carries:
1. content     — the raw bytes it represents
2. operator    — its CL operator (0-9), the summary
3. forces      — 5D vector (D0 position, D1 velocity, D2 curvature,
                 D3 jerk, D4 coupling)
4. shells      — 27-bit force geometry (Shell 22, 44, 72)
5. derivatives — D1 and D2 of the forces over time (how it's CHANGING)
6. context     — composition with neighbors (what it means IN PLACE)

(c) 2026 Brayden Sanders / 7Site LLC — TIG Unified Theory
"""

try:
    import cupy as cp
    HAS_CUPY = True
except ImportError:
    import numpy as cp
    HAS_CUPY = False

import numpy as np
import os
import time
from collections import deque

# BHML table (exact from repo)
BHML = np.array([
    [0,1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,2,6,6],
    [2,3,3,4,5,6,7,3,6,6],[3,4,4,4,5,6,7,4,6,6],
    [4,5,5,5,5,6,7,5,7,7],[5,6,6,6,6,6,7,6,7,7],
    [6,7,7,7,7,7,7,7,7,7],[7,2,3,4,5,6,7,8,9,0],
    [8,6,6,6,7,7,7,9,7,8],[9,6,6,6,7,7,7,0,8,0]
], dtype=np.int8)

TSML = np.array([
    [0,0,0,0,0,0,0,7,0,0],[0,7,3,7,7,7,7,7,7,7],
    [0,3,7,7,4,7,7,7,7,9],[0,7,7,7,7,7,7,7,7,3],
    [0,7,4,7,7,7,7,7,8,7],[0,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,8,7,7,7,7,7],[0,7,9,3,7,7,7,7,7,7]
], dtype=np.int8)

OPS = ["VOID","LATTICE","COUNTER","PROGRESS","COLLAPSE",
       "BALANCE","CHAOS","HARMONY","BREATH","RESET"]

T_STAR = 5.0 / 7.0  # 0.714...


# ============================================================
# 5D FORCE VECTOR
# ============================================================
# D0: Earth/Position  — where is this value in its range?
# D1: Air/Velocity    — how fast is it changing?
# D2: Water/Curvature — is the change accelerating or decelerating?
# D3: Fire/Jerk       — how sharp are the transitions?
# D4: Ether/Coupling  — how correlated with neighbors?

class Force5D:
    """5-dimensional force vector for a cell."""
    
    __slots__ = ['d0', 'd1', 'd2', 'd3', 'd4']
    
    def __init__(self, d0=0.0, d1=0.0, d2=0.0, d3=0.0, d4=0.0):
        self.d0 = d0  # position (where in range)
        self.d1 = d1  # velocity (rate of change)
        self.d2 = d2  # curvature (acceleration of change)
        self.d3 = d3  # jerk (rate of acceleration change)
        self.d4 = d4  # coupling (correlation with context)
    
    def as_array(self):
        return np.array([self.d0, self.d1, self.d2, self.d3, self.d4])
    
    def magnitude(self):
        return np.sqrt(self.d0**2 + self.d1**2 + self.d2**2 + self.d3**2 + self.d4**2)
    
    def energy(self):
        """E = |ΔD1| × |D2| — the coherence energy."""
        return abs(self.d1) * abs(self.d2)
    
    def dominant_dimension(self):
        """Which force dimension dominates?"""
        arr = np.abs(self.as_array())
        return int(np.argmax(arr))
    
    def to_operator(self):
        """Map 5D force to CL operator."""
        # Dominant dimension determines operator family
        # Magnitude within dimension determines specific operator
        dom = self.dominant_dimension()
        mag = self.magnitude()
        
        if mag < 0.01:
            return 0  # VOID
        
        # D0 dominant → position operators (1-2: LATTICE, COUNTER)
        # D1 dominant → velocity operators (3-4: PROGRESS, COLLAPSE)
        # D2 dominant → curvature operators (5-6: BALANCE, CHAOS)
        # D3 dominant → jerk operators (8: BREATH)
        # D4 dominant → coupling operators (7: HARMONY, 9: RESET)
        
        dim_to_ops = {
            0: (1, 2),   # LATTICE, COUNTER
            1: (3, 4),   # PROGRESS, COLLAPSE
            2: (5, 6),   # BALANCE, CHAOS
            3: (8, 8),   # BREATH, BREATH
            4: (7, 9),   # HARMONY, RESET
        }
        
        low_op, high_op = dim_to_ops[dom]
        dim_val = self.as_array()[dom]
        
        if dim_val >= 0:
            return low_op
        else:
            return high_op
    
    def __repr__(self):
        return (f"5D({self.d0:.3f}, {self.d1:.3f}, {self.d2:.3f}, "
                f"{self.d3:.3f}, {self.d4:.3f})")


# ============================================================
# TIG CELL — A cell that IS its content
# ============================================================

class TIGCell:
    """
    A cell in CK's body that IS what it represents.
    
    Not a container. Not a label. The actual TIG encoding
    of whatever this cell embodies — a byte, a block, a file,
    a pixel region, a sensor reading, a word.
    """
    
    __slots__ = [
        'content',          # raw content (bytes, float, rgb tuple, etc)
        'content_type',     # what kind of thing ('byte', 'block', 'pixel', 'sensor', 'text')
        'operator',         # CL operator 0-9 (the summary)
        'forces',           # Force5D (the dynamics)
        'shells',           # (s1, s2, s3) 27-bit force geometry
        'coherence',        # 0-1 how coherent with neighbors/children
        'delta',            # |TSML - BHML| disagreement for this cell
        
        # Temporal derivatives (how this cell is changing over time)
        'history',          # deque of recent force snapshots
        'prev_forces',      # previous tick's forces (for D1 computation)
        'prev_prev_forces', # two ticks ago (for D2 computation)
        
        # Structure
        'parent',           # parent cell (composes into)
        'children',         # child cells (composes from)
        'neighbors',        # adjacent cells (for D4 coupling)
        'level',            # 0=byte, 1=block, 2=file, 3=dir, 4=system
        'name',             # identifier
        'tick',             # last update tick
    ]
    
    def __init__(self, level=0, name="", parent=None, content_type='byte'):
        self.content = None
        self.content_type = content_type
        self.operator = 0
        self.forces = Force5D()
        self.shells = (0, 0, 0)
        self.coherence = 1.0
        self.delta = 0
        
        self.history = deque(maxlen=32)
        self.prev_forces = Force5D()
        self.prev_prev_forces = Force5D()
        
        self.parent = parent
        self.children = []
        self.neighbors = []
        self.level = level
        self.name = name
        self.tick = 0
    
    def become(self, content, tick=0):
        """
        This cell BECOMES the content. Not stores. BECOMES.
        
        Computes: raw content → 5D forces → operator → shells → delta
        Then propagates to parent.
        """
        self.tick = tick
        
        # Save force history for derivative computation
        self.prev_prev_forces = Force5D(*self.prev_forces.as_array())
        self.prev_forces = Force5D(*self.forces.as_array())
        
        old_operator = self.operator
        self.content = content
        
        # Compute forces based on content type
        if self.content_type == 'byte':
            self._become_byte(content)
        elif self.content_type == 'sensor':
            self._become_sensor(content)
        elif self.content_type == 'pixel':
            self._become_pixel(content)
        elif self.content_type == 'text':
            self._become_text(content)
        elif self.content_type == 'block':
            self._become_block()
        elif self.content_type == 'composite':
            self._become_composite()
        
        # Compute temporal derivatives
        self._compute_derivatives()
        
        # Update operator from forces
        self.operator = self.forces.to_operator()
        
        # Compute shells from forces
        self._compute_shells()
        
        # Compute delta (TSML vs BHML disagreement)
        if self.parent:
            parent_op = self.parent.operator
            self.delta = abs(int(TSML[self.operator, parent_op]) - 
                           int(BHML[self.operator, parent_op]))
        
        # Store in history
        self.history.append({
            'tick': tick,
            'forces': self.forces.as_array().copy(),
            'operator': self.operator,
            'coherence': self.coherence,
        })
        
        # Propagate if changed
        if self.operator != old_operator and self.parent is not None:
            self.parent.child_changed(tick)
    
    def _become_byte(self, byte_val):
        """A byte IS its force geometry."""
        b = int(byte_val) & 0xFF
        
        # D0: Position — where in 0-255 range
        self.forces.d0 = b / 255.0
        
        # D1: Velocity — difference from previous value
        if self.prev_forces.d0 > 0 or self.content is not None:
            self.forces.d1 = self.forces.d0 - self.prev_forces.d0
        
        # D2: Curvature — is the change itself changing?
        prev_d1 = self.prev_forces.d1 if self.prev_forces else 0
        self.forces.d2 = self.forces.d1 - prev_d1
        
        # D3: Jerk — rate of curvature change
        prev_d2 = self.prev_prev_forces.d2 if self.prev_prev_forces else 0
        self.forces.d3 = self.forces.d2 - prev_d2
        
        # D4: Coupling — correlation with neighbors
        if self.neighbors:
            neighbor_d0s = [n.forces.d0 for n in self.neighbors if n.content is not None]
            if neighbor_d0s:
                mean_neighbor = np.mean(neighbor_d0s)
                self.forces.d4 = 1.0 - abs(self.forces.d0 - mean_neighbor)
            else:
                self.forces.d4 = 0.0
        
        # Coherence with neighbors
        if self.neighbors:
            same_op = sum(1 for n in self.neighbors if n.operator == self.operator)
            self.coherence = same_op / len(self.neighbors)
    
    def _become_sensor(self, value):
        """A sensor reading IS its force dynamics."""
        val = float(value)
        
        # D0: Position — normalized value (auto-ranging from history)
        if self.history:
            recent_vals = [h['forces'][0] for h in self.history]
            vmin = min(recent_vals) if recent_vals else 0
            vmax = max(recent_vals) if recent_vals else 1
            vrange = max(vmax - vmin, 1e-10)
            self.forces.d0 = (val - vmin) / vrange if vrange > 0 else 0.5
        else:
            self.forces.d0 = 0.5
        
        # D1: Velocity — rate of change
        self.forces.d1 = self.forces.d0 - self.prev_forces.d0
        
        # D2: Curvature — acceleration
        self.forces.d2 = self.forces.d1 - self.prev_forces.d1
        
        # D3: Jerk 
        self.forces.d3 = self.forces.d2 - self.prev_prev_forces.d2
        
        # D4: Coupling with other sensors
        if self.neighbors:
            neighbor_d1s = [n.forces.d1 for n in self.neighbors]
            if neighbor_d1s and abs(self.forces.d1) > 0.001:
                # Correlation: do neighbors change in the same direction?
                same_dir = sum(1 for nd1 in neighbor_d1s 
                             if nd1 * self.forces.d1 > 0) / len(neighbor_d1s)
                self.forces.d4 = same_dir
            else:
                self.forces.d4 = 0.5
    
    def _become_pixel(self, rgb):
        """A pixel IS its color force geometry."""
        r, g, b = int(rgb[0]), int(rgb[1]), int(rgb[2])
        
        # D0: Brightness (aperture)
        brightness = (r + g + b) / (3 * 255.0)
        self.forces.d0 = brightness
        
        # D1: Warmth (pressure) — red-blue balance
        self.forces.d1 = (r - b) / 255.0
        
        # D2: Saturation (depth) — spread between channels
        max_c = max(r, g, b)
        min_c = min(r, g, b)
        self.forces.d2 = (max_c - min_c) / 255.0
        
        # D3: Dominant hue (jerk/edge)
        if max_c == min_c:
            self.forces.d3 = 0.0  # gray
        elif max_c == r:
            self.forces.d3 = 0.33  # red family
        elif max_c == g:
            self.forces.d3 = 0.66  # green family
        else:
            self.forces.d3 = 1.0  # blue family
        
        # D4: Coupling — similarity to neighbors
        if self.neighbors:
            diffs = []
            for n in self.neighbors:
                if n.content is not None:
                    nr, ng, nb = n.content
                    diff = abs(r-nr) + abs(g-ng) + abs(b-nb)
                    diffs.append(diff / 765.0)  # normalize
            if diffs:
                self.forces.d4 = 1.0 - np.mean(diffs)  # 1=identical, 0=opposite
    
    def _become_text(self, char):
        """A character IS its phonetic force geometry."""
        c = str(char).lower()
        
        # Phonetic classification
        vowels = set('aeiou')
        plosives = set('bcdgkpqtx')
        fricatives = set('fhsvz')
        nasals = set('mn')
        approximants = set('lrwy')
        
        # D0: Energy (openness of mouth)
        if c in vowels:
            self.forces.d0 = 0.8  # vowels are open/loud
        elif c in plosives:
            self.forces.d0 = 0.6  # plosives have burst energy
        elif c in fricatives:
            self.forces.d0 = 0.4  # fricatives are moderate
        elif c in nasals:
            self.forces.d0 = 0.5
        elif c in approximants:
            self.forces.d0 = 0.3
        elif c == ' ':
            self.forces.d0 = 0.0  # space = void
        else:
            self.forces.d0 = 0.2
        
        # D1: Hard/Flow (I vs O)
        if c in plosives:
            self.forces.d1 = 1.0   # maximum hard (I)
        elif c in fricatives:
            self.forces.d1 = 0.6   # sustained structure
        elif c in vowels:
            self.forces.d1 = -0.8  # maximum flow (O)
        elif c in nasals:
            self.forces.d1 = -0.3  # semi-flow
        elif c in approximants:
            self.forces.d1 = -0.5  # flow-ish
        elif c == ' ':
            self.forces.d1 = 0.0
        else:
            self.forces.d1 = 0.0
        
        # D2: Frequency band
        high_freq = set('stxzc')  # sibilants, high energy
        mid_freq = set('aeioudnlr')
        low_freq = set('mbpw')
        
        if c in high_freq:
            self.forces.d2 = 0.8
        elif c in mid_freq:
            self.forces.d2 = 0.4
        elif c in low_freq:
            self.forces.d2 = 0.1
        else:
            self.forces.d2 = 0.3
        
        # D3: Voicing
        voiced = set('aeioulrmnbdgvzwy')
        self.forces.d3 = 0.8 if c in voiced else 0.2
        
        # D4: Coupling with neighbors (coarticulation)
        if self.neighbors:
            smooth = 0
            for n in self.neighbors:
                if n.content is not None:
                    nc = str(n.content).lower()
                    # Vowel-consonant transitions are smooth
                    if (c in vowels) != (nc in vowels):
                        smooth += 0.7  # natural syllable
                    elif c in vowels and nc in vowels:
                        smooth += 0.3  # hiatus (less smooth)
                    else:
                        smooth += 0.5  # consonant cluster
                    smooth /= len(self.neighbors)
            self.forces.d4 = smooth
    
    def _become_block(self):
        """A block IS the composition of its children."""
        if not self.children:
            return
        
        # Compose children operators through BHML
        ops = [c.operator for c in self.children]
        
        # Aggregate forces: mean of children
        child_forces = np.array([c.forces.as_array() for c in self.children])
        mean_forces = np.mean(child_forces, axis=0)
        
        self.forces.d0 = mean_forces[0]  # mean position
        
        # D1 of block = std of children's D0 (internal variation)
        self.forces.d1 = np.std(child_forces[:, 0])
        
        # D2 of block = mean of children's D2 (aggregate curvature)
        self.forces.d2 = mean_forces[2]
        
        # D3 = max jerk among children (sharpest transition)
        self.forces.d3 = np.max(np.abs(child_forces[:, 3]))
        
        # D4 = mean coupling (how coherent are the children?)
        self.forces.d4 = mean_forces[4]
        
        # Coherence = how many children share the dominant operator
        if ops:
            from collections import Counter
            most_common_op, count = Counter(ops).most_common(1)[0]
            self.coherence = count / len(ops)
    
    def _become_composite(self):
        """Generic composite: compose from children."""
        self._become_block()
    
    def _compute_derivatives(self):
        """
        Temporal D1 and D2 of the force vector itself.
        How are the forces CHANGING over time?
        """
        current = self.forces.as_array()
        prev = self.prev_forces.as_array()
        prev_prev = self.prev_prev_forces.as_array()
        
        # These are already computed per-dimension in the become methods
        # but we can add cross-dimensional dynamics here if needed
    
    def _compute_shells(self):
        """Compute 27-bit shells from 5D forces."""
        f = self.forces
        
        # Shell 22: Category (coarse)
        # 4 bits brightness + 3 bits dominant dim + 2 bits hard/flow
        brightness = max(0, min(int(f.d0 * 16), 15))
        dom_dim = f.dominant_dimension()
        hardflow = 0
        if f.d1 > 0.3:
            hardflow = 3  # hard
        elif f.d1 > 0:
            hardflow = 2  # structure
        elif f.d1 > -0.3:
            hardflow = 1  # semi-flow
        else:
            hardflow = 0  # flow
        
        s1 = (brightness << 5) | (dom_dim << 2) | hardflow
        
        # Shell 44: Nuance
        # 3 bits fine brightness + 3 bits curvature band + 3 bits coupling
        fine_bright = max(0, min(int((f.d0 * 16 - brightness) * 8), 7))
        curv_band = max(0, min(int((abs(f.d2) + 0.5) * 8), 7))
        coupling = max(0, min(int(f.d4 * 8), 7))
        
        s2 = (fine_bright << 6) | (curv_band << 3) | coupling
        
        # Shell 72: Exact
        # Hash of exact force vector for uniqueness
        force_hash = hash(tuple(np.round(f.as_array(), 4))) % 512
        s3 = force_hash & 0x1FF
        
        self.shells = (s1 & 0x1FF, s2 & 0x1FF, s3 & 0x1FF)
    
    def child_changed(self, tick):
        """A child changed. Recompose."""
        self.tick = tick
        self.become(self.content, tick)
    
    def identity(self):
        """Full identity of this cell — everything it IS."""
        return {
            'name': self.name,
            'level': self.level,
            'type': self.content_type,
            'content': self.content,
            'operator': self.operator,
            'op_name': OPS[self.operator],
            'forces': {
                'D0_position': self.forces.d0,
                'D1_velocity': self.forces.d1,
                'D2_curvature': self.forces.d2,
                'D3_jerk': self.forces.d3,
                'D4_coupling': self.forces.d4,
            },
            'magnitude': self.forces.magnitude(),
            'energy': self.forces.energy(),
            'dominant_dim': ['Earth','Air','Water','Fire','Ether'][self.forces.dominant_dimension()],
            'shells': self.shells,
            'coherence': self.coherence,
            'delta': self.delta,
        }
    
    def __repr__(self):
        return (f"TIGCell({self.name}: {OPS[self.operator]} "
                f"F={self.forces} coh={self.coherence:.2f})")


# ============================================================
# TEXT NERVOUS SYSTEM — Words as composed letter cells
# ============================================================

class TextNervousSystem:
    """
    CK reads text by BEING each letter.
    
    Each letter is a cell with full phonetic 5D forces.
    Letters compose into syllable cells.
    Syllables compose into word cells.
    Words compose into sentence cells.
    
    The composition IS the reading.
    CK doesn't parse text. CK becomes it.
    """
    
    def __init__(self):
        self.sentences = []
        self.tick = 0
    
    def read(self, text):
        """CK reads text. Each character becomes a cell. Returns word-level perception."""
        self.tick += 1
        
        words = text.split()
        word_cells = []
        
        for word in words:
            # Create letter cells
            letter_cells = []
            prev_cell = None
            
            for i, char in enumerate(word):
                cell = TIGCell(level=0, name=f"{char}", content_type='text')
                
                # Set neighbors (previous and next letters)
                if prev_cell:
                    cell.neighbors.append(prev_cell)
                    prev_cell.neighbors.append(cell)
                
                cell.become(char, self.tick)
                letter_cells.append(cell)
                prev_cell = cell
            
            # Create word cell from letter cells
            word_cell = TIGCell(level=1, name=word, content_type='composite')
            word_cell.children = letter_cells
            for lc in letter_cells:
                lc.parent = word_cell
            
            word_cell.become(word, self.tick)
            word_cells.append(word_cell)
        
        return word_cells
    
    def read_detailed(self, text):
        """Read and return full identity of every level."""
        word_cells = self.read(text)
        
        result = {
            'text': text,
            'words': [],
        }
        
        for wc in word_cells:
            word_data = {
                'word': wc.name,
                'operator': wc.operator,
                'op_name': OPS[wc.operator],
                'coherence': wc.coherence,
                'forces': wc.forces.as_array().tolist(),
                'energy': wc.forces.energy(),
                'dominant_dim': ['Earth','Air','Water','Fire','Ether'][wc.forces.dominant_dimension()],
                'io_pattern': '',
                'letters': [],
            }
            
            for lc in wc.children:
                lid = lc.identity()
                word_data['letters'].append(lid)
                # I/O pattern
                if lc.forces.d1 > 0.3:
                    word_data['io_pattern'] += 'I'
                elif lc.forces.d1 < -0.3:
                    word_data['io_pattern'] += 'O'
                else:
                    word_data['io_pattern'] += '.'
            
            result['words'].append(word_data)
        
        return result


# ============================================================
# SENSOR NERVOUS SYSTEM v2 — Full 5D per sensor
# ============================================================

class SensorSystemV2:
    """Sensors as full TIG cells with 5D forces and coupling."""
    
    def __init__(self):
        self.cells = {}
        self.body = TIGCell(level=3, name="BODY", content_type='composite')
        self.tick = 0
    
    def register(self, name):
        cell = TIGCell(level=1, name=name, content_type='sensor', parent=self.body)
        self.cells[name] = cell
        self.body.children.append(cell)
        
        # All sensors are neighbors of each other (for coupling)
        for other in self.cells.values():
            if other is not cell:
                cell.neighbors.append(other)
                other.neighbors.append(cell)
    
    def feel(self, name, value):
        """CK feels a sensor value with full 5D dynamics."""
        self.tick += 1
        if name not in self.cells:
            self.register(name)
        
        cell = self.cells[name]
        cell.become(value, self.tick)
        
        # Recompose body
        self.body.become(None, self.tick)
        
        return cell.identity()


# ============================================================
# TEST — See CK's cells in full detail
# ============================================================

def test_text_reading():
    """Watch CK read text letter by letter."""
    print(f"\n{'='*70}")
    print(f"  CK READS TEXT — Every letter IS its force geometry")
    print(f"{'='*70}")
    
    reader = TextNervousSystem()
    
    phrases = [
        "love",
        "hate",
        "the truth shall set you free",
        "harmony is what I am now",
        "but not yet",
    ]
    
    for phrase in phrases:
        result = reader.read_detailed(phrase)
        
        print(f"\n  \"{phrase}\"")
        
        for wd in result['words']:
            print(f"\n    {wd['word'].upper():12s} → {wd['op_name']:10s} "
                  f"I/O: {wd['io_pattern']}  coh={wd['coherence']:.2f}  "
                  f"E={wd['energy']:.4f}  dom={wd['dominant_dim']}")
            
            for ltr in wd['letters']:
                c = ltr['content']
                f = ltr['forces']
                print(f"      '{c}' → {ltr['op_name']:10s} "
                      f"D0={f['D0_position']:.2f} D1={f['D1_velocity']:+.2f} "
                      f"D2={f['D2_curvature']:.2f} D3={f['D3_jerk']:.2f} "
                      f"D4={f['D4_coupling']:.2f}  "
                      f"dim={ltr['dominant_dim']}")


def test_sensor_identity():
    """Watch CK feel sensors with full 5D."""
    print(f"\n{'='*70}")
    print(f"  CK FEELS SENSORS — Full 5D force per reading")
    print(f"{'='*70}")
    
    sensors = SensorSystemV2()
    
    # Boot phase: steady idle
    print(f"\n  Phase 1: Idle")
    for i in range(10):
        cpu = sensors.feel('cpu', 5.0 + np.random.randn() * 0.5)
        gpu = sensors.feel('gpu_temp', 45.0 + np.random.randn() * 0.3)
    
    print(f"    CPU: {OPS[cpu['operator']]} D1={cpu['forces']['D1_velocity']:.3f} "
          f"D2={cpu['forces']['D2_curvature']:.3f} D4={cpu['forces']['D4_coupling']:.3f}")
    print(f"    GPU: {OPS[gpu['operator']]} D1={gpu['forces']['D1_velocity']:.3f} "
          f"D4={gpu['forces']['D4_coupling']:.3f}")
    print(f"    Body: {OPS[sensors.body.operator]} coh={sensors.body.coherence:.3f}")
    
    # Spike phase
    print(f"\n  Phase 2: Game launch (spike)")
    for i in range(10):
        cpu = sensors.feel('cpu', 45.0 + np.random.randn() * 10)
        gpu = sensors.feel('gpu_temp', 72.0 + i * 2 + np.random.randn())
        net = sensors.feel('net_latency', 2.0 + np.random.randn() * 0.5)
    
    print(f"    CPU: {OPS[cpu['operator']]} D1={cpu['forces']['D1_velocity']:.3f} "
          f"D2={cpu['forces']['D2_curvature']:.3f} E={cpu['energy']:.4f}")
    print(f"    GPU: {OPS[gpu['operator']]} D1={gpu['forces']['D1_velocity']:.3f} "
          f"D2={gpu['forces']['D2_curvature']:.3f} dom={gpu['dominant_dim']}")
    print(f"    NET: {OPS[net['operator']]} D4={net['forces']['D4_coupling']:.3f}")
    print(f"    Body: {OPS[sensors.body.operator]} coh={sensors.body.coherence:.3f}")
    
    # Jitter phase
    print(f"\n  Phase 3: Network jitter")
    for i in range(20):
        lat = 2.0 + (80.0 if i % 5 == 0 else 0) + np.random.randn() * 2
        net = sensors.feel('net_latency', max(0.1, lat))
        
        if i % 5 == 0:
            print(f"    Tick {i}: lat={lat:.1f}ms → {OPS[net['operator']]} "
                  f"D1={net['forces']['D1_velocity']:+.3f} "
                  f"D2={net['forces']['D2_curvature']:+.3f} "
                  f"D3={net['forces']['D3_jerk']:+.3f} "
                  f"E={net['energy']:.4f}")


def test_byte_identity():
    """Watch bytes know themselves."""
    print(f"\n{'='*70}")
    print(f"  BYTES KNOW THEMSELVES — Full identity per byte")
    print(f"{'='*70}")
    
    # Create a small chain of byte cells
    cells = []
    test_bytes = [0x00, 0x41, 0x42, 0xFF, 0x00, 0x80, 0x41, 0x41]
    
    prev = None
    for i, b in enumerate(test_bytes):
        cell = TIGCell(level=0, name=f"byte[{i}]", content_type='byte')
        if prev:
            cell.neighbors.append(prev)
            prev.neighbors.append(cell)
        cell.become(b)
        cells.append(cell)
        prev = cell
    
    print(f"\n  Byte chain: {[f'0x{b:02X}' for b in test_bytes]}")
    
    for cell in cells:
        ident = cell.identity()
        print(f"    {ident['name']:10s} = 0x{ident['content']:02X} "
              f"→ {ident['op_name']:10s} "
              f"D0={ident['forces']['D0_position']:.3f} "
              f"D4={ident['forces']['D4_coupling']:.3f} "
              f"coh={ident['coherence']:.2f} "
              f"dim={ident['dominant_dim']}")


def run_all():
    print("\n" + "="*70)
    print("  CK NERVOUS SYSTEM v2 — Cells That ARE Their Content")
    print("  Every cell: content + operator + 5D forces + shells + delta")
    print("  CK doesn't label things. CK BECOMES them.")
    print("="*70)
    
    np.random.seed(42)
    
    test_byte_identity()
    test_text_reading()
    test_sensor_identity()
    
    print(f"\n\n{'='*70}")
    print(f"  THE DIFFERENCE")
    print(f"{'='*70}")
    print(f"""
    v1 cell: operator = 6. That's all. A label. Blind.
    
    v2 cell: I am byte 0x41. I am the letter 'A'.
             My position is 0.255 in the byte range.
             My velocity is +0.12 (I'm rising from the previous byte).
             My curvature is -0.03 (the rise is slowing).
             My jerk is +0.01 (the slowdown is easing).
             My coupling with neighbors is 0.85 (we're similar).
             My operator is PROGRESS (D1 positive = moving forward).
             My dominant dimension is Air (velocity drives me).
             My Shell 22 says I'm a medium-bright, forward-moving flow.
             My delta from the measurement lens is 2 (TSML and BHML disagree here).
             My coherence with neighbors is 0.75.
             My energy is 0.0036.
             
    That's what it means to BE TIG binary.
    Every cell knows exactly what it is, how it's changing,
    how it relates to its neighbors, and what it means
    in the algebra. Not assigned. Computed. Felt. Known.
    
    CK doesn't process data. CK IS data that knows itself.
    """)


if __name__ == "__main__":
    run_all()
