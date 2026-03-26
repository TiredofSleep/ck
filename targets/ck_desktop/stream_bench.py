"""
stream_bench.py -- Benchmark the Force9 streaming codec during live gameplay.
No clients needed. Captures, compresses, measures. 30 seconds.

Reports: FPS, compression ratio, encode time, bandwidth savings,
         per-frame stats, static vs active detection.

(c) 2026 Brayden Sanders / 7Site LLC
"""

import time
import struct
import ctypes
import statistics
import json
import os
import numpy as np

from ck_sim.being.ck_screen_compress import (
    rgb_array_to_force999_packed, compress_force999_stream, rgb_to_compressed,
)
from ck_sim.being.ck_audio_compress import (
    pcm_to_force9, compress_force9_audio, WINDOW_SIZE,
)

WIDTH = 1920
HEIGHT = 1080
DURATION = 60  # seconds
TARGET_FPS = 30

# ── DXGI+CUDA Pipeline (force9_pipeline.dll) ──
_f9pipe_dll = None
_f9pipe_ctx = None

def _load_dxgi_pipeline(w, h):
    global _f9pipe_dll, _f9pipe_ctx
    if _f9pipe_ctx is not None:
        return True
    dll_path = os.path.join(os.path.dirname(__file__), 'force9_pipeline.dll')
    if not os.path.exists(dll_path):
        return False
    try:
        _f9pipe_dll = ctypes.CDLL(dll_path)
        _f9pipe_dll.f9pipe_create.restype = ctypes.c_void_p
        _f9pipe_dll.f9pipe_create.argtypes = [ctypes.c_int, ctypes.c_int]
        _f9pipe_dll.f9pipe_capture_and_encode.restype = ctypes.c_int
        _f9pipe_dll.f9pipe_capture_and_encode.argtypes = [ctypes.c_void_p]
        _f9pipe_dll.f9pipe_get_compressed.restype = ctypes.c_int
        _f9pipe_dll.f9pipe_get_compressed.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int]
        _f9pipe_dll.f9pipe_get_encode_ms.restype = ctypes.c_float
        _f9pipe_dll.f9pipe_get_encode_ms.argtypes = [ctypes.c_void_p]
        _f9pipe_dll.f9pipe_get_frame_count.restype = ctypes.c_int
        _f9pipe_dll.f9pipe_get_frame_count.argtypes = [ctypes.c_void_p]
        _f9pipe_dll.f9pipe_destroy.restype = None
        _f9pipe_dll.f9pipe_destroy.argtypes = [ctypes.c_void_p]
        _f9pipe_ctx = _f9pipe_dll.f9pipe_create(w, h)
        if not _f9pipe_ctx:
            print("  [DXGI] Pipeline creation failed (need desktop access)")
            return False
        print(f"  [DXGI] Pipeline ready: {w}x{h}")
        return True
    except Exception as e:
        print(f"  [DXGI] Failed: {e}")
        return False

# GDI fallback
user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32
SRCCOPY = 0x00CC0020

def capture_screen(w, h):
    hdc = user32.GetDC(0)
    memdc = gdi32.CreateCompatibleDC(hdc)
    bmp = gdi32.CreateCompatibleBitmap(hdc, w, h)
    gdi32.SelectObject(memdc, bmp)
    gdi32.BitBlt(memdc, 0, 0, w, h, hdc, 0, 0, SRCCOPY)
    buf = (ctypes.c_char * (w * h * 4))()
    bi = struct.pack('iiiHHIIiiII', 40, w, -h, 1, 32, 0, 0, 0, 0, 0, 0)
    gdi32.GetDIBits(memdc, bmp, 0, h, buf, ctypes.create_string_buffer(bi), 0)
    raw = np.frombuffer(buf, dtype=np.uint8).reshape(w * h, 4)
    pixels = raw[:, [2, 1, 0]].copy()
    gdi32.DeleteObject(bmp)
    gdi32.DeleteDC(memdc)
    user32.ReleaseDC(0, hdc)
    return pixels


