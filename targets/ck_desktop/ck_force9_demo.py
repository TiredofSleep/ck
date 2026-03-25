"""
ck_force9_demo.py -- Force9 Codec Live Demo
Actually compresses and decompresses screen + audio in real-time.
Not measurement. Actual work. Real savings.

Usage:
  python ck_force9_demo.py --mode screen    (screen mirror with compression)
  python ck_force9_demo.py --mode video     (compress a video file)
  python ck_force9_demo.py --mode audio     (mic -> compress -> decompress -> speaker)
  python ck_force9_demo.py --mode full      (screen + audio together)

(c) 2026 Brayden Sanders / 7Site LLC
"""

import sys
import os
import argparse
import struct
import time
import threading
import ctypes
import ctypes.wintypes
import traceback

import numpy as np

# -- Force9 codec imports --
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ck_sim.being.ck_screen_compress import (
    rgb_array_to_force9,
    compress_force9_stream,
    decompress_force9_stream,
    force9_to_rgb,
)
from ck_sim.being.ck_audio_compress import (
    pcm_to_force9,
    compress_force9_audio,
    decompress_force9_audio,
    force9_to_pcm,
    WINDOW_SIZE as AUDIO_WINDOW_SIZE,
)

# -- Optional imports --
try:
    import pygame
    HAS_PYGAME = True
except ImportError:
    HAS_PYGAME = False

try:
    import sounddevice as sd
    HAS_SOUNDDEVICE = True
except ImportError:
    HAS_SOUNDDEVICE = False

try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False

# ============================================================
# FORCE9 RGB LUT (512 entries, built once)
# ============================================================

_F9_LUT = None

def _build_lut():
    """Build a 512-entry lookup table: force9 value -> (r, g, b)."""
    global _F9_LUT
    if _F9_LUT is not None:
        return _F9_LUT
    lut = np.zeros((512, 3), dtype=np.uint8)
    for i in range(512):
        r, g, b = force9_to_rgb(i)
        lut[i] = [r, g, b]
    _F9_LUT = lut
    return lut


def force9_array_to_rgb(f9_arr):
    """Convert array of force9 values to (N,3) uint8 RGB using the LUT."""
    lut = _build_lut()
    return lut[f9_arr.astype(np.int32)]


# ============================================================
# SCREEN CAPTURE (Windows ctypes, proven working)
# ============================================================

def capture_screen_region(x, y, w, h):
    """
    Capture a region of the screen using Windows GDI.
    Returns (w*h, 3) uint8 numpy array in RGB order.
    """
    user32 = ctypes.windll.user32
    gdi32 = ctypes.windll.gdi32

    hdesktop = user32.GetDesktopWindow()
    hdc = user32.GetDC(hdesktop)
    memdc = gdi32.CreateCompatibleDC(hdc)
    hbmp = gdi32.CreateCompatibleBitmap(hdc, w, h)
    gdi32.SelectObject(memdc, hbmp)

    # BitBlt: copy screen region to our bitmap
    SRCCOPY = 0x00CC0020
    gdi32.BitBlt(memdc, 0, 0, w, h, hdc, x, y, SRCCOPY)

    # Read pixel data via GetBitmapBits
    # BGRA format, 4 bytes per pixel
    buf_size = w * h * 4
    buf = ctypes.create_string_buffer(buf_size)

    # Use GetDIBits for reliable output
    class BITMAPINFOHEADER(ctypes.Structure):
        _fields_ = [
            ('biSize', ctypes.c_uint32),
            ('biWidth', ctypes.c_int32),
            ('biHeight', ctypes.c_int32),
            ('biPlanes', ctypes.c_uint16),
            ('biBitCount', ctypes.c_uint16),
            ('biCompression', ctypes.c_uint32),
            ('biSizeImage', ctypes.c_uint32),
            ('biXPelsPerMeter', ctypes.c_int32),
            ('biYPelsPerMeter', ctypes.c_int32),
            ('biClrUsed', ctypes.c_uint32),
            ('biClrImportant', ctypes.c_uint32),
        ]

    bmi = BITMAPINFOHEADER()
    bmi.biSize = ctypes.sizeof(BITMAPINFOHEADER)
    bmi.biWidth = w
    bmi.biHeight = -h  # negative = top-down
    bmi.biPlanes = 1
    bmi.biBitCount = 32
    bmi.biCompression = 0  # BI_RGB

    DIB_RGB_COLORS = 0
    gdi32.GetDIBits(
        memdc, hbmp, 0, h,
        buf, ctypes.byref(bmi), DIB_RGB_COLORS
    )

    # Cleanup
    gdi32.DeleteObject(hbmp)
    gdi32.DeleteDC(memdc)
    user32.ReleaseDC(hdesktop, hdc)

    # Convert BGRA -> RGB
    raw = np.frombuffer(buf, dtype=np.uint8).reshape(h, w, 4)
    rgb = raw[:, :, [2, 1, 0]].copy()  # BGR -> RGB, drop alpha
    return rgb.reshape(-1, 3)


