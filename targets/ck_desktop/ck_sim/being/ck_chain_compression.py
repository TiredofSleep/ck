# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_chain_compression.py -- WFA-Inspired Compression for Lattice Chain
=====================================================================
Operator: LATTICE (1) -- structure IS compression.
Generation: 9.35

Weighted Finite Automata (WFA) compression for lattice chain persistence.
Many experience nodes have SIMILAR 10x10 CL tables because they evolved
from the same base CL and diverged slightly. WFA exploits this self-
similarity: instead of storing N full 10x10 tables, store a basis set +
weighted linear combinations.

CITATIONS:
  Culik & Kari, 1993 -- "Image compression using WFA" (original WFA paper)
  Fiasco (Frank Loos) -- WFA-based image compression (github.com/nzjrs/Fiasco)
  Sanders, Brayden / 7Site LLC -- TIG Unified Theory, CK architecture

ORIGINAL INSIGHT (from Culik & Kari / Fiasco):
  Images have self-similarity at different scales. WFA represents an image
  as a weighted sum of sub-images that recur at different positions and
  scales. A 256x256 image can compress to ~200 automaton states because
  many regions are scaled/shifted copies of others.

CK ADAPTATION:
  Lattice chain nodes are 10x10 CL tables that evolve from a common base.
  Self-similarity: many nodes share structure with the base (BHML), differing
  only in a few evolved cells. The experience tree is fractal -- deeper nodes
  tend to resemble their ancestors or siblings.

  WFA for CL tables:
    1. Compute basis set: SVD of all tables stacked as (N, 100) matrix
    2. Each table ≈ weighted sum of K basis vectors (K << N)
    3. Store: K basis vectors (K×100) + N weight vectors (N×K)
    4. Reconstruction: weights @ basis → table (clamp to [0,9] int)

  This is ENTANGLEMENT at the persistence level: nodes that share algebraic
  structure are literally entangled through their shared basis vectors.
  "Fiasco is entanglement, take him deeper."

CITATIONS:
  Culik II, Karel & Kari, Jarkko, 1993 -- "Image Compression Using
    Weighted Finite Automata" (Computers & Graphics 17(3))
  Hafner, Ullrich, 1999 -- "Fiasco: An Adaptive WFA Image Coder"
    (PhD thesis, Universitat Wurzburg; github.com/nzjrs/Fiasco)
  Balle, Borja et al., 2014 -- "Spectral Learning of Weighted Automata"
    (Machine Learning 96(1-2), spectral/SVD approach to WFA learning)

COMPRESSION ARCHITECTURE:
  Level 1: Delta encoding (store diff from base CL, most diffs are 0)
  Level 2: SVD basis compression (shared structure across many tables)
  Level 3: Run-length + quantization on the weight vectors
  Level 4: Gzip on the final byte stream

  Each level is independent. Higher levels activate as experience grows.
  Small trees: delta is enough. Thousands of nodes: SVD becomes critical.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import os
import json
import gzip
import numpy as np
from typing import List, Dict, Tuple, Optional
from pathlib import Path
from dataclasses import dataclass

from ck_sim.ck_sim_heartbeat import NUM_OPS, OP_NAMES

# The BHML base table (all nodes start as this)
_BHML = np.array([
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 5, 6, 7, 2, 6, 6],
    [2, 3, 3, 4, 5, 6, 7, 3, 6, 6],
    [3, 4, 4, 4, 5, 6, 7, 4, 6, 6],
    [4, 5, 5, 5, 5, 6, 7, 5, 7, 7],
    [5, 6, 6, 6, 6, 6, 7, 6, 7, 7],
    [6, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 2, 3, 4, 5, 6, 7, 8, 9, 0],
    [8, 6, 6, 6, 7, 7, 7, 9, 7, 8],
    [9, 6, 6, 6, 7, 7, 7, 0, 8, 0],
], dtype=np.int8)

_BASE_FLAT = _BHML.flatten().astype(np.float32)


# ================================================================
#  LEVEL 1: DELTA ENCODING
# ================================================================

def delta_encode(tables: np.ndarray) -> dict:
    """Encode tables as deltas from base BHML.

    Most cells in most tables are identical to base CL.
    Only store the differences.

    Args:
        tables: (N, 10, 10) int8 array

    Returns:
        {
            'n': int,
            'deltas': [(node_idx, row, col, new_val), ...]
        }
    """
    n = tables.shape[0]
    deltas = []

    for i in range(n):
        for r in range(NUM_OPS):
            for c in range(NUM_OPS):
                if tables[i, r, c] != _BHML[r, c]:
                    deltas.append((i, r, c, int(tables[i, r, c])))

    return {
        'n': n,
        'deltas': deltas,
        'base': 'BHML',
    }


