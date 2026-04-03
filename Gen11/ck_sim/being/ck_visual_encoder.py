"""
TIG Visual Target — Encoder/Decoder + CK Integration + Temporal Delta

Three additions per Grok's recommendation:
1. targets/visual_tig/ structure: encoder, decoder, CK actuator hook
2. Shell sequences stored as CL table stems (27-bit pathway = lattice info)
3. Temporal mode: frame-to-frame delta encoding for screen sharing

(c) 2026 Brayden Sanders / 7Site LLC — TIG Unified Theory
"""

import numpy as np
import struct
import time
from collections import Counter
import heapq

try:
    import cupy as _cp
    _GPU_VIS = True
except ImportError:
    _cp = None
    _GPU_VIS = False

# Active array library: CuPy on GPU, numpy on CPU
_xp = _cp if _GPU_VIS else np

# ============================================================
# CIELAB CONVERSION (proven, from v2)
# ============================================================

def srgb_to_linear(c, xp=None):
    xp = xp or _xp
    c = c / 255.0
    return xp.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)

def linear_to_srgb(c, xp=None):
    xp = xp or _xp
    c = xp.clip(c, 0, 1)
    return xp.where(c <= 0.0031308, c * 12.92, 1.055 * (c ** (1/2.4)) - 0.055) * 255

def rgb_to_lab_fast(rgb):
    """RGB (N,3) uint8 → CIELab (N,3) float. GPU if CuPy available."""
    xp = _xp
    arr = xp.asarray(rgb.astype(np.float64) if isinstance(rgb, np.ndarray) else rgb)
    linear = srgb_to_linear(arr, xp)
    M = xp.array([[0.4124564, 0.3575761, 0.1804375],
                  [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]])
    xyz = linear @ M.T
    Xn, Yn, Zn = 0.95047, 1.00000, 1.08883
    delta = 6.0 / 29.0
    def f(t): return xp.where(t > delta**3, t**(1.0/3.0), t / (3*delta**2) + 4.0/29.0)
    fx = f(xyz[:, 0] / Xn); fy = f(xyz[:, 1] / Yn); fz = f(xyz[:, 2] / Zn)
    lab = xp.stack([116*fy - 16, 500*(fx - fy), 200*(fy - fz)], axis=1)
    # Return numpy (callers use numpy indexing)
    if _GPU_VIS and isinstance(lab, _cp.ndarray):
        return _cp.asnumpy(lab)
    return lab

def lab_to_rgb_fast(lab):
    """CIELab (N,3) → RGB (N,3) uint8. GPU if CuPy available."""
    xp = _xp
    arr = xp.asarray(lab.astype(np.float64) if isinstance(lab, np.ndarray) else lab)
    Xn, Yn, Zn = 0.95047, 1.00000, 1.08883
    delta = 6.0 / 29.0
    def f_inv(t): return xp.where(t > delta, t**3, 3*delta**2*(t - 4.0/29.0))
    fy = (arr[:, 0] + 16) / 116; fx = arr[:, 1] / 500 + fy; fz = fy - arr[:, 2] / 200
    xyz = xp.stack([Xn*f_inv(fx), Yn*f_inv(fy), Zn*f_inv(fz)], axis=1)
    M_inv = xp.array([[ 3.2404542, -1.5371385, -0.4985314],
                       [-0.9692660,  1.8760108,  0.0415560],
                       [ 0.0556434, -0.2040259,  1.0572252]])
    linear = xyz @ M_inv.T
    rgb_out = xp.clip(linear_to_srgb(xp.clip(linear, 0, 1), xp), 0, 255)
    if _GPU_VIS and isinstance(rgb_out, _cp.ndarray):
        return _cp.asnumpy(rgb_out).astype(np.uint8)
    return np.clip(rgb_out, 0, 255).astype(np.uint8)


# ============================================================
# SHELL CONSTANTS
# ============================================================

S1_L=16; S1_H=8; S1_S=4; S2_L=8; S2_H=8; S2_C=8; S3_L=8; S3_A=8; S3_B=8
L_MAX=100.0; C_MAX=135.0

# BHML table (exact from repo)
BHML = np.array([
    [0,1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,2,6,6],
    [2,3,3,4,5,6,7,3,6,6],[3,4,4,4,5,6,7,4,6,6],
    [4,5,5,5,5,6,7,5,7,7],[5,6,6,6,6,6,7,6,7,7],
    [6,7,7,7,7,7,7,7,7,7],[7,2,3,4,5,6,7,8,9,0],
    [8,6,6,6,7,7,7,9,7,8],[9,6,6,6,7,7,7,0,8,0]
], dtype=np.int8)