# ============================================================
# MODE 1: SCREEN MIRROR
# ============================================================

def run_screen_mirror():
    """
    Capture screen region, compress with Force9, decompress, display
    side-by-side in a pygame window with live stats.
    """
    if not HAS_PYGAME:
        print("ERROR: pygame is required for screen mirror mode.")
        print("  pip install pygame")
        return

    CAP_W, CAP_H = 320, 240
    CAP_X, CAP_Y = 100, 100  # top-left corner of capture region

    WIN_W = CAP_W * 2 + 20  # two panels + gap
    WIN_H = CAP_H + 80       # panels + stats bar
    FONT_SIZE = 16

    pygame.init()
    screen = pygame.display.set_mode((WIN_W, WIN_H))
    pygame.display.set_caption("Force9 Screen Mirror -- LIVE Compression Demo")
    font = pygame.font.SysFont("consolas", FONT_SIZE)
    clock = pygame.time.Clock()

    # Build LUT once
    _build_lut()

    # Stats accumulators
    total_raw_bytes = 0
    total_compressed_bytes = 0
    frame_count = 0
    fps_timer = time.time()
    display_fps = 0.0

    running = True
    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                running = False

        t0 = time.time()

        # 1) Capture
        pixels_rgb = capture_screen_region(CAP_X, CAP_Y, CAP_W, CAP_H)
        t_cap = time.time() - t0

        # 2) Compress
        t1 = time.time()
        force9_vals = rgb_array_to_force9(pixels_rgb)
        packed, num_runs = compress_force9_stream(force9_vals)
        t_enc = time.time() - t1

        # 3) Decompress
        t2 = time.time()
        f9_decoded = decompress_force9_stream(packed, CAP_W * CAP_H)
        rgb_decoded = force9_array_to_rgb(f9_decoded)
        t_dec = time.time() - t2

        # Sizes
        raw_size = CAP_W * CAP_H * 3
        comp_size = len(packed)
        total_raw_bytes += raw_size
        total_compressed_bytes += comp_size
        frame_count += 1

        # FPS
        now = time.time()
        elapsed = now - fps_timer
        if elapsed >= 1.0:
            display_fps = frame_count / elapsed
            frame_count = 0
            fps_timer = now

        ratio = raw_size / max(comp_size, 1)

        # -- Draw --
        screen.fill((20, 20, 24))

        # Left panel: original
        orig_img = pixels_rgb.reshape(CAP_H, CAP_W, 3)
        surf_orig = pygame.surfarray.make_surface(
            np.transpose(orig_img, (1, 0, 2))
        )
        screen.blit(surf_orig, (5, 5))

        # Right panel: Force9 reconstructed
        dec_img = rgb_decoded.reshape(CAP_H, CAP_W, 3)
        surf_dec = pygame.surfarray.make_surface(
            np.transpose(dec_img, (1, 0, 2))
        )
        screen.blit(surf_dec, (CAP_W + 15, 5))

        # Labels
        lbl_orig = font.render("ORIGINAL (24-bit RGB)", True, (200, 200, 200))
        lbl_f9 = font.render("FORCE9 (9-bit recon)", True, (200, 200, 200))
        screen.blit(lbl_orig, (5, CAP_H + 8))
        screen.blit(lbl_f9, (CAP_W + 15, CAP_H + 8))

        # Stats bar
        stats_y = CAP_H + 28
        raw_bw = raw_size * display_fps
        comp_bw = comp_size * display_fps

        lines = [
            "FPS: {:.1f}  |  Ratio: {:.1f}x  |  Runs: {}  |  Cap: {:.1f}ms  Enc: {:.1f}ms  Dec: {:.1f}ms".format(
                display_fps, ratio, num_runs,
                t_cap * 1000, t_enc * 1000, t_dec * 1000
            ),
            "Raw BW: {:.0f} KB/s  |  Compressed BW: {:.0f} KB/s  |  Saved: {:.0f} KB/s ({:.0f}%)".format(
                raw_bw / 1024, comp_bw / 1024,
                (raw_bw - comp_bw) / 1024,
                (1 - comp_bw / max(raw_bw, 1)) * 100
            ),
            "Total: {:.1f} MB raw -> {:.1f} MB compressed".format(
                total_raw_bytes / (1024 * 1024),
                total_compressed_bytes / (1024 * 1024)
            ),
        ]
        for i, line in enumerate(lines):
            surf = font.render(line, True, (0, 220, 120))
            screen.blit(surf, (5, stats_y + i * 18))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    print("\nScreen mirror session complete.")
    print("  Total raw:        {:,.0f} bytes".format(total_raw_bytes))
    print("  Total compressed: {:,.0f} bytes".format(total_compressed_bytes))
    if total_compressed_bytes > 0:
        print("  Overall ratio:    {:.1f}x".format(
            total_raw_bytes / total_compressed_bytes))