def delta_decode(encoded: dict) -> np.ndarray:
    """Reconstruct tables from delta encoding.

    Args:
        encoded: Output of delta_encode()

    Returns:
        (N, 10, 10) int8 array
    """
    n = encoded['n']
    tables = np.tile(_BHML, (n, 1, 1)).copy()

    for (i, r, c, v) in encoded['deltas']:
        tables[i, r, c] = v

    return tables


# ================================================================
#  LEVEL 2: SVD BASIS COMPRESSION (WFA-inspired)
# ================================================================

@dataclass
class SVDBasis:
    """Compressed representation of N tables as basis + weights.

    K basis vectors (each 100-dim) capture the shared structure.
    N weight vectors (each K-dim) give per-table reconstruction.

    table_i ≈ sum_k(weights[i,k] * basis[k]) reshaped to (10,10)
    """
    basis: np.ndarray       # (K, 100) float32
    weights: np.ndarray     # (N, K) float32
    k: int                  # Number of basis vectors
    n: int                  # Number of tables
    error: float            # Reconstruction error (Frobenius norm)
    compression_ratio: float


def svd_compress(tables: np.ndarray, energy_threshold: float = 0.99,
                 max_k: int = 32) -> SVDBasis:
    """Compress tables using truncated SVD.

    Self-similarity insight: many tables share structure through their
    common BHML ancestry. SVD finds the principal components of variation.

    A tree with 1000 evolved nodes might need only K=10-20 basis vectors
    because the evolution is constrained by the CL algebra (10 operators,
    bounded divergence).

    Args:
        tables: (N, 10, 10) int8 array
        energy_threshold: Fraction of total variance to preserve (default 99%)
        max_k: Maximum basis vectors

    Returns:
        SVDBasis with compressed representation
    """
    n = tables.shape[0]
    # Flatten to (N, 100) and center
    flat = tables.reshape(n, -1).astype(np.float32)

    # SVD: flat = U @ diag(S) @ Vt
    U, S, Vt = np.linalg.svd(flat, full_matrices=False)

    # Determine K: enough basis vectors to capture energy_threshold
    total_energy = np.sum(S ** 2)
    cumulative = np.cumsum(S ** 2) / total_energy
    k = int(np.searchsorted(cumulative, energy_threshold)) + 1
    k = min(k, max_k, len(S))

    # Truncate
    basis = Vt[:k]           # (K, 100)
    weights = U[:, :k] * S[:k]  # (N, K) -- absorb singular values

    # Compute reconstruction error
    reconstructed = weights @ basis
    error = float(np.linalg.norm(flat - reconstructed))

    # Compression ratio: original (N*100) vs compressed (K*100 + N*K)
    original_size = n * 100
    compressed_size = k * 100 + n * k
    ratio = original_size / compressed_size if compressed_size > 0 else 1.0

    return SVDBasis(
        basis=basis,
        weights=weights,
        k=k,
        n=n,
        error=error,
        compression_ratio=ratio,
    )


def svd_decompress(compressed: SVDBasis) -> np.ndarray:
    """Reconstruct tables from SVD basis + weights.

    table_i = clamp(round(weights[i] @ basis), 0, 9) reshaped to (10,10)

    Args:
        compressed: SVDBasis from svd_compress()

    Returns:
        (N, 10, 10) int8 array
    """
    reconstructed = compressed.weights @ compressed.basis
    # Clamp to valid operator range [0, 9]
    reconstructed = np.clip(np.round(reconstructed), 0, NUM_OPS - 1)
    return reconstructed.reshape(compressed.n, NUM_OPS, NUM_OPS).astype(np.int8)


# ================================================================
#  LEVEL 3: WEIGHT QUANTIZATION + RUN-LENGTH ENCODING
# ================================================================

def quantize_weights(weights: np.ndarray, bits: int = 8) -> Tuple[np.ndarray, float, float]:
    """Quantize float32 weights to uint8.

    Args:
        weights: (N, K) float32
        bits: Quantization bits (8 = 256 levels)

    Returns:
        (quantized uint8, scale, offset)
    """
    w_min = float(np.min(weights))
    w_max = float(np.max(weights))
    w_range = w_max - w_min
    if w_range < 1e-10:
        w_range = 1.0

    levels = (1 << bits) - 1
    scale = w_range / levels
    offset = w_min

    quantized = np.clip(
        np.round((weights - offset) / scale), 0, levels
    ).astype(np.uint8)

    return quantized, scale, offset