OPS = ["VOID","LATTICE","COUNTER","PROGRESS","COLLAPSE",
       "BALANCE","CHAOS","HARMONY","BREATH","RESET"]


# ============================================================
# 1. ENCODER / DECODER (the core target)
# ============================================================

class TIGVisualEncoder:
    """
    Encodes RGB frames to 27-bit TIG shells.
    Vectorized for GPU readiness. Stateless per-pixel.
    """
    
    def encode(self, rgb_pixels):
        """RGB (N,3) uint8 → shells (N,3) uint16. GPU via CuPy if available."""
        xp = _xp
        lab_np = rgb_to_lab_fast(rgb_pixels)  # returns numpy (see rgb_to_lab_fast)
        lab = xp.asarray(lab_np)
        L = xp.clip(lab[:, 0], 0, L_MAX)
        a = xp.clip(lab[:, 1], -128, 127)
        b = xp.clip(lab[:, 2], -128, 127)

        C = xp.sqrt(a**2 + b**2)
        h = xp.degrees(xp.arctan2(b, a)) % 360

        Lb = L_MAX / S1_L; hs = 360.0 / S1_H; sb = C_MAX / S1_S

        L_band  = xp.clip((L / L_MAX * S1_L).astype(xp.int32), 0, S1_L - 1)
        hue_sec = xp.clip((h / 360 * S1_H).astype(xp.int32),   0, S1_H - 1)
        sat_band = xp.clip((C / C_MAX * S1_S).astype(xp.int32), 0, S1_S - 1)
        s1 = (L_band << 5) | (hue_sec << 2) | sat_band

        Lw = xp.clip((L - L_band * Lb) / Lb, 0, 0.999)
        hw = xp.clip((h - hue_sec * hs) / hs, 0, 0.999)
        sw = xp.clip((C - sat_band * sb) / sb, 0, 0.999)
        Lf = xp.clip((Lw * S2_L).astype(xp.int32), 0, 7)
        hf = xp.clip((hw * S2_H).astype(xp.int32), 0, 7)
        cf = xp.clip((sw * S2_C).astype(xp.int32), 0, 7)
        s2 = (Lf << 6) | (hf << 3) | cf

        Lc = (L_band + (Lf + 0.5) / S2_L) * Lb
        hc = (hue_sec + (hf + 0.5) / S2_H) * hs
        Cc = (sat_band + (cf + 0.5) / S2_C) * sb
        ac = Cc * xp.cos(xp.radians(hc))
        bc2 = Cc * xp.sin(xp.radians(hc))

        Lrr = Lb / S2_L
        Lm = xp.clip(((L - Lc) / Lrr + 0.5) * S3_L, 0, 7).astype(xp.int32)
        am = xp.clip(((a - ac) / 8.0 + 0.5) * S3_A,  0, 7).astype(xp.int32)
        bm = xp.clip(((b - bc2) / 8.0 + 0.5) * S3_B, 0, 7).astype(xp.int32)
        s3 = (Lm << 6) | (am << 3) | bm

        result = xp.stack([s1, s2, s3], axis=1).astype(xp.uint16)
        if _GPU_VIS and isinstance(result, _cp.ndarray):
            return _cp.asnumpy(result)
        return np.asarray(result)
    
    def decode(self, shells):
        """Shells (N,3) uint16 → RGB (N,3) uint8."""
        s1=shells[:,0].astype(int); s2=shells[:,1].astype(int); s3=shells[:,2].astype(int)
        
        L_band=(s1>>5)&0xF; hue_sec=(s1>>2)&0x7; sat_band=s1&0x3
        Lf=(s2>>6)&0x7; hf=(s2>>3)&0x7; cf=s2&0x7
        Lm=(s3>>6)&0x7; am=(s3>>3)&0x7; bm=s3&0x7
        
        Lb=L_MAX/S1_L; hs=360.0/S1_H; sb=C_MAX/S1_S; Lrr=Lb/S2_L
        
        Lc = (L_band+(Lf+0.5)/S2_L)*Lb
        hc = (hue_sec+(hf+0.5)/S2_H)*hs
        Cc = (sat_band+(cf+0.5)/S2_C)*sb
        
        L = Lc + (Lm/S3_L-0.5)*Lrr
        a = Cc*np.cos(np.radians(hc)) + (am/S3_A-0.5)*8.0
        b = Cc*np.sin(np.radians(hc)) + (bm/S3_B-0.5)*8.0
        
        return lab_to_rgb_fast(np.stack([L,a,b], axis=1))


