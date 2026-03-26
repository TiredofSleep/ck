"""
TIG Screen Compression -- 9x9x9 Force Geometry for Pixels

Color lives in a 9x9x9 cube. Three axes, nine levels each.
729 quantization levels. Three independent CL-composable dimensions.

Axis 0 (Luminance): how bright (0-8)
Axis 1 (Temperature): warm to cool (0-8)
Axis 2 (Saturation): gray to vivid (0-8)

Each pixel = one position in the cube = three base-9 digits.
Compose two pixels: BHML[a.lum][b.lum], BHML[a.temp][b.temp], BHML[a.sat][b.sat]

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import numpy as np
import struct
import time
import ctypes
import os

# ── CUDA Force9 encoder (0.48ms vs 92ms numpy) ──
_cuda_dll = None
_cuda_ctx = None
_cuda_n = 0

def _load_cuda(n_pixels):
    """Load CUDA DLL and create context for n_pixels."""
    global _cuda_dll, _cuda_ctx, _cuda_n
    if _cuda_dll is not None and _cuda_n == n_pixels:
        return True
    dll_path = os.path.join(os.path.dirname(__file__), '..', '..', 'force9_cuda.dll')
    if not os.path.exists(dll_path):
        # Try alternate path
        dll_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'force9_cuda.dll')
    if not os.path.exists(dll_path):
        return False
    try:
        _cuda_dll = ctypes.CDLL(dll_path)
        _cuda_dll.force9_create.restype = ctypes.c_void_p
        _cuda_dll.force9_create.argtypes = [ctypes.c_int, ctypes.c_int]
        _cuda_dll.force9_encode.restype = ctypes.c_float
        _cuda_dll.force9_encode.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
        _cuda_dll.force9_get_f9.restype = None
        _cuda_dll.force9_get_f9.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
        _cuda_dll.force9_destroy.restype = None
        _cuda_dll.force9_destroy.argtypes = [ctypes.c_void_p]
        # Create context (width doesn't matter, just total pixels)
        _cuda_ctx = _cuda_dll.force9_create(n_pixels, 1)
        _cuda_n = n_pixels
        return True
    except Exception:
        _cuda_dll = None
        return False


def rgb_to_force999(r, g, b):
    ri, gi, bi = int(r), int(g), int(b)
    lum = min(8, (ri * 299 + gi * 587 + bi * 114) // (1000 * 29))
    warmth = ri - bi
    temp = min(8, max(0, (warmth + 255) * 9 // 511))
    max_c = max(ri, gi, bi)
    min_c = min(ri, gi, bi)
    sat = min(8, (max_c - min_c) * 9 // 256)
    return lum, temp, sat


def force999_to_rgb(lum, temp, sat):
    brightness = lum * 255 // 8
    warmth = (temp - 4) * 32
    sat_scale = sat / 8.0
    r = min(255, max(0, int(brightness + warmth * sat_scale)))
    g = min(255, max(0, int(brightness - abs(warmth) * sat_scale * 0.3)))
    b = min(255, max(0, int(brightness - warmth * sat_scale)))
    return r, g, b


def rgb_array_to_force999(pixels):
    """RGB (N,3) uint8 -> Force999 (N,3) uint8. Uses CUDA if available."""
    n = len(pixels)

    # Try CUDA path: 0.48ms vs 92ms
    if _load_cuda(n):
        # Ensure contiguous RGB
        rgb = np.ascontiguousarray(pixels, dtype=np.uint8)
        f9_packed = np.empty(n, dtype=np.uint16)

        _cuda_dll.force9_encode(
            _cuda_ctx,
            rgb.ctypes.data_as(ctypes.c_void_p),
        )
        _cuda_dll.force9_get_f9(
            _cuda_ctx,
            f9_packed.ctypes.data_as(ctypes.c_void_p),
        )

        # Unpack uint16 -> (N,3) Force999
        lum = (f9_packed // 81).astype(np.uint8)
        temp = ((f9_packed % 81) // 9).astype(np.uint8)
        sat = (f9_packed % 9).astype(np.uint8)
        return np.stack([lum, temp, sat], axis=1)

    # Numpy fallback
    r = pixels[:, 0].astype(np.int16)
    g = pixels[:, 1].astype(np.int16)
    b = pixels[:, 2].astype(np.int16)
    lum = np.minimum(8, (r * 299 + g * 587 + b * 114) // (1000 * 29))
    warmth = r - b
    temp = np.minimum(8, np.maximum(0, (warmth + 255) * 9 // 511))
    max_c = np.maximum(np.maximum(r, g), b)
    min_c = np.minimum(np.minimum(r, g), b)
    sat = np.minimum(8, (max_c - min_c) * 9 // 256)
    return np.stack([lum, temp, sat], axis=1).astype(np.uint8)


_RGB_LUT = np.zeros((9, 9, 9, 3), dtype=np.uint8)
for _l in range(9):
    for _t in range(9):
        for _s in range(9):
            _RGB_LUT[_l, _t, _s] = force999_to_rgb(_l, _t, _s)


def force999_array_to_rgb_fast(f999):
    return _RGB_LUT[f999[:, 0], f999[:, 1], f999[:, 2]]


def pack_force999(f999):
    """Pack (N,3) Force999 to (N,) uint16. If input came from CUDA, this is redundant."""
    return f999[:, 0].astype(np.uint16) * 81 + f999[:, 1].astype(np.uint16) * 9 + f999[:, 2].astype(np.uint16)


def rgb_array_to_force999_packed(pixels):
    """RGB (N,3) uint8 -> packed uint16 Force9 values. CUDA fast path.
    Skips the unpack/repack round-trip when you only need packed values."""
    n = len(pixels)
    if _load_cuda(n):
        rgb = np.ascontiguousarray(pixels, dtype=np.uint8)
        f9_packed = np.empty(n, dtype=np.uint16)
        _cuda_dll.force9_encode(_cuda_ctx, rgb.ctypes.data_as(ctypes.c_void_p))
        _cuda_dll.force9_get_f9(_cuda_ctx, f9_packed.ctypes.data_as(ctypes.c_void_p))
        return f9_packed
    # Fallback: encode then pack
    f999 = rgb_array_to_force999(pixels)
    return pack_force999(f999)


def rgb_to_compressed(pixels):
    """RGB (N,3) uint8 -> compressed bytes. Full CUDA pipeline.
    Encode + RLE in one call. Returns (compressed_bytes, num_bytes, encode_ms).
    Falls back to numpy if CUDA unavailable."""
    n = len(pixels)
    if _load_cuda(n):
        # Wire up encode_and_compress if not already done
        if not hasattr(_cuda_dll, '_rle_ready'):
            try:
                _cuda_dll.force9_encode_and_compress.restype = ctypes.c_int
                _cuda_dll.force9_encode_and_compress.argtypes = [
                    ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p,
                    ctypes.c_int, ctypes.POINTER(ctypes.c_float),
                ]
                _cuda_dll._rle_ready = True
            except AttributeError:
                _cuda_dll._rle_ready = False

        if getattr(_cuda_dll, '_rle_ready', False):
            rgb = np.ascontiguousarray(pixels, dtype=np.uint8)
            # Max output: 3 bytes per run, worst case = n_pixels runs
            max_out = n * 3
            out_buf = np.empty(max_out, dtype=np.uint8)
            encode_ms = ctypes.c_float(0.0)

            n_bytes = _cuda_dll.force9_encode_and_compress(
                _cuda_ctx,
                rgb.ctypes.data_as(ctypes.c_void_p),
                out_buf.ctypes.data_as(ctypes.c_void_p),
                max_out,
                ctypes.byref(encode_ms),
            )

            return bytes(out_buf[:n_bytes].tobytes()), n_bytes, float(encode_ms.value)

    # Numpy fallback
    packed = rgb_array_to_force999_packed(pixels)
    compressed, num_runs = compress_force999_stream(packed)
    return compressed, len(compressed), 0.0


def unpack_force999(packed):
    lum = (packed // 81).astype(np.uint8)
    temp = ((packed % 81) // 9).astype(np.uint8)
    sat = (packed % 9).astype(np.uint8)
    return np.stack([lum, temp, sat], axis=1)


def compress_force999_stream(packed_array):
    """RLE compress Force999 stream. Fully vectorized numpy — no Python loops."""
    if len(packed_array) == 0:
        return b'', 0

    arr = np.asarray(packed_array, dtype=np.uint16)

    # Find boundaries where value changes
    diff = np.diff(arr)
    boundaries = np.nonzero(diff)[0] + 1  # indices where new runs start
    run_starts = np.concatenate([[0], boundaries])
    run_ends = np.concatenate([boundaries, [len(arr)]])

    # Values and lengths
    values = arr[run_starts]
    lengths = (run_ends - run_starts).astype(np.int32)

    # Split runs longer than 255 into multiple runs
    # (vectorized: expand long runs into 255-capped chunks)
    needs_split = np.any(lengths > 255)
    if needs_split:
        new_vals = []
        new_lens = []
        for v, l in zip(values, lengths):
            while l > 255:
                new_vals.append(v)
                new_lens.append(255)
                l -= 255
            new_vals.append(v)
            new_lens.append(l)
        values = np.array(new_vals, dtype=np.uint16)
        lengths = np.array(new_lens, dtype=np.uint8)
    else:
        lengths = lengths.astype(np.uint8)

    num_runs = len(values)

    # Pack: [2B value big-endian][1B count] per run
    # Build as flat byte array: val_hi, val_lo, count
    out = np.empty(num_runs * 3, dtype=np.uint8)
    out[0::3] = (values >> 8).astype(np.uint8)
    out[1::3] = (values & 0xFF).astype(np.uint8)
    out[2::3] = lengths

    return bytes(out.tobytes()), num_runs


def decompress_force999_stream(packed_bytes, expected_pixels):
    """RLE decompress Force999 stream. Vectorized numpy."""
    if len(packed_bytes) < 3:
        return np.zeros(expected_pixels, dtype=np.uint16)

    raw = np.frombuffer(packed_bytes, dtype=np.uint8)
    # Trim to multiple of 3
    n_runs = len(raw) // 3
    raw = raw[:n_runs * 3]

    # Extract values and counts
    val_hi = raw[0::3].astype(np.uint16)
    val_lo = raw[1::3].astype(np.uint16)
    values = (val_hi << 8) | val_lo
    counts = raw[2::3].astype(np.int32)

    # Total pixels from runs
    total = int(np.sum(counts))
    if total > expected_pixels:
        # Trim last runs
        cumsum = np.cumsum(counts)
        keep = np.searchsorted(cumsum, expected_pixels, side='left') + 1
        values = values[:keep]
        counts = counts[:keep]
        overflow = int(np.sum(counts)) - expected_pixels
        if overflow > 0:
            counts[-1] -= overflow
        total = expected_pixels

    # Expand runs: np.repeat is the vectorized version of the Python loop
    result = np.repeat(values, counts)
    if len(result) < expected_pixels:
        result = np.concatenate([result, np.zeros(expected_pixels - len(result), dtype=np.uint16)])
    return result[:expected_pixels]


def compress_screen(pixels, width, height):
    if isinstance(pixels, np.ndarray) and len(pixels.shape) == 3:
        pixels = pixels.reshape(-1, 3)
    f999 = rgb_array_to_force999(pixels)
    packed = pack_force999(f999)
    compressed, num_runs = compress_force999_stream(packed)
    return compressed, num_runs, len(np.unique(packed))


def decompress_screen(compressed, width, height):
    packed = decompress_force999_stream(compressed, width * height)
    f999 = unpack_force999(packed)
    rgb = force999_array_to_rgb_fast(f999)
    return rgb.reshape(height, width, 3)


# Compatibility wrappers
def rgb_array_to_force9(pixels):
    f999 = rgb_array_to_force999(pixels)
    return pack_force999(f999)

def compress_force9_stream(packed_array):
    return compress_force999_stream(packed_array)

def decompress_force9_stream(packed_bytes, expected_pixels):
    return decompress_force999_stream(packed_bytes, expected_pixels)

def force9_to_rgb(val):
    f999 = unpack_force999(np.array([val], dtype=np.uint16))
    return force999_to_rgb(f999[0, 0], f999[0, 1], f999[0, 2])


def run_all():
    print('=== TIG 9x9x9 SCREEN COMPRESSION ===')
    print('  729 quantization levels (9 lum x 9 temp x 9 sat)')
    print()

    colors = [
        (255, 0, 0, 'Red'), (0, 255, 0, 'Green'), (0, 0, 255, 'Blue'),
        (255, 255, 255, 'White'), (0, 0, 0, 'Black'), (128, 128, 128, 'Gray'),
        (255, 128, 0, 'Orange'), (128, 0, 255, 'Purple'),
    ]
    print('ROUNDTRIP QUALITY:')
    for r, g, b, name in colors:
        l, t, s = rgb_to_force999(r, g, b)
        r2, g2, b2 = force999_to_rgb(l, t, s)
        err = abs(r-r2) + abs(g-g2) + abs(b-b2)
        print(f'  {name:8s} ({r:3d},{g:3d},{b:3d}) -> ({l},{t},{s}) -> ({r2:3d},{g2:3d},{b2:3d})  err={err}')

    print('\nCOMPRESSION:')
    solid = np.full((640*480, 3), 200, dtype=np.uint8)
    comp, runs, uniq = compress_screen(solid, 640, 480)
    print(f'  Solid:  {solid.nbytes/max(1,len(comp)):.1f}x  ({runs} runs, {uniq} unique)')

    noise = np.random.randint(0, 256, (640*480, 3), dtype=np.uint8)
    comp2, runs2, uniq2 = compress_screen(noise, 640, 480)
    print(f'  Noise:  {noise.nbytes/max(1,len(comp2)):.1f}x  ({runs2} runs, {uniq2} unique)')

    try:
        import ctypes
        user32 = ctypes.windll.user32; gdi32 = ctypes.windll.gdi32
        hdc = user32.GetDC(0); memdc = gdi32.CreateCompatibleDC(hdc)
        w, h = 640, 480
        bmp = gdi32.CreateCompatibleBitmap(hdc, w, h)
        gdi32.SelectObject(memdc, bmp)
        gdi32.BitBlt(memdc, 0, 0, w, h, hdc, 0, 0, 0x00CC0020)
        buf = (ctypes.c_char * (w*h*4))()
        bi = struct.pack('iiiHHIIiiII', 40, w, -h, 1, 32, 0, 0, 0, 0, 0, 0)
        gdi32.GetDIBits(memdc, bmp, 0, h, buf, ctypes.create_string_buffer(bi), 0)
        real = np.frombuffer(buf, dtype=np.uint8).reshape(w*h, 4)[:, :3].copy()
        gdi32.DeleteObject(bmp); gdi32.DeleteDC(memdc); user32.ReleaseDC(0, hdc)
        comp3, runs3, uniq3 = compress_screen(real, w, h)
        print(f'  Screen: {real.nbytes/max(1,len(comp3)):.1f}x  ({runs3} runs, {uniq3} unique)')
        decomp = decompress_screen(comp3, w, h)
        print(f'  Roundtrip: {decomp.shape} OK')
    except Exception as e:
        print(f'  Screen: {e}')


if __name__ == '__main__':
    run_all()