# ============================================================
# MODE 2: VIDEO FILE COMPRESSION
# ============================================================

F9V_MAGIC = b'F9V1'

def run_video_file(input_path):
    """
    Read video file with OpenCV, compress each frame to Force9,
    write .f9v file, then play it back from the compressed file.
    """
    if not HAS_CV2:
        print("ERROR: opencv-python (cv2) is required for video mode.")
        print("  pip install opencv-python")
        return
    if not HAS_PYGAME:
        print("ERROR: pygame is required for video playback.")
        print("  pip install pygame")
        return

    if not os.path.isfile(input_path):
        print("ERROR: Video file not found: {}".format(input_path))
        return

    # Build LUT once
    _build_lut()

    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print("ERROR: Cannot open video: {}".format(input_path))
        return

    orig_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    orig_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Scale down for speed if needed
    scale = 1.0
    MAX_DIM = 480
    if max(orig_w, orig_h) > MAX_DIM:
        scale = MAX_DIM / max(orig_w, orig_h)
    out_w = int(orig_w * scale)
    out_h = int(orig_h * scale)

    out_path = os.path.splitext(input_path)[0] + '.f9v'

    print("Force9 Video Encoder")
    print("  Input:  {} ({}x{} @ {:.1f} fps, {} frames)".format(
        input_path, orig_w, orig_h, fps, total_frames))
    print("  Output: {} ({}x{})".format(out_path, out_w, out_h))
    print("  Encoding...")

    # -- ENCODE: Write .f9v --
    compressed_frames = []
    frame_idx = 0
    total_raw = 0
    t_start = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize if needed
        if scale != 1.0:
            frame = cv2.resize(frame, (out_w, out_h))

        # BGR -> RGB, flatten to (N, 3)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pixels = rgb.reshape(-1, 3)
        total_raw += pixels.nbytes

        # Compress
        f9 = rgb_array_to_force9(pixels)
        packed, _ = compress_force9_stream(f9)
        compressed_frames.append(packed)

        frame_idx += 1
        if frame_idx % 50 == 0:
            print("    Frame {}/{}  ({:.0f}%)".format(
                frame_idx, total_frames,
                frame_idx / max(total_frames, 1) * 100))

    cap.release()
    encode_time = time.time() - t_start
    actual_frame_count = len(compressed_frames)

    # Write .f9v file
    with open(out_path, 'wb') as f:
        # Header: magic, width, height, fps_int, frame_count
        f.write(F9V_MAGIC)
        f.write(struct.pack('>IIII', out_w, out_h, int(fps), actual_frame_count))
        # Each frame: [4B length][data]
        for cdata in compressed_frames:
            f.write(struct.pack('>I', len(cdata)))
            f.write(cdata)

    f9v_size = os.path.getsize(out_path)
    orig_size = os.path.getsize(input_path)

    print("\n  Encoding complete in {:.1f}s".format(encode_time))
    print("  Original file:     {:>12,} bytes".format(orig_size))
    print("  Raw pixel data:    {:>12,} bytes".format(total_raw))
    print("  .f9v file:         {:>12,} bytes".format(f9v_size))
    print("  vs original file:  {:>12.1f}x".format(orig_size / max(f9v_size, 1)))
    print("  vs raw pixels:     {:>12.1f}x".format(total_raw / max(f9v_size, 1)))
    print("  Encode FPS:        {:>12.1f}".format(
        actual_frame_count / max(encode_time, 0.001)))

    # -- DECODE: Play back .f9v --
    print("\n  Playing back from .f9v ...")

    pygame.init()
    win_w = out_w
    win_h = out_h + 40
    screen = pygame.display.set_mode((win_w, win_h))
    pygame.display.set_caption("Force9 Video Player -- {}".format(
        os.path.basename(out_path)))
    pfont = pygame.font.SysFont("consolas", 14)
    clock = pygame.time.Clock()

    with open(out_path, 'rb') as f:
        magic = f.read(4)
        if magic != F9V_MAGIC:
            print("  ERROR: Invalid .f9v file")
            pygame.quit()
            return
        pw, ph, pfps, pcount = struct.unpack('>IIII', f.read(16))

        fi = 0
        running = True
        while running and fi < pcount:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    running = False
                elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                    running = False

            if not running:
                break

            # Read compressed frame
            frame_len_data = f.read(4)
            if len(frame_len_data) < 4:
                break
            frame_len = struct.unpack('>I', frame_len_data)[0]
            frame_data = f.read(frame_len)

            # Decompress
            t0 = time.time()
            f9_dec = decompress_force9_stream(frame_data, pw * ph)
            rgb_dec = force9_array_to_rgb(f9_dec)
            dt = time.time() - t0

            # Display
            img = rgb_dec.reshape(ph, pw, 3)
            surf = pygame.surfarray.make_surface(
                np.transpose(img, (1, 0, 2))
            )
            screen.fill((20, 20, 24))
            screen.blit(surf, (0, 0))

            info = "Frame {}/{}  |  Decode: {:.1f}ms  |  Size: {} B".format(
                fi + 1, pcount, dt * 1000, frame_len)
            screen.blit(pfont.render(info, True, (0, 220, 120)), (5, ph + 5))

            pygame.display.flip()
            clock.tick(pfps if pfps > 0 else 30)
            fi += 1

    pygame.quit()
    print("  Playback complete. {} frames decoded.".format(fi))


