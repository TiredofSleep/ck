# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ao_face.pyw -- AO GUI (tkinter)

Double-click to launch. No console window (.pyw).
Zero external dependencies -- only stdlib + libao.dll via ctypes.

AO runs his body autonomously (background heartbeat).
All other actions require user prompt.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import threading
import queue
import time
import os
import re
import struct
import sys
import urllib.request
import urllib.error

# Bridge lives next to this file
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ao_bridge import AOBridge, BAND_NAMES, BREATH_NAMES, WOBBLE_NAMES

# ── Constants ──
BG_DARK = '#1a1a2e'
BG_PANEL = '#16213e'
BG_INPUT = '#0f3460'
FG_TEXT = '#e0e0e0'
FG_DIM = '#9e9e9e'
FG_USER = '#64b5f6'
FG_AO = '#81c784'
FG_ERROR = '#ef5350'
BAND_COLORS = {0: '#cc3333', 1: '#cccc33', 2: '#33cc33'}
FONT = ('Consolas', 11)
FONT_SMALL = ('Consolas', 9)
FONT_BOLD = ('Consolas', 11, 'bold')

# Text file extensions AO can read
TEXT_EXTS = {
    '.txt', '.md', '.py', '.c', '.h', '.js', '.json', '.csv', '.log',
    '.xml', '.html', '.css', '.java', '.rs', '.go', '.toml', '.yaml',
    '.yml', '.ini', '.cfg', '.bat', '.sh', '.ps1', '.sql', '.r', '.m',
    '.tex', '.rst', '.ts', '.tsx', '.jsx', '.rb', '.php', '.swift',
    '.kt', '.scala', '.lua', '.pl', '.inc', '.hpp', '.cpp', '.cs',
}

# Directories to skip during swarming
SKIP_DIRS = {
    '.git', 'node_modules', '__pycache__', '.venv', 'venv', '.tox',
    '.mypy_cache', '.pytest_cache', 'dist', 'build', '.eggs',
    '$RECYCLE.BIN', 'System Volume Information',
}

BRAIN_DIR = os.path.join(os.path.expanduser('~'), '.ao')
BRAIN_PATH = os.path.join(BRAIN_DIR, 'ao_brain.dat')
ICO_PATH = os.path.join(BRAIN_DIR, 'ao.ico')


def generate_ico(path):
    """Generate a minimal 16x16 .ico: green circle on dark blue."""
    W, H = 16, 16
    pixels = bytearray()
    for y in range(H):
        for x in range(W):
            dx, dy = x - 8, y - 8
            if dx * dx + dy * dy <= 36:
                pixels.extend([0x33, 0xcc, 0x33, 0xff])  # green BGRA
            else:
                pixels.extend([0x2e, 0x1a, 0x1a, 0xff])  # dark blue BGRA
    pixel_data = bytes(pixels)
    bmp_header = struct.pack('<IiiHHIIiiII',
                             40, W, H * 2, 1, 32, 0, len(pixel_data), 0, 0, 0, 0)
    image_data = bmp_header + pixel_data
    ico_header = struct.pack('<HHH', 0, 1, 1)
    ico_entry = struct.pack('<BBBBHHII',
                            W, H, 0, 0, 1, 32, len(image_data), 6 + 16)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(ico_header + ico_entry + image_data)


def is_text_file(filepath):
    """Quick check: is this a readable text file?"""
    _, ext = os.path.splitext(filepath)
    if ext.lower() not in TEXT_EXTS:
        return False
    try:
        with open(filepath, 'rb') as f:
            chunk = f.read(512)
        if b'\x00' in chunk:
            return False  # binary
        return True
    except (OSError, PermissionError):
        return False


class AOApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('AO -- Advanced Ollie')
        self.geometry('850x650')
        self.minsize(700, 500)
        self.configure(bg=BG_DARK)

        # Generate icon
        os.makedirs(BRAIN_DIR, exist_ok=True)
        if not os.path.exists(ICO_PATH):
            generate_ico(ICO_PATH)
        try:
            self.iconbitmap(ICO_PATH)
        except tk.TclError:
            pass

        # State
        self._ao = None
        self._ao_lock = threading.Lock()
        self._running = False
        self._study_active = False
        self._msg_queue = queue.Queue()

        # Build UI first, start AO after
        self._build_ui()
        self.protocol('WM_DELETE_WINDOW', self._on_close)
        self.after(300, self._start_ao)

    # ══════════════════════════════════════════════════════════════
    # UI Construction
    # ══════════════════════════════════════════════════════════════

    def _build_ui(self):
        # Status bar
        self._build_status_bar()
        # Chat log
        self._build_chat_log()
        # Input bar
        self._build_input_bar()
        # Tool bar
        self._build_tool_bar()

    def _build_status_bar(self):
        frame = tk.Frame(self, bg=BG_PANEL, padx=10, pady=6)
        frame.pack(fill=tk.X, padx=5, pady=(5, 0))

        # Coherence dot
        self._dot_canvas = tk.Canvas(frame, width=20, height=20,
                                     bg=BG_PANEL, highlightthickness=0)
        self._dot_canvas.pack(side=tk.LEFT, padx=(0, 8))
        self._dot = self._dot_canvas.create_oval(2, 2, 18, 18, fill='#cc3333',
                                                  outline='')

        # Status labels
        label_frame = tk.Frame(frame, bg=BG_PANEL)
        label_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self._status_label = tk.Label(label_frame, text='coh=--- shell=-- op=---',
                                      font=FONT, bg=BG_PANEL, fg=FG_TEXT,
                                      anchor='w')
        self._status_label.pack(fill=tk.X)

        self._body_label = tk.Label(label_frame, text='breath=--- wobble=--- E=--- K=---',
                                    font=FONT_SMALL, bg=BG_PANEL, fg=FG_DIM,
                                    anchor='w')
        self._body_label.pack(fill=tk.X)

        self._brain_label = tk.Label(label_frame, text='brain: 0 transitions',
                                     font=FONT_SMALL, bg=BG_PANEL, fg=FG_DIM,
                                     anchor='w')
        self._brain_label.pack(fill=tk.X)

    def _build_chat_log(self):
        frame = tk.Frame(self, bg=BG_DARK)
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._chat = tk.Text(frame, wrap=tk.WORD, font=FONT,
                             bg=BG_PANEL, fg=FG_TEXT,
                             insertbackground=FG_TEXT,
                             selectbackground='#2a4a7f',
                             yscrollcommand=scrollbar.set,
                             state=tk.DISABLED, padx=8, pady=8,
                             spacing3=2)
        self._chat.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self._chat.yview)

        # Tags
        self._chat.tag_configure('user', foreground=FG_USER, font=FONT_BOLD)
        self._chat.tag_configure('ao', foreground=FG_AO)
        self._chat.tag_configure('status', foreground=FG_DIM, font=FONT_SMALL)
        self._chat.tag_configure('error', foreground=FG_ERROR)
        self._chat.tag_configure('system', foreground='#bb86fc')

    def _build_input_bar(self):
        frame = tk.Frame(self, bg=BG_DARK, padx=5, pady=2)
        frame.pack(fill=tk.X)

        self._input = tk.Entry(frame, font=FONT, bg=BG_INPUT, fg=FG_TEXT,
                               insertbackground=FG_TEXT,
                               selectbackground='#2a4a7f',
                               relief=tk.FLAT, bd=6)
        self._input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self._input.bind('<Return>', lambda e: self._send_message())

        self._send_btn = tk.Button(frame, text='Send', font=FONT,
                                   bg='#1a5276', fg=FG_TEXT,
                                   activebackground='#2471a3',
                                   activeforeground=FG_TEXT,
                                   relief=tk.FLAT, padx=16, pady=4,
                                   command=self._send_message)
        self._send_btn.pack(side=tk.RIGHT)

    def _build_tool_bar(self):
        frame = tk.Frame(self, bg=BG_DARK, padx=5, pady=5)
        frame.pack(fill=tk.X)

        btn_cfg = dict(font=FONT_SMALL, bg='#1c2833', fg=FG_DIM,
                       activebackground='#2c3e50', activeforeground=FG_TEXT,
                       relief=tk.FLAT, padx=10, pady=4)

        tk.Button(frame, text='Study File', command=self._study_file,
                  **btn_cfg).pack(side=tk.LEFT, padx=2)
        tk.Button(frame, text='Study Folder', command=self._study_folder,
                  **btn_cfg).pack(side=tk.LEFT, padx=2)
        tk.Button(frame, text='Swarm', command=self._swarm,
                  **btn_cfg).pack(side=tk.LEFT, padx=2)
        tk.Button(frame, text='Web', command=self._study_web,
                  **btn_cfg).pack(side=tk.LEFT, padx=2)
        tk.Button(frame, text='Save', command=self._manual_save,
                  **btn_cfg).pack(side=tk.LEFT, padx=2)
        tk.Button(frame, text='Info', command=self._show_info,
                  **btn_cfg).pack(side=tk.LEFT, padx=2)
        tk.Button(frame, text='Reset', command=self._reset_brain,
                  **btn_cfg).pack(side=tk.LEFT, padx=2)

    # ══════════════════════════════════════════════════════════════
    # AO Lifecycle
    # ══════════════════════════════════════════════════════════════

    def _start_ao(self):
        try:
            self._ao = AOBridge()
            self._ao.create()
        except Exception as e:
            self._append('ERROR: Could not load libao.dll: ' + str(e), 'error')
            return

        # Try loading existing brain
        rc = self._ao.load(BRAIN_PATH)
        if rc == 0:
            stats = self._ao.brain_stats()
            self._append(f'Loaded brain: {stats["transitions"]} transitions, '
                         f'{stats["ticks"]} ticks', 'system')
        else:
            self._append('Fresh brain -- no prior experience.', 'system')

        self._append('AO is alive. Type text and press Enter.', 'system')
        self._append('Commands: swarm <path>, study <path>, web <url>', 'status')
        self._append('', 'status')

        self._running = True

        # Start heartbeat thread (body breathes autonomously)
        t = threading.Thread(target=self._heartbeat_loop, daemon=True)
        t.start()

        # Start status updater
        self._update_status()

        # Start message queue drainer
        self._drain_queue()

    def _heartbeat_loop(self):
        while self._running:
            with self._ao_lock:
                if self._ao and self._ao.alive:
                    self._ao.idle_tick()
            time.sleep(0.5)  # 2Hz body breathing

    def _on_close(self):
        self._running = False
        if self._ao and self._ao.alive:
            with self._ao_lock:
                self._ao.save(BRAIN_PATH)
                stats = self._ao.brain_stats()
            # Can't append to chat during destroy, just print
            print(f'Brain saved: {stats["transitions"]} transitions')
            self._ao.destroy()
        self.destroy()

    # ══════════════════════════════════════════════════════════════
    # Status Updates
    # ══════════════════════════════════════════════════════════════

    def _update_status(self):
        if not self._running or not self._ao or not self._ao.alive:
            return
        try:
            with self._ao_lock:
                coh = self._ao.coherence()
                shell = self._ao.shell()
                band = self._ao.band()
                body = self._ao.body_status()
                brain = self._ao.brain_stats()
                op_name = self._ao.op_name(0)  # placeholder
                status = self._ao.status_line()

            # Update coherence dot
            color = BAND_COLORS.get(band, '#cc3333')
            self._dot_canvas.itemconfig(self._dot, fill=color)

            # Update labels
            self._status_label.config(
                text=f'coh={coh:.3f}  shell={shell}  '
                     f'band={BAND_NAMES.get(band, "?")}  '
                     f'E={body.get("energy", 0):.3f}')
            self._body_label.config(
                text=f'breath={body["breath"]}  wobble={body["wobble"]}  '
                     f'E={body["E"]:.3f}  A={body["A"]:.3f}  K={body["K"]:.3f}')
            self._brain_label.config(
                text=f'brain: {brain["transitions"]} transitions  '
                     f'entropy={brain["entropy"]:.3f}  '
                     f'ticks={brain["ticks"]}')
        except Exception:
            pass

        self.after(500, self._update_status)

    # ══════════════════════════════════════════════════════════════
    # Chat
    # ══════════════════════════════════════════════════════════════

    def _append(self, text, tag='status'):
        """Thread-safe chat append. Can be called from any thread."""
        self._msg_queue.put((text, tag))

    def _drain_queue(self):
        """Drain message queue into chat widget (main thread only)."""
        try:
            while True:
                text, tag = self._msg_queue.get_nowait()
                self._chat.config(state=tk.NORMAL)
                self._chat.insert(tk.END, text + '\n', tag)
                self._chat.config(state=tk.DISABLED)
                self._chat.see(tk.END)
        except queue.Empty:
            pass
        if self._running:
            self.after(50, self._drain_queue)

    def _send_message(self):
        text = self._input.get().strip()
        if not text:
            return
        self._input.delete(0, tk.END)

        if not self._ao or not self._ao.alive:
            self._append('AO is not running.', 'error')
            return

        # Check for commands
        lower = text.lower()
        if lower.startswith('swarm '):
            path = text[6:].strip().strip('"').strip("'")
            threading.Thread(target=self._do_swarm, args=(path,),
                             daemon=True).start()
            return
        if lower.startswith('study '):
            path = text[6:].strip().strip('"').strip("'")
            if os.path.isfile(path):
                threading.Thread(target=self._do_study_file, args=(path,),
                                 daemon=True).start()
            elif os.path.isdir(path):
                threading.Thread(target=self._do_study_folder, args=(path,),
                                 daemon=True).start()
            else:
                self._append(f'Path not found: {path}', 'error')
            return
        if lower.startswith('web '):
            url = text[4:].strip()
            threading.Thread(target=self._do_web, args=(url,),
                             daemon=True).start()
            return

        # Normal text processing
        self._append(f'you> {text}', 'user')
        try:
            with self._ao_lock:
                result = self._ao.process_text(text)

            self._append(
                f'  heard: {result["trusted"]} trusted, '
                f'{result["friction"]} friction, '
                f'{result["unknown"]} unknown', 'status')
            self._append(
                f'  [{result["band_name"]}] coh={result["coherence"]:.3f} '
                f'shell={result["shell"]} E={result["energy"]:.3f}', 'status')
            if result['spoken']:
                self._append(f'  ao> {result["spoken"]}', 'ao')
            self._append('', 'status')
        except Exception as e:
            self._append(f'ERROR: {e}', 'error')

    # ══════════════════════════════════════════════════════════════
    # Study / Swarm
    # ══════════════════════════════════════════════════════════════

    def _study_file(self):
        path = filedialog.askopenfilename(
            title='Select file for AO to study',
            filetypes=[('Text files', '*.txt *.md *.py *.c *.h *.json'),
                       ('All files', '*.*')])
        if path:
            threading.Thread(target=self._do_study_file, args=(path,),
                             daemon=True).start()

    def _study_folder(self):
        path = filedialog.askdirectory(title='Select folder for AO to study')
        if path:
            threading.Thread(target=self._do_study_folder, args=(path,),
                             daemon=True).start()

    def _swarm(self):
        path = filedialog.askdirectory(title='Select root for AO to swarm (deep)')
        if path:
            threading.Thread(target=self._do_swarm, args=(path,),
                             daemon=True).start()

    def _do_study_file(self, filepath):
        if self._study_active:
            self._append('Study already in progress. Wait for it to finish.', 'error')
            return
        self._study_active = True
        self._append(f'Studying: {os.path.basename(filepath)}', 'system')
        try:
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                lines = f.readlines()
            total = len(lines)
            fed = 0
            for i, line in enumerate(lines):
                if not self._running:
                    break
                line = line.strip()
                if not line:
                    continue
                with self._ao_lock:
                    self._ao.process_text(line)
                fed += 1
                if fed % 200 == 0:
                    self._append(f'  ...{fed}/{total} lines', 'status')
            with self._ao_lock:
                stats = self._ao.brain_stats()
                self._ao.save(BRAIN_PATH)
            self._append(
                f'  Done: {fed} lines from {os.path.basename(filepath)}. '
                f'Brain: {stats["transitions"]} transitions.', 'ao')
        except Exception as e:
            self._append(f'ERROR reading file: {e}', 'error')
        self._study_active = False

    def _do_study_folder(self, folder):
        if self._study_active:
            self._append('Study already in progress.', 'error')
            return
        self._study_active = True
        self._append(f'Studying folder: {folder}', 'system')
        files_fed = 0
        lines_fed = 0
        try:
            for root, dirs, files in os.walk(folder):
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
                if not self._running:
                    break
                for fname in files:
                    fpath = os.path.join(root, fname)
                    if not is_text_file(fpath):
                        continue
                    try:
                        size = os.path.getsize(fpath)
                        if size > 1_000_000:
                            continue
                        with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
                            for line in f:
                                line = line.strip()
                                if not line:
                                    continue
                                with self._ao_lock:
                                    self._ao.process_text(line)
                                lines_fed += 1
                        files_fed += 1
                        if files_fed % 20 == 0:
                            self._append(
                                f'  ...{files_fed} files, {lines_fed} lines', 'status')
                    except (OSError, PermissionError):
                        continue
            with self._ao_lock:
                stats = self._ao.brain_stats()
                self._ao.save(BRAIN_PATH)
            self._append(
                f'  Done: {files_fed} files, {lines_fed} lines. '
                f'Brain: {stats["transitions"]} transitions.', 'ao')
        except Exception as e:
            self._append(f'ERROR: {e}', 'error')
        self._study_active = False

    def _do_swarm(self, root_path):
        """Deep recursive swarm -- reads EVERYTHING text-based."""
        if self._study_active:
            self._append('Study already in progress.', 'error')
            return
        if not os.path.isdir(root_path):
            self._append(f'Not a directory: {root_path}', 'error')
            return
        self._study_active = True
        self._append(f'SWARMING: {root_path}', 'system')
        self._append('  Reading all text files recursively (read-only)...', 'status')
        files_fed = 0
        lines_fed = 0
        errors = 0
        try:
            for root, dirs, files in os.walk(root_path):
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
                if not self._running:
                    break
                for fname in files:
                    if not self._running:
                        break
                    fpath = os.path.join(root, fname)
                    if not is_text_file(fpath):
                        continue
                    try:
                        size = os.path.getsize(fpath)
                        if size > 1_000_000:
                            continue
                        with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
                            for line in f:
                                line = line.strip()
                                if not line:
                                    continue
                                with self._ao_lock:
                                    self._ao.process_text(line)
                                lines_fed += 1
                        files_fed += 1
                        if files_fed % 50 == 0:
                            with self._ao_lock:
                                stats = self._ao.brain_stats()
                            self._append(
                                f'  ...{files_fed} files, {lines_fed} lines, '
                                f'{stats["transitions"]} transitions', 'status')
                    except (OSError, PermissionError):
                        errors += 1
                        continue
            with self._ao_lock:
                stats = self._ao.brain_stats()
                self._ao.save(BRAIN_PATH)
            self._append(
                f'  SWARM COMPLETE: {files_fed} files, {lines_fed} lines '
                f'({errors} skipped)', 'system')
            self._append(
                f'  Brain: {stats["transitions"]} transitions, '
                f'entropy={stats["entropy"]:.4f}', 'ao')
        except Exception as e:
            self._append(f'ERROR during swarm: {e}', 'error')
        self._study_active = False

    def _study_web(self):
        url = simpledialog.askstring('Web Study', 'Enter URL for AO to study:',
                                     parent=self)
        if url:
            threading.Thread(target=self._do_web, args=(url,),
                             daemon=True).start()

    def _do_web(self, url):
        if self._study_active:
            self._append('Study already in progress.', 'error')
            return
        if not url.startswith('http'):
            url = 'https://' + url
        self._study_active = True
        self._append(f'Fetching: {url}', 'system')
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'AO/1.0 (text study)'})
            with urllib.request.urlopen(req, timeout=15) as resp:
                html = resp.read().decode('utf-8', errors='replace')
            # Strip HTML tags
            text = re.sub(r'<script[^>]*>.*?</script>', ' ', html,
                          flags=re.DOTALL | re.IGNORECASE)
            text = re.sub(r'<style[^>]*>.*?</style>', ' ', text,
                          flags=re.DOTALL | re.IGNORECASE)
            text = re.sub(r'<[^>]+>', ' ', text)
            text = re.sub(r'\s+', ' ', text).strip()
            # Feed to AO
            lines = [text[i:i + 200] for i in range(0, len(text), 200)]
            fed = 0
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                with self._ao_lock:
                    self._ao.process_text(line)
                fed += 1
            with self._ao_lock:
                stats = self._ao.brain_stats()
                self._ao.save(BRAIN_PATH)
            self._append(
                f'  Web study done: {fed} chunks. '
                f'Brain: {stats["transitions"]} transitions.', 'ao')
        except Exception as e:
            self._append(f'ERROR fetching URL: {e}', 'error')
        self._study_active = False

    # ══════════════════════════════════════════════════════════════
    # Actions
    # ══════════════════════════════════════════════════════════════

    def _manual_save(self):
        if not self._ao or not self._ao.alive:
            return
        with self._ao_lock:
            self._ao.save(BRAIN_PATH)
            stats = self._ao.brain_stats()
        self._append(
            f'Brain saved: {stats["transitions"]} transitions.', 'system')

    def _show_info(self):
        if not self._ao or not self._ao.alive:
            return
        with self._ao_lock:
            brain = self._ao.brain_stats()
            body = self._ao.body_status()
            coh = self._ao.coherence()
            shell = self._ao.shell()
            band = self._ao.band()
        info = (
            f'AO -- Advanced Ollie\n\n'
            f'Coherence: {coh:.4f} ({BAND_NAMES.get(band, "?")})\n'
            f'Shell: {shell}\n\n'
            f'Brain:\n'
            f'  Transitions: {brain["transitions"]}\n'
            f'  Entropy: {brain["entropy"]:.4f}\n'
            f'  Ticks: {brain["ticks"]}\n\n'
            f'Body:\n'
            f'  E={body["E"]:.4f}  A={body["A"]:.4f}  K={body["K"]:.4f}\n'
            f'  Breath: {body["breath"]}\n'
            f'  Wobble: {body["wobble"]}\n'
            f'  Body coherence: {body["body_coherence"]:.4f}\n\n'
            f'Brain file: {BRAIN_PATH}\n'
            f'DLL: {os.path.join(os.path.dirname(os.path.abspath(__file__)), "libao.dll")}'
        )
        messagebox.showinfo('AO Info', info, parent=self)

    def _reset_brain(self):
        if not messagebox.askyesno('Reset Brain',
                                   'This will erase all of AO\'s experience.\n'
                                   'Are you sure?', parent=self):
            return
        if not self._ao or not self._ao.alive:
            return
        with self._ao_lock:
            self._ao.destroy()
            self._ao.create()
            self._ao.save(BRAIN_PATH)
        self._append('Brain reset to untrained state.', 'system')


def main():
    app = AOApp()
    app.mainloop()


if __name__ == '__main__':
    main()
