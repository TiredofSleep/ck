"""
ck_stream_server.py -- TIG Audio+Video Streaming Server
Captures screen + audio, compresses both with Force9, streams over TCP.

Video: TIG 3-shell visual encoder, 127x compression at dE=1.03
Audio: Force9 9-bit force geometry, 47-4009x compression
Both interleaved in the same TCP stream with frame type markers.

Protocol:
  [1B type][4B length][payload]
  type 0x01 = video frame: [2B width][2B height][compressed pixels]
  type 0x02 = audio frame: [4B sample_rate][4B sample_count][4B window_count][compressed]

Usage: python ck_stream_server.py [--port 7778] [--fps 30] [--width 1920] [--height 1080]
       python ck_stream_server.py --no-audio  (video only)

(c) 2026 Brayden Sanders / 7Site LLC
"""

import argparse
import ctypes
import socket
import struct
import sys
import threading
import time
import numpy as np

# TIG Visual Encoder with temporal delta compression
from ck_sim.being.ck_visual_encoder import TIGTemporalEncoder

# TIG Audio Encoder
from ck_sim.being.ck_audio_compress import (
    pcm_to_force9 as audio_pcm_to_force9,
    compress_force9_audio,
    WINDOW_SIZE as AUDIO_WINDOW_SIZE,
)

# Frame type markers
FRAME_VIDEO = 0x01
FRAME_AUDIO = 0x02

# Windows GDI
user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32
SRCCOPY = 0x00CC0020

# Audio capture via WASAPI loopback (system audio)
_HAS_SOUNDDEVICE = False
try:
    import sounddevice as sd
    _HAS_SOUNDDEVICE = True
except ImportError:
    pass


def capture_screen(w, h):
    """Capture screen via GDI BitBlt. Returns (w*h, 3) uint8 array."""
    hdc = user32.GetDC(0)
    memdc = gdi32.CreateCompatibleDC(hdc)
    bmp = gdi32.CreateCompatibleBitmap(hdc, w, h)
    gdi32.SelectObject(memdc, bmp)
    gdi32.BitBlt(memdc, 0, 0, w, h, hdc, 0, 0, SRCCOPY)
    buf = (ctypes.c_char * (w * h * 4))()
    bi = struct.pack('iiiHHIIiiII', 40, w, -h, 1, 32, 0, 0, 0, 0, 0, 0)
    gdi32.GetDIBits(memdc, bmp, 0, h, buf, ctypes.create_string_buffer(bi), 0)
    raw = np.frombuffer(buf, dtype=np.uint8).reshape(w * h, 4)
    pixels = raw[:, [2, 1, 0]].copy()  # BGR -> RGB
    gdi32.DeleteObject(bmp)
    gdi32.DeleteDC(memdc)
    user32.ReleaseDC(0, hdc)
    return pixels