# ============================================================
# MODE 3: AUDIO PASSTHROUGH
# ============================================================

def run_audio_passthrough():
    """
    Capture mic, compress with Force9, decompress, play through speakers.
    Shows live compression stats.
    """
    if not HAS_SOUNDDEVICE:
        print("ERROR: sounddevice is required for audio mode.")
        print("  pip install sounddevice")
        return

    SAMPLE_RATE = 44100
    BLOCK_SIZE = 1024  # samples per block
    CHANNELS = 1

    print("Force9 Audio Passthrough")
    print("  Sample rate: {} Hz".format(SAMPLE_RATE))
    print("  Block size:  {} samples ({:.1f} ms)".format(
        BLOCK_SIZE, BLOCK_SIZE / SAMPLE_RATE * 1000))
    print("  Press Ctrl+C to stop.\n")

    # Stats
    stats_lock = threading.Lock()
    stats = {
        'total_raw': 0,
        'total_compressed': 0,
        'blocks': 0,
        'last_ratio': 0.0,
        'last_latency_ms': 0.0,
    }

    def audio_callback(indata, outdata, frames, t_info, status):
        if status:
            pass  # ignore xruns silently

        t0 = time.time()

        # Mono int16
        mono = (indata[:, 0] * 32767).astype(np.int16)

        # Compress
        f9 = pcm_to_force9(mono, SAMPLE_RATE)
        packed, num_runs = compress_force9_audio(f9)

        # Decompress
        f9_dec = decompress_force9_audio(packed, len(f9))
        pcm_out = force9_to_pcm(f9_dec, SAMPLE_RATE)

        # Ensure correct length
        if len(pcm_out) < frames:
            pcm_out = np.concatenate([
                pcm_out, np.zeros(frames - len(pcm_out), dtype=np.int16)
            ])
        pcm_out = pcm_out[:frames]

        # Output (float32 for sounddevice)
        outdata[:, 0] = pcm_out.astype(np.float32) / 32768.0

        dt = time.time() - t0
        raw_size = frames * 2  # int16
        comp_size = len(packed)

        with stats_lock:
            stats['total_raw'] += raw_size
            stats['total_compressed'] += comp_size
            stats['blocks'] += 1
            stats['last_ratio'] = raw_size / max(comp_size, 1)
            stats['last_latency_ms'] = dt * 1000

    try:
        with sd.Stream(
            samplerate=SAMPLE_RATE,
            blocksize=BLOCK_SIZE,
            channels=CHANNELS,
            dtype='float32',
            callback=audio_callback,
        ):
            print("  Audio stream active. Speak into your microphone.\n")
            while True:
                time.sleep(1.0)
                with stats_lock:
                    if stats['blocks'] == 0:
                        continue
                    raw_bps = stats['total_raw'] * 8  # bits
                    comp_bps = stats['total_compressed'] * 8
                    ratio = stats['total_raw'] / max(stats['total_compressed'], 1)
                    lat = stats['last_latency_ms']

                print("  Blocks: {:>6}  |  Ratio: {:>5.1f}x  |"
                      "  Raw: {:>6.0f} kbps  |  Compressed: {:>6.0f} kbps  |"
                      "  Latency: {:>5.1f} ms".format(
                          stats['blocks'], ratio,
                          raw_bps / 1024, comp_bps / 1024, lat))

    except KeyboardInterrupt:
        pass

    print("\n  Audio passthrough stopped.")
    with stats_lock:
        if stats['total_compressed'] > 0:
            print("  Total raw:        {:>12,} bytes".format(stats['total_raw']))
            print("  Total compressed: {:>12,} bytes".format(
                stats['total_compressed']))
            print("  Overall ratio:    {:>12.1f}x".format(
                stats['total_raw'] / stats['total_compressed']))


