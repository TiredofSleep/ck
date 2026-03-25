"""
ck_stream_server.py -- TIG Visual Streaming Server
Captures screen, compresses with TIG 3-shell visual encoder, streams over TCP.
127x compression at dE=1.03 (barely perceptible). CL-composable lattice stems.

Usage: python ck_stream_server.py [--port 7778] [--fps 30] [--width 1920] [--height 1080]

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
_temporal = None  # initialized after width/height known

# Windows GDI
user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

SRCCOPY = 0x00CC0020


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
    # BGRA -> RGB, reshape to (N, 3)
    raw = np.frombuffer(buf, dtype=np.uint8).reshape(w * h, 4)
    pixels = raw[:, [2, 1, 0]].copy()  # BGR -> RGB
    gdi32.DeleteObject(bmp)
    gdi32.DeleteDC(memdc)
    user32.ReleaseDC(0, hdc)
    return pixels


class StreamServer:
    """TCP server that streams Force9-compressed screen frames to clients."""

    def __init__(self, port, fps, width, height):
        self.port = port
        self.target_fps = fps
        self.width = width
        self.height = height
        self.clients = []
        self.clients_lock = threading.Lock()
        self.running = False
        self.frame_count = 0
        self.total_bytes_sent = 0
        self.total_raw_bytes = 0
        self.stats_time = time.time()

    def start(self):
        self.running = True
        # Start accept thread
        accept_thread = threading.Thread(target=self._accept_loop, daemon=True)
        accept_thread.start()
        # Start capture loop on main thread
        print("[server] Force9 Screen Streaming Server")
        print("[server] Resolution: %dx%d  Target FPS: %d  Port: %d" % (
            self.width, self.height, self.target_fps, self.port))
        print("[server] Waiting for clients...")
        self._capture_loop()

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

    def _send_to_client(self, conn, frame_data):
        """Send a complete frame to one client. Returns False if client dropped."""
        try:
            conn.sendall(frame_data)
            return True
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError, OSError):
            return False

    def _broadcast_frame(self, frame_data):
        """Send frame to all connected clients, removing dead ones."""
        dead = []
        with self.clients_lock:
            for conn in self.clients:
                if not self._send_to_client(conn, frame_data):
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

    def _print_stats(self):
        """Print performance stats every second."""
        now = time.time()
        elapsed = now - self.stats_time
        if elapsed >= 1.0:
            fps = self.frame_count / elapsed
            bw_sent = self.total_bytes_sent / elapsed
            bw_raw = self.total_raw_bytes / elapsed
            ratio = bw_raw / bw_sent if bw_sent > 0 else 0
            with self.clients_lock:
                num_clients = len(self.clients)
            print("[stats] FPS: %.1f | Compression: %.1fx | Bandwidth: %.2f MB/s (raw %.2f MB/s) | Clients: %d" % (
                fps, ratio, bw_sent / (1024 * 1024), bw_raw / (1024 * 1024), num_clients))
            self.frame_count = 0
            self.total_bytes_sent = 0
            self.total_raw_bytes = 0
            self.stats_time = now

    def _capture_loop(self):
        """Main loop: capture -> encode -> compress -> broadcast."""
        frame_interval = 1.0 / self.target_fps
        pixel_count = self.width * self.height
        raw_frame_size = pixel_count * 3  # RGB bytes

        while self.running:
            t_start = time.time()

            # Skip if no clients
            with self.clients_lock:
                has_clients = len(self.clients) > 0
            if not has_clients:
                time.sleep(0.1)
                continue

            # 1. Capture screen
            pixels = capture_screen(self.width, self.height)

            # 2. RGB -> TIG 3-shell encode + RLE + delta compress
            global _temporal
            if _temporal is None:
                _temporal = TIGTemporalEncoder(self.width, self.height)
            frame_type, compressed, stats = _temporal.encode_frame(pixels)

            # 4. Build frame packet: [4B length][2B width][2B height][data]
            header = struct.pack('>IHH', len(compressed), self.width, self.height)
            frame_packet = header + compressed

            # 5. Broadcast
            self._broadcast_frame(frame_packet)

            # Stats
            self.frame_count += 1
            self.total_bytes_sent += len(frame_packet)
            self.total_raw_bytes += raw_frame_size
            self._print_stats()

            # Frame pacing
            elapsed = time.time() - t_start
            sleep_time = frame_interval - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

    def stop(self):
        self.running = False
        with self.clients_lock:
            for conn in self.clients:
                try:
                    conn.close()
                except OSError:
                    pass
            self.clients.clear()


def main():
    parser = argparse.ArgumentParser(description="Force9 Screen Streaming Server")
    parser.add_argument('--port', type=int, default=7778, help='TCP port (default: 7778)')
    parser.add_argument('--fps', type=int, default=30, help='Target FPS (default: 30)')
    parser.add_argument('--width', type=int, default=1920, help='Capture width (default: 1920)')
    parser.add_argument('--height', type=int, default=1080, help='Capture height (default: 1080)')
    args = parser.parse_args()

    server = StreamServer(args.port, args.fps, args.width, args.height)
    try:
        server.start()
    except KeyboardInterrupt:
        print("\n[server] Shutting down...")
        server.stop()


if __name__ == '__main__':
    main()