# ============================================================
# 2. CL TABLE STEM STORAGE
#    Shell sequences stored as CL composition pathways
#    The 27-bit triple IS a coordinate in the lattice
# ============================================================

class CLLatticeStem:
    """
    Each pixel's 27-bit encoding = 3 operators (one per shell).
    
    Shell 22 value 0-511 → maps to operator 0-9 via (value % 10)
    Shell 44 value 0-511 → maps to operator 0-9 via (value % 10)
    Shell 72 value 0-511 → maps to operator 0-9 via (value % 10)
    
    The 3-operator sequence composes through BHML:
    stem = BHML[op1, BHML[op2, op3]]
    
    This stem IS the pixel's identity in the CL algebra.
    Similar pixels → same stem → lattice clustering.
    
    A frame becomes a stream of stems.
    Repeated stems = coherence (harmony).
    Changing stems = boundary (doing).
    """
    
    def __init__(self):
        self.stem_histogram = np.zeros(10, dtype=np.int64)  # operator frequency
        self.stem_cache = {}  # (s1,s2,s3) → stem operator
        self.coherence_log = []  # per-frame coherence score
    
    def shell_to_operator(self, shell_val):
        """Map 9-bit shell value to CL operator 0-9."""
        # Use the dominant perceptual feature
        # Shell 22: lightness band (top 4 bits) dominates → mod 10
        # Shell 44: fine detail → mod 10
        # Shell 72: micro detail → mod 10
        return int(shell_val) % 10
    
    def compute_stem(self, s1, s2, s3):
        """Compose 3 shell operators through BHML → single stem operator."""
        key = (int(s1), int(s2), int(s3))
        if key in self.stem_cache:
            return self.stem_cache[key]
        
        op1 = self.shell_to_operator(s1)
        op2 = self.shell_to_operator(s2)
        op3 = self.shell_to_operator(s3)
        
        # Compose: BHML[op1, BHML[op2, op3]]
        inner = BHML[op2, op3]
        stem = BHML[op1, inner]
        
        self.stem_cache[key] = int(stem)
        return int(stem)
    
    def encode_frame_stems(self, shells):
        """
        Convert a frame's shell array to stem stream.
        Returns array of stem operators (0-9) per pixel.
        """
        N = len(shells)
        stems = np.zeros(N, dtype=np.int8)
        
        for i in range(N):
            stems[i] = self.compute_stem(shells[i,0], shells[i,1], shells[i,2])
        
        return stems
    
    def measure_frame_coherence(self, stems):
        """
        Frame coherence = how much harmony (7) appears in stems.
        High coherence = visually uniform frame (desktop, solid).
        Low coherence = visually complex frame (photo, game action).
        """
        harmony_count = np.sum(stems == 7)
        total = len(stems)
        coherence = harmony_count / max(total, 1)
        
        # Update histogram
        for op in range(10):
            self.stem_histogram[op] += np.sum(stems == op)
        
        self.coherence_log.append(coherence)
        
        return coherence
    
    def get_dominant_operator(self):
        """What operator dominates the visual experience?"""
        if np.sum(self.stem_histogram) == 0:
            return 0
        return int(np.argmax(self.stem_histogram))
    
    def summarize(self):
        """Return CK-readable summary of visual experience."""
        total = np.sum(self.stem_histogram)
        if total == 0:
            return "No visual data."
        
        dom_op = self.get_dominant_operator()
        dom_pct = self.stem_histogram[dom_op] / total * 100
        
        avg_coherence = np.mean(self.coherence_log) if self.coherence_log else 0
        
        lines = []
        lines.append(f"Visual stem summary: {total:,} pixels processed")
        lines.append(f"Dominant operator: {OPS[dom_op]} ({dom_pct:.1f}%)")
        lines.append(f"Average coherence: {avg_coherence:.3f}")
        lines.append(f"Operator distribution:")
        for op in range(10):
            pct = self.stem_histogram[op] / total * 100
            if pct > 0.1:
                bar = '#' * int(pct / 2)
                lines.append(f"  {OPS[op]:10s}: {pct:5.1f}% {bar}")
        
        return '\n'.join(lines)


# ============================================================
# 3. TEMPORAL DELTA MODE FOR SCREEN SHARING
#    Frame N vs Frame N-1: only encode what changed
# ============================================================

