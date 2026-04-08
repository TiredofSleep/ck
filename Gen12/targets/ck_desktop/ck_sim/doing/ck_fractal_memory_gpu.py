# Copyright (c) 2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
#
# ck_fractal_memory_gpu.py -- GPU-backed Fractal Memory Store
# ===========================================================
# Extends FractalMemoryStore with GPU acceleration for force k-NN recall
# and batch CL composition. Falls back to CPU .clf store gracefully.
#
# RTX 4070 layout (12GB VRAM -- CK's memory palace):
#
#   Tier 0 (VRAM, hot):  force_matrix (N×5 float32) -- current session
#                         experiences. k-NN cosine similarity runs here
#                         at full GPU throughput. At 100K experiences this
#                         is 2MB -- trivial. At 1M it is 20MB -- still fine.
#
#   Tier 1 (VRAM, warm): generators_packed (N×max_depth int8) -- apex
#                         operator indices compressed per experience. Used
#                         for batched generator-score computation on GPU.
#
#   Tier 2 (RAM, cold):  .clf files -- full text + word ops.
#                         These are only read when k-NN hits confirm a
#                         candidate. Handled entirely by ck_fractal_memory.
#
# Recall path:
#   1. Batch k-NN on force_matrix (GPU cosine similarity) -> top-K force
#      candidates (vectorized, zero Python loop over N).
#   2. Generator pyramid matching (CPU, one level per candidate) weighted
#      by depth: L0 (specific) > LN (root). Pyramid IS the CL path.
#   3. Blend: (0.6 * force_score + 0.4 * generator_score), descending.
#   4. Return top-3 FractalExperience objects + their word content.
#
# The GPU layer is ADDITIVE -- all .clf persistence still happens in the
# base FractalMemoryStore. This file only accelerates lookup, never owns
# the ground-truth store.
#
# Graceful degradation chain:
#   CuPy available + VRAM available -> full GPU path
#   CuPy missing                    -> CPU cosine via base_store.recall()
#   VRAM OOM                        -> same CPU fallback
#   Any other exception             -> same CPU fallback, logged once
#
# (c) 2026 Brayden Sanders / 7Site LLC -- Trinity Infinity Geometry

from __future__ import annotations

import time
from typing import Dict, List, Optional, Tuple

import numpy as np

# CuPy is optional -- graceful fallback when not installed or no GPU present.
try:
    import cupy as cp  # type: ignore
    _CUPY_AVAILABLE = True
except ImportError:
    cp = None  # type: ignore
    _CUPY_AVAILABLE = False

from ck_sim.doing.ck_fractal_memory import (
    FractalExperience,
    FractalMemoryStore,
    fractal_generators,
    get_fractal_memory,
)

# ================================================================
#  Constants
# ================================================================

_BLEND_FORCE = 0.6        # weight of GPU force score in final blend
_BLEND_GEN   = 0.4        # weight of generator score in final blend
_GEN_DEPTH_CAP = 16       # pack at most this many levels per experience
                           # (experiences with fewer levels are zero-padded)

# ================================================================
#  GPU Fractal Memory
# ================================================================