class StreamServer:
    """TCP server that streams Force9-compressed screen + audio to clients."""

    def __init__(self, port, fps, width, height, enable_audio=True):
        self.port = port
        self.target_fps = fps
        self.width = width
        self.height = height
        self.enable_audio = enable_audio and _HAS_SOUNDDEVICE
        self.clients = []
        self.clients_lock = threading.Lock()
        self.running = False

        # Video stats
        self.frame_count = 0
        self.total_video_bytes = 0
        self.total_video_raw = 0

        # Audio stats
        self.audio_frames = 0
        self.total_audio_bytes = 0
        self.total_audio_raw = 0

        self.stats_time = time.time()

        # Audio buffer (filled by sounddevice callback)
        self._audio_buffer = []
        self._audio_lock = threading.Lock()
        self._audio_sample_rate = 44100
        self._audio_stream = None

        # Video encoder (lazy init)
        self._temporal = None

    def start(self):
        self.running = True

        # Start accept thread
        threading.Thread(target=self._accept_loop, daemon=True).start()

        # Start audio capture thread
        if self.enable_audio:
            self._start_audio_capture()

        print("[server] Force9 A/V Streaming Server")
        print("[server] Video: %dx%d @ %d FPS" % (self.width, self.height, self.target_fps))
        print("[server] Audio: %s" % (
            "WASAPI loopback %d Hz" % self._audio_sample_rate if self.enable_audio
            else "disabled"))
        print("[server] Port: %d" % self.port)
        print("[server] Waiting for clients...")

        self._capture_loop()

    def _start_audio_capture(self):
        """Start capturing system audio via WASAPI loopback."""
        try:
            # Find loopback device (system audio output)
            devices = sd.query_devices()
            loopback_id = None
            # Priority: true WASAPI loopback > Stereo Mix > Windows mixer
            LOOPBACK_KEYWORDS = ('loopback', 'stereo mix', 'what u hear',
                                 'wave out mix', 'what you hear', 'mix')
            best_priority = 99
            for i, d in enumerate(devices):
                if d['max_input_channels'] < 1:
                    continue
                name = d['name'].lower()
                for pri, kw in enumerate(LOOPBACK_KEYWORDS):
                    if kw in name and pri < best_priority:
                        loopback_id = i
                        best_priority = pri
                        break

            if loopback_id is None:
                # Use default input as fallback
                loopback_id = sd.default.device[0]
                if loopback_id is None or loopback_id < 0:
                    print("[audio] No audio input device found")
                    self.enable_audio = False
                    return

            dev_info = sd.query_devices(loopback_id)
            self._audio_sample_rate = int(dev_info.get('default_samplerate', 44100))

            def audio_callback(indata, frames, time_info, status):
                if status:
                    pass  # ignore underruns
                # Convert to mono int16
                mono = indata[:, 0] if indata.ndim > 1 else indata
                samples = (mono * 32767).astype(np.int16)
                with self._audio_lock:
                    self._audio_buffer.append(samples)

            self._audio_stream = sd.InputStream(
                device=loopback_id,
                channels=1,
                samplerate=self._audio_sample_rate,
                blocksize=AUDIO_WINDOW_SIZE * 32,  # ~23ms chunks
                dtype='float32',
                callback=audio_callback,
            )
            self._audio_stream.start()
            print("[audio] Capturing from: %s @ %d Hz" % (
                dev_info['name'], self._audio_sample_rate))
        except Exception as e:
            print("[audio] Failed to start capture: %s" % e)
            self.enable_audio = False

    def _accept_loop(self):
        """Accept incoming client connections."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('0.0.0.0', self.port))
        sock.listen(5)
        sock.settimeout(1.0)
        while self.running:
            try:
                conn, addr = sock.accept()
                conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                conn.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024 * 1024)
                with self.clients_lock:
                    self.clients.append(conn)
                print("[server] Client connected: %s:%d  (total: %d)" % (
                    addr[0], addr[1], len(self.clients)))
            except socket.timeout:
                continue
            except OSError:
                break
        sock.close()

    def _broadcast(self, packet):
        """Send packet to all connected clients, removing dead ones."""
        dead = []
        with self.clients_lock:
            for conn in self.clients:
                try:
                    conn.sendall(packet)
                except (BrokenPipeError, ConnectionResetError,
                        ConnectionAbortedError, OSError):
                    dead.append(conn)
            for conn in dead:
                self.clients.remove(conn)
                try:
                    conn.close()
                except OSError:
                    pass
        if dead:
            print("[server] %d client(s) disconnected  (remaining: %d)" % (
                len(dead), len(self.clients)))

    def _flush_audio(self):
        """Compress and broadcast any buffered audio."""
        with self._audio_lock:
            if not self._audio_buffer:
                return
            chunks = self._audio_buffer
            self._audio_buffer = []

        # Concatenate all buffered audio
        samples = np.concatenate(chunks)
        if len(samples) < AUDIO_WINDOW_SIZE:
            return

        raw_bytes = samples.nbytes

        # Force9 encode + RLE compress
        force9 = audio_pcm_to_force9(samples, self._audio_sample_rate)
        packed, num_runs = compress_force9_audio(force9)

        # Build audio frame: [1B type][4B len][4B rate][4B samples][4B windows][data]
        audio_header = struct.pack('>III',
                                   self._audio_sample_rate,
                                   len(samples),
                                   len(force9))
        payload = audio_header + packed
        packet = struct.pack('>BI', FRAME_AUDIO, len(payload)) + payload

        self._broadcast(packet)

        self.audio_frames += 1
        self.total_audio_bytes += len(packet)
        self.total_audio_raw += raw_bytes

    def _print_stats(self):
        """Print performance stats every second."""
        now = time.time()
        elapsed = now - self.stats_time
        if elapsed >= 1.0:
            fps = self.frame_count / elapsed
            v_ratio = self.total_video_raw / max(1, self.total_video_bytes)
            v_bw = self.total_video_bytes / elapsed

            with self.clients_lock:
                num_clients = len(self.clients)

            line = "[stats] FPS: %.1f | Video: %.1fx (%.2f MB/s)" % (
                fps, v_ratio, v_bw / (1024 * 1024))

            if self.enable_audio and self.total_audio_bytes > 0:
                a_ratio = self.total_audio_raw / max(1, self.total_audio_bytes)
                a_bw = self.total_audio_bytes / elapsed
                line += " | Audio: %.1fx (%.2f KB/s)" % (
                    a_ratio, a_bw / 1024)

            line += " | Clients: %d" % num_clients
            print(line)

            self.frame_count = 0
            self.total_video_bytes = 0
            self.total_video_raw = 0
            self.audio_frames = 0
            self.total_audio_bytes = 0
            self.total_audio_raw = 0
            self.stats_time = now

    def _capture_loop(self):
        """Main loop: capture video + audio -> encode -> compress -> broadcast."""
        frame_interval = 1.0 / self.target_fps
        pixel_count = self.width * self.height
        raw_frame_size = pixel_count * 3

        while self.running:
            t_start = time.time()

            # Skip if no clients
            with self.clients_lock:
                has_clients = len(self.clients) > 0
            if not has_clients:
                # Still drain audio buffer so it doesn't grow
                with self._audio_lock:
                    self._audio_buffer.clear()
                time.sleep(0.1)
                continue

            # ── VIDEO ──
            pixels = capture_screen(self.width, self.height)

            if self._temporal is None:
                self._temporal = TIGTemporalEncoder(self.width, self.height)
            frame_type, compressed, stats = self._temporal.encode_frame(pixels)

            # Build video packet: [1B type][4B len][2B w][2B h][data]
            video_header = struct.pack('>HH', self.width, self.height)
            payload = video_header + compressed
            packet = struct.pack('>BI', FRAME_VIDEO, len(payload)) + payload

            self._broadcast(packet)

            self.frame_count += 1
            self.total_video_bytes += len(packet)
            self.total_video_raw += raw_frame_size

            # ── AUDIO ──
            if self.enable_audio:
                self._flush_audio()

            self._print_stats()

            # Frame pacing
            elapsed = time.time() - t_start
            sleep_time = frame_interval - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

    def stop(self):
        self.running = False
        if self._audio_stream:
            try:
                self._audio_stream.stop()
                self._audio_stream.close()
            except Exception:
                pass
        with self.clients_lock:
            for conn in self.clients:
                try:
                    conn.close()
                except OSError:
                    pass
            self.clients.clear()


def main():
    parser = argparse.ArgumentParser(description="Force9 A/V Streaming Server")
    parser.add_argument('--port', type=int, default=7778, help='TCP port (default: 7778)')
    parser.add_argument('--fps', type=int, default=30, help='Target FPS (default: 30)')
    parser.add_argument('--width', type=int, default=1920, help='Capture width (default: 1920)')
    parser.add_argument('--height', type=int, default=1080, help='Capture height (default: 1080)')
    parser.add_argument('--no-audio', action='store_true', help='Disable audio capture')
    args = parser.parse_args()

    server = StreamServer(args.port, args.fps, args.width, args.height,
                          enable_audio=not args.no_audio)
    try:
        server.start()
    except KeyboardInterrupt:
        print("\n[server] Shutting down...")
        server.stop()


if __name__ == '__main__':
    main()