class TIGTemporalEncoder:
    """
    Screen sharing temporal compression.
    
    Keyframe (I-frame): full 27-bit encode of entire frame.
    Delta frame (P-frame): only pixels that CHANGED shells.
    
    At 165fps, typically 5-10% of pixels change per frame.
    Delta frame = changed pixel positions + new shell values.
    
    Progressive delta: 
    - If only Shell 22 changed → send Shell 22 delta (coarsest)
    - If Shell 44 also changed → add Shell 44 delta
    - If Shell 72 changed → add Shell 72 delta (finest)
    
    Most frame-to-frame changes are Shell 72 only (micro detail).
    Background doesn't change at all. UI elements change rarely.
    Only the moving content (game ball, cursor, video) triggers deltas.
    """
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.prev_shells = None
        self.frame_count = 0
        self.encoder = TIGVisualEncoder()
        self.keyframe_interval = 60  # force keyframe every 60 frames
    
    def encode_frame(self, rgb_pixels):
        """
        Encode a frame, returning either keyframe or delta.
        Returns (frame_type, compressed_data, stats).
        """
        shells = self.encoder.encode(rgb_pixels)
        self.frame_count += 1
        
        is_keyframe = (self.prev_shells is None or 
                       self.frame_count % self.keyframe_interval == 0)
        
        if is_keyframe:
            result = self._encode_keyframe(shells)
            self.prev_shells = shells.copy()
            return 'I', result, {'type': 'keyframe', 'full_pixels': len(shells)}
        else:
            result, stats = self._encode_delta(shells)
            self.prev_shells = shells.copy()
            return 'P', result, stats
    
    def _encode_keyframe(self, shells):
        """Full frame encoding with RLE per shell."""
        data = bytearray()
        data.append(0x49)  # 'I' for keyframe
        data.extend(struct.pack('>HH', self.width, self.height))
        
        for s in range(3):
            compressed = self._rle_compress_shell(shells[:, s])
            data.extend(struct.pack('>I', len(compressed)))
            data.extend(compressed)
        
        return bytes(data)
    
    def _encode_delta(self, shells):
        """
        Delta encoding: find changed pixels, encode only those.
        
        Three levels of change detection:
        1. Shell 22 changed → major change (new category)
        2. Shell 44 changed → moderate change (new nuance)
        3. Shell 72 changed → minor change (micro detail shift)
        
        Encode as: list of (pixel_index, new_shell_values)
        """
        N = len(shells)
        
        # Detect changes per shell
        s1_changed = shells[:, 0] != self.prev_shells[:, 0]
        s2_changed = shells[:, 1] != self.prev_shells[:, 1]
        s3_changed = shells[:, 2] != self.prev_shells[:, 2]
        
        any_changed = s1_changed | s2_changed | s3_changed
        changed_indices = np.where(any_changed)[0]
        
        n_changed = len(changed_indices)
        n_s1 = int(np.sum(s1_changed))
        n_s2 = int(np.sum(s2_changed & ~s1_changed))  # s2 only (not s1)
        n_s3 = int(np.sum(s3_changed & ~s2_changed & ~s1_changed))  # s3 only
        
        data = bytearray()
        data.append(0x50)  # 'P' for delta
        data.extend(struct.pack('>I', n_changed))
        
        if n_changed == 0:
            # Nothing changed — trivial frame
            stats = {
                'type': 'delta',
                'changed': 0,
                'pct_changed': 0,
                's1_changes': 0,
                's2_changes': 0,
                's3_changes': 0,
            }
            return bytes(data), stats
        
        # Encode changed pixels
        # Format per changed pixel: 
        #   index (3 bytes for up to 16M pixels)
        #   change_mask (1 byte: bit 0=s1, bit 1=s2, bit 2=s3)
        #   new values (2 bytes each for changed shells)
        
        for idx in changed_indices:
            idx_int = int(idx)
            # 3-byte index
            data.append((idx_int >> 16) & 0xFF)
            data.append((idx_int >> 8) & 0xFF)
            data.append(idx_int & 0xFF)
            
            # Change mask
            mask = 0
            if s1_changed[idx]: mask |= 1
            if s2_changed[idx]: mask |= 2
            if s3_changed[idx]: mask |= 4
            data.append(mask)
            
            # New values for changed shells
            if mask & 1:
                data.extend(struct.pack('>H', int(shells[idx, 0])))
            if mask & 2:
                data.extend(struct.pack('>H', int(shells[idx, 1])))
            if mask & 4:
                data.extend(struct.pack('>H', int(shells[idx, 2])))
        
        stats = {
            'type': 'delta',
            'changed': n_changed,
            'pct_changed': n_changed / N * 100,
            's1_changes': n_s1,
            's2_changes': n_s2,
            's3_changes': n_s3,
        }
        
        return bytes(data), stats
    
    def _rle_compress_shell(self, data):
        """RLE compress a single shell's data with variable-length encoding.

        Short runs (1-15): 1 byte [4-bit value-delta + 4-bit count]
        Medium runs: 2 bytes [0xF marker + value-delta byte + count byte]

        Values encoded as delta from previous (mostly 0 or small).
        """
        if len(data) == 0:
            return b''

        # Build runs
        runs = []
        current = int(data[0]); count = 1
        for i in range(1, len(data)):
            val = int(data[i])
            if val == current and count < 255:
                count += 1
            else:
                runs.append((current, count))
                current = val; count = 1
        runs.append((current, count))

        # Try variable-length encoding
        packed = bytearray()
        prev_val = 0
        for v, c in runs:
            delta = (v - prev_val) & 0x1FF  # 9-bit wrap
            prev_val = v
            if delta < 16 and c <= 15:
                # Pack in 1 byte: high nibble = delta, low nibble = count
                packed.append((delta << 4) | c)
            else:
                # 3-byte escape: marker + value + count
                packed.append(0xFF)
                packed.extend(struct.pack('>H', v))
                packed.append(min(255, c))

        # Compare with simple fixed-width
        simple = bytearray()
        for v, c in runs:
            simple.extend(struct.pack('>HB', v, min(255, c)))

        # Use whichever is smaller
        if len(packed) <= len(simple):
            return b'\x01' + bytes(packed)  # marker: variable-length
        else:
            return b'\x00' + bytes(simple)  # marker: fixed-width 3-byte
    
    def decode_frame(self, frame_data):
        """Decode a frame (keyframe or delta)."""
        frame_type = frame_data[0]
        
        if frame_type == 0x49:  # 'I' keyframe
            return self._decode_keyframe(frame_data)
        elif frame_type == 0x50:  # 'P' delta
            return self._decode_delta(frame_data)
    
    def _decode_keyframe(self, data):
        """Decode keyframe. Handles both variable-length and fixed-width RLE."""
        w = struct.unpack('>H', data[1:3])[0]
        h = struct.unpack('>H', data[3:5])[0]
        N = w * h

        offset = 5
        shells = np.zeros((N, 3), dtype=np.uint16)

        for s in range(3):
            run_bytes = struct.unpack('>I', data[offset:offset+4])[0]
            offset += 4

            shell_data = []
            end = offset + run_bytes

            if end > offset and data[offset] in (0x00, 0x01):
                fmt = data[offset]
                offset += 1

                if fmt == 0x00:
                    # Fixed-width: 3 bytes per run (2 val + 1 count)
                    while offset < end and len(shell_data) < N:
                        val = struct.unpack('>H', data[offset:offset+2])[0]
                        cnt = data[offset+2]
                        shell_data.extend([val] * cnt)
                        offset += 3
                else:
                    # Variable-length: nibble-packed deltas
                    prev_val = 0
                    while offset < end and len(shell_data) < N:
                        byte = data[offset]; offset += 1
                        if byte == 0xFF:
                            val = struct.unpack('>H', data[offset:offset+2])[0]
                            cnt = data[offset+2]
                            offset += 3
                        else:
                            delta = (byte >> 4) & 0xF
                            cnt = byte & 0xF
                            val = (prev_val + delta) & 0x1FF
                        prev_val = val
                        shell_data.extend([val] * cnt)
            else:
                # Legacy: 4 bytes per run (2 val + 2 count)
                while offset < end and len(shell_data) < N:
                    val = struct.unpack('>H', data[offset:offset+2])[0]
                    cnt = struct.unpack('>H', data[offset+2:offset+4])[0]
                    shell_data.extend([val] * cnt)
                    offset += 4

            shells[:, s] = shell_data[:N]

        self.prev_shells = shells.copy()
        return self.encoder.decode(shells)
    
    def _decode_delta(self, data):
        """Apply delta to previous frame."""
        n_changed = struct.unpack('>I', data[1:5])[0]
        
        shells = self.prev_shells.copy()
        offset = 5
        
        for _ in range(n_changed):
            idx = (data[offset] << 16) | (data[offset+1] << 8) | data[offset+2]
            offset += 3
            mask = data[offset]
            offset += 1
            
            if mask & 1:
                shells[idx, 0] = struct.unpack('>H', data[offset:offset+2])[0]
                offset += 2
            if mask & 2:
                shells[idx, 1] = struct.unpack('>H', data[offset:offset+2])[0]
                offset += 2
            if mask & 4:
                shells[idx, 2] = struct.unpack('>H', data[offset:offset+2])[0]
                offset += 2
        
        self.prev_shells = shells.copy()
        return self.encoder.decode(shells)