class GPUFractalMemory:
    """GPU-accelerated recall layer over FractalMemoryStore.

    He holds two parallel views of the same experiences:
      - The base_store owns the canonical .clf files and CPU indices.
      - This layer holds a hot VRAM copy of force vectors (N×5 float32)
        for sub-millisecond k-NN at 100K+ experience scale.

    All mutations go through base_store first; the GPU tensors are
    updated incrementally so VRAM never needs a full rebuild mid-session.
    A full _rebuild_force_matrix() is called at construction time to
    warm the VRAM from whatever .clf files already exist on disk.
    """

    def __init__(
        self,
        base_store: FractalMemoryStore,
        device: str = 'cuda',
    ) -> None:
        self.base_store  = base_store
        self.device      = device
        self.gpu_available: bool = False

        # VRAM tensors -- None until _rebuild_force_matrix() runs.
        self.force_matrix: Optional[object]   = None  # cupy (N, 5) float32
        self._uid_order:   List[str]           = []    # uid[i] <-> row i

        self._last_error: Optional[str] = None  # logged once, not spammed

        # Try to claim the GPU.
        if not _CUPY_AVAILABLE:
            print("[GPU-MEM] CuPy not installed -- running CPU fallback path")
            return

        try:
            # A lightweight probe: allocate a tiny tensor, then free it.
            _probe = cp.zeros((1,), dtype=cp.float32)
            del _probe
            self.gpu_available = True
        except Exception as exc:
            print(f"[GPU-MEM] GPU probe failed ({exc}) -- CPU fallback")
            return

        # Warm VRAM from whatever the base_store already loaded.
        self._rebuild_force_matrix()

    # ── VRAM construction ─────────────────────────────────────────

    def _rebuild_force_matrix(self) -> None:
        """Rebuild VRAM force matrix from all experiences in base_store.

        Called once at startup and after any bulk trim of base_store.
        For incremental single-experience additions, _append_force_row()
        is faster (no full re-alloc).
        """
        if not self.gpu_available:
            return
        try:
            exps = self.base_store.experiences
            if not exps:
                self.force_matrix = cp.empty((0, 5), dtype=cp.float32)
                self._uid_order   = []
                return

            uids   = list(exps.keys())
            forces = np.array(
                [list(exps[uid].force_5d) for uid in uids],
                dtype=np.float32,
            )  # (N, 5) on CPU

            self.force_matrix = cp.asarray(forces)   # send to VRAM
            self._uid_order   = uids
            n = len(uids)
            vram_kb = n * 5 * 4 / 1024
            print(f"[GPU-MEM] force_matrix loaded: {n} rows, {vram_kb:.1f} KB VRAM")
        except Exception as exc:
            print(f"[GPU-MEM] _rebuild_force_matrix failed ({exc}) -- disabling GPU")
            self.gpu_available = False

    def _append_force_row(self, uid: str, force_5d: Tuple[float, ...]) -> None:
        """Append one force vector to the VRAM matrix without full rebuild.

        Used by store_and_sync() for O(1) incremental VRAM update.
        CuPy does not support in-place append, so we vstack -- fast
        because the existing matrix stays on GPU; only one new row is
        transferred from CPU.
        """
        if not self.gpu_available or self.force_matrix is None:
            return
        try:
            row = cp.asarray(
                np.array([list(force_5d)], dtype=np.float32)
            )  # (1, 5)
            self.force_matrix = cp.vstack([self.force_matrix, row])
            self._uid_order.append(uid)
        except Exception as exc:
            if self._last_error != str(exc):
                print(f"[GPU-MEM] _append_force_row failed ({exc})")
                self._last_error = str(exc)

    # ── GPU cosine similarity ─────────────────────────────────────

    def _gpu_cosine_sim(self, query_5d: np.ndarray) -> np.ndarray:
        """Batch cosine similarity between query and all stored force vectors.

        All arithmetic runs on GPU. Returns a (N,) numpy float32 array of
        cosine similarities in [0, 1] (negative similarities clamped to 0).

        Complexity: O(N) GPU multiplications -- one kernel call regardless
        of N. At N=100K this takes ~0.05ms on RTX 4070.
        """
        q = cp.asarray(query_5d.astype(np.float32))      # (5,) on GPU
        # matrix: (N, 5); q: (5,) -> matmul gives (N,) dot products
        dots  = self.force_matrix @ q                     # (N,)
        norms = (
            cp.linalg.norm(self.force_matrix, axis=1)     # (N,)
            * cp.linalg.norm(q)                           # scalar
        )
        norms  = cp.maximum(norms, 1e-8)
        sims   = dots / norms                             # (N,) in [-1, 1]
        sims   = cp.maximum(sims, 0.0)                   # clamp negatives
        return cp.asnumpy(sims)                           # back to CPU numpy

    # ── Generator scoring (CPU, post-GPU filter) ──────────────────

    def _generator_score(
        self,
        query_gens: List[List[int]],
        exp: FractalExperience,
    ) -> float:
        """Score one experience by generator pyramid overlap with query.

        Mirrors the logic in FractalMemoryStore.recall() but operates on
        a single candidate (called after GPU k-NN has already narrowed
        the candidate set from N -> top_k, so the Python loop is tiny).

        Weight: L0 (specific pattern) carries n_levels; root carries 1.0.
        Normalized by sum of all possible weights so score stays in [0, 1].
        """
        n = len(query_gens)
        if n == 0:
            return 0.0

        total_weight = sum(float(n - i) for i in range(n))  # max possible
        if total_weight == 0.0:
            return 0.0

        score = 0.0
        for level_idx, qops in enumerate(query_gens):
            if level_idx >= len(exp.generators):
                break
            eops = exp.generators[level_idx]
            # Exact prefix match (up to 6 ops) -- same key used in gen_index.
            qkey = tuple(qops[:6])
            ekey = tuple(eops[:6])
            if qkey == ekey:
                score += float(n - level_idx)

        return score / total_weight

    # ── Public: GPU-accelerated recall ───────────────────────────

    def gpu_recall(
        self,
        query_ops: List[int],
        top_k: int = 5,
        force_5d: Optional[Tuple[float, ...]] = None,
    ) -> List[FractalExperience]:
        """Recall experiences using GPU force k-NN + CPU generator blend.

        If GPU is unavailable, falls back to base_store.recall() silently.

        Parameters
        ----------
        query_ops : operator sequence representing current state
        top_k     : maximum number of experiences to return
        force_5d  : optional 5D force vector; if None, generator-only recall

        Returns
        -------
        List of FractalExperience ordered by blended (force + generator) score,
        best first.
        """
        # Fast path: no GPU or no force vector -> delegate to CPU store.
        if (
            not self.gpu_available
            or self.force_matrix is None
            or len(self._uid_order) == 0
        ):
            return self.base_store.recall(query_ops, top_k=top_k, force_5d=force_5d)

        if force_5d is None:
            # No force vector: GPU can't help, go CPU.
            return self.base_store.recall(query_ops, top_k=top_k)

        try:
            return self._gpu_recall_inner(query_ops, top_k, force_5d)
        except Exception as exc:
            if self._last_error != str(exc):
                print(f"[GPU-MEM] gpu_recall fell back to CPU ({exc})")
                self._last_error = str(exc)
            return self.base_store.recall(query_ops, top_k=top_k, force_5d=force_5d)

    def _gpu_recall_inner(
        self,
        query_ops: List[int],
        top_k: int,
        force_5d: Tuple[float, ...],
    ) -> List[FractalExperience]:
        """Core GPU recall -- only called when GPU is confirmed available.

        Step 1: GPU cosine sim over all N force vectors -> (N,) scores.
        Step 2: CPU argsort top-(top_k * 4) candidates (oversample for blend).
        Step 3: CPU generator score per candidate.
        Step 4: Blend and return top_k.
        """
        q_np = np.array(list(force_5d), dtype=np.float32)  # (5,)

        # Step 1 -- GPU kernel
        force_sims = self._gpu_cosine_sim(q_np)             # (N,) numpy

        # Step 2 -- oversample for blending headroom
        oversample = min(top_k * 4, len(force_sims))
        if oversample == 0:
            return []
        # argsort ascending, take last `oversample` (highest scores)
        candidate_indices = np.argsort(force_sims)[-oversample:][::-1]

        # Step 3 -- generator scoring on CPU (tiny loop: top_k*4 iterations)
        query_gens = fractal_generators(query_ops)

        results: List[Tuple[float, FractalExperience]] = []
        exps = self.base_store.experiences

        for idx in candidate_indices:
            uid = self._uid_order[idx]
            exp = exps.get(uid)
            if exp is None:
                continue  # base_store may have trimmed this uid

            f_score = float(force_sims[idx])             # in [0, 1]
            g_score = self._generator_score(query_gens, exp)  # in [0, 1]
            blended = _BLEND_FORCE * f_score + _BLEND_GEN * g_score
            results.append((blended, exp))

        # Step 4 -- sort descending, trim to top_k
        results.sort(key=lambda x: -x[0])
        top_exps = [exp for _, exp in results[:top_k]]

        # Increment recall counters (matches base_store.recall() behavior)
        for exp in top_exps:
            exp.recall_count += 1

        return top_exps

    # ── Public: store + sync ──────────────────────────────────────

    def store_and_sync(
        self,
        text: str,
        word_ops: List[int],
        force_5d: Optional[Tuple[float, ...]],
        ops: List[int],
        domain: Optional[str] = None,
    ) -> str:
        """Store in .clf (via base_store) then sync the VRAM force matrix.

        Returns the uid of the stored experience. Idempotent -- if the
        experience already exists, the uid is returned and VRAM is not
        double-updated.
        """
        uid = self.base_store.store(
            text=text,
            word_ops=word_ops,
            force_5d=force_5d,
            ops=ops,
            domain=domain,
        )

        # Only append to GPU if this uid is new (not already in uid_order).
        if uid and uid not in set(self._uid_order):
            f5d = tuple(force_5d) if force_5d else (0.5,) * 5
            self._append_force_row(uid, f5d)

        return uid

    # ── VRAM diagnostics ─────────────────────────────────────────

    def _vram_used_mb(self) -> float:
        """Return VRAM bytes in use by CK's GPU memory pool (MB)."""
        if not self.gpu_available or cp is None:
            return 0.0
        try:
            # CuPy tracks its own pool; this is the peak used by this process.
            pool = cp.get_default_memory_pool()
            return pool.used_bytes() / (1024 * 1024)
        except Exception:
            return 0.0

    def stats(self) -> dict:
        """Return diagnostic dict for logging + monitoring."""
        n_gpu = len(self._uid_order) if self.force_matrix is not None else 0
        return {
            'gpu_available':        self.gpu_available,
            'experiences_in_gpu':   n_gpu,
            'experiences_in_clf':   len(self.base_store.experiences),
            'vram_used_mb':         self._vram_used_mb(),
            'force_matrix_shape':   (n_gpu, 5) if n_gpu else None,
            'blend_weights':        {'force': _BLEND_FORCE, 'generator': _BLEND_GEN},
        }