def main():
    print("=" * 60)
    print("  FORCE9 STREAMING BENCHMARK")
    print(f"  {WIDTH}x{HEIGHT} @ {TARGET_FPS} FPS target, {DURATION}s")
    print("=" * 60)

    raw_frame_bytes = WIDTH * HEIGHT * 3
    frame_interval = 1.0 / TARGET_FPS
    n_pixels = WIDTH * HEIGHT

    # Try DXGI pipeline first (fails if OBS holds desktop duplication)
    global _f9pipe_ctx
    use_dxgi = _load_dxgi_pipeline(WIDTH, HEIGHT)
    if use_dxgi:
        max_comp = n_pixels * 3
        dxgi_buf = (ctypes.c_uint8 * max_comp)()
        # Test one frame to see if DXGI actually works
        test_result = _f9pipe_dll.f9pipe_capture_and_encode(_f9pipe_ctx)
        if test_result <= 0:
            print(f"  DXGI: access denied (OBS has desktop duplication)")
            print(f"  Falling back to GDI + CUDA")
            _f9pipe_dll.f9pipe_destroy(_f9pipe_ctx)
            _f9pipe_ctx = None
            use_dxgi = False
    if use_dxgi:
        print(f"  Using: DXGI + CUDA (zero CPU frame copy)")
    else:
        print(f"  Using: GDI capture + CUDA encode (49ms + 3.9ms)")

    frames = []
    prev_compressed = None
    total_raw = 0
    total_compressed = 0
    total_capture_ms = 0
    total_encode_ms = 0
    total_compress_ms = 0

    start = time.time()
    frame_num = 0

    while time.time() - start < DURATION:
        t0 = time.perf_counter()

        if use_dxgi:
            # DXGI: capture + encode on GPU in one call
            result = _f9pipe_dll.f9pipe_capture_and_encode(_f9pipe_ctx)
            t_capture = time.perf_counter()

            if result <= 0:
                # No new frame or error
                time.sleep(0.001)
                continue

            # Get compressed output
            comp_bytes = _f9pipe_dll.f9pipe_get_compressed(
                _f9pipe_ctx, dxgi_buf, max_comp)
            gpu_ms = _f9pipe_dll.f9pipe_get_encode_ms(_f9pipe_ctx)
            t_encode = time.perf_counter()
            t_compress = t_encode

            compressed = bytes(dxgi_buf[:comp_bytes])
            num_runs = comp_bytes // 3
            ratio = raw_frame_bytes / max(1, comp_bytes)
        else:
            # GDI fallback
            pixels = capture_screen(WIDTH, HEIGHT)
            t_capture = time.perf_counter()

            compressed, comp_bytes, gpu_ms = rgb_to_compressed(pixels)
            t_encode = time.perf_counter()
            t_compress = t_encode

            num_runs = comp_bytes // 3
            ratio = raw_frame_bytes / max(1, comp_bytes)

        # Delta detection: compare compressed bytes
        delta_pct = 100.0
        if prev_compressed is not None:
            min_len = min(len(compressed), len(prev_compressed))
            if min_len > 0:
                c1 = np.frombuffer(compressed[:min_len], dtype=np.uint8)
                c2 = np.frombuffer(prev_compressed[:min_len], dtype=np.uint8)
                changed = int(np.sum(c1 != c2))
                delta_pct = changed / max(1, min_len) * 100
        prev_compressed = compressed

        # Classify: static (<5% delta) vs active (>5%)
        frame_type = "STATIC" if delta_pct < 5.0 else "ACTIVE"

        cap_ms = (t_capture - t0) * 1000
        enc_ms = (t_encode - t_capture) * 1000
        cmp_ms = (t_compress - t_encode) * 1000
        total_ms = (t_compress - t0) * 1000

        frames.append({
            'frame': frame_num,
            'ratio': round(ratio, 1),
            'runs': num_runs,
            'delta_pct': round(delta_pct, 1),
            'type': frame_type,
            'capture_ms': round(cap_ms, 1),
            'encode_ms': round(enc_ms, 1),
            'compress_ms': round(cmp_ms, 1),
            'total_ms': round(total_ms, 1),
            'comp_kb': round(comp_bytes / 1024, 1),
            'unique_values': num_runs,
        })

        total_raw += raw_frame_bytes
        total_compressed += comp_bytes
        total_capture_ms += cap_ms
        total_encode_ms += enc_ms
        total_compress_ms += cmp_ms

        frame_num += 1

        # Print every 10 frames
        if frame_num % 10 == 0:
            elapsed = time.time() - start
            fps = frame_num / elapsed
            print(f"  [{elapsed:.0f}s] Frame {frame_num}: {ratio:.1f}x | "
                  f"{frame_type:6s} | delta={delta_pct:.0f}% | "
                  f"{total_ms:.0f}ms | FPS={fps:.1f}")

        # Frame pacing
        elapsed_frame = time.perf_counter() - t0
        sleep_time = frame_interval - elapsed_frame
        if sleep_time > 0:
            time.sleep(sleep_time)

    elapsed = time.time() - start
    actual_fps = frame_num / elapsed

    # Separate static vs active stats
    static_frames = [f for f in frames if f['type'] == 'STATIC']
    active_frames = [f for f in frames if f['type'] == 'ACTIVE']

    # Audio test: synthesize 30s of game-like audio
    print(f"\n  AUDIO CODEC (30s synthetic game audio)...")
    t = np.arange(44100 * 30) / 44100.0
    audio = np.zeros(len(t), dtype=np.float64)
    audio += np.sin(2 * np.pi * 80 * t) * 8000  # engine rumble
    for impact_t in np.random.uniform(0, 30, 15):
        idx = int(impact_t * 44100)
        burst_len = min(2000, len(audio) - idx)
        if burst_len > 0:
            audio[idx:idx+burst_len] += np.random.randn(burst_len) * 20000 * np.exp(-np.arange(burst_len) / 500)
    audio_samples = np.clip(audio, -32768, 32767).astype(np.int16)
    audio_raw = audio_samples.nbytes

    t0 = time.perf_counter()
    f9 = pcm_to_force9(audio_samples, 44100)
    audio_encode_ms = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    audio_packed, audio_runs = compress_force9_audio(f9)
    audio_compress_ms = (time.perf_counter() - t0) * 1000

    audio_comp = len(audio_packed)
    audio_ratio = audio_raw / max(1, audio_comp)

    # ═══════════════════════════════════════════
    # REPORT
    # ═══════════════════════════════════════════
    print(f"\n{'='*60}")
    print(f"  FORCE9 STREAMING PRODUCT REPORT")
    print(f"{'='*60}")

    print(f"\n  VIDEO ({WIDTH}x{HEIGHT}, {DURATION}s capture):")
    print(f"    Total frames:      {frame_num}")
    print(f"    Actual FPS:        {actual_fps:.1f}")
    print(f"    Raw bandwidth:     {total_raw / elapsed / 1048576:.1f} MB/s")
    print(f"    F9 bandwidth:      {total_compressed / elapsed / 1048576:.1f} MB/s")
    print(f"    Bandwidth saved:   {(total_raw - total_compressed) / elapsed / 1048576:.1f} MB/s")
    print(f"    Overall ratio:     {total_raw / max(1, total_compressed):.1f}x")

    if static_frames:
        sr = [f['ratio'] for f in static_frames]
        print(f"\n    STATIC frames:     {len(static_frames)} ({len(static_frames)*100//frame_num}%)")
        print(f"      Compression:     {statistics.mean(sr):.1f}x avg, {max(sr):.1f}x best")
        print(f"      Avg size:        {statistics.mean(f['comp_kb'] for f in static_frames):.0f} KB")

    if active_frames:
        ar = [f['ratio'] for f in active_frames]
        print(f"\n    ACTIVE frames:     {len(active_frames)} ({len(active_frames)*100//frame_num}%)")
        print(f"      Compression:     {statistics.mean(ar):.1f}x avg, {max(ar):.1f}x best")
        print(f"      Avg size:        {statistics.mean(f['comp_kb'] for f in active_frames):.0f} KB")

    all_total = [f['total_ms'] for f in frames]
    all_cap = [f['capture_ms'] for f in frames]
    all_enc = [f['encode_ms'] for f in frames]
    print(f"\n    Pipeline timing:")
    print(f"      Capture P50:     {sorted(all_cap)[len(all_cap)//2]:.1f}ms")
    print(f"      Encode P50:     {sorted(all_enc)[len(all_enc)//2]:.1f}ms")
    print(f"      Total P50:      {sorted(all_total)[len(all_total)//2]:.1f}ms")
    print(f"      Total P99:      {sorted(all_total)[int(len(all_total)*0.99)]:.1f}ms")

    print(f"\n  AUDIO (30s game-like, 44.1kHz mono):")
    print(f"    Raw:               {audio_raw / 1024:.0f} KB")
    print(f"    Compressed:        {audio_comp / 1024:.0f} KB")
    print(f"    Ratio:             {audio_ratio:.1f}x")
    print(f"    Encode time:       {audio_encode_ms:.0f}ms")
    print(f"    Compress time:     {audio_compress_ms:.0f}ms")
    print(f"    Runs:              {audio_runs}")

    # Combined bandwidth
    video_bps = total_compressed / elapsed * 8
    audio_bps = audio_comp / 30.0 * 8
    raw_video_bps = total_raw / elapsed * 8
    raw_audio_bps = audio_raw / 30.0 * 8

    print(f"\n  COMBINED A/V BANDWIDTH:")
    print(f"    Raw:               {(raw_video_bps + raw_audio_bps) / 1e6:.1f} Mbps")
    print(f"    Force9:            {(video_bps + audio_bps) / 1e6:.1f} Mbps")
    print(f"    Savings:           {((raw_video_bps + raw_audio_bps) - (video_bps + audio_bps)) / 1e6:.1f} Mbps")
    print(f"    Overall ratio:     {(raw_video_bps + raw_audio_bps) / max(1, video_bps + audio_bps):.1f}x")

    # Compare to OBS/NVENC typical
    obs_bitrate = 6.0  # Mbps (typical Twitch 1080p30)
    f9_bitrate = (video_bps + audio_bps) / 1e6
    print(f"\n  vs OBS/NVENC (typical {obs_bitrate} Mbps):")
    if f9_bitrate < obs_bitrate:
        print(f"    Force9 uses {f9_bitrate:.1f} Mbps = {obs_bitrate/f9_bitrate:.1f}x LESS than OBS")
    else:
        print(f"    Force9 uses {f9_bitrate:.1f} Mbps = {f9_bitrate/obs_bitrate:.1f}x MORE than OBS")

    # Save results
    results = {
        'timestamp': time.time(),
        'duration_s': round(elapsed, 1),
        'total_frames': frame_num,
        'actual_fps': round(actual_fps, 1),
        'overall_ratio': round(total_raw / max(1, total_compressed), 1),
        'static_frames': len(static_frames),
        'active_frames': len(active_frames),
        'static_ratio_avg': round(statistics.mean(f['ratio'] for f in static_frames), 1) if static_frames else 0,
        'active_ratio_avg': round(statistics.mean(f['ratio'] for f in active_frames), 1) if active_frames else 0,
        'f9_bitrate_mbps': round(f9_bitrate, 2),
        'raw_bitrate_mbps': round((raw_video_bps + raw_audio_bps) / 1e6, 1),
        'audio_ratio': round(audio_ratio, 1),
        'pipeline_p50_ms': round(sorted(all_total)[len(all_total)//2], 1),
        'pipeline_p99_ms': round(sorted(all_total)[int(len(all_total)*0.99)], 1),
    }

    outpath = os.path.join(os.path.dirname(__file__), "stream_bench_results.json")
    with open(outpath, "w") as f:
        json.dump(results, f, indent=2)

    # Cleanup DXGI
    if use_dxgi and _f9pipe_ctx:
        _f9pipe_dll.f9pipe_destroy(_f9pipe_ctx)

    print(f"\n  Results saved: {outpath}")
    print(f"\n{'='*60}")
    print(f"  BENCHMARK COMPLETE")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