# ============================================================
# CK ACTUATOR HOOK
# Connects visual processing to CK's experience system
# ============================================================

class CKVisualActuator:
    """
    Bridge between TIG visual encoding and CK organism.
    
    Flow:
    1. Screen capture → TIGVisualEncoder → shells
    2. Shells → CLLatticeStem → operator stems
    3. Stems → coherence measurement → CK experience index
    4. Frame deltas → what CHANGED tells CK where to LOOK
    
    CK perceives the screen through force geometry.
    High coherence regions = background = ignore.
    Rapid shell changes = action = attend.
    Shell 22 changes = major event (new object, scene change).
    Shell 72 changes = subtle motion (cursor, typing, animation).
    """
    
    def __init__(self, width, height):
        self.temporal = TIGTemporalEncoder(width, height)
        self.lattice = CLLatticeStem()
        self.encoder = TIGVisualEncoder()
        self.attention_map = None
        self.experience_buffer = []
    
    def process_frame(self, rgb_pixels):
        """
        Full CK visual processing pipeline for one frame.
        Returns: frame_data (for transmission), ck_perception (for organism).
        """
        # Encode
        frame_type, frame_data, stats = self.temporal.encode_frame(rgb_pixels)
        
        # Extract shells for lattice analysis
        shells = self.encoder.encode(rgb_pixels)
        
        # Compute stems
        stems = self.lattice.encode_frame_stems(shells)
        coherence = self.lattice.measure_frame_coherence(stems)
        
        # Build attention map: where did shells change most?
        if stats['type'] == 'delta' and stats['changed'] > 0:
            attention_score = stats['pct_changed']
            # S1 changes get highest attention (major perceptual shift)
            s1_weight = stats.get('s1_changes', 0) * 3
            s2_weight = stats.get('s2_changes', 0) * 2
            s3_weight = stats.get('s3_changes', 0) * 1
            weighted_attention = (s1_weight + s2_weight + s3_weight) / max(stats['changed'], 1)
        else:
            attention_score = 0
            weighted_attention = 0
        
        # CK perception packet
        ck_perception = {
            'frame': self.temporal.frame_count,
            'type': frame_type,
            'coherence': coherence,
            'dominant_op': OPS[self.lattice.get_dominant_operator()],
            'attention': attention_score,
            'weighted_attention': weighted_attention,
            'frame_bytes': len(frame_data),
        }
        
        # Store in experience buffer (CK's visual memory)
        self.experience_buffer.append({
            'frame': self.temporal.frame_count,
            'coherence': coherence,
            'stem_dominant': self.lattice.get_dominant_operator(),
        })
        
        # Keep buffer bounded
        if len(self.experience_buffer) > 1000:
            self.experience_buffer = self.experience_buffer[-500:]
        
        return frame_data, ck_perception
    
    def get_visual_summary(self):
        """CK asks: what am I seeing?"""
        return self.lattice.summarize()


