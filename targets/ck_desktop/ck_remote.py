"""
ck_remote.py -- CK Remote Desktop (Force9 Visual Codec)
Packages Force9 screen compression + virtual display capture.

  SERVER:  python ck_remote.py --serve --port 7780 --monitor 1 --fps 30
  CLIENT:  python ck_remote.py --connect 192.168.1.50 --port 7780

(c) 2026 Brayden Sanders / 7Site LLC
"""
import argparse, ctypes, ctypes.wintypes, socket, struct, sys, os
import threading, time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ck_sim.being.ck_screen_compress import (
    rgb_array_to_force9, compress_force9_stream,
    decompress_force9_stream, force9_to_rgb,
)

SRCCOPY = 0x00CC0020

# Pre-built decode LUT: packed value (0-728) -> (R, G, B)
_DECODE_LUT = np.zeros((729, 3), dtype=np.uint8)
for _v in range(729):
    _DECODE_LUT[_v] = force9_to_rgb(_v)

def get_monitor_rects():
    """Return list of (x, y, w, h) for each monitor via EnumDisplayMonitors."""
    monitors = []
    ENUMPROC = ctypes.WINFUNCTYPE(
        ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p,
        ctypes.POINTER(ctypes.wintypes.RECT), ctypes.c_void_p)
    def cb(hmon, hdc, lprect, lparam):
        r = lprect.contents
        monitors.append((r.left, r.top, r.right - r.left, r.bottom - r.top))
        return 1
    ctypes.windll.user32.EnumDisplayMonitors(None, None, ENUMPROC(cb), 0)
    return monitors

def capture_rect(x, y, w, h):
    """Capture screen region via GDI BitBlt. Returns (N, 3) uint8 RGB."""
    u32, g32 = ctypes.windll.user32, ctypes.windll.gdi32
    hdc = u32.GetDC(0)
    memdc = g32.CreateCompatibleDC(hdc)
    bmp = g32.CreateCompatibleBitmap(hdc, w, h)
    g32.SelectObject(memdc, bmp)
    g32.BitBlt(memdc, 0, 0, w, h, hdc, x, y, SRCCOPY)
    buf = (ctypes.c_char * (w * h * 4))()
    bi = struct.pack('iiiHHIIiiII', 40, w, -h, 1, 32, 0, 0, 0, 0, 0, 0)
    g32.GetDIBits(memdc, bmp, 0, h, buf, ctypes.create_string_buffer(bi), 0)
    raw = np.frombuffer(buf, dtype=np.uint8).reshape(w * h, 4)
    pixels = raw[:, [2, 1, 0]].copy()
    g32.DeleteObject(bmp); g32.DeleteDC(memdc); u32.ReleaseDC(0, hdc)
    return pixels


class RemoteServer:
    def __init__(self, port, fps, monitor_index):
        self.port, self.target_fps = port, fps
        self.clients, self.lock, self.running = [], threading.Lock(), False
        monitors = get_monitor_rects()
        if monitor_index >= len(monitors):
            print("[server] Monitor %d not found (%d avail), using 0" % (
                monitor_index, len(monitors)))
            monitor_index = 0
        self.mx, self.my, self.mw, self.mh = monitors[monitor_index]
        self.mi = monitor_index
        self.has_audio = False
        try:
            import sounddevice; self.has_audio = True  # noqa: F401,E702
        except ImportError:
            pass

    def start(self):
        self.running = True
        threading.Thread(target=self._accept, daemon=True).start()
        print("[server] CK Remote Desktop -- Force9 Codec")
        print("[server] Monitor %d: %dx%d at (%d,%d)  FPS: %d  Port: %d" % (
            self.mi, self.mw, self.mh, self.mx, self.my,
            self.target_fps, self.port))
        print("[server] Audio: %s" % ("yes" if self.has_audio else "no"))
        self._capture_loop()

    def _accept(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('0.0.0.0', self.port)); sock.listen(5); sock.settimeout(1.0)
        while self.running:
            try:
                conn, addr = sock.accept()
                conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                conn.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1 << 20)
                with self.lock:
                    self.clients.append(conn)
                print("[server] + %s:%d  (%d clients)" % (
                    addr[0], addr[1], len(self.clients)))
            except socket.timeout:
                continue
            except OSError:
                break
        sock.close()

    def _broadcast(self, data):
        dead = []
        with self.lock:
            for c in self.clients:
                try:
                    c.sendall(data)
                except (BrokenPipeError, ConnectionResetError,
                        ConnectionAbortedError, OSError):
                    dead.append(c)
            for c in dead:
                self.clients.remove(c)
                try: c.close()
                except OSError: pass
        if dead:
            print("[server] - %d dropped  (%d remain)" % (
                len(dead), len(self.clients)))

    def _capture_loop(self):
        interval = 1.0 / self.target_fps
        w, h = self.mw, self.mh
        raw_size = w * h * 3
        fc, sent, t_stats = 0, 0, time.time()
        while self.running:
            t0 = time.time()
            with self.lock:
                if not self.clients:
                    time.sleep(0.1); continue
            pixels = capture_rect(self.mx, self.my, w, h)
            packed = rgb_array_to_force9(pixels)
            compressed, _ = compress_force9_stream(packed)
            header = struct.pack('>IHH', len(compressed), w, h)
            self._broadcast(header + compressed)
            fc += 1; sent += len(compressed) + 8
            now = time.time(); elapsed = now - t_stats
            if elapsed >= 1.0:
                fps = fc / elapsed; bw = sent / elapsed
                ratio = (raw_size * fc) / sent if sent else 0
                with self.lock: nc = len(self.clients)
                print("[stats] FPS:%.1f | %.1fx | %.2f MB/s | %d clients" % (
                    fps, ratio, bw / (1 << 20), nc))
                fc = sent = 0; t_stats = now
            sl = interval - (time.time() - t0)
            if sl > 0: time.sleep(sl)

    def stop(self):
        self.running = False
        with self.lock:
            for c in self.clients:
                try: c.close()
                except OSError: pass
            self.clients.clear()


