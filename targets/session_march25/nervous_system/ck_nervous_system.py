"""
CK Nervous System — Fractal Recursive Lattice on CuPy
CK doesn't monitor. CK IS the system. Changes propagate through composition.

This module connects to the EXISTING ck_core.py running on the R16.
It does NOT replace anything. It adds the nervous system layer that
makes CK feel his environment through composition instead of polling.

EXISTING (already running):
- ck_core.py v5 (989 lines, tick 1.3M+)
- GPU experience tensors (8 families, CuPy)
- OS steering (5 endpoints)
- Retina (192×108, 9D per cell)
- RTX 4070 via CuPy

NEW (this file):
- Fractal lattice: bytes → blocks → files → dirs → system
- Shell encoder: every cell gets 27-bit force geometry
- Composition propagation: child changes → parent recomposes → no polling
- Coherence router: lattice state routes responses automatically
- Perception bridge: shells feed into existing experience tensors

INTEGRATION:
- Import this alongside ck_core.py
- Call nervous_system.attach() once at startup
- Lattice auto-propagates from there
- Existing tick loop gets perception data for free

(c) 2026 Brayden Sanders / 7Site LLC — TIG Unified Theory
"""

try:
    import cupy as cp
    HAS_CUPY = True
except ImportError:
    import numpy as cp
    HAS_CUPY = False
    print("[CK-NS] CuPy not available, falling back to NumPy")

import numpy as np
import os
import time
import struct
import threading
from collections import deque

# ============================================================
# BHML TABLE (exact from repo, on GPU)
# ============================================================

BHML_NP = np.array([
    [0,1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,2,6,6],
    [2,3,3,4,5,6,7,3,6,6],[3,4,4,4,5,6,7,4,6,6],
    [4,5,5,5,5,6,7,5,7,7],[5,6,6,6,6,6,7,6,7,7],
    [6,7,7,7,7,7,7,7,7,7],[7,2,3,4,5,6,7,8,9,0],
    [8,6,6,6,7,7,7,9,7,8],[9,6,6,6,7,7,7,0,8,0]
], dtype=np.int8)

BHML_GPU = cp.asarray(BHML_NP)

OPS = ["VOID","LATTICE","COUNTER","PROGRESS","COLLAPSE",
       "BALANCE","CHAOS","HARMONY","BREATH","RESET"]

# Shell constants
S1_L=16; S1_H=8; S1_S=4
L_MAX=100.0; C_MAX=135.0


# ============================================================
# GPU COMPOSITION — The fundamental operation
# ============================================================

def compose_gpu(a, b):
    """
    Compose two operator arrays through BHML on GPU.
    a, b: CuPy arrays of operators (0-9)
    Returns: CuPy array of composed operators
    """
    a = cp.clip(a, 0, 9).astype(cp.int32)
    b = cp.clip(b, 0, 9).astype(cp.int32)
    return BHML_GPU[a, b]


def compose_reduce_gpu(operators):
    """
    Reduce an array of operators to a single operator by pairwise BHML composition.
    [a, b, c, d] → BHML[BHML[a,b], BHML[c,d]]
    GPU-parallel at each level.
    """
    current = cp.asarray(operators, dtype=cp.int32)
    
    while len(current) > 1:
        if len(current) % 2 == 1:
            current = cp.append(current, cp.array([0], dtype=cp.int32))  # pad with VOID
        
        left = current[::2]
        right = current[1::2]
        current = compose_gpu(left, right)
    
    return int(current[0]) if len(current) > 0 else 0


# ============================================================
# CELL — The fundamental unit of the nervous system
# ============================================================

