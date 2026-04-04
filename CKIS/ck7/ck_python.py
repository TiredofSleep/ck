"""
ck_python.py — Python ctypes bridge to CK native library
═════════════════════════════════════════════════════════
Text processing stays Python. Math goes native.

Usage:
    from ck_python import CKNative
    ck = CKNative()           # loads ck.dll / libck.so
    ck.fuse([3, 7, 2, 5, 7])  # → 7 (harmony)
    ck.coherence_chain([3, 7, 2, 5, 7])  # → 0.75

(c) 2026 Brayden Sanders / 7Site LLC — TIG Unified Theory
"""

import ctypes
import ctypes.util
import os
import platform
from typing import List, Optional, Tuple


class CKNative:
    """Thin Python wrapper around ck.dll / libck.so"""

    def __init__(self, lib_path: Optional[str] = None):
        if lib_path is None:
            lib_path = self._find_library()
        self._lib = ctypes.CDLL(lib_path)
        self._setup_signatures()

    def _find_library(self) -> str:
        """Find ck.dll or libck.so relative to this file."""
        base = os.path.dirname(os.path.abspath(__file__))
        system = platform.system()

        candidates = []
        if system == 'Windows':
            candidates = [
                os.path.join(base, 'ck.dll'),
                os.path.join(base, 'build', 'Release', 'ck.dll'),
                os.path.join(base, 'build', 'Debug', 'ck.dll'),
                os.path.join(base, 'build', 'ck.dll'),
            ]
        else:
            candidates = [
                os.path.join(base, 'ck.so'),
                os.path.join(base, 'libck.so'),
                os.path.join(base, 'build', 'ck.so'),
                os.path.join(base, 'build', 'libck.so'),
            ]

        for path in candidates:
            if os.path.exists(path):
                return path

        raise FileNotFoundError(
            f"CK native library not found. Build with cmake first.\n"
            f"Searched: {candidates}"
        )

    def _setup_signatures(self):
        """Declare ctypes function signatures for type safety."""
        lib = self._lib

        # Pure math — stateless
        lib.ck_ffi_fuse.argtypes = [ctypes.POINTER(ctypes.c_int8), ctypes.c_int]
        lib.ck_ffi_fuse.restype = ctypes.c_int

        lib.ck_ffi_fuse2.argtypes = [ctypes.c_int, ctypes.c_int]
        lib.ck_ffi_fuse2.restype = ctypes.c_int

        lib.ck_ffi_fuse_table.argtypes = [ctypes.POINTER(ctypes.c_int8), ctypes.c_int, ctypes.c_int]
        lib.ck_ffi_fuse_table.restype = ctypes.c_int

        lib.ck_ffi_coherence_chain.argtypes = [ctypes.POINTER(ctypes.c_int8), ctypes.c_int]
        lib.ck_ffi_coherence_chain.restype = ctypes.c_float

        lib.ck_ffi_information.argtypes = [ctypes.POINTER(ctypes.c_int8), ctypes.c_int]
        lib.ck_ffi_information.restype = ctypes.c_float

        lib.ck_ffi_shape.argtypes = [ctypes.POINTER(ctypes.c_int8), ctypes.c_int]
        lib.ck_ffi_shape.restype = ctypes.c_int

        lib.ck_ffi_bump_signature.argtypes = [ctypes.POINTER(ctypes.c_int8), ctypes.c_int]
        lib.ck_ffi_bump_signature.restype = ctypes.c_int

        lib.ck_ffi_is_bump.argtypes = [ctypes.c_int, ctypes.c_int]
        lib.ck_ffi_is_bump.restype = ctypes.c_int

        lib.ck_ffi_s_star.argtypes = [ctypes.c_float, ctypes.c_float, ctypes.c_float]
        lib.ck_ffi_s_star.restype = ctypes.c_float

        lib.ck_ffi_coherence_eak.argtypes = [ctypes.c_float, ctypes.c_float, ctypes.c_float]
        lib.ck_ffi_coherence_eak.restype = ctypes.c_float

        lib.ck_ffi_band.argtypes = [ctypes.c_float]
        lib.ck_ffi_band.restype = ctypes.c_int

        lib.ck_ffi_cl_lookup.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
        lib.ck_ffi_cl_lookup.restype = ctypes.c_int

        lib.ck_ffi_t_star.argtypes = []
        lib.ck_ffi_t_star.restype = ctypes.c_float

        lib.ck_ffi_num_ops.argtypes = []
        lib.ck_ffi_num_ops.restype = ctypes.c_int

        lib.ck_ffi_gravity.argtypes = [ctypes.c_int]
        lib.ck_ffi_gravity.restype = ctypes.c_float

        # TL operations
        lib.ck_ffi_tl_create.argtypes = []
        lib.ck_ffi_tl_create.restype = ctypes.c_void_p

        lib.ck_ffi_tl_destroy.argtypes = [ctypes.c_void_p]
        lib.ck_ffi_tl_destroy.restype = None

        lib.ck_ffi_tl_eat_ops.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int8), ctypes.c_int]
        lib.ck_ffi_tl_eat_ops.restype = None

        lib.ck_ffi_tl_entropy.argtypes = [ctypes.c_void_p]
        lib.ck_ffi_tl_entropy.restype = ctypes.c_float

        lib.ck_ffi_tl_predict.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ctypes.c_float)]
        lib.ck_ffi_tl_predict.restype = ctypes.c_int

        lib.ck_ffi_tl_total.argtypes = [ctypes.c_void_p]
        lib.ck_ffi_tl_total.restype = ctypes.c_int64

        lib.ck_ffi_tl_save.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        lib.ck_ffi_tl_save.restype = ctypes.c_int

        lib.ck_ffi_tl_load.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        lib.ck_ffi_tl_load.restype = ctypes.c_int

        # Organism lifecycle
        lib.ck_ffi_create.argtypes = []
        lib.ck_ffi_create.restype = ctypes.c_void_p

        lib.ck_ffi_destroy.argtypes = [ctypes.c_void_p]
        lib.ck_ffi_destroy.restype = None

        lib.ck_ffi_tick.argtypes = [ctypes.c_void_p]
        lib.ck_ffi_tick.restype = ctypes.c_int

        lib.ck_ffi_save.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        lib.ck_ffi_save.restype = None

        lib.ck_ffi_load.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        lib.ck_ffi_load.restype = ctypes.c_int

    # ── Helper: convert Python list to c_int8 array ──

    @staticmethod
    def _ops_array(ops: List[int]):
        """Convert a Python list of ints to a ctypes int8 array."""
        arr = (ctypes.c_int8 * len(ops))(*ops)
        return arr, len(ops)

    # ── Pure Math API ──

    def fuse(self, ops: List[int]) -> int:
        arr, n = self._ops_array(ops)
        return self._lib.ck_ffi_fuse(arr, n)

    def fuse2(self, a: int, b: int) -> int:
        return self._lib.ck_ffi_fuse2(a, b)

    def fuse_table(self, ops: List[int], table_id: int = 0) -> int:
        arr, n = self._ops_array(ops)
        return self._lib.ck_ffi_fuse_table(arr, n, table_id)

    def coherence_chain(self, ops: List[int]) -> float:
        arr, n = self._ops_array(ops)
        return self._lib.ck_ffi_coherence_chain(arr, n)

    def information(self, ops: List[int]) -> float:
        arr, n = self._ops_array(ops)
        return self._lib.ck_ffi_information(arr, n)

    def shape(self, ops: List[int]) -> int:
        arr, n = self._ops_array(ops)
        return self._lib.ck_ffi_shape(arr, n)

    def shape_name(self, ops: List[int]) -> str:
        s = self.shape(ops)
        return ['SMOOTH', 'ROLLING', 'JAGGED', 'QUANTUM'][s]

    def bump_signature(self, ops: List[int]) -> int:
        arr, n = self._ops_array(ops)
        return self._lib.ck_ffi_bump_signature(arr, n)

    def is_bump(self, a: int, b: int) -> bool:
        return bool(self._lib.ck_ffi_is_bump(a, b))

    def s_star(self, sigma: float, V: float = 1.0, A: float = 1.0) -> float:
        return self._lib.ck_ffi_s_star(sigma, V, A)

    def coherence_eak(self, E: float, A: float, K: float) -> float:
        return self._lib.ck_ffi_coherence_eak(E, A, K)

    def band(self, C: float) -> int:
        return self._lib.ck_ffi_band(C)

    def band_name(self, C: float) -> str:
        b = self.band(C)
        return ['RED', 'YELLOW', 'GREEN'][b]

    def cl_lookup(self, table_id: int, a: int, b: int) -> int:
        return self._lib.ck_ffi_cl_lookup(table_id, a, b)

    @property
    def t_star(self) -> float:
        return self._lib.ck_ffi_t_star()

    @property
    def num_ops(self) -> int:
        return self._lib.ck_ffi_num_ops()

    def gravity(self, op: int) -> float:
        return self._lib.ck_ffi_gravity(op)

    # ── TL API ──

    def tl_create(self):
        """Create a standalone TransitionLattice. Returns opaque handle."""
        return self._lib.ck_ffi_tl_create()

    def tl_destroy(self, tl_handle):
        self._lib.ck_ffi_tl_destroy(tl_handle)

    def tl_eat_ops(self, tl_handle, ops: List[int]):
        arr, n = self._ops_array(ops)
        self._lib.ck_ffi_tl_eat_ops(tl_handle, arr, n)

    def tl_entropy(self, tl_handle) -> float:
        return self._lib.ck_ffi_tl_entropy(tl_handle)

    def tl_predict(self, tl_handle, current: int) -> Tuple[int, float]:
        prob = ctypes.c_float(0.0)
        op = self._lib.ck_ffi_tl_predict(tl_handle, current, ctypes.byref(prob))
        return op, prob.value

    def tl_total(self, tl_handle) -> int:
        return self._lib.ck_ffi_tl_total(tl_handle)

    def tl_save(self, tl_handle, path: str) -> int:
        return self._lib.ck_ffi_tl_save(tl_handle, path.encode('utf-8'))

    def tl_load(self, tl_handle, path: str) -> int:
        return self._lib.ck_ffi_tl_load(tl_handle, path.encode('utf-8'))

    # ── Organism API ──

    def create_organism(self):
        """Create a full CK organism. Returns opaque handle."""
        return self._lib.ck_ffi_create()

    def destroy_organism(self, handle):
        self._lib.ck_ffi_destroy(handle)

    def organism_tick(self, handle) -> int:
        """One heartbeat tick. Returns phase_bc."""
        return self._lib.ck_ffi_tick(handle)

    def organism_save(self, handle, dir_path: str):
        self._lib.ck_ffi_save(handle, dir_path.encode('utf-8'))

    def organism_load(self, handle, dir_path: str) -> int:
        return self._lib.ck_ffi_load(handle, dir_path.encode('utf-8'))