# ============================================================
# MODE 4: FULL PIPELINE (screen + audio)
# ============================================================

def run_full_pipeline():
    """
    Screen mirror + audio passthrough simultaneously.
    Two threads, combined stats display.
    """
    if not HAS_PYGAME:
        print("ERROR: pygame is required for full pipeline mode.")
        return
    if not HAS_SOUNDDEVICE:
        print("ERROR: sounddevice is required for full pipeline mode.")
        print("  (audio will be skipped)")

    CAP_W, CAP_H = 320, 240
    CAP_X, CAP_Y = 100, 100
    WIN_W = CAP_W * 2 + 20
    WIN_H = CAP_H + 120

    SAMPLE_RATE = 44100
    BLOCK_SIZE = 1024

    _build_lut()

    pygame.init()
    screen = pygame.display.set_mode((WIN_W, WIN_H))
    pygame.display.set_caption("Force9 Full Pipeline -- Screen + Audio")
    font = pygame.font.SysFont("consolas", 14)
    clock = pygame.time.Clock()

    # Shared audio stats
    audio_lock = threading.Lock()
    audio_stats = {
        'total_raw': 0,
        'total_compressed': 0,
        'blocks': 0,
        'last_ratio': 0.0,
        'active': False,
    }
    audio_stop = threading.Event()

    def audio_thread_fn():
        if not HAS_SOUNDDEVICE:
            return

        def cb(indata, outdata, frames, t_info, status):
            mono = (indata[:, 0] * 32767).astype(np.int16)
            f9 = pcm_to_force9(mono, SAMPLE_RATE)
            packed, _ = compress_force9_audio(f9)
            f9_dec = decompress_force9_audio(packed, len(f9))
            pcm_out = force9_to_pcm(f9_dec, SAMPLE_RATE)
            if len(pcm_out) < frames:
                pcm_out = np.concatenate([
                    pcm_out,
                    np.zeros(frames - len(pcm_out), dtype=np.int16)
                ])
            pcm_out = pcm_out[:frames]
            outdata[:, 0] = pcm_out.astype(np.float32) / 32768.0

            raw_size = frames * 2
            comp_size = len(packed)
            with audio_lock:
                audio_stats['total_raw'] += raw_size
                audio_stats['total_compressed'] += comp_size
                audio_stats['blocks'] += 1
                audio_stats['last_ratio'] = raw_size / max(comp_size, 1)
                audio_stats['active'] = True

        try:
            with sd.Stream(
                samplerate=SAMPLE_RATE,
                blocksize=BLOCK_SIZE,
                channels=1,
                dtype='float32',
                callback=cb,
            ):
                while not audio_stop.is_set():
                    audio_stop.wait(0.1)
        except Exception:
            pass

    # Start audio thread
    audio_thread = threading.Thread(target=audio_thread_fn, daemon=True)
    audio_thread.start()

    # Screen loop
    total_screen_raw = 0
    total_screen_comp = 0
    screen_frames = 0
    fps_timer = time.time()
    display_fps = 0.0

    running = True
    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                running = False

        t0 = time.time()

        # Capture
        pixels_rgb = capture_screen_region(CAP_X, CAP_Y, CAP_W, CAP_H)

        # Compress
        f9 = rgb_array_to_force9(pixels_rgb)
        packed, num_runs = compress_force9_stream(f9)

        # Decompress
        f9_dec = decompress_force9_stream(packed, CAP_W * CAP_H)
        rgb_dec = force9_array_to_rgb(f9_dec)

        raw_size = CAP_W * CAP_H * 3
        comp_size = len(packed)
        total_screen_raw += raw_size
        total_screen_comp += comp_size
        screen_frames += 1

        now = time.time()
        elapsed = now - fps_timer
        if elapsed >= 1.0:
            display_fps = screen_frames / elapsed
            screen_frames = 0
            fps_timer = now

        frame_time = now - t0
        ratio = raw_size / max(comp_size, 1)

        # Draw
        screen_surf = pygame.display.get_surface()
        screen_surf.fill((20, 20, 24))

        # Original
        orig_img = pixels_rgb.reshape(CAP_H, CAP_W, 3)
        surf_orig = pygame.surfarray.make_surface(
            np.transpose(orig_img, (1, 0, 2)))
        screen_surf.blit(surf_orig, (5, 5))

        # Reconstructed
        dec_img = rgb_dec.reshape(CAP_H, CAP_W, 3)
        surf_dec = pygame.surfarray.make_surface(
            np.transpose(dec_img, (1, 0, 2)))
        screen_surf.blit(surf_dec, (CAP_W + 15, 5))

        # Labels
        screen_surf.blit(
            font.render("ORIGINAL", True, (200, 200, 200)), (5, CAP_H + 8))
        screen_surf.blit(
            font.render("FORCE9", True, (200, 200, 200)),
            (CAP_W + 15, CAP_H + 8))

        # Screen stats
        sy = CAP_H + 26
        raw_bw = raw_size * display_fps
        comp_bw = comp_size * display_fps

        screen_surf.blit(font.render(
            "SCREEN  FPS:{:.0f}  Ratio:{:.1f}x  Raw:{:.0f}KB/s  Comp:{:.0f}KB/s  Saved:{:.0f}%".format(
                display_fps, ratio,
                raw_bw / 1024, comp_bw / 1024,
                (1 - comp_bw / max(raw_bw, 1)) * 100),
            True, (0, 220, 120)), (5, sy))

        # Audio stats
        with audio_lock:
            a_active = audio_stats['active']
            a_raw = audio_stats['total_raw']
            a_comp = audio_stats['total_compressed']
            a_ratio = audio_stats['last_ratio']
            a_blocks = audio_stats['blocks']

        if a_active:
            screen_surf.blit(font.render(
                "AUDIO   Blocks:{}  Ratio:{:.1f}x  Raw:{:.0f}KB  Comp:{:.0f}KB".format(
                    a_blocks, a_raw / max(a_comp, 1),
                    a_raw / 1024, a_comp / 1024),
                True, (0, 180, 220)), (5, sy + 18))
        else:
            screen_surf.blit(font.render(
                "AUDIO   (waiting for mic input...)" if HAS_SOUNDDEVICE
                else "AUDIO   (sounddevice not installed)",
                True, (150, 150, 150)), (5, sy + 18))

        # Combined
        combined_raw = total_screen_raw + a_raw
        combined_comp = total_screen_comp + a_comp
        screen_surf.blit(font.render(
            "TOTAL   Raw:{:.1f}MB  Compressed:{:.1f}MB  Overall:{:.1f}x savings".format(
                combined_raw / (1024 * 1024),
                combined_comp / (1024 * 1024),
                combined_raw / max(combined_comp, 1)),
            True, (220, 220, 0)), (5, sy + 36))

        # Pipeline indicator
        screen_surf.blit(font.render(
            "Capture -> Force9 Encode -> RLE Pack -> Unpack -> Force9 Decode -> Display",
            True, (120, 120, 130)), (5, sy + 56))

        pygame.display.flip()
        clock.tick(30)

    audio_stop.set()
    audio_thread.join(timeout=2.0)
    pygame.quit()

    print("\nFull pipeline session complete.")
    print("  Screen raw:    {:>12,} bytes".format(total_screen_raw))
    print("  Screen comp:   {:>12,} bytes".format(total_screen_comp))
    with audio_lock:
        print("  Audio raw:     {:>12,} bytes".format(audio_stats['total_raw']))
        print("  Audio comp:    {:>12,} bytes".format(
            audio_stats['total_compressed']))
        combined_raw = total_screen_raw + audio_stats['total_raw']
        combined_comp = total_screen_comp + audio_stats['total_compressed']
    print("  Combined raw:  {:>12,} bytes".format(combined_raw))
    print("  Combined comp: {:>12,} bytes".format(combined_comp))
    if combined_comp > 0:
        print("  Overall ratio: {:>12.1f}x".format(
            combined_raw / combined_comp))


# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Force9 Codec Live Demo -- real-time compression pipeline"
    )
    parser.add_argument(
        '--mode', choices=['screen', 'video', 'audio', 'full'],
        default='screen',
        help='Demo mode: screen (mirror), video (file), audio (mic), full (all)'
    )
    parser.add_argument(
        '--input', type=str, default=None,
        help='Input video file for video mode'
    )
    parser.add_argument(
        '--capture-x', type=int, default=100,
        help='Screen capture X offset (default: 100)'
    )
    parser.add_argument(
        '--capture-y', type=int, default=100,
        help='Screen capture Y offset (default: 100)'
    )

    args = parser.parse_args()

    print("=" * 60)
    print("  Force9 Codec Live Demo")
    print("  Real compression. Real decompression. Real pipeline.")
    print("  (c) 2026 Brayden Sanders / 7Site LLC")
    print("=" * 60)
    print()

    if args.mode == 'screen':
        print("Mode: SCREEN MIRROR")
        print("  Captures 320x240 region at ({}, {})".format(
            args.capture_x, args.capture_y))
        print("  Every pixel: RGB -> Force9 9-bit -> RLE -> decompress -> display")
        print("  Press ESC or close window to stop.\n")
        run_screen_mirror()

    elif args.mode == 'video':
        if not args.input:
            print("ERROR: --input <video_file> is required for video mode.")
            print("  Example: python ck_force9_demo.py --mode video --input clip.mp4")
            sys.exit(1)
        print("Mode: VIDEO FILE COMPRESSION")
        run_video_file(args.input)

    elif args.mode == 'audio':
        print("Mode: AUDIO PASSTHROUGH")
        print("  Mic -> Force9 compress -> decompress -> speakers")
        print("  Press Ctrl+C to stop.\n")
        run_audio_passthrough()

    elif args.mode == 'full':
        print("Mode: FULL PIPELINE (Screen + Audio)")
        print("  Screen mirror + audio passthrough simultaneously")
        print("  Press ESC or close window to stop.\n")
        run_full_pipeline()


if __name__ == '__main__':
    main()