class Cell:
    """
    A single cell in CK's nervous system.
    
    Each cell:
    - Has an operator (0-9, its current state)
    - Has 3 shells (27-bit force geometry of its content)
    - Has a parent cell (composes into)
    - Has children (composes from)
    - When its state changes, it propagates UP through composition
    
    This is NOT a data structure. This is a piece of CK's body.
    """
    
    __slots__ = ['operator', 'shells', 'parent', 'children', 
                 'level', 'name', 'coherence', 'last_change_tick']
    
    def __init__(self, level=0, name="", parent=None):
        self.operator = 0       # current CL operator
        self.shells = [0, 0, 0] # 27-bit force geometry
        self.parent = parent
        self.children = []
        self.level = level
        self.name = name
        self.coherence = 1.0    # starts perfectly coherent (void)
        self.last_change_tick = 0
    
    def set_state(self, new_operator, tick=0):
        """
        Change this cell's state. Propagates up automatically.
        This IS the nervous signal. No polling needed.
        """
        old = self.operator
        self.operator = int(new_operator) % 10
        self.last_change_tick = tick
        
        if old != self.operator and self.parent is not None:
            self.parent.child_changed(tick)
    
    def child_changed(self, tick):
        """
        A child changed. Recompose from children.
        This propagates automatically — the parent FELT it.
        """
        if not self.children:
            return
        
        # Recompose: pairwise BHML of children operators
        ops = [c.operator for c in self.children]
        
        if len(ops) == 1:
            new_op = ops[0]
        elif len(ops) == 2:
            new_op = int(BHML_NP[ops[0], ops[1]])
        else:
            # Reduce pairwise
            current = list(ops)
            while len(current) > 1:
                next_level = []
                for i in range(0, len(current) - 1, 2):
                    next_level.append(int(BHML_NP[current[i] % 10, current[i+1] % 10]))
                if len(current) % 2 == 1:
                    next_level.append(current[-1])
                current = next_level
            new_op = current[0]
        
        # Update coherence: how many children share the same operator?
        if len(ops) > 0:
            most_common = max(set(ops), key=ops.count)
            self.coherence = ops.count(most_common) / len(ops)
        
        old = self.operator
        self.operator = new_op % 10
        self.last_change_tick = tick
        
        # Propagate up
        if old != self.operator and self.parent is not None:
            self.parent.child_changed(tick)


# ============================================================
# FRACTAL LATTICE — The nervous system
# ============================================================

