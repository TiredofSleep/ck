"""
ck_stream_client.py -- Force9 Screen Streaming Client
Receives Force9 compressed frames, decompresses, displays in pygame window.

Usage: python ck_stream_client.py [--host localhost] [--port 7778]

(c) 2026 Brayden Sanders / 7Site LLC
"""

import argparse
import socket
import struct
import sys
import threading
import time
import numpy as np

try:
    import pygame
except ImportError:
    print("[error] pygame is required: pip install pygame")
    sys.exit(1)

# TIG Visual Encoder (3-shell CIELAB decoder)
from ck_sim.being.ck_visual_encoder import TIGVisualEncoder
_encoder = TIGVisualEncoder()


def shells_to_rgb(shell_bytes, width, height):
    """Decode TIG 3-shell data back to RGB."""
    shells = np.frombuffer(shell_bytes, dtype=np.uint16).reshape(-1, 3)
    return _encoder.decode(shells).reshape(height, width, 3)


class StreamClient:
    """TCP client that receives and displays Force9-compressed screen frames."""

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = None
        self.running = False
        self.frame_ready = threading.Event()
        self.frame_lock = threading.Lock()
        self.current_frame = None
        self.current_width = 0
        self.current_height = 0
        # Stats
        self.frame_count = 0
        self.total_bytes = 0
        self.stats_time = time.time()

    def connect(self):
        """Connect to the streaming server."""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024 * 1024)
        print("[client] Connecting to %s:%d..." % (self.host, self.port))
        self.sock.connect((self.host, self.port))
        print("[client] Connected.")

    def _recv_exact(self, n):
        """Receive exactly n bytes from socket."""
        data = bytearray()
        while len(data) < n:
            chunk = self.sock.recv(n - len(data))
            if not chunk:
                raise ConnectionError("Server disconnected")
            data.extend(chunk)
        return bytes(data)

    def _receive_loop(self):
        """Receive compressed frames from server."""
        while self.running:
            try:
                # Read header: [4B length][2B width][2B height]
                header = self._recv_exact(8)
                data_len, width, height = struct.unpack('>IHH', header)

                # Read compressed data
                compressed = self._recv_exact(data_len)

                t_start = time.time()

                # Decode TIG 3-shell back to RGB
                rgb_frame = shells_to_rgb(compressed, width, height)

                decompress_ms = (time.time() - t_start) * 1000

                # Store frame
                with self.frame_lock:
                    self.current_frame = rgb_frame
                    self.current_width = width
                    self.current_height = height
                self.frame_ready.set()

                # Stats
                self.frame_count += 1
                self.total_bytes += data_len + 8
                self._print_stats(decompress_ms)

            except ConnectionError:
                print("[client] Server disconnected.")
                self.running = False
                break
            except Exception as e:
                print("[client] Error: %s" % str(e))
                self.running = False
                break

    def _print_stats(self, decompress_ms):
        """Print stats every second."""
        now = time.time()
        elapsed = now - self.stats_time
        if elapsed >= 1.0:
            fps = self.frame_count / elapsed
            bw = self.total_bytes / elapsed
            print("[stats] FPS: %.1f | Bandwidth: %.2f MB/s | Decompress: %.1f ms" % (
                fps, bw / (1024 * 1024), decompress_ms))
            self.frame_count = 0
            self.total_bytes = 0
            self.stats_time = now

    def run(self):
        """Main loop: receive frames in background, display with pygame."""
        self.running = True
        self.connect()

        # Start receiver thread
        recv_thread = threading.Thread(target=self._receive_loop, daemon=True)
        recv_thread.start()

        # Wait for first frame to get dimensions
        print("[client] Waiting for first frame...")
        self.frame_ready.wait(timeout=10.0)
        if not self.running:
            print("[client] No frames received.")
            return

        with self.frame_lock:
            win_w = self.current_width
            win_h = self.current_height

        # Init pygame
        pygame.init()
        screen = pygame.display.set_mode((win_w, win_h))
        pygame.display.set_caption("Force9 Stream - %s:%d" % (self.host, self.port))
        clock = pygame.time.Clock()

        print("[client] Display: %dx%d" % (win_w, win_h))

        while self.running:
            # Handle pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        break

            if not self.running:
                break

            # Display latest frame
            if self.frame_ready.is_set():
                with self.frame_lock:
                    frame = self.current_frame
                    fw = self.current_width
                    fh = self.current_height
                self.frame_ready.clear()

                if frame is not None:
                    # Resize window if server resolution changed
                    if fw != win_w or fh != win_h:
                        win_w, win_h = fw, fh
                        screen = pygame.display.set_mode((win_w, win_h))

                    # numpy (H, W, 3) -> pygame surface
                    surf = pygame.surfarray.make_surface(
                        np.transpose(frame, (1, 0, 2)))
                    screen.blit(surf, (0, 0))
                    pygame.display.flip()

            clock.tick(60)  # cap display at 60Hz

        # Cleanup
        pygame.quit()
        if self.sock:
            try:
                self.sock.close()
            except OSError:
                pass

    def stop(self):
        self.running = False


def main():
    parser = argparse.ArgumentParser(description="Force9 Screen Streaming Client")
    parser.add_argument('--host', type=str, default='localhost',
                        help='Server host (default: localhost)')
    parser.add_argument('--port', type=int, default=7778,
                        help='Server port (default: 7778)')
    args = parser.parse_args()

    client = StreamClient(args.host, args.port)
    try:
        client.run()
    except KeyboardInterrupt:
        print("\n[client] Shutting down...")
        client.stop()
    except ConnectionRefusedError:
        print("[client] Could not connect to %s:%d -- is the server running?" % (
            args.host, args.port))


if __name__ == '__main__':
    main()