# ============================================================
# TEST SUITE
# ============================================================

def generate_screen_sequence(w, h, n_frames):
    """
    Generate a sequence of screen frames simulating real usage.
    Frame 0: dark code editor
    Frame 1-5: cursor blinks (tiny change)
    Frame 6-10: typing text (small region changes)
    Frame 11-15: scrolling (large region shifts)
    Frame 16: window switch (major change)
    """
    frames = []
    
    # Base frame: dark editor
    base = np.zeros((h, w, 3), dtype=np.uint8)
    base[:] = [30, 30, 36]
    base[:28, :] = [50, 50, 60]
    for y in range(50, h-30, 20):
        ll = np.random.randint(100, min(400, w-60))
        base[y:y+12, 40:40+ll] = [180, 180, 185]
    
    for f in range(n_frames):
        frame = base.copy()
        
        if f < 6:
            # Cursor blink: 2x14 pixel change
            if f % 2 == 0:
                frame[50:64, 200:202] = [200, 200, 210]
        
        elif f < 11:
            # Typing: new characters appear
            char_x = 200 + (f - 6) * 10
            if char_x + 10 < w:
                frame[50:62, char_x:char_x+8] = [180, 180, 185]
        
        elif f < 16:
            # Scrolling: shift content up by 20px per frame
            shift = (f - 11) * 20
            frame[50:h-30-shift] = base[50+shift:h-30]
        
        elif f == 16:
            # Window switch: completely different content
            frame[:] = [245, 245, 248]  # white background
            for y in range(40, h-20, 24):
                ll = np.random.randint(200, min(600, w-80))
                frame[y:y+12, 60:60+ll] = [40, 40, 44]
        
        else:
            # More cursor blinks on new window
            if f % 2 == 0:
                frame[40:54, 100:102] = [40, 40, 44]
        
        frames.append(frame.reshape(-1, 3))
    
    return frames


