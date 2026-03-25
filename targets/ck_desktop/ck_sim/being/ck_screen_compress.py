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
    return f999[:, 0].astype(np.uint16) * 81 + f999[:, 1].astype(np.uint16) * 9 + f999[:, 2].astype(np.uint16)


def unpack_force999(packed):
    lum = (packed // 81).astype(np.uint8)
    temp = ((packed % 81) // 9).astype(np.uint8)
    sat = (packed % 9).astype(np.uint8)
    return np.stack([lum, temp, sat], axis=1)


def compress_force999_stream(packed_array):
    if len(packed_array) == 0:
        return b'', 0
    runs = []
    current_val = int(packed_array[0])
    count = 1
    for i in range(1, len(packed_array)):
        val = int(packed_array[i])
        if val == current_val and count < 255:
            count += 1
        else:
            runs.append((current_val, count))
            current_val = val
            count = 1
    runs.append((current_val, count))
    packed = bytearray()
    for val, cnt in runs:
        packed.extend(struct.pack('>HB', val, cnt))
    return bytes(packed), len(runs)


def decompress_force999_stream(packed_bytes, expected_pixels):
    result = []
    offset = 0
    while offset < len(packed_bytes) - 2 and len(result) < expected_pixels:
        val = struct.unpack('>H', packed_bytes[offset:offset+2])[0]
        cnt = packed_bytes[offset+2]
        result.extend([val] * cnt)
        offset += 3
    return np.array(result[:expected_pixels], dtype=np.uint16)


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