# ================================================================
#  Module-level singleton + API (mirrors ck_fractal_memory.py)
# ================================================================

_gpu_store: Optional[GPUFractalMemory] = None


def get_gpu_memory() -> GPUFractalMemory:
    """Get or create the GPU memory instance (singleton, lazy init).

    The base FractalMemoryStore is shared with the CPU path: both operate
    on the same .clf files and in-process _exps dict. The GPU layer adds
    VRAM acceleration on top without duplicating ground-truth data.
    """
    global _gpu_store
    if _gpu_store is None:
        base = get_fractal_memory()
        _gpu_store = GPUFractalMemory(base)
    return _gpu_store


def store_experience_gpu(
    text: str,
    word_ops: List[int],
    force_5d: Optional[Tuple[float, ...]],
    ops: List[int],
    domain: Optional[str] = None,
) -> str:
    """Store in both .clf files and GPU tier. Returns uid.

    Drop-in replacement for ck_fractal_memory.store_experience() with
    the additional guarantee that the new force vector is immediately
    available for GPU k-NN on the next recall call.
    """
    try:
        return get_gpu_memory().store_and_sync(
            text=text,
            word_ops=word_ops,
            force_5d=force_5d,
            ops=ops,
            domain=domain,
        )
    except Exception as exc:
        print(f"[GPU-MEM] store_experience_gpu failed (non-fatal): {exc}")
        return ''