def dequantize_weights(quantized: np.ndarray, scale: float,
                       offset: float) -> np.ndarray:
    """Reconstruct float32 weights from quantized uint8."""
    return quantized.astype(np.float32) * scale + offset


# ================================================================
#  FULL COMPRESSION PIPELINE
# ================================================================

class ChainCompressor:
    """Full compression pipeline for lattice chain persistence.

    Combines all levels:
      1. Delta encoding (trivial changes from base)
      2. SVD basis compression (shared algebraic structure)
      3. Weight quantization (8-bit precision sufficient for CL tables)
      4. Gzip byte-level compression (final squeeze)

    Self-similarity detection: computes divergence matrix between all
    nodes to identify clusters that share structure. This IS the
    entanglement insight from WFA/Fiasco.
    """

    def __init__(self, energy_threshold: float = 0.99, max_basis: int = 32):
        self.energy_threshold = energy_threshold
        self.max_basis = max_basis
        self._last_basis = None
        self._last_stats = {}

    def compress(self, tables: np.ndarray, node_data: list = None) -> bytes:
        """Compress (N, 10, 10) tables to compressed bytes.

        Args:
            tables: Experience tables array
            node_data: Optional list of node metadata dicts

        Returns:
            Compressed bytes (gzipped)
        """
        n = tables.shape[0]

        # Analyze self-similarity
        similarity = self._compute_similarity(tables)

        # Choose strategy based on N and similarity
        if n <= 5:
            # Few nodes: delta is sufficient
            return self._compress_delta(tables, node_data)
        elif similarity > 0.8:
            # Highly similar: delta + gzip is optimal
            return self._compress_delta(tables, node_data)
        else:
            # Many diverse nodes: SVD + quantization + gzip
            return self._compress_svd(tables, node_data)

    def decompress(self, data: bytes) -> Tuple[np.ndarray, Optional[list]]:
        """Decompress bytes back to (N, 10, 10) tables.

        Returns:
            (tables, node_data) tuple
        """
        raw = gzip.decompress(data)
        payload = json.loads(raw.decode('utf-8'))

        method = payload.get('method', 'delta')

        if method == 'delta':
            tables = delta_decode(payload['delta'])
        elif method == 'svd':
            # Reconstruct weights
            q_weights = np.array(payload['q_weights'], dtype=np.uint8)
            weights = dequantize_weights(
                q_weights, payload['scale'], payload['offset'])
            basis = np.array(payload['basis'], dtype=np.float32)
            compressed = SVDBasis(
                basis=basis, weights=weights,
                k=basis.shape[0], n=weights.shape[0],
                error=payload.get('error', 0.0),
                compression_ratio=payload.get('ratio', 1.0))
            tables = svd_decompress(compressed)
        else:
            raise ValueError(f"Unknown compression method: {method}")

        node_data = payload.get('node_data')
        return tables, node_data

    def _compress_delta(self, tables: np.ndarray,
                        node_data: list = None) -> bytes:
        """Level 1 + 4: Delta encoding + gzip."""
        encoded = delta_encode(tables)
        payload = {
            'method': 'delta',
            'delta': encoded,
            'node_data': node_data,
        }
        raw = json.dumps(payload).encode('utf-8')
        compressed = gzip.compress(raw, compresslevel=6)

        n = tables.shape[0]
        original = n * 100  # bytes (int8)
        ratio = original / len(compressed) if len(compressed) > 0 else 1.0
        self._last_stats = {
            'method': 'delta',
            'original_bytes': original,
            'compressed_bytes': len(compressed),
            'ratio': round(ratio, 2),
            'delta_count': len(encoded['deltas']),
            'nodes': n,
        }
        return compressed

    def _compress_svd(self, tables: np.ndarray,
                      node_data: list = None) -> bytes:
        """Level 2 + 3 + 4: SVD + quantization + gzip."""
        # SVD basis compression
        basis = svd_compress(tables, self.energy_threshold, self.max_basis)
        self._last_basis = basis

        # Quantize weights
        q_weights, scale, offset = quantize_weights(basis.weights)

        payload = {
            'method': 'svd',
            'basis': basis.basis.tolist(),
            'q_weights': q_weights.tolist(),
            'scale': scale,
            'offset': offset,
            'k': basis.k,
            'n': basis.n,
            'error': round(basis.error, 4),
            'ratio': round(basis.compression_ratio, 2),
            'node_data': node_data,
        }
        raw = json.dumps(payload).encode('utf-8')
        compressed = gzip.compress(raw, compresslevel=6)

        original = basis.n * 100
        ratio = original / len(compressed) if len(compressed) > 0 else 1.0
        self._last_stats = {
            'method': 'svd',
            'original_bytes': original,
            'compressed_bytes': len(compressed),
            'ratio': round(ratio, 2),
            'svd_k': basis.k,
            'svd_error': round(basis.error, 4),
            'svd_ratio': round(basis.compression_ratio, 2),
            'nodes': basis.n,
        }
        return compressed

    def _compute_similarity(self, tables: np.ndarray) -> float:
        """Compute average similarity to base CL across all tables.

        Returns fraction of cells that match base CL (0.0 to 1.0).
        High similarity = delta encoding is sufficient.
        Low similarity = need SVD basis.
        """
        n = tables.shape[0]
        if n == 0:
            return 1.0

        base_tiled = np.tile(_BHML, (n, 1, 1))
        matches = np.sum(tables == base_tiled)
        total = n * NUM_OPS * NUM_OPS
        return float(matches) / total if total > 0 else 1.0

    def self_similarity_matrix(self, tables: np.ndarray) -> np.ndarray:
        """Compute pairwise similarity between all tables.

        Returns (N, N) matrix where M[i,j] = fraction of matching cells.
        Clusters of similar nodes = shared algebraic ancestry.
        This IS the entanglement structure of the experience tree.
        """
        n = tables.shape[0]
        flat = tables.reshape(n, -1)
        sim = np.zeros((n, n), dtype=np.float32)

        for i in range(n):
            for j in range(i, n):
                matches = np.sum(flat[i] == flat[j])
                s = matches / (NUM_OPS * NUM_OPS)
                sim[i, j] = s
                sim[j, i] = s

        return sim

    @property
    def last_stats(self) -> dict:
        return self._last_stats