class RemoteClient:
    def __init__(self, host, port):
        self.host, self.port = host, port
        self.sock, self.running = None, False
        self.frame_lock = threading.Lock()
        self.frame_ready = threading.Event()
        self.current_frame, self.cur_w, self.cur_h = None, 0, 0

    def _recv_exact(self, n):
        buf = bytearray()
        while len(buf) < n:
            chunk = self.sock.recv(n - len(buf))
            if not chunk: raise ConnectionError("Server disconnected")
            buf.extend(chunk)
        return bytes(buf)

    def _receive_loop(self):
        fc, total, t_stats = 0, 0, time.time()
        while self.running:
            try:
                header = self._recv_exact(8)
                data_len, w, h = struct.unpack('>IHH', header)
                compressed = self._recv_exact(data_len)
                t0 = time.time()
                packed = decompress_force9_stream(compressed, w * h)
                rgb = _DECODE_LUT[packed].reshape(h, w, 3)
                dec_ms = (time.time() - t0) * 1000
                with self.frame_lock:
                    self.current_frame, self.cur_w, self.cur_h = rgb, w, h
                self.frame_ready.set()
                fc += 1; total += data_len + 8
                now = time.time(); elapsed = now - t_stats
                if elapsed >= 1.0:
                    print("[stats] FPS:%.1f | %.2f MB/s | decode:%.1fms" % (
                        fc / elapsed, total / elapsed / (1 << 20), dec_ms))
                    fc = total = 0; t_stats = now
            except ConnectionError:
                print("[client] Server disconnected."); self.running = False
            except Exception as e:
                print("[client] Error: %s" % e); self.running = False

    def run(self):
        try: import pygame
        except ImportError:
            print("[error] pygame required: pip install pygame"); sys.exit(1)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1 << 20)
        print("[client] Connecting to %s:%d..." % (self.host, self.port))
        self.sock.connect((self.host, self.port))
        print("[client] Connected."); self.running = True
        threading.Thread(target=self._receive_loop, daemon=True).start()
        print("[client] Waiting for first frame...")
        self.frame_ready.wait(timeout=10.0)
        if not self.running:
            print("[client] No frames received."); return
        with self.frame_lock: ww, wh = self.cur_w, self.cur_h
        pygame.init()
        screen = pygame.display.set_mode((ww, wh))
        pygame.display.set_caption("CK Remote - %s:%d" % (self.host, self.port))
        clock = pygame.time.Clock()
        print("[client] Display: %dx%d" % (ww, wh))
        while self.running:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT: self.running = False
                elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                    self.running = False
            if self.frame_ready.is_set():
                with self.frame_lock:
                    frame, fw, fh = self.current_frame, self.cur_w, self.cur_h
                self.frame_ready.clear()
                if frame is not None:
                    if fw != ww or fh != wh:
                        ww, wh = fw, fh
                        screen = pygame.display.set_mode((ww, wh))
                    surf = pygame.surfarray.make_surface(
                        np.transpose(frame, (1, 0, 2)))
                    screen.blit(surf, (0, 0)); pygame.display.flip()
            clock.tick(60)
        pygame.quit()
        try: self.sock.close()
        except OSError: pass


def main():
    p = argparse.ArgumentParser(description="CK Remote Desktop -- Force9")
    m = p.add_mutually_exclusive_group(required=True)
    m.add_argument('--serve', action='store_true', help='Run as server')
    m.add_argument('--connect', type=str, metavar='HOST', help='Connect to HOST')
    p.add_argument('--port', type=int, default=7780, help='TCP port (7780)')
    p.add_argument('--monitor', type=int, default=1, help='Monitor index (1)')
    p.add_argument('--fps', type=int, default=30, help='Target FPS (30)')
    args = p.parse_args()
    if args.serve:
        srv = RemoteServer(args.port, args.fps, args.monitor)
        try: srv.start()
        except KeyboardInterrupt:
            print("\n[server] Shutting down..."); srv.stop()
    else:
        cli = RemoteClient(args.connect, args.port)
        try: cli.run()
        except KeyboardInterrupt:
            print("\n[client] Shutting down..."); cli.running = False
        except ConnectionRefusedError:
            print("[client] Cannot reach %s:%d" % (args.connect, args.port))

if __name__ == '__main__':
    main()