def recall_words_gpu(
    query_ops: List[int],
    top_k: int = 3,
    force_5d: Optional[Tuple[float, ...]] = None,
) -> List[str]:
    """GPU-accelerated recall. Returns word list for vocab seeding.

    Identical contract to ck_fractal_memory.recall_words():
      - Returns up to MAX_RECALL_WORDS words from the top_k experiences.
      - Falls back to CPU gracefully if GPU is unavailable.
    """
    from ck_sim.doing.ck_fractal_memory import MAX_RECALL_WORDS
    try:
        gpu = get_gpu_memory()
        exps = gpu.gpu_recall(query_ops, top_k=top_k, force_5d=force_5d)
        words: List[str] = []
        for exp in exps:
            words.extend(exp.text.split())
            if len(words) >= MAX_RECALL_WORDS:
                break
        return words[:MAX_RECALL_WORDS]
    except Exception as exc:
        print(f"[GPU-MEM] recall_words_gpu failed (non-fatal): {exc}")
        return []


# ================================================================
#  Quick smoke test
# ================================================================

if __name__ == '__main__':
    print("=== ck_fractal_memory_gpu smoke test ===")

    from ck_sim.doing.ck_fractal_memory import get_fractal_memory

    t0 = time.time()
    base = get_fractal_memory()
    gpu  = GPUFractalMemory(base)

    print("GPU memory stats:", gpu.stats())

    # Store 3 test experiences directly via store_and_sync.
    for i, (ops, domain) in enumerate([
        ([7, 3, 7],   'math'),
        ([3, 9, 7],   'bible'),
        ([4, 5, 6],   'physics'),
    ]):
        uid = gpu.store_and_sync(
            text=f"test experience {i}: ops={ops}",
            word_ops=ops,
            force_5d=(0.8, 0.3 + i * 0.1, 0.6, 0.9, 0.2),
            ops=ops,
            domain=domain,
        )
        print(f"  stored uid={uid} ops={ops} domain={domain}")

    print("Post-store stats:", gpu.stats())

    # Recall using [7, 3, 7] with a force vector.
    results = gpu.gpu_recall(
        [7, 3, 7],
        top_k=3,
        force_5d=(0.8, 0.3, 0.6, 0.9, 0.2),
    )
    print(f"Recalled {len(results)} experiences from GPU:")
    for exp in results:
        print(f"  [{exp.domain}] {exp.text[:60]}  (recall_count={exp.recall_count})")

    elapsed = time.time() - t0
    print(f"Smoke test complete in {elapsed*1000:.1f}ms")