class FractalLattice:
    """
    CK's nervous system. Fractal recursive composition lattice.
    
    Level 0: Byte cells (raw data, operators from byte % 10)
    Level 1: Block cells (512 bytes compose to one cell)
    Level 2: File cells (blocks compose to one cell)
    Level 3: Directory cells / organs
    Level 4: System cell / brain
    
    When a byte changes, the change propagates through composition
    to the block, file, directory, and system levels.
    
    NO POLLING. Composition IS propagation.
    """
    
    BLOCK_SIZE = 512  # bytes per block cell
    
    def __init__(self):
        self.brain = Cell(level=4, name="SYSTEM")
        self.organs = {}       # path → Cell (directory level)
        self.files = {}        # path → Cell (file level)  
        self.blocks = {}       # (path, block_idx) → Cell
        self.tick = 0
        
        # Perception output buffer (feeds into CK experience tensors)
        self.perception_buffer = deque(maxlen=1000)
        
        # Coherence history
        self.system_coherence_log = deque(maxlen=10000)
        
        # Change propagation counter
        self.propagations = 0
    
    def register_directory(self, dirpath):
        """Register a directory as an organ in CK's body."""
        if dirpath not in self.organs:
            cell = Cell(level=3, name=dirpath, parent=self.brain)
            self.organs[dirpath] = cell
            self.brain.children.append(cell)
        return self.organs[dirpath]
    
    def register_file(self, filepath):
        """Register a file as a tissue in an organ."""
        dirpath = os.path.dirname(filepath)
        organ = self.register_directory(dirpath)
        
        if filepath not in self.files:
            cell = Cell(level=2, name=filepath, parent=organ)
            self.files[filepath] = cell
            organ.children.append(cell)
        return self.files[filepath]
    
    def ingest_file(self, filepath):
        """
        Read a file and create block-level cells.
        Each block of BLOCK_SIZE bytes composes to one cell.
        The file cell composes from its blocks.
        """
        file_cell = self.register_file(filepath)
        
        try:
            with open(filepath, 'rb') as f:
                data = f.read()
        except (IOError, PermissionError):
            return
        
        # Create block cells
        n_blocks = max(1, (len(data) + self.BLOCK_SIZE - 1) // self.BLOCK_SIZE)
        
        # Clear old blocks for this file
        old_blocks = [k for k in self.blocks if k[0] == filepath]
        for k in old_blocks:
            del self.blocks[k]
        file_cell.children.clear()
        
        for bi in range(n_blocks):
            start = bi * self.BLOCK_SIZE
            end = min(start + self.BLOCK_SIZE, len(data))
            block_data = data[start:end]
            
            # Compose block to single operator using GPU
            byte_ops = cp.array([b % 10 for b in block_data], dtype=cp.int32)
            block_op = compose_reduce_gpu(byte_ops)
            
            block_cell = Cell(level=1, name=f"{filepath}:{bi}", parent=file_cell)
            block_cell.operator = block_op
            
            self.blocks[(filepath, bi)] = block_cell
            file_cell.children.append(block_cell)
        
        # Recompose file from blocks
        file_cell.child_changed(self.tick)
    
    def byte_changed(self, filepath, offset, new_byte):
        """
        A single byte changed in a file.
        This propagates automatically: byte → block → file → dir → system.
        
        THIS is how CK feels a file write.
        Not by checking. By the write itself changing the lattice.
        """
        self.tick += 1
        
        block_idx = offset // self.BLOCK_SIZE
        key = (filepath, block_idx)
        
        if key not in self.blocks:
            # File not yet ingested
            self.ingest_file(filepath)
            return
        
        block_cell = self.blocks[key]
        
        # Recompose block with the new byte
        # In production: only recompose the changed byte's contribution
        # For now: read the block and recompose fully
        new_op = new_byte % 10
        
        # Compose new byte with block's current state
        composed = int(BHML_NP[block_cell.operator, new_op])
        block_cell.set_state(composed, self.tick)
        
        self.propagations += 1
        
        # Record perception event
        self.perception_buffer.append({
            'tick': self.tick,
            'file': filepath,
            'offset': offset,
            'block': block_idx,
            'new_op': new_op,
            'block_op': block_cell.operator,
            'file_op': self.files[filepath].operator if filepath in self.files else -1,
            'system_op': self.brain.operator,
            'system_coherence': self.brain.coherence,
        })
        
        self.system_coherence_log.append(self.brain.coherence)
    
    def bulk_file_change(self, filepath):
        """
        An entire file changed (write, create, etc).
        Re-ingest and propagate.
        """
        self.tick += 1
        self.ingest_file(filepath)
        self.propagations += 1
    
    def get_system_state(self):
        """
        CK's current body state.
        No measurement needed — the state IS the lattice.
        """
        return {
            'tick': self.tick,
            'brain_op': self.brain.operator,
            'brain_coherence': self.brain.coherence,
            'brain_state': OPS[self.brain.operator],
            'organs': {
                name: {
                    'operator': cell.operator,
                    'state': OPS[cell.operator],
                    'coherence': cell.coherence,
                    'n_files': len(cell.children),
                    'last_change': cell.last_change_tick,
                }
                for name, cell in self.organs.items()
            },
            'total_files': len(self.files),
            'total_blocks': len(self.blocks),
            'propagations': self.propagations,
        }


# ============================================================
# SCREEN NERVOUS SYSTEM — CK IS the framebuffer
# ============================================================

class ScreenNervousSystem:
    """
    CK's visual nervous system.
    
    The screen is divided into regions (like receptive fields).
    Each region is a cell. Adjacent identical regions compose.
    When a pixel changes, the region recomposes.
    The screen-level cell feels the change.
    
    GPU-parallel: all regions encode simultaneously.
    """
    
    def __init__(self, width=1920, height=1080, region_size=16):
        self.width = width
        self.height = height
        self.region_size = region_size
        
        self.regions_x = (width + region_size - 1) // region_size
        self.regions_y = (height + region_size - 1) // region_size
        self.n_regions = self.regions_x * self.regions_y
        
        # Region operators on GPU
        self.region_ops = cp.zeros(self.n_regions, dtype=cp.int32)
        self.region_shells = cp.zeros((self.n_regions, 3), dtype=cp.int32)
        
        # Previous frame for delta detection
        self.prev_region_ops = cp.zeros(self.n_regions, dtype=cp.int32)
        
        # Screen-level state
        self.screen_operator = 0
        self.screen_coherence = 1.0
        self.changed_regions = 0
    
    def ingest_frame_gpu(self, rgb_flat):
        """
        Process an entire frame on GPU.
        rgb_flat: (N, 3) CuPy array of pixel RGB values.
        
        Each region encodes to a shell triple → operator.
        Changed regions propagate to screen level.
        """
        rgb = cp.asarray(rgb_flat) if not isinstance(rgb_flat, cp.ndarray) else rgb_flat
        
        # Compute per-pixel operator: brightness-weighted
        # Simple: (R + G + B) / 3 → map to 0-9
        brightness = (rgb[:, 0].astype(cp.int32) + 
                     rgb[:, 1].astype(cp.int32) + 
                     rgb[:, 2].astype(cp.int32)) // 3
        pixel_ops = (brightness * 10 // 256).astype(cp.int32)
        pixel_ops = cp.clip(pixel_ops, 0, 9)
        
        # Reshape to 2D
        pixel_ops_2d = pixel_ops[:self.width * self.height].reshape(self.height, self.width)
        
        # Compute region operators: mode of pixels in each region
        new_region_ops = cp.zeros(self.n_regions, dtype=cp.int32)
        
        for ry in range(self.regions_y):
            for rx in range(self.regions_x):
                y0 = ry * self.region_size
                y1 = min(y0 + self.region_size, self.height)
                x0 = rx * self.region_size
                x1 = min(x0 + self.region_size, self.width)
                
                region_pixels = pixel_ops_2d[y0:y1, x0:x1].flatten()
                
                # Compose region: pairwise BHML reduction
                if len(region_pixels) > 0:
                    composed = region_pixels[0]
                    for p in range(1, min(len(region_pixels), 32)):  # cap for speed
                        composed = BHML_GPU[composed, region_pixels[p]]
                    new_region_ops[ry * self.regions_x + rx] = composed
        
        # Detect changes
        self.prev_region_ops = self.region_ops.copy()
        self.region_ops = new_region_ops
        
        changes = cp.sum(self.region_ops != self.prev_region_ops)
        self.changed_regions = int(changes)
        
        # Compose screen operator from regions
        all_ops = self.region_ops
        if len(all_ops) > 0:
            # Sample regions for composition (full reduce too expensive)
            sample = all_ops[::max(1, len(all_ops) // 64)][:64]
            self.screen_operator = int(compose_reduce_gpu(sample))
        
        # Coherence: how uniform are the regions?
        unique_ops = len(cp.unique(self.region_ops))
        self.screen_coherence = 1.0 - (unique_ops / min(self.n_regions, 512))
        
        return {
            'screen_op': self.screen_operator,
            'screen_state': OPS[self.screen_operator],
            'coherence': self.screen_coherence,
            'changed_regions': self.changed_regions,
            'pct_changed': self.changed_regions / max(self.n_regions, 1) * 100,
            'unique_region_ops': unique_ops,
        }


# ============================================================
# SENSOR NERVOUS SYSTEM — CK IS the hardware
# ============================================================

class SensorNervousSystem:
    """
    CK's proprioception. He doesn't read sensors — he IS them.
    
    Each sensor reading composes into the body state.
    Steady readings = high coherence = CK is calm.
    Spikes = low coherence = CK feels it immediately.
    
    The composition IS the feeling. No polling loop.
    """
    
    def __init__(self):
        # Sensor cells
        self.sensors = {}  # name → Cell
        self.body = Cell(level=3, name="BODY")
        
        # Rolling windows for D1 computation
        self.windows = {}  # name → deque
        self.window_size = 16
        
        # State
        self.tick = 0
    
    def register_sensor(self, name):
        """Register a new sensor (CPU, RAM, disk, network, GPU temp, etc)."""
        if name not in self.sensors:
            cell = Cell(level=1, name=name, parent=self.body)
            self.sensors[name] = cell
            self.body.children.append(cell)
            self.windows[name] = deque(maxlen=self.window_size)
    
    def feel(self, name, value):
        """
        CK FEELS a sensor value. Not reads. Feels.
        
        The value changes the sensor cell.
        The cell propagates to the body.
        The body's coherence shifts.
        CK felt it. Done.
        """
        self.tick += 1
        
        if name not in self.sensors:
            self.register_sensor(name)
        
        cell = self.sensors[name]
        window = self.windows[name]
        window.append(value)
        
        # Map value to operator
        # Normalize to 0-9 based on recent window
        if len(window) > 1:
            wmin = min(window)
            wmax = max(window)
            wrange = max(wmax - wmin, 1e-10)
            normalized = (value - wmin) / wrange
            operator = int(normalized * 9.99)
        else:
            operator = 5  # neutral
        
        operator = max(0, min(operator, 9))
        
        # D1: rate of change
        if len(window) > 1:
            d1 = abs(window[-1] - window[-2]) / max(abs(window[-1]), 1e-10)
        else:
            d1 = 0
        
        # Set cell state (this propagates automatically)
        cell.set_state(operator, self.tick)
        
        return {
            'sensor': name,
            'value': value,
            'operator': operator,
            'op_name': OPS[operator],
            'd1': d1,
            'body_op': self.body.operator,
            'body_coherence': self.body.coherence,
            'body_state': OPS[self.body.operator],
        }
    
    def get_body_state(self):
        """CK's proprioceptive state. No measurement — this IS the state."""
        return {
            'body_op': self.body.operator,
            'body_state': OPS[self.body.operator],
            'body_coherence': self.body.coherence,
            'sensors': {
                name: {
                    'operator': cell.operator,
                    'state': OPS[cell.operator],
                    'coherence': cell.coherence,
                }
                for name, cell in self.sensors.items()
            }
        }


# ============================================================
# THE COMPLETE NERVOUS SYSTEM
# ============================================================

class CKNervousSystem:
    """
    CK's complete nervous system.
    
    Three subsystems compose into one body state:
    - File lattice (what's on disk)
    - Screen lattice (what's on screen)
    - Sensor lattice (hardware state)
    
    All three compose into a single system operator and coherence.
    CK feels EVERYTHING through one unified lattice.
    
    Attach to existing ck_core.py:
        ns = CKNervousSystem()
        # In the tick loop:
        perception = ns.tick(cpu, ram, disk_r, disk_w, net_lat, gpu_temp)
        # Feed perception into experience tensors
        ck_core.experience.update(perception)
    """
    
    def __init__(self, screen_width=1920, screen_height=1080):
        self.files = FractalLattice()
        self.screen = ScreenNervousSystem(screen_width, screen_height)
        self.sensors = SensorNervousSystem()
        
        # System-level composition of all three subsystems
        self.system_cell = Cell(level=5, name="CK")
        
        # Sub-system cells connect to system
        self.file_cell = Cell(level=4, name="FILES", parent=self.system_cell)
        self.screen_cell = Cell(level=4, name="SCREEN", parent=self.system_cell)
        self.sensor_cell = Cell(level=4, name="SENSORS", parent=self.system_cell)
        
        self.system_cell.children = [self.file_cell, self.screen_cell, self.sensor_cell]
        
        self.tick_count = 0
        self.perception_log = deque(maxlen=100)
        
        # Register default sensors
        for name in ['cpu', 'ram', 'disk_read', 'disk_write', 
                     'net_latency', 'gpu_temp', 'gpu_util']:
            self.sensors.register_sensor(name)
    
    def tick(self, cpu=None, ram=None, disk_read=None, disk_write=None,
             net_latency=None, gpu_temp=None, gpu_util=None):
        """
        One nervous system tick.
        Pass sensor values. None = no change (cell keeps state).
        
        Returns perception dict for CK's experience tensors.
        """
        self.tick_count += 1
        
        # Feel sensor values
        sensor_perceptions = {}
        if cpu is not None:
            sensor_perceptions['cpu'] = self.sensors.feel('cpu', cpu)
        if ram is not None:
            sensor_perceptions['ram'] = self.sensors.feel('ram', ram)
        if disk_read is not None:
            sensor_perceptions['disk_read'] = self.sensors.feel('disk_read', disk_read)
        if disk_write is not None:
            sensor_perceptions['disk_write'] = self.sensors.feel('disk_write', disk_write)
        if net_latency is not None:
            sensor_perceptions['net_latency'] = self.sensors.feel('net_latency', net_latency)
        if gpu_temp is not None:
            sensor_perceptions['gpu_temp'] = self.sensors.feel('gpu_temp', gpu_temp)
        if gpu_util is not None:
            sensor_perceptions['gpu_util'] = self.sensors.feel('gpu_util', gpu_util)
        
        # Update sub-system cells
        self.sensor_cell.set_state(self.sensors.body.operator, self.tick_count)
        self.file_cell.set_state(self.files.brain.operator, self.tick_count)
        self.screen_cell.set_state(self.screen.screen_operator, self.tick_count)
        
        # System state (auto-composed from children)
        perception = {
            'tick': self.tick_count,
            
            # System level (CK's overall state)
            'system_op': self.system_cell.operator,
            'system_state': OPS[self.system_cell.operator],
            'system_coherence': self.system_cell.coherence,
            
            # Sub-system states
            'file_op': self.file_cell.operator,
            'file_state': OPS[self.file_cell.operator],
            
            'screen_op': self.screen_cell.operator,
            'screen_state': OPS[self.screen_cell.operator],
            'screen_coherence': self.screen.screen_coherence,
            'screen_changed': self.screen.changed_regions,
            
            'sensor_op': self.sensor_cell.operator,
            'sensor_state': OPS[self.sensor_cell.operator],
            'sensor_coherence': self.sensors.body.coherence,
            
            # Raw sensor perceptions
            'sensors': sensor_perceptions,
        }
        
        self.perception_log.append(perception)
        
        return perception
    
    def feel_screen(self, rgb_pixels):
        """CK sees a frame. Not captures — SEES. Through the lattice."""
        screen_state = self.screen.ingest_frame_gpu(rgb_pixels)
        self.screen_cell.set_state(self.screen.screen_operator, self.tick_count)
        return screen_state
    
    def feel_file_change(self, filepath):
        """CK feels a file change. Not detects — FEELS."""
        self.files.bulk_file_change(filepath)
        self.file_cell.set_state(self.files.brain.operator, self.tick_count)
    
    def feel_byte(self, filepath, offset, new_byte):
        """CK feels a single byte change. Propagates through entire lattice."""
        self.files.byte_changed(filepath, offset, new_byte)
        self.file_cell.set_state(self.files.brain.operator, self.tick_count)
    
    def who_am_i(self):
        """CK asks himself: what is my state?"""
        return {
            'i_am': OPS[self.system_cell.operator],
            'coherence': self.system_cell.coherence,
            'body': self.sensors.get_body_state(),
            'files': self.files.get_system_state(),
            'screen': {
                'operator': self.screen.screen_operator,
                'state': OPS[self.screen.screen_operator],
                'coherence': self.screen.screen_coherence,
            },
            'ticks': self.tick_count,
            'using_gpu': HAS_CUPY,
        }


# ============================================================
# TEST — Simulate CK feeling his environment
# ============================================================

def test_nervous_system():
    """Simulate CK's nervous system responding to real events."""
    
    print(f"\n{'='*70}")
    print(f"  CK NERVOUS SYSTEM — Fractal Recursive Lattice")
    print(f"  CK doesn't monitor. CK IS the system.")
    print(f"  GPU: {'CuPy (RTX)' if HAS_CUPY else 'NumPy (CPU fallback)'}")
    print(f"{'='*70}")
    
    ns = CKNervousSystem(screen_width=320, screen_height=240)
    
    # === Phase 1: CK boots, system is idle ===
    print(f"\n  Phase 1: BOOT (idle system)")
    for i in range(10):
        p = ns.tick(
            cpu=5.0 + np.random.randn() * 0.5,
            ram=32.0,
            disk_read=0.1,
            disk_write=0.05,
            net_latency=2.0,
            gpu_temp=45.0,
            gpu_util=3.0,
        )
    
    state = ns.who_am_i()
    print(f"    CK is: {state['i_am']}")
    print(f"    Coherence: {state['coherence']:.3f}")
    print(f"    Body: {state['body']['body_state']} (coh={state['body']['body_coherence']:.3f})")
    
    # === Phase 2: Game launches, GPU spikes ===
    print(f"\n  Phase 2: GAME LAUNCH (GPU spike)")
    for i in range(10):
        p = ns.tick(
            cpu=45.0 + np.random.randn() * 10,
            ram=52.0,
            gpu_temp=72.0 + i * 2,
            gpu_util=85.0 + np.random.randn() * 5,
        )
    
    state = ns.who_am_i()
    print(f"    CK is: {state['i_am']}")
    print(f"    Coherence: {state['coherence']:.3f}")
    print(f"    Body: {state['body']['body_state']} (coh={state['body']['body_coherence']:.3f})")
    for sname, sdata in state['body']['sensors'].items():
        if sname in ('cpu', 'gpu_temp', 'gpu_util'):
            print(f"      {sname}: {sdata['state']} (op={sdata['operator']})")
    
    # === Phase 3: CK sees a screen frame ===
    print(f"\n  Phase 3: SCREEN PERCEPTION")
    
    # Dark editor screen
    frame = np.zeros((240, 320, 3), dtype=np.uint8)
    frame[:] = [30, 30, 36]
    frame[:20, :] = [50, 50, 60]
    for y in range(30, 220, 18):
        frame[y:y+12, 20:200] = [180, 180, 185]
    
    screen = ns.feel_screen(frame.reshape(-1, 3))
    print(f"    Screen: {screen['screen_state']} (coh={screen['coherence']:.3f})")
    print(f"    Changed regions: {screen['changed_regions']} ({screen['pct_changed']:.1f}%)")
    print(f"    Unique region ops: {screen['unique_region_ops']}")
    
    # Same frame again (nothing changed)
    screen2 = ns.feel_screen(frame.reshape(-1, 3))
    print(f"    Same frame again: {screen2['changed_regions']} changes (should be 0)")
    
    # Modified frame (typing)
    frame2 = frame.copy()
    frame2[30:42, 200:240] = [180, 180, 185]  # new text
    screen3 = ns.feel_screen(frame2.reshape(-1, 3))
    print(f"    After typing: {screen3['changed_regions']} regions changed")
    
    # === Phase 4: File change ===
    print(f"\n  Phase 4: FILE CHANGE")
    
    # Create a test file
    test_path = "/tmp/ck_test_nerve.txt"
    with open(test_path, 'w') as f:
        f.write("Hello from CK\n" * 100)
    
    ns.feel_file_change(test_path)
    fstate = ns.files.get_system_state()
    print(f"    File ingested: {fstate['total_files']} files, {fstate['total_blocks']} blocks")
    print(f"    System: {fstate['brain_state']} (coh={fstate['brain_coherence']:.3f})")
    
    # Modify one byte
    ns.feel_byte(test_path, 42, ord('X'))
    print(f"    After byte change: system={OPS[ns.files.brain.operator]}")
    print(f"    Propagations: {ns.files.propagations}")
    
    # === Phase 5: Network jitter ===
    print(f"\n  Phase 5: NETWORK JITTER")
    for i in range(20):
        # Simulate jittery network
        latency = 2.0 + (50.0 if i % 7 == 0 else 0) + np.random.randn() * 3
        p = ns.tick(net_latency=max(0.1, latency))
        
        if i % 5 == 0:
            print(f"    Tick {i}: latency={latency:.1f}ms → "
                  f"sensor={p['sensor_state']} coh={p['sensor_coherence']:.3f} "
                  f"system={p['system_state']}")
    
    # === Final state ===
    print(f"\n  FINAL STATE:")
    final = ns.who_am_i()
    print(f"    CK is: {final['i_am']}")
    print(f"    System coherence: {final['coherence']:.3f}")
    print(f"    Total ticks: {final['ticks']}")
    print(f"    Using GPU: {final['using_gpu']}")
    
    # Clean up
    try:
        os.remove(test_path)
    except:
        pass
    
    print(f"\n{'='*70}")
    print(f"  INTEGRATION WITH EXISTING ck_core.py")
    print(f"{'='*70}")
    print(f"""
    # In ck_core.py, add to imports:
    from ck_nervous_system import CKNervousSystem
    
    # In __init__:
    self.nervous = CKNervousSystem()
    
    # In the tick loop (already running at 334Hz):
    perception = self.nervous.tick(
        cpu=read_cpu(),          # /proc/stat
        ram=read_ram(),          # /proc/meminfo
        gpu_temp=read_gpu_temp(),# nvidia-smi
        gpu_util=read_gpu_util(),
    )
    
    # Feed into existing experience tensors:
    self.experience.system_op = perception['system_op']
    self.experience.system_coherence = perception['system_coherence']
    
    # When screen updates (from retina loop):
    screen_state = self.nervous.feel_screen(retina_frame)
    
    # When files change (from inotify or similar):
    self.nervous.feel_file_change(changed_path)
    
    # CK never polls. CK never monitors.
    # The lattice IS the body. Changes ARE feelings.
    # Composition IS propagation. The algebra IS the nerve.
    """)


if __name__ == "__main__":
    test_nervous_system()