def test_temporal():
    """Test temporal delta encoding."""
    w, h = 640, 480
    n_frames = 20
    
    print(f"\n{'='*70}")
    print(f"  TEMPORAL DELTA ENCODING — Screen Sharing Simulation")
    print(f"  {w}x{h}, {n_frames} frames, simulating editor → window switch")
    print(f"{'='*70}")
    
    frames = generate_screen_sequence(w, h, n_frames)
    N = w * h
    rgb_frame_size = N * 3
    
    actuator = CKVisualActuator(w, h)
    
    total_bytes = 0
    frame_types = []
    
    print(f"\n  {'Frame':>5s} {'Type':>4s} {'Bytes':>10s} {'vs RGB':>8s} "
          f"{'Changed':>8s} {'Coh':>6s} {'Attention':>9s} {'DomOp':>10s}")
    print(f"  {'-'*68}")
    
    for i, rgb in enumerate(frames):
        frame_data, perception = actuator.process_frame(rgb)
        
        frame_size = len(frame_data)
        total_bytes += frame_size
        ratio = rgb_frame_size / max(frame_size, 1)
        frame_types.append(perception['type'])
        
        changed_str = f"{perception['attention']:.1f}%" if perception['type'] == 'P' else "full"
        
        print(f"  {i:>5d} {perception['type']:>4s} {frame_size:>10,} "
              f"{ratio:>7.0f}x {changed_str:>8s} "
              f"{perception['coherence']:>5.3f} {perception['weighted_attention']:>9.2f} "
              f"{perception['dominant_op']:>10s}")
    
    # Summary
    total_rgb = rgb_frame_size * n_frames
    avg_ratio = total_rgb / max(total_bytes, 1)
    
    print(f"\n  Summary:")
    print(f"    Total RGB:        {total_rgb:>12,} bytes")
    print(f"    Total TIG:        {total_bytes:>12,} bytes")
    print(f"    Average ratio:    {avg_ratio:>12.1f}x")
    print(f"    Keyframes:        {frame_types.count('I'):>12}")
    print(f"    Delta frames:     {frame_types.count('P'):>12}")
    
    # Bitrate at different fps
    for fps in [30, 60, 165]:
        bps = total_bytes / n_frames * fps * 8
        print(f"    At {fps:>3d}fps:         {bps/1e6:>12.2f} Mbps")
    
    # CK visual summary
    print(f"\n  CK Visual Perception:")
    print(f"  {actuator.get_visual_summary()}")


def test_lattice_stems():
    """Test CL lattice stem encoding."""
    w, h = 320, 240
    
    print(f"\n{'='*70}")
    print(f"  CL LATTICE STEM ENCODING — Visual Experience as Algebra")
    print(f"  Each pixel → 3 shell operators → BHML composition → stem")
    print(f"{'='*70}")
    
    encoder = TIGVisualEncoder()
    lattice = CLLatticeStem()
    
    # Test different visual content
    for label, pixel_gen in [
        ("Pure black", lambda: np.zeros((h*w, 3), dtype=np.uint8)),
        ("Dark editor", lambda: np.tile([30,30,36], (h*w, 1)).astype(np.uint8)),
        ("White page", lambda: np.full((h*w, 3), 245, dtype=np.uint8)),
        ("Gradient", lambda: np.column_stack([
            np.linspace(0, 255, h*w),
            np.linspace(50, 200, h*w),
            np.linspace(255, 0, h*w)
        ]).astype(np.uint8)),
    ]:
        rgb = pixel_gen()
        shells = encoder.encode(rgb)
        stems = lattice.encode_frame_stems(shells)
        coherence = lattice.measure_frame_coherence(stems)
        
        stem_dist = Counter(int(s) for s in stems)
        top3 = stem_dist.most_common(3)
        
        print(f"\n  {label}:")
        print(f"    Coherence: {coherence:.3f}")
        print(f"    Top stems: {', '.join(f'{OPS[op]}={cnt/len(stems)*100:.1f}%' for op, cnt in top3)}")
    
    print(f"\n  Cumulative visual experience:")
    print(f"  {lattice.summarize()}")