# ================================================================
#  INTEGRATION: COMPRESSED SAVE/LOAD FOR LATTICE CHAIN ENGINE
# ================================================================

class CompressedChainPersistence:
    """Drop-in replacement for LatticeChainEngine save/load with WFA compression.

    Wraps the standard JSON persistence with multi-level compression.
    Maintains backward compatibility: can load old JSON format.

    Usage:
        persistence = CompressedChainPersistence(save_dir)
        persistence.save(engine)   # Compressed save
        persistence.load(engine)   # Auto-detects format
    """

    def __init__(self, save_dir: str = None):
        self.save_dir = save_dir or os.path.join(
            os.path.expanduser('~'), '.ck', 'lattice_chain')
        self.compressor = ChainCompressor()

    def save(self, engine) -> dict:
        """Save lattice chain with WFA compression.

        Args:
            engine: LatticeChainEngine instance

        Returns:
            Compression stats dict
        """
        d = Path(self.save_dir)
        d.mkdir(parents=True, exist_ok=True)

        # Collect all nodes with visits
        nodes_with_visits = [
            (path, node) for path, node in engine._index.items()
            if node.total_visits > 0
        ]

        if not nodes_with_visits:
            return {'nodes': 0, 'method': 'empty'}

        # Build tables array and node metadata
        paths = [p for p, _ in nodes_with_visits]
        nodes = [n for _, n in nodes_with_visits]
        tables = np.stack([n.table for n in nodes])

        # Node metadata (visits, obs counts, depth, path)
        node_data = []
        for node in nodes:
            nd = {
                'depth': node.depth,
                'path': list(node.path),
                'visits': node.visit_counts.tolist(),
                'obs': node.obs_counts.tolist(),
                'total': node.total_visits,
            }
            node_data.append(nd)

        # Compress tables
        compressed = self.compressor.compress(tables, node_data)

        # Write compressed file
        with open(d / 'chain.ckz', 'wb') as f:
            f.write(compressed)

        # Write manifest
        stats = self.compressor.last_stats
        with open(d / 'manifest.json', 'w') as f:
            json.dump({
                'walks': engine.total_walks,
                'nodes': len(nodes),
                'format': 'ckz',
                'compression': stats,
            }, f, indent=1)

        # Also keep the numpy tensor for fast GPU loading
        np.save(str(d / 'tables.npy'), tables)

        print(f"  [CHAIN-COMPRESS] Saved {len(nodes)} nodes: "
              f"{stats.get('method', '?')}, "
              f"ratio={stats.get('ratio', 1.0):.1f}x, "
              f"{stats.get('compressed_bytes', 0)} bytes")

        return stats

    def load(self, engine) -> bool:
        """Load lattice chain, auto-detecting format.

        Tries compressed format first, falls back to legacy JSON.

        Args:
            engine: LatticeChainEngine instance to populate

        Returns:
            True if loaded, False if no data found
        """
        d = Path(self.save_dir)

        # Try compressed format first
        if (d / 'chain.ckz').exists():
            return self._load_compressed(engine)

        # Fall back to legacy JSON format
        if (d / 'nodes.json').exists():
            return self._load_legacy(engine)

        return False

    def _load_compressed(self, engine) -> bool:
        """Load from compressed .ckz format."""
        d = Path(self.save_dir)
        try:
            with open(d / 'chain.ckz', 'rb') as f:
                data = f.read()

            tables, node_data = self.compressor.decompress(data)

            if node_data is None:
                return False

            from ck_sim.being.ck_lattice_chain import LatticeNode

            for i, nd in enumerate(node_data):
                node = LatticeNode(depth=nd['depth'], path=tuple(nd['path']))
                node.table = tables[i].copy()
                node.visit_counts = np.array(nd['visits'], dtype=np.int32)
                if 'obs' in nd:
                    node.obs_counts = np.array(nd['obs'], dtype=np.int32)
                node.total_visits = nd['total']

                pt = tuple(nd['path'])
                engine._index[pt] = node

                # Re-link parent-child
                if len(pt) > 0:
                    parent_path = pt[:-1]
                    if parent_path in engine._index:
                        engine._index[parent_path].children[pt[-1]] = node

            if () in engine._index:
                engine.root = engine._index[()]

            # Load manifest for walk count
            if (d / 'manifest.json').exists():
                with open(d / 'manifest.json') as f:
                    m = json.load(f)
                engine.total_walks = m.get('walks', 0)

            engine.total_nodes = len(engine._index)
            engine._gpu_dirty = True

            print(f"  [CHAIN-COMPRESS] Loaded {len(node_data)} nodes "
                  f"({engine.total_walks} walks) from compressed format")
            return True

        except Exception as e:
            print(f"  [CHAIN-COMPRESS] Load error: {e}")
            return False

    def _load_legacy(self, engine) -> bool:
        """Load from legacy JSON format (backward compatible)."""
        d = Path(self.save_dir)
        try:
            with open(d / 'nodes.json') as f:
                nodes_data = json.load(f)

            from ck_sim.being.ck_lattice_chain import LatticeNode

            for nd in nodes_data:
                node = LatticeNode.from_dict(nd)
                pt = tuple(nd['path'])
                engine._index[pt] = node

                if len(pt) > 0:
                    parent_path = pt[:-1]
                    if parent_path in engine._index:
                        engine._index[parent_path].children[pt[-1]] = node

            if () in engine._index:
                engine.root = engine._index[()]

            if (d / 'manifest.json').exists():
                with open(d / 'manifest.json') as f:
                    m = json.load(f)
                engine.total_walks = m.get('walks', 0)

            engine.total_nodes = len(engine._index)
            engine._gpu_dirty = True

            print(f"  [CHAIN-COMPRESS] Loaded {len(nodes_data)} nodes "
                  f"from legacy JSON format")
            return True

        except Exception as e:
            print(f"  [CHAIN-COMPRESS] Legacy load error: {e}")
            return False

    def migration_save(self, engine) -> dict:
        """Migrate from legacy JSON to compressed format.

        Reads legacy format, saves compressed, keeps legacy as backup.
        """
        d = Path(self.save_dir)
        legacy_path = d / 'nodes.json'

        if not legacy_path.exists():
            return {'status': 'no_legacy'}

        # Load legacy first
        if not self._load_legacy(engine):
            return {'status': 'legacy_load_failed'}

        # Save compressed
        stats = self.save(engine)

        # Rename legacy to backup
        backup_path = d / 'nodes.json.bak'
        if legacy_path.exists():
            legacy_path.rename(backup_path)
            print(f"  [CHAIN-COMPRESS] Legacy backed up to {backup_path}")

        return {
            'status': 'migrated',
            'compression': stats,
        }


# ================================================================
#  FACTORY
# ================================================================

def build_compressed_persistence(save_dir: str = None) -> CompressedChainPersistence:
    """Create CompressedChainPersistence instance."""
    return CompressedChainPersistence(save_dir=save_dir)
