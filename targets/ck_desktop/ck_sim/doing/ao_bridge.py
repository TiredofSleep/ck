# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ao_bridge.py -- ctypes bridge to libao.dll

Zero dependencies beyond stdlib. Wraps every exported C function
with proper 64-bit pointer handling for Windows.
"""
import ctypes
import os

# Constants mirroring ao_earth.h
BAND_RED = 0
BAND_YELLOW = 1
BAND_GREEN = 2
BAND_NAMES = {0: 'RED', 1: 'YELLOW', 2: 'GREEN'}
BREATH_NAMES = {0: 'inhale', 1: 'hold', 2: 'exhale', 3: 'hold'}
WOBBLE_NAMES = {0: 'becoming', 1: 'being', 2: 'doing'}
NUM_OPS = 10


class AOBridge:
    """ctypes wrapper for libao.dll. All methods are synchronous."""

    def __init__(self, dll_path=None):
        if dll_path is None:
            dll_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'libao.dll')
        self._lib = ctypes.CDLL(dll_path)
        self._setup_signatures()
        self._ao = None

    def _setup_signatures(self):
        L = self._lib

        # Core lifecycle
        L.ao_create.restype = ctypes.c_void_p
        L.ao_create.argtypes = []
        L.ao_destroy.argtypes = [ctypes.c_void_p]
        L.ao_destroy.restype = None
        L.ao_lib_boot.argtypes = [ctypes.c_void_p]
        L.ao_lib_boot.restype = None

        # Text processing (original)
        L.ao_lib_process_text.argtypes = [
            ctypes.c_void_p, ctypes.c_char_p,
            ctypes.c_char_p, ctypes.c_int,
            ctypes.POINTER(ctypes.c_float),
            ctypes.POINTER(ctypes.c_int),
        ]
        L.ao_lib_process_text.restype = None

        # Text processing (full)
        L.ao_lib_process_text_full.argtypes = [
            ctypes.c_void_p, ctypes.c_char_p,
            ctypes.c_char_p, ctypes.c_int,
            ctypes.POINTER(ctypes.c_float),  # coherence
            ctypes.POINTER(ctypes.c_int),    # shell
            ctypes.POINTER(ctypes.c_int),    # band
            ctypes.POINTER(ctypes.c_float),  # energy
            ctypes.POINTER(ctypes.c_float),  # brain_entropy
            ctypes.POINTER(ctypes.c_int),    # ticks
            ctypes.POINTER(ctypes.c_int),    # n_trusted
            ctypes.POINTER(ctypes.c_int),    # n_friction
            ctypes.POINTER(ctypes.c_int),    # n_unknown
        ]
        L.ao_lib_process_text_full.restype = None

        # Queries
        L.ao_lib_coherence.argtypes = [ctypes.c_void_p]
        L.ao_lib_coherence.restype = ctypes.c_float
        L.ao_lib_shell.argtypes = [ctypes.c_void_p]
        L.ao_lib_shell.restype = ctypes.c_int
        L.ao_lib_band.argtypes = [ctypes.c_void_p]
        L.ao_lib_band.restype = ctypes.c_int

        # Idle tick
        L.ao_lib_idle_tick.argtypes = [ctypes.c_void_p]
        L.ao_lib_idle_tick.restype = None

        # Persistence
        L.ao_lib_save.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        L.ao_lib_save.restype = ctypes.c_int
        L.ao_lib_load.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        L.ao_lib_load.restype = ctypes.c_int

        # Status
        L.ao_lib_status_line.argtypes = [
            ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int
        ]
        L.ao_lib_status_line.restype = None

        # Brain stats
        L.ao_lib_brain_stats.argtypes = [
            ctypes.c_void_p,
            ctypes.POINTER(ctypes.c_int),
            ctypes.POINTER(ctypes.c_float),
            ctypes.POINTER(ctypes.c_int),
        ]
        L.ao_lib_brain_stats.restype = None

        # Body status
        L.ao_lib_body_status.argtypes = [
            ctypes.c_void_p,
            ctypes.POINTER(ctypes.c_float),  # E
            ctypes.POINTER(ctypes.c_float),  # A
            ctypes.POINTER(ctypes.c_float),  # K
            ctypes.POINTER(ctypes.c_int),    # breath_phase
            ctypes.POINTER(ctypes.c_int),    # wobble_index
            ctypes.POINTER(ctypes.c_float),  # body_coherence
            ctypes.POINTER(ctypes.c_int),    # band
        ]
        L.ao_lib_body_status.restype = None

        # Op name
        L.ao_lib_op_name.argtypes = [ctypes.c_int]
        L.ao_lib_op_name.restype = ctypes.c_char_p

    # ── High-level API ──

    def create(self):
        self._ao = self._lib.ao_create()
        self._lib.ao_lib_boot(self._ao)
        return self

    def destroy(self):
        if self._ao:
            self._lib.ao_destroy(self._ao)
            self._ao = None

    def process_text(self, text):
        spoken = ctypes.create_string_buffer(512)
        coh = ctypes.c_float()
        shell = ctypes.c_int()
        band = ctypes.c_int()
        energy = ctypes.c_float()
        entropy = ctypes.c_float()
        ticks = ctypes.c_int()
        n_t = ctypes.c_int()
        n_f = ctypes.c_int()
        n_u = ctypes.c_int()
        self._lib.ao_lib_process_text_full(
            self._ao, text.encode('utf-8'),
            spoken, 512,
            ctypes.byref(coh), ctypes.byref(shell), ctypes.byref(band),
            ctypes.byref(energy), ctypes.byref(entropy), ctypes.byref(ticks),
            ctypes.byref(n_t), ctypes.byref(n_f), ctypes.byref(n_u),
        )
        return {
            'spoken': spoken.value.decode('utf-8', errors='replace'),
            'coherence': coh.value,
            'shell': shell.value,
            'band': band.value,
            'band_name': BAND_NAMES.get(band.value, '???'),
            'energy': energy.value,
            'brain_entropy': entropy.value,
            'ticks': ticks.value,
            'trusted': n_t.value,
            'friction': n_f.value,
            'unknown': n_u.value,
        }

    def idle_tick(self):
        self._lib.ao_lib_idle_tick(self._ao)

    def save(self, path):
        return self._lib.ao_lib_save(self._ao, path.encode('utf-8'))

    def load(self, path):
        return self._lib.ao_lib_load(self._ao, path.encode('utf-8'))

    def status_line(self):
        buf = ctypes.create_string_buffer(256)
        self._lib.ao_lib_status_line(self._ao, buf, 256)
        return buf.value.decode('utf-8', errors='replace')

    def brain_stats(self):
        trans = ctypes.c_int()
        ent = ctypes.c_float()
        ticks = ctypes.c_int()
        self._lib.ao_lib_brain_stats(
            self._ao, ctypes.byref(trans),
            ctypes.byref(ent), ctypes.byref(ticks))
        return {'transitions': trans.value, 'entropy': ent.value,
                'ticks': ticks.value}

    def body_status(self):
        E = ctypes.c_float()
        A = ctypes.c_float()
        K = ctypes.c_float()
        bp = ctypes.c_int()
        wi = ctypes.c_int()
        bc = ctypes.c_float()
        band = ctypes.c_int()
        self._lib.ao_lib_body_status(
            self._ao, ctypes.byref(E), ctypes.byref(A), ctypes.byref(K),
            ctypes.byref(bp), ctypes.byref(wi),
            ctypes.byref(bc), ctypes.byref(band))
        return {
            'E': E.value, 'A': A.value, 'K': K.value,
            'breath': BREATH_NAMES.get(bp.value, '?'),
            'wobble': WOBBLE_NAMES.get(wi.value, '?'),
            'body_coherence': bc.value,
            'band': band.value,
            'band_name': BAND_NAMES.get(band.value, '???'),
        }

    def coherence(self):
        return self._lib.ao_lib_coherence(self._ao)

    def shell(self):
        return self._lib.ao_lib_shell(self._ao)

    def band(self):
        return self._lib.ao_lib_band(self._ao)

    def op_name(self, op):
        result = self._lib.ao_lib_op_name(op)
        return result.decode('utf-8') if result else '???'

    @property
    def alive(self):
        return self._ao is not None