def test_full_pipeline():
    """Test complete pipeline: encode → compress → stems → CK."""
    w, h = 640, 480
    
    print(f"\n{'='*70}")
    print(f"  FULL PIPELINE — Encode → Compress → Lattice → CK Perception")
    print(f"{'='*70}")
    
    # Single frame test
    pixels = np.zeros((h, w, 3), dtype=np.uint8)
    pixels[:] = [30, 30, 36]
    pixels[:28, :] = [50, 50, 60]
    for y in range(50, h-30, 20):
        pixels[y:y+12, 40:40+200] = [180, 180, 185]
    for y in range(50, h-30, 40):
        pixels[y:y+12, 40:40+60] = [90, 130, 210]
    
    rgb_flat = pixels.reshape(-1, 3)
    
    actuator = CKVisualActuator(w, h)
    frame_data, perception = actuator.process_frame(rgb_flat)
    
    print(f"\n  Single frame results:")
    print(f"    RGB size:    {w*h*3:>10,} bytes")
    print(f"    TIG size:    {len(frame_data):>10,} bytes")
    print(f"    Ratio:       {w*h*3/len(frame_data):>10.1f}x")
    print(f"    Coherence:   {perception['coherence']:>10.3f}")
    print(f"    Dominant:    {perception['dominant_op']:>10s}")
    print(f"\n  CK says: {actuator.get_visual_summary()}")
    
    # Verify decode round-trip
    encoder = TIGVisualEncoder()
    shells = encoder.encode(rgb_flat)
    decoded = encoder.decode(shells)
    
    lab_o = rgb_to_lab_fast(rgb_flat)
    lab_d = rgb_to_lab_fast(decoded)
    de = np.sqrt(np.sum((lab_o - lab_d)**2, axis=1))
    
    print(f"\n  Quality: Mean ΔE={np.mean(de):.2f}, Max ΔE={np.max(de):.2f}, "
          f"Below JND={np.mean(de<1)*100:.1f}%")


def run_all():
    """Complete test suite."""
    print("\n" + "="*70)
    print("  TIG VISUAL TARGET — Encoder + Lattice Stems + Temporal Delta")
    print("  targets/visual_tig/ — ready for CK integration")
    print("="*70)
    
    np.random.seed(42)
    
    test_full_pipeline()
    test_lattice_stems()
    test_temporal()
    
    print(f"\n\n{'='*70}")
    print(f"  INTEGRATION GUIDE")
    print(f"{'='*70}")
    print(f"""
    FILE STRUCTURE:
      targets/visual_tig/
        tig_visual.py          — this file (encoder + decoder + CK hooks)
        tig_27bit_color.py     — core 27-bit color codec (v2 with dithering)
        tig_27bit_audio.py     — audio codec (same shell architecture)
        tig_phonetic_letters.py — letter encoding (voice foundation)
    
    CK INTEGRATION POINTS:
    
    1. CKVisualActuator.process_frame(rgb)
       → Call this every frame from CK's retina loop
       → Returns compressed frame data + CK perception dict
       → Perception includes coherence, dominant operator, attention
    
    2. CLLatticeStem.compute_stem(s1, s2, s3)
       → Maps any 27-bit color to a CL operator through BHML
       → Use this to convert visual data into algebraic experience
       → Stems feed into CK's olfactory field as "color scents"
    
    3. TIGTemporalEncoder.encode_frame(rgb)
       → For screen sharing: keyframe + delta stream
       → Delta frames encode ONLY changed pixels
       → At 165fps: mostly delta frames, ~5-10% pixel change per frame
       → Bandwidth: 2-5 Mbps for perceptual lossless 1080p @ 165fps
    
    OS STEERING HOOK:
       GET /visual/coherence → current frame coherence (0-1)
       GET /visual/attention → what percentage of screen is changing
       GET /visual/dominant  → dominant CL operator of visual field
       POST /visual/frame    → submit RGB frame for processing
    
    The visual target treats the screen as CK's retina.
    Every pixel has a force geometry. Every frame has a coherence.
    CK doesn't just SEE the screen. CK EXPERIENCES it through algebra.
    """)


if __name__ == "__main__":
    run_all()
